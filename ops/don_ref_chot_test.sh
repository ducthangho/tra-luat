#!/usr/bin/env bash
# Phản chứng cho CHỐT của `.github/workflows/ops-don-ref.yml`.
#
# VÌ SAO CÓ TỆP NÀY. Workflow ấy cấp lại đúng quyền mà sandbox cố ý không cho (xoá
# ref, ghi tag), và toàn bộ an toàn của nó nằm ở MỘT bước bash. Một chốt chưa ai chạy
# thì chỉ là chữ — đúng bệnh "ca có MẶT khác ca có ĐO" mà kho này đã trả giá nhiều lần.
# Ở đây tệ hơn chỗ khác: chốt chỉ chạy khi có người bấm dispatch, nên nếu nó hỏng thì
# lượt phát hiện đầu tiên CHÍNH LÀ lượt xoá nhầm.
#
# CÁCH LÀM. Trích nguyên văn thân bước chốt TỪ CHÍNH tệp YAML (không chép lại — chép
# lại là hai bản sẽ trôi lệch, và bên quên cập nhật chính là bên đẩy lọt), rồi chạy nó
# với `gh` GIẢ và bảng đầu vào. Không đụng mạng, không đụng repo thật.
#
# Chạy:  bash ops/don_ref_chot_test.sh
set -uo pipefail

GOC="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
YML="$GOC/.github/workflows/ops-don-ref.yml"
[ -f "$YML" ] || { echo "khong thay $YML"; exit 1; }

TAM="$(mktemp -d)"
trap 'rm -rf "$TAM"' EXIT

PY=python3; command -v python3 >/dev/null || PY=python   # Windows thường chỉ có `python`
"$PY" - "$YML" "$TAM/chot.sh" "$TAM/lam.sh" <<'PYEOF'
import sys, yaml
from pathlib import Path
d = yaml.safe_load(Path(sys.argv[1]).read_text(encoding="utf-8"))
steps = d["jobs"]["don"]["steps"]
# Bước CHỐT nhận diện bằng biến môi trường nó đọc, không bằng CHỈ SỐ: chèn thêm một
# bước vào đầu workflow sẽ làm chỉ số cứng trỏ nhầm mà test vẫn xanh.
chot = [s for s in steps if "XAC_NHAN" in (s.get("env") or {})]
assert len(chot) == 1, f"mong dung MOT buoc doc XAC_NHAN, thay {len(chot)}"
Path(sys.argv[2]).write_text("#!/usr/bin/env bash\n" + chot[0]["run"], encoding="utf-8")
lam = [s for s in steps if {"CHI_THU", "GH_TOKEN"} <= set(s.get("env") or {}) and "XAC_NHAN" not in (s.get("env") or {})]
assert len(lam) == 1, f"mong dung MOT buoc LAM, thay {len(lam)}"
Path(sys.argv[3]).write_text("#!/usr/bin/env bash\n" + lam[0]["run"], encoding="utf-8")
PYEOF
[ -s "$TAM/chot.sh" ] || { echo "khong trich duoc buoc chot"; exit 1; }
[ -s "$TAM/lam.sh" ]  || { echo "khong trich duoc buoc lam"; exit 1; }

# `gh` giả: chỉ trả nhánh mặc định. Chốt không được gọi gì khác ở bước này.
mkdir -p "$TAM/bin"
cat > "$TAM/bin/gh" <<'GHEOF'
#!/usr/bin/env bash
[ "${2:-}" = "repos/$GITHUB_REPOSITORY" ] && { echo master; exit 0; }
echo "gh gia: khong mong lenh nay: $*" >&2
exit 1
GHEOF
chmod +x "$TAM/bin/gh"
export PATH="$TAM/bin:$PATH" GITHUB_REPOSITORY=ducthangho/tra-luat

QUA=0; HONG=0
ca() {
  local ten="$1" mong="$2" hd="$3" ref="$4" sha="$5" xn="$6"
  env HANH_DONG="$hd" REF="$ref" SHA="$sha" XAC_NHAN="$xn" \
      bash "$TAM/chot.sh" >"$TAM/out" 2>&1
  local rc=$?
  if [ "$rc" = "$mong" ]; then QUA=$((QUA+1)); printf '  QUA   %s\n' "$ten"
  else HONG=$((HONG+1)); printf '  ĐỎ    %s  (rc=%s, mong %s)\n' "$ten" "$rc" "$mong"; sed 's/^/          /' "$TAM/out" | tail -3; fi
}

echo "chốt của ops-don-ref.yml — phản chứng"
SHA_THAT=b4e5c5f9ef85e652fa2cc98bb3474036519d663c

ca "xac_nhan sai thì DỪNG"                2 xoa-nhanh tmp-probe-2 "" xoa
ca "xac_nhan rỗng thì DỪNG"               2 xoa-nhanh tmp-probe-2 "" ""
ca "xac_nhan TAO cho lệnh XOÁ thì DỪNG"   2 xoa-nhanh tmp-probe-2 "" TAO
ca "ref thường + XOA thì QUA"             0 xoa-nhanh tmp-probe-2 "" XOA
ca "nhánh MẶC ĐỊNH thì DỪNG"              2 xoa-nhanh master "" XOA
ca "luu-tru/** thì DỪNG"                  2 xoa-nhanh luu-tru/wp55-r4/x "" XOA
ca "ops/** thì DỪNG"                      2 xoa-nhanh ops/wp55-r4-ho-so "" XOA
ca "claude/** thì DỪNG"                   2 xoa-nhanh claude/abc "" XOA
ca "codex/** thì DỪNG"                    2 xoa-nhanh codex/abc "" XOA
ca "agent/** thì DỪNG"                    2 xoa-nhanh agent/abc "" XOA
ca "mission/** thì DỪNG"                  2 xoa-nhanh mission/54/integration "" XOA
ca "có tiền tố refs/ thì DỪNG"            2 xoa-nhanh refs/heads/x "" XOA
ca "ký tự đại diện thì DỪNG"              2 xoa-nhanh 'tmp-*' "" XOA
ca "dấu ? thì DỪNG"                       2 xoa-nhanh 'tmp-?' "" XOA
ca "khoảng trắng giữa tên thì DỪNG"       2 xoa-nhanh 'tmp probe' "" XOA
ca "danh sách RỖNG thì DỪNG"              2 xoa-nhanh '  ,  ' "" XOA
ca "hai ref hợp lệ thì QUA"               0 xoa-nhanh 'tmp-probe-2, tmp-probe-delete' "" XOA
ca "xoá TAG dưới luu-tru/ thì DỪNG"       2 xoa-tag luu-tru/wp55-r4-verdict-review-1 "" XOA
# Bốn ca dưới khoá finding P2 `protection-is-exact-case-only`. Git PHÂN BIỆT hoa thường
# nên `Ops/x` đúng là nhánh khác `ops/x` — nhưng người đọc log thì không phân biệt, và
# `оps/x` với chữ `о` Cyrillic thì mắt thường không thấy gì cả.
ca "Ops/** viết HOA thì DỪNG"             2 xoa-nhanh Ops/secret "" XOA
ca "LUU-TRU/** viết HOA thì DỪNG"         2 xoa-nhanh LUU-TRU/x "" XOA
ca "chữ Cyrillic nhìn giống ops/ thì DỪNG" 2 xoa-nhanh 'оps/secret' "" XOA
ca "dấu // trong tên thì DỪNG"            2 xoa-nhanh 'a//b' "" XOA
ca "tạo TAG mang tên vùng bảo vệ thì DỪNG" 2 tao-tag ops/x "$SHA_THAT" TAO
ca "tạo tag: sha sai dạng thì DỪNG"       2 tao-tag v1 "abc" TAO
ca "tạo tag: sha CHỮ HOA thì DỪNG"        2 tao-tag v1 "B4E5C5F9EF85E652FA2CC98BB3474036519D663C" TAO
ca "tạo tag: lệch số lượng thì DỪNG"      2 tao-tag 'v1,v2' "$SHA_THAT" TAO
ca "tạo tag hợp lệ thì QUA"               0 tao-tag v1 "$SHA_THAT" TAO
ca "tạo tag: hai cặp khớp thì QUA"        0 tao-tag 'v1,v2' "$SHA_THAT,$SHA_THAT" TAO


# ================= BƯỚC LÀM =================
# VÌ SAO PHẢI CÓ PHẦN NÀY. Bản đầu của tệp này chỉ phủ bước CHỐT — 23/23 xanh trong khi
# bước LÀM mang HAI lỗi P1 (coi mọi lỗi API là "ref đã mất"; ghép lệch chỉ số khi danh
# sách có phần tử rỗng). Cross-review codex chỉ đúng: chốt được phủ mà thao tác PHÁ thì
# không, nên bộ test xanh chẳng nói gì về thứ nguy hiểm nhất.
#
# `gh` giả ở đây LÁI ĐƯỢC bằng biến GIA_*: mỗi ca dựng một kịch bản API rồi đo hành vi.
cat > "$TAM/bin/gh" <<'GHEOF'
#!/usr/bin/env bash
echo "$*" >> "$GIA_LOG"
case "$*" in
  *"-X DELETE"*)  exit "${GIA_DELETE_RC:-0}" ;;
  *"-X POST"*)
      # Ghi lai sha vua duoc yeu cau tao. Nho no ma phep kiem chung o buoc lam moi do
      # duoc GHEP DUNG CAP hay khong — thay vi luon tra mot hang so.
      printf '%s' "$*" | tr ' ' '\n' | sed -n 's/^sha=//p' > "$GIA_LOG.sha"
      exit "${GIA_POST_RC:-0}" ;;
  *"--jq .object.sha"*) echo "${GIA_TAG_SHA:-$(cat "$GIA_LOG.sha" 2>/dev/null)}"; exit 0 ;;
  *"git/ref/"*)
      n=$(grep -c 'git/ref/' "$GIA_LOG")          # lần đọc thứ mấy
      ma="GIA_GET_$n"; kb="${!ma:-${GIA_GET:-co}}"
      case "$kb" in
        co)      echo '{"ref":"x"}'; exit 0 ;;
        khong)   echo "gh: Not Found (HTTP 404)" >&2; exit 1 ;;
        loi)     echo "gh: HTTP 500 Internal Server Error" >&2; exit 1 ;;
      esac ;;
esac
exit 0
GHEOF
chmod +x "$TAM/bin/gh"

lam() {
  local ten="$1" mong="$2" hd="$3" ref="$4" sha="$5" thu="$6"; shift 6
  : > "$TAM/gialog"
  env GIA_LOG="$TAM/gialog" HANH_DONG="$hd" REF="$ref" SHA="$sha" CHI_THU="$thu" \
      GITHUB_REPOSITORY=ducthangho/tra-luat "$@" bash "$TAM/lam.sh" >"$TAM/out" 2>&1
  local rc=$?
  if [ "$rc" = "$mong" ]; then QUA=$((QUA+1)); printf '  QUA   %s\n' "$ten"
  else HONG=$((HONG+1)); printf '  ĐỎ    %s  (rc=%s, mong %s)\n' "$ten" "$rc" "$mong"; sed 's/^/          /' "$TAM/out" | tail -4; fi
}

echo
echo "bước LÀM của ops-don-ref.yml — phản chứng"
S1=b4e5c5f9ef85e652fa2cc98bb3474036519d663c
S2=872679c360a43a4b12221749901aa0cf231566ac

lam "thử khô: KHÔNG gọi gh lần nào"      0 xoa-nhanh 'a,b' ""      true
if [ -s "$TAM/gialog" ]; then HONG=$((HONG+1)); echo "  ĐỎ    thử khô mà VẪN gọi gh"; else QUA=$((QUA+1)); echo "  QUA   thử khô: gialog rỗng"; fi

lam "xoá: có trước, mất sau -> XANH"     0 xoa-nhanh a "" false GIA_GET_1=co GIA_GET_2=khong
lam "xoá: ref không tồn tại -> ĐỎ"       1 xoa-nhanh a "" false GIA_GET=khong
lam "xoá: đọc TRƯỚC lỗi 500 -> ĐỎ"       1 xoa-nhanh a "" false GIA_GET=loi
lam "xoá: gọi xong mà VẪN CÒN -> ĐỎ"     1 xoa-nhanh a "" false GIA_GET=co
lam "xoá: đọc SAU lỗi 500 -> ĐỎ (fail-close)" 1 xoa-nhanh a "" false GIA_GET_1=co GIA_GET_2=loi
lam "tạo tag: đúng sha -> XANH"          0 tao-tag v1 "$S1" false GIA_TAG_SHA="$S1"
lam "tạo tag: API trả sha KHÁC -> ĐỎ"    1 tao-tag v1 "$S1" false GIA_TAG_SHA="$S2"
lam "tạo tag: hai cặp KHÁC sha, ghép đúng -> XANH" 0 tao-tag 'v1,v2' "$S1,$S2" false
# Đây là ca khoá finding P1 `sparse-list-misaligns-tag-and-sha`: có phần tử RỖNG ở
# GIỮA cả hai danh sách. Bản trước nén một bên mà không nén bên kia nên `b` nhận sha
# RỖNG; nay hai danh sách cùng được nén nên `b` phải nhận đúng $S2.
lam "tạo tag: phần tử rỗng giữa danh sách, vẫn ghép đúng" 0 tao-tag 'a,,b' "$S1,,$S2" false
lam "tạo tag: số cặp lệch sau khi nén -> ĐỎ" 1 tao-tag 'a,b' "$S1" false

TONG=$((QUA+HONG))
echo
echo "don_ref: $QUA/$TONG đạt (chốt + bước làm)"
[ "$HONG" = 0 ] || exit 1
