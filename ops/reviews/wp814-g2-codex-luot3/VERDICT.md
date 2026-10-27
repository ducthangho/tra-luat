Verdict: request_changes
Reviewed commit: 24f6a7314e8c5a32c693ed6b041fee72de68a171
Spec sha256: 39b4288959f3889c6c3aad2d24b355c1c02b1462a8854c6a5b00677e81a7ce73; Chung sha256: 4e3d1e1b3f6a0b60b96ad7b70f0ece97eca4bb3d6d10defeab1cd24ac6d1cbf0

**Kết luận lượt 3: 1 lớp P2, 2 lớp P3; 0 P0/P1.** Hai chuỗi `finding-lineage-counter-reset` của lượt 2 đã bị chặn đúng. Tuy nhiên, các cửa ngoài record-review vẫn nhận bảng nối khai lớp mới với đích không có trong bảng lớp, trái M1/I4. Chưa đạt ngưỡng approve. Verdict chỉ neo commit dòng 2; không cấp quyền push, merge, land hay kích hoạt ADR-0054.

| slug | hạng P0–P3 | biểu hiện file:dòng | phép đo/tái hiện đã chạy | hướng vá |
|---|---|---|---|---|
| `receipt-map-validation-skipped` | **P2**, giữ lớp lượt 1, biểu hiện ngữ nghĩa còn sót | `.claude/dev/packet_loop.py:3065`, `:3068`; callers `:2900`, `:2974`; kiểm đích chỉ ở `:3083` | H có `bang_noi: [{tu: [], den: missing-x, ly_do: new class}]`, bang_lop không có missing-x: ci-do rc0/running, connector rc0/cho_chu_kho, accept rc0/accepted; cả ba ghi state. Đối chứng đích có thật rc0; record-review đích không có rc11/nguyên byte. | Owner executor Claude #814. Kiểm tham chiếu đích trên chính ảnh H đã đọc ở mọi cửa; giữ tách biệt với phép tính vòng P3. |
| `legacy-p3-failure-counts-retained` | **P3 theo quyết định chủ kho**, không nâng lại P2 | `.claude/dev/packet_loop.py:672`, `:1206`, `:1228` | Fixture nâng cấp do blob base 20a2e2b tạo qua CLI: approve P3 có finding-id lưu count1; candidate vua-p3 rồi cùng slug lên P2 thành count2/rc3. State tạo mới trên candidate chỉ count1/rc0. Không tìm được state ADR-0054 thật trong SRC cung cấp. | Owner **#816**, ghi nợ theo quyết định; **không viết migration ở #814**. Trước kích hoạt rà dữ liệu thực và quyết định riêng nếu cần. |
| `r814-mutation-evidence-incomplete` | **P3**, hai biểu hiện lượt 2 đã đóng, một biểu hiện mới | `.claude/dev/packet_loop_test.py:9094`; chốt sản phẩm `.claude/dev/packet_loop.py:3068` | Mutant `first-map-only` chỉ xét hàng đầu bảng nối sống toàn tập chọn đã xác minh. A/B accept: hàng đầu khai mới, hàng thứ hai nối lại; candidate rc11/nguyên byte, mutant rc0/accepted; oracle riêng AssertionError. | Owner executor Claude #814. Thêm ca nhiều hàng với hàng đầu hợp lệ, hàng sau nối lại; thêm mutant gỡ đúng phép duyệt toàn bộ. Giữ chốt sản phẩm đang đúng. |

**Lý do phân hạng.** P2 ở hàng đầu là hành vi sai của mã sản phẩm trên đầu vào H có tham chiếu đích không hợp lệ, không phải kết luận từ mutant sống. Đặc tả M1 yêu cầu “bảng nối … trỏ slug không có ⇒ từ chối, state nguyên byte”; không miễn `tu: []` hay cửa accept/mo-lai. Giữ slug `receipt-map-validation-skipped` vì cùng nguyên nhân kiểm bảng nối chưa đi hết các cửa, không gộp vào lineage: trong phản chứng mới không có nguồn được nối để reset counts. Lớp legacy giữ P3 theo quyết định chủ kho được prompt ghi lại; state nâng cấp dưới OUT là fixture tự kích hoạt ADR, **không** là state vận hành thật. Mutant mới first-map-only là nợ P3 vì candidate xử lý đúng ở A/B và đây chưa phải phản chứng từ lượt trước hay ca nghiệm thu bắt buộc bị thiếu.

**Bằng chứng và hướng xử lý P2.** `probes.py::map_gate_matrix` dựng nền dương đầy đủ bằng CLI, receipt H đúng packet/generation/head/spec_hash, validator canon, readback CI/connector và quyết định P3 hợp lệ. Đổi riêng đích khai mới thành `missing-x`, không có trong bang_lop:

| cửa | đích không có | đích có thật | hình dạng null / lý do rỗng | nối nguồn khác rỗng |
|---|---|---|---|---|
| mo-lai ci-do | **rc0, running, state đổi** | rc0/running | rc11/nguyên byte | rc11/nguyên byte |
| mo-lai connector | **rc0, cho_chu_kho, state đổi** | rc0/cho_chu_kho | rc11/nguyên byte | rc11/nguyên byte |
| accept, có P3 connector | **rc0, accepted, state đổi** | rc0/accepted | rc11/nguyên byte | rc11/nguyên byte |
| record-review | rc11/nguyên byte | kiểm theo ngữ cảnh vòng P3 | suite/schema từ chối | chỉ nguồn/đích P3 đúng vòng được xét |

Các state cuối đều reload bằng `status` rc0. Bảng nối rỗng `[]` vẫn được nhận ở ba cửa ngoài review như đối chứng. [Kết quả đầy đủ](probes_final/results.json), [trace CLI](probes_final/trace.jsonl), [script](probes.py).

Vá tại validator dùng chung hoặc helper kiểm ngữ nghĩa được gọi ở ba cửa ngoài review, vì chính những cửa này bỏ qua đích. Hướng rẻ nhất là kiểm mọi `den` có trong bang_lop trên cùng ảnh bn trước xét dừng/ghi state, kể cả `tu` rỗng; giữ kiểm hạng/nguồn/vòng tại record-review và chặn nối lại ngoài vòng. Không cần đổi parser/hợp đồng các đầu vào cũ không có bang_noi. Ca khóa lỗi: mỗi cửa có cặp đích có thật/không có; đòi rc11, thông điệp rõ và state nguyên byte cho vế sai; mutant bỏ riêng kiểm đích phải làm đỏ đúng ca. Rủi ro cần tránh: gọi nguyên `_vong_p3` từ accept/mo-lai sẽ tính nhầm vòng offline; cấm toàn bộ `tu: []` sẽ làm mất khai lớp mới hợp lệ. Đây là hướng sửa, không phải patch sản phẩm giao áp lên SRC.

**ĐỐI CHIẾU LƯỢT TRƯỚC.**

| lớp ở lượt 2 / lịch sử | trạng thái lượt này | phép đo độc lập |
|---|---|---|
| `finding-lineage-counter-reset` | **ĐÃ VÁ THẬT trong phạm vi cửa H hiện hành** | Hai chuỗi a-b:P2 count1 → approve sạch → mo-lai ci-do/connector với H c-b:P2, bảng nối a-b→c-b: đều rc11/“đổi tên/gộp”/nguyên byte, counts chỉ a-b:1. Hai đối chứng cùng a-b không đổi tên: rc3/blocked, a-b:2. Cả bốn status rc0. record-review nối P2, accept nối lại cũng bị ca riêng bắt; mutant từng cửa chết đúng. |
| `legacy-p3-failure-counts-retained` | **CHƯA VÁ, chuyển/giữ nợ P3 theo chủ kho** | Blob base thật tạo fixture qua CLI, không chèn counts/history. Hai vế upgrade/fresh cùng vòng k1/1→0; upgrade count2/blocked do same-failure, fresh count1/running. Không có bằng chứng state ADR thật, không kích hoạt ngoại lệ nâng P2. |
| `r814-mutation-evidence-incomplete`: source-rank | **ĐÃ VÁ THẬT biểu hiện cũ** | `r814_noi_nguon_p2` PASS; `r814_noi_nguon_hang` (chỉ gỡ hạng nguồn, chính dạng mutant lượt 2) làm ca AssertionError đòi11/được0. |
| `r814-mutation-evidence-incomplete`: destination-rank | **ĐÃ VÁ THẬT biểu hiện cũ** | `r814_noi_dich_p2` PASS; `r814_noi_dich_hang` (chỉ gỡ hạng đích) làm ca AssertionError đòi11/được0. Lớp còn biểu hiện mới P3 first-map-only nêu trên. |
| Lịch sử `receipt-map-validation-skipped` | **Các biểu hiện schema cũ đã vá; lớp CHƯA ĐÓNG về ngữ nghĩa tham chiếu** | Null/lý do rỗng bị cả ba cửa ngoài review từ chối; đích không tồn tại với nguồn rỗng vẫn được nhận. Vì vậy rút lại phạm vi kết luận đóng toàn lớp của lượt 2, giữ slug lịch sử. |
| Lịch sử `p3-mapping-namespace-collision` | giữ **ĐÃ VÁ THẬT** | r814_noi_chuoi PASS, mutant bỏ điều kiện nguồn rời vòng này bị giết; gộp áp lên cả hai vòng ra1→1/blocked. |
| Lịch sử `p3-reopen-enters-failure-counter` | giữ **ĐÃ VÁ THẬT** | CI P3 ở trần1 rc0/running/counts{}; r814_mo_lai_dem_p3 bị oracle counts bắt. |
| Lịch sử `legacy-p3-milestone-lost` | giữ **ĐÃ VÁ THẬT phần mốc** | Ca state cũ và mutant giữ mốc đạt; probe upgrade thật từ blob base cũng ghi k1/1→0. Nợ counts lịch sử được giữ riêng. |
| Lịch sử `new-command-codepage-matrix-incomplete` | giữ **ĐÃ VÁ THẬT** | stdout_cp1252, stdout_cp1258 PASS, gồm vua-p3 thành công có stdout. Đây là chạy Linux với env codepage, không là Windows thật. |
| Nợ M4 `r813-mutation-evidence-incomplete` | **ĐÃ VÁ THẬT hai biểu hiện được giao** | Mixed check_refs: rc11/“đúng dạng”/nguyên byte; bỏ so độ dài làm đỏ. CI→begin→void→connector: rc8/“chưa mở lượt mới”/nguyên byte; cả mutant riêng và mutant r813 dùng chung làm đỏ đúng bước. |

**Nợ P3 mới và nợ legacy.** Mutant first-map-only đổi duy nhất vòng duyệt trong `_khong_noi_lai` từ mọi hàng thành hàng đầu. Probe có hai lớp connector c-d/e-f, hai refs phân biệt và hai quyết định P3 đầy đủ. Bảng nối hàng1 khai mới c-d, hàng2 old-x→e-f. Candidate từ chối rc11/nguyên byte; mutant nhận rc0/accepted. Đối chứng hai hàng đều khai mới được candidate nhận rc0. Không ca hiện có nào trong tập đã đo bắt mutant sau khi sửa lỗi logger riêng. Mỏ neo/thay và oracle chạy được nằm ở [extra_mutations.py](extra_mutations.py), [mutation.json](extra_mutations/first-map-only/mutation.json), [A/B](extra_mutations/observations.json), [đối chứng dương](boundary_probes/results.json). Hướng vá test: mở rộng baseline nhiều hàng rồi đổi riêng nguồn của hàng sau, dùng oracle rc/lý do/byte state; giữ mutant first-map-only và ba đối chứng khác họ. Rủi ro: hàng đầu sai schema/đích hoặc refs không phủ đủ sẽ che chốt cần đo. Không sửa product đang đúng chỉ để làm test xanh.

Legacy: owner #816; rẻ nhất ở #814 là ghi nợ theo chỉ thị, không migration. Trước kích hoạt kiểm state thực và chính sách nâng cấp. Nếu về sau có authority di trú, cần phân biệt lượt P3 có bằng chứng với lượt P0–P2 thật, bảo toàn sổ audit và tính nhất quán `_load`; test khóa bằng state do bản cũ tạo, cùng slug P2 về sau và đối chứng state mới. Xóa counts đơn độc sẽ làm hỏng invariant findings; hồi tố không có bằng chứng có thể xóa lỗi nghiêm trọng. [Hai vế upgrade/fresh](probes_final/results.json), [blob base](base-product/packet_loop.py), [quét state thực trong SRC](REAL_STATE_SCAN.json).

**Từng ca nghiệm thu và mutant.** Nền r814 **30/30 PASS**. **31 mutant / 34 target GIET / 93 đối chứng khác họ PASS**, không skip hay tín dụng giả. Đọc đầy đủ tên ca, loại ngoại lệ và thông điệp; mọi target là AssertionError tại oracle rc/counts/quyền, không traceback/CLI sập. Với oracle quyền đã đọc state: mutant giữ ci-do neo A trong khi pending là B, A≠B; mutant bỏ quyền cho None. Không chỉ dựa vào nhãn GIET của harness. [Audit đầy đủ](MUTATION_AUDIT.md), [JSON kết quả](mutants/results.json).

| yêu cầu / bổ sung | ca (nền PASS) | mutant bị giết | AssertionError đúng lý do |
|---|---|---|---|
| {A,B}→{B} hợp lệ | `r814_ab_b_hop_le` | `r814_giam_hai_lop` | r813 bước 1: đòi rc=0, được rc=3; stderr='vòng vá P3 thứ 1 (tối đa 2), lớp P3 2 → 1 (phải giảm) — packet về blocked; ghi handoff, hỏi chủ kho.' |
| biểu hiện trùng, 2→2 bị blocked | `r814_bieu_hien_trung` | `r814_khong_giam_van_qua` | r813 bước 1: đòi rc=3, được rc=0; stderr='' |
| mốc→vòng1 không giảm | `r814_moc_vong1_khong_giam` | `r814_vong1_mien_so` | r813 bước 1: đòi rc=3, được rc=0; stderr='' |
| đổi tên thiếu bảng nối | `r814_doi_ten_khong_noi` | `r814_doi_ten_tu_do` | r813 bước 1: đòi rc=11, được rc=0; stderr='' |
| gộp thuần sau nối 1→1 | `r814_gop_qua_noi` | `r814_noi_chi_vong_nay` | r813 bước 1: đòi rc=3, được rc=0; stderr='' |
| bổ sung M1–M3 | `r814_noi_sai_luoc_do` | `r814_noi_bo_ly_do` | r813 bước 1: đòi rc=11, được rc=3; stderr='vòng vá P3 thứ 1 (tối đa 2), lớp P3 1 → 1 (phải giảm) — packet về blocked; ghi handoff, hỏi chủ kho.' |
| bổ sung M1–M3 | `r814_noi_tro_slug_khong_co` | `r814_noi_bo_nguon` | r813 bước 1: đòi rc=11, được rc=0; stderr='' |
| vòng thứ3 bị blocked | `r814_vong_3` | `r814_vong_3_lot` | r813 bước 6: đòi rc=3, được rc=0; stderr='' |
| P3 không vào same-failure | `r814_p3_khong_dem` | `r814_p3_vao_dem` | counts đòi {}, được a-b:1 |
| đối chứng P2 vẫn đếm | `r814_p2_van_dem` | `r814_bo_ca_p2` | counts đòi a-b:1, được {} |
| tự chọn vá P3, quyền đúng tuple | `r814_vua_p3_di_duoc` | `r814_vua_khong_ghi_quyen` | oracle quyền thấy None thay (p3,1,pending_sha) |
| tập chọn P3 rỗng | `r814_vua_p3_rong` | `r814_vua_tap_rong` | r813 bước 0: đòi rc=2, được rc=0; stderr='' |
| tập chọn ngoài biên nhận | `r814_vua_p3_ngoai_bien_nhan` | `r814_vua_ngoai_bien_nhan` | r813 bước 0: đòi rc=11, được rc=0; stderr='' |
| vòng vá xóa hết P3 | `r814_xoa_het_p3` | `r814_rong_la_khong_giam` | r813 bước 1: đòi rc=0, được rc=3; stderr='vòng vá P3 thứ 1 (tối đa 2), lớp P3 1 → 1 (phải giảm) — packet về blocked; ghi handoff, hỏi chủ kho.' |
| bổ sung M1–M3 | `r814_vua_p3_xet_dung` | `r814_vua_khong_xet` | r813 bước 2: đòi rc=3, được rc=0; stderr='' |
| changes_requested sai generation | `r814_am_generation_khac` | `r812_bo_generation` | r812 review ['bn', 'ids', 'lop', 'verdict']: đòi rc=11, được rc=0; stderr='' |
| M4(a), check_refs hợp lệ trộn null | `r814_check_refs_tron_null` | `r814_refs_bo_do_dai` | r813 bước 0: đòi rc=11, được rc=0; stderr='' |
| bổ sung M1–M3 | `r814_noi_chuoi` | `r814_noi_chuoi_lot` | r813 bước 1: đòi rc=11, được rc=0; stderr='' |
| bổ sung M1–M3 | `r814_noi_lop_p2` | `r814_noi_moi_hang` | r813 bước 0: đòi rc=11, được rc=0; stderr='' |
| bổ sung M1–M3 | `r814_noi_nguon_lap` | `r814_noi_nguon_lap_lot` | r813 bước 1: đòi rc=11, được rc=0; stderr='' |
| bổ sung M1–M3 | `r814_mo_lai_noi_hong` | `r814_noi_chi_record_review` | r813 bước 0: đòi rc=11, được rc=0; stderr='' |
| bổ sung M1–M3 | `r814_mo_lai_p3_khong_dem` | `r814_mo_lai_dem_p3` | counts đòi {}, được ci-gate:1 |
| bổ sung M1–M3 | `r814_state_cu_giu_moc` | `r814_state_cu_mat_moc` | r813 bước 2: đòi rc=3, được rc=0; stderr='' |
| bổ sung M1–M3 | `r814_vua_thay_quyen_ci` | `r814_vua_giu_quyen_cu` | oracle quyền thấy (ci-do,1,A), phải (p3,1,B), A≠B |
| cửa H ci-do từ chối nối lại | `r814_mo_lai_ci_noi_lai` | `r814_mo_lai_ci_bo_chan_noi` | r813 bước 0: đòi rc=11, được rc=0; stderr='' |
| cửa H connector từ chối nối lại | `r814_mo_lai_cn_noi_lai` | `r814_mo_lai_cn_bo_chan_noi` | r813 bước 0: đòi rc=11, được rc=0; stderr='' |
| cửa H accept từ chối nối lại | `r814_accept_noi_lai` | `r814_accept_bo_chan_noi` | r834 accept: đòi rc=11, được rc=0; stderr='' |
| P3 lượt2: kiểm riêng hạng nguồn | `r814_noi_nguon_p2` | `r814_noi_nguon_hang` | r813 bước 0: đòi rc=11, được rc=0; stderr='' |
| P3 lượt2: kiểm riêng hạng đích | `r814_noi_dich_p2` | `r814_noi_dich_hang` | r813 bước 1: đòi rc=11, được rc=0; stderr='' |
| M4(b), CI→begin→void→connector | `r814_ci_void_connector` | `r813_quyen_ci_qua_luot_moi`; `r814_void_khoi_phuc_quyen_ci` | r813 bước 3: đòi rc=8, được rc=0; stderr='' |


Đối chứng bắt buộc: **148 ca r812 + 43 ca r813 + 63 ca r834 + 2 ca stdout = 256/256 được xác minh PASS** sau recheck lỗi logger. Cộng r814: **286/286 ca chọn lọc PASS**; không phải full suite N/N. Ca `r812_r4_own_parent` bị loại trước chạy theo chỉ thị không tự soạn nội dung đường dẫn thoát cây, không tính là PASS.

**Bản đồ cửa H và bất biến.** Đã tự tìm bằng `_du_dieu_kien_approve(`, mọi đọc bang_lop/bang_noi/bien_nhan_approve, các điểm đọc YAML và validator. Ba call sites của vị từ H: record-review (`1198`), _slug_connector/accept (`2899`), mo-lai (`2973`, tách ci-do/connector). Không thấy cửa chuyển state khác tiêu thụ bảng nối bị bỏ khỏi bảng executor. `vua-p3` đọc ảnh pending đã xác thực; `_vong_p3` đọc lớp lịch sử/ảnh pending cũ. `chu-kho-duyet` đọc checkpoint, record-lease đọc lease, không dùng bảng nối. Lệnh báo cáo `bien-nhan` (`2138`) đọc receipt để đếm hiện vật theo khóa neo, không đọc bảng lớp/nối, không chuyển state hoặc cộng finding_counts; đây là consumer receipt rộng hơn nhưng không phải đường vòng M1/I11.

| bất biến / mục tiêu | kết luận trong phạm vi đã đo |
|---|---|
| I1/I2/I8/I10 | Authority/lease/canon không đổi trong diff; hồi quy r812 kiểm các trường/nguồn. H âm sai generation bị rc11. vua-p3 dùng P3 từ H pending và neo đúng generation/pending_sha. Không đo lease hay GitHub thật online. |
| I3/M1 | Schema optional bang_noi kiểm chung; nguồn/đích P3 và nguồn đã rời vòng kiểm tại record-review. Còn lỗi ngữ nghĩa đích nguồn-rỗng ở ba cửa khác như P2 đã ghi. Tập chọn P3 rỗng bị rc2; finding còn mở rỗng hoàn tất được. |
| I4 | Đầu vào map lỗi và vua-p3 sai giữ nguyên byte, kể cả vua-p3 tại trần same-failure. Ngoại lệ là P2 đích thiếu. Vòng hợp lệ không giảm/vòng3 ghi reviews, tăng rounds, đóng attempt, tiêu thụ call và lưu blocked_vong_p3 trước rc3. |
| I5 | vua-p3 gọi cùng _xet_dung và đăng ký CUA_DI_TIEP; mutant bỏ đăng ký bị bắt. Cửa khép review vẫn ghi kết quả. Không thêm máy xét dừng song song. |
| I6 | Quyền p3 thay quyền ci-do cũ, đúng tuple trên head mới. Quyền p3 không dùng để mở connector từ running (rc8/nguyên byte). chu-kho-duyet cho_phep_va tiêu thụ quyền connector như cũ. Tiêu thụ quyền tại cửa đẩy thuộc #816. |
| I7 | r813/r834 và M4 kiểm kho/PR/head, app/workflow/job, run/attempt mới nhất, refs đủ/đúng dạng. Không truy cập CI thật. |
| I9 | Đường non-ADR giữ dem=ids; ca đường lease cũ và hồi quy đạt. Chế độ ADR trong fixture tự dựng, không suy thành đã kích hoạt ngoài đời. Tương thích counts cũ là nợ P3 theo chủ kho. |
| I11/M2 | P3 bị loại khỏi reviews.finding_ids và history.mo_lai.finding_ids; _load tái dựng counts nhất quán, state probe reload rc0. Hai chuỗi lineage cũ và các cửa nối lại bị chặn. |
| M2: verdict âm và sự kiện xen | changes_requested toàn-P3 lặp 2→2 bị rc3; giảm2→1 rc0/running, counts{}. vua-p3→begin→void→review cùng lớp vẫn rc3. connector→chu-kho-duyet→review tạo mốc mới theo cơ chế công bố vì có mo_lai. Vòng2 sạch rc0, k2/1→0; vòng3 bị suite bắt. |
| M4 | Cả hai ca nợ #813 và mutant đúng chốt đạt. Chốt (b) là không có begin_attempt sau mo_lai cuối tại dòng2966; void không xóa dấu begin. Không sửa mã sản phẩm M4 trong diff. |

`tu: []` khai **đích có thật** là lớp mới C đồng thời reviewer khai A/B đã hết vẫn được nhận2→1; cùng slug P3 nâng P2 được ghi1→0 nhưng state running/changes_requested, chưa approve. Theo mô hình tin cậy H, phân lớp/hạng và xác nhận đã sửa là việc reviewer; không tạo finding chỉ vì máy không chứng minh được mã đã sửa. Trường hợp P2 được báo khác ở điều kiện đo được ngay trong H: đích missing-x **không có trong chính bang_lop**, nên không cần suy ý reviewer hoặc đọc mã để chứng minh vi phạm.

**Định danh, phạm vi, lệnh và giới hạn.** Reviewer độc lập Codex/OpenAI, họ openai, shell Linux qua công cụ, transport machine; executor Claude theo lease bản chép, họ claude. Packet #814 revision3 generation2, sensitive, assurance_target cross_approved. Serving model/effort/session và launcher attestation codex_cli không được đo độc lập; không tự tạo receipt assurance, không suy danh tính model từ actor GitHub. Không kế thừa context executor; verdict trước là lịch sử finding, handoff #813 dùng cho M4.

Đã đọc toàn bộ prompt.snapshot. Theo chỉ thị trực tiếp, đường tương đối lấy từ cwd, SRC=src, OUT=out. Đã đọc **toàn bộ hunk** diff 7f19424→24f6a73 và 4adbf92→b35a7e4, cả product/test, cùng các đường load/save/review/begin/void/rescue/H/CI/connector/checkpoint/parser liên quan. [FULL.diff](FULL.diff), [FIX.diff](FIX.diff).

Tự xác minh bốn SHA256: hai đặc tả dòng3; verdict lượt2 `d2459a3672a0b3de757323fc1a86bb0346637655e64f775ab3156df45a29bc0a`; lượt1 `8ca0f12346366fd9efde9a445923d2c7e7bfc98358fb2a1a05989de6bc62aea2`. HEAD đúng dòng2; tree `0f4d202ab6a265f968af29e217e7960c45613517`; origin/master `7f19424478616b2c5d0a0c7f26839e1d1c41261b`. Clone thường, .git là thư mục, không nông, detached. Base là tổ tiên head rc0. Base lease09db703 là mốc lịch sử, không bị nhầm với base review. Numstat product+89/−6, test+113/−6: **202 dòng thêm, hai đường dẫn**, dưới450; diff-check rc0. Handoff trong lease chỉ ở nhánh lease, không trong diff PR. [IDENTITY.json](IDENTITY.json).

Môi trường: PYTHONDONTWRITEBYTECODE=1, TMPDIR=out/tmp, GIT_CONFIG_GLOBAL=/dev/null, GIT_CONFIG_SYSTEM=/dev/null, GIT_OPTIONAL_LOCKS=0, GIT_ALLOW_PROTOCOL=file; copy core.abbrev=7. Fetch/push/ls-remote của fixture chỉ trỏ kho bare riêng dưới OUT, không mạng/GitHub và không push SRC/remote thật. Đã đọc chon.py cùng logic main mục3; runner tái dùng chay_suite, phân loại và đối chứng, thêm kiểm tập chọn khác rỗng/ca đích tồn tại/tên duy nhất/neo thay duy nhất, giữ toàn văn thông điệp.

| command | rc | bằng chứng dương / kết quả |
|---|---:|---|
| `python -B out/bootstrap.py` | 0 | 4 hash khớp, exact head/tree/ref, ancestry, sạch, clone đầy đủ, đúng write set. |
| `python -B -W ignore out/run_review.py baseline_r814 '^r814_'` | 0 | 30/30 PASS. |
| `python -B -W ignore out/run_review.py baseline_regression '^r81[23]_|^r834_|^stdout_cp'` | 1 do logger reviewer | 255 ca PASS, một lỗi UnicodeEncodeError khi logger ghi surrogate trong argv; không phải lỗi sản phẩm. |
| `python -B -W ignore out/run_review.py logging_recheck '^r812_r6_receipt_native$'` | 0 | 1/1 PASS sau sửa logger JSON ensure_ascii=True; cùng product, không sửa test. Tổng hợp256/256 tại REGRESSION_VERIFIED.json. |
| `python -B -W ignore out/run_review.py mutants` | 0 | 31/31, 34 target GIET, 93 đối chứng PASS, không tín dụng giả. |
| `python -B -W ignore out/run_review.py gates` | 0 | doctrine-scan rc0: 10 tệp/0 chỗ chép; adr-song rc0: 55/55, ngoại lệ0016 có sẵn. |
| `python -B -W ignore out/probes.py` lần đầu | 1 do runner reviewer | Helper bỏ bang_noi khi giá trị None; probe định đo null thực tế gửi vắng trường. Giữ log; không tính làm finding hay PASS. |
| `python -B -W ignore out/probes.py all probes_final` | 0 | 40 kịch bản hoàn tất, 445 bước CLI có trace; rc/state sai đặc tả đã ghi thành P2/nợ P3, không gọi toàn bộ là PASS. |
| `python -B -W ignore out/boundary_probes.py` | 0 | Hai khai mới hợp lệ accepted; vòng2 sạch k2/1→0, status rc0. |
| `python -B -W ignore out/extra_mutations.py` | 1 do cùng logger trước sửa | A/B riêng đúng; 288 ca PASS, một lỗi logger surrogate. |
| `python -B -W ignore out/run_review.py logging_recheck_mutant '^r812_r6_receipt_native$' out/extra_mutations/first-map-only/packet_loop.py` | 0 | 1/1 PASS; hợp nhất mutant sống **289/289** ca đã chọn, gồm ba đối chứng khác họ. EXTRA_MUTANT_VERIFIED.json. |
| `python -B out/make_audit.py` | 0 | 30 ca r814 đều có mutant, 31/34/93; giữ từng AssertionError và mỏ neo/thay. |
| `python -B out/finalize.py` | 0 | Tổng hợp và xác minh mọi kết quả, inventory SRC không đổi, exact head/tree/ref/worktree/index. |

Hai lỗi instrumentation đã giữ log gốc và recheck riêng, không gán cho sản phẩm, không lấy làm tín dụng mutant. Tập mutant mới sống chỉ được khẳng định trên **289 ca đã chọn**, không suy thành toàn bộ repository. [SUMMARY.json](SUMMARY.json), [REGRESSION_VERIFIED.json](REGRESSION_VERIFIED.json), [EXTRA_MUTANT_VERIFIED.json](EXTRA_MUTANT_VERIFIED.json).

Snapshot SRC sau preflight và cuối: **7420→7420 tệp, 0 delta byte/mode**, gồm tracked/untracked/ignored và .git. Đây là so hai mốc, không phải giám sát liên tục mọi lần ghi. Sandbox thực tế workspace-write; mọi script/probe/mutant/fixture/report do reviewer tạo ở OUT. [SOURCE_INTEGRITY.json](SOURCE_INTEGRITY.json), [bản ghi tăng dần](VERDICT-progress.md), [băm hiện vật](ARTIFACTS.json).

`not_run`: full suite `python .claude/dev/packet_loop_test.py` (~60 phút; assignment ưu tiên chọn lọc), mutants ngoài tập đã nêu, CI/thu-hoi/lease readback online, Windows thật, bare Ruff lint và Ruff pin/probe contract. Không nhận lời khai full-suite executor làm kết quả độc lập. `r812_r4_own_parent` loại trước chạy theo chỉ thị. Hướng thử đường dẫn thoát cây chỉ mô tả bằng lời: receipt/lease/checkpoint/liên kết dẫn ngoài phạm vi phải bị từ chối trước truy cập ngoài cây, state nguyên byte; không tự soạn payload đó.

#977, generation kế tiếp #815, ghi đẩy/tiêu thụ quyền tại cửa đẩy #816 và kích hoạt ADR-0054 ngoài phạm vi. Không phát hiện mâu thuẫn buộc sửa parser/hợp đồng các lệnh cũ; P2 còn lại nằm trong yêu cầu kiểm trường bảng nối mới của M1.
