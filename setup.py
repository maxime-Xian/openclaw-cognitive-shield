
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
