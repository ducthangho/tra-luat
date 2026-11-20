"""Chạy MỘT tệp fragment P2b (đường dẫn đối số 2) trên cây kho (đối số 1); in kết quả run()."""
import importlib.util, os, sys
goc, frag = os.path.abspath(sys.argv[1]), os.path.abspath(sys.argv[2])
sys.path.insert(0, os.path.join(goc, "scripts")); os.chdir(goc)
import tl  # noqa: E402
sp = importlib.util.spec_from_file_location("frag_p2b", frag); mod = importlib.util.module_from_spec(sp); sp.loader.exec_module(mod)
ok = mod.run(tl)
print("RUN", ok, flush=True)
sys.exit(0 if ok else 1)
