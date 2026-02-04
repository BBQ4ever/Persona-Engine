# Phase 3 Report: Orchestration & Scenario Degradation

## 🎯 Objective
Empower the system (Layer 0) to sense the environment and automatically scale the persona's influence to prevent interference in critical tasks.

## 🛠️ Key Components
1.  **Scene Analyzer**: A regex-based engine that classifies input into `SOCIAL_CREATIVE` or `STRICT_FACT`.
2.  **Influence Scaler**: Dynamically adjusts the `influence_level` (from 1.0 to 0.1) based on the detected scene.
3.  **Emergency Kill-Switch**: A top-level override to completely bypass the persona layer in high-risk situations.

## 💡 Technical Insights
- **The 0.1 Floor**: We never set the influence to 0.0 in strict mode; a 0.1 "Style-only" floor is maintained to keep the response structure without adding noise.
- **Bi-Directional Keywords**: Supports both English and Chinese critical keywords (e.g., "calculate", "证明").

## ✅ Outcome
A safety-first orchestrator.
- **Demo Proof**: Successfully degraded personality during math queries in `src/main_demo.py`.
---
# Phase 3 报告：调度与场景降级

## 🎯 目标
赋予系统（第 0 层）感知环境的能力，并自动缩放人格的影响力，以防止在关键任务中产生干扰。

## 🛠️ 关键组件
1.  **场景分析器**：一个基于正则的引擎，将输入分类为 `SOCIAL_CREATIVE`（社交创意）或 `STRICT_FACT`（严谨事实）。
2.  **影响力缩放器**：根据检测到的场景动态调整 `influence_level`（从 1.0 到 0.1）。
3.  **紧急熔断开关**：一个顶级覆盖机制，在交互风险极高时完全绕过人格层。

## 💡 技术见解
- **0.1 的底线**：在严谨模式下，我们从不将影响力设为 0.0；保持 0.1 的“仅风格”底线，以在不添加噪音的情况下保持回复结构。
- **双语关键词**：支持中英文关键术语（如 "calculate", "证明"）。

## ✅ 成果
一个安全第一的调度器。
- **演示验证**：在 `src/main_demo.py` 的数学查询中成功降级了人格。
