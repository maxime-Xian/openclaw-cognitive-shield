#!/usr/bin/env python3

import os
import json
from pathlib import Path

def create_setup_py():
    """Create setup.py for pip installation"""
    setup_content = '''
from setuptools import setup, find_packages
import os
import json

# Read version from skill.json
with open('skill.json', 'r') as f:
    skill_config = json.load(f)
    version = skill_config.get('version', '1.0.0')

# Read README
with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="openclaw-skill-max-cognitive-shield",
    version=version,
    description="Max Cognitive Shield - AI cognitive protection and mood support skill",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="OpenClaw Community",
    author_email="community@openclaw.ai",
    url="https://github.com/[REDACTED_ORG]/max-cognitive-shield",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    install_requires=[
        "grpcio>=1.50.0",
        "grpcio-tools>=1.50.0",
        "flask>=2.0.0",
        "protobuf>=4.0.0",
        "requests>=2.25.0",
        "cryptography>=3.4.0",
        "pyyaml>=6.0",
        "python-json-logger>=2.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=22.0.0",
            "flake8>=5.0.0",
            "mypy>=0.990",
        ],
        "test": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "pytest-mock>=3.0.0",
        ]
    },
    entry_points={
        "console_scripts": [
            "openclaw-skill-deploy=openclaw_skill_max_cognitive_shield.deploy:main",
            "max-cognitive-shield=openclaw_skill_max_cognitive_shield.cli:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Software Development :: Libraries",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    python_requires=">=3.9",
    keywords="openclaw skill cognitive ai mental-health",
    project_urls={
        "Bug Reports": "https://github.com/[REDACTED_ORG]/max-cognitive-shield/issues",
        "Source": "https://github.com/[REDACTED_ORG]/max-cognitive-shield",
        "Documentation": "https://docs.openclaw.ai/skills/max-cognitive-shield",
    },
)
'''

    with open('setup.py', 'w') as f:
        f.write(setup_content)

    print("Created setup.py")

def create_package_structure():
    """Create Python package structure"""
    # Create package directory
    package_dir = Path('src/openclaw_skill_max_cognitive_shield')
    package_dir.mkdir(parents=True, exist_ok=True)

    # Create __init__.py
    init_content = '''
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
'''

    with open(package_dir / '__init__.py', 'w') as f:
        f.write(init_content)

    print("Created package __init__.py")

def create_requirements():
    """Create requirements.txt"""
    requirements = '''
grpcio>=1.50.0
grpcio-tools>=1.50.0
flask>=2.0.0
protobuf>=4.0.0
requests>=2.25.0
cryptography>=3.4.0
pyyaml>=6.0
python-json-logger>=2.0.0
'''

    with open('requirements.txt', 'w') as f:
        f.write(requirements)

    print("Created requirements.txt")

def main():
    """Main setup function"""
    print("Setting up Python package for Max Cognitive Shield...")

    # Create all files
    create_setup_py()
    create_package_structure()
    create_requirements()

    print("\nPackage setup completed!")
    print("\nTo install the package:")
    print("  pip install -e .")
    print("\nTo deploy the skill:")
    print("  python -m openclaw_skill_max_cognitive_shield deploy")
    print("  or")
    print("  openclaw-skill-deploy")

if __name__ == "__main__":
    main()