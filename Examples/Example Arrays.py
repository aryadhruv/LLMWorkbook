"""
Example usage script for WrapDataFrame, WrapDataArray, and WrapPromptList.
"""

import numpy as np
from llmworkbook import LLMConfig, LLMRunner, LLMDataFrameIntegrator, WrapDataArray
from dotenv import load_dotenv

load_dotenv()


def main():
    """
    Example usage of WrapDataArray with a 2D array-like structure.
    """
    # 1. Create a 2D NumPy array
    data = np.array(
        [
            ["prompt_1", "review_1", "en"],
            ["prompt_2", "review_2", "es"],
            ["prompt_3", "review_3", "fr"],
        ]
    )
    wrapper = WrapDataArray(data, prompt_index=0, data_indices=[1, 2])
    wrapped_df = wrapper.wrap()

    # 2. Create an LLM configuration
    config = LLMConfig(
        provider="openai",
        system_prompt="Process these Data rows as per the provided prompt",
        options={
            "model": "gpt-4o-mini",
            "temperature": 1,
            "max_tokens": 1024,
        },
    )

    # 3. Instantiate the runner and integrator
    runner = LLMRunner(config)
    integrator = LLMDataFrameIntegrator(runner=runner, df=wrapped_df)

    # 4. Add LLM responses to the DataFrame
    updated_df = integrator.add_llm_responses(
        prompt_column="wrapped_output", response_column="llm_response", async_mode=True
    )

    print("Updated DataFrame with LLM responses (Array):\n", updated_df)


if __name__ == "__main__":
    main()
