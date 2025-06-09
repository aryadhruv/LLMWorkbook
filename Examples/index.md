---
layout: page
title: Examples
permalink: /examples/
---

# Code Examples

This section contains practical examples demonstrating how to use LLMWorkbook with different providers and data formats.

## Provider Examples

### LLM Providers
- [OpenAI Example](Example%20OpenAI.py) - Basic OpenAI GPT integration
- [Anthropic Example](Example%20Anthropic.py) - Claude integration
- [Ollama Example](Example%20Ollama.py) - Local Ollama deployment
- [GPT4All Example](Example%20GPT4ALL.py) - Local GPT4All usage

### Advanced OpenAI Features
- [Response Format](Example%20OpenAI%20Response%20Format.py) - Structured output formatting
- [JSON Response Unpacked](Example%20OpenAI%20JSON%20Response%20Unpacked.py) - JSON parsing utilities

## Data Format Examples

### Data Sources
- [DataFrames](Example%20DataFrames.py) - Working with pandas DataFrames
- [Excel](Example%20Excel.py) - Excel workbook processing
- [Arrays](Example%20Arrays.py) - Multi-dimensional array handling

## Processing Examples

### Workflow Patterns
- [Batch Processing](Example%20Batch%20Processing.py) - Efficient batch operations
- [PromptSeries](Example%20PromptSeries.py) - Sequential prompt execution

### Utilities
- [Sanitize Prompts](Example%20Sanitize%20Prompts.py) - Input cleaning and validation

## Quick Start

Most examples follow this pattern:

```python
from llmworkbook import LLMConfig, LLMRunner, LLMDataFrameIntegrator

# 1. Configure provider
config = LLMConfig(provider="openai", ...)

# 2. Create runner
runner = LLMRunner(config)

# 3. Process data
integrator = LLMDataFrameIntegrator(runner=runner, df=df)
result = integrator.add_llm_responses(...)
```

Browse the individual files above to see complete, runnable examples for your specific use case.