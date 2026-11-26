# Verdict packet #1525 r41 lượt 41 — Codex

reviewed_sha: 4d6495bacd8922a841ddabce50686bca54bca9cf
reviewed_tree: 07a489476b240cd234d1c1a14e679d6ae5d406af
base_sha: 64b7f2c14776d5d0e1d34a6be4725490956f5bec

## Preflight

- Checkout độc lập của `ducthangho/tra-luat`, detached, đúng HEAD/tree trên. `git merge-base 64b7f2c14776d5d0e1d34a6be4725490956f5bec HEAD` rc 0 và trả đúng base. Diff bản vá lấy từ `f63028ad85b3ba4a37b10c0d9f6795eba78690e8`. Diff toàn PR lấy từ `695916ea3bfffdd7b2e8fcb94b0740b3c421fe70`, phía master của merge `8afb0c7`. Ref tracking trong bản giao được seed tại HEAD. Tình trạng ref phía máy chủ theo assignment offline. [Prompt đóng băng](../../run/b5dfd4d1/prompt.snapshot)
- #1525 r41/g1, `sensitive`, lời gọi **42/45** theo lease và assignment. Lease còn hạn tới `2026-11-27T03:29:00Z`. Spec SHA-256 `292d5e157e6b711edcb1bd26dabd4945a6267777e9ddf8fe10775c73f22cece2`. Write set **217 path**, SHA-256 `ee9dd5635781cd7694bd34a6cbe09fa307552934a185f9c3d3c100a6739061f1`. **12/12** path của bản vá thuộc lease. Toàn PR có **261** path, **213** thuộc lease, **48** là hồ sơ, lease và spec của #1514 kế thừa. Kiểm `thay_the_cho` và `da_bi_thay_the` xác nhận **41/41** cặp bia mộ #1514 r9 → #1525 r1 → r41, cùng **42/42** spec hash. [Lease r41](../ops/leases/llm-khoan-docx-r41-g1-claude.yaml) · [Đặc tả r41](../ops/specs/llm-khoan-docx-r41.md)
- Executor theo assignment là `claude / claude_code / machine/local`. Reviewer `openai_codex / codex_cli / machine`, run `b5dfd4d13a2b4c44b5d749f8d1ff0cda`. SHA-256 prompt `4457013727f1671f2b5a0e26c641273431971393e3d4ced057954b48d7a5db03` khớp hồ sơ run. Linux x86-64, Python 3.13.18, Git 2.43.0, `core.abbrev=7`, sandbox thực tế `workspace-write`, approval `never`. Các phép đo dùng bản sao Git cục bộ ngoài cây reviewer. `PYTHONDONTWRITEBYTECODE=1` khi chạy Python và `--no-cache` khi lint. [Hồ sơ launcher](../../run/b5dfd4d1/run.json) · [Protocol §8.1–8.2](../docs/PROTOCOL_DA_PHIEN.md#L770)

## Đối chiếu lượt 40 và đặc tả r41

| Mục | Trạng thái | Bằng chứng |
| --- | --- | --- |
| Lượt 40 `ranh-gioi-khoan` · §2.38–§2.43 | **ĐÃ VÁ THẬT** dấu kết ngoài nhóm đơn và `là` + đệm + dấu kết đã báo. **VÁ MỘT PHẦN** toàn lớp. | Bộ quét đi qua nháy/ngoặc cân đơn, nhận dấu kết sau nhóm, giữ các đối chứng chú thích, cụm bọc nháy và phần định nghĩa. Hai phía miền và giới hạn nhãn số trùng khóa trong `PHAM_VI_KIEM`. Ba giới hạn nhãn giữ theo quyết định chủ kho. Bộ quét vẫn dùng mô hình dấu lồng và mốc từ nối khác phép so nguyên văn. [Mã](../scripts/tl_core/llm_route.py#L587) · [Tín hiệu](../scripts/tl_core/llm_route.py#L1677) · [Ca](../scripts/tl_core/llm_route_test.py#L1945) |
| Lượt 40 `can-tai-nguyen-doc-nguon` · §2.37–§2.43 | **ĐÃ VÁ THẬT** phản chứng locator ngoài cửa sổ và join đọc. **VÁ MỘT PHẦN** toàn lớp. **VÁ SINH LỖI MỚI** ở cách tính mutant nhóm trên Windows, theo đọc mã. | Locator lấy từ `EOCD − 20` trên cùng handle trước `ZipFile`. Ca đuôi EOCD 65 535 byte dùng stub phân biệt mở gói sớm. Kiểu nén 99/member mã hóa về `ValueError`. Hai ống báo lỗi, join kẹp theo phần còn lại và POSIX giết nhóm ở các nhánh lỗi đã liệt kê. Ca Linux có cháu giữ ống. Xem những cửa biên và oracle còn hở bên dưới. [ZIP](../scripts/tl_core/llm_route.py#L1409) · [Extract](../scripts/tl_core/llm_route.py#L1961) · [Ca](../scripts/tl_core/llm_route_test.py#L2033) |
| Lượt 40 `ve-sinh-diff-ho-so-review` · §2.43 | **ĐÃ VÁ THẬT** dòng trống cuối verdict lượt 39. **VÁ MỘT PHẦN** toàn lớp. | Bản vá hiện hành qua `git diff --check f63028a HEAD`. Cổng trên toàn PR vẫn đỏ tại hai verdict đã nhận diện lượt 40. Xem finding P3. [Verdict lượt 39](../ops/acceptance/llm-khoan-docx/r1/review-39-codex/VERDICT.md) |
| #1514 K1 · §2.3, §2.38 | **ĐÃ VÁ THẬT** cả hai nhánh ghép gốc. | `tach_khoan` xét từng dòng qua allowlist và từ chối cả Điều khi gặp đầu dòng kiểu điểm của K1. Nguồn có số không có cửa nhập dòng không số mở bằng `là` vào khoản trước. Nguồn mất số được so theo từng dòng, hai vế đều phải khác rỗng. Chốt dãy 1..N, dấu kết và số nội dòng còn nguyên. [K1 gốc](../ops/acceptance/llm-ranh-gioi-khoan/r1/review-10-codex/VERDICT.md#L35) · [Tách và so](../scripts/tl_core/llm_route.py#L1687) |
| §1, §2.1–§2.15 và §3 · cấu trúc, CLI, bộ đếm | **ĐÃ VÁ THẬT** các biểu hiện đã khóa trong miền hiện hành. **HẾT ĐỐI TƯỢNG** các lỗi cắt vùng, đếm trong bảng và điểm gõ tay sau r7. | DOCX chọn theo chữ ký, cần `--dieu` và nguồn duy nhất. Tiêu đề đầu phải hợp lệ, phần sau đọc tới EOF, tiêu đề khác/bảng/khối lạ bị chặn. Bộ đếm riêng theo `numId`, áp `start` (mặc định 0) và `startOverride`, bỏ bộ đếm cấp con khi cấp cha tăng, chặn nhảy cấp/sai cấp/sai danh sách/số khoản ngoài 1..N. Chỉ chấp nhận câu dẫn trọn dòng trước khoản đầu. DOCX không có auto numbering dừng rc 2 theo §2.7, không còn `KhongCauTruc`. So nguyên văn trên vị trí, số và hai vế trọn khoản, từ nối DOCX chỉ dò ở đoạn đầu khoản. `can_nguoi_duyet` luôn true. [Định nghĩa số](../scripts/tl_core/llm_route.py#L940) · [Vùng và bộ đếm](../scripts/tl_core/llm_route.py#L1522) · [CLI](../scripts/tl_core/ops_misc.py#L3027) |
| §2.16–§2.26 · chữ gốc, markup, cấu trúc part và đường số hiệu | **ĐÃ VÁ THẬT** các biểu hiện đã khóa. U2, V3, W1, W3 và phần số hiệu W2 giữ theo giới hạn đã công bố. | Chốt ký tự chạy trước khi bỏ đoạn rỗng; tên part theo quan hệ, trường đơn trị và tên member trùng bị chặn. Bộ đọc XML gốc loại gạch đơn/kép, `del`/`moveFrom`, giữ riêng mẩu chỉ có khoảng trắng. Lệch mốc move, sửa dấu đoạn hoặc nhánh `mc:` bị chặn. Số hiệu giữ `--markup-strict`, CAP, `--config` và `--profile`. [Markup](../scripts/tl_core/llm_route.py#L1264) · [XML gốc](../scripts/tl_core/llm_route.py#L1483) · [Extract](../scripts/tl_core/llm_route.py#L2031) |
| §2.27–§2.37 · style, chữ bỏ và chốt tài nguyên sớm | **ĐÃ VÁ THẬT** các hình dạng ca cũ, với lớp nhãn thô và ngân sách còn mở như bảng trên. | `xml:space` kế thừa và đặt lại, kể cả ruột bị bỏ; trạng thái ngắt/phần tử lạ của run chỉ ghi sau khi xét gạch. Kiểu style/ID được xác thực trước phân giải, nhớ kết quả theo chuỗi `basedOn`. Bộ quét thô đời cũ đã được thay theo §2.38. Ngân sách ký tự, số, độ sâu/nút, nhãn và tổng chữ còn ở các điểm đọc. [Style](../scripts/tl_core/llm_route.py#L1041) · [Chữ run](../scripts/tl_core/llm_route.py#L1209) · [Trần XML](../scripts/tl_core/llm_route.py#L695) |
| Lượt 39 `huong-dan-docx` và `ghi-chu-write-set` · §2.42 | **ĐÃ VÁ THẬT**, giữ trên r41. | Hướng dẫn tách `pStyle` vắng/sai loại, `rStyle` vắng/sai loại và `basedOn` vắng/sai loại. Lease r41 trỏ danh sách path đã băm để định phạm vi. [Hướng dẫn](../docs/GOI_AGENT_DA_NEN.md#L429) · [Ghi chú lease](../ops/leases/llm-khoan-docx-r41-g1-claude.yaml#L243) |

### Đối chiếu ID lịch sử

Các hàng ghi trạng thái từng nhóm ID theo hồ sơ lượt trước, phần thực thi còn hiệu lực và ca sẵn có. Hai lớp P2 giữ nguyên slug qua các lượt. [Hồ sơ lượt 1–40](../ops/acceptance/llm-khoan-docx/r1) · [Đối chiếu exact SHA lượt 40](../ops/acceptance/llm-khoan-docx/r1/review-40-codex/VERDICT.md)

| Lượt | Đối chiếu trên r41 |
| --- | --- |
| 1–3 | **ĐÃ VÁ THẬT** A1 phần tiêu đề/khối, A2–A4, A5 phần danh sách dùng, A7–A8, B1 phần tiêu đề nguyên đoạn, B2 phần style, B3–B8, C1 phần ngắt, C2 phần nhãn sau Z, C3–C7. **HẾT ĐỐI TƯỢNG** A1/B1/C1 phần điểm cắt, A5 phần ngoài Điều, A6 và B2/C2 phần bảng. |
| 4–6 | **HẾT ĐỐI TƯỢNG** D1 phần điểm cắt, E1/E3/E4 và F1 theo r7. **ĐÃ VÁ THẬT** D1 phần bỏ fallback, D2–D4, D6, E2/E5/E6, F2–F6. D5 là giới hạn Strict có chẩn đoán. |
| 7–9 | **ĐÃ VÁ THẬT** G1/G2/G4–G6, H1–H5 và J1–J5, với J2 được thay bằng chốt `mc:` toàn part tại §2.13. **HẾT ĐỐI TƯỢNG** G3 vì nhảy cấp bị chặn. |
| 10–12 | **ĐÃ VÁ THẬT** K1–K4 của #1525, L1–L6, M1–M2 theo miền hiện hành. Tiền tố cấm thay hình dạng tiêu đề của L2/M1. |
| 13–15 | **ĐÃ VÁ THẬT** N1–N3, Q1–Q2, R1–R3. Chữ gốc được kiểm trước khi loại đoạn rỗng, bản chiếu tiền tố phục vụ dò và không sửa chữ. |
| 16–18 | **ĐÃ VÁ THẬT** S1–S3, T1–T2 trong write set, U1. U2 là giới hạn của đường số hiệu. |
| 19–21 | **ĐÃ VÁ THẬT** V1/V2/V4, W2 DOCX, W4/W5, X1–X3 ở hình dạng đã báo. V3/W1/W3 và W2 phần số hiệu là giới hạn đã công bố. |
| 22–24 | **ĐÃ VÁ THẬT** Y1–Y3, Z1–Z4, A1–A2 ở hình dạng đã báo. Chốt tên ZIP trùng vẫn chạy sau tiền kiểm. |
| 25–28 | **ĐÃ VÁ THẬT** B1–B3, C1/C2, D1 và E1 ở hình dạng đã báo. Miền đối chứng đọc theo §2.38. |
| 29–33 | **ĐÃ VÁ THẬT** F1/F2, G1/G2, H1–H3, I1, I2 phần nhãn có dấu đã báo, J1 và J2. I2 phần nhãn thiếu dấu phân biệt đã công bố. |
| 34–36 | **ĐÃ VÁ THẬT** lớp `ranh-gioi-ky-tu` và các hình dạng nhãn một vế/dấu đầu dòng đã báo. Số trùng nhãn khoản thuộc giới hạn có tín hiệu. **VÁ MỘT PHẦN** hai lớp P2. |
| 37–38 | **ĐÃ VÁ THẬT** các hình dạng nhãn chữ Việt một vế, span kiểm ngoặc, số âm và trừ ngân sách trước ghép đã khóa. **VÁ MỘT PHẦN** hai lớp sau thu hẹp miền và đổi chốt tài nguyên. |
| 39–40 | Hai P3 lượt 39 và biểu hiện EOF của lượt 40 đã vá. Hai lớp P2 và lớp P3 vệ sinh toàn PR tiếp tục mở theo findings. |

Trên đường cấu trúc, đối chiếu mã và fixture hiện có chưa xác lập một cửa P1 về bỏ, gộp, cắt, tráo khoản hay nhận chữ đã bỏ ngoài các hình dạng đã khóa. Các nhóm DOCX thường được hỏi đã có cách xử lý hoặc giới hạn nêu trong §2.5 và các mục thay thế, gồm content control nội dòng/khối, hyperlink, custom XML, bookmark/comment, tab căn vị trí, dấu nối không ngắt, ngắt trang/cột, trường, hình, ký hiệu và bảng. Chưa có bằng chứng độc lập về một phần tử export Word/Google Docs phổ biến khác bị chặn ngoài giới hạn. [Đặc tả §2.5–§2.11](../ops/specs/llm-khoan-docx-r41.md#L103) · [Hướng dẫn](../docs/GOI_AGENT_DA_NEN.md#L390)

## Findings THEO LỚP

### Lớp `ranh-gioi-khoan` [P2] — [`llm_route.py:604`](../scripts/tl_core/llm_route.py#L604)

- **Bất biến.** Với cả hai nguồn thô, dấu phân biệt thuộc đầu nhãn nhìn thấy phải làm từ chối cả Điều. Điểm dừng dò nhãn phải là đúng vị trí từ nối cấp khoản mà phép so dùng.
- **Miền và bằng chứng đọc mã.** Bộ quét dùng chung cho dòng có và mất số. Các dấu kết sau cụm cân đơn, dấu kết trong nháy đầu dòng và `là` kèm đệm nhưng chưa có vế phải đã có ca khóa. Hai đường khác còn hở.
  1. **Ngoặc chứa nháy.** Nhánh mở nháy tại dòng 629 chỉ chạy nếu `sau == 0`. Sau hai từ đầu hợp lệ, một ngoặc chú thích chứa ngoặc mở **bên trong nháy cân** làm tăng độ sâu nhầm. Ngoặc đóng thật đưa bộ quét về độ sâu giả còn dương. Nó bỏ qua dấu kết, kể cả dấu chấm hay gạch có đệm, sau chỗ nhóm đã đóng. Với ngoặc đóng bên trong nháy, sai lệch diễn ra theo hướng ngược lại: bộ quét có thể coi dấu bên trong nhóm là dấu ngoài nhóm và chặn chú thích hợp lệ. `_dong_mo_ho` và `_quet` nhận nháy cả bên trong ngoặc và giữ độ sâu đúng, nên chốt cân có thể qua và phép so tìm được từ nối thật sau dấu kết. Khi model chép lại đủ hai vế của dòng đã nhận sai, nhãn có thể nằm trong thuật ngữ đã qua kiểm.
  2. **Mốc từ nối đọc theo hai ngữ pháp.** Dòng 636–641 nhận cả chữ `là` đứng sát sau một ký tự phi chữ/số, chẳng hạn ngay sau dấu phẩy hoặc nháy đóng. `_RE_LA` trong `_tu_noi` đòi đệm hoặc đầu chuỗi phía trước. Vì vậy bộ quét có thể dừng sớm ở chữ giống từ nối và bỏ qua dấu kết nhãn trước một từ nối hợp lệ xuất hiện muộn hơn. Theo chiều ngược lại, `_tu_noi` vẫn có thể chọn một `là` đứng trước dấu phân cách, hoặc trả rỗng khi gặp dấu hai chấm ngoài nhóm, trong khi bộ quét dùng quy tắc vế phải khác và tiếp tục tìm. Ngoài nhóm, gạch dính chữ được bỏ qua. Trong nháy đầu thân, nhánh dòng 615 lại coi cả gạch dính chữ là dấu kết nếu còn chữ về sau. Đây là một đường chặn oan của đối chứng gạch dính chữ nếu nó nằm trong thuật ngữ bọc nháy. [Bộ quét](../scripts/tl_core/llm_route.py#L587) · [Chốt cân và phép chọn từ nối](../scripts/tl_core/llm_route.py#L1783) · [Phép so](../scripts/tl_core/llm_route.py#L1856)
- **Hạng P2.** Dấu kết vẫn hiện diện, nên hai đường nhận sai nêu trên nằm ngoài ba giới hạn chủ kho đã khai. Sai lệch cần một phân đoạn thô có điều kiện và đầu ra khớp phân đoạn ấy. Cờ duyệt ranh giới vẫn đi kèm. Đây là cùng lớp và cùng hạng với lượt 40.
- **Hint patch.** Cho `_quet` cung cấp cùng trạng thái ngoặc/nháy và vị trí mở/đóng cho `_dong_mo_ho`, `_mo_dau_nhieu_ve` và `_tu_noi`. Dùng một quyết định từ nối cho thân thô từ chốt đầu dòng tới phép so, giữ quy tắc phạm vi đoạn đầu ở DOCX. Bộ phân loại nhãn dùng một hàm quyết dấu kết (gạch chỉ tính trước đệm/dấu mở), cộng điều kiện về nhóm bắt đầu thân. Theo dõi dấu lẻ trong nháy đầu bằng trạng thái cục bộ của chính nháy đó. Quy tắc này phủ dấu trực tiếp, dấu trước/sau cụm cân, các lớp lồng và chữ giống từ nối kề dấu mà không cần đếm số vế.
  ```text
  than = span_sau_so_khoan
  trang_thai = quet_dau(than)
  moc = tim_tu_noi_cap_khoan(than, trang_thai, quy_tac_tho)
  nhan = co_dau_ket_nhan(than, trang_thai, truoc=moc)
  # lech_nguyen_van dùng cùng moc trên chính span thân thô.
  ```
- **Hint test.** Ca âm cho dấu kết sau nhóm, ngoặc chứa nháy có ngoặc mở/đóng, nháy chứa ngoặc, chữ giống từ nối sát dấu trước và nhãn trước từ nối thật. Ca dương cho chú thích có hai kiểu lồng, gạch dính chữ trong/ngoài nháy, dấu câu sau từ nối thật, thân có và mất số. Khóa cả dấu chấm, gạch cách đệm và ngoặc đóng đầu thân. Đột biến bỏ chuyển trạng thái nháy bên trong ngoặc, nới biên trái của từ nối hoặc bỏ điều kiện bên phải của gạch phải làm đỏ ca tương ứng. Giữ các assertion hai phía của `pham_vi_kiem`.
- **Giao miền.** Ba giới hạn hiện hành đủ cho phần không phân biệt được bằng hình dạng. Nếu chủ kho muốn nhận đầu thân có dấu kết nhìn thấy trước từ nối, phải ghi cụ thể miền bổ sung vào đặc tả và tín hiệu đầu ra.

### Lớp `can-tai-nguyen-doc-nguon` [P2] — [`llm_route.py:1431`](../scripts/tl_core/llm_route.py#L1431), [`llm_route.py:1990`](../scripts/tl_core/llm_route.py#L1990)

- **Bất biến.** Chốt tài nguyên chạy trước bước cấp phát hoặc trước khi bắt đầu chờ. Lỗi đọc nguồn qua CLI phải có chẩn đoán và vòng đời tiến trình/luồng phải được thu hồi trong ngân sách đã khai. Oracle phải xác nhận chốt đặc thù nền đã thực sự chạy.
- **Miền và bằng chứng.**
  1. **DOCX, từ tiền kiểm tới mở/đọc member.** Chốt locator EOCD tuyệt đối đã có đối chứng. Lớp ngoại lệ mới bắt được lỗi mở gói do phiên bản lạ, lỗi mở member như kiểu nén chưa biết hoặc mã hóa, cùng các ngoại lệ đã liệt kê. Nó vẫn cho `lzma.LZMAError` thoát ra từ một member loại ZIP_LZMA được thư viện chuẩn nhận diện. CPython 3.13.18 có `zipfile.LZMADecompressor.decompress` giải thuộc tính bộ lọc rồi gọi bộ giải nén. `LZMAError` kế thừa trực tiếp `Exception` và vắng ở cả biên DOCX lẫn catch của CLI. ZIP dùng codec đã biết nhưng stream hỏng vì thế có thể traceback thay vì rc 2. Đây là cửa **đọc** member sau mở thành công. Ca r41 đo hai lỗi **mở** member và gộp chúng vào một mutant. [Biên mở/đọc](../scripts/tl_core/llm_route.py#L1422) · [Đọc member](../scripts/tl_core/llm_route.py#L861) · [Catch CLI](../scripts/tl_core/ops_misc.py#L3044) · [Ca ZIP](../scripts/tl_core/llm_route_test.py#L2163)
  2. **Extract, sở hữu tiến trình từ lúc spawn tới khi hoàn tất.** Bốn nhánh vượt byte/lỗi reader, reader quá hạn, `wait` quá hạn và kết quả qua hạn đều gọi `thu_hoi`; ca Linux xác nhận cháu cùng nhóm giữ ống. Sau `Popen` thành công, việc tạo và khởi động reader, kẹp chờ và `p.wait` nằm ngoài một khối thu hồi chung. Nếu khởi động luồng thứ hai lỗi, `wait` phát sinh lỗi khác timeout, hoặc CLI nhận ngắt khi chờ, luồng/ống và tiến trình đã mở chưa được thu hồi qua chốt r41. Ở POSIX, phiên riêng còn có nghĩa ngắt terminal của tiến trình gọi không tự đi tới nhóm con. `thu_hoi` cũng dừng sau join có hạn mà không kiểm hay báo reader nào chưa rời. Giới hạn giết trực tiếp trên Windows vẫn thuộc hợp đồng. [Vòng đời extract](../scripts/tl_core/llm_route.py#L1961) · [Catch CLI](../scripts/tl_core/ops_misc.py#L3095)
  3. **Oracle theo nền.** Ca cháu giữ ống chạy với `os.name != "nt"` nhưng dùng `/proc/<pid>/stat`. Mọi `OSError` được coi là đã chết. Trên POSIX không có procfs, ca dương có thể qua mà chưa xác nhận thu hồi và mutant bỏ `killpg` sống. Trên Windows ca cháu bị bỏ qua, mutant POSIX vẫn nằm trong `DOT_BIEN` và harness đòi giết mọi mutant. Linux hiện tại có procfs. Suy luận Windows/POSIX khác dựa trên các điều kiện trong mã. [Oracle hiện hành](../scripts/tl_core/llm_route_test.py#L2069) · [Mutant nhóm](../scripts/tl_core/llm_route_test.py#L2265) · [Harness](../scripts/tl_core/llm_route_test.py#L2652)
- **Hạng P2.** Các đường còn hở ảnh hưởng thoát lỗi nguồn và thu hồi, và làm suy yếu gate bắt buộc theo nền. Chưa có bằng chứng chúng xác nhận sai chữ nguyên văn.
- **Hint patch.** Dùng một biên đọc ZIP tại `doc_dieu_docx`/`_doc_thanh_phan` cho mở gói, mở member và **đọc** theo codec. Giữ thứ tự trần byte → kiểm EOCD/CD và số entry thật → mới mở gói. Tại biên member, cho phép bộ codec có ngân sách phù hợp và ánh xạ các lỗi stream/thuộc tính codec hỗ trợ về cùng `ValueError` có nguyên nhân. Giới hạn catch đúng thao tác ZIP thay cho ôm cả parser. Tại biên extract, gom quyền sở hữu tiến trình, ống và các luồng đã start vào một khối `try/finally` bao từ sau `Popen` đến khi có kết quả. Mọi lối thoát bất thường qua cùng `thu_hoi`, kể cả lỗi setup sau spawn và ngắt. Giữ deadline đọc–wait cùng ngân sách thu hồi riêng. Đóng endpoint lúc an toàn, tránh khóa ống đang được reader giữ, báo cụ thể nếu sau ngân sách vẫn còn reader. Hai biên dùng cùng hợp đồng lỗi nguồn của CLI, vì ZIP và tiến trình có điểm cấp phát khác nhau.
  ```text
  p = Popen(..., start_new_session=posix)
  luong_da_start, thanh_cong = [], False
  try:
      khoi_dong_reader_va_ghi_so(luong_da_start)
      ket_qua = doc_va_wait_trong_han(p, luong_da_start)
      thanh_cong = True
      return ket_qua
  finally:
      ket_thuc_doc(p, luong_da_start, thu_hoi=not thanh_cong)
  ```
- **Hint test.** Giữ biên đúng/vượt byte, entry, EOCD, trần XML/số và hai ống. Tách ca mở gói, mở member, lỗi đọc stream của codec được nhận và đối chứng member tốt. Dùng fake process/reader xác nhận ngắt, start lỗi một phần, wait lỗi và thoát theo deadline đều vào cùng điểm thu hồi. Tách ca nhóm POSIX khỏi ca chung. Dùng tín hiệu vòng đời/EOF có thể quan sát hoặc probe khả năng procfs thật trước khi diễn giải lỗi đọc trạng thái. Báo riêng ca không áp dụng trên Windows. Đột biến bỏ ánh xạ lỗi **đọc**, bỏ thu hồi từ lối thoát bất thường hoặc bỏ kill nhóm phải đỏ đúng ca có capability. Chạy native Windows theo ADR-0060 M3.

### Lớp `ve-sinh-diff-ho-so-review` [P3] — [verdict #1525 lượt 35](../ops/acceptance/llm-khoan-docx/r1/review-35-codex/VERDICT.md#L3)

- **Bất biến.** Diff toàn PR đạt kiểm tra khoảng trắng cho hồ sơ Markdown. Bản gốc đã có mỏ neo byte phải đối chiếu được sau chuẩn hóa.
- **Miền và bằng chứng.** Verdict lượt 39 đã bỏ đúng dòng trống thừa ở EOF, `git diff --check f63028a HEAD` rc 0. `git diff --check 695916e HEAD` vẫn rc 2, với **8 chẩn đoán**: bốn dòng có khoảng trắng cuối dòng và một dòng trống EOF ở #1525 lượt 35, ba dòng có khoảng trắng cuối dòng ở #1514 lượt 8. Loại đúng hai đường dẫn đó khỏi lệnh đối chứng cho rc 0. Hai tệp là phần tăng thêm của PR. Lỗi sổ sách có thể cản cổng, ảnh hưởng hạng P3. Tệp #1514 nằm ngoài write set r41 hiện hành. [Verdict #1514 lượt 8](../ops/acceptance/llm-ranh-gioi-khoan/r1/review-8-codex/VERDICT.md#L3) · [Cổng §12](../docs/PROTOCOL_DA_PHIEN.md#L1122)
- **Hint patch.** Chuẩn hóa ở bước nhập hồ sơ, bỏ đệm cuối từng dòng và ghi đúng một LF cuối, trước khi băm. Dọn cả hai path đã nêu trong write set successor được duyệt. Nếu tệp lịch sử có biên nhận neo byte, bảo toàn đối tượng gốc theo hash và ghi provenance của bản trình bày, hoặc đưa quyết định xử lý exact SHA vào audit. Kiểm trên diff toàn PR để bắt cả hồ sơ kế thừa từ #1514.
- **Hint test.** `git diff --check` trên mốc toàn PR phải xanh. Đối chứng bản Markdown sạch và so hash bản gốc với biên nhận nếu có. Bỏ bước chuẩn hóa hoặc đưa lại đệm cuối dòng/dòng trống EOF phải làm cổng đỏ ở đúng path.

## Kết quả test và đột biến

Các lệnh chạy trên head/tree đã neo. Selftest, doc-claims và Ruff có đối chứng ở base `64b7f2c14776d5d0e1d34a6be4725490956f5bec`, tree `0cc14e79cecd2ce44bc4dc6cff92cadb31fd7ee4`. [Log và rc từng lệnh](/tmp/wp1525-r41-review.ziiGsW)

| Lệnh | Trạng thái và rc | Bằng chứng |
| --- | --- | --- |
| `python scripts/tl_core/llm_route_test.py` | `passed`, rc 0 | **64/64** ca, **283/283** đột biến bị giết, gồm **186/186** `wp1525_*` và 11 mutant mới của r41. Harness chỉ tính khi ca đích báo `TinHieuChotCa`. Điều 3 và ba kết quả đã lưu giữ **8/8** theo assertion sẵn có. [Log](/tmp/wp1525-r41-review.ziiGsW/route.log) · [Ca 8/8](../scripts/tl_core/llm_route_test.py#L1160) |
| `python scripts/tl.py --deterministic workflow-audit --strict --json` | `passed`, rc 0 | `ok=true`, 26 card, 11 nhóm, 60 task, 194 lệnh khả dụng, **201/201** leaf đã đăng ký, 0 lỗi/cảnh báo. [Log](/tmp/wp1525-r41-review.ziiGsW/workflow.log) |
| `python scripts/tl.py --deterministic golden-test --json` | `passed`, rc 0 | `ok=true`, **20/20** ca và **20/20** projection ổn định. Raw ổn định **19/20**, `hygiene_sweep_fixture` đạt theo projection của cổng. [Log](/tmp/wp1525-r41-review.ziiGsW/golden.log) |
| `python scripts/tl.py release-verify RELEASE_MANIFEST.json --strict --json` | `passed`, rc 0 | `ok=true`, **187/187** tệp. Package hash khớp `a9bd8a27cca0b0c5eacefc4f8f4e364218f30f8b931f0143b53036ccb11467fa`. [Log](/tmp/wp1525-r41-review.ziiGsW/release.log) |
| `python ops/lease_publish.py check --root . ops/leases/llm-khoan-docx-r41-g1-claude.yaml` | `passed` cục bộ, rc 0. Hai phép GitHub `skipped` theo công cụ. | “ĐĂNG ĐƯỢC”, issue #1525, neo `64b7f2c14776`, hạn `2026-11-27T03:29:00Z`. Các phép đọc Issue/PR và dò comment được bỏ qua trong chế độ offline. [Log](/tmp/wp1525-r41-review.ziiGsW/lease.log) |
| `python scripts/tl.py --selftest` | `failed`, rc 1 trên head và base | Head **1774/1790**, base **1773/1789**, transport **12/12** ở mỗi lượt. `r1525_llm_khai_niem_tep_docx_cau_truc` và `r380_llm_khai_niem_bien_dau_vao` là `[OK]` trên head. Cùng 16 ID đỏ, delta 0. [Head](/tmp/wp1525-r41-review.ziiGsW/selftest.log) · [Base](/tmp/wp1525-r41-review.ziiGsW/base-selftest.log) |
| `python scripts/tl.py --deterministic determinism-audit --strict --json` | `passed`, rc 0 | `ok=true`, **15/15** phép kiểm. [Log](/tmp/wp1525-r41-review.ziiGsW/determinism.log) |
| `python scripts/tl.py --deterministic doc-claims-check --strict --json` | `failed`, rc 2 trên head và base | Cùng 131 tệp, 410 advisory và một cờ cứng L2 `SHA_NOT_A_COMMIT` cho `9941d8af52aeede1c78ea4e232fbe9a8d5272033`. Hai danh sách flags bằng nhau (`cmp` rc 0). Git store shallow được giao thiếu object này. [Head](/tmp/wp1525-r41-review.ziiGsW/claims.log) · [Base](/tmp/wp1525-r41-review.ziiGsW/base-claims.log) |
| Ruff pin/probe qua `loi_ruff_ci()` trong `.claude/dev/ci_dang_ky_test.py` | `passed`, rc 0 | `RUFF_CONTRACT 3 []`, 3 bước pin/probe, 0 lỗi hợp đồng. [Log](/tmp/wp1525-r41-review.ziiGsW/ruff-contract.log) |
| `python -m ruff check --no-cache --select F scripts/tl.py` · Ruff 0.15.15 | Bare lint `failed`, rc 1 trên head/base. Điều kiện **delta 0** đạt. | **12 F821** mỗi bên, output giống nhau (`cmp` rc 0). [Head](/tmp/wp1525-r41-review.ziiGsW/ruff-head.log) · [Base](/tmp/wp1525-r41-review.ziiGsW/ruff-base.log) |
| `python -m ruff check --no-cache --select F scripts/tl_core/llm_route.py scripts/tl_core/llm_route_test.py` | `passed`, rc 0 | 0 chẩn đoán trong hai tệp Python thay đổi ở r41. Phép lint mở rộng vào các module re-home trước khi xác nhận scope CLAUDE.md cho 4816 chẩn đoán, rc 1. Scope mở rộng không dùng để suy delta. [Hai tệp r41](/tmp/wp1525-r41-review.ziiGsW/ruff-route.log) · [Log thăm dò](/tmp/wp1525-r41-review.ziiGsW/ruff.log) |
| `git diff --check f63028a HEAD` | `passed`, rc 0 | Diff bản vá sạch. [Log](/tmp/wp1525-r41-review.ziiGsW/r41-diff-check.log) |
| `git diff --check 695916e HEAD` | `failed`, rc 2 | 8 chẩn đoán ở 2 hồ sơ, như lớp P3 bên trên. [Log](/tmp/wp1525-r41-review.ziiGsW/pr-diff-check.log) |

Danh sách 16 ID selftest đỏ khớp byte trên head và base (`cmp` rc 0, SHA-256 `6c344d8f8a71b854460d8d4badd425904bdd116177ea8b3e14bd2387a2a14505`). Gồm 14 ca `r973_bootstrap_*`, `wp433_*` và `wp727_tl_gws_refresh` khi sandbox có `/tmp/.git` rỗng, cộng `r226_nguong_l2_troi_theo_abbrev_va_ci_ghim` và `r268_l2_trichotomy_theo_trang_thai_object`. Hai ca sau cũng đã đỏ hai phía trong lượt 40. Gate N/N hiện vẫn đỏ. [ID head](/tmp/wp1525-r41-review.ziiGsW/head-selftest-fail.ids) · [ID base](/tmp/wp1525-r41-review.ziiGsW/base-selftest-fail.ids)

Hai phản chứng lớp tài nguyên ở lượt 40 đã có mutant trực tiếp trong bảng r41. `wp1525_zip64_cua_so_cu` khôi phục giới hạn cửa sổ và `wp1525_extract_join_khong_kep` khôi phục `join(0.05)`. Cả hai bị giết cùng mutant `wp1525_extract_khong_giet_nhom` trên Linux. Các phép đột biến đo ngay trong harness sẵn có, trên bản sao tạm của module. [Bảng đột biến](../scripts/tl_core/llm_route_test.py#L2253) · [Harness](../scripts/tl_core/llm_route_test.py#L2652)

Bản sao kiểm tra head và base có diff tracked/index rỗng sau chạy. Fixture và trạng thái bị ignore sinh trong bản sao thử nghiệm. Diff và numstat được lưu dưới scratch. SHA-256 diff PR `9f23adb0751a05d5d09965b016acb829c7a834b70dba73c8cefc6c43203b77a2`. SHA-256 diff vá r41 `c0afdcee709831c2e39908a0bd449edfdcccbd25840fafc36373280435df6ce3`. [Diff PR](/tmp/wp1525-r41-review.ziiGsW/pr.diff) · [Diff r41](/tmp/wp1525-r41-review.ziiGsW/r41.diff) · [Numstat](/tmp/wp1525-r41-review.ziiGsW/pr.numstat)

## Không đo được

- `not_run`: phép đo động cho các hình dạng mới trong findings, native Windows theo ADR-0060 M3, POSIX không có procfs, export mới từ Word/Google Docs, CI/GitHub và model thật. Findings mới neo vào đường đi trong mã và thư viện chuẩn. Không có fixture, chuỗi thử nghiệm hay script dò mới. Phạm vi doc-claims strict trên kho Git đầy đủ chưa đo được với kho object hiện có. [ADR-0060 M3](../docs/adr/0060-dieu-kien-merge-va-moc-ready.md#L44)
- Model/effort phục vụ `KHONG_DO_DUOC` từ hồ sơ launcher tại lúc ghi verdict. Rc tiến trình review và hash stdout terminal do launcher xác nhận sau khi lượt kết thúc. Verdict này báo kết quả review offline trên SHA được giao. [Hồ sơ launcher](../../run/b5dfd4d1/run.json)
- Snapshot đầu/cuối đối chiếu exact SHA/tree, diff và index. Tại cây reviewer, chỉ có .review/VERDICT.md mới và .codex/ ignored đã có từ đầu. Snapshot xác nhận delta quan sát ở hai mốc. [Protocol §8.2](../docs/PROTOCOL_DA_PHIEN.md#L797)

**CHƯA ĐỦ ĐIỀU KIỆN MERGE** do hai lớp P2, một lớp P3, cổng selftest N/N, doc-claims strict, diff check toàn PR và bằng chứng Windows/CI còn thiếu hoặc đỏ. Theo quy tắc verdict của assignment, 0 P0/P1 cho kết luận nội dung APPROVE. Theo §8.3/§12, lượt này xác nhận đóng 0/3 lớp còn mở từ lượt 40, dù các phản chứng đích cụ thể đã được vá. [ADR-0060 M1/M3/M5/M12](../docs/adr/0060-dieu-kien-merge-va-moc-ready.md#L32) · [Protocol §12](../docs/PROTOCOL_DA_PHIEN.md#L1097)

P0_mo: 0
P1_mo: 0
P2_mo: 2
P3_mo: 1
VERDICT: APPROVE
