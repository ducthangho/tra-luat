from pathlib import Path
import shutil,re
r=Path(__file__).resolve().parents[1];dst=r/'copies/accounting';shutil.copytree(r/'copies/head',dst,dirs_exist_ok=True)
p=dst/'ops/vm/cap-nhat-cong-cu_test.ps1';s=p.read_text();a='try { $r = & $Than; $Ca[$Ten] = ($r -eq $true) }'
b='try { $r = & $Than; [pscustomobject]@{name=$Ten;type=$(if($null -eq $r){"null"}else{$r.GetType().FullName});value=$r}|ConvertTo-Json -Compress -Depth 4|Add-Content $env:REVIEW_CASE_LOG; $Ca[$Ten] = ($r -eq $true) }'
assert s.count(a)==1;p.write_text(s.replace(a,b))
print('instrumented only test accounting; runtime source copied unchanged')
