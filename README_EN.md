# 🧠 Max-Cognitive-Shield 

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

> **Transform your AI from an obedient assistant into an active, protective "Prefrontal Guardian".**

Have you ever experienced this?
- 🌙 It's 1 AM, you're manic and trying to "fix just one more bug", only to discard everything the next morning.
- 😤 You fall into a spiral of self-attack: "I'm so useless, why does this always happen to me?"
- 🤯 Late at night, you're flooded with epic ideas and try to command your AI to do a massive, unrealistic refactor.

**Max-Cognitive-Shield** is an open-source **Meta-Cognitive Operating System (Meta-Cognitive OS)** designed for AI Agents (especially for [OpenClaw](https://openclaw.ai) and similar agent frameworks). It moves beyond the traditional "prompt-response" paradigm, empowering AI with the ability to detect your self-destructive behavioral patterns (Legacy Scripts) and proactively interrupt you at the most critical moments.

---

## ✨ Core Moat & Features

This system is built upon a battle-tested cognitive defense architecture:

1. 🚦 **Three-Level Proactive Intervention Engine (L1/L2/L3)**
   - **L1 Green to Yellow**: Gentle reminder ("You just mentioned... This sounds a bit like your old pattern of...")
   - **L2 Yellow**: Active Intervention (Pauses the task, presents your own historical lessons as evidence, forces reflection.)
   - **L3 Red / Forced Interrupt**: Triggered by critical risks (like severe sleep deprivation, cardiac warnings, manic episodes). Fully halts the AI's complex reasoning and provides recovery guidance.

2. 🔍 **Dual-Channel Intent Filtering Protocol**
   - The AI accurately distinguishes whether a phrase is truly "you speaking" or simply "you quoting someone else." Prevents false positives caused by code comments or debug logs.

3. 📜 **Legacy Script Blocking System**
   - Everyone has their own "self-destructive scripts" (e.g., Willpower Cult, Perfectionist Evasion). You define your own trigger keywords and let the AI guard against them.

4. 🧠 **Meta-Cognitive Monitoring & Energy Management**
   - Built-in awareness of "Cognitive Load", "Learning Stagnation", and "Sleep Vulnerability." If you're overloaded, the AI automatically shifts from "Execution Mode" back into "Protection Mode".

---

## 🚀 Quick Start

### Option A: Install via ClawHub (OpenClaw Environments)

If you are using the OpenClaw framework, simply pull the core Safety Engine Skill:

```bash
clawhub install guardian-safety-engine
```

Then, clone this repo to deploy the base protocols and architecture in your workspace:

```bash
git clone https://github.com/maxime-Xian/max-cognitive-shield.git
cd max-cognitive-shield
./scripts/setup.sh
```

### Option B: Manual Setup (For Any LLM Agent)

At its core, this architecture relies on a structured hierarchy of Markdown prompts and protocols that can be adopted by any agent capable of reading workspace files (like Cursor, Claude Code, Devin, etc.).

```bash
git clone https://github.com/maxime-Xian/max-cognitive-shield.git
cd max-cognitive-shield
```

1. Move `.md` files from `core/` to the root of your Agent's workspace.
2. Move the `knowledge/` folder into your workspace.
3. Open `USER.md` and complete your **Safety Profile** and **Cognitive Preferences** based on the embedded guidelines.

---

## 📂 Architecture & Knowledge Modules (L0-L6)

Max-Cognitive-Shield is designed as a strict top-down knowledge tree:

*   **L0 Core Routing Layer**
    *   `SOUL.md`: AI personality baseline. Forces the AI to remain an "objective, structured, non-emotional" arbiter.
    *   `AGENTS.md`: Entry-point for request classification (Simple vs. Complex vs. State-based) and intervention routing.
    *   `USER.md`: Stores the user's cognitive bottlenecks, preferences, and high-risk signals.
*   **L1-L6 Knowledge Layer**
    *   `methodology.md`: SOPs for analyzing complex problems.
    *   `human_framework.md`: Theories including Kahneman's System 1/2 and Sweller's Cognitive Load.
    *   `meta_cognition.md`: Threshold configurations.
    *   `cognitive_bias_evidence.md` & `mental_models_index.md`: Evidence libraries used to push back against user biases.
*   **Skills (Pluggable Capabilities)**
    *   `guardian-safety-engine`: V3.3 dynamically loaded pulse engine.

---

## ⚖️ License & Attribution

This project is open-sourced under the [Apache License 2.0](./LICENSE).

**Core Principle**: You are free to use, modify, and even commercialize this architecture, but **you must retain the attribution notice** (refer to the [`NOTICE`](./NOTICE) file). This is our way of protecting the original architectural logic and IP while allowing the community to benefit.

> This isn't just a pile of config files; it is a defensive architecture designed for human rationality.

---
*Powered by Maxime Xian & The OpenClaw Community*
