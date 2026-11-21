from pathlib import Path
import sys,datetime,json,subprocess,inspect
W=Path(__file__).resolve().parent.parent;R=W/'cay-kho';O=W/'out';sys.dont_write_bytecode=True;sys.path.insert(0,str(R/'ops'))
import lease_publish as lp
rows=lp._quet_lease_toan_kho(R,doi_chieu_ref=False)
time=datetime.datetime(2026,11,21,1,19,7,tzinfo=datetime.timezone.utc)
live=[r for r in rows if lp._phan_loai_lease(r['lease'],time)=='CÒN_HẠN'];tomb=[r for r in live if lp._bia_mo_doi_xung(r['lease'],rows) is True];active=[r for r in live if r not in tomb]
print('LEASE_COUNTS',len(rows),len(live),len(tomb),len(active),'AT',time.isoformat(),flush=True)
for r in active:print('ACTIVE',json.dumps({k:r['lease'].get(k) for k in ['lease_id','packet_issue','write_set','effective_write_set','lease_expires_at_utc','spec_path','branch','base_sha']},ensure_ascii=False),flush=True)
for n in (1460,1462,1469,1470):
 allr=[r for r in rows if r['lease'].get('packet_issue')==n];print('PACKET_LEASES',n,len(allr),[r['lease'].get('lease_id') for r in allr],flush=True)
 for r in allr:
  if r in active:
   p=r['lease'].get('spec_path');print('ACTIVE_SPEC_SOURCE',n,r['ref'],p,flush=True)
   if p:
    q=subprocess.run(['git','-C',str(R),'show',r['ref']+':'+p],capture_output=True);assert q.returncode==0;(O/f'packet-{n}-spec.md').write_bytes(q.stdout)
print('POLICY_EXISTS',(R/'.github/coordination/change-impact.v1.json').exists())
q='.claude/dev/packet_loop.py'
for name,lease in [('exact',{'write_set':[q]}),('prefix',{'write_set':['.claude/dev/']}),('case',{'write_set':[q.upper()]}),('effective_only',{'write_set':['docs/a.md'],'effective_write_set':[q]})]:print('LEASE_MATCH',name,lp._lease_cham_duong(lease,q))
print('LEASE_MATCH_SOURCE',inspect.getsource(lp._lease_cham_duong))
source=(R/'.claude/dev/packet_loop.py').read_text(); print('CLOSURE_READER',any(x in source for x in ['change-impact.v1.json','write_closure']))
# No record-lease call: its reading order is inspected, to avoid authority/mutations on source.
for i,line in enumerate(source.splitlines(),1):
 if 'def cmd_record_lease' in line or '_nguoi_dang_giu' in line or 'I2(Đ)' in line:print('RECORD_LEASE_SOURCE',i,line)
