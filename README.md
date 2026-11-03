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
| Menu | Montimor, Oshein | `IMenu` |
| Customer | Lauzon, Nelle | `ICustomer` |
| Order | Casuboc, Ruena | `IOrder` |
| Payment | Odarve, Love | `IPayment` |
| Kitchen | Macaya, Jay Mark | `IKitchen` |


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

- **Abstraction:** Each module implements an Abstract Base Class (ABC) from the shared `contracts` package.
- **Encapsulation:** Internal attributes and read-only properties protect object data.
- **Inheritance and Polymorphism:** Classes implement shared contracts, allowing compatible objects to be used interchangeably.
- **Validation and Exceptions:** Invalid inputs raise `ValueError`, while business-rule violations raise `CanteenError` or its subclasses.
- **Independent Testing:** Test doubles, such as `FakeOrder` and `FakeMenu`, implement shared contracts to test modules independently without relying on teammates' concrete implementations.

Modules import only shared contracts and the Python standard library. The concrete implementations are intended to be connected through `main.py` during system integration.

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

This keeps the repository organized and prevents unnecessary changes or conflicts involving generated files.

## Development Tools and References

| Tool | Purpose |
|---|---|
| Python | Application development |
| VS Code | Code editing and debugging |
| Git and GitHub | Version control and collaboration |
| Python `unittest` | Automated unit testing |
| ChatGPT (OpenAI) | Learning assistance, debugging, testing, system integration, and documentation |

### AI Assistance Disclosure

Although we had a basic understanding of Object-Oriented Programming, working together on a project like this was not as easy as we first thought. We encountered challenges along the way, especially when testing and connecting our modules. Since some concepts were still new to us, we used ChatGPT (OpenAI) to help us better understand them, figure out our mistakes, and learn how to make things work in the following areas:

- **Unit Testing:** We initially struggled with understanding how unit testing works. AI helped us learn Python's `unittest` framework, create meaningful test cases, and use fake classes to test our modules independently.
- **System Integration (`main.py`):** At first, we thought integrating our modules would be as simple as calling functions. However, we learned that connecting different classes and passing objects between modules required a better understanding of their shared contracts. AI guided us through this process.
- **Exception Handling:** We had difficulty demonstrating business-rule violations without interrupting the program. AI introduced us to using `try-except` blocks to catch and handle expected errors gracefully while allowing the demonstration to continue.
- **Debugging and Code Review:** AI helped us identify mistakes, understand error messages, and improve our implementations when we encountered problems during development.

We remain fully responsible for understanding, testing, and explaining our work. All AI-assisted suggestions and implementations are subject to our own review and verification, ensuring that we can confidently demonstrate and justify the functionality of our respective modules.

