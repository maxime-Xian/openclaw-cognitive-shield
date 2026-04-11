import json
import re

class ComplianceChecker:
    """
    马克西姆揍钢琴 (MaximeXian) 合规审查工具类
    """
    
    def __init__(self):
        # 简单演示敏感词和广告法禁用词
        self.sensitive_words = ["最强", "第一", "国家级", "世界领先", "独家", "极品", "万能", "保本", "100%"]
        self.legal_disclaimer = "© 2026 马克西姆揍钢琴 (MaximeXian). All rights reserved. 遵循 Apache License 2.0 开源协议。"
        self.original_statement = "本文为【马克西姆揍钢琴】原创，未经授权禁止转载。"

    def check_text(self, text: str) -> dict:
        """
        检查文本是否合规
        """
        found_words = [word for word in self.sensitive_words if word in text]
        is_compliant = len(found_words) == 0
        
        return {
            "is_compliant": is_compliant,
            "found_violations": found_words,
            "suggestions": "请替换上述违禁词以符合广告法要求。" if not is_compliant else "符合合规要求。"
        }

    def add_original_footer(self, content: str) -> str:
        """
        为文章添加原创声明与版权页脚
        """
        return f"{content}\n\n---\n{self.original_statement}\n{self.legal_disclaimer}"

if __name__ == "__main__":
    checker = ComplianceChecker()
    test_text = "这是世界上最强的元认知系统，100% 保本收益。"
    result = checker.check_text(test_text)
    print(json.dumps(result, indent=2, ensure_ascii=False))
    
    final_post = checker.add_original_footer("Max-Cognitive-Shield 架构深度解析...")
    print("\n[最终文章示例]:\n", final_post)
