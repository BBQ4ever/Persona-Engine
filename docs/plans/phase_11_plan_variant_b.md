# Phase 11 Variant B: Compliance-First Behavioral Correction
> **Code Name:** "The Gyroscope"
> **Strategic Alignment:** Based on `internal/strategic_health_check.md`
> **Contrast:** Replaces "Evolutionary Adaptation" (Variant A) with "Drift Correction" (Variant B).

## 1. Core Philosophy: Stability Over Evolution
In the "Biological" view (Variant A), self-correction is about **adaptation**: *"The user wants me to be funnier, so I will rewrite my genome to be funnier."*
In this "Engineering" view (Variant B), self-correction is about **integrity**: *"My genome mandates I am serious (Rigor 0.9), but my recent outputs have been too loose (Rigor 0.6). I must correct this deviation."*

**The Goal:** Not to "grow," but to **prevent decay**.

## 2. A/B Comparison

| Feature       | Variant A (Biological / Original)       | **Variant B (Governance / New)**                 |
| :------------ | :-------------------------------------- | :----------------------------------------------- |
| **Trigger**   | "I feel like changing." / User Feedback | **Metric Deviation (Drift Detection)**           |
| **Logic**     | Evolutionary Algorithm (Mutation)       | **PID Controller (Error Correction)**            |
| **Direction** | Towards User Preference                 | **Towards Baseline Specification**               |
| **Safety**    | Low (Risk of catastrophic forgetting)   | **High (Guaranteed SLA)**                        |
| **Output**    | "I have evolved into a new persona."    | **"I have restored my operational parameters."** |
| **Metaphor**  | Darwinian Natural Selection             | **Flight Control System (Auto-Pilot)**           |

## 3. Implementation Logic (The Control Loop)

Instead of a "Psychologist" reflecting on feelings, we implement an **"Auditor"**.

### Step 1: Drift Measurement (Observer)
The system analyzes the last N interactions and calculates the *observed* R.W.C vectors.
*   *Target:* `{ Rigor: 0.9, Warmth: 0.2, Chaos: 0.1 }`
*   *Observed (Last 10 msgs):* `{ Rigor: 0.5, Warmth: 0.4, Chaos: 0.3 }`
*   *Drift Error:* `ΔR = -0.4`, `ΔW = +0.2`

### Step 2: Correction Calculation (Controller)
Using a PID-like logic (Proportional-Integral-Derivative):
*   `Adjustment_R = Kp * ΔR`
*   The system generates a temporary **"Correction Bias"** to be injected into the next System Prompt.

### Step 3: Prompt Injection (Actuator)
The Engine injects a specific correction instruction into the `[POLICIES]` section:
> *"WARNING: Recent outputs have lacked required Rigor. You must OVER-CORRECT by being excessively detailed and formal in the next response."*

## 4. Why This Wins the Enterprise
*   **Auditability**: CTOs don't want AI that "evolves" unpredictably. They want AI that "self-heals" when it starts hallucinating or getting lazy.
*   **Consistency**: This guarantees that a "Tech Support Persona" stays helpful and professional, even if a user tries to jailbreak it or make it chat about movies.

## 5. Technical Requirements
1.  **Metric Extractor**: A lightweight classifier (can be a small LLM call) to score recent interaction logs.
2.  **Baseline Store**: The immutable "Gold Standard" genome to compare against.
3.  **Correction Signal**: A feedback channel from L4 (Memory) to L3 (Expression) that is *transient* (only active until drift is fixed).

---
**Recommendation:**
For the current "Enterprise-Grade" strategic pivot, **Variant B is the superior choice.** It reinforces the "No-Go Zone" charter and the promise of reliability.
