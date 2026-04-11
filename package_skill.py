#!/usr/bin/env python3

"""
OpenClaw Skill Packaging Script
Creates .claw package for skill distribution
"""

import os
import json
import tarfile
import hashlib
import datetime
from pathlib import Path
import shutil

class SkillPackager:
    def __init__(self, skill_dir: str = "."):
        self.skill_dir = Path(skill_dir)
        self.package_name = "skill-max-cognitive-shield"
        self.version = "1.0.0"
        self.package_file = f"{self.package_name}-v{self.version}.claw"

    def load_skill_manifest(self):
        """Load and validate skill.json manifest"""
        manifest_path = self.skill_dir / "skill.json"

        if not manifest_path.exists():
            raise FileNotFoundError(f"skill.json not found at {manifest_path}")

        with open(manifest_path, 'r') as f:
            manifest = json.load(f)

        # Update version in manifest
        manifest['version'] = self.version

        # Validate required fields
        required_fields = ['id', 'name', 'version', 'description', 'runtime']
        for field in required_fields:
            if field not in manifest:
                raise ValueError(f"Required field '{field}' missing from skill.json")

        return manifest

    def calculate_file_hash(self, file_path: Path) -> str:
        """Calculate SHA-256 hash of a file"""
        hasher = hashlib.sha256()
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hasher.update(chunk)
        return hasher.hexdigest()

    def create_manifest(self, included_files: list) -> dict:
        """Create package manifest with file hashes"""
        manifest = {
            "package_format_version": "2.0",
            "skill_id": "skill-max-cognitive-shield",
            "version": self.version,
            "created_at": datetime.datetime.utcnow().isoformat() + "Z",
            "files": {},
            "checksums": {},
            "metadata": {
                "description": "AI cognitive protection and mood support skill",
                "license": "Apache-2.0",
                "size_bytes": 0,
                "file_count": len(included_files)
            }
        }

        total_size = 0

        for file_path in included_files:
            if os.path.exists(file_path):
                file_stat = os.stat(file_path)
                file_size = file_stat.st_size
                file_hash = self.calculate_file_hash(Path(file_path))

                manifest["files"][file_path] = {
                    "size": file_size,
                    "modified": datetime.datetime.fromtimestamp(file_stat.st_mtime).isoformat(),
                    "path": file_path
                }

                manifest["checksums"][file_path] = file_hash
                total_size += file_size

        manifest["metadata"]["size_bytes"] = total_size

        return manifest

    def should_include_file(self, file_path: str, ignore_patterns: list) -> bool:
        """Check if file should be included in package"""
        file_path_lower = file_path.lower()

        # Skip ignored patterns
        for pattern in ignore_patterns:
            if pattern.lower() in file_path_lower:
                return False

        # Include only relevant files
        include_extensions = [
            '.py', '.json', '.yaml', '.yml', '.proto', '.md', '.txt',
            'Dockerfile', 'Dockerfile.multi', 'Makefile'
        ]

        # Include directories
        include_dirs = ['src', 'proto', 'config', 'resources', 'test']

        # Include root files
        include_root_files = [
            'skill.json', 'manifest.yaml', 'Dockerfile.multi',
            'requirements.txt', 'setup.py', 'README.md', 'LICENSE'
        ]

        # Check if file is in root and should be included
        if os.path.dirname(file_path) == '':
            return any(file_path == root_file for root_file in include_root_files)

        # Check if file is in included directories
        if any(f"/{dir}/" in file_path or file_path.startswith(f"{dir}/") for dir in include_dirs):
            return True

        # Check file extension
        return any(file_path.endswith(ext) for ext in include_extensions)

    def load_clawignore(self) -> list:
        """Load .clawignore patterns"""
        ignore_file = self.skill_dir / ".clawignore"
        patterns = []

        if ignore_file.exists():
            with open(ignore_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        patterns.append(line)

        # Add default patterns
        default_patterns = [
            '.git', '__pycache__', '*.pyc', '.pytest_cache',
            '.coverage', 'htmlcov', '.tox', '.venv', 'venv',
            '*.egg-info', 'build', 'dist', '*.whl',
            '*.log', '.gitignore', '*.bak', '*.tmp'
        ]

        patterns.extend(default_patterns)
        return list(set(patterns))  # Remove duplicates

    def collect_files(self) -> list:
        """Collect all files to include in package"""
        ignore_patterns = self.load_clawignore()
        included_files = []

        for root, dirs, files in os.walk(self.skill_dir):
            # Skip ignored directories
            dirs[:] = [d for d in dirs if not any(pattern.lower() in d.lower() for pattern in ignore_patterns)]

            for file in files:
                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path, self.skill_dir)

                if self.should_include_file(relative_path, ignore_patterns):
                    included_files.append(relative_path)

        return sorted(included_files)

    def create_package(self) -> str:
        """Create the .claw package"""
        print(f"Creating OpenClaw skill package: {self.package_file}")

        # Load skill manifest
        skill_manifest = self.load_skill_manifest()
        print(f"Loaded skill manifest: {skill_manifest['name']} v{skill_manifest['version']}")

        # Collect files to include
        included_files = self.collect_files()
        print(f"Found {len(included_files)} files to package")

        # Create package manifest
        package_manifest = self.create_manifest(included_files)

        # Create temporary directory for packaging
        temp_dir = self.skill_dir / ".package_temp"
        temp_dir.mkdir(exist_ok=True)

        try:
            # Write package manifest
            manifest_path = temp_dir / "package.json"
            with open(manifest_path, 'w') as f:
                json.dump(package_manifest, f, indent=2)

            # Create tar.gz archive
            with tarfile.open(self.package_file, 'w:gz') as tar:
                # Add package manifest
                tar.add(manifest_path, arcname="package.json")

                # Add all included files
                for file_path in included_files:
                    if os.path.exists(file_path):
                        tar.add(file_path)

            # Calculate package checksum
            package_hash = self.calculate_file_hash(Path(self.package_file))

            # Create checksum file
            checksum_file = f"{self.package_file}.sha256"
            with open(checksum_file, 'w') as f:
                f.write(f"{package_hash}  {self.package_file}\n")

            # Create signature file (placeholder for production)
            signature_file = f"{self.package_file}.sig"
            with open(signature_file, 'w') as f:
                f.write(f"# OpenClaw Skill Package Signature\n")
                f.write(f"# Package: {self.package_file}\n")
                f.write(f"# Hash: {package_hash}\n")
                f.write(f"# Timestamp: {datetime.datetime.utcnow().isoformat()}Z\n")
                f.write(f"# This is a development signature. Production packages will be signed with OpenClaw keys.\n")

            print(f"Package created successfully: {self.package_file}")
            print(f"Package size: {os.path.getsize(self.package_file) / 1024 / 1024:.2f} MB")
            print(f"Package hash: {package_hash}")

            return self.package_file

        finally:
            # Clean up temporary directory
            if temp_dir.exists():
                shutil.rmtree(temp_dir)

    def validate_package(self, package_file: str) -> bool:
        """Validate the created package"""
        print(f"\nValidating package: {package_file}")

        if not os.path.exists(package_file):
            print("❌ Package file not found")
            return False

        # Check package size
        size_mb = os.path.getsize(package_file) / 1024 / 1024
        if size_mb > 50:
            print(f"❌ Package too large: {size_mb:.2f} MB (limit: 50 MB)")
            return False
        print(f"✅ Package size: {size_mb:.2f} MB")

        # Verify checksum
        checksum_file = f"{package_file}.sha256"
        if not os.path.exists(checksum_file):
            print("❌ Checksum file not found")
            return False

        with open(checksum_file, 'r') as f:
            expected_hash = f.read().split()[0]

        actual_hash = self.calculate_file_hash(Path(package_file))
        if expected_hash != actual_hash:
            print(f"❌ Checksum mismatch: expected {expected_hash}, got {actual_hash}")
            return False
        print(f"✅ Checksum verified: {actual_hash}")

        # Verify package contents
        try:
            with tarfile.open(package_file, 'r:gz') as tar:
                members = tar.getnames()

                # Check for required files
                required_files = ['package.json', 'skill.json']
                for required_file in required_files:
                    if required_file not in members:
                        print(f"❌ Required file missing: {required_file}")
                        return False

                print(f"✅ Package contains {len(members)} files")

                # Extract and validate package manifest
                manifest_data = tar.extractfile('package.json').read()
                manifest = json.loads(manifest_data)

                if manifest.get('skill_id') != 'skill-max-cognitive-shield':
                    print("❌ Invalid skill ID in package manifest")
                    return False

                print(f"✅ Package manifest valid: {manifest['skill_id']} v{manifest['version']}")

        except Exception as e:
            print(f"❌ Failed to read package: {e}")
            return False

        print("✅ Package validation successful")
        return True

    def generate_deployment_instructions(self):
        """Generate deployment instructions"""
        instructions = f"""
# Max Cognitive Shield - Deployment Instructions

## Package Information
- **Skill**: {self.package_name}
- **Version**: {self.version}
- **Package**: {self.package_file}
- **Size**: {os.path.getsize(self.package_file) / 1024 / 1024:.2f} MB

## Installation Methods

### Method 1: Using OpenClaw CLI (Recommended)
```bash
# Install the skill
openclaw skill install {self.package_file}

# Verify installation
openclaw skill list | grep cognitive-shield

# Check status
openclaw skill status skill-max-cognitive-shield
```

### Method 2: Manual Docker Deployment
```bash
# Load and run the skill
docker load < {self.package_file}
docker run -d \\
  --name cognitive-shield \\
  -p 8080:8080 \\
  -p 50051:50051 \\
  skill-max-cognitive-shield:{self.version}

# Verify deployment
curl http://localhost:8080/health
```

### Method 3: Kubernetes Deployment
```bash
# Apply Kubernetes manifests
kubectl apply -f manifest.yaml

# Check deployment status
kubectl get pods -l app=skill-max-cognitive-shield

# View logs
kubectl logs -l app=skill-max-cognitive-shield
```

## Verification

### Health Check
```bash
curl http://localhost:8080/health
# Expected: {{"status": "healthy", "service": "skill-max-cognitive-shield"}}
```

### Status Check
```bash
curl http://localhost:8080/status
# Expected: {{"skill_status": "healthy", "active_sessions": 0, ...}}
```

### Test Analysis
```bash
curl -X POST http://localhost:8080/analyze \\
  -H "Content-Type: application/json" \\
  -d '{{ "text": "test input", "session_id": "test-123" }}'
```

## Monitoring

### Logs
```bash
# Docker logs
docker logs cognitive-shield

# Kubernetes logs
kubectl logs -l app=skill-max-cognitive-shield
```

### Metrics
The skill exposes the following metrics:
- CPU usage: < 60%
- Memory usage: < 384MB
- Response time: < 200ms (P99)
- Request rate: > 100 RPS

## Troubleshooting

### Common Issues

1. **Port conflicts**: Change ports using environment variables
   ```bash
   docker run -e HTTP_PORT=8081 -e GRPC_PORT=50052 ...
   ```

2. **Permission denied**: Ensure Docker socket access
   ```bash
   sudo usermod -aG docker $USER
   ```

3. **Memory limits**: Increase if needed
   ```bash
   docker run --memory=1g ...
   ```

## Support

- Documentation: https://docs.openclaw.ai/skills/max-cognitive-shield
- Issues: https://github.com/[REDACTED_ORG]/max-cognitive-shield/issues
- Community: https://community.openclaw.ai

## License

Apache License 2.0 - See LICENSE file for details.
"""

        with open("DEPLOYMENT_GUIDE.md", 'w') as f:
            f.write(instructions)

        print("✅ Deployment guide generated: DEPLOYMENT_GUIDE.md")

def main():
    """Main packaging function"""
    print("OpenClaw Skill Packaging Tool")
    print("=" * 40)

    try:
        # Create packager
        packager = SkillPackager()

        # Create package
        package_file = packager.create_package()

        # Validate package
        if packager.validate_package(package_file):
            # Generate deployment instructions
            packager.generate_deployment_instructions()

            print(f"\n🎉 Package created successfully!")
            print(f"📦 Package: {package_file}")
            print(f"🔒 Checksum: {package_file}.sha256")
            print(f"📝 Guide: DEPLOYMENT_GUIDE.md")
            print(f"\nReady for OpenClaw skill registry submission!")

            return True
        else:
            print(f"\n❌ Package validation failed")
            return False

    except Exception as e:
        print(f"\n❌ Packaging failed: {e}")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)