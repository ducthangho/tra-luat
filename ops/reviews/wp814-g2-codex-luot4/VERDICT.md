Verdict: approve
Reviewed commit: 5a5c5c1f687f74b73301fe161e332ae6b4c0f779
Spec sha256: 39b4288959f3889c6c3aad2d24b355c1c02b1462a8854c6a5b00677e81a7ce73; Chung sha256: 4e3d1e1b3f6a0b60b96ad7b70f0ece97eca4bb3d6d10defeab1cd24ac6d1cbf0

**Kết luận lượt 4: 0 P0/P1/P2 còn mở; 2 lớp P3.** `receipt-map-validation-skipped` đã được vá thật, và biểu hiện `first-map-only` của lượt 3 đã có ca bắt đột biến. Ngưỡng approve là không còn P0/P1/P2 theo prompt. Verdict chỉ neo commit dòng 2; không cấp quyền push, merge, land hay kích hoạt ADR-0054.

| slug | hạng P0–P3 | biểu hiện file:dòng | phép đo/tái hiện đã chạy | hướng vá |
|---|---|---|---|---|
| `legacy-p3-failure-counts-retained` | **P3 theo quyết định chủ kho**, giữ slug | `.claude/dev/packet_loop.py:672`, `:1207`, `:1229` | Blob base20a2e2b tạo state qua CLI: approve a-x:P3 có finding-id lưu count1. Candidate vua-p3 rồi cùng a-x lên P2: count2/rc3/blocked. State mới bằng candidate: count1/rc0/running. Cả hai ghi vòng k1/1→0 và status rc0. | Owner **#816**. Giữ nợ, không migration ở #814. Trước kích hoạt kiểm dữ liệu thực và quyết định riêng về lịch sử P3 có bằng chứng. |
| `r814-mutation-evidence-incomplete` | **P3**, biểu hiện mới `duplicate-destination`; `first-map-only` đã đóng | `.claude/dev/packet_loop_test.py:9060`, `:9116`; chốt sản phẩm `.claude/dev/packet_loop.py:3064` | Mutant chỉ bỏ `and len(set(den)) == len(den)` sống **312/312 ca đã chọn**. A/B accept với hai hàng khai cùng đích: candidate rc11/`bang-noi`/nguyên byte; mutant rc0/accepted. Oracle riêng AssertionError; status cả hai rc0. | Owner executor **Claude #814**, chủ kho định tuyến nợ. Thêm ca đích lặp và mutant gỡ đúng kiểm duy nhất đích; giữ predicate sản phẩm đang đúng. Không yêu cầu mở thêm vòng vá #814 chỉ vì nợ P3 này. |

**Lý do phân hạng và slug lặp.** Nợ legacy được prompt chỉ định giữ P3, owner#816; lần đo này không phát hiện state ADR-0054 vận hành thật trong SRC. Fixture nâng cấp tái hiện hành vi cũ, không phải phát hiện dữ liệu vận hành thật để tự nâng lại P2. `duplicate-destination` là đột biến độ phủ **mới**, mã sản phẩm từ chối đúng ở A/B; không phải ca nghiệm thu bắt buộc bị thiếu, cũng không phải mutant đã báo ở lượt trước còn sống. Vì vậy giữ P3 theo luật chủ kho. Giữ slug lớp `r814-mutation-evidence-incomplete` theo nguyên nhân, không đổi slug để che lịch sử; biểu hiện cũ đã đóng, biểu hiện mới được ghi riêng. Không xin thêm ngoại lệ same_failure_limit. Ngoài nợ legacy đã được chuyển rõ sang #816, không có slug cũ tái diễn kèm hành vi sai trên candidate; lượt vá bắt buộc #814 có thể dừng theo ngưỡng được giao.

**ĐỐI CHIẾU LƯỢT TRƯỚC.**

| lớp / biểu hiện | trạng thái | bằng chứng đo độc lập |
|---|---|---|
| `receipt-map-validation-skipped` | **ĐÃ VÁ THẬT** | Dựng lại chính ma trận lượt3: nguồn rỗng, đích missing-x không có trong bang_lop ở ci-do, connector, accept đều rc11/`bang-noi`/nguyên byte. record-review cùng sai cũng bị từ chối. Đối chứng bang_noi rỗng được nhận; đích P3 có thật được nhận tại ci-do/accept/record-review. |
| `r814-mutation-evidence-incomplete` · `first-map-only` | **ĐÃ VÁ THẬT biểu hiện cũ** | Accept có hai lớp c-d/e-f, đủ refs và quyết định; hàng1 khai mới c-d, hàng2 nối old-x→e-f. Candidate rc11/nguyên byte, mutant chỉ kiểm hàng1 rc0/accepted. Mutant này bị cả ba ca `r814_rr_nhieu_hang`, `r814_ci_nhieu_hang`, `r814_accept_nhieu_hang` bắt bằng AssertionError đúng lý do. Lớp còn biểu hiện mới P3 đích lặp trong bảng trên. |
| `legacy-p3-failure-counts-retained` | **CHƯA VÁ, giữ nợ P3 theo chủ kho** | Upgrade/fresh từ CLI thật tái hiện count2/count1; cùng vòng k1/1→0. Không sửa migration. |
| Lịch sử `finding-lineage-counter-reset` | giữ **ĐÃ VÁ THẬT** | P2 a-b count1→approve sạch→mo-lai ci-do hoặc connector với bảng nối a-b→c-b đều rc11/nguyên byte, counts chỉ a-b:1. Hai đối chứng giữ a-b đều rc3/blocked/count2. |
| Lịch sử `p3-mapping-namespace-collision` | giữ **ĐÃ VÁ THẬT** | `r814_noi_chuoi` từ chối; mutant bỏ yêu cầu nguồn rời vòng này bị bắt. Gộp A/B→C áp nối hai phía thành1→1/blocked. |
| Lịch sử `p3-reopen-enters-failure-counter` | giữ **ĐÃ VÁ THẬT với sự kiện mới** | CI P3 rc0/running/counts{}; r814_mo_lai_dem_p3 bị oracle counts bắt; review P3 và P2 có ca đối chứng riêng. |
| Lịch sử `legacy-p3-milestone-lost` | giữ **ĐÃ VÁ THẬT phần mốc** | `r814_state_cu_giu_moc` và mutant đạt; upgrade thật từ blob base vẫn tính vòng k1. Nợ counts lịch sử được giữ ở slug riêng. |
| Lịch sử `new-command-codepage-matrix-incomplete` | giữ **ĐÃ VÁ THẬT** | stdout_cp1252/cp1258 PASS, có vua-p3 thành công và stdout. Đo Linux với biến môi trường codepage, không phải Windows thật. |
| M4 · `r813-mutation-evidence-incomplete` | **ĐÃ VÁ THẬT cả hai biểu hiện được giao** | Mixed check_refs rc11/đúng dạng/nguyên byte; CI→begin→void→connector rc8/chưa mở lượt mới/nguyên byte. Mutant đúng chốt của mỗi ca đều bị bắt. |

**Ma trận cửa đọc H và bản vá A'.**

| cửa | đích không có (`tu: []`) | đối chứng hợp lệ | hàng đầu hợp lệ, hàng sau sai |
|---|---|---|---|
| record-review | rc11/`bang-noi`/nguyên byte | giảm2→1, bang_noi=[] hoặc khai mới đích P3 có thật: rc0/approved_pending | rc11/nguyên byte; mutant chỉ hàng1 bị oracle bắt dù sau đó bị chốt vòng chặn rc3 |
| mo-lai ci-do | rc11/`bang-noi`/nguyên byte, đo cả bang_lop P1 như lượt3 và P3 | bang_noi=[] hoặc khai mới ci-gate:P3: rc0/running/counts{} | rc11/nguyên byte; mutant rc0, ca bắt đúng |
| mo-lai connector | rc11/`bang-noi`/nguyên byte | bang_noi=[]: rc0/cho_chu_kho | không có hàng không rỗng hợp lệ để đặt đầu: bảng lớp connector chỉ P0–P2, trong khi đích nối phải P3 |
| accept / _slug_connector | rc11/`bang-noi`/nguyên byte | khai mới một hoặc hai đích P3 có thật, đủ refs/quyết định: rc0/accepted | đích thiếu hoặc nguồn nối ở hàng2 đều rc11/nguyên byte; mutant rc0, ca bắt đúng |

Null/sai lý do/nguồn nối ngoài record-review cũng bị từ chối rc11/nguyên byte. Việc `tu: []` trỏ đích P1 có thật ở connector bị từ chối là đúng cơ chế A' được giao, không dùng ca ấy làm đối chứng dương. Mỗi state cuối của 47 probe đều reload qua `status` rc0. Xem [probes.py](probes.py), [kết quả](probes/results.json), [trace từng CLI](probes/trace.jsonl).

Đã tự lần các call site `_du_dieu_kien_approve`, nơi đọc YAML, `bang_lop`, `bang_noi` và `bien_nhan_approve`. Các cửa chuyển state nhận bảng lớp/nối từ tệp H đều qua cùng vị từ: record-review:1199, _slug_connector:2900, mo-lai:2973. `_kiem_noi` có một caller ở:2751. `_vong_p3` không còn kiểm tham chiếu rải; chỉ nhận diện vòng, kiểm slug mới không qua nối và đếm lớp. `vua-p3` đọc ảnh pending đã xác thực; `chu-kho-duyet` đọc checkpoint; `record-lease` đọc lease. Lệnh báo cáo `bien-nhan`:2138 đọc receipt để đếm hiện vật, không dùng bảng lớp/nối, không chuyển state hay tăng finding_counts; không phải đường lách M1/I11. Không thấy cửa đọc bảng nối cấp quyền đi đường riêng.

**Nợ kiểm thử mới — hướng vá cụ thể.** Nền accept hợp lệ có lớp c-d:P3, connector ref đúng và đúng một quyết định P3. Bảng nối có hai hàng cùng `{tu: [], den: c-d, ly_do: reviewer class mapping}`. Candidate từ chối rc11 trước ghi; bỏ riêng kiểm duy nhất đích ở:3064 thì accepted. Mỏ neo/thay nằm tại [mutation.json](extra-mutants/duplicate-destination/mutation.json); A/B và oracle đã chạy trong [probes.py](probes.py). Tập có sẵn đã đo với mutant gồm r812/r813/r834/r814, codepage, 17 ca doctrine và hai đối chứng ac18/ac19: 312 PASS, không skip hay CLI sập. Đây là phạm vi đã đo, **không** khẳng định toàn bộ repository đã được chạy dưới mutant.

Vá rẻ nhất ở `.claude/dev/packet_loop_test.py`, cạnh các ca bảng nối: dựng đối chứng một hàng hợp lệ; thêm đúng một hàng lặp đích; đòi rc11, `bang-noi`, state nguyên byte; khai mutant bỏ duy nhất `and len(set(den)) == len(den)`. Có thể thêm đối chứng hai đích khác nhau để chống siết quá mức. Rủi ro khi dựng ca: lặp nguồn, đích không có, refs/quyết định thiếu hoặc vòng P3 không giảm có thể che chốt đích lặp; dùng accept với `tu: []` tránh các nhiễu đó. Không cần đổi mã sản phẩm đang đúng.

**Nợ legacy — hướng xử lý theo #816.** Blob base20a2e2b được lấy từ git của bản sao, không chèn tay counts/history. Nếu chủ kho sau này cho phép di trú, phân biệt lượt P3 có bằng chứng với lượt P0–P2 thật; giữ audit và cập nhật sổ finding_ids cùng counts để `_load` vẫn nhất quán. Ca khóa là upgrade P3 có finding-id rồi cùng slug lên P2, đối chứng state mới và reload. Rủi ro: xóa counts đơn độc làm hỏng invariant findings; suy hạng không có bằng chứng có thể xóa lỗi nghiêm trọng. Quét JSON trong SRC không thấy state có `luat_adr0054:true` cùng state/reviews: [real-state-scan.json](real-state-scan.json). Không lấy việc quét này làm khẳng định không có dữ liệu ở nơi khác.

**Từng ca bắt buộc trong nghiệm thu.** Nền r814 **37/37 PASS**. **30 mutant / 47 lượt ca đích GIET / 90 lượt đối chứng khác họ PASS**. Tất cả target là AssertionError tại oracle nghiệp vụ; không có BO_QUA/TIN_DUNG_GIA. Đã đọc cả tên ca, lớp lỗi và thông điệp; hai oracle quyền được đối chiếu với tuple trong state, không chỉ dựa vào rc. [MUTATION_AUDIT.md](MUTATION_AUDIT.md) liệt kê mọi ca và mọi target, cùng mỏ neo/thay và thông điệp đầy đủ trong [mutants/results.json](mutants/results.json).

| yêu cầu bắt buộc | ca r814 (nền PASS) | mutant bị chính ca đó bắt | bằng chứng đúng lý do |
|---|---|---|---|
| {A,B}→{B} hợp lệ | r814_ab_b_hop_le | r814_giam_hai_lop | AssertionError đòi0/được3; siết sai mức giảm2→1 |
| biểu hiện trùng, lớp2→2 | r814_bieu_hien_trung | r814_khong_giam_van_qua | đòi3/được0; baseline ghi blocked_vong_p3 2→2 |
| đổi tên không bảng nối | r814_doi_ten_khong_noi | r814_doi_ten_tu_do | đòi11/được0; baseline lý do không qua bảng nối, nguyên byte |
| gộp thuần sau nối1→1 | r814_gop_qua_noi | r814_noi_chi_vong_nay | đòi3/được0; baseline1→1/blocked |
| mốc→vòng1 không giảm | r814_moc_vong1_khong_giam | r814_vong1_mien_so | đòi3/được0 |
| vòng3 | r814_vong_3 | r814_vong_3_lot | bước6 đòi3/được0; baseline vòng3,1→0 vẫn blocked |
| P3 không đẩy same-failure | r814_p3_khong_dem | r814_p3_vao_dem | counts đòi{}, được a-b:1 |
| đối chứng P2 vẫn đếm | r814_p2_van_dem | r814_bo_ca_p2 | counts đòi a-b:1, được{} |
| tự chọn vá P3 đi được | r814_vua_p3_di_duoc | r814_vua_khong_ghi_quyen | oracle tuple: None thay vì (p3,1,pending_sha) |
| tập chọn rỗng | r814_vua_p3_rong | r814_vua_tap_rong | đòi2/được0; baseline ít nhất một, nguyên byte |
| slug ngoài biên nhận | r814_vua_p3_ngoai_bien_nhan | r814_vua_ngoai_bien_nhan | đòi11/được0; baseline không phải lớp P3, nguyên byte |
| xóa hết P3 | r814_xoa_het_p3 | r814_rong_la_khong_giam | đòi0/được3; mutant đếm tập sạch thành không giảm |
| changes_requested sai generation | r814_am_generation_khac | r812_bo_generation | đòi11/được0; baseline lỗi `generation`, nguyên byte |
| M4(a): check_refs hợp lệ trộn null | r814_check_refs_tron_null | r814_refs_bo_do_dai | đòi11/được0; baseline đúng dạng/nguyên byte |
| M4(b): CI→begin→void→connector | r814_ci_void_connector | r814_void_khoi_phuc_quyen_ci; r813_quyen_ci_qua_luot_moi | cả hai đòi8/được0 ở bước3; baseline chưa mở lượt mới/nguyên byte |
| đối chứng r812/r813/r834 | 148 r812 + 43 r813 + 63 r834 | không chạy mọi mutant lịch sử | **254/254 PASS**, cộng2 codepage thành256/256; r812_r4_own_parent loại trước chạy theo chỉ thị đường dẫn |

Các ca bổ sung nguồn/đích sai hạng, nguồn lặp, nối chuỗi, lý do rỗng, bảng nối ở từng cửa, giữ mốc cũ, thay quyền, P3 ở ci-do và vua-p3 xét dừng đều PASS và có mutant bị bắt. `r814_bo_kiem_noi_chung` bị cả10 ca đích bắt; `r814_noi_dich_thieu_lot` bị4 cửa bắt; `r814_noi_chi_hang_dau` bị3 ca nhiều hàng bắt. Riêng rr_nhieu_hang trên mutant nhận đầu vào sai rồi bị chốt vòng chặn rc3: đây vẫn là lỗi nghiệp vụ đúng chốt (phải rc11 và nguyên byte), không phải tín dụng giả do CLI sập. Không đòi mutant bỏ-riêng-từng-cửa vì A' chủ ý có một lời gọi chung.

Chốt M4(b) là điều kiện không có `begin_attempt` kể từ `mo_lai` cuối tại packet_loop.py:2966; void không xóa dấu begin. Hai mutant bắt đúng chốt đó, không có thay đổi sản phẩm M4 trong diff. Đã đối chiếu nợ với handoff#813 và verdict lượt6 được cung cấp; không nhận kết quả executor làm bằng chứng riêng.

**Bất biến I1–I11 và M1–M4 trong phạm vi thay đổi.**

| bất biến | kết luận và giới hạn |
|---|---|
| I1/I2/I8/I10 | Authority lease/canon không đổi; các ca r812 hồi quy đạt. H âm sai generation bị từ chối. vua-p3 dùng P3 từ H pending, neo generation/pending_sha; không suy quyền từ readback R. Không xác minh lease/comment GitHub thật online. |
| I3/M1 | Một validator kiểm schema, lý do, nguồn/đích duy nhất, đích P3 thật, nguồn P3 vòng trước đã rời vòng hiện tại. Ngoài record-review không có truoc, nên nguồn khác rỗng bị chặn. Tập chọn rỗng không đạt; tập finding sạch được phép rỗng. |
| I4 | Mọi probe đầu vào sai map/vua-p3 giữ state nguyên byte, kể cả vua-p3 tại ngưỡng same-failure. Vòng không giảm/vòng3 là kết quả hợp lệ: ghi review, tăng rounds, đóng attempt, tiêu thụ codex-call rồi blocked_vong_p3/rc3; status đọc lại được. |
| I5 | vua-p3 gọi cùng _xet_dung và thuộc CUA_DI_TIEP. Mutant bỏ đăng ký bị r814_vua_p3_xet_dung bắt. Không thêm máy xét dừng song song; review là cửa khép vẫn ghi kết quả. |
| I6 | Quyền p3 thay ci-do trên headA bằng (p3,generation,headB); mutant giữ quyềnA bị oracle tuple bắt. Quyền p3 không mở connector từ running: rc8/nguyên byte. chu-kho-duyet cho_phep_va tiêu thụ quyền connector như cũ. Tiêu thụ quyền tại cửa đẩy thuộc#816. |
| I7 | r813/r834 và M4 kiểm refs, định danh checks, head/PR/kho, run/attempt mới nhất; dùng fixture bare cục bộ, không CI thật. |
| I9 | Nhánh non-ADR giữ dem=ids; đường lease cũ và toàn bộ tập hồi quy được phép chạy đạt. State ADR cũ giữ mốc approve từ H pending; counts lịch sử là nợ P3 được chuyển#816. Không tuyên bố full-suite N/N. |
| I11/M2 | Slug từ H; P3 bị loại ở review.finding_ids, history.record_review.finding_ids và mo_lai.finding_ids, nên _load tái dựng counts nhất quán với sự kiện mới. Nối P0–P2 không lách được same_failure ở hai cửa mo-lai. |
| M2, verdict âm và sự kiện xen | changes_requested toàn-P3: lặp2→2 bị rc3, giảm2→1 rc0/running/counts{}. vua-p3→begin→void→review không giảm vẫn blocked. Checkpoint cho_phep_day không reset vòng. ci-do hoặc connector→chu-kho-duyet xen giữa tạo mốc mới theo cơ chế đã công bố. Vòng2 xóa hết đạt k2/1→0; vòng3 bị chặn. |
| M4 | Hai ca bắt buộc và cả mutant riêng/dùng chung đạt, không còn nợ hai biểu hiện#813 trong phạm vi giao. |

`tu: []` khai đích C có thật, đồng thời reviewer khai A/B đã hết, vẫn được nhận2→1. Cùng slug P3 lên P2 được ghi1→0 nhưng **running/changes_requested**, counts1; không trở thành approve. Đây là phân lớp/hạng do reviewer H chịu trách nhiệm theo I11 và mô hình tin cậy; máy không có oracle chứng minh mã đã được sửa. Không gán lỗi chỉ vì máy tin khai báo phân lớp hợp lệ. Ngược lại, đích không tồn tại trong chính bang_lop hoặc bảng nối khai cùng nguyên nhân nhưng tách bộ đếm là điều kiểm được ngay từ H, và các phản chứng ấy nay bị chặn.

**Định danh và phạm vi.** Đã đọc toàn bộ prompt.snapshot; đường tương đối tính từ cwd theo chỉ thị trực tiếp, SRC=src, OUT=out. Review không lọc toàn bộ [diff4488444→5a5c5c1](full-diff.txt) và [vá24f6a73→f029321](patch-f029321.txt), cả product/test, cùng các đường load/save/review/begin/void/H/CI/connector/checkpoint/xét dừng/parser liên quan. Hai blob trong write set không đổi giữa f029321 và head merge.

HEAD đúng dòng2; tree `39d5d5ffa25a2e349bec7d6afc363f42e572e1c8`; origin/master=`44884446f71c89e25f9a72ac58e4f597db63c1ba`. Clone thường, .git là thư mục, không nông, detached, sạch. Base là tổ tiên head rc0. Base lease09db703 là mốc lịch sử; không nhầm với base review. Numstat product+85/−6, test+125/−6: **210 dòng thêm, đúng2 đường dẫn, ≤450**; diff-check rc0. Handoff trong lease chỉ dành nhánh lease, không nằm trong diff PR.

Hai SHA256 đặc tả khớp dòng3. Verdict lượt1 `8ca0f12346366fd9efde9a445923d2c7e7bfc98358fb2a1a05989de6bc62aea2`; lượt2 `d2459a3672a0b3de757323fc1a86bb0346637655e64f775ab3156df45a29bc0a`; lượt3 `9dc9d5a696f9fee205e964b582cf6f4b0c0a23a304250fde4c1e26fee1fd1c7f`: đều băm lại khớp. [IDENTITY.json](IDENTITY.json).

Reviewer độc lập Codex/OpenAI, họ openai; executor Claude theo gói, họ claude; packet#814 revision3 generation2, sensitive, assurance_target cross_approved. Thực tế có shell Linux qua công cụ/API, transport machine. Không có attestation độc lập cho serving model/effort/session hoặc launcher codex_cli trong phép đo này; không tự sinh receipt assurance, không suy model từ actor GitHub. Không kế thừa context executor. Verdict trước dùng để theo dõi finding, không thay kiểm thử độc lập.

Mọi fixture/script/mutant/bản sao/report do reviewer tạo ở OUT. PYTHONDONTWRITEBYTECODE=1, TMPDIR=out/tmp, GIT_CONFIG_GLOBAL=/dev/null, GIT_CONFIG_SYSTEM=/dev/null, GIT_OPTIONAL_LOCKS=0, GIT_ALLOW_PROTOCOL=file; core.abbrev của bản sao=7. Các git fetch/push/ls-remote của fixture chỉ trỏ kho bare riêng dưới OUT; không mạng, không GitHub, không push SRC/remote thật. Đã đọc chon.py và logic main mục3; runner tái dùng chay_suite, phân loại đột biến/tín dụng giả và đối chứng, thêm kiểm tập chọn không rỗng, tên ca duy nhất, ca đích tồn tại, neo thay duy nhất, log toàn văn stderr/rc/hash state.

| command đã chạy | rc | bằng chứng dương / kết quả |
|---|---:|---|
| git/hash preflight và kiểm cuối | 0 (symbolic-ref -q HEAD=1 đúng detached) | head/tree/ref/spec/verdict/ancestry/write set khớp, source không đổi; IDENTITY.json |
| `python -B -W ignore out/audit.py baseline_r814 '^r814_'` | 0 |37/37 PASS |
| `python -B -W ignore out/audit.py baseline_regression '^r81[23]_\|^r834_\|^stdout_cp'` | 0 |256/256 PASS, loại1 ca đường dẫn trước chạy |
| `python -B -W ignore out/audit.py mutants` | 0 |30 mutant,47 target GIET,90 đối chứng PASS,0 tín dụng giả |
| `python -B -W ignore out/probes.py` | 0 |47 kịch bản, status tất cả rc0; rc nghiệp vụ khác0 được kiểm với oracle tương ứng, không coi toàn bộ là phép approve |
| `python -B -W ignore out/audit.py extra_first_map_only '^r814_(rr_nhieu_hang\|ci_nhieu_hang\|accept_nhieu_hang)$' out/extra-mutants/first-map-only/packet_loop.py` | 1 **đúng mong đợi** |3/3 ca đỏ bằng AssertionError nghiệp vụ; mutant cũ bị giết |
| `python -B -W ignore out/audit.py extra_duplicate_destination '^r81[234]_\|^r834_\|^stdout_cp\|^doctrine_' out/extra-mutants/duplicate-destination/packet_loop.py` | 0 |310/310 PASS trên mutant mới ⇒ thiếu ca bảo vệ chốt; A/B riêng bắt lỗi mutant |
| `python -B -W ignore out/audit.py extra_duplicate_controls '^ac18_nfkc_hai_cham_toan_rong$\|^ac19_oan_claude_md_master$' out/extra-mutants/duplicate-destination/packet_loop.py` | 0 |2/2 đối chứng khác họ bổ sung PASS; tổng312 ca phân biệt của mutant |
| `python -B out/review-src/.claude/dev/packet_loop.py doctrine-scan --root out/review-src` | 0 |sạch,10 tệp,0 chỗ chép doctrine |
| `python -B out/review-src/.claude/dev/packet_loop.py adr-song --root out/review-src` | 0 |55 ADR/55 dòng, khớp1–1; ngoại lệ0016 có sẵn |
| `python -B out/make_audit.py` | 0 |mọi37 ca r814 có mutant bị chính ca đó bắt; mọi47 target AssertionError |
| `python -B out/finalize.py` | 0 |kiểm kết quả, source inventory và toàn vẹn evidence; kết luận cuối |

Tổng nền chọn lọc **293/293 PASS**. Mutant mới sống312/312 chỉ được khẳng định trên tập đã đo. [SUMMARY.json](SUMMARY.json), [nền r814](baseline_r814/results.json), [hồi quy](baseline_regression/results.json), [mutant mới](extra_duplicate_destination/results.json), [đối chứng](extra_duplicate_controls/results.json).

Snapshot SRC trong quá trình review và khi kết thúc: **7502→7502 tệp,0 delta byte/mode**, gồm .git và tracked/untracked/ignored; đây là so hai mốc, không phải giám sát mọi lần ghi. [SOURCE_INTEGRITY.json](SOURCE_INTEGRITY.json). Bản ghi tăng dần được giữ tại [VERDICT-progress.md](VERDICT-progress.md); băm evidence tại [ARTIFACTS.json](ARTIFACTS.json).

`not_run`: full suite `python .claude/dev/packet_loop_test.py` (~60 phút; prompt ưu tiên chọn lọc); toàn bộ mutant ngoài tập đã nêu; CI/thu-hoi/lease/GitHub online; Windows thật; Ruff và contract pin/probe của Ruff. Không lấy lời khai full-suite của executor làm phép đo độc lập. `r812_r4_own_parent` loại trước chạy theo chỉ thị không soạn đường dẫn thoát cây, không tính là PASS. Hướng thử đó chỉ mô tả bằng lời: lease/receipt/checkpoint hoặc liên kết dẫn ngoài phạm vi phải bị từ chối trước truy cập ngoài cây và giữ state nguyên byte; không tự soạn payload.

#977, generation kế tiếp#815, ghi đẩy/tiêu thụ quyền tại cửa đẩy#816 và kích hoạt ADR-0054 ngoài phạm vi. Không phát hiện mâu thuẫn mới buộc sửa parser/hợp đồng accept, mo-lai hoặc chu-kho-duyet. Bản vá đang được review giữ các hợp đồng cũ và kiểm trường bảng nối mới theo cơ chế A' đã được giao.
