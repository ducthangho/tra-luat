# ĐÍNH CHÍNH 1 — spec r3 của packet #541, tiêu chí `N6'`

| | |
|---|---|
| áp cho | `ops/specs/wp541-path-toi-thieu-theo-nen-r3.md`, `spec_hash 3920f23f9635e46899dac4157a8d1e7eb49a3dee64996ca9fe0644e87b1a379d` |
| phát hiện | `2026-09-18T18:20Z`, phiên điều phối claude, khi rà soát bản vá g2 của `agy` (`9583168`) |
| trạng thái spec | **KHÔNG SỬA.** Xem §4. |

> **Tệp này KHÔNG phải một revision.** Nó không đổi `spec_hash`, không làm lease mất hiệu lực,
> không mở rộng phạm vi. Nó sửa **một câu sai về CÁCH ĐO** trong một tiêu chí, và chỉ thế.

## 1. Câu sai

Spec r3 §`nghiem_thu`, tiêu chí **`N6'`**, nguyên văn:

> `git diff --numstat` so `d705623162b75b7340ee7cca54ac2d2abbddbb6f`: **≤ 2 tệp và ≤ 400 dòng thêm**.

Và spec r3 §`Ràng buộc thi công`, cũng nguyên văn:

> **Hoà `origin/master` bằng MERGE, KHÔNG rebase** — `2f70869a` là `reviewed_sha` của bốn lượt.

**Hai câu ấy mâu thuẫn nhau.** Sau khi executor merge `origin/master` theo đúng chỉ thị, phép đo
`--numstat` so một base **trước lúc merge** sẽ đếm cả những gì master mang vào — tức đếm việc của
packet KHÁC vào hạn ngạch của packet này.

## 2. Phép đo — con số thật, không phải lo xa

Trên bản vá g2 của `agy`, head `9583168`, đo `18:20Z 18-09-2026`:

```
so d705623   ->  5 tep, +812    (gom ops/reviews/README.md,
                                 ops/reviews/ci-windows-review-5-claude-verdict.md,
                                 ops/reviews/ci-windows-review-5-claude-verdict.receipt.yaml
                                 — ba tep nay den TU origin/master qua merge eb15657)
so merge-base ->  2 tep, +353   <- viec THAT cua agy
```

`merge-base(origin/master, fix_issue_541)` lúc đo = `eb15657`.

Đối chứng: cả ba tệp `ops/reviews/*` kia **có mặt trên `origin/master`** — chúng không do `agy` viết.

## 3. Hậu quả nếu làm đúng theo chữ

`+812 > 400`. Một người chấm theo đúng chữ của `N6'` sẽ kết luận **VƯỢT TRẦN** và bác một bản vá
**không hề vượt trần** — `2 tệp / +353` nằm gọn trong `2 tệp / 400 dòng`.

Đây không phải rủi ro lý thuyết: nó là kết quả mà chính phiên soạn spec thu được khi chạy phép đo
đầu tiên, và suýt báo sai.

## 4. Luật ĐÚNG

> **`N6'` đo `git diff --numstat` so `merge-base(origin/master, HEAD)`**, không so một SHA ghim sẵn.
> Ngưỡng giữ nguyên: **≤ 2 tệp và ≤ 400 dòng thêm**.
> Không tính được `merge-base` ⇒ **`KHÔNG ĐO ĐƯỢC`**, không đoán, không rơi về base cũ.

Con số theo base cũ vẫn nên IN RA làm **đối chiếu**, kèm câu nói rõ nó không dùng để chấm — để
người đọc thấy chênh lệch và hiểu vì sao.

## 5. Vì sao KHÔNG sửa thẳng vào spec

Sửa spec đổi `spec_hash` ⇒ theo `docs/PROTOCOL_DA_PHIEN.md` §3.2 phải **cấp lại lease**, và lease
`wp541-path-r2-g2-antigravity` đang có hiệu lực với executor đã giao hàng xong. Cái giá ấy lớn hơn
một câu về cách đo **không đổi ngưỡng, không đổi phạm vi, không đổi write set, không đổi mục tiêu
nào**. Chủ kho quyết định như vậy, phiên điều phối 18-09-2026, nguyên văn: *"không sửa spec, ghi
đính chính thôi"*.

Nếu sau này packet #541 có revision vì lý do khác, **gộp câu §4 vào spec lúc đó** thay vì để đính
chính sống mãi bên cạnh.

## 6. Đã sửa ở đâu rồi

`ops/reviews/wp541-do-g2-windows.py` (và bản đóng gói `ops/reviews/wp541-do-g2.ps1`) nay tính
`merge-base(origin/master, HEAD)` và chấm theo đó; vẫn in con số theo base cũ làm đối chiếu, kèm
câu cảnh báo. Commit `bc183c0` trên nhánh `claude/do-541-g2-20260918`.

## 7. Bài học — thuộc họ đã có trong `CLAUDE.md`

Kho đã ghi: *"PHÉP ĐO DELTA SO HAI VẾ PHẢI DỰNG CẢ HAI TRONG MỘT LỆNH"*, và
*"một bất biến còn đúng không chứng minh các số hạng còn đúng"*. Đây là mặt thứ ba của cùng gốc:

**Một tiêu chí đo DELTA mà ghim MỘT vế bằng SHA sẽ chết ngay khi vế kia được lệnh di chuyển.**
Spec vừa ghim base, vừa ra lệnh merge — hai câu ấy ở cách nhau bảy mục trong cùng một tệp, mỗi câu
đọc riêng đều đúng, và người viết chúng là cùng một phiên. Chỗ hỏng không nằm trong câu nào cả; nó
nằm giữa hai câu.

Nếp rút ra: **tiêu chí đo delta phải khai vế nền bằng một PHÉP TÍNH (`merge-base`), không bằng một
HẰNG SỐ** — trừ khi spec cũng cấm luôn việc di chuyển vế kia.
