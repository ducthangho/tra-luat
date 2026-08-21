# PROMPT EXECUTOR — `SLICE-B-C` (#215). Hai mục sổ nợ + hạ lời khai `t34`.

Bạn là executor cho packet nhỏ cuối cùng của Slice B. Đọc Issue #215 trước; tệp này chỉ đóng
băng PHẠM VI để phiên vá không tự nới việc cho mình giữa chừng.

## Write set — ĐÚNG hai tệp, không hơn
```
ops/NO_KY_THUAT.md
ops/lease_publish_test.py
```
Tệp thứ ba là finding, kể cả khi "chỉ sửa một dòng cho gọn".

## Ba việc

**1. Hai mục sổ nợ.** `.github/workflows/ci.yml` khai **2** chuỗi "NỢ CÓ TÊN" (dòng 135, 177) mà
`ops/NO_KY_THUAT.md` có **0** mục tương ứng. Đếm hai bên phải BẰNG NHAU sau khi xong.
- `PLAT-X5-required-status-check` — nợ **THƯỜNG TRỰC**, không phải nợ có hạn, vì người giữ kho đã
  quyết **Q7 = KHÔNG BẬT**. Ghi thẳng cái mất: câu hỏi *"CI có thật sự chạy gate không"* **vĩnh
  viễn không có nhà**. Ghi thẳng cái KHÔNG mất: với `PATH` thiếu `actionlint` vẫn còn **8 ca đỏ**
  — thứ mất là **DETECTION**, không phải **PROTECTION**. Đừng viết câu để ai đó đọc rộng hơn thực tế.
- `don-nhanh-test-chua-chay-duoc-tren-windows` — marker thứ hai.

**2. Hạ lời khai `t34` xuống phạm vi ĐO ĐƯỢC.** Q7 làm `t34` sống lâu dài, nên việc KHÔNG còn là
"xoá `t34`" mà là ghi vào docstring **nguyên văn năm dạng gọi đã ĐO là lọt**:
`python -m` · `python3 -u` · shebang trực tiếp · `uv run` · `python -X`.
Nói bằng SỐ: `t34` che **3/8 = 37,5%** dạng gọi đã biết. Đừng viết "che phần lớn".

**3. Một ca máy đòi docstring `t34` chứa đủ năm dạng ấy.** Kèm **ĐỘT BIẾN**: bỏ một dạng khỏi
docstring ⇒ ca đích phải **ĐỎ**. Không có đột biến thì không biết ca đang đo lời khai hay đo thứ
khác — và kho đã trả giá đúng chỗ này bốn lần.

## Chốt của kho, áp cho lượt này
1. Bằng chứng DƯƠNG: `N/N` hai số BẰNG NHAU, `"ok": true`. `rc=0` một mình đã lừa cổng này nhiều lần.
2. Đọc mã thoát TRỰC TIẾP (`OUT=$(cmd); RC=$?`), KHÔNG qua pipe — `| tail` nuốt rc, đã tái phát 3 lần.
3. Đột biến chạy trên BẢN SAO TẠM, không ghi vào tệp thật.
4. Đo nền TRƯỚC khi nghi bản vá của mình: cổng đỏ ⇒ chạy lại trên `origin/master` sạch, so DELTA.

## Tiêu chí hoàn tất — đo được, không phải mô tả
- số mục trong `NO_KY_THUAT.md` ứng với marker `ci.yml`: **2 = 2**
- `python3 ops/lease_publish_test.py` → `N/N` hai số bằng nhau (nền hiện tại: **41/41**, nay 42/42)
- đột biến "bỏ một dạng khỏi docstring `t34`" → ca đích **ĐỎ** (chứng minh bằng lượt chạy, không bằng lời)
- `tl.py --selftest` **1698/1698**
- `workflow-audit --strict` · `golden-test` · `doc-claims-check --strict` · `determinism-audit --strict`
  · `release-verify --strict` → cả năm `"ok": true`
- `git diff --numstat origin/master...HEAD` → **đúng 2 tệp**

## Không được làm
Không đụng `.github/workflows/**` (đó là write set của packet khác). Không đụng
`ops/lease_publish.py` — chỉ bộ TEST. Không bật required status check: Q7 đã quyết là KHÔNG.
