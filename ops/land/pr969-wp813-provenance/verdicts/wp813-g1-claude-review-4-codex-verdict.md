Verdict: approve
Reviewed commit: 25bd151727b5be2574594cf104658048816c4942
Spec sha256: 9df36da1ef2be23c7519934bf6aee0dfecb6d2082cb8e485c7a6819c8a6154f3; Chung sha256: 4e3d1e1b3f6a0b60b96ad7b70f0ece97eca4bb3d6d10defeab1cd24ac6d1cbf0

**Kết luận lượt 4: 0 P0/P1/P2; còn 1 lớp P3 về độ phủ đột biến.** Phản chứng giữ quyền `mo_lai_tu` cũ của lượt 3 đã bị bắt đúng tại oracle quyền, và chuỗi dùng checkpoint trên candidate chạy đúng. Đột biến bổ sung về phần tử `check_refs` sai hình dạng sống, nhưng candidate từ chối đúng; biểu hiện MỚI này xếp P3 theo luật bắt buộc trong prompt. Ngưỡng approve đã áp là không còn P0/P1/P2. Verdict chỉ neo commit dòng 2, không cấp quyền push, merge hoặc land.

| slug | hạng P0–P3 | biểu hiện file:dòng | phép đo/tái hiện đã chạy | hướng vá |
|---|---|---|---|---|
| `r813-mutation-evidence-incomplete` | **P3 — còn mở chỉ với biểu hiện mới** | `.claude/dev/packet_loop.py:2970`: so tổng số refs đúng dạng với tổng số refs khai; bộ ca từ `.claude/dev/packet_loop_test.py:8924` chưa khóa chốt này ở nhánh CI. | Mutant bỏ đúng phép so độ dài sống **105/105 ca r813+r834**. A/B: một cặp check_refs hợp lệ trộn một phần tử null ⇒ candidate rc11/nguyên byte, mutant rc0/running. Ca reviewer bổ sung giết bằng AssertionError đòi11/được0; 3 đối chứng khác họ vẫn PASS. | Owner: executor Packet #813 (Claude), chủ kho theo dõi. Thêm ca trộn ref hợp lệ và phần tử sai dạng; đòi rc11, đúng lý do, state nguyên byte; khai mutant bỏ chốt độ dài. Giữ predicate sản phẩm đang đúng. |

Tên nợ: **thiếu phản chứng bảo vệ việc không bỏ qua phần tử check_refs sai hình dạng**. Giữ slug lớp cũ để không đổi khóa lịch sử; không coi các biểu hiện P2 đã được sửa là còn sống. Lý do **P3, không P2**: phản chứng này được reviewer dựng lần đầu ở lượt 4, chưa nêu ở lượt 3; candidate xử lý đúng ở A/B; không thiếu ca bắt buộc nào trong `nghiem_thu`. Quy tắc riêng của chủ kho trong prompt được ưu tiên so với suy luận “cùng lớp độ phủ thì tự động P2”. Không phát hiện hành vi sản phẩm sai trong phạm vi đã đo.

Gợi ý bốn phần: sửa vùng test `r813_*` vì thiếu quan sát nằm ở nhánh lọc refs; dùng baseline approved_pending thật, chỉ thêm null vào danh sách có cặp workflow/job đỏ hợp lệ; khóa bằng mutant tại dòng 2970 và oracle rc/lý do/byte state. Rủi ro: ca chỉ có refs hỏng sẽ bị chốt khác bắt, tạo tín dụng sai; nới sản phẩm để sửa test sẽ cho bằng chứng hỏng lọt. Cặp tìm/thay, mã đã chạy, ca reviewer và A/B: [extra_mutation.py](extra_mutation.py), [mutation.json](extra_ref_shape/mutation.json), [ab_results.json](extra_ref_shape/ab_results.json). Đây là dữ liệu phản chứng trên bản sao, không phải patch giao áp lên source.

**Phạm vi và danh tính.** Đã đọc toàn bộ `runs/7bb77f5e/prompt.snapshot`; các đường dẫn tính từ gốc rv4 theo chỉ thị trực tiếp. Packet #813/revision 2/generation 1, review_class sensitive, assurance_target cross_approved. Reviewer Codex/OpenAI, họ openai; executor theo lease bản chép Claude, họ claude. Phiên reviewer độc lập, không kế thừa context executor. Thực thi shell qua công cụ Linux, transport machine; exact serving model/effort và attestation launcher `codex_cli` không được đo độc lập trong phiên này. Không tạo receipt assurance hoặc suy identity từ actor đăng GitHub. Trần 10 và lý do cấp lượt 4 theo assignment, không xác minh comment bằng mạng.

**ĐỐI CHIẾU LƯỢT TRƯỚC.** Nguồn: `tham-chieu/wp813-g1-codex-luot3-VERDICT.md`, head `71c19c937442ae38875717989654ee93f387d04e`. Đã review không lọc toàn bộ [FULL.diff](FULL.diff), không chỉ [FIX.diff](FIX.diff).

| lớp/biểu hiện trước | phân loại trên candidate | bằng chứng độc lập lượt 4 |
|---|---|---|
| `r813-mutation-evidence-incomplete`: giữ mo_lai_tu cũ sau CI → connector, P2 lượt 3 | **ĐÃ VÁ THẬT biểu hiện P2**; không tuyên bố toàn lớp đóng vì còn biểu hiện mới P3 | Chính mutant giữ quyền cũ làm `r813_connector_sau_ci` đỏ bằng `AssertionError: r813: nội dung quyền sai`. Oracle so đủ `(connector,1,pending_sha)`. Ca mới `r813_connector_sau_ci_roi_duyet` cũng đỏ đòi0/được8, `state hỏng (mo-lai)`. Ba đối chứng khác họ PASS. |
| `ci-reopen-run-context-unbound`, đã đóng lượt 3 | **Giữ ĐÃ VÁ THẬT** | Probe check-run đỏ sai head hoặc head rỗng: rc12/nguyên byte. Mutant bỏ so head bị `r813_ci_do_check_head_khac` bắt đòi12/được0. Check mới hơn, app sai, kho sai đều bị từ chối. |
| Hai biểu hiện độ phủ đã đóng: kiểu repository.full_name và thay checkpoint_day | **Giữ ĐÃ VÁ THẬT** | `r813_m5_bo_full_name` và `r813_quyen_day_giu_cu` bị đúng ca giết; probe kiểu run trước lọc và thay quyền checkpoint đều đạt. |

Không báo tỷ lệ đóng lớp 100%: lớp độ phủ còn nợ P3 mới, dù phản chứng P2 cụ thể của lượt 3 đã sửa thật. Không đổi slug, không reset lịch sử.

| phép đo cùng phản chứng lượt 3 | candidate | mutant giữ quyền cũ |
|---|---|---|
| mo-lai ci-do | rc0, running, quyền `(ci-do,1,H)` | rc0, cùng kết quả |
| mo-lai connector | rc0, cho_chu_kho, quyền **`(connector,1,H)`** | rc0, quyền vẫn **`(ci-do,1,H)`** |
| chu-kho-duyet cho_phep_va trên master fixture | rc0, running, **mo_lai_tu=None** | rc8, `state hỏng (mo-lai)`, state nguyên byte |

Bằng chứng: [probes/results_original.json](probes/results_original.json), nhãn candidate-chain-* và old-counterexample-*; [mutant/results.json](mutants/r813_quyen_mo_lai_giu_cu/results.json). rc8 ở ca nối là từ chối có kiểm soát của `_load`, không traceback. Tín dụng chính đóng phản chứng là oracle tuple ngay sau connector, không chỉ việc lệnh sau từ chối state.

**Định danh, băm và merge.** Đo bằng byte và Git object, không dùng tên nhánh làm danh tính. [IDENTITY.json](IDENTITY.json) lưu từng command, rc, stdout/stderr.

| phép đo | rc | bằng chứng dương |
|---|---:|---|
| `sha256sum tham-chieu/wp813-r2.md src/ops/specs/may-adr-0054-chung.md` | 0 | Cả hai khớp đủ 64 ký tự ở dòng 3. |
| `git -C src rev-parse HEAD HEAD^{tree} refs/remotes/origin/master` | 0 | Head dòng 2; tree `608cd03d01eec5a21ebe2bd171c70470f8bbc593`; base/ref `a917673114ae03ba4f7ab19d308de0a4ed6d8341`. |
| `git -C src merge-base --is-ancestor a917673114ae03ba4f7ab19d308de0a4ed6d8341 25bd151727b5be2574594cf104658048816c4942` | 0 | Base là tổ tiên head. |
| `git -C src symbolic-ref -q HEAD`; `rev-parse --is-shallow-repository` | 1 kỳ vọng; 0 | Detached, false; `.git` là thư mục. |
| `git -C src diff --numstat a917673114ae03ba4f7ab19d308de0a4ed6d8341 25bd151727b5be2574594cf104658048816c4942` | 0 | packet_loop.py **+153/-11**; packet_loop_test.py **+218/-3**. Đúng 2 đường dẫn, **371 dòng thêm ≤450**. |
| `git -C src diff --check <base> <head>` | 0 | Rỗng. |
| `git -C src diff --exit-code 083807e 25bd151 -- .claude/dev/packet_loop.py .claude/dev/packet_loop_test.py` | 0 | Rỗng: merge không đổi hai tệp write set. |

Blob code ở cả 083807e và head: `64020cf2ff7c8ab23f0a0958ce2ea13abb7e3afb`; blob test: `dac0434460141ee6ec5b52c46aaa00e564dcfba2`. Các phụ thuộc validator/launcher/AGENTS/protocol/ADR cũng không đổi qua merge: [MERGE_DEPENDENCIES.json](MERGE_DEPENDENCIES.json). Master mang vào `.claude/dev/launcher_test.py` (+3 dòng xử lý phép đo ngoài Linux) và hồ sơ `ops/land/**`; packet_loop/harness không nhập hoặc gọi launcher_test. Không nhận các hồ sơ land ấy làm bằng chứng review của mình. Lease bản chép có đường handoff riêng nhánh lease; diff PR vẫn chỉ hai tệp. Base lease f577ab5 là mốc cấp lịch sử, base review lần này là a917673 theo assignment.

**Đối chiếu từng ca bắt buộc trong nghiệm thu.** Mọi ca trong bảng PASS trên candidate. Ngoại lệ dưới đây được đo ở đúng ca trên mutant, không suy từ rc chung của runner.

| yêu cầu | ca r813 tương ứng | mutant | lỗi của đúng ca / lý do giết |
|---|---|---|---|
| Chạm trần qua mo-lai → blocked | `r813_cham_tran_mo_lai` | `r813_mo_lai_khong_xet` | AssertionError bước 1: đòi rc3, được0 — bỏ xét dừng. |
| Cùng nguyên nhân dưới hai comment ID → chung bộ đếm | `r813_cung_slug_hai_id` | `r813_dem_theo_id` | AssertionError bước 4: đòi3, được0 — đếm ID thay slug làm né trần. |
| Đối chứng hai nguyên nhân độc lập | `r813_hai_slug_doc_lap` | `r813_gop_nguyen_nhan` | AssertionError bước 4: đòi0, được3; gop×2 — gộp sai lớp gây chặn oan. |
| Slug không nằm trong H | `r813_slug_ngoai_bien_nhan` | `r812_bo_slug_trong_bang` | AssertionError bước 0: đòi11, được0 — bỏ chốt slug H dùng chung. |
| begin-attempt khi bộ đếm chạm | `r813_begin_attempt_cham` | `r813_begin_khong_xet` | AssertionError bước 2: đòi3, được0. |
| Cửa khép lượt không bị chặn | `r813_cua_khep_khong_chan` | `r813_chan_cua_khep` | AssertionError bước 3: đòi0, được3; ci-gate×1 — chặn oan cửa ghi kết quả. |
| mo-lai không finding | `r813_khong_finding` | `r813_bo_tap_rong` | AssertionError bước 0: đòi2, được0. |
| Connector chỉ phủ tập con P0–P2 | `r813_connector_tap_con` | `r813_tap_con_lot` | AssertionError bước 0: đòi11, được0 — tập con lọt thay tập bằng đúng. |
| CI đỏ và connector P1 cùng head | `r813_ci_va_p1_cung_head` | `r813_bo_ci_do` | AssertionError bước 0: đòi12, được0 — lẽ ra phải dùng nguyên nhân connector. |
| Connector đến sau CI: điều kiện vào | `r813_connector_sau_ci` | `r813_chi_tu_approved` | AssertionError bước 1: đòi0, được8; không chạy từ running — siết oan đường CI. |
| Connector đến sau CI: thời điểm hoàn tất | `r813_connector_sau_ci` | `r813_ci_do_doi_connector_xong` | AssertionError bước 0: đòi0, được12; connector chưa xong — siết oan CI khi connector đang chạy. |
| Connector sau CI: thay/dùng quyền, khóa phản chứng lượt 3 | `r813_connector_sau_ci`, `r813_connector_sau_ci_roi_duyet` | `r813_quyen_mo_lai_giu_cu` | AssertionError nội dung quyền sai; ca nối đòi0/được8, state hỏng (mo-lai). |
| Checkpoint chỉ trên nhánh khác | `r813_checkpoint_nhanh_khac` | `r813_checkpoint_ref_tuy_y` | AssertionError bước 1: đòi7, được0 — đọc HEAD tùy ý thay master đã đo. |
| Checkpoint packet khác | `r813_checkpoint_packet_khac` | `r813_bo_packet_checkpoint` | AssertionError bước 1: đòi7, được0. |
| Không dùng cho_phep_va làm quyền đẩy | `r813_va_lam_quyen_day` | `r813_moi_pham_vi_la_du` | AssertionError bước 0: đòi7, được0. |
| M5 run mới in_progress thiếu repository | `r813_m5_run_moi_thieu_repository` | `r813_m5_bo_repository` | AssertionError r834 accept: đòi12, được0 — nhận run cũ xanh. |
| M5 path sai kiểu | `r813_m5_run_path_sai_kieu` | `r813_m5_bo_path` | AssertionError accept: đòi12, được0. |
| M5 head_sha sai kiểu | `r813_m5_run_head_sai_kieu` | `r813_m5_bo_head_sha` | AssertionError accept: đòi12, được0. |
| M5 full_name sai kiểu, khóa biểu hiện lượt 2 | `r813_m5_run_full_name_sai_kieu` | `r813_m5_bo_full_name` | AssertionError accept: đòi12, được0. |
| M5 đối chứng accept hiện có | **63/63 ca r834 PASS** | Các mutant đổi mỏ neo/dùng chung chạy lại | r834_bo_attempt_moi_nhat, r834_bo_job_xanh, app/workflow/run mới nhất đều bị đúng ca bắt. |

Tổng audit: **36 mutant tiền tố r813  + 4 dùng chung có target r813  + 2 mutant r834 đổi mỏ neo = 42 mutant, 47 quan hệ target GIẾT đúng, 126 đối chứng khác họ PASS**. Không thiếu/trùng mỏ neo, không target vắng, không BO_QUA/TIN_DUNG_GIA/SONG trong tập target. Toàn bộ tên ca, ngoại lệ và thông điệp 47 quan hệ: [MUTATION_AUDIT.md](MUTATION_AUDIT.md); dữ liệu không cắt ngắn: [mutants/results.json](mutants/results.json). Ca quyền giữ đủ state trong JSON. Hai helper chon.py/dotbien.py đã được đọc trước khi dùng logic; runner riêng tái dùng chay_suite, phân loại mutant và đối chứng, thêm kiểm inventory không rỗng, neo duy nhất và giữ thông điệp đầy đủ.

**Bất biến I1–I11 và M1/M2/M3/M5.** Đã rà các đường đọc state, begin/review, H canon, connector, CI, mo-lai, checkpoint, parser và các hunk test/codepage.

| bất biến/mục tiêu | kết quả và bằng chứng |
|---|---|
| I1 / M2–M3 | mo-lai dùng H qua `_du_dieu_kien_approve`; rời cho_chu_kho dùng Đ: fetch master, so ls-remote, đọc blob tại OID vừa đo. R chỉ bổ sung. |
| I2 | Đường cấp lease không đổi. Baseline dựng H/Đ/R thật trên bare repo cục bộ; 148 ca r812 PASS. Không xác minh lease thật ngoài bundle bằng mạng. |
| I3 | Finding rỗng, refs thiếu/trùng/thừa/sai dạng đều bị từ chối ở candidate. failure/timed_out/startup_failure nhận rc0; cancelled/neutral/skipped/action_required/success/stale/null/rỗng bị chặn rc12. |
| I4 | Các ca âm kiểm state nguyên byte. 75 probe chính và 9 probe checkpoint/khóa state lưu hash trước/sau; các lần từ chối đều nguyên byte. Hợp lệ chạm trần ghi findings/history rồi blocked. `_save` mã hóa trước mở tệp. |
| I5 / M1 | Hai cửa mới gọi chung `_xet_dung` sau kiểm đầu vào; mutant xét sớm bị bắt đòi11/được3. Probe checkpoint sai packet khi bộ đếm chạm vẫn rc7/nguyên byte. begin-attempt bị chặn; record-review khép lượt vẫn chạy. |
| I6 | Candidate thay ci-do bằng connector, checkpoint mới thay checkpoint cũ, cho_phep_va tiêu thụ mo_lai_tu. Oracle mới khóa quyền thay; ca checkpoint khóa quyền riêng/tiêu thụ/dùng lại. Tiêu thụ tại cửa đẩy thuộc #816, không suy đã triển khai ở đây. |
| I7 | Head từ state: pending_sha khi approved_pending; SHA nguồn trong quyền ci-do khi running, cùng generation; không có cờ caller tự chọn head. Probe đổi pending_sha sau CI vẫn dùng SHA nguồn trong quyền. R sai kho/PR/head bị chặn. CI chọn run/workflow/repo/head mới nhất, attempt/job/check-run/suite/app; check đỏ so đúng head. Trang qua tập ID phân biệt, không so chéo không gian ID. |
| I8 | H tái dùng chuẩn hóa provider/họ/surface/transport của validator canon, không thêm chuẩn riêng. Probe executor sai và hồi quy r812 đều đúng. |
| I9 | accept không truyền p0p2: vẫn đòi connector hoàn tất và chặn P0–P2. 63 r834, 148 r812 và hai codepage PASS; state cũ vắng quyền mới vẫn đọc được. Không suy Linux codepage thành Windows thật. |
| I10 | H sai packet/generation/reviewed_sha/spec_hash/role/verdict bị chặn rc11/nguyên byte. Checkpoint sai tuple/phạm vi/người quyết bị chặn rc7. Vai trò nguồn của connector sau CI dùng SHA nguồn đã ghi, không lấy từ caller. |
| I11 | Slug lấy từ bảng H, đủ mọi lớp; bộ đếm đọc lại từ reviews + sự kiện mo_lai. Hai ID cùng nguyên nhân chung bộ đếm, hai nguyên nhân riêng đếm riêng. Mutant đếm theo ID/gộp lớp đều bị bắt. |
| M5 | Kiểm path/head_sha/repository/full_name của mọi run trước lọc. Ca thiếu/sai kiểu và probe run khác workflow có trường scope hỏng đều rc12 với KHÔNG ĐO ĐƯỢC, nguyên byte. |

cho_chu_kho không có đường transition thoát; bốn đích transition cùng begin-attempt đã thử đều rc8/nguyên byte. Checkpoint lỗi fetch hoặc ls-remote lệch sau fetch đều rc7/nguyên byte; baseline qua cùng wrapper rc0. Đây là fault injection ở ranh giới Git và bare repo cục bộ, không phải phép đo race trên mạng thật. Lược đồ checkpoint có tập khóa đóng, từng phần tử phạm vi thuộc miền cho phép; mỗi cặp (hash hiện vật, phạm vi) dùng một lần. Không thấy mâu thuẫn đặc tả con/phần chung buộc đổi hợp đồng accept. Protocol §4/§12 chưa mô tả cho_chu_kho là phần M4 đã tách rõ khỏi r2; hai gate doctrine/ADR vẫn xanh.

**Lệnh đã chạy và bằng chứng dương.** Mọi script/fixture/mutant nằm dưới OUT. Môi trường: `PYTHONDONTWRITEBYTECODE=1`, `TMPDIR=OUT/tmp`, `GIT_CONFIG_GLOBAL=/dev/null`, `GIT_CONFIG_SYSTEM=/dev/null`, `GIT_OPTIONAL_LOCKS=0`, `GIT_ALLOW_PROTOCOL=file`; copy có core.abbrev=7. Fixture có commit/fetch/push/ls-remote chỉ với repo bare cục bộ dưới OUT; không mạng/GitHub, không thao tác remote repository packet.

| command/phép đo | rc | bằng chứng / artifact |
|---|---:|---|
| `python -B out/bootstrap.py` | 0 | Định danh, băm, snapshot đầu, copy; IDENTITY.json, FULL.diff, FIX.diff. |
| `python -B -W ignore out/run_review.py baseline_r813_r834 r813_,r834_` | 0 | **105/105 PASS = 42 r813 + 63 r834**; baseline_r813_r834/results.json, summary.json, logs/baseline_r813_r834.log. |
| `python -B -W ignore out/run_review.py baseline_r812 r812_,stdout_cp` | 0 | **150/150 PASS = 148 r812 + 2 codepage**; baseline_r812/results.json, inventory.json, logs/baseline_r812.log. |
| `python -B -W ignore out/run_review.py mutants` | 0 | **42 mutant / 47 target GIẾT / 126 đối chứng PASS**; mutants/results.json, logs/mutants.log. |
| `python -B -W ignore out/probes.py` | 0 | **75** phép gọi CLI đã assert rc/lý do/byte state/quyền; probes/results_original.json, logs/probes.log. |
| `python -B -W ignore out/checkpoint_probes.py` | 0 | **9** phép gọi kiểm fetch/ls-remote/đường thoát state; checkpoint_probes/results.json, logs/checkpoint_probes.log. |
| `python -B -W ignore out/extra_mutation.py` | 0 | Mutant **SỐNG 105/105**; A/B candidate rc11/mutant rc0; oracle reviewer PASS candidate, GIẾT mutant đúng AssertionError; 3 đối chứng PASS mỗi vế. extra_ref_shape/**, logs/extra_mutation.log. |
| `python -B out/copy/.claude/dev/packet_loop.py doctrine-scan --root out/copy` | 0 | **10 tệp, 0 chỗ chép doctrine**; GATES.json. |
| `python -B out/copy/.claude/dev/packet_loop.py adr-song --root out/copy` | 0 | **55 ADR/55 dòng §20**, khớp 1–1, ngoại lệ 0016 khai sẵn; GATES.json. |

Tổng nền chọn lọc **255/255 PASS**, không failed/skipped trong tập được chọn. `r812_r4_own_parent` bị loại **trước chạy** vì soạn nội dung đường dẫn có thành phần cha; không tính vào 255 và không gọi là pass. rc0 của extra_mutation chỉ có nghĩa phép đo hoàn tất, không có nghĩa suite gốc giết được mutant. Không gộp số probe/đối chứng thành N/N toàn repository.

**Giới hạn.** `not_run`: full suite `python .claude/dev/packet_loop_test.py` và toàn bộ mutant repository (prompt ưu tiên chọn lọc), mutant #812/#834 ngoài tập nêu trên, CI online, Windows thật, bare Ruff lint và Ruff pin/probe contract. Không nhận lời khai gate executor làm kết quả độc lập. Hướng thử đường dẫn thoát cây chỉ mô tả bằng lời: checkpoint/receipt hoặc liên kết dẫn ra ngoài cây phải bị chặn trước đọc/ghi ngoài phạm vi và giữ state nguyên byte; không tự soạn payload như vậy.

M4/protocol, vòng P3 #814, generation kế tiếp #815, ghi đẩy/tiêu thụ quyền tại cửa đẩy #816 và kích hoạt ADR-0054 nằm ngoài phạm vi. Nợ P3 #834 required-mutation-coverage-missing không được mở lại, nâng hạng hay khai đã đóng; biểu hiện mới ở đây thuộc check_refs của mo-lai #813.

**Toàn vẹn cuối lượt.** SOURCE_INITIAL/SOURCE_FINAL so cả tracked/untracked/ignored và `.git`; yêu cầu 0 delta byte/mode, HEAD/tree/ref không đổi, source và copy sạch worktree/index, code/test/chung bằng blob exact candidate. Xem SOURCE_INTEGRITY.json và FINAL_CHECKS.json cho số đo cuối; ARTIFACTS.json băm verdict, script, diff, log và kết quả, không đưa toàn bộ fixture/copy vào manifest. Snapshot đầu được tạo sau preflight và trước mọi phép thử: đây là đối chiếu hai mốc, không là giám sát mọi write trong lịch sử. Sandbox thực tế workspace-write; source được đối xử chỉ đọc, mọi artifact reviewer ở OUT.

Đo cuối: `python -B out/finalize.py` **rc0**; **7003 → 7003 tệp, 0 delta byte/mode**. HEAD/tree/ref không đổi; source và copy sạch.
