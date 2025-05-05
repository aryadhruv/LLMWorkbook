"""
Example usage script for Anthropic API endpoint.
"""

import pandas as pd
from llmworkbook import LLMConfig, LLMRunner, LLMDataFrameIntegrator
from dotenv import load_dotenv

load_dotenv()


def main():
    # 1. Sample data
    data = {
        "id": [1, 2, 3],
        "prompt_text": [
            "Summarize Newton's first law in simple words.",
            "Compose a haiku about the moon.",
            "Give 3 tips to improve productivity at work.",
        ],
    }
    df = pd.DataFrame(data)

    # 2. Anthropic LLM config
    config = LLMConfig(
        provider="anthropic",
        system_prompt="You are a helpful assistant processing each user input. Be concise and clear.",
        options={
            "model": "claude-3-sonnet-20240229",
            "max_tokens": 1024,
        },
    )

    # 3. LLM pipeline setup
    runner = LLMRunner(config)
    integrator = LLMDataFrameIntegrator(runner=runner, df=df)

    # 4. Enrich DataFrame with Claude responses
    updated_df = integrator.add_llm_responses(
        prompt_column="prompt_text",
        response_column="llm_response",
        async_mode=True
    )

    print("DataFrame with Claude responses:\n", updated_df)


if __name__ == "__main__":
    main()

