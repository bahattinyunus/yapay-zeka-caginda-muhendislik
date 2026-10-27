# -*- coding: utf-8 -*-
"""
Otonom Değerlendirme ve İterasyon Koşucusu (Eval Runner)
Yapay zekâ tarafından üretilen iş mantıklarını N sayıda rastgele senaryoda
ve değişmezlik (invariant) denetiminde koşturur.
"""

import sys
import time
import random
from typing import Callable, List, Dict, Any, Tuple

# UTF-8 konsol desteği
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

class EvalReport:
    def __init__(self, name: str):
        self.name = name
        self.total_runs = 0
        self.success_count = 0
        self.failure_count = 0
        self.violations: List[str] = []
        self.duration_seconds = 0.0

    def add_result(self, is_success: bool, violation_msg: str = None):
        self.total_runs += 1
        if is_success:
            self.success_count += 1
        else:
            self.failure_count += 1
            if violation_msg:
                self.violations.append(violation_msg)

    def print_summary(self) -> bool:
        print("=" * 60)
        print(f"EVAL DEĞERLENDİRME ÖZETİ: {self.name}")
        print("=" * 60)
        print(f"Toplam İterasyon   : {self.total_runs}")
        success_rate = (self.success_count / self.total_runs) * 100 if self.total_runs > 0 else 0
        print(f"Başarılı İterasyon : {self.success_count} (%{success_rate:.1f})")
        print(f"İhlal / Başarısız  : {self.failure_count}")
        print(f"Toplam Süre        : {self.duration_seconds:.4f} saniye")
        print("-" * 60)
        if self.failure_count == 0:
            print("DEĞERLENDİRME: [KUSURSUZ] Sistem değişmezleri tam korundu.")
            return True
        else:
            print("DEĞERLENDİRME: [BAŞARISIZ] Değişmez kurallar ihlal edildi!")
            for v in self.violations[:5]:
                print(f"  - {v}")
            return False

def execute_eval(test_name: str, iterations: int, test_fn: Callable[[], Tuple[bool, str]]) -> bool:
    report = EvalReport(test_name)
    start_time = time.time()
    
    for _ in range(iterations):
        passed, msg = test_fn()
        report.add_result(passed, msg)
        
    report.duration_seconds = time.time() - start_time
    return report.print_summary()

if __name__ == "__main__":
    print("Eval Runner modülü çalıştırıldı.")
