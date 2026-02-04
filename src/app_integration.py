import json
import os
import sys

# 将项目路径加入环境
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.l0_orchestrator.engine import PersonaEngine
from src.l1_core.fsm import PersonaFSM, PersonaState
from src.l3_expression.projection import SeededSampler
from src.l3_expression.prompt_augmenter import PromptAugmenter

class PersonaService:
    """
    这是您在业务逻辑中直接调用的服务类。
    """
    def __init__(self, genome_path="src/l2_genome/sample_genome.json"):
        # 1. 初始化内核组件
        with open(genome_path, "r") as f:
            self.genome = json.load(f)
        
        self.fsm = PersonaFSM(persona_id="pioneer_v2", initial_state=PersonaState.STABLE)
        self.engine = PersonaEngine(self.fsm, self.genome)
        self.sampler = SeededSampler()
        self.augmenter = PromptAugmenter()

    def get_llm_payload(self, user_input, session_id="user_123"):
        """
        核心方法：将普通的用户请求，包装成带有“人格指令”的 LLM 请求包。
        """
        # A. 场景分析与降级 (L0)
        constraints = self.engine.get_effective_constraints(user_input)
        
        # B. 这里的逻辑就是执行采样 (L3)
        projection = {}
        for trait in self.genome['loci']:
            val = self.sampler.sample_trait(
                trait, 
                session_id, 
                influence=constraints['influence']
            )
            projection[trait['id']] = val
            
        # C. 将数值投影转化为系统提示词 (Prompt Augmenter)
        status = self.fsm.get_status()
        system_instructions = self.augmenter.augment(
            projection, 
            influence=constraints['influence'], 
            intimacy=status['intimacy_level']
        )
        
        # D. 构造最终发给 LLM 的格式
        llm_payload = {
            "model": "gpt-4", # 或者您选择的任何模型
            "messages": [
                {
                    "role": "system", 
                    "content": f"You are a helpful assistant with the following personality traits:\n{system_instructions}"
                },
                {"role": "user", "content": user_input}
            ]
        }
        
        return llm_payload

# --- 模拟业务调用 ---
if __name__ == "__main__":
    service = PersonaService()
    
    # 场景 1: 正常聊天
    print("\n[SCENARIO: SOCIAL]")
    payload_social = service.get_llm_payload("嘿，你今天心情怎么样？")
    print(json.dumps(payload_social, indent=2, ensure_ascii=False))

    # 场景 2: 技术纠偏
    print("\n[SCENARIO: CRITICAL MATH]")
    payload_math = service.get_llm_payload("计算 123456 的平方根并给出证明过程。")
    print(json.dumps(payload_math, indent=2, ensure_ascii=False))
