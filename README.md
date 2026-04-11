# Max Cognitive Shield - Comprehensive Documentation

## Project Overview

**max-cognitive-shield** is an open-source OpenClaw skill for emotional-support scenarios. Fully anonymized and GDPR/CCPA compliant, it can be deployed in one command to give your agent cognitive-protection and mood-soothing capabilities—ideal for community, education, and corporate mental-health assistants.

### 中文介绍

**max-cognitive-shield** 是一款面向情绪支持场景的开源 OpenClaw 技能，已完全脱敏并符合国际隐私法规。一键部署即可为您的智能体添加认知防护与情绪安抚能力，适用于社区、教育及企业心理健康助手。

## Quick Start

### Prerequisites

- Docker 20.10 or higher
- 512MB RAM available
- 1GB disk space

### One-Click Deployment

```bash
# Method 1: Using deployment script
./deploy.sh

# Method 2: Using pip package
pip install openclaw-skill-max-cognitive-shield
openclaw-skill-deploy

# Method 3: Manual Docker deployment
docker run -d \
  --name cognitive-shield \
  -p 8080:8080 \
  -p 50051:50051 \
  skill-max-cognitive-shield:1.0.0
```

### Verification

```bash
# Check health
curl http://localhost:8080/health

# Check status
curl http://localhost:8080/status

# Test analysis
curl -X POST http://localhost:8080/analyze \
  -H "Content-Type: application/json" \
  -d '{"text": "I need to finish this tonight no matter what", "session_id": "test-session"}'
```

## API Documentation

### REST API Endpoints

#### Health Check
```http
GET /health
```
**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2026-04-11T18:00:00Z",
  "service": "skill-max-cognitive-shield"
}
```

#### Get Status
```http
GET /status
```
**Response:**
```json
{
  "skill_status": "healthy",
  "active_sessions": 2,
  "metrics": {
    "cpu_usage": 0.3,
    "memory_usage": 0.4,
    "total_requests": 150,
    "average_response_time": 0.05
  }
}
```

#### Analyze Input
```http
POST /analyze
Content-Type: application/json

{
  "text": "I'm so tired but I have to keep working",
  "session_id": "user-session-123",
  "user_id": "anonymous-user",
  "session_duration": 45
}
```
**Response:**
```json
{
  "cognitive_state": {
    "cognitive_load": 0.7,
    "stress_indicator": 0.8,
    "focus_level": 0.3,
    "active_biases": ["过度自耗"]
  },
  "detected_patterns": [
    {
      "pattern_id": "OS-001",
      "pattern_name": "意志力崇拜 (过度自耗)",
      "description": "Detected trigger: 硬扛",
      "severity": 3
    }
  ],
  "recommended_intervention": 3,
  "confidence_score": 0.85
}
```

#### Request Intervention
```http
POST /intervention
Content-Type: application/json

{
  "session_id": "user-session-123",
  "level": 3,
  "reason": "Detected high cognitive stress patterns"
}
```
**Response:**
```json
{
  "intervention_applied": true,
  "intervention_message": "I need to intervene here. This approach may be harmful to your wellbeing.",
  "suggested_actions": [
    "Stop working immediately",
    "Take a 30-minute rest",
    "Consider ending the session",
    "Contact support if needed"
  ]
}
```

### gRPC API

For high-performance applications, use the gRPC interface:

```protobuf
service CognitiveShieldSkill {
  rpc Initialize(InitializeRequest) returns (InitializeResponse);
  rpc AnalyzeInput(AnalyzeInputRequest) returns (AnalyzeInputResponse);
  rpc RequestIntervention(InterventionRequest) returns (InterventionResponse);
  rpc GetStatus(StatusRequest) returns (StatusResponse);
  rpc Run(RunRequest) returns (stream RunResponse);
}
```

## Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `LOG_LEVEL` | `INFO` | Logging level (DEBUG, INFO, WARNING, ERROR) |
| `MAX_INTERVENTIONS_PER_SESSION` | `3` | Maximum interventions per session |
| `SESSION_TIMEOUT_MINUTES` | `60` | Session timeout in minutes |
| `SKILL_SECRET_KEY` | None | Encryption key for sensitive data |

### Intervention Patterns

Customize cognitive risk patterns in `config/intervention_patterns.json`:

```json
{
  "patterns": [
    {
      "id": "OS-001",
      "name": "意志力崇拜 (过度自耗)",
      "triggers": ["硬扛", "再撑一会", "今晚必须干完"],
      "level": "L3"
    }
  ]
}
```

## Security & Privacy

### Data Protection

- **No Personal Data Storage**: All processing is ephemeral
- **SHA-256 Hashing**: User IDs are hashed before processing
- **AES-256 Encryption**: Sensitive data encrypted at rest
- **TLS 1.3**: All communications encrypted in transit
- **30-Day Retention**: Audit logs automatically rotated

### Compliance

- ✅ **GDPR Compliant**: Data minimization, right to deletion
- ✅ **CCPA Compliant**: Consumer rights, no data selling
- ✅ **HIPAA Considered**: No medical data processed
- ✅ **SOC 2 Ready**: Security controls implemented

### Security Features

- Non-root container execution (UID 10000)
- Read-only filesystem
- Network policy restrictions
- Seccomp and AppArmor profiles
- Regular vulnerability scanning
- Comprehensive audit logging

## Deployment Options

### Docker Compose

```yaml
version: '3.8'
services:
  cognitive-shield:
    image: skill-max-cognitive-shield:1.0.0
    ports:
      - "8080:8080"
      - "50051:50051"
    environment:
      - LOG_LEVEL=INFO
      - MAX_INTERVENTIONS_PER_SESSION=3
    restart: unless-stopped
```

### Kubernetes

```bash
# Apply Kubernetes manifests
kubectl apply -f manifest.yaml

# Check deployment
kubectl get pods -l app=skill-max-cognitive-shield

# View logs
kubectl logs -l app=skill-max-cognitive-shield
```

### Helm Chart

```bash
helm install cognitive-shield ./charts/cognitive-shield \
  --set image.tag=1.0.0 \
  --set resources.limits.memory=512Mi
```

## Monitoring & Observability

### Metrics

The skill exposes the following metrics:

- `cognitive_shield_requests_total`: Total requests processed
- `cognitive_shield_interventions_total`: Total interventions applied
- `cognitive_shield_session_duration`: Session duration histogram
- `cognitive_shield_cpu_usage`: CPU usage percentage
- `cognitive_shield_memory_usage`: Memory usage percentage

### Logging

Structured JSON logging with privacy audit trail:

```json
{
  "timestamp": "2026-04-11T18:00:00Z",
  "skill_id": "skill-max-cognitive-shield",
  "event": "analyze_input",
  "data_category": "user_text",
  "hash_user_id": "a1b2c3d4...",
  "result": "processed"
}
```

### Health Checks

- **Liveness**: `/health` endpoint responds within 10s
- **Readiness**: All dependencies available
- **Startup**: Service ready within 30s

## Testing

### Unit Tests

```bash
# Run unit tests
python -m pytest test/unit/ -v

# Run with coverage
python -m pytest test/unit/ --cov=src --cov-report=html
```

### Integration Tests

```bash
# Run integration tests
./test/integration_test.sh

# Run in local Kubernetes (Kind)
./test/kind-integration-test.sh
```

### Performance Tests

```bash
# Load testing with locust
locust -f test/load_test.py --headless -u 100 -r 10
```

## Contributing

### Development Setup

```bash
# Clone repository
git clone https://github.com/[REDACTED_ORG]/max-cognitive-shield.git
cd max-cognitive-shield

# Install dependencies
pip install -e .[dev]

# Run tests
make test

# Build Docker image
docker build -f Dockerfile.multi -t skill-max-cognitive-shield:dev .
```

### Code Style

- Python: Black, Flake8, MyPy
- Commit messages: Conventional Commits
- Documentation: Markdown with clear structure

### Pull Request Process

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

```
Copyright 2026 OpenClaw Community

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
```

## Support

### Documentation
- [API Reference](docs/api-reference.md)
- [Deployment Guide](docs/deployment-guide.md)
- [Security Guide](docs/security-guide.md)
- [Privacy Policy](docs/privacy-policy.md)

### Community
- [GitHub Issues](https://github.com/[REDACTED_ORG]/max-cognitive-shield/issues)
- [Discussions](https://github.com/[REDACTED_ORG]/max-cognitive-shield/discussions)
- [OpenClaw Community](https://community.openclaw.ai)

### Professional Support
- Enterprise deployment assistance
- Custom pattern development
- Compliance consulting
- Training and workshops

## Changelog

### v1.0.0 (2026-04-11)

**Initial Release**

- ✅ Complete desensitization of all sensitive data
- ✅ OpenClaw v2.x platform compatibility
- ✅ gRPC and REST API endpoints
- ✅ Cognitive pattern detection engine
- ✅ Three-level intervention system (L1/L2/L3)
- ✅ Privacy-compliant audit logging
- ✅ Security hardening (non-root, encryption, network policies)
- ✅ Comprehensive documentation
- ✅ Automated deployment scripts
- ✅ GDPR and CCPA compliance

### Upcoming Features

- [ ] Multi-language pattern support
- [ ] Advanced machine learning models
- [ ] Real-time collaboration features
- [ ] Mobile application integration
- [ ] Advanced analytics dashboard

---

**max-cognitive-shield**: Protecting cognitive wellbeing through intelligent intervention.

*Open-source, privacy-first, community-driven.*
