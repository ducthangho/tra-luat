VERDICT: changes_requested

reviewed_sha: 127b82a8a9e41fda3c4a230810118f0bedfb200d
reviewed_tree: 862746ce6dae133012b0cfce90bf4913c8784c41
spec_sha256: 345520e199ba7072c2bea92b876a3db1877cabce7969f82a379bb078d1dc2e4d

Kết luận: **changes_requested — 3 finding P2, không có P0/P1.** Baseline đạt, không phải `blocked`. Các cổng đã chạy xanh nhưng chưa đủ để approve.

- **Spec: changes_requested** — F01, F02, F03.
- **Standards/Security: changes_requested** — kiểm dữ liệu ngoài chưa đầy đủ; hạn tổng chưa được cưỡng chế hết; các chốt của transport thật chưa được bộ ca bảo vệ (F01–F03).

Reviewer độc lập: `provider: openai_codex`; `execution_surface: codex_service` (API/tool có shell, không có bằng chứng được khởi chạy qua CLI/Desktop); `transport: machine`. Review class sensitive, generation 2, lượt review **mã nguồn 1**. Model/effort yêu cầu gpt-6-astra, suy luận cao nhất; `served_model/served_effort: KHONG_DO_DUOC` vì không có telemetry phục vụ độc lập. Không dùng danh tính tài khoản GitHub làm reviewer identity. Không gọi GitHub ghi, không dispatch, không sửa src.

Đã đo đầu vào: HEAD/tree, băm SPEC và HANDOFF đều khớp; git status --short rỗng (rc 0). Snapshot băm toàn bộ tệp, kể cả ignored và .git: evidence/snapshot-before.json.

## Baseline và write set (đã đo)

Lệnh: `PYTHONDONTWRITEBYTECODE=1 python3 -B out/evidence/baseline.py`; rc 0; dòng dương `BASELINE: DAT`. Log đầy đủ: [baseline.log](evidence/baseline.log).

| Điều kiện | Số đo |
|---|---|
| B trên first-parent; không shallow | PASS; origin/master `437257a3cad68bdec7c646aa99ccd4f5fd4256da`; `false` |
| B merge PR B1a | Hai parent; subject `Merge pull request #1516 from ducthangho/agent/wp1460-r9-g4-fable` |
| Schema/fixture tại B | `844b5218…` / `ce859573…`, khớp đầy đủ GHIM-B1A |
| Khối Lệnh kiểm | `d9c78e708e18a211b7d8c7309638ffd1c73200578cf3128f9f0fc4275430f24e`; 14992 byte, 254 dòng |
| Bốn hàm chép nguyên văn | 4/4 bằng byte, trích theo AST và giữ nguyên dòng nguồn; băm riêng trong log |
| KHUNG_DAU | committer B `2026-11-25T05:36:53Z`; floor `2026-11-21T19:17:00Z`; khung nhỏ nhất ≥ committer = `2026-11-28T19:17:00Z`, khớp mã/lease/Mission |
| Job và upload ở B | `bien-nhan-audit` có upload đúng name/tệp; T3 cho 11 tên, 11 khoá phân biệt |
| Ba tệp mới vắng tại B | 3 lần `git cat-file -e` rc 128, đúng kỳ vọng |
| Registry tại B | 0 chuỗi `canh_tuoi_audit_test` |
| Numstat B→H | 4 tệp: registry +1; workflow +29; module +1000; test +1843; tổng +2873/−0, trong trần 6/3500 |

Không fetch vào `src/` vì checkout chỉ đọc; phép first-parent dùng toàn bộ refs đã được cấp theo prompt. Không xác nhận refs remote tại thời điểm hiện tại bằng mạng. Hai bản sao H/B đều đặt `git config core.abbrev 7`.

## Findings

Lệnh probe dưới đây chạy từ thư mục gốc phiên, có `PYTHONDONTWRITEBYTECODE=1`. Chúng rc 0 nghĩa là hoàn tất phép đo; **không có nghĩa sản phẩm đạt**. Kết quả sản phẩm/tiến trình con nằm trong output. Đường tệp trong bảng tính từ `src/`, trên đúng H.

| ID | Mức | Lớp nguyên nhân | Tệp:dòng | Mô tả, ảnh hưởng và bằng chứng chạy được | Gợi ý vá |
|---|---|---|---|---|---|
| F01 | P2 | `rest-response-domain-incomplete` | `ops/canh_tuoi_audit.py:418`, `:850`, `:864`, `:896` | T1 chưa kiểm miền dương của attempt, kiểu `conclusion` và `digest`; `_hinh_issue` coi thiếu `body` như `null` nhưng nơi dùng truy cập trực tiếp. `python3 -B out/evidence/reviewer_probes.py` rc 0: `run_attempt_zero` / `job_attempt_zero` có T1 `dat`; `unused_artifact_digest_number` cho `fresh`, exit 0. `python3 -B out/evidence/additional_probes.py` rc 0: `missing-issue-body` ném `KeyError 'body'` tại **W0, W3, W8** (lần lượt PATCH/POST = 0/0, 1/0, 2/1), không trả báo cáo/mã 3 như hợp đồng. Đối chứng body `null` và REST đúng đều đạt. T1 kế thừa K1 của B3 ghim; lớp J đòi đúng hình trước khi dùng. | Hoàn thiện kiểm miền ở biên, phân biệt thiếu khoá với giá trị nullable; dùng bộ kiểm chung tại cả ba nơi đọc Issue. Giữ dữ liệu sai REST ở `khong_do_duoc`; lỗi đọc Issue vào luồng lỗi ghi có báo cáo. |
| F02 | P2 | `bounded-evaluation-order-dependent` | `ops/canh_tuoi_audit.py:305`, `:678`, `:895`, `:909`, `:985` | Hạn chưa bao phủ toàn công việc. Probe `late_final_calculation`: tính O sau chốt đồng hồ làm clock = 601 nhưng vẫn `fresh`, SHA khác null, exit 0. Probe `W0-heartbeat-parsing-budget`: đọc/kiểm nhịp tim tiêu 181 s **sau** lúc chốt `w0_dung`; W0 vẫn `moi`, PATCH 1, exit 0. `_mot_lan` không có hạn tổng cho vòng đọc; luồng thường 3 khúc × 20 s vẫn HTTP 200 dù timeout truyền = 30, kể cả hạn pha = 40. Các lệnh probe trên rc 0; [log chính](evidence/reviewer-probes.log), [log bổ sung](evidence/additional-probes.log). | Kiểm thời điểm hoàn tất sau phép tính cuối và trên mọi đường trả S; tính toàn bộ W0 vào hạn ghi; cưỡng chế hạn tuyệt đối cho lần thử và luồng đọc thật, không chỉ truyền socket timeout. |
| F03 | P2 | `mutant-oracles-non-discriminating` | `ops/canh_tuoi_audit_test.py:627`, `:642`, `:822`, `:1591`, `:1786`; các chốt tại `ops/canh_tuoi_audit.py:310`, `:569`, `:978`, `:985`, `:997` | `207/207` là output thật nhưng chưa chứng minh đúng quan sát/đủ chốt. D134 giữ số D5 ngoài biên nhận **0→0**; ca đỏ do S1 `danh_gia_nem:builtins.KeyError`, không phải quan sát 0→≥1 đã đóng băng. Sáu đột biến R22/R23/R24/R25/R27/R28 sống qua **320/320** ca, rc 0 từng bản: bỏ đọc theo khúc, bật redirect tự động, main luôn trả 0, bỏ timeout adapter, bỏ `event` ở D2 cuối, bỏ `run_attempt` của U6. `python3 -B out/evidence/run_survivors.py` rc 0 (runner đo xong), kết quả từng bản trong [survivor-results.json](evidence/survivor-results.json). `oracle_audit.py` rc 0: hai ca mới của reviewer cho gốc rc 0 → mutant rc 3 với `DO:review_T7_event:` / `DO:review_U6_attempt:`, chứng minh không tương đương. | Sửa kiểm kê từ chốt thực chạy và từng nơi gọi; thêm ca tới `transport_that`/`main`; đo riêng trường D2/U6. D134 phải báo điều phối giải quyết quan sát bất khả thi, không tự đổi tiêu chí nghiệm thu để lấy tín dụng. |

**Quét theo lớp (§8.3), ca khoá và rủi ro của gợi ý:**

- **F01** còn ở cả run/job/artifact và cả W0/W3/W8 của Issue; không phải một field đơn lẻ. Đã dò các validator của D1, T1, D6/D7, D8/D9, D10–D14 và đường dùng sau kiểm. D1 có kiểm thời gian/danh tính chặt hơn; D8/D9 không đổi S; W6 dùng `.get` nên thiếu body thành lỗi đọc lại, không tái hiện KeyError ấy. Ca cần thêm: mỗi loại attempt 0/âm; conclusion số; digest số ở artifact không được chọn; ba nơi Issue thiếu `body`, và đối chứng `body: null`. Rủi ro khi vá: từ chối nhầm `conclusion: null` khi đang chạy hoặc `digest: null` được K1 cho phép; cần giữ đúng nullable, không áp regex SHA thay cho kiểm kiểu ở T1. Slug cuối là lớp kiểm REST mới; nhãn B1 ở bản ghi tạm ban đầu đã được thu hẹp lại theo nguyên nhân thật, không coi lỗi byte T2/T5 cũ là tái phát.
- **F02** đã tìm trên đánh giá, W0, các bước ghi/đọc lại, D14 và adapter chung J/R/S. Hai khoảng hở thời gian nội bộ được tái hiện bằng đồng hồ tiêm; lỗ hạn vòng đọc nằm ở một hàm chung nên mọi phương thức/lớp chịu tác động. Các đường `_buoc_ghi` W2/W3/W5/W6/W7/W8 kiểm sau đọc+JSON; ca POST hoàn tất đúng biên trả 3 và giữ pending (đạt), các ca W8 cũng đạt. D14 có chốt sau phân trang nhưng trước `_khop`; đó là cùng ranh giới cần rà khi sửa, chưa tuyên bố một false-green riêng tại D14. Ca cần thêm: hoàn tất O/S ở 599.5/600/600.5, W0 JSON+kiểm miền qua hạn, nhiều lần đọc socket đều dưới 30 s nhưng tổng vượt 30 s. Rủi ro khi vá: đếm pha đánh giá vào ngân sách ghi, đổi ngoại lệ sang sai lớp kết cục, hoặc tự retry PATCH/POST; phải giữ các luật ấy.
- **F03** có ba biểu hiện cùng lớp: đổi quan sát D134; phủ thiếu từng trường/nơi gọi D2/U6; test dừng ở transport giả nên không canh adapter và `main`. Không lỗi trong cơ chế nhận diện `TinHieuChotCa` đã đo: tự kiểm 5/5 đạt; lỗi ở điều ca đích đòi và phạm vi được chạy. `d01_02_head_sha` khai chỉ ca T1, thiếu ca T7 trong chính mục đột biến; reviewer chạy thêm `n1_lien_ket_cuoi` và giết đúng tín hiệu. Ca khoá mới phải đỏ do chính tên ca, không do ngoại lệ thư viện hay ca phụ. Rủi ro khi vá: lấy assertion về chi tiết hiện thực làm oracle, tăng mẫu số bằng đột biến tương đương, hoặc xem mọi rc khác 0 là giết. Hai ca mới minh hoạ trong [oracle_audit.py](evidence/oracle_audit.py) chỉ là bằng chứng/gợi ý ở cây nháp, chưa phải bản vá sản phẩm.

Phép đo luồng tiêm chứng minh wrapper không kiểm hạn tổng; suy luận về adapter thật dựa thêm vào tài liệu chính thức: `urllib.open(timeout=...)` đặt timeout thao tác blocking, không bảo đảm deadline tổng tải. [urllib.request](https://docs.python.org/3/library/urllib.request.html#urllib.request.OpenerDirector.open), [socket timeout](https://docs.python.org/3/library/socket.html#socket.socket.settimeout). Không trình bày phép đo này như benchmark HTTP thật.

## Đo lại lời khai executor

Tất cả phép chạy Python dưới đây có `PYTHONDONTWRITEBYTECODE=1` và `-B`; cwd là bản sao H hoặc B, không phải `src/`. Log và JSON metadata giữ lệnh, rc, thời gian thật. Hai registry chạy đồng thời nên thời gian không phải benchmark so sánh H/B.

| Lời khai / lệnh đã chạy | rc | Dòng dương / số đo | Kết luận |
|---|---:|---|---|
| H: `python3 -B ops/canh_tuoi_audit_test.py` | 0 | 71.739 s; `CA: 320/320 dat`; `DOT BIEN: 207/207 bi giet dung ly do`; `TU KIEM PHAN HANG: DAT (5 dot bien)`; `TONG: DAT` | Khớp output khai; **không** xác nhận đủ quan sát đặc tả, xem F03 |
| H: cùng lệnh thêm `--chi-tiet` | 0 | 86.202 s; cùng tổng kết; có cặp gốc/đột biến của cả 207 mục | Đã chạy, không nhận lời handoff |
| H: `python3 -B .claude/dev/ci_dang_ky_test.py` | 0 | 461.727 s; `ĐĂNG KÝ: 33/33`; `PHẢN CHỨNG: 1677/1677 đỏ đúng`; `TỔNG: ĐẠT` | Đạt chế độ mặc định |
| B: cùng lệnh registry | 0 | 469.933 s; `ĐĂNG KÝ: 32/32`; `PHẢN CHỨNG: 1677/1677 đỏ đúng`; `TỔNG: ĐẠT` | Baseline đạt; tăng đúng một đăng ký |
| H: `actionlint -shellcheck /usr/bin/shellcheck .github/workflows/canh-tuoi-audit.yml` | 0 | actionlint 1.7.7, shellcheck 0.9.0; 0 chẩn đoán (stdout/stderr rỗng) | Workflow mới, B không có tệp; delta 0 |
| H: `python3 -m ruff check --no-cache --select F .claude/dev/ci_dang_ky_test.py ops/canh_tuoi_audit.py ops/canh_tuoi_audit_test.py` | 0 | Ruff 0.15.15; `All checks passed!` | 0 finding |
| B: cùng Ruff F trên `.claude/dev/ci_dang_ky_test.py` | 0 | `All checks passed!` | delta H−B = 0 |
| H: `python3 -B .claude/dev/packet_loop.py doctrine-scan --root .` | 0 | `sạch — đã quét 12 tệp, 0 chỗ` | Đạt |
| H: `python3 -B .claude/dev/packet_loop.py adr-song --root .` | 0 | `adr-song: sạch — 66 ADR trên đĩa, 66 dòng trong §20, khớp 1–1` (còn chú thích ngoại lệ trạng thái ADR 0016 trong log) | Đạt |
| H: `git diff --check B HEAD` (B đầy đủ trong metadata) | 0 | 0 lỗi khoảng trắng | Đạt |
| `python3 -B out/evidence/write_set.py` | 0 | `WRITE_SET: 4/4; REGISTRY: exactly one literal MOI item, 0 removed`; `CI_MARKERS: 0 in 4 full files and 5 commit messages` | Đúng write set; regex MOI nhận đúng output không cờ đã đo |

Các dòng không phải output nguyên văn (số chẩn đoán bằng 0) đã ghi rõ là số đếm, không tạo một dòng “PASS” giả cho công cụ im lặng. Bằng chứng: [suite thường](evidence/suite-H-plain.log), [suite chi tiết](evidence/suite-H.log), [registry H](evidence/registry-H.log), [registry B](evidence/registry-B.log), [gates.py](evidence/gates.py), [write-set.log](evidence/write-set.log). JSON cùng tên log giữ rc và argv.

`HOP_DONG_B1A: hinh 120/120 · ngu nghia 118/118 · ghim 2/2 · khoi_ma khong_co_trong_cay` được in thật trên H. B không có bộ test mới; “tại B” ở lựa chọn 8 là thiếu tệp SPEC trong cây nền B được H kế thừa. Bốn hàm của H đã được reviewer so byte trực tiếp với object ghim, không dựa vào nhánh bỏ qua của bộ test.

## Đột biến bản vá độc lập của reviewer

31 bản sửa được dựng **ngoài `src/`**, neo phải xuất hiện đúng một lần, mỗi bản một tên tệp, nạp không bytecode. 41 cặp gốc/đột biến trên ca đích: **41 gốc rc 0; 29 ca mutant GIẾT đúng (rc 3 + `DO:<chính ca>:`); 12 ca SỐNG rc 0; 0 ca TÍN DỤNG GIẢ do lỗi/ngoại lệ khác**. Tính theo mutant và đòi mọi ca đích: **24/31 giết đủ; R26 giết 1/2; 6/31 sống toàn bộ 320 ca**. Không đổi ca đích R26 sau khi thấy kết quả để nâng số đếm.

Lệnh đã chạy: `python3 -B out/evidence/reviewer_mutations.py` rc 0 (`TARGET_MUTATIONS_COMPLETE`); `python3 -B out/evidence/i2_mutations.py` rc 0 (`I2_MUTATIONS_COMPLETE`). Các script chứa nguyên văn neo/thay. Mỗi JSON dưới đây chứa lệnh-ca, rc gốc, rc mutant và toàn bộ tín hiệu; runner con là `python3 -B <test> --mot-ca <ca> <H-copy> <mutant>`. “GIẾT” trong bảng luôn có tín hiệu đúng tên ca; không dùng test khác đỏ thay thế.

| ID | Gỡ/nới chốt | Ca đích đã chạy | Kết quả |
|---|---|---|---|
| [R01](evidence/R01_fresh_becomes_unknown.json) | S5: fresh thành unknown | `n0_nen_fresh` | GIẾT; mọi ca rc 0→3 |
| [R02](evidence/R02_unknown_becomes_fresh.json) | Bỏ S6 (unknown rơi sang due) | `n4_gop_kdd_thang_chay` | GIẾT; mọi ca rc 0→3 |
| [R03](evidence/R03_due_becomes_stale.json) | S9: due thành stale | `n4_s9_p_dat` | GIẾT; mọi ca rc 0→3 |
| [R04](evidence/R04_stale_becomes_fresh.json) | Bỏ S2 (stale rơi sang due) | `n4_gop_do_thang_kdd` | GIẾT; mọi ca rc 0→3 |
| [R05](evidence/R05_old_obligation.json) | Bỏ S3 nghĩa vụ cũ | `n4_s3_p_vang` | GIẾT; mọi ca rc 0→3 |
| [R06](evidence/R06_link_T1.json) | Bỏ LIÊN KẾT T1 | `n1_lien_ket_created_at` | GIẾT; mọi ca rc 0→3 |
| [R07](evidence/R07_link_T7.json) | Bỏ LIÊN KẾT T7 | `n1_lien_ket_cuoi` | GIẾT; mọi ca rc 0→3 |
| [R08](evidence/R08_final_deadline.json) | Bỏ kiểm hạn hoàn tất đánh giá | `n15_phan_tich_qua_han` | GIẾT; mọi ca rc 0→3 |
| [R09](evidence/R09_all_or_nothing.json) | Bỏ cạn tất-cả-hoặc-không | `n15_can_ngan_sach` | GIẾT; mọi ca rc 0→3 |
| [R10](evidence/R10_post_retry.json) | Cho POST retry | `n8_post_khong_thu_lai` | GIẾT; mọi ca rc 0→3 |
| [R11](evidence/R11_patch_retry.json) | Cho PATCH retry | `n8_patch_khong_thu_lai` | GIẾT; mọi ca rc 0→3 |
| [R12](evidence/R12_pending_deleted.json) | Xoá pending khi luật không đòi tin mới | `n8_giao_lai_gian_doan`; `n8_cho_bao_khong_bi_bo` | GIẾT; mọi ca rc 0→3 |
| [R13](evidence/R13_pending_replaced.json) | Thay pending bằng sự kiện mới | `n8_cho_bao_khong_bi_thay` | GIẾT; mọi ca rc 0→3 |
| [R14](evidence/R14_reconciliation_bot.json) | Bỏ danh tính bot ở đối soát | `n8_gia_danh` | GIẾT; mọi ca rc 0→3 |
| [R15](evidence/R15_reconciliation_since.json) | Bỏ since neo vào sự kiện | `n8_doi_soat_cua_so` | GIẾT; mọi ca rc 0→3 |
| [R16](evidence/R16_shared_heartbeat.json) | Bỏ kiểm miền trước cả hai PATCH | `n8_tu_kiem_truoc_patch`; `n8_tu_kiem_truoc_patch2` | GIẾT; mọi ca rc 0→3 |
| [R17](evidence/R17_zip_expansion.json) | Bỏ trần giải nén mỗi gói T2/T5 | `n2_giai_nen_t2_tren`; `n2_giai_nen_t5_tren` | GIẾT; mọi ca rc 0→3 |
| [R18](evidence/R18_zip_entries.json) | Bỏ trần mục ZIP T2/T5 | `n2_muc_t2_tren`; `n2_muc_t5_tren` | GIẾT; mọi ca rc 0→3 |
| [R19](evidence/R19_zip_total.json) | Bỏ trần giải nén cộng dồn | `n2_tong_vuot` | GIẾT; mọi ca rc 0→3 |
| [R20](evidence/R20_workflow_step.json) | Bỏ kiểm khoá bước 4 workflow | `n10_buoc4_if` | GIẾT; mọi ca rc 0→3 |
| [R21](evidence/R21_workflow_permission.json) | Bỏ kiểm permissions workflow | `n10_quyen` | GIẾT; mọi ca rc 0→3 |
| [R22](evidence/R22_chunk_read_removed.json) | Đọc toàn luồng bằng read() không n | `n1_j_vuot_tran`; `n1_s_vuot_tran` | SỐNG; mọi ca rc 0→0; cả 320/320 đạt |
| [R23](evidence/R23_real_redirect_guard.json) | Adapter tự theo redirect | `n1_s_khong_auth`; `n1_r_qua_3` | SỐNG; mọi ca rc 0→0; cả 320/320 đạt |
| [R24](evidence/R24_main_exit_zero.json) | main luôn trả 0 | `n9_ma_thoat` | SỐNG; mọi ca rc 0→0; cả 320/320 đạt |
| [R25](evidence/R25_real_timeout_ignored.json) | Adapter urllib nhận timeout=None | `n1_han_goi`; `n15_kep_timeout` | SỐNG; mọi ca rc 0→0; cả 320/320 đạt |
| [R26](evidence/R26_api_auth_removed.json) | Bỏ Authorization API | `n0_nen_fresh`; `n1_s_khong_auth` | 1/2 GIẾT: n0 sống; n1_s_khong_auth rc 3 |
| [R27](evidence/R27_last_link_event.json) | T7 bỏ riêng event | `n1_lien_ket_event`; `n1_lien_ket_cuoi` | SỐNG; mọi ca rc 0→0; cả 320/320 đạt |
| [R28](evidence/R28_U6_attempt_removed.json) | U6 bỏ riêng run_attempt | `n1_u6`; `n1_chua_xong` | SỐNG; mọi ca rc 0→0; cả 320/320 đạt |
| [R29](evidence/R29_heartbeat_reader_bypass.json) | Người đọc bỏ bộ kiểm miền chung | `n8_mien_m4` | GIẾT; mọi ca rc 0→3 |
| [R30](evidence/R30_I2_unknown_promoted_dat.json) | I2: gộp khong_do_duoc thành dat | `n4_s6` | GIẾT; mọi ca rc 0→3 |
| [R31](evidence/R31_I2_fresh_with_old_obligation.json) | I2: xoá toàn O dù còn khung cũ | `n4_s3_p_vang` | GIẾT; mọi ca rc 0→3 |

R02/R04 giữ tên tệp nháp ban đầu có chữ “fresh”, nhưng neo/thay thực tế là **bỏ S6/S2**, và output đo được chuyển sang `due_in_progress`; bảng trên ghi hành vi thật. R30/R31 mới là hai phép nâng sai sang `fresh`, đều bị giết đúng.

Quét rộng 6 mutant sống: `python3 -B out/evidence/run_survivors.py`, runner rc 0; mỗi tiến trình `mutant_all_cases.py <mutant>` rc 0 và `cases: 320, passed: 320, failed: []`. Không gọi lại vòng sinh 207 mutant bên trong bản đã sửa vì mục tiêu ở đây là đo 320 ca gốc trên từng mutant. [Tổng hợp](evidence/survivor-results.json).

**Không tương đương:** R27 và R28 được hai ca dữ liệu thường mới phân biệt (D2 cuối chỉ đổi event hoặc attempt): gốc rc 0, mutant rc 3, đúng `TinHieuChotCa` của `review_T7_event` / `review_U6_attempt`; S mutant thành `fresh`. R22 đổi cách cấp phát/đọc trước kiểm trần; R23 bỏ chốt không tự chuyển hướng; R24 bỏ mã thoát; R25 bỏ timeout thật. Chúng thay chốt được đặc tả đặt ra, dù đồ giả hiện tại không chạy/không quan sát tầng ấy.

**GIẾT SAI LÝ DO so với quan sát đóng băng:** D134 của executor. Đây không phải lỗi nhận diện ngoại lệ ở runner: ca thực sự ném `TinHieuChotCa` đúng tên. Nhưng đại lượng D5 đã khai không đổi (0→0), còn ca được báo giết bằng trạng thái sau KeyError. Vì vậy không công nhận “207/207 đúng quan sát đặc tả”; không tự suy ra 206/207 là tổng đã audit hết từng quan sát. Những dòng khác có tổng kết chạy thật và những điểm nghi vấn đã kiểm riêng; reviewer không chứng nhận thay bảng đầy đủ bằng một phép trừ số học.

## Đối chiếu lớp của review đặc tả vào mã nguồn

Nguồn đã đọc từ `origin/ops/wp1494-r1:ops/specs/wp1494-r1/reviews/` và bảng **Thay đổi** của SPEC: [lượt 1](evidence/spec-review-1.json) trên `1a758cbea0ec9fe9f8b9387f990ec8e0adb83fba`, [lượt 2](evidence/spec-review-2.json) trên `1c692ccba157fe99c133074570197cadd3db0ef3`, [lượt 3](evidence/spec-review-3.json) trên `c22631484758ae12720d096c85aa727815a82d84`. Cache còn có [tệp lượt 4](evidence/spec-review-4.json), verdict blocked vì bootstrap refs, 0 finding, và [tệp lượt 5](evidence/spec-review-5.json), approve; cả hai trên đặc tả r4 `8c68b39153a62ff26a982dc72add5f079277e051`. Đây đều là review **đặc tả**, không phải bằng chứng chạy mã H. Không suy số lượt nguồn từ số tệp review lịch sử.

Mỗi lớp chỉ có **một** nhãn ở cột kết luận. “ĐÃ SỬA ĐÚNG LỚP” nói về cơ chế mã hiện tại ở phạm vi lớp ấy, không miễn lỗ kiểm thử thuộc F03, không bảo đảm vận hành GitHub thật.

| Lớp kế thừa | Nhãn trên mã H | Cơ chế và bằng chứng đo |
|---|---|---|
| `b1-consumer-contract-mismatch` | **ĐÃ SỬA ĐÚNG LỚP** | Bảng byte hỏng/không hoàn tất đi đúng nơi dùng T2/T5/YAML; các ca `n2_t2_*`, `n2_t5_*`, `n6_x2_name` đã chạy; fixture 120/120 + ngữ nghĩa 118/118; bốn hàm bằng byte ghim. F01 là kiểm miền REST, không tái đặt lỗi chính sách ngoại lệ byte cũ dưới cùng tên. |
| `notification-dedup-before-delivery` | **ĐÃ SỬA ĐÚNG LỚP** | Pending là dữ liệu bền trước POST, `da_bao` tiến sau xác nhận, D14 neo vào khung sự kiện. R12–R15 bị giết; các ca `n8_giao_lai_*`, đổi Issue hai chiều, cửa sổ 1000/1001 và hồi phục đã chạy. Bảo đảm chỉ trong phạm vi Issue/nhịp tim còn đọc được như đặc tả. |
| `write-retries-violate-delivery-contract` | **ĐÃ SỬA ĐÚNG LỚP** | `_goi` chỉ retry GET; R10/R11 giết đúng bằng số lần gửi vật lý. POST hoàn tất đúng hạn: 1 POST, rc 3, pending còn; không gửi lại trong lượt. |
| `mutant-oracles-non-discriminating` | **VÁ HỜ** | Runner có tín hiệu riêng và tự kiểm 5/5, nhưng D134 đổi quan sát, sáu mutant sống toàn 320 ca, thiếu ca ở nơi gọi dùng chung. F03. |
| `bounded-evaluation-order-dependent` | **VÁ HỜ** | Xếp E/ID_TẢI và tất-cả-hoặc-không đã đúng ở ca đã có (`n15_thu_tu_goi`, R08/R09). Nhưng ranh giới hoàn tất vẫn thiếu phần cuối tính S/W0 và hạn luồng thật: F02, clock 601 vẫn fresh; W0 181 s vẫn xanh. |
| `consumer-freshness-anchor-unverified` | **ĐÃ SỬA ĐÚNG LỚP** | T1/T7 cùng so chín trường; neo unknown thắng T2/T3/T6 âm. R06/R07 giết đúng; shared head_sha thử thêm tại T7 cũng giết. Gốc vượt qua hai ca mới event/U6; lỗ chống hồi quy R27/R28 thuộc F03, chưa phải lỗi neo của mã gốc. |
| `freshness-forgets-overdue-obligations` | **ĐÃ SỬA ĐÚNG LỚP** | O, tiền tố `dong_den`, khung đóng tay được giải trước E. R05/R31 giết; `n4_r_khung_cu`, `n4_dong_den_tien_to`, `n4_dong_tay*` đạt; chưa thấy phép đóng tay nào tạo SHA audit. |
| `heartbeat-value-domain-incomplete` | **ĐÃ SỬA ĐÚNG LỚP** | Chung `kiem_nhip_tim` ở đọc và trước cả hai PATCH; 32 điều kiện/23 điểm mã dùng chung đã đo; R16/R29 giết; khứ hồi người ghi→người đọc sau ca, `n8_ma_dau_unicode`, `n8_truoc_khung_dau`, context biên đạt. |
| `workflow-step-controls-unconstrained` | **ĐÃ SỬA ĐÚNG LỚP** | Tập khoá và giá trị đóng tới từng bước; ca thêm if/name/shell/quyền/bước đều đã chạy, R20/R21 giết; actionlint thật rc 0. Khoá YAML trùng cùng giá trị là giới hạn parser đã đóng băng, actionlint độc lập từ chối. |
| `unbounded-artifact-expansion` | **ĐÃ SỬA ĐÚNG LỚP** | `_tho_zip` kiểm số mục rồi đọc từng ZipInfo, đếm byte thực mỗi gói/toàn pha; R17–R19 giết trên cả T2/T5. Ca dưới/bằng/trên đạt. Lỗ ca canh cách đọc HTTP R22 thuộc F03; hạn thời gian đọc thuộc F02. |
| `markdown-state-table-column-drift` | **KHÔNG ÁP DỤNG** | Lớp lỗi bảng Markdown của đặc tả; write set mã H không sửa SPEC hay bảng trạng thái Markdown. S1–S9 ở mã đã được bộ ca trạng thái chạy. |
| `merged-misreported-as-landed` | **KHÔNG ÁP DỤNG** | Lớp lỗi phát biểu trạng thái điều phối trong văn bản đặc tả, không có lời khẳng định land mới trong bốn tệp. Review này chỉ chứng nhận mã/đo tại H, không chứng nhận land hay Mission complete. |

Tổng: 8 lớp ĐÃ SỬA ĐÚNG LỚP, 2 VÁ HỜ, 2 KHÔNG ÁP DỤNG; không có lớp xếp CHƯA SỬA. Lịch sử F03/SPEC-04 xuyên nhiều lượt đặc tả vẫn được giữ: cần điều phối xử lý thiết kế oracle/quan sát theo §12 trước chu kỳ vá tiếp, không chỉ tăng số mutant hoặc đổi tên lớp. Reviewer không tự mở generation, không cấp thêm ngân sách, không sửa đặc tả.

## Các hướng đầu vào thù địch — mô tả, đường xử lý và độ phủ

Chỉ mô tả hướng tác động; reviewer không tạo nội dung nhằm thoát cây, khai thác hay thực thi lệnh. Probe mới chỉ dùng JSON REST giả, luồng byte thường, đồng hồ giả và YAML lặp lại cùng một giá trị lệnh đã có. Các ca có sẵn được chạy nguyên trạng trong bản sao. ZIP được đọc trong bộ nhớ theo `ZipInfo`, không `extract` ra filesystem.

| Hướng | Đường xử lý | Ca đã commit / phép đo và kết luận |
|---|---|---|
| Phân trang lặp, mất phần tử, `total_count` sai | `_liet_ke`: giới hạn 10 trang, đòi trang cuối không còn next, số đếm bằng total cuối, id dương/duy nhất | `n1_hai_trang`, `n1_total_count`, `n1_trung_id`, `n1_id_bool`, `n4_s1_khong_tron`; D14 `n8_doi_soat_khong_tron`. Đã chạy; không dùng phần thấy được để xanh. Lặp Link vô tận sẽ hết trần; không có ca riêng cho chính URL lặp. |
| Đổi thứ tự trang/lượt/job/artifact | Xếp E và ID_TẢI theo id; jobs theo U7; chọn SHA id nhỏ nhất | `n15_thu_tu_goi`, `n4_u7_jobs`, `n4_sha_audit_hai_trang` đạt. R09 giết tại cạn ngân sách ở cả thứ tự API. |
| `created_at` sai dạng hoặc ngày không tồn tại | `gio` regex rồi `doc_moc`; HINH_D1 trước gán khung | Ca commit `n1_d1_hinh_created_at` kiểm sai dạng. Reviewer thêm ngày lịch không tồn tại, sai dạng và null: cả ba S `khong_do_duoc/khoa_chon_khong_doc_duoc`, exit 1; `ordinary_inputs.py` rc 0. Không gọi ca format là đã phủ riêng lịch không tồn tại. |
| Rerun attempt làm cũ thành mới; dispatch lẫn vào | Khung từ created_at đã liên kết; artifact theo attempt hiện tại; HINH_D1 event schedule | `n5_chay_lai_khong_lam_tuoi`, `n5_attempt_thap`, `n5_dispatch` đạt. Attempt ngoài miền là lỗ F01. |
| `head_sha` đổi giữa hai lần D2; trường khác đổi ở cuối | `_t1`, `_t7`, `_lech_lien_ket`; U6 riêng bốn trường | `n1_lien_ket_cuoi`, `n1_u6`, các ca neo ưu tiên đạt; R07 giết. Riêng event cuối / U6 attempt thiếu ca commit phân biệt, R27/R28 sống; hai ca reviewer mới giết đúng (F03). |
| Comment giả dòng sự kiện từ người không phải bot | `_khop` đòi đúng login, đúng một dòng marker và JSON bằng sự kiện chờ; W6 kiểm lại login | `n8_gia_danh`, `n8_gia_danh_doi_chung`, `n8_hai_dong_su_kien`, `n8_doc_lai_comment_login`; R14 giết. Chưa đo khả năng tài khoản/bot GitHub bị chiếm quyền. |
| Thân Issue bị sửa tay; heartbeat cũ/hỏng/vắng | `doc_nhip_tim`, miền m1–m33, giữ dữ liệu đọc được dù cũ; W3/W8 so nguyên thân và open | `n8_doc_lai_than`, `n8_state`, `n8_json_hong`, `n8_hai_dong`, `n8_thieu_khoa`, `n8_nhip_tim_cu`, `n8_bien_24h`, đổi Issue và lượt đầu đạt. Người có quyền sửa được một heartbeat **hợp lệ** vẫn là ranh giới tin cậy đã khai, không có chữ ký. Issue REST thiếu body là F01. |
| Thiếu `X-GitHub-Request-Id` | `_j` không nhận JSON 2xx thiếu dấu; `_tai` đòi dấu ở hop API 302 | `n1_j_khong_dau`, `n1_j_403_co_dau`, `n1_j_403_khong_dau` đạt. Chốt R thiếu dấu đọc thấy trong mã nhưng không có ca commit riêng cho 302 thiếu dấu; không gán độ phủ J cho R. |
| Redirect xuống HTTP hoặc sang host khác | `_KhongChuyenHuong` chặn tự theo; `_tai` chỉ nhận Location HTTPS; `_goi` chỉ gắn Authorization khi hostname đúng api.github.com | `n1_r_khong_https`, `n1_r_qua_3`, `n1_r_dung_3`, `n1_s_khong_auth` đạt ở transport giả. Host lưu trữ HTTPS khác được phép theo đặc tả và không mang token. Adapter offline đã được reviewer gọi; đường redirect thật chưa đo (socket bị sandbox chặn). R23 sống qua suite. Link phân trang được `_liet_ke` nhận nguyên URL, không có allowlist origin ở đó; không dựng payload hay tuyên bố đã kiểm an toàn mọi URL. |
| Content-Length sai; thân quá trần | `_mot_lan` đọc tối đa TRAN_GOI+1 rồi từ chối; `_tai` so byte đã đọc với Content-Length | `n1_s_ngan`, `n1_s_vuot_tran`, `n1_j_vuot_tran` đạt. R22 cho thấy ca không canh cách đọc trước cấp phát; F02 cho thấy không canh tổng thời gian đọc. |
| ZIP nhiều mục/tổng giải nén lớn | `_tho_zip` đếm mọi mục, chỉ đọc tệp, đếm byte thực theo khúc ≤1 MiB; trần mỗi gói/toàn pha | `n2_muc_*`, `n2_giai_nen_*`, `n2_tong_vuot`, hai tệp cùng tên/thư mục thường đạt; R17–R19 giết. Không tạo đường dẫn thoát cây hoặc gói nhằm khai thác. Trần thật 64/256 MiB chưa benchmark với artifact live. |
| Đồng hồ đúng hạn, POST xong sau hạn | `_goi` trước gửi/chờ; `_buoc_ghi` sau nhận; chốt đánh giá tại dòng 678 | `n15_han_cuoi_danh_gia`, `n15_han_cuoi_ghi`, `n15_cho_qua_han`, `n15_khong_goi_sau_han` đạt. Reviewer đo POST lưu thành công nhưng đọc xong đúng 180: rc 3, 1 POST, còn pending, chưa ack. Lỗ CPU cuối/W0/luồng: F02. |
| Workflow thêm khoá, bước, quyền | `kiem_hinh` dùng safe_load và tập khoá đóng; actionlint+shellcheck bổ sung | Toàn nhóm `n10_*` đã chạy, R20/R21 giết. YAML hai run cùng giá trị: cấu trúc bằng gốc và `kiem_hinh=[]`, actionlint rc 1; giới hạn parser đã đo, không coi actionlint thất bại ấy là lỗi của tệp H. |

## Phán từng lựa chọn 1–9 của executor

| # | Phán | Căn cứ |
|---|---|---|
| 1 — D134 dùng KeyError thay quan sát D5 | **Không chấp nhận tín dụng nghiệm thu; F03.** Nhận định đầu vào trong câu đặc tả không dựng được là đúng. | Schema ghim không cho `ok:false` kèm job/manh. Probe cả false đúng hình và false có các trường ấy: D5 ngoài gói biên nhận luôn 0 ở cả gốc/mutant. Bỏ guard làm bản đúng hình ném KeyError; lưới đổi S1 rồi ca đỏ. Nghiệm thu 11 cấm tự đổi quan sát cho khớp. Không thể gọi toàn mutant tương đương vì S đã đổi; phải đưa mâu thuẫn quan sát lên điều phối. |
| 2 — D61 có 23 mutant cho 32 điều kiện | **Chấp nhận việc gộp theo chốt dùng chung, không chấp nhận bỏ điều kiện.** Số đo ở H đủ 32. | `oracle_audit.py`: `D61_MUTANTS 23 UNIQUE_CONDITIONS 32 ALL_TARGETS 32`, gồm m1,m2,m4…m33; m3 có D62 riêng. m12/m14, m17/m26 và bảy cặp miền sự kiện dùng cùng điểm mã; mỗi mutant gộp chạy cả hai ca và đều giết trong suite chi tiết. Diễn giải ×32 là 32 nghĩa vụ phân biệt, cùng luật nơi gọi cho phép chung điểm mã; không cần nhân bản mã chỉ để đủ 32 tệp mutant. |
| 3 — Gộp đột biến hàm chung | **Đúng một phần; bằng chứng LIÊN KẾT chưa đủ nơi gọi trong mục mutant.** | D07_69 chạy D1+D14; D96 W2+W7; D107 J+S; D108/D109 T2+T5, đều đúng và đã chạy. RIÊNG `d01_02_head_sha` chỉ khai T1; reviewer chạy thêm T7 `n1_lien_ket_cuoi` và giết đúng. Gộp chốt hợp lệ, nhưng không lấy ca của caller này thay cho caller kia. R27/R28 cho thấy phạm vi regression còn hở. |
| 4 — Hai mutant thêm D82; YAML khoá trùng | **Hai mutant thêm hợp lệ; không coi việc chưa thêm duplicate-key parser là vi phạm đặc tả đóng băng.** | `d82_01b_gia_tri_name`, `d82_01c_hai_khoa_on` đều giết. H kiểm cả True và chuỗi on sau quy đổi. Hai khoá run cùng giá trị bị safe_load gộp: `kiem_hinh=[]`, cấu trúc bằng H; actionlint 1.7.7 từ chối rc 1. Giới hạn thực của safe_load đã đo; không khẳng định bộ kiểm hình tự phát hiện mọi lỗi YAML nguồn. |
| 5 — TimeoutError → transport_nem; het_gio chỉ pha | **Chấp nhận cách phân lớp ngoại lệ; không miễn F02.** | `_goi` bắt mọi Exception rồi mã hoá module.qualname, không chọn chính sách theo `isinstance(TimeoutError)`; phù hợp bảng nguyên hàm. Hết hạn pha do đồng hồ là `het_gio`. Ca `n1_j_het_gio`, biên transport, retry và timeout truyền đã chạy. Thiếu cưỡng chế hạn tổng luồng thật là vấn đề khác. |
| 6 — Chỉ ghi thong_bao_hoan khi sự kiện khác | **Chấp nhận.** | Mục 6 định nghĩa sự kiện “luật đòi nhưng lượt này không cấp vì đang có sự kiện chờ”. Cùng loại/cùng bộ chính là sự kiện đang được giao; không có tin khác bị hoãn. `chay` phần cấp sự kiện so `(loại, bộ)`; `n8_giao_lai_*` đòi hoan null khi gửi lại cùng sự kiện, các ca pending không bị thay kiểm trường hợp khác. |
| 7 — D2 đầu hỏng thì T7 khong_danh_gia | **Chấp nhận khi chưa có bản đầu để làm U6; không được gán T7 dat.** | Probe `D2-start-fails`: T1 `khong_do_duoc/http_github:403`; T7 `khong_danh_gia`; tổng `khong_do_duoc/khung_khong_do_duoc`, rc 1. Đây là phép không đủ đầu vào; không bỏ qua một bất nhất rồi nâng xanh. |
| 8 — Nghiệm thu 3 ghim 2/2 khi thiếu SPEC B1a | **Chấp nhận đúng ngoại lệ đã viết ở nghiệm thu 3.** | Test H in thật `khoi_ma khong_co_trong_cay`; schema+fixture vẫn bắt buộc và được băm. Reviewer đã trích đúng khối từ object `d1b08c…`, băm `d9c78e70…` và so 4/4 hàm bằng byte ở H. Nhánh test này không tự khoá sự nguyên văn trong tương lai; đó là giới hạn được đặc tả cho phép, không đủ lý do mở finding mới trên H. |
| 9 — Không ca commit chạy transport_that/main | **Lỗ kiểm thử thực, F03; adapter thời gian còn lỗi F02.** | R23/R24/R25 sống 320/320 chứng minh các ca transport/exit hiện tại dừng trước lớp thật. Reviewer gọi adapter bằng opener giả để kiểm Request GET/PATCH/POST, dummy Authorization, JSON body, timeout 2.5, và handler không redirect; gọi main với chay thật + transport stateful giả: exits 0/0/1/1/3/2, stdout một JSON ASCII, summary có khi có S, không in dummy token. Đây là phép đo offline bổ sung, chưa thành ca commit và không thay phép đo wire thật. |

## BẢNG SĂN chủ động

Các hướng dưới đây được chọn để có thể bác bỏ lời khai, không chỉ lặp ca happy path. Các lệnh script đều có rc 0 khi đo xong trừ phép socket ghi rõ; kết quả ca con/đầu ra sản phẩm nằm trong log.

| Hướng | Giả thuyết | Phép đo đã chạy | Kết quả |
|---|---|---|---|
| 1. Sai nền hoặc ghim | H/B/contract hoặc mốc khởi đầu không đúng sẽ làm nghiệm thu vô nghĩa | `baseline.py`; rev-parse, first-parent, sha256; so AST giữ byte bốn hàm | Không tìm thấy lệch; BASELINE DAT, 4/4 hàm bằng byte |
| 2. REST ngoài miền | Kiểm kiểu có thể bỏ qua giá trị âm/null/khuyết và cho false-green | `reviewer_probes.py`, `additional_probes.py`, fixture scalar/list thường | Có: F01, gồm fresh trên digest số và KeyError ở cả ba caller Issue |
| 3. Bốn trạng thái/I2 | Bỏ nhánh ưu tiên hoặc nâng unknown thành dat vẫn xanh suite | R01–R05, R30/R31 | Bị giết đúng; đặc biệt R30/R31 tạo fresh trái nghĩa vụ và ca đích đỏ |
| 4. Anchor và U6 theo caller/field | Ca đầu D2 có thể không canh D2 cuối; chỉ updated_at không canh attempt | R06/R07/R27/R28, quét toàn 320, hai ca mới trong `oracle_audit.py` | R06/R07 giết; R27/R28 sống 320/320, ca mới giết đúng; F03 |
| 5. Hạn sau công việc cuối | Chốt trước I/O hoặc trước tính S có thể xanh sau hạn | R08/R09; probe CPU cuối, W0 và luồng đọc; POST kết thúc đúng 180 | F02 tái hiện ba điểm; POST không ack quá hạn là đối chứng đúng |
| 6. Pending bị xoá/thay và dedup sớm | Lượt kế tiếp bỏ tin chưa giao hoặc phát trùng | R10–R15; các trace multi-run `n8_*` trong suite | Các mutant bị giết; không thấy lỗi cơ chế pending trong các trace đã đo |
| 7. Người ghi/người đọc lệch miền | Một caller không gọi bộ kiểm chung sẽ nhận/ghi heartbeat sai | R16/R29; D61 23 điểm/32 điều kiện; `n8_tu_kiem_truoc_patch2` | Giết đúng cả hai writer và reader; số miền đủ |
| 8. Resource cap chỉ sau cấp phát | Ca quá trần có thể kiểm kết quả mà không kiểm cách đọc | R17–R19 và R22; quét 320 trên R22 | Trần ZIP bị gỡ thì đỏ; bỏ đọc HTTP theo khúc vẫn 320/320, F03 |
| 9. Adapter thật bị bỏ trống | Đồ giả che redirect/timeout/exit-code thật | R23–R25, cả 320; offline adapter/main; thử HTTP loopback | Ba mutant sống; adapter/main gốc offline cho kết quả đúng; socket Python bị PermissionError rc 1, không có kết luận wire |
| 10. Oracle lấy tín dụng sai | D134 chết bởi lỗi an toàn khác thay vì quan sát cam kết | Probe hai dạng false ở gốc/mutant, log số D5 | 0→0; giết sai quan sát đóng băng, F03 |
| 11. Workflow ngoài ngữ pháp | Thêm khoá/bước/quyền hoặc dùng khoá trùng qua parser | Suite n10; R20/R21; YAML duplicate benign + actionlint | Ca thêm cấu trúc bị chặn; khoá trùng chỉ actionlint bắt (rc 1), phù hợp giới hạn đã khai |
| 12. Scope và dấu bỏ CI | Tệp thứ năm/registry sửa khác/commit ẩn dấu bỏ CI | `write_set.py`, numstat, diff-check | Đúng bốn tệp +2873/−0; một MOI đúng nguyên văn; 0 dấu trong 4 tệp/5 message |

## KHÔNG ĐO ĐƯỢC / chưa chạy

- **Model/effort phục vụ thật và receipt identity:** không có telemetry độc lập; không suy từ prompt, binary hiện diện hoặc tài khoản GitHub. Review có shell đã chạy như log; không tự phát hành receipt/assurance hay đăng GitHub.
- **HTTP thật/redirect trên wire:** phép HTTP loopback thông thường bị sandbox từ chối ngay khi tạo socket, `PermissionError: [Errno 1] Operation not permitted`; Python rc 1, [transport-probe.log](evidence/transport-probe.log). Vỏ shell cat log sau đó có rc 0 không được tính là phép HTTP đạt. Không né hạn chế; các kết quả transport đã báo là tiêm/offline. Chưa đo độ trễ thấy comment, quyền token, lịch GitHub hoặc kênh thông báo thật.
- **Môi trường đích:** đã chạy Python 3.13.18/Linux, PyYAML 6.0.3, jsonschema 4.26.0; workflow ghim Python 3.12 chưa được chạy trên runner ấy. Không chạy Windows. Spec yêu cầu Windows hoặc miễn trừ neo exact H; chưa có bằng chứng được đo ở lượt này về một trong hai. Đây là điều kiện riêng chưa được chứng nhận, không tự miễn từ việc local xanh.
- **Nghiệm thu sau tích hợp:** không CI PR/connector/M9 thật, không dispatch để tạo bằng chứng nghiệm thu 13–14, không ghi Issue/comment thật, không kiểm kênh giao tin. H chưa đẩy theo prompt. Chưa xác nhận quy trình land/Mission complete.
- **Gate rộng ngoài yêu cầu:** registry chỉ chạy mặc định ở B/H, không `--chay` toàn bộ registry, không `scripts/tl.py --selftest`, không release/golden/build. Đã chạy trực tiếp suite mới và mutation đầy đủ của nó. Không nhầm registry mặc định với toàn bộ suite đã đăng ký.
- **Tính mới của refs:** first-parent và nguồn lease/review dựa trên clone đầy đủ refs được cấp. Không fetch vào cây chỉ đọc, không tự xác nhận trạng thái tất cả ref/Issue remote mới hơn. HEAD/tree và byte tại thời điểm review được kiểm đầu/cuối.
- **Trần tải trên artifact thật:** có ca byte/ZIP nhỏ với trần tiêm và đối chứng đúng biên; chưa benchmark các mức 50/64/256 MiB với GitHub thật hoặc môi trường thiếu bộ nhớ.
- **Không chứng nhận mọi cặp trong bảng bằng suy luận số đếm:** chạy thật 207 mục, đã audit quan sát của các điểm nghi vấn và phản chứng thêm. D134 đủ bác bỏ tuyên bố “tất cả đúng quan sát”; kết quả này không khẳng định 206 mục còn lại đều đã được chứng minh độc lập về tính tương đương/độ cô lập.

## Toàn vẹn cuối lượt và cách tái hiện

`PYTHONDONTWRITEBYTECODE=1 python3 -B out/evidence/final_integrity.py` rc 0, [log](evidence/final-integrity.log):

```text
SRC_FILES 18159 -> 18159 ADDED 0 REMOVED 0 CHANGED 0
HEAD 127b82a8a9e41fda3c4a230810118f0bedfb200d
TREE 862746ce6dae133012b0cfce90bf4913c8784c41
GIT_STATUS_EMPTY True
H_TESTED_FILES_MATCH_GIT 4
READ_ONLY_INTEGRITY: DAT
```

Snapshot bao gồm cả `.git` và ignored; không chỉ dựa vào git status. Cả bản sao H/B có `core.abbrev=7`. Băm HANDOFF đo lại vẫn `c937ae597935a9db399f38f35309e98907ab3966226f69835d48b49084b39d9f`; băm SPEC đầy đủ như đầu báo cáo. [Định danh đầu vào và refs](evidence/input-identities.json), [lease](evidence/lease.yaml), [Mission r109](evidence/MCR-1172-r109.md) được giữ để đối chiếu.

Hồ sơ `out/` giữ script, log, bảng neo/thay và snapshot. [Hướng dẫn tái hiện](evidence/README.md) có lệnh dựng lại bản sao local từ object đã có; không cần sửa `src/`, fetch hay ghi GitHub. Các gợi ý vá là dữ liệu review, không phải thay đổi đã áp vào nhánh executor.

Đã dọn thư mục nháp `review-tmp/` do reviewer tạo; giữ nguyên toàn bộ `out/`. Không commit/push, không ghi GitHub, không dispatch.
