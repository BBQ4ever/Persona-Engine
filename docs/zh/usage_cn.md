# 🛠️ 使用指南：集成 Persona Engine

本指南介绍了如何将 Persona Engine 集成到您现有的 AI 应用或聊天机器人流程中。

---

## 1. 基础集成流程

人格引擎充当 **“提示词预处理器”**。您不直接将原始用户输入发送给大模型，而是先将其通过引擎处理，生成“人格增强后的请求包”。

### `PersonaService` 包装类
我们在 `src/app_integration.py` 中提供了一个高级包装类，方便快速调用：

```python
from src.app_integration import PersonaService

# 1. 初始化服务（自动加载 L2 基因和 L0-L1-L3 逻辑）
service = PersonaService(genome_path="path/to/your_genome.json")

# 2. 处理一次交互
user_text = "嘿，你是谁？"
payload = service.get_llm_payload(user_text, session_id="user_unique_id")

# 3. 'payload' 现在是一个标准的 OpenAI 兼容字典
# messages = [
#   {"role": "system", "content": "... (由引擎生成的动态人格指令集) ..."},
#   {"role": "user", "content": "嘿，你是谁？"}
# ]
```

---

## 2. 深度控制

### A. 亲密度管理 (关系深度)
您可以手动调整亲密度，以解锁不同的“表达带宽”（Phase 6 功能）。
- **亲密度低**：AI 说话会显得礼貌而克制。
- **亲密度高**：AI 会释放更多个性。

```python
service.fsm.intimacy_level = 0.8  # 解锁更具表现力/非正式的语言
```

### B. 场景感知 (L0)
引擎会自动检测用户是否在询问 **事实** 或 **逻辑**。
- 如果检测到严谨场景，`influence_level` 会坍缩至 **0.1**。
- 生成的 System Prompt 会自动剥离冗余的笑话、隐喻或俚语，确保回答的专业性。

### C. 演进与状态 (L1)
人格会随着交互次数的增加而自动演化：
- 在 50 次交互后，状态会从 `STABILIZING`（趋于稳定）切换为 `STABLE`（稳定）。

---

## 3. 自定义人格 (L2 DNA)

要创建新的人格，请按照 **L2 Loci Schema** 创建 JSON 文件。您可以定义：
- **认知风格**：如“解释深度”。
- **表现风格**：如“幽默密度”。
- **话题吸引子**：如“对特定领域的爱好”。

---

## 4. 启动仪表盘
用于实时调试和可视化：
1. `cd dashboard`
2. `npm run dev`
3. 调整滑块并点击 **GENERATE**，观察 DNA 采样如何影响最终输出的指令。

---

## 🏁 生产环境总结
- **使用本引擎** 生成 `system` 指令。
- **使用您的 LLM API** 生成最终的回复。
- **通过 GECCE 事件日志** 追踪一切，并审计人格一致性。
