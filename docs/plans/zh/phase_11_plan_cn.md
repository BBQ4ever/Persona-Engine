# Phase 11 开发计划：元认知自我修正 (Meta-Cognitive Self-Correction)

## 1. 阶段目标
将 Persona Engine 从一个“反应式系统”升级为“自我进化实体”。AI 将分析其自身的行为历史（`Reflection Journal`），识别风格偏离或情感失调，并主动调整其 DNA 参数。

## 2. 核心模块

### 2.1 反思调度器 (`src/l4_memory/reflection.py`)
- **职责**：一个定期触发“反思周期”的后台服务。
- **逻辑**：
    - 从 `PersonaReflectionJournal` 中读取最近 N 条记录。
    - 将这些记录封装为“时间叙事”。
    - 将叙事发送给 LLM，并赋予其“元观察者”角色进行分析。

### 2.2 性格自愈接口 (`src/app_integration.py` 升级)
- **方法**：`propose_dna_mutation()`
- **动作**：根据反思结果，建议微调特定的 DNA 位点（例如：“最近 10 轮对话中我过于激进，建议将 `assertiveness` 默认值下调 0.05”）。

### 2.3 治理护栏 (`src/l1_core/governance.py` 升级)
- **校验**：在应用任何变异前，根据 `GOVERNANCE_CHARTER`（治理宪章）进行约束校验。
- **安全性**：防止由于变异失控导致的人格崩塌。

### 2.4 可视化：反思看板
- 在 Dashboard 中展示 AI 的“反思推理过程”。
- 增加“进化历史”日志，展示 DNA 变动的具体时间点和缘由。

## 3. 实施步骤

1.  **第一步：观察者提示词 (Observer Prompt)**
    - 在 `PromptAugmenter` 中创建专注于行为分析的模板。
2.  **第二步：自动化反思循环**
    - 在 `PersonaService` 中实现 `perform_reflection()` 方法。
    - 测试：模拟一系列交互，检查 AI 是否能识别出自己的情绪模式。
3.  **第三步：变异逻辑实现**
    - 实现动态更新 `self.genome` 的逻辑。
    - 将进化后的基因组保存为新的“内核快照”。
4.  **第四步：UI 集成**
    - 更新 Dashboard 中的 `Reflection Journal` 区域，展示 AI 的自我剖析。

## 4. 验证指标
- 创建 `tests/test_phase_11.py`。
- 验证流程：交互历史 -> 自我反思 -> DNA 更新 -> 下一轮提示词优化。
