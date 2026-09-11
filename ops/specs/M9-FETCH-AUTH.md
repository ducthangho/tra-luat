# ĐẶC TẢ ĐÓNG BĂNG — `M9-FETCH-AUTH` — **BẢN 1 — ĐÃ CHỐT 11-09-2026** (Q1/Q2 tại #499 comment 5629586342)

| trường | giá trị |
|---|---|
| `packet_id` | `M9-FETCH-AUTH` |
| `packet_issue` | **#503** (mission #499) |
| `nguon_cap_viec` | **Packet khắc phục** của A0 (packet #488, PR #492, merge `0721811`). Nợ **#499 C2a** (comment `5613562702`, 05:16:52Z 10-09-2026), đã được chủ kho duyệt đề xuất số 1 trong phiên 11-09-2026 (*"đồng ý các đề xuất, trừ nội dung số 3"*). Spec cha: `THU-HOI-LEASE-VA-CAP-LAI` r9 (sha256 `465538364b1a3f9477782fba79869bbd1c9351140e3fa9df50451baae22f9c79`), hợp đồng M9. |
| `review_class` | **`sensitive`** — `.github/workflows/**` (PROTOCOL §8) và `ops/lease_publish_test.py` (gate test). Vế nghiêm ADR-0044: ≤3 tệp, ≤300 dòng thêm — **trong trần** (2 tệp, ước +45). |

**GIỚI HẠN LỜI KHAI:** chứng minh BYTE tới consumer adapter. **Ba trạng thái:** có · không · **KHÔNG ĐO ĐƯỢC**.

---

## VÌ SAO — phép đo, không phải lập luận

`ops-thu-hoi-admission.yml` (M9, cài ở A0 chế độ chưa kích hoạt) chạy lần đầu trên PR #500 (run `34440291662`,
`pull_request_target`, S=`0721811`, H=`5a29d35`): mọi chốt input qua, rồi chết ở bước fetch H:

```
fatal: could not read Username for 'https://github.com': No such device or address
##[error]Process completed with exit code 128.
```

Nguyên nhân (đọc được ngay trong tệp, dòng 92–94 của `27c413c3`): checkout S dùng `persist-credentials: false`
(đúng thiết kế M9 — không để lại credential trong cây) và lệnh fetch gọi endpoint TƯỜNG MINH
`https://github.com/$TL_KHO` **không kèm xác thực**; kho không cho fetch nặc danh ⇒ Git hỏi username, không tty ⇒
128. Fail-close (không receipt, job ĐỎ) nên không mở lỗ — nhưng đây là cổng **không bao giờ xanh**, và không lượt
review nào của A0 thấy vì sandbox review không có mạng (đúng `chua_do_duoc` #4 của r9: *"actions/checkout exact S +
fetch H trong pull_request_target … nghiệm thu A1"*). Nợ #499 **C2** (canary raw API) cũng kẹt sau nó: chưa có
receipt nào để đọc.

Hệ quả lan sang: **mỗi lần sửa thân PR** (`edited` nằm trong `types` của M9) đều bắn lại một lượt ĐỎ — đo trên #500/#501.

---

## `write_set` — HAI đường

```
.github/workflows/ops-thu-hoi-admission.yml    141 dòng  (đo 03:04:52Z 11-09-2026, cây 27c413c3)
ops/lease_publish_test.py                     5394 dòng · 146 ca `@ca` · ca cao nhất t151 ⇒ ca mới là **t152**
```

**Đã đo ai giữ — 02:54:23Z 11-09-2026, bản sao sạch detach `27c413c3`, hai nguồn ref 324/324, `comm` 0/0:**

```
.github/workflows/ops-thu-hoi-admission.yml → NGƯỜI_GIỮ 0  (HẾT_HẠN: wp488-thu-hoi-lease-a0-exec-1-claude-20260909)
ops/lease_publish_test.py                   → NGƯỜI_GIỮ 0  (HẾT_HẠN: slice-b-c-exec-1-claude-20260821, plat-x5-exec-1r4-codex-20260821)
```

Giao thoa với packet **`WINDOWS-LEASE-SUITE`** (cùng `ops/lease_publish_test.py`) và **`THU-HOI-LEASE-A1`** (cả hai
đường) — ba packet này **KHÔNG được cấp chồng**; thứ tự đề nghị: `M9-FETCH-AUTH` → `WINDOWS-LEASE-SUITE` → `A1`
(Q2). Không giao với `BO-CONG-DUYET-KHAC-DANH-TINH`.

## `ngoai_pham_vi` — cố ý KHÔNG làm

- **F07 — ghim `actions/upload-artifact@v4` bằng SHA** (#499 A1): cần chủ kho readback SHA từ kho ngoài; thuộc A1.
  Packet này KHÔNG đụng dòng 136. Nếu chủ kho cấp SHA kịp trước khi cấp lease này thì mở revision 2 gộp vào
  (cùng tệp, +1 dòng) — Q1.
- **`types: [..., edited]`** — giữ nguyên theo hợp đồng M9 (r9: *"types opened/reopened/synchronize/ready_for_review/
  edited, không lọc"*). Việc `edited` bắn lại là chi phí đã chấp nhận trong spec cha, không sửa ở đây.
- **Consumer đọc receipt** (`LAND-DOC-RECEIPT-THU-HOI`, #499 C1) — packet riêng.
- **`ops/lease_publish.py`** — không đụng; canary C2 chỉ đọc artifact, không đổi mã cổng.
- **`permissions`** của job — giữ `contents: read · pull-requests: read · actions: read`; `GITHUB_TOKEN` đọc được
  `refs/pull/<n>/head` với `contents: read`. Nếu canary chứng minh ngược lại ⇒ DỪNG (S3), không tự nâng quyền
  (hợp đồng M9: *"không tự nâng quyền khi API lỗi"*).

---

## `muc_tieu`

**M1** *(`ops-thu-hoi-admission.yml`)* — bước fetch H mang xác thực bằng **header** lấy từ `TL_TOKEN`
(`secrets.GITHUB_TOKEN`, đã có trong `env` của bước), phạm vi **đúng một lời gọi `git fetch`**, KHÔNG ghi vào bất kỳ
tệp config nào, KHÔNG nhúng token vào URL. Dạng khuyến nghị (Q1 chọn giữa hai dạng tương đương):

```bash
# Dạng (a) — biến môi trường cấu hình của git, chỉ sống trong MỘT tiến trình; không xuất hiện trong argv:
GIT_CONFIG_COUNT=1 \
GIT_CONFIG_KEY_0="http.https://github.com/.extraheader" \
GIT_CONFIG_VALUE_0="AUTHORIZATION: basic $(printf 'x-access-token:%s' "$TL_TOKEN" | base64 -w0)" \
git -c protocol.allow=never -c protocol.https.allow=always \
    fetch --no-tags "https://github.com/$TL_KHO" "+refs/pull/$TL_PR/head:refs/thu-hoi/ung-vien"
# Dạng (b) — `-c http.https://github.com/.extraheader=...` (cùng ngữ nghĩa, nhưng chuỗi base64 nằm trong argv).
```

Giữ nguyên hai chốt đã có ngay sau đó: `NHAN == TL_H` (OID nhận được phải bằng `head.sha`) và `set -euo pipefail`.

**M2** *(`ops/lease_publish_test.py`)* — ca **`t152_C2a_M9_fetch_H_mang_xac_thuc_qua_header_khong_token_trong_URL`**
đọc `WORKFLOW_THU_HOI` bằng `yaml.safe_load` (cùng cách t148), tìm đúng dòng lệnh chứa `fetch --no-tags` và khoá
BỐN điều: (i) cấu hình `http.https://github.com/.extraheader` có mặt trên chính lời gọi ấy (qua `GIT_CONFIG_KEY_0`
hoặc `-c`), giá trị dẫn từ `$TL_TOKEN`; (ii) URL fetch **không** chứa `@`, không chứa `TL_TOKEN`; (iii) không có lời
gọi `git config` nào ghi `extraheader` (không để credential lại trong cây S); (iv) bước checkout vẫn
`persist-credentials: false`. Cộng chốt của t148 không đổi.

**M3** *(cả hai)* — canary C2: lượt chạy thật của workflow trên PR **đầu tiên sau khi land** phải `success`, và
executor tải `receipt.json` từ artifact `thu-hoi-receipt-<H>-<attempt>` (qua MCP `/mcp/x/actions` hoặc
`list_workflow_run_artifacts`), đọc `check_run_id`, `workflow_definition_commit`, `workflow_definition_sha256`,
`checker_rc` và ghi vào PR hồ sơ (ADR-0034) — đóng phần còn lại của #499 C2.

---

## `nghiem_thu`

**A1 (M1, M2)** — `t152` **ĐỎ trên nền** `27c413c3` (thiếu extraheader) và **XANH sau vá**. Executor chép cả hai
dòng in ra vào PR. *Đột biến làm nó ĐỎ trở lại:* (m1) xoá cấu hình extraheader ⇒ ĐỎ; (m2) đổi sang
`https://x-access-token:${TL_TOKEN}@github.com/...` ⇒ ĐỎ vì (ii); (m3) thêm `git config --local http...extraheader`
trước fetch ⇒ ĐỎ vì (iii); (m4) đổi `persist-credentials: false` → `true` ⇒ ĐỎ vì (iv). Bốn đột biến, bốn răng
riêng — cùng đỏ vì một lý do là chưa độc lập.

**A2 (M1)** — `actionlint` (`AL_VER=1.7.7`, có `shellcheck`) `rc=0` trên tệp; `AL_VER=1.7.7 bash ops/chay_lease_publish_test.sh`
⇒ `147/147` (146 nền + t152), delta so `origin/master` = 0 ở mọi ca cũ.

**A3 (M3)** — trên PR **đầu tiên sau land** (định nghĩa `pull_request_target` lấy từ `master`): run của
`ops-thu-hoi-admission.yml` `conclusion: success`; log bước fetch không in token (GitHub mask `GITHUB_TOKEN`; chuỗi
base64 của nó KHÔNG được mask — executor kiểm bằng mắt rằng log không chứa chuỗi 40+ ký tự base64 sau `AUTHORIZATION`;
nếu có ⇒ P1, DỪNG). Artifact có đúng một `receipt.json`; các trường M3 đọc được.
*Phép đo làm nó ĐỎ:* run vẫn 128 ⇒ giả thuyết "thiếu xác thực" sai — DỪNG, revision, không thử tiếp bằng cách nâng quyền.

**A4** — `git diff --numstat`: ≤ 2 tệp, dòng thêm ≤ 80.

---

## `hinh_dang_ke_thua` (L4)

Chép từ spec cha r9 §`hinh_dang_ke_thua` (biên nhận A0 `ops/reviews/pr492-*.receipt.yaml` **không mang bộ đếm này** —
đo 03:04Z 11-09: `grep hinh_dang` trên 8 tệp ⇒ 0; đó là một lỗ của quy trình biên nhận, ghi ở `chua_do_duoc`):

| hình dạng | số lần | nguồn |
|---|---|---|
| "thu hồi là dữ liệu ghi vào bản sao" | 2 | r9 §1 |
| "lời khai hội tụ rộng hơn phép đo" | 3 | r9 g2, lượt 1 |
| "hai cổng bất đồng" | 1 | #473 |
| "nguồn được tin mà chưa xác minh" | 6 | r9 lượt 1–6 |
| **"cổng có MẶT khác cổng ĐO ĐƯỢC"** — canary chưa từng chạy được | **1** (mới, #499 C2a) | run `34440291662` |

Hình dạng thứ năm là hình dạng của packet này. Lần thứ hai (nếu canary sau vá vẫn đỏ vì một lý do khác) ⇒ hỏi lại
cách làm trước khi vá tiếp.

## `chua_do_duoc`

- **`GITHUB_TOKEN` với `contents: read` fetch được `refs/pull/<n>/head` trong `pull_request_target`** — suy từ tài liệu
  và từ `actions/checkout` (dùng cùng header với cùng token); **chưa có run nào chứng minh trên kho này**. A3 là phép đo.
- **Chuỗi base64 của token có bị mask trong log không** — GitHub chỉ mask giá trị secret nguyên văn; A3 kiểm bằng mắt.
- **Biên nhận A0 không mang `hinh_dang_ke_thua`** — L4 nói bộ đếm "sống trong biên nhận packet trước"; thực tế nó sống
  trong SPEC. Không sửa ở packet này; ghi nhận để `bien_nhan_v2` cân nhắc (ngoài phạm vi).
- **Parity Windows** — workflow chạy `ubuntu-latest`; `base64 -w0` là GNU; không có vế Windows để đo.

## Điều kiện DỪNG

- **S1** cần đường dẫn thứ BA ⇒ DỪNG.
- **S2** dòng thêm > 80 ⇒ DỪNG (bản vá này là 3–6 dòng workflow + một ca test).
- **S3** canary sau vá vẫn 128 hoặc 403 ⇒ DỪNG, KHÔNG nâng `permissions`, KHÔNG nhúng token vào URL.
- **S4** `origin/master` đi tiếp mà chạm một trong hai đường ⇒ DỪNG, đo lại.
- **S5** `WINDOWS-LEASE-SUITE` hoặc `A1` được cấp trước và chưa land ⇒ DỪNG (chồng write set).
- **S6** trần HAI vòng review (ADR-0043).

## Câu hỏi biên giới — ĐÃ CHỐT (chủ kho: *"Bước 2: Trả lời luôn hộ tôi"* = lấy khuyến nghị; #499 comment 5629586342)

| câu | kết luận |
|---|---|
| Q1 | **dạng (a)** `GIT_CONFIG_COUNT/GIT_CONFIG_KEY_0/GIT_CONFIG_VALUE_0` cho đúng một lời gọi `git fetch`; t152 nhận cả (a) lẫn (b). Chưa có SHA F07 ⇒ không gộp |
| Q2 | **M9-FETCH-AUTH → WINDOWS-LEASE-SUITE → THU-HOI-LEASE-A1**, mỗi packet cấp sau khi packet trước land |

Nguyên văn hai câu hỏi giữ dưới đây làm hồ sơ:

❓ **Q1 — Dạng cấu hình header.** (a) `GIT_CONFIG_KEY_0/VALUE_0` (không lộ trong argv, không tệp) hay (b) `-c` như
comment C2a đề nghị. ➡️ **(a)** — cùng ngữ nghĩa, ít bề mặt hơn; t152 nhận cả hai dạng để không khoá vào cú pháp.
Kèm: nếu chủ kho đã có SHA cho F07 (A1) thì gộp +1 dòng vào revision 2 của packet này, tránh mở lại tệp workflow ba lần.

❓ **Q2 — Thứ tự ba packet chung write set.** ➡️ `M9-FETCH-AUTH` (nhỏ nhất, mở khoá canary C2) → `WINDOWS-LEASE-SUITE`
→ `THU-HOI-LEASE-A1`. Mỗi packet cấp SAU khi packet trước land và `ai-dang-giu` ⇒ 0 trên cả hai đường.
