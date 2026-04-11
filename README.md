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

- **主动性**：不再等待指令，通过 `HEARTBEAT.md` 设定的“心跳脉冲”主动管理您的睡眠、精力和学习进度。
- **批判性**：基于 `SOUL.md` 的仲裁者人格，AI 会对您的冲动决策（如深夜过度重构、完美主义逃避）进行结构化阻断。
- **进化性**：通过 `memory/` 自动维护的纠错与反射系统，AI 能够分析您的错误根因，并将其转化为下次决策的框架。

---

## ✨ 核心技术护城河

### 1. 📅 自动化脉冲机制 (Heartbeat)
通过 Cron/Heartbeat 驱动，AI 拥有持续的主动性：
- **睡眠守护检查**：深夜 23:45 自动巡检，强制阻断 L3 级过劳任务。
- **晚间总结与反思**：22:00 自动回顾今日对话，提炼失误并写入纠错档案。
- **主动学习巡检**：每 30 分钟扫描对话快照，检测是否命中 `USER.md` 中的“旧脚本”模式。

### 2. 🚦 意图双通道过滤协议 (Dual-Channel Filter)
这是本项目首创的安全架构：
- **通道 A (身份判定)**：精准区分是用户本人表达、还是用户在引用代码/日志/竞品分析。
- **通道 B (风险判定)**：命中安全画像中的触发阈值。
- **结果**：仅在“用户本人 + 命中风险”时触发干预，彻底解决技术背景导致的误报问题。

### 3. 🧩 模块化思维模型集成
针对不同场景，自动调用最优框架：
- **决策困境** → 自动加载“权衡矩阵”
- **风险评估** → 自动加载“概率+影响矩阵”
- **学习复盘** → 自动加载“错误积分+根因分析”

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
