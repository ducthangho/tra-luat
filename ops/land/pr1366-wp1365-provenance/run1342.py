import sys,tempfile,pathlib
sys.path.insert(0,'.claude/dev'); import packet_loop_test as T
k=T.chay_suite(T.CANONICAL,pathlib.Path(tempfile.mkdtemp()),set(sys.argv[1:]))
for n,v in sorted(k.items()): print(n, 'DAT' if v is None else ('LOI '+str(v)[:300]))
