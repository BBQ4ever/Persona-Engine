import os
from openai import OpenAI
from src.app_integration import PersonaService

# 初始化人格引擎服务
service = PersonaService()

# 初始化 OpenAI 客户端
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY", "your-key-here"))

def chat_with_openai(user_text):
    # 1. 让引擎处理输入，生成带有人格指令的消息包
    payload = service.get_llm_payload(user_text)
    
    # 2. 发送给模型
    print(f"📡 发送请求中（人格强度: {payload['messages'][0]['role']}）...")
    
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=payload["messages"],
        temperature=0.7 # 建议保持在 0.7-0.9 之间以释放采样得到的个性
    )
    
    return response.choices[0].message.content

if __name__ == "__main__":
    print("--- Persona Engine x OpenAI Demo ---")
    user_input = input("你: ")
    reply = chat_with_openai(user_input)
    print(f"\nAI: {reply}")
