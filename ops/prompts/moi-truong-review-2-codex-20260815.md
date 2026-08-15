# CROSS-REVIEW lượt 2 — nhánh `ops/moi-truong-env-first` head `026c4ea` — reviewer `codex`

Bạn là **reviewer độc lập**. Vai này **CHỈ ĐỌC**: không sửa tệp kho, không commit, không
push, không merge, không land, không deploy. Đầu ra là **verdict** + **evidence §7**.

Người vá là `claude` ⇒ reviewer phải là `codex` (§8). Không phải `codex` thì **DỪNG**.

**ĐÂY KHÔNG PHẢI wp55.** Nhánh rẽ từ `master`, sửa hạ tầng môi trường, không đụng
`packet_loop*`. Lease dùng issue #55 làm luồng điều phối nhưng `la_viec_cua_packet: false`
— nó **không** tiêu attempt của packet.

---

## Bước 0 — MÔI TRƯỜNG KHÁC PROMPT Ở ĐÚNG HAI LỆNH, đọc trước khi làm

`git fetch` và `git config` **không chạy được** trong vai này: sandbox `workspace-write`
của `codex` đặt `.git/` thành chỉ đọc theo chính sách của chính codex. Đã đo: ngay trong
một clone **độc lập** nằm trọn trong vùng ghi được vẫn trả
`could not lock config file .git/config: Read-only file system`.

Lượt review TRƯỚC của nhánh này đã `blocked` đúng ở chỗ đó, và nó ĐÚNG khi dừng — lỗi là
của người giao việc. Nên phiên điều phối chạy hộ cả hai **trong chính clone bạn đứng**,
và bước 0 của bạn là **xác minh bằng đọc**:

```bash
git rev-parse --is-shallow-repository       # ĐÒI false
git config --get core.abbrev                # ĐÒI 7
git rev-parse HEAD                          # ĐÒI 026c4ea95ae5039ce32f794018a69f03a94bf41a
git rev-parse origin/ops/moi-truong-env-first
git remote -v                               # ĐÒI github.com/ducthangho/tra-luat
git diff --name-status 0194ea0eea9d4b9eed569059f1bda9775ad92971 026c4ea95ae5039ce32f794018a69f03a94bf41a
#   ĐÒI ĐÚNG 3 tệp: launcher.py · launcher_test.py · session-start.sh
sha256sum <đường dẫn prompt này>            # ĐÒI khớp prompt_sha256_required
```

Nếu bạn cho rằng "fetch do người khác chạy" là chưa đủ tin, hãy **nêu thành finding** và
**vẫn làm tiếp**. Đừng dừng cả lượt vì riêng mục đó: mọi mỏ neo ở đây là SHA bất biến,
mà khớp SHA bất biến là bằng chứng mạnh hơn độ tươi của ref.

---

## Bối cảnh: lượt 1 đã duyệt tới `0194ea0`, đây là DELTA hai commit

Verdict lượt 1: `changes_requested`, một finding mức HIGH —
`deterministic-secret-fingerprint-is-dictionary-oracle`. Bản gốc:
`ops/reviews/moi-truong-review-1-codex-verdict.md` trên `ops/moi-truong-review-1-verdict`,
sha256 `54139baff2789cd2da4f36661e563ed33bdc95495518b3161458803c033ad6fc`.
**Đọc bản gốc, đừng đọc tóm tắt.**

Lượt 1 đã xác nhận nhiều thứ (hợp đồng `doctor`, bốn chốt `chuan_bi_xac_thuc`, không còn
bệnh `set -e`, tài liệu khai đúng). Những mục đó **không cần soi lại** trừ khi delta đụng
vào. Việc của lượt này là **hai commit mới**:

```
0d05c61  bịt oracle (đáp lại finding HIGH của chính bạn)
026c4ea  vá nốt hai điểm bạn nêu mà không xếp thành finding
```

---

## 1. `0d05c61` — bản vá oracle. ĐÂY LÀ AN NINH, soi kỹ nhất.

Thay đổi:

- `_van_tay` từ **sha256 trần** → **HMAC khoá ngẫu nhiên mỗi tiến trình** (`_KHOA_PHIEN`,
  `secrets.token_bytes(32)`, không bao giờ xuất).
- Đầu ra **bỏ hẳn** trường `van_tay`; thay bằng **nhãn nhóm thứ tự** (`nhom-1`), chỉ đặt
  cho nhóm có từ 3 biến trở lên.
- Độ dài giá trị **ngắn** gộp thành `<8`; giá trị dài vẫn in số chính xác.

Người vá đo: từ điển 4 ứng viên → 0 khớp; `van_tay` không còn trong đầu ra; nhóm 5 biến
giữ chỗ **vẫn** bị phát hiện.

**Hỏi ngược — đừng dừng ở "đã bỏ digest là xong":**

- Còn **oracle nào khác** không? Bộ ba `nhom` + `nghi_giu_cho` + `do_dai` tự nó nói
  "năm biến này CÙNG một giá trị dài 14". Với kẻ biết bối cảnh, thế đã đủ chưa?
- **Độ dài chính xác của giá trị DÀI** có đáng lo không? Ngưỡng 8 là con số người vá tự
  đặt, không có căn cứ đo. Phán định xem nó đúng chỗ hay tuỳ tiện.
- `_KHOA_PHIEN` sinh ở **mức module**. Có đường nào cùng một tiến trình xuất nhãn ra hai
  lần rồi bị nối lại không? `--json` chạy hai lần trong cùng tiến trình thì sao?
- HMAC-SHA256 cắt còn **8 hex (32 bit)**. Trong CÙNG một lượt, va chạm 32 bit có làm hai
  giá trị KHÁC nhau bị gom nhầm thành "cùng giá trị" không? Xác suất thực tế bao nhiêu,
  và gom nhầm thì hậu quả là gì (báo oan "giữ chỗ")?
- Còn đường nào **in giá trị** trong toàn nhánh không — kể cả gián tiếp qua traceback,
  `repr()`, thông điệp lỗi của `chuan_bi_xac_thuc`, hay log của chính lệnh?

## 2. `026c4ea` — `hook-phien` đo NĂNG LỰC thay vì băm toàn tệp

Đáp lại đúng điều bạn nêu: so băm cả tệp thì sửa chú thích cũng đỏ, mà chốt đỏ vì lý do
vô hại là chốt bị bỏ qua. Bạn cũng đã loại đường tổ tiên commit.

Cơ chế mới: hook khai `# hook-nang-luc: <tên> <tên> …`; `_do_hook_cu` so **tập tên** giữa
hook đang checkout và hook trên `origin/master`. Thiếu tên nào báo tên đó. Hook cũ không
khai gì ⇒ tập rỗng ⇒ thiếu tất cả. Master chưa khai ⇒ `KHONG_DO_DUOC`, **không** tụt về
so băm.

**Hỏi ngược:**

- Người vá tự khai cách hỏng duy nhất: **thêm năng lực mà quên thêm tên** thì nhánh cũ
  không được cảnh báo, và hỏng **im lặng**. Có chốt cơ học nào bắt được chuyện đó không,
  hay nó vốn không bắt được? Nếu không bắt được thì cơ chế này mạnh hơn băm toàn tệp ở
  đâu, yếu hơn ở đâu?
- Tên năng lực là **chuỗi tự do**. Gõ sai một chữ (`rg-bat-buoc` → `rg-batbuoc`) thì sao?
  Đổi tên một năng lực đã có thì hai phía lệch thế nào?
- `_nang_luc_hook` nhận **nhiều dòng** khai (`finditer` + `update`). Cố ý hay sơ suất?
  Có cho phép ai đó vô hiệu hoá bằng cách thêm một dòng khai thứ hai không?
- Dòng khai nằm trong **chú thích shell**. Có kịch bản nào hook bị sửa mà dòng khai vẫn
  nguyên, khiến chốt báo xanh cho một hook đã hỏng không? (Đây chính là đánh đổi mà bản
  vá cố ý chọn — phán định xem đánh đổi đó có đúng không.)
- `t88` đọc hook THẬT của kho qua `Path(__file__).resolve().parents[2]`. Giả định đường
  dẫn ấy có bền không?

## 3. `026c4ea` — nối năm ca vào `DOT_BIEN`

Đáp lại mục bạn nêu: t84/t85/t86 chưa được cưỡng chế tự động. Nay có cả t87, t88.

Đáng chú ý, và người vá tự khai: đột biến `do_codex_tin_DONG_DAU_thay_vi_ma_thoat` bản
đầu **giết 0/1**, phải gỡ **hai** lớp mới tái hiện được bug fail-open — vì `_do_codex` có
hai lớp độc lập (mã thoát; lọc dòng `WARNING`/`NOTE`/`HINT`).

**Hỏi ngược:** gộp hai thay đổi vào một đột biến là **phòng thủ nhiều lớp** (giống tiền lệ
`bo_kiem_rong_CA_BON_LOP`), hay là **làm nhẹ** một đột biến để nó chịu chết? Phân biệt hai
thứ đó là việc của lượt này. Nếu là làm nhẹ, nói thẳng.

## 4. Chỗ người vá nói CHƯA GIẢI THÍCH ĐƯỢC — mời bạn đo

Ở lượt chạy **đầu** của cổng đột biến trên nhánh này, hai mục `so_URL_tho_khong_chuan_hoa`
và `bo_cung_hoa_dau_ra` báo `SAI`; lượt sau cả hai `OK`, nền master cũng `OK`. Người vá
kết luận là **chập chờn**, chưa tìm ra điều kiện tái lập, và ghi ra thay vì giấu.

Bạn chạy `--dot-bien` và nói bạn thấy gì. Nếu bạn tái lập được điều kiện, đó là finding
có giá trị. Nếu bạn cũng chỉ thấy chập chờn, nói vậy cũng có giá trị.

## 5. Gate — tự chạy, đừng chép

```bash
python3 .claude/dev/launcher_test.py              # ĐÒI hai số BẰNG NHAU
python3 .claude/dev/launcher_test.py --dot-bien   # cổng đột biến
python3 .githooks/eol_policy.py --all --json      # ĐÒI violations=0
python3 scripts/tl.py doc-claims-check --strict --json   # ĐÒI flags=[]
bash -n .claude/hooks/session-start.sh
```

Người vá đo trên `026c4ea`: suite **88/88** (qua 87, bỏ qua 1 fixture Windows) · đột biến
**47/47** (1 không đo được) · nền master `d5b7bcc` **42/42** ⇒ delta +5 mục đều giết ·
EOL checked=330 violations=0 · doc-claims `flags=[]`.

**Mọi lệnh trong verdict phải neo SHA BẤT BIẾN** — không `origin/master`, không `HEAD`,
không tên nhánh.

## 6. CẢNH BÁO AN NINH khi tự đo

Bản vá đụng credential thật.

- **TUYỆT ĐỐI KHÔNG in GIÁ TRỊ** biến môi trường nào, kể cả một phần, kể cả để chứng minh.
  Chỉ nêu TÊN, ĐỘ DÀI, nhãn nhóm. `CODEX_AUTH_JSON` chứa refresh token.
- Mọi phản chứng đụng credential **phải chạy trên `HOME=$(mktemp -d)`**. TUYỆT ĐỐI KHÔNG
  ghi/xoá/đổi `~/.codex/auth.json` THẬT — đó là credential đang nuôi chính phiên bạn.
  Đột biến ghi vào tệp thật rồi khôi phục trong `finally` là bom hẹn giờ.
- Phép đo nào buộc phải đụng tệp thật mới làm được thì **ĐỪNG LÀM** — ghi vào `boundaries`.

---

## Verdict và evidence

`approve` · `changes_requested` · `blocked`.

Mỗi finding: `finding_id` kebab-case ổn định, `severity`, `disposition`, **bằng chứng chạy
được neo SHA bất biến** + **lệnh/fixture nguyên văn**. Không tái lập được thì ghi rõ là
**nghi vấn**. **Nói thẳng chỗ bạn KHÔNG chạy được.**

`approve` là verdict hợp lệ nếu bạn thật sự không tìm ra gì — đừng nặn ra finding cho có.
Ngược lại, hai commit này **chưa ai soi**, nên đừng cho qua vì lượt 1 đã duyệt phần khác.

### Giao kết quả

REST tới `api.github.com` bị proxy 403, `gh` không cài ⇒ ghi verdict RA TỆP:

```
ops/reviews/moi-truong-review-2-codex-verdict.md
ops/reviews/moi-truong-review-2-codex-verdict.receipt.yaml
```

Xuất **thẳng `stdout` ra tệp**, đừng chép tay. Báo `sha256` + số byte. Phiên điều phối
`claude` đăng hộ và push.

## Stop conditions

Head đổi giữa chừng · lease hết hạn · bạn không phải `codex` · bước 0 lệch (trừ hai lệnh
đã nêu) · bị đòi sửa tệp/commit/push/merge/land · không chạy được phần thiết yếu (báo
`blocked` kèm lý do ĐO ĐƯỢC, đừng đoán rồi `approve`) · chạm quota (ghi lý do allowlist).
