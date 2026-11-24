#!/usr/bin/env python3
"""So ket qua bo quet ghim (luat 9) giua BASE va HEAD cua dot B — cong cu DO dev-side, khong phai ma thi cong.

  so_base_head.py <D_base> <D_head> <ke_thua.jsonl> <ra.md>

<D_base>, <D_head>: thu muc ra cua `quet_dot_bien.py do` tren base va tren head (manifest.jsonl + kq.jsonl).
<ke_thua.jsonl>: `quet_dot_bien.py hoi-quy <manifest base dang {id:{src,kind}}> <base.py> <head.py>` — moi dot bien cua BASE
ap len dang chuan cua HEAD. Dot bien cua manifest HEAD co sha256 trung mot dong AP_DUNG la KE THUA; con lai la DELTA cua dot B.
"""
import collections
import json
import sys


def doc(p):
    return [json.loads(x) for x in open(p, encoding="utf-8") if x.strip()]


def main(d_base, d_head, ke_thua, ra):
    kq_b = {k["id"]: k for k in doc(f"{d_base}/kq.jsonl")[1:]}
    dau_h = doc(f"{d_head}/kq.jsonl")[0]
    kq_h = {k["id"]: k for k in doc(f"{d_head}/kq.jsonl")[1:]}
    man_h = doc(f"{d_head}/manifest.jsonl")
    kt = doc(ke_thua)
    sha_sang_base = {k["sha256"]: k["id"][len("kho:"):] for k in kt if "sha256" in k}
    khong_ap = [k["id"][len("kho:"):] for k in kt if "sha256" not in k]
    dong, delta, ke, hoi_quy = [], [], [], []
    for m in man_h:
        h = kq_h[m["id"]]
        goc = sha_sang_base.get(m["sha256"])
        if goc is None:
            delta.append((m["id"], h["phan_hang"], (h["giet"] or [""])[0]))
            continue
        b = kq_b[goc]["phan_hang"]
        ke.append((goc, m["id"], b, h["phan_hang"]))
        if b == "GIET" and h["phan_hang"] != "GIET":
            hoi_quy.append((goc, m["id"], b, h["phan_hang"]))
    dem = lambda ds, i: dict(sorted(collections.Counter(x[i] for x in ds).items()))
    dong.append(f"# So base ↔ head — bo quet ghim luat 9\n")
    dong.append(f"- neo head: `{json.dumps(dau_h.get('neo'), sort_keys=True)}`")
    dong.append(f"- manifest head: {len(man_h)} = {len(ke)} ke thua + {len(delta)} delta; manifest base: {len(kq_b)} "
                f"({len(khong_ap)} khong ap duoc len head: {khong_ap})")
    dong.append(f"- phan hang head (tat ca): {dem([(0, kq_h[m['id']]['phan_hang']) for m in man_h], 1)}")
    dong.append(f"- ke thua, hang o BASE: {dem(ke, 2)}; hang o HEAD: {dem(ke, 3)}")
    dong.append(f"- ke thua GIET o base ma KHONG GIET o head (hoi quy): {len(hoi_quy)} {hoi_quy}")
    dong.append(f"- ke thua doi hang bat ky: {[x for x in ke if x[2] != x[3]]}")
    dong.append(f"- delta, hang o HEAD: {dem(delta, 1)}\n")
    dong.append("## Ledger delta (tung ID)\n\n| id | hang | ca giet |\n|---|---|---|")
    dong += [f"| `{i}` | {h} | {c} |" for i, h, c in delta]
    dong.append("\n## Ke thua khong GIET o head (no cua ma L1–L7 co san, tung ID)\n\n| id base | id head | base | head |\n|---|---|---|---|")
    dong += [f"| `{a}` | `{b}` | {c} | {d} |" for a, b, c, d in ke if d != "GIET"]
    open(ra, "w", encoding="utf-8").write("\n".join(dong) + "\n")
    print("\n".join(dong[:8]))
    return 1 if hoi_quy or any(h != "GIET" for _, h, _ in delta) else 0


if __name__ == "__main__":
    sys.exit(main(*sys.argv[1:]))
