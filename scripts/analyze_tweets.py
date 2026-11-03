"""
CTA ERHAN TERMİNALİ — Gemini Analiz v9.5 (Batch API Entegrasyonlu)
=============================================================================
Yeni SDK: google-genai (Batch API ile %50 Maliyet Tasarrufu)
Wayne Enterprise CTA Panosu Değerlendirme Entegrasyonlu
"""

import os
import json
import time
import re
import base64
from datetime import datetime, timezone
from pathlib import Path

import requests
from google import genai
from google.genai import types

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
MODEL_NAME = "gemini-2.5-flash"  # Veya projede kullandığın model

DATA_DIR = Path("data")
TWEETS_DIR = DATA_DIR / "tweets"
ANALYSIS_DIR = DATA_DIR / "analysis"
STATE_DIR = DATA_DIR / "state"  # Veya mevcut state dosyası konumu
STATE_FILE = DATA_DIR / "analysis_state.json"

PRIORITY_ACCOUNTS = ["wayneterprises", "JuanJesusMontoy", "misterpuertas"]
PRIORITY_LOWER = [a.lower() for a in PRIORITY_ACCOUNTS]


def is_priority_tweet(tweet: dict) -> bool:
    username = (tweet.get("username") or "").lower()
    return username in PRIORITY_LOWER


def ensure_dirs():
    ANALYSIS_DIR.mkdir(parents=True, exist_ok=True)


def load_state() -> dict:
    if STATE_FILE.exists():
        try:
            with open(STATE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}


def save_state(state: dict):
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)


def get_all_tweets_files():
    return sorted(TWEETS_DIR.glob("tweets_*.json"))


def load_tweets(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


def download_image_as_base64(url: str):
    """Görseli indirir ve Batch API için Base64 formatına çevirir."""
    try:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        response = requests.get(url, timeout=4, headers=headers, allow_redirects=True)
        if response.status_code == 200:
            ct = response.headers.get("Content-Type", "").lower()
            if "image" in ct and "html" not in ct:
                encoded = base64.b64encode(response.content).decode("utf-8")
                return encoded, ct
    except Exception as e:
        print(f"    [IMG] Atlandı (Timeout/Hata): {e}")
    return None, None


PROMPT = """Sen kıdemli bir CTA (Commodity Trading Advisor) ve vadeli işlemler analistisin.

GÖREV: Aşağıdaki tweet metnini ve varsa görsellerdeki (özellikle Wayne Enterprise vb. CTA panolarındaki) tabloları analiz et. Tweet'te ve görsellerde geçen HER finansal varlığı ÇIKAR.

====================================================================
WAYNE ENTERPRISE CTA PANOSU DEĞERLENDİRME VE AKIŞ KURALLARI (KESİN UYULACAK):
1. ÇÖP SİNYAL YASAĞI: Tabloların en sağında yer alan "CTA Signal" (LONG/SHORT/NEUTRAL) sütunu tamamen geçmiş ralli/düşüşlerden kalan gecikmeli (lagging) bir etikettir. Bu sütundaki renk ve yazıları tamamen YOK SAYACAK ve analizlerine kesinlikle dahil etmeyeceksin.
2. PATRON SÜTUN (1w Net Flow z): Haftalık kurumsal para yönünü belirleyen ana göstergedir.
   - Değer +0.5 üzerindeyse yön kesinlikle LONG.
   - Değer -0.5 altındaysa yön kesinlikle SHORT.
   - Değer -0.5 ile +0.5 arasındaysa (nötr/zayıf akış) kurumsallar kararsızdır; acele edilmez, likidite temizliği (iğne) beklenir.
3. DİVERJANS / UYUMSUZLUK AVCISI (1w Return vs 1w Net Flow):
   - Fiyat çakılırken (1w Return < 0) para akışı yeşilse (1w Net Flow z > 0), bu bir "Dip Tuzağı / Kurumsal Mal Toplama" (Muazzam Long Fırsatı) olarak etiketlenmelidir.
   - Fiyat yükselirken para akışı kırmızıysa, "Tepe Tuzağı / Kurumsal Satış" olarak etiketlenmelidir.
4. LİKİDİTE VE AÇIK POZİSYON (OI Change & OI Correlation):
   - Fiyat düşerken Açık Pozisyon azalıyorsa (OI Change < 0), bu bir "Stop Patlatma / Long Liquidation" hareketidir.
   - Spot Korelasyonu (OI Corr) %15 altındaysa piyasada manipülasyon/kararsızlık yüksektir; stop mesafesinin geniş tutulması not düşülmelidir.
5. ZAMANLAMA PROTOKOLÜ:
   - Veri gece yarısı veya seans kapanışında yayınlansa bile hemen işleme girilmez; Londra/New York seans açılışları ve silkeleme iğnesi (Stop Hunt) beklenmelidir.
====================================================================

ÇOK ÖNEMLİ — AGRESİF VE DOĞRU VARLIK ÇIKARIMI:
- Tweet kısa olsa bile, ima etse bile, dolaylı konuşsa bile varlık çıkar.
- Hashtag (#gold, #SPX, #BTC) ve kısaltma ($ES, $GC, $SPX) varsa mutlaka yakala.
- Tweet'te şirket adı geçiyorsa (Nvidia, Tesla, Apple) → hisse sembolü olarak al (NVDA, TSLA, AAPL).
- Varlık listesinden uygun olanları kesinlikle eşleştir.

Tweet metni:
{text}

Kullanıcı: @{username}

ÇIKTI (SADECE JSON):

{{
  "varliklar": [
    {{
      "sembol": "GC",
      "isim": "Gold",
      "yon": "YUKARI",
      "gerekce": "kısa Türkçe gerekçe (1w Net Flow ve Diverjans odaklı, max 150 karakter)",
      "skor": 0.7
    }}
  ],
  "genel_yon": "YUKARI",
  "ozet": "Wayne Enterprise kurallarına dayalı Türkçe 1-2 cümle özet",
  "confidence": 0.8
}}

KURALLAR:
- yon: YUKARI, AŞAĞI, NÖTR
- gerekce: Türkçe, max 150 karakter
- skor: 0.0 - 1.0
- varliklar boş olabilir → []

Şimdi analiz et:"""


def parse_gemini_json(raw: str) -> dict:
    """Gemini çıktısındaki JSON'ı güvenli şekilde temizler ve parse eder."""
    if not raw:
        return {"varliklar": [], "ozet": "Boş yanıt"}
    
    raw = raw.strip()
    if raw.startswith("```"):
        parts = raw.split("```")
        if len(parts) >= 2:
            raw = parts[1]
            if raw.startswith("json"):
                raw = raw[4:]
    raw = raw.strip()

    if not raw.startswith("{"):
        m = re.search(r'\{.*\}', raw, re.DOTALL)
        if m:
            raw = m.group(0)

    try:
        return json.loads(raw)
    except Exception:
        pass

    try:
        cleaned = re.sub(r',\s*([}\]])', r'\1', raw)
        return json.loads(cleaned)
    except Exception:
        return {"varliklar": [], "ozet": "JSON parse edilemedi", "raw": raw[:200]}


def main():
    print("=" * 60)
    print("CTA Erhan Terminali — Gemini Batch Analiz v9.5")
    print(f"Zaman: {datetime.now(timezone.utc).isoformat()}")
    print("=" * 60)

    if not GEMINI_API_KEY:
        print("[FATAL] GEMINI_API_KEY yok")
        return

    client = genai.Client(api_key=GEMINI_API_KEY)
    ensure_dirs()

    files = get_all_tweets_files()
    if not files:
        print("[FATAL] Tweet dosyası yok")
        return

    all_tweets = []
    for fp in files:
        try:
            tweets = load_tweets(fp)
            all_tweets.extend(tweets)
        except Exception as e:
            print(f"  [ERR] {fp.name}: {e}")

    priority_tweets = [t for t in all_tweets if is_priority_tweet(t)]

    seen_ids = set()
    unique_tweets = []
    for t in priority_tweets:
        tid = str(t.get("id", ""))
        if tid and tid not in seen_ids:
            seen_ids.add(tid)
            unique_tweets.append(t)

    state = load_state()
    analyzed_ids = set(state.get("analyzed_ids", []))

    new_tweets = [t for t in unique_tweets if str(t.get("id")) not in analyzed_ids]
    
    # Güvenlik sınırı (Maksimum son 15 yeni tweet)
    if len(new_tweets) > 15:
        print(f"[INFO] Toplam {len(new_tweets)} yeni tweet var, en son 15 tanesi işlenecek.")
        new_tweets = new_tweets[-15:]

    print(f"[INFO] İşlenecek taze tweet sayısı (Batch kuyruğuna eklenecek): {len(new_tweets)}")

    if not new_tweets:
        print("[DONE] İşlenecek yeni tweet yok")
        return

    # 1. BATCH İSTEKLERİNİ JSONL FORMATINDA HAZIRLA
    jsonl_lines = []
    tweet_map = {} # custom_id eşleştirmesi için

    for tweet in new_tweets:
        tweet_id = str(tweet.get("id", ""))
        username = tweet.get("username", "")
        text = tweet.get("text", "")
        images = tweet.get("images", [])

        tweet_map[tweet_id] = tweet

        prompt = PROMPT.format(text=(text or "")[:1500], username=username)
        parts = [{"text": prompt}]

        # Görselleri ekle (varsa)
        for img_url in images[:2]:
            img_base64, mime_type = download_image_as_base64(img_url)
            if img_base64:
                parts.append({
                    "inline_data": {
                        "mime_type": mime_type or "image/jpeg",
                        "data": img_base64
                    }
                })

        # Batch API İstek Yapısı
        request_obj = {
            "custom_id": tweet_id,
            "request": {
                "contents": [
                    {
                        "role": "user",
                        "parts": parts
                    }
                ],
                "generation_config": {
                    "temperature": 0.2,
                    "max_output_tokens": 2048
                }
            }
        }
        jsonl_lines.append(json.dumps(request_obj))

    # JSONL dosyasını yerel olarak yaz
    batch_file_path = "batch_requests.jsonl"
    with open(batch_file_path, "w", encoding="utf-8") as f:
        f.write("\n".join(jsonl_lines) + "\n")

    try:
        # 2. DOSYAYI GEMINI'YE YÜKLE (%50 İndirim Başlangıcı)
        print(">>> Batch istek dosyası Google'a yükleniyor...")
        uploaded_file = client.files.upload(
            file=batch_file_path,
            config={'mime_type': 'jsonl'}
        )

        # 3. BATCH JOB BAŞLAT
        batch_job = client.batches.create(
            model=MODEL_NAME,
            src=uploaded_file.file_name,
            config={'display_name': 'cta_tweets_batch_job'}
        )
        print(f">>> Batch Job başarıyla başlatıldı! Job ID: {batch_job.name}")

        # 4. TAMAMLANMASINI BEKLE (3 saatlik döngü için güvenli döngü)
        print(">>> Batch işleme alındı, sonuçlar bekleniyor...")
        while True:
            job_status = client.batches.get(name=batch_job.name)
            state_name = job_status.state.name
            print(f"    Durum: {state_name}")

            if state_name in ['JOB_STATE_SUCCEEDED', 'JOB_STATE_FAILED', 'JOB_STATE_CANCELLED']:
                break
            time.sleep(20)  # 20 saniyede bir kontrol et

        if job_status.state.name != 'JOB_STATE_SUCCEEDED':
            print(f"[FATAL] Batch Job başarısız oldu veya iptal edildi: {job_status.state.name}")
            return

        # 5. SONUÇLARI İNDİR VE İŞLE
        print(">>> Batch sonuçları indiriliyor...")
        result_bytes = client.files.download(file=job_status.dest.file.name)
        result_lines = result_bytes.decode('utf-8').splitlines()

        results = []
        success = 0
        failed = 0
        total_assets = 0

        for line in result_lines:
            if not line.strip():
                continue
            res_json = json.loads(line)
            custom_id = res_json.get("custom_id")
            
            # Yanıt metnini güvenli al
            response_candidate = res_json.get("response", {}).get("candidates", [{}])[0]
            raw_text = ""
            for part in response_candidate.get("content", {}).get("parts", []):
                if "text" in part:
                    raw_text += part["text"]

            tweet = tweet_map.get(custom_id, {})
            analysis = parse_gemini_json(raw_text)

            if analysis and "varliklar" in analysis:
                varliklar = analysis.get("varliklar", [])
                result = {
                    "tweet_id": custom_id,
                    "username": tweet.get("username", ""),
                    "text": tweet.get("text", ""),
                    "images": tweet.get("images", []),
                    "analyzed_at": datetime.now(timezone.utc).isoformat(),
                    "varliklar": varliklar,
                    "genel_yon": analysis.get("genel_yon", "NÖTR"),
                    "ozet": analysis.get("ozet", ""),
                    "confidence": analysis.get("confidence", 0.0),
                }
                results.append(result)
                analyzed_ids.add(custom_id)
                success += 1
                total_assets += len(varliklar)
            else:
                failed += 1

        # Sonuçları dosyaya kaydet
        if results:
            timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
            output_file = ANALYSIS_DIR / f"analysis_{timestamp}.json"
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(results, f, ensure_ascii=False, indent=2)
            print(f"\n[SAVE] Sonuçlar kaydedildi: {output_file.name}")

        # State güncelle
        state["analyzed_ids"] = list(analyzed_ids)
        state["last_run"] = datetime.now(timezone.utc).isoformat()
        save_state(state)

        print(f"\n{'=' * 60}")
        print(f"Batch İşlem Tamamlandı — Başarılı: {success}, Başarısız: {failed}")
        print(f"Toplam çıkarılan varlık: {total_assets}")
        print(f"{'=' * 60}")

    except Exception as e:
        print(f"[HATA] Batch çalıştırma sırasında hata oluştu: {e}")


if __name__ == "__main__":
    main()
