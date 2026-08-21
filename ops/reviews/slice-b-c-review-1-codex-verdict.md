# VERDICT cross-review — `SLICE-B-C` (#215 / PR "#216"), lượt 1

**Chép nguyên văn** kết luận của lượt cross-review. Lease `slice-b-c-review-1-codex-20260821`, reviewer **codex**
(khác nhà cung cấp), neo exact head `181bd7f822f84a528da4cfde810d240bcc726dbf`.

- Nguồn: stdout/stderr của `codex exec` do `launcher.py` giữ, run `9756518c`, `ma_thoat=0`.
- Chốt read-only sau lượt: `worktree_sach=True`, `so_muc_ban=0`, HEAD không đổi.
- Đường dẫn tuyệt đối của thư mục phiên đã rút gọn về `kho/…`; **không sửa gì khác**.
- **Kết luận: `changes_requested`.**

---

codex
## Báo cáo review

Reviewer: `openai_codex`, phiên độc lập, kho được giữ chỉ đọc; mọi đột biến chạy trên bản sao toàn cây tại `/tmp`.

SHA/tree được duyệt:

- HEAD: `181bd7f822f84a528da4cfde810d240bcc726dbf`
- Tree: `e2dde0babddd0ffc212722789cb76d0b69c4ee80`
- Diff: đúng 2 tệp, `+100/−0`
- `git status --short`: rỗng ở cuối lượt

### Finding 1 — P2: `t42` chưa neo lời khai vào hành vi

Vị trí: [ops/lease_publish_test.py:2006](kho/ops/lease_publish_test.py:2006).

Ba đột biến đã khai có răng thật:

- Bỏ một dạng khỏi docstring → `41/42`, chỉ `t42` đỏ.
- Bỏ `3/8` → `41/42`, chỉ `t42` đỏ.
- Đổi bảng mà không đổi docstring → `41/42`, chỉ `t42` đỏ.

Nhưng đột biến thứ tư sống sót: nới `_CHAY_BO_TEST` để nhận thêm cờ đơn trước đường dẫn:

```diff
-\s+["']?\S*lease_publish_test
+\s+(?:-\S+\s+)*["']?\S*lease_publish_test
```

Phép đo hành vi đổi từ:

```text
HEAD: bat=3/8 lot=5/8
M4:   bat=4/8 lot=4/8
```

`python3 -u ops/lease_publish_test.py` chuyển từ lọt sang bị bắt, trong khi suite M4 vẫn:

```text
lease_publish: 42/42 đạt
```

`t42` đúng khi tự khai nó đo lời khai, không đo hành vi. Nhưng câu “phép đo ấy nằm ở `_CHAY_BO_TEST` và bảng trên” cùng chú thích “phạm vi thật phải chết cùng lúc” là sai chiều ngược: bảng chỉ là dữ liệu tĩnh, không ca nào thực thi bảng qua regex.

Bất biến bị cắt: phạm vi tuyên bố phải bằng phạm vi hành vi đã đo; thay đổi hành vi phải làm lời khai cũ đỏ.

Gợi ý vá:

- Vá tại `_DANG_DA_DO_LA_LOT`/`t42`, vì đây là nơi sở hữu quan hệ regex–bảng–docstring.
- Cho ca máy khẳng định mọi dạng trong bảng lọt đều không khớp regex; thêm ba dạng canonical bị bắt và khẳng định chúng đều khớp. Sinh tỷ lệ từ hai tập thay vì chỉ tìm chuỗi `3/8`.
- Đột biến M4 trên phải làm đúng ca mới đỏ; ba đột biến hiện có vẫn phải chết.
- Rủi ro: đừng biến tám ví dụ thành tuyên bố phân tích mọi cú pháp shell; tiếp tục khai đây chỉ là tập dạng gọi đã biết.

### Finding 2 — P2: con số “8 ca đỏ” không đo được từ cây và trái kết quả chạy trực tiếp

Vị trí: [ops/NO_KY_THUAT.md:499](kho/ops/NO_KY_THUAT.md:499).

Chạy trên bản sao toàn cây với `PATH` không có `actionlint`:

```text
PATH=/usr/bin:/bin /usr/local/bin/python3 ops/lease_publish_test.py

ĐỎ t33_workflow_dang_lease_phai_qua_actionlint: KHÔNG ĐO ĐƯỢC: thiếu actionlint
lease_publish: 41/42 đạt
rc=1
```

Kết quả có đúng một ca đỏ, không phải tám. Nếu “8” chỉ tám phản chứng/đột biến ngoài suite, cây không liệt kê tám ca, lệnh chạy hay kết quả tương ứng, nên số ấy là **KHÔNG ĐO ĐƯỢC**. Chính [THAM_DINH_KE_HOACH_20260821.md:242](kho/ops/THAM_DINH_KE_HOACH_20260821.md:242) cũng khai kết luận “8 ca đỏ trên runner thật” chỉ là suy từ PATH sạch và đọc mã.

Bất biến bị cắt: tài liệu không được ghi số đo như sự thật khi trạng thái đúng là `KHÔNG ĐO ĐƯỢC`.

Gợi ý vá:

- Vá §9, nơi packet vừa đưa con số này vào sổ nợ sống.
- Bỏ số 8 hoặc ghi rõ `KHÔNG ĐO ĐƯỢC`; có thể ghi phép đo thật hiện tại là thiếu `actionlint` làm `t33` fail-close, suite `41/42`.
- Nếu muốn giữ số 8, phải đưa tám fixture/mutant có tên vào test và đếm kết quả máy; bỏ một fixture phải làm chốt số lượng đỏ.
- Rủi ro: không được đếm tám lỗi cùng chết vì thiếu một dependency rồi gọi đó là tám lớp protection độc lập.

### Finding 3 — P2: bất biến đếm `2 = 2` hiện chỉ là ảnh chụp, không phải cổng

HEAD hiện đúng:

```text
ci_markers=2
ledger_matching_headings=2
```

Hai ID cũng tương ứng chính xác.

Trên bản sao toàn cây, thêm marker thứ ba vào `ci.yml` mà không thêm mục sổ nợ cho kết quả:

```text
ci_markers=3
ledger_matching_headings=2
lease_publish: 42/42 đạt
actionlint_rc=0 workflow_files=5
doc_claims_ok=True advisory_count=366
```

Vì vậy không có ca máy canh phép đếm; người sau có thể thêm marker thứ ba và mọi cổng liên quan vẫn xanh.

Bất biến bị cắt: mỗi marker `NỢ CÓ TÊN` trong `ci.yml` phải có đúng một mục tương ứng trong sổ nợ.

Gợi ý vá:

- Thêm ca mới cạnh `t42`, vì suite này đã đọc `ci.yml` và packet được phép sửa đúng tệp test đó.
- Trích ID từ các dòng comment marker trong `ci.yml`, trích ID từ tiêu đề mục sổ nợ, rồi so hai tập bằng nhau; không chỉ so tổng.
- Đột biến thêm marker thứ ba phải làm đúng ca mới đỏ.
- Rủi ro: giới hạn parser vào comment marker và tiêu đề mục để các câu giải thích có chữ “NỢ CÓ TÊN” không bị đếm nhầm.

### Phần đã đo và giới hạn

- `lease_publish_test.py`: `42/42`, rc=0.
- `workflow-audit`, `golden-test`, `doc-claims-check`, `determinism-audit`, `release-verify`: đều `rc=0`, `ok=true`; release verify có `failed=[]`.
- Full `tl --selftest` tại môi trường reviewer đạt `1696/1698`; hai ca đỏ là `r226_nguong_l2_troi_theo_abbrev_va_ci_ghim` và `r268_l2_trichotomy_theo_trang_thai_object`, không thuộc hai tệp diff. Vì vậy tôi không khai lại số `1698/1698` của executor là đã được xác minh độc lập.
- §10 đo tĩnh đúng: bước `don-nhanh` có `if: runner.os != 'Windows'`, và các tệp `.ps1`, `.cmd`, test đều tồn tại. Chạy thật Windows/Linux trong phiên này là **KHÔNG ĐO ĐƯỢC** vì không có Windows hoặc `pwsh`.
- Trạng thái branch protection thực tế nằm ngoài cây và là **KHÔNG ĐO ĐƯỢC** trong phiên này.
- Kho thật không bị sửa; HEAD và trạng thái sạch được kiểm lại sau toàn bộ phép đo.

VERDICT: changes_requested
Reviewed commit: 181bd7f822f84a528da4cfde810d240bcc726dbf
diff --git a//tmp/rv216-review.FmNxkB/m1/ops/lease_publish_test.py b//tmp/rv216-review.FmNxkB/m1/ops/lease_publish_test.py
index d0e924ce331d1977f2ef4470a43771fbc51033df..ace40adf4001f0b8fe515e6011d58f86535f1545
--- a//tmp/rv216-review.FmNxkB/m1/ops/lease_publish_test.py
+++ b//tmp/rv216-review.FmNxkB/m1/ops/lease_publish_test.py
@@ -1282,7 +1282,7 @@
 
     PHẠM VI ĐO ĐƯỢC: t34 chỉ nhận canonical
     `python|python3|py <đường-dẫn>/lease_publish_test.py` KHÔNG CỜ. Năm dạng đã đo là
-    lọt: `python -m ops.lease_publish_test`; `python3 -u ops/lease_publish_test.py`;
+    lọt: `python -m ops.lease_publish_test`;
     shebang trực tiếp `./ops/lease_publish_test.py`; `uv run ops/lease_publish_test.py`;
     và `python -X utf8 ops/lease_publish_test.py`. Runner khác ngoài ba token canonical
     cũng không thuộc lời hứa. Lời khai được hạ xuống đúng phép đo thay vì nối regex để
diff --git a//tmp/rv216-review.FmNxkB/m2/ops/lease_publish_test.py b//tmp/rv216-review.FmNxkB/m2/ops/lease_publish_test.py
index d0e924ce331d1977f2ef4470a43771fbc51033df..3a6c0de0d333d5c02c4222e10d9cc3779c39479e
--- a//tmp/rv216-review.FmNxkB/m2/ops/lease_publish_test.py
+++ b//tmp/rv216-review.FmNxkB/m2/ops/lease_publish_test.py
@@ -1291,7 +1291,7 @@
     Đổi wrapper thành một trong các dạng lọt vẫn có cùng nghĩa với xoá wiring của gate;
     một selftest không thể tự chứng minh nó đã được CI gọi.
 
-    PHẠM VI BẰNG SỐ: `t34` che **3/8 = 37,5%** dạng gọi đã biết (3 canonical nhận được,
+    PHẠM VI BẰNG SỐ: `t34` che **ba trên tám = 37,5%** dạng gọi đã biết (3 canonical nhận được,
     5 dạng đã đo là lọt). Nói bằng số vì "che phần lớn" là lời khai không có phép đo, và
     kho đã trả giá đúng hình dạng ấy nhiều lần.
 
diff --git a//tmp/rv216-review.FmNxkB/m3/ops/lease_publish_test.py b//tmp/rv216-review.FmNxkB/m3/ops/lease_publish_test.py
index d0e924ce331d1977f2ef4470a43771fbc51033df..9cdc8dc101cd530aa01171d542838856b39102a2
--- a//tmp/rv216-review.FmNxkB/m3/ops/lease_publish_test.py
+++ b//tmp/rv216-review.FmNxkB/m3/ops/lease_publish_test.py
@@ -2010,7 +2010,7 @@
     "python -m ops.lease_publish_test",
     "python3 -u ops/lease_publish_test.py",
     "./ops/lease_publish_test.py",
-    "uv run ops/lease_publish_test.py",
+    "pipx run ops/lease_publish_test.py",
     "python -X utf8 ops/lease_publish_test.py",
 )
 
diff --git a//tmp/rv216-review.FmNxkB/m4/ops/lease_publish_test.py b//tmp/rv216-review.FmNxkB/m4/ops/lease_publish_test.py
index d0e924ce331d1977f2ef4470a43771fbc51033df..496d1e9e1d6df202b3d3b734a995c52cbfd7b32a
--- a//tmp/rv216-review.FmNxkB/m4/ops/lease_publish_test.py
+++ b//tmp/rv216-review.FmNxkB/m4/ops/lease_publish_test.py
@@ -1340,7 +1340,7 @@
 # và không được nối regex ở packet này. Nợ "CI có chạy gate không" thuộc required
 # status check được nêu ngay trong t34.
 _CHAY_BO_TEST = __import__("re").compile(
-    r"""(?<![\w.])(?:python3?|py)\s+["']?\S*lease_publish_test\.py["']?""")
+    r"""(?<![\w.])(?:python3?|py)\s+(?:-\S+\s+)*["']?\S*lease_publish_test\.py["']?""")
 
 
 def _goi_actionlint_gia(dich, ver, than):
diff --git a//tmp/rv216-review.FmNxkB/m5/.github/workflows/ci.yml b//tmp/rv216-review.FmNxkB/m5/.github/workflows/ci.yml
index c93bf40290219c17b5a2f914687f6754d022436e..73124ea7b6a8ee41e28b19771af5204a9629f1a6
--- a//tmp/rv216-review.FmNxkB/m5/.github/workflows/ci.yml
+++ b//tmp/rv216-review.FmNxkB/m5/.github/workflows/ci.yml
@@ -135,6 +135,7 @@
       # NỢ CÓ TÊN `PLAT-X5-required-status-check`: selftest không thể tự chứng minh job
       # này thật sự được GitHub gọi. Branch protection phải require status của job `gate`;
       # t34 chỉ còn canh lời gọi thẳng tệp `.py`, không giả làm bộ phân tích shell.
+      # NỢ CÓ TÊN `MUTANT-thu-ba-khong-co-muc-so-no`: marker cố ý để đo phép đếm.
       - name: lease-publish selftest (cài công cụ + chạy cổng)
         shell: bash
         env:

