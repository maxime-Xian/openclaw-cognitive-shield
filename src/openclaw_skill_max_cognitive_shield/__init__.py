
"""
Max Cognitive Shield - OpenClaw Skill
AI cognitive protection and mood support skill for emotional-support scenarios.
"""

__version__ = "1.0.0"
__author__ = "OpenClaw Community"
__license__ = "Apache-2.0"

from .skill import CognitiveShieldSkill
from .deploy import deploy_skill
from .cli import main

__all__ = ["CognitiveShieldSkill", "deploy_skill", "main"]
