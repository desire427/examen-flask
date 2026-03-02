import unittest
from types import SimpleNamespace
from flask import Flask

# we import the service inside tests to allow patches to apply
from services.ai_service import AIService

class AIServiceTestCase(unittest.TestCase):
    """Tests unitaires pour AIService (sans appel réseau réel)"""

    def setUp(self):
        self.app = Flask(__name__)
        self.app.config['GEMINI_API_KEY'] = 'fake-key'
        # start with a model that will *not* be in the fake list
        self.app.config['GEMINI_MODEL'] = 'imaginaire-foo'
        self.logger_messages = []

        # intercept warnings emitted via current_app.logger
        class DummyLogger:
            def warning(inner, msg, *args, **kwargs):
                self.logger_messages.append(msg % args if args else msg)
            def error(inner, msg, *args, **kwargs):
                self.logger_messages.append(msg % args if args else msg)

        self.app.logger = DummyLogger()

    def test_init_logs_warning_when_model_missing(self):
        """AIService doit logguer un avertissement si le modèle demandé est absent"""
        # patch list_models to return a small set
        import google.generativeai as genai
        original = genai.list_models

        def fake_list():
            return [SimpleNamespace(name='cnn'), SimpleNamespace(name='rnn')]

        genai.list_models = fake_list

        with self.app.app_context():
            svc = AIService()  # should not raise
            self.assertIn('imaginaire-foo', svc.model_name)
            # check warning was logged
            self.assertTrue(any('Modèle spécifié' in msg for msg in self.logger_messages))

        # restore
        genai.list_models = original

    def test_error_message_contains_model_list(self):
        """Si l'appel à generate_content échoue (404), on ajoute la liste"""
        import google.generativeai as genai
        class DummyModel:
            def generate_content(self, prompt):
                raise Exception('404 Not Found: modèle introuvable')

        # patch list_models and GenerativeModel
        original_list = genai.list_models
        original_model = genai.GenerativeModel

        genai.list_models = lambda: [SimpleNamespace(name='abc')]
        genai.GenerativeModel = lambda name: DummyModel()

        with self.app.app_context():
            self.app.config['DEBUG'] = True
            svc = AIService()
            result = svc.analyze_compatibility('offre', 'bio')
            self.assertEqual(result['score'], 0)
            self.assertIn('Modèles disponibles', result['justification'])

        genai.list_models = original_list
        genai.GenerativeModel = original_model


if __name__ == '__main__':
    unittest.main()
