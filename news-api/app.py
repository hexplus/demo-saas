from flask import Flask, jsonify,request
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, create_refresh_token, get_jwt_identity, get_jwt
from models.db import db, User
from helpers.roles import roles_required
from helpers.helpers import get_adapters, get_adapters_by_country_code, get_styles, get_tones, get_complexities, get_summary_lengths, get_social_networks, get_summary_types
from dotenv import load_dotenv
import os
from flask_cors import CORS
from adapters.cri import contraloria, ice, poderjudicial, muni_san_jose, aresep, earth, esph, fecoba
from adapters.world import cnn_es
from datetime import timedelta
from ai.prompt import run_prompt

load_dotenv()

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = (
    f"mysql+mysqlconnector://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
    f"@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}"
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.getenv('SECRET_KEY')
API_VERSION = os.getenv('API_VERSION')
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=8)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)

# ADAPTERS:

CGR = 'CGR'
ICE = 'ICE'
AYA = 'AYA'
CNNE = 'CNNE'
PJ = 'PJ'
MPSJ = 'MPSJ'
ARSP = 'ARSP'
EARTH = 'EARTH'
ESPH = 'ESPH'
FECOBA = 'FECOBA'


db.init_app(app)
jwt = JWTManager(app)
CORS(app)


with app.app_context():
    db.create_all()


@app.route('/', methods=['GET'])
def index():
    return jsonify({
        "version": API_VERSION,
    })


@app.route('/register', methods=['POST'])
@jwt_required()
@roles_required('admin')
def register_user():
    data = request.get_json()
    
    result = User.add_user(
        username=data['username'],
        country=data['country'],
        language=data['language'],
        password=data['password'],
        role=data['role']
    )

    if isinstance(result, User):
        return jsonify({"msg": "User registered successfully", "user": result.username}), 201
    else:        
        return jsonify({"msg": "Error registering user", "error": result}), 400


@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        if not data or 'username' not in data or 'password' not in data:
            return jsonify({"msg": "Missing credentials"}), 400
        

        user = User.query.filter_by(username=data['username']).first()
        

        if user and user.check_password(data['password']):

            access_token = create_access_token(
                identity=user.username,
                additional_claims={"role": user.role}
            )
            refresh_token = create_refresh_token(
                identity=user.username, 
                additional_claims={"role": user.role}
            )            
            
            return jsonify({
                "access_token": access_token,
                "refresh_token": refresh_token,
                "token_type": "Bearer",
                "expires_in": 3600,
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "role": user.role,
                    "language": user.language,
                    "country": user.country
                }
            }), 200
        
        return jsonify({"msg": "Invalid credentials"}), 401

    except Exception as e:        
        return jsonify({"msg": "Server error", "error": str(e)}), 500




@app.route('/auth/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    try:
        current_user = get_jwt_identity()
        claims = get_jwt()    
        user_role = claims.get('role')
        
        access_token = create_access_token(
            identity=current_user,
            additional_claims={"role": user_role}
        )
        refresh_token = create_refresh_token(
            identity=current_user,
            additional_claims={"role": user_role}
        )

        return jsonify({
                "access_token": access_token,
                "refresh_token": refresh_token
            }), 200

    except Exception as e:
        return jsonify({"msg": "Unable to refresh token", "error": str(e)}), 500
    


@app.route('/headlines/<adapter>', methods=['GET'])
@jwt_required()
@roles_required('admin', 'manager', 'operator')
def headlines(adapter):
    # adapter = request.args.get('adapter')
    slug = request.args.get('slug')

    if not adapter:
        return jsonify({
            "error": "Invalid 'adapter' parameter."
        }), 400
    else:
        adapter.upper()

    if adapter == CGR:
        headlines = contraloria.get_headlines()        
    elif adapter == ICE:
        headlines = ice.get_headlines()
    elif adapter == CNNE:
        if slug:
            headlines = cnn_es.get_headlines(slug=slug) 
        else:
            headlines = cnn_es.get_headlines() 
    elif adapter == PJ:
        headlines = poderjudicial.get_headlines()
    elif adapter == MPSJ:
        headlines = muni_san_jose.get_headlines()
    elif adapter == ARSP:
        headlines = aresep.get_headlines()
    elif adapter == EARTH:
        headlines = earth.get_headlines()
    elif adapter == ESPH:
        headlines = esph.get_headlines()
    elif adapter == FECOBA:
        headlines = fecoba.get_headlines()
    else:
       headlines = {}

    return jsonify(headlines), 200


@app.route('/content/<adapter>', methods=['GET'])
@jwt_required()
@roles_required('admin', 'manager', 'operator')
def news(adapter):
    slug = request.args.get('slug')    
    id = request.args.get('id')
    
    if not adapter:
        return jsonify({
            "error": "Invalid 'adapter' parameter."
        }), 400
    elif not slug:
        return jsonify({
            "error": "'Slug' parameter required."
        }), 400
    else:
        adapter.upper()


    if adapter == CGR:
        content = contraloria.get_content(slug)
    if adapter == ICE:
        content = ice.get_content(slug)
    if adapter == CNNE:
        content = cnn_es.get_content(slug)
    if adapter == ARSP:
        content = aresep.get_content(slug)
    if adapter == FECOBA:
        content = fecoba.get_content(slug)
    if adapter == PJ:
        content = poderjudicial.get_content(slug)
    if adapter == EARTH:
        content = earth.get_content(slug)
    if adapter == MPSJ:
        content = muni_san_jose.get_content(slug)

    return jsonify(content), 200


@app.route('/adapters', methods=['GET'])
@jwt_required()
@roles_required('admin', 'manager', 'operator')
def adapters():
    data = get_adapters()
    return jsonify({
        "adapters": data
    }), 200


@app.route('/styles', methods=['GET'])
@jwt_required()
@roles_required('admin', 'manager', 'operator')
def styles():
    data = get_styles()
    return jsonify({
        "styles": data
    }), 200

@app.route('/tones', methods=['GET'])
@jwt_required()
@roles_required('admin', 'manager', 'operator')
def tones():
    data = get_tones()
    return jsonify({
        "tones": data
    }), 200


@app.route('/complexities', methods=['GET'])
@jwt_required()
@roles_required('admin', 'manager', 'operator')
def complexities():
    data = get_complexities()
    return jsonify({
        "complexities": data
    }), 200


@app.route('/summary-types', methods=['GET'])
@jwt_required()
@roles_required('admin', 'manager', 'operator')
def summary_types():
    data = get_summary_types()
    return jsonify({
        "summary_types": data
    }), 200


@app.route('/summary-lengths', methods=['GET'])
@jwt_required()
@roles_required('admin', 'manager', 'operator')
def summary_lengths():
    data = get_summary_lengths()
    return jsonify({
        "summary_lengths": data
    }), 200


@app.route('/social-networks', methods=['GET'])
@jwt_required()
@roles_required('admin', 'manager', 'operator')
def social_networks():
    data = get_social_networks()
    return jsonify({
        "social_networks": data
    }), 200

@app.route('/adapters/<country_code>', methods=['GET'])
@jwt_required()
@roles_required('admin', 'manager', 'operator')
def adapters_by_country(country_code):
    data = get_adapters_by_country_code(country_code)
    return jsonify({
        "adapters": data
    }), 200

@app.route('/categories/<adapter>', methods=['GET'])
@jwt_required()
@roles_required('admin', 'manager', 'operator')
def categories(adapter):
    # adapter = request.args.get('adapter')
    if not adapter:
        return jsonify({
            "error": "Invalid 'adapter' parameter."
        }), 400
    else:
        adapter.upper()

    if adapter == CGR:        
        categories =  {
            'categories': []
        }
    elif adapter == ICE:
        categories =  {
            'categories': []
        }
    elif adapter == CNNE:
        categories = cnn_es.get_categories()
    elif adapter == PJ:
        categories =  {
            'categories': []
        }
    elif adapter == MPSJ:
        categories = {
            'categories': []
        }
    elif adapter == ARSP:
        categories = {
            'categories': []
        }
    elif adapter == EARTH:
        categories = {
            'categories': []
        }  
    elif adapter == ESPH:
        categories = {
            'categories': []
        }
    elif adapter == FECOBA:
        categories = {
            'categories': []
        }
    else:
       categories = {}

    return jsonify(categories), 200

@app.route('/ai', methods=['POST'])
@jwt_required()
@roles_required('admin', 'manager', 'operator')
def ai():
    config = request.get_json()
    response = run_prompt(config);

    return jsonify({
        "response": response
    }), 200

# Rutas protegidas con roles
# @app.route('/configurar', methods=['POST'])
# @jwt_required()
# @role_required('moderator')
# def configurar():
#     return jsonify({"msg": "Configuración realizada con éxito"}), 200

# @app.route('/operar', methods=['POST'])
# @jwt_required()
# @role_required('operator')
# def operar():
#     return jsonify({"msg": "Operación realizada con éxito"}), 200

if __name__ == '__main__':
    app.run(debug=True)
