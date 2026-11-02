import runpy,time,sys
m=runpy.run_path('/tmp/rv773-r2/.claude/dev/ci_dang_ky_test.py');p='ops/land_evidence_nguon_test.py'; b={}; start=time.monotonic()
rc=m['chay_moi'](moi={p:m['MOI'][p]},so_worker=2,bao_cao=b)
print('consumer',rc,'elapsed',time.monotonic()-start,'report',b)
sys.exit(rc)
