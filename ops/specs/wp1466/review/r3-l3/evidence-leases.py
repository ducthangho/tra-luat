from pathlib import Path
import sys,importlib.util,datetime,json,subprocess
W=Path(__file__).resolve().parent.parent;R=W/'cay-kho';sys.dont_write_bytecode=True
sys.path.insert(0,str(R/'ops'))
import lease_publish as lp
rows=lp._quet_lease_toan_kho(R,doi_chieu_ref=False)
time=datetime.datetime(2026,11,21,0,11,44,tzinfo=datetime.timezone.utc)
live=[r for r in rows if lp._phan_loai_lease(r['lease'],time)=='CÒN_HẠN'];tomb=[r for r in live if lp._bia_mo_doi_xung(r['lease'],rows) is True];active=[r for r in live if r not in tomb]
print('LEASE_COUNTS',len(rows),len(live),len(tomb),len(active),'AT',time.isoformat(),flush=True)
for r in active:print('ACTIVE',json.dumps({k:r['lease'].get(k) for k in ['lease_id','packet_issue','write_set','effective_write_set','lease_expires_at_utc','spec_path','branch']},ensure_ascii=False),flush=True)
for n in (1460,1462,1469,1470):
 allr=[r for r in rows if r['lease'].get('packet_issue')==n]
 print('PACKET_LEASES',n,len(allr),[r['lease'].get('lease_id') for r in allr],flush=True)
 for r in allr:
  if r in active:
   spec=r['lease'].get('spec_path');print('ACTIVE_SPEC_SOURCE',n,r['ref'],spec,flush=True)
   if spec:
    p=subprocess.run(['git','-C',str(R),'show',r['ref']+':'+spec],capture_output=True,text=True)
    (W/'out'/f'packet-{n}-spec.md').write_text(p.stdout)
print('POLICY_FILE_EXISTS',(R/'.github/coordination/change-impact.v1.json').exists())
