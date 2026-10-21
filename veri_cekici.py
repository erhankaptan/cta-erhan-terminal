import os
import requests
import json
import re
import feedparser
from google import genai
from google.genai import types
from core.signal_engine import apply_wayne_handbook_rules

# ⚠️ BURAYA KENDİ GEMINI API ANAHTARINI YAPIŞTIR
GEMINI_API_KEY = "SENIN_GEMINI_API_KEYIN"
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
            
            if feed.entries:
                entry = feed.entries[0]
                summary = entry.get("summary", "")
                resim_linkleri = re.findall(r'<img src="([^"]+)"', summary)
                
                print(f"[{isim}] Son tweet okundu. Icinde resim var mi? {'EVET' if resim_linkleri else 'HAYIR'}")
                
                if resim_linkleri and isim == "wayneterprises":
                    print(f"📸 {isim} yeni bir tablo paylasti! Isleniyor...")
                    extract_and_process_wayne_image(resim_linkleri[0])
            else:
                print(f"[{isim}] RSS beslemesinde tweet bulunamadi.")
                    
        except Exception as e:
            print(f"HATA: {isim} -> {e}")

if __name__ == "__main__":
    print("Sistem baslatiliyor, X verileri kontrol ediliyor...")
    x_verilerini_cek()