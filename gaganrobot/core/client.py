# pylint: disable=missing-module-docstring

__all__ = ['GaganRobot']

import time
import signal
import asyncio
import importlib
from types import ModuleType
from typing import List, Awaitable, Any, Optional, Union

from pyrogram import idle

from gaganrobot import logging, Config, logbot
from gaganrobot.utils import time_formatter
from gaganrobot.utils.exceptions import GaganRobotBotNotFound
from gaganrobot.plugins import get_all_plugins
from .methods import Methods
from .ext import RawClient, pool

_LOG = logging.getLogger(__name__)
_LOG_STR = "<<<!  #####  %s  #####  !>>>"

_IMPORTED: List[ModuleType] = []
_INIT_TASKS: List[asyncio.Task] = []
_START_TIME = time.time()


def _shutdown() -> None:
    _LOG.info(_LOG_STR, 'received stop signal, cancelling tasks ...')
    for task in asyncio.all_tasks():
        task.cancel()
    _LOG.info(_LOG_STR, 'all tasks cancelled !')


async def _complete_init_tasks() -> None:
    if not _INIT_TASKS:
        return
    await asyncio.gather(*_INIT_TASKS)
    _INIT_TASKS.clear()


class _AbstractGaganRobot(Methods, RawClient):
    @property
    def is_bot(self) -> bool:
        """ returns client is bot or not """
        if self._bot is not None:
            return hasattr(self, 'ubot')
        if Config.BOT_TOKEN:
            return True
        return False

    @property
    def uptime(self) -> str:
        """ returns gaganrobot uptime """
        return time_formatter(time.time() - _START_TIME)

    async def finalize_load(self) -> None:
        """ finalize the plugins load """
        await asyncio.gather(_complete_init_tasks(), self.manager.init())

    async def load_plugin(self, name: str, reload_plugin: bool = False) -> None:
        """ Load plugin to GaganRobot """
        _LOG.debug(_LOG_STR, f"Importing {name}")
        _IMPORTED.append(
            importlib.import_module(f"gaganrobot.plugins.{name}"))
        if reload_plugin:
            _IMPORTED[-1] = importlib.reload(_IMPORTED[-1])
        plg = _IMPORTED[-1]
        self.manager.update_plugin(plg.__name__, plg.__doc__)
        if hasattr(plg, '_init'):
            # pylint: disable=protected-access
            if asyncio.iscoroutinefunction(plg._init):
                _INIT_TASKS.append(
                    asyncio.get_event_loop().create_task(plg._init()))
        _LOG.debug(
            _LOG_STR, f"Imported {_IMPORTED[-1].__name__} Plugin Successfully")

    async def _load_plugins(self) -> None:
        _IMPORTED.clear()
        _INIT_TASKS.clear()
        logbot.edit_last_msg("Importing All Plugins", _LOG.info, _LOG_STR)
        for name in get_all_plugins():
            try:
                await self.load_plugin(name)
            except ImportError as i_e:
                _LOG.error(_LOG_STR, f"[{name}] - {i_e}")
        await self.finalize_load()
        _LOG.info(_LOG_STR, f"Imported ({len(_IMPORTED)}) Plugins => "
                  + str([i.__name__ for i in _IMPORTED]))

    async def reload_plugins(self) -> int:
        """ Reload all Plugins """
        self.manager.clear_plugins()
        reloaded: List[str] = []
        _LOG.info(_LOG_STR, "Reloading All Plugins")
        for imported in _IMPORTED:
            try:
                reloaded_ = importlib.reload(imported)
            except ImportError as i_e:
                _LOG.error(_LOG_STR, i_e)
            else:
                reloaded.append(reloaded_.__name__)
        _LOG.info(_LOG_STR, f"Reloaded {len(reloaded)} Plugins => {reloaded}")
        await self.finalize_load()
        return len(reloaded)


class _GaganRobotBot(_AbstractGaganRobot):
    """ GaganRobotBot, the bot """

    def __init__(self, **kwargs) -> None:
        _LOG.info(_LOG_STR, "Setting GaganRobotBot Configs")
        super().__init__(session_name=":memory:", **kwargs)

    @property
    def ubot(self) -> 'GaganRobot':
        """ returns userbot """
        return self._bot


class GaganRobot(_AbstractGaganRobot):
    """ GaganRobot, the userbot """

    def __init__(self, **kwargs) -> None:
        _LOG.info(_LOG_STR, "Setting GaganRobot Configs")
        kwargs = {
            'api_id': Config.API_ID,
            'api_hash': Config.API_HASH,
            'workers': Config.WORKERS
        }
        if Config.BOT_TOKEN:
            kwargs['bot_token'] = Config.BOT_TOKEN
        if Config.HU_STRING_SESSION and Config.BOT_TOKEN:
            RawClient.DUAL_MODE = True
            kwargs['bot'] = _GaganRobotBot(bot=self, **kwargs)
        kwargs['session_name'] = Config.HU_STRING_SESSION or ":memory:"
        super().__init__(**kwargs)

    @property
    def bot(self) -> '_GaganRobotBot':
        """ returns gaganrobotbot """
        if self._bot is None:
            if Config.BOT_TOKEN:
                return self
            raise GaganRobotBotNotFound("Need BOT_TOKEN ENV!")
        return self._bot

    async def start(self) -> None:
        """ start client and bot """
        pool._start()  # pylint: disable=protected-access
        _LOG.info(_LOG_STR, "Starting GaganRobot")
        await super().start()
        if self._bot is not None:
            _LOG.info(_LOG_STR, "Starting GaganRobotBot")
            await self._bot.start()
        await self._load_plugins()

    async def stop(self) -> None:  # pylint: disable=arguments-differ
        """ stop client and bot """
        if self._bot is not None:
            _LOG.info(_LOG_STR, "Stopping GaganRobotBot")
            await self._bot.stop()
        _LOG.info(_LOG_STR, "Stopping GaganRobot")
        await super().stop()
        await pool._stop()  # pylint: disable=protected-access

    def begin(self, coro: Optional[Awaitable[Any]] = None) -> None:
        """ start gaganrobot """
        loop = asyncio.get_event_loop()
        loop.add_signal_handler(signal.SIGHUP, _shutdown)
        loop.add_signal_handler(signal.SIGTERM, _shutdown)
        run = loop.run_until_complete
        try:
            run(self.start())
            loop = asyncio.get_event_loop()
            running_tasks: List[asyncio.Task] = []
            for task in self._tasks:
                running_tasks.append(loop.create_task(task()))
            if coro:
                _LOG.info(_LOG_STR, "Running Coroutine")
                run(coro)
            else:
                _LOG.info(_LOG_STR, "Idling GaganRobot")
                logbot.edit_last_msg("GaganRobot has Started Successfully !")
                logbot.end()
                idle()
            _LOG.info(_LOG_STR, "Exiting GaganRobot")
            for task in running_tasks:
                task.cancel()
            run(self.stop())
            run(loop.shutdown_asyncgens())
        except asyncio.exceptions.CancelledError:
            pass
        finally:
            if not loop.is_running():
                loop.close()
