# Architecture Brief: The Identity Runtime (Persona Engine V1)

## 1. The Core Thesis
The Persona Engine is not a chatbot; it is a **distributed cognitive compiler**. It translates raw user intent into an **Artifact** (System Prompt) governed by a **Canonical Event Stream**.

## 2. Structural Layering (L0-L4)
| Layer  | Name           | Function                                | Governance            |
| :----- | :------------- | :-------------------------------------- | :-------------------- |
| **L0** | **Scenario**   | Intent Classification (Fact vs. Social) | Mode Gating           |
| **L1** | **Affect**     | PAD Emotional Manifold (Clock-based)    | Expression Modulation |
| **L2** | **Genome**     | Safety Anchors & Identity Charter       | Hardcoded Sovereignty |
| **L3** | **Projection** | Seeded Stochastic trait sampling        | Isolation Boundary    |
| **L4** | **Memory**     | Saliency-based short-term reflection    | Audit & Continuity    |

## 3. Constitutional Guarantees
1.  **Safety Absolute**: Safety anchors are hardcoded; no affective state or user input can modify the sovereignty of the Genome.
2.  **Explicit Reasoning**: Every decision produces a `Reason Code`. No code = No execution.
3.  **Event-Driven Truth**: The `EventBus` is the canonical narrative; it facilitates real-time auditing and replayability.
4.  **L3 Isolation**: "How the AI feels" (Affect) can only warp "How the AI speaks" (L3), never "What the AI is allowed to do" (L2).

## 4. Operational Protocol
- **Input**: User Message + Session Context.
- **Processing**: Synchronous Pipeline (CognitiveDirector) emitting asynchronous events.
- **Output**: Multi-part Artifact containing:
    - `messages`: Ready-to-use LLM packet.
    - `metadata`: Full audit trail (TraceID, Reason Codes, Stance).

## 5. Strategic Identity
By decoupling identity from the underlying LLM, we provide an **Identity Runtime** that ensures character consistency across different models and sessions, enabling verifiable and stable digital personhood.
