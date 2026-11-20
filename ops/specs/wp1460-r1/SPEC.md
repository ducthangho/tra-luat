# wp1460 r5 — B1a của kế hoạch nguồn r4: biên nhận full audit `bien_nhan_audit.v1` (phần bên tiêu dùng cần) + canary A3 (BIEN-NHAN-AUDIT-V1-A)
packet_id: wp1460
revision: 5
tran_kich_thuoc_sensitive: ADR-0053@8ab100793df9831505f495543a74044b91c2c9ab

Trạng thái: thay r4 (cùng đường dẫn, commit `9f09a12a53fb0fc032c4496728b49feef09d5c5e`, sha256 `5bdd23707bdf2a0ebd995538fbf794a57e5bcbcf7368701585994167e519562d`; r3 `29c99e7`, r2 `9f7010e`, r1 `d7e89d9`). Bốn lượt review spec Codex; lượt 4 (`wp1460-spec-review-4`) còn hai lớp P2: `v1-not-fully-specified` (lần thứ tư) và `legacy-selector-equivalence-is-impossible` (lần thứ hai). Quyết định chủ kho E1 (chat 2026-11-20, ghi vào Mission r87): **TÁCH B1**. Nguyên nhân gốc được nhận: đóng băng một hợp đồng rất rộng bằng văn xuôi trước khi có mã. r5 là **B1a**: phạm vi hẹp, hợp đồng đóng băng bằng HIỆN VẬT MÁY (schema + fixture), văn xuôi chỉ trỏ tới chúng. Phần còn lại thành packet kế nhiệm B1b (mục "Ngoài phạm vi"). Chưa có lease.

Nguồn: kế hoạch nguồn r4 (`ops/specs/wp1172-source-plan-r4/KE_HOACH_NGUON_R4.md`, nhánh `ops/wp1172-plan-r4`, sha256 `0f287ce4369fbeb7b1939daa8de5db7c27c2a4efdc1a21f2fccdd37dc9d83fbe`; "§…" không ghi nguồn là tới tệp ấy). Thẩm quyền: Mission r85 và các revision kế tiếp ghi quyết định chủ kho 2026-11-20 (r86: nâng trần soạn/review, luật kích thước, bỏ A4 khỏi B1; r87: tách B1, thêm một lượt soạn); r84 Q6 = có. Base lúc soạn: `master` `0f9aa2a2cc697129e1f5be72feddf60986286865`; base thi công đo lại khi cấp lease. Đặc tả chỉ có hiệu lực khi chủ kho duyệt băm của nó và một Mission revision cài nó.

Dòng `tran_kich_thuoc_sensitive` là điều kiện `ADR-0053` đặt ra để trần MẶC ĐỊNH của packet `sensitive` là 6 tệp / 450 dòng thêm (thiếu nó thì 3 tệp / 300 dòng; PR giao nộp có 4 tệp). Nó không xin ngoại lệ. OID đã đo: tệp ADR có ở OID ấy, vắng ở cha thứ nhất, OID trên chuỗi first-parent của `origin/master`.

## Mục tiêu
Mỗi lượt `ci-dot-bien-du.yml` (`full_mutant_audit`, M9 của `ADR-0060`) để lại MỘT biên nhận máy đọc do một job thu cuối cùng ghi; job ấy ĐỎ khi không chứng minh được đủ các điều B2/B3 cần. B1a chỉ mang những gì bên tiêu dùng cần: định danh (kho, id kho, đường dẫn workflow, `github.workflow_sha` hoặc `not_measured`), sự kiện và khung, SHA sự kiện, SHA/tree checkout từng job, `run_id`/attempt và attempt bên sản xuất từng mảnh, kiểm kê job kỳ vọng (lập độc lập) so với thực có, kết luận cuối, id + digest artifact, dấu hiệu dương. Kèm canary concurrency A3 còn nợ từ PR0 (§8.2).

## Hợp đồng

### 1. Hiện vật đóng băng (nguồn DUY NHẤT của hình biên nhận)
| Tệp | sha256 | Vai trò |
|---|---|---|
| `ops/specs/wp1460-r1/hop_dong/bien_nhan_audit.v1.schema.json` | `ca19c7178a331c41304a46ad4ccc65034970e2f347b3cad302af7e132ee9390f` | JSON Schema draft 2020-12, mọi object `additionalProperties: false`, mọi khoá bắt buộc. Gốc = biên nhận; `$defs/dau_job_v1` = dấu job |
| `ops/specs/wp1460-r1/hop_dong/fixture.json` | `38b003e07623056be5b78e19662a9d1263ea5daf36871142979245f77df01cab` | 70 ca: 3 nền (`xanh`, `khong_xanh`, `dau_job`) + danh sách sửa theo JSON Pointer; mỗi ca khai `hinh_hop_le` |

Hai tệp do người soạn viết và ĐÃ CHẠY (mục "Số đo"). Văn xuôi dưới đây KHÔNG định nghĩa lại trường nào; chỗ nào văn xuôi và schema lệch nhau thì **schema thắng** và đó là lỗi của đặc tả. Đổi một byte của hai tệp là đổi hợp đồng ⇒ cần revision đặc tả mới. Executor chép NGUYÊN BYTE hai tệp này vào PR giao nộp (cùng đường dẫn) và không sửa.

Tóm tắt để định hướng (không chuẩn tắc): biên nhận có đúng HAI hình. **Xanh** (`ok: true`): đủ mọi dòng, không trường nào `null` ngoài `ket_luan`/`completed_at` của chính job thu và `workflow_sha` khi `not_measured`. **Không xanh** (`ok: false`): chỉ định danh lấy từ context (kho, workflow, sự kiện, lượt, công cụ, thời điểm) cộng `ly_do` (danh sách chuỗi cho người đọc, không mang nghĩa máy). Không có hình "xanh thiếu dữ liệu": cái gì không quan sát được thì biên nhận KHÔNG XANH. Chẩn đoán chi tiết vì sao không xanh nằm ở log job và thuộc B1b.

Artifact biên nhận: tên `bien-nhan-audit-<run_id>-<run_attempt>`, đúng một tệp `bien_nhan_audit.json` (UTF-8, LF). Artifact dấu: `dau-job-<run_id>-<run_attempt>-<khoa_job>`, đúng một tệp `dau-job.json`.

### 2. Bất biến
- **I1 — chỉ siết M9.** Giữ nguyên `on` (cron `17 19 * * 6` + `workflow_dispatch` trần), `permissions` mức workflow, `concurrency`, ba job hiện có với `runs-on`, `timeout-minutes`, `env`, `strategy`, mọi bước và lệnh. Ba job ấy chỉ được THÊM đúng hai bước dấu job (mục 3). Không `continue-on-error`; không `if:` nào ở job/bước hiện có. Không đầu vào nào đang đỏ ở PR0 mà thành xanh.
- Job thu là job của workflow ⇒ K7 hiện có ("mọi job `success`") bắt nó; không sửa `packet_loop.py`.
- Không sửa `ops/nhanh_don_duoc_test.py`, bảng đột biến, cách phân hạng, `chon_bien_nhan_du`, `--kiem-bien-nhan-du`, job gom. Tính đúng của TỪNG MỤC đột biến (đúng chế độ, nền, giết, tín dụng giả) vẫn do job mảnh và job gom hiện có quyết định; B1a đòi hai job ấy `success` chứ không tự phán lại.
- Không dựng một kết luận REST hay mốc thời gian mà REST không trả. Không điền `workflow_sha` từ checkout.
- Không hồi tố: lượt trước B1a không có biên nhận.

### 3. Bên sản xuất
- **Dấu job.** Mỗi job (cả job thu) thêm đúng hai bước GHIM ngay sau bước đo HEAD của PR0: (a) bước chỉ dùng thư viện chuẩn, thân giống nhau ở mọi job, tham số chỉ vào qua `env:` (thân không chứa biểu thức Actions), ghi `dau-job.json` đúng `$defs/dau_job_v1` với `checkout_sha` = `git rev-parse HEAD`, `checkout_tree` = `git rev-parse HEAD^{tree}`; (b) `actions/upload-artifact@v4` với tên ở mục 1, `if-no-files-found: error`.
- **Job thu `bien-nhan-audit`** (job thứ tư): `needs: [dot-bien-du, dot-bien-manh, dot-bien-gop]`, `if: always()` mức job, `runs-on: ubuntu-latest`, `timeout-minutes: 10`, `permissions` mức job `{contents: read, actions: read}`. Bước: (1) checkout ghim + đo HEAD; (2) setup-python 3.12; (3) pip ghim như job gom; (4) dấu job + tải lên; (5) tải artifact mảnh của run (mẫu `TAI_VE_DU`); (6) tải mọi dấu (`dau-job-<run_id>-*`); (7) bước REST; (8) lệnh thu; (9) tải biên nhận lên, `if-no-files-found: error`. Bước 5–9 mang `if: always()` để một bước tải hỏng vẫn để lại biên nhận không xanh; job vẫn đỏ vì bước hỏng vẫn hỏng. Bước 1–3 hỏng ⇒ không có biên nhận.
- **Bước REST** (`gh api`, token của job) không dừng giữa chừng: mỗi điểm ghi `rest/<tên>.json` hoặc `rest/<tên>.loi`, rồi thoát 0. Điểm: `run`, `jobs` (`filter=all`, phân trang hết), `artifacts` (phân trang hết), `definition` (contents tại `github.workflow_sha`; chỉ gọi khi giá trị ấy là 40 hex).
- **Lệnh thu** = cờ CLI mới `--thu-bien-nhan-audit` trong `.claude/dev/ci_dang_ky_test.py` (cạnh `--kiem-bien-nhan-du`; không tạo `.py` mới). Hàm thuần trên tệp, chạy offline. LUÔN ghi một biên nhận hợp lệ theo schema rồi mới thoát: 0 khi xanh, 1 khi không xanh, 2 khi sai đối số. Dòng dương duy nhất khi 0: `BIEN_NHAN_AUDIT: ĐẠT job trước a/a · mảnh b/b · sha <H> · run <id>/<attempt> · job thu CHƯA XONG`.
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
Schema chỉ kiểm HÌNH. Các luật chéo trường dưới đây schema không biểu diễn được; bên tiêu dùng PHẢI tự kiểm. Mỗi luật có ca `luat-C*` trong `fixture.json` (hợp lệ về hình, phải bị từ chối).
- **C1.** Lấy biên nhận của attempt CAO NHẤT của run; hợp lệ theo schema; `ok == true`. Attempt mới hơn không có biên nhận xanh ⇒ không đạt, không lùi về attempt cũ.
- **C2.** REST: run `completed`/`success`; mọi job của attempt mới nhất `success`, **kể cả `bien-nhan-audit`**. Biên nhận ghi trước khi job thu xong nên kết luận của job thu CHỈ lấy từ REST.
- **C3.** `kho`, `kho_id`, `workflow.duong_dan`, `luot`, `su_kien.sha` khớp REST và khớp H mà bên tiêu dùng đang xét.
- **C4.** `kiem_ke_job.ky_vong` = `kiem_ke_job.thuc_co` = tập `job[].ten` (so tập), và khớp tên job REST.
- **C5.** Mọi `job[].checkout_sha` = mọi `manh[].head` = `su_kien.sha`; mọi `job[].checkout_tree` bằng nhau (B3: bằng tree của H).
- **C6.** `manh[].attempt_ben_san_xuat` = `run_attempt` của job có `khoa` = `manh[].khoa_job`; ≤ `run_attempt` của `dot-bien-gop`; mọi `job[].run_attempt` ≤ `luot.run_attempt`.
- **C7.** `dau_hieu_duong`: hai số của mỗi cặp bằng nhau; `job_truoc_success` = số job không `tu_than`; `manh` = số phần tử `manh`.
- **C8.** Khớp byte: sha256(gói tải qua REST) = `digest`; sha256(tệp bên trong) = `sha256_noi_dung`. Artifact hết hạn ⇒ coi là vắng.
- **C9.** Tuổi bằng chứng tính từ `su_kien.khung_danh_nghia_utc` (schedule) hoặc `su_kien.run_created_at` (dispatch); chạy lại attempt không làm mới.
- **C10.** `dinh_danh_definition.trang_thai == "not_measured"`: biên nhận không chứng minh định danh definition; B2 báo nguyên văn; B3 xử lý bằng A4 theo đặc tả của B3.

**Ánh xạ L1–L13 của B3:** L1 `schema` · L2 `kho`, `kho_id` · L3 `workflow.duong_dan` · L4 `su_kien.ten`, `su_kien.cron`, `su_kien.khung_danh_nghia_utc` · L5 `su_kien.sha`, `job[].checkout_sha`, `job[].checkout_tree` · L6 `luot`, `manh[].attempt_ben_san_xuat` · L7 `kiem_ke_job`, `job[].ten` · L8 `job[].ket_luan` cho job trước, REST cho job thu (C2) · L9 `dinh_danh_definition` · L10 `job[].dau_job`, `manh[].artifact` · L11 `ok` (B1a không có `ket_cuc`; kết cục A+3 thuộc B1b) · L12 `dau_hieu_duong` · L13 tên artifact và tên tệp ở mục 1.

### 6. Chốt hình dạng (`.claude/dev/ci_dang_ky_test.py`)
`loi_workflow_dot_bien_du` và `loi_ghim_sha_du` mở rộng TƯỜNG MINH, vẫn là danh sách cho phép: đúng bốn job; ba job cũ = hình PR0 cộng đúng hai bước dấu ở đúng vị trí; job thu ghim trọn (needs, `if`, quyền, timeout, từng bước và `if` của nó, tên artifact, mẫu tải, thân bước REST, lệnh thu).

### 7. Canary A3 (trên H CUỐI, trước merge; điều phối gọi theo uỷ quyền của chủ kho)
- **Điều kiện mở:** review mã 0 P0–P2, CI PR xanh trên H, chủ kho đã audit exact-H, H đã đẩy. Mọi thay đổi head sau đó làm A3 và K7 hết hiệu lực; chạy lại trọn mục này trên H mới.
- **A3 (BẮT BUỘC, chặn merge).** Hai `workflow_dispatch` của `ci-dot-bien-du.yml` trên cùng ref có đầu = H, khác `run_id`; lượt hai gọi khi lượt một đã có ít nhất một job `dot-bien-manh` `in_progress`. Đạt ⇔ tồn tại thời điểm cả hai lượt cùng có job mảnh đang chạy (đo bằng `started_at`/`completed_at`); cả hai `success`, 11/11 job `success`, không job nào `cancelled`; HAI biên nhận hợp lệ theo schema, `ok: true`, `su_kien.sha` = H, cùng `kiem_ke_job`, khác `luot.run_id`; cả hai qua C1–C8 khi đối chiếu REST. Lượt một đồng thời là bằng chứng K7.
- **Quan sát push (RIÊNG; không chặn merge).** Một lượt `ci.yml` sự kiện `push` trên `master` có khoảng chạy giao với lúc ít nhất một lượt canary đang chạy; ghi `run_id`, `head_sha`, `created_at`, `run_started_at`, `updated_at`, kết luận, số job có `runner_id` khác 0; rồi đo lại hai lượt canary không có job `cancelled`. Push phải tự nhiên (chủ kho merge một PR sẵn sàng trong cửa sổ); B1a không tạo commit giả, không thêm trigger. Không có push ⇒ ghi `not_run` (nghiệm thu chưa đạt, giữ nguyên tên trong hồ sơ).
- **Đo attempt thật (1 `ci_reruns`; không chặn merge).** Sau lượt hai: chạy lại RIÊNG job `bien-nhan-audit` ⇒ biên nhận attempt 2 `ok: true`, `luot.run_attempt == 2`, mảnh vẫn attempt 1, artifact biên nhận attempt 1 còn nguyên. Lượt rerun đã dùng cho sự cố hạ tầng ⇒ `not_run`.
- **Chi phí CI (ƯỚC LƯỢNG từ nền #1434).** Mỗi lượt: 8 mảnh ≈ 13 282 s (`[B: M1.luot_du_8_manh_success.tong_giay_8_job_manh_moi_luot]`) + job registry ≈ 1 680 s (`[B: M1.theo_job."dot-bien-du | ubuntu-latest".trung_vi]`) + gom ≈ 10 s ⇒ ≈ 14 972 s; hai lượt ≈ 29 944 s ≈ 8,3 giờ job. CHƯA ĐO: thời gian tường, job thu, 11 bước dấu mỗi lượt, xếp hàng khi 22 job chạy cạnh một lượt push. Ca mới chạy trong `gate-registry` của `ci.yml`; executor báo delta thời gian job (§13).
- **Ngân sách:** `full_m9_runs` = 2 cho packet này (quyết định chủ kho, hiệu lực khi Mission revision ghi nó), vừa đủ MỘT canary; cộng 1 `ci_reruns`. H đổi sau canary ⇒ DỪNG và xin nâng trần trước khi gọi thêm.
- Bằng chứng ghi ở comment PR và hồ sơ land của điều phối, không trong PR giao nộp.

## Nghiệm thu
1. **Hợp đồng máy (reviewer kiểm bằng cách CHẠY).** Lưu khối mã ở mục "Lệnh kiểm" ra một tệp ngoài kho rồi chạy `python -B <tệp> ops/specs/wp1460-r1/hop_dong` với `jsonschema==4.26.0`: kết quả phải là `FIXTURE: 70/70 ca dung ky vong · hop le 20 · khong hop le 50 · ca luat C 11` và `TONG: DAT`, mã thoát 0. sha256 hai tệp bằng mục 1, trên nhánh đặc tả và trong PR giao nộp.
2. **Lệnh thu ↔ schema.** Mọi biên nhận lệnh thu ghi ra trong bộ test (xanh và không xanh) hợp lệ theo schema; mọi dấu hợp lệ theo `$defs/dau_job_v1`. Ba ca dương: lượt đầu khoẻ; chạy lại riêng job thu (attempt 2); chạy lại một mảnh (mảnh, gom, thu ở attempt 2) — đều `ok: true`, thoát 0, và qua C4–C7.
3. **Ca âm, MỖI ca làm lệnh thu thoát 1 và ghi biên nhận KHÔNG XANH hợp lệ theo schema:** thiếu / thừa / trùng job (X2) · job trước `failure` / `cancelled` / `timed_out` / `skipped` (X3) · dấu: vắng, trùng, sai `schema`, sai `run_id`, sai attempt, sai `khoa_job`, sai SHA, tree lệch — mỗi ca thử cả trên dấu attempt hiện tại lẫn dấu attempt 1 của job không chạy lại trong lượt attempt 2 (X4) · mảnh: vắng ở attempt mới nhất dù có bản attempt cũ, tệp không đọc được, `head` sai (X5) · gom cũ hơn mảnh (X6) · `digest` vắng, artifact tên lạ, tên trùng (X7) · cron lệch (X8) · REST: `.loi` từng điểm lõi, thiếu trang, `run.head_sha` / kho / id kho lệch (X1). Ca `definition` hỏng ⇒ `not_measured` mà vẫn XANH; không ca nào ra `workflow_sha` bằng SHA checkout khi context vắng.
4. **Trình tự bước thật:** mô phỏng điều kiện `if` trích từ CHÍNH tệp YAML (bước không `if` chỉ chạy khi mọi bước trước thành công): tải artifact hỏng ⇒ lệnh thu và bước tải biên nhận vẫn chạy; job trước đỏ ⇒ job thu vẫn chạy. Thân bước REST chạy thật với `gh` giả GIỮ TRẠNG THÁI.
5. **Hồi quy đường cũ (thay cho mọi lời khai tương đương).** `--kiem-bien-nhan-du` (tức `chon_bien_nhan_du`) cho đầu ra TRÙNG BYTE (stdout, mã thoát, thư mục `--chon-ra`) giữa base và head trên các fixture hiện có của nó, A/B dựng trong MỘT lệnh. Các ca cũ của wp1166/#651/#661 vẫn đạt. Không có yêu cầu nào so tập chọn của lệnh thu với bộ chọn cũ.
6. **Chốt hình dạng:** ca âm cho từng điểm mục 6 (bỏ job thu; bỏ `if: always()` mức job; bỏ `if` của từng bước 5–9; thêm `if` vào job/bước cũ; bỏ một `needs`; nới quyền; `continue-on-error`; bỏ/đổi chỗ bước dấu; đổi tên artifact; thêm trigger; đổi cron/ma trận/timeout; `merge-multiple`).
7. **Đột biến riêng cho MỖI chốt mới** (từng điều X1–X8, mỗi phép ràng buộc của X4 một đột biến, "lấy mảnh attempt cũ thay", "job thu tự khai `success`", "không xanh mà thoát 0", "ghi biên nhận sai schema", từng điểm mục 6), chạy trên BẢN SAO tạm, tên tệp riêng, tắt bytecode; phân hạng bằng LỚP NGOẠI LỆ RIÊNG của ca đích, neo tên ca; chết vì lỗi vô can ⇒ tín dụng giả; kèm ca tự kiểm bộ phân hạng. Đòi `n/n` giết thật.
8. **Dương trên H + canary:** mục 7; mỗi phần ghi riêng `đạt` / `not_run`.
9. **Cổng kho:** `actionlint` trên `ci-dot-bien-du.yml` rc 0 với `shellcheck` CÓ MẶT (ghi phiên bản; vắng ⇒ phép đo không tính), delta finding so base = 0; `python .claude/dev/ci_dang_ky_test.py` N/N; Ruff F delta = 0 trên mọi `.py` đổi; numstat trong trần (mục "Kích thước"); CI PR Ubuntu xanh; K7 trên đúng H; đọc lượt push sau merge theo nhãn job.
10. **Đối chiếu §8.2 trong hồ sơ:** A1, A2 (11/11 job, mọi checkout/artifact = H), A3, A4 (`chuyen_B3`), A5 (Windows miễn), A6 (`landed` chỉ `true` khi đủ bốn mốc §10.2.2), §3.5 (biên nhận máy đọc: phần B1a).
11. **Sau merge (M8, không chặn):** lượt `schedule` đầu tiên trên `master` có biên nhận hợp lệ với khung đúng.

## Lệnh kiểm (dùng cho Nghiệm thu 1)
```python
import copy, json, sys
import jsonschema
D = sys.argv[1].rstrip("/") + "/"
S = json.load(open(D + "bien_nhan_audit.v1.schema.json", encoding="utf-8"))
F = json.load(open(D + "fixture.json", encoding="utf-8"))
jsonschema.Draft202012Validator.check_schema(S)
V = {"bien_nhan": jsonschema.Draft202012Validator(S),
     "dau_job": jsonschema.Draft202012Validator({"$schema": S["$schema"], "$ref": "#/$defs/dau_job_v1", "$defs": S["$defs"]})}
def ap(doc, sua):
    for s in sua:
        p = [x.replace("~1", "/").replace("~0", "~") for x in s["duong"].split("/")[1:]]
        o = doc
        for k in p[:-1]:
            o = o[int(k)] if isinstance(o, list) else o[k]
        k = int(p[-1]) if isinstance(o, list) else p[-1]
        if s.get("xoa"):
            del o[k]
        else:
            o[k] = s["gia_tri"]
    return doc
sai, dem = [], {"hop_le": 0, "khong_hop_le": 0, "luat": 0}
for c in F["ca"]:
    doc = ap(copy.deepcopy(F["nen"][c["nen"]]), c["sua"])
    hop_le = V["dau_job" if c["nen"] == "dau_job" else "bien_nhan"].is_valid(doc)
    dem["hop_le" if hop_le else "khong_hop_le"] += 1
    dem["luat"] += "vi_pham_luat" in c
    if hop_le != c["hinh_hop_le"]:
        sai.append(c["ten"])
ten = [c["ten"] for c in F["ca"]]
assert len(ten) == len(set(ten)), "ten ca trung"
print(f"FIXTURE: {len(F['ca']) - len(sai)}/{len(F['ca'])} ca dung ky vong · hop le {dem['hop_le']} · khong hop le {dem['khong_hop_le']} · ca luat C {dem['luat']}")
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
- Đã đo: hai tệp `hop_dong/` chiếm 24 + 81 = 105 dòng thêm (`wc -l` trên chính hai tệp đã ghim băm).
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
- Lệnh kiểm ở trên, `jsonschema` 4.26.0, trên hai tệp đã ghim: `FIXTURE: 70/70 ca dung ky vong · hop le 20 · khong hop le 50 · ca luat C 11` / `TONG: DAT`, mã thoát 0.
- REST: run `43990524880` có 10 job `dot-bien-du`, `dot-bien-manh (0)`…`(7)`, `dot-bien-gop`; artifact có trường `digest` dạng `sha256:<64 hex>`.
- CHƯA ĐO: `actionlint`/Ruff nền; giá trị `github.workflow_sha` và `github.repository_id` trên lượt dispatch của nhánh; cách REST liệt kê job qua nhiều attempt (mục 7 đo); hạn mức job đồng thời; thời hạn lưu artifact.

## Thay đổi
**r4 → r5 (quyết định chủ kho E1: tách B1; review spec lượt 4). Sửa theo LỚP.**

| Lớp / nguồn | Sửa ở r5 |
|---|---|
| `v1-not-fully-specified` (B1-04, lượt 1–4) | Bỏ cách làm đã không hội tụ: không còn hợp đồng viết bằng văn xuôi. Hình biên nhận là hai hiện vật máy ghim băm (mục 1), kiểm bằng lệnh chạy được. Mọi phần từng sinh finding của lớp này bị gỡ khỏi B1a và chuyển B1b: `chan_doan`, bảng mã, bộ kiểm tự khớp, các trường nullable theo từng trạng thái sẵn có, `Manh` chép trường, `Muc`. Bài toán "không quan sát được vs quan sát được mà sai" được loại khỏi hợp đồng bằng cấu trúc: chỉ có hai hình, xanh (đủ, không `null`) và không xanh (định danh + `ly_do`) |
| `legacy-selector-equivalence-is-impossible` (B1-14, lượt 3–4) | Bỏ mọi lời khai tương đương giữa lệnh thu và bộ chọn cũ. Thay bằng hồi quy: CLI cũ không đổi, đầu ra trùng byte trước/sau trên fixture hiện có (Nghiệm thu 5) |
| Phạm vi (E1) | Giữ: định danh, sự kiện/khung, SHA, checkout từng job, attempt, kiểm kê job, kết luận, artifact id + digest, dấu hiệu dương, canary A3. Gỡ: kiểm kê mục, A+3, `phu_thuoc`, bộ nhớ, `--kiem-bien-nhan-audit`, `if: always()` ở bước tải mảnh (I1 nay không còn ngoại lệ nào) |
| Kích thước (r86) | Giữ luật r4; thêm số ĐÃ ĐO của hai tệp hợp đồng (105 dòng); nêu `ADR-0044` cho điểm dừng trước review |

Lịch sử r1–r4 (mười bốn lớp finding, bảng theo từng lượt) nằm ở các commit `d7e89d9`, `9f7010e`, `29c99e7`, `9f09a12` của nhánh này; không chép lại ở đây vì phần lớn nội dung chúng mô tả đã rời B1a.
