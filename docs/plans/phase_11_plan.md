# Phase 11 Implementation Plan: Meta-Cognitive Self-Correction

## 1. Objective
Transform the Persona Engine from a reactive system into a self-evolving entity. The AI will analyze its own behavioral history (`Reflection Journal`), identify stylistic drift or emotional incongruence, and proactively adjust its DNA parameters.

## 2. Key Modules

### 2.1 Reflection Orchestrator (`src/l4_memory/reflection.py`)
- **Job**: A background service that triggers "Reflection Cycles."
- **Logic**: 
    - Read the last N entries from the `PersonaReflectionJournal`.
    - Batch them into a "Temporal Narrative."
    - Send this narrative to the LLM with a "Meta-Observer" role.

### 2.2 Persona Self-Correction API (`src/app_integration.py` updates)
- **Method**: `propose_dna_mutation()`
- **Action**: Based on reflection findings, suggest minor shifts in specific DNA loci (e.g., "I was too aggressive in the last 10 turns; reducing `assertiveness` default by 0.05").

### 2.3 Governance Guardrail (`src/l1_core/governance.py` updates)
- **Check**: Before a mutation is applied, verify it against the `GOVERNANCE_CHARTER` constraints.
- **Safety**: Prevent runaway mutations that would lead to "personality collapse."

### 2.4 Dashboard: Reflection View
- Visualize the "Reflection Reasoning" in the UI.
- Add an "Evolution History" log to show when and why the DNA changed.

## 3. Implementation Steps

1.  **Step 1: The Observer Prompt**
    - Create a template in `PromptAugmenter` focused on behavioral analysis.
2.  **Step 2: Automated Reflection Cycle**
    - Implement a method in `PersonaService` called `perform_reflection()`.
    - Test it by simulating a series of interactions and checking if the AI can identify its own mood patterns.
3.  **Step 3: Mutation Logic**
    - Implement the logic to update `self.genome` values dynamically.
    - Save the mutated genome to a new "evolved" snapshot.
4.  **Step 4: UI Integration**
    - Update the `Reflection Journal` section in the Dashboard to show AI's self-critique.

## 4. Verification
- Create `tests/test_phase_11.py`.
- Verify: "Interaction History" -> "Reflection" -> "DNA Update" -> "Next Prompt is improved."
