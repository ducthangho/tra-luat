# Reviewer Claude — vòng 6 r8 (SPEC sha256 7c85e68e…) — ghi chú đo

Mọi script chạy bằng `python3 -I`, từ `work/v6/` (hoặc từ `repo/` với đường `../work/v6/…` cho script cần `git show`). Không sửa gì trong `repo/`
(HEAD `95565cb`, `git status` rỗng trước và sau).

| script | đo gì | kết quả |
|---|---|---|
| `khoa_ast_r8.py` (bản sao) | tham chiếu của phiên soạn, main_v5 | rc 0; JSON trùng byte bản trong kho |
| `thu_s0_v6.py` | W1 `functools.wraps` (def thứ hai), W2 `__wrapped__` gán tay, W3 `__code__` thay bằng code bọc có `co_firstlineno` của def gốc, W4 mục `linecache` mtime None | cả bốn ĐẠT `kiem_s0_v5` (rỗng), đổi `cu_phap_run("python ops/a.py \|\| exit 0", None)` thành None |
| `thu_de_xuat_v6.py` | đề xuất: `vars(f) == {}`; đọc thẳng `module.__file__`, `compile`, code object con tại `co_firstlineno` phải `== f.__code__`; `ast` của def tại dòng ấy | 22/22 đúng kỳ vọng (hợp lệ ĐẠT, mọi biến thể v4/v5/v6 + W5 `co_consts` ĐỎ) |
| `thu_chan_oan_v6.py` | đề xuất có chặn oan code nóng/đang bị đo không | rỗng sau 200 000 lời gọi, dưới `sys.settrace`, dưới `sys.monitoring` |
| `thu_goi_v6.py` | biến đổi `run` Ở CHỖ GỌI vs gián điệp (30 thân F-ok/F-ok-goc + 10 lượt đặc biệt) và A14-S3b (119 + 206) | `removesuffix(" \|\| :")`, `(" \|\| exit 0")`, `(" \|\| true")`: 0 thay đổi ở gián điệp, 0/325 lệch A14-S3b, 0/61 530 lệch kho S6 |
| `thu_goi_de_xuat_v6.py` | thêm 10 thân một dòng KHÔNG LF (× 2 shell) vào gián điệp; A14-S3b thêm bản bỏ LF của 116 vế | 12/12 biến đổi bị gián điệp mở rộng bắt (trừ NFC, đã bị năm thân cũ bắt) |
| `thu_bash_v6.py` | Bash/dash thật, `python ops/hong.py \|\| :` / `\|\| true` / `\|\| exit 0` không LF | rc 0, DA_CHAY dưới cả ba dòng lệnh GitHub |
| `thu_s0_v5cu_qua_v5.json` | các biến thể vòng 5 của tôi qua `kiem_s0_v5` | 6/6 nhóm A ĐỎ; B hợp lệ ĐẠT; chú thích kiểu tham số ĐỎ (đúng luật) |
| `probes_r8.py`, `dot_bien_r8.py`, `g1_qua_grammar.py`, `sinh_r8.py` | chạy lại | 112/112, 53/53, 52/52, 61 530 / 2 647 / 0 / 0 / 0 (2 phút 6 giây); bốn JSON trùng byte |
| `fuzz_ebnf.py` (hạt 20261108) | grammar sạch, sinh từ EBNF | 300 thân, 902 lượt, 0 không nhận, 0 xấu |

Đếm: 25/30 thân bước luật ở `ci.yml@fe84620` là một dòng KHÔNG LF; 110/112 vế âm có LF cuối (2 còn lại không phải chuỗi).
