# Phase 12.5 Spec: The Memory Charter (Data Sovereignty & Multimodal Governance)

**Code Name:** *The Vault*
**Status:** Draft
**Parent Spec:** Phase 12 (The Persona Contract)
**Focus:** Privacy, Compliance, and Data Sovereignty
**Audience:** Data Protection Officers (DPO), Enterprise Architects, Integrators

---

## 1. The Ontology: Memory vs. Knowledge

To prevent hallucination and authorization leakage, the Persona Engine enforces a strict ontological separation:

### 1.1 Knowledge (The Library)
*   **Definition**: Static, verifiable facts external to the persona's identity.
*   **Source**: RAG Indices, Documents, APIs.
*   **Nature**: Read-Only, Replaceable, Non-Sensitive.
*   **Governance**: **Version Control.** (e.g., "Use Company Handbook v2.1")

### 1.2 Memory (The Journal)
*   **Definition**: Contextual, subjective records of interactions and state changes.
*   **Source**: User Interactions, Internal Reflection (L4), System Events.
*   **Nature**: Append-Only (Log), Sensitive, Identity-Binding.
*   **Governance**: **The Memory Charter.**

> **Rule:** A Persona can *cite* Knowledge, but it *lives* in Memory.

---

## 2. Multimodal Governance Model

We treat memory not as a text log, but as a collection of **Artifacts** with strict permissions.

### 2.1 The "Default Deny" Principle
All non-text modalities are **disabled by default**. They must be explicitly enabled in the Persona Contract.

### 2.2 Modality Tiers

| Tier   | Modality            | Risk Profile     | Default Policy                            |
| :----- | :------------------ | :--------------- | :---------------------------------------- |
| **L0** | **Text / Metadata** | Low              | **Allowed** (with PII redaction)          |
| **L1** | **Embeddings**      | Low              | **Allowed** (Opaque vectors)              |
| **L2** | **Audio / Voice**   | High (Biometric) | **Restricted** (Requires Consent + Audit) |
| **L3** | **Visual / Image**  | High (Privacy)   | **Restricted** (Ephemeral Only)           |

### 2.3 Biometric Artifact Contract
For **L2/L3** artifacts (e.g., Voice Fingerprints), the following metadata is MANDATORY:
*   `consent_id`: Reference to user consent record.
*   `usage_scope`: (e.g., "Authentication Only" vs "Generative Synthesis").
*   `retention_ttl`: Expiration date (e.g., "Session Only" vs "30 Days").

---

## 3. Data Sovereignty & Lifecycle

### 3.1 The Right to be Forgotten
Every Memory Artifact must carry a unique ID. The Engine must support:
*   `purge_memory(id)`: Surgical removal.
*   `forget_user(user_id)`: Bulk removal of associated context.
*   `reset_persona()`: Restoration to factory Genome (Knowledge retained, Memory wiped).

### 3.2 Automated Retention (TTL)
Memory is not eternal. The Charter defines automated pruning:
*   **Short-term**: Raw logs kept for N turns (Context Window).
*   **Long-term**: Summarized/Vectorized insights (L4).
*   **Expired**: Biometric data deleted after T seconds (if ephemeral).

### 3.3 Exportability
*   **Format**: `.persona_memory` (Encrypted Zip).
*   **Constraint**: Knowledge indices are NOT included (preventing IP theft). Only the *subjective experience* (Memory) is exported.

---

## 4. Implementation Requirements

To support "The Vault", the storage layer must implement:
1.  **Encryption at Rest**: AES-256 for the Memory Store.
2.  **Access Logs**: Every read of an L2/L3 artifact is logged to an immutable audit trail.
3.  **PII Scrubber**: In-flight redaction of credit cards/SSNs before writing to L0 Text Memory.

---

## 5. Strategic Value

> **"We don't just store data; we govern experience."**

By implementing The Memory Charter, Persona Engine becomes compliant with GDPR, CCPA, and Enterprise Security Standards out of the box. It transforms "Memory" from a liability into a managed asset.
