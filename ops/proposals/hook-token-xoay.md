# Đề xuất: hook không nạp được credential MỚI sau khi token bị xoay

**Trạng thái:** CHƯA ÁP. Soạn cho phiên đang giữ `ops/moi-truong-ba-p1`.
`.claude/hooks/session-start.sh` nằm NGOÀI `write_set` của wp55, và đang do phiên khác sửa —
nên đây là đề xuất, không phải bản vá.

## Sự cố đã xảy ra thật, 15–16/08

1. Phiên executor in nguyên `CODEX_AUTH_JSON` ra transcript (lỗi riêng, đã ghi ở
   `ops/bai-hoc/2026-08-15-ro-ri-secret-hai-lan.md`).
2. Chủ kho thu hồi và cấp lại credential — đúng phản ứng cần có.
3. Biến `CODEX_AUTH_JSON` trong môi trường phiên **đã đổi** (5648 → 5868 ký tự).
4. Nhưng `~/.codex/auth.json` trên đĩa **vẫn là bản cũ**, và hook KHÔNG nạp bản mới.
5. `codex exec` chết ngay: `refresh_token_invalidated`, `401`.

Phải khôi phục **bằng tay** mới chạy tiếp được.

## Nguyên nhân — chốt số 2 đúng ý ĐỊNH, sai ĐIỀU KIỆN

`.claude/hooks/session-start.sh` (bản `a3fd3ff`, dòng 219–221):

```bash
if [ -n "${CODEX_AUTH_JSON:-}" ] && co codex && [ "${CODEX_BI_CHAN:-0}" = 0 ]; then
  if codex login status >/dev/null 2>&1 </dev/null; then
    echo "[session-start] codex: da dang nhap san — GIU nguyen, khong ghi de"
```

Ý định của chốt là đúng và đáng giữ: **bản trên đĩa có thể MỚI HƠN biến**, vì codex tự làm
mới token rồi ghi lại `last_refresh`; đè bừa là hạ cấp một credential đang tốt.

Cái sai nằm ở **cách hỏi**. `codex login status` chỉ **đọc tệp**, không hỏi máy chủ. Đo được
trong phiên 16/08 khi token đã bị thu hồi:

```
$ codex login status
Logged in using ChatGPT          ← token đã CHẾT
$ codex exec …
ERROR: refresh token was revoked
```

Nên chốt trả lời "đã đăng nhập" cho một token đã chết, hook bỏ qua, và phiên chạy với
credential hỏng. Cùng họ với bài học đã ghi: **`doctor` nói CÓ codex, không nói codex GỌI
ĐƯỢC** — nay thêm: **`login status` nói CÓ TỆP, không nói tệp còn HIỆU LỰC.**

## Phép phân biệt đúng — so `refresh_token`, không hỏi `login status`

Hai tình huống cần tách, và `refresh_token` tách được chúng mà không cần gọi mạng:

| | `refresh_token` biến vs đĩa | nghĩa | phải làm |
|---|---|---|---|
| codex tự làm mới token | **GIỐNG** | cùng credential, đĩa có thể mới hơn | **GIỮ đĩa** — đúng ý chốt cũ |
| chủ kho xoay credential | **KHÁC** | credential mới hẳn, đĩa đã chết | **GHI biến đè lên đĩa** |

Đo trên dữ liệu thật của phiên 16/08 sau khi khôi phục tay: `refresh_token` biến == đĩa,
`last_refresh` hai bên bằng nhau ⇒ nhánh "giữ đĩa" đúng, không đè oan.

## Diff đề xuất

Thay khối điều kiện, giữ nguyên bốn chốt an toàn cũ (không in giá trị, kiểm JSON trước khi
ghi, ghi qua tệp tạm + `chmod 600`):

```diff
 if [ -n "${CODEX_AUTH_JSON:-}" ] && co codex && [ "${CODEX_BI_CHAN:-0}" = 0 ]; then
-  if codex login status >/dev/null 2>&1 </dev/null; then
-    echo "[session-start] codex: da dang nhap san — GIU nguyen, khong ghi de"
+  # KHONG hoi `codex login status`: lenh ay chi DOC TEP, khong hoi may chu, nen no bao
+  # "Logged in" cho ca mot token DA BI THU HOI. Do duoc 16-08: login status tra 0 trong
+  # khi `codex exec` chet voi refresh_token_invalidated. Chot cu vi the bo qua dung luc
+  # can nap nhat — sau khi chu kho xoay credential.
+  #
+  # Phep phan biet dung: so `tokens.refresh_token` giua BIEN va DIA.
+  #   GIONG  => cung credential, dia co the moi hon (codex tu lam moi) => GIU DIA
+  #   KHAC   => credential da bi XOAY => GHI BIEN de len dia
+  # Khong goi mang, khong in gia tri.
+  if "$PY" - <<'PYEOF'
+import base64, json, os, sys
+def rt(d):
+    return ((d or {}).get("tokens") or {}).get("refresh_token", "")
+try:
+    moi = json.loads(base64.b64decode(os.environ.get("CODEX_AUTH_JSON", "").strip(), validate=True))
+except Exception:
+    sys.exit(1)                      # bien hong => de nhanh duoi bao loi dung khuon
+p = os.path.join(os.path.expanduser("~"), ".codex", "auth.json")
+try:
+    with open(p, encoding="utf-8") as f:
+        cu = json.load(f)
+except Exception:
+    sys.exit(1)                      # chua co tep => phai ghi
+sys.exit(0 if rt(moi) and rt(moi) == rt(cu) else 1)
+PYEOF
+  then
+    echo "[session-start] codex: auth tren dia CUNG credential voi bien — GIU nguyen"
```

Phần `else` (khối khôi phục hiện có) giữ nguyên không đổi.

## Ca kiểm đề nghị — cả hai chiều

| ca | dựng thế nào | đòi |
|---|---|---|
| credential bị xoay | biến có `refresh_token` khác đĩa | **GHI ĐÈ**, đĩa mang giá trị của biến |
| codex tự làm mới | cùng `refresh_token`, đĩa có `last_refresh` mới hơn | **GIỮ ĐĨA**, không đè |
| chưa có tệp | xoá `~/.codex/auth.json` | **GHI** |
| biến hỏng | `CODEX_AUTH_JSON` không phải base64 | **KHÔNG ghi**, cảnh báo, không traceback |
| biến rỗng/chưa đặt | unset | bỏ qua cả khối |

Ca thứ hai là ca chống hồi quy cho chính chốt cũ — đừng bỏ, nó là lý do chốt cũ tồn tại.

## Điều KHÔNG đề xuất

**Đừng thay bằng một lời gọi mạng thật** (`codex exec` thử). Nó chậm, phụ thuộc mạng, và
biến `SessionStart` thành chỗ có thể treo. Phép so `refresh_token` trả lời đúng câu hỏi cần
hỏi — *biến và đĩa có phải cùng một credential không* — mà không rời khỏi máy.

## Liên quan tới việc phiên môi trường đang làm

Bản `a3fd3ff` đã sửa nhiều thứ quanh khối này (thêm `CODEX_BI_CHAN`, đổi thứ tự đặt biến so
với hai lời gọi `codex login status`), nhưng **chốt số 2 chưa đổi**. Nếu đường sửa của các
bạn đã chạm tới nó theo cách khác thì bỏ qua đề xuất này — chỉ xin kiểm giúp ca "credential
bị xoay", vì nó đã hỏng thật một lần và mất khoảng một giờ để phát hiện.
