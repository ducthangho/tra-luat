# Cross-review OFFLINE — packet #899 `wp899` (CI-PROVENANCE-REST-LOG, P-A), **revision 4**, lượt 1, lớp **sensitive**

Bạn là REVIEWER độc lập (Codex/OpenAI). Executor là Claude. Không kế thừa context executor; không gọi subagent; không đăng
GitHub; không đẩy git; không sửa tệp nào trong cây kho (`git status` phải sạch khi xong). Mọi tệp bạn tạo nằm trong `.review/`.
Bạn không có mạng.

## Đối tượng — định danh bằng BĂM, không bằng tên nhánh

| | |
|---|---|
| reviewed_sha (HEAD) | `ca11a6f…` — đọc OID đầy đủ bằng `git rev-parse HEAD` và ghi nó vào verdict |
| điểm xuất phát | `fe7522e` = cha của HEAD: ba tệp nguyên văn từ ứng viên r3 `7f5a02c9c2ff346484e10c2f5b4e94fcb0468b8b` (hai tệp `ops/` chép nguyên; `.claude/dev/ci_dang_ky_test.py` chỉ áp dòng `MOI` lên bản của base) |
| base | `ba222ffd1615f0d74b59985b9612f725211b62f5` |
| đặc tả r4 | `.review-input/wp899-r4.md`, sha256 `be1e1feabe7c23b832168e36b0cce333043863af505e65c48d5a22d2101cef45` — kiểm băm, đọc TRỌN |
| đặc tả r3 / r2 | `.review-input/wp899-r3.md` (`dd1a997d…f36f`), `.review-input/wp899-r2.md` (`d858c7c6…1707`) — r4 dẫn nguyên văn nhiều mục của chúng (`luat_vong_doi` V1–V4, `dinh_danh_reviewer`, M1–M10, A1–A18, `dinh_nghia`); đọc các mục được dẫn |
| verdict r3 | `.review-input/r3-luot1/`, `.review-input/r3-luot2/` (VERDICT.md + `review-scripts/`). **Đọc lượt 2 trước.** |
| A10 | `.review-input/a10/` (stdout + thư mục `--out` của hai run, đo LIVE trên HEAD này); log đầy đủ 37 job ở `.review-input/log-that/<run>/<job>.log` kèm `SHA256SUMS` (sha256 khớp `log_day_du` của provenance) |
| write set | `ops/ci_provenance.py` · `ops/ci_provenance_test.py` · `.claude/dev/ci_dang_ky_test.py` |

Delta cần review: `git diff fe7522e HEAD`; toàn bộ: `git diff ba222ff HEAD`.

## Authority — coi là quyết định, KHÔNG phải finding

- Q1–Q12 của đặc tả r4 (bảng `quyet_dinh_r4`). Trần **≤ 3 tệp / ≤ 1250 dòng thêm** (`nang_tran`). Executor khai
  `git diff --numstat ba222ff HEAD` = 1 + 444 + 772 = **1217** (còn dư 33). HINT của bạn phải tính tới phần dư này.
- **V5 của r4 — ĐÂY LÀ LƯỢT 1 CỦA r4, lời gọi Codex 1/8** (r4 đếm lại từ 0, Q4). Một lớp — kể cả F01–F08 kế thừa — lặp ở
  **lượt 2** của r4 thì packet DỪNG HẲN. Vì vậy hãy quét RỘNG ngay lượt này: mọi biểu hiện cùng nguyên nhân phải được báo bây
  giờ, không để lượt 2. Phân loại theo NGUYÊN NHÂN, không theo vị trí; đừng nới để cứu packet, đừng gộp nguyên nhân khác vào F02.
- `gioi_han_khai` của r4: gốc tin là nội dung tại SHA checkout đã đo, gồm cả action pin theo tag. Đường nào chứng minh được bằng
  chứng sai mà KHÔNG cần quyền sửa nội dung tại SHA là finding; đường cần quyền ấy là giới hạn khai.

## Executor đã làm gì (đánh giá, đừng nhận lời)

1. **M12 `ghep_buoc`** (`ops/ci_provenance.py`): (d) `ghep_job` — đúng một khoá `k` với tên REST bằng `k`, bằng `name:` nguyên văn
   không `${{`, hoặc dạng `<k|name> (<…>)`; job có `uses:` mức job ⇒ không ghép. (a) số nhóm `##[group]Run` = số bước REST đã chạy,
   VÀ số bước REST ứng với YAML = số bước YAML (hai `if` riêng). (b) tên REST = `ten_du_kien` từng vị trí. (c) giờ header cắt về giây
   ∈ `[started_at, completed_at]` (dạng `YYYY-MM-DDTHH:MM:SSZ`, khác dạng ⇒ hỏng). Hỏng một vế ⇒ `ghep_buoc` `not_measured` kèm vế,
   cả job không marker. Bỏ hẳn `ung_vien` (tìm ứng viên trùng chữ toàn workflow).
2. **M4**: `do_dau_duong` chỉ xét nhóm i qua bước YAML được định danh; bước có `uses:` không sinh marker; khối phải bằng nguyên văn
   `run:` của CHÍNH bước ấy. `chan_buoc` áp chặn chế độ lên đúng bước/job/workflow; `GITHUB_ENV`/`GITHUB_PATH` chỉ xét `run:` đứng
   trước trong cùng job. `tach_buoc` thêm luật nhóm lồng (`##[group]` khác trong vùng nhóm đang mở ⇒ khối không hợp lệ) và `gio`.
3. **M11**: `job()` không khai `steps` ⇒ `chay` sinh `steps[]` MỘT lần bằng `buoc_rest` từ log + workflow đang giữ (cài độc lập với
   `ten_du_kien` của công cụ); ca lệch sửa state ấy. `khong_marker` nay đòi `ghep_buoc` = `passed` (mặc định) để "không marker" đến
   từ chốt chứ không từ ghép hỏng. Ca mới c33 (A19), c36–c43 (A20–A27); c31/c35 đổi fixture theo vị trí; đột biến cho từng vế.
4. Suite tại chỗ: `CA: 43/43 dat` · `DOT BIEN: 87/87 bi giet dung ly do` · `TU KIEM PHAN HANG: DAT (2 dot bien)` · `TONG: DAT`.
5. Hai phản chứng r3 lượt 2 chạy lại trên HEAD: `composite_case.py` ⇒ `DAT` (cả ba biến thể Gate `not_measured`, `ghep_buoc`
   `steps_rest_sai_dang` vì fixture không có `number`); `boundary_case.py` ⇒ rc 3 nhưng VÌ `khong_marker` mới đòi ghép `passed`
   mà fixture ấy có 2 bước YAML / 1 nhóm (ghép hỏng vế a, không marker). Phiên bản có ghép `passed` của nó là c40. Hãy tự chạy lại
   và tự dựng biến thể có `steps[]` khớp (dùng `buoc_rest`/`g1` của test) cho CẢ HAI cơ chế.
6. A10 LIVE (HEAD này): run 39342960764 rc 0, provenance sha256 `5ad9afea…afe0`; run 40074551995 rc 0, `24ffa770…185b`; ghép
   13/14 và 22/23 (`chuan-bi` `sha_checkout_chua_do`); 8 job `gate-nhanh-manh` marker `che_do_khong_xac_dinh`; 0 `failed`.
7. A9 (`ci_dang_ky_test.py --chay`): executor chạy riêng; kết quả không nằm trong lượt này.

## Đường executor tự liệt kê (đo từng cái, và tìm cái executor chưa nghĩ tới)

- Nhóm giả in từ output của một bước, cùng giây với bước kế (vế c không phân biệt được) — executor tin vế (a) chặn; kiểm.
- Bước chạy dưới một giây; nhiều bước chung một giây; giờ header thiếu; giờ REST có phần thập phân hoặc offset.
- Bước tên `Post …`/`Set up job` do người viết đặt; `name:` không phải chuỗi; `run:` bắt đầu bằng dòng trống; `name:` chứa `${{`
  ở job KHÁC; hai job REST cùng ghép một job YAML (matrix).
- `steps[]` REST trùng/thiếu `number`, sắp xếp lệch thứ tự log; bước `skipped` nằm giữa; `continue-on-error`.
- Composite: bước `uses:` có nhóm con; job gọi lại.
- Luật nhóm lồng: `##[group]` không phải `Run` TRƯỚC `shell:`; `##[endgroup]` con; nhóm con ở PHẦN OUTPUT (sau `##[endgroup]` cha).

## Cách làm — BẮT BUỘC

1. `.review/VERDICT.md` pending ngay đầu, cập nhật dần.
2. Kiểm băm spec, HEAD, base, write set, numstat, `git diff --check`.
3. **Đối chiếu F01–F08**: F02 phải được chứng minh ĐÓNG bằng phản chứng chạy được (chạy lại mọi script phản chứng của r3 lượt 1 và
   2, và biến thể cùng cơ chế trên cấu trúc mới); F01, F03–F08 giữ đóng.
4. Chạy ca có sẵn (`python -B ops/ci_provenance_test.py`, `--mot-ca <tên>`); đột biến trên BẢN SAO TẠM (`python -B`,
   `PYTHONDONTWRITEBYTECODE=1`, env `CI_PROVENANCE_MA=<bản sao>`); chỉ tính giết khi ca đích chết bởi `TinHieuChotCa` của ĐÚNG ca.
   Tự đột biến thêm bản vá (bỏ từng vế a/b/c/d, đổi thứ tự, nới regex giờ…) và báo mutant nào SỐNG.
5. **Đo lại căn cứ Q1 trên log thật** (`.review-input/log-that/` + `jobs.json` trong `a10/out-*/` + `ci.yml` tại `b27fe85`/`dc65714`
   qua `git show`): job ghép, số đếm ba mức, tên, giờ — cho cả 37 job; so với bảng của đặc tả và với output công cụ.
6. A1–A27: đối chiếu từng tiêu chí với ca/mutant; ca nào CÓ MẶT mà không ĐO (return sớm, khẳng định yếu, thành công vì ghép hỏng
   thay vì vì chốt) là finding.
7. **Không tự soạn nội dung tấn công nhạy cảm**; hướng nào cần thì MÔ TẢ BẰNG LỜI. Mọi phản chứng cần thiết đã có sẵn trong cây
   hoặc dựng được từ helper của test.
8. Review theo LỚP (V3).

## Hạng

- **P0**: bằng chứng sai theo hướng có lợi (thiếu/lệch mà ra `passed`, rc 0 khi phải 12/3), hoặc rò credential.
- **P1**: vi phạm M1–M12/A1–A27 đo được; ca/mutant không có răng ở chốt đặc tả đòi.
- **P2**: lỗi thật nhưng hẹp, hoặc ca có mặt mà không đo.
- **P3**: nợ/chất lượng; kèm đề xuất quyết định có căn cứ.

## Đầu ra — `.review/VERDICT.md`

Dòng đầu `verdict: approve` hoặc `verdict: changes_requested`; rồi `reviewed_sha:`, `base_sha:`, `Reviewed commit: <40 hex>`.
Approve CHỈ khi P0 = P1 = P2 = 0 (V2), mỗi P3 có quyết định đề xuất. Bắt buộc: bảng ĐỐI CHIẾU F01–F08; **BẢNG LỚP**
`| lớp | hạng | biểu hiện (tệp:dòng) | phép đo tái hiện | HINT patch | ước lượng dòng |` (HINT phải chỉ CHỖ và CÁCH rẻ nhất trong 33
dòng dư; ước lượng dòng ròng); ghi rõ lớp nào thuộc F01–F08 (⇒ lặp ở lượt 2 sẽ chạm V5) và lớp nào mới; đối chiếu A1–A27;
danh sách mutant kèm hạng; kết quả đo lại căn cứ Q1. Không khẳng định thứ chưa đo; không đo được thì ghi `KHÔNG ĐO ĐƯỢC`.
