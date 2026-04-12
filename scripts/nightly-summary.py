import json
import os
from datetime import datetime

# 定义路径
REFLECTIONS_DIR = "memory/reflections"
DAILY_LOGS_DIR = "memory/daily"

def generate_nightly_summary():
    """
    晚间总结：回顾当日对话，提炼失误并写入纠错档案
    """
    today = datetime.now().strftime("%Y-%m-%d")
    log_file = os.path.join(DAILY_LOGS_DIR, f"{today}.md")
    summary_file = os.path.join(REFLECTIONS_DIR, f"summary_{today}.md")

    print(f"[NightlySummary] Processing logs for {today}...")

    # 模拟从日志提炼总结
    summary_content = f"""# 晚间反思汇总 - {today}

## 今日关键决策
- [模拟] 决定推迟大规模重构，优先修复紧急 Bug。

## 认知模式识别
- 命中模式：OS-002 (逃避行为 - 试图通过美化 UI 逃避核心逻辑开发)。

## 改进建议
- 下次遇到此类情况，先执行 `methodology.md` 中的障碍识别流程。
"""

    if not os.path.exists(REFLECTIONS_DIR):
        os.makedirs(REFLECTIONS_DIR)

    with open(summary_file, "w", encoding="utf-8") as f:
        f.write(summary_content)

    print(f"[NightlySummary] Summary saved to {summary_file}")

if __name__ == "__main__":
    generate_nightly_summary()
