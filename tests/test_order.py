# Order module test (Casuboc)

import unittest

from contracts import IMenu, CanteenError
from order import (
    Order,
    DuplicateOrderError,
    OrderNotFoundError,
    InsufficientStockError,
    OrderLockedError
)


class FakeMenu(IMenu):
    """Fake menu used for testing the Order module."""

    def __init__(self):
        self._menu = [
            ["Meal", "Chicken Rice", 75.00, 10],
            ["Meal", "Burger", 50.00, 5],
            ["Ready-To-Eat", "Iced Tea", 25.00, 8]
        ]

    def add_item(self, item, quantity: int):
        pass

    def remove_item(self, item_name: str):
        pass

    @property
    def menu(self):
        return self._menu.copy()

    @property
    def available_items(self):
        return [item for item in self._menu if item[3] > 0]

    @property
    def unavailable_items(self):
        return [item for item in self._menu if item[3] <= 0]


class TestOrder(unittest.TestCase):

    def setUp(self):
        self.menu = FakeMenu()
        self.order = Order(self.menu)

    # 1. Test adding items
    def test_add_to_cart(self):
        self.order.add_to_cart("Chicken Rice", 2)

        self.assertEqual(len(self.order), 1)
        self.assertIn("Chicken Rice", self.order)

    # 2. Test invalid quantity
    def test_invalid_quantity(self):
        with self.assertRaises(ValueError):
            self.order.add_to_cart("Chicken Rice", 0)

    # 3. Test insufficient stock
    def test_insufficient_stock(self):
        with self.assertRaises(InsufficientStockError):
            self.order.add_to_cart("Chicken Rice", 11)

    # 4. Test calculating total
    def test_calculate_total(self):
        self.order.add_to_cart("Chicken Rice", 2)
        self.order.add_to_cart("Burger", 1)

        self.assertEqual(self.order.calculate_total(), 200.00)

    # 5. Test removing an item
    def test_remove_from_cart(self):
        self.order.add_to_cart("Burger", 1)
        self.order.remove_from_cart("Burger")

        self.assertNotIn("Burger", self.order)

    # 6. Test modifying cart
    def test_modify_cart(self):
        self.order.add_to_cart("Chicken Rice", 2)
        self.order.modify_cart("Chicken Rice", 3)

        self.assertEqual(self.order.calculate_total(), 225.00)

    # 7. Test submitting an order
    def test_create_order(self):
        self.order.add_to_cart("Chicken Rice", 2)
        self.order.create_order("ORD001", "Chicken Rice")

        self.assertEqual(self.order.active_orders, ("ORD001",))

    # 8. Test duplicate order number
    def test_duplicate_order(self):
        self.order.add_to_cart("Chicken Rice", 1)
        self.order.create_order("ORD001", "Chicken Rice")

        with self.assertRaises(DuplicateOrderError):
            self.order.create_order("ORD001", "Chicken Rice")

    # 9. Test cancelling an order
    def test_cancel_order(self):
        self.order.add_to_cart("Burger", 1)
        self.order.create_order("ORD001", "Burger")
        self.order.cancel_order("ORD001")

        self.assertEqual(self.order.active_orders, ())

    # 10. Test cancelling a nonexistent order
    def test_cancel_nonexistent_order(self):
        with self.assertRaises(OrderNotFoundError):
            self.order.cancel_order("ORD999")

    # 11. Test submitted order cannot be modified
    def test_locked_order(self):
        self.order.add_to_cart("Burger", 1)
        self.order.create_order("ORD001", "Burger")

        with self.assertRaises(OrderLockedError):
            self.order.add_to_cart("Iced Tea", 1)

    # 12. Test cart returns a tuple
    def test_cart_is_immutable(self):
        self.order.add_to_cart("Burger", 1)

        self.assertIsInstance(self.order.cart, tuple)

    # 13. Test total property
    def test_total_property(self):
        self.order.add_to_cart("Chicken Rice", 2)

        self.assertEqual(self.order.total, 150.00)

    # 14. Test string representation
    def test_string_representation(self):
        self.order.add_to_cart("Burger", 2)

        self.assertEqual(
            str(self.order),
            "Order(Cart Items: 1, Total: Php 100.00)"
        )


if __name__ == "__main__":
    unittest.main()
