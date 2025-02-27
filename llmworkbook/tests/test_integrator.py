# pylint: skip-file
import pytest
import pandas as pd
import asyncio
from unittest.mock import Mock

from llmworkbook import LLMDataFrameIntegrator


# Mock LLMRunner class
class MockLLMRunner:
    def __init__(
        self, sync_response="Mock response", async_response="Mock async response"
    ):
        self.config = Mock()
        self.config.options = {"max_tokens": 1000}
        self.sync_response = sync_response
        self.async_response = async_response

    def run_sync(self, prompt: str) -> str:
        return self.sync_response

    async def run(self, prompt: str) -> str:
        return self.async_response


@pytest.fixture
def sample_df():
    # Create a DataFrame - not a function
    df = pd.DataFrame(
        {
            "id": range(1, 6),
            "prompt_column": [
                "Test prompt 1",
                "Test prompt 2",
                "Test prompt 3",
                "Test prompt 4",
                "Test prompt 5",
            ],
        }
    )
    return df


@pytest.fixture
def mock_runner():
    return MockLLMRunner()


@pytest.fixture
def integrator(sample_df, mock_runner):
    return LLMDataFrameIntegrator(runner=mock_runner, df=sample_df.copy())


def test_initialization(sample_df, mock_runner):
    """Test proper initialization of LLMDataFrameIntegrator"""
    integrator = LLMDataFrameIntegrator(runner=mock_runner, df=sample_df)
    assert integrator.df is not None
    assert integrator.runner is not None
    assert integrator.max_tokens == 1000


def test_token_estimation(integrator):
    """Test token estimation functionality"""
    text = "This is a test sentence with seven words"
    estimated_tokens = integrator._estimate_token_count(text)
    # Round to avoid floating point comparison issues
    assert round(estimated_tokens) == 11


@pytest.mark.asyncio
async def test_individual_processing_async(integrator):
    """Test processing individual rows asynchronously"""
    # Create a new event loop for this test
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    try:

        async def run_test():
            return await integrator.runner.run("test prompt")

        response = await run_test()
        assert response == "Mock async response"
    finally:
        loop.close()


def test_batch_processing_sync(integrator):
    """Test processing multiple rows in batches synchronously"""
    # Get initial state of specific rows
    row_indices = [0, 1, 2]

    result_df = integrator._process_batches(
        row_indices=row_indices,
        prompt_column="prompt_column",
        response_column="llm_response",
        async_mode=False,
        batch_size=2,
        split_response=True,
    )

    # Verify each row in the batch was processed
    assert result_df.iloc[0]["llm_response"] is not None, f"Row {0} was not processed"
    assert result_df.iloc[2]["llm_response"] is not None, f"Row {2} was not processed"


def test_add_llm_responses_full_batch(integrator):
    """Test processing all rows in a single batch"""
    result_df = integrator.add_llm_responses(
        prompt_column="prompt_column",
        response_column="llm_response",
        batch_size=0,  # Process all rows at once
    )

    # Check that each row has the expected response
    assert result_df["llm_response"][0] == "Mock response", "Unexpected response value"


def test_add_llm_responses_with_split_response(sample_df):
    """Test processing with split response option"""
    # Mock runner that returns multi-line response
    mock_runner = MockLLMRunner(sync_response="Response 1\nResponse 2\nResponse 3")

    # Create a new DataFrame instance
    test_df = sample_df.copy()
    test_df["llm_response"] = None

    integrator_split = LLMDataFrameIntegrator(runner=mock_runner, df=test_df)

    result_df = integrator_split.add_llm_responses(batch_size=3, split_response=True)

    # Check that responses were split correctly
    assert result_df.iloc[0]["llm_response"] == "Response 1"
    assert result_df.iloc[1]["llm_response"] == "Response 2"
    assert result_df.iloc[2]["llm_response"] == "Response 3"


def test_response_overflow_handling(sample_df):
    """Test handling of overflow responses"""
    # Mock runner that returns more responses than rows
    mock_runner = MockLLMRunner(sync_response="R1\nR2\nR3\nR4\nR5\nR6")

    # Create a new DataFrame with exactly 3 rows
    test_df = sample_df.iloc[0:3].copy()
    test_df["llm_response"] = None

    integrator_overflow = LLMDataFrameIntegrator(runner=mock_runner, df=test_df)

    result_df = integrator_overflow.add_llm_responses(batch_size=3, split_response=True)

    # Check that overflow is handled properly
    assert len(result_df) == 3  # Should still have only 3 rows
    assert (
        "Overflow" in result_df.iloc[2]["llm_response"]
    )  # Last row should contain overflow data


if __name__ == "__main__":
    pytest.main([__file__])
