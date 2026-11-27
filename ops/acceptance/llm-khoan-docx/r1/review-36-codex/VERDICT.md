# Verdict packet #1525 r36 lượt 36 — Codex

reviewed_sha: 7b839ba02d90015dab228bcf471a832f1a509094
reviewed_tree: bba5c2c0863b8cf2af355fb4b882a0644f39cd7d
base_sha: 64b7f2c14776d5d0e1d34a6be4725490956f5bec

**Kết luận nội dung.** Còn hai lớp P2. K1 gốc đã đóng và ranh giới ký tự vẫn đạt trong phạm vi đã chốt. Danh sách đầu dòng còn vùng giao giữa số khoản và nhãn điểm thập phân. Ngân sách đọc còn khe ở tiền kiểm văn bản thô và xử lý DOCX.

## Preflight

- Checkout detached của `ducthangho/tra-luat`. Merge base khớp `base_sha`; ref `origin/ccr-89c0d2e2-inanqb` được cấp trỏ đúng `reviewed_sha` khi đo. Tree của base là `0cc14e79cecd2ce44bc4dc6cff92cadb31fd7ee4`. Diff cây làm việc và index rỗng ở đầu lượt. Có mục ignored `.codex/` sẵn.
- Lease #1525 r36/g1 khai và áp lớp `sensitive`, hiệu lực đến 2026-11-27 00:18 UTC. Đây là lời gọi 37/37 theo lease, sau 36 lời gọi đã tính. Blob đặc tả là `4672234a8cd8f3492b46295a555f4521ce5d24ce`, SHA-256 `3b067374981778df6597344cf6af9746c106b7ec8ff17727552ecab54bc0c8ee`. Hash spec trong 37/37 lease khớp blob tương ứng. Bia mộ `thay_the_cho` và `da_bi_thay_the` khớp cả hai chiều ở 36/36 chuyển tiếp, từ #1514 r9 qua #1525 r1 đến r36. [Đặc tả r36](../ops/specs/llm-khoan-docx-r36.md) · [Lease r36](../ops/leases/llm-khoan-docx-r36-g1-claude.yaml)
- Write set có 192 đường dẫn. SHA-256 của danh sách sắp xếp theo LF là `e5d58ae1f4bd37bfa8050e9882495c783d0fae5de727dd92fc0a36ce0d091c6a`. Bản vá r36 khớp 14/14 đường dẫn. Diff packet từ `fcb12b3873c3bec2c339029136243ed2c804ce05` khớp 188/188 sau khi loại bốn hồ sơ #1514 theo prompt. Toàn PR có 236 đường dẫn, gồm 48 đường ngoài phạm vi #1525 thuộc #1514 theo mốc diff. SHA-256 của `git diff --binary <mốc> HEAD` lần lượt là `e196642beaac5ae608cf051bd414f0063268f44fec4476f87927c78b4ebcef8c` (lượt 35), `1172ac086262e23b21382a96f18b930cb434eb7c9acc7888b7086a1fd1ac5cbf` (#1514 r9), `3599799159e4f68fd63ed617525e389a77f5ba0e6224a9c451110c2043c783d0` (base).
- Executor theo lease là `claude / claude_code / machine/local`, hồ sơ quyền đứng ghi phiên `session_015GtxrZQYT3Vt8PJdXrjEKg`. Reviewer là `openai_codex / codex_cli / machine` trong checkout và context độc lập. Launcher run `1742c9fbfcc042afa9a654dd9c0fb30d` chỉ đúng workspace và HEAD. SHA-256 prompt `8566a77b01963a7c42751f6a74c558b592637295ac82bb5f5ef7280b341300e6` và checkpoint `9930e638111b870dac1df09f830107ba80ff50838543902e3b003d9b5935ab4e` khớp metadata. Sandbox `workspace-write`, mạng hạn chế theo cấu hình phiên. Model và effort phục vụ `KHONG_DO_DUOC` từ metadata phục vụ của run. Trạng thái terminal và hash stdout do launcher chốt sau khi lượt này kết thúc. [Run](../../run/1742c9fb/run.json) · [Protocol §8.1–§8.2](../docs/PROTOCOL_DA_PHIEN.md#L770)

## Đối chiếu lượt 35 và đặc tả r36

Lượt 35 trên `8b6782620a6a365d7e5c890481d19a0077609f2e` bị ngắt. Hai lớp P2 và hint trong bản tạm là đầu vào đối chiếu. [Ghi chú lượt 35](../ops/acceptance/llm-khoan-docx/r1/review-35-codex/GHI_CHU.md) · [Verdict tạm lượt 35](../ops/acceptance/llm-khoan-docx/r1/review-35-codex/VERDICT.md)

| Mục | Trạng thái | Bằng chứng |
| --- | --- | --- |
| `ranh-gioi-khoan` · §2.3, §2.28–§2.38 | **VÁ MỘT PHẦN** | Danh sách cho phép đã khóa dấu đầu dòng, nhãn có dấu chấm tiền tố và dấu nối ngoài tập. Quyết định r36 bỏ tokenizer theo hint r35 và xét cùng một lớp đầu dòng cho hai nguồn. Nhãn điểm thập phân trùng ngữ pháp số khoản vẫn qua khi dãy số và thân thỏa các chốt. Xem finding. [Đầu dòng](../scripts/tl_core/llm_route.py#L579) · [Ca](../scripts/tl_core/llm_route_test.py#L1926) |
| `can-tai-nguyen-doc-nguon` · §2.37–§2.38 | **VÁ MỘT PHẦN** | Các chốt đọc byte, số quá dài trên LF thường, sâu/số nút XML, cú pháp `lvlText` trước mở rộng và tổng đúng biên đã có. Cách dùng cache style, phạm vi dòng của tiền kiểm và thời điểm áp trần vẫn còn khe so với đề xuất chốt tại biên đọc của lượt 35. Xem finding. [Tiền kiểm](../scripts/tl_core/llm_route.py#L559) · [Parser](../scripts/tl_core/llm_route.py#L625) · [Style](../scripts/tl_core/llm_route.py#L1018) |
| `ranh-gioi-ky-tu` · §2.16–§2.21, §2.37 | **ĐÃ VÁ THẬT** trong miền đã chốt | Cờ tính trên chữ hiệu lực trước gộp trắng. Mọi đoạn đều bị kiểm trước chọn tiêu đề và bỏ đoạn rỗng. Ca ba vị trí trắng ngoài miền và hai đối chứng đã chạy. Nguồn thô kiểm ký tự trước tách dòng, giữ hợp đồng một BOM. U2 giữ theo quyết định về bộ đọc chung. [DOCX](../scripts/tl_core/llm_route.py#L1320) · [Ca](../scripts/tl_core/llm_route_test.py#L1991) |
| §1, §2.2–§2.3 · K1 #1514 | **ĐÃ VÁ THẬT** đối với hai hành vi ghép gốc | Dòng điểm mang dấu chữ/bullet đứng riêng bị chặn. Dòng tiếp mở bằng “là” ở nguồn có số là dòng không số nên không ghép. Ở nguồn mất số, từ nối đầu dòng cho vế thuật ngữ rỗng nên không đạt phép so. Ca Điều 3 và ba đầu ra lưu 8/8 giữ nguyên. `can_nguoi_duyet: true`, hai giá trị `pham_vi_kiem` và đường gọi model giữ nguyên. [K1 gốc](../ops/acceptance/llm-ranh-gioi-khoan/r1/review-10-codex/VERDICT.md#L35) · [Tách](../scripts/tl_core/llm_route.py#L1518) · [So](../scripts/tl_core/llm_route.py#L1685) · [JSON](../scripts/tl_core/ops_misc.py#L3136) |
| §2.1, §2.4–§2.18 · Vùng Điều, câu dẫn, điểm gõ tay | **ĐÃ VÁ THẬT** theo hợp đồng r7. Cắt vùng, đếm trong bảng và nhận điểm gõ tay **HẾT ĐỐI TƯỢNG** | Đoạn nội dung đầu tiên phải là tiêu đề đầy đủ và đúng Điều, không đánh số, ngắt mềm hay phần tử lạ. Vùng đi đến hết tệp, chặn tiêu đề thứ hai trong miền quy định và chặn bảng/khối lạ. Trước khoản đầu chỉ có một câu dẫn chuẩn hoặc vắng. Đoạn có chữ, không đánh số sau khoản đầu bị từ chối. [Vùng](../scripts/tl_core/llm_route.py#L1400) · [Điểm](../scripts/tl_core/llm_route.py#L1463) · [Câu dẫn](../scripts/tl_core/llm_route.py#L1498) |
| §2.4–§2.18, §2.22–§2.26 · Số Word | **ĐÃ VÁ THẬT** với các biểu hiện lịch sử trong miền hỗ trợ | `start` vắng mặc định 0; `startOverride` thay giá trị cấp. Bộ đếm tách theo `numId`, xóa đếm cấp con khi cha tăng, chặn thiếu tổ tiên. Cấp khoản phải decimal với nhãn của chính cấp, liên tục từ 1. Danh sách khác, lỗi kiểu, override ngoài miền và metadata đơn trị trùng đều bị từ chối. Ca dương đo override khác gốc, reset và chữ lặp sau Z. [Định nghĩa](../scripts/tl_core/llm_route.py#L860) · [Bộ đếm](../scripts/tl_core/llm_route.py#L1383) · [Ca dương](../scripts/tl_core/llm_route_test.py#L1351) |
| §2.5–§2.13, §2.23–§2.29, §2.32–§2.35 · Markup, style và phép so | **ĐÃ VÁ THẬT** với các biểu hiện lịch sử của đường cấu trúc | Xử lý bỏ chữ theo XML gốc, gạch đơn/kép và style hiệu lực, dấu đoạn, `xml:space`, move và khoảng trắng trong mẩu đã bỏ. Nhận diện ID style theo bảng loại. Phép so đếm khoản, so thứ tự, tìm từ nối trong đoạn mở khoản và so trọn hai vế. Không thấy r36 đảo các chốt nội dung đó. [Style](../scripts/tl_core/llm_route.py#L961) · [Markup](../scripts/tl_core/llm_route.py#L1180) · [Phép so](../scripts/tl_core/llm_route.py#L1685) |
| §2.7 D1, §2.9 · `KhongCauTruc` | **ĐÃ VÁ THẬT** | DOCX thiếu đánh số tự động ném `ValueError`. CLI trả rc 2 trong nhánh DOCX, không chuyển sang đọc UTF-8. [Chốt](../scripts/tl_core/llm_route.py#L1447) · [CLI](../scripts/tl_core/ops_misc.py#L3037) |
| §2.21 U2, §2.22 V1/V3, §2.23 W1–W3 · Đường số hiệu | **ĐẠT trong phạm vi đã chốt** | `--markup-strict`, mã thoát extract và cảnh báo trần export được xét trước model. Ký tự đã mất ở bộ đọc chung, cắt Điều theo regex, gạch qua style, strict chặn bản sạch và XML→chữ bỏ tab/ngắt nằm trong giới hạn đã duyệt. Hai finding hiện tại ở các bước sau bộ đọc hoặc cùng có trên đường tệp cục bộ. [Adapter](../scripts/tl_core/llm_route.py#L1790) · [Giới hạn](../docs/GOI_AGENT_DA_NEN.md#L405) |
| §3, §2.38 · Ca và đột biến | **ĐẠT các phép đã viết**, **VÁ MỘT PHẦN về độ phủ** | Harness xác nhận neo duy nhất và chỉ tính `TinHieuChotCa` ở ca đích trên bản tạm. Bảng r36 chưa khóa độc lập va chạm nhãn số, cách tiền kiểm phân dòng, đầu đọc byte, phân giải chuỗi style hoặc thời điểm chặn tổng chữ đã dựng. Ca CLI số 5 chữ số dùng tệp LF, model giả. [Bảng](../scripts/tl_core/llm_route_test.py#L2020) · [Harness](../scripts/tl_core/llm_route_test.py#L2391) · [CLI](../scripts/tl_selftest.py#L32348) |

### Đối chiếu lịch sử #1525

Trạng thái dưới đây áp cho biểu hiện gốc. Các lớp còn mở được đánh giá theo toàn miền ở phần sau. Đối chiếu mã trên r36, các điều khoản thay thế, bảng ca/đột biến và hồ sơ từng lượt. [Hồ sơ lượt 1–35](../ops/acceptance/llm-khoan-docx/r1) · [Bảng lớp lượt 34](../ops/acceptance/llm-khoan-docx/r1/review-34-codex/VERDICT.md)

| Lượt / SHA nguồn | Trạng thái trên r36 |
| --- | --- |
| 1 · `3d24751` | **ĐÃ VÁ THẬT** A1 phần tiêu đề/khối, A2–A4, A5 phần chỉ xác thực danh sách dùng, A7–A8. A1 phần cắt, A5 phần trước/sau Điều và A6 **HẾT ĐỐI TƯỢNG** theo r7. |
| 2 · `38c481f` | **ĐÃ VÁ THẬT** B1 phần tiêu đề nguyên đoạn, B2 phần style, B3–B8. Dò điểm cắt B1 và duyệt bảng B2 **HẾT ĐỐI TƯỢNG**. |
| 3 · `b0f3cb9` | **ĐÃ VÁ THẬT** C1 phần ngắt tiêu đề, C2 phần nhãn chữ sau Z, C3–C7. Cắt vùng C1 và đếm bảng C2 **HẾT ĐỐI TƯỢNG**. |
| 4 · `fa3a8e2` | D1 phần cắt và lùi thô **HẾT ĐỐI TƯỢNG**. **ĐÃ VÁ THẬT** D2–D4 và chốt dấu phân cách của D6. D5 có chẩn đoán và giới hạn Strict công bố. |
| 5 · `3c1e143` | **ĐÃ VÁ THẬT** E2, E5 và biểu hiện E6. E1, E3, E4 **HẾT ĐỐI TƯỢNG**. |
| 6 · `6781d11` | F1 **HẾT ĐỐI TƯỢNG**. **ĐÃ VÁ THẬT** F2–F6 ở biểu hiện gốc, gồm chốt số thứ tự 999, thêm dạng tab và mốc move cân. |
| 7 · `4badb3d` | **ĐÃ VÁ THẬT** G1–G2, G4–G6. G3 **HẾT ĐỐI TƯỢNG** vì cấp thiếu tổ tiên bị chặn. |
| 8 · `6d28f34` | **ĐÃ VÁ THẬT** H1–H5, trọng tâm là tiêu đề, quan hệ part, ID lỗi và chữ hiệu lực sau ngắt. |
| 9 · `4c647c8` | **ĐÃ VÁ THẬT** J1–J5, gồm chặn phần tử `mc:` cả part và cấm chữ trần trong nhãn. |
| 10 · `674a28c` | **ĐÃ VÁ THẬT** K1–K4 của #1525. |
| 11 · `e1ed11f` | **ĐÃ VÁ THẬT** L1–L6. Tiền tố r14 phủ L2, XML part chính vẫn đưa bytes cho parser. |
| 12 · `f305663` | **ĐÃ VÁ THẬT** M1–M2 với bản chiếu riêng cho tiền tố và chẩn đoán tham số vắng/lỗi. |
| 13 · `069b734` | **ĐÃ VÁ THẬT** N1–N3, gồm chuẩn hóa ID theo chuỗi và QName đầy đủ. |
| 14 · `0447395` | **ĐÃ VÁ THẬT** Q1–Q2. Giữ chốt ký tự gốc và hướng dẫn giữ nguyên chữ dẫn chiếu. |
| 15 · `b5cff42` | **ĐÃ VÁ THẬT** R1–R3. R35 bổ sung chốt ký tự trước tiêu đề. |
| 16 · `7a913aa` | **ĐÃ VÁ THẬT** S1–S3 trong miền chữ hiệu lực và marker quyền chỉnh sửa. |
| 17 · `8f31901` | **ĐÃ VÁ THẬT** T1–T2 trong phạm vi packet. Chuẩn hóa trước biên ở extract thuộc U2. |
| 18 · `5ed4386` | **ĐÃ VÁ THẬT** U1. U2 là giới hạn đường số hiệu đã duyệt. |
| 19 · `7c4abd7` | **ĐÃ VÁ THẬT** V1–V2 và nhãn chữ có dấu chấm của V4. V3 là giới hạn đường số hiệu đã duyệt. |
| 20 · `8a685fe` | **ĐÃ VÁ THẬT** W2 DOCX và biểu hiện gốc W4–W5. W1, W3 và W2 đường số hiệu là giới hạn đã duyệt. |
| 21 · `3d21bd1` | **ĐÃ VÁ THẬT** X1–X3 ở biểu hiện gốc, kể cả nhãn chữ kết gạch ngoài tập. |
| 22 · `fbddd47` | **ĐÃ VÁ THẬT** Y1–Y3 ở biểu hiện gốc, gồm trường đơn trị và nhãn nhiều cấp. |
| 23 · `30e3e07` | **ĐÃ VÁ THẬT** Z1–Z4 ở biểu hiện gốc. |
| 24 · `b755fef` | **ĐÃ VÁ THẬT** A1–A2 ở biểu hiện gốc. |
| 25 · `659d9f2` | **ĐÃ VÁ THẬT** B2–B3 và nhãn ghép được ghi ở B1. Lớp B1 **VÁ MỘT PHẦN**. |
| 26 · `475fee9` | **ĐÃ VÁ THẬT** C1–C2 ở biểu hiện gốc. Lớp C1 **VÁ MỘT PHẦN**. |
| 27 · `9972282` | **ĐÃ VÁ THẬT** D1 ở nhãn ghép gốc. Các đối chứng bị thu hẹp có chủ đích ở §2.38. Lớp D1 **VÁ MỘT PHẦN**. |
| 28 · `0e1c112` | **ĐÃ VÁ THẬT** E1 ở dấu mở gốc. Lớp E1 **VÁ MỘT PHẦN**. |
| 29 · `291919e` | **ĐÃ VÁ THẬT** F1 nhãn nhiều dấu và F2 style vắng. Lớp F1 **VÁ MỘT PHẦN**. |
| 30 · `749e6ac` | **ĐÃ VÁ THẬT** G1 và G2 ở biểu hiện gốc. Lớp G2 **VÁ MỘT PHẦN**. |
| 31 · `7e9cde7` | **ĐÃ VÁ THẬT** H1–H3 ở biểu hiện gốc. Lớp H2 **VÁ MỘT PHẦN**. |
| 32 · `571e83f` | **ĐÃ VÁ THẬT** I1 và phần ghép chữ có dấu kết của I2. Lớp I2 **VÁ MỘT PHẦN**. |
| 33 · `3278bfe` | **ĐÃ VÁ THẬT** J1 ở nhãn ghép có dấu kết và J2 ở regex đã bỏ. Hai lớp nguyên nhân **VÁ MỘT PHẦN**. |
| 34 · `a3ef89a` | **ĐÃ VÁ THẬT** ranh giới ký tự trong hợp đồng. Ranh giới khoản và tài nguyên đọc **VÁ MỘT PHẦN**. |
| 35 · `8b67826` | Ranh giới ký tự giữ **ĐÃ VÁ THẬT**. Hai lớp còn mở **VÁ MỘT PHẦN**, xem đối chiếu và finding. |

Với #1514 r9, các chốt tiêu đề/câu dẫn, dấu kết, số nội dòng, thứ tự và trọn hai vế còn trong ca có sẵn. G1/H1/J1/K1 về ghép dòng được thay bằng hợp đồng một dòng. A4 vẫn 8/8 trên ba bản lưu. B1 thuộc bằng chứng launcher. D2 và số ở cuối dòng của C2 thuộc giới hạn đã công bố. [Verdict #1514 lượt 10](../ops/acceptance/llm-ranh-gioi-khoan/r1/review-10-codex/VERDICT.md) · [Đặc tả #1514 r9](../ops/specs/llm-ranh-gioi-khoan-r9.md)

## Findings THEO LỚP

| Lớp | Nguồn lịch sử | Hạng còn mở | Biểu hiện |
| --- | --- | --- | --- |
| `ranh-gioi-khoan` | K1 #1514, V4–J1 #1525, lớp lượt 34 và lượt 35 | P2 | Số khoản và nhãn điểm thập phân có hình dạng trùng nhau. Kiểm chữ đầu dòng cũng dùng miền ASCII+đ cho nhánh đặc tả gọi là ASCII. |
| `can-tai-nguyen-doc-nguon` | E6/F4, J2 #1525, lớp lượt 34 và lượt 35 | P2 | Tiền kiểm thô có đường đi vòng, xử lý ZIP/style vẫn đi trước các chốt tương ứng, tổng dựng chỉ chặn hết ở bước cuối. |

### Lớp `ranh-gioi-khoan` [P2] — `scripts/tl_core/llm_route.py:579–606,1548–1576`

- **Bất biến.** Mỗi dòng được nhận là khoản phải có căn cứ phân biệt với điểm hoặc dòng tiếp trong miền đã công bố. Nếu hai vai trò cùng cho một chuỗi, chốt phải từ chối hoặc hợp đồng phải giao rõ trường hợp ấy cho bước duyệt ranh giới.
- **Miền.** `_chu_cai` chỉ sinh A–Z/a–z lặp cùng chữ, `_nhan` ghép placeholder đó hoặc số thập phân với dấu `lvlText`; bullet được quy về gạch. Các từ có chữ ngoài ASCII+đ thực sự không thể là toàn bộ nhãn theo ngữ pháp này. Một nhãn chữ đứng trước từ có dấu trong cùng dải chữ rơi vào giới hạn dính thân. Nhãn ghép chữ không dấu đứng trước đệm và một chữ cái rơi vào giới hạn chỉ ngăn bằng khoảng trắng. Dấu đầu dòng, chấm tiền tố, nhãn nhiều dấu/số và mọi chữ số còn lại sau khi bóc số khoản làm điều kiện từ đầu thất bại. Các dạng `Tp.`, `e-mail`, `A1`, `1. A là`, `ASEAN (` bị chặn theo quyết định. Dấu nháy đơn cong có thể qua điều kiện đầu dòng nhưng vẫn chịu chốt ngoặc/trích dẫn cũ.
- **Biểu hiện còn mở.** `_nhan` cũng dựng được nhãn **điểm cấp con kiểu decimal** chỉ gồm số cấp đó với dấu chấm, ngoặc đóng hoặc cặp ngoặc. Ba hình dạng ấy trùng toàn bộ nhóm số khoản của `_RE_SO_DAU`. Sau khi nhóm này nuốt nhãn, cả hai nhánh từ đầu đều có thể nhận thân. `tach_khoan` chỉ kiểm dãy số liên tục và cú pháp của phần chữ còn lại. Nó không còn dấu nào để biết dấu chấm/ngoặc vốn thuộc nhãn điểm. Khi dãy phẳng vẫn bắt đầu từ 1 và liên tục, điểm có thể trở thành khoản riêng; `lech_nguyen_van` có thể chấp nhận đầu ra khớp chính phân đoạn đó. Ở đây nhãn có dấu phân cách hữu hình với thân nên hai giới hạn đã khai chưa bao quát. Cơ chế chung áp ở `--tep` UTF-8 và sau `extract`. Nhánh (b) còn cho qua dải gồm ASCII và `đ/Đ` nếu dải đạt điều kiện dài, khác chữ lặp và có từ sau. Theo đặc tả (a) dải này thuộc bảng placeholder, còn (b) yêu cầu ASCII. `_nhan` thực tế không sinh `đ/Đ`, nên sai khác nhánh (b) tự nó chưa chứng minh nhận nhầm điểm. [Bộ dựng nhãn](../scripts/tl_core/llm_route.py#L1049) · [Cửa nhận](../scripts/tl_core/llm_route.py#L585) · [Hợp đồng](../ops/specs/llm-khoan-docx-r36.md#L442)
- **Hạng P2.** Đây là sai ranh giới ở đường thô, cần bố cục đã mất cấp, số trùng cả thứ tự, thân qua chốt cú pháp và kết quả model khớp phân đoạn. `pham_vi_kiem` vẫn báo ranh giới thô và đòi người duyệt. Tác động cùng loại K1 và H2. [K1](../ops/acceptance/llm-ranh-gioi-khoan/r1/review-10-codex/VERDICT.md#L35) · [H2](../ops/acceptance/llm-khoan-docx/r1/review-31-codex/VERDICT.md#L76) · [ADR-0060 M1](../docs/adr/0060-dieu-kien-merge-va-moc-ready.md#L32)
- **Hint patch.** Phác thảo bằng lời. Cho `dau_dong_cho_phep` trả vai trò và span duy nhất, gồm trường hợp “số khoản hoặc nhãn điểm thập phân”. `tach_khoan` dùng chính span đã phân loại để kiểm thân và ngoặc, chung cho hai nguồn. Xác định tập chữ placeholder từ miền thật của `_chu_cai`, hoặc kiểm ASCII tường minh ở nhánh (b) nếu giữ bảng rộng hơn trong (a). Ở trường hợp vai trò trùng, dùng cấu trúc danh sách đã xác minh nếu có. Khi chỉ còn chữ thô, từ chối xác minh ranh giới có số nếu mục tiêu là đóng toàn miền. Nếu chủ kho giữ tương thích nguồn có số, bổ sung giới hạn dưới đây vào đặc tả, hướng dẫn và kết quả thô. Cả hai cách xử lý tại một quyết định chung cho mọi hình dạng nhãn số.
- **Hint test.** Dùng cùng nhóm ca qua hai đường thô với ba dạng số, cả hai nhánh từ đầu, thứ tự số liên tục/đứt và đối chứng nhãn chữ dính thân hoặc chỉ có đệm. Giữ ca dương DOCX gắn cấp, ca không số và các dạng bị chặn có chủ đích. Nếu chốt dừng ở vùng giao, mutant biến “mơ hồ” thành khoản phải làm đỏ ca đích. Nếu hợp đồng giữ vùng giao để người duyệt, khóa tín hiệu đầu ra về giới hạn đó. Kiểm riêng ranh giới ASCII và `đ/Đ` theo quyết định ở trên.
- **Giới hạn nếu giữ nguồn thô có số.** “Trên văn bản thô, nhãn điểm thập phân cùng dạng `N.`, `N)` hoặc `(N)` với số khoản có thể trùng một dãy khoản liên tục. Phép so chữ dựa trên phân đoạn đó. Duyệt ranh giới theo tài liệu gốc hoặc dùng DOCX còn cấp danh sách.”

### Lớp `can-tai-nguyen-doc-nguon` [P2] — `scripts/tl_core/llm_route.py:559,1018–1046,1335–1345,1441–1489`

- **Bất biến.** Mọi nguồn vượt ngân sách đã công bố phải dừng với lỗi nguồn có kiểm soát trước model và trước công việc đọc, giải style, mở rộng nhãn hay tạo bản dựng có thể vượt ngân sách.
- **Thô.** `--tep` đã giới hạn số byte thực đọc và ca LF có số 5 chữ số đã có chốt CLI. `vuot_ngan_sach` hiện tách bằng LF, trong khi `tach_khoan` dùng `splitlines` và miền ký tự chấp nhận CR. Số quá 4 chữ số ngay sau CR đơn lẻ lọt tiền kiểm trên tệp. BOM đơn ở đầu dòng số đầu tiên cũng làm regex không khớp tại CLI, vì BOM chỉ được gỡ khi kiểm ký tự hoặc khi `tach_khoan` chạy sau model. Cả hai trường hợp trên tệp có thể gọi model rồi mới báo lệch thay vì rc 2. Trần ký tự của CLI còn đo sau khi strip biên tệp, nên số ký tự gốc và số ký tự đã đo có thể khác nhau trong phạm vi trần byte. Với đường số hiệu, `capture_output=True` nạp stdout/stderr trước khi tiền kiểm. Chốt CAP của nguồn export và trần văn bản sau nhận vẫn chạy như đã công bố. [Tiền kiểm](../scripts/tl_core/llm_route.py#L559) · [Tách dòng](../scripts/tl_core/llm_route.py#L1532) · [Đọc byte](../scripts/tl_core/ops_misc.py#L3057) · [Extract](../scripts/tl_core/llm_route.py#L1790)
- **DOCX.** `XMLPullParser` áp giới hạn sâu/số nút theo khối. `read_member_bounded` đặt trần cho từng part. Khi mở gói, `ZipFile` đã nạp thư mục trung tâm trước kiểm tên trùng hoặc trần part, và lời gọi `namelist()` tiếp tục vật chất hóa danh sách. Cache `_dem_bat_trong_chuoi` chỉ ghi kết quả theo style gốc. Nhiều style được dùng cùng chia sẻ một chuỗi tổ tiên vẫn duyệt lại phần chung. `_theo_kieu` còn đi riêng qua chuỗi cho `numId`/cấp mỗi đoạn, kể cả khi kết quả vắng. Độ sâu cây XML không giới hạn độ sâu đồ thị `basedOn`, vì các style có thể cùng cấp XML. Công việc có thể tăng bậc hai trước chốt tổng chữ. Kiểm cú pháp/độ dài `lvlText` thô diễn ra sớm, còn nhãn mở rộng vẫn tạo chuỗi trước khi kiểm 64 ký tự. Bộ đếm chỉ chặn phía trên 999, do đó các giá trị bắt đầu âm trong cấp decimal vẫn đi qua bước dựng đến chốt độ dài nhãn. Chốt sớm 400.000 ký tự tính chữ các đoạn sau khi phân tích tất cả các đoạn, chưa tính tiêu đề/nhãn/xuống dòng. Chốt cuối đã sửa sai một ký tự của r35 nhưng chạy sau khi dựng từng khoản và từng dòng đưa model. [Mở gói](../scripts/tl_core/llm_route.py#L1335) · [Style](../scripts/tl_core/llm_route.py#L1018) · [Nhãn](../scripts/tl_core/llm_route.py#L1057) · [Tổng](../scripts/tl_core/llm_route.py#L1441)
- **Hạng P2.** Ảnh hưởng quan sát được từ luồng mã là tiêu thụ model ngoài hợp đồng hoặc vượt ngân sách xử lý cục bộ trước lỗi. Không có bằng chứng nhánh này làm một đầu ra sai vượt phép so nguyên văn. [§2.37–§2.38](../ops/specs/llm-khoan-docx-r36.md#L423) · [ADR-0060 M1](../docs/adr/0060-dieu-kien-merge-va-moc-ready.md#L32)
- **Hint patch.** Phác thảo bằng lời. Cho bộ đọc nguồn trả văn bản và kết quả tiền kiểm chuẩn hóa đúng một BOM, cùng quy tắc LF/CRLF/CR với `tach_khoan`. Đếm ký tự trước khi bỏ biên nếu trần đo chữ gốc, giới hạn byte trước giải mã, lưu riêng mã lỗi ngân sách để CLI rc 2. Ở đường extract, đặt ngưỡng ở bộ nhận stdout/stderr hoặc ghi rõ đại lượng được bộ đọc chung bảo đảm. Trên DOCX, áp trần gói và metadata trước khi nạp danh sách member, rồi dùng trần mỗi part và parser hiện có. Dùng một bộ phân giải `basedOn` lưu kết quả cho mọi hậu tố đã đi qua cho cả bốn thuộc tính, gồm kết quả vắng và phát hiện chu kỳ. Tính số ký tự nhãn theo token trước dấu nối, trừ ngân sách ngay khi thêm từng đoạn, số, nhãn và phân cách, rồi ghép đúng một lần. Giữ đối chứng đúng 400.000 ký tự.
- **Hint test.** Khóa biên byte/ký tự và biên 4 chữ số trên BOM đơn, LF/CRLF/CR, cả đường tệp và đường extract giả. Khẳng định rc 2 và số lời gọi model bằng 0 khi vượt. Với DOCX, đo số member/nút đã đọc, số cạnh style đã duyệt và số ký tự chuẩn bị thêm. Dùng ca cùng hậu tố style, số âm cấp con, nhiều đoạn nhỏ cộng nhãn, cùng đối chứng đúng/vượt một đơn vị. Mutant dời từng chốt qua khâu tương ứng hoặc bỏ lưu hậu tố phải làm đỏ riêng ca đích. Các gợi ý chưa áp và chưa chạy với fixture mới.

## Kết quả test và đột biến

Linux x86_64, Python 3.13.18, Git 2.43.0, Codex CLI 0.172.0 và Ruff 0.15.15. Git dùng `core.abbrev=7`; bytecode tắt. Các bản sao detached, cache và log ở `/tmp/wp1525-r36-review.lGsk2E`. Gói strict được đo trước khi sinh fixture. Hai selftest chạy trong bản sao riêng, với cơ chế chặn mạng mặc định của bộ test và thông tin xác thực giả. Ca LLM dùng đường giả. [Log kiểm thử](/tmp/wp1525-r36-review.lGsk2E)

| Lệnh | Phạm vi, trạng thái, rc | Bằng chứng |
| --- | --- | --- |
| `python scripts/tl_core/llm_route_test.py` | Head, `passed`, rc 0 | **64/64 ca, 257/257 đột biến**. Bảng có 160 mục `wp1525_*`, đều nằm trong 257 đạt. `llm.log`, SHA-256 `82a382050265c2ac6d12d8857f1d5df1de9464159ec61bc5aff5640244964508`. |
| `python scripts/tl.py --deterministic workflow-audit --strict --json` | Head, `passed`, rc 0 | `ok=true`, 26 card, 11 nhóm, 60 task, 194 lệnh khả dụng, 0 lỗi/cảnh báo. `workflow.log`. |
| `python scripts/tl.py --deterministic golden-test --json` | Head, hai lượt `passed`, rc 0 mỗi lượt | `ok=true`, 20/20 ca và projection ổn định cả hai lượt. Raw lượt đầu 19/20, chỉ `snapshot_age_s` đã khai volatile của `hygiene_sweep_fixture` thay đổi. Lượt sau 20/20 raw. `golden.log`, `golden-repeat.log`. |
| `python scripts/tl.py release-verify RELEASE_MANIFEST.json --strict --json` | Head, `passed`, rc 0 | `ok=true`, **187/187**, 0 thiếu/thừa/lệch, package hash khớp. `release.log`. |
| `python ops/lease_publish.py check --root . ops/leases/llm-khoan-docx-r36-g1-claude.yaml` | Head, validator cục bộ `passed`, rc 0 | “ĐĂNG ĐƯỢC” cho đúng lease #1525, base và hạn. Hai lớp GitHub đo Issue/PR và dò comment là `skipped` theo output. `lease.log`. |
| `python scripts/tl.py --selftest` | Head, `failed`, rc 1 | **1776/1790**; transport **12/12**. `r1525_llm_khai_niem_tep_docx_cau_truc` và `r380_llm_khai_niem_bien_dau_vao` đều đạt. `selftest-head.log`, SHA-256 `12437a9154dc02589d2a8830b012bf2c7df0b4d998701da54b3d1f37434fff89`. |
| `python scripts/tl.py --selftest` | Base, `failed`, rc 1 | **1775/1789**; transport **12/12**. `selftest-base.log`, SHA-256 `30b8c88c3f5a9232b8f2800a32af0d89c1bb80c687db6284904925a5251b634d`. |
| `python scripts/tl.py --deterministic determinism-audit --strict --json` | Head, `passed`, rc 0 | `ok=true`, **15/15**. `determinism.log`. |
| `python scripts/tl.py doc-claims-check --strict --json` | Head và base, `failed`, rc 2 mỗi cây | Cùng quét 131 tệp, 410 advisory và một cờ cứng `SHA_NOT_A_COMMIT` ở protocol dòng 1680. Object `9941d8af52aeede1c78ea4e232fbe9a8d5272033` thiếu trong checkout shallow, `git cat-file -t` rc 128. `claims-head.log`, `claims-base.log`. |
| `loi_ruff_ci()` từ `.claude/dev/ci_dang_ky_test.py` qua `python -B -c` | Head, pin/probe `passed`, rc 0 | `RUFF_CONTRACT 3 []`. `ruff-contract.log`. |
| `python -m ruff check --no-cache --select F scripts/tl.py` | Head và base, lệnh lint `failed`, rc 1 mỗi cây; phép đo delta theo §5 `passed` | 12 lỗi mỗi cây, hai log giống byte, delta 0. SHA-256 chung `5fe63d91f6092b479ca73219b31e3c3554a23019e5c1e35861755990b5f9513c`. |
| `git diff --check <mốc> HEAD` | Ba mốc lượt 35, #1514 r9 và base, `failed`, rc 2 mỗi mốc | Bản vá r36 thêm bản lưu verdict tạm lượt 35 có dấu cách cuối dòng và dòng trắng cuối tệp. Diff toàn PR cũng báo hồ sơ #1514. Phần `scripts`, manifest, changelog và hướng dẫn trả rc 0 khi đo từ base. `diff-check-*.log`. [Hồ sơ lượt 35](../ops/acceptance/llm-khoan-docx/r1/review-35-codex/VERDICT.md) |
| Windows exact SHA và CI/GitHub | `not_run` | M3 yêu cầu Windows vì diff mã toàn PR có dòng `encoding=` và `subprocess`. Phạm vi lượt này là Linux cục bộ. [ADR-0060 M3](../docs/adr/0060-dieu-kien-merge-va-moc-ready.md#L41) |

Tập lỗi selftest trùng byte sau sắp xếp, SHA-256 `bfd9b9eb98856effd2c8a1b4d7de523053a22b47981b7b1735c18383d9f42bab`. Gồm tám ca `r973_bootstrap_*`, năm ca `wp433_*` và `wp727_tl_gws_refresh` trong môi trường có `/tmp/.git` rỗng. Delta lỗi bằng 0. Điều kiện selftest N/N vẫn đỏ.

Harness áp đột biến có sẵn dưới thư mục tạm và chỉ ghi bị giết khi ca đích ném `TinHieuChotCa`. Các nhóm r36 đã chạy gồm danh sách đầu dòng, trần chữ số, độ sâu/số nút XML, nhãn mở rộng và tổng DOCX. Có 0 đột biến sống, 0 lỗi nạp và 0 neo không áp được. [Bảng đột biến](../scripts/tl_core/llm_route_test.py#L2020) · [Harness](../scripts/tl_core/llm_route_test.py#L2391)

Đọc lại checkout bàn giao sau nghiệm thu cho cùng HEAD/tree với preflight. Diff tracked và index vẫn rỗng. `.review/VERDICT.md` là tệp untracked duy nhất, ngoài mục ignored `.codex/` sẵn có. Fixture/cache phát sinh nằm trong các bản sao ngoài checkout. Hai snapshot kiểm được delta tại đầu và cuối lượt.

## Không đo được

- Các đường lỗi còn mở là suy luận đọc mã. Phản chứng đầu-cuối cho vai trò nhãn số, CR đơn/BOM ở số đầu tiên, đồ thị style và vị trí trần dựng cần fixture mới. Phép đo của lượt này dùng ca và đột biến sẵn có.
- Chưa xác nhận định dạng DOCX thông dụng bị chặn ngoài giới hạn đã khai. Mã đã xử lý tab/ptab, hyperlink, content control, bookmark, proof/permission/comment marker và ngắt trình bày. Các wrapper hướng chữ `w:dir` và `w:bdo` sẽ vào nhánh phần tử lạ theo ngữ pháp, nhưng chưa có mẫu Word/Google Docs sẵn có để xác nhận tần suất trong tài liệu luật hoặc chữ hiển thị. Cũng chưa đo render riêng cho các trường hợp phức tạp của move và style ẩn. [Danh sách phần tử](../scripts/tl_core/llm_route.py#L727) · [Duyệt nội dòng](../scripts/tl_core/llm_route.py#L1271)
- Model thật, LIVE, Windows, CI và provenance GitHub thuộc `not_run`. Model/effort phục vụ và receipt terminal của launcher chưa có bằng chứng trong lúc ghi tệp.

## Kết luận

**0 P0, 0 P1, 2 P2, 0 P3.** Hai lớp P2 mở từ lượt 35 vẫn mở, tỷ lệ đóng lớp 0/2. Lượt này dùng hết lời gọi đã cấp cho r36. `APPROVE` là nhãn kết luận nội dung theo ngưỡng P0/P1 của prompt. Điều kiện merge của ADR-0060 M1 chưa đạt, và các cổng đỏ hoặc chưa đo được giữ nguyên trạng thái ghi ở trên. [Protocol §8.3 và §12](../docs/PROTOCOL_DA_PHIEN.md#L812) · [ADR-0060 M1](../docs/adr/0060-dieu-kien-merge-va-moc-ready.md#L32) · [ADR-0062](../docs/adr/0062-adr-0060-mac-dinh-va-dong-bang-adr-0054.md#L12)

P2_mo: 2
VERDICT: APPROVE
