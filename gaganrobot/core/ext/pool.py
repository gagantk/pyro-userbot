# pylint: disable=missing-module-docstring

__all__ = ['submit_thread', 'run_in_thread']

import asyncio
from typing import Any, Callable
from concurrent.futures import ThreadPoolExecutor, Future
from functools import wraps, partial

from gaganrobot import logging, Config

_LOG = logging.getLogger(__name__)
_LOG_STR = "<<<!  ||||  %s  ||||  !>>>"
_EXECUTOR = ThreadPoolExecutor(Config.WORKERS)


def submit_thread(func: Callable[..., Any], *args: Any, **kwargs: Any) -> Future:
    """ submit thread to thread pool """
    return _EXECUTOR.submit(func, *args, **kwargs)


def run_in_thread(func: Callable[..., Any]) -> Callable[..., Any]:
    """ run in a thread """
    @wraps(func)
    async def wrapper(*args: Any, **kwargs: Any) -> Any:
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(_EXECUTOR, partial(func, *args, **kwargs))
    return wrapper


def _stop():
    _EXECUTOR.shutdown(wait=False)
    # pylint: disable=protected-access
    _LOG.info(_LOG_STR, f"Stopped Pool : {_EXECUTOR._max_workers} Workers")


# pylint: disable=protected-access
_LOG.info(_LOG_STR, f"Started Pool : {_EXECUTOR._max_workers} Workers")
