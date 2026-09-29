from pathlib import Path
import csv,json,re,subprocess,hashlib,importlib.util,sys,contextlib,io,datetime as dt
import yaml
R=Path(__file__).resolve().parents[1];T=R/'cay-kho';O=R/'do-review10';P=T/'ops/reviews/pr468-hoso-4-packet-review-6-codex';S=P/'nen-a1-a5'
sha=lambda b:hashlib.sha256(b).hexdigest()
def git(*a):return subprocess.check_output(['git','-C',str(T),*a])
G='ops/specs/GATE-TACH-JOB-CAT-CHI-PHI.md';L='ops/specs/LO-319-LINUX-BANG-CHUNG-XANH.md'
g=(T/G).read_text();l=(T/L).read_text();base_l=git('show','0bc6e56:'+L).decode()
report={'utc':dt.datetime.now(dt.timezone.utc).isoformat()}
nums=git('diff','--numstat','0bc6e56..HEAD');nr=[s.split('\t') for s in nums.decode().splitlines()]
report['diff']={'files':len(nr),'additions':sum(int(s[0]) for s in nr),'deletions':sum(int(s[1]) for s in nr),
    'patch_equal':git('diff','0bc6e56..HEAD')==(R/'diff-sau-luot9.patch').read_bytes(),'numstat_equal':nums==(R/'numstat-sau-luot9.txt').read_bytes(),'outside_ops':[s[2] for s in nr if not s[2].startswith('ops/')],
    'new_commits':int(git('rev-list','--count','0bc6e56..HEAD'))}
report['spec_anchors']=[]
for issueid,prefix in [(463,'gate-tach-job-cat-chi-phi-exec-1r4'),(464,'lo-319-linux-bang-chung-xanh-exec-1'),(465,'mutant-windows-subagent-ghi-detect-exec-1'),(466,'mutant-windows-nhanh-don-duoc-exec-1')]:
    issue=next((T/'ops/issues').glob(str(issueid)+'-*.md'));it=issue.read_text();frozen=re.search(r'@ `([0-9a-f]{40})`',it).group(1)
    lease=next((T/'ops/leases').glob(prefix+'-claude*.yaml*'));d=yaml.safe_load(lease.read_text());actual=sha((T/d['spec_path']).read_bytes());blob=sha(git('show',frozen+':'+d['spec_path']))
    report['spec_anchors'].append({'issue':issueid,'spec':d['spec_path'],'lease':str(lease.relative_to(T)),'revision':d['revision'],'actual':actual,'lease_hash':d['spec_hash'],'alias':d['spec_sha256'],'issue_blob_hash':blob,'commit':frozen,'issue_has_hash':actual in it,'all_equal':actual==d['spec_hash']==d['spec_sha256']==blob,'null_keys':[k for k,v in d.items() if v is None]})
report['grep_checks']={}
for name,pattern,path in [('lo_old','chưa được chọn\\|chưa chọn',L),('gate_old','còn đúng',G)]:
    p=subprocess.run(['grep','-c',pattern,str(T/path)],capture_output=True,text=True)
    report['grep_checks'][name]={'pattern':pattern,'rc':p.returncode,'stdout':p.stdout,'stderr':p.stderr}
ld=yaml.safe_load((T/'ops/leases/lo-319-linux-bang-chung-xanh-exec-1-claude-20260906.yaml.nhap').read_text());it=(T/'ops/issues/464-LO-319-LINUX-BANG-CHUNG-XANH.md').read_text();url='https://github.com/ducthangho/tra-luat/issues/464#issuecomment-5567158069'
def blocks(s):
    a=s.index('### Thiết kế H');b=s.index('### Ca đang khoá',a)
    return re.findall(r'```python\n(.*?)\n```',s[a:b],re.S)
report['h_decision']={'url_3_of_3':all(url in s for s in [l,it,(T/'ops/leases/lo-319-linux-bang-chung-xanh-exec-1-claude-20260906.yaml.nhap').read_text()]),
    'intro_selected':'CHỌN lựa chọn (1) — tiếp H' in l,'row_selected':'**chủ kho CHỌN 07-09-2026 — lựa chọn 1**' in l,
    'decision_selected':'lựa chọn (1), tiếp H trong write set hiện tại' in l,'issue_selected':'lựa chọn (1) — tiếp H' in it,
    'lease_selected':'CHỦ KHO ĐÃ CHỌN 07-09-2026' in ld['ly_do_cap'],'draft_null':[k for k,v in ld.items() if v is None],
    'conditions':[x for x in ['Đ1','Đ2','Đ3','Đ4','Đ5'] if re.search(r'^\| '+x+r' \|',l,re.M)],
    'h_python_blocks_unchanged':blocks(l)==blocks(base_l),'h_block_hashes':[sha(x.encode()) for x in blocks(l)],
    'deferred_execution':'thi công chưa bắt đầu, lease chưa cấp, Đ1–Đ5 còn ràng buộc' in l}
rows=list(csv.DictReader((S/'buoc.tsv').open(),delimiter='\t'));jobs=list(csv.DictReader((S/'job.tsv').open(),delimiter='\t'))
def data(h):return [{'step':s['step_name'],'platform':'windows' if 'windows' in s['job_name'] else 'ubuntu','conclusion':s['step_conclusion'],'number':int(s['step_number']),'job':'gate'} for s in rows if s['head7']==h]
def triples(rr):return {(s['step'],s['platform'],s['conclusion']) for s in rr}
def split(rr):
    out=[]
    for s in rr:
        job='gate-registry' if s['step'].startswith('test registry') else 'gate-packet-loop' if s['step']=='packet-loop selftest' else 'gate'
        out.append(dict(s,job=job))
        if 2<=s['number']<=10:
            for j in ['gate-registry','gate-packet-loop']:out.append(dict(s,job=j))
    return out
lease=yaml.safe_load((T/'ops/leases/gate-tach-job-cat-chi-phi-exec-1r4-claude-20260906.yaml').read_text());base=lease['start_from_sha'];baseyaml=git('show',base+':.github/workflows/ci.yml');yy=yaml.safe_load(baseyaml)
disp=data(base[:7]);changes=[]
for s in disp:
    for prefix,condition,target in [('release-verify strict (lane LAND',"github.ref == 'refs/heads/master'",'skipped'),('release-verify strict (lane WORKER',"github.ref != 'refs/heads/master'",'success')]:
        if s['step'].startswith(prefix):
            assert next(x for x in yy['jobs']['gate']['steps'] if x.get('name','').startswith(prefix))['if']==condition
            changes.append(dict(s,model_conclusion=target));s['conclusion']=target
def compare(rr):
    before=triples(rr);after=triples(split(rr));drop={s for s in after if s[0]!='bien-nhan v2 selftest'}
    return {'before':len(before),'after':len(after),'full_equal':before==after,'drop_receipt_equal':before==drop,'drop_missing':len(after-drop)}
pr_candidates=[j for j in jobs if j['event']=='pull_request' and 'ubuntu' in j['job_name'] and git('show',j['head7']+':.github/workflows/ci.yml')==baseyaml]
chosen=max(pr_candidates,key=lambda j:j['started_at']);pr=[s for s in data(chosen['head7']) if s['platform']=='ubuntu']
before=triples(data(base[:7]));after=triples(disp)
report['a2']={'model_only':True,'base':base,'dispatch':compare(disp),'pr':compare(pr),'pr_source':chosen,'wrong_lane':{'equal':before==after,'added':len(after-before),'removed':len(before-after)},'yaml_steps_old':len(yaml.safe_load(git('show','1b3caa1:.github/workflows/ci.yml'))['jobs']['gate']['steps']),'yaml_steps_base':len(yy['jobs']['gate']['steps']),
    'ordering_row':next(s for s in g.splitlines() if s.startswith('| số đo của GATE')),'lane_changes':changes}
# Replay existing stored bytes only: no test suite invocation, no new test text.
sp=importlib.util.spec_from_file_location('review10_registry',T/'.claude/dev/ci_dang_ky_test.py');C=importlib.util.module_from_spec(sp);sys.modules[sp.name]=C;sp.loader.exec_module(C)
H={'re':re}
for code in blocks(l):exec(code,H)
basefn=C.bang_chung_xanh;bm=C.MOI.copy();bwin=C.MOI_WINDOWS.copy()
hm={p:(span,H['TONG'][p]) for p,span in bm.items()};hwin={p:tuple((span,H['TONG_WINDOWS'][p][i]) for i,span in enumerate(spans)) for p,spans in bwin.items()}
def replay(p,text,rc=0,base=False):
    C.bang_chung_xanh=basefn if base else H['bang_chung_xanh'];C.MOI_WINDOWS=bwin if base else hwin
    try:
        with contextlib.redirect_stdout(io.StringIO()):return C.chay_moi(moi={p:bm[p] if base else hm[p]},cach_ly={},chay_mot=lambda _:(rc,text),doc_moi_truong=lambda:C.MOI_TRUONG_CI,doc_trong_ci=lambda:True,doc_nen_windows=lambda:False)
    except Exception as e:return type(e).__name__
report['d2_replay']=[]
real=json.loads((P/'real-results.json').read_text());rerun=json.loads((P/'nhanh-rerun.json').read_text());that=json.loads((P/'d2-that-results.json').read_text())
for r in real:
    p=r['path'];src=P/r['output'];meta=r
    if p==rerun['path']:src=P/'outputs/nhanh_don_duoc_test.rerun.stdout';meta=rerun
    if p in that['ket_qua']:meta=that['ket_qua'][p];src=P/'outputs-that'/src.name
    raw=src.read_bytes()
    report['d2_replay'].append({'path':p,'source':str(src.relative_to(T)),'recorded_rc':meta['rc'],'bytes':len(raw),'sha256':sha(raw),'hash_matches':meta.get('sha256',sha(raw))==sha(raw),'H':replay(p,raw.decode(),meta['rc']),'BASE':replay(p,raw.decode(),meta['rc'],True)})
saved=json.loads((T/'ops/reviews/pr468-hoso-4-packet-review-8-codex/replay-h.json').read_text())
report['d9_replay']={k:{'source_sha256':sha(v['text'].encode()),'path':v['path'],'H':replay(v['path'],v['text']),'BASE':replay(v['path'],v['text'],base=True)} for k,v in saved['d9'].items()}
report['runtime_unchanged']=git('diff','0bc6e56..HEAD','--','.claude','.github','scripts')==b''
(O/'contracts.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:report[k] for k in ['diff','spec_anchors','grep_checks','h_decision','a2','d9_replay','runtime_unchanged']},ensure_ascii=False,indent=2))
print('D2 recorded-rc,H,BASE:',[(x['recorded_rc'],x['H'],x['BASE'],x['hash_matches']) for x in report['d2_replay']])
