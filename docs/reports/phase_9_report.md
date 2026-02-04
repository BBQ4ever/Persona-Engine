# Persona Engine Technical Report - Phase 9: Fluid Stance & R.W.C Model

## 1. Phase Objective
The objective of this phase was to transition from a discrete, "RPG-style" archetype switching system to a continuous "Fluid Stance" model. This removes the artificial boundaries between personality presets and allows the persona to adapt its "vibe" and "auras" smoothly across a 3D parameter space.

## 2. Core Implementations

### 2.1 R.W.C Stance Vector Model
We replaced hardcoded enums with a 3-dimensional **Stance Vector**:
- **Rigor (R)**: Controls logical depth, technical precision, and analytical strategy.
- **Warmth (W)**: Controls emotional valence, linguistic softness (feminine/masculine bias), and harmony.
- **Chaos (C)**: Controls humor density and stochastic variability (predictability vs. creativity).

### 2.2 Vector-to-DNA Mapping (The Projection)
The `ArchetypeManager` was refactored into a stance projector. Instead of overwriting values, it performs linear interpolation across the valid range of each DNA locus based on the R.W.C coordinates. 
- **Dynamic Variability**: The `Chaos` parameter now directly modulates the `variability` coefficient of every locus, making the persona feel "unstable" or "exuberant" at high C levels.

### 2.3 Intent-Driven Auto-Switching
The Layer-0 `PersonaEngine` was upgraded from suggesting "Names" to calculating "Stances":
- **Math/Scientific Intent**: Automatically projects to `Rigor=0.9, Warmth=0.2, Chaos=0.1`.
- **Emotional/Support Intent**: Automatically projects to `Rigor=0.3, Warmth=0.9, Chaos=0.4`.
- This ensures the transition is no longer a "mask swap" but an organic shift in the AI's cognitive posture.

### 2.4 Visualization: DNA Topology Radar
To expose the hidden geometry of the R.W.C model, we implemented the **L2 DNA Radar**:
- **Dynamic Morphing**: The radar chart visualizes the real-time values of DNA loci. As the R.W.C stance shifts, the radar's shape morphs smoothly, showing the "soul shape" of the persona.
- **Visual Purity**: We optimized the radar with smart-anchored labels to prevent clipping of technical terms (e.g., LOGICAL, EXPLANATION).

### 2.5 Structural Refactor & Stabilization
- **Test Relocation**: Moved all `test_*.py` files to a dedicated `/tests` directory to clean up the `src` root.
- **Sampling Polish**: Fixed a noise amplification bug in `SeededSampler` to ensure that stance-based anchoring is respected even at higher influence levels.

## 3. Technical Insight: Personality as a Liquid Stance
By moving to a vector-based model, we've achieved "Personality Continuity." Any two archetypes (e.g., "Cold Analyst" and "Warm Mentor") can now be blended at any ratio (e.g., a "Burned-out but Kind Detective" at 70% Analyst / 30% Mentor). The visualization reflects this by showing the persona's topology in a state of constant, fluid transition.

## 4. Deliverables
- `src/l2_genome/archetypes.py`: Refactored R.W.C mapping logic.
- `src/l2_genome/presets/standard_archetypes.json`: Externalized presets configuration.
- `src/l0_orchestrator/engine.py`: Updated to stance-aware intent analysis.
- `src/app_integration.py`: Fluid stance API (`set_stance`).
- `tests/test_phase_9.py`: Comprehensive fluid transition validation.

## 5. Next Step Preview: Phase 10 - Multi-Session Coherence & Persistence
We will begin implementing long-term memory integration, allowing the persona's affective state and learned drifts to persist across sessions via Kernel Snapshots.
