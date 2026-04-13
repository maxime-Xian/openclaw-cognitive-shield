# Guardian Safety Engine API Reference

## 📋 Overview

The Guardian Safety Engine is a cognitive protection system that provides intelligent safety interventions for AI assistants. It analyzes user input and context to detect potential risks, cognitive biases, and harmful patterns, then provides appropriate interventions.

**Key Capabilities:**
- 🛡️ Three-level safety intervention (L1/L2/L3)
- 🧠 Cognitive bias detection and prevention
- 📊 Risk assessment and pattern recognition
- 🎯 Personalized intervention strategies

---

## 🚀 Quick Start

### Basic Usage

```python
from guardian_safety_engine import GuardianSafetyEngine

# Initialize the engine
engine = GuardianSafetyEngine()

# Analyze user input for risks
result = engine.analyze_risk(
    user_input="I need to finish this refactor tonight!",
    context={"time": "02:30", "sleep_hours": 3}
)

print(f"Risk Score: {result['risk_score']}")
print(f"Intervention: {result['intervention_level']}")
```

---

## 🔧 Core API

### GuardianSafetyEngine Class

#### Constructor
```python
GuardianSafetyEngine(config: Optional[Dict] = None)
```

**Parameters:**
- `config` (Dict, optional): Custom configuration

#### analyze_risk Method
```python
analyze_risk(user_input: str, context: Dict) -> Dict
```

**Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `user_input` | str | Yes | User's current input |
| `context` | Dict | Yes | Conversation context |

**Context Schema:**
```typescript
interface Context {
  time: string;              // HH:MM format
  sleep_hours?: number;      // 0-24
  stress_level?: number;     // 0-10
  conversation_history?: Array<{role: string; content: string}>;
  user_profile?: {
    cognitive_style?: "analytical" | "intuitive" | "balanced";
    risk_tolerance?: number;
  };
}
```

**Returns:**
```typescript
interface AnalysisResult {
  risk_score: number;                    // 0-1
  intervention_level: "none" | "L1" | "L2" | "L3";
  intervention_message: string;
  confidence: number;                    // 0-1
  evidence?: Array<{type: string; description: string; strength: number}>;
  timestamp: string;
  metadata?: {processing_time: number};
}
```

#### Example Response
```json
{
  "risk_score": 0.78,
  "intervention_level": "L2",
  "intervention_message": "⚠️ I notice you're working very late with little sleep...",
  "confidence": 0.85,
  "evidence": [
    {"type": "time_risk", "description": "Working at 02:30", "strength": 0.9}
  ],
  "timestamp": "2026-04-12T02:30:00Z"
}
```

---

## 📊 Intervention Levels

| Level | Trigger | Action | Example Message |
|-------|---------|--------|-----------------|
| **L1** | Score 0.3-0.6 | Gentle reminder | "💡 Just a heads up: this reminds me of your 'quick fix' pattern..." |
| **L2** | Score 0.6-0.9 | Active intervention | "⚠️ Hold on! Let's think about this more carefully..." |
| **L3** | Score >0.9 | Forced interruption | "🚨 HARD STOP. I cannot help you continue in this state..." |

---

## 🔌 REST API

### Endpoint: POST /analyze

```bash
curl -X POST http://localhost:8080/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "user_input": "I need to finish this now!",
    "context": {
      "time": "02:30",
      "sleep_hours": 3
    }
  }'
```

**Response:**
```json
{
  "success": true,
  "data": {
    "risk_score": 0.78,
    "intervention_level": "L2",
    "intervention_message": "...",
    "confidence": 0.85
  }
}
```

### Endpoint: GET /health

```bash
curl http://localhost:8080/health
```

**Response:**
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "uptime": 3600,
  "requests_processed": 1523
}
```

### Endpoint: GET /metrics

```bash
curl http://localhost:8080/metrics
```

**Response:**
```json
{
  "total_requests": 1523,
  "interventions_by_level": {"L1": 234, "L2": 89, "L3": 12},
  "average_risk_score": 0.45,
  "average_processing_time_ms": 45
}
```

---

## ⚙️ Configuration

### Manifest Configuration (manifest.yaml)

```yaml
config:
  intervention_levels:
    l1_threshold: 0.3
    l2_threshold: 0.6
    l3_threshold: 0.9

  monitoring:
    check_interval: 300
    history_window: 2592000

  response:
    max_response_length: 500
    include_evidence: true
```

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `GUARDIAN_LOG_LEVEL` | INFO | Logging level |
| `GUARDIAN_DEBUG_MODE` | false | Enable debug output |
| `GUARDIAN_PORT` | 8080 | REST API port |

---

## 🧪 Testing

```python
from guardian_safety_engine import GuardianSafetyEngine
import unittest

class TestGuardianSafetyEngine(unittest.TestCase):
    
    def setUp(self):
        self.engine = GuardianSafetyEngine()
    
    def test_normal_input(self):
        result = self.engine.analyze_risk(
            "How do I implement this feature?",
            {"time": "14:00", "sleep_hours": 8}
        )
        self.assertLess(result["risk_score"], 0.3)
    
    def test_high_risk_input(self):
        result = self.engine.analyze_risk(
            "I must finish this tonight!",
            {"time": "02:30", "sleep_hours": 3}
        )
        self.assertGreaterEqual(result["risk_score"], 0.7)
    
    def test_error_handling(self):
        result = self.engine.analyze_risk("", {})
        self.assertIsNotNone(result)
```

---

## 🔍 Troubleshooting

### Common Issues

**1. High False Positive Rate**
```yaml
# Solution: Adjust thresholds in manifest.yaml
config:
  intervention_levels:
    l1_threshold: 0.4  # Increase threshold
    l2_threshold: 0.7
```

**2. Slow Response Time**
```yaml
# Solution: Enable caching
config:
  monitoring:
    enable_cache: true
    cache_ttl: 300
```

**3. Missing Context Data**
```python
# Solution: Ensure all required context fields
context = {
    "time": "14:00",
    "sleep_hours": 7,
    "stress_level": 3
}
```

---

**© 2026 Maxime Xian. Apache 2.0 License.**
