# Verdict packet #1525 r32 lượt 32 — Codex

reviewed_sha: 571e83f62ee4833f73392bd13d2353524b31e732
reviewed_tree: d0f1c777cd65d0c8dcab8e43fa005fe89d7f02e2
base_sha: 64b7f2c14776d5d0e1d34a6be4725490956f5bec
base_tree: 0cc14e79cecd2ce44bc4dc6cff92cadb31fd7ee4

## Preflight

- Checkout độc lập, detached, origin `ducthangho/tra-luat`. Ref local và remote-tracking của nhánh `ccr-89c0d2e2-inanqb` đều trỏ exact head. `git merge-base` cho đúng base SHA. Mốc bản vá `f5ce6a201b5d33e6fd511d141cf5f9acb4c7d060`, mốc kết thúc #1514 `fcb12b3873c3bec2c339029136243ed2c804ce05`. Git SHA-256 của luồng diff nhị phân lần lượt là `a1d07f9c88590299ccd9b9a06fd1f104b7fa29f0ff8536f73c0df72b3d6e9c94`, `10f401f917403dc31e225f3bc3d9abe31c3b282b0e94cb5463da6a9b149fbc02`, và `c9f68c78621e04d0f67c911f3feb4c8a3029ac3f6a3fec1eadcee122d405b0c7` cho bản vá, packet và toàn PR.
- Reviewer `openai_codex / codex_cli / machine`, qua launcher, run `2688dc5bcb874a7580e34c43cf7cb5df`. Sandbox `workspace-write` với mạng bị giới hạn theo quyền phiên. Prompt SHA-256 `5615bd3334d2d85194200005d853af7abb464d5c98a74c2a489dec9839c75988` khớp tệp, checkpoint và run. Executor `anthropic_claude / claude_code / machine/local` theo lease (`provider: claude`), Review Class khai báo và hiệu lực đều `sensitive`. [Run](../../run/2688dc5b/run.json) · [Checkpoint](../../run/2688dc5b/checkpoint.json) · [Bảng provider](../ops/KE_HOACH_THI_CONG_DA_PROVIDER.md#L26)
- Lease #1525 r32/g1 còn hạn tới 21:48 UTC ngày 26-11-2026 tại lúc kiểm. Lượt **32/32**, inference budget 0. SHA-256 đặc tả `ded29ad80dd22355f6504aca425987ab6d72503db4bc6822a838ad781eeb111e` khớp byte tệp, Git blob và lease. Quyền đứng, hợp đồng một Điều và ngoại lệ M5 có trong đặc tả. [Lease r32](../ops/leases/llm-khoan-docx-r32-g1-claude.yaml) · [Đặc tả r32](../ops/specs/llm-khoan-docx-r32.md)
- Write set 171 đường dẫn, SHA-256 tính lại `e8a39a78ccf9da2b8e8e1a357e37fd2137edcdb3b3e0cc0fb6d9819dcf420e16`. Bản vá có 7/7 đường dẫn hợp lệ. Diff packet có 167/167 đường dẫn hợp lệ sau khi trừ bốn hồ sơ #1514 theo prompt. Trong 215 đường dẫn của toàn PR, 48 ngoài lease hiện hành đều thuộc hồ sơ, spec và lease của #1514. Cặp bia mộ **32/32** khớp hai chiều và **33/33** hash spec khớp trên đĩa và trong Git, từ #1514 r9 đến #1525 r32. [Bia mộ #1514 r9](../ops/leases/llm-ranh-gioi-khoan-r9-g1-claude.yaml#L97) · [Bia mộ r31](../ops/leases/llm-khoan-docx-r31-g1-claude.yaml#L208)

## Đối chiếu lượt 31 và đặc tả r32

| Mục | Trạng thái | Bằng chứng |
| --- | --- | --- |
| H1 lượt 31 · §2.34 | **ĐÃ VÁ THẬT** đối với lỗi chọn style đoạn mặc định theo loại thô | Cả chọn mặc định lẫn bảng loại dùng cùng quy tắc vắng `w:type` là `paragraph`. Mặc định được tra khi vắng `pStyle`, giữ chẩn đoán cho tham chiếu sai loại và kế thừa khác loại. Đột biến trả lại điều kiện cũ khiến đúng chữ đã gạch xuất hiện. [Chọn style mặc định](../scripts/tl_core/llm_route.py#L925) · [Ca H1](../scripts/tl_core/llm_route_test.py#L1531) |
| H2 lượt 31 · §2.28–§2.34 | **ĐÃ VÁ THẬT** đối với đệm trước dấu ở các biểu hiện gốc. **VÁ MỘT PHẦN** lớp | Nhánh số–dấu–chữ nhận đệm ngang trước dấu và giữ ngoại lệ đệm sau dấu. Đột biến khôi phục mẫu cũ làm ca H2 đỏ. Miền dựng và miền nhận diện vẫn lệch khi nhiều placeholder chữ đứng liền, xem I2. [Ngữ pháp](../scripts/tl_core/llm_route.py#L526) · [Ca H2](../scripts/tl_core/llm_route_test.py#L717) |
| H3 lượt 31 · §2.34 | **ĐÃ VÁ THẬT** đối với khai báo ID. **VÁ MỘT PHẦN** lớp | ID rỗng, vắng hoặc mở bằng `#` bị từ chối khi nạp định nghĩa. Bỏ chốt làm lỗi `TypeError` có sẵn tái hiện. Lối nhận ID từ tham chiếu vẫn đi vào bảng chung, xem I1. [Kiểm khai báo](../scripts/tl_core/llm_route.py#L918) · [Ca H3](../scripts/tl_core/llm_route_test.py#L1738) |
| §1, §2.2–§2.3 · K1 #1514 | **ĐÃ VÁ THẬT** hai hành vi đã báo | Nhãn điểm của K1 làm từ chối cả nguồn. Dòng tiếp mở bằng “là” trong nguồn có số đi vào nhánh từ chối dòng không số. Nguồn mất số có dòng thiếu vế thuật ngữ sẽ lệch khi so. Suite giữ ba đầu ra Điều 3 Luật 134/2025/QH15 ở 8/8. Route model giữ nguyên và CLI luôn đặt `can_nguoi_duyet: true`. [K1 gốc](../ops/acceptance/llm-ranh-gioi-khoan/r1/review-10-codex/VERDICT.md#L35) · [Tách thô](../scripts/tl_core/llm_route.py#L1456) · [CLI](../scripts/tl_core/ops_misc.py#L3121) |
| §2.1, §2.4–§2.17 · vùng Điều, câu dẫn, điểm gõ tay và fallback | **ĐÃ VÁ THẬT** ở các biểu hiện từng báo thuộc hợp đồng hiện hành. Quy tắc cắt cuối Điều, đếm qua bảng và nhận đoạn điểm gõ tay **HẾT ĐỐI TƯỢNG** | Tiêu đề nguyên đoạn khớp Điều đích và đứng đầu phần nội dung. Bộ đọc kiểm tới hết tệp, chặn bảng, khối lạ và tiền tố cấu trúc. Chỉ chấp nhận một câu dẫn chuẩn trước khoản đầu hoặc vắng. Đoạn có chữ sau khoản đầu phải có đánh số tự động hợp lệ. §2.7 D1 đã bỏ `KhongCauTruc`. DOCX thiếu số tự động ném `ValueError`, CLI trả rc 2. [Duyệt khối](../scripts/tl_core/llm_route.py#L1008) · [Vùng Điều](../scripts/tl_core/llm_route.py#L1318) · [Câu dẫn](../scripts/tl_core/llm_route.py#L1408) · [CLI DOCX](../scripts/tl_core/ops_misc.py#L3037) |
| §2.4–§2.15, §2.22–§2.26 · số Word | **ĐÃ VÁ THẬT** các biểu hiện gốc trong miền hỗ trợ | `start` vắng có gốc 0, `startOverride` thay gốc khởi tạo, bộ đếm tách `numId` và xóa cấp sâu khi cấp cha tăng. Chặn nhảy cấp, ID/cấp trùng và các cấu hình restart ngoài miền. Lúc ghép chỉ nhận một `numId`, khoản có nhãn thập phân của chính cấp ấy và số liên tục từ 1. Điểm giữ thứ tự tài liệu và thuộc khoản đang mở. [Định nghĩa số](../scripts/tl_core/llm_route.py#L786) · [Bộ đếm](../scripts/tl_core/llm_route.py#L1290) · [Ghép khoản](../scripts/tl_core/llm_route.py#L1362) |
| §2.5–§2.13, §2.23–§2.29 · chữ còn hiệu lực | **ĐÃ VÁ THẬT** đối với chữ bị bỏ, phân cách, ngắt và ký hiệu theo các ca gốc | Duyệt XML gốc, giữ `ins`/`moveTo`, lọc `del`/`moveFrom` và tính gạch đơn, gạch kép riêng. Chặn sửa dấu đoạn và mốc move thiếu cặp. Dùng chung cách đọc `xml:space`. Mẩu đã bỏ chỉ chứa khoảng trắng giữ lại phân cách. Cờ ngắt và phần tử run lạ được ghi sau khi xét gạch. I1 còn ở lớp tra bảng style. [Đọc chữ](../scripts/tl_core/llm_route.py#L1043) · [Lọc run](../scripts/tl_core/llm_route.py#L1120) · [Dấu đoạn và move](../scripts/tl_core/llm_route.py#L1273) |
| §2.14–§2.21 · part, tiền tố và ký tự | **ĐÃ VÁ THẬT** trong miền công bố | Quan hệ dùng URI Transitional đầy đủ và tệp quan hệ của part chính. Parser đọc bytes. QName theo namespace, chữ gốc được kiểm trước gộp hoặc tách. Đường thô kiểm một BOM. Giá chặn dẫn chiếu đầu đoạn và ký tự ngoài tập đã được khai. [Quan hệ](../scripts/tl_core/llm_route.py#L745) · [Biên ký tự](../scripts/tl_core/llm_route.py#L619) |
| §2.22–§2.23 · đường số hiệu | **ĐÃ VÁ THẬT** đối với chốt strict và chặn trần. U2, V3, W1, W3 và phần số hiệu của W2 là giới hạn đã duyệt | Lời gọi `tl extract` có `--markup-strict`, kiểm rc, mốc Điều và tín hiệu chạm trần. Hành vi làm sạch cache, cắt Điều và lọc markup của bộ đọc dùng chung thuộc phạm vi đã công bố. I2 nằm trong bộ tách thô của packet, áp cả tệp văn bản địa phương. [Lời gọi extract](../scripts/tl_core/llm_route.py#L1696) · [Giới hạn](../ops/specs/llm-khoan-docx-r32.md#L269) |
| §3 · so nguyên văn, CLI và đột biến | **ĐẠT** ở suite sẵn có | So lần lượt số lượng, vị trí, số khoản và cả hai vế, giữ ranh giới dòng. Trên DOCX chỉ dò từ nối ở đoạn mở khoản. Bỏ, cắt, ghép hoặc tráo khoản so với bản phân đoạn đã đọc đều lệch. Chỉ ghi `--out` khi phép so đạt. Sai sót ở phân đoạn đầu vào như I2 có thể truyền qua phép so. [Phép so](../scripts/tl_core/llm_route.py#L1591) · [Đầu ra CLI](../scripts/tl_core/ops_misc.py#L3133) · [Harness](../scripts/tl_core/llm_route_test.py#L2284) |

### Các finding lịch sử

ID có nghĩa theo từng lượt. “Đã vá” trong bảng chỉ các biểu hiện đã báo và còn hiệu lực. Giới hạn đã duyệt giữ nguyên trong đặc tả r32. [Bảng lịch sử lượt 31 trên exact SHA 7e9cde7](../ops/acceptance/llm-khoan-docx/r1/review-31-codex/VERDICT.md#L29)

| Lượt #1525 | Đối chiếu trên r32 |
| --- | --- |
| [1](../ops/acceptance/llm-khoan-docx/r1/review-1-codex/VERDICT.md) | A1 phần cắt vùng và A6 hết đối tượng. Phần còn lại A1, A2–A5 và A7–A8 đã vá. |
| [2](../ops/acceptance/llm-khoan-docx/r1/review-2-codex/VERDICT.md) | Phần cắt B1 và đếm bảng B2 hết đối tượng. Phần còn lại B1/B2 và B3–B8 đã vá. |
| [3](../ops/acceptance/llm-khoan-docx/r1/review-3-codex/VERDICT.md) | C1 phần điểm cắt và C2 phần duyệt hàng/ô hết đối tượng. Phần còn lại C1/C2 và C3–C7 đã vá. |
| [4](../ops/acceptance/llm-khoan-docx/r1/review-4-codex/VERDICT.md) | D1 phần cắt hết đối tượng, bỏ fallback đã vá. D2–D4 và D6 đã vá, D5 đã khai giới hạn Strict. |
| [5](../ops/acceptance/llm-khoan-docx/r1/review-5-codex/VERDICT.md) | E1/E3/E4 hết đối tượng. E2/E5/E6 đã vá. |
| [6](../ops/acceptance/llm-khoan-docx/r1/review-6-codex/VERDICT.md) | F1 cắt Điều và F2 nhận đoạn điểm gõ tay hết đối tượng. F3–F6 đã vá. |
| [7](../ops/acceptance/llm-khoan-docx/r1/review-7-codex/VERDICT.md) | G1–G6 đã vá. G3 hết đối tượng đối với cơ chế khởi tạo tổ tiên cũ. |
| [8](../ops/acceptance/llm-khoan-docx/r1/review-8-codex/VERDICT.md) | H1–H5 đã vá. |
| [9](../ops/acceptance/llm-khoan-docx/r1/review-9-codex/VERDICT.md) | J1–J5 đã vá. |
| [10](../ops/acceptance/llm-khoan-docx/r1/review-10-codex/VERDICT.md) | K1–K4 đã vá. |
| [11](../ops/acceptance/llm-khoan-docx/r1/review-11-codex/VERDICT.md) | L1–L6 đã vá. |
| [12](../ops/acceptance/llm-khoan-docx/r1/review-12-codex/VERDICT.md) | M1–M2 đã vá với các đầu vào đã báo. I1 là đường tra bảng riêng. |
| [13](../ops/acceptance/llm-khoan-docx/r1/review-13-codex/VERDICT.md) | N1–N3 đã vá. |
| [14](../ops/acceptance/llm-khoan-docx/r1/review-14-codex/VERDICT.md) | Q1/Q2 đã vá bằng chốt ký tự gốc và chỉ dẫn giữ nguyên dẫn chiếu. |
| [15](../ops/acceptance/llm-khoan-docx/r1/review-15-codex/VERDICT.md) | R1–R3 đã vá. |
| [16](../ops/acceptance/llm-khoan-docx/r1/review-16-codex/VERDICT.md) | S1–S3 đã vá. |
| [17](../ops/acceptance/llm-khoan-docx/r1/review-17-codex/VERDICT.md) | T1/T2 đã vá trong packet. Phần bộ đọc chung nằm trong U2. |
| [18](../ops/acceptance/llm-khoan-docx/r1/review-18-codex/VERDICT.md) | U1 đã vá theo miền chữ số ASCII. U2 thuộc giới hạn đã duyệt. |
| [19](../ops/acceptance/llm-khoan-docx/r1/review-19-codex/VERDICT.md) | V1/V2/V4 đã vá. V3 thuộc giới hạn đã duyệt. |
| [20](../ops/acceptance/llm-khoan-docx/r1/review-20-codex/VERDICT.md) | W2 DOCX và W4/W5 đã vá. W1/W3 và W2 số hiệu thuộc giới hạn đã duyệt. |
| [21](../ops/acceptance/llm-khoan-docx/r1/review-21-codex/VERDICT.md) | X1–X3 đã vá ở dạng đã báo. |
| [22](../ops/acceptance/llm-khoan-docx/r1/review-22-codex/VERDICT.md) | Y1–Y3 đã vá ở dạng đã báo. I1 là xung đột với metadata, ngoài chốt ID trùng giữa hai định nghĩa của Y2. |
| [23](../ops/acceptance/llm-khoan-docx/r1/review-23-codex/VERDICT.md) | Z1–Z4 đã vá. |
| [24](../ops/acceptance/llm-khoan-docx/r1/review-24-codex/VERDICT.md) | A1/A2 đã vá. |
| [25](../ops/acceptance/llm-khoan-docx/r1/review-25-codex/VERDICT.md) | B1 đã vá các ví dụ gốc. Lớp miền nhãn còn I2. B2/B3 đã vá. |
| [26](../ops/acceptance/llm-khoan-docx/r1/review-26-codex/VERDICT.md) | C1/C2 đã vá các dạng đã báo. Lớp miền nhãn còn I2. |
| [27](../ops/acceptance/llm-khoan-docx/r1/review-27-codex/VERDICT.md) | D1 đã vá ca gốc. Lớp miền nhãn còn I2. |
| [28](../ops/acceptance/llm-khoan-docx/r1/review-28-codex/VERDICT.md) | E1 đã vá ca gốc. Lớp miền nhãn còn I2. |
| [29](../ops/acceptance/llm-khoan-docx/r1/review-29-codex/VERDICT.md) | F1/F2 đã vá ca gốc. Lớp miền nhãn còn I2. |
| [30](../ops/acceptance/llm-khoan-docx/r1/review-30-codex/VERDICT.md) | G1/G2 đã vá ca gốc và H1/H2 đã vá ca phát sinh báo ở lượt 31. Lớp tra bảng và miền nhãn còn I1/I2. |
| [31](../ops/acceptance/llm-khoan-docx/r1/review-31-codex/VERDICT.md) | H1–H3 theo ba dòng đầu của bảng đối chiếu. |

Ở #1514, A1/A2/D3/E2/F2 về câu dẫn, C1 về tiêu đề dính thân, A3/C2/D1/E1/F1 về dấu kết hoặc số nội dòng, và G1/H1/J1/K1 về ghép sai dòng đều có chốt hiện hành. X2/X3/X4 giữ chốt phân cách, dấu kết và nguyên văn cả dòng điểm trong bộ so. A4 giữ đối chứng 8/8. B1 về bề mặt được đối chiếu qua launcher. D2 và ngoại lệ dấu số nội dòng của C2 nằm trong giới hạn công bố. Với thô mất cấp, nhiều dòng đủ hai vế và dấu kết vẫn có thể trông hệt các khoản, và tiểu mục có đúng hình dạng số khoản kế vẫn có thể qua. Phạm vi thô ghi rõ ranh giới phải do người duyệt kiểm tra. I2 có dấu phân biệt nhãn vẫn hiện hữu và thuộc miền `lvlText` đã công bố. [Lượt 10 #1514](../ops/acceptance/llm-ranh-gioi-khoan/r1/review-10-codex/VERDICT.md) · [Phạm vi thô](../scripts/tl_core/llm_route.py#L1424)

## Findings

### I1 [P2] Tham chiếu style vẫn có thể tra trúng khóa nội bộ — scripts/tl_core/llm_route.py:958

**Kịch bản và căn cứ.** Một `pStyle`, `rStyle` hoặc `basedOn` trỏ tên dành riêng cho cờ đánh số mặc định của bộ đọc. Theo H3, tên đó bị cấm ở khai báo style, nên tham chiếu này không trỏ một định nghĩa. Nó vẫn có trong `kieu` với giá trị kiểu `bool`. `_dem_bat_trong_chuoi` và `_theo_kieu` dùng phép kiểm thuộc bảng chung rồi lập chỉ mục như thể đó là tuple style. Với `pStyle`, việc đếm gạch xảy ra trước khi đoạn bị đánh dấu lạ. Với `basedOn`, bước kiểm khác loại bỏ qua khóa vắng trong bảng loại và đường tra tiếp theo chạm nó. Handler không bắt `TypeError`. Khóa dành cho bảng loại có cùng vấn đề miền khóa, với giá trị kiểu dict. Suy luận từ mã. [Tạo bảng](../scripts/tl_core/llm_route.py#L928) · [Tra chuỗi style](../scripts/tl_core/llm_route.py#L944) · [Điểm gọi](../scripts/tl_core/llm_route.py#L1104) · [Handler](../scripts/tl_core/ops_misc.py#L3044)

**Hạng và đề xuất.** P2 theo H3, vì traceback trước bước kiểm nguyên văn làm mất chẩn đoán rc 2. Tách metadata khỏi bảng định nghĩa hoặc chỉ cho tra cứu trong tập ID đã xác thực của định nghĩa. Kiểm đủ ba điểm vào với tên dành riêng và giữ quy tắc đã công bố cho `rStyle` trỏ một style vắng. [H3 lượt 31](../ops/acceptance/llm-khoan-docx/r1/review-31-codex/VERDICT.md#L82) · [§2.33–§2.34](../ops/specs/llm-khoan-docx-r32.md#L378)

### I2 [P2] Nhãn thô còn lọt khi hai placeholder chữ viết liền — scripts/tl_core/llm_route.py:526

**Kịch bản và căn cứ.** Bản chép thô mang nhãn điểm gồm một thành phần số, dấu chấm rồi hai thành phần chữ viết sát nhau, có đệm sau nhãn để tách thân. Miền `_nhan` cho phép nhãn có cấu trúc này, chẳng hạn dùng số thứ tự của chính cấp điểm và hai placeholder chữ khác nhau từ cấp trên. Các nhánh số–dấu–chữ trong `_RE_NHIEU_CAP` đòi thành phần chữ là một chữ lặp đứng riêng. Vì có hai chữ khác nhau liền nhau, các nhánh ấy bỏ qua. `_RE_SO_KHOAN` sau đó nhận số kèm dấu chấm, và ưu tiên này bỏ qua `_RE_DIEM`. Nếu số đầu trùng thứ tự kế và thân điểm đủ hai vế, dấu kết, điểm có thể thành khoản riêng với phần chữ của nhãn còn trong thuật ngữ. `lech_nguyen_van` có thể nhận đầu ra khớp phân đoạn đó. Tình huống dùng dấu chấm giữa các thành phần và không có đệm sau dấu chấm. Suy luận từ mã. [Cú pháp nhãn cấu trúc](../scripts/tl_core/llm_route.py#L978) · [Cú pháp thô](../scripts/tl_core/llm_route.py#L517) · [Thứ tự nhánh](../scripts/tl_core/llm_route.py#L1456) · [Miền nhãn](../ops/specs/llm-khoan-docx-r32.md#L350)

**Hạng và đề xuất.** P2 theo H2 và K1 vì cần mất cấp, nhãn cụ thể trùng số kế, thân hợp lệ và đầu ra khớp phân đoạn thô, vốn mang cờ duyệt. Đồng bộ miền nhãn nhiều thành phần với miền mà `_nhan` sinh được, kể cả thành phần kề nhau. Phép kiểm đóng lớp cần giữ đối chứng với thân dính số hợp lệ, thân mở ngoặc và ngoại lệ đệm sau dấu. Nếu thu hẹp miền hỗ trợ, phải đồng bộ đặc tả và hướng dẫn. [H2 lượt 31](../ops/acceptance/llm-khoan-docx/r1/review-31-codex/VERDICT.md#L76) · [§2.34](../ops/specs/llm-khoan-docx-r32.md#L386)

| Lớp | Finding còn mở | Lịch sử và cách đóng |
| --- | --- | --- |
| `docx-markup-du-thao` | 0 biểu hiện đã báo còn mở trong miền đã kiểm | A4 lượt 1 → B3/C4/E2 → F2 lượt 29 → G1 lượt 30 → H1 lượt 31. Ca và đột biến H1 xác nhận lựa chọn mặc định dùng loại hiệu lực. |
| `docx-khoa-bang-style` | I1 · P2 | Y2 lượt 22 → H3 lượt 31 → I1. Sửa chung ở miền khóa của cả định nghĩa và tham chiếu. |
| `ranh-gioi-khoan` | I2 · P2 | K1 #1514 → V4/W4/X3/Y3/Z3/A2/B1/C1/D1/E1/F1 → G2/H2 → I2. So miền nhãn sinh được có dấu với miền chặn và ngoại lệ đã khai. |
| `docx-so-hien-thi` | 0 biểu hiện đã báo còn mở trong miền đã kiểm | A2/B2/G1/J1/V2/W5/X2/Y2/Z2. Ca sẵn có kiểm gốc, override, reset, nhiều danh sách và định nghĩa lỗi. |
| `docx-test-doc-lap` | 0 biểu hiện đã báo còn mở trong miền đã kiểm | A7/B7/C6/D4/E5/F5/G5/H3/J4/Z4/B2. Harness đo các chốt r32, phép đo cho I1/I2 chưa có. |

Đối chiếu §2.5 và các sửa đổi sau đó cho thấy bookmark, comment, quyền chỉnh sửa, hyperlink, content control, tab, dấu nối không ngắt và dấu ngắt trang do Word render đều có nhánh đọc. Hình, trường, ký hiệu, chú thích, bảng, ngắt mềm và phần tử tương thích thuộc các giới hạn đã khai. Trong dữ liệu có sẵn chưa xác lập được một phần tử phổ biến khác của Word hoặc Google Docs gây chặn oan ngoài hợp đồng. [Danh sách phần tử](../scripts/tl_core/llm_route.py#L652) · [Hướng dẫn DOCX](../docs/GOI_AGENT_DA_NEN.md#L392)

## Kết quả test và đột biến

Linux x86_64, Python 3.13.18, Git 2.43.0, Codex CLI 0.172.0, `core.abbrev=7`. Dùng `PYTHONDONTWRITEBYTECODE=1` và đưa bytecode cache ra ngoài checkout. Log và mã thoát tại `/tmp/wp1525-r32-review.DHO20g/`. Hai bản sao Git cục bộ detached dùng chung object store, mỗi bản có tree khớp OID đã ghi.

| Lệnh | Trạng thái | Mã thoát và bằng chứng |
| --- | --- | --- |
| `python scripts/tl_core/llm_route_test.py` | `passed` | rc 0. **63/63** ca đạt, **261/261** đột biến bị giết. `route.log`. |
| `python scripts/tl.py --deterministic workflow-audit --strict --json` | `passed` | rc 0, `ok=true`. 26 card, 60 task, 194 lệnh hiện diện, warnings rỗng. `audit.log`. |
| `python scripts/tl.py --deterministic golden-test --json` | `passed` | rc 0 trên head và base. **20/20** ca và **20/20** bản chiếu ổn định, **19/20** stdout thô trùng byte. Sai khác duy nhất ở khóa biến động đã khai `snapshot_age_s` của `hygiene_sweep_fixture`. `golden.log`, `golden_clean.log`, `golden_base.log`. |
| `python scripts/tl.py release-verify RELEASE_MANIFEST.json --strict --json` | `passed` trên bản sao sạch | rc 0, `ok=true`, **187/187** tệp, 0 sai, thiếu hoặc thừa. Package SHA-256 khớp `483dc683b61d9191cb36d439db1066c09b30f7d9ed4451f56c2960d9fe9d6a21`. Lần đầu tại checkout có verdict trả rc 2 vì dư đúng `.review/VERDICT.md`. `release_clean.log`, `release.log`. |
| `python ops/lease_publish.py check --root . ops/leases/llm-khoan-docx-r32-g1-claude.yaml` | `passed` cục bộ | rc 0, “ĐĂNG ĐƯỢC”, Issue #1525, neo `64b7f2c14776`, hạn 21:48 UTC. Hai lớp GitHub ngoài phép đo cục bộ. `lease.log`. |
| `python scripts/tl.py --selftest` | `failed` trên head và base | rc 1 mỗi bản. Head **1774/1790**, base **1773/1789**. Ca mới `r1525_llm_khai_niem_tep_docx_cau_truc` có `[OK]` trên head. `selftest.log`, `base_selftest.log`. |
| `python scripts/tl.py --deterministic determinism-audit --strict --json` | `passed` | rc 0, `ok=true`, **15/15** phép. `determinism.log`. |
| `python scripts/tl.py doc-claims-check --strict --json` | `failed` trên head và base | rc 2 mỗi bản. Cùng một cờ cứng `SHA_NOT_A_COMMIT` cho `9941d8af52aeede1c78ea4e232fbe9a8d5272033` ở `docs/PROTOCOL_DA_PHIEN.md:1680`. `git cat-file` xác nhận object vắng trong checkout shallow. `claims.log`, `base_claims.log`. |
| `python -m ruff check --no-cache --select F scripts/tl.py` | `failed` lint, đạt tiêu chí delta | Ruff 0.15.15, rc 1 mỗi bản. Cùng 12 F821, 0 F401 và hai log khớp byte. `ruff_lint.log`, `base_ruff.log`. |
| `python -m ruff check --no-cache --select F scripts/tl_core/llm_route.py scripts/tl_core/llm_route_test.py` | `passed` | rc 0, “All checks passed!”. `ruff_modules.log`. |
| `loi_ruff_ci()` qua `runpy.run_path(".claude/dev/ci_dang_ky_test.py")` | `passed` | rc 0, `RUFF_CONTRACT 3 []` cho hợp đồng pin/probe workflow. `ruff_contract.log`. |
| `git diff --check` cho bản vá, packet và toàn PR | `passed` bản vá và packet, `failed` toàn PR | rc 0, 0, 2. Ba dấu ngắt Markdown bằng khoảng trắng ở dòng 3–5 của verdict lượt 8 #1514. `source_meta.log`. |

So hai danh sách ID selftest đỏ đã sắp bằng `cmp` cho rc 0. Cùng 16 ID đỏ. 14 ID thuộc nhóm `/tmp/.git` rỗng đã nêu, gồm 8 `r973_bootstrap_*`, 5 `wp433_*` và `wp727_tl_gws_refresh`. Hai ID còn lại là `r226_nguong_l2_troi_theo_abbrev_va_ci_ghim` và `r268_l2_trichotomy_theo_trang_thai_object`. Log head SHA-256 `60c870879b7a0c45f6e717734ee7e529c6cc544817bba76bb188bac782100c88`, log base `ccf10ecb441bbcce9d5631a4642c1825f2ae261915bdc634bccb6dfd56a1d2bc`.

Harness chép từng đột biến của `DOT_BIEN` vào thư mục tạm. Lần chạy bằng `python -B -m pdb scripts/tl_core/llm_route_test.py` trên bản sao exact head, breakpoint dòng 2304 với điều kiện `ten.startswith("wp1525_")`, ghi tên, ca đích và `str(sys.exception())`. Rc 0, **164/164** đột biến `wp1525_*` vào đúng nhánh `TinHieuChotCa`. Lần đặt breakpoint theo đường dẫn tương đối không gắn được, được thay bằng breakpoint theo số dòng trong tệp đang chạy. SHA-256 `trace_selected.log` là `8ac9e29677faaa30064677df26d83f7efcab9e65c46827bfce3ac031e961dc71`. [Harness](../scripts/tl_core/llm_route_test.py#L2284)

| Đột biến | Ca đích và tín hiệu |
| --- | --- |
| `wp1525_mac_dinh_loai_tho` | `ca_cau_truc_docx_dat` thấy lại chữ đã gạch do style mặc định không khai loại. |
| `wp1525_so_dinh_chu_khong_dem` | `ca_khoan_mat_so_co_diem_dat` thấy nhãn số–dấu–chữ có đệm trước dấu lọt. |
| `wp1525_style_id_noi_bo` | `ca_cau_truc_docx_chan` báo `TypeError` thay vì `ValueError` với ID khai báo trùng khóa nội bộ. |
| `wp1525_tho_nhan_diem` | `ca_wp1514_luot9` thấy dòng điểm trở thành khoản thô. |
| `wp1525_khong_dat_lai_cap_con`, `wp1525_bo_qua_start_override` | `ca_cau_truc_docx_dat` thấy nhãn điểm tiếp tục ở khoản sau và số khoản bắt đầu ở 5 khi bỏ override. |

## Không đo được

- I1 và I2 dựa trên luồng mã. Tái hiện hai biểu hiện mới và xác định tần suất chặn oan trong bản Word hoặc Google Docs thật cần dữ liệu ngoài bộ có sẵn. Checkout không có tệp DOCX được Git theo dõi.
- `skipped`: 0 trong sáu lệnh của prompt. `not_run`: Windows bản địa, CI từ xa, hai lớp GitHub của lease, model thật và LIVE. Windows là `required` theo M3 vì diff toàn PR có dòng Python thêm hoặc sửa chứa `encoding=`. [ADR-0060 M3](../docs/adr/0060-dieu-kien-merge-va-moc-ready.md#L43)
- Model và effort phục vụ là `KHONG_DO_DUOC` từ metadata đã giao. Launcher đang ở trạng thái `dang_chay` khi đọc. Rc con, SHA-256 stdout và trạng thái terminal cần readback sau khi lượt gọi kết thúc. [Run launcher](../../run/2688dc5b/run.json)

## Readback và kết luận

Head và tree khớp đầu và cuối. `git diff --exit-code` và `git diff --cached --exit-code` đều rc 0 trên checkout được giao. Các lệnh sẵn có sinh fixture golden và state bị Git ignore trong checkout. Hai thư mục sinh ra được chuyển vào thư mục tạm sau khi test kết thúc. Readback cuối thấy `.codex/` như lúc đầu và thêm `.review/VERDICT.md`. Snapshot xác nhận delta quan sát được giữa hai mốc. Repo nguồn Executor nằm ngoài phạm vi quan sát.

Còn **0 P0, 0 P1, 2 P2, 0 P3**. Đóng **1/3** lớp mở từ lượt 31 trong miền đối chiếu. `APPROVE` theo ngưỡng verdict trong prompt. Điều kiện merge của ADR-0060 M1 vẫn chưa đạt vì I1 và I2 còn mở. Bằng chứng selftest N/N, doc-claims strict và Windows trên exact head cũng chưa đạt hoặc chưa có. [Protocol §8.3](../docs/PROTOCOL_DA_PHIEN.md#L812) · [ADR-0060 M1](../docs/adr/0060-dieu-kien-merge-va-moc-ready.md#L32) · [ADR-0062](../docs/adr/0062-adr-0060-mac-dinh-va-dong-bang-adr-0054.md#L12)

P2_mo: 2
VERDICT: APPROVE
