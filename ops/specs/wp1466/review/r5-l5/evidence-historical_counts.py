from pathlib import Path
import sys,datetime,subprocess
O=Path(__file__).resolve().parent;R=O.parent/'cay-kho';sys.path.insert(0,str(R/'ops'));sys.dont_write_bytecode=True
import lease_publish as lp
rows=lp._quet_lease_toan_kho(O/'historical.git',doi_chieu_ref=False)
for stamp in ['2026-11-21T02:57:49+00:00','2026-11-21T03:24:55+00:00']:
 now=datetime.datetime.fromisoformat(stamp);live=[r for r in rows if lp._phan_loai_lease(r['lease'],now)=='CÒN_HẠN'];dead=[r for r in live if lp._bia_mo_doi_xung(r['lease'],rows) is True];active=[r for r in live if r not in dead];print('RECONSTRUCTED_AT',stamp,'COUNTS',len(rows),len(live),len(dead),len(active));print('ACTIVE',[r['lease']['lease_id'] for r in active])
