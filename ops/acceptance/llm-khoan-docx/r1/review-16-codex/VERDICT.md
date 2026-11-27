# Verdict packet #1525 r16 lượt 16 — Codex
reviewed_sha: 7a913aa327ff942fff82f616ca96ea38dbfd4feb
reviewed_tree: e6f5e155e6ff2c8ecf1961e3d03e50adfa2fcc56
base_sha: 64b7f2c14776d5d0e1d34a6be4725490956f5bec

## Preflight

- Checkout độc lập, HEAD detached, origin cục bộ trỏ `ducthangho/tra-luat`. Base, mốc #1514 `fcb12b3873c3bec2c339029136243ed2c804ce05` và mốc bản vá `8fb9c29f87b8e0b2f9b4aa6a179df2b33180e2ba` đều là tổ tiên của exact head. Cây và index lúc nhận sạch, với `.codex/` thuộc nhóm ignored.
- Packet #1525 r16/g1, `sensitive`, lượt 16/16, quota gọi model thật để test bằng 0. SHA-256 đặc tả trên đĩa và blob của head cùng `b78ea28c2bbae0e8f73d783174382834a5c90d1e7da52fa4b840de2f50219035`, khớp lease. Băm lại **17/17** spec, so **16/16** cặp `thay_the_cho` ↔ `da_bi_thay_the` từ #1514 r9 qua #1525 r1 đến r16, cùng branch, base và generation. Lease r16 là đầu chuỗi, hiệu lực 02:15–10:15 UTC ngày 26-11-2026, launcher bắt đầu 02:16:30 UTC. [Spec](../ops/specs/llm-khoan-docx-r16.md) · [Lease](../ops/leases/llm-khoan-docx-r16-g1-claude.yaml) · [Lease #1514 r9](../ops/leases/llm-ranh-gioi-khoan-r9-g1-claude.yaml#L97)
- Tập ghi gồm **91** đường dẫn, SHA-256 `471172aa6239b2111ea403d2bd80ea4545525b61b78f20081debb8887f21fa8b`. Có **8/8** đường dẫn của bản vá r16 và **87/87** đường dẫn của packet trong tập, sau khi loại bốn tệp hồ sơ #1514 theo prompt. Diff toàn PR có **135** đường dẫn, gồm lịch sử #1514. `git merge-base --is-ancestor` trả rc 0 với cả ba mốc.
- Reviewer `openai_codex / codex_cli / machine`, run `186f091a283a4d50827cd37e179a20b1`, launcher 1.6.2, Codex CLI 0.172.0. SHA-256 prompt `0384f7f4317d524144d0c75bde6a230569f350b5ae17da5fda0db9974c9ee523` khớp run và checkpoint. Executor `claude / claude_code / machine/local` theo lease. Đo trên Linux x86_64, Python 3.13.18, Git 2.43.0, `core.abbrev=7`, `PYTHONDONTWRITEBYTECODE=1`, sandbox workspace-write với Git metadata chỉ đọc.

## Đối chiếu lượt 15 và đặc tả r16

So với lượt 15 tại `b5cff4212a6abf052c74c772a525f54950b32b5e`. Các hàng A–Q đối chiếu các biểu hiện trong verdict gốc với quy tắc r16 còn hiệu lực. [Lượt 15](../ops/acceptance/llm-khoan-docx/r1/review-15-codex/VERDICT.md) · [Lịch sử review](../ops/acceptance/llm-khoan-docx/r1) · [§2.18](../ops/specs/llm-khoan-docx-r16.md#L215)

| Mục | Trạng thái | Bằng chứng |
| --- | --- | --- |
| R1 / Q1 / N1 · §2.16–2.18 · Tiền tố trong thân DOCX | **VÁ MỘT PHẦN** | Các ca `Cf` chen với dấu tổ hợp, NFD, bộ chọn biến thể, chữ không NFC và dấu gõ tay sau `Cf` đều bị chặn. Các đột biến DOCX bỏ chốt chung, NFC, `Cf` và `Mn` đều bị giết. Phép chiếu vẫn giữ ký tự mặc định vô hình nhóm `Lo`; chốt nhóm `Cc` chạy sau bước gộp khoảng trắng. Xem S1–S2. [Ca](../scripts/tl_core/llm_route_test.py#L1533) · [Mã](../scripts/tl_core/llm_route.py#L548) |
| R2 · §2.18 · Số gõ tay ngoặc kín | **ĐÃ VÁ THẬT** cho cú pháp R2 | Nhánh ngoặc kín đứng riêng, nên thân dính chữ số vẫn bị chặn. Đối chứng số thập phân đạt. Hai đột biến bỏ nhánh ngoặc kín và nuốt số thập phân đều bị giết. [Mẫu](../scripts/tl_core/llm_route.py#L574) · [Đột biến](../scripts/tl_core/llm_route_test.py#L1717) |
| R3 · §2.18 · Điểm bị che ở đường thô | **VÁ MỘT PHẦN** | Ba ca r16 `Cf` trước dấu điểm bị chặn, nguồn đối chứng sạch đạt, đột biến bỏ chốt đường thô bị giết. Ca cùng cơ chế với ký tự vô hình nhóm `Lo` và việc tách tại `Cc` còn S1–S2. [Ca](../scripts/tl_core/llm_route_test.py#L648) · [Mã](../scripts/tl_core/llm_route.py#L1206) |
| §1 và §2.2 · Bất biến và CLI | **ĐẠT** trong phạm vi ca sẵn có | ZIP đi đường DOCX với `--dieu` và không kèm số hiệu. Nguồn chữ và `<số hiệu>` giữ tuyến thô. `can_nguoi_duyet: true` và `pham_vi_kiem` lấy theo tuyến thực tế. Logic `goi`, `duong_api`, `duong_sub`, `_chay_co_moc` giữ nguyên so với #1514 r9. Điều 3 và từng kết quả trong ba kết quả lưu đều 8/8. [CLI](../scripts/tl_core/ops_misc.py#L3025) · [Đầu ra](../scripts/tl_core/ops_misc.py#L3126) · [Hồi quy](../scripts/tl_core/llm_route_test.py#L1067) |
| A1/B1/C1/D1/E1/F1/G6/H1 · §2.4–2.11 · Vùng Điều | **HẾT ĐỐI TƯỢNG do hợp đồng r7** cho điểm cắt, đếm trước Điều và lùi về thô. **ĐÃ VÁ THẬT** cho các dạng tiêu đề đích, bảng và khối lạ đã báo. | Đoạn đầu có nội dung phải khớp nguyên mẫu tiêu đề và đúng số; vùng kéo tới hết tài liệu. Bảng/khối lạ chặn toàn tệp. DOCX không có đánh số ném `ValueError`; CLI đi rc 2. `KhongCauTruc` đã rời tuyến. S1 thuộc chốt tiền tố trong vùng mới. [Định vị và phân vùng](../scripts/tl_core/llm_route.py#L1085) · [Không có số](../scripts/tl_core/llm_route.py#L1123) |
| A2/A5/B2/C2/D2/E6/F3–F5/G1/G3/H4/J1/J3/K3/L4/M2/N2 · §2.4–2.16 · Đánh số | **ĐÃ VÁ THẬT** với các dạng đã báo, **HẾT ĐỐI TƯỢNG** cho đếm ô bảng và tự dựng cấp tổ tiên. | `start` vắng lấy 0, `startOverride` có đối chứng khác `start`; bộ đếm theo `numId` và đặt lại cấp sâu hơn. Chặn nhảy cấp, danh sách thứ hai, danh sách dựa style, ID/cấp lỗi khi dùng và số vượt trần. Khoản cấp thấp nhất phải dùng decimal với nhãn của chính cấp và dãy 1..N. ID không chuyển qua `int()`; nhãn chữ lặp theo Word. `lvlText` ngoài tập dấu bị chặn; S2 ghi phần khoảng trắng Unicode. [Định nghĩa](../scripts/tl_core/llm_route.py#L688) · [Đếm](../scripts/tl_core/llm_route.py#L1065) · [Nhãn](../scripts/tl_core/llm_route.py#L848) |
| A3/C3/D6 · §2.4–2.9 · Từ nối và dấu phân cách | **ĐÃ VÁ THẬT** | So dấu phân cách trên chữ cả đoạn, kể cả cấp con. Dò từ nối trong đầu khoản, ngoài ngoặc/trích dẫn và trước hai chấm cấp khoản. [Kiểm đoạn](../scripts/tl_core/llm_route.py#L1172) · [Phép so](../scripts/tl_core/llm_route.py#L1348) |
| A4/B3/C4/D3/E2/E5/J2/K1 #1525 · §2.4–2.13 · Dự thảo | **ĐÃ VÁ THẬT** với các dạng đã báo trên DOCX; nợ E5 ở bộ lọc cũ đã ghi trong đặc tả. | Đọc XML gốc, bỏ `del`/`delText`/`moveFrom`, giữ `ins`/`moveTo`. Gạch đơn/kép xét riêng qua mặc định, style và định dạng trực tiếp. Chặn toggle không xác định, sửa dấu đoạn, mốc move lẻ/thiếu ID và phần tử `mc:` trong ba part. [Run](../scripts/tl_core/llm_route.py#L917) · [Dấu đoạn](../scripts/tl_core/llm_route.py#L1033) |
| B4–B6/C5/D5/E3–E4/F6/G4/H5/J5/N3 · §2.5–2.16 · Phần tử và bố cục | **ĐÃ VÁ THẬT** với biểu hiện gốc, **HẾT ĐỐI TƯỢNG** với sửa hàng/ô và thuộc tính ô do r7. | Hỗ trợ `noBreakHyphen`, `ptab`, wrapper `customXml` và `sdt` nội dòng, mốc move cân và ngắt trang/cột cuối đoạn hiệu lực. Chặn Strict và khối ngoài namespace Word. Mốc quyền chỉnh sửa trong đoạn còn S3. [Danh sách phần tử](../scripts/tl_core/llm_route.py#L575) · [Duyệt](../scripts/tl_core/llm_route.py#L877) |
| A6/B5/F2 · §2.5/2.9 · Điểm gõ tay và câu dẫn | A6 **HẾT ĐỐI TƯỢNG do hợp đồng r7**. B5/F2 **ĐÃ VÁ THẬT** trên ca gốc. | Điểm phải là cấp con cùng danh sách. Đoạn có chữ và không đánh số sau khoản đầu bị từ chối. Trước khoản đầu cho phép vắng câu dẫn hoặc đúng một đoạn khớp nguyên mẫu. [Phân vai](../scripts/tl_core/llm_route.py#L1140) · [Câu dẫn](../scripts/tl_core/llm_route.py#L1182) |
| G2/H2/J4/L1/L5 · §2.10–2.14 · Part và encoding | **ĐÃ VÁ THẬT** | URI quan hệ Transitional đầy đủ. Part chính theo quan hệ gốc, numbering/styles theo quan hệ của chính part đó. Parser nhận bytes để tự đọc encoding. Có ca part đổi tên và UTF-16. [Quan hệ](../scripts/tl_core/llm_route.py#L647) · [Parser](../scripts/tl_core/llm_route.py#L1027) |
| K2/L2/L3/M1 · §2.13–2.16 · Tiền tố cấu trúc | **ĐÃ VÁ THẬT** cho các dạng cũ đã báo, **HẾT ĐỐI TƯỢNG** cho phép suy tiêu đề theo dấu câu cuối thay bằng N1. | Chương/Mục/Phần dùng La Mã viết hoa, số, từ chỉ thứ tự hoặc chữ hoa. Điều dùng chốt tiền tố, áp cả khi thiếu dấu sau số hoặc khi dẫn chiếu ở đầu. S1 nêu giới hạn nhìn thấy tiền tố. [Mẫu](../scripts/tl_core/llm_route.py#L527) · [Ca](../scripts/tl_core/llm_route_test.py#L1517) |
| A7/B7/C6/D4/E5/F5/G5/H3/J4/K4 · §3 · Bằng chứng đo | **ĐÃ VÁ THẬT** với các ca và đột biến lịch sử còn áp dụng; **VÁ MỘT PHẦN** cho độ phủ lớp r16. | Bộ dương đo điểm, ngắt, markup và reset; bộ âm có ca trên đúng chốt, gồm bảng, cấu trúc lạ, nhãn và quan hệ đổi tên. §3 mô tả đúng tệp một Điều. Ca r16 đo `Cf`, `Mn`, NFC và ngoặc kín; S1–S3 cần ca khác để đóng lớp. [Ca dương](../scripts/tl_core/llm_route_test.py#L1259) · [Harness](../scripts/tl_core/llm_route_test.py#L1979) |
| A8/B8/C7/L6/Q2 · Hướng dẫn | **ĐÃ VÁ THẬT** với các biểu hiện đã báo. | Hướng dẫn một dòng cho nguồn thô, một Điều cho DOCX, điểm tự động, giới hạn style và dạng nhãn. Chỉ dẫn giữ câu chữ nguồn khi dẫn chiếu ở đầu bị chặn. [Hướng dẫn](../docs/GOI_AGENT_DA_NEN.md#L373) |
| K1 #1514 · §2.3 · Điểm và tiếp dòng | **ĐÃ VÁ THẬT** với hai nhánh ghép gốc. | Dòng khớp `_RE_DIEM` bị từ chối dù nguồn có số hay mất số. Với nguồn có số, dòng mở bằng “là” là dòng không số và bị từ chối. Với nguồn mất số, dòng mở bằng từ nối không có thuật ngữ, nên phép so hai vế từ chối. S1–S2 nằm ở nhận dạng đầu dòng và tập dòng, trước hai chốt cũ. [K1 nguồn](../ops/acceptance/llm-ranh-gioi-khoan/r1/review-10-codex/VERDICT.md#L35) · [Ca tiếp dòng](../scripts/tl_core/llm_route_test.py#L815) · [Phân đoạn](../scripts/tl_core/llm_route.py#L1217) |

### Đường tới kết quả được chấp nhận

- **Cấu trúc.** Khi danh sách chuẩn được dựng đúng, `lech_nguyen_van` bắt đầu ra bỏ, gộp, cắt hoặc tráo khoản bằng số thứ tự, vị trí, tổng mục và so trọn hai vế, giữ xuống dòng giữa các điểm. Chữ đã lọc khỏi DOCX cũng lệch nếu model đưa lại. S1 có thể làm danh sách chuẩn sai từ trước phép so. [Phân vai](../scripts/tl_core/llm_route.py#L1140) · [So nguyên văn](../scripts/tl_core/llm_route.py#L1348)
- **Thô.** Chốt kiểm theo dòng, mức bảo đảm đã khai. Hai dòng không có số, đều có hai vế và kết câu, có thể được nhận thành hai khoản dù bố cục trước export chỉ có một khoản. Dấu đầu dòng nhìn thấy ngoài mẫu, chẳng hạn bullet tròn đặc khác `•`, cũng có thể thành chữ đầu thuật ngữ của nguồn mất số. Hai mục này minh họa giới hạn nhận dạng của đường thô; S1–S2 nêu phần vi phạm tính chất từ chối ký tự r16. Văn bản mất metadata gạch/xóa có thể vẫn qua so trên đúng chuỗi đã mất metadata. Tuyến số hiệu dừng khi thấy CAP, còn cảnh báo `[markup]` được chuyển ra stderr; nợ regex E5 thuộc bộ lọc cũ. [Đường thô](../scripts/tl_core/llm_route.py#L1188) · [CAP](../scripts/tl_core/llm_route.py#L1463) · [Cảnh báo](../scripts/tl_core/ops_misc.py#L3083)

## Findings

### S1 [P1] Ký tự Unicode trống thuộc nhóm chữ cái có thể che tiền tố Điều — `scripts/tl_core/llm_route.py:548`

**Kịch bản và căn cứ.** Hangul Filler U+3164 là ký tự mặc định bỏ qua khi hiển thị thuộc nhóm `Lo`, đứng riêng vẫn ở NFC. Ở môi trường trình bày nó như khoảng trống, một tiêu đề Điều đặt sau ký tự ấy vẫn nhìn như tiêu đề. `_ky_tu_la` cho qua vì thiếu thuộc tính này, còn `_dau_doan` giữ ký tự đầu vì `isalnum()` là đúng. Regex neo đầu vì thế không thấy tiền tố. Nếu đoạn mang cấp con của cùng danh sách, trình đọc ghép nó vào khoản đang mở. Đầu ra chép nguyên nội dung ghép có thể đạt phép so với phạm vi cấu trúc dù đã nhập chữ thuộc Điều khác. Cùng cơ chế có thể che dấu điểm đầu một dòng mất số hoặc che số gõ tay trong một đoạn tự đánh số. Hạng P1 vì ranh giới DOCX đã sai ngay trong dữ liệu làm chuẩn so nguyên văn. [Bộ lọc và phép chiếu](../scripts/tl_core/llm_route.py#L540) · [Chốt tiền tố](../scripts/tl_core/llm_route.py#L1109) · [Nhập cấp con](../scripts/tl_core/llm_route.py#L1154)

**Đề xuất.** Giữ thiết kế từ chối. Định nghĩa tập ký tự mặc định bỏ qua khi hiển thị theo Unicode và áp ngay ở mọi đầu vào phân đoạn, gồm các ký tự thuộc nhóm chữ cái. Tiêu chí đóng lớp là cùng một ca âm cho DOCX và nguồn thô có ký tự trống trước tiền tố/dấu điểm, kèm đối chứng tiếng Việt NFC và dấu câu thông thường.

### S2 [P2] Tách dòng và gộp khoảng trắng chạy trước chốt cấm ký tự điều khiển — `scripts/tl_core/llm_route.py:1206`

**Kịch bản và căn cứ.** `splitlines()` tiêu thụ ký tự điều khiển như U+0085 (NEL) trước khi `_ky_tu_la` kiểm từng dòng. Với nguồn mất số có hai mảnh đủ hai vế và dấu kết, bộ đọc có thể biến ký tự cấm thành ranh giới giữa hai khoản và nhận cả hai. `strip()` cũng có thể xóa ký tự cấm ở biên trước khi kiểm; `lstrip("\ufeff")` bỏ mọi BOM liên tiếp, kể cả BOM dư sau khi CLI đã giải mã `utf-8-sig`. Trong DOCX, `_gon_doan` dùng `split()` trên chữ `w:t` trước chốt; U+0085 hợp lệ trong XML 1.0 bị biến thành khoảng trắng hoặc mất hẳn. Tiêu đề chỉ được kiểm sau khi gộp, nên danh sách hình dạng nguyên đoạn không chứng minh chữ gốc sạch. Ngoài ra `lvlText` của cấp con chấp nhận `\s`, và phần khoảng trắng bên trong nhãn được dựng có thể vào văn bản đưa đi so. P2 vì vi phạm §2.18 và có thể nhận sai ranh giới trên tuyến thô vốn đã khai chỉ suy từ dòng. Tác động xác định được trên tuyến DOCX là chấp nhận ký tự đáng lẽ phải từ chối. [Gộp chữ](../scripts/tl_core/llm_route.py#L619) · [Trả đoạn](../scripts/tl_core/llm_route.py#L1011) · [Tiêu đề và thân](../scripts/tl_core/llm_route.py#L1090) · [Nhãn](../scripts/tl_core/llm_route.py#L867) · [Giải mã tệp thô](../scripts/tl_core/ops_misc.py#L3057)

**Đề xuất.** Kiểm chữ nguồn trước mọi thao tác làm mất dấu vết. Chốt cú pháp chỉ bỏ một BOM ở đúng lớp giải mã và xác định tường minh ngắt dòng vật lý, tab cấu trúc `w:tab`/`w:ptab` và khoảng trắng hợp lệ trong nhãn. Tiêu chí đóng lớp gồm ca âm ký tự điều khiển giữa dòng và ở biên, DOCX có ký tự điều khiển trong chữ hiệu lực, cùng đối chứng CRLF và tab Word chuẩn.

### S3 [P2] Mốc quyền chỉnh sửa nội dòng bị từ chối dù §2.5 cho phép — `scripts/tl_core/llm_route.py:581`

**Kịch bản và căn cứ.** Word có thể dùng cặp `w:permStart`/`w:permEnd` trong một đoạn khi đánh dấu phần được sửa trong tài liệu Restrict Editing, phù hợp với mẫu văn bản được bảo vệ chỉ cho sửa một số vùng. Cặp mốc không mang chữ hiển thị. Mã chỉ có chúng trong `_KHOI_BO_QUA` ở cấp khối, thiếu trong `_CON_DOAN_BO_QUA`. `duyet` đánh dấu đoạn lạ và CLI trả rc 2 cho cả Điều. P2 vì từ chối an toàn một cấu trúc Word được tuyên bố hỗ trợ, độc lập với tần suất xuất hiện trong corpus. [§2.5](../ops/specs/llm-khoan-docx-r16.md#L75) · [Duyệt nội dòng](../scripts/tl_core/llm_route.py#L967) · [Chốt đoạn lạ](../scripts/tl_core/llm_route.py#L1111)

**Đề xuất.** Nhận đúng QName của hai mốc metadata ở cấp đoạn, giữ chốt cho phần tử có nội dung chưa hiểu. Tiêu chí đóng lớp là ca dương có cặp mốc giữa hai run, giữ đủ chữ và số, cùng ca âm QName khác namespace.

| Lớp | Biểu hiện đang mở | Lịch sử và phép kiểm đóng lớp |
| --- | --- | --- |
| `ranh-gioi-khoan` | S1 P1, S2 P2 | Kế thừa R1/R3 tại `b5cff4212a6abf052c74c772a525f54950b32b5e`, nối Q1/N1. Kiểm ký tự ở biên trước thao tác bỏ/gộp; đối chứng riêng DOCX, TXT, nguồn có/mất số, cùng tên thuật ngữ và dẫn chiếu giữa đoạn. |
| `docx-chu-hien-thi` | S3 P2 | R2 tại cùng SHA đã đóng ở ca ngoặc kín. S3 nối C5/F6 vì xuất phát từ xử lý metadata nội dòng, cần kiểm vị trí và QName trong bộ duyệt XML. |

Hai lớp còn mở, ba biểu hiện **0 P0, 1 P1, 2 P2, 0 P3**. Chuyển tiếp 15→16 đóng hoàn toàn **0/2 lớp**. [Protocol §8.3](../docs/PROTOCOL_DA_PHIEN.md#L812) · [ADR-0060 M1–M2](../docs/adr/0060-dieu-kien-merge-va-moc-ready.md#L32)

## Kết quả test và đột biến

Log và mã thoát tại `/tmp/wp1525-review16.xwWd8LQd/`. Mọi phép đo dùng head ở đầu báo cáo, trừ các dòng đối chứng base có tree `0cc14e79cecd2ce44bc4dc6cff92cadb31fd7ee4`. Clone head và clone base dựng từ bản sao Git cục bộ.

| Lệnh | Trạng thái | Mã thoát và bằng chứng dương |
| --- | --- | --- |
| `python scripts/tl_core/llm_route_test.py` | `passed` | rc 0, **63/63** ca, **200/200** đột biến bị giết, gồm **103/103** có tiền tố `wp1525_`. `llm.stdout`. |
| `python scripts/tl.py --deterministic workflow-audit --strict --json` | `passed` | rc 0, `ok=true`, 26 card, 60 task, 194 lệnh hiện diện, 0 lỗi, 0 cảnh báo. `workflow.stdout`. |
| `python scripts/tl.py --deterministic golden-test --json` · checkout và clone sạch head | `passed` | rc 0 cả hai lần, `ok=true`, **20/20** ca đạt, **20/20** bản chiếu ổn định, **19/20** raw ổn định. `hygiene_sweep_fixture` chỉ dao động ở `snapshot_age_s` đã khai, `raw_drift_undeclared=[]`. `golden.stdout`, `golden_clean.stdout`. |
| `python scripts/tl.py release-verify RELEASE_MANIFEST.json --strict --json` · checkout giao review | `failed` | rc 2, 187/187 mục trong manifest khớp; tệp verdict tạm là mục thừa duy nhất. `release.stdout`. |
| Cùng `release-verify` · clone sạch exact head | `passed` | rc 0, `ok=true`, **187/187** tệp, 0 lệch/thiếu/thừa. Package hash mong đợi và đo được cùng `ede9d96a1a319a5d92ac81fb7d299972fa16511fc1fac776b00fd13916d0caca`. `release_clean.stdout`. |
| `python ops/lease_publish.py check --root . ops/leases/llm-khoan-docx-r16-g1-claude.yaml` | `passed` cục bộ | rc 0, “ĐĂNG ĐƯỢC”, issue #1525, mốc base, hết hạn 10:15 UTC. `lease.stdout`. |
| `python scripts/tl.py --selftest` · head | `failed` | rc 1, **1774/1790**, transport **12/12**. `r1525_llm_khai_niem_tep_docx_cau_truc` đạt, kiểm CLI rc 0/5/2 với model giả lập. `selftest.stdout`. |
| `python scripts/tl.py --selftest` · base | `failed` | rc 1, **1773/1789**, transport **12/12**. `selftest_base.stdout`. |
| `python scripts/tl.py --deterministic determinism-audit --strict --json` | `passed` | rc 0, `ok=true`, **15/15** phép kiểm đạt. `determinism.stdout`. |
| `python scripts/tl.py --deterministic doc-claims-check --strict --json` · head sạch và base | `failed` trên cả hai | rc 2 mỗi cây, cùng hard flag L2 `SHA_NOT_A_COMMIT` tại protocol:1680. Object `9941d8af52aeede1c78ea4e232fbe9a8d5272033` vắng trong checkout shallow. `claims_clean.stdout`, `claims_base.stdout`. |
| `python -B -c` nạp `.claude/dev/ci_dang_ky_test.py` bằng `runpy.run_path` và gọi `loi_ruff_ci()` | `passed` | rc 0, `RUFF_CONTRACT 3 []`, phạm vi pin/probe của định nghĩa CI. |
| `python -m ruff check --no-cache --select F scripts/tl.py` · head và base, Ruff 0.15.15 | `failed` ở cả hai, đạt tiêu chí delta 0 | rc 1 mỗi cây, **12 F821**, **0 F401** mỗi cây, log trùng byte. `ruff_head.stdout`, `ruff_base.stdout`. |
| `git diff --check 8fb9c29 HEAD` và `git diff --check fcb12b3 HEAD -- . ':(exclude)ops/acceptance/llm-ranh-gioi-khoan/'` | `passed` | rc 0 ở cả hai phạm vi. |
| `git diff --check 64b7f2c HEAD` và `git diff --check 64b7f2c fcb12b3` | `failed` trên cả hai | rc 2 mỗi lệnh. Cùng ba dòng có khoảng trắng cuối dòng ở hồ sơ #1514 lượt 8, hai log đối chứng trùng byte. [Hồ sơ](../ops/acceptance/llm-ranh-gioi-khoan/r1/review-8-codex/VERDICT.md#L3) |

Harness hiện có viết từng đột biến `DOT_BIEN` vào thư mục tạm, nạp lại module và chỉ tính giết khi ca đích ném đúng `TinHieuChotCa`. Các đột biến r16 trong bảng đối chiếu đều nằm trong lần chạy này. Không có fixture, chuỗi thử nghiệm hay phép đột biến tự soạn. [Harness](../scripts/tl_core/llm_route_test.py#L1979)

`diff -u` danh sách ID đỏ trả rc 0. Đối chiếu thứ tự và trạng thái toàn bộ ID chung, sau khi loại ca DOCX mới, cũng trả rc 0. Cả hai lượt đều đỏ đúng 16 ID. Có 8 ca `r973_bootstrap_*`, 5 ca `wp433_*` và `wp727_tl_gws_refresh` khớp ghi chú môi trường `/tmp/.git` rỗng. Hai ca `r226_nguong_l2_troi_theo_abbrev_va_ci_ghim` và `r268_l2_trichotomy_theo_trang_thai_object` cũng đỏ trên cả hai SHA. Điều kiện selftest N/N và doc-claims strict vẫn chưa đạt. SHA-256 stdout selftest head `690f29e766c090f9a4eebcec1ace131550e3bf7e9b5be25e20ae14d1a7c9197a`, base `08c96775b4d8e21d6d356d27fe288b8f363476955bff3eb7e33577d58217fa30`.

Các cổng tạo `references/golden/fixtures/` và `scripts/.tl_state/` ở nhóm ignored. Hai thư mục này đã được chuyển ra scratch sau khi đo. HEAD, tree, diff tracked và index ở hai mốc khớp; snapshot cuối có `.codex/` trong nhóm ignored và tệp verdict trong nhóm untracked. Phép đo giới hạn ở chênh lệch quan sát được tại hai mốc. [Protocol §8.2](../docs/PROTOCOL_DA_PHIEN.md#L797)

## Không đo được

- S1–S3 dựa trên đọc mã. Bộ ca có sẵn chưa đo các trường hợp nêu trong findings. Chưa đo cách Word/Google Docs hiển thị Hangul Filler, tần suất mốc quyền nội dòng, hoặc tỷ lệ chặn oan của các wrapper ngoài tập cho phép trong corpus. Ảnh hưởng của `docDefaults/pPrDefault/numPr`, chữ ẩn và content control có data binding cũng chưa có bằng chứng từ ca được giao.
- `skipped` trong lệnh lease `check` đối với xác minh Issue/PR và dò comment. `not_run` đối với xác minh GitHub, CI/connector, Windows bản địa và model thật. Windows thuộc `required` theo ADR-0060 M3 khi xét diff toàn PR vì mã Python thêm dòng có `encoding=`. [ADR-0060 M3](../docs/adr/0060-dieu-kien-merge-va-moc-ready.md#L43) · [Dòng kích hoạt](../scripts/tl_selftest.py#L32275)
- Model và effort phục vụ `KHONG_DO_DUOC` theo metadata hiện có của run. Mã thoát tiến trình con, hash stdout cuối và biên nhận hoàn tất thuộc launcher sau phiên; kho nguồn Executor ngoài phạm vi quan sát. [Protocol §8.1](../docs/PROTOCOL_DA_PHIEN.md#L770)

**Lượt 16/16 đã chạm Review Rescue Checkpoint.** Điều kiện merge ADR-0060 M1 chưa đạt với **1 P1 và 2 P2** còn mở. [ADR-0060 M1](../docs/adr/0060-dieu-kien-merge-va-moc-ready.md#L32) · [Protocol §12](../docs/PROTOCOL_DA_PHIEN.md#L1097)

P2_mo: 2

VERDICT: REQUEST_CHANGES
