# Persona Engine 技术报告 - Phase 7: 身份基座与风格锚点 (Identity Substrate)

## 1. 阶段目标
本阶段致力于将“身份”与“性别”等社会化属性从传统的硬编码标签（Hardcoded Labels）升级为动态的**风格偏置标量 (Stylistic Bias Scalar)**，在保证系统治理性的前提下，赋予 AI 细腻且一致的表达风格。

## 2. 核心实现项

### 2.1 身份特征位点化 (L2 Genome)
在基因组中引入了 `identity_signature` 位点。该位点不再通过叙事性语言定义，而是作为一个处于 `[0.0, 1.0]` 区间的连续量化特征：
- **0.0 - 0.4**: 男性化偏置（侧重断言、精简、逻辑直接）。
- **0.4 - 0.6**: 中性化偏置（侧重客观、平衡、绝对中立）。
- **0.6 - 1.0**: 女性化偏置（侧重协作、详尽、关系连接）。

### 2.2 风格滤波器设计 (L3 Expression)
重构了 `PromptAugmenter` 的映射流形（Manifold），将 `identity_signature` 作为采样后的终尾滤波器：
- **动态合成**：根据采样值动态注入“Linguistic Softeners”或“Direct Assertions”。
- **层级兼容**：确保风格锚点与 L2 的认知位点（如 `logical_rigor`）产生良性复合而非冲突。

### 2.3 治理宪章落库
正式将《治理与表达裁决章程》 (Governance Charter) 独立，明确了 **Expressive Hierarchy（表达层级）**。确保身份风格在面临 L0 场景变化或 L1 情感波动时，具有清晰的优先级裁决逻辑。

## 3. 技术洞察：从“声明”到“表现”
本阶段完成了一次关键的思维脱钩：
- **过去**：告诉 AI “你是一个女性/男性”，这容易导致刻板印象或 prompt 注入风险。
- **现在**：告诉 AI “采用一种协作且细节丰富的沟通风格”，这在工程上更可控，且能通过 L2 基因微调实现极致的语气拟合。

## 4. 交付物清单
- `src/l2_genome/sample_genome.json`: 更新 identity 位点。
- `src/l3_expression/prompt_augmenter.py`: 实现风格映射逻辑。
- `src/test_phase_7.py`: 完成多场景身份偏移验证。
- `docs/GOVERNANCE_CHARTER.md`: 发布项目“宪章”。
- `dashboard/main.js`: Web UI 同步支持身份位点可视化。

## 5. 下阶段预告: Phase 8 - 情感流形 (The Affective Core)
我们将引入 PAD 情绪模型，让 Persona 拥有实时波动的心理能量场。
