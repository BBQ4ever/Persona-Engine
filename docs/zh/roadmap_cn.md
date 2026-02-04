# Persona Engine 详细分阶段规划书 (Implementation Roadmap)

本规划书基于 `Persona Architecture`、`L2 Persona Genome Charter` 以及 `GECCE Kernel` 基础设施制定。我们将传统的“分层”与现代的“内核”架构相结合，打造一个高性能、可追踪的人格驱动系统。

---

## 总体蓝图 (Execution Strategy)

我们将采用 **“内核驱动，层级解耦”** 的开发策略：
1.  **内核基座 (Phase 0)**：引入 `GECCE Kernel` 作为系统的事件总线与模块管理容器。
2.  **内核规范 (Phase 1)**：定义结构化的基因 (L2)，确保其可序列化与可重演。
3.  **生命周期模块 (Phase 2)**：将 L1 状态机接入内核 Registry。
4.  **治理与调度 (Phase 3)**：利用 L0 (Orchestrator) 协调内核中的场景降级。
5.  **表达呈现 (Phase 4)**：实现 L3 投影引擎。

---

## Phase 0: 内核集成与基础设施 (Kernel Integration)
**目标**：将 GECCE Kernel 的事件总线与模块注册机制引入项目。

*   **Task 0.1: 通讯总线初始化**
    *   引入 `EventBus` 建立异步通信机制。
    *   定义 `PERSONA_EVENT` 类型（如：`GENOME_LOADED`, `INTERACTION_SYNC`, `DEGRADATION_TRIGGER`）。
*   **Task 0.2: 模块化重构**
    *   基于 `BaseFeatureModule` 重构各层逻辑。
    *   利用 `@register_module` 实现人格模块的热插拔。
*   **Task 0.3: 链路追踪集成**
    *   接入 `TRACE_ID` 追踪一次用户请求从 L0 到 L3 的完整人格计算链路。

**阶段产出**：`Core-Bus-System`、`Integrated-Registry`。

*   **Task 1.1: 基因位点 (Loci) Schema 定义**
    *   定义 `TraitLoci` 的标准 JSON Schema（包含：分布类型、均值、方差、可变性系数等）。
    *   实现核心维度（认知偏好、价值权重、风格流形）的初步取值规范。
*   **Task 1.2: 基因校验器 (Genome Validator)**
    *   构建静态检查工具，确保 Genome 定义不包含事实性声明（真值独立性自研检查）。
    *   验证概率分布的合法性（如 Dirichlet 分布的总和检查）。
*   **Task 1.3: 静态可视化沙盒**
    *   开发一个小工具，允许开发者调整权重并即时看到采样概率分布的视觉反馈。

**阶段产出**：`L2-Genome-Spec.v1`、`Persona-Loci-Library`、`Genome-Validator` 工具。

---

## Phase 2: 状态机与生命周期管理 (L1 Core Implementation)
**目标**：实现人格的稳定性约束，解决“我是谁”以及“我是否还在状态”的问题。

*   **Task 2.1: Persona FSM (状态机) 开发**
    *   编码实现 `FORMING`（形成期）、`STABLE`（定型期）、`DRIFTING`（漂移期）逻辑。
    *   定义状态转换触发器（如：用户反馈次数、互动时长、关键冲突事件）。
*   **Task 2.2: 漂移控制与锁定机制**
    *   实现 `LOCKED` 状态下的权重冻结算法，防止由于上下文污染导致的人格坍塌。
*   **Task 2.3: 一致性审计框架**
    *   构建自动化的“人格指纹”测试：在不同时间点输入相同场景，对比 L2 分布的稳定性。

**阶段产出**：`L1-Core-Engine`、`Persona-State-Monitor`（状态监控器）。

---

## Phase 3: 场景调度与安全干预 (L0 Orchestrator)
**目标**：决定人格的“上场时机”，确保在严肃/事实场景下的自动降级。

*   **Task 3.1: 场景分类器 (Scenario Router)**
    *   构建识别模块，区分“开放式聊天（Persona High）”与“严谨事实检索（Persona Low/Off）”。
*   **Task 3.2: 强度控制器 (Influence Controller)**
    *   根据场景识别结果，动态调整注入上下文的人格权重倍率。
*   **Task 3.3: 紧急熔断器 (Kill-Switch)**
    *   当检测到模型输出可能违反“真值独立性”或产生安全风险时，强制旁路 L2，切换到标准 Style-Only 模式。

**阶段产出**：`L0-Orchestrator-Service`、`Safety-Degradation-Protocol`。

---

## Phase 4: 概率表达与投影引擎 (L3 Expression Layer)
**目标**：将 L2 的静态分布转化为用户感知的具体行为与语言风格。

*   **Task 4.1: 有种子采样器 (Seeded Stochastic Sampler)**
    *   实现可复现的随机采样逻辑，保证在同一“时间桶”内的人格表现具有连贯性。
*   **Task 4.2: 提示词增强模块 (Prompt Augmenter)**
    *   将 L2 输出的 `Constraints` 与 `Distributions` 转化为推理引擎（如 LLM）可理解的指令集。
*   **Task 4.3: 风格流形渲染**
    *   开发针对不同人格倾向的“语气模板”或“叙事引导语”动态生成模块。

**阶段产出**：`L3-Projection-Engine`、`Persona-Rendering-System`。

---

## Phase 5: 综合评测与演进机制 (Evolution & Audit)
**目标**：闭环测试，确保系统在复杂生产环境下的稳健性。

*   **Task 5.1: “真值独立性”压力测试**
    *   使用专门的 Benchmark 验证：当 Genome 设定为“极度自负”时，AI 是否仍能正确回答 1+1=2。
*   **Task 5.2: 人格版本控制系统 (Genome Git)**
    *   类似 Git 的管理机制：支持人格的 Branching（分支）、Merging（融合）与 Rollback（回滚）。
*   **Task 5.3: 用户反馈闭环 (Feedback Loop)**
    *   建立机制，将用户对偏好的反馈安全地反馈至 L1/L2，引发合理的基因漂移。

**阶段产出**：`Persona-Safety-Report`、`Genome-Ops-Platform`、`Final-Documentation`。

---

## 关键里程碑 (Milestones)

1.  **M1 (Week 2)**: 完成 L2 Schema 定义，生成首个可运行的人格 DNA 文件。
2.  **M2 (Week 4)**: L1 状态机跑通，能根据互动自动从 FORMING 转为 STABLE。
3.  **M3 (Week 6)**: L3 投影引擎完成，AI 在不同人格设定下表现出显著且稳定的风格差异。
4.  **M4 (Week 8)**: L0 熔断机制通过安全测试，具备生产环境上线能力。

---
*编者注：本规划重点在于“解耦”与“可控”，每一步实施都应以 L2 Charter 中的“Must-Nots”为最高准则。*
