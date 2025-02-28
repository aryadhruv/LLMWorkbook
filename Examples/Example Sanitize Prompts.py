"""
LLMWORKBOOK provides a easy to use utility function that allow you to quickly clean the prompt inputs.
This utility allows developer to ensure that the prompt passed to wrappers or integrators are secure and clean.
"""

from llmworkbook import sanitize_prompt

prompt : str = "Some placefolder prompt"

#Example 1: Sanitizing a single string prompt
prompt = "   Tell me about AI <script>alert('XSS')</script> with [markdown] formatting!    "
clean_prompt = sanitize_prompt(prompt)
print(clean_prompt)
# Output: "Tell me about AI alert('XSS') with markdown formatting!"

#Example 2: Sanitizing a list of prompts
prompt_list = [
    "Tell me about {Python}",
    "  <script>alert('XSS')</script>  ",
    "Analyze the following data: [1, 2, 3, 4, 5]"
]
clean_list = sanitize_prompt(prompt_list)
print(clean_list)
# Output: ['Tell me about Python', "alert('XSS')", 'Analyze the following data: 1, 2, 3, 4, 5']

# Example 3: Sanitizing a pandas DataFrame column
import pandas as pd

# Create a sample DataFrame with prompts
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
# Output:
#    user_id                            prompt                     clean_prompt
# 0        1  Generate a *summary* of this article  Generate a summary of this article
# 1        2    <script>malicious code</script>             malicious code
# 2        3               What is the answer to [4+5]?     What is the answer to 45?

#Example 4: Sanitizing a numpy array
import numpy as np

# Create an array of prompts
prompt_array = np.array([
    "Calculate 2+2=?",
    "   What is the ```result```?  ",
    "<script>alert('XSS')</script>"
])

clean_array = sanitize_prompt(prompt_array)
print(clean_array)


#Above clean prompts can be pass through the wrapper or integrator as needed. 
