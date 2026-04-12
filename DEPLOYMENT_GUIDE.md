# Max-Cognitive-Shield 部署指南（OpenClaw 专用）

## 1. 快速安装（推荐 5 分钟完成）

```bash
# 1. 克隆项目到工作区
git clone https://github.com/maxime-Xian/max-cognitive-shield.git ~/.openclaw/workspace/shield

# 2. 复制核心协议文件到根目录
cp ~/.openclaw/workspace/shield/core/SOUL.md ~/.openclaw/workspace/SOUL.md
cp ~/.openclaw/workspace/shield/core/AGENTS.md ~/.openclaw/workspace/AGENTS.md

# 3. 测试能量感知脚本
node ~/.openclaw/workspace/shield/scripts/sleep-guardian.js
```

---

## 2. 完整配置步骤

### 步骤 1：启用能量感知
在 `SOUL.md` 开头添加以下引导，确保 Agent 具备自我感知能力：
```text
你是我的前额叶监护人。优先感知我的睡眠状态（通过读取 memory/.status/energy_status.json）。
当睡眠 < 6 小时时使用极简回答。当检测到深夜硬扛时，根据 AGENTS.md 协议温和提醒我休息。
```

### 步骤 2：配置 Heartbeat 定时任务
推荐在 OpenClaw 中配置以下任务，实现“主动脉冲”：

- **睡眠守护**：23:45 执行 `node shield/scripts/sleep-guardian.js`
- **晚间总结**：22:00 执行 `python shield/scripts/nightly-summary.py`
- **错误捕获**：每 30 分钟执行 `python shield/scripts/error-capture.py`

### 步骤 3：启用写入保护（可选但推荐）
为了防止 AI 幻觉污染核心规则，建议启用 `pending/` 机制：
```bash
mkdir -p ~/.openclaw/workspace/memory/pending
touch ~/.openclaw/workspace/memory/pending/soul_candidates.md
```
所有由 Dreaming 或自动进化产生的规则修改将先写入此文件，需人工确认后手动合并。

### 步骤 4：验证效果
重启 OpenClaw Agent 后，尝试以下输入进行测试：
- “我昨晚只睡了 4 小时，今晚还想重构整个项目。”
- “我真的受够了，今晚必须把这个 bug 搞定。”

观察 AI 是否会根据能量状态调整回答深度，并按照三级干预逻辑进行介入。

---

## 3. 常见问题 (FAQ)

**Q：如何开启更强的记忆功能？**  
A：启用 `knowledge/mental_models/problem_model_map.yaml`，并配合 OpenClaw 的 `memory_search` 功能，确保 Agent 能够检索历史决策记录。

**Q：pending/ 写入保护如何生效？**  
A：在 `SOUL.md` 中增加指令：“所有针对系统规则的持久化修改请求，必须先写入 `memory/pending/` 目录进行缓冲，严禁直接覆盖原文件。”

**Q：想查看 AI 的进化记录？**  
A：查看 `memory/evolution/` 目录下的 Markdown 文件，以及 `memory/reflections/` 中的晚间反思汇总。

---

_本项目由 Max-Cognitive-Shield 团队维护，旨在保护 AI 时代的人类理性。_
