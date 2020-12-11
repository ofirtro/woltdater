from urllib.parse import quote

from aiogram.utils.emoji import emojize

IS_VENUE_AVAILABLE_KEY = 'isVenueAvailable'
URL_FORMAT = "https://wolt.com/en/isr/tel-aviv/restaurant/{restaurant_symbol}"
DATA_START_TEXT = quote('{"activeCity"').encode()
DATA_END_TEXT = (quote('}') + '\n').encode()
VENUE_OPEN_MSG = emojize('The restaurant {restaurant_symbol} is open right now! :hamburger: :smile:')
RESTAURANT_SYMBOL_EXAMPLES = ['gdb', 'golda-derech-hashalom']
WELCOME_MSG = emojize("Hi!\n"
                      "I'm sure you are hungry!\n"
                      "Please enter restaurant symbol and i'll let you know when the venue is open :yum: \n"
                      "Find the restaurant symbol from the URL :globe_with_meridians: in wolt.com .\n"
                      "You can find examples in your keyboard :yum: \n"
                      "Then, write it to me and I'll let you know when it is open :+1:"
                      )
WOLTDATER_API_TOKEN_KEY = 'WOLTDATER_API_TOKEN'
RESTAURANT_NOT_FOUND_MSG = emojize('Restaurant was not found! :cry:')
WILL_UPDATE_MSG = "I'll let you know when {restaurant_symbol} is open!"
UPDATE_INTERVAL_IN_SECONDS = 60
