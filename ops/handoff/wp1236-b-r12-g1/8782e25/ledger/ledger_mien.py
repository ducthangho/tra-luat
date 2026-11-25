#!/usr/bin/env python3
"""Ledger MIEN / VI TRI -> o cua luat 4 va luat 8 qua consumer L8 — cong cu DO dev-side, khong phai ma thi cong.
Chay cac ca c24-c36 cua bo test dot B tren ma nguyen ven va ghi lai MOI lan `main` -> L8 duoc goi:
  - ca bang cua dot B (ky8): moi o = (ca, nhan o, ho so, rc, dong L8 thuc do);
  - c36 (bang IMPORT tu bo test dot A): moi phan tu = (ca A, vi tri ngu phap, phan tu, dong L8 thuc do), vi tri doc tu bien cuc bo
    `truong` / `vi_tri` / `field` cua chinh ca A dang chay (khong sua bo test nao).
Dung: ledger_mien.py <kho> <ra.md> <ra-o.json> <ra-c36.jsonl>"""
import collections
import importlib.util
import json
import sys
from pathlib import Path

kho, ra_md, ra_o, ra_c36 = Path(sys.argv[1]), sys.argv[2], sys.argv[3], sys.argv[4]
sys.dont_write_bytecode = True
s = importlib.util.spec_from_file_location("t", kho / "ops/land_evidence_nguon_test.py")
t = importlib.util.module_from_spec(s)
s.loader.exec_module(t)
CA_B = [c for c in t.CA if c[:3] in ("c25", "c26", "c27", "c29", "c30", "c31", "c32", "c34", "c35")]
o, pt, ten_ca = [], [], [None]
chay_goc, dong_goc = t.chay, t.dong_l8


def ky8(ho_so, prov, mong, ly_do, l8=(), dong=(), doi_chieu=t.DOI_CHIEU, ten=t.TEN):
    rc, ra = chay_goc(ho_so, prov, doi_chieu=doi_chieu, ten=ten)
    do_l8 = dong_goc(ra)
    dat = rc == mong and do_l8 == list(l8) and all(x in ra.split("\n") for x in dong)
    hs = ho_so if isinstance(ho_so, str) else repr(ho_so)
    o.append({"ca": ten_ca[0], "o": ly_do, "ho_so": hs if len(hs) < 400 else hs[:120] + f"... ({len(hs)} ky tu)", "rc_mong": mong, "rc_do": rc,
              "l8_mong": list(l8), "l8_do": do_l8, "dat": dat})
    t.bang(dat, ly_do)


def dong_l8(ra):
    kq, f, ca_a, vi_tri, du_lieu = dong_goc(ra), sys._getframe(1), None, None, None
    if f.f_code.co_name != "qua_l8":
        return kq
    du_lieu = f.f_locals.get("du_lieu")
    while f is not None:
        for k in ("truong", "vi_tri", "field"):
            if vi_tri is None and k in f.f_locals and isinstance(f.f_locals[k], (str, int)):
                vi_tri = f"{k}={f.f_locals[k]}"
        if f.f_code.co_name[:2] == "a1" and f.f_code.co_name[2:4].isdigit():
            ca_a = f.f_code.co_name
            break
        f = f.f_back
    pt.append({"ca_a": ca_a, "vi_tri": vi_tri or "(ca khong chia vi tri)", "phan_tu": ascii(du_lieu)[:300], "l8": kq})
    return kq


t.ky8, t.dong_l8 = ky8, dong_l8
for ten in CA_B + [c for c in t.CA if c[:3] == "c36"]:
    ten_ca[0] = ten
    rc, dong = t.chay_ca(ten)
    assert rc == 0, (ten, rc, dong)
assert all(x["dat"] for x in o) and pt
Path(ra_o).write_text(json.dumps(o, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
Path(ra_c36).write_text("".join(json.dumps(x, ensure_ascii=True) + "\n" for x in pt), encoding="utf-8")
md = ["# Ledger MIEN / VI TRI -> o qua consumer L8 (`main` -> L8), do tren ma nguyen ven\n",
      f"Tong: {len(o)} o cua cac bang dot B (ky8) + {len(pt)} phan tu cua bang IMPORT tu bo test dot A (c36). Tat ca DAT (moi o/phan tu da qua "
      "phep so cua chinh ca: rc va DUNG danh sach dong L8 voi ky vong viet tu dac ta).\n",
      "## Bang dot B (ky8)\n", "| ca | so o | duong (khong dong L8) | am (co dong L8) |", "|---|---:|---:|---:|"]
for ten in CA_B:
    ds = [x for x in o if x["ca"] == ten]
    md.append(f"| `{ten}` | {len(ds)} | {sum(not x['l8_do'] for x in ds)} | {sum(bool(x['l8_do']) for x in ds)} |")
md += ["\n## c36 — bang ngu phap luat 8 IMPORT tu `ops/gate_output_doi_chieu_test.py`\n",
       "| ca A (bo sinh + oracle) | vi tri ngu phap | phan tu | duong | am | ly do L8 quan sat (dem) |", "|---|---|---:|---:|---:|---|"]
nhom = collections.OrderedDict()
for x in pt:
    nhom.setdefault((x["ca_a"], x["vi_tri"]), []).append(x)
for (ca_a, vt), ds in nhom.items():
    ly = collections.Counter(v.split(": ", 1)[1].split(":")[0] + (":" + v.rsplit(":", 1)[1] if "not_measured:" in v or "waiver" in v else "")
                             for x in ds for v in x["l8"])
    md.append(f"| `{ca_a}` | {vt} | {len(ds)} | {sum(not x['l8'] for x in ds)} | {sum(bool(x['l8']) for x in ds)} | "
              f"{', '.join(f'{k} ×{v}' for k, v in sorted(ly.items())) or '—'} |")
tong = collections.Counter(x["ca_a"] for x in pt)
md += ["\n| ca A | tong phan tu qua L8 |", "|---|---:|"] + [f"| `{k}` | {v} |" for k, v in tong.items()] + [f"| **tong** | **{len(pt)}** |"]
for ten in CA_B:
    md += [f"\n## `{ten}`\n", "| # | o | rc | dong L8 thuc do |", "|---:|---|---:|---|"]
    md += [f"| {i} | {x['o'].replace('|', '¦')[:110]} | {x['rc_do']} | {'; '.join(x['l8_do']).replace('|', '¦') or '—'} |"
           for i, x in enumerate((x for x in o if x["ca"] == ten), 1)]
Path(ra_md).write_text("\n".join(md) + "\n", encoding="utf-8")
print("\n".join(md[:60])[:6000])
