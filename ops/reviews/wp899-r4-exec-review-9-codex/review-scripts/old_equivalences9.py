import concurrent.futures,json,pathlib,subprocess,sys
R=pathlib.Path(__file__).resolve().parent
def one(x):
 cmd=[sys.executable,'-B',str(R/'closed8.py'),'child',x['source'],x['function']];p=subprocess.run(cmd,capture_output=True)
 x=x|{'command':cmd,'rc':p.returncode,'result':json.loads(p.stdout),'stderr':p.stderr.decode()};return x
with concurrent.futures.ThreadPoolExecutor(3) as ex:rows=list(ex.map(one,json.loads((R/'old-equivalences9-selection.json').read_text())))
(R/'old-equivalences9-results.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2));print([(x['id'],len(x['result']['cases']),all(c[1]==0 for c in x['result']['cases'])) for x in rows]);assert all(x['rc']==0 and len(x['result']['cases'])==52 and all(c[1]==0 for c in x['result']['cases']) for x in rows)
