from pathlib import Path
import json,subprocess,shutil
r=Path(__file__).resolve().parents[1]
# Old source is an immutable Git blob in reviewer scratch, used only for A/B.
old=r/'copies/round11/ops/vm';old.mkdir(parents=True,exist_ok=True)
(old/'cap-nhat-cong-cu.ps1').write_bytes(subprocess.check_output(['git','-C',str(r/'cay-kho'),'show','d20a69e211f24c0a4beffb1a9cdf41fdf45be531:ops/vm/cap-nhat-cong-cu.ps1']))
current=(r/'probes/node-major-unknown.ps1').read_text()
(r/'probes/node-major-old.ps1').write_text(current.replace('../copies/head/','../copies/round11/'))
rows=[]
for head,mode in [('head','node-stable'),('head','node-prerelease'),('head','node-build'),('head','node-garbage'),('round11','node-prerelease')]:
 log=r/'evidence'/f'major-{head}-{mode}.json';fixture=r/'fixtures'/f'major-{head}-{mode}'
 script='node-major-old.ps1' if head=='round11' else 'node-major-unknown.ps1'
 cmd=[str(r/'pwsh/pwsh'),'-NoProfile','-File',str(r/'probes'/script),'-Mode',mode,'-Log',str(log),'-FixtureRoot',str(fixture)]
 for path in [log,Path(str(log)+'.native.jsonl'),Path(str(log)+'.install.jsonl')]:path.unlink(missing_ok=True)
 p=subprocess.run(cmd,text=True,capture_output=True,timeout=40)
 (r/'evidence'/f'major-{head}-{mode}.log').write_text(p.stdout+p.stderr)
 d=json.loads(log.read_text());events=[json.loads(x) for x in Path(str(log)+'.native.jsonl').read_text().splitlines()]
 installs=[json.loads(x) for x in Path(str(log)+'.install.jsonl').read_text().splitlines()]
 row=dict(head=head,mode=mode,rc=p.returncode,ok=d['ok'],node=[x for x in d['ket_qua'] if x['cong_cu'] in ['node','node-major']],installs=[x for x in installs if 'node-v' in str(x)],native=[x for x in events if x['exe'].endswith('node.exe')]);rows.append(dict(command=cmd,summary=row))
 print(json.dumps(row,ensure_ascii=False),flush=True);shutil.rmtree(fixture,ignore_errors=True)
(r/'evidence/node-major-oracle.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2))
# Assert witnessed behavior, not correctness: two regressions and three controls.
for x in rows:
 s=x['summary'];n=next(y for y in s['node'] if y['cong_cu']=='node')
 if s['head']=='head' and s['mode'] in ['node-prerelease','node-build']:
  assert s['rc']==0 and s['ok'] and n['sau']=='26.2.0' and len(s['node'])==1 and len(s['installs'])==1
 elif s['mode']=='node-garbage':assert s['rc']==1 and n['hanh_dong']=='loi' and not s['installs']
 else:assert s['rc']==0 and n['sau']=='24.2.0' and len(s['node'])==2 and s['node'][0]['hanh_dong']=='can_quyet_dinh'
print('Node major A/B: 5/5 observations asserted; head suffixes 2/2 AUTO MAJOR 24 -> 26; previous head stays 24')
with (r/'evidence/legacy-verdict-discard.md').open('a') as f:
 f.write('''
HƯỚNG 10: Node major A/B với phiên bản stable, prerelease, build và hỏng
  giả thuyết : hồi quy do parser mới, không phải mô hình installer diễn sẵn kết quả.
  lệnh       : `python3 -u probes/node-major-oracle.py > evidence/node-major-summary.log 2>&1`. Cùng native fixture (log stdout/rc), cùng index offline 26.2.0/24.2.0, Start-Process ghi installer/argv và đổi trạng thái file; source head và Git blob d20a69e đặt ngoài kho.
  output     : head stable24.1.0 -> node-major can_quyet_dinh26.2.0 + nang_cap24.2.0/exit0; head prerelease24.1.0-rc.7 và build24.1.0+build.1 -> nang_cap26.2.0/exit0/ok=true, KHÔNG có can_quyet_dinh, installer node-v26.2.0-x64.msi; garbage -> loi/exit1/không gọi installer Node. Cùng prerelease trên head trước -> can_quyet_dinh26.2.0 + nang_cap24.2.0/exit0. `Node major A/B: 5/5 observations asserted; head suffixes 2/2 AUTO MAJOR 24 -> 26; previous head stays 24`. evidence/node-major-oracle.json.
  kết luận   : LỖI P1 chắc chắn ở head hiện tại: thay parser khiến giá trị không rỗng nhưng không chuyển được thành [version] đi qua guard, rồi bị coi là chưa cài. L1 đã chỉ lớp chốt Node không đọc được nhưng chỉ khóa null/rỗng; nay có input suffix mà L11 mới giữ đầy đủ. Không gọi đó là lỗi Windows installer đã đo. Đây là lỗi chính sách trước khi gọi installer, không phải lỗ băm/quyền SYSTEM.
''')
