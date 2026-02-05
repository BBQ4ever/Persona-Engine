import json
import os
import sys

from src.utils.paths import resolve_resource

from src.l0_orchestrator.engine import PersonaEngine
from src.l1_core.fsm import PersonaFSM, PersonaState
from src.l3_expression.projection import SeededSampler
from src.l3_expression.prompt_augmenter import PromptAugmenter
from src.l2_genome.archetypes import ArchetypeManager
from src.l0_orchestrator.persistence import SnapshotManager
from src.l3_expression.memory_bridge import MemorySalienceBridge
from src.l4_memory.journal import PersonaReflectionJournal

class PersonaService:
    def __init__(self, genome_path=None, persona_id="pioneer_v2", use_kernel=False):
        # 1. 初始化内核组件
        if genome_path is None:
            genome_path = resolve_resource("src/l2_genome/sample_genome.json")
            
        with open(genome_path, "r") as f:
            self.genome = json.load(f)
        
        if use_kernel:
            from src.kernel_integration import PersonaKernel
            self.kernel = PersonaKernel()
        else:
            self.kernel = None
        self.fsm = PersonaFSM(persona_id=persona_id, initial_state=PersonaState.STABLE)
        self.engine = PersonaEngine(self.fsm, self.genome)
        self.sampler = SeededSampler()
        self.augmenter = PromptAugmenter()
        self.archetype_mgr = ArchetypeManager(self.genome)
        self.persistence = SnapshotManager()
        self.memory_bridge = MemorySalienceBridge(self.fsm)
        self.journal = PersonaReflectionJournal()
        
        from src.l4_memory.short_term import ShortTermMemory
        self.stm = ShortTermMemory(max_entries=10)
        
        from src.l2_genome.habits import HabitGenerator
        self.habit_gen = HabitGenerator()
        
        # Sprint 2: Cognitive Pipeline
        from src.l0_orchestrator.pipeline import CognitiveDirector
        self.director = CognitiveDirector(self)

    def get_memory_filters(self):
        """
        Returns filters for downstream Vector DB retrieval.
        """
        return self.memory_bridge.get_retrieval_filters()

    def save_state(self, label="auto"):
        return self.persistence.save_snapshot(self, label)

    def load_state(self, filepath=None):
        if filepath:
            return self.persistence.load_snapshot(self, filepath)
        return self.persistence.load_latest_snapshot(self)

    def set_stance(self, rigor=0.5, warmth=0.5, chaos=0.3, preset_name=None):
        """
        Set the persona's stance using RWC vectors or a preset name.
        """
        if preset_name:
            stance = self.archetype_mgr.get_preset_stance(preset_name)
            rigor, warmth, chaos = stance['rigor'], stance['warmth'], stance['chaos']
            sys.stderr.write(f"🎭 Loading Preset Stance: {preset_name}\n")

        # A. Calculate Genome from Stance
        self.genome = self.archetype_mgr.calculate_genome_from_stance(rigor, warmth, chaos)
        self.engine.genome = self.genome 
        
        # B. Sync Affective Baseline
        bl = self.archetype_mgr.get_affect_baseline(rigor, warmth, chaos)
        self.fsm.affect.set_baseline(p=bl['p'], a=bl['a'], d=bl['d'])
            
        sys.stderr.write(f"🌊 Stance Adjusted -> Rigor: {rigor}, Warmth: {warmth}, Chaos: {chaos}\n")

    def get_llm_payload(self, user_input, session_id="user_123", override_influence=None, manual_seed=None):
        """
        核心方法：将普通的用户请求，包装成带有“人格指令”的 LLM 请求包。
        Sprint 2: Now orchestrates via the CognitiveDirector.
        """
        # A. 执行 Pipeline Cycle
        context = self.director.run_cycle(user_input, session_id=session_id, manual_seed=manual_seed)
        
        # B. 返回生成的 Artifact
        return context.artifact

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
