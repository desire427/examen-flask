# Smart Recruit API

Une API RESTful moderne développée avec Flask pour la gestion de processus de recrutement. Cette application se distingue par l'intégration d'une **Intelligence Artificielle (Google Gemini)** capable d'analyser automatiquement la compatibilité entre le profil d'un candidat et une offre d'emploi.

## Fonctionnalités

*   **Gestion des Candidats** : Inscription, consultation et gestion des profils candidats.
*   **Gestion des Offres** : Publication d'offres d'emploi avec compétences requises.
*   **Système de Candidature** : Permet de lier un candidat à une offre.
*   **IA & Matching Intelligent** : Analyse sémantique via Google Gemini pour générer un score de compatibilité (0-100%) et une justification détaillée.
*   **Architecture Modulaire** : Utilisation de Blueprints, Service Layer et validation stricte des données.

## Technologies Utilisées

*   **Backend** : Python 3.12, Flask
*   **Base de Données** : PostgreSQL, SQLAlchemy (ORM)
*   **Validation** : Marshmallow
*   **IA** : Google Generative AI (Gemini Pro)
*   **Sécurité & Config** : Python-dotenv, CORS

## Installation et Démarrage

### 1. Prérequis
*   Python 3.10 ou supérieur
*   PostgreSQL installé et en cours d'exécution
*   Une clé API Google Gemini (disponible sur Google AI Studio)

### 2. Installation

Cloner le dépôt et installer les dépendances :

```bash
git clone [<votre-repo-url>](https://github.com/desire427/examen-flask.git)
cd smart-recruit-api

# Création de l'environnement virtuel
python3 -m venv venv
source venv/bin/activate  # Sur Windows : venv\Scripts\activate

# Installation des paquets
pip install -r requirements.txt
```

### 3. Configuration

Créez un fichier `.env` à la racine du projet en copiant la structure suivante :

```env
FLASK_ENV=development
SECRET_KEY=votre_cle_secrete_securisee

# Configuration PostgreSQL (Adaptez user:password)
DATABASE_URL=postgresql://postgres:votre_mot_de_passe@localhost:5432/smart_recruit_db

# Configuration IA
GEMINI_API_KEY=votre_cle_api_gemini_ici
# Modèles disponibles: gemini-2.5-flash, gemini-2.5-pro, gemini-2.0-flash
GEMINI_MODEL=gemini-2.5-flash
```

### 4. Base de Données

Assurez-vous de créer la base de données dans PostgreSQL avant de lancer l'application :

```sql
CREATE DATABASE smart_recruit_db;
```
*Les tables seront créées automatiquement par SQLAlchemy au premier lancement.*



---

### 🔧 Résolution des erreurs de modèle Gemini

Si vous recevez une erreur du type :
```
404 models/gemini-1.5-pro is not found for API version v1beta
```

**Cause** : Les modèles `gemini-1.5-*` sont dépréciés. Google a migré vers les séries 2.0 et 2.5.

**Solution** : Mettez à jour `GEMINI_MODEL` dans votre `.env` :

1. **Pour une API rapide et efficace** :
   ```env
   GEMINI_MODEL=gemini-2.5-flash
   ```

2. **Pour une API plus puissante** :
   ```env
   GEMINI_MODEL=gemini-2.5-pro
   ```

3. **Pour voir tous les modèles disponibles** :
   ```python
   import google.generativeai as genai
   genai.configure(api_key="VOTRE_CLE")
   for m in genai.list_models():
       if 'generateContent' in m.supported_generation_methods:
           print(m.name)
   ```

4. **Mettez à jour le SDK** (version ≥ 0.9.0 requis) :
   ```bash
   pip install --upgrade google-generativeai
   ```

---

```bash
python3 app.py
```
L'API sera accessible sur `http://127.0.0.1:5000`.

## Documentation de l'API

---

**Guide de test professionnel (Postman / cURL)**

Ce guide fournit des requêtes prêtes à l'emploi pour tester chaque endpoint de l'API Smart‑Recruit. Remplacez `{{BASE_URL}}` par `http://127.0.0.1:5000` (ou l'URL de votre instance).

Préparer Postman :
- Menu → Environments → Create → ajoutez la variable `BASE_URL` = `http://127.0.0.1:5000`.
- Pour chaque requête POST, définir l'en‑tête `Content-Type: application/json`.

1) Créer un candidat — POST `{{BASE_URL}}/api/candidates`

URL: `{{BASE_URL}}/api/candidates`

Body (raw JSON):
```json
{
   "nom": "Jean Dupont",
   "email": "jean.dupont@example.com",
   "bio": "Développeur Python avec 5 ans d'expérience",
   "diplome": "Master Informatique"
}
```

cURL (copier/coller dans un terminal) :
```bash
curl -s -X POST "{{BASE_URL}}/api/candidates" \
   -H "Content-Type: application/json" \
   -d '{"nom":"Jean Dupont","email":"jean.dupont@example.com","bio":"Développeur Python avec 5 ans d\'expérience","diplome":"Master Informatique"}'
```

2) Lister les candidats — GET `{{BASE_URL}}/api/candidates`

```bash
curl -s "{{BASE_URL}}/api/candidates"
```

3) Récupérer un candidat — GET `{{BASE_URL}}/api/candidates/<id>`

```bash
curl -s "{{BASE_URL}}/api/candidates/1"
```

4) Créer une offre — POST `{{BASE_URL}}/api/offers`

Body (raw JSON):
```json
{
   "titre": "Développeur Python Senior",
   "description": "Recherche développeur Python expérimenté pour projets innovants",
   "competences_cles": ["Python", "Django", "Flask", "PostgreSQL"],
   "salaire": 55000
}
```

cURL :
```bash
curl -s -X POST "{{BASE_URL}}/api/offers" \
   -H "Content-Type: application/json" \
   -d '{"titre":"Développeur Python Senior","description":"Recherche développeur Python expérimenté pour projets innovants","competences_cles":["Python","Django","Flask","PostgreSQL"],"salaire":55000}'
```

5) Lister les offres — GET `{{BASE_URL}}/api/offers`

```bash
curl -s "{{BASE_URL}}/api/offers"
```

6) Récupérer une offre — GET `{{BASE_URL}}/api/offers/<id>`

```bash
curl -s "{{BASE_URL}}/api/offers/1"
```

7) Soumettre une candidature — POST `{{BASE_URL}}/api/apply`

Body (raw JSON):
```json
{
   "candidat_id": 1,
   "offre_id": 1
}
```

cURL :
```bash
curl -s -X POST "{{BASE_URL}}/api/apply" \
   -H "Content-Type: application/json" \
   -d '{"candidat_id":1,"offre_id":1}'
```

8) Liste des candidats d'une offre — GET `{{BASE_URL}}/api/offers/<id>/candidates`

```bash
curl -s "{{BASE_URL}}/api/offers/1/candidates"
```

9) Analyser la compatibilité (Gemini) — POST `{{BASE_URL}}/api/offers/<id>/analyze-match`

Body (raw JSON) attendu :
```json
{ "candidat_id": 1 }
```

cURL :
```bash
curl -s -X POST "{{BASE_URL}}/api/offers/1/analyze-match" \
   -H "Content-Type: application/json" \
   -d '{"candidat_id":1}'
```

Remarques importantes :
- L'endpoint d'analyse utilise la clé `GEMINI_API_KEY` du fichier `.env`. Sans clé valide, l'appel renverra une erreur ou un message explicatif.
- Le service tente d'extraire du JSON même si le modèle entoure sa réponse d'un bloc Markdown (```json ... ```). Si la réponse n'est pas du JSON valide, vérifiez le contenu renvoyé par Gemini.

10) Vérification santé — GET `{{BASE_URL}}/health`

```bash
curl -s "{{BASE_URL}}/health"
```

Importer rapidement dans Postman :
1. Créez un nouvel environnement `Local` avec la variable `BASE_URL` = `http://127.0.0.1:5000`.
2. Dans Postman → Import → Raw Text, collez un des exemples cURL ci‑dessus ; Postman proposera d'importer la requête.
3. Dupliquez la requête et adaptez l'URL / body pour chaque endpoint.

Si vous souhaitez, je peux générer et ajouter une collection Postman prête à l'import (fichier JSON) dans le dépôt.


### Candidats
| Méthode | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/api/candidates` | Liste tous les candidats |
| `POST` | `/api/candidates` | Créer un candidat |
| `GET` | `/api/candidates/<id>` | Détails d'un candidat |

**Exemple JSON (Création) :**
```json
{
    "nom": "Prims Parolier",
    "email": "primsparolier@gmail.com",
    "bio": "Développeur Python Senior experte en Flask.",
    "diplome": "Master Informatique"
}
```

### Offres d'Emploi
| Méthode | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/api/offers` | Liste toutes les offres |
| `POST` | `/api/offers` | Créer une offre |
| `POST` | `/api/offers/<id>/analyze-match` | **IA** : Analyser la compatibilité avec un candidat |

**Exemple JSON (Offre) :**
```json
{
    "titre": "Backend Developer",
    "description": "Expertise Python requise.",
    "competences_cles": ["Python", "SQL"],
    "salaire": 100000
}
```

### Candidatures
| Méthode | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/api/apply` | Postuler à une offre (`candidat_id`, `offre_id`) |
| `GET` | `/api/applications` | Voir toutes les candidatures |

## Auteur  
Alpohonse Desire HABA  
Projet réalisé dans le cadre de l'examen Flask.
