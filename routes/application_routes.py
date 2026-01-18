from flask import Blueprint, request, jsonify
from models.models import db, Candidature, Candidat, OffreEmploi
from models.schemas import candidature_schema

application_bp = Blueprint('applications', __name__)

@application_bp.route('/apply', methods=['POST'])
def create_application():
    """Soumettre une candidature à une offre"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Données JSON requises"}), 400
        
        # Vérifier que le candidat existe
        candidat_id = data.get('candidat_id')
        candidat = db.session.get(Candidat, candidat_id)
        if not candidat:
            return jsonify({"error": "Candidat non trouvé"}), 404
        
        # Vérifier que l'offre existe
        offre_id = data.get('offre_id')
        offre = db.session.get(OffreEmploi, offre_id)
        if not offre:
            return jsonify({"error": "Offre non trouvée"}), 404
        
        # Vérifier si la candidature existe déjà
        existing_application = Candidature.query.filter_by(
            candidat_id=candidat_id,
            offre_id=offre_id
        ).first()
        
        if existing_application:
            return jsonify({"error": "Candidature déjà existante"}), 409
        
        # Créer la candidature
        application = Candidature(
            candidat_id=candidat_id,
            offre_id=offre_id
        )
        
        # Sauvegarde en base
        db.session.add(application)
        db.session.commit()
        
        return jsonify(candidature_schema.dump(application)), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

@application_bp.route('/applications', methods=['GET'])
def get_applications():
    """Récupérer toutes les candidatures"""
    try:
        applications = Candidature.query.all()
        result = []
        
        for app in applications:
            app_data = candidature_schema.dump(app)
            app_data['candidat'] = {
                'id': app.candidat.id,
                'nom': app.candidat.nom,
                'email': app.candidat.email
            }
            app_data['offre'] = {
                'id': app.offre.id,
                'titre': app.offre.titre
            }
            result.append(app_data)
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500