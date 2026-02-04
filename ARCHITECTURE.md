# Persona Architecture (Formal Specification)

> **In one sentence:**
> Provide AI with a **stable, constrained, and evolving internal persona substrate** that determines preferences, behavioral styles, and choice spaces, **without interfering with factual judgment and reasoning correctness**.

---

## L0 — Persona Engine

**(System Level / Orchestrator Layer)**

### Responsibilities

- Unified management of persona-related **lifecycle, state, scheduling, and boundaries**.
- Determines **when** the persona intervenes and **to what extent**.
- Provides standard external interfaces, isolating downstream system complexity.

### Boundaries (What it does NOT do)

- ❌ Does not generate final answers.
- ❌ Does not make factual judgments.
- ❌ Does not claim "consciousness / self / subjectivity".

### Typical Tasks

- Scenario recognition (whether to enable persona).
- Intensity control (persona influence level).
- Safety/Strict scenario degradation (persona → style-only).

---

## L1 — Persona Core

**(Core Control Layer / Deterministic Controller)**

### Responsibilities

- Defines "what this AI essentially is".
- Manages the **evolutionary states (Forming / Stable / Drifting)**.
- Ensures cross-session consistency and long-term stability.

### Typical States

- FORMING: Initial discovery phase.
- STABILIZING: Convergence of traits.
- STABLE: Mature persona.
- LOCKED: High-consistency/Unchangeable state.

---

## L2 — Persona Genome

**(Structure Layer / Data + Constraint Layer)**

### Responsibilities

- Defines internal tendencies using **structural Gene Loci**.
- Outputs **preference distributions and behavioral weights**.
- Does not give answers, only **boundaries**.

---

## L3 — Persona Expression

**(Expression Layer / Stochastic Projection Layer)**

### Responsibilities

- Samples specific traits from boundaries (Seeded Sampling).
- Translates numerical traits into **Natural Language Instructions (Prompt Augmentation)**.
- Ensures the "flavor" of the response matches the current persona state.
