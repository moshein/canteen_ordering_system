'''
main.py

What it is:
A demo script that creates objects
from all 5 modules and runs a
realistic story

Who writes it:
Whole group during integration
'''


from menu import Menu, Meal, ReadyToEat, InvalidQuantityError
from customer import Customer, CanteenError
from order import Order,  OrderLockedError
from payment import CashPayment, EWalletPayment
from kitchen import KitchenQueue, KitchenFullError, OrderNotFoundError



def main():

    ############################
    ##    Menu Module 
    ############################

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

    print("\n========== BUSINESS RULE: INVALID QUANTITY ==========")

    try:
        canteen_menu.add_item(Meal("Pancit", 60.00), 0)

    except InvalidQuantityError as error:
        print("Handled error:", error)


    #######################################
    ##    Order & Customer Modules 
    ###################################


    # Create an Order object
    order = Order(canteen_menu)

    # Create a Customer object
    customer = Customer(
        "Love Odarve",
        "Student",
        order
    )

    # Add food to the cart
    order.add_to_cart("Chicken Rice", 1)

    # Submit the order
    order.create_order("ORD-001", "Chicken Rice")

    # Associate the order with the customer
    customer.add_order("ORD-001")


    # Display customer information
    print("\n========== CUSTOMER INFORMATION ==========")
    print("Name:", customer.name)
    print("Customer Type:", customer.customer_type)


    # Display customer's order IDs
    print("\n========== CUSTOMER ORDERS ==========")
    print("Order IDs:", customer.order_ids)


    # Show pending orders
    print("\n========== PENDING ORDERS ==========")
    print("Active Orders:", order.active_orders)

    # Demonstrate business rule: modifying order
    
    try:
        order.add_to_cart("Chicken Rice", 10)

    except OrderLockedError as error:
        print("Handled error:", error)

    # Attempt to remove customer with pending orders
    print("\n========== REMOVE CUSTOMER ==========")


    try:
        customer.remove_customer()
        print(f"{customer.name}'s order records cleared.")

    except CanteenError as error:
        print(f"Unable to remove customer: {error}")


    ############################
    ##    Payment Module 
    ############################

    print("\n========== PAYMENT MODULE ==========")

    # Successful cash payment: 2 burgers at PHP 50 each = PHP 100.
    cash_order = Order(canteen_menu)
    cash_order.add_to_cart("Burger", 2)
    cash_order.create_order("PAY-001", "Burger")

    cash_payment = CashPayment(150)
    cash_change = cash_payment.pay(cash_order)

    print("\n[CASH PAYMENT]")
    print(f"Order total: PHP {cash_order.total:.2f}")
    print(f"Cash received: PHP {cash_payment.cash_received:.2f}")
    print(f"Change: PHP {cash_change:.2f}")
    print(f"Paid: {cash_payment.paid}")

    # Successful simulated wallet payment.
    wallet_order = Order(canteen_menu)
    wallet_order.add_to_cart("Chicken Rice", 1)
    wallet_order.create_order("PAY-002", "Chicken Rice")

    wallet_payment = EWalletPayment(200)
    wallet_payment.pay(wallet_order)

    print("\n[SIMULATED E-WALLET PAYMENT]")
    print(f"Order total: PHP {wallet_order.total:.2f}")
    print(f"Remaining wallet balance: PHP {wallet_payment.balance:.2f}")
    print(f"Paid: {wallet_payment.paid}")

    # Business rule 1: insufficient cash.
    print("\n[BUSINESS RULE: INSUFFICIENT FUNDS]")

    try:
        CashPayment(50).pay(cash_order)

    except CanteenError as error:
        print(f"Handled error: {error}")

    # Business rule 2: a payment object cannot be used twice.
    print("\n[BUSINESS RULE: DUPLICATE PAYMENT]")

    try:
        cash_payment.pay(cash_order)

    except CanteenError as error:
        print(f"Handled error: {error}")


    #############################
    ## Kitchen Module
    ############################

    print("\n========== KITCHEN MODULE ==========")

    # 1. Create a KitchenQueue object
    kitchen = KitchenQueue(capacity=3)

    print(kitchen)

    # 2. Create and add orders
    print("\nAdding orders to the kitchen queue...")

    kitchen.add_to_queue("ORD001", "Chicken Adobo")
    kitchen.add_to_queue("ORD002", "Pork Sinigang")
    kitchen.add_to_queue("ORD003", "Fried Rice")

    print("Orders successfully added to the queue!")
    print()
    print("Pending Orders:", kitchen.pending_orders)

    # 3. Update order status
    print("\nUpdating order status...")

    kitchen.update_status("ORD001", "Preparing")
    kitchen.update_status("ORD002", "Ready")

    print("ORD001 is now Preparing.")
    print("ORD002 is now Ready.")

    # 4. Display kitchen information
    print("\nKitchen Information:")
    print(kitchen)
    print("Active Orders:", kitchen.pending_orders)

    # 5. Demonstrate kitchen capacity exception
    print("\nTesting Kitchen Capacity...")

    try:
        kitchen.add_to_queue("ORD004", "Pancit")

    except KitchenFullError as error:
        print("Error:", error)

    # 6. Demonstrate order not found
    print("\nTesting Order Not Found...")

    try:
        kitchen.update_status("ORD999", "Preparing")

    except OrderNotFoundError as error:
        print("Error:", error)

    # 7. Complete an order
    print("\nCompleting an order...")

    kitchen.update_status("ORD001", "Completed")

    print("ORD001 has been completed.")
    print("Remaining Active Orders:", kitchen.pending_orders)

    print("\n=== DEMO FINISHED ===")


if __name__ == "__main__":
    main()

