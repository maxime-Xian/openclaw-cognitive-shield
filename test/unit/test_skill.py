import unittest
import json
import time
from unittest.mock import patch, MagicMock
import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from openclaw_skill_max_cognitive_shield.skill import CognitiveShieldSkill
from openclaw_skill_max_cognitive_shield.deploy import deploy_skill

class TestCognitiveShieldSkill(unittest.TestCase):
    """Unit tests for CognitiveShieldSkill"""

    def setUp(self):
        """Set up test fixtures"""
        self.skill = CognitiveShieldSkill()
        self.test_session_id = "test-session-123"
        self.test_user_id = "test-user-456"

    def test_initialization(self):
        """Test skill initialization"""
        result = self.skill.initialize(
            skill_id="test-skill",
            config={"test_mode": True}
        )

        self.assertTrue(result["success"])
        self.assertIn("session_id", result)
        self.assertIsInstance(result["session_id"], str)
        self.assertGreater(len(result["session_id"]), 0)

    def test_analyze_normal_input(self):
        """Test analysis of normal, non-concerning input"""
        # Initialize session first
        init_result = self.skill.initialize("test-skill", {})
        session_id = init_result["session_id"]

        result = self.skill.analyze_input(
            session_id=session_id,
            user_input="I'm working on a project and feeling good about it",
            user_context={"user_id": self.test_user_id}
        )

        self.assertIn("cognitive_state", result)
        self.assertIn("detected_patterns", result)
        self.assertIn("recommended_intervention", result)
        self.assertIn("confidence_score", result)

        # Normal input should have low intervention level
        self.assertEqual(result["recommended_intervention"], "NONE")
        self.assertEqual(len(result["detected_patterns"]), 0)

    def test_analyze_stressful_input_chinese(self):
        """Test analysis of stressful input in Chinese"""
        init_result = self.skill.initialize("test-skill", {})
        session_id = init_result["session_id"]

        result = self.skill.analyze_input(
            session_id=session_id,
            user_input="我今晚必须干完这个，不管多累都要硬扛",
            user_context={"user_id": self.test_user_id}
        )

        self.assertGreater(len(result["detected_patterns"]), 0)
        self.assertIn("LEVEL_3_CRITICAL", result["recommended_intervention"])

    def test_analyze_stressful_input_english(self):
        """Test analysis of stressful input in English"""
        init_result = self.skill.initialize("test-skill", {})
        session_id = init_result["session_id"]

        result = self.skill.analyze_input(
            session_id=session_id,
            user_input="I have to push through this pain and finish tonight no matter what",
            user_context={"user_id": self.test_user_id}
        )

        self.assertGreater(len(result["detected_patterns"]), 0)
        self.assertIn("LEVEL", result["recommended_intervention"])

    def test_self_critical_patterns(self):
        """Test detection of self-critical patterns"""
        init_result = self.skill.initialize("test-skill", {})
        session_id = init_result["session_id"]

        result = self.skill.analyze_input(
            session_id=session_id,
            user_input="我太废了，我怎么总是做不好这些事情",
            user_context={"user_id": self.test_user_id}
        )

        self.assertGreater(len(result["detected_patterns"]), 0)
        self.assertIn("LEVEL_2_INTERVENTION", result["recommended_intervention"])

    def test_intervention_limits(self):
        """Test intervention limits per session"""
        init_result = self.skill.initialize("test-skill", {})
        session_id = init_result["session_id"]

        # Apply maximum interventions
        for i in range(5):  # More than the default limit of 3
            result = self.skill.request_intervention(
                session_id=session_id,
                level="LEVEL_2_INTERVENTION",
                reason=f"Test intervention {i+1}"
            )

        # The last intervention should fail due to limit
        self.assertFalse(result["intervention_applied"])
        self.assertIn("Maximum interventions reached", result["intervention_message"])

    def test_intervention_levels(self):
        """Test different intervention levels"""
        init_result = self.skill.initialize("test-skill", {})
        session_id = init_result["session_id"]

        # Test LEVEL_1_MONITOR
        result1 = self.skill.request_intervention(
            session_id=session_id,
            level="LEVEL_1_MONITOR",
            reason="Test L1 intervention"
        )
        self.assertTrue(result1["intervention_applied"])
        self.assertIn("pause and reflect", result1["intervention_message"])

        # Test LEVEL_2_INTERVENTION
        result2 = self.skill.request_intervention(
            session_id=session_id,
            level="LEVEL_2_INTERVENTION",
            reason="Test L2 intervention"
        )
        self.assertTrue(result2["intervention_applied"])
        self.assertIn("step back", result2["intervention_message"])

        # Test LEVEL_3_CRITICAL
        result3 = self.skill.request_intervention(
            session_id=session_id,
            level="LEVEL_3_CRITICAL",
            reason="Test L3 intervention"
        )
        self.assertTrue(result3["intervention_applied"])
        self.assertIn("harmful to your wellbeing", result3["intervention_message"])

    def test_invalid_session_handling(self):
        """Test handling of invalid session IDs"""
        result = self.skill.request_intervention(
            session_id="invalid-session",
            level="LEVEL_1_MONITOR",
            reason="Test with invalid session"
        )

        self.assertFalse(result["intervention_applied"])
        self.assertEqual(result["intervention_message"], "Invalid session")

    def test_cognitive_state_calculation(self):
        """Test cognitive state calculation"""
        init_result = self.skill.initialize("test-skill", {})
        session_id = init_result["session_id"]

        # Test with concerning input
        result = self.skill.analyze_input(
            session_id=session_id,
            user_input="我必须硬扛过去",
            user_context={"user_id": self.test_user_id}
        )

        cognitive_state = result["cognitive_state"]
        self.assertGreater(cognitive_state["cognitive_load"], 0.3)
        self.assertGreater(cognitive_state["stress_indicator"], 0.5)
        self.assertLess(cognitive_state["focus_level"], 0.6)

    def test_confidence_scoring(self):
        """Test confidence score calculation"""
        init_result = self.skill.initialize("test-skill", {})
        session_id = init_result["session_id"]

        # Test with clear pattern
        result1 = self.skill.analyze_input(
            session_id=session_id,
            user_input="我今晚必须干完",
            user_context={"user_id": self.test_user_id}
        )
        self.assertGreater(result1["confidence_score"], 0.8)

        # Test with normal input
        result2 = self.skill.analyze_input(
            session_id=session_id,
            user_input="我正在正常工作",
            user_context={"user_id": self.test_user_id}
        )
        self.assertGreater(result2["confidence_score"], 0.9)

    def test_user_id_hashing(self):
        """Test that user IDs are properly hashed"""
        with self.assertLogs() as log_context:
            init_result = self.skill.initialize("test-skill", {})
            session_id = init_result["session_id"]

            self.skill.analyze_input(
                session_id=session_id,
                user_input="test input",
                user_context={"user_id": "test-user-123"}
            )

        # Check that logs contain hashed user ID, not original
        log_output = " ".join(log_context.output)
        self.assertNotIn("test-user-123", log_output)
        self.assertIn("hash_user_id", log_output)


class TestDeployment(unittest.TestCase):
    """Tests for deployment functionality"""

    @patch('subprocess.run')
    def test_docker_build_success(self, mock_run):
        """Test successful Docker build"""
        mock_run.return_value.returncode = 0

        result = deploy_skill()
        self.assertTrue(result)

    @patch('subprocess.run')
    def test_docker_build_failure(self, mock_run):
        """Test failed Docker build"""
        mock_run.return_value.returncode = 1
        mock_run.return_value.stderr = "Build failed"

        result = deploy_skill()
        self.assertFalse(result)

    @patch('subprocess.run')
    def test_container_start_failure(self, mock_run):
        """Test container start failure"""
        def side_effect(cmd, **kwargs):
            mock_result = MagicMock()
            if 'build' in cmd:
                mock_result.returncode = 0
            else:
                mock_result.returncode = 1
                mock_result.stderr = "Container failed"
            return mock_result

        mock_run.side_effect = side_effect

        result = deploy_skill()
        self.assertFalse(result)


class TestConfiguration(unittest.TestCase):
    """Tests for skill configuration"""

    def test_default_configuration(self):
        """Test default configuration values"""
        skill = CognitiveShieldSkill()

        self.assertEqual(skill.config["max_interventions_per_session"], 3)
        self.assertEqual(skill.config["session_timeout_minutes"], 60)
        self.assertEqual(skill.config["log_level"], "INFO")

    def test_custom_configuration(self):
        """Test custom configuration loading"""
        import tempfile
        import json

        # Create temporary config file
        config_data = {
            "max_interventions_per_session": 5,
            "session_timeout_minutes": 120,
            "log_level": "DEBUG"
        }

        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(config_data, f)
            config_path = f.name

        try:
            skill = CognitiveShieldSkill(config_path)
            self.assertEqual(skill.config["max_interventions_per_session"], 5)
            self.assertEqual(skill.config["session_timeout_minutes"], 120)
            self.assertEqual(skill.config["log_level"], "DEBUG")
        finally:
            os.unlink(config_path)


class TestPatternDetection(unittest.TestCase):
    """Tests for cognitive pattern detection"""

    def setUp(self):
        self.skill = CognitiveShieldSkill()

    def test_chinese_patterns(self):
        """Test detection of Chinese cognitive patterns"""
        test_cases = [
            ("硬扛", True),
            ("再撑一会", True),
            ("今晚必须干完", True),
            ("我太废了", True),
            ("好恨自己", True),
            ("正常的工作", False),
            ("今天天气不错", False)
        ]

        for text, should_detect in test_cases:
            with self.subTest(text=text):
                init_result = self.skill.initialize("test-skill", {})
                session_id = init_result["session_id"]

                result = self.skill.analyze_input(
                    session_id=session_id,
                    user_input=text,
                    user_context={"user_id": "test-user"}
                )

                detected = len(result["detected_patterns"]) > 0
                self.assertEqual(detected, should_detect,
                    f"Pattern detection failed for: '{text}'")

    def test_english_patterns(self):
        """Test detection of English cognitive patterns"""
        test_cases = [
            ("push through", True),
            ("just one more", True),
            ("have to finish tonight", True),
            ("hate myself", True),
            ("normal work", False),
            ("feeling good", False)
        ]

        for text, should_detect in test_cases:
            with self.subTest(text=text):
                init_result = self.skill.initialize("test-skill", {})
                session_id = init_result["session_id"]

                result = self.skill.analyze_input(
                    session_id=session_id,
                    user_input=text,
                    user_context={"user_id": "test-user"}
                )

                detected = len(result["detected_patterns"]) > 0
                self.assertEqual(detected, should_detect,
                    f"Pattern detection failed for: '{text}'")


if __name__ == '__main__':
    # Run tests with verbose output
    unittest.main(verbosity=2)