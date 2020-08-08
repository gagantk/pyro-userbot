from pyrogram import Client, Filters

from myrobot import COMMAND_HANDLER


def aesthetify(string):
    PRINTABLE_ASCII = range(0x21, 0x7f)
    for c in string:
        c = ord(c)
        if c in PRINTABLE_ASCII:
            c += 0xFF00 - 0x20
        elif c == ord(' '):
            c = 0x3000
        yield chr(c)


@Client.on_message(Filters.command(['ae'], COMMAND_HANDLER))
async def asthetic(client, message):
    status_message = await message.reply_text('...')
    text = ''.join(str(e) for e in message.command[1:])
    text = ''.join(aesthetify(text))
    await status_message.edit(text)
