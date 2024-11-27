from app import app
from models.db import db, User
from werkzeug.security import generate_password_hash, check_password_hash

with app.app_context():
    
    password = ''
    username = ''

    existing_admin = User.query.filter_by(username=username).first()

    if existing_admin:
        print("El usuario administrador ya existe.")
    else:        
        admin_user = User(
            username='',
            email='',
            country='CRI',
            language='SPA',
            role='admin',
            status=True
        )        

        
        
        admin_user.password_hash = generate_password_hash(password, method='pbkdf2:sha256')

        if check_password_hash(admin_user.password_hash, password):
            print("Password match")
        else:
            print("Password does not match")

        db.session.add(admin_user)
        db.session.commit()
        print("Usuario administrador creado exitosamente.")
