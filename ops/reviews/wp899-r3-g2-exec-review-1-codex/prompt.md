# Cross-review OFFLINE — packet #899 `wp899` (CI-PROVENANCE-REST-LOG, P-A), **revision 3**, lượt 1, lớp **sensitive**

Bạn là REVIEWER độc lập (Codex/OpenAI). Executor là Claude. Không kế thừa context executor; không gọi subagent; không đăng
GitHub; không đẩy git; không sửa tệp nào trong cây kho (`git status` phải sạch khi xong). Mọi tệp bạn tạo nằm trong `.review/`.
Bạn không có mạng.

## Đối tượng — định danh bằng BĂM, không bằng tên nhánh

| | |
|---|---|
| reviewed_sha (HEAD) | `29d641cbd4a38504eb30d87f0fc7eaa82a185f24` |
| base | `dc657149941f9db3ab2afc6fb6462ba4827bf18f` |
| điểm xuất phát | `9e5019e` = ba tệp chép nguyên văn từ ứng viên r2 `19b114867fbcad4c3b580bcbe4367bc78a890773` (commit cha của HEAD). Delta r3 thật: `git diff 9e5019e HEAD`; toàn bộ: `git diff dc65714 HEAD` |
| đặc tả r3 | `.review-input/wp899-r3.md`, sha256 `dd1a997d1f3682e23bb4b5577264076b7d9a12aeff5d9823f491cdda05e4f36f` (kiểm băm, đọc TRỌN) |
| đặc tả r2 (r3 dẫn nguyên văn nhiều mục) | `.review-input/wp899-r2.md`, sha256 `d858c7c65a38a7f0fadda1cabf839c98ce70a881372d847c8979165925971707` |
| verdict r2 | `.review-input/r2/VERDICT-r2-luot{1..4}.md` — đọc **lượt 4 trước** (F02 lặp lần 4 ⇒ có r3) |
| write set | `ops/ci_provenance.py` · `ops/ci_provenance_test.py` · `.claude/dev/ci_dang_ky_test.py` |

## Authority — coi là quyết định, KHÔNG phải finding

- Tám quyết định Q1–Q8 của đặc tả r3 (mục `quyet_dinh_r3`).
- **Trần nâng lên ≤ 8 tệp / ≤ 1050 dòng thêm** (chủ kho, #899 issuecomment-6383572422, 24-10-2026). Write set lease KHÔNG đổi
  (3 tệp). Executor khai `git diff --numstat dc65714 HEAD` = 1 + 388 + 627 = **1016**.
- Luật vòng đời V1–V5 (đặc tả r3). **V5: một lớp — kể cả F01–F07 kế thừa — lặp ở lượt review thứ 2 của r3 ⇒ DỪNG HẲN.** Đây là
  lượt 1 của r3, lời gọi Codex thứ 5/8. Vì vậy hãy quét ĐỦ ở lượt này: lớp nào bạn bỏ sót bây giờ mà lượt 2 thấy là packet chết.

## Thiết kế r3 executor đã thi công (để bạn tấn công, không phải để bạn tin)

1. Kịch bản của bước = `run:` của workflow đọc bằng `git cat-file blob <SHA checkout ĐÃ ĐO passed của chính job>:<path REST>`
   (`git_blob`, `thu()`), parse bằng `yaml.safe_load` (`ung_vien`). Log chỉ để ĐỊNH VỊ: khối in lại (`tach_buoc` → `in_lai`) phải
   BẰNG NGUYÊN VĂN `run.rstrip("\n")` của ≥ 1 ứng viên; luật lời gọi tối giản (`RE_LOI_GOI`, không đối số) áp lên `run:` YAML.
2. Chặn chế độ (`not_measured`, `che_do_khong_xac_dinh`): ứng viên khớp nào có khoá bước ngoài `KHOA_BUOC` (allowlist; gồm `env:`,
   `working-directory`…), `shell:` ngoài bash/pwsh/sh, job hoặc workflow có `defaults:` hoặc `env:` mang `CI_DANG_KY_*` (hoặc `env:`
   không phải dict), một `run:` bất kỳ trong workflow nhắc `GITHUB_ENV`/`GITHUB_PATH`, hoặc lời gọi có tiền tố `VAR=`. **Sáu vế sau
   vế (i)/(ii)/(iii) của A17 là executor tự thêm, ngoài chữ đặc tả** — đánh giá chúng có đúng/đủ/quá tay không.
3. Gate ghi thêm `kich_ban: {trang_thai, buoc_xac_thuc | ly_do}` để đo chính phép xác thực (dùng trong ca A14/A15).
4. **Giới hạn khai sẵn (executor): gốc tin là nội dung tại SHA checkout.** Một workflow tại SHA ấy vốn quyết định được mọi output
   (kể cả tự in một nhóm `##[group]Run …` giả bằng lệnh workflow, hoặc sửa chính script test). Công cụ không chống tác giả workflow.
   Nếu bạn cho rằng giới hạn này quá rộng hoặc có đường F02 KHÔNG cần quyền sửa workflow/script tại SHA, đó là finding.

## Cách làm — BẮT BUỘC

1. `.review/VERDICT.md` pending ngay đầu, cập nhật dần.
2. Kiểm băm spec, HEAD, base, write set, numstat, `git diff --check`.
3. **Đối chiếu F01–F07** (bảng `hinh_dang_ke_thua` của r3): F02 phải được chứng minh ĐÓNG trên thiết kế mới — chạy lại đúng hai phản
   chứng lượt 4 (`r4_F02_env_metadata`, `r4_F02_mixed_color`; dựng lại từ mô tả trong `VERDICT-r2-luot4.md`) và mọi biến thể cùng
   cơ chế bạn nghĩ ra. F01/F03–F07 phải giữ đóng (bản vá r3 đụng `moc_gate`/`thu`/`tach_buoc` — kiểm lại F01/F05 trên các trường mới).
4. Chạy ca có sẵn (`python -B ops/ci_provenance_test.py`, `--mot-ca <tên>`); đột biến trên BẢN SAO TẠM (`python -B`,
   `PYTHONDONTWRITEBYTECODE=1`, env `CI_PROVENANCE_MA=<bản sao>`); chỉ tính giết khi ca đích chết bởi `TinHieuChotCa` của ĐÚNG ca.
   Đo từng tiêu chí A14–A19 bằng đúng đột biến đặc tả nêu ở cột "phép đo làm ĐỎ".
5. **Quét lớp MỚI** bản vá r3 có thể sinh, gợi ý (không phải trần): ranh giới khối in lại (`##[endgroup]` thiếu/lồng, dòng trống
   trong `run:`, khoảng trắng đầu/cuối dòng, CRLF, `run:` kết thúc bằng nhiều `\n`, block scalar `|-`/`>`), đối chiếu nhiều ứng viên
   (A19, các job khác nhau, workflow gọi lại), `yaml.safe_load` (alias/anchor, khoá không phải chuỗi, `on:` thành `True`, YAML rất sâu,
   tệp không UTF-8), `git_blob` (đường dẫn REST lạ, SHA chưa đo, kho thiếu object), luật chặn (allowlist bước, `shell:` dạng
   `bash -e {0}`, env mức workflow, biểu thức `${{ }}` trong `env:`), và các đường đổi chế độ/đổi thứ được thực thi mà vẫn lọt.
6. A10: không đo LIVE được; `.review-input/a10/` là lời khai của executor (stdout + provenance hai run). Đối chiếu với kỳ vọng A10 của
   r3. Lưu ý diễn giải của executor: "Gate không có mục marker nào" được hiểu là không có mục marker cho đường dẫn trong `MOI`; mục
   `not_measured`/`khong_co_trong_MOI` cho test không đăng ký là hành vi M4(e) của r2. Nếu bạn đọc khác, ghi thành finding có căn cứ.
7. **Không tự soạn nội dung tấn công nhạy cảm**; hướng nào cần thì MÔ TẢ BẰNG LỜI.
8. Review theo LỚP (V3): khái quát biểu hiện thành lớp, quét mọi biểu hiện cùng lớp trước khi báo.

## Hạng

- **P0**: bằng chứng sai theo hướng có lợi (thiếu/lệch mà ra `passed`, rc 0 khi phải 12/3), hoặc rò credential.
- **P1**: vi phạm M1–M11/A1–A19 đo được; ca/mutant không có răng ở chốt đặc tả đòi.
- **P2**: lỗi thật nhưng hẹp, hoặc ca có mặt mà không đo.
- **P3**: nợ/chất lượng; kèm đề xuất quyết định có căn cứ.

## Đầu ra — `.review/VERDICT.md`

Dòng đầu `verdict: approve` hoặc `verdict: changes_requested`; rồi `reviewed_sha:`, `base_sha:`, `Reviewed commit: <40 hex>`.
Approve CHỈ khi P0 = P1 = P2 = 0 (V2), mỗi P3 có quyết định đề xuất. Bắt buộc: bảng ĐỐI CHIẾU F01–F07; **BẢNG LỚP**
`| lớp | hạng | biểu hiện (tệp:dòng) | phép đo tái hiện | HINT patch | ước lượng dòng |` (slug mới cho nguyên nhân mới; biểu hiện mới
của F01–F07 ghi là LẶP LỚP); đối chiếu A1–A19; danh sách mutant kèm hạng. Không khẳng định thứ chưa đo; không đo được thì ghi
`KHÔNG ĐO ĐƯỢC`. HINT phải kèm ước lượng số dòng (ứng viên ở 1016/1050).
