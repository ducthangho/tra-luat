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
