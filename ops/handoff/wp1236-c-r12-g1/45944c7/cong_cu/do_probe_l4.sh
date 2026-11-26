#!/usr/bin/env bash
# Chay lai NGUYEN VAN probe_models.py cua reviewer luot 4 (ops/reviews/wp1236-c-r12-ma-4-codex, nhanh ops/wp1236-bc-lease) tren mot checkout.
# "previous" cua probe = packet_loop.py tai d5a7d85 (ung vien luot 4), "head" = packet_loop.py cua checkout. Khong sua gi trong checkout.
# dung: do_probe_l4.sh <goc checkout> <thu muc lam viec (moi)> <ref chua probe>
set -eu
GOC="$1"; W="$2"; REF="$3"
[ ! -e "$W" ] || { echo "KHONG_DO_DUOC: $W da ton tai"; exit 2; }
mkdir -p "$W/work/previous" "$W/work/tmp"
ln -s "$GOC" "$W/repo"
git -C "$GOC" show "$REF:ops/reviews/wp1236-c-r12-ma-4-codex/probe_models.py" > "$W/work/probe_models.py"
git -C "$GOC" show d5a7d8510af03e0d08545f677ad5de687e0264f4:.claude/dev/packet_loop.py > "$W/work/previous/packet_loop.py"
echo "probe sha256 $(sha256sum "$W/work/probe_models.py" | cut -d' ' -f1) · previous sha256 $(sha256sum "$W/work/previous/packet_loop.py" | cut -d' ' -f1) · head $(git -C "$GOC" rev-parse HEAD) sach=$(git -C "$GOC" status --porcelain | wc -l) · packet_loop.py sha256 $(sha256sum "$GOC/.claude/dev/packet_loop.py" | cut -d' ' -f1)"
(cd "$W/work" && PYTHONDONTWRITEBYTECODE=1 python3 -B probe_models.py 2>&1 | grep -v Warning | grep -v trong_bang)
echo "probe rc=${PIPESTATUS[0]:-?}"
