verdict: approve
reviewed_sha: dff2ec14ed5b

# CROSS-REVIEW LƯỢT 5 — packet #548 `CI-MA-TRAN-WINDOWS-CHAY-MOI-LAN-LAND` **r2 / gen 2**

| | |
|---|---|
| `reviewed_sha` | `dff2ec14ed5b` — **đo lại `17:46Z 17-09-2026`: head KHÔNG trôi** |
| `base_sha` | `a612c70cbc56` · `numstat` **6 tệp, +286 / −31** |
| lease | `ci-windows-r2-g2-antigravity`, `spec_hash f825cf30f11f9f84440d8c2cad795f32931997335cff1fe9d5ac1dd04017c06f` |
| lượt trước | `93abdf2aeb9c` lượt 4 → `blocked` (khiếm khuyết đặc tả, đã chữa bằng r2) |
| kết luận | **`approve`** |
| assurance | **`advisory_review`** — trần cứng, xem cuối tệp |

## TÔI ĐỢI CỔNG XONG MỚI PHÁT `approve`

Nợ `REVIEW-KHONG-DOC-CHECK-RUN` do chính tôi đặt ở lượt 3 sau khi tự mắc: lượt 2 tôi phát `approve`
trong khi CI trên đúng `reviewed_sha` **đã đỏ từ 11 phút trước**, và phải rút.

Lượt này làm ngược lại: đọc `get_check_runs` **trước** mọi việc khác, rồi **đợi cả năm job
`completed`** mới viết dòng verdict. `gate-registry (ubuntu-latest)` chạy **22 phút 27 giây**
(`17:19:26Z` → `17:41:53Z`); trong lúc ấy tôi ghi nó là `KHÔNG ĐO ĐƯỢC`, **không** đoán hộ.

## `A10` — tiêu chí MỚI của r2, và nó là thứ duy nhất có răng với lớp lỗi `P1`

Đo trên run `35252006006`, head `dff2ec14ed5b`:

| check run | kết luận |
|---|---|
| **`chuan-bi`** | **success** (`17:19:21Z` → `17:19:24Z`) |
| **`gate (ubuntu-latest)`** | **success** (→ `17:28:21Z`) |
| **`gate-registry (ubuntu-latest)`** | **success** (→ `17:41:53Z`) |
| **`gate-packet-loop (ubuntu-latest)`** | **success** (→ `17:23:44Z`) |
| `thu-hoi` | **success** |

Cả hai vế của `A10` đạt: `chuan-bi` `success`, **và** ba job gate **CÓ CHẠY** — không job nào
`skipped`. Đối chiếu để thấy `A10` đo đúng thứ nó sinh ra để đo:

| head | `chuan-bi` | ba job gate |
|---|---|---|
| `93abdf2aeb9c` (lượt 3) | **FAILURE** | **`skipped` cả ba** — cổng VẮNG MẶT |
| `6d46e6fc16ca` (lượt 4) | success | CÓ CHẠY, `gate` **FAILURE** ở bước 26 |
| **`dff2ec14ed5b`** | **success** | **CÓ CHẠY, success cả ba** |

## `M8` — kê khai slot, ĐẠT, và viết tốt hơn mức tôi yêu cầu

```python
-        ok3 = int(j.get("file_count") or 0) == len(paths) and len(paths) + 73 == 253
+        ok3 = int(j.get("file_count") or 0) == len(paths) and len(paths) + 74 == 254
-        ok4 = (len(tren_dia) == 73
+        ok4 = (len(tren_dia) == 74
```

Kèm khối `KÊ KHAI SLOT` nêu **đích danh** tệp được thêm (`docs/adr/0049-…md`), và phân biệt hai thứ
mà bản kê khai cẩu thả hay gộp: `docs/PROTOCOL_DA_PHIEN.md` là **sửa**, không phải **thêm**; còn
`RELEASE_MANIFEST.json` đổi **chỉ vì băm của chính `tl_selftest.py`** đổi — không tệp runtime nào
được thêm, nên `file_count` giữ **180** và trần Package 200 không nhúc nhích.

Phạm vi: **chỉ** ca `r291_docs_ngoai_goi`, đúng `PHAM_VI_TREN_TL_SELFTEST` của lease.

## `M9` — tái sinh manifest, ĐẠT, đo theo CẤU TRÚC chứ không đếm dòng

Không đọc `git diff` bằng mắt mà so hai bản manifest theo chỉ mục đường dẫn:

```
file_count : 180 -> 180
mục ĐỔI    : ['scripts/tl_selftest.py']
mục THÊM   : []      mục BỚT : []
```

Đúng **một** mục đổi, đúng tệp phải đổi, không thêm không bớt. Thoả `PHAM_VI_TREN_MANIFEST`
(*"diff phải CHỈ chứa `scripts/tl_selftest.py`; `file_count` phải GIỮ 180"*).

## `A11` — ĐẠT

| | |
|---|---|
| `docs/**/*.md` | **74** |
| `r291_docs_ngoai_goi` | **ĐẠT** |
| `tl.py --selftest` | **`1710/1710`**, `rc=0`, **0 `[FAIL]`** — hai số BẰNG NHAU |
| `release-verify --strict` | `ok=true` · `expected_file_count` **180** == `checked_file_count` **180** · `package_hash_match=true` · `package_hash_self_match=true` · `errors=0` |

## BẢNG ĐO ĐẦY ĐỦ — KỂ CẢ CÁI KHỚP

| phép đo | kết quả |
|---|---|
| head trôi từ lúc bắt đầu review? | **không** — `dff2ec14ed5b` ở cả hai lần đo (`17:20Z`, `17:46Z`) |
| `write_set` | **đúng 6 đường**; `git diff --name-only` lọc ngược ⇒ **0** đường lạ |
| `numstat` so `a612c70cbc56` | **6 tệp, +286 / −31** ⇒ trần `6 tệp / 300` → **ĐẠT, dư 14 dòng** |
| người giữ write set | **`NGƯỜI_GIỮ 1: ci-windows-r2-g2-antigravity`** — gen 1 đã khai tử hai chiều, không còn cửa sổ hai writer |
| `docs/PROTOCOL_DA_PHIEN.md` | **+1 / −0**, vẫn đúng một hàng §20.A |
| `A7` — `ops/lease_publish_test.py` đầy đủ | **`157/157 đạt`**, đã chạy 157, bỏ qua **0**, **0 ĐỎ** |
| `adr-song` | **rc=0** |
| `doctrine-scan` | **rc=0** |
| `doc-claims-check --strict` | **rc=0** |
| `git diff --check` | **rc=0** |
| `actionlint` (có `shellcheck`) | head `rc=1` / **1** finding · nền `a612c70` `rc=1` / **1** finding ⇒ **delta = 0** |
| lease gen 2 còn hạn | **~23h13m** lúc viết (hết `2026-09-18T17:00:00Z`) |

## KHAI VÒNG TRÒN

`M8` và `M9` đi từ `Đ2` — **phát hiện của tôi ở lượt 4** — và spec r2 do tôi soạn nêu sẵn con số
`73 → 74`, `253 → 254`. Nên phán quyết về **hình dạng** hai mục ấy **không có giá trị độc lập**.

Thứ **có**: (a) phép đo `M9` theo **cấu trúc** (so chỉ mục hai manifest) chứ không đọc diff — nó có
thể bác lời khai, và không bác; (b) `A10`/`A11` chạy trên CI và trên cây, không đọc mã; (c) phát hiện
`P3` dưới đây, không ai chỉ.

## `P3` — LỖI CHỮ NGHĨA TRONG CHÍNH SPEC r2 CỦA TÔI (không chặn)

`A7` của r2 viết *"`release-verify --strict` … `ok=true`, `expected == checked`"*. Khoá **thật** trong
`release-verify --json` là **`expected_file_count`** và **`checked_file_count`** — đo được, 23 khoá,
không có khoá nào tên `expected` hay `checked`.

Tôi chép cách gọi ấy từ r1 và từ `CLAUDE.md` mà **không đo khoá**. Không sai về bản chất (cả hai đều
**180** và tôi đã kiểm đúng trường), nhưng ai đọc `A7` rồi `grep` đúng chữ sẽ **không thấy gì** và có
thể kết luận nhầm là `KHÔNG ĐO ĐƯỢC`.

**Không chặn**: tiêu chí vẫn đạt, chỉ tên trường viết thiếu hậu tố. Sửa ở revision sau, hoặc để nguyên
kèm ghi chú. Nhưng nó **cùng họ** với hai hình dạng đã đếm — một tiêu chí nêu một phép đo mà không ai
chạy thử phép đo ấy trước khi đóng băng.

## `hinh_dang_ke_thua` — CẬP NHẬT BỘ ĐẾM

| hình dạng | trước lượt này | sau lượt này |
|---|---|---|
| `TIEU-CHI-THEO-GIA-TRI-TUYET-DOI` | 2 | **2** (không tăng) |
| `DOT-BIEN-TAUTOLOGY` | 2 | **2** (không tăng) |
| **`TIEU-CHI-NEU-TRUONG-CHUA-AI-DO`** *(mới)* | — | **1** (`A7` của r2, xem `P3`) |

Hai hình dạng cũ **không tăng** ở lượt này — đó là tin đáng ghi, vì chốt *"lần thứ BA"* đang ở mức 2
cho cả hai và một lần tăng nữa là chạm trần.

## `KHÔNG ĐO ĐƯỢC` — khai, không lấp

1. **`A9` chỉ đo được SAU merge** — đếm job Windows sinh bởi push `master` đầu tiên phải là **0** từ
   `ci.yml`. Không có đường đo nào khác dưới `manual_ci_budget: 0`.
2. **`gate (windows-latest)` chưa từng xanh và sẽ KHÔNG xanh sau packet này** — và đó **không phải**
   việc của #548. Phiên WP541 đo riêng từng ca trong 15 ca đỏ: **14 ca là lỗi PATH**
   (`ops/lease_publish.py:1106`), còn **`t150` hỏng vì lý do ĐỘC LẬP** (nó đợi nhánh *"policy không
   phải UTF-8"* nhưng nhận nhánh *"policy vắng hoặc không phải JSON object (Q13)"*; hai dòng chẩn đoán
   của nó không chứa `PATH tối thiểu` và không chứa `/usr/bin`).
   **Đây là một đính chính cho verdict lượt 4 của tôi**, nơi tôi mô tả 15 ca như thể cùng một nguyên
   nhân. Con số đúng là **14 + 1**, không phải 15. Lời khai của tôi khi ấy **rộng hơn phép đo**.
3. **Evaluator viết tay vẫn không đo được GitHub** — `t162` đọc ngữ nghĩa điều kiện, không đọc hợp
   đồng kiểu. `A10` thu hẹp lớp này, **không đóng** nó.

## ASSURANCE — trần cứng, không phải nhận xét về bản vá

**`advisory_review`**, và lease khai `assurance_target: human_audited`. `antigravity` xuất hiện **0
lần** trong `docs/PROTOCOL_DA_PHIEN.md`, §8 nêu **đích danh** `Codex` cho class `sensitive`. Không bản
vá nào của packet này mua được `cross_approved`; việc ấy thuộc packet riêng **#551**.

## NGUỒN CÓ THẨM QUYỀN

Tệp này trong kho, có băm. Bản đăng trên GitHub chỉ là **bản chiếu**.
Verdict lượt 1 (`606287b2…`), 2 (`5682e471…`), 3 (`113b5115…`), 4 (`e112e404…`) giữ nguyên trên đĩa.
`approve` của lượt 2 **đã bị rút** ở lượt 3 và **không** sống lại; `approve` có hiệu lực là của lượt
này, neo `dff2ec14ed5b`.
