import asyncio
import os
import time

from pyrogram import Client, Filters

from myrobot import MAX_MESSAGE_LENGTH, COMMAND_HANDLER


@Client.on_message(Filters.command('exec', COMMAND_HANDLER))
async def execution(_, message):
    cmd = message.text.split(' ', maxsplit=1)[1]

    reply_to_id = message.message_id
    if message.reply_to_message:
        reply_to_id = message.reply_to_message.message_id

    process = await asyncio.create_subprocess_shell(cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
    stdout, stderr = await process.communicate()
    e = stderr.decode()
    if not e:
        e = 'No Error'
    o = stdout.decode()
    if not o:
        o = 'No Output'

    OUTPUT = ''
    OUTPUT += f'<b>QUERY:</b>\n<u>Command</u>:\n<code>{cmd}</code>\n'
    OUTPUT += f'<u>PID</u>: <code>{process.pid}</code>\n\n'
    OUTPUT += f'<b>stderr</b>:\n<code>{e}</code>\n\n'
    OUTPUT += f'<b>stdout</b>:\n<code>{o}</code>'

    if len(OUTPUT) > MAX_MESSAGE_LENGTH:
        with open('exec.txt', 'w+', encoding='utf8') as out_file:
            out_file.write(str(OUTPUT))
        await message.reply_document(document='exec.txt', caption=cmd, disable_notification=True, reply_to_message_id=reply_to_id)
        os.remove('exec.txt')
    else:
        await message.reply_text(OUTPUT)
