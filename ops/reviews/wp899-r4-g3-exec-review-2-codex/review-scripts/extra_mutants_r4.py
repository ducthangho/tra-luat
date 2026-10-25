import pathlib,sys,importlib.util,subprocess,os,json,collections
R=pathlib.Path(__file__).resolve().parent;root=R.parent
s=importlib.util.spec_from_file_location('tt',root/'ops/ci_provenance_test.py');t=importlib.util.module_from_spec(s);s.loader.exec_module(t)
if len(sys.argv)>1 and sys.argv[1]=='cases':
 rows=[]
 for c in t.CA:
  rc,out=t.chay_ca(c);rows.append({'case':c,'rc':rc,'output':out})
 print(json.dumps(rows,ensure_ascii=False));sys.exit(0 if all(x['rc']==0 for x in rows) else 3)
src=(root/'ops/ci_provenance.py').read_text();dest=R/'extra-r4';dest.mkdir(exist_ok=True)
mutants=[
 ('sort_bi_bo','sorted(st, key=lambda s: s["number"])','st'),
 ('kiem_number_bi_bo','and len({s["number"] for s in st}) == len(st)','and True'),
 ('sap_xep_theo_ten','sorted(st, key=lambda s: s["number"])','sorted(st, key=lambda s: s["name"])'),
 ('gio_nhan_offset',r'\d\d:\d\d:\d\dZ")',r'\d\d:\d\d:\d\d(?:Z|[+-]\d\d:\d\d)")'),
 ('gio_thieu_header_lay_rest','a <= b["gio"][:19] <= z','a <= (b["gio"][:19] or a) <= z'),
 ('gio_bo_can_duoi','a <= b["gio"][:19] <= z','b["gio"][:19] <= z'),
 ('gio_bo_can_tren','a <= b["gio"][:19] <= z','a <= b["gio"][:19]'),
 ('a_bo_dem_nhom','    if len(buoc) != len(chay):','    if False:'),
 ('a_bo_dem_yaml','    if len(ung) != len(sy):','    if False:'),
 ('b_bo_ten','if any(s.get("name") != ten_du_kien(y)','if False and any(s.get("name") != ten_du_kien(y)'),
 ('d_lay_dau','return khop[0] if len(khop) == 1 else None','return khop[0] if khop else None'),
 ('env_quet_ca_job','for t in j["steps"][:i]))','for t in j["steps"]))'),
 ('env_bo_PATH','re.search("GITHUB_(ENV|PATH)", t["run"])','re.search("GITHUB_ENV", t["run"])'),
 ('number_missing_tu_sinh','_so(s.get("number"), 1)','_so(s.get("number", 1), 1)'),
 ('job_ten_name_bi_bo','for x in (k, j.get("name"))','for x in (k,)'),
 ('job_khoa_bi_bo','for x in (k, j.get("name"))','for x in (j.get("name"),)'),
 ('ten_run_lstrip','v.split("\\n")[0]','v.lstrip().split("\\n")[0]'),
 ('ten_name_khong_kiem_bieu_thuc','_chuoi(s["name"]) and "${{" not in s["name"]','_chuoi(s["name"])'),
]
rows=[]
for name,old,new in [('baseline','TRANG = 100','TRANG = 100')]+mutants:
 rec={'name':name,'old':old,'new':new,'anchor_count':src.count(old)}
 if src.count(old)!=1:rec['rank']='HONG_NEO';rows.append(rec);continue
 p=dest/(name+'.py');p.write_text(src.replace(old,new))
 cmd=[sys.executable,'-B',str(__file__),'cases'];r=subprocess.run(cmd,capture_output=True,env=dict(os.environ,CI_PROVENANCE_MA=str(p),PYTHONDONTWRITEBYTECODE='1'))
 (dest/(name+'.stdout.txt')).write_bytes(r.stdout);(dest/(name+'.stderr.txt')).write_bytes(r.stderr)
 try:res=json.loads(r.stdout)
 except ValueError:rec.update(rc=r.returncode,rank='HONG',stderr=r.stderr.decode());rows.append(rec);continue
 killed=[x['case'] for x in res if x['rc']==3 and x['output'].startswith('DO:'+x['case']+':')]
 bad=[x for x in res if x['rc'] not in (0,3)]
 rec.update(command=cmd,rc=r.returncode,source=str(p),rank='GIET' if killed and not bad else 'TIN_DUNG_GIA' if bad else 'SONG_SOT',killed=killed,other_errors=bad,green=sum(x['rc']==0 for x in res),cases=len(res))
 rows.append(rec);(dest/'results.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2));print(name,rec['rank'],rec.get('killed'),flush=True)
print(collections.Counter(r['rank'] for r in rows))
