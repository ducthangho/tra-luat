# wp1463 do-chuan-bi: hook quan sat `open` cho MOI tien trinh Python thua ke PYTHONPATH.
# Ghi moi dong "<pid>\t<kieu>\t<duong dan tuyet doi>"; kieu: BAT_DAU | MO | DIRFD | DIRFD_KHONG_GIAI.
# os.open(..., dir_fd=fd) voi duong dan tuong doi: giai theo /proc/self/fd/<fd> (khong theo cwd);
# su kien audit cung luot ay bi bo qua de khong ghi nham duong dan giai theo cwd.
import os
import sys
import threading

_LOG = os.environ.get("AUDIT_OPEN_LOG")
if _LOG:
    _fd = os.open(_LOG, os.O_WRONLY | os.O_APPEND | os.O_CREAT, 0o600)
    _tl = threading.local()

    def _ghi(kieu, p):
        try:
            os.write(_fd, f"{os.getpid()}\t{kieu}\t{p}\n".encode("utf-8", "surrogateescape"))
        except Exception:
            pass

    def _hook(ev, args):
        if ev == "open" and args and isinstance(args[0], (str, bytes)) and not getattr(_tl, "dirfd", False):
            _ghi("MO", os.path.abspath(os.fsdecode(args[0])))

    _goc_open = os.open

    def _open(path, flags, mode=0o777, *, dir_fd=None):
        if dir_fd is None or os.path.isabs(os.fsdecode(path)):
            return _goc_open(path, flags, mode, dir_fd=dir_fd)
        try:
            goc = os.readlink(f"/proc/self/fd/{dir_fd}")
            _ghi("DIRFD", os.path.normpath(os.path.join(goc, os.fsdecode(path))))
        except Exception:
            _ghi("DIRFD_KHONG_GIAI", os.fsdecode(path))
        _tl.dirfd = True
        try:
            return _goc_open(path, flags, mode, dir_fd=dir_fd)
        finally:
            _tl.dirfd = False

    os.open = _open
    try:
        os.supports_dir_fd.add(_open)  # shutil.rmtree chon nhanh an toan theo tap nay
    except Exception:
        pass
    sys.addaudithook(_hook)
    _ghi("BAT_DAU", "-")
