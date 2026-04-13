# Sleep Guardian API Reference

## 📋 Overview

Sleep Guardian monitors user sleep patterns and energy levels to provide adaptive AI responses based on physiological state. It automatically adjusts response complexity and length based on detected energy levels.

**Key Capabilities:**
- 💤 Sleep pattern monitoring
- ⚡ Energy level assessment
- 🎯 Dynamic response adjustment
- 🔔 Smart reminders and alerts

---

## 🚀 Quick Start

### Basic Usage

```javascript
const SleepGuardian = require('./sleep-guardian');

// Initialize
const guardian = new SleepGuardian();

// Check current energy status
const status = guardian.getEnergyStatus();

console.log(`Status: ${status.status}`);
console.log(`Sleep Hours: ${status.sleep_hours}`);
console.log(`Max Response Length: ${status.restrictions.max_response_length}`);
```

---

## 🔧 Core API

### SleepGuardian Class

#### Constructor
```javascript
constructor(config?: SleepGuardianConfig)
```

**Parameters:**
```typescript
interface SleepGuardianConfig {
  checkInterval?: number;      // ms, default: 300000 (5 min)
  lowSleepThreshold?: number;   // hours, default: 5
  optimalSleepThreshold?: number; // hours, default: 7
}
```

#### getEnergyStatus Method
```javascript
getEnergyStatus(): EnergyStatus
```

**Returns:**
```typescript
interface EnergyStatus {
  status: 'LOW' | 'SUBOPTIMAL' | 'NORMAL';
  sleep_hours: number;
  confidence: number;
  recommendations: string[];
  restrictions: {
    max_response_length: number;
    allowed_complexity: 'simple' | 'moderate' | 'full';
    complex_reasoning_enabled: boolean;
  };
  timestamp: string;
}
```

**Example Response:**
```json
{
  "status": "LOW",
  "sleep_hours": 4,
  "confidence": 0.92,
  "recommendations": [
    "Take a 20-minute break",
    "Consider stopping work soon",
    "Stay hydrated"
  ],
  "restrictions": {
    "max_response_length": 120,
    "allowed_complexity": "simple",
    "complex_reasoning_enabled": false
  },
  "timestamp": "2026-04-12T14:30:00Z"
}
```

#### checkSystemStatus Method
```javascript
checkSystemStatus(): SystemStatus
```

**Returns:**
```typescript
interface SystemStatus {
  system_uptime: number;           // seconds
  last_user_activity: string;      // ISO timestamp
  active_processes: string[];
  cpu_usage: number;               // percentage
  memory_usage: number;            // percentage
  estimated_awake_duration: number; // seconds
  detected_pattern: 'normal' | 'overwork' | 'at_risk';
}
```

#### shouldSendReminder Method
```javascript
shouldSendReminder(): ReminderResult
```

**Returns:**
```typescript
interface ReminderResult {
  should_remind: boolean;
  reminder_type: 'rest' | 'break' | 'sleep' | 'none';
  message: string;
  priority: 'low' | 'medium' | 'high';
}
```

---

## 📊 Energy Levels

| Status | Sleep Hours | Response Length | Complexity | Reasoning |
|--------|-------------|-----------------|------------|-----------|
| **LOW** | < 5h | ≤ 120 words | Simple only | Disabled |
| **SUBOPTIMAL** | 5-7h | ≤ 200 words | Moderate | Limited |
| **NORMAL** | > 7h | ≤ 1000 words | Full | Enabled |

---

## 🔌 REST API

### Endpoint: GET /energy-status

```bash
curl http://localhost:8081/energy-status
```

**Response:**
```json
{
  "success": true,
  "data": {
    "status": "SUBOPTIMAL",
    "sleep_hours": 6,
    "confidence": 0.88
  }
}
```

### Endpoint: GET /system-status

```bash
curl http://localhost:8081/system-status
```

**Response:**
```json
{
  "success": true,
  "data": {
    "system_uptime": 43200,
    "last_activity": "2026-04-12T14:25:00Z",
    "detected_pattern": "normal"
  }
}
```

### Endpoint: GET /health

```bash
curl http://localhost:8081/health
```

**Response:**
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "uptime": 86400,
  "last_check": "2026-04-12T14:30:00Z"
}
```

---

## ⚙️ Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `SLEEP_CHECK_INTERVAL` | 300 | Check interval in seconds |
| `SLEEP_LOW_THRESHOLD` | 5 | Hours for LOW status |
| `SLEEP_OPTIMAL_THRESHOLD` | 7 | Hours for NORMAL status |
| `SLEEP_LOG_LEVEL` | INFO | Logging level |
| `SLEEP_PORT` | 8081 | REST API port |

---

## 🧪 Testing

```javascript
const SleepGuardian = require('./sleep-guardian');
const assert = require('assert');

describe('SleepGuardian', () => {
  let guardian;
  
  beforeEach(() => {
    guardian = new SleepGuardian();
  });
  
  test('LOW status with <5h sleep', () => {
    const status = guardian.getEnergyStatus();
    expect(status.status).toBeDefined();
  });
  
  test('returns valid restrictions', () => {
    const status = guardian.getEnergyStatus();
    expect(status.restrictions.max_response_length).toBeGreaterThan(0);
  });
  
  test('health check endpoint', () => {
    const health = guardian.getHealth();
    expect(health.status).toBe('healthy');
  });
});
```

---

## 🔍 Troubleshooting

### Common Issues

**1. Inaccurate Sleep Estimation**
```javascript
// Solution: Provide explicit sleep data
guardian.setExplicitSleepData({
  last_sleep: '2026-04-11T23:00:00Z',
  wake_time: '2026-04-12T07:00:00Z'
});
```

**2. Too Many Reminders**
```yaml
# Solution: Adjust reminder frequency
config:
  reminders:
    rest_reminder_interval: 7200  # 2 hours
    max_daily_reminders: 5        # Reduce from 10
```

**3. Performance Issues**
```yaml
# Solution: Reduce check frequency
config:
  monitoring:
    check_interval: 600  # 10 minutes instead of 5
```

---

**© 2026 Maxime Xian. Apache 2.0 License.**
