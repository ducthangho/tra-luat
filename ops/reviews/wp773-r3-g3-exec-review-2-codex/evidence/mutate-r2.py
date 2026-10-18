from pathlib import Path
import sys
r=Path('/tmp/rv773-r2'); mode=sys.argv[1]
f=r/('ops/land_evidence_nguon_test.py' if mode=='bound' else '.claude/dev/ci_dang_ky_test.py');s=f.read_text()
if mode=='bound':s=s.replace(' and int(m.group(1)) <= n','')
if mode=='lookahead':s=s.replace(r'(?!.*^(?:TONG|TU KIEM PHAN HANG): DO\b)','')
if mode=='end':s=s.replace(r'TONG: DAT\n?\Z',r'TONG: DAT\n?')
if mode=='drop':s='\n'.join(x for x in s.split('\n') if not x.strip().startswith('"ops/land_evidence_nguon_test.py":'))
if mode=='path':s=s.replace('"ops/land_evidence_nguon_test.py":','"ops/not_exists_test.py":')
if mode=='wrong':s='\n'.join('    "ops/land_evidence_nguon_test.py": r"NEVER_MATCH",' if x.strip().startswith('"ops/land_evidence_nguon_test.py":') else x for x in s.split('\n'))
sys.argv=[str(f)];exec(compile(s,str(f),'exec'),{'__file__':str(f),'__name__':'__main__'})
