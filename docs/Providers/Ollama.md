---
layout: page
title: Ollama
permalink: /docs/providers/ollama/
---

# LLMWORKBOOK Provider Ollama

Each provider function uses specific keys from the configuration’s `options` dictionary. In addition to these, you can also set a `system_prompt` (outside of `options`) and—where applicable—an API key (for OpenAI). Below are the options available for each provider.

---

### 1. Ollama Provider (`call_llm_ollama`)

**Configuration Keys in `options`:**

- **`model`**  
  - **Type:** `str`  
  - **Description:** Specifies the model to use.  
  - **Default Behavior:** Defaults to `"default-model"` if not provided.

- **`suffix`**  
  - **Type:** (Depends on your usage; typically `str`)  
  - **Description:** An optional string appended to the generated output.

- **`images`**  
  - **Type:** (Varies)  
  - **Description:** Option to include or handle image data alongside text prompts.

- **`format`**  
  - **Type:** `str`  
  - **Description:** Specifies the format of the output.

- **`options`**  
  - **Type:** Typically a `dict` (or other appropriate type)  
  - **Description:** A nested dictionary for additional, provider-specific configurations.

- **`system`**  
  - **Type:** `str`  
  - **Description:** May provide additional system-level configuration beyond the primary `system_prompt`.

- **`template`**  
  - **Type:** `str`  
  - **Description:** A template string that can format the prompt or response in a specific manner.

- **`stream`**  
  - **Type:** `bool`  
  - **Description:** If `True`, enables streaming responses rather than a single complete response.  
  - **Default:** `False`

- **`raw`**  
  - **Type:** (Varies)  
  - **Description:** An option to request raw output (formatting or additional data) from the provider.

- **`keep_alive`**  
  - **Type:** `bool`  
  - **Description:** If `True`, maintains a persistent connection with the server for subsequent requests.

- **`context`**  
  - **Type:** Typically `str` or `dict`  
  - **Description:** Additional context or metadata that can be sent along with the prompt.

**Additional Configurations (Outside `options`):**

- **`system_prompt`**  
  - **Description:** A prompt that is sent as a system-level message prior to the user prompt.

- **`url` (Parameter)**  
  - **Description:** The endpoint URL for the Ollama server. If not provided when calling the function, it defaults to `"http://localhost:11434"`.

---
