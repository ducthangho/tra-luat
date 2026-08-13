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

# --- Công cụ: MỘT hợp đồng "kiểm rồi cài", nằm trong launcher chứ không chép lại
# ở đây. Bản trước dựng lại logic cài (npm cho hai CLI, apt-get cho ripgrep) ngay
# trong hook, nên bảng công cụ sống ở HAI chỗ và trôi khỏi nhau — `doctor` biết
# lệnh cài chính thức của từng nền, còn hook chỉ biết nhánh Linux.
#
# `doctor --cai` cài xong sẽ ĐO LẠI: báo cáo là trạng thái SAU CÙNG, không phải
# "đã chạy lệnh cài" (rc của trình cài không phải bằng chứng công cụ dùng được).
# Ở đây KHÔNG kiểm mã thoát: thiếu công cụ KHÔNG bắt buộc thì không phải lý do
# giết phiên. Cổng thật là lệnh `doctor` cuối tệp.
PY=python3
co python3 || PY=python
echo "[session-start] kiem va cai cong cu:"
"$PY" .claude/dev/launcher.py doctor --cai || true

# --- Xác thực codex. Container phù du: ~/.codex/auth.json mất theo container, nên
# phải làm lại mỗi phiên. KHÔNG dùng API key: kho này đăng nhập bằng tài khoản
# ChatGPT, API key tính tiền riêng nên là trả hai lần cho cùng một việc.
#
# Hook KHÔNG làm được việc tương tác, nên nó không giả vờ: thiếu đường không tương
# tác thì IN THẲNG lệnh người dùng cần chạy, chứ không cảnh báo mơ hồ rồi để lượt
# sau chết ở chỗ khó đọc.
if command -v codex >/dev/null 2>&1; then
  # BẰNG CHỨNG DƯƠNG qua chính chốt của launcher: nó đọc NỘI DUNG đầu ra, không đọc
  # rc — `codex` chưa đăng nhập có lệnh in 401 mà vẫn thoát 0.
  da_xac_thuc() {
    "$PY" .claude/dev/launcher.py check \
      --auth-probe '["codex","login","status"]' >/dev/null 2>&1
  }
  if da_xac_thuc; then
    echo "[session-start] codex: da xac thuc"
  elif [ -n "${CODEX_ACCESS_TOKEN:-}" ]; then
    echo "[session-start] codex: dang nhap bang CODEX_ACCESS_TOKEN ..."
    printenv CODEX_ACCESS_TOKEN | codex login --with-access-token >/dev/null 2>&1 || true
    # Hỏi LẠI. rc của lệnh login không phải bằng chứng đã đăng nhập được.
    if da_xac_thuc; then
      echo "[session-start] codex: xac thuc OK"
    else
      echo "[session-start] CANH BAO: co CODEX_ACCESS_TOKEN nhung van CHUA xac thuc"
      echo "[session-start]   token co the da het han (~10 ngay) — chay: codex login --device-auth"
    fi
  else
    echo "[session-start] codex CHUA xac thuc. Chay lenh nay MOT LAN cho container nay:"
    echo "[session-start]     codex login --device-auth"
    echo "[session-start]   (in ra ma, duyet bang dien thoai; dung tai khoan ChatGPT, khong ton credit API)"
  fi
fi

# --- phụ thuộc Python của kho ($PY đã chọn ở trên)
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

# --- BẰNG CHỨNG DƯƠNG, không tin "đã cài xong". doctor thoát khác 0 khi thiếu
# công cụ BẮT BUỘC; thiếu codex/claude chỉ là cảnh báo vì có phiên không cần gọi agent.
echo "[session-start] kiem cong cu:"
"$PY" .claude/dev/launcher.py doctor || {
  echo "[session-start] THIEU CONG CU BAT BUOC — xem bang tren"
  exit 1
}

echo "[session-start] xong"
