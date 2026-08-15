# CROSS-REVIEW lượt 3 — nhánh `ops/moi-truong-env-first` head `c89ca59` — reviewer `codex`

Bạn là **reviewer độc lập**. **CHỈ ĐỌC**: không sửa tệp kho, không commit, không push,
không merge, không land, không deploy. Đầu ra là **verdict** + **evidence §7**.

Người vá là `claude` ⇒ reviewer phải là `codex` (§8). Không phải `codex` thì **DỪNG**.

**KHÔNG PHẢI wp55.** Nhánh rẽ từ `master`, sửa hạ tầng môi trường. `la_viec_cua_packet:
false` — không tiêu attempt của packet.

---

## Bước 0 — hai lệnh KHÁC prompt, đã xử lý sẵn

`git fetch` và `git config` **không chạy được** trong vai này: sandbox `workspace-write`
của `codex` đặt `.git/` thành chỉ đọc theo chính sách của chính codex (đã đo: clone
**độc lập** nằm trọn trong vùng ghi được vẫn hỏng y hệt). Phiên điều phối chạy hộ cả hai
**trong chính clone bạn đứng**. Bước 0 của bạn là **xác minh bằng đọc**:

```bash
git rev-parse --is-shallow-repository       # ĐÒI false
git config --get core.abbrev                # ĐÒI 7
git rev-parse HEAD                          # ĐÒI c89ca5929c2d5da6c182f7858e652c51df147cd5
git rev-parse origin/ops/moi-truong-env-first
git remote -v                               # ĐÒI github.com/ducthangho/tra-luat
git diff --name-status 026c4ea95ae5039ce32f794018a69f03a94bf41a c89ca5929c2d5da6c182f7858e652c51df147cd5
#   ĐÒI ĐÚNG 1 tệp: .claude/dev/launcher_test.py
```

Không tin "fetch do người khác chạy" thì **nêu thành finding và VẪN LÀM TIẾP** — mọi mỏ
neo là SHA bất biến, khớp SHA bất biến mạnh hơn độ tươi của ref.

---

## Delta: ĐÚNG MỘT TỆP, đáp lại finding HIGH của chính bạn

Lượt 2 bạn ra `launcher-tests-leak-global-module-monkeypatches` (HIGH):
`_tai_launcher_thu()` nạp module launcher mới nhưng module ấy dùng **chính** các singleton
`os` / `shutil` / `subprocess` / `platform` của tiến trình test; các ca gán đè mà không
khôi phục, nên `t85` làm bẩn `subprocess.run` và cổng đột biến đổ ba mục.

Bản gốc verdict lượt 2: `ops/reviews/moi-truong-review-2-codex-verdict.md` trên
`ops/moi-truong-review-2-verdict`, sha256
`0b28a66da5765f05384ddf724e5f88f95c5046f85745a0a07bae21f35ec4a390`. **Đọc bản gốc.**

### Bản vá

Chữa **ở tầng harness**, không chữa từng chỗ gọi: `_co_lap_toan_cuc()` chụp rồi hoàn
nguyên `os.environ` · `platform.system` · `subprocess.run` · `shutil.which` ·
`os.path.expanduser`, bọc quanh **mọi** lượt gọi ca ở **cả hai** vòng lặp (suite chuẩn và
runner đột biến). `os.environ` hoàn nguyên **cả nội dung**, không chỉ tham chiếu.

Lý do chọn tầng harness: sửa 14 chỗ gán thì hôm nay sạch, ca thứ 15 viết tháng sau lại rò
— và rò **im lặng**, chỉ hiện ra ở một mục không liên quan cách đó vài trăm dòng.

Người vá đo: cô lập BẬT → **0** ca làm bẩn toàn cục; cô lập TẮT → bẩn ngay từ `t81`
(ca của **master**, không phải ca mới).

---

## Việc của lượt này

### 1. Bản vá có THẬT SỰ đủ không

- Danh sách `_TOAN_CUC_CAN_CO_LAP` có **năm** mục. Còn singleton nào ca test đụng mà
  **chưa** nằm trong danh sách không? Quét cả tệp, đừng tin danh sách.
- Ca test có đường nào làm bẩn trạng thái toàn cục **ngoài** phạm vi năm mục đó không —
  `sys.path`, `sys.modules`, biến môi trường qua `os.putenv`, thư mục làm việc (`os.chdir`),
  `signal`, `atexit`, tệp còn sót?
- `os.environ` hoàn nguyên bằng `clear()` + `update()`. Có ca nào giữ **tham chiếu** tới
  `os.environ` cũ rồi thao tác tiếp sau khi hoàn nguyên không? Hoàn nguyên kiểu này có
  làm hỏng `os.environb` hay biến con-tiến-trình không?
- Bọc `with` quanh lời gọi ca **nhưng không** quanh code ở mức module. Có ca nào vá toàn
  cục **lúc import** không?

### 2. Con số có đáng tin hơn lần trước không

Người vá TỰ RÚT LẠI con số `47/47` đã công bố trước đó, vì nó đo trên harness bị ô nhiễm.
Số mới:

```
standard suite   89/89 (qua 88, bỏ qua 1 fixture Windows, hỏng 0)
cổng đột biến    47/47 đạt, KHÔNG còn mục SAI (1 không đo được trên nền này)
                 ba mục từng đổ nay đều giết được ca đích
eol checked=330 violations=0 · doc-claims flags=[]
```

**Tự chạy, đừng chép.** Và chạy `--dot-bien` **ít nhất hai lần** — chính chỗ này lần
trước cho hai kết quả khác nhau. Khác nhau giữa hai lượt là finding.

```bash
python3 .claude/dev/launcher_test.py
python3 .claude/dev/launcher_test.py --dot-bien
python3 .githooks/eol_policy.py --all --json
python3 scripts/tl.py doc-claims-check --strict --json
```

### 3. Chỗ người vá KHAI là giới hạn — phán định xem có đúng là giới hạn không

Không có đột biến nào cho `_co_lap_toan_cuc`. Lý do người vá đưa: runner đọc
`goc = LAUNCHER.read_text()` nên chỉ đột biến `launcher.py`, còn chốt cô lập sống trong
`launcher_test.py` — ngoài tầm với. Người vá nói đã THỬ đặt hai mục và cả hai trả
"khong tim thay doan de dot bien", nên bỏ hẳn vì một mục **đỏ thường trực** là thứ sẽ bị
bỏ qua.

**Đây là lập luận cần bạn phán định, không phải kết luận đã chốt.** Có cách cơ học nào
khoá chốt harness mà không cần bảng đột biến hiện tại không? Nếu không có, `t89` một mình
có đủ mạnh không — nó khẳng định trực tiếp cả đường ném ngoại lệ giữa chừng.

### 4. `t89` có RĂNG không

Đột biến chính `t89` (bỏ chụp, bỏ hoàn nguyên nội dung `os.environ`, bỏ `finally`) trên
**bản sao** rồi xem nó có đỏ không. Đây là ca duy nhất canh chốt harness, nên nếu nó mù
thì cả cơ chế mù theo.

### 5. Phần delta trước đã duyệt — ĐỪNG soi lại

Lượt 2 đã xác nhận: bản vá oracle đúng hướng; ngưỡng 8 không đủ thành finding chặn; va
chạm HMAC 32 bit không đáng nâng; không có đường in plaintext credential; đột biến t85 gỡ
hai lớp là hợp lệ; `hook-nang-luc` fail-closed khi gõ sai tên; `parents[2]` của t88 đúng.
Chỉ nêu lại nếu bạn **đo được điều khác**.

---

## CẢNH BÁO AN NINH

Nhánh này đụng credential thật.

- **KHÔNG in GIÁ TRỊ** biến môi trường nào, kể cả một phần, kể cả để chứng minh. Chỉ nêu
  TÊN, ĐỘ DÀI, nhãn nhóm. `CODEX_AUTH_JSON` chứa refresh token.
- Mọi phản chứng đụng credential **chạy trên `HOME=$(mktemp -d)`**. TUYỆT ĐỐI không
  ghi/xoá/đổi `~/.codex/auth.json` thật — credential đang nuôi chính phiên bạn.
- Phép đo nào buộc phải đụng tệp thật thì **ĐỪNG LÀM**, ghi vào `boundaries`.

## Verdict và evidence

`approve` · `changes_requested` · `blocked`. Mỗi finding: `finding_id` kebab-case,
`severity`, `disposition`, **bằng chứng chạy được neo SHA bất biến** + lệnh nguyên văn.
Không tái lập được thì ghi rõ là **nghi vấn**. **Nói thẳng chỗ bạn KHÔNG chạy được.**

`approve` là verdict hợp lệ nếu thật sự không tìm ra gì — đừng nặn finding cho có. Ngược
lại, delta này **chưa ai soi**, và hai lượt trước bạn đều tìm ra finding HIGH ở đúng vùng
mã này.

Mọi lệnh trong verdict phải neo **SHA bất biến**.

### Giao kết quả

REST tới `api.github.com` bị proxy 403, `gh` không cài ⇒ ghi verdict RA TỆP:

```
ops/reviews/moi-truong-review-3-codex-verdict.md
ops/reviews/moi-truong-review-3-codex-verdict.receipt.yaml
```

Xuất **thẳng `stdout` ra tệp**, đừng chép tay. Báo `sha256` + số byte.

## Stop conditions

Head đổi giữa chừng · lease hết hạn · bạn không phải `codex` · bước 0 lệch (trừ hai lệnh
đã nêu) · bị đòi sửa tệp/commit/push/merge/land · không chạy được phần thiết yếu (báo
`blocked` kèm lý do ĐO ĐƯỢC, đừng đoán rồi `approve`) · chạm quota.
