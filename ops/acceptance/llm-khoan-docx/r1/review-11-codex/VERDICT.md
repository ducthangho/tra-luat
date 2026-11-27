# Verdict packet #1525 r11 lượt 11 — Codex

reviewed_sha: e1ed11fe536632b943c52b04a90bf549425f1bf9
reviewed_tree: ca3527460b8f9f2c3d9c8cd4f43911c2ee308326
base_sha: 64b7f2c14776d5d0e1d34a6be4725490956f5bec
base_tree: 0cc14e79cecd2ce44bc4dc6cff92cadb31fd7ee4

## Preflight

- Checkout rời của `ducthangho/tra-luat`, detached đúng SHA. Hai ref cục bộ của nhánh `ccr-89c0d2e2-inanqb` cùng trỏ SHA đó. Baseline nghiệm thu, mốc tiếp nối #1514 `fcb12b3873c3bec2c339029136243ed2c804ce05`, ứng viên lượt 10 `674a28c6c42342f9ab34651cbadea411a0d05c1d` và mốc bản vá `582cb4427e43b18f78f9edf6b766f34b0bc9cbb1` đều là tổ tiên. `git diff` và index đầu phiên rỗng. `.codex/` là đường dẫn ignored đã có trước phiên.
- Packet #1525, r11/g1, class `sensitive`, lease hết hạn 22:53 UTC ngày 25-11-2026. Lượt này dùng suất cuối, 11/11. Blob đặc tả tại exact head là `7dc4bef24817b76c9177807afbb34afd14f1d69c`. SHA-256 của blob và bản trên đĩa cùng là `e04bccacf22cd9ad385b2c1b2930a7e20c3ebee5a4296372e76b7e1c0f0626a3`, khớp lease. [Spec r11](../ops/specs/llm-khoan-docx-r11.md) · [Lease r11](../ops/leases/llm-khoan-docx-r11-g1-claude.yaml)
- Write set gồm 66 đường dẫn, SHA-256 `3299f952c8f320154f3997b9cd027f97ee31271d1e09acce2d98cc28c05d9dfe` theo quy tắc của lease. Diff từ `fcb12b3` có 66 đường dẫn. Bốn đường dẫn thuộc hồ sơ nghiệm thu #1514 được loại theo prompt, 62/62 đường dẫn còn lại thuộc lease. Diff bản vá r11 có 8/8 trong lease. Diff toàn PR có 110 đường dẫn, trong đó 48 đường dẫn ngoài lease r11 thuộc phạm vi #1514 hoặc hồ sơ #1514 đã loại. Đối chiếu `thay_the_cho` và `da_bi_thay_the` đạt 11/11 liên kết #1514 r9 ↔ #1525 r1 ↔ … ↔ r11, cùng nhánh và đầu r11 chưa có successor. Hash spec khớp 11/11 lease #1525. [Lease #1514 r9](../ops/leases/llm-ranh-gioi-khoan-r9-g1-claude.yaml) · [Lease #1525 r1](../ops/leases/llm-khoan-docx-r1-g1-claude.yaml)
- Run `abe5903027014820be084414f1cc592b` qua launcher ghi `openai_codex` / `codex_cli` / `machine`. Checkpoint, run và bytes prompt cùng neo exact SHA và SHA-256 `f849f81ec91ddf6c0286feea94ec1c6d2af8315d9a5158c006238141a80a0384`. Executor theo lease là `claude` / `claude_code` / `machine/local`. Codex CLI `0.172.0`, sandbox `workspace-write`, Linux 6.18.44-fc-v880 x86_64, Python 3.13.18, Git 2.43.0. Ghim `core.abbrev=7` ở checkout giao và các bản sao chạy test. [Protocol §8.1](../docs/PROTOCOL_DA_PHIEN.md#L770)

## Đối chiếu lượt 10 và đặc tả r11

Đọc các bổ sung theo thứ tự thay thế trong spec. Trạng thái áp cho biểu hiện đã báo trên `674a28c` và cho các ca lịch sử còn thuộc hợp đồng. [Verdict lượt 10](../ops/acceptance/llm-khoan-docx/r1/review-10-codex/VERDICT.md)

| Mục | Trạng thái | Bằng chứng |
| --- | --- | --- |
| K1 · §2.13 · markup compatibility | **ĐÃ VÁ THẬT** cho biểu hiện lượt 10 | `_chan_mc` duyệt toàn cây theo namespace, kể cả dưới `numPr`, `lvl` và ở cấp gốc của styles. Bỏ riêng guard ở document, numbering hoặc styles đều làm đỏ ca tương ứng. `mc:Ignorable` là thuộc tính, ngoài lệnh cấm phần tử của r11. Việc chọn part còn L1. [Mã](../scripts/tl_core/llm_route.py#L545) |
| K2 · §2.13 · tiêu đề đánh số bằng chữ | **VÁ SINH LỖI MỚI** | `Phần thứ hai` ở cấp con đã bị chặn, đột biến khôi phục regex cũ chết đúng ca. Đối chứng `Mục tiêu` đạt. Nhánh `thứ` nhận mọi từ và nhánh chữ cái nhận cả chữ thường ở đầu đoạn. Xem L2 và L3 về hai phía của chốt. [Regex](../scripts/tl_core/llm_route.py#L526) · [Ca](../scripts/tl_core/llm_route_test.py#L1468) |
| K3 · §2.13 · miền `lvlText` | **ĐÃ VÁ THẬT** cho chuỗi ngoài miền đã báo | `fullmatch` đòi ít nhất một `%1`–`%9`, phần còn lại chỉ là placeholder, dấu cho phép và khoảng trắng. Ca âm chữ số trần và `%` lẻ có mặt. Đột biến vô hiệu hóa chốt chết ở chữ số trần. Bullet vẫn chuẩn hóa sang `-`. Đọc thuộc tính vắng và hướng dẫn còn L4, L6. [Mã](../scripts/tl_core/llm_route.py#L774) · [Ca](../scripts/tl_core/llm_route_test.py#L1471) |
| K4 · §3 · ca dương một Điều | **ĐÃ VÁ THẬT** | §3 ghi đọc hết tệp một Điều và chặn tệp chứa thêm tiêu đề Điều. Ca quan hệ riêng của part chính đổi tên và đột biến tương ứng vẫn có kết quả. [§3](../ops/specs/llm-khoan-docx-r11.md#L169) · [Ca](../scripts/tl_core/llm_route_test.py#L1405) |
| §1, §2.1–§2.2 · CLI và đối chiếu | **ĐẠT** trong các ca có sẵn | Phát hiện zip theo chữ ký, buộc `--dieu`, cấm số hiệu kèm tệp DOCX, giữ đường gọi model và mặt cờ CLI. Ca nguồn mất số và ba kết quả đã lưu xác nhận 8/8. Với `khoan` cấu trúc, phép so đối chiếu vị trí, số thứ tự và đủ hai vế, đồng thời báo mục thừa/thiếu. `can_nguoi_duyet` luôn `true`, `pham_vi_kiem` theo đường nguồn. [CLI](../scripts/tl_core/ops_misc.py#L3025) · [Phép so](../scripts/tl_core/llm_route.py#L1258) · [Ca 8 khoản](../scripts/tl_core/llm_route_test.py#L1060) |
| A1/B1/C1/D1/E1/F1/G6/H1 · vùng Điều | **HẾT ĐỐI TƯỢNG do hợp đồng r7** với điểm cắt và đếm ngoài Điều. **ĐÃ VÁ THẬT** với fallback và ca tiêu đề cũ | Đoạn có nội dung đầu phải là tiêu đề đích đúng mẫu cả đoạn, không số tự động, không ngắt mềm hoặc phần tử lạ. Sau tiêu đề đọc đến hết tệp. Bảng và khối lạ chặn toàn tệp. Không số tự động trả `ValueError`, CLI rc 2, không còn `KhongCauTruc` hoặc quay về TXT. G6/H1 đã khóa hoa thường trong mẫu hiện hành. L2 còn kiểu tiêu đề ngoài regex. [Khối và vùng](../scripts/tl_core/llm_route.py#L998) · [Không có số](../scripts/tl_core/llm_route.py#L1035) |
| A2/B2/C2/D2/E6/F3–F5/G1/G3/H4/J1 · số Word | **ĐÃ VÁ THẬT** với biểu hiện cũ, **HẾT ĐỐI TƯỢNG** với đếm hàng/ô và tự khởi tạo tổ tiên | `start` vắng là 0, `startOverride` khác start gốc có đối chứng. Bộ đếm tách từng numId, reset cấp con khi cấp trên tăng, chặn nhảy cấp và vượt 999. Chặn ID lỗi/trùng sau chuẩn hóa, cấp ngoài miền, danh sách lai, lvlRestart/isLgl, restart qua section và style link. Cấp khoản phải decimal, đúng `%N.`/`%N)`, liên tục từ 1. Đoạn dùng style mang `numId` hoặc `ilvl` bị chặn dù có numId trực tiếp. [Định nghĩa](../scripts/tl_core/llm_route.py#L632) · [Cấp của đoạn](../scripts/tl_core/llm_route.py#L910) · [Bộ đếm](../scripts/tl_core/llm_route.py#L971) |
| A3/C3/D6 · từ nối và dấu | **ĐÃ VÁ THẬT** | Chốt dấu phân cách kiểm chữ mọi đoạn. Dò “là” chỉ ở đoạn mở khoản, ngoài ngoặc/trích dẫn và trước dấu hai chấm cấp khoản. Nguồn đã chia đúng thì lời đáp bỏ, gộp, cắt hoặc tráo khoản không qua so hai vế. [Chốt chữ](../scripts/tl_core/llm_route.py#L1084) · [Từ nối](../scripts/tl_core/llm_route.py#L1237) |
| A4/B3/C4/D3/E2/E5/J2 · chữ đã bỏ | **ĐÃ VÁ THẬT** trong biểu hiện cũ | Đọc XML gốc, bỏ `del`/`delText`/`moveFrom`, giữ `ins`/`moveTo` và chặn sửa dấu đoạn. Gạch đơn/kép xử lý riêng từ docDefaults và chuỗi style, nhiều tầng thì chặn trừ khi định dạng trực tiếp quyết định. Phản chứng quay về lọc regex hoặc giữ moveFrom vẫn chết. J2 được thay bằng chốt K1. [Run](../scripts/tl_core/llm_route.py#L823) · [Dấu đoạn](../scripts/tl_core/llm_route.py#L956) |
| A5/E3/E4 · định nghĩa danh sách và bảng | **HẾT ĐỐI TƯỢNG do hợp đồng r7** cho đoạn ngoài Điều và duyệt hàng/ô. **ĐẠT** cho kiểu danh sách không dùng | Vẫn có ca dương một định nghĩa không hỗ trợ nhưng không được dùng. Markup compatibility ở bất kỳ đâu trong ba part là ngoại lệ chặn toàn part theo r11. [Ca dương](../scripts/tl_core/llm_route_test.py#L1278) |
| A6/F2 · điểm gõ tay và câu dẫn | **HẾT ĐỐI TƯỢNG** với yêu cầu chấp nhận điểm gõ tay. **ĐÃ VÁ THẬT** với cửa nhập điểm tay | Đoạn có chữ không số sau khoản đầu bị chặn, điểm phải cùng numId và ở cấp con. Đoạn đã đánh số có tiền tố số gõ tay cũng bị chặn, còn số thập phân có đối chứng. Trước khoản đầu chỉ chấp nhận vắng câu dẫn hoặc đúng một câu khớp mẫu toàn đoạn. [Ghép đoạn](../scripts/tl_core/llm_route.py#L1052) · [Câu dẫn](../scripts/tl_core/llm_route.py#L1094) |
| B4–B6/C5/D5/F6/G4/H5/J5 · phần tử và ngắt | **ĐÃ VÁ THẬT** cho các biểu hiện cũ | Dấu nối không ngắt, tab/ptab, wrapper và mốc move cân có ca sẵn. Strict, phần tử chưa hiểu và mốc move lẻ bị chặn. Ngắt trang/cột cuối đoạn được nhận, chữ hữu hiệu theo sau thì chặn. Chữ gạch sau ngắt được bỏ trước khi áp chốt. [Danh sách](../scripts/tl_core/llm_route.py#L530) · [Ngắt](../scripts/tl_core/llm_route.py#L862) |
| G2/H2/J4 · quan hệ part | **ĐÃ VÁ THẬT** cho tên mặc định và rels sai vị trí. Lớp vẫn mở | Quan hệ gốc chọn part chính, quan hệ của part đó chọn styles/numbering. Ca rels đổi tên đạt. Cửa so kiểu quan hệ bằng hậu tố còn L1. [Quan hệ](../scripts/tl_core/llm_route.py#L593) |
| A7/B7/C6/D4/E5/F5/G5/H3 · phép đo | **ĐẠT** cho các ca đích lịch sử còn áp dụng | Harness chỉ tính đột biến chết khi ca đích ném `TinHieuChotCa`. Log breakpoint xác nhận các chốt bản vá và các trường hợp riêng đã báo gồm `startOverride`, điểm gạch, abstract ID và part đánh số đổi tên. Xem bảng phép đo. [Harness](../scripts/tl_core/llm_route_test.py#L1856) |
| A8/B8/C7 · hướng dẫn | **ĐÃ VÁ THẬT** với mâu thuẫn cũ | Hướng dẫn ghi một khoản một dòng TXT, một Điều một DOCX, hai dạng dấu cuối nhãn khoản, đánh số qua style và điểm tay bị chặn. Miền dấu của nhãn cấp con còn L6. [Hướng dẫn](../docs/GOI_AGENT_DA_NEN.md#L373) |
| K1 **của #1514** · §2.3 | **ĐÃ VÁ THẬT** ở hai cửa ghép đã báo | Dòng điểm khớp `_RE_DIEM` trả `None` ở cả hai loại nguồn. Dòng mở bằng “là” ở nguồn có số rơi vào nhánh từ chối dòng không số. Ở nguồn mất số nó tự đứng và phép so chặn do thuật ngữ rỗng. Mẫu và đột biến `wp1525_tho_nhan_diem` xác nhận chốt điểm. [Tách thô](../scripts/tl_core/llm_route.py#L1127) · [Ca điểm](../scripts/tl_core/llm_route_test.py#L1170) · [Verdict #1514](../ops/acceptance/llm-ranh-gioi-khoan/r1/review-10-codex/VERDICT.md#L35) |

Đường thô vẫn có thể nhận một điểm ngoài miền nhận diện làm khoản độc lập nếu dòng có hình dạng định nghĩa đầy đủ. Tương tự, tiểu mục đã bị làm phẳng có thể mang số đúng dãy khoản, và một dòng tiếp tự kết câu có thể thành khoản riêng trong nguồn mất số. Nếu TXT đã mất chữ, markup hoặc phần đuôi trước khi vào lệnh, nó chỉ được so với chính snapshot đưa vào. Đường số hiệu chặn tín hiệu CAP và chuyển tiếp cảnh báo markup của `tl extract`. Đây là giới hạn của lớp `ranh-gioi-khoan` trên nguồn thô, đã khai trong `pham_vi_kiem` và hướng dẫn. [Phạm vi thô](../scripts/tl_core/llm_route.py#L1100) · [CAP](../scripts/tl_core/llm_route.py#L1363) · [Chuyển cảnh báo](../scripts/tl_core/ops_misc.py#L3088)

## Findings

### L1 [P1] Kiểu quan hệ OOXML được so bằng hậu tố nên có thể chọn sai part — `scripts/tl_core/llm_route.py:593`

**Kịch bản và căn cứ.** Kiểu quan hệ là URI đầy đủ. `_giai_quan_he` chỉ so đuôi `/styles`, `/numbering` hoặc `/officeDocument`. Với DOCX có part chính và numbering chuẩn, nhưng không có quan hệ styles chuẩn, một quan hệ mở rộng có cùng hậu tố trỏ tới một part chứa định nghĩa style có thể được nhận làm styles chính. `_doc_kieu` áp định nghĩa đó vào run, rồi `_phan_tich_doan` có thể lọc nhầm chữ vẫn hiển thị. Với numbering, cùng cách so có thể làm bộ đọc dựng số từ part mà Word không dùng cho danh sách của tài liệu. Khi quan hệ chuẩn và quan hệ mở rộng cùng tồn tại, reader lại thấy hai quan hệ và chặn oan. Hạng P1 vì ở nhánh chỉ có một quan hệ đuôi trùng, phép so có thể chấp nhận một bản chép theo chữ hoặc số dựng từ sai part. Kết luận lần theo mã. Các fixture quan hệ đã có dùng đúng URI chuẩn. [Chọn quan hệ](../scripts/tl_core/llm_route.py#L601) · [Lọc gạch theo style](../scripts/tl_core/llm_route.py#L836) · [URI trong ca sẵn](../scripts/tl_core/llm_route_test.py#L1323)

**Đề xuất.** So kiểu quan hệ theo bảng URI đầy đủ của OOXML Transitional ở cả ba nơi. Giữ quy tắc đếm nhiều quan hệ đúng loại và fallback đúng trường hợp thiếu tệp rels. Khóa hành vi cho URI chuẩn, URI mở rộng trùng hậu tố và cả hai cùng tồn tại.

### L2 [P1] Tiêu đề Điều thiếu dấu phân cách có thể trở thành điểm của Điều trước — `scripts/tl_core/llm_route.py:524`

**Kịch bản và căn cứ.** Khi chép từ Word hoặc Google Docs, tiêu đề của Điều tiếp theo có thể chỉ mang tên loại và số, hoặc có tên Điều sau một khoảng trắng. Nếu đoạn đó vô tình kế thừa đánh số cấp con của khoản liền trước, chốt tiêu đề trong vùng đòi dấu chấm hoặc hai chấm ngay sau số nên không nhận ra. Chốt số gõ tay chỉ xét đầu bằng chữ số. Cùng numId và cấp con đủ để nối cả đoạn vào khoản trước, rồi đầu ra chép theo khối đó có thể qua so. Hạng P1 vì §2.9 buộc từ chối tiêu đề Điều khác trong vùng và chuẩn so có thể bị nối thêm chữ của Điều khác. Ca sẵn chỉ khóa tiêu đề thứ hai có dấu. [Chốt tiêu đề](../scripts/tl_core/llm_route.py#L1020) · [Nối cấp con](../scripts/tl_core/llm_route.py#L1063) · [Ca hiện tại](../scripts/tl_core/llm_route_test.py#L1489)

**Đề xuất.** Giữ mẫu chặt cho tiêu đề đích. Với vùng thân, dùng thêm hình dạng đầu đề nguyên đoạn khi thiếu dấu và chặn vị trí mơ hồ trước khi nối cấp con. Đo cùng đối chứng dẫn chiếu Điều có trong thân hợp lệ để giới hạn chặn oan.

### L3 [P2] Mẫu tiêu đề viết bằng chữ có thể chặn thuật ngữ hợp lệ ở đầu khoản — `scripts/tl_core/llm_route.py:526`

**Kịch bản và căn cứ.** Một khoản có thể mở bằng thuật ngữ chỉ một loại phần thứ cấp. Regex coi mọi từ sau `thứ` là số thứ tự và chỉ kiểm tiền tố, nên đoạn định nghĩa bị từ chối trước khi xét vai trò. Mẫu chữ cái đơn cũng dùng `IGNORECASE` cho cả hậu tố, rộng hơn chữ hoa của §2.13. Ca dương `Mục tiêu` không đi qua hai nhánh mới này. Hạng P2 vì đường này từ chối nguồn có nội dung đọc được. [Regex](../scripts/tl_core/llm_route.py#L526) · [Đối chứng](../scripts/tl_core/llm_route_test.py#L1348)

**Đề xuất.** Phân biệt từ chỉ số thứ tự với từ bổ nghĩa, và giữ điều kiện chữ hoa của ký hiệu riêng với điều kiện hoa thường của tiền tố. Đo đối chứng đoạn định nghĩa mở bằng cùng nhóm từ.

### L4 [P2] Thiếu giá trị `lvlText` làm thoát bằng `TypeError` — `scripts/tl_core/llm_route.py:667`

**Kịch bản và căn cứ.** Nếu phần tử `lvlText` có mặt nhưng không khai `w:val`, decoder giữ `None`. Cấp khoản truyền giá trị đó cho `re.fullmatch`, cấp điểm không phải bullet cũng làm tương tự. Cả hai ném `TypeError`, ngoài các exception mà CLI bắt để trả rc 2. Cùng loại lỗi chuyển giá trị có thể xảy ra nếu phần tử `start` hoặc `startOverride` hiện diện mà thiếu `w:val`. Hạng P2 vì nguồn không tạo kết quả sai, nhưng thoát traceback thay cho từ chối có chẩn đoán theo hợp đồng. [Đọc giá trị](../scripts/tl_core/llm_route.py#L660) · [Kiểm nhãn](../scripts/tl_core/llm_route.py#L793) · [Chốt cấp khoản](../scripts/tl_core/llm_route.py#L1048) · [CLI](../scripts/tl_core/ops_misc.py#L3044)

**Đề xuất.** Xác thực trường vắng hoặc rỗng tại lúc đọc định nghĩa, với lỗi cấu trúc có chẩn đoán cho danh sách được dùng. Giữ mặc định hiện hành khi vắng hẳn phần tử `start`.

### L5 [P2] Part chính bị buộc UTF-8 trước khi parser XML đọc khai báo mã hóa — `scripts/tl_core/llm_route.py:948`

**Kịch bản và căn cứ.** XML WordprocessingML chính có thể dùng UTF-16. Mã hiện ép bytes của part chính qua UTF-8 trước `ET.fromstring`, trong khi nạp styles và numbering trực tiếp từ bytes. Một tài liệu Transitional có cấu trúc khoản hợp lệ nhưng mã hóa part chính UTF-16 bị chặn ở CLI. Hạng P2 vì đây là giới hạn mã hóa chưa khai và chặn oan. Chưa đo tần suất phát sinh từ Word hoặc Google Docs. [Nạp part chính](../scripts/tl_core/llm_route.py#L944) · [Nạp numbering](../scripts/tl_core/llm_route.py#L637)

**Đề xuất.** Đưa bytes đã giới hạn vào parser XML như hai part kia để parser xử lý mã hóa. Giữ nguyên chốt namespace Transitional và chẩn đoán XML không hợp lệ.

### L6 [P3] Hướng dẫn `lvlText` thiếu dấu gạch en, khoảng trắng và ngoại lệ bullet — `docs/GOI_AGENT_DA_NEN.md:398`

Hướng dẫn mô tả miền hẹp hơn §2.13 K3 và quy tắc đang chạy. Hạng P3 vì đây là sai lệch tài liệu, còn guard thực thi đúng miền của K3 với chuỗi. Đồng bộ đoạn hướng dẫn với miền thật và ngoại lệ bullet. [Hướng dẫn](../docs/GOI_AGENT_DA_NEN.md#L398) · [K3](../ops/specs/llm-khoan-docx-r11.md#L165)

| Lớp | Biểu hiện, mức cao nhất và phép kiểm đóng |
| --- | --- |
| `docx-markup-du-thao` | A4/B3/C4/D3/E2/G2/H2 → J2 → K1 → L1, P1. K1 đã khóa phần tử `mc:`; L1 cần xác minh định danh đầy đủ của quan hệ trước khi áp style hoặc bộ đếm. |
| `ranh-gioi-khoan` | A1/F1/G6/H1 → J3 → K2 → L2/L3, P1. K1 của #1514 đã đóng ở hai cửa ghép thô. Trong DOCX cần đo chốt tiêu đề với hai chiều, tránh ghép tiêu đề thật và tránh chặn thuật ngữ. |
| `docx-so-hien-thi` | A2/B2/C2/D2/F3/G1/H4 → J1 → K3 → L4/L6, P2. Kiểm kiểu và giá trị thật của định nghĩa nhãn trước khi dựng nhãn; hướng dẫn khớp miền đã kiểm. |
| `docx-ma-hoa-part` | L5, P2, lớp mới. Đo cùng nội dung qua mã hóa XML được hỗ trợ và lỗi parse có kiểm soát. |
| `do-phu-chot-docx` | A7/B7/C6/D4/E5/F5/G5/H3 → J4 → K4, các biểu hiện đã báo đã đóng. |
| `docx-ngat-trinh-bay` | G4/H5 → J5, các biểu hiện đã báo đã đóng. |

Có 6 finding mở trên 4 lớp, gồm 0 P0, 2 P1, 3 P2 và 1 P3. Theo ADR-0060 M1 và ADR-0062, exact head chưa đạt điều kiện merge. Đây là lượt cuối 11/11, các lớp lặp và finding mở được chuyển về Review Rescue Checkpoint của §12. [ADR-0060 M1](../docs/adr/0060-dieu-kien-merge-va-moc-ready.md#L32) · [ADR-0062](../docs/adr/0062-adr-0060-mac-dinh-va-dong-bang-adr-0054.md) · [Protocol §12](../docs/PROTOCOL_DA_PHIEN.md#L1097)

## Kết quả test và đột biến

Các lệnh chạy với `PYTHONDONTWRITEBYTECODE=1` trong bản sao exact head/tree. Selftest nền dùng checkout baseline có tree `0cc14e79cecd2ce44bc4dc6cff92cadb31fd7ee4`. Log và mã thoát lưu trong `/tmp/wp1525-r11-review.2dHH8pD5/`.

| Lệnh | Trạng thái | Rc và bằng chứng |
| --- | --- | --- |
| `python scripts/tl_core/llm_route_test.py` | `passed` | rc 0, **63/63** ca, **174/174** đột biến chết tại ca đích. `llm.log`. |
| `python scripts/tl.py --deterministic workflow-audit --strict --json` | `passed` | rc 0, `ok=true`, 26 card, 60 task, 194 lệnh hiện diện, 0 lỗi và 0 cảnh báo. `workflow.log`. |
| `python scripts/tl.py --deterministic golden-test --json` | `passed` | rc 0, `ok=true`, **20/20** ca và **20/20** raw stable trên hai lần chạy nội bộ. `golden.log`. |
| `python scripts/tl.py release-verify RELEASE_MANIFEST.json --strict --json` | `passed` | rc 0, `ok=true`, **187/187** tệp, 0 lỗi/thiếu/thừa, `package_hash_match=true`, hash gói `54b478502067304bba8aca3c9e279b9b6192780254756740b4ea1f2750c55745`. `release.log`. |
| `python ops/lease_publish.py check --root . ops/leases/llm-khoan-docx-r11-g1-claude.yaml` | `passed` cục bộ | rc 0, “ĐĂNG ĐƯỢC”, Issue #1525, neo `64b7f2c14776`, hết hạn 22:53 UTC. `lease.log`. |
| `python scripts/tl.py --selftest`, head | `failed` | rc 1, **1774/1790**, transport **12/12**. Ca CLI `r1525_llm_khai_niem_tep_docx_cau_truc` **OK**, kiểm các rc 0/5/2 bằng stub. `selftest-head.log`. |
| `python scripts/tl.py --selftest`, baseline | `failed` | rc 1, **1773/1789**, transport **12/12**. `selftest-base.log`. |
| `git diff --check 582cb44 HEAD` và `git diff --check fcb12b3 HEAD -- . ':!ops/acceptance/llm-ranh-gioi-khoan/'` | `passed` | rc 0 cho từng diff. |
| `git diff --check 64b7f2c HEAD` và `git diff --check 64b7f2c fcb12b3` | `failed` | rc 2 mỗi lần, cùng ba dòng có khoảng trắng cuối dòng của [verdict #1514 lượt 8](../ops/acceptance/llm-ranh-gioi-khoan/r1/review-8-codex/VERDICT.md#L3). |

Cả hai selftest có cùng 16 ca đỏ. `diff -u` hai danh sách `[FAIL]` trả rc 0, và `diff -u` toàn bộ dòng `[OK]`/`[FAIL]` cũng rc 0 sau khi loại đúng ca CLI mới #1525 khỏi danh sách head. Nhóm 14 ca trong prompt gồm 8 `r973_bootstrap_*`, 5 `wp433_*` và `wp727_tl_gws_refresh`. `/tmp/.git` tồn tại, rỗng và chỉ đọc trong môi trường này. Hai ca đỏ thêm trên cả hai cây là `r226_nguong_l2_troi_theo_abbrev_va_ci_ghim` và `r268_l2_trichotomy_theo_trang_thai_object`. Chênh lệch ca đỏ bằng 0, selftest vẫn chưa đạt N/N. SHA-256 log head `c90dc46d1ee2a41cad21f88946e91f43cf61537ee371717bf3b05cfe3a0f824c`, log nền `6f75fd4baa64ad3c3fe29daddcee8ddfa92139576d76fed6bbd9e32277042b32`.

Đo `python -m pdb scripts/tl_core/llm_route_test.py` với breakpoint dòng 1876, điều kiện `ten.startswith('wp1525_')`, tại nhánh bắt `TinHieuChotCa`. Rc trình gỡ lỗi và suite đều 0, ghi nhận **77/77** đột biến `wp1525_*` đến đúng ca đích. Lần đầu đặt breakpoint bằng đường dẫn tương đối bị PDB từ chối, nên phép đo dùng lần chạy lại đặt breakpoint tại dòng trong module hiện hành. Log `mutation-targets-retry.log`, SHA-256 `f435d86598736e60bbfdd625882c93fbf6be7653e66f0c6d09da4d7c866571c3`. [Harness](../scripts/tl_core/llm_route_test.py#L1856)

| Đột biến | Ca đích và kết quả |
| --- | --- |
| `wp1525_mc_bo_qua` | `ca_cau_truc_docx_chan`, lộ `mc` trong `rPr` của run. |
| Bỏ riêng `_chan_mc` ở document, styles hoặc numbering, từng lần trên bản sao tạm, chạy `python scripts/tl_core/llm_route_test.py` | Mỗi lần rc 1 và **62/63**. `ca_cau_truc_docx_chan` thất bại đúng điều kiện `mc trong rPr cua run`, `mc trong styles` hoặc `mc trong numbering`. Logs `mutation-no-mc-document.log`, `mutation-no-mc-styles.log`, `mutation-no-mc-numbering.log`. Đã đối chiếu lại byte mã của bản sao sau phép đo. |
| `wp1525_ranh_gioi_lon_chi_so` | `ca_cau_truc_docx_chan`, lộ tiêu đề Phần viết số thứ tự bằng chữ ở cấp con. |
| `wp1525_lvltext_tu_do` | `ca_cau_truc_docx_chan`, lộ nhãn chữ số trần. Ca `%` lẻ đã chạy trong suite dương, breakpoint dừng ở chốt đầu tiên của đột biến. |
| `wp1525_bo_qua_start_override` | `ca_cau_truc_docx_dat`, đọc số gốc 5 thay vì override 1 nên bị từ chối. |
| `wp1525_rels_part_chinh_mac_dinh` | `ca_cau_truc_docx_rels_part_chinh`, đọc numbering theo tên mặc định khiến khoản dùng `lowerLetter` ngoài hợp đồng. |
| `wp1525_gach_sau_ngat_la_ngat` | `ca_cau_truc_docx_dat`, chữ đã gạch sau ngắt trang làm chặn oan đối chứng. |
| `wp1525_tho_nhan_diem` | `ca_wp1514_luot9`, mất chốt khiến dòng điểm được nhận thành khoản. Suite gốc có cả nguồn có số và mất số. |

Không lệnh nào trong sáu lệnh của prompt ở trạng thái `skipped`.

## Không đo được

- L1–L5 là kết luận tĩnh, giới hạn ở đường đi đã nêu. Chưa có phép đo trên Word hoặc Google Docs cho quan hệ mở rộng, đầu đề thiếu dấu, thân khoản mở trùng tiền tố, thuộc tính `lvlText` vắng và XML UTF-16. Chưa xác lập thêm phần tử thông dụng của bản export bị chặn oan ngoài giới hạn đã khai. Bảng, hình, trường, chú thích, DOCX Strict, điểm tay, đánh số qua style và phần tử `mc:` đã nằm trong giới hạn. Tần suất chặn oan và khác biệt render giữa ứng dụng chưa đo. [Danh sách cho phép](../scripts/tl_core/llm_route.py#L530) · [Hướng dẫn](../docs/GOI_AGENT_DA_NEN.md#L390)
- Chưa đo Word áp `docDefaults/pPrDefault/numPr` trong tổ hợp với override trực tiếp, hoặc render dữ liệu liên kết của content control và chữ ẩn. Mã hiện đọc `rPrDefault`, `w:style/w:pPr` và `sdtContent`. Các ca hiện có chưa cho phép kết luận đường đọc này phù hợp với mọi tùy chọn hiển thị theo ứng dụng. [Styles](../scripts/tl_core/llm_route.py#L704) · [Wrapper nội dòng](../scripts/tl_core/llm_route.py#L890)
- `not_run` gồm `determinism-audit --strict`, `doc-claims-check --strict` độc lập, Ruff contract và lint, CI/GitHub và hai kiểm GitHub của lease. Windows bản địa và Windows CI cũng `not_run`. Diff toàn PR chạm mẫu `encoding=` của ADR-0060 M3, nên evidence Windows còn thiếu. [Nghiệm thu §5](../ops/specs/llm-khoan-docx-r11.md#L182) · [ADR-0060 M3](../docs/adr/0060-dieu-kien-merge-va-moc-ready.md#L43)
- Model và effort đã phục vụ `KHONG_DO_DUOC` từ metadata hiện có. Mã thoát con, mã thoát launcher và băm stdout cuối là dữ liệu chốt sau khi run kết thúc. Head máy chủ, repo Executor và runtime Executor ngoài phạm vi quan sát của lượt offline. [Protocol §8.1–8.2](../docs/PROTOCOL_DA_PHIEN.md#L770)

Đầu và cuối lượt cùng exact SHA/tree. Checkout được giao có diff và index rỗng, chỉ thêm `.review/VERDICT.md` và giữ mục ignored `.codex/` có sẵn. Các fixture do test tự sinh và cache nằm trong bản sao tạm. Snapshot chứng minh delta quan sát được tại hai mốc. Phép đo dùng mục có sẵn và đột biến mã trong bản sao, với không lần gọi mô hình thật.

P2_mo: 3
VERDICT: REQUEST_CHANGES
