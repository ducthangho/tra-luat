Verdict: request_changes
Reviewed commit: 4adbf92cba01c8ef186dce90c649c8a65df4d8ae
Spec sha256: 39b4288959f3889c6c3aad2d24b355c1c02b1462a8854c6a5b00677e81a7ce73; Chung sha256: 4e3d1e1b3f6a0b60b96ad7b70f0ece97eca4bb3d6d10defeab1cd24ac6d1cbf0

**Kết luận lượt 2: 2 lớp P2, 1 lớp P3; 0 P0/P1.** Chưa đạt ngưỡng approve. Một lớp P2 lượt trước vẫn sống ở cửa `mo-lai`; một lỗi P2 mới nằm ở dữ liệu P3 từ phiên bản trước #814. Hai biểu hiện P3 cũ đã được khóa bằng test; hai mutant mới cho thấy nợ độ phủ cùng lớp còn mở. Verdict chỉ neo commit dòng 2, không cấp quyền push, merge, land hoặc kích hoạt ADR-0054.

| slug | hạng P0–P3 | biểu hiện file:dòng | phép đo/tái hiện đã chạy | hướng vá |
|---|---|---|---|---|
| `finding-lineage-counter-reset` | **P2 — giữ slug cũ, còn sống** | `.claude/dev/packet_loop.py:2971`, `:2994`; chốt nối P0–P2 chỉ nằm ở `:3073` | `p2-ci-map`: P2 a-b đã đếm1 → approve sạch → ci-do H P2 c-b, bảng nối a-b→c-b khai cùng nguyên nhân ⇒ rc0/running, counts a-b:1+c-b:1. `connector-lineage-map` cũng rc0/cho_chu_kho. Đối chứng giữ a-b ở từng cửa đều rc3/blocked a-b:2. | Áp bất biến lineage ở mọi cửa nhận bảng lớp H. Với cơ chế cấm nối P0–P2 đã chọn, từ chối bảng ấy trước xét dừng/ghi ở mo-lai; nếu hỗ trợ nối thì chuẩn hóa cả bộ đếm và lịch sử. |
| `legacy-p3-failure-counts-retained` | **P2 mới — lỗi hành vi** | `.claude/dev/packet_loop.py:672`, `:1206`, `:1228`, `:3116` | `legacy-base-counts`: state do **product base thật** tạo, approve a-x:P3 có finding-id a-x → candidate vua-p3 → lần P2 đầu của a-x ⇒ rc3/blocked count2. State tương đương do candidate tạo ⇒ rc0/running count1. | Chuyển đổi lịch sử cũ có đủ bằng chứng H: loại lần P3 khỏi sổ đếm và counts đồng bộ, giữ audit. Không xóa lượt P0–P2 có thật của cùng slug, không suy hạng khi thiếu bằng chứng. |
| `r814-mutation-evidence-incomplete` | **P3 — biểu hiện cũ đóng, hai biểu hiện độ phủ mới** | `.claude/dev/packet_loop_test.py:9085`, `:9107`; chốt sản phẩm `.claude/dev/packet_loop.py:3073` | Gỡ riêng kiểm hạng nguồn hoặc riêng kiểm hạng đích; từng mutant sống toàn bộ tập chọn. A/B riêng: candidate từ chối rc11/nguyên byte; mutant nhận rc0 và bị oracle AssertionError bắt. Số liệu đầy đủ bên dưới. | Owner: executor Claude Packet #814. Thêm riêng ca P2→P3 và P3→P2 có bảng nối, mỗi ca giữ vế hạng còn lại hợp lệ; thêm hai mutant độc lập. |

**Lý do phân hạng.** Lớp đầu vẫn làm bộ đếm cùng nguyên nhân bị tách, là lỗi sản phẩm thực và giữ stable slug lượt 1. Lớp thứ hai có phản chứng sản phẩm thật trên state hợp lệ do base tạo; không phải suy luận từ mutant sống. Lớp độ phủ chỉ có mutant **mới** sống, còn candidate xử lý đúng trong A/B, nên **P3**, không nâng P2. Không có mutant đã báo lượt 1 còn sống được gán thành nợ P3 mới. Hai biểu hiện `mo-lai ci-do` và `connector` của lớp đầu chỉ tính **một** nguyên nhân.

**ĐỐI CHIẾU LƯỢT TRƯỚC — đo lại từng lớp.**

| lớp lượt 1 | trạng thái lượt 2 | phản chứng tương đương và bằng chứng |
|---|---|---|
| `p3-mapping-namespace-collision` | **ĐÃ VÁ THẬT** | `rename-chain` {a,b}→{b,c}, a→b/b→c: rc11/“trỏ slug”, state nguyên byte. Đối chứng đổi sang hai tên rời nguồn rc3 với 2→2. Ca `r814_noi_chuoi` đạt; mutant `r814_noi_chuoi_lot` chết đúng. |
| `finding-lineage-counter-reset` | **VÁ HỜ ở cấp lớp: đã vá record-review, còn sống ở mo-lai** | `p2-rename` offline rc11/nguyên byte; giữ a-b rc3/count2. Nhưng hai cửa ci-do/connector còn nhận H nối P2 và tạo hai khóa đếm1 như bảng finding. |
| `p3-reopen-enters-failure-counter` | **ĐÃ VÁ THẬT** với sự kiện mới | `ci-P3` tại same_failure_limit=1: rc0/running, counts={}, history.mo_lai.finding_ids=[]. `ci-P2`: rc3/blocked/count1. Cả hai reload status rc0. Mutant bỏ lọc P3 chết ở oracle counts. Lỗi lịch sử cũ được tách thành slug mới vì cần migration, không phải lỗi cộng sự kiện mo-lai mới. |
| `legacy-p3-milestone-lost` | **ĐÃ VÁ THẬT** cho phản chứng đã báo | `legacy-base-milestone` dựng approve P3 bằng blob base, xác nhận review chưa có lop; đổi CLI sang candidate → vua-p3 → P3 không giảm: rc3, vong_p3={k:1,truoc:1,sau:1}. Đối chứng state mới giống kết quả. Lỗi mới về counts cũ không phủ nhận việc mốc đã được giữ. |
| `receipt-map-validation-skipped` | **ĐÃ VÁ THẬT** với lỗi lược đồ lượt 1 | Cùng bang_noi là object sai kiểu: record-review rc11; `ci-invalid-map` và `accept-invalid-map` đều rc11/“bang-noi”, state nguyên byte; không có trường ấy ở đối chứng thì rc0. Việc bỏ qua ngữ nghĩa nối P2 ở mo-lai được theo dõi **một lần** trong `finding-lineage-counter-reset`. |
| `new-command-codepage-matrix-incomplete` | **ĐÃ VÁ THẬT** | `stdout_cp1252`, `stdout_cp1258` đều PASS. Đọc ma trận mới: dựng H P3 thật, chạy vua-p3 thành công, đòi rc0 và stdout khác rỗng rồi mới thêm tên vào tập đã phủ. Không chứng minh Windows thật. |
| `r814-mutation-evidence-incomplete` | **Hai biểu hiện cũ ĐÃ VÁ THẬT; có hai biểu hiện mới P3** | `replace-ci-right`: approve A→ci-do A→review B P3→vua-p3 thay quyền thành (p3,1,B), B≠A; mutant giữ cũ bị oracle tuple bắt. `duplicate-source`: rc11/“bang-noi”/nguyên byte; mutant nguồn lặp bị ca mới bắt. Hai thiếu sót mới chỉ liên quan kiểm hạng nguồn/đích độc lập. |

**Chi tiết hai lỗi hành vi.**

1. `finding-lineage-counter-reset` — M1/I11 và same_failure_limit.

Phản chứng offline lượt 1 đã được đóng, nhưng `_vong_p3` chỉ chạy trong `cmd_record_review`. `cmd_mo_lai` dùng `_du_dieu_kien_approve`, nơi chỉ kiểm hình dạng bang_noi, sau đó bỏ qua `bn["noi"]` và tăng counts theo slug mới. Trường lý do trong H công khai khẳng định cùng nguyên nhân; đây không phải giả định reviewer âm thầm đổi tên.

```text
record-review changes_requested: a-b:P2 → running, {a-b:1}
review kế tiếp approve sạch             → approved_pending, {a-b:1}
mo-lai ci-do, H c-b:P2, bang_noi a-b→c-b, ly_do="same cause"
  candidate: rc0/running, {a-b:1,c-b:1}
  đối chứng cùng a-b, không đổi tên: rc3/blocked, {a-b:2}
mo-lai connector với cùng phép đổi tên, trên fixture độc lập
  candidate: rc0/cho_chu_kho, {a-b:1,c-b:1}
  đối chứng cùng a-b: rc3/blocked, {a-b:2}
```

Nguồn a-b không phải lớp P3 vòng trước, đích c-b cũng là P2. Theo cơ chế executor đã chọn, biên nhận phải bị từ chối trước ghi; nó không được âm thầm bỏ bảng nối rồi coi đây là nguyên nhân mới. Bất biến I11 bao gồm offline và connector, nên đóng riêng ca offline chưa đóng lớp. Trên mọi state cuối của cặp thử, `status` rc0: lỗi không đến từ state hỏng hoặc fixture giả lập bộ đếm.

Hướng sửa: tách kiểm hình dạng và kiểm ngữ nghĩa theo đúng vai trò H; áp giới hạn hạng/nguồn ở mọi nơi tiêu thụ bảng nối, bảo toàn I4. Không gọi nguyên `_vong_p3` từ mo-lai/accept vì sẽ vô tình tính thêm vòng offline. Nếu chọn hỗ trợ nối P0–P2 thay vì từ chối, phải bảo toàn lineage xuyên nguồn và cách `_load` tái dựng counts. Phép đóng lớp cần cả hai chuỗi ở trên, đối chứng cùng slug, và reload state. [Script](probes.py), [CI results](probes/results.json), [connector script](additional_probes.py), [connector results](additional_probes/results.json).

2. `legacy-p3-failure-counts-retained` — M2, tương thích state ADR-0054 đã có.

Dùng chính blob `.claude/dev/packet_loop.py` tại base `20a2e2b` để tạo state qua CLI; không chèn tay counts/history. Lệnh approve có bảng lớp `a-x:P3` và `--finding-id a-x` là đầu vào hợp lệ của base. Base lưu `reviews[0].finding_ids=['a-x']`, `finding_counts={'a-x':1}`, đồng thời `bien_nhan_approve.lop` chứng minh hạng P3. Sau nâng CLI lên candidate, vua-p3 rc0; lần review đầu tiên nâng **cùng slug** lên P2 bị chặn vì count2. Review P3 trước đó đã bị tính vào same_failure_limit. Với chính đầu vào khởi tạo đó trên candidate, review đầu không vào counts và lần P2 chỉ có count1/rc0/running.

Ở hai vế, vong_p3 cuối đều là `{k:1,truoc:1,sau:0}`; vì vậy rc3 của vế nâng cấp thực sự do **same-failure**, không phải vòng P3 hay quota. Bản vá khôi phục `lop` tạm thời trong `_vong_p3` chỉ giữ mốc; nó không chuyển đổi finding_ids/counts cũ. Đây là nguyên nhân khác với “mất mốc”, nên dùng slug mới. Không yêu cầu áp luật mới lên packet non-ADR.

Hướng sửa cần phân biệt lịch sử P3 có bằng chứng với lịch sử P0–P2: loại lượt P3 có thể xác minh, giữ lượt nghiêm trọng có thật và audit gốc; cập nhật cách tái dựng counts cùng sổ, không chỉ xóa khóa counts (sẽ bị `_load` từ chối). Migration không ghi state trước khi đầu vào lệnh được kiểm, để giữ I4. Ca cần bao gồm approve P3 cũ có finding-id, cùng slug P2 về sau, đối chứng state mới, và reload. [Base product](base-product/packet_loop.py), [probes.py](probes.py), [state/rc đầy đủ](probes/results.json).

**Độ phủ mới P3.** `r814_noi_lop_p2` kiểm một bảng nối có **cả nguồn lẫn đích đều P2**; mutant khai báo `r814_noi_moi_hang` nới cả hai điều kiện cùng lúc. Gỡ chỉ một vế thì vế còn lại vẫn từ chối, nên ca hiện tại không phân biệt được việc mất từng chốt. Reviewer tạo hai mutant riêng:

- `source-rank`: đổi `cu.get(s) == "P3" and s not in nay` thành `s in cu and s not in nay`; probe H nối P2→P3.
- `destination-rank`: đổi `all(nay.get(s) == "P3" for s in den)` thành `all(s in nay for s in den)`; probe H nối P3→P2.

Mỗi A/B chỉ đổi một predicate, fixture dương đầy đủ, H/schema/nguồn/đích và lý do đều hợp lệ trừ hạng đang kiểm. Candidate rc11/“trỏ slug không có” và nguyên byte. Mutant rc0 (approved_pending ở vế nguồn, running ở vế đích), oracle riêng ném AssertionError. Owner executor Claude #814; thêm hai ca và mutant độc lập, giữ chốt sản phẩm hiện đang đúng. Script và cặp neo/thay là dữ liệu phản chứng dưới OUT, không phải patch giao áp lên SRC. [extra_mutations.py](extra_mutations.py), [source-rank](extra_mutations/source-rank/summary.json), [destination-rank](extra_mutations/destination-rank/summary.json).

**Từng ca nghiệm thu và mutant khai báo.** 25/25 ca r814 PASS. 26 mutant có target r814 được đo theo logic main mục3: **29 target GIET, 78 đối chứng khác họ PASS**, không tín dụng giả/skip. Mọi ngoại lệ target là **AssertionError**, không traceback/CLI sập. Bảng ghi rc đòi/được của CLI, trừ oracle counts và quyền đã nêu rõ. Toàn văn lỗi trong [MUTATION_AUDIT.md](MUTATION_AUDIT.md), [mutants/results.json](mutants/results.json).

| ca bắt buộc / bổ sung | ca r814 | mutant | lỗi đúng lý do |
|---|---|---|---|
| {A,B}→{B} hợp lệ | r814_ab_b_hop_le | r814_giam_hai_lop | đòi0/được3, siết sai mức giảm2→1 |
| biểu hiện trùng 2→2 | r814_bieu_hien_trung | r814_khong_giam_van_qua | đòi3/được0 |
| đổi tên thiếu bảng nối | r814_doi_ten_khong_noi | r814_doi_ten_tu_do | đòi11/được0 |
| gộp thuần, sau nối1→1 | r814_gop_qua_noi | r814_noi_chi_vong_nay | đòi3/được0 |
| mốc→vòng1 không giảm | r814_moc_vong1_khong_giam | r814_vong1_mien_so | đòi3/được0 |
| vòng3 | r814_vong_3 | r814_vong_3_lot | bước6 đòi3/được0 |
| P3 không vào same-failure | r814_p3_khong_dem | r814_p3_vao_dem | counts đòi{}, được a-b:1 |
| P2 vẫn đếm | r814_p2_van_dem | r814_bo_ca_p2 | counts đòi a-b:1, được{} |
| tự chọn vá, quyền tuple | r814_vua_p3_di_duoc | r814_vua_khong_ghi_quyen | quyền thiếu, phải (p3,1,pending_sha) |
| tập chọn rỗng | r814_vua_p3_rong | r814_vua_tap_rong | đòi2/được0 |
| slug ngoài H | r814_vua_p3_ngoai_bien_nhan | r814_vua_ngoai_bien_nhan | đòi11/được0 |
| xóa hết P3 | r814_xoa_het_p3 | r814_rong_la_khong_giam | đòi0/được3; tập finding còn mở được phép rỗng |
| changes_requested sai generation | r814_am_generation_khac | r812_bo_generation | đòi11/được0; hai target r812/r834 dùng chung cũng chết đúng |
| M4 mixed check_refs | r814_check_refs_tron_null | r814_refs_bo_do_dai | đòi11/được0 |
| M4 CI→begin→void→connector | r814_ci_void_connector | r814_void_khoi_phuc_quyen_ci; r813_quyen_ci_qua_luot_moi | cả hai: bước3 đòi8/được0 |
| sai lược đồ bảng nối | r814_noi_sai_luoc_do | r814_noi_bo_ly_do | đòi11/được3; lọt kiểm input, tới chốt vòng |
| nguồn không có | r814_noi_tro_slug_khong_co | r814_noi_bo_nguon | đòi11/được0 |
| vua-p3 xét dừng | r814_vua_p3_xet_dung | r814_vua_khong_xet | đòi3/được0 |
| nối chuỗi | r814_noi_chuoi | r814_noi_chuoi_lot | đòi11/được0 |
| nối cả hai đầu P2 | r814_noi_lop_p2 | r814_noi_moi_hang | đòi11/được0 |
| nguồn lặp | r814_noi_nguon_lap | r814_noi_nguon_lap_lot | đòi11/được0 |
| schema nối ở mo-lai | r814_mo_lai_noi_hong | r814_noi_chi_record_review | đòi11/được0 |
| mo-lai P3 miễn đếm | r814_mo_lai_p3_khong_dem | r814_mo_lai_dem_p3 | counts đòi{}, được ci-gate:1 |
| state cũ giữ mốc | r814_state_cu_giu_moc | r814_state_cu_mat_moc | đòi3/được0 |
| p3 thay quyền ci-do | r814_vua_thay_quyen_ci | r814_vua_giu_quyen_cu | oracle tuple thấy (ci-do,1,A), phải (p3,1,B), A≠B |

M4 đóng đúng cả hai biểu hiện nợ `r813-mutation-evidence-incomplete` từ handoff và verdict #813 lượt6: mixed refs bị rc11/“đúng dạng”/nguyên byte; chuỗi void bị rc8/“chưa mở lượt mới”/nguyên byte. Chốt (b) là kiểm **không có begin_attempt sau mo_lai cuối** tại dòng2964; void không xóa dấu begin. Mutant đúng chốt làm ca đỏ; không gán đây là nợ P3 còn lại của #814.

**Bất biến I1–I11 và nhánh biên.**

| bất biến / mục tiêu | kết luận trong phạm vi |
|---|---|
| I1/I2/I8/I10 | Đường lease/authority/canon không đổi trong diff; hồi quy r812 kiểm H/Đ/R và chuẩn hóa. vua-p3 lấy lớp từ H pending đã lưu, neo generation/pending_sha. Receipt âm sai generation bị rc11. Không đo lease/comment/check online. |
| I3/M1 | Schema bang_noi được kiểm ở vị từ H chung, từ chối object/rỗng lý do/nguồn lặp; kiểm tham chiếu ở record-review ngăn chain và P2 nối. Ngữ nghĩa nối chưa áp đủ ở mo-lai, là finding còn sống. |
| I4 | Probe vua-p3 rỗng/ngoài H tại ngưỡng same-failure vẫn rc2/11 và nguyên byte; map lỗi rc11 trước ghi. Vòng không giảm/vòng3 ghi reviews, đóng attempt, tăng rounds, tiêu thụ call rồi blocked_vong_p3. status đọc lại được. |
| I5/M3 | vua-p3 gọi cùng _xet_dung, có trong CUA_DI_TIEP; mutant bỏ đăng ký bị bắt. Cửa khép review vẫn ghi kết quả. Không thêm cơ chế xét dừng song song. |
| I6 | Quyền p3 thay ci-do trên head cũ, đúng nguyên nhân/generation/head; gọi connector từ running mang quyền p3 bị rc8/nguyên byte. chu-kho-duyet tiêu thụ quyền connector như cũ. Việc tiêu thụ tại cửa đẩy thuộc #816. |
| I7 | Hồi quy r813/r834 và M4 giữ checks theo kho/head/app/workflow/job, run/attempt mới nhất và refs đúng dạng. Đo trên fixture bare cục bộ; không kiểm CI thật. |
| I9 | Non-ADR vẫn đi nhánh dem=ids; ca r812/r813/r834 chọn an toàn và hai codepage đạt. State ADR cũ giữ mốc nhưng vẫn mang counts P3 cũ: finding mới. Không tuyên bố N/N toàn repository. |
| I11/M1/M2 | Chuỗi đổi tên P3 mơ hồ bị chặn; gộp so sau nối ở cả hai vòng. P2 giữ slug ở record-review, nhưng đổi qua H mo-lai vẫn né đếm. P3 mới được loại khỏi cả review và mo_lai.finding_ids; _load tái dựng nhất quán trên state mới. |
| M2: verdict âm toàn-P3 | `negative-p3-repeat` rc3/2→2; `negative-p3-reduce` rc0/running/2→1, counts{}. Không giới hạn mốc vào verdict approve. |
| M2: sự kiện xen | vua-p3→begin→void→review không giảm vẫn rc3; connector→chu-kho-duyet→review tạo mốc mới theo cơ chế công bố vì có mo_lai. Vòng2 xóa hết còn rc0 với k2/1→0. |
| M4 | Hai ca nợ #813 và các mutant đúng chốt đạt, không sửa mã sản phẩm M4 trong diff. |

`tu:[]` khai lớp mới C đồng thời reviewer khai A/B đã hết được nhận 2→1; đổi cùng slug P3 lên P2 được ghi1→0 nhưng state là running/changes_requested. Theo mô hình H và I11, reviewer chịu trách nhiệm phân lớp/hạng và việc lỗi cũ đã được sửa; máy không có oracle để chứng minh H nói sai về mã. Không tự sinh finding chỉ vì nhận các đầu vào ấy. Ngược lại, bảng nối trong phản chứng P2 **khai rõ cùng nguyên nhân**, nên việc đếm thành hai nguyên nhân là lỗi có bằng chứng ngay từ H.

**Định danh, phạm vi và bằng chứng lệnh.** Reviewer độc lập Codex/OpenAI, họ openai; executor Claude theo lease bản chép, họ claude; packet #814 revision3 generation2, sensitive, assurance_target cross_approved. Có shell Linux/công cụ cục bộ, transport machine. Exact serving model/effort/session và attestation launcher codex_cli không được đo độc lập trong phiên; không tự tạo receipt assurance hay suy model từ actor GitHub. Không kế thừa context executor; verdict trước chỉ dùng làm lịch sử finding.

Đã đọc toàn bộ prompt.snapshot. Theo chỉ thị trực tiếp, mọi đường tương đối lấy từ cwd, không từ thư mục runs. SRC luôn được đối xử read-only. Đã đọc **mọi hunk** của diff base→head và diff 335e746→head, gồm cả hai tệp product/test; xem [FULL.diff](FULL.diff), [FIX.diff](FIX.diff). Đọc tiếp các đường load/save, review, begin/void, H/canon, mo-lai, accept, checkpoint, xét dừng và parser. Base lease09db703 là mốc lịch sử, không bị nhầm với base review20a2e2b. Handoff trong lease chỉ dành nhánh lease; PR vẫn chỉ hai tệp.

HEAD đúng dòng2; tree `badd0845dbc7e1e41b957295f0389591b0e259ea`; origin/master=`20a2e2b3dd52a83442c739d17db1f1bd66181a6c`; clone thường, .git là thư mục, không nông, detached. Ba SHA256 (đặc tả con, chung, verdict lượt1) khớp, gồm verdict lượt1 `8ca0f12346366fd9efde9a445923d2c7e7bfc98358fb2a1a05989de6bc62aea2`. Ancestry rc0; diff-check rc0; product+78/−5, test+101/−6: **179 dòng thêm, 2 đường dẫn**, dưới trần450. [IDENTITY.json](IDENTITY.json).

Môi trường thử: PYTHONDONTWRITEBYTECODE=1, TMPDIR=out/tmp, GIT_CONFIG_GLOBAL=/dev/null, GIT_CONFIG_SYSTEM=/dev/null, GIT_OPTIONAL_LOCKS=0, GIT_ALLOW_PROTOCOL=file; copy core.abbrev=7. Các fetch/push/ls-remote do fixture dùng chỉ trỏ kho bare riêng dưới OUT; không mạng/GitHub, không push ref của SRC hay remote thật. Runner đã đọc `tham-chieu/chon.py`, tái dùng chay_suite và logic mutant/control/false-credit của main mục3, kiểm tên ca không trùng, tập chọn không rỗng, target tồn tại và neo thay duy nhất; giữ toàn văn lỗi, không dùng riêng rc runner làm tín dụng.

| command | rc | bằng chứng dương / kết quả |
|---|---:|---|
| `python -B out/bootstrap.py` | 0 | Ba hash khớp, ancestry, detached/không nông, exact head/tree/ref, diff đúng write set; IDENTITY.json. |
| `python -B -W ignore out/run_review.py baseline_r814 '^r814_'` | 0 | **25/25 PASS**; baseline_r814/results.json. |
| `python -B -W ignore out/run_review.py baseline_regression '^r81[23]_|^r834_|^stdout_cp'` | 0 | **256/256 PASS**: r812=148, r813=43, r834=63, stdout=2. Bỏ riêng ca đường dẫn bị cấm trước chạy. |
| `python -B -W ignore out/run_review.py mutants` | 0 | **26/26**, 29 target GIET, 78 đối chứng PASS, 0 tín dụng giả. |
| `python -B -W ignore out/run_review.py gates` (đã sửa entrypoint runner) | 0 | packet_loop.py doctrine-scan rc0: 10 tệp/0 chỗ chép; adr-song rc0: 55/55 ADR, ngoại lệ0016 có sẵn. |
| Lần gates đầu dùng nhầm scripts/tl.py | 1 runner; 2 mỗi CLI | Lỗi cú pháp entrypoint của **runner reviewer**, không phải gate sản phẩm. Giữ log và wrong-entrypoint-results.json, không tính PASS/kill. |
| `python -B -W ignore out/probes.py` | 0 | **24 kịch bản, 307 bước CLI có trace**, hoàn tất; các rc sai đặc tả được báo thành finding, không gọi là PASS chỉ vì runner rc0. |
| `python -B -W ignore out/additional_probes.py` | 0 | **6 kịch bản, 90 bước CLI**, gồm connector lineage, input trước xét dừng và vòng2 sạch. |
| `python -B -W ignore out/extra_mutations.py source-rank` | 0 | Mutant sống **281/281**; candidate oracle PASS, mutant bị AssertionError riêng; 3 đối chứng khác họ PASS. |
| `python -B -W ignore out/extra_mutations.py destination-rank` | 0 | Mutant sống **281/281**; candidate oracle PASS, mutant bị AssertionError riêng; 3 đối chứng khác họ PASS. |
| `python -B out/finalize.py` | 0 | Snapshot SRC không đổi, exact head/tree/ref/worktree/index sạch; băm hiện vật kết quả. |

Tổng nền chọn lọc **281/281 PASS**, không phải N/N toàn repository. Hai mutant mới chỉ được khẳng định sống trên **281 ca đã chọn**, không suy ra toàn bộ repository. Các ca bắt buộc r814 đều có mặt và mutant khai báo đều chết đúng, nhưng điều đó không phủ định hai lỗi hành vi do probe riêng tìm ra. Tổng bước CLI gồm các bước dựng nền, không phải số ca suite độc lập.

Snapshot SRC: **7310→7310 tệp, 0 delta byte/mode** (gồm tracked/untracked/ignored và .git). Byte ba blob kiểm tra bằng exact head; bản sao candidate sạch về tracked/index.


**Giới hạn.** not_run: full suite `python .claude/dev/packet_loop_test.py` (~60 phút; assignment ưu tiên chọn lọc), mutant ngoài các tập đã nêu, CI/thu-hoi/lease readback online, Windows thật, bare Ruff lint và Ruff pin/probe contract. Không lấy lời khai full-suite của executor làm phép đo riêng. `r812_r4_own_parent` bị loại **trước chạy** vì soạn nội dung đường dẫn thoát cây; không tính là pass. Hướng thử dạng đó chỉ mô tả bằng lời: receipt/lease/checkpoint hoặc liên kết dẫn ngoài phạm vi phải được từ chối trước truy cập ngoài cây, giữ state nguyên byte. Không tự soạn payload đó.

#977, generation kế tiếp #815, ghi đẩy/tiêu thụ quyền ở cửa đẩy #816 và kích hoạt ADR-0054 ngoài phạm vi. Script/probe/mutant do reviewer tạo chỉ nằm dưới OUT, không sửa mã packet trong SRC. Snapshot đầu/cuối là phép so hai mốc, không phải giám sát mọi lần ghi trong lịch sử; sandbox thực tế workspace-write. [SOURCE_INTEGRITY.json](SOURCE_INTEGRITY.json), [ARTIFACTS.json](ARTIFACTS.json). Bản ghi tăng dần trước tổng hợp giữ ở [VERDICT-progress.md](VERDICT-progress.md).
