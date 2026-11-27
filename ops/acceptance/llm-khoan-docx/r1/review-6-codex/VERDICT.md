# Verdict packet #1525 r6 lượt 6 — Codex

reviewed_sha: 6781d1187c1a500b530e56017e4e2625a7dc990e

reviewed_tree: 8ef77ad3fee479906dcb8a71fb10ab6028b37f9e

base_sha: 64b7f2c14776d5d0e1d34a6be4725490956f5bec

VERDICT: REQUEST_CHANGES

## Preflight

- Checkout rời của `ducthangho/tra-luat`, HEAD detached, merge-base đúng `base_sha`, `core.abbrev=7`. Baseline chuyển tiếp #1514 là `fcb12b3873c3bec2c339029136243ed2c804ce05`. Đã đối chiếu ba phạm vi `1ee8a2441a1ef17add1f125a532aa5ec7c5e52b8..HEAD`, `fcb12b3..HEAD` và `64b7f2c..HEAD`. Verdict lượt 5 neo `3c1e1436996468419875d05a7adefe8d5bd21a76`.
- Spec có thẩm quyền trong snapshot được giao là `6781d1187c1a500b530e56017e4e2625a7dc990e:ops/specs/llm-khoan-docx-r6.md`, blob `0e5a016fc585ffca9253bbf7b65678f97f26e644`. SHA-256 của blob và tệp local cùng bằng `c2f82715d9af088f3cd20a77a8c6363dacf1dce427d77c2a3678801df55c6000`, khớp lease r6/g1, class `sensitive`. Lease còn hạn đến 19:34 UTC ngày 25-11-2026.
- Sau khi bỏ hồ sơ acceptance của #1514 theo prompt, diff từ `fcb12b3` có 37 đường dẫn, đều trong write set. SHA-256 của write set đã sắp xếp và nối LF là `f1bfa3873c81a9292e5acc0eee9297fe92ca44ef7cf127860762dd7748603471`. Năm bia mộ r1↔r2↔r3↔r4↔r5↔r6 và bia mộ #1514 r9↔#1525 r1 đều khớp hai chiều qua `thay_the_cho` và `da_bi_thay_the`. r6 là lượt 6/7 theo chỉ thị chủ kho ghi trong lease. [Đặc tả r6](../ops/specs/llm-khoan-docx-r6.md) · [Lease r6](../ops/leases/llm-khoan-docx-r6-g1-claude.yaml)
- Executor theo lease là `claude / claude_code / machine/local`, phiên được ghi `session_015GtxrZQYT3Vt8PJdXrjEKg`. Reviewer `openai_codex / codex_cli / machine`, `codex-cli 0.172.0`, sandbox `workspace-write`, chính sách approval `never`. Run `d2a1daade8004af6a9e71ea61630cb6a` qua launcher, SHA-256 snapshot `dd2da383c76673b5e62350ba59a8052ba3f9c01b0bf71d2960da8d051b71d79d`.

## Đối chiếu lượt 5 và đặc tả r6

| Mục | Trạng thái | Bằng chứng |
| --- | --- | --- |
| E1 · §2.8 · A1/B1/C1/D1 | **VÁ MỘT PHẦN** | Hai chốt trùng khóa và dấu cuối được thêm, có đột biến riêng chết. Mốc giả duy nhất, kết thúc bình thường vẫn cắt được phần đuôi khi phần đuôi dùng điểm tay, đoạn thường, bảng hoặc `numId` khác. Cửa không có đánh số tự động đã đóng từ r5. [Chọn vùng](../scripts/tl_core/llm_route.py#L948) · [Ca E1](../scripts/tl_core/llm_route_test.py#L1452) · F1 |
| E2 · §2.8 · A4/B3/C4/D3 | **ĐÃ VÁ THẬT** với toggle hai tầng | Hai loại gạch tính độc lập. Định dạng trực tiếp thắng theo từng thuộc tính. Đếm từ hai tầng bật trở lên đặt `la`, nên không âm thầm bỏ chữ của run như r5. Đột biến `wp1525_toggle_hai_tang_nhan` chết. [Tính hiệu lực](../scripts/tl_core/llm_route.py#L780) · [Ca E2](../scripts/tl_core/llm_route_test.py#L1456) |
| E3 · §2.8 · A2/B2/C2/D2 | **ĐÃ VÁ THẬT** với sửa đổi hàng/ô đã báo | `trPr/del`, `trPr/ins`, `tcPr/cellDel`, `cellIns`, `cellMerge` sinh khối lạ trước khi đến đoạn mang số. Khối trước hoặc trong Điều làm dừng. Hai ca xóa hàng và ô, hai đột biến đích chết. Lớp bộ đếm còn F3 với một cơ chế khác. [Duyệt bảng](../scripts/tl_core/llm_route.py#L744) · [Ca E3](../scripts/tl_core/llm_route_test.py#L1462) |
| E4 · §2.8 | **ĐÃ VÁ THẬT** với thuộc tính ô | Sau khi kiểm revision, `tcPr` được bỏ qua ở đúng cấp ô. Ca dương bảng có `tcW` đạt, đột biến chuyển nguyên ô vào bộ duyệt chết. [Đọc ô](../scripts/tl_core/llm_route.py#L754) · [Ca E4](../scripts/tl_core/llm_route_test.py#L1297) |
| E5 · §2.8 và §3 | **ĐÃ VÁ THẬT** với cả hai đột biến lượt 5 | Đối chứng hai khoản còn đủ sau run rỗng và run gạch, ca riêng loại chữ `moveFrom`. `wp1525_loc_bang_regex` và `wp1525_doc_chu_movefrom` đều chết bằng tín hiệu ca đích. Đường DOCX đọc XML gốc. Regex chung trong `docx_markup.py` là nợ đã khai, ngoài write set. [Hai ca E5](../scripts/tl_core/llm_route_test.py#L1285) · [Đột biến](../scripts/tl_core/llm_route_test.py#L1583) |
| E6 · §2.8 | **ĐÃ VÁ THẬT** với `ilvl` ngoài 0–8 | `lvl`, `lvlOverride` và cấp hiệu lực của đoạn đều có cửa kiểm trước khi cấp đó vào bộ đếm. Đột biến sẵn có giết nhánh định nghĩa. Giới hạn độ dài nhãn và độ phủ hai cửa còn lại xem F4, F5. [Định nghĩa và override](../scripts/tl_core/llm_route.py#L593) · [Cấp của đoạn](../scripts/tl_core/llm_route.py#L850) |
| A2/B2/C2/D2 · §2.4–2.7 | **ĐÃ VÁ THẬT** với các biểu hiện cũ đã đo | `start` vắng dùng 0, `startOverride` thật sự đè giá trị gốc, bộ đếm tách theo khóa danh sách và xóa cấp con khi cha tăng. Ca bảng lồng, wrapper bảng, rollover nhãn chữ và reset section qua chốt riêng. Liên kết cấp/style và số qua style trong Điều bị chặn theo r3. Một khe nhận dạng ID vẫn mở ở F3. [Bộ đếm](../scripts/tl_core/llm_route.py#L905) · [Ca startOverride](../scripts/tl_core/llm_route_test.py#L1271) · [Ca bảng và nhãn](../scripts/tl_core/llm_route_test.py#L1325) |
| A3/C3/D6 · §2.4/2.6/2.7 | **ĐÃ VÁ THẬT** | Lấy từ nối trong đoạn mở khoản, so định nghĩa tới hết các điểm. Chốt dấu phân cách chạy trên chữ từng đoạn và chỉ gỡ tiền tố ở điểm tay đã phân vai. Có ca chặn từ nối chỉ xuất hiện ở cấp điểm và ca phân biệt tiền tố trên đoạn đánh số tự động. [Chốt đoạn](../scripts/tl_core/llm_route.py#L1045) · [So hai vế](../scripts/tl_core/llm_route.py#L1219) |
| A5/A6/B5 · §2.4/2.5 | **ĐÃ VÁ THẬT** với các biểu hiện đã báo | Ca danh sách không hỗ trợ ngoài Điều, điểm tay liền thân và số thập phân đầu thân đều đạt. Ranh giới của đoạn mang dấu điểm tay vẫn suy từ chữ. Xem F2. [Ca A5/A6](../scripts/tl_core/llm_route_test.py#L1263) · [Ca B5](../scripts/tl_core/llm_route_test.py#L1318) |
| A7/B7/C6/D4 · §3 | **ĐÃ VÁ THẬT** với các đột biến đích lịch sử | Override khác giá trị gốc, bảng trong Điều, phần tử lạ ở tiêu đề và hàng bảng, các chốt tách của ranh giới và liên kết style có mẫu đo. R5 bỏ fallback, nên thứ tự trước fallback của B7 không còn là đường runtime. F5 ghi hai cửa mới r6 thiếu phép đo độc lập. [Các ca âm](../scripts/tl_core/llm_route_test.py#L1359) · [DOT_BIEN](../scripts/tl_core/llm_route_test.py#L1519) |
| B4/B6/C5 · §2.5/2.6 | **ĐÃ VÁ THẬT** với các phần tử đã báo | `noBreakHyphen` giữ dấu nối. `customXmlPr` là thuộc tính wrapper, `sdtContent` nội dòng được duyệt. Phần tử hiển thị chưa hỗ trợ vẫn chặn. F6 ghi hai nhóm phần tử chuẩn khác còn chặn oan. [Đọc run](../scripts/tl_core/llm_route.py#L809) · [Wrapper](../scripts/tl_core/llm_route.py#L830) |
| D5 · §2.7 | **ĐÃ VÁ THẬT** theo giới hạn đã khai | Gốc Strict bị từ chối với chẩn đoán Transitional. Ca dương kiểm thông báo và đột biến `wp1525_nhan_strict` chết. [Cửa namespace](../scripts/tl_core/llm_route.py#L893) |
| A8/B8/C7 · hướng dẫn | **ĐÃ VÁ THẬT** với các biểu hiện đã báo | Hướng dẫn nhất quán một dòng ở đường thô, phân biệt style trong và ngoài Điều, nêu cả `%N.` và `%N)`. [Hướng dẫn](../docs/GOI_AGENT_DA_NEN.md#L373) |
| §1–§2.3 · K1 | **ĐÃ VÁ THẬT** với hai đường ghép thô | `_RE_DIEM` làm từ chối cả có số và mất số. “là” không số trong nguồn có số rơi vào `return None`, kể cả khi khoản trước thiếu từ nối. Ở nguồn mất số, dòng mở “là” không có vế thuật ngữ nên không qua phép so. Có ca đủ dấu kết và đột biến điểm thô. Fixture Điều 3 và ba kết quả đã lưu đạt 8/8 mỗi kết quả. [Phân đoạn thô](../scripts/tl_core/llm_route.py#L1079) · [Ca điểm](../scripts/tl_core/llm_route_test.py#L1170) · [Ca tiếp dòng](../scripts/tl_core/llm_route_test.py#L810) · [Đối chứng tám khoản](../scripts/tl_core/llm_route_test.py#L1034) |
| §1/§2.2–§2.7 · đường CLI | **ĐẠT** ở các luồng đã khai | Chữ ký ZIP chọn DOCX, cần `--dieu` và tệp đứng riêng. Lỗi parser về rc 2. `KhongCauTruc` đã bị bỏ theo D1, nên DOCX không có numbering không lùi về văn bản thô. Không đổi đường gọi model hoặc cờ, `can_nguoi_duyet: true` giữ nguyên, `pham_vi_kiem` theo nguồn ranh giới. [CLI](../scripts/tl_core/ops_misc.py#L3025) · [Metadata và ghi tệp](../scripts/tl_core/ops_misc.py#L3123) |
| §2.1 và §3 · câu dẫn, so nguyên văn | **ĐẠT** trên dạng hỗ trợ | Không hoặc đúng một câu dẫn chuẩn trước khoản đầu. Số từ 1 liên tục, danh sách khác trong vùng bị từ chối. Khi oracle đã đủ và đúng, phép so phát hiện thiếu, gộp, cắt hoặc tráo mục bằng số, vị trí và toàn bộ hai vế. Ca CLI giả model đạt các nhánh rc 0/5/2. [Câu dẫn và cố định vùng](../scripts/tl_core/llm_route.py#L1045) · [Ca CLI](../scripts/tl_selftest.py#L32235) |

**Ranh giới còn lại ở đường thô.** K1 đã đóng ở hai nhánh ghép. Khi export làm mất phân cấp, hai dòng tự đủ hình thức định nghĩa vẫn có thể được coi là hai khoản, hoặc số tiểu mục còn lại có thể trùng dãy số khoản. Dấu điểm ngoài mẫu có thể tồn tại như chữ thường ở nguồn mất số. Phạm vi một dòng và `pham_vi_kiem` đã công bố phần cần người dùng xác nhận. Với TXT mất markup, phép so không biết chữ từng bị bỏ. Với số hiệu, `tl extract` có thể trả văn bản kèm cảnh báo chưa xác minh markup. CLI hiện chuyển tiếp cảnh báo và vẫn so với bản đó nếu extract thành công, chưa chạm CAP. Đây là đường nguồn thô kế thừa, đã ghi ở lượt 5, khác với đường lọc XML gốc của packet. [Phạm vi thô](../scripts/tl_core/llm_route.py#L1061) · [Đọc extract](../scripts/tl_core/llm_route.py#L1324) · [Cảnh báo của extract](../scripts/tl_core/extract_cache.py#L118)

## Findings

### F1 [P1] Mốc duy nhất vẫn có thể cắt bỏ phần cuối Điều — `scripts/tl_core/llm_route.py:948`

**Kịch bản và căn cứ.** Trong một trích đoạn DOCX, sau khoản đầu có một đoạn trích dẫn mở bằng tiền tố Điều kế tiếp hoặc Chương/Mục/Phần, xuất hiện duy nhất và kết bằng dấu chấm. Điểm tay, đoạn nối, bảng hoặc khoản thuộc danh sách khác ở phía sau bị loại khỏi `vung` khi vòng lặp `break`. Chốt sau mốc cắt chỉ tìm cùng `numId`. Tính duy nhất và dấu cuối chỉ loại được hai hình dạng của E1. Khi model chép đúng phần giữ lại, phép so có thể qua và CLI có thể ghi `--out` thiếu phần đuôi. Cùng cơ chế còn dùng chữ đã lọc để xác định mốc. Parser không giữ cờ chữ đã bỏ ở mốc, nên chốt B1 về đoạn ranh giới mang chữ đã bỏ không còn được thực thi độc lập. P1 vì oracle cấu trúc có thể bị rút ngắn trước phép so. [Điểm cắt](../scripts/tl_core/llm_route.py#L948) · [Cửa sau điểm cắt](../scripts/tl_core/llm_route.py#L1000) · [Bỏ chữ](../scripts/tl_core/llm_route.py#L823)

**Đề xuất.** Tại `doc_dieu_docx`, yêu cầu một tín hiệu cấu trúc cho vị trí kết thúc hoặc báo cấu trúc mơ hồ trước khi bỏ phần sau. Giữ thông tin revision của đoạn ứng viên cho chốt B1. Ca đóng lớp cần phân biệt mốc thật với mốc giả duy nhất trong bản trích, kể cả khi phần sau không cùng `numId`. Chốt quá chặt có thể từ chối heading gõ tay hợp lệ, nên giữ đối chứng cho Điều kế tiếp và giới hạn mốc có bằng chứng.

### F2 [P2] Dấu điểm gõ tay đủ để nhập một định nghĩa độc lập vào khoản trước — `scripts/tl_core/llm_route.py:1014`

**Kịch bản và căn cứ.** Một khoản tự động mang lời dẫn nhóm đã có từ nối cấp khoản. Các đoạn kế tiếp có dấu gạch hoặc dấu điểm gõ tay, mỗi đoạn là một định nghĩa độc lập theo bố cục của người soạn. Parser dùng duy nhất tiền tố chữ để nhập toàn bộ các đoạn vào khoản trước. Việc chỉ dò “là” ở đầu khoản bảo vệ A3, nhưng vẫn cho qua khi lời dẫn nhóm đã có “là” và model chép cả nhóm thành một định nghĩa. Đây là biến thể bố cục của K1 trong đường cấu trúc. P2 vì cần mẫu nhóm có điều kiện, dấu tay và đầu ra chép đúng khối đã gộp. Cờ duyệt ranh giới vẫn hiện. [Mẫu dấu tay](../scripts/tl_core/llm_route.py#L526) · [Ghép đoạn](../scripts/tl_core/llm_route.py#L1011) · [So đầu khoản](../scripts/tl_core/llm_route.py#L1235)

**Đề xuất.** Xác minh quan hệ thụt lề hoặc cấp danh sách ở nhánh điểm tay, và dừng khi không phân biệt được nhóm định nghĩa với các điểm thật. Ca đóng lớp cần giữ điểm tay liền thân hợp lệ và từ chối lời dẫn nhóm có các định nghĩa riêng. Yêu cầu bằng chứng thụt lề có thể chặn nguồn Word đã chuẩn hóa phẳng, nên khai rõ dạng được nhận.

### F3 [P1] Khóa ID dạng chuỗi có thể làm đếm thiếu mục trước Điều — `scripts/tl_core/llm_route.py:610`

**Kịch bản và căn cứ.** ID đánh số OOXML có giá trị nguyên. Phần khai báo trong numbering và khoản trong Điều có thể cùng cách viết, trong khi một đoạn trước Điều dùng dạng từ vựng khác của cùng số nguyên, chẳng hạn khác số chữ số 0 đệm. `_doc_danh_so` và `_phan_tich_doan` giữ nguyên các chuỗi ID. Đoạn trước Điều không tra được danh sách, bộ đếm bỏ qua và khoản đích có thể được gán 1 thay vì 2. Dãy sau đó vẫn liên tục theo bộ đếm nội bộ. Cùng chỗ so chuỗi làm yếu phép nhận dạng danh sách còn tiếp sau mốc cắt. P1 vì kết quả có thể mang số khoản sai trong khi đi qua phép so. [Khai báo danh sách](../scripts/tl_core/llm_route.py#L608) · [ID của đoạn](../scripts/tl_core/llm_route.py#L850) · [Khóa bộ đếm](../scripts/tl_core/llm_route.py#L916)

**Đề xuất.** Chuẩn hóa ID số tại lúc đọc ở cả định nghĩa, style và đoạn, giữ nghĩa đặc biệt của ID 0 và báo trùng định nghĩa sau chuẩn hóa. Đo cùng số Word khi nguồn dùng một cách viết chuẩn và khi tham chiếu trước Điều biểu diễn số nguyên theo cách khác. Thêm đối chứng hai `numId` thực sự khác để tránh vô tình hợp nhất bộ đếm.

### F4 [P2] Giới hạn cấp chưa giới hạn độ dài nhãn chữ sinh ra — `scripts/tl_core/llm_route.py:690`

**Căn cứ.** `start` và `startOverride` vào bộ đếm qua giá trị số nguyên, chưa có giới hạn độ dài nhãn. `_chu_cai` lặp một ký tự theo bậc của số này. Một tham số đếm lớn trong XML nhỏ có thể tạo nhãn rất dài ở cấp điểm hợp lệ, rồi bị sao chép khi nối điểm vào khoản. Giới hạn thành phần ZIP và cấp 0–8 đều đã qua trước đó. P2 vì tác động là tài nguyên của tiến trình đọc tệp. [Giá trị bắt đầu](../scripts/tl_core/llm_route.py#L605) · [Dựng nhãn](../scripts/tl_core/llm_route.py#L690) · [Nối nhãn vào khoản](../scripts/tl_core/llm_route.py#L1027)

**Đề xuất.** Tại điểm dựng nhãn, chặn độ dài vượt ngân sách trước khi nhân chuỗi, và bảo vệ cả tổng chữ sinh từ các nhãn. Ca đóng lớp cần xác nhận lỗi có kiểm soát và giữ các nhãn qua Z cùng override thông thường. Ngưỡng quá thấp sẽ từ chối danh sách dài hợp lệ, nên chọn và công bố giới hạn độ dài theo đầu ra.

### F5 [P2] Hai cửa miền `ilvl` thiếu ca đích riêng — `scripts/tl_core/llm_route_test.py:1468`

**Bằng chứng.** Ca E6 và đột biến có sẵn chỉ thay cửa ở `abstractNum/lvl`. Hai bản sao tạm, mỗi bản vô hiệu hóa đúng một cửa ở `lvlOverride` hoặc ở đoạn, đều trả rc 0, 59/59 ca và 164/164 đột biến có sẵn. Tiêu chí độ phủ kiểu A7/§3 còn thiếu hai phép đo. P2 vì cửa sản phẩm hiện có, hồi quy xóa từng cửa chưa bị suite bắt. [Ca hiện tại](../scripts/tl_core/llm_route_test.py#L1468) · [Neo đột biến hiện tại](../scripts/tl_core/llm_route_test.py#L1582)

**Đề xuất.** Khóa từng cửa bằng ca đích phân biệt xác thực cấp với lỗi thiếu định nghĩa hoặc lỗi trước đó. Mỗi đột biến phải chết bằng tín hiệu của ca đó và có đối chứng cấp hợp lệ. Đo đúng hợp đồng từ chối để tránh khóa cứng câu chẩn đoán.

### F6 [P2] Danh sách phần tử cho phép từ chối một số cách lưu hợp lệ của Word — `scripts/tl_core/llm_route.py:531`

**Kịch bản và căn cứ.** Tab căn lề `w:ptab` có thể xuất hiện trong run ở bố cục Word. Nó tách hiển thị mà không bổ sung chữ, nhưng chưa có ánh xạ tương tự `w:tab` và làm đoạn rơi vào `la`. Với tài liệu dùng Track Changes để chuyển chữ, các cặp mốc phạm vi `moveFromRangeStart/End` và `moveToRangeStart/End` có thể nằm cạnh wrapper `moveFrom`/`moveTo`. Bộ đọc khai hỗ trợ nội dung wrapper, nhưng các mốc đồng hành rơi vào nhánh khối hoặc phần tử lạ. Dạng Word hợp lệ có thể bị rc 2 dù phần chữ và cấp danh sách vẫn đọc được. P2 vì đây là chặn oan. Tần suất xuất hiện theo từng exporter chưa được đo. [Danh sách phần tử](../scripts/tl_core/llm_route.py#L531) · [Cửa run](../scripts/tl_core/llm_route.py#L809) · [Cửa nội dòng](../scripts/tl_core/llm_route.py#L830)

**Đề xuất.** Chuẩn hóa tab căn lề như khoảng trắng ở đúng cấp run. Xác thực phạm vi move theo cặp và theo cấp XML trước khi xử lý mốc. Đo dạng Word vừa có mốc phạm vi vừa có chữ chuyển đi/chuyển đến. Giữ chặn khi mốc không cân hoặc có sửa dấu đoạn, vì bỏ mọi mốc vô điều kiện có thể làm lọt thay đổi cấu trúc.

### Lịch sử theo lớp

| Slug lớp | Lượt 6 và phép kiểm đóng lớp |
| --- | --- |
| `ranh-gioi-khoan` | F1 P1 tiếp E1/D1/C1/B1/A1. F2 P2 là biểu hiện ở điểm tay của cùng lớp, kế thừa hình dạng K1. Hai cơ chế cần kiểm độc lập, gồm chọn mốc cuối Điều và chứng cứ quan hệ cha con trong vùng. |
| `docx-so-hien-thi` | E3 đóng ở cấu trúc bảng, F3 P1 còn mở ở định danh số. Kiểm số Word khi cách viết ID thay đổi và khi ID thực sự khác nhau. |
| `docx-markup-du-thao` | Đóng E2, hai biểu hiện D3/E5 về XML gốc và chữ chuyển đi có đối chứng. Kiểm mốc ranh giới mang revision nằm ở F1. |
| `docx-gioi-han-bo-dem` | E6 đóng ở miền cấp, F4 P2 còn ở kích thước nhãn. Giới hạn cấp và số lượng ký tự sinh ra cần hai phép kiểm. |
| `do-phu-chot-docx` | Hai biểu hiện E5 đóng. F5 P2 còn hai đột biến bổ sung sống. |
| `docx-chu-hien-thi` | E4 đóng ở `tcPr`. F6 P2 còn ở tab căn lề và metadata phạm vi move, cần xác định ngữ nghĩa theo vị trí. |

Lượt này còn **0 P0, 2 P1, 4 P2, 0 P3** trên 5 lớp. Trong 6 lớp mở của lượt 5, đóng 1 lớp (16,7%). Hai chuyển tiếp liên tiếp dưới 50% và lớp ranh giới lặp lại đủ điều kiện Review Rescue Checkpoint theo §12. Trần lời gọi hiện dùng 6/7. [Protocol §8.3](../docs/PROTOCOL_DA_PHIEN.md#L812) · [Protocol §12](../docs/PROTOCOL_DA_PHIEN.md#L1129) · [ADR-0060 M1–M2](../docs/adr/0060-dieu-kien-merge-va-moc-ready.md#L32)

## Kết quả test và đột biến

Linux x86_64, Python 3.13.18, Git 2.43.0. Tắt ghi bytecode Python. Log, mã thoát và các bản sao nằm ở `/tmp/wp1525-r6-review.UWhPEKVl/`. Hai bản sao sạch head/base được clone từ object Git local, checkout detached và ghim `core.abbrev=7` như nhau. Base tree là `0cc14e79cecd2ce44bc4dc6cff92cadb31fd7ee4`.

| Lệnh | Trạng thái | Mã thoát và bằng chứng |
| --- | --- | --- |
| `python scripts/tl_core/llm_route_test.py` | `passed` | rc 0, **59/59** ca, **164/164** đột biến bị giết, gồm **67/67** tên `wp1525_*`. Runner áp mỗi cặp neo/thay trên module tạm và chỉ ghi giết khi ca đích ném `TinHieuChotCa`. `llm.stdout`. |
| Cùng lệnh trên hai bản sao E6 bổ sung | `failed` về độ phủ | Mỗi bản chỉ bỏ một cửa, tại `llm_route.py:620` hoặc `:861`. Cả hai lần đo hợp lệ đều rc 0, 59/59 và 164/164. Hai đột biến bổ sung sống, 0/2 bị giết. `e6_override.patch`, `e6_doan.patch`, `e6_override_rerun.stdout`, `e6_doan_rerun.stdout`. |
| `python scripts/tl.py --deterministic workflow-audit --strict --json` | `passed` | rc 0, `ok=true`, 26 card, 60 task, 194 lệnh, 0 lỗi, 0 cảnh báo. `workflow.stdout`. |
| `python scripts/tl.py --deterministic golden-test --json` | `passed` | rc 0, `ok=true`, 20/20 ca và 20/20 bản chiếu ổn định, 19/20 byte thô ổn định. `hygiene_sweep_fixture` có `raw_stable=false` và diff bản chiếu rỗng. `golden.stdout`. |
| `python scripts/tl.py release-verify RELEASE_MANIFEST.json --strict --json` | `passed` trên bản sao sạch của head | rc 0, `ok=true`, 187/187 tệp, 0 thừa/sai/thiếu, `package_hash_match=true`, hash `e6a9ca3152055fee6cffb70fa482771590ac82ee3460bde0ab8eae339ae197ba`. Lượt trên checkout chứa verdict trả rc 2 với tệp thừa duy nhất là `.review/VERDICT.md`. `release_clean.stdout`, `release.stdout`. |
| `python ops/lease_publish.py check --root . ops/leases/llm-khoan-docx-r6-g1-claude.yaml` | `passed` cục bộ | rc 0, “ĐĂNG ĐƯỢC”, Issue #1525, neo `64b7f2c14776`, hết hạn `2026-11-25T19:34:00Z`. Hai lớp GitHub của lease `not_run`. `lease.stdout`. |
| `python scripts/tl.py --selftest` | `failed` trên head và base | rc 1 ở cả ba lượt. Checkout được giao và bản sao head đều **1774/1790**. Base **1773/1789**. Transport selftest **12/12** ở cả ba. `cmp` danh sách ca đỏ head/base rc 0. So mọi dòng trạng thái, khác biệt duy nhất là `[OK] r1525_llm_khai_niem_tep_docx_cau_truc` thêm ở head. `selftest.stdout`, `self_head.stdout`, `self_base.stdout`. |
| `python scripts/tl.py --deterministic determinism-audit --strict --json` | `passed` | rc 0, `ok=true`, 15/15, phạm vi mặc định `full=false`. `determinism.stdout`. |
| `python scripts/tl.py --deterministic doc-claims-check --strict --json` | `failed` trên head và base | rc 2/2, cùng 131 tệp quét và một cờ cứng L2 `SHA_NOT_A_COMMIT` tại `docs/PROTOCOL_DA_PHIEN.md:1680`. `git cat-file -t 9941d8af52aeede1c78ea4e232fbe9a8d5272033` rc 128 trên kho được giao. `doc_claims_head.stdout`, `doc_claims_base.stdout`. |
| `ruff check --no-cache --select F --output-format concise scripts/tl.py` | `failed` tuyệt đối, đạt delta 0 | Ruff 0.16.9, rc 1/1, cùng 12 F821 và 0 F401 ở head và base. `cmp` stdout rc 0. `ruff_head.stdout`, `ruff_base.stdout`. |
| Cùng lệnh Ruff trên `scripts/tl_core/llm_route.py scripts/tl_core/llm_route_test.py` | `passed` | rc 0, không có chẩn đoán F. `ruff_module.stdout`. |
| `loi_ruff_ci()` trong `.claude/dev/ci_dang_ky_test.py` qua `python -B -c` | `passed` về pin/probe contract | rc 0, `RUFF_CONTRACT 3 []`. Đây là kiểm hợp đồng YAML, đo lint thật ở hai dòng riêng. `ruff_contract.stdout`. |
| `git diff --check fcb12b3 HEAD` và `git diff --check 64b7f2c HEAD` | Packet `passed`, toàn PR `failed` | rc 0 và 2. Ba dòng Markdown hard break đã có trong hồ sơ #1514 lượt 8. `git diff --check 64b7f2c fcb12b3` cũng rc 2 với đúng ba dòng đó. [Hồ sơ](../ops/acceptance/llm-ranh-gioi-khoan/r1/review-8-codex/VERDICT.md#L3) |

Cả head và base có đúng 14 ca thuộc `r973_bootstrap_*`, `wp433_*` và `wp727_tl_gws_refresh` đỏ khi `/tmp/.git` rỗng có mặt, cùng hai ca `r226_nguong_l2_troi_theo_abbrev_va_ci_ghim` và `r268_l2_trichotomy_theo_trang_thai_object` đỏ. Đây là bằng chứng delta 0 ở tập ca đỏ, còn yêu cầu selftest N/N vẫn chưa đạt trong môi trường được giao.

Lần đầu chạy hai bản sao đột biến E6 thiếu đường import `docx_markup`. Mỗi lệnh trả rc 1, 59/59 ca và 163/164 đột biến vì đột biến sẵn có về regex gặp `ModuleNotFoundError`. Đã chạy lại với `PYTHONPATH` trỏ tới `scripts/` của exact head để dùng helper sẵn có. Kết quả hợp lệ là hai lượt `_rerun` trong bảng. Không có fixture hoặc ca test mới.

## Không đo được

- Các kịch bản F1–F4 và F6 được suy ra từ mã. Chưa chạy trên tệp Word/Google Docs mới hay đo tỷ lệ xuất hiện của mốc giả, ID khác dạng chữ, tab căn lề, range move, hoặc mức tài nguyên khi nhãn dài. Chưa đối chiếu Word thực tế khi danh sách bỏ qua cấp cha hoặc trộn `ilvl` trực tiếp với cấp khai trong style. Suite đo reset cấp con trong bố cục mẫu và các chốt từ chối liên kết không hỗ trợ.
- Lượt này không dùng model thật. Windows bản địa và Windows CI `not_run`. Toàn PR chạm tiêu chí `required` của ADR-0060 M3 vì thêm dòng test Python có `encoding=`. CI và readback head/authority trên GitHub `not_run` theo phạm vi offline. Không có phép bắt buộc nào được báo `skipped` thay cho mã thoát. [ADR-0060 M3](../docs/adr/0060-dieu-kien-merge-va-moc-ready.md#L43) · [Dòng test](../scripts/tl_selftest.py#L32357)
- Model/effort phục vụ và mã thoát terminal của chính lượt launcher là `KHONG_DO_DUOC` tại thời điểm ghi verdict. `run.json` của đúng run đang ở `dang_chay`. Bề mặt và transport lấy từ bản ghi run, sandbox từ chính môi trường thực thi. Không suy model từ CLI version hay tài khoản đăng.

## Readback

Selftest trên checkout được giao sinh hai thư mục ignored `references/golden/fixtures/` và `scripts/.tl_state/`. Đã chuyển cả hai sang `head-generated/` ở scratch. Snapshot đầu/cuối khớp exact HEAD/tree và diff tracked/index rỗng. Trạng thái ignored trở về `.codex/` có sẵn, tệp untracked duy nhất là verdict. Kiểm này xác nhận trạng thái tại hai thời điểm, không kiểm lịch sử mọi lần ghi hoặc nội dung riêng dưới `.codex/`.

ADR-0060 M1 yêu cầu 0 P0/P1/P2 mở. Candidate còn 2 P1 và 4 P2. Các cổng cục bộ và snapshot offline cũng chưa đủ điều kiện merge.

P2_mo: 4

VERDICT: REQUEST_CHANGES
