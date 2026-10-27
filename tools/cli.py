# -*- coding: utf-8 -*-
"""
Orkestrasyon Araç Seti Ana CLI (Command-Line Interface)
Kullanım:
  python -m tools.cli validate-spec [dosya]
  python -m tools.cli scan-guardrails [dizin/dosya]
  python -m tools.cli run-evals
  python -m tools.cli check-all
"""

import sys
import os

# UTF-8 konsol desteği
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

from tools import spec_validator, guardrail_scanner

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(0)
        
    command = sys.argv[1].lower()
    
    if command == "validate-spec":
        target = sys.argv[2] if len(sys.argv) > 2 else "templates/spec-driven-template.md"
        ok = spec_validator.validate_file(target)
        sys.exit(0 if ok else 1)
        
    elif command == "scan-guardrails":
        target = sys.argv[2] if len(sys.argv) > 2 else "."
        if os.path.isfile(target):
            findings = guardrail_scanner.scan_file(target)
        else:
            findings = guardrail_scanner.scan_directory(target)
        ok = guardrail_scanner.print_report(findings)
        sys.exit(0 if ok else 1)
        
    elif command == "run-evals":
        print("Eval suiteleri calistiriliyor...")
        from templates import eval_harness_example
        eval_harness_example.run_eval_suite()
        sys.exit(0)
        
    elif command == "check-all":
        print("TUM SISTEM KONTROLLERI BASLATILIYOR...")
        print("\n--- 1. SPESIFIKASYON KONTROLU ---")
        ok_spec = spec_validator.validate_file("templates/spec-driven-template.md")
        
        print("\n--- 2. KOD KORKULUK KONTROLU ---")
        findings = guardrail_scanner.scan_directory(".")
        ok_guard = guardrail_scanner.print_report(findings)
        
        print("\n--- 3. DETERMINISTIK EVAL TESTI ---")
        from templates import eval_harness_example
        eval_harness_example.run_eval_suite()
        
        overall = ok_spec and ok_guard
        print("\n" + "=" * 60)
        print("GENEL SISTEM DURUMU:", "[GECIS ONAYLANDI]" if overall else "[HATALAR MEVCUT]")
        print("=" * 60)
        sys.exit(0 if overall else 1)
        
    else:
        print(f"Bilinmeyen komut: {command}")
        print(__doc__)
        sys.exit(1)

if __name__ == "__main__":
    main()
