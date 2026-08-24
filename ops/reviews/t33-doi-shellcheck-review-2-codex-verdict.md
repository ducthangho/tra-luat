verdict: changes_requested
reviewed_sha: efcf5757403bd989c0ebbd388fa7a7180171b49f
luot: 2

## ĐỐI CHIẾU LƯỢT TRƯỚC

- Bảy ô: KHÔNG KIỂM ĐƯỢC **trên cây pristine trong môi trường hiện tại** — smoke pristine ra `80/98` vì tại thời điểm đo có cả `TMPDIR/.git` và `/tmp/.git` (Issue #296, không phải finding #293). Với đúng hiệu chỉnh #296 được giao, tự dựng X1/X2, không dùng `bay_o.sh`, cho đủ bảy số khớp lượt 1.
- Giải thích `bỏ qua=8`: ĐÚNG — tám dòng là `t51`, `t52`, `t59`, `t60`, `t62`, `t63`, `t66`, `t68`; `t73` vẫn chạy và đỏ.
- 5 dòng chứa `_ly_do_bo_qua_workflow` (189, 2308, 2612, 3136, 3151): ĐÚNG — dòng 3136 là docstring.
- 4 định nghĩa + lời gọi thật: ĐÚNG — định nghĩa 189; AST cho call ở **2308, 2612, 3151**. Số 2613/3152 của bản nháp là sai.
- Chỉ `t70` gọi thẳng hàm: ĐÚNG — AST cho call dòng 2612; `t98` không gọi thẳng.
- Gỡ mọi ca gọi thẳng vẫn còn răng dây nối: ĐÚNG với hiệu chỉnh #296 — X1 đỏ `t73` ở 88/89; X2 đỏ `t98` ở 96/97.
- Khối `t98` chép nguyên văn từ r3, băm `4c9b223d…`: ĐÚNG — đối chiếu hồ sơ lượt 1 và diff không thấy sai khác khối.
- Bỏ mock `os.name` cho 96/98, đỏ `t72` và `t98`: ĐÚNG với hiệu chỉnh #296; `t73` không đỏ. Runner có `os.name == "posix"`, nên `t73(..., "posix")` không đổi trạng thái thật, còn `t98(..., "nt")` thì có.
- Không có cơ chế canh docstring `t33`: ĐÚNG — `doc-claims-check --strict`, `doctrine-scan`, `adr-song` đều rc=0; thân `t33` chỉ lint `ops-publish-lease.yml`.
- Windows thật: KHÔNG KIỂM ĐƯỢC — không có runner Windows; mock không thay thế Windows thật.
- GitHub trực tiếp: KHÔNG KIỂM ĐƯỢC — `origin` là mirror cục bộ.
- Spec r3 có băm `78c3ecb4…`: ĐÚNG — đo được `78c3ecb40eb8dd7dcf628ef7ea9a372aae5cfbf7a4fcfd25bb4ec7f32fe6ea0d`.
- Exact head/base và numstat: ĐÚNG — head `efcf5757403bd989c0ebbd388fa7a7180171b49f`, base `f33c12db19e7bcc0b18b394635a142c9d45d671d`, đúng một tệp `+22/-1`, dưới trần 120 dòng.
- Ghi chú môi trường có hai `.git` rỗng: ĐÚNG cho quan sát lượt 1 và lượt 2 lúc 00:27:51Z — cả hai hiện diện, read-only, giữ nguyên qua sáu mẫu cách nhau 2 giây. Khẳng định executor rằng chúng vắng ở thời điểm trước/sau khác KHÔNG THỂ BÁC từ ảnh chụp này; cả hai có thể đúng nếu trạng thái thoáng qua.
- “Hiệu chỉnh #296 tách biệt với X1/X2”: KHÔNG KIỂM ĐƯỢC theo chuẩn lượt 2 — bảy ô có hiệu chỉnh khớp, nhưng phép đo pristine bắt buộc bị môi trường làm hỏng.
- “Không có finding trong write set”: SAI — docstring `t98` gọi phép chạy worktree cục bộ là “toàn chân Ubuntu”; xem finding dưới.
- M3 bắt X2, giữ X1, sống khi gỡ ca gọi thẳng và giết đột biến dây nối: ĐÚNG với hiệu chỉnh #296; riêng bảy ô pristine vẫn KHÔNG KIỂM ĐƯỢC.
- M4 hạ lời `t33` đúng với thân: ĐÚNG — thân lint đúng một tệp; kho có 5 workflow nên còn đúng 4 tệp không được lint.

## BẢNG ĐO

| khẳng định | ai khai | đo được | khớp? |
|---|---|---|---|
| `TMPDIR` đúng gốc sandbox | hồ sơ | `/rv293/tmpdir` | có |
| smoke pristine head | hồ sơ: `98/98` | `80/98`, rc=1; hai `.git` rỗng hiện diện | KHÔNG ĐO ĐƯỢC do #296 |
| NỀN | PR/lượt 1/executor | hiệu chỉnh #296: `97/97`, chạy 97, bỏ qua 0, rc=0 | có (không phải pristine) |
| NỀN + X2 | PR/lượt 1/executor | hiệu chỉnh #296: `97/97`, chạy 97, bỏ qua 0, rc=0 | có (không phải pristine) |
| VÁ | PR/lượt 1/executor | hiệu chỉnh #296: `98/98`, chạy 98, bỏ qua 0, rc=0 | có (không phải pristine) |
| VÁ + X1 | PR/lượt 1/executor | hiệu chỉnh #296: `89/90`, chạy 90, bỏ qua 8, đỏ `t73`, rc=1 | có (không phải pristine) |
| VÁ + X2 | PR/lượt 1/executor | hiệu chỉnh #296: `97/98`, chạy 98, bỏ qua 0, đỏ `t98`, rc=1 | có (không phải pristine) |
| VÁ + X1 · gỡ t70 | PR/lượt 1/executor | hiệu chỉnh #296: `88/89`, chạy 89, bỏ qua 8, đỏ `t73`, rc=1 | có (không phải pristine) |
| VÁ + X2 · gỡ t70 | PR/lượt 1/executor | hiệu chỉnh #296: `96/97`, chạy 97, bỏ qua 0, đỏ `t98`, rc=1 | có (không phải pristine) |
| bỏ mock `os.name` | executor | hiệu chỉnh #296: `96/98`, đỏ đúng `t72`, `t98`; `t73` không đỏ; rc=1 | có |
| số dòng chứa tên hàm | lượt 1 | 5: 189, 2308, 2612, 3136, 3151 | có |
| định nghĩa + call thật | lượt 1 | định nghĩa 189; AST call 2308, 2612, 3151 | có |
| call thẳng trong ca | lượt 1 | chỉ `t70`, dòng 2612 | có |
| `t33` lint đúng một tệp | PR | `actionlint` nhận đúng `ops-publish-lease.yml` | có |
| số workflow không được `t33` lint | PR | 5 tệp tổng; 1 được lint; còn 4 | có |
| docstring `t98`: “toàn chân Ubuntu” | PR | nguồn phép đo là worktree cục bộ; không có run/job Ubuntu thật | không |
| spec r3 SHA-256 | hồ sơ | `78c3ecb40eb8dd7dcf628ef7ea9a372aae5cfbf7a4fcfd25bb4ec7f32fe6ea0d` | có |
| head/base | hồ sơ | `efcf5757403bd989c0ebbd388fa7a7180171b49f` / `f33c12db19e7bcc0b18b394635a142c9d45d671d` | có |
| phạm vi/numstat | lease/PR | đúng `ops/lease_publish_test.py`; `22/1`; trần thêm 120 | có |
| cổng tài liệu | lượt 1 | ba cổng rc=0 | có |
| M1/M2 thuộc packet #290; pin một nơi | phạm vi | không có cơ sở tạo pin thứ hai trong PR này | có |
| Windows thật | hồ sơ | KHÔNG ĐO ĐƯỢC — không có runner Windows | KHÔNG ĐO ĐƯỢC |
| GitHub trực tiếp | hồ sơ | KHÔNG ĐO ĐƯỢC — chỉ có mirror cục bộ | KHÔNG ĐO ĐƯỢC |

### ubuntu-leg-overclaim  [P2]  Docstring biến phép đo worktree cục bộ thành kết quả của cả chân Ubuntu

TỆP/DÒNG: `ops/lease_publish_test.py:3133-3134`

VẤN ĐỀ: Spec r3 mô tả X2 được chạy trên một `git worktree` rời; sandbox không đo trạng thái GitHub trực tiếp. Docstring lại ghi `rc=0 trên toàn chân Ubuntu`, cách nói chỉ cả job/leg CI và rộng hơn bằng chứng hiện có. Đây chính hình dạng lời khai rộng hơn phép đo mà M4 đang sửa ở `t33`. Nó không làm yếu răng của `t98`, nhưng để lại metadata sai ngay trong ca mới.

ĐÃ THỬ VÁ: có — trong `goi-va-293-luot2/`, đổi thành `rc=0 khi chạy cục bộ trên Linux (đo 23-08-2026)`, không đổi logic.

ĐÃ THỬ NGHIỆM: `python3 scripts/tl.py doc-claims-check --strict` trên cây đã sửa ⇒ rc=0; `git diff --check` ⇒ rc=0; delta đề xuất `1/1`. Suite pristine của đề xuất: KHÔNG ĐO ĐƯỢC vì #296 đang hoạt hóa; thay đổi chỉ ở docstring.

ĐỘ TIN: cao
