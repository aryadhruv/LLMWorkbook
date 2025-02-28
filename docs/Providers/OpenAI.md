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

**Additional OpenAI API Parameters**
Description: Any valid OpenAI API parameter (e.g., max_tokens, top_p, frequency_penalty, etc.) can be provided via options. This ensures full control over the API request without modifying the function.

Example -
```
config = {
    "options": {
        "model": "gpt-4o-mini",
        "temperature": 0.7,
        #Additional Parameter as needed
        "max_tokens": 500,
        "top_p": 0.9,
        "frequency_penalty": 0.5
        #Output format
        'response_format' : ...,
    },
'''

- **`api_key`**  
  - **Description:** Your OpenAI API key. If not provided in the config, the code will attempt to read it from the environment variable `OPENAI_API_KEY`.

---
