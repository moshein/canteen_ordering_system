## Author: Jay Mark Macaya (module: kitchen)

## order queue
## status

# Author: Jay Mark J. Macaya (module: kitchen)
from contracts import IKitchen, CanteenError

class KitchenFullError(CanteenError):
    """Raised when the kitchen queue reaches its limit."""
    pass

class OrderNotFoundError(CanteenError):
    """Raised when an order ID cannot be found in the kitchen."""
    pass

class KitchenQueue(IKitchen):
    """Manages the canteen order queue, preparation status, and cooking workflow."""

    def __init__(self, capacity: int = 3) -> None:
        """Initialize kitchen with a maximum order capacity."""
        if not isinstance(capacity, int) or capacity <= 0:
            raise ValueError("Capacity must be a positive integer.")
        
        self._capacity = capacity
        # Stores order_id: {"item": str, "status": str}
        self._orders = {} 

    @property
    def capacity(self) -> int:
        """Return maximum queue capacity (Read-only)."""
        return self._capacity

    @property
    def pending_orders(self) -> tuple:
        """Return an immutable tuple of pending or preparing orders (Read-only)."""
        active_states = {"Pending", "Preparing"}
        return tuple(
            order_id for order_id, info in self._orders.items() 
            if info["status"] in active_states
        )

    def add_to_queue(self, order_number: str, item: str) -> None:
        """Add a new order to the kitchen queue.
        
        Raises:
            ValueError: If inputs are invalid.
            KitchenFullError: If the queue is full.
        """
        if not isinstance(order_number, str) or not order_number.strip():
            raise ValueError("Order Number must be a non-empty string.")
        if not isinstance(item, str) or not item.strip():
            raise ValueError("Item must be a non-empty string.")
            
        if len(self._orders) >= self._capacity:
            raise KitchenFullError("Kitchen queue is full!")

        self._orders[order_number] = {"item": item, "status": "Pending"}

    def update_status(self, order_number: str, status: str) -> None:
        """Update the preparation status of an order (e.g., 'Preparing', 'Ready').
        
        Raises:
            ValueError: If status is invalid.
            OrderNotFoundError: If order_number does not exist.
        """
        valid_statuses = {"Pending", "Preparing", "Ready", "Completed"}
        if not isinstance(status, str) or status not in valid_statuses:
            raise ValueError(f"Invalid status. Must be one of {valid_statuses}")
            
        if order_number not in self._orders:
            raise OrderNotFoundError(f"Order '{order_number}' not found in kitchen.")
            
        self._orders[order_number]["status"] = status

    def __str__(self) -> str:
        """Return a simple string representation."""
        return f"KitchenQueue(Capacity: {self._capacity}, Active Orders: {len(self.pending_orders)})"