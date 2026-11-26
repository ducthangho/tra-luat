import pathlib,sys,json,datetime,unicodedata,subprocess
root=pathlib.Path('cay-kho').resolve(); sys.path.insert(0,str(root/'ops'))
import lease_publish as lp
rows=lp._quet_lease_toan_kho(root,doi_chieu_ref=False)
now=datetime.datetime(2026,11,20,18,35,tzinfo=datetime.timezone.utc)
live=[r for r in rows if lp._phan_loai_lease(r['lease'],now)=='CÒN_HẠN']
print('SNAPSHOT',now.isoformat(),'RECORDS',len(rows),'LEASED_AT',sum('leased_at_utc' in r['lease'] for r in rows),'LIVE',len(live),'TOMBSTONED',sum(lp._bia_mo_doi_xung(r['lease'],rows) is True for r in live),flush=True)
for r in live:
 l=r['lease']; print('LIVE',l.get('lease_id'),'TOMB',lp._bia_mo_doi_xung(l,rows),'REF',r['ref'],'UNTIL',str(l.get('lease_expires_at_utc')),'WRITE',l.get('write_set'),flush=True)
paths=['docs/adr/0068-bat-bien-protocol-va-review-theo-lop.md','docs/PROTOCOL_DA_PHIEN.md','.claude/dev/packet_loop.py','.claude/dev/packet_loop_test.py','.claude/dev/ci_dang_ky_test.py','.github/workflows/ci.yml','ops/ci_duong_nhanh.py','ops/ci_duong_nhanh_test.py']
for p in paths:
 holders=[]
 for r in live:
  l=r['lease']
  if lp._bia_mo_doi_xung(l,rows) is True: continue
  for raw in l.get('write_set',[]):
   if not isinstance(raw,str):continue
   path=unicodedata.normalize('NFC',raw.strip().removeprefix('planned:').replace('\\','/')).casefold()
   pp=unicodedata.normalize('NFC',p).casefold()
   if pp==path or (path.endswith('/') and pp.startswith(path)):
    holders.append(l.get('lease_id'));break
 print('HOLDERS',p,holders,flush=True)
refs=subprocess.check_output(['git','-C',str(root),'for-each-ref','--format=%(refname)','refs/remotes/origin'],text=True).splitlines()
newadr=[]
for ref in refs:
 paths=subprocess.check_output(['git','-C',str(root),'ls-tree','-r','--name-only',ref,'--','docs/adr'],text=True).splitlines()
 hits=[p for p in paths if pathlib.PurePosixPath(p).name[:4].isdigit() and int(pathlib.PurePosixPath(p).name[:4])>=68]
 if hits:newadr.append([ref,hits])
print('ADR_GE68_REFS',newadr,flush=True)
pathlib.Path('out/leases.json').write_text(json.dumps(rows,ensure_ascii=False,default=str))
