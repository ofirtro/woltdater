from .base import AbstractMemoryPlugin


class InMemoryPlugin(AbstractMemoryPlugin):
    def __init__(self):
        self._data: dict[str, set] = dict()

    async def get_all_restaurants(self) -> list:
        return list(self._data.keys()).copy()

    async def get_chat_ids_for_restaurant(self, restaurant_symbol: str) -> set:
        return self._data.get(restaurant_symbol, set()).copy()

    async def subscribe(self, restaurant_symbol: str, chat_id: int) -> None:
        self._data.setdefault(restaurant_symbol, set()).add(chat_id)

    async def unsubscribe(self, restaurant_symbol: str, chat_id: int) -> None:
        self._data[restaurant_symbol].discard(chat_id)
        if restaurant_symbol in self._data and not self._data[restaurant_symbol]:
            self._data.pop(restaurant_symbol)
