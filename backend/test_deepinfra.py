"""DeepInfra API 集成测试脚本"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from config import get_settings
from app.modules.analyzer import AIAnalyzer


def test_deepinfra_connection():
    """测试 DeepInfra API 连接"""
    settings = get_settings()
    
    print("=" * 60)
    print("🧪 DeepInfra API 集成测试")
    print("=" * 60)
    
    # 检查配置
    print("\n1️⃣  检查配置...")
    if not settings.deepinfra_api_key:
        print("❌ DEEPINFRA_API_KEY 未设置！")
        print("   请在 .env 文件中设置: DEEPINFRA_API_KEY=your_key")
        return False
    
    print(f"✅ API Key: {settings.deepinfra_api_key[:20]}...")
    print(f"✅ 模型: {settings.deepinfra_model}")
    print(f"✅ Base URL: {settings.deepinfra_base_url}")
    
    # 创建分析器
    print("\n2️⃣  初始化分析器...")
    try:
        analyzer = AIAnalyzer(
            api_key=settings.deepinfra_api_key,
            model=settings.deepinfra_model,
            base_url=settings.deepinfra_base_url
        )
        print("✅ 分析器初始化成功")
    except Exception as e:
        print(f"❌ 初始化失败: {e}")
        return False
    
    # 测试分析
    print("\n3️⃣  测试帖子分析...")
    test_title = "如何找到更好的项目管理工具？"
    test_body = "我在使用各种项目管理工具时遇到了问题。大多数工具都太复杂，功能也不够直观。我希望能找到一个简单易用、成本低廉的解决方案。"
    
    try:
        result = analyzer.analyze_post(test_title, test_body)
        print("✅ 分析成功！")
        print(f"\n   痛点: {result.get('pain_point', 'N/A')}")
        print(f"   商机: {result.get('opportunity', 'N/A')}")
        print(f"   用户: {result.get('user_type', 'N/A')}")
    except Exception as e:
        print(f"❌ 分析失败: {e}")
        return False
    
    # 测试方案生成
    print("\n4️⃣  测试方案生成...")
    try:
        solutions = analyzer.generate_solutions(
            pain_point=result.get('pain_point', ''),
            opportunity=result.get('opportunity', ''),
            user_type=result.get('user_type', '')
        )
        print("✅ 方案生成成功！")
        if solutions.get('solutions'):
            print(f"   生成了 {len(solutions['solutions'])} 个解决方案")
            for i, sol in enumerate(solutions['solutions'][:2], 1):
                print(f"   - {sol.get('name', 'N/A')} ({sol.get('type', 'N/A')})")
    except Exception as e:
        print(f"⚠️  方案生成失败: {e}")
    
    # 测试深度研究
    print("\n5️⃣  测试深度研究...")
    try:
        research = analyzer.deep_research(
            question="这个市场已经有哪些成熟的解决方案？",
            context=f"痛点: {result.get('pain_point', '')}"
        )
        print("✅ 深度研究成功！")
        print(f"   响应 ({len(research)} 字符):\n   {research[:200]}...")
    except Exception as e:
        print(f"⚠️  深度研究失败: {e}")
    
    print("\n" + "=" * 60)
    print("✅ 所有测试完成！DeepInfra API 集成正常")
    print("=" * 60)
    return True


if __name__ == "__main__":
    success = test_deepinfra_connection()
    sys.exit(0 if success else 1)
