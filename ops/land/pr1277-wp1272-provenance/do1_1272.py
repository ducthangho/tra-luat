"""Do tap trung DUNG 1 dot bien (HOTFIX-R1252-POSIX). Dung: python do1_1272.py <goc-checkout> [--nhan-posix] [--gia-windows]"""
import contextlib, importlib.util, io, re, sys
from pathlib import Path
goc = Path(sys.argv[1]).resolve(); co = set(sys.argv[2:])
sys.dont_write_bytecode = True
sys.path.insert(0, str(goc / ".claude" / "dev"))
sp = importlib.util.spec_from_file_location("lt", goc / ".claude" / "dev" / "launcher_test.py")
lt = importlib.util.module_from_spec(sp); sys.modules["lt"] = lt; sp.loader.exec_module(lt)
muc = [x for x in lt.DOT_BIEN if x[0] == "r1252_ghi_de_dich_truc_tiep"]
assert len(muc) == 1, len(muc)
m = tuple(muc[0][:3])
if "--nhan-posix" in co:
    m = m + (("posix", "nhanh dir_fd cua _ghi_tep_0600 khong chay tren Windows (_CO_DIR_FD False)"),)
elif len(muc[0]) > 3:
    m = muc[0]
lt.DOT_BIEN[:] = [m]
lt.DOT_BIEN_HOOK[:] = []
lt.DOT_BIEN_HARNESS[:] = []
if "--gia-windows" in co:
    lt.LA_WINDOWS = True
print("so muc DOT_BIEN/HOOK/HARNESS:", len(lt.DOT_BIEN), len(lt.DOT_BIEN_HOOK), len(lt.DOT_BIEN_HARNESS), "| phan tu:", len(m))
buf = io.StringIO()
with contextlib.redirect_stdout(buf):
    kq = lt.chay_dot_bien()
out = buf.getvalue()
dong = [x for x in out.splitlines() if re.match(r"^  \S+\s+(OK|SAI|KHONG DO DUOC)", x)]
print("so dong ket qua dot bien:", len(dong))
for x in dong:
    print(x)
print("tra ve:", kq)
