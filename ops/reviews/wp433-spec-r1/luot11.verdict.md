**Review đặc tả lượt 11, packet 1, Issue #433.** Hai finding lượt 10 đã đóng. Packet 1 còn hai finding P2 mới.

| Finding lượt 10 | Trạng thái | Bằng chứng |
|---|---|---|
| P2 — W1/W3 bỏ gộp kiểm jar và kiểm đích, thiếu đột biến riêng theo caller | **Đóng** | Mô phỏng RAM với `khac.json`, đúng tiền điều kiện M1. Đối chứng thu tập nhãn rỗng. Mỗi lần chỉ bỏ kiểm jar ở một caller, giữ kiểm đích và writer giả, thu đúng một cặp `(N1k-W1, khong_khoa_la)`, `(N1k-W2, khong_khoa_la)` hoặc `(N1k-W3, khong_khoa_la)`. |
| P3 — M4 còn hứa về lỗi dữ liệu W6 đã chuyển và dẫn M3(0b) | **Đóng** | M4 giới hạn cam kết theo phạm vi xử lý của packet 1. §2 và M3(3) giao phần kiểm dữ liệu W6 cho packet 2. M3(0b) chỉ còn trong lịch sử chuyển khối. |

### Finding mới

- **P2 · Packet 1 — §4b dòng 4 vẫn đổi hai cơ chế tại W2.** `db_w2_bo_chot` đưa vòng ghi W2 về base. Theo §0.1 và M2, thao tác đó vừa bỏ `_kiem_dich_ghi`, vừa thay writer nguyên tử bằng `makedirs` + `open("w")` + `chmod`. Chốt jar M3(1) còn nguyên, nhưng điều đó chưa đủ để kết luận “chỉ mất kiểm đích”. Giữ nguyên writer và xử lý lỗi, chỉ bỏ lời gọi kiểm đích. Fixture symlink hiện tại vẫn có thể làm đỏ `khong_ra_ngoai`. [Đặc tả, §4b dòng 4](/tmp/claude-0/-home-user-tra-luat/1adbda56-058d-5ab2-9b04-c994e35e8ec6/scratchpad/wtP1/ops/specs/NLM-GWS-DICH-NGOAI-KHO-r1.md:303)
- **P2 · Packet 1 — N1 đòi stderr tại biên W3 vốn trả tuple.** Cả `w3_load_rel_thoat` và `N1k-W3` đòi `ok is False` cùng một dòng `ngoài danh sách cho phép`. M4 giao `_nlm_auth_load` trả `(False, lý do)` và giao việc in cho caller. Gọi trực tiếp W3 theo M4 cho stderr rỗng. Nếu thêm in trong W3, `cmd_nlm_auth_load` giữ nhánh base sẽ in lần thứ hai. N1 cần kiểm cụm trong lý do trả về ở lượt W3 và đo stderr ở biên CLI nếu cần. [N1](/tmp/claude-0/-home-user-tra-luat/1adbda56-058d-5ab2-9b04-c994e35e8ec6/scratchpad/wtP1/ops/specs/NLM-GWS-DICH-NGOAI-KHO-r1.md:264) · [Caller CLI trên base](/tmp/claude-0/-home-user-tra-luat/1adbda56-058d-5ab2-9b04-c994e35e8ec6/scratchpad/wtP1/scripts/tl_gws.py:2050)
- **P3 · Packet 1 — Hai con trỏ hiện hành `M7/N9` trỏ nhầm tiêu chí của packet 2.** §2 và §7 cần dẫn `M7/N9w6`. `N9` của packet 2 là gate selftest và bundled. [Packet 1, §2](/tmp/claude-0/-home-user-tra-luat/1adbda56-058d-5ab2-9b04-c994e35e8ec6/scratchpad/wtP1/ops/specs/NLM-GWS-DICH-NGOAI-KHO-r1.md:223) · [Packet 2, N9w6 và N9](/tmp/claude-0/-home-user-tra-luat/1adbda56-058d-5ab2-9b04-c994e35e8ec6/scratchpad/wtP1/ops/specs/GWS-CRED-DICH-NGOAI-KHO-r1.md:115)

P0/P1 mới: không có. Packet 2 giữ trạng thái hoãn và các finding lượt 10 đã ghi ở cuối đặc tả của nó. Rà ranh giới không phát sinh finding mới riêng cho packet 2.

### §4b, trần và L1–L7

- Đã rà đủ 30 dòng §4b, gồm 26 H và 4 E. Bốn dòng E là 10 (`N3.1-W1/W2`), 11 (`N3.3`), 22 (sáu lượt `N8.1-*`) và 24 (`N8.4-W1`). Phép đo nguyên tố xác nhận bốn cặp loại/dấu và đối chứng sai lượt. Các dòng H được rà theo fixture và hợp đồng M1–M4. Hai điểm cần sửa nằm ở các finding P2 trên.
- L1/L2: số đếm có đơn vị và M1–M7 chiếu vào ba đường trong write set. L3/L6: hai P2 ảnh hưởng tính cô lập của đột biến và tính đúng của phép đo lỗi. L4: §7 giữ bộ đếm qua lần tách và khai rõ biên nhận tiền nhiệm chưa đo được. L5: 369–420 là ước lượng có mốc, biên trên còn 30 dòng. Mô phỏng N13 với đúng ba đường cho 450 xanh, 451 đỏ. `numstat` triển khai chờ exact head có mã.
- L7: lượt 11/12 theo quyết định riêng cho packet 1. Khi chạm trần thì áp Review Rescue Checkpoint. Điều kiện duyệt băm, comment cấp ngoại lệ bundled và các điều kiện dừng trước lease vẫn áp dụng.

**Neo và môi trường.** `HEAD`, `master` cục bộ và `origin/master` cục bộ cùng OID `641108cb997872b0ef2a277ea9c8faf8b82532bb`. Tree `e6c7c50863421e32cac4f5f1894f176d758375b1`. Đặc tả là tệp untracked, neo bằng SHA-256 `1818a8598763c5a54e73f26a81c0cfbfefb63071ed2421d3984725479def2bc7`. Phiên reviewer độc lập họ OpenAI trên Codex, runtime Linux chỉ đọc, Python 3.13.18. Hai lệnh `python3 -I -B -` chạy mô phỏng RAM và kiểm chữ ký ngoại lệ đều rc 0. Dùng dữ liệu giả, không mạng. Gate triển khai `not_run` vì packet chưa có mã.

KET_LUAN: request_changes
tokens used
83,514
**Review đặc tả lượt 11, packet 1, Issue #433.** Hai finding lượt 10 đã đóng. Packet 1 còn hai finding P2 mới.

| Finding lượt 10 | Trạng thái | Bằng chứng |
|---|---|---|
| P2 — W1/W3 bỏ gộp kiểm jar và kiểm đích, thiếu đột biến riêng theo caller | **Đóng** | Mô phỏng RAM với `khac.json`, đúng tiền điều kiện M1. Đối chứng thu tập nhãn rỗng. Mỗi lần chỉ bỏ kiểm jar ở một caller, giữ kiểm đích và writer giả, thu đúng một cặp `(N1k-W1, khong_khoa_la)`, `(N1k-W2, khong_khoa_la)` hoặc `(N1k-W3, khong_khoa_la)`. |
| P3 — M4 còn hứa về lỗi dữ liệu W6 đã chuyển và dẫn M3(0b) | **Đóng** | M4 giới hạn cam kết theo phạm vi xử lý của packet 1. §2 và M3(3) giao phần kiểm dữ liệu W6 cho packet 2. M3(0b) chỉ còn trong lịch sử chuyển khối. |

### Finding mới

- **P2 · Packet 1 — §4b dòng 4 vẫn đổi hai cơ chế tại W2.** `db_w2_bo_chot` đưa vòng ghi W2 về base. Theo §0.1 và M2, thao tác đó vừa bỏ `_kiem_dich_ghi`, vừa thay writer nguyên tử bằng `makedirs` + `open("w")` + `chmod`. Chốt jar M3(1) còn nguyên, nhưng điều đó chưa đủ để kết luận “chỉ mất kiểm đích”. Giữ nguyên writer và xử lý lỗi, chỉ bỏ lời gọi kiểm đích. Fixture symlink hiện tại vẫn có thể làm đỏ `khong_ra_ngoai`. [Đặc tả, §4b dòng 4](/tmp/claude-0/-home-user-tra-luat/1adbda56-058d-5ab2-9b04-c994e35e8ec6/scratchpad/wtP1/ops/specs/NLM-GWS-DICH-NGOAI-KHO-r1.md:303)
- **P2 · Packet 1 — N1 đòi stderr tại biên W3 vốn trả tuple.** Cả `w3_load_rel_thoat` và `N1k-W3` đòi `ok is False` cùng một dòng `ngoài danh sách cho phép`. M4 giao `_nlm_auth_load` trả `(False, lý do)` và giao việc in cho caller. Gọi trực tiếp W3 theo M4 cho stderr rỗng. Nếu thêm in trong W3, `cmd_nlm_auth_load` giữ nhánh base sẽ in lần thứ hai. N1 cần kiểm cụm trong lý do trả về ở lượt W3 và đo stderr ở biên CLI nếu cần. [N1](/tmp/claude-0/-home-user-tra-luat/1adbda56-058d-5ab2-9b04-c994e35e8ec6/scratchpad/wtP1/ops/specs/NLM-GWS-DICH-NGOAI-KHO-r1.md:264) · [Caller CLI trên base](/tmp/claude-0/-home-user-tra-luat/1adbda56-058d-5ab2-9b04-c994e35e8ec6/scratchpad/wtP1/scripts/tl_gws.py:2050)
- **P3 · Packet 1 — Hai con trỏ hiện hành `M7/N9` trỏ nhầm tiêu chí của packet 2.** §2 và §7 cần dẫn `M7/N9w6`. `N9` của packet 2 là gate selftest và bundled. [Packet 1, §2](/tmp/claude-0/-home-user-tra-luat/1adbda56-058d-5ab2-9b04-c994e35e8ec6/scratchpad/wtP1/ops/specs/NLM-GWS-DICH-NGOAI-KHO-r1.md:223) · [Packet 2, N9w6 và N9](/tmp/claude-0/-home-user-tra-luat/1adbda56-058d-5ab2-9b04-c994e35e8ec6/scratchpad/wtP1/ops/specs/GWS-CRED-DICH-NGOAI-KHO-r1.md:115)

P0/P1 mới: không có. Packet 2 giữ trạng thái hoãn và các finding lượt 10 đã ghi ở cuối đặc tả của nó. Rà ranh giới không phát sinh finding mới riêng cho packet 2.

### §4b, trần và L1–L7

- Đã rà đủ 30 dòng §4b, gồm 26 H và 4 E. Bốn dòng E là 10 (`N3.1-W1/W2`), 11 (`N3.3`), 22 (sáu lượt `N8.1-*`) và 24 (`N8.4-W1`). Phép đo nguyên tố xác nhận bốn cặp loại/dấu và đối chứng sai lượt. Các dòng H được rà theo fixture và hợp đồng M1–M4. Hai điểm cần sửa nằm ở các finding P2 trên.
- L1/L2: số đếm có đơn vị và M1–M7 chiếu vào ba đường trong write set. L3/L6: hai P2 ảnh hưởng tính cô lập của đột biến và tính đúng của phép đo lỗi. L4: §7 giữ bộ đếm qua lần tách và khai rõ biên nhận tiền nhiệm chưa đo được. L5: 369–420 là ước lượng có mốc, biên trên còn 30 dòng. Mô phỏng N13 với đúng ba đường cho 450 xanh, 451 đỏ. `numstat` triển khai chờ exact head có mã.
- L7: lượt 11/12 theo quyết định riêng cho packet 1. Khi chạm trần thì áp Review Rescue Checkpoint. Điều kiện duyệt băm, comment cấp ngoại lệ bundled và các điều kiện dừng trước lease vẫn áp dụng.

**Neo và môi trường.** `HEAD`, `master` cục bộ và `origin/master` cục bộ cùng OID `641108cb997872b0ef2a277ea9c8faf8b82532bb`. Tree `e6c7c50863421e32cac4f5f1894f176d758375b1`. Đặc tả là tệp untracked, neo bằng SHA-256 `1818a8598763c5a54e73f26a81c0cfbfefb63071ed2421d3984725479def2bc7`. Phiên reviewer độc lập họ OpenAI trên Codex, runtime Linux chỉ đọc, Python 3.13.18. Hai lệnh `python3 -I -B -` chạy mô phỏng RAM và kiểm chữ ký ngoại lệ đều rc 0. Dùng dữ liệu giả, không mạng. Gate triển khai `not_run` vì packet chưa có mã.

KET_LUAN: request_changes
rc=0 xong 2026-11-18T08:16:07Z
