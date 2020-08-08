import os


class Config():
    LOGGER = True
    API_ID = int(os.environ.get('API_ID', 12345))
    API_HASH = os.environ.get('API_HASH', None)
    HU_STRING_SESSION = os.environ.get('HU_STRING_SESSION', None)
    TMP_DOWNLOAD_DIRECTORY = os.environ.get(
        'TMP_DOWNLOAD_DIRECTORY', './DOWNLOADS/')
    COMMAND_HANDLER = os.environ.get('COMMAND_HANDLER', '.')
    MAX_MESSAGE_LENGTH = 4096


class Production(Config):
    LOGGER = False


class Development(Config):
    LOGGER = True
