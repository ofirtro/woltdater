import logging
import json

from aiogram import types, Dispatcher, Bot



from consts import VENUE_OPEN_MSG, WILL_UPDATE_MSG, RESTAURANT_NOT_FOUND_MSG, WELCOME_MSG
from exceptions import RestaurantWasNotFoundException
from plugins import AbstractMemoryPlugin
from utils.updater import get_restaurant_symbol_from_url
from utils.wolt import is_venue_available_status , search_vanue_by_name , get_vanue_by_id
# from woltdater.consts import VENUE_OPEN_MSG, WILL_UPDATE_MSG, RESTAURANT_NOT_FOUND_MSG, WELCOME_MSG
# from woltdater.exceptions import RestaurantWasNotFoundException
# from woltdater.plugins import AbstractMemoryPlugin
# from woltdater.utils.updater import get_restaurant_symbol_from_url
# from woltdater.utils.wolt import is_venue_available_status , search_vanue_by_name


def keyboard_maker(venues: list):
    kb = types.InlineKeyboardMarkup()
    for i in venues:
        kb.add(types.InlineKeyboardButton(f"{i['name']}, {i['city']}\n", 
                                            callback_data = i['id']))
    return kb


async def reply_welcome(message: types.message):
    await message.reply(WELCOME_MSG)


async def check_status(message: types.Message, memory_plugin: AbstractMemoryPlugin):
    """
    Gets message and subscribe client if needed
    """
    logging.info(f'Trying to get venue status for {message.text}')

    if "https://" in message.text:
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
    else:
        venue = await search_vanue_by_name(message.text)

        if venue:
            if len(venue) > 1:
                kb = keyboard_maker(venue)
                await message.answer("Which venue?\n", reply_markup=kb)
            else:
                if venue[0]["online"]:
                    await message.answer(VENUE_OPEN_MSG.format(name=venue[0]['name']))
                else:
                    await message.answer(f"I will notify you when {venue[0]['name']} is online!\n")
                    await memory_plugin.subscribe(venue[0]["slug"], message.chat.id)
        else:
            await message.answer(RESTAURANT_NOT_FOUND_MSG) 


async def inline_kb_answer_callback_handler(query: types.CallbackQuery, memory_plugin: AbstractMemoryPlugin, bot: Bot):
    await query.answer()
    venue = await get_vanue_by_id(query.data)
    if not venue:
        await bot.send_message(query.from_user.id,RESTAURANT_NOT_FOUND_MSG)
    else:
        if venue["online"]:
            await bot.send_message(query.from_user.id,VENUE_OPEN_MSG.format(restaurant_symbol=venue['name']))
        else:
            await bot.send_message(query.from_user.id, f"I will notify you when {venue['name']} is online!\n")
            await memory_plugin.subscribe(venue["slug"], query.from_user.id)

def setup_handlers(dispatcher: Dispatcher, memory_plugin: AbstractMemoryPlugin, bot: Bot):
    dispatcher.register_message_handler(reply_welcome, commands=['start', 'help'])
    dispatcher.register_message_handler(lambda message: check_status(message, memory_plugin))
    dispatcher.register_callback_query_handler(lambda message: inline_kb_answer_callback_handler(message, memory_plugin, bot))
