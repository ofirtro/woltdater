from .base import AbstractMemoryPlugin


class InMemoryPlugin(AbstractMemoryPlugin):
    def __init__(self):
        self._data: dict[str, set] = dict()

    async def get_all_restaurants(self) -> list:
        return list(self._data.keys()).copy()

    async def get_chat_ids_for_restaurant(self, restaurant_url: str) -> set:
        return self._data.get(restaurant_url, set()).copy()

    async def subscribe(self, restaurant_url: str, chat_id: int) -> None:
        self._data.setdefault(restaurant_url, set()).add(chat_id)

    async def unsubscribe(self, restaurant_url: str, chat_id: int) -> None:
        self._data[restaurant_url].discard(chat_id)
        if restaurant_url in self._data and not self._data[restaurant_url]:
            self._data.pop(restaurant_url)
