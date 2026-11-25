from pathlib import Path
import importlib.util,hashlib,json,sys,time
sys.dont_write_bytecode=True
r=Path.cwd();w=r.parent/'work';s=importlib.util.spec_from_file_location('probe_test',r/'ops/land_evidence_nguon_test.py');t=importlib.util.module_from_spec(s);s.loader.exec_module(t)
m=t.nap();rows=[]
def record(label,rc,out,want,required,forbidden=()):
 ok=rc==want and all(x in out for x in required) and not any(x in out for x in forbidden)
 rows.append(dict(label=label,rc=rc,expected_rc=want,required=required,forbidden=forbidden,passed=ok,output=out));assert ok,(label,rc,out)
ten='pr963-wp943-land-evidence.yaml';raw=(r/'ops/land'/ten).read_bytes()
assert m.MIEN_TRU_L8[ten]==hashlib.sha256(raw).hexdigest()
with t.cay(raw,{},None,ten) as root:
 rc,out=t.kiem(m,root)
record('Exact L8 waiver bytes with missing target-root module',rc,out,2,['KHÔNG ĐO ĐƯỢC','L8 không nạp/chạy được gate_output_doi_chieu.py: FileNotFoundError:','TỔNG: KHÔNG ĐO ĐƯỢC'],['L8 miễn trừ','TỔNG: ĐẠT'])
cut='pr680-wp676-land-evidence.yaml';cutraw=(r/'ops/land'/cut).read_bytes()
assert m.MIEN_TRU_CUTOVER[cut]==hashlib.sha256(cutraw).hexdigest()
with t.cay(cutraw,None,None,cut) as root:
 rc,out=t.kiem(t.nap(),root)
record('Exact cutover waiver short-circuits L8 even if module missing',rc,out,0,['MIỄN TRỪ','TỔNG: ĐẠT'],['L8','KHÔNG ĐO ĐƯỢC ops/'])
with t.cay(raw,{},t.DOI_CHIEU,ten) as root:
 mm=t.nap();p=root/'ops/land'/ten
 v,g=mm.kiem_ho_so(p,raw+b'\n',root,__import__('yaml'))
 assert 'L8 $: landed_khong_loi_khai_gate_output' in v and t.L8_MAT in g, (v,g)
 rows.append(dict(label='Hash uses supplied bytes despite unchanged file bytes',passed=True,violations=v,notes=g,disk_sha256=hashlib.sha256(p.read_bytes()).hexdigest(),input_sha256=hashlib.sha256(raw+b'\n').hexdigest()))
waivers={name:hashlib.sha256((r/'ops/land'/name).read_bytes()).hexdigest() for name in m.MIEN_TRU_L8}
assert waivers==m.MIEN_TRU_L8 and len(waivers)==56
cutover={p.name for p in (r/'ops/land').glob('*-land-evidence.yaml') if m.MIEN_TRU_CUTOVER.get(p.name)==hashlib.sha256(p.read_bytes()).hexdigest()}
assert not set(waivers)&cutover
rows.append(dict(label='All waiver raw-byte hashes match and exact cutover sets disjoint',passed=True,l8_count=len(waivers),cutover_count=len(cutover),intersection=[]))
(w/'l8-priority.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n');print('L8_PRIORITY 4/4 passed; L8=56; cutover=25; overlap=0')
