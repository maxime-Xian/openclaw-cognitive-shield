#!/bin/bash
# Max-Cognitive-Shield — OpenClaw Deployment Script

# 默认 OpenClaw 工作区路径
WORKSPACE="${OPENCLAW_WORKSPACE:-$HOME/.openclaw/workspace}"

echo "开始向 OpenClaw 部署 Max-Cognitive-Shield..."
echo "目标工作区: $WORKSPACE"

if [ ! -d "$WORKSPACE" ]; then
    echo "❌ 错误: 找不到 OpenClaw 工作区目录 ($WORKSPACE)。请确认 OpenClaw 已正确安装。"
    exit 1
fi

# 创建必要的目录结构
mkdir -p "$WORKSPACE/knowledge"
mkdir -p "$WORKSPACE/skills/guardian-safety-engine"
mkdir -p "$WORKSPACE/memory/guardian/reflections"
mkdir -p "$WORKSPACE/memory/guardian/evolution"
mkdir -p "$WORKSPACE/memory/guardian/error-correction"
mkdir -p "$WORKSPACE/memory/guardian/operational"
mkdir -p "$WORKSPACE/memory/shared"
mkdir -p "$WORKSPACE/memory/episodes"
mkdir -p "$WORKSPACE/memory/daily"

# 部署核心层 (直接放到工作区根目录)
echo "部署 Core 层 (AGENTS, HEARTBEAT, IDENTITY, MEMORY, SOUL, TOOLS, USER)..."
cp core/*.md "$WORKSPACE/"

# 部署知识层
echo "部署 Knowledge 层..."
cp knowledge/*.md "$WORKSPACE/knowledge/"

# 部署安全引擎 Skill
echo "部署 Guardian Safety Engine Skill..."
cp skills/guardian-safety-engine/SKILL.md "$WORKSPACE/skills/guardian-safety-engine/"

echo "✅ 部署完成！"
echo "你的 OpenClaw Agent 现在具备了三级主动干预和双通道意图过滤能力。"
echo "请记得配置并执行心跳脚本以激活被动巡检功能。"
