# -*- coding: utf-8 -*-
"""
Sistem Performans ve Gecikme Ölçüm Aracı (Benchmark Runner)
"""

import os
import sys
import time
from typing import Callable, Any, Dict

# UTF-8 konsol desteği
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

def run_benchmark(name: str, fn: Callable[[], Any], iterations: int = 1000) -> Dict[str, Any]:
    print(f"⚡ BENCHMARK BAŞLATILIYOR: {name} ({iterations:,} iterasyon)...")
    start = time.perf_counter()
    for _ in range(iterations):
        fn()
    elapsed = time.perf_counter() - start
    
    avg_us = (elapsed / iterations) * 1_000_000
    ops_sec = int(iterations / elapsed) if elapsed > 0 else 0
    
    print("=" * 60)
    print(f"BENCHMARK SONUCU: {name}")
    print("=" * 60)
    print(f"Toplam Süre     : {elapsed:.4f} saniye")
    print(f"Ortalama İşlem  : {avg_us:.2f} µs (mikrosaniye)")
    print(f"İşlem / Saniye  : {ops_sec:,} ops/sec")
    print("-" * 60)
    return {"name": name, "total_seconds": elapsed, "avg_microseconds": avg_us, "ops_sec": ops_sec}

if __name__ == "__main__":
    # Test amaçlı örnek mikroservis benchmarkı
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "examples", "resilient-payment-service"))
    from service import ResilientPaymentService
    srv = ResilientPaymentService()
    req = {"idempotencyKey": "bench-key", "orderId": "bench-order", "amountCents": 100, "currency": "TRY"}
    run_benchmark("ResilientPaymentService (Idempotent Cache Hit)", lambda: srv.process_payment(req), 10_000)
