from pathlib import Path
from datetime import datetime
from collections import Counter
import yaml,json,subprocess,hashlib,importlib.util,sys
b=Path(__file__).resolve().parent.parent;r=b/'cay-kho';p=r/'ops/land/pr1041-wp1037-provenance'
def git(*a):return subprocess.check_output(['git','-C',str(r),*a])
s=importlib.util.spec_from_file_location('lp_parent',r/'ops/lease_publish.py');m=importlib.util.module_from_spec(s);sys.modules[s.name]=m;s.loader.exec_module(m)
raw=git('show','a34b9a3:ops/leases/wp1037-r1-g1-claude.yaml');lease=yaml.safe_load(raw);print('LEASE_SNAPSHOT_EQUAL',raw==(p/'lease-wp1037-r1-g1.yaml.txt').read_bytes())
for t in ['2026-10-30T17:37:00Z','2026-10-30T17:53:00Z','2026-10-30T18:07:34Z']:print('LEASE_CLASS',t,m._phan_loai_lease(lease,bay_gio=datetime.fromisoformat(t)))
log=(p/'ai-dang-giu-sau-rut-han/luc-do.txt').read_bytes();h=hashlib.sha256(log).hexdigest();print('AFTER_EXPIRY_LOG_HASH',h,'IN_MANIFEST',h in (p/'SHA256SUMS').read_text());print(log.decode())
land=yaml.safe_load((r/'ops/land/pr1041-wp1037-land-evidence.yaml').read_text());print('LANDED',land['trang_thai_packet']['landed']);print('LEASE_CLAIM',land['lease']['thu_hoi_cuoi']);print('NEW_MEASUREMENT',land['lease']['do_lai_sau_han_20261030T1807Z'])
for a in (1,2):
 jobs=json.loads((p/f'readback-jobs-41069257658-a{a}.json').read_text());run=json.loads((p/f'readback-run-41069257658-a{a}.json').read_text());print('WINDOWS',a,'EVENT',run['event'],'RUN_ATTEMPT',run['run_attempt'],'TOTAL',jobs['total_count'],'ACTUAL',len(jobs['jobs']),'COUNTS',dict(Counter(j['conclusion'] for j in jobs['jobs'])),'WINDOWS_JOBS',sum('windows-latest' in j['labels'] for j in jobs['jobs']))
 for j in jobs['jobs']:
  if j['conclusion']=='failure':print('FAILED_STEPS',j['name'],[x['name'] for x in j['steps'] if x['conclusion']=='failure'])
check=next(x for x in land['pre_merge_checks'] if x.get('run_id')==41069257658);print('WINDOWS_NAME',check['name']);print('WINDOWS_NOTE',check['ghi_chu'])
print('NO_REMOTE_QUERY: historical server ref set 708/708 cannot be independently replayed offline; only saved log and lease classification measured.')
