'''
main.py

What it is:
A demo script that creates objects
from all 5 modules and runs a
realistic story

Who writes it:
Whole group during integration
'''

## akjdf


# Author: Jay Mark J. Macaya
# Demo script for KitchenQueue

from kitchen import KitchenQueue, KitchenFullError, OrderNotFoundError

# 1. Create a KitchenQueue object
kitchen = KitchenQueue(capacity=3)

print("=== KITCHEN QUEUE DEMO ===")
print(kitchen)

# 2. Create and add orders
print("\nAdding orders...")

kitchen.add_to_queue("ORD001", "Chicken Adobo")
kitchen.add_to_queue("ORD002", "Pork Sinigang")
kitchen.add_to_queue("ORD003", "Fried Rice")

print("Orders successfully added!")
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

# 5. Demonstrate exception handling
print("\nTesting Kitchen Capacity...")

try:
    kitchen.add_to_queue("ORD004", "Pancit")
except KitchenFullError as e:
    print("Error:", e)

# 6. Demonstrate order not found
print("\nTesting Order Not Found...")

try:
    kitchen.update_status("ORD999", "Preparing")
except OrderNotFoundError as e:
    print("Error:", e)

# 7. Complete an order
print("\nCompleting an order...")

kitchen.update_status("ORD001", "Completed")

print("ORD001 has been completed.")
print("Remaining Active Orders:", kitchen.pending_orders)

print("\n=== DEMO FINISHED ===")