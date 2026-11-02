import collections
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import unicodedata
from datetime import datetime
import yaml
S=Path(__file__).resolve().parent
R=S/'cay-kho'
P=R/'ops/land/pr1047-wp1045-provenance'
L=R/'ops/land/pr1047-wp1045-land-evidence.yaml'
D=yaml.safe_load(L.read_text())
BASE='afc82f6d7447eb76fc8adbe46c1be90be88d331f'
HEAD='3534a6ec9b343cfa484142b14b7c7db7fd3b6f6e'
PREV='5dd347c67da680099e292acf02da7e363a0559bd'
def out(k,**v): print(json.dumps(dict(check=k,**v),ensure_ascii=False,default=str))
def sha(b): return hashlib.sha256(b).hexdigest()
def j(n): return json.loads((P/n).read_text())
def git(*args):
 p=subprocess.run(['git',*args],cwd=R,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'),capture_output=True)
 if p.returncode: raise AssertionError((args,p.returncode,p.stderr.decode()))
 return p.stdout

def closure():
 pr=j('readback-pr-1047.json'); c=j('readback-comment-6529094452.json')
 note=D['authorization_ghi_chu']; conditions=D['trang_thai_packet']['landed_dieu_kien']
 assert 'uy quyen land la hanh dong merge' not in note
 assert 'Readback chi chung minh THAO TAC merge (merged_by), khong phai duyet land' in note
 assert 'chua co nguon duyet land ben neo exact SHA 2014602' in note
 assert '(5) uy quyen land neo SHA: CHUA DAT' in conditions and 'chu kho ghi duyet ben neo 2014602' in conditions
 assert D['trang_thai_packet']['landed'] is False
 out('authorization',result='CLOSED at original location',claim=note,conditions=conditions,merged=pr['merged'],merged_by=pr['merged_by']['login'],head_sha=pr['head']['sha'],comment_author=c['user']['login'],comment_app=c['performed_via_github_app']['slug'],comment_body=c['body'],identity_and_exact_sha_authorization='KHÔNG ĐO ĐƯỢC')
 jobs=j('readback-jobs-41099486628.json')['jobs']
 gates=[x for x in jobs if x['name'].startswith('gate')]
 executed=[x for x in gates if x['conclusion']!='skipped']
 skipped=[x for x in gates if x['conclusion']=='skipped']
 assert len(executed)==14 and all(x['labels']==['windows-latest'] and x['runner_id'] for x in executed)
 assert len(skipped)==1 and skipped[0]['id']==124215501550 and skipped[0]['labels']==[] and skipped[0]['runner_id'] is None
 counts=collections.Counter(x['conclusion'] for x in jobs)
 assert counts=={'success':15,'skipped':1}
 claim=D['pre_merge_checks'][1]['ghi_chu']
 assert '14 job gate* DA CHAY deu nhan windows-latest' in claim and 'gate-cong-cu-gop skipped, labels rong, runner_id null' in claim
 out('windows_labels',result='CLOSED',total=len(jobs),counts=counts,executed_gates=len(executed),skipped=[{k:x[k] for k in ['id','name','conclusion','labels','runner_id']} for x in skipped],preparation=[{k:x[k] for k in ['name','labels','conclusion']} for x in jobs if x['name']=='chuan-bi'],claim=claim)

def sources():
 for f in sorted(P.glob('readback-run-*.json')):
  run=json.loads(f.read_text()); rid=run['id']; item={k:run.get(k) for k in ['id','name','head_sha','head_branch','path','event','run_attempt','status','conclusion','created_at','updated_at']}
  jf=P/f'readback-jobs-{rid}.json'
  if jf.exists():
   data=json.loads(jf.read_text()); jobs=data['jobs']
   assert data['total_count']==len(jobs)==len({x['id'] for x in jobs})
   assert all(x['run_id']==rid and x['head_sha']==run['head_sha'] and x['run_attempt']==run['run_attempt'] for x in jobs)
   item.update(job_count=len(jobs),conclusions=dict(collections.Counter(x['conclusion'] for x in jobs)),labels=dict(collections.Counter(','.join(x['labels']) or 'NO_LABEL' for x in jobs)),runner_nonzero=sum(bool(x.get('runner_id')) for x in jobs))
   if rid==41099486628:
    selected=[x for x in jobs if x['name'] in ['gate-cong-cu (windows-latest, 0)','gate-packet-loop (windows-latest)']]
    assert len(selected)==2
    for x in selected:
     steps=[t for t in x['steps'] if 'shellcheck' in t['name'] or t['name'].startswith('G5 ')]
     assert len(steps)==2 and all(t['status']=='completed' and t['conclusion']=='success' for t in steps)
     out('windows_steps',job=x['name'],steps=steps)
  else: item.update(jobs='KHÔNG ĐO ĐƯỢC; no jobs readback')
  out('run',**item)
 for name in ['readback-runs-b2d5f06.json','readback-runs-b2d5f06-sau.json']:
  data=j(name); runs=data['workflow_runs']; assert data['total_count']==len(runs)==2
  out('run_snapshot',source=name,runs=[{k:r[k] for k in ['id','head_sha','event','status','conclusion','updated_at']} for r in runs])
 pr=j('readback-pr-1047.json')
 assert pr['head']['sha']==D['authorized_head_sha'] and pr['merge_commit_sha']==D['merge_commit']
 out('pr',merged=pr['merged'],merged_by=pr['merged_by']['login'],merged_at=pr['merged_at'],head=pr['head']['sha'],base=pr['base']['sha'],merge=pr['merge_commit_sha'],additions=pr['additions'],deletions=pr['deletions'],changed_files=pr['changed_files'])
 c=j('readback-comment-6531582115.json')
 state=json.loads(re.search(r'codex-review-state:v1 (\{.*?\}) -->',c['body']).group(1))
 out('connector',author=c['user']['login'],updated_at=c['updated_at'],state=state,trigger='Draft marked ready' in c['body'],land_claim=D['pre_merge_checks'][-1],land_condition=D['trang_thai_packet']['landed_dieu_kien'])
 a=(P/'ai-dang-giu-sau-rut-han/luc-do.txt').read_text()
 blocks=a.split('$ python3 ops/lease_publish.py ai-dang-giu ')[1:]
 assert len(blocks)==3
 for b in blocks:
  assert 'NGƯỜI_GIỮ 0: không có' in b and 'rc=0' in b
  assert 'HẾT_HẠN\twp1045-r1-g2-claude' in b and 'CÒN_HẠN · ĐÃ_BỊ_THAY_THẾ\twp1045-r1-g1-claude' in b
 out('lease_snapshot',header=a.splitlines()[:3],paths=[b.splitlines()[0] for b in blocks],zero_holders=len(blocks),history_remote_completeness='KHÔNG ĐO ĐƯỢC')
 out('land_state',landed=D['trang_thai_packet']['landed'],assurance=D['assurance_81'],review=D['review'])

def bytes_git():
 changes=git('diff','--name-only',BASE,HEAD).decode().splitlines()
 outside=[x for x in changes if not x.startswith(('ops/reviews/','ops/land/'))]
 assert len(changes)==51 and not outside
 assert git('rev-parse','HEAD').decode().strip()==HEAD
 patch=git('diff',BASE,HEAD); patch2=git('diff',PREV,HEAD)
 assert patch==(S/'DIFF.patch').read_bytes()
 assert patch2==(S/'DIFF-LUOT2.patch').read_bytes()
 out('scope',count=len(changes),outside=outside,delta_round2=git('diff','--name-only',PREV,HEAD).decode().splitlines(),DIFF_sha256=sha(patch),DIFF_LUOT2_sha256=sha(patch2),patches_match=True)
 manifests=[P/'SHA256SUMS']+list((R/'ops/reviews').glob('wp1045-g1-codex-luot[123]/SHA256SUMS'))
 for m in manifests:
  names=[]
  for row in m.read_text().splitlines():
   h,n=row.split(maxsplit=1); n=str(Path(n.lstrip('*'))); names.append(n)
   assert sha((m.parent/n).read_bytes())==h,(m,n)
  actual={p.relative_to(m.parent).as_posix() for p in m.parent.rglob('*') if p.is_file() and p!=m}
  assert set(names)==actual
  out('manifest',path=m.relative_to(R),items=len(names),result='PASS')
 for k in ['authorized_head_sha','merge_commit']:
  oid=D[k]; tree=D['authorized_head_tree' if k=='authorized_head_sha' else 'merge_commit_tree']
  assert git('rev-parse',oid+'^{tree}').decode().strip()==tree
 assert git('show','-s','--format=%P',D['merge_commit']).decode().split()==D['merge_commit_parents']
 diff1=git('diff','5e458f4','2014602'); diff2=git('diff','b2d5f06^1','b2d5f06')
 assert diff1==diff2 and sha(diff1)=='65b4fa2e33f4c39fec5d4a287d3b1c94decdcde532141d25ab0bd82b046a69d7'
 stat=git('diff','--numstat','b2d5f06^1','b2d5f06').decode()
 out('merge_git',diff_hash=sha(diff1),numstat=stat,trees=[D['authorized_head_tree'],D['merge_commit_tree']],parents=D['merge_commit_parents'])
 ref='origin/ops/wp1045-r1-g1-lease'
 spec=git('show',ref+':ops/specs/wp1045.md'); assert sha(spec)==D['spec']['sha256']
 originals=[('lease-wp1045-r1-g1.yaml.txt','4b4f37f','ops/leases/wp1045-r1-g1-claude.yaml'),('lease-wp1045-r1-g2.yaml.txt','4b4f37f','ops/leases/wp1045-r1-g2-claude.yaml'),('lease-wp1045-r1-g2-sau-rut-han-a430543.yaml.txt','a430543','ops/leases/wp1045-r1-g2-claude.yaml')]
 for n,commit,p in originals: assert (P/n).read_bytes()==git('show',commit+':'+p)
 old=yaml.safe_load((P/originals[1][0]).read_text()); new=yaml.safe_load((P/originals[2][0]).read_text()); g1=yaml.safe_load((P/originals[0][0]).read_text())
 assert old['spec_hash']==new['spec_hash']==g1['spec_hash']==sha(spec)
 assert git('show','a430543:ops/leases/wp1045-r1-g1-claude.yaml')==git('show','a430543^:ops/leases/wp1045-r1-g1-claude.yaml')
 assert g1['da_bi_thay_the']==old['lease_id'] and new['thay_the_cho']==[g1['lease_id']]
 ws=sorted(unicodedata.normalize('NFC',x).casefold() for x in D['lease']['write_set'])
 ws_hash=sha(json.dumps(ws,separators=(',',':'),ensure_ascii=False).encode()); assert ws_hash==D['lease']['write_set_hash']==new['write_set_hash']
 delta=(datetime.fromisoformat(new['lease_until'].replace('Z','+00:00'))-datetime.fromisoformat(new['lease_sua_lan_cuoi'].replace('Z','+00:00'))).total_seconds(); assert delta==1200
 out('leases_git',ref_head=git('rev-parse',ref).decode().strip(),snapshots_match=3,spec_sha256=sha(spec),write_set_hash=ws_hash,g1_unchanged=True,old_expiry=old['lease_until'],new_expiry=new['lease_until'],seconds_after_edit=delta,budget=new['budget'])

def receipts():
 # Round 2 must leave receipt/README/artifacts unchanged byte for byte.
 diff=git('diff','--name-only',PREV,HEAD,'--','ops/reviews').decode(); assert diff==''
 current=(R/'ops/reviews/README.md').read_text(); base=git('show',BASE+':ops/reviews/README.md').decode()
 it=iter(current.splitlines()); assert all(any(y==x for y in it) for x in base.splitlines())
 out('receipt_regression',round2_changed_review_paths=diff,base_README_lines_preserved_in_order=True)
 for i in range(1,4):
  root=R/f'ops/reviews/wp1045-g1-codex-luot{i}'; rcpt=yaml.safe_load((R/f'ops/reviews/wp1045-g1-codex-luot{i}-verdict.receipt.yaml').read_text())
  verdict=(root/'VERDICT.md').read_bytes(); run=json.loads((root/'run/run.json').read_text())
  assert verdict==(R/rcpt['verdict_path']).read_bytes()
  assert sha(verdict)==rcpt['verdict_sha256'] and len(verdict)==rcpt['verdict_bytes']
  source_files=[f for f in root.rglob('*') if f.is_file() and f.name!='SHA256SUMS']; assert len(source_files)==6
  for f in source_files:
   path=f'ops/handoff/wp1045-g1-claude/luot{i}/'+f.relative_to(root).as_posix()
   assert f.read_bytes()==git('show','4b4f37f:'+path)==git('show','origin/ops/wp1045-r1-g1-lease:'+path)
  for part in ['stdout','stderr']:
   raw=(root/f'run/{part}.log').read_bytes()
   assert len(raw)==run[part+'_byte'] and sha(raw)==run[part+'_sha256']
  assert sha((root/'PROMPT.md').read_bytes())==run['prompt_sha256']
  assert sha((root/'run/checkpoint.json').read_bytes())==run['checkpoint_sha256']
  s=verdict.decode(); found=re.findall(r'^- \[P([0-3])\]\s+([^:\n]+)',s,re.M)
  counts=[sum(int(n)==k for n,_ in found) for k in range(4)]
  assert counts==[rcpt['so_p'+str(k)] for k in range(4)]
  assert rcpt['reviewed_sha']==run['head'] and run['head'] in s.splitlines()[1]
  assert run['run_id']==rcpt['model_reviewer_identity']['session_run_id']
  git('merge-base','--is-ancestor',run['head'],'b2d5f06')
  anchor,path=rcpt['evidence_url'].split('/blob/')[1].split('/',1)
  assert git('show',anchor+':'+path)==verdict; git('merge-base','--is-ancestor',anchor,HEAD)
  assert len(run['model_phuc_vu'])==[25,42,43][i-1] and all(e['model']=='gpt-6-astra' for e in run['model_phuc_vu'])
  assert run['effort_phuc_vu']==['xhigh'] and run['sandbox_trang_thai']=='KHONG_DO_DUOC'
  assert run['ma_thoat']==0 and run['trang_thai']=='xong'
  duration=(datetime.fromisoformat(run['ket_thuc_utc'])-datetime.fromisoformat(run['bat_dau_utc'])).total_seconds()
  assert abs(duration-run['thoi_luong_giay'])<0.001
  rows=[line for line in current.splitlines() if line.startswith('|') and f'wp1045-g1-codex-luot{i}-verdict.md' in line]; assert len(rows)==4
  out('receipt',round=i,files_source_equal=len(source_files),reviewed_sha=run['head'],run_id=run['run_id'],verdict=s.splitlines()[0],counts=counts,bytes=len(verdict),sha256=sha(verdict),model_events=len(run['model_phuc_vu']),duration=run['thoi_luong_giay'],model_state=run['model_phuc_vu_trang_thai'],effort_state=run['effort_phuc_vu_trang_thai'],sandbox_state=run['sandbox_trang_thai'],README_rows=len(rows),caveat_ids=[c['id'] for c in rcpt['verdict_usage_caveats']])

def final_state():
 out('final_state',head=git('rev-parse','HEAD').decode().strip(),tree=git('rev-parse','HEAD^{tree}').decode().strip(),config_abbrev=git('config','--get','core.abbrev').decode().strip(),status=git('status','--porcelain=v1','--untracked-files=all','--ignored').decode(),diff=git('diff','--exit-code').decode(),index=git('diff','--cached','--exit-code').decode())

if __name__ == '__main__':
    for name in sys.argv[1:] or ['closure','sources','bytes_git','receipts']:
     globals()[name]()
     out('section_done',section=name,result='PASS')
