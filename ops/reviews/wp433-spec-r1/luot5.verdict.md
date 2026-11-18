## Review độc lập lượt 5 · Issue #433

**Còn P2 ở cả hai packet.** Packet 1 thiếu phép nghiệm thu trước land cho cam kết từ chối symlink ở tệp cuối của jar NLM. Packet 2 có tiêu chí quyền tệp mâu thuẫn với phạm vi Windows. Cả hai còn một khe trong hợp đồng chẩn đoán một dòng.

Review chỉ đọc trên Linux, Python 3.13.18, trong phiên Codex họ OpenAI qua API. `HEAD` là `641108cb997872b0ef2a277ea9c8faf8b82532bb`, trùng ref `master` cục bộ, tree `e6c7c50863421e32cac4f5f1894f176d758375b1`. Checkout ở detached HEAD. Diff tracked và index đều sạch, chín bản đặc tả là untracked. Các phép thử dùng dữ liệu giả trong RAM, không gọi mạng hoặc đọc secret thật. Các kết luận đóng dưới đây áp dụng ở mức đặc tả. Chưa có mã ứng viên để chạy fragment, đo `numstat` hoặc kiểm hành vi native Windows.

## Đối chiếu finding lượt 4

| Finding | Packet | Trạng thái | Bằng chứng |
|---|---|---|---|
| P2 · NUL trong biến môi trường | 1 | Đóng | M3(0b) kiểm cả hai trường trước mọi phép gán. N3(7) kiểm cả hai biến giữ giá trị cũ và config giữ byte. `python3 -B` với `x\x00y` tái hiện `ValueError: embedded null byte`. Hai đột biến phân biệt bỏ kiểm NUL với gán token quá sớm. |
| P2 · `db_reparse_moi_thu` sống | 1 | Đóng | N6(5) dùng đối chứng `FILE_ATTRIBUTE_DIRECTORY = 16`. Phép bit với `REPARSE_POINT = 1024` trả false cho 16 và true cho 1024. Đột biến dùng `bool(attributes)` trả true cho cả hai, nên làm đỏ `khong_bit`. |
| P2 · Nhánh định dạng W1/W3 | 1 | Đóng | `git show HEAD:scripts/tl_gws.py` xác nhận W1 in cảnh báo ở dòng 1652 rồi trả 1. W3 kiểm kiểu và rỗng ở 1955, trả lý do nguyên văn ở 1956. M2 và N3(8) giữ hai nhánh, đồng thời giữ W2 bỏ qua jar falsy. |
| P2 · rc 4 khi ghi bootstrap bị từ chối | 1 và 2 | Đóng | Packet 1 N8(2) chạy lại đúng ca W2 bị từ chối. Packet 2 N7(1) dùng ca W4 bị từ chối. Chạy đuôi `cmd_bootstrap` trích từ AST của base với `degraded=True` và agent giả cho rc 1/4 tùy cờ, luôn có một dòng `agent_creds:`. Vế kết hợp với từ chối ghi sẽ được đo khi có mã. |
| P2 · Đường Windows theo ổ | 2 | Đóng | M1 nêu rõ hai dạng phải từ chối và N2w có đối chứng. `ntpath` 3.13.18 cho `D:fake → ('D:', 'fake'), False`, `\fake → ('', '\\fake'), False`, `D:\fake → ('D:', '\\fake'), True`. `join` với `C:\cwd` giữ `D:fake` nhưng biến `\fake` thành `C:\fake`. Vì vậy phải phân loại đường thô trước khi ghép cwd, theo `splitdrive` và dấu phân cách đầu phần đuôi. |
| P3 · §7 khai quá độ phủ | 1 | Đóng | §7 phân biệt ca config `dich == goc`, ca thành phần thư mục, reparse giả lập, hai chuỗi Git chuyển tiếp và đột biến tệp cuối chuyển tiếp. Khoảng trống nghiệm thu còn lại được nêu riêng bên dưới. |

## Finding mới

| Mức | Packet | Finding và điều kiện đóng |
|---|---|---|
| **P2** | **1**, liên quan 2 | **Cam kết từ chối symlink ở lá jar chưa có phép nghiệm thu trước land.** M1/M2 yêu cầu kiểm đến chính `dich`. N6(2) chỉ kiểm trường hợp `dich == goc`, N6(3) kiểm thư mục trung gian. Một vòng lặp bỏ đúng tiền tố cuối khi tuple khác rỗng vẫn qua hai ca đó. Ghi nguyên tử vẫn giữ byte tệp được trỏ tới nhưng có thể thay chính symlink bằng tệp thường và báo thành công. Packet 2 N3 bắt được lỗi chung sau khi packet 1 land, qua W4; nó cũng không bắt được lỗi riêng khi caller NLM dựng tuple thiếu lá. Giữ một ca W1 tối thiểu ngay ở packet 1, đòi rc từ chối, đúng lý do, symlink còn nguyên và tệp được trỏ tới giữ byte. Có thể để đột biến đầy đủ ở packet 2 nếu cần giữ trần. [Packet 1 M1 và N6](ops/specs/NLM-GWS-DICH-NGOAI-KHO-r1.md#4-nghiem_thu) · [Packet 2 N3](ops/specs/GWS-CRED-DICH-NGOAI-KHO-r1.md#4-nghiem_thu) |
| **P2** | **1 và 2** | **Hợp đồng một dòng và một cụm lỗi chưa quy định cách hiển thị dữ liệu biến thiên.** Packet 1 M1 trả lý do kèm đường kho hoặc tiền tố, M2 thêm `repr(khoá)`, còn M4/N8 và packet 2 M3/N7 đòi đúng một dòng theo cụm cố định. Trong RAM, nội suy đường POSIX giả `/fake/a\nb` cho hai dòng. Một khoá lạ chứa nguyên văn cụm của lỗi khác cũng làm phép đếm cụm trả hai, kể cả khi dùng `repr`. Chốt cách thoát ký tự xuống dòng và ký tự điều khiển, rồi nhận diện loại lỗi ở phần cố định của mẫu. Thêm ca đường có xuống dòng và khóa mang cụm lỗi khác. |
| **P2** | **2** | **N5 đòi quyền `0600` trên mọi nền, trái §2.** N5 kiểm cả quyền nguồn tại lúc `os.replace` và quyền đích sau ghi. Theo §2, Windows không đo `0600` bằng `stat`, nhưng N5 không điều kiện hóa hai phép đo này. Giữ các hậu điều về byte, đường, số lần `replace` và bản cũ trên Windows. Ghi rõ cả hai phép kiểm mode chỉ áp dụng trên POSIX, như packet 1 N2 đã làm. |
| **P3** | **1 và 2** | **Mốc đo lại ADR và lịch sử lớp cần rõ hơn trong bàn giao.** Hai OID ADR có tệp tại commit, thiếu ở cha thứ nhất và nằm trên first-parent của `origin/master` cục bộ, với rc lần lượt `0/128/0`. Điều kiện ref vừa fetch vẫn chưa xác minh trong lượt offline. §7 đã khai thiếu biên nhận tiền nhiệm. Khi ghi bộ đếm bắt đầu từ 1, ghi rõ đây là bộ đếm có chứng cứ hiện tại và giữ liên kết lớp của đặc tả gốc qua lần tách. |

## Phần chuyển tiếp, trần và hợp đồng chung

- **Hai chuỗi Git.** Packet 1 giữ lời hứa kiểm cả chuỗi từ vựng và `realpath` bằng cách gọi `_trong_kho_git` nguyên thân. N4 chứng minh caller dùng chốt; PD7/PD8 canh hàm nền. Phản chứng tách từng chuỗi qua chính `_kiem_dich_ghi` nằm ở packet 2 N3b. §7 packet 1 đã khai đúng giới hạn này. Tương tự, giả lập bit reparse là bằng chứng logic tại packet 1, còn junction thật thuộc packet 2 N4. Riêng việc từ chối lá jar cần phép đo tại packet 1 vì đây là hành vi mà packet 1 bàn giao trước.
- **Trần packet 1.** Số học đúng, `108–133 + 282–312 + 1 = 391–446` dòng thêm, ba tệp. Generator hiện tạo một dòng cho mỗi fragment. Bốn dòng là khoảng cách từ đầu trên của **ước lượng** đến 450. Mức dùng thật chỉ có sau `git diff --numstat` trên exact base và exact head. N13 kiểm mã thoát, đúng tập ba đường và biên 450/451. §6 dừng trước review nếu vượt, rồi revision để tách tiếp theo quyết định đã ghi. Tính lại dự toán sau khi đưa ca lá jar trở lại và xác minh lại hiệu lực ADR trước khi dùng trần 450.
- **`_kiem_dich_ghi`.** W4/W5 với `goc=cfgdir_chuẩn`, `thanh_phan=("credentials.json",)` và `dich=join(goc, *thanh_phan)` phù hợp tiền điều kiện của packet 1. Cùng một `dich` đi vào chốt, writer và kết quả W5. Giữ thứ tự kiểm kho trên `dirname(dich)` trước `lstat` từ `goc` đến lá. Packet 2 xử lý chuẩn hóa và cụm `đường không hợp lệ` ở caller. §6 packet 2 đặt đúng điểm dừng nếu base đã land thiếu hợp đồng hoặc cần sửa thân hàm. Cả hai caller cần cùng quy tắc định dạng chẩn đoán nêu trên.

## Rà L1–L7

| Luật | Kết quả |
|---|---|
| L1 | Hai packet ghi đơn vị cho số chỗ ghi, số tệp, dòng thêm và số ca/đột biến. |
| L2 | Mỗi mục tiêu chiếu vào một đường trong write set. Packet 2 chỉ đột biến helper trong RAM; mọi sửa thân helper cần revision. Ngoại lệ bundled cần comment riêng cho từng packet trước lease. |
| L3 | Có ca đỏ và nhãn đích cho phần lớn tiêu chí. Còn khe lá jar ở packet 1 và hậu điều mode Windows ở packet 2. Cả hai khai rõ `doctrine-scan`/`adr-song` là gate kế thừa, chưa có phép đỏ riêng. |
| L4 | Cả hai khai thiếu biên nhận và ghi rõ suy luận từ tiêu đề PR. Giữ liên kết lớp xuyên lần tách như finding P3. |
| L5 | Đã neo số dòng vào blob base và ghi mốc ước lượng. `numstat` ứng viên, base sau land của packet 2 và độ mới của ref cần đo ở mốc tương ứng. |
| L6 | `fullmatch` từng dòng, đột biến thêm dòng và kiểm đúng tập đường cho `numstat` là các thước đo phù hợp. Phần chẩn đoán biến thiên còn khe P2 ở cả hai packet. |
| L7 | Trần, revision và các điểm chờ chủ kho có căn cứ ADR hoặc E2. Hai packet khai phạm vi E4/E5. Đặc tả vẫn chờ duyệt băm và quyền bundled theo từng packet. |

KET_LUAN: request_changes
tokens used
61,689
## Review độc lập lượt 5 · Issue #433

**Còn P2 ở cả hai packet.** Packet 1 thiếu phép nghiệm thu trước land cho cam kết từ chối symlink ở tệp cuối của jar NLM. Packet 2 có tiêu chí quyền tệp mâu thuẫn với phạm vi Windows. Cả hai còn một khe trong hợp đồng chẩn đoán một dòng.

Review chỉ đọc trên Linux, Python 3.13.18, trong phiên Codex họ OpenAI qua API. `HEAD` là `641108cb997872b0ef2a277ea9c8faf8b82532bb`, trùng ref `master` cục bộ, tree `e6c7c50863421e32cac4f5f1894f176d758375b1`. Checkout ở detached HEAD. Diff tracked và index đều sạch, chín bản đặc tả là untracked. Các phép thử dùng dữ liệu giả trong RAM, không gọi mạng hoặc đọc secret thật. Các kết luận đóng dưới đây áp dụng ở mức đặc tả. Chưa có mã ứng viên để chạy fragment, đo `numstat` hoặc kiểm hành vi native Windows.

## Đối chiếu finding lượt 4

| Finding | Packet | Trạng thái | Bằng chứng |
|---|---|---|---|
| P2 · NUL trong biến môi trường | 1 | Đóng | M3(0b) kiểm cả hai trường trước mọi phép gán. N3(7) kiểm cả hai biến giữ giá trị cũ và config giữ byte. `python3 -B` với `x\x00y` tái hiện `ValueError: embedded null byte`. Hai đột biến phân biệt bỏ kiểm NUL với gán token quá sớm. |
| P2 · `db_reparse_moi_thu` sống | 1 | Đóng | N6(5) dùng đối chứng `FILE_ATTRIBUTE_DIRECTORY = 16`. Phép bit với `REPARSE_POINT = 1024` trả false cho 16 và true cho 1024. Đột biến dùng `bool(attributes)` trả true cho cả hai, nên làm đỏ `khong_bit`. |
| P2 · Nhánh định dạng W1/W3 | 1 | Đóng | `git show HEAD:scripts/tl_gws.py` xác nhận W1 in cảnh báo ở dòng 1652 rồi trả 1. W3 kiểm kiểu và rỗng ở 1955, trả lý do nguyên văn ở 1956. M2 và N3(8) giữ hai nhánh, đồng thời giữ W2 bỏ qua jar falsy. |
| P2 · rc 4 khi ghi bootstrap bị từ chối | 1 và 2 | Đóng | Packet 1 N8(2) chạy lại đúng ca W2 bị từ chối. Packet 2 N7(1) dùng ca W4 bị từ chối. Chạy đuôi `cmd_bootstrap` trích từ AST của base với `degraded=True` và agent giả cho rc 1/4 tùy cờ, luôn có một dòng `agent_creds:`. Vế kết hợp với từ chối ghi sẽ được đo khi có mã. |
| P2 · Đường Windows theo ổ | 2 | Đóng | M1 nêu rõ hai dạng phải từ chối và N2w có đối chứng. `ntpath` 3.13.18 cho `D:fake → ('D:', 'fake'), False`, `\fake → ('', '\\fake'), False`, `D:\fake → ('D:', '\\fake'), True`. `join` với `C:\cwd` giữ `D:fake` nhưng biến `\fake` thành `C:\fake`. Vì vậy phải phân loại đường thô trước khi ghép cwd, theo `splitdrive` và dấu phân cách đầu phần đuôi. |
| P3 · §7 khai quá độ phủ | 1 | Đóng | §7 phân biệt ca config `dich == goc`, ca thành phần thư mục, reparse giả lập, hai chuỗi Git chuyển tiếp và đột biến tệp cuối chuyển tiếp. Khoảng trống nghiệm thu còn lại được nêu riêng bên dưới. |

## Finding mới

| Mức | Packet | Finding và điều kiện đóng |
|---|---|---|
| **P2** | **1**, liên quan 2 | **Cam kết từ chối symlink ở lá jar chưa có phép nghiệm thu trước land.** M1/M2 yêu cầu kiểm đến chính `dich`. N6(2) chỉ kiểm trường hợp `dich == goc`, N6(3) kiểm thư mục trung gian. Một vòng lặp bỏ đúng tiền tố cuối khi tuple khác rỗng vẫn qua hai ca đó. Ghi nguyên tử vẫn giữ byte tệp được trỏ tới nhưng có thể thay chính symlink bằng tệp thường và báo thành công. Packet 2 N3 bắt được lỗi chung sau khi packet 1 land, qua W4; nó cũng không bắt được lỗi riêng khi caller NLM dựng tuple thiếu lá. Giữ một ca W1 tối thiểu ngay ở packet 1, đòi rc từ chối, đúng lý do, symlink còn nguyên và tệp được trỏ tới giữ byte. Có thể để đột biến đầy đủ ở packet 2 nếu cần giữ trần. [Packet 1 M1 và N6](ops/specs/NLM-GWS-DICH-NGOAI-KHO-r1.md#4-nghiem_thu) · [Packet 2 N3](ops/specs/GWS-CRED-DICH-NGOAI-KHO-r1.md#4-nghiem_thu) |
| **P2** | **1 và 2** | **Hợp đồng một dòng và một cụm lỗi chưa quy định cách hiển thị dữ liệu biến thiên.** Packet 1 M1 trả lý do kèm đường kho hoặc tiền tố, M2 thêm `repr(khoá)`, còn M4/N8 và packet 2 M3/N7 đòi đúng một dòng theo cụm cố định. Trong RAM, nội suy đường POSIX giả `/fake/a\nb` cho hai dòng. Một khoá lạ chứa nguyên văn cụm của lỗi khác cũng làm phép đếm cụm trả hai, kể cả khi dùng `repr`. Chốt cách thoát ký tự xuống dòng và ký tự điều khiển, rồi nhận diện loại lỗi ở phần cố định của mẫu. Thêm ca đường có xuống dòng và khóa mang cụm lỗi khác. |
| **P2** | **2** | **N5 đòi quyền `0600` trên mọi nền, trái §2.** N5 kiểm cả quyền nguồn tại lúc `os.replace` và quyền đích sau ghi. Theo §2, Windows không đo `0600` bằng `stat`, nhưng N5 không điều kiện hóa hai phép đo này. Giữ các hậu điều về byte, đường, số lần `replace` và bản cũ trên Windows. Ghi rõ cả hai phép kiểm mode chỉ áp dụng trên POSIX, như packet 1 N2 đã làm. |
| **P3** | **1 và 2** | **Mốc đo lại ADR và lịch sử lớp cần rõ hơn trong bàn giao.** Hai OID ADR có tệp tại commit, thiếu ở cha thứ nhất và nằm trên first-parent của `origin/master` cục bộ, với rc lần lượt `0/128/0`. Điều kiện ref vừa fetch vẫn chưa xác minh trong lượt offline. §7 đã khai thiếu biên nhận tiền nhiệm. Khi ghi bộ đếm bắt đầu từ 1, ghi rõ đây là bộ đếm có chứng cứ hiện tại và giữ liên kết lớp của đặc tả gốc qua lần tách. |

## Phần chuyển tiếp, trần và hợp đồng chung

- **Hai chuỗi Git.** Packet 1 giữ lời hứa kiểm cả chuỗi từ vựng và `realpath` bằng cách gọi `_trong_kho_git` nguyên thân. N4 chứng minh caller dùng chốt; PD7/PD8 canh hàm nền. Phản chứng tách từng chuỗi qua chính `_kiem_dich_ghi` nằm ở packet 2 N3b. §7 packet 1 đã khai đúng giới hạn này. Tương tự, giả lập bit reparse là bằng chứng logic tại packet 1, còn junction thật thuộc packet 2 N4. Riêng việc từ chối lá jar cần phép đo tại packet 1 vì đây là hành vi mà packet 1 bàn giao trước.
- **Trần packet 1.** Số học đúng, `108–133 + 282–312 + 1 = 391–446` dòng thêm, ba tệp. Generator hiện tạo một dòng cho mỗi fragment. Bốn dòng là khoảng cách từ đầu trên của **ước lượng** đến 450. Mức dùng thật chỉ có sau `git diff --numstat` trên exact base và exact head. N13 kiểm mã thoát, đúng tập ba đường và biên 450/451. §6 dừng trước review nếu vượt, rồi revision để tách tiếp theo quyết định đã ghi. Tính lại dự toán sau khi đưa ca lá jar trở lại và xác minh lại hiệu lực ADR trước khi dùng trần 450.
- **`_kiem_dich_ghi`.** W4/W5 với `goc=cfgdir_chuẩn`, `thanh_phan=("credentials.json",)` và `dich=join(goc, *thanh_phan)` phù hợp tiền điều kiện của packet 1. Cùng một `dich` đi vào chốt, writer và kết quả W5. Giữ thứ tự kiểm kho trên `dirname(dich)` trước `lstat` từ `goc` đến lá. Packet 2 xử lý chuẩn hóa và cụm `đường không hợp lệ` ở caller. §6 packet 2 đặt đúng điểm dừng nếu base đã land thiếu hợp đồng hoặc cần sửa thân hàm. Cả hai caller cần cùng quy tắc định dạng chẩn đoán nêu trên.

## Rà L1–L7

| Luật | Kết quả |
|---|---|
| L1 | Hai packet ghi đơn vị cho số chỗ ghi, số tệp, dòng thêm và số ca/đột biến. |
| L2 | Mỗi mục tiêu chiếu vào một đường trong write set. Packet 2 chỉ đột biến helper trong RAM; mọi sửa thân helper cần revision. Ngoại lệ bundled cần comment riêng cho từng packet trước lease. |
| L3 | Có ca đỏ và nhãn đích cho phần lớn tiêu chí. Còn khe lá jar ở packet 1 và hậu điều mode Windows ở packet 2. Cả hai khai rõ `doctrine-scan`/`adr-song` là gate kế thừa, chưa có phép đỏ riêng. |
| L4 | Cả hai khai thiếu biên nhận và ghi rõ suy luận từ tiêu đề PR. Giữ liên kết lớp xuyên lần tách như finding P3. |
| L5 | Đã neo số dòng vào blob base và ghi mốc ước lượng. `numstat` ứng viên, base sau land của packet 2 và độ mới của ref cần đo ở mốc tương ứng. |
| L6 | `fullmatch` từng dòng, đột biến thêm dòng và kiểm đúng tập đường cho `numstat` là các thước đo phù hợp. Phần chẩn đoán biến thiên còn khe P2 ở cả hai packet. |
| L7 | Trần, revision và các điểm chờ chủ kho có căn cứ ADR hoặc E2. Hai packet khai phạm vi E4/E5. Đặc tả vẫn chờ duyệt băm và quyền bundled theo từng packet. |

KET_LUAN: request_changes
rc=0 xong 2026-11-18T06:25:40Z
