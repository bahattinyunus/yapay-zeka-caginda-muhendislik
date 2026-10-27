# -*- coding: utf-8 -*-
"""
Referans Ödeme Servisi İçin Deterministik Testler ve Property Sınaması
"""

import os
import sys
import unittest
import threading
import uuid
import random

# Dizin içi import desteği
sys.path.insert(0, os.path.dirname(__file__))
from service import ResilientPaymentService

class TestResilientPaymentService(unittest.TestCase):
    def setUp(self):
        self.service = ResilientPaymentService()

    def test_single_payment_success(self):
        req = {
            "idempotencyKey": "key-1",
            "orderId": "order-1",
            "amountCents": 1500,
            "currency": "TRY"
        }
        res = self.service.process_payment(req)
        self.assertEqual(res["status"], "SUCCESS")
        self.assertEqual(res["cached"], False)
        self.assertEqual(self.service.total_collected_cents, 1500)

    def test_idempotency_prevents_double_charge(self):
        req = {
            "idempotencyKey": "unique-idem-key",
            "orderId": "order-idem",
            "amountCents": 2000,
            "currency": "TRY"
        }
        res1 = self.service.process_payment(req)
        res2 = self.service.process_payment(req)

        self.assertEqual(res1["transactionId"], res2["transactionId"])
        self.assertEqual(res2["cached"], True)
        self.assertEqual(self.service.total_collected_cents, 2000, "Cift tahsilat engellenmeliydi!")

    def test_concurrent_idempotent_requests(self):
        # 50 eşzamanlı iş parçacığı aynı ödemeyi yapmaya çalışsın
        threads = []
        results = []
        idem_key = "concurrent-key-" + uuid.uuid4().hex
        order_id = "concurrent-order-" + uuid.uuid4().hex

        def worker():
            req = {
                "idempotencyKey": idem_key,
                "orderId": order_id,
                "amountCents": 5000,
                "currency": "TRY"
            }
            try:
                res = self.service.process_payment(req)
                results.append(res)
            except Exception:
                pass

        for _ in range(50):
            t = threading.Thread(target=worker)
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        self.assertEqual(len(results), 50)
        self.assertEqual(self.service.total_collected_cents, 5000, "50 istekte bakiye yalnizca 1 kez artmali!")

    def test_invalid_amounts_rejected(self):
        with self.assertRaises(ValueError):
            self.service.process_payment({
                "idempotencyKey": "k",
                "orderId": "o",
                "amountCents": -50,
                "currency": "TRY"
            })

if __name__ == "__main__":
    unittest.main()
