# Author: Marie Eugenie H. Tesocan (module: customer)
"""Customer module: people with an e-wallet balance."""
from contracts import ICustomer, CanteenError


def _check_amount(amount) -> float:
    if isinstance(amount, bool) or not isinstance(amount, (int, float)) or amount <= 0:
        raise ValueError("amount must be a number greater than 0")
    return float(amount)


class Customer(ICustomer):
    """A canteen customer with an e-wallet balance in pesos."""

    _KIND = "Customer"

    def __init__(self, name: str, balance: float = 0.0):
        if not isinstance(name, str) or not name.strip():
            raise ValueError("name must be a non-empty string")
        if isinstance(balance, bool) or not isinstance(balance, (int, float)) or balance < 0:
            raise ValueError("balance must be a number >= 0")
        self._name = name.strip()
        self._balance = float(balance)

    @property
    def name(self) -> str:
        """Customer name."""
        return self._name

    @property
    def balance(self) -> float:
        """E-wallet balance in pesos."""
        return self._balance

    @property
    def kind(self) -> str:
        """'Customer', 'Student' or 'Staff'."""
        return self._KIND

    def top_up(self, amount: float) -> None:
        """Add pesos to the balance."""
        self._balance += _check_amount(amount)

    def deduct(self, amount: float) -> None:
        """Remove pesos from the balance (CanteenError if not enough)."""
        amount = _check_amount(amount)
        if amount > self._balance:
            raise CanteenError(
                f"{self._name} has P{self._balance:.2f} but needs P{amount:.2f}")
        self._balance -= amount

    def __str__(self) -> str:
        return f"{self._KIND} {self._name} (P{self._balance:.2f})"


class StudentCustomer(Customer):
    """A student customer."""
    _KIND = "Student"


class StaffCustomer(Customer):
    """A staff / faculty customer."""
    _KIND = "Staff"
