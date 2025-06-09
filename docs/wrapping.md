---
layout: page
title: Data Wrapping
permalink: /docs/wrapping/
---

# LLMWORKBOOK WRAPPERS

This feature provides tools to transform your data into a format ready for Large Language Models (LLMs). It offers three concrete implementations to handle different data source types:

1. **`WrapDataFrame`** – For transforming a **pandas DataFrame**.
2. **`WrapDataArray`** – For transforming a **2D array-like structure** (e.g., a NumPy array or a list of lists).
3. **`WrapPromptList`** – For transforming a **list of prompts** (a 1D list of strings).

---

## Module Overview

The module is designed to wrap each row of data into an XML-like structure that LLMs can easily consume. For every row, the following transformation is applied:
- **Data columns** are wrapped into a `<data>` tag containing individual `<cell>` (or custom tag names) elements.
- The **prompt** is wrapped into a `<prompt>` tag.
- The wrapped data and prompt are concatenated to produce the final output.

The module also provides utility methods to preview the transformed data and export it to CSV, JSON, or Excel formats.

---

## Classes and Usage

### 1. BaseLLMWrapper
This is an abstract class that provides the core functionality:
- **Provided Methods:**
  - `wrap()`: Returns the LLM-ready DataFrame.
  - `transform_and_export()`: Exports the transformed DataFrame to a file (supports CSV, JSON, and Excel).
  - `preview()`: Prints a preview of the wrapped data.
---

### 2. WrapDataFrame

#### Description
`WrapDataFrame` is used when your data is in a pandas DataFrame. It allows you to:
- Specify which column contains the prompt.
- Optionally define a subset of data columns to include.
- Optionally use individual column headers as XML tags instead of generic `<cell>` tags.

#### Parameters
- **`df`** (`DataFrame`): The input DataFrame.
- **`prompt_column`** (`str`): The column name in `df` that contains the prompt.  
  *Default:* `"prompt_column"`
- **`data_columns`** (`Optional[List[str]]`): A list of column names to wrap as data. If not provided, all columns except the prompt column are used.
- **`use_column_header`** (`bool`): If `True`, each cell is wrapped with its column header as the tag name.  
  *Default:* `False`
- **`column_header_index`** (`int`):  Row Index for applying column headers.
  *Default:* `0`

#### Example

```python
import pandas as pd
from llmworkbook import WrapDataFrame

# Sample DataFrame with data and prompt columns
df = pd.DataFrame({
    'data1': [10, 20, 30],
    'data2': ['A', 'B', 'C'],
    'prompt_column': ["Prompt 1", "Prompt 2", "Prompt 3"]
})

# Initialize the wrapper
wrapper_df = WrapDataFrame(
    df,
    prompt_column='prompt_column',     
    data_columns=['data1', 'data2'],     
    use_column_header=True,              
    column_header_index=0            
)

# Generate the wrapped DataFrame
wrapped_output_df = wrapper_df.wrap()

# Preview the result
wrapper_df.preview()
```

---

### 3. WrapDataArray

#### Description
`WrapDataArray` is designed to work with 2D array-like structures such as NumPy arrays or lists of lists. It:
- Converts the input array into a DataFrame for easier manipulation.
- Uses a specified column index for the prompt.
- Optionally selects which columns to wrap as data.

#### Parameters
- **`arr`** (`Union[np.ndarray, list]`): The input 2D array.
- **`prompt_index`** (`int`): The column index in the array that contains the prompt.  
  *Default:* `0`
- **`data_indices`** (`Optional[List[int]]`): A list of column indices to wrap as data. If not provided, all columns except the prompt column are used.

#### Example

```python
import numpy as np
from llmworkbook import WrapDataArray 

# Sample 2D array (or list of lists)
data_array = np.array([
    ["Prompt A", 100, 200],
    ["Prompt B", 300, 400],
    ["Prompt C", 500, 600]
])

wrapper_array = WrapDataArray(
    data_array,
    prompt_index=0,        
    data_indices=[1, 2]    
)

# Generate the wrapped output DataFrame
wrapped_output_array = wrapper_array.wrap()

# Preview the wrapped output
wrapper_array.preview()
```

---

### 4. WrapPromptList

#### Description
`WrapPromptList` is a simple wrapper for when you only have a list of prompts (i.e., no associated data columns). It creates an empty DataFrame for data (to maintain row alignment) and wraps each prompt.

#### Parameters
- **`prompts`** (`List[str]`): A list of prompt strings.

#### Example

```python
from llmworkbook import WrapPromptList 

# Sample list of prompts
prompt_list = [
    "How is the weather today?",
    "What is the capital of France?",
    "Summarize the following article."
]

# Initialize the wrapper
wrapper_prompts = WrapPromptList(prompt_list)

# Generate the wrapped DataFrame
wrapped_output_prompts = wrapper_prompts.wrap()

# Preview the wrapped output
wrapper_prompts.preview()
```

---

## Common Methods

All wrapper classes (by inheritance) provide the following methods:

- **`wrap()`**  
  Transforms the data/prompt input into a single-column DataFrame with wrapped XML-like content.

- **`transform_and_export(file_path: str, file_format: str = "excel")`**  
  Transforms the data and exports it to a file.  
  **Parameters:**
  - `file_path`: Path to save the output.
  - `file_format`: Output format – choose between `"csv"`, `"json"`, or `"excel"`.

- **`preview(n: int = 5)`**  
  Prints the first `n` rows of the wrapped output for a quick look.

#### Example: Exporting Wrapped Data

```python
# Assume wrapper_df is an instance of one of the wrapper classes (e.g., WrapDataFrame)
wrapper_df.transform_and_export("wrapped_data.xlsx", file_format="excel")
```

