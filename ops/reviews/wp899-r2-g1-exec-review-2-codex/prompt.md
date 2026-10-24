# Cross-review OFFLINE — packet #899 `wp899` (CI-PROVENANCE-REST-LOG, P-A), lượt 2, lớp **sensitive**

Bạn là REVIEWER độc lập (Codex/OpenAI). Executor là Claude. Không kế thừa context executor; không gọi subagent; không đăng
GitHub; không đẩy git; không sửa tệp nào trong cây kho (`git status` phải sạch khi xong). Mọi tệp bạn tạo nằm trong `.review/`.

## Đối tượng — định danh bằng BĂM

| | |
|---|---|
| reviewed_sha (HEAD) | `7c5742c3bf46a427b1525a86247c7448a6149948` |
| lượt trước | `f43ea20fafaee9596d8a5847534cb8489217df02`, verdict ở `.review-input/VERDICT-luot1.md` (changes_requested, F01–F07) |
| base | `76cf4c51a6b1a5a0f30621c73f9a6f03e7e68138` |
| đặc tả | `.review-input/wp899-r2.md`, sha256 `d858c7c65a38a7f0fadda1cabf839c98ce70a881372d847c8979165925971707` (kiểm băm, đọc trọn) |
| write set | `ops/ci_provenance.py` · `ops/ci_provenance_test.py` · `.claude/dev/ci_dang_ky_test.py` |

Delta cần review: `git diff f43ea20 HEAD`; toàn bộ: `git diff 76cf4c5 HEAD`.

## Quyết định chủ kho sau lượt 1 (issuecomment-6380183334 trên #899) — coi là authority, không phải finding

- **Trần nâng lên ≤ 3 tệp / ≤ 900 dòng thêm** (`git diff --numstat <base> HEAD`). Lượt này executor khai 1 + 336 + 468 = 805.
- **A10 đính chính:** 13 job ra `b27fe85c9e9593ddbb059808fe4347fe1bd267be` (parents `5618020…` + `4005893…`, tree `857bc47…`),
  job `chuan-bi` (118368688427) ra `not_measured`. Như vậy F07 đóng bằng authority, không bằng mã. Đo lại LIVE trên HEAD này nằm ở
  `.review-input/a10/` (lời khai; bạn không có mạng).

## Cách làm — BẮT BUỘC

1. `.review/VERDICT.md` pending ngay đầu, cập nhật dần.
2. Kiểm băm/HEAD/base/write set/numstat.
3. **Đối chiếu từng lớp F01–F06 của lượt 1**: đã vá thật / vá một phần / chưa vá — mỗi lớp chạy lại ĐÚNG phép đo tái hiện của
   lượt 1 (các script lượt 1 không có trong workspace này; hãy dựng lại từ mô tả trong `VERDICT-luot1.md`) và đột biến bản vá để
   đo răng. Lớp nào xuất hiện lại biểu hiện mới cũng ghi.
4. Chạy ca có sẵn (`python -B ops/ci_provenance_test.py`, `--mot-ca <tên>`); đột biến trên BẢN SAO TẠM (`python -B`,
   `PYTHONDONTWRITEBYTECODE=1`); chỉ tính giết khi ca đích chết bởi `TinHieuChotCa` của ĐÚNG ca.
5. **Quét lớp MỚI** mà bản vá có thể sinh: parser lời gọi `loi_goi_python` (shlex/punctuation_chars, nhiều dòng, nối dòng `\`,
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
