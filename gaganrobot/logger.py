# pylint: disable=missing-module-docstring

__all__ = ['logging']

import logging
from logging.handlers import RotatingFileHandler

logging.basicConfig(level=logging.INFO,
                    format='[%(asctime)s - %(levelname)s] - %(name)s - %(message)s',
                    datefmt='%d-%b-%y %H:%M:%S',
                    handlers=[
                        RotatingFileHandler(
                            "logs/gaganrobot.log", maxBytes=(20480), backupCount=10),
                        logging.StreamHandler()
                    ])
logging.getLogger("pyrogram").setLevel(logging.WARNING)
logging.getLogger("pyrogram.client.parser.html").setLevel(logging.ERROR)
logging.getLogger('googleapiclient.discovery').setLevel(logging.WARNING)
