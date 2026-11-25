#!/usr/bin/env bash
# Dung HAI clone day du cho phep do delta (base ↔ head) trong MOT lenh, cung cac buoc (bai hoc CLAUDE.md: rig khac nhau de ra hoi quy gia).
# dung: ab_dung.sh <kho nguon> <thu muc rig> <sha nen> <sha sau>
set -eu
NGUON="$1"; RIG="$2"; A="$3"; B="$4"
mkdir -p "$RIG"
for cap in "nen:$A" "sau:$B"; do
  ten="${cap%%:*}"; sha="${cap##*:}"
  [ ! -e "$RIG/$ten" ] || { echo "KHONG_DO_DUOC: $RIG/$ten da ton tai — dung thu muc rig moi"; exit 2; }
  git clone -q --no-hardlinks "$NGUON" "$RIG/$ten"
  git -C "$RIG/$ten" -c advice.detachedHead=false checkout -q "$sha"
  git -C "$RIG/$ten" config core.abbrev 7; git -C "$RIG/$ten" config core.autocrlf false; git -C "$RIG/$ten" config core.eol lf
  echo "$ten HEAD=$(git -C "$RIG/$ten" rev-parse HEAD) tree=$(git -C "$RIG/$ten" rev-parse 'HEAD^{tree}') shallow=$(git -C "$RIG/$ten" rev-parse --is-shallow-repository) .git=$([ -d "$RIG/$ten/.git" ] && echo thu_muc || echo TEP) sach=$(git -C "$RIG/$ten" status --porcelain | wc -l)"
done
