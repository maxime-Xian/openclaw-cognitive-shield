import json
from datetime import datetime, timedelta

class EvolutionEngine:
    """
    自动总结与进化引擎：量化日报、能力曲线、决策归档、错误闭环
    """
    
    def __init__(self, user_id: str):
        self.user_id = user_id
        self.knowledge_base = "knowledge/error_knowledge_v1.0.0.md"

    def generate_daily_report(self, data: dict):
        """
        场景：每日量化日报 (22:30 自动推送)
        """
        html_template = f"""
        <html>
            <body style='font-family: Inter, sans-serif; background-color: #F5F5F5;'>
                <h2 style='color: #1A2B4C;'>🧠 每日量化日报 - {datetime.now().strftime('%Y-%m-%d')}</h2>
                <ul>
                    <li>🕒 专注时长：{data['focus_hours']}h (环比昨日：{data['focus_growth']})</li>
                    <li>✅ 任务完成率：{data['completion_rate']}%</li>
                    <li>📊 情绪评分：{data['mood_score']}</li>
                    <li>👟 运动步数：{data['steps']}</li>
                </ul>
                <p>🚦 监护人点评：{data['guardian_comment']}</p>
            </body>
        </html>
        """
        return html_template

    def generate_weekly_evolution(self, weekly_data: list):
        """
        场景：每周能力进化曲线 (周日 08:00 生成)
        """
        # 这里模拟雷达图数据，真实环境会调用 matplotlib/plotly
        radar_categories = ["逻辑", "表达", "执行", "学习", "健康", "社交"]
        scores = [8, 7, 9, 8, 6, 7]
        return {
            "type": "RADAR_CHART",
            "categories": radar_categories,
            "scores": scores,
            "status": "800x800 PNG generated"
        }

    def archive_decision(self, decision_data: dict):
        """
        场景：关键决策记录归档 (24小时内自动提取)
        """
        decision_record = {
            "decision_id": f"DEC-{int(datetime.now().timestamp())}",
            "context": decision_data["context"],
            "options": decision_data["options"],
            "rationale": decision_data["rationale"],
            "status": "archived to Notion"
        }
        return decision_record

    def auto_evolve_error(self, error_report: dict):
        """
        场景：错误素材闭环 (5分钟内自动创建 Issue)
        """
        issue_body = f"""
        - 用户ID: {self.user_id}
        - 时间: {datetime.now().isoformat()}
        - 错误原文: {error_report['raw_text']}
        - 上下文日志: {error_report['logs']}
        """
        # 这里会模拟 GitHub API 调用
        return {
            "status": "GitHub Issue created",
            "labels": ["bug", "auto-evolution"],
            "assigned_to": "maxime-Xian"
        }

if __name__ == "__main__":
    evo = EvolutionEngine(user_id="maxime888666")
    report_data = {
        "focus_hours": 6.5,
        "focus_growth": "+12%",
        "completion_rate": 85,
        "mood_score": 7.8,
        "steps": 10240,
        "guardian_comment": "学习强度略高，建议今晚开启‘L3 保护模式’。🌙"
    }
    print("[日报 HTML 预览]:", evo.generate_daily_report(report_data))
