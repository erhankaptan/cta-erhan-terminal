#!/bin/bash
set -e

# ============================================================
# run_at_time: hedef saate (ve istege bagli haftanin gunune) kadar
# bekler, calistirir, sonra bir sonrakine kadar tekrar bekler.
# ATLAS/GOZLEM'deki AYNI desen -- native Windows Task
# Scheduler + gizli .vbs dosyalarinin yerini aliyor.
#   $1: HH:MM hedef saat (container TZ'sinde, bkz. Dockerfile ENV TZ)
#   $2: (opsiyonel) hedef haftanin gunu, GNU `date -d` formatinda
#       (orn. "friday"). Bos birakilirsa her gun calisir.
#   $3: calistirilacak komut (bash -c ile)
# ============================================================
run_at_time() {
    local target_time="$1"
    local target_weekday="$2"
    local cmd="$3"

    while true; do
        now_epoch=$(date +%s)
        today_target_epoch=$(date -d "today $target_time" +%s)

        if [ -n "$target_weekday" ]; then
            today_weekday=$(date +%A | tr '[:upper:]' '[:lower:]')
            target_weekday_lower=$(echo "$target_weekday" | tr '[:upper:]' '[:lower:]')
            if [ "$today_weekday" = "$target_weekday_lower" ] && [ "$today_target_epoch" -gt "$now_epoch" ]; then
                next_epoch=$today_target_epoch
            else
                next_epoch=$(date -d "next $target_weekday $target_time" +%s)
            fi
        else
            if [ "$today_target_epoch" -gt "$now_epoch" ]; then
                next_epoch=$today_target_epoch
            else
                next_epoch=$(date -d "tomorrow $target_time" +%s)
            fi
        fi

        sleep_seconds=$((next_epoch - now_epoch))
        next_human=$(date -d "@$next_epoch" "+%Y-%m-%d %H:%M:%S %z")
        echo "[CTA_ERHAN][ENTRYPOINT] Sonraki calisma: $next_human (${sleep_seconds}s sonra)"
        sleep "$sleep_seconds"

        echo "[CTA_ERHAN][ENTRYPOINT] Calistiriliyor: $cmd"
        bash -c "$cmd" || echo "[CTA_ERHAN][ENTRYPOINT] HATA (devam ediliyor): $cmd basarisiz oldu"
    done
}

# ============================================================
# sync_data_from_github: GitHub'daki public repo'yu (GH Actions'in
# saatlik pipeline'i burayi besliyor) AYRI bir klasore shallow-clone
# edip SADECE data/ altindaki *.json dosyalarini /app/data/'ye kopyalar.
# KASITLI OLARAK /app icindeki .py dosyalarina DOKUNMUYOR -- native
# "git pull" bunu yapardi ama Docker'da bu, PROJECT_ROOT/MERKEZ_EXPORT
# icin uyguladigim env-var patch'lerini upstream'in orijinal (Windows'a
# sabit, Linux'ta patlayacak) haliyle ezerdi. Boylece sadece veri taze
# kalir, kod degismez.
# ============================================================
sync_data_from_github() {
    local repo_url="https://github.com/erhankaptan/cta-erhan-terminal.git"
    local sync_dir="/app/data_sync/repo"

    rm -rf "$sync_dir"
    if git clone --depth 1 -q "$repo_url" "$sync_dir" 2>/app/data_sync/last_clone_error.log; then
        if [ -d "$sync_dir/data" ]; then
            # DUZELTME: ilk surum sadece data/'nin EN UST seviyesindeki
            # *.json dosyalarini kopyaliyordu (-maxdepth 1). Ama app.py
            # asil verileri data/rss/, data/tweets/, data/analysis/,
            # data/snapshots/ ALT klasorlerinden okuyor (RSS_DIR,
            # TWEETS_DIR, ANALYSIS_DIR, SNAPSHOTS_DIR) -- bu yuzden
            # Tickmill Yorumlari ve CTA Radari hep bos goruntleniyordu.
            # `cp --parents` ile klasor yapisini KORUYARAK, TUM alt
            # klasorlerdeki *.json dosyalarini kopyaliyoruz (evidence.db/
            # signals.db zaten GitHub'da gitignore'lu, hic gelmiyor).
            (cd "$sync_dir/data" && find . -name "*.json" -exec cp --parents -f {} /app/data/ \;)
            echo "[CTA_ERHAN][SYNC] GitHub'dan taze data/**/*.json (alt klasorler dahil) senkronize edildi."
        fi
    else
        echo "[CTA_ERHAN][SYNC] UYARI: GitHub clone basarisiz (internet yok olabilir), eldeki veriyle devam."
    fi
}

MODE="${1:-ui}"

case "$MODE" in
    ui)
        echo "[CTA_ERHAN][ENTRYPOINT] Streamlit UI baslatiliyor (port ${CTA_ERHAN_UI_PORT:-8504})."
        exec streamlit run app.py \
            --server.port "${CTA_ERHAN_UI_PORT:-8504}" \
            --server.enableCORS false \
            --server.enableXsrfProtection false
        ;;

    sync)
        echo "[CTA_ERHAN][ENTRYPOINT] Senkronizasyon dongusu baslatiliyor (${CTA_ERHAN_SYNC_INTERVAL_MIN:-30}dk kadans)."
        while true; do
            sync_data_from_github
            echo "[CTA_ERHAN][SYNC] veri_cekici.py calistiriliyor (X/Tickmill OCR tarama)..."
            python veri_cekici.py || echo "[CTA_ERHAN][SYNC] HATA (devam ediliyor): veri_cekici.py basarisiz oldu"
            sleep "$(( ${CTA_ERHAN_SYNC_INTERVAL_MIN:-30} * 60 ))"
        done
        ;;

    cot_weekly)
        echo "[CTA_ERHAN][ENTRYPOINT] Haftalik COT zamanlayicisi aktif (hedef=${CTA_ERHAN_COT_WEEKLY_TIME:-23:30} ${CTA_ERHAN_COT_WEEKLY_DAY:-friday}, TZ=$TZ -- native Windows Task Scheduler'daki ile AYNI)."
        run_at_time "${CTA_ERHAN_COT_WEEKLY_TIME:-23:30}" "${CTA_ERHAN_COT_WEEKLY_DAY:-friday}" "python scripts/run_weekly_cot.py"
        ;;

    *)
        echo "[CTA_ERHAN][ENTRYPOINT] Bilinmeyen mod: $MODE (ui|sync|cot_weekly bekleniyor)"
        exit 1
        ;;
esac
