#!/bin/bash

# Docker Compose 启动脚本

set -e

echo "🚀 IdeaForge Docker 启动"
echo "========================"

# 检查环境变量文件
if [ ! -f .env ]; then
    echo "⚠️  .env 文件不存在，请先复制 .env.example 并填入必要的 API Key"
    cp .env.example .env
    echo "✓ 已创建 .env 示例文件"
    echo ""
    echo "📝 请编辑 .env 文件，填入以下信息："
    echo "  - REDDIT_CLIENT_ID: 从 https://www.reddit.com/prefs/apps 获取"
    echo "  - REDDIT_SECRET: Reddit API Secret"
    echo "  - OPENAI_API_KEY: 从 https://platform.openai.com/api-keys 获取"
    echo ""
    echo "完成后再次执行: ./run-docker.sh"
    exit 1
fi

# 启动 Docker Compose
echo "📦 启动所有服务..."
docker-compose up -d

echo ""
echo "✓ 容器启动完成！"
echo ""
echo "📍 服务地址："
echo "  - API: http://localhost:8000"
echo "  - API 文档: http://localhost:8000/docs"
echo "  - 前端: http://localhost:8000"
echo "  - PostgreSQL: localhost:5432"
echo "  - Redis: localhost:6379"
echo ""
echo "📊 查看日志: docker-compose logs -f backend"
echo "⛔ 停止服务: docker-compose down"
