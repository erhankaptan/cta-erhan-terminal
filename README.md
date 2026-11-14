# CTA ERHAN -- Docker (FAZ 3)

ATLAS/GÖZLEM'de kanıtlanan şablonun CTA ERHAN'a uygulanmış hali.

## Önemli: Bu terminalin mimarisi diğerlerinden FARKLI

CTA ERHAN'ın **gerçek/canlı sistemi bu bilgisayarda değil** -- GitHub
Actions'ta çalışıyor (repo: `erhankaptan/cta-erhan-terminal`, **public**),
saatlik otomatik pipeline (`fetch_nitter.py` → `analyze_tweets.py` →
`fetch_rss.py` → `translate_rss.py` → `build_evidence_pool.py` →
`run_synthesis.py` → `send_report.py` → `git commit/push data/`) oradan
yürüyor, Telegram+Email bildirimleri de oradan gidiyor. Bu bilgisayardaki
(ve şimdi Docker'daki) kopya sadece **yerel görüntüleme + ek yerel
zenginleştirme** katmanı:

- `git pull` ile GitHub'daki taze `data/*.json` state'ini çeker,
- `veri_cekici.py` ile X hesaplarından (Wayne/misterpuertas/montoya) ve
  Tickmill RSS'ten KENDİ başına da bir OCR/analiz turu yapar (yerel-only,
  GitHub'a push edilmez -- `data/evidence.db`, `data/signals.db` gitignore'da),
  Gemini Vision ile tablo görsellerini okur,
  (`core/signal_engine.py::apply_wayne_handbook_rules`),
- Streamlit (`app.py`, port 8504) ile ikisini birden gösterir.

Reis'e soruldu: gerçek sistem zaten buluttayken bu yerel/yedek kopyayı yine
de Docker'a almak mı, yoksa atlamak mı istediği -- **"yine de Docker'a al"**
kararı verildi (tutarlılık + FAZ 6'daki tam bulut geçişine hazırlık için).

## git pull YERİNE ayrı senkronizasyon -- NEDEN

Native `CTA ERHAN TERMINAL.bat`, terminal her açıldığında proje klasöründe
doğrudan `git pull --ff-only` çalıştırıyordu. Docker'da bunu AYNEN
yapmadım: `sources/evidence_pool.py` ve `sources/merkez_cot_loader.py`'de
bulduğum hardcoded Windows yollarını env-var'a bağladım (aşağıda), ama bu
patch'ler SADECE bu yerel kopyada var, GitHub'daki repo'ya hiç push
edilmedi. Eğer Docker container'ı gerçekten `git pull` yapsaydı, upstream'in
ORİJİNAL (Windows'a sabit, Linux container'da anında patlayacak) sürümüyle
kendi patch'lerimi ezerdi. Bunun yerine `docker/entrypoint.sh::
sync_data_from_github()` GitHub'ı AYRI bir klasöre (`/app/data_sync/repo`)
shallow-clone edip SADECE `data/` altındaki `*.json` dosyalarını
`/app/data/`'ye kopyalıyor -- hiçbir `.py` dosyasına dokunmuyor. Böylece
veri taze kalıyor, kod (ve patch'lerim) değişmiyor.

## Bulunan ve düzeltilen gerçek sorunlar

1. **`sources/evidence_pool.py`**: `PROJECT_ROOT` sabit
   `C:\Users\erhan\Desktop\CTA ERHAN PYTHON DOSYASI\erhan_proje\erhan`
   idi. `CTA_ERHAN_PROJECT_ROOT` ortam değişkenine bağlandı (Docker'da
   `/app`), native fallback korunarak.
2. **`sources/merkez_cot_loader.py`** -- İKİ ayrı hardcoded yol:
   - **Terminaller-arası bağımlılık:** `MERKEZ_EXPORT` sabiti aslında
     GÖZLEM/MERKEZ değil, **CTA Terminali**'nin (`C:\cta_terminal\`,
     ayrı bir terminal, henüz Docker'a geçmedi -- FAZ 3 sırasında CTA
     ERHAN'dan SONRA geliyor) ürettiği `cme_cot_raw_export.json`'u
     okuyor. `CTA_ERHAN_MERKEZ_COT_EXPORT_PATH` ortam değişkenine
     bağlandı; Docker'da host'taki `C:\cta_terminal\` klasörü
     `CTA_ERHAN_MERKEZ_COT_HOST_DIR` ile salt-okunur bind-mount
     ediliyor. **CTA Terminali Docker'a geçtiğinde bu mount'un hedefini
     güncellemek gerekecek.**
   - İkinci bir hardcoded `evidence.db` yolu da aynı dosyada, aynı
     `CTA_ERHAN_PROJECT_ROOT`'a bağlandı.
3. **`requirements.txt`'te eksik `python-dotenv`**: `veri_cekici.py`
   `from dotenv import load_dotenv` kullanıyordu ama hiç listelenmemişti
   (GÖZLEM'deki eksik-`pandas` bulgusuyla AYNI desen).

## Kullanılmayan/ölü kod -- Docker'a hiç alınmadı

- **`sources/__main__.py` (533 KB!)**: Projede HİÇBİR YERDEN
  (`python -m sources` dahil) çağrılmadığı doğrulandı -- `sources/`
  paketinin eski, tek-dosyaya-dökülmüş bir kopyası/taslağı gibi
  görünüyor. Gerçek paket zaten ayrı dosyalara (`sources/*.py`)
  bölünmüş haliyle kullanılıyor.
- **`master_source/` klasöründeki 6 dosya** (`canonical_intelligence.py`,
  `display_query_update_freshness.py`, `evidence_precedence.py`,
  `final_coverage.py`, `operational_access.py`, `source_registry.py` --
  toplam ~240 KB): Projede HİÇBİR YERDEN import edilmediği doğrulandı.
  Sadece `master_source/asset_catalog.py` gerçekten kullanılıyor
  (`core/asset_mapper.py` tarafından) -- SADECE o + `__init__.py`
  Docker'a alındı.
- Onlarca `app.py.*` yedek dosyası (`app.py.bak`, `app.py.yedek3`,
  `app.py.20260927_YEDEK` vb.), `test_*.py` dosyaları, `*.bak`/`.yedek`
  dosyaları, `__pycache__/` -- hepsi hariç tutuldu.
- `main.py`: etkileşimli bir CLI menüsü (`input()` ile 1-6 seçim) --
  arkada sürekli çalışan bir Docker servisine uygun değil, hiç
  kullanılmıyor (gerçek UI zaten `app.py`/Streamlit).

## instance_lock yine YOK

ATLAS/GÖZLEM'deki AYNI bulgu -- bilgi amaçlı not edildi.

## Kurulum

```
copy .env.example .env
REM .env'i GERCEK GEMINI_API_KEY'inle doldur, CTA_ERHAN_MERKEZ_COT_HOST_DIR'i
REM kontrol et (varsayilan C:\cta_terminal dogruysa dokunma)

docker compose up -d --build
```

veya `cta_erhan_docker_baslat.bat`'ı çalıştır.

## 3 servis

- `cta_erhan_ui` -- Streamlit dashboard (port **8504**, native'deki AYNI
  port), paylaşılan volume'den okuyor, kendisi senkronizasyon yapmıyor.
- `cta_erhan_sync` -- 30dk kadansla `sync_data_from_github()` +
  `veri_cekici.py` (native'de "her terminal açılışında bir kez" idi,
  Docker sürekli çalıştığı için periyodik yapıldı -- nitter mirror'ını
  aşırı yormamak için GitHub Actions'ın kendi saatlik kadansına yakın
  seçildi).
- `cta_erhan_cot_weekly` -- haftalık COT çekimi (26 ürün), native
  `CTA_COT_WEEKLY_GIZLI.vbs`'nin (Windows Task Scheduler) tetiklediği
  AYNI `scripts/run_weekly_cot.py`. Native loglardan (`logs/cot_weekly.log`,
  10 haftalık kayıt) tetikleme saati **her Cuma 23:30** olarak
  doğrulandı -- Docker'da `TZ=Europe/Paris` (DST-farkında, native Windows
  Task Scheduler'la AYNI) ile birebir aynı.

Hepsi AYNI `cta_erhan_data`/`cta_erhan_data_store`/`cta_erhan_logs` named
volume'larını paylaşıyor.

## Doğrulama

Native'i durdurduktan sonra Docker'ı başlatıp:
- UI'nin `http://localhost:8504`'te açıldığını,
- `cta_erhan_sync` loglarında GitHub clone + `veri_cekici.py` turunun
  başarıyla tamamlandığını,
- `cta_erhan_cot_weekly` loglarında "Sonraki calisma: ..." satırının
  bir sonraki Cuma 23:30 +02/+01'i (DST'ye göre) doğru gösterdiğini,

kontrol et.
