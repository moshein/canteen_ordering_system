'''
Contracts

What it is:
The ABCs and custom exceptions every module codes against

Who writes it:
Whole group, together before anyone starts coding
'''

# from abc import ABC, abstractmethod

from abc import ABC, abstractmethod

class CanteenError(Exception):
    """Base exception for canteen errors."""
    pass

class IKitchen(ABC):
    @abstractmethod
    def add_to_queue(self, order_number: str, item: str) -> None:
        """Add an order to the kitchen queue."""
        pass
        
    @property
    @abstractmethod
    def pending_orders(self) -> tuple:
        """Return tuple of pending orders."""
        pass