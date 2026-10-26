# -*- coding: utf-8 -*-
"""
Deterministik Doğrulama ve Eval Harness Örneği
Bu script, bir yapay zekâ modelinin veya ajanının ürettiği fonksiyonu
Property-Based Testing mantığıyla 1.000 rastgele senaryoda sınar.
"""

import sys
from typing import Dict, Any

# Konsol UTF-8 desteği
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

# ============================================================================
# 1. MODELİN ÜRETTİĞİ FONKSİYON (ÖRNEK TEST EDİLEN KOD)
# ============================================================================
def transfer_balance(sender: Dict[str, Any], receiver: Dict[str, Any], amount: int) -> bool:
    """
    Bir hesaptan diğerine bakiye transfer eder.
    Değişmez 1: Transfer tutarı pozitif tamsayı olmalıdır.
    Değişmez 2: Göndericinin bakiyesi transfer tutarından az olamaz (eksi bakiye yasak).
    Değişmez 3: Sistemdeki toplam para (sender + receiver) işlem öncesi ve sonrası EŞİT kalmalıdır.
    """
    if amount <= 0:
        return False
    if sender["balance"] < amount:
        return False
    
    sender["balance"] -= amount
    receiver["balance"] += amount
    return True


# ============================================================================
# 2. DETERMINISTIK EVAL HARNESS & PROPERTY TESTER
# ============================================================================
def run_eval_suite():
    print("Deterministik Dogrulama Testi Baslatiliyor...")
    import random

    iterations = 1000
    violations = []

    for i in range(iterations):
        initial_sender_balance = random.randint(0, 100_000)
        initial_receiver_balance = random.randint(0, 100_000)
        transfer_amount = random.randint(-10_000, 120_000)

        sender = {"id": "user_1", "balance": initial_sender_balance}
        receiver = {"id": "user_2", "balance": initial_receiver_balance}

        total_before = initial_sender_balance + initial_receiver_balance
        success = transfer_balance(sender, receiver, transfer_amount)

        total_after = sender["balance"] + receiver["balance"]

        # Değişmez Kontrolleri (Invariant Assertions)
        if success:
            # Başarılı ise toplam bakiye korunmalıdır
            if total_before != total_after:
                violations.append(f"İterasyon {i}: Para yoktan var oldu veya kayboldu! Öncesi={total_before}, Sonrası={total_after}")
            # Gönderici bakiyesi negatif olamaz
            if sender["balance"] < 0:
                violations.append(f"İterasyon {i}: Gönderici bakiyesi negatife düştü: {sender['balance']}")
        else:
            # Başarısız ise bakiyeler ASLA değişmemelidir
            if sender["balance"] != initial_sender_balance or receiver["balance"] != initial_receiver_balance:
                violations.append(f"İterasyon {i}: Başarısız işlemde bakiye mutasyona uğradı!")

    if violations:
        print(f"X BASARISIZ! {len(violations)} adet degismez kural ihlali tespit edildi:")
        for v in violations[:5]:
            print(f"   - {v}")
        sys.exit(1)
    else:
        print(f"[OK] BASARILI! {iterations} rastgele senaryoda hicbir sistem degismezi ihlal edilmedi.")
        print("[OK] Kod deterministik dogrulama suzgecinden basariyla gecti.")


if __name__ == "__main__":
    run_eval_suite()
