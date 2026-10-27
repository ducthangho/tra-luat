Verdict: approve
Reviewed commit: 83358d40e59c6fb8edef6347de049570887a66ca
Spec sha256: 9df36da1ef2be23c7519934bf6aee0dfecb6d2082cb8e485c7a6819c8a6154f3; Chung sha256: 4e3d1e1b3f6a0b60b96ad7b70f0ece97eca4bb3d6d10defeab1cd24ac6d1cbf0

**Kết luận lượt 5: 0 P0/P1/P2; giữ nguyên 1 lớp P3, 1 biểu hiện của lượt 4.** Đây là biên nhận xác minh merge. Hai tệp write set tại head mới giống từng byte với `25bd151727b5be2574594cf104658048816c4942`; base mới là tổ tiên head. Thay đổi protocol/ADR-0056 không làm đổi hợp đồng các cửa của packet trong các phép đo dưới đây. Ngưỡng approve theo assignment: không còn P0/P1/P2. Verdict chỉ neo commit dòng 2, không cấp quyền push, merge hoặc land.

| slug | hạng P0–P3 | biểu hiện file:dòng | phép đo/tái hiện đã chạy | hướng vá |
|---|---|---|---|---|
| `r813-mutation-evidence-incomplete` | **P3 — CHƯA VÁ, giữ nguyên lượt 4** | `.claude/dev/packet_loop.py:2970`; bộ test từ `.claude/dev/packet_loop_test.py:8924` chưa bảo vệ phép so số refs đúng dạng với tổng refs khai ở nhánh CI. | Tự tái dựng mutant bỏ phép so độ dài: sống **105/105 ca r813+r834**. A/B một ref workflow/job hợp lệ cộng phần tử null: candidate rc11, state nguyên byte; mutant rc0, running. Oracle reviewer giết bằng `AssertionError: mixed refs must reject: đòi rc=11, được rc=0`; 3 đối chứng khác họ PASS trên mỗi vế. | Owner: executor Packet #813 (Claude), chủ kho theo dõi. Thêm ca mixed check_refs vào test, đòi rc11 + lý do + nguyên byte; khai mutant bỏ đúng phép so độ dài. Giữ predicate sản phẩm đang đúng. |

Tên nợ: **thiếu phản chứng bảo vệ việc không bỏ qua phần tử check_refs sai hình dạng**. Lý do giữ P3: đây là đúng nợ P3 đã được lượt 4 chấp nhận, code/test không đổi; chỉ thị riêng (c) của lượt xác minh merge yêu cầu giữ hạng nếu không đổi. Không áp nâng P2 tự động cho việc tái đo nợ này; không có lỗi sản phẩm hoặc ca nghiệm thu bắt buộc bị thiếu. Không phát hiện lớp P0–P2 mới do merge.

Bốn phần gợi ý: sửa vùng test r813; dùng nền approved_pending thật và giữ cặp ref đỏ hợp lệ khi thêm null; oracle phải kiểm rc/lý do/state và được mutant làm đỏ; tránh fixture chỉ có refs hỏng vì chốt khác có thể bắt thay, tạo tín dụng sai. [extra_mutation.py](extra_mutation.py), [cặp tìm/thay](extra_ref_shape/mutation.json), [A/B](extra_ref_shape/ab_results.json), [oracle](extra_ref_shape/oracle_results.json) là bằng chứng trên bản sao riêng, không phải patch sản phẩm giao áp lên source.

**Phạm vi, nguồn và danh tính.** Đã đọc toàn bộ `runs/4a00bdd3/prompt.snapshot`; mọi đường dẫn tương đối tính từ gốc rv5 theo chỉ thị trực tiếp. Review độc lập, offline, packet #813/revision 2/generation 1, review_class sensitive, assurance_target cross_approved. Reviewer Codex/OpenAI, họ openai; executor theo lease bản chép là Claude, họ claude. Thực thi shell qua công cụ Linux, transport machine; exact serving model/effort/session và attestation launcher `codex_cli` không được đo độc lập ở đây. Không tạo receipt assurance và không suy model identity từ actor GitHub. Không kế thừa context executor; verdict trước là bằng chứng lịch sử, không thay phép đo riêng.

Đặc tả con và phần chung đã băm lại, khớp dòng 3. Lease bản chép có thêm đường handoff dành riêng nhánh lease; diff PR vẫn chỉ hai tệp. Base lease `f577ab5` là mốc cấp lịch sử, base review lượt này là `7129f7d` theo assignment. Không xác minh online lease, PR #969, check thu-hoi hoặc comment chủ kho; các thông tin này là bối cảnh do assignment cung cấp. Verdict #834 lượt 8 là đầu vào thiết kế; không mở lại nợ ngoài M5.

**ĐỐI CHIẾU LƯỢT TRƯỚC.** [Verdict lượt 4](../tham-chieu/wp813-g1-codex-luot4-VERDICT.md), SHA-256 `c0be64699b26b9b3a43d8b3a12c0f11b956a041382d827d6283e4071d0e37ae2`, neo `25bd151727b5be2574594cf104658048816c4942`.

| lớp/biểu hiện | trạng thái lượt 5 | bằng chứng độc lập |
|---|---|---|
| `r813-mutation-evidence-incomplete`, mixed check_refs | **CHƯA VÁ — P3 giữ nguyên** | Blob/byte không đổi; mutant 105/105 sống; A/B candidate từ chối đúng và oracle reviewer giết mutant. |
| Biểu hiện P2 cũ: giữ mo_lai_tu ci-do sau connector | **Giữ ĐÃ VÁ THẬT** | Mutant `r813_quyen_mo_lai_giu_cu` bị oracle tuple của `r813_connector_sau_ci` bắt (`nội dung quyền sai`); ca nối tới checkpoint cũng đỏ rc8 thay rc0. Không coi rc8 đơn lẻ là bằng chứng chính; oracle tuple mới là chốt. |
| `ci-reopen-run-context-unbound`, đã đóng trước lượt 4 | **Giữ ĐÃ VÁ THẬT** | Ca wrong-head, wrong-app, wrong-workflow/run mới nhất PASS; mutant head/app/workflow bị bắt đúng. Probe check-run khác head/kho hoặc bản mới hơn đều rc12 và state nguyên byte. |
| M5 full_name và thay checkpoint_day, đã đóng | **Giữ ĐÃ VÁ THẬT** | `r813_m5_bo_full_name` chết đúng ở accept rc0 thay12; `r813_quyen_day_giu_cu` chết tại oracle quyền checkpoint mới. |

Không đổi slug, không reset lịch sử và không tuyên bố lớp độ phủ đã đóng. Việc giữ P3 áp dụng theo chỉ thị cụ thể của lượt merge, không làm yếu luật phân hạng chung cho lỗi sản phẩm hoặc phản chứng P2 chưa sửa.

**Định danh và trần diff.** [IDENTITY.json](IDENTITY.json) ghi command/rc/output/hash. `python -B out/bootstrap.py` rc0.

| phép đo | rc | bằng chứng dương |
|---|---:|---|
| Băm hai đặc tả bằng SHA-256 trên byte | 0 | Khớp đủ hai hash dòng 3; `sha256sum` độc lập cũng khớp. |
| `git -C src rev-parse HEAD HEAD^{tree} refs/remotes/origin/master` | 0 | HEAD dòng 2; tree `f619d6ddcb7e7cc06fe0bb9d6a1a303b019e46ba`; base/ref `7129f7de204a6f92db8e29e8a5a79383d4907029`. |
| `git -C src merge-base --is-ancestor <base> <head>`; tương tự `<prior> <head>` | 0 mỗi lệnh | Base và head lượt 4 đều là tổ tiên head mới. |
| `git -C src symbolic-ref -q HEAD`; `rev-parse --is-shallow-repository` | 1 kỳ vọng; 0 | Detached HEAD, `false`; `.git` là thư mục thật. |
| `git show <commit>:<path>` và `git rev-parse <commit>:<path>` ở prior/head | 0 mỗi lệnh | Cùng blob OID, byte prior = byte head = byte worktree cho cả hai tệp. |
| `git -C src diff --numstat <base> <head>` | 0 | packet_loop.py +153/-11; packet_loop_test.py +218/-3. **2 đường dẫn, 371 dòng thêm ≤450**. |
| `git -C src diff --check <base> <head>` | 0 | Output rỗng. |

| tệp | blob OID ở cả prior và head |
|---|---|
| `.claude/dev/packet_loop.py` | `64020cf2ff7c8ab23f0a0958ce2ea13abb7e3afb` |
| `.claude/dev/packet_loop_test.py` | `dac0434460141ee6ec5b52c46aaa00e564dcfba2` |

Đã đọc toàn bộ [FULL.diff](FULL.diff), `git diff 7129f7d 83358d4`, và [MERGE.diff](MERGE.diff), `git diff 25bd151 83358d4`. Không chỉ xem tên tệp/thống kê.

**Tương tác merge.** Delta merge chỉ có protocol (+1/-1) và ADR-0056 (+11/-4). `git diff --raw --no-abbrev <prior> <head>` bằng đúng byte output của `<merge-base> <base>`; merge-base là `a917673114ae03ba4f7ab19d308de0a4ed6d8341`. Không có chỉnh sửa merge riêng ngoài delta master.

- **Protocol §4 không đổi qua merge.** Điều kiện lease mới sau kích hoạt 0056 dùng 360 phút đã có trong §4; lease cũ giữ nguyên giá trị đóng dấu, nên lease #813 khai 30 không bị hồi tố. Graph vẫn chưa ghi cho_chu_kho: đó là M4 đã tách khỏi r2, không tính hạng ở packet này.
- **§20 chỉ đổi dòng ADR-0056.** Dòng ADR-0054 giữ nguyên “chưa kích hoạt”; `_che_do_0054` (`packet_loop.py:2563`) chọn riêng dòng 0054 và tìm cụm kích hoạt 0054 trong ADR khác. Nội dung mới của 0056 không thoả cụm đó. Phép gọi helper trên bản sao kho thật, với dòng khai 0054 hợp lệ và birth OID đã đo `7cc384ec9e02ed79b429ac6ee2455d3bfbb75b16`, vẫn trả **False**. Đây là phép đo helper hỗ trợ, không tính thành ca CLI.
- **CANON và H.** Protocol là phụ thuộc được `_canon` chép từ origin/master. `_nap` nạp validator thật dưới protocol mới trả `PROVIDER_NGUON_HONG=None`; hash protocol chép khớp byte head. §8 và các neo provider/assurance không đổi. lease_publish.py, bien_nhan_v2.py, launcher.py, AGENTS.md, CLAUDE.md và phần chung giữ nguyên OID.
- **Đối chiếu CLI hai phía.** Fixture riêng nhận nguyên protocol/ADR-0056 của prior và candidate. Khi dòng 0054 chưa kích hoạt, record-lease rc0/leased/luat_adr0054=False ở cả hai phía. Khi fixture chủ ý bật riêng dòng 0054 và có hiện vật kích hoạt của fixture, record-review rc0/approved_pending, mo-lai connector rc0/cho_chu_kho, chu-kho-duyet cho_phep_va rc0/running và tiêu thụ mo_lai_tu ở cả hai phía. **8 kết quả CLI đều đạt**; không thay nguồn packet hoặc kích hoạt ADR thật.
- **Gate đọc tài liệu.** doctrine-scan đọc protocol làm nguồn đối chiếu: 10 tệp, 0 chỗ chép doctrine. adr-song đọc docs/adr và §20: 55 ADR/55 dòng, khớp 1–1, ngoại lệ 0016 khai sẵn. Cả hai rc0; không nới chốt để tránh sửa protocol.

Bằng chứng: [merge_checks/results.json](merge_checks/results.json), [merge_cli/results.json](merge_cli/results.json), [gates/results.json](gates/results.json). Không thấy mâu thuẫn mới buộc đổi hợp đồng accept hay chạm M4.

**Đối chiếu từng ca bắt buộc của nghiệm thu.** Mỗi ca trong bảng PASS trên candidate. Đã đọc fixture: dựng nền approved_pending thật qua H/Đ/R; ca âm đòi rc, lý do và state nguyên byte; ca chạm trần đòi blocked cùng sổ finding. Cột cuối là ngoại lệ đo ở đúng ca trên mutant, không suy từ rc chung.

| yêu cầu | ca tương ứng | mutant | lỗi đo được / lý do giết |
|---|---|---|---|
| Chạm trần qua mo-lai | `r813_cham_tran_mo_lai` | `r813_mo_lai_khong_xet` | AssertionError: r813 bước 1: đòi rc=3, được rc=0; stderr='' |
| Hai comment ID cùng nguyên nhân chung bộ đếm | `r813_cung_slug_hai_id` | `r813_dem_theo_id` | AssertionError: r813 bước 4: đòi rc=3, được rc=0; stderr='' |
| Hai nguyên nhân độc lập đếm riêng | `r813_hai_slug_doc_lap` | `r813_gop_nguyen_nhan` | AssertionError: r813 bước 4: đòi rc=0, được rc=3; stderr='cùng finding-id lặp tới trần (gop×2; trần 2) — packet về blocked. Lặp lại nghĩa là bản vá không trúng gốc; ghi failure evidence + handoff rồi dừng.' |
| Slug ngoài H bị từ chối | `r813_slug_ngoai_bien_nhan` | `r812_bo_slug_trong_bang` | AssertionError: r813 bước 0: đòi rc=11, được rc=0; stderr='' |
| begin-attempt khi đã chạm | `r813_begin_attempt_cham` | `r813_begin_khong_xet` | AssertionError: r813 bước 2: đòi rc=3, được rc=0; stderr='' |
| Cửa khép lượt không bị chặn | `r813_cua_khep_khong_chan` | `r813_chan_cua_khep` | AssertionError: r813 bước 3: đòi rc=0, được rc=3; stderr='cùng finding-id lặp tới trần (ci-gate×1; trần 1) — packet về blocked. Lặp lại nghĩa là bản vá không trúng gốc; ghi failure evidence + handoff rồi dừng.' |
| Không finding bị từ chối | `r813_khong_finding` | `r813_bo_tap_rong` | AssertionError: r813 bước 0: đòi rc=2, được rc=0; stderr='' |
| Connector tập con P0–P2 bị từ chối | `r813_connector_tap_con` | `r813_tap_con_lot` | AssertionError: r813 bước 0: đòi rc=11, được rc=0; stderr='' |
| CI đỏ và connector P1 cùng head | `r813_ci_va_p1_cung_head` | `r813_bo_ci_do` | AssertionError: r813 bước 0: đòi rc=12, được rc=0; stderr='' |
| Connector sau CI: vào từ running | `r813_connector_sau_ci` | `r813_chi_tu_approved` | AssertionError: r813 bước 1: đòi rc=0, được rc=8; stderr="mo-lai connector không chạy từ 'running' (đòi approved_pending của packet áp ADR-0054, hoặc running mở lại bằng ci-do cùng generation)" |
| Connector sau CI: CI không chờ connector xong | `r813_connector_sau_ci` | `r813_ci_do_doi_connector_xong` | AssertionError: r813 bước 0: đòi rc=0, được rc=12; stderr='connector chưa xong trên 85ab4b90cfeb36bc23f891f17ba4b2d6910f562b: không review hoàn tất/kết luận nào của chatgpt-codex-connector[bot]' |
| Connector sau CI: thay quyền | `r813_connector_sau_ci` | `r813_quyen_mo_lai_giu_cu` | AssertionError: r813: nội dung quyền sai — quyền vẫn ci-do thay vì connector, cùng generation/head. Chi tiết state đầy đủ trong audit. |
| Connector sau CI: dùng quyền ở checkpoint | `r813_connector_sau_ci_roi_duyet` | `r813_quyen_mo_lai_giu_cu` | AssertionError bước 2: đòi rc0, được rc8; state hỏng (mo-lai). Oracle tuple ở hàng trước là bằng chứng chính. |
| Checkpoint chỉ ở nhánh khác bị từ chối | `r813_checkpoint_nhanh_khac` | `r813_checkpoint_ref_tuy_y` | AssertionError: r813 bước 1: đòi rc=7, được rc=0; stderr='' |
| Checkpoint packet khác bị từ chối | `r813_checkpoint_packet_khac` | `r813_bo_packet_checkpoint` | AssertionError: r813 bước 1: đòi rc=7, được rc=0; stderr='' |
| cho_phep_va không thành quyền đẩy | `r813_va_lam_quyen_day` | `r813_moi_pham_vi_la_du` | AssertionError: r813 bước 0: đòi rc=7, được rc=0; stderr='' |
| M5 run mới in_progress thiếu repository | `r813_m5_run_moi_thieu_repository` | `r813_m5_bo_repository` | AssertionError: r834 accept: đòi rc=12, được rc=0; stderr='' |
| M5 path sai kiểu | `r813_m5_run_path_sai_kieu` | `r813_m5_bo_path` | AssertionError: r834 accept: đòi rc=12, được rc=0; stderr='' |
| M5 head_sha sai kiểu | `r813_m5_run_head_sai_kieu` | `r813_m5_bo_head_sha` | AssertionError: r834 accept: đòi rc=12, được rc=0; stderr='' |
| M5 full_name sai kiểu | `r813_m5_run_full_name_sai_kieu` | `r813_m5_bo_full_name` | AssertionError: r834 accept: đòi rc=12, được rc=0; stderr='' |
| M5 đối chứng mọi ca accept hiện có | **63/63 r834 PASS** | 5 mutant r834 dùng chung/đổi mỏ neo đã chạy | Cùng hợp đồng accept; app/workflow/run mới nhất/attempt/job xanh đều được bảo vệ ở các ca đã đo. |

Tổng audit **36 mutant r813 + 4 dùng chung có target r813 + 2 mutant r834 đổi mỏ neo = 42 mutant, 47 target GIET, 126 đối chứng PASS**. Không thiếu/trùng neo, target vắng, SONG/BO_QUA/TIN_DUNG_GIA trong tập khai phải chết. Đã đọc tên ca, lớp AssertionError và thông điệp để loại kill vì lỗi fixture hoặc CLI sập. [MUTATION_AUDIT.md](MUTATION_AUDIT.md) và [JSON đầy đủ](mutants/results.json) giữ cả thông điệp dài và state của oracle quyền.

Hai helper chon.py/dotbien.py đã được đọc trước khi dùng logic. Runner riêng tái dùng chay_suite và phân loại/đối chứng của main(), đồng thời kiểm tập tên không rỗng, target tồn tại, neo duy nhất và lưu thông điệp không cắt. Không dựa vào rc0 của helper với tập rỗng. Mutant reviewer ngoài MUTANTS tái dựng đúng nợ lượt 4, không mở thêm vòng thiết kế; sự sống của nó được ghi rõ ở bảng lớp.

**Bất biến I1–I11 / M1, M2, M3, M5.** Rà không lọc các hunk và các đường gọi liên quan: load/history, lease/canon, review, connector/CI, mo-lai, checkpoint, xét dừng, parser, codepage. Không kế thừa kết quả probe chưa chạy lại của lượt trước.

| bất biến/mục tiêu | kết quả trên head mới |
|---|---|
| I1, I2 / M2–M3 | mo-lai tái dùng H `_du_dieu_kien_approve` với changes_requested; rời cho_chu_kho dùng checkpoint Đ sau fetch/ls-remote. R chỉ bổ sung. Đường lease H/Đ/R không đổi; hồi quy r812 và phép đo CANON mới đạt. |
| I3 | Finding phải khác rỗng; refs được kiểm hình dạng/không lặp; connector bằng đúng P0–P2. Probe refs rỗng/null/sai kiểu/trùng/thừa/mixed-null từ chối. CI chỉ nhận failure/timed_out/startup_failure; success/cancelled/neutral/skipped/action_required/stale/null/rỗng bị chặn. |
| I4 | Ca âm r813/r834 và 34 probe kiểm byte state. Các lần đầu vào bị từ chối trong probe đều nguyên byte; đầu vào checkpoint hợp lệ khi chạm trần ghi sổ rồi blocked. |
| I5 / M1 | CUA_DI_TIEP gồm begin-attempt, mo-lai, chu-kho-duyet; dùng chung `_xet_dung` sau xác thực đầu vào. Mutant xét sớm bị bắt đúng. Probe checkpoint sai packet ở trần vẫn rc7/nguyên byte, checkpoint hợp lệ ở cùng trần rc3/blocked. Cửa khép record-review vẫn được ghi. |
| I6 | Quyền neo nguyên nhân/generation/SHA; connector thay quyền ci-do; checkpoint mới thay quyền cũ; cho_phep_va tiêu thụ mo_lai_tu; cùng hash hiện vật/phạm vi không dùng lại. Ca quyền và mutant đều đạt. Tiêu thụ quyền tại cửa đẩy thuộc #816, không suy đã có ở đây. |
| I7 | Head lấy từ pending_sha hoặc SHA nguồn của quyền ci-do trong state; running chỉ được mở theo connector khi có quyền ci-do cùng generation. CI chọn run/attempt/job/check-run theo kho/head/workflow/app; probes wrong-head/repo/latest-check bị chặn. Trang kiểm tập ID phân biệt từng endpoint, không so chéo không gian ID. |
| I8 | Không thêm chuẩn danh tính riêng; H dùng hàm chuẩn hóa của validator canon. Protocol §8/neo nguồn không đổi, validator nạp hợp lệ; hồi quy provider của r812 đạt. |
| I9 | accept không truyền p0p2 và vẫn đòi connector xong, không P0–P2. 63 r834 và 148 r812 đạt; state cũ có thể thiếu mo_lai_tu/checkpoint_day qua st.get. Hai ca codepage đạt trên Linux; không suy thành Windows thật. |
| I10 | H đối chiếu đủ packet/generation/reviewed_sha/spec_hash/role/verdict; sáu probe đổi riêng trường bị chặn rc11/nguyên byte. Checkpoint đối chiếu tuple/phạm vi/người quyết trên master đã đo; mutant từng chốt bị bắt. |
| I11 | Slug từ bảng H; finding_counts tái dựng cả reviews và history.mo_lai. Hai ID cùng slug chạm chung trần; hai slug độc lập không gộp. |
| M5 | Kiểm path/head_sha/repository/full_name của mọi run trước lọc; bốn ca sai scope làm accept rc12, lý do KHÔNG ĐO ĐƯỢC, nguyên byte. Cả bốn mutant chốt tương ứng bị bắt. |

Bằng chứng probe: [focused_probes.py](focused_probes.py), [34 kết quả CLI](focused_probes/results.json). Mọi fetch/push/ls-remote phát sinh trong fixture chỉ trỏ bare repo cục bộ dưới OUT. Không thử race mạng thật, không gọi remote GitHub.

**Lệnh đã chạy và phạm vi bằng chứng.** Môi trường test: PYTHONDONTWRITEBYTECODE=1, TMPDIR=OUT/tmp, GIT_CONFIG_GLOBAL=/dev/null, GIT_CONFIG_SYSTEM=/dev/null, GIT_OPTIONAL_LOCKS=0, GIT_ALLOW_PROTOCOL=file; core.abbrev=7 trên copy. Mọi script/mutant/fixture/output nằm trong OUT. Các lệnh Python dưới chạy với `-B`; các runner test thêm `-W ignore` để không lẫn SyntaxWarning nền vào bằng chứng.

| command | rc | bằng chứng dương / artifact |
|---|---:|---|
| `python -B out/bootstrap.py` | 0 | Định danh, băm, ancestry, blob/byte, trần diff; IDENTITY.json, FULL.diff, MERGE.diff. |
| `python -B -W ignore out/run_review.py baseline_r813_r834 r813_,r834_` | 0 | **105/105 PASS = 42 r813 + 63 r834**; baseline_r813_r834/results.json, inventory.json, summary.json, logs/baseline_r813_r834.log. |
| `python -B -W ignore out/run_review.py baseline_r812 r812_,stdout_cp` | 0 | **150/150 PASS = 148 r812 + 2 codepage**; baseline_r812/results.json, inventory.json, summary.json, logs/baseline_r812.log. |
| `python -B -W ignore out/run_review.py mutants` | 0 | **42 mutant / 47 target GIET / 126 đối chứng PASS**; mutants/results.json, summary.json, logs/mutants.log. |
| `python -B -W ignore out/run_review.py gates` | 0 | Hai subprocess doctrine-scan/adr-song đều rc0, lần lượt 10/0 và 55/55; gates/results.json. |
| `python -B -W ignore out/merge_checks.py` | 0 | Delta đúng master, §4/§8/ADR54 không đổi, helper vẫn False, CANON nguồn hợp lệ; merge_checks/results.json. |
| `python -B -W ignore out/merge_cli_probes.py` | 0 | **8 kết quả CLI** đối chiếu protocol/ADR56 cũ–mới; merge_cli/results.json. |
| `python -B -W ignore out/focused_probes.py` | 0 | **34 probe CLI** đúng rc/lý do/state; focused_probes/results.json. |
| `python -B -W ignore out/extra_mutation.py` | 0 | Mutant reviewer **SỐNG 105/105**; A/B candidate rc11/nguyên byte vs mutant rc0/running; oracle reviewer GIET đúng, 6 đối chứng PASS tổng hai vế. extra_ref_shape/**. |
| `python -B out/finalize.py` | 0 sau sửa giả định runner | **7003 → 7003 tệp, 0 delta byte/mode** ở source; copy cũng 0 delta; HEAD/tree/ref và worktree/index sạch. SOURCE_INTEGRITY.json, logs/finalize.log. |

Lần đầu finalize rc1 do runner của reviewer đòi `.git/config` phải khác sau khi đặt core.abbrev=7; thực tế nguồn đã có 7 nên delta rỗng. Đã sửa đúng giả định của runner và chạy lại rc0; không phải lỗi sản phẩm, không dùng traceback đó làm mutant kill. Các bộ test không phải chạy lại vì không đổi sản phẩm/fixture/oracle của chúng.

Tổng nền chọn lọc **255/255 PASS**, không failed/skipped trong tập được chọn. `r812_r4_own_parent` bị loại trước khi chạy vì ca soạn nội dung đường dẫn chứa thành phần cha, theo chỉ thị prompt; không tính vào 255 và không gọi là pass. Các số probe/mutant/đối chứng không cộng thành N/N toàn repository. rc0 của extra_mutation nghĩa là phép đo hoàn tất; không nghĩa là suite gốc giết được mutant P3.

**Giới hạn và toàn vẹn.** `not_run`: full suite `python .claude/dev/packet_loop_test.py` (~45–60 phút; assignment ưu tiên chọn lọc), toàn bộ mutant ngoài 42 đã nêu, CI online/thu-hoi, Windows thật, bare Ruff lint, Ruff pin/probe contract, toàn bộ 75+9 probe riêng của lượt 4. Không nhận lời khai gate executor làm kết quả độc lập. Hướng thử đường dẫn thoát cây chỉ mô tả bằng lời: receipt/checkpoint hoặc liên kết dẫn ra ngoài cây cần bị từ chối trước đọc/ghi ngoài phạm vi và giữ state nguyên byte; không tự soạn payload đó.

M4 protocol §4/§12, vòng P3 #814, generation kế tiếp #815, ghi đẩy/tiêu thụ quyền ở cửa đẩy #816 và kích hoạt ADR-0054 nằm ngoài phạm vi. Nợ #834 `required-mutation-coverage-missing` không được mở lại hoặc khai đã đóng.

Snapshot đầu/cuối gồm tracked/untracked/ignored và .git, so byte/hash và mode: **7003 → 7003, không delta**, source và copy đều sạch; HEAD/tree/ref không đổi. Đây là đối chiếu hai mốc, không phải giám sát mọi lần ghi trong lịch sử. Sandbox thực tế workspace-write; source được đối xử read-only, tất cả ghi do reviewer nằm trong OUT. [SOURCE_INTEGRITY.json](SOURCE_INTEGRITY.json) chứa số đo; [ARTIFACTS.json](ARTIFACTS.json) băm report, script, log và kết quả, không bao gồm toàn bộ fixture/copy.
