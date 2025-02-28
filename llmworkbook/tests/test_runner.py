# pylint: skip-file
import pytest
from unittest.mock import AsyncMock
from llmworkbook import LLMRunner, LLMConfig


@pytest.fixture
def mock_config():
    """Fixture for creating an LLMConfig object."""
    return LLMConfig(
        provider="openai",
        api_key="test-api-key",
        system_prompt="Process these Data rows as per the provided prompt",
        options={
            "model": "gpt-4o-mini",
            "temperature": 1,
            "max_tokens": 1024,
        },
    )


@pytest.mark.asyncio
async def test_llmrunner_initialization(mock_config):
    """Test that LLMRunner initializes correctly."""
    runner = LLMRunner(config=mock_config)
    assert runner.config == mock_config


@pytest.mark.asyncio
async def test_run(mock_config):
    """Test the synchronous wrapper for the run method."""
    # Initialize the runner
    runner = LLMRunner(config=mock_config)

    # Mock the async run method
    runner.run = AsyncMock(return_value="LLM response for prompt")

    # Call run_sync
    result = await runner.run("Explain Newton's first law in simple terms.")

    # Assert the result
    assert result == "LLM response for prompt"

    # Verify the run method call
    runner.run.assert_called_once_with("Explain Newton's first law in simple terms.")


def test_run_sync(mock_config):
    """Test the synchronous wrapper for the run method."""
    # Initialize the runner
    runner = LLMRunner(config=mock_config)

    # Mock the async run method
    runner.run = AsyncMock(return_value="LLM response for prompt")

    # Call run_sync
    result = runner.run_sync("Explain Newton's first law in simple terms.")

    # Assert the result
    assert result == "LLM response for prompt"

    # Verify the run method call
    runner.run.assert_called_once_with("Explain Newton's first law in simple terms.")


@pytest.mark.asyncio
async def test_provider():
    """Test handling of an unimplemented provider."""
    with pytest.raises(NotImplementedError):
        await LLMRunner(config=LLMConfig(provider="llmprovider")).run("prompt")
