# Author: Student 3 (module: order)
import unittest
from contracts import ICustomer, IMenuItem, IPayment, CanteenError
from order import Order


class FakeCustomer(ICustomer):
    name = property(lambda s: "Fake")
    balance = property(lambda s: 0.0)
    def top_up(self, amount): pass
    def deduct(self, amount): pass


class FakeItem(IMenuItem):
    def __init__(self, name="Rice", price=10.0, stock=100):
        self._n, self._p, self._s = name, price, stock
    name = property(lambda s: s._n)
    price = property(lambda s: s._p)
    stock = property(lambda s: s._s)
    def take(self, qty):
        if qty > self._s:
            raise CanteenError("no stock")
        self._s -= qty


class FakePayment(IPayment):
    def __init__(self): self.paid = None
    def pay(self, amount, customer):
        self.paid = amount
        return 0.0


class TestOrder(unittest.TestCase):
    def setUp(self):
        self.order = Order(1, FakeCustomer())

    def test_bad_id_rejected(self):
        with self.assertRaises(ValueError):
            Order(0, FakeCustomer())

    def test_total_is_computed(self):
        self.order.add_item(FakeItem(price=12.5), 2)
        self.assertEqual(self.order.total, 25.0)

    def test_same_item_merges_lines(self):
        item = FakeItem()
        self.order.add_item(item, 1)
        self.order.add_item(item, 2)
        self.assertEqual(self.order.lines(), (("Rice", 3, 10.0),))

    def test_limit_of_ten_pieces(self):
        with self.assertRaises(CanteenError):
            self.order.add_item(FakeItem(), 11)

    def test_out_of_stock_error_passes_through(self):
        with self.assertRaises(CanteenError):
            self.order.add_item(FakeItem(stock=1), 2)

    def test_empty_checkout_rejected(self):
        with self.assertRaises(CanteenError):
            self.order.checkout(FakePayment())

    def test_checkout_uses_any_payment_and_marks_paid(self):
        pay = FakePayment()
        self.order.add_item(FakeItem(price=10), 3)
        self.order.checkout(pay)
        self.assertEqual(pay.paid, 30.0)
        self.assertEqual(self.order.status, "PAID")

    def test_cannot_add_after_paid(self):
        self.order.add_item(FakeItem(), 1)
        self.order.checkout(FakePayment())
        with self.assertRaises(CanteenError):
            self.order.add_item(FakeItem(), 1)

    def test_status_flow(self):
        self.order.add_item(FakeItem(), 1)
        with self.assertRaises(CanteenError):
            self.order.advance_status()  # not paid yet
        self.order.checkout(FakePayment())
        self.assertEqual(self.order.advance_status(), "PREPARING")
        self.assertEqual(self.order.advance_status(), "READY")


if __name__ == "__main__":
    unittest.main()
