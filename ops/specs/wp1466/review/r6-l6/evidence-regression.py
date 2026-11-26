from pathlib import Path
import os,sys,subprocess,json,shutil,re,concurrent.futures,datetime
O=Path(__file__).resolve().parent; S=O.parent/'cay-kho/ops/specs/wp1466'; P=O/'prototype'
env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',TMPDIR=str(O/'tmp'),GIT_CONFIG_COUNT='1',GIT_CONFIG_KEY_0='commit.gpgsign',GIT_CONFIG_VALUE_0='false')
for name in ['chay5.py','probes_r5.py','thu_pv5.py','khoa_tu_tinh.py']:
 shutil.copyfile(S/'nguyen-mau-r5/sc'/name,O/'sc'/name)
spec=(S.parent/'wp1466.md').read_bytes()
for label,name in [('do-pham-vi','do_pham_vi.py'),('so-dang-ky','so_dang_ky.py')]:
 b=re.search(rb'~~~ '+label.encode()+rb'\n(.*?)\n~~~',spec,re.S).group(1)+b'\n'
 assert b==(S/'nguyen-mau-r5/sc'/name).read_bytes()
 (O/'sc'/name).write_bytes(b)
(O/'n8').mkdir(exist_ok=True)
(O/'cay').symlink_to(P,target_is_directory=True)
for name in ['packet_loop.py','packet_loop_test.py']: shutil.copyfile(O/'base/.claude/dev'/name,O/'n8'/('nen-'+name))
def run(name,args,cwd=None):
 t=datetime.datetime.now(datetime.timezone.utc).isoformat()
 with (O/(name+'.log')).open('w') as f: r=subprocess.run([sys.executable,'-B',*map(str,args)],stdout=f,stderr=subprocess.STDOUT,env=env,cwd=cwd)
 print(name,'rc',r.returncode,flush=True)
 return {'name':name,'rc':r.returncode,'utc':t,'command':[sys.executable,'-B',*map(str,args)]}
results=[run('locks',[O/'sc/khoa_tu_tinh.py',P/'docs/PROTOCOL_DA_PHIEN.md','--json',O/'locks.json'])]
jobs=[('bytes',[O/'sc/probes_r5.py',P,O/'locks.json',O/'tmp/bytes']),('n8-ma',[O/'sc/thu_pv5.py',O,'ma','2']),('n8-test',[O/'sc/thu_pv5.py',O,'test','2']),('registry',[O/'sc/so_dang_ky.py',O/'base',P])]
jobs += [(x,[O/'sc/chay5.py',P,O/'tmp/regression',x]) for x in ['ca','adr','moi','cu']]
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
 for r in pool.map(lambda x:run(*x),jobs):
  results.append(r);(O/'regression-results.json').write_text(json.dumps(results,indent=2))
for name in ['base','prototype','master']:
 for gate in ['doctrine-scan','adr-song']:
  results.append(run(name+'-'+gate,[O/name/'.claude/dev/packet_loop.py',gate,'--root',O/name],cwd=O/name))
(O/'regression-results.json').write_text(json.dumps(results,indent=2))
