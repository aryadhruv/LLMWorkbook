# LLMWORKBOOK Provider OpenAI

Each provider function uses specific keys from the configuration’s `options` dictionary. In addition to these, you can also set a `system_prompt` (outside of `options`) and—where applicable—an API key (for OpenAI). Below are the options available for each provider.

---

### 1. OpenAI Provider (`call_llm_openai`)

**Configuration Keys in `options`:**

- **`model` (earlier 'model_name')**  
  - **Type:** `str`  
  - **Description:** Specifies the model to use for generating responses (e.g., `"gpt-4o-mini"`).  
  - **Default Behavior:** If not provided, the code defaults to `"gpt-4o-mini"`.

- **`temperature`**  
  - **Type:** `float` or `int`  
  - **Description:** Controls the randomness of the output. A higher temperature produces more varied results.

**Additional Configurations (Outside `options`):**

- **`api_key`**  
  - **Description:** Your OpenAI API key. If not provided in the config, the code will attempt to read it from the environment variable `OPENAI_API_KEY`.

---
