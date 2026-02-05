# Phase 11 Final Spec: The Cognitive Control Plane
> **Code Name:** "The Gyroscope"
> **Governance Level:** Enterprise Grade (Zero Autonomous Mutation)
> **Strategic Goal:** Ensure Persona reliability via automated drift correction and managed evolution.

---

## 1. Core Philosophy
> **"The goal of Phase 11 is not to let the AI evolve, but to ensure it never degrades."**

We define the Persona Engine not as a biological experiment, but as a **Cognitive Operating System** with strict Service Level Agreements (SLAs).

*   **Production Environment**: Immutable Genome. The system fights entropy to maintain the "Golden State".
*   **Evolutionary Sandbox**: Experimental. The system *proposes* changes (Deltas), but humans must *commit* them.

---

## 2. Architecture: "The Immune System"

### 2.1 The Control Loop (Production Default)
This loop runs automatically on every N interactions to correct behavioral drift. It does **NOT** modify the Genome.

1.  **Observer (L4)**: Reads the last window of interactions (e.g., 20 turns).
2.  **Comparator**: Calculates the *Observed Stance* vs. *Baseline Genome Stance*.
    *   *Baseline*: `Rigor 0.9`
    *   *Observed*: `Rigor 0.6` (Drift detected!)
3.  **Controller (L1)**: Generates a temporary **Correction Bias**.
    *   `Bias_Rigor = +0.4`
4.  **Actuator (L3)**: Injects a high-priority instruction into the System Prompt:
    *   `[GOVERNANCE OVERRIDE]: You are drifting towards informality. IMMEDIATELY increase Rigor and Detail.`

**Result**: The specific instance "heals" itself without altering the master file.

### 2.2 The Evolution Sandbox (Experimental / Opt-in)
This process runs offline or on-demand to analyze long-term patterns. It does **NOT** auto-apply changes.

1.  **Analysis**: "Users consistently react negatively to the high hostility (Chaos 0.8)."
2.  **Proposal**: Generate a `Persona Delta Artifact`.
3.  **Governance**: Human admin reviews the Delta.
    *   *Approve*: Apply Delta to Genome -> Release `v1.1`.
    *   *Reject*: Add constraint to prevent this drift in future.

---

## 3. The New Artifact: Persona Delta
To support "Managed Evolution," we introduce a standardized object for representing proposed changes.

```json
{
  "delta_id": "delta_20260204_001",
  "source_window": "session_882_to_950",
  "reasoning": "User explicitly requested shorter answers in 40% of turns.",
  "drift_metrics": {
    "current_verbosity": 0.8,
    "target_verbosity": 0.4
  },
  "suggested_mutation": {
    "loci": "explanation_depth",
    "old_value": 0.8,
    "new_value": 0.5,
    "operation": "SET"
  },
  "confidence_score": 0.85,
  "risk_level": "LOW",
  "status": "PENDING_APPROVAL" // PENDING | APPROVED | REJECTED
}
```

---

## 4. Implementation Plan

### Step 1: Metrics Extraction (The Yardstick)
We need a way to measure the "Observed Stance" dynamically.
*   *Action*: Create `src/l4_memory/metrics.py`.
*   *Task*: Use a small, cheap LLM call (or embedding analysis) to score the last N messages on R/W/C scales.

### Step 2: Gyroscope Logic (The Stabilizer)
Update `src/l0_orchestrator/engine.py`:
*   Add `check_drift()` method.
*   Implement `Correction Bias` logic in `get_effective_constraints()`.

### Step 3: Governance CLI (The Gavel)
Update `persona_cli.py`:
*   Add command `propose-delta` to generate a delta file.
*   Add command `apply-delta` to merge a delta into the Genome.

---

## 5. Strategic Value

| Feature              | Business Value                                                                |
| :------------------- | :---------------------------------------------------------------------------- |
| **Drift Correction** | **SLA Compliance**. "Your banking bot will strictly stay professional."       |
| **Delta Artifacts**  | **A/B Testing**. "We can mathematically prove version 1.2 is 10% friendlier." |
| **Sandbox**          | **Safety**. "No Chatbot Tay scenarios. All mutations are reviewed."           |

---

**Verdict:**
This architecture changes the Persona Engine from a "Creative Writing Tool" to a **"Governance Platform for AI Behavior"**. 
