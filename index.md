---
layout: home
title: Home
---

<div align="center">
  <!-- Logo placeholder - add your logo to assets/images/logo.png -->
  <img src="assets/images/logo.png" alt="LLMWorkbook Logo" width="200" height="200" style="margin: 20px 0;" onerror="this.style.display='none'">
  
  <h1>LLMWorkbook</h1>
  
  <p><strong>Effortlessly harness the power of LLMs on Excel and DataFrames—seamless, smart, and efficient!</strong></p>
</div>

---

Welcome to the LLMWorkbook documentation site! This site provides comprehensive documentation for integrating Large Language Models with your tabular data workflows.

## Quick Navigation

- **[📖 Documentation](/documentation/)** - Complete documentation and guides
- **[🚀 Examples](/examples/)** - Real-world usage examples
- **[📦 Installation](#installation)** - Get started quickly
- **[🔧 Provider Setup](/documentation/#llm-providers)** - Configure LLM providers

## Installation

```bash
pip install llmworkbook
```

## Key Features

- ✅ **Easy DataFrame Integration** - Map LLM responses to DataFrame columns
- ✅ **Multiple LLM Providers** - OpenAI, Anthropic, Ollama, GPT4All support  
- ✅ **Async Processing** - High-performance batch operations
- ✅ **Rich Progress Tracking** - Beautiful console progress bars
- ✅ **CLI Interface** - Command-line tools included

## Quick Example

```python
from llmworkbook import LLMConfig, LLMRunner, LLMDataFrameIntegrator
import pandas as pd

# Configure LLM
config = LLMConfig(
    provider="openai",
    system_prompt="Analyze the data",
    options={"model": "gpt-4o-mini"}
)

# Process DataFrame
runner = LLMRunner(config)
integrator = LLMDataFrameIntegrator(runner=runner, df=your_df)

result = integrator.add_llm_responses(
    prompt_column="input_text",
    response_column="llm_output",
    async_mode=True
)
```

## Links

- [GitHub Repository](https://github.com/aryadhruv/LLMWorkbook)
- [PyPI Package](https://pypi.org/project/llmworkbook/)
- [Issue Tracker](https://github.com/aryadhruv/LLMWorkbook/issues)