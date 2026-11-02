# Author: Student 4 (module: payment)
"""Payment module: cash and e-wallet."""
from contracts import IPayment, ICustomer, CanteenError


class PaymentMethod(IPayment):
    """Base class for payment types (still abstract: pay() is left to subclasses)."""

    _NAME = "Payment"

    @property
    def method_name(self) -> str:
        """Readable name of the payment type."""
        return self._NAME

    @staticmethod
    def _check(amount, customer) -> float:
        if isinstance(amount, bool) or not isinstance(amount, (int, float)) or amount <= 0:
            raise ValueError("amount must be a number greater than 0")
        if not isinstance(customer, ICustomer):
            raise ValueError("customer must follow ICustomer")
        return float(amount)

    def __str__(self) -> str:
        return self._NAME


class Cash(PaymentMethod):
    """Pay with cash handed over (tendered) at the counter."""

    _NAME = "Cash"

    def __init__(self, tendered: float):
        if isinstance(tendered, bool) or not isinstance(tendered, (int, float)) or tendered <= 0:
            raise ValueError("tendered must be a number greater than 0")
        self._tendered = float(tendered)

    @property
    def tendered(self) -> float:
        """Cash handed over in pesos."""
        return self._tendered

    def pay(self, amount: float, customer: ICustomer) -> float:
        """Return the change; CanteenError if the cash is not enough."""
        amount = self._check(amount, customer)
        if self._tendered < amount:
            raise CanteenError(
                f"Cash P{self._tendered:.2f} is not enough for P{amount:.2f}")
        return round(self._tendered - amount, 2)


class EWallet(PaymentMethod):
    """Pay from the customer's e-wallet balance."""

    _NAME = "E-Wallet"

    def pay(self, amount: float, customer: ICustomer) -> float:
        """Deduct from the customer's balance; change is always 0.0."""
        amount = self._check(amount, customer)
        customer.deduct(amount)  # raises CanteenError if balance is too low
        return 0.0
