# -*- coding: utf-8 -*-
"""CTA'ya mail ozelligi ekle."""
from pathlib import Path
ROOT = Path(__file__).parent

# Yedek
import shutil
for f in ["scripts/send_report.py", ".github/workflows/daily_report.yml"]:
    src = ROOT / f
    if src.exists():
        bak = src.with_suffix(src.suffix + ".bak")
        shutil.copy2(src, bak)
        print(f"[+] Yedek: {bak.name}")

# ============================================================
# 1) send_report.py - send_email fonksiyonu ekle
# ============================================================
sr_path = ROOT / "scripts" / "send_report.py"
sr = sr_path.read_text(encoding="utf-8")

if "send_email" in sr:
    print("[=] send_email zaten var")
else:
    # Import'lara smtplib ekle
    sr = sr.replace(
        "import os\nimport json\nimport requests",
        "import os\nimport json\nimport re\nimport smtplib\nimport requests\n"
        "from email.mime.text import MIMEText\n"
        "from email.mime.multipart import MIMEMultipart"
    )

    # send_email fonksiyonunu send_telegram'dan sonra ekle
    marker = "def main():"
    email_func = '''def send_email(subject, html_body):
    """SMTP ile mail gonder."""
    smtp_host = os.environ.get("EMAIL_SMTP_HOST", "smtp.gmail.com")
    smtp_port = int(os.environ.get("EMAIL_SMTP_PORT", "587"))
    user = os.environ.get("EMAIL_USER", "")
    password = os.environ.get("EMAIL_PASS", "")
    to = os.environ.get("EMAIL_TO", "")
    enabled = os.environ.get("EMAIL_ENABLED", "true").lower()

    if enabled != "true":
        print("[SKIP] EMAIL_ENABLED != true")
        return False

    if not all([user, password, to]):
        print("[FATAL] EMAIL_USER/PASS/TO eksik")
        return False

    # HTML'i temizle - basit text
    plain = re.sub(r"<[^>]+>", "", html_body)
    plain = plain.replace("&nbsp;", " ").replace("&amp;", "&")

    msg = MIMEMultipart("alternative")
    msg["From"] = user
    msg["To"] = to
    msg["Subject"] = subject
    msg.attach(MIMEText(html_body, "html", "utf-8"))
    msg.attach(MIMEText(plain, "plain", "utf-8"))

    try:
        with smtplib.SMTP(smtp_host, smtp_port, timeout=30) as s:
            s.starttls()
            s.login(user, password)
            s.send_message(msg)
        print("[OK] Email gonderildi")
        return True
    except Exception as e:
        print(f"[ERR] Email: {e}")
        return False


def main():'''

    sr = sr.replace(marker, email_func, 1)

    # main() icinde send_telegram cagrisindan sonra send_email cagir
    sr = sr.replace(
        '''    send_telegram(msg)''',
        '''    send_telegram(msg)

    # Mail gonder
    subject = f"CTA ERHAN RAPORU - {datetime.now(timezone.utc).strftime('%d %b %Y %H:%M')}"
    send_email(subject, msg)'''
    )

    sr_path.write_text(sr, encoding="utf-8")
    print("[+] send_report.py: send_email eklendi")


# ============================================================
# 2) daily_report.yml - EMAIL env ve adim ekle
# ============================================================
yml_path = ROOT / ".github" / "workflows" / "daily_report.yml"
yml = yml_path.read_text(encoding="utf-8")

if "EMAIL_USER" in yml:
    print("[=] EMAIL env zaten var")
else:
    # Mevcut Telegram adimini genislet - EMAIL env ekle
    old_step = '''      - name: Send Telegram report
        env:
          TELEGRAM_BOT_TOKEN: ${{ secrets.TELEGRAM_BOT_TOKEN }}
          TELEGRAM_CHAT_ID: ${{ secrets.TELEGRAM_CHAT_ID }}
        run: python scripts/send_report.py'''

    new_step = '''      - name: Send Telegram + Email report
        env:
          TELEGRAM_BOT_TOKEN: ${{ secrets.TELEGRAM_BOT_TOKEN }}
          TELEGRAM_CHAT_ID: ${{ secrets.TELEGRAM_CHAT_ID }}
          EMAIL_ENABLED: ${{ secrets.EMAIL_ENABLED }}
          EMAIL_SMTP_HOST: ${{ secrets.EMAIL_SMTP_HOST }}
          EMAIL_SMTP_PORT: ${{ secrets.EMAIL_SMTP_PORT }}
          EMAIL_USER: ${{ secrets.EMAIL_USER }}
          EMAIL_PASS: ${{ secrets.EMAIL_PASS }}
          EMAIL_TO: ${{ secrets.EMAIL_TO }}
        run: python scripts/send_report.py'''

    if old_step in yml:
        yml = yml.replace(old_step, new_step)
        yml_path.write_text(yml, encoding="utf-8")
        print("[+] daily_report.yml: EMAIL env eklendi")
    else:
        print("[!] daily_report.yml: eski adim bulunamadi")

print()
print("=" * 60)
print("SIMDI YAPILACAK:")
print()
print("1) GitHub'da CTA repo'ya git")
print("2) 2 dosyayi commit et:")
print("   - scripts/send_report.py")
print("   - .github/workflows/daily_report.yml")
print()
print("3) Actions -> 'CTA Terminal - Daily Report'")
print("4) 'Run workflow' -> manuel test")
print("5) Mail gelmeli (8-10 dk)")
print()
print("NOT: EMAIL_* secrets Kurumsal Makro'da var, ayni repo'da")
print("     degilse CTA repo'ya eklemen gerek.")
print("=" * 60)