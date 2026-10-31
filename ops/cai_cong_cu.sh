#!/usr/bin/env bash
# ops/cai_cong_cu.sh <ten>|--bat-buoc — doc ops/cong_cu.yaml (G1), cai roi DO LAI,
# KHONG tin rc trinh cai (r244). Giu 2 tinh chat cua cai_actionlint.sh: ban ghim o MOT noi
# (YAML) · KHONG `command -v` roi thoat som (T5). Thu muc vua cai di qua KENH KET QUA rieng
# (`chon_thu_muc_chay_duoc`, wp868); cong thuc KHONG goi bo chon thi DONG CUOI stdout cua no
# la thu muc (vd cai_actionlint.sh); khong in duong dan (vd pip) thi `[ -d ]` tra sai an toan.
set -euo pipefail
KICH="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)/$(basename -- "${BASH_SOURCE[0]}")"
GOC="$(cd -- "$(dirname -- "$KICH")/.." && pwd)"
cd -- "$GOC"  # cong thuc YAML la duong dan TUONG DOI; doc lap CWD nguoi goi
TEN="${1:-}"
[ -n "$TEN" ] || { echo "cai_cong_cu: thieu ten cong cu (vi du: actionlint)" >&2; exit 2; }
# Windows thuong chi co `python`; Linux/macOS co the chi co `python3` (CLAUDE.md).
# wp831 (Codex luot 3 F03): luot duoc `source` trong vong `--bat-buoc` cua CUNG shell DUNG LAI PY da ghim cua luot
# cha — chon lai o day se doc PATH ma cong thuc cong cu truoc vua doi (vd thu muc rg co Python thieu PyYAML). Dau hieu
# la bien shell KHONG export gan voi $$, va PY phai la MANG do luot cha tao.
# Codex luot 4 F04: dau den tu MOI TRUONG luon mang thuoc tinh export (va `exec` giu nguyen PID, nen so gia tri voi $$
# khong du) => bo dau ay truoc khi xet; PY vo huong tu moi truong khong bao gio duoc dung lai.
case "$(declare -p CAI_CONG_CU_PY_CUA 2>/dev/null)" in "declare -x"*) unset CAI_CONG_CU_PY_CUA ;; esac
if [ "${CAI_CONG_CU_PY_CUA:-}" = "$$" ] && [[ "$(declare -p PY 2>/dev/null)" == "declare -a"* ]]; then :
elif command -v python >/dev/null 2>&1; then PY=(python)
elif command -v python3 >/dev/null 2>&1; then PY=(python3)
elif command -v py >/dev/null 2>&1; then PY=(py -3)
else echo "cai_cong_cu: khong tim thay python, python3 hay py" >&2; exit 4
fi
# wp831 (Codex luot 2 F03): ghim PY[0] thanh duong dan tuyet doi NGAY tai day. Cong thuc `rg.cai` goi checker duoi
# `PATH="$RG_D:$PATH"`, va dong kiem cuoi chay sau `export PATH="$DICH:$PATH"`: ten tran se doi sang Python cua thu muc
# ung vien (vd thieu PyYAML). Giu nguyen doi so con lai cua mang (`py -3`).
PY[0]="$(command -v "${PY[0]}")"

# wp858 (L1, Q1): MOT bo chon thu muc cho cong thuc `cai` (duoc `eval` duoi day). `dirname "$(command -v X)"` in thu
# muc ban DAU PATH, ke ca ban HONG. Chuan DUY NHAT: CHINH `cong_cu.py kiem-tra --chi <ten>` bang PY da ghim (wp831 F03),
# khong loc `-f/-x/.exe` (ten tran chua DAT thi thu muc khong co <ten> khong doi phep tra ten — F858-02).
# wp868 (N1, Q1): ket qua ghi vao KENH RIENG `$KENH_KQ` (tep mktemp, bien KHONG export => trinh cai con khong biet duong
# dan), KHONG in ra stdout: stdout di chung voi trinh cai nen moi dong canh/LF deu thua (F858-03, 4 duong). Noi dung
# kenh: `GIU_PATH` (ten tran da DAT => khong doi PATH, Q3) hoac `DICH` + LF + thu muc (khong LF cuoi, doc nguyen van).
# `--win`: ung vien qua `cygpath -u`, $GITHUB_PATH qua `cygpath -w`; ghi $GITHUB_PATH chi khi ten tran chua DAT. Moi buoc
# hong => `return 1` TUONG MINH vi cong thuc chay voi `errexit` tat (F858-01/04).
# wp1045: "<ten> DAT" = `trang_thai` cua CHINH cong cu ay trong `kiem-tra --chi <ten> --json`, KHONG phai rc. `tong_hop`
# chi nang KHONG_DO_DUOC len trang_thai_tong khi `bat_buoc: true` (#498, hop dong #290) => cong cu tuy chon VANG MAT van
# rc=0. Tin rc la nhan `GIU_PATH` cho shellcheck khong co tren PATH (run 41069257658, windows-latest: bo chon khong thu
# `choco\bin`, khong ghi $GITHUB_PATH, buoc xanh roi `G5 probe` do). Ket qua JSON phai co DUNG MOT muc, dung ten.
cong_cu_json_dung() {  # <ten> <khoa> <gia tri JSON> — muc DUY NHAT cua <ten> trong `kiem-tra --chi` co <khoa> == <gia tri>
  local json
  json="$("${PY[@]}" "$GOC/ops/cong_cu.py" kiem-tra --chi "$1" --json 2>/dev/null)" || return 1
  printf '%s' "$json" | "${PY[@]}" -c 'import json, sys
c = json.load(sys.stdin).get("cong_cu") or []
sys.exit(0 if len(c) == 1 and c[0].get("ten") == sys.argv[1] and c[0].get(sys.argv[2]) == json.loads(sys.argv[3]) else 1)' \
    "$1" "$2" "$3" 2>/dev/null
}
cong_cu_dat() { cong_cu_json_dung "$1" trang_thai '"DAT"'; }  # <ten>

chon_thu_muc_chay_duoc() {  # [--win] <ten> <ung vien>...
  local win="" ten d dich="" w
  [ -n "${KENH_KQ:-}" ] || { echo "cai_cong_cu: chon_thu_muc_chay_duoc chi chay duoi cai_cong_cu.sh (thieu KENH_KQ)" >&2; return 1; }
  if [ "${1:-}" = "--win" ]; then win=1; shift; fi
  ten="$1"; shift
  if cong_cu_dat "$ten"; then
    echo "cai_cong_cu: '$ten' ten tran da DAT, giu nguyen PATH" >&2
    printf 'GIU_PATH' > "$KENH_KQ" || { echo "cai_cong_cu: khong ghi duoc kenh ket qua" >&2; return 1; }
    return 0
  fi
  for d in "$@"; do
    if [ -n "$win" ]; then
      d="$(cygpath -u "$d")" || { echo "cai_cong_cu: cygpath -u hong cho ung vien cua '$ten'" >&2; return 1; }
    fi
    if PATH="$d:$PATH" cong_cu_dat "$ten"; then dich="$d"; break; fi
  done
  [ -n "$dich" ] || { echo "cai_cong_cu: khong thu muc nao co '$ten' chay duoc" >&2; return 1; }
  if [ -n "${GITHUB_PATH:-}" ]; then
    w="$dich"
    if [ -n "$win" ]; then
      w="$(cygpath -w "$dich")" || { echo "cai_cong_cu: cygpath -w hong cho '$dich'" >&2; return 1; }
    fi
    printf '%s\n' "$w" >> "$GITHUB_PATH" || { echo "cai_cong_cu: khong ghi duoc \$GITHUB_PATH" >&2; return 1; }
  fi
  printf 'DICH\n%s' "$dich" > "$KENH_KQ" || { echo "cai_cong_cu: khong ghi duoc kenh ket qua" >&2; return 1; }
}

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
  # Gan ROI MOI go export: duoi `allexport` (`bash -a`, SHELLOPTS) chinh phep gan tu export lai, ke ca sau `unset`
  # hay `declare +x X=...` mot buoc (Codex luot 5: luot `source` cho rg thay dau export, xoa no, va bash chon lai Python).
  CAI_CONG_CU_PY_CUA=$$
  declare +x CAI_CONG_CU_PY_CUA  # chi cac luot `source` duoi day thay (xem khoi chon python); installer con khong thay
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

# wp868 (N1/N2, Q1/Q2): thu muc TAM rieng cho kenh ket qua + stdout trinh cai. Gan ROI MOI go export (allexport, nhu
# CAI_CONG_CU_PY_CUA): trinh cai con khong thay duong dan kenh. `rm` tuong minh sau khi doc; `trap` lo duong thoat loi
# (luot `source` cua --bat-buoc ghi de trap cua nhau, nen moi luot tu xoa thu muc cua no).
TAM_CAI="$(mktemp -d "${TMPDIR:-/tmp}/cai_cong_cu.XXXXXX")"
declare +x TAM_CAI
trap 'rm -rf -- "$TAM_CAI"' EXIT
KENH_KQ="$TAM_CAI/kq"
declare +x KENH_KQ
: > "$KENH_KQ"
# eval TREN LENH doc tu ban ke cua CHINH kho — khong phai dau vao nguoi dung/mang ngoai. Subshell `( )` + chuyen huong
# vao TEP thay cho `$( )`: bash chi cho subshell thoat, KHONG cho EOF cua stdout — tien trinh con chay nen giu stdout
# (writer muon) khong lam treo (N2), va moi gi no ghi sau do khong con duoc doc lam ket qua. `set +e`: giu ngu nghia
# `$( )` cu (errexit tat) — ma thoat la cua chuoi `&&`, cac `return 1` tuong minh cua bo chon la chot.
# wp1045 (M2): bo chon nay THU ung vien cho cong cu tuy chon vang mat, nen no co the hong o day; luot `source` cua --bat-buoc
# KHONG duoc dung vi cong cu `bat_buoc: false` (vd shellcheck dung truoc rg) — canh bao roi di tiep, `kiem-tra --json` toan bo
# cuoi vong quyet. Moi truong hop khac thoat DUNG ma cu (errexit truoc day thoat bang chinh ma cua lenh hong).
# Codex wp1045 luot 1 (P3): KHONG `( … ) || RC_CAI=$?` — `||` dat CA subshell vao ngu canh dieu kien, nen cong thuc tu bat lai
# `set -e` cung khong dung (base rc=1, ban `||` rc=0). Tat errexit o shell CHA, chay subshell o vi tri khong dieu kien, lay `$?`.
set +e
( set +e; eval "$LENH" ) > "$TAM_CAI/stdout"
RC_CAI=$?
set -e
if [ "$RC_CAI" -ne 0 ]; then
  if [ "${CAI_CONG_CU_PY_CUA:-}" = "$$" ] && cong_cu_json_dung "$TEN" bat_buoc false; then
    echo "cai_cong_cu: '$TEN' (bat_buoc: false) khong cai duoc (rc=$RC_CAI); --bat-buoc di tiep" >&2
    rm -rf -- "$TAM_CAI"
    return 0
  fi
  exit "$RC_CAI"
fi
# F868-01 (Codex luot 1): `;` truoc `printf x` che loi doc kenh => kenh "rong" => roi ve stdout. Doc hong => DUNG.
KQ="$(cat -- "$KENH_KQ" && printf x)" || { echo "cai_cong_cu: khong doc duoc kenh ket qua" >&2; exit 7; }
KQ="${KQ%x}"
case "$KQ" in
  GIU_PATH) DICH="" ;;
  DICH$'\n'?*) DICH="${KQ#DICH$'\n'}" ;;
  "")  # cong thuc khong goi bo chon (pip, cai_actionlint.sh): dong cuoi stdout nhu truoc (N3)
    KET_QUA_CAI="$(cat -- "$TAM_CAI/stdout")"
    DICH="$(printf '%s\n' "$KET_QUA_CAI" | tail -1)"
    DICH="${DICH%$'\r'}" ;;  # trinh cai Windows (choco) in CRLF; \r lam `[ -d ]` sai am tham
  *) echo "cai_cong_cu: kenh ket qua hong: $(printf '%q' "$KQ")" >&2; exit 7 ;;
esac
rm -rf -- "$TAM_CAI"
[ -d "$DICH" ] && export PATH="$DICH:$PATH"

# wp1045 (M2): goi TRUC TIEP mot cong cu => cai xong ma CHINH no chua DAT thi thoat 3 (KHONG_DO_DUOC) kem dong neu ten, ke ca
# khi `bat_buoc: false` lam kiem-tra rc=0. Codex luot 1 (P2): kiem cuoi KHONG duoc dung tran duoi `set -e` o nhanh nay — DO
# (rc=2) / bat buoc vang (rc=3) se thoat truoc chot. Luot `source` cua --bat-buoc (CAI_CONG_CU_PY_CUA = $$) giu hanh vi cu:
# dong kiem tran, rc khac 0 cham dut vong nhu truoc; cong cu tuy chon thieu (rc=0) khong chan cong cu dung sau no.
if [ "${CAI_CONG_CU_PY_CUA:-}" = "$$" ]; then
  "${PY[@]}" "$GOC/ops/cong_cu.py" kiem-tra --chi "$TEN" --json
else
  RC_KT=0
  "${PY[@]}" "$GOC/ops/cong_cu.py" kiem-tra --chi "$TEN" --json || RC_KT=$?
  if [ "$RC_KT" -ne 0 ] || ! cong_cu_dat "$TEN"; then
    echo "cai_cong_cu: '$TEN' chua DAT sau khi cai (trang_thai cua chinh no khac DAT; kiem-tra rc=$RC_KT)" >&2
    exit 3
  fi
fi
