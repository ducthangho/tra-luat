verdict: blocked
reviewed_sha: 6d46e6fc16ca

# CROSS-REVIEW LƯỢT 4 — packet #548 `CI-MA-TRAN-WINDOWS-CHAY-MOI-LAN-LAND` r1/g1

| | |
|---|---|
| `reviewed_sha` | `6d46e6fc16ca` (PR #550) |
| `base_sha` | `a612c70cbc56` · `numstat` **4 tệp, +257 / −24** |
| lượt trước | `93abdf2aeb9c` — lượt 3, `changes_requested`, 1 × P1 |
| kết luận | **`blocked`** — **KHIẾM KHUYẾT NẰM Ở ĐẶC TẢ ĐÃ ĐÓNG BĂNG**, không ở bản vá |
| assurance | **`advisory_review`** |

**`P1` của lượt 3 đã ĐÓNG, và đóng tốt.** Verdict `blocked` này **không** phải lỗi của bản vá. Nó là
vì phép đo lượt này cho thấy **đặc tả `r1` chứa một tiêu chí không thể đạt được cùng lúc với bản vá
đúng** — và theo `docs/PROTOCOL_DA_PHIEN.md` §3.2, *"finding cho thấy chính spec thiếu thì verdict là
`blocked` và đi qua revision mới"*.

---

## `P1` (lượt 3) — ĐÓNG, có phép đo ở đúng lớp đã đòi

Bản vá, toàn bộ diễn biến:

```yaml
     outputs:
-      os: ${{ fromJSON(
-            (github.event_name == 'workflow_dispatch'
-             || contains(github.event.pull_request.labels.*.name, 'windows'))
-            && '["ubuntu-latest","windows-latest"]'
-            || '["ubuntu-latest"]') }}
+      os: ${{ (github.event_name == 'workflow_dispatch'
+               || contains(github.event.pull_request.labels.*.name, 'windows'))
+              && '["ubuntu-latest","windows-latest"]'
+              || '["ubuntu-latest"]' }}
```

Phản chứng bắt buộc của lượt 3 đòi **hai** điều, đo bằng `get_check_runs` trên head mới. Đo được
(run `35247032621`):

| check run | trước (`93abdf2`) | sau (`6d46e6f`) |
|---|---|---|
| `chuan-bi` | **FAILURE** | **success** |
| `gate` | `skipped` | **`gate (ubuntu-latest)` — CÓ CHẠY** |
| `gate-registry` | `skipped` | **`gate-registry (ubuntu-latest)` — CÓ CHẠY** |
| `gate-packet-loop` | `skipped` | **`gate-packet-loop (ubuntu-latest)` — success** |

Ba job nay mang hậu tố `(ubuntu-latest)` ⇒ ma trận **nở đúng** từ `chuan-bi.outputs.os`. Cả hai điều
kiện của phản chứng đều thoả.

### Chốt mới có răng — đo, không nhận lời khai

agy thêm `_kiem_tra_outputs_ci_khong_boc_fromjson` và nối vào `t161`. Nó quét **mọi** job (không phải
danh sách tên) và **không phân biệt hoa thường** — đúng hai điều lượt 3 dặn.

Đột biến bơm vào hàm thật (cho nó luôn trả `[]`):

| đột biến | ca | rc | câu đã giết |
|---|---|---|---|
| `_kiem_tra_outputs_ci_khong_boc_fromjson` luôn trả `[]` | `t161` **ĐỎ** | 1 | `"chốt không bắt được output bọc fromJSON: []"` |

Nền: `t161` và `t162` đều `1/1 đạt`, `rc=0`.

---

## `P2-MỚI` — ĐẶC TẢ ĐÓNG BĂNG ĐÒI GIỮ CHÍNH CON BUG

### Phép đo

Đặc tả `ops/specs/ci-ma-tran-windows-chay-moi-lan-land-r1.md`, băm đo từ blob
`56cb4bdc07052e7653aad41fb91b5c0f2291e748f553a83ce60d05f0f516e7e1` — **khớp `spec_hash` trong lease**
`ci-windows-r1-g1-antigravity`. Dòng 104, nguyên văn:

> **A1** (M1,M2) | `grep -c 'os: ${{ fromJSON'` trên `ci.yml` = **1** (chỉ `chuan-bi`), giảm từ **3**
> (Đ1) | **số khác 1 ⇒ ĐỎ**

Đo tại `6d46e6fc16ca`:

```
$ grep -c 'os: ${{ fromJSON' .github/workflows/ci.yml
0
```

⇒ theo đúng chữ của đặc tả, **`A1` ĐỎ**.

### Và không vá được, vì hai thứ LOẠI TRỪ NHAU

`A1` chỉ đạt khi `ci.yml` chứa nguyên văn chuỗi `os: ${{ fromJSON` tại `chuan-bi.outputs`. Nhưng đó
**chính là** con bug `P1`: bọc `fromJSON` vào `outputs` làm giá trị thành **mảng**, và GitHub từ chối
cả template (*"A sequence was not expected"*), kéo ba job gate thành `skipped`.

**Nên đặc tả đang đòi giữ lỗi.** Không bản vá đúng nào thoả được `A1` như nó đang viết.

### Đây là khiếm khuyết ĐẶC TẢ, không phải khiếm khuyết MÃ

Bất biến mà `A1` sinh ra để canh — *"chỉ một nguồn cho ma trận `os`, giảm từ 3 xuống 1"* — **vẫn được
giữ**, và được đo tử tế bởi `t161` (`_kiem_tra_nguon_duy_nhat_os_ci` tìm chuỗi
`needs.chuan-bi.outputs.os`, tức đo **THẨM QUYỀN**). Thứ hỏng là **cách phát biểu** của `A1`: nó đo
**CHÍNH TẢ** của một tên hàm.

Đúng lớp lỗi kho đã đặt tên: *"phân biệt CÁCH VIẾT, không phân biệt THẨM QUYỀN"*.

### TÔI ĐÃ THẤY ĐIỀU NÀY Ở LƯỢT 1 VÀ CỐ Ý KHÔNG NÂNG THÀNH FINDING

Verdict lượt 1 (`606287b2…`) viết, nguyên văn:

> Còn lại một điểm nhỏ **không** nâng thành finding: `A1` là `grep` theo chữ `fromJSON`, nó ra **1**
> chỉ vì ba consumer viết `fromJson` chữ thường; ai chuẩn hoá cách viết sẽ làm `A1` **đỏ giả**.

Tôi mô tả đúng cơ chế, rồi tự hạ nó xuống *"điểm nhỏ"*. Nay nó thành hiện thực qua một đường khác —
bản vá **xoá hẳn** chuỗi ấy thay vì đổi cách viết. Nếu tôi nâng nó thành finding ở lượt 1, đặc tả đã
được sửa **trước** ba lượt vá. Chi phí của việc tôi làm tròn xuống: ba lượt.

### Đường ra — theo §3.2, và chủ kho quyết

`A1` nằm trong đặc tả **đã đóng băng và được lease neo băm**, nên **không sửa đè được**. §3.2:
*"Đổi objective, **acceptance**, write set, dependency, executor hoặc environment tạo revision mới và
làm lease cũ mất hiệu lực"*.

Việc cần làm, và **tôi không tự làm bất kỳ phần nào**:

1. Đóng băng **revision 2** của đặc tả, phát biểu lại `A1` theo **THẨM QUYỀN**, không theo chính tả —
   ví dụ *"`t161` xanh: đúng một nguồn `needs.chuan-bi.outputs.os`, không job nào khai `os:` riêng"*;
2. Cấp lại lease gen 2 neo `spec_hash` mới (lease hiện tại mất hiệu lực theo §3.2);
3. Nhân thể xem lại `A4`: đặc tả đòi *"đột biến: đổi nhánh fail-close thành `return ["ubuntu-latest"]`
   ⇒ ca ấy phải ĐỎ"*. Ở lượt 2 tôi yêu cầu gỡ dòng đột biến giả, agy gỡ — nên **đột biến ấy nay do
   REVIEWER thực hiện** (tôi đã chạy, và nó ĐỎ đúng), **không** còn nằm trong tệp test. Đó là một
   thay đổi **cách** thoả `A4`, nên r2 nên nói rõ đột biến do ai chạy và ghi ở đâu.

---

## `P3-MỚI` — CHỐT MỚI ĐO MỘT TÊN HÀM, KHÔNG ĐO BẤT BIẾN NÓ TỰ KHAI

Docstring của chốt viết: *"Outputs của job **bắt buộc phải là chuỗi**"*. Nhưng thân hàm chỉ kiểm
`"fromjson(" in str(v).lower()`.

Đo bằng các biểu thức **thật sự sinh sequence/object** mà không dùng `fromJson`:

| biểu thức đặt vào `outputs` | chốt |
|---|---|
| `${{ fromJSON('["ubuntu-latest"]') }}` — ca đã xảy ra | **BẮT ĐƯỢC** |
| `${{ github.event.pull_request.labels.*.name }}` — bộ lọc `.*.` trả **MẢNG** | **LỌT** |
| `${{ needs.chuan-bi.outputs }}` — **đối tượng** | **LỌT** |

Hai ca lọt làm GitHub chết **y hệt** `P1`, với cùng thông điệp *"A sequence was not expected"*.

Đúng bài học *"danh sách CẤM không bao giờ đủ — phải đảo thành danh sách CHO PHÉP"*: chốt phải đoán
trước mọi cách sinh ra một mảng, nên **thua từ trong thiết kế**.

**Không chặn**, vì xác suất ai đó viết `labels.*.name` vào `outputs` là thấp, và chốt hiện tại vẫn bắt
đúng ca đã xảy ra cùng cách tái phát nhiều khả năng nhất. Nhưng hậu quả của một ca lọt thì **bằng
đúng `P1`**, nên phải ghi.

**Hướng — đề xuất, không chỉ định:** đảo thành **danh sách CHO PHÉP** cho riêng `chuan-bi.outputs.os`
(giá trị phải khớp hình *"bộ ba điều kiện của các literal có nháy"*), **giữ** phép cấm `fromjson` rộng
cho các job khác, và **khai thẳng phần còn mù**.

---

## BẢNG ĐO ĐẦY ĐỦ — KỂ CẢ CÁI KHỚP

| phép đo | kết quả |
|---|---|
| `write_set` · tệp trong `khong_duoc_cham` bị chạm | **đúng 4 đường** · **0** |
| `ops/lease_publish.py` | **không chạm** — đúng, ngoài write set |
| `docs/PROTOCOL_DA_PHIEN.md` | **+1 / −0**, vẫn đúng một hàng §20.A |
| `numstat` so `a612c70` | **4 tệp, +257 / −24** ⇒ trần ngoại lệ 4 tệp / ≤300 → **đạt, dư 43 dòng** |
| **`A1`** `grep -c 'os: ${{ fromJSON'` | **0** — đặc tả đòi **1** ⇒ **ĐỎ theo chữ**, xem `P2-MỚI` |
| `adr-song` | **rc=0** |
| `doctrine-scan` | **rc=0** |
| `doc-claims-check --strict` | **rc=0** |
| `git diff --check` | **rc=0** |
| `actionlint` (có `shellcheck 0.9.0`) | **rc=1, 1 finding** — bằng nền và bằng master ⇒ **delta = 0** |
| `t161` · `t162` | `1/1 đạt`, `rc=0` mỗi ca |
| đột biến vào chốt mới | **bị giết** |
| `chuan-bi` trên CI | **success** |
| `gate-packet-loop (ubuntu-latest)` | **success** |
| `gate (ubuntu-latest)` · `gate-registry (ubuntu-latest)` | **`in_progress` lúc viết ⇒ `KHÔNG ĐO ĐƯỢC`** |

**Hai job `in_progress` là `KHÔNG ĐO ĐƯỢC`, không phải đạt.** Verdict `blocked` lượt này **không** phụ
thuộc chúng — khiếm khuyết nằm ở đặc tả — nhưng bất kỳ `approve` nào về sau **phải** đợi chúng
`completed`, đúng nợ `REVIEW-KHONG-DOC-CHECK-RUN` mà tôi đặt ở lượt 3 sau khi tự mắc.

## THỨ ĐÃ ĐÓNG THÌ VẪN ĐÓNG

| | trạng thái |
|---|---|
| `P2-a` lượt 1 (ADR ghi trạng thái WP541 tại thời điểm land) | **ĐÓNG** |
| `P2-b` lượt 1 (chọn (b)+(c), đo mệnh đề `deploy-package.*`) | **ĐÓNG** |
| `P3` lượt 1 (tautology) | **ĐÓNG** |
| `P1` lượt 3 (`outputs` bọc `fromJSON`) | **ĐÓNG** |
| `P3-MỚI` lượt 2 (`A6` phát biểu `rc=0` — không thể đạt) | **CÒN MỞ**, không chặn |

**`A6` và `A1` cùng một bệnh.** `A6` đòi `rc=0` trong khi nền đỏ sẵn `rc=1`; `A1` đòi một chuỗi mà bản
vá đúng phải xoá. Hai tiêu chí, cùng một lỗi thiết kế: **phát biểu theo giá trị TUYỆT ĐỐI của một phép
đo bề mặt thay vì theo DELTA hoặc theo BẤT BIẾN**. Revision 2 nên sửa **cả hai** trong một lượt.

## NGUỒN CÓ THẨM QUYỀN

Tệp này trong kho, có băm. Bản đăng trên GitHub chỉ là **bản chiếu**.
Verdict lượt 1 (`606287b2…`), lượt 2 (`5682e471…`), lượt 3 (`113b5115…`) giữ nguyên trên đĩa.
