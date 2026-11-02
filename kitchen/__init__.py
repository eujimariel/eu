# Author: Kissaia Caralde (module: kitchen)
"""Kitchen module: first-in-first-out queue of paid orders."""
from collections import deque

from contracts import IKitchen, IOrder, CanteenError


class Kitchen(IKitchen):
    """A kitchen that works with ANY object following IOrder."""

    def __init__(self, capacity: int = 5):
        if isinstance(capacity, bool) or not isinstance(capacity, int) or capacity <= 0:
            raise ValueError("capacity must be an int greater than 0")
        self._capacity = capacity
        self._queue = deque()

    @property
    def capacity(self) -> int:
        """Maximum orders waiting at once."""
        return self._capacity

    @property
    def pending(self) -> tuple:
        """Order ids waiting, oldest first."""
        return tuple(o.order_id for o in self._queue)

    def enqueue(self, order: IOrder) -> None:
        """Add a PAID order to the queue."""
        if not isinstance(order, IOrder):
            raise ValueError("order must follow IOrder")
        if order.status != "PAID":
            raise CanteenError(f"Order #{order.order_id} is not paid yet")
        if len(self._queue) >= self._capacity:
            raise CanteenError("Kitchen is full, please wait")
        self._queue.append(order)

    def prepare_next(self) -> IOrder:
        """Cook the oldest order and return it (status READY)."""
        if not self._queue:
            raise CanteenError("No orders to prepare")
        order = self._queue.popleft()
        order.advance_status()  # PAID -> PREPARING
        order.advance_status()  # PREPARING -> READY
        return order

    def __len__(self) -> int:
        return len(self._queue)

    def __str__(self) -> str:
        return f"Kitchen({len(self._queue)}/{self._capacity} waiting)"
