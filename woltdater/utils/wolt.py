import asyncio
import json
from http import HTTPStatus
from urllib.parse import unquote

import aiohttp

from woltdater.consts import DATA_START_TEXT, DATA_END_TEXT, URL_FORMAT, IS_VENUE_AVAILABLE_KEY
from woltdater.exceptions import RestaurantWasNotFoundException


async def extract_data_from_response(response: asyncio.StreamReader) -> dict:
    """
    Gets the restaurant json memory from the API response
    """
    response_data = await response.read()
    restaurant_data = response_data[
                      response_data.find(DATA_START_TEXT):
                      response_data.find(DATA_END_TEXT) + len(DATA_END_TEXT) - 1]
    return json.loads(unquote(restaurant_data.decode()))


async def is_venue_available_status(restaurant_symbol: str) -> bool:
    """
    The function returns whether the restaurant's venue is open or closed
    """
    async with aiohttp.ClientSession() as session:
        response = await session.get(URL_FORMAT.format(restaurant_symbol=restaurant_symbol))
        if response.status != HTTPStatus.OK:
            raise RestaurantWasNotFoundException()
        data = await extract_data_from_response(response.content)
        return data['venues']['venue'][IS_VENUE_AVAILABLE_KEY]
