# Smart Recruit API

Une API RESTful moderne développée avec Flask pour la gestion de processus de recrutement. Cette application se distingue par l'intégration d'une **Intelligence Artificielle (Google Gemini)** capable d'analyser automatiquement la compatibilité entre le profil d'un candidat et une offre d'emploi.

## 📋 Fonctionnalités

*   **Gestion des Candidats** : Inscription, consultation et gestion des profils candidats.
*   **Gestion des Offres** : Publication d'offres d'emploi avec compétences requises.
*   **Système de Candidature** : Permet de lier un candidat à une offre.
*   **IA & Matching Intelligent** : Analyse sémantique via Google Gemini pour générer un score de compatibilité (0-100%) et une justification détaillée.
*   **Architecture Modulaire** : Utilisation de Blueprints, Service Layer et validation stricte des données.

## 🛠 Technologies Utilisées

*   **Backend** : Python 3.12, Flask
*   **Base de Données** : PostgreSQL, SQLAlchemy (ORM)
*   **Validation** : Marshmallow
*   **IA** : Google Generative AI (Gemini Pro)
*   **Sécurité & Config** : Python-dotenv, CORS

## 🚀 Installation et Démarrage

### 1. Prérequis
*   Python 3.10 ou supérieur
*   PostgreSQL installé et en cours d'exécution
*   Une clé API Google Gemini (disponible sur Google AI Studio)

### 2. Installation

Cloner le dépôt et installer les dépendances :

```bash
git clone <votre-repo-url>
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
GEMINI_MODEL=gemini-pro
```

### 4. Base de Données

Assurez-vous de créer la base de données dans PostgreSQL avant de lancer l'application :

```sql
CREATE DATABASE smart_recruit_db;
```
*Les tables seront créées automatiquement par SQLAlchemy au premier lancement.*

### 5. Lancement

```bash
python3 app.py
```
L'API sera accessible sur `http://127.0.0.1:5000`.

## 📚 Documentation de l'API

### Candidats
| Méthode | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/api/candidates` | Liste tous les candidats |
| `POST` | `/api/candidates` | Créer un candidat |
| `GET` | `/api/candidates/<id>` | Détails d'un candidat |

**Exemple JSON (Création) :**
```json
{
    "nom": "Alice Martin",
    "email": "alice@example.com",
    "bio": "Développeuse Python Senior experte en Flask.",
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
    "salaire": 55000
}
```

### Candidatures
| Méthode | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/api/apply` | Postuler à une offre (`candidat_id`, `offre_id`) |
| `GET` | `/api/applications` | Voir toutes les candidatures |

## 👤 Auteur
Projet réalisé dans le cadre de l'examen Flask.