# 🧠 Max-Cognitive-Shield: 元认知操作系统 (Meta-Cognitive OS)

[English](./README_EN.md) | [简体中文](./README.md)

[![GitHub License](https://img.shields.io/github/license/maxime-Xian/max-cognitive-shield)](https://github.com/maxime-Xian/max-cognitive-shield/blob/main/LICENSE)
[![GitHub Stars](https://img.shields.io/github/stars/maxime-Xian/max-cognitive-shield)](https://github.com/maxime-Xian/max-cognitive-shield/stargazers)
[![GitHub Forks](https://img.shields.io/github/forks/maxime-Xian/max-cognitive-shield)](https://github.com/maxime-Xian/max-cognitive-shield/network/members)
[![OpenClaw](https://img.shields.io/badge/Platform-OpenClaw-orange)](https://openclaw.ai)

> **将您的 AI 从“言听计从”的助手，进化为具备“主动脉冲”与“元认知监测”能力的——前额叶监护人 (Prefrontal Guardian)。**

---

## 📖 项目定位：什么是“前额叶监护人”？

在传统的 AI 交互中，AI 只是被动响应指令。而 **Max-Cognitive-Shield** 是一套完整的元认知操作系统，它通过 `core/` 下的核心协议与 `knowledge/` 库，赋予 AI 以下能力：

- **主动性**：不再等待指令，通过 `HEARTBEAT.md` 设定的“心跳脉冲”主动管理您的睡眠、精力和学习进度。具备**能量感知 (Energy Awareness)** 能力，基于系统开关机时长自动调节响应深度。
- **批判性**：基于 `SOUL.md` 的仲裁者人格，AI 会对您的冲动决策（如深夜过度重构、完美主义逃避）进行结构化阻断。
- **进化性**：通过 `memory/` 自动维护的纠错与反射系统，AI 能够分析您的错误根因，并将其转化为下次决策的框架。具备**自我进化 (Self-Evolution)** 能力，自动更新本地知识库，实现认知闭环。

---

## ✨ 核心技术护城河

### 1. 📅 自动化脉冲机制 (Heartbeat)
通过 Cron/Heartbeat 驱动，AI 拥有持续的主动性：
- **睡眠守护检查**：深夜 23:45 自动巡检，强制阻断 L3 级过劳任务。
- **晚间总结与反思**：22:00 自动回顾今日对话，提炼失误并写入纠错档案。
- **主动学习巡检**：每 30 分钟扫描对话快照，检测是否命中 `USER.md` 中的“旧脚本”模式。

### 2. ⚡ 能量感知响应协议 (Energy Awareness)
本项目最独特的人机交互设计：
- **物理状态映射**：通过 `sleep-monitor.js` 监测系统实际开机/关机时长，真实映射用户的生理能量状态。
- **动态策略调节**：
  - **LOW (<5h 睡眠)**：响应限制 ≤ 120 字，强制休息提醒，禁止复杂推理。
  - **SUBOPTIMAL (5-7h 睡眠)**：响应限制 ≤ 200 字，简化句式。
  - **NORMAL (>7h 睡眠)**：开放完整响应与深度认知任务。
- **优势**：零记忆负担，无需复杂配置，运行极其可靠且不依赖网络。

### 2. 🔄 AI 自我进化闭环 (Self-Evolution)
这是本项目最核心的“智能”体现：
- **错误自动捕获**：5 分钟内自动创建 GitHub Issue 并记录本地错误日志。
- **模式自动提炼**：AI 定期分析 `memory/evolution/error_logs.jsonl` 中的失败案例。
- **知识库自动更新**：提炼出的新认知模式与决策框架，将自动追加至 `knowledge/error_knowledge_v1.0.0.md`，实现 AI 逻辑的自我优化，确保“同样的错误不犯第二次”。

### 4. 🚦 意图双通道过滤协议 (Dual-Channel Filter)
本项目首创的安全架构，像是一个“聪明的分辨器”，防止 AI 像复读机一样看到敏感词就误报。
- **通道 A (身份判定)**：区分是用户本人表达，还是用户在贴代码/日志/竞品分析。
- **通道 B (风险判定)**：命中安全画像中的触发阈值。
- **场景示例**：
    - *误报排除*：用户粘贴包含“我受够了”字样的报错日志 → **AI 保持沉默**（识别为日志）。
    - *精准干预*：用户说“我真的受够了，今晚必须搞定” → **AI 介入**（识别为本人+风险）。

### 5. 🎭 场景化解释引擎 (Scenario-based Engine)
当您反馈“解释不清楚”时，自动触发重构流程：
- **全场景库**：涵盖生活、工作、学习三大类 50+ 场景。
- **四要素架构**：每个解释包含背景设定、角色代入、决策节点、结果对比。
- **智能匹配**：根据历史行为数据，选择与您关联度最高的场景进行类比。

### 6. 🧠 元认知决策支持体系
- **决策数据库**：记录每次决策的问题类型、路径、结果与复盘。
- **误区识别**：自动检测 10+ 种常见思维误区（如幸存者偏差、沉没成本）。
- **历史检索**：新决策前自动比对相似度 > 80% 的历史案例，避免在同一个坑里摔倒两次。

### 7. 🛠️ 场景化框架自动调用系统
- **决策困境**：自动加载“权衡矩阵”，支持 ≥ 6 个维度权重分配及敏感性分析。
- **风险评估**：调用“5×5 风险矩阵”，集成蒙特卡洛模拟，提供概率分布图。
- **学习复盘**：激活“错误积分系统”（1-10级）与“5Why 根因分析”，追踪至第 3 层深度。

### 8. 🛡️ 专业化问题解决通道
- **情绪专区**：集成 20+ 种心理调节技术，构建情绪-认知关联模型。
- **复杂分析区**：强制使用系统分析、利益相关者分析，调用 SWOT、KT 决策法、TRIZ 等顶级思维模型。

---

## 📈 设计目标 (Design Goals)

| 指标 | 目标值 | 当前状态 |
|------|------|------|
| 场景匹配准确率 | ≥ 90% | 待验证 |
| 决策改进率 (30天) | ≥ 40% | 待验证 |
| 框架调用延迟 (gRPC) | < 50ms | 实时性极佳 ✅ |
| 内存占用 | ~200MB | 轻量化部署 ✅ |

---

## 📂 架构图谱

```text
.
├── core/               # 核心协议层 (OS 核心)
│   ├── SOUL.md         # 仲裁者人格基线与输出风格
│   ├── AGENTS.md       # 意图双通道过滤与三级干预逻辑
│   ├── HEARTBEAT.md    # 主动脉冲任务定义
│   └── IDENTITY.md     # 身份定义：前额叶监护人
├── knowledge/          # 知识层 (认知闭环)
│   ├── methodology.md  # 复杂问题拆解 SOP
│   ├── meta_cognition.md # 认知负荷监测阈值
│   └── cognitive_bias_evidence.md # 循证偏差库
├── memory/             # 进化层 (AI 自我迭代)
│   ├── reflections/    # 晚间反思汇总
│   └── evolution/      # 决策框架进化记录
└── skills/             # 插件层 (guardian-safety-engine)
```

---

## 🚀 核心功能演示

### 🧠 复杂问题拆解
当您面对大难题硬刚时，AI 会自动执行：
> **输入**: "这个项目怎么推进？"
>
> **AI 响应**: "正在调用 `methodology.md`。已拆解为：[定义目标] → [识别障碍] → [排优先级] → [具体行动项]。"

### ⚡ 能量管理与主动干预
当您状态不佳仍强行推进时：
> **输入**: "我今晚必须把这个重构做完。" (时间: 01:00 AM)
>
> **AI 响应 (L3 强制中断)**: "当前时间已进入睡眠红灯期。根据 `USER.md` 的历史记录，此类深夜重构成功率为 0%，且会导致次日严重认知赤字。已暂时停止任务，请立即休息。这是您的历史类似记录 [链接]。"

---

## 🛠️ 快速部署

### A. OpenClaw 原生集成 (推荐)
```bash
# 1. 安装安全引擎
clawhub install guardian-safety-engine

# 2. 克隆本仓库并初始化元认知 OS
git clone https://github.com/maxime-Xian/max-cognitive-shield.git
./scripts/setup.sh
```

### B. 通用 Agent 配置 (Cursor/Claude Code/Devin)
1. 将 `core/` 下的 `.md` 文件移至您的 Agent 工作区根目录。
2. 将 `knowledge/` 文件夹移入工作区。
3. 在 `USER.md` 中配置您的安全画像与风险阈值。

---

## 🤝 贡献与参与

我们正在寻找对 **AI 安全性**、**认知科学** 和 **元认知架构** 感兴趣的贡献者。
- **Discord**: [加入我们的前额叶社区](https://discord.gg/your-link)
- **微信公众号**: 搜索 "MaximeXian"

---

## 📄 许可证

本项目采用 [Apache License 2.0](./LICENSE) 许可证。

> **这不是一堆配置文件，这是一套保护人类理性的防御架构。**
