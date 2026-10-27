# -*- coding: utf-8 -*-
"""
Referans Ödeme Servisi İmplemantasyonu (Orkestrasyon Standardı)
Bu kod, spec.json şartnamesine %100 sadık kalınarak,
idempotency, concurrency locking ve strict state machine ilkeleriyle inşa edilmiştir.
"""

import time
import uuid
import threading
from typing import Dict, Any, Optional

class ResilientPaymentService:
    def __init__(self):
        self._idempotency_store: Dict[str, Dict[str, Any]] = {}
        self._order_locks: Dict[str, threading.Lock] = {}
        self._global_lock = threading.Lock()
        self._order_status: Dict[str, str] = {}
        self._total_collected_cents = 0

    def _get_order_lock(self, order_id: str) -> threading.Lock:
        with self._global_lock:
            if order_id not in self._order_locks:
                self._order_locks[order_id] = threading.Lock()
            return self._order_locks[order_id]

    def process_payment(self, request: Dict[str, Any]) -> Dict[str, Any]:
        # 1. Girdi ve Sözleşme Denetimi
        idempotency_key = request.get("idempotencyKey")
        order_id = request.get("orderId")
        amount = request.get("amountCents", 0)
        currency = request.get("currency", "TRY")

        if not idempotency_key or not order_id:
            raise ValueError("idempotencyKey ve orderId zorunludur.")
        if not isinstance(amount, int) or amount <= 0:
            raise ValueError("amountCents sifirdan buyuk tam sayi olmalidir.")

        # 2. Idempotency Kontrolü (Hızlı Yol)
        with self._global_lock:
            if idempotency_key in self._idempotency_store:
                cached = self._idempotency_store[idempotency_key]
                return {**cached, "cached": True}

        # 3. Sipariş Seviyesinde Kilitleme (Concurrency Protection)
        order_lock = self._get_order_lock(order_id)
        with order_lock:
            # Kilidi aldıktan sonra tekrar idempotency kontrolü (Double-checked locking)
            with self._global_lock:
                if idempotency_key in self._idempotency_store:
                    return {**self._idempotency_store[idempotency_key], "cached": True}
                if self._order_status.get(order_id) == "SUCCESS":
                    raise RuntimeError(f"Siparis zaten odenmis: {order_id}")

            # 4. İşlem Gerçekleştirme (Simülasyon)
            tx_id = f"tx_{uuid.uuid4().hex[:12]}"
            response = {
                "transactionId": tx_id,
                "orderId": order_id,
                "amountCents": amount,
                "currency": currency,
                "status": "SUCCESS",
                "processedAt": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                "cached": False
            }

            # 5. Atomik Durum ve Bakiye Güncellemesi
            with self._global_lock:
                self._total_collected_cents += amount
                self._order_status[order_id] = "SUCCESS"
                self._idempotency_store[idempotency_key] = response

            return response

    @property
    def total_collected_cents(self) -> int:
        with self._global_lock:
            return self._total_collected_cents
