__all__ = ['Terminate']

from ...ext import RawClient


class Terminate(RawClient):  # pylint: disable=missing-class-docstring
    async def terminate(self) -> None:
        """ terminate gaganrobot """
        if not self.no_updates:
            for task in self.dispatcher.handler_worker_tasks:
                task.cancel()
            self.dispatcher.handler_worker_tasks.clear()
        await super().terminate()
