import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Configuration de base"""
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    DEBUG = os.getenv('FLASK_ENV') == 'development'
    
    # Base de données
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://postgres:desire@localhost:5432/smart_recruit_db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Configuration API Gemini
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
    GEMINI_MODEL = os.getenv('GEMINI_MODEL', 'gemini-pro')
    
    # Configuration CORS
    CORS_HEADERS = 'Content-Type'
    
class DevelopmentConfig(Config):
    """Configuration développement"""
    DEBUG = True
    
class ProductionConfig(Config):
    """Configuration production"""
    DEBUG = False
    
class TestingConfig(Config):
    """Configuration tests"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'