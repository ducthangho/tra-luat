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
# hook-nang-luc: codex-auth-restore rg-bat-buoc doctor-kha-dung pip-bang-chung-duong codex-env-policy codex-env-policy-thu-hoi codex-env-policy-fail-close codex-env-policy-chi-doc co-chay-probe moi-truong-doc-truoc github-nguon-that pip-bang-chung-import
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

# Chỉ chạy trong môi trường remote. Máy cá nhân đã có sẵn công cụ theo ý người
# dùng; cài đè vào đó là vượt quyền.
if [ "${CLAUDE_CODE_REMOTE:-}" != "true" ]; then
  echo "[session-start] khong phai moi truong remote — bo qua"
  exit 0
fi

GOC="${CLAUDE_PROJECT_DIR:-$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)}"
cd "$GOC"

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
CODEX_AUTH_CO=0; [ -n "${CODEX_AUTH_JSON:-}" ] && CODEX_AUTH_CO=1
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

# --- ripgrep: cả codex lẫn Claude Code đều gọi `rg` để tìm trong mã. Thiếu nó thì
# lệnh tìm gãy giữa chừng chứ KHÔNG tự lùi về grep — phiên mất khả năng tra cứu mà
# không hỏng ở chỗ đọc được. Vì thế `rg` là BAT BUOC trong `doctor` từ 15-08-2026.
#
# Ba đường cài, thử lần lượt: apt-get (có/không sudo), rồi cargo. Không đường nào
# chạy thì nói THẲNG là phiên sẽ thiếu — đừng để nó lộ ra giữa chừng.
if ! co_chay rg; then
  echo "[session-start] cai ripgrep ..."
  if co apt-get; then
    apt-get install -y -qq ripgrep >/dev/null 2>&1 \
      || sudo apt-get install -y -qq ripgrep >/dev/null 2>&1 \
      || { apt-get update -qq >/dev/null 2>&1 || sudo apt-get update -qq >/dev/null 2>&1; \
           apt-get install -y -qq ripgrep >/dev/null 2>&1 \
           || sudo apt-get install -y -qq ripgrep >/dev/null 2>&1; } \
      || true
  fi
  co rg || { co cargo && cargo install ripgrep >/dev/null 2>&1 || true; }
  # BANG CHUNG DUONG: `command -v` la CO MAT, `rg --version` la CHAY DUOC. Audit
  # codex tung dung hai tep RONG ten git.exe/python.exe roi doctor bao xanh.
  if rg --version >/dev/null 2>&1; then
    echo "[session-start] rg: $(rg --version | head -1)"
  else
    echo "[session-start] CANH BAO: KHONG cai duoc rg — tra cuu ma se gay giua chung"
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
  VAN_TAY="$( "$PY" -c "
import hashlib, sys
h = hashlib.sha256(open('requirements.txt','rb').read()).hexdigest()[:16]
print(h + '_' + hashlib.sha256(sys.prefix.encode()).hexdigest()[:8])" )"
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
# r338 (do 06-09-2026): TEN GOI (pip) KHAC TEN MODULE (import), va suy ten bang chuan
# hoa chuoi la DOAN chu khong phai DO. Phan chung chay duoc: `PyYAML==6.0.3` -> ban cu
# suy ra `pyyaml` -> ModuleNotFoundError, TRONG KHI `import yaml` chay tot. Tuc them mot
# phu thuoc that vao requirements.txt lam chot nay bao dong GIA va fail-close chan phien.
# Chua bang mot BANG TAY DOI TEN thi cung la doan, chi la doan som hon; hoi
# `importlib.metadata` cua ban DA CAI moi la do — no doc tu metadata that cua goi.
try:
    from importlib.metadata import packages_distributions
except ImportError:                 # Python < 3.10
    packages_distributions = None
ban_do = {}
if packages_distributions is not None:
    for _mod, _dists in packages_distributions().items():
        # BO module gach duoi: chung la ban tang toc TUY CHON, doi ho chung la tai tao
        # dung lop loi vua sua. Phan chung: PyYAML khai ca `_yaml` (C ext cua libyaml),
        # ma `yaml/__init__.py` boc no trong `try: from .cyaml import * / except
        # ImportError` — chan `_yaml` roi `import yaml` VAN OK. Doi `_yaml` la bao GIA
        # tren moi may cai PyYAML thuan Python.
        if _mod.startswith("_"):
            continue
        for _d in _dists:
            ban_do.setdefault(_d.lower().replace("-", "_"), set()).add(_mod)

# r338b (P2 cua codex tren PR #449, da TAI HIEN truoc khi vá): IMPORT DUOC khong chung
# minh BAN DUNG. Phan chung chay duoc: requirements doi `pypdf>=4.0`, moi truong cai
# `pypdf` 3.17.4 — import chay ngon nen chot tra rc=0, hook BO QUA pip, va giu nguyen
# mot moi truong khong con thoa requirements.txt. Dung thu troi ma chot nay sinh ra de
# sua. Cung ho "CO MAT != DUNG DUOC", them mot nac: DUNG DUOC != DUNG BAN.
#
# CHI kiem ban o che do `--kiem-ban`, tuc luc tra loi cau "co duoc BO QUA pip khong".
# Sau khi pip vua chay xong thi moi truong thoa requirements THEO CACH DUNG (pip la
# thâm quyen), nen doi them mot phep do o do chi tao ra chot do thuong truc khi may
# khong co bo phan tich specifier.
kiem_ban = "--kiem-ban" in sys.argv[1:]
_spec = None
if kiem_ban:
    for _m in ("packaging.specifiers", "pip._vendor.packaging.specifiers"):
        # `packaging` tran KHONG co trong venv tran (do 06-09-2026); ban vendor cua pip
        # thi co o CA HAI nen — ma hook nay von da doi pip. Do la ly do co duong lui.
        try:
            _spec = __import__(_m, fromlist=["SpecifierSet"]).SpecifierSet
            break
        except ImportError:
            continue
try:
    from importlib.metadata import version as _ban_da_cai
except ImportError:
    _ban_da_cai = None

hong = []
for dong in open("requirements.txt", encoding="utf-8"):
    dong = dong.split("#", 1)[0].strip()
    if not dong or dong.startswith("-"):
        continue
    dong = dong.split(";", 1)[0].strip()          # bo environment marker
    m = re.match(r"([A-Za-z0-9._-]+)\s*(?:\[[^\]]*\])?\s*(.*)$", dong)
    if not m:
        continue
    ten_goi, dieu_kien = m.group(1), m.group(2).strip()
    goi = ten_goi.strip().lower().replace("-", "_")
    # Goi CHUA CAI thi khong co trong metadata -> lui ve ten suy ra -> import that bai
    # -> bao THIEU. Do la dung: ban do chi chua ten, khong che duoc rang cua chot.
    for ten in sorted(ban_do.get(goi) or {goi}):
        try:
            __import__(ten)
        except KeyboardInterrupt:
            raise
        except BaseException as e:  # PanicException (pyo3) khong phai Exception
            hong.append(f"{ten}: {type(e).__name__}")
    if not (kiem_ban and dieu_kien):
        continue
    # KHONG DO DUOC != DAT. Thieu bo phan tich hay thieu metadata thi KHONG duoc khai
    # la thoa; tra hong o day nghia la "dung bo qua pip", tuc de pip — thâm quyen that
    # su — quyet dinh. Do la tu chua, khong phai chot chet.
    if _spec is None or _ban_da_cai is None:
        hong.append(f"{ten_goi}: KHONG_DO_DUOC_BAN (thieu bo phan tich specifier)")
        continue
    try:
        ban = _ban_da_cai(ten_goi)
    except KeyboardInterrupt:
        raise
    except BaseException:
        hong.append(f"{ten_goi}: KHONG_DO_DUOC_BAN (khong co metadata)")
        continue
    try:
        thoa = _spec(dieu_kien).contains(ban, prereleases=True)
    except KeyboardInterrupt:
        raise
    except BaseException as e:
        hong.append(f"{ten_goi}: KHONG_DO_DUOC_BAN ({type(e).__name__})")
        continue
    if not thoa:
        hong.append(f"{ten_goi}: ban {ban} KHONG thoa {dieu_kien}")
if hong:
    print("[session-start] requirements.txt CHUA THOA (import hong hoac lech ban): "
          + " · ".join(hong))
    sys.exit(1)
PYEOF
  }
  CAN_CAI=1
  if [ -f "$DAU" ]; then
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
      : > "$DAU"     # moc CHI duoc dat khi da chung minh import duoc
    else
      rm -f "$DAU"   # khong de lai moc "da cai" cho mot moi truong chua chung minh
      echo "[session-start] CANH BAO: requirements.txt CHUA DUNG DUOC (xem dong tren)."
      echo "[session-start]   chua: $PY -m pip install --force-reinstall -r requirements.txt ; roi $PY scripts/tl.py doctor --offline"
    fi
  fi
fi

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

if [ -n "${CODEX_AUTH_JSON:-}" ] && co codex && [ "${CODEX_BI_CHAN:-0}" = 0 ]; then
  if codex login status >/dev/null 2>&1 </dev/null; then
    echo "[session-start] codex: da dang nhap san — GIU nguyen, khong ghi de"
  else
    if "$PY" - <<'PYEOF'
import base64, binascii, json, os, sys, tempfile
raw = os.environ.get("CODEX_AUTH_JSON", "").strip()
try:
    data = base64.b64decode(raw, validate=True)
except (binascii.Error, ValueError):
    sys.exit(1)                      # KHONG in noi dung, ke ca doan dau
try:
    d = json.loads(data)
except Exception:
    sys.exit(2)
if not isinstance(d, dict) or "tokens" not in d:
    sys.exit(3)                      # thieu khoa bat buoc
dst = os.path.join(os.path.expanduser("~"), ".codex", "auth.json")
os.makedirs(os.path.dirname(dst), mode=0o700, exist_ok=True)
fd, tmp = tempfile.mkstemp(dir=os.path.dirname(dst))
try:
    os.write(fd, data); os.close(fd)
    os.chmod(tmp, 0o600); os.replace(tmp, dst)
except BaseException:
    os.unlink(tmp); raise
PYEOF
    then
      echo "[session-start] codex: da khoi phuc auth tu CODEX_AUTH_JSON"
    else
      echo "[session-start] CANH BAO: CODEX_AUTH_JSON khong dung dang (base64 cua auth.json) — bo qua"
    fi
  fi
fi
if co codex && [ "${CODEX_BI_CHAN:-0}" = 0 ]; then
  # BẰNG CHỨNG DƯƠNG, không suy từ việc đã ghi tệp: hỏi chính codex.
  echo "[session-start] codex auth: $(codex login status 2>&1 </dev/null | head -1)"
elif co codex; then
  echo "[session-start] codex auth: BO QUA — codex dang bi chan (xem tren)"
fi

# --- KHOI PHUC credential codex: KHOI O TREN da lam roi, dung goi lai o day.
# `launcher.py chuan-bi` la duong CUU HO cho truong hop hook NAY khong chay — xem
# chu thich cua `chuan_bi_xac_thuc()`. Goi ca hai trong mot luot chi thanh nhieu.

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
