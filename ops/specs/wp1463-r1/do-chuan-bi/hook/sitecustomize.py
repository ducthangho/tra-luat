import sys, os
_LOG = os.environ.get("AUDIT_OPEN_LOG")
if _LOG:
    _fd = os.open(_LOG, os.O_WRONLY | os.O_APPEND | os.O_CREAT, 0o600)
    def _h(ev, args):
        if ev == "open" and args and isinstance(args[0], (str, bytes)):
            try:
                os.write(_fd, (os.path.abspath(os.fsdecode(args[0])) + "\n").encode("utf-8", "replace"))
            except Exception:
                pass
    sys.addaudithook(_h)
