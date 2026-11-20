# wp1448 r2 — PR1 của kế hoạch nguồn r3: quan sát G5, không đổi cổng (QUAN-SAT-G5)
packet_id: wp1448
revision: 2

Trạng thái: thay r1 (`ops/specs/wp1448-r1/SPEC.md`, sha256 `a2e264f07bd552193a07e24a54a009be8105116934387f0f8f746de73befadd7`). Review spec Codex `wp1448-spec-review-1` (gpt-6-astra) trả `changes_requested` 4 P2 + 1 P3; r2 sửa cả năm theo đúng `suggested_fix`: (F1) A/B MANH không thể trùng byte vì MANH nhúng head và băm tệp test; (F2) một mảnh không đủ, phải phủ mọi định danh; (F3) ca dương PR4 ở PR1 phải là lợi ích=1/tồn dư=1; (F4) bao đóng phải vô hiệu khi một bộ đọc thực thi bất kỳ đổi; (F5) thời gian phải có dữ liệu dùng được tối thiểu. Đặc tả Packet #1448, vai PR1 của Mission #1172 theo **kế hoạch nguồn r3** (`ops/specs/wp1172-source-plan-r3/KE_HOACH_NGUON_R3.md`, sha256 `2e9fb13f1ab3f299c2d2dc1e5a6e407ff0aadb8aee1f6ffd00d88fc02b146f89`, cài ở Mission r81). Mọi tham chiếu "§" dưới đây là mục của kế hoạch r3; nơi đặc tả này và kế hoạch khác nhau thì **đặc tả này thắng** cho packet này. Rủi ro: nhạy cảm (đụng tệp test nóng và bộ phân loại CI), nhưng **không đổi quyết định nào của cổng**.

## Mục tiêu
Thay các ƯỚC LƯỢNG của r3 bằng số đo, để PR2–PR8 có căn cứ: (1) thời gian G5 tách theo thành phần; (2) tỷ lệ PR mà bao đóng phụ thuộc bảo thủ cho phép bỏ G5 (bóng, chưa bỏ thật); (3) tần suất luật phân loại cũ ≠ ngữ cảnh so sánh mới (bóng); (4) bộ thu có danh tính lượt và phép quy G4.

## Hợp đồng

### 1. Bất biến (từ §4, cưỡng chế bằng ca test)
- **Không đổi hành vi.** Mọi output mà job khác đọc (`GITHUB_OUTPUT` của `chuan-bi`: `che_do`, `packet_loop`, …; bản ghi phán quyết đột biến của G5; mã thoát mọi job) giữ NGUYÊN từng byte so với base trên cùng đầu vào. Dòng bóng chỉ in ra stdout/log và (tuỳ chọn) `GITHUB_STEP_SUMMARY`; **cấm** ghi vào `GITHUB_OUTPUT` hay tệp mà job khác đọc.
- **I1/I2/I6:** không sửa bảng đột biến, không đổi số ca, không đổi cách phân hạng giết/sống/tín dụng giả; tập tên bảng `M3.bang.*` không lùi.
- **Fail-safe của bóng:** mọi lỗi trong mã bóng (git lỗi, ngoại lệ, đầu vào lạ) chỉ làm dòng bóng in `khong_do_duoc` kèm lý do; KHÔNG làm job đỏ và KHÔNG đổi output thật.

### 2. Thời gian G5 (§PR1 mục 1)
Trong `ops/cong_cu_test.py`, ở chế độ bán kính, ghi cho mỗi mảnh: thời gian tường của bước ở tiến trình cha; với mỗi tiến trình con: mốc bắt đầu/kết thúc và CPU (user+sys); với mỗi đột biến: thời gian dựng cây, thời gian ca ĐÍCH, tổng thời gian các ca KHÁC. In thành các dòng có tiền tố riêng `G5_THOI_GIAN ` (JSON một dòng), tách khỏi dòng `MANH`/`BKCON` mà job gom đọc. Đối chiếu thời gian tường bằng HỢP các khoảng con (không bằng tổng); phần không phân bổ được in riêng. Bộ nhận của job gom và bản ghi phán quyết KHÔNG đọc các dòng này.

### 3. Bóng tập phụ thuộc (§PR1 mục 2, định nghĩa ở §PR3)
`ops/ci_duong_nhanh.py` in thêm một dòng `BONG_CONG_CU: <chay|bo_qua|khong_do_duoc> ly_do=… run=… head=…`. Vị từ `bo_qua` đúng như §PR3 "Thiết kế": sự kiện `pull_request`; `che_do` đang chạy = `day_du`; diff đo được, khác rỗng, đường dẫn sạch; đóng góp merge đã kiểm có ≥ 1 đường dẫn ngoài allowlist hồ sơ; không mục nào của diff (kể cả thêm, xoá, đổi tên, đổi mode, symlink) thuộc **bao đóng bảo thủ** = toàn bộ `ops/` trừ bốn tiền tố hồ sơ, toàn bộ `.claude/dev/`, `scripts/*.py` (mức tên), `.github/`, tệp cấu hình gốc kho (`*.toml`, `*.cfg`, `requirements*.txt`, `.gitattributes`, `.gitignore`), cùng mọi đường dẫn mà rà tĩnh các lời gọi `git` trong `ops/cong_cu_test.py` chỉ ra (liệt kê trong hằng số, có ca kiểm). Bao đóng mang một **dấu vân tay bảo thủ** gồm: tập tên và nội dung (băm) của mọi tệp thuộc các thư mục chứa bộ đọc thực thi của bộ ca G5 — `ops/` (trừ bốn tiền tố hồ sơ), `.claude/dev/`, `.claude/hooks/`, `scripts/` (tên) — tức gồm cả module được import hay nạp bằng `runpy` (ví dụ `.claude/dev/launcher.py` qua t18, `ops/lease_publish_test.py`). Bất kỳ bộ đọc nào đổi hoặc tập thành viên đổi so với dấu vân tay đo lúc dựng bao đóng ⇒ `chay` cho MỌI lượt tới khi bao đóng được dựng lại; vì các thư mục ấy đã nằm trong bao đóng, thay đổi đầu tiên vào chúng cũng tự cho `chay`. Push ⇒ `chay`. Mọi trường hợp khác ⇒ `chay` hoặc `khong_do_duoc` (không bao giờ `bo_qua` theo mặc định).

### 4. Bóng phân loại (§PR1 mục 3, §PR4 "Thiết kế", §3 G5)
In thêm `BONG_PHAN_LOAI: cu=<…> moi=<…|khong_do_duoc> goc_su_kien=<oid> goc_so=<oid|-> dau=<oid> hop=<oid>`. "Mới" dùng ngữ cảnh của §PR4 (cha thứ nhất của `github.sha` khi `github.sha` có đúng hai cha, cha hai = head, và `goc_su_kien` là tổ tiên của cha một; sai một điều kiện hoặc git lỗi ⇒ `khong_do_duoc`) và đi qua CÙNG các phép kiểm raw/mode/diff-check như luật cũ, chỉ trong bóng. Bộ thu tính hai bộ đếm TÁCH RIÊNG: **LỢI ÍCH** (cu ≠ moi) và **SAI SÓT TỒN DƯ** (phân loại đang chạy ≠ oracle `moi` tính lại độc lập từ bốn OID); trước PR4, SAI SÓT TỒN DƯ chỉ ghi làm mốc.

### 5. Bộ thu v2 (§PR1 mục 4, §3 "Mẫu số G4", "G4a", "Phép quy G4b")
Thư mục MỚI `ops/specs/wp1448-r2/do/` (không sửa `ops/specs/wp1434-r3/**`): `thu_thap.py` kế thừa hợp đồng của #1434 (ảnh chụp ngoài kho, `--thu/--tinh/--tu-kiem`, ba trạng thái, ghi có giới hạn, `--tinh` tất định không gọi git), thêm: bản ghi theo (run_id, attempt, sự kiện, head) với chế độ dự định, chế độ thực chạy, lý do bỏ, trạng thái hoàn tất, dấu hiệu dương; đọc các dòng `G5_THOI_GIAN`, `BONG_CONG_CU`, `BONG_PHAN_LOAI` khi có; thêm workflow `packet-loop-dot-bien.yml` và thời gian theo bước của `gate`, `gate-ops`; cài phép quy G4a và G4b đúng bảng mười bước của §3 (mỗi lượt của mẫu số đúng một loại; bước 0–1 ngoài mẫu số).

## Nghiệm thu
1. **Không đổi hành vi (A/B dựng trong MỘT lệnh, base và head):** (a) `GITHUB_OUTPUT` của `ops/ci_duong_nhanh.py` trùng BYTE trên ≥ 12 fixture sự kiện/OID giống hệt nhau cho cả hai vế, phủ pull_request/push/workflow_dispatch, allowlist, ngoài allowlist, diff không đo được. (b) Phán quyết G5: chạy đủ cả 8 mảnh ở cả hai vế; mỗi vế kiểm RIÊNG trường nguồn gốc thật của chính nó (head, `sha256_test` đúng tệp đang chạy — KHÔNG làm giả để khớp); rồi so một **phép chiếu** được định nghĩa hẹp: với mỗi định danh đột biến, tập phán quyết từng ca (giết/sống/tín dụng giả, ca đích, lớp ngoại lệ phân hạng), bỏ các trường nguồn gốc và dòng chẩn đoán mới đã khai (`G5_THOI_GIAN`). Hợp kết quả hai vế phải phủ MỌI định danh đột biến hiện hành (490 tại base `a995f0b`, kiểm từ `_phan_manh`); báo riêng định danh thiếu, trùng, thêm; thiếu bất kỳ phép so bắt buộc nào ⇒ nghiệm thu TRƯỢT. (c) `BKCON` của hai vế trùng trên cùng dữ liệu phán quyết.
2. **Ca hai chiều và ba trạng thái (§4 phép a, c)** cho `BONG_CONG_CU` và `BONG_PHAN_LOAI`, gồm các ca đối kháng của §PR3 điều kiện (3) (tệp mới trong `ops/`, đổi tên/xoá trong bao đóng, đổi mode, symlink, ký tự lạ, diff CHỈ hồ sơ ⇒ không phải bỏ mới, gốc cũ; ca HAI THAY ĐỔI LIÊN TIẾP: lần một sửa `.claude/dev/launcher.py` cho nó đọc một tệp dữ liệu mới ngoài bao đóng, lần hai chỉ sửa tệp dữ liệu ấy ⇒ lần hai vẫn `chay` vì dấu vân tay lệch) và các ca của §PR4 (cha dị dạng một/ba cha, cha hai ≠ head; git lỗi ⇒ `khong_do_duoc`). Ca dương PR4 (master chỉ thêm tệp mã không liên quan sau `base.sha`, PR chỉ hồ sơ): ở PR1, vì phân loại đang chạy vẫn là luật cũ, tích hợp bóng thật phải ra **lợi ích=1 và tồn dư=1**; một fixture bộ thu ghi rõ là MÔ PHỎNG sau PR4 (phân loại đang chạy = `moi`) mới được ra lợi ích=1/tồn dư=0. Không đổi định nghĩa hai bộ đếm.
3. **Đột biến riêng cho mỗi chốt mới (§4 phép b),** phân hạng bằng lớp ngoại lệ riêng của ca: ít nhất "dòng bóng lọt vào `GITHUB_OUTPUT`"; "bỏ điều kiện `che_do=day_du`"; "bỏ một thành phần của bao đóng" (từng thành phần: `ops/`, `.claude/dev/`, `scripts/*.py`, `.github/`, cấu hình gốc); "bỏ vô hiệu hoá theo dấu vân tay"; "thu hẹp dấu vân tay về ba tệp cũ"; "nới allowlist hồ sơ"; "dùng `goc_so` khi cha hai ≠ head"; "đếm lợi ích bằng tồn dư"; "dòng `G5_THOI_GIAN` lọt vào bộ nhận của job gom".
4. **Thời gian G5:** trên một lượt CI thật của H, hợp các khoảng con khớp thời gian tường của bước trong ±10 % ở mỗi mảnh, phần lệch in "không phân bổ"; mỗi đột biến có đủ ba thành phần hoặc `khong_do_duoc` có lý do; trên lượt CI tham chiếu `success`, ≥ 95 % định danh đột biến phải có đủ ba thành phần đo được (báo mẫu số phần thiếu). Lỗi đo không bao giờ làm đổi phán quyết; job xanh KHÔNG đồng nghĩa nghiệm thu phần đo đạt.
5. **Bộ thu v2:** `--tu-kiem` N/N; chạy `--tinh` trên ảnh chụp #1434 tái lập các khoá `[B: …]` của §2 và hai phép khoá của `[DX-2]` (7832 dòng, 8 542 030 s); fixture đủ mười bước G4b, mỗi fixture đúng một loại, bắt buộc có: run 44126854175 (8 mảnh `cancelled`) KHÔNG ra `du_hoan_tat`; ca dương PR4 ra `duong_nhanh_co_bang_chung`; đủ 8 biên nhận + gom `cancelled` (run 44443875641) ra `gom_hong`; chọn bỏ + gom `cancelled` ra `gom_hong`; đột biến trên bản sao cho từng bước G4b đều làm `--tu-kiem` đỏ.
6. **Kiểm kê:** `M3.bang.*` sau ⊇ trước; bảng đột biến của `ops/cong_cu_test.py` và `ops/ci_duong_nhanh_test.py` chỉ THÊM mục cho chốt mới.
7. **Cổng kho:** `python ops/ci_duong_nhanh_test.py` và `python ops/cong_cu_test.py` (chế độ bộ ca) N/N; Ruff F delta = 0 trên mọi tệp `.py` đổi; CI PR xanh; một lượt `ci-dot-bien-du.yml` `success` trên đúng H (K7, §4 phép e); đọc lượt push sau merge theo nhãn job.
8. **Sau merge (ghi ở M8, không chặn merge):** ≥ 14 ngày dữ liệu bóng được thu bằng bộ thu v2 làm đầu vào của PR3/PR4.

## Write set
- `ops/specs/wp1448-r2/SPEC.md` (nhánh `ops/wp1448-r1`, không thuộc PR giao nộp)
- `ops/leases/wp1448-r2-g1-claude.yaml` (nhánh `ops/wp1448-r1`, không thuộc PR giao nộp)
- `ops/cong_cu_test.py`
- `ops/ci_duong_nhanh.py`
- `ops/ci_duong_nhanh_test.py`
- `.github/workflows/ci.yml` (CHỈ nếu cần truyền biến môi trường cho dòng bóng; không đổi `if:`, ma trận hay output)
- `.claude/dev/ci_dang_ky_test.py` (CHỈ nếu chốt hình dạng workflow đòi cập nhật băm vì đổi `ci.yml`)
- `ops/specs/wp1448-r2/do/` (tệp MỚI: bộ thu v2, fixture, kết quả tự kiểm; không `*_test.py`)

## Quy trình và quyền
- Executor: Claude Code (Fable 5.2). Reviewer: Codex service gpt-6-astra, mức suy luận cao nhất, phiên độc lập, chỉ đọc. Trần đề xuất: attempts 3, review mã 3, connector 2, CI PR Ubuntu 3, `ci-dot-bien-du.yml` 1, CI rerun 1.
- Chủ kho duyệt băm đặc tả này trước khi cấp lease và tự audit exact-H trước LẦN ĐẨY ĐẦU của H (đăng trên PR bootstrap); điều phối không ký thay. Merge do chủ kho bấm.
- **Windows:** kế hoạch r3 ghi "một lượt dispatch `windows-only`"; theo quy tắc thường trực "không Windows CI", đặc tả này MIỄN Windows (K6 bằng dòng miễn của chủ kho) trừ khi chủ kho chỉ định khác lúc duyệt.
- Trước khi đẩy H: cập nhật nhánh lên master mới nhất và đo lại làn (bài học #1439); PR này dự kiến `day_du` (đụng mã), nên CI đột biến trên PR là bình thường.
- Ngoài phạm vi: mọi thay đổi quyết định cổng (bật bỏ G5, đổi ngữ cảnh phân loại thật — thuộc PR3/PR4), sửa bảng đột biến, PR2, PR5–PR8, route production, LIVE.
