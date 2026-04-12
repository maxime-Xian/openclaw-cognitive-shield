
# OpenClaw Deployment Guide for Max Cognitive Shield

## Overview
This guide provides step-by-step instructions for deploying Max Cognitive Shield as an OpenClaw skill, leveraging OpenClaw's native features for optimal integration.

## Prerequisites
- OpenClaw CLI installed and configured
- Python 3.9+ environment
- Basic understanding of OpenClaw skill architecture

## Installation Methods

### Method 1: OpenClaw Native Installation (Recommended)
```bash
# Install the guardian safety engine from ClawHub
clawhub install guardian-safety-engine

# Clone the repository
git clone https://github.com/maxime-Xian/max-cognitive-shield.git
cd max-cognitive-shield

# Initialize the meta-cognitive OS
./scripts/setup.sh

# Deploy as OpenClaw skill
openclaw-skill-deploy
```

### Method 2: Manual Integration
```bash
# 1. Copy core protocols to OpenClaw workspace
cp -r core/SOUL.md $OPENCLAW_WORKSPACE/
cp -r core/AGENTS.md $OPENCLAW_WORKSPACE/
cp -r core/IDENTITY.md $OPENCLAW_WORKSPACE/
cp -r core/HEARTBEAT.md $OPENCLAW_WORKSPACE/

# 2. Integrate knowledge layer
cp -r knowledge/ $OPENCLAW_WORKSPACE/

# 3. Set up memory structure (OpenClaw native)
mkdir -p $OPENCLAW_WORKSPACE/memory/daily
mkdir -p $OPENCLAW_WORKSPACE/memory/reflections
mkdir -p $OPENCLAW_WORKSPACE/memory/evolution
mkdir -p $OPENCLAW_WORKSPACE/memory/pending

# 4. Configure OpenClaw hooks
claw config set hooks.pre_process "python scripts/error-capture.py"
claw config set hooks.heartbeat "node scripts/sleep-guardian.js"
```

### Method 3: Using Pre-built Package
```bash
# Install the skill
openclaw skill install skill-max-cognitive-shield-v1.0.0.claw

# Verify installation
openclaw skill list | grep cognitive-shield

# Check status
openclaw skill status skill-max-cognitive-shield
```

### Method 4: Docker Deployment
```bash
# Load and run the skill
docker load < skill-max-cognitive-shield-v1.0.0.claw
docker run -d \
  --name cognitive-shield \
  -p 8080:8080 \
  -p 50051:50051 \
  skill-max-cognitive-shield:1.0.0

# Verify deployment
curl http://localhost:8080/health
```

### Method 5: Kubernetes Deployment
```bash
# Apply Kubernetes manifests
kubectl apply -f manifest.yaml

# Check deployment status
kubectl get pods -l app=skill-max-cognitive-shield

# View logs
kubectl logs -l app=skill-max-cognitive-shield
```

## Configuration

### 1. Energy Awareness Setup
```bash
# Configure sleep monitoring
chmod +x scripts/sleep-guardian.js
# Add to crontab for automatic execution
echo "*/30 * * * * cd $(pwd) && node scripts/sleep-guardian.js" | crontab -
```

### 2. Memory Structure Initialization
```bash
# Create initial memory structure
mkdir -p memory/.status memory/.dreams

# Initialize energy status
echo '{"last_sleep_check": "$(date -Iseconds)", "energy_level": "NORMAL"}' > memory/.status/energy_status.json

# Set up daily logging structure
touch memory/daily/$(date +%Y-%m-%d).md
```

### 3. OpenClaw Skill Registration
```bash
# Register the skill with OpenClaw
claw skill register max-cognitive-shield \
  --entry-point skills/guardian-safety-engine \
  --memory-path memory/ \
  --config core/ \
  --heartbeat core/HEARTBEAT.md
```

## OpenClaw-Specific Features

### Memory Search Integration
The memory/daily/ structure is natively compatible with OpenClaw's memory_search feature:

```bash
# Search through daily reflections
claw memory search "energy levels" --type daily

# Query decision patterns
claw memory search "decision framework" --type evolution
```

### QMD (Queryable Markdown) Support
All core .md files are formatted for QMD compatibility:

```bash
# Query SOUL personality traits
claw qmd query SOUL.md "energy awareness protocols"

# Search intervention logic
claw qmd query AGENTS.md "three-tier intervention"
```

### Dreaming Integration
The .dreams/ directory integrates with OpenClaw's experimental Dreaming feature:

```bash
# Enable dreaming for pattern recognition
claw config set dreaming.enabled true
claw config set dreaming.cache_dir memory/.dreams/
```

## Heartbeat Configuration

### Automatic Pulse Tasks
Configure OpenClaw to execute heartbeat tasks:

```bash
# Sleep guardian check (23:45 daily)
claw heartbeat add "sleep-guardian" \
  --schedule "45 23 * * *" \
  --command "python scripts/sleep-guardian.py --check"

# Nightly summary (22:00 daily)
claw heartbeat add "nightly-summary" \
  --schedule "0 22 * * *" \
  --command "python scripts/nightly-summary.py"

# Error capture (every 5 minutes)
claw heartbeat add "error-capture" \
  --schedule "*/5 * * * *" \
  --command "python scripts/error-capture.py"
```

## Skill Dependencies

### Required OpenClaw Skills
- guardian-safety-engine (core protection)
- sleep-guardian (energy monitoring)

### Optional Skills
- meta-cognition-assistant (enhanced decision support)
- cognitive-bias-detector (bias identification)

## Monitoring and Maintenance

### Health Checks
```bash
# Check skill status
claw skill status max-cognitive-shield

# View memory usage
claw memory stats

# Monitor heartbeat execution
claw heartbeat logs --last 24h
```

### Performance Tuning
```bash
# Adjust memory cache size
claw config set memory.cache_size 500MB

# Configure response timeouts
claw config set skills.max-cognitive-shield.timeout 30s

# Enable verbose logging for debugging
claw config set logging.level DEBUG
```

## Verification

### Health Check
```bash
curl http://localhost:8080/health
# Expected: {"status": "healthy", "service": "skill-max-cognitive-shield"}
```

### Status Check
```bash
curl http://localhost:8080/status
# Expected: {"skill_status": "healthy", "active_sessions": 0, ...}
```

### Test Analysis
```bash
curl -X POST http://localhost:8080/analyze \
  -H "Content-Type: application/json" \
  -d '{ "text": "test input", "session_id": "test-123" }'
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

1. **Memory Search Not Working**
   ```bash
   # Ensure daily logs are properly formatted
   claw memory validate daily/
   # Rebuild memory index
   claw memory rebuild
   ```

2. **Heartbeat Tasks Not Executing**
   ```bash
   # Check cron service
   systemctl status cron
   # Verify heartbeat registration
   claw heartbeat list
   ```

3. **Energy Awareness Not Responding**
   ```bash
   # Check sleep guardian logs
   tail -f logs/sleep-guardian.log
   # Verify system uptime access
   node scripts/sleep-guardian.js --test
   ```

### Debug Mode
```bash
# Enable debug mode
claw config set debug.enabled true

# View real-time skill execution
claw skill debug max-cognitive-shield
```

## Security Considerations

### Memory Protection
- The pending/ directory is write-protected by default
- Critical interventions require explicit user confirmation
- All memory operations are logged for audit trails

### Access Control
```bash
# Restrict memory access
claw config set security.memory_read_only true

# Enable intervention approval
claw config set security.require_approval true
```

## Upgrading

### Version Management
```bash
# Check current version
claw skill version max-cognitive-shield

# Update to latest version
claw skill update max-cognitive-shield

# Rollback if needed
claw skill rollback max-cognitive-shield v1.2.0
```

### Migration Guide
When upgrading between major versions:
1. Backup memory/ directory
2. Review breaking changes in CHANGELOG.md
3. Test in staging environment
4. Migrate configuration files
5. Validate heartbeat tasks

## Support

For issues specific to OpenClaw integration:
- OpenClaw Documentation: https://docs.openclaw.ai
- Discord Community: https://discord.gg/openclaw
- Issue Tracker: https://github.com/maxime-Xian/max-cognitive-shield/issues

## Next Steps

1. Complete the basic installation using Method 1
2. Configure your energy awareness preferences in USER.md
3. Set up heartbeat tasks for your schedule
4. Test the dual-channel filter with sample scenarios
5. Monitor the first nightly summary generation

This deployment guide ensures seamless integration with OpenClaw while maintaining all the powerful cognitive protection features of Max Cognitive Shield.
