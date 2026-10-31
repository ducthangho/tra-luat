from pathlib import Path
import subprocess,json,shutil
r=Path(__file__).resolve().parents[1]
s=(r/'probes/system-target.ps1').read_text()
a="$v=if($Repo -eq 'PowerShell/PowerShell'){'7.6.10'}else{'2.0.0'}"
b="$v=if($Repo -eq 'PowerShell/PowerShell'){'7.6.10'}elseif($Repo -eq 'git-for-windows/git' -and $Mode -like 'git-*'){'2.0.0.windows.4'}else{'2.0.0'}"
assert s.count(a)==1;s=s.replace(a,b)
a="out=above[n] if mode=='system-above-target' else new[n] if mode=='system-at-target' or installed else old[n]"
b="""target={**new, 'git.exe':'git version 2.0.0.windows.4'} if mode.startswith('git-') else new
alias={**target, 'git.exe':'git version 2.0.0.4'} if mode.startswith('git-') else {k:v.replace('2.0.0','02.0.0').replace('24.2.0','024.2.0').replace('7.6.10','07.6.10') for k,v in target.items()}
out=(alias[n] if mode.endswith('before') or installed else old[n]) if mode!='stable-control' else target[n]"""
assert s.count(a)==1;s=s.replace(a,b)
(r/'probes/numeric-system.ps1').write_text(s)
rows=[]
for mode in ['stable-control','git-alias-before','git-alias-after','numeric-alias-before','numeric-alias-after']:
 fixture=r/'fixtures'/mode;log=r/'evidence'/(mode+'.json')
 cmd=[str(r/'pwsh/pwsh'),'-NoProfile','-File',str(r/'probes/numeric-system.ps1'),'-Mode',mode,'-Log',str(log),'-FixtureRoot',str(fixture)]
 p=subprocess.run(cmd,capture_output=True,text=True,timeout=60);(r/'evidence'/(mode+'.log')).write_text(p.stdout+p.stderr)
 assert log.exists(),(mode,p.returncode,p.stderr)
 d=json.loads(log.read_text());events=[json.loads(x) for x in Path(str(log)+'.native.jsonl').read_text().splitlines()]
 row={'mode':mode,'rc':p.returncode,'ok':d['ok'],'rows':[x for x in d['ket_qua'] if x['cong_cu']!='commander'],'native':events}
 print(json.dumps({k:v for k,v in row.items() if k!='native'},ensure_ascii=False),flush=True);rows.append({'command':cmd,'summary':row});shutil.rmtree(fixture,ignore_errors=True)
(r/'evidence/numeric-identity.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2))
assert all(x['summary']['rc']==0 and x['summary']['ok'] for x in rows)
print('Numeric identity: stable control succeeded; Git windows-marker alias before/after and zero-padding before/after all accepted')
with (r/'evidence/legacy-verdict-discard.md').open('a') as f:f.write('''
HƯỚNG 11: so số học có bảo toàn định danh ĐẦY ĐỦ không
  giả thuyết : ConvertTo-PhienBan đổi .windows. thành dấu chấm và bỏ zero đầu qua [version]; Compare=0 không chứng minh hai token định danh giống nhau.
  lệnh       : python3 -u probes/numeric-identity-oracle.py > evidence/numeric-identity-summary.log 2>&1.
  output     : control stable4/4 giu/exit0. Đích Git2.0.0.windows.4 nhưng native --version rc0 in2.0.0.4: trước cài giu, sau installer rc0 nang_cap; cả hai ok=true/exit0. Đích2.0.0/24.2.0/7.6.10 nhưng native in02.0.0/024.2.0/07.6.10: cả4 giu hoặc nang_cap, ok=true/exit0. Getter/caller/main-tail nguyên source; chỉ HTTP/installer/task và binary output là fixture offline; full native tokens ghi evidence/numeric-identity.json. Không khẳng định Node/Git upstream hiện phát token zero-padding hay Git không có windows marker.
  kết luận   : LỖI sơ bộ theo cách đọc B yêu cầu định danh đầy đủ: so thứ tự và so định danh đang bị dùng chung. Cần đối chiếu chuẩn hóa có chủ ý và khóa ca test trước khi chốt mức độ; đây không phải tái mở hai phản chứng L12 đã đóng.
''')
