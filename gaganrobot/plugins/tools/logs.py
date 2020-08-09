import aiofiles

from gaganrobot import gaganrobot, Message, logging


@gaganrobot.on_cmd("logs", about={'header': "check gaganrobot logs"}, allow_channels=False)
async def check_logs(message: Message):
    """ check logs """
    await message.edit("`checking logs ...`")
    async with aiofiles.open("logs/gaganrobot.log", "r") as l_f:
        await message.edit_or_send_as_file(f"**GAGANROBOT LOGS** :\n\n`{await l_f.read()}`",
                                           filename='gaganrobot.log',
                                           caption='gaganrobot.log')

_LEVELS = {
    'debug': logging.DEBUG,
    'info': logging.INFO,
    'warning': logging.WARNING,
    'error': logging.ERROR,
    'critical': logging.CRITICAL
}


@gaganrobot.on_cmd("setlvl", about={
    'header': "set logger level, default to info",
    'types': ['debug', 'info', 'warning', 'error', 'critical'],
    'usage': "{tr}setlvl [level]",
    'examples': ["{tr}setlvl info", "{tr}setlvl debug"]})
async def set_level(message: Message):
    """ set logger level """
    await message.edit("`setting logger level ...`")
    level = message.input_str.lower()
    if level not in _LEVELS:
        await message.err("unknown level !")
        return
    for logger in (logging.getLogger(name) for name in logging.root.manager.loggerDict):
        logger.setLevel(_LEVELS[level])
    await message.edit(f"`successfully set logger level as` : **{level.upper()}**", del_in=3)
