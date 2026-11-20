# wp1460 r6 — B1a của kế hoạch nguồn r4: biên nhận full audit `bien_nhan_audit.v1` (phần bên tiêu dùng cần) + canary A3 (BIEN-NHAN-AUDIT-V1-A)
packet_id: wp1460
revision: 6
tran_kich_thuoc_sensitive: ADR-0053@8ab100793df9831505f495543a74044b91c2c9ab

Trạng thái: thay r5 (cùng đường dẫn, commit `f18abde3c05e15659a9c8ccfe8aa28e67e36d789`, sha256 `75a1f16459f9dc8e747c486035de4cd04b0fb4e7faec0476b60a244161d5b882`; r4 `9f09a12`, r3 `29c99e7`, r2 `9f7010e`, r1 `d7e89d9`). Năm lượt review spec Codex; lượt 5 (`wp1460-spec-review-5`, trên r5) trả 4 P2 + 1 P3, r6 sửa theo LỚP (bảng "Thay đổi"). Lượt 4 còn hai lớp P2: `v1-not-fully-specified` và `legacy-selector-equivalence-is-impossible`. Quyết định chủ kho E1 (chat 2026-11-20, ghi vào Mission r87): **TÁCH B1**. Nguyên nhân gốc được nhận: đóng băng một hợp đồng rất rộng bằng văn xuôi trước khi có mã. Từ r5, packet là **B1a**: phạm vi hẹp, hợp đồng đóng băng bằng HIỆN VẬT MÁY (schema + fixture), văn xuôi chỉ trỏ tới chúng. Phần còn lại thành packet kế nhiệm B1b (mục "Ngoài phạm vi"). Chưa có lease.

Nguồn: kế hoạch nguồn r4 (`ops/specs/wp1172-source-plan-r4/KE_HOACH_NGUON_R4.md`, nhánh `ops/wp1172-plan-r4`, sha256 `0f287ce4369fbeb7b1939daa8de5db7c27c2a4efdc1a21f2fccdd37dc9d83fbe`; "§…" không ghi nguồn là tới tệp ấy). Thẩm quyền: Mission r85 và các revision kế tiếp ghi quyết định chủ kho 2026-11-20 (r86: nâng trần soạn/review, luật kích thước, bỏ A4 khỏi B1; r87: tách B1, thêm một lượt soạn); r84 Q6 = có. Base lúc soạn: `master` `0f9aa2a2cc697129e1f5be72feddf60986286865`; base thi công đo lại khi cấp lease. Đặc tả chỉ có hiệu lực khi chủ kho duyệt băm của nó và một Mission revision cài nó.

Dòng `tran_kich_thuoc_sensitive` là điều kiện `ADR-0053` đặt ra để trần MẶC ĐỊNH của packet `sensitive` là 6 tệp / 450 dòng thêm (thiếu nó thì 3 tệp / 300 dòng; PR giao nộp có 4 tệp). Nó không xin ngoại lệ. OID đã đo: tệp ADR có ở OID ấy, vắng ở cha thứ nhất, OID trên chuỗi first-parent của `origin/master`.

## Mục tiêu
Mỗi lượt `ci-dot-bien-du.yml` (`full_mutant_audit`, M9 của `ADR-0060`) để lại MỘT biên nhận máy đọc do một job thu cuối cùng ghi; job ấy ĐỎ khi không chứng minh được đủ các điều B2/B3 cần. B1a chỉ mang những gì bên tiêu dùng cần: định danh (kho, id kho, đường dẫn workflow, `github.workflow_sha` hoặc `not_measured`), sự kiện và khung, SHA sự kiện, SHA/tree checkout từng job, `run_id`/attempt và attempt bên sản xuất từng mảnh, kiểm kê job kỳ vọng (lập độc lập) so với thực có, kết luận cuối, id + digest artifact, dấu hiệu dương. Kèm canary concurrency A3 còn nợ từ PR0 (§8.2).

## Hợp đồng

### 1. Hiện vật đóng băng (nguồn DUY NHẤT của hình biên nhận)
| Tệp | sha256 | Vai trò |
|---|---|---|
| `ops/specs/wp1460-r1/hop_dong/bien_nhan_audit.v1.schema.json` | `e65907c890356e59e73b01c1a9d585e11932d51ebfc29731d64341193dc87a82` | JSON Schema draft 2020-12, mọi object `additionalProperties: false`, mọi khoá bắt buộc. Gốc = biên nhận; `$defs/dau_job_v1` = dấu job |
| `ops/specs/wp1460-r1/hop_dong/fixture.json` | `0edcd0c0e69b7757f82c6b58d049fe858171ba90fad091295058f7a718094169` | 5 nền (`xanh`, `khong_xanh`, `dau_job`, `rest`, `ngoai`), 107 ca (sửa theo JSON Pointer; mỗi ca khai `hinh_hop_le` và TẬP luật C bị vi phạm), 10 địa điểm từ vựng |

Nguồn chuẩn tắc thứ ba là khối mã ở mục "Lệnh kiểm" (ghim bằng băm của chính tệp này): hàm `tieu_dung` trong đó là ĐỊNH NGHĨA chạy được của luật C1–C10 cho bên tiêu dùng. Hai tệp do người soạn viết và ĐÃ CHẠY (mục "Số đo"). Văn xuôi dưới đây KHÔNG định nghĩa lại trường nào; chỗ nào văn xuôi lệch schema hoặc lệch hàm `tieu_dung` thì **hiện vật máy thắng** và đó là lỗi của đặc tả. Đổi một byte của hai tệp là đổi hợp đồng ⇒ cần revision đặc tả mới. Executor chép NGUYÊN BYTE hai tệp này vào PR giao nộp (cùng đường dẫn) và không sửa.

Tóm tắt để định hướng (không chuẩn tắc): biên nhận có đúng HAI hình. **Xanh** (`ok: true`): đủ mọi dòng, không trường nào `null` ngoài `ket_luan`/`completed_at` của chính job thu và `workflow_sha` khi `not_measured`. **Không xanh** (`ok: false`): chỉ định danh lấy từ context (kho, workflow, sự kiện, lượt, công cụ, thời điểm) cộng `ly_do` (danh sách chuỗi cho người đọc, không mang nghĩa máy). Hình không xanh có `su_kien` RIÊNG (`su_kien_khong_xanh`): tên sự kiện bất kỳ, và ba trường `cron`, `khung_danh_nghia_utc`, `run_created_at` được `null` khi không biết; hình xanh không dùng định nghĩa ấy và không được nới. Không có hình "xanh thiếu dữ liệu": cái gì không quan sát được thì biên nhận KHÔNG XANH. Chẩn đoán chi tiết vì sao không xanh nằm ở log job và thuộc B1b.

Artifact biên nhận: tên `bien-nhan-audit-<run_id>-<run_attempt>`, đúng một tệp `bien_nhan_audit.json` (UTF-8, LF). Artifact dấu: `dau-job-<run_id>-<run_attempt>-<khoa_job>`, đúng một tệp `dau-job.json`.

### 2. Bất biến
- **I1 — chỉ siết M9.** Giữ nguyên `on` (cron `17 19 * * 6` + `workflow_dispatch` trần), `permissions` mức workflow, `concurrency`, ba job hiện có với `runs-on`, `timeout-minutes`, `env`, `strategy`, mọi bước và lệnh. Ba job ấy chỉ được THÊM đúng hai bước dấu job (mục 3). Không `continue-on-error`; không `if:` nào ở job/bước hiện có. Không đầu vào nào đang đỏ ở PR0 mà thành xanh.
- Job thu là job của workflow ⇒ K7 hiện có ("mọi job `success`") bắt nó; không sửa `packet_loop.py`.
- Không sửa `ops/nhanh_don_duoc_test.py`, bảng đột biến, cách phân hạng, `chon_bien_nhan_du`, `--kiem-bien-nhan-du`, job gom. Tính đúng của TỪNG MỤC đột biến (đúng chế độ, nền, giết, tín dụng giả) vẫn do job mảnh và job gom hiện có quyết định; B1a đòi hai job ấy `success` chứ không tự phán lại.
- Không dựng một kết luận REST hay mốc thời gian mà REST không trả. Không điền `workflow_sha` từ checkout.
- Không hồi tố: lượt trước B1a không có biên nhận.

### 3. Bên sản xuất
- **Dấu job.** Ở MỌI job (ba job cũ và job thu, cùng một luật): đúng hai bước GHIM đứng NGAY SAU bước đo HEAD của PR0 và trước mọi bước khác (kể cả `setup-python`): (a) bước chạy bằng `python3` có sẵn của image, chỉ dùng thư viện chuẩn, thân giống nhau ở mọi job, tham số chỉ vào qua `env:` (thân không chứa biểu thức Actions), ghi `dau-job.json` đúng `$defs/dau_job_v1` với `checkout_sha` = `git rev-parse HEAD`, `checkout_tree` = `git rev-parse HEAD^{tree}`; (b) `actions/upload-artifact@v4` với tên ở mục 1, `if-no-files-found: error`.
- **Job thu `bien-nhan-audit`** (job thứ tư): `needs: [dot-bien-du, dot-bien-manh, dot-bien-gop]`, `if: always()` mức job, `runs-on: ubuntu-latest`, `timeout-minutes: 10`, `permissions` mức job `{contents: read, actions: read}`. Thứ tự bước DUY NHẤT (chốt hình dạng ghim đúng danh sách này): (1) checkout ghim; (2) đo HEAD; (3) dấu job; (4) tải dấu lên; (5) setup-python 3.12; (6) pip ghim như job gom; (7) tải artifact mảnh của run (mẫu `TAI_VE_DU`); (8) tải mọi dấu (`dau-job-<run_id>-*`); (9) bước REST; (10) lệnh thu; (11) tải biên nhận lên, `if-no-files-found: error`. Bước 7–11 mang `if: always()` để một bước tải hỏng vẫn để lại biên nhận không xanh; job vẫn đỏ vì bước hỏng vẫn hỏng. Bước 1–6 hỏng ⇒ không có biên nhận.
- **Bước REST** (`gh api`, token của job) không dừng giữa chừng: mỗi điểm ghi `rest/<tên>.json` hoặc `rest/<tên>.loi`, rồi thoát 0. Điểm: `run`, `jobs` (`filter=all`, phân trang hết), `artifacts` (phân trang hết), `definition` (contents tại `github.workflow_sha`; chỉ gọi khi giá trị ấy là 40 hex).
- **Lệnh thu** = cờ CLI mới `--thu-bien-nhan-audit` trong `.claude/dev/ci_dang_ky_test.py` (cạnh `--kiem-bien-nhan-du`; không tạo `.py` mới). Hàm thuần trên tệp, chạy offline. Ranh giới đầu vào: các giá trị CONTEXT do workflow truyền qua đối số (tên và id kho, `workflow_ref`, tên sự kiện, `github.sha`, `run_id`, `run_attempt`, chuỗi `github.event.schedule` khi có) phải có mặt và đúng dạng (SHA 40 hex, số nguyên dương, `workflow_ref` trỏ đúng tệp workflow này, tên sự kiện khác rỗng); thiếu hoặc sai ⇒ LỖI ĐỐI SỐ, thoát 2, KHÔNG ghi biên nhận. Mọi thứ còn lại (tệp REST, thư mục artifact, nội dung tệp) là đầu vào THU ĐƯỢC: vắng, hỏng hay sai đều cho biên nhận không xanh. Với đối số hợp lệ lệnh thu LUÔN ghi một biên nhận hợp lệ theo schema rồi mới thoát: 0 khi xanh, 1 khi không xanh. `run_created_at` và `khung_danh_nghia_utc` chỉ lấy từ `run.created_at` của REST; không đọc được hoặc sai dạng ⇒ ghi `null` ở biên nhận không xanh; CẤM thay bằng giờ hiện tại, giờ bắt đầu job hay bất kỳ mốc nào khác. Sự kiện ngoài `schedule`/`workflow_dispatch` ⇒ biên nhận không xanh ghi đúng tên sự kiện. Dòng dương duy nhất khi 0: `BIEN_NHAN_AUDIT: ĐẠT job trước a/a · mảnh b/b · sha <H> · run <id>/<attempt> · job thu CHƯA XONG`.
- **Định danh definition.** `workflow_sha` chỉ lấy từ `github.workflow_sha`. Có giá trị và đọc được tệp workflow tại đúng OID ấy qua REST contents ⇒ `measured` (kèm blob và sha256 của byte). Còn lại ⇒ `not_measured` kèm `ly_do` (giữ `workflow_sha` nếu context có). `not_measured` KHÔNG làm biên nhận mất xanh. B1a không gọi, không đọc, không so với A4 (`ops-do-workflow-definition.yml`); A4 là bước của người vận hành do B3 đặc tả.

### 4. Điều kiện XANH của lệnh thu
Biên nhận chỉ `ok: true` khi lệnh thu QUAN SÁT ĐƯỢC và xác nhận ĐỦ mọi điều dưới đây. Không quan sát được (tệp `.loi`, thư mục vắng, tệp hỏng) và quan sát được mà sai đều cho cùng kết quả: KHÔNG XANH, thoát 1. B1a không phân biệt hai trường hợp ấy trong hợp đồng.

- **X1 REST.** Ba điểm `run`, `jobs`, `artifacts` đọc được; `total_count` bằng số phần tử đã đọc; `run.id`, `run.run_attempt`, `run.head_sha`, `run.path`, `run.event`, tên và id kho khớp context.
- **X2 Kiểm kê job độc lập.** Tập kỳ vọng dựng từ CHÍNH tệp workflow tại checkout: job không ma trận ⇒ tên khoá; job có đúng một trục ma trận dạng danh sách ⇒ `<khoá> (<giá trị>)`; hình khác ⇒ không xanh. Tập tên trong `jobs` phải BẰNG tập kỳ vọng; không có hai bản ghi cùng (tên, `run_attempt`). Không ghi cứng số hay tên job.
- **X3 Kết luận.** Với mỗi job kỳ vọng trừ job thu: bản ghi có `run_attempt` lớn nhất có `conclusion == "success"`. Job thu ghi `ket_luan: null`, `completed_at: null`.
- **X4 Dấu.** Mỗi job kỳ vọng (cả job thu) có ĐÚNG MỘT artifact dấu ở attempt của bản ghi REST mới nhất của CHÍNH job ấy (có thể nhỏ hơn attempt của lượt); dấu đúng `dau_job_v1`; `run_id` nhúng = lượt; `run_attempt` nhúng = attempt trong tên; `khoa_job` nhúng = khoá trong tên = khoá kỳ vọng; `su_kien_sha` = `checkout_sha` = `github.sha`; mọi `checkout_tree` bằng nhau.
- **X5 Mảnh.** Số mảnh lấy từ trục ma trận của job mảnh. Mỗi mảnh có đúng một artifact `dot-bien-manh-<run>-<att>-<k>` với `att` = attempt của bản ghi REST mới nhất của job mảnh ấy; trong đó đúng một tệp `manh-<k>.json` đọc được, là object, `head` = `github.sha`. Vắng ở attempt ấy ⇒ không xanh (không lấy bản attempt khác thay).
- **X6 Dòng attempt.** attempt(mảnh) ≤ attempt(`dot-bien-gop`) ≤ `github.run_attempt`; attempt của mọi job ≤ `github.run_attempt`.
- **X7 Artifact.** Mọi artifact được ghi vào biên nhận có `digest` REST dạng `sha256:` + 64 hex; `sha256_noi_dung` do lệnh thu tự băm tệp. Tên artifact của run chỉ thuộc ba họ: mảnh, dấu, và biên nhận của attempt TRƯỚC; tên khác hoặc tên trùng ⇒ không xanh.
- **X8 Sự kiện.** `schedule`: `github.event.schedule` bằng chuỗi cron ghim; khung = mốc cron gần nhất ≤ `run.created_at`. Sự kiện khác `schedule`/`workflow_dispatch` ⇒ không xanh.

### 5. Luật cho bên tiêu dùng (B2, B3)
Schema chỉ kiểm HÌNH. Luật C là phần bên tiêu dùng PHẢI tự kiểm; **định nghĩa chuẩn tắc là hàm `tieu_dung` ở mục "Lệnh kiểm"**, đã chạy trên mọi ca của `fixture.json`. Bên tiêu dùng hiện thực lại theo ngôn ngữ của mình và phải cho CÙNG tập luật vi phạm trên mọi ca (`vi_pham`), cùng `canh_bao`, cùng `moc_tuoi`. Tóm tắt (không chuẩn tắc):
- **Đầu vào độc lập với biên nhận:** REST của run (`run`, `jobs` mọi attempt, `artifacts`); H và tree của H mà bên tiêu dùng đang xét; sha256 của gói và của tệp bên trong do bên tiêu dùng tự băm sau khi tải. Kiểm kê và mẫu số LẬP TỪ REST (bản ghi có `run_attempt` lớn nhất của TỪNG tên job), không lấy từ mảng hay số đếm trong biên nhận.
- **C1.** Biên nhận hợp lệ theo schema, `ok == true`, và `luot.run_attempt` = attempt mới nhất của run (biên nhận của attempt cũ, hoặc biên nhận không xanh ⇒ không đạt; không lùi về attempt cũ).
- **C2.** Run `completed`/`success`; bản ghi mới nhất của MỌI job `success`, kể cả `bien-nhan-audit` (biên nhận ghi trước khi job thu xong nên kết luận của nó CHỈ lấy từ REST).
- **C3.** `kho`, `kho_id`, `workflow.duong_dan`, `luot.run_id`, `su_kien.ten`, `su_kien.sha` khớp REST; `su_kien.sha` = H.
- **C4 (song ánh job).** Đúng MỘT dòng `job[]` cho mỗi tên job của REST, không dòng thừa, không dòng trùng; `kiem_ke_job.ky_vong` = `thuc_co` = danh sách tên REST đã xếp; từng dòng: `job_id` và `run_attempt` = bản ghi REST mới nhất của tên ấy; `khoa` suy từ `ten` (`<a> (<b>)` → `<a>-<b>`); `tu_than` ⇔ `khoa == "bien-nhan-audit"`; tên artifact dấu = `dau-job-<run_id>-<run_attempt của dòng>-<khoa>`. Job không chạy lại giữ attempt cũ của CHÍNH nó là hợp lệ.
- **C5.** Mọi `checkout_sha` và mọi `manh[].head` = `su_kien.sha`; mọi `checkout_tree` = tree của H.
- **C6 (song ánh mảnh).** Tập mảnh kỳ vọng = các job REST tên `dot-bien-manh (<k>)`; đúng một dòng `manh[]` cho mỗi mảnh; `manh` = k; `attempt_ben_san_xuat` = `run_attempt` của dòng job mảnh ấy ≤ của `dot-bien-gop`; tên artifact = `dot-bien-manh-<run_id>-<attempt>-<k>`; mọi `run_attempt` của job ≤ `luot.run_attempt`.
- **C7.** `dau_hieu_duong` = `n/n` với n = số job REST trừ job thu, và `m/m` với m = số mảnh kỳ vọng.
- **C8.** Mọi artifact được nêu (dấu, mảnh) có trong REST với cùng id, tên, `digest`, chưa hết hạn; sha256(gói tải về) = `digest`; sha256(tệp bên trong) = `sha256_noi_dung`.
- **C9 (không phải từ chối).** Mốc tính tuổi = `khung_danh_nghia_utc` khi có, không thì `run_created_at`; ngưỡng do từng bên tiêu dùng đặt. Chạy lại attempt không làm mới.
- **C10 (cảnh báo, không phải từ chối ở mức hợp đồng).** `not_measured` ⇒ biên nhận không chứng minh định danh definition; B2 báo nguyên văn; B3 xử lý bằng A4 theo đặc tả của B3 và có thể chặn theo luật riêng của nó.

Mỗi luật C1–C8 có ít nhất một ca âm mang đúng nhãn luật; C9 có ca khai `moc_tuoi`; C10 có ca khai `canh_bao`; lệnh kiểm tự xác nhận độ phủ 10/10. B1a tự chạy `tieu_dung` trên hai biên nhận canary (mục 7).

**Ánh xạ L1–L13 của B3:** L1 `schema` · L2 `kho`, `kho_id` · L3 `workflow.duong_dan` · L4 `su_kien.ten`, `su_kien.cron`, `su_kien.khung_danh_nghia_utc` · L5 `su_kien.sha`, `job[].checkout_sha`, `job[].checkout_tree` · L6 `luot`, `manh[].attempt_ben_san_xuat` · L7 `kiem_ke_job`, `job[].ten` (đối chiếu song ánh với REST theo C4) · L8 `job[].ket_luan` cho job trước, REST cho job thu (C2) · L9 `dinh_danh_definition` · L10 `job[].dau_job`, `manh[].artifact` · L11 `ok` (B1a không có `ket_cuc`; kết cục A+3 thuộc B1b) · L12 `dau_hieu_duong` · L13 tên artifact và tên tệp ở mục 1.

### 6. Chốt hình dạng (`.claude/dev/ci_dang_ky_test.py`)
`loi_workflow_dot_bien_du` và `loi_ghim_sha_du` mở rộng TƯỜNG MINH, vẫn là danh sách cho phép: đúng bốn job; ba job cũ = hình PR0 cộng đúng hai bước dấu ở đúng vị trí; job thu ghim trọn (needs, `if`, quyền, timeout, từng bước và `if` của nó, tên artifact, mẫu tải, thân bước REST, lệnh thu).

### 7. Canary A3 (trên H CUỐI, trước merge; điều phối gọi theo uỷ quyền của chủ kho)
- **Điều kiện mở:** review mã 0 P0–P2, CI PR xanh trên H, chủ kho đã audit exact-H, H đã đẩy. Mọi thay đổi head sau đó làm A3 và K7 hết hiệu lực; chạy lại trọn mục này trên H mới.
- **A3 (BẮT BUỘC, chặn merge).** Hai `workflow_dispatch` của `ci-dot-bien-du.yml` trên cùng ref có đầu = H, khác `run_id`; lượt hai gọi khi lượt một đã có ít nhất một job `dot-bien-manh` `in_progress`. Đạt ⇔ tồn tại thời điểm cả hai lượt cùng có job mảnh đang chạy (đo bằng `started_at`/`completed_at`); cả hai `success`, 11/11 job `success`, không job nào `cancelled`; HAI biên nhận hợp lệ theo schema, `ok: true`, `su_kien.sha` = H, cùng `kiem_ke_job`, khác `luot.run_id`; cả hai cho tập vi phạm RỖNG khi chạy `tieu_dung` với REST thật của chính lượt ấy (sau khi lượt kết thúc). Lượt một đồng thời là bằng chứng K7.
- **Quan sát push (RIÊNG; không chặn merge).** Một lượt `ci.yml` sự kiện `push` trên `master` có khoảng chạy giao với lúc ít nhất một lượt canary đang chạy; ghi `run_id`, `head_sha`, `created_at`, `run_started_at`, `updated_at`, kết luận, số job có `runner_id` khác 0; rồi đo lại hai lượt canary không có job `cancelled`. Push phải tự nhiên (chủ kho merge một PR sẵn sàng trong cửa sổ); B1a không tạo commit giả, không thêm trigger. Không có push ⇒ ghi `not_run` (nghiệm thu chưa đạt, giữ nguyên tên trong hồ sơ).
- **Đo attempt thật (1 `ci_reruns`; không chặn merge).** Sau lượt hai: chạy lại RIÊNG job `bien-nhan-audit` ⇒ biên nhận attempt 2 `ok: true`, `luot.run_attempt == 2`, mảnh vẫn attempt 1, artifact biên nhận attempt 1 còn nguyên. Lượt rerun đã dùng cho sự cố hạ tầng ⇒ `not_run`.
- **Chi phí CI (ƯỚC LƯỢNG từ nền #1434).** Mỗi lượt: 8 mảnh ≈ 13 282 s (`[B: M1.luot_du_8_manh_success.tong_giay_8_job_manh_moi_luot]`) + job registry ≈ 1 680 s (`[B: M1.theo_job."dot-bien-du | ubuntu-latest".trung_vi]`) + gom ≈ 10 s ⇒ ≈ 14 972 s; hai lượt ≈ 29 944 s ≈ 8,3 giờ job. CHƯA ĐO: thời gian tường, job thu, 11 bước dấu mỗi lượt, xếp hàng khi 22 job chạy cạnh một lượt push. Ca mới chạy trong `gate-registry` của `ci.yml`; executor báo delta thời gian job (§13).
- **Ngân sách:** `full_m9_runs` = 2 cho packet này (quyết định chủ kho, hiệu lực khi Mission revision ghi nó), vừa đủ MỘT canary; cộng 1 `ci_reruns`. H đổi sau canary ⇒ DỪNG và xin nâng trần trước khi gọi thêm.
- Bằng chứng ghi ở comment PR và hồ sơ land của điều phối, không trong PR giao nộp.

## Nghiệm thu
1. **Hợp đồng máy (reviewer kiểm bằng cách CHẠY).** Lưu khối mã ở mục "Lệnh kiểm" ra một tệp ngoài kho rồi chạy `python3 -B <tệp> ops/specs/wp1460-r1/hop_dong` với `jsonschema==4.26.0`: kết quả phải là `FIXTURE: 274/274 phep kiem dung ky vong · hinh 107 · ngu nghia 102 · tu vung 65 · luat duoc phu 10/10` và `TONG: DAT`, mã thoát 0. sha256 hai tệp bằng mục 1, trên nhánh đặc tả và trong PR giao nộp. Bộ test của PR giao nộp chạy cùng ba phép ấy (hình, ngữ nghĩa, từ vựng) trên hai tệp đã chép; đột biến riêng: "đổi kết thúc pattern về `$`", "so tập thay vì song ánh ở C4", "lấy mẫu số từ mảng nhận được ở C7", "bỏ ràng buộc bản ghi REST mới nhất".
2. **Lệnh thu ↔ schema.** Mọi biên nhận lệnh thu ghi ra trong bộ test (xanh và không xanh) hợp lệ theo schema; mọi dấu hợp lệ theo `$defs/dau_job_v1`. Ba ca dương: lượt đầu khoẻ; chạy lại riêng job thu (attempt 2); chạy lại một mảnh (mảnh, gom, thu ở attempt 2) — đều `ok: true`, thoát 0, và `tieu_dung` cho tập vi phạm rỗng khi đưa đúng dữ liệu REST của ca. Bốn ca vòng khép kín cho hình không xanh: `run.loi`; `run.json` thiếu hoặc sai dạng `created_at`; `schedule` không biết khung; sự kiện `push` — mỗi ca ghi biên nhận không xanh hợp lệ với mốc `null` (không mốc bịa). Ca đối số: thiếu `github.sha`, `run_id` không phải số ⇒ thoát 2, không có tệp biên nhận.
3. **Ca âm, MỖI ca làm lệnh thu thoát 1 và ghi biên nhận KHÔNG XANH hợp lệ theo schema:** thiếu / thừa / trùng job (X2) · job trước `failure` / `cancelled` / `timed_out` / `skipped` (X3) · dấu: vắng, trùng, sai `schema`, sai `run_id`, sai attempt, sai `khoa_job`, sai SHA, tree lệch — mỗi ca thử cả trên dấu attempt hiện tại lẫn dấu attempt 1 của job không chạy lại trong lượt attempt 2 (X4) · mảnh: vắng ở attempt mới nhất dù có bản attempt cũ, tệp không đọc được, `head` sai (X5) · gom cũ hơn mảnh (X6) · `digest` vắng, artifact tên lạ, tên trùng (X7) · cron lệch (X8) · REST: `.loi` từng điểm lõi, thiếu trang, `run.head_sha` / kho / id kho lệch (X1). Ca `definition` hỏng ⇒ `not_measured` mà vẫn XANH; không ca nào ra `workflow_sha` bằng SHA checkout khi context vắng.
4. **Trình tự bước thật:** mô phỏng điều kiện `if` trích từ CHÍNH tệp YAML (bước không `if` chỉ chạy khi mọi bước trước thành công): tải artifact hỏng ⇒ lệnh thu và bước tải biên nhận vẫn chạy; job trước đỏ ⇒ job thu vẫn chạy. Thân bước REST chạy thật với `gh` giả GIỮ TRẠNG THÁI.
5. **Hồi quy đường cũ (thay cho mọi lời khai tương đương).** `--kiem-bien-nhan-du` (tức `chon_bien_nhan_du`) cho đầu ra TRÙNG BYTE (stdout, mã thoát, thư mục `--chon-ra`) giữa base và head trên các fixture hiện có của nó, A/B dựng trong MỘT lệnh. Các ca cũ của wp1166/#651/#661 vẫn đạt. Không có yêu cầu nào so tập chọn của lệnh thu với bộ chọn cũ.
6. **Chốt hình dạng:** ca âm cho từng điểm mục 6 (bỏ job thu; bỏ `if: always()` mức job; bỏ `if` của từng bước 7–11; dời cặp bước dấu khỏi vị trí ngay sau đo HEAD (ở job cũ và ở job thu); thêm `if` vào job/bước cũ; bỏ một `needs`; nới quyền; `continue-on-error`; bỏ/đổi chỗ bước dấu; đổi tên artifact; thêm trigger; đổi cron/ma trận/timeout; `merge-multiple`).
7. **Đột biến riêng cho MỖI chốt mới** (từng điều X1–X8, mỗi phép ràng buộc của X4 một đột biến, "lấy mảnh attempt cũ thay", "job thu tự khai `success`", "không xanh mà thoát 0", "ghi biên nhận sai schema", "điền giờ hiện tại vào `run_created_at`", "lỗi đối số mà vẫn ghi biên nhận", "dời cặp bước dấu qua `setup-python`", từng điểm mục 6), chạy trên BẢN SAO tạm, tên tệp riêng, tắt bytecode; phân hạng bằng LỚP NGOẠI LỆ RIÊNG của ca đích, neo tên ca; chết vì lỗi vô can ⇒ tín dụng giả; kèm ca tự kiểm bộ phân hạng. Đòi `n/n` giết thật.
8. **Dương trên H + canary:** mục 7; mỗi phần ghi riêng `đạt` / `not_run`.
9. **Cổng kho:** `actionlint` trên `ci-dot-bien-du.yml` rc 0 với `shellcheck` CÓ MẶT (ghi phiên bản; vắng ⇒ phép đo không tính), delta finding so base = 0; `python .claude/dev/ci_dang_ky_test.py` N/N; Ruff F delta = 0 trên mọi `.py` đổi; numstat trong trần (mục "Kích thước"); CI PR Ubuntu xanh; K7 trên đúng H; đọc lượt push sau merge theo nhãn job.
10. **Đối chiếu §8.2 trong hồ sơ:** A1, A2 (11/11 job, mọi checkout/artifact = H), A3, A4 (`chuyen_B3`), A5 (Windows miễn), A6 (`landed` chỉ `true` khi đủ bốn mốc §10.2.2), §3.5 (biên nhận máy đọc: phần B1a).
11. **Sau merge (M8, không chặn):** lượt `schedule` đầu tiên trên `master` có biên nhận hợp lệ với khung đúng.

## Lệnh kiểm (dùng cho Nghiệm thu 1)
```python
import copy, json, re, sys
import jsonschema
D = sys.argv[1].rstrip("/") + "/"
S = json.load(open(D + "bien_nhan_audit.v1.schema.json", encoding="utf-8"))
F = json.load(open(D + "fixture.json", encoding="utf-8"))
jsonschema.Draft202012Validator.check_schema(S)
V = {"bien_nhan": jsonschema.Draft202012Validator(S),
     "dau_job": jsonschema.Draft202012Validator({"$schema": S["$schema"], "$ref": "#/$defs/dau_job_v1", "$defs": S["$defs"]})}
JOB_THU, TIEN_TO_MANH = "bien-nhan-audit", "dot-bien-manh"

def ap(doc, sua):
    for s in sua or []:
        p = [x.replace("~1", "/").replace("~0", "~") for x in s["duong"].split("/")[1:]]
        o = doc
        for k in p[:-1]:
            o = o[int(k)] if isinstance(o, list) else o[k]
        if isinstance(o, list) and p[-1] == "-":
            o.append(s["gia_tri"])
            continue
        k = int(p[-1]) if isinstance(o, list) else p[-1]
        if s.get("xoa"):
            del o[k]
        else:
            o[k] = s["gia_tri"]
    return doc

def khoa_tu_ten(ten):
    m = re.fullmatch(r"(.+) \((.+)\)", ten)
    return f"{m[1]}-{m[2]}" if m else ten

def tieu_dung(b, rest, ngoai):
    """Luat C cua ben tieu dung. Tra (tap luat vi pham, canh bao, moc tinh tuoi)."""
    if not V["bien_nhan"].is_valid(b) or b["ok"] is not True:
        return {"C1"}, [], None
    vp, run, lu = set(), rest["run"], b["luot"]
    def doi(luat, dk):
        if not dk: vp.add(luat)
    doi("C1", lu["run_attempt"] == run["run_attempt"])
    moi = {}                                   # ten job -> ban ghi REST co run_attempt lon nhat
    cap = [(j["name"], j["run_attempt"]) for j in rest["jobs"]]
    for j in rest["jobs"]:
        if j["name"] not in moi or j["run_attempt"] > moi[j["name"]]["run_attempt"]:
            moi[j["name"]] = j
    doi("C2", run["status"] == "completed" and run["conclusion"] == "success"
        and all(j["conclusion"] == "success" for j in moi.values()))
    doi("C3", b["kho"] == run["repository"]["full_name"] and b["kho_id"] == run["repository"]["id"]
        and b["workflow"]["duong_dan"] == run["path"] and lu["run_id"] == run["id"]
        and b["su_kien"]["ten"] == run["event"] and b["su_kien"]["sha"] == run["head_sha"] == ngoai["h"])
    hang = {r["ten"]: r for r in b["job"]}
    doi("C4", len(cap) == len(set(cap)) and len(b["job"]) == len(hang) == len(moi) and set(hang) == set(moi)
        and b["kiem_ke_job"]["ky_vong"] == b["kiem_ke_job"]["thuc_co"] == sorted(moi)
        and all(r["job_id"] == moi[t]["id"] and r["run_attempt"] == moi[t]["run_attempt"]
                and r["khoa"] == khoa_tu_ten(t) and r["tu_than"] == (r["khoa"] == JOB_THU)
                and r["dau_job"]["ten"] == f"dau-job-{lu['run_id']}-{r['run_attempt']}-{r['khoa']}"
                for t, r in hang.items() if t in moi))
    doi("C5", all(r["checkout_sha"] == b["su_kien"]["sha"] for r in b["job"])
        and all(m["head"] == b["su_kien"]["sha"] for m in b["manh"])
        and {r["checkout_tree"] for r in b["job"]} == {ngoai["tree_h"]})
    ky = {}                                    # khoa job manh -> k, lap tu REST (doc lap voi bien nhan)
    for t in moi:
        m = re.fullmatch(re.escape(TIEN_TO_MANH) + r" \((0|[1-9][0-9]*)\)", t)
        if m: ky[khoa_tu_ten(t)] = int(m[1])
    theo_khoa = {r["khoa"]: r for r in b["job"]}
    gop = theo_khoa.get("dot-bien-gop")
    doi("C6", len(b["manh"]) == len(ky) and {m["khoa_job"] for m in b["manh"]} == set(ky) and gop is not None
        and all(r["run_attempt"] <= lu["run_attempt"] for r in b["job"])
        and all(m["khoa_job"] in ky and m["khoa_job"] in theo_khoa and m["manh"] == ky[m["khoa_job"]]
                and m["attempt_ben_san_xuat"] == theo_khoa[m["khoa_job"]]["run_attempt"] <= gop["run_attempt"]
                and m["artifact"]["ten"] == f"{TIEN_TO_MANH}-{lu['run_id']}-{m['attempt_ben_san_xuat']}-{m['manh']}"
                for m in b["manh"]))
    doi("C7", b["dau_hieu_duong"] == {"job_truoc_success": f"{len(moi) - 1}/{len(moi) - 1}", "manh": f"{len(ky)}/{len(ky)}"})
    kho = {a["id"]: a for a in rest["artifacts"]}
    def khop(a):
        r, t = kho.get(a["id"]), ngoai["tai_ve"].get(str(a["id"]))
        return (r is not None and t is not None and r["name"] == a["ten"] and r["digest"] == a["digest"] and r["expired"] is False
                and a["digest"] == "sha256:" + t["sha256_goi"] and a["sha256_noi_dung"] == t["sha256_tep"])
    doi("C8", len(kho) == len(rest["artifacts"]) and all(khop(a) for a in [r["dau_job"] for r in b["job"]] + [m["artifact"] for m in b["manh"]]))
    canh = ["C10"] if b["dinh_danh_definition"]["trang_thai"] == "not_measured" else []
    return vp, canh, b["su_kien"].get("khung_danh_nghia_utc") or b["su_kien"]["run_created_at"]   # C9

sai, dem, phu = [], {"hinh": 0, "ngu_nghia": 0, "tu_vung": 0}, set()
ten = [c["ten"] for c in F["ca"]]
assert len(ten) == len(set(ten)), "ten ca trung"
for c in F["ca"]:
    doc = ap(copy.deepcopy(F["nen"][c["nen"]]), c.get("sua"))
    la_dau = c["nen"] == "dau_job"
    hop_le = V["dau_job" if la_dau else "bien_nhan"].is_valid(doc)
    dem["hinh"] += 1
    if hop_le != c["hinh_hop_le"]:
        sai.append("HINH " + c["ten"])
    if la_dau:
        continue
    vp, canh, moc = tieu_dung(doc, ap(copy.deepcopy(F["nen"]["rest"]), c.get("sua_rest")), ap(copy.deepcopy(F["nen"]["ngoai"]), c.get("sua_ngoai")))
    ky_vong = ["C1"] if not hop_le else c["vi_pham"]
    dem["ngu_nghia"] += 1
    if sorted(vp) != ky_vong or canh != c.get("canh_bao", []) or ("moc_tuoi" in c and moc != c["moc_tuoi"]):
        sai.append(f"NGU NGHIA {c['ten']}: vi pham {sorted(vp)} canh bao {canh} moc {moc}")
    phu |= set(vp) | set(canh) | ({"C9"} if "moc_tuoi" in c else set())
for t in F["tu_vung"]:                         # moi dia diem co pattern: mau dung hop le; them LF/CRLF/khoang trang/sai do dai thi khong
    bien = [t["mau"] + "\n", t["mau"] + "\r\n", " " + t["mau"], t["mau"] + " "] + t.get("sai_do_dai", [])
    for gt, mong in [(t["mau"], True)] + [(x, False) for x in bien]:
        nen = "dau_job" if t["nen"] == "dau_job" else "bien_nhan"
        dem["tu_vung"] += 1
        if V[nen].is_valid(ap(copy.deepcopy(F["nen"][t["nen"]]), [{"duong": t["duong"], "gia_tri": gt}])) != mong:
            sai.append(f"TU VUNG {t['dia_diem']}: {gt!r}")
can = {f"C{i}" for i in range(1, 11)}
if phu != can:
    sai.append(f"PHU LUAT thieu {sorted(can - phu)}")
n = sum(dem.values())
print(f"FIXTURE: {n - len(sai)}/{n} phep kiem dung ky vong · hinh {dem['hinh']} · ngu nghia {dem['ngu_nghia']} · tu vung {dem['tu_vung']} · luat duoc phu {len(phu & can)}/10")
for x in sai: print("LECH:", x)
print("TONG:", "DAT" if not sai else "DO")
sys.exit(1 if sai else 0)
```

## Write set
- Nhánh `ops/wp1460-r1` (đặc tả, không thuộc PR giao nộp): `ops/specs/wp1460-r1/SPEC.md`, hai tệp `hop_dong/` ở mục 1, `ops/leases/wp1460-*.yaml`.
- PR giao nộp, đúng BỐN tệp: `.github/workflows/ci-dot-bien-du.yml` · `.claude/dev/ci_dang_ky_test.py` · hai tệp `hop_dong/` ở mục 1 (chép nguyên byte từ nhánh đặc tả, executor không soạn và không sửa).

Không tệp thứ năm. Không đặt được lệnh thu trong `ci_dang_ky_test.py` ⇒ DỪNG và báo.

## Kích thước
- Trần là trần MẶC ĐỊNH của lớp `sensitive` theo `ADR-0053`: **≤ 6 tệp và ≤ 450 dòng thêm** theo `git diff --numstat` so base. Lease cấp theo trần ấy. Đặc tả không xin, không ước lượng, không cấp ngoại lệ.
- Đã đo: hai tệp `hop_dong/` chiếm 27 + 132 = 159 dòng thêm (`wc -l` trên chính hai tệp đã ghim băm).
- Executor đo `git diff --numstat <base>...HEAD` trên đúng bốn tệp giao nộp trong lúc thi công và trước MỖI lần xin review; ghi số đo vào PR.
- Theo `ADR-0044`: ứng viên giao nộp vượt trần ⇒ DỪNG TRƯỚC review; không cắt ca, fixture hay đột biến để lọt trần; báo điều phối kèm numstat đã đo và phần việc còn thiếu.
- Khi ấy điều phối xin chủ kho một khối `nang_tran` đúng `ADR-0053` (bốn trường `ai_nang`, `can_cu` có numstat ĐÃ ĐO, `tran_cu`, `tran_moi`); chủ kho duyệt; khối vào một revision đặc tả (chỉ đổi dòng `revision`, đoạn Trạng thái, mục này, bảng Thay đổi) và chép nguyên vào lease. Executor chỉ tiếp tục sau khi lease mang khối ấy.

## Quy trình và quyền
- Lớp review: `sensitive`. Executor: Claude Code (Fable 5.2). Reviewer: Codex service gpt-6-astra, mức suy luận cao nhất, phiên độc lập, chỉ đọc.
- Trần: theo r85 `per_new_packet` cùng các mức chủ kho đã nâng cho packet này ngày 2026-11-20 (soạn spec, review spec, `full_m9_runs` = 2), có hiệu lực khi Mission revision ghi chúng; attempts 3, review mã 3, connector 2, CI PR Ubuntu 3, CI rerun 1, Windows CI 0.
- Trước lease: chủ kho duyệt băm; Mission revision riêng; `ai-dang-giu` trên MỌI ref cho write set; lease `wp1236-a-r9-g1-claude-20261120` (giữ `.claude/dev/ci_dang_ky_test.py` tới `2026-11-22T15:35Z`) đã hết hạn hoặc đã thu hồi hai chiều. B2, PR2, B1b (và B3 nếu đăng ký bộ test) dùng chung tệp ấy nên xếp NỐI TIẾP.
- Chủ kho tự audit exact-H trước LẦN ĐẨY ĐẦU của H; điều phối không ký thay. Merge do chủ kho bấm. Windows: miễn theo quy tắc thường trực.
- Hoàn tác: revert PR về hình PR0; biên nhận đã sinh giữ làm lịch sử.

## Ngoài phạm vi
- **Chuyển sang packet kế nhiệm B1b (chưa mở, cần đặc tả và thẩm quyền riêng):** bảng mã chẩn đoán và việc tính lại kết luận từ biên nhận (`chan_doan`, phân biệt `do` / `khong_ket_luan`); bốn tầng kết cục A+3 và kiểm kê MỤC đột biến (gồm phép so 321 khoá G6); nguồn gốc phụ thuộc (Python/OS/`requirements`/phiên bản công cụ); giây và bộ nhớ (RSS) từng mảnh; đưa biên nhận mảnh ĐỎ tới job thu. B1b phải mở rộng theo cách không làm biên nhận B1a mất hợp lệ, hoặc dùng `schema` mới.
- B2, B3, B4, PR2, PR5; `ci.yml`; `.claude/dev/packet_loop.py`; `ops/nhanh_don_duoc_test.py`; `ops/ci_provenance.py`, `ops-do-workflow-definition.yml` và toàn bộ A4; trigger, cron, ma trận, timeout; mọi giá trị `CHO_PHEP`; kho uỷ quyền do máy kiểm; chế độ chặn của bên tiêu dùng; route production; LIVE.

## Số đo lúc soạn (2026-11-20, `master` `0f9aa2a`)
- Lệnh kiểm (trích từ CHÍNH tệp này rồi chạy), `jsonschema` 4.26.0, trên hai tệp đã ghim: `FIXTURE: 274/274 phep kiem dung ky vong · hinh 107 · ngu nghia 102 · tu vung 65 · luat duoc phu 10/10` / `TONG: DAT`, mã thoát 0. Kỳ vọng `vi_pham` của từng ca do người soạn viết tay trước khi chạy hàm `tieu_dung`.
- REST: run `43990524880` có 10 job `dot-bien-du`, `dot-bien-manh (0)`…`(7)`, `dot-bien-gop`; artifact có trường `digest` dạng `sha256:<64 hex>`.
- CHƯA ĐO: `actionlint`/Ruff nền; giá trị `github.workflow_sha` và `github.repository_id` trên lượt dispatch của nhánh; cách REST liệt kê job qua nhiều attempt (mục 7 đo); hạn mức job đồng thời; thời hạn lưu artifact.

## Thay đổi
**r5 → r6 (review spec lượt 5). Sửa theo LỚP.**

| Lớp | Sửa ở r6 |
|---|---|
| `v1-not-fully-specified` (B1-04; lượt 5: hình không xanh không biểu diễn được mốc không biết và sự kiện lạ) | Hình không xanh có `su_kien_khong_xanh` riêng: tên sự kiện bất kỳ, `cron`/`khung_danh_nghia_utc`/`run_created_at` nullable; hình xanh giữ nguyên và có ca âm chống nới. Mục 3 định ranh giới lỗi đối số (thoát 2, không biên nhận) với đầu vào thu được (luôn có biên nhận), và cấm bịa mốc. Ca: `khong-xanh-run-loi-khong-co-moc`, `khong-xanh-schedule-khong-co-khung`, `khong-xanh-su-kien-push`, `am-xanh-run-created-at-null`, `am-xanh-dung-su-kien-khong-xanh` |
| `consumer-records-not-bound-to-producers` (B1-15) | C4 và C6 thành song ánh với bản ghi REST mới nhất của từng job; kiểm kê và mẫu số C7 lập từ REST; tên artifact ràng với (run, attempt, khoá). Bốn phản ví dụ của reviewer nay là ca âm: `luat-C4-dong-job-trung-sua-dau-hieu`, `luat-C6-manh-trung-thay-manh-khac`, `luat-C6-thieu-manh-sua-dau-hieu`, `luat-C4-dong-attempt-cu`; ca dương giữ attempt cũ hợp lệ: `xanh-chay-lai-job-thu` |
| `frozen-fixture-semantic-oracle-missing` (B1-16) | Lệnh kiểm có hàm `tieu_dung` (oracle chạy được của C1–C10) và chạy nó trên MỌI ca với REST/dữ liệu ngoài riêng của ca; mỗi ca khai TẬP luật vi phạm, so bằng nhau tuyệt đối (đổi nhãn là đỏ); tự kiểm độ phủ 10/10 luật. `xanh-chay-lai-mot-manh` đã nhất quán (tên artifact, job id, REST attempt 2). C9/C10 có kỳ vọng riêng (`moc_tuoi`, `canh_bao`), không biến cảnh báo thành từ chối |
| `collector-stamp-order-conflict` (B1-17) | Một luật vị trí cho mọi job (cặp bước dấu ngay sau đo HEAD, trước `setup-python`) và một danh sách 11 bước duy nhất cho job thu |
| `schema-patterns-accept-trailing-newline` (B1-18, P3) | Mọi pattern kết thúc bằng `(?![\s\S])` thay cho `$`; SHA, digest, mốc thời gian thêm `minLength`/`maxLength`; `kho` và cặp số thành định nghĩa dùng chung. Phần `tu_vung` của fixture: 10 địa điểm × (mẫu đúng, +LF, +CRLF, khoảng trắng đầu, khoảng trắng cuối, sai độ dài) = 65 phép kiểm |
| `legacy-selector-equivalence-is-impossible` (B1-14) | Không đổi so với r5: không còn lời khai tương đương; chỉ hồi quy trùng byte của CLI cũ (Nghiệm thu 5) |

Các lớp của lượt 1–4 đã rời B1a cùng phần hợp đồng chúng nhắm tới (chẩn đoán, A+3, phụ thuộc, A4, kích thước tạm, tương đương bộ chọn cũ); chúng được chuyển phạm vi, không tính là đã vá, và B1b phải xét lại khi mở.

**r4 → r5 (quyết định chủ kho E1: tách B1; review spec lượt 4). Sửa theo LỚP.**

| Lớp / nguồn | Sửa ở r5 |
|---|---|
| `v1-not-fully-specified` (B1-04, lượt 1–4) | Bỏ cách làm đã không hội tụ: không còn hợp đồng viết bằng văn xuôi. Hình biên nhận là hai hiện vật máy ghim băm (mục 1), kiểm bằng lệnh chạy được. Mọi phần từng sinh finding của lớp này bị gỡ khỏi B1a và chuyển B1b: `chan_doan`, bảng mã, bộ kiểm tự khớp, các trường nullable theo từng trạng thái sẵn có, `Manh` chép trường, `Muc`. Bài toán "không quan sát được vs quan sát được mà sai" được loại khỏi hợp đồng bằng cấu trúc: chỉ có hai hình, xanh (đủ, không `null`) và không xanh (định danh + `ly_do`) |
| `legacy-selector-equivalence-is-impossible` (B1-14, lượt 3–4) | Bỏ mọi lời khai tương đương giữa lệnh thu và bộ chọn cũ. Thay bằng hồi quy: CLI cũ không đổi, đầu ra trùng byte trước/sau trên fixture hiện có (Nghiệm thu 5) |
| Phạm vi (E1) | Giữ: định danh, sự kiện/khung, SHA, checkout từng job, attempt, kiểm kê job, kết luận, artifact id + digest, dấu hiệu dương, canary A3. Gỡ: kiểm kê mục, A+3, `phu_thuoc`, bộ nhớ, `--kiem-bien-nhan-audit`, `if: always()` ở bước tải mảnh (I1 nay không còn ngoại lệ nào) |
| Kích thước (r86) | Giữ luật r4; thêm số ĐÃ ĐO của hai tệp hợp đồng (105 dòng); nêu `ADR-0044` cho điểm dừng trước review |

Lịch sử r1–r4 (mười bốn lớp finding, bảng theo từng lượt) nằm ở các commit `d7e89d9`, `9f7010e`, `29c99e7`, `9f09a12` của nhánh này; không chép lại ở đây vì phần lớn nội dung chúng mô tả đã rời B1a.
