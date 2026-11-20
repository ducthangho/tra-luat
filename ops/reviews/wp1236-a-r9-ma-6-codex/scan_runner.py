import sys,os,json,importlib.util,pathlib
# Pure-Python SafeLoader retained; cache only identical immutable input bytes/strings, deepcopy each return.
import yaml,copy
original_safe_load=yaml.safe_load
cache={}
def memo(x):
 if not isinstance(x,(str,bytes)):return original_safe_load(x)
 if x not in cache:cache[x]=original_safe_load(x)
 return copy.deepcopy(cache[x])
if not os.environ.get('REVIEW_NO_CACHE'):yaml.safe_load=memo
p=pathlib.Path(__file__).resolve().parent.parent/'repo/ops/gate_output_doi_chieu_test.py'
s=importlib.util.spec_from_file_location('suite_review',p); m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
slow=('a102_ca_kho_tai_base','a213_la_landed_khop_kiem_ho_so_land')
cs=sys.argv[1:] or [c for c in m.CA if c not in slow]+list(slow)
for c in cs:
 rc,ra=m.chay_ca(c)
 print(json.dumps({'case':c,'rc':rc,'output':ra},ensure_ascii=False),flush=True)
 if rc==3: break
