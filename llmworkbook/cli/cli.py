#!/usr/bin/env python3
"""
CLI for LLMWorkbook Wrappers and Connectivity Testing (Poetry-based)

This script provides a command-line interface (CLI) for:
- Wrapping data in different formats (DataFrame, Array, Prompts)
- Testing LLM connectivity using an API key

Usage:
    python script.py <command> [options]

Commands:
    - wrap_dataframe: Wraps a pandas DataFrame into a structured format.
    - wrap_array: Wraps a 2D array into a structured format.
    - wrap_prompts: Wraps a list of prompts.
    - test: Tests the LLM connection using a sample prompt.
"""

import argparse
import json
import pandas as pd
import numpy as np
from llmworkbook import (
    WrapDataFrame,
    WrapDataArray,
    WrapPromptList,
    LLMConfig,
    LLMRunner,
)


def wrap_dataframe(
    input_file: str, output_file: str, prompt_column: str, data_columns: str
):
    """
    Wraps a pandas DataFrame into a structured format.

    Args:
        input_file (str): Path to the input CSV or Excel file.
        output_file (str): Path to save the wrapped DataFrame as a CSV.
        prompt_column (str): Column name to be used as the prompt.
        data_columns (str): Comma-separated column names for wrapping data.
    """
    df = (
        pd.read_csv(input_file)
        if input_file.endswith(".csv")
        else pd.read_excel(input_file)
    )
    wrapper = WrapDataFrame(
        df, prompt_column=prompt_column, data_columns=data_columns.split(",")
    )
    wrapped_df = wrapper.wrap()
    wrapped_df.to_csv(output_file, index=False)
    print(f"✅ Wrapped DataFrame saved to {output_file}")


def wrap_array(input_file: str, output_file: str, prompt_index: str, data_indices: str):
    """
    Wraps a 2D array from a JSON file into a structured format.

    Args:
        input_file (str): Path to the input JSON file containing array data.
        output_file (str): Path to save the wrapped DataFrame as a CSV.
        prompt_index (str): Index of the prompt column in the array.
        data_indices (str): Comma-separated indices for data columns.
    """
    with open(input_file, "r", encoding="utf-8") as file:
        array_data = json.load(file)
    wrapper = WrapDataArray(
        np.array(array_data),
        prompt_index=int(prompt_index),
        data_indices=[int(idx) for idx in data_indices.split(",")],
    )
    wrapped_df = wrapper.wrap()
    wrapped_df.to_csv(output_file, index=False)
    print(f"✅ Wrapped Array saved to {output_file}")


def wrap_prompts(prompts_file: str, output_file: str):
    """
    Wraps a list of prompts into a structured format.

    Args:
        prompts_file (str): Path to the input file containing prompts (one per line).
        output_file (str): Path to save the wrapped prompts as a CSV.
    """
    with open(prompts_file, "r", encoding="utf-8") as file:
        prompts = file.readlines()
    wrapper = WrapPromptList([prompt.strip() for prompt in prompts])
    wrapped_df = wrapper.wrap()
    wrapped_df.to_csv(output_file, index=False)
    print(f"✅ Wrapped Prompts saved to {output_file}")


def test_llm(api_key: str, model_name: str = "gpt-3.5-turbo"):
    """
    Tests the LLM connection by sending a sample prompt.

    Args:
        api_key (str): API key for the LLM provider.
        model_name (str, optional): Model name to use for testing. Defaults to "gpt-3.5-turbo".
    """
    config = LLMConfig(
        provider="openai",
        api_key=api_key,
        system_prompt="User is testing connection. Respond by saying Hi and a haiku.",
        options={
            "model_name": model_name,
        },
    )

    runner = LLMRunner(config)
    sample_prompt = "Hello, LLM! Can you confirm that this connection is working?"

    print("🔄 Sending test prompt to LLM...")
    try:
        response = runner.run_sync(sample_prompt)
        print("\n✅ LLM Connection Successful! Response:")
        print("------------------------------------------------")
        print(response)
        print("------------------------------------------------")
    except Exception as e:  # pylint: disable=W0718
        print("❌ LLM Connection Failed!")
        print(f"Error: {e}")


def main():
    """
    Main function to handle CLI arguments and execute respective commands.
    """
    parser = argparse.ArgumentParser(
        description="CLI for wrapping data and testing LLM connectivity."
    )
    subparsers = parser.add_subparsers(dest="command", help="Sub-command help")

    # Wrap DataFrame
    parser_df = subparsers.add_parser("wrap_dataframe", help="Wrap a pandas DataFrame")
    parser_df.add_argument("input_file", help="Path to the input file (CSV/Excel)")
    parser_df.add_argument("output_file", help="Path to save the wrapped output (CSV)")
    parser_df.add_argument("prompt_column", help="Column name for the prompt")
    parser_df.add_argument(
        "data_columns", help="Comma-separated column names for the data to wrap"
    )

    # Wrap Array
    parser_array = subparsers.add_parser("wrap_array", help="Wrap a 2D array")
    parser_array.add_argument(
        "input_file", help="Path to the JSON file with array data"
    )
    parser_array.add_argument(
        "output_file", help="Path to save the wrapped output (CSV)"
    )
    parser_array.add_argument(
        "prompt_index", help="Index of the prompt column in the array"
    )
    parser_array.add_argument(
        "data_indices", help="Comma-separated indices for data columns"
    )

    # Wrap Prompts
    parser_prompts = subparsers.add_parser(
        "wrap_prompts", help="Wrap a list of prompts"
    )
    parser_prompts.add_argument(
        "prompts_file", help="Path to the file containing prompts (one per line)"
    )
    parser_prompts.add_argument(
        "output_file", help="Path to save the wrapped output (CSV)"
    )

    # Test LLM Connection
    parser_test = subparsers.add_parser(
        "test", aliases=["t"], help="Test LLM connection with a sample prompt"
    )
    parser_test.add_argument("api_key", help="API key for the LLM provider")
    parser_test.add_argument(
        "--model_name",
        default="gpt-3.5-turbo",
        help="Optional: LLM model name (default: gpt-3.5-turbo)",
    )

    args = parser.parse_args()

    # Dispatch Commands
    if args.command == "wrap_dataframe":
        wrap_dataframe(
            args.input_file, args.output_file, args.prompt_column, args.data_columns
        )
    elif args.command == "wrap_array":
        wrap_array(
            args.input_file, args.output_file, args.prompt_index, args.data_indices
        )
    elif args.command == "wrap_prompts":
        wrap_prompts(args.prompts_file, args.output_file)
    elif args.command in ["test", "t"]:
        test_llm(args.api_key, args.model_name)
    else:
        parser.print_help()
