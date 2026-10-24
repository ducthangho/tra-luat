# Cross-review OFFLINE — packet #899 `wp899` (CI-PROVENANCE-REST-LOG, P-A), **revision 3**, lượt 2, lớp **sensitive**

Bạn là REVIEWER độc lập (Codex/OpenAI). Executor là Claude. Không kế thừa context executor; không gọi subagent; không đăng
GitHub; không đẩy git; không sửa tệp nào trong cây kho (`git status` phải sạch khi xong). Mọi tệp bạn tạo nằm trong `.review/`.
Bạn không có mạng.

## Đối tượng — định danh bằng BĂM, không bằng tên nhánh

| | |
|---|---|
| reviewed_sha (HEAD) | `7f5a02c9c2ff346484e10c2f5b4e94fcb0468b8b` |
| lượt trước (r3 lượt 1) | `29d641cbd4a38504eb30d87f0fc7eaa82a185f24` = cha của HEAD; verdict `.review-input/r3-luot1/VERDICT.md` (changes_requested: F02 P0 LẶP LỚP, F08 `nguon-workflow-git-khong-duoc-kiem-thu` P1 mới). Toàn bộ thư mục `.review/` của lượt 1 (script, probe, mutant, kết quả) ở `.review-input/r3-luot1/` |
| base | `dc657149941f9db3ab2afc6fb6462ba4827bf18f` |
| điểm xuất phát | `9e5019e` (ba tệp nguyên văn từ ứng viên r2 `19b114867fbcad4c3b580bcbe4367bc78a890773`) |
| đặc tả r3 | `.review-input/wp899-r3.md`, sha256 `dd1a997d1f3682e23bb4b5577264076b7d9a12aeff5d9823f491cdda05e4f36f` (kiểm băm, đọc TRỌN) |
| đặc tả r2 | `.review-input/wp899-r2.md`, sha256 `d858c7c65a38a7f0fadda1cabf839c98ce70a881372d847c8979165925971707` |
| verdict r2 | `.review-input/r2/VERDICT-r2-luot{1..4}.md` |
| write set | `ops/ci_provenance.py` · `ops/ci_provenance_test.py` · `.claude/dev/ci_dang_ky_test.py` |

Delta cần review: `git diff 29d641c HEAD`; toàn bộ: `git diff dc65714 HEAD`.

## Authority — coi là quyết định, KHÔNG phải finding

- Q1–Q8 của đặc tả r3. Trần **≤ 8 tệp / ≤ 1050 dòng thêm** (chủ kho, #899 issuecomment-6383572422); write set lease vẫn 3 tệp.
  Executor khai `git diff --numstat dc65714 HEAD` = 1 + 393 + 656 = **1050** (chạm trần, không còn dư).
- **V5 — ĐÂY LÀ LƯỢT 2 CỦA r3, lời gọi Codex 6/8.** Một lớp — F01–F08 — **lặp ở lượt này ⇒ packet DỪNG HẲN**. Vì vậy phân loại
  phải CHÍNH XÁC theo nguyên nhân, không theo vị trí: biểu hiện mới cùng nguyên nhân với F02/F08 là LẶP LỚP; nguyên nhân khác thì
  slug mới. Đừng nới để cứu packet, cũng đừng gộp một nguyên nhân khác vào F02 cho tiện.

## Executor đã vá gì sau lượt 1

1. **F02** (`tach_buoc`): khối in lại chỉ `hop_le` khi đúng cấu trúc: dòng `36;1m` LIỀN ngay sau header và dòng màu đầu = text header;
   dòng ngay sau khối màu bắt đầu bằng `shell: `; không dòng màu nào sau đó trong nhóm; nhóm đóng bằng `##[endgroup]`. Chỉ khối
   `hop_le` mới được so nguyên văn với `run:` (`do_dau_duong`). **Căn cứ đo được:** trên 37 log job thật của hai run A10
   (`.review-input/log-that/`, kèm `SHA256SUMS`), 226/226 nhóm có dòng màu đúng cả bốn điều kiện, 0 nhóm có màu ngoài khối liền
   header; công cụ cho `hop_le` = 226. Script và kết quả: `.review-input/do_cau_truc.py`, `.review-input/do_cau_truc.out.json` —
   hãy CHẠY LẠI nó, và đo thêm những gì nó không đo.
2. Chặn thêm: workflow có job gọi lại (`uses:` mức job) ⇒ chặn chế độ cho mọi bước (bước thật nằm ở tệp khác).
3. **F08**: ca `c34_git_blob_that` gọi `git_blob` THẬT trên một kho git tạm, đối tượng là **tree** (không commit ⇒ không cần ký),
   HEAD chưa sinh; kiểm byte đúng, thiếu path ⇒ None, không UTF-8 ⇒ None. Đột biến `F08_git_bo_sha` (HEAD thay SHA) và
   `F08_git_luon_vang` phải chết đúng ca.
4. Ca `c35_f02_khoi_khong_tron_ven` (năm biến thể, mỗi biến thể có ứng viên va chạm ở bước khác) + 5 đột biến, mỗi điều kiện cấu
   trúc một đột biến. c25/c26 thêm biến thể khối đúng cấu trúc để đột biến A14/A15/A16 vẫn có răng sau khi thêm lớp cấu trúc.
5. Executor đã chạy lại **đúng các script của bạn ở lượt 1** trên HEAD này: `review_cases.py` sáu ca đều `DAT`, `r4_compare.py`
   tám biến thể va chạm đều Gate `not_measured`. Bạn tự chạy lại từ `.review-input/r3-luot1/` để xác minh, đừng tin lời khai này.
6. Suite tại chỗ: `CA: 35/35 dat` · `DOT BIEN: 74/74 bi giet dung ly do` · `TU KIEM PHAN HANG: DAT (2 dot bien)` · `TONG: DAT`.
7. A10 LIVE chạy lại trên HEAD này: provenance của cả hai run **trùng byte** với lần đo trên `29d641c` (sha256 `87b8be84…06b4`,
   `d2e5247f…6c6a`). Lời khai ở `.review-input/a10/`.

## Giới hạn executor khai sẵn (đánh giá, đừng nhận lời)

- Gốc tin là nội dung tại SHA checkout: workflow/script tại SHA ấy vốn quyết định được output (kể cả tự in một nhóm giả bằng
  lệnh workflow). Công cụ không chống tác giả workflow.
- Bước chạy bên trong **composite action** (`uses:` ở mức bước, `run:` nằm trong `action.yml` của action) — chưa đo nhóm log của
  nó trông thế nào, và công cụ không phân biệt được nếu text trùng một `run:` của workflow. Nếu bạn cho rằng đây là đường F02 thật
  (lệnh KHÔNG chạy mà vẫn thành bằng chứng) hay đường chặn chế độ, phân loại cho đúng nguyên nhân.
- Windows/`pwsh`: không đo; khác định dạng ⇒ không hợp lệ ⇒ `not_measured`.

## Cách làm — BẮT BUỘC

1. `.review/VERDICT.md` pending ngay đầu, cập nhật dần.
2. Kiểm băm spec, HEAD, base, write set, numstat, `git diff --check`.
3. **Đối chiếu F01–F08**: F02 và F08 phải được chứng minh ĐÓNG — chạy lại MỌI phản chứng lượt 1 của bạn và mọi biến thể cùng
   cơ chế mới mà bạn nghĩ ra trên cấu trúc mới; F01/F03–F07 giữ đóng.
4. Chạy ca có sẵn (`python -B ops/ci_provenance_test.py`, `--mot-ca <tên>`); đột biến trên BẢN SAO TẠM (`python -B`,
   `PYTHONDONTWRITEBYTECODE=1`, env `CI_PROVENANCE_MA=<bản sao>`); chỉ tính giết khi ca đích chết bởi `TinHieuChotCa` của ĐÚNG ca.
   Đo lại hai mutant F08 của bạn trên bộ ca mới.
5. **Quét lớp MỚI** do bản vá sinh, gợi ý: ranh giới nhóm (nhóm `##[group]` không phải `Run` lồng bên trong, `##[endgroup]` của nhóm
   con, dòng trống/khoảng trắng trong khối màu, header dài, CRLF, dòng màu rỗng), dòng `shell:` (thứ tự `shell:`/`env:`), cấu trúc trên
   log thật (dùng `log-that/`), `c34` (phụ thuộc `git` trên CI, `check=True`, tree thay commit có đúng hợp đồng `<sha>:<path>`).
6. **Không tự soạn nội dung tấn công nhạy cảm**; hướng nào cần thì MÔ TẢ BẰNG LỜI.
7. Review theo LỚP (V3).

## Hạng

- **P0**: bằng chứng sai theo hướng có lợi (thiếu/lệch mà ra `passed`, rc 0 khi phải 12/3), hoặc rò credential.
- **P1**: vi phạm M1–M11/A1–A19 đo được; ca/mutant không có răng ở chốt đặc tả đòi.
- **P2**: lỗi thật nhưng hẹp, hoặc ca có mặt mà không đo.
- **P3**: nợ/chất lượng; kèm đề xuất quyết định có căn cứ.

## Đầu ra — `.review/VERDICT.md`

Dòng đầu `verdict: approve` hoặc `verdict: changes_requested`; rồi `reviewed_sha:`, `base_sha:`, `Reviewed commit: <40 hex>`.
Approve CHỈ khi P0 = P1 = P2 = 0 (V2), mỗi P3 có quyết định đề xuất. Bắt buộc: bảng ĐỐI CHIẾU F01–F08; **BẢNG LỚP**
`| lớp | hạng | biểu hiện (tệp:dòng) | phép đo tái hiện | HINT patch | ước lượng dòng |`; ghi rõ lớp nào LẶP (⇒ V5) và lớp nào mới;
đối chiếu A1–A19; danh sách mutant kèm hạng. Không khẳng định thứ chưa đo; không đo được thì ghi `KHÔNG ĐO ĐƯỢC`.
