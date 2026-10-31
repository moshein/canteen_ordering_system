# Author: Nelle Lauzon (module: customer)

from contracts import ICustomer

class Customer(ICustomer):

    def __init__(self, name: str):
        

        if not isinstance(name, str) or not name.strip():
            raise ValueError("Customer name cannot be empty.")

        self._name = name.strip()
        self._order = None

    @property
    def name(self) -> str:
        return self._name

    @property
    def order(self):
        return self._order

    def sample_func(self):
        pass

    def __str__(self) -> str:
        return f"Customer: {self._name}"
