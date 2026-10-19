verdict: changes_requested
reviewed_sha: c95bd7f80a45a592f3cb089149c0c23fb4df2317

Đang review độc lập; verdict tạm thời, sẽ chốt sau phép đo.

- Vai trò: reviewer OpenAI, Codex qua công cụ shell của phiên hiện tại; không phải ChatGPT Web/human-mediated. Không có bằng chứng runtime về tên model cụ thể hoặc launcher ngoài chỉ thị phiên; không suy danh tính từ tài khoản.
- Phạm vi ghi: chỉ `review-data/`; cây `cay-kho/` read-only; không gọi GitHub, push, merge hoặc land.
- Dữ liệu neo và đối chiếu: `preflight.json`.

Phép đo bổ sung `python review-data/probe_behavior.py`: 53/53 ca khớp kỳ vọng; 12 hồ sơ không miễn trừ; 10 landed true, 5 thiếu `lease.thu_hoi_cuoi`. Bằng chứng: `behavior-results.json`, `real-tree-audit.json`, `history-results.json`, `exemption-results.json`.

Đột biến độc lập: tám đột biến L6 trong `DOT_BIEN` đều rc=3, dòng `DO:c16_…`, phân hạng GIET. Ba đột biến bổ sung sống sót c16 (rc=0): `all` thành `any`, bookkeeping chỉ kiểm có giá trị, và chỉ tìm dấu tới hai tầng. Mỗi phản chứng riêng cho head rc=1, mutant rc=0. Bằng chứng: `mutation-results.json`, `mutation-counterexamples.json`.

Đã đo A/B trong cùng một lệnh `python review-data/run_ab.py`: hai bản archive Git được dựng trước khi chạy. `TMPDIR=review-data/tmp` (đường tuyệt đối), `PYTHONDONTWRITEBYTECODE=1`, `GIT_OPTIONAL_LOCKS=0`.

| Vế | Lệnh trong bản sao | rc thật | Dòng tổng kết |
|---|---|---:|---|
| base | `python ops/land_evidence_nguon_test.py` | 0 | CA: 15/15 dat; DOT BIEN: 37/37 bi giet dung ly do; TU KIEM PHAN HANG: DAT (2 dot bien); TONG: DAT |
| base | `python ops/land_evidence_nguon.py --root .` | 0 | land_evidence_nguon: 12 ĐẠT · 28/28 miễn trừ (băm khớp) · 0 vi phạm · 0 KHÔNG ĐO ĐƯỢC · tổng 40; TỔNG: ĐẠT |
| head | `python ops/land_evidence_nguon_test.py` | 0 | CA: 16/16 dat; DOT BIEN: 45/45 bi giet dung ly do; TU KIEM PHAN HANG: DAT (2 dot bien); TONG: DAT |
| head | `python ops/land_evidence_nguon.py --root .` | 0 | land_evidence_nguon: 12 ĐẠT · 28/28 miễn trừ (băm khớp) · 0 vi phạm · 0 KHÔNG ĐO ĐƯỢC · tổng 40; TỔNG: ĐẠT |

Kết luận nội dung sau các phép đo: yêu cầu đổi do P2 `c16-thieu-rang-q1` (ba biểu hiện cùng lớp), dù mã L6 hiện tại khớp Q1 trên 53 ca đã thử. Số lượng trong đặc tả cần đính chính thành 5/10; các dòng L6 trong lịch sử đều khớp lời khai executor, nhưng không được đánh đồng “0 L6” với rc=0 của toàn cổng.

| Severity | Slug lớp | Vị trí | Phản chứng và hướng xử lý |
|---|---|---|---|
| P2 | `c16-thieu-rang-q1` | `cay-kho/ops/land_evidence_nguon_test.py:304`, `:306`, `:307`, `:369` | c16 không thử danh sách trộn mapping/vô hướng, không thử sai kiểu bookkeeping khi trường có mặt, không thử dấu ở sâu hơn hai tầng. Ba đột biến tương ứng đều c16 rc=0; head gốc bác từng phản chứng bằng L6 rc=1, mutant cho rc=0. Bổ sung ca và đột biến mục tiêu, đòi giết bằng `TinHieuChotCa`, không lấy lỗi neo hay lỗi runtime làm tín dụng. |
| P3 | `loi-khai-bang-chung-cu` | `SPEC-r1.md:21`, `cay-kho/ops/land_evidence_nguon.py:33` | Cả hai cây có 10 hồ sơ landed true, 5 thiếu thu_hoi_cuoi; docstring “chưa nằm trên đường CI” cũng đã cũ vì registry đăng ký suite và workflow gọi registry. Owner: executor/điều phối packet. Đính chính số ở handoff, đưa vào revision kế tiếp nếu cần sửa spec đóng băng; làm rõ docstring về đường chạy gián tiếp qua test. Đây là nợ P3, không phải lý do chặn chính. |

Kết luận cuối đã chốt: **changes_requested**. Ngưỡng của prompt: không P0/P1/P2 mở mới được approve; còn **1 lớp P2 với 3 biểu hiện**. Thêm **1 lớp P3 với 2 biểu hiện** được ghi nợ bên dưới. Không phát hiện sai hành vi L6 đang có so với Q1 trong phạm vi đã đo. Finding P2 nói về răng của phép nghiệm thu, không khẳng định head hiện tại nhận nhầm các phản chứng.

Neo kiểm độc lập: HEAD `c95bd7f80a45a592f3cb089149c0c23fb4df2317`; tree `a339b7a943aa931d2dcace7cde25598d012d1b8f`; base và origin/master cùng `9f4a539b12d1d948817123d117f4bf2aedb1898f`. SPEC đo SHA-256 `a5a89622376495186ae265f18f4f6d1ce7e2b2e3b7613c61c2d96087a2c3af0b`. `git -c core.abbrev=7 diff <base> <head>` khớp byte `diff.patch`; numstat khớp byte, đúng 2 tệp, +46/-0 (Q3 đạt). Cấu hình mặc định cho băm 8 ký tự chỉ gây khác dòng index, không khác hunk. Không sửa cấu hình Git của cây nguồn.

Môi trường đo: Python 3.13.16, PyYAML 6.0.1, Linux; mọi bản sao, mã đột biến, archive và log nằm dưới `review-data/`. Hai vế được tạo bằng Git archive trong **cùng một lệnh**; không dùng worktree/checkout ghi vào kho nguồn. `TMPDIR` là đường tuyệt đối tới `review-data/tmp`; các tiến trình đột biến đều có `PYTHONDONTWRITEBYTECODE=1`. `GIT_OPTIONAL_LOCKS=0` cho các phép đo từ khi chụp snapshot. Tool `cloud_environment.environment_status` không có trong danh sách khả dụng, nên trạng thái đó không đo được; không có thao tác mạng nào.

Reviewer là Codex họ OpenAI theo context phiên, dùng công cụ thực thi shell `exec_command`, transport machine. Không có attestation độc lập cho model cụ thể, effort hoặc invocation launcher; **Q4 về đường gọi `.claude/dev/launcher.py run` không tự xác minh được từ checkout**. Không tạo lời gọi Codex lồng, không tự cấp receipt/cross_approved, không gọi GitHub. Verdict là kết quả review nội dung trên exact SHA; không cấp quyền land.

Bảng săn bổ sung (các lệnh A/B và stdout đầy đủ đã được ghi ở bảng phía trên, `ab-results.json`, `base-test.json`, `head-test.json`, `base-root.json`, `head-root.json`):

| Lệnh / phép đo | Kết quả thật | Ý nghĩa |
|---|---|---|
| `git -C cay-kho rev-parse HEAD HEAD^{tree}`; `git ... rev-parse origin/master`; SHA-256 SPEC | rc=0, các neo khớp như trên | Review đúng head/base và spec đóng băng |
| `git -c core.abbrev=7 -C cay-kho diff <base> <head>`; `git ... diff --numstat <base> <head>` | rc=0; diff và numstat khớp; +17 và +29 | Đúng write set, không có sửa hồ sơ hoặc CI |
| `python review-data/run_ab.py` | rc=0; base 15/15, 37/37; head 16/16, 45/45; cả hai root rc=0 | Hành vi nền và cây thật đều xanh; không suy răng đầy đủ chỉ từ tổng suite |
| `PYTHONDONTWRITEBYTECODE=1 python review-data/probe_behavior.py` | rc=0; 53/53 khớp; các kết quả base/head cùng đầu vào được lưu | Đo riêng biên Q1, phạm vi và lịch sử |
| `PYTHONDONTWRITEBYTECODE=1 python review-data/probe_mutations.py` | rc=0 của script đo; 8 GIET bằng rc=3/DO:c16; 3 SONG_SOT rc=0 | Script đo thành công không có nghĩa mọi mutant bị giết |
| Trích Git blobs ở cả hai SHA, parse toàn bộ 12 hồ sơ không miễn trừ | 12 có landed kiểu bool; 10 true, 2 false; 5/10 true thiếu thu_hoi_cuoi; 0 dấu trong chuỗi YAML | Lời khai 5/9 sai mẫu số; quyết định không đòi trường ấy vẫn có căn cứ |
| So stdout hai suite với regex đăng ký ở `.claude/dev/ci_dang_ky_test.py:53` bằng AST và `re.search` | rc=0, cả hai khớp marker | Định dạng tổng kết tương thích sổ CI; không phải một lần chạy CI thực |
| Snapshot byte/mode/symlink toàn cây `cay-kho/`, cả ignored/untracked và `.git`, cùng Git status/diff/index/HEAD/tree trước–sau | rc=0, không delta | Không quan sát thấy thay đổi cây nguồn tại hai mốc; không chứng minh lịch sử giữa hai mốc chưa từng ghi rồi hoàn nguyên |

Đối chiếu Q1 và `ngoai_pham_vi` từ `behavior-results.json`:

| Điều khoản | Kết quả đo trên head | Đánh giá |
|---|---|---|
| Q1.1, kiểu landed | Chuỗi true/yes/on có nháy, số 1/0/1.0, null, mapping, list đều rc=1/L6; true/True/TRUE và yes/on không nháy là bool YAML 1.1, rc=0 khi hai danh sách đúng | Kiểm kiểu sau parse, không bắt buộc cách viết literal true. Khớp spec |
| Q1.2, cả hai danh sách | Mapping thay list, chuỗi bất kể dấu, list rỗng, null, thiếu trường, phần tử vô hướng hoặc trộn phần tử đều rc=1/L6 cho từng trường. List chứa mapping rỗng được chấp nhận | Khớp quy tắc kiểu. Không chứng minh công việc/gate trong mapping đã hoàn tất hoặc có conclusion success |
| Q1.3, mọi chuỗi | Dấu CHO_DIEN nguyên văn ở khoá sâu, giá trị sâu, và nằm giữa chuỗi đều rc=1/L6. cho_dien/Cho_Dien rc=0 với hai list hợp lệ | Phân biệt hoa thường đúng literal của spec; “không còn giữ chỗ dưới mọi cách viết” sẽ là lời khai quá rộng |
| Q1.4, bản nháp | false/no/off không nháy và hai chuỗi giữ chỗ rc=0, 0 L6. Bản nháp có lời khai measured thiếu provenance vẫn rc=2 | Chỉ L6 được bỏ qua; không miễn L1–L5 |
| Khoá trùng trong trang_thai_packet hoặc trùng trang_thai_packet ở gốc | rc=2, “khoá trùng”, 0 L6, không pass | L4 chặn trước L6; lời nói “landed true luôn rc=1/L6” cần điều kiện YAML đo được |
| Status không-mapping, thiếu landed, landed ở nơi khác; dấu trong chú thích | rc=0 và không L6 cho các fixture độc lập không vướng luật khác | Đúng các loại trừ đã ghi; không yêu cầu mở scope |
| Không có lease/landed_dieu_kien/landed_ly_do | Hồ sơ tối thiểu đúng hai list rc=0 | Không tự thêm điều kiện ngoài spec |
| Q2 miễn trừ | 28/28 byte/hash khớp được bỏ qua; ví dụ plat-x8 nguyên byte rc=0/1 miễn trừ, byte đổi mất miễn trừ và rc=2 do khoá trùng trong phép thử | L5 không đổi, chạy trước parse/L6. Không suy ví dụ byte đổi này là một phép giết L6 |

Lịch sử: ba tệp được giao khớp byte với blob Git theo băm đầy đủ bên dưới; `611ef62` được lấy thêm từ Git cục bộ để kiểm nốt dòng thứ tư của lời khai. Chạy cả hai checker bằng `python <checker> --root <history-tree> --tep ops/land/pr832-wp831-land-evidence.yaml` trong bản sao đầy đủ, thay **chỉ byte hồ sơ** từng phiên bản, giữ provenance của head. Đây là đối chiếu L6 trên hồ sơ lịch sử, không tái hiện CI, mạng hoặc toàn bộ cây từng thời điểm.

| Git OID của hồ sơ | Khớp tệp giao | landed | L6 thực đo / khai | rc base / head | Vi phạm khác |
|---|---|---|---|---|---|
| `473d56a10362ea542df2894d54979d5c62b9960a` | có | True | 7/7 | 1/1 | 4 L1 ở cả hai vế |
| `ef81b987f8d8062315cfbfe8d596f9f135138c7f` | có | False | 0/0 | 0/0 | 0 |
| `611ef62fcb4fc394b9847943f2f8472ba2d59b10` | không được giao; đọc Git | False | 0/0 | 1/1 | 4 L1 ở cả hai vế |
| `79045a07b4c4feaf5d5ff74ad58d8f59176a62b7` | có | True | 0/0 | 0/0 | 0 |

`l6-lich-su-840.txt` đúng cả bốn số L6: 7, 0, 0, 0. Ở `473d56a`, 7 L6 gồm hai lỗi kiểu và năm chuỗi dấu (post_merge_checks, bookkeeping, lease.thu_hoi_cuoi, landed_dieu_kien, ho_qua_cho_802). Không được báo “base cho hồ sơ lịch sử này qua”: base đã rc=1 vì 4 L1. Ở `ef81b98`, 8 lần xuất hiện CHO_DIEN trong văn bản gồm cả chú thích; parser thấy 5 chuỗi giá trị, được phép vì landed false. 0 L6 của `611ef62` cũng không có nghĩa gate xanh (vẫn 4 L1). Bằng chứng nguyên stdout và SHA-256 byte: `history-results.json`.

Bảng đột biến độc lập: baseline c16 trên head gốc **rc=0**, không stderr. Mỗi hàng là một file module riêng và một tiến trình `python review-data/head/ops/land_evidence_nguon_test.py --mot-ca c16_l6_landed_true_phai_co_phan_hoan_tat`, đặt `LAND_EVIDENCE_NGUON_MA` tới module trong `review-data/mutations/`, `PYTHONDONTWRITEBYTECODE=1`. Neo thay thế duy nhất được đếm bằng mã (1 lần mỗi hàng). `GIET` chỉ được ghi khi rc=3 và đúng `DO:c16_l6_landed_true_phai_co_phan_hoan_tat:`; chốt do `TinHieuChotCa` theo `chay_ca`, không có KeyError/TypeError/traceback được tính công.

| Đột biến | Điểm Q1 | Trong DOT_BIEN | rc thật | Phân hạng / tín hiệu thật |
|---|---|---|---:|---|
| `L6_bo_ca_luat` | 1–4 | có | 3 | GIET: ca #840 head 473d56a |
| `L6_bo_kiem_bool` | 1 | có | 3 | GIET: landed 'true' không phải bool |
| `L6_ban_nhap_van_kiem` | 4 | có | 3 | GIET: bản nháp landed false được giữ chỗ |
| `L6_chuoi_thay_danh_sach` | 2 | có | 3 | GIET: chuỗi KHÔNG mang dấu đứng chỗ danh sách |
| `L6_danh_sach_rong_hop_le` | 2 | có | 3 | GIET: danh sách rỗng |
| `L6_phan_tu_bat_ky` | 2 | có | 3 | GIET: phần tử không phải mapping |
| `L6_bo_bookkeeping` | 2 | có | 3 | GIET: thiếu bookkeeping |
| `L6_bo_dau_giu_cho` | 3 | có | 3 | GIET: dấu trong trường chuỗi |
| `RV_L6_all_thanh_any` | 2 | không | 0 | SONG_SOT: Không phát tín hiệu DO; c16 qua |
| `RV_L6_bookkeeping_chi_can_co` | 2 | không | 0 | SONG_SOT: Không phát tín hiệu DO; c16 qua |
| `RV_L6_dau_chi_hai_tang` | 3 | không | 0 | SONG_SOT: Không phát tín hiệu DO; c16 qua |

Như vậy mỗi điểm 1–4 đã có một phép gỡ chốt riêng chết đúng lý do; tuy nhiên bảng 45/45 chỉ là tập đột biến được liệt kê, không phủ hết luật Q1. Các module và stdout nguyên văn ở `mutation-results.json`; phản chứng phân biệt head/mutant ở `mutation-counterexamples.json`.

Đo thêm toàn bộ suite với module đột biến `RV_L6_all_thanh_any.py` qua biến môi trường được test hỗ trợ:

`LAND_EVIDENCE_NGUON_MA=<đường tuyệt đối>/review-data/mutations/RV_L6_all_thanh_any.py PYTHONDONTWRITEBYTECODE=1 TMPDIR=<đường tuyệt đối>/review-data/tmp python review-data/head/ops/land_evidence_nguon_test.py` ⇒ rc=0; CA: 16/16 dat; DOT BIEN: 45/45 bi giet dung ly do; TU KIEM PHAN HANG: DAT (2 dot bien); TONG: DAT (`survivor-full-suite.json`).

Giới hạn phép đo này: bộ vòng đột biến lấy mã gốc từ HERE/head rồi sinh các module riêng, không lấy module override để dựng lại toàn bộ DOT_BIEN. Vì vậy 45/45 ở đây là kiểm chính bảng cũ trên mã gốc; **16/16** cho thấy tập ca không phân biệt all/any. Không tuyên bố đã thay mã tại chỗ rồi toàn bộ hạ tầng mutation vẫn xanh; lỗi neo nếu thay tại chỗ cũng không phải giết bằng TinHieuChotCa.

Chi tiết finding P2 `c16-thieu-rang-q1`, owner executor packet #845 (3 biểu hiện, nguồn lượt 1 trên reviewed_sha ở dòng 2):

- **A — MỌI thành CÓ ÍT NHẤT MỘT** tại `cay-kho/ops/land_evidence_nguon_test.py:305` và bảng `:371`. Ca hiện tại chỉ có list một phần tử, nên đổi lượng từ all sang any không bị bắt. Phản chứng bằng lời: landed true, bookkeeping hợp lệ, post_merge_checks có một mapping và một chuỗi thường không mang dấu; head rc=1/L6, mutant rc=0, c16 rc=0. Đây là sai Q1.2 về mọi phần tử, không phải mutant tương đương.
- **B — bookkeeping chỉ còn kiểm có mặt/có giá trị** tại `cay-kho/ops/land_evidence_nguon_test.py:306` và bảng `:372`. Ca thiếu bookkeeping chết khi bỏ hẳn trường bắt buộc, nhưng không chứng minh kiểm kiểu trường khi đã có mặt. Phản chứng bằng lời: hai trường hiện diện, post_merge_checks là list mapping, bookkeeping là mapping khác rỗng; head rc=1/L6, mutant rc=0, c16 rc=0. Sai Q1.2 dù mutant “bỏ bookkeeping” trong bảng cũ đã bị giết.
- **C — dấu bị giới hạn độ sâu** tại `cay-kho/ops/land_evidence_nguon_test.py:307` và bảng `:373`. Hai ca dấu hiện tại chỉ đi tới hai tầng đường YAML. Phản chứng bằng lời: landed true, hai list hợp lệ, một giá trị chuỗi CHO_DIEN dưới ba mapping lồng nhau; head rc=1/L6, mutant chỉ duyệt hai tầng cho rc=0, c16 rc=0. Sai Q1.3 “mọi độ sâu”.

Vá **ở đâu**: chỉ tệp test đã thuộc write_set, trong c16 và DOT_BIEN. Vá **thế nào**: thêm ca phân biệt từng tính chất trên từng trường, cả phần tử lỗi đứng trước/sau mapping hợp lệ; thêm chuỗi/khoá giữ chỗ qua mapping và list nhiều tầng; bổ sung mỗi mutant tương ứng, giữ neo duy nhất. **Ca khoá/đóng lớp**: c16 vẫn rc=0 trên gốc; từng mutant A/B/C rc=3 với đúng DO:c16, không chấp nhận lỗi neo hoặc lỗi vô can. Chạy lại A/B và giữ 12 hồ sơ không miễn trừ ĐẠT. **Nguy cơ của bản vá test**: fixture chứa từ measured hoặc positive có thể kích L1/L2 trước L6; dấu nằm trong list sai kiểu có thể che việc không duyệt dấu. Dùng fixture cô lập như mô tả, hai list hợp lệ cho phép đo dấu; không siết schema hay hoa/thường ngoài spec. Không có patch gate do reviewer soạn để executor áp mù.

Chi tiết finding P3 `loi-khai-bang-chung-cu`, owner executor/điều phối packet #845 (2 biểu hiện):

- **A — mẫu số landed cũ** tại `SPEC-r1.md:21`: “5/9” sai cả trên base và head. `git-tree-counts.json` đo từ Git blobs ở từng OID đầy đủ, cùng `real-tree-audit.json`: 10 true là pr778, pr779, pr791, pr792, pr793, pr800, pr801, pr818, pr832, pr836; 2 false là pr772 và pr823. Năm hồ sơ thiếu thu_hoi_cuoi đúng danh sách spec. `cay-kho/ops/land/pr836-wp812-land-evidence.yaml:86` cũng landed true ở base; không được loại khỏi mẫu số vì không miễn trừ. Hướng xử lý: đính chính số đo theo exact SHA trong handoff; nếu cần sửa văn bản spec, soạn revision mới theo quy tắc đóng băng, không sửa r1 để đổi băm ngầm. Phép khoá: đếm từ tập hồ sơ không miễn trừ theo byte/hash rồi lọc landed is True, không hard-code mẫu số. Nguy cơ: đếm lẫn 28 hồ sơ miễn trừ hoặc lọc bằng truthiness thay bool sẽ cho số khác.
- **B — mô tả đường CI cũ** tại `cay-kho/ops/land_evidence_nguon.py:33`: dòng “Chưa nằm trên đường CI tự động” đã có từ base, không được bản vá này gây ra. Đối chứng tĩnh: registry ở `.claude/dev/ci_dang_ky_test.py:53` đăng ký suite; workflow `.github/workflows/ci.yml:895` gọi `--chay`; c11 trong suite gọi checker trên cây thật. Hướng xử lý trong docstring (cùng write_set): mô tả chính xác CI đi qua suite/c11. Không khẳng định đã chạy GitHub Actions. Phép khoá: đối chiếu registry/workflow/c11 và marker suite; không cần thêm test riêng chỉ để soi câu văn. Nguy cơ: đổi câu thành “mọi CI đều chạy thành công” sẽ lại rộng hơn bằng chứng tĩnh. Ghi nhận nợ kế thừa, không yêu cầu đổi CI ngoài scope.

Các lời khai docstring/commit còn lại phải đọc trong giới hạn: L6 là kiểm kiểu và dấu CHO_DIEN nguyên văn trên YAML parse được và không miễn trừ; không xác minh hậu-merge gate thành công, sự thật bookkeeping, lease đã nhả hoặc quyền landed. List chứa mapping rỗng vẫn hợp lệ theo Q1.2. “landed false không đòi” chỉ áp L6; khoá trùng vẫn KHÔNG ĐO ĐƯỢC do L4. Commit khai 16/16, 45/45, +46 dòng, 12 ĐẠT và 28/28 miễn trừ đều được tái đo đúng; số lịch sử L6 cũng đúng. Câu không cổng nào bắt được ca lịch sử không được dùng làm kết luận A/B trên base hiện tại vì hồ sơ cũ vẫn vướng L1 như bảng lịch sử.

Không chạy full repository selftest, Ruff, gate phát hành hoặc CI từ xa: **not_run** trong review hẹp này; không suy chúng đạt từ targeted suite. Không có P0/P1 được phát hiện trong phạm vi review. P2 còn mở nên không đạt ngưỡng approve dù P3 có hướng xử lý. Cần executor bổ sung răng trên cây của họ và reviewer đo lại exact SHA mới.

Snapshot cuối: 4579 mục file/symlink trước, 4579 sau, **0 delta nội dung/mode/symlink và 0 delta Git** (`readonly-delta.json`). HEAD/tree vẫn giữ nguyên. Các script đo chỉ nằm trong `review-data/`; cây thật không được sửa.
