import asyncio
import logging

from aiogram import Bot
from aiogram.utils.exceptions import TelegramAPIError

from woltdater.consts import VENUE_OPEN_MSG, UPDATE_INTERVAL_IN_SECONDS
from woltdater.plugins import AbstractMemoryPlugin
from woltdater.utils.wolt import is_venue_available_status

def get_restaurant_symbol_from_url(restaurant_url: str) -> str:
    """
    Get the restaurant symbol from it URL
    """
    return restaurant_url.rsplit('/')[-1]


async def update_subscriber(bot: Bot, chat_id: int, memory_plugin: AbstractMemoryPlugin, restaurant_symbol: str):
    """
    Update subscriber and unsubscribe him for the specific restaurant
    """
    try:
        await bot.send_message(chat_id=chat_id, text=VENUE_OPEN_MSG.format(restaurant_symbol=restaurant_symbol))
    except TelegramAPIError:
        logging.exception(f'Unable to update chat {chat_id}')
    finally:
        await memory_plugin.unsubscribe(restaurant_symbol, chat_id)


async def update_forever(bot: Bot, memory_plugin: AbstractMemoryPlugin):
    """
    Clients updater
    """
    while True:
        for restaurant_symbol in await memory_plugin.get_all_restaurants():
            logging.debug(f'Checking if {restaurant_symbol} is now open!')
            if await is_venue_available_status(restaurant_symbol):
                logging.info(f'{restaurant_symbol} is now open! Updating subscribers....')
                for chat_id in await memory_plugin.get_chat_ids_for_restaurant(restaurant_symbol):
                    await update_subscriber(bot, chat_id, memory_plugin, restaurant_symbol)
        await asyncio.sleep(UPDATE_INTERVAL_IN_SECONDS)
