import time

from pyrogram import Client, Filters

from myrobot import COMMAND_HANDLER

ALIVE = 'ಸತ್ತಿಲ್ಲ...'
HELP = 'CAADAgAD6AkAAowucAABsFGHedLEzeUWBA'


@Client.on_message(Filters.command(['alive', 'start'], COMMAND_HANDLER))
async def check_alive(_, message):
    await message.reply_text(ALIVE)


@Client.on_message(Filters.command('help', COMMAND_HANDLER))
async def help_me(_, message):
    await message.reply_sticker(HELP)


@Client.on_message(Filters.command('ping', COMMAND_HANDLER))
async def ping(_, message):
    start_t = time.time()
    rm = await message.reply_text('...')
    end_t = time.time()
    time_taken_s = (end_t - start_t) * 1000
    await rm.edit(f'Pong!\n{time_taken_s:.3f} ms')
