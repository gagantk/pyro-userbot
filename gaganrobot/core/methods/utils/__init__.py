# pylint: disable=missing-module-docstring

__all__ = ['Utils']

from .get_logger import GetLogger
from .get_channel_logger import GetCLogger


class Utils(GetLogger, GetCLogger):
    """ methods.utils """
