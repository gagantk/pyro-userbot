from gaganrobot import gaganrobot, Message, logging, Config, pool

_LEVELS = {
    'debug': logging.DEBUG,
    'info': logging.INFO,
    'warning': logging.WARNING,
    'error': logging.ERROR,
    'critical': logging.CRITICAL
}


@gaganrobot.on_cmd("logs", about={
    'header': "check gaganrobot logs",
    'flags': {
        '-h': "get heroku logs",
        '-l': "heroku logs lines limit : default 100"}}, allow_channels=False)
async def check_logs(message: Message):
    """ check logs """
    await message.edit("`checking logs ...`")
    if '-h' in message.flags and Config.HEROKU_APP:
        limit = int(message.flags.get('-l', 100))
        logs = await pool.run_in_thread(Config.HEROKU_APP.get_log)(lines=limit)
        await message.client.send_as_file(chat_id=message.chat.id,
                                          text=logs,
                                          filename='gaganrobot-heroku.log',
                                          caption=f'gaganrobot-heroku.log [ {limit} lines ]')
    else:
        await message.client.send_document(chat_id=message.chat.id,
                                           document="logs/gaganrobot.log",
                                           caption='gaganrobot.log')
    await message.delete()


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
