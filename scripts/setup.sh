#!/bin/bash
# Max-Cognitive-Shield — Interactive Setup Script
# Version: 1.0.0

echo "🧠 Max-Cognitive-Shield 安装向导"
echo "======================================"
echo "这个脚本将引导你初始化个人的元认知操作系统。"

# 1. 收集用户信息
read -p "你的名字/昵称 (AI 将用这个称呼你): " USER_NAME
if [ -z "$USER_NAME" ]; then
    USER_NAME="User"
fi

# 2. 替换模板中的占位符 (针对 core/ 和 knowledge/ 下的所有文件)
echo "正在应用你的个人配置..."

# macOS sed 和 GNU sed 的兼容性处理
if [[ "$OSTYPE" == "darwin"* ]]; then
  SED_ARGS=(-i '')
else
  SED_ARGS=(-i)
fi

# 替换 USER_NAME
find core knowledge -type f -name "*.md" -exec sed "${SED_ARGS[@]}" "s/{USER_NAME}/$USER_NAME/g" {} +
find core knowledge -type f -name "*.md" -exec sed "${SED_ARGS[@]}" "s/{BOT_NAME}/Max-Shield/g" {} +

echo "✅ 配置注入完成。"
echo ""
echo "🚀 部署说明："
echo "1. 如果你使用 OpenClaw，请运行 ./scripts/deploy-openclaw.sh"
echo "2. 如果你使用其他 Agent 工具，请将其指向本目录及下面的 core/ 文件夹"
echo ""
echo "⚠️ 重要：请打开 core/USER.md 手动填充你的【隐私安全画像】和【旧脚本】词库！"
echo "守护伞已为你撑开。保持理性，保护能量。"
