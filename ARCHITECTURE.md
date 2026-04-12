# Max-Cognitive-Shield 架构详解

## 1. 设计哲学：前额叶监护人 (Prefrontal Guardian)

本项目不仅仅是一套 Prompt，而是一个完整的**元认知操作系统**。它的设计灵感来源于人类大脑的“前额叶”，旨在弥补当前 LLM 仅能“听从指令”而缺乏“理智监督”的缺陷。

---

## 2. 核心分层架构

项目采用四层解耦架构，确保在 OpenClaw 平台上的轻量化运行与深度集成：

### 2.1 协议层 (Protocol Layer) - `/core`
这是 Agent 的“主脑指令集”，在会话启动时被注入：
- **SOUL.md**：定义了 AI 的底线、语气、人格基线及**能量感知响应逻辑**。
- **AGENTS.md**：定义了核心逻辑流（检索-诊断-策略），特别是**意图过滤协议**。
- **IDENTITY.md**：定义了前额叶监护人的身份特征。
- **HEARTBEAT.md**：定义了定时任务，将 AI 从“被动”转化为“主动”。

### 2.2 知识层 (Knowledge Layer) - `/knowledge`
这是 Agent 的“专业工具库”：
- **循证偏差库**：收录了 20+ 种认知偏差。
- **方法论 SOP**：包含复杂问题拆解、根因分析等结构化思维框架。
- **思维模型映射**：通过 `problem_model_map.yaml` 实现场景与框架的自动关联。

### 2.3 记忆层 (Memory Layer) - `/memory`
这是 Agent 的“成长区”，与 OpenClaw 深度兼容：
- **daily/**：OpenClaw 原生每日日志。
- **reflections/**：存放晚间反思汇总。
- **evolution/**：记录 AI 从错误中提炼的模式。
- **pending/**：核心防护区，提供规则写入保护。

### 2.4 脚本层 (Script Layer) - `/scripts`
这是物理世界的“传感器”与“执行器”：
- **sleep-guardian.js**：监测系统开关机时长，输出能量状态。
- **nightly-summary.py**：执行晚间总结。
- **error-capture.py**：自动捕获并记录错误。

---

## 3. 核心机制流程

### 3.1 主动脉冲 (Proactive Pulse)
1. **触发**：Heartbeat 定时触发脚本执行。
2. **分析**：脚本读取当前对话快照与环境数据。
3. **注入**：如果命中阈值，执行对应级别的干预。

### 3.2 意图双通道过滤 (Dual-Channel Filter)
1. **通道 A (Identity)**：判断文本属于“技术引用”还是“用户表达”。
2. **通道 B (Risk)**：判断内容是否命中风险点。
3. **决策**：仅当 A 与 B 同时满足时，触发干预。

---

_Max-Cognitive-Shield：让 AI 成为您理性的最后一道防线。_
