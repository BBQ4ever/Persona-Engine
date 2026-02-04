# Persona Architecture（正式版）

> **目标一句话**
> 为 AI 提供一个**稳定、可约束、可演化的内在人格驱动系统**，
> 用于决定偏好、行为风格与选择空间，而**不参与事实判断与推理正确性**。

---

## L0 — Persona Engine

**（系统级 / Orchestrator 层）**

### 职责

* 统一管理人格相关的**生命周期、状态、调度与边界**
* 决定 **什么时候** 人格介入，**介入到什么程度**
* 对外提供标准接口，隔离下游系统复杂度

### 不做什么（边界很重要）

* ❌ 不生成具体答案
* ❌ 不做事实判断
* ❌ 不声明“意识 / 自我 / 主体性”

### 典型职责

* 场景识别（是否启用 persona）
* 强度控制（persona influence level）
* 安全/严肃场景降级（persona → style-only）

> **一句定位**：
> *Persona Engine 决定“人格是否上场，以及上场到几分”。*

---

## L1 — Persona Core

**（核心控制层 / Deterministic Controller）**

### 职责

* 定义“这个 AI **大体上是一个什么样的存在**”
* 管理人格的**阶段性状态（形成 / 定型 / 漂移）**
* 负责人格的一致性与长期稳定

### 核心机制

* Persona FSM（人格状态机）
* 人格一致性约束（跨问题、跨时间）
* 漂移控制与锁定策略

### 典型状态

* FORMING（形成期）
* STABILIZING（收敛期）
* STABLE（定型期）
* DRIFTING（受反馈影响的微调期）
* LOCKED（强一致期）

> **一句定位**：
> *Persona Core 决定“我是不是还是同一个我”。*

---

## L2 — Persona Genome

**（结构层 / Data + Constraint Layer）**

这是你最核心、也最“DNA”的那一层。

### 职责

* 以**结构化基因位点（Loci）**定义人格的内在倾向
* 输出的是 **偏好分布、行为权重、可选空间**
* 不直接给答案，只给**边界**

### 内容形态

* Trait Loci（偏好 / 认知 / 行为 / 价值）
* 每个位点 = 分布 + 权重 + 可变性
* 可版本化、可审计、可复制

### 例子（抽象）

* RiskTolerance ∈ [0.2 – 0.4]
* HumorDensity ∈ [0.1 – 0.3]
* ExplorationBias ∈ Dirichlet(…)
* FoodPreference → Flavor × Culture × Health manifold

> **一句定位**：
> *Persona Genome 决定“我倾向于什么，但不决定具体选什么”。*

---

## L3 — Persona Expression

**（表达层 / Stochastic Projection Layer）**

### 职责

* 将 Persona Genome 的“倾向空间”**投影成具体选择**
* 在**严格边界内引入随机性**
* 保证“像一个人，但不失控”

### 核心机制

* 有种子随机（seeded stochastic sampling）
* 时间桶稳定性（短期一致，长期可变）
* 叙事与语气渲染

### 输出形式

* 偏好答案（“我更可能喜欢 X 这类”）
* 行为选择（先问 vs 先答）
* 风格选择（简洁 / 解释 / 幽默）

> **一句定位**：
> *Persona Expression 决定“在允许的范围内，我这次具体怎么表现”。*

---

## 四层关系一句话总结（非常重要）

> **Persona Engine** 决定 *要不要用人格*
> **Persona Core** 决定 *我是不是同一个人*
> **Persona Genome** 决定 *我能偏向哪里*
> **Persona Expression** 决定 *这次落在哪个点*

这是一个**从“治理 → 约束 → 生成”的标准系统分层**，不是噱头。

---

## 为什么这个架构非常稳（实话）

1. **工程上可控**

   * 每一层都能单独测试、冻结、回放
2. **哲学上不过界**

   * 没有“自我意识”声明风险
3. **产品上好解释**

   * “这是人格驱动，不是事实判断”
4. **未来可扩展**

   * 可以加 Memory / Learning / Social Adaptation，不破坏原层级

