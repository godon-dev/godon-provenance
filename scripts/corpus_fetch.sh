#!/usr/bin/env bash
# Fetch dependency sources as the snippet-audit corpus. Cargo-only for now.
# Usage: corpus_fetch.sh <target-dir> <corpus-dir>
set -euo pipefail
TARGET="$1"
CORPUS="$2"
mkdir -p "$CORPUS"
LOCK="$TARGET/Cargo.lock"
if [ ! -f "$LOCK" ]; then echo "no Cargo.lock; corpus stays empty"; exit 0; fi
python3 - "$LOCK" "$CORPUS" <<'PY'
import pathlib, sys, tarfile, tempfile, urllib.request
lock, corpus = sys.argv[1], sys.argv[2]
pairs = []
name = None
for line in open(lock):
    s = line.strip()
    if s.startswith("name = "):
        name = s.split('"')[1]
    elif s.startswith("version = ") and name:
        pairs.append((name, s.split('"')[1]))
        name = None
ua = {"User-Agent": "godon-provenance-snippet-audit (one-shot)"}
ok = miss = 0
for n, v in pairs:
    dest = pathlib.Path(corpus) / (n + "-" + v)
    if dest.exists():
        continue
    try:
        url = "https://crates.io/api/v1/crates/" + n + "/" + v + "/download"
        req = urllib.request.Request(url, headers=ua)
        with urllib.request.urlopen(req, timeout=30) as r:
            data = r.read()
        dest.mkdir(parents=True, exist_ok=True)
        with tempfile.NamedTemporaryFile(suffix=".crate") as tf:
            tf.write(data)
            tf.flush()
            with tarfile.open(tf.name, "r:gz") as t:
                t.extractall(dest)
        ok += 1
    except Exception as e:
        miss += 1
        print("skip", n, v, type(e).__name__)
print("corpus:", ok, "fetched,", miss, "skipped")
PY
