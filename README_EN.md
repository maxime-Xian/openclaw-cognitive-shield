# 🧠 Max-Cognitive-Shield

[English](./README_EN.md) | [简体中文](./README.md)

[![GitHub License](https://img.shields.io/github/license/maxime-Xian/max-cognitive-shield)](https://github.com/maxime-Xian/max-cognitive-shield/blob/main/LICENSE)
[![GitHub Stars](https://img.shields.io/github/stars/maxime-Xian/max-cognitive-shield)](https://github.com/maxime-Xian/max-cognitive-shield/stargazers)
[![GitHub Forks](https://img.shields.io/github/forks/maxime-Xian/max-cognitive-shield)](https://github.com/maxime-Xian/max-cognitive-shield/network/members)
[![GitHub Issues](https://img.shields.io/github/issues/maxime-Xian/max-cognitive-shield)](https://github.com/maxime-Xian/max-cognitive-shield/issues)
[![OpenClaw](https://img.shields.io/badge/Platform-OpenClaw-orange)](https://openclaw.ai)

> **Transform your AI from an obedient assistant into an active, protective "Prefrontal Guardian".**

## 📖 Project Background

In the AI era, we often face these dilemmas:
- 🌙 **1 AM Obsession**: Falling into the mania of "fixing just one more bug," leading to low efficiency and health damage.
- 😤 **Emotional Rumination**: Falling into a spiral of self-attack in front of the AI ("I'm so useless, why can't I ever do this right?").
- 🤯 **Decision Overload**: Late-night brainstorms commanding the AI to perform massive, unrealistic refactors.

**Max-Cognitive-Shield** is an open-source **Meta-Cognitive Operating System (Meta-Cognitive OS)** designed for AI Agents (especially for the [OpenClaw](https://openclaw.ai) framework). It moves beyond the traditional "command-response" model, empowering AI to recognize user self-depletion patterns (Legacy Scripts) and proactively intervene at critical moments.

---

## ✨ Core Features

1. 🚦 **Three-Level Proactive Intervention Engine (L1/L2/L3)**
   - **L1 Green to Yellow (Gentle Reminder)**: "You just mentioned... This sounds a bit like your old pattern of [Specific Behavior]..."
   - **L2 Yellow (Active Intervention)**: Forces a task pause, presents historical lessons as evidence, and guides the user through meta-cognitive reflection.
   - **L3 Red (Forced Interrupt)**: Triggered by critical risks (e.g., severe sleep deprivation, cardiac warnings, manic episodes). Fully halts complex reasoning and provides recovery guidance.

2. 🔍 **Dual-Channel Intent Filtering Protocol**
   - Accurately distinguishes whether a phrase is a user's "true expression" or simply "quoting/debugging," preventing false positives from code comments or logs.

3. 📜 **Legacy Script Blocking System**
   - Everyone has their own "self-depletion scripts" (e.g., Willpower Cult, Perfectionist Evasion). Users can define trigger keywords to let the AI guard against them.

4. 🧠 **Meta-Cognitive Monitoring & Energy Management**
   - Built-in awareness of "Cognitive Load," "Learning Stagnation," and "Sleep Vulnerability." When the user is under high stress, the AI automatically shifts from "Execution Mode" to "Protection Mode."

---

## 🛠️ Tech Stack

- **Core Language**: Python 3.9+
- **Protocols**: gRPC (High-performance analysis), REST API (Flexible integration)
- **Deployment**: Docker (One-click), OpenClaw Skill (Native integration)
- **Security**: SHA-256 data anonymization, AES-256 encrypted storage, GDPR/CCPA compliant

---

## 📂 Directory Structure

```text
.
├── api/                # API Definitions (OpenAPI YAML)
├── core/               # Core Protocols (Meta-Cognitive OS Layer)
├── docs/               # Detailed Documentation
├── knowledge/          # Knowledge Base (Cognitive Bias, Mental Models, Methodology)
├── proto/              # gRPC Protocol Definitions
├── scripts/            # Deployment & Setup Scripts
├── skills/             # OpenClaw Skill Definitions
├── src/                # Source Code Implementation
└── test/               # Test Suite (Unit & Integration)
```

---

## 🚀 Quick Start

### Option A: Install via OpenClaw (Recommended)

```bash
# Install core Safety Engine Skill
clawhub install guardian-safety-engine

# Clone and initialize base protocols
git clone https://github.com/maxime-Xian/max-cognitive-shield.git
cd max-cognitive-shield
./scripts/setup.sh
```

### Option B: Manual Deployment (Docker)

```bash
docker run -d \
  --name cognitive-shield \
  -p 8080:8080 \
  -p 50051:50051 \
  skill-max-cognitive-shield:1.0.0
```

---

## 💡 Usage Example

**Scenario: User attempting to overwork late at night**
> User: "I'm so tired, but I have to finish this refactor tonight."
>
> **AI Intervention (L2)**: "Detected 'Willpower Cult' script trigger. Based on your records in `USER.md`, such decisions usually lead to significant rework the next day. I suggest resting immediately. I have temporarily locked complex modification features."

---

## 📊 Performance Benchmarks

| Metric | Value | Notes |
|------|------|------|
| Analysis Latency (gRPC) | < 50ms | Excellent real-time performance |
| Memory Usage | ~200MB | Lightweight deployment |
| Accuracy (Intent ID) | 94.2% | Based on Dual-Channel Filtering |

---

## ❓ FAQ

**Q: Will this interfere with my normal coding work?**
A: No. The Dual-Channel Filtering protocol precisely identifies code contexts and only intervenes when obvious cognitive risk patterns are detected.

**Q: Is my data safe?**
A: This project is fully open-source. All data is anonymized and supports fully local deployment.

---

## 🗺️ Roadmap & Changelog

- [x] v1.0.0: Core intervention engine released
- [ ] v1.1.0: Support for heart rate monitors/physiological data (Planned)
- [ ] v1.2.0: Multi-agent collaborative protection mode (Planned)

---

## 🤝 Contributing

We welcome community contributions! Please see [CONTRIBUTING.md](./docs/CONTRIBUTING.md) for how to submit PRs or report issues.

---

## 📄 License

This project is licensed under the [Apache License 2.0](./LICENSE).

---

## 📮 Contact

- **Author**: Maxime Xian
- **Community**: [Discord](https://discord.gg/your-link) | [WeChat Official Account](https://weixin.qq.com/r/your-id)
- **GitHub**: [@maxime-Xian](https://github.com/maxime-Xian)
