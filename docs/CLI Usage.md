---
layout: page
title: CLI Usage
permalink: /docs/cli-usage/
---

# LLMWORKBOOK CLI Usage

`LLMWorkbook` provides a command-line interface (**CLI**) for wrapping data and testing LLM connectivity. This makes it easy to process DataFrames, arrays, and prompt lists without writing additional code.

#### **Installation**
The CLI is installed automatically when you install `LLMWorkbook` via Poetry:

```bash
poetry install
```

Once installed, you can use the `llmWorkbook` command.

#### **Available Commands**
```bash
llmworkbook wrap_dataframe <input_file> <output_file> <prompt_column> <data_columns>
llmworkbook wrap_array <input_file> <output_file> <prompt_index> <data_indices>
llmworkbook wrap_prompts <prompts_file> <output_file>
llmworkbook test <api_key> [--model_name gpt-3.5-turbo]
llmworkbook version
```

#### **Examples**
- **Wrap a DataFrame:**
  ```bash
  llmworkbook wrap_dataframe sample.xlsx wrapped_output.csv prompt "Reviews,Language"
  ```

- **Wrap a 2D Array (JSON file input):**
  ```bash
  llmworkbook wrap_array array_data.json wrapped_output.csv 0 1,2
  ```

- **Wrap a List of Prompts:**
  ```bash
  llmworkbook wrap_prompts prompts.txt wrapped_output.csv
  ```

- **Test LLM Connectivity:**
  ```bash
  llmworkbook test YOUR_API_KEY --model gpt-4
  ```

- **See Version of package:**
  ```bash
  llmworkbook version
  ```
This CLI allows you to quickly process data and validate your LLM connection without modifying code. 🚀
