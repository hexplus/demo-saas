from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import NoResultFound
import uuid
from sqlalchemy import Column, Integer, String, Boolean

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    country = db.Column(db.String(3), nullable=False)
    language = db.Column(db.String(3), nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(50), nullable=False)  # admin, moderator, operator, demo
    status = db.Column(db.Boolean, default=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    

    def add_user(username, email, country, language, password, role):    
        new_user = User(
            username=username,
            email=email,
            country=country,
            language=language,
            role=role,
            status=False
        )
                
        new_user.set_password(password)

        try:        
            db.session.add(new_user)
            db.session.commit()
            return new_user
        except Exception as e:            
            db.session.rollback()
            return str(e)
    
    def edit_user(user_id, email=None, username=None, country=None, language=None, role=None, status=None):
        try:            
            user = User.query.get(user_id)

            if not user:
                return "User not found."
            
            if username:
                user.username = username
            if email:
                user.email = email
            if country:
                user.country = country
            if language:
                user.language = language
            if role:
                user.role = role
            if status is not None:
                user.status = status
            
            db.session.commit()
            return user
        except Exception as e:            
            db.session.rollback()
            return str(e)
    
    def delete_user(user_id):
        try:            
            user = User.query.get(user_id)

            if not user:
                return "User not found."
            
            db.session.delete(user)
            db.session.commit()
            return f"User {user.username} has been deleted."
        except Exception as e:            
            db.session.rollback()
            return str(e)





class Headlines(db.Model):
    __tablename__ = 'headlines'
    id = db.Column(db.String(36), primary_key=True)
    date = db.Column(db.Date(), nullable=False)
    title = db.Column(db.String(256), nullable=False)
    link = db.Column(db.String(256), nullable=False)
    adapter = db.Column(db.String(10), nullable=False)

    @staticmethod
    def get_headline_by_id(id):
        try:            
            headline = db.session.query(Headlines).filter_by(id=id).one()
            return headline
        except NoResultFound:
            return None 
        except Exception as e:            
            print(f"Error al buscar el titular: {str(e)}")
            return None
        
    @staticmethod
    def get_headlines_by_date(target_date):
        try:            
            headlines = db.session.query(Headlines).filter_by(date=target_date).all()
            return headlines if headlines else None
        except Exception as e:            
            print(f"Error al buscar titulares por fecha: {str(e)}")
            return None
        
    @staticmethod
    def get_headlines_by_adapter(adapter, limit=10, offset=0):
        try:            
            headlines = (
                db.session.query(Headlines)
                .filter_by(adapter=adapter)
                .limit(limit)
                .offset(offset)
                .all()
            )
            return headlines
        except Exception as e:            
            print(f"Error al obtener titulares: {str(e)}")
            return None



class News(db.Model):
    __tablename__ = 'news'
    id = db.Column(db.String(36), primary_key=True)
    body = db.Column(db.String(256), nullable=False)
    status = db.Column(db.Boolean, nullable=False, default=True)


    @staticmethod
    def get_news_by_id(id):
        try:            
            news_item = db.session.query(News).filter_by(id=id).one()
            return news_item
        except NoResultFound:
            return None
        except Exception as e:            
            print(f"Error al obtener la noticia: {str(e)}")
            return None
        

    # How to:
    # news_item = New.get_new_by_id("123e4567-e89b-12d3-a456-426614174000")
    # news_item.set_status_disabled()
    def set_status_disabled(self):
        try:
            self.status = False
            db.session.commit()
            print(f"El estado de la noticia con ID {self.id} ha sido cambiado a False.")
        except Exception as e:            
            db.session.rollback()
            print(f"Error al cambiar el estado: {str(e)}")


    
class Drafts(db.Model):
    __tablename__ = 'drafts'

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    id_user = Column(Integer, nullable=False)
    body = Column(String(256), nullable=False)
    status = Column(Boolean, nullable=False, default=True)

    @staticmethod
    def get_draft_by_id(draft_id):        
        try:
            draft = db.session.query(Drafts).filter_by(id=draft_id).one()
            return draft
        except NoResultFound:
            return None
        except Exception as e:
            print(f"Error al obtener el borrador: {str(e)}")
            return None

    def disable_status(self):        
        try:
            self.status = False
            db.session.commit()
            print(f"El estado del borrador con ID {self.id} ha sido cambiado a False.")
        except Exception as e:
            db.session.rollback()
            print(f"Error al cambiar el estado: {str(e)}")

    
    @staticmethod
    def set_draft(id_user, body, draft_id=None):        
        try:
            if draft_id:                
                draft = Drafts.get_draft_by_id(draft_id)
                if draft:
                    draft.body = body
                    print(f"Borrador {draft_id} actualizado.")
                else:
                    print(f"No se encontró un borrador con ID {draft_id}.")
                    return None
            else:                
                draft = Drafts(id_user=id_user, body=body)
                db.session.add(draft)
                print(f"Nuevo borrador creado con ID: {draft.id}")

            db.session.commit()
            return draft
        except Exception as e:
            db.session.rollback()
            print(f"Error al crear o actualizar el borrador: {str(e)}")
            return None
        

    @staticmethod
    def delete_draft(draft_id):        
        try:            
            draft = Drafts.get_draft_by_id(draft_id)
            if draft:
                db.session.delete(draft)
                db.session.commit()
                print(f"Borrador con ID {draft_id} eliminado exitosamente.")
                return True
            else:
                print(f"No se encontró un borrador con ID {draft_id}.")
                return False
        except Exception as e:
            db.session.rollback()
            print(f"Error al eliminar el borrador: {str(e)}")
            return False
        


class Adapter(db.Model):
    __tablename__ = 'adapters'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    code = db.Column(db.String(5), nullable=False)
    country = db.Column(db.String(3), nullable=False)
    status = Column(Boolean, nullable=False, default=True)
    
    def add_adapter(name, code, status=False):
        try:
            new_adapter = Adapter(name=name, code=code, status=status)
            db.session.add(new_adapter)
            db.session.commit()
            return {"message": "Adapter added successfully", "adapter": new_adapter.id}, 201
        except Exception as e:
            db.session.rollback()
            return {"message": f"Error adding adapter: {str(e)}"}, 400
    
    def delete_adapter(adapter_id):
        adapter = Adapter.query.get(adapter_id)
        if not adapter:
            return {"message": "Adapter not found"}, 404
        
        try:
            db.session.delete(adapter)
            db.session.commit()
            return {"message": "Adapter deleted successfully"}, 200
        except Exception as e:
            db.session.rollback()
            return {"message": f"Error deleting adapter: {str(e)}"}, 400
    
    def edit_adapter(adapter_id, name=None, code=None, status=None):
        adapter = Adapter.query.get(adapter_id)
        if not adapter:
            return {"message": "Adapter not found"}, 404

        try:
            if name:
                adapter.name = name
            if code:
                adapter.code = code
            if status is not None:
                adapter.status = status

            db.session.commit()
            return {"message": "Adapter updated successfully"}, 200
        except Exception as e:
            db.session.rollback()
            return {"message": f"Error updating adapter: {str(e)}"}, 400

    # Retornar todos los Adapters
    def get_all_adapters():
        adapters = Adapter.query.all()
        return adapters
        # return jsonify([{
        #     "id": adapter.id,
        #     "name": adapter.name,
        #     "code": adapter.code,
        #     "status": adapter.status
        # } for adapter in adapters]), 200   
