# Payment module test (Odarve)

import unittest

from contracts import IOrder, IPayment, CanteenError
from payment import CashPayment, EWalletPayment



class FakeOrder(IOrder):
    def __init__(self, total):
        self._total = total
        self._active_orders = ()

    @property
    def total(self) -> float:
        """Return the amount the customer must pay."""
        return self._total

    @property
    def active_orders(self) -> tuple:
        """Return active orders."""
        return self._active_orders

    def create_order(self, order_number: str, item: str) -> None:
        """Not used in Payment tests."""
        raise NotImplementedError(
            "Order creation is not part of these tests."
        )

    def cancel_order(self, order_number: str) -> None:
        """Not used in Payment tests."""
        raise NotImplementedError(
            "Order cancellation is not part of these tests."
        )


class TestPayment(unittest.TestCase):
    # 1. Test if cash payment calculates the correct change and updates the payment status.
    def test_cash_payment_calculates_change(self):
        payment = CashPayment(200)
        self.assertEqual(payment.pay(FakeOrder(150)), 50.0)
        self.assertTrue(payment.paid)

    # 2. Test if exact cash payment is accepted with zero change.
    def test_cash_exact_payment(self):
        payment = CashPayment(150)
        self.assertEqual(payment.pay(FakeOrder(150)), 0.0)

    # 3. Test if insufficient cash raises CanteenError and leaves the payment unpaid.
    def test_insufficient_cash_raises_canteen_error(self):
        payment = CashPayment(100)
        with self.assertRaises(CanteenError):
            payment.pay(FakeOrder(150))
        self.assertFalse(payment.paid)

    # 4. Test if duplicate cash payment raises CanteenError.
    def test_duplicate_cash_payment_raises_canteen_error(self):
        payment = CashPayment(200)
        order = FakeOrder(150)
        payment.pay(order)
        with self.assertRaises(CanteenError):
            payment.pay(order)

    # 5. Test if e-wallet payment deducts the correct balance and marks payment as successful.
    def test_e_wallet_deducts_balance(self):
        payment = EWalletPayment(500)
        self.assertEqual(payment.pay(FakeOrder(150)), 0.0)
        self.assertEqual(payment.balance, 350.0)
        self.assertTrue(payment.paid)

    # 6. Test if insufficient wallet funds raise CanteenError without deducting the balance.
    def test_insufficient_wallet_raises_canteen_error(self):
        payment = EWalletPayment(100)
        with self.assertRaises(CanteenError):
            payment.pay(FakeOrder(150))
        self.assertEqual(payment.balance, 100.0)
        self.assertFalse(payment.paid)

    # 7. Test if duplicate e-wallet payment is rejected without another balance deduction.
    def test_duplicate_wallet_payment_raises_canteen_error(self):
        payment = EWalletPayment(500)
        order = FakeOrder(150)
        payment.pay(order)
        with self.assertRaises(CanteenError):
            payment.pay(order)
        self.assertEqual(payment.balance, 350.0)

    # 8. Test if CashPayment rejects invalid amounts during initialization.
    def test_cash_constructor_rejects_bad_inputs(self):
        for bad_amount in (-1, 0, "200", True, 100.123):
            with self.subTest(bad_amount=bad_amount):
                with self.assertRaises(ValueError):
                    CashPayment(bad_amount)

    # 9. Test if EWalletPayment rejects invalid balances but allows zero balance.
    def test_wallet_constructor_rejects_bad_inputs(self):
        for bad_balance in (-1, "500", False, float("inf")):
            with self.subTest(bad_balance=bad_balance):
                with self.assertRaises(ValueError):
                    EWalletPayment(bad_balance)
        self.assertEqual(EWalletPayment(0).balance, 0.0)

    # 10. Test if both payment classes reject objects that do not implement IOrder.
    def test_payment_requires_an_iorder_object(self):
        with self.assertRaises(ValueError):
            CashPayment(200).pay(150)
        with self.assertRaises(ValueError):
            EWalletPayment(500).pay("order")

    # 11. Test if CashPayment rejects invalid order totals.
    def test_invalid_order_totals_are_rejected(self):
        for bad_total in (0, -5, 10.123, "150", True):
            with self.subTest(bad_total=bad_total):
                with self.assertRaises(ValueError):
                    CashPayment(200).pay(FakeOrder(bad_total))

    # 12. Test if EWalletPayment rejects an order with zero total.
    def test_e_wallet_rejects_invalid_order_total(self):
        with self.assertRaises(ValueError):
            EWalletPayment(500).pay(FakeOrder(0))

    # 13. Test if read-only properties prevent direct reassignment.
    def test_properties_are_read_only(self):
        cash = CashPayment(200)
        wallet = EWalletPayment(500)
        with self.assertRaises(AttributeError):
            cash.cash_received = 900
        with self.assertRaises(AttributeError):
            wallet.balance = 900
        with self.assertRaises(AttributeError):
            cash.method = "e-wallet"

    # 14. Test if CashPayment and EWalletPayment both implement IPayment.
    def test_both_classes_follow_ipayment(self):
        self.assertIsInstance(CashPayment(200), IPayment)
        self.assertIsInstance(EWalletPayment(500), IPayment)

    # 15. Test if polymorphism allows one checkout function to handle both payment types.
    def test_polymorphism_with_both_payment_types(self):
        def checkout(payment: IPayment, order: IOrder):
            return payment.pay(order)

        order = FakeOrder(150)
        self.assertEqual(checkout(CashPayment(200), order), 50.0)
        self.assertEqual(checkout(EWalletPayment(500), order), 0.0)

    # 16. Test if both payment classes provide readable descriptions through __str__().
    def test_str_descriptions(self):
        self.assertIn("Cash payment", str(CashPayment(200)))
        self.assertIn("E-wallet balance", str(EWalletPayment(500)))
