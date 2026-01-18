from flask import Flask, jsonify, request  # <-- Ajouter 'request' ici
from flask_cors import CORS
from sqlalchemy import inspect, text
from config import DevelopmentConfig
from models.models import db
from services.database_service import DatabaseService
from routes.candidate_routes import candidate_bp
from routes.offer_routes import offer_bp
from routes.application_routes import application_bp

def create_app(config_class=DevelopmentConfig):
    """Factory pour créer l'application Flask"""
    
    # Création de l'application
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Configuration CORS
    CORS(app, resources={r"/*": {"origins": "*"}})
    
    # Initialisation de la base de données
    db.init_app(app)
    
    # Création des tables au démarrage
    with app.app_context():
        try:
            db.create_all()
            # Test de connexion sécurisé (remplace votre test qui plantait)
            db.session.execute(text('SELECT 1'))
            
            inspector = inspect(db.engine)
            tables = inspector.get_table_names()
            print(f"\n * SUCCÈS BDD (PostgreSQL) : Connecté à {app.config['SQLALCHEMY_DATABASE_URI']}")
            print(f" * Tables trouvées dans la base : {tables}\n")
        except Exception as e:
            print(f"\nERREUR CRITIQUE DB: Impossible de se connecter à la base de données: {e}")
            print("Assurez-vous d'avoir exécuté: CREATE DATABASE smart_recruit_db;\n")
    
    # Enregistrement des blueprints
    app.register_blueprint(candidate_bp, url_prefix='/api')
    app.register_blueprint(offer_bp, url_prefix='/api')
    app.register_blueprint(application_bp, url_prefix='/api')
    
    # Route de santé
    @app.route('/health', methods=['GET'])
    def health_check():
        """Endpoint de vérification de santé"""
        return jsonify({
            "status": "healthy",
            "service": "Smart-Recruit API",
            "version": "1.0.0"
        })
    
    @app.route('/api/test', methods=['GET'])
    def api_test():
        return jsonify({
            "status": "success",
            "message": "API test endpoint",
            "timestamp": "2026-01-17T15:00:00Z"
        })
    
    # Route racine
    @app.route('/')
    def index():
        return jsonify({
            "message": "Bienvenue sur Smart-Recruit API",
            "version": "1.0.0",
            "endpoints": {
                "health": "/health",
                "candidates": "/api/candidates",
                "offers": "/api/offers",
                "applications": "/api/applications"
            }
        })
    
    # Gestionnaire d'erreurs global
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"error": "Ressource non trouvée"}), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        app.logger.error(f"Erreur serveur: {error}")
        return jsonify({"error": "Erreur interne du serveur"}), 500
    
    # Middleware pour le logging
    @app.after_request
    def after_request(response):
        """Logging des requêtes"""
        app.logger.info(
            f"{request.remote_addr} {request.method} {request.path} {response.status_code}"
        )
        return response
    
    return app

if __name__ == '__main__':
    app = create_app()
    
    # Configuration du logging
    import logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Lancement de l'application
    app.run(host='0.0.0.0', port=5000, debug=app.config['DEBUG'])