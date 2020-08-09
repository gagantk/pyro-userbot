# pylint: disable=missing-module-docstring

__all__ = ['Conversation']

from typing import Union

from ... import types


class Conversation:  # pylint: disable=missing-class-docstring
    def conversation(self,
                     chat_id: Union[str, int],
                     *, timeout: Union[int, float] = 10,
                     limit: int = 10) -> 'types.new.Conversation':
        """\nThis returns new conversation object.

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.
                For your personal cloud (Saved Messages)
                you can simply use "me" or "self".
                For a contact that exists in your Telegram address book
                you can use his phone number (str).

            timeout (``int`` | ``float`` | , *optional*):
                set conversation timeout.
                defaults to 10.

            limit (``int`` | , *optional*):
                set conversation message limit.
                defaults to 10.
        """
        return types.new.Conversation(self, chat_id, timeout, limit)