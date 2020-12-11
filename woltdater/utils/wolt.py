import asyncio
import json
from http import HTTPStatus
from urllib.parse import unquote, urlparse

import aiohttp

from woltdater.consts import DATA_START_TEXT, DATA_END_TEXT, IS_VENUE_AVAILABLE_KEY, WOLT_BASE_URL
from woltdater.exceptions import RestaurantWasNotFoundException, BadRestaurantUrlException


async def extract_data_from_response(response: asyncio.StreamReader) -> dict:
    """
    Gets the restaurant json memory from the API response
    """
    response_data = await response.read()
    restaurant_data = response_data[
                      response_data.find(DATA_START_TEXT):
                      response_data.find(DATA_END_TEXT) + len(DATA_END_TEXT) - 1]
    return json.loads(unquote(restaurant_data.decode()))


async def get_restaurant_data_from_url(restaurant_url: str) -> dict:
    """
    Get the restaurant data dict from it wolt URL
    """
    if urlparse(restaurant_url).netloc.lower() != WOLT_BASE_URL:
        raise BadRestaurantUrlException()

    async with aiohttp.ClientSession() as session:
        async with session.get(restaurant_url) as response:
            if response.status != HTTPStatus.OK:
                raise RestaurantWasNotFoundException()
            return await extract_data_from_response(response.content)


async def is_venue_available_status(restaurant_url: str) -> bool:
    """
    The function returns whether the restaurant's venue is open or closed
    """
    data = await get_restaurant_data_from_url(restaurant_url)
    return data['venues']['venue'][IS_VENUE_AVAILABLE_KEY]
