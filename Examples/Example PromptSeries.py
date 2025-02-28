"""
Example usage script for WrapDataFrame, WrapDataArray, and WrapPromptList.
"""

from llmworkbook import LLMConfig, LLMRunner, LLMDataFrameIntegrator, WrapPromptList
from dotenv import load_dotenv

load_dotenv()


def main():
    """
    Example usage of WrapPromptList with a 1D list of prompts.
    """
    # 1. Create a list of prompts
    prompts = [
        "Summarize the following review.",
        "Translate this text to English.",
        "Provide a sentiment analysis of the input.",
    ]
    wrapper = WrapPromptList(prompts)
    wrapped_df = wrapper.wrap()

    # 2. Create an LLM configuration
    config = LLMConfig(
        provider="openai",
        system_prompt="Process these prompts",
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

    print("Updated DataFrame with LLM responses (Prompts):\n", updated_df)


if __name__ == "__main__":
    main()
