# scripts/run_weekly_cot.py
"""
Haftalık COT çekimi script'i.
Windows Task Scheduler tarafından tetiklenir.
"""
from __future__ import annotations

import sys
import logging
from datetime import datetime, timezone
from pathlib import Path


# ============================================================
# Proje kökünü sys.path'e ekle
# ============================================================
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


# ============================================================
# Log ayarları
# ============================================================
LOG_DIR = PROJECT_ROOT / "logs"
LOG_DIR.mkdir(exist_ok=True)
LOG_FILE = LOG_DIR / "cot_weekly.log"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
        logging.StreamHandler(sys.stdout),
    ],
)
logger = logging.getLogger("cot_weekly")


from sources.ingestion import run_ingestion_pipelineForProduct


URUNLER = [
    "ES", "MES", "NQ", "MNQ", "RTY", "YM",
    "CL", "MCL", "NG",
    "GC", "MGC", "SI", "HG", "PL",
    "6E", "6J", "6B", "6A", "6C", "6S",
    "ZC", "ZS", "ZW", "ZL", "ZM",
]


def main() -> int:
    baslangic = datetime.now(timezone.utc)
    logger.info("=" * 60)
    logger.info("HAFTALIK COT CEKIMI BASLADI")
    logger.info(f"Baslangic : {baslangic.isoformat()}")
    logger.info(f"Urun sayisi: {len(URUNLER)}")
    logger.info("-" * 60)

    toplam_added = 0
    toplam_hata = 0

    for i, urun in enumerate(URUNLER, start=1):
        urun_baslangic = datetime.now(timezone.utc)
        try:
            logger.info(f"[{i}/{len(URUNLER)}] {urun} basliyor...")
            sonuc = run_ingestion_pipelineForProduct(urun)
            added = sonuc.get("added", 0)
            total = sonuc.get("total_in_pool", 0)
            skipped = sonuc.get("skipped_duplicates", 0)
            unavailable = sonuc.get("unavailable_sources", 0)

            toplam_added += added
            sure = (datetime.now(timezone.utc) - urun_baslangic).total_seconds()

            logger.info(
                f"[{i}/{len(URUNLER)}] {urun} TAMAM | "
                f"added: {added} | skipped: {skipped} | "
                f"total: {total} | unavailable: {unavailable} | "
                f"sure: {sure:.2f}s"
            )
        except Exception as e:
            toplam_hata += 1
            logger.error(f"[{i}/{len(URUNLER)}] {urun} HATA: {type(e).__name__}: {e}")

    bitis = datetime.now(timezone.utc)
    sure = (bitis - baslangic).total_seconds()

    logger.info("-" * 60)
    logger.info(f"Bitis     : {bitis.isoformat()}")
    logger.info(f"Sure      : {sure:.2f} saniye")
    logger.info(f"Toplam eklenen: {toplam_added}")
    logger.info(f"Hata sayisi   : {toplam_hata}")
    logger.info("=" * 60)
    logger.info("HAFTALIK COT CEKIMI TAMAMLANDI")
    logger.info("=" * 60)

    return 0 if toplam_hata == 0 else 1


if __name__ == "__main__":
    sys.exit(main())