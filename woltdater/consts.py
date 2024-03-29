from aiogram.utils.emoji import emojize

VENUE_OPEN_MSG = emojize('The restaurant {restaurant_symbol} is open right now! :hamburger: :smile:')
WELCOME_MSG = emojize("Hi!\n"
                      "I'm sure you are hungry!\n"
                      "Please enter restaurant url from wolt.com and i'll let you know when the venue is open :yum: \n")
WOLTDATER_API_TOKEN_KEY = 'WOLTDATER_API_TOKEN'
RESTAURANT_NOT_FOUND_MSG = emojize('Restaurant was not found! :cry:')
WILL_UPDATE_MSG = "I'll let you know when {restaurant_symbol} is open!"
UPDATE_INTERVAL_IN_SECONDS = 60
WOLT_API_URL = 'https://restaurant-api.wolt.com/v3/venues/slug/{restaurant_symbol}'
WOLT_OK_STATUS = 'OK'