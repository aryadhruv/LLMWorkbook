"""
Example usage script for WrapDataFrame, WrapDataArray, and WrapPromptList.
"""

import pandas as pd
import numpy as np
from llmworkbook import LLMConfig, LLMRunner, LLMDataFrameIntegrator, WrapDataFrame
from dotenv import load_dotenv

load_dotenv()

def main():
    """
    Example usage of WrapDataFrame with a Excel Workbook.
    """
    # 1. Load a pandas DataFrame from Excel source
    df = pd.read_excel("sample dataset.xlsx")
    wrapper = WrapDataFrame(df, prompt_column="prompt", data_columns=(['Review', 'Date']))
    wrapped_df = wrapper.wrap()

    # 2. Create an LLM configuration
    config = LLMConfig(
        provider="openai",
        system_prompt="Process these Data rows as per the provided prompt",
        options={
            "model_name": "gpt-4o-mini",
            "temperature": 1,
            "max_tokens": 1024,
        },
    )

    # 3. Instantiate the runner and integrator
    runner = LLMRunner(config)
    integrator = LLMDataFrameIntegrator(runner=runner, df=wrapped_df)

    # 4. Add LLM responses to the DataFrame
    updated_df = integrator.add_llm_responses(
        prompt_column="wrapped_output",
        response_column="llm_response",
        async_mode=True
    )

    print("Updated DataFrame with LLM responses (DataFrame):\n", updated_df)

if __name__ == "__main__":
    main()
