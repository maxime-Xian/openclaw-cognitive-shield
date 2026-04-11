# TOOLS.md - 工具与环境变量备忘

> 此文件记录你在 Agent 平台的底层调用配置及可用资源结构。

## AI 模型提供商配置
> (由于不同任务对模型需求不同，可以提示 AI 默认选择哪个)
- **主要模型**：[如：GPT-4o / Claude 3.5 Sonnet / Gemini]
- **降本模型**：[如：GPT-4o-mini / Haiku]，用于摘要等日常操作

## 常用工具与服务API
| 工具名称 | 状态 | 用途 |
|----------|------|------|
| Web Search | ✅ 已配置 | 用于实时新闻获取与核验事实 |
| 飞书/Notion | ⬜ 未配置 | 知识库的双向同步 |
| Telegram/Slack| ⬜ 未配置 | 用于主动向你推送 L2/L3 报警 |

## 工作区结构映射
```
$WORKSPACE/
├── core/
│   └── (SOUL.md / USER.md / IDENTITY.md / AGENTS.md / TOOLS.md ...)
├── knowledge/  (存放通用理论和方法论)
├── memory/     (存放日记、反省与错误库)
└── skills/     (OpenClaw Skills 或其他可插拔动作库)
```
