from pyrogram import Client, Filters
from pyrogram.client.handlers.handler import Handler
from myrobot import (COMMAND_HANDLER, LOGGER)
from pathlib import Path
from importlib import reload, import_module
import os


@Client.on_message(Filters.command(['load', 'install'], COMMAND_HANDLER))
async def load_plugin(client, message):
    status_message = await message.reply('Processing...')
    try:
        if message.reply_to_message is not None:
            downloaded_plugin_name = await message.reply_to_message.download(file_name='./plugins/')
            if downloaded_plugin_name is not None:
                relative_path_for_dlpn = os.path.relpath(
                    downloaded_plugin_name, os.getcwd())
                loaded_count = 0
                path = Path(relative_path_for_dlpn)
                module_path = '.'.join(path.parent.parts + (path.stem,))
                module = reload(import_module(module_path))
                for name in vars(module).keys():
                    try:
                        handler, group = getattr(module, name).handler
                        if isinstance(handler, Handler) and isinstance(group, int):
                            client.add_handler(handler, group)
                            LOGGER.info(
                                f'[{client.session_name}] [LOAD] {type(handler).__name__}("{name}") in group {group} from "{module_path}"')
                            loaded_count += 1
                    except Exception:
                        pass
                await status_message.edit(f'Installed {loaded_count} commands / plugins.')
    except Exception as e:
        await status_message.edit(f'ERROR: <code>{e}</code>')
