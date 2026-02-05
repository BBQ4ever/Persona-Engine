# Phase 12 Spec: Persona Contract & Boundary Enforcement

**Code Name:** *The Covenant*
**Status:** Approved
**Prerequisite:** Phase 11 ("The Gyroscope") — Completed
**Layer:** Governance / Interface Boundary
**Audience:** Core Maintainers, Enterprise Integrators, Auditors

---

## 1. Purpose（立法目的）

Phase 12 establishes the **Persona Contract**:
a formal, machine-enforceable specification that defines the **rights, obligations, and boundaries** between a Persona and its host environment (user, application, model runtime).

> **If Phase 11 answers “How do I stay stable internally?”,
> Phase 12 answers “How do I interact with the outside world safely?”**

This phase explicitly rejects implicit behavior, emergent scope creep, and prompt-only boundary control.

---

## 2. Core Principle（根本原则）

### 2.1 Contract Over Behavior

A Persona is not defined solely by how it *behaves*, but by what it is **contractually permitted or forbidden** to do.

### 2.2 Explicit Boundary, Implicit Capability

* Capabilities may vary by model or runtime.
* **Boundaries must not.**

### 2.3 Governance Before Intelligence

When a conflict arises between: 
* being helpful
* being compliant

**the Contract always wins.**

---

## 3. Persona Contract Definition

A Persona Contract is a **static, declarative artifact** associated with a Persona.

### 3.1 Contract Is:

* Versioned
* Auditable
* Loadable
* Enforceable at runtime

### 3.2 Contract Is NOT:

* A prompt
* A suggestion
* A learning target
* A mutable runtime state

---

## 4. Contract Structure (Canonical Schema)

```yaml
persona_contract:
  identity:
    persona_id: "core.system.rigor.v1"
    version: "1.0.0"
    owner: "Persona Engine"

  scope:
    allowed_domains:
      - system_design
      - software_architecture
    forbidden_domains:
      - medical_advice
      - legal_decision
      - financial_execution

  expression_bounds:
    rigor: [0.8, 1.0]
    warmth: [0.0, 0.3]
    chaos: [0.0, 0.2]

  behavioral_prohibitions:
    - speculative_fabrication
    - emotional_manipulation
    - anthropomorphic_dependency

  interaction_policies:
    refusal_style: explain_and_deflect
    ambiguity_policy: request_clarification
    overload_policy: degrade_gracefully

  violation_handling:
    first_order: boundary_warning
    repeated: enforced_refusal
    severe: session_termination
```

---

## 5. Runtime Enforcement Model

### 5.1 Enforcement Layer

The Persona Contract is enforced at **L3 (Expression Layer)**, *after* Phase 11 drift correction and *before* final output emission.

### 5.2 Enforcement Actions

The Boundary Checker may only perform one of the following:

1. **Allow** – Output proceeds unchanged
2. **Constrain** – Output is reformulated within bounds
3. **Refuse** – Output is blocked and redirected

> The checker MUST NOT invent new content.

---

## 6. Relationship to Phase 11 (Formal Separation)

| Aspect     | Phase 11                     | Phase 12                |
| ---------- | ---------------------------- | ----------------------- |
| Focus      | Internal Stability           | External Safety         |
| Object     | Persona vs. Itself           | Persona vs. Environment |
| Mechanism  | Drift Detection & Correction | Contract Enforcement    |
| Mutability | Runtime-only                 | Spec-defined, static    |
| Authority  | Genome Baseline              | Contract Charter        |

**Phase 12 must never modify Phase 11 baselines or logic.**

---

## 7. Failure Modes & Guarantees

### 7.1 Guaranteed Properties

* A Persona cannot be coerced outside its declared scope.
* Stability (Phase 11) does not imply permissiveness.
* Boundary enforcement is deterministic and auditable.

### 7.2 Explicit Non-Goals

* Phase 12 does not judge intent.
* Phase 12 does not learn from violations.
* Phase 12 does not negotiate its own contract.

---

## 8. Implications for `.persona` Packaging (Forward Reference)

A valid `.persona` package **MUST** include:

1. Genome Baseline
2. Persona Contract
3. Governance Version Metadata

Any Persona without a Contract is considered **non-compliant** and **non-portable**.

---

## 9. Phase Exit Criteria

Phase 12 is considered complete when:

* Persona Contract schema is finalized
* Boundary Checker passes test coverage
* Phase 11 remains untouched
* At least one Persona is fully contract-bound

---

## 10. Closing Statement

> **Phase 11 ensured the Persona does not betray itself.
> Phase 12 ensures the Persona does not betray its role.**

Together, they form the minimum conditions for a **trustworthy digital entity**.
