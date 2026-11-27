# Verdict packet #1525 r44 lượt 44 — Codex

reviewed_sha: cc7fac74fd99fa2ecc9a84017357657e2fff0d5f
reviewed_tree: cc339bfbe559dee83e675d98f5c3b70f70b34e91
base_sha: 64b7f2c14776d5d0e1d34a6be4725490956f5bec
base_tree: 0cc14e79cecd2ce44bc4dc6cff92cadb31fd7ee4

## Xác minh đầu vào

- Packet #1525 r44/g1, lease `llm-khoan-docx-r44-g1-claude`, Review Class khai báo và hiệu lực đều `sensitive`. Executor theo lease là `claude / claude_code / machine/local`, họ Claude. Hồ sơ launcher xác nhận reviewer `openai_codex / codex_cli / machine`, run `09c240cd2b264af6af9e8fd2a66e38f5`. Linux x86_64, Python 3.13.18, Codex CLI 0.172.0, sandbox `workspace-write` với mạng hạn chế, `core.abbrev=7`. Lease hết hạn 2026-11-27 10:15 UTC. Đây là lời gọi thứ 45/45 theo lease và prompt.
- Bản giao detached đúng SHA và tree. Mốc bàn giao #1514 là `fcb12b3873c3bec2c339029136243ed2c804ce05` với bản lưu bàn giao `2c9183223b48c36e56df7617ce97dcdc9dc259d2`. Mốc tách diff toàn PR là `695916ea3bfffdd7b2e8fcb94b0740b3c421fe70`, được merge ở `8afb0c7`. Hai cha lần lượt là `c671163` và `695916e`. Mốc bản vá lượt này là `b68bdeaff3c9de6768450f096def34f3be3da109`. Trạng thái ứng viên chưa push lấy từ prompt bàn giao.
- Blob đặc tả `6d681a27bf5367847e9b2082d4203f351892886f` và tệp checkout đều có SHA-256 `b6b014cd24c70d1e86183c0ba86d6c38ae573636cd8cf54837d315c720c6cee6`, khớp lease. SHA-256 prompt `689a16bb5df74ca5152f53df95a0c3b0e45f7a1c71bac77d5528656fce8bc5b1` khớp run và checkpoint. [Đặc tả r44](../../../../../ops/specs/llm-khoan-docx-r44.md) · [Lease r44](../../../../../ops/leases/llm-khoan-docx-r44-g1-claude.yaml)

## Đối chiếu lượt 43 và đặc tả r44

| Mục | Trạng thái | Bằng chứng |
| --- | --- | --- |
| Lượt 43 `can-tai-nguyen-doc-nguon`, §2.46 và hint thu hồi | **VÁ MỘT PHẦN**, còn đường trước khi ghi sổ và giao ống chưa hoàn tất. | Giữ lỗi khởi động reader và `__cause__`, bảo vệ từng `join`, ghi chú timeout và in ghi chú qua CLI. Probe thu hồi phân biệt được sáu đầu vào đã khóa. Sổ vẫn sinh theo từng reader, không ghi cả hai ống lúc nhận từ `Popen`. Trạng thái bootstrap vẫn lấy `is_alive()` tức thời để cấp quyền đóng ống. Reader và oracle còn các nhánh liệt kê trong finding. [R44](https://github.com/ducthangho/tra-luat/blob/cc7fac74fd99fa2ecc9a84017357657e2fff0d5f/scripts/tl_core/llm_route.py#L1982) · [Hint lượt 43](../../../../../ops/acceptance/llm-khoan-docx/r1/review-43-codex/VERDICT.md#L48) |
| Lượt 43 `lien-ket-bang-chung-review`, §2.46 | **ĐÃ VÁ THẬT** trong phạm vi archive 41–43. | Đọc 113 đích blob/dòng riêng, 32 đích tương đối và 4 đích neo riêng tính theo từng verdict. Cả ba run có exact head, rc 0 và hash prompt checkout khớp. Mã/tài liệu ghim blob đúng `reviewed_sha`. Neo scratch mở mục có thật, gồm chú thích phạm vi lưu trữ. [Chỉ mục](../../../../../ops/acceptance/llm-khoan-docx/r1/LIEN_KET.md) · [Log](#nhat-ky-scratch) |
| `ranh-gioi-khoan`, §2.38–§2.45 | **VẪN ĐÓNG** trong miền chủ kho đã chốt. | Diff r44 không đổi bộ quét. Cả nguồn có số và mất số qua `dau_dong_cho_phep` và chốt trên cùng span thân. `_mo_dau_nhieu_ve` dùng vị trí `_tu_noi`, dấu kết chung và trạng thái ngoài nhóm/ngoặc đầu/nháy đầu. `_dong_mo_ho` lấy trạng thái cuối và sự kiện từ cùng máy quét. Hai phía miền và giới hạn nhãn số trùng khoản giữ trong `PHAM_VI_KIEM`. [Đầu dòng](https://github.com/ducthangho/tra-luat/blob/cc7fac74fd99fa2ecc9a84017357657e2fff0d5f/scripts/tl_core/llm_route.py#L587) · [Dấu phân cách](https://github.com/ducthangho/tra-luat/blob/cc7fac74fd99fa2ecc9a84017357657e2fff0d5f/scripts/tl_core/llm_route.py#L1785) · [Tín hiệu kết quả](https://github.com/ducthangho/tra-luat/blob/cc7fac74fd99fa2ecc9a84017357657e2fff0d5f/scripts/tl_core/llm_route.py#L1679) |
| §1, §2.2–§2.3, K1 của #1514 | **ĐÃ VÁ THẬT**. | Dòng điểm chữ hoặc dấu đầu dòng ở miền K1 làm từ chối cả Điều. Dòng tiếp mở bằng “là” ở nguồn có số thiếu số khoản nên bị từ chối. Ở nguồn mất số, phép so đòi vế thuật ngữ và định nghĩa đều khác rỗng. Giữ một dòng mỗi khoản, số liên tục từ 1, so đủ mục theo thứ tự, giữ `can_nguoi_duyet: true`. [K1](../../../../../ops/acceptance/llm-ranh-gioi-khoan/r1/review-10-codex/VERDICT.md#L35) · [Phân đoạn](https://github.com/ducthangho/tra-luat/blob/cc7fac74fd99fa2ecc9a84017357657e2fff0d5f/scripts/tl_core/llm_route.py#L1689) · [Phép so](https://github.com/ducthangho/tra-luat/blob/cc7fac74fd99fa2ecc9a84017357657e2fff0d5f/scripts/tl_core/llm_route.py#L1865) · [CLI](https://github.com/ducthangho/tra-luat/blob/cc7fac74fd99fa2ecc9a84017357657e2fff0d5f/scripts/tl_core/ops_misc.py#L3140) |
| §2.1, §2.4–§2.18, vùng Điều, điểm gõ tay, câu dẫn và fallback | **HẾT ĐỐI TƯỢNG** đối với lỗi định vị/cắt vùng cũ, đếm qua bảng và nhập điểm gõ tay. **ĐÃ VÁ THẬT** các chốt hiện hành. | Đọc tệp một Điều, tiêu đề nguyên đoạn ở nội dung đầu tiên, vùng đến EOF, chặn tiền tố Điều/Chương/Mục/Phần và bảng/khối không hiểu. Điểm sau khoản phải cùng danh sách cấp con tự động. Trước khoản đầu nhận tối đa một câu dẫn khớp toàn đoạn. DOCX thiếu cấu trúc dừng với lỗi, đường lùi `KhongCauTruc` đã bỏ. [Vùng](https://github.com/ducthangho/tra-luat/blob/cc7fac74fd99fa2ecc9a84017357657e2fff0d5f/scripts/tl_core/llm_route.py#L1557) · [Câu dẫn](https://github.com/ducthangho/tra-luat/blob/cc7fac74fd99fa2ecc9a84017357657e2fff0d5f/scripts/tl_core/llm_route.py#L1663) · [Định tuyến](https://github.com/ducthangho/tra-luat/blob/cc7fac74fd99fa2ecc9a84017357657e2fff0d5f/scripts/tl_core/ops_misc.py#L3037) |
| §2.4, §2.10–§2.15, §2.22–§2.27, số Word và part | **ĐÃ VÁ THẬT** ở các biểu hiện đã báo trong miền nhận. | Đọc part theo quan hệ, ID chuẩn hoá bằng chuỗi. `start` mặc định 0, `startOverride` đúng cấp, bộ đếm 0–999 theo numId, reset cấp con, chặn nhảy cấp, đòi cùng numId và khoản liên tục từ 1. Cấp/override ngoài miền dừng và chữ Word lặp đúng quy tắc. Phép so tìm từ nối ở đoạn đầu khoản, so đầy đủ thân kể cả dòng điểm. [Định nghĩa](https://github.com/ducthangho/tra-luat/blob/cc7fac74fd99fa2ecc9a84017357657e2fff0d5f/scripts/tl_core/llm_route.py#L932) · [Nhãn](https://github.com/ducthangho/tra-luat/blob/cc7fac74fd99fa2ecc9a84017357657e2fff0d5f/scripts/tl_core/llm_route.py#L1129) · [Bộ đếm](https://github.com/ducthangho/tra-luat/blob/cc7fac74fd99fa2ecc9a84017357657e2fff0d5f/scripts/tl_core/llm_route.py#L1540) |
| §2.5–§2.8, §2.13, §2.19–§2.35, §2.37, chữ hiệu lực, style và biên ký tự | **ĐÃ VÁ THẬT** ở các biểu hiện lịch sử được khóa trong đường CLI. | Giữ `ins/moveTo`, lọc `del/moveFrom` và run gạch hiệu lực trên XML gốc. Gạch đơn/kép được tính riêng, có chốt sửa dấu đoạn và mốc move. Kiểm `xml:space`, loại style, trường đơn trị, `mc:` và chữ gốc ở mọi đoạn trước khi chọn tiêu đề. [Style](https://github.com/ducthangho/tra-luat/blob/cc7fac74fd99fa2ecc9a84017357657e2fff0d5f/scripts/tl_core/llm_route.py#L1033) · [Run và wrapper](https://github.com/ducthangho/tra-luat/blob/cc7fac74fd99fa2ecc9a84017357657e2fff0d5f/scripts/tl_core/llm_route.py#L1256) · [Kiểm tài liệu](https://github.com/ducthangho/tra-luat/blob/cc7fac74fd99fa2ecc9a84017357657e2fff0d5f/scripts/tl_core/llm_route.py#L1498) |
| §2.21 U2, §2.22 V3, §2.23 W1/W3 và phần số hiệu của W2 | **GIỚI HẠN ĐÃ KHAI**. | Tuyến `<số hiệu>` vẫn dùng `tl extract --markup-strict` và chặn CAP. Làm sạch cache, cách cắt Điều, chữ gạch qua style và tab/ngắt thuộc các giới hạn đã ghi của tầng extract. Nhãn dính thân, nhãn chỉ ngăn bằng đệm và nhãn số trùng khoản thuộc ba giới hạn đường thô của §2.38–§2.39. [Giới hạn CLI](https://github.com/ducthangho/tra-luat/blob/cc7fac74fd99fa2ecc9a84017357657e2fff0d5f/docs/GOI_AGENT_DA_NEN.md#L390) · [Extract](https://github.com/ducthangho/tra-luat/blob/cc7fac74fd99fa2ecc9a84017357657e2fff0d5f/scripts/tl_core/llm_route.py#L2080) |
| §2.37–§2.45, ngân sách ngoài bộ chạy extract | **VẪN ĐÓNG** với các biểu hiện lịch sử của tệp thô, XML và ZIP. | Tệp thô có trần byte/ký tự/số đầu dòng. Tiền kiểm gói đếm entry thật trên cùng handle, đọc locator ZIP64 ở vị trí tuyệt đối, chặn mã hoá/codec ngoài miền trước `ZipFile`. Lỗi mở/đọc ZIP ở biên hẹp. XML có giới hạn nút/độ sâu, style giải có nhớ, nhãn và tổng chữ có ngân sách trước khi dựng chuỗi. [Biên ZIP](https://github.com/ducthangho/tra-luat/blob/cc7fac74fd99fa2ecc9a84017357657e2fff0d5f/scripts/tl_core/llm_route.py#L1401) · [XML](https://github.com/ducthangho/tra-luat/blob/cc7fac74fd99fa2ecc9a84017357657e2fff0d5f/scripts/tl_core/llm_route.py#L696) |
| Write set và bia mộ | **KHỚP**. | Tập 234 path có SHA-256 `0f1ee2686884988e69c21b755f82cfa8fdc65ddd6742f6c9f4f90aa5475dcb48`. 14/14 path r44 thuộc tập. Diff toàn PR có 277 path, 47 ngoài tập là hồ sơ, spec và lease lịch sử #1514 còn nguyên từ `2c91832`. Bia mộ #1514 r9 ↔ #1525 r1 ↔ … ↔ r44 khớp 88/88 chiều của 44 cặp. [Log](#nhat-ky-scratch) |

### Đối chiếu các biểu hiện lịch sử

| Lượt #1525 | Kết quả |
| --- | --- |
| 1–6, A1–A8, B1–B8, C1–C7, D1–D6, E1–E6, F1–F6 | **HẾT ĐỐI TƯỢNG** với điểm cắt, đếm qua bảng, fallback và nhận điểm gõ tay theo hợp đồng cũ. **ĐÃ VÁ THẬT** ở đường đọc XML, từ nối, số Word, wrapper và các chốt còn hiệu lực. Strict Word có giới hạn và chẩn đoán. |
| 7–12, G1–G6, H1–H5, J1–J5, K1–K4, L1–L6, M1–M2 | **ĐÃ VÁ THẬT** các cửa còn chạy về ID/cấp, nhãn, part, dấu ngắt, hướng dẫn, kiểm tiêu đề và mã hoá. G3 hết cơ chế cũ nhờ chặn nhảy cấp. J2 dùng chốt `mc:` cả part. L2/M1 dùng chốt tiền tố. |
| 13–21, N1–N3, Q1–Q2, R1–R3, S1–S3, T1–T2, U1–U2, V1–V4, W1–W5, X1–X3 | **ĐÃ VÁ THẬT** các biểu hiện trong write set của biên ký tự, kiểu số, tiền tố, markup, nút đơn trị và chốt số. U2, V3, W1/W3/W2 phần số hiệu theo giới hạn đã duyệt. |
| 22–33, Y1–Y3, Z1–Z4, A1–A2, B1–B3, C1–C2, D1, E1, F1–F2, G1–G2, H1–H3, I1–I2, J1–J2 | **ĐÃ VÁ THẬT** các biểu hiện đã báo theo điều khoản thay thế. Đường thô dùng danh sách cho phép và một bộ quét, giữ chốt ký tự, style, chữ bị bỏ và ngắt theo hợp đồng. |
| 34–38 | **ĐÃ VÁ THẬT** các hình dạng nhãn đã báo nằm trong miền từ chối, ký tự mọi đoạn và trần nguồn tệp. Ghi nhận nhãn số trùng khoản theo quyết định §2.39. Phần ngân sách tiến trình được xét tại finding còn mở. |
| 39–43 | **ĐÃ VÁ THẬT** hướng dẫn DOCX, ghi chú write set, kết tệp hồ sơ, ZIP64/codec, hợp nhất quét nhãn và liên kết archive trong miền đã kiểm. **VÁ MỘT PHẦN** bộ chạy extract và oracle §2.46. |

Đọc mã chưa xác lập đường P0/P1 trên CLI để nhận thiếu, gộp, tráo khoản hoặc nhận chữ đã bỏ ngoài giới hạn đã nêu. Trong miền DOCX, phép so giữ vị trí, đủ mục, hai vế và dòng điểm. Với export thông thường, danh sách có bookmark, comment, perm, proofErr, hyperlink, smartTag, content control, tab, dấu nối, ngắt trình bày cuối đoạn. `w:dir`/`w:bdo` là phần tử chưa hiểu theo mã. Dữ liệu được cấp chưa xác lập chúng xuất hiện thường gặp trong Word/Google Docs của văn bản tiếng Việt để tính P2. [Danh sách phần tử](https://github.com/ducthangho/tra-luat/blob/cc7fac74fd99fa2ecc9a84017357657e2fff0d5f/scripts/tl_core/llm_route.py#L800) · [Đường so](https://github.com/ducthangho/tra-luat/blob/cc7fac74fd99fa2ecc9a84017357657e2fff0d5f/scripts/tl_core/llm_route.py#L1865)

## Findings THEO LỚP

### Lớp `can-tai-nguyen-doc-nguon` [P2] — `scripts/tl_core/llm_route.py:1982`

- **Bất biến.** Sau khi spawn, mỗi ống phải có chủ sở hữu xác định ở mọi trạng thái. Mọi lối thoát bất thường phải thu hồi tài nguyên trong hạn, giữ lỗi gốc và báo phần chưa thu hồi. Ca thu hồi chỉ đạt khi oracle xác nhận tiến trình đích đã kết thúc.
- **Miền và bằng chứng từ mã.**
  1. **Ống chưa ghi sổ.** `Popen` cấp hai ống nhưng `luong` bắt đầu rỗng. `_cho_ket_qua` tạo `Thread` rồi mới ghi mục, lần lượt cho stdout và stderr. Lỗi ở constructor đầu có thể bỏ cả hai ống khỏi sổ. Lỗi constructor thứ hai hoặc thoát ngay khi `start` thứ nhất lỗi bỏ ống stderr chưa được đăng ký. `_thu_hoi` chỉ duyệt các mục đã ghi. Ca ngắt thứ nhất hiện chỉ xác nhận kiểu ngoại lệ, còn ca đòi đóng cả hai ống gây lỗi ở lần `start` thứ hai, sau khi cả hai đã có mục. [Ghi sổ](https://github.com/ducthangho/tra-luat/blob/cc7fac74fd99fa2ecc9a84017357657e2fff0d5f/scripts/tl_core/llm_route.py#L2052) · [Ca sẵn](https://github.com/ducthangho/tra-luat/blob/cc7fac74fd99fa2ecc9a84017357657e2fff0d5f/scripts/tl_core/llm_route_test.py#L2151)
  2. **Quyền đóng ống trong bootstrap và khi thu hồi lỗi.** `Thread.start()` tạo thread trước khi chờ cờ `_started` trong Python 3.13. Nếu ngắt giữa hai bước, cả `join` báo chưa start và `is_alive() == False` đều có thể là trạng thái tạm thời. `_thu_hoi` hiện dùng trạng thái đó để đóng ống. Reader vẫn có thể khởi động sau phép kiểm và tranh khoá với `close`. Luồng đã chạy giữ ống có báo cáo, còn lỗi `kill`/`close` bị nuốt, `is_alive` nằm ngoài hàng rào và ngắt thứ hai trong thu hồi có thể che lỗi gốc. Phân biệt trường hợp tiến trình/nhóm đã biến mất với lỗi thu hồi thật. [Thu hồi](https://github.com/ducthangho/tra-luat/blob/cc7fac74fd99fa2ecc9a84017357657e2fff0d5f/scripts/tl_core/llm_route.py#L2000)
  3. **Ngoại lệ đọc và bằng chứng oracle.** Lỗi `RuntimeError`/`OSError` ở `start` hoặc `wait` đã giữ nguyên thông điệp và cause. Lỗi tương tự từ `read1` trên cả hai ống được gom vào `loi`, nhưng nhánh tổng hợp chỉ giữ tên kiểu, mất thông điệp và cause trước khi tới biên báo lỗi. Ở oracle, `rc=0` với stdout bắt đầu bằng `Z` được coi là đã kết thúc kể cả khi token sai định dạng hoặc stderr có chẩn đoán. Sáu ca hiện có chưa phủ nhánh này. Bảng `DOT_BIEN` thay mã runner trong `llm_route.py`, chưa có đột biến đích cho chính bộ phân loại oracle ở tệp test. [Lỗi đọc](https://github.com/ducthangho/tra-luat/blob/cc7fac74fd99fa2ecc9a84017357657e2fff0d5f/scripts/tl_core/llm_route.py#L2036) · [Tổng hợp](https://github.com/ducthangho/tra-luat/blob/cc7fac74fd99fa2ecc9a84017357657e2fff0d5f/scripts/tl_core/llm_route.py#L2066) · [Oracle](https://github.com/ducthangho/tra-luat/blob/cc7fac74fd99fa2ecc9a84017357657e2fff0d5f/scripts/tl_core/llm_route_test.py#L1920)
- **Hạng P2.** Các đường này ảnh hưởng thời hạn, vệ sinh tài nguyên và chẩn đoán trước khi gọi model, đồng thời làm phép chứng minh thu hồi có thể xanh thiếu căn cứ ở nhánh dự phòng. Chưa có bằng chứng nhận sai nguyên văn từ lớp này.
- **Hint patch.** Đặt hợp đồng vòng đời ở biên `_chay_gioi_han`. Khởi tạo hai mục sở hữu trước spawn, gắn ngay cả hai ống trả về, rồi cho phép dựng reader. Dùng trạng thái truyền quyền có xác nhận và quyền huỷ trước khi reader chạm ống.
  ```text
  _chay_gioi_han:
      chuẩn bị hai mục stdout/stderr và hạn chót, rồi spawn
      gắn cả hai ống vào sổ trước khi dựng reader thứ nhất
      try: đọc/chờ với một hạn chót theo từng mục
      except BaseException as lỗi_gốc:
          báo_cáo = _thu_hoi(p, sổ)
          ánh xạ lỗi vận hành và reader, giữ message/cause
          giữ kiểu timeout/ngắt và gắn báo_cáo

  _thu_hoi:
      thu hồi nhóm/con và reap trong hạn, ghi riêng lỗi từng thao tác
      với mỗi mục, huỷ bàn giao trước I/O hoặc chờ xác nhận/reader trong hạn
      chỉ đóng khi quyền còn ở caller hoặc reader đã trả lại
      quyền chưa xác định thì báo và để reader đóng khi thoát
      giữ lỗi gốc kể cả khi một thao tác cleanup thất bại

  _phan_loai_ps / _trang_thai_pid:
      xác thực rc, một token trạng thái hợp lệ và stderr của nền
      chỉ nhận vắng PID theo quy ước đã chứng minh
      sai định dạng, lỗi đọc hoặc timeout => khong_do_duoc
  ```
  Sổ bao phủ cả hai đầu ống ngay cả khi thiếu reader, reader mới được yêu cầu chạy, đang đọc hoặc đã trả quyền. Không suy quyền đóng từ `is_alive()` trong lúc bàn giao. Giới hạn chờ vẫn áp cho kill/reap/join và trạng thái chưa xác nhận. Giữ ngoại lệ từ reader gắn với đầu ống tại cùng biên, giữ riêng chẩn đoán cleanup cùng nguyên nhân ban đầu.
- **Hint test.** Mở rộng ca sẵn theo các cửa constructor/start đầu và thứ hai, bootstrap đã tạo nhưng chưa trả, `wait` lỗi, reader lỗi ở cả hai ống, reader còn giữ một ống, lỗi `join`/`close`, timeout và ngắt. Khóa để ống an toàn luôn đóng còn ống đã bàn giao chỉ đóng bởi chủ sở hữu, kể cả sau một lỗi cleanup. Đối chứng đủ stdout/stderr và ca cháu kết thúc trên POSIX. Oracle phủ trạng thái hợp lệ, token sai, stderr trong lần rc 0, vắng PID theo quy ước đã xác nhận và lỗi truy vấn. Đột biến bỏ ghi sổ ống thứ hai, đổi trạng thái chưa xác nhận thành an toàn, nuốt cause hoặc đọc lỗi oracle thành kết thúc phải làm đỏ đúng ca.
- **Giới hạn.** Giữ giới hạn đã công bố trên Windows về thu hồi tiến trình trực tiếp. Với bootstrap chưa xác nhận hết hạn, hợp đồng có thể nói rõ “Ghi nhận đầu ống chưa thu hồi trong hạn và chuyển trách nhiệm đóng cho reader nếu nó nhận quyền sau đó.” Chốt quyền sở hữu phải thực thi được câu này.

| Lớp từ lượt 43 | Trạng thái r44 | Hạng mở |
| --- | --- | --- |
| `can-tai-nguyen-doc-nguon` | Vá một phần ở cùng lớp. Ba nhóm biểu hiện còn mở nêu trên. | P2 |
| `lien-ket-bang-chung-review` | Đóng qua readback archive. | 0 |

Đóng 1/2 lớp mở của lượt 43. K1 và lớp ranh giới khoản giữ kết luận theo phạm vi đã kiểm. [Protocol §8.3](https://github.com/ducthangho/tra-luat/blob/cc7fac74fd99fa2ecc9a84017357657e2fff0d5f/docs/PROTOCOL_DA_PHIEN.md#L812)

## Kết quả test và đột biến

Các lệnh chạy trên bản sao có exact SHA/tree nêu đầu verdict, với `core.abbrev=7`, tắt bytecode, từng lệnh dùng TMPDIR riêng. Git 2.43.0, Ruff 0.15.15. Strict manifest chạy trên bản sao sạch trước những lệnh sinh hiện vật. [Nhật ký](#nhat-ky-scratch)

| Lệnh | Trạng thái và mã thoát | Bằng chứng |
| --- | --- | --- |
| `python scripts/tl_core/llm_route_test.py` | `passed`, rc 0 | **64/64** ca, **292/292** đột biến, gồm **195/195** `wp1525_*` trên POSIX. Harness chỉ tính mutant chết bằng `TinHieuChotCa` của ca đích, chạy bản đột biến trong thư mục tạm. |
| `python scripts/tl.py --deterministic workflow-audit --strict --json` | `passed`, rc 0 | `ok=true`, **201/201** lệnh leaf đăng ký, 26 card, 11 nhóm, 60 task, 194 lệnh khả dụng, 0 lỗi/cảnh báo. |
| `python scripts/tl.py --deterministic golden-test --json` | `passed`, head/base rc 0 | Cả hai SHA `ok=true`, **20/20** ca và projection ổn định. Raw **19/20** mỗi bên, do `snapshot_age_s` của `hygiene_sweep_fixture` đã khai báo volatile. JSON báo 0 khóa drift chưa khai. |
| `python scripts/tl.py release-verify RELEASE_MANIFEST.json --strict --json` | `passed`, rc 0 | `ok=true`, **187/187** tệp, 0 tệp thừa. Package hash `ca212280b7be8ea9f08415e1cec5570ca138cf054ed1f689d1cbcdf836f59342` khớp. |
| `python ops/lease_publish.py check --root . ops/leases/llm-khoan-docx-r44-g1-claude.yaml` | `passed` cục bộ, rc 0 | “ĐĂNG ĐƯỢC”, #1525, neo `64b7f2c14776`, hạn 2026-11-27 10:15 UTC. Công cụ ghi `skipped` hai phép kiểm Issue/PR và comment GitHub. |
| `python scripts/tl.py --selftest` | `failed`, head/base rc 1 | Head **1774/1790**, base **1773/1789**, transport **12/12** mỗi bên. 16 ID đỏ giống nhau, delta 0. Hai ca `r1525_llm_khai_niem_tep_docx_cau_truc` và `r380_llm_khai_niem_bien_dau_vao` đều đạt trên head. |
| `python scripts/tl.py --deterministic determinism-audit --strict --json` | `passed`, rc 0 | `ok=true`, **15/15** phép kiểm. |
| `python scripts/tl.py doc-claims-check --strict --json` | `failed`, head/base rc 2 | Cả hai rà 131 tệp, 410 advisory, 1 cờ cứng L2 `SHA_NOT_A_COMMIT` cho `9941d8af52aeede1c78ea4e232fbe9a8d5272033`. Mảng `flags` giống nhau. Mốc này không có object trong kho shallow được giao (`git cat-file -t`, rc 128). |
| Ruff pin/probe qua `loi_ruff_ci()` của `.claude/dev/ci_dang_ky_test.py` | `passed`, rc 0 | `RUFF_CONTRACT 3 []`, 3 bước hợp đồng, 0 lỗi. |
| `python -m ruff check --no-cache --select F --output-format json scripts/tl.py` | Bare lint `failed`, head/base rc 1. Tiêu chí delta 0 đạt. | **12 F821** mỗi bên, danh sách chẩn đoán giống nhau sau khi bỏ đường dẫn tuyệt đối của bản sao. |
| `python -m ruff check --no-cache --select F scripts/tl_core/llm_route.py scripts/tl_core/llm_route_test.py` | `passed`, rc 0 | 0 chẩn đoán. |

Năm mutant mới của r44 bị giết ở `ca_r35_lop_loi`. Chúng đo hàng rào `join`, tránh đóng ống đang bị giữ, phép đóng ống đã an toàn, ánh xạ lỗi vận hành và ghi chú thu hồi. Mutant cũ dựa trên `ident` được thay bằng phép đo theo sổ. Các ca K1, nhãn nhiều vế, bộ đếm Word, XML gốc và fallback cùng chạy trong suite. Không có đột biến ngoài bảng sẵn. [Bảng mutant](https://github.com/ducthangho/tra-luat/blob/cc7fac74fd99fa2ecc9a84017357657e2fff0d5f/scripts/tl_core/llm_route_test.py#L2377) · [Harness](https://github.com/ducthangho/tra-luat/blob/cc7fac74fd99fa2ecc9a84017357657e2fff0d5f/scripts/tl_core/llm_route_test.py#L2789)

Tập ID selftest đỏ khớp byte (`cmp` rc 0), SHA-256 `6c344d8f8a71b854460d8d4badd425904bdd116177ea8b3e14bd2387a2a14505`. Trong đó 14 ca thuộc các nhóm `r973_bootstrap_*`, `wp433_*` và `wp727_tl_gws_refresh` mà prompt ghi nhận với `/tmp/.git` rỗng. Hai ca còn lại là `r226_nguong_l2_troi_theo_abbrev_va_ci_ghim` và `r268_l2_trichotomy_theo_trang_thai_object`. Gate N/N vẫn đỏ. `git diff --check b68bdea HEAD` và `git diff --check 695916e HEAD` đều `passed`, rc 0 và không có chẩn đoán.

## Không đo được

- `not_run` cho ca mới, mẫu export thật của Word/Google Docs, cuộc đua bootstrap luồng thực tế và probe `ps` trên một nền thực sự dùng đường dự phòng. Ca POSIX đã chạy bằng procfs, cùng sáu đầu vào đơn vị của bộ phân loại `ps`. Các nhận định còn lại về bootstrap, đường lỗi và oracle đến từ đọc mã.
- `not_run` cho Windows native, CI/GitHub và model thật. Windows là `required` theo ADR-0060 M3 vì diff chạm bộ chạy subprocess và phân nhánh hệ điều hành. Hai phép GitHub trong lệnh kiểm lease là `skipped` theo công cụ. [ADR-0060 M3](https://github.com/ducthangho/tra-luat/blob/cc7fac74fd99fa2ecc9a84017357657e2fff0d5f/docs/adr/0060-dieu-kien-merge-va-moc-ready.md#L43)
- `not_measured` cho strict doc-claims trên kho đủ object và cho tần suất các phần tử ngoài danh sách của export thực tế. Lượt strict trên bản shallow được ghi `failed` trong bảng.
- Model và effort phục vụ `KHONG_DO_DUOC` từ hồ sơ run tại thời điểm đọc. Mã thoát terminal, hash stdout cuối và delivery receipt thuộc readback sau khi launcher kết thúc. Cây nguồn Executor nằm ngoài phạm vi quan sát của checkout reviewer. [Protocol §8.1–§8.2](https://github.com/ducthangho/tra-luat/blob/cc7fac74fd99fa2ecc9a84017357657e2fff0d5f/docs/PROTOCOL_DA_PHIEN.md#L770)

<a id="nhat-ky-scratch"></a>

## Nhật ký scratch

Bản sao và nhật ký thử nghiệm ở `/tmp/wp1525-r44-review.151ufwoR`. Các cặp `head.*.log` / `head.*.rc` và `base.*.log` / `base.*.rc` khớp tên phép đo trong bảng. `head.selftest.failed-ids` và `base.selftest.failed-ids` lưu danh sách đỏ. `links-41-43.log`, `lease-chain.log`, `pr.outside`, `outside-touched.paths` và `pr.numstat` lưu readback hồ sơ và phạm vi diff. Checkpoint và hồ sơ thực thi ở `../run/09c240cd/` tính từ checkout được giao.

- Diff r44 SHA-256 `8b4e5b743168093bbfc55a4425d6525c0cdfdc648bdccc43c746fc1703002365`.
- Diff toàn PR SHA-256 `8598cefe929464d944d5338c996872b195d2a6ebee63b8d316298acf3d93b695`.
- HEAD/tree đầu và cuối khớp trên checkout reviewer và cả hai bản sao. Diff tracked/index rỗng, rc 0, hash diff rỗng `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`. Checkout reviewer chỉ thêm `.review/VERDICT.md`. Mục ignored `.codex/` đã hiện diện trước review. Hai bản sao có hiện vật test trong ignored, được lưu danh sách ở `*.status.after.log`. Phép đo là snapshot hai mốc.

## Kết luận

**Chưa đủ điều kiện push hoặc merge.** Ngưỡng verdict nội dung do prompt giao là 0 P0/P1. Ứng viên vẫn còn một lớp P2 theo ngưỡng merge của chủ kho. Selftest N/N và doc-claims strict vẫn đỏ trong môi trường đo, đồng thời còn thiếu bằng chứng Windows/CI trên exact head. Đây là lời gọi thứ **45/45**, chạm điểm dừng của lease r44 khi còn P2. [ADR-0060](https://github.com/ducthangho/tra-luat/blob/cc7fac74fd99fa2ecc9a84017357657e2fff0d5f/docs/adr/0060-dieu-kien-merge-va-moc-ready.md#L32) · [Lease r44](../../../../../ops/leases/llm-khoan-docx-r44-g1-claude.yaml)

P0_mo: 0
P1_mo: 0
P2_mo: 1
P3_mo: 0
VERDICT: APPROVE
