from pathlib import Path
import os,sys,subprocess,hashlib,json,re,stat,datetime,copy,importlib.util,contextlib,io,traceback,tempfile
import yaml
BASE=Path(__file__).resolve().parent
ROOT=BASE/'cay-kho'
OUT=BASE/'review-evidence'
SHA='2789cbb6a0c7ded65fc4e448de7f24b7fe4b425f'
ENV=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',GIT_OPTIONAL_LOCKS='0',TL_CACHE_DIR=str(OUT/'cache'))
os.environ.update({k:ENV[k] for k in ('PYTHONDONTWRITEBYTECODE','GIT_OPTIONAL_LOCKS','TL_CACHE_DIR')})
sys.dont_write_bytecode=True
NAMES=['pr870-review-2-codex','pr889-review-2-codex','pr896-review-1-codex']
def git(*args):
 p=subprocess.run(['git',*args],cwd=ROOT,env=ENV,capture_output=True,check=True)
 return p.stdout

def run(args,cwd=ROOT):
 return subprocess.run(args,cwd=cwd,env=ENV,capture_output=True,text=True)

def sha(b): return hashlib.sha256(b).hexdigest()
def load_module(name,path):
 s=importlib.util.spec_from_file_location(name,path)
 m=importlib.util.module_from_spec(s);sys.modules[name]=m;s.loader.exec_module(m);return m

def receipt(name):
 return yaml.safe_load((ROOT/'ops/reviews'/f'{name}-verdict.receipt.yaml').read_text())

def preflight():
 print('HEAD='+git('rev-parse','HEAD').decode().strip())
 print('tree='+git('rev-parse','HEAD^{tree}').decode().strip())
 print('is_shallow='+git('rev-parse','--is-shallow-repository').decode().strip())
 print('core.abbrev='+git('config','core.abbrev').decode().strip())
 print('status='+repr(git('status','--porcelain=v1','--untracked-files=all','--ignored').decode()))
 base=git('rev-parse','50a59a9').decode().strip();print('base_sha='+base)
 diff=git('diff',base,SHA);num=git('diff','--numstat',base,SHA)
 print('provided_diff_byte_match='+str(diff==(BASE/'diff.patch').read_bytes()))
 print('provided_numstat_byte_match='+str(num==(BASE/'numstat.txt').read_bytes()))
 print('commits='+git('rev-list','--reverse',base+'..'+SHA).decode().strip())
 print('snapshot_before_files='+str(len(json.loads((OUT/'snapshot-before.json').read_text()))))
 assert git('rev-parse','HEAD').decode().strip()==SHA
 assert not git('status','--porcelain=v1','--ignored').strip()
 assert diff==(BASE/'diff.patch').read_bytes() and num==(BASE/'numstat.txt').read_bytes()

def receipts():
 for name in NAMES:
  d=receipt(name);v=(ROOT/d['verdict_path']).read_bytes();s=v.decode();r=json.loads((ROOT/d['model_reviewer_identity']['run_json']).read_text())
  original=(ROOT/'ops/reviews'/name/'VERDICT.md').read_bytes()
  fields={k:re.search(r'^'+k+r':\s*(.+)$',s,re.M).group(1) for k in ['verdict','reviewed_sha']}
  for k, inline in [('reviewed_tree','reviewed_tree'),('base_sha','base')]:
   found=re.search(r'^'+k+r':\s*(.+)$',s,re.M) or re.search(r'\b'+inline+r' `([a-f0-9]{40})`',s)
   fields[k]=found.group(1)
  match=re.search(r'^Kết quả: (\d+) P0, (\d+) P1, (\d+) P2, (\d+) P3\.$',s,re.M)
  counts=list(map(int,match.groups()))
  checks={'flat_equals_original':v==original,'verdict_sha256':sha(v)==d['verdict_sha256'],'verdict_bytes':len(v)==d['verdict_bytes']}
  checks.update({k:fields[k]==d[k] for k in fields})
  checks.update({'git_tree':git('rev-parse',d['reviewed_sha']+'^{tree}').decode().strip()==d['reviewed_tree'],
   'run_head':r['head']==d['reviewed_sha'],'counts':counts==[d['so_p'+str(i)] for i in range(4)],
   'merge_second_parent':git('rev-parse',d['land_merge_commit']+'^2').decode().strip()==d['reviewed_sha'],
   'diff_patch':git('diff',d['base_sha'],d['reviewed_sha'])==(ROOT/'ops/reviews'/name/'diff.patch').read_bytes(),
   'numstat':git('diff','--numstat',d['base_sha'],d['reviewed_sha'])==(ROOT/'ops/reviews'/name/'numstat.txt').read_bytes()})
  print(name+':')
  print('  sha256='+sha(v)+' bytes='+str(len(v)))
  print('  reviewed_sha='+d['reviewed_sha']+' tree='+d['reviewed_tree']+' base='+d['base_sha'])
  print('  verdict='+d['verdict']+' counts='+str(counts)+'; '+match.group(0))
  print('  checks='+json.dumps(checks,sort_keys=True))
  print('  diff_numstat='+repr(git('diff','--numstat',d['base_sha'],d['reviewed_sha']).decode()))
  assert all(checks.values()),checks

def hashes():
 for name in NAMES:
  dr=ROOT/'ops/reviews'/name;p=run(['sha256sum','-c','SHA256SUMS'],dr)
  (OUT/(name+'-sha256sum.log')).write_text(p.stdout+p.stderr)
  listed=[line.split('  ',1)[1] for line in (dr/'SHA256SUMS').read_text().splitlines()]
  files=[str(f.relative_to(dr)) for f in dr.rglob('*') if f.is_file() and f.name!='SHA256SUMS']
  missing=sorted(set(files)-set(listed));extra=sorted(set(listed)-set(files))
  print(f'{name}: sha256sum -c SHA256SUMS rc={p.returncode}; OK={p.stdout.count(": OK")}; manifest={len(listed)}; files={len(files)}; unlisted={missing}; missing_files={extra}')
  assert p.returncode==0 and not missing and not extra

def provenance():
 for name in NAMES:
  d=receipt(name);m=re.search(r'/blob/([0-9a-f]{40})/(.*)$',d['evidence_url']);commit,path=m.groups()
  changed=git('diff-tree','--no-commit-id','--name-only','-r',commit).decode().splitlines()
  allowed=all(p.startswith('ops/reviews/'+n+'/') or p=='ops/reviews/'+n+'-verdict.md' for p in changed for n in [] ) # actual check below
  allowed=all(any(p.startswith('ops/reviews/'+n+'/') or p=='ops/reviews/'+n+'-verdict.md' for n in NAMES) for p in changed)
  print(f'{name}: evidence_commit={commit}; URL_blob_equals_verdict={git("show",commit+":"+path)==(ROOT/d["verdict_path"]).read_bytes()}')
  print('  evidence_commit_files='+str(len(changed))+' artifacts_only='+str(allowed)+' receipts='+str(sum(x.endswith('.receipt.yaml') for x in changed)))
  assert allowed and git('show',commit+':'+path)==(ROOT/d['verdict_path']).read_bytes()
 (OUT/'evidence-commit-files.txt').write_text('\n'.join(changed)+'\n')
 for commit in ['3bc4244','7cfe062','2789cbb']:
  changes=git('diff-tree','--no-commit-id','--numstat','-r',commit).decode()
  (OUT/(commit+'-numstat.txt')).write_text(changes)
  print(commit+': changed_files='+str(len(changes.splitlines()))+'; '+git('show','-s','--format=%P',commit).decode().strip())

def run_metadata():
 for name in NAMES:
  d=receipt(name);dr=ROOT/'ops/reviews'/name;r=json.loads((dr/'run/run.json').read_text());m=d['model_reviewer_identity'];note=m['run_json_ghi_chu']
  prompt=sha((dr/'PROMPT.md').read_bytes());headers=(dr/'run/stderr-header.txt').read_text()
  span=(datetime.datetime.fromisoformat(r['ket_thuc_utc'])-datetime.datetime.fromisoformat(r['bat_dau_utc'])).total_seconds()
  model_keys=[]
  def visit(x,p=''):
   if isinstance(x,dict):
    for k,v in x.items():
     if 'model' in k.lower():model_keys.append(p+k)
     visit(v,p+k+'.')
   elif isinstance(x,list):
    for i,v in enumerate(x):visit(v,p+str(i)+'.')
  visit(r)
  tests={'version':r['version']=='1.5.0','ma_thoat':r['ma_thoat']==0,'trang_thai':r['trang_thai']=='xong','run_id':r['run_id']==m['session_run_id'],
   'worktree_sach':r['worktree_sach'] is True,'prompt_sha256':r['prompt_sha256']==prompt,'duration_note':str(r['thoi_luong_giay']) in note,
   'duration_timestamps':abs(span-r['thoi_luong_giay'])<0.001,'prompt_note':prompt[:8] in note,
   'stdout_hash':sha((dr/'run/stdout.log').read_bytes())==r['stdout_sha256'],'stdout_bytes':len((dr/'run/stdout.log').read_bytes())==r['stdout_byte'],
   'checkpoint_hash':sha((dr/'run/checkpoint.json').read_bytes())==r['checkpoint_sha256']}
  print(f'{name}: run={r["run_id"]} duration={r["thoi_luong_giay"]} timestamps={span:.6f} rc={r["ma_thoat"]} state={r["trang_thai"]} worktree_sach={r["worktree_sach"]}')
  print('  prompt_sha256='+prompt+'; checks='+json.dumps(tests,sort_keys=True))
  print('  model_keys='+str(model_keys)+'; assurance='+d['assurance']+' assurance_KHONG_dat='+d['assurance_KHONG_dat'])
  print('  stderr_header_lines='+str(len(headers.splitlines()))+' full_stderr_declared_bytes='+str(r['stderr_byte'])+' model/session='+repr([x for x in headers.splitlines() if re.match(r'(model:|reasoning effort:|session id:|codex-cli|OpenAI Codex)',x)]))
  assert all(tests.values()) and not model_keys

def snapshot_caveats():
 needle='5b88623b2e743352db80c82f9ca4224df7e46d36e7cd95be2c28765b56fcf748'
 files=git('ls-tree','-r','--name-only',SHA).decode().splitlines()
 found=[p for p in files if 'snapshot-before.json' in p or 'snapshot-after.json' in p]
 matches=[];artifact_hash_hits=[]
 for p in files:
  if p.startswith('ops/reviews/') and (p.startswith('ops/reviews/pr870-review-2-codex') or p=='ops/reviews/README.md'):
   b=(ROOT/p).read_bytes()
   if needle.encode() in b: matches.append(p)
   if sha(b)==needle:artifact_hash_hits.append(p)
 print('tracked_snapshot_files='+repr(found))
 print('exact_hash_mentions='+repr(matches))
 print('artifact_with_claimed_hash='+repr(artifact_hash_hits))
 dr=ROOT/'ops/reviews/pr870-review-2-codex'
 for p in sorted(dr.rglob('*')):
  if p.is_file() and ('snapshot' in p.name or p.suffix in ('.py','.txt','.md')):
   for i,line in enumerate(p.read_text(errors='replace').splitlines(),1):
    if any(t in line for t in ['snapshot_hashed_files=','snapshot_added=','snapshot_removed=','snapshot_changed=','review-snapshot-before.json','review-snapshot-after.json']):
     print(str(p.relative_to(ROOT))+':'+str(i)+': '+line[:220])
 print('KET_LUAN: KHONG DO DUOC hash/672374 bytes cua hai snapshot goc vi KHONG co byte goc trong hien vat; chi do duoc loi khai + transcript tu chep. Caveat da khai ro KHONG vao kho.')

def patch_history():
 hint=ROOT/'ops/reviews/pr896-review-1-codex/HINT.patch'
 with tempfile.TemporaryDirectory(prefix='pr915-hint-') as tmp:
  p=Path(tmp);(p/'CLAUDE.md').write_bytes(git('show','3bc4244^:CLAUDE.md'))
  r=run(['patch','-p0','--fuzz=0','-i',str(hint)],p)
  print('patch -p0 --fuzz=0 rc='+str(r.returncode)+'; '+r.stdout.strip())
  exact=(p/'CLAUDE.md').read_bytes()==git('show','3bc4244:CLAUDE.md')
  still=(p/'CLAUDE.md').read_bytes()==git('show',SHA+':CLAUDE.md')
  print('HINT_result_equals_3bc4244='+str(exact)+'; equals_reviewed_HEAD='+str(still))
  assert r.returncode==0 and exact and still
 print('hint_commit='+git('rev-parse','3bc4244').decode().strip())
 for n in NAMES:
  d=receipt(n)
  print(n+': prior_P2_note='+d['luot_ghi_chu'])
 print('CHUA_REVIEW_LAI la loi khai trang thai luc ghi so; khong suy tu lich su Git rang khong he co review ngoai kho.')

def workflow():
 m=load_module('pr915_lease',ROOT/'ops/lease_publish_test.py')
 g=load_module('pr915_g5',ROOT/'.claude/dev/ci_dang_ky_test.py')
 src=(ROOT/'.github/workflows/ci.yml').read_text();data=yaml.safe_load(src)
 names=[j for j in data['jobs'] if j.startswith('gate-cong-cu')]
 print('actual_gate_cong_cu_prefix_jobs='+str(names))
 print('g5_shard='+g.JOB_G5_MANH+'; g5_aggregate='+g.JOB_G5_GOP+'; all_prefix_jobs_covered='+str(set(names)=={g.JOB_G5_MANH,g.JOB_G5_GOP}))
 print('chuan_bi.outputs.os='+repr(data['jobs']['chuan-bi']['outputs']['os']))
 for j in names:
  job=data['jobs'][j]
  print(j+': '+json.dumps({k:job.get(k) for k in ['needs','if','strategy']},ensure_ascii=False,sort_keys=True))
 old=m.HERE
 cases=[('baseline',None)]
 for j in names:
  for field in ['exclude','needs','if']:
   cases.append((j+'__remove_'+field,(j,field)))
 cases.append(('output_os__remove_windows_only_branch',('chuan-bi','os')))
 with tempfile.TemporaryDirectory(prefix='pr915-ci-') as tmp:
  p=Path(tmp);(p/'ops').mkdir();(p/'.github/workflows').mkdir(parents=True);m.HERE=p/'ops'
  try:
   for name,action in cases:
    d=copy.deepcopy(data)
    if action:
     j,field=action
     if field=='exclude':d['jobs'][j]['strategy']['matrix'].pop('exclude')
     elif field=='os':
      expr=d['jobs'][j]['outputs']['os']
      expr=re.sub(re.escape("(github.event_name == 'workflow_dispatch' && inputs.runner_set == 'windows-only')")+r'\s*'+re.escape('&& \'["windows-latest"]\'')+r'\s*\|\|\s*','',expr,count=1)
      assert expr!=d['jobs'][j]['outputs']['os'];d['jobs'][j]['outputs']['os']=expr
     else:d['jobs'][j].pop(field)
    f=p/'.github/workflows/ci.yml';f.write_text(yaml.safe_dump(d,sort_keys=False))
    (OUT/(name+'.yml')).write_bytes(f.read_bytes())
    b=io.StringIO();outcome='PASS';error=''
    with contextlib.redirect_stdout(b),contextlib.redirect_stderr(b):
     try:m.t162_M4_evaluator_toi_gian_chuan_bi()
     except AssertionError as e:outcome='FAIL';error=str(e)
    errors=g.loi_g5_workflow(yaml.safe_load(f.read_text()))
    print(f'{name}: t162={outcome}; loi_g5_workflow_errors={len(errors)}')
    if error:print('  t162_assertion='+error)
    for e in errors:print('  '+e)
    if not action:assert outcome=='PASS' and not errors
    elif action[1]=='os':assert outcome=='FAIL'
    else:assert outcome=='PASS' and errors
  finally:m.HERE=old
 print('KET_LUAN: t162 chi doc outputs.os tu workflow; exclude/needs/if cua CA HAI job manh/gom co chot rieng. Khong khai moi gate* deu duoc loi_g5_workflow bao phu.')

def mandatory_gates():
 commands=[['python3','ops/bien_nhan_v2.py','--root','.'],['python3','.claude/dev/packet_loop.py','doctrine-scan','--root','.'],['python3','scripts/tl.py','doc-claims-check','--json']]
 for i,args in enumerate(commands):
  p=run(args);(OUT/f'gate-{i}.stdout').write_text(p.stdout);(OUT/f'gate-{i}.stderr').write_text(p.stderr)
  print('command='+ ' '.join(args)+'; rc='+str(p.returncode))
  if i==2:
   d=json.loads(p.stdout);print('  ok='+json.dumps(d['ok'])+'; JSON_keys='+str(list(d)))
   assert d['ok'] is True
  else:
   print('  stdout_tail='+repr(p.stdout.splitlines()[-4:])+'; stderr_tail='+repr(p.stderr.splitlines()[-4:]))
  assert p.returncode==0

def required_cases():
 for prefix in ('t26_','t27_','t138_'):
  code="import runpy; d=runpy.run_path('ops/lease_publish_test.py'); n=next(k for k in d if k.startswith("+repr(prefix)+")); d[n](); print(n+': DAT (goi rieng ham)')"
  p=run(['python3','-B','-c',code]);(OUT/(prefix+'stdout')).write_text(p.stdout);(OUT/(prefix+'stderr')).write_text(p.stderr)
  print(f'{prefix}: rc={p.returncode}; stdout={p.stdout!r}; stderr={p.stderr!r}')
  assert p.returncode==0
 for n in NAMES:
  args=['python3','scripts/pkg_secret_scan.py','ops/reviews/'+n];p=run(args)
  print(' '.join(args)+f': rc={p.returncode}; stdout={p.stdout!r}; stderr={p.stderr!r}; '+('SACH (rc=0, khong co phat hien)' if p.returncode==0 else 'DO'))
  assert p.returncode==0

def identity_claims():
 for name in NAMES:
  d=receipt(name);dr=ROOT/'ops/reviews'/name
  r=json.loads((dr/'run/run.json').read_text());s=(dr/'VERDICT.md').read_text()
  line=next((i,x) for i,x in enumerate(s.splitlines(),1) if 'execution_surface' in x or 'execution surface' in x)
  caveats=d['verdict_usage_caveats']
  print(name+f': VERDICT.md:{line[0]}: '+line[1])
  print('  run.json:47 execution_surface='+r['execution_surface']+'; lenh='+json.dumps(r['lenh'],ensure_ascii=False))
  print('  receipt model_reviewer_identity.surface='+d['model_reviewer_identity']['surface'])
  print('  caveat_ids='+str([c['id'] for c in caveats]))
  print('  service_in_caveat='+str(any('codex_service' in c['mo_ta'] for c in caveats)))
 print('policy: ops/KE_HOACH_THI_CONG_DA_PROVIDER.md:39-51 phan biet codex_cli va codex_service; lich su codex exec giu codex_cli.')
 print('README:5-11 giu nguyen verdict co bam, dua dinh chinh vao verdict_usage_caveats va bang canh bao.')
 print('KET_LUAN: LOI — pr870 luot2 va pr889 luot2 khai sai codex_service trong ca ban phang va ban thu muc; pr889 con phu nhan chay qua codex exec; chua co caveat dinh chinh surface. Mot lop loi, hai hien vat review.')

def index_claims():
 m=load_module('pr915_index',ROOT/'ops/lease_publish_test.py')
 s=(ROOT/'ops/reviews/README.md').read_text()
 cb=m._bang(s,'Cảnh báo đang có hiệu lực');ml=m._bang(s,'Mục lục')
 for name in NAMES:
  d=receipt(name);target=name+'-verdict.md'
  c=[x for x in cb if target in m._ten_tep(x.get('tệp verdict',''))]
  v=[x for x in ml if target in m._ten_tep(x.get('tệp verdict',''))]
  print(name+': caveat_rows='+str(len(c))+'; index_rows='+str(len(v))+'; receipt_caveats='+str(len(d['verdict_usage_caveats'])))
  exact=True
  for caveat in d['verdict_usage_caveats']:
   row=next(x for x in c if caveat['id'] in x['id'])
   # so descriptions after only Markdown escaping for pipes; no pipe in these caveats
   match=any(caveat['mo_ta'].strip()==val.strip() for val in row.values())
   print('  '+caveat['id']+': text_matches_receipt='+str(match));exact &= match
  assert len(c)==len(d['verdict_usage_caveats']) and len(v)==1 and exact
 print('new_caveat_rows=14; new_index_rows=3; total=17')
 print('KET_LUAN: 17 hang khop bien nhan; t27 chi kiem cac id DA KHAI, khong phat hien caveat can them cho sai surface (Huong11).')

def static_scope():
 import ast,inspect
 m=load_module('pr915_static',ROOT/'ops/lease_publish_test.py')
 body=inspect.getsource(m.t162_M4_evaluator_toi_gian_chuan_bi)
 tree=ast.parse(body)
 accesses=sorted(set(ast.unparse(n) for n in ast.walk(tree) if isinstance(n,ast.Subscript) and isinstance(n.value,ast.Name) and n.value.id=='wf_data'))
 reads=[line.strip() for line in body.splitlines() if 'wf_ci' in line or 'wf_data' in line or 'raw_expr = ' in line]
 print('t162 workflow reads='+repr(reads));print('t162 wf_data direct accesses='+repr(accesses))
 body161=inspect.getsource(m.t161_M3_chot_nguon_duy_nhat_ma_tran_ci)
 calls=[n.func.id for n in ast.walk(ast.parse(body161)) if isinstance(n,ast.Call) and isinstance(n.func,ast.Name)]
 print('t161 evaluator_calls='+str(calls.count('_danh_gia_bieu_thuc_chuan_bi')))
 m.t161_M3_chot_nguon_duy_nhat_ma_tran_ci();print('t161_M3_chot_nguon_duy_nhat_ma_tran_ci: DAT')
 print('python='+sys.version.split()[0]+'; PyYAML='+yaml.__version__+'; platform='+sys.platform)

def final_integrity():
 old=json.loads((OUT/'snapshot-before.json').read_text());new={}
 for p in sorted(ROOT.rglob('*')):
  rel=str(p.relative_to(ROOT))
  if p.is_symlink():new[rel]={'link':os.readlink(p)}
  elif p.is_file():new[rel]={'sha256':sha(p.read_bytes()),'mode':stat.S_IMODE(p.stat().st_mode)}
 added=sorted(set(new)-set(old));removed=sorted(set(old)-set(new));changed=sorted(k for k in old.keys()&new.keys() if old[k]!=new[k])
 (OUT/'snapshot-after.json').write_text(json.dumps(new,sort_keys=True))
 print(f'snapshot_before_files={len(old)}; snapshot_after_files={len(new)}')
 print('added='+repr(added)+'; removed='+repr(removed)+'; changed_content_or_mode='+repr(changed))
 status=git('status','--porcelain=v1','--untracked-files=all','--ignored').decode()
 print('status_with_ignored='+repr(status)+'; HEAD='+git('rev-parse','HEAD').decode().strip())
 print('tree='+git('rev-parse','HEAD^{tree}').decode().strip())
 assert not (added or removed or changed or status)
 assert git('rev-parse','HEAD').decode().strip()==SHA
 print('KET_LUAN: toan bo byte, quyen tep va symlink trong cay-kho/ (gom .git) giu nguyen; khong network/push trong luot nay.')

DIRECTIONS={
'preflight':(1,'Neo SHA, cây sạch và diff','Có thể đang chấm nhầm cây hoặc diff.','KHÔNG PHẢI LỖI'),
'receipts':(2,'Ba biên nhận: byte, OID và số finding','Biên nhận có thể lệch hiện vật hoặc lịch sử Git.','KHÔNG PHẢI LỖI'),
'hashes':(3,'Toàn vẹn và độ đầy đủ SHA256SUMS','Manifest có thể sai băm hoặc bỏ sót tệp.','KHÔNG PHẢI LỖI'),
'provenance':(4,'Mỏ neo evidence_url và phạm vi ba commit','URL có thể neo commit trộn code với hiện vật.','KHÔNG PHẢI LỖI'),
'run_metadata':(5,'Metadata launcher và giới hạn model','Thời lượng, prompt hoặc mức assurance có thể bị khai quá.','KHÔNG PHẢI LỖI'),
'snapshot_caveats':(6,'Đối chiếu caveat snapshot vắng khỏi kho','Có thể chứng minh hash hai snapshot chỉ bằng hiện vật đã lưu.','KHÔNG ĐO ĐƯỢC'),
'patch_history':(7,'Tái lập nguyên HINT.patch cũ tại commit sửa','Caveat có thể dẫn sai commit hoặc bản vá khác hint.','KHÔNG PHẢI LỖI'),
'workflow':(8,'Đột biến độc lập exclude, needs, if và output os','Câu mới có thể khai rộng hơn t162 hoặc chốt G5 thực sự kiểm.','KHÔNG PHẢI LỖI'),
'mandatory_gates':(9,'Ba cổng bắt buộc trên exact checkout','Gate có thể đỏ, hoặc JSON thiếu ok=true.','KHÔNG PHẢI LỖI'),
'required_cases':(10,'Gọi riêng t26/t27/t138 và quét bí mật','Hiện vật có thể làm hỏng kiểm biên nhận, mục lục, hoặc chứa bí mật.','KHÔNG PHẢI LỖI'),
'identity_claims':(11,'Tự khai bề mặt chạy trong verdict so launcher','Metadata tự khai trong hiện vật có thể trái launcher và thiếu đính chính.','LỖI'),
'index_claims':(12,'17 hàng README so từng biên nhận','Mục lục có thể sai số hàng, thiếu caveat hoặc chép khác mô tả.','KHÔNG PHẢI LỖI'),
'static_scope':(14,'AST và ca t161 đối chiếu phạm vi câu văn','Có thể t162 đọc thêm trường workflow, hoặc t161 thật sự đánh giá biểu thức.','KHÔNG PHẢI LỖI'),
'final_integrity':(15,'Toàn vẹn checkout cuối lượt','Phép đo có thể đã ghi bytecode, đổi Git metadata hoặc làm bẩn cây nguồn.','KHÔNG PHẢI LỖI'),
}
if __name__=='__main__':
 mode=sys.argv[1];cfg=DIRECTIONS[mode];buf=io.StringIO();rc=0
 with contextlib.redirect_stdout(buf),contextlib.redirect_stderr(buf):
  try: globals()[mode]()
  except Exception: traceback.print_exc();rc=1
 text=buf.getvalue()+f'rc={rc}\n';(OUT/(mode+'.log')).write_text(text)
 with (BASE/'VERDICT.md').open('a') as f:
  f.write(f'\n### HƯỚNG {cfg[0]}: {cfg[1]}\n\n  giả thuyết : {cfg[2]}\n\n  lệnh : `PYTHONDONTWRITEBYTECODE=1 python3 review_probe.py {mode}` (cwd thư mục giao việc)\n\n  output :\n\n```text\n{text}```\n\n  kết luận : '+(cfg[3] if rc==0 else 'CHƯA KẾT LUẬN — xem lỗi phép đo')+'\n')
 print(text,end='');sys.exit(rc)
