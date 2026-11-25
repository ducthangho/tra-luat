import concurrent.futures,json,os,subprocess,sys,time
from review_measure import W,R,C,save,sha
D=R/'ops/reviews/wp1236-r10-soan'
P={x['id']:x for x in map(json.loads,(D/'pilot_c2d606b_kq.jsonl').read_text().splitlines())};K=list(map(json.loads,(W/'pilot_subset_kq.jsonl').read_text().splitlines()));M={x['id']:x for x in map(json.loads,(W/'pilot_subset.jsonl').read_text().splitlines())}
summary=json.loads((W/'measurement_summary.json').read_text());surv=summary['p2_survivors']+summary['p3_survivors'];eq=summary['equivalent']
fields=('sha256','giet','hong','rc');diff=[{'id':x['id'],'fields':[f for f in fields if x[f]!=P[x['id']][f]]} for x in K if any(x[f]!=P[x['id']][f] for f in fields)]
# Native target runs without YAML cache: replay only already supplied mutants and the original suite.
N=W/'native_targets';N.mkdir(exist_ok=True)
def one(pair):
 i,x=pair;p=N/(str(i)+'.py');p.write_text(M[x['id']]['src']);case=x['giet'][0];cmd=[sys.executable,'-B',str(C/'ops/gate_output_doi_chieu_test.py'),'--mot-ca',case]
 r=subprocess.run(cmd,env=dict(os.environ,GATE_OUTPUT_DOI_CHIEU_MA=str(p),PYTHONDONTWRITEBYTECODE='1',TMPDIR=str(W/'tmp')),capture_output=True,timeout=300)
 return {'id':x['id'],'case':case,'command':cmd,'module_sha256':sha(p.read_bytes()),'rc':r.returncode,'stdout':r.stdout.decode(),'stderr':r.stderr.decode(),'exact_signal':r.returncode==3 and r.stdout.decode().startswith('DO:'+case+':')}
t=time.monotonic()
with concurrent.futures.ThreadPoolExecutor(4) as ex:out=list(ex.map(one,enumerate(x for x in K if x['giet'])))
save('native_target_replays.json',out)
k={x['id']:x for x in K}
result={'subset':len(K),'diff_from_pilot':diff,'non_equivalent_25_survive':all('kho:'+i in k and not k['kho:'+i]['giet'] and not k['kho:'+i]['hong'] and k['kho:'+i]['rc']==0 for i in surv),'equivalent_9_survive':all('kho:'+i in k and not k['kho:'+i]['giet'] and not k['kho:'+i]['hong'] for i in eq),'native_kills':len(out),'native_exact_signals':sum(x['exact_signal'] for x in out),'native_seconds':time.monotonic()-t}
save('pilot_comparison.json',result);print('PILOT_COMPARISON_COMPLETE',json.dumps(result,ensure_ascii=False),flush=True)
