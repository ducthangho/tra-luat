# CROSS-REVIEW — nhánh `ops/moi-truong-env-first` `0194ea0` — reviewer `codex`

Bạn là **reviewer độc lập**. Vai này **CHỈ ĐỌC**: không sửa tệp, không commit, không push,
không merge, không land, không deploy. Đầu ra là **verdict** + **evidence §7**.

Người viết bản vá là `claude` ⇒ reviewer phải là `codex` (§8). Không phải `codex` thì
**DỪNG** và báo lại.

**ĐÂY KHÔNG PHẢI wp55.** Nhánh này rẽ từ `master` và sửa hạ tầng môi trường của kho, không
đụng `packet_loop*`. Nó dùng issue #55 làm luồng điều phối vì sự cố sinh ra nó xảy ra trong
lúc chạy wp55 — nhưng nó **không** tiêu attempt của packet và **không** thuộc write_set
của packet.

---

## Bước 0 — xác minh. Lệch bất kỳ mục nào ⇒ DỪNG, báo lại.

```bash
git rev-parse --is-shallow-repository       # ĐÒI false
git config core.abbrev 7
git fetch origin ops/moi-truong-env-first
git rev-parse origin/ops/moi-truong-env-first
#   ĐÒI 0194ea0eea9d4b9eed569059f1bda9775ad92971
git diff --name-status d5b7bccd679480f2eb9e7f7d84c518bade7f7df1 0194ea0eea9d4b9eed569059f1bda9775ad92971
#   ĐÒI ĐÚNG 5 tệp:
#     .claude/dev/launcher.py · .claude/dev/launcher_test.py
#     .claude/hooks/session-start.sh · CLAUDE.md · docs/GOI_AGENT_DA_NEN.md
sha256sum ops/prompts/moi-truong-review-1-codex-20260815.md   # ĐÒI khớp prompt_sha256_required
```

**KIỂM ĐƯỜNG GIAO VERDICT TRƯỚC KHI LÀM VIỆC.** REST thẳng tới `api.github.com` bị proxy
trả 403 bất kể token; `gh` không cài; `git push` chạy. Không ghi được lên GitHub thì **vẫn
review** và ghi verdict ra tệp.

---

## Bối cảnh — sự cố mà bản vá này chốt lại

15-08-2026 phiên điều phối chạy `codex login status`, nhận `Not logged in`, rồi **kết luận**
"container không gọi được codex" và bắt chủ kho chờ máy khác gần trọn ngày. Sai.

Nguyên nhân gốc **không phải xác thực**: hook `.claude/hooks/session-start.sh` trên `master`
ĐÃ khôi phục `CODEX_AUTH_JSON` từ 14-08 với bốn chốt viết kỹ, và `docs/GOI_AGENT_DA_NEN.md`
mô tả đúng như thế. Nhưng phiên đứng trên **nhánh packet** rẽ từ `base_sha` CŨ HƠN commit
ấy, nên hook chạy thật là bản cũ. Đo được: hook cây phiên `298d96fe51f70e4e` nhắc
`CODEX_AUTH_JSON` **0 lần**; hook master `3c3dd49a8a163479` nhắc **5 lần**. Nên `codex` nói
"chưa đăng nhập" còn tài liệu nói "hook lo rồi" — **hai câu cùng đúng**.

---

## Việc cần làm

### 1. Mục `hook-phien` — chốt nguyên nhân gốc

`_do_hook_cu()` so `sha256` hook đang checkout với `origin/master`. Hỏi ngược:

- Chốt này **đỏ trên gần như MỌI nhánh packet** (nhánh nào cũng rẽ từ base cũ). Người vá
  vì thế để nó KHÔNG vào mã thoát mặc định, chỉ vào `--doi-kha-dung`, với lý do "chốt đỏ
  thường trực là chốt bị bỏ qua". **Đó là lý do đúng hay là hạ chuẩn?**
- So băm TOÀN TỆP báo lệch cả khi khác biệt vô hại (sửa chú thích). Có tiêu chí nào chặt
  hơn mà vẫn cơ học không — ví dụ chỉ đòi hook đang có là TỔ TIÊN hay HẬU DUỆ của bản master?
- Chưa fetch `origin/master` thì trả `KHONG_DO_DUOC`. Có im lặng thành "coi như đạt" ở
  đường nào không?

### 2. Quét biến môi trường — có rò giá trị ở đâu không

Đây là phần **an ninh** của bản vá. Soi kỹ nhất chỗ này.

- `quet_bien_moi_truong` · `lenh_moi_truong` · `_van_tay` · `_nhom_van_tay` · `lenh_doctor`
  — có **đường nào** in ra GIÁ TRỊ biến không? Kể cả gián tiếp: thông điệp lỗi, traceback,
  `--json`, `repr()`, độ dài + vân tay có đủ để suy ngược không?
- `_van_tay` cắt sha256 còn 8 ký tự. Với biến giá trị NGẮN và không gian nhỏ (`"1"`,
  `"true"`, `"0"`), 8 ký tự ấy có thành **oracle** để dò giá trị không? Đáng lo tới mức nào?
- `chuan_bi_xac_thuc` ghi credential ra đĩa. Kiểm bốn chốt nó khai có thật không:
  không đè khi đã đăng nhập · đòi khoá `tokens` · tệp tạm + `chmod 600` + `os.replace` ·
  không in giá trị kể cả khi hỏng. Có cửa sổ nào tệp mang quyền rộng không? Tệp tạm còn
  sót khi chết giữa chừng không?
- Hàm này **trùng việc** với khối trong hook. Hai bản có trôi lệch được không? Bên nào
  quên cập nhật thì bên đó đẩy lọt cái gì?

### 3. Mở rộng hợp đồng — có nới ngầm chỗ nào không

`doctor` thêm mã thoát 13 và trường JSON `ok_kha_dung`. Người vá khai đã GIỮ nguyên nghĩa
cũ của `ok` và của mã 12, và chỉ nới bằng CỜ `--doi-kha-dung`.

**Kiểm bằng chạy, đừng đọc.** Có phía gọi nào trong kho đọc `doctor` mà bản vá làm đổi hành
vi không? (`git grep -n 'launcher.py doctor'`)

### 4. Hook — `set -e` và các nhánh mã thoát

Người vá tự khai đã suýt để lại code chết: `"$PY" … doctor; MA=$?` với `set -e` giết script
ngay tại `doctor`, nên toàn bộ xử lý 12/13 không bao giờ chạy. Nay dùng `MA=0` rồi `|| MA=$?`.

- Còn chỗ nào trong hook có cùng bệnh không? (`set -euo pipefail` + lệnh có thể trả != 0)
- Đường cài `rg` mới có ba nhánh nối bằng `||` và kết bằng `|| true`. `|| true` ấy có nuốt
  lỗi cần thấy không?
- `rg` nay là **BẮT BUỘC**. Lý do người vá đưa: thiếu `rg` thì lệnh tìm của agent gãy giữa
  chừng chứ không tự lùi về `grep`. Có nền nào (Windows) mà đòi `rg` bắt buộc là chặn oan không?

### 5. Chạy bộ test và phản chứng

```bash
python3 .claude/dev/launcher_test.py          # ĐÒI hai số BẰNG NHAU, người vá đo 86/86
python3 .githooks/eol_policy.py --all --json  # ĐÒI violations=0
python3 scripts/tl.py doc-claims-check --strict --json   # ĐÒI flags=[]
```

Ba ca mới: `t84` (nhóm vân tay không bắt oan cờ bật/tắt) · `t85` (`_do_codex` không
fail-open khi dòng đầu là cảnh báo) · `t86` (`chuan-bi` nhận cả hai định dạng, từ chối rác).

**Đột biến từng ca mới và xem nó có RĂNG không.** Một ca xanh không chứng minh gì nếu bỏ
chốt đi nó vẫn xanh.

**Phản chứng phải chạy trên `HOME` TẠM.** Đột biến ghi vào `~` thật rồi khôi phục trong
`finally` là bom hẹn giờ (`CLAUDE.md`). Đừng đụng `~/.codex/auth.json` thật.

### 6. Tài liệu có khai đúng HÀNH VI không

`CLAUDE.md` và `docs/GOI_AGENT_DA_NEN.md` được sửa. Kiểm từng con số/khẳng định:

- "hook cây phiên 0 lần, hook master 5 lần" — đo lại.
- "năm biến cùng vân tay `f07d7417`" — đo lại trong môi trường của bạn (có thể khác!).
  Nếu môi trường bạn khác thì **nói rõ**, đừng chép số của người vá.
- "REST 403 bất kể token, `/user` lại 200" — đo lại.
- Tài liệu khai HÀNH VI hay chỉ khai Ý ĐỊNH? Bài học của kho: bản cũ chỉ khai ý định và
  lỗi sống sót qua nhiều lượt vì thế.

---

## Verdict và evidence

`approve` · `changes_requested` · `blocked`.

Mỗi finding: `finding_id` (slug kebab-case ổn định), `severity`, `disposition`, **bằng
chứng chạy được neo SHA bất biến** + **fixture/lệnh nguyên văn**. Không tái lập được thì
ghi rõ là **nghi vấn**. **Nói thẳng chỗ bạn KHÔNG chạy được.**

Mọi lệnh trong verdict phải neo **SHA bất biến** — không `origin/master`, không `HEAD`,
không tên nhánh.

### Giao kết quả

```
ops/reviews/moi-truong-review-1-codex-verdict.md
ops/reviews/moi-truong-review-1-codex-verdict.receipt.yaml
```

Xuất **thẳng `stdout` ra tệp**, đừng chép tay. Báo `sha256` + số byte. Phiên điều phối
`claude` sẽ đăng hộ lên #55.

## Stop conditions

Head đổi giữa chừng · lease hết hạn · bạn không phải `codex` · bước 0 lệch · bị đòi sửa
tệp/commit/push/merge/land · không chạy được phần thiết yếu (báo `blocked` kèm lý do ĐO
ĐƯỢC, đừng đoán rồi `approve`) · chạm quota (ghi lý do allowlist).
