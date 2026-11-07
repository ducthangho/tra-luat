import re

P = r"[A-Za-z0-9_.][A-Za-z0-9_./-]*"
W = r"[A-Za-z0-9_./=:-]+"
DANG = rf"(?:python {P}\.py|bash {P}\.sh|pwsh -NoProfile -File {P}\.ps1)"
LENH = rf"{DANG}(?: {W})*"
RE_DON = re.compile(LENH, re.ASCII)
RE_ONG = re.compile(rf"{LENH}(?: \| {LENH})+", re.ASCII)

def cu_phap_run(run, shell):
    if type(run) is not str:
        return "lenh_ngoai_cu_phap"
    if shell not in (None, "bash", "sh"):
        return "shell_ngoai_cu_phap"
    b = run[:-1] if run.endswith("\n") else run
    if RE_DON.fullmatch(b):
        return None
    if RE_ONG.fullmatch(b):
        return None if shell == "bash" else "ong_khong_bash_tuong_minh"
    return "lenh_ngoai_cu_phap"

import functools
_original = cu_phap_run
_calls = 0

def counted(run, shell):
    global _calls
    _calls += 1
    return _original(run, shell)

cu_phap_run = functools.update_wrapper(counted, _original)
