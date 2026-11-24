#!/usr/bin/env python3
"""Ledger tung MIEN/O cua luat 4 qua L8 — cong cu DO dev-side. Chay cac ca c24-c35 cua bo test tren ma nguyen ven, ghi lai MOI
loi goi `ky8` (ho so dua vao `main`, rc va cac dong L8 THUC DO, ky vong cua ca). Dung: ledger_o.py <kho> <ra.json> <ra.md>"""
import importlib.util
import json
import sys
from pathlib import Path

kho, ra_json, ra_md = Path(sys.argv[1]), sys.argv[2], sys.argv[3]
sys.dont_write_bytecode = True
s = importlib.util.spec_from_file_location("t", kho / "ops/land_evidence_nguon_test.py")
t = importlib.util.module_from_spec(s)
s.loader.exec_module(t)
MIEN = {   # ca -> (mien cua luat 4 / dong bang Dot B, ghi chu)
    "c25_b2_l8_ho_so_moi_duong_khong_tep_danh_gia": "B2 dong `L8 ...` (luat 1)",
    "c26_b6_l8_duong_khop_tep_danh_gia": "B6 duong khop / thieu provenance",
    "c27_b7_l8_landed_khong_loi_khai": "luat 4: ba dang landed x True/1, uu tien trang_thai_packet, ten khoi landed_<8 so> (B7)",
    "c29_b3_l8_mien_tru_theo_ten_va_bam": "B3 mien tru theo ten + bam (luat 1: dong mat mien tru)",
    "c30_b4_l8_module_khong_nap_duoc_la_khong_do_duoc": "B4 rc 2 KHONG DO DUOC (doi chung module cua goc)",
    "c31_b8_l8_chay_sau_chot_cutover": "B8 thu tu cutover (doi chung mat mien tru L5)",
    "c32_l8_ma_tran_token_va_khoa_qua_cong": "luat 4: tap token, dau phan cach sau token, tep trich, chuan hoa khoa giu chu so, ba ten phi-loi-khai",
    "c34_l8_ma_tran_mien_qua_cong": "luat 4: so URL 0/1/2, dong mien khop tron sau strip, thu tu chin dieu kien kiem_mien (mot loi + hai loi)",
    "c35_l8_ngu_phap_tep_danh_gia_qua_cong": "luat 4: ngu phap tung loai dong cua tep danh gia + luat xuong dong",
}
o, ten_ca = [], [None]
chay_goc = t.chay


def ky8(ho_so, prov, mong, ly_do, l8=(), dong=(), doi_chieu=t.DOI_CHIEU, ten=t.TEN):
    rc, ra = chay_goc(ho_so, prov, doi_chieu=doi_chieu, ten=ten)
    do_l8 = t.dong_l8(ra)
    dat = rc == mong and do_l8 == list(l8) and all(x in ra.split("\n") for x in dong)
    o.append({"ca": ten_ca[0], "o": ly_do, "ho_so": ho_so if len(ho_so) < 400 else ho_so[:120] + f"... ({len(ho_so)} ky tu)",
              "tep_provenance": sorted(prov) if prov is not None else None, "rc_mong": mong, "rc_do": rc, "l8_mong": list(l8), "l8_do": do_l8,
              "dong_mong": list(dong), "dat": dat})
    t.bang(dat, ly_do)


t.ky8 = ky8
for ten in MIEN:
    ten_ca[0] = ten
    rc, dong = t.chay_ca(ten)
    assert rc == 0, (ten, rc, dong)
assert all(x["dat"] for x in o)
Path(ra_json).write_text(json.dumps(o, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
md = ["# Ledger tung mien / o cua luat 4 qua consumer L8 (`main` -> L8), do tren ma nguyen ven\n",
      f"Tong: {len(o)} o qua `ky8` (moi o: mot ho so tam, mot lan chay `main`, so rc va DUNG danh sach dong L8). Tat ca DAT.\n",
      "| ca | mien | so o | o duong (khong dong L8) | o am (co dong L8) |", "|---|---|---:|---:|---:|"]
for ten, mien in MIEN.items():
    ds = [x for x in o if x["ca"] == ten]
    md.append(f"| `{ten}` | {mien} | {len(ds)} | {sum(not x['l8_do'] for x in ds)} | {sum(bool(x['l8_do']) for x in ds)} |")
for ten in MIEN:
    md += [f"\n## `{ten}`\n", "| # | o | rc | dong L8 thuc do |", "|---:|---|---:|---|"]
    md += [f"| {i} | {x['o'].replace('|', '¦')[:110]} | {x['rc_do']} | {'; '.join(x['l8_do']).replace('|', '¦') or '—'} |"
           for i, x in enumerate((x for x in o if x["ca"] == ten), 1)]
Path(ra_md).write_text("\n".join(md) + "\n", encoding="utf-8")
print("\n".join(md[:14]))
