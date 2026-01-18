from flask import Blueprint, request, jsonify
from models.models import db, OffreEmploi, Candidature
from models.schemas import offre_schema, offres_schema, candidats_schema
from services.services import AIService

offer_bp = Blueprint('offers', __name__)

@offer_bp.route('/offers', methods=['POST'])
def create_offer():
    """Création d'une offre d'emploi"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Données JSON requises"}), 400
        
        # Validation avec Marshmallow
        offer = offre_schema.load(data, session=db.session)
        
        # Sauvegarde en base
        db.session.add(offer)
        db.session.commit()
        
        return jsonify(offre_schema.dump(offer)), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

@offer_bp.route('/offers', methods=['GET'])
def get_offers():
    """Récupérer toutes les offres"""
    try:
        offers = OffreEmploi.query.all()
        return jsonify(offres_schema.dump(offers)), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@offer_bp.route('/offers/<int:offer_id>', methods=['GET'])
def get_offer(offer_id):
    """Récupérer une offre spécifique"""
    try:
        offer = OffreEmploi.query.get_or_404(offer_id)
        return jsonify(offre_schema.dump(offer)), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 404

@offer_bp.route('/offers/<int:offer_id>/candidates', methods=['GET'])
def get_offer_candidates(offer_id):
    """Liste tous les candidats ayant postulé à une offre spécifique"""
    try:
        # Vérifier que l'offre existe
        offer = OffreEmploi.query.get_or_404(offer_id)
        
        # Récupérer les candidatures pour cette offre
        applications = Candidature.query.filter_by(offre_id=offer_id).all()
        
        # Extraire les candidats
        candidates = [app.candidat for app in applications]
        
        return jsonify(candidats_schema.dump(candidates)), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@offer_bp.route('/offers/<int:offer_id>/analyze-match', methods=['POST'])
def analyze_match(offer_id):
    """Analyser la compatibilité entre une offre et un candidat"""
    try:
        # Vérifier que l'offre existe
        offer = OffreEmploi.query.get_or_404(offer_id)
        
        # Récupérer les données du candidat
        data = request.get_json()
        if not data:
            return jsonify({"error": "Données JSON requises"}), 400
        
        candidat_id = data.get('candidat_id')
        if not candidat_id:
            return jsonify({"error": "candidat_id est requis"}), 400
        
        # Récupérer le candidat
        from models.models import Candidat
        candidat = Candidat.query.get_or_404(candidat_id)
        
        # Initialiser le service IA
        ai_service = AIService()
        
        # Analyser la compatibilité
        result = ai_service.analyze_compatibility(
            offre_description=offer.description,
            candidat_bio=candidat.bio
        )
        
        return jsonify(result), 200
        
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500