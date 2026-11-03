# canteen_ordering_system

**DS212 – Object-Oriented Programming – Team Package Project**

## Project Overview

The Canteen Ordering System is a Python-based application designed to manage food ordering in a school canteen. It allows customers to be registered according to their names and customer types, while food items and their availability are managed through the menu. Customers can place orders, calculate their totals, and proceed with payments. The kitchen module manages the order queue and monitors order statuses. The system uses separate modules and shared abstract contracts to organize responsibilities and allow the modules to work together.

## Team Members and Module Responsibilities

| Module | Owner | Contract ABC |
|---|---|---|
| Menu | Montimor | `IMenu` |
| Customer | Lauzon | `ICustomer` |
| Order | Casuboc | `IOrder` |
| Payment | Odarve | `IPayment` |
| Kitchen | Macaya | `IKitchen` |


## Project Structure

```text
canteen_ordering_system/
│
├── contracts/
│   └── __init__.py
│
├── menu/
│   └── __init__.py
│
├── customer/
│   └── __init__.py
│
├── payment/
│   └── __init__.py
│
├── kitchen/
│   └── __init__.py
│
├── order/
│   └── __init__.py
│
├── tests/
│   ├── test_menu.py
│   ├── test_customer.py
│   ├── test_payment.py
│   ├── test_kitchen.py
│   └── test_order.py
│
└── main.py
```

## Requirements

- Python 3.10 or later
- Python standard library

No external packages are required.

## How to Run the Program

Open a terminal in the project root directory and run:

```bash
python main.py
```

## How to Run the Tests

To run all module tests:

```bash
python -m unittest discover tests -v
```

To run an individual module's tests, for example Customer:

```bash
python -m unittest discover -s tests -p "test_customer.py" -v
```

## Notes

- Each module implements its assigned abstract contract from the `contracts` package.
- The `main.py` file connects the concrete module implementations.
- Unit tests are located in the `tests` directory.
