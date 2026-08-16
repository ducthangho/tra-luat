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
"$PY" - "$YML" "$TAM/chot.sh" <<'PYEOF'
import sys, yaml
from pathlib import Path
d = yaml.safe_load(Path(sys.argv[1]).read_text(encoding="utf-8"))
steps = d["jobs"]["don"]["steps"]
# Bước CHỐT nhận diện bằng biến môi trường nó đọc, không bằng CHỈ SỐ: chèn thêm một
# bước vào đầu workflow sẽ làm chỉ số cứng trỏ nhầm mà test vẫn xanh.
chot = [s for s in steps if "XAC_NHAN" in (s.get("env") or {})]
assert len(chot) == 1, f"mong dung MOT buoc doc XAC_NHAN, thay {len(chot)}"
Path(sys.argv[2]).write_text("#!/usr/bin/env bash\n" + chot[0]["run"], encoding="utf-8")
PYEOF
[ -s "$TAM/chot.sh" ] || { echo "khong trich duoc buoc chot"; exit 1; }

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
ca "tạo tag: sha sai dạng thì DỪNG"       2 tao-tag v1 "abc" TAO
ca "tạo tag: sha CHỮ HOA thì DỪNG"        2 tao-tag v1 "B4E5C5F9EF85E652FA2CC98BB3474036519D663C" TAO
ca "tạo tag: lệch số lượng thì DỪNG"      2 tao-tag 'v1,v2' "$SHA_THAT" TAO
ca "tạo tag hợp lệ thì QUA"               0 tao-tag v1 "$SHA_THAT" TAO
ca "tạo tag: hai cặp khớp thì QUA"        0 tao-tag 'v1,v2' "$SHA_THAT,$SHA_THAT" TAO

TONG=$((QUA+HONG))
echo
echo "don_ref_chot: $QUA/$TONG đạt"
[ "$HONG" = 0 ] || exit 1
