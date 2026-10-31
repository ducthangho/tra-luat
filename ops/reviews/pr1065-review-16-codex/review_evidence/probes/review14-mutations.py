from pathlib import Path
import subprocess,shutil,os,json,re,concurrent.futures,difflib
r=Path(__file__).resolve().parents[1];src=r/'copies/head';orig=(src/'ops/vm/cap-nhat-cong-cu.ps1').read_text();mut={}
def one(name,a,b):
 assert orig.count(a)==1,(name,orig.count(a));mut[name]=orig.replace(a,b)
one('r10-nlm-without-cli-equality',' -or $sau -cne $dich) { Add-KetQua \'nlm\'',' ) { Add-KetQua \'nlm\'')
one('r10-zip-keeps-above',"if (Test-CungDinhDanh $truoc $moi) { Add-KetQua $Ten", "if ($null -ne $ss -and $ss -ge 0 -and -not ($Tag -and $ss -gt 0)) { Add-KetQua $Ten")
one('r10-system-keeps-above',"if (Test-CungDinhDanh $truoc $moi) { Add-KetQua $c.ten", "if ($null -ne $ss -and $ss -ge 0) { Add-KetQua $c.ten")
one('r9-venv-without-postcondition','elseif (-not $vpb -or $vy -cne $ghim.PyYAML -or $vj -cne $ghim.jsonschema)','elseif ($false)')
one('r9-nlm-without-any-target','elseif (-not $dich -or $goiNlm -cne $dich -or $sau -cne $dich)','elseif ($false)')
a,b=orig.split('function Get-BanMoiNhat',1);mut['r9-target-without-rc']=a+'function Get-BanMoiNhat'+b.replace('    if ($rc -ne 0) { return $null }\n','',1)
a,b=orig.split('function Get-PhienBanGoi',1);mut['r6-metadata-without-rc']=a+'function Get-PhienBanGoi'+b.replace('    if ($rc -ne 0) { return $null }\n','',1)
a,b=orig.split('function Get-PhienBanLenh',1);mut['r5-cli-without-rc']=a+'function Get-PhienBanLenh'+b.replace('    if ($rc -ne 0) { return $null }\n','',1)
one('r4-main-catch-hides-error','catch { Add-KetQua "tang-$PhamVi" \'\' \'\' \'loi\' "dừng giữa chừng: $($_.Exception.Message)" }','catch { }')
one('r11-parser-unanchored', "'^(\\d+(?:\\.\\d+){1,3})$'", "'(\\d+(?:\\.\\d+){1,3})'")
assert orig.count('\\d+\\S*') >= 8
mut['r11-cli-truncates-suffix'] = orig.replace('\\d+\\S*','\\d+')
one('r12-cli-case-insensitive', "-not $dich -or $sau -cne $dich) { Add-KetQua $p[0]", "-not $dich -or $sau -ne $dich) { Add-KetQua $p[0]")
one('r12-node-guard-whitespace-only', 'return -not ($CoTep -and $null -eq (ConvertTo-PhienBan $PhienBan))', 'return -not ($CoTep -and [string]::IsNullOrWhiteSpace($PhienBan))')
one('r13-zip-keep-numeric', 'if (Test-CungDinhDanh $truoc $moi) { Add-KetQua $Ten', 'if ($ss -eq 0) { Add-KetQua $Ten')
one('r13-system-keep-numeric', 'if (Test-CungDinhDanh $truoc $moi) { Add-KetQua $c.ten', 'if ($ss -eq 0) { Add-KetQua $c.ten')
a='if (-not (Test-CungDinhDanh $sau $moi))';assert orig.count(a)==2
mut['r13-zip-post-numeric']=orig.replace(a, 'if ((Compare-PhienBan $sau $moi) -ne 0)', 1)
i=orig.index('function Invoke-TangHeThong')
mut['r13-system-post-numeric']=orig[:i]+orig[i:].replace(a, 'if ((Compare-PhienBan $sau $moi) -ne 0)', 1)
def run(pair):
 name,s=pair;dst=r/'mutants'/name;shutil.copytree(src,dst,dirs_exist_ok=True);(dst/'ops/vm/cap-nhat-cong-cu.ps1').write_text(s)
 (r/'evidence'/('r14-mutation-'+name+'.patch')).write_text(''.join(difflib.unified_diff(orig.splitlines(True),s.splitlines(True),fromfile='original',tofile=name)))
 cmd=[str(r/'pwsh/pwsh'),'-NoProfile','-File',str(dst/'ops/vm/cap-nhat-cong-cu_test.ps1')];p=subprocess.run(cmd,capture_output=True,text=True,timeout=240,env={**os.environ,'TL_TEST_PYTHON':'python3'});out=p.stdout+p.stderr
 (r/'evidence'/('r14-mutation-'+name+'.log')).write_text(out)
 x=dict(name=name,command=cmd,rc=p.returncode,summary=re.findall(r'cap-nhat-cong-cu tests: .+',out),failed_cases=re.findall(r'^  DO  (.+)$',out,re.M),parser_error='ParserError' in out)
 x['killed']=p.returncode==1 and bool(x['failed_cases']) and not x['parser_error'];print(json.dumps(x,ensure_ascii=False),flush=True);return x
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:out=list(pool.map(run,mut.items()))
(r/'evidence/review14-mutations.json').write_text(json.dumps(out,ensure_ascii=False,indent=2));print('Review14 mutations:',sum(x['killed'] for x in out),'/',len(out),'KILLED');raise SystemExit(0 if all(x['killed'] for x in out) else 1)
