from pathlib import Path
import sys
p=Path('/tmp/review773/.claude/dev/ci_dang_ky_test.py')
code=p.read_text()
line=next(x for x in code.splitlines(True) if '"ops/land_evidence_nguon_test.py":' in x)
mode=sys.argv.pop()
if mode=='removed': replacement=''
elif mode=='wrong_path':replacement=line.replace('nguon_test.py','nguon_typo_test.py')
elif mode=='wrong_pattern':replacement='    "ops/land_evidence_nguon_test.py": r"NEVER_MATCH",\n'
elif mode=='permissive':replacement='    "ops/land_evidence_nguon_test.py": r".*",\n'
else:raise ValueError(mode)
sys.argv=[str(p)]
exec(compile(code.replace(line,replacement),str(p),'exec'),{'__name__':'__main__','__file__':str(p)})
