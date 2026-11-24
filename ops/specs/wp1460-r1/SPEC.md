# wp1460 r9 — B1a của kế hoạch nguồn r4: biên nhận full audit `bien_nhan_audit.v1` (phần bên tiêu dùng cần) + canary A3 (BIEN-NHAN-AUDIT-V1-A)
packet_id: wp1460
revision: 9
tran_kich_thuoc_sensitive: ADR-0053@8ab100793df9831505f495543a74044b91c2c9ab
tran_loi_goi_codex: ADR-0055@d2e3052d479d140b7e7b91df41ec4914fab7d544

Trạng thái: thay r8 (cùng đường dẫn, commit `d26c8ae8d27a0bddd71bbd08a5153bb47b879130`, sha256 `33d433b018d6eb74048fe27f2cc517b01276a28b76edbe50ffea387a0614dd0c`; lease `wp1460-r8-g2-claude`). r9 CHỈ thêm khối `nang_tran` thứ hai (`ADR-0053`) sau review mã Codex lượt 2/3 (run `6e53f3d5`, trên `1c31f5a88ba125af708a9609085c0edd2f8dc3ee`, còn 1 P2 F02-R2); chỉ đổi dòng `revision`, đoạn Trạng thái, mục "Kích thước" và bảng "Thay đổi". Đoạn trạng thái của r8, giữ làm lịch sử: thay r7 (cùng đường dẫn, commit `d1b08c219227d4b8925702029cd20d4e0febed54`, sha256 `d53341fb8d549d89f99e4cda0bd6ed380bf9975ce47b95a43ad1adaf5b3963b3`, review spec lượt 7 approve 0 finding; lease thi công `wp1460-r7-g1-claude`). r8 CHỈ thêm khối `nang_tran` theo `ADR-0053` theo đúng đường mục "Kích thước" của r7 đã định: executor lượt 2 dừng TRƯỚC review vì ứng viên sẽ vượt trần mặc định. r8 chỉ đổi dòng `revision`, đoạn Trạng thái này, mục "Kích thước" và bảng "Thay đổi"; hợp đồng, nghiệm thu, lệnh kiểm, write set và quy trình giữ nguyên từng byte. Đoạn trạng thái của r7, giữ làm lịch sử: thay r6 (cùng đường dẫn, commit `2e93730ff2451353086964e78d0bcff7e9bb5ac5`, sha256 `8080a30f639812e8274c4e3a2249301d1eb776bf6320f5a0f833c80f17232009`; r5 `f18abde`, r4 `9f09a12`, r3 `29c99e7`, r2 `9f7010e`, r1 `d7e89d9`). Sáu lượt review spec Codex; lượt 6 (`wp1460-spec-review-6`, trên r6) trả 4 P2 + 1 P3, trong đó hai lớp bị xếp VÁ HỜ; r7 sửa theo LỚP và lần này người soạn TỰ ĐO RĂNG bằng đột biến trước khi báo (bảng "Thay đổi", mục "Số đo"). Lượt 4 còn hai lớp P2: `v1-not-fully-specified` và `legacy-selector-equivalence-is-impossible`. Quyết định chủ kho E1 (chat 2026-11-20, ghi vào Mission r87): **TÁCH B1**. Nguyên nhân gốc được nhận: đóng băng một hợp đồng rất rộng bằng văn xuôi trước khi có mã. Từ r5, packet là **B1a**: phạm vi hẹp, hợp đồng đóng băng bằng HIỆN VẬT MÁY (schema + fixture), văn xuôi chỉ trỏ tới chúng. Phần còn lại thành packet kế nhiệm B1b (mục "Ngoài phạm vi"). Chưa có lease.

Nguồn: kế hoạch nguồn r4 (`ops/specs/wp1172-source-plan-r4/KE_HOACH_NGUON_R4.md`, nhánh `ops/wp1172-plan-r4`, sha256 `0f287ce4369fbeb7b1939daa8de5db7c27c2a4efdc1a21f2fccdd37dc9d83fbe`; "§…" không ghi nguồn là tới tệp ấy). Thẩm quyền: Mission r85 và các revision kế tiếp ghi quyết định chủ kho 2026-11-20 (r86: nâng trần soạn/review, luật kích thước, bỏ A4 khỏi B1; r87: tách B1, thêm một lượt soạn); r84 Q6 = có. Base lúc soạn: `master` `0f9aa2a2cc697129e1f5be72feddf60986286865`; base thi công đo lại khi cấp lease. Đặc tả chỉ có hiệu lực khi chủ kho duyệt băm của nó và một Mission revision cài nó.

Dòng `tran_kich_thuoc_sensitive` là điều kiện `ADR-0053` đặt ra để trần MẶC ĐỊNH của packet `sensitive` là 6 tệp / 450 dòng thêm (thiếu nó thì 3 tệp / 300 dòng; PR giao nộp có 4 tệp). Nó không xin ngoại lệ. Dòng `tran_loi_goi_codex` kích hoạt trần lời gọi Codex review của `ADR-0055` (mười lời gọi mỗi PR; ba phép đo của ADR ấy cho OID này do điều phối đo: có tệp ở OID, vắng ở cha thứ nhất, trên first-parent của `origin/master`, kho không shallow); cách nó ghép với trần Mission ở mục "Quy trình và quyền". OID của `ADR-0053` đã đo: tệp ADR có ở OID ấy, vắng ở cha thứ nhất, OID trên chuỗi first-parent của `origin/master`.

## Mục tiêu
Mỗi lượt `ci-dot-bien-du.yml` (`full_mutant_audit`, M9 của `ADR-0060`) để lại MỘT biên nhận máy đọc do một job thu cuối cùng ghi; job ấy ĐỎ khi không chứng minh được đủ các điều B2/B3 cần. B1a chỉ mang những gì bên tiêu dùng cần: định danh (kho, id kho, đường dẫn workflow, `github.workflow_sha` hoặc `not_measured`), sự kiện và khung, SHA sự kiện, SHA/tree checkout từng job, `run_id`/attempt và attempt bên sản xuất từng mảnh, kiểm kê job kỳ vọng (lập độc lập) so với thực có, kết luận cuối, id + digest artifact, dấu hiệu dương. Kèm canary concurrency A3 còn nợ từ PR0 (§8.2).

## Hợp đồng

### 1. Hiện vật đóng băng (nguồn DUY NHẤT của hình biên nhận)
| Tệp | sha256 | Vai trò |
|---|---|---|
| `ops/specs/wp1460-r1/hop_dong/bien_nhan_audit.v1.schema.json` | `844b5218b6f6844945f5c4c9440f09015d238fe09a60d64b3787c440787e4f46` | JSON Schema draft 2020-12, mọi object `additionalProperties: false`, mọi khoá bắt buộc. Gốc = biên nhận; `$defs/dau_job_v1` = dấu job |
| `ops/specs/wp1460-r1/hop_dong/fixture.json` | `ce8595739a1ab2f4a86c9c196255e5f91fb19a9f6d3865df6caa2d66f9970e6d` | 5 nền (`xanh`, `khong_xanh`, `dau_job`, `rest`, `ngoai`), 120 ca (mỗi ca khai `hinh_hop_le` và TẬP luật C bị vi phạm), 7 địa điểm từ vựng, 17 địa điểm đối tượng |

Nguồn chuẩn tắc thứ ba là khối mã ở mục "Lệnh kiểm" (ghim bằng băm của chính tệp này): hàm `tieu_dung` trong đó là ĐỊNH NGHĨA chạy được của luật C1–C12 cho bên tiêu dùng, viết thành các VỊ TỪ có tên; cùng khối ấy chứa bộ chạy đột biến (`--dot-bien`) gỡ lần lượt TỪNG vị từ và nới lần lượt TỪNG ràng buộc của schema, và đòi mỗi lần như thế làm phép kiểm đỏ. Hai tệp do người soạn viết và ĐÃ CHẠY (mục "Số đo"). Văn xuôi dưới đây KHÔNG định nghĩa lại trường nào; chỗ nào văn xuôi lệch schema hoặc lệch hàm `tieu_dung` thì **hiện vật máy thắng** và đó là lỗi của đặc tả. Đổi một byte của hai tệp là đổi hợp đồng ⇒ cần revision đặc tả mới. Executor chép NGUYÊN BYTE hai tệp này vào PR giao nộp (cùng đường dẫn) và không sửa.

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
- **Job thu `bien-nhan-audit`** (job thứ tư): `needs: [dot-bien-du, dot-bien-manh, dot-bien-gop]`, `if: always()` mức job, `runs-on: ubuntu-latest`, `timeout-minutes: 10`, `permissions` mức job `{contents: read, actions: read}`. Thứ tự bước DUY NHẤT (chốt hình dạng ghim đúng danh sách này): (1) checkout ghim; (2) đo HEAD; (3) dấu job; (4) tải dấu lên; (5) setup-python 3.12; (6) pip ghim như job gom; (7) tải artifact mảnh của run (mẫu `TAI_VE_DU`); (8) tải mọi dấu (`dau-job-<run_id>-*`); (9) bước REST; (10) lệnh thu; (11) tải biên nhận lên, `if-no-files-found: error`. Bước 7–11 mang `if: always()`, nên chúng chạy sau BẤT KỲ bước nào hỏng trước đó. Hệ quả, nói đúng mức: một bước 1–6 hỏng KHÔNG bảo đảm có biên nhận và cũng KHÔNG bảo đảm vắng biên nhận — nếu `python3` của image và mã tại checkout còn chạy được thì lệnh thu vẫn ghi một biên nhận (thường là không xanh); nếu không thì bước 10 hỏng và bước 11 hỏng theo vì thiếu tệp. Trong mọi trường hợp job thu ĐỎ (bước hỏng vẫn hỏng), nên bên tiêu dùng từ chối lượt ấy bằng C2 dù biên nhận nói gì. Không thêm điều kiện `success()` nào vào bước 7–11.
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
Schema chỉ kiểm HÌNH. Luật C là phần bên tiêu dùng PHẢI tự kiểm; **định nghĩa chuẩn tắc là hàm `tieu_dung` ở mục "Lệnh kiểm"**: mỗi dòng `vt("<luật>.<tên>", <điều kiện>)` là một vị từ, luật bị vi phạm khi ít nhất một vị từ của nó sai. Bên tiêu dùng hiện thực lại theo ngôn ngữ của mình và phải cho CÙNG `vi_pham`, `canh_bao`, `moc_tuoi` trên mọi ca của `fixture.json`. Tóm tắt (không chuẩn tắc):
- **Đầu vào độc lập với biên nhận** (`nen.rest`, `nen.ngoai` của fixture): REST của run (`run`, `jobs` mọi attempt, `artifacts`); H và tree của H đang xét; **`job_ky_vong` = tên job bên tiêu dùng TỰ lập từ tệp workflow tại H** (job ma trận: `<khoá> (<giá trị>)`; B3 đọc từ checkout, B2 đọc qua REST contents tại `su_kien.sha`); với mỗi artifact được nêu, thứ bên tiêu dùng đo sau khi tải gói: sha256 gói, và danh sách tệp bên trong (tên, sha256, NỘI DUNG JSON đã đọc).
- **C1.** Hợp lệ theo schema, `ok == true`, `luot.run_attempt` = attempt mới nhất của run.
- **C2.** Run `completed` và `success`; bản ghi REST mới nhất của MỌI job `success`, kể cả `bien-nhan-audit`.
- **C3.** Tên kho, id kho, đường dẫn workflow, `run_id`, tên sự kiện, SHA khớp REST; SHA = H.
- **C4 (song ánh job, kiểm kê từ workflow tại H).** Tập tên REST = `job_ky_vong`; tập tên dòng `job[]` = `job_ky_vong`, không dòng trùng; REST không có hai bản ghi cùng (tên, attempt); `kiem_ke_job.ky_vong` và `thuc_co` = `job_ky_vong` đã xếp; từng dòng: `job_id`, `run_attempt` = bản ghi REST mới nhất của tên ấy; `khoa` suy từ `ten`; `tu_than` ⇔ tên là job thu; tên artifact dấu đúng (run, attempt REST, khoá). Job không chạy lại giữ attempt cũ của CHÍNH nó là hợp lệ.
- **C5.** Mọi `checkout_sha` và `manh[].head` = `su_kien.sha`; mọi `checkout_tree` = tree của H.
- **C6 (song ánh mảnh).** Tập mảnh kỳ vọng lập từ `job_ky_vong`; đúng một dòng `manh[]` mỗi mảnh, không trùng; chỉ số, attempt (= attempt REST mới nhất của job mảnh, ≤ của `dot-bien-gop`) và tên artifact đúng; không job nào có attempt lớn hơn `luot.run_attempt`.
- **C7.** `dau_hieu_duong` = `n/n` và `m/m` với n, m lập từ `job_ky_vong`.
- **C8 (artifact).** Mỗi artifact được nêu: có trong REST với cùng id, tên, `digest`, chưa hết hạn; đã tải được; sha256(gói) = `digest`; gói có ĐÚNG MỘT tệp, đúng tên (`dau-job.json` hoặc `manh-<k>.json`); sha256(tệp) = `sha256_noi_dung`.
- **C9 (mốc tuổi, đã xác thực).** `su_kien.run_created_at` = `run.created_at` của REST và là một thời điểm có thật; với `schedule`: `cron` = chuỗi ghim và `khung_danh_nghia_utc` = mốc cron gần nhất ≤ thời điểm ấy, TÍNH LẠI. Sai ⇒ vi phạm C9. Đạt thì mốc tính tuổi = khung (schedule) hoặc `run_created_at` (dispatch); ngưỡng tuổi do từng bên tiêu dùng đặt. Chạy lại attempt không đổi mốc.
- **C10 (cảnh báo, không phải từ chối ở mức hợp đồng).** `not_measured` ⇒ biên nhận không chứng minh định danh definition; B2 báo nguyên văn; B3 xử lý bằng A4 theo đặc tả của B3.
- **C11 (NỘI DUNG dấu).** Tệp dấu đã tải, đọc ra, đúng `dau_job_v1`, và `khoa_job`, `run_id`, `run_attempt`, `su_kien_sha`, `checkout_sha`, `checkout_tree` trong nó BẰNG điều dòng `job[]` tương ứng khai. Băm khớp mà nội dung nói khác ⇒ vi phạm.
- **C12 (NỘI DUNG mảnh).** Tệp mảnh đã tải là object, `head` và `manh` trong nó bằng dòng `manh[]` tương ứng. (Tính đúng của từng mục đột biến trong tệp ấy thuộc job gom và B1b.)

Độ phủ do lệnh kiểm tự xác nhận: 12/12 luật có ca; mỗi vị từ có ít nhất một ca mà trong luật của nó CHỈ vị từ ấy sai (nên gỡ nó là đỏ). B1a tự chạy `tieu_dung` trên hai biên nhận canary (mục 7).

**Ánh xạ L1–L13 của B3:** L1 `schema` · L2 `kho`, `kho_id` · L3 `workflow.duong_dan` · L4 `su_kien.ten`, `su_kien.cron`, `su_kien.khung_danh_nghia_utc` · L5 `su_kien.sha`, `job[].checkout_sha`, `job[].checkout_tree` · L6 `luot`, `manh[].attempt_ben_san_xuat` · L7 `kiem_ke_job`, `job[].ten` (đối chiếu song ánh với kiểm kê lập từ workflow tại H và với REST, theo C4) · L8 `job[].ket_luan` cho job trước, REST cho job thu (C2) · L9 `dinh_danh_definition` · L10 `job[].dau_job`, `manh[].artifact` · L11 `ok` (B1a không có `ket_cuc`; kết cục A+3 thuộc B1b) · L12 `dau_hieu_duong` · L13 tên artifact và tên tệp ở mục 1.

### 6. Chốt hình dạng (`.claude/dev/ci_dang_ky_test.py`)
`loi_workflow_dot_bien_du` và `loi_ghim_sha_du` mở rộng TƯỜNG MINH, vẫn là danh sách cho phép: đúng bốn job; ba job cũ = hình PR0 cộng đúng hai bước dấu ở đúng vị trí; job thu ghim trọn (needs, `if`, quyền, timeout, từng bước và `if` của nó, tên artifact, mẫu tải, thân bước REST, lệnh thu).

### 7. Canary A3 (trên H CUỐI, trước merge; điều phối gọi theo uỷ quyền của chủ kho)
- **Điều kiện mở:** review mã 0 P0–P2, CI PR xanh trên H, chủ kho đã audit exact-H, H đã đẩy. Mọi thay đổi head sau đó làm A3 và K7 hết hiệu lực; chạy lại trọn mục này trên H mới.
- **A3 (BẮT BUỘC, chặn merge).** Hai `workflow_dispatch` của `ci-dot-bien-du.yml` trên cùng ref có đầu = H, khác `run_id`; lượt hai gọi khi lượt một đã có ít nhất một job `dot-bien-manh` `in_progress`. Đạt ⇔ tồn tại thời điểm cả hai lượt cùng có job mảnh đang chạy (đo bằng `started_at`/`completed_at`); cả hai `success`, 11/11 job `success`, không job nào `cancelled`; HAI biên nhận hợp lệ theo schema, `ok: true`, `su_kien.sha` = H, cùng `kiem_ke_job`, khác `luot.run_id`; cả hai cho tập vi phạm RỖNG khi chạy `tieu_dung` với đầu vào THẬT của chính lượt ấy sau khi lượt kết thúc (REST, `job_ky_vong` lập từ workflow tại H, gói artifact tải về và nội dung đọc từ đó). Lượt một đồng thời là bằng chứng K7.
- **Quan sát push (RIÊNG; không chặn merge).** Một lượt `ci.yml` sự kiện `push` trên `master` có khoảng chạy giao với lúc ít nhất một lượt canary đang chạy; ghi `run_id`, `head_sha`, `created_at`, `run_started_at`, `updated_at`, kết luận, số job có `runner_id` khác 0; rồi đo lại hai lượt canary không có job `cancelled`. Push phải tự nhiên (chủ kho merge một PR sẵn sàng trong cửa sổ); B1a không tạo commit giả, không thêm trigger. Không có push ⇒ ghi `not_run` (nghiệm thu chưa đạt, giữ nguyên tên trong hồ sơ).
- **Đo attempt thật (1 `ci_reruns`; không chặn merge).** Sau lượt hai: chạy lại RIÊNG job `bien-nhan-audit` ⇒ biên nhận attempt 2 `ok: true`, `luot.run_attempt == 2`, mảnh vẫn attempt 1, artifact biên nhận attempt 1 còn nguyên. Lượt rerun đã dùng cho sự cố hạ tầng ⇒ `not_run`.
- **Chi phí CI (ƯỚC LƯỢNG từ nền #1434).** Mỗi lượt: 8 mảnh ≈ 13 282 s (`[B: M1.luot_du_8_manh_success.tong_giay_8_job_manh_moi_luot]`) + job registry ≈ 1 680 s (`[B: M1.theo_job."dot-bien-du | ubuntu-latest".trung_vi]`) + gom ≈ 10 s ⇒ ≈ 14 972 s; hai lượt ≈ 29 944 s ≈ 8,3 giờ job. CHƯA ĐO: thời gian tường, job thu, 11 bước dấu mỗi lượt, xếp hàng khi 22 job chạy cạnh một lượt push. Ca mới chạy trong `gate-registry` của `ci.yml`; executor báo delta thời gian job (§13).
- **Ngân sách:** `full_m9_runs` = 2 cho packet này (quyết định chủ kho, hiệu lực khi Mission revision ghi nó), vừa đủ MỘT canary; cộng 1 `ci_reruns`. H đổi sau canary ⇒ DỪNG và xin nâng trần trước khi gọi thêm.
- Bằng chứng ghi ở comment PR và hồ sơ land của điều phối, không trong PR giao nộp.

## Nghiệm thu
1. **Hợp đồng máy (reviewer kiểm bằng cách CHẠY).** Lưu khối mã ở mục "Lệnh kiểm" ra một tệp ngoài kho rồi chạy `python3 -B <tệp> ops/specs/wp1460-r1/hop_dong --dot-bien` với `jsonschema==4.26.0`. Kết quả phải là đúng ba dòng: `FIXTURE: 480/480 phep kiem dung ky vong · hinh 120 · ngu nghia 118 · tu vung 79 · doi tuong 163 · luat duoc phu 12/12` · `DOT BIEN: giet 249/249 · vi tu 57 · noi long schema 192` · `TONG: DAT`, mã thoát 0 (bỏ `--dot-bien` thì chỉ có dòng đầu và dòng cuối; lần chạy của người soạn mất khoảng 5 giây không đột biến và khoảng 5 phút có đột biến). Một đột biến chỉ được tính là GIẾT khi phép kiểm báo lệch bằng tín hiệu riêng `LechDauTien`; mọi ngoại lệ khác (`KeyError`, lỗi schema…) được in `LOI … (khong tinh la giet)` và làm tổng ĐỎ; bộ chạy tự kiểm điều ấy bằng một đột biến ném `KeyError`. sha256 hai tệp bằng mục 1, trên nhánh đặc tả và trong PR giao nộp. Bộ test của PR giao nộp chạy lại đúng các phép này trên hai tệp đã chép.
2. **Lệnh thu ↔ schema.** Mọi biên nhận lệnh thu ghi ra trong bộ test (xanh và không xanh) hợp lệ theo schema; mọi dấu hợp lệ theo `$defs/dau_job_v1`. Ba ca dương: lượt đầu khoẻ; chạy lại riêng job thu (attempt 2); chạy lại một mảnh (mảnh, gom, thu ở attempt 2) — đều `ok: true`, thoát 0, và `tieu_dung` cho tập vi phạm rỗng khi đưa đúng đầu vào của ca (REST, `job_ky_vong`, gói và NỘI DUNG tệp do chính bộ test tải/đọc từ artifact giả, không dựng từ biên nhận). Bốn ca vòng khép kín cho hình không xanh: `run.loi`; `run.json` thiếu hoặc sai dạng `created_at`; `schedule` không biết khung; sự kiện `push` — mỗi ca ghi biên nhận không xanh hợp lệ với mốc `null` (không mốc bịa). Ca đối số: thiếu `github.sha`, `run_id` không phải số ⇒ thoát 2, không có tệp biên nhận.
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
"""Lenh kiem hop dong bien_nhan_audit.v1 (wp1460 B1a). python3 -B <tep> <thu muc hop_dong> [--dot-bien]"""
import copy, datetime, json, re, sys
import jsonschema
JOB_THU, JOB_GOP, TIEN_TO_MANH, CRON_GHIM = "bien-nhan-audit", "dot-bien-gop", "dot-bien-manh", "17 19 * * 6"

def nap(d):
    d = d.rstrip("/") + "/"
    return (json.load(open(d + "bien_nhan_audit.v1.schema.json", encoding="utf-8")), json.load(open(d + "fixture.json", encoding="utf-8")))

def bo_kiem(S):
    jsonschema.Draft202012Validator.check_schema(S)
    return {"bien_nhan": jsonschema.Draft202012Validator(S),
            "dau_job": jsonschema.Draft202012Validator({"$schema": S["$schema"], "$ref": "#/$defs/dau_job_v1", "$defs": S["$defs"]})}

def tro(doc, duong):
    o = doc
    for k in [x.replace("~1", "/").replace("~0", "~") for x in duong.split("/")[1:]]:
        o = o[int(k)] if isinstance(o, list) else o[k]
    return o

def ap(doc, sua):
    for s in sua or []:
        cha, _, cuoi = s["duong"].rpartition("/")
        o, cuoi = tro(doc, cha), cuoi.replace("~1", "/").replace("~0", "~")
        if isinstance(o, list) and cuoi == "-":
            o.append(s["gia_tri"])
        elif s.get("xoa"):
            del o[int(cuoi) if isinstance(o, list) else cuoi]
        else:
            o[int(cuoi) if isinstance(o, list) else cuoi] = s["gia_tri"]
    return doc

def khoa_tu_ten(ten):
    m = re.fullmatch(r"(.+) \((.+)\)", ten)
    return f"{m[1]}-{m[2]}" if m else ten

def doc_moc(v):
    try:
        return datetime.datetime.strptime(v, "%Y-%m-%dT%H:%M:%SZ")
    except (TypeError, ValueError):
        return None

def khung_cron(tao):
    """Moc `17 19 * * 6` (thu Bay 19:17 UTC) gan nhat <= tao."""
    t = tao.replace(hour=19, minute=17, second=0) - datetime.timedelta(days=(tao.weekday() - 5) % 7)
    return t if t <= tao else t - datetime.timedelta(days=7)

def tieu_dung(V, b, rest, ngoai, bo=None, hop_le=None):
    """Luat C cua ben tieu dung, tung VI TU co ten. Tra (tap luat vi pham, canh bao, moc tinh tuoi). `bo` = ten vi tu bi go (dot bien);
    `hop_le` = ket qua kiem hinh da co cua b (None thi tu kiem)."""
    if not (V["bien_nhan"].is_valid(b) if hop_le is None else hop_le) or b["ok"] is not True:
        return {"C1"}, [], None
    vp, run, lu, sk = set(), rest["run"], b["luot"], b["su_kien"]
    def vt(ten, dk):                           # ten = "<luat>.<vi tu>"
        if ten != bo and not dk: vp.add(ten.split(".")[0])
    E = ngoai["job_ky_vong"]                   # ten job ben tieu dung TU lap tu tep workflow tai H
    moi = {}                                   # ten job -> ban ghi REST co run_attempt lon nhat
    for j in rest["jobs"]:
        if j["name"] not in moi or j["run_attempt"] > moi[j["name"]]["run_attempt"]:
            moi[j["name"]] = j
    cap = [(j["name"], j["run_attempt"]) for j in rest["jobs"]]
    vt("C1.attempt_moi_nhat", lu["run_attempt"] == run["run_attempt"])
    vt("C2.run_completed", run["status"] == "completed")
    vt("C2.run_success", run["conclusion"] == "success")
    vt("C2.moi_job_success", all(j["conclusion"] == "success" for j in moi.values()))
    vt("C3.kho", b["kho"] == run["repository"]["full_name"])
    vt("C3.kho_id", b["kho_id"] == run["repository"]["id"])
    vt("C3.duong_dan", b["workflow"]["duong_dan"] == run["path"])
    vt("C3.run_id", lu["run_id"] == run["id"])
    vt("C3.su_kien_ten", sk["ten"] == run["event"])
    vt("C3.sha_rest", sk["sha"] == run["head_sha"])
    vt("C3.sha_h", sk["sha"] == ngoai["h"])
    hang = {r["ten"]: r for r in b["job"]}
    vt("C4.rest_khong_trung", len(cap) == len(set(cap)))
    vt("C4.rest_du", set(moi) == set(E))
    vt("C4.dong_khong_trung", len(b["job"]) == len(hang))
    vt("C4.tap_ten", set(hang) == set(E))
    vt("C4.ky_vong", b["kiem_ke_job"]["ky_vong"] == sorted(E))
    vt("C4.thuc_co", b["kiem_ke_job"]["thuc_co"] == sorted(E))
    cung = [(r, moi[t]) for t, r in hang.items() if t in moi]
    vt("C4.job_id", all(r["job_id"] == j["id"] for r, j in cung))
    vt("C4.run_attempt", all(r["run_attempt"] == j["run_attempt"] for r, j in cung))
    vt("C4.khoa", all(r["khoa"] == khoa_tu_ten(r["ten"]) for r in b["job"]))
    vt("C4.tu_than", all(r["tu_than"] == (r["ten"] == JOB_THU) for r in b["job"]))
    vt("C4.ten_dau", all(r["dau_job"]["ten"] == f"dau-job-{lu['run_id']}-{j['run_attempt']}-{khoa_tu_ten(r['ten'])}" for r, j in cung))
    vt("C5.job_sha", all(r["checkout_sha"] == sk["sha"] for r in b["job"]))
    vt("C5.manh_head", all(m["head"] == sk["sha"] for m in b["manh"]))
    vt("C5.tree_h", all(r["checkout_tree"] == ngoai["tree_h"] for r in b["job"]))
    ky = {}                                    # khoa job manh -> k, lap tu E (doc lap voi bien nhan va REST)
    for t in E:
        m = re.fullmatch(re.escape(TIEN_TO_MANH) + r" \((0|[1-9][0-9]*)\)", t)
        if m: ky[khoa_tu_ten(t)] = int(m[1])
    ten_theo_khoa = {khoa_tu_ten(t): t for t in E}
    att = lambda khoa: moi.get(ten_theo_khoa.get(khoa), {}).get("run_attempt")   # attempt REST moi nhat cua job mang khoa ay
    co = [m for m in b["manh"] if m["khoa_job"] in ky and att(m["khoa_job"]) is not None]
    vt("C6.manh_khong_trung", len(b["manh"]) == len({m["khoa_job"] for m in b["manh"]}))
    vt("C6.tap_manh", {m["khoa_job"] for m in b["manh"]} == set(ky))
    vt("C6.job_le_luot", all(j["run_attempt"] <= lu["run_attempt"] for j in moi.values()))
    vt("C6.chi_so", all(m["manh"] == ky[m["khoa_job"]] for m in co))
    vt("C6.attempt", all(m["attempt_ben_san_xuat"] == att(m["khoa_job"]) for m in co))
    vt("C6.le_gop", att(JOB_GOP) is not None and all(att(m["khoa_job"]) <= att(JOB_GOP) for m in co))
    vt("C6.ten_artifact", all(m["artifact"]["ten"] == f"{TIEN_TO_MANH}-{lu['run_id']}-{att(m['khoa_job'])}-{ky[m['khoa_job']]}" for m in co))
    vt("C7.job_truoc", b["dau_hieu_duong"]["job_truoc_success"] == f"{len(E) - 1}/{len(E) - 1}")
    vt("C7.manh", b["dau_hieu_duong"]["manh"] == f"{len(ky)}/{len(ky)}")
    kho = {a["id"]: a for a in rest["artifacts"]}
    dau = [(r["dau_job"], "dau-job.json", r) for r in b["job"]]
    mnh = [(m["artifact"], f"manh-{m['manh']}.json", m) for m in b["manh"]]
    cr = [(a, kho[a["id"]]) for a, _, _ in dau + mnh if a["id"] in kho]
    ct = [(a, ten, d, ngoai["tai_ve"][str(a["id"])]) for a, ten, d in dau + mnh if str(a["id"]) in ngoai["tai_ve"]]
    c1 = [x for x in ct if len(x[3]["tep"]) == 1 and x[3]["tep"][0]["ten"] == x[1]]      # dung MOT tep, dung ten
    vt("C8.co_trong_rest", len(cr) == len(dau + mnh))
    vt("C8.ten", all(a["ten"] == r["name"] for a, r in cr))
    vt("C8.digest_rest", all(a["digest"] == r["digest"] for a, r in cr))
    vt("C8.chua_het_han", all(r["expired"] is False for a, r in cr))
    vt("C8.da_tai", len(ct) == len(dau + mnh))
    vt("C8.goi", all(a["digest"] == "sha256:" + t["sha256_goi"] for a, _, _, t in ct))
    vt("C8.mot_tep", len(c1) == len(ct))
    vt("C8.tep_bam", all(a["sha256_noi_dung"] == t["tep"][0]["sha256"] for a, _, _, t in c1))
    nd = [(t["tep"][0]["noi_dung"], d) for a, ten, d, t in c1 if ten == "dau-job.json"]
    nho = V.setdefault("nho", {})                # nho ket qua kiem hinh dau theo noi dung
    def dau_hop_le(n):
        k = json.dumps(n, sort_keys=True)
        if k not in nho: nho[k] = V["dau_job"].is_valid(n)
        return nho[k]
    ok = [(n, d) for n, d in nd if dau_hop_le(n)]
    vt("C11.hinh", len(ok) == len(nd))
    vt("C11.khoa_job", all(n["khoa_job"] == d["khoa"] for n, d in ok))
    vt("C11.run_id", all(n["run_id"] == lu["run_id"] for n, d in ok))
    vt("C11.run_attempt", all(n["run_attempt"] == d["run_attempt"] for n, d in ok))
    vt("C11.su_kien_sha", all(n["su_kien_sha"] == sk["sha"] for n, d in ok))
    vt("C11.checkout_sha", all(n["checkout_sha"] == d["checkout_sha"] for n, d in ok))
    vt("C11.checkout_tree", all(n["checkout_tree"] == d["checkout_tree"] for n, d in ok))
    nm = [(t["tep"][0]["noi_dung"], d) for a, ten, d, t in c1 if ten != "dau-job.json"]
    om = [(n, d) for n, d in nm if isinstance(n, dict)]
    vt("C12.la_object", len(om) == len(nm))
    vt("C12.head", all(n.get("head") == d["head"] for n, d in om))
    vt("C12.manh", all(type(n.get("manh")) is int and n.get("manh") == d["manh"] for n, d in om))
    tao = doc_moc(sk["run_created_at"])
    vt("C9.tao_khop_rest", sk["run_created_at"] == run["created_at"])
    vt("C9.lich_hop_le", tao is not None)
    if sk["ten"] == "schedule":
        vt("C9.cron_ghim", sk["cron"] == CRON_GHIM)
        vt("C9.khung", tao is None or sk["khung_danh_nghia_utc"] == khung_cron(tao).strftime("%Y-%m-%dT%H:%M:%SZ"))
    canh = ["C10"] if bo != "C10.canh_bao" and b["dinh_danh_definition"]["trang_thai"] == "not_measured" else []
    return vp, canh, sk.get("khung_danh_nghia_utc") or sk["run_created_at"]

class LechDauTien(Exception):
    """Tin hieu RIENG cua bo kiem: phep kiem dau tien lech (dung cho dot bien; ngoai le khac KHONG duoc tinh la giet)."""

def chay(S, F, bo=None, som=False):
    """Chay moi phep kiem. Tra (danh sach lech, bo dem, tap luat duoc phu). `bo` (go mot vi tu) chi anh huong phan ngu nghia nen chi chay phan ay."""
    V, sai, dem, phu = bo_kiem(S), [], {"hinh": 0, "ngu_nghia": 0, "tu_vung": 0, "doi_tuong": 0}, set()
    def hop(nen, doc): return V["dau_job" if nen == "dau_job" else "bien_nhan"].is_valid(doc)
    def lech(x):
        sai.append(x)
        if som: raise LechDauTien(x)
    ten = [c["ten"] for c in F["ca"]]
    assert len(ten) == len(set(ten)), "ten ca trung"
    for t in [] if bo else F["tu_vung"]:         # moi dia diem co pattern: mau hop le; bien the thi khong
        bien = [t["mau"] + "\n", t["mau"] + "\r\n", " " + t["mau"], t["mau"] + " ", 5, None, [t["mau"]]] + t["sai"]
        for gt, mong in [(t["mau"], True)] + [(x, False) for x in bien]:
            dem["tu_vung"] += 1
            if hop(t["nen"], ap(copy.deepcopy(F["nen"][t["nen"]]), [{"duong": t["duong"], "gia_tri": gt}])) != mong:
                lech(f"TU VUNG {t['dia_diem']}: {gt!r}")
    for t in [] if bo else F["doi_tuong"]:       # moi object: go tung khoa / them khoa la / thay bang chuoi, danh sach deu KHONG hop le
        goc = ap(copy.deepcopy(F["nen"][t["nen"]]), t.get("sua_truoc"))
        o = tro(goc, t["duong"]) if t["duong"] else goc
        bien = [{k: v for k, v in o.items() if k != x} for x in o] + [dict(o, khoa_la=1), "x", [o]]
        for moi, mong in [(o, True)] + [(x, False) for x in bien]:
            dem["doi_tuong"] += 1
            doc = moi if not t["duong"] else ap(copy.deepcopy(goc), [{"duong": t["duong"], "gia_tri": moi}])
            if hop(t["nen"], doc) != mong:
                lech(f"DOI TUONG {t['nen']}{t['duong']}: {sorted(moi) if isinstance(moi, dict) else moi!r}")
    for c in F["ca"]:
        doc = ap(copy.deepcopy(F["nen"][c["nen"]]), c.get("sua"))
        hop_le = c["hinh_hop_le"] if bo else hop(c["nen"], doc)
        dem["hinh"] += 1
        if hop_le != c["hinh_hop_le"]:
            lech("HINH " + c["ten"])
            continue                             # lech hinh: bao rieng, khong roi xuong nhanh ngu nghia
        if c["nen"] == "dau_job":
            continue
        vp, canh, moc = tieu_dung(V, doc, ap(copy.deepcopy(F["nen"]["rest"]), c.get("sua_rest")), ap(copy.deepcopy(F["nen"]["ngoai"]), c.get("sua_ngoai")), bo, hop_le)
        dem["ngu_nghia"] += 1
        if sorted(vp) != sorted(["C1"] if not hop_le else c["vi_pham"]) or canh != c.get("canh_bao", []) or ("moc_tuoi" in c and moc != c["moc_tuoi"]):
            lech(f"NGU NGHIA {c['ten']}: vi pham {sorted(vp)} canh bao {canh} moc {moc}")
        phu |= set(vp) | set(canh) | ({"C9"} if "moc_tuoi" in c else set())
    can = {f"C{i}" for i in range(1, 13)}
    if bo is None and phu != can:
        lech(f"PHU LUAT thieu {sorted(can - phu)}")
    return sai, dem, phu

def vi_tri_schema(S):
    """Moi cho noi long schema: (mo ta, ham sua tren ban sao)."""
    ra = []
    def di(n, duong):
        if isinstance(n, dict):
            for k in ("pattern", "minLength", "minimum", "minItems", "uniqueItems", "const", "maxContains", "type"):
                if k in n: ra.append((f"{duong}: go {k}", duong, ("go", k)))
            if "contains" in n: ra.append((f"{duong}: go contains", duong, ("go", "contains")))
            if n.get("additionalProperties") is False: ra.append((f"{duong}: mo additionalProperties", duong, ("mo", None)))
            for x in n.get("required", []): ra.append((f"{duong}: bo required {x}", duong, ("req", x)))
            for i in range(len(n.get("oneOf", []))): ra.append((f"{duong}: bo nhanh oneOf[{i}]", duong, ("oneOf", i)))
            for k, v in n.items(): di(v, f"{duong}/{k}")
        elif isinstance(n, list):
            for i, v in enumerate(n): di(v, f"{duong}/{i}")
    di(S, "")
    return ra

def sua_schema(S, duong, lenh):
    S = copy.deepcopy(S)
    n = tro(S, duong) if duong else S
    if lenh[0] == "go":
        del n[lenh[1]]
        if lenh[1] == "contains": n.pop("maxContains", None)
    elif lenh[0] == "mo": n["additionalProperties"] = True
    elif lenh[0] == "req": n["required"].remove(lenh[1])
    else: del n["oneOf"][lenh[1]]
    return S

def dot_bien(S, F):
    """Moi dot bien phai lam `chay` bao LECH ma KHONG nem ngoai le. Tra (giet, tong, danh sach song/loi)."""
    ten_vt = sorted(set(re.findall(r'vt\("(C[0-9]+\.[a-z_0-9]+)"', open(__file__, encoding="utf-8").read())) | {"C10.canh_bao"})
    ds = [("vi tu " + t, lambda t=t: chay(S, F, bo=t, som=True)) for t in ten_vt]
    ds += [("schema " + mt, lambda d=d, l=l: chay(sua_schema(S, d, l), F, som=True)) for mt, d, l in vi_tri_schema(S)]
    def loi_gia(): raise KeyError("tu kiem")       # tu kiem bo phan hang: ngoai le KHONG duoc tinh la giet
    giet, xau = 0, []
    for ten, f in ds + [("TU KIEM ngoai le vo can", loi_gia)]:
        try:
            f()
            ket = "SONG"
        except LechDauTien:                        # CHI tin hieu rieng cua bo kiem moi la giet
            ket = "GIET"
        except Exception as e:                     # noqa: BLE001
            ket = f"LOI {type(e).__name__}"
        if ten.startswith("TU KIEM"):
            if ket != "LOI KeyError": xau.append(f"TU KIEM bo phan hang hong: {ket}")
        elif ket == "GIET": giet += 1
        else: xau.append(f"{ket} (khong tinh la giet): {ten}")
    return giet, len(ds), xau, len(ten_vt)

if __name__ == "__main__":
    S, F = nap(sys.argv[1])
    sai, dem, phu = chay(S, F)
    n = sum(dem.values())
    print(f"FIXTURE: {n - len(sai)}/{n} phep kiem dung ky vong · hinh {dem['hinh']} · ngu nghia {dem['ngu_nghia']} · tu vung {dem['tu_vung']} · doi tuong {dem['doi_tuong']} · luat duoc phu {len(phu)}/12")
    for x in sai: print("LECH:", x)
    if "--dot-bien" in sys.argv[2:] and not sai:
        giet, tong, xau, so_vt = dot_bien(S, F)
        print(f"DOT BIEN: giet {giet}/{tong} · vi tu {so_vt} · noi long schema {tong - so_vt}")
        for x in xau: print("LECH:", x)
        sai += xau
    print("TONG:", "DAT" if not sai else "DO")
    sys.exit(1 if sai else 0)
```

## Write set
- Nhánh `ops/wp1460-r1` (đặc tả, không thuộc PR giao nộp): `ops/specs/wp1460-r1/SPEC.md`, hai tệp `hop_dong/` ở mục 1, `ops/leases/wp1460-*.yaml`.
- PR giao nộp, đúng BỐN tệp: `.github/workflows/ci-dot-bien-du.yml` · `.claude/dev/ci_dang_ky_test.py` · hai tệp `hop_dong/` ở mục 1 (chép nguyên byte từ nhánh đặc tả, executor không soạn và không sửa).

Không tệp thứ năm. Không đặt được lệnh thu trong `ci_dang_ky_test.py` ⇒ DỪNG và báo.

## Kích thước
- Trần là trần MẶC ĐỊNH của lớp `sensitive` theo `ADR-0053`: **≤ 6 tệp và ≤ 450 dòng thêm** theo `git diff --numstat` so base. Lease cấp theo trần ấy. Đặc tả không xin, không ước lượng, không cấp ngoại lệ.
- Đã đo: hai tệp `hop_dong/` chiếm 34 + 161 = 195 dòng thêm (đếm dòng trên chính hai tệp đã ghim băm); còn 255 dòng trong trần cho workflow, lệnh thu, ca và đột biến.
- Executor đo `git diff --numstat <base>...HEAD` trên đúng bốn tệp giao nộp trong lúc thi công và trước MỖI lần xin review; ghi số đo vào PR.
- Theo `ADR-0044`: ứng viên giao nộp vượt trần ⇒ DỪNG TRƯỚC review; không cắt ca, fixture hay đột biến để lọt trần; báo điều phối kèm numstat đã đo và phần việc còn thiếu.
- Khi ấy điều phối xin chủ kho một khối `nang_tran` đúng `ADR-0053` (bốn trường `ai_nang`, `can_cu` có numstat ĐÃ ĐO, `tran_cu`, `tran_moi`); chủ kho duyệt; khối vào một revision đặc tả (chỉ đổi dòng `revision`, đoạn Trạng thái, mục này, bảng Thay đổi) và chép nguyên vào lease. Executor chỉ tiếp tục sau khi lease mang khối ấy.
- **Khối `nang_tran` (`ADR-0053`, quyết định chủ kho 2026-11-24, ghi hộ trên #1172):**
  - `ai_nang`: chủ kho `ducthangho`, câu trả lời nguyên văn «6 tệp / 1600 dòng» (phiên điều phối Mission hỏi qua công cụ hỏi đáp, ~12:15Z).
  - `can_cu`: numstat ĐÃ ĐO trên head dở `877295930d136413dce68a9cdee5a8a3f35075e1` (tree `72ab13c24c391110094e37eb130fd9ba32a911a7`) so base `5259239d763c9ffc1677f033bd9a9cf23ede9299`: 4 tệp, +408/−20 (`.claude/dev/ci_dang_ky_test.py` +127, `.github/workflows/ci-dot-bien-du.yml` +86, schema +34, fixture +161); phiên điều phối gói đo lại khớp lời executor. Phần còn thiếu lúc dừng: collector `--thu-bien-nhan-audit`, bộ kiểm hợp đồng (Nghiệm thu 1), ca Nghiệm thu 2–4, bộ chạy đột biến cùng các mutant (Nghiệm thu 7). Ước tính của executor cho ứng viên đầy đủ 930–1120 dòng thêm là ƯỚC, KHÔNG phải số đo, và không là căn cứ của trần.
  - `tran_cu`: 6 tệp / 450 dòng thêm (trần mặc định `sensitive`).
  - `tran_moi`: 6 tệp / 1600 dòng thêm theo `git diff --numstat` so base của lease.
  - Khối này chép NGUYÊN vào lease kế nhiệm. Mọi luật còn lại của mục này giữ nguyên với `tran_moi` thay cho trần mặc định: đo trong lúc thi công và trước MỖI lần xin review; vượt `tran_moi` ⇒ DỪNG trước review, không cắt ca/fixture/đột biến.

- **Khối `nang_tran` thứ hai (`ADR-0053`, quyết định chủ kho 2026-11-24 ~14:45Z, ghi hộ trên #1172):**
  - `ai_nang`: chủ kho `ducthangho`, lựa chọn nguyên văn «+1 executor, nâng trần thêm» với mô tả kèm theo «nâng trần lên 6 tệp/1700 dòng để có dư».
  - `can_cu`: numstat ĐÃ ĐO trên `1c31f5a88ba125af708a9609085c0edd2f8dc3ee` (tree `d316445a44465cd563ce72b64a65b4893e63ad0c`) so base `5259239d763c9ffc1677f033bd9a9cf23ede9299`: 4 tệp, +1566/−20; còn 34 dòng tới `tran_moi` 1600 của khối thứ nhất. Việc còn lại: vá F02-R2 (bắt `RecursionError` ở biên X2, một ca tiến trình con, một đột biến riêng), reviewer ước 10–20 dòng (ƯỚC, không phải số đo).
  - `tran_cu`: 6 tệp / 1600 dòng thêm (khối thứ nhất).
  - `tran_moi`: 6 tệp / 1700 dòng thêm theo `git diff --numstat` so base của lease.
  - Khối này thay khối thứ nhất làm trần hiệu lực và được chép NGUYÊN vào lease kế nhiệm. Các luật còn lại của mục giữ nguyên.

## Quy trình và quyền
- Lớp review: `sensitive`. Executor: Claude Code (Fable 5.2). Reviewer: Codex service gpt-6-astra, mức suy luận cao nhất, phiên độc lập, chỉ đọc.
- Trần lời gọi Codex review trên PR giao nộp: dòng khai `ADR-0055` ở đầu tệp đặt trần PACKET là mười lời gọi mỗi PR (đếm mọi lời gọi Codex review trên PR ấy: review mã qua service VÀ connector). Trần Mission cho packet này hẹp hơn và là trần dùng được: review mã 3 + connector 2 = 5 lời gọi ≤ 10. Thiếu dòng khai thì trần packet là hai và lượt review mã thứ ba không dùng được. Review ĐẶC TẢ là bộ đếm khác (theo Mission), không tính vào mười lời gọi này và không được đặt lại khi đặc tả đổi revision.
- Trần khác: theo r85 `per_new_packet` cùng các mức chủ kho đã nâng cho packet này ngày 2026-11-20 (soạn spec, review spec, `full_m9_runs` = 2), có hiệu lực khi Mission revision ghi chúng; attempts 3, CI PR Ubuntu 3, CI rerun 1, Windows CI 0.
- Trước lease: chủ kho duyệt băm; Mission revision riêng; `ai-dang-giu` trên MỌI ref cho write set; lease `wp1236-a-r9-g1-claude-20261120` (giữ `.claude/dev/ci_dang_ky_test.py` tới `2026-11-22T15:35Z`) đã hết hạn hoặc đã thu hồi hai chiều. B2, PR2, B1b (và B3 nếu đăng ký bộ test) dùng chung tệp ấy nên xếp NỐI TIẾP.
- Chủ kho tự audit exact-H trước LẦN ĐẨY ĐẦU của H; điều phối không ký thay. Merge do chủ kho bấm. Windows: miễn theo quy tắc thường trực.
- Hoàn tác: revert PR về hình PR0; biên nhận đã sinh giữ làm lịch sử.

## Ngoài phạm vi
- **Chuyển sang packet kế nhiệm B1b (chưa mở, cần đặc tả và thẩm quyền riêng):** bảng mã chẩn đoán và việc tính lại kết luận từ biên nhận (`chan_doan`, phân biệt `do` / `khong_ket_luan`); bốn tầng kết cục A+3 và kiểm kê MỤC đột biến (gồm phép so 321 khoá G6); nguồn gốc phụ thuộc (Python/OS/`requirements`/phiên bản công cụ); giây và bộ nhớ (RSS) từng mảnh; đưa biên nhận mảnh ĐỎ tới job thu. B1b phải mở rộng theo cách không làm biên nhận B1a mất hợp lệ, hoặc dùng `schema` mới.
- B2, B3, B4, PR2, PR5; `ci.yml`; `.claude/dev/packet_loop.py`; `ops/nhanh_don_duoc_test.py`; `ops/ci_provenance.py`, `ops-do-workflow-definition.yml` và toàn bộ A4; trigger, cron, ma trận, timeout; mọi giá trị `CHO_PHEP`; kho uỷ quyền do máy kiểm; chế độ chặn của bên tiêu dùng; route production; LIVE.

## Số đo lúc soạn (2026-11-20, `master` `0f9aa2a`)
- Lệnh kiểm (trích từ CHÍNH tệp này rồi chạy với `--dot-bien`), `jsonschema` 4.26.0, trên hai tệp đã ghim: `FIXTURE: 480/480 phep kiem dung ky vong · hinh 120 · ngu nghia 118 · tu vung 79 · doi tuong 163 · luat duoc phu 12/12` / `DOT BIEN: giet 249/249 · vi tu 57 · noi long schema 192` / `TONG: DAT`, mã thoát 0. Kỳ vọng `vi_pham` của từng ca do người soạn viết tay TRƯỚC khi chạy; lần chạy đầu lệch 2 ca và cả hai là kỳ vọng viết tay sai (đã lập luận lại từng vị từ rồi mới sửa kỳ vọng, không sửa oracle).
- REST: run `43990524880` có 10 job `dot-bien-du`, `dot-bien-manh (0)`…`(7)`, `dot-bien-gop`; artifact có trường `digest` dạng `sha256:<64 hex>`.
- CHƯA ĐO: `actionlint`/Ruff nền; giá trị `github.workflow_sha` và `github.repository_id` trên lượt dispatch của nhánh; cách REST liệt kê job qua nhiều attempt (mục 7 đo); hạn mức job đồng thời; thời hạn lưu artifact.

## Thay đổi
**r8 → r9 (`nang_tran` thứ hai). Chỉ đổi:**

| Chỗ | Đổi |
|---|---|
| dòng tiêu đề, `revision` | 8 → 9 |
| đoạn Trạng thái | thêm câu dẫn r9, giữ nguyên đoạn r8 làm lịch sử |
| mục "Kích thước" | thêm khối `nang_tran` thứ hai (`tran_cu` 6/1600 → `tran_moi` 6/1700) |
| bảng "Thay đổi" | thêm mục này |

**r7 → r8 (`nang_tran`, không qua review spec mới về nội dung). Chỉ đổi:**

| Chỗ | Đổi |
|---|---|
| dòng tiêu đề, `revision` | 7 → 8 |
| đoạn Trạng thái | thêm câu dẫn r8, giữ nguyên đoạn r7 làm lịch sử |
| mục "Kích thước" | thêm khối `nang_tran` (`ai_nang`, `can_cu` có numstat đã đo, `tran_cu`, `tran_moi`) |
| bảng "Thay đổi" | thêm mục này |

**r6 → r7 (review spec lượt 6). Sửa theo LỚP; răng do người soạn tự đo.**

| Lớp | Sửa ở r7 |
|---|---|
| `consumer-records-not-bound-to-producers` (B1-15, VÁ HỜ ở r6) | Hai ràng buộc mới ở biên bên tiêu dùng. (a) NỘI DUNG: luật C11 (dấu) và C12 (mảnh) so nội dung tệp đã tải với dòng biên nhận; C8 đòi gói có đúng một tệp đúng tên; đầu vào `tai_ve` mang nội dung đã đọc. (b) KIỂM KÊ: `job_ky_vong` lập từ tệp workflow tại H thay cho "tập tên REST"; C4/C6/C7 dùng nó. Chín phản ví dụ "băm thật, nội dung khai khác" và hai phản ví dụ "cùng thiếu ở REST lẫn biên nhận" của reviewer nay là ca âm (`luat-C11-*`, `luat-C12-*`, `luat-C4-cung-thieu-*`) |
| `frozen-fixture-semantic-oracle-missing` (B1-16, VÁ HỜ ở r6) | Oracle viết thành vị từ có tên; bộ chạy `--dot-bien` trong lệnh kiểm gỡ TỪNG vị từ và nới TỪNG ràng buộc schema (gỡ `pattern`/`type`/`const`/`minimum`/`minLength`/`minItems`/`uniqueItems`/`contains`/`maxContains`, mở `additionalProperties`, bỏ từng khoá `required`, bỏ từng nhánh `oneOf`); số giết/tổng in ra và phải bằng nhau. Ca âm viết lại để mỗi vị từ có ca cô lập. Schema bỏ `minLength`/`maxLength` thừa (pattern đã cố định độ dài) để không còn đột biến tương đương; thêm ca sai ký tự cùng độ dài và ca sai kiểu. Lệch hình báo riêng, không rơi xuống nhánh ngữ nghĩa. Tín hiệu giết là lớp ngoại lệ riêng, có tự kiểm |
| `consumer-freshness-anchor-unverified` (B1-19) | C9 thành luật có vi phạm: `run_created_at` phải bằng `run.created_at` của REST và là thời điểm có thật; `schedule` phải đúng cron ghim và khung TÍNH LẠI. Ca: mốc 2099, ngày không tồn tại, cron lạ, khung tương lai, khung tuần trước; ca biên đúng mốc cron, trước mốc một giây, trễ sang thứ Ba; ca chạy lại job thu giữ nguyên mốc. Niên biểu của `xanh-schedule` đã sửa |
| `collector-early-failure-contract-contradiction` (B1-20, P3) | Mục 3: bỏ câu "bước 1–6 hỏng ⇒ không có biên nhận"; nói đúng hệ quả của `always()`: không bảo đảm có, không bảo đảm vắng; job đỏ và C2 từ chối trong mọi trường hợp |
| `source-review-budget-not-activated` (B1-21) | Thêm dòng khai `tran_loi_goi_codex: ADR-0055@…`; mục "Quy trình và quyền" đối chiếu trần packet (10) với trần Mission (review mã 3 + connector 2) và tách bộ đếm review đặc tả |
| `v1-not-fully-specified` (B1-04) | Phần B1a của lớp này reviewer lượt 6 đã đo là sửa xong ở r6 (hình không xanh); r7 không đổi nó. Các biểu hiện cũ (chẩn đoán, A+3) vẫn là chuyển phạm vi sang B1b, không tính là đã vá |
| `collector-stamp-order-conflict`, `schema-patterns-accept-trailing-newline`, `legacy-selector-equivalence-is-impossible` | Không đổi so với r6 |

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
