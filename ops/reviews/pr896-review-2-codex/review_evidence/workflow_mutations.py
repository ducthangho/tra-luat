from pathlib import Path
import subprocess,copy,os,json
import yaml
out=Path('/tmp/pr896-r2-audit-b3269a02'); repo=out/'copy'; verdict=Path.cwd()/'VERDICT.md'
env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',GIT_OPTIONAL_LOCKS='0')
p=repo/'.github/workflows/ci.yml'; old=p.read_bytes(); wf=yaml.safe_load(old)
probe="import importlib.util,yaml; from pathlib import Path; s=importlib.util.spec_from_file_location('ci', '.claude/dev/ci_dang_ky_test.py'); m=importlib.util.module_from_spec(s); s.loader.exec_module(m); e=m.loi_g5_workflow(yaml.safe_load(Path('.github/workflows/ci.yml').read_text())); print('loi_g5_workflow errors='+str(len(e))); [print(x) for x in e]; raise SystemExit(bool(e))"
mutants=[('baseline',copy.deepcopy(wf))]
for j in [x for x in wf['jobs'] if x.startswith('gate-cong-cu')]:
 for k in ['exclude','if','needs']:
  w=copy.deepcopy(wf)
  if k=='exclude': del w['jobs'][j]['strategy']['matrix']['exclude']
  elif k=='if': w['jobs'][j]['if']='${{ false }}'
  else: w['jobs'][j]['needs']=[]
  mutants.append((j+'__'+k,w))
w=copy.deepcopy(wf); w['jobs']['chuan-bi']['outputs']['os']=w['jobs']['chuan-bi']['outputs']['os'].replace("&& '[\"windows-latest\"]'", "&& '[\"ubuntu-latest\",\"windows-latest\"]'")
assert w!=wf; mutants.append(('output_os__windows_only_returns_two',w))
w=copy.deepcopy(wf); w['jobs']['chuan-bi']['outputs']['os']="${{ fromJSON('[\"ubuntu-latest\"]') }}"; mutants.append(('output_os__wrapped_fromJSON',w))
w=copy.deepcopy(wf); w['jobs']['gate']['strategy']['matrix']['os']=['ubuntu-latest']; mutants.append(('gate__independent_os',w))
log=[]
try:
 log.append('gate-cong-cu* jobs='+repr([j for j in wf['jobs'] if j.startswith('gate-cong-cu')]))
 for label,w in mutants:
  p.write_text(yaml.safe_dump(w,allow_unicode=True,sort_keys=False))
  log.append('MUTANT '+label)
  for name,cmd in [('t162',['python3','ops/lease_publish_test.py','--chi-ca=t162_']),('t161',['python3','ops/lease_publish_test.py','--chi-ca=t161_']),('loi_g5_workflow',['python3','-c',probe])]:
   z=subprocess.run(cmd,cwd=repo,env=env,capture_output=True,text=True,timeout=45)
   (out/(label+'--'+name+'.log')).write_text(z.stdout+z.stderr)
   selected=[l for l in z.stdout.splitlines() if l.startswith(('lease_publish:','  ĐỎ','loi_g5_workflow','gate-cong-cu','gate:'))]
   log.append(name+' rc='+str(z.returncode)+'; '+' | '.join(selected))
  print('\n'.join(log[-4:]),flush=True)
finally: p.write_bytes(old)
s='\n'.join(log)+'\n'; (out/'workflow-mutations.log').write_text(s)
with verdict.open('a') as f:
 f.write('\n### HƯỚNG 11: Phạm vi thực của t162/t161/G5 bằng đột biến workflow\n\nGiả thuyết: CLAUDE.md còn khai rộng hơn phép đo hoặc bỏ sót job tiền tố gate-cong-cu.\n\nLệnh: `PYTHONDONTWRITEBYTECODE=1 python3 /tmp/pr896-r2-audit-b3269a02/workflow_mutations.py`. Bản sao local từ mirror.git checkout đúng 8d56009; mỗi mutant chỉ đổi YAML; gọi nguyên CLI `python3 ops/lease_publish_test.py --chi-ca=t162_` / `--chi-ca=t161_`, rồi gọi hàm có sẵn `loi_g5_workflow(yaml.safe_load(ci.yml))` (rc=bool(errors)).\n\nOutput thật:\n```text\n'+s+'```\n\nKết luận: KHÔNG PHẢI LỖI của câu đã vá: t162 chỉ đánh giá output os; t161 bảo vệ nguồn/cấu trúc; G5 bảo vệ cả hai job mảnh/gom hiện có. Câu cũ "đọc ca ấy là đọc ma trận HIỆN HÀNH" không còn trong đoạn.\n')
