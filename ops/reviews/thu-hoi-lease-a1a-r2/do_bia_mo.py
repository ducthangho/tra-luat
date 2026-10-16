"""Do mien BIA_MO_LICH_SU theo (b) — doc bang ham cua chinh cong (yaml.safe_load), khong regex."""
import sys, json, importlib.util
from pathlib import Path
from collections import defaultdict
goc = Path(sys.argv[1]).resolve()
spec = importlib.util.spec_from_file_location("lp", goc / "ops/lease_publish.py")
lp = importlib.util.module_from_spec(spec); sys.modules["lp"] = lp; spec.loader.exec_module(lp)
cac = lp._quet_lease_toan_kho(goc, chan_nhanh_tut_sau=True)
theo_id = defaultdict(list)
for m in cac:
    lid = m["lease"].get("lease_id")
    if lid: theo_id[str(lid)].append(m)
cap2, cap1, cap2_b = set(), set(), set()
for lid, ms in theo_id.items():
    for m in ms:
        for x in (lp._danh_sach_thay_the_cho(m["lease"].get("thay_the_cho")) or []):
            cu = theo_id.get(str(x), [])
            hai_chieu = any(str(c["lease"].get("da_bi_thay_the") or "") == lid for c in cu)
            (cap2 if hai_chieu else cap1).add((str(x), lid))
# (b): lease MOI con hieu luc = CON_HAN va KHONG bi thay (bia mo doi xung) tren bat ky ban sao nao
def con_hieu_luc(lid):
    ms = theo_id[lid]
    if not any(lp._phan_loai_lease(m["lease"]) == "CÒN_HẠN" for m in ms): return False
    for m in ms:
        if m["lease"].get("da_bi_thay_the") and lp._bia_mo_doi_xung(m["lease"], cac) is True: return False
    return True
for cu, moi in cap2:
    if con_hieu_luc(moi): cap2_b.add((cu, moi))
print(json.dumps({"ban_sao_lease": len(cac), "lease_id": len(theo_id),
  "cap_hai_chieu": len(cap2), "cap_mot_chieu": len(cap1),
  "cap_b_moi_con_hieu_luc": sorted(cap2_b)}, ensure_ascii=False, indent=1))
