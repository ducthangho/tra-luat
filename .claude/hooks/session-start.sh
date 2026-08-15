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
set -euo pipefail

# Đọc TOÀN BỘ biến điều phối/xác thực cần dùng trước khi resolve hay gọi tool.
# Chỉ giữ trạng thái/nguồn; tuyệt đối không echo giá trị credential.
MOI_TRUONG_DA_DOC=1
REMOTE_VALUE="${CLAUDE_CODE_REMOTE:-}"
PROJECT_VALUE="${CLAUDE_PROJECT_DIR:-}"
PATH_VALUE="${PATH:-}"
CODEX_AUTH_CO=0; [ -n "${CODEX_AUTH_JSON:-}" ] && CODEX_AUTH_CO=1
GITHUB_AUTH_SOURCE=none
if [ -n "${GH_TOKEN:-}" ]; then
  GITHUB_AUTH_SOURCE=GH_TOKEN
elif [ -n "${GITHUB_TOKEN:-}" ]; then
  GITHUB_AUTH_SOURCE=GITHUB_TOKEN
elif [ -n "${GITHUB_PAT:-}" ]; then
  # `gh` không đọc tên biến lịch sử GITHUB_PAT. Chỉ ánh xạ trong tiến trình hook,
  # không ghi token xuống đĩa và không in giá trị.
  export GH_TOKEN="${GITHUB_PAT}"
  GITHUB_AUTH_SOURCE=GITHUB_PAT-to-GH_TOKEN
fi

# Chỉ chạy trong môi trường remote. Máy cá nhân đã có sẵn công cụ theo ý người
# dùng; cài đè vào đó là vượt quyền.
if [ "$REMOTE_VALUE" != "true" ]; then
  echo "[session-start] khong phai moi truong remote — bo qua"
  exit 0
fi

GOC="${PROJECT_VALUE:-$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)}"
cd "$GOC"

# `command -v` chứ không `which`: có sẵn ở mọi shell POSIX và không phụ thuộc gói ngoài.
co() { command -v "$1" >/dev/null 2>&1; }
if co python3; then PY=python3
elif co python; then PY=python
else
  echo "[session-start] HONG: khong co python/python3 de probe va chay launcher"
  exit 1
fi
# `command -v` chỉ chứng minh có path. Probe thật có timeout, rc=0 và output.
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

echo "[session-start] goc du an: $GOC"
echo "[session-start] moi truong: da doc truoc tool; GitHub auth source=$GITHUB_AUTH_SOURCE; CODEX_AUTH_JSON present=$CODEX_AUTH_CO"

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

# --- GitHub CLI là đường vận hành bắt buộc. MCP có thể là đường chính ở một số
# phiên, nhưng ADR-0017 đặt Issue/PR làm nguồn sự thật nên không được để mất cả
# đường dự phòng/chuẩn đoán `gh`.
if ! co_chay gh; then
  if co apt-get; then
    echo "[session-start] cai gh ..."
    (apt-get install -y -qq gh >/dev/null 2>&1 \
      || sudo apt-get install -y -qq gh >/dev/null 2>&1) \
      || echo "[session-start] CANH BAO: cai gh that bai"
  else
    echo "[session-start] CANH BAO: khong co gh va khong co apt-get"
  fi
fi

# --- ripgrep: cả codex lẫn Claude Code đều gọi `rg` để tìm trong mã. Thiếu nó thì
# lệnh tìm gãy giữa chừng chứ không tự lùi về grep.
if ! co_chay rg; then
  if co apt-get; then
    echo "[session-start] cai ripgrep ..."
    (apt-get install -y -qq ripgrep >/dev/null 2>&1 \
      || sudo apt-get install -y -qq ripgrep >/dev/null 2>&1) \
      || echo "[session-start] CANH BAO: cai ripgrep that bai"
  else
    echo "[session-start] CANH BAO: khong co rg va khong co apt-get"
  fi
fi

# --- phụ thuộc Python của kho
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
if [ -n "${CODEX_AUTH_JSON:-}" ] && co codex; then
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
if co codex; then
  # BẰNG CHỨNG DƯƠNG, không suy từ việc đã ghi tệp: hỏi chính codex.
  echo "[session-start] codex auth: $(codex login status 2>&1 </dev/null | head -1)"
fi

if co claude; then
  if claude auth status >/dev/null 2>&1 </dev/null; then
    echo "[session-start] claude auth: OK"
  else
    echo "[session-start] CANH BAO: claude auth KHONG dung"
  fi
fi
if co gh; then
  if gh auth status >/dev/null 2>&1 </dev/null; then
    echo "[session-start] github auth: OK"
  else
    echo "[session-start] CANH BAO: github auth KHONG dung"
  fi
fi

# --- BẰNG CHỨNG DƯƠNG, không tin "đã cài xong". doctor thoát khác 0 khi thiếu
# công cụ BẮT BUỘC; Claude/Codex/GitHub/rg/bash đều fail-closed theo yêu cầu vận hành.
echo "[session-start] kiem cong cu:"
"$PY" .claude/dev/launcher.py doctor || {
  echo "[session-start] THIEU CONG CU BAT BUOC — xem bang tren"
  exit 1
}

echo "[session-start] xong"
