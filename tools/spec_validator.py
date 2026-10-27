# -*- coding: utf-8 -*-
"""
Spesifikasyon Doğrulayıcı (Spec Validator)
Bir şartname dosyasının (Markdown veya JSON) yapay zekâ orkestrasyonu için
gerekli asgari mimari disipline sahip olup olmadığını denetler.
"""

import sys
import os
import re
from typing import Dict, List, Tuple

# UTF-8 konsol desteği
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

REQUIRED_SECTIONS = [
    ("Problem Tanımı / Kapsam", [r"problem", r"kapsam", r"scope", r"overview"]),
    ("Sözleşmeler / Kontratlar", [r"contract", r"sözleşme", r"schema", r"api", r"interface"]),
    ("Değişmezler (Invariants)", [r"invariant", r"değişmez", r"kural", r"business rule"]),
    ("Arıza Modları (Failure Modes)", [r"failure mode", r"arıza", r"timeout", r"resilience", r"hata"]),
    ("Doğrulama / Kabul Kriterleri", [r"acceptance", r"kabul kriter", r"test", r"verification", r"eval"])
]

def validate_spec_text(content: str) -> Tuple[int, List[str], List[str]]:
    passed = []
    missing = []
    lower_content = content.lower()
    
    for section_name, patterns in REQUIRED_SECTIONS:
        found = any(re.search(pat, lower_content, re.IGNORECASE) for pat in patterns)
        if found:
            passed.append(section_name)
        else:
            missing.append(section_name)
            
    score = int((len(passed) / len(REQUIRED_SECTIONS)) * 100)
    return score, passed, missing

def validate_file(file_path: str) -> bool:
    if not os.path.exists(file_path):
        print(f"HATA: Dosya bulunamadı: {file_path}")
        return False
        
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()
        
    score, passed, missing = validate_spec_text(content)
    
    print("=" * 60)
    print(f"SPESİFİKASYON ANALİZ RAPORU: {os.path.basename(file_path)}")
    print("=" * 60)
    print(f"Olgunluk Skoru: %{score}")
    print("-" * 60)
    
    for p in passed:
        print(f"  [OK]    Mevcut   : {p}")
    for m in missing:
        print(f"  [EKSİK] Bulunamadı: {m}")
        
    print("-" * 60)
    if score >= 80:
        print("SONUÇ: [GEÇERLİ] Şartname yapay zekâ ajanlarına teslim edilmeye hazır.")
        return True
    else:
        print("SONUÇ: [YETERSİZ] Şartname eksik. Lütfen eksik bölümleri tamamlayın.")
        return False

if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "templates/spec-driven-template.md"
    success = validate_file(target)
    sys.exit(0 if success else 1)
