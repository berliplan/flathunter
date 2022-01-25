from importlib import util
import asyncio
import logging
from flathunter.abstract_processor import Processor
from nio import (AsyncClient, SyncResponse, RoomMessageText)

class SenderMatrix(Processor):
    """Expose processor that sends Matrix messages"""
    __log__ = logging.getLogger('flathunt')

    def __init__(self, config):
        self.config = config
        self.server = self.config.get('matrix', dict()).get('server', '')
        self.user_name = self.config.get('matrix', dict()).get('user_name', '')
        self.password = self.config.get('matrix', dict()).get('password', '')
        self.room_id = self.config.get('matrix', dict()).get('room_id', '')

    def process_expose(self, expose):
        """Send a message to a user describing the expose"""
        message = self.config.get('message', "").format(
            title=expose['title'],
            rooms=expose['rooms'],
            size=expose['size'],
            price=expose['price'],
            url=expose['url'],
            address=expose['address'],
            durations="" if 'durations' not in expose else expose['durations']).strip()
        self.send_msg(message)
        return expose

    def send_msg(self, message):
        """Send messages to the matrix room"""
        self.__log__.debug(('room_id:', self.room_id))
        self.__log__.debug(('message', message))
        client = AsyncClient(
            self.server, self.user_name
        )

        async def main():
            await client.login(self.password)
            await client.room_send(
                room_id=self.room_id,
                message_type="m.room.message",
                content={
                    "msgtype": "m.text",
                    "body": message
                }
            )
            await client.close()

        asyncio.get_event_loop().run_until_complete(main())
