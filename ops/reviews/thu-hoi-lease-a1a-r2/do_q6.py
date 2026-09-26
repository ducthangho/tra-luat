"""Q6 + (b): cap hai chieu dan xuat tu DUNG cay moc, loc (b) tai clock. yaml.safe_load, khong regex."""
import subprocess,yaml,sys,json,hashlib,importlib.util
from datetime import datetime
goc, moc, clock = sys.argv[1], sys.argv[2], sys.argv[3]
spec=importlib.util.spec_from_file_location("lp",f"{goc}/ops/lease_publish.py"); lp=importlib.util.module_from_spec(spec); sys.modules['lp']=lp; spec.loader.exec_module(lp)
git=lambda *a: subprocess.run(["git","-C",goc,*a],capture_output=True,text=True,check=True).stdout
L={}; hong=[]
for e in git("ls-tree","-z",moc,"ops/leases/").split("\0"):
    if not e: continue
    meta,path=e.split("\t",1); oid=meta.split()[2]
    try: d=yaml.safe_load(git("cat-file","-p",oid))
    except Exception as x: hong.append(path); continue
    if isinstance(d,dict) and d.get("lease_id"):
        if str(d["lease_id"]) in L: hong.append("TRUNG:"+path)
        L[str(d["lease_id"])]=(d,oid,path)
cap=[]; mot_chieu=[]
for lid,(d,oid,p) in L.items():
    for x in (lp._danh_sach_thay_the_cho(d.get("thay_the_cho")) or []):
        c=L.get(str(x))
        if c and str(c[0].get("da_bi_thay_the") or "")==lid: cap.append((str(x),lid,c[1],oid))
        else: mot_chieu.append((str(x),lid))
for lid,(d,oid,p) in L.items():
    t=d.get("da_bi_thay_the")
    if t and not any(c[0]==lid and c[1]==str(t) for c in cap): mot_chieu.append((lid,str(t)))
cap.sort()
now=datetime.fromisoformat(clock.replace("Z","+00:00"))
def trang_thai(moi):
    d=L[moi][0]; het=datetime.fromisoformat(str(d.get("lease_expires_at_utc")).replace("Z","+00:00"))
    if het<=now: return "HET_HAN"
    t=d.get("da_bi_thay_the")
    if not t: return "CON_HIEU_LUC"
    return "DA_BI_THAY" if any(c[0]==moi and c[1]==str(t) for c in cap) else "KHONG_XAC_DINH"
rows=[(a,b,ba,bb,str(L[b][0].get("lease_expires_at_utc")),trang_thai(b)) for a,b,ba,bb in cap]
giu=[r[:4] for r in rows if r[5]=="CON_HIEU_LUC"]
kxd=[r for r in rows if r[5]=="KHONG_XAC_DINH"]
rep=json.dumps(sorted(list(r[:4]) for r in rows),separators=(",",":")).encode()
print(json.dumps({"moc":moc,"clock":clock,"lease_trong_cay":len(L),"yaml_hong_hoac_trung":hong,
  "cap_hai_chieu":len(cap),"mot_chieu":sorted(set(mot_chieu)),"digest_cap_hai_chieu_sha256":hashlib.sha256(rep).hexdigest(),
  "hang":rows,"KHONG_XAC_DINH":len(kxd),"BIA_MO_LICH_SU_theo_b":giu},ensure_ascii=False,indent=1))
sys.exit(3 if kxd or hong else 0)
