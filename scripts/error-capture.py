import json
import os
from datetime import datetime

# 定义路径
EVOLUTION_DIR = "memory/evolution"
ERROR_LOG = os.path.join(EVOLUTION_DIR, "error_logs.jsonl")

def capture_error(error_msg, context=""):
    """
    错误自动记录：捕捉报错或负面反馈，存入本地日志
    """
    entry = {
        "timestamp": datetime.now().isoformat(),
        "error": error_msg,
        "context": context,
        "status": "pending_analysis"
    }

    if not os.path.exists(EVOLUTION_DIR):
        os.makedirs(EVOLUTION_DIR)

    with open(ERROR_LOG, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")

    print(f"[ErrorCapture] Error recorded: {error_msg}")

if __name__ == "__main__":
    # 模拟捕获到一个错误
    capture_error("用户反馈：AI 响应太慢，且没有给出具体的权衡矩阵分析。", context="Session-12345")
