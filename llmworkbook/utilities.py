"""
Additional utility functions for the llmworkbook package.
"""

import re
from typing import List, Union, Optional

import json
import numpy as np
import pandas as pd
import warnings


def sanitize_prompt(
    prompt: Union[str, List[str], pd.Series, np.ndarray]
) -> Union[str, List[str], pd.Series, np.ndarray]:
    """
    A versatile prompt sanitization function that works with various input types.

    Args:
        prompt: Input that can be a string, list of strings, pandas Series, or numpy array

    Returns:
        Sanitized version of the input in the same format
    """

    # Helper function for single string sanitization
    def _sanitize_single(text: str) -> str:
        if not isinstance(text, str):
            return str(text)

        # Remove extra whitespace
        text = text.strip()

        # Remove special characters that could cause issues
        text = re.sub(r"[\\`*_{}[\]()#+.!$]", "", text)

        # Replace potentially harmful patterns
        text = text.replace("javascript:", "")
        text = text.replace("<script>", "")

        # Normalize whitespace
        text = re.sub(r"\s+", " ", text)

        return text

    # Handle different input types
    if isinstance(prompt, str):
        return _sanitize_single(prompt)

    elif isinstance(prompt, list):
        return [_sanitize_single(item) for item in prompt]

    elif isinstance(prompt, pd.Series):
        return prompt.apply(_sanitize_single)

    elif isinstance(prompt, np.ndarray):
        vectorized_sanitize = np.vectorize(_sanitize_single)
        return vectorized_sanitize(prompt)

    else:
        raise TypeError(f"Unsupported input type: {type(prompt)}")


def unpack_json_responses(
    df: pd.DataFrame,
    response_column: str = "llm_response",
    error_handling: str = "warn",
    flatten_nested: bool = True,
    prefix: Optional[str] = None,
    columns_to_extract: Optional[List[str]] = None,
    drop_original: bool = True,
) -> pd.DataFrame:
    """
    Unpacks JSON responses from a specified DataFrame column into separate columns.

    Args:
        df (pd.DataFrame): DataFrame containing the LLM responses in JSON format.
        response_column (str): Column name where JSON responses are stored.
        error_handling (str): Strategy for handling JSON parsing errors:
                             'warn' (default): Replace with None and log warning
                             'error': Raise exception
                             'ignore': Replace with None silently
        flatten_nested (bool): Whether to flatten nested JSON structures (default: True)
        prefix (str, optional): Prefix to add to all extracted columns
        columns_to_extract (List[str], optional): Specific fields to extract from JSON,
                                                 extracts all if None
        drop_original (bool): Whether to drop the original JSON column (default: True)

    Returns:
        pd.DataFrame: DataFrame with unpacked JSON response columns.
    """
    result_df = df.copy()

    # Helper function to safely parse JSON
    def safe_json_parse(x):
        if pd.isna(x):
            return None
        if not isinstance(x, str):
            return x  # Already parsed or not a string

        try:
            return json.loads(x)
        except json.JSONDecodeError as e:
            if error_handling == "error":
                raise e
            elif error_handling == "warn":
                warnings.warn(f"Error parsing JSON: {e}. Value: {x[:100]}...")
            return None

    result_df[response_column] = result_df[response_column].apply(safe_json_parse)

    # Filter out any rows with None or invalid JSON
    valid_json_mask = result_df[response_column].notna()

    if valid_json_mask.sum() == 0:
        warnings.warn("No valid JSON found in the response column")
        return result_df

    # Normalize JSON structure with configurable options
    normalize_kwargs = {"record_path": None}

    if not flatten_nested:
        normalize_kwargs["max_level"] = 0

    if columns_to_extract:
        json_df = pd.DataFrame(index=range(len(result_df)))

        for col in columns_to_extract:
            json_df[col] = result_df.loc[valid_json_mask, response_column].apply(
                lambda x: x.get(col) if isinstance(x, dict) else None
            )
    else:
        try:
            json_df = pd.json_normalize(
                result_df.loc[valid_json_mask, response_column].tolist(),
                **normalize_kwargs,
            )
        except Exception as e:
            if error_handling == "error":
                raise e
            warnings.warn(f"Error normalizing JSON: {e}")
            return result_df

    # Add prefix to columns if specified
    if prefix:
        json_df.columns = [
            f"{prefix}_{col}" if not col.startswith(prefix) else col
            for col in json_df.columns
        ]

    expanded_df = pd.DataFrame(index=result_df.index)

    if len(json_df) > 0:
        valid_indices = result_df.index[valid_json_mask]
        for col in json_df.columns:
            expanded_df.loc[valid_indices, col] = json_df[col].values

    if drop_original:
        original_cols = result_df.columns.difference([response_column])
    else:
        original_cols = result_df.columns

    result = pd.concat([result_df[original_cols], expanded_df], axis=1)

    return result
