# pylint: disable=missing-module-docstring

__all__ = ['GetCLogger']

from gaganrobot import logging
from ...ext import RawClient
from ... import types

_LOG = logging.getLogger(__name__)
_LOG_STR = "<<<!  #####  %s  #####  !>>>"


class GetCLogger(RawClient):  # pylint: disable=missing-class-docstring
    def getCLogger(self, name: str) -> 'types.new.ChannelLogger':  # pylint: disable=invalid-name
        """ This returns new channel logger object """
        _LOG.debug(_LOG_STR, f"Creating CLogger => {name}")
        return types.new.ChannelLogger(self, name)
