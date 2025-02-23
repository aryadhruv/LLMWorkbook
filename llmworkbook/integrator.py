"""
Integrator module to combine LLM responses and DataFrames with batch processing.
"""

import warnings
import asyncio
import pandas as pd
from typing import Optional, List, Union
from .runner import LLMRunner


class LLMDataFrameIntegrator:
    """
    Integrates LLM calls with a DataFrame.
    """

    def __init__(self, runner: LLMRunner, df: pd.DataFrame) -> None:
        """
        Args:
            runner (LLMRunner): The runner object to call the LLM.
            df (pd.DataFrame): The DataFrame to attach results to.
        """
        self.runner = runner
        self.df = df
        self.max_tokens = runner.config.options.get("max_tokens", None)

        if self.max_tokens is None:
            warnings.warn(
                "Warning: max_tokens is not set in LLMConfig. "
                "Proceeding without validation, but API may reject large requests.",
                UserWarning,
            )

    def _estimate_token_count(self, text: str) -> int:
        """
        Estimates the token count of a given text.

        Args:
            text (str): The input text.

        Returns:
            int: Estimated token count.
        """
        return len(text.split()) * 1.33  # Approximate GPT-style tokenization

    def _validate_batch_size(self, prompts: List[str]) -> None:
        """
        Validates if the batch of prompts exceeds the token limit.

        Args:
            prompts (List[str]): The list of prompt texts.

        Raises:
            ValueError: If the total token count exceeds max_tokens.
        """
        if self.max_tokens is None:
            return  # Skip validation if max_tokens is not set

        total_tokens = sum(self._estimate_token_count(p) for p in prompts)
        if total_tokens > self.max_tokens:
            raise ValueError(
                f"Total estimated token count ({total_tokens}) exceeds the max token limit ({self.max_tokens}). "
                "Please truncate the DataFrame or reduce batch size."
            )

    def add_llm_responses(
        self,
        prompt_column: str = "prompt_column",
        response_column: str = "llm_response",
        row_filter: Optional[List[int]] = None,
        async_mode: Optional[int] = False,
        batch_size: Optional[int] = None,  # If None, default to row-wise processing
        split_response: Optional[int] = False,
    ) -> pd.DataFrame:
        """
        Runs the LLM on each row's `prompt_column` text and stores the response in
        `response_column`.

        Args:
            prompt_column (str): The column in the DataFrame containing prompt text.
            response_column (str, optional): The name of the column to store LLM responses.
                                             Defaults to "llm_response".
            row_filter (List[int], optional): Subset of row indices to run.
                                             If None, runs on all rows.
            async_mode (bool, optional): If True, uses async calls to LLM. Otherwise uses sync.
            batch_size (Optional[int], optional):
                - If `None`, processes row by row (default behavior).
                - If `batch_size > 1`, processes multiple rows together in a batch.
                - If `batch_size=0`, processes all rows in a **single LLM request**.
            split_response (bool, optional): If true response from multiline response from LLM will be into rows.
            Otherwise, a single response per batch will be presented.

        Returns:
            pd.DataFrame: The updated DataFrame with responses.
        """
        if response_column not in self.df.columns:
            self.df[response_column] = None

        if row_filter is None:
            row_indices = self.df.index.tolist()
        else:
            row_indices = row_filter

        # Default to row-wise processing if batch_size is None
        if batch_size is None:
            return self._process_individually(
                row_indices, prompt_column, response_column, async_mode
            )

        # If batch_size=0, process all rows at once
        if batch_size == 0:
            batch_size = len(row_indices)

        return self._process_batches(
            row_indices,
            prompt_column,
            response_column,
            async_mode,
            batch_size,
            split_response,
        )

    def _process_individually(
        self, row_indices, prompt_column, response_column, async_mode
    ):
        """
        Processes rows one by one.
        """
        if async_mode:
            return self._run_async_prompts(row_indices, prompt_column, response_column)

        for idx in row_indices:
            prompt_value = self.df.at[idx, prompt_column]
            if prompt_value:
                response = self.runner.run_sync(str(prompt_value))
                self.df.at[idx, response_column] = response
        return self.df

    def _process_batches(
        self,
        row_indices,
        prompt_column,
        response_column,
        async_mode,
        batch_size,
        split_response,
    ):
        """
        Processes multiple rows at once while ensuring token limit is not exceeded.
        """
        batches = [
            row_indices[i : i + batch_size]
            for i in range(0, len(row_indices), batch_size)
        ]

        for batch in batches:
            prompts = [str(self.df.at[idx, prompt_column]) for idx in batch]
            self._validate_batch_size(prompts)

            batch_prompt = "\n".join(prompts)

            if async_mode:
                responses = asyncio.run(self._run_batch_async(batch_prompt))
            else:
                responses = self.runner.run_sync(
                    batch_prompt
                )  # Single LLM request for batch

            # Handle multi-line responses if the LLM returns one response per row
            if isinstance(responses, str):
                response_list = responses.split("\n") if split_response else [responses]

            # Handle Overflow (if LLM returns more responses than expected)
            if len(response_list) > len(batch):
                response_list[len(batch) - 1] += " | Overflow: " + " <sep> ".join(
                    response_list[len(batch) - 1 :]
                )

            response_list = response_list[: len(batch)]

            # Assign responses to rows
            for idx, response in zip(batch, response_list):
                self.df.at[idx, response_column] = response

        return self.df

    async def _run_batch_async(self, batch_prompt: str) -> List[str]:
        """
        Processes a batch of prompts asynchronously.

        Args:
            batch_prompt (str): Concatenated prompt string.

        Returns:
            List[str]: List of LLM responses.
        """
        response = await self.runner.run(batch_prompt)
        return response

    def reset_responses(self, response_column: str = "llm_response") -> pd.DataFrame:
        """
        Resets the response column in the DataFrame by setting it to None.

        Args:
            response_column (str, optional): The name of the column to reset.

        Returns:
            pd.DataFrame: The updated DataFrame with the response column reset.
        """
        if response_column in self.df.columns:
            self.df[response_column] = None
        return self.df

    def _run_async_prompts(
        self, row_indices: List[int], prompt_column: str, response_column: str
    ) -> pd.DataFrame:
        """
        Helper method that runs LLM calls asynchronously in parallel.
        """

        async def process_row(idx: Union[int, str]) -> None:
            prompt_value = self.df.at[idx, prompt_column]
            if prompt_value:
                response = await self.runner.run(str(prompt_value))
                self.df.at[idx, response_column] = response

        async def main():
            tasks = [process_row(idx) for idx in row_indices]
            await asyncio.gather(*tasks)

        asyncio.run(main())
        return self.df
