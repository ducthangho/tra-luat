#!/usr/bin/env bash
# Setup script cho môi trường Codex Cloud (chatgpt.com/codex) — kho này.
# Ô "Setup script" của môi trường chỉ cần MỘT dòng:   bash ops/codex_cloud_setup.sh
# Chạy ở gốc kho, lúc dựng container (bật mạng cho giai đoạn setup). Test: ops/codex_cloud_setup_test.py.
#
# Đo 27-10-2026 trên Codex Cloud: KHÔNG có root lẫn `sudo` (`sudo: command not found`, rc=127) ⇒ công thức
# `sudo apt-get` của `ops/cong_cu.yaml` không dùng được ở đó. Nên mọi nhị phân hệ thống đi qua `cai_deb`:
# có sẵn thì thôi · root/sudo không mật khẩu thì apt-get thường · còn lại tải .deb (kèm phụ thuộc CHƯA cài)
# về $HOME/.local, giải nén, và tạo wrapper chỉ đặt LD_LIBRARY_PATH cho đúng lệnh đó (không đặt toàn cục).
# Cũng đo được: `pip install --upgrade pip` CHẾT trên Python của distro ("installed by debian") — đừng thêm.
set -euo pipefail

BIN="$HOME/.local/bin"
GOC="$HOME/.local/tra-luat-goc"     # gốc giải nén .deb khi không có root

# cai_deb <gói apt> <lệnh>
cai_deb() {
  local goi="$1" lenh="$2"
  command -v "$lenh" >/dev/null 2>&1 && return 0
  if [ "$(id -u)" = 0 ]; then apt-get update -qq && apt-get install -y -qq "$goi" >/dev/null; return; fi
  if command -v sudo >/dev/null 2>&1 && sudo -n true 2>/dev/null; then
    sudo apt-get update -qq && sudo apt-get install -y -qq "$goi" >/dev/null; return
  fi
  local A="$HOME/.local/apt"
  local O=(-o "Dir::State::Lists=$A/lists" -o "Dir::Cache=$A/cache" -o Debug::NoLocking=1
           -o "APT::Sandbox::User=$(id -un)")
  mkdir -p "$A/lists/partial" "$A/cache/archives/partial" "$A/deb" "$GOC" "$BIN"
  [ -n "$(ls "$A/lists" 2>/dev/null | grep -v partial)" ] || apt-get "${O[@]}" update -qq 2>/dev/null || true
  local p
  for p in $(apt-cache "${O[@]}" depends --recurse --no-recommends --no-suggests --no-conflicts \
               --no-breaks --no-replaces --no-enhances "$goi" | grep -v '^[ <]' | sort -u); do
    dpkg -s "$p" >/dev/null 2>&1 && continue
    (cd "$A/deb" && apt-get "${O[@]}" download "$p" >/dev/null 2>&1) || true
  done
  for p in "$A"/deb/*.deb; do dpkg-deb -x "$p" "$GOC"; done
  local lib
  lib="$(find "$GOC" -maxdepth 3 -type d -name '*-linux-gnu' | tr '\n' ':')"
  printf '#!/bin/sh\nLD_LIBRARY_PATH="%s${LD_LIBRARY_PATH:-}" exec "%s" "$@"\n' \
    "$lib" "$GOC/usr/bin/$lenh" > "$BIN/$lenh"
  chmod +x "$BIN/$lenh"
}

# ghi_bashrc: các dòng shell của agent cần, mỗi dòng đúng MỘT lần (chạy lại setup không nhân bản).
# Đo 27-10-2026: lúc agent chạy task, Codex Cloud gắn $HOME CHỈ ĐỌC — `_config_backup_dir()` mặc định là
# `${LOCALAPPDATA:-$HOME}/tra-luat/_config_backups` nên mkdir ném EROFS và selftest đỏ đúng
# r202_profile_delete_backup_ngoai_cay (1730/1731). Trỏ LOCALAPPDATA ra thư mục tạm GHI ĐƯỢC, NGOÀI cây kho
# (luật r202 vẫn giữ); tái hiện tại chỗ với HOME chỉ đọc: thiếu dòng này 1730/1731, có thì 1731/1731.
#
# Các dòng đặt ĐẦU tệp, không nối cuối (finding P2 Codex trên PR #984, tái hiện được): ~/.bashrc mặc định
# có `[ -z "$PS1" ] && return`, nên dòng nối cuối KHÔNG BAO GIỜ tới được với shell không tương tác của agent.
# Bản cũ (đã nối cuối từ lượt setup trước) bị gỡ rồi đặt lại ở đầu; chạy lại cho ra đúng cùng một tệp.
ghi_bashrc() {
  local f="$HOME/.bashrc" tam rc=0
  local khoi=('export PATH="$HOME/.local/bin:$PATH"'
              'export LOCALAPPDATA="${LOCALAPPDATA:-${TMPDIR:-/tmp}/tra-luat-localappdata}"')
  tam="$(mktemp "$HOME/.bashrc.tra-luat.XXXXXX")"
  printf '%s\n' "${khoi[@]}" > "$tam"
  if [ -f "$f" ]; then
    # grep -v: rc 1 = không còn dòng nào khác (hợp lệ); rc 2 = KHÔNG ĐỌC ĐƯỢC ⇒ huỷ, đừng ghi đè mất nội dung.
    grep -vxF -f <(printf '%s\n' "${khoi[@]}") "$f" >> "$tam" || rc=$?
    [ "$rc" -le 1 ] || { rm -f "$tam"; echo "ghi_bashrc: không đọc được $f (rc=$rc)" >&2; return 1; }
    chmod --reference="$f" "$tam"
  fi
  mv -f "$tam" "$f"
}

main() {
  local PY d t GP
  PY="$(command -v python3 || command -v python)"
  mkdir -p "$BIN"
  export PATH="$BIN:$PATH"

  # 1. Phụ thuộc Python: runtime + đúng bản CI ghim (ci.yml); shellcheck qua pip vì không cần root.
  "$PY" -m pip install --quiet -r requirements.txt
  "$PY" -m pip install --quiet jsonschema==4.26.0 ruff==0.15.15 shellcheck-py
  d="$("$PY" -c 'import sysconfig; print(sysconfig.get_path("scripts"))')"
  [ -x "$d/shellcheck" ] && ln -sf "$d/shellcheck" "$BIN/shellcheck"

  # 1b. Credential agent (wp1039): sau pip (bootstrap cần gói); luôn rc 0, đúng một dòng `agent_creds:`; không cài agy (Q5).
  "$PY" ops/cloud_agent_creds.py nap || true

  # 2. Nhị phân hệ thống: pdftotext (BẮT BUỘC cho đường nạp PDF), rg (bắt buộc cho agent).
  cai_deb poppler-utils pdftotext
  cai_deb ripgrep rg

  # 3. actionlint đúng bản ghim + đối chiếu băm (ops/cong_cu.yaml) — đường này không cần root.
  GP="$(mktemp)"
  GITHUB_PATH="$GP" RUNNER_TEMP="$HOME/.local/tra-luat-cong-cu" bash ops/cai_cong_cu.sh actionlint >/dev/null
  while IFS= read -r d; do [ -x "$d/actionlint" ] && ln -sf "$d/actionlint" "$BIN/actionlint"; done < "$GP"
  rm -f "$GP"

  # 4. PATH + LOCALAPPDATA bền cho shell của agent + core.abbrev = 7 cho gate golden/determinism
  #    (CLAUDE.md, Quy ước deploy mục 6).
  ghi_bashrc
  git config --global core.abbrev 7

  # 5. Bằng chứng DƯƠNG — đừng tin rc của trình cài. Thiếu thứ nào thì script ĐỎ.
  "$PY" -c "import pypdf, yaml, jsonschema; print('python deps OK')"
  pdftotext -v 2>&1 | head -1
  for t in actionlint shellcheck rg; do
    "$PY" ops/cong_cu.py kiem-tra --chi "$t" >/dev/null || { echo "$t THIEU" >&2; exit 1; }
    echo "$t OK"
  done
  "$PY" scripts/tl_boot.py --version
}

# `source` để test gọi riêng `cai_deb`; chạy thẳng thì làm trọn.
if [ "${BASH_SOURCE[0]}" = "$0" ]; then main "$@"; fi
