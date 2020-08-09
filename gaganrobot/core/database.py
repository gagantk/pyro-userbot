# pylint: disable=missing-module-docstring
__all__ = ['get_collection']

import asyncio
from typing import List

from motor.motor_asyncio import AsyncIOMotorClient
from motor.core import AgnosticClient, AgnosticDatabase, AgnosticCollection

from gaganrobot import logging, Config
from gaganrobot import logbot

_LOG = logging.getLogger(__name__)
_LOG_STR = "$$$>>> %s <<<$$$"

logbot.edit_last_msg("Connecting to Database ...", _LOG.info, _LOG_STR)

_MGCLIENT: AgnosticClient = AsyncIOMotorClient(Config.DB_URI)
_RUN = asyncio.get_event_loop().run_until_complete

if 'GaganRobot' in _RUN(_MGCLIENT.list_database_names()):
    _LOG.info(_LOG_STR, "GaganRobot Database Found :) => Now Logging to it...")
else:
    _LOG.info(
        _LOG_STR, "GaganRobot Database Not Found :( => Creating New Database...")

_DATABASE: AgnosticDatabase = _MGCLIENT["GaganRobot"]
_COL_LIST: List[str] = _RUN(_DATABASE.list_collection_names())


def get_collection(name: str) -> AgnosticCollection:
    """ Create or Get Collection from your database """
    if name in _COL_LIST:
        _LOG.debug(
            _LOG_STR, f"{name} Collection Found :) => Now Logging to it...")
    else:
        _LOG.debug(
            _LOG_STR, f"{name} Collection Not Found :( => Creating New Collection...")
    return _DATABASE[name]


logbot.del_last_msg()
