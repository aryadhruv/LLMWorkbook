# **LLMWorkbook**

[![CodeQL Advanced](https://github.com/aryadhruv/LLMWorkbook/actions/workflows/codeql.yml/badge.svg)](https://github.com/aryadhruv/LLMWorkbook/actions/workflows/codeql.yml)
[![Quality Scans](https://github.com/aryadhruv/LLMWorkbook/actions/workflows/Quality%20Check.yml/badge.svg)](https://github.com/aryadhruv/LLMWorkbook/actions/workflows/Quality%20Check.yml)
[![Tests](https://github.com/aryadhruv/LLMWorkbook/actions/workflows/test.yml/badge.svg)](https://github.com/aryadhruv/LLMWorkbook/actions/workflows/test.yml)
[![PyPI Downloads](https://static.pepy.tech/badge/llmworkbook)](https://pepy.tech/projects/llmworkbook)
<img src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json" alt="Ruff linter" href="https://github.com/astral-sh/ruff" />
<img src="https://img.shields.io/badge/linting-pylint-yellowgreen" alt="Pylint linter" href="https://github.com/pylint-dev/pylint" />  <img src="https://img.shields.io/badge/code%20style-black-000000.svg" alt="Code Style" href="https://github.com/ambv/black" />

"Effortlessly harness the power of LLMs on Excel and DataFrames—seamless, smart, and efficient!"

**LLMWorkbook** is a Python package designed to seamlessly integrate Large Language Models (LLMs) into your workflow with tabular data, be it Excel, CSV, DataFrames/Arrays. This package allows you to easily configure an LLM, send prompts **row-wise** from any tabular datasets, and store responses back in the DataFrame with minimal effort.

## **Documentation Website**

**[Visit our complete documentation site →](https://aryadhruv.github.io/LLMWorkbook/)**

For comprehensive guides, examples, and API reference, visit our dedicated documentation website.

---

## **Features**
- Easily map LLM responses to a specific column in a pandas DataFrame, Excel, CSV.
- Run list of prompts easily.
- Get started with easy to follow Examples


---

## LLMWorkbook v1.4.3 🦦:
✔ New OpenAI Responses Endpoint

---

## **Installation**

Install the package from GitHub:

```bash
    pip install llmworkbook
```

---

## **Quick Start**

---

### **Wrapper Utilities for LLM Preparation**

`LLMWorkbook` provides wrapper utilities to prepare various data formats for LLM consumption. These utilities transform input data into a format suitable for LLM processing, ensuring consistency and compatibility.
These wrapper methods can handle popular data sources like Excel (xlsx), CSV, Pandas DataFrames, multi dimensional arrays.

*See Examples for details. - [Github - Examples](https://github.com/aryadhruv/LLMWorkbook/tree/main/Examples)*

### Providers Supported -
* [OpenAI](docs/Providers/OpenAI.md)
* [Gpt4All](docs/Providers/Gpt4All.md)
* [Ollama](docs/Providers/Ollama.md)


---

### **1. Import the Package**

```python
import pandas as pd
from llmworkbook import LLMConfig, LLMRunner, LLMDataFrameIntegrator
```

### **2. DataFrame**

```python
# Provide a dataframe, the usual
df = pd.DataFrame(data)
```

### **3. Configure the LLM**

```python
config = LLMConfig(
    provider="openai",
    system_prompt="Process these Data rows as per the provided prompt",
    options={
        "model": "gpt-4o-mini",
        "temperature": 1,
        "max_tokens": 1024,
    },
)
```

### **4. Create a Runner and Integrate**

```python
runner = LLMRunner(config)
integrator = LLMDataFrameIntegrator(runner=runner, df=df)
```

### **5. Add LLM Responses to DataFrame**

```python
updated_df = integrator.add_llm_responses(
    prompt_column="prompt_text",
    response_column="llm_response",
    async_mode=False  # Set to True for asynchronous requests
)

```

Example code is available in the Git Repository for easy reference.

---
## **Future Roadmap**

- Add support for more LLM providers (Google VertexAI, Cohere, Groq, MistralAI).
- Add an interface frontend for low code applications.
- Implement rate-limiting and token usage tracking.
- Summarized history persisted across session to provide quick context for next session.


## Extended Documentation

Detailed documentation for each module is available in the [Documentation](docs) file.
- [Wrapping Data](docs/wrapping.md) file.
- [Providers](docs/Providers/) -
    [OpenAI](docs/Providers/OpenAI.md)
    [Gpt4All](docs/Providers/Gpt4All.md)
    [Ollama](docs/Providers/Ollama.md)
- [CLI Useage](docs/CLI%20Usage.md) file.
- [LLMDataFrameIntegrator - Row/Batch Processing](docs/Batch%20and%20Row%20Processing.md)



## **Links**

[Homepage](https://github.com/aryadhruv/LLMWorkbook)
[Repository](https://github.com/aryadhruv/LLMWorkbook)
[Documentation](https://github.com/aryadhruv/LLMWorkbook/tree/main/docs)
[Examples](https://github.com/aryadhruv/LLMWorkbook/tree/main/Examples)
[Bug Tracker](https://github.com/aryadhruv/LLMWorkbook/issues)
[Issues](https://github.com/aryadhruv/LLMWorkbook/issues)


