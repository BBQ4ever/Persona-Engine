class MemorySalienceBridge:
    """
    Bridges the Persona Core with RAG (Retrieval-Augmented Generation) systems.
    Adjusts memory retrieval parameters based on the current affective state.
    """
    def __init__(self, fsm):
        self.fsm = fsm

    def get_retrieval_filters(self):
        """
        Generates metadata filters for a Vector Database based on the AI's mood.
        """
        affect = self.fsm.affect.get_affect()
        
        # Logic: 
        # 1. High Arousal (A) -> 'Detailed' or 'Recent' bias
        # 2. Low Pleasure (P) -> 'Melancholic' or 'Serious' bias
        # 3. High Dominance (D) -> 'Authoritative' or 'Core Logic' bias
        
        bias = "neutral"
        if affect['p'] > 0.4: bias = "positive"
        elif affect['p'] < -0.4: bias = "melancholic"
        
        intensity = "normal"
        if affect['a'] > 0.5: intensity = "high"
        
        return {
            "mood_bias": bias,
            "retrieval_intensity": intensity,
            "top_k_multiplier": 1.0 + (abs(affect['a']) * 0.5) # Arousal expands search breadth
        }

    def rerank_memories(self, memories):
        """
        Simple simulation of re-ranking retrieved memories based on current affect.
        Each memory is assumed to have an 'affect_signature' metadata.
        """
        current_p = self.fsm.affect.p
        
        # Prefer memories that are emotionally congruent
        for mem in memories:
            mem_p = mem.get("metadata", {}).get("pleasure_valence", 0.0)
            # Congruence Score: Higher is better
            congruence = 1.0 - abs(current_p - mem_p)
            mem["score"] = mem.get("score", 0.5) * (0.8 + 0.4 * congruence)
            
        return sorted(memories, key=lambda x: x["score"], reverse=True)
