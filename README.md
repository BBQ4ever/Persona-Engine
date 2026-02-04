# 🧠 Persona Engine (GECCE-Substrate)

> **"Beyond static prompts: Implementing a 4-Layer Dynamic Persona Substrate for LLMs."**

Persona Engine is a high-performance framework built on the **GECCE Kernel**. It replaces static "System Prompts" with a dynamic 4-layer architecture (Engine, Core, Genome, Expression), enabling **Stochastic Sampling**, **Scenario-Aware Degradation**, and **Deterministic Evolution**.

---

## 🇨🇳 中文文档 (Chinese Documentation)
针对中文用户，我们提供了完整的中文文档库：
👉 **[点击进入中文文档中心 | Chinese Documentation Center](./docs/README_CN.md)**

---

## 🏗️ 4-Layer Architecture
This project follows the strict specifications outlined in **[ARCHITECTURE.md](./ARCHITECTURE.md)**:

1.  **L0: Orchestrator** - Scenario recognition and persona influence scaling.
2.  **L1: Core** - Lifecycle FSM (Forming -> Stable) and consistency control.
3.  **L2: Genome** - Structural DNA defined by **[GENOME_CHARTER.md](./GENOME_CHARTER.md)**.
4.  **L3: Expression** - Seeded sampling and Prompt Augmentation.

---

## 🚀 Key Features
- **Kernel-Driven**: Built on GECCE Event Bus for 100% traceability.
- **Truth Independence**: Physical separation of persona and factual logic.
- **DNA Dashboard**: A high-tech interactive UI to observe "Personality Fingerprints".
- **Asset Migration**: Persona states can be snapshotted, exported, and rolled back.

---

## ⚡ Quick Start

### 1. Environment Setup
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Run Kernel Demo
Verify the coordination of all 4 layers on the GECCE substrate:
```bash
export PYTHONPATH=$PYTHONPATH:$(pwd)/src:$(pwd)/gecce_kernel_pkg
python3 src/main_kernel_demo.py
```

### 3. Launch Dashboard
Visualize the live "Personality DNA":
```bash
cd dashboard && npm run dev
```

---

## 🛠️ Tech Stack
- **Backend**: Python 3.10+, GECCE Kernel, Pydantic.
- **Frontend**: Vite, Vanilla JS, CSS (Glassmorphism UI).
- **Core Data**: JSON Schema (L2 Loci).

---

## 📅 Roadmap
Project milestones and current status: **[ROADMAP.md](./ROADMAP.md)**

---

*“Personality is no longer a collection of adjectives, but a computable, observable stream of probability.”*
