# -*- coding: utf-8 -*-
"""
Çoklu Ajan Orkestrasyon Motoru (Simülasyon ve İcra)
"""

import sys
import time
from typing import Dict, Any, List, Tuple

# UTF-8 konsol desteği
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

class AgentWorkflowOrchestrator:
    def __init__(self, task_name: str, max_iterations: int = 3):
        self.task_name = task_name
        self.max_iterations = max_iterations
        self.history: List[Dict[str, Any]] = []

    def plan_phase(self) -> Dict[str, Any]:
        print("[1. MİMAR AJAN] Sistem şartnamesi analiz ediliyor ve iş planı çıkarılıyor...")
        plan = {
            "module": self.task_name,
            "contracts": ["input: integer (age)", "output: boolean (is_eligible)"],
            "invariants": ["age >= 0", "age < 18 -> False", "age >= 18 -> True"],
            "failure_modes": ["age < 0 -> ValueError"]
        }
        time.sleep(0.05)
        print("  -> Mimar sözleşmeyi ve değişmez kuralları belirledi.")
        return plan

    def code_phase(self, plan: Dict[str, Any], feedback: str = None) -> str:
        print("[2. KODLAYICI AJAN] Kod üretiliyor...")
        if feedback:
            print(f"  -> Geri bildirim işleniyor: {feedback}")
            # İyileştirilmiş kod
            code = """
def check_eligibility(age: int) -> bool:
    if not isinstance(age, int) or age < 0:
        raise ValueError("Yaş negatif veya geçersiz olamaz.")
    return age >= 18
"""
        else:
            # İlk taslak (kasıtlı olarak negatif sınır kontrolü eksik)
            code = """
def check_eligibility(age: int) -> bool:
    return age >= 18
"""
        time.sleep(0.05)
        return code.strip()

    def red_team_phase(self) -> List[int]:
        print("[3. RED TEAM AJANI] Saldırı vektörleri ve sınır değerler üretiliyor...")
        test_inputs = [25, 17, 18, 0, -5, -999]
        time.sleep(0.05)
        print(f"  -> {len(test_inputs)} adet uç durum test girdisi sağlandı.")
        return test_inputs

    def verify_phase(self, code_str: str, test_inputs: List[int]) -> Tuple[bool, str]:
        print("[4. DETERMINİSTİK DOĞRULAYICI] Testler icra ediliyor...")
        local_scope = {}
        try:
            exec(code_str, {}, local_scope)  # noqa: DANGEROUS_EXEC (Sandbox execution)
            fn = local_scope.get("check_eligibility")
        except Exception as e:
            return False, f"Derleme/Syntax Hatası: {e}"

        for val in test_inputs:
            try:
                res = fn(val)
                if val < 0:
                    return False, f"Değişmez ihlali! Negatif yaş ({val}) hata fırlatmalıydı ama {res} döndü!"
                if val >= 18 and not res:
                    return False, f"Doğruluk ihlali! Yaş={val} için True beklenirken False döndü."
                if val < 18 and res:
                    return False, f"Doğruluk ihlali! Yaş={val} için False beklenirken True döndü."
            except ValueError:
                if val >= 0:
                    return False, f"Hatalı istisna! Geçerli yaş ({val}) için ValueError fırlatıldı!"
            except Exception as e:
                return False, f"Beklenmeyen hata: {e}"

        return True, "Tüm testler ve değişmezler başarıyla doğrulandı."

    def run(self) -> bool:
        print("=" * 65)
        print(f"AJAN İŞ AKIŞI ORKESTRASYONU BAŞLATILDI: {self.task_name}")
        print("=" * 65)

        plan = self.plan_phase()
        test_inputs = self.red_team_phase()
        feedback = None

        for iteration in range(1, self.max_iterations + 1):
            print(f"\n--- DÖNGÜ {iteration} / {self.max_iterations} ---")
            code = self.code_phase(plan, feedback)
            passed, message = self.verify_phase(code, test_inputs)

            if passed:
                print(f"\n[SONUÇ] {message}")
                print("[ONAY] Kod deterministik doğrulama hattından geçti ve imzalandı.")
                print("-" * 65)
                print("NİHAİ DOĞRULANMIŞ KOD:\n" + code)
                print("-" * 65)
                return True
            else:
                print(f"\n[BAŞARISIZLIK] {message}")
                print("  -> Deterministik geri besleme oluşturuluyor ve Kodlayıcı Ajana aktarılıyor...")
                feedback = message

        print("\n[KRİTİK] Maksimum iterasyon aşıldı! Sistem insan mimara eskalasyon yaptı.")
        return False

if __name__ == "__main__":
    orchestrator = AgentWorkflowOrchestrator("EligibilityVerificationService")
    success = orchestrator.run()
    sys.exit(0 if success else 1)
