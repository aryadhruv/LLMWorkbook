---
layout: page
title: Examples
permalink: /examples/
---

# Code Examples

Practical examples demonstrating LLMWorkbook usage with different providers and data formats.

## LLM Provider Examples

### [🤖 OpenAI Example](https://github.com/aryadhruv/LLMWorkbook/blob/main/Examples/Example%20OpenAI.py)
Basic OpenAI GPT integration with configuration and usage.

### [🧠 Anthropic Example](https://github.com/aryadhruv/LLMWorkbook/blob/main/Examples/Example%20Anthropic.py)
Claude integration with Anthropic's API for conversational AI.

### [🏠 Ollama Example](https://github.com/aryadhruv/LLMWorkbook/blob/main/Examples/Example%20Ollama.py)
Local Ollama deployment and usage.

### [🔧 GPT4All Example](https://github.com/aryadhruv/LLMWorkbook/blob/main/Examples/Example%20GPT4ALL.py)
Local GPT4All integration for offline processing.

## Advanced OpenAI Features

### [📋 Response Format](https://github.com/aryadhruv/LLMWorkbook/blob/main/Examples/Example%20OpenAI%20Response%20Format.py)
Structured output formatting and response handling.

### [📄 JSON Response Unpacked](https://github.com/aryadhruv/LLMWorkbook/blob/main/Examples/Example%20OpenAI%20JSON%20Response%20Unpacked.py)
JSON parsing utilities and data extraction.

## Data Format Examples

### [📊 DataFrames](https://github.com/aryadhruv/LLMWorkbook/blob/main/Examples/Example%20DataFrames.py)
Working with pandas DataFrames and LLM integration.

### [📈 Excel](https://github.com/aryadhruv/LLMWorkbook/blob/main/Examples/Example%20Excel.py)
Excel workbook processing and manipulation.

### [🔢 Arrays](https://github.com/aryadhruv/LLMWorkbook/blob/main/Examples/Example%20Arrays.py)
Multi-dimensional array handling and processing.

## Processing Patterns

### [⚡ Batch Processing](https://github.com/aryadhruv/LLMWorkbook/blob/main/Examples/Example%20Batch%20Processing.py)
Efficient batch operations for large datasets.

### [🔄 PromptSeries](https://github.com/aryadhruv/LLMWorkbook/blob/main/Examples/Example%20PromptSeries.py)
Sequential prompt execution and workflow management.

### [🧹 Sanitize Prompts](https://github.com/aryadhruv/LLMWorkbook/blob/main/Examples/Example%20Sanitize%20Prompts.py)
Input cleaning and validation utilities.

## Quick Start Pattern

Most examples follow this workflow:

```python
from llmworkbook import LLMConfig, LLMRunner, LLMDataFrameIntegrator

# 1. Configure your LLM provider
config = LLMConfig(
    provider="openai",  # or "anthropic", "ollama", "gpt4all"
    system_prompt="Your system prompt here",
    options={"model": "gpt-4o-mini", "temperature": 0.7}
)

# 2. Create runner
runner = LLMRunner(config)

# 3. Process your data
integrator = LLMDataFrameIntegrator(runner=runner, df=your_dataframe)
result = integrator.add_llm_responses(
    prompt_column="input_column",
    response_column="output_column",
    async_mode=True
)
````

## Quick Links

- [🏠 Home](/)
- [💡 Examples]({{ site.baseurl }}/examples/)
- [📚 GitHub Docs](https://github.com/aryadhruv/LLMWorkbook/tree/main/docs)
- [🐛 Issues](https://github.com/aryadhruv/LLMWorkbook/issues)
