# Order module test (Casuboc)
import unittest

from contracts import IMenu, CanteenError
from order import (
    Order,
    DuplicateOrderError,
    OrderNotFoundError,
    InsufficientStockError
)


# Fake Menu implementing the IMenu contract
class FakeMenu(IMenu):

    def __init__(self):
        self._menu = [
            ["Meal", "Chicken Rice", 75.00, 10],
            ["Meal", "Burger", 50.00, 5],
            ["Ready-To-Eat", "Iced Tea", 25.00, 8]
        ]

    def add_item(self, item, quantity: int):
        self._menu.append(
            [item.foodType, item.name, item.price, quantity]
        )

    def remove_item(self, item_name: str):
        self._menu = [
            item for item in self._menu
            if item[1] != item_name
        ]

    @property
    def menu(self):
        return self._menu.copy()

    @property
    def available_items(self):
        return [
            item for item in self._menu
            if item[3] > 0
        ]

    @property
    def unavailable_items(self):
        return [
            item for item in self._menu
            if item[3] <= 0
        ]


class TestOrder(unittest.TestCase):

    def setUp(self):
        """Create a fresh Order object before every test."""
        self.menu = FakeMenu()
        self.order = Order(self.menu)

    def test_add_to_cart(self):
        """Test adding a valid food item."""
        self.order.add_to_cart("Chicken Rice", 2)

        self.assertEqual(len(self.order), 1)
        self.assertIn("Chicken Rice", self.order)

    def test_invalid_quantity(self):
        """Test rejection of zero quantity."""
        with self.assertRaises(ValueError):
            self.order.add_to_cart("Chicken Rice", 0)

    def test_insufficient_stock(self):
        """Test rejection of quantities exceeding stock."""
        with self.assertRaises(InsufficientStockError):
            self.order.add_to_cart("Burger", 10)

    def test_calculate_total(self):
        """Test calculation of the cart total."""
        self.order.add_to_cart("Chicken Rice", 2)
        self.order.add_to_cart("Burger", 1)

        self.assertEqual(self.order.calculate_total(), 200.00)

    def test_remove_from_cart(self):
        """Test removing an item from the cart."""
        self.order.add_to_cart("Chicken Rice", 2)
        self.order.remove_from_cart("Chicken Rice")

        self.assertNotIn("Chicken Rice", self.order)
        self.assertEqual(len(self.order), 0)

    def test_create_order(self):
        """Test creating an order with a valid cart."""
        self.order.add_to_cart("Chicken Rice", 2)

        self.order.create_order("ORD-001", "Chicken Rice")

        self.assertIn("ORD-001", self.order.active_orders)

    def test_duplicate_order(self):
        """Test rejection of duplicate order numbers."""
        self.order.add_to_cart("Chicken Rice", 1)
        self.order.create_order("ORD-001", "Chicken Rice")

        with self.assertRaises(DuplicateOrderError):
            self.order.create_order("ORD-001", "Chicken Rice")

    def test_cancel_order(self):
        """Test cancelling an existing pending order."""
        self.order.add_to_cart("Chicken Rice", 1)
        self.order.create_order("ORD-001", "Chicken Rice")

        self.order.cancel_order("ORD-001")

        self.assertNotIn("ORD-001", self.order.active_orders)

    def test_cancel_nonexistent_order(self):
        """Test cancelling an order that does not exist."""
        with self.assertRaises(OrderNotFoundError):
            self.order.cancel_order("ORD-999")

    def test_cart_returns_tuple(self):
        """Test that cart returns an immutable collection."""
        self.order.add_to_cart("Chicken Rice", 1)

        self.assertIsInstance(self.order.cart, tuple)

    def test_total_is_read_only(self):
        """Test that total cannot be directly reassigned."""
        with self.assertRaises(AttributeError):
            self.order.total = 500

    def test_string_representation(self):
        """Test the Order class string representation."""
        self.order.add_to_cart("Burger", 2)

        self.assertIn("100.00", str(self.order))


if __name__ == "__main__":
    unittest.main()
