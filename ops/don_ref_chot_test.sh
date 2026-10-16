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
DONG="$*"
echo "$DONG" >> "${GIA_LOG_CHOT:-/dev/null}"
case "$DONG" in
  *"repos/$GITHUB_REPOSITORY --jq .default_branch"*) echo master; exit 0 ;;
  *"git/ref/heads/"*)
      # SHA cua nhanh luu-tru. GIA_SHA_NHANH= rong => coi nhu doc KHONG duoc.
      [ -n "${GIA_SHA_NHANH:-}" ] && { echo "$GIA_SHA_NHANH"; exit 0; }
      exit 1 ;;
  *"/compare/"*)
      # `behind_by` cua phep do to-tien. GIA_BEHIND rong => coi nhu KHONG DO DUOC.
      # GIA_BEHIND_RAC=1 => tra ra thu KHONG phai so, de khoa chot kiem dang.
      [ "${GIA_BEHIND_RAC:-0}" = 1 ] && { echo "null"; exit 0; }
      [ -n "${GIA_BEHIND:-}" ] && { echo "$GIA_BEHIND"; exit 0; }
      exit 1 ;;
  *"repos/$GITHUB_REPOSITORY/tags"*)
      # Danh sach tag DA dereference. GIA_TAG_SHAS = trang MOT, cach nhau bang khoang trang.
      for s in ${GIA_TAG_SHAS:-}; do echo "$s"; done
      # TRANG HAI chi hien khi co `--paginate`. Nho no ma bo test khoa duoc chinh co ay:
      # bo `--paginate` thi mot tag nam o trang sau tro nen vo hinh, va nhanh co tag giu
      # se bi tu choi SAI.
      case "$DONG" in *--paginate*) for s in ${GIA_TAG_SHAS_TRANG2:-}; do echo "$s"; done ;; esac
      # Xuat mot phan roi HONG — ca nay khoa `pipefail`. Neu thieu pipefail thi `grep`
      # tra 0 va chot cho xoa trong khi danh sach tag CHUA doc tron ven.
      [ "${GIA_TAG_HONG_GIUA:-0}" = 1 ] && exit 1
      exit 0 ;;
esac
echo "gh gia: khong mong lenh nay: $DONG" >&2
exit 1
GHEOF
chmod +x "$TAM/bin/gh"
export PATH="$TAM/bin:$PATH" GITHUB_REPOSITORY=ducthangho/tra-luat

QUA=0; HONG=0
ca() {
  local ten="$1" mong="$2" hd="$3" ref="$4" sha="$5" xn="$6"; shift 6
  : > "$TAM/gialog_chot"
  env HANH_DONG="$hd" REF="$ref" SHA="$sha" XAC_NHAN="$xn" GIA_LOG_CHOT="$TAM/gialog_chot" "$@" \
      bash "$TAM/chot.sh" >"$TAM/out" 2>&1
  local rc=$?
  if [ "$rc" = "$mong" ]; then QUA=$((QUA+1)); printf '  QUA   %s\n' "$ten"
  else HONG=$((HONG+1)); printf '  ĐỎ    %s  (rc=%s, mong %s)\n' "$ten" "$rc" "$mong"; sed 's/^/          /' "$TAM/out" | tail -3; fi
}

# Đo THÔNG ĐIỆP, không chỉ đo mã thoát. Cần vì ba trạng thái `là tổ tiên` / `không phải`
# / `KHÔNG ĐO ĐƯỢC` cùng cho mã 2, nên mã thoát KHÔNG phân biệt được chúng. Đã đo: thiếu
# phép này thì đột biến gỡ chốt kiểm DẠNG SỐ của `behind_by` vẫn cho 99/99 — vì `!= 0`
# tự nó đã từ chối mọi thứ không phải "0", kể cả `null`. Quyết định thì giống, LÝ DO thì
# khác, và kho này phân biệt "không có" với "không đo được".
doi_ra() {
  local ten="$1" mau="$2"
  if grep -q -- "$mau" "$TAM/out" 2>/dev/null; then QUA=$((QUA+1)); printf '  QUA   %s\n' "$ten"
  else HONG=$((HONG+1)); printf '  ĐỎ    %s  (không thấy %q trong đầu ra)\n' "$ten" "$mau"; sed 's/^/          /' "$TAM/out" | tail -3; fi
}

# Đo NHẬT KÝ của bước chốt. Cần vì mã thoát không phân biệt được "dừng vì không đọc
# được SHA" với "dừng vì không tag nào giữ" — cả hai đều là 2. Đã đo: thiếu phép này
# thì đột biến GỠ chốt "không đọc được SHA thì dừng" vẫn cho 69/69, tức chốt ấy không
# được khoá. Fail-close mà không ai đo thì cũng chỉ là chữ.
doi_log_chot() {
  local ten="$1" mau="$2" mong="$3"
  local n; n=$(grep -c -- "$mau" "$TAM/gialog_chot" 2>/dev/null || true)
  if [ "$n" = "$mong" ]; then QUA=$((QUA+1)); printf '  QUA   %s\n' "$ten"
  else HONG=$((HONG+1)); printf '  ĐỎ    %s  (đếm %s, mong %s)\n' "$ten" "$n" "$mong"; fi
}

echo "chốt của ops-don-ref.yml — phản chứng"
SHA_THAT=b4e5c5f9ef85e652fa2cc98bb3474036519d663c

ca "xac_nhan sai thì DỪNG"                2 xoa-nhanh tmp-probe-2 "" xoa
ca "xac_nhan rỗng thì DỪNG"               2 xoa-nhanh tmp-probe-2 "" ""
ca "xac_nhan TAO cho lệnh XOÁ thì DỪNG"   2 xoa-nhanh tmp-probe-2 "" TAO
# Từ bản vá CAS: MỌI ref sắp xoá đều được đọc SHA để ghim, vì bước làm xoá bằng lease.
# Không cấp SHA giả ⇒ chốt DỪNG, và đó là hành vi ĐÚNG (không ghim được thì không xoá).
S_THUONG=dddddddddddddddddddddddddddddddddddddddd
ca "ref thường + XOA thì QUA"             0 xoa-nhanh tmp-probe-2 "" XOA GIA_SHA_NHANH="$S_THUONG"
ca "ref thường mà KHÔNG đọc được SHA thì DỪNG" 2 xoa-nhanh tmp-probe-2 "" XOA
ca "nhánh MẶC ĐỊNH thì DỪNG"              2 xoa-nhanh master "" XOA
# BẤT BIẾN mới cho `luu-tru/**`: xoá NHÁNH được, nhưng CHỈ KHI commit của nó còn tag
# giữ. Năm ca dưới khoá đúng hợp đồng ấy — cả chiều cho phép lẫn ba chiều từ chối.
S_LT=aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
ca "luu-tru/**: có tag giữ thì QUA"       0 xoa-nhanh luu-tru/wp55-r4/x "" XOA GIA_SHA_NHANH="$S_LT" GIA_TAG_SHAS="$S_LT bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb"
doi_log_chot "…và CÓ đọc SHA của nhánh"   "git/ref/heads/" 1
doi_log_chot "…và CÓ hỏi danh sách tag"   "/tags" 1
ca "luu-tru/**: KHÔNG tag nào giữ thì DỪNG" 2 xoa-nhanh luu-tru/wp55-r4/x "" XOA GIA_SHA_NHANH="$S_LT" GIA_TAG_SHAS="bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb"
ca "luu-tru/**: kho KHÔNG có tag nào thì DỪNG" 2 xoa-nhanh luu-tru/wp55-r4/x "" XOA GIA_SHA_NHANH="$S_LT" GIA_TAG_SHAS=""
ca "luu-tru/**: không đọc được SHA thì DỪNG" 2 xoa-nhanh luu-tru/wp55-r4/x "" XOA GIA_TAG_SHAS="$S_LT"
# DỪNG SỚM: không đọc được SHA thì KHÔNG được hỏi tiếp danh sách tag. Nếu vẫn hỏi thì
# nghĩa là chốt đã bị gỡ và luồng chảy tiếp — mã thoát vẫn 2 nên chỉ nhật ký thấy.
doi_log_chot "…và KHÔNG hỏi danh sách tag (dừng sớm)" "/tags" 0
ca "luu-tru/**: xoá TAG thì vẫn CẤM"      2 xoa-tag luu-tru/wp55-r4/x "" XOA GIA_SHA_NHANH="$S_LT" GIA_TAG_SHAS="$S_LT"
# Hai ca dưới là finding P2 của cross-review codex trên chính bản vá này: hợp đồng đúng
# nhưng KHÔNG ĐƯỢC KHOÁ — gỡ `--paginate` hay gỡ `pipefail` thì bộ test vẫn xanh.
ca "luu-tru/**: tag giữ ở TRANG SAU vẫn QUA" 0 xoa-nhanh luu-tru/wp55-r4/x "" XOA GIA_SHA_NHANH="$S_LT" GIA_TAG_SHAS="bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb" GIA_TAG_SHAS_TRANG2="$S_LT"
ca "luu-tru/**: gh hỏng GIỮA phân trang thì DỪNG" 2 xoa-nhanh luu-tru/wp55-r4/x "" XOA GIA_SHA_NHANH="$S_LT" GIA_TAG_SHAS="$S_LT" GIA_TAG_HONG_GIUA=1
# ═══ HỢP ĐỒNG MỚI cho vùng làm việc (21-08-2026): lệnh CẤM đổi thành PHÉP ĐO ═══
# Bất biến giữ nguyên — "đừng làm commit thành không tra được" — nhưng nay ĐO thay vì
# đoán: nhánh mà MỌI commit đã nằm trong nhánh mặc định thì xoá không mất gì.
# Ba trạng thái: là tổ tiên · không phải · KHÔNG ĐO ĐƯỢC. Trạng thái thứ ba phải ĐỎ.
S_VLV=cccccccccccccccccccccccccccccccccccccccc
ca "ops/**: 0 commit ngoài mặc định thì QUA"   0 xoa-nhanh ops/wp55-r4-ho-so "" XOA GIA_SHA_NHANH="$S_VLV" GIA_BEHIND=0 NEO_TEP="$TAM/neo.txt"
doi_log_chot "…và CÓ đọc SHA của nhánh"        "git/ref/heads/" 1
doi_log_chot "…và CÓ gọi compare"              "/compare/" 1
ca "claude/**: 0 commit ngoài mặc định thì QUA" 0 xoa-nhanh claude/abc "" XOA GIA_SHA_NHANH="$S_VLV" GIA_BEHIND=0 NEO_TEP="$TAM/neo.txt"
ca "codex/**: 0 commit ngoài mặc định thì QUA"  0 xoa-nhanh codex/abc "" XOA GIA_SHA_NHANH="$S_VLV" GIA_BEHIND=0 NEO_TEP="$TAM/neo.txt"
ca "agent/**: 0 commit ngoài mặc định thì QUA"  0 xoa-nhanh agent/abc "" XOA GIA_SHA_NHANH="$S_VLV" GIA_BEHIND=0 NEO_TEP="$TAM/neo.txt"
ca "mission/**: 0 commit ngoài mặc định thì QUA" 0 xoa-nhanh mission/54/integration "" XOA GIA_SHA_NHANH="$S_VLV" GIA_BEHIND=0 NEO_TEP="$TAM/neo.txt"
# Chiều TỪ CHỐI — ba đường, ba lý do khác nhau, cùng mã thoát 2 nên phải soi nhật ký.
ca "ops/**: CÒN commit ngoài mặc định thì DỪNG" 2 xoa-nhanh ops/dang-lam "" XOA GIA_SHA_NHANH="$S_VLV" GIA_BEHIND=3 NEO_TEP="$TAM/neo.txt"
doi_ra "…và nói ĐÚNG lý do: còn 3 commit"      "còn 3 commit CHƯA có trong"
ca "ops/**: không đọc được SHA thì DỪNG"       2 xoa-nhanh ops/dang-lam "" XOA GIA_BEHIND=0 NEO_TEP="$TAM/neo.txt"
# DỪNG SỚM: không đọc được SHA thì KHÔNG được đi hỏi compare. Mã thoát không phân biệt
# được, chỉ nhật ký thấy — đúng lối `luu-tru/**` đã dùng.
doi_log_chot "…và KHÔNG gọi compare (dừng sớm)" "/compare/" 0
ca "ops/**: compare KHÔNG ĐO ĐƯỢC thì DỪNG"    2 xoa-nhanh ops/dang-lam "" XOA GIA_SHA_NHANH="$S_VLV" NEO_TEP="$TAM/neo.txt"
doi_ra "…và nói ĐÚNG lý do: KHÔNG ĐO ĐƯỢC"    "KHÔNG ĐO ĐƯỢC quan hệ"
# `null` là thứ `--jq` trả khi trường vắng mặt. Nó KHÔNG phải số, và đọc nó thành 0 là
# đúng cách một cổng biến "không có dữ liệu" thành "đạt".
ca "ops/**: compare trả RÁC (không phải số) thì DỪNG" 2 xoa-nhanh ops/dang-lam "" XOA GIA_SHA_NHANH="$S_VLV" GIA_BEHIND_RAC=1 NEO_TEP="$TAM/neo.txt"
doi_ra "…và nói ĐÚNG lý do: KHÔNG ĐO ĐƯỢC"    "KHÔNG ĐO ĐƯỢC quan hệ"
# TAG mang tên vùng làm việc: KHÔNG có quan hệ tổ-tiên để đo ⇒ phép đo không thay được
# lệnh cấm, và lệnh cấm ở đó giữ nguyên.
ca "xoá TAG tên vùng làm việc thì vẫn CẤM"     2 xoa-tag ops/x "" XOA GIA_SHA_NHANH="$S_VLV" GIA_BEHIND=0 NEO_TEP="$TAM/neo.txt"
# GHIM: bước chốt phải ghi lại SHA đã đo, vì bước làm sẽ đòi đúng SHA ấy ngay trước khi
# xoá. Không ghim thì phép đo chỉ nói về QUÁ KHỨ.
: > "$TAM/neo.txt"
ca "ops/**: QUA thì phải GHIM SHA ra tệp"      0 xoa-nhanh ops/ho-so-x5 "" XOA GIA_SHA_NHANH="$S_VLV" GIA_BEHIND=0 NEO_TEP="$TAM/neo.txt"
if grep -qxF "ops/ho-so-x5 $S_VLV" "$TAM/neo.txt"; then
  QUA=$((QUA+1)); printf '  QUA   %s\n' "…và dòng ghim đúng 'ref sha'"
else
  HONG=$((HONG+1)); printf '  ĐỎ    %s\n' "…và dòng ghim đúng 'ref sha'"; sed 's/^/          /' "$TAM/neo.txt"
fi
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
ca "hai ref hợp lệ thì QUA"               0 xoa-nhanh 'tmp-probe-2, tmp-probe-delete' "" XOA GIA_SHA_NHANH="$S_THUONG"
ca "xoá TAG dưới luu-tru/ thì DỪNG"       2 xoa-tag luu-tru/wp55-r4-verdict-review-1 "" XOA GIA_SHA_NHANH=aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa GIA_TAG_SHAS=aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
# Bốn ca dưới khoá finding P2 `protection-is-exact-case-only`. Git PHÂN BIỆT hoa thường
# nên `Ops/x` đúng là nhánh khác `ops/x` — nhưng người đọc log thì không phân biệt, và
# `оps/x` với chữ `о` Cyrillic thì mắt thường không thấy gì cả.
ca "Ops/** viết HOA thì DỪNG"             2 xoa-nhanh Ops/secret "" XOA
ca "LUU-TRU/** viết HOA: cùng luật, không tag thì DỪNG" 2 xoa-nhanh LUU-TRU/x "" XOA GIA_SHA_NHANH=aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa GIA_TAG_SHAS=""
ca "chữ Cyrillic nhìn giống ops/ thì DỪNG" 2 xoa-nhanh 'оps/secret' "" XOA
ca "dấu // trong tên thì DỪNG"            2 xoa-nhanh 'a//b' "" XOA
ca "tên bắt đầu bằng dấu chấm thì DỪNG"   2 xoa-nhanh '.hidden' "" XOA
ca "thành phần bắt đầu bằng chấm thì DỪNG" 2 xoa-nhanh 'a/.b' "" XOA
ca "tên kết thúc .lock thì DỪNG"          2 xoa-nhanh 'a.lock' "" XOA
ca "tên kết thúc bằng / thì DỪNG"         2 xoa-nhanh 'a/' "" XOA
ca "tên dài 250 ký tự thì DỪNG"           2 xoa-nhanh "$(printf 'a%.0s' $(seq 250))" "" XOA
ca "tạo TAG mang tên vùng bảo vệ thì DỪNG" 2 tao-tag ops/x "$SHA_THAT" TAO
# `luu-tru/` LÀ NGOẠI LỆ CÓ CHỦ Ý, và phải khoá cả hai chiều.
# Bản trước cấm luôn `luu-tru/`, nên workflow TỰ CHẶN TRÌNH TỰ CHÍNH NÓ QUY ĐỊNH:
# nhánh `xoa-nhanh` dặn "Tạo tag TRƯỚC (hành động tao-tag), rồi mới xoá" mà `tao-tag`
# lại từ chối đúng không gian tên ấy. ĐO ĐƯỢC 17-08-2026 trên run thật:
#   tao-tag luu-tru/doctor-github-mcp-verdict-6 -> "DỪNG: … Đặt tên khác." (rc=2)
ca "tạo tag luu-tru/ thì QUA (trình tự của chính workflow)" 0 tao-tag luu-tru/x "$SHA_THAT" TAO
ca "tạo tag LUU-TRU/ hoa cũng QUA"        0 tao-tag LUU-TRU/x "$SHA_THAT" TAO
# ...nhưng MỞ TẠO KHÔNG kéo theo MỞ XOÁ. Tag là mỏ neo; xoá nó vẫn cấm tuyệt đối.
ca "mở tạo KHÔNG mở xoá: xoá tag luu-tru/ vẫn DỪNG" 2 xoa-tag luu-tru/x "" XOA GIA_SHA_NHANH="$S_LT" GIA_TAG_SHAS="$S_LT"
# ...và các vùng còn lại KHÔNG được nới theo.
ca "tạo tag claude/ vẫn DỪNG"             2 tao-tag claude/x "$SHA_THAT" TAO
ca "tạo tag codex/ vẫn DỪNG"              2 tao-tag codex/x "$SHA_THAT" TAO
ca "tạo tag dispatcher/ vẫn DỪNG"         2 tao-tag dispatcher/x "$SHA_THAT" TAO
ca "tạo tag mission/ vẫn DỪNG"            2 tao-tag mission/x "$SHA_THAT" TAO
ca "tạo tag agent/ vẫn DỪNG"              2 tao-tag agent/x "$SHA_THAT" TAO
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
      # DONG DAU co nguyen token " 404 " nhung KHONG bat dau bang dong trang thai HTTP.
      # Khoa bien the `*" 404 "*` — reviewer luot 5 do duoc rang no con song khi chua co
      # ca nay. Phai dat o lan doc SAU: o lan doc TRUOC ca `khong` lan `khong-do-duoc`
      # deu cho ra ma 1, nen ca ay khong phan biet duoc hai nhanh.
      [ "${GIA_GET_TOKEN_404:-0}" = "$n" ] && { printf 'gateway 404 unavailable\n'; exit 1; }
      if [ "${GIA_MISSING:-0}" = 1 ] || grep -qxF "$ten" "$DA_XOA"; then
        echo "HTTP/2 404 Not Found"; exit 1
      fi
      echo "HTTP/2 200 OK"; exit 0 ;;
esac
exit 0
GHEOF
chmod +x "$TAM/bin/gh"

# `git` GIẢ — GIỮ TRẠNG THÁI, không diễn kịch bản. Kho này đã trả giá đúng chỗ đó: một
# bản `gh` giả diễn kịch bản từng cho 40/40 trong khi đột biến XOÁ HẲN lệnh phá vẫn qua.
# Ở đây trạng thái là tệp `GIA_REF_STATE` (mỗi dòng `refs/loai/ten <sha>`), và lease
# được cưỡng chế ĐÚNG như git thật: so old-oid, lệch thì `stale info` + rc=1 + ref CÒN.
S1=b4e5c5f9ef85e652fa2cc98bb3474036519d663c
S2=872679c360a43a4b12221749901aa0cf231566ac

cat > "$TAM/bin/git" <<'GITEOF'
#!/usr/bin/env bash
DONG="$*"
echo "git $DONG" >> "${GIA_LOG:-/dev/null}"
case "$DONG" in
  push*--force-with-lease=*)
      lease=$(printf '%s' "$DONG" | tr ' ' '\n' | sed -n 's/^--force-with-lease=//p')
      ref="${lease%%:*}"; mong="${lease##*:}"
      ST="${GIA_REF_STATE:-/dev/null}"
      hien=$(awk -v k="$ref" '$1==k{print $2}' "$ST" 2>/dev/null | tail -1)
      if [ -z "$hien" ]; then
        printf ' ! [remote rejected] (delete) -> %s (no such ref)\n' "${ref##*/}" >&2; exit 1
      fi
      if [ "$hien" != "$mong" ]; then
        printf ' ! [rejected] (delete) -> %s (stale info)\n' "${ref##*/}" >&2; exit 1
      fi
      # GIA_PUSH_KHONG_AN_GI=1: lease KHOP, bao thanh cong, nhung KHONG doi trang thai.
      # Khoa phep "DO LAI sau khi xoa" — khong co no thi mot lenh xoa im lang vo hieu
      # van cho cong xanh.
      if [ "${GIA_PUSH_KHONG_AN_GI:-0}" != 1 ]; then
        grep -v "^$ref " "$ST" > "$ST.tmp" 2>/dev/null; mv "$ST.tmp" "$ST" 2>/dev/null
        printf '%s\n' "${ref#refs/}" >> "${GIA_LOG}.daxoa"
      fi
      printf ' - [deleted]         %s\n' "${ref##*/}"
      exit 0 ;;
esac
exit 0
GITEOF
chmod +x "$TAM/bin/git"

lam() {
  local ten="$1" mong="$2" hd="$3" ref="$4" sha="$5" thu="$6"; shift 6
  : > "$TAM/gialog"; rm -f "$TAM/gialog.daxoa" "$TAM/gialog.sha"
  # Trạng thái ref + tệp ghim MẶC ĐỊNH: mọi ref trong `$ref` đang ở `$S1`, và ghim cũng
  # `$S1` ⇒ lease khớp. Ca nào muốn dựng ĐUA thì tự cấp `GIA_REF_STATE`/`NEO_TEP` khác.
  local loai=heads; [ "$hd" != xoa-nhanh ] && loai=tags
  # #675 B1: do dau tung doi so bang `case`, KHONG `printf | grep -q` — grep khop som + printf an SIGPIPE
  # => pipefail 141 => `!` doi thanh dung => nhanh fallback noi de GIA_REF_STATE/NEO_TEP tuong minh. Khoa: ops/do_sigpipe.sh
  local a mac_ref=1 mac_neo=1
  for a in "$@"; do case "$a" in GIA_REF_STATE=*) mac_ref=0 ;; NEO_TEP=*) mac_neo=0 ;; esac; done
  if [ "$mac_ref" -eq 1 ]; then
    : > "$TAM/refstate"
    local x; IFS=',' read -ra _rr <<< "$ref"
    for x in "${_rr[@]}"; do x="${x//[[:space:]]/}"; [ -n "$x" ] && printf 'refs/%s/%s %s\n' "$loai" "$x" "$S1" >> "$TAM/refstate"; done
    set -- "$@" GIA_REF_STATE="$TAM/refstate"
  fi
  if [ "$mac_neo" -eq 1 ]; then
    : > "$TAM/neo_auto"
    local y; IFS=',' read -ra _r2 <<< "$ref"
    for y in "${_r2[@]}"; do y="${y//[[:space:]]/}"; [ -n "$y" ] && printf '%s %s\n' "$y" "$S1" >> "$TAM/neo_auto"; done
    set -- "$@" NEO_TEP="$TAM/neo_auto"
  fi
  env GIA_LOG="$TAM/gialog" HANH_DONG="$hd" REF="$ref" SHA="$sha" CHI_THU="$thu" \
      GITHUB_REPOSITORY=ducthangho/tra-luat "$@" bash "$TAM/lam.sh" >"$TAM/out" 2>&1
  local rc=$?
  if [ "$rc" = "$mong" ]; then QUA=$((QUA+1)); printf '  QUA   %s\n' "$ten"
  else HONG=$((HONG+1)); printf '  ĐỎ    %s  (rc=%s, mong %s)\n' "$ten" "$rc" "$mong"; sed 's/^/          /' "$TAM/out" | tail -4; fi
}

# Đo THÔNG ĐIỆP của bước làm — phân biệt "từ chối vì lease" với mọi kiểu ĐỎ khác.
doi_ra_lam() {
  local ten="$1" mau="$2"
  if grep -q -- "$mau" "$TAM/out" 2>/dev/null; then QUA=$((QUA+1)); printf '  QUA   %s\n' "$ten"
  else HONG=$((HONG+1)); printf '  ĐỎ    %s  (không thấy %q)\n' "$ten" "$mau"; sed 's/^/          /' "$TAM/out" | tail -3; fi
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

lam "thử khô: KHÔNG gọi gh lần nào"       0 xoa-nhanh 'a,b' ""    true
doi_log "thử khô: nhật ký gh RỖNG"        "." 0

lam "xoá: có trước, mất sau -> XANH"      0 xoa-nhanh a "" false
doi_log "xoá: ĐÚNG MỘT lệnh push có lease" "force-with-lease" 1
doi_log "xoá: lease neo ĐÚNG refs/heads/a" "force-with-lease=refs/heads/a:" 1

lam "xoá HAI ref -> hai lệnh push"        0 xoa-nhanh 'a,b' "" false
doi_log "xoá hai: đếm push có lease = 2"  "force-with-lease" 2

# ═══ GHIM SHA — bước LÀM phải đòi đúng SHA mà bước CHỐT đã đo ═══
# Không có ba ca này thì phép đo tổ-tiên chỉ nói về QUÁ KHỨ: ai đẩy commit mới giữa hai
# bước là commit ấy bị xoá mà chưa từng được đo. Khe ấy KHÔNG đóng được bằng API
# (`DELETE /git/refs` không nhận SHA mong đợi), nên nó phải đóng bằng phép đọc lại.
# ═══ LEASE (CAS) — finding P1 của cross-review lượt 1 trên PR "#213" ═══
# Bản trước đọc lại SHA rồi so rồi mới gọi `DELETE`. Reviewer dựng đồ giả GIỮ TRẠNG THÁI
# cho nhánh nhảy SHA ĐÚNG GIỮA lần đọc cuối và lệnh xoá, và bản ấy XOÁ MẤT commit chưa
# từng được đo. "Đọc lại" THU HẸP khe, KHÔNG đóng nó.
# Nay xoá bằng `git push --force-with-lease=<ref>:<sha ghim>`: old-oid đi TRONG CÙNG giao
# dịch, nên không còn khe nào để chen.
NEO="$TAM/neo_lam.txt"
printf 'ops/da-land %s\n' "$S1" > "$NEO"
printf 'refs/heads/ops/da-land %s\n' "$S1" > "$TAM/rs_khop"
lam "lease KHỚP -> XANH"                  0 xoa-nhanh ops/da-land "" false NEO_TEP="$NEO" GIA_REF_STATE="$TAM/rs_khop"
doi_log "…và CÓ push có lease đúng 1 lần" "force-with-lease" 1

# ĐÂY LÀ CA CỦA REVIEWER: ghim đo được `S1`, nhưng lúc xoá nhánh đã ở `S2`.
printf 'refs/heads/ops/da-land %s\n' "$S2" > "$TAM/rs_lech"
lam "nhánh nhảy SHA giữa ĐO và XOÁ -> ĐỎ" 1 xoa-nhanh ops/da-land "" false NEO_TEP="$NEO" GIA_REF_STATE="$TAM/rs_lech"
doi_ra_lam "…và git từ chối vì stale info" "stale info"
if grep -qxF "refs/heads/ops/da-land $S2" "$TAM/rs_lech"; then
  QUA=$((QUA+1)); printf '  QUA   %s\n' "…và ref VẪN CÒN, không bị xoá"
else
  HONG=$((HONG+1)); printf '  ĐỎ    %s\n' "…và ref VẪN CÒN, không bị xoá"
fi

# MỌI ref sắp xoá đều cần ghim, không riêng vùng làm việc: không có giá trị kỳ vọng thì
# không dựng được lease, mà xoá không lease là quay lại đúng lỗ vừa vá.
: > "$TAM/neo_rong.txt"
lam "KHÔNG có ghim -> ĐỎ (vùng làm việc)" 1 xoa-nhanh ops/da-land "" false NEO_TEP="$TAM/neo_rong.txt"
doi_log "…và KHÔNG push"                 "force-with-lease" 0
lam "KHÔNG có ghim -> ĐỎ (ref thường)"    1 xoa-nhanh tmp-thuong "" false NEO_TEP="$TAM/neo_rong.txt"
doi_log "…và KHÔNG push"                 "force-with-lease" 0

lam "xoá TAG: đi đường refs/tags"         0 xoa-tag t1 "" false
doi_log "xoá tag: lease neo refs/tags/t1" "force-with-lease=refs/tags/t1:" 1

lam "xoá: ref không tồn tại -> ĐỎ"        1 xoa-nhanh a "" false GIA_MISSING=1
doi_log "không tồn tại: KHÔNG push"      "force-with-lease" 0

lam "xoá: đọc TRƯỚC lỗi 500 -> ĐỎ"        1 xoa-nhanh a "" false GIA_GET_ERR=1
doi_log "lỗi đọc trước: KHÔNG push"      "force-with-lease" 0

lam "xoá: push báo XANH mà ref VẪN CÒN -> ĐỎ" 1 xoa-nhanh a "" false GIA_PUSH_KHONG_AN_GI=1
lam "xoá: đọc SAU lỗi 500 -> ĐỎ (fail-close)" 1 xoa-nhanh a "" false GIA_GET_ERR=2
lam "xoá: 500 mà thân có chữ Not Found -> vẫn ĐỎ" 1 xoa-nhanh a "" false GIA_GET_500_NOTFOUND=2
lam "xoá: 500-có-Not-Found ở lần đọc TRƯỚC -> ĐỎ" 1 xoa-nhanh a "" false GIA_GET_500_NOTFOUND=1
lam "xoá: 500 có DÒNG THÂN giả mạo 404 -> vẫn ĐỎ" 1 xoa-nhanh a "" false GIA_GET_500_GIA_DONG_404=2
lam "xoá: dòng thân giả 404 ở lần đọc TRƯỚC -> ĐỎ" 1 xoa-nhanh a "" false GIA_GET_500_GIA_DONG_404=1
lam "xoá: dòng ĐẦU có chữ 404 mà là 500 -> ĐỎ" 1 xoa-nhanh a "" false GIA_GET_500_CO_CHU_404=2
lam "xoá: dòng đầu có chữ 404, lần đọc TRƯỚC -> ĐỎ" 1 xoa-nhanh a "" false GIA_GET_500_CO_CHU_404=1
lam "xoá: dòng đầu 'gateway 404 unavailable' -> ĐỎ" 1 xoa-nhanh a "" false GIA_GET_TOKEN_404=2

lam "tạo tag: đúng sha -> XANH"           0 tao-tag v1 "$S1" false
lam "tạo tag: API trả sha KHÁC -> ĐỎ"     1 tao-tag v1 "$S1" false GIA_TAG_SHA="$S2"
lam "tạo tag: hai cặp KHÁC sha, ghép đúng" 0 tao-tag 'v1,v2' "$S1,$S2" false
lam "tạo tag: phần tử rỗng giữa, vẫn ghép đúng" 0 tao-tag 'a,,b' "$S1,,$S2" false
lam "tạo tag: số cặp lệch sau khi nén -> ĐỎ" 1 tao-tag 'a,b' "$S1" false

# ================= GITHUB CO NHAN TEP NAY KHONG =================
# BAI HOC DAT NHAT CUA CA DOT NAY. Sau luot cross-review deu ket luan "YAML ok" — vi ca
# sau chi kiem bang PyYAML. Nhung GitHub NOI SUY BIEU THUC tren toan bo than `run` TRUOC
# khi shell thay no, nen mot cap dau ngoac kep-kep RONG nam trong mot dong CHU THICH la
# mot bieu thuc RONG => tep workflow KHONG HOP LE, GitHub tu choi truoc khi chay job nao.
# Lan chay dau tien tren GitHub tra ve mot "workflow run" mang ten DUONG DAN TEP, 0 job,
# conclusion=failure — chu khong phai mot job do.
#
# Nen o day goi trinh kiem THAT (actionlint). Neu khong co no thi KHONG im lang bo qua:
# in KHONG DO DUOC va tra ma khac 0, vi mot cong tu tat khi thieu cong cu la cong khong
# ton tai — dung luc no can nhat.
echo
if command -v actionlint >/dev/null 2>&1; then
  AL=actionlint
elif [ -x "${ACTIONLINT:-}" ]; then
  AL="$ACTIONLINT"
else
  AL=""
fi
if [ -n "$AL" ]; then
  if "$AL" -shellcheck= -pyflakes= "$YML"; then
    QUA=$((QUA+1)); echo "  QUA   actionlint: GitHub nhận tệp workflow này"
  else
    HONG=$((HONG+1)); echo "  ĐỎ    actionlint bắt lỗi ở trên"
  fi
else
  HONG=$((HONG+1))
  echo "  ĐỎ    KHÔNG ĐO ĐƯỢC: thiếu actionlint, không kiểm được GitHub có nhận tệp không."
  echo "        Cài: https://github.com/rhysd/actionlint/releases  ·  hoặc đặt ACTIONLINT=<đường dẫn>"
fi

TONG=$((QUA+HONG))
echo
echo "don_ref: $QUA/$TONG đạt (chốt + bước làm)"
[ "$HONG" = 0 ] || exit 1
