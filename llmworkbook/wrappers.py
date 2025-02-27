"""
Module to transform data for LLM readiness.

The three concrete implementations:

1) WrapDataFrame  - for pandas DataFrame
2) WrapDataArray  - for 2D array-like structures
3) WrapPromptList - for 1D lists (of prompts only)

All only handle the data source specifics.
"""

from abc import ABC, abstractmethod
from typing import List, Optional, Union

import numpy as np
from pandas import DataFrame, Series
from pandas.errors import InvalidColumnName
from rich import print


class BaseLLMWrapper(ABC):
    """
    An abstract base class providing common methods to transform and export data
    for LLM consumption.

    Methods to Implement in Child Classes:
        - _prepare_data_for_wrapping() -> DataFrame:
            This method should return a DataFrame of shape (n, m) containing the data
            columns that need to be wrapped. Typically, it excludes the 'prompt' column.
        - _get_prompt_series() -> Series:
            This method should return a single-column Series (or one-column DataFrame)
            holding the "prompt" values to wrap.
    """

    @abstractmethod
    def _prepare_data_for_wrapping(self) -> DataFrame:
        """
        Return a DataFrame containing only the data columns to be wrapped.
        """

    @abstractmethod
    def _get_prompt_series(self) -> Series:
        """
        Return a single-column Series of prompt data.
        """

    def _wrap_data_row(self, row: Series) -> str:
        """
        Wrap a row of data into the <data><cell>...</cell></data> format.

        Args:
            row (Series): A single row containing data columns.

        Returns:
            str: The wrapped string for the data row.
        """
        if row.empty:
            # If there are no data columns, return an empty <data></data> block
            return "<data></data>"
        cells = "\n".join(f"  <cell>{value}</cell>" for value in row)
        return f"<data>\n{cells}\n</data>"

    def _wrap_prompt(self, value) -> str:
        """
        Wrap a prompt value into the <prompt>...</prompt> format.

        Args:
            value: The prompt value to wrap.

        Returns:
            str: The wrapped string for the prompt.
        """
        return f"<prompt>{value}</prompt>"

    def _generate_transformed_content(self) -> DataFrame:
        """
        Generate the final, LLM-ready DataFrame by combining wrapped data rows and prompt rows.

        Returns:
            DataFrame: A single-column DataFrame with the wrapped output.
        """
        data_df = self._prepare_data_for_wrapping()
        prompt_series = self._get_prompt_series()

        # Wrap the data rows
        data_content = data_df.apply(self._wrap_data_row, axis=1)

        # Wrap the prompt column
        prompt_content = prompt_series.apply(self._wrap_prompt)

        # Combine data and prompt columns into a single column
        transformed_content = data_content + prompt_content

        return DataFrame({"wrapped_output": transformed_content})

    def wrap(self) -> DataFrame:
        """
        Wrap the data for LLM consumption.

        Returns:
            DataFrame: A DataFrame with transformed (wrapped) content.
        """
        print("[bold green]Data Wrapped.")
        return self._generate_transformed_content()

    def transform_and_export(self, file_path: str, file_format: str = "excel") -> None:
        """
        Transform the data and export it to a specified file.

        Args:
            file_path (str): The path to save the exported file.
            file_format (str): The format of the file ('csv', 'json', or 'excel').

        Raises:
            ValueError: If an unsupported file format is provided.
        """
        transformed_df = self.wrap()
        if file_format == "csv":
            transformed_df.to_csv(file_path, index=False)
        elif file_format == "json":
            transformed_df.to_json(file_path, orient="records")
        elif file_format == "excel":
            transformed_df.to_excel(file_path, index=False, engine="openpyxl")
        else:
            raise ValueError("Unsupported file format. Use 'csv', 'json', or 'excel'.")

    def preview(self, n: int = 5) -> None:
        """
        Display a preview of the transformed output.

        Args:
            n (int): Number of rows to preview. Default is 5.
        """
        transformed_df = self.wrap()
        print(transformed_df.head(n))


class WrapDataFrame(BaseLLMWrapper):
    """
    A class to wrap DataFrame data for LLM consumption.

    Attributes:
        df (DataFrame): The input DataFrame.
        prompt_column (str): The column containing prompt data.
        data_columns (Optional[List[str]]): The columns containing the data to wrap.
        use_column_header (bool): If True, use individual column headers as cell tags.
        column_header_index (int): The starting index from which to use column headers for wrapping.
                                   Cells before this index will use the default <cell> tag.
    """

    def __init__(
        self,
        df: DataFrame,
        prompt_column: str = "prompt_column",
        data_columns: Optional[List[str]] = None,
        use_column_header: bool = False,
        column_header_index: int = 0,
    ) -> None:
        """
        Initialize the WrapDataFrame object.

        Args:
            df (DataFrame): The input DataFrame.
            prompt_column (str): The column containing prompt data.
            data_columns (Optional[List[str]]): The columns containing the data to wrap.
            use_column_header (bool): If True, wrap each cell with its corresponding column header.
            column_header_index (int): The index from which column headers should be used as tags.
                                       Cells before this index will use the default <cell> tag.
        """
        self.df = df
        self.prompt_column = prompt_column
        self.data_columns = data_columns or []
        self.use_column_header = use_column_header
        self.column_header_index = column_header_index
        self._validate_columns()

        print("[bold magenta]Dataframe wrapper init...")

    def _validate_columns(self) -> None:
        """
        Validate that the required columns exist in the DataFrame.

        Raises:
            InvalidColumnName: If required columns are missing from the DataFrame.
        """
        if self.prompt_column not in self.df.columns:
            raise InvalidColumnName(
                f"Prompt column '{self.prompt_column}' not found in the DataFrame."
            )

        missing_columns = [
            col for col in self.data_columns if col not in self.df.columns
        ]
        if missing_columns:
            raise InvalidColumnName(
                f"Data columns {missing_columns} not found in the DataFrame."
            )

    def _prepare_data_for_wrapping(self) -> DataFrame:
        """
        Return a DataFrame of only the data columns that we need to wrap.
        """
        # Drop the prompt column from the DataFrame to isolate data columns
        data_df = self.df.drop(columns=[self.prompt_column], errors="ignore")

        # If user provided specific data columns, use them; otherwise, use all
        if self.data_columns:
            data_df = data_df[self.data_columns]

        return data_df

    def _get_prompt_series(self) -> Series:
        """
        Return the prompt column as a Series.
        """
        return self.df[self.prompt_column]

    def _wrap_data_row(self, row: Series) -> str:
        """
        Wrap a row of data into the <data> tag with cells wrapped either in generic <cell> tags
        or in individual column header tags, based on the use_column_header flag.

        Args:
            row (Series): A single row of data.

        Returns:
            str: The wrapped data row.
        """
        if row.empty:
            return "<data></data>"
        if not self.use_column_header:
            return super()._wrap_data_row(row)
        else:
            wrapped_cells = []
            for idx, (col, value) in enumerate(row.items()):
                tag = col if idx >= self.column_header_index else "cell"
                wrapped_cells.append(f"  <{tag}>{value}</{tag}>")
            cells_str = "\n".join(wrapped_cells)
            return f"<data>\n{cells_str}\n</data>"


class WrapDataArray(BaseLLMWrapper):
    """
    A class to wrap 2D array-like data for LLM consumption.

    Attributes:
        arr (Union[np.ndarray, list]): The input array (or list of lists).
        prompt_index (int): The index (column) containing prompt data in the array.
        data_indices (Optional[List[int]]): The indices (columns) containing data to wrap.
    """

    def __init__(
        self,
        arr: Union[np.ndarray, list],
        prompt_index: int = 0,
        data_indices: Optional[List[int]] = None,
    ) -> None:
        """
        Initialize the WrapDataArray object.

        Args:
            arr (Union[np.ndarray, list]): The input array or list of lists.
            prompt_index (int): The index (column) containing prompt data.
            data_indices (Optional[List[int]]): The columns (by index) with data to wrap.
        """
        # Convert list to numpy array if not already
        if isinstance(arr, list):
            arr = np.array(arr, dtype=object)

        if len(arr.shape) != 2:
            raise ValueError(
                "Input arr must be a 2D structure (e.g., rows and columns)."
            )

        self.arr = arr
        self.prompt_index = prompt_index
        self.data_indices = data_indices or []
        self._validate_indices()

        # Convert the array into a DataFrame for easier manipulation
        # We'll assign generic column names as col_0, col_1, etc.
        column_names = [f"col_{i}" for i in range(self.arr.shape[1])]
        self.temp_df = DataFrame(self.arr, columns=column_names)

        print("[bold magenta]Data Array wrapper init...")

    def _validate_indices(self) -> None:
        """
        Validate that the required indices exist in the array.

        Raises:
            IndexError: If required columns (prompt or data) are out of bounds.
        """
        num_columns = self.arr.shape[1]

        if not 0 <= self.prompt_index < num_columns:
            raise IndexError(
                f"Prompt index {self.prompt_index} is out of bounds "
                f"for an array with {num_columns} columns."
            )

        for idx in self.data_indices:
            if idx < 0 or idx >= num_columns:
                raise IndexError(
                    f"Data index {idx} is out of bounds for an array with {num_columns} columns."
                )

    def _prepare_data_for_wrapping(self) -> DataFrame:
        """
        Return a DataFrame of only the data columns to wrap, excluding the prompt column.
        """
        # Drop the prompt column from the DataFrame
        data_df = self.temp_df.drop(
            columns=[f"col_{self.prompt_index}"], errors="ignore"
        )

        # If the user specified data_indices, keep only those columns
        if self.data_indices:
            data_col_names = [f"col_{idx}" for idx in self.data_indices]
            data_df = data_df[data_col_names]

        return data_df

    def _get_prompt_series(self) -> Series:
        """
        Return a Series of prompt data from the specified prompt_index column.
        """
        prompt_col_name = f"col_{self.prompt_index}"
        return self.temp_df[prompt_col_name]


class WrapPromptList(BaseLLMWrapper):
    """
    A class to wrap a 1D list of prompts for LLM consumption.

    This is useful if you only have a list of prompts (no associated data columns).
    Example:
        prompts = ["Hello", "How are you?", "Please summarize this text..."]
        wrapper = WrapPromptList(prompts)
        df = wrapper.wrap()
    """

    def __init__(self, prompts: List[str]) -> None:
        """
        Initialize the WrapPromptList object.

        Args:
            prompts (List[str]): A list of prompt strings.
        """
        self.prompts = prompts

        print("[bold magenta]Prompt wrapper init...")

    def _prepare_data_for_wrapping(self) -> DataFrame:
        """
        Return an empty DataFrame, since we have no data columns to wrap.
        However, we need the same number of rows as the length of our prompts
        so that alignment (row-by-row) works in the base class methods.
        """
        return DataFrame(index=range(len(self.prompts)))

    def _get_prompt_series(self) -> Series:
        """
        Return the list of prompts as a pandas Series.
        """
        return Series(self.prompts)
