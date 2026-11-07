"""Cài đặt THAM CHIẾU của K7-S (`ops/specs/wp1236-r8.md`), dùng cho phép đo của phiên soạn r8. Không phải mã của module."""
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


cp = cu_phap_run
