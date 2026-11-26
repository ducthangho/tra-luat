"""So kq.jsonl của bộ quét ghim luật 9 giữa nen (base) và sau (head) cho MỘT cặp module/test. Module không đổi ⇒ manifest phải trùng
(cùng tập id, cùng sha256 từng đột biến). In số từng hạng ở hai vế, mọi id đổi hạng, và số id GIET ở base mà KHÔNG GIET ở head (hồi quy).
Dùng: python3 so_base_head.py <D nen> <D sau>   — rc 0 khi inventory trùng và hồi quy = 0; rc 1 nếu không; rc 2 khi không đo được."""
import json
import sys
from collections import Counter
from pathlib import Path


def doc(d):
    dong = [json.loads(x) for x in (Path(d) / "kq.jsonl").read_text(encoding="utf-8").splitlines() if x.strip()]
    log = (Path(d) / "do.log").read_text(encoding="utf-8")
    return dong[0], {k["id"]: k for k in dong[1:]}, sum(x.startswith("HOAN_TAT") for x in log.splitlines())


try:
    (dau_n, n, ht_n), (dau_s, s, ht_s) = doc(sys.argv[1]), doc(sys.argv[2])
except (OSError, ValueError, IndexError, KeyError) as e:
    print(f"KHONG_DO_DUOC: {type(e).__name__}: {e}")
    sys.exit(2)
for ten, dau, ht in (("nen", dau_n, ht_n), ("sau", dau_s, ht_s)):
    print(f"- neo {ten}: {json.dumps(dau['neo'], sort_keys=True)} · baseline {dau['baseline']} · {len(dau['baseline_ca_dat'])} ca dat · tap_con={dau['tap_con']} · HOAN_TAT={ht}")
cung_id = list(n) == list(s)
cung_sha = cung_id and all(n[i].get("sha256") == s[i].get("sha256") for i in n)
cung_neo = all(dau_n["neo"][k] == dau_s["neo"][k] for k in ("cong_cu", "goc", "manifest", "kho", "python"))
print(f"- inventory: nen {len(n)} · sau {len(s)} · cung id va thu tu: {cung_id} · cung sha256 tung dot bien: {cung_sha} · cung neo (cong_cu, goc, manifest, kho, python): {cung_neo}")
print(f"- hang nen: {dict(sorted(Counter(k['phan_hang'] for k in n.values()).items()))}")
print(f"- hang sau: {dict(sorted(Counter(k['phan_hang'] for k in s.values()).items()))}")
doi = [(i, n[i]["phan_hang"], s[i]["phan_hang"]) for i in n if i in s and n[i]["phan_hang"] != s[i]["phan_hang"]]
hoi_quy = [x for x in doi if x[1] == "GIET"]
doi_ca = [(i, n[i]["giet"][:1], s[i]["giet"][:1]) for i in n if i in s and n[i]["phan_hang"] == s[i]["phan_hang"] == "GIET" and n[i]["giet"][:1] != s[i]["giet"][:1]]
print(f"- doi hang bat ky: {len(doi)} {doi}")
print(f"- GIET o nen ma KHONG GIET o sau (hoi quy): {len(hoi_quy)} {hoi_quy}")
print(f"- GIET o ca hai ve nhung ca giet khac nhau: {len(doi_ca)} {doi_ca[:20]}")
dat = cung_id and cung_sha and cung_neo and not hoi_quy and ht_n == ht_s == 1 and not dau_n["tap_con"] and not dau_s["tap_con"]
print(f"KET LUAN: {'KHONG HOI QUY (0 dot bien doi tu GIET sang hang khac)' if dat else 'CO LECH — doc cac dong tren'}")
sys.exit(0 if dat else 1)
