from gaganrobot import gaganrobot, Message


@gaganrobot.on_cmd("s", about={
    'header': "search commands in GAGANROBOT",
    'examples': "{tr}s wel"}, allow_channels=False)
async def search(message: Message):
    cmd = message.input_str
    if not cmd:
        await message.err("Enter any keyword to search in commands")
        return
    found = [i for i in sorted(list(gaganrobot.manager.enabled_commands)) if cmd in i]
    out_str = '    '.join(found)
    if found:
        out = f"**--I found ({len(found)}) commands for-- : `{cmd}`**\n\n`{out_str}`"
    else:
        out = f"__command not found for__ : `{cmd}`"
    await message.edit(text=out, del_in=0)
