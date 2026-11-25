VERDICT: changes_requested
reviewed_sha: dac537eb7fdb75fb74e1f0cfa17a67dc4ec69cae
reviewed_tree: b09ec579523ad20492c4160850d6bb349445c0d0
spec_sha256: 345520e199ba7072c2bea92b876a3db1877cabce7969f82a379bb078d1dc2e4d

Lượt review mã nguồn 4/4, cuối. **Còn một finding P2: RV4-F01, mất dữ liệu báo cáo khi cạn tài nguyên. Không approve.** Không có P0/P1. Baseline đạt nên không dùng verdict `blocked`; phần kiểm socket không đo được ghi riêng, không biến thành lỗi sản phẩm. Báo cáo được ghi tăng dần trong quá trình review.

| Trục | Phán quyết |
|---|---|
| Spec | **changes_requested** — nhánh S1 mới vi phạm nội dung báo cáo ở mục 6. Các chốt dừng tài nguyên và ba ca quá hạn cũ đã sửa được hành vi được nêu ở lượt 3. |
| Standards/Security | **Chưa đủ nghiệm thu toàn bộ**: suite nguyên trạng còn một ca và bốn mutant không đo được do quyền socket. Các gate lint/registry đạt; không tìm thêm lỗi an ninh P0–P2 ở đường đã đo. Miễn pha mở vẫn áp dụng đúng phạm vi, không phải lý do chặn. |

Reviewer độc lập: Codex, provider OpenAI, thực thi shell cục bộ qua công cụ API; transport machine/local. Model/effort phục vụ không có metadata độc lập để chứng thực (KHÔNG ĐO ĐƯỢC). Sandbox workspace-write, approval never. Không sửa src/, không commit/push/GitHub ghi/dispatch.

## Định danh đã đo

`git -C src rev-parse HEAD HEAD^{tree}` rc 0: đúng H/tree trên. `git status --porcelain=v1` rỗng. Băm SPEC đo TRƯỚC khi đọc: đúng 345520e199ba7072c2bea92b876a3db1877cabce7969f82a379bb078d1dc2e4d. `sha256sum HANDOFF.yaml` rc 0: 29a7b6a4623d0f484aeab4d2f34f0c765c2ca4a13f8aaeb2811d2d2fb60903cd.

## Baseline nghiệm thu — ĐẠT

`PYTHONDONTWRITEBYTECODE=1 python3 -B out/evidence/baseline.py` rc 0, `BASELINE: DAT` ([log](evidence/baseline.log)). Kho không shallow; B là merge #1516 với hai parent, nằm trên first-parent origin/master `d0868dbf7f6324755aa4ed0f3e02d4efa84866f0`. Schema/fixture đúng băm ghim. Khối Lệnh kiểm đúng `d9c78e708e18a211b7d8c7309638ffd1c73200578cf3128f9f0fc4275430f24e`, 254 dòng / 14.992 byte. Bốn hàm chép nguyên văn trùng byte.

Committer B = 2026-11-25T05:36:53Z; khung nhỏ nhất không trước mốc này = 2026-11-28T19:17:00Z, trùng mã/lease/Mission. ISSUE_THEO_DOI = 1520 ở cả ba. Workflow B có job/upload đúng tên và path; T3 cho 11 tên/11 khoá duy nhất. B không có ba tệp mới và không có mục registry mới.

Numstat B..H rc 0: đúng 4 tệp, +3415/−0 (1, 29, 1051, 2334); dưới trần 6/3500. H3..H sản phẩm chỉ sửa `_tho_zip`, `_t5`, `_phan_luot`, `_danh_gia`; phép đo riêng xác nhận pha mở trùng byte.

## Cổng và probe đã chạy

- Suite Python 3.13.18: rc 1; `CA: 477/478 dat`, `DOT BIEN: 285/289 bi giet dung ly do`, `TU KIEM PHAN HANG: DAT (5 dot bien)`, `TONG: DO`. Ca `n16_socket_that` và bốn mutant phụ thuộc nó không đo được vì sandbox từ chối `socketpair` với errno 1. Không biến rc 1 này thành pass; không nhận lời khai 478/478 thay phép đo riêng. [Log](evidence/suite.log).
- `python3 -B out/evidence/gates.py` rc 0: actionlint 1.7.7 với ShellCheck 0.9.0 rc 0; Ruff 0.15.15 `--no-cache --select F` H=0, B=0, delta=0 (`All checks passed!`); doctrine-scan sạch 12 tệp; adr-song 66/66; diff-check rc 0. [Log](evidence/gates.log).
- `resource_stop.py` nguyên bản rc 0 `RESOURCE_STOP_COMPLETE`: cap 1/10637 đều 0 GET đánh giá và 0 ZIP sau cạn; cap đủ vẫn fresh. `resource_stop_signals.py` nguyên bản rc 1 ở assert cũ đòi hai ca thất bại; thực đo hai ca rc 0. Bản `_g4` rc 0 `2/2 CURRENT_CODE_MEETS_NAMED_EXPECTATION`.
- `rv3_body_deadlines.py` nguyên bản rc 0: `BODY_PAIRS 84 ORIGINAL_OK 84 GIET 84` với HTTPResponse/BufferedReader thật, raw giả tôn trọng timeout; không phải socket/TLS thật.
- `static_audit.py` rc 0: sáu nút mã pha mở/transport trùng byte H3..H, đúng tám biểu thức so hạn ngân sách/lần thử. Write set 4/4, MOI nguyên văn 1/1, 0 dấu bỏ CI trong bốn tệp và 16 commit message; core.abbrev=7 ở H/B. [Log](evidence/static-audit.log).

## Finding mới đã tái hiện

| id | severity | lớp nguyên nhân | tệp:dòng | mô tả | bằng chứng chạy được | gợi ý vá |
|---|---|---|---|---|---|---|
| RV4-F01 | P2 | `evaluation-report-evidence-dropped` | `ops/canh_tuoi_audit.py:717`–`:718` | Trả S1 ngay sau `_phan_luot` bỏ toàn bộ `luot` đã tích lũy trước khi dựng báo cáo. Khi chỉ gói cuối làm vượt tổng, lượt 10 đã `dat` với đủ T1–T7 vẫn biến mất, `khung={}`. SPEC §6 yêu cầu báo cáo mỗi khung xét và danh sách lượt; §3 cấm dùng kết quả một phần để kết luận audit, không miễn nghĩa vụ báo cáo các quan sát đã có. Mất dữ liệu chẩn đoán khi chạm trần là hồi quy do bản vá mới. | `PYTHONDONTWRITEBYTECODE=1 python3 -B out/evidence/rv4_report_contract.py` rc 0: `REPORT_CONTRACT_REGRESSION: H3=0 H=3 EXACT_NAMED_SIGNAL`. Ca `rv4_report_preserves_evaluated_runs` đỏ đúng tín hiệu ở H, đạt ở H3; S1/sha null không đổi. [Log](evidence/rv4-report-contract.log), [JSON](evidence/rv4-report-contract.json). | Dừng thu thập ngay khi cạn nhưng giữ quan sát đã có khi dựng báo cáo, biểu thị phần chưa đánh giá một cách trung thực; không dùng lượt đã đạt để chọn SHA hay tiến `dong_den`. Không bỏ chốt dừng, không tự đổi SPEC. Đây chỉ là gợi ý, reviewer không sửa mã. |

`rv4_resource_matrix.py` rc 0: `RESOURCE_MATRIX 80 EXHAUSTION_RUNS 40 ZIP_POSITIONS AFTER_WORK=0`; đúng tổng vẫn fresh, hai ZIP dữ liệu thường dừng trước khúc/tệp sau. Trong 40 lượt đã có ít nhất một lượt `dat`, `khung` vẫn rỗng. Lỗi tiêu tài nguyên RV3-F04 đã được chặn; lỗi báo cáo là hệ quả riêng cần ghi nhận, không trộn hai quan sát.

`rv4_post_deadline.py` rc 0: `POST_DEADLINE_COMPLETE: 4/4, NEXT_RUN_DUPLICATE_POST=0`. Hoàn tất phân tích POST ở 179,5 s được xác nhận; 180/181/500 s giữ pending, 1 PATCH/1 POST, mã 3, lượt sau đối soát không POST lại.

Registry hoàn tất rc 0: `PHẢN CHỨNG: 1677/1677 đỏ đúng`, `TỔNG: ĐẠT`. Python 3.12 cũng cho 477/478 và 285/289, rc 1 do cùng lỗi socketpair; không còn khoảng trống về việc chạy bằng 3.12, nhưng socket thật vẫn chưa đo được.

## Phạm vi lớp của finding mới

RV4-F01 có **một lớp, một cơ chế**, tái hiện ở nhiều vị trí cạn: `luot` đã có dữ liệu nhưng `kq['khung']` chỉ được điền sau vòng E; `return s1(...)` đi vòng qua phần dựng báo cáo. Không tách thành các finding cho T2/T5/F/P. Đã quét mọi đường trả của `_danh_gia`, lưới ngoại lệ ở `chay`, phần dựng `bc` và `main`: cả JSON stdout và summary dùng cùng báo cáo nên cùng mất dữ liệu. Những S1 trước khi D1/E được xác định (schema, danh sách không đọc được, quá nhiều khung) không phải bằng chứng cho phép bỏ các quan sát đã có. Lưới an toàn cũng tạo báo cáo rỗng khi có ngoại lệ bất ngờ; chưa tái hiện một lỗi dữ liệu thường riêng ở đường đó và không gán thêm finding.

Trong ma trận, cạn ở lượt đầu làm mất chi tiết phép gây cạn; cạn ở lượt sau còn làm mất lượt trước đã đủ T1–T7. Ca đích chốt trường hợp thứ hai, tổng trần **28.861**, gói cuối vượt, lượt 10 đã `dat`. H3 và H đều S1, `sha_audit=null`; chỉ H mất `id=10`, phán quyết và các mã phép con. Không có cáo buộc H trả `fresh` sai trong phản chứng này. Gợi ý chung là tách việc dừng thu thập khỏi việc xuất các quan sát đã có, vẫn giữ S1 và `dong_den` cũ. Đó là nghĩa vụ báo cáo hiện hữu, không phải quyền thêm giao thức hay cơ chế mới.

## Bảng điều kiện của B và write set

Nguồn phép đo là object Git, không phải tên nhánh. Đặc tả được lấy từ commit đóng băng và đo băm trước khi đọc; đã đọc toàn văn cùng CLAUDE, AGENTS và Protocol §8/§8.3/§12, lease và Mission r109. Lệnh chi tiết ở [baseline.py](evidence/baseline.py).

| Điều kiện | Thực đo |
|---|---|
| Không shallow, B trên first-parent master đã được cấp | `false`; B có trên first-parent `origin/master` tại `d0868dbf7f6324755aa4ed0f3e02d4efa84866f0` |
| B đúng merge B1a | 2 parent; subject merge PR #1516 |
| Schema tại B | `844b5218b6f6844945f5c4c9440f09015d238fe09a60d64b3787c440787e4f46` |
| Fixture tại B | `ce8595739a1ab2f4a86c9c196255e5f91fb19a9f6d3865df6caa2d66f9970e6d` |
| Khối Lệnh kiểm tại commit d1b08c2… | `d9c78e708e18a211b7d8c7309638ffd1c73200578cf3128f9f0fc4275430f24e`; 254 dòng / 14.992 byte |
| Bốn hàm nguyên văn | `tieu_dung` 6.885 byte; `khoa_tu_ten` 108; `doc_moc` 148; `khung_cron` 248. Từng đoạn nguồn trùng byte, băm đầy đủ trong log |
| Mốc và tham số thi công | committer B 2026-11-25T05:36:53Z; ceil cron 2026-11-28T19:17:00Z = KHUNG_DAU ở mã/lease/Mission; Issue 1520 cả ba |
| Job/upload B | `bien-nhan-audit`, upload `bien-nhan-audit-${{ github.run_id }}-${{ github.run_attempt }}`, path `bien_nhan_audit.json`; T3/X2 ra 11 tên, 11 khoá duy nhất |
| Ba tệp mới, registry ở B | Ba lần `git cat-file -e` rc 128 đúng kỳ vọng; mục registry mới xuất hiện 0 lần |
| Lease và trần | Hiệu lực theo `nang_tran`: tối đa 6 tệp / 3.500 dòng thêm; thực tế 4 / 3.415 |

| Đường dẫn trong B..H | Thêm | Xoá |
|---|---:|---:|
| `.claude/dev/ci_dang_ky_test.py` | 1 | 0 |
| `.github/workflows/canh-tuoi-audit.yml` | 29 | 0 |
| `ops/canh_tuoi_audit.py` | 1051 | 0 |
| `ops/canh_tuoi_audit_test.py` | 2334 | 0 |
| Tổng | **3415** | **0** |

Registry chỉ thêm đúng một mục `MOI` nguyên văn SPEC, không sửa/xoá mục khác. Quét **toàn bộ nội dung bốn tệp** và **16 commit message B..H**: không có dấu bỏ qua CI. H3..H chỉ hai tệp `ops/canh_tuoi_audit*.py`: sản phẩm +9/−6, test +113/−43. `git diff --check` rc 0. Hai clone H/B đều `core.abbrev=7`; các mutant là tệp rời, không phải clone khác.

## Bảng đo lại lời khai executor

Mọi Python dùng `-B` và `PYTHONDONTWRITEBYTECODE=1`; cwd mặc định là thư mục rv4, trừ khi ghi khác. Suite và mutant chạy dưới `ulimit -v 3000000`. Không sửa/bỏ ca socket để lấy rc 0.

| Lời khai / lệnh đã chạy | rc thực | Kết quả thực, đối chiếu |
|---|---:|---|
| `git -C src rev-parse HEAD HEAD^{tree}`; `sha256sum HANDOFF.yaml`; hash SPEC bằng object Git | 0 | Đúng H/tree và hai SHA256 đã nêu đầu báo cáo |
| `python3 -B out/evidence/baseline.py` | 0 | `BASELINE: DAT`; numstat, các điều B và ghim khớp |
| `python3 -B out/evidence/B1A-lenh-kiem.py review-tmp/B/ops/specs/wp1460-r1/hop_dong --dot-bien` | 0 | `FIXTURE: 480/480 phep kiem dung ky vong`; `DOT BIEN: giet 249/249 · vi tu 57 · noi long schema 192`; `TONG: DAT`. [Log](evidence/B1A-contract.log) |
| `python3 -B review-tmp/H/ops/canh_tuoi_audit_test.py` | **1** | Python 3.13.18: `CA: 477/478 dat`; `DOT BIEN: 285/289 bi giet dung ly do`; `TU KIEM PHAN HANG: DAT (5 dot bien)`; `TONG: DO`. Không tái lập 478/478, 289/289 do sandbox |
| Cùng suite bằng `/usr/bin/python3.12 -B`, `PYTHONPATH` trỏ `../g4/py312` | **1** | Python 3.12.3, cùng bốn dòng kết quả trên; dependency có sẵn ở scratch executor, không cài/sửa hệ thống. [Log](evidence/suite312.log) |
| `python3 -B .claude/dev/ci_dang_ky_test.py` (cwd `review-tmp/H`) | 0 | `PHẢN CHỨNG: 1677/1677 đỏ đúng`, `TỔNG: ĐẠT`; khớp. Registry mặc định không đồng nghĩa chạy mọi chương trình đã đăng ký |
| `actionlint -shellcheck /usr/bin/shellcheck .github/workflows/canh-tuoi-audit.yml` (H) | 0 | stdout/stderr rỗng; actionlint 1.7.7, ShellCheck 0.9.0. Không tự tạo dòng “PASS” |
| `python3 -m ruff check --no-cache --select F` ba tệp Python thay đổi H; registry B | 0 / 0 | Ruff 0.15.15: `All checks passed!` cả hai; F H=0, B=0, delta=0 |
| Registry kiểm hợp đồng Ruff/Windows | 0 | `RUFF CI: 3/3 hợp đồng`, `LAUNCHER WINDOWS: 4/4 hợp đồng`; đây là kiểm cấu hình, không phải chạy Windows hay thay thế bare lint |
| `python3 -B .claude/dev/packet_loop.py doctrine-scan --root .` / `adr-song --root .` (H) | 0 / 0 | Sạch 12 tệp; ADR 66/66 |
| `python3 -B out/evidence/rv3_deadline_coverage.py` **nguyên bản** | 0 | `RV3_DEADLINE_COVERAGE_COMPLETE`; Q01/Q02/Q03 gốc 0 → mutant 3, đúng tên ca cũ. Toàn 478 ca được gọi trên mỗi mutant; lỗi socket vẫn được tách riêng |
| Tám phép so, mỗi phép gỡ/biên/chỉ bằng | Đo riêng bên dưới | Đúng 8 phép so hạn thực thi. Trong 24 mục committed, 22 mục hoàn tất toàn bộ target; 2 mục `f02_nen_han`, `f02_nen_han_bien` còn target socket không đo được. Cả 24 có target mô phỏng phân biệt. Không ghi 24/24 đầy đủ thay executor |
| `python3 -B out/evidence/resource_stop.py` **nguyên bản** | 0 | `RESOURCE_STOP_COMPLETE`; cap 1/10637: 0 GET đánh giá/0 ZIP sau cạn; cap đủ fresh |
| `python3 -B out/evidence/resource_stop_signals.py` **nguyên bản** | **1** | Dòng 33 còn khẳng định mã hiện tại phải hỏng, nhưng hai ca thực tế rc 0. Giữ nguyên rc này trong bằng chứng |
| `python3 -B out/evidence/resource_stop_signals_g4.py` | 0 | `RESOURCE_STOP_SIGNALS: 2/2 CURRENT_CODE_MEETS_NAMED_EXPECTATION`; byte-diff chỉ dòng 33–34 |
| Năm chốt `f04:*`, ca T2/T5/same-ZIP | 0→3 từng target | 5 mutant / 7 cặp đều GIẾT đúng tín hiệu, không sống/khác lý do; [JSON](evidence/rv4-mutations.json) |
| Mã pha mở trùng H3 | 0 | `STATIC_AUDIT_COMPLETE`; 6/6 đoạn hàm/lớp bằng byte; miễn được giữ |

Ba probe yêu cầu chạy nguyên bản được so byte với `review-3/evidence/`, đều bằng nhau. [Provenance](evidence/probe-provenance.json) giữ hash và đúng hai dòng sửa của bản `_g4`; không dùng bản sửa để xoá rc 1 của bản gốc.

`python3 -B out/evidence/rv4_inventory.py` rc 0: `INVENTORY_CASES 469 -> 478 ADDED 9 REMOVED 0`; `INVENTORY_MUTANTS 275 -> 289 ADDED 14 REMOVED 0`; `DEADLINE24 24 SOCKET_TARGETS ['f02_nen_han', 'f02_nen_han_bien'] D134 []`. [Danh sách đầy đủ](evidence/rv4-inventory.json).

## Bảng đột biến độc lập

**Quy tắc tín dụng:** từng cặp phải có bản gốc rc 0 và mutant rc 3 mang `DO:<đúng tên ca>:` từ `TinHieuChotCa`. Không tính ngoại lệ vô can, `KeyError`, timeout của runner hoặc permission denial là giết. Một biến thể có target giết không có nghĩa mọi target được chạy đều giết; bảng giữ cả cặp sống và sai lý do.

Lệnh `python3 -B out/evidence/rv4_mutations.py` chạy xong **53 biến thể / 175 cặp** rồi rc **1**, vì assertion cuối yêu cầu không có cặp sai lý do. Output thật: `SURVIVING_VARIANTS [] WRONG_REASON_PAIRS 6`. Phân loại chi tiết: **125 GIẾT đúng / 44 SỐNG ở cặp đó / 6 GIẾT SAI LÝ DO**. Cả 53 biến thể có ít nhất một target giết đúng; không diễn đạt kết quả này thành “175/175” hoặc “script đạt”. [Log](evidence/rv4-mutations.log), [mọi cặp](evidence/rv4-mutations.json).

| Chốt tại H | Biến thể độc lập | GIẾT / SỐNG / sai lý do theo cặp | Ca phân biệt chính |
|---|---:|---:|---|
| d104, dòng 370 — trước chờ | 6 | 11 / 7 / 0 | `n15_cho_qua_han`, `n15_cho_dung_han`, `n15_cho_con_han` |
| d106, dòng 887 — hoàn tất bước ghi/đọc | 6 | 13 / 5 / 0 | `n15_han_cuoi_ghi`, `n15_han_cuoi_ghi_bien`, đối chứng fresh |
| f02:d14, dòng 984 — sau khớp đối soát | 6 | 11 / 7 / 0 | `n15_d14_khop_qua_han`, `dung_han`, `con_han` |
| d105, dòng 357 — trước lần thử | 6 | 13 / 5 / 0 | `n15_goi_dung_han`, `qua_han`, `kep_timeout` |
| d99, dòng 955 — kết thúc đánh giá | 6 | 13 / 5 / 0 | `n15_tinh_cuoi_qua_han`, `phan_tich_qua_han`, fresh |
| w0:tron_ven, dòng 939 | 6 | 13 / 5 / 0 | `n15_w0_bien`, `w0_phan_tich_qua_han`, fresh |
| f02:vong_doc, dòng 342 | 6 | 20 / 10 / 6 | biên/quá hạn; GET API/kho, PATCH, POST, fresh |
| f02:nen_han, dòng 316 | 6 | 24 / 0 / 0 | `n15_nen_get_api/get_kho/patch/post` |
| f04:goi, dòng 246 | 1 | 1 / 0 / 0 | `n2_can_tn_cung_goi` |
| f04:t5, dòng 590 | 1 | 1 / 0 / 0 | `n2_can_tn_t5` |
| f04:t3, dòng 637 | 1 | 1 / 0 / 0 | `n2_can_tn_t2` |
| f04:t7, dòng 653 | 1 | 2 / 0 / 0 | `n2_can_tn_t2/t5` |
| f04:e, dòng 717 | 1 | 2 / 0 / 0 | `n2_can_tn_t2/t5` |

Với `>=`, sáu thay thế là `>`, `==`, `!=`, `<`, `<=`, gỡ chốt; với `<=` là `<`, `==`, `!=`, `>`, `>=`, gỡ chốt. **44 cặp sống được giữ đủ trong JSON**: ví dụ `d104_gt` sống ở ca quá hạn nhưng chết ở ca đúng hạn; `d104_eq` sống ở ca đúng hạn nhưng chết ở ca quá hạn. Đây là lý do phải giữ cả hai đầu vào. Sáu cặp sai lý do là `f02_vong_doc_{ne,lt,le}` × `n15_vong_doc_{patch,post}`: `KeyError 'W2'` hoặc `'W5'`, rc 4; **không tín dụng**. Các biến thể ấy vẫn bị ca GET/quá hạn/fresh giết đúng. Không tìm thấy một biến thể sống trên toàn bộ nhóm ca phân biệt đã chọn.

| Bộ đo hồi quy / lệnh tại `out/evidence/` | rc | Kết quả phân biệt |
|---|---:|---|
| `python3 -B rv3_deadline_coverage.py` | 0 | Q01–Q03: 3/3 gốc 0 → mutant 3 tại chính ba ca tên cũ |
| `python3 -B reviewer_mutations_rv4.py` | 0 | 29 biến thể R, 45 cặp: 35 GIẾT / 10 SỐNG / 0 sai lý do; mọi biến thể có ca giết |
| `python3 -B rv2_mutations_g3.py` | 0 | N01–N12: 12/12 GIẾT đúng ca mới committed |
| `python3 -B rv2_distinguish.py` | 0 | `RV2_DISTINGUISH: 9/9 GIET DUNG CA DICH`, quan sát độc lập giữ nguyên |
| `python3 -B rv2_heartbeat_callers.py` | 0 | `HEARTBEAT_WRITER_CALLERS 192 GIET 192 ORIGINAL_OK 192`; có 64 cặp caller/điều kiện khác nhau, lặp ba lần vì target của D61 nay khai đủ W0/W2/W7, không tính thành 192 điều kiện độc lập |
| `python3 -B rv3_body_deadlines.py` | 0 | `BODY_PAIRS 84 ORIGINAL_OK 84 GIET 84`; 4 đường phương thức/host, success/error, length/chunked/EOF; lớp HTTP thật trên raw giả, không socket thật |
| `python3 -B rv4_test_structure.py` | 0 | `TEST_STRUCTURE_EQUIVALENT 65 PAIRS: ORIGINAL_AND_12_MUTANTS` |

Mười cặp R còn sống ở **target cũ**, không bị che: R23 tại `n1_s_khong_auth` và `n1_r_qua_3`; R24 tại `n9_ma_thoat`; R25 tại `n1_han_goi` và `n15_kep_timeout`; R26 tại `n0_nen_fresh`; R27 tại `n1_lien_ket_event` và `n1_lien_ket_cuoi`; R28 tại `n1_u6` và `n1_chua_xong`. Target phân biệt đã commit nay giết: R23/R25 → `n16_transport_that`; R24 → `n9_main_ma_thoat`; R26 → `n1_s_khong_auth`; R27 → `n1_lien_ket_cuoi_event`; R28 → `n1_u6_run_attempt`. R22 có thêm `n1_j_doc_theo_khuc`, chết đúng dưới giới hạn bộ nhớ. [Kết quả R](evidence/reviewer-mutations.json).

**Săn phép so hạn thứ chín:** duyệt mọi `ast.Compare` toàn mô-đun, đối chiếu toàn bộ lần đọc/đặt `dong_ho`, `han`, `het`, `con`, và đọc luồng gọi. Có đúng tám phép so trên. `min(HAN_GOI, con)` là kẹp timeout, không phải phép so Boolean thứ chín; nó được `n15_kep_timeout` bảo vệ. S7/S8 và các mốc 24 giờ của nhịp tim là tuổi lịch/dữ liệu, không phải ngân sách thực thi. Không thấy alias hạn hoặc một đường đọc body khác bỏ qua tám vị trí này. Không suy ra miễn cưỡng chế pha mở từ phép đếm này.

## Đối chiếu từng finding các lượt trước

Nguồn bất biến: lượt 1 H1 `127b82a8a9e41fda3c4a230810118f0bedfb200d`; lượt 2 H2 `d3bcd6a171644b18d9fd37a185cfb8fc6d641ef4`; lượt 3 H3 `c524d1233c2709679e31cd972711d4b8d5534fa8`. Đã đối chiếu các verdict ở `review-1/`, `review-2/`, `review-3/`. Nhãn **VÁ HỜ** ở các hàng có thiếu phép socket là cách đếm bảo thủ theo §8.3: biểu hiện đã đo được đã sửa, nhưng chưa chứng nhận đóng **toàn lớp**; không tạo thêm finding P2 vì sandbox.

| Finding nguồn | Đúng một nhãn | Phép đo và phạm vi còn lại |
|---|---|---|
| Lượt 1 F01 — `rest-response-domain-incomplete` | **ĐÃ SỬA ĐÚNG LỚP** | N02–N05 giết đúng; ca attempt/run/job/artifact của suite đạt. Thiếu body W0/W3/W8 nay trả rc 3 có báo cáo; null body đối chứng rc 0. Rà lớp J, D1, T1/T7/U6, D6/D7, Issue/comment và heartbeat; không thấy biểu hiện cùng cơ chế còn hở |
| Lượt 1 F02 — `bounded-evaluation-order-dependent` | **VÁ HỜ** | Tính S cuối/W0/D14 đã bị chặn; R08/R09, Q và 84 cặp body đạt. 3.12 đã chạy lại; socket thật vẫn không đo được. Miễn pha mở tách riêng, không dùng để giữ nhãn |
| Lượt 1 F03 — `mutant-oracles-non-discriminating` | **VÁ HỜ** | R22–R28 nay có ca đúng giết, D134 ngoài mẫu số đúng miễn, Q01–Q03 đã đóng. Còn 4 mục committed không hoàn tất target socket, không tuyên bố toàn bộ bảng đã được kiểm độc lập |
| Lượt 2 F02 — body có đệm | **VÁ HỜ** | `_NenCoHan` dùng read1 và timeout còn lại; 84 cặp success/error/framing qua đủ 4 đường. Không có phản chứng body còn hở trong mô hình đo; thiếu socket thật như trên |
| Lượt 2 F03 — N01–N09 và D61 nơi ghi | **VÁ HỜ** | 12/12 N committed, 9/9 oracle độc lập, 64 cặp writer khác nhau đều giết đúng; không còn lỗi N06 chết do HTTPError vô can. Không đóng toàn lớp oracle khi 4 mục còn target không đo được |
| Lượt 3 RV3-F03 — ba đầu vào quá hạn bị thay | **VÁ HỜ** | **Ba biểu hiện đã sửa:** Q01–Q03 0→3 đúng ca nguyên bản; 8 chốt có gỡ/biên/chỉ-bằng, 53 biến thể độc lập có ca phân biệt. Nhãn toàn lớp vẫn bảo thủ vì 2/24 mục hạn còn socket target chưa đo, không phải vì Q còn sống |
| Lượt 3 RV3-F04 — không dừng sau cạn tổng | **VÁ SINH LỖI MỚI** | Cơ chế tiêu tài nguyên đã sửa đúng: 80 lượt/40 vị trí, 0 việc đánh giá sau cạn; 5 chốt/7 cặp giết. Nhưng trả sớm làm mất báo cáo đã có: RV4-F01, H3=0/H=3 ở ca mục 6. Không đổi slug lỗi cũ thành lỗi báo cáo để che lịch sử |

## Đối chiếu các lớp đặc tả

Nhãn ở đây nói về **cơ chế của lớp**, khác bảng trên đánh giá hệ quả của từng lần vá. Vì vậy `unbounded-artifact-expansion` được đóng ở đường hiện tại, trong khi lần vá RV3-F04 được xếp sinh lỗi mới ở lớp báo cáo. Đây là hai quan sát khác nhau, không thay tên lớp để lấy tín dụng.

| Lớp | Đúng một nhãn | Bằng chứng / quét cùng lớp |
|---|---|---|
| `notification-dedup-before-delivery` | **ĐÃ SỬA ĐÚNG LỚP** | R12/R13, R14/R15 và các ca pending, đối soát/cửa sổ trong suite; POST 180/181/500 còn pending, lượt sau 0 POST, cùng comment được xác nhận. Không mở rộng bảo đảm vượt ranh giới Issue/heartbeat còn đọc được |
| `write-retries-violate-delivery-contract` | **ĐÃ SỬA ĐÚNG LỚP** | R10/R11 giết đúng; GET retry riêng, mỗi PATCH/POST logic đúng một lần gửi vật lý |
| `b1-consumer-contract-mismatch` | **ĐÃ SỬA ĐÚNG LỚP** | Bốn hàm trùng byte, schema/fixture ghim; suite chạy 120 hình/118 ngữ nghĩa; chính sách byte T2/T5 và C10 giữ nguyên |
| `consumer-freshness-anchor-unverified` | **ĐÃ SỬA ĐÚNG LỚP** | R06/R07/R27/R28; LIÊN KẾT dùng chung ở T1/T7, U6 từng trường, neo unknown thắng T2/T3/T6; không dùng rerun/dispatch làm mới snapshot |
| `freshness-forgets-overdue-obligations` | **ĐÃ SỬA ĐÚNG LỚP** | R05, nhóm n4 R/O, đóng tay trước E, `dong_den` liên tục; F xanh không xoá nghĩa vụ; S1 giữ `dong_den` trong mọi lượt cạn đã đo |
| `bounded-evaluation-order-dependent` | **VÁ HỜ** | Lịch E/artifact tất định; tám guard, W0 và D14 sau parse/khớp, body/HTTPError đủ đường đã đo. Chưa đủ socket thật; waiver chỉ pha mở |
| `heartbeat-value-domain-incomplete` | **ĐÃ SỬA ĐÚNG LỚP** | Bộ kiểm chung W0/W2/W7, R16/R29, 64 cặp writer khác nhau; suite hậu kiểm khứ hồi mỗi ca. Miền ID/mã/khoá và nullable giữ đúng |
| `unbounded-artifact-expansion` | **ĐÃ SỬA ĐÚNG LỚP** | J/S cap byte, ZIP cap mục/gói, R17–R19; cap tổng 80 lượt, 2 ca cùng ZIP, đúng tổng fresh, cả 5 stop mutant giết. Không còn đường caller hiện tại làm I/O/giải nén sau cạn. Lỗi mất báo cáo ghi dưới RV4-F01 riêng |
| `workflow-step-controls-unconstrained` | **ĐÃ SỬA ĐÚNG LỚP** | Allowlist từng tầng/bước; nhóm n10, R20/R21 giết, actionlint đạt. Không dispatch để suy diễn vận hành |
| `mutant-oracles-non-discriminating` | **VÁ HỜ** | Các lỗ Q/R/N đã có quan sát phân biệt, phân hạng loại rc 4; nhưng suite nguyên trạng không hoàn tất 4 mục có socket, không nhận tổng executor thay phép đo |
| `markdown-state-table-column-drift` | **KHÔNG ÁP DỤNG** | B..H không sửa Markdown/SPEC; lỗi thuộc tài liệu đặc tả cũ |
| `merged-misreported-as-landed` | **KHÔNG ÁP DỤNG** | Không merge/land và không sửa phát biểu trạng thái ấy; review không chứng nhận landed |

Tổng bảng đặc tả: 8 lớp ĐÃ SỬA ĐÚNG LỚP, 2 VÁ HỜ, 2 KHÔNG ÁP DỤNG. Lớp mới `evaluation-report-evidence-dropped` còn P2, không nằm trong mẫu số lịch sử để làm tăng tỷ lệ sửa. Lịch sử oracle qua các lượt đặc tả/mã nguồn được giữ nguyên.

## BẢNG SĂN — giả thuyết và phép đo đã chạy

Chỉ dùng fixture REST JSON và ZIP dữ liệu thường, đồng hồ/trần tiêm; không soạn payload tấn công. Các hướng thù địch dưới đây là mô tả, không hướng dẫn khai thác.

| Hướng / giả thuyết | Phép đo đã chạy | Kết quả |
|---|---|---|
| Sai B/ghim khiến acceptance vô nghĩa | `baseline.py`, Git object, hash, bốn hàm | Baseline đạt, không có blocker nền |
| Guard thứ chín bị bỏ khỏi bảng | `static_audit.py`, quét mọi tham chiếu hạn/đồng hồ, AST Compare toàn mô-đun | Đúng 8 guard ngân sách/lần thử; không tìm được thứ chín |
| Khôi phục tên ca nhưng không khôi phục đầu vào quá hạn | Q01–Q03 nguyên bản; 48 mutant toán tử | Ba ca cũ đều giết `==`; biên và đối chứng riêng còn phân biệt |
| Hai cấu trúc test tương thích che nhảy đồng hồ | `rv4_test_structure.py` chuẩn hoá trên test tạm | 65/65 cặp kết quả giống hệt, gồm gốc và 12 mutant; không thấy che lỗi |
| Cạn ở gói đầu, giữa T5, giữa E, gói cuối vẫn đọc tiếp | `resource_stop.py`, `rv4_resource_matrix.py`, 5 mutant stop | 0 I/O/ZIP đánh giá sau cạn ở mọi vị trí đã đo; ngay cả cùng khúc/tệp sau đều dừng |
| Trả sớm S1 làm mất dấu vết đã biết | `rv4_report_contract.py`, ma trận tài nguyên | Có: H3 rc 0 → H rc 3 đúng ca; 40 lượt có run dat trước đó vẫn `khung={}`; RV4-F01 |
| Đúng bằng tổng bị coi là cạn | Ma trận tổng 28.862 và 28.861, ca n2_tong_vuot | Bằng trần fresh/sha đúng; thiếu 1 byte S1/sha null/1 PATCH/rc 1 |
| POST đến máy chủ nhưng phản hồi hoàn tất muộn bị ack hoặc gửi đôi | `rv4_post_deadline.py`, `additional_probes.py` | 179,5 s xác nhận; 180/181/500 s giữ pending, lượt sau đối soát và 0 POST |
| Một read có đệm/HTTPError trốn hạn body | `rv3_body_deadlines.py`, n15 nền, N06 | 84/84 cặp phân biệt; socket thật bị sandbox từ chối, không giả đã đo |
| REST thiếu trường/kiểu sai gây xanh giả hoặc crash | `rv2_distinguish.py`, `ordinary_inputs.py`, `additional_probes.py` | REST sai miền bị từ chối; thiếu body W0/W3/W8 rc 3 có báo cáo; null đối chứng đúng |
| Bộ kiểm miền chỉ bảo vệ đọc mà bỏ nơi ghi | `rv2_heartbeat_callers.py`, R16/R29 | 64 cặp W2/W7 khác nhau giết đúng; không PATCH với heartbeat tự sinh ngoài miền |
| Phân trang/đổi thứ tự che phần chưa đọc | `pagination_ordinary.py`, n15_thu_tu_goi và ma trận đảo D1 | Lặp trang bị từ chối sau 10 GET; mất trang sau 1 GET; thứ tự đảo không đổi điểm cạn/việc sau cạn |
| F xanh xoá nghĩa vụ hoặc attempt mới làm mới tuổi | R05/R06/R07/R27/R28, nhóm n4/n5 toàn suite | Không tìm lỗi mới; neo/ưu tiên/nghĩa vụ được bảo vệ |
| Ghi retry hoặc xoá/thay pending | R10–R15, ca stateful committed | Mutant giết đúng, không tìm lỗi mới trong giao thức đã đo |
| Workflow/registry hoặc commit bỏ qua CI | `static_audit.py`, actionlint, registry, n10 | Đúng write set/literal MOI; 0 dấu bỏ qua; gate đạt |

## Phán bốn câu hỏi executor

1. **Không chấp nhận `khung: {}` ở S1 đã có E và dữ liệu đánh giá.** Mục 6 không miễn báo cáo từng khung/lượt khi cạn tổng; “tất-cả-hoặc-không” ở mục 3 ràng buộc kết luận S/SHA/tiến `dong_den`, không buộc xoá bằng chứng chẩn đoán. Phản chứng chỉ đòi giữ lượt 10 đã hoàn tất, không ép kết luận cho lượt chưa đánh giá. Nếu không thể sửa trong authority hiện hành thì cần chủ kho xử lý mâu thuẫn phạm vi/acceptance; reviewer không tự miễn hay cấp lượt mới. RV4-F01.

2. **Mã pha mở thật sự trùng byte, miễn áp nguyên theo chỉ dẫn của chủ kho trong yêu cầu review này.** `_mot_lan`, `_goi`, `transport_that`, `_NenCoHan`, `_NguCanh`, `_KhongChuyenHuong`: 6/6 bằng byte, hash riêng ở `static-audit.json`. H3..H sản phẩm chỉ đổi bốn hàm tài nguyên. Không cần suy từ tên nhánh hay lời khai executor.

3. **Không thấy hai cấu trúc test che lỗi.** W8 `180.0` rồi cộng `qua` đạt đúng 180/181, không có phép đọc đồng hồ xen hai phép gán. D14 hai wrapper lồng vẫn gọi hàm gốc đúng một lần và tổng nhảy 180+qua, cho 179/180/500; context manager khôi phục đúng. Thay bằng biểu thức tổng/wrapper đơn trên bản test tạm cho kết quả giống hệt ở 65 cặp gồm bản đúng và 12 mutant. Chúng khó đọc hơn cần thiết nhưng không thành finding P0–P2.

4. **Đủ đóng hành vi tiếp tục tiêu tài nguyên ở các caller hiện có.** `f04:goi` dừng cùng ZIP; `f04:t5` dừng artifact kế; `f04:t3`/`f04:t7` dừng I/O còn lại của lượt; T5/T6 phụ thuộc kết quả nên không chạy thêm; `f04:e` dừng lượt E kế. Năm guard bị gỡ riêng đều có target đúng giết; ma trận 40 vị trí × 2 thứ tự và cùng ZIP cho 0 việc sau cạn. Không cần thêm chốt trung tâm chỉ để làm một lời gọi trực tiếp không thể tới từ luồng sản phẩm xanh. Đây là kết luận cho graph hiện tại, không bảo đảm caller tương lai. Phần **báo cáo** của cách trả sớm vẫn sai như câu 1.

## Rủi ro tồn dư đã miễn

- [Quyết định 7162892740](https://github.com/ducthangho/tra-luat/issues/1172#issuecomment-7162892740) neo H3: DNS/connect/TLS/gửi request/đọc status+header **trong pha mở `urllib.open()`** chỉ có socket timeout từng thao tác, chưa có hạn tuyệt đối cho toàn pha; kết quả mở muộn bị các chốt sau đó từ chối. So byte cho phép giữ miễn ở H theo yêu cầu chủ kho. Không gán P0–P2. Không mở rộng miễn sang body, HTTPError, W0, D14, retry/chờ, hoàn tất POST hay giải nén.
- [Quyết định 7157619068](https://github.com/ducthangho/tra-luat/issues/1172#issuecomment-7157619068): quan sát dòng đột biến 134 bất khả với schema ghim, **ngoài mẫu số, không tín dụng**. D134 không còn trong bảng thực thi; không đòi khôi phục một ca đổi quan sát để lấy kill.
- [Review Rescue lần hai 7163782461](https://github.com/ducthangho/tra-luat/issues/1172#issuecomment-7163782461): executor 5/5 chỉ vá RV3-F03/F04, review này 4/4 cuối. Đã đọc cả ba comment bằng công cụ GitHub **chỉ đọc**, lưu [nội dung](evidence/owner-comments.json). Quyết định Rescue không miễn nội dung báo cáo ở SPEC §6.

## KHÔNG ĐO ĐƯỢC / không chạy

| Phần | Trạng thái, giới hạn |
|---|---|
| `n16_socket_that` | **not_measured** trên cả Python 3.13.18 và 3.12.3: `socket.socketpair()` bị `PermissionError: [Errno 1] Operation not permitted` ngay trên mã gốc. Không vượt quyền hay thay API để lấy xanh |
| Bốn mutant phụ thuộc ca đó | `f02_nen_han`, `f02_nen_han_bien`, `f02_nen_socket`, `f02_nen_loi` không hoàn tất toàn bộ target. Những target mô phỏng được chạy và phân biệt, nhưng không thay phép socket thật |
| Socket/TLS/HTTP loopback và thời gian thực | Không đo; 84 cặp dùng HTTPResponse/BufferedReader thật nhưng nền/đồng hồ giả. Phụ thuộc `SocketIO._sock` chưa được xác nhận bằng phép socket của reviewer |
| Windows M3, selftest toàn kho, registry `--chay`, M9, CI PR | Không chạy trong review chỉ đọc này. Kiểm hợp đồng launcher/registry không thay những gate ấy; lease không có miễn Windows |
| Giao tin GitHub thật, người nhận thật, nghiệm thu sau merge | Không chạy; không gửi comment/PATCH, không dispatch. Không chứng nhận vận hành, push/merge/land |
| Ref remote sau snapshot clone được cấp | Không fetch vào src; chỉ chứng minh B trên first-parent của refs được bàn giao |
| Model/effort phục vụ | `KHONG_DO_DUOC`, không dùng tên yêu cầu làm attestation. Provider/surface/session ghi riêng bên dưới |
| Byte `.git` trước/sau | Snapshot nội dung chỉ phủ toàn worktree ngoài `.git`; Git HEAD/tree/status/diff/index có đối chiếu. Không tuyên bố đã băm mọi object/ref/config `.git` tại hai mốc |

## Receipt thực thi, tính chỉ đọc và điểm dừng

Reviewer: provider **OpenAI Codex**, execution surface **API tool shell**, transport **machine/local**; `CODEX_SESSION_ID` và `CODEX_THREAD_ID` cùng **01a21333-975e-7b40-ad5b-eacb8cd92056**, đo từ biến môi trường đúng tên, không lấy GitHub actor làm reviewer. Sandbox **workspace-write**, approval **never**, `CODEX_SANDBOX_NETWORK_DISABLED=1`. Prompt chỉ đọc không được mô tả thành sandbox read-only. [Identity](evidence/reviewer-identity.json).

Snapshot trước/sau gồm tracked, untracked và ignored ngoài `.git`: **18.097 → 18.097 tệp; 0 đổi băm, 0 thêm, 0 xoá**. HEAD/tree đúng H, status/diff/index không đổi và rỗng. `python3 -B out/evidence/finalize_evidence.py` rc 0: `READONLY_COMPLETE 18097 FILES; CHANGED=0 ADDED=0 REMOVED=0; GIT_STATE_EQUAL`. [Kết quả](evidence/readonly-result.json), [trước](evidence/src-before.json), [sau](evidence/src-after.json). Chỉ chứng minh hai mốc quan sát không có delta, không phải chứng minh tuyệt đối mọi thời điểm trung gian.

Mọi bản sao, mutant, probe/output mới ở ngoài `src/`. Không commit, push, GitHub ghi hoặc dispatch. Các script có đường tương đối `parents[2]`; muốn chạy lại cần dựng `review-tmp/H` đúng H và `review-tmp/B` đúng B, đặt `core.abbrev=7`, giữ các gói Python cần thiết; lệnh mutant phải giữ giới hạn bộ nhớ. Script tạo mutant có lưu định nghĩa/target và output từng cặp trong `out/evidence/`, không cần giữ bản mã đã đột biến để đọc kết quả. `rv4_mutations.py` tạo các mutant trước khi chạy `rv4_test_structure.py`; `rv2_mutations_g3.py` tạo đường mutant cho `rv2_distinguish.py`. Thư mục `review-tmp/` do reviewer tạo đã được dọn; giữ toàn bộ `out/`. Hash/size hiện vật ổn định nằm trong `out/artifact-manifest.json` sau khi mọi writer kết thúc.

**Đây là lượt cuối, không tự mở lượt 5.** Báo cáo chuyển kết quả và giới hạn đo cho chủ kho/điều phối theo authority hiện có; không chuyển vai executor, không tự sửa SPEC hay mã để biến verdict xanh. Tồn tại RV4-F01 P2 nên kết luận cuối là `changes_requested`, độc lập với việc môi trường khác có chạy được ca socket hay không.
