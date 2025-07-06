"""
Provider (LLM) module that contains routing to various LLM providers that LLMWORKBOOK supports
"""

import os
from typing import Optional
import aiohttp

from .config import LLMConfig

from openai import OpenAI
import anthropic
from anthropic.types import Message

from rich import print


async def call_llm_openai(config: LLMConfig, prompt: str) -> str:
    """
    Calls OpenAI's completion/chat endpoint asynchronously.

    Args:
        prompt (str): The user prompt to send to the LLM.

    Returns:
        str: The LLM response text.
    """

    if config.options.get("model_name"):
        print(
            "[bold red]⚠️ 'model_name' is deprecated![/bold red] Use [green]'model'[/green] instead."
        )
        raise DeprecationWarning("'model_name' is deprecated, use 'model' instead.")

    messages = []
    if config.system_prompt:
        messages.append({"role": "system", "content": config.system_prompt})
    messages.append({"role": "user", "content": prompt})

    client = OpenAI(api_key=config.api_key or os.environ["OPENAI_API_KEY"])

    options = {
        "model": config.options.get("model", "gpt-4o-mini"),
        "input": prompt,
        "instructions" : config.system_prompt if config.system_prompt else "Respond with emoji only :"
    }
    options.update({k: v for k, v in config.options.items() if k not in options})

    response = client.responses.create(**options)

    try:
        return response.output[0].content[0].text
    except (KeyError, IndexError):
        return str(response)


async def call_llm_ollama(config, prompt: str, url: Optional[str] = None) -> str:
    """
    Calls Ollama's completion/chat endpoint asynchronously.

    Args:
        prompt (str): The user prompt to send to the LLM.
        url (str): The URL of the Ollama server.

    Returns:
        str: The LLM response text.
    """
    # Default URL if none is provided
    if url is None:
        url = "http://localhost:11434"

    messages = []
    if config.system_prompt:
        messages.append({"role": "system", "content": config.system_prompt})
    messages.append({"role": "user", "content": prompt})

    payload = {
        "model": config.options.get("model", "default-model"),
        "prompt": str(messages),
        "stream": False,
    }

    valid_options = [
        "suffix",
        "images",
        "format",
        "options",
        "system",
        "template",
        "stream",
        "raw",
        "keep_alive",
        "context",
    ]
    for option in valid_options:
        if option in config.options:
            payload[option] = config.options[option]

    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(f"{url}/api/generate", json=payload) as response:
                if response.status == 200:
                    completion = await response.json()
                    return completion["response"]
                else:
                    return f"Error: {response.status}, {await response.text()}"
        except Exception as e:
            return f"Exception: {str(e)}"


async def call_llm_gpt4all(config, prompt: str, url: Optional[str] = None) -> str:
    """
    Calls GPT4ALL's completion/chat endpoint asynchronously.

    Args:
        prompt (str): The user prompt to send to the LLM.
        url (str): The URL of the GPT4ALL server.

    Returns:
        str: The LLM response text.
    """
    # Default URL if none is provided
    if url is None:
        url = "http://localhost:4891"  # Default GPT4ALL server URL

    messages = []
    if config.system_prompt:
        messages.append({"role": "system", "content": config.system_prompt})
    messages.append({"role": "user", "content": prompt})

    payload = {
        "model": config.options.get("model", "default-model"),
        "messages": messages,
    }

    # TODO - Expand options for OpenAI
    valid_options = ["max_tokens", "temperature"]
    for option in valid_options:
        if option in config.options:
            payload[option] = config.options[option]

    print(payload)
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(
                f"{url}/v1/chat/completions", json=payload
            ) as response:
                if response.status == 200:
                    completion = await response.json()
                    return (
                        completion.get("choices", [{}])[0]
                        .get("message", {})
                        .get("content", "")
                    )
                else:
                    return f"Error: {response.status}, {await response.text()}"
        except Exception as e:
            return f"Exception: {str(e)}"

async def call_llm_anthropic(config: LLMConfig, prompt: str) -> str:
    """
    Asynchronously calls Anthropic's Claude chat API.

    Args:
        config (LLMConfig): Configuration including API key, model, system prompt, and other options.
        prompt (str): The user message to send.

    Returns:
        str: The content of Claude's response.
    """

    client = anthropic.Anthropic(
        api_key=config.api_key or os.environ.get("ANTHROPIC_API_KEY")
    )

    model = config.options.get("model", "claude-3-sonnet-20240229")
    max_tokens = config.options.get("max_tokens", 1024)

    messages = []
    if config.system_prompt:
        messages.append({"role": "system", "content": config.system_prompt})
    messages.append({"role": "user", "content": prompt})

    # Claude expects only user/assistant roles and the system prompt as a separate param
    response: Message = client.messages.create(
        model=model,
        max_tokens=max_tokens,
        system=config.system_prompt,
        messages=[{"role": m["role"], "content": m["content"]} for m in messages if m["role"] != "system"]
    )

    try:
        return response.content[0]["text"] if response.content else ""
    except Exception as e:
        return f"Error parsing Claude response: {e}"
