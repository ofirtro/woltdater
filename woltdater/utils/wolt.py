import aiohttp
import json

from consts import WOLT_API_URL, WOLT_OK_STATUS, WOLT_API_SEARCH_URL, WOLT_API_TLV_LOCATION, WOLT_FOUND_STATUS, WOLT_API_ID_URL
from exceptions import RestaurantWasNotFoundException
# from woltdater.consts import WOLT_API_URL, WOLT_OK_STATUS, WOLT_API_SEARCH_URL, WOLT_API_TLV_LOCATION, WOLT_FOUND_STATUS
# from woltdater.exceptions import RestaurantWasNotFoundException


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
    The function returns whether the restaurant's venue is online or offline
    """
    data = await get_restaurant_data(restaurant_symbol)
    return data['results'][0]['online']


async def search_vanue_by_name(searchKey: str) -> list:
    '''
    Search venue by venue name
    '''
    async with aiohttp.ClientSession() as session:
        async with session.get(WOLT_API_SEARCH_URL.format(searchKey=searchKey.replace(" ", '+'), location = WOLT_API_TLV_LOCATION)) as response:
            result = await response.json()
            if result['sections'][0]['name'] != WOLT_FOUND_STATUS:
                return None
            toReturn = list();
            for i in result['sections'][0]['items']:
                toReturn.append(dict({
                    'name' : i['venue']['name'], 
                    'address' : i['venue']['address'], 
                    'city' : i['venue']['city'], 
                    'id' : i['venue']['id'], 
                    'slug' : i['venue']['slug'], 
                    'online' : i['venue']['online']}))
            return toReturn

async def get_vanue_by_id(id: str) -> dict:
    async with aiohttp.ClientSession() as session:
        async with session.get(WOLT_API_ID_URL.format(venueId=id)) as response:
            response_json = await response.json()
            if response_json['status'] != WOLT_OK_STATUS:
                raise RestaurantWasNotFoundException()
            venue = dict({
                "name": response_json["results"][0]["name"][0]["value"],
                "online": response_json["results"][0]["online"],
                "city": response_json["results"][0]["city"],
                "address": response_json["results"][0]["address"],
                "slug": response_json["results"][0]["slug"],
                "id": response_json["results"][0]["id"]["$oid"]
            })
            return venue

