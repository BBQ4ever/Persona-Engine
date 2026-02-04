# 🛠️ How to Use: Integrating Persona Engine

This guide explains how to integrate the Persona Engine into your existing AI application or chatbot pipeline.

---

## 1. Basic Integration Flow

The engine acts as a **Prompt Pre-processor**. Instead of sending raw user input to an LLM, you pass it through the engine to generate a "Personality-Augmented Payload."

### The `PersonaService` Wrapper
We provide a high-level wrapper in `src/app_integration.py` for easy use:

```python
from src.app_integration import PersonaService

# 1. Initialize the service (loads L2 Genome and L0-L1-L3 logic)
service = PersonaService(genome_path="path/to/your_genome.json")

# 2. Process an interaction
user_text = "Hello, who are you?"
payload = service.get_llm_payload(user_text, session_id="user_unique_id")

# 3. The 'payload' is now a standard OpenAI-compatible dictionary
# messages = [
#   {"role": "system", "content": "... (Augmented personality instructions) ..."},
#   {"role": "user", "content": "Hello, who are you?"}
# ]
```

---

## 2. Advanced Controls

### A. Managing Intimacy (Relationship Depth)
You can manually adjust the intimacy level to unlock different "Expression Bandwidths" (Phase 6 feature).

```python
# Unlocks more expressive/informal language
service.fsm.intimacy_level = 0.8 
```

### B. Scenario Awareness (L0)
The engine automatically detects if the user is asking for a **FACT** or **LOGIC**. 
- If detected, `influence_level` collapses to **0.1**.
- The resulting System Prompt will automatically strip out jokes, metaphors, and slang.

### C. Evolution & State (L1)
The persona evolves automatically as you record interactions:
```python
# The engine records interactions internally
# After 50 interactions, state shifts from STABILIZING to STABLE.
```

---

## 3. Customizing Your Persona (L2 DNA)

To create a new persona, edit or create a JSON file following the **L2 Loci Schema**:

```json
{
  "id": "humor_density",
  "category": "style",
  "distribution": {
    "type": "range",
    "values": { "min": 0.5, "max": 0.9, "default": 0.7 }
  }
}
```

---

## 4. Running the Dashboard
For real-time debugging and visualization:
1. `cd dashboard`
2. `npm run dev`
3. Adjust sliders and click **GENERATE** to see how DNA sampling affects the output strings.

---

## 🏁 Summary for Production
- **Use the Engine** to generate the `system` message.
- **Use your LLM API** to generate the final completion.
- **Trace everything** via the GECCE Event Log for auditing personality consistency.
