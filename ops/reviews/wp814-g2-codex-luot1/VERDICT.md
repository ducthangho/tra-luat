Verdict: request_changes
Reviewed commit: 335e746edf041908ca5a965596c8a8a0b3ea0455
Spec sha256: 39b4288959f3889c6c3aad2d24b355c1c02b1462a8854c6a5b00677e81a7ce73; Chung sha256: 4e3d1e1b3f6a0b60b96ad7b70f0ece97eca4bb3d6d10defeab1cd24ac6d1cbf0

Kết luận cuối: **6 lớp P2, 1 lớp P3 mới; 0 P0/P1**. Chưa đạt ngưỡng approve: năm lỗi hành vi sản phẩm và một hồi quy nghiệm thu codepage hiện có. Hai biểu hiện nợ `r813-mutation-evidence-incomplete` được M4 giao đã **ĐÃ VÁ THẬT về độ phủ**. Verdict chỉ neo commit dòng 2, không cấp quyền push, merge, land hoặc kích hoạt ADR-0054.

| slug | hạng P0–P3 | biểu hiện file:dòng | phép đo/tái hiện đã chạy | hướng vá |
|---|---|---|---|---|
| `p3-mapping-namespace-collision` | **P2** | `.claude/dev/packet_loop.py:3068`, `:3071` | `rename-chain`: hai đổi tên a→b, b→c cho `{a,b}→{b,c}` được rc0/approved_pending và ghi `truoc=2,sau=1`; đối chứng tên đích rời nguồn bị rc3 với 2→2. | Chuẩn hoá danh tính nhất quán giữa hai vòng; tránh áp tên nguồn lên tên đích một lần nữa. |
| `finding-lineage-counter-reset` | **P2** | `.claude/dev/packet_loop.py:1206`, `:1228`, `:672` | `p2-rename`: cùng lớp P2 đổi a→b qua bảng nối H hợp lệ được rc0/running, counts `{a-x:1,b-x:1}`; giữ slug a thì rc3/blocked vì a×2. | Đếm theo lớp đã nối, bảo toàn lịch sử cùng lớp; cập nhật cả cách `_load` tái dựng counts. |
| `p3-reopen-enters-failure-counter` | **P2** | `.claude/dev/packet_loop.py:2992`, `:2995` | `ci-p3`: biên nhận H hạng P3, check đỏ hợp lệ vẫn cộng `ci-gate:1`, rc3/blocked ở trần1; P2 đối chứng cũng rc3. | Áp quy tắc loại P3 của M2 ở cửa mo-lai; lưu đủ hạng để tái dựng lịch sử. |
| `legacy-p3-milestone-lost` | **P2** | `.claude/dev/packet_loop.py:3056`, `:3065` | `upgrade-from-real-base`: state do code base tạo, approved_pending với H P3; đổi sang candidate, vua-p3 rồi review cùng P3 được rc0, `vong_p3=null`; state mới tương đương bị rc3 vì 1→1. | Khôi phục mốc từ H đã lưu hoặc migration có xác minh; không coi thiếu trường mới là không có mốc. |
| `receipt-map-validation-skipped` | **P2** | `.claude/dev/packet_loop.py:2756`, `:2969`, `:2901` | H có `bang_noi` là object sai lược đồ: `ci-invalid-map` rc0/running; `accept-invalid-map` rc0/accepted. Cùng dạng sai ở record-review bị rc11/nguyên byte. | Đưa kiểm lược đồ optional bang_noi vào vị từ H dùng chung; kiểm ngữ cảnh nối tại cửa tiêu thụ phù hợp, trước xét dừng/ghi. |
| `new-command-codepage-matrix-incomplete` | **P2** | `.claude/dev/packet_loop_test.py:1799`, `:1817`; parser `packet_loop.py:3351` | `stdout_cp1252`, `stdout_cp1258` FAIL trên candidate, cùng AssertionError thiếu phủ vua-p3; hai ca PASS khi dùng product base. | Thêm đường vua-p3 thành công vào ma trận với H P3 thật và env codepage; giữ guard phủ mọi subcommand. |
| `r814-mutation-evidence-incomplete` | **P3 mới** | `.claude/dev/packet_loop_test.py:9053`; chốt sản phẩm `packet_loop.py:3059`, `:3086` | Hai mutant mới: giữ quyền cũ khi vua-p3; bỏ kiểm nguồn lặp trong bảng nối. Cả hai sống toàn tập r812+r813+r834+r814 đã chọn. A/B riêng: candidate đúng, mutant bị oracle giết bằng AssertionError. | Owner: executor Claude Packet #814. Thêm ca thay quyền sau CI trên head cũ và ca nguồn lặp; giữ predicate sản phẩm đang đúng, thêm mutant đúng chốt. |

**Luật phân hạng.** Năm lớp P2 đầu là phản chứng hành vi thật trên candidate. Lớp codepage P2 là hai ca sẵn có bị đỏ, trái I9 và nghiệm thu bắt buộc full suite N/N; không phải một mutant độ phủ mới do reviewer nghĩ ra. Không xếp P2 chỉ vì mutant mới sống. Lớp P3 là hai thiếu sót độ phủ mới, không phải hai ca M4 đã nêu ở lượt trước, và candidate xử lý đúng ở A/B; vì vậy giữ đúng P3 theo chỉ thị chủ kho. Không thiếu hàng ca r814 nào trong danh sách nghiệm thu; nhưng điều kiện mọi ca sẵn có đạt bị vi phạm bởi hai ca codepage. Thiếu sót độ phủ mới P3 không bị gán thành thiếu ca bắt buộc.

**Phạm vi, nguồn và định danh.** Đã đọc toàn bộ `runs/250b3011/prompt.snapshot`; các đường tương đối tính từ cwd theo chỉ thị trực tiếp. Review không lọc diff và các đường gọi liên quan, trên bản sao riêng `out/candidate`; SRC được đối xử read-only. Reviewer Codex/OpenAI, họ openai, shell Linux qua công cụ, transport machine; executor Claude theo lease bản chép. Packet #814 r3 g2, review_class sensitive, assurance_target cross_approved. Exact serving model/effort/session và attestation launcher codex_cli không được đo độc lập; không tự tạo receipt assurance. Không dùng tài khoản GitHub làm danh tính model, không kế thừa context Executor.

HEAD `335e746edf041908ca5a965596c8a8a0b3ea0455`, tree `c5349f80173b237fa3dbcba6b3abe7333c7f36da`; ref origin/master là `20a2e2b3dd52a83442c739d17db1f1bd66181a6c`. Clone thường, `.git` là thư mục, không nông, detached; `merge-base --is-ancestor` rc0. Hai cha merge là packet `1a8388b92c22a0525b875ccd7366a845c3d632b4` và base review. Base lease `09db70350414d767b793a71cb630e643f216a1b1` là mốc cấp lịch sử, không bị nhầm với base review. Hash hai đặc tả khớp đủ 64 ký tự. Lease có thêm handoff chỉ ở nhánh lease; diff PR đúng hai đường dẫn: product +67/−5, test +73/−3, tổng **140 dòng thêm ≤450**. `diff --check` rc0. [IDENTITY.json](IDENTITY.json), [FULL.diff](FULL.diff).

**Bằng chứng và hướng xử lý từng lớp.**

1. **p3-mapping-namespace-collision — M1/M2, I11.** Nền H approve có `a-x:P3,b-x:P3`; vua-p3; lượt sau H có `b-x:P3,c-x:P3`, bảng nối `a-x→b-x` và `b-x→c-x`, cả hai lý do ghi rõ chỉ đổi tên cùng nguyên nhân. Bảng có nguồn/đích duy nhất và thuộc đúng vòng. Hàm p3 áp map thô lên cả hai danh sách: vòng trước thành `{b-x,c-x}`, vòng sau thành `{c-x}`, tạo giảm giả. Nếu coi chuỗi là các tên đồng nghĩa thì phải chuẩn hoá khép kín cả hai vế; nếu coi nguồn/đích thuộc hai không gian vòng thì phải giữ hai lớp. Cả hai cách đều không cho giảm 2→1 chỉ nhờ đổi tên. Đối chứng `a→c,b→d` đúng rc3/2→2. Hướng vá ở `_vong_p3`: dùng danh tính chuẩn hoặc từ chối bảng nối mơ hồ; thêm ca nguồn/đích giao nhau, chain/cycle và gộp thật. Rủi ro: chỉ bỏ map ở một vế làm hỏng ca gộp 1→1 đã có. Không cung cấp patch sản phẩm cho mã authority. [probes/results.json](probes/results.json), [trace](probes/trace.json).

2. **finding-lineage-counter-reset — M1, I11.** Hai verdict changes_requested mang cùng lớp P2 và bảng nối một-một có lý do vẫn tạo hai khóa đếm độc lập, tránh same_failure_limit=2. Đây không phải reviewer tự khai lớp mới: H công khai khẳng định cùng nguyên nhân. Map chỉ được lưu ở review, không tham gia `dem` hay tái dựng findings của `_load`. Hướng vá: canonical hoá lineage cho reviews và history.mo_lai, bảo toàn số lần cùng nguyên nhân xuất hiện (không cộng đôi nhiều biểu hiện của cùng một review), giữ audit slug gốc. Test cần chuỗi đổi tên P2, gộp, đối chứng hai nguyên nhân độc lập và reload state; tránh sửa counts đơn độc khiến `_load` từ chối state. [probe p2-rename/p2-stable-control](probes/results.json).

3. **p3-reopen-enters-failure-counter — M2.** M2 nói lớp P3 không vào same_failure_limit, nhưng chỉ `cmd_record_review` được đổi; `cmd_mo_lai` vẫn gom mọi slug. Hạng P3 ở ci-do thuộc miền được sản phẩm nhận (connector riêng vẫn đòi P0–P2), H và readback của probe đều hợp lệ. Đặt trần1 để đo ngay: P3 bị ghi `history.mo_lai.finding_ids=['ci-gate']`, counts1 và blocked; không phải lỗi receipt hay gate. Cơ chế này có từ base nhưng trái mục tiêu M2 của packet hiện tại, nên không thể tuyên bố M2 đã hoàn tất. Hướng vá: lọc P3 ở điểm cộng và lưu hạng cho `_load`, giữ việc P2 vẫn chạm trần. Nếu executor muốn đổi miền chấp nhận của mo-lai thay vì miễn P3, đó là đổi hợp đồng, cần xử lý mâu thuẫn theo đặc tả; reviewer không tự cấp quyền đổi hợp đồng. [ci-p3 và ci-p2-control](probes/results.json).

4. **legacy-p3-milestone-lost — M2/M3 và tương thích dữ liệu cũ.** Probe quyết định dùng **chính blob packet_loop.py của base** (sha256 `662e173a5104d64b8dec0b4bf72d3adc80dbee58ff9c608704baad20106f1de1`) để tạo state qua CLI thật. Review cũ không có lop/bang_noi/vong_p3, nhưng `bien_nhan_approve.lop` và `.p3` vẫn ghi a-x P3. Candidate đọc state được, vua-p3 rc0, rồi cùng a-x P3 được rc0/approved_pending vì `truoc=[]` khiến trả None. Đối chứng state mới cùng lớp bị rc3/blocked. Không đòi non-ADR chạy luật mới; đây là state **đã áp ADR-0054**, đúng đầu vào mới của M3, và lời hứa “lượt sau tính là vòng vá” bị bỏ. Hướng vá: khôi phục mốc đúng tuple từ H đã lưu trước khi mở/ghi vòng, hoặc migration được kiểm; thiếu bằng chứng phải báo rõ, không tự tạo thêm vòng miễn giảm. Test upgrade từ base thật, H sạch/rỗng, H có P3 và state non-ADR; tránh hồi tố làm hỏng I9. [more_probes/results.json](more_probes/results.json), [trace](more_probes/trace.json). Probe xoá trường mới trong fixture riêng cũng tái hiện, nhưng bằng chứng chính là upgrade từ code base thật.

5. **receipt-map-validation-skipped — M1, I3/I4.** `_du_dieu_kien_approve` chuyển tiếp bang_noi mà không kiểm; `_vong_p3` chỉ được gọi ở record-review. Do đó biên nhận H cùng tuple đúng nhưng optional bang_noi sai kiểu vẫn được cửa mo-lai hoặc accept tiêu thụ và ghi state. M1 không miễn các receipt của hai cửa này khỏi lỗi lược đồ. Có thể giữ nguyên parser và hợp đồng các đầu vào cũ không có trường này: tách validator hình dạng dùng chung, chỉ kiểm nếu có bang_noi; kiểm tham chiếu nguồn/đích theo đúng vai trò hiện vật. **Không** gọi toàn bộ `_vong_p3` từ accept để vô tình tính một vòng offline mới. Test hai cửa, đúng rc/lý do/byte state, cùng đối chứng receipt không có bang_noi. Phần ngữ nghĩa nối nguồn connector/offline nếu chưa được đặc tả đủ phải chốt với chủ kho, không đoán để sửa. [ci-invalid-map](more_probes/results.json), [accept-invalid-map](boundary_probes/results.json).

6. **new-command-codepage-matrix-incomplete — I9 và full-suite N/N.** Hai ca có sẵn `stdout_cp1252`, `stdout_cp1258` chạy xong các bước CLI rồi cùng ném `AssertionError: [cp1252/cp1258] ma trận codepage THIẾU PHỦ lệnh con ['vua-p3']`. Parser đã thêm subcommand nhưng `_kich_ban_in`/`da_phu` chưa bổ sung đường thành công. Đối chứng dùng chính hai ca và blob product base: 2/2 PASS; không phải lỗi môi trường Windows giả hoặc CLI sập. Hướng vá phần test: dựng approved_pending mang H P3 thật, chạy vua-p3 ở cả hai env codepage, kiểm rc0 và stdout khác rỗng/đọc được, thêm tên vào tập đã thực chạy. Rủi ro: đưa vào `LENH_KHONG_CO_STDOUT` là ngoại lệ sai vì lệnh thực sự in stdout; chạy nhánh lỗi chỉ in stderr cũng không đo được tính chất cần khóa. Không suy đây là lỗi encoding thật của sản phẩm: bằng chứng là guard độ phủ hiện có đỏ trên candidate. [baseline_regression/results.json](baseline_regression/results.json), [đối chứng base](codepage_base/results.json).

7. **r814-mutation-evidence-incomplete — nợ P3 mới.** Mutant `p3-retains-old-right` đổi phép gán quyền p3 thành giữ `mo_lai_tu` cũ nếu có; mutant `mapping-allows-duplicate-source` bỏ kiểm nguồn lặp. Candidate: chuỗi approve A→ci-do A→review B P3→vua-p3 thay đúng tuple `(p3,1,B)`; mutant giữ `(ci-do,1,A)`, oracle tuple ném AssertionError. Candidate từ chối nguồn lặp rc11/“sai lược đồ” và nguyên byte; mutant nhận rc0, oracle rc/byte ném AssertionError. Owner Claude executor #814; hướng vá test ở ca r814 và MUTANTS, không sửa predicate sản phẩm đang đúng. Rủi ro: ca quyền chỉ bắt đầu từ state chưa có quyền sẽ không phân biệt giữ cũ với thay mới; ca lặp nguồn có thể bị lỗi khác che nếu không giữ mọi yếu tố còn lại hợp lệ. Cặp neo/thay và runner ở [extra_mutations.py](extra_mutations.py); A/B và oracle ở [more_probes.py](more_probes.py), [kết quả](more_probes/results.json). Đây là dữ liệu phản chứng trên cây riêng, không phải patch giao áp lên SRC.

**Đối chiếu M4 với nợ #813.**

| biểu hiện trong verdict lượt6 #813 | trạng thái ở candidate | bằng chứng độc lập |
|---|---|---|
| check_refs gồm cặp hợp lệ trộn null | **ĐÃ VÁ THẬT về độ phủ** | `r814_check_refs_tron_null` PASS, rc11/“đúng dạng”/nguyên byte; `r814_refs_bo_do_dai` chết tại đúng ca: AssertionError đòi11/được0. |
| ci-do→begin→void→connector | **ĐÃ VÁ THẬT về độ phủ** | `r814_ci_void_connector` PASS, rc8/“chưa mở lượt mới”/nguyên byte; `r814_void_khoi_phuc_quyen_ci` và `r813_quyen_ci_qua_luot_moi` đều chết đúng ca, đòi8/được0. |

Chốt ca (b) đúng là không có begin_attempt kể từ mo_lai cuối, dòng2962; void không xoá dấu begin. Không nhận lời khai handoff làm kết quả riêng. Không chuyển hai biểu hiện đã đóng sang slug nợ mới.

**Từng ca nghiệm thu và mutant khai báo.** Mọi ca trong bảng dưới PASS trên candidate; từng lỗi mutant là **AssertionError** tại đúng ca, không traceback/CLI sập. `đòi/được` là rc CLI, trừ hai oracle counts và oracle tuple đã ghi rõ. [MUTATION_AUDIT.md](MUTATION_AUDIT.md) và [JSON đầy đủ](mutants/results.json) giữ tên ca, thông điệp không cắt, mỏ neo/thay và đối chứng.

| yêu cầu | ca r814 | mutant | lỗi đúng lý do trên mutant |
|---|---|---|---|
| {A,B}→{B} hợp lệ | `r814_ab_b_hop_le` | `r814_giam_hai_lop` | đòi0/được3; siết sai 2→1 |
| biểu hiện trùng, 2→2 blocked | `r814_bieu_hien_trung` | `r814_khong_giam_van_qua` | đòi3/được0 |
| đổi tên thiếu bảng nối | `r814_doi_ten_khong_noi` | `r814_doi_ten_tu_do` | đòi11/được0 |
| gộp thuần, sau nối 1→1 blocked | `r814_gop_qua_noi` | `r814_noi_chi_vong_nay` | đòi3/được0 |
| bảng nối sai lược đồ | `r814_noi_sai_luoc_do` | `r814_noi_bo_ly_do` | đòi11/được3; tới chốt vòng thay vì từ chối đầu vào |
| bảng nối trỏ slug không có | `r814_noi_tro_slug_khong_co` | `r814_noi_bo_nguon` | đòi11/được0 |
| mốc→vòng1 không giảm | `r814_moc_vong1_khong_giam` | `r814_vong1_mien_so` | đòi3/được0 |
| vòng3 blocked | `r814_vong_3` | `r814_vong_3_lot` | đòi3/được0 ở bước6 |
| P3 không vào same-failure ở review | `r814_p3_khong_dem` | `r814_p3_vao_dem` | counts đòi{}, được a-b:1 |
| đối chứng P2 vẫn đếm | `r814_p2_van_dem` | `r814_bo_ca_p2` | counts đòi a-b:1, được{} |
| tự chọn vá đi được, ghi quyền | `r814_vua_p3_di_duoc` | `r814_vua_khong_ghi_quyen` | oracle tuple mo_lai_tu sai/thiếu |
| tập chọn rỗng | `r814_vua_p3_rong` | `r814_vua_tap_rong` | đòi2/được0 |
| slug ngoài H | `r814_vua_p3_ngoai_bien_nhan` | `r814_vua_ngoai_bien_nhan` | đòi11/được0 |
| xoá hết P3 hoàn tất vòng | `r814_xoa_het_p3` | `r814_rong_la_khong_giam` | đòi0/được3; tập finding sạch được phép rỗng |
| vua-p3 dùng xét dừng | `r814_vua_p3_xet_dung` | `r814_vua_khong_xet` | đòi3/được0 ở bước2 |
| changes_requested generation khác | `r814_am_generation_khac` | `r812_bo_generation` | đòi11/được0; mutant còn giết đúng hai ca r812/r834 |
| M4 mixed refs | `r814_check_refs_tron_null` | `r814_refs_bo_do_dai` | đòi11/được0 |
| M4 void không khôi phục ci-do | `r814_ci_void_connector` | `r814_void_khoi_phuc_quyen_ci`; `r813_quyen_ci_qua_luot_moi` | cả hai đòi8/được0 ở bước3 |

Đối chứng bắt buộc r812/r813/r834: 254/254 ca an toàn đã chọn PASS. Hai ca codepage sẵn có bổ sung: 0/2, **FAIL**, lớp P2 riêng ở trên. Mỗi mutant khai báo có ba đối chứng khác họ PASS. Runner riêng tái dùng chay_suite/_phan_loai_dot_bien/_doi_chung_khac_ho/_phan_loai_giet của main mục3; đã đọc `tham-chieu/chon.py` trước khi dùng logic. Runner kiểm tập chọn không rỗng, ca đích tồn tại, neo duy nhất, giữ toàn thông điệp thay vì cắt 200 ký tự. Không suy pass từ rc0 của regex rỗng. Ca dương được mutant siết sai làm đỏ, không ép chúng dùng mutant nới chốt vô nghĩa.

**Bất biến và nhánh biên đã soi.**

| bất biến/mục tiêu | kết luận trong phạm vi đã đo |
|---|---|
| I1/I2/I8/I10 | Các đường authority/lease/canon không đổi; r812 hồi quy PASS; receipt âm sai generation bị từ chối. vua-p3 lấy P3 từ H pending đã lưu và neo generation/head hiện hành. Không xác minh thẩm quyền lease online trong review offline. |
| I3/I4 | record-review từ chối map null/sai kiểu/sai phần tử/thiếu nguồn/thiếu đích/nguồn lặp/đích lặp/lý do trống/khóa thừa với rc11, đúng lý do và nguyên byte. vua-p3 rỗng rc2, ngoài H rc11, kể cả tại trần same-failure. Map sai trước khi cộng lớp tái diễn vẫn nguyên byte. Ngoại lệ có thật là `receipt-map-validation-skipped` ở hai cửa khác. |
| I4/I5 | Vòng hợp lệ không giảm hoặc vòng3 ghi reviews, đóng attempt, tăng review_rounds_used, tiêu thụ codex-call, lưu blocked_vong_p3 rồi rc3. vua-p3 gọi cùng _xet_dung; mutant bỏ nó chết đúng. 33 state cuối của probe được lệnh status đọc lại rc0, gồm các nhánh blocked và changes_requested P3. |
| I6 | Quyền p3 đúng tuple và thay quyền cũ trên candidate; quyền p3 không mở được mo-lai connector từ running (rc8/nguyên byte). Mutant giữ cũ là P3 mới, không gán lỗi đó cho candidate. Tiêu thụ ở cửa đẩy thuộc #816 ngoài phạm vi. |
| I7 | Hồi quy r834/r813 giữ check theo kho/PR/head, app/workflow/job và run/attempt mới nhất; M4 check_refs mixed đo đúng chốt độ dài. Không chạy CI thật hoặc đo mạng. |
| I9 | Nhánh non-ADR trong record-review giữ dem=ids; đường lease cũ và r812/r813/r834 chọn lọc đạt; hai ca codepage FAIL. Tương thích state ADR cũ có lỗi riêng `legacy-p3-milestone-lost`, không giả định thiếu lop nghĩa là không từng có P3. Không tuyên bố full suite N/N. |
| I11/M1/M2 | Còn hai lỗi identity/map và lỗi P3 ở mo-lai trong bảng lớp; bảng nối H có lý do không được phép làm giảm giả hay reset lớp tái diễn. |
| M3 | Đường tự chọn, tập chọn, quyền và chốt same-failure đạt các ca khai; nâng cấp từ state cũ chưa giữ lời hứa vòng sau của M2. |
| M4 | Cả hai biểu hiện kế thừa được test và mutant khóa đúng; mã sản phẩm liên quan không bị sửa trong diff. |

Probe `changes_requested` toàn-P3: mốc→cùng lớp bị rc3/1→1; hai→một được rc0/running, counts vẫn{}. `vua-p3→begin→void→review` cùng lớp vẫn rc3, nên void không reset vòng. `mo-lai connector→chu-kho-duyet→review` tạo mốc mới theo cơ chế công bố (`vong_p3=null`); số vòng đã ghi vẫn được cộng trong k, không tự reset budget toàn packet.

Hai gợi ý về “giảm giả” cần phân biệt với quyền phân lớp của H: `tu:[]` khai lớp mới C đồng thời A/B không còn trong verdict được nhận 2→1; đổi cùng slug P3 lên P2 được ghi 1→0 nhưng state là running/changes_requested, chưa approve. H do reviewer chịu trách nhiệm cho việc các lớp cũ đã được sửa và hạng mới. Máy không có oracle để chứng minh reviewer nói sai về mã thực, nên không tự xếp thêm finding chỉ vì hai đầu vào H hợp lệ này được nhận. Trái lại, chuỗi đổi tên ở lớp đầu đã có **bằng chứng trong chính H rằng chỉ đổi tên**, đủ chứng minh giảm giả mà không cần suy ý reviewer.

**Lệnh và kết quả độc lập.** Tất cả script/fixture/mutant/log do reviewer tạo ở OUT. Môi trường: `PYTHONDONTWRITEBYTECODE=1`, `TMPDIR=out/tmp`, `GIT_CONFIG_GLOBAL=/dev/null`, `GIT_CONFIG_SYSTEM=/dev/null`, `GIT_OPTIONAL_LOCKS=0`, `GIT_ALLOW_PROTOCOL=file`; copy ghim core.abbrev=7. Fetch/push/ls-remote trong fixture chỉ thao tác các kho bare cục bộ dưới OUT; không mạng/GitHub, không push SRC hoặc remote thật.

| command | rc | bằng chứng dương |
|---|---:|---|
| `python -B out/bootstrap.py` | 0 | Hai hash khớp, ancestry, head/tree/ref, detached/không nông, diff đúng write set; IDENTITY.json. |
| `python -B -W ignore out/run_review.py baseline_r814 '^r814_'` | 0 | 18/18 PASS; baseline_r814/results.json. |
| `python -B -W ignore out/run_review.py baseline_regression '^r81[23]_|^r834_|^stdout_cp'` | 1 | 254/256 PASS; r812: 148, r813: 43, r834: 63, stdout: 2; 2 ca stdout FAIL thiếu vua-p3. |
| `python -B -W ignore out/codepage_baseline.py` | 0 | 2/2 ca stdout PASS trên product base; codepage_base/results.json. |
| `python -B -W ignore out/run_review.py mutants` | 0 | 19/19 mutant, 22 target GIET, 57 đối chứng PASS, 0 tín dụng giả. |
| `python -B -W ignore out/run_review.py gates` | 0 | doctrine-scan rc0: 10 tệp/0 chỗ chép; adr-song rc0: 55/55, ngoại lệ0016 đã khai. |
| `python -B -W ignore out/probes.py` | 0 | 24 kịch bản hoàn tất, không lỗi runner; rc/state/lý do từng bước ở probes/trace.json. Các rc0 sai kỳ vọng đặc tả được ghi thành findings, không gọi là PASS. |
| `python -B -W ignore out/more_probes.py` | 0 | 5 kịch bản bổ sung, 2 cặp A/B; nâng cấp từ base thật và oracle mutant đầy đủ. |
| `python -B -W ignore out/boundary_probes.py` | 0 | 4 kịch bản biên; 33/33 state reload qua CLI status rc0. |
| `python -B -W ignore out/extra_mutations.py` | 0 | Mỗi mutant mới sống 272/272 ca r812+r813+r834+r814; A/B riêng đã giết đúng. |
| `python -B out/finalize.py` | 0 | Đối chiếu inventory, snapshot source, exact head/tree/ref, băm artifact; SOURCE_INTEGRITY.json, ARTIFACTS.json. |

Tổng nền chọn lọc **272/274 PASS, 2 FAIL**, không phải N/N toàn repository. **Bỏ trước chạy** `r812_r4_own_parent` vì ca tạo nội dung đường dẫn có thành phần thoát cây, đúng chỉ thị prompt; không tính ca đó là pass. Hai mutant mới chỉ được khẳng định sống trên tập 272 ca đã chọn, không suy ra toàn bộ repository. Hai ca stdout vốn đỏ ở baseline không được dùng để nhận tín dụng giết mutant mới. Phép đo trên Linux không chứng minh Windows thật. Mã rc0 của runner probe chỉ chứng minh kịch bản đã hoàn tất và ghi bằng chứng, không chứng minh sản phẩm đúng đặc tả.

**Giới hạn và toàn vẹn.** not_run: full suite `python .claude/dev/packet_loop_test.py` (~60 phút, assignment ưu tiên chọn lọc), mutants ngoài tập đã nêu, online CI/thu-hoi/lease readback, Windows thật, bare Ruff lint và Ruff pin/probe contract. Không nhận full-suite executor làm kết quả độc lập. Tệp tham chiếu #813 là lịch sử finding; không review lại ngoài phạm vi nợ M4. #977, #815, ghi đẩy/tiêu thụ quyền ở cửa đẩy #816 và kích hoạt ADR-0054 ngoài phạm vi.

Hướng thử cần nội dung đường dẫn thoát cây chỉ mô tả bằng lời: biên nhận/lease/checkpoint hoặc liên kết dẫn ngoài phạm vi phải bị từ chối trước truy cập ngoài cây, giữ state nguyên byte. Không tự soạn payload đó.

Snapshot SRC sau preflight và trước test so với cuối: 7304→7304 tệp (tracked/untracked/ignored và .git), **0 delta byte/mode**, exact head/tree/ref và worktree/index sạch. Đây là so sánh hai mốc, không chứng minh toàn bộ lịch sử mọi lần ghi. Sandbox thực tế workspace-write; quy tắc user chỉ ghi OUT được giữ cho script và phép thử. [SOURCE_INTEGRITY.json](SOURCE_INTEGRITY.json) giữ phép đo; [ARTIFACTS.json](ARTIFACTS.json) băm report/scripts/logs/results, không băm toàn bộ fixture/copy. Bản ghi tăng dần trước khi tổng hợp được lưu ở [VERDICT-progress.md](VERDICT-progress.md).
