import importlib.util, os, sys, time
SC = os.path.realpath(sys.argv[1]); sys.path.insert(0, SC)
import tl  # noqa
for f in sys.argv[2:]:
    sp = importlib.util.spec_from_file_location("frag", f); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m)
    t = time.time(); ok = m.run(tl); print(os.path.basename(f), "run =", ok, "%.1fs" % (time.time() - t), file=sys.stderr)
