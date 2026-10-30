'''
main.py

What it is:
A demo script that creates objects
from all 5 modules and runs a
realistic story

Who writes it:
Whole group during integration
'''


from menu import Menu, Meal, ReadyToEat


def main():

    # Create a Menu object
    canteen_menu = Menu()

    # Add food items
    canteen_menu.add_item(Meal("Chicken Rice", 75.00), 10)
    canteen_menu.add_item(Meal("Burger", 50.00), 5)
    canteen_menu.add_item(ReadyToEat("Iced Tea", 25.00), 8)

    # Display the menu
    print("\n========== CANTEEN MENU ==========")

    for food_type, name, price, quantity in canteen_menu.menu:
        print(f"{name} - Php {price:.2f} - Quantity: {quantity}")

    # Check if an item exists
    print("\n========== ITEM SEARCH ==========")
    print("Burger exists:", canteen_menu.has_item("Burger"))

    # Display available items
    print("\n========== AVAILABLE ITEMS ==========")

    for item in canteen_menu.available_items:
        print(item)

    # Remove an item
    print("\n========== REMOVE ITEM ==========")
    print(canteen_menu.remove_item("Iced Tea"))

    # Display updated menu
    print("\n========== UPDATED MENU ==========")

    for item in canteen_menu.menu:
        print(item)


if __name__ == "__main__":
    main()

