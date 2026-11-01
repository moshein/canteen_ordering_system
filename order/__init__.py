## Author: Ruena Casuboc (module: order)

## cart
## totals

"""
Order Module

Manages the customer's cart, order creation,
cancellation, and total price calculation.
"""

from contracts import IOrder, IMenu, CanteenError


class DuplicateOrderError(CanteenError):
    """Raised when an order number already exists."""
    pass


class OrderNotFoundError(CanteenError):
    """Raised when an order cannot be found."""
    pass


class InsufficientStockError(CanteenError):
    """Raised when the requested quantity exceeds available stock."""
    pass


class Order(IOrder):
    """Manages shopping carts and customer orders."""

    def __init__(self, menu: IMenu) -> None:
        """Initialize an order manager using an IMenu object."""

        if not isinstance(menu, IMenu):
            raise ValueError("Menu must implement IMenu.")

        self._menu = menu
        self._cart = {}
        self._orders = {}

    def add_to_cart(self, item_name: str, quantity: int) -> None:
        """Add a food item and quantity to the cart."""

        if not isinstance(item_name, str) or not item_name.strip():
            raise ValueError("Item name must be a non-empty string.")

        if type(quantity) is not int or quantity <= 0:
            raise ValueError("Quantity must be a positive integer.")

        available_item = None

        for item in self._menu.available_items:
            if item[1] == item_name:
                available_item = item
                break

        if available_item is None:
            raise ValueError(f"{item_name} is not available.")

        price = available_item[2]
        stock = available_item[3]

        current_quantity = self._cart.get(
            item_name, {}
        ).get("quantity", 0)

        if current_quantity + quantity > stock:
            raise InsufficientStockError(
                f"Insufficient stock for {item_name}."
            )

        if item_name in self._cart:
            self._cart[item_name]["quantity"] += quantity
        else:
            self._cart[item_name] = {
                "price": price,
                "quantity": quantity
            }

    def remove_from_cart(self, item_name: str) -> None:
        """Remove a food item from the cart."""

        if item_name not in self._cart:
            raise ValueError(f"{item_name} is not in the cart.")

        del self._cart[item_name]

    def calculate_total(self) -> float:
        """Calculate the total price of all cart items."""

        return round(
            sum(
                item["price"] * item["quantity"]
                for item in self._cart.values()
            ),
            2
        )

    def create_order(self, order_number: str, item: str) -> None:
        """Create an order using the current cart contents."""

        if not isinstance(order_number, str) or not order_number.strip():
            raise ValueError("Order number must be a non-empty string.")

        if not isinstance(item, str) or not item.strip():
            raise ValueError("Item must be a non-empty string.")

        if order_number in self._orders:
            raise DuplicateOrderError(
                f"Order '{order_number}' already exists."
            )

        if not self._cart:
            raise ValueError("Cannot create an order with an empty cart.")

        if item not in self._cart:
            raise ValueError("The specified item must be in the cart.")

        cart_snapshot = tuple(
            (name, details["price"], details["quantity"])
            for name, details in self._cart.items()
        )

        self._orders[order_number] = {
            "item": item,
            "cart": cart_snapshot,
            "total": self.calculate_total(),
            "status": "Pending"
        }

    def cancel_order(self, order_number: str) -> None:
        """Cancel an existing active order."""

        if order_number not in self._orders:
            raise OrderNotFoundError(
                f"Order '{order_number}' does not exist."
            )

        if self._orders[order_number]["status"] != "Pending":
            raise CanteenError(
                "Only pending orders can be cancelled."
            )

        self._orders[order_number]["status"] = "Cancelled"

    @property
    def cart(self) -> tuple:
        """Return an immutable snapshot of the shopping cart."""

        return tuple(
            (name, details["price"], details["quantity"])
            for name, details in self._cart.items()
        )

    @property
    def total(self) -> float:
        """Return the current cart total."""

        return self.calculate_total()

    @property
    def active_orders(self) -> tuple:
        """Return the order numbers of all pending orders."""

        return tuple(
            order_number
            for order_number, details in self._orders.items()
            if details["status"] == "Pending"
        )

    def __len__(self) -> int:
        """Return the number of distinct items in the cart."""

        return len(self._cart)

    def __contains__(self, item_name: str) -> bool:
        """Check whether a food item exists in the cart."""

        return item_name in self._cart

    def __str__(self) -> str:
        """Return a readable summary of the cart."""

        return (
            f"Order(Cart Items: {len(self)}, "
            f"Total: Php {self.total:.2f})"
        )
