from gaganrobot import gaganrobot, Message, Config, versions, get_version


@gaganrobot.on_cmd("repo", about={'header': "get repo link and details"})
async def see_repo(message: Message):
    """see repo"""
    output = f"""
**Hey**, __I am using__ 🔥 **GaganRobot** 🔥

    __Durable as a Serge__

• **gaganrobot version** : `{get_version()}`
• **license** : {versions.__license__}
• **copyright** : {versions.__copyright__}
• **repo** : [GaganRobot]({Config.UPSTREAM_REPO})
"""
    await message.edit(output)
