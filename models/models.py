from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class OffreEmploi(db.Model):
    """Modèle pour les offres d'emploi"""
    __tablename__ = 'offres_emploi'
    
    id = db.Column(db.Integer, primary_key=True)
    titre = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    competences_cles = db.Column(db.JSON, nullable=False)  # Liste de compétences
    salaire = db.Column(db.Float, nullable=True)
    date_creation = db.Column(db.DateTime, default=datetime.utcnow)
    date_modification = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relations
    candidatures = db.relationship('Candidature', back_populates='offre', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<OffreEmploi {self.titre}>'

class Candidat(db.Model):
    """Modèle pour les candidats"""
    __tablename__ = 'candidats'
    
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    bio = db.Column(db.Text, nullable=False)
    diplome = db.Column(db.String(100), nullable=False)
    date_inscription = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relations
    candidatures = db.relationship('Candidature', back_populates='candidat', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Candidat {self.nom}>'

class Candidature(db.Model):
    """Modèle pour les candidatures"""
    __tablename__ = 'candidatures'
    
    id = db.Column(db.Integer, primary_key=True)
    candidat_id = db.Column(db.Integer, db.ForeignKey('candidats.id'), nullable=False)
    offre_id = db.Column(db.Integer, db.ForeignKey('offres_emploi.id'), nullable=False)
    date_depot = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relations
    candidat = db.relationship('Candidat', back_populates='candidatures')
    offre = db.relationship('OffreEmploi', back_populates='candidatures')
    
    # Contrainte d'unicité
    __table_args__ = (
        db.UniqueConstraint('candidat_id', 'offre_id', name='unique_candidature'),
    )
    
    def __repr__(self):
        return f'<Candidature {self.candidat_id} -> {self.offre_id}>'