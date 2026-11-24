# Verdict PR #1503 lượt 9 — Codex

reviewed_sha: 50d151899ae528e2a7e4dbc67288b092c0961cd5
reviewed_tree: 4503cde4ba3fbed774b6926623c2b9b9aa69cff5
base_sha: a03a28ef076503c7fe93c208a4998c32590a977f
base_tree: 1c3dfd0b5363745cb27ca976cb37ae865aeb2ebe
nang_tran: chủ kho nâng trần lên 9 (lời gọi thứ 9, cuối cùng)

## Neo review

- Chỉ thị lượt 9 do người dùng giao và dẫn quyết định 7135632032. SHA-256 của prompt `e5ef2a7d59561cad41b928b2f0b1163c3947578849b13d789ceb907e24cf90fa` khớp run và checkpoint. Run `f46ec0981f2f4d44817b6eb2618065cc` ghi `openai_codex / codex_cli / machine`. Linux x86_64, Bash, Python 3.13.18, Codex CLI 0.172.0, sandbox `workspace-write`. Model và effort phục vụ `KHONG_DO_DUOC` theo biên nhận đang chạy.
- Checkout detached đúng SHA, origin nhận diện `ducthangho/tra-luat`, `core.abbrev=7`. SHA base là cha thứ hai của SHA lượt 8 và là tổ tiên của HEAD. Ref `origin/master` trong bản sao dừng ở `5259239d763c9ffc1677f033bd9a9cf23ede9299` là cha thứ nhất của base đã giao. Dùng hai OID đã đóng băng để đối chiếu.
- Phạm vi review xử lý theo lớp `sensitive` vì PR làm đổi xác thực và launcher. Phạm vi ghi trong checkout là `.review/VERDICT.md`. Lúc nhận cây, diff tracked và index rỗng, `.codex/` ignored rỗng.
- Mỗi phép đo chạy trên bản sao tạm, detached, với HOME và cache riêng, môi trường tối giản, proxy loopback, Git chỉ cho transport `file` và các CLI ngoài thay bằng stub. Lệnh, mã thoát và SHA-256 của stdout/stderr nằm trong `/tmp/pr1503-r9.08N2tN/logs/`. Diff toàn PR SHA-256 `18312bb4e72761e9cf3d506a7c17296559d0a2108ca72d6b87408c33265d254f`. Diff lượt 9 SHA-256 `fb553f8337a4a4336a52d8716c1ec2ff4cf602524b291c7dd7d4e6693162880b`.

## Đối chiếu lượt 8 (và các lớp còn mở)

Mốc A là lượt 8 `a93b8f3069cd845468545fa79c501a2a6a1782f0`, tree `2f2487f4c735ec243e66aa469424eb1614b36b07`. Mốc B là HEAD. Dùng lại fixture lượt 8, cập nhật kỳ vọng theo quyết định mới. Probe cấu trúc chạy qua handler thật với model giả và tệp đích có byte cũ. Các phép đo được dẫn dưới đây đều có rc 0 tại cả hai mốc.

| # | Trạng thái | Bằng chứng |
|---|---|---|
| U1 | ĐÃ ĐÓNG ca gốc | `probe-structure.py`: cắt sai trong trích dẫn kép cong lồng cùng kiểu ở nguồn có và mất số đều đổi từ `lech=[]`, rc 0, `ok=true`, ghi đè tệp, sang `lech=[0]`, rc 5, `ok=false`, giữ byte cũ. Cả cách cắt đúng trên cùng nguồn mơ hồ cũng bị chặn. Đối chứng trích dẫn con khác kiểu vẫn nhận cách cắt đúng và chặn cách cắt sai. |
| U2 | ĐÃ ĐÓNG ca mô phỏng · Windows bản địa chưa đo | `probe-threaded-pipes.py` dùng các hàm đọc có luồng của CPython Windows với pipe và tiến trình Python thật trên Linux. Mốc A trả sau 6,003 giây, khi đầu ghi phụ đã đóng. Mốc B ép nhánh Windows và trả timeout gốc sau 0,105 giây khi đầu ghi vẫn mở, con trực tiếp đã có `returncode=-9`. `probe-mutants.py` kiểm độc lập thứ tự và timeout của cleanup. |
| U3 | ĐÃ ĐÓNG ca gốc | `probe-numbering-in-quote.py`: số thứ tự trong trích dẫn kép cong hoặc ngoặc tròn trải hai dòng từng sinh hai mục, rc 0, `ok=true` và đè tệp. HEAD chặn cả kết quả một mục lẫn hai mục với `lech=[0]`, rc 5, `ok=false`, giữ byte cũ. `probe-structure.py` xác nhận hai biến thể tiếp dòng bằng “là” và dòng điểm cũng đổi rc 0 → 5. |
| `ranh-gioi-khoan` | CÒN MỞ · P1 | U1/U3 đóng ở các mẫu cũ. V1 ghi dấu trích dẫn còn nằm ngoài bộ quét. Đối chứng số khoản liên tục, mất số mỗi dòng một khoản, dòng mở bằng “là” và dòng điểm cân dấu vẫn đạt. |
| `thu-hoi-tien-trinh-sub` | ĐÃ ĐÓNG trong phạm vi đã đo | T2 EIO và timeout thu hồi con trực tiếp trên Linux. U2 qua mô phỏng Windows có bên khác giữ pipe. V2 ghi độ phủ của suite đối với hợp đồng cleanup. Cần phép đo Windows bản địa để kết luận cho nền này. |
| `phan-loai-sub` | ĐÃ ĐÓNG ca đã đo | `probe-runtime.py`: auth API-key, auth timeout, lỗi dựng cwd và spawn lỗi thật chỉ đi API giả khi marker model chưa tồn tại. Timeout, EIO, hết hạn mức và mất envelope sau marker có 0 lượt API giả. Lỗi dọn cwd sau model thành công giữ kết quả sub. |

## Findings mới

### V1 [P1] Dấu trích dẫn ngoài cặp kép không được xét khi xác định ranh giới — scripts/tl_core/llm_route.py:546

Lớp `ranh-gioi-khoan`. Biểu hiện mới của U1/U3 ở dấu kép góc và dấu đơn cong. `_dong_mo_ho` chỉ mở trạng thái ở dấu kép thẳng hoặc kép cong. `_quet` dùng cùng phạm vi ký tự. Hợp đồng lượt 9 và `docs/GOI_AGENT_DA_NEN.md` yêu cầu chặn trích dẫn trải dòng, và tài liệu kho cũng dùng dấu kép góc để biểu thị trích dẫn.

Kịch bản theo mô tả. Một trích dẫn dùng dấu kép góc hoặc dấu đơn cong trải qua dòng chứa số nối tiếp có thể bị chia thành hai khoản, vì hai dấu biên đều bị coi là chữ thường và nhánh đánh số mở khoản ở đầu dòng kế. Trên một dòng, từ “là” nằm trong một tên gọi được trích bằng các dấu đó cũng có thể bị chọn làm từ nối thay cho từ nối thật. Phép so hai vế ở `lech_nguyen_van` dùng chính ranh giới đó nên có thể nhận kết quả sai và cho ghi `--out`.

Bằng chứng đã chạy. `run-check head quote-tokens-head python <scratch>/probe-quote-tokens.py`, rc 0. Với ký hiệu mở hoặc đóng đứng riêng, cặp kép cong và kép thẳng cho `_dong_mo_ho=True` ở cả hai chiều. Cặp `U+00AB/U+00BB` và `U+2018/U+2019` đều cho `False`. Trên cụm trung tính đã khép, `_quet` vẫn báo phần chữ của cả hai cặp này ở ngoài trích dẫn. Chạy cùng phép đo trên A cho thấy `_quet` đã có hành vi này từ lượt 8. Bản vá mới chưa bao phủ nó. Phản chứng kết hợp đánh số hoặc cắt từ nối được mô tả bằng lời.

Đề xuất dùng cùng một tập kiểu dấu cho kiểm tra mơ hồ và chọn từ nối. Với kiểu dấu chưa hỗ trợ, có thể từ chối cả nguồn theo quyết định bảo thủ. Khóa ca báo đạt sai khi số của mục trích dẫn nằm đầu dòng và ca chọn “là” trong tên gọi. Giữ đối chứng dấu kép thẳng được trích như một ký tự trong cặp kép cong.
