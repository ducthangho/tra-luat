# Cross-review OFFLINE — packet #899 `wp899` (CI-PROVENANCE-REST-LOG, P-A), lượt 4, lớp **sensitive**

Bạn là REVIEWER độc lập (Codex/OpenAI). Executor là Claude. Không kế thừa context executor; không gọi subagent; không đăng
GitHub; không đẩy git; không sửa tệp nào trong cây kho (`git status` phải sạch khi xong). Mọi tệp bạn tạo nằm trong `.review/`.

## Đối tượng — định danh bằng BĂM

| | |
|---|---|
| reviewed_sha (HEAD) | `19b114867fbcad4c3b580bcbe4367bc78a890773` |
| lượt trước | lượt 1 `f43ea20…`, lượt 2 `7c5742c…`, lượt 3 `5ab75a4ca5b237f881a5be9ea97047d3f9395115` (`.review-input/VERDICT-luot3.md`, changes_requested: F01/F02 P0, F05 P1; F03 đã vá thật) |
| base | `76cf4c51a6b1a5a0f30621c73f9a6f03e7e68138` |
| đặc tả | `.review-input/wp899-r2.md`, sha256 `d858c7c65a38a7f0fadda1cabf839c98ce70a881372d847c8979165925971707` (kiểm băm, đọc trọn) |
| write set | `ops/ci_provenance.py` · `ops/ci_provenance_test.py` · `.claude/dev/ci_dang_ky_test.py` |

Delta cần review: `git diff 5ab75a4 HEAD`; toàn bộ: `git diff 76cf4c5 HEAD`.

## Quyết định chủ kho sau lượt 1 (issuecomment-6380183334 trên #899) — coi là authority, không phải finding

- **Trần nâng lên ≤ 3 tệp / ≤ 900 dòng thêm** (`git diff --numstat <base> HEAD`). Lượt này executor khai 1 + 359 + 539 = 899.
- **A10 đính chính:** 13 job ra `b27fe85c9e9593ddbb059808fe4347fe1bd267be` (parents `5618020…` + `4005893…`, tree `857bc47…`),
  job `chuan-bi` (118368688427) ra `not_measured`. Như vậy F07 đóng bằng authority, không bằng mã. Đo lại LIVE trên HEAD này nằm ở
  `.review-input/a10/` (lời khai; bạn không có mạng).

## Cách làm — BẮT BUỘC

1. `.review/VERDICT.md` pending ngay đầu, cập nhật dần.
2. Kiểm băm/HEAD/base/write set/numstat.
3. **Đối chiếu từng lớp còn mở của lượt 3 (F01, F02, F05) và giữ F03/F04/F06 đóng**: đã vá thật / vá một phần / chưa vá — mỗi lớp chạy lại ĐÚNG phép đo tái hiện của
   lượt 3 (script lượt 3 không có trong workspace này; dựng lại từ mô tả trong `VERDICT-luot3.md`) và đột biến bản vá để
   đo răng. Lớp nào xuất hiện lại biểu hiện mới cũng ghi.
4. Chạy ca có sẵn (`python -B ops/ci_provenance_test.py`, `--mot-ca <tên>`); đột biến trên BẢN SAO TẠM (`python -B`,
   `PYTHONDONTWRITEBYTECODE=1`); chỉ tính giết khi ca đích chết bởi `TinHieuChotCa` của ĐÚNG ca.
5. **Quét lớp MỚI** mà bản vá có thể sinh: parser lời gọi `RE_LOI_GOI`/`dong_logic`/`loi_goi_python` (nhiều dòng, nối dòng `\`,
   PowerShell/Windows, `python -m`, cờ có đối số như `-W x`), `lay_trang` (vòng lặp/điều kiện dừng, total đổi, thân sai dạng),
   bảng trường bắt buộc (kiểu `bool` là `int`, chuỗi rỗng, list rỗng), `goi_that` (vòng 2 lượt, redirect lồng), dòng
   `NOT_MEASURED` ở mọi đường thoát.
6. **Không tự soạn nội dung tấn công nhạy cảm**; hướng nào cần thì MÔ TẢ BẰNG LỜI.
7. Review theo LỚP (V3): khái quát biểu hiện thành lớp, quét mọi biểu hiện cùng lớp trước khi báo.

## Hạng

- **P0**: bằng chứng sai theo hướng có lợi (thiếu/lệch mà ra `passed`, rc 0 khi phải 12/3), hoặc rò credential.
- **P1**: vi phạm M1–M9/A1–A11 đo được; ca/mutant không có răng ở chốt đặc tả đòi.
- **P2**: lỗi thật nhưng hẹp, hoặc ca có mặt mà không đo.
- **P3**: nợ/chất lượng; kèm đề xuất quyết định (chấp nhận/vá) có căn cứ. Nếu P3 vá được rẻ trong write set, nói rõ HINT.

## Đầu ra — `.review/VERDICT.md`

Dòng đầu `verdict: approve` hoặc `verdict: changes_requested`; rồi `reviewed_sha:`, `base_sha:`, `Reviewed commit: <40 hex>`.
Approve CHỈ khi P0 = P1 = P2 = 0 (V2). Bắt buộc: bảng ĐỐI CHIẾU F01–F07; **BẢNG LỚP** mới
`| lớp | hạng | biểu hiện (tệp:dòng) | phép đo tái hiện | HINT patch |`; đối chiếu A1–A11; danh sách mutant kèm hạng. Không khẳng
định thứ chưa đo; không đo được thì ghi `KHÔNG ĐO ĐƯỢC`.

## Ghi chú lượt 4 — sau checkpoint chủ kho

- Lượt 3 chạm `dieu_kien_dung` (F01/F02/F05 lặp lần 3). Chủ kho duyệt vá lượt 4 theo **thiết kế đóng gốc** (issuecomment-6380890740
  trên #899) — coi là authority: F02 chỉ nhận khi **TOÀN KHỐI** kịch bản của bước là lời gọi tối giản; F01 kiểm từng phần tử `steps`
  và so khớp toàn chuỗi (`fullmatch`); F05 chiếu job chỉ từ trường đã hợp lệ + lưới cuối in dòng đếm cho mọi lỗi thu.
- Chủ kho: **lặp lớp ở lượt 4 thì dừng hẳn.** Phân loại thật chính xác: biểu hiện mới của F01/F02/F05 là LẶP LỚP; nguyên nhân khác
  thì đặt slug mới. Tấn công chính các thiết kế đóng gốc ấy (vd: dòng kịch bản được nhận diện bằng mã ANSI `\x1b[36;1m` — có
  cách nào làm một dòng không phải kịch bản mang mã ấy, hoặc dòng kịch bản thiếu nó?).
- Trần 900; ứng viên ở 899 nên mọi HINT cần đi kèm ước lượng số dòng.
