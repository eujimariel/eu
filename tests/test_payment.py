# Author: Student 4 (module: payment)
import unittest
from contracts import ICustomer, CanteenError
from payment import Cash, EWallet


class FakeCustomer(ICustomer):
    def __init__(self, balance=100.0): self._b = balance
    name = property(lambda s: "Fake")
    balance = property(lambda s: s._b)
    def top_up(self, amount): self._b += amount
    def deduct(self, amount):
        if amount > self._b:
            raise CanteenError("not enough")
        self._b -= amount


class TestPayment(unittest.TestCase):
    def test_cash_returns_change(self):
        self.assertEqual(Cash(100).pay(75, FakeCustomer()), 25.0)

    def test_cash_not_enough(self):
        with self.assertRaises(CanteenError):
            Cash(50).pay(75, FakeCustomer())

    def test_cash_bad_tendered(self):
        with self.assertRaises(ValueError):
            Cash(-1)

    def test_ewallet_deducts_balance(self):
        customer = FakeCustomer(100)
        self.assertEqual(EWallet().pay(40, customer), 0.0)
        self.assertEqual(customer.balance, 60)

    def test_ewallet_insufficient_balance(self):
        with self.assertRaises(CanteenError):
            EWallet().pay(40, FakeCustomer(10))

    def test_bad_amount_rejected(self):
        with self.assertRaises(ValueError):
            EWallet().pay(0, FakeCustomer())

    def test_method_names_and_str(self):
        self.assertEqual(Cash(10).method_name, "Cash")
        self.assertEqual(str(EWallet()), "E-Wallet")


if __name__ == "__main__":
    unittest.main()
