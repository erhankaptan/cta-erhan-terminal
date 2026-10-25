"""
CTA ERHAN TERMİNALİ — Run Synthesis
=====================================
Evidence pool'daki tüm kanıtları okur.
Her varlık için sentez üretir.
Sonuçları JSON ve SQLite'a kaydeder.
Wayne Enterprise Kılavuzu Kuralları Entegre Edilmiştir.

Kullanım:
    python -m scripts.run_synthesis
"""

import json
import sys
from pathlib import Path
from datetime import datetime, timezone
from typing import Dict, List

from core.evidence_models import Evidence
from core.evidence_repository import EvidenceRepository
from core.synthesis_engine import synthesize_all, SynthesisResult


# ============================================================
# AYARLAR
# ============================================================

PROJECT_ROOT = Path(__file__).parent.parent.resolve()
DATA_DIR = PROJECT_ROOT / "data"
# DENETCI KARARI (2026-10-25): KOK NEDEN -- build_evidence_pool.py
# "evidence_pool.db" dosyasina YAZIYOR (her calistirmada sifirdan
# yeniden uretiyor), ama bu dosya eskiden "evidence.db" OKUYORDU --
# iki ayri dosya adi. "evidence.db" .gitignore'da (*.db) oldugu icin
# GitHub Actions'daki taze checkout'ta HICBIR ZAMAN var olmuyordu ->
# asagidaki EVIDENCE_DB.exists() kontrolu HER SEFERINDE False donuyor
# ve fonksiyon sessizce return ediyordu (is basarili gorunuyor, ama
# latest.json 1 aydir hic guncellenmiyordu). Simdi dogru/taze dosyayi
# okuyor: build_evidence_pool.py'nin YAZDIGI ayni dosya.
EVIDENCE_DB = DATA_DIR / "evidence_pool.db"
SNAPSHOTS_DIR = DATA_DIR / "snapshots"


# ============================================================
# YARDIMCI
# ============================================================

def now_utc_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


# ============================================================
# ANA FONKSİYON
# ============================================================

def main():
    print("=" * 60)
    print("Run Synthesis — Wayne Enterprise Kılavuzu Etkin")
    print(f"Zaman: {now_utc_iso()}")
    print("=" * 60)

    # Evidence DB kontrol
    # DENETCI KARARI (2026-10-25): return yerine sys.exit(1) -- gercek bir
    # hata durumunda GitHub Actions adimi KIRMIZI yansin, "basarili"
    # gorunup hicbir sey yapmamis olan sessiz return bir daha olmasin.
    if not EVIDENCE_DB.exists():
        print(f"[FATAL] Evidence DB bulunamadı: {EVIDENCE_DB}")
        print("        Önce: python -m scripts.build_evidence_pool")
        sys.exit(1)

    # Kanıtları yükle
    repo = EvidenceRepository(str(EVIDENCE_DB))
    all_evidences = repo.get_all(limit=10000)
    print(f"\n[LOAD] {len(all_evidences)} kanıt yüklendi")

    if not all_evidences:
        print("[FATAL] Hiç kanıt yok")
        sys.exit(1)

    # Varlıkları bul
    asset_codes = sorted({e.asset_code for e in all_evidences})
    print(f"[INFO] {len(asset_codes)} varlık: {', '.join(asset_codes)}")

    # Her varlık için sentez
    print("\n[SYNTHESIS] (1w Net Flow z Patron Kuralı ve Diverjans Filtreleri Devrede)")
    results: Dict[str, SynthesisResult] = synthesize_all(all_evidences, asset_codes)

    # Özet
    state_counts = {}
    for code, r in results.items():
        state_counts[r.state] = state_counts.get(r.state, 0) + 1

    print(f"\n  Toplam varlık: {len(results)}")
    print(f"  Durum dağılımı:")
    for state, cnt in sorted(state_counts.items()):
        print(f"    {state}: {cnt}")

    # Sonuçları göster
    print(f"\n[DETAIL]")
    for code in asset_codes:
        r = results[code]
        print(
            f"  {code:5s} → {r.state:12s} "
            f"score={r.score:+.3f} "
            f"conf={r.confidence:3d} "
            f"kanıt={r.evidence_count}"
        )

    # JSON olarak kaydet
    SNAPSHOTS_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    output_file = SNAPSHOTS_DIR / f"synthesis_{timestamp}.json"

    snapshot = {
        "generated_at": now_utc_iso(),
        "total_assets": len(results),
        "state_counts": state_counts,
        "results": {code: r.to_dict() for code, r in results.items()},
        "protocol_rules": {
            "garbage_signal_ignored": True,
            "net_flow_z_threshold": 0.5,
            "divergence_trap_active": True,
            "session_timing_rule": "Pazartesi/Salı seans açılışları ve Stop Hunt iğnesi beklenir",
            "weekend_rule": "Cuma kapanışında pozisyonlar kapatılır"
        }
    }

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(snapshot, f, ensure_ascii=False, indent=2)

    print(f"\n[SAVE] {output_file}")

    # Son dosya olarak da kaydet (UI için)
    latest_file = SNAPSHOTS_DIR / "latest.json"
    with open(latest_file, "w", encoding="utf-8") as f:
        json.dump(snapshot, f, ensure_ascii=False, indent=2)

    print(f"[SAVE] {latest_file}")

    print("\n" + "=" * 60)
    print("OPERASYONEL HATIRLATMA:")
    print("- Gece yarısı sığ piyasada işlem yapılmaz.")
    print("- Pazartesi/Salı likidite iğneleri (Stop Hunt) beklenir.")
    print("- Tüm pozisyonlar Cuma kapanışında kapatılır.")
    print("=" * 60)
    print("TAMAMLANDI")
    print("=" * 60)


if __name__ == "__main__":
    main()
