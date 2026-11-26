#!/usr/bin/env bash
# Chay lai NGUYEN VAN probe_paths.py va probe_modes.py cua reviewer luot 5 (ops/reviews/wp1236-c-r12-ma-5-codex, nhanh ops/wp1236-bc-lease)
# tren mot checkout (probe nap packet_loop_test + packet_loop cua chinh checkout do). Khong sua gi trong checkout.
# dung: do_probe_l5.sh <goc checkout> <thu muc lam viec (moi)> <kho co ref> <ref chua probe>
set -eu
GOC="$1"; W="$2"; KHO="$3"; REF="$4"
[ ! -e "$W" ] || { echo "KHONG_DO_DUOC: $W da ton tai"; exit 2; }
mkdir -p "$W/work/tmp"
ln -s "$GOC" "$W/repo"
for p in probe_paths.py probe_modes.py; do git -C "$KHO" show "$REF:ops/reviews/wp1236-c-r12-ma-5-codex/$p" > "$W/work/$p"; done
echo "## checkout $(git -C "$GOC" rev-parse HEAD) sach=$(git -C "$GOC" status --porcelain | wc -l) · packet_loop.py sha256 $(sha256sum "$GOC/.claude/dev/packet_loop.py" | cut -d' ' -f1) · probe_paths sha256 $(sha256sum "$W/work/probe_paths.py" | cut -d' ' -f1) · probe_modes sha256 $(sha256sum "$W/work/probe_modes.py" | cut -d' ' -f1) · python $(python3 -c 'import sys; print(sys.version.split()[0])')"
for p in probe_paths.py probe_modes.py; do
  (cd "$W/work" && PYTHONDONTWRITEBYTECODE=1 python3 -B "$p" > "$p.out" 2>&1; echo "$p rc=$?")
done
python3 - "$W/work" <<'PY'
import json, sys, glob
w = sys.argv[1]
for f in sorted(glob.glob(w + "/paths-*.json")) + [w + "/modes.json"]:
    for r in json.load(open(f, encoding="utf-8")):
        ly = [d for d in (r.get("stderr") or "").split("\n") if d.strip()]
        print(f.rsplit("/", 1)[1], r["scenario"], r.get("mode") or "native", "rc=%s" % r["rc"], ly[0] if ly else "", [(o["target"], o["exists"]) for o in r.get("observed", [])] or "", sep=" | ")
PY
rm -f "$W/repo"
