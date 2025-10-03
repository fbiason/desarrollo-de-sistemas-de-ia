import sys
import os
import unittest

# Agregar el directorio padre al path para poder importar los módulos
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from knowledge_base.expert_system import EdTechExpertSystem
from knowledge_base.facts import Symptom, SystemInfo, ServerStatus

class TestEdTechExpertSystem(unittest.TestCase):
    """Tests for the EdTech Expert System."""
    
    def setUp(self):
        """Set up the expert system for each test."""
        self.expert_system = EdTechExpertSystem()
    
    def test_login_credentials_issue(self):
        """Test diagnosis for login credentials issue."""
        symptoms_data = {
            "symptoms": [
                {"type": "login", "description": "cannot_login"}
            ],
            "system_info": {
                "browser": "Chrome",
                "browser_version": "90.0"
            },
            "server_status": {
                "is_online": True
            }
        }
        
        diagnosis = self.expert_system.diagnose(symptoms_data)
        
        self.assertEqual(diagnosis["diagnosis"], "login")
        self.assertEqual(diagnosis["cause"], "user")
        self.assertGreater(diagnosis["confidence"], 0.7)
    
    def test_video_slow_connection(self):
        """Test diagnosis for video not loading due to slow connection."""
        symptoms_data = {
            "symptoms": [
                {"type": "video", "description": "video_not_loading"}
            ],
            "system_info": {
                "browser": "Chrome",
                "browser_version": "90.0",
                "connection_type": "cellular"
            }
        }
        
        diagnosis = self.expert_system.diagnose(symptoms_data)
        
        self.assertEqual(diagnosis["diagnosis"], "video")
        self.assertEqual(diagnosis["cause"], "user")
        self.assertGreater(diagnosis["confidence"], 0.7)
    
    def test_chat_server_issues(self):
        """Test diagnosis for chat lag due to server issues."""
        symptoms_data = {
            "symptoms": [
                {"type": "chat", "description": "chat_lag"}
            ],
            "server_status": {
                "is_online": True,
                "reported_issues": 10
            }
        }
        
        diagnosis = self.expert_system.diagnose(symptoms_data)
        
        self.assertEqual(diagnosis["diagnosis"], "chat")
        self.assertEqual(diagnosis["cause"], "server")
        self.assertGreater(diagnosis["confidence"], 0.7)
    
    def test_content_permission_issue(self):
        """Test diagnosis for content access denied."""
        symptoms_data = {
            "symptoms": [
                {"type": "content", "description": "access_denied_to_content"}
            ]
        }
        
        diagnosis = self.expert_system.diagnose(symptoms_data)
        
        self.assertEqual(diagnosis["diagnosis"], "content")
        self.assertEqual(diagnosis["cause"], "user")
        self.assertGreater(diagnosis["confidence"], 0.7)
    
    def test_unknown_issue(self):
        """Test diagnosis for an unknown issue."""
        symptoms_data = {
            "symptoms": [
                {"type": "other", "description": "unknown_problem"}
            ]
        }
        
        diagnosis = self.expert_system.diagnose(symptoms_data)
        
        self.assertEqual(diagnosis["cause"], "unknown")
        self.assertLess(diagnosis["confidence"], 0.5)
    
    def test_get_available_symptoms(self):
        """Test getting available symptoms."""
        symptoms = self.expert_system.get_available_symptoms()
        
        self.assertIn("login", symptoms)
        self.assertIn("video", symptoms)
        self.assertIn("chat", symptoms)
        self.assertIn("content", symptoms)
        
        self.assertGreater(len(symptoms["login"]), 0)
        self.assertGreater(len(symptoms["video"]), 0)
        self.assertGreater(len(symptoms["chat"]), 0)
        self.assertGreater(len(symptoms["content"]), 0)

if __name__ == '__main__':
    unittest.main()
