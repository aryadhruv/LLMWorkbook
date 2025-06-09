---
layout: page
title: Examples
permalink: /examples/
---

# Code Examples

Practical examples demonstrating LLMWorkbook usage with different providers and data formats.

## LLM Provider Examples

### [🤖 OpenAI Example](Examples/Example OpenAI.py)
Basic OpenAI GPT integration with configuration and usage.

### [🧠 Anthropic Example](Examples/Example Anthropic.py)
Claude integration with Anthropic's API for conversational AI.

### [🏠 Ollama Example](Examples/Example Ollama.py)
Local Ollama deployment and usage.

### [🔧 GPT4All Example](Examples/Example GPT4ALL.py)
Local GPT4All integration for offline processing.

## Advanced OpenAI Features

### [📋 Response Format](Examples/Example OpenAI Response Format.py)
Structured output formatting and response handling.

### [📄 JSON Response Unpacked](Examples/Example OpenAI JSON Response Unpacked.py)
JSON parsing utilities and data extraction.

## Data Format Examples

### [📊 DataFrames](Examples/Example DataFrames.py)
Working with pandas DataFrames and LLM integration.

### [📈 Excel](Examples/Example Excel.py)
Excel workbook processing and manipulation.

### [🔢 Arrays](Examples/Example Arrays.py)
Multi-dimensional array handling and processing.

## Processing Patterns

### [⚡ Batch Processing](Examples/Example Batch Processing.py)
Efficient batch operations for large datasets.

### [🔄 PromptSeries](Examples/Example PromptSeries.py)
Sequential prompt execution and workflow management.

### [🧹 Sanitize Prompts](Examples/Example Sanitize Prompts.py)
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
```

## Links

- [📁 All Examples on GitHub](https://github.com/aryadhruv/LLMWorkbook/tree/main/Examples)
- [🏠 Home](/)
- [📚 Documentation](/documentation/)
- [🐛 Report Issues](https://github.com/aryadhruv/LLMWorkbook/issues)