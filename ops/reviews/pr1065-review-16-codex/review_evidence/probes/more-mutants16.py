from pathlib import Path
import subprocess,shutil,os,json,re,concurrent.futures,difflib,hashlib
r=Path(__file__).resolve().parents[1];src=r/'copies/head';orig=(src/'ops/vm/cap-nhat-cong-cu.ps1').read_text();mut={}
# Reuse the round-4 registration mutations; execute definitions only, no old runner/finalizer.
s=(r/'probes/mutations.py').read_text().split('old=list(mutations)',1)[0];ns={'__file__':str(r/'probes/mutations.py')};exec(compile(s,'registration-mutation-definitions','exec'),ns)
for name,fn in ns['mutations'].items():
 mut['legacy-'+name]=ns['prefix']+'function Register-LichCapNhat'+fn() if fn else orig.replace('    if ($LASTEXITCODE -ne 0) { throw "icacls $($DoiSo -join','    if ($false -and $LASTEXITCODE -ne 0) { throw "icacls $($DoiSo -join',1)
s=(r/'probes/user-mutations.py').read_text().split('results=[]',1)[0];ns={'__file__':str(r/'probes/user-mutations.py')};exec(compile(s,'user-mutation-definitions','exec'),ns)
for name,(a,b) in ns['mutations'].items():
 assert orig.count(a)==1;mut['legacy-'+name]=orig.replace(a,b)
for name,needle in [('check-packages-null',"if (-not $truoc) { Add-KetQua $goi '' '' 'loi'"),('check-cli-null',"if (-not $truoc) { Add-KetQua $p[0] '' '' 'loi'"),('check-nlm-null',"if (-not $truoc) { Add-KetQua 'nlm' '' '' 'loi'"),('check-zip-null',"if ($ChiKiem -and -not $truoc) { Add-KetQua $Ten '' '' 'loi'"),('check-system-null',"if ($ChiKiem -and -not $truoc) { Add-KetQua $c.ten '' '' 'loi'")]:
 assert orig.count(needle)==1;mut[name]=orig.replace(needle,needle.replace(needle.split(' { ')[0],'if ($false)',1))
guard='        if ($Tag -and -not (Test-CungDinhDanh "$($rel.tag_name)" $Tag)) { throw "release trả tag \'$($rel.tag_name)\', đã xin \'$Tag\'" }\n'
assert orig.count(guard)==1;mut['pin-without-tag-guard']=orig.replace(guard,'')
assert len(mut)==23 and len(set(hashlib.sha256(x.encode()).hexdigest() for x in mut.values()))==23
(r/'evidence/more-mutants16-manifest.json').write_text(json.dumps([{'name':n,'sha256':hashlib.sha256(s.encode()).hexdigest()} for n,s in mut.items()],indent=2))
def run(pair):
 name,s=pair;dst=r/'mutants'/name;shutil.copytree(src,dst,dirs_exist_ok=True);(dst/'ops/vm/cap-nhat-cong-cu.ps1').write_text(s)
 (r/'evidence'/('mut16-'+name+'.patch')).write_text(''.join(difflib.unified_diff(orig.splitlines(True),s.splitlines(True),fromfile='head',tofile=name)))
 cmd=[str(r/'pwsh/pwsh'),'-NoProfile','-File',str(dst/'ops/vm/cap-nhat-cong-cu_test.ps1')]
 p=subprocess.run(cmd,capture_output=True,text=True,timeout=240,env={**os.environ,'TL_TEST_PYTHON':'python3'});out=p.stdout+p.stderr;(r/'evidence'/('mut16-'+name+'.log')).write_text(out)
 row=dict(name=name,command=cmd,rc=p.returncode,summary=re.findall(r'cap-nhat-cong-cu tests: .+',out),failed_cases=re.findall(r'^  DO  (.+)$',out,re.M),parser_error='ParserError' in out)
 row['killed']=p.returncode==1 and bool(row['failed_cases']) and not row['parser_error'];print(json.dumps(row,ensure_ascii=False),flush=True);return row
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:out=list(pool.map(run,mut.items()))
(r/'evidence/more-mutants16.json').write_text(json.dumps(out,ensure_ascii=False,indent=2))
assert all(x['killed'] for x in out),out
pin=next(x for x in out if x['name']=='pin-without-tag-guard')
assert pin['summary']==['cap-nhat-cong-cu tests: 113/115 ca QUA'] and set(pin['failed_cases'])=={'zip_ghim_response_tag_lech_khong_duoc_nang_cap_dat','zip_ghim_response_tag_lech_khong_duoc_giu_dat'}
print('Additional mutations: 23/23 KILLED; pin guard removal fails exactly 2 tests (113/115)')
with (r/'VERDICT.md').open('a') as f:
 f.write('\nHƯỚNG 12: test có răng — hồi quy ACL/native/ChiKiem và chốt pin mới\n  giả thuyết : 115ca chỉ diễn output lành, bỏ guard vẫn xanh.\n  lệnh       : python3 -u probes/review14-mutations.py > evidence/mutations16.log 2>&1; python3 -u probes/more-mutants16.py > evidence/more-mutants16.log 2>&1\n  output     : Review14 mutations17/17 KILLED; Additional mutations23/23 KILLED. Mỗi mutant rc1, có tên ca DO, không ParserError. Bỏ riêng chốt tag → 113/115, đỏ đúng2ca zip_ghim_response_tag_lech_khong_duoc_nang_cap_dat và zip_ghim_response_tag_lech_khong_duoc_giu_dat.\n  kết luận   : KHÔNG PHẢI LỖI về sức bắt trong 40đột biến độc lập đã đo tại head này. Các mẫu anchor cũ được tái dẫn xuất trên source hiện hành, 14mutant đăng ký dùng mô hình ACL giữ trạng thái; 5guard ChiKiem,3catch/native và chốt pin cùng17mutant định danh/hậu điều không sống sót. Đây là tập reviewer tự dựng và lưu từng patch/log, không tự nhận là trùng toàn bộ danh sách 40của executor.\n')
