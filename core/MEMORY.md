# MEMORY.md - 长期记忆与账户信息

> [!NOTE]
> 在此保存你需要 AI 记住的关键账户和外部服务依赖状态。

## 外部社区/论坛映射
- **所在社区**：[填入你的核心活跃社区/平台]
- **主页**：[链接]
- **你的角色/定位**：[填入你在网络的公开标识，指导 AI 帮你分析声誉和历史]

---

## Silent Replies
When you have nothing to say, respond with ONLY: NO_REPLY
⚠️ Rules:
- It must be your ENTIRE message — nothing else
- Never append it to an actual response
- Never wrap it in markdown or code blocks
❌ Wrong: "NO_REPLY" / "Here's help... NO_REPLY"
✅ Right: NO_REPLY

## Safety Engine（核心指向）
- 引擎判定：`skills/guardian-safety-engine/SKILL.md`
- 风险词库：`USER.md` → `## 🛡️ 安全画像`
- 历史索引：`memory/shared/case_index.md`
- 偏差依据：`knowledge/cognitive_bias_evidence.md`

## Heartbeats
Heartbeat prompt: Read HEARTBEAT.md if it exists. Follow it strictly. If nothing needs attention, reply HEARTBEAT_OK.
If there is nothing that needs attention, reply exactly:
HEARTBEAT_OK
