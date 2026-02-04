import os
import json
from openai import OpenAI  # 示例使用 OpenAI，其他模型同理
from src.app_integration import PersonaService

# 1. 初始化你的“人格服务”
# 它会自动加载 L2 基因，并准备好 L0-L1-L3 的全套逻辑
persona_service = PersonaService()

# 2. 如果你有 API KEY，可以填在这里（现在只是演示逻辑）
client = OpenAI(api_key="YOUR_OPENAI_API_KEY")

def chat_with_persona(user_input):
    print(f"\n--- [新消息: {user_input}] ---")
    
    # 【核心步骤 A】：让 Persona Engine 计算当前的“状态”和“指令”
    # 它会做场景分析（L0）、亲密度检查（L1）、随机采样（L3）
    # 最后返回一个标准化的 LLM 请求包
    payload = persona_service.get_llm_payload(user_input, session_id="user_unique_id")
    
    # 查看生成的 System Prompt（看看 Engine 为 AI 画好的“精神蓝图”）
    system_prompt = payload["messages"][0]["content"]
    print(f"🎭 [Persona Engine 指令]:\n{system_prompt}")

    # 【核心步骤 B】：正式发送给 AI
    # 注意：这里的 'messages' 已经包含了 Engine 注入的人格指令
    # response = client.chat.completions.create(
    #     model="gpt-4",
    #     messages=payload["messages"]
    # )
    # return response.choices[0].message.content
    
    print("\n🚀 [状态]: 系统已将上述指令注入 System Role，AI 将以此性格回复。")

if __name__ == "__main__":
    # 测试 1: 闲聊（你会看到充满个性的指令）
    chat_with_persona("嘿！你今天过得怎么样？")
    
    # 测试 2: 数学（你会看到指令瞬间变得极其专业且克制）
    chat_with_persona("计算 1024 的三次方，并告诉我原理。")
