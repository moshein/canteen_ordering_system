# tests/test_kitchen.py
import unittest
from kitchen import KitchenQueue, KitchenFullError, OrderNotFoundError

class TestKitchenQueue(unittest.TestCase):
    
    def setUp(self):
        """Set up a small kitchen queue for testing."""
        self.kitchen = KitchenQueue(capacity=2)

    def test_init_validation(self):
        """Test that bad capacity raises ValueError."""
        self.assertEqual(self.kitchen.capacity, 2)
        with self.assertRaises(ValueError):
            KitchenQueue(capacity=0)

    def test_add_order_success(self):
        """Test successfully adding an order."""
        self.kitchen.add_to_queue("O1", "Burger")
        self.assertEqual(len(self.kitchen.pending_orders), 1)
        self.assertIn("O1", self.kitchen.pending_orders)

    def test_update_status_success(self):
        """Test updating order status to 'Preparing' or 'Ready'."""
        self.kitchen.add_to_queue("O1", "Burger")
        self.kitchen.update_status("O1", "Preparing")
        self.assertIn("O1", self.kitchen.pending_orders)
        
        # Complete the order so it leaves pending status
        self.kitchen.update_status("O1", "Completed")
        self.assertEqual(len(self.kitchen.pending_orders), 0)

    def test_update_status_not_found(self):
        """Test that updating a non-existent order raises OrderNotFoundError."""
        with self.assertRaises(OrderNotFoundError):
            self.kitchen.update_status("O99", "Preparing")

    def test_kitchen_full_error(self):
        """Test that KitchenFullError raises when capacity is breached."""
        self.kitchen.add_to_queue("O1", "Burger")
        self.kitchen.add_to_queue("O2", "Fries")
        
        with self.assertRaises(KitchenFullError):
            self.kitchen.add_to_queue("O3", "Soda")

    def test_str_method(self):
        """Test string representation dunder method."""
        self.assertIn("KitchenQueue", str(self.kitchen))

if __name__ == "__main__":
    unittest.main()