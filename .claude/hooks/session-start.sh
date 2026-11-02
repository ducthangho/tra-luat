#!/bin/bash
# SessionStart — dựng đủ công cụ cho phiên chạy trên Claude Code web/remote.
#
# VÌ SAO: container phiên remote ĐÃ ĐO (12-08-2026) có python/git/node/claude
# nhưng KHÔNG có codex, gh, pwsh. Thiếu công cụ mà chỉ lộ ra giữa chừng thì lượt
# chạy hỏng ở chỗ khó đọc; dựng sẵn ở đây thì hỏng ở chỗ dễ đọc.
#
# KHÔNG tự viết script spawn agent. Hook này CHỈ cài CLI CHÍNH THỨC
# (@openai/codex, @anthropic-ai/claude-code) rồi để launcher.py bọc chốt quanh
# chúng. Mọi việc gọi agent đi qua đúng hai CLI đó.
#
# Chạy thử tay:  CLAUDE_CODE_REMOTE=true ./.claude/hooks/session-start.sh
#
# ------------------------------------------------------------------------------------
# hook-nang-luc: codex-auth-restore rg-bat-buoc doctor-kha-dung pip-bang-chung-duong codex-env-policy codex-env-policy-thu-hoi codex-env-policy-fail-close codex-env-policy-chi-doc co-chay-probe moi-truong-doc-truoc github-nguon-that pip-bang-chung-import rg-windows-khong-tu-cai rg-co-chay-truoc-cargo agent-creds-bootstrap agy-ghim
# ------------------------------------------------------------------------------------
# DÒNG TRÊN LÀ HỢP ĐỒNG, KHÔNG PHẢI CHÚ THÍCH. `launcher.py doctor` (mục `hook-phien`)
# đọc nó ở CẢ hook đang checkout LẪN hook trên `origin/master`, rồi báo động khi bản
# đang chạy THIẾU năng lực mà master đã có.
#
# VÌ SAO KHÔNG SO BĂM TOÀN TỆP: bản trước làm vậy và cross-review bác đúng — sửa một
# dấu phẩy trong chú thích cũng làm chốt đỏ, mà chốt đỏ vì lý do vô hại là chốt sẽ bị
# bỏ qua. Cái cần biết không phải "hai tệp có khác nhau không" mà là "bản đang chạy có
# THIẾU thứ gì không".
#
# VÌ SAO KHÔNG DÙNG QUAN HỆ TỔ TIÊN COMMIT: reviewer nêu thẳng và đúng — chính nhánh
# packet CŨ mới là thứ cần cảnh báo, mà nó LÀ tổ tiên hợp lệ của master. Tổ tiên tính
# không phân biệt được "cũ nhưng đủ" với "cũ và thiếu".
#
# THÊM NĂNG LỰC MỚI thì thêm TÊN vào dòng trên. Quên thêm thì phiên chạy nhánh cũ sẽ
# không được cảnh báo về đúng thứ vừa thêm — đó là cách hỏng duy nhất của cơ chế này,
# và nó hỏng IM LẶNG. Tên đặt theo NĂNG LỰC, đừng theo số phiên bản: số thì phải nhớ
# tăng, còn tên thì tự nói nó là gì khi báo động.
set -euo pipefail

# Keep the snapshot in an unexported shell variable before ANY external command.
unset TL_CODEX_SNAPSHOT
TL_CODEX_SNAPSHOT="${CODEX_AUTH_JSON:-}"
unset CODEX_AUTH_JSON
CODEX_AUTH_CO=0; [ -n "$TL_CODEX_SNAPSHOT" ] && CODEX_AUTH_CO=1

GOC="${CLAUDE_PROJECT_DIR:-$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)}"
ghi_dau_vet_hook() {
  local nhan="${1:-chay}"
  for d in "$GOC/.claude/.packet_state" "$GOC/.tl_state"; do
    if mkdir -p "$d" 2>/dev/null; then
      printf "%s %s\n" "$(date -u +"%Y-%m-%dT%H:%M:%SZ")" "$nhan" > "$d/session-start.ran" 2>/dev/null || true
      return 0
    fi
  done
  return 1
}

# Chỉ chạy trong môi trường remote. Máy cá nhân đã có sẵn công cụ theo ý người
# dùng; cài đè vào đó là vượt quyền.
if [ "${CLAUDE_CODE_REMOTE:-}" != "true" ]; then
  ghi_dau_vet_hook "cuc_bo" || true
  echo "[session-start] khong phai moi truong remote — bo qua"
  exit 0
fi

ghi_dau_vet_hook "remote" || echo "[session-start] CANH BAO: khong ghi duoc dau vet hook"
PATH_GOC="$PATH"   # chup PATH cua PHIEN truoc khi hook tu noi PATH cho rieng no
cd "$GOC"

# M4 / L4: Cưỡng chế UTF-8 tránh lỗi cp1258/charmap trên Windows (source hook de co o shell cha)
export PYTHONUTF8=1
export PYTHONIOENCODING=utf-8

# M4 / A4: Ghim phiên bản actionlint đồng bộ với 5 chỗ trong .github/workflows/ci.yml
AL_VER="1.7.7"

# `command -v` chứ không `which`: có sẵn ở mọi shell POSIX và không phụ thuộc gói ngoài.
co() { command -v "$1" >/dev/null 2>&1; }

# Interpreter dùng cho mọi probe bên dưới. Windows KHÔNG có `python3`, nên nhận cả
# hai tên; thiếu cả hai thì DỪNG — hook không probe được thì mọi kết luận sau đó
# chỉ là phỏng đoán, và một hook đoán còn tệ hơn hook không chạy.
if co python3; then PY=python3
elif co python; then PY=python
else
  echo "[session-start] HONG: khong co python/python3 de probe"
  exit 1
fi

# wp484 g7 (Codex lượt 1 F04): khối materialize snapshot đã DỜI xuống ngay SAU bước cài CLI agent.
# Snapshot mới cần probe bằng `codex` thật; đặt ở đây thì máy chưa có `codex` chết rc=13 TRƯỚC
# `npm install` và không bao giờ tự phục hồi được. `TL_CODEX_SNAPSHOT` là biến shell KHÔNG export
# nên installer và mọi lệnh ở giữa không thấy nó.

# CÓ MẶT ≠ CHẠY ĐƯỢC. `command -v` chỉ chứng minh có đường dẫn: audit dựng hai tệp
# RỖNG tên git.exe/python.exe mà doctor vẫn báo xanh, và trên Windows `rg.exe` nằm
# trong PATH nhưng chạy ra "Access is denied". Probe thật: có timeout, đòi rc=0 VÀ
# có đầu ra — rc=0 mà im lặng là đúng chữ ký của "chạy nhưng chẳng làm gì" (r244).
co_chay() {
  local duong
  duong="$(command -v "$1" 2>/dev/null || true)"
  [ -n "$duong" ] || return 1
  "$PY" -c 'import subprocess,sys
try:
 p=subprocess.run([sys.argv[1],"--version"],capture_output=True,text=True,timeout=8)
except (OSError,subprocess.SubprocessError):
 raise SystemExit(1)
raise SystemExit(0 if p.returncode == 0 and (p.stdout+p.stderr).strip() else 1)' "$duong"
}

# --- ĐỌC BIẾN MÔI TRƯỜNG TRƯỚC KHI KẾT LUẬN VỀ CÔNG CỤ (bài học 15-08-2026).
# Chỉ giữ TRẠNG THÁI và NGUỒN; tuyệt đối không echo giá trị credential.
#
# Thứ tự chọn CỐ Ý KHÁC tài liệu của gh, và lý do đo được 17-08-2026: trong
# container này `GH_TOKEN` `GITHUB_TOKEN` `AWS_*` `CLOUDSDK_*` mang CÙNG một chuỗi
# giữ chỗ 14 ký tự, còn credential thật nằm ở `GITHUB_PAT` (93 ký tự). Lấy
# `GH_TOKEN` trước là xuất khẩu đúng bản giữ chỗ, rồi `gh` báo "sai thông tin đăng
# nhập" thay vì "chưa đăng nhập" — biến giữ chỗ TỆ HƠN biến chưa đặt.
# Dấu hiệu máy đọc được: "token GitHub" mà TRÙNG BYTE với một biến chẳng liên quan
# tới GitHub thì không phải credential. So bằng băm để không giá trị nào bị in ra.
# Luật này phải GIỐNG `_doc_moi_truong` trong launcher.py — hai bản của cùng một
# quy tắc sẽ trôi lệch, và bên quên cập nhật chính là bên đẩy lọt.
GITHUB_AUTH_SOURCE="$(
  "$PY" -c '
import hashlib, os, secrets
khoa = secrets.token_bytes(16)
def vt(v): return hashlib.blake2s(v.encode("utf-8","replace"), key=khoa).hexdigest()
ngoai = {vt(os.environ[t]) for t in
         ("AWS_ACCESS_KEY_ID","AWS_SECRET_ACCESS_KEY","CLOUDSDK_AUTH_ACCESS_TOKEN")
         if os.environ.get(t)}
for ten in ("GH_TOKEN","GITHUB_TOKEN","GITHUB_PAT"):
    v = os.environ.get(ten)
    if v and vt(v) not in ngoai:
        print(ten); break
else:
    print("none")'
)"
case "$GITHUB_AUTH_SOURCE" in
  none)
    # Thà KHÔNG có còn hơn có bản giữ chỗ.
    unset GH_TOKEN GITHUB_TOKEN 2>/dev/null || true ;;
  GH_TOKEN) : ;;
  *)
    # `gh` không đọc tên biến lịch sử `GITHUB_PAT`. Ánh xạ trong tiến trình hook,
    # không ghi token xuống đĩa và không in giá trị.
    eval "export GH_TOKEN=\"\${$GITHUB_AUTH_SOURCE}\"" ;;
esac
echo "[session-start] moi truong: da doc truoc tool; GitHub auth source=$GITHUB_AUTH_SOURCE; CODEX_AUTH_JSON present=$CODEX_AUTH_CO"

echo "[session-start] goc du an: $GOC"

# --- CLI agent chính thức. Idempotent: đã có thì không đụng (container được
# cache sau khi hook xong, nên lần sau vào thẳng).
if co npm; then
  if ! co_chay codex; then
    echo "[session-start] cai @openai/codex ..."
    npm install -g @openai/codex >/dev/null 2>&1 || echo "[session-start] CANH BAO: cai codex that bai"
  fi
  if ! co_chay claude; then
    echo "[session-start] cai @anthropic-ai/claude-code ..."
    npm install -g @anthropic-ai/claude-code >/dev/null 2>&1 || echo "[session-start] CANH BAO: cai claude that bai"
  fi
else
  echo "[session-start] CANH BAO: khong co npm — bo qua phan CLI agent"
fi

# Only the trusted repository materializer receives the raw snapshot — chạy SAU khi đã cố cài
# `codex` (F04) nhưng vẫn TRƯỚC mọi probe credential phía dưới.
if [ "$CODEX_AUTH_CO" = 1 ]; then
  MA_AUTH=0
  CODEX_AUTH_JSON="$TL_CODEX_SNAPSHOT" "$PY" .claude/dev/launcher.py chuan-bi || MA_AUTH=$?
  unset TL_CODEX_SNAPSHOT
  if [ "$MA_AUTH" != 0 ]; then
    echo "[session-start] CHO snapshot Codex moi; dung truoc cac probe"
    exit 13
  fi
else
  unset TL_CODEX_SNAPSHOT
fi

# --- ripgrep: cả codex lẫn Claude Code đều gọi `rg` để tìm trong mã. Thiếu nó thì
# lệnh tìm gãy giữa chừng chứ KHÔNG tự lùi về grep — phiên mất khả năng tra cứu mà
# không hỏng ở chỗ đọc được. Vì thế `rg` là BAT BUOC trong `doctor` từ 15-08-2026.
#
# Ba đường cài, thử lần lượt: apt-get (có/không sudo), rồi cargo. Không đường nào
# chạy thì nói THẲNG là phiên sẽ thiếu — đừng để nó lộ ra giữa chừng.
#
# wp802 (Q4): Windows (Git Bash) KHÔNG có apt-get và thường vắng cargo — hook KHÔNG tự cài ở
# đó: in ĐÚNG MỘT lệnh rồi để `doctor` chặn (thoát 12). Chuỗi dưới PHẢI khớp `rg.cai.windows`
# của ops/cong_cu.yaml (phần trước ` && ` đầu tiên) — canh: `r802_bang_cai_rg_khop_cong_cu_yaml`.
RG_CAI_WINDOWS='winget install --id BurntSushi.ripgrep.MSVC -e --accept-source-agreements --accept-package-agreements --disable-interactivity || choco install ripgrep --yes --no-progress'
RG_WIN=0; case "$(uname -s 2>/dev/null || true)" in MINGW*|MSYS*|CYGWIN*) RG_WIN=1 ;; esac
if [ "$RG_WIN" = 1 ]; then   # chọn nền TRƯỚC probe: Windows probe ĐÚNG MỘT lần (Codex lượt 2 F5)
  co_chay rg || { echo "[session-start] CANH BAO: rg THIEU/HONG (Windows) — hook KHONG tu cai; doctor se chan. Cai bang:"
                  echo "$RG_CAI_WINDOWS"; }
elif ! co_chay rg; then
  echo "[session-start] cai ripgrep ..."
  if co apt-get; then
    apt-get install -y -qq ripgrep >/dev/null 2>&1 \
      || sudo apt-get install -y -qq ripgrep >/dev/null 2>&1 \
      || { apt-get update -qq >/dev/null 2>&1 || sudo apt-get update -qq >/dev/null 2>&1; \
           apt-get install -y -qq ripgrep >/dev/null 2>&1 \
           || sudo apt-get install -y -qq ripgrep >/dev/null 2>&1; } \
      || true
  fi
  # wp802 (M3): `co_chay`, KHÔNG `co` — `rg` có mặt mà hỏng thì `co rg` đúng, bỏ mất cargo.
  co_chay rg || { co cargo && cargo install ripgrep >/dev/null 2>&1 || true; }
  # BANG CHUNG DUONG: `command -v` la CO MAT, `rg --version` la CHAY DUOC. Audit
  # codex tung dung hai tep RONG ten git.exe/python.exe roi doctor bao xanh.
  if rg --version >/dev/null 2>&1; then
    echo "[session-start] rg: $(rg --version | head -1)"
  else
    echo "[session-start] CANH BAO: KHONG cai duoc rg — tra cuu ma se gay giua chung"
  fi
fi

# --- actionlint (M4 / L2): cài actionlint bản ghim để kiểm tra workflow GitHub Actions
if ! co_chay actionlint; then
  echo "[session-start] cai actionlint $AL_VER ..."
  AL_DICH="${HOME}/.local/bin"
  mkdir -p "$AL_DICH" 2>/dev/null || AL_DICH="/tmp/actionlint"
  if AL_VER="$AL_VER" AL_DICH="$AL_DICH" bash "$GOC/ops/cai_actionlint.sh" >/dev/null 2>&1; then
    export PATH="$AL_DICH:$PATH"
    if env -u PATH PATH="$PATH_GOC" command -v actionlint >/dev/null 2>&1; then
      echo "[session-start] actionlint: $(actionlint --version 2>/dev/null | head -1)"
    else
      echo "[session-start] CANH BAO: da cai actionlint vao $AL_DICH nhung PHIEN KHONG thay no (chua co trong PATH)"
    fi
  else
    echo "[session-start] CANH BAO: KHONG cai duoc actionlint — kiem tra GitHub Actions workflow se gay giua chung"
  fi
fi

# --- KHONG cai `gh`. Da DO 15-08-2026: REST truc tiep toi api.github.com bi PROXY
# tra 403 ("GitHub access is not enabled for this session") BAT KE token — `GITHUB_PAT`
# that cung 403, `/user` lai 200, tuc chinh sach theo DUONG DAN chu khong theo danh
# tinh. Nen `gh` co cai cung khong dung duoc cho viec cua kho. Duong DUNG: cong cu
# MCP github (dang comment/doc issue) va git over HTTPS (day/keo). `doctor` in ro
# duong nao mo, de khong ai ket luan "GitHub khong goi duoc" tu duong hong.

# --- phụ thuộc Python của kho
# (`PY` đã được chọn Ở ĐẦU tệp, cùng chỗ với `co_chay`. Trước đây nó được gán LẠI
# ở đây; hai chỗ gán cùng một biến là hai bản của một quy tắc, và bản dưới sẽ âm
# thầm thắng bản trên nếu ai đó sửa một bên. Giữ đúng MỘT chỗ chọn interpreter.)
# Chi cai lai khi requirements.txt DOI. Audit codex: hook chay pip moi lan
# SessionStart la khong idempotent that su - vua cham vua co the keo ve ban khac
# (pypdf>=4.0 khong ghim tran).
#
# Audit vong 3 - dau moc la BANG CHUNG AM ("tung cai sha nay"), khong phai bang
# chung DUONG ("goi dang co"). Do duoc hai ca sai:
#   A->B->A : buoc 3 BO QUA vi moc cua A con, trong khi moi truong dang la B.
#   hai du an khac nhau, requirements.txt GIONG HET, chung TMPDIR: du an sau bo
#   qua du chua bao gio cai o do (sai han khi moi du an mot venv).
# Sua hai chuyen: (1) moc neo theo CA sha LAN sys.prefix (venv nao), va nam trong
# .git/ cua du an chu khong phai TMPDIR dung chung; (2) truoc khi tin moc, DOI
# BANG CHUNG DUONG. Ban dau lay `pip install --dry-run` lam bang chung — SAI, xem
# r337 ngay duoi: dry-run tra rc=0 ke ca khi "Would install", nen no khong bao thieu
# bao gio. Bang chung duong nay la IMPORT DUOC tung goi trong requirements.txt.
if [ -f requirements.txt ]; then
  KHO_MOC="$("$PY" -c "import subprocess,sys;print(subprocess.run(['git','rev-parse','--git-dir'],capture_output=True,text=True).stdout.strip() or '.')" 2>/dev/null || echo .)"
  # VAN TAY phai bao gom CA TEP DUOC INCLUDE (r345). Ban truoc bam MOI tep ngoai, nen
  # `-r extra.txt` sua noi dung ma bam khong doi ⇒ moc con hieu luc ⇒ hook bo qua cai dat
  # mai mai. Theo `-r`/`-c` de quy, giai duong TUONG DOI theo tep CHUA no, va chan chu
  # trinh bang tap da tham. Doc khong duoc mot tep include ⇒ dua CHINH DUONG DAN vao bam
  # (KHONG DO DUOC != giong nhau): tep xuat hien lai sau nay se doi bam.
  # r351 — NGUNG BAT CHUOC CU PHAP PIP. Doc ky truoc khi "them lai cho day du".
  #
  # Hinh dang loi nay lap LAN THU HAI. Lan mot (r338-r341, 5 finding): tu phan tich DONG
  # REQUIREMENT ⇒ chua bang cach uy quyen cho pip. Lan hai (r347/r349/r350 + vong 10,
  # ~7 finding): tu phan tich CHI THI INCLUDE — chu thich, noi dong, bien moi truong,
  # symlink, va cham bam. Moi vong vá xong lai lo ra mot luat cua pip ma ta chua chep
  # dung: `expand_env_variables` chi nhan `${UPPER}` va bo gia tri rong · `join_lines`
  # dung `strip(backslash)` chu khong bo mot ky tu · `realpath` gop lam mat mot nhanh
  # symlink · va chuoi 'KHONG_DOC_DUOC' trong tep that trung voi trang thai tep bi xoa.
  #
  # Lan nay KHONG uy quyen duoc: phep bam phai chay OFFLINE, ma pip thi khong.
  # Nen cach dung la NGUNG DOAN: neu requirements.txt co BAT KY dong chi thi nao thi ta
  # KHONG DU SUC noi "khong doi", va phai noi thang thay vi doan cho ra ve chinh xac.
  #
  # r352 — luat tho lan mot con THUNG: pip GIAI BIEN MOI TRUONG TRUOC khi phan tich
  # option, nen mot dong `${INCLUDE}` voi `INCLUDE='-r extra.txt'` keo duoc tep khac
  # vao trong khi ky tu dau la dola chu khong phai gach ngang. Do duoc: pip keo
  # `extra.txt`, luat cu tra 0. Chua bang cach THO HON — dong nao CHUA dau dola cung
  # tinh la co chi thi. Khong doc gia tri bien, khong chep luat `${UPPER}` cua pip:
  # chep luat chinh la thu da hong bay lan.
  #
  # Phep do rat tho — ky tu dau khong-trang la '-', hoac dong co dola — va tho CO CHU
  # DICH: no khong can biet cu phap pip. Mot dong chu thich '# -r x' bi tinh nham chi la
  # chay pip thua mot lan; chieu sai duy nhat cua no la AN TOAN. Doi lay: ca lop loi
  # "chep sai luat cua pip" chet theo KIEN TRUC, khong con nhanh nao de vá.
  #
  # GIA PHAI TRA, khai thang: kho nao DUNG `-r`/`-c`/`-e` se chay pip MOI lan mo phien
  # (mat moc). Kho nay khong dung chi thi nao nen gia o day bang KHONG — do duoc bang
  # chinh phep kiem ben duoi.
  KQ_VT="$( "$PY" -c "
import hashlib, sys
noi_dung = open('requirements.txt','rb').read()
h = hashlib.sha256(noi_dung).hexdigest()[:16]
tien_to = hashlib.sha256(sys.prefix.encode()).hexdigest()[:8]
co = any(d.lstrip().startswith(b'-') or b'\x24' in d
         for d in noi_dung.splitlines())
print(h + '_' + tien_to + ' ' + ('1' if co else '0'))" )"
  VAN_TAY="${KQ_VT%% *}"
  CO_CHI_THI="${KQ_VT##* }"
  DAU="$KHO_MOC/.tl_reqs_$VAN_TAY"
  # BANG CHUNG DUONG = IMPORT DUOC, khong phai `pip install --dry-run` (r337, do 02-09-2026).
  # Ban truoc tin ma thoat cua dry-run: no tra rc=0 KE CA khi in "Would install cffi-2.1.1"
  # (pip 24.0 — dry-run chi that bai khi KHONG GIAI DUOC phu thuoc), nen chot ay chua bao gio
  # noi "thieu"; hook in "moi truong con khop" roi bo qua pip mai. Va ke ca khi pip du, goi
  # co mat van co the KHONG NAP DUOC: pypdf 6.16.2 co mat ma `import pypdf` chet PanicException
  # vi cryptography he thong thieu _cffi_backend — duong nap PDF hong ma khong ai biet toi luc
  # `tl doctor` (luc do cung chet theo). Cung benh "CO MAT != DUNG DUOC" cua `co_chay`, doi
  # doi tuong tu binary sang module. Ten module = ten goi da chuan hoa (pypdf, cffi); bat
  # BaseException vi PanicException KHONG phai Exception; chi cho KeyboardInterrupt xuyen qua.
  reqs_import_duoc() {
    "$PY" - "$@" <<'PYEOF'
import re, sys

# r345 — BO HAN PHEP HOI PIP. Doc ky truoc khi "khoi phuc cho chac".
#
# Bay luot review ra MUOI BA finding. Nam vong dau cung mot hinh dang (ta tu lam thay
# pip), nen r342 uy quyen cho pip. Ba vong sau lai cung mot hinh dang KHAC: moi cach
# lam cho phep hoi ay AN TOAN deu thua.
#   r343: `--no-index` khong chan direct reference ⇒ host chet lam moi phien cham 8,5s.
#   r344: danh sach CAM (`@ scheme://`) lot URL TRAN va `git+https://`.
#   r345: va day la PHAN CHUNG giet ca thiet ke — mot goi DA CAI co `Requires-Dist:
#         childpkg @ http://.../x.whl` khien pip di lay URL do NGAY CA khi tep
#         requirements.txt chi co mot dong TRAN. Do truc tiep: dung mot socket lang
#         nghe va DEM ket noi ⇒ **1 ket noi**. Tuc KHONG THE bao dam offline bang cach
#         soi tep requirements — thu quyet dinh nam trong metadata cua goi da cai.
#
# Do khong phai khe ho va duoc; do la phan chung cho BAO DAM cua thiet ke. Nen phep hoi
# pip bi BO, va ca lop rui ro "mo phien cham vi mang" chet theo KIEN TRUC chu khong theo
# ban va: khong con subprocess nao, khong con duong mang nao.
#
# Con lai la ba phep do CUC BO, deu offline theo cau tao:
#   1. BAN da cai co thoa specifier khong  — `importlib.metadata` + `SpecifierSet`.
#   2. Goi co CON DO khong                 — `distribution()`; VANG MAT la hong.
#   3. `import` co chay khong              — lop loi r337 ma pip khong bao gio thay
#      (goi du, dung ban, ma pyo3 nem PanicException).
#
# KHAI THANG THU DA MAT: khong con phep giai phu thuoc cua pip, nen extras sau va
# `-r` long nhau khong duoc kiem noi dung. Bu lai o cho khac: VAN_TAY nay bam CA cac tep
# `-r`/`-c` (xem khoi tren), nen sua tep include se lam moc het hieu luc va pip that su
# chay lai. Doi mot phep do KHONG BAO DAM DUOC lay mot phep do BAO DAM DUOC.
kiem_ban = "--kiem-ban" in sys.argv[1:]
hong = []

_Req = _Spec = None
for _m in ("packaging", "pip._vendor.packaging"):
    # `packaging` tran KHONG co trong venv tran (do 06-09-2026); ban vendor cua pip thi
    # co o CA HAI nen — ma hook nay von da doi pip. Do la ly do co duong lui.
    try:
        _Req = __import__(_m + ".requirements", fromlist=["Requirement"]).Requirement
        _Spec = __import__(_m + ".specifiers", fromlist=["SpecifierSet"]).SpecifierSet
        break
    except ImportError:
        _Req = _Spec = None

# IMPORT RIENG TUNG TEN, khong gop mot cau. Tren Python 3.8/3.9 `packages_distributions`
# chua co nhung `distribution` DA co; gop chung mot `from ... import a, b` lam nhanh
# `except ImportError` vut luon `distribution` ⇒ phep kiem VANG MAT im lang bien mat
# tren dung cac nen ma ta co y ho tro.
try:
    from importlib.metadata import distribution as _dist
except ImportError:
    _dist = None
try:
    from importlib.metadata import version as _ban
except ImportError:
    _ban = None
try:
    from importlib.metadata import packages_distributions
except ImportError:                 # Python < 3.10
    packages_distributions = None

# pip chi coi `#` la chu thich khi no o DAU DONG hoac di sau KHOANG TRANG; `#` giua mot
# chuoi (marker, fragment cua URL) la ky tu HOP LE. Chep LUAT cua pip, KHONG import
# `pip._internal` — API khong on dinh, buoc hook vao do la doi mot lop troi lay lop khac.
_CHU_THICH = re.compile(r"(^|\s)#.*$")

# r347 — DUONG LUI CHO Python 3.8/3.9. `packages_distributions` chi co tu 3.10, nen tren
# hai nen ta CO Y ho tro thi `ban_do` rong ⇒ vong tham import khong tham gi ca ⇒ lop bao
# ve r337 (goi du, dung ban, ma `import` chet) BIEN MAT IM LANG. Do duoc: gia lap bo
# `packages_distributions` roi pha `pypdf/__init__.py` ⇒ chot tra 0 thay vi 1.
def _module_cua(ten_goi):
    """Tap module top-level cua mot dist, KHONG can `packages_distributions`."""
    if _dist is None:
        return set()
    try:
        d = _dist(ten_goi)
    except KeyboardInterrupt:
        raise
    except BaseException:
        return set()
    try:
        tl = d.read_text("top_level.txt")
    except KeyboardInterrupt:
        raise
    except BaseException:
        tl = None
    if tl:
        return {x.strip() for x in tl.splitlines() if x.strip() and not x.startswith("_")}
    ra = set()
    try:
        tep = d.files or ()
    except KeyboardInterrupt:
        raise
    except BaseException:
        tep = ()
    for f in tep:
        dau = str(f).replace("\\", "/").split("/")[0]
        if dau.endswith(".py"):
            dau = dau[:-3]
        # `isidentifier()` la chot QUYET DINH, khong phai lam dep: RECORD cua mot goi
        # CHI CO CLI ghi duong kieu `../../../bin/clix`, nen doan dau la `..` — khong
        # bat dau bang gach duoi, khong trung hau to nao — va ban truoc di
        # `__import__("..")` roi bao BAO DONG GIA. Do duoc truoc khi va: rc=1 cho mot
        # moi truong HOAN TOAN DUNG. Ten module hop le luon la mot dinh danh Python.
        if (dau and dau.isidentifier() and not dau.startswith("_")
                and not dau.endswith((".dist-info", ".data", ".egg-info", ".pth"))):
            ra.add(dau)
    return ra


ban_do = {}
if packages_distributions is not None:
    for _mod, _dists in packages_distributions().items():
        # BO module gach duoi: chung la ban tang toc TUY CHON. Phan chung: PyYAML khai ca
        # `_yaml` (C ext cua libyaml), ma `yaml/__init__.py` boc no trong
        # `try: from .cyaml import * / except ImportError` — chan `_yaml` roi `import yaml`
        # VAN OK. Doi `_yaml` la bao gia tren may cai PyYAML thuan Python.
        if _mod.startswith("_"):
            continue
        for _d in _dists:
            ban_do.setdefault(_d.lower().replace("-", "_"), set()).add(_mod)

if _Req is not None:
    for dong in open("requirements.txt", encoding="utf-8"):
        dong = _CHU_THICH.sub("", dong).strip()
        if not dong or dong.startswith("-"):
            continue          # chi thi cua pip: noi dung da nam trong VAN_TAY
        try:
            _r = _Req(dong)
            if _r.marker is not None and not _r.marker.evaluate():
                continue      # khong ap dung tren nen nay
        except KeyboardInterrupt:
            raise
        except BaseException:
            continue          # khong hieu dong nay ⇒ THAM IT HON, khong bao hong
        if _dist is not None:
            try:
                _dist(_r.name)
            except KeyboardInterrupt:
                raise
            except BaseException:
                hong.append(f"{_r.name}: VANG MAT (khong co metadata)")
                continue
        # BAN chi kiem o che do `--kiem-ban`, tuc luc hoi "co duoc BO QUA pip khong".
        # Sau khi pip vua chay xong thi pip la tham quyen; doi them mot phep do o do chi
        # tao chot do thuong truc tren may thieu bo phan tich.
        if kiem_ban and str(_r.specifier) and _Spec is not None and _ban is not None:
            try:
                b = _ban(_r.name)
                thoa = _Spec(str(_r.specifier)).contains(b, prereleases=True)
            except KeyboardInterrupt:
                raise
            except BaseException as e:
                hong.append(f"{_r.name}: KHONG_DO_DUOC_BAN ({type(e).__name__})")
                continue
            if not thoa:
                hong.append(f"{_r.name}: ban {b} KHONG thoa {_r.specifier}")
                continue
        # `or _module_cua(...)`: tren <3.10 `ban_do` rong nen phai suy tu metadata.
        _mods = ban_do.get(_r.name.lower().replace("-", "_")) or _module_cua(_r.name)
        for ten in sorted(_mods):
            try:
                __import__(ten)
            except KeyboardInterrupt:
                raise
            except BaseException as e:  # PanicException (pyo3) KHONG phai Exception
                hong.append(f"{ten}: {type(e).__name__}")

if hong:
    print("[session-start] requirements.txt CHUA THOA: " + " · ".join(hong))
    sys.exit(1)
PYEOF
  }
  CAN_CAI=1
  # `CO_CHI_THI` (r351): tep co chi thi `-r`/`-c`/`-e` thi ta KHONG DU SUC noi "khong doi"
  # — noi dung that nam o tep khac ma ta khong phan tich duong dan nua. Khong tin moc,
  # de pip lam. Chieu sai duy nhat la chay pip THUA, khong bao gio la BO SOT.
  if [ "$CO_CHI_THI" = 1 ]; then
    echo "[session-start] requirements.txt co chi thi -r/-c/-e — khong dung moc, de pip quyet"
  elif [ -f "$DAU" ]; then
    if reqs_import_duoc --kiem-ban; then
      echo "[session-start] requirements.txt khong doi va moi goi import duoc — bo qua pip"
      CAN_CAI=0
    else
      echo "[session-start] moc con nhung goi KHONG import duoc — cai lai"
    fi
  fi
  if [ "$CAN_CAI" = 1 ]; then
    echo "[session-start] cai requirements.txt ..."
    if "$PY" -m pip install --quiet -r requirements.txt && reqs_import_duoc; then
      # Co chi thi ⇒ KHONG dat moc: dat vao la tu khai mot dieu ta khong do duoc.
      [ "$CO_CHI_THI" = 1 ] || : > "$DAU"   # moc CHI dat khi da chung minh import duoc
    else
      rm -f "$DAU"   # khong de lai moc "da cai" cho mot moi truong chua chung minh
      echo "[session-start] CANH BAO: requirements.txt CHUA DUNG DUOC (xem dong tren)."
      echo "[session-start]   chua: $PY -m pip install --force-reinstall -r requirements.txt ; roi $PY scripts/tl.py doctor --offline"
    fi
  fi
fi

# >>> agent-creds (wp1039)
# Spec CLOUD-SETUP-P2B-WIRE r1: SAU pip (bootstrap cần gói), TRƯỚC policy/doctor; `|| MA_AC=$?` để set -e không giết hook.
MA_AC=0; "$PY" "$GOC/ops/cloud_agent_creds.py" nap 2>&1 | sed 's/^/[session-start] /' || MA_AC=$?; echo "[session-start] agent-creds-bootstrap: rc=$MA_AC"
MA_AC=0; "$PY" "$GOC/ops/cloud_agent_creds.py" cai-agy 2>&1 | sed 's/^/[session-start] /' || MA_AC=$?; echo "[session-start] agy-ghim: rc=$MA_AC"
# <<< agent-creds (wp1039)

# --- Xác thực codex, để nó chạy được trên NHIỀU môi trường
#
# VÌ SAO: `codex login --device-auth` giải quyết được lượt đăng nhập không cần trình
# duyệt (đo 14-08-2026: in link + mã 15 phút, xong thì `Logged in using ChatGPT`).
# Nhưng container phiên remote là PHÙ DU — thu hồi là mất `~/.codex/auth.json`, và
# lượt sau lại phải nhập mã tay. Một chốt đòi thao tác tay mỗi lượt thì sớm muộn bị
# bỏ qua.
#
# Cách bền: người dùng đăng nhập MỘT LẦN trên máy có trình duyệt, rồi đặt nội dung
# `auth.json` (base64) vào biến Environment `CODEX_AUTH_JSON`, đúng khuôn `GITHUB_PAT`.
# Hook này khôi phục lại. Cách lấy chuỗi ấy: xem `docs/GOI_AGENT_DA_NEN.md`.
#
# BỐN CHỐT, mỗi cái bịt một đường hỏng đã lường:
#   1. KHÔNG in giá trị, và KHÔNG truyền qua đối số dòng lệnh — python đọc thẳng từ
#      MÔI TRƯỜNG. Đối số lộ trong `ps` cho mọi tiến trình cùng máy; biến này chứa
#      refresh token, lộ một lần là lộ hẳn.
#      (Bản đầu `printf … | python - <<'PYEOF'` vừa pipe giá trị vừa nạp script qua
#      heredoc — heredoc thắng, python đọc chuỗi RỖNG rồi báo "sai định dạng". Chốt
#      chặn đúng nhưng vì lý do sai; chỉ lộ khi chạy thử ca thuận lợi.)
#   2. KHÔNG đè khi đã đăng nhập. Bản trên đĩa có thể MỚI HƠN biến (codex tự làm mới
#      token và ghi lại `last_refresh`), nên đè bừa là hạ cấp một credential đang tốt.
#   3. Kiểm JSON + khoá bắt buộc TRƯỚC khi ghi. Biến hỏng mà ghi đè thì đổi một phiên
#      "chưa đăng nhập" (dễ đọc) thành "đăng nhập hỏng" (khó đọc).
#   4. Ghi qua tệp tạm + `chmod 600` rồi mới `mv` — không để lộ khoảnh khắc tệp có
#      quyền rộng, và không để lại tệp nửa vời nếu tiến trình chết giữa chừng.
# --- THU HOI CHINH SACH BIEN MOI TRUONG CHO CODEX  (cross-review luot 7, HIGH)
#
# LICH SU, de khong ai dung lai: khoi cu dat `shell_environment_policy.inherit = "all"`
# de phien codex "thay duoc" $CODEX_AUTH_JSON. Do la truyen TOAN BO moi truong cho moi
# lenh con cua codex, chi loai BON ten quan sat duoc tren MOT may tai MOT thoi diem.
#
# Ly le bao ve no SAI ngay trong chinh tep nay: khoi khoi phuc credential o TREN da ghi
# $CODEX_AUTH_JSON ra ~/.codex/auth.json TRUOC khi khoi policy chay. Tu do codex doc
# credential tu tep chuan, khong can bien. Va neu hook nay khong chay thi policy cung
# khong duoc cai — nen no chua bao gio la duong cuu ho doc lap. Ta doi MOT credential
# lay CA MOI TRUONG ma khong mua duoc gi.
#
# `exclude` khong cuu duoc: quet theo TEN khong chung minh duoc gi cho PGPASSWORD,
# DATABASE_URL, SSH_AUTH_SOCK hay bien vendor moi, va no loi thoi dung luc moi truong doi.
#
# Nay chi con duong GO, va go PHAI KHONG DUOC lam hong config nguoi dung — ban truoc
# luon prepend mot bang, nen mot config da co [shell_environment_policy] KHONG marker se
# thanh HAI bang trung ten va codex tu choi parse. Logic nam o mot tep RIENG de test
# duoc (t100): go dung khoi cua ta, hoac TU CHOI kem chan doan. Khong doan.
#
# FAIL-CLOSE, khong phai canh bao (cross-review luot 8, HIGH — loi cua ban va truoc).
# Ban truoc bat rc=3 roi chi in CANH BAO va di tiep: dung luc phat hien config NGUY HIEM
# ma khong go duoc thi khoi `inherit="all"` cu VAN CON HIEU LUC. Do la bien mot loi
# xac-dinh-an-toan thanh phoi moi truong CO CHU DICH.
#
# VI TRI CUA KHOI NAY LA MOT PHAN CUA CHOT (cross-review luot 9, HIGH):
# ban truoc dat no SAU hai loi goi `codex login status` cua chinh hook, nen dung
# truong hop can chan thi hook DA GOI codex xong roi. Nay khoi chay TRUOC MOI loi goi
# codex, va hai loi goi do deu bi boc bang `[ "${CODEX_BI_CHAN:-0}" = 0 ]`.
#
# PHAM VI, NOI THANG — day la cho ban truoc toi noi qua:
#   CHAN DUOC : moi duong DO KHO CUNG CAP (hook nay, `_do_codex`, `_do_codex_song`,
#               tuc ca `doctor`, `doctor --kiem-song` va `--doi-kha-dung`).
#   KHONG CHAN DUOC : nguoi dung go thang `codex` o terminal. Mot la co ma chi ma
#               cua ta doc thi khong the thuc thi hop dong "chan executable".
# Ghi nhan gioi han thay vi dat ten to hon viec no lam duoc — dung bai hoc da tra gia.
#
# HOOK CHI PHAT HIEN, KHONG GHI (quyet dinh 16-08-2026 — xem dau
# `.claude/dev/codex_env_policy.py`). Bon luot cross-review, BAY phat hien, TAT CA cung
# mot duong: viec TU DONG ghi lai config cua nguoi dung. Moi lan va bao toan duoc thu ta
# NGHI TOI va lam hong thu ta KHONG NGHI TOI (bang trung ten, mat du lieu, tep cut,
# symlink bi xuyen, CRLF, lost-update). Bay lan cung mot hinh dang thi loi nam o QUYET
# DINH GOC, khong nam o cac ban va. Ma phan thuong thi nho: go mot khoi CHINH TA them vao.
#
# Nen: hook DOC, dat co chan, va in cach chua. Nguoi dung tu chay `--go` roi tu `mv`.
# Ca lop rui ro tren chet theo KIEN TRUC, khong theo ban va.
if co codex; then
  MA_GO=0
  "$PY" "$GOC/.claude/dev/codex_env_policy.py" 2>&1 | sed 's/^/[session-start] /' || MA_GO=$?
  # KHONG doc `${PIPESTATUS[0]}` o day. Ban truoc co dong do, kem chu thich "`set -o
  # pipefail` khong bat o day" — chu thich SAI: tep nay dat `set -euo pipefail` o dong 34.
  # Va dong "phong thu" ay chinh la thu GIET ma thoat: `MA_GO=$?` la MOT LENH, nen no
  # dat lai PIPESTATUS ve 0; doc PIPESTATUS SAU do luon ra 0 ⇒ `CODEX_BI_CHAN` khong bao
  # gio duoc dat ⇒ hook van goi `codex login status` du da phat hien `inherit=all`.
  # DO DUOC (bash, cung hinh dang pipeline): sau `|| MA_GO=$?` thi MA_GO=3 PIPESTATUS[0]=0;
  # gan lai tu PIPESTATUS dua MA_GO ve 0. Lan thu BA chot fail-close chet vi mot dong
  # tuong la lam cho chac. Co `pipefail` thi `$?` cua pipeline DA la ma cua python.
  if [ "$MA_GO" -ne 0 ]; then
    CODEX_BI_CHAN=1
    echo "[session-start] !! CHAN MOI DUONG CODEX CUA KHO (ma $MA_GO): config con khoi"
    echo "[session-start]    env policy cu, hoac khong phan loai duoc. \`inherit=all\` co"
    echo "[session-start]    the CON HIEU LUC — moi lenh con cua codex nhan TOAN BO moi truong."
    echo "[session-start]    LUU Y: lenh \`codex\` go THANG o terminal KHONG bi chan."
    echo "[session-start]    Chua (cong cu KHONG tu ghi vao config cua ban):"
    echo "[session-start]      $PY .claude/dev/codex_env_policy.py --go   # dung ban da go"
    echo "[session-start]      diff ~/.codex/config.toml{,.tra-luat-da-go} && mv ... # ban tu thay"
  fi
fi

if co codex && [ "${CODEX_BI_CHAN:-0}" = 0 ]; then
  MA_AUTH=0
  "$PY" .claude/dev/launcher.py credential-status || MA_AUTH=$?
  if [ "$MA_AUTH" = 0 ]; then
    # Offline status is not proof of live health. Doctor labels it accordingly.
    codex login status >/dev/null 2>&1 </dev/null || true
  else
    echo "[session-start] codex: CHO snapshot moi; khong thu lai credential da hong"
  fi
fi

# --- BANG CHUNG DUONG, khong tin "da cai xong".
#   12 = thieu cong cu BAT BUOC          -> phien nay khong lam viec duoc, DUNG.
#   13 = co mat nhung CHUA XAC THUC      -> canh bao, khong chan: co phien khong
#        can goi agent, va chan o day se khoa luon duong nguoi dung tu sua.
# `doctor` LUON in phan bien moi truong, ke ca khi moi thu xanh — de khong ai bao
# "cong cu X khong dung duoc" ma chua tung nhin vao bien.
echo "[session-start] kiem cong cu + kha dung:"
# `MA=0` rồi `|| MA=$?`, KHÔNG phải chạy rồi `MA=$?` ở dòng sau: tệp này có `set -e`,
# nên lệnh thoát khác 0 giết cả script NGAY, trước khi dòng gán kịp chạy. Đã đo: hook
# chết ở đây với rc=13 và KHÔNG in nổi dòng "xong", tức phần xử lý 12/13 bên dưới là
# CODE CHẾT. Vế `||` đưa lệnh vào ngữ cảnh điều kiện nên `set -e` không bắt.
MA=0
"$PY" .claude/dev/launcher.py doctor --doi-kha-dung || MA=$?
if [ "$MA" -eq 12 ]; then
  echo "[session-start] THIEU CONG CU BAT BUOC — xem bang tren"
  exit 1
elif [ "$MA" -eq 13 ]; then
  echo "[session-start] CANH BAO: co cong cu CHUA DUNG DUOC (thieu xac thuc)."
  echo "[session-start] DUNG ket luan 'khong goi duoc' truoc khi doc bien:"
  echo "[session-start]   $PY .claude/dev/launcher.py moi-truong"
elif [ "$MA" -ne 0 ]; then
  echo "[session-start] doctor thoat $MA — xem bang tren"
  exit 1
fi

echo "[session-start] xong"
