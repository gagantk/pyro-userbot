from gaganrobot import gaganrobot, Message


@gaganrobot.on_cmd("cancel", about={
    'header': "Reply this to message you want to cancel",
    'flags': {'-a': "cancel all tasks"}})
async def cancel_(message: Message):
    if '-a' in message.flags:
        ret = Message._call_all_cancel_callbacks()  # pylint: disable=protected-access
        if ret == 0:
            await message.err("nothing found to cancel", show_help=False)
        return
    replied = message.reply_to_message  # type: Message
    if replied:
        if not replied._call_cancel_callbacks():  # pylint: disable=protected-access
            await message.err("nothing found to cancel", show_help=False)
    else:
        await message.err("source not provided !", show_help=False)
