verdict: changes_requested
reviewed_sha: 93abdf2aeb9c

# CROSS-REVIEW LƯỢT 3 — packet #548 — **RÚT `approve` CỦA LƯỢT 2**

| | |
|---|---|
| `reviewed_sha` | `93abdf2aeb9c` — **cùng head lượt 2 đã `approve`** |
| kết luận | **`changes_requested`** — **1 × P1** |
| thay thế | verdict lượt 2 (`sha256 5682e47107ef0a52d6f5591483ddb626b15bb0f1c75311f5dbeda0723f811587`) — **`approve` của nó BỊ RÚT** |
| assurance | **`advisory_review`** |

## TÔI RÚT `approve`, VÀ LỖI LÀ CỦA TÔI TRƯỚC HẾT

Verdict lượt 2 khai `approve` cho `93abdf2aeb9c`, và trong mục `KHÔNG ĐO ĐƯỢC` viết:

> `gate` trên head `93abdf2` — **chưa đo lúc viết verdict này**.

**Câu đó sai.** Lượt CI đã **chạy xong** lúc `2026-09-17T16:11:47Z`
([run `35245043682`](https://github.com/ducthangho/tra-luat/actions/runs/35245043682)); tôi viết verdict
lúc ~`16:2x`Z. Nó không phải *chưa đo được* — nó là **tôi không hỏi**.

Đây đúng bệnh mà `CLAUDE.md` đã đặt tên: *"HỎI CHỖ TIỆN TAY thay vì hỏi CHỖ KẾT LUẬN ĐƯỢC GHI"*. Tôi
đo bảy cổng tại chỗ trên cây rồi kết luận, mà không đi hỏi chỗ ghi kết luận thật là **check run của
PR trên đúng head ấy**.

Trớ trêu đúng chỗ đáng nhớ: chính verdict lượt 2 của tôi viết, cùng mục ấy, rằng
*"Phép đo duy nhất đóng được lớp này là chính lượt CI — nên lượt ấy phải được đọc, đừng bỏ qua."*
Tôi viết câu đó rồi bỏ qua đúng lượt đang nói tới.

**Verdict lượt 2 giữ nguyên trên đĩa** làm hồ sơ; `approve` của nó bị rút **tại đây**, không sửa đè.

---

## `P1` — JOB `chuan-bi` LÀM TOÀN BỘ CỔNG BIẾN MẤT

### Phép đo

Check run trên head `93abdf2aeb9c` (PR #550):

| check run | kết luận |
|---|---|
| **`chuan-bi`** | **FAILURE** — [job `105282976101`](https://github.com/ducthangho/tra-luat/actions/runs/35245043682/job/105282976101) |
| `gate` | **skipped** |
| `gate-registry` | **skipped** |
| `gate-packet-loop` | **skipped** |
| `thu-hoi` | success |

Log của `chuan-bi`, nguyên văn:

```
##[error]Fail to evaluate job outputs
##[error]The template is not valid. .github/workflows/ci.yml (Line: 40, Col: 11): A sequence was not expected
```

Dòng 40 đo trên cây tại `93abdf2`:

```yaml
    outputs:
      os: ${{ fromJSON(
            (github.event_name == 'workflow_dispatch'
             || contains(github.event.pull_request.labels.*.name, 'windows'))
            && '["ubuntu-latest","windows-latest"]'
            || '["ubuntu-latest"]') }}
```

### Nguyên nhân

**Giá trị `outputs` của một job phải là CHUỖI.** `fromJSON('["ubuntu-latest"]')` trả về một **mảng**
(sequence), nên GitHub từ chối: *"A sequence was not expected"*. Không phải lỗi cú pháp YAML — YAML
hợp lệ hoàn toàn; lỗi ở **hợp đồng kiểu của `outputs`**, và nó chỉ lộ ra lúc GitHub **chạy** job.

### Vì sao đây là `P1` chứ không phải một job đỏ bình thường

`chuan-bi` hỏng ⇒ ba job `needs: chuan-bi` **không chạy**, và chúng hiện ra là **`skipped`**, không
phải `failure`. Tức packet này, ở trạng thái hiện tại, **xoá sạch cổng của kho** và làm việc đó theo
cách **trông không giống hỏng**.

Đúng bài học đã trả giá của kho: *"cổng không nói dối — nó **VẮNG MẶT**, và trên giao diện 'xanh' với
'không chạy' nhìn giống hệt nhau."* Nếu merge, master sẽ ở đúng trạng thái ấy.

### Và nó chứng minh đúng giới hạn tôi đã khai ở lượt 1 và lượt 2

Cả hai lượt tôi đều ghi trong `KHÔNG ĐO ĐƯỢC`:

> `t162` đo một **evaluator viết tay** mô phỏng biểu thức Actions, không đo GitHub chạy thật. Nếu
> evaluator hiểu biểu thức khác GitHub thì cả bảng bốn ca vẫn xanh trong khi CI làm việc khác.

Đây **chính xác** là ca ấy, và nó còn hẹp hơn tôi tưởng: evaluator đọc **ngữ nghĩa điều kiện** (và đọc
đúng — bốn ca đều ra kết quả đúng), nhưng không ai đo **hợp đồng kiểu của `outputs`**. Hai thứ khác
nhau. `t161`/`t162` xanh, `A1` = 1, `actionlint` delta 0, `adr-song` rc=0 — **tất cả đều đúng**, và
workflow vẫn chết.

Cùng họ *"YAML parse được KHÁC GitHub NHẬN"*, khác ở chỗ: lần trước GitHub từ chối **cả tệp** lúc đẩy
nên lộ ngay; lần này tệp hợp lệ, job **chạy**, rồi chết ở bước *"Evaluate and set job outputs"*.

### Vá đề xuất — ĐỀ XUẤT, không chỉ định

Gỡ `fromJSON` ở **`chuan-bi`**, để nó phát ra **chuỗi JSON**; ba consumer đã `fromJson(...)` sẵn nên
không phải đổi:

```yaml
    outputs:
      os: ${{ (github.event_name == 'workflow_dispatch'
               || contains(github.event.pull_request.labels.*.name, 'windows'))
              && '["ubuntu-latest","windows-latest"]'
              || '["ubuntu-latest"]' }}
```

**Phản chứng BẮT BUỘC, và lần này không được đo bằng evaluator viết tay:** phép đo duy nhất đóng được
lớp này là **lượt CI thật trên PR**. Sau khi đẩy, phải ĐO rằng `chuan-bi` **success** và ba job
`gate` / `gate-registry` / `gate-packet-loop` **CÓ CHẠY** (không `skipped`), bằng
`pull_request_read get_check_runs` trên đúng head mới. Đừng suy từ `git push` thành công, và đừng suy
từ bảy cổng tại chỗ.

**Và thêm một chốt đo được vào `ops/lease_publish_test.py`** (đã trong write set): `outputs` của một
job **không được** là biểu thức bọc `fromJSON`/`fromJson`. Đột biến bọc lại `fromJSON` quanh giá trị
`outputs` phải làm ca ấy **ĐỎ**. Không có chốt ấy thì lớp lỗi này quay lại im lặng ở lần sửa sau.

---

## THỨ ĐÃ ĐÓNG Ở LƯỢT 2 THÌ VẪN ĐÓNG

`P1` này **không** mở lại `P2-a`, `P2-b`, `P3` — chúng đã đóng bằng phép đo và không dính tới lỗi kiểu
của `outputs`:

| | trạng thái |
|---|---|
| `P2-a` (ADR ghi trạng thái WP541 tại thời điểm land) | **ĐÓNG** |
| `P2-b` (chọn (b)+(c), đo mệnh đề `deploy-package.*`) | **ĐÓNG** |
| `P3` lượt 1 (tautology) | **ĐÓNG**, răng còn nguyên |
| `P3-MỚI` lượt 2 (`A6` phát biểu `rc=0` — không thể đạt) | **CÒN MỞ**, không chặn |

## BẢNG ĐO LƯỢT NÀY

| phép đo | kết quả |
|---|---|
| check run trên `93abdf2` | `chuan-bi` **FAILURE**; `gate` · `gate-registry` · `gate-packet-loop` **skipped**; `thu-hoi` success |
| nguyên nhân | `ci.yml:40` — `outputs.os` bọc `fromJSON` ⇒ trả mảng ⇒ *"A sequence was not expected"* |
| head có trôi từ lúc lượt 2 review không | **không** — vẫn `93abdf2aeb9c` |
| `master` | `a612c70cbc56`, không đổi |

## NỢ MỚI

**`REVIEW-KHONG-DOC-CHECK-RUN`** — không cổng nào bắt việc một verdict `approve` được phát ra trong
khi check run trên chính `reviewed_sha` đang đỏ. Lượt này là ca đo được: bảy cổng tại chỗ xanh, verdict
`approve`, CI trên đúng head **đã đỏ từ 11 phút trước**. Chốt rẻ: trước khi phát `approve`, đọc
`get_check_runs` trên `reviewed_sha` và coi **`skipped` là KHÔNG ĐO ĐƯỢC**, không phải đạt.

## NGUỒN CÓ THẨM QUYỀN

Tệp này trong kho, có băm. Bản đăng trên GitHub chỉ là **bản chiếu**.
Verdict lượt 1 (`606287b2…`) và lượt 2 (`5682e471…`) giữ nguyên; `approve` của lượt 2 bị rút tại đây.
