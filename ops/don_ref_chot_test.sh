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
# `read -ra` NUỐT phần tử rỗng ở cuối, nên `a,` từng lọt vòng kiểm phần tử. Ba ca dưới
# soi chuỗi THÔ — không có chúng thì gỡ chốt ấy đi bộ test vẫn xanh (đã đo).
ca "dấu phẩy ở CUỐI thì DỪNG"             2 xoa-nhanh 'a,' "" XOA
ca "dấu phẩy ở ĐẦU thì DỪNG"              2 xoa-nhanh ',a' "" XOA
ca "hai dấu phẩy liền thì DỪNG"           2 xoa-nhanh 'a,,b' "" XOA
ca "sha có dấu phẩy cuối thì DỪNG"        2 tao-tag v1 "$SHA_THAT," TAO
ca "hai ref hợp lệ thì QUA"               0 xoa-nhanh 'tmp-probe-2, tmp-probe-delete' "" XOA
ca "xoá TAG dưới luu-tru/ thì DỪNG"       2 xoa-tag luu-tru/wp55-r4-verdict-review-1 "" XOA
# Bốn ca dưới khoá finding P2 `protection-is-exact-case-only`. Git PHÂN BIỆT hoa thường
# nên `Ops/x` đúng là nhánh khác `ops/x` — nhưng người đọc log thì không phân biệt, và
# `оps/x` với chữ `о` Cyrillic thì mắt thường không thấy gì cả.
ca "Ops/** viết HOA thì DỪNG"             2 xoa-nhanh Ops/secret "" XOA
ca "LUU-TRU/** viết HOA thì DỪNG"         2 xoa-nhanh LUU-TRU/x "" XOA
ca "chữ Cyrillic nhìn giống ops/ thì DỪNG" 2 xoa-nhanh 'оps/secret' "" XOA
ca "dấu // trong tên thì DỪNG"            2 xoa-nhanh 'a//b' "" XOA
ca "tên bắt đầu bằng dấu chấm thì DỪNG"   2 xoa-nhanh '.hidden' "" XOA
ca "thành phần bắt đầu bằng chấm thì DỪNG" 2 xoa-nhanh 'a/.b' "" XOA
ca "tên kết thúc .lock thì DỪNG"          2 xoa-nhanh 'a.lock' "" XOA
ca "tên kết thúc bằng / thì DỪNG"         2 xoa-nhanh 'a/' "" XOA
ca "tên dài 250 ký tự thì DỪNG"           2 xoa-nhanh "$(printf 'a%.0s' $(seq 250))" "" XOA
ca "tạo TAG mang tên vùng bảo vệ thì DỪNG" 2 tao-tag ops/x "$SHA_THAT" TAO
ca "tạo tag: sha sai dạng thì DỪNG"       2 tao-tag v1 "abc" TAO
ca "tạo tag: sha CHỮ HOA thì DỪNG"        2 tao-tag v1 "B4E5C5F9EF85E652FA2CC98BB3474036519D663C" TAO
ca "tạo tag: lệch số lượng thì DỪNG"      2 tao-tag 'v1,v2' "$SHA_THAT" TAO
ca "tạo tag hợp lệ thì QUA"               0 tao-tag v1 "$SHA_THAT" TAO
ca "tạo tag: hai cặp khớp thì QUA"        0 tao-tag 'v1,v2' "$SHA_THAT,$SHA_THAT" TAO


# ================= BƯỚC LÀM =================
# VÌ SAO PHẢI CÓ PHẦN NÀY. Bản đầu của tệp này chỉ phủ bước CHỐT — 23/23 xanh trong khi
# bước LÀM mang HAI lỗi P1. Chốt được phủ mà thao tác PHÁ thì không, nên bộ test xanh
# chẳng nói gì về thứ nguy hiểm nhất.
#
# VÀ BẢN THỨ HAI CỦA PHẦN NÀY CŨNG SAI, theo một cách đáng ghi hơn: `gh` giả khi ấy
# DIỄN KỊCH BẢN (lần đọc thứ hai luôn trả "không còn") thay vì mô phỏng TRẠNG THÁI.
# Hệ quả: đột biến XOÁ HẲN lệnh `gh api -X DELETE` vẫn cho 40/40 — bộ test đo NHÁNH RẼ
# của script chứ không đo THAO TÁC CÓ XẢY RA KHÔNG. Cross-review codex tìm ra bằng đúng
# đột biến ấy. Bản này: `gh` giả giữ TRẠNG THÁI thật (ref nào đã bị xoá), nên chỉ khi
# DELETE thật sự được gọi thì lần đọc sau mới thấy mất; cộng thêm phép đòi ĐÚNG MỘT lời
# gọi DELETE đúng endpoint trong nhật ký.
cat > "$TAM/bin/gh" <<'GHEOF'
#!/usr/bin/env bash
# `${*##...}` khai triển theo TỪNG tham số rồi mới nối, nên nó trả `api -X DELETE heads/a`
# chứ không phải `heads/a`. Gán vào một biến TRƯỚC rồi mới cắt. (Đo được khi ca "xoá:
# có trước, mất sau" đỏ với "VẪN CÒN" — bản ghi trạng thái và bản đọc lại cắt ra hai
# chuỗi khác nhau nên không bao giờ khớp.)
DONG="$*"
echo "$DONG" >> "$GIA_LOG"
DA_XOA="$GIA_LOG.daxoa"; touch "$DA_XOA"
case "$DONG" in
  *"-X DELETE"*)
      ten="${DONG##*/git/refs/}"
      [ "${GIA_DELETE_KHONG_AN_GI:-0}" = 1 ] || echo "$ten" >> "$DA_XOA"
      exit "${GIA_DELETE_RC:-0}" ;;
  *"-X POST"*)
      printf '%s' "$DONG" | tr ' ' '\n' | sed -n 's/^sha=//p' > "$GIA_LOG.sha"
      exit "${GIA_POST_RC:-0}" ;;
  *"--jq .object.sha"*) echo "${GIA_TAG_SHA:-$(cat "$GIA_LOG.sha" 2>/dev/null)}"; exit 0 ;;
  *"git/ref/"*)
      ten="${DONG##*/git/ref/}"
      n=$(grep -c 'git/ref/' "$GIA_LOG")            # lần đọc thứ mấy
      [ "${GIA_GET_ERR:-0}" = "$n" ] && { echo "HTTP/2 500 Internal Server Error"; exit 1; }
      # 500 mà THÂN có chữ "Not Found" — đây là ca khoá cách nhận diện 404. Phân loại
      # bằng chuỗi tự do sẽ đọc nó thành "ref không còn"; phân loại bằng DÒNG TRẠNG
      # THÁI thì không.
      [ "${GIA_GET_500_NOTFOUND:-0}" = "$n" ] && { printf 'HTTP/2 500 Internal Server Error\nmessage: Not Found\n'; exit 1; }
      # 500 mà THÂN có nguyên một dòng nhìn y hệt dòng trạng thái 404. Thân phản hồi do
      # máy chủ đầu kia quyết định, nên đây không phải ca giả tưởng.
      [ "${GIA_GET_500_GIA_DONG_404:-0}" = "$n" ] && { printf 'HTTP/2 500 Internal Server Error\nHTTP/2 404 dong than gia mao\n'; exit 1; }
      # DONG DAU chua chuoi "404" nhung KHONG phai trang thai 404. Neu ai do noi long
      # phep khop thanh mau bao trum thi ca nay lo ra ngay — reviewer luot 4 do duoc
      # rang dot bien ay song sot khi chua co no.
      [ "${GIA_GET_500_CO_CHU_404:-0}" = "$n" ] && { printf 'HTTP/2 500 upstream-404 gateway\n'; exit 1; }
      if [ "${GIA_MISSING:-0}" = 1 ] || grep -qxF "$ten" "$DA_XOA"; then
        echo "HTTP/2 404 Not Found"; exit 1
      fi
      echo "HTTP/2 200 OK"; exit 0 ;;
esac
exit 0
GHEOF
chmod +x "$TAM/bin/gh"

lam() {
  local ten="$1" mong="$2" hd="$3" ref="$4" sha="$5" thu="$6"; shift 6
  : > "$TAM/gialog"; rm -f "$TAM/gialog.daxoa" "$TAM/gialog.sha"
  env GIA_LOG="$TAM/gialog" HANH_DONG="$hd" REF="$ref" SHA="$sha" CHI_THU="$thu" \
      GITHUB_REPOSITORY=ducthangho/tra-luat "$@" bash "$TAM/lam.sh" >"$TAM/out" 2>&1
  local rc=$?
  if [ "$rc" = "$mong" ]; then QUA=$((QUA+1)); printf '  QUA   %s\n' "$ten"
  else HONG=$((HONG+1)); printf '  ĐỎ    %s  (rc=%s, mong %s)\n' "$ten" "$rc" "$mong"; sed 's/^/          /' "$TAM/out" | tail -4; fi
}

# Đo NHẬT KÝ, không đo mã thoát: đây là thứ duy nhất phân biệt "đã gọi lệnh xoá" với
# "ref tình cờ không còn".
doi_log() {
  local ten="$1" mau="$2" mong="$3"
  local n; n=$(grep -c -- "$mau" "$TAM/gialog" 2>/dev/null || true)
  if [ "$n" = "$mong" ]; then QUA=$((QUA+1)); printf '  QUA   %s\n' "$ten"
  else HONG=$((HONG+1)); printf '  ĐỎ    %s  (đếm %s, mong %s)\n' "$ten" "$n" "$mong"; fi
}

echo
echo "bước LÀM của ops-don-ref.yml — phản chứng"
S1=b4e5c5f9ef85e652fa2cc98bb3474036519d663c
S2=872679c360a43a4b12221749901aa0cf231566ac

lam "thử khô: KHÔNG gọi gh lần nào"       0 xoa-nhanh 'a,b' ""    true
doi_log "thử khô: nhật ký gh RỖNG"        "." 0

lam "xoá: có trước, mất sau -> XANH"      0 xoa-nhanh a "" false
doi_log "xoá: ĐÚNG MỘT lời gọi DELETE"    "-X DELETE" 1
doi_log "xoá: DELETE đi đúng endpoint"    "git/refs/heads/a" 1

lam "xoá HAI ref -> hai lời gọi DELETE"   0 xoa-nhanh 'a,b' "" false
doi_log "xoá hai: đếm DELETE = 2"         "-X DELETE" 2

lam "xoá TAG: đi đường refs/tags"         0 xoa-tag t1 "" false
doi_log "xoá tag: endpoint là refs/tags"  "git/refs/tags/t1" 1

lam "xoá: ref không tồn tại -> ĐỎ"        1 xoa-nhanh a "" false GIA_MISSING=1
doi_log "không tồn tại: KHÔNG gọi DELETE" "-X DELETE" 0

lam "xoá: đọc TRƯỚC lỗi 500 -> ĐỎ"        1 xoa-nhanh a "" false GIA_GET_ERR=1
doi_log "lỗi đọc trước: KHÔNG gọi DELETE" "-X DELETE" 0

lam "xoá: DELETE không ăn gì -> ĐỎ"       1 xoa-nhanh a "" false GIA_DELETE_KHONG_AN_GI=1
lam "xoá: đọc SAU lỗi 500 -> ĐỎ (fail-close)" 1 xoa-nhanh a "" false GIA_GET_ERR=2
lam "xoá: 500 mà thân có chữ Not Found -> vẫn ĐỎ" 1 xoa-nhanh a "" false GIA_GET_500_NOTFOUND=2
lam "xoá: 500-có-Not-Found ở lần đọc TRƯỚC -> ĐỎ" 1 xoa-nhanh a "" false GIA_GET_500_NOTFOUND=1
lam "xoá: 500 có DÒNG THÂN giả mạo 404 -> vẫn ĐỎ" 1 xoa-nhanh a "" false GIA_GET_500_GIA_DONG_404=2
lam "xoá: dòng thân giả 404 ở lần đọc TRƯỚC -> ĐỎ" 1 xoa-nhanh a "" false GIA_GET_500_GIA_DONG_404=1
lam "xoá: dòng ĐẦU có chữ 404 mà là 500 -> ĐỎ" 1 xoa-nhanh a "" false GIA_GET_500_CO_CHU_404=2
lam "xoá: dòng đầu có chữ 404, lần đọc TRƯỚC -> ĐỎ" 1 xoa-nhanh a "" false GIA_GET_500_CO_CHU_404=1

lam "tạo tag: đúng sha -> XANH"           0 tao-tag v1 "$S1" false
lam "tạo tag: API trả sha KHÁC -> ĐỎ"     1 tao-tag v1 "$S1" false GIA_TAG_SHA="$S2"
lam "tạo tag: hai cặp KHÁC sha, ghép đúng" 0 tao-tag 'v1,v2' "$S1,$S2" false
lam "tạo tag: phần tử rỗng giữa, vẫn ghép đúng" 0 tao-tag 'a,,b' "$S1,,$S2" false
lam "tạo tag: số cặp lệch sau khi nén -> ĐỎ" 1 tao-tag 'a,b' "$S1" false

TONG=$((QUA+HONG))
echo
echo "don_ref: $QUA/$TONG đạt (chốt + bước làm)"
[ "$HONG" = 0 ] || exit 1
