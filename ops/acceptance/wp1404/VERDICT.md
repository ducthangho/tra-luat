# WP1404 r1 — verdict review độc lập

Nguồn có thẩm quyền là tệp này trong kho. Mỗi lượt chép nguyên văn `scratch/VERDICT.md` do reviewer ghi; sha256 ghi kèm
là băm của tệp gốc trong sandbox review.

## Lượt 1 — Codex (OpenAI), `codex_cli`, read-only · lời gọi 1/2

- Exact head được review: `141a3a73626791ab4be1853c1d684893f6ed54bf`. Chạy 2026-11-18T17:25:25Z → 17:29:06Z, rc 0.
- sha256 `scratch/VERDICT.md`: `93a16483cb82966cd9aa019d5ac46c55d6dfc5da1196430cc57cb82ed22353e6`.
- Kết luận: `request_changes` (2 P2, 2 P3).

### Nguyên văn

> reviewed_sha: 141a3a73626791ab4be1853c1d684893f6ed54bf  
> verdict: request_changes  
> reviewer: codex (OpenAI), codex_cli, read-only
> 
> ## Findings
> 
> - **P2 — Stdout lần cài đầu có thể ghi đè kết quả lần thử lại** — `ops/cai_cong_cu.sh:164`. Chuyển hướng bằng `>` cắt nội dung nhưng dùng lại inode. Probe `writer` chạy công thức `: && apt-get install -y ripgrep`. Lần đầu trả 100 và để tiến trình con giữ stdout. Lần hai in đường dẫn đúng rồi ra hiệu cho tiến trình con ghi đường dẫn hỏng qua FD cũ trước khi thoát. Script lấy đường dẫn hỏng từ stdout, báo rg chưa DAT và trả 3. Tạo tệp stdout mới cho lần thử lại, hoặc unlink tên tệp trước `continue` để lần mở tiếp theo tạo inode mới. Probe có đồng bộ bằng hai tệp dấu. Trên bản sao có unlink, cùng probe trả 0. Thêm probe này vào nhóm r868 hoặc r1404 và bắt buộc kiểm dấu writer đã ghi.
> - **P2 — Stdout của update làm hỏng đầu ra JSON** — `ops/cai_cong_cu.sh:173–174`. Hai lệnh update thừa kế stdout của script. Stub in `update-noise`, cài lại thành công và script trả 0, nhưng stdout bắt đầu bằng `update-noise\n{` nên không đọc được như JSON. Chuyển stdout của update sang stderr hoặc tệp log riêng ở cả hai nhánh. Bổ sung ca cho update in một dòng và parse toàn bộ stdout bằng `json.loads`, vẫn chốt nhật ký đúng ba bước.
> - **P3 — LAN_CAI chiếm tên biến của shell gọi khi source** — `ops/cai_cong_cu.sh:161–167`. Mỗi lượt cài đặt lại về 0 nên không kế thừa số lần thử của lượt trước. Tuy nhiên biến toàn cục vẫn còn giá trị 1 hoặc 2 sau khi source. Nếu shell gọi đã có biến cùng tên, giá trị bị ghi đè. Nếu biến là readonly, phép gán đầu tiên lỗi trước khi cài. Giới hạn bộ đếm bằng biến local trong hàm được gọi ở vị trí không điều kiện, giữ nguyên cách lấy mã thoát của subshell. Ca hồi quy nên source trong một vòng của shell gọi với `LAN_CAI` đã gán, buộc cài lại, rồi chốt giá trị của caller và số lượt vòng ngoài.
> - **P3 — Ca r1404 bỏ lọt các hành vi bắt buộc** — `.claude/dev/launcher_test.py:11317–11347,17180–17186`. Cả ba đột biến chính thức đều đỏ, nhưng chỉ bao phủ một phần B1 và nhánh loại lỗi ngoài apt của B3. B1 còn thiếu chốt sudo, `-qq`, kênh sạch và lấy mã lỗi mới. B2 không có đột biến, và B4 chỉ kiểm một cụm chữ. Fixture luôn trả 0 cho update, hai lần install trong ca luôn lỗi cùng trả 100, lần lỗi đầu không ghi kênh, sudo giả và lệnh trực tiếp cùng gọi một apt giả. Brew giả có mặt và rc được kiểm, nhưng lời gọi/đối số brew không được ghi. Giữ bốn ca N1, bổ sung nhật ký riêng cho sudo và toàn bộ argv, update lỗi với rc 78 và hai lượt install có rc 100/42, lần đầu ghi kết quả rồi lỗi và lần sau thành công qua stdout, cùng chốt stderr có đúng một dòng báo thử lại chứa tên và rc lần đầu. Bổ sung đột biến cho các chốt này và cho nhánh cập nhật khi lần đầu thành công. Ca thành công ngay hiện đã chốt nhánh đó bằng nhật ký.
> 
> ## Đối chiếu hành vi
> 
> - B1/B3. Vòng lặp chỉ update khi lần đầu khác 0 và chuỗi chứa `apt-get install`, kể cả ở giữa công thức. `sudo` chỉ được chọn khi chuỗi bắt đầu bằng `sudo apt-get`, đúng tiêu chí chữ của B1. Lượt hai thoát vòng dù rc là gì. Công thức brew lỗi và công thức apt thành công ngay không đi vào update. Bootstrap PyYAML của `--bat-buoc` vẫn có đường apt riêng từ base, ở dòng 90–95.
> - `while :` chỉ đặt lệnh `:` ở ngữ cảnh điều kiện. Subshell chạy công thức nằm trong thân vòng và giữ cơ chế wp1045. Phép gán số học ở dòng 167 trả trạng thái thành công với bộ đếm hợp lệ. `continue` thuộc vòng thử lại gần nhất, không nhảy vòng `for` bao quanh `source`. Probe batch thử cả thứ tự rg → bash và bash → rg. Mỗi thứ tự có đúng bốn bước apt, một update, ba tài liệu JSON và rc 0. Cờ `CAI_CONG_CU_PY_CUA` giữ nguyên đường xử lý kết quả. Nếu lượt hai thất bại, công cụ tùy chọn vẫn đi theo nhánh báo rồi `return 0` của base.
> - B2/B4. Update trả 78 vẫn dẫn tới lần install thứ hai, và wrapper trả 42 của lần hai, sau rc 100 của lần đầu. Khi mô phỏng sudo từ chối, có đủ ba lời gọi sudo và rc cuối là 126. Khi bỏ sudo khỏi PATH, hoặc bỏ apt-get và dùng công thức gọi thẳng, mỗi trường hợp có ba lỗi `command not found` và rc cuối 127. Không có cơ chế đổi sang quyền root. Dòng stderr báo thử lại trên probe có tên rg và rc lần đầu.
> - Kênh `KENH_KQ` được làm rỗng trước retry rồi mới đọc sau thành công. Dữ liệu stdout cũ đã ghi bị cắt, nhưng writer còn mở FD có thể ghi tiếp như finding P2.
> - B5. Diff base→head chỉ có hai tệp mã trong phạm vi và ba tệp hồ sơ. Từ `3d2035b` tới exact head chỉ thêm RESULTS.md.
> 
> ## Lệnh và mã thoát
> 
> - Đối chiếu `test "$(git -C repo rev-parse HEAD)" = "$(cat HEAD_SHA.txt)"`, `test -z "$(git -C repo status --porcelain=v1)"`, `sha256sum -c` với băm đặc tả đã cho — mỗi lệnh rc 0. `git -C repo diff --check e2c3b82f81..HEAD`, `git -C repo diff --exit-code 3d2035b..HEAD -- ops/cai_cong_cu.sh .claude/dev/launcher_test.py`, `bash -n repo/ops/cai_cong_cu.sh` — mỗi lệnh rc 0.
> - Trong clone `scratch/review`, `python .claude/dev/launcher_test.py --lap-ca r1404_cai_apt_update_roi_thu_lai --lan 3` — rc 0, 3/3.
> - Cùng lệnh với `--lan 1` cho các tên dưới đây — từng ca 1/1, rc 0. Xem `scratch/tests.log` để đối chiếu từng lần gọi.
>   - `r831_cai_rg_linux_chon_ban_chay_duoc`, `r831_cai_rg_macos_chon_ban_chay_duoc`, `r831_cai_rg_linux_python_ham_ke_thua`, `r831_cai_rg_macos_python_ham_ke_thua`.
>   - `r858_cai_linux_chon_ban_chay_duoc`, `r858_cai_macos_chon_ban_chay_duoc`, `r858_cai_windows_chon_ban_chay_duoc`, `r858_cai_python_khong_in_thu_muc_ban_hong`, `r858_bat_buoc_bash_khong_dua_rg_hong_len_dau`, `r858_hinh_dang_cong_thuc_cai`, `r858_selftest_editskill_thu_muc_rieng`.
>   - `r868_kenh_rieng_khong_doc_stdout_trinh_cai`, `r868_writer_muon_khong_lam_treo`, `r868_khong_bo_chon_doc_dong_cuoi`, `r868_doc_kenh_hong_thi_dung`, `r868_ghi_kenh_hong_thi_dung`, `r868_don_kenh_khi_loi`, `r868_vong_duyet_ung_vien`, `r868_hinh_dang_kenh_ket_qua`.
> - Cùng lệnh với `r858_goc_tam_tranh_to_tien_co_git --lan 1` — rc 1. Ca kiểm thư mục tạm, ngoài hành vi cài công cụ. Nó cố tạo tệp trong `/var/tmp` (filesystem chỉ đọc). `/tmp/.git` có mặt trong môi trường review.
> - `python .claude/dev/packet_loop.py doctrine-scan --root .` — rc 0, 12 tệp, 0 chỗ chép doctrine.
> - `python ../review_probe.py hooks` — rc 0, chạy harness với riêng ba hook wp1404, cả ba giết 1/1. `python ../review_probe.py clear|limit|sudo|b2|b4` (gọi riêng từng đối số) lần lượt rc **0, 1, 0, 0, 0**. Chỉ việc đổi `-eq 1` thành `-le 2` làm ca đỏ, với chuỗi `install update install update install`. Các đột biến còn sống lần lượt bỏ làm rỗng kênh, bỏ sudo khi update, làm lỗi update kích hoạt errexit, và bỏ tên/rc khỏi dòng báo thử lại. Một lượt khởi chạy ban đầu dùng sai chữ ký `main` trong runner tự viết. Các mã trên lấy từ lượt chạy lại sau khi sửa runner.
> - `python ../review_probe.py writer` — rc 1 (wrapper rc 3). `python ../review_probe.py writer_fixed` — rc 0 (wrapper rc 0). Các lệnh `python ../review_probe.py` với từng đối số `update_fail`, `sudo_denied`, `update_stdout`, `no_sudo`, `no_apt`, `batch` — mỗi probe rc 0, tức tái hiện đúng hành vi đã mô tả. Wrapper lần lượt trả 42, 126, 0 với stdout nhiễu, 127, 127 và 0 trên cả hai thứ tự batch.
> 
> ## RESULTS.md và phần không đo được
> 
> - Bốn kịch bản N1 được tái chạy cùng các chốt của executor, 3/3 so với 1/1 đã khai. Bảng kết quả khớp ở mức chốt hiện có. Mô tả ghi từng đối số rộng hơn phép đo thực tế, vì apt chỉ ghi `$1` và brew không ghi argv. Ba kết quả N2 đều khớp 1/1. Ở đột biến bỏ nhánh retry, update chưa chạy. Vì vậy mô tả “rc 100 sau update” ở hàng đầu của bảng N2 sai về thứ tự.
> - Doctrine scan khớp 12 tệp, rc 0. Đã xác minh exact head và mã cài/test giống `3d2035b`. Diff `6d52f57..3d2035b` xác nhận hai tệp mã thay đổi. Phép review này không chạy toàn suite hoặc toàn `--dot-bien`, nên chưa tái đo được 424/424, 425/425, 426/427 tổng, hai ca bỏ qua, 720/720, 721/723, 723/723 hoặc sáu đột biến không đo được. Chưa xác nhận delta hồi quy toàn bộ. Không có dòng `DOT BIEN:` của toàn bộ suite trong lần review này.
> - Chưa xác minh 19 lượt gate, 343 bước cài, một lỗi rc 100 trên run đã nêu, hoặc CI của PR #1406 trên exact head. Hai trang GitHub trả cache miss. Chưa chạy apt thật trên runner Ubuntu thiếu danh sách gói hay runner người dùng thường, macOS thật hoặc Windows thật. Các probe dùng stub, gồm cả trường hợp sudo từ chối quyền.

### Executor xử lý (sửa ở `921cbb6`)

| Finding | Kiểm lại | Xử lý |
|---|---|---|
| P2 stdout lần đầu ghi đè lần cài lại | Thật: `>` cắt nhưng giữ inode. Probe của reviewer dựng thành ca (e). | `rm -f -- "$TAM_CAI/stdout"` trước `continue`. Đột biến `wp1404_sh_dung_lai_inode_stdout` làm (e) đỏ. |
| P2 stdout của update làm hỏng JSON | Thật: script `3d2035b` đỏ ở ca (a) với `Expecting value: line 1 column 1`. | `apt-get update -qq >&2` ở cả hai nhánh. Đột biến `wp1404_sh_update_vao_stdout` làm (a) đỏ. |
| P3 `LAN_CAI` ở shell gọi khi `source` | Đúng là biến toàn cục. Nhưng trong chế độ `source`, script vốn đã gán `TEN` `LENH` `RC_CAI` `TAM_CAI` `KENH_KQ` `KQ` `DICH` `KET_QUA_CAI` ở shell gọi, và shell gọi là chính vòng `--bat-buoc` của script. `LAN_CAI=0` đặt lại ở mỗi lượt (probe `batch` của reviewer: hai thứ tự, mỗi thứ tự đúng một update). Một biến readonly cùng tên ở shell gọi cũng làm hỏng `RC_CAI` như vậy. | Không đổi. Đã thử thêm `unset LAN_CAI` rồi bỏ, vì dòng ấy không có phép đo nào phân biệt được. Không thêm hàm `local`, vì đặt lần chạy công thức vào hàm là đổi ngữ cảnh errexit mà wp1045 P3 đã chốt. |
| P3 ca test thiếu chốt | Thật. | Ca mới `r1404_thu_lai_chot_chi_tiet` gồm (a)–(e), cộng 8 đột biến (gồm `-eq 1`→`-le 2` của reviewer). Mỗi đột biến chết đúng kịch bản nhắm tới (RESULTS.md §4). Dòng làm rỗng kênh nay có răng nhờ (d): bộ chọn ghi kênh rồi một bước sau lỗi. |
| RESULTS.md N2: "rc 100 sau update" sai thứ tự | Thật: đột biến `bo_thu_lai_apt` không chạy update. | Sửa câu ở RESULTS.md §4. |

## Lượt 2 — Codex (OpenAI), `codex_cli`, read-only · lời gọi 2/2 (hết ngân sách lease)

- Exact head được review: `f9eba6e8b346c274b7f9342e5b53d844089298be` (mã trùng `921cbb6`). Chạy 2026-11-18T17:45:31Z → 17:54:12Z, rc 0.
- sha256 `scratch/VERDICT.md`: `4dcd255881706bb8893231c8b182184ffa99d708c6948f39e4378faa86815fa4`.
- Kết luận: `request_changes` (1 P2, 3 P3). Hai P2 của lượt 1 reviewer xác nhận ĐÃ ĐÓNG.
- Ghi chú về `git diff --check` mà reviewer nêu: khoảng trắng cuối dòng trong phần nguyên văn là của chính tệp gốc
  (ngắt dòng Markdown); giữ nguyên để băm khớp.

### Nguyên văn

> reviewed_sha: f9eba6e8b346c274b7f9342e5b53d844089298be
> verdict: request_changes
> reviewer: codex (OpenAI), codex_cli, read-only
> 
> Tree `8c64eeb110e01a9622ff5bfc6cd21ed3aac385bd`. Linux, Python 3.13.18, Bash 5.2.21, transport machine/local. Head khớp `HEAD_SHA.txt`, cây sạch, SHA-256 đặc tả khớp `1eb8f4428e0da7c2074b94938e89990c3f3bd681b254bcacccb2336a76a5314d`. Diff base → head nằm trong write set. Hai tệp mã trùng với `921cbb6`.
> 
> ## Findings
> 
> - **P2 · Writer muộn có thể ghi lại kênh kết quả lần đầu sau khi kênh đã được làm rỗng** — `ops/cai_cong_cu.sh:80,144,179,195`. Công thức của probe `late_channel` để một subshell nền giữ giá trị `KENH_KQ`, rồi trả 100 từ install. Retry in đường dẫn tốt ra stdout và báo hiệu cho subshell nền gọi bộ chọn, mở lại kênh bằng đường dẫn cũ và ghi thư mục khác. Probe chốt writer đã ghi và làm thư mục đó hỏng sau khi ghi. Trình cài đọc lại kênh, chọn thư mục hỏng và trả 3 dù lần retry trả 0. Cấp **đường dẫn mới** cho kênh lần hai, giữ thuộc tính không export, rồi dọn cùng thư mục tạm. Unlink và tạo lại cùng tên vẫn cho phép writer mở lại đường dẫn. Thêm biến thể của (e) gọi bộ chọn trong subshell nền và chốt dấu writer cùng kết quả `DAT`. Cùng probe trên bản sao cấp đường dẫn mới trả 0.
> 
> - **P3 · Bước CI kế tiếp có thể nhận đường dẫn từ lần cài thất bại** — `ops/cai_cong_cu.sh:73–80,179` và `.claude/dev/launcher_test.py:11402–11410`. Ngay fixture (d) ghi `tot2` vào `GITHUB_PATH` trước `false`. Sau update, `tot2/rg` hỏng. Retry qua stdout làm checker hiện tại báo `DAT`, nhưng tệp dùng để cấp PATH cho bước kế tiếp vẫn chỉ có `tot2`. Probe `channel` đo wrapper rc 0, `DAT` và dòng `tot2`. Khi mô phỏng bước CI kế tiếp bằng cách đưa dòng này lên đầu PATH, `rg --version` trả 1 dù thư mục tốt cũng có trong PATH. Các công thức apt hiện hành đều kết thúc bằng bộ chọn, nên tôi tái hiện bằng công thức của (d). Hoãn ghi đường dẫn ra `GITHUB_PATH` tới khi công thức thành công, hoặc giữ phần ghi theo từng lần cài và chỉ chuyển phần thành công vào tệp CI. Mở rộng (d) để chốt update đã chạy, `tot2` vắng khỏi tệp và mô phỏng PATH của bước kế tiếp.
> 
> - **P3 · Xung đột `LAN_CAI` khi source vẫn còn** — `ops/cai_cong_cu.sh:164–171`. Probe source hai lượt trong vòng ngoài ghi nhận `LAN_CAI` của caller đổi từ 42 thành 2, rồi 1. Cả hai lượt vòng ngoài vẫn chạy. Khi caller khai readonly, script dừng ở dòng 164 với rc 1 trước khi cài. Lý do của executor giải thích vì sao batch nội bộ hiện an toàn: vòng cha dùng `cong_cu`, không dùng `LAN_CAI`, và bộ đếm luôn được khởi tạo lại. Những biến toàn cục có từ base không loại bỏ xung đột mới. Gọi một hàm ở vị trí câu lệnh độc lập với bộ đếm `local` tên có tiền tố riêng có thể giữ nguyên ngữ cảnh errexit. Chốt bằng ca gọi source trong vòng của caller, kiểm giá trị caller và hai lượt, kèm probe công thức tự bật `set -e`.
> 
> - **P3 · Còn ba lỗ đo ở nhánh update gọi thẳng** — `.claude/dev/launcher_test.py:11393–11401,17270`. (c) ghi `$1`, update im lặng và trả 0. Bỏ `-qq`, bỏ chuyển stdout hoặc bỏ nhánh xử lý lỗi update ở nhánh gọi thẳng đều sống qua ca chi tiết. Ví dụ lệnh update trần trả 78 sẽ chặn hẳn lần cài lại nếu bỏ `||`; (b) chỉ phát hiện lỗi này ở nhánh sudo. Mở rộng (c) để ghi toàn argv, in một dòng rác, cho update trả 78 và chốt JSON cùng mã lần cài lại. Ca brew cũ chốt rc và apt log rỗng, còn lời gọi và argv brew chỉ có trong fixture. Có thể ghi nhật ký brew riêng nếu muốn chốt nó trực tiếp.
> 
> ## Đóng findings lượt 1
> 
> | Finding | Lượt 2 |
> |---|---|
> | P2 inode stdout dùng lại | Đã đóng. `writer` trên `3d2035b` probe rc 1, wrapper rc 3. Trên head probe rc 0, wrapper rc 0, marker writer có mặt. Ca (e) và đột biến bỏ unlink đo đúng lỗi này. |
> | P2 stdout update phá JSON | Đã đóng. `update_stdout` trên `3d2035b` probe rc 1, wrapper rc 0 với JSON nhiễu. Trên head probe và wrapper đều rc 0, parse toàn bộ JSON thành công, dòng nhiễu có trong stderr. |
> | P3 `LAN_CAI` | Còn mở khi source từ caller có biến cùng tên. Batch nội bộ đã được chạy lại theo cả hai thứ tự, từng thứ tự đúng bốn lệnh apt, đúng một update và wrapper rc 0. |
> | P3 thiếu chốt | Đóng các thiếu sót chính ở nhánh sudo, mã lỗi cuối, dòng stderr, kênh ghi sớm và stdout writer. Còn các lỗ đo nêu trên. |
> 
> ## Đọc B1–B5 và ca (a)–(e)
> 
> - B1/B3. Điều kiện retry đòi rc khác 0, lượt 1 và chuỗi chứa `apt-get install`, kể cả khi ở giữa công thức. Mẫu sudo xét đầu chuỗi theo đúng đặc tả. Lượt 2 luôn rời vòng. Ca cài được ngay chỉ ghi install. Ca brew lỗi không gọi apt. Bootstrap PyYAML của batch có update riêng tại dòng 90–95, kế thừa từ base.
> - `while :` chỉ đặt `:` vào điều kiện. Dòng eval nằm trong thân vòng, chạy độc lập và thu `$?` trước khi bật lại errexit. Probe công thức chứa lệnh apt ở giữa, tự bật `set -e` rồi `false`, đo rc lần đầu 1 và retry thành công. Phép gán số học của bộ đếm hợp lệ trả 0. `continue` tiếp tục vòng retry trong cùng lượt source. Ba ca r1045 về batch và cờ `CAI_CONG_CU_PY_CUA` đều qua.
> - B2/B4. Update trả 78 vẫn chạy install lần hai và trả rc 42. PATH giới hạn thiếu sudo hoặc apt-get cho ba lỗi tìm lệnh và rc cuối 127. Stub sudo từ chối quyền ghi ba lời gọi và rc cuối 126. Không có fallback nâng quyền. Thông báo thử lại có tên và rc đầu. B5 được xác nhận bằng diff.
> - (a) Đo đúng chuỗi argv của apt và sudo, đầu ra là một tài liệu JSON và đúng một thông báo thử lại có tên và rc. (b) Đo đúng update lỗi và lấy rc mới. (c) Đo lệnh gọi thẳng và không có sudo qua nhật ký, với giới hạn nêu trong finding.
> - (d) Có đi qua retry. Ban đầu marker chưa có, apt trả 0, bộ chọn ghi kênh và `false` làm nhánh `else` và toàn công thức trả 1. Update tạo marker, khiến lượt hai đi vào `then`, in đường dẫn tốt và trả 0. Bỏ làm rỗng kênh khiến đúng (d) đỏ với wrapper rc 3. (d) không kiểm tệp `GITHUB_PATH` hoặc writer tới muộn.
> - (e) Đo đúng writer giữ FD stdout, có marker hoàn thành và phép thử bỏ unlink đỏ. Vòng chờ bên writer có giới hạn, nhưng để fixture chặt hơn nên yêu cầu marker cho phép tồn tại trước khi ghi, kể cả khi hết thời gian chờ.
> - Ba hook ban đầu đo bỏ nhánh retry, retry lỗi ngoài apt và update mà bỏ cài lại. Tám hook bổ sung đo giới hạn số lần, stderr/JSON, hai nhánh chọn sudo, B2 trên nhánh sudo, tên/rc đầu, kênh ghi sớm và inode stdout. Ca cài thành công ngay có phép đo B3 nhưng thiếu hook chính thức nhắm riêng điều kiện rc khác 0. Đột biến riêng bỏ điều kiện đó đã đỏ.
> 
> ## Lệnh và mã thoát
> 
> - `git clone --no-local repo scratch/head`, tương tự cho `scratch/base`, checkout base detached và đặt `core.abbrev 7` cho hai bản sao. Chuỗi clone/checkout rc 0. Kiểm SHA, cây sạch và `sha256sum -c` từng lệnh rc 0. `git diff --exit-code 921cbb6..HEAD -- ops/cai_cong_cu.sh .claude/dev/launcher_test.py`, `bash -n repo/ops/cai_cong_cu.sh` và diff check cho hai tệp mã rc 0. Diff check toàn packet rc 2 do khoảng trắng cuối dòng trong trích dẫn verdict ở `ops/acceptance/wp1404/VERDICT.md:14–47`. Xem `diff-check.log`.
> - Trong `scratch/head`, `python .claude/dev/launcher_test.py --lap-ca r1404_cai_apt_update_roi_thu_lai --lan 3` và tương tự cho `r1404_thu_lai_chot_chi_tiet` đều rc 0, 3/3. Cùng lệnh `--lan 1` cho 19 ca r831/r858/r868 liên quan script và 3 ca r1045 về batch đều rc 0, 1/1. Ca môi trường `r858_goc_tam_tranh_to_tien_co_git` rc 1 do tự chọn `/var/tmp` chỉ đọc khi thấy `/tmp/.git`. Từng tên ca và rc nằm trong `targeted.log`.
> - `python ../probe.py hooks` rc 0. Chạy từng hook bằng harness gốc, giết **3/3 cũ và 8/8 mới**, từng hook 1/1, bỏ qua 0. Xem `probes.log`.
> - `python ../mutate.py` với từng đối số `success`, `direct_args`, `direct_stdout`, `direct_abort`, `clear` lần lượt rc **1, 0, 0, 0, 1**. Hai ca đỏ ném `TinHieuChotCa`. Xem `mutants.log`.
> - `python ../probe.py` với `writer`, `update_stdout`, `channel`, `late_channel`, `source`, `readonly` lần lượt probe rc **0, 0, 1, 1, 1, 1**, wrapper rc **0, 0, 0, 3, 0, 1**. `late_channel ../cai-new-channel.sh` probe và wrapper rc 0. `no_sudo`, `no_apt`, `sudo_denied`, `errexit`, `batch` mỗi probe rc 0. Hai lần dựng probe ban đầu đã sửa fixture trước khi lấy kết quả: công thức nhiều dòng không hợp giao thức YAML của `cai-lenh`, và mẫu argv của stub batch thiếu đối số thứ ba.
> - `python .claude/dev/packet_loop.py doctrine-scan --root .` rc 0, 12 tệp, 0 vị trí. `python ops/bash_nen.py quet --root .` rc **2 trên cả base và head**. `diff -u scratch/bash-base.log scratch/bash-head.log` rc 0. Hai lỗi y hệt nhau tại `ops/land/pr1386-wp646-provenance/linux/n1env_1386.py:30` và `n1rig_1386.py:25`, và diff hai tệp đó rc 0.
> 
> ## Đối chiếu RESULTS.md
> 
> - §1. Log GitHub của job `134953391585` xác nhận bước cài rg dừng với `Unable to locate package ripgrep`, rc 100, trước các bước probe và selftest. Chưa kiểm đếm lại 19 lượt gate, 343 bước và tổng số lỗi trong cả mẫu. [Job gốc](https://github.com/ducthangho/tra-luat/actions/runs/44347295196/job/134953391585)
> - §2–§4. Diff khớp mô tả thay đổi. Hai ca lặp 3/3 thay cho 2/2 của executor, đủ bốn kịch bản N1 và năm kịch bản chi tiết với giới hạn đã nêu. Cả 11 hook wp1404 giết 1/1. Phản chứng bằng script cũ tái hiện JSON nhiễu và writer stdout. Không xác nhận tuyên bố fixture (d) như một phép đo cách ly toàn bộ đầu ra, vì nó chỉ kiểm trạng thái hiện tại.
> - §5. Đếm trực tiếp registry bằng `python ../probe.py counts`, rc 0 trên cả hai bản sao: base 426 ca/726 hook và đột biến tổng cộng, head 428/737. Khớp delta +2 ca, +11 đột biến. Tôi chạy đầy đủ `TMPDIR="$PWD/../tmp" python .claude/dev/launcher_test.py` trong từng bản clone. Base rc 1, **401/416 qua, 10 bỏ qua, 15 hỏng**. Head rc 1, **403/418 qua, 10 bỏ qua, 15 hỏng**. So danh sách ca hỏng/bỏ qua bằng `diff -u scratch/suite-names-base.log scratch/suite-names-head.log` rc 0. Delta +2 ca qua, 0 ca hỏng hoặc bỏ qua mới trong sandbox. Các lỗi chung gồm `/var/tmp` chỉ đọc và fixture xác thực nằm dưới cây có `.git`. Tám skip thêm so với executor đều báo không dựng được venv/pip. Vì vậy chưa tái lập các số tuyệt đối 424/424, 425/425, 426/426 và hai skip của executor. Xem `suite-base.log` và `suite-head.log`. Đếm đăng ký không xác minh số đo được. Diff lịch sử xác nhận `6d52f57` có hai dòng eval và `3d2035b` trở đi còn một. Các số toàn `--dot-bien` 720/720, 721/723, 723/723, 731/731 và sáu ca không đo được là lời khai executor. Lượt này chạy riêng wp1404 nên không có dòng tổng `DOT BIEN:`.
> - §6. Doctrine scan khớp. Đọc trực tiếp ba job CI xác nhận cả ba đỏ ở G5 và log nêu đúng hai tệp. Quét local base/head xác nhận delta 0 của báo cáo. Chưa xác minh tuyên bố lượt push trên master không chạy `cong_cu_test`. Trên exact head, job gate `135006578500` đã kết thúc đỏ ở G5 và log nêu đúng hai tệp trên. Workflow Windows bỏ qua. N4 chưa đạt. [CI 3d2035b](https://github.com/ducthangho/tra-luat/actions/runs/44356207824/job/134985225080), [CI 141a3a7](https://github.com/ducthangho/tra-luat/actions/runs/44358498604/job/134993417970), [CI 5505f7a](https://github.com/ducthangho/tra-luat/actions/runs/44359968089/job/134998669752), [gate exact head](https://github.com/ducthangho/tra-luat/actions/runs/44362172770/job/135006578500).
> - §7. Đã đo xung đột `LAN_CAI`. Kiểm thử hành vi cài dùng stub, không chạy apt thật trên runner thiếu danh sách gói, không chạy trên macOS/Windows thật.

### Review Rescue Checkpoint sau lượt 2

Ngân sách Codex trong lease đã hết (2/2), nên executor dừng và hỏi chủ kho. Chủ kho chọn qua AskUserQuestion
(18-11-2026, khoảng 22:35Z): **"Sửa 3, nợ 1, Codex lượt 3"**. Lease ghi `nang_tran` 2→3 và `gia_han` tới 2026-11-19T04:51:13Z.

### Executor xử lý (sửa ở `6b0e375`)

| Finding | Kiểm lại | Xử lý |
|---|---|---|
| P2 writer muộn ghi lại kênh lần đầu | Thật. Ca (f) dựng từ probe `late_channel` của reviewer: script `921cbb6` ĐỎ, rc 3. | Lần cài lại dùng đường dẫn kênh MỚI `$TAM_CAI/kq-thu-lai` (`export -n` vì allexport tự export phép gán). Đột biến `wp1404_sh_giu_kenh_lan_dau` (giữ đường dẫn cũ) làm (f) đỏ; `wp1404_sh_kenh_moi_lo_export` làm (h) đỏ; `wp1404_sh_kenh_moi_khong_tao` làm (d) đỏ (rc 7). |
| P3 `GITHUB_PATH` của lần cài lỗi | Thật với công thức dạng (d). Mọi công thức apt hiện có kết thúc bằng bộ chọn nên hiện không xảy ra. | **Nợ có tên `WP1404-GITHUB-PATH-LAN-LOI`**, theo quyết định của chủ kho. Sửa đúng phải hoãn ghi `GITHUB_PATH` trong `chon_thu_muc_chay_duoc` (bộ chọn của wp858) tới khi công thức thành công; ngoài phạm vi đã duyệt của packet này. |
| P3 `LAN_CAI` ghi đè biến shell gọi | Thật: probe `source`/`readonly` của reviewer. | Bỏ vòng và biến đếm. Dòng `eval` nằm trong hàm `_wp1404_chay_cong_thuc` gọi hai lần (bốn dòng thân không thụt lề, giữ nguyên neo của `r1045_hinh_dang…` và đột biến wp1045). Ca (g) chạy `source` hai lượt từ shell gọi có `readonly LAN_CAI=42`; đột biến `wp1404_sh_bien_dem_toan_cuc` làm (g) đỏ. Hàm là một tên MỚI ở shell gọi khi `source`; tên có tiền tố packet. |
| P3 lỗ đo nhánh update gọi thẳng | Thật. | (c) tách thành (c1) toàn argv + update in rác + stdout JSON và (c2) update rc 78, cài lại rc 42 ⇒ thoát 42. Ba đột biến `wp1404_sh_tran_*` (bỏ `>&2`, bỏ `-qq`, bỏ `\|\| echo`) làm (c1)/(c2) đỏ. (e) chặt hơn: writer chỉ ghi khi đã được phép. |

Bảng đột biến loại `cai_sh` (65, gồm 17 của wp1404) chạy riêng: 65/65 giết, không neo nào khớp sai. Lần đầu đo ra 64/65:
dòng `declare +x KENH_KQ` mới làm neo `wp868_sh_kenh_export` khớp hai chỗ; đổi sang `export -n KENH_KQ`.

## Lượt 3 — Codex (OpenAI), `codex_cli`, read-only · lời gọi 3/3 (trần sau `nang_tran`)

- Exact head được review: `0b3cda8e23addf3bc7d63427ac1543b0fc1fe591` (mã trùng `6b0e375`). Chạy 2026-11-18T22:54:51Z → 23:04:11Z, rc 0.
- sha256 `scratch/VERDICT.md`: `becbda8e8e7da4a19174e9b7a80cb421b792876f1643ad48630020dd2b2f514c`.
- Kết luận: `request_changes` (0 P0/P1/P2, 1 P3). Mọi finding lượt 2 (trừ nợ `WP1404-GITHUB-PATH-LAN-LOI`) reviewer xác nhận ĐÃ ĐÓNG.
- Liên kết tương đối trong nguyên văn trỏ tới tệp trong sandbox review, không có trong kho.

### Nguyên văn

> reviewed_sha: 0b3cda8e23addf3bc7d63427ac1543b0fc1fe591
> verdict: request_changes
> reviewer: codex (OpenAI), codex_cli, read-only
> 
> Tree `f29ccecc7fca2c6668c88dff69e2052af29d63f3`. Linux, Bash 5.2.21, Python 3.13.18, transport machine/local. HEAD khớp `HEAD_SHA.txt`, worktree sạch, SHA-256 đặc tả khớp `1eb8f4428e0da7c2074b94938e89990c3f3bd681b254bcacccb2336a76a5314d`. Diff base → head nằm trong write set. Hai tệp mã trùng `6b0e375`. Lease ghi nâng trần 2→3 và gia hạn tới 04:51:13Z ngày 19-11.
> 
> ## Findings
> 
> - **P3 · Hàm mới làm mất tham số vị trí của công thức** — `ops/cai_cong_cu.sh:165–171`, `:184`. Trước delta, `eval` trong subshell thấy tham số của script hoặc lượt `source`. Hai lời gọi hàm mới truyền 0 đối số, nên công thức YAML như `test "${1-}" = rg && apt-get install -y ripgrep && chon_thu_muc_chay_duoc rg …` trượt ngay ở `test`. Với stub install luôn thành công, bản lượt 2 cài ngay và trả 0, head chỉ gọi `update -qq` rồi trả 1. Khi stub cần update trước, bản lượt 2 chạy `install update install` rồi trả 0, head vẫn chỉ chạy update. Các công thức hiện tại trong YAML chưa dùng tham số vị trí. Truyền `"$@"` ở cả hai lời gọi độc lập và giữ nguyên dòng neo `eval`. Cập nhật các neo đột biến khớp lời gọi khi thêm đối số. Hai probe `positions` và `positions_retry` đều qua trên bản sao sửa theo cách này. Thêm fixture YAML dùng `${1-}` với hai stub trên, chốt rc, `DAT` và nhật ký chính xác.
> 
> ## Đóng findings lượt 2
> 
> | Finding | Kết quả kiểm lại |
> |---|---|
> | P2 writer muộn ghi lại kênh lần đầu | Đã đóng. `late_channel` dựng lại từ mô tả lượt 2 xác nhận writer hoàn thành. Probe/wrapper rc **0/0** trên head và **1/3** với script `f9eba6e`. |
> | P3 `LAN_CAI` đụng biến caller | Đã đóng. `source` và `readonly` đều probe/wrapper rc **0/0** trên head, giữ 42 qua hai lượt vòng ngoài với cờ `CAI_CONG_CU_PY_CUA=$$`. Trên `f9eba6e`, tương ứng **1/0** (biến đổi thành 2 rồi 1) và **1/1** (readonly). |
> | P3 ba lỗ đo nhánh gọi thẳng | Đã đóng. (c1) bắt mất `-qq`, bỏ đổi đích stdout hoặc thêm sudo. (c2) bắt dừng ở rc 78 của update. |
> | `WP1404-GITHUB-PATH-LAN-LOI` | Hồ sơ ghi đúng phạm vi fixture (d) và quyết định giữ nợ của chủ kho. Fixture chốt `DAT`; nội dung tệp CI nằm ngoài assertion. |
> 
> ## B1–B5 và ngữ cảnh shell
> 
> - B1/B3. Nhánh mới chỉ xét chuỗi có `apt-get install` sau rc khác 0, kể cả chuỗi nằm giữa công thức. Lệnh update chọn sudo theo tiền tố của đặc tả. Luồng có một lời gọi đầu và tối đa một lời gọi lại, sau đó đi thẳng vào xử lý kết quả. Vòng retry, `continue` và phép gán số học của lượt 2 đã bị bỏ. Bootstrap pip của `--bat-buoc` tại dòng 90–95 vẫn có update riêng từ base.
> - Hai lời gọi hàm là câu lệnh độc lập. Lời gọi trong thân nhánh `case` không mang ngữ cảnh kiểm điều kiện của `if`. Hai probe công thức bật lại `set -e` xác nhận lệnh sau lỗi bị bỏ qua. Lỗi 1 ở lượt đầu kích hoạt update rồi wrapper trả 0. Lỗi 42 trong lượt hai đi thẳng ra wrapper với rc 42. Giữ nguyên thân hàm không thụt lề bảo toàn neo, bao gồm ca hình dạng r1045.
> - B2/B4. Thiếu sudo (apt giả vẫn có trên PATH) hoặc thiếu apt-get ở công thức gọi thẳng đều cho ba lỗi tìm lệnh và rc cuối 127. Stub sudo từ chối cho ba lời gọi đúng argv và rc cuối 126. (b)/(c2) đo update rc 78 rồi retry rc 42. (a) chốt đúng một dòng báo retry chứa tên và rc lần đầu.
> - Kênh và stdout. Retry mở `kq-thu-lai`, huỷ export của phép gán, và unlink stdout trước lần mở mới. Dòng 196 đọc giá trị hiện hành của `KENH_KQ`. Hai probe source thấy chuỗi `kq → kq-thu-lai → kq`, nhận `DAT` ở cả hai lượt và ghi đúng `install update install install`. Hai probe allexport, dùng `bash -a` và `SHELLOPTS=allexport`, xác nhận cả hai biến thực sự vắng trong môi trường của stub ở cả ba lời gọi.
> - B5. Diff xác nhận YAML, launcher, hook và workflow giữ nguyên.
> 
> ## Ca test và đột biến
> 
> - N1 lặp 3/3. Ca đo nhật ký apt qua `$1`, mã lỗi, và `DAT` khi khôi phục. Stub brew có mặt và trả 1. Ca đo rc và apt log rỗng. Lời gọi brew và argv brew chưa có nhật ký riêng. Nhánh B3 cài thành công ngay có assertion, nhưng thiếu hook đăng ký nhắm riêng việc bỏ điều kiện rc khác 0. Đột biến độc lập bỏ điều kiện ấy đỏ. Giới hạn số lần, loại công thức, sudo, B2, tên/rc B4 đều có hook.
> - Ca chi tiết lặp 3/3. (a)/(c1) chốt toàn argv và parse toàn bộ stdout. (b)/(c2) chốt mã cuối và nhật ký. (d) chốt bỏ kết quả lần đầu. (e)/(f) chốt marker writer cùng `DAT`. (g) chốt hai lượt vòng ngoài, giá trị readonly và hai thông báo retry. (h) chốt ba dòng nhật ký không có giá trị hai biến, và giết hook làm lộ đường dẫn thật. Biểu thức `${VAR:-VANG}` của (h) gộp vắng với rỗng. Probe riêng dùng `${VAR+SET}` và kiểm cả hai cách bật allexport. Hai probe errexit và kiểm tên kênh của lượt source kế tiếp cũng là bằng chứng bổ sung ngoài các chốt của ca chi tiết.
> - Ba hook gốc N2 đều giết 1/1. Cả 17 hook wp1404 ném `TinHieuChotCa` đúng kịch bản. Sáu hook mới lần lượt đỏ ở (d) rc 7, (h) lộ đường dẫn, (g) rc 1 readonly, (c1) JSON, (c1) argv thiếu `-qq`, (c2) rc 78. Hook giữ kênh cũ đỏ ở (f) rc 3, hook giữ inode stdout đỏ ở (e) rc 3.
> - Bốn đột biến riêng đều đỏ bằng assertion: bỏ tạo kênh mới, thêm lượt update/install thứ hai, bỏ sudo ở update và ép retry cả khi thành công. Head đã bỏ bộ đếm, nên đột biến giới hạn được dựng bằng cách thêm một cặp update/install.
> 
> ## Lệnh và mã thoát
> 
> - `git clone --no-local repo scratch/head`, `git clone --no-local repo scratch/base`, checkout base detached, và đặt `core.abbrev 7` trong hai clone đều hoàn tất. Hai diff yêu cầu đều rc 0 và lưu ở [base-head.diff](base-head.diff), [delta.diff](delta.diff). Các phép xác minh HEAD/cây sạch/spec, `git diff --exit-code 6b0e375..HEAD` trên hai tệp mã, `git diff --check` trên hai tệp mã và `bash -n` đều rc 0. Xem [preflight.log](preflight.log).
> - `python .claude/dev/launcher_test.py --lap-ca TEN --lan 3` cho hai ca r1404, từng lệnh rc 0. Cùng entry point với `--lan 1` cho 19 ca r831/r858/r868 liên quan script và 5 ca r1045, từng lệnh rc 0. Ca môi trường `r858_goc_tam_tranh_to_tien_co_git` rc 1 vì `/tmp/.git` có mặt và `/var/tmp` chỉ đọc. Từng tên ca và rc ở [targeted.log](targeted.log).
> - `python ../probe.py TEN [SCRIPT]` từ clone head. Trên head, `late_channel`, `source`, `readonly`, `errexit`, `errexit_retry`, `allexport_env`, `allexport_flag`, `no_sudo`, `no_apt`, `sudo_denied` đều probe rc 0. Wrapper lần lượt trả **0, 0, 0, 0, 42, 0, 0, 127, 127, 126**. Probe `positions` và `positions_retry` rc 1 trên head, rc 0 với script `f9eba6e` và bản sao chuyển tiếp đối số. [probes.log](probes.log) · [extra.log](extra.log) · [positions-retry.log](positions-retry.log)
> - `python ../history.py ../round1.sh` và `python ../history.py ../round2.sh` cùng rc 1 do assertion, lần lượt tại (a) và (f), dùng script lịch sử `3d2035b` và `f9eba6e`. `python ../mutations.py details` rc 0, runner ghi 17 hook và 4 đột biến riêng đều đỏ. Lần đầu gọi runner lọc `cai_sh` in `(0, 0)` rồi trả rc 1 vì wrapper truyền tuple vào `sys.exit`. Lần đo xác nhận `python ../mutations.py all` rc 0, **65/65**, không có hook bỏ qua hay neo sai. [mutations.log](mutations.log) · [cai-sh-verified.log](cai-sh-verified.log)
> - `python .claude/dev/packet_loop.py doctrine-scan --root .` rc 0 trên base và head (12 tệp, 0 vị trí). `python ops/bash_nen.py quet --root .` rc 2 ở cả hai; diff hai log rc 0. Hai lỗi cùng nằm tại `ops/land/pr1386-wp646-provenance/linux/n1env_1386.py:30` và `n1rig_1386.py:25`. Diff thư mục chứa chúng rc 0. [checks-base.log](checks-base.log) · [checks-head.log](checks-head.log)
> 
> ## Đối chiếu RESULTS.md
> 
> - §1. GitHub xác nhận job `134953391585` lỗi ở bước cài rg, log có `Unable to locate package ripgrep` và rc 100, rồi bỏ qua G5 và selftest. Chưa kiểm đếm lại mẫu 19 lượt gate, 343 bước và tổng một lỗi. [Job gốc](https://github.com/ducthangho/tra-luat/actions/runs/44347295196/job/134953391585)
> - §2–§3b. Diff xác nhận hai tệp mã trùng `6b0e375`. Cả hai ca đạt 3/3, so với 2/2 executor ghi. Hai phản chứng lịch sử khớp (a) và (f); `git diff --exit-code 921cbb6..f9eba6e -- ops/cai_cong_cu.sh` rc 0. Mô tả thời điểm (f) cần đọc chính xác hơn. Writer ghi sau khi lượt hai đã **in đường dẫn**, trong lúc lượt hai đang đợi marker, rồi wrapper mới đọc kết quả. Mô tả (h) về sự vắng mặt được xác nhận bởi probe riêng như ở trên. Fixture (g) gọi `source` trong vòng riêng; các probe `source` và `readonly` của review còn bật cờ batch.
> - §4. Tái lập cả 17/17 và 65/65. Hàng `wp1404_sh_nhanh_tran_dung_sudo` thực tế đỏ tại (c1), nơi bảng vẫn gọi tắt (c).
> - §5. Đếm registry runtime bằng `python ../mutations.py counts` trên base và runner `cai_sh` trên head. Đếm AST qua `git show REF:.claude/dev/launcher_test.py` (rc 0) cho chuỗi ca/đột biến đăng ký **426/726 → 427/729 → 427/729 → 428/737 → 428/743**, theo thứ tự base, `6d52f57`, `3d2035b`, `921cbb6`, `6b0e375`. Head cũng là 428/743. Delta đăng ký +2/+17 khớp. `git show` và đếm dòng xác nhận hai neo eval ở `6d52f57` và một ở các bản sau.
> - §5. Chạy toàn bộ `python .claude/dev/launcher_test.py` với `TMPDIR` trong scratch trên cả hai clone. Base rc **1**, **400/416** qua, 10 bỏ qua, 16 hỏng. Head rc **1**, **402/418** qua, 10 bỏ qua, 16 hỏng. `diff -u scratch/suite-names-base.log scratch/suite-names-head.log` rc 0. Delta quan sát là +2 ca qua, 0 ca hỏng hoặc bỏ qua mới. Hai bên cùng có lỗi filesystem `/var/tmp`, fixture credential nằm dưới cây có `.git` và ca ngắt tiến trình t72 ghi trạng thái `xong`. Ngoài hai skip nền executor báo, tám ca ở mỗi vế báo lỗi dựng venv/pip. Số tuyệt đối 424/424, 425/425, 426/426 và hai skip của executor chưa tái lập trong sandbox này. [Suite base](suite-base.log) · [Suite head](suite-head.log)
> - §6. Doctrine scan khớp; ba log CI lịch sử nêu đúng hai tệp đã có ở base. GitHub báo gate trên exact SHA đang chạy và Windows bị bỏ qua ở lần kiểm tra, vì vậy chưa có bằng chứng xanh N4. Chưa kiểm lại tuyên bố về workflow push master. [CI 3d2035b](https://github.com/ducthangho/tra-luat/actions/runs/44356207824/job/134985225080) · [CI 141a3a7](https://github.com/ducthangho/tra-luat/actions/runs/44358498604/job/134993417970) · [CI 5505f7a](https://github.com/ducthangho/tra-luat/actions/runs/44359968089/job/134998669752) · [Gate exact SHA](https://github.com/ducthangho/tra-luat/actions/runs/44416024897) · [Windows exact SHA](https://github.com/ducthangho/tra-luat/actions/runs/44416024928)
> 
> ## Phần chưa đo được
> 
> - Không chạy toàn bộ `--dot-bien`. Các số 720/720, 721/723, 723/723, 731/731, 737/737 và sáu đột biến không đo được vẫn là lời khai executor. Phép đo lọc `cai_sh` chỉ có dòng tổng **65/65**, không có dòng `DOT BIEN:` của toàn bộ bộ đột biến.
> - Các probe cài dùng stub. Chưa chạy apt thật trên runner Ubuntu thiếu danh sách gói, thử quyền sudo thật, hoặc chạy trên macOS/Windows thật.

### Review Rescue Checkpoint lần hai

Trần Codex sau nâng (3/3) đã hết. Chủ kho chọn qua AskUserQuestion (18-11-2026, khoảng 23:22Z): **"Sửa + Codex lượt 4
delta"**. Lease ghi `nang_tran` 3→4.

### Executor xử lý (sửa ở `b0e9866`)

| Finding | Kiểm lại | Xử lý |
|---|---|---|
| P3 hàm làm mất tham số vị trí | Thật. Ca (i) với công thức `test "${1-}" = rg && apt-get install -y ripgrep && chon_thu_muc_chay_duoc …`: script `6b0e375` ĐỎ (cài được ngay ⇒ rc 1, nhật ký chỉ `update`). | `_wp1404_chay_cong_thuc "$@"` ở cả hai lời gọi. Hai đột biến `wp1404_sh_mat_tham_so_lan_dau` / `_cai_lai` làm (i) đỏ ở đúng hai nhánh (cài được ngay / cần update). Bảng `cai_sh` 67/67. |
| Ghi chú (không phải finding): bảng N2 gọi tắt (c) cho `wp1404_sh_nhanh_tran_dung_sudo` | Đúng, ca thực đỏ ở (c1). | Sửa RESULTS.md §4. |
