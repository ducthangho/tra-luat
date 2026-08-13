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

# --- Xac thuc codex. CAI XONG KHONG PHAI LA DUNG DUOC, va day la lop noi doi cao
# hon lop `which` ma doctor da va: `codex --version` chay rc=0 nen doctor bao "co
# codex", trong khi MOI lenh `codex exec` tra 401. DO DUOC 13-08 tren container
# Claude Code web, hai su that tach roi nhau:
#   · `OPENAI_API_KEY` trong moi truong bi codex BO QUA — goi di KHONG kem bearer,
#     OpenAI tra dung chu "Missing bearer or basic authentication in header";
#   · khoa phai nam trong `~/.codex/auth.json`, ghi bang `codex login --with-api-key`,
#     doc tu STDIN nen chay duoc khong can trinh duyet.
# Da chung minh het duong bang khoa GIA: sau khi login, loi doi tu "Missing bearer"
# thanh "Incorrect API key provided: sk-thu-n***" — tuc bearer DA toi OpenAI qua
# proxy, va thu duy nhat con thieu la mot khoa THAT.
# Im lang o day se de lai mot cong cu TRONG NHU dung duoc, nen thieu khoa thi noi ra.
#
# HAI DUONG NAP, theo dung thu tu uu tien:
#   1. CODEX_AUTH_JSON — noi dung `~/.codex/auth.json` bung nguyen tu may da
#      `codex login` bang tai khoan ChatGPT. Day la duong DUY NHAT dung duoc goi
#      ChatGPT Plus/Pro o container khong co trinh duyet: dang nhap ChatGPT la
#      OAuth qua localhost, khong dien duoc o day. LUU Y: tep do chua REFRESH
#      TOKEN, tuc mot bi mat song lau — dat no o cho nao thi cho do can duoc coi
#      la kho bi mat.
#   2. OPENAI_API_KEY — khoa API tra tien theo luot. GOI CHATGPT PRO KHONG KEM
#      khoa API va khong kem tin dung API; do la hai thu tinh tien khac nhau.
if co codex; then
  if codex login status >/dev/null 2>&1; then
    echo "[session-start] codex: da dang nhap"
  elif [ -n "${CODEX_AUTH_JSON:-}" ]; then
    mkdir -p "$HOME/.codex"
    # 0600 NGAY TU LUC TAO: `printf > tep` de lai quyen theo umask, ma day la
    # refresh token. Cung ly le voi ban chup prompt trong launcher.
    ( umask 077; printf '%s' "$CODEX_AUTH_JSON" > "$HOME/.codex/auth.json" )
    if codex login status >/dev/null 2>&1; then
      echo "[session-start] codex: da nap phien dang nhap tu CODEX_AUTH_JSON"
    else
      echo "[session-start] CANH BAO: CODEX_AUTH_JSON co nhung khong dung duoc -"
      echo "[session-start]   dang nhap lai tren may that roi bung lai ~/.codex/auth.json"
    fi
  elif [ -n "${OPENAI_API_KEY:-}" ]; then
    if printf '%s' "$OPENAI_API_KEY" | codex login --with-api-key >/dev/null 2>&1; then
      echo "[session-start] codex: da dang nhap bang OPENAI_API_KEY"
    else
      echo "[session-start] CANH BAO: co OPENAI_API_KEY nhung codex login THAT BAI"
    fi
  else
    echo "[session-start] CANH BAO: codex DA CAI nhung CHUA DANG NHAP - moi lenh se tra 401."
    echo "[session-start]   Goi ChatGPT: chay \`codex login\` tren may that roi dat noi dung"
    echo "[session-start]   ~/.codex/auth.json vao bien CODEX_AUTH_JSON cua moi truong nay."
    echo "[session-start]   Khoa API (tinh tien rieng): dat OPENAI_API_KEY, hoac chay tay:"
    echo "[session-start]   printf %s \"\$KHOA\" | codex login --with-api-key"
  fi
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

# --- cffi: BAT BUOC de `import pypdf` khong NO. DO DUOC 13-08 tren container Claude
# Code web ngay sau khi hook nay chay pip: `pypdf` keo `cryptography` (ban apt), ma
# ban do thieu `cffi` thi nem `pyo3_runtime.PanicException` — KHONG phai ngoai le
# Python thuong, no giet ca tien trinh. Hau qua doc rat sai: `--selftest` chet giua
# chung nen KHONG in noi dong `N/N`, trong y het "co ca do", trong khi cac ca deu
# xanh. Cai xong: 1697/1697.
# Khong dua vao requirements.txt vi day la khuyet cua MOI TRUONG (ban cryptography
# cai bang apt), khong phai mot phu thuoc cua san pham.
if ! "$PY" -c "import pypdf" >/dev/null 2>&1; then
  echo "[session-start] pypdf khong nap duoc — cai cffi (thieu no thi cryptography ban apt panic)"
  "$PY" -m pip install --quiet cffi || echo "[session-start] CANH BAO: cai cffi that bai"
  if "$PY" -c "import pypdf" >/dev/null 2>&1; then
    echo "[session-start] pypdf: nap duoc sau khi cai cffi"
  else
    echo "[session-start] CANH BAO: pypdf VAN khong nap duoc — selftest se chet giua chung"
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
