# Do LAI doc lap ba phat hien cua luot 4. Ca doi chung chay TRUOC: rig phai tra loi
# dung mot ca ta BIET TRUOC dap an, truoc khi tin bat ky ca nao khac.
import importlib.util, os, sys, tempfile
from pathlib import Path
spec = importlib.util.spec_from_file_location("lp", sys.argv[1])
lp = importlib.util.module_from_spec(spec); spec.loader.exec_module(lp)

def moi(t):
    d = Path(t)/"ngoai"; d.mkdir()
    cw = Path(t)/"cwd";  cw.mkdir()
    return d, cw

print("=== CA DOI CHUNG (biet truoc dap an) ===")
with tempfile.TemporaryDirectory() as t:
    d, cw = moi(t); (d/"git.exe").write_text("x")
    r = lp._git_windows(path=str(d), program_files=str(Path(t)/"pf"), cwd=str(cw))
    print(f"  git.exe ngoai cwd  -> {'NHAN' if r else 'None':5}  {'OK' if r else 'RIG HONG'}")
with tempfile.TemporaryDirectory() as t:
    d, cw = moi(t); (cw/"git.exe").write_text("x")
    r = lp._git_windows(path=str(cw), program_files=str(Path(t)/"pf"), cwd=str(cw))
    print(f"  git.exe TRONG cwd  -> {'NHAN' if r else 'None':5}  {'RIG HONG' if r else 'OK'}")

print()
print("=== P1: buoc 1 CONG_CU_GIT — co kiem duoi tep khong? ===")
for ten in ("git.exe","git.bat","git.cmd","git.py","khong-phai-git-chut-nao.txt"):
    with tempfile.TemporaryDirectory() as t:
        d, cw = moi(t); f = d/ten; f.write_text("x")
        r = lp._git_windows(cong_cu_git=str(f), path="", program_files=str(Path(t)/"pf"), cwd=str(cw))
        print(f"  CONG_CU_GIT={ten:32} -> {'NHAN' if r else 'TU CHOI'}")

print()
print("=== P2: muc PATH co dau nhay kep ===")
for boc in (False, True):
    with tempfile.TemporaryDirectory() as t:
        d, cw = moi(t); (d/"git.exe").write_text("x")
        muc = f'"{d}"' if boc else str(d)
        r = lp._git_windows(path=muc, program_files=str(Path(t)/"pf"), cwd=str(cw))
        print(f"  PATH={'co nhay kep' if boc else 'khong nhay':12} -> {'NHAN' if r else 'None (TU CHOI)'}")

print()
print("=== P3-1: mot dau ';' trong TEN thu muc (tren posix) ===")
with tempfile.TemporaryDirectory() as t:
    la = Path(t)/"co;dau-cham-phay"; la.mkdir()
    d, cw = moi(t); (d/"git.exe").write_text("x")
    muc = str(la) + os.pathsep + str(d)
    r = lp._git_windows(path=muc, program_files=str(Path(t)/"pf"), cwd=str(cw))
    print(f"  os.pathsep={os.pathsep!r}, mot muc chua ';' -> {r if r else 'None (MAT muc git.exe hop le)'}")
