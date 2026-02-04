import requests
import json
from src.app_integration import PersonaService

# 初始化引擎
service = PersonaService()

def chat_with_ollama(user_text, model="llama3"):
    """
    对接本地跑在 Ollama 上的模型 (默认端口 11434)
    """
    # 1. 生成带人格的指令包
    payload = service.get_llm_payload(user_text)
    
    # 2. 构造 Ollama API 格式
    ollama_payload = {
        "model": model,
        "messages": payload["messages"],
        "stream": False
    }
    
    try:
        response = requests.post(
            "http://localhost:11434/api/chat",
            json=ollama_payload
        )
        return response.json()['message']['content']
    except Exception as e:
        return f"❌ 错误: 请确保 Ollama 已在本地运行. ({e})"

if __name__ == "__main__":
    print(f"--- Persona Engine x Ollama (Local) ---")
    user_input = input("你: ")
    reply = chat_with_ollama(user_input)
    print(f"\nAI: {reply}")
