
import unittest
from customer import Customer


class TestCustomer(unittest.TestCase):

    def test_valid_customer_name(self):
        customer = Customer("Maria Santos", "Student")
        self.assertEqual(customer.name, "Maria Santos")

    def test_valid_customer_type(self):
        customer = Customer("Maria Santos", "Teacher")
        self.assertEqual(customer.customer_type, "Teacher")

    def test_customer_type_normalization(self):
        customer = Customer("Maria Santos", "student")
        self.assertEqual(customer.customer_type, "Student")

    def test_empty_customer_name(self):
        with self.assertRaises(ValueError):
            Customer("", "Student")

    def test_invalid_customer_type(self):
        with self.assertRaises(ValueError):
            Customer("Maria Santos", "Tourist")


if __name__ == "__main__":
    unittest.main()
