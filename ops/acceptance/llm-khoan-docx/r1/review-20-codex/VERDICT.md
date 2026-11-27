# Verdict packet #1525 r20 lượt 20 — Codex

reviewed_sha: 8a685fe0031d4d537cbefc6589087b4fc45d7334
reviewed_tree: cbab5413ae313292ce52de3570e58c6fa807b3a7
VERDICT: REQUEST_CHANGES

## Đối chiếu lượt 19 và đặc tả r20

- Checkout detached của `ducthangho/tra-luat`. Baseline nghiệm thu `64b7f2c14776d5d0e1d34a6be4725490956f5bec`, mốc kế thừa #1514 `fcb12b3873c3bec2c339029136243ed2c804ce05`, mốc trước vá `e1c3015e594c99abbe33e7453a5a947673cabd9f`. `git merge-base --is-ancestor 64b7f2c14776d5d0e1d34a6be4725490956f5bec HEAD` rc 0. Spec được đọc tại exact head, blob `88b1f2cd446ca48cc276f4c554f933605b2d182a`. SHA-256 của blob và tệp local cùng là `7c4fbfc77a17ee80318cf55b446761f3cbf3b5f719618b278f4f68bd1988ccc2`, khớp lease r20/g1 (blob `ea03d4a7289ceddd6e8a920e56342609904846a5`). [Spec r20](../ops/specs/llm-khoan-docx-r20.md) · [Lease r20](../ops/leases/llm-khoan-docx-r20-g1-claude.yaml)
- Đối chiếu cục bộ xác nhận **20/20** liên kết bia mộ hai chiều #1514 r9 ↔ #1525 r1 ↔ … ↔ r20 và **21/21** băm spec, cùng branch, base và generation. Write set 111 đường dẫn, SHA-256 `65544087f974c540499dcda02e0b8ef80a53dc5f8cfe393a3d2b4225acf9b873`. Diff bản vá r20 **8/8** và diff riêng packet **107/107** đường dẫn thuộc write set sau khi bỏ hồ sơ #1514 theo prompt. Diff toàn PR có **155** đường dẫn, gồm 48 đường dẫn kế thừa #1514 ngoài write set r20. Lease khai `sensitive`, lượt gọi **20/20**, có chỉ thị đứng của chủ kho ghi trong spec.
- Reviewer `openai_codex / codex_cli / machine`, run `066bfadcde88430184536eaae5f56131`, launcher 1.6.2, `codex-cli 0.172.0` theo `codex --version`. SHA-256 prompt snapshot `a87b91aa9309fa8ebd85e72625278e861317f568ad496b0ea3ee7ea717f112db` khớp metadata. Executor khai `claude / claude_code / machine/local` trong lease. Run bắt đầu lúc 09:47:21 UTC, trường `leased_at_utc` ghi 10:00 UTC cùng ngày. `lease_publish.py check` kiểm hạn cuối 18:00 UTC, còn thứ tự cấp thực tế chưa được kiểm từ remote. Môi trường Linux x86_64, Python 3.13.18, Git 2.43.0, `core.abbrev=7`, checkout shallow, sandbox `workspace-write` với Git metadata chỉ đọc. [Protocol §8.1–8.2](../docs/PROTOCOL_DA_PHIEN.md#L770)

Lượt 19 neo `7c4abd7870807ef4b4e5e685f0171a67fa487414`. Các trạng thái áp dụng điều khoản r20 hiện hành. [Verdict lượt 19](../ops/acceptance/llm-khoan-docx/r1/review-19-codex/VERDICT.md) · [Hồ sơ #1514 lượt 10](../ops/acceptance/llm-ranh-gioi-khoan/r1/review-10-codex/VERDICT.md)

| Mục | Trạng thái | Bằng chứng |
| --- | --- | --- |
| V1 · §2.22 · markup đường số hiệu | **VÁ MỘT PHẦN** | Cờ `--markup-strict` tới producer. Test giả lập rc 3 xác nhận `ValueError`, handler trả rc 2 trước model. Đường text/plain đã đóng. Tiêu chí của producer vẫn có thể coi một bản lọc thiếu là đủ, xem W1. [Gọi extract](../scripts/tl_core/llm_route.py#L1488) · [Ca và mutant](../scripts/tl_core/llm_route_test.py#L669) |
| V2 · §2.22 · đánh số từ mặc định đoạn | **ĐÃ VÁ THẬT** cho biểu hiện mặc định đoạn | Reader kiểm sự có mặt của `docDefaults/pPrDefault/pPr/numPr` trước khi phân tích đoạn, kể cả khi mọi đoạn có số trực tiếp. Ca chặn và ca dương mặc định chỉ có giãn dòng đều đạt. Hai mutant gỡ chốt và chặn quá rộng bị bắt. [Chốt](../scripts/tl_core/llm_route.py#L834) · [Dương](../scripts/tl_core/llm_route_test.py#L1430) · [Âm](../scripts/tl_core/llm_route_test.py#L1601) |
| V3 · §2.22 · cắt Điều theo regex của extract | **CHƯA VÁ** ở runtime, **giới hạn đã duyệt** | Chủ kho chọn giữ đường số hiệu, §2.22 V3 và hướng dẫn khai rõ dẫn chiếu đầu dòng có thể làm mất các khoản sau. Hiện tượng thuộc giới hạn này đã hết là finding mở theo r20. [Spec](../ops/specs/llm-khoan-docx-r20.md#L275) · [Hướng dẫn](../docs/GOI_AGENT_DA_NEN.md#L412) |
| V4 · §2.22 · nhãn điểm thô | **ĐÃ VÁ THẬT** với hai dạng chữ thường theo §2.22; lớp ranh giới còn mở | `a.` và `(a)` chữ thường đã bị chặn. Hai mutant gỡ từng dạng bị bắt, đối chứng chữ viết tắt đạt. W4 chỉ ra chênh lệch với hướng dẫn công khai và biểu hiện còn lại ở đường mất số. [Regex](../scripts/tl_core/llm_route.py#L494) · [Ca](../scripts/tl_core/llm_route_test.py#L685) |
| §1–§2.3 · K1 #1514, đường gọi và cờ duyệt | **ĐÃ VÁ THẬT** cho hai nhánh K1 | `_RE_DIEM` chặn nhánh điểm K1 của cả hai loại nguồn. Dòng tiếp mở bằng “là” ở nguồn có số rơi vào nhánh từ chối dòng không số. Ở nguồn mất số, phép so đòi thuật ngữ trước từ nối khác rỗng. `ca_wp1514` kiểm nguồn Điều 3 và ba đầu ra lưu sẵn **8/8**. Cờ CLI, các hàm gọi model và hai nhãn phạm vi/duyệt giữ hành vi. [Tách](../scripts/tl_core/llm_route.py#L1243) · [So](../scripts/tl_core/llm_route.py#L1383) · [CLI](../scripts/tl_core/ops_misc.py#L3120) |
| §2.1–§2.2, §2.4–§2.9 · A1, B1/B2, C1/C2, D1/D4, E1/E3/E4, F1/F2 | **HẾT ĐỐI TƯỢNG** với cắt cuối Điều, duyệt bảng, `KhongCauTruc` và hỗ trợ điểm gõ tay; **ĐÃ VÁ THẬT** với các chốt còn hiệu lực | Đoạn có nội dung đầu tiên phải khớp nguyên tiêu đề đích. Đọc qua hết tệp một Điều, chặn bảng/khối lạ, ngắt mềm, đoạn có số nhưng rỗng và đoạn không số sau khoản đầu. DOCX không có đánh số tự động ném `ValueError`; CLI trả rc 2. Điểm gõ tay dạng đoạn riêng bị chặn, số gõ tay đầu đoạn tự động có chốt riêng. [Vùng và các chốt](../scripts/tl_core/llm_route.py#L1114) · [Handler](../scripts/tl_core/ops_misc.py#L3037) |
| §2.4–§2.15 · A2/A5, B2/B5, C2, D2, E6, F3–F5, G1/G3, H4, J1/J3, K3, L4, M2 | **ĐÃ VÁ THẬT** đối với các biểu hiện lịch sử còn hiệu lực | ID chuẩn hóa theo chuỗi ASCII, ID trùng sau chuẩn hóa bị đánh lỗi. Số bắt đầu mặc định 0, `startOverride` theo cấp, bộ đếm theo `numId`, tăng cha xóa bộ đếm con, từ chối nhảy cấp và chặn trên 999. Định nghĩa lỗi bị chặn khi dùng. Chỉ một danh sách, số khoản thập phân đúng nhãn cấp và liên tục từ 1. Các biểu hiện mới ở định nghĩa cấp mâu thuẫn xem W5. [Định nghĩa](../scripts/tl_core/llm_route.py#L713) · [Bộ đếm](../scripts/tl_core/llm_route.py#L1086) · [Ranh giới khoản](../scripts/tl_core/llm_route.py#L1155) |
| §2.4–§2.9 · A3/A6, C3, D6, F2 | **ĐÃ VÁ THẬT** với câu dẫn, dấu phân cách và phạm vi từ nối | Tối đa một câu dẫn khớp nguyên đoạn trước khoản đầu. Chốt dấu phân cách chạy trên chữ mỗi đoạn. Tuyến cấu trúc chỉ tìm từ nối trên đoạn mở khoản, rồi đối chiếu toàn bộ định nghĩa theo vị trí, có kiểm hai vế và số mục. Việc sửa nguồn trước khi so vẫn có thể làm sai chuẩn đối chiếu, xem W2. [Câu dẫn](../scripts/tl_core/llm_route.py#L1204) · [So từng khoản](../scripts/tl_core/llm_route.py#L1383) |
| §2.4–§2.16 · A4, B3/B4/B6, C4/C5, D3/D5, E2–E5, F6, G2/G4, H2/H5, J2/J5, K1, L1/L5, M2, N3, S3 | **ĐÃ VÁ THẬT** với các biểu hiện được khóa; lớp markup còn mở | Part theo URI Transitional và các tệp quan hệ đúng nguồn. Cấu trúc đọc XML gốc, chặn `mc:`, sửa dấu đoạn, mốc move lẻ/thiếu ID và tổ hợp gạch từ nhiều tầng chưa giải được; lọc chữ gạch/xóa/chuyển đi. Ca có sẵn phủ content control, `w:ptab`, `w:noBreakHyphen`, mốc perm, bytes theo mã hóa XML và ngắt trang có chữ hiệu lực theo sau. Vẫn còn W1 ở producer thô và W2 ở xử lý khoảng trắng. [Đọc run](../scripts/tl_core/llm_route.py#L929) · [Kiểm toàn part](../scripts/tl_core/llm_route.py#L1064) |
| §2.10–§2.21 · G6, H1, K2, L2/L3, M1, N1/N2, Q1/Q2, R1–R3, S1/S2, T1/T2, U1/U2 | **ĐÃ VÁ THẬT** trong miền ký tự đã khai đối với các biểu hiện lịch sử; tổn thất U2 là giới hạn đã duyệt | Cấm tiền tố cấu trúc trên bản chiếu chữ/số đã kiểm ký tự. ASCII là miền chữ số duy nhất, nên dạng số mũ bị chặn ở cả hai tuyến. Chốt TXT đứng trước tách dòng, xử lý một BOM và strip ASCII. Dạng số gõ tay ngoặc kín bị chặn kể cả dính thân. Những lớp mất chữ ở W1/W2 xảy ra trong chuyển XML thành text, ngoài các biến đổi sanitizer khai tại U2. [Chốt ký tự và tiền tố](../scripts/tl_core/llm_route.py#L529) · [TXT CLI](../scripts/tl_core/ops_misc.py#L3057) |
| §3 · A7/A8, B7/B8, C6/C7, D4, E5, F5, G5, H3, J4, K4, L6, Q2 | **ĐÃ VÁ THẬT** với hành vi còn hiệu lực và ca có sẵn | Bảng đột biến có neo riêng cho dấu gạch điểm gõ tay, ID trừu tượng, quan hệ part/numbering đổi tên, đọc XML gốc, `startOverride`, reset con và các chốt mới r20. §3 và hướng dẫn phản ánh hợp đồng một Điều; các ca từng chấp nhận điểm gõ tay hết đối tượng. [Bảng mutant](../scripts/tl_core/llm_route_test.py#L1777) · [Hướng dẫn](../docs/GOI_AGENT_DA_NEN.md#L391) |

## Findings

### W1 [P1] Đường số hiệu có thể qua strict dù chữ gạch bỏ còn trong text — `extract_cache.py:223`, `docx_markup.py:74`

**Kịch bản và căn cứ.** Một bản export có sửa đổi trực tiếp được bộ quét nhận diện, đồng thời có chữ bị gạch qua style. Producer mở `word/document.xml`, lấy thống kê và chạy lọc regex. `_strike_on` chỉ xét thuộc tính trong chính run, nên gạch qua style không được đánh giá. `markup_found` chỉ cần một bộ đếm khác 0 và strict chỉ chặn khi có `markup_warning`. Bởi vậy dấu sửa đã nhận ở chỗ khác có thể cho phép cả bản qua dù chữ bị gạch trong một định nghĩa vẫn còn. Bộ đọc DOCX cục bộ có logic gạch theo style riêng, còn chuẩn so của đường số hiệu đến từ producer. P1 vì phép so có thể xác nhận và lưu chữ đã bỏ ngay cả khi ranh giới khoản đúng. Đây là phần còn lại của lớp V1, bên ngoài giới hạn sanitizer/cắt Điều U2/V3. [Producer](../scripts/tl_core/extract_cache.py#L213) · [Điều kiện strict](../scripts/tl_core/extract_cache.py#L291) · [Đọc DOCX ở producer](../scripts/tl_core/lookup_ops.py#L2398) · [Quét gạch](../scripts/docx_markup.py#L74)

**Đề xuất.** Yêu cầu tín hiệu hoàn tất xử lý markup hiệu lực trên chính snapshot trước khi nhận text. Tách tình trạng đã quét đủ, phát hiện sửa đổi và đã lọc thành công. Nếu chưa giải được cách lọc đó, trả trạng thái chưa xác minh hoặc yêu cầu nguồn DOCX cục bộ đã có cấu trúc phù hợp. Phép kiểm đóng lớp cần một tài liệu có cả sửa đổi trực tiếp và gạch qua style, cùng đối chứng cả hai được xử lý.

### W2 [P1] Bộ đọc DOCX bỏ dấu cách bị gạch rồi xác nhận chữ đã dính — `llm_route.py:967`

**Kịch bản và căn cứ.** Hai run hiệu lực cách nhau bằng một run gạch chỉ mang khoảng trắng. `run()` thu phần chữ và loại toàn bộ run gạch trước `kq["phan"].extend`. Cuối đoạn nối run bằng chuỗi rỗng rồi mới gộp khoảng trắng, nên hai từ dính lại. Lớp này đã có ca repo `r222_dau_cach_bi_gach_khong_dinh_chu`, và bộ lọc dùng chung giữ dấu cách chỉ mang định dạng để tránh sinh chữ mới. Tuyến cấu trúc đọc XML gốc và tự lọc nên ca r222 của bộ lọc dùng chung vẫn xanh. Cùng dạng mất phân cách ở tuyến số hiệu xảy ra khi bộ đọc chuyển XML sang text bỏ `w:tab` và `w:br` như tag rỗng, trước sanitizer U2. P1 vì chuẩn đối chiếu có thể đã mất phân cách giữa các từ từ trước khi gửi model, rồi kết quả trùng chuẩn ấy vẫn qua. [Nối run](../scripts/tl_core/llm_route.py#L987) · [Ca r222](../scripts/tl_selftest.py#L17915) · [Chính sách dấu cách của bộ lọc chung](../scripts/docx_markup.py#L209) · [Bóc XML ở producer](../scripts/docx_markup.py#L117)

**Đề xuất.** Áp dụng chính sách giữ phân cách của r222 trên cây XML tại cửa loại run/wrapper đã bỏ. Kiểm cả dấu cách đơn lẻ và run có chữ bị loại thật. Ở tuyến số hiệu, chuyển các phần tử phân cách được hỗ trợ thành phân cách tương ứng hoặc từ chối trước khi text mất cấu trúc.

### W3 [P2] Strict chặn cả bản export sạch và đường cache-build được hướng dẫn — `extract_cache.py:180`, `extract_cache.py:223`

**Kịch bản và căn cứ.** Export DOCX đọc thành công từ nguồn đã ban hành có thể trả thống kê mọi số đếm bằng 0. `cmd_extract` vẫn tạo `markup_warning` chỉ vì không thấy dấu sửa, rồi trả rc 3 khi strict. Khi có record consolidated, producer ưu tiên nó trước DOCX và luôn gắn cảnh báo vì không biết chế độ markup đã dùng. Lỗi CAP và tài liệu vẫn khuyên dựng `tl cache-build` rồi thử lại chính đường số hiệu, nên ở r20 đường được gợi ý cũng bị strict chặn. P2 vì người dùng mất đường đọc dù export DOCX khả dụng, và hướng dẫn khôi phục không vượt được chốt. V1 khai cái giá text/plain; hai trường hợp trên có nhánh producer khác. Chưa đo tỷ lệ tài liệu thật gặp trường hợp này. [Chọn cache](../scripts/tl_core/extract_cache.py#L176) · [Không thấy dấu sửa](../scripts/tl_core/extract_cache.py#L223) · [Lời khuyên CAP](../scripts/tl_core/llm_route.py#L1508) · [Hướng dẫn](../docs/GOI_AGENT_DA_NEN.md#L386)

**Đề xuất.** Dùng chứng cứ ở W1 để nhận snapshot đã kiểm đầy đủ và sạch, giữ chốt với snapshot chưa rõ. Nếu consolidated chưa thể chứng nhận, cập nhật chẩn đoán/hướng dẫn của lệnh để chỉ đường còn dùng được. Kiểm đối chứng bản DOCX sạch, bản có dấu đã lọc và bản cache chưa chứng nhận.

### W4 [P2] Tuyến thô mất số vẫn nhận điểm mang nhãn chữ hoa hoặc lặp chữ — `llm_route.py:494`, `llm_route.py:1252`

**Kịch bản và căn cứ.** Một điểm trong bản mất số khoản vẫn có thể mang nhãn chữ hoa kết thúc bằng dấu chấm, hoặc nhãn lặp chữ của danh sách chữ vượt 26. Bộ đọc cấu trúc thực tế hỗ trợ `upperLetter` và nhãn lặp chữ. Dạng chấm không gây ngoặc lẻ, không khớp `_RE_DIEM` chữ thường đơn và không phải đánh số nội dòng. Khi bản thô mất toàn bộ số khoản và dòng điểm có hình dạng một định nghĩa kết câu, dòng đó vào `khoan` như một mục độc lập. §2.22 V4 mô tả đúng miền chữ thường. Hướng dẫn r20 nói rộng hơn rằng một chữ cái và dấu chấm đầu dòng bị chặn, trong khi nhãn hoa đi qua. P2 theo K1/V4 vì lớp ranh giới còn biểu hiện cùng cơ chế và đầu ra thô mang nghĩa so theo phân đoạn của bộ quét, kèm cờ cần duyệt ranh giới. [Dạng nhãn cấu trúc](../scripts/tl_core/llm_route.py#L868) · [Tách thô](../scripts/tl_core/llm_route.py#L1252) · [Hướng dẫn](../docs/GOI_AGENT_DA_NEN.md#L414)

**Đề xuất.** Xác định miền nhãn điểm trên nguồn thô nhất quán với các dạng danh sách hỗ trợ, kiểm cả chữ hoa, lặp chữ, dấu và vị trí. Nếu ưu tiên giữ chữ viết tắt và khó tách nhãn, chuyển nhóm mơ hồ sang tuyến có cấu trúc. Nguồn mất cả nhãn lẫn số có giới hạn phân biệt theo hình dạng dòng đã phản ánh trong `pham_vi_kiem`.

### W5 [P1] Hai định nghĩa cùng cấp có thể được âm thầm quy về định nghĩa cuối — `llm_route.py:736`, `llm_route.py:779`

**Kịch bản và căn cứ.** Reader đã chặn trùng `numId` và `abstractNumId` sau chuẩn hóa. Bên trong một danh sách, hai `w:lvl` có cùng `ilvl` sau chuyển sang số cùng ghi vào `muc[il]`. Hai `lvlOverride` chỉ chứa `startOverride` cho cùng cấp cũng thay nhau ghi giá trị bắt đầu, không đặt cờ lỗi. Bộ đếm, phép dựng nhãn và phép so chỉ thấy giá trị cuối. Một cấp con có hai giá trị bắt đầu khác nhau vẫn có thể cho một chuẩn có nhãn và được xác nhận theo chuẩn đó. P1 vì một định nghĩa mâu thuẫn được nhận ở tuyến tuyên bố ranh giới từ cấu trúc, trong khi §2.2 yêu cầu rc 2 khi cấu trúc mơ hồ. Kết luận ở đây dựa vào hành vi ghi đè trong reader; chưa đo ứng dụng Word xử lý tài liệu mâu thuẫn ra sao. [Đọc cấp](../scripts/tl_core/llm_route.py#L736) · [Đọc override](../scripts/tl_core/llm_route.py#L779) · [Đếm](../scripts/tl_core/llm_route.py#L1097)

**Đề xuất.** Đánh dấu định nghĩa có cấp trùng sau chuẩn hóa hoặc có override trùng cấp là chưa hỗ trợ, theo cùng quy tắc chặn khi dùng danh sách của §2.4 A5. Khóa đối chứng hai cấp khác nhau hợp lệ và danh sách lỗi không được Điều dùng.

| Lớp | Cao nhất còn mở | Lịch sử và phép kiểm đóng |
| --- | --- | --- |
| `docx-markup-du-thao` | P1 · W1, W3 | A4/B3/D3/G2/H2/L1 → V1. Chốt trạng thái producer phải bao phủ chữ kế thừa, phân biệt đủ chứng cứ với có dấu sửa và giữ đường nguồn sạch có chứng cứ. |
| `docx-khoang-trang-sau-loc` | P1 · W2 | Lớp chuẩn hóa phân cách có tiền lệ r222: mất khoảng trắng trong chuẩn trước so. Đóng với đối chứng chữ gạch bị bỏ, dấu cách chỉ mang định dạng được giữ, phân cách XML còn nghĩa sau khi đưa ra text. |
| `ranh-gioi-khoan` | P2 · W4 | Nối K1/V4, giữ lịch sử F1, N1 → Q1 → R1/R3 → S1/S2 → T1/T2 → U1/U2. V3 đã chuyển thành giới hạn theo quyết định chủ kho; phép đóng còn lại cần phân loại nhãn điểm ở đường thô. |
| `docx-so-hien-thi` | P1 · W5 | A2/B2/G1/J1 → V2. Mặc định đoạn đã fail-closed; cấp trùng trong danh sách dùng vẫn cần fail-closed trước đếm và dựng nhãn. |

Còn **4 lớp, 5 finding** (0 P0, 3 P1, 2 P2, 0 P3). Chuyển tiếp 19→20 đóng các biểu hiện riêng V2 và hai dạng nhãn trong V4, còn **0/3 lớp** cũ đóng hoàn toàn. W2 là lớp mới trong bảng của lượt này. Điều kiện merge của ADR-0060 M1 chưa đạt. [Protocol §8.3](../docs/PROTOCOL_DA_PHIEN.md#L812) · [ADR-0060 M1–M2](../docs/adr/0060-dieu-kien-merge-va-moc-ready.md#L32)

## Kết quả test và đột biến

Log và mã thoát nằm ngoài checkout tại `/tmp/wp1525-r20-review.KW88R5/`. Python chạy với `PYTHONDONTWRITEBYTECODE=1` và cache ngoài checkout. Các bản sao local detached dùng cùng cấu hình `core.abbrev=7` và giữ nguyên nội dung exact SHA. Bản base đối chứng neo `64b7f2c14776d5d0e1d34a6be4725490956f5bec`, tree `0cc14e79cecd2ce44bc4dc6cff92cadb31fd7ee4`.

| Lệnh | Trạng thái | Mã thoát và bằng chứng |
| --- | --- | --- |
| `python scripts/tl_core/llm_route_test.py` | `passed` | rc 0, **63/63** ca, **211/211** mutant bị bắt, gồm **114/114** mutant `wp1525_*`. `route.log`, SHA-256 `1cd57d21389f380cc888dcf781e0a74e47aabd9d9ffc841db95fbe0e6b43296f`. |
| `python scripts/tl.py --deterministic workflow-audit --strict --json` | `passed` | rc 0, `ok=true`, 26 card, 60 task, 194 lệnh, 0 lỗi, 0 cảnh báo. `workflow.log`. |
| `python scripts/tl.py --deterministic golden-test --json` | `passed` | rc 0, `ok=true`, **20/20** ca, **20/20** bản chiếu ổn định. Byte thô **19/20** ổn định. `hygiene_sweep_fixture` chỉ lệch khóa biến động đã khai `snapshot_age_s`, bản chiếu có `diff={}`. `golden.log`. |
| `python scripts/tl.py release-verify RELEASE_MANIFEST.json --strict --json` | `passed` | rc 0, `ok=true`, **187/187** tệp, danh sách lỗi/thiếu/thừa rỗng. Hash gói khớp `976150b336fb54124c6292181f9a7195f1802352b32260f008c07cbcae0a467f`. Chạy trên bản sao head sạch để tệp verdict ghi sớm nằm ngoài kiểm kê. `release.log`. |
| `python ops/lease_publish.py check --root . ops/leases/llm-khoan-docx-r20-g1-claude.yaml` | `passed` cục bộ | rc 0, “ĐĂNG ĐƯỢC”, Issue #1525, neo `64b7f2c14776`, hạn 18:00 UTC. Hai lớp kiểm GitHub `skipped` theo thông báo của lệnh. `lease.log`. |
| `python scripts/tl.py --selftest` · head, lần chạy lại | `failed` | rc 1, **1774/1790**, transport **12/12**. Ca CLI `r1525_llm_khai_niem_tep_docx_cau_truc` đạt. `selftest-retry.log`, SHA-256 `57fcdeb75ee23735aeafeff2aa3cfb9941b702c35e0b27be2e26cda84fd2eabc`. |
| `python scripts/tl.py --selftest` · base, lần chạy lại | `failed` | rc 1, **1773/1789**, transport **12/12**. `selftest-base-retry.log`, SHA-256 `0d7158ac58638eedd511197fcfc5e6c269ddc42596fc6a0904b0f0838ab88fad`. |
| `git diff --check e1c3015 HEAD` và `git diff --check fcb12b3 HEAD -- . ':(exclude)ops/acceptance/llm-ranh-gioi-khoan/'` | `passed` | rc 0 cho cả hai phạm vi. |
| `git diff --check 64b7f2c HEAD` và `git diff --check 64b7f2c fcb12b3` | `failed` | Cả hai rc 2, cùng ba khoảng trắng cuối dòng ở verdict #1514 lượt 8, dòng 3–5. |

Harness ghi từng mutant vào thư mục tạm ngoài checkout, yêu cầu đúng một neo và chỉ tính bị bắt nếu ca đích ném `TinHieuChotCa`. Trong lượt này, harness xác nhận cả năm mutant mới. [Bảng mutant r20](../scripts/tl_core/llm_route_test.py#L1793) · [Harness](../scripts/tl_core/llm_route_test.py#L2059)

| Mutant | Ca đích |
| --- | --- |
| `wp1525_extract_bo_markup_strict` | `ca_khoan_mat_so_co_diem_dat` đòi cờ strict trong argv giả lập. |
| `wp1525_bo_chan_numpr_mac_dinh` | `ca_cau_truc_docx_chan` đòi chặn mặc định đoạn mang `numPr`. |
| `wp1525_numpr_mac_dinh_qua_rong` | `ca_cau_truc_docx_dat` đòi mặc định không có số vẫn đọc được. |
| `wp1525_diem_bo_dang_cham`, `wp1525_diem_bo_ngoac_mo` | `ca_khoan_mat_so_co_diem_dat` đòi chặn riêng dạng chấm và dạng ngoặc mở. |
| `wp1525_tho_nhan_diem` | `ca_wp1514_luot9` đòi chặn điểm trên nguồn có số và mất số. |

Lượt selftest đầu chạy đồng thời với thư mục tạm mặc định. Head dừng rc 1 trước khi in tổng vì hai lượt dùng chung tên tệp tạm ở ca `r38`. Cơ chế phù hợp với việc tệp cấu hình thử bị lượt kia dọn, sau đó luồng ghi rơi xuống cấu hình home chỉ đọc. Tôi chạy lại hai exact SHA với hai `TMPDIR` riêng dưới scratch và giữ mạng selftest ở chế độ tắt. Lượt base đầu đã chạy hết và trả rc 1, **1773/1789**, transport **12/12**. Log lần đầu là `selftest.log` và `selftest-base.log`.

Hai lượt chạy lại có **1.801** dòng kết quả chung, gồm cả transport. Sau khi bỏ đúng dòng `[OK]` của ca mới `r1525_llm_khai_niem_tep_docx_cau_truc`, `cmp` trả rc 0. Head và base có cùng **16** ca đỏ. Nhóm 14 mà prompt nêu gồm 8 `r973_bootstrap_*`, 5 `wp433_*` và `wp727_tl_gws_refresh`, với `/tmp/.git` rỗng. Hai ca còn lại là `r226_nguong_l2_troi_theo_abbrev_va_ci_ghim` và `r268_l2_trichotomy_theo_trang_thai_object`. Các ca `r222_dau_cach_bi_gach_khong_dinh_chu`, `r186_extract_canh_bao_va_markup_strict` và `r380_llm_khai_niem_bien_dau_vao` đạt ở cả hai cây. Delta ca đỏ bằng 0. Gate N/N vẫn `failed` trong môi trường này.

## Không đo được

- W1–W5 là kết luận đọc mã, với W2 có thêm đối chứng r222 trên bộ lọc dùng chung. Phép đo đầu-cuối của từng finding, cách Word chọn cấp ghi trùng, việc làm mới content control liên kết dữ liệu và cách hiển thị chữ ẩn cần thêm fixture hoặc ứng dụng thực tế. Suite hiện có chỉ đo các ca đã giao.
- Về danh sách phần tử §2.5, ca sẵn có xác nhận bookmark/comment/perm và các wrapper hoặc run được hỗ trợ trong đặc tả, gồm content control nội dòng, `w:ptab` và ngắt trang cuối đoạn. Các dạng trường, hình, ký hiệu, chú thích, bảng, Strict và `mc:` thuộc giới hạn đã khai. Từ nguồn có sẵn chưa xác lập thêm phần tử phổ biến của Word/Google Docs bị chặn oan ở đường DOCX local. W3 là chặn oan tại strict của đường số hiệu. Tần suất trong export thật chưa đo.
- `skipped` với hai lớp kiểm GitHub của lệnh lease. `not_run` với GitHub, CI từ xa, gọi model thật, Windows bản địa, determinism-audit, doc-claims-check, Ruff pin/probe và bare lint. Windows là `required` theo ADR-0060 M3 vì diff PR sửa dòng Python chứa `encoding=`. [ADR-0060 M3](../docs/adr/0060-dieu-kien-merge-va-moc-ready.md#L43) · [Dòng đổi encoding](../scripts/tl_core/ops_misc.py#L3061)
- Model và effort phục vụ là `KHONG_DO_DUOC` trong metadata của run còn mở. Launcher chịu trách nhiệm ghi trạng thái terminal, rc con và hash đầu ra sau khi lượt kết thúc. Kho nguồn Executor nằm ngoài phạm vi quan sát.

## Đọc lại checkout và kết luận

`git rev-parse HEAD 'HEAD^{tree}'` khớp ở đầu và cuối phiên. `git diff --quiet` và `git diff --cached --quiet` trả rc 0 trên checkout được giao và các bản sao đo. Checkout được giao có `.codex/` ignored từ đầu và `.review/VERDICT.md` của lượt này. Fixture và state do gate sinh nằm trong các bản sao dưới scratch. Snapshot chứng minh trạng thái ở hai lần quan sát. [Protocol §8.2](../docs/PROTOCOL_DA_PHIEN.md#L797)

Lượt 20 chạm trần lease 20/20. Ba P1 và hai P2 còn mở, nên verdict nội dung là `REQUEST_CHANGES`. Gate selftest N/N và bằng chứng bắt buộc ngoài phạm vi đo cũng chưa đủ cho merge.

P2_mo: 2

VERDICT: REQUEST_CHANGES
