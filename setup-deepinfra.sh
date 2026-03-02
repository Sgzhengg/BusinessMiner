#!/bin/bash

# DeepInfra API 快速配置脚本

set -e

echo "🚀 IdeaForge - DeepInfra 快速配置"
echo "===================================="
echo ""

# 检查是否存在 .env 文件
if [ ! -f .env ]; then
    echo "📝 创建 .env 文件..."
    cp .env.example .env
    echo "✅ .env 文件已创建"
    echo ""
fi

# 提示用户配置 API Key
echo "⚠️  请完成以下步骤："
echo ""
echo "1️⃣  访问 https://deepinfra.com/"
echo "2️⃣  注册或登录账号"
echo "3️⃣  获取 API Key (https://deepinfra.com/account/keys)"
echo "4️⃣  编辑 .env 文件，填入以下内容:"
echo ""
echo "   DEEPINFRA_API_KEY=your_api_key_here"
echo "   DEEPINFRA_MODEL=deepseek-ai/deepseek-r1-distill-llama-70b"
echo ""

# 检查 DEEPINFRA_API_KEY 是否已设置
if grep -q "DEEPINFRA_API_KEY=your_" .env; then
    echo "❌ DEEPINFRA_API_KEY 未配置"
    echo ""
    echo "请按照上述步骤配置后再运行此脚本"
    exit 1
fi

echo "✅ DeepInfra API 已配置"
echo ""
echo "📊 支持的模型列表:"
echo "  • deepseek-ai/deepseek-r1-distill-llama-70b (推荐，成本低)"
echo "  • Qwen/Qwen2.5-72B-Instruct (中文友好)"
echo "  • meta-llama/Llama-3.1-70B-Instruct (通用能力强)"
echo "  • mistralai/Mistral-Large (速度快)"
echo ""
echo "💡 更改模型: 编辑 .env 中的 DEEPINFRA_MODEL 参数"
echo ""

# 询问是否要运行测试
echo "🧪 是否运行 DeepInfra API 测试？(y/n)"
read -r response

if [[ "$response" =~ ^[Yy]$ ]]; then
    echo ""
    echo "运行测试..."
    cd backend
    python test_deepinfra.py
    cd ..
fi

echo ""
echo "✅ 配置完成！"
echo ""
echo "🚀 启动应用:"
echo "   cd backend"
echo "   python main.py"
echo ""
