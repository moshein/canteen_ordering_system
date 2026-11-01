# Author: Nelle Lauzon (module: customer)

from contracts import ICustomer, IOrder, CanteenError


class Customer(ICustomer):
    """
    Represents a customer in the canteen ordering system.

    Stores customer information and manages associated order IDs.
    """

    VALID_CUSTOMER_TYPES = (
        "Student",
        "Teacher",
        "Staff",
        "Visitor"
    )

    def __init__(
        self,
        name: str,
        customer_type: str,
        order: IOrder
    ):
        """
        Initialize a customer with their name, type, and order reference.

        Raises:
            ValueError: If the customer information or order is invalid.
        """

        if not isinstance(name, str) or not name.strip():
            raise ValueError("Customer name cannot be empty.")

        if not isinstance(customer_type, str):
            raise ValueError("Customer type must be a string.")

        customer_type = customer_type.strip().title()

        if customer_type not in self.VALID_CUSTOMER_TYPES:
            raise ValueError("Invalid customer type.")

        if not isinstance(order, IOrder):
            raise ValueError("Order must implement IOrder.")

        self._name = name.strip()
        self._customer_type = customer_type
        self._order = order
        self._order_ids = []

    @property
    def name(self) -> str:
        """Return the customer's name."""
        return self._name

    @property
    def customer_type(self) -> str:
        """Return the customer's type."""
        return self._customer_type

    @property
    def order_ids(self) -> tuple:
        """Return an immutable collection of the customer's order IDs."""
        return tuple(self._order_ids)

    def add_order(self, order_id: str) -> None:
        """
        Associate an order ID with this customer.

        Raises:
            ValueError: If the order ID is invalid.
            CanteenError: If the order ID is already associated.
        """

        if not isinstance(order_id, str) or not order_id.strip():
            raise ValueError("Order ID cannot be empty.")

        order_id = order_id.strip()

        if order_id in self._order_ids:
            raise CanteenError(
                f"Order '{order_id}' is already associated with this customer."
            )

        self._order_ids.append(order_id)

    def remove_customer(self) -> None:
        """
        Check whether this customer can be removed.

        Raises:
            CanteenError: If the customer still has pending orders.
        """

        pending_orders = self._order.active_orders

        for order_id in self._order_ids:
            if order_id in pending_orders:
                raise CanteenError(
                    "Cannot remove a customer with pending orders."
                )

        self._order_ids.clear()

    def __str__(self) -> str:
        """Return a readable description of the customer."""
        return (
            f"Customer: {self._name} | "
            f"Type: {self._customer_type}"
        )
