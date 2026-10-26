from pathlib import Path
R=Path('.review').resolve();root=R.parent
s=(root/'.review-input/tu-dot-bien/toan_tu.py').read_text().replace('/home/user/tra-luat',str(root))
s=s.replace('d = Path(tempfile.mkdtemp(prefix="tt_"))','d = Path(tempfile.mkdtemp(prefix="tt_", dir='+repr(str(R/'tmp'))+'))')
s=s.replace('return ten, "GIET" if giet and not vo else "TIN_DUNG_GIA" if vo and not giet else "GIET+NEM" if vo else "SONG", (giet[:3], vo[:3])','return {"name": ten, "rank": "GIET" if giet and not vo else "TIN_DUNG_GIA" if vo and not giet else "GIET+NEM" if vo else "SONG", "killed": giet, "other_errors": vo, "cases": kq, "source": str(p)}')
a=s.index('print("so dot bien"')
s=s[:a]+'''out = ROOT / ".review/operators";out.mkdir(exist_ok=True)
rows=[]
print("so dot bien",len(M),flush=True)
with ThreadPoolExecutor(4) as ex:
 for r in ex.map(mot,M):
  rows.append(r);(out/"results.json").write_text(json.dumps(rows,ensure_ascii=False,indent=2))
  print(r["name"],r["rank"],flush=True)
'''
(R/'operators.py').write_text(s)
