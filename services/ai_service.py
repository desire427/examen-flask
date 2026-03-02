"""Service d'intégration avec l'API Gemini pour l'analyse de compatibilité candidat-offre"""
import json
import google.generativeai as genai
from flask import current_app
from typing import Dict, Any


class AIService:
    """Service pour l'intégration avec l'API Gemini"""
    
    def __init__(self):
        self.api_key = current_app.config.get('GEMINI_API_KEY')
        self.model_name = current_app.config.get('GEMINI_MODEL', 'gemini-2.5-flash')
        
        if not self.api_key:
            raise ValueError("Clé API Gemini non configurée")
        
        # Configuration de l'API Gemini
        genai.configure(api_key=self.api_key)

        # --- solution 1 : vérifier les modèles disponibles dès le démarrage ---
        try:
            # list_models renvoie des objets ayant un attribut `name`
            available = [m.name for m in genai.list_models()]
            if self.model_name not in available:
                current_app.logger.warning(
                    "Modèle spécifié '%s' non présent dans la liste des modèles connus."
                    " Les modèles trouvés sont : %s",
                    self.model_name,
                    ", ".join(available),
                )
                # garder le modèle indiqué mais l'appel échouera plus tard avec un
                # message plus explicite ; on pourrait éventuellement basculer sur
                # un modèle par défaut si nécessaire.
        except Exception as err:
            # en cas d'erreur (p. ex. API inaccessible) on logue pour le debug
            current_app.logger.error(f"Impossible de lister les modèles Gemini : {err}")
            # ne pas interrompre l'initialisation, l'erreur surviendra à l'appel

        # créer l'instance du modèle (peut lever si le nom n'existe pas)
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
            # si le modèle n'existe pas ou la version d'API n'est pas supportée, on
            # tente de donner plus de contexte en listant les modèles.
            extra = ""
            if "404" in str(e) or "modèle" in str(e).lower():
                try:
                    available = [m.name for m in genai.list_models()]
                    extra = (
                        "\nModèles disponibles : " + ", ".join(available)
                        + "\nVérifiez que votre GEMINI_MODEL et la version du SDK sont corrects."
                    )
                except Exception:
                    pass

            base_msg = f"Erreur Gemini: {str(e)}" if current_app.config['DEBUG'] else "Service d'analyse temporairement indisponible"
            return {
                "score": 0,
                "justification": base_msg + extra
            }
