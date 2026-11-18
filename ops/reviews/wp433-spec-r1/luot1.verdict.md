Review đặc tả #433 r1. **Còn hai lỗi P1**: M1/M5 vẫn cho phép ghi qua liên kết ra ngoài đích, và write set giao hai artifact dành cho phiên land cho Executor.

**Mốc review.** HEAD `641108cb997872b0ef2a277ea9c8faf8b82532bb`, tree `e6c7c50863421e32cac4f5f1894f176d758375b1`, Git blob của đặc tả `161e9229d3a4609d911570e77f7c87d47d3385d6`. Checkout detached tại OID cũng được nhánh `master` cục bộ trỏ tới. Đặc tả là tệp untracked duy nhất. Provider `openai_codex`, transport `machine`. Phiên dùng shell qua API. Bề mặt triển khai cụ thể, model phục vụ và generation chưa có biên nhận để xác minh.

### Bảng kiểm sự thật

| Mục | Kết quả |
|---|---|
| §0.1, W1–W6 | Đúng vị trí và luồng ghi. Blob `tl_gws.py` và SHA-256 khớp khai báo. W2 vẫn ghi khi có `--no-nlm`. Với chuỗi bắt đầu bằng `/`, phép `split("/")` bỏ tác dụng của dấu `/` đầu khi truyền các thành phần vào `join`. Phép đo thoát đích bằng `..` vẫn đúng. |
| §0.2, A–G | Chạy `python3 -IB -` trên các thân hàm trích từ blob Git, với dữ liệu và hệ tệp giả trong RAM, rc 0. A/B/C lần lượt trả `0/1/True` và ghi `HOME/thoat.json`. D ghi khoá lạ, rc 0. E1/E2 ghi `K/gwscfg/credentials.json`, trả `True/0`. F trả 1 và ghi cả config lẫn jar trong `K/home`. G trả 0 và chỉ ghi config trong rig. `mktemp -d /tmp/wp433-review.XXXXXXXX` thất bại, rc 1, vì filesystem chỉ đọc. Chưa đo syscall trên filesystem thật, porcelain hay hành vi Windows. |
| Rà các chỗ ghi khác | Trong `tl_gws.py`, writer Codex ở dòng 1271 dùng chốt kho và thay tệp nguyên tử. `cmd_gws_bootstrap_cowork` gọi lại W5. W6 còn sao chép `nlm_auth` vào config. Trong `tl.py`, các hit ghi/copy là probe thư mục tạm, mã tự phục hồi và PDF tạm. Trong `ops/cloud_agent_creds.py`, `_ghi_dau` có chốt kho và chỉ ghi metadata. `gop_settings` và `dat_env_file` có thể ghi lại **nội dung đã có** vào đường dẫn nằm trong kho. `dat_env_file` dùng đích do `CLAUDE_ENV_FILE` chỉ định. Hai đường này không nhận credential từ bundle. Cần ghi rõ phạm vi này trong §0.1. |
| §0.3, allowlist | Ba producer được nêu đều dùng cùng bộ thu khoá. Ba đường hợp lệ và mọi tập con do producer sinh vẫn qua allowlist. Các hit `nlm_auth` trong `ops_misc.py` và `profile_env.py` là trạng thái, không sinh bundle. Bundle cũ hoặc do bên ngoài tạo chưa xác minh. |
| §0.4–0.5, gate | Đối chiếu neo PD, d5 và cơ chế fragment. Manifest base có 185 mục. Gọi trực tiếp `_test_fragments_check('.')` bằng `python3 -IB -` trả `ok: true`, hai SHA-256 bằng nhau, rc 0. CLI gate dừng ở bước tìm thư mục tạm. `git diff --check` rc 0 trên diff tracked. Selftest đầy đủ, cloud agent suite, bundle topology, Ruff và lease từ xa chưa chạy lại. |

### Findings

**P1 — M1/M5, N3/N4/N5. Kiểm kho ở thư mục cha còn lọt đường ghi thực.** Với `auth.json` hoặc `.tra_luat_config.json` là symlink tới tệp trong kho, chốt cha trả `None` và `open("w")` ghi vào đích liên kết. Cả hai trường hợp đã cho kết quả đó trong rig RAM. Một thư mục `profiles/default` trỏ ra ngoài NLM root tới nơi không có `.git` cũng qua chốt hiện tại. Ghi đè tại chỗ còn thay đổi cả inode có hardlink ở nơi khác.

Câu thay thế: “W1–W3 xác thực tất cả khoá và đích trước khi tạo hoặc ghi tệp. Đích sau khi giải liên kết ở thư mục cha phải nằm dưới NLM root thực và qua chốt kho trên đường dẫn gốc. W1–W3 và W6 thay tệp nguyên tử để tránh ghi xuyên symlink hoặc hardlink của tệp cuối. Thêm ca thư mục con trỏ sang đích ngoài root, ca tệp cuối trỏ vào kho và phản chứng riêng cho từng chốt. Ghi rõ giả định về việc thư mục đích có thể bị đổi đồng thời hay không.”

**P1 — §1, M7/M8, N10–N12. Giao artifact land-only cho sai vai.** Protocol quy định worker sinh bundled candidate và manifest tạm ngoài repo. Hai commit tiền lệ và yêu cầu release trong `CLAUDE.md` chưa chứng minh quyền đưa hai tệp sinh vào diff worker. [Protocol về artifact release](docs/PROTOCOL_DA_PHIEN.md#L863) · [Protocol về worker gate](docs/PROTOCOL_DA_PHIEN.md#L997)

Câu thay thế: “Bỏ `scripts/tl_test_fragments_bundled.py` và `RELEASE_MANIFEST.json` khỏi write set worker. N10–N11 kiểm bundled candidate và manifest strict trong cây tạm dựng từ exact head. Phiên land tái sinh artifact canonical theo protocol. N12 so numstat với write set worker đã sửa.”

**P2 — M1/M5, N1. Hợp đồng từ chối NLM bỏ qua bản sao trong W6.** N1 cho W2 fixture thiếu token. Khi có token, W6 ghi cả `nlm_auth` vào config trước khi W2 từ chối khoá lạ. Ca N1 hiện có thể xanh dù config đã lưu payload bị từ chối.

Câu thay thế: “N1 của bootstrap dùng bundle có token, GWS hợp lệ, một khoá NLM hợp lệ và một khoá bị từ chối. Token vẫn được nạp vào env. Config được phép lưu không nhận `nlm_auth` của lượt bị từ chối. Kiểm cả config lẫn cây jar.” Phạm vi này cần được chốt cùng quyết định W6 khi duyệt đặc tả.

**P2 — M3/M6, N5–N7. Rig có thể gọi tải thật và chưa khoá hợp đồng lỗi.** `TL_AGENT_CREDS_FILEID=""` rơi về hằng baked. N5 còn thiếu `gws_cred`, nên rc 1 có thể tới từ cảnh báo GWS kể cả khi nhánh từ chối quên đặt `degraded`. `_ghi_nguyen_tu_0600` có thể ném `OSError`. N7 hiện đếm cụm từ nên một dòng stderr thừa không chứa cụm vẫn lọt. M3 cũng cần giữ precedence của `--require-agent-creds` và xác định lỗi hạ cấp W3 khi cùng xuất hiện.

Câu thay thế: “Mỗi ca ghim cả env lẫn ID baked hoặc thay toàn bộ đường tải bằng đồ giả có kiểm đếm. Dựng mọi nhánh ngoài đích ở trạng thái thành công, bắt stdout/stderr riêng, kiểm toàn bộ dòng chẩn đoán gồm thẻ và số dòng. Thêm ca I/O giả ném `OSError` và kiểm rc, thông báo đã lọc, dòng `agent_creds:` và trạng thái tệp. Ghi rõ rc 4 với `--require-agent-creds` và thứ tự từ chối W3. Khoá không hợp lệ được mô tả bằng dữ liệu giới hạn và đã lọc để giá trị nhạy cảm không lọt log.”

**P2 — N1, N4, N6, N8, N12. Một số phản chứng chưa chứng minh được điều đã khai.**

| Tiêu chí | Vấn đề và câu thay thế |
|---|---|
| N1/N8 | Bỏ riêng assert `thoat.json` vẫn còn assert về `auth.json`, rc và chẩn đoán. Mutant W1 vẫn có thể bị giết. “Kiểm cơ chế SỐNG bằng một mutant chỉ đổi hậu điều đích, hoặc tắt toàn bộ oracle đích trong lượt tự kiểm. Giữ một nhãn oracle riêng để chứng minh hậu điều nào đã giết mutant.” |
| N4/N8 | Cho phép skip symlink nhưng vẫn đòi giết mọi mutant và in `n/n`, `m/m`. “Khai tổng dự kiến, số đã chạy, số đạt/giết và số skip riêng. Ca/đột biến phụ thuộc symlink bị skip cùng nhau với lý do. Skip không tính đạt.” |
| N6 | Kiểm bên trong callback `os.replace` có thể không chạy nếu mutant bỏ hẳn `replace`. “Sau khi gọi writer, assert observer đã thấy đúng một lần thay đích, rồi kiểm nguồn cùng thư mục, bản cũ trước thay, bytes và mode sau thay.” |
| N12 | `doctrine-scan` và `adr-song` chưa có phép đỏ. “Ghi đây là gate kế thừa và chỉ rõ fixture âm hiện có, hoặc khai chưa có phản chứng riêng theo L3. Thêm phản chứng riêng cho vượt dòng với nguyên tập đường dẫn hợp lệ.” |

Các mutant W1–W6 cần neo nguyên văn có ngữ cảnh riêng cho từng call site. Kiểm cardinality bằng 1, kiểm compile/bind thành công, rồi mới chấm lỗi đúng oracle. Chưa có mã head để xác nhận các phép đo này.

**P3 — M4/N9 và §8. Chuyển điều kiện d5 vào fragment nếu chủ kho chấp thuận đổi vị trí.** d5 đã kiểm không export, không tạo `.gemini` và có auth Codex. Điều kiện `.claude` có thể kiểm tương đương trong fragment với fixture thực sự đi qua `_bootstrap_agent_creds`. Điều này bỏ khóa tuần tự trên `tl_selftest.py`. Nếu giữ lựa chọn sửa d5 đã được ghi nhận, giữ điều kiện tuần tự và yêu cầu mutant xác nhận đã chạy tới lệnh tạo `.claude`.

Câu thay thế: “Fragment thêm ca bootstrap nhận bundle agent giả có khoá Claude/Gemini, xác minh nạp Codex thành công và HOME không có `.claude`. Mutant tạo `.claude` phải làm đỏ đúng hậu điều này. Giữ lựa chọn sửa trực tiếp d5 khi quyết định về vị trí test được xác nhận.”

**P3 — §0.3, §7–§8. Chỉnh số liệu và provenance theo L1/L4/L5/L7.** Cận trên 451 **vượt một dòng**. Chưa cần tách chỉ vì ước lượng. Bỏ hai artifact land-only và chuyển d5 sang fragment giúp giảm phần diff worker, nhưng các ca bổ sung cũng cần tính lại trước khi đóng băng. `git log -S '_NLM_AUTH_RELS =' HEAD -- scripts` cho `394e934`, `47310dc`, `bf5ca78`. Số lần lặp từ tiêu đề PR là suy luận, chưa phải bộ đếm có biên nhận.

Câu thay thế: “Ước lượng lại số tệp và dòng thêm cho write set r2. Đo `git diff --numstat base..HEAD` trước review. Chỉ tách khi phạm vi mới không kham được ≤6 tệp và ≤450 dòng thêm hoặc thực hiện ngoại lệ E2 theo ADR-0053. Ghi số đếm lịch sử là chưa xác minh và đo lại các số động trước mỗi lần công bố. Giữ phân loại §5 cho phiên chỉ dùng dữ liệu giả. Mọi phép xác minh cần đọc bundle thật thuộc E4.”

KET_LUAN: request_changes
tokens used
64,843
Review đặc tả #433 r1. **Còn hai lỗi P1**: M1/M5 vẫn cho phép ghi qua liên kết ra ngoài đích, và write set giao hai artifact dành cho phiên land cho Executor.

**Mốc review.** HEAD `641108cb997872b0ef2a277ea9c8faf8b82532bb`, tree `e6c7c50863421e32cac4f5f1894f176d758375b1`, Git blob của đặc tả `161e9229d3a4609d911570e77f7c87d47d3385d6`. Checkout detached tại OID cũng được nhánh `master` cục bộ trỏ tới. Đặc tả là tệp untracked duy nhất. Provider `openai_codex`, transport `machine`. Phiên dùng shell qua API. Bề mặt triển khai cụ thể, model phục vụ và generation chưa có biên nhận để xác minh.

### Bảng kiểm sự thật

| Mục | Kết quả |
|---|---|
| §0.1, W1–W6 | Đúng vị trí và luồng ghi. Blob `tl_gws.py` và SHA-256 khớp khai báo. W2 vẫn ghi khi có `--no-nlm`. Với chuỗi bắt đầu bằng `/`, phép `split("/")` bỏ tác dụng của dấu `/` đầu khi truyền các thành phần vào `join`. Phép đo thoát đích bằng `..` vẫn đúng. |
| §0.2, A–G | Chạy `python3 -IB -` trên các thân hàm trích từ blob Git, với dữ liệu và hệ tệp giả trong RAM, rc 0. A/B/C lần lượt trả `0/1/True` và ghi `HOME/thoat.json`. D ghi khoá lạ, rc 0. E1/E2 ghi `K/gwscfg/credentials.json`, trả `True/0`. F trả 1 và ghi cả config lẫn jar trong `K/home`. G trả 0 và chỉ ghi config trong rig. `mktemp -d /tmp/wp433-review.XXXXXXXX` thất bại, rc 1, vì filesystem chỉ đọc. Chưa đo syscall trên filesystem thật, porcelain hay hành vi Windows. |
| Rà các chỗ ghi khác | Trong `tl_gws.py`, writer Codex ở dòng 1271 dùng chốt kho và thay tệp nguyên tử. `cmd_gws_bootstrap_cowork` gọi lại W5. W6 còn sao chép `nlm_auth` vào config. Trong `tl.py`, các hit ghi/copy là probe thư mục tạm, mã tự phục hồi và PDF tạm. Trong `ops/cloud_agent_creds.py`, `_ghi_dau` có chốt kho và chỉ ghi metadata. `gop_settings` và `dat_env_file` có thể ghi lại **nội dung đã có** vào đường dẫn nằm trong kho. `dat_env_file` dùng đích do `CLAUDE_ENV_FILE` chỉ định. Hai đường này không nhận credential từ bundle. Cần ghi rõ phạm vi này trong §0.1. |
| §0.3, allowlist | Ba producer được nêu đều dùng cùng bộ thu khoá. Ba đường hợp lệ và mọi tập con do producer sinh vẫn qua allowlist. Các hit `nlm_auth` trong `ops_misc.py` và `profile_env.py` là trạng thái, không sinh bundle. Bundle cũ hoặc do bên ngoài tạo chưa xác minh. |
| §0.4–0.5, gate | Đối chiếu neo PD, d5 và cơ chế fragment. Manifest base có 185 mục. Gọi trực tiếp `_test_fragments_check('.')` bằng `python3 -IB -` trả `ok: true`, hai SHA-256 bằng nhau, rc 0. CLI gate dừng ở bước tìm thư mục tạm. `git diff --check` rc 0 trên diff tracked. Selftest đầy đủ, cloud agent suite, bundle topology, Ruff và lease từ xa chưa chạy lại. |

### Findings

**P1 — M1/M5, N3/N4/N5. Kiểm kho ở thư mục cha còn lọt đường ghi thực.** Với `auth.json` hoặc `.tra_luat_config.json` là symlink tới tệp trong kho, chốt cha trả `None` và `open("w")` ghi vào đích liên kết. Cả hai trường hợp đã cho kết quả đó trong rig RAM. Một thư mục `profiles/default` trỏ ra ngoài NLM root tới nơi không có `.git` cũng qua chốt hiện tại. Ghi đè tại chỗ còn thay đổi cả inode có hardlink ở nơi khác.

Câu thay thế: “W1–W3 xác thực tất cả khoá và đích trước khi tạo hoặc ghi tệp. Đích sau khi giải liên kết ở thư mục cha phải nằm dưới NLM root thực và qua chốt kho trên đường dẫn gốc. W1–W3 và W6 thay tệp nguyên tử để tránh ghi xuyên symlink hoặc hardlink của tệp cuối. Thêm ca thư mục con trỏ sang đích ngoài root, ca tệp cuối trỏ vào kho và phản chứng riêng cho từng chốt. Ghi rõ giả định về việc thư mục đích có thể bị đổi đồng thời hay không.”

**P1 — §1, M7/M8, N10–N12. Giao artifact land-only cho sai vai.** Protocol quy định worker sinh bundled candidate và manifest tạm ngoài repo. Hai commit tiền lệ và yêu cầu release trong `CLAUDE.md` chưa chứng minh quyền đưa hai tệp sinh vào diff worker. [Protocol về artifact release](docs/PROTOCOL_DA_PHIEN.md#L863) · [Protocol về worker gate](docs/PROTOCOL_DA_PHIEN.md#L997)

Câu thay thế: “Bỏ `scripts/tl_test_fragments_bundled.py` và `RELEASE_MANIFEST.json` khỏi write set worker. N10–N11 kiểm bundled candidate và manifest strict trong cây tạm dựng từ exact head. Phiên land tái sinh artifact canonical theo protocol. N12 so numstat với write set worker đã sửa.”

**P2 — M1/M5, N1. Hợp đồng từ chối NLM bỏ qua bản sao trong W6.** N1 cho W2 fixture thiếu token. Khi có token, W6 ghi cả `nlm_auth` vào config trước khi W2 từ chối khoá lạ. Ca N1 hiện có thể xanh dù config đã lưu payload bị từ chối.

Câu thay thế: “N1 của bootstrap dùng bundle có token, GWS hợp lệ, một khoá NLM hợp lệ và một khoá bị từ chối. Token vẫn được nạp vào env. Config được phép lưu không nhận `nlm_auth` của lượt bị từ chối. Kiểm cả config lẫn cây jar.” Phạm vi này cần được chốt cùng quyết định W6 khi duyệt đặc tả.

**P2 — M3/M6, N5–N7. Rig có thể gọi tải thật và chưa khoá hợp đồng lỗi.** `TL_AGENT_CREDS_FILEID=""` rơi về hằng baked. N5 còn thiếu `gws_cred`, nên rc 1 có thể tới từ cảnh báo GWS kể cả khi nhánh từ chối quên đặt `degraded`. `_ghi_nguyen_tu_0600` có thể ném `OSError`. N7 hiện đếm cụm từ nên một dòng stderr thừa không chứa cụm vẫn lọt. M3 cũng cần giữ precedence của `--require-agent-creds` và xác định lỗi hạ cấp W3 khi cùng xuất hiện.

Câu thay thế: “Mỗi ca ghim cả env lẫn ID baked hoặc thay toàn bộ đường tải bằng đồ giả có kiểm đếm. Dựng mọi nhánh ngoài đích ở trạng thái thành công, bắt stdout/stderr riêng, kiểm toàn bộ dòng chẩn đoán gồm thẻ và số dòng. Thêm ca I/O giả ném `OSError` và kiểm rc, thông báo đã lọc, dòng `agent_creds:` và trạng thái tệp. Ghi rõ rc 4 với `--require-agent-creds` và thứ tự từ chối W3. Khoá không hợp lệ được mô tả bằng dữ liệu giới hạn và đã lọc để giá trị nhạy cảm không lọt log.”

**P2 — N1, N4, N6, N8, N12. Một số phản chứng chưa chứng minh được điều đã khai.**

| Tiêu chí | Vấn đề và câu thay thế |
|---|---|
| N1/N8 | Bỏ riêng assert `thoat.json` vẫn còn assert về `auth.json`, rc và chẩn đoán. Mutant W1 vẫn có thể bị giết. “Kiểm cơ chế SỐNG bằng một mutant chỉ đổi hậu điều đích, hoặc tắt toàn bộ oracle đích trong lượt tự kiểm. Giữ một nhãn oracle riêng để chứng minh hậu điều nào đã giết mutant.” |
| N4/N8 | Cho phép skip symlink nhưng vẫn đòi giết mọi mutant và in `n/n`, `m/m`. “Khai tổng dự kiến, số đã chạy, số đạt/giết và số skip riêng. Ca/đột biến phụ thuộc symlink bị skip cùng nhau với lý do. Skip không tính đạt.” |
| N6 | Kiểm bên trong callback `os.replace` có thể không chạy nếu mutant bỏ hẳn `replace`. “Sau khi gọi writer, assert observer đã thấy đúng một lần thay đích, rồi kiểm nguồn cùng thư mục, bản cũ trước thay, bytes và mode sau thay.” |
| N12 | `doctrine-scan` và `adr-song` chưa có phép đỏ. “Ghi đây là gate kế thừa và chỉ rõ fixture âm hiện có, hoặc khai chưa có phản chứng riêng theo L3. Thêm phản chứng riêng cho vượt dòng với nguyên tập đường dẫn hợp lệ.” |

Các mutant W1–W6 cần neo nguyên văn có ngữ cảnh riêng cho từng call site. Kiểm cardinality bằng 1, kiểm compile/bind thành công, rồi mới chấm lỗi đúng oracle. Chưa có mã head để xác nhận các phép đo này.

**P3 — M4/N9 và §8. Chuyển điều kiện d5 vào fragment nếu chủ kho chấp thuận đổi vị trí.** d5 đã kiểm không export, không tạo `.gemini` và có auth Codex. Điều kiện `.claude` có thể kiểm tương đương trong fragment với fixture thực sự đi qua `_bootstrap_agent_creds`. Điều này bỏ khóa tuần tự trên `tl_selftest.py`. Nếu giữ lựa chọn sửa d5 đã được ghi nhận, giữ điều kiện tuần tự và yêu cầu mutant xác nhận đã chạy tới lệnh tạo `.claude`.

Câu thay thế: “Fragment thêm ca bootstrap nhận bundle agent giả có khoá Claude/Gemini, xác minh nạp Codex thành công và HOME không có `.claude`. Mutant tạo `.claude` phải làm đỏ đúng hậu điều này. Giữ lựa chọn sửa trực tiếp d5 khi quyết định về vị trí test được xác nhận.”

**P3 — §0.3, §7–§8. Chỉnh số liệu và provenance theo L1/L4/L5/L7.** Cận trên 451 **vượt một dòng**. Chưa cần tách chỉ vì ước lượng. Bỏ hai artifact land-only và chuyển d5 sang fragment giúp giảm phần diff worker, nhưng các ca bổ sung cũng cần tính lại trước khi đóng băng. `git log -S '_NLM_AUTH_RELS =' HEAD -- scripts` cho `394e934`, `47310dc`, `bf5ca78`. Số lần lặp từ tiêu đề PR là suy luận, chưa phải bộ đếm có biên nhận.

Câu thay thế: “Ước lượng lại số tệp và dòng thêm cho write set r2. Đo `git diff --numstat base..HEAD` trước review. Chỉ tách khi phạm vi mới không kham được ≤6 tệp và ≤450 dòng thêm hoặc thực hiện ngoại lệ E2 theo ADR-0053. Ghi số đếm lịch sử là chưa xác minh và đo lại các số động trước mỗi lần công bố. Giữ phân loại §5 cho phiên chỉ dùng dữ liệu giả. Mọi phép xác minh cần đọc bundle thật thuộc E4.”

KET_LUAN: request_changes
rc=0 xong 2026-11-18T05:12:16Z
