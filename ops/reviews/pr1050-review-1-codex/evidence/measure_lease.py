import datetime,subprocess,yaml,importlib.util
from pathlib import Path
repo=Path('cay-kho');head='c24875d00e93e6a98e0a0abd0837e0cbcad65d4d'
when=subprocess.check_output(['git','-C',str(repo),'show','-s','--format=%cI',head]).decode().strip()
p=repo/'ops/land/pr1041-wp1037-provenance/lease-wp1037-r1-g1.yaml.txt';d=yaml.safe_load(p.read_text())
now=datetime.datetime.fromisoformat(when);end=datetime.datetime.fromisoformat(d['lease_until'].replace('Z','+00:00'))
print('reviewed_commit_time',when)
print('recording_snapshot_time 2026-10-30T17:37:30Z')
print('lease_sua_lan_cuoi',d['lease_sua_lan_cuoi'])
print('lease_until',d['lease_until'],'lease_expires_at_utc',d['lease_expires_at_utc'])
print('at_reviewed_commit_lease_expired',now>=end,'seconds_until_expiration',int((end-now).total_seconds()))
print('da_bi_thay_the',d.get('da_bi_thay_the'),'bia_mo',d.get('bia_mo'))
print('lease_source_limitation',d['thu_hoi_bang_rut_han']['gioi_han'])
print('lease_source_reason',d['thu_hoi_bang_rut_han']['ly_do'])
print('LAND_CLAIM',yaml.safe_load((repo/'ops/land/pr1041-wp1037-land-evidence.yaml').read_text())['lease']['thu_hoi_cuoi'])
s=importlib.util.spec_from_file_location('lease_measure',repo/'ops/lease_publish.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
for t in ['2026-10-30T17:37:30+00:00','2026-10-30T17:41:02+00:00','2026-10-30T17:53:00+00:00']:
 print('EXISTING_CLASSIFIER',t,m._phan_loai_lease(d,bay_gio=datetime.datetime.fromisoformat(t)))
