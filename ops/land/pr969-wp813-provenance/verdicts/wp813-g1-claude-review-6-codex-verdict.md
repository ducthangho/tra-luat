Verdict: approve
Reviewed commit: be88cafd7bdaee556c0ec3e60b3cba0d22efbb7e
Spec sha256: 9df36da1ef2be23c7519934bf6aee0dfecb6d2082cb8e485c7a6819c8a6154f3; Chung sha256: 4e3d1e1b3f6a0b60b96ad7b70f0ece97eca4bb3d6d10defeab1cd24ac6d1cbf0

**Kết luận lượt 6: 0 P0/P1/P2 còn mở; 1 lớp P3 với 2 biểu hiện độ phủ.** Finding connector PR #969 đã được tái hiện trên bản trước và đóng trên candidate bằng chính chuỗi CLI đã báo. Review không lọc toàn bộ diff `e3ea139…be88caf`, bao gồm các đường liên quan tới quyền cũ sau thay đổi ngữ cảnh. Ngưỡng approve theo assignment là không còn P0/P1/P2. Verdict chỉ neo commit dòng 2, không cấp quyền push, merge hoặc land.

| slug | hạng P0–P3 | biểu hiện file:dòng | phép đo/tái hiện đã chạy | hướng vá |
|---|---|---|---|---|
| `r813-mutation-evidence-incomplete` | **P3** — giữ hạng biểu hiện cũ, thêm một biểu hiện mới cùng nguyên nhân thiếu ca khóa chốt | `.claude/dev/packet_loop.py:2971`: mixed check_refs; `:2958`: vòng begin → void sau ci-do. Bộ ca tại `.claude/dev/packet_loop_test.py:8926` chưa bắt hai mutant tương ứng. | Mỗi mutant sống **106/106 ca r813+r834**. Mixed refs: candidate rc11/nguyên byte, mutant rc0/running. Void: candidate rc8/nguyên byte, mutant rc0/cho_chu_kho. Hai oracle reviewer giết đúng bằng AssertionError; 3 đối chứng khác họ PASS trên mỗi vế, mỗi mutant. | Owner: executor Packet #813 (Claude), chủ kho theo dõi. Thêm ca mixed check_refs và ca ci-do → begin → void → connector, đòi rc/lý do/nguyên byte; khai hai mutant đúng chốt. Giữ predicate sản phẩm đang đúng. |

Tên nợ: **thiếu phản chứng bảo vệ refs và việc quyền ci-do không sống lại sau void**. Đếm theo nguyên nhân: một lớp độ phủ, hai biểu hiện; không tách thành hai lớp để đổi lịch sử. Mixed check_refs là nợ lượt 4–5 không đổi, giữ P3 theo mục (c). Mutant void là phản chứng độ phủ MỚI do reviewer dựng trong lượt này; candidate xử lý đúng trong A/B và không thiếu ca nghiệm thu bắt buộc, nên P3 theo luật phân hạng chủ kho. Không nâng P2 chỉ vì một mutant mới sống. Các phản chứng P2 cũ vẫn bị đúng ca bắt.

Hướng vá đủ bốn phần: sửa phần test r813 vì thiếu quan sát nằm ở hai kịch bản này; dùng baseline approved_pending thật, một trường refs đổi từ cặp hợp lệ sang cặp hợp lệ cộng null, và một chuỗi begin/void thật sau ci-do. Oracle đòi đúng thông điệp từ chối và byte state; mutant bỏ kiểm tổng refs hoặc cho void khôi phục quyền phải làm đỏ oracle, đối chứng khác họ vẫn xanh. Rủi ro: refs chỉ có phần tử lỗi có thể bị chốt khác bắt thay; chỉ nhìn attempts_used sau void sẽ bỏ qua lịch sử begin. Không sửa mã sản phẩm để hợp thức hóa test. Mã và cặp neo/thay đã chạy ở [extra_mutations.py](extra_mutations.py), [mutation refs](extra_mutations/mixed-check-refs/mutation.json), [mutation void](extra_mutations/void-restores-ci-right/mutation.json); đây là dữ liệu phản chứng trong OUT, không phải bản vá giao áp lên SRC.

**Phạm vi và danh tính.** Đã đọc toàn bộ `runs/d54c2a29/prompt.snapshot`; mọi đường dẫn tính từ gốc rv6 theo chỉ thị trực tiếp. Reviewer độc lập Codex/OpenAI, họ openai; executor theo lease bản chép là Claude, họ claude; packet #813 revision 2 generation 1, review_class sensitive, assurance_target cross_approved. Shell qua công cụ Linux, transport machine. Exact serving model/effort/session và attestation launcher `codex_cli` không được đo độc lập trong phiên này; không tạo receipt assurance hoặc suy identity từ tài khoản GitHub. Không kế thừa context executor. Các verdict trước dùng làm lịch sử finding, không thay kết quả đo riêng.

Lease bản chép có thêm đường handoff chỉ dành nhánh lease; diff PR vẫn đúng hai tệp đặc tả. Base lease f577ab5 là mốc cấp lịch sử; base review do assignment chỉ định là e3ea139. Không xác minh online lease, PR, check thu-hoi hoặc comment chủ kho. Verdict #834 lượt 8 là đầu vào thiết kế, không thay đặc tả. M4 protocol, #814, #815, ghi đẩy/tiêu thụ quyền tại cửa đẩy #816 và kích hoạt ADR-0054 nằm ngoài phạm vi.

**Định danh độc lập.** `python -B out/bootstrap.py` rc0; [IDENTITY.json](IDENTITY.json) chứa command/rc/stdout/stderr, hash và diff.

| phép đo | rc | bằng chứng dương |
|---|---:|---|
| SHA-256 đặc tả con và phần chung | 0 | Khớp đủ hai hash dòng 3; sha256sum độc lập cũng khớp. Byte phần chung và hai tệp code/test trong worktree bằng blob exact head. |
| `git rev-parse HEAD HEAD^{tree} refs/remotes/origin/master` | 0 | HEAD dòng 2; tree `d010f718a85af630bc7e817a1d303f3bcf099144`; ref master `e3ea13923dceab7c15fc62a0823ef5f4f576e589`. |
| `git merge-base --is-ancestor e3ea139… be88caf…` | 0 | Base là tổ tiên head. |
| `git symbolic-ref -q HEAD`; `rev-parse --is-shallow-repository` | 1 kỳ vọng; 0 | Detached HEAD, false; `.git` là thư mục thật. |
| `git diff --numstat e3ea139… be88caf…` | 0 | packet_loop.py +155/-11; packet_loop_test.py +222/-3; **2 đường dẫn, 377 dòng thêm ≤450**. |
| `git diff --check`; status, diff worktree/index | 0 từng lệnh | Sạch ở các phép đo. |

Đã đọc tất cả hunk trong [FULL.diff](FULL.diff) và bản vá riêng [FIX.diff](FIX.diff), không chỉ stat/tên tệp. Đọc các đường gọi load, begin/void, record-review, transition/rescue, H/canon, connector/CI, accept, mo-lai, checkpoint, xét dừng và parser. Không phát hiện mâu thuẫn mới buộc đổi hợp đồng accept. Graph protocol chưa ghi cho_chu_kho là M4 đã tách; hai gate tài liệu vẫn xanh, không nới chốt.

**ĐỐI CHIẾU LƯỢT TRƯỚC và finding connector.**

| lớp/biểu hiện | trạng thái lượt 6 | bằng chứng độc lập |
|---|---|---|
| Connector PR #969: quyền ci-do sống qua lượt mới | **ĐÃ VÁ THẬT**; không còn P2 trong hành vi đã báo | f8d7167 nhận H/R của A sau review B changes_requested (rc0/cho_chu_kho); be88caf từ chối (rc8, đúng lý do, nguyên byte). Mutant r813_quyen_ci_qua_luot_moi bị r813_quyen_ci_sau_luot_moi giết đúng. |
| r813-mutation-evidence-incomplete: mixed check_refs P3 lượt 5 | **CHƯA VÁ — giữ P3** | Chốt sản phẩm không đổi trong FIX.diff; mutant sống 106/106. A/B tự chạy lại candidate rc11/nguyên byte, mutant rc0/running. |
| P2 cũ: giữ mo_lai_tu ci-do sau connector | **Giữ ĐÃ VÁ THẬT** | r813_quyen_mo_lai_giu_cu chết tại oracle tuple quyền của r813_connector_sau_ci; chuỗi checkpoint sau đó cũng bị bắt rc8/state hỏng. Dùng oracle tuple làm bằng chứng chính, không dựa riêng rc8 của bước sau. |
| ci-reopen-run-context-unbound | **Giữ ĐÃ VÁ THẬT** | Ca head/app/workflow/run mới nhất và các mutant tương ứng đạt; probe check khác kho, check mới hơn, run khác head/kho, job sai run/attempt đều rc12/nguyên byte. |
| M5 full_name; giữ checkpoint_day cũ | **Giữ ĐÃ VÁ THẬT** | Hai mutant chết đúng: accept rc0 thay12; oracle checkpoint thấy hash cũ khác hash sự kiện mới nhất. |

Chuỗi tái hiện thật của #969 trong [probes/trace.json](probes/trace.json), nhãn `reported-old` và `reported-candidate`:

```text
record-review approve trên A → approved_pending
mo-lai --nguyen-nhan ci-do, H/R trên A → rc0, running
begin-attempt; transition reviewing trên B (B != A)
record-review --verdict changes_requested --reviewed-sha B → rc0, running
mo-lai --nguyen-nhan connector, H/R vẫn trên A
    f8d71673480e55863639c59de3fbbe1ddc80b414: rc0 → cho_chu_kho (lỗi)
    be88cafd7bdaee556c0ec3e60b3cba0d22efbb7e: rc8, running, state nguyên byte
```

Lý do candidate: `mo-lai connector không chạy từ 'running' (đòi approved_pending của packet áp ADR-0054, hoặc running mở lại bằng ci-do cùng generation, chưa mở lượt mới)`. Quyền mo_lai_tu vẫn được giữ làm dữ liệu cho #816; cửa connector kiểm lịch sử kể từ sự kiện mo_lai cuối, nên giữ dữ liệu không đồng nghĩa còn dùng được quyền.

Đã đo thêm các nhánh sau, với trace lệnh/rc/head/hash state trước-sau:

| ngữ cảnh | kết quả |
|---|---|
| begin mới nhưng chưa vào review; begin/review mới vẫn cùng head | connector rc8/nguyên byte ở cả hai. |
| void từ running hoặc reviewing sau begin | void rc0; connector vẫn rc8/nguyên byte. |
| begin bị từ chối vì sai provider | rc4/nguyên byte, không ghi begin; connector muộn trên A vẫn rc0. |
| CI → connector → chu-kho-duyet cho_phep_va | rc0/0/0, mo_lai_tu=None; gọi connector lại từ running rc8. |
| CI trên A → review B approve | H cũ reviewed_sha=A bị rc11/nguyên byte; H/R đúng B được connector nhận rc0. |
| Sau approve B, CI mới trên B rồi connector | Quyền mới neo B; rc0/0. Begin tiếp rồi void vẫn không khôi phục quyền. |
| checkpoint_day A → review B approve → checkpoint_day B | Quyền mới thay hash và neo B; không dùng quyền A cho B. |
| CI → begin/review → hết budget → nâng trần/rescue → void | rescue về running; connector rc8 cả trước và sau void, state nguyên byte ở mỗi từ chối. |

Các nhánh này xác nhận điều kiện mới kiểm theo sự kiện begin, không theo số attempts_used có thể bị hoàn. Source scan còn kiểm đường transition và rescue không xóa lịch sử begin. [probes/results.json](probes/results.json), [rescue_probe_final/results.json](rescue_probe_final/results.json).

**Đối chiếu từng ca bắt buộc trong nghiệm thu.** Tất cả ca dưới PASS trên candidate. Các lỗi cột cuối đều là ngoại lệ `AssertionError` đo tại đúng ca trên mutant; “đòi/được” là mã CLI do oracle kiểm, không phải rc chung của runner.

| yêu cầu | ca r813 tương ứng | mutant | lỗi đo được / đúng lý do |
|---|---|---|---|
| Chạm trần mo-lai → blocked | `r813_cham_tran_mo_lai` | `r813_mo_lai_khong_xet` | AssertionError: bước 1: đòi3/được0 — bỏ xét trần |
| Hai comment ID cùng nguyên nhân, chung bộ đếm | `r813_cung_slug_hai_id` | `r813_dem_theo_id` | AssertionError: bước 4: đòi3/được0 — đếm theo ID bỏ lọt cùng slug |
| Hai nguyên nhân độc lập đếm riêng | `r813_hai_slug_doc_lap` | `r813_gop_nguyen_nhan` | AssertionError: bước 4: đòi0/được3; cùng finding-id gop×2 |
| Slug ngoài H bị từ chối | `r813_slug_ngoai_bien_nhan` | `r812_bo_slug_trong_bang` | AssertionError: bước 0: đòi11/được0 |
| begin-attempt khi đã chạm trần | `r813_begin_attempt_cham` | `r813_begin_khong_xet` | AssertionError: bước 2: đòi3/được0 |
| Cửa khép lượt không bị chặn | `r813_cua_khep_khong_chan` | `r813_chan_cua_khep` | AssertionError: bước 3: đòi0/được3; cùng finding-id ci-gate×1 |
| mo-lai không finding | `r813_khong_finding` | `r813_bo_tap_rong` | AssertionError: bước 0: đòi2/được0 |
| Connector tập con P0–P2 | `r813_connector_tap_con` | `r813_tap_con_lot` | AssertionError: bước 0: đòi11/được0 — tập con được nhận sai |
| CI đỏ + connector P1 cùng head | `r813_ci_va_p1_cung_head` | `r813_bo_ci_do` | AssertionError: bước 0: đòi12/được0 |
| Connector đến sau CI, vào từ running | `r813_connector_sau_ci` | `r813_chi_tu_approved` | AssertionError: bước 1: đòi0/được8; mo-lai không chạy từ running |
| CI đỏ trước khi connector xong | `r813_connector_sau_ci` | `r813_ci_do_doi_connector_xong` | AssertionError: bước 0: đòi0/được12; connector chưa xong |
| Connector sau CI thay quyền nguồn | `r813_connector_sau_ci` | `r813_quyen_mo_lai_giu_cu` | AssertionError: nội dung quyền sai: vẫn ci-do thay vì connector, cùng generation/SHA |
| Dùng quyền thay thế ở checkpoint | `r813_connector_sau_ci_roi_duyet` | `r813_quyen_mo_lai_giu_cu` | AssertionError: bước 2: đòi0/được8, state hỏng (mo-lai); oracle tuple hàng trước là bằng chứng chính |
| Checkpoint chỉ ở nhánh khác | `r813_checkpoint_nhanh_khac` | `r813_checkpoint_ref_tuy_y` | AssertionError: bước 1: đòi7/được0 |
| Checkpoint packet khác | `r813_checkpoint_packet_khac` | `r813_bo_packet_checkpoint` | AssertionError: bước 1: đòi7/được0 |
| Không dùng cho_phep_va làm quyền đẩy | `r813_va_lam_quyen_day` | `r813_moi_pham_vi_la_du` | AssertionError: bước 0: đòi7/được0 |
| M5 run mới in_progress thiếu repository | `r813_m5_run_moi_thieu_repository` | `r813_m5_bo_repository` | AssertionError: r834 accept: đòi12/được0 |
| M5 path sai kiểu | `r813_m5_run_path_sai_kieu` | `r813_m5_bo_path` | AssertionError: r834 accept: đòi12/được0 |
| M5 head_sha sai kiểu | `r813_m5_run_head_sai_kieu` | `r813_m5_bo_head_sha` | AssertionError: r834 accept: đòi12/được0 |
| M5 full_name sai kiểu | `r813_m5_run_full_name_sai_kieu` | `r813_m5_bo_full_name` | AssertionError: r834 accept: đòi12/được0 |
| Finding connector lượt 6: begin mới vô hiệu quyền cũ | `r813_quyen_ci_sau_luot_moi` | `r813_quyen_ci_qua_luot_moi` | AssertionError: bước 3: đòi8/được0 |

Đối chứng M5: **63/63 ca r834 hiện có PASS**. Các ca M5 dựng nền accept đầy đủ rồi thêm run sai kiểu; lỗi trên candidate là RC_GATE=12, có lý do KHÔNG ĐO ĐƯỢC, state nguyên byte. Tập audit gồm **37 mutant r813 + 4 mutant dùng chung có target r813 + 2 mutant r834 đổi mỏ neo = 43 mutant / 48 target GIET / 129 đối chứng PASS**. Toàn bộ ngoại lệ và thông điệp không cắt ở [MUTATION_AUDIT.md](MUTATION_AUDIT.md), [mutants/results.json](mutants/results.json). Không có traceback/CLI sập được tính là kill.

Đã đọc chon.py và dotbien.py trước khi dùng logic. Runner riêng [run_review.py](run_review.py) tái dùng chay_suite, phân loại kill và đối chứng của main; thêm kiểm tên ca không rỗng/không trùng, target tồn tại, neo duy nhất và lưu thông điệp đầy đủ. Không suy pass từ rc0 của tập chọn rỗng. Mutant reviewer chạy toàn bộ 106 ca r813+r834 để tìm chốt không được bảo vệ, rồi chạy oracle riêng và đối chứng A/B.

**Bất biến I1–I11 và M1/M2/M3/M5.**

| bất biến/mục tiêu | kết luận và bằng chứng trong phạm vi |
|---|---|
| I1, I2 / M2, M3 | mo-lai dùng biên nhận H qua _du_dieu_kien_approve; rời cho_chu_kho dùng checkpoint Đ trên master đo bằng fetch/ls-remote. Lease H/Đ/R không đổi, r812 hồi quy đạt. R do caller cung cấp chỉ được kiểm nhất quán, không tự trở thành authority. |
| I3 | Finding khác rỗng; refs đúng dạng/không lặp; connector phải bằng đúng P0–P2. Các probe rỗng/null/số/phần tử sai/mixed/trùng/thừa đều bị từ chối. CI nhận failure/timed_out/startup_failure; success/cancelled/neutral/skipped/action_required/stale/null/unknown đều rc12. |
| I4 | Ca âm r813/r834 và các probe kiểm từng byte state. Đầu vào hỏng bị từ chối trước ghi; checkpoint hợp lệ ở trần ghi sổ rồi blocked. _load tái dựng finding_counts từ reviews và history.mo_lai, không đếm đôi record_review trong history. |
| I5 / M1 | CUA_DI_TIEP dùng chung _xet_dung cho begin-attempt/mo-lai/chu-kho-duyet. Mutant gọi sớm bị bắt. Checkpoint sai packet/phạm vi/kiểu generation/neo tại trần vẫn rc7/nguyên byte; checkpoint hợp lệ ở cùng trần rc3/blocked. Cửa khép record-review vẫn ghi kết quả. |
| I6 | Quyền mo_lai_tu mới thay quyền cũ; connector muộn phải chưa có begin từ mo_lai cuối. Void và rescue không xóa dấu begin. cho_phep_va tiêu thụ mo_lai_tu; checkpoint_day thay theo hiện vật mới, neo generation/head; cùng hash/phạm vi không tái sử dụng. Việc tiêu thụ tại cửa đẩy thuộc #816, chưa được suy là đã làm. |
| I7 | Head lấy từ state (pending_sha hoặc SHA nguồn của ci-do), không từ cờ caller. Readback neo repo/PR/head, đủ trang theo tập ID riêng từng endpoint. CI lọc run đúng kho/head/workflow, chọn run/attempt/job/check mới nhất và app github-actions. Probe sai ngữ cảnh bị chặn; không so đồng hồ hay chéo không gian ID. |
| I8 | Tái dùng validator canon và các hàm chuẩn hóa danh tính của #812; không thêm phép so provider riêng. Hồi quy r812 xác nhận các cửa identity trong tập được chọn. |
| I9 | accept không truyền p0p2: vẫn đòi connector xong và không P0–P2. 63 r834 + 148 r812 + 2 codepage PASS. State cũ thiếu mo_lai_tu/checkpoint_day được _load đọc qua get; đường record-lease cũ giữ luật cũ. |
| I10 | H ở mo-lai có vai trò reviewer, verdict changes_requested và đủ tuple packet/generation/reviewed_sha/spec_hash; 6 probe đổi riêng trường bị rc11/nguyên byte. H cũ A bị từ chối sau approve B. Checkpoint đo đúng tuple/phạm vi/người quyết; không dùng cho_phep_va làm quyền đẩy. |
| I11 | Slug chỉ lấy từ bảng lớp H đã xác thực và CLI phải khai đủ bảng; cùng slug qua ID khác cộng chung, nguyên nhân khác đếm riêng. |
| M5 | Kiểm kiểu path/head_sha/repository/full_name của mọi run trước lọc. Bốn ca âm và bốn mutant tương ứng đo đúng chốt; không có thay đổi hợp đồng accept ngoài việc chặn dữ liệu run hỏng mà đặc tả yêu cầu. |

Checkpoint chỉ đọc blob ở OID đã fetch và so ls-remote, không đọc HEAD cục bộ. Hai probe mô phỏng fetch lỗi và remote đổi sau fetch đều rc7/nguyên byte; wrapper git chỉ dùng trong fixture dưới OUT. Không suy phép mô phỏng thành kiểm race mạng thật. [checkpoint_probes/results.json](checkpoint_probes/results.json).

**Lệnh đã chạy, rc và bằng chứng dương.** Môi trường: PYTHONDONTWRITEBYTECODE=1; TMPDIR=OUT/tmp; GIT_CONFIG_GLOBAL=/dev/null; GIT_CONFIG_SYSTEM=/dev/null; GIT_OPTIONAL_LOCKS=0; GIT_ALLOW_PROTOCOL=file. Copy có core.abbrev=7. Mọi script, mutant, fixture và output do reviewer tạo nằm dưới OUT. Các fetch/push/ls-remote trong fixture chỉ trỏ repo bare cục bộ; không mạng/GitHub, không push ref kho được review.

| command | rc | bằng chứng / artifact |
|---|---:|---|
| `python -B out/bootstrap.py` | 0 | Hash, ancestry, exact head/tree/ref, diff; IDENTITY.json, FULL.diff, FIX.diff. |
| `python -B -W ignore out/run_review.py baseline_r813_r834 r813_,r834_` | 0 | 106/106 PASS (43+63); baseline_r813_r834/results.json, summary.json, log cùng tên tại OUT. |
| `python -B -W ignore out/run_review.py baseline_r812 r812_,stdout_cp` | 0 | 150/150 PASS (148+2); baseline_r812/results.json, summary.json, log. |
| `python -B -W ignore out/run_review.py mutants` | 0 | 43/43 mutant, 48 target GIET, 129 đối chứng PASS; mutants/results.json, summary.json, mutants.log. |
| `python -B -W ignore out/run_review.py gates` | 0 | doctrine-scan rc0: 10 tệp/0 chỗ chép; adr-song rc0: 55/55, ngoại lệ 0016 khai sẵn; gates/results.json. |
| `python -B -W ignore out/probes.py` | 1 do runner reviewer | 84 bước CLI trước lỗi đúng kỳ vọng; probes/results.json và trace.json. Lỗi riêng script truyền pham_vi hai lần, không phải CLI sản phẩm; nhóm bị gián đoạn được chạy hoàn chỉnh ở hàng sau. |
| `python -B -W ignore out/checkpoint_probes.py` | 0 | 14/14 bước, gồm toàn bộ 5 kịch bản checkpoint đã định và 2 lỗi Git mô phỏng; checkpoint_probes/results.json. |
| `python -B -W ignore out/rescue_probe.py` | 1 lần đầu; 0 sau sửa oracle | Lần đầu đòi chữ thường rescue trong thông điệp Rescue; mã/state sản phẩm đúng. Sửa literal, chạy lại chuỗi: 7/7 bước đúng; rescue_probe_final/results.json. |
| `python -B -W ignore out/extra_mutations.py` | 0 | Hai mutant, mỗi mutant sống 106/106; mỗi A/B đúng rc/state và oracle giết đúng; tổng 12 đối chứng PASS; extra_mutations/summary.json, observations.json. |
| `python -B out/finalize.py` | 0 | Đối chiếu inventory/kết quả, snapshot source, Git exact head/tree/ref và trạng thái sạch; SOURCE_INTEGRITY.json, ARTIFACTS.json. |

**256/256** là tổng nền chọn lọc, không phải N/N toàn repository. `r812_r4_own_parent` bị loại trước chạy vì ca soạn nội dung đường dẫn chứa thành phần cha; không tính vào 256 và không gọi là pass. Hai lỗi runner reviewer được giữ nguyên log, không gán cho sản phẩm và không tính tín dụng đột biến. Các sửa runner không sửa code/test candidate. 84+14+7 bước probe là kết quả từng chuỗi được ghi rõ, có một số đối chứng lặp, không cộng thành số ca suite độc lập.

**Giới hạn và toàn vẹn.** not_run: full suite `python .claude/dev/packet_loop_test.py` (~45–60 phút, assignment ưu tiên chọn lọc), mutant ngoài tập đã nêu, CI online/thu-hoi, Windows thật, bare Ruff lint và Ruff pin/probe contract. Không nhận lời khai gate executor làm kết quả độc lập. Hai ca codepage chạy trên Linux không chứng minh Windows thật.

Hướng thử cần nội dung đường dẫn thoát cây chỉ mô tả bằng lời theo assignment: receipt/checkpoint hoặc liên kết trỏ ra ngoài phạm vi cần bị từ chối trước đọc/ghi ngoài cây, giữ state nguyên byte. Không tự soạn payload đó. Nợ #834 required-mutation-coverage-missing ngoài M5 không được mở lại hoặc khai đã đóng. Quyền tiêu thụ ở cửa đẩy #816 chưa được kiểm vì ngoài phạm vi.

Snapshot source đầu/cuối bao gồm tracked/untracked/ignored và .git: **7004 → 7004 tệp, 0 delta byte/mode**. HEAD/tree/ref, worktree/index của SRC và copy đều đúng/sạch. Đây là so sánh hai mốc, không phải giám sát mọi lần ghi trong lịch sử. Sandbox thực tế workspace-write; source được đối xử read-only. [SOURCE_INTEGRITY.json](SOURCE_INTEGRITY.json) giữ số đo; [ARTIFACTS.json](ARTIFACTS.json) băm report/scripts/logs/results, không gồm toàn bộ fixture/copy.
