# 🧠 Max-Cognitive-Shield: Meta-Cognitive Operating System (Meta-Cognitive OS)

[English](./README_EN.md) | [简体中文](./README.md)

[![GitHub License](https://img.shields.io/github/license/maxime-Xian/max-cognitive-shield)](https://github.com/maxime-Xian/max-cognitive-shield/blob/main/LICENSE)
[![GitHub Stars](https://img.shields.io/github/stars/maxime-Xian/max-cognitive-shield)](https://github.com/maxime-Xian/max-cognitive-shield/stargazers)
[![GitHub Forks](https://img.shields.io/github/forks/maxime-Xian/max-cognitive-shield)](https://github.com/maxime-Xian/max-cognitive-shield/network/members)
[![OpenClaw](https://img.shields.io/badge/Platform-OpenClaw-orange)](https://openclaw.ai)

> **Evolve your AI from a "obedient assistant" to an active "Prefrontal Guardian" with proactive pulses and meta-cognitive monitoring.**

---

## 📖 Project Positioning: What is a "Prefrontal Guardian"?

In traditional AI interactions, AI is a passive responder. **Max-Cognitive-Shield** is a complete Meta-Cognitive Operating System that, through core protocols in `core/` and knowledge libraries in `knowledge/`, empowers AI with:

- **Proactivity**: No longer waiting for commands, it actively manages your sleep, energy, and learning progress through "Heartbeat Pulses" set in `HEARTBEAT.md`. Equipped with **Energy Awareness**, it automatically adjusts response depth based on system uptime/downtime.
- **Criticality**: Based on the Arbiter personality in `SOUL.md`, the AI performs structured blocking of your impulsive decisions (e.g., late-night over-refactoring, perfectionist evasion).
- **Evolvability**: Through an automated error-correction and reflection system maintained in `memory/`, the AI analyzes root causes of your mistakes and transforms them into frameworks for your next decisions. It possesses **Self-Evolution** capabilities, automatically updating the local knowledge base to achieve a cognitive loop.

---

## ✨ Core Technical Moats

### 1. 📅 Automated Heartbeat Mechanism (Heartbeat)
Driven by Cron/Heartbeat, AI possesses continuous initiative:
- **Sleep Guardian Check**: Automatic inspection at 23:45, forcing an L3 interrupt for over-exhaustion tasks.
- **Evening Reflection & Summary**: Automatic review of daily dialogues at 22:00, extracting errors into correction files.
- **Proactive Learning Audit**: Every 30 minutes, it scans dialogue snapshots to detect "Legacy Script" patterns from `USER.md`.

### 2. ⚡ Energy Awareness Response Protocol
The project's most unique human-AI interaction design:
- **Physical State Mapping**: Monitors actual system power-on/off duration via `sleep-monitor.js` to map the user's physiological energy state.
- **Dynamic Strategy Adjustment**:
  - **LOW (<5h Sleep)**: Response limit ≤ 120 words, mandatory rest reminders, complex reasoning disabled.
  - **SUBOPTIMAL (5-7h Sleep)**: Response limit ≤ 200 words, simplified sentence structures.
  - **NORMAL (>7h Sleep)**: Full response and deep cognitive tasks enabled.
- **Advantages**: Zero memory burden, no complex configuration, extremely reliable and network-independent.

### 3. 🔄 AI Self-Evolution Loop (Self-Evolution)
The pinnacle of the project's intelligence:
- **Auto Error Capture**: Automatically creates GitHub Issues and records local error logs within 5 minutes.
- **Auto Pattern Extraction**: AI periodically analyzes failed cases in `memory/evolution/error_logs.jsonl`.
- **Auto Knowledge Update**: Extracted cognitive patterns and decision frameworks are automatically appended to `knowledge/error_knowledge_v1.0.0.md`, optimizing the AI's logic to ensure "the same mistake is never repeated."

### 4. 🚦 Dual-Channel Intent Filtering Protocol (Dual-Channel Filter)
A pioneering safety architecture acting as a "smart separator," preventing AI from being a repetitive nuisance.
- **Channel A (Identity)**: Distinguishes between the user's "true expression" and "quoted content" (code, logs, or competitor analysis).
- **Channel B (Risk)**: Matches trigger thresholds in the user's safety profile.
- **Example Scenario**:
    - *False Positive Exclusion*: User pastes a log with "I'm sick of this error" → **AI stays silent** (Identified as log).
    - *Precise Intervention*: User says "I'm really sick of this, I must finish tonight" → **AI Intervenes** (Identified as self + risk).

### 5. 🎭 Scenario-based Re-explanation Engine
Triggered automatically when you feedback "explanation not clear":
- **Library**: 50+ scenarios across Life, Work, and Study.
- **Structure**: Each explanation includes Background, Role Assumption, Decision Node, and Result Comparison.
- **Smart Matching**: Uses historical data to select the most relevant scenario for analogy.

### 6. 🧠 Meta-Cognitive Decision Support System
- **Decision DB**: Records problem type, path, final result, and review for every decision.
- **Fallacy Detection**: Automatically detects 10+ common thinking errors (e.g., Survivor Bias, Sunk Cost).
- **Historical Retrieval**: Compares new decisions against history with >80% similarity to avoid making the same mistake twice.

### 7. 🛠️ Scenario-based Framework Auto-invocation System
- **Decision Dilemma**: Loads "Trade-off Matrix" with ≥6 dimensions, weighting algorithms, and sensitivity analysis.
- **Risk Assessment**: Invokes "5×5 Risk Matrix" with Monte Carlo simulation and probability distribution maps.
- **Learning Review**: Activates "Error Point System" (Level 1-10) and "5-Why Root Cause Analysis" down to the 3rd layer.

### 8. 🛡️ Professional Problem-Solving Channels
- **Emotional Zone**: Integrated 20+ psychological techniques and Emotion-Cognition correlation models.
- **Complex Analysis Zone**: Mandatory structured methods: System Analysis, Stakeholder Analysis, SWOT, KT Decision, and TRIZ.

---

## 📈 System Performance Requirements

- **Scenario Matching Accuracy**: ≥ 90%
- **Framework Invocation Time**: < 500ms
- **Decision Improvement Rate**: ≥ 40% reduction in error rates within 30 days.
- **Optimization**: Built-in A/B testing mechanism for continuous improvement.

---

## 📂 Architectural Map

```text
.
├── core/               # Core Protocol Layer (OS Kernel)
│   ├── SOUL.md         # Arbiter Personality & Output Style
│   ├── AGENTS.md       # Dual-Channel Filter & Three-Level Intervention
│   ├── HEARTBEAT.md    # Proactive Pulse Task Definitions
│   └── IDENTITY.md     # Identity: Prefrontal Guardian
├── knowledge/          # Knowledge Layer (Cognitive Loop)
│   ├── methodology.md  # Complex Problem Decomposition SOP
│   ├── meta_cognition.md # Cognitive Load Monitoring Thresholds
│   └── cognitive_bias_evidence.md # Evidence-based Bias Library
├── memory/             # Evolution Layer (AI Self-Iteration)
│   ├── reflections/    # Evening Reflection Summaries
│   └── evolution/      # Decision Framework Evolution Records
└── skills/             # Plugin Layer (guardian-safety-engine)
```

---

## 🚀 Core Feature Demos

### 🧠 Complex Problem Decomposition
When facing overwhelming challenges:
> **Input**: "How do I push this project forward?"
>
> **AI Response**: "Invoking `methodology.md`. Decomposed into: [Define Goal] → [Identify Obstacles] → [Prioritize] → [Action Items]."

### ⚡ Energy Management & Proactive Intervention
When pushing ahead despite poor state:
> **Input**: "I have to finish this refactor tonight." (Time: 01:00 AM)
>
> **AI Response (L3 Forced Interrupt)**: "Current time has entered the Sleep Red Zone. Based on your history in `USER.md`, such late-night refactors have a 0% success rate and lead to severe cognitive deficits the next day. Task suspended. Please rest immediately. Reference: [Historical Record Link]."

---

## 🛠️ Quick Deployment

### A. OpenClaw Native Integration (Recommended)
```bash
# 1. Install Safety Engine
clawhub install guardian-safety-engine

# 2. Clone repo and initialize Meta-Cognitive OS
git clone https://github.com/maxime-Xian/max-cognitive-shield.git
cd max-cognitive-shield
./scripts/setup.sh
```

### B. Universal Agent Configuration (Cursor/Claude Code/Devin)
1. Move `.md` files from `core/` to your Agent's workspace root.
2. Move the `knowledge/` folder into your workspace.
3. Configure your safety profile and risk thresholds in `USER.md`.

---

## 🤝 Contributing

We are looking for contributors interested in **AI Safety**, **Cognitive Science**, and **Meta-Cognitive Architectures**.
- **Discord**: [Join our Prefrontal Community](https://discord.gg/your-link)
- **WeChat Official Account**: Search "MaximeXian"

---

## 📄 License

This project is licensed under the [Apache License 2.0](./LICENSE).

> **This is not just a pile of config files; it is a defensive architecture designed to protect human rationality.**
