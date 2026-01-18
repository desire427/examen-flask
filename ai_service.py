import json
import google.generativeai as genai
from flask import current_app
from typing import Dict, Any, Optional

class AIService:
    """Service pour l'intégration avec l'API Gemini"""
    
    def __init__(self):
        self.api_key = current_app.config.get('GEMINI_API_KEY')
        self.model_name = current_app.config.get('GEMINI_MODEL', 'gemini-pro')
        
        if not self.api_key:
            raise ValueError("Clé API Gemini non configurée")
        
        # Configuration de l'API Gemini
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel(self.model_name)
    
    def analyze_compatibility(self, offre_description: str, candidat_bio: str) -> Dict[str, Any]:
        """
        Analyse la compatibilité entre une offre et un candidat
        
        Args:
            offre_description: Description de l'offre
            candidat_bio: Bio du candidat
            
        Returns:
            Dict avec 'score' et 'justification'
        """
        # Construction du prompt structuré
        prompt = f"""
        Analyse la compatibilité entre cette offre et ce candidat.
        
        OFFRE:
        {offre_description}
        
        CANDIDAT:
        {candidat_bio}
        
        Réponds EXCLUSIVEMENT au format JSON avec les clés suivantes:
        1. 'score': un nombre entre 0 et 100 représentant le pourcentage de compatibilité
        2. 'justification': une brève explication de 200 caractères maximum
        
        Format de réponse attendu:
        {{
            "score": 85,
            "justification": "Le candidat possède 3 des 5 compétences requises..."
        }}
        """
        
        try:
            # Appel à l'API Gemini
            response = self.model.generate_content(prompt)
            
            # Extraction du JSON de la réponse
            response_text = response.text.strip()
            
            # Nettoyage du texte pour extraire le JSON
            if '```json' in response_text:
                response_text = response_text.split('```json')[1].split('```')[0].strip()
            elif '```' in response_text:
                response_text = response_text.split('```')[1].split('```')[0].strip()
            
            # Parsing du JSON
            result = json.loads(response_text)
            
            # Validation des données reçues
            if 'score' not in result or 'justification' not in result:
                raise ValueError("Réponse de l'IA mal formatée")
            
            # S'assurer que le score est entre 0 et 100
            result['score'] = max(0, min(100, int(result['score'])))
            
            # Tronquer la justification si nécessaire
            result['justification'] = result['justification'][:200]
            
            return result
            
        except json.JSONDecodeError as e:
            current_app.logger.error(f"Erreur de parsing JSON de la réponse IA: {e}")
            return {
                "score": 0,
                "justification": "Erreur lors de l'analyse de compatibilité"
            }
        except Exception as e:
            current_app.logger.error(f"Erreur lors de l'appel à l'API Gemini: {e}")
            return {
                "score": 0,
                "justification": "Service d'analyse temporairement indisponible"
            }
    
    @staticmethod
    def get_ai_service() -> 'AIService':
        """Factory pour obtenir une instance du service IA"""
        return AIService()