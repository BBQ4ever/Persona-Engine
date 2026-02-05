from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
import uuid
import time
import sys
from src.utils.paths import resolve_resource
sys.path.append(str(resolve_resource("gecce_kernel_pkg")))

@dataclass
class PipelineContext:
    """
    Request-scoped execution + audit container.
    Captures the total state of a single 'Cognitive Cycle'.
    """
    trace_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    session_id: str = "default"
    user_input: str = ""
    manual_seed: Optional[int] = None
    
    # Intermediate state
    scene: str = "UNKNOWN"
    constraints: Dict[str, Any] = field(default_factory=dict)
    persona_snapshot: Dict[str, Any] = field(default_factory=dict)
    
    # Outputs
    artifact: Dict[str, Any] = field(default_factory=dict)
    reason_codes: List[str] = field(default_factory=list)
    
    # Audit trail
    event_refs: List[str] = field(default_factory=list) # IDs of emitted events
    start_time: float = field(default_factory=time.time)

class PipelineStep:
    """
    Abstract Base Class for Cognitive Pipeline Steps.
    """
    def __init__(self, name: str):
        self.name = name

    def execute(self, context: PipelineContext, bus=None) -> None:
        """
        Executes the logic for this step, updating the context in-place.
        """
        raise NotImplementedError("Steps must implement execute()")

    def notify(self, bus, event_type, data, context: PipelineContext):
        """
        Helper to emit events and track them in the context.
        """
        if bus:
            from gecce_kernel.core.types import Event
            event = Event(
                event_type=event_type,
                source=self.name,
                data=data,
                metadata={"trace_id": context.trace_id}
            )
            bus.publish(event)
            context.event_refs.append(event.event_id)

class ScenarioAnalysisStep(PipelineStep):
    def __init__(self, engine):
        super().__init__("L0_ScenarioAnalysis")
        self.engine = engine

    def execute(self, context: PipelineContext, bus=None) -> None:
        from gecce_kernel.core.types import EventType
        from src import config
        
        scene = self.engine.analyze_scenario(context.user_input)
        context.scene = scene
        context.reason_codes.append(f"SCENE_{scene}")
        
        # Determine base influence
        if scene == "STRICT_FACT":
            context.constraints['influence'] = 0.1
            context.constraints['mode'] = "STYLE_ONLY"
            context.constraints['recommended_stance'] = config.FACTUAL_STANCE
            context.reason_codes.append("INFLUENCE_DEGRADED_FACTUAL")
        elif scene == "SOCIAL_SUPPORT":
            context.constraints['influence'] = self.engine.influence_level
            context.constraints['mode'] = "FULL_PERSONA"
            context.constraints['recommended_stance'] = config.SUPPORTIVE_STANCE
            context.reason_codes.append("INFLUENCE_FULL_SUPPORT")
        else:
            context.constraints['influence'] = self.engine.influence_level
            context.constraints['mode'] = "FULL_PERSONA"
            context.constraints['recommended_stance'] = None
            context.reason_codes.append("INFLUENCE_FULL_CREATIVE")

        self.notify(bus, EventType.SCENE_ANALYZED, {
            "scene": context.scene,
            "mode": context.constraints['mode']
        }, context)

class FSMEvaluationStep(PipelineStep):
    def __init__(self, fsm):
        super().__init__("L1_FSMEvaluation")
        self.fsm = fsm

    def execute(self, context: PipelineContext, bus=None) -> None:
        from gecce_kernel.core.types import EventType
        
        # Pulse affect based on scene
        if context.scene == "SOCIAL_SUPPORT":
            self.fsm.affect.update(delta_p=0.2, delta_a=0.1)
        elif context.scene == "SOCIAL_CREATIVE":
            self.fsm.affect.update(delta_p=0.05, delta_a=0.02)
        
        from src.l1_core.fsm import PersonaState
        self.fsm.affect.decay(is_locked=(self.fsm.state == PersonaState.LOCKED))
        
        status = self.fsm.get_status()
        context.persona_snapshot['state'] = status['state']
        context.persona_snapshot['affect'] = status['affect']
        context.reason_codes.append(f"FSM_STATE_{status['state']}")
        
        self.notify(bus, EventType.PERSONA_STATE_CHANGED, {
            "state": status['state'],
            "affect": status['affect']
        }, context)

class ValidationStep(PipelineStep):
    def __init__(self, engine):
        super().__init__("L2_Validation")
        self.engine = engine

    def execute(self, context: PipelineContext, bus=None) -> None:
        from gecce_kernel.core.types import EventType
        
        # Phase 11 Drift Check
        correction = self.engine.check_drift()
        if correction:
            context.constraints['governance_override'] = correction
            context.reason_codes.append("DRIFT_DETECTED_CORRECTION_APPLIED")
        else:
            context.reason_codes.append("GOVERNANCE_PASS")
            
        self.notify(bus, EventType.DRIFT_CHECKED, {
            "correction": correction,
            "has_drift": bool(correction)
        }, context)

class ProjectionStep(PipelineStep):
    def __init__(self, service):
        super().__init__("L3_Projection")
        self.service = service

    def execute(self, context: PipelineContext, bus=None) -> None:
        from gecce_kernel.core.types import EventType
        
        # 1. Update stance if recommended
        rec_stance = context.constraints.get('recommended_stance')
        if rec_stance:
            self.service.set_stance(
                rigor=rec_stance['rigor'], 
                warmth=rec_stance['warmth'], 
                chaos=rec_stance['chaos']
            )
            context.reason_codes.append("STANCE_AUTO_ADJUSTED")
        
        # 2. Sample Traits
        projection = {}
        influence = context.constraints['influence']
        affect_warp = self.service.fsm.affect.get_warp_factors()
        
        for trait in self.service.genome['loci']:
            val = self.service.sampler.sample_trait(
                trait, 
                context.session_id, 
                influence=influence,
                affect_warp=affect_warp,
                manual_seed=context.manual_seed
            )
            projection[trait['id']] = val
            
        # 3. Augment Prompt
        intimacy = self.service.fsm.get_status()['intimacy_level']
        system_instructions = self.service.augmenter.augment(
            projection, 
            influence=influence, 
            intimacy=intimacy
        )
        context.reason_codes.append("PROMPT_AUGMENTED")
        
        # 4. Hybrid Profile Generation (Sprint 3)
        habits = self.service.habit_gen.generate(context.session_id)
        habit_text = "\n".join([f"- {h['text']}" for h in habits])
        
        # 5. Apply Governance Directive if any
        governance_directive = ""
        if context.constraints.get('governance_override'):
            governance_directive = f"\n[GOVERNANCE OVERRIDE]\n{context.constraints['governance_override']}\n"
            
        final_prompt = (
            f"You are operating under personality constraints:\n{system_instructions}\n\n"
            f"[BEHAVIORAL HABITS (PROVENANCE: GENERATED)]\n{habit_text}"
            f"{governance_directive}"
        )
        
        context.artifact = {
            "model": "persona_v1",
            "messages": [
                {"role": "system", "content": final_prompt},
                {"role": "user", "content": context.user_input}
            ],
            "metadata": {
                "trace_id": context.trace_id,
                "session_id": context.session_id,
                "contract_version": "1.0.0",
                "stance": rec_stance or {"rigor": 0.5, "warmth": 0.5, "chaos": 0.5},
                "affect": context.persona_snapshot.get('affect'),
                "reason_codes": context.reason_codes,
                "mode": context.constraints['mode']
            }
        }
        
        self.notify(bus, EventType.TRAITS_SAMPLED, {"projection": projection}, context)
        self.notify(bus, EventType.ARTIFACT_READY, {"metadata": context.artifact['metadata']}, context)

class MemoryRefinementStep(PipelineStep):
    def __init__(self, service):
        super().__init__("L4_MemoryRefinement")
        self.service = service

    def execute(self, context: PipelineContext, bus=None) -> None:
        from gecce_kernel.core.types import EventType
        
        status = self.service.fsm.get_status()
        entry = {
            "timestamp": time.time(),
            "state": status['state'],
            "affect": status['affect'],
            "user_input": context.user_input,
            "trace_id": context.trace_id
        }
        
        # 1. Active Memory (Saliency Pruning)
        prune_codes = self.service.stm.add(entry)
        context.reason_codes.extend(prune_codes)
        
        # 2. Permanent Journal (Append-only)
        self.service.journal.log_entry(status, user_input=context.user_input)
        
        self.notify(bus, EventType.MEMORY_REFINED, {
            "pruned": bool(prune_codes),
            "reason_codes": prune_codes
        }, context)

class CognitiveDirector:
    """
    Orchestrates the Cognitive Pipeline using a Step-based Event-Driven flow.
    """
    def __init__(self, service):
        self.service = service
        self.steps = [
            ScenarioAnalysisStep(service.engine),
            FSMEvaluationStep(service.fsm),
            ValidationStep(service.engine),
            ProjectionStep(service),
            MemoryRefinementStep(service)
        ]

    def run_cycle(self, user_input: str, session_id: str = "default", manual_seed: Optional[int] = None) -> PipelineContext:
        """
        Synchronous run of the pipeline for CLI/API compatibility.
        In a fully async world, these triggers would come from EventBus subscribers.
        """
        context = PipelineContext(user_input=user_input, session_id=session_id, manual_seed=manual_seed)
        bus = self.service.kernel.bus if self.service.kernel else None
        
        for step in self.steps:
            step.execute(context, bus)
            
        return context
