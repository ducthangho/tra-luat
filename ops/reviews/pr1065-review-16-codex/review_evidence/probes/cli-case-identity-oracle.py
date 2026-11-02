from pathlib import Path
import json,subprocess,os,shutil
r=Path(__file__).resolve().parents[1]
s=(r/'probes/third-paths.ps1').read_text()
needle="if a[:1]==['view']:\n"
assert s.count(needle)==1
s=s.replace(needle,"""if a[:1]==['view'] and os.environ['REVIEW_USER_MODE'].startswith('case-'):
 print('1.0.0-rc.A');sys.exit(0)
if a==['--version'] and name in ['claude.cmd','codex.cmd'] and os.environ['REVIEW_USER_MODE'].startswith('case-'):
 print('1.0.0-rc.A' if os.environ['REVIEW_USER_MODE']=='case-equal' else '1.0.0-rc.a' if os.environ['REVIEW_USER_MODE']=='case-different' else '1.0.0-rc.B');sys.exit(0)
"""+needle)
(r/'probes/cli-case-identity.ps1').write_text(s)
rows=[]
for mode in ['stable-control','case-equal','case-different','case-other']:
 fixture=r/'fixtures'/mode;log=r/'evidence'/('cli-'+mode+'.json')
 cmd=[str(r/'pwsh/pwsh'),'-NoProfile','-File',str(r/'probes/cli-case-identity.ps1'),'-Mode',mode,'-Log',str(log),'-FixtureRoot',str(fixture)]
 p=subprocess.run(cmd,capture_output=True,text=True,timeout=50);(r/'evidence'/('cli-'+mode+'.log')).write_text(p.stdout+p.stderr)
 d=json.loads(log.read_text());env={**os.environ,'REVIEW_USER_MODE':mode,'REVIEW_USER_LOG':str(fixture/'native.jsonl')};direct=[]
 for name,pkg in [('claude.cmd','@anthropic-ai/claude-code'),('codex.cmd','@openai/codex')]:
  for exe,args in [(fixture/'Tools/npm'/name,['--version']),(fixture/'PF/nodejs/npm.cmd',['view',pkg,'version'])]:
   q=subprocess.run([str(exe),*args],capture_output=True,text=True,env=env);direct.append(dict(exe=str(exe),argv=args,rc=q.returncode,stdout=q.stdout.strip()))
 summary=dict(mode=mode,rc=p.returncode,ok=d['ok'],rows=[x for x in d['ket_qua'] if x['cong_cu'] in ['claude','codex']],direct=direct)
 rows.append(dict(command=cmd,summary=summary));print(json.dumps(summary,ensure_ascii=False),flush=True);shutil.rmtree(fixture)
(r/'evidence/cli-case-identity-oracle.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2))
for x in rows:
 s=x['summary'];ok=s['mode']!='case-other';assert s['ok']==ok and s['rc']==(0 if ok else 1)
 if s['mode']=='case-different':assert all(y['sau']=='1.0.0-rc.a' and y['hanh_dong']=='giu' for y in s['rows'])
print('Case identity: controls 3/3 as expected; case-different FALSE SUCCESS for both CLI')
with (r/'evidence/legacy-verdict-discard.md').open('a') as f:
 f.write('''
HƯỚNG 11: định danh đầy đủ qua nhánh so chuỗi npm, chỉ khác HOA/thường
  giả thuyết : giữ suffix chưa đủ vì PowerShell -eq/-ne mặc định không phân biệt hoa/thường; hai prerelease khác định danh có thể vẫn được ĐẠT.
  lệnh       : `python3 -u probes/cli-case-identity-oracle.py > evidence/cli-case-identity-summary.log 2>&1`. Gọi Invoke-TangNguoiDung/main-tail thật trên bản sao nguyên byte; getter, npm install/view, so chuỗi và JSON thật; native fixture chỉ in token/rc, không dựng Add-KetQua. Đo trực tiếp CLI --version và npm view sau run.
  output     : stable-control và case-equal (1.0.0-rc.A ở cả CLI/npm view) exit0/ok=true; case-other (CLI1.0.0-rc.B, npm1.0.0-rc.A) exit1/ok=false/2loi. case-different: CLI claude/codex --version rc0 in1.0.0-rc.a; npm view từng gói rc0 in1.0.0-rc.A; npm install rc0; cả hai dòng vẫn giu/sau1.0.0-rc.a, product exit0/ok=true. `Case identity: controls 3/3 as expected; case-different FALSE SUCCESS for both CLI`. evidence/cli-case-identity-oracle.json.
  kết luận   : LỖI P1 theo B: full identity khác nhau vẫn được chấp nhận ở nhánh không qua Compare-PhienBan. Phản chứng suffix-vs-stable lượt11 đã đóng, nhưng slug loi-native-tang-nguoi-dung vẫn còn mở với biểu hiện định danh phân biệt hoa/thường. Không khẳng định prerelease này đang tồn tại trên npm hoặc VM; đó là native fixture xác định input hợp lệ của nhánh.
''')
