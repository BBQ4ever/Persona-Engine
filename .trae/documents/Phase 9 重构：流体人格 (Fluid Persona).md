# Phase 9 重构计划：从“RPG 职业切换”进化为“流体人格 (Fluid Persona)”

我很认同你的直觉。目前的 `ArchetypeManager` 确实像 RPG 游戏的“转职系统”（切换一个枚举，覆盖一套数值），这种离散的、硬编码的方式虽然简单，但缺乏真实人格的**连续性**和**深度**。

为了去除“二次元感”并解决“预设过多”的问题，我建议进行以下重构，将系统从**基于模板 (Template-Based)** 升级为 **基于向量 (Vector-Based)**。

## 核心理念转变
-   **旧模式 (Discrete Archetypes)**: 只有 4 种预设状态（A, B, C, D）。用户意图 -> 匹配最近的模板 -> 切换。
-   **新模式 (Fluid Stance)**: 这是一个连续的参数空间。用户意图 -> 计算目标姿态向量 -> 动态生成 DNA。

## 具体执行步骤

### 1. 去除硬编码 Enum (De-Gamification)
-   **动作**: 废弃 `ArchetypeType` 枚举类。
-   **替代**: 将现有的人格预设提取为独立的 JSON 配置文件 (`archetype_presets.json`)。
-   **好处**: 以后增加“毒舌老师”只需加一个 JSON 配置，不需要改代码，也不需要预设太多，按需加载即可。

### 2. 引入“姿态向量” (Stance Vector)
这是解决“预设过多”的关键。我们不再穷举所有可能的性格，而是定义 3-4 个**核心维度（元参数）**，由它们来驱动底层的几十个 DNA 位点。

建议引入 **R.W.C 模型** (临时命名) 作为中间层：
-   **Rigor (严谨度)**: 映射到 `logical_rigor`, `explanation_depth`, `conflict_strategy(analytical)`
-   **Warmth (温度)**: 映射到 `identity_signature`, `affect_baseline(P)`, `conflict_strategy(accommodating)`
-   **Chaos (熵/混乱度)**: 映射到 `humor_density`, `variability` (DNA 抖动), `topic_attractors`

**工作流变化**:
-   *原流程*: 意图识别 -> `Switch to ANALYTICAL_CHALLENGER`
-   *新流程*: 意图识别 -> `Adjust Stance(Rigor=+0.8, Warmth=-0.2)` -> 自动计算出底层 DNA。

### 3. 重构 `ArchetypeManager`
-   **新增 `calculate_genome_from_stance(rigor, warmth, chaos)`**: 实现从高层维度到底层 DNA 的映射算法。
-   **保留 `apply_preset`**: 仍然允许加载预设（如 "Analytical Challenger"），但它本质上只是 `Rigor=0.9, Warmth=0.1` 的一个别名快捷方式。
-   **实现平滑过渡**: 既然变成了向量计算，我们就可以实现真正的“渐变”（比如从严肃逐渐变得温和），而不是生硬的跳变。

## 下一步行动 (Action Plan)
1.  **创建配置**: 将 Python 中的字典硬编码迁移到 `src/l2_genome/presets/standard_archetypes.json`。
2.  **重写 Manager**: 修改 `ArchetypeManager`，支持加载外部 JSON 配置。
3.  **(可选) 实现向量映射**: 如果你同意 RWC 模型，我可以尝试写一个简单的映射器，自动根据 3 个维度生成 DNA。

这个方案会让系统感觉更像一个**有机的生物**，它会根据环境调整自己的“姿态”，而不是在几个固定的面具之间切换。你觉得这个方向如何？
