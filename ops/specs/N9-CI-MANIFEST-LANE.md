# ĐẶC TẢ ĐÓNG BĂNG — `N9-CI-MANIFEST-LANE`

Packet Issue: #427 · Gỡ nút thắt cho #421 · Họ hàng #413 (cùng chạm `.github/workflows/**`,
nhưng là HAI packet riêng)

Đặc tả này ĐÓNG BĂNG khi lease neo băm của nó. Sửa sau khi cấp lease là làm `spec_hash` trỏ
vào thứ không còn tồn tại — đường đi vòng qua §3.2.

## 1. Vấn đề — mâu thuẫn CẤU TRÚC, đo được

| nguồn | nói gì |
|---|---|
| `PROTOCOL:652` | Worker **không sửa** `RELEASE_MANIFEST.json` |
| `PROTOCOL:710` | Worker CI **không so** feature branch với manifest **committed** |
| `ci.yml:511` | chạy `release-verify RELEASE_MANIFEST.json --strict --json`, **không `if:`** |

Bước ấy ở trong job `gate`, mà `gate` chạy cho **cả** `push`, `pull_request` và
`workflow_dispatch` (`ci.yml:11-19, 35`). Nên mọi PR chạm một tệp có trong manifest đều **buộc**
worker sửa manifest committed để CI xanh — cấu hình CI **ép** worker làm đúng thứ protocol cấm.

Không phải lỗi của phiên nào. Đã đẻ ra một P1 thật ở packet `N8-REVIEW-KEM-PATCH` (#421):
lease của N8 phải cấp `RELEASE_MANIFEST.json` vào write set chỉ để CI xanh.

## 2. Việc — và ĐỪNG đọc thành "tắt cổng đi"

Bước `--strict` đang bảo vệ một thứ THẬT, chú thích ngay trên nó nói rõ: *"file THỪA trong cây
mà manifest không có ⇒ ĐỎ (bản cũ chỉ cảnh báo rồi trôi qua)"*. Bỏ hẳn ở lane PR là **mất** lớp
ấy tới tận lúc land.

`PROTOCOL:711-715` nêu đường giữ được cả hai: worker **được** sinh manifest **TẠM ngoài repo**
và kiểm byte/topology trên đó — chỉ không được so với bản **committed**, không được sửa tệp
land-only trong diff.

Yêu cầu:

1. Lane **land** (`push` vào nhánh mặc định): giữ nguyên đối chiếu manifest committed.
2. Lane **worker** (`pull_request`): KHÔNG so với manifest committed; thay bằng phép kiểm tương
   đương dùng manifest TẠM sinh ngoài repo, vẫn bắt được "file thừa trong cây".
3. `workflow_dispatch`: chọn lane và **NÊU LÝ DO**. Không để rơi vào khoảng xám.

## 3. Write set — ĐÚNG 1 tệp

```
.github/workflows/ci.yml
```

Đo `2026-08-31`: `ai-dang-giu` cho `.github/workflows/ci.yml` ⇒ `NGƯỜI_GIỮ 0` (hai lease chạm
đường này — `cong-ngoai-write-set-exec-1r5` và `plat-x2-exec-3` — đều HẾT_HẠN). Quét cả
`.github/workflows/` cũng `NGƯỜI_GIỮ 0`.

Cần tệp thứ hai ⇒ `S1`, DỪNG và trình người giữ. KHÔNG tự nới.

## 4. CHỐT BẮT BUỘC — bốn phép đo, thiếu cái nào thì packet chưa xong

1. **Lớp bảo vệ KHÔNG mất.** Phản chứng: thêm một tệp thừa vào cây trên một PR giả lập ⇒ lane
   PR **phải ĐỎ**. Thiếu phép đo này thì bản vá chỉ là "tắt cổng cho đỡ vướng".
2. **Lane land KHÔNG đổi hành vi.** Cùng phản chứng ở lane land vẫn ĐỎ.
3. **PR chạm tệp trong manifest KHÔNG còn buộc sửa manifest.** Đây là MỤC TIÊU của packet;
   thiếu nó thì không biết đã chữa được gì.
4. **`actionlint` chạy thật và rc được ghi.** Xem §5.

`release-verify` có hỗ trợ chế độ manifest-tạm hay không — **CHƯA AI ĐO**. Nếu không thì nêu
đường thay thế kèm phép đo, đừng viết một câu hứa không kiểm được.

## 5. `actionlint` — BẮT BUỘC, và fail-close khi thiếu công cụ

Tệp này đã đốt kho: `ops-don-ref.yml` từng bị GitHub **TỪ CHỐI** vì một cặp `${{ }}` RỖNG nằm
trong một dòng **CHÚ THÍCH** của thân `run`. GitHub nội suy biểu thức trên TOÀN BỘ thân `run`
trước khi shell thấy nó, nên một biểu thức rỗng trong comment làm cả tệp không hợp lệ.

Dấu hiệu KHÔNG phải một job đỏ mà là: một workflow run mang tên **ĐƯỜNG DẪN TỆP**, **0 job**,
`conclusion: failure`. `get_job_logs` trả `total_jobs: 0` nên đi tìm log sẽ không thấy gì.

**SÁU lượt cross-review đều kết luận "YAML ok"** vì cả sáu chỉ kiểm bằng PyYAML, mà PyYAML
không biết luật của GitHub. Nên: chạy `actionlint` THẬT, và **thiếu công cụ thì ĐỎ** — một cổng
tự tắt khi thiếu công cụ là cổng không tồn tại đúng lúc nó cần nhất.

Nền đã đo (23-08-2026): `actionlint` trên toàn bộ workflow ⇒ `rc=1`, một finding
`ops-don-ref.yml:106 SC1003:info`. **ĐỎ SẴN** — phải đo nền trước khi nghi bản vá của mình.
Và nền ấy phụ thuộc `shellcheck` CÓ MẶT hay không: thiếu `shellcheck` thì `actionlint` im lặng
bỏ luật nền ấy và trả `rc=0`. Ghi rõ `shellcheck` có hay không khi báo số.

## 6. Điều kiện dừng

- `S1` cần đường dẫn thứ hai ⇒ DỪNG, trình phép đo.
- `S2` muốn sửa `docs/PROTOCOL_DA_PHIEN.md` ⇒ DỪNG. Protocol là nguồn quy tắc; packet này làm
  CI **khớp** protocol, không sửa protocol cho khớp CI.
- `S3` không đo được lớp bảo vệ còn giữ ⇒ DỪNG. KHÔNG land một bản chỉ tắt cổng.
- `S4` `origin/master` đi tiếp so `base_sha` mà chưa đo lại ⇒ DỪNG.
- `S5` `actionlint` không chạy được ⇒ ĐỎ, không được bỏ qua.
- `S6` vượt 1 tệp hoặc 80 dòng thêm ⇒ DỪNG, KHÔNG tự khai cổng ADR-0044 là ĐẠT.

## 7. Chưa đo được — gọi tên tử tế

- `workflow_dispatch` nên thuộc lane nào: chưa có phép đo, là câu hỏi THIẾT KẾ cho phiên thi
  hành, phải nêu lý do chứ không chọn im lặng.
- Sau khi sửa, packet #421 có thật sự bỏ được `RELEASE_MANIFEST.json` khỏi write set không —
  phải đo trên chính nhánh của #421, không suy.
