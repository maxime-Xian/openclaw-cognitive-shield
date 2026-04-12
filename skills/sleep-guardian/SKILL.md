# Sleep Guardian Skill

## 描述
实时感知用户的睡眠与能量状态，为 Agent 提供响应深度调节的依据。

## 核心逻辑
1. 定时运行 `scripts/sleep-guardian.js`。
2. 将结果写入 `memory/.status/energy_status.json`。
3. Agent 在 `SOUL.md` 引导下读取该文件。

## 状态定义
- **NORMAL**: 睡眠 ≥ 7h，全速运行。
- **SUBOPTIMAL**: 睡眠 5-7h，精简回答。
- **LOW**: 睡眠 < 5h，强制简洁 + 休息提醒。
