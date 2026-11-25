# Handoff wp1236 đợt C — lượt 3, ứng viên `dbe650d` (revision 12, generation 1)

Nguồn có thẩm quyền của thư mục này là `handoff.yaml`; tệp này chỉ giải thích những chỗ một bảng YAML không nói hết.
Trả lời review mã lượt 2 (`ops/reviews/wp1236-c-r12-ma-2-codex/` trên `ops/wp1236-bc-lease` @ `ed9d958`, `changes_requested`: C01 `VA_MOT_PHAN`
còn P1; C02 `DA_VA_THAT`). Ứng viên CHƯA push, CHƯA có PR (ADR-0060 M5/M12): lấy bằng bundle. Executor không tự review và không tự gán nhãn đóng lớp.

```bash
git fetch ops/handoff/wp1236-c-r12-g1/dbe650d/wp1236-c-dbe650d.bundle claude/wp1236-c-r12-g1:claude/wp1236-c-r12-g1   # cần base f602325
git rev-parse claude/wp1236-c-r12-g1            # dbe650d2a3c3fb6da9573ea485adc65934efdc78
git rev-parse 'claude/wp1236-c-r12-g1^{tree}'   # b0a8b1bd4360ac33e5e0b076d820393e65d6f5bb
git diff 2439922 dbe650d --stat                 # phần đổi của lượt 3: packet_loop.py +12 −8 · packet_loop_test.py +41 −12
```

## 1. Vì sao lượt 2 hở, và vì sao bản vá lượt 3 là LIỆT KÊ chứ không phải tra

Lượt 2 đã đặt đúng bất biến (bản bung phải là cây của `oid`) nhưng đo nó trên tập sai: `git ls-tree -r` trần chỉ liệt kê tệp lá, và mỗi lá được kiểm
bằng cách TRA tên của nó trên đĩa. Hai lỗi chồng nhau:

- tập mục thiếu thư mục, nên hai thư mục `A` và `a` có lá khác khoá đi lọt phép kiểm trùng khoá (reviewer lượt 2);
- phép TRA theo tên đi qua đúng phép gộp tên của nền. Trên nền gộp `A` với `a`, tra `A/note.txt` và `a/readback-….json` đều thấy, đều đúng băm, nên
  không gì lệch. Cùng một lẽ ấy áp cho mọi phép đổi tên mà khoá NFC + casefold không đoán trước (dấu chấm hoặc khoảng trắng cuối, tên dành riêng
  của Windows, luồng phụ NTFS).

Lượt 3 tách ba luật (thông điệp rc 8 riêng cho từng luật):

| luật | đo trên | bắt được |
|---|---|---|
| tên trùng khoá | danh mục git `ls-tree -r -t`, TRƯỚC khi bung | hai tệp, hai thư mục, thư mục và tệp trùng khoá — phán quyết như nhau trên mọi nền |
| danh mục | {đường dẫn: loại} LIỆT KÊ từ đĩa bằng `os.walk`, so hai chiều với danh mục git | tệp bị ẩn (`export-ignore`), symlink thành tệp (nền không tạo được symlink), mọi phép thêm/bớt/gộp/đổi tên của nền |
| nội dung | băm blob của tệp, và của ĐÍCH symlink (`os.readlink`) | byte đổi (`eol`, `autocrlf`), đích symlink bị bộ lọc `data` viết lại |

Liệt kê đĩa thì thấy được tên mà nền đã THỰC SỰ ghi, nên không cần biết trước nền đổi tên theo luật nào. Đó là lý do bản vá không thêm luật riêng
cho dấu chấm cuối hay tên dành riêng, và không đổi miền ký tự E3 của chủ kho.

Phép đổi tên của NTFS chỉ được MÔ PHỎNG trên Linux: `_D2B_NEN` trong bộ test biến đổi đĩa ngay sau khi bung (gộp hai thư mục, thêm một mục, bớt một
mục, viết lại đích symlink), qua móc `git_loi` sẵn có của `_rev_list_loi`. Hành vi thật của Windows là việc của điều phối (M3).

## 2. Tự kiểm các chốt có răng riêng

Ca thật dừng ở biến thể lệch ĐẦU TIÊN, nên "đột biến bị giết" chưa nói biến thể nào bắt nó. `gate/ma_tran_c4.log` chạy riêng từng biến thể của
`cong_d2b_c4_symlink` dưới từng đột biến khai báo của ca ấy: mỗi luật bị đúng các biến thể thiết kế cho nó bắt, và hai đối chứng anh em cùng tiền tố
(`anh_em_khong_readback`, `anh_em_co_readback`) không đổi dưới bất kỳ đột biến nào ngoài các đột biến làm hỏng cả danh mục.

## 3. Dữ liệu thật

`gate/kho_that.log`: chạy CHÍNH `_d2b_kiem` của ứng viên lượt 2 và lượt 3 trên mọi tệp `danh-gia-gate-output-*.txt` của `ops/land` tại `origin/master`
(biên bản dựng từ header của từng tệp nên ba neo luôn khớp; phần còn lại là đường dẫn, mode, bản bung và `kiem_tep`). Hai bảng kết quả từng tệp so
bằng `cmp`. Kèm số nhóm trùng khoá trên toàn bộ mục (cả thư mục) của `ops/land`.

## 4. Không hồi quy và luật 9

Như lượt 2, trên rig mới (`ab/`): hai clone dựng trong một lệnh (`ab/cong_cu/ab_dung.sh`), base `f602325` và ứng viên `dbe650d`, mỗi vế đủ 16 mảnh
nền, job gom và 16 mảnh đột biến. Bảng số từng mảnh và kết luận (i)(ii) ở `ab/bang_so.md`. Luật 9 trên khối D2b như hai lượt trước (`luat9/`).

## 5. Tệp trong thư mục

`handoff.yaml` · `wp1236-c-dbe650d.bundle` · `ab/` · `gate/` (`gate2.tong`, `dot_bien_khai_bao.log`, đuôi selftest và `ci_dang_ky_test`,
`ruff_nen.log`, `ma_tran_c4.log`, `kho_that.log` + hai bảng `.tsv`, `probe_l2.log`, `mc11.log`, `dich_symlink.log`, `bundle_verify.log`) · `luat9/`
· `cong_cu/` (script nháp của executor đã dùng để đo; không phải cổng).
