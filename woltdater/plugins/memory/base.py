
class AbstractMemoryPlugin:
    """
    An abstract class which keeps the memory of current subscribers
    """
    async def get_all_restaurants(self) -> list:
        """
        Returns list of all subscribed restaurants
        """
        raise NotImplementedError

    async def get_chat_ids_for_restaurant(self, restaurant_symbol: str) -> set:
        """
        Get all subscribed chat ids for specific restaurant
        """
        raise NotImplementedError

    async def subscribe(self, restaurant_symbol: str, chat_id: int) -> None:
        """
        Subscribe chat id to specific restaurant
        """
        raise NotImplementedError

    async def unsubscribe(self, restaurant_symbol: str, chat_id: int) -> None:
        """
        Unsubscribe chat id for specific restaurant
        """
        raise NotImplementedError
