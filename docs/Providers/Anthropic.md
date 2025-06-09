# LLMWORKBOOK Provider Anthropic

Anthropic's Claude API has a distinct structure and accepts only specific parameters. This documentation explains how to configure and use the `call_llm_anthropic` function through the `LLMConfig` system in `llmworkbook`.

---

### 1. Anthropic Provider (`call_llm_anthropic`)

**Configuration Keys in `options`:**

* **`model`**

  * **Type:** `str`
  * **Required**
  * **Description:** Specifies the Claude model to use.
  * **Example Values:**

    * `"claude-3-opus-20240229"`
    * `"claude-3-sonnet-20240229"`
    * `"claude-3-haiku-20240307"`
  * **Default:** `"claude-3-sonnet-20240229"` (if not explicitly set)

* **`max_tokens`**

  * **Type:** `int`
  * **Required**
  * **Description:** Maximum number of tokens Claude can generate in the response.

* **`system_prompt`**

  * **Type:** `str`
  * **Optional (set outside `options`)**
  * **Description:** The system prompt guiding Claude's behavior. Passed as `system=...` in API call.


---

### ✅ Example Configuration

```python
from llmworkbook import LLMConfig

config = LLMConfig(
    provider="anthropic",
    system_prompt="You are a helpful assistant.",
    options={
        "model": "claude-3-haiku-20240307",
        "max_tokens": 512,
    }
)
```

---

### API Key

* **`api_key`**

  * Your Anthropic API key can be:

    * Provided explicitly via `config.api_key`, or
    * Fetched automatically from the environment variable: `ANTHROPIC_API_KEY`.

---
