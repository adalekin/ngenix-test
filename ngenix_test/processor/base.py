import asyncio


class BaseProcessor:
    name = ''

    def __init__(self, args, loop=None):
        self.args = args

        self.loop = loop

        if self.loop is None:
            self.loop = asyncio.get_event_loop()

    def run(self):
        raise NotImplementedError
