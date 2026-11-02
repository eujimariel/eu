# Author: Student 2 (module: customer)
import unittest
from contracts import CanteenError
from customer import Customer, StudentCustomer, StaffCustomer


class TestCustomer(unittest.TestCase):
    def test_empty_name_rejected(self):
        with self.assertRaises(ValueError):
            Customer("")

    def test_negative_balance_rejected(self):
        with self.assertRaises(ValueError):
            Customer("Ana", -1)

    def test_top_up(self):
        c = Customer("Ana", 10)
        c.top_up(5)
        self.assertEqual(c.balance, 15.0)

    def test_deduct_too_much_raises_canteen_error(self):
        with self.assertRaises(CanteenError):
            Customer("Ana", 10).deduct(20)

    def test_top_up_zero_rejected(self):
        with self.assertRaises(ValueError):
            Customer("Ana").top_up(0)

    def test_subclass_kinds(self):
        self.assertEqual(StudentCustomer("A").kind, "Student")
        self.assertEqual(StaffCustomer("B").kind, "Staff")

    def test_balance_is_read_only(self):
        with self.assertRaises(AttributeError):
            Customer("Ana", 5).balance = 100

    def test_str(self):
        self.assertIn("Ana", str(Customer("Ana", 5)))


if __name__ == "__main__":
    unittest.main()
