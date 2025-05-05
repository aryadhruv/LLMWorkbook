"""
Configuration module for LLMs.
"""

from typing import Optional, Dict
from rich import print


class LLMConfig:  # pylint: disable=too-few-public-methods
    """
    LLM configuration object to store various LLM parameters.
    """

    def __init__(
        self,
        provider: str = "openai",
        api_key: Optional[str] = None,
        system_prompt: Optional[
            str
        ] = "You're an assistant, process the data for given prompt.",
        options: Optional[Dict[str, Optional[float]]] = None,
    ) -> None:
        """
        Initializes the LLM configuration.

        Args:
            provider (str): The name of the LLM provider. Available providers - openai, ollama, gpt4all, anthropic.
            api_key (str): The API key to authenticate requests to the LLM provider.
            system_prompt (str, optional): System-level prompt to guide the LLM.
            options (Dict, optional): Additional parameters for the model configuration, including:
                - model (str): Name or version of the LLM model. Default is "gpt-4o-mini".
                - temperature (float): Sampling temperature to control randomness. Default is 0.7.
                - max_tokens (int): Maximum tokens for the output. Default is 1024.
        """
        # Default options
        default_options = {
            "model": "gpt-4o-mini",
            "temperature": 0.7,
        }

        # Update defaults with provided options
        self.provider = provider
        self.api_key = api_key
        self.system_prompt = system_prompt
        self.options = {**default_options, **(options or {})}
        print("[bold green]Configurations set.")

    def to_dict(self) -> Dict:
        """
        Converts the configuration to a dictionary.

        Returns:
            Dict: The configuration as a dictionary.
        """
        return {
            "provider": self.provider,
            "api_key": self.api_key,
            "system_prompt": self.system_prompt,
            "options": self.options,
        }
