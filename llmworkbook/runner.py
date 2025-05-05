"""
Runner module to handle the actual LLM call.
"""

from .config import LLMConfig
from .utils import sync_to_async
from .providers import call_llm_ollama, call_llm_openai, call_llm_gpt4all, call_llm_anthropic
from rich import print


class LLMRunner:
    """
    LLMRunner handles calling the LLM provider using the configuration.
    """

    def __init__(self, config: LLMConfig) -> None:
        """
        Args:
            config (LLMConfig): The configuration object for the LLM.
        """
        self.config = config
        print("[bold green]Runner init...")

    async def run(self, prompt: str) -> str:
        """
        Entry point for calling any LLM provider.

        Args:
            prompt (str): The user prompt to send to the LLM.

        Returns:
            str: The LLM response text.
        """
        provider = self.config.provider.lower()
        print("[bold magenta]Using provider  - %s" % provider)

        if provider == "openai":
            return await call_llm_openai(self.config, prompt)

        if provider == "ollama":
            # Check if 'url' is defined in self.config.options
            url = self.config.options.get("url")

            # Call the function conditionally
            if url:
                return await call_llm_ollama(self.config, prompt, url=url)
            else:
                return await call_llm_ollama(self.config, prompt)

        if provider == "gpt4all":
            # Check if 'url' is defined in self.config.options
            url = self.config.options.get("url")

            # Call the function conditionally
            if url:
                return await call_llm_gpt4all(self, prompt, url=url)
            else:
                return await call_llm_gpt4all(self, prompt)
            
        
        if provider == "anthropic":
            return await call_llm_anthropic(self.config, prompt)

        raise NotImplementedError(f"Provider {provider} is not supported yet.")

    @sync_to_async
    async def run_sync(self, prompt: str) -> str:
        """
        Synchronous wrapper for simpler usage.

        Args:
            prompt (str): The user prompt.

        Returns:
            str: The LLM response text.
        """
        return await self.run(prompt)
