# pylint: disable=missing-module-docstring

import os

from gaganrobot import gaganrobot


async def _worker() -> None:
    chat_id = int(os.environ.get("CHAT_ID") or 0)
    type_ = 'unofficial' if os.path.exists("../gaganrobot/plugins/unofficial") else 'main'
    await gaganrobot.send_message(chat_id, f'`{type_} build completed !`')

if __name__ == "__main__":
    gaganrobot.begin(_worker())
    print('gaganrobot test has been finished!')
