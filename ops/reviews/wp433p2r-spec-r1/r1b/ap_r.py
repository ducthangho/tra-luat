# ap_r.py <r1.md> <moi.md> - ap 3 phep thay (moi neo khop DUNG 1 lan) + 1 muc nhat ky cuoi tep len ban dong bang 4d4b3181; in sha256 ban moi.
import hashlib, sys
s = open(sys.argv[1], encoding="utf-8", newline="").read()
assert hashlib.sha256(s.encode("utf-8")).hexdigest().startswith("4d4b31812788"), "sai ban goc"
CAP = [
 ("`W5.khong_bit` (`a = 16`, FILE_ATTRIBUTE_DIRECTORY) ⇒", "`W5.khong_bit` (`a = 528`: FILE_ATTRIBUTE_DIRECTORY 16 hợp bit FILE_ATTRIBUTE_SPARSE_FILE 512) ⇒"),
 ('(vế thuộc tính thành `getattr(st, "st_file_attributes", 0) != 0`)', "(mặt nạ của vế thuộc tính thành hợp bit của `stat.FILE_ATTRIBUTE_REPARSE_POINT` và `stat.FILE_ATTRIBUTE_SPARSE_FILE`)"),
 ("lập luận (16 ≠ 0) |", "lập luận (`528 & 1536` ≠ 0; entry thật của Windows không mang bit 512); phép thay cũ `!= 0` chết sai lượt trên nt (§10) |"),
]
for a, b in CAP:
    assert s.count(a) == 1, a
    s = s.replace(a, b)
assert s.endswith("Bản lượt 5." + chr(10))
s += """- 2026-11-19T21:30Z (executor wp433-r5-g1-claude, sau thi công trên `20eac11`, chưa push): phép thay cũ của đột biến 2 (`!= 0`) chết SAI LƯỢT
  trên nt: `os.lstat` của Windows đặt `st_file_attributes` khác 0 cho mọi entry thật, nên ở `W5.bit` vòng tiền tố chặn tại gốc ổ. Đo: probe
  `probe_db2.py` (sha256 `93d92dbb…`) trên Desktop (Windows 11, Python 3.12.10): attr gốc ổ 22, attr T 16, candidate chặn tại `cfg`, phép
  thay cũ chặn tại gốc ổ. Sửa: §4b dòng 2 (mặt nạ mở rộng sang bit 512), N1 `W5.khong_bit` giả lập `a = 528`. M1 không đổi.
"""
open(sys.argv[2], "w", encoding="utf-8", newline="").write(s)
print(hashlib.sha256(s.encode("utf-8")).hexdigest())
