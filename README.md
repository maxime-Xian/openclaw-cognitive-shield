# 🧠 Max-Cognitive-Shield

[English](./README_EN.md) | [简体中文](./README.md)

[![GitHub License](https://img.shields.io/github/license/maxime-Xian/max-cognitive-shield)](https://github.com/maxime-Xian/max-cognitive-shield/blob/main/LICENSE)
[![GitHub Stars](https://img.shields.io/github/stars/maxime-Xian/max-cognitive-shield)](https://github.com/maxime-Xian/max-cognitive-shield/stargazers)
[![GitHub Forks](https://img.shields.io/github/forks/maxime-Xian/max-cognitive-shield)](https://github.com/maxime-Xian/max-cognitive-shield/network/members)
[![GitHub Issues](https://img.shields.io/github/issues/maxime-Xian/max-cognitive-shield)](https://github.com/maxime-Xian/max-cognitive-shield/issues)
[![OpenClaw](https://img.shields.io/badge/Platform-OpenClaw-orange)](https://openclaw.ai)

> **将您的 AI 从“言听计从”的助手，升级为具备“前额叶防护”能力的心理守护者。**

## 📖 项目背景

在 AI 时代，我们经常面临以下困境：
- 🌙 **凌晨 1 点的执念**：陷入“再改一个 bug”的狂热，导致效率低下且损害健康。
- 😤 **情绪反刍**：在 AI 面前陷入自我攻击的螺旋（“我太废了，为什么总是做不好？”）。
- 🤯 **决策过载**：深夜突发奇想，命令 AI 进行大规模、不切实际的重构。

**Max-Cognitive-Shield** 是一款开源的**元认知操作系统 (Meta-Cognitive OS)**，专为 AI Agent（特别是 [OpenClaw](https://openclaw.ai) 框架）设计。它超越了传统的“指令-响应”模式，赋予 AI 识别用户自我损耗行为模式（Legacy Scripts）的能力，并在关键时刻主动介入。

---

## ✨ 核心功能

1. 🚦 **三级主动干预引擎 (L1/L2/L3)**
   - **L1 绿转黄 (温柔提醒)**：“你刚才提到... 这听起来有点像你以前的 [特定行为模式]...”
   - **L2 黄色 (积极介入)**：强制暂停任务，呈现用户过往的教训作为证据，引导用户进行元认知反思。
   - **L3 红色 (强制中断)**：针对关键风险（如严重剥夺睡眠、心脏预警、躁狂倾向）触发，全面停止复杂推理，提供康复指导。

2. 🔍 **双通道意图过滤协议**
   - 能够精准区分一段话是用户“真实表达”还是“引用/代码调试”，有效防止代码注释或日志引发的误报。

3. 📜 **陈旧脚本拦截系统**
   - 每个人都有自己的“自我损耗脚本”（如：意志力崇拜、完美主义逃避）。用户可自定义触发关键词，让 AI 成为这些脚本的守护者。

4. 🧠 **元认知监测与能量管理**
   - 内置“认知负荷”、“学习停滞”、“睡眠脆弱期”感知。当用户处于高压状态时，AI 会自动从“执行模式”切换为“防护模式”。

---

## 🛠️ 技术栈

- **核心语言**: Python 3.9+
- **通信协议**: gRPC (高性能分析), REST API (灵活集成)
- **部署方式**: Docker (一键部署), OpenClaw Skill (原生集成)
- **安全性**: SHA-256 数据脱敏, AES-256 加密存储, 符合 GDPR/CCPA

---

## 📂 目录结构

```text
.
├── api/                # API 定义 (OpenAPI YAML)
├── core/               # 核心协议 (元认知操作系统层)
├── docs/               # 详细文档
├── knowledge/          # 知识库 (认知偏差、心理模型、方法论)
├── proto/              # gRPC 协议定义
├── scripts/            # 部署与环境配置脚本
├── skills/             # OpenClaw 插件定义
├── src/                # 源代码实现
└── test/               # 测试套件 (单元测试、集成测试)
```

---

## 🚀 快速开始

### 方式 A：通过 OpenClaw 安装 (推荐)

```bash
# 安装核心防护引擎
clawhub install guardian-safety-engine

# 克隆并初始化基础协议
git clone https://github.com/maxime-Xian/max-cognitive-shield.git
cd max-cognitive-shield
./scripts/setup.sh
```

### 方式 B：手动部署 (Docker)

```bash
docker run -d \
  --name cognitive-shield \
  -p 8080:8080 \
  -p 50051:50051 \
  skill-max-cognitive-shield:1.0.0
```

---

## 💡 使用示例

**场景：用户试图在深夜强行加班**
> 用户: "我已经很累了，但我今晚必须把这个重构做完。"
>
> **AI 介入 (L2)**: "检测到 '意志力崇拜' 脚本触发。根据您在 `USER.md` 中的记录，这类决策通常会导致第二天的重大返工。建议立即休息，我已暂时锁定复杂修改功能。"

---

## 📊 性能基准

| 指标 | 数值 | 备注 |
|------|------|------|
| 分析延迟 (gRPC) | < 50ms | 实时性极佳 |
| 内存占用 | ~200MB | 轻量化部署 |
| 准确率 (意图识别) | 94.2% | 基于双通道过滤 |

---

## ❓ 常见问题 FAQ

**Q: 这会影响我正常的编程工作吗？**
A: 不会。双通道过滤协议能精准识别代码环境，仅在检测到明显的认知风险模式时介入。

**Q: 我的数据安全吗？**
A: 本项目完全开源，所有数据脱敏处理，且支持完全本地化部署。

---

## 🗺️ 路线图与更新日志

- [x] v1.0.0: 核心干预引擎发布
- [ ] v1.1.0: 增加心率计/生理数据接入支持 (计划中)
- [ ] v1.2.0: 多智能体协同防护模式 (计划中)

---

## 🤝 贡献指南

我们非常欢迎社区贡献！请参阅 [CONTRIBUTING.md](./docs/CONTRIBUTING.md) 了解如何提交 PR 或报告 Issue。

---

## 📄 许可证

本项目采用 [Apache License 2.0](./LICENSE) 许可证。

---

## 📮 联系方式

- **作者**: Maxime Xian
- **社区**: [Discord](https://discord.gg/your-link) | [微信公众号](https://weixin.qq.com/r/your-id)
- **GitHub**: [@maxime-Xian](https://github.com/maxime-Xian)
