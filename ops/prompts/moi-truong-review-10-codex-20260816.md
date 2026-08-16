# CROSS-REVIEW lượt 10 — `ops/moi-truong-ba-p1` head `a3fd3ff` — reviewer `codex`

**CHỈ ĐỌC**: không sửa tệp kho, không commit/push/merge/land/deploy. Người vá là `claude`
⇒ reviewer phải là `codex` (§8). **KHÔNG PHẢI wp55**, không tiêu attempt.

## Bước 0

```bash
git rev-parse --is-shallow-repository   # ĐÒI false
git config --get core.abbrev            # ĐÒI 7
git rev-parse HEAD                      # ĐÒI a3fd3ff705bf4831495b1988de7655b32dc68197
git diff --name-status 1df800be15580d7432a1200900dd04ed9a7b997c HEAD
#   ĐÒI 5 tệp: .claude/dev/codex_env_policy.py · .claude/dev/launcher.py
#              .claude/dev/launcher_test.py · .claude/hooks/session-start.sh · CLAUDE.md
```

## Lượt 9: cả năm mục đúng, và HAI trong số đó là lỗ tôi tự mở khi đang vá lỗ khác

Cờ chặn tôi đặt tên "CODEX BI CHAN" chỉ chặn được một cửa. Writer "nguyên tử" của tôi
dùng tên tạm đoán được nên ghi đè xuyên symlink — hỏng **trước** `os.replace`, phá đúng
hợp đồng viết ở dòng ngay trên. Cả hai đều là *vá một lỗ, mở lỗ khác trong cùng hàm*.

## VIỆC SỐ MỘT — `t72` chập chờn hay phụ thuộc thứ tự?

Lượt 8 nhật ký chạy trọn `100/100` rồi vỏ shell mới chết. Lượt 9 chết **trong `t72`**,
`vao=74 ra=73`. Hai chỗ khác nhau. Nay có chế độ đo lặp:

```bash
probe_home=$(mktemp -d); nk=$(mktemp); mk=$(mktemp)
printf 'truoc\n' > "$mk"
HOME="$probe_home" python3 .claude/dev/launcher_test.py --lap-ca t72 --lan 40 --nhat-ky "$nk"
printf 'rc=%s\n' "$?" >> "$mk"; cat "$mk"
python3 - "$nk" <<'PY'
import sys, re
d = open(sys.argv[1]).read().splitlines()
vao = [re.match(r">>> vao\s+(\d+)", x).group(1) for x in d if x.startswith(">>> vao")]
ra  = {re.match(r"<<< ra\s+(\d+)", x).group(1) for x in d if x.startswith("<<< ra")}
print("lan chay:", len(vao), "| lan xong:", len(ra), "| LAN CHET:", [v for v in vao if v not in ra] or "khong")
print("tron ven:", d and d[-1] == "# XONG TRON VEN")
PY
```

**Ba kết cục, ba kết luận khác nhau — báo đúng cái bạn đo được:**
- 40/40 qua ⇒ `t72` **một mình** không chết; cái chết cần NGỮ CẢNH (các ca chạy trước nó).
- chết ở lần thứ k ⇒ **tự nó chập chờn**; con số k là dữ liệu.
- chết ngay lần 1 ⇒ khác hẳn lượt 8, cần đo lại cả hai.

Tôi đo tại chỗ **40/40 qua**, tức không tái hiện trên nền tôi. **Đừng tin con số của
tôi** — nền của bạn mới là nền lỗi xuất hiện.

Nếu 40/40 qua, chạy tiếp một lượt suite đầy đủ có `--nhat-ky` để xem lần này chết ở đâu.
Hai lượt cùng chỉ vào một ca là bằng chứng; hai lượt hai chỗ vẫn là "chập chờn".

**KHÔNG đoán nguyên nhân.** Đo được đến đâu báo đến đó.

## Delta (một commit, `a3fd3ff`)

### 1. Fail-close thật

Khối thu hồi nay chạy **trước** mọi lời gọi codex trong hook; hai lời gọi đó bọc bằng
`CODEX_BI_CHAN`. `_co_chan_codex()` là chốt dùng chung, cả `_do_codex` lẫn
`_do_codex_song` đọc, **mỗi cửa một đột biến riêng**.

- Còn cửa nào của kho gọi codex mà không qua chốt?
- Tôi khai thẳng là **không chặn được** `codex` gõ tay ở terminal. Phạm vi khai như thế
  đã đúng chưa, hay còn chỗ nào tôi vẫn nói quá?
- `CODEX_BI_CHAN` là biến shell trong hook: có đường nào nó **không** được đặt mà đáng ra
  phải đặt (ví dụ bộ gỡ chết vì lý do khác)?

### 2. So nguyên khối canonical

`_THAN_KHOI_CU` giữ nguyên văn thân khối lấy từ `c7bbd81`. Chuẩn hoá: bỏ khoảng trắng
cuối dòng + dòng trắng đầu/cuối.

- Chuẩn hoá thế **có quá tay** không (một sửa đổi thật của người dùng bị chuẩn hoá mất)?
- Có ca nào khối THẬT của ta bị **từ chối oan** — ví dụ tệp CRLF, BOM, hoặc hook cũ chạy
  trên nền khác sinh ra kết thúc dòng khác?
- Ca `t100(e)` nay bỏ hằng canonical ra trước khi kiểm "không còn đường ghi inherit=all".
  Cách loại trừ đó có tạo lỗ để ai đó nhét lại đường ghi vào chính vùng bị loại không?

### 3. Ghi nguyên tử v2

`mkstemp` (O_EXCL) · từ chối khi đích là symlink · giữ nguyên quyền tệp gốc · `fsync`
thư mục.

- Từ chối symlink có làm ai đó **không bao giờ gỡ được** khối (dotfiles quản lý bằng
  symlink)? Thông điệp đã chỉ đúng đường thoát chưa?
- Giữ nguyên quyền: nếu tệp gốc là `0644` thì ta giữ `0644` — với một tệp cạnh
  `auth.json` thì đó là **đúng** (tôn trọng người dùng) hay **sai** (nên siết)? Nói rõ
  quan điểm, tôi đã chọn "tôn trọng" và có thể chọn sai.
- `mkstemp` tạo tệp `0600` rồi ta `chmod` sang mode gốc — có khoảnh khắc nào lộ quyền rộng?
- Còn đường đua nào giữa `stat` (đọc mode) và `replace`?

### 4. Cờ lặp · 5. `--lap-ca`

- `t101` phủ đủ chưa? `--lan` không kèm `--lap-ca` bị từ chối; `--lan 0` bị từ chối.
- `--lap-ca` khớp theo **tiền tố**: hai ca cùng tiền tố thì nó từ chối — đúng chưa?

## Bản khai + hai lượt `--dot-bien`

Dán lại bản khai; chạy `--dot-bien` **hai lần**. Bốn lượt gần nhất hai bên ra cùng con số.

## CẢNH BÁO AN NINH

Không in **giá trị** biến môi trường hay token. `HOME=$(mktemp -d)`. **Không** đụng
`~/.codex/auth.json` hay `~/.codex/config.toml` thật — có
`.claude/dev/fixtures/config_codex_mau.toml` và `--tep <tệp tạm>`.

## Verdict

`approve` · `changes_requested` · `blocked`. Neo SHA bất biến. **Năm lượt liền
`changes_requested` không phải hạn ngạch** — `approve` hợp lệ nếu thật sự không tìm ra gì,
và nói thẳng nếu bạn cho rằng nhánh này nên dừng lại thay vì vá tiếp.

Ghi verdict RA TỆP:

```
ops/reviews/moi-truong-review-10-codex-verdict.md
ops/reviews/moi-truong-review-10-codex-verdict.receipt.yaml
```

Báo `sha256` + số byte.
