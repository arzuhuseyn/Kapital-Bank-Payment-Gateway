import unittest

from base import KapitalPayment


class KapitalPaymentTest(unittest.TestCase):
    def setUp(self) -> None:
        self.gateway=KapitalPayment(
            merchant_id="E1000010",
            approve_url="https://test.com/approve",
            cancel_url="https://test.com/cancel",
            decline_url="https://test.com/decline",
        )

    def test_create_order(self):
        transaction = self.gateway.create_order(amount=10, currency=944, description="Test", lang="AZ")
        payment_obj=self.gateway.get_payment_obj()
        result = {'url': f'https://e-commerce.kapitalbank.az/?ORDERID={payment_obj.order_id}&SESSIONID={payment_obj.session_id}'}
        self.assertDictEqual(result, transaction)
        self.assertEqual(payment_obj.status_code, '00')
