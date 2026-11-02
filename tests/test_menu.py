# Author: Student 1 (module: menu)
import unittest
from contracts import IMenuItem, CanteenError
from menu import MenuItem, Menu


class FakeItem(IMenuItem):
    """Fake item that follows the contract (not a teammate's real class)."""
    def __init__(self, name): self._n = name
    name = property(lambda s: s._n)
    price = property(lambda s: 1.0)
    stock = property(lambda s: 1)
    def take(self, qty): pass


class TestMenuItem(unittest.TestCase):
    def test_bad_name_rejected(self):
        with self.assertRaises(ValueError):
            MenuItem("  ", 10, 5)

    def test_negative_price_rejected(self):
        with self.assertRaises(ValueError):
            MenuItem("Adobo", -5, 5)

    def test_take_reduces_stock(self):
        item = MenuItem("Adobo", 50, 3)
        item.take(2)
        self.assertEqual(item.stock, 1)

    def test_take_too_many_raises_canteen_error(self):
        with self.assertRaises(CanteenError):
            MenuItem("Adobo", 50, 1).take(2)

    def test_equality_ignores_case(self):
        self.assertEqual(MenuItem("Adobo", 50, 1), MenuItem("ADOBO", 60, 9))


class TestMenu(unittest.TestCase):
    def test_works_with_fake_items(self):
        menu = Menu([FakeItem("Rice"), FakeItem("Egg")])
        self.assertEqual(len(menu), 2)
        self.assertIn("rice", menu)

    def test_unknown_item_raises(self):
        with self.assertRaises(CanteenError):
            Menu([FakeItem("Rice")]).get_item("Pizza")

    def test_items_returns_tuple(self):
        self.assertIsInstance(Menu([FakeItem("Rice")]).items(), tuple)

    def test_duplicate_rejected(self):
        with self.assertRaises(ValueError):
            Menu([FakeItem("Rice"), FakeItem("rice")])


if __name__ == "__main__":
    unittest.main()
