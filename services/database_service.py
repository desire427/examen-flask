from models.models import db
from contextlib import contextmanager

class DatabaseService:
    """Service pour la gestion de la base de données"""
    
    @contextmanager
    def session_scope(self):
        """Context manager pour gérer les sessions de base de données"""
        session = db.session
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
    
    def create_tables(self):
        """Créer toutes les tables"""
        db.create_all()
    
    def drop_tables(self):
        """Supprimer toutes les tables"""
        db.drop_all()
    
    def init_db(self, app):
        """Initialiser la base de données avec l'application"""
        db.init_app(app)
        with app.app_context():
            self.create_tables()