# Verdict packet #1525 r45 lượt 45 — Codex

reviewed_sha: 32cf3ad5b10f32eff31c10ce64a13e89cb4fd99d
reviewed_tree: 691169100d374cdb68307a8eb0331a705218923d
base_sha: 64b7f2c14776d5d0e1d34a6be4725490956f5bec

**APPROVE theo ngưỡng verdict offline của prompt. Chưa đủ điều kiện push hoặc merge.**

Reviewer `openai_codex / codex_cli / machine`, run `0427ee0c6da24df7a0706cd81a6563f2`. Executor theo lease `claude / claude_code / machine/local`. Linux x86_64, Python 3.13.18, Git 2.43.0, Codex CLI 0.172.0, sandbox `workspace-write` với mạng hạn chế.

## Đối chiếu lượt 44 và đặc tả r45

| Mục | Trạng thái | Bằng chứng |
| --- | --- | --- |
| Preflight | Khớp cục bộ | Checkout detached, tracked/index sạch, `core.abbrev=7`. Lease #1525 r45 g1, `sensitive`, lời gọi 46/46, đúng spec hash và write set 239 đường dẫn. |
| Lượt 44, §2.47 · Sổ và bàn giao hai ống | **ĐÃ VÁ THẬT** với lỗi dựng reader và tranh quyền lúc reader khởi động muộn. | Sổ có hai mục trước `Popen`. Cả hai ống được gắn trước constructor và `start()` đầu tiên. Cùng khóa quyết định ai chạm ống. Nếu thu hồi thắng, reader đến muộn rút trước `read1`. Nếu reader thắng, thu hồi đợi và chỉ đóng sau khi reader đánh dấu xong. Các ca có sẵn đo lỗi constructor, lỗi ở hai lần start, ngắt và reader thật còn giữ ống. `llm_route.py:1982,2025,2050`. |
| Lượt 44, §2.43–§2.47 · Thu hồi và lỗi đọc | **VÁ MỘT PHẦN**. | Lỗi đọc giữ nội dung và `__cause__`. Lỗi kill/wait/join/close trong lời gọi được ghi theo bước. Một số bước chuẩn bị và bàn giao nằm ngoài hàng rào. Ống đang đọc sau khi hết ngân sách có ghi chú, nhưng reader không có bước đóng khi thoát muộn. Chi tiết trong lớp `can-tai-nguyen-doc-nguon`. |
| Lượt 44, §2.47 · Oracle POSIX | **VÁ MỘT PHẦN**. | Tra cứu có timeout, lỗi kèm chẩn đoán và token chứa đệm bên trong bị loại. Mẫu cho phép vẫn chấp nhận chuỗi ký tự tùy ý bắt đầu bằng `Z`. Bảng tự kiểm 10 ca đo bộ phân loại phía test. `DOT_BIEN` chỉ đột biến runtime theo hợp đồng r45. `llm_route_test.py:1920,1958,2861`. |
| Lượt 34–43, §2.38–§2.46 · `ranh-gioi-khoan` và K1 của #1514 | **ĐÃ VÁ THẬT** trong miền hiện hành. | Hai tuyến thô dùng một danh sách đầu dòng, chung span thân, máy trạng thái, từ nối và luật dấu kết. Nguồn có số từ chối điểm chữ/dấu đầu dòng và dòng tiếp “là”. Nguồn mất số đòi hai vế khác rỗng. Chốt nhiều vế xét toàn phần đầu đến từ nối cấp khoản, gồm các dấu kết ngoài nhóm, ngoặc ở đầu thân và nháy ở đầu thân. Ca hai phía miền chạy trong `ca_r35_lop_loi`. `PHAM_VI_KIEM` ghi phía bị từ chối, phía có thể nhận và giới hạn nhãn số trùng khoản. Ba giới hạn chủ kho chốt được giữ. `llm_route.py:587,643,1679,1689,1785,1803,1844`. |
| Lượt 1–23, §2.1–§2.18 và §2.22–§2.27 · Vùng Điều, đếm số, điểm và fallback | **HẾT ĐỐI TƯỢNG** với đoán điểm cắt, đếm qua bảng, nhập điểm gõ tay và fallback `KhongCauTruc`. **ĐÃ VÁ THẬT** với các chốt lịch sử còn hiệu lực đã đối chiếu. | Toàn bộ thân tệp một Điều được kiểm cho tới EOF. Tiêu đề đúng số và toàn đoạn, chặn bảng/khối lạ, tiêu đề thứ hai và đoạn có số trống. Chỉ nhận một câu dẫn chuẩn trước khoản đầu. `start` mặc định 0, `startOverride` theo cấp, reset các cấp thấp hơn khi cấp cha tăng, đếm riêng theo `numId` và chặn đổi danh sách, nhảy cấp, giá trị bất hợp lệ. Chỉ điểm cấp con trong danh sách mới được ghép. DOCX thiếu cấu trúc dừng rc 2. `llm_route.py:932,1129,1485,1540,1603,1663`, `ops_misc.py:3037`. |
| Lượt 1–35, §2.4–§2.37 · Markup, style, ký tự | **ĐÃ VÁ THẬT** với các biểu hiện lịch sử đã đối chiếu, gồm `ranh-gioi-ky-tu`. | Đọc XML gốc theo QName. Bỏ `del/moveFrom` và gạch còn hiệu lực, giữ `ins/moveTo`. Tính gạch đơn/kép riêng, kiểm sửa dấu đoạn, mốc move, `mc:`, trường đơn trị, style và khóa nội bộ. Chốt ký tự đo trước bỏ đoạn rỗng/chọn tiêu đề, cả trên văn bản thô. Chặn số mũ, giữ quy tắc một BOM và đối chứng chữ ngoài miền trong mẩu bị bỏ. `llm_route.py:748,1033,1201,1256,1500,1562,1703`. |
| Lượt 18–20, §2.21 U2, §2.22 V3, §2.23 W1/W3 và phần số hiệu của W2 | **GIỚI HẠN ĐÃ KHAI**. | Tuyến số hiệu vẫn dùng `tl extract --markup-strict` và từ chối tín hiệu chạm trần export. Làm sạch đầu ra cache, cắt Điều theo dòng mở đầu, gạch qua style, tab/ngắt và false reject ở strict nằm trong giới hạn đã chấp thuận. `llm_route.py:2097`, `docs/GOI_AGENT_DA_NEN.md:412`. |
| Lượt 34–43, §2.37–§2.45 · Ngân sách nguồn ngoài vòng đời | **VẪN ĐÓNG** cho các biểu hiện lịch sử. | Chốt byte/chữ/số thô, XML giới hạn độ sâu và nút, style có bộ nhớ theo hậu tố, chặn trần cấp/nhãn/chữ trước dựng. ZIP đo cùng handle, đếm thư mục trung tâm trước mở, đọc locator ZIP64 tuyệt đối, từ chối mã hóa/codec ngoài miền và giữ biên lỗi ZIP hẹp. `llm_route.py:550,696,1090,1401,1428,1440`. |
| §1 và §3 · Đối chiếu nguyên văn và CLI | **ĐẠT** trên các ca hiện có. | Mục thứ i phải có đúng số và hai vế của khoản i, giữ xuống dòng điểm, đánh dấu thiếu mục và chỉ ghi `--out` khi qua. DOCX chỉ dò từ nối trong đoạn đầu khoản. `can_nguoi_duyet: true` được giữ ở cả hai tuyến. Giữ model route, schema và CLI hiện hành. `llm_route.py:1865,2127`, `ops_misc.py:3131,3144,3179`. |
| Lượt 39–43 · P3 lịch sử | **ĐÃ VÁ THẬT** ở phạm vi cũ của ghi chú write set, mô tả quy tắc style, kết tệp và liên kết lượt 41–43. **TÁI MỞ** liên kết ở hồ sơ lượt 44 và hướng dẫn ở các chỗ nêu dưới. | `git diff --check` sạch trên bản vá và toàn PR. Readback lượt 41–43 khớp SHA/prompt, các đích mở được cục bộ, gồm một đích thư mục ở lượt 41. Lượt 44 giữ 40 liên kết tương đối của vị trí `.review/` sau khi lưu vào archive. |
| Write set và bia mộ | **KHỚP**. | 10/10 đường dẫn của bản vá `cc7fac7..32cf3ad` thuộc lease. Diff tách master `695916e..32cf3ad` có 282 đường dẫn, 47 ngoài lease là nội dung lịch sử #1514 đã giống byte ở `2c91832`. Kiểm 90/90 chiều `thay_the_cho`/`da_bi_thay_the`, 46/46 hash đặc tả từ #1514 r9 đến #1525 r45. r45 còn hiệu lực đến 10:39 UTC và chưa có successor. |

### Phạm vi xác minh nguyên văn và khả năng đọc DOCX

Đọc mã và các ca hiện có chưa xác lập cửa P0/P1 trên CLI cho bỏ, gộp, cắt, tráo khoản hoặc nhận lại chữ đã bỏ ngoài các giới hạn chủ kho đã khai. Các chốt nhận biết DOCX đo cửa đoạn/khối, số Word và phần chữ còn hiệu lực, rồi phép so dùng toàn thân từng khoản. Đường thô vẫn có ba vùng giao đã được công bố. Nhãn dính thân, nhãn chỉ ngăn bằng đệm và nhãn số trùng số khoản cần người duyệt ranh giới.

Danh sách phần tử đã nhận bookmark/comment/perm/proofErr, hyperlink, custom XML, content control, tab, no-break hyphen, soft hyphen và ngắt trình bày cuối đoạn. `w:dir`/`w:bdo` là các ví dụ phần tử chưa xử lý theo mã, nhưng không có mẫu export Word/Google Docs trong hồ sơ này xác lập độ phổ biến của chúng cho văn bản luật tiếng Việt. Chặn bảng, phần tử tương thích, trường, hình, markup không giải được, ngắt mềm và Strict đều nằm trong miền đã khai. Chưa xác lập P2 chặn oan một dạng export thường gặp ngoài giới hạn đó.

## Findings THEO LỚP

### Lớp `can-tai-nguyen-doc-nguon` [P2] — `scripts/tl_core/llm_route.py:1985`

- **Bất biến.** Mỗi ống được cấp từ spawn có một chủ sở hữu và đường đóng hữu hạn khi không còn I/O. Mọi lỗi sau khi nhận tiến trình đều được thu hồi trong ngân sách, giữ lỗi gốc và báo tài nguyên chưa thu hồi. Oracle chỉ xác nhận cháu đã kết thúc khi trạng thái có bằng chứng dương.
- **Miền và bằng chứng từ mã.**
  1. **Spawn và chuẩn bị bàn giao.** `Popen` nằm ngoài `try` ở dòng 1985, còn hai mục `ong` ban đầu là `None`. Một ngắt sau khi `Popen` đã trả nhưng trước khi vào vùng bảo vệ có thể bỏ đường thu hồi. Một ngắt trong câu gán hai mục ở dòng 1988 có thể để lại mục chưa gắn. `_thu_hoi` bỏ qua mục `None` dù ống có trên `p.stdout`/`p.stderr`. Lỗi constructor/start và quyền I/O lúc reader tới muộn **đã** có chốt sau khi gắn sổ. `Thread.start()` và `Popen` vẫn là lời gọi đồng bộ không nhận thời gian còn lại. Mức trễ thật ở bootstrap ngoài phạm vi đo của ca sẵn.
  2. **Kết thúc và hạn thu hồi.** Khi reader đã giữ ống nhưng còn chạy lúc hết ngân sách, dòng 2040 rời mục. Khi reader thoát muộn, `finally` ở dòng 2069 chỉ đánh dấu `xong`. Không có bên đóng tường minh sau thời điểm đó. Chẳng hạn trên POSIX một ống có thể trả EOF muộn sau lỗi thu hồi nhóm, hoặc trên Windows sau khi tiến trình cháu kết thúc. Traceback lỗi còn giữ `so` và `p`, nên không thể lấy việc giải phóng ngầm theo vòng đời object làm bằng chứng đã đóng. Đường thành công cũng dựa vào vòng đời object thay cho đóng ống tường minh. Biên xử lý lỗi reader bắt đầu sau lúc giành khóa và chỉ bắt `Exception`. Lỗi ở bàn giao hoặc `BaseException` từ reader không có bản ghi hoàn tất lỗi để caller phân biệt với EOF. Đường lỗi lúc `read1` thuộc kiểu vận hành đã giữ message và cause như r45 yêu cầu.
  3. **Hàng rào thu hồi.** `buoc` chỉ bọc phần gọi callback. Phần chuẩn bị như lấy mốc thời gian ở dòng 2020 và duyệt giữa các bước ở ngoài hàng rào, trong khi dòng 1991 gọi `_thu_hoi` trực tiếp trong lúc đang xử lý ngoại lệ gốc. Ngắt lần hai ở đây có thể che ngoại lệ gốc và bỏ phần thu hồi còn lại. Việc bỏ qua `ProcessLookupError` áp vào cả wait, join và đóng ống, trong khi chỉ lỗi định danh tiến trình/nhóm đã biến mất ở bước gửi tín hiệu chứng minh hậu điều của bước đó.
  4. **Oracle POSIX.** `_phan_loai_ps` nhận toàn bộ dải chữ cái và dấu qua biểu thức `[A-Za-z<+]+`, rồi dùng ký tự đầu để quyết zombie. Một từ nhiều chữ bắt đầu bằng `Z` nhưng có hậu tố ngoài ngữ pháp cờ của `ps stat` vẫn được đọc là đã kết thúc. Bảng 10 ca chỉ chặn rác có khoảng trắng bên trong và chẩn đoán stderr có chữ. Nhánh `rc=1` với stdout/stderr rỗng được nhận sau phép dò PID sống, vốn mới xác nhận cú pháp hỏi PID có thật. Đường procfs tách token chưa có nhánh `khong_do_duoc` cho bản ghi cụt hoặc không phân tích được. `scripts/tl_core/llm_route_test.py:1920,1931,1958`.
- **Hạng P2.** Các đường này làm hụt thu hồi hoặc chẩn đoán trước model, và làm ca kiểm thu hồi có thể xanh khi tín hiệu dự phòng không đủ. Chưa xác lập đường nhận sai nguyên văn từ lớp này. Giữ một lớp như lượt 44 vì runtime và oracle cùng bảo vệ hậu điều thu hồi.
- **Hint patch** (phác thảo, chưa áp). Đặt nhận tiến trình, đăng ký ống và chuyển quyền vào cùng biên sở hữu của `_chay_gioi_han`. Phân biệt rõ hoàn tất đọc với đã đóng ống bằng trạng thái mỗi mục.

  ```text
  _chay_gioi_han:
      dựng sổ và hạn chót trước khi spawn
      trong biên sở hữu: nhận p, gắn hai ống, đọc/chờ
      mọi lối thoát sau spawn:
          hoàn tất mục chưa gắn từ p, nếu đã nhận p
          chạy thu hồi có hạn và giữ lỗi gốc nếu chính cơ chế thu hồi lỗi
          báo từng mục chưa đóng, rồi chuyển lỗi theo kiểu và cause gốc

  reader sau khi tranh quyền:
      nếu quyền thuộc thu hồi: rút trước I/O
      nếu được quyền: ghi EOF hoặc lỗi, tự đóng ống trong finally
      công bố kết quả đọc và đóng qua cùng mục sổ

  _thu_hoi:
      thử kill nhóm/con và reap theo hạn
      chỉ coi ProcessLookupError ở bước gửi tín hiệu là đích đã biến mất
      với từng ống: nếu chưa giao thì nhận rồi đóng
      nếu reader có quyền thì chờ kết quả có hạn, quá hạn thì báo và reader giữ trách nhiệm đóng
      giữ tín hiệu ngắt trong lúc chạy chuỗi thu hồi, giao lại lỗi gốc khi chuỗi kết thúc

  oracle POSIX:
      kiểm đúng một trạng thái chính và các cờ hợp lệ của backend
      chỉ chấp nhận quy ước PID vắng ở backend có đối chứng tương ứng
      lỗi định dạng, lỗi quan sát và thiếu capability trả khong_do_duoc
  ```

  Khi có hợp đồng deadline cho cả bootstrap, dùng cơ chế spawn/start có trạng thái sẵn sàng và thời gian chờ hữu hạn, với chủ sở hữu tài nguyên rõ ngay cả khi caller hết hạn. Nếu nền không bảo đảm qua ranh giới cấp phát của thư viện, đặc tả nên ghi giới hạn cụ thể của lúc chưa nhận handle. Giữ giới hạn Windows chỉ giết tiến trình trực tiếp. Chốt phần trong quyền kiểm soát bằng câu “Ống do reader giữ quá hạn được báo ngay, reader đóng khi kết thúc đọc.”
- **Hint test.** Dùng chung nhóm ca hai ống: lượt sạch, gắn sổ một phần, lỗi constructor/start ở mỗi vị trí, reader được gọi muộn, reader giữ ống quá hạn rồi thoát, lỗi đọc và lỗi chốt quyền, lỗi và ngắt trong từng bước thu hồi, kể cả khoảng giữa hai thao tác. Xác nhận lỗi gốc, số ống đóng đúng chủ và lỗi nào còn tồn. Giữ ca cháu POSIX và bảng kiểm oracle gồm cờ trạng thái hợp lệ, token sai dù bắt đầu bằng ký tự zombie, bản ghi cụt, PID vắng có đối chứng và lỗi truy vấn. Mutant bỏ gắn ống hoặc bỏ đóng bên reader, làm ngắt che lỗi gốc, bỏ kill nhóm hay biến dữ liệu hỏng thành “đã kết thúc” phải làm đỏ đúng ca. Bảng oracle tự kiểm vẫn thuộc phía test theo §2.47.

### Lớp `lien-ket-bang-chung-review` [P3] — `ops/acceptance/llm-khoan-docx/r1/review-44-codex/VERDICT.md:12`

- **Bất biến.** Khi verdict đổi chỗ từ `.review/` sang archive, các đích mã/tài liệu mở đúng blob và dòng tại `reviewed_sha`, đích hồ sơ tồn tại trong gói, và đích scratch gắn với neo có mô tả.
- **Miền và bằng chứng.** Lượt 41–43 giữ các dạng đích theo `LIEN_KET.md`. Lượt 44 trên `cc7fac74fd99fa2ecc9a84017357657e2fff0d5f` có 43 liên kết tính cả lặp. Đọc theo vị trí lưu chỉ 3 neo nội bộ mở được. 40 đích dạng `../scripts/`, `../docs/` hoặc `../ops/` bắt đầu từ sai thư mục, gồm nguồn mã cho finding, lease, prompt/biên nhận tham chiếu và điều kiện merge. SHA-256 của prompt lưu vẫn khớp `run.json` và run neo đúng head. Hạng P3 vì lỗi nằm ở cách truy cập hồ sơ đã lưu.
- **Hint patch.** Áp một bước chuyển đích lúc lưu mọi lượt kể từ 41. Giải đích theo vị trí gốc, viết lại mã/tài liệu bằng blob tại SHA review, dùng đường tương đối đúng cho hồ sơ, giữ `PROMPT.md` và `run.json` đồng gói, viết đích scratch thành neo nội bộ. Giữ nguyên câu chữ và xử lý hash/biên nhận theo quy tắc archive.
- **Hint test.** Readback cả khối liên kết từ vị trí archive, kiểm blob OID, phạm vi dòng, đường dẫn, tệp đồng gói và neo. Đối chứng có verdict hợp lệ và mutant bỏ bước chuyển gốc khi lưu. Mutant phải làm đỏ các đích repo dù prompt và SHA vẫn khớp.

### Lớp `huong-dan-docx` [P3] — `docs/GOI_AGENT_DA_NEN.md:418`

- **Bất biến.** Hướng dẫn và mô tả bộ đọc nói đúng điều kiện cuối cùng của từng tuyến, gồm trường hợp phần dữ liệu qua chốt đầu nhưng bị chốt sau từ chối.
- **Miền và bằng chứng.** Hướng dẫn dòng 418–421 nêu một dấu mở `‘` và từ ASCII dài ít nhất hai ở danh sách nhận đầu dòng. Đoạn 376–378 và `_dong_mo_ho` lại từ chối `‘` cho cả dòng. Điều kiện ASCII cũng cần từ đầu không phải một chữ lặp theo `dau_dong_cho_phep` dòng 665. Ở phía DOCX, docstring `_doan_trong` và chú thích bộ đếm dòng 1524 còn nói duyệt đoạn trong bảng để đếm, trong khi nhánh `tbl` chỉ phát dấu bảng và r7 chặn cả tệp. Công bố quy tắc style đã sửa ở r40 vẫn khớp. Hạng P3 vì đây là sai khác mô tả. Các chốt runtime hiện hành vẫn từ chối đúng theo miền đã chốt.
- **Hint patch.** Dùng mục hướng dẫn đầu dòng ngay cạnh các luật thô làm một mô tả đầy đủ, nêu từ ASCII không lặp một chữ và danh sách dấu sau cả chốt cân bằng. Cập nhật docstring cùng chú thích DOCX thành “đoạn ngoài bảng, cả tệp bị chặn khi có bảng”. Giữ các dẫn chiếu về miền fail-closed hiện hành.
- **Hint test.** Đọc đối chứng câu hướng dẫn với ca sẵn có ở hai phía miền và ca chặn bảng. Đột biến tài liệu bỏ điều kiện chữ lặp hoặc đưa một dấu bị chặn vào danh sách nhận phải bị phát hiện khi đối chiếu chốt cuối và bảng ví dụ.

## Kết quả test và đột biến

Lệnh chạy trong bản sao detached có exact SHA/tree nêu trên, với `core.abbrev=7`, tắt bytecode và TMPDIR riêng từng lệnh. Baseline là `64b7f2c14776d5d0e1d34a6be4725490956f5bec`, tree `0cc14e79cecd2ce44bc4dc6cff92cadb31fd7ee4`. Strict manifest chạy trên bản sao ứng viên sạch trước các phép sinh hiện vật.

| Lệnh | Trạng thái và mã thoát | Bằng chứng |
| --- | --- | --- |
| `python scripts/tl_core/llm_route_test.py` | `passed`, rc 0 | **64/64** ca và **295/295** đột biến bị giết, gồm **198/198** `wp1525_*` trên POSIX. Harness tạo đột biến trong TMPDIR, đòi neo duy nhất và chỉ tính khi ca đích ném `TinHieuChotCa`. Ca A4 kiểm đủ 8 khoản của fixture Điều 3 và ba đầu ra đã lưu, mỗi đầu ra **8/8**. |
| `python scripts/tl.py --deterministic workflow-audit --strict --json` | `passed`, rc 0 | `ok=true`, **201/201** lệnh leaf đã đăng ký, 26 card, 11 nhóm, 60 task, 194 lệnh khả dụng, 0 lỗi/cảnh báo. |
| `python scripts/tl.py --deterministic golden-test --json` | `passed`, head/base rc 0 | Hai SHA cùng `ok=true`, **20/20** ca, **20/20** projection ổn định. Raw head **20/20**, base **19/20**. Ca `hygiene_sweep_fixture` ở base khai `snapshot_age_s` volatile và có `diff={}` sau chiếu. |
| `python scripts/tl.py release-verify RELEASE_MANIFEST.json --strict --json` | `passed`, rc 0 | `ok=true`, **187/187** tệp kiểm, 0 tệp thừa. Package hash `35e5cbae5c5917b18cd7efabe2d2d6e8200719efd44d579de8fbab6e03dde086` khớp. |
| `python ops/lease_publish.py check --root . ops/leases/llm-khoan-docx-r45-g1-claude.yaml` | `passed` cục bộ, rc 0 | “ĐĂNG ĐƯỢC”, #1525, neo `64b7f2c14776`, hết hạn 10:39 UTC. Hai phép Issue/PR và comment GitHub được lệnh báo `skipped`. |
| `python scripts/tl.py --selftest` | `failed`, head/base rc 1 | Head **1774/1790**, base **1773/1789**. Transport **12/12** mỗi bên. Cùng 16 ID đỏ, `cmp` rc 0. Head đạt `r1525_llm_khai_niem_tep_docx_cau_truc` và `r380_llm_khai_niem_bien_dau_vao`. |
| `python scripts/tl.py --deterministic determinism-audit --strict --json` | `passed`, rc 0 | `ok=true`, **15/15** phép. |
| `python scripts/tl.py doc-claims-check --strict --json` | `failed`, head/base rc 2 | 131 tệp và 410 advisory mỗi bên. Mảng `flags` đồng nhất: một cờ L2 `SHA_NOT_A_COMMIT` cho `9941d8af52aeede1c78ea4e232fbe9a8d5272033`. Kho được giao là shallow, `git cat-file -t` rc 128 cho object này. |
| `loi_ruff_ci()` từ `.claude/dev/ci_dang_ky_test.py`, qua `python -B -c` | `passed`, rc 0 | Pin/probe workflow `RUFF_CONTRACT 3 []`. |
| `python -m ruff check --no-cache --select F --output-format json scripts/tl.py` | `failed` bare lint, head/base rc 1. Tiêu chí delta 0 đạt. | Ruff 0.15.15. **12 F821**, 0 F401 mỗi bên. JSON chuẩn hóa bỏ đường dẫn tuyệt đối khớp, `cmp` rc 0. |
| `python -m ruff check --no-cache --select F scripts/tl_core/llm_route.py scripts/tl_core/llm_route_test.py` | `passed`, rc 0 | 0 chẩn đoán. Phép mở rộng thêm `ops_misc.py` đỏ (rc 1). Lint riêng module re-home này có **411 F821 và 1 F811** trên cả head lẫn base (rc 1 mỗi bên). |
| `git diff --check cc7fac7 HEAD` và `git diff --check 695916e HEAD` | `passed`, rc 0 mỗi lệnh | Không có chẩn đoán khoảng trắng/kết tệp. |

Sáu đột biến liên quan trực tiếp r45 chạy qua `ca_r35_lop_loi`: bỏ đóng ống, dời gắn ống sau constructor, đóng ống khi reader còn giữ, mất cause, nuốt chẩn đoán thu hồi và báo nhầm tiến trình đã biến mất. Bảng 10 đầu vào cho oracle đi cùng ca nhưng không đột biến mã phía test. Ca luồng giả chưa giành quyền chỉ kiểm nhánh caller đóng, vì stub không thực thi target sau lúc đóng. Ca reader thật bị chặn kiểm rằng ống chưa bị đóng tại thời điểm timeout và có ghi chú. Sau khi mở khóa cho reader thoát, ca chưa kiểm đóng muộn. Không có đột biến ngoài bảng có sẵn.

Tập 16 ID selftest đỏ có SHA-256 `e25d2f470c310f96910f047b2ac28dcc04084fa56471970a55f00efea4b3b43b`. Nhóm 14 ca `r973_bootstrap_*`, `wp433_*`, `wp727_tl_gws_refresh` khớp hiện tượng môi trường `/tmp/.git` rỗng đã nêu trong prompt. Hai ca còn lại là `r226_nguong_l2_troi_theo_abbrev_va_ci_ghim` và `r268_l2_trichotomy_theo_trang_thai_object`. Tập đỏ không đổi giữa base và head, gate N/N vẫn đỏ.

## Không đo được

- `not_run` cho đua bootstrap/đóng muộn hoặc ngắt lần hai tại các cửa mới, và cho probe `ps` trên POSIX thật không có procfs. Linux đo ca thu hồi cháu bằng procfs và 10 đầu vào oracle sẵn có. Các biểu hiện ngoài bộ ca được kết luận từ đọc mã.
- `not_run` cho mẫu export mới của Word/Google Docs và tần suất phần tử ngoài danh sách trong tài liệu luật tiếng Việt. `not_measured` cho doc-claims strict trên kho có đủ object.
- `not_run` cho Windows bản địa và CI/GitHub trên exact head, cũng như model thật hoặc LIVE. Windows là `required` theo ADR-0060 M3 vì diff chạm `subprocess` và nhánh theo hệ điều hành. Hai phép GitHub của kiểm lease là `skipped` theo công cụ. Ref cục bộ của bản sao chỉ dùng để xác nhận commit được giao. Trạng thái remote hiện hành và điều kiện push từ xa thuộc ngoài phép đo.
- Model và effort phục vụ `KHONG_DO_DUOC` từ hồ sơ launcher tại thời điểm ghi. Hồ sơ run còn `dang_chay`; rc terminal, stdout hash cuối và delivery receipt cần readback sau khi launcher kết thúc. Sandbox khai từ môi trường phiên. Kho nguồn của Executor nằm ngoài cửa quan sát.

<a id="nhat-ky-scratch"></a>

## Nhật ký scratch và readback

- Nhật ký ở `/tmp/wp1525-r45-review.TTSKSE9a/`, gồm log và rc từng phép `head.*`/`base.*`, diff raw, numstat, tập lỗi selftest và readback lease/absent path/link. Đích thư mục ở lượt 41 được xác nhận tồn tại riêng với `test -d`, rc 0. `chain-archive.log` phân loại đích này theo phép kiểm tệp. Lượt 41–43 lần lượt đọc được **78/78**, **80/80** và **61/61** đích sau đối chiếu đó.
- Spec blob `b6fa44c64a59c21346674696b845791391055eeb` có SHA-256 `6c252e59f89b8eb06e15fc705fd0e425c5651ead006462e34e43c09b2c6c2e95` khớp lease. Write set SHA-256 `03a08c0f80297ea54cf3899318376e3f1ad88deee9750150f581118629be141d` khớp. Prompt snapshot SHA-256 `e8f45e991b459869ddc5a455d937da75814b21a51882e0bec697c7109dc51924` khớp `run.json`. Scope r45 diff SHA-256 `c68c3455baa8eaa7707aff19cfe12b72b8ea9303cef41ed8e99872c41b6835f5`. Diff toàn PR SHA-256 `b24220bc70130349250dcbbe6355afd082572731164b063e188e018b682774bb`.
- Exact head/tree được đọc lại cuối lượt trên checkout bàn giao và hai bản sao đo. Diff tracked/index rỗng ở cả ba, SHA-256 byte rỗng `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`. Checkout reviewer có duy nhất tệp đầu ra `.review/VERDICT.md` mới và thư mục ignored `.codex/` rỗng đã có. Các trạng thái ignored của bản sao test được lưu riêng. Snapshot đối chiếu hai mốc, giới hạn ở các thay đổi quan sát được.

## Kết luận

**Đóng 0/1 lớp còn mở từ lượt 44.** Lớp vòng đời tài nguyên đã thu hẹp nhưng còn P2. Hai lớp P3 liên quan hồ sơ lưu và mô tả hành vi. Theo ngưỡng verdict nội dung được giao (0 P0/P1), kết luận là **APPROVE**. Theo điều kiện 0 P0/P1/P2/P3 của chủ kho và ADR-0060 M1/M3/M5/M12, ứng viên **chưa đủ điều kiện push hoặc merge**. Cổng selftest N/N và doc-claims strict chưa xanh, Windows và CI chưa có bằng chứng exact SHA. Đây là lời gọi **46/46**, chạm điểm dừng của lease r45.

P0_mo: 0
P1_mo: 0
P2_mo: 1
P3_mo: 2
VERDICT: APPROVE
