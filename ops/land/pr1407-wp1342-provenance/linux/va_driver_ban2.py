"""Vá driver đột biến bản 1 (comment 6995876153, sha256 e01af575…) thành bản 2 theo đặc tả bản 13. va_driver_ban2.py <dot_bien_r4.py bản 1> <tệp ra>"""
import hashlib
import sys
from pathlib import Path

s = Path(sys.argv[1]).read_text(encoding="utf-8")
assert hashlib.sha256(s.encode()).hexdigest() == "e01af5752a4b841fd18039866cd19e866a81d7b489aeb109698e9f6c7ad38c16", "đầu vào không phải bản 1"
CAP = [
    ('"J6 (ii): marker đã có lúc between", J + "thuan"),', '"J6 (ii): marker đã có lúc between", (J + "query_loi", P + "hang_luong")),'),
    ('"J0 THREADENTRY32 offset th32OwnerProcessID == 12", J + "thuan"),',
     '"J0 THREADENTRY32 offset th32OwnerProcessID == 12", (J + "query_loi", P + "hang_luong")),'),
    ('"J8: bản sao con chưa signaled khi hàm trả"', '"J8: bản sao con chưa signaled trong 5 s"'),
    ('"J9: tiến trình phụ còn sống VÀ j9 không có ghi chú cleanup:xac_nhan"',
     '"J9: tiến trình phụ chưa signaled trong 5 s VÀ j9 không có ghi chú cleanup:xac_nhan"'),
    ('# id: (nền, [(tìm, thay)...], ca đích, nhãn phải có trong thông điệp AssertionError, ca đối chứng)',
     '# id: (nền, [(tìm, thay)...], ca đích, nhãn phải có trong thông điệp AssertionError, ca đối chứng HOẶC bộ ca đối chứng)\n'
     '# b và abi làm hỏng CHÍNH đường spawn mà J1 đi qua (đo native 19-11) ⇒ đối chứng của chúng là J11 + S1 (đặc tả bản 13 §4b).'),
    ('''            sach, do, dc = chay_ca(dev, dev / "packet_loop.py", dich), chay_ca(dev, ban, dich), chay_ca(dev, ban, doi_chung)
            giet = sach[0] == "DAT" and do[0] == "DO" and nhan in do[1] and dc[0] == "DAT"''',
     '''            doi_chung = (doi_chung,) if isinstance(doi_chung, str) else doi_chung
            sach, do, dc = chay_ca(dev, dev / "packet_loop.py", dich), chay_ca(dev, ban, dich), [chay_ca(dev, ban, t)[0] for t in doi_chung]
            giet = sach[0] == "DAT" and do[0] == "DO" and nhan in do[1] and dc == ["DAT"] * len(dc)'''),
    ("đối chứng={doi_chung} [{dc[0]}]", "đối chứng={'+'.join(doi_chung)} {dc}"),
]
for tim, thay in CAP:
    assert s.count(tim) == 1, tim
    s = s.replace(tim, thay)
bam = hashlib.sha256(s.encode()).hexdigest()
assert bam == "9e32013a92c6c89c0a21c00858bcb6b9e1af40ba18d2fc35e6745dff9c380afa", bam
Path(sys.argv[2]).write_text(s, encoding="utf-8", newline="\n")
print("bản 2 sha256", bam, len(s.encode()), "byte")
