#!/usr/bin/env bash
# ops/cai_cong_cu.sh <ten>|--bat-buoc — doc ops/cong_cu.yaml (G1), cai roi DO LAI,
# KHONG tin rc trinh cai (r244). Giu 2 tinh chat cua cai_actionlint.sh: ban ghim o MOT noi
# (YAML) · KHONG `command -v` roi thoat som (T5). `cai.lenh` PHAI in duong dan vua cai lam
# DONG CUOI stdout de dua vao PATH truoc buoc DO LAI; khong in duong dan (vd pip) thi
# `[ -d ]` tra sai an toan.
set -euo pipefail
KICH="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)/$(basename -- "${BASH_SOURCE[0]}")"
GOC="$(cd -- "$(dirname -- "$KICH")/.." && pwd)"
cd -- "$GOC"  # cong thuc YAML la duong dan TUONG DOI; doc lap CWD nguoi goi
TEN="${1:-}"
[ -n "$TEN" ] || { echo "cai_cong_cu: thieu ten cong cu (vi du: actionlint)" >&2; exit 2; }
# Windows thuong chi co `python`; Linux/macOS co the chi co `python3` (CLAUDE.md).
if command -v python >/dev/null 2>&1; then PY=(python)
elif command -v python3 >/dev/null 2>&1; then PY=(python3)
elif command -v py >/dev/null 2>&1; then PY=(py -3)
else echo "cai_cong_cu: khong tim thay python, python3 hay py" >&2; exit 4
fi

if [ "$TEN" = "--bat-buoc" ]; then
  # PyYAML la bootstrap cua chinh ban ke. Ghim nay duoc t20 doi chieu voi YAML/CI;
  # khong the doc YAML de tim cong thuc cai khi module doc YAML chua ton tai.
  if ! "${PY[@]}" -c 'import yaml' 2>/dev/null; then
    if ! "${PY[@]}" -c 'import pip' 2>/dev/null; then
      "${PY[@]}" -m ensurepip --upgrade >/dev/null 2>&1 || true
    fi
    if ! "${PY[@]}" -c 'import pip' 2>/dev/null; then
      case "$(uname -s 2>/dev/null || true)" in
        Linux*)
          if command -v sudo >/dev/null 2>&1; then sudo apt-get update && sudo apt-get install -y python3-pip
          else apt-get update && apt-get install -y python3-pip
          fi ;;
        *) echo "cai_cong_cu: thieu pip; 'python -m ensurepip --upgrade' khong thanh cong" >&2; exit 6 ;;
      esac
    fi
    "${PY[@]}" -m pip install --quiet PyYAML==6.0.3
  fi
  BAT_BUOC=()
  # Windows: stdout cua python (text mode) la CRLF, `read -r` GIU `\r` => ten cong cu
  # thanh 'rg\r' va cong_cu.py tra "khong biet cong cu". Do that: run 33629605694 lane
  # windows-latest, batch rc=3 voi "khong biet cong cu 'batch-path-t21\r'". Cat CR o
  # phia DOC vi day la noi CRLF den; python phia kia khong doi duoc newline cua -c.
  while IFS= read -r cong_cu; do
    cong_cu="${cong_cu%$'\r'}"
    [ -n "$cong_cu" ] && BAT_BUOC+=("$cong_cu")
  done < <("${PY[@]}" -c '
import yaml
d=yaml.safe_load(open("ops/cong_cu.yaml", encoding="utf-8"))
print("\n".join(k for k,v in d["cong_cu"].items() if v["bat_buoc"] or v.get("chuan_bi")))')
  [ "${#BAT_BUOC[@]}" -gt 0 ] || { echo "cai_cong_cu: ban ke khong co cong cu bat buoc" >&2; exit 5; }
  for cong_cu in "${BAT_BUOC[@]}"; do
    # source de PATH do installer vua them ton tai o parent cho vong sau + probe cuoi.
    # KICH la path tuyet doi, khong dung lai $0 tu CWD cua caller.
    . "$KICH" "$cong_cu"
  done
  "${PY[@]}" "$GOC/ops/cong_cu.py" kiem-tra --json
  exit $?
fi
DAU_RA="$("${PY[@]}" "$GOC/ops/cong_cu.py" cai-lenh "$TEN")" || {
  echo "cai_cong_cu: '$TEN' khong co cong thuc cai tu dong cho nen nay" >&2
  exit 3
}
DAU_RA="${DAU_RA//$'\r'/}"  # cung ly do CRLF o tren: LENH/bien moi truong khong duoc mang \r
# #675: `| head -1` duoi pipefail = SIGPIPE khi head thoat truoc printf (do 2/3000; 20000 dong -> rc=141).
# Khai trien tham so khong co pipeline; do lai: ops/do_sigpipe.sh
LENH="${DAU_RA%%$'\n'*}"
while IFS= read -r dong; do
  case "$dong" in *=*) export "${dong?}" ;; esac
done < <(printf '%s\n' "$DAU_RA" | tail -n +2)

# eval TREN LENH doc tu ban ke cua CHINH kho — khong phai dau vao nguoi dung/mang ngoai.
KET_QUA_CAI="$(eval "$LENH")"
DICH="$(printf '%s\n' "$KET_QUA_CAI" | tail -1)"
DICH="${DICH%$'\r'}"  # trinh cai Windows (choco) in CRLF; \r lam `[ -d ]` sai am tham
[ -d "$DICH" ] && export PATH="$DICH:$PATH"

"${PY[@]}" "$GOC/ops/cong_cu.py" kiem-tra --chi "$TEN" --json
