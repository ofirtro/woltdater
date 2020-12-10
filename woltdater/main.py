import asyncio
import logging
import os

import click
from aiogram import Bot, Dispatcher
from aiogram.utils import executor

from woltdater.consts import WOLTDATER_API_TOKEN_KEY
from woltdater.plugins import InMemoryPlugin
from woltdater.utils import setup_handlers
from woltdater.utils import update_forever

logging.basicConfig(level=logging.INFO)


@click.command()
@click.option('--api-token', default=os.environ.get(WOLTDATER_API_TOKEN_KEY), help='The bot API token', required=True)
def main(api_token: str):
    loop = asyncio.get_event_loop()
    memory_plugin = InMemoryPlugin()
    bot = Bot(token=api_token)
    dp = Dispatcher(bot)
    loop.create_task(update_forever(bot, memory_plugin))
    setup_handlers(dp, memory_plugin)
    executor.start_polling(dp, skip_updates=True)


if __name__ == "__main__":
    main()
