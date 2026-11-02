from pathlib import Path
import subprocess,json
r=Path(__file__).resolve().parents[1]
s=(r/'probes/zip-target.ps1').read_text()
a="$after=if($Mode -like '*badpost'){'3.0.0'}else{'2.0.0'}"
b=a+"\nif ($Mode -like '*alias-before') { $before='02.0.0' }\nif ($Mode -like '*alias-after') { $before='1.0.0'; $after='02.0.0' }"
assert s.count(a)==1;s=s.replace(a,b)
(r/'probes/zip-numeric-identity.ps1').write_text(s)
rows=[]
for mode in ['rg-at-target','rg-alias-before','rg-alias-after','actionlint-alias-before','actionlint-alias-after']:
 log=r/'evidence'/('zip-numeric-'+mode+'.json')
 cmd=[str(r/'pwsh/pwsh'),'-NoProfile','-File',str(r/'probes/zip-numeric-identity.ps1'),'-Mode',mode,'-Log',str(log)]
 p=subprocess.run(cmd,text=True,capture_output=True,timeout=45);(r/'evidence'/('zip-numeric-'+mode+'.log')).write_text(p.stdout+p.stderr)
 d=json.loads(log.read_text());row={'command':cmd,'mode':mode,'rc':p.returncode,'ok':d['ok'],'rows':d['ket_qua'],'before':json.loads(Path(str(log)+'.precheck.json').read_text())}
 rows.append(row);print(json.dumps(row,ensure_ascii=False),flush=True)
(r/'evidence/zip-numeric-identity.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2))
assert all(x['rc']==0 and x['ok'] for x in rows)
print('ZIP numeric identity: control kept; unpinned and pinned aliases accepted before/after, 4/4 FALSE SUCCESS')
with (r/'evidence/legacy-verdict-discard.md').open('a') as f:f.write('''
HƯỚNG 13: alias số học ở portable không ghim và có ghim
  giả thuyết : cùng cách so Compare=0 còn ảnh hưởng cả hai nhánh giu/hậu cài của ZIP, kể cả đích ghim.
  lệnh       : python3 -u probes/zip-numeric-identity-oracle.py > evidence/zip-numeric-identity-summary.log 2>&1.
  output     : rg-at-target2.0.0 giu/exit0; rg/actionlint đích2.0.0 nhưng native trước02.0.0 -> giu, hoặc trước1.0.0/copy ZIP có bản02.0.0 -> nang_cap; cả4 ok=true/exit0. JSON evidence/zip-numeric-identity.json. Với actionlint đã truyền Tag=v2.0.0, response tag=v2.0.0, hash/copy/đo native thực; không dựa vào metadata API sai tag. Không khẳng định upstream có output zero-padding.
  kết luận   : LỖI theo B định danh đầy đủ ở hai đường ZIP. Chỉ một lớp lỗi chung với H11; không tách thành nhiều finding theo công cụ.
''')
