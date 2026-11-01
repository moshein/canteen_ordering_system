
import unittest

from customer import Customer
from contracts import IOrder, CanteenError


class FakeOrder(IOrder):
    """Fake Order object for testing Customer."""

    def __init__(self):
        self._active_orders = ()

    def create_order(self, order_number: str, item: str) -> None:
        pass

    def cancel_order(self, order_number: str) -> None:
        pass

    @property
    def active_orders(self) -> tuple:
        return self._active_orders

    @property
    def total(self) -> float:
        return 0.0


class TestCustomer(unittest.TestCase):

    def setUp(self):
        self.order = FakeOrder()
        self.customer = Customer(
            "Maria Santos",
            "Student",
            self.order
        )

    def test_valid_customer_name(self):
        self.assertEqual(self.customer.name, "Maria Santos")

    def test_valid_customer_type(self):
        self.assertEqual(self.customer.customer_type, "Student")

    def test_customer_type_normalization(self):
        customer = Customer("Maria Santos", "student", self.order)
        self.assertEqual(customer.customer_type, "Student")

    def test_empty_customer_name(self):
        with self.assertRaises(ValueError):
            Customer("", "Student", self.order)

    def test_invalid_customer_type(self):
        with self.assertRaises(ValueError):
            Customer("Maria Santos", "Tourist", self.order)

    def test_add_order(self):
        self.customer.add_order("ORD-001")
        self.assertIn("ORD-001", self.customer.order_ids)

    def test_duplicate_order(self):
        self.customer.add_order("ORD-001")

        with self.assertRaises(CanteenError):
            self.customer.add_order("ORD-001")

    def test_remove_customer_with_pending_order(self):
        self.customer.add_order("ORD-001")
        self.order._active_orders = ("ORD-001",)

        with self.assertRaises(CanteenError):
            self.customer.remove_customer()

    def test_remove_customer_without_pending_orders(self):
        self.customer.add_order("ORD-001")
        self.customer.remove_customer()

        self.assertEqual(self.customer.order_ids, ())


if __name__ == "__main__":
    unittest.main()
