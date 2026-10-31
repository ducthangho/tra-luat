from pathlib import Path
from datetime import datetime
from collections import Counter
import hashlib, json, subprocess, sys, yaml
root=Path(__file__).resolve().parent.parent/'cay-kho'
sys.path.insert(0,str(root/'ops'))
import lease_publish as gate
def blob(sha,path):return subprocess.check_output(['git','-C',str(root),'show',sha+':'+path])
p=root/'ops/land/pr1041-wp1037-provenance'
land='ops/land/pr1041-wp1037-land-evidence.yaml'
old=yaml.safe_load(blob('c24875d',land));new=yaml.safe_load(blob('f37b519',land))
print('EXACT_OLD_NEW_LAND_MATCH_CURRENT_SNAPSHOTS',blob('f37b519',land)==(root/land).read_bytes())
leasepath='ops/leases/wp1037-r1-g1-claude.yaml'
leasebytes=blob('a34b9a38cda2669f9a90958c69bb6f2faa0f4353',leasepath)
print('LEASE_SNAPSHOT_EQUAL_GIT_OBJECT',leasebytes==(p/'lease-wp1037-r1-g1.yaml.txt').read_bytes())
lease=yaml.safe_load(leasebytes)
for t in ['2026-10-30T17:37:00Z','2026-10-30T17:53:00Z','2026-10-30T18:07:34Z']:
    print('CLASSIFY',t,gate._phan_loai_lease(lease,bay_gio=datetime.fromisoformat(t)))
log=(p/'ai-dang-giu-sau-rut-han/luc-do.txt').read_bytes()
digest=hashlib.sha256(log).hexdigest()
print('POST_EXPIRY_LOG_HASH',digest,'IN_MANIFEST',digest in (p/'SHA256SUMS').read_text(),'NEW_SOURCE_BLOCK', 'do_lai_sau_han_20261030T1807Z' in new['lease'])
print('NEW_LOG_MARKERS',[l for l in log.decode().splitlines() if 'wp1037-r1-g1-claude' in l or l.startswith('NGƯỜI_GIỮ') or l.startswith('rc=')])
print('LEASE_OLD_CLAIM',old['lease']['thu_hoi_cuoi'].split(': ',1)[-1][:65])
print('LEASE_NEW_HISTORICAL_CLAIM',new['lease']['thu_hoi_cuoi'].split(': ',1)[-1][:100])
print('WINDOWS_NEW_NAME',new['pre_merge_checks'][1]['name'])
for a in [1,2]:
    data=json.loads((p/f'readback-jobs-41069257658-a{a}.json').read_text())
    jobs=data['jobs']
    print('WINDOWS_ATTEMPT',a,'total',data['total_count'],'array',len(jobs),'conclusions',dict(Counter(j['conclusion'] for j in jobs)),'windows_jobs',sum(j['labels']==['windows-latest'] for j in jobs))
text=new['pre_merge_checks'][1]['ghi_chu']
print('CAUSE_IS_IN_THUAT_LAI_SEGMENT','Thuat_lai — executor khai input runner_set=windows-only' in text and 'KHONG_DO_DUOC tu readback run/jobs da luu' in text)
print('THREE_FILES_CHANGED',subprocess.check_output(['git','-C',str(root),'diff','--numstat','c24875d','f37b519'],text=True).strip())
print('LANDED_STAYS_FALSE',old['trang_thai_packet']['landed'] is False and new['trang_thai_packet']['landed'] is False)
print('NO_REMOTE_REF_READBACK: server 708/708 summary not independently reproducible offline; no network used.')
