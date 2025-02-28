# pylint: skip-file
from ..utilities import sanitize_prompt


def test_sanitize_prompt():
    # Arrange
    sample_prompt = "This is a sample string  "

    # Action
    sanitized_prompt = sanitize_prompt(sample_prompt)

    # Assert
    assert sanitized_prompt == "This is a sample string"
