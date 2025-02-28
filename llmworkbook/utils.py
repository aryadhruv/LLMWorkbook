import asyncio
from functools import wraps
from typing import Callable, Coroutine

import nest_asyncio


def sync_to_async(func: Coroutine) -> Callable:
    """
    A decorator to make an asynchronous function callable in a synchronous context.

    Args:
        func (coroutine): The asynchronous function to wrap.

    Returns:
        callable: A function that can be called synchronously.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:  # No running event loop
            loop = None

        if loop and loop.is_running():
            # If there's already an event loop running (e.g., in Jupyter Notebook)

            nest_asyncio.apply()  # Apply patch for nested loops
            return loop.run_until_complete(func(*args, **kwargs))
        # If no loop is running, use asyncio.run
        return asyncio.run(func(*args, **kwargs))

    return wrapper
