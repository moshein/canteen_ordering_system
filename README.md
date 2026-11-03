# Canteen Ordering System

**DS212 – Object-Oriented Programming**  
**Team Package Project**  
**Year & Section:** 2nd Year – DS2B  
**Language:** Python 3.10+

## Project Overview

The Canteen Ordering System is a Python-based application that simulates food ordering in a school canteen. It manages customers, food items, orders, cash and e-wallet payments, and kitchen operations. The system consists of five independently developed modules connected through shared Abstract Base Classes (ABCs). It demonstrates Object-Oriented Programming principles, including abstraction, encapsulation, inheritance, polymorphism, and exception handling.

## Team Members and Responsibilities

| Module | Owner | Contract |
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
├── .gitignore
├── main.py
└── README.md
```

## Requirements

- Python 3.10 or later
- Python standard library only
- No external packages required

## How to Run

Open a terminal in the project's root directory.

**Run the application:**

```bash
python main.py
```

**Run all unit tests:**

```bash
python -m unittest discover tests -v
```

**Run a specific module's tests (Payment example):**

```bash
python -m unittest discover -s tests -p "test_payment.py" -v
```

Replace `test_payment.py` with another test filename to test a different module.

## OOP Design and Integration

The system follows a contract-based architecture:

- **Abstraction:** Each module implements an ABC from `contracts/`.
- **Encapsulation:** Internal attributes and read-only properties protect object data.
- **Inheritance and Polymorphism:** Classes implement shared contracts, allowing compatible objects to be used interchangeably.
- **Validation and Exceptions:** Invalid inputs use `ValueError`, while business-rule violations use the shared `CanteenError`.
- **Independent Testing:** Test doubles, such as `FakeOrder`, implement shared contracts to test modules without importing teammates' concrete classes.

Modules import only shared contracts and the Python standard library. Concrete implementations are connected through `main.py`.

## Contract Change Log

| Contract | Changes |
|---|---|
| `IOrder` | Added `create_order()`, `cancel_order()`, and `active_orders` alongside `total`. |
| `IPayment` | Uses `pay(order: IOrder)` for contract-based payment processing. |
| `IOrder` | Consolidated duplicate definitions into one complete contract. |

Changes to shared contracts are coordinated through the group's designated contract keeper.

## Git Configuration

The `.gitignore` file excludes Python-generated cache files:

```gitignore
__pycache__/
*.pyc
```

This keeps the repository organized and prevents unnecessary changes or conflicts involving generated files. Previously tracked cache files must be removed from Git tracking separately.

## Development Tools and References

| Tool | Purpose |
|---|---|
| Python | Application development |
| VS Code | Code editing and debugging |
| Git and GitHub | Version control and collaboration |
| Python `unittest` | Automated unit testing |
| ChatGPT (OpenAI) | Guidance on OOP concepts, debugging, contracts, unit testing, Git workflows, and documentation |

Team members are responsible for understanding and explaining their own implementations. 


