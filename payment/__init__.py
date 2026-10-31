# Author: Love Romelyn U. Odarve (module: payment)

from math import isfinite
from contracts import IPayment, IOrder, CanteenError


def _check_amount(amount, allow_zero=False):
    """Validate a peso amount and return it to two decimal places."""
    if isinstance(amount, bool) or not isinstance(amount, (int, float)):
        raise ValueError("Amount must be a number.")
    if not isfinite(amount) or amount < 0 or (amount == 0 and not allow_zero):
        raise ValueError("Amount must be positive, or zero when allowed.")
    if round(amount, 2) != amount:
        raise ValueError("Amount must have at most two decimal places.")
    return round(float(amount), 2)


def _get_order_total(order):
    """Read the final payable amount from an IOrder object."""
    if not isinstance(order, IOrder):
        raise ValueError("Payment requires an IOrder object.")
    return _check_amount(order.total)


class CashPayment(IPayment):
    """Process one cash payment and calculate the customer's change."""

    def __init__(self, cash_received):
        """Store the cash received from the customer."""
        self._cash_received = _check_amount(cash_received)
        self._paid = False

    @property
    def method(self):
        """Return the payment method name."""
        return "cash"

    @property
    def cash_received(self):
        """Return the cash received in pesos (read-only)."""
        return self._cash_received

    @property
    def paid(self):
        """Return True if this payment has already succeeded."""
        return self._paid

    def pay(self, order: IOrder) -> float:
        """Pay an order once; return the change in pesos."""
        if self._paid:
            raise CanteenError("This checkout is already paid.")

        total = _get_order_total(order)
        if self._cash_received < total:
            raise CanteenError("Not enough cash.")

        self._paid = True
        return round(self._cash_received - total, 2)

    def __str__(self):
        """Describe this cash payment."""
        return f"Cash payment: PHP {self._cash_received:.2f} received"


class EWalletPayment(IPayment):
    """Process one simulated e-wallet payment; no real funds are transferred."""

    def __init__(self, balance):
        """Store the simulated wallet's starting balance in pesos."""
        self._balance = _check_amount(balance, allow_zero=True)
        self._paid = False

    @property
    def method(self):
        """Return the payment method name."""
        return "e-wallet"

    @property
    def balance(self):
        """Return the simulated wallet's current balance (read-only)."""
        return self._balance

    @property
    def paid(self):
        """Return True if this payment has already succeeded."""
        return self._paid

    def pay(self, order: IOrder) -> float:
        """Pay an order once; return 0.0 when successful."""
        if self._paid:
            raise CanteenError("This checkout is already paid.")

        total = _get_order_total(order)
        if self._balance < total:
            raise CanteenError("Not enough e-wallet balance.")

        self._balance = round(self._balance - total, 2)
        self._paid = True
        return 0.0

    def __str__(self):
        """Describe this simulated wallet payment."""
        return f"E-wallet balance: PHP {self._balance:.2f}"
