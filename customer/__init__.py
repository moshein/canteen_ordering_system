# Author: Nelle Lauzon (module: customer)

from contracts import ICustomer


class Customer(ICustomer):
    """
    Represents a customer in the canteen ordering system.

    Stores the customer's name and customer type.
    """

    VALID_CUSTOMER_TYPES = (
        "Student",
        "Teacher",
        "Staff",
        "Visitor"
    )

    def __init__(self, name: str, customer_type: str):
        """
        Initialize a customer with their name and customer type.

        Raises:
            ValueError: If the name or customer type is invalid.
        """

        if not isinstance(name, str) or not name.strip():
            raise ValueError("Customer name cannot be empty.")

        if not isinstance(customer_type, str):
            raise ValueError("Customer type must be a string.")

        customer_type = customer_type.strip().title()

        if customer_type not in self.VALID_CUSTOMER_TYPES:
            raise ValueError("Invalid customer type.")
            
        self._name = name.strip()
        self._customer_type = customer_type

    @property
    def name(self) -> str:
        """Return the customer's name."""
        return self._name

    @property
    def customer_type(self) -> str:
        """Return the customer's type."""
        return self._customer_type

    def sample_func(self):
        """
        Temporary implementation of the current ICustomer
        contract placeholder.
        """
        return f"{self._name} ({self._customer_type})"

    def __str__(self) -> str:
        """Return a readable description of the customer."""
        return f"Customer: {self._name} | Type: {self._customer_type}"
