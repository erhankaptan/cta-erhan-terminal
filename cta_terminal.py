from pathlib import Path
import shutil
import re

APP = Path("app.py")
BACKUP = Path("app_bozuk_yedek.py")

if not APP.exists():
    raise SystemExit("app.py bulunamadı.")

# Mevcut dosyayı güvenli yedekle
shutil.copy2(APP, BACKUP)

# UTF-8 olarak oku
text = APP.read_text(encoding="utf-8")

# Mojibake onarımı.
# Örn:
# Ãœ -> Ü
# Ä° -> İ
# ÅŸ -> ş
# â—ˆ -> ◈
for _ in range(3):
    try:
        fixed = text.encode("latin1").decode("utf-8")
    except (UnicodeEncodeError, UnicodeDecodeError):
        break

    # Dönüşüm gerçekten daha iyi görünüyorsa uygula
    bad_before = sum(
        text.count(x)
        for x in (
            "Ã", "Ä", "Å", "Â", "â", "ð", " "
        )
    )
    bad_after = sum(
        fixed.count(x)
        for x in (
            "Ã", "Ä", "Å", "Â", "â", "ð", " "
        )
    )

    if bad_after < bad_before:
        text = fixed
    else:
        break

# Başlığın güvenli ve doğru olması
text = re.sub(
    r'<h1 class="cta-main-title">.*?</h1>',
    '<h1 class="cta-main-title">◈ CTA ERHAN TERMİNALİ</h1>',
    text,
    flags=re.DOTALL
)

# Eski düzeltme bloğu varsa kaldır
text = re.sub(
    r'/\* BANT VE BAŞLIK DÜZELTMESİ.*?\*/',
    '',
    text,
    flags=re.DOTALL
)

# CSS düzeltmesini yalnızca bir kez ekle
css = r'''

/* CTA ERHAN TERMINALI - BANT VE BAŞLIK DÜZELTMESİ */
[data-testid="stMetric"],
[data-testid="stExpander"],
[data-testid="stAlert"],
[data-testid="stStatusWidget"],
.stAlert,
.stMetric,
.stExpander {
    background-color: #164A68 !important;
    border: 1px solid #2B7097 !important;
    color: #FFFFFF !important;
}

[data-testid="stMetric"] *,
[data-testid="stExpander"] *,
[data-testid="stAlert"] *,
[data-testid="stStatusWidget"] *,
.stAlert *,
.stMetric *,
.stExpander * {
    color: #FFFFFF !important;
}

.stButton button {
    background-color: #164A68 !important;
    border: 1px solid #2B7097 !important;
    color: #FFFFFF !important;
}

.stButton button:hover {
    background-color: #1B5A7D !important;
    color: #FFFFFF !important;
}

section[data-testid="stSidebar"] [data-baseweb="select"] > div {
    background-color: #164A68 !important;
    color: #FFFFFF !important;
    border-color: #2B7097 !important;
}

section[data-testid="stSidebar"] [data-baseweb="select"] * {
    color: #FFFFFF !important;
}

.cta-main-title {
    display: block !important;
    width: 100% !important;
    max-width: none !important;
    overflow: visible !important;
    white-space: nowrap !important;
    line-height: 1.35 !important;
    padding: 8px 0 14px 0 !important;
    margin: 0 !important;
    color: #FFFFFF !important;
}
'''

# CSS'i mevcut </style> bloğuna ekle
if "BANT VE BAŞLIK DÜZELTMESİ" not in text:
    if "</style>" in text:
        text = text.replace("</style>", css + "\n</style>", 1)
    else:
        text = text + "\n<style>\n" + css + "\n</style>\n"

# UTF-8 olarak güvenli şekilde yaz
APP.write_text(text, encoding="utf-8", newline="\n")

print()
print("==========================================")
print(" CTA ERHAN TERMINALI DUZELTILDI")
print("==========================================")
print()
print("Yedek: app_bozuk_yedek.py")
print("Dosya: app.py")
print()
print("UTF-8: OK")
print("Turkce karakter onarimi: OK")
print("Bant renkleri: #164A68")
print("Bant yazilari: BEYAZ")
print("Baslik: ◈ CTA ERHAN TERMINALI")
print()