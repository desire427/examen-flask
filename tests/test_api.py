import unittest
import json
from app import create_app
from config import TestingConfig
from models.models import db

class SmartRecruitAPITestCase(unittest.TestCase):
    """Tests pour l'API Smart-Recruit"""
    
    def setUp(self):
        """Configuration avant chaque test"""
        self.app = create_app(TestingConfig)
        self.client = self.app.test_client()
        
        with self.app.app_context():
            db.create_all()
    
    def tearDown(self):
        """Nettoyage après chaque test"""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
    
    def test_create_candidate(self):
        """Test de création d'un candidat"""
        data = {
            "nom": "Jean Dupont",
            "email": "jean.dupont@email.com",
            "bio": "Développeur Python avec 5 ans d'expérience",
            "diplome": "Master Informatique"
        }
        
        response = self.client.post('/api/candidates', 
                                   data=json.dumps(data),
                                   content_type='application/json')
        
        self.assertEqual(response.status_code, 201)
        json_data = response.get_json()
        self.assertEqual(json_data['nom'], "Jean Dupont")
        self.assertEqual(json_data['email'], "jean.dupont@email.com")
    
    def test_create_candidate_duplicate_email(self):
        """Test de création avec email dupliqué"""
        data = {
            "nom": "Jean Dupont",
            "email": "jean.dupont@email.com",
            "bio": "Développeur Python",
            "diplome": "Master"
        }
        
        # Première création
        self.client.post('/api/candidates', 
                        data=json.dumps(data),
                        content_type='application/json')
        
        # Seconde création avec même email
        response = self.client.post('/api/candidates',
                                   data=json.dumps(data),
                                   content_type='application/json')
        
        self.assertEqual(response.status_code, 409)
    
    def test_create_offer(self):
        """Test de création d'une offre"""
        data = {
            "titre": "Développeur Python Senior",
            "description": "Recherche développeur Python expérimenté pour projets innovants",
            "competences_cles": ["Python", "Django", "Flask", "PostgreSQL"],
            "salaire": 55000
        }
        
        response = self.client.post('/api/offers',
                                   data=json.dumps(data),
                                   content_type='application/json')
        
        self.assertEqual(response.status_code, 201)
        json_data = response.get_json()
        self.assertEqual(json_data['titre'], "Développeur Python Senior")
        self.assertEqual(len(json_data['competences_cles']), 4)
    
    def test_create_application(self):
        """Test de soumission d'une candidature"""
        # Créer un candidat
        candidat_data = {
            "nom": "Marie Martin",
            "email": "marie.martin@email.com",
            "bio": "Data Scientist",
            "diplome": "PhD"
        }
        candidat_response = self.client.post('/api/candidates',
                                            data=json.dumps(candidat_data),
                                            content_type='application/json')
        candidat_id = candidat_response.get_json()['id']
        
        # Créer une offre
        offre_data = {
            "titre": "Data Scientist",
            "description": "Analyse de données",
            "competences_cles": ["Python", "Machine Learning", "SQL"],
            "salaire": 60000
        }
        offre_response = self.client.post('/api/offers',
                                         data=json.dumps(offre_data),
                                         content_type='application/json')
        offre_id = offre_response.get_json()['id']
        
        # Soumettre une candidature
        application_data = {
            "candidat_id": candidat_id,
            "offre_id": offre_id
        }
        
        response = self.client.post('/api/apply',
                                   data=json.dumps(application_data),
                                   content_type='application/json')
        
        self.assertEqual(response.status_code, 201)
    
    def test_get_offer_candidates(self):
        """Test de récupération des candidats d'une offre"""
        # Créer offre et candidats
        offre_data = {
            "titre": "Test Offre",
            "description": "Description test",
            "competences_cles": ["Test"],
            "salaire": 30000
        }
        offre_response = self.client.post('/api/offers',
                                         data=json.dumps(offre_data),
                                         content_type='application/json')
        offre_id = offre_response.get_json()['id']
        
        # Test avec aucune candidature
        response = self.client.get(f'/api/offers/{offre_id}/candidates')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.get_json()), 0)
    
    def test_health_check(self):
        """Test de l'endpoint de santé"""
        response = self.client.get('/health')
        self.assertEqual(response.status_code, 200)
        json_data = response.get_json()
        self.assertEqual(json_data['status'], "healthy")

if __name__ == '__main__':
    unittest.main()