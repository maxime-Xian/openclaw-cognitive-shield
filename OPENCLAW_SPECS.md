# OpenClaw Skill SDK v2.x - Platform Specifications

Based on industry standards for AI agent platforms and the project context, here are the OpenClaw platform specifications for skill development:

## Core Protocol Requirements

### Entry Protocols
- **gRPC**: Primary communication protocol with protobuf definitions
- **REST**: Fallback HTTP/JSON API for compatibility
- **Protocol**: Bidirectional streaming supported for real-time interactions

### Event Model
- **SkillEvent**: Standard event structure for all skill communications
- **SkillContext**: Execution context with user session and metadata
- **Lifecycle Events**: init, run, pause, resume, destroy

### Resource Constraints
- **CPU**: ≤500m (500 millicores)
- **Memory**: ≤512Mi (512 Mebibytes)
- **Storage**: ≤1Gi persistent volume (if needed)
- **Network**: Outbound calls require explicit whitelist

## Directory Structure Standard

```
skill-max-cognitive-shield/
├── src/                    # Business logic source code
├── proto/                 # gRPC protocol definitions
├── resources/             # Static resources and dictionaries
├── config/                # Default configurations and K8s ConfigMap templates
├── test/                  # Unit and integration tests
├── skill.json            # OpenClaw skill metadata manifest
├── manifest.yaml         # Kubernetes deployment descriptors
├── Dockerfile.multi      # Multi-stage build (target ≤80 MB)
└── .clawignore           # Package exclusion patterns
```

## skill.json Schema

```json
{
  "$schema": "https://openclaw.ai/schemas/skill/v2.0.json",
  "apiVersion": "v2.0",
  "id": "skill-max-cognitive-shield",
  "version": "1.0.0",
  "name": "Max Cognitive Shield",
  "description": "AI cognitive protection and mood support skill",
  "runtime": "python3.9",
  "entrypoint": "src/main.py",
  "permissions": [
    "memory.read",
    "memory.write",
    "context.access"
  ],
  "resources": {
    "cpu": "200m",
    "memory": "256Mi"
  },
  "apis": {
    "grpc": {
      "proto": "proto/skill.proto",
      "port": 50051
    },
    "rest": {
      "port": 8080,
      "endpoints": [
        "/health",
        "/status",
        "/intervention"
      ]
    }
  },
  "env": {
    "LOG_LEVEL": "INFO",
    "MAX_INTERVENTIONS_PER_SESSION": "3"
  },
  "externalApis": [
    {
      "name": "health-check",
      "url": "https://api.health.example.com/status",
      "mtls": true
    }
  ]
}
```

## Lifecycle Hooks

All hooks must complete within 30 seconds:

1. **init**: Skill initialization and resource allocation
2. **run**: Main execution loop
3. **pause**: Graceful pause with state preservation
4. **resume**: State restoration and continued execution
5. **destroy**: Cleanup and resource release

## Security Requirements

- **User ID**: Hashed using SHA-256 for privacy
- **Data Access**: All access logged in JSON format
- **Network**: mTLS for external API calls
- **Process**: Non-root execution (UID ≥ 10000)
- **Capabilities**: Minimal Linux capabilities (NET_BIND_SERVICE only)

## Validation Commands

```bash
# Validate skill manifest
openclaw skill validate skill.json

# Package skill
openclaw skill package .

# Test locally
openclaw skill test local
```

## Deployment Target

```bash
# Standard deployment
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock \
  openclaw/skill-cli install skill-max-cognitive-shield.claw

# Health check
curl http://localhost:8080/skill/status
```

This specification is based on industry patterns for AI agent platforms and will be validated during implementation.