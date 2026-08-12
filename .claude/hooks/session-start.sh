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
# lệnh tìm gãy giữa chừng chứ không tự lùi về grep.
if ! co rg; then
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
PY=python3
co python3 || PY=python
# Chi cai lai khi requirements.txt DOI. Audit codex: hook chay pip moi lan
# SessionStart la khong idempotent that su - vua cham vua co the keo ve ban khac
# (pypdf>=4.0 khong ghim tran).
if [ -f requirements.txt ]; then
  DAU="${TMPDIR:-/tmp}/.tl_reqs_$( "$PY" -c "import hashlib,sys;print(hashlib.sha256(open('requirements.txt','rb').read()).hexdigest()[:16])" )"
  if [ -f "$DAU" ]; then
    echo "[session-start] requirements.txt khong doi — bo qua pip"
  else
    echo "[session-start] cai requirements.txt ..."
    if "$PY" -m pip install --quiet -r requirements.txt; then
      : > "$DAU"
    else
      echo "[session-start] CANH BAO: pip that bai"
    fi
  fi
fi

# --- BẰNG CHỨNG DƯƠNG, không tin "đã cài xong". doctor thoát khác 0 khi thiếu
# công cụ BẮT BUỘC; thiếu codex/claude chỉ là cảnh báo vì có phiên không cần gọi agent.
echo "[session-start] kiem cong cu:"
"$PY" .claude/dev/launcher.py doctor || {
  echo "[session-start] THIEU CONG CU BAT BUOC — xem bang tren"
  exit 1
}

echo "[session-start] xong"
