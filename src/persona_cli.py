import sys
from src.app_integration import PersonaService

def main():
    """
    这是一个极客工具。
    用法: python3 persona_cli.py "你好" | some_llm_tool
    它只输出生成的 System Prompt 指令内容。
    """
    if len(sys.argv) < 2:
        print("用法: python3 persona_cli.py <user_input>")
        return

    user_input = sys.argv[1]
    service = PersonaService()
    
    # 提取指令
    payload = service.get_llm_payload(user_input)
    system_instruction = payload["messages"][0]["content"]
    
    # 将调试信息输出到 stderr，确保 stdout 只有指令
    sys.stderr.write(f"--- Persona Engine CLI ---\n")
    sys.stderr.write(f"Input: {user_input}\n")
    
    # 核心输出
    print(system_instruction)

if __name__ == "__main__":
    main()
