### 🏛️ Phase 6: Evolution & Salience Module Charter (Restrained)

**Status:** PROPOSAL / ENGINEERING SPEC
**Layer:** L1+ (Plugin) / L3- (Filter)
**Core Principle:** 人格必须是“外显”的变量，而非“内隐”的逻辑污染。

---

#### 1. 记忆映射规则：显著性加权 (Salience Weighting)
*   **❌ 错误路径 (Ingestion Bias)**: 在存入记忆时根据性格修改事实。 (会导致系统不可审计)
*   **✅ 正确路径 (Retrieval Salience)**: 
    *   L0 始终存储 100% 原始、中立的 Context。
    *   在 Retrieval（检索）阶段，L1/L3 根据当前人格位点，对检索到的向量结果进行 **Salience Weighting (显著性加权)**。
    *   *结果*：悲观人格在检索时，会自动调高带有“风险”标签记录的 Top-K 权重。

#### 2. 关系定义：表达带宽解锁 (Bandwidth Gating)
*   **❌ 错误路径 (Personality Morphing)**: 亲密度越高，性格变得越极端。 (会导致 OOD/越狱风险)
*   **✅ 正确路径 (Expression Bandwidth)**: 
    *   亲密度（Intimacy）被视为一个 **Low-Pass Filter (低通滤波器)**。
    *   **Low Intimacy**: 严格过滤 L3 输出，强制使用中立、礼貌、标准的模版词汇。
    *   **High Intimacy**: 增大 L3 采样方差，允许出现自我披露、非正式语料、甚至基于 L2 设定的特定情绪波动。
    *   *准则*：亲密度改变“说话的力道”，不改变“说话的逻辑”。

#### 3. 演化约束：不可杂交域 (Non-Recombinable Axes)
在执行 Genetic Recombination（基因杂交）时，以下位点禁止交叉或突变：
*   **Truth-Alignment Loci**: 任何涉及逻辑边界、安全红线的部分（由 L2 Charter 强制锁定）。
*   **Consistency Anchor**: 若两个 Parent 基因在核心认知上存在 180 度对立，杂交算法必须强制进行“显性/隐性”选择，而非取平均值（防止生成矛盾人格）。

#### 4. 业务落地优先级 (MVP Hierarchy)
1.  **Topic Attractors (话题吸引子)**: 优先级最高。纯粹的分布偏移，工程风险接近零。
2.  **Expression Gating (表达带宽)**: 优先级中。属于 L3 的输出控制。
3.  **Salience Retrieval (显著性检索)**: 优先级中。依赖 RAG 架构接入。
4.  **Generic Recombination (离线杂交)**: 优先级低。仅作为实验室功能。

---

### 💡 架构师点评 (Architect's Note)

这次修正将系统从“模拟生命”拉回了“模拟人格表达”。
我们保留了 **“看起来有生命”** 的所有外显特征，但切断了它 **“污染逻辑基座”** 的所有物理路径。
这是一个 **“可审计的人格 (Auditable Persona)”**。
