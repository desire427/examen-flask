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
    
    def analyze_compatibility(self, offre_description: str, candidat_bio: str, offre_competences: list = None) -> Dict[str, Any]:
        """
        Analyse la compatibilité entre une offre et un candidat
        
        Args:
            offre_description: Description de l'offre
            candidat_bio: Bio du candidat
            offre_competences: Liste des compétences requises (optionnel)
            
        Returns:
            Dict avec 'score' et 'justification'
        """
        competences_str = ", ".join(offre_competences) if offre_competences else "Non spécifiées"
        
        # Construction du prompt structuré
        prompt = f"""
        Agis comme un expert en recrutement. Analyse la compatibilité entre cette offre et ce candidat.
        
        OFFRE:
        Description: {offre_description}
        Compétences techniques requises: {competences_str}
        
        CANDIDAT:
        Profil/Bio: {candidat_bio}
        
        Réponds UNIQUEMENT avec un objet JSON valide (sans Markdown).
        Les clés requises sont:
        1. 'score': un entier de 0 à 100.
        2. 'justification': une explication courte (max 200 caractères).
        
        Exemple de réponse:
        {{
            "score": 85,
            "justification": "Le profil correspond bien aux attentes..."
        }}
        """
        
        # Paramètres de sécurité pour éviter les blocages (faux positifs)
        safety_settings = [
            {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"}
        ]
        
        try:
            # Appel à l'API Gemini
            response = self.model.generate_content(prompt, safety_settings=safety_settings)
            
            # Extraction du JSON de la réponse
            try:
                response_text = response.text.strip()
            except ValueError:
                # Si response.text échoue, c'est souvent dû aux filtres de sécurité
                current_app.logger.warning(f"Réponse IA bloquée. Feedback: {response.prompt_feedback}")
                return {
                    "score": 0,
                    "justification": "Analyse bloquée par les filtres de sécurité de l'IA."
                }
            
            # Nettoyage du texte pour extraire le JSON
            # Suppression des balises markdown si présentes
            response_text = response_text.replace('```json', '').replace('```', '')
            
            # On cherche la première accolade ouvrante et la dernière fermante
            start_idx = response_text.find('{')
            end_idx = response_text.rfind('}')
            if start_idx != -1 and end_idx != -1:
                response_text = response_text[start_idx:end_idx+1]
            
            # Parsing du JSON
            result = json.loads(response_text)
            
            # Validation des données reçues
            if 'score' not in result or 'justification' not in result:
                raise ValueError("Réponse de l'IA mal formatée")
            
            # Nettoyage du score (si c'est une string "85%")
            score_val = result['score']
            if isinstance(score_val, str):
                # On garde que les chiffres
                score_val = ''.join(filter(str.isdigit, score_val))
                if not score_val: score_val = "0"
            
            # S'assurer que le score est entre 0 et 100
            result['score'] = max(0, min(100, int(score_val)))
            
            # Tronquer la justification si nécessaire
            result['justification'] = result['justification'][:200]
            
            return result
            
        except json.JSONDecodeError as e:
            current_app.logger.error(f"Erreur de parsing JSON de la réponse IA: {e}")
            # Tentative de récupération du score via regex en dernier recours
            import re
            match = re.search(r'score["\']?\s*:\s*(\d+)', response_text, re.IGNORECASE)
            if match:
                return {
                    "score": int(match.group(1)),
                    "justification": "Score extrait partiellement (format IA non standard)."
                }
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