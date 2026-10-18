# Chay launcher_test.py voi os.getpid bi ep ve argv[1] ("that" = khong ep).
import os, sys, runpy
p = sys.argv[1]
if p != "that":
    os.getpid = lambda: int(p)
sys.argv = ["launcher_test.py"] + sys.argv[2:]
runpy.run_path(".claude/dev/launcher_test.py", run_name="__main__")
