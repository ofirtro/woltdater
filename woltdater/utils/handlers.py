import logging

from aiogram import types, Dispatcher

from woltdater.consts import VENUE_OPEN_MSG, WILL_UPDATE_MSG, RESTAURANT_NOT_FOUND_MSG, WELCOME_MSG
from woltdater.exceptions import RestaurantWasNotFoundException
from woltdater.plugins import AbstractMemoryPlugin
from woltdater.utils.updater import get_restaurant_symbol_from_url
from woltdater.utils.wolt import is_venue_available_status


async def reply_welcome(message: types.message):
    await message.reply(WELCOME_MSG)


async def check_status(message: types.Message, memory_plugin: AbstractMemoryPlugin):
    """
    Gets message and subscribe client if needed
    """
    logging.info(f'Trying to get venue status for {message.text}')
    restaurant_symbol = get_restaurant_symbol_from_url(message.text.lower())
    try:
        venue_status = await is_venue_available_status(restaurant_symbol)
        if venue_status:
            await message.reply(VENUE_OPEN_MSG.format(restaurant_symbol=restaurant_symbol))
        else:
            await message.reply(WILL_UPDATE_MSG.format(restaurant_symbol=restaurant_symbol))
            await memory_plugin.subscribe(restaurant_symbol, message.chat.id)
    except RestaurantWasNotFoundException:
        await message.reply(RESTAURANT_NOT_FOUND_MSG)


def setup_handlers(dispatcher: Dispatcher, memory_plugin: AbstractMemoryPlugin):
    dispatcher.register_message_handler(reply_welcome, commands=['start', 'help'])
    dispatcher.register_message_handler(lambda message: check_status(message, memory_plugin))
