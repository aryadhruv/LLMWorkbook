"""
Example usage script for LLMDataFrameIntegrator with batch processing and summarization.
"""

import pandas as pd
from llmworkbook import LLMConfig, LLMRunner, LLMDataFrameIntegrator, WrapDataFrame
from dotenv import load_dotenv

load_dotenv()


def main():
    """
    Example usage of WrapDataFrame with batch processing and history tracking.
    """
    # 1. Load a pandas DataFrame from Excel source
    df = pd.read_excel("sample dataset.csv")

    # 2. Wrap the DataFrame for LLM readiness
    wrapper = WrapDataFrame(df, prompt_column="prompt", data_columns=["Review", "Date"])
    wrapped_df = wrapper.wrap()

    # 3. Create an LLM configuration
    config = LLMConfig(
        provider="openai",
        system_prompt="Process these Data rows as per the provided prompt",
        options={
            "model": "gpt-4o-mini",
            "temperature": 1,
            "max_tokens": 2048,  # Ensure token limit is set
        },
    )

    # 4. Instantiate the runner and integrator
    runner = LLMRunner(config)
    integrator = LLMDataFrameIntegrator(runner=runner, df=wrapped_df)

    # 5. Add LLM responses using batch processing (batch_size = 10)
    updated_df = integrator.add_llm_responses(
        prompt_column="wrapped_output",
        response_column="llm_response",
        batch_size=10,  # Process 10 rows at a time
        async_mode=True,  # Set to True for async processing
    )

    print("Updated DataFrame with LLM responses:\n", updated_df)

    # 8. Save the updated DataFrame to an Excel file
    updated_df.to_excel("processed_dataset.xlsx", index=False)
    print("\nProcessed DataFrame saved to 'processed_dataset.xlsx'")


if __name__ == "__main__":
    main()
