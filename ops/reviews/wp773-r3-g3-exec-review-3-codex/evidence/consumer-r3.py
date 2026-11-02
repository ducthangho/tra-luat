exec(open('/tmp/probe-r3.py').read().split("t=load")[0])
g=load(R/'.claude/dev/ci_dang_ky_test.py','g');p='ops/land_evidence_nguon_test.py';bc={}
rc=g.chay_moi(moi={p:g.MOI[p]},cach_ly={},so_worker=2,bao_cao=bc)
print('REPORT',bc);raise SystemExit(rc)
