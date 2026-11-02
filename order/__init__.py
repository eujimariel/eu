# Author: Iera Madorable (module: order)
"""Order module: the cart, the total and checkout."""
from contracts import IOrder, IMenuItem, ICustomer, IPayment, CanteenError

OPEN, PAID, PREPARING, READY = "OPEN", "PAID", "PREPARING", "READY"
_FLOW = (OPEN, PAID, PREPARING, READY)


class Order(IOrder):
    """A cart for one customer. Works with ANY IMenuItem, ICustomer and IPayment."""

    MAX_PIECES = 10

    def __init__(self, order_id: int, customer: ICustomer):
        if isinstance(order_id, bool) or not isinstance(order_id, int) or order_id <= 0:
            raise ValueError("order_id must be an int greater than 0")
        if not isinstance(customer, ICustomer):
            raise ValueError("customer must follow ICustomer")
        self._id = order_id
        self._customer = customer
        self._lines = {}  # name -> [price, qty]
        self._status = OPEN

    @property
    def order_id(self) -> int:
        """Order number."""
        return self._id

    @property
    def customer_name(self) -> str:
        """Name of the customer."""
        return self._customer.name

    @property
    def status(self) -> str:
        """OPEN, PAID, PREPARING or READY."""
        return self._status

    @property
    def total(self) -> float:
        """Total price in pesos."""
        return round(sum(p * q for p, q in self._lines.values()), 2)

    def lines(self) -> tuple:
        """Cart lines as a tuple of (name, qty, price)."""
        return tuple((n, q, p) for n, (p, q) in self._lines.items())

    def add_item(self, item: IMenuItem, qty: int) -> None:
        """Add qty pieces of item (takes them from stock)."""
        if not isinstance(item, IMenuItem):
            raise ValueError("item must follow IMenuItem")
        if isinstance(qty, bool) or not isinstance(qty, int) or qty <= 0:
            raise ValueError("qty must be an int greater than 0")
        if self._status != OPEN:
            raise CanteenError("Cannot change an order that is already paid")
        if len(self) + qty > self.MAX_PIECES:
            raise CanteenError(f"An order can have at most {self.MAX_PIECES} pieces")
        item.take(qty)  # may raise CanteenError (out of stock)
        line = self._lines.setdefault(item.name, [item.price, 0])
        line[1] += qty

    def checkout(self, payment: IPayment) -> float:
        """Pay for the order and return the change in pesos."""
        if not isinstance(payment, IPayment):
            raise ValueError("payment must follow IPayment")
        if self._status != OPEN:
            raise CanteenError("Order is already paid")
        if not self._lines:
            raise CanteenError("Cannot check out an empty order")
        change = payment.pay(self.total, self._customer)
        self._status = PAID
        return change

    def advance_status(self) -> str:
        """Move to the next status after PAID."""
        if self._status == OPEN:
            raise CanteenError("Order must be paid first")
        if self._status == READY:
            raise CanteenError("Order is already READY")
        self._status = _FLOW[_FLOW.index(self._status) + 1]
        return self._status

    def __len__(self) -> int:
        return sum(q for _, q in self._lines.values())

    def __str__(self) -> str:
        return f"Order #{self._id} for {self.customer_name}: P{self.total:.2f} [{self._status}]"
