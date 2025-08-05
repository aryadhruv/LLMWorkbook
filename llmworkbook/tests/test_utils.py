# pylint: skip-file
from ..utilities import sanitize_prompt
import pandas as pd
import numpy as np


def test_sanitize_prompt():
    # Arrange
    sample_prompt = "This is a sample string  "

    # Action
    sanitized_prompt = sanitize_prompt(sample_prompt)

    # Assert
    assert sanitized_prompt == "This is a sample string"


def test_sanitize_prompt_list():
    sample_list = [" Item 1! ", "Item 2?", "Item 3..."]
    sanitized = sanitize_prompt(sample_list)
    assert sanitized == ["Item 1", "Item 2", "Item 3"]


def test_sanitize_prompt_series():
    sample_series = pd.Series([" Panda  ", "Bear!", "  Zoo@"])  # type: ignore[var-annotated]
    sanitized = sanitize_prompt(sample_series)
    expected = pd.Series(["Panda", "Bear", "Zoo"])  # type: ignore[var-annotated]
    pd.testing.assert_series_equal(sanitized, expected)


def test_sanitize_prompt_ndarray():
    sample_array = np.array(["   One  ", "Two*", "Three#"])
    sanitized = sanitize_prompt(sample_array)
    expected = np.array(["One", "Two", "Three"])
    assert np.array_equal(sanitized, expected)
