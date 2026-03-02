#!/bin/bash

# IdeaForge 启动脚本

set -e

echo "🚀 IdeaForge 启动"
echo "==============="

# 检查环境变量文件
if [ ! -f .env ]; then
    echo "⚠️  .env 文件不存在，复制 .env.example"
    cp .env.example .env
    echo "✓ 已创建 .env 文件，请编辑后运行此脚本"
    exit 1
fi

# 检查 Python 版本
if ! command -v python3 &> /dev/null; then
    echo "❌ 未找到 Python 3，请先安装 Python 3.9+"
    exit 1
fi

echo "✓ Python 版本检查通过"

# 安装依赖
echo "📦 安装依赖..."
cd backend
pip install -r requirements.txt
cd ..

echo "✓ 依赖安装完成"

# 初始化数据库
echo "🗄️  初始化数据库..."
cd backend
python init_db.py
cd ..

echo "✓ 数据库初始化完成"

# 启动应用
echo "🎯 启动 IdeaForge..."
cd backend
python main.py
