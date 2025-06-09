---
layout: page
title: Batch and Row Processing
permalink: /docs/batch-row-processing/
---

# **LLMWorkbook - Batch and Row Processing Documentation**

## **Overview**

The **LLMDataFrameIntegrator** class allows users to integrate Large Language Models (LLMs) into a pandas `DataFrame` pipeline. This class provides flexibility by allowing both **row-wise processing** and **batch processing** of prompts, helping optimize the use of LLMs while ensuring the token limit of the LLM is respected. This documentation explains how the data is processed, with a detailed breakdown of **row processing** and **batch processing** modes.

---

## **Data Processing Overview**

In the `LLMDataFrameIntegrator` class, data processing can occur in two primary ways:
1. **Row-wise Processing**: Each row is processed separately by sending one prompt at a time to the LLM.
2. **Batch Processing**: Multiple rows are grouped together, and the entire batch is sent to the LLM in a single request.

The user can choose between **row-wise** and **batch** processing depending on their needs. Both modes allow for flexibility in how the data is sent to the LLM, and batch processing, in particular, is designed to improve efficiency by reducing the number of API calls.

### **Key Features**
- **Batch Size Control**: Control the number of rows to be sent in each batch request.
- **Token Limit Validation**: Ensure the total number of tokens in a batch does not exceed the LLM’s `max_tokens` limit.
- **Overflow Handling**: Handle cases where the number of LLM responses differs from the number of rows.
- **Flexible Response Handling**: Option to split responses by row or store the entire batch's response in a single row.

---

## **1. Row-wise Processing**

### **How Row-wise Processing Works**

Row-wise processing is the default behavior when using the `LLMDataFrameIntegrator`. Each row in the DataFrame is treated as an independent prompt, and the LLM is called for each row’s prompt sequentially.

- **Prompt Processing**: For each row, the value from the specified `prompt_column` is used as the prompt for the LLM.
- **Response Storage**: The response from the LLM is stored in the specified `response_column` for each row.

### **When to Use Row-wise Processing**
- Use **row-wise processing** when:
  - Each row represents an independent task or question.
  - You do not need to batch multiple rows into one API call for efficiency.
  - The responses should be handled individually.

### **Example: Row-wise Processing**
```python
updated_df = integrator.add_llm_responses(
    prompt_column="prompt_column",
    response_column="llm_response",
    batch_size=None  # Default to row-wise processing
)
```
In this case, the integrator will process each prompt row by row and store the response in the `llm_response` column for each row.

---

## **2. Batch Processing**

### **How Batch Processing Works**

Batch processing groups multiple rows together and sends them as a single request to the LLM. The prompt texts from the specified `prompt_column` for each batch of rows are concatenated into a single string, separated by newline characters (`\n`), and then sent together to the LLM.

- **Batch Construction**: A batch is created by selecting a subset of rows based on the `batch_size`. The prompts for these rows are concatenated into a single string.
- **Single Request**: The entire batch (concatenated string of prompts) is sent as one LLM request.
- **Response Handling**: The LLM's response, which could contain multiple answers (one per row), is split and assigned back to the individual rows. If there are fewer responses than rows, the excess rows will receive an "Overflow" tag.

### **When to Use Batch Processing**
- Use **batch processing** when:
  - Let's say you want a summary of multiple texts, or other long context tasks.
  - You have multiple related prompts (e.g., reviews, articles) and prefer to process them together for efficiency.

### **Batch Mode Behavior**
- The batch is created by selecting rows in the DataFrame based on the `batch_size`.
- The total tokens in a batch (i.e., the number of tokens for all prompts in the batch) are **estimated** to ensure they do not exceed the `max_tokens` limit set by the LLM.
- If the total token count exceeds `max_tokens`, an error is raised, and the user is advised to truncate the DataFrame or reduce the batch size.
- If there are more responses than rows in a batch, the excess responses are **merged** into the last row with an `"Overflow"` tag.

### **Overflow Handling**
- If LLM returns more responses than rows, the excess responses are concatenated and stored in the last row with an `Overflow:` tag, separating the overflowed messages by `<sep>`.
- If LLM returns fewer responses than rows, the remaining rows will contain `"Overflow"` messages indicating missing responses.

### **Example: Batch Processing with Split Responses**
```python
updated_df = integrator.add_llm_responses(
    prompt_column="prompt_column",
    response_column="llm_response",
    batch_size=5,  # Process 5 rows together
    split_response=True  # Split responses row by row
)
```
Here, the integrator will process 5 rows at once, send them as a single request, and assign the individual responses to the corresponding rows. If there are fewer responses than expected, the remaining rows will have the `"Overflow"` tag.

### **Example: Batch Processing Without Splitting Responses**
```python
updated_df = integrator.add_llm_responses(
    prompt_column="prompt_column",
    response_column="llm_response",
    batch_size=5,  # Process 5 rows together
    split_response=False  # Store the entire batch's response in the first row
)
```
In this case, the response from the LLM for the batch is stored in the first row, and the other rows in the batch remain empty.

---

## **3. Handling Overflow Responses**

When processing in **batch mode**, it is possible for the LLM to return:
- **Fewer responses than rows in the batch**: The remaining rows will be marked with `"Overflow: msg"`.
- **More responses than rows in the batch**: The extra responses will be merged into the last row with an `"Overflow: msg1 <sep> msg2"` tag.

### **Overflow Example**

If 3 rows are processed together, but the LLM returns 5 responses:
```plaintext
Batch: ["Prompt 1", "Prompt 2", "Prompt 3"]
Responses: ["Response 1", "Response 2", "Response 3", "Response 4", "Response 5"]
```

The response will be processed as:
```plaintext
Row 1: "Response 1"
Row 2: "Response 2"
Row 3: "Response 3 | Overflow: Response 4 <sep> Response 5"
```

---

## **4. Token Limit and Batch Size**

### **Token Limit Validation**
- When **batch processing**, the total estimated token count for a batch is calculated before sending the request to ensure that it doesn't exceed the LLM's `max_tokens` limit.
- The token limit validation is based on the **estimated token count** (roughly calculated by dividing the number of words by 1.33).
- If the total tokens for a batch exceed the allowed limit, a `ValueError` is raised with a message asking the user to reduce the batch size or truncate the input.

---

## **Function Overview**

### **Key Methods**

- **`add_llm_responses()`**  
   - Runs the LLM on each row's `prompt_column` text and stores the response in `response_column`.
   - Supports both row-wise and batch processing, with validation for `max_tokens`.
   - Accepts `batch_size`, `split_response`, and `async_mode` as parameters.

- **`_process_batches()`**  
   - Processes multiple rows in batches while ensuring the total token count is within limits.
   - Can handle overflow scenarios and map responses to rows.

- **`_process_individually()`**  
   - Processes rows one by one (default behavior when `batch_size=None`).

---

## **Final Thoughts**

### **Batch vs Row-wise Processing**
- **Row-wise**: Best for independent, single-question tasks where each row’s prompt needs to be processed separately.
- **Batch**: Best for related tasks (e.g., processing multiple reviews into summary) where sending batches together is more efficient, and token limits can be managed.

By offering both options, this feature allows users to decide whether to send prompts individually or in batches, optimizing for performance and cost, while ensuring that token limits are respected.
