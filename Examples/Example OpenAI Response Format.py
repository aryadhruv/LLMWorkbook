"""
Example usage script for OpenAI API endpoint.
"""

import pandas as pd
from llmworkbook import LLMConfig, LLMRunner, LLMDataFrameIntegrator
from dotenv import load_dotenv

load_dotenv()


def main():
    # 1. Create a sample dataframe
    data = {
        "id": [1, 2, 3, 4, 5],
        "prompt_text": [
            "Extract key entities (persons, places, organizations) from this text: 'OpenAI, based in San Francisco, is a leading AI research lab founded by Sam Altman and Greg Brockman.'",
            "Convert this product description into structured data: 'The iPhone 15 Pro features a 6.1-inch display, A17 Bionic chip, and a titanium body.'",
            "Provide a breakdown of this sentence into subject, verb, and object: 'The cat chased the mouse across the room.'",
            "Generate a JSON object with three random trivia questions along with their answers.",
            "Summarize the given customer review into structured categories like 'sentiment', 'key topics', and 'rating' from this text: 'The camera quality of this phone is fantastic, but the battery life could be better. I would rate it 4 out of 5.'",
        ],
    }

    df = pd.DataFrame(data)

    # 2. Create an LLM configuration
    config = LLMConfig(
        provider="openai",
        system_prompt="Process these data rows as per the provided prompt. Ensure the response is strictly in JSON format.",
        options={
            "model": "gpt-4o-mini",
            "temperature": 1,
            "max_tokens": 1024,
            "response_format" : { "type": "json_object" },
        },
    )

    # 3. Instantiate the runner and the integrator
    runner = LLMRunner(config)
    integrator = LLMDataFrameIntegrator(runner=runner, df=df)

    # 4. Add LLM responses to the df
    updated_df = integrator.add_llm_responses(
        prompt_column="prompt_text", response_column="llm_response", async_mode=True
    )

    print("DataFrame with LLM responses:\n", updated_df)

    #Print Expected output - 
    # {
    # "subject": "The cat",
    # "verb": "chased",
    # "object": "the mouse"
    # }

    updated_df.to_excel("testdf.xlsx")


if __name__ == "__main__":
    main()
