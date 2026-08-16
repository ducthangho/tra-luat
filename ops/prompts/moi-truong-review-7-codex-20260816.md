# CROSS-REVIEW lượt 7 — `ops/moi-truong-ba-p1` head `69bc3ce` — reviewer `codex`

**CHỈ ĐỌC**: không sửa tệp kho, không commit/push/merge/land/deploy. Người vá là `claude`
⇒ reviewer phải là `codex` (§8). **KHÔNG PHẢI wp55**, không tiêu attempt của packet.

## Bước 0

`git fetch`/`git config` không chạy được trong vai này (sandbox codex đặt `.git/` chỉ đọc).
Điều phối chạy hộ trong chính clone bạn đứng. Xác minh **bằng đọc**:

```bash
git rev-parse --is-shallow-repository   # ĐÒI false
git config --get core.abbrev            # ĐÒI 7
git rev-parse HEAD                      # ĐÒI 69bc3cede6085bf6229ac95a44da4aae9e51ee42
git diff --name-status c775c0a5b0bf0816e913ba0b300d898fec3c58b0 HEAD
#   ĐÒI 5 tệp: .claude/dev/launcher.py · .claude/dev/launcher_test.py
#              .claude/hooks/session-start.sh · CLAUDE.md · docs/GOI_AGENT_DA_NEN.md
```

Không tin thì **nêu thành finding và VẪN LÀM TIẾP** — mỏ neo là SHA bất biến.

## Trước hết: lượt 6 của bạn ĐÚNG cả bốn mục, và tôi đã đăng con số SAI

Lease lượt 6 ghi `dot_bien: 50/50 đạt, KHÔNG mục nào SAI`. Đo lại hai lượt ở đúng
`c775c0a`: `49/50`, mutant `do_codex_tin_DONG_DAU_thay_vi_ma_thoat` `giet 0/1`. Bạn đúng.
Đã đăng đính chính công khai trên #55.

## Delta: BỐN commit

```
71aa638  CẢNH BÁO SỚM trước khi credential codex hết hạn        <- CHƯA AI SOI
c7bbd81  mở CODEX_AUTH_JSON cho codex qua shell_environment_policy  <- CHƯA AI SOI
2348e63  sửa hai lỗi của chính bản vá cảnh báo sớm             <- CHƯA AI SOI
69bc3ce  ba P1 + một P2 của lượt 6
```

Ba commit đầu rẽ ra trong lúc lượt 5 chết vì credential bị thu hồi, nên **chưa ai soi**.

## Việc của lượt này

### 1. Cổng đột biến đang CHẤM ĐIỂM NHẦM BẢN — mục nặng nhất

Truy `giet 0/1` của bạn tới cùng thì không phải mutant hết răng: runner ghi **mọi** bản
đột biến vào **cùng một đường dẫn** tạm, mà CPython coi `.pyc` còn hợp lệ theo
**(mtime tính bằng GIÂY, kích thước nguồn)**. Đột biến #3 và #4 tình cờ ra tệp **cùng
129395 byte**; hai lượt ghi rơi cùng một giây ⇒ #4 **không bao giờ được biên dịch**,
Python phục vụ lại mã của #3.

A/B: `dont_write_bytecode=0` ⇒ `0/1` · `=1` ⇒ `1/1`. Gỡ cả ba lớp vá ra thì mutant canh
bản vá `killpg` **cũng câm** — cơ chế tước răng bất kỳ mutant nào.

Đây cũng là lời giải tôi đề xuất cho ba lượt "cùng cổng, hai kết quả": va chạm chỉ xảy ra
khi hai lượt ghi lọt cùng một giây, tức phụ thuộc máy.

**Hỏi thẳng bạn:**
- Lời giải này có đủ giải thích con số của **bạn** không? Chạy `--dot-bien` trên
  `c775c0a` (bản CŨ) rồi trên `69bc3ce` — nếu lời giải đúng, mutant đó phải chuyển từ
  `SAI` sang `OK`. Nếu **không** chuyển thì lời giải của tôi sai, nói thẳng.
- Bốn lớp (`xoá .pyc` · tắt ghi bytecode · `invalidate_caches` · tên tệp riêng) có lớp
  nào **thừa** hoặc **giả**? Tôi đã đo: lớp "tắt ghi bytecode" lúc đầu **không có răng**
  (gỡ ra mà `t97` vẫn xanh), phải thêm phép đo thẳng. Còn lớp nào như thế nữa không?
- `_nap_sach` nay xoá `.pyc` — có xoá nhầm gì ngoài phạm vi không? Có ca nào tệp không
  ghi được / `cache_from_source` ném lỗi mà ta nuốt im?

### 2. Chốt trưởng nhóm sau khi bịt fail-open

`killpg` nay chỉ chạy khi ĐO ĐƯỢC và `pgid == pid`. Không đo được ⇒ giết qua `_giet_rieng`
trên ảnh chụp (từng pid, có khoá danh tính). Không killpg mà ảnh chụp rỗng ⇒ `tu_choi`.

- Còn đường nào tới `killpg` không qua chốt?
- `_con_lai()` khi **không** dùng killpg lấy phần nhóm là `[]`. Tôi khai đó là "nhóm không
  thuộc phạm vi nhận trách nhiệm", không phải "nhóm đã rỗng". Cách khai đó có làm
  `me_da_chet`/`ca_cay` nói dối ở ca nào không?
- Khe tôi khai thẳng: tiến trình **gia nhập nhóm SAU** lúc chụp thì `_giet_rieng` không
  với tới. Khe đó có rộng hơn tôi nghĩ không?
- `t92(c)` **đảo chiều** so với bản trước (đang ghim fail-open ⇒ nay cấm). Đổi kỳ vọng một
  ca sẵn có luôn đáng soi: đúng hợp đồng, hay nới cho vừa bản vá?

### 3. `chua_chung_minh` + danh sách TRẮNG

`DA_CHUNG_MINH_KHA_DUNG = {"DUNG_DUOC"}`. `SAP_HET_HAN`, `KHONG_DO_DUOC`, `CO_CREDENTIAL`,
`THIEU` đều rơi vào "chưa chứng minh". `--doi-kha-dung` fail-closed; **mặc định giữ 0** để
không dựng chốt đỏ thường trực.

- Chọn mặc định rộng lượng như thế có làm chốt vô dụng ở đúng chỗ cần chặn không?
- `t98` ghim bảng `KHA_NANG`/`CONG_CU` để khỏi phụ thuộc máy. Ghim như thế có làm ca mất
  liên hệ với hành vi thật không?

### 4. Ba commit chưa ai soi

- `71aa638`/`2348e63` — cảnh báo sớm: ngưỡng 24h, `_TOKEN_KHONG_XET_HAN` loại `id_token`
  ở **hai** tầng (thu thập + quyết định), `tuoi_anh_chup_gio`. Có chỗ nào cảnh báo sớm
  biến thành **chốt đỏ thường trực** không? Có rò giá trị token qua thông điệp không?
- `c7bbd81` — ghi `[shell_environment_policy] inherit="all"` + `exclude` vào
  `~/.codex/config.toml`. **Mở toàn bộ môi trường cho tiến trình con của codex.** Danh sách
  `exclude` có đủ không? Khối đặt TRƯỚC mọi bảng `[projects...]` (TOML buộc khoá vào bảng
  gần nhất phía trên) — kiểm giúp, và kiểm tính bất biến khi chạy lại nhiều lần.
  Nếu bạn cho rằng `inherit="all"` nay là **thừa** (đã có `device-auth` đúc credential tại
  chỗ) hoặc **có hại**, nói thẳng — đó là finding có giá trị.

### 5. Bản khai môi trường + hai lượt `--dot-bien`

Lượt 6 là lần đầu hai bên có bản khai để so, và nó đổi hẳn chẩn đoán: bạn `pid=4 pgid=1
sid=1`, tôi `17306/17306/17306`; hai PID namespace khác nhau. **Dán lại bản khai của bạn**
và chạy `--dot-bien` **hai lần**.

Suite chuẩn ở lượt 6 **giết caller** bên bạn (dừng sau `t62`, không tổng kết) trong khi
bên tôi `93/93` và vỏ shell sống. Nếu bịt fail-open `killpg` là đúng nguyên nhân thì
**lượt này suite phải chạy hết bên bạn**. Nếu vẫn chết, đó là finding HIGH và là bằng
chứng giả thuyết của tôi sai — báo thẳng, đừng nương.

## CẢNH BÁO AN NINH

Không in **giá trị** biến môi trường hay token. Phản chứng đụng credential chạy trên
`HOME=$(mktemp -d)`; **không** đụng `~/.codex/auth.json` thật.

## Verdict

`approve` · `changes_requested` · `blocked`. Bằng chứng **neo SHA bất biến**. Nói thẳng chỗ
không chạy được. `approve` hợp lệ nếu thật sự không tìm ra gì.

Ghi verdict RA TỆP:

```
ops/reviews/moi-truong-review-7-codex-verdict.md
ops/reviews/moi-truong-review-7-codex-verdict.receipt.yaml
```

Xuất thẳng `stdout` ra tệp, báo `sha256` + số byte.
