from urllib.parse import quote

from aiogram.utils.emoji import emojize

IS_VENUE_AVAILABLE_KEY = 'isVenueAvailable'
DATA_START_TEXT = quote('{"activeCity"').encode()
DATA_END_TEXT = (quote('}') + '\n').encode()
VENUE_OPEN_MSG = emojize('The restaurant {restaurant_symbol} is open right now! :hamburger: :smile:')
WELCOME_MSG = emojize("Hi!\n"
                      "I'm sure you are hungry!\n"
                      "Please enter restaurant url from wolt.com and i'll let you know when the venue is open :yum: \n")
WOLTDATER_API_TOKEN_KEY = 'WOLTDATER_API_TOKEN'
RESTAURANT_NOT_FOUND_MSG = emojize('Restaurant was not found! :cry:')
WILL_UPDATE_MSG = "I'll let you know when {restaurant_symbol} is open!"
UPDATE_INTERVAL_IN_SECONDS = 60
WOLT_BASE_URL = 'wolt.com'
BAD_RESTAURANT_URL_MSG = emojize('The url you have given is not a valid URL :confused:')
