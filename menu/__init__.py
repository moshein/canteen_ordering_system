from contracts import IMenu

class Food(IMenu):
    def __init__(self, name: str, price: int):
        ## price shouldnt be zero dont forget

        self._name = name
        self._price = price

class Meal(Food):
    def __init__(self, name: str, price: int):
        super().__init__(name, price)

class ReadyToEat(Food):
    def __init__(self, name: str, price: int):
        super().__init__(name, price)

###############################################################################

class Menu(IMenu):
    def __init__(self):
        self._menu = {}

    def add_item(self, item: Food, quantity: int):
        menu = self._menu

        ## quantity should not be equal to 0
        ## quantity should not be negative rarawrawr
            ## if negative, dapat mag raise error
        ## later nako mag add cuz am so sleepy askdjfh

        menu.update({item: quantity})

        return f"{item} has been added to the menu"

    def remove_item(self, item: Food):
        menu = self._menu

        ## dont forget to raise error if wala ang item sa menu

        removed_item = menu.pop(item)

        return f"{removed_item} has been removed from the menu"

    @property
    def get_menu(self):
        menu = self._menu

        ## dont forget to add na if menu doesnt contain anything, it returns "menu doesnt have stuff"
        ## if menu == {""}

        return f"Canteen's menu \n\n{menu}"

    @property
    def available_items(self):
        menu = self._menu
        items_available = {}

        ## dont forget to add na if menu doesnt contain anything, it returns "menu doesnt have stuff"
        
        for item in menu:
            items_available.update({item: menu[item]})

    @property
    def unavailable_items(self):
        menu= self._menu
        items_unavailable = {}

        ## dont forget na mag add if menu doesnt contain anything hekhek

        for item in menu:
            items_unavailable.update({item: menu[item]})

## mew

