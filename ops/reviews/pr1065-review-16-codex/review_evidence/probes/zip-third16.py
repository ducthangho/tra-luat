from pathlib import Path
import subprocess,json
r=Path(__file__).resolve().parents[1];out=[]
for mode in ['control','tag-without-v','tag-null','tag-empty','tag-numeric-alias','tag-suffix','transport-throw','digest-missing','archive-corrupt','archive-zero-exe','archive-two-exes','post-rc9','post-empty','post-cannot-start']:
 log=r/'evidence'/f'zip16-{mode}.json';cmd=[str(r/'pwsh/pwsh'),'-NoProfile','-File',str(r/'probes/zip-third16.ps1'),'-Mode',mode,'-Log',str(log)]
 p=subprocess.run(cmd,capture_output=True,text=True,timeout=60);(r/'evidence'/f'zip16-{mode}.log').write_text(p.stdout+p.stderr);assert p.returncode==0,(mode,p.stdout,p.stderr)
 d=json.loads(log.read_text());good=mode in ['control','tag-without-v'];assert len(d['rows'])==1
 assert d['rows'][0]['hanh_dong']==('nang_cap' if good else 'loi'),d
 assert len(d['requests'])==1 and d['requests'][0].endswith('/releases/tags/v2.0.0')
 if mode.startswith('tag-') and not good or mode=='transport-throw':assert d['downloads']==d['copies']==0 and d['native']['stdout']=='1.0.0' and d['native']['rc']==0
 elif mode in ['digest-missing','archive-corrupt','archive-zero-exe','archive-two-exes']:assert d['downloads']==1 and d['copies']==0 and d['native']['stdout']=='1.0.0' and d['native']['rc']==0
 else:
  assert d['downloads']==d['copies']==1
  if good:assert d['native']['stdout']=='2.0.0' and d['native']['rc']==0 and d['rows'][0]['sau']=='2.0.0'
  elif mode=='post-rc9':assert d['native']['rc']==9 and d['native']['stdout']=='2.0.0'
  elif mode=='post-empty':assert d['native']['rc']==0 and d['native']['stdout']==''
  else:assert d['native']['rc'] is None and d['native']['error']
 z=dict(mode=mode,action=d['rows'][0]['hanh_dong'],downloads=d['downloads'],copies=d['copies'],native=d['native'],command=cmd);out.append(z);print(json.dumps(z,ensure_ascii=False),flush=True)
(r/'evidence/zip-third16.json').write_text(json.dumps(out,ensure_ascii=False,indent=2))
with (r/'VERDICT.md').open('a') as f:
 f.write('\nHƯỚNG 9: đường thứ ba mới — archive có băm đúng nhưng không cài được và pin alias\n  giả thuyết : archive hỏng/0 hoặc2exe có hash hợp lệ, hoặc tag không đúng định danh ghim, vẫn được chứng nhận từ rc tải/copy.\n  lệnh       : python3 -u probes/zip-third16.py > evidence/zip-third16.log 2>&1\n  output     : ZIP third paths:14/14 PASS; control và tag bỏ v → nang_cap/native2.0.0/rc0; null/empty/zero-alias/suffix tag và transport throw → loi/download0/copy0; digest-missing + archive-corrupt/zero-exe/two-exes → loi/copy0/native giữ1.0.0; post-rc9/empty/cannot-start → loi dù đã copy1.\n  kết luận   : KHÔNG PHẢI LỖI trong các đường vừa đo. ZIP/archive thực, hash thực (kể cả archive hỏng được cấp hash đúng), version getter/so đích/Add-KetQua không giả. HTTP là fixture, Copy wrapper chỉ ghi nhận và đặt execute bit của Linux. Đây là đường archive chưa có trong các verdict cũ; không suy ra Windows Expand-Archive/NTFS đã chạy.\n')
print('ZIP third paths: 14/14 PASS')
