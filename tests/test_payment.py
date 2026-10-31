# Payment module test (Odarve)

import unittest

from contracts import IOrder, IPayment, CanteenError
from payment import CashPayment, EWalletPayment


class FakeOrder(IOrder):
    """A small IOrder implementation used ani nga tests."""

    def __init__(self, total):
        """Store a sample total (including invalid values for validation tests)."""
        self._total = total

    @property
    def total(self):
        """Return the sample total."""
        return self._total


class TestPayment(unittest.TestCase):
    """Check cash, e-wallet, contract usage, and payment failure rules."""

    def test_cash_payment_calculates_change(self):
        payment = CashPayment(200)
        self.assertEqual(payment.pay(FakeOrder(150)), 50.0)
        self.assertTrue(payment.paid)

    def test_cash_exact_payment(self):
        payment = CashPayment(150)
        self.assertEqual(payment.pay(FakeOrder(150)), 0.0)

    def test_insufficient_cash_raises_canteen_error(self):
        payment = CashPayment(100)
        with self.assertRaises(CanteenError):
            payment.pay(FakeOrder(150))
        self.assertFalse(payment.paid)

    def test_duplicate_cash_payment_raises_canteen_error(self):
        payment = CashPayment(200)
        order = FakeOrder(150)
        payment.pay(order)
        with self.assertRaises(CanteenError):
            payment.pay(order)

    def test_e_wallet_deducts_balance(self):
        payment = EWalletPayment(500)
        self.assertEqual(payment.pay(FakeOrder(150)), 0.0)
        self.assertEqual(payment.balance, 350.0)
        self.assertTrue(payment.paid)

    def test_insufficient_wallet_raises_canteen_error(self):
        payment = EWalletPayment(100)
        with self.assertRaises(CanteenError):
            payment.pay(FakeOrder(150))
        self.assertEqual(payment.balance, 100.0)
        self.assertFalse(payment.paid)

    def test_duplicate_wallet_payment_raises_canteen_error(self):
        payment = EWalletPayment(500)
        order = FakeOrder(150)
        payment.pay(order)
        with self.assertRaises(CanteenError):
            payment.pay(order)
        self.assertEqual(payment.balance, 350.0)

    def test_cash_constructor_rejects_bad_inputs(self):
        for bad_amount in (-1, 0, "200", True, 100.123):
            with self.subTest(bad_amount=bad_amount):
                with self.assertRaises(ValueError):
                    CashPayment(bad_amount)

    def test_wallet_constructor_rejects_bad_inputs(self):
        for bad_balance in (-1, "500", False, float("inf")):
            with self.subTest(bad_balance=bad_balance):
                with self.assertRaises(ValueError):
                    EWalletPayment(bad_balance)
        self.assertEqual(EWalletPayment(0).balance, 0.0)

    def test_payment_requires_an_iorder_object(self):
        with self.assertRaises(ValueError):
            CashPayment(200).pay(150)
        with self.assertRaises(ValueError):
            EWalletPayment(500).pay("order")

    def test_invalid_order_totals_are_rejected(self):
        for bad_total in (0, -5, 10.123, "150", True):
            with self.subTest(bad_total=bad_total):
                with self.assertRaises(ValueError):
                    CashPayment(200).pay(FakeOrder(bad_total))

    def test_e_wallet_rejects_invalid_order_total(self):
        with self.assertRaises(ValueError):
            EWalletPayment(500).pay(FakeOrder(0))

    def test_properties_are_read_only(self):
        cash = CashPayment(200)
        wallet = EWalletPayment(500)
        with self.assertRaises(AttributeError):
            cash.cash_received = 900
        with self.assertRaises(AttributeError):
            wallet.balance = 900
        with self.assertRaises(AttributeError):
            cash.method = "e-wallet"

    def test_both_classes_follow_ipayment(self):
        self.assertIsInstance(CashPayment(200), IPayment)
        self.assertIsInstance(EWalletPayment(500), IPayment)

    def test_polymorphism_with_both_payment_types(self):
        def checkout(payment: IPayment, order: IOrder):
            return payment.pay(order)

        order = FakeOrder(150)
        self.assertEqual(checkout(CashPayment(200), order), 50.0)
        self.assertEqual(checkout(EWalletPayment(500), order), 0.0)

    def test_str_descriptions(self):
        self.assertIn("Cash payment", str(CashPayment(200)))
        self.assertIn("E-wallet balance", str(EWalletPayment(500)))


if __name__ == "__main__":
    unittest.main()
