import time
import random
from datetime import datetime, timedelta

class ProactiveReminderEngine:
    """
    主动提醒引擎：集成会议、任务、习惯提醒功能
    """
    
    def __init__(self, user_id: str):
        self.user_id = user_id
        self.notification_channels = ["local", "wechat", "sms"]

    def check_meeting_reminders(self, meetings: list):
        """
        场景：会议前 5 分钟 (300秒)
        """
        current_time = int(time.time())
        reminders = []
        for meeting in meetings:
            if meeting["status"] != "cancelled":
                time_diff = meeting["start_time"] - current_time
                if 290 <= time_diff <= 310:
                    reminders.append({
                        "type": "MEETING",
                        "title": meeting["title"],
                        "link": meeting["link"],
                        "attachments": meeting.get("attachments", []),
                        "message": f"🧠 您的会议‘{meeting['title']}’将在 5 分钟后开始。点击入会：{meeting['link']}"
                    })
        return reminders

    def check_task_deadlines(self, tasks: list):
        """
        场景：任务截止前 24 小时 (86400秒)
        """
        current_time = int(time.time())
        reminders = []
        for task in tasks:
            if task["status"] != "completed" and task["assignee"] == self.user_id:
                time_diff = task["deadline"] - current_time
                if 86300 <= time_diff <= 86500:
                    reminders.append({
                        "type": "TASK",
                        "id": task["id"],
                        "title": task["title"],
                        "message": f"🚦 任务‘{task['title']}’将在 24 小时后截止。需要一键延期吗？⚡",
                        "action": "postpone"
                    })
        return reminders

    def check_habit_reminders(self, habits: list):
        """
        场景：习惯养成打卡时间 (±15分钟随机窗口)
        """
        now = datetime.now()
        reminders = []
        for habit in habits:
            target_time = datetime.strptime(habit["time"], "%H:%M").replace(
                year=now.year, month=now.month, day=now.day
            )
            random_offset = random.randint(-900, 900)
            trigger_time = target_time + timedelta(seconds=random_offset)
            
            if abs((now - trigger_time).total_seconds()) <= 30:
                reminders.append({
                    "type": "HABIT",
                    "habit_name": habit["name"],
                    "message": f"📅 打卡时刻：‘{habit['name']}’。让坚持成为你的操作系统。⚡",
                    "channel": "dual-channel (local+wechat)"
                })
        return reminders

if __name__ == "__main__":
    engine = ProactiveReminderEngine(user_id="maxime888666")
    # 模拟数据
    meetings = [{"title": "元认知架构评审", "start_time": int(time.time()) + 300, "status": "active", "link": "https://zoom.us/j/123"}]
    print("[会议提醒测试]:", engine.check_meeting_reminders(meetings))
