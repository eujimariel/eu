# Author: Whole group (contracts)
"""The contract: every module imports ONLY from here (plus the standard library)."""
from abc import ABC, abstractmethod


class CanteenError(Exception):
    """Raised when a canteen rule is broken (out of stock, not enough money, ...)."""


class IMenuItem(ABC):
    """One food item on the menu."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Non-empty item name."""

    @property
    @abstractmethod
    def price(self) -> float:
        """Price per piece in pesos (> 0)."""

    @property
    @abstractmethod
    def stock(self) -> int:
        """Pieces left (>= 0)."""

    @abstractmethod
    def take(self, qty: int) -> None:
        """Remove qty pieces from stock.
        Raises ValueError if qty is not an int > 0.
        Raises CanteenError if qty is more than the stock."""


class IMenu(ABC):
    """A collection of menu items."""

    @abstractmethod
    def get_item(self, name: str) -> IMenuItem:
        """Find an item by name (case-insensitive).
        Raises CanteenError if the item is not on the menu."""

    @abstractmethod
    def items(self) -> tuple:
        """All items as a tuple of IMenuItem (never the internal list)."""


class ICustomer(ABC):
    """Someone who buys food. Holds an e-wallet balance."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Non-empty customer name."""

    @property
    @abstractmethod
    def balance(self) -> float:
        """E-wallet balance in pesos (>= 0)."""

    @abstractmethod
    def top_up(self, amount: float) -> None:
        """Add pesos to the balance. Raises ValueError if amount <= 0 or not a number."""

    @abstractmethod
    def deduct(self, amount: float) -> None:
        """Remove pesos from the balance.
        Raises ValueError if amount <= 0 or not a number.
        Raises CanteenError if amount is more than the balance."""


class IPayment(ABC):
    """A way to pay (cash, e-wallet, ...)."""

    @abstractmethod
    def pay(self, amount: float, customer: ICustomer) -> float:
        """Pay amount (pesos) for customer. Returns the CHANGE in pesos (0.0 if none).
        Raises ValueError if amount <= 0.
        Raises CanteenError if the payment is not enough."""


class IOrder(ABC):
    """A customer's cart that becomes a kitchen ticket after payment."""

    @property
    @abstractmethod
    def order_id(self) -> int:
        """Positive integer id."""

    @property
    @abstractmethod
    def customer_name(self) -> str:
        """Name of the customer who owns the order."""

    @property
    @abstractmethod
    def status(self) -> str:
        """One of 'OPEN', 'PAID', 'PREPARING', 'READY'."""

    @property
    @abstractmethod
    def total(self) -> float:
        """Total price in pesos, rounded to 2 decimals."""

    @abstractmethod
    def add_item(self, item: IMenuItem, qty: int) -> None:
        """Add qty pieces (takes them from stock). Only while status is 'OPEN'.
        Raises ValueError for bad input.
        Raises CanteenError if out of stock, order is not OPEN, or the order would exceed 10 pieces."""

    @abstractmethod
    def checkout(self, payment: IPayment) -> float:
        """Pay for the order; status becomes 'PAID'. Returns change in pesos.
        Raises CanteenError if the cart is empty, already paid, or payment fails."""

    @abstractmethod
    def advance_status(self) -> str:
        """Move PAID -> PREPARING -> READY and return the new status.
        Raises CanteenError if the order is not paid yet or already READY."""


class IKitchen(ABC):
    """Queue of paid orders waiting to be cooked (first in, first out)."""

    @property
    @abstractmethod
    def pending(self) -> tuple:
        """Order ids waiting, oldest first, as a tuple of int."""

    @abstractmethod
    def enqueue(self, order: IOrder) -> None:
        """Add a PAID order to the queue.
        Raises CanteenError if the order is not PAID or the queue is full."""

    @abstractmethod
    def prepare_next(self) -> IOrder:
        """Cook the oldest order (status ends as 'READY') and return it.
        Raises CanteenError if the queue is empty."""
