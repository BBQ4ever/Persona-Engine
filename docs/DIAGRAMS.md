# 📊 Persona Engine: Technical Diagrams

This document provides a visual representation of the Persona Engine's architecture, data flows, and logic systems using Mermaid diagrams.

---

## 1. 🏛️ Layered Architecture (L0-L3)
The system is built on a 4-layer substrate, governed by the GECCE Kernel.

```mermaid
graph TD
    subgraph L3 [Layer 3: Expression]
        E1[Seeded Sampler] --> E2[Prompt Augmenter]
    end

    subgraph L2 [Layer 2: Genome]
        G1[JSON Loci DNA] --> G2[Truth Validator]
    end

    subgraph L1 [Layer 1: Core]
        C1[Persona FSM] --> C2[Drift Controller]
        C3[Relationship Mgr]
    end

    subgraph L0 [Layer 0: Orchestrator]
        O1[Scenario Analyzer] --> O2[Influence Scaler]
    end

    Input((User Input)) --> O1
    O2 --> L1
    L1 --> L2
    L2 --> L3
    L3 --> Output[System Prompt]
    
    style L0 fill:#f9f,stroke:#333,stroke-width:2px
    style L1 fill:#bbf,stroke:#333,stroke-width:2px
    style L2 fill:#bfb,stroke:#333,stroke-width:2px
    style L3 fill:#fbb,stroke:#333,stroke-width:2px
```

---

## 2. 🔄 Sequence Diagram: Interaction Loop
How an event travels through the kernel substrate.

```mermaid
sequenceDiagram
    participant U as User
    participant K as GECCE Kernel (EventBus)
    participant L0 as Orchestrator
    participant L1 as Core (FSM)
    participant L3 as Expression (Augmenter)
    participant LLM as Language Model

    U->>K: Send Input (e.g. "Calculate Sqrt")
    K->>L0: Trigger PERSONA_INPUT event
    L0->>L0: Analyze Scenario (Strict Fact Detected)
    L0->>K: Emit PERSONA_DEGRADED (Influence -> 0.1)
    
    K->>L1: Update State & Intimacy
    L1->>K: Fetch Current Genome (L2)
    
    K->>L3: Request Projection
    L3->>L3: Seeded Sampling + Bandwidth Gating
    L3->>K: Output Augmented Prompt
    
    K->>LLM: System Prompt + User Query
    LLM->>U: Balanced Response
```

---

## 3. 🧬 Data Model: Genome DNA Entity
Structural definition of a Trait Locus.

```mermaid
classDiagram
    class Genome {
        +String version
        +Metadata metadata
        +List~Locus~ loci
    }
    class Locus {
        +String id
        +Enum category
        +Distribution distribution
        +Float weight
        +Float variability
    }
    class Distribution {
        +Enum type (Scalar/Range/Categorical)
        +Map values
    }
    Genome "1" *-- "many" Locus
    Locus "1" *-- "1" Distribution
```

---

## 4. 📈 Persona Lifecycle (FSM)
The evolution path of a single persona entity.

```mermaid
stateDiagram-v2
    [*] --> FORMING: Creation
    FORMING --> STABILIZING: Interaction > 10
    STABILIZING --> STABLE: Interaction > 50
    STABLE --> DRIFTING: Feedback Loop
    DRIFTING --> STABLE: Convergence
    STABLE --> LOCKED: Manual/Final Lockdown
    LOCKED --> [*]: Immutable Asset
```

---

## 🌐 Navigation
- [Back to README](../README.md)
- [Architecture Details](./zh/architecture_cn.md)
