"""Do: bo test cua UNG VIEN (cac bien the mo hinh Windows `git_loi="tep"` va cac bien the symlink that) chay tren MA SAN PHAM cu (dbe650d) va moi.
Tra loi: mo hinh co tai hien ca do M3 tren ma cu khong, va ma moi co dat khong. Cong cu nhap cua executor, KHONG phai gate.
dung: do_m3.py <goc checkout ung vien> <packet_loop.py cu> """
import sys, tempfile
from pathlib import Path

goc, cu = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
sys.path.insert(0, str(goc / ".claude/dev"))
import packet_loop_test as T  # noqa: E402

for nhan, script in (("ma_cu", cu), ("ma_moi", T.CANONICAL)):
    with tempfile.TemporaryDirectory(prefix="m3_") as td:
        ket = T.chay_suite(script, Path(td) / "luot", chi_chay={"cong_d2b_c4_symlink"})
    v = ket["cong_d2b_c4_symlink"]
    print(nhan, "sha256", __import__("hashlib").sha256(script.read_bytes()).hexdigest()[:16], "::", "DAT" if v is None else f"DO {T._phan_loai_giet(v)} {str(v)[:420]}")
