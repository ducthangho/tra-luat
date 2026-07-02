# COWORK_EDIT_SAFETY — chống cắt cụt khi SỬA file skill (mount Cowork #51435/#53940)

Bug: tool **Edit/Write native của Cowork** đôi khi **cắt cụt file** — clamp độ dài về kích thước file TRƯỚC khi sửa,
và **Read có thể trả cache cũ** nên không thấy hỏng ngay. Skill có phòng thủ 3 lớp; tài liệu này là lớp **NGĂN** (write-side).

> Lớp 1 NGĂN (write-side, dưới đây) · Lớp 2 PHÁT HIỆN (`tl verify-integrity`; `build_parts.py --verify` so
> `_parts/MANIFEST.sha256`) · Lớp 3 KHÔI PHỤC — **★ `tl_fetch.sh` (tải từ Drive về /tmp, BỎ QUA mount) là chắc nhất**;
> local: `_parts/` + `_healed_script_path` + `tl_rebuild.sh` (shell) + `build_parts.py --rebuild`. Dùng cả ba.

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

- **Một lệnh, đối chiếu toàn bộ với `_parts/`:**
  ```bash
  python scripts/tl_boot.py verify-integrity        # ✓OK ·NOPARTS ~DRIFT ⚠NUL ✗TRUNCATED/MISSING ; exit 2 nếu có lỗi
  ```
- Thủ công: `wc -l scripts/tl.py` và `md5sum scripts/tl.py` so trước/sau; hoặc `python -c "import ast,sys; ast.parse(open(sys.argv[1],encoding='utf-8').read())" scripts/tl.py` (đỏ = cắt cụt).
- **DRIFT** = file compile được nhưng KHÁC `_parts/` → bạn vừa sửa hợp lệ; **chạy lại `python scripts/build_parts.py`** để cập nhật mảnh (BẮT BUỘC sau mỗi lần sửa file đã-chunk, nếu không recovery sẽ ghép ra bản CŨ).

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
1. **Chỉ `tl.py` cắt cụt (tl_boot còn sống, mount local lành phần khác):** `python scripts/tl_boot.py <args>` — tự ghép
   `tl.py` từ `_parts/tl/`, verify sha (bắt cả ca "compile được nhưng mangled"). Script subprocess tự lành qua `_healed_script_path`.
2. **Sửa tại chỗ từ `_parts/`:** `python scripts/tl_boot.py verify-integrity --fix` (ghép lại TRUNCATED/NUL/MISSING,
   ghi bằng Python; không đụng DRIFT).
3. **`tl_boot.py` HOẶC `build_parts.py` cũng cắt cụt (Python recovery chết):** dùng **shell**:
   ```sh
   sh scripts/tl_rebuild.sh                 # ghép MỌI _parts -> /tmp/tl_rebuilt, verify MANIFEST, báo mảnh hỏng
   python /tmp/tl_rebuilt/tl.py <args>
   ```
4. **Soi mảnh nào mount cắt (chẩn đoán):** `python scripts/build_parts.py --verify` (hoặc, không cần Python:
   `cd scripts && sha256sum -c _parts/MANIFEST.sha256 | grep -v ': OK$'`).
5. **MẢNH `_parts` cũng bị mount cắt** (MANIFEST báo lệch / `tl_rebuild.sh` exit 3): ghép local KHÔNG cứu được →
   quay lại **bước 0 (`tl_fetch.sh` tải từ Drive)** — đây mới là lối thoát khi mount giao bản hỏng cho cả nguồn lẫn mảnh.
   Hết cách nữa (egress chặn + zip Drive cũng lỗi) → **RE-SYNC skill** (restart Cowork + cài lại) / `/rewind` / revert git ở host.

*(Thư mục skill read-only → mọi bản ghép ra ghi vào `/tmp` (writable), không ghi đè thư mục skill.)*

## 4. Quy tắc đóng gói (liên quan)
Mỗi lần bump version / sửa `*.py`: **chạy `python scripts/build_parts.py`** để `_parts/` khớp on-disk (build_parts tự
verify `ghép==gốc`). `FORCE_CHUNK` đảm bảo bootstrap + script subprocess luôn có `_parts/` dù nhỏ. Xem `build_parts.py`.
