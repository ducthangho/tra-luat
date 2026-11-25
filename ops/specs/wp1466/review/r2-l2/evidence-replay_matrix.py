"""Replay author-supplied fixtures, remeasure outputs, and separately apply §8.4 assertions.
No new path/hostile-string fixtures: source fixtures are exactly those provided by author.
"""
from measure import *
dest=OUT/'matrix';dest.mkdir(exist_ok=True)
(dest/'k').mkdir(exist_ok=True)
neo=[d.split(' | ',3) for d in blocks['neo'].splitlines()]
(dest/'k/neo').write_text('\n'.join(' | '.join([n,k,t]) for n,k,h,t in neo)+'\n')
source=(REPO/'ops/specs/wp1466/nguyen-mau-r2/ma_tran.py').read_text()
source=source.replace('here = pathlib.Path(__file__).parent.resolve(); cay = here / "cay";', 'here = pathlib.Path(__file__).parent.resolve(); cay = here.parent / "prototype";')
source=source.replace('def chay(script, ten):','ALL_RESULTS = {}\ndef chay(script, ten):')
source=source.replace('    return f"{r.returncode}', '    ALL_RESULTS.setdefault(str(script), {})[ten] = {"rc": r.returncode, "stdout": r.stdout, "stderr": r.stderr}\n    return f"{r.returncode}')
source+='\njson.dump(ALL_RESULTS, open(here / "raw-results.json", "w"), ensure_ascii=False)\n'
path=dest/'replay_author.py';path.write_text(source)
rc=subprocess.run([sys.executable,'-B',str(path)],env=os.environ).returncode
assert rc==0,rc
results=json.loads((dest/'raw-results.json').read_text())
positive={'nguyen_ven','ngat_dong_lai_van_xanh','bang_them_khoang_trang_van_xanh','lien_ket_noi_bo_van_xanh'}
unknown={'lien_ket_ra_ngoai','rao_khong_dong','dong_html'}
def assertion(case,r):
    if case in positive:return r['rc']==0 and 'doctrine-scan: sạch' in r['stdout']
    if r['rc']!=9:return False
    if case in unknown:return 'KHÔNG ĐO ĐƯỢC' in r['stderr']
    labels=re.findall(r'neo (N\d+)',r['stderr'])
    if case.startswith('xoa_neo_'):return labels==[case.removeprefix('xoa_neo_')]
    if case.startswith('bang_') or case=='hai_tieu_muc':return 'bảng bất biến' in r['stderr']
    return bool(labels)
counts={}
for script,rs in results.items():
    name=pathlib.Path(script).parent.name
    failed=[c for c,r in rs.items() if not assertion(c,r)]
    counts[name]=failed
    print('ASSERTION_MEASURE',name,len(failed),failed,flush=True)
(dest/'assertion-results.json').write_text(json.dumps(counts,ensure_ascii=False,indent=2))
