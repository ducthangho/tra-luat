# Cross-review ĐỘC LẬP sau merge — PR #945 (packet #899 `wp899` r4), lớp **sensitive**, mục đích: reviewer assurance §8.1

Bạn là REVIEWER độc lập (Codex/OpenAI). Executor và người ghi sổ là Claude. Không kế thừa context của ai; không gọi subagent;
không đăng GitHub; không đẩy git; không sửa tệp nào trong cây kho (`git status` phải sạch khi xong). Mọi tệp bạn tạo nằm trong
`.review/` (đã có trong `.git/info/exclude`). Chủ kho chọn chạy lượt này (#955, phương án A) để đo được model phục vụ.

## Đối tượng — định danh bằng BĂM, không bằng tên nhánh

| | |
|---|---|
| reviewed_sha (HEAD) | `4511b1eb6168904da117791cea178aa0c80e0e47` — đúng head đã merge vào master qua PR #945 (merge `cebb5b2`) |
| phạm vi diff | **`git diff f9f4a8d6da2d351fbcf5203256aba4e1bbf027b7 HEAD`** (đúng diff của PR #945: 3 tệp, +2045/-0). Diff toàn cây từ base lease `ba222ff` lẫn các merge master — KHÔNG review phần ấy |
| base lease | `ba222ffd1615f0d74b59985b9612f725211b62f5` |
| đặc tả | `.review-input/wp899-r4.md`, sha256 `be1e1feabe7c23b832168e36b0cce333043863af505e65c48d5a22d2101cef45` — kiểm băm, đọc TRỌN; r4 dẫn nguyên văn một số mục của r2/r3, chỗ nào thiếu thì ghi `KHÔNG ĐO ĐƯỢC` |
| write set | `ops/ci_provenance.py` · `ops/ci_provenance_test.py` · `.claude/dev/ci_dang_ky_test.py` |

Tham khảo (LỜI KHAI, không phải bằng chứng): `.review-input/VERDICT-r4-luot11.md` — lượt approve offline cuối, chấm `1f731c7`.
`4511b1e` = `1f731c7` + merge `origin/master` `f9f4a8d` + một commit thêm dòng `MOI`. Bạn phải TỰ ĐO lại, không chép kết luận.

## Cách làm — BẮT BUỘC

1. `.review/VERDICT.md` với `verdict: pending` ngay đầu, cập nhật dần.
2. Kiểm băm đặc tả, HEAD, phạm vi diff, write set.
3. Chạy ca có sẵn (`python -B ops/ci_provenance_test.py`, `--mot-ca <tên>`) và đột biến BẢN VÁ trên BẢN SAO TẠM (`python -B`,
   `PYTHONDONTWRITEBYTECODE=1`); chỉ tính giết khi ca đích chết bởi `TinHieuChotCa` của ĐÚNG ca.
4. Review theo LỚP: mỗi biểu hiện khái quát thành một lớp nguyên nhân, quét mọi biểu hiện cùng lớp trước khi báo. Ưu tiên luật năm
   trạng thái (thiếu dữ liệu không bao giờ thành `passed`), định danh bước/kịch bản (lớp F02 lịch sử), SHA checkout từ log, `MOI`
   một nguồn, ghi nguyên tử, mã thoát và dòng `NOT_MEASURED`, REST giả giữ trạng thái, mutant giết đúng lý do.
5. **Không tự soạn nội dung tấn công nhạy cảm**; hướng nào cần thì MÔ TẢ BẰNG LỜI.
6. Không có mạng; mọi lời khai LIVE (A10) là `KHÔNG ĐO ĐƯỢC` trong lượt này.

## Hạng

P0 bằng chứng sai theo hướng có lợi (thiếu/lệch mà ra `passed`, rc 0 khi phải 12/3) hoặc rò credential · P1 vi phạm mục tiêu/tiêu
chí đo được, ca/mutant không có răng ở chốt đặc tả đòi · P2 lỗi thật nhưng hẹp · P3 nợ, kèm đề xuất quyết định có căn cứ.

## Đầu ra — `.review/VERDICT.md`

Dòng đầu `verdict: approve` hoặc `verdict: changes_requested`; rồi `reviewed_sha:`, `base_sha:`, `Reviewed commit: <40 hex>`.
Approve CHỈ khi P0 = P1 = P2 = 0. Bắt buộc **BẢNG LỚP** `| lớp | hạng | biểu hiện (tệp:dòng) | phép đo tái hiện | HINT |`,
danh sách mutant kèm hạng, và mục giới hạn. Không khẳng định thứ chưa đo.
