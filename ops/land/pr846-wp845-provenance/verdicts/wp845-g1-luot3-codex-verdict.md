verdict: changes_requested
reviewed_sha: ecebffe9675d0952f3a0ab65eaa44087853a26bc

Bản ghi tích lũy lượt 3/3, đã chốt **changes_requested**. Reviewer độc lập họ OpenAI, phiên Codex có shell cục bộ; executor theo packet là Claude. Chỉ ghi dưới `review-data/`, không gọi GitHub, không sửa `cay-kho/`, không push/merge/land. Các mốc 1–2 bên dưới giữ lịch sử ghi tăng dần; kết luận cuối và bảng chi tiết ở sau.

Preflight đã đo: HEAD đúng neo; tree `9c9683856e952e1bccb5b90c939b70483dc72cfa`; checkout sạch. Spec SHA-256 `a5a89622376495186ae265f18f4f6d1ce7e2b2e3b7613c61c2d96087a2c3af0b` khớp. Diff base–head gồm đúng hai tệp trong write_set, +83/-1, đạt Q3 (≤150 dòng thêm). Đang dựng phép đo A/B và đột biến độc lập; không dùng kết quả executor thay kết quả chạy.

Mốc đo 1: cả 18 mutant L6 trong bảng executor và 8 mutant A–H do reviewer dựng lại đều bị c16 giết bằng rc=3, đúng tiền tố `DO:c16_l6_landed_true_phai_co_phan_hoan_tat:`. Các biên còn lại đã có mutant sống, gồm kiểu landed 0/float, phần tử null, mapping rỗng hợp lệ, dấu khác hoa thường và draft thiếu trường. Lớp P2 `c16-thieu-rang-q1` chưa đủ điều kiện đóng; đang kiểm toàn bộ 16 CA và các phản chứng CLI. Chi tiết tích lũy: `mutation-results.json`.

Mốc đo 2: lệnh A/B `python -B review-data/run_ab.py` hoàn tất rc=0; base 15/15 CA và 37/37 đột biến, head 16/16 CA và 55/55 đột biến; hai checker cây thật đều rc=0, 12 ĐẠT, 28/28 miễn trừ, 0 vi phạm. `probe_behavior.py` rc=0, 225/225 ca khớp kỳ vọng. `check_survivors.py` rc=0: cả 9 mutant sống đều qua đủ 16 CA; từng phản chứng CLI đã phân biệt head và mutant. Đếm Git blobs hai OID xác nhận 5/10, không phải 5/9; P3 đính chính mô tả PR chưa có hiện vật để kiểm độc lập. Kết luận nội dung dự kiến: changes_requested vì 1 lớp P2 còn mở.

KẾT LUẬN CUỐI: tám biểu hiện A–H đã vá thật, nhưng lớp P2 `c16-thieu-rang-q1` chỉ được vá **MỘT PHẦN**, chưa đóng. Có 9 mutant không tương đương mới qua c16 và toàn bộ 16 CA; phản chứng CLI riêng cho từng mutant chứng minh bỏ lọt, từ chối oan hoặc crash. Vì ngưỡng packet không cho P0/P1/P2 mở, chưa thể approve. Không phát hiện P0/P1 hoặc sai hành vi L6 của checker gốc trên 225 ca độc lập. Đếm riêng: **1 lớp P2 mở, 9 biểu hiện mới I–Q; 1 lớp P3 mở, 1 biểu hiện A chưa hoàn tất**. Không đếm 9 mutant thành 9 lớp hoặc báo lỗi giả định của mutant như lỗi runtime đang có ở head.

ĐỐI CHIẾU LƯỢT TRƯỚC. Nguồn: lượt 1 `c95bd7f80a45a592f3cb089149c0c23fb4df2317`, lượt 2 `fa4fb7ce98c56b56a2523bf8c2b6a6bc2fb98181`. `test:` là `cay-kho/ops/land_evidence_nguon_test.py`. Cột cũ/mới là rc của đúng c16 trên cùng module mutant reviewer dựng, không phải suy từ diff.

| Mức / slug / biểu hiện | Trạng thái | Bằng chứng độc lập trên head này |
|---|---|---|
| P2 `c16-thieu-rang-q1` A: all→any | ĐÃ VÁ THẬT | `RV_A_all_any`: c16 lượt 1/hiện tại = 0/3; DO:c16 đúng. Phản chứng list bookkeeping trộn mapping/chuỗi: head/mutant CLI = 1/0. |
| P2 cùng lớp B: bookkeeping chỉ cần có giá trị | ĐÃ VÁ THẬT | `RV_B_bookkeeping_truthy`: cũ/mới = 0/3; mapping thay list: head/mutant = 1/0. Ma trận kiểm hai trường là bản chép riêng tại test:36, không đọc danh sách từ checker. |
| P2 cùng lớp C: dấu chỉ tới ít tầng | ĐÃ VÁ THẬT | `RV_C_depth_mapping`, giới hạn số tầng mapping qua đường đi: cũ/mới = 0/3; dấu trong giá trị sâu: head/mutant = 1/0. Cả dấu ở khoá sâu cũng được thử trong ma trận mới. |
| P2 cùng lớp D: dấu chỉ ở đầu chuỗi | ĐÃ VÁ THẬT | `RV_D_marker_find_zero` dùng phép find bằng 0, khác biểu thức startswith của executor: c16 lượt 2/hiện tại = 0/3; dấu giữa câu: head/mutant = 1/0. Chốt test:319. |
| P2 cùng lớp E: thiếu post_merge_checks được mặc định hợp lệ | ĐÃ VÁ THẬT | `RV_E_missing_pmc_fallback` dùng tra khoá trực tiếp nếu có, fallback riêng trường thiếu: cũ/mới = 0/3; bỏ hẳn trường: head/mutant = 1/0. Chốt test:313–318. |
| P2 cùng lớp F: bookkeeping rỗng được qua | ĐÃ VÁ THẬT | `RV_F_empty_bookkeeping` nới độ dài riêng bookkeeping: cũ/mới = 0/3; list rỗng: head/mutant = 1/0. |
| P2 cùng lớp G: chỉ kiểm phần tử cuối bookkeeping | ĐÃ VÁ THẬT | `RV_G_last_bookkeeping` chỉ cắt lát ở bookkeeping, trường kia giữ all: cũ/mới = 0/3; chuỗi đứng trước mapping: head/mutant = 1/0. Không dựa vào mutant executor bị bắt ở trường post_merge_checks. |
| P2 cùng lớp H: bỏ điều kiện có landed | ĐÃ VÁ THẬT | `RV_H_no_landed_guard`: cũ/mới = 0/3. Status mapping chỉ có merged: head rc=0; mutant CLI rc=1/KeyError. C16 mới bắt ngoại lệ ở đúng fixture không được ném rồi `bang()` phát TinHieuChotCa (test:322–329); không ghi crash trần thành GIET. |
| P2 `c16-thieu-rang-q1`, toàn lớp | MỘT PHẦN | A–H đóng đúng phạm vi đã đo. Các biên I–Q dưới đây chưa có chốt; 9 mutant qua đủ 16 CA. |
| P3 `loi-khai-bang-chung-cu` A: 5/9→5/10 | CHƯA (đính chính PR/handoff chưa kiểm được) | Git blobs base và head đều 10 true, trong đó 5 thiếu thu_hoi_cuoi. Prompt đã nhận số đúng, nhưng chỉ hẹn sửa mô tả PR; không có hiện vật PR/handoff chứa đính chính để xác minh. SPEC-r1.md:21 giữ 5/9 là dữ kiện cũ trong spec đóng băng, không yêu cầu sửa đè. |
| P3 cùng lớp B: docstring đường CI | ĐÃ VÁ THẬT | Checker:33–34 ghi đường gián tiếp qua c11. Registry `.claude/dev/ci_dang_ky_test.py:53`, workflow `.github/workflows/ci.yml:895` và test:277–280 khớp; marker base/head đều khớp regex đăng ký. |
| P3 `loi-khai-bang-chung-cu`, toàn lớp | MỘT PHẦN | Còn A; owner executor/điều phối #845, đính chính số bằng chứng trong mô tả PR/handoff neo exact SHA khi chuẩn bị công bố; nếu sửa spec thì revision mới. Không chặn riêng bằng P3. |

BẢNG SĂN. Các lệnh chạy từ gốc rv845c; bản sao Git archive, module đột biến, dữ liệu tạm và log đều trong `review-data/`. `TMPDIR` là đường tuyệt đối tới `review-data/tmp`; `PYTHONDONTWRITEBYTECODE=1`, `GIT_OPTIONAL_LOCKS=0`. Không chạy trên checkout nguồn.

| Phép đo / lệnh | Kết quả thực | Kết luận / giới hạn |
|---|---|---|
| `python -B review-data/run_ab.py` | rc=0, 4 tiến trình con đều rc=0; stdout/stderr đầy đủ trong `ab-results.json`, `base-test.json`, `head-test.json`, `base-root.json`, `head-root.json` | Cùng một lệnh dựng cả hai cây từ exact OID rồi chạy suite và checker; kết quả hai vế ở bảng kế tiếp. |
| `python -B review-data/probe_mutations.py` | rc=0 của phép đo; 36 mutant: 27 GIET bằng TinHieuChotCa, 9 SONG_SOT, 0 tín dụng giả | 18 từ bảng executor và 18 do reviewer dựng; script rc=0 không có nghĩa mọi mutant chết. `mutation-results.json`, `mutation-summary.json`, `mutation-baselines.json`. |
| `python -B review-data/check_survivors.py` | rc=0; từng mutant I–Q đều rc=0 với đủ 16/16 CA, stderr rỗng | `survivor-functional-results.json`. Chạy mọi CA, gồm c11 trên cây thật trong bản sao; không lấy lỗi neo khi chạy vòng mutation trên mã đã sửa làm tín dụng. |
| `python -B review-data/probe_behavior.py` | rc=0; 225/225 ca khớp kỳ vọng | 222 ca Q1/phạm vi base rc=0; 3 ca L4 cả base/head rc=2. Head gốc khớp oracle độc lập trên tập hữu hạn; không suy phủ mọi YAML. `behavior-results.json`. |
| Đếm Git blobs ở base/head, miễn trừ theo băm byte rồi lọc landed bằng `is True` | Mỗi cây: 28 miễn trừ, 12 không miễn trừ, 10 true, 2 false; 5/10 true thiếu thu_hoi_cuoi | `git-tree-counts.json`; 0 dấu CHO_DIEN ở khoá/giá trị parse của 12 hồ sơ. Không đếm lẫn cutover, không dùng truthiness. |
| `git -c core.abbrev=7 -C cay-kho diff <base> <head>`; diff lượt 2; `diff --numstat`; `diff --check` | Diff và numstat giao kèm khớp byte; whitespace rc=0; checker +19/-1, test +64/-0 | `preflight.json`; tổng +83/-1, đúng 2 tệp, đạt Q3. Từ lượt 2 chỉ đổi test. Không đổi CI, hồ sơ hay miễn trừ. |
| AST lấy regex registry, so stdout hai suite bằng re.search | Cả hai matched=true | `registry-marker.json`. Xác nhận tương thích định dạng tổng kết, không phải một lần chạy GitHub Actions. |
| Snapshot byte/mode/symlink toàn cây nguồn, cả tracked/untracked/ignored và .git; HEAD/tree/status/diff/index trước–sau | Kết quả cuối ở `readonly-delta.json` | Chỉ kết luận về delta quan sát được ở hai mốc; không chứng minh lịch sử giữa hai mốc chưa từng ghi rồi hoàn nguyên. |

| Vế | Lệnh bên trong bản sao | rc thật | Bằng chứng dương |
|---|---|---:|---|
| base `9f4a539b12d1d948817123d117f4bf2aedb1898f` | `python -B ops/land_evidence_nguon_test.py` | 0 | CA: 15/15 dat; DOT BIEN: 37/37 bi giet dung ly do; TU KIEM PHAN HANG: DAT (2 dot bien); TONG: DAT |
| base | `python -B ops/land_evidence_nguon.py --root .` | 0 | 12 ĐẠT · 28/28 miễn trừ · 0 vi phạm · 0 KHÔNG ĐO ĐƯỢC · tổng 40; TỔNG: ĐẠT |
| head `ecebffe9675d0952f3a0ab65eaa44087853a26bc` | `python -B ops/land_evidence_nguon_test.py` | 0 | CA: 16/16 dat; DOT BIEN: 55/55 bi giet dung ly do; TU KIEM PHAN HANG: DAT (2 dot bien); TONG: DAT |
| head | `python -B ops/land_evidence_nguon.py --root .` | 0 | 12 ĐẠT · 28/28 miễn trừ · 0 vi phạm · 0 KHÔNG ĐO ĐƯỢC · tổng 40; TỔNG: ĐẠT |

CÁC BIÊN CÒN LẠI ĐÃ TỰ LIỆT KÊ, không lấy bảy hình dạng hoặc bảng executor làm trần:

| Điều khoản / nhóm biên | Phép đo độc lập | Tình trạng chốt c16 hiện tại |
|---|---|---|
| Guard/phạm vi | 13 ca: status vắng/null/bool/số/list/chuỗi/mapping thiếu landed; root list, status lồng sai chỗ; khoá int/ngày/null; dấu trong chú thích | Các guard mapping thiếu landed và chuỗi đã có chốt; status list chứa từ landed chưa có (Q sống). Không yêu cầu L6 áp cho status không-mapping. |
| Q1.1: kiểu sau parse | 22 ca: chuỗi có nháy true/false/yes/rỗng, int 0/1/-1, float 0.0/1.0/nan/inf, null, list/mapping, ngày; bool true/True/TRUE/yes/on/!!bool được nhận | C16 chỉ dùng chuỗi true, int 1, null để khóa kiểu. I/J sống ở zero/float. Không đòi cách viết literal true khi YAML đã dựng bool. |
| Q1.2: hai trường, kiểu container và mọi phần tử | 92 ca sai + 10 ca hợp lệ. Từng trường: vắng, null tường minh, rỗng, mapping/chuỗi/số/bool/ngày; phần tử null/số/bool/list/chuỗi/ngày, riêng lẻ hoặc đầu/giữa/cuối với mapping; dương gồm mapping rỗng, nhiều mapping, trường tùy ý | Matrix mới phủ cả hai trường nhưng sentinel Python None bị **bỏ dòng**, không tạo YAML null. Mọi phần tử sai được c16 thử đều là chuỗi. Mapping rỗng hợp lệ chưa có đối chứng. K/O/P và L sống. |
| Q1.3: chứa dấu chính xác ở khoá/giá trị | 40 ca: đầu/giữa/cuối, xen list/mapping tới 12 tầng, khoá và giá trị; 10 biên: khác hoa thường, dấu nằm trong từ dài hơn, chuỗi nhiều dòng có dấu nguyên vẹn hoặc dấu bị tách qua newline | Contains/startswith, keys/values, độ sâu đang được bắt (D/C/R chết). Chưa khóa tính phân biệt hoa thường: M sống. Không mở rộng sang biến thể dấu hoặc chú thích. |
| Q1.4: false không đòi gì của L6 | 35 ca: false/False/FALSE/no/off sau parse, hai trường cùng vắng/null/rỗng/sai kiểu/list trộn/dấu ở khoá | C16 chỉ có false với hai trường đều hiện diện ở dạng chuỗi giữ chỗ. N sống khi draft thiếu trường. L1–L5 vẫn áp độc lập. |
| L4/Q2/phần ngoài mô hình | 3 ca L4: khoá trùng, alias và set đều rc=2 ở base/head; 28/28 cutover vẫn miễn trừ; suite c08/c09/c10 tiếp tục xanh | Không đòi L6 cho YAML parser từ chối hoặc kiểu duyet từ chối; không dùng rc=2 làm bằng chứng đã kiểm L6. Q2 không đổi trong diff. |

**Lớp chưa đóng.** Độ phủ trên là phân hoạch hữu hạn của loại dữ liệu, tính hợp lệ và phạm vi trong Q1. Việc mỗi điểm 1–4 có ít nhất một mutant riêng chết đúng lý do đã đạt, nhưng không đủ đóng lớp với các phản chứng không tương đương đang sống. Không cần thêm giới hạn độ sâu tùy tiện hay điều kiện nghiệp vụ ngoài spec để thấy lỗ này.

BẢNG ĐỘT BIẾN. Lệnh đích: `LAND_EVIDENCE_NGUON_MA=<đường tuyệt đối module trong review-data/mutations> python -B review-data/head/ops/land_evidence_nguon_test.py --mot-ca c16_l6_landed_true_phai_co_phan_hoan_tat`. Baseline c16 gốc rc=0; chỉ ghi GIET khi rc=3 và có đúng `DO:c16_l6_landed_true_phai_co_phan_hoan_tat:` do `chay_ca` bắt TinHieuChotCa. Lỗi neo, import, syntax hoặc rc=4 không được tín dụng. Mỗi neo dưới đây đã kiểm xuất hiện đúng một lần; mã mutant và cặp neo/thay lưu trong `probe_mutations.py` và `mutation-results.json`.

| Mutant trong bảng executor | Q1 | rc c16 | Phân hạng / chốt thực tế |
|---|---|---:|---|
| L6_bo_ca_luat | 1–4 | 3 | GIET, ca #840 |
| L6_bo_kiem_bool | 1 | 3 | GIET, chuỗi true |
| L6_ban_nhap_van_kiem | 4 | 3 | GIET, draft false |
| L6_chuoi_thay_danh_sach | 2 | 3 | GIET, chuỗi không dấu |
| L6_danh_sach_rong_hop_le | 2 | 3 | GIET, list rỗng |
| L6_phan_tu_bat_ky | 2 | 3 | GIET, list chứa chuỗi |
| L6_bo_bookkeeping | 2 | 3 | GIET, thiếu bookkeeping |
| L6_bo_dau_giu_cho | 3 | 3 | GIET, dấu trong giá trị |
| L6_moi_thanh_mot | 2 | 3 | GIET, list trộn |
| L6_bookkeeping_chi_co_mat | 2 | 3 | GIET, bookkeeping mapping |
| L6_dau_gioi_han_do_sau | 3 | 3 | GIET, giá trị sâu |
| L6_dau_chi_o_dau_chuoi | 3 | 3 | GIET, dấu giữa câu |
| L6_thieu_pmc_mac_dinh_hop_le | 2 | 3 | GIET, thiếu post_merge_checks |
| L6_bookkeeping_rong_hop_le | 2 | 3 | GIET, bookkeeping rỗng |
| L6_chi_kiem_phan_tu_cuoi | 2 | 3 | GIET, phần tử sai ở đầu post_merge_checks |
| L6_bo_kiem_co_landed | guard | 3 | GIET, chốt không ném ở status thiếu landed |
| L6_bo_kiem_mapping | guard | 3 | GIET, chốt không ném ở status chuỗi |
| L6_dau_bo_kiem_chuoi | 3 | 3 | GIET, chốt không ném ở khoá ngày/null |

Ba hàng cuối không lấy traceback làm tín dụng trực tiếp: c16 đo đầu vào hợp lệ/không áp L6, bắt exception thành kết quả rc=-1 rồi **bang(rc==0 và không L6)** ném TinHieuChotCa. Đó là chốt đúng cho thuộc tính không được ném ở các fixture này. TU_KIEM vẫn phân biệt KeyError vô can ở c01 thành TIN_DUNG_GIA.

| Mutant độc lập reviewer | Điều khoản | rc c16 cũ → mới | Phân hạng; head/mutant CLI trên phản chứng riêng |
|---|---|---|---|
| RV_A_all_any | 2 / A | 0 → 3 | GIET; 1/0 |
| RV_B_bookkeeping_truthy | 2 / B | 0 → 3 | GIET; 1/0 |
| RV_C_depth_mapping | 3 / C | 0 → 3 | GIET; 1/0 |
| RV_D_marker_find_zero | 3 / D | 0 → 3 | GIET; 1/0 |
| RV_E_missing_pmc_fallback | 2 / E | 0 → 3 | GIET; 1/0 |
| RV_F_empty_bookkeeping | 2 / F | 0 → 3 | GIET; 1/0 |
| RV_G_last_bookkeeping | 2 / G | 0 → 3 | GIET; 1/0 |
| RV_H_no_landed_guard | guard / H | 0 → 3 | GIET; 0/1, mutant KeyError |
| RV_I_bool_or_zero | 1 / I | — → 0 | SONG_SOT; 1/0 |
| RV_J_float_as_bool | 1 / J | — → 0 | SONG_SOT; 1/0 |
| RV_K_ignore_null_elements | 2 / K | — → 0 | SONG_SOT; 1/0 |
| RV_L_mapping_must_nonempty | 2 / L | — → 0 | SONG_SOT; 0/1, mutant từ chối oan |
| RV_M_case_insensitive_marker | 3 / M | — → 0 | SONG_SOT; 0/1, mutant từ chối oan |
| RV_N_draft_requires_presence | 4 / N | — → 0 | SONG_SOT; 0/1, mutant từ chối oan |
| RV_O_list_null_normalized | 2 / O | — → 0 | SONG_SOT; 1/0 |
| RV_P_numeric_elements_allowed | 2 / P | — → 0 | SONG_SOT; 1/0 |
| RV_Q_nonstring_status_list | guard / Q | — → 0 | SONG_SOT; 0/1, mutant TypeError |
| RV_R_marker_only_values | 3 / đối chứng | — → 3 | GIET; 1/0 |

Tổng reviewer: 36 mutant = 18 executor + 18 độc lập; **27 GIET, 9 SONG_SOT, 0 TIN_DUNG_GIA**. Không thay hoặc diễn giải lại 55/55 của tập đăng ký. Với cả I–Q, wrapper `run_cases.py` gọi đúng toàn bộ hàm CA của suite qua `chay_ca`, không chạy vòng DOT_BIEN vốn dựng từ mã gốc HERE; từng wrapper thực trả rc=0 và 16/16 CA. Bởi vậy không tuyên bố chạy toàn suite mutation trên mutant rồi xanh.

FINDING MỚI — **P2 `c16-thieu-rang-q1`**, nối cùng lớp lượt 1–2, owner executor/điều phối #845. Vị trí chính `cay-kho/ops/land_evidence_nguon_test.py:313`, `:330`; bảng mutation L6 bắt đầu `:386`. Lỗi là tập ca chưa khóa các nhánh đúng của Q1 và phạm vi, không phải checker gốc đang nhận các hồ sơ sai dưới đây. Đường checker liên quan: `ops/land_evidence_nguon.py:278` guard, `:279` bool, `:284` kiểu list/phần tử, `:287` dấu.

| Biểu hiện / file:dòng | Phản chứng bằng lời và sai lệch mutant đã chạy | Kết quả head/mutant; c16 / đủ CA |
|---|---|---|
| I — test:330 | Hai list hợp lệ, landed là số nguyên 0. Mutant bỏ lỗi kiểu cho giá trị bằng False, vô tình nhận 0 qua phép bằng của Python. C16 hiện chỉ thử int 1. | 1/L6 → 0; c16 0, 16/16 CA |
| J — test:330 | Hai list hợp lệ, landed là float 0.0. Mutant mở kiểu nhận bool hoặc float. Không ca nào của c16 dùng float. | 1/L6 → 0; c16 0, 16/16 CA |
| K — test:313 | Landed true, post_merge_checks đúng, bookkeeping có mapping và một phần tử null. Mutant lọc bỏ phần tử null trước all. Cả ba thứ tự trộn trong matrix chỉ dùng chuỗi làm phần tử sai. | 1/L6 → 0; c16 0, 16/16 CA |
| L — test:300–301 | Landed true, cả hai list mỗi cái chứa một mapping rỗng. Đây là dữ liệu đúng Q1.2. Mutant thêm điều kiện mỗi mapping phải khác rỗng. Các ca dương c16 đều dùng mapping có nội dung. | 0 → 1/L6; c16 0, 16/16 CA |
| M — test:319 | Landed true, hai list đúng, một ghi chú chứa cho_dien viết thường. Theo literal Q1.3 nó không chứa CHO_DIEN. Mutant upper chuỗi trước so sánh, từ chối oan. | 0 → 1/L6; c16 0, 16/16 CA |
| N — test:332 | Landed false, bỏ cả hai trường hoàn tất. Mutant cũng kiểm list khi thiếu bất kỳ trường bắt buộc nào, bất kể false. Ca draft duy nhất của c16 có đủ hai trường nên không thấy sai lệch. | 0 → 1/L6; c16 0, 16/16 CA |
| O — test:313–317 | Landed true, post_merge_checks đúng, bookkeeping có mặt với giá trị YAML null. Mutant chuẩn hoá null hiện diện thành list chứa mapping. None ở matrix chỉ bỏ dòng, nên chỉ thử thiếu chứ không thử null tường minh. | 1/L6 → 0; c16 0, 16/16 CA |
| P — test:313 | Landed true, post_merge_checks đúng, bookkeeping chứa mapping và số nguyên 3. Mutant nới kiểu phần tử sang dict/int/float; mọi phần tử sai đang có trong c16 là chuỗi nên vẫn bị từ chối. | 1/L6 → 0; c16 0, 16/16 CA |
| Q — test:322–324 | Status là list có một chuỗi landed. Theo guard Q1, L6 không áp. Mutant nhận dict hoặc list làm status rồi tra chỉ số chuỗi, sinh TypeError. C16 đã khóa chuỗi nhưng chưa khóa list. | 0 → CLI 1/TypeError; c16 0, 16/16 CA |

Các đầu vào phản chứng, stdout/stderr và rc nằm dưới `counterexamples/RV_I_bool_or_zero` đến `counterexamples/RV_Q_nonstring_status_list` và trong `mutation-results.json`; không chỉ có hướng tấn công chưa chạy. Các fixture được mô tả bằng lời ở đây, không cung cấp bản vá gate để áp mù.

Hướng đóng **chung cả lớp**: sửa test trong write_set, xây bảng phân hoạch từ miền kiểu sau parse của Q1, gồm cả **được phép và bị cấm**. Mở tập landed để tách bool khỏi số 0/1/float/null/chuỗi/container; mở matrix hai trường để tách vắng/null/container sai/phần tử sai kiểu (null, số, bool, list, chuỗi) và đối chứng mapping rỗng; giữ các thứ tự trộn. Bổ sung đối chứng dấu khác hoa thường và draft false thiếu/null các trường; thêm status list để bảo vệ guard. Đăng ký mutant phân biệt đúng các thuộc tính đó, đòi baseline xanh và mỗi mutant đỏ bằng TinHieuChotCa. Có thể gom thành các vòng dữ liệu ngắn; không cần vá riêng checker hoặc thêm điều kiện nghiệp vụ.

Phép kiểm đóng lớp: mọi A–Q cùng các mutant trực tiếp bảo vệ Q1.1–4 đều được tái đo trên cùng candidate; không còn mutant không tương đương sống trong phân hoạch đã công bố; A/B suite + cây thật vẫn đạt; ≤2 tệp/≤150 dòng thêm. Những miền chưa đo phải được khai riêng, không dùng từ mọi để mô tả bảy hình dạng. Nguy cơ của sửa test: nhầm sentinel vắng với null YAML; Python bool là kiểu con của int; đưa điều kiện nội dung mapping hoặc dấu không phân biệt hoa thường vào oracle rồi siết ngoài spec; dùng lỗi L1/L2 để che L6. Với guard, kiểm CLI/no-throw rồi bang trên kết quả cụ thể, tránh catch rộng cho tất cả ca sai làm exception vô can thành tín dụng.

P3 còn mở — **`loi-khai-bang-chung-cu` A, SPEC-r1.md:21**. Số đo đúng trên cả hai OID: 10 hồ sơ true (pr778, pr779, pr791, pr792, pr793, pr800, pr801, pr818, pr832, pr836), trong đó 5 thiếu thu_hoi_cuoi (pr778, pr791, pr793, pr800, pr801); hai false là pr772 và pr823. Chủ nợ executor/điều phối #845. Đính chính 5/10 trong hiện vật handoff/mô tả PR, ghi phạm vi và exact OID, giữ r1 bất biến; nếu cần sửa đặc tả thì ra r2. Khóa bằng phép đếm Git blobs bỏ miễn trừ theo băm, lọc `landed is True`. Nguy cơ: đếm lẫn cutover hoặc lọc theo truthiness. Chỉ lời hẹn sửa chưa đủ chứng minh đã xử lý; không gọi GitHub để kiểm thêm vì prompt cấm.

Neo cuối và giới hạn: head/tree tại đầu báo cáo, base `9f4a539b12d1d948817123d117f4bf2aedb1898f`; spec khớp SHA-256 đã giao. Python 3.13.16, PyYAML 6.0.1, Linux. Provider theo context phiên là OpenAI/Codex, có công cụ shell `exec_command`, transport machine; không suy model/effort hoặc execution surface CLI từ tên công cụ. Không có attestation độc lập của model/effort hay invocation `.claude/dev/launcher.py run`; Q4 về bề mặt gọi không tự xác minh được từ checkout. Không gọi Codex lồng, không tự tạo receipt, `cross_approved` hay quyền land. `cloud_environment.environment_status` không có trong danh sách công cụ khả dụng; không có thao tác mạng.

Targeted suite và checker: **passed** như bằng chứng trên. Full repository selftest, bare Ruff lint, release/deploy gate và GitHub Actions: **not_run**, không tuyên bố passed hay skipped. Ba đầu vào ngoài mô hình: đo được rc=2 đúng kỳ vọng, không phải bỏ qua phép chạy. Không tái hiện thêm toàn lịch sử PR #840 ở lượt này; kết luận lịch sử trong verdict trước không được coi là kết quả chạy mới.

Budget/không hội tụ: đây là lượt cuối 3/3 theo prompt. Hai lớp mở cuối lượt 2 vẫn chưa đóng toàn lớp ở lượt 3: |F|/|U| = 0/2; chuyển tiếp lượt 1→2 cũng 0/2 theo hai verdict giao kèm. Lớp P2 xuất hiện cả ba lượt. Theo protocol §12 cần Review Rescue Checkpoint với human/điều phối sau verdict này; không tự cấp lượt 4 hoặc đổi slug để reset lịch sử. Đề nghị xem lại cách nghiệm thu theo miền kiểu; chỉ tách phần độc lập nếu đạt điều kiện Stable Slice, không merge hỗn hợp rồi hứa sửa sau.

Kiểm cuối: snapshot trước/sau đều **4.878 mục**, 0 delta byte/mode/symlink và 0 delta HEAD/tree/status/diff/index (`readonly-before.json`, `readonly-after.json`, `readonly-delta.json`). Các bộ đếm trong verdict đã đối chiếu với JSON thô, không lấy rc=0 của script đo thay bằng chứng dương. Chỉ tạo đầu ra dưới `review-data/`; checkout nguồn vẫn giữ nguyên exact SHA đã review.
