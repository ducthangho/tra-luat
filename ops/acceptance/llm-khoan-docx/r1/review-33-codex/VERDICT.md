# Verdict packet #1525 r33 lượt 33 — Codex
reviewed_sha: 3278bfe6aad3bb0f3f3cc9e6d97dbdc7d38618c9

- Tree `01ac1c9478ea422342b564903713d7bf84bae945`, checkout detached, lớp `sensitive`.
- Base nghiệm thu `64b7f2c14776d5d0e1d34a6be4725490956f5bec`. Nền diff packet `fcb12b3`, nền diff bản vá `38a01cf`.
- SHA-256 của blob đặc tả r33 tại head và bản đọc tại checkout đều là `d81835df4b4dea11ca8bdd318756ad6e176ea1a6d9a9882792b3d6bc1edf7e58`, khớp lease r33/g1.
- Reviewer `openai_codex / codex_cli / machine` theo lượt gọi được giao.

## Preflight

- Repo `ducthangho/tra-luat`, nhánh ứng viên `ccr-89c0d2e2-inanqb`; ref local và remote-tracking cùng trỏ exact head. Tree của base là `0cc14e79cecd2ce44bc4dc6cff92cadb31fd7ee4`; `git merge-base` trả exact base. Mốc giao #1514 là `fcb12b3873c3bec2c339029136243ed2c804ce05`, mốc bản vá là `38a01cfe72d1f43d000b319730916db6054a49a3`. SHA-256 luồng `git diff --binary` lần lượt theo bản vá, packet, toàn PR là `af9bbda4601e5dea568abd2c0d42db6a95dcbdc3becbf6cb7ac55486be2a3388`, `3edc72d2edc5dde4bc5624570dcc82476619290bfd166f68ad6ebff5822a1834`, `69e89570ce2462bd3da7e904c12a40a26ed142b74224757f56c16ee95f10d665`.
- Run launcher `ac9b50a78d604b72a51f4b13622f573b`; SHA-256 prompt `29cae7255d816c409d177195fad8b56d920f4901adc0dd96c3e2a69a47bf88f7` khớp snapshot, run và checkpoint. SHA-256 checkpoint `a186d068500b4553602965ccf33eb8da9ef300716e32c172ad339ccbbb6dccd2` khớp run. Executor `anthropic_claude / claude_code / machine/local` theo lease. Checkout riêng và context reviewer độc lập. Sandbox `workspace-write`, mạng bị giới hạn.
- Lease #1525 revision 33, generation 1, lượt **33/33**, inference budget 0, hạn 22:08 UTC ngày 26-11-2026. Lớp khai báo và hiệu lực đều là `sensitive`. Bảng ghi quyền đứng và lịch sử thay hợp đồng khớp đặc tả. [Lease r33](../ops/leases/llm-khoan-docx-r33-g1-claude.yaml) · [Đặc tả r33](../ops/specs/llm-khoan-docx-r33.md)
- Write set **176** đường dẫn, SHA-256 tính lại `7c3648fdceafd52c327df18cac4688970b60e591843a891aac3b0d4cc4f235c7`. Bản vá khớp **8/8** đường dẫn. Diff packet khớp **172/172** sau khi trừ đúng bốn hồ sơ #1514 mà prompt loại ra. Trong **220** đường dẫn của toàn PR, **48** đường ngoài lease r33 đều là hồ sơ, lease và spec của #1514. Cặp bia mộ khớp **33/33** hai chiều. Hash đặc tả khớp **34/34** trên đĩa và trong Git, từ #1514 r9 đến #1525 r33. [Bia mộ #1514 r9](../ops/leases/llm-ranh-gioi-khoan-r9-g1-claude.yaml) · [Bia mộ r32](../ops/leases/llm-khoan-docx-r32-g1-claude.yaml#L213)

## Đối chiếu lượt 32 và đặc tả r33

| Mục | Trạng thái | Bằng chứng |
| --- | --- | --- |
| I1 lượt 32 · §2.35 | **ĐÃ VÁ THẬT** | Cả hai hàm đi qua `basedOn` dùng tập ID của bảng loại, kể cả khi điểm vào là khóa nội bộ. `pStyle` ngoài tập bị đánh dấu lạ. `rStyle` vắng và `basedOn` vắng đi hết đường đọc với kết quả dương. Hai đột biến mở lại tra theo bảng chung tái hiện `TypeError` ở ca `pStyle`. [Mã](../scripts/tl_core/llm_route.py#L947) · [Điểm vào](../scripts/tl_core/llm_route.py#L1120) · [Ca dương](../scripts/tl_core/llm_route_test.py#L1532) |
| I2 lượt 32 · §2.35 | **VÁ MỘT PHẦN, VÁ SINH LỖI MỚI** | Nhãn số–dấu–hai chữ kề có dấu kết và không có đệm trước chữ đã bị chặn; bỏ nhánh r33 làm ca đích đỏ. Kịch bản gốc của I2 thiếu dấu kết thuộc giới hạn mới, được đưa về bước duyệt ranh giới. Nhãn có dấu kết nhưng đệm sau dấu nối hoặc có dấu ở vị trí khác vẫn lọt (J1). Mẫu mới sinh số cách quay lui tăng theo cấp số nhân (J2). [Regex](../scripts/tl_core/llm_route.py#L526) · [Ca r33](../scripts/tl_core/llm_route_test.py#L718) · [I2 gốc](../ops/acceptance/llm-khoan-docx/r1/review-32-codex/VERDICT.md) |
| §1 và §2.2–§2.3 · K1 #1514 | **ĐÃ VÁ THẬT** với hai hành vi gốc | Điểm nhận dạng được trả `None`, dòng tiếp mở “là” ở nguồn có số rơi vào nhánh từ chối dòng không số. Nguồn mất số không ghép dòng; dòng mở “là” thiếu vế thuật ngữ ở phép so. Ba đầu ra lưu của Điều 3 Luật 134/2025/QH15 vẫn đạt 8/8 trong suite. Đường gọi model giữ nguyên, CLI gắn cờ duyệt và phạm vi tương ứng với từng đường. [K1 gốc](../ops/acceptance/llm-ranh-gioi-khoan/r1/review-10-codex/VERDICT.md#L35) · [Tách thô](../scripts/tl_core/llm_route.py#L1463) · [CLI](../scripts/tl_core/ops_misc.py#L3130) |
| §2.1, §2.4–§2.18 · vùng Điều, điểm gõ tay, câu dẫn | **ĐÃ VÁ THẬT** ở hành vi còn hiệu lực. Quy tắc cắt vùng, đếm trong bảng và nhận điểm gõ tay **HẾT ĐỐI TƯỢNG** | Tiêu đề nguyên đoạn phải đứng đầu phần có nội dung và khớp Điều được yêu cầu. Vùng chạy tới hết tệp; bảng, khối lạ, tiêu đề khác và đoạn không số sau khoản đầu bị chặn. Chỉ nhận tối đa một câu dẫn chuẩn trước khoản đầu. Chốt hỗn hợp từ chối số gõ tay trong đoạn có số tự động. Nhánh `KhongCauTruc` đã bị bỏ ở r5 và không có lùi về thô khi DOCX thiếu danh sách. [Vùng Điều](../scripts/tl_core/llm_route.py#L1321) · [Ghép khoản](../scripts/tl_core/llm_route.py#L1379) · [Câu dẫn](../scripts/tl_core/llm_route.py#L1411) · [CLI](../scripts/tl_core/ops_misc.py#L3037) |
| §2.4–§2.16, §2.22–§2.26 · số Word | **ĐÃ VÁ THẬT** với các biểu hiện đã báo trong miền hỗ trợ | `start` vắng cho gốc 0; `startOverride` thay gốc; bộ đếm theo từng `numId` và xóa cấp sâu khi mục cha tăng. Chặn nhảy cấp, cấu hình khởi động lại ngoài miền, ID hoặc cấp trùng, số trên 999. Khi ghép chỉ nhận một `numId`, nhãn khoản thập phân của chính cấp đó, số liên tục từ 1. Điểm giữ thứ tự và thuộc khoản đang mở. [Định nghĩa](../scripts/tl_core/llm_route.py#L789) · [Bộ đếm](../scripts/tl_core/llm_route.py#L1294) · [Ghép khoản](../scripts/tl_core/llm_route.py#L1372) |
| §2.5–§2.14, §2.23–§2.29, §2.32–§2.35 · markup và style | **ĐÃ VÁ THẬT** ở các ca gốc | Duyệt XML gốc, giữ `ins` và `moveTo`, bỏ `del` và `moveFrom`, xét gạch đơn/kép riêng. Chặn sửa dấu đoạn và mốc move thiếu cặp. Dùng chung `xml:space` và phép đọc mẩu bị bỏ chỉ có khoảng trắng. Cờ ngắt và phần tử run lạ được ghi sau khi xét gạch. Style vắng/sai loại, style mặc định, khóa trùng và khóa nội bộ có chốt riêng. [Run](../scripts/tl_core/llm_route.py#L1101) · [Dấu đoạn và move](../scripts/tl_core/llm_route.py#L1276) · [Style](../scripts/tl_core/llm_route.py#L890) |
| §2.14–§2.21 · part, tiền tố, ký tự gốc | **ĐÃ VÁ THẬT** trong miền công bố | Quan hệ dùng URI Transitional đầy đủ và tệp quan hệ của part chính. Parser nhận bytes. Khối nhận theo QName. Mọi đoạn từ tiêu đề trong DOCX và toàn văn thô sau một BOM đều kiểm ký tự gốc trước khi gộp hoặc tách. Chặn oan do ký tự ngoài tập và dẫn chiếu đầu đoạn đã được khai. [Quan hệ](../scripts/tl_core/llm_route.py#L748) · [Ký tự](../scripts/tl_core/llm_route.py#L619) · [Tiền tố](../scripts/tl_core/llm_route.py#L1344) |
| §2.21–§2.23 · đường số hiệu | **ĐÃ VÁ THẬT** với chốt strict và chạm trần. U2, V3, W1, W3 và phần số hiệu của W2 là giới hạn đã duyệt | Lời gọi có `--markup-strict` và kiểm rc, mốc Điều, tín hiệu chạm trần. Các hành vi trên snapshot, cắt Điều và lọc markup của bộ đọc dùng chung vẫn theo quyết định chủ kho. J1/J2 nằm ở khâu đọc thô của packet sau khi nhận văn bản, cũng áp cho `--tep` UTF-8. [Lời gọi extract](../scripts/tl_core/llm_route.py#L1699) · [Giới hạn](../ops/specs/llm-khoan-docx-r33.md#L280) |
| §2.25–§2.35 · miền nhận biết nhãn thô | **VÁ MỘT PHẦN** ở lớp `ranh-gioi-khoan` | Chốt nhiều thành phần chạy trước chốt số đơn; các minh chứng đã báo có ca đích. Vẫn có dạng nhãn mang dấu trong miền công bố đi qua bộ tách (J1). Các dạng chỉ ngăn bằng khoảng trắng, phần đuôi chữ kề thiếu dấu và tiểu mục trùng hệt số khoản đơn tiếp theo vẫn thuộc duyệt ranh giới theo giới hạn đã khai. [Ngữ pháp](../scripts/tl_core/llm_route.py#L526) · [Thứ tự nhánh](../scripts/tl_core/llm_route.py#L1450) |
| §3 · so nguyên văn, CLI và đột biến | **ĐẠT** ở phép đo sẵn có | So kiểm số lượng, vị trí, số khoản và toàn bộ hai vế, giữ ranh giới dòng. DOCX chỉ dò từ nối ở đoạn mở khoản. Bỏ, cắt, gộp hoặc tráo khoản so với phân đoạn đã đọc đều lệch, đầu ra chỉ được ghi khi so đạt. Nếu phân đoạn đầu vào sai, đầu ra chép đúng phân đoạn đó vẫn có thể qua, như J1. [Phép so](../scripts/tl_core/llm_route.py#L1594) · [Đầu ra CLI](../scripts/tl_core/ops_misc.py#L3133) · [Harness](../scripts/tl_core/llm_route_test.py#L2303) |

### Finding lịch sử trên ứng viên r33

Mỗi ID thuộc lượt trong cột đầu. “Đã vá” ghi nhận biểu hiện gốc. Trạng thái toàn lớp và các biểu hiện còn mở nằm ở bảng sau các finding.

| Lượt và nguồn SHA | Đối chiếu |
| --- | --- |
| [1 · `3d24751`](../ops/acceptance/llm-khoan-docx/r1/review-1-codex/VERDICT.md) | A1 phần cắt vùng, A5 phần nội dung ngoài Điều và A6 hết đối tượng theo r7. A1 phần kiểm tiêu đề/bảng/khối, A2–A4, A5 phần định nghĩa chưa dùng, A7–A8 đã vá. |
| [2 · `38c481f`](../ops/acceptance/llm-khoan-docx/r1/review-2-codex/VERDICT.md) | B1 phần điểm cắt và B2 phần duyệt bảng hết đối tượng. Các phần còn lại của B1/B2 và B3–B8 đã vá. |
| [3 · `b0f3cb9`](../ops/acceptance/llm-khoan-docx/r1/review-3-codex/VERDICT.md) | C1 phần cắt vùng và C2 phần đếm trong bảng hết đối tượng. Ngắt ở tiêu đề C1, nhãn chữ sau Z của C2 và C3–C7 đã vá. |
| [4 · `fa3a8e2`](../ops/acceptance/llm-khoan-docx/r1/review-4-codex/VERDICT.md) | D1 hết đối tượng; nhánh `KhongCauTruc` cũng đã bỏ. D2–D4, D6 đã vá. D5 có chẩn đoán và giới hạn DOCX Strict đã công bố. |
| [5 · `3c1e143`](../ops/acceptance/llm-khoan-docx/r1/review-5-codex/VERDICT.md) | E1, E3, E4 hết đối tượng khi bỏ cắt vùng và chặn bảng ở mọi vị trí. E2, E5 và E6 đã vá. |
| [6 · `6781d11`](../ops/acceptance/llm-khoan-docx/r1/review-6-codex/VERDICT.md) | F1 và phạm vi hỗ trợ điểm tay của F2 hết đối tượng; chốt F2 hiện từ chối đoạn không số. F3, F4, F6 đã vá. F5 có đột biến override riêng; kiểm cấp ở đoạn đi qua tập cấp đã xác thực. |
| [7 · `4badb3d`](../ops/acceptance/llm-khoan-docx/r1/review-7-codex/VERDICT.md) | G1/G2 và G4–G6 đã vá. G3 hết đối tượng khi bỏ khởi tạo tổ tiên. |
| [8 · `6d28f34`](../ops/acceptance/llm-khoan-docx/r1/review-8-codex/VERDICT.md) | H1–H5 đã vá. Ngắt trang/cột ở H5 xét theo chữ còn hiệu lực. |
| [9 · `4c647c8`](../ops/acceptance/llm-khoan-docx/r1/review-9-codex/VERDICT.md) | J1–J5 đã vá. Chốt tương thích J2 hiện áp cho toàn part. |
| [10 · `674a28c`](../ops/acceptance/llm-khoan-docx/r1/review-10-codex/VERDICT.md) | K1–K4 đã vá. |
| [11 · `e1ed11f`](../ops/acceptance/llm-khoan-docx/r1/review-11-codex/VERDICT.md) | L1–L6 đã vá; hình dạng L2 được bao bởi chốt tiền tố r14. |
| [12 · `f305663`](../ops/acceptance/llm-khoan-docx/r1/review-12-codex/VERDICT.md) | M1 đã vá bằng chốt tiền tố, M2 đã vá bằng kiểm kiểu và xử lý giá trị vắng. |
| [13 · `069b734`](../ops/acceptance/llm-khoan-docx/r1/review-13-codex/VERDICT.md) | N1–N3 đã vá ở các ca tiền tố, ID dài và QName. |
| [14 · `0447395`](../ops/acceptance/llm-khoan-docx/r1/review-14-codex/VERDICT.md) | Q1/Q2 đã vá bằng chốt ký tự gốc và hướng dẫn giữ nguyên dẫn chiếu. |
| [15 · `b5cff42`](../ops/acceptance/llm-khoan-docx/r1/review-15-codex/VERDICT.md) | R1–R3 đã vá trong miền ký tự và số gõ tay hiện hành. |
| [16 · `7a913aa`](../ops/acceptance/llm-khoan-docx/r1/review-16-codex/VERDICT.md) | S1–S3 đã vá, kể cả đối chứng mốc quyền chỉnh sửa. |
| [17 · `8f31901`](../ops/acceptance/llm-khoan-docx/r1/review-17-codex/VERDICT.md) | T1/T2 đã vá trong packet; phần xử lý ở bộ đọc chung thuộc U2. |
| [18 · `5ed4386`](../ops/acceptance/llm-khoan-docx/r1/review-18-codex/VERDICT.md) | U1 đã vá theo miền chữ số ASCII. U2 là giới hạn đường số hiệu đã duyệt. |
| [19 · `7c4abd7`](../ops/acceptance/llm-khoan-docx/r1/review-19-codex/VERDICT.md) | V1 chốt strict, V2 số mặc định và ca gốc V4 đã vá. V3 là giới hạn đã duyệt. |
| [20 · `8a685fe`](../ops/acceptance/llm-khoan-docx/r1/review-20-codex/VERDICT.md) | W2 DOCX và W4/W5 đã vá ở ca gốc. W1/W3 và phần số hiệu của W2 là giới hạn đã duyệt. |
| [21 · `3d21bd1`](../ops/acceptance/llm-khoan-docx/r1/review-21-codex/VERDICT.md) | X1–X3 đã vá ở ca gốc. |
| [22 · `fbddd47`](../ops/acceptance/llm-khoan-docx/r1/review-22-codex/VERDICT.md) | Y1–Y3 đã vá ở ca gốc; I1 khóa thêm miền tra cứu style. |
| [23 · `30e3e07`](../ops/acceptance/llm-khoan-docx/r1/review-23-codex/VERDICT.md) | Z1–Z4 đã vá ở ca gốc. |
| [24 · `b755fef`](../ops/acceptance/llm-khoan-docx/r1/review-24-codex/VERDICT.md) | A1/A2 đã vá ở ca gốc. |
| [25 · `659d9f2`](../ops/acceptance/llm-khoan-docx/r1/review-25-codex/VERDICT.md) | B1 đã vá ở ca gốc, miền nhãn còn J1. B2/B3 đã vá. |
| [26 · `475fee9`](../ops/acceptance/llm-khoan-docx/r1/review-26-codex/VERDICT.md) | C1/C2 đã vá ở ca gốc. Miền nhãn của C1 còn J1. |
| [27 · `9972282`](../ops/acceptance/llm-khoan-docx/r1/review-27-codex/VERDICT.md) | D1 đã vá ở ca gốc. Miền nhãn còn J1. |
| [28 · `0e1c112`](../ops/acceptance/llm-khoan-docx/r1/review-28-codex/VERDICT.md) | E1 đã vá ở ca gốc. Miền nhãn còn J1. |
| [29 · `291919e`](../ops/acceptance/llm-khoan-docx/r1/review-29-codex/VERDICT.md) | F1/F2 đã vá ở ca gốc. Miền nhãn của F1 còn J1. |
| [30 · `749e6ac`](../ops/acceptance/llm-khoan-docx/r1/review-30-codex/VERDICT.md) | G1/G2 đã vá ở ca gốc. Miền nhãn của G2 còn J1. |
| [31 · `7e9cde7`](../ops/acceptance/llm-khoan-docx/r1/review-31-codex/VERDICT.md) | H1–H3 đã vá ở dạng đã báo. Miền nhãn của H2 còn J1. |
| [32 · `571e83f`](../ops/acceptance/llm-khoan-docx/r1/review-32-codex/VERDICT.md) | I1 đã vá thật. I2 vá một phần, còn J1 và sinh J2. |

Ở #1514, A1/A2/D3/E2/F2 về câu dẫn, C1 về tiêu đề dính thân, A3/C2/D1/E1/F1 về dấu kết hoặc số nội dòng và G1/H1/J1/K1 về ghép sai dòng vẫn có chốt. X2/X3/X4 giữ chốt phân cách, dấu kết và nguyên văn cả dòng điểm trong bộ so. A4 giữ đối chứng 8/8, B1 về bề mặt được đối chiếu qua launcher. D2 và ngoại lệ dấu số nội dòng của C2 nằm trong giới hạn công bố. [Lượt 10 #1514](../ops/acceptance/llm-ranh-gioi-khoan/r1/review-10-codex/VERDICT.md) · [Đặc tả #1514 r9](../ops/specs/llm-ranh-gioi-khoan-r9.md)

## Findings

### J1 [P2] Bộ tách thô vẫn nhận một số nhãn chữ kề có dấu kết làm khoản — scripts/tl_core/llm_route.py:539

**Kịch bản.** Bản chép thô có một điểm mang nhãn Word gồm số, dấu chấm, khoảng đệm ngang, hai thành phần chữ khác nhau viết liền, rồi dấu chấm kết nhãn. Điểm chép thành một dòng có đủ hai vế và dấu kết câu. Nếu số của điểm trùng số khoản kế và các số nhìn thấy vẫn liên tục, bộ tách có thể nhận điểm làm một khoản. Ở nguồn mất số, biến thể ghép số với hai thành phần chữ liền nhau và chỉ đặt dấu chấm ở cuối nhãn có thể được nhận nguyên dòng làm một khoản không số.

**Căn cứ.** `_nhan` cho phép các placeholder liền nhau, có dấu và khoảng cách trong `lvlText`. Nhánh mới đòi chữ phải sát dấu nối và chỉ vào được khi đã có dấu giữa số và chữ. Các nhánh cũ có đệm đòi một chữ cái lặp đứng riêng. Nhánh nhiều cấp bỏ qua cả hai dạng. Ở dạng thứ nhất, `_RE_SO_KHOAN` nhận số và dấu đầu trước khi xét `_RE_DIEM`, để phần chữ của nhãn lọt vào thuật ngữ. Ở dạng thứ hai, cả hai mẫu đầu dòng đều bỏ qua nhãn. Dấu chấm của nhãn không bị chốt ngoặc hay chốt số nội dòng bắt sau khi đã tách. `lech_nguyen_van` so với chính phân đoạn đó. Giới hạn §2.35 dành cho chuỗi chữ kề **thiếu** dấu kết và khoảng đệm của §2.34 dành cho chữ đơn **thiếu** dấu kết. Hai trường hợp trên đều có dấu kết. Suy luận đọc mã. [Dựng nhãn](../scripts/tl_core/llm_route.py#L981) · [Nhận nhãn](../scripts/tl_core/llm_route.py#L526) · [Thứ tự nhánh](../scripts/tl_core/llm_route.py#L1459) · [§2.34–§2.35](../ops/specs/llm-khoan-docx-r33.md#L386)

**Hạng và đề xuất.** P2 theo I2 và K1 vì cần mất cấp, hình dạng nhãn cụ thể, thân đủ điều kiện và đầu ra khớp phân đoạn thô có cờ duyệt. Kiểm miền nhãn trước khi nhận số khoản bằng một phép quét có giới hạn, với quy tắc rõ cho khoảng đệm, vị trí dấu và các placeholder kề nhau. Đối chiếu toàn miền nhãn dựng được có dấu và giữ các đối chứng thân khoản đã duyệt.

### J2 [P2] Regex mới có thể khiến bước so văn bản thô không trả kết quả — scripts/tl_core/llm_route.py:539

**Kịch bản và căn cứ.** Một dòng có số dính với chữ thuộc danh sách cho phép. Sau dấu là một dải dài lặp cùng chữ, tiếp đến một chữ khác, rồi phần văn bản thay cho dấu kết nhãn. Nhánh r33 cho phép lặp ngoài từ hai nhóm trở lên; mỗi nhóm lại có thể nhận tùy ý số lần lặp của chính chữ vừa bắt. Khi thiếu dấu kết, Python `re` phải thử các cách phân chia dải chữ lặp vào nhiều nhóm trước khi trả về không khớp. Số cách phân chia tăng theo cấp số nhân. Nhánh số–chữ cũ không chặn trước vì chữ khác theo sát dải lặp. Chốt này chạy trong đường so sau khi lệnh đã gọi model và trước khi CLI trả trạng thái hoặc ghi `--out`. Suy luận từ mã; thời gian chạy thực tế chưa đo. [Regex](../scripts/tl_core/llm_route.py#L526) · [Kiểm đầu dòng](../scripts/tl_core/llm_route.py#L1459) · [Thứ tự gọi và so](../scripts/tl_core/llm_route.py#L1729)

**Hạng và đề xuất.** P2 theo tiền lệ cạn tài nguyên E6/F4. Tác động trực tiếp là treo bước kiểm của một lần gọi, có thể xảy ra sau khi đã tiêu token. Ngôn ngữ của nhánh r33 tương đương một dải ít nhất hai chữ trong tập: mỗi chữ luôn có thể là một nhóm một ký tự. Dùng lớp ký tự phẳng hoặc bộ quét dùng chung cho J1. Đo cả trường hợp cần khớp và trường hợp thất bại ở dấu cuối.

| Lớp | Biểu hiện mở | Đối chiếu và phép kiểm đóng |
| --- | --- | --- |
| `docx-khoa-bang-style` | 0 | Y2 lượt 22 → H3 lượt 31 → I1 lượt 32. Chốt tra ID dùng chung cho mọi điểm vào và mọi bước `basedOn`. Ca sẵn có khóa thoát có kiểm soát và giữ đường style vắng. |
| `ranh-gioi-khoan` | J1 · P2 | K1 #1514 → V4/W4/X3/Y3/Z3/A2/B1/C1/D1/E1/F1 → G2/H2/I2. So toàn miền dựng nhãn có dấu với miền nhận diện và các ngoại lệ đã công bố. |
| `can-tai-nguyen-doc-nguon` | J2 · P2 | E6 lượt 5 và F4 lượt 6 gây cạn tài nguyên ở bộ đọc Word, đã có chốt cấp và trần số. J2 thuộc bộ tách thô, cần khóa độ phức tạp của nhánh nhãn khi dấu kết vắng. |
| `docx-markup-du-thao`, `docx-so-hien-thi`, `docx-test-doc-lap` | 0 biểu hiện đã báo còn mở trong miền đã kiểm | Ca sẵn có khóa lọc markup, đọc gốc/override/reset, nhiều danh sách và kiểu dữ liệu, cùng các phép đối chiếu trong bảng lịch sử. |

**DOCX Word/Google Docs.** Danh sách hỗ trợ các phần tử không mang nội dung thường gặp như mốc bookmark, đánh dấu soát lỗi, comment, quyền chỉnh sửa và ngắt trang do trình render. Hyperlink, content control, tab, dấu nối không ngắt và ngắt trang/cột cuối đoạn cũng có nhánh riêng. Hình, trường, ký hiệu, chú thích, bảng, ngắt mềm, `mc:` và đếm số qua style thuộc các giới hạn đã khai. Dữ liệu sẵn có chưa xác lập được phần tử export phổ biến gây chặn oan ngoài giới hạn. [Danh sách trong mã](../scripts/tl_core/llm_route.py#L655) · [Hướng dẫn DOCX](../docs/GOI_AGENT_DA_NEN.md#L390)

## Kết quả test và đột biến

Log ở `/tmp/wp1525-r33-evidence.UIz764sH/`. Linux x86_64, Python 3.13.18, Git 2.43.0, Codex CLI 0.172.0, Ruff 0.15.15. Cả checkout được giao và bản sao cục bộ đều ghim `core.abbrev=7`; các phép Python tắt ghi bytecode. Hai bản sao Git cục bộ detached dùng đúng OID/tree ở trên, cùng object store của checkout shallow được giao.

| Lệnh | Trạng thái | Mã thoát và bằng chứng |
| --- | --- | --- |
| `python scripts/tl_core/llm_route_test.py` | `passed` | Rc 0. **63/63** ca đạt và **264/264** đột biến chết bằng tín hiệu của ca đích. `llm.log`. |
| `python scripts/tl.py --deterministic workflow-audit --strict --json` | `passed` | Rc 0, `ok=true`, 26 card, 60 task, 194 lệnh hiện diện, 0 lỗi và 0 cảnh báo. `workflow.log`. |
| `python scripts/tl.py --deterministic golden-test --json` | `passed` | Rc 0, `ok=true`, **20/20** ca đạt, **20/20** bản chiếu ổn định và **20/20** stdout thô trùng byte trong lần chạy này. `golden.log`. |
| `python scripts/tl.py release-verify RELEASE_MANIFEST.json --strict --json` | `failed` tại checkout có verdict; `passed` trên bản sao sạch exact head | Rc 2 do thừa duy nhất `.review/VERDICT.md` được ghi sớm theo prompt. Bản sao sạch rc 0, `ok=true`, **187/187**, 0 sai, thiếu hoặc thừa. Package hash khớp `ec07803848a6a0f5b3b78ce47cb77029c450d1422ea0c1d709c966e42aa6c92e`. `release.log`, `release-clean.log`. |
| `python ops/lease_publish.py check --root . ops/leases/llm-khoan-docx-r33-g1-claude.yaml` | `passed` cục bộ | Rc 0, “ĐĂNG ĐƯỢC”, Issue #1525, base `64b7f2c14776`, hạn 22:08 UTC. Lệnh tự báo hai lớp kiểm GitHub nằm ngoài phép đo local. `lease.log`. |
| `python scripts/tl.py --selftest` | `failed` trên head | Rc 1, **1774/1790**, ca tích hợp `r1525_llm_khai_niem_tep_docx_cau_truc` đạt và kiểm rc 0/5/2 bằng model giả. `selftest.log`. |
| `python scripts/tl.py --deterministic determinism-audit --strict --json` | `passed` | Rc 0, `ok=true`, **15/15** phép trên head. `determinism.log`. |
| `python scripts/tl.py --deterministic doc-claims-check --strict --json` | `failed` trên head và base | Rc 2 mỗi bản, 131 tệp quét mỗi bản, cùng một cờ cứng `SHA_NOT_A_COMMIT` cho `9941d8af52aeede1c78ea4e232fbe9a8d5272033` ở `docs/PROTOCOL_DA_PHIEN.md:1680`. `git cat-file -t` rc 128 trên checkout shallow. `claims.log`, `base-claims.log`. |
| `python -m ruff check --no-cache --select F scripts/tl.py` | `failed` lint, đạt tiêu chí delta | Rc 1 trên head và base, cùng 12 F821, 0 F401, `cmp` hai log rc 0. `ruff-lint.log`, `base-ruff.log`. |
| `python -m ruff check --no-cache --select F scripts/tl_core/llm_route.py scripts/tl_core/llm_route_test.py` | `passed` | Rc 0, “All checks passed!”. `ruff-modules.log`. |
| `loi_ruff_ci()` qua `runpy.run_path(".claude/dev/ci_dang_ky_test.py")` theo adapter | `passed` | Rc 0, `RUFF_CONTRACT 3 []` cho hợp đồng pin/probe workflow. `ruff-contract.log`. |
| `git diff --check <mốc> HEAD` | `passed` bản vá và packet, `failed` toàn PR | Rc lần lượt 0, 0, 2. Toàn PR báo ba dấu xuống dòng cứng Markdown trong verdict lượt 8 #1514, dòng 3–5, có sẵn ở mốc nhận packet. |

Harness tự chép từng đột biến trong `DOT_BIEN` vào thư mục tạm. Chạy lại bằng `python -B -m pdb scripts/tl_core/llm_route_test.py`, breakpoint dòng 2323 với điều kiện `ten.startswith("wp1525_")`. Rc 0, **167/167** đột biến thuộc packet vào nhánh `TinHieuChotCa`; tổng suite vẫn 63/63, 264/264. SHA-256 `mutation-trace-clean.log` là `0f5bc92671e2bc37e02f8ba2ead8aad103a0921a8109cada0df189c5d550b34b`. [Harness](../scripts/tl_core/llm_route_test.py#L2303)

| Đột biến | Tín hiệu từ ca đích |
| --- | --- |
| `wp1525_pstyle_dut_khong_chan`, `wp1525_pstyle_chi_kiem_co_mat` | `ca_cau_truc_docx_chan` phát hiện không từ chối `pStyle` vắng hoặc trỏ kiểu ký tự, tương ứng. |
| `wp1525_theo_kieu_tra_khoa_noi_bo`, `wp1525_dem_tra_khoa_noi_bo` | `ca_cau_truc_docx_chan` phát hiện `TypeError` thay cho `ValueError` khi `pStyle` tra trúng khóa nội bộ. |
| `wp1525_chu_ke_nhau_bo` | `ca_khoan_mat_so_co_diem_dat` phát hiện nhãn hai chữ kề có dấu kết lọt vào phân đoạn thô. |
| `wp1525_tho_nhan_diem` | `ca_wp1514_luot9` phát hiện dòng điểm trở thành khoản thô; hợp đồng K1 bị phá. |
| `wp1525_khong_dat_lai_cap_con`, `wp1525_bo_qua_start_override` | `ca_cau_truc_docx_dat` phát hiện nhãn điểm tiếp số qua khoản sau và số khoản bắt đầu ở 5 khi bỏ override, tương ứng. |

Selftest đối chứng trên base trả rc 1, **1773/1789**. Sắp hai danh sách ID đỏ rồi so bằng `cmp` trả rc 0. Cùng **16** ca đỏ, delta tập lỗi **0**. Trong đó có 14 ca thuộc nhóm `/tmp/.git` rỗng đã nêu (8 `r973_bootstrap_*`, 5 `wp433_*` và `wp727_tl_gws_refresh`) và hai ca `r226_nguong_l2_troi_theo_abbrev_va_ci_ghim`, `r268_l2_trichotomy_theo_trang_thai_object`. Hash log head `21f6344c719d2b9afaf358d4a3d99ab85b445f25b15895e8d56b14c9d36a2da2`, log base `ebb5a7b7e5b23bc37da44e6a53ca0985259b5f58a0a9af701f6fab1af49dfce2`. Gate selftest N/N vẫn đỏ trong môi trường này.

## Không đo được

- J1 và J2 dựa trên đọc mã. Chưa đo ca nhãn lọt mới, tần suất xuất hiện hay thời gian chạy khi dấu kết vắng. Bộ có sẵn đo nhánh mục tiêu r33 và các đối chứng đã ghi. Với I1, hai đột biến truy cập bảng chung đều báo đỏ ngay ở `pStyle`; `rStyle` và `basedOn` có ca dương, chưa có lượt đột biến tách riêng hai điểm vào đó trong bảng sẵn có.
- Chưa đo hành vi của các bản Word/Google Docs thật với phần tử ngoài danh sách, tần suất chặn oan hay kết quả Word render cho biến thể thuộc tính đánh số ngoài ca sẵn có. Checkout không có DOCX được Git theo dõi.
- `skipped` trong sáu lệnh của prompt: 0. `not_run`: Windows bản địa, CI từ xa, hai lớp GitHub của lease, model thật và LIVE. Windows là `required` theo M3 vì diff toàn PR có dòng Python thêm hoặc sửa chứa `encoding=`. [ADR-0060 M3](../docs/adr/0060-dieu-kien-merge-va-moc-ready.md#L43)
- Họ reviewer lấy theo provider đã xác minh từ run launcher. Model và effort phục vụ `KHONG_DO_DUOC` từ metadata hiện có. Run đang ở `dang_chay` khi kiểm; trạng thái terminal, mã thoát của tiến trình reviewer và hash output của launcher chờ lượt gọi kết thúc.

## Readback và kết luận

Head và tree khớp đầu/cuối. `git diff --exit-code` và `git diff --cached --exit-code` đều rc 0. Trước phép đo chỉ thấy `.codex/` là ignored. Sau khi chuyển fixture golden và state do các lệnh tạo vào thư mục bằng chứng, checkout chỉ tăng `.review/VERDICT.md`. Snapshot chứng minh delta quan sát được giữa hai mốc. Repo nguồn của Executor nằm ngoài phạm vi quan sát.

**0 P0, 0 P1, 2 P2, 0 P3.** Đóng 1/2 lớp mở từ lượt 32. Lớp ranh giới còn J1 và bản vá mở lại lớp cạn tài nguyên ở J2. Verdict theo ngưỡng của prompt. Điều kiện merge của ADR-0060 M1 chưa đạt vì còn hai P2. Bằng chứng selftest N/N, doc-claims strict và Windows exact head cũng chưa đạt hoặc còn thiếu. [Protocol §8.3](../docs/PROTOCOL_DA_PHIEN.md#L812) · [ADR-0060 M1](../docs/adr/0060-dieu-kien-merge-va-moc-ready.md#L32) · [ADR-0062](../docs/adr/0062-adr-0060-mac-dinh-va-dong-bang-adr-0054.md#L12)

P2_mo: 2
VERDICT: APPROVE
