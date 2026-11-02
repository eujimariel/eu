# Author: Student 5 (module: kitchen)
import unittest
from contracts import IOrder, CanteenError
from kitchen import Kitchen


class FakeOrder(IOrder):
    def __init__(self, oid, status="PAID"):
        self._id, self._status = oid, status
    order_id = property(lambda s: s._id)
    customer_name = property(lambda s: "Fake")
    status = property(lambda s: s._status)
    total = property(lambda s: 0.0)
    def add_item(self, item, qty): pass
    def checkout(self, payment): return 0.0
    def advance_status(self):
        self._status = {"PAID": "PREPARING", "PREPARING": "READY"}[self._status]
        return self._status


class TestKitchen(unittest.TestCase):
    def test_bad_capacity(self):
        with self.assertRaises(ValueError):
            Kitchen(0)

    def test_unpaid_order_rejected(self):
        with self.assertRaises(CanteenError):
            Kitchen().enqueue(FakeOrder(1, "OPEN"))

    def test_fifo_order(self):
        k = Kitchen()
        k.enqueue(FakeOrder(1))
        k.enqueue(FakeOrder(2))
        self.assertEqual(k.pending, (1, 2))
        self.assertEqual(k.prepare_next().order_id, 1)

    def test_prepared_order_is_ready(self):
        k = Kitchen()
        k.enqueue(FakeOrder(1))
        self.assertEqual(k.prepare_next().status, "READY")

    def test_full_kitchen(self):
        k = Kitchen(1)
        k.enqueue(FakeOrder(1))
        with self.assertRaises(CanteenError):
            k.enqueue(FakeOrder(2))

    def test_empty_kitchen(self):
        with self.assertRaises(CanteenError):
            Kitchen().prepare_next()

    def test_len_and_pending_is_tuple(self):
        k = Kitchen()
        k.enqueue(FakeOrder(1))
        self.assertEqual(len(k), 1)
        self.assertIsInstance(k.pending, tuple)


if __name__ == "__main__":
    unittest.main()
