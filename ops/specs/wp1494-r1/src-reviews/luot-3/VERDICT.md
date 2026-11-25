VERDICT: changes_requested
reviewed_sha: c524d1233c2709679e31cd972711d4b8d5534fa8
reviewed_tree: 0dc451fddbfc48217c6fac9fb46187a0f55fdc0f
spec_sha256: 345520e199ba7072c2bea92b876a3db1877cabce7969f82a379bb078d1dc2e4d

Review mã nguồn lượt 3/3, cuối; executor attempt 4/4 theo Review Rescue. **Còn hai finding P2, thuộc hai lớp nguyên nhân. Không approve.** F03 tái diễn dưới dạng mất phủ do đổi đầu vào ca; F04 là lỗi thực thi trần giải nén tổng, phát hiện khi săn toàn lớp. Không dùng rủi ro pha mở kết nối đã miễn để chặn verdict.

Reviewer: Codex / OpenAI; công cụ thực thi cục bộ qua API; transport machine. Độc lập với executor, không dùng sub-agent. Model/effort phục vụ thực tế không có metadata độc lập để xác nhận; không suy từ tài khoản GitHub hay lời chỉ định trong prompt. Thực thi: Linux, Python 3.13.18, PyYAML 6.0.3, jsonschema 4.26.0, Ruff 0.15.15, actionlint 1.7.7, ShellCheck 0.9.0. Sandbox workspace-write, approval never; socketpair bị từ chối. Không sửa `src/`, không commit/push/GitHub ghi/dispatch.

## Hai trục

| Trục | Kết luận |
|---|---|
| Spec | **Không đạt.** RV3-F03 vi phạm đầu vào nghiệm thu 15 và yêu cầu quan sát phân biệt; RV3-F04 vi phạm yêu cầu dừng pha đánh giá khi vượt trần tổng ở mục 3. Baseline, GHIM-B1A, phạm vi và registry đúng. |
| Standards/Security | **changes_requested.** Cờ cạn tài nguyên chưa chặn công việc tiếp theo; bằng chứng hồi quy bỏ mất nhánh quá hạn. Lớp đọc thân có đệm đã qua phản chứng độc lập, nhưng kiểm socket thật chưa đo được. |

## Finding còn mở

| ID | Severity | Lớp nguyên nhân | Tệp:dòng tại H | Mô tả / tác động | Bằng chứng chạy được | Gợi ý vá, không thi công |
|---|---|---|---|---|---|---|
| RV3-F03 | P2 | `mutant-oracles-non-discriminating` | `ops/canh_tuoi_audit_test.py:1743`, `:1771`, `:2023` | Ba đầu vào quá hạn được thay bằng đúng hạn. Chốt sai chỉ từ chối `==` và cho qua `>` nay sống ở ca đích lẫn mọi ca thực thi được. Hai đầu vào đầu còn được SPEC nghiệm thu 15 ghi rõ: GET 500 còn 0,5 s; phân tích W8 nhảy **qua** hạn. Quan sát đầu ra không đổi không bảo toàn khả năng phân biệt. Mã sản phẩm hiện tại vẫn dùng `>=`; đây là lỗi nghiệm thu/hồi quy, không cáo buộc sản phẩm hiện đang dùng `==`. | `python3 -B out/evidence/rv3_deadline_coverage.py` → rc 0, `RV3_DEADLINE_COVERAGE_COMPLETE`. Q01/Q02/Q03: gốc 0, mutant 0; toàn suite 468 ca đạt trên mỗi mutant, 1 ca socket lỗi hạ tầng. Chỉ khôi phục đầu vào cũ: gốc 0, mutant 3, đúng `DO:n15_cho_qua_han`, `DO:n15_han_cuoi_ghi`, `DO:n15_d14_khop_qua_han`. [Dữ liệu](evidence/rv3-deadline-coverage.json). | Giữ cả `<`, `==`, `>` tại từng chốt; phục hồi các đầu vào quá hạn đã mất, thêm ca biên thay vì thay thế. Bổ sung mutant chỉ giữ dấu bằng. Dùng cùng cách tham số hóa cho ba đường, vẫn giữ tín hiệu riêng của từng ca. |
| RV3-F04 | P2 | `unbounded-artifact-expansion` | `ops/canh_tuoi_audit.py:600`, `:713`; nguồn cờ `:244`, kiểm muộn `:719` | Sau khi `_tho_zip` đặt `c.can_tn=True`, `_t5` tiếp tục artifact, `_phan_luot` tiếp tục T3/T7, `_danh_gia` tiếp tục E; `_tho_zip` lần sau vẫn mở và đọc ZIP. Chỉ kết quả cuối được đổi thành S1. Vì thế tổng tài nguyên vẫn tăng sau khi đã cạn; trần tổng không thực sự dừng pha theo mục 3. | `python3 -B out/evidence/resource_stop.py` → rc 0, `RESOURCE_STOP_COMPLETE`. ZIP thường có sẵn, trần tiêm 1: còn 7 GET đánh giá + 1 lần giải nén sau cạn. Trần 10637: còn **43 GET + 19 lần giải nén**, tổng tới 25068. Đối chứng trần đủ: `fresh`, SHA đúng. `python3 -B out/evidence/resource_stop_signals.py` → rc 0, `2/2 CURRENT_CODE_FAILS_NAMED_EXPECTATION`; hai ca trên H rc 3 đúng tín hiệu. [Dữ liệu](evidence/resource-stop.json), [tín hiệu](evidence/resource-stop-signals.json). | Cho trạng thái cạn tổng chặn mọi công việc đánh giá tiếp theo: cùng gói, artifact kế, lượt kế và T3/T7; truyền kết quả S1 lên điểm điều phối, giữ pha ghi với ngân sách riêng. Thêm ca cạn sớm ở T2 và T5, kiểm không đọc ZIP/GET đánh giá sau cạn. Không chỉ thêm chốt trả S1 cuối pha. |

**Săn theo lớp:** F03 có ba biểu hiện đo được, ở kiểm trước chờ GET, hoàn tất bước ghi chung và hoàn tất đối soát D14; các nhánh REST, W0/W2/W7, adapter, workflow, phân hạng và các chốt hạn khác cũng đã rà, xem bảng phạm vi. F04 có hai đường khởi phát T2/T5 và nhiều đường tiếp tục chung: `_tho_zip` → `_t5`/`_phan_luot` → `_danh_gia`. Không tách các biểu hiện ấy thành finding riêng để tăng số lượng. F04 đã tồn tại trước H2..H: bốn hàm này trùng byte giữa H2 và H, [đối chiếu](evidence/resource-history.json). Đây là phát hiện mới của reviewer, không phải cơ chế mới do lượt vá cuối sinh ra.

Ở F04, lỗi là **các lần đọc tiếp sau khi đã phát hiện cạn**, không phải số byte vượt ở khúc đầu tiên dùng để phát hiện cạn. Không dựng ZIP lớn, ZIP bomb hay payload thoát cây; chỉ dùng fixture bình thường của test, tiêm trần nhỏ đúng I3. Trạng thái cuối vẫn S1, `sha_audit=null`; không có bằng chứng `fresh` giả ở phép này. `n2_tong_vuot` hiện chỉ cạn ở gói cuối và quan sát kết quả cuối, nên không phát hiện lỗi dừng sớm.

## Định danh, authority và điều kiện B

Đã đo băm trước khi đọc toàn bộ [SPEC 605 dòng](evidence/SPEC.md), kể cả GHIM-B1A, bảng kết cục, toàn bảng đột biến và Baseline nghiệm thu. `git -C src rev-parse HEAD HEAD^{tree}` khớp hai OID ở đầu báo cáo. HANDOFF SHA-256: `7078af6d04015619e3c81f16859dc74eddf146e0bc3538913ee4d4f6212dac13`.

Nguồn cố định: SPEC tại `a819291bb08af5e72cdd833b86544ea48d97b1fd`; Mission r109 tại `2e70d3b3dada5babd17e6c5e83f8c2b16cacc874`; B=`b4b79bf0cd301bb067a22c5245505d9a8ab232cb`; lease g3 từ ref được cấp, lưu [lease](evidence/lease.yaml), [Mission](evidence/mission.md). Đã đọc CLAUDE/AGENTS, protocol §8/8.3/12 và hướng dẫn làm việc liên quan.

Đã đọc lại bằng GET riêng nội dung [quyết định sau lượt 1](https://github.com/ducthangho/tra-luat/issues/1172#issuecomment-7157619068), [Review Rescue](https://github.com/ducthangho/tra-luat/issues/1172#issuecomment-7161189582), [miễn pha mở tại đúng H/tree](https://github.com/ducthangho/tra-luat/issues/1172#issuecomment-7162892740). JSON authority giữ trong `evidence/authority-*.json`. Không thao tác ghi GitHub. D134 là **tương đương theo schema**, ngoài mẫu số, không tín dụng; không có spec r6.

Baseline được đo **trước** các phép review mã: `PYTHONDONTWRITEBYTECODE=1 python3 -B out/evidence/baseline.py` → rc 0, **`BASELINE: DAT`**, [log](evidence/baseline.log). Không có điều kiện baseline lệch để gán blocked.

| Điều kiện | Kết quả độc lập |
|---|---|
| Không shallow; B trên first-parent origin/master | `false`; có B; đầu ref được cấp `98039c79a159e5b9b1cca0e50f1728ba26fdb3c5` |
| B là merge PR #1516 của B1a | Hai parent, subject merge #1516 đúng |
| Schema tại B = GHIM-B1A | `844b5218b6f6844945f5c4c9440f09015d238fe09a60d64b3787c440787e4f46` |
| Fixture tại B = GHIM-B1A | `ce8595739a1ab2f4a86c9c196255e5f91fb19a9f6d3865df6caa2d66f9970e6d` |
| Khối Lệnh kiểm tại d1b08c2… | SHA-256 `d9c78e708e18a211b7d8c7309638ffd1c73200578cf3128f9f0fc4275430f24e`; 254 dòng, 14992 byte |
| Bốn hàm chép nguyên văn | 4/4 trùng byte: `tieu_dung` 6885; `khoa_tu_ten` 108; `doc_moc` 148; `khung_cron` 248 byte. Trích theo ranh AST và giữ nguyên dòng nguồn; băm riêng trong log. |
| KHUNG_DAU theo thời điểm committer của B | B: `2026-11-25T05:36:53Z`; floor cron `2026-11-21T19:17:00Z`, ceil `2026-11-28T19:17:00Z`; KHUNG_DAU là ceil, khớp mã/Mission/lease |
| Tham số Mission/lease | B đúng; ISSUE_THEO_DOI=1520; KHUNG_DAU đúng |
| Job và upload tại B | Có `bien-nhan-audit`; artifact `bien-nhan-audit-${{ github.run_id }}-${{ github.run_attempt }}`, path `bien_nhan_audit.json`, `if: always()`, `if-no-files-found: error`; T3/X2 cho 11 tên/11 khóa riêng |
| Ba tệp mới vắng ở B | Workflow, module, test: cả ba `git cat-file -e` rc 128 |
| Registry tại B | 0 mục `canh_tuoi_audit_test` |

## Write set và kích thước

`git diff --numstat B H`: **4 tệp, +3342/−0**. H2..H: **chỉ hai tệp Python, +273/−29**; module +31/−2, test +242/−27. Trần lease/nang_tran 6 tệp/3500 dòng thêm: đạt.

| Tệp | Thêm | Xóa |
|---|---:|---:|
| `.claude/dev/ci_dang_ky_test.py` | 1 | 0 |
| `.github/workflows/canh-tuoi-audit.yml` | 29 | 0 |
| `ops/canh_tuoi_audit.py` | 1048 | 0 |
| `ops/canh_tuoi_audit_test.py` | 2264 | 0 |

`python3 -B out/evidence/write_set.py` → rc 0: **`WRITE_SET: 4/4; REGISTRY: exactly one literal MOI item, 0 removed`**; **`CI_MARKERS: 0 in 4 full files and 12 commit messages`**; `CORE_ABBREV H 7`, `CORE_ABBREV B 7`, `WRITE_SET_COMPLETE`. Script lấy mục MOI nguyên văn từ SPEC, so với toàn bộ dòng thêm, xác nhận không có dòng xóa. Không chép nguyên các chuỗi bỏ-qua-CI vào báo cáo. [Log](evidence/write-set-run.log).

Regex MOI không nhận output suite đỏ thực đo (`False`), đúng hành vi; không dùng việc registry đạt để gọi suite xanh. Script write_set đã điều chỉnh phần kiểm output từ kỳ vọng xanh cũ sang việc từ chối output đỏ thực tế; phần kiểm write set/literal/marker giữ nguyên logic.

## Đo lại lời khai executor

Các lệnh suite/registry/gates chạy tại bản sao H hoặc B ngoài `src/`; mọi Python dùng `-B`/`PYTHONDONTWRITEBYTECODE=1`. `evidence/<tên>.json` của wrapper lưu argv, cwd, rc, thời gian và băm log. Rc 0 của **runner phản chứng** chỉ nói runner hoàn tất, không mặc nhiên nói mutant chết.

| Lời khai / lệnh đã chạy | Rc thật | Kết quả thật / giới hạn |
|---|---:|---|
| `python3 -B ops/canh_tuoi_audit_test.py` | **1** | `CA: 468/469 dat`; `DOT BIEN: 271/275 bi giet dung ly do`; `TU KIEM PHAN HANG: DAT (5 dot bien)`; `TONG: DO`. [Log nguyên](evidence/suite-H-plain.log), 147,968 s. Không tái lập 469/469, 275/275 ở sandbox này. |
| Cùng suite `--chi-tiet` | **1** | Cùng số liệu. `n16_socket_that` rc 4 `PermissionError: [Errno 1] Operation not permitted`; bốn mutant HONG do ca gốc chưa đạt: `f02_nen_han`, `f02_nen_han_bien`, `f02_nen_socket`, `f02_nen_loi`. [Chi tiết từng ca/đột biến](evidence/suite-H.log). Không gọi đây là bốn mutant sống hoặc bốn lỗi sản phẩm. |
| Registry H: `python3 -B .claude/dev/ci_dang_ky_test.py` | 0 | **`PHẢN CHỨNG: 1677/1677 đỏ đúng`**, `TỔNG: ĐẠT`; 480,276 s. [Log](evidence/registry-H.log). |
| Cùng registry tại B | 0 | **`PHẢN CHỨNG: 1677/1677 đỏ đúng`**, `TỔNG: ĐẠT`; 481,419 s. [Log](evidence/registry-B.log). |
| actionlint với `/usr/bin/shellcheck` trên workflow H | 0 | stdout/stderr rỗng; syntax/ShellCheck đạt. [Lệnh, version](evidence/gates.log). |
| `python3 -m ruff check --no-cache --select F` trên ba Python H / registry B | 0 / 0 | `All checks passed!` cả hai, F delta 0. Đây là bare lint; contract/probe pin thuộc registry đã chạy riêng. |
| `packet_loop.py doctrine-scan --root .` / `adr-song --root .` | 0 / 0 | `12 tệp, 0 chỗ chép doctrine`; `66 ADR ... 66 dòng ... khớp 1–1`, ngoại lệ trạng thái 0016 được công cụ ghi rõ. |
| `git diff --check B HEAD` ở H | 0 | stdout/stderr rỗng. |
| `python3 -B out/evidence/offline_guard.py` | **1** | Vá connect/getaddrinfo để ném; **`OFFLINE_GUARD {"connect": 0, "getaddrinfo": 0} CA_RC 1`**, 468/469; ca socketpair vẫn bị sandbox chặn. Xác nhận các ca thực thi không dùng hai đường mạng này, không chứng nhận ca chưa chạy. |
| `rv2_distinguish.py` nguyên bản | 0 | **`RV2_DISTINGUISH: 9/9 GIET DUNG CA DICH`**. |
| `rv2_heartbeat_callers.py` nguyên bản | 0 | **`HEARTBEAT_WRITER_CALLERS 192 GIET 192 ORIGINAL_OK 192`**. Do script duyệt danh sách target nay có cả W0/W2/W7 rồi sinh lại W2/W7, 192 chứa ba lần lặp của **64 cặp phân biệt**; không gọi là 192 điều kiện độc lập. |
| `rv2_mutations.py` nguyên bản | 0 | 6 cặp GIẾT, 6 SỐNG tại ca cũ (N02–N05/N07/N08). Quét cả suite cho sáu mutant: mỗi mutant có đúng một ca mới giết đúng, cộng lỗi socket môi trường. N06 nay rc 3 đúng tín hiệu, không rc 4 HTTPError. |
| `buffered_deadline.py` nguyên bản | **1** | Cả bốn dòng đã đo `original_rc=0`, `t=30.0`, `TimeoutError`, control rc 0. Assert cuối vẫn đòi `original_rc==3` theo kết luận cũ nên thất bại. [Log gốc](evidence/buffered-original.log). |
| `buffered_deadline_g3.py` | 0 | **`BUFFERED_DEADLINE: 4/4 HEAD_BOUNDED_AT_30s; 4/4 READ1_CONTROL_STOPS_AT_30s; NO_NETWORK`**. [Diff](evidence/buffered_deadline-g3.diff). Không phải phép đo đồng hồ thực. |
| `rv2_mutations_g3.py` | 0 | **12/12** cặp gốc 0 → mutant 3 đúng ca. Chỉ đổi target N01–N09 và tên output; neo/thay không đổi. [Diff](evidence/rv2_mutations-g3.diff), [kết quả](evidence/rv2-mutations-g3.json). |
| `inventory.py` | 0 | **357→469** ca (+112, không bỏ tên ca), **229→275** mutant (+46); D61 23 mutant, 32 điều kiện × W0/W2/W7 = 96 target; 64 ca writer +2 đối chứng, thêm 4 ca writer dòng 62/116. D134 không còn trong bảng. |
| `rv3_body_deadlines.py` — reviewer mới | 0 | **`BODY_PAIRS 84 ORIGINAL_OK 84 GIET 84`**; raw giả tôn trọng timeout còn lại, HTTPResponse/BufferedReader thật; GET API/GET kho/PATCH/POST, Content-Length/chunked/EOF, success/HTTPError. |
| `additional_probes.py`, `ordinary_inputs.py`, `pagination_ordinary.py` | 0 mỗi script | Issue thiếu body W0/W3/W8 có báo cáo rc 3; null control rc 0; POST hoàn tất đúng hạn giữ pending; ngày không thật/sai dạng/vắng bị từ chối; `PAGINATION_ORDINARY: 3/3 REJECTED AS EXPECTED`. |

Lời khai về cấu trúc `_NenCoHan`, bọc `HTTPError.fp`, lấy socket qua `SocketIO._sock`, các nhóm ca mới và diff hẹp khớp mã đã đọc. Bằng chứng executor về socketpair/loopback thật chưa được reviewer tái lập; không nhận thay cho phép đo riêng.

## Bảng đột biến độc lập

Quy tắc: chỉ **GIẾT** khi ca gốc đạt, mutant rc 3 và `DO:<chính tên ca>:` do `TinHieuChotCa`; rc 4 là lỗi/giết sai lý do, không tín dụng. Mọi mutant được dựng ngoài `src/`. Hai bản sao Git H/B đều `core.abbrev=7`.

### R01–R31: bất biến và các chốt cũ

Lệnh `python3 -B out/evidence/reviewer_mutations.py` và `python3 -B out/evidence/i2_mutations.py`, rc 0/0. Mọi ca gốc ở bảng sau rc 0. Mỗi tên R ánh xạ neo/thay cụ thể trong [reviewer-mutants.json](evidence/reviewer-mutants.json); R30/R31 trong [i2_mutations.py](evidence/i2_mutations.py). R02 bỏ S6, R04 bỏ S2: tên cũ có chữ “fresh” không thay ý nghĩa neo; kết quả sau bỏ nhánh phụ thuộc các luật sau nó.

| Mutant | Ca đích và kết quả thực |
|---|---|
| R01_fresh_becomes_unknown | `n0_nen_fresh` → GIET rc 3 |
| R02_unknown_becomes_fresh | `n4_gop_kdd_thang_chay` → GIET rc 3 |
| R03_due_becomes_stale | `n4_s9_p_dat` → GIET rc 3 |
| R04_stale_becomes_fresh | `n4_gop_do_thang_kdd` → GIET rc 3 |
| R05_old_obligation | `n4_s3_p_vang` → GIET rc 3 |
| R06_link_T1 | `n1_lien_ket_created_at` → GIET rc 3 |
| R07_link_T7 | `n1_lien_ket_cuoi` → GIET rc 3 |
| R08_final_deadline | `n15_phan_tich_qua_han` → GIET rc 3 |
| R09_all_or_nothing | `n15_can_ngan_sach` → GIET rc 3 |
| R10_post_retry | `n8_post_khong_thu_lai` → GIET rc 3 |
| R11_patch_retry | `n8_patch_khong_thu_lai` → GIET rc 3 |
| R12_pending_deleted | `n8_giao_lai_gian_doan` → GIET rc 3; `n8_cho_bao_khong_bi_bo` → GIET rc 3 |
| R13_pending_replaced | `n8_cho_bao_khong_bi_thay` → GIET rc 3 |
| R14_reconciliation_bot | `n8_gia_danh` → GIET rc 3 |
| R15_reconciliation_since | `n8_doi_soat_cua_so` → GIET rc 3 |
| R16_shared_heartbeat | `n8_tu_kiem_truoc_patch` → GIET rc 3; `n8_tu_kiem_truoc_patch2` → GIET rc 3 |
| R17_zip_expansion | `n2_giai_nen_t2_tren` → GIET rc 3; `n2_giai_nen_t5_tren` → GIET rc 3 |
| R18_zip_entries | `n2_muc_t2_tren` → GIET rc 3; `n2_muc_t5_tren` → GIET rc 3 |
| R19_zip_total | `n2_tong_vuot` → GIET rc 3 |
| R20_workflow_step | `n10_buoc4_if` → GIET rc 3 |
| R21_workflow_permission | `n10_quyen` → GIET rc 3 |
| R22_chunk_read_removed | `n1_j_vuot_tran` → GIET rc 3; `n1_s_vuot_tran` → GIET rc 3 |
| R23_real_redirect_guard | `n1_s_khong_auth` → SONG rc 0; `n1_r_qua_3` → SONG rc 0 |
| R24_main_exit_zero | `n9_ma_thoat` → SONG rc 0 |
| R25_real_timeout_ignored | `n1_han_goi` → SONG rc 0; `n15_kep_timeout` → SONG rc 0 |
| R26_api_auth_removed | `n0_nen_fresh` → SONG rc 0; `n1_s_khong_auth` → GIET rc 3 |
| R27_last_link_event | `n1_lien_ket_event` → SONG rc 0; `n1_lien_ket_cuoi` → SONG rc 0 |
| R28_U6_attempt_removed | `n1_u6` → SONG rc 0; `n1_chua_xong` → SONG rc 0 |
| R29_heartbeat_reader_bypass | `n8_mien_m4` → GIET rc 3 |
| R30_I2_unknown_promoted_dat | `n4_s6` → GIET rc 3 |
| R31_I2_fresh_with_old_obligation | `n4_s3_p_vang` → GIET rc 3 |

Tổng **cặp**: {'GIET': 31, 'SONG': 10}; không cộng vào mẫu số 275 của executor. Output chính xác từng cặp ở `evidence/R*.json`; bảng gộp [reviewer-mutations-targets.json](evidence/reviewer-mutations-targets.json).

R23/R24/R25/R27/R28 còn SỐNG trên target cũ, nhưng quét 469 ca xác định mỗi mutant có một ca mới GIẾT đúng: lần lượt `n16_transport_that`, `n9_main_ma_thoat`, `n16_transport_that`, `n1_lien_ket_cuoi_event`, `n1_u6_run_attempt`. Mỗi lượt quét có 467 đạt, một GIẾT đúng và một rc 4 socket môi trường; **không** tính rc 4 là tín dụng. `run_survivors.py` rc 0, `ALL_SURVIVORS_COMPLETE`; log `evidence/R*-all.log`. R26 sống tại `n0_nen_fresh` nhưng chết đúng ở `n1_s_khong_auth`.

Các mutant trên bao phủ bốn trạng thái I2 và chiều một chiều (R01–R04/R30), nghĩa vụ cũ (R05/R31), LIÊN KẾT hai nơi (R06/R07), hạn hoàn tất và tất-cả-hoặc-không (R08/R09), số lần gửi vật lý POST/PATCH (R10/R11), pending không bị bỏ/thay (R12/R13), D14 bot/cửa sổ (R14/R15), validator đọc/ghi (R16/R29), ba trần ZIP (R17–R19), bộ kiểm workflow (R20/R21). Không suy từ R19 chết rằng “dừng ngay khi cạn” đã được kiểm: RV3-F04 là phản chứng cho suy luận đó.

### N01–N12: ca riêng mới của lượt cuối

| Mutant | Target nguyên bản: gốc/mutant | Target g3 đã commit: gốc/mutant |
|---|---|---|
| N01_attempt_equal | `n15_vong_doc_qua_han` 0/3 GIET | `n15_vong_doc_bien` 0/3 GIET |
| N02_digest_presence | `n1_t1_mien_art_digest` 0/0 SONG | `n1_t1_mien_art_digest_vang` 0/3 GIET |
| N03_artifact_name | `n1_t1_mien_art_khac` 0/0 SONG | `n1_t1_mien_art_ten` 0/3 GIET |
| N04_run_conclusion_presence | `n1_t1_mien_run_conclusion` 0/0 SONG | `n1_t1_mien_run_conclusion_vang` 0/3 GIET |
| N05_job_status | `n1_t1_mien_job_chuoi` 0/0 SONG | `n1_t1_mien_job_status` 0/3 GIET |
| N06_http_error_adapter | `n16_transport_that` 0/3 GIET | `n16_http_error` 0/3 GIET |
| N07_post_read_deadline | `n15_vong_doc_qua_han` 0/0 SONG | `n15_vong_doc_post` 0/3 GIET |
| N08_storage_read_deadline | `n15_vong_doc_qua_han` 0/0 SONG | `n15_vong_doc_get_kho` 0/3 GIET |
| N09_W0_equal | `n15_w0_phan_tich_qua_han` 0/3 GIET | `n15_w0_bien` 0/3 GIET |
| N10_final_equal | `n15_tinh_cuoi_qua_han` 0/3 GIET | `n15_tinh_cuoi_qua_han` 0/3 GIET |
| N11_W0_check_removed | `n15_w0_phan_tich_qua_han` 0/3 GIET | `n15_w0_phan_tich_qua_han` 0/3 GIET |
| N12_D14_check_removed | `n15_d14_khop_qua_han` 0/3 GIET | `n15_d14_khop_qua_han` 0/3 GIET |

Không còn N06 “giết sai lý do”: adapter wrapper nay bắt đúng HTTPError để phát `TinHieuChotCa`, cả target mới lẫn `n16_transport_that` đều gốc 0 → mutant 3. Phép riêng `rv2_distinguish.py` cũng 9/9, không dựa vào tên target executor đổi.

### Q01–Q13: ưu tiên bản vá mới và phần bảng executor bỏ sót

| Mutant độc lập | Target / số cặp | Gốc → mutant, phân hạng |
|---|---|---|
| Q01: d104 `>=` → `==` | `n15_cho_qua_han` | 0→0 **SỐNG**; mọi 468 ca thực thi được đều đạt. Phục hồi `moc=599.5`: 0→3 **GIẾT đúng ca**, quan sát hàm ngủ từ `[]` thành `[1]`. |
| Q02: d106 `>=` → `==` | `n15_han_cuoi_ghi` | 0→0 **SỐNG**; 468 ca đạt. Phục hồi `g.t=181.0`: 0→3 **GIẾT đúng ca**, mã thoát từ 3 thành 1. |
| Q03: f02:d14 `>=` → `==` | `n15_d14_khop_qua_han` | 0→0 **SỐNG**; 468 ca đạt. Phục hồi `them=500.0`: 0→3 **GIẾT đúng ca**, `doi_soat_loi:het_gio` thành `da_giao`. |
| Q10: bỏ reset socket timeout còn lại | 24 ca reviewer = 4 caller ×3 kiểu framing ×success/error | **24/24** gốc 0 → mutant 3 đúng tên ca |
| Q11: `read1` → `read` trong `_NenCoHan` | Cùng 24 ca | **24/24** gốc 0 → mutant 3 |
| Q12: dùng timeout cố định thay hạn còn lại | Cùng 24 ca | **24/24** gốc 0 → mutant 3 |
| Q13: không lấy `HTTPError.fp` | 12 ca HTTPError =4 caller ×3 framing | **12/12** gốc 0 → mutant 3 |

Q01–Q03 không có kill hợp lệ trong suite đã commit. Ca socket lỗi trên **cả nền gốc lẫn mutant**, nên không có bằng chứng nó giết ba mutant ấy. Đối chứng đầu vào cũ chứng minh chúng không tương đương. Q10–Q13 dùng nền giả mô phỏng một thao tác đọc bị chặn bởi timeout được đặt; bao gồm đối chứng nhanh trả trọn byte và chậm dừng ở 30 s. [Script](evidence/rv3_body_deadlines.py), [84 cặp và quan sát](evidence/rv3-body-deadlines.json). Không gọi ma trận này là thử socket/TLS thật.

Giết sai lý do: không có cặp R/N/Q được nhận tín dụng từ rc 4; các lượt quét toàn suite có rc 4 ở `n16_socket_that` đã tách là **KHÔNG ĐO ĐƯỢC**, không lỗi mutant. Tự kiểm của harness vẫn đạt đủ 5: kill thật, lỗi AttributeError, assertion ca khác, mutant sống, mutant tương đương. D134 ngoài mẫu số; probe schema nguyên trạng vẫn cho D5 thêm bằng 0 trên cả hai biến thể, không lấy làm finding.

## Đối chiếu finding các lượt mã nguồn

Nguồn: lượt 1 H1=`127b82a8a9e41fda3c4a230810118f0bedfb200d`, [verdict](../review-1/VERDICT.md); lượt 2 H2=`d3bcd6a171644b18d9fd37a185cfb8fc6d641ef4`, [verdict](../review-2/VERDICT.md). Nhãn đúng một trong bốn nhãn yêu cầu. Theo §8.3, thiếu phép đo cần để đóng lớp không được ghi đã sửa toàn lớp.

| Finding nguồn | Nhãn trên H | Phép đo / phần còn hở |
|---|---|---|
| Lượt 1 F01 — REST domain | **ĐÃ SỬA ĐÚNG LỚP** | T1 từ chối attempt 0/âm, conclusion sai kiểu, artifact digest/name/status sai hoặc thiếu; N02–N05 có ca riêng và kill đúng. Issue thiếu/sai kiểu body/state tại W0/W3/W8 có báo cáo rc 3, null control rc 0. Không tìm thấy biểu hiện cùng cơ chế còn hở trong phạm vi đã kiểm. |
| Lượt 1 F02 — hạn/thứ tự | **VÁ HỜ** | Các lỗi hành vi đã nêu được chặn ở W0, tính S cuối, body và D14; R08/R09, N10–N12, buffered 4/4 và Q10–Q13 đều phân biệt. Tuy nhiên chưa đủ bằng chứng đóng **toàn lớp** theo §8.3 vì `n16_socket_that` và bốn mutant phụ thuộc nó chưa chạy được; Python 3.12/TLS chưa xác minh. Nhãn này ghi giới hạn nghiệm thu, không khẳng định còn lỗi body đã tái hiện. Pha mở được miễn, không dùng làm lý do nhãn. |
| Lượt 1 F03 — oracle | **VÁ SINH LỖI MỚI** | Các R cũ đã có target giết, D134 xử lý đúng miễn, N01–N09 và writer đã sửa. Nhưng thay đầu vào ba ca cũ làm Q01–Q03 sống; phục hồi đúng đầu vào cũ giết. Cùng lớp, biểu hiện mới RV3-F03. |
| Lượt 2 F02 — đọc có đệm | **VÁ HỜ** | Phản chứng cũ nay dừng ở 30,0 s trên cả bốn caller; HTTPError/framing bổ sung qua 84 cặp. Cơ chế raw wrapper đã sửa đúng hướng và chưa tìm thấy lỗi body còn mở trong mô hình đo. Giữ nhãn chưa đóng vì phép socket thật bắt buộc không đo được, như hàng trên. Không gán P2 cho việc sandbox từ chối. |
| Lượt 2 F03 — N01–N09, D61 writer | **VÁ SINH LỖI MỚI** | 12/12 N qua ca đích mới; 23 D61 chạy W0/W2/W7, writer 64 cặp phân biệt, N06 rc 3 đúng tín hiệu. Ba input sửa ở H2..H gây mất phủ quá hạn: Q01–Q03. Việc sửa đủ danh sách N không đóng toàn lớp. |

**Phạm vi săn toàn lớp trong cả bản vá:**

| Lớp | Các đường đã rà | Kết luận theo đường |
|---|---|---|
| `rest-response-domain-incomplete` | `_j` JSON/status/request-id; `_liet_ke` D1/D3/D4/D14; HINH_D1; `_hinh_rest` run/job/artifact ở T1; LIÊN KẾT T1/T7 và U6; D6/D7 b64/workflow/tree; D8/D9 master/compare; `_hinh_issue` W0/W3/W8; D12/D13/D14 comment; context run ID/attempt; heartbeat reader/writer | Các fixture sai miền không được dùng làm kết quả xanh. N02–N05 target cũ không nhạy nhưng ca mới nhạy. T7 kiểm định danh/U6; không giả rằng nó chạy lại nguyên T1. Chưa tìm thấy lỗi sản phẩm cùng lớp. |
| `bounded-evaluation-order-dependent` | Sắp xếp E/artifact; không thoát sớm khi thấy dat; cap timeout trước gọi; kiểm trước chờ; `_mot_lan`/`_NenCoHan` cho GET API/GET kho/PATCH/POST/HTTPError; kiểm hoàn tất đọc; W0 gồm parse/validator và khấu trừ ngân sách; tính S cuối; `_buoc_ghi` D8/D9/W2/W3/W5/W6/W7/W8; D14 sau khớp | Phản chứng thời gian trên các đường đo được đều bị chặn. Waiver chỉ pha mở. Socket thật/Python 3.12 còn thiếu phép đo; Q01–Q03 là lỗ test, không bằng chứng `>=` hiện tại sai. |
| `mutant-oracles-non-discriminating` | Harness/TinHieuChotCa/self-check; toàn 275 mục; D134 miễn; R22–R28 adapter/main/T7/U6; N01–N09 REST/hạn/HTTPError; các nhánh K1/Issue; D61/62/116 W0/W2/W7; chốt biên d99/d104/d105/d106/W0/D14/read/raw; bộ kiểm workflow | Còn hở tại ba chốt quá hạn Q01–Q03. `n2_tong_vuot` chỉ phủ kết cục cuối, không phủ dừng ngay sau cạn (bằng chứng bổ sung cho RV3-F04). Không tuyên bố đã chứng minh mọi biểu thức ghép tương lai bằng tổng số mutant. |
| `unbounded-artifact-expansion` | Byte tải J/S; mục ZIP; byte giải nén/gói; tổng tiến trình; T2 biên nhận; T5 mọi bằng chứng; cùng artifact/lượt kế; T3/T7 và toàn E | Trần byte tải/mục/gói có mutant và ca biên giết. Trần tổng quyết định đúng S1 nhưng không dừng phần việc còn lại ở hai nhánh T2/T5. RV3-F04; cùng cách sửa cần đi tới điểm điều phối. |

## Đối chiếu lớp review đặc tả vào mã H

Đã đọc các finding/classes từ bản Git của review đặc tả 1–3, lưu [lượt 1](evidence/spec-review-1.json), [lượt 2](evidence/spec-review-2.json), [lượt 3](evidence/spec-review-3.json); đối chiếu bảng Thay đổi của SPEC đóng băng. Không dùng số đo mô hình đặc tả làm kết quả sản phẩm.

| Lớp đặc tả | Đúng một nhãn | Bằng chứng áp vào mã hiện tại |
|---|---|---|
| `notification-dedup-before-delivery` | **ĐÃ SỬA ĐÚNG LỚP** | R12/R13 giết đúng ca pending; `n8_phan_hoi_mat`, `n8_giao_lai_*`, đối soát rồi cấp mới, cửa sổ 1000/1001 đều chạy trong suite; POST hoàn tất đúng hạn: 1 POST, pending còn, ack null. Đổi Issue/heartbeat hỏng có giới hạn đã công bố trong SPEC §10, không giả bất biến vô điều kiện chống người có quyền sửa. |
| `write-retries-violate-delivery-contract` | **ĐÃ SỬA ĐÚNG LỚP** | `_goi` chỉ GET retry; R10/R11 0→3. Đếm **lần gửi vật lý** ở ca POST/PATCH hỏng; W2 và W7 là hai thao tác khác nhau, mỗi thao tác một lần gửi. |
| `b1-consumer-contract-mismatch` | **ĐÃ SỬA ĐÚNG LỚP** | GHIM schema/fixture, 4 hàm byte-equal; 120/120 hình, 118/118 ngữ nghĩa, 2/2 ghim; T2/T5 byte fixture qua bảng kết cục; trần gói và lỗi nguyên hàm được phân biệt. Vấn đề dừng trần tổng được giữ dưới lớp riêng RV3-F04. |
| `consumer-freshness-anchor-unverified` | **ĐÃ SỬA ĐÚNG LỚP** | `_lech_lien_ket` dùng chung chín trường T1/T7; R06/R07 giết; các target `n1_lien_ket_*` và `n1_lien_ket_cuoi_*`; U6 từng trường; NEO thắng lỗi con trong suite. Không lấy created_at của biên nhận thay neo D1 chưa liên kết. |
| `freshness-forgets-overdue-obligations` | **ĐÃ SỬA ĐÚNG LỚP** | R05/R31 giết; các ca R nhiều khung, đóng liên tục `dong_den`, đóng tay trước dựng E, đóng tay không phải dat và P đóng tay không due đều đạt; không cho F xanh xóa O. |
| `bounded-evaluation-order-dependent` | **VÁ HỜ** | Lịch gọi tất định, final check và raw-body probes đã đạt; không còn phản chứng cũ trên mô hình đo. Chưa đủ phép đo socket thật/Python 3.12 để đóng toàn lớp (§8.3). Miễn mở kết nối được ghi riêng, không tính lỗi. |
| `heartbeat-value-domain-incomplete` | **ĐÃ SỬA ĐÚNG LỚP** | Chung `kiem_nhip_tim` ở W0/W2/W7; D61 23 mutant/96 target, 64 cặp writer độc lập giết đúng; D62/D116 cả ba nơi; R16/R29 giết; tự sinh m9/m25 chặn trước PATCH. |
| `unbounded-artifact-expansion` | **VÁ HỜ** | R17–R19 đều giết trên ca đã commit, nhưng fixture cạn sớm T2/T5 trên H cho thêm 1/19 lần giải nén sau cạn. RV3-F04. |
| `workflow-step-controls-unconstrained` | **ĐÃ SỬA ĐÚNG LỚP** | Bộ kiểm allowlist từng tầng/bước; n10 âm/dương đã chạy; R20/R21 giết; dòng 82 có 18 mệnh đề + hai vế phụ. Ca YAML lặp cùng `run` được parser cấu trúc nhận nhưng actionlint rc 1 chặn, nên gate ghép vẫn từ chối. |
| `mutant-oracles-non-discriminating` | **VÁ HỜ** | N và writer được sửa; ba mutant chỉ-chặn-bằng-hạn sống trên suite, có đối chứng phân biệt hợp lệ. Không thể đóng lớp bằng 275 mục được kê. |
| `markdown-state-table-column-drift` | **KHÔNG ÁP DỤNG** | Lỗi thuộc trình bày bảng SPEC cũ; B..H không đổi Markdown/SPEC, write set chỉ bốn tệp đã đo. |
| `merged-misreported-as-landed` | **KHÔNG ÁP DỤNG** | Lỗi phát biểu trạng thái ở SPEC cũ; mã H không thay phát biểu đó hay tiến hành merge/land. Không dùng review này để chứng nhận landed. |

## Đầu vào thù địch: mô tả, đường mã, ca phủ

Chỉ mô tả các hướng gây sai lệch. Phép dựng bổ sung dùng JSON REST/ZIP dữ liệu thường và đồng hồ giả; không payload tấn công, không đường dẫn thoát thư mục, không gọi GitHub thật từ suite.

| Hướng | Đường mã xử lý | Ca commit đã chạy / đo bổ sung |
|---|---|---|
| Phân trang lặp/thiếu/đổi thứ tự; total_count không khớp | `_liet_ke`: trần 10 trang, tổng và ID duy nhất; `_danh_gia`/`_t5` xếp id tăng | `n1_hai_trang`, `n1_total_count`, `n1_trung_id`, `n4_s1_khong_tron`, `n15_thu_tu_goi`; probe lặp bị `khong_tron` sau 10 GET, thiếu bị `tong_lech` sau 1 GET. Không tuyên bố phát hiện được danh sách thiếu mà máy chủ nói dối đồng bộ mọi chứng cứ. |
| created_at sai dạng, vắng hoặc ngày không tồn tại | `gio`/`doc_moc`, HINH_D1, LIÊN KẾT | `n1_d1_hinh_created_at` và các ca trường D1; ordinary-inputs đo ngày 30/2, dạng không Z, null; pagination đo vắng: đều `khong_do_duoc/khoa_chon_khong_doc_duoc`. |
| Rerun attempt; workflow_dispatch lẫn vào; head_sha đổi giữa hai D2 | HINH_D1 schedule/master/path; T1 kiểm miền; LIÊN KẾT T1/T7; U6 attempt/status/conclusion/updated_at; neo khung D1 | Nhóm `n1_d1_*`, `n1_lien_ket_*`, `n1_lien_ket_cuoi_head_sha`, `n1_u6_run_attempt`; R06/R07/R27/R28 và oracle_audit T7 phân biệt. Dispatch không được dùng làm bằng chứng làm tươi. |
| Comment giả B2_SU_KIEN từ người không phải bot | `_khop`: login bot, đúng một dòng, nội dung sự kiện; D13/D14 | `n8_gia_danh`, đối chứng bot, `n8_hai_dong_su_kien`, `n8_doc_lai_comment_login`; R14 giết đúng. Không chống workflow khác cùng quyền bot; SPEC công bố giới hạn đó. |
| Người sửa tay thân Issue; nhịp tim cũ/hỏng/vắng | `doc_nhip_tim` và validator miền; `_ghi_than` kiểm trước ghi/đọc lại byte và state; `_thong_bao_can` | `n8_doc_lai_than`, `n8_state`, `n8_json_hong`, `n8_nhip_tim_cu`, `n8_bien_24h`, `n8_qua_24h`, nhóm miền và body/state W0/W3/W8. Thiếu body trả lỗi có báo cáo; body null được coi rỗng. |
| Thiếu X-GitHub-Request-Id; redirect http/host khác | `_j` đòi dấu GitHub; `_KhongChuyenHuong` ngăn tự theo; `_tai` xử lý R/S tường minh và đếm chuyển hướng; `_goi` chỉ gửi Authorization tới api.github.com | `n1_j_khong_dau`, `n1_j_403_khong_dau`, `n1_r_khong_https`, `n1_r_qua_3`, `n1_s_khong_auth`, `n16_transport_that`; R23/R25/R26. HTTPS host kho khác là đường **được phép** theo SPEC, không có allowlist host kho; không gán nhầm mọi host lạ là lỗi. |
| Content-Length sai; gói nhiều mục hoặc giải nén tổng lớn | `_mot_lan` cap byte J/S; `_tai` so chiều dài; `_tho_zip` đếm mục/byte thực; T2/T5 phân loại | `n1_s_ngan`, `n1_j_vuot_tran`, `n1_s_vuot_tran`, `n2_muc_t2/t5_*`, `n2_giai_nen_t2/t5_*`, `n2_tong_vuot`; R17–R19 giết. **Thiếu dừng sau cạn tổng: RV3-F04**, đã đo thêm bằng ZIP bình thường. |
| Đồng hồ chạm đúng hạn; POST hoàn tất ở/sau hạn | `_goi`, `_mot_lan`/raw wrapper, W0, final evaluation, `_buoc_ghi`, D14 final | `n15_vong_doc_bien`, `n15_w0_bien`, `n15_tinh_cuoi_qua_han`, `n15_goi_dung_han`, `n15_vong_doc_post`, `n15_nen_post`; probe POST ở 180 giữ pending, không ack. Ba ca đổi sang bằng hạn bỏ mất phía `>`: RV3-F03. |
| Workflow thêm khóa/bước/quyền | `kiem_hinh`/`_lech`/`_khoa` trong suite, 18 chốt mục 8; actionlint bổ trợ cú pháp | `n10_khoa_workflow`, `n10_quyen`, `n10_so_buoc`, các n10 bước 1–4 và `n10_tep_that`; R20/R21 giết. Không dispatch workflow. |

## BẢNG SĂN chủ động

| Hướng / giả thuyết | Phép đo đã chạy | Kết quả |
|---|---|---|
| Sai B hoặc ghim đã làm phép review vô nghĩa | baseline.py, object Git, byte compare bốn hàm | BASELINE DAT; không có blocker nền |
| Body buffered có thể giữ luồng dù guard ngoài đúng | buffered_deadline gốc/g3; 84 cặp Q10–Q13 | Phản chứng cũ đã bị chặn; error, chunked và EOF cùng chịu hạn; giới hạn socket thật tách riêng |
| Thay `>` bằng `==` trong fixture làm mất nhánh quá hạn | Q01–Q03 và toàn suite; phục hồi đúng input cũ | 3 mutant sống; input cũ giết đúng, RV3-F03 |
| HTTPError vẫn chết sai lý do | N06 nguyên/g3, rv2_distinguish, ma trận body error | Đã chuyển thành rc 3 đúng ca; không còn lỗi HTTPError rc 4 ở target đó |
| Bộ kiểm miền chỉ bảo vệ W0, bỏ W2/W7 | R16/R29, D61 inventory, 192 lượt writer/64 cặp khác nhau | Giết đúng ở mọi nơi được kiểm; 96 target D61 gồm đủ ba caller |
| F xanh che nghĩa vụ cũ hoặc unknown bị nâng lên dat | R01–R05/R30/R31, ca gộp/đóng tay | Các mutant chết đúng, không tìm thấy lỗi mới |
| Mất sự kiện pending hoặc POST gửi lại vật lý | R10–R15, ca stateful, POST muộn | Sự kiện còn chờ, đối soát trước gửi; mỗi thao tác ghi một lần gửi |
| Cờ cạn tổng chỉ đổi kết quả, không dừng tiêu tài nguyên | resource_stop.py + hai ca tín hiệu T2/T5 | Xác nhận 7/43 GET và 1/19 lần giải nén sau cạn, RV3-F04 |
| REST lỗi hình bị nhận xanh hoặc crash | reviewer_probes, additional_probes, ordinary_inputs, N02–N05 | Từ chối đúng, có báo cáo; null body là đối chứng hợp lệ |
| Thứ tự/phân trang làm đổi kết quả theo phần đã đọc | pagination_ordinary, n15_thu_tu_goi/can_ngan_sach, R09 | Phân trang lỗi bị từ chối, chuỗi gọi tất định và cạn thời gian toàn pha |
| Workflow kiểm hình bỏ lọt khóa/bước/quyền | R20/R21, n10, oracle_audit duplicate YAML | Khóa/bước/quyền bị chặn; duplicate cùng giá trị bị actionlint chặn dù parser cấu trúc nhận |
| Chỉ tin lời khai scope/CI/network | write_set.py, registry B/H, offline_guard, snapshot toàn cây | 4 tệp/literal MOI/0 marker, registry 1677/1677; 0 connect/DNS; src delta 0 |

## Phán ba câu hỏi executor

1. **Ca đóng lớp ngoài danh sách hẹp: trong phạm vi vá hẹp.** Diff H2..H chỉ ở hai tệp đã cho; bổ sung W2/W7, nhánh REST/Issue, biên hạn và PATCH trực tiếp phục vụ F02/F03 cùng cơ chế. Không thêm hành vi sản phẩm mới ngoài raw wrapper cần cho F02. Số “khoảng 36 dòng” không phải trần authority; các commit df63236/81c6416 được xét theo nội dung. Việc đổi mất input quá hạn bị phản đối vì chất lượng nghiệm thu, không vì vượt scope.

2. **Có làm mất phủ quá hạn.** Q01/Q02/Q03 là bằng chứng trực tiếp: suite hiện không phân biệt guard `==` với guard đúng `>=`. Hai ca còn không giữ đầu vào SPEC nghiệm thu 15 đã nêu. Giữ quan sát cũ là chưa đủ. Giữ cả đầu vào bằng hạn và quá hạn sẽ kiểm được cả gỡ chốt, sai biên và chỉ-chặn-dấu-bằng.

3. **Chấp nhận `*_g3.py` làm bằng chứng bổ sung sau khi kiểm diff và tự chạy.** buffered g3 sửa assert mô tả kết luận cũ, không thay stimulus; mutations g3 chọn các ca mới đã commit, không đổi neo/thay. Cả nguyên bản và bản sửa, rc thật và JSON đều được giữ. Không dùng g3 để che việc target cũ sống, hoặc thay phép kiểm độc lập: reviewer đã chạy rv2_distinguish và Q mới. Bằng chứng g3 không chứng minh toàn lớp đã đóng.

## Rủi ro tồn dư đã miễn

Theo [comment 7162892740](https://github.com/ducthangho/tra-luat/issues/1172#issuecomment-7162892740) neo đúng H/tree: **pha MỞ** trong `urllib open()` — DNS/connect/TLS/gửi request/đọc status và header — chỉ được giới hạn bởi socket timeout từng thao tác. `_mot_lan` chưa thể ngắt toàn pha đó đúng hạn tuyệt đối; kết quả mở muộn bị chặn ở đường đọc/kiểm sau đó. Đây là **rủi ro tồn dư chủ kho đã chấp nhận**, không gán P0–P2 và không làm verdict changes_requested.

Không mở rộng miễn trừ sang body, HTTPError, kiểm hoàn tất, retry sleep, W0/D14 hay trần giải nén. Các phần ấy được phán bình thường. Không tự nhận đã tái lập số giây loopback trong handoff. Dùng thuộc tính riêng `SocketIO._sock` là phụ thuộc triển khai cần kiểm trên môi trường chạy; phép socketpair bảo vệ phụ thuộc này chưa chạy được ở sandbox hiện tại.

## KHÔNG ĐO ĐƯỢC / không chạy

| Phần | Trạng thái và lý do |
|---|---|
| n16_socket_that và bốn mutant phụ thuộc | **not_measured**: socketpair bị OS/sandbox từ chối. Suite nguyên trạng rc 1; không sửa ca, không bỏ ca để lấy xanh, không nới quyền. |
| Socket/TLS/HTTP loopback với đồng hồ thực | Không tái lập; chỉ có lớp HTTPResponse/BufferedReader thật trên nền byte/dong_ho giả. Không dùng log executor làm phép đo reviewer. |
| Python 3.12 của workflow | Probe môi trường rc 1: 3.12.3 có sẵn nhưng thiếu `jsonschema`; chưa chạy suite bằng 3.12. Mọi kết quả suite trên 3.13.18. [Log](evidence/python312-check.log). |
| Windows M3, selftest toàn kho, registry --chay, full M9, CI PR | Không chạy trong review offline này; registry mặc định không thay các gate đó. Không chứng nhận sẵn sàng push/land. |
| GitHub live delivery, chủ kho thực nhận tin, nghiệm thu 14 sau merge | Không chạy; không tạo Issue/comment hay dispatch. Không có bằng chứng kênh nhận thật từ review này. |
| Trạng thái remote sau clone được cấp | Phép first-parent dùng origin/master đã fetch trong clone; không fetch mới vào src và không chứng nhận remote bất biến sau thời điểm đó. |
| Model/effort phục vụ thực tế | Không có metadata xác nhận độc lập; khai provider/tool surface theo phiên, không dùng prompt làm attestation. |

## Tính chỉ đọc, bằng chứng và điểm dừng

Snapshot trước/sau bao gồm tracked, untracked, ignored và `.git`: **18192 → 18192 tệp, 0 băm đổi, 0 tệp thêm/xóa**. HEAD/tree đúng H; status/diff/index rỗng. [Kết quả](evidence/readonly-result.json), [trước](evidence/readonly-before.json), [sau](evidence/readonly-after.json). Snapshot chỉ chứng minh không có delta quan sát tại hai mốc; không dùng nó như chứng minh tuyệt đối về mọi thời điểm trung gian. Mọi script, mutant và output do reviewer tạo nằm ngoài src.

Báo cáo đã được ghi tăng dần; bản ghi tiến độ trước khi hợp nhất ở [VERDICT-progress.md](evidence/VERDICT-progress.md). Toàn bộ log và JSON thật giữ tại `out/evidence/`; bản sao H/B và mutant ở `review-tmp/` được giữ để chạy lại. Nếu dựng lại: sao chép src thành review-tmp/H, clone chia sẻ src thành review-tmp/B checkout B, đặt `git config core.abbrev 7` trên cả hai; chạy các script tại thư mục gốc rv3. Các script có `parents[2]` để tìm thư mục gốc, không cần sửa src. Lưu ý phép quét R sống dùng `reviewer-mutations-targets.json`; file `reviewer-mutations.json` là metadata wrapper, không phải danh sách kết quả. Từng `R*.json` là nguồn kết quả không bị ghi đè.

**Giới hạn lượt:** review 3/3 đã dùng; executor 4/4 theo Rescue đã dùng. Lớp oracle tái diễn ba lượt mã nguồn và có lịch sử ở review đặc tả; §12 yêu cầu dừng vòng và xét lại cách làm. Không tự cấp lượt review/attempt mới, không chuyển vai executor hay sửa giúp. Theo cách đếm bảo thủ §8.3, F02 còn phần phải đo nên không đưa vào tử số lớp đã đóng; trong hai lớp mở ở lượt 2, không lớp nào được chứng nhận đóng trọn ở lượt 3. RV3-F04 là lớp mới đối với finding mã nguồn, nhưng tái mở lớp đã có ở lịch sử đặc tả; báo riêng, không dùng để làm đẹp tỷ lệ. Quyết định tiếp theo thuộc điều phối/chủ kho theo authority hiện hành; báo cáo này không tự tạo quyền push, merge, land hay thêm vòng vá.
