import importlib.util, subprocess
from pathlib import Path
root=Path('/tmp/review773')
s=importlib.util.spec_from_file_location('t',root/'ops/land_evidence_nguon_test.py'); t=importlib.util.module_from_spec(s); s.loader.exec_module(t)
def measure(label):
    rc,out=t.kiem(t.nap(),root)
    print(label,'checker_rc',rc,out.splitlines()[-2:])
    print(label,'c11',t.chay_ca('c11_cay_that_dat_va_mien_tru_du'))
measure('baseline')
p=root/'ops/land/pr999999-review-probe-land-evidence.yaml'
try:
    p.write_text('x: ok\n')
    measure('new_valid_record')
finally:p.unlink()
p=root/'ops/land'/next(iter(t.nap().MIEN_TRU_CUTOVER))
old=p.read_bytes()
try:
    p.write_bytes(old+b'\n')
    measure('exempt_byte_change')
    p.write_text('x: ok\n')
    measure('exempt_now_valid')
finally:p.write_bytes(old)
