#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import logging

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logging.getLogger('pyrogram').setLevel(logging.WARNING)

if bool(os.environ.get('ENV', False)):
    from myrobot.sample_config import Config
else:
    from myrobot.config import Development as Config

LOGGER = logging.getLogger(__name__)
API_ID = Config.API_ID
API_HASH = Config.API_HASH
HU_STRING_SESSION = Config.HU_STRING_SESSION
COMMAND_HANDLER = Config.COMMAND_HANDLER
TMP_DOWNLOAD_DIRECTORY = Config.TMP_DOWNLOAD_DIRECTORY
if not os.path.isdir(TMP_DOWNLOAD_DIRECTORY):
    os.makedirs(TMP_DOWNLOAD_DIRECTORY)
MAX_MESSAGE_LENGTH = Config.MAX_MESSAGE_LENGTH
