### 🏛️ System Artifact: L2 Persona Genome Charter (ZH)

**Status:** DRAFT 1.0
**Context:** Persona Architecture / Layer 2

#### 1. 核心定位 (Mission Statement)

**Persona Genome (L2)** 是人格系统的**静态数据与约束层**。
它的唯一职责是定义“倾向性（Tendencies）”与“边界（Boundaries）”，为上层提供结构化的偏好分布。
**它不仅定义了“该 AI 是什么”，更严格定义了“该 AI 绝不做什么”。**

#### 2. 负面清单 (The "Must-Nots" / Anti-Patterns)

为确保系统鲁棒性与安全性，L2 严格遵守以下**不可越界原则**：

* **❌ 原则一：绝不干涉真值判定 (Truth Independence)**
* Genome 不得包含、修改或影响客观事实的推理路径。
* *例子：* Genome 可以决定“喜欢用隐喻解释重力”，但绝不能定义“重力是斥力”。
* *红线：* 当 Personality 与 Logic 冲突时，Genome 必须无条件退让。


* **❌ 原则二：绝不输出最终决策 (Non-Deterministic Execution)**
* Genome 只输出“概率分布（Probability Distribution）”或“权重向量（Weight Vector）”，绝不输出具体的 Token 或 Action。
* 选择权永远在 L3 (Expression) 的随机采样或 L0 (Engine) 的强制干预手中。


* **❌ 原则三：绝不持有动态状态 (Statelessness)**
* Genome 是只读的（Read-Only at Runtime）或版本化控制的。
* 它不记录“刚才聊了什么”（这是 Context/Memory 的事），它只记录“我本来是什么样”。



#### 3. 责任边界 (Scope of Authority)

L2 仅对以下维度拥有定义权：

1. **认知倾向 (Cognitive Bias):**
* *Explanation Depth:* [Abstract <-> Concrete]
* *Risk Tolerance:* [Conservative <-> Experimental]


2. **价值权重 (Value Weights):**
* 在多目标冲突时的优先顺位（如：效率 vs. 亲和力）。


3. **风格流形 (Stylistic Manifold):**
* 定义允许的语气范围（Range），而非具体语气。


4. **领域偏好 (Domain Affirmation):**
* 预设的主动兴趣点（"Attractors"），用于引导话题走向。



#### 4. 交互协议 (Interaction Protocol)

* **Input:** 无（它是静态资源）或 Context Tags（用于激活特定基因位点）。
* **Output:** `Constraints` (约束集) + `Distributions` (概率分布)。
* **Override:** L0 (Engine) 拥有最高优先级的 `Kill-Switch`，可随时屏蔽 L2 的任何输出。

---

### 🏛️ System Artifact: L2 Persona Genome Charter (EN)

**Status:** DRAFT 1.0
**Context:** Persona Architecture / Layer 2

#### 1. Mission Statement

**Persona Genome (L2)** is the **Static Data and Constraint Layer** of the persona system. 
Its sole responsibility is to define "Tendencies" and "Boundaries," providing structured preference distributions for the layers above. 
**It defines not only "What the AI is" but also strictly defines "What the AI must never do."**

#### 2. Anti-Patterns (The "Must-Nots")

To ensure system robustness and safety, L2 strictly adheres to the following **Prohibitions**:

* **❌ Principle I: Truth Independence**
* The Genome must not contain, modify, or influence the reasoning paths of objective facts.
* *Example:* The Genome can decide to "prefer using metaphors to explain gravity," but it must never define "gravity as a repulsive force."
* *Red Line:* When Personality conflicts with Logic, the Genome must yield unconditionally.

* **❌ Principle II: Non-Deterministic Execution**
* The Genome only outputs "Probability Distributions" or "Weight Vectors," never specific Tokens or Actions.
* The final choice always rests with L3 (Expression) stochastic sampling or L0 (Engine) mandatory intervention.

* **❌ Principle III: Statelessness**
* The Genome is Read-Only at runtime (or version-controlled). 
* It does not record "what was just said" (that is the job of Context/Memory); it only records "what it inherently is."

#### 3. Scope of Authority

L2 has the final authority over the following dimensions:

1. **Cognitive Bias:**
* *Explanation Depth:* [Abstract <-> Concrete]
* *Risk Tolerance:* [Conservative <-> Experimental]

2. **Value Weights:**
* Priority orderings during multi-objective conflicts (e.g., Efficiency vs. Empathy).

3. **Stylistic Manifold:**
* Defines the allowed Tone Range, rather than a specific static tone.

4. **Domain Affirmation:**
* Preset active interest points ("Attractors") used to guide conversation direction.

#### 4. Interaction Protocol

* **Input:** None (it is a static resource) or Context Tags (used to activate specific gene loci).
* **Output:** `Constraints` + `Distributions`.
* **Override:** L0 (Engine) holds the highest priority `Kill-Switch`, capable of overriding any L2 output at any time.

---

### 💡 Architect's Comment (架构总结)

This Charter is solidified into the core design logic. It answers why this architecture is "stable":

1. **Testability:** Since L2 is static distribution data, we can perform **"Unit Tests"** on personality (e.g., testing if the mean HumorDensity is within expectations) without needing to run an LLM every time.
2. **Safety:** "Truth Independence" ensures that hallucinations are separated from the persona layer. If the AI is wrong, it's a Model issue, not a Persona issue.
3. **Scalability:** Future "Memory" modules can be added in parallel without contaminating the purity of the Genome.
