# Author: Student 1 (module: menu)
"""Menu module: food items with prices and stock."""
from contracts import IMenuItem, IMenu, CanteenError


class MenuItem(IMenuItem):
    """A food item with a price in pesos and limited stock."""

    def __init__(self, name: str, price: float, stock: int):
        if not isinstance(name, str) or not name.strip():
            raise ValueError("name must be a non-empty string")
        if isinstance(price, bool) or not isinstance(price, (int, float)) or price <= 0:
            raise ValueError("price must be a number greater than 0")
        if isinstance(stock, bool) or not isinstance(stock, int) or stock < 0:
            raise ValueError("stock must be an int >= 0")
        self._name = name.strip()
        self._price = float(price)
        self._stock = stock

    @property
    def name(self) -> str:
        """Item name."""
        return self._name

    @property
    def price(self) -> float:
        """Price per piece in pesos."""
        return self._price

    @property
    def stock(self) -> int:
        """Pieces left."""
        return self._stock

    def take(self, qty: int) -> None:
        """Remove qty pieces from stock (CanteenError if not enough)."""
        if isinstance(qty, bool) or not isinstance(qty, int) or qty <= 0:
            raise ValueError("qty must be an int greater than 0")
        if qty > self._stock:
            raise CanteenError(f"Only {self._stock} {self._name} left, wanted {qty}")
        self._stock -= qty

    def __str__(self) -> str:
        return f"{self._name} - P{self._price:.2f} ({self._stock} left)"

    def __eq__(self, other) -> bool:
        return isinstance(other, MenuItem) and self._name.lower() == other._name.lower()

    def __hash__(self) -> int:
        return hash(self._name.lower())


class Menu(IMenu):
    """A menu that holds any objects following IMenuItem."""

    def __init__(self, items):
        self._items = {}
        for item in items:
            if not isinstance(item, IMenuItem):
                raise ValueError("every menu entry must be an IMenuItem")
            key = item.name.lower()
            if key in self._items:
                raise ValueError(f"duplicate item: {item.name}")
            self._items[key] = item

    @property
    def size(self) -> int:
        """How many items are on the menu."""
        return len(self._items)

    @property
    def names(self) -> tuple:
        """Item names as a tuple."""
        return tuple(i.name for i in self._items.values())

    def get_item(self, name: str) -> IMenuItem:
        """Find an item by name (CanteenError if it is not on the menu)."""
        item = self._items.get(str(name).strip().lower())
        if item is None:
            raise CanteenError(f"'{name}' is not on the menu")
        return item

    def items(self) -> tuple:
        """All items as a tuple."""
        return tuple(self._items.values())

    def __len__(self) -> int:
        return len(self._items)

    def __contains__(self, name) -> bool:
        return str(name).strip().lower() in self._items
