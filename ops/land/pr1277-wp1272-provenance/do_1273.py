"""Do #1273 tren Windows (chi doc/ghi thu muc tam cua San/harness). Dung: python do_1273.py <goc-checkout @27fd808>"""
import importlib.util, os, platform, subprocess, sys
from pathlib import Path

goc = Path(sys.argv[1]).resolve()
sys.dont_write_bytecode = True
print("HEAD", subprocess.run(["git", "-C", str(goc), "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip())
print("platform", platform.system(), platform.release(), "| python", sys.version.split()[0])
print("os.open in supports_dir_fd:", os.open in os.supports_dir_fd, "| os.unlink in supports_dir_fd:", os.unlink in os.supports_dir_fd)
print("hasattr O_NOFOLLOW:", hasattr(os, "O_NOFOLLOW"), "| hasattr O_DIRECTORY:", hasattr(os, "O_DIRECTORY"))
sys.path.insert(0, str(goc / ".claude" / "dev"))


def nap():
    sp = importlib.util.spec_from_file_location("lt", goc / ".claude" / "dev" / "launcher_test.py")
    lt = importlib.util.module_from_spec(sp); sys.modules["lt"] = lt; sp.loader.exec_module(lt)
    return lt


lt = nap()
m = lt._tai_launcher_thu()
print("launcher._CO_DIR_FD =", m._CO_DIR_FD)
print("dong dich co trong launcher.py:", (goc / ".claude" / "dev" / "launcher.py").read_text("utf-8").count(
    "os.replace(tam, duong.name, src_dir_fd=dfd, dst_dir_fd=dfd)"))

print("== 1: ca dich tren ban goc")
try:
    kq = lt.r1252_ghi_bang_chung_an_toan()
    print("ca r1252_ghi_bang_chung_an_toan:", "QUA" if kq is None else kq)
except BaseException as e:  # noqa: BLE001
    print("ca r1252_ghi_bang_chung_an_toan: HONG", type(e).__name__, str(e)[:200])

print("== 2: dot bien nhu tren master (khong nhan)")
muc = [x for x in lt.DOT_BIEN if x[0] == "r1252_ghi_de_dich_truc_tiep"]
print("so muc:", len(muc), "| so phan tu:", len(muc[0]) if muc else None)
lt.DOT_BIEN[:] = muc
print("ket qua:", lt.chay_dot_bien())

print("== 3: dot bien + nhan posix (ban va de xuat)")
lt = nap()
muc = [x for x in lt.DOT_BIEN if x[0] == "r1252_ghi_de_dich_truc_tiep"]
lt.DOT_BIEN[:] = [tuple(muc[0][:3]) + (("posix", "nhanh dir_fd cua _ghi_tep_0600 khong chay tren Windows (_CO_DIR_FD False)"),)]
print("ket qua:", lt.chay_dot_bien())
