from flask import Blueprint, request, jsonify
from models.models import db, Candidat
from models.schemas import candidat_schema, candidats_schema
from services.database_service import DatabaseService

candidate_bp = Blueprint('candidates', __name__)
db_service = DatabaseService()

@candidate_bp.route('/candidates', methods=['POST'])
def create_candidate():
    """Inscription d'un candidat"""
    try:
        # Validation des données
        data = request.get_json()
        if not data:
            return jsonify({"error": "Données JSON requises"}), 400
        
        # Vérification de l'unicité de l'email
        existing_candidate = Candidat.query.filter_by(email=data.get('email')).first()
        if existing_candidate:
            return jsonify({"error": "Un candidat avec cet email existe déjà"}), 409
        
        # Validation avec Marshmallow (fournir la session SQLAlchemy pour la désérialisation)
        candidate = candidat_schema.load(data, session=db.session)
        
        # Sauvegarde en base
        db.session.add(candidate)
        db.session.commit()
        
        return jsonify(candidat_schema.dump(candidate)), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

@candidate_bp.route('/candidates', methods=['GET'])
def get_candidates():
    """Récupérer tous les candidats"""
    try:
        candidates = Candidat.query.all()
        return jsonify(candidats_schema.dump(candidates)), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@candidate_bp.route('/candidates/<int:candidate_id>', methods=['GET'])
def get_candidate(candidate_id):
    """Récupérer un candidat spécifique"""
    try:
        candidate = Candidat.query.get_or_404(candidate_id)
        return jsonify(candidat_schema.dump(candidate)), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 404