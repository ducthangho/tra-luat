from common import *
import shutil,base64
V=Path('/workspace/scratch/wp1296-review1-H2');H='15ad82f56924a0ccc99833ec73eec078ce00b726'
assert not (W/'review1-invocation.json').exists()
assert (W/'AUX2-gates-receipt.json').exists() and (W/'AUX2-gates-final.txt').exists()
print('Read AUX2 receipt and require explicit positive gate audit approval before running this script.',flush=True)
bind=json.loads((W/'active-binding.json').read_text());a=json.loads((W/'review1-publication-binding.json').read_text());assert a['issue_readback_exact'] and sha(W/'review1-prompt.md')==a['prompt_sha256']
assert git('rev-parse','HEAD',repo=R)==git('rev-parse','HEAD',repo=V)==H and not git('status','--porcelain',repo=R) and not git('status','--porcelain',repo=V)
assert not (V/'.git/objects/info/alternates').exists()
subprocess.run([GIT,'-C',str(V),'fetch',str(P),'ops/wp1296-spec:refs/metadata/wp1296-spec'],env=env,check=True,capture_output=True)
assert git('ls-remote','origin','refs/heads/master').split()[0]==B
sys.path.insert(0,str(V/'.claude/dev'));launcher=load_module('launch1296review1',V/'.claude/dev/launcher.py')
for name,repo in [('source',R),('review',V)]:
 snap=launcher._chup_an_toan(repo,None);assert snap;(W/('review1-'+name+'-snapshot-before.txt')).write_bytes(snap[1])
t=datetime.datetime.now(datetime.timezone.utc);deadline=t+datetime.timedelta(minutes=60);assert deadline<datetime.datetime.fromisoformat(bind['until'].replace('Z','+00:00'))
b=json.loads((W/'live-budget.json').read_text());assert b['shared_used']==2 and b['formal_used']==0 and b['author_used']==2 and b['push_used']==0
b['shared_used']=3;b['shared_calls'].append({'n':3,'purpose':'Fresh independent CodexCLI xhigh formalreview1 wholeB..H2 spec+security','state':'reserved_before_dispatch','at':t.isoformat(),'deadline':deadline.isoformat(),'head':H});save(W/'live-budget.json',b)
childenv=env.copy()
for k in list(childenv):
 if k.startswith('TL_') or k in ['CODEX_AUTH_JSON','GITHUB_PAT','GH_TOKEN','GITHUB_TOKEN','CLAUDE_CODE_OAUTH_TOKEN','ANTHROPIC_API_KEY','OPENAI_API_KEY','PROXIMA_API_KEY']:childenv.pop(k,None)
childenv.update(PYTHONIOENCODING='utf-8',PYTHONPYCACHEPREFIX=str(W/'review1-pycache'))
cmd=[sys.executable,'-B',str(V/'.claude/dev/launcher.py'),'run','--workspace',str(V),'--expected-repo','ducthangho/tra-luat','--expected-head',H,'--expected-ref','review/wp1296-H2','--require-clean','--prompt-file',str(W/'review1-prompt.md'),'--expected-prompt-sha256',a['prompt_sha256'],'--deadline-utc',deadline.isoformat(),'--run-root',str(W/'review1-runs'),'--name','wp1296-r3-H2-review1-xhigh-call3','--giu-ban-chup','--chup-workspace','--json','--','/opt/codex/bin/codex','exec','--ephemeral','--sandbox','read-only','--model','gpt-6.1-sol','-c','model_reasoning_effort="xhigh"','-c','approval_policy="never"','--cd',str(V),'--json','--output-last-message',str(W/'review1-verdict.md'),'Read {PROMPT_FILE} fully and perform assigned fresh independent entire B..H2 sensitive review. Return original two-axis verdict and final matching KET_LUAN marker. No source edits, network, agents/models, Windows operations, or Git mutations.']
save(W/'review1-invocation.json',{'command':cmd,'started_at':t.isoformat(),'deadline':deadline.isoformat(),'requested_model':'gpt-6.1-sol','requested_effort':'xhigh','actual_model_effort':'unknown_until_telemetry','original_product_executor_effort':'high','assurance':'same_provider_only_sensitivepromotionHOLD'})
with (W/'review1-launcher.log').open('wb') as out:q=subprocess.run(cmd,env=childenv,cwd=V,stdout=out,stderr=subprocess.STDOUT)
result={'launcher_rc':q.returncode,'ended':now(),'head':H,'post_snapshots':{}}
for name,repo in [('source',R),('review',V)]:
 snap=launcher._chup_an_toan(repo,None);assert snap;(W/('review1-'+name+'-snapshot-after.txt')).write_bytes(snap[1]);result['post_snapshots'][name]={'sha256':hashlib.sha256(snap[1]).hexdigest(),'same_as_before':snap[1]==(W/('review1-'+name+'-snapshot-before.txt')).read_bytes()}
save(W/'review1-controller-result.json',result);b=json.loads((W/'live-budget.json').read_text());b['shared_calls'][-1]['state']='terminal_pending_valid_delivery';save(W/'live-budget.json',b);print(json.dumps(result),flush=True)
