## Author: Oshein P. Montimor (module: menu)

from contracts import IMenu

class Food:
    def __init__(self, name: str, price: int|float):

        if not isinstance(name, str):
            raise TypeError("Name must be a string")

        if not isinstance(price, (int, float)):
            raise TypeError("Price must be a number.")

        if price <= 0:
            raise ValueError("Price must be greater than zero.")

        self._name = name
        self._price = round(float(price), 2)
        self._type = ""

    def __str__(self):
        return f"{self._name} - Php {self._price}"

    @property
    def name(self):
        return self._name

    @property
    def price(self):
        return self._price

    @property
    def foodType(self):
        return self._type


class Meal(Food):
    def __init__(self, name: str, price: int|float):
        super().__init__(name, price)
        self._type = "Meal"

    def __str__(self):
        return super().__str__()


class ReadyToEat(Food):
    def __init__(self, name: str, price: int|float):
        super().__init__(name, price)
        self._type = "Ready-To-Eat"

    def __str__(self):
        return super().__str__()


###############################################################################

class Menu(IMenu):
    def __init__(self):
        self._menu = []

    def add_item(self, item: Food, quantity: int):

        if not isinstance(item, Food):
            raise TypeError("Item must be a Food object")

        if not isinstance(quantity, int):
            raise TypeError("Quantity must be an integer.")

        if quantity <= 0:
            raise ValueError("Quantity should greater than zero.")

        menu = self._menu
        entry = [item.foodType, item.name, item.price]

        entry.append(quantity)
        menu.append(entry)
        

        return f"{item.name} has been added to the menu"

    def remove_item(self, item_name: str):

        if not self._menu:
            raise ValueError("Cannot remove a food item. The menu is empty")

        menu = self._menu

        for item in menu:
            if item[1] == item_name:
                menu.remove(item)

                return f"{item_name} has been removed from the menu"

        raise ValueError(f"{item_name} doesn't exist in the menu")

    @property
    def menu(self):
        
        if not self._menu:
            raise ValueError("Menu is empty.")

        return self._menu.copy()

        # ### uncomment this part if they dont need this function for data
                        
        # menu_meal = ""
        # menu_ready = ""

        # for item in self._menu:

        #     if item[0] == "Meal":
        #         menu_meal += f"{item[1]} - Php {item[2]} (Stocks available: {item[3]})\n"

        #     if item[0] == "Ready-To-Eat":
        #         menu_ready += f"{item[1]} - Php {item[2]} (Stocks available: {item[3]})\n"

        # menu_display = "Food Meals: \n" + menu_meal + "\n\n" + "Ready-To-Eat Foods: \n" + menu_ready

        # return menu_display

    @property
    def available_items(self):

        if not self._menu:
            raise ValueError("Menu is empty. Add more food items.")

        items_available_list = []

        for item in self._menu:
            if item[3] > 0:
                items_available_list.append(item)

        return items_available_list

        

    @property
    def unavailable_items(self):

        if not self._menu:
            raise ValueError("Menu is empty. Add more food items")

        menu= self._menu
        items_unavailable_list = []


        for item in menu:
            if item[3] <= 0:
                items_unavailable_list.append(item)

        return items_unavailable_list

##mew