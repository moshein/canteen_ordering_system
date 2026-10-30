'''
Contract

What this file is:
The ABCs and custom exceptions every module codes against in our canteen ordering system.

People tasked in writing the contract: (dont forget to transfer it to readme.md)
Montimor - IMenu
Lauzon - ICustomer
Odarve - IPayment
Macaya - IKitchen
Casuboc - IOrder

'''

from abc import ABC, abstractmethod

class IMenu(ABC):
    # @abstractmethod
    # def food_item(self, name: str, price: int):
    #     '''Creates a food item and its price. Price shouldnt be zero or negative'''
    #     pass
    ## i think dili ata ni i-add?? not sure :3

    @abstractmethod
    def add_item(self, item, quantity: int):
        '''Adds food item and its quantity to the menu. The quantity shouldn't be zero or negative'''
        pass

    @abstractmethod
    def remove_item(self, item: str):
        '''Removes a food item and its quantity to the menu'''
        pass

    @property
    @abstractmethod
    def get_menu(self):
        '''Returns all menu entries including the temporarily out of stock items'''
        pass

    @property
    @abstractmethod
    def available_items(self):
        '''Returns the food items available in the menu'''
        pass

    @property
    @abstractmethod
    def unavailable_items(self):
        '''Returns the unavailable food items in the canteen'''
        pass

class ICustomer(ABC):
    ## customer names A, B, Cs (i think during testing rani)

    @abstractmethod
    def sample_func(self):
        pass

class IPayment(ABC):
    ## cash
    ## e-wallet

    @abstractmethod
    def sample_func(self):
        pass

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

class IOrder(ABC):
    ## add order_number (since each orders kay unique)

    @abstractmethod
    def sample_func(self):
        pass
