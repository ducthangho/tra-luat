# COWORK_EDIT_SAFETY — chống cắt cụt khi SỬA file skill (mount Cowork #51435/#53940)

Bug: tool **Edit/Write native của Cowork** đôi khi **cắt cụt file** — clamp độ dài về kích thước file TRƯỚC khi sửa,
và **Read có thể trả cache cũ** nên không thấy hỏng ngay. Skill có phòng thủ 3 lớp; tài liệu này là lớp **NGĂN** (write-side).

> Lớp 1 NGĂN (write-side, dưới đây) · Lớp 2 PHÁT HIỆN (`tl verify-integrity`) · Lớp 3 KHÔI PHỤC —
> **★ `tl_fetch.sh` (tải zip SẠCH từ Drive, BỎ QUA mount) là đường khôi phục DUY NHẤT còn lại**: cơ chế
> `_parts/` ĐÃ BỎ từ khi Cowork bootstrap qua zip tải-về (xem docstring đầu `scripts/tl_boot.py`). Dùng cả ba lớp.

## 1. NGĂN — khi sửa file skill trong Cowork, ĐỪNG tin tool Edit/Write native. FALLBACK (theo thứ tự ưu tiên):

1. **Ghi bằng Python qua Bash** (né hẳn tầng gây cắt cụt):
   ```bash
   python - <<'PY'
   from pathlib import Path
   Path("scripts/tl.py").write_text(NOI_DUNG_DAY_DU, encoding="utf-8")
   PY
   ```
2. **Heredoc ghi TRỌN file** (không sửa từng dòng):
   ```bash
   cat << 'EOF' > scripts/ten_file.py
   ...toàn văn...
   EOF
   ```
3. **git checkpoint** trước mỗi lô sửa: `git add -A && git commit -m "pre-edit"` → hỏng thì revert.

## 2. PHÁT HIỆN — sau MỖI lần ghi, verify trong terminal (đừng tin Read cache):

- **Một lệnh:**
  ```bash
  python scripts/tl_boot.py verify-integrity        # exit ≠ 0 khi có file hỏng/cắt cụt
  ```
- Thủ công: `wc -l scripts/tl.py` và `md5sum scripts/tl.py` so trước/sau; hoặc `python -c "import ast,sys; ast.parse(open(sys.argv[1],encoding='utf-8').read())" scripts/tl.py` (đỏ = cắt cụt).

## 3. KHÔI PHỤC — THANG LEO theo mức nặng (mount có thể cắt cụt CẢ công cụ recovery)

> **Cốt lõi:** **shell chạy TỪNG DÒNG → sống sót cắt cụt** (chạy tới chỗ bị cắt); **Python parse CẢ file trước khi
> chạy → 1 dòng cụt là chết hẳn.** Khi mount cắt cụt CẢ `_parts` (recovery local bó tay), **mạng giao byte trung thực** →
> tải bản thật từ Drive về `/tmp` là lối thoát chắc nhất. `_parts/MANIFEST.sha256` chỉ rõ mảnh nào mount cắt (thay `SyntaxError` mù).

0. **★ NHANH & CHẮC NHẤT — bỏ qua mount, chạy bản tải-về:** `sh scripts/tl_fetch.sh <args>` (đầy đủ: `--setup --nlm`).
   Zip skill PUBLIC → **curl** `drive.usercontent.google.com` (allowlist, off-context, không token), ghi vào **`$HOME/.tl_fetch`**
   — **KHÔNG `/tmp`** (sticky bit: file rỗng owner `nobody` của lần hỏng trước chặn `curl -o`→exit23 + làm script tưởng
   "đã có"). Fallback: webapp `download` (token) → Drive MCP. Config/token PRIVATE → curl trả trang login → **chỉ Drive MCP**
   lấy được. Verify end-to-end: curl→unzip→`tl.py --selftest` 115/115. **Nếu chính `tl_fetch.sh` bị cắt**, dán lại (path MÌNH sở hữu):
   ```sh
   D=$HOME/.tl_fetch; mkdir -p "$D"
   curl -fsSL "https://drive.usercontent.google.com/download?id=1H5kAt3SRVP7_xmLMIzcqyFtFc4VSDH0P&export=download&confirm=t" -o "$D/skill.zip"
   rm -rf "$D/live"; unzip -oq "$D/skill.zip" -d "$D/live" || { echo "zip hỏng→tải lại"; exit 3; }
   cd "$(dirname "$(dirname "$(find "$D/live" -path '*/scripts/tl.py'|head -1)")")" && python3 scripts/tl.py ping
   ```
   (curl public OK; nếu sandbox CHẶN cả Drive → đổi sang webapp: xem nhánh python trong `tl_fetch.sh`.)
   (curl thẳng Drive chỉ chạy khi allowlist `drive.usercontent.google.com`. Drive file `1H5kAt3SRVP7_…` = zip skill share "anyone with link".)
1. **Chỉ `tl.py` hỏng nhẹ (NUL-pad):** `python scripts/tl_boot.py <args>` — launcher tự strip NUL rồi chạy `tl.py`
   (v1.35.45 r209/H0: cơ chế ghép `_parts/` ĐÃ BỎ — tl_boot chỉ còn strip NUL, xem docstring đầu file).
2. **Nghi cắt cụt bất kỳ file nào:** `python scripts/tl_boot.py verify-integrity` để CHỈ MẶT file hỏng — rồi quay
   lại **bước 0** (`tl_fetch.sh` tải zip SẠCH): từ khi bỏ `_parts/`, KHÔNG còn đường ghép local nào; đừng mất thời
   gian tìm công cụ ghép (bài học H0 26-07: chỉ dẫn cũ trỏ vào `build_parts.py`/`tl_rebuild.sh` chưa từng tồn tại).
3. **Hết cách (egress chặn + zip Drive cũng lỗi):** **RE-SYNC skill** (restart Cowork + cài lại) / `/rewind` /
   revert git ở host.

*(Thư mục skill read-only → bản tải-về chạy từ `$HOME/.tl_fetch`, không ghi đè thư mục skill.)*

## 4. Quy tắc đóng gói (liên quan)
Cơ chế `_parts/` ĐÃ BỎ — KHÔNG còn bước sinh mảnh sau khi sửa. Sau MỌI lần sửa file skill: chạy chuỗi
LỆNH KIỂM CUỐI trong `SKILL.md` (selftest → workflow-audit/determinism-audit --strict → golden-test →
`release-manifest` sinh Ở BƯỚC CUỐI → release-bundle + release-verify --archive).
