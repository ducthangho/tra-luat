VERDICT: changes_requested
reviewed_sha: d3bcd6a171644b18d9fd37a185cfb8fc6d641ef4
reviewed_tree: 7176af1b194328a9e8f1c73619f88abe1bd11fe0
spec_sha256: 345520e199ba7072c2bea92b876a3db1877cabce7969f82a379bb078d1dc2e4d

Báo cáo được ghi tăng dần. Kết quả đã đo hiện còn hai finding P2; không đủ điều kiện approve. Reviewer: Codex, provider OpenAI, công cụ thực thi shell cục bộ qua API, transport machine/local. Không tự chứng thực model/effort từ tên tài khoản hay từ prompt; phiên hiện tại không cung cấp phép đo độc lập hai giá trị ấy.

## Định danh đã đo

`git -C src rev-parse HEAD HEAD^{tree}` rc 0: hai OID đúng như trên. `git -C src status --short` rc 0, rỗng. Băm đặc tả đo trước khi đọc bằng `git -C src show a819291bb08af5e72cdd833b86544ea48d97b1fd:ops/specs/wp1494-r1/SPEC.md | sha256sum`: đúng băm trên, rc 0. `sha256sum HANDOFF.yaml`: bac31736440412c589bed469e17cca8b5795e8251d0c5d37cf868bf0a6600a44, rc 0.

Đã đọc quyết định chủ kho bằng GitHub GET comment 7157619068: chủ kho cho lượt 3 vá theo lớp, miễn riêng quan sát dòng 134, ngoài mẫu số/không tín dụng; mọi dòng khác giữ nguyên. Không có thao tác GitHub ghi.

## Hai trục

- Spec: **không đạt** — F02 còn đường transport vượt hạn; F03 chưa đủ kiểm kê/phủ nơi gọi theo nghiệm thu 11.
- Standards/Security: **changes_requested** — chốt hạn chưa chặn được một lời đọc có đệm kéo dài; bằng chứng hồi quy còn chỗ sống/đỏ sai lý do. Baseline, scope và các gate cục bộ đã chạy đều đạt.

## Baseline nghiệm thu — đã đo trước khi review mã

Lệnh `PYTHONDONTWRITEBYTECODE=1 python3 -B out/evidence/baseline.py`, rc 0, dòng dương `BASELINE: DAT`; [toàn bộ kết quả](evidence/baseline.log).

| Điều kiện | Kết quả thực đo |
|---|---|
| B first-parent, không shallow | Đạt; origin/master 98039c79a159e5b9b1cca0e50f1728ba26fdb3c5; shallow=false |
| B merge B1a | Hai parent, subject merge PR #1516 |
| Schema và fixture tại B | 844b5218b6f6844945f5c4c9440f09015d238fe09a60d64b3787c440787e4f46 / ce8595739a1ab2f4a86c9c196255e5f91fb19a9f6d3865df6caa2d66f9970e6d |
| Khối Lệnh kiểm | d9c78e708e18a211b7d8c7309638ffd1c73200578cf3128f9f0fc4275430f24e; 14992 byte, 254 dòng |
| Bốn hàm nguyên văn | 4/4 bằng byte, trích theo dòng AST; băm riêng ở log |
| KHUNG_DAU | committer B 2026-11-25T05:36:53Z; floor 2026-11-21T19:17:00Z; ceil 2026-11-28T19:17:00Z; khớp mã, lease, Mission r109; Issue=1520 |
| Job/upload B | bien-nhan-audit; name và path đúng; T3 cho 11 tên, 11 khoá phân biệt |
| Ba tệp mới tại B | Cả ba vắng, cat-file rc 128 từng tệp |
| Registry tại B | 0 mục canh_tuoi_audit_test |
| Numstat B..H | 4 tệp, +3098/−0: registry +1, workflow +29, module +1019, test +2049; trong trần 6/3500 |

Baseline hợp lệ. Bản sao H/B ở `review-tmp/`, mỗi bản đã đặt `git config core.abbrev 7`. Không fetch vào `src/`; phép first-parent dùng refs của clone được cấp, không chứng nhận remote chưa thay đổi.

## Đo lại lời khai — các phép chạy đã hoàn tất

Mọi lệnh Python dùng `-B`/`PYTHONDONTWRITEBYTECODE=1`; bản H/B là bản sao ngoài `src/`. Lệnh đầy đủ, cwd, rc nằm trong các tệp JSON ở `evidence/`.

| Lời khai / lệnh | Rc đo | Dòng dương hoặc kết quả thực |
|---|---:|---|
| `python3 -B ops/canh_tuoi_audit_test.py` tại H | 0 | `CA: 357/357 dat`; `DOT BIEN: 229/229 bi giet dung ly do`; `TU KIEM PHAN HANG: DAT (5 dot bien)`; `TONG: DAT` |
| `python3 -B .claude/dev/ci_dang_ky_test.py` tại H | 0 | `PHẢN CHỨNG: 1677/1677 đỏ đúng`; `TỔNG: ĐẠT`; 489,228 s |
| Cùng registry tại B | 0 | `PHẢN CHỨNG: 1677/1677 đỏ đúng`; `TỔNG: ĐẠT`; 501,976 s |
| `actionlint -shellcheck /usr/bin/shellcheck .github/workflows/canh-tuoi-audit.yml` | 0 | stdout/stderr rỗng |
| Ruff F trên ba tệp Python H / registry B | 0 / 0 | `All checks passed!` cả hai; delta 0 |
| `git diff --check B HEAD` trên bản H | 0 | stdout rỗng |
| `python3 -B out/evidence/write_set.py` | 0 | `WRITE_SET: 4/4; REGISTRY: exactly one literal MOI item, 0 removed`; `CI_MARKERS: 0 in 4 full files and 7 commit messages` |
| Diff H1..H | 0 | Chỉ `ops/canh_tuoi_audit.py`, `ops/canh_tuoi_audit_test.py` |
| `reviewer_probes.py` nguyên bản | 1 | `TypeError: object of type 'NoneType' has no len()`; đây là lỗi trình in probe sau khi transport nay từ chối trả byte quá hạn |
| `reviewer_probes_co_chan.py` | 0 | Chỉ sửa `len(None)` ở phần in; `PROBES_COMPLETE`; T1 sai miền → `rest_sai_hinh`, tính cuối quá hạn → `het_ngan_sach_danh_gia` |
| `additional_probes.py` nguyên bản | 0 | Issue thiếu body tại W0/W3/W8 đều rc 3 có báo cáo; body null đối chứng rc 0; POST đúng hạn giữ pending |
| `reviewer_mutations.py`, `i2_mutations.py` | 0 / 0 | Runner chạy hết; rc 0 của runner **không** có nghĩa mọi mutant chết. R23–R25/R27/R28 sống ở ca gốc |
| `run_survivors.py` | 0 | Cả năm mutant trên qua 356/357, chỉ chết đúng một ca mới dành riêng; chi tiết dưới đây |
| `oracle_audit.py` nguyên bản | 1 | `StopIteration` khi tra d134 đã rời bảng |
| `oracle_audit_bo_d134.py` | 0 | Chỉ bỏ tên d134 khỏi vòng tra cứu; `D61_MUTANTS 23 UNIQUE_CONDITIONS 32 ALL_TARGETS 32`; tất cả target miền là W0 |

Bản log gốc và biến thể sửa trình in/tra cứu đều được giữ; không ghi đè bằng chứng rc 1. Các con số của executor về suite, registry, lint và probe cũ tái lập được. Chúng chưa chứng minh đủ yêu cầu phủ chốt theo lớp: đột biến độc lập mới đang được phân loại ở phần tiếp theo.


## Finding còn mở

| ID | Mức | Lớp nguyên nhân | Tệp:dòng tại H | Mô tả và tác động | Bằng chứng chạy được | Gợi ý vá (không thi công) |
|---|---|---|---|---|---|---|
| F02 | P2 | `bounded-evaluation-order-dependent` | `ops/canh_tuoi_audit.py:313`, `:1001` | Chốt mới kiểm đồng hồ **sau** `luong.read(65536)`. Với `HTTPResponse` thật, lời gọi này dùng `BufferedReader.read`, có thể chứa nhiều lần đọc nền, mỗi lần dưới socket timeout. Vì vậy một lần thử timeout 30 s vẫn giữ luồng quá cả ngân sách pha; chốt sau read chỉ từ chối khi lời đọc ấy chịu trả. Còn ở GET API, GET kho artifact, PATCH, POST; cùng nguyên nhân qua một hàm chung. Mất khả năng bảo đảm sang pha ghi nhịp tim trước khi watchdog bị timeout. | `python3 -B out/evidence/buffered_deadline.py`, rc 0: `BUFFERED_DEADLINE: 4/4 ORIGINAL_EXCEEDS_30s; 4/4 READ1_CONTROL_STOPS_AT_30s; NO_NETWORK`. Mỗi ca trên H rc 3, đúng `DO:rv2_buffered_*`; JSON thường 1046 byte qua `HTTPResponse`/`BufferedReader` thật, đồng hồ giả: 1046 lần đọc nền × 1 s, timeout truyền 30, chỉ đọc đồng hồ ở 0 và 1046. Đối chứng chỉ đổi cách đọc trên bản tạm dừng ở 30. [Log](evidence/buffered-deadline.log), [script](evidence/buffered_deadline.py). | Đặt kiểm hạn và giới hạn thời gian ở đơn vị I/O thực có thể trả quyền điều khiển; cập nhật timeout theo lượng còn lại, bao phủ mở/gửi/đọc và các caller. `read1` trong probe chỉ là đối chứng phân biệt, chưa phải bản vá hoàn chỉnh. Thêm ca dùng lớp đọc có đệm thật, thay vì chỉ giả mỗi `read` là một thao tác nguyên tử. |
| F03 | P2 | `mutant-oracles-non-discriminating` | `ops/canh_tuoi_audit_test.py:1760`, `:1820`, `:1844`, `:1896`, `:1336` | Sửa được các mutant cũ nhưng chưa đóng lớp trên mã mới: tám mutant N01–N05/N07–N09 qua **357/357**; N06 làm n16 lỗi `HTTPError` rc 4, không phải tín hiệu của ca. Thiếu ca phân biệt biên bằng hạn mỗi lần thử/W0, REST thiếu digest/conclusion và kiểu name/status, caller POST/kho lưu trữ của hạn đọc. 23 mutant D61 vẫn chỉ khai W0, thiếu W2/W7 theo luật nơi gọi. Không cáo buộc 229 dòng hiện có được tính sai; thiếu nằm ngoài bảng ấy. | `python3 -B out/evidence/rv2_mutations.py`, rc 0: 8 SONG, 1 TIN_DUNG_GIA, 3 GIET. `python3 -B out/evidence/rv2_distinguish.py`, rc 0: `RV2_DISTINGUISH: 9/9 GIET DUNG CA DICH` — gốc 0, mutant 3 đúng tên ca, chứng minh không tương đương. `python3 -B out/evidence/rv2_heartbeat_callers.py`, rc 0: `HEARTBEAT_WRITER_CALLERS 64 GIET 64 ORIGINAL_OK 64`. [Kết quả mới](evidence/rv2-mutations.json), [cặp phân biệt](evidence/rv2-distinguish.json), [writer](evidence/rv2-heartbeat-callers.json). | Rà toàn bộ chốt và caller theo nghiệm thu 11, thêm quan sát riêng cho từng nhánh còn hở; giữ phân biệt sống/đỏ sai lý do. Kiểm HTTPError tại biên adapter bằng oracle chủ động của ca; bổ sung ca W2/W7 cho miền dùng chung hoặc đưa ngoại lệ cần thiết lên điều phối, không tự miễn. |

F02 là lỗi hành vi hiện tại; F03 là lỗi nghiệm thu/hồi quy hiện tại. Các mutant trong F03 không khẳng định H đang nhận các REST sai miền: H từ chối đúng trong toàn bộ ca phân biệt mới. Hai finding không dùng D134 để đòi tín dụng hoặc thay đổi quyết định chủ kho.

## Bảng đột biến độc lập — chạy lại R01–R31

Lệnh: `python3 -B out/evidence/reviewer_mutations.py` và `python3 -B out/evidence/i2_mutations.py`, runner rc 0. Mỗi dòng dưới giữ nguyên ca đích lượt 1; mọi ca gốc rc 0. `GIẾT` chỉ ứng với rc 3 và `DO:<đúng tên ca>:`; không coi rc 0 của runner là giết. Neo/thay đầy đủ trong `reviewer-mutants.json` và hai tệp R30/R31; output từng ca trong `R*.json`.

| Mutant | Ca đích gốc → kết quả trên H |
|---|---|
| R01_fresh_becomes_unknown | `n0_nen_fresh` → GIET (rc 3) |
| R02_unknown_becomes_fresh | `n4_gop_kdd_thang_chay` → GIET (rc 3) |
| R03_due_becomes_stale | `n4_s9_p_dat` → GIET (rc 3) |
| R04_stale_becomes_fresh | `n4_gop_do_thang_kdd` → GIET (rc 3) |
| R05_old_obligation | `n4_s3_p_vang` → GIET (rc 3) |
| R06_link_T1 | `n1_lien_ket_created_at` → GIET (rc 3) |
| R07_link_T7 | `n1_lien_ket_cuoi` → GIET (rc 3) |
| R08_final_deadline | `n15_phan_tich_qua_han` → GIET (rc 3) |
| R09_all_or_nothing | `n15_can_ngan_sach` → GIET (rc 3) |
| R10_post_retry | `n8_post_khong_thu_lai` → GIET (rc 3) |
| R11_patch_retry | `n8_patch_khong_thu_lai` → GIET (rc 3) |
| R12_pending_deleted | `n8_giao_lai_gian_doan` → GIET (rc 3); `n8_cho_bao_khong_bi_bo` → GIET (rc 3) |
| R13_pending_replaced | `n8_cho_bao_khong_bi_thay` → GIET (rc 3) |
| R14_reconciliation_bot | `n8_gia_danh` → GIET (rc 3) |
| R15_reconciliation_since | `n8_doi_soat_cua_so` → GIET (rc 3) |
| R16_shared_heartbeat | `n8_tu_kiem_truoc_patch` → GIET (rc 3); `n8_tu_kiem_truoc_patch2` → GIET (rc 3) |
| R17_zip_expansion | `n2_giai_nen_t2_tren` → GIET (rc 3); `n2_giai_nen_t5_tren` → GIET (rc 3) |
| R18_zip_entries | `n2_muc_t2_tren` → GIET (rc 3); `n2_muc_t5_tren` → GIET (rc 3) |
| R19_zip_total | `n2_tong_vuot` → GIET (rc 3) |
| R20_workflow_step | `n10_buoc4_if` → GIET (rc 3) |
| R21_workflow_permission | `n10_quyen` → GIET (rc 3) |
| R22_chunk_read_removed | `n1_j_vuot_tran` → GIET (rc 3); `n1_s_vuot_tran` → GIET (rc 3) |
| R23_real_redirect_guard | `n1_s_khong_auth` → SONG (rc 0); `n1_r_qua_3` → SONG (rc 0) |
| R24_main_exit_zero | `n9_ma_thoat` → SONG (rc 0) |
| R25_real_timeout_ignored | `n1_han_goi` → SONG (rc 0); `n15_kep_timeout` → SONG (rc 0) |
| R26_api_auth_removed | `n0_nen_fresh` → SONG (rc 0); `n1_s_khong_auth` → GIET (rc 3) |
| R27_last_link_event | `n1_lien_ket_event` → SONG (rc 0); `n1_lien_ket_cuoi` → SONG (rc 0) |
| R28_U6_attempt_removed | `n1_u6` → SONG (rc 0); `n1_chua_xong` → SONG (rc 0) |
| R29_heartbeat_reader_bypass | `n8_mien_m4` → GIET (rc 3) |
| R30_I2_unknown_promoted_dat | `n4_s6` → GIET (rc 3) |
| R31_I2_fresh_with_old_obligation | `n4_s3_p_vang` → GIET (rc 3) |

Tổng cặp ca gốc/đột biến R: {'GIET': 31, 'SONG': 10, 'TIN_DUNG_GIA': 0}. Đây là số **cặp**, không phải mẫu số 229 của executor.


| Mutant sống ở ca gốc | Quét toàn 357 ca H | Ca mới duy nhất giết đúng |
|---|---|---|
| R23 | 356 đạt, 1 đỏ rc 3 | `n16_transport_that` |
| R24 | 356 đạt, 1 đỏ rc 3 | `n9_main_ma_thoat` |
| R25 | 356 đạt, 1 đỏ rc 3 | `n16_transport_that` |
| R27 | 356 đạt, 1 đỏ rc 3 | `n1_lien_ket_cuoi_event` |
| R28 | 356 đạt, 1 đỏ rc 3 | `n1_u6_run_attempt` |

Lệnh `python3 -B out/evidence/run_survivors.py`, rc 0; [log/cặp ca](evidence/survivor-results.json). R26 là đối chứng quan trọng: `n0_nen_fresh` vẫn sống, nhưng `n1_s_khong_auth` giết đúng bằng nhật ký Authorization. Không gọi một ca đích không nhạy là bằng chứng đường sản phẩm còn hở nếu ca khác thực sự quan sát đúng đường ấy.

## Đối chiếu lượt 1 và săn toàn lớp

| Finding lượt 1 | Đúng một nhãn | Phép đo và kết luận |
|---|---|---|
| F01 — `rest-response-domain-incomplete` | **ĐÃ SỬA ĐÚNG LỚP** | Năm probe T1 cũ đều `khong_do_duoc/rest_sai_hinh`; thêm thiếu digest, thiếu conclusion, artifact name số và job status số đều bị H từ chối đúng. Issue thiếu body W0/W3/W8 đều rc 3 có báo cáo; body null đối chứng rc 0. Chưa tìm thấy đường cùng lớp còn hở trong sản phẩm; lỗ ca phân biệt thuộc F03. |
| F02 — `bounded-evaluation-order-dependent` | **VÁ HỜ** | Tính S cuối ở 600/600,5 s, phân tích W0, D14 và kết quả POST hoàn tất muộn nay bị chặn; N10–N12 giết đúng. Nhưng `_mot_lan` vẫn bị giữ trong một `HTTPResponse.read`: cả bốn đường GET API/GET kho/PATCH/POST vượt timeout vật lý 30 s tới 1046 s. Không đổi lớp chỉ vì đã đóng ba probe cũ. |
| F03 — `mutant-oracles-non-discriminating` | **VÁ HỜ** | R22 và R23–R25/R27/R28 nay có ca thực sự giết; LIÊN KẾT đã thêm T7; D134 bỏ đúng phạm vi miễn. Tuy nhiên tám đột biến mới sống 357/357, một đỏ sai lý do và D61 thiếu W2/W7. Những chỗ còn hở đều nằm trong lớp kiểm kê/quan sát/nơi gọi mà lượt trước yêu cầu rà toàn bộ. |

Phạm vi quét theo lớp trong toàn bản vá:

| Lớp | Mọi đường liên quan đã rà | Đường còn hở / giới hạn đo |
|---|---|---|
| REST domain | `_j` hình JSON và dấu GitHub; `_liet_ke` D1/D3/D4/D14, số đếm, ID, phân trang; `HINH_D1`; `_hinh_rest` run/job/artifact tại T1; `_lech_lien_ket` T1/T7 và U6; `_b64`, D6/D7; `cau_master` D8/D9; `_hinh_issue` W0/W3/W8; `_khop` D13/D14; context run ID/attempt; bộ đọc/ghi heartbeat | Không tìm thấy lỗi sản phẩm cùng lớp F01 qua các fixture đã đo. T7 giữ chốt định danh/U6, không phải một bản sao đầy đủ của T1. Thiếu ca phân biệt trên bốn nhánh mới của `_hinh_rest` đã được ghi F03, không nhầm thành F01 chưa sửa. |
| Hạn/thứ tự | Sắp xếp lượt và artifact; cache D6/D7; `_goi` trước lần gửi/chờ, GET retry và timeout kẹp; `_mot_lan` open/send/read; W0 toàn phần và trừ thời gian; hạn đánh giá sau tính cuối kể cả lưới an toàn; S1 xóa sha/không tiến dong_den; `_buoc_ghi` D8/D9/W2/W3/W5/W6/W7/W8; D14 sau `_khop`; trần byte và ZIP | Logic trả kết quả sau hoàn tất đã đóng các đường cũ. Đường còn hở là thời gian giữ luồng bên **trong** open/read của adapter: đã tái hiện cụ thể read có đệm, dùng chung cho API/kho/GET/PATCH/POST. Không chứng nhận DNS/TLS/connect/write/header bằng mạng thật. |
| Oracle/caller | Toàn 229 mutant chi tiết; 41 cặp R; các chốt mới H1..H về T1/body/timeout/adapter/main/LIÊN KẾT/U6; phân hạng gốc/đỏ sai lý do; hàm chung phân trang D1/D14, tải J/S, ZIP T2/T5, heartbeat W0/W2/W7; workflow 18 mệnh đề và hai mutant bổ sung; danh sách tương đương/D134 | D1/D14, d107 J/S, d108/d109 T2/T5, d96 W2/W7, LIÊN KẾT T1/T7 có ca đích đúng. Hở đã đo: N01–N09 (trừ N06 là đỏ sai lý do), các miền D61 chỉ W0, và mô hình read giả không bao phủ BufferedReader của F02. Chưa chứng minh mọi chốt độc lập ngoài các đột biến đã chạy đều đầy đủ; không dùng “229/229” làm chứng minh ấy. |

## Đối chiếu lớp từ review ĐẶC TẢ lượt 1–3

Đã đọc các JSON `wp1494-spec-review-{1,2,3}.json` từ ref được cấp và bảng Thay đổi của SPEC; bản sao ở `evidence/`. Lượt 4 đặc tả không có finding. Các nhãn dưới áp vào **mã H và bằng chứng kiểm thử H**, không dùng việc đặc tả đã approve để suy ra mã đạt. Đây là lượt review mã **thứ 2** theo chính hồ sơ `src-reviews/luot-1` và yêu cầu hiện tại; bốn lượt review đặc tả là bộ đếm khác.

| Lớp | Đúng một nhãn | Bằng chứng đo / giới hạn |
|---|---|---|
| `notification-dedup-before-delivery` | **ĐÃ SỬA ĐÚNG LỚP** | R12/R13 giết đúng: pending không bị xóa/thay. R14/R15 giết đúng đối soát bot/since. Các trace `n8_giao_lai_*`, phản hồi mất, D14, đổi Issue chạy đạt. POST hoàn tất đúng hạn 180 s vẫn giữ pending. Đổi Issue bỏ pending cũ và báo trạng thái hiện tại là lựa chọn runbook đã công khai, không hứa giao lại tin cũ. |
| `write-retries-violate-delivery-contract` | **ĐÃ SỬA ĐÚNG LỚP** | R10/R11 giết bằng đếm POST/PATCH vật lý; toàn trace giữ POST ≤1, PATCH ≤2. N07 gốc POST=1 khi phản hồi quá hạn; không phát lại trong lượt. |
| `b1-consumer-contract-mismatch` | **ĐÃ SỬA ĐÚNG LỚP** | Băm GHIM-B1A đúng; 4 hàm nguyên văn; `hinh 120/120 · ngu nghia 118/118 · ghim 2/2`. Ca byte hỏng T2/T5 và tiêm ngoại lệ theo bảng mục 3 chạy đạt. D134 ngoài mẫu số theo quyết định riêng, không dùng để khẳng định hành vi mutant tương đương toàn phần. |
| `consumer-freshness-anchor-unverified` | **ĐÃ SỬA ĐÚNG LỚP** | R06/R07 giết; R27/R28 chết đúng ca mới. T1/T7 ràng buộc chín trường LIÊN KẾT; U6 bốn trường; sai anchor thắng đỏ con; rerun/dispatch không làm tươi giả. `oracle_audit_bo_d134.py` chạy ca T7 bổ sung đạt gốc/đỏ mutant. |
| `freshness-forgets-overdue-obligations` | **ĐÃ SỬA ĐÚNG LỚP** | R05 và R31 giết; `n4_r_khung_cu`, đóng tay, dong_den tiền tố, các S1–S9 và I2 chạy đạt. Đóng tay được loại trước lịch đọc. |
| `bounded-evaluation-order-dependent` | **VÁ HỜ** | Lịch tất định/cạn tất-cả-hoặc-không/final CPU đã đúng trong các ca; còn F02 read có đệm. N01/N07/N08/N09 chỉ ra lỗ test trên cùng lớp. |
| `heartbeat-value-domain-incomplete` | **ĐÃ SỬA ĐÚNG LỚP** | Mã dùng chung bộ kiểm tại W0/W2/W7; 32 miền đọc, ngữ cảnh run và ca đọc lại roundtrip đạt; 64 ca writer reviewer gốc đều từ chối đúng mã trước PATCH. Thiếu đưa các cặp writer vào bảng nghiệm thu là F03, không có bằng chứng H hiện sinh/nhận heartbeat ngoài miền. |
| `workflow-step-controls-unconstrained` | **ĐÃ SỬA ĐÚNG LỚP** | 18 mệnh đề checker, hai mutant bổ sung; R20/R21 giết đúng. Tập khóa/quyền/job/bước/with/env và giá trị đóng. Duplicate YAML cùng giá trị được safe_load gộp nhưng actionlint từ chối; không coi checker ngữ nghĩa là parser YAML có kiểm duplicate. |
| `mutant-oracles-non-discriminating` | **VÁ HỜ** | F03: các cặp cũ đã vá, còn tám sống + một đỏ sai lý do và thiếu caller miền writer; tất cả có cặp phân biệt dựng được, trừ miễn đúng D134. |
| `unbounded-artifact-expansion` | **ĐÃ SỬA ĐÚNG LỚP** | R17/R18/R19 giết: trần byte giải nén, số mục và cộng dồn; d108/d109 T2/T5 đều giết; biên bằng/trên và S1 tổng chạy đạt. Fixture ZIP thường, trần nhỏ tiêm vào; không dựng payload gây thoát thư mục hay ép cạn bộ nhớ. Lỗi thời gian đọc mạng riêng ở F02. |
| `markdown-state-table-column-drift` | **KHÔNG ÁP DỤNG** | Finding về trình bày bảng đặc tả, không phải luồng mã. Không có thay đổi Markdown trong bốn tệp; trạng thái mã kiểm qua S1–S9/I2. |
| `merged-misreported-as-landed` | **KHÔNG ÁP DỤNG** | Finding về lời khai trạng thái tiền nhiệm trong đặc tả. Write set không có hồ sơ land; review này chỉ chứng nhận exact H/tree và baseline được cấp, không tuyên bố H đã push/merge/land. |

## Bảng đột biến mới trên H1..H và caller còn thiếu

`python3 -B out/evidence/rv2_mutations.py` rc 0. Neo/thay chính xác: [rv2-mutants.json](evidence/rv2-mutants.json). Tám mutant sống được quét **toàn 357 ca**; N06 cũng quét toàn bộ và chỉ có một ca đỏ sai lý do. Mọi ca gốc trong bảng rc 0.

| ID / thay chốt | Ca đã commit được chọn | Kết quả mutant tại ca ấy | Quét rộng / ca phân biệt độc lập |
|---|---|---|---|
| N01_attempt_equal — Nới >= thành > ở hạn mỗi lần thử | `n15_vong_doc_qua_han` | SONG (rc 0) | 357/357 đạt; `rv2_N01`: gốc 0 → mutant 3 GIẾT |
| N02_digest_presence — Cho digest vắng như digest null | `n1_t1_mien_art_digest` | SONG (rc 0) | 357/357 đạt; `rv2_N02`: gốc 0 → mutant 3 GIẾT |
| N03_artifact_name — Bỏ kiểm tên artifact là chuỗi | `n1_t1_mien_art_khac` | SONG (rc 0) | 357/357 đạt; `rv2_N03`: gốc 0 → mutant 3 GIẾT |
| N04_run_conclusion_presence — Cho conclusion vắng như conclusion null | `n1_t1_mien_run_conclusion` | SONG (rc 0) | 357/357 đạt; `rv2_N04`: gốc 0 → mutant 3 GIẾT |
| N05_job_status — Bỏ kiểm job.status là chuỗi | `n1_t1_mien_job_chuoi` | SONG (rc 0) | 357/357 đạt; `rv2_N05`: gốc 0 → mutant 3 GIẾT |
| N06_http_error_adapter — Cho HTTPError lan khỏi adapter | `n16_transport_that` | TIN_DUNG_GIA (rc 4) | 356/357 đạt; n16 lỗi HTTPError rc 4; `rv2_N06`: gốc 0 → mutant 3 GIẾT |
| N07_post_read_deadline — Miễn POST khỏi chốt hạn đọc | `n15_vong_doc_qua_han` | SONG (rc 0) | 357/357 đạt; `rv2_N07`: gốc 0 → mutant 3 GIẾT |
| N08_storage_read_deadline — Chỉ kiểm hạn đọc cho host API, bỏ caller kho | `n15_vong_doc_qua_han` | SONG (rc 0) | 357/357 đạt; `rv2_N08`: gốc 0 → mutant 3 GIẾT |
| N09_W0_equal — Nới >= thành > tại hoàn tất W0 | `n15_w0_phan_tich_qua_han` | SONG (rc 0) | 357/357 đạt; `rv2_N09`: gốc 0 → mutant 3 GIẾT |
| N10_final_equal — Nới >= thành > tại tính cuối DG | `n15_tinh_cuoi_qua_han` | GIET (rc 3) | Không cần quét rộng; đúng TinHieuChotCa |
| N11_W0_check_removed — Bỏ kiểm hạn toàn W0 | `n15_w0_phan_tich_qua_han` | GIET (rc 3) | Không cần quét rộng; đúng TinHieuChotCa |
| N12_D14_check_removed — Bỏ kiểm hạn sau khớp D14 | `n15_d14_khop_qua_han` | GIET (rc 3) | Không cần quét rộng; đúng TinHieuChotCa |


Cặp phân biệt mới: `python3 -B out/evidence/rv2_distinguish.py`, rc 0, `RV2_DISTINGUISH: 9/9 GIET DUNG CA DICH`. Quan sát cụ thể:

- N01: EOF hoàn tất đúng 30 s; H từ chối ba lần, mutant `fresh` sau một lần. Biên chặt là quan sát, không phải chỉ “hàm có gọi đồng hồ”.
- N02/N03/N05: H T1 `rest_sai_hinh`, mutant T1 `dat` và tổng `fresh`. N04: T1 đổi sai sang `dat`, dù một chốt phía sau vẫn giữ tổng khong_do_duoc; vì vậy phải quan sát T1 riêng.
- N06: ca commit n16 để HTTPError lan ra rc 4. Ca reviewer bắt đúng HTTPError ở biên adapter rồi chốt “phải trả mã HTTP”, mutant rc 3 đúng tên. Đây là bằng chứng phân biệt, không cộng tín dụng vào 229 dòng executor.
- N07: H POST=1, 40 s, pending còn, ack null, exit 3; mutant POST=1, 80 s, pending bị ack, exit 1. Lỗi mutant là dùng kết quả của lần thử quá 30 s, dù chưa hết ngân sách pha 180 s.
- N08: bỏ hạn ở caller kho artifact làm T2 từ khong_do_duoc sang dat, tổng fresh; H từ chối. Mutant giới hạn chốt vào host API, không dựa vào tên fixture cụ thể.
- N09: W0 xong đúng 180 s; H mã d10_loi:het_gio, mutant moi. Cả hai vẫn exit 3/PATCH=0 vì chốt ghi sau đó; quan sát tổng mã thoát sẽ không phân biệt được.

D61 có 23 điểm mã cho 32 điều kiện (m1,m2,m4…m33; m3 có D62). Reviewer đặt cùng 32 dict dữ liệu thường tại biên `_ghi_than` của **W2 và W7** rồi chạy chính từng mutant D61: 64/64 gốc rc 0; 64/64 mutant rc 3 với `DO:rv2_W2_mien_m*` hoặc `DO:rv2_W7_mien_m*`. Không tiêm đường dẫn hay giải nén ra ngoài cây. Đây là kiểm thử trực tiếp biên caller, không khẳng định mỗi dict ngoài miền có thể tự phát sinh từ một lượt sản xuất hợp lệ. [64 cặp và quan sát](evidence/rv2-heartbeat-callers.json).

Bảng đã commit vẫn thật sự 229/229 giết đúng trên những ca nó khai. Các mutant sống/đỏ sai lý do trên đây là phép mở rộng độc lập để kiểm tính đầy đủ; không thay mẫu số một cách ngầm định. D134 giữ “tương đương theo schema” theo quyết định chủ kho, ngoài mọi mẫu số giết thật.

## Đầu vào thù địch — đường xử lý và độ phủ

Chỉ mô tả hướng dữ liệu; các phép chạy dùng REST/ZIP giả thường, không có payload nhằm thoát cây thư mục, socket thật hay gọi GitHub ghi.

| Hướng | Đường mã xử lý | Ca đã commit đã chạy / phép bổ sung |
|---|---|---|
| Trang lặp, thiếu trang, đổi thứ tự, total_count nói sai | `_liet_ke:366` giới hạn 10 trang, so độ dài/tổng cuối, ID duy nhất; `_danh_gia:656` sắp ID; T5 sắp artifact | `n1_hai_trang`, `n1_total_count`, `n1_trung_id`, `n4_s1_khong_tron`, `n15_thu_tu_goi`, D14 `n8_doi_soat_khong_tron`. Bổ sung `pagination_ordinary.py` rc 0: lặp Link tự nó dừng ở 10 GET/khong_tron; thiếu trang → tong_lech. Không thể suy ra API không giấu phần tử nếu cả dữ liệu và metadata cùng nói dối nhất quán. |
| created_at sai dạng, ngày không tồn tại, vắng | `gio:189`, `HINH_D1`, lựa chọn khung trước T1 | `n1_d1_hinh_created_at`, `n5_lien_ket_created_at`; `ordinary_inputs.py` thử ngày không tồn tại, dạng sai, null đều KDD; `pagination_ordinary.py` thử thiếu khóa cũng KDD. |
| Rerun attempt, dispatch lọt D1, head_sha thay khi đọc D2 lần cuối | `HINH_D1`; LIÊN KẾT T1/T7; U6 `_t7:582`; tuổi từ created_at gốc | `n5_chay_lai_khong_lam_tuoi`, `n5_dispatch`, `n5_attempt_thap`, `n1_lien_ket_cuoi_head_sha`, `n1_u6_run_attempt` và cả bốn trường U6. R27/R28 được ca mới giết đúng. |
| Comment giả B2_SU_KIEN, body Issue bị sửa, heartbeat cũ/hỏng/vắng | `_khop:842` yêu cầu bot và đúng một dòng sự kiện; D14 so sự kiện/cửa sổ; `_hinh_issue`, `doc_nhip_tim:800`, `_ghi_than` đọc lại bằng từng ký tự | `n8_gia_danh`, `n8_doc_lai_comment_login`, `n8_hai_dong_su_kien`, `n8_doc_lai_than`, `n8_state`, `n8_hai_dong`, `n8_json_hong`, `n8_qua_24h`, `n8_giao_lai_*`, 32 ca miền. Sửa tay đúng hoàn toàn schema không được xác thực chữ ký: đây là body lưu trạng thái theo đặc tả, không phải bằng chứng tác giả. |
| Thiếu X-GitHub-Request-Id; chuyển hướng HTTP/host khác | `_j:346` từ chối thiếu dấu; `_tai:388` chỉ nhận 302 có dấu từ API, Location phải HTTPS, tối đa ba chặng; `_goi` chỉ gắn token cho hostname api.github.com; adapter chặn tự redirect | `n1_j_khong_dau`, 403 có/không dấu, `n1_r_khong_https`, `n1_r_qua_3`, `n1_r_dung_3`, `n1_s_khong_auth`, `n16_transport_that`. Host HTTPS khác là **kho lưu trữ được phép theo lớp S**, nhận 200 không Authorization; không mô tả nhầm thành “mọi host lạ đều bị từ chối”. Chưa đo mạng thật. |
| Content-Length sai, nhiều mục ZIP, tổng giải nén lớn | `_mot_lan` chặn byte tải; `_tai` so length nếu có; `_tho_zip:228` đếm mục/byte thực trước giữ; cộng dồn → S1 | `n1_s_ngan`, `n1_s_vuot_tran`, `n1_j_vuot_tran`, `n2_t2_hai_tep`, `n2_muc_t2_*`/`t5_*`, `n2_giai_nen_t2_*`/`t5_*`, `n2_tong_vuot`; R17–R19 giết. Zip không được extract ra filesystem trong đường kiểm này. |
| Đồng hồ đúng hạn; POST hoàn tất muộn | `_goi`, `_mot_lan`, chốt cuối `chay`, `_buoc_ghi`, D14; pending chỉ ack sau xác nhận | `n15_han_cuoi_danh_gia`, `n15_tinh_cuoi_qua_han`, `n15_han_cuoi_ghi`, `n15_d14_khop_qua_han`; probe POST ở đúng 180 s giữ pending. N01/N07/N09 bổ sung biên mà ca commit chưa phân biệt; F02 còn lỗi thời gian giữ trong read có đệm. |
| Workflow thêm khóa/bước/quyền | `kiem_hinh` và các `_khoa`/`_lech` trong test: danh sách cho phép đến từng bước/with/env | Toàn `n10_*`, 18 mutant mệnh đề + hai mutant bổ sung, R20/R21 và actionlint. Thêm if/continue-on-error/permission hoặc đổi số/thứ tự bước đều đỏ đúng. Duplicate khóa nguồn cùng giá trị chỉ actionlint bắt; giới hạn này được ghi rõ. |

## BẢNG SĂN chủ động

| Hướng | Giả thuyết | Phép đo đã chạy | Kết quả |
|---|---|---|---|
| 1. Nền/định danh | HEAD/tree, GHIM hoặc mốc khởi đầu sai khiến review vô nghĩa | baseline.py, sha256, first-parent, AST giữ byte | Đạt toàn bộ baseline; không blocked vì nền |
| 2. REST miền mới | Vá năm mẫu cụ thể vẫn bỏ thiếu khóa/kiểu nhánh cạnh | Probe cũ, N02–N05, ca rv2_N02–N05 | Mã H đúng; ca commit không nhạy với bốn chốt riêng → F03 |
| 3. I2 và bốn trạng thái | Unknown nâng dat hoặc fresh khi còn nợ cũ | R01–R05, R30/R31 và S1–S9 | Giết đúng; không thấy đường false-green này ở H |
| 4. D1↔D2/U6 | Chỉ khóa D2 đầu hoặc updated_at, bỏ event/attempt cuối | R06/R07/R27/R28; quét 357 | Ca mới đóng các mutant cũ; T7 phân biệt đúng |
| 5. Hạn sau tính cuối | CPU cuối/W0/D14 quá hạn vẫn nhận kết quả | N09–N12, probe cũ, POST đúng 180 | Các chốt sản phẩm đúng; biên bằng W0 thiếu hồi quy |
| 6. Hạn bên trong read | Đọc có đệm chứa nhiều lần I/O, chốt sau read đến quá muộn | buffered_deadline.py, 4 phương thức/caller, đối chứng read1 | Tái hiện F02 ở H: 1046 s giả cho timeout 30 |
| 7. Caller của hạn đọc | Chỉ GET API được test, bỏ POST hoặc kho vẫn suite xanh | N07/N08, toàn 357, ca riêng | Cả hai sống toàn suite; ca riêng giết đúng → F03 |
| 8. Pending/dedup/retry | Ghi ack trước giao, xóa pending, retry POST/PATCH | R10–R15, multi-run n8, additional_probes | Các mutant giết đúng; không có đường pending bị xóa ở H trong trace đã đo |
| 9. Miền chung reader/writer | Chỉ W0 phân biệt miền, writer thiếu bằng chứng caller | R16/R29, audit D61, 64 cặp W2/W7 | Mã H chặn đủ 64; nghiệm thu thiếu cặp writer → F03 |
| 10. Tài nguyên ZIP | Trần chỉ hậu kiểm sau giải nén hoặc không cộng dồn | R17–R19; ca dưới/bằng/trên T2/T5 | Giết đúng; không thấy lỗi cấp phát kiểu đó |
| 11. Adapter/main | Fake transport che nhánh thật, raw exception bị nhận tín dụng | R23–R25, N06, n16/main, bộ tự kiểm 5 mutant | R23–R25 đã có target; N06 đỏ sai lý do, ca độc lập phân biệt được |
| 12. Workflow/scope | Khóa thừa, thêm quyền, registry hoặc message bỏ CI | n10, R20/R21, actionlint, write_set.py | Cấu trúc bị chặn; đúng bốn tệp/registry một mục; 0 dấu bỏ CI |
| 13. Phân trang/ngày | Vòng Link hoặc ngày không thật làm treo/xanh | pagination_ordinary.py, ordinary_inputs.py | 3/3 fixture bổ sung bị từ chối; lặp dừng 10 trang |

## Phán chín lựa chọn lượt 1

| Lựa chọn | Phán ở lượt 2 |
|---|---|
| 1 — D134/KeyError | Chấp nhận bỏ quan sát/mẫu số theo [quyết định chủ kho](https://github.com/ducthangho/tra-luat/issues/1172#issuecomment-7157619068). Nhãn “tương đương theo schema” là phạm vi quan sát được miễn: D5 luôn 0; không suy rộng mutant không đổi mọi hành vi, vì nhánh ok:false đúng hình vẫn có thể đổi sang KeyError/S1. Không dùng nó làm GIẾT. |
| 2 — 23 mutant D61/32 điều kiện | Chấp nhận gộp điểm mã thành 23 khi đủ 32 target đọc; không chấp nhận dùng số đó để miễn caller writer. 64 cặp W2/W7 dựng được và giết đúng. |
| 3 — Gộp hàm chung | Chấp nhận nguyên tắc một mutant/điểm mã. H đã thêm T7 cho d01_02_head_sha; D1/D14, J/S, T2/T5, d96 W2/W7 đạt các cặp đã khai. D61 và hạn đọc còn thiếu phủ caller, F03. |
| 4 — Hai mutant D82/YAML duplicate | Chấp nhận; 18+2 mutant checker chết đúng. Duplicate cùng giá trị là giới hạn safe_load; actionlint bắt rc 1. Không đòi thay parser ngoài hợp đồng hiện hành. |
| 5 — TimeoutError → transport_nem | Chấp nhận mã hóa nguyên hàm; `het_gio` dành chốt pha. Không miễn thời gian vật lý: F02 vẫn mở dù phân loại cuối đúng. |
| 6 — thong_bao_hoan chỉ khi sự kiện khác | Chấp nhận; pending cùng loại/cùng bộ đang được giao lại không phải một sự kiện khác bị hoãn. Các ca giao lại và không thay pending chạy đạt. |
| 7 — D2 đầu hỏng, T7 khong_danh_gia | Chấp nhận khi không có đầu vào để so U6; ordinary_inputs tái lập T1 KDD/http_github:403, T7 khong_danh_gia, tổng KDD/exit 1. |
| 8 — Thiếu SPEC B1a trong cây, ghim 2/2 | Chấp nhận đúng ngoại lệ nghiệm thu 3. Reviewer lấy object d1b08c…, băm khối và so 4 hàm bằng byte. Không nói test này tự khóa nguyên văn nếu object không nằm trong cây. |
| 9 — Thiếu transport_that/main | Các đường R23–R25 đã đóng bằng n16/main mới, quét 357 cho đúng một target mỗi mutant. Lớp rộng vẫn còn HTTPError oracle N06 và BufferedReader F02; không đóng cả lớp từ ba mutant cũ. |

## Ba câu hỏi executor

1. **Hai sửa một dòng vào script reviewer:** chấp nhận làm phép tái đo có ghi rõ. Chốt `len(None)` chỉ bảo vệ trình in; bỏ tra `d134` chỉ áp quyết định miễn đã xác minh. Giữ cả script nguyên bản, rc 1 và script sửa, rc 0; không đổi assertion hoặc tính thêm một lần giết. Hai script sửa không thay thế yêu cầu suite commit.
2. **R23–R25/R27/R28 chỉ chết ở ca mới:** chấp nhận **cho các mutant ấy**. “Chính ca đích” đòi ca khai rõ, gốc đạt, mutant đỏ vì `TinHieuChotCa` đúng tên và đúng quan sát; không bắt buộc một ca chọn thiếu nhạy từ lượt trước phải mãi là target. Ca gốc sống cho thấy nó không chạm chốt, không tự chứng minh đường mã còn hở. Quét toàn 357 xác nhận từng target mới thực sự giết. F03 tiếp tục mở vì các chốt/caller mới khác, không vì phủ nhận năm ca này.
3. **D61 chỉ W0 do người ghi không tự sinh ngoài miền:** không đủ đáp ứng luật nơi gọi đã đóng băng. Có thể thử dữ liệu thường ngay tại biên gọi chung `_ghi_than`, như 64 cặp reviewer đã đo; đây là kiểm hợp đồng người ghi và hồi quy guard. Không yêu cầu cố tạo một lượt sản xuất tự sinh dữ liệu bất khả. Nếu muốn miễn các cặp này phải là quyết định điều phối rõ phạm vi; miễn D134 không bao trùm D61.

## KHÔNG ĐO ĐƯỢC / không được chứng nhận bởi lượt review này

- Không chạy mạng thật, GitHub Actions, workflow_dispatch, comment/Issue thật; không đo khả năng chủ kho nhận thông báo. Probe F02 dùng `HTTPResponse`/`BufferedReader` thư viện thật và đồng hồ/nguồn byte giả, không phải số giây treo mạng thật. Nó chứng minh cấu trúc lời đọc vượt hạn giữa hai lần kiểm đồng hồ; không chứng nhận DNS/TLS/connect/upload/header.
- Chạy trên Linux/Python **3.13.18**, PyYAML **6.0.3**, jsonschema **4.26.0**, actionlint **1.7.7**, ShellCheck **0.9.0**, Ruff **0.15.15**. Chưa chạy Python 3.12 của workflow hoặc Windows.
- Windows M3 được SPEC/lease phân loại required; lease ghi chưa miễn. Chưa có bằng chứng trong tài liệu được review về dòng chủ kho `windows: <H> mien` neo H cuối hoặc một lượt Windows được cấp và đã chạy. Đây là gate riêng chưa được chứng nhận, không tự miễn từ Linux xanh; không mở một finding mã giả tạo thay cho gate này.
- Không chạy `ci_dang_ky_test.py --chay`, full M9, `scripts/tl.py --selftest`, CI PR hay phép đo sau merge của nghiệm thu 14. Registry mặc định và bộ test mới đã chạy trực tiếp; không gọi chúng là toàn bộ CI. Lượt M9/CI có trần riêng trong lease.
- Không chứng thực served model/effort từ tên model trong yêu cầu, tên nhánh, file lease hoặc tài khoản. Bề mặt công cụ của phiên là Codex service/API có shell cục bộ; không tự đổi thành chứng nhận `codex_cli` mà lease ghi. Nếu điều phối cần biên nhận danh tính runtime, phiên này không cung cấp phép đo độc lập ấy.
- Không xác minh lại toàn bộ trạng thái ref/lease sống trên remote; first-parent dùng các ref đầy đủ được cấp. Đã đọc riêng quyết định chủ kho bằng GitHub GET; không có GitHub write. Chưa push/merge/land H và review này không cấp các trạng thái ấy.
- Không thực hiện bốn lượt review đặc tả như bốn lượt review mã. Hồ sơ mã lượt 1 là nền đối chiếu bắt buộc ở đây; các lớp đặc tả được đánh giá riêng như bảng trên.

## Chứng cứ chỉ đọc và trạng thái kết thúc

`readonly-final.json`: trước **18169** tệp, sau **18169** tệp; thêm **0**, xóa **0**, đổi SHA-256 **0**, symlink **0**. Snapshot gồm cả `.git`, tracked, untracked và ignored. `git -C src status --short --untracked-files=all` rc 0, output rỗng; HEAD/tree giữ nguyên exact H/tree đầu báo cáo. Băm SPEC và HANDOFF đo lại đều giữ nguyên. Không sửa `src/`, không commit/push, không GitHub write, không dispatch.

Suite chi tiết chạy rc 0 và có đúng **229 tên mutant khác nhau**, khớp hoàn toàn 229 hàng tính tín dụng của HANDOFF; hàng thứ 230 của HANDOFF là D134 không tính. Doctrine scan và ADR scan trên bản H cùng rc 0; scope/registry/CI-marker như bảng đo lại. Hai diff chỉnh helper được giữ ở `probe-helper.diff` và `oracle-helper.diff`, mỗi diff đúng một dòng.

Kết luận exact H: **changes_requested**, hai P2 mở **F02, F03**; F01 **ĐÃ SỬA ĐÚNG LỚP**, F02/F03 **VÁ HỜ**. Baseline hợp lệ nên không dùng `blocked` thay cho finding. Gợi ý vá trong báo cáo không cấp thêm executor attempt: hồ sơ xác định đã dùng 3/3 và lớp oracle đã tái diễn; bước quyết định tiếp theo thuộc điều phối/chủ kho theo §12, không phải reviewer tự thi công hoặc tự miễn yêu cầu.
