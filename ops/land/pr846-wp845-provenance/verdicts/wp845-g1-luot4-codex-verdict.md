verdict: approve
reviewed_sha: 7a39463e8b6c25d4811bcc9cd544b164e7ce53a7

Bản ghi tăng dần lượt 4/4, đã chốt approve. Các mốc 0–2 dưới đây giữ lịch sử phép đo; kết luận cuối và quyết định P3 ở sau. Reviewer độc lập OpenAI/Codex, executor theo assignment là Claude. Phạm vi: Spec và Standards/Security của packet #845; không gọi GitHub, không sửa `cay-kho/`, không push/merge/land. Mọi bản sao và đầu ra nằm trong `review-data/`.

Mốc 0: HEAD và SHA-256 `SPEC-r1.md` khớp assignment. Đọc Q1–Q4, diff, lịch sử finding lượt 3 và mã c16. Đang kiểm chứng A–Q bằng đột biến độc lập; chưa lấy 64/64 executor khai làm bằng chứng.

Mốc 1: `python -B review-data/run_ab.py` rc=0. Base: 15/15 CA, 37/37 đột biến. Head: 16/16 CA, 64/64 đột biến. Cả hai checker cây thật: rc=0, 12 ĐẠT, 28/28 miễn trừ, 0 vi phạm, 0 KHÔNG ĐO ĐƯỢC. `probe_mutations.py` rc=0: 27 mutant L6 đăng ký và 24 mutant reviewer thể hiện lỗi đọc Q1 đều GIET bằng rc=3/DO:c16; 3 mutant ngưỡng tùy ý còn sống. A–Q: suite trước tương ứng rc=0 → suite hiện tại rc=3, có phản chứng CLI riêng. Đang kiểm các miền hành vi và phân loại mutant sống, chưa chốt severity.

Mốc 2: `probe_behavior.py` sau sửa bộ sinh fixture rc=0, **496/496** khớp oracle Q1/phạm vi trên head và kỳ vọng base; 3 ca L4 được đo riêng rc=2. Lượt đầu của probe bị hỏng phương pháp: PyYAML tự sinh alias khi hai trường trỏ cùng đối tượng Python, dẫn tới 226 ca bị L4 chặn; giữ kết quả đó ở `behavior-*-initial-alias.json`, không tính thành lỗi sản phẩm hoặc bằng chứng kiểm L6. Bộ sinh hiện tại không phát alias cho dữ liệu Q1; ca alias L4 vẫn giữ nguyên. Ba mutant ngưỡng tùy ý qua đủ 16 CA (rc=0), từng phản chứng CLI vẫn head/mutant=1/0. Đếm Git blobs: mỗi vế 10 true, 5 thiếu thu_hoi_cuoi, nên P3 mẫu số 5/9 vẫn còn. Regex registry khớp stdout cả hai suite. Metadata launcher và header hiện hành đã đo được model/surface; chi tiết ở phần giới hạn cuối.

**Kết luận cuối: răng của c16 với L6 đã đủ để approve theo ngưỡng của prompt.** Không còn P0/P1/P2 mở trong phạm vi đã review. Toàn bộ 17 biểu hiện A–Q của P2 cũ đều bị giết đúng bằng `TinHieuChotCa`, không chỉ được bổ sung tên vào bảng executor. Bảy cách đọc sai Q1 bổ sung R–X cũng bị giết. Không phát hiện sai hành vi checker gốc trên 496 ca độc lập. Không đồng nhất kết quả này với chứng minh mọi YAML hoặc mọi đột biến đều được phủ.

Có **2 lớp P3 mở, 4 biểu hiện**: 3 biến thể ngưỡng tùy ý thuộc lớp `c16-thieu-rang-q1`, và số liệu 5/9 thuộc lớp `loi-khai-bang-chung-cu`. Quyết định cho từng P3: chấp nhận ghi nợ có owner và hướng xử lý bên dưới; không yêu cầu vòng sửa thứ năm. Các biểu hiện A–Q không bị hạ hạng để được approve: chúng đã được tái dựng và giết thật. Phần P3 mới chỉ ghi giới hạn hữu hạn, không cáo buộc checker hiện tại có các ngưỡng của mutant.

**Neo và phạm vi.** Nguồn đo: `preflight.json`, `identity-evidence.json`; đọc Git với `GIT_OPTIONAL_LOCKS=0`, ghim `core.abbrev=7` theo từng lệnh, không đổi config nguồn.

| Mục | Kết quả kiểm độc lập |
|---|---|
| Reviewed head | `7a39463e8b6c25d4811bcc9cd544b164e7ce53a7` |
| Reviewed tree | `43afc653cdf9ea3ceb0b6b3f04e6874e150e5455` |
| Base | `9f4a539b12d1d948817123d117f4bf2aedb1898f` |
| Lượt 1 / 2 / 3 | `c95bd7f80a45a592f3cb089149c0c23fb4df2317` / `fa4fb7ce98c56b56a2523bf8c2b6a6bc2fb98181` / `ecebffe9675d0952f3a0ab65eaa44087853a26bc` |
| Spec ngoài checkout | `SPEC-r1.md`, SHA-256 `a5a89622376495186ae265f18f4f6d1ce7e2b2e3b7613c61c2d96087a2c3af0b`, khớp |
| Diff / diff từ lượt 3 / numstat | Cả ba hiện vật giao kèm khớp byte với Git; diff lượt 3 chỉ tệp test |
| Q3 / write_set | Đúng 2 tệp: checker +19/-1, test +81/-0; tổng **+100/-1**, đạt ≤150 dòng thêm; `git diff --check` rc=0 |
| Checkout | Detached HEAD, status sạch; snapshot đầu gồm 4.878 mục, kiểm cuối ở cuối báo cáo |

**ĐỐI CHIẾU LƯỢT TRƯỚC — P2 `c16-thieu-rang-q1`, biểu hiện A–Q.** `test:` dưới đây là `cay-kho/ops/land_evidence_nguon_test.py`. Cột cũ→nay là rc của c16 trên cùng module mutant từ head hiện tại: cũ lấy suite ở lượt đã bỏ lọt (A–C: lượt 1; D–H: lượt 2; I–Q: lượt 3), nay lấy suite head. Baseline c16 gốc ở cả bốn suite đều rc=0. Các ca phản chứng được mô tả bằng lời; fixture, output đầy đủ, neo/thay và SHA-256 module nằm trong `mutation-results.json`, `probe_mutations.py`, `counterexamples/`.

| Biểu hiện / mutant độc lập | Trạng thái | c16 cũ→nay | Phản chứng CLI đã chạy: head/mutant | Chốt hiện tại |
|---|---|---:|---|---|
| A / `RV_A` — mọi→một | ĐÃ VÁ THẬT | 0→3 | Bookkeeping trộn mapping/chuỗi: 1/0 | test:313, ma trận cả hai trường |
| B / `RV_B` — bookkeeping chỉ cần truthy | ĐÃ VÁ THẬT | 0→3 | Bookkeeping mapping thay list: 1/0 | test:315, chép riêng hai tên trường ở test:36 |
| C / `RV_C` — chỉ đi ít tầng | ĐÃ VÁ THẬT | 0→3 | Dấu trong giá trị lồng nhiều mapping: 1/0 | test:321 |
| D / `RV_D` — dấu chỉ ở đầu chuỗi | ĐÃ VÁ THẬT | 0→3 | Dấu giữa câu: 1/0 | test:320 |
| E / `RV_E` — mặc định hợp lệ khi thiếu post_merge_checks | ĐÃ VÁ THẬT | 0→3 | Bỏ hẳn post_merge_checks: 1/0 | test:313–319, sentinel vắng |
| F / `RV_F` — bookkeeping rỗng được qua | ĐÃ VÁ THẬT | 0→3 | Bookkeeping list rỗng: 1/0 | test:313 |
| G / `RV_G` — chỉ xem phần tử cuối bookkeeping | ĐÃ VÁ THẬT | 0→3 | Chuỗi rồi mapping trong bookkeeping: 1/0 | test:313 |
| H / `RV_H` — bỏ guard có landed | ĐÃ VÁ THẬT | 0→3 | Status mapping chỉ có merged: 0/1, KeyError ở mutant | test:323, :330–334 |
| I / `RV_I` — chấp nhận số bằng False | ĐÃ VÁ THẬT | 0→3 | Landed số nguyên 0, hai list đúng: 1/0 | test:335 |
| J / `RV_J` — float được coi là bool | ĐÃ VÁ THẬT | 0→3 | Landed 0.0, hai list đúng: 1/0 | test:335 |
| K / `RV_K` — lọc bỏ phần tử null | ĐÃ VÁ THẬT | 0→3 | Bookkeeping gồm mapping và null: 1/0 | test:314 |
| L / `RV_L` — đòi nội dung mapping khác rỗng | ĐÃ VÁ THẬT | 0→3 | Hai list mỗi cái chứa mapping rỗng, hợp lệ Q1.2: 0/1 | test:327 |
| M / `RV_M` — dấu không phân biệt hoa | ĐÃ VÁ THẬT | 0→3 | Hai list đúng, ghi chú cho_dien viết thường: 0/1 | test:328 |
| N / `RV_N` — draft vẫn phải có trường | ĐÃ VÁ THẬT | 0→3 | Landed false, bỏ cả hai trường hoàn tất: 0/1 | test:326 |
| O / `RV_O` — null tường minh chuẩn hóa thành list hợp lệ | ĐÃ VÁ THẬT | 0→3 | Bookkeeping có mặt với null: 1/0 | test:313, chuỗi YAML null tách sentinel Python None |
| P / `RV_P` — cho phép phần tử số | ĐÃ VÁ THẬT | 0→3 | Bookkeeping gồm mapping và số 3: 1/0 | test:314 |
| Q / `RV_Q` — status list bị coi là mapping | ĐÃ VÁ THẬT | 0→3 | Status list có từ landed: 0/1, TypeError ở mutant | test:325, :330–334 |

Các module I–Q được viết lại theo ngữ nghĩa, không chép bảng executor: I dùng phép khác False, J dùng `type` và tuple kiểu, K dùng bộ lọc null, L kiểm độ dài từng dict, M dùng casefold, N dùng any cho trường thiếu, O dùng truy cập có khoá rồi chuẩn hóa, P dùng tập kiểu cụ thể, Q dùng `type` cho dict/list. Mỗi neo thay được kiểm đúng một lần trước khi chạy. H và Q không lấy crash trần làm tín dụng: input của chốt phải được xử lý rc=0/không L6; test chuyển kết quả ngoại lệ thành rc=-1 rồi `bang()` ném `TinHieuChotCa`. Do đó c16 thật sự thoát 3 với đúng `DO:c16_l6_landed_true_phai_co_phan_hoan_tat:`, không phải 4/HONG.

| Lớp / biểu hiện khác của lượt trước | Trạng thái | Bằng chứng và quyết định |
|---|---|---|
| P2 `c16-thieu-rang-q1`, phần (a) A–Q | ĐÃ VÁ THẬT | 17/17 độc lập cũ=0, nay=3; mọi Q1.1–4 có chốt riêng; không còn cách đọc sai thuộc nhóm (a) sống trong phép săn này |
| `c16-thieu-rang-q1`, toàn lớp kể cả phần (b) mới | MỘT PHẦN; cao nhất còn mở P3 | Giữ nguyên slug lịch sử. A–Q đóng; ba giới hạn mẫu SPACE bên dưới ghi nợ P3, không giữ P2 mở bằng yêu cầu giết mọi mutant |
| P3 `loi-khai-bang-chung-cu` A — 5/9 | CHƯA | Hai OID đều 10 true, trong đó 5 thiếu thu_hoi_cuoi. Không có hiện vật đính chính handoff/PR #845 trong bundle để xác nhận; không gọi GitHub theo chỉ thị |
| P3 cùng lớp B — docstring đường CI | ĐÃ VÁ THẬT | Checker:33–34 nói đúng đường gián tiếp registry:53 → workflow:895 → c11 test:277; regex đăng ký khớp stdout A/B |
| P3 `loi-khai-bang-chung-cu`, toàn lớp | MỘT PHẦN | Chỉ còn A; giữ spec r1 bất biến, giao executor/điều phối đính chính trong hiện vật công bố |

**BẢNG SĂN / phép đo độc lập.** Bản sao là Git archive của exact OID, không chạy suite trên checkout nguồn. Mọi tiến trình dùng `TMPDIR` tuyệt đối dưới `review-data/tmp`, tắt bytecode. Oracle Q1 viết riêng, dùng type/list/loop và duyệt chuỗi riêng, không lấy hằng hoặc hàm kiểm L6 từ sản phẩm.

| Giả thuyết / phạm vi | Lệnh đã chạy | Output thật / kết luận |
|---|---|---|
| So sánh nền và candidate, tránh lỗi nền | `python -B review-data/run_ab.py` | rc=0; cả 4 tiến trình con rc=0, stderr rỗng; bảng A/B bên dưới |
| C16 chỉ giết các mutant được executor chỉ | `python -B review-data/probe_mutations.py` | rc=0 phép đo; 54 module = 51 GIET, 3 SONG_SOT, 0 TIN_DUNG_GIA; 17 module A–Q có cặp CLI phản chứng riêng |
| Bool bị nhầm truthiness hoặc số | `python -B review-data/probe_behavior.py` | rc=0 toàn probe; 22/22 miền landed và 9/9 cách viết bool YAML. Int/float/null/chuỗi/container/ngày không phải bool; true/yes/on không nháy parse thành bool được chấp nhận |
| Hai trường hoặc phần tử bị kiểm thiếu / draft bị siết | Cùng lệnh probe hành vi | 104/104 ca true, 104/104 ca false; 32/32 tổ hợp hai trường, 4/4 đối chứng mapping hợp lệ. Gồm vắng/null/rỗng/sai container, phần tử null/số/bool/chuỗi/list/ngày ở đơn/đầu/giữa/cuối; mapping rỗng được nhận |
| Duyệt dấu thiếu khoá, thiếu tầng hoặc sai contains/case | Cùng lệnh probe hành vi | 200/200 ca khoá/giá trị, lồng dict/list tới 12 vòng, đầu/giữa/cuối, chuỗi dài/nhiều dòng, khác hoa; thêm 1/1 dấu trong comment không áp |
| Guard bị mở rộng sang status/root không mapping | Cùng lệnh probe hành vi | 17/17 scope: status vắng/null/bool/số/chuỗi/list/mapping thiếu landed; root list/scalar và status nằm sai chỗ. Không L6, không crash |
| L4 che sai phạm L6 | Cùng lệnh probe hành vi | 3/3 ca khoá trùng/alias/set đều base=head=2. Không dùng rc=2 làm bằng chứng giết L6. Kết quả cuối tổng 496/496, JSON đầu vào/rc/stdout lưu đầy đủ |
| Mutant sống chỉ qua c16 nhưng CA khác bắt | `python -B review-data/check_survivors.py` | rc=0; mỗi SPACE qua đủ 16/16 CA, không chạy vòng DOT_BIEN trên module đã đổi; `survivor-functional-results.json` |
| Số trong spec hoặc mô tả CI đã cũ | `python -B review-data/audit_evidence.py` | rc=0; Git blobs base/head đều 40 hồ sơ, 28 miễn trừ, 12 không miễn trừ, 10 true/2 false, 5/10 true thiếu thu_hoi_cuoi; regex cả hai matched=true |
| Ca lịch sử #840 thực bị L6 bắt, draft không bị bắt | Cùng lệnh audit | L6 trên byte của 473d56a/ef81b98/611ef62/79045a0 = 7/0/0/0; landed=True/False/False/True; bản cung cấp khớp blob nếu có. `history-results.json` |
| Kích thước, write_set, giữ nguồn nguyên trạng | `python -B review-data/prepare.py`; phép kiểm cuối | rc=0 preflight; diff/numstat khớp, +100/-1 đúng 2 tệp, whitespace rc=0; snapshot cuối ghi riêng ở cuối |

Các đầu ra nguyên văn: `ab-results.json`, `base-test.json`, `head-test.json`, `base-root.json`, `head-root.json`, `behavior-results.json`, `behavior-summary.json`, `mutation-baselines.json`, `mutation-results.json`, `git-tree-counts.json`, `registry-marker.json`, `history-results.json`. Rc=0 của script đo mutant chỉ chứng minh hoàn thành phép đo; ba SONG_SOT vẫn được giữ rõ trong bảng.

| Vế | Lệnh trong bản sao | rc | Bằng chứng dương |
|---|---|---:|---|
| Base | `python -B ops/land_evidence_nguon_test.py` | 0 | `CA: 15/15 dat`; `DOT BIEN: 37/37 bi giet dung ly do`; `TU KIEM PHAN HANG: DAT (2 dot bien)`; `TONG: DAT` |
| Head | Cùng lệnh suite | 0 | `CA: 16/16 dat`; `DOT BIEN: 64/64 bi giet dung ly do`; `TU KIEM PHAN HANG: DAT (2 dot bien)`; `TONG: DAT` |
| Base | `python -B ops/land_evidence_nguon.py --root .` | 0 | 12 ĐẠT · 28/28 miễn trừ · 0 vi phạm · 0 KHÔNG ĐO ĐƯỢC · tổng 40; `TỔNG: ĐẠT` |
| Head | Cùng lệnh checker | 0 | 12 ĐẠT · 28/28 miễn trừ · 0 vi phạm · 0 KHÔNG ĐO ĐƯỢC · tổng 40; `TỔNG: ĐẠT` |

Q2 được giữ: không đổi `MIEN_TRU_CUTOVER`, nhánh băm hoặc hồ sơ; suite c09/c10/c13 tiếp tục đạt. Kiểm tra lịch sử dùng byte từng blob cùng provenance của bản sao head, **không** tuyên bố tái hiện toàn cây hoặc CI của từng commit. Băm/OID đầy đủ từng lịch sử nằm trong JSON; ca true thiếu lease vẫn đúng vì lease không thuộc điều kiện Q1.

**BẢNG ĐỘT BIẾN.** Lệnh c16 cho mỗi module: biến môi trường `LAND_EVIDENCE_NGUON_MA` trỏ module tuyệt đối dưới `review-data/mutations/`, chạy `python -B review-data/head/ops/land_evidence_nguon_test.py --mot-ca c16_l6_landed_true_phai_co_phan_hoan_tat`. Baseline rc=0. GIET đòi rc=3 **và** đúng DO của ca đích; lỗi neo/import/syntax/exception vô can không được tín dụng. SHA-256 từng module và fixture lưu trong `mutation-results.json`; tên RV/SPACE chỉ là nhãn đọc bảng, không thay băm định danh mã.

| Mutant đăng ký / điều khoản | rc c16 | Kết quả / chốt |
|---|---:|---|
| L6_bo_ca_luat / Q1 | 3 | GIET; ca #840 |
| L6_bo_kiem_bool / 1 | 3 | GIET; chuỗi true |
| L6_ban_nhap_van_kiem / 4 | 3 | GIET; false thiếu trường |
| L6_chuoi_thay_danh_sach / 2 | 3 | GIET; chuỗi thay list |
| L6_danh_sach_rong_hop_le / 2 | 3 | GIET; list rỗng |
| L6_phan_tu_bat_ky / 2 | 3 | GIET; phần tử chuỗi |
| L6_bo_bookkeeping / 2 | 3 | GIET; thiếu bookkeeping |
| L6_bo_dau_giu_cho / 3 | 3 | GIET; dấu trong giá trị |
| L6_moi_thanh_mot / 2 | 3 | GIET; list trộn |
| L6_bookkeeping_chi_co_mat / 2 | 3 | GIET; bookkeeping mapping |
| L6_dau_gioi_han_do_sau / 3 | 3 | GIET; dấu sâu |
| L6_dau_chi_o_dau_chuoi / 3 | 3 | GIET; dấu giữa câu |
| L6_thieu_pmc_mac_dinh_hop_le / 2 | 3 | GIET; thiếu post_merge_checks |
| L6_bookkeeping_rong_hop_le / 2 | 3 | GIET; bookkeeping rỗng |
| L6_chi_kiem_phan_tu_cuoi / 2 | 3 | GIET; chuỗi rồi mapping |
| L6_bo_kiem_co_landed / guard | 3 | GIET; chốt không ném khi thiếu landed |
| L6_bo_kiem_mapping / guard | 3 | GIET; chốt status không mapping |
| L6_dau_bo_kiem_chuoi / 3 | 3 | GIET; chốt khoá ngày/null không phải chuỗi |
| L6_I_nhan_so_0 / 1 | 3 | GIET; số 0 |
| L6_J_nhan_float / 1 | 3 | GIET; 0.0 |
| L6_K_loc_null / 2 | 3 | GIET; phần tử null |
| L6_L_doi_mapping_khac_rong / 2 | 3 | GIET; mapping rỗng hợp lệ |
| L6_M_khong_phan_biet_hoa / 3 | 3 | GIET; dấu viết thường hợp lệ |
| L6_N_ban_nhap_doi_truong / 4 | 3 | GIET; false thiếu phần hoàn tất |
| L6_O_null_thanh_hop_le / 2 | 3 | GIET; trường null tường minh |
| L6_P_phan_tu_so / 2 | 3 | GIET; phần tử 3 |
| L6_Q_list_la_trang_thai / guard | 3 | GIET; status list không được ném |

17 mutant độc lập RV_A–RV_Q và các cặp cũ→nay / head→mutant đã liệt kê từng hàng trong bảng đối chiếu; **17/17 GIET**. Bảng sau bổ sung 7 phép thử thuộc (a), không phát sinh finding vì đều chết:

| Mutant reviewer bổ sung | Cách đọc sai (a) | c16 / CLI head–mutant |
|---|---|---|
| RV_R_values_only | Chỉ giá trị, bỏ khoá | 3/GIET; 1/0 |
| RV_S_exact_marker | Dấu phải bằng toàn chuỗi, thay contains | 3/GIET; 1/0 |
| RV_T_top_level_marker | Chỉ chuỗi ở gốc, bỏ cấu trúc lồng | 3/GIET; 1/0 |
| RV_U_only_one_completion | Chỉ đòi bookkeeping | 3/GIET; 1/0 |
| RV_V_check_first | Chỉ kiểm phần tử đầu | 3/GIET; 1/0 |
| RV_W_coerce_bool | Ép bool trước kiểm kiểu | 3/GIET; 1/0 |
| RV_X_marker_on_drafts | Kiểm mọi trạng thái kể cả false | 3/GIET; 0/1 |

**Phân biệt (a)/(b) và mutant sống.** (a) làm thay đổi một mệnh đề của Q1 mà tác giả có thể đọc hoặc cài sai: kiểu bool, lượng từ MỌI, hai trường, contains, khoá/giá trị, duyệt lồng, guard và ngoại lệ false. Những nhánh đó hiện có đối chứng và bị c16 khóa. (b) ở đây là áp ngưỡng hằng không có nguồn từ Q1/triển khai hiện tại, đặt sau kích thước các mẫu để giữ suite xanh. Tăng bất kỳ bộ fixture hữu hạn nào vẫn sinh được ngưỡng cao hơn; không coi mỗi ngưỡng mới là một P2 mới. Bằng chứng b vẫn là mutant **không tương đương**, không được gọi là tương đương để che sống sót.

| Mutant (b) / chỗ giới hạn tập mẫu | c16 / đủ CA | Phản chứng đã chạy, bằng lời | CLI head/mutant |
|---|---|---|---|
| SPACE_depth8 / test:320 | 0 / 16/16 | Hai list hợp lệ, dấu nằm dưới 12 mapping; mutant chỉ quét đường đi có tổng số phân cách ≤8 | 1/0 |
| SPACE_first64_chars / test:320 | 0 / 16/16 | Hai list hợp lệ, chuỗi ghi chú có 80 ký tự rồi mới đến dấu; mutant chỉ dò 64 ký tự đầu | 1/0 |
| SPACE_first8_elements / test:313 | 0 / 16/16 | Bookkeeping có tám mapping rồi một chuỗi sai ở phần tử thứ chín; mutant chỉ kiểm tám phần tử đầu | 1/0 |

Không có lát cắt tám phần tử, ngưỡng sâu tám hoặc cắt trước kiểm ở checker head: Q1.2 dùng `all` trên cả ds, Q1.3 dùng toàn `nut` do `duyet` dựng và contains trên toàn v; `v[:60]` chỉ dùng khi tạo thông báo sau điều kiện. C và R/T là thiếu duyệt theo cấu trúc; SPACE_depth8 đã đi mọi cấu trúc thông thường rồi thêm trần hằng tùy ý. Tương tự G/V thay lượng từ/phần tử đại diện, SPACE_first8_elements thêm giới hạn không có trong thiết kế. Vì vậy ba SPACE là **P3 (b)** về giới hạn phép nghiệm thu, không đủ giữ P2 mở. Nếu về sau xuất hiện cap thực trong code hoặc lý do thiết kế dẫn đến cap, phải đánh giá lại theo rủi ro thực, không mặc định dùng nhãn (b).

**Finding mới / nợ còn mở và cách xử lý.** Không có finding P0/P1/P2 mới. Không đề nghị sửa checker, miễn trừ, hồ sơ hoặc nới write_set trong lượt này.

| Mức / slug / file:dòng | Bằng chứng và phân loại | Owner / quyết định / hướng xử lý |
|---|---|---|
| P3 `c16-thieu-rang-q1`, biểu hiện SPACE-depth/length/count; `cay-kho/ops/land_evidence_nguon_test.py:313`, `:320` | Ba phản chứng trong bảng SPACE; (b). Suite lấy các mẫu hữu hạn ở độ sâu, độ dài và chiều dài list ngắn; không có lỗi tương ứng trong checker gốc. Giữ slug cũ, mức cao nhất còn mở đổi thành P3 vì toàn bộ biểu hiện P2 A–Q đã bị giết | Executor/điều phối #845. **Chấp nhận nợ, không chặn approve.** Hướng rẻ: mô tả chính xác giới hạn mẫu, tránh diễn giải chữ “mọi” trong comment thành phủ vô hạn. Nếu nâng độ bền sau này, sinh ca theo nhiều kích thước/độ sâu/độ dài, đặt phần tử sai ở vị trí thay đổi cho cả hai trường và có đối chứng dương. Khóa bằng test sinh dữ liệu và mutant cap đại diện, vẫn đòi TinHieuChotCa. Không chạy theo từng hằng SPACE; nếu mở test rộng thì làm packet riêng. Nguy cơ: test chậm/nondeterministic, vượt trần Q3 hoặc chạm giới hạn parser L4 rồi nhận nhầm tín dụng L6; dùng tập giá trị/seed cố định, giữ ca Q1 đo được |
| P3 `loi-khai-bang-chung-cu` A; `SPEC-r1.md:21` | Phản chứng Git blobs hai OID: 10 landed true, 5 thiếu thu_hoi_cuoi, không phải 5/9. Đây là finding tài liệu cũ còn mở, **N/A (không phải mutant Q1)**; không gán sai vào (a)/(b) | Executor/điều phối #845. **Chấp nhận nợ, không chặn approve.** Đính chính 5/10 trong handoff/mô tả công bố, neo exact OID và phạm vi bỏ miễn trừ bằng băm; giữ r1 đóng băng, nếu cần đổi spec thì ra revision mới. Phép khóa là đếm byte blobs theo exemption/hash rồi lọc `landed is True`, so danh sách thật; 10 true: pr778, pr779, pr791, pr792, pr793, pr800, pr801, pr818, pr832, pr836. Năm thiếu: pr778, pr791, pr793, pr800, pr801. Nguy cơ: đếm lẫn cutover/truthiness hoặc sửa đè spec. Không có hiện vật công bố để xác nhận đã đính chính; báo cáo này không tự đóng nghĩa vụ của executor |

**Bảng lớp và lịch sử.** Lượt 3 còn hai slug; lượt 4 giữ đúng hai slug đó, không đổi tên để reset lịch sử. `c16-thieu-rang-q1`: A–Q ĐÃ VÁ THẬT, còn ba biểu hiện mới (b) ở P3; `loi-khai-bang-chung-cu`: B đã đóng, A chưa đóng P3. Nếu tính ĐÃ VÁ THẬT cho *toàn lớp* theo §8.3, F/U từ lượt 3→4 là 0/2 vì vẫn có phần P3; riêng phần P2 đã đóng 17/17 biểu hiện. Không dùng tỷ lệ lớp để phủ nhận việc hạ rủi ro đã đo, cũng không dùng nó để nhận toàn lớp sạch. Prompt hiện hành đã cấp lượt 4 cuối cùng bằng authority được chuyển trong snapshot; không tự cấp lượt 5. Ngưỡng quyết định nội dung áp đúng prompt: không P0/P1/P2 mở, P3 được quyết định ghi nợ như trên. Công bố/receipt/land thuộc bước có thẩm quyền sau review này.

**Danh tính, assurance và giới hạn phép đo.** `identity-evidence.json` lưu metadata đọc từ chính thư mục run được giao và 12 dòng header đầu, prompt hash khớp launcher `28e22aa62219385ce6d3a342350c5a0cea72ed34b4e46a1393cfba1319f8c38b`. Run ID `620b7047bb964f7c93676348f87c9ffe`, session CLI `01a15317-ea30-7e92-8100-c8722d77b9f7`; launcher ghi provider `openai_codex`, surface `codex_cli`, transport `machine`, exact head khớp. Header thật: Codex v0.163.0, model `gpt-6.1-sol`, effort `xhigh`, sandbox `workspace-write`, approval `never`. Đây là bằng chứng CLI công bố cho lượt này, không chứng minh từng request được phục vụ bởi cùng model/effort; model/effort executor chỉ được assignment nhận là Claude, không có runtime thống kê riêng. Độc lập với context executor; chỉ kế thừa các verdict và bundle được giao.

Q4: có metadata và header của launcher cho chính run này; không tạo lời gọi Codex lồng. Ràng buộc gốc tối đa 3 được chỉ thị hiện hành nâng lên 4 và xác định đây là lượt CUỐI; nguồn authority nhận qua prompt, không kiểm GitHub vì bị cấm. Tại lúc đọc metadata, run đang `dang_chay`, chưa có rc terminal của chính phiên; controller phải kiểm terminal/hash hiện vật trước khi ghi receipt/state. Verdict approve là kết quả nội dung trên exact SHA, không tự sinh `cross_approved`, receipt đã validate, GitHub approval hoặc quyền push/merge/land.

Môi trường: Python 3.13.16, PyYAML 6.0.1, Linux x86_64; `environment.json`. Tool `cloud_environment.environment_status` không có trong danh sách khả dụng, nên readiness quản lý không đo được; không thao tác mạng. Checkout được đối xử read-only theo vai trò; sandbox thực là workspace-write, không giả là cơ chế filesystem read-only tuyệt đối.

Suite thành phần, checker cây thật, probe Q1, mutant và regex registry: **passed** như dữ liệu trên. Lượt probe hành vi đầu lỗi alias: **failed (bộ đo của reviewer), đã sửa và chạy lại**, giữ JSON gốc. Ba mutant SPACE: **survived**, không bị che trong tổng. Full repository selftest, bare Ruff lint, các release/deploy gate, Windows và GitHub Actions: **not_run**, không khai passed/skipped. Không có check bị skipped được nhận là pass. Miền ngoài mô hình L4 đo riêng; nội dung nghiệp vụ của mapping, sự hoàn tất thực, lease, landed_dieu_kien/ly_do, comments YAML và mọi kiểu spelling giữ chỗ ngoài CHO_DIEN nguyên văn không được suy từ L6.

Kiểm cuối: `python -B review-data/validate_evidence.py` **rc=0**, đối chiếu số trong báo cáo với JSON thô và xác nhận 17 A–Q cũ=0/nay=3, 51 GIET/3 SONG_SOT/0 tín dụng giả, 496/496 hành vi, 4 tiến trình A/B rc=0. Snapshot nguồn trước/sau đều **4.878 mục**, **0 delta byte/mode/symlink**, **0 delta HEAD/tree/status/diff/index**; `readonly-before.json`, `readonly-after.json`, `readonly-delta.json`, `validation-summary.json`. Chỉ kết luận không có delta quan sát được tại hai mốc, không chứng minh lịch sử chưa từng ghi rồi hoàn nguyên. Manifest băm hiện vật cuối ở `artifact-manifest.json`; không sửa bất kỳ tệp nào dưới `cay-kho/`.
