# **sanitize_prompt Utility Documentation**

## **Overview**
The `sanitize_prompt` utility function in `LLMWorkbook` ensures that prompts passed to **wrappers** or **integrators** are **clean and secure** before being processed by an LLM. 

This function removes unnecessary special characters, excessive whitespace, and potentially harmful content such as **HTML/JavaScript injections**. It supports various input types, including:
- **Strings**
- **Lists of strings**
- **pandas Series**
- **NumPy arrays**

---

## **Key Features**
✔ **Removes unnecessary special characters** (`\`, `*`, `_`, `{}`, `[]`, `()`, `#`, `+`, `!`, `$`).  
✔ **Eliminates potential script injections** (`<script>` and `javascript:`).  
✔ **Normalizes excessive whitespace** to ensure clean formatting.  
✔ **Supports multiple input formats** (`str`, `list`, `pandas.Series`, `numpy.ndarray`).  
✔ **Returns sanitized content in the same format as input** for easy integration.  

---

## **Function Definition**
```python
def sanitize_prompt(prompt: Union[str, List[str], pd.Series, np.ndarray]) -> Union[str, List[str], pd.Series, np.ndarray]:
    """
    A versatile prompt sanitization function that works with various input types.
    
    Args:
        prompt: Input that can be a string, list of strings, pandas Series, or numpy array
        
    Returns:
        Sanitized version of the input in the same format
    """
```

---

## **Usage Examples**
### **Example 1: Sanitizing a Single String Prompt**
```python
from llmworkbook import sanitize_prompt

prompt = "   Tell me about AI <script>alert('XSS')</script> with [markdown] formatting!    "
clean_prompt = sanitize_prompt(prompt)
print(clean_prompt)
```
**Output:**
```plaintext
"Tell me about AI alert('XSS') with markdown formatting!"
```
🚀 The function **removes HTML script tags** and **normalizes whitespace**.

---

### **Example 2: Sanitizing a List of Prompts**
```python
prompt_list = [
    "Tell me about {Python}",
    "  <script>alert('XSS')</script>  ",
    "Analyze the following data: [1, 2, 3, 4, 5]"
]
clean_list = sanitize_prompt(prompt_list)
print(clean_list)
```
**Output:**
```plaintext
['Tell me about Python', "alert('XSS')", 'Analyze the following data: 1, 2, 3, 4, 5']
```
✔ The function **removes curly braces**, **HTML tags**, and **cleans formatting**.

---

### **Example 3: Sanitizing a pandas DataFrame Column**
```python
import pandas as pd

# Sample DataFrame
df = pd.DataFrame({
    'user_id': [1, 2, 3],
    'prompt': [
        "Generate a *summary* of this article",
        "  <script>malicious code</script>  ",
        "What is the answer to [4+5]?"
    ]
})

# Sanitize the 'prompt' column
df['clean_prompt'] = sanitize_prompt(df['prompt'])
print(df)
```
**Output:**
```plaintext
   user_id                            prompt                     clean_prompt
0        1  Generate a *summary* of this article  Generate a summary of this article
1        2    <script>malicious code</script>             malicious code
2        3       What is the answer to [4+5]?     What is the answer to 45?
```
✔ **Markdown special characters**, **HTML tags**, and **extra whitespace** are removed. 

---

### **Example 4: Sanitizing a NumPy Array**
```python
import numpy as np

prompt_array = np.array([
    "Calculate 2+2=?",
    "   What is the ```result```?  ",
    "<script>alert('XSS')</script>"
])

clean_array = sanitize_prompt(prompt_array)
print(clean_array)
```
**Output:**
```plaintext
['Calculate 22=?' 'What is the result?' 'alert(XSS)']
```
✔ Handles **NumPy arrays** efficiently with **vectorized sanitization**.

---

## **Why Use `sanitize_prompt`?**
| Feature | Benefit |
|---------|---------|
| ✅ **Security** | Removes potential **JavaScript injections**, preventing XSS risks. |
| ✅ **Consistency** | Ensures prompts are **properly formatted** for better LLM output. |
| ✅ **Flexibility** | Works with **strings, lists, pandas Series, and NumPy arrays**. |
| ✅ **Easy Integration** | Use before passing prompts to **wrappers** or **integrators**. |

---

## **Integration with LLM Wrappers**
Sanitized prompts can be **directly passed** to LLM wrappers or integrators to ensure safe and clean input.

```python
from llmworkbook import sanitize_prompt, WrapDataFrame

df = pd.DataFrame({
    "prompt": ["Tell me about *Python*.", "<script>alert('XSS')</script>", "What is 4+5?"]
})

# Clean the prompts
df["clean_prompt"] = sanitize_prompt(df["prompt"])

# Pass cleaned prompts to the wrapper
wrapper = WrapDataFrame(df, prompt_column="clean_prompt")
wrapped_df = wrapper.wrap()
print(wrapped_df)
```
✔ **Ensures that LLM receives sanitized input, improving response quality and security.**

---

**Use `sanitize_prompt` before passing data to LLM integrators for cleaner, more secure results!**

---
