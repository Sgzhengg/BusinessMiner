"""AI 分析模块 - 识别痛点和商机"""
import json
import logging
from typing import Dict, Any
from openai import OpenAI
from config import get_settings

logger = logging.getLogger(__name__)


class AIAnalyzer:
    """使用 DeepInfra API 进行文本分析"""
    
    def __init__(self, api_key: str, model: str, base_url: str = "https://api.deepinfra.com/openai/v1"):
        self.client = OpenAI(api_key=api_key, base_url=base_url)
        self.model = model
    
    def analyze_post(self, title: str, body: str) -> Dict[str, Any]:
        """
        分析 Reddit 帖子，提取痛点和商机
        
        Args:
            title: 帖子标题
            body: 帖子内容
        
        Returns:
            包含 pain_point, opportunity 的字典
        """
        text = f"标题: {title}\n\n内容: {body}"
        
        prompt = f"""
你是一位资深产品经理和商业分析师。请从以下Reddit帖子中提取关键信息：

1. **主要痛点**: 用户抱怨或提到的问题是什么？
2. **商机信号**: 这代表了什么样的市场需求或商机？
3. **潜在用户类型**: 这个痛点主要影响哪类用户？

帖子内容：
{text}

请直接返回JSON格式（无需markdown标记），包含以下字段：
{{
  "pain_point": "用户遇到的主要痛点",
  "opportunity": "对应的商机描述",
  "user_type": "目标用户类型"
}}
"""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "你是一个专业的商业分析师。返回有效的JSON。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=500
            )
            
            content = response.choices[0].message.content.strip()
            # 清理可能的 markdown 标记
            if content.startswith("```"):
                content = content.split("```")[1]
                if content.startswith("json"):
                    content = content[4:]
            content = content.strip()
            
            result = json.loads(content)
            logger.info(f"分析成功: {result.get('pain_point', '')[:50]}...")
            return result
        except json.JSONDecodeError as e:
            logger.error(f"JSON 解析失败: {str(e)}, 响应: {content[:200]}")
            return {
                "pain_point": "解析失败",
                "opportunity": "请手动检查",
                "user_type": "未知"
            }
        except Exception as e:
            logger.error(f"AI 分析失败: {str(e)}")
            return {
                "pain_point": f"分析错误: {str(e)}",
                "opportunity": "",
                "user_type": ""
            }
    
    def generate_solutions(self, pain_point: str, opportunity: str, user_type: str) -> Dict[str, Any]:
        """
        基于痛点生成解决方案建议
        
        Returns:
            包含 solutions, action_steps 的字典
        """
        prompt = f"""
基于以下业务痛点，提出可执行的解决方案建议：

痛点: {pain_point}
商机: {opportunity}
用户: {user_type}

请返回JSON格式，包含：
{{
  "solutions": [
    {{"type": "工具类/服务类/内容类", "name": "解决方案名称", "description": "描述"}}
  ],
  "action_steps": ["第一步", "第二步", "第三步"],
  "success_metrics": ["指标1", "指标2"]
}}
"""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=800
            )
            
            content = response.choices[0].message.content.strip()
            if content.startswith("```"):
                content = content.split("```")[1]
                if content.startswith("json"):
                    content = content[4:]
            content = content.strip()
            
            return json.loads(content)
        except Exception as e:
            logger.error(f"生成解决方案失败: {str(e)}")
            return {"solutions": [], "action_steps": [], "success_metrics": []}
    
    def deep_research(self, question: str, context: str) -> str:
        """
        进行深度研究 - 多轮对话的 AI 助手
        
        Args:
            question: 用户的追问
            context: 已有的研究上下文
        
        Returns:
            研究结果文本
        """
        prompt = f"""
你是一位商业研究分析师。用户基于以下背景信息提出了一个问题。

背景: {context}

用户问题: {question}

请提供专业、可操作的回答。
"""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.8,
                max_tokens=1000
            )
            
            return response.choices[0].message.content.strip()
        except Exception as e:
            logger.error(f"深度研究失败: {str(e)}")
            return "分析过程中出错，请稍后重试。"
