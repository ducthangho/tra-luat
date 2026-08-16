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
# hook-nang-luc: codex-auth-restore rg-bat-buoc doctor-kha-dung pip-bang-chung-duong codex-env-policy codex-env-policy-thu-hoi codex-env-policy-fail-close
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

echo "[session-start] goc du an: $GOC"

# --- CLI agent chính thức. Idempotent: đã có thì không đụng (container được
# cache sau khi hook xong, nên lần sau vào thẳng).
if co npm; then
  if ! co codex; then
    echo "[session-start] cai @openai/codex ..."
    npm install -g @openai/codex >/dev/null 2>&1 || echo "[session-start] CANH BAO: cai codex that bai"
  fi
  if ! co claude; then
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
if ! co rg; then
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
PY=python3
co python3 || PY=python
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
# BANG CHUNG DUONG bang `pip install --dry-run` - no im lang va nhanh khi da du,
# va bao thieu khi moi truong khong con khop.
if [ -f requirements.txt ]; then
  KHO_MOC="$("$PY" -c "import subprocess,sys;print(subprocess.run(['git','rev-parse','--git-dir'],capture_output=True,text=True).stdout.strip() or '.')" 2>/dev/null || echo .)"
  VAN_TAY="$( "$PY" -c "
import hashlib, sys
h = hashlib.sha256(open('requirements.txt','rb').read()).hexdigest()[:16]
print(h + '_' + hashlib.sha256(sys.prefix.encode()).hexdigest()[:8])" )"
  DAU="$KHO_MOC/.tl_reqs_$VAN_TAY"
  CAN_CAI=1
  if [ -f "$DAU" ]; then
    # Moc noi da cai. Kiem lai bang bang chung duong truoc khi tin.
    if "$PY" -m pip install --dry-run --quiet -r requirements.txt >/dev/null 2>&1; then
      echo "[session-start] requirements.txt khong doi va moi truong con khop — bo qua pip"
      CAN_CAI=0
    else
      echo "[session-start] moc con nhung moi truong KHONG con khop — cai lai"
    fi
  fi
  if [ "$CAN_CAI" = 1 ]; then
    echo "[session-start] cai requirements.txt ..."
    if "$PY" -m pip install --quiet -r requirements.txt; then
      : > "$DAU"
    else
      echo "[session-start] CANH BAO: pip that bai"
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
if co codex; then
  MA_GO=0
  "$PY" "$GOC/.claude/dev/codex_env_policy.py" 2>&1 | sed 's/^/[session-start] /' || MA_GO=$?
  # `set -o pipefail` khong bat o day => lay ma cua PYTHON, khong phai cua `sed`.
  MA_GO=${PIPESTATUS[0]:-$MA_GO}
  if [ "$MA_GO" -ne 0 ]; then
    CODEX_BI_CHAN=1
    echo "[session-start] !! CHAN MOI DUONG CODEX CUA KHO (ma $MA_GO): khong go duoc"
    echo "[session-start]    khoi env policy cu. \`inherit=all\` co the CON HIEU LUC —"
    echo "[session-start]    moi lenh con cua codex nhan TOAN BO moi truong."
    echo "[session-start]    LUU Y: lenh \`codex\` go THANG o terminal KHONG bi chan."
    echo "[session-start]    Sua tay ~/.codex/config.toml roi chay:"
    echo "[session-start]      $PY .claude/dev/codex_env_policy.py"
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
