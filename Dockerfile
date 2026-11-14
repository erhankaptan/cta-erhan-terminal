FROM python:3.12-slim

WORKDIR /app

# git: GitHub'daki (erhankaptan/cta-erhan-terminal, public) taze data/*.json
# state'ini periyodik senkronize etmek icin (bkz. docker/entrypoint.sh --
# KOD DOSYALARINA DOKUNMUYOR, sadece data/ altindaki JSON'lari).
# tzdata: haftalik COT zamanlayicisi native Windows Task Scheduler'daki
# AYNI Europe/Paris (DST-farkinda) saatini kullanabilsin diye.
RUN apt-get update && apt-get install -y --no-install-recommends \
        git \
        tzdata \
    && rm -rf /var/lib/apt/lists/*

ENV TZ=Europe/Paris

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chmod +x docker/entrypoint.sh

# Non-root kullanici + data klasorune onceden sahiplik (named volume
# root:root olarak mount olup container'in yazmasini engelleyen bilinen
# Docker davranisi -- MERKEZ/ATLAS/GOZLEM'de de karsilasilan ayni bug,
# burada USER'dan ONCE mkdir+chown ile onden onleniyor).
RUN groupadd -g 1000 ctaerhan && \
    useradd -u 1000 -g ctaerhan -m -s /bin/bash ctaerhan && \
    mkdir -p /app/data /app/data_store /app/logs /app/data_sync && \
    chown -R ctaerhan:ctaerhan /app

USER ctaerhan

ENTRYPOINT ["/app/docker/entrypoint.sh"]
