import os
import requests
import json
import re
import calendar
import feedparser
from dotenv import load_dotenv
from google import genai
from google.genai import types
from core.signal_engine import apply_wayne_handbook_rules

# .env dosyasındaki gizli değişkenleri yükle
load_dotenv()

# API anahtarını .env dosyasından oku
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    print("HATA: GEMINI_API_KEY bulunamadi! Lutfen .env dosyasini kontrol edin.")
    exit(1)

client = genai.Client(api_key=GEMINI_API_KEY)

def download_image(image_url: str, save_path: str = "temp_table.jpg") -> str:
    """Nitter/X üzerindeki görsel linkini bilgisayara indirir."""
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    if image_url.startswith("/"):
        image_url = "https://nitter.meowing.monster" + image_url
        
    response = requests.get(image_url, headers=headers, stream=True)
    if response.status_code == 200:
        with open(save_path, 'wb') as f:
            for chunk in response.iter_content(1024):
                f.write(chunk)
        return save_path
    raise Exception(f"Resim indirilemedi, HTTP Hata Kodu: {response.status_code}")

def extract_and_process_wayne_image(image_url: str):
    """Resmi indirir, Gemini Vision ile okutur ve El Kitabı kurallarını çalıştırır."""
    local_image_path = download_image(image_url)
    
    with open(local_image_path, "rb") as f:
        image_bytes = f.read()

    prompt = """
    Sen bir finansal OCR uzmanısın. Ekstrakte edeceğin tablo Wayne Enterprise CTA akış panosudur.
    Resimdeki her bir satır için aşağıdaki alanları BİREBİR çıkar ve SADECE GEÇERLİ BİR JSON ARRAY döndür:
    [
      {
        "ticker": "CO1", "asset_name": "Brent Crude",
        "net_flow_1w": 1.1, (Okuyamazsan null ver)
        "net_flow_4w": 1.0,
        "return_1w": 4.9,
        "oi_change": 2.1,
        "oi_corr": 17
      }
    ]
    Ekstra hiçbir metin veya markdown ekleme, sadece saf JSON döndür.
    """

    print("🧠 Gemini tabloyu okuyor, lutfen bekleyin...")
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[
            types.Part.from_bytes(data=image_bytes, mime_type="image/jpeg"),
            prompt
        ]
    )

    clean_json_str = response.text.replace("```json", "").replace("```", "").strip()
    raw_data_list = json.loads(clean_json_str)

    final_results = []
    for raw_item in raw_data_list:
        processed_item = apply_wayne_handbook_rules(raw_item)
        final_results.append(processed_item)

    os.makedirs("data", exist_ok=True)
    with open("data/latest_wayne_analysis.json", "w", encoding="utf-8") as f:
        json.dump({"data": final_results}, f, ensure_ascii=False, indent=2)

    print(f"✅ Tablo başarıyla okundu ve Panoya kaydedildi!")

def x_verilerini_cek():
    kaynaklar = {
        "wayneterprises": "https://nitter.meowing.monster/wayneterprises/rss",
        "misterpuertas": "https://nitter.meowing.monster/misterpuertas/rss",
        "juanjesusmontoy": "https://nitter.meowing.monster/juanjesusmontoy/rss"
    }
    
    for isim, url in kaynaklar.items():
        try:
            req = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=15)
            feed = feedparser.parse(req.text)

            if not feed.entries:
                print(f"[{isim}] RSS beslemesinde tweet bulunamadi.")
                continue

            if isim == "misterpuertas":
                # DUZELTME (2026-10-28, Reis'in "sadece Wayne degil, o uc
                # hesaptan gelen bilgiler de skora dahil olsun" talebi):
                # onceden burada sadece "resim var mi" kontrol edilip
                # GECILIYORDU, hicbir icerik islenmiyordu. Artik gercekten
                # isleniyor (bkz. sources/x_extra_accounts.py).
                from sources.x_extra_accounts import (
                    pick_latest_entry, process_misterpuertas_entry,
                    save_misterpuertas_analysis,
                )
                entry = pick_latest_entry(feed.entries, max_scan=20)
                if not entry:
                    print(f"[{isim}] Islenecek girdi bulunamadi.")
                    continue
                data = process_misterpuertas_entry(entry)
                if data:
                    save_misterpuertas_analysis(data)
                    print(f"[{isim}] CTA Flow senaryosu islendi -> {entry.get('title','')[:70]!r}")
                else:
                    print(f"[{isim}] Tweet islenemedi (veri cikarilamadi).")
                continue

            if isim == "juanjesusmontoy":
                from sources.x_extra_accounts import (
                    pick_latest_entry, process_montoya_entry,
                    save_montoya_analysis,
                )
                entry = pick_latest_entry(feed.entries, max_scan=20)
                if not entry:
                    print(f"[{isim}] Islenecek girdi bulunamadi.")
                    continue
                data = process_montoya_entry(entry)
                if data:
                    save_montoya_analysis(data)
                    print(f"[{isim}] SPX gamma raporu islendi -> {entry.get('title','')[:70]!r}")
                else:
                    print(f"[{isim}] Tweet islenemedi (veri cikarilamadi).")
                continue

            if isim != "wayneterprises":
                # (bilinmeyen/ileride eklenebilecek baska bir hesap icin
                # eski guvenli davranis: sadece resim kontrolu.)
                entry = feed.entries[0]
                summary = entry.get("summary", "")
                resim_linkleri = re.findall(r'<img src="([^"]+)"', summary)
                print(f"[{isim}] Son tweet okundu. Icinde resim var mi? {'EVET' if resim_linkleri else 'HAYIR'}")
                continue

            # DUZELTME (2026-10-27, Reis'in "6 saat once tweet atti hala
            # gorunmuyor" raporu sonrasi): GERCEK KOK SEBEP -- nitter RSS'i
            # girdileri yayin SAATINE gore degil, kendi ic sirasina gore
            # donduruyor (entries[0] en yeni OLMAYABILIR -- dogrulandi:
            # check_wayne_rss.py ciktisinda entries[0] saat 16:59, entries[1]
            # saat 17:17, entries[2] -- asil aradigimiz "CTA signal" tablosu --
            # saat 16:22'de ama 3. sirada). Simdi SADECE entries[0]'a degil,
            # ilk 20 girdiyi tarayip BASLIGINDA "cta signal" gecen VE gorseli
            # olan tweetler arasindan EN YENI YAYIN TARIHLI olani seciyoruz --
            # sira degil, gercek saat belirleyici.
            adaylar = []
            for entry in feed.entries[:20]:
                title = (entry.get("title") or "").lower()
                if "cta signal" not in title:
                    continue
                summary = entry.get("summary", "")
                resim_linkleri = re.findall(r'<img src="([^"]+)"', summary)
                if not resim_linkleri:
                    continue
                published_struct = entry.get("published_parsed")
                # time.struct_time'i karsilastirilabilir bir sayiya (epoch
                # saniyesi) ceviriyoruz -- None gelirse (nadir) 0 kullanilir,
                # boylece farkli tiplerin karsilastirilmasi (TypeError) riski
                # ortadan kalkar.
                epoch = calendar.timegm(published_struct) if published_struct else 0
                adaylar.append((epoch, entry.get("title", ""), resim_linkleri[0]))

            if not adaylar:
                print(f"[{isim}] Son 20 girdi arasinda gorselli 'CTA signal' tablosu bulunamadi "
                      f"-- muhtemelen henuz yeni bir tablo paylasilmamis.")
                continue

            adaylar.sort(key=lambda t: t[0], reverse=True)
            secilen_epoch, secilen_baslik, secilen_resim = adaylar[0]
            print(f"📸 {isim}: en yeni 'CTA signal' tablosu bulundu -> {secilen_baslik[:70]!r}. Isleniyor...")
            extract_and_process_wayne_image(secilen_resim)

        except Exception as e:
            print(f"HATA: {isim} -> {e}")

if __name__ == "__main__":
    print("Sistem baslatiliyor, X verileri kontrol ediliyor...")
    x_verilerini_cek()