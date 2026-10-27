# -*- coding: utf-8 -*-
"""
Deterministik Korkuluk ve Anti-Pattern Tarayıcı (Guardrail Scanner)
Yapay zekâ modellerinin ürettiği koddaki tipik amelelik ve güvenlik zafiyeti
kalıntılarını kaynak kod üzerinde statik analizle tespit eder.
"""

import sys
import os
import re
from typing import List, Dict, Any

# UTF-8 konsol desteği
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

PATTERNS = [
    {
        "id": "HARDCODED_SECRET",
        "desc": "Kod içinde hardcoded API key / gizli anahtar bulundu",
        "regex": r"""(?i)(api[_-]?key|secret|token|password|passwd)\s*[:=]\s*["'][a-zA-Z0-9_\-\.]{16,}["']""",
        "severity": "CRITICAL"
    },
    {
        "id": "UNFINISHED_TODO",
        "desc": "Model kodu eksik bırakmış (TODO / FIXME / placeholder)",
        "regex": r"""(?i)(#|//)\s*(todo|fixme|burayi doldur|implement here)""",
        "severity": "HIGH"
    },
    {
        "id": "BLIND_EXCEPTION",
        "desc": "Kör hata yakalama (Hataları yutan ve sessizce gizleyen yapı)",
        "regex": r"""(?i)(except\s*:\s*pass|except\s+Exception\s*:\s*pass|catch\s*\([^\)]*\)\s*\{\s*\})""",
        "severity": "HIGH"
    },
    {
        "id": "DANGEROUS_EXEC",
        "desc": "Tehlikeli dinamik kod çalıştırma fonksiyonu kullanımı",
        "regex": r"""\b(eval|exec)\s*\(""",
        "severity": "CRITICAL"
    },
    {
        "id": "MISSING_TIMEOUT",
        "desc": "HTTP çağrısında timeout parametresi eksik olabilir",
        "regex": r"""requests\.(get|post|put|delete)\s*\((?!.*timeout\s*=)[^\)]*\)""",
        "severity": "MEDIUM"
    }
]

def scan_file(file_path: str) -> List[Dict[str, Any]]:
    findings = []
    if not os.path.exists(file_path):
        return findings
        
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            lines = f.readlines()
    except Exception:
        return findings
        
    for line_num, line in enumerate(lines, 1):
        for rule in PATTERNS:
            if re.search(rule["regex"], line):
                findings.append({
                    "file": file_path,
                    "line": line_num,
                    "id": rule["id"],
                    "desc": rule["desc"],
                    "severity": rule["severity"],
                    "snippet": line.strip()
                })
    return findings

def scan_directory(directory: str) -> List[Dict[str, Any]]:
    all_findings = []
    valid_exts = {".py", ".js", ".ts", ".jsx", ".tsx", ".go"}
    
    for root, _, files in os.walk(directory):
        if any(skip in root for skip in ["node_modules", ".git", "__pycache__", ".venv", "venv"]):
            continue
        for f in files:
            ext = os.path.splitext(f)[1]
            if ext in valid_exts:
                path = os.path.join(root, f)
                all_findings.extend(scan_file(path))
    return all_findings

def print_report(findings: List[Dict[str, Any]]) -> bool:
    print("=" * 70)
    print("KOD KORKULUK VE GÜVENLİK TARAMA RAPORU (GUARDRAIL SCANNER)")
    print("=" * 70)
    
    if not findings:
        print("[TEMİZ] Tebrikler! Hiçbir anti-pattern veya kritik zafiyet bulunamadı.")
        return True
        
    print(f"Toplam {len(findings)} adet şüpheli örüntü tespit edildi:\n")
    critical_count = 0
    
    for f in findings:
        sev = f["severity"]
        if sev == "CRITICAL":
            critical_count += 1
        print(f"[{sev}] {f['file']}:{f['line']}")
        print(f"  Kural   : {f['id']} - {f['desc']}")
        print(f"  Kod     : {f['snippet']}")
        print("-" * 70)
        
    if critical_count > 0:
        print(f"SONUÇ: [REDDEDİLDİ] {critical_count} adet KRİTİK zafiyet var. PR merge edilemez.")
        return False
    else:
        print("SONUÇ: [UYARI] Bazı iyileştirme alanları var, lütfen gözden geçirin.")
        return True

if __name__ == "__main__":
    target_path = sys.argv[1] if len(sys.argv) > 1 else "."
    if os.path.isfile(target_path):
        results = scan_file(target_path)
    else:
        results = scan_directory(target_path)
    is_clean = print_report(results)
    sys.exit(0 if is_clean else 1)
