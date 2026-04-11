
# Max Cognitive Shield - Deployment Instructions

## Package Information
- **Skill**: skill-max-cognitive-shield
- **Version**: 1.0.0
- **Package**: skill-max-cognitive-shield-v1.0.0.claw
- **Size**: 0.03 MB

## Installation Methods

### Method 1: Using OpenClaw CLI (Recommended)
```bash
# Install the skill
openclaw skill install skill-max-cognitive-shield-v1.0.0.claw

# Verify installation
openclaw skill list | grep cognitive-shield

# Check status
openclaw skill status skill-max-cognitive-shield
```

### Method 2: Manual Docker Deployment
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
