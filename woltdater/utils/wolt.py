import aiohttp

from woltdater.consts import WOLT_API_URL, WOLT_OK_STATUS
from woltdater.exceptions import RestaurantWasNotFoundException


async def get_restaurant_data(restaurant_symbol: str) -> dict:
    """
    Get the restaurant data dict from it wolt URL
    """
    async with aiohttp.ClientSession() as session:
        async with session.get(WOLT_API_URL.format(restaurant_symbol=restaurant_symbol)) as response:
            response_json = await response.json()
            if response_json['status'] != WOLT_OK_STATUS:
                raise RestaurantWasNotFoundException()
            return response_json


async def is_venue_available_status(restaurant_symbol: str) -> bool:
    """
    The function returns whether the restaurant's venue is open or closed
    """
    data = await get_restaurant_data(restaurant_symbol)
    return data['results'][0]['online']
