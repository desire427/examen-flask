from marshmallow import Schema, fields, validate, validates, ValidationError
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from models.models import db, OffreEmploi, Candidat, Candidature

class OffreEmploiSchema(SQLAlchemyAutoSchema):
    """Schéma de validation pour les offres d'emploi"""
    class Meta:
        model = OffreEmploi
        sqlalchemy_session = db.session
        load_instance = True
        include_fk = True
    
    titre = fields.Str(required=True, validate=validate.Length(min=1, max=200))
    description = fields.Str(required=True, validate=validate.Length(min=10))
    competences_cles = fields.List(fields.Str(), required=True)
    salaire = fields.Float(validate=validate.Range(min=0))
    
    @validates('competences_cles')
    def validate_competences_cles(self, value):
        if not isinstance(value, list):
            raise ValidationError('Les compétences clés doivent être une liste')
        if len(value) == 0:
            raise ValidationError('Au moins une compétence clé est requise')

class CandidatSchema(SQLAlchemyAutoSchema):
    """Schéma de validation pour les candidats"""
    class Meta:
        model = Candidat
        sqlalchemy_session = db.session
        load_instance = True
        include_fk = True
    
    nom = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    email = fields.Email(required=True)
    bio = fields.Str(required=True, validate=validate.Length(min=10))
    diplome = fields.Str(required=True, validate=validate.Length(min=1, max=100))

class CandidatureSchema(SQLAlchemyAutoSchema):
    """Schéma de validation pour les candidatures"""
    class Meta:
        model = Candidature
        sqlalchemy_session = db.session
        load_instance = True
        include_fk = True
    
    candidat_id = fields.Int(required=True)
    offre_id = fields.Int(required=True)

# Instances des schémas
offre_schema = OffreEmploiSchema()
offres_schema = OffreEmploiSchema(many=True)
candidat_schema = CandidatSchema()
candidats_schema = CandidatSchema(many=True)
candidature_schema = CandidatureSchema()
candidatures_schema = CandidatureSchema(many=True)

# Schémas pour les réponses
class MatchAnalysisSchema(Schema):
    """Schéma pour la réponse d'analyse de compatibilité"""
    score = fields.Int(required=True, validate=validate.Range(min=0, max=100))
    justification = fields.Str(required=True, validate=validate.Length(max=200))

match_analysis_schema = MatchAnalysisSchema()