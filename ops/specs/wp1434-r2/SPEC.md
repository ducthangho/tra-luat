# wp1434 r2 — Đo nền mutation testing, chỉ đọc (DO-NEN-DOT-BIEN)
packet_id: wp1434
revision: 2

Trạng thái: đặc tả cho Packet #1434 thuộc Mission #1172. Thay r1 (`ops/specs/wp1434-r1/SPEC.md`, sha256 `88c49734c051ae16135cfae6d9464c7ee19eefa6ec5b557ff74fd10cedcb39bf`). Lượt review spec Codex `wp1434-spec-review-1` trả `changes_requested` với 4 P2 + 1 P3; r2 sửa cả năm: (F1) bố cục đầu ra kích hoạt CI đột biến và bị bộ đăng ký test từ chối; (F2) phép so chạy lại không khả thi với cửa sổ trượt và nguồn hết hạn; (F3) chưa định nghĩa cách tính các lượt chạy lại (attempt); (F4) thiếu thời gian theo bộ test và chế độ nhẹ/đủ có sẵn trong log; (F5, P3) phân biệt số 0 đo được với dữ liệu thiếu.

Packet chỉ đo: không sửa workflow, test, runtime hay chú thích đang lệch; không tạo lượt CI đột biến mới. Kết quả là đầu vào cho **kế hoạch nguồn r3**, bản thay thế cho kế hoạch nguồn r2 (sha256 `f4611b0f0c79f33d56b293f5fcb854eeeae2fcbb6acbdfd59d6134dcbfbdcb8f`) không còn tìm được. Packet KHÔNG soạn r3 và KHÔNG đề xuất tối ưu.

## Vấn đề

Mission #1172 cam kết tối ưu mutation testing PR0–PR8, nhưng mục tiêu và acceptance chi tiết của PR1–PR8 nằm trong kế hoạch r2 đã mất. Viết lại kế hoạch mà không có số nền thì PR1–PR8 không có tiêu chí kiểm được. Số trong kho đã có dấu hiệu trôi: `.github/workflows/ci-dot-bien-du.yml:11` ghi "~73 800 s nối tiếp ⇒ 8 mảnh ≈ 2,6 h/mảnh", còn lượt 43990524880 (17/11/2026) có tám job `dot-bien-manh` chạy 1531–1730 s (25m31s–28m50s; đo ở review spec r1).

## Hợp đồng

### 1. Nguồn và hành động được phép (chỉ đọc)
- GitHub REST GET trên `ducthangho/tra-luat`: `actions/workflows/<tệp>/runs`, `actions/runs/<id>`, `actions/runs/<id>/attempts/<n>`, `actions/runs/<id>/jobs?filter=all`, `actions/runs/<id>/artifacts`, tải artifact còn hạn, và **tải log job** (`actions/jobs/<id>/logs`).
- Đọc tệp trong cây `origin/master` ở SHA ghi trong `meta`; import module để đọc bảng hằng (không gọi hàm chạy ca, không chạy đột biến); `git log/show/rev-parse`; `rg`.
- Cấm: `workflow_dispatch`, rerun, chạy bất kỳ bộ test hay bộ đột biến nào (`ops/nhanh_don_duoc_test.py`, `.claude/dev/ci_dang_ky_test.py --chay`, …), mọi lệnh GHI GitHub ngoài push nhánh packet và mở PR.

### 2. Cohort đóng băng (sửa F2)
- Một lần thu (`--thu`) định nghĩa **cohort**: khoảng UTC đóng `[T0, T1]` ghi cứng trong `meta` (T1 = thời điểm bắt đầu thu, T0 = T1 − 30 ngày), SHA master lúc thu, và danh sách cố định các cặp `(run_id, run_attempt)` thuộc hai workflow (`ci-dot-bien-du.yml`: mọi lượt API còn trả có `created_at ≤ T1`; `ci.yml`: sự kiện `push` lên master và `pull_request`, `created_at ∈ [T0, T1]`), chỉ lấy lượt đã `completed` lúc thu.
- Mọi phản hồi thô (JSON API, log, artifact) ghi vào thư mục **ảnh chụp** ngoài kho, kèm `MANIFEST.json` (đường dẫn, sha256, kích thước, URL không kèm chữ ký/token). Ảnh chụp KHÔNG commit. Kho chỉ commit `COHORT.json` (cohort + sha256 từng tệp thô + sha256 của `MANIFEST.json`).
- Tính toán là bước riêng, thuần offline: `--tinh --anh-chup <thư mục>` đọc DUY NHẤT ảnh chụp và cây kho ở SHA trong `meta`, sinh `BASELINE.json` và `BAO_CAO.md`. **Kiểm chạy lại** = chạy `--tinh` trên cùng ảnh chụp ra `BASELINE.json` **trùng từng byte**. Thu lại live (nếu reviewer làm) chỉ để đối chiếu phép chiếu bất biến của các cặp trong cohort còn nguồn; nguồn hết hạn sau lần thu được ghi `het_han_sau_thu`, không làm đổi số đã đo.

### 3. Tính lượt chạy và attempt (sửa F3)
- Lấy job của MỌI attempt (`filter=all` và/hoặc `attempts/<n>/jobs`). Mỗi dòng job gắn `(run_id, run_attempt, job_id)`.
- Phân loại mỗi dòng: `thuc_thi` (job chạy thật trong attempt ấy) hoặc `mang_sang` (kết quả mang từ attempt trước: `started_at` sớm hơn `created_at` của attempt chứa nó, hoặc cùng `job_id` đã xuất hiện ở attempt trước). Quy tắc phân loại ghi trong `BAO_CAO.md` và có ca tự kiểm.
- Báo **ba con số tách biệt**: giây thực thi (tổng `thuc_thi`, gồm cả attempt hỏng/huỷ), thời gian đầu-cuối của lượt (attempt đầu `created_at` → attempt cuối `completed_at`), và thời gian chờ (`created_at → started_at`). Đếm số lượt có rerun và số job hỏng ở attempt trước; KHÔNG gọi là flaky.

### 4. Phép đo bắt buộc
- **M1 — full audit** (`ci-dot-bien-du.yml`), theo §3: từng job (`dot-bien-du`, `dot-bien-manh (0..7)`, `dot-bien-gop`) và từng bước của job mảnh; runner label; số liệu trong artifact mảnh còn hạn (số mục, rc, mọi trường thời gian có sẵn); từ log job mảnh: thời gian từng ca/mutant có ghi trong dòng kết quả (vd. dòng `KET QUA … <giây>`).
- **M2 — gate CI** (`ci.yml`), theo §3: thời lượng mỗi lượt; mỗi job nhóm `gate*`; từng bước của `gate-cong-cu*`, `gate-nhanh-*`, `gate-registry`, `gate-packet-loop*`. Tách theo nền (nhãn job) và theo làn (`duong_nhanh`/`day_du`, đọc từ log bước phân loại khi có). Lượt huỷ/đỏ vẫn ghi, có cờ.
- **M2b — thời gian theo bộ test và chế độ** (sửa F4): từ log `gate-registry` và `dot-bien-du`, trích mọi bản ghi thời gian theo bộ mà registry in (`CI_DANG_KY_THOI_GIAN`; trường bộ, giây, rc, chế độ `day_du|nhe` theo `.claude/dev/ci_dang_ky_test.py` ~1333–1336 và ~2982). Báo theo từng bộ: số lượt, trung vị/p90 giây, phân bố chế độ.
- **M3 — kiểm kê tĩnh:** các bộ test có đột biến theo bảng đăng ký (`DANG_KY`, `MOI`, `NHE` trong `.claude/dev/ci_dang_ky_test.py`; `CA`, `TU_KIEM`, `DOT_BIEN`, `DOT_BIEN_TU_KIEM` trong `ops/nhanh_don_duoc_test.py`; bảng tương ứng của các bộ khác khi đọc được bằng import). Số nào chỉ sinh khi chạy hàm thì ghi `khong_do_duoc` + lý do, không chạy để lấy.
- **M4 — đối chiếu lời khai:** mọi con số thời gian/số lượng về đột biến đang ghi trong chú thích workflow, `CLAUDE.md`, `docs/`, `ops/specs/wp1166*` (lệnh `rg` ghi lại), mỗi lời khai kèm số đo tương ứng và kết luận `khop | lech | khong_do_duoc`.
- **Độ phủ:** với mỗi loại nguồn (job, log, artifact), báo số yêu cầu / số có / số hết hạn / số cắt cụt / số lỗi.

### 5. Ba trạng thái và số 0 (sửa F5)
- `do_duoc`: có dữ liệu hợp lệ; **0 đo được là `do_duoc` với giá trị 0** (vd. bước có `started_at == completed_at` ở độ phân giải API).
- `khong_ap_dung`: phép đo không tồn tại cho đối tượng ấy (bước `skipped`, job không có trong attempt, bộ không có đột biến).
- `khong_do_duoc` kèm `ly_do`: thiếu dấu thời gian, thời gian đảo (`completed < started`), log/artifact hết hạn, cắt cụt hoặc lỗi API. Không thay dữ liệu thiếu bằng 0 hay ước lượng; không kẹp giá trị âm về 0.
- Mọi giá trị dẫn xuất (tổng, trung vị, p90) ghi công thức và tập đầu vào; chỉ tính trên phần `do_duoc`, và ghi số phần bị loại.

### 6. Bố cục giao nộp (sửa F1)
Mọi tệp packet nằm dưới `ops/specs/wp1434-r2/do/`, là tệp **MỚI** (diff `A`), mode `100644`, sâu hơn một cấp dưới `ops/specs/`, không có tệp nào khớp `*_test.py`. Như vậy PR khớp allowlist `ops/{land,leases,reviews,specs}/**` của `ops/ci_duong_nhanh.py` (đi làn nhanh, không chạy đột biến) và không sinh vị trí test lạ cho `.claude/dev/ci_dang_ky_test.py::tim`. Ca tự kiểm là chế độ `--tu-kiem` của chính `thu_thap.py`, đọc fixture JSON/log trong `fixtures/`, không mạng. Trước khi đẩy, executor chạy cả hai bộ phân loại trên tập đường dẫn của PR và ghi kết quả vào `BAO_CAO.md`: `phan_loai_tu_diff` + `ly_do_ve_day_du` ⇒ `duong_nhanh`, lý do rỗng; `tim()` ⇒ không vị trí lạ. Làn của PR được đo lại trên log CI thật trước merge.

### 7. Đầu ra
- `ops/specs/wp1434-r2/do/thu_thap.py`: ba chế độ `--thu --ra <ảnh chụp>`, `--tinh --anh-chup <ảnh chụp> --ra <thư mục>`, `--tu-kiem`. Không ghi ngoài thư mục chỉ định; không nối vào CI hay registry; không in hay lưu token, header xác thực hay URL tải có chữ ký.
- `ops/specs/wp1434-r2/do/fixtures/…`: fixture tối thiểu cho `--tu-kiem`, gồm ít nhất: 0 đo được; thiếu `started_at`; thời gian đảo; bước `skipped`; biên cohort (lượt ở sát T0 và sát T1); lượt hai attempt có job hỏng ở attempt 1 và dòng `mang_sang` ở attempt 2 (hình dạng như lượt 44522844747); artifact hết hạn; log còn, log cắt cụt, log thiếu cho bộ trích `CI_DANG_KY_THOI_GIAN` và dòng `KET QUA`. Fixture là dữ liệu tổng hợp hoặc trích đã lọc, không chứa token hay URL có chữ ký.
- `ops/specs/wp1434-r2/do/COHORT.json`, `ops/specs/wp1434-r2/do/BASELINE.json`: mỗi giá trị có `trang_thai`, `nguon` (URL API không chữ ký, `tệp:dòng@SHA`, hoặc lệnh) và `ly_do` khi không `do_duoc`; khối `meta` như §2.
- `ops/specs/wp1434-r2/do/BAO_CAO.md`: tối đa ~250 dòng — bảng tổng hợp M1–M4 và độ phủ; 5 điểm tốn thời gian nhất theo giây thực thi (kèm nguồn); mục **"Không đo được"**; mục **"Lời khai lệch"**; quy tắc §3; kết quả hai bộ phân loại §6. Không có mục khuyến nghị tối ưu.

### 8. Kiểm của reviewer
Reviewer (Codex, phiên độc lập, chỉ đọc) nhận đường dẫn ảnh chụp và: chạy `--tu-kiem` (rc0, N/N); chạy `--tinh` trên ảnh chụp, so byte với `BASELINE.json` đã commit; kiểm sha256 ảnh chụp với `COHORT.json`; đột biến trên BẢN SAO `thu_thap.py` (ít nhất: bỏ phân loại `mang_sang`; kẹp số âm về 0; coi 0 là thiếu; bỏ lọc biên cohort; bỏ trích `CI_DANG_KY_THOI_GIAN`) và xác nhận mỗi đột biến làm `--tu-kiem` đỏ đúng ca; đối chiếu ngẫu nhiên ít nhất 10 con số trong `BASELINE.json` với API live; soát tệp commit không chứa token/URL có chữ ký.

## Write set
- `ops/specs/wp1434-r2/SPEC.md` (nhánh `ops/wp1434-r1`, không thuộc PR giao nộp)
- `ops/leases/wp1434-r2-g1-claude.yaml` (nhánh `ops/wp1434-r1`, không thuộc PR giao nộp)
- `ops/specs/wp1434-r2/do/thu_thap.py`
- `ops/specs/wp1434-r2/do/fixtures/` (chỉ tệp `.json`, `.txt`, `.log`)
- `ops/specs/wp1434-r2/do/COHORT.json`
- `ops/specs/wp1434-r2/do/BASELINE.json`
- `ops/specs/wp1434-r2/do/BAO_CAO.md`

## Quy trình và quyền
- Executor: Claude Code (Fable 5.2). Reviewer: Codex service (gpt-6-astra, mức suy luận cao nhất), phiên độc lập, chỉ đọc. Trần: attempts 2, review 2, lời gọi Codex review mã 2; thêm 1 lời gọi review spec cho r2 (cần Mission r73).
- Chủ kho duyệt băm đặc tả này và Mission r73 trước khi cấp lease, và audit exact-H trước merge vì kết quả là căn cứ của kế hoạch r3. Điều phối không ký thay. Merge do chủ kho bấm. Không Windows CI, không full M9 mới.
- Ngoài phạm vi: soạn kế hoạch nguồn r3, đề xuất hay thử tối ưu, sửa workflow/test/chú thích đang lệch (chỉ ghi vào "Lời khai lệch"), PR1–PR8, installation, LIVE.
