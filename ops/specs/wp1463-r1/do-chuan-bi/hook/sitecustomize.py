# wp1463 do-chuan-bi: hook quan sat cho MOI tien trinh Python thua ke PYTHONPATH.
# Moi dong: "<pid>\t<kieu>\t<du lieu>". Kieu:
#   BAT_DAU                     hook da cai trong tien trinh nay (truoc moi import cua ma duoc do)
#   MO / THAT                   duong dan tuyet doi theo chu (lexical) / sau realpath, khi khac nhau
#   DIRFD / DIRFD_KHONG_GIAI    os.open(ten tuong doi, dir_fd=fd): giai theo /proc/self/fd/<fd>, khong theo cwd
#   SINH                        su kien tao tien trinh con (JSON: executable, argv)
import json
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

    def _ghi_duong(kieu, p):
        _ghi(kieu, p)
        try:
            that = os.path.realpath(p)
            if that != p:
                _ghi("THAT", that)
        except Exception:
            pass

    def _argv(x):
        try:
            return [os.fsdecode(a) for a in x] if isinstance(x, (list, tuple)) else [os.fsdecode(x)]
        except Exception:
            return [repr(x)]

    def _hook(ev, args):
        if getattr(_tl, "trong", False):
            return
        _tl.trong = True
        try:
            if ev == "open" and args and isinstance(args[0], (str, bytes)) and not getattr(_tl, "dirfd", False):
                _ghi_duong("MO", os.path.abspath(os.fsdecode(args[0])))
            elif ev == "subprocess.Popen":
                _ghi("SINH", json.dumps({"exe": os.fsdecode(args[0]) if args[0] else None, "argv": _argv(args[1])}))
            elif ev in ("os.posix_spawn", "os.exec"):
                _ghi("SINH", json.dumps({"exe": os.fsdecode(args[0]), "argv": _argv(args[1])}))
            elif ev == "os.system":
                _ghi("SINH", json.dumps({"exe": "/bin/sh", "argv": ["sh", "-c", os.fsdecode(args[0])]}))
        finally:
            _tl.trong = False

    _goc_open = os.open

    def _open(path, flags, mode=0o777, *, dir_fd=None):
        if dir_fd is None or os.path.isabs(os.fsdecode(path)):
            return _goc_open(path, flags, mode, dir_fd=dir_fd)
        try:
            goc = os.readlink(f"/proc/self/fd/{dir_fd}")
            _ghi_duong("DIRFD", os.path.normpath(os.path.join(goc, os.fsdecode(path))))
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
