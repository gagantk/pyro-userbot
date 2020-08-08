"""Get info about the replied user
Syntax: .whois """
from datetime import datetime
import time

from pyrogram import Client, Filters

from myrobot import COMMAND_HANDLER
from myrobot.helper_functions.extract_user import extract_user


@Client.on_message(Filters.command(['whois', 'info', 'id'], COMMAND_HANDLER))
async def who_is(client, message):
    status_message = await message.reply_text('Gathering info...')
    from_user = None
    from_user_id, _ = extract_user(message)
    try:
        user_id = from_user_id
        if not str(user_id).startswith('@'):
            user_id = int(user_id)
        from_user = await client.get_users(user_id)
    except Exception as e:
        await status_message.edit(str(e))
        return
    if from_user is None:
        await status_message.edit('No valid user_id / message specified.')
    else:
        message_out_str = ''
        message_out_str += f'ID: <code>{from_user.id}</code>\n'
        message_out_str += f'First Name: <a href="tg://user?id={from_user.id}">'
        message_out_str += from_user.first_name or ''
        if from_user.last_name:
            message_out_str += f'</a>\nLast Name: {from_user.last_name or ""}\n'
        if from_user.dc_id:
            message_out_str += f'</a>\nDC ID: <code>{from_user.dc_id or ""}</code>\n'
        if message.chat.type in (('supergroup', 'channel')):
            chat_member_p = await message.chat.get_member(from_user.id)
            joined_date = datetime.fromtimestamp(
                chat_member_p.joined_date or time.time()).strftime('%d-%m-%Y %H:%M:%S')
            message_out_str += f'<b>Joined On</b>: <code>{joined_date}</code>\n'
        chat_photo = from_user.photo
        if chat_photo:
            local_user_photo = await client.download_media(message=chat_photo.big_file_id)
            await message.reply_photo(photo=local_user_photo, quote=True, caption=message_out_str, parse_mode='html', disable_notification=True)
            os.remove(local_user_photo)
        else:
            await message.reply_text(text=message_out_str, quote=True, parse_mode='html', disable_notification=True)
        await status_message.delete()
        await message.delete()
