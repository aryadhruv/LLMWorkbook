---
layout: page
title: GPT4All
permalink: /docs/providers/gpt4all/
---

# LLMWORKBOOK Provider - GPT4ALL

Each provider function uses specific keys from the configuration’s `options` dictionary. In addition to these, you can also set a `system_prompt` (outside of `options`) and—where applicable—an API key (for OpenAI). Below are the options available for each provider.

---

### 1. GPT4ALL Provider (`call_llm_gpt4all`)

**Configuration Keys in `options`:**

- **`model`**  
  - **Type:** `str`  
  - **Description:** Specifies the model to use.  
  - **Default Behavior:** Defaults to `"default-model"` if not provided.

- **`max_tokens`**  
  - **Type:** `int`  
  - **Description:** Sets the maximum number of tokens to generate in the response.

- **`temperature`**  
  - **Type:** `float` or `int`  
  - **Description:** Controls the randomness and creativity of the generated output.

**Additional Configurations (Outside `options`):**

- **`system_prompt`**  
  - **Description:** A system-level prompt that is added before the user prompt in the message list.

- **`url` (Parameter)**  
  - **Description:** The endpoint URL for the GPT4ALL server. Defaults to `"http://localhost:4891"` if not provided.

---
