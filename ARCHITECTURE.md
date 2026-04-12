# Max-Cognitive-Shield 架构详解

## 1. 设计哲学：前额叶监护人 (Prefrontal Guardian)

本项目不仅仅是一套 Prompt，而是一个完整的**元认知操作系统**。它的设计灵感来源于人类大脑的“前额叶”，旨在弥补当前 LLM 仅能“听从指令”而缺乏“理智监督”的缺陷。

---

## 2. 核心分层架构

项目采用四层解耦架构，确保在 OpenClaw 平台上的轻量化运行与深度集成：

### 2.1 协议层 (Protocol Layer) - `/core`
这是 Agent 的“主脑指令集”，在会话启动时被注入：
- **SOUL.md**：定义了 AI 的底线、语气、人格基线及**能量感知响应逻辑**。
- **AGENTS.md**：定义了核心逻辑流（检索-诊断-策略），特别是**双通道过滤协议**。
- **HEARTBEAT.md**：定义了主动任务列表，将 AI 从“被动”转化为“主动”。

### 2.2 知识层 (Knowledge Layer) - `/knowledge`
这是 Agent 的“专业工具库”：
- **循证偏差库**：收录了 20+ 种认知偏差，由 AI 在检测到相关模式时自动调用。
- **方法论 SOP**：包含复杂问题拆解、根因分析等结构化思维框架。
- **阈值管理**：在 `meta_cognition.md` 中定义了具体的能量等级与干预红线。

### 2.3 记忆层 (Memory Layer) - `/memory`
这是 Agent 的“自我进化区”，与 OpenClaw Memory API 深度对齐：
- **daily/**：存放 OpenClaw 原生的 YYYY-MM-DD.md 格式日志。
- **evolution/**：记录 AI 从错误中提炼的模式，实现“同样的错误不犯第二次”。
- **pending/**：核心防护区，所有规则修改建议必须在此缓冲，待用户手动“批准”。

### 2.4 脚本层 (Script Layer) - `/scripts`
这是物理世界的“传感器”与“执行器”：
- **sleep-guardian.js**：通过系统 API 获取开关机时长，计算生理能量。
- **nightly-summary.py**：执行晚间总结与反思，将对话转化为认知经验。

---

## 3. 核心机制流程

### 3.1 主动脉冲 (Proactive Pulse)
1. **触发**：Heartbeat 定时触发脚本执行。
2. **分析**：脚本读取当前对话快照与环境数据（如时间、能量）。
3. **注入**：如果命中干预阈值，向 OpenClaw 发送一个 `agentTurn`，告知 Agent 立即介入。

### 3.2 意图双通道过滤 (Dual-Channel Filter)
1. **通道 A (Identity)**：判断文本属于“代码/引用/日志”还是“用户表达”。
2. **通道 B (Risk)**：判断内容是否命中“深夜硬刚”、“情绪失控”等风险点。
3. **决策**：仅当 A 与 B 同时为真时，触发 L2/L3 级强制干预。

---

## 4. 与 OpenClaw 的集成

本项目专为 OpenClaw 优化：
- **原生支持**：文件结构完全匹配 OpenClaw Workspace 规范。
- **Memory Search**：利用 OpenClaw 的向量搜索功能，实现对历史决策的快速回弹。
- **QMD 兼容**：所有协议均为标准 Markdown，支持 QMD 本地语义搜索引擎。

---

_Max-Cognitive-Shield：让 AI 成为您理性的最后一道防线。_
