import unittest
import time
from assets.scripts.reminders.engine import ProactiveReminderEngine

class TestReminderEngine(unittest.TestCase):
    def setUp(self):
        self.engine = ProactiveReminderEngine(user_id="test_user")

    def test_meeting_reminder_timing(self):
        # 模拟会议前 5 分钟 (300秒)
        meetings = [{"title": "测试会议", "start_time": int(time.time()) + 300, "status": "active", "link": "https://test.link"}]
        reminders = self.engine.check_meeting_reminders(meetings)
        self.assertEqual(len(reminders), 1)
        self.assertIn("测试会议", reminders[0]["title"])

    def test_task_deadline_timing(self):
        # 模拟任务截止前 24 小时 (86400秒)
        tasks = [{"id": "T1", "title": "测试任务", "deadline": int(time.time()) + 86400, "status": "active", "assignee": "test_user"}]
        reminders = self.engine.check_task_deadlines(tasks)
        self.assertEqual(len(reminders), 1)
        self.assertEqual(reminders[0]["action"], "postpone")

if __name__ == "__main__":
    unittest.main()
