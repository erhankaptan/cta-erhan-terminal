"""
CTA ERHAN TERMİNALİ — Asset Mapper
====================================
Metinden futures kontrat kodunu çıkarır.

Örnek:
    "Gold is bullish"    → GC
    "WTI crude oil long" → CL
    "S&P 500 up"         → ES
    "Altın yükseliş"     → GC

Kullanım:
    from core.asset_mapper import find_assets_in_text
    codes = find_assets_in_text("Gold and Silver are up")
    # ["GC", "SI"]
"""

import re
from typing import List, Set, Optional

# Mevcut master_source/asset_catalog.py'den import
try:
    from master_source.asset_catalog import ASSET_CATALOG, get_asset
except ImportError:
    # Fallback: direkt yükleme
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).parent.parent))
    from master_source.asset_catalog import ASSET_CATALOG, get_asset


# ============================================================
# ALIAS → ASSET CODE HARİTASI (hızlı arama için)
# ============================================================

_ALIAS_TO_CODE = {}

def _build_alias_index():
    """Alias listesini tek seferde indeksler."""
    global _ALIAS_TO_CODE
    if _ALIAS_TO_CODE:
        return

    for code, asset in ASSET_CATALOG.items():
        # Kod kendisi
        _ALIAS_TO_CODE[code.lower()] = code

        # Türkçe isim
        if asset.get("name_tr"):
            _ALIAS_TO_CODE[asset["name_tr"].lower()] = code

        # İngilizce isim
        if asset.get("name_en"):
            _ALIAS_TO_CODE[asset["name_en"].lower()] = code

        # Alias'lar
        for alias in asset.get("aliases", []):
            _ALIAS_TO_CODE[alias.lower().strip()] = code


_build_alias_index()


# ============================================================
# METİN TEMİZLEME
# ============================================================

def _normalize_text(text: str) -> str:
    """Metni normalize et: küçük harf, fazla boşluk sil."""
    if not text:
        return ""
    text = text.lower()
    text = re.sub(r"\s+", " ", text)
    text = text.strip()
    return text


def _clean_word(word: str) -> str:
    """Kelimeyi temizle: noktalama işaretlerini sil."""
    return re.sub(r"[^\w\s&$%-]", "", word, flags=re.UNICODE).strip()


# ============================================================
# ANA FONKSİYON: METİNDEN ASSET ÇIKAR
# ============================================================

def find_assets_in_text(text: str, max_results: int = 10) -> List[str]:
    """
    Metinden futures kontrat kodlarını çıkarır.

    Args:
        text: Kaynak metin (tweet, RSS makalesi, vs.)
        max_results: Maksimum sonuç sayısı

    Returns:
        Benzersiz asset code listesi (örn: ["GC", "SI", "CL"])
    """
    if not text:
        return []

    normalized = _normalize_text(text)
    if not normalized:
        return []

    found: List[str] = []
    seen: Set[str] = set()

    # 1. AŞAMA: Kelime kelime tara
    words = normalized.split()

    # Tek kelime + iki kelime kombinasyonları
    for i, word in enumerate(words):
        # Temizle
        cleaned = _clean_word(word)
        if not cleaned:
            continue

        # Tek kelime kontrol
        if cleaned in _ALIAS_TO_CODE:
            code = _ALIAS_TO_CODE[cleaned]
            if code not in seen:
                seen.add(code)
                found.append(code)
                if len(found) >= max_results:
                    return found
            continue

        # İki kelime kombinasyonu (i ve i+1)
        if i + 1 < len(words):
            two_word = f"{cleaned} {_clean_word(words[i+1])}"
            if two_word in _ALIAS_TO_CODE:
                code = _ALIAS_TO_CODE[two_word]
                if code not in seen:
                    seen.add(code)
                    found.append(code)
                    if len(found) >= max_results:
                        return found

    # 2. AŞAMA: Tam metin içinde alias ara (uzun alias'lar için)
    for alias, code in _ALIAS_TO_CODE.items():
        if len(alias) < 3:
            continue  # Çok kısa alias'ları atla (gürültü)
        if code in seen:
            continue
        # Kelime sınırı ile ara
        pattern = r"\b" + re.escape(alias) + r"\b"
        if re.search(pattern, normalized):
            seen.add(code)
            found.append(code)
            if len(found) >= max_results:
                break

    return found


def find_single_asset(text: str) -> Optional[str]:
    """Metinde tek bir asset varsa onu döner, yoksa None."""
    assets = find_assets_in_text(text, max_results=2)
    if len(assets) == 1:
        return assets[0]
    return None


def get_asset_name(asset_code: str) -> str:
    """Kod → Türkçe isim."""
    asset = get_asset(asset_code)
    return asset.get("name_tr", asset_code) if asset else asset_code


def get_asset_class(asset_code: str) -> str:
    """Kod → varlık sınıfı."""
    asset = get_asset(asset_code)
    return asset.get("asset_class", "Bilinmiyor") if asset else "Bilinmiyor"


# ============================================================
# KONTROL
# ============================================================

if __name__ == "__main__":
    test_cases = [
        "Gold is bullish today",
        "WTI crude oil long, Natural Gas short",
        "S&P 500 and Nasdaq both up",
        "Altın yükseliş, Gümüş düşüş",
        "Latest CTA signal + flows for Commodities: "
        "Long all Energy but flipped short Nat Gas, "
        "CTAs flipped Long Copper & Gold to now Neutral, "
        "Short Silver. Still long all the major Ags",
        "Nasdaq 100 bull, Dow bear",
        "Brent and WTI",
        "Euro and Yen both up",
    ]

    print("=" * 60)
    print("Asset Mapper Test")
    print("=" * 60)

    for i, text in enumerate(test_cases, 1):
        codes = find_assets_in_text(text)
        names = [get_asset_name(c) for c in codes]
        print(f"\n{i}. Metin: {text[:60]}...")
        print(f"   Kodlar: {codes}")
        print(f"   İsimler: {names}")