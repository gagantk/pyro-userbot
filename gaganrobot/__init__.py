# pylint: disable=missing-module-docstring

from gaganrobot.logger import logging  # noqa
from gaganrobot.config import Config, get_version  # noqa
from gaganrobot.core import (  # noqa
    GaganRobot, filters, Message, get_collection, pool)

gaganrobot = GaganRobot()  # gaganrobot is the client name
