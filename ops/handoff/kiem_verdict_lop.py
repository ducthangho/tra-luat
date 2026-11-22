#!/usr/bin/env python3
"""Chot may trong phien dieu phoi Mission #1172: verdict review phai theo PROTOCOL_DA_PHIEN §8.3.

Dung: kiem_verdict_lop.py VERDICT.json [--vong N]
rc 0 = HOP_LE; rc 1 = KHONG_HOP_LE (khong duoc dung verdict de va hay approve); rc 2 = khong doc duoc.
Doi:
  - moi finding co class_slug dung dang slug (chu thuong, so, gach noi);
  - class_table la danh sach, moi slug cua findings co dung mot dong, moi dong co slug, manifestations/finding ids,
    highest_open_severity (P0..P3), common_fix, closing_check khong rong;
  - tu vong 2: prior_class_status la danh sach khac rong, moi phan tu co slug va status thuoc
    {DA_VA_THAT, VA_MOT_PHAN, CHUA_VA, KHONG_DO_DUOC} kem bang chung;
  - verdict 'approve' chi khi findings rong.
"""
import json
import re
import sys

SLUG = re.compile(r"^[a-z0-9][a-z0-9-]*$")
TRANG_THAI = {"ĐÃ VÁ THẬT", "VÁ HỜ", "VÁ SINH LỖI MỚI", "CHƯA VÁ"}


def lay(d, *khoa):
    for k in khoa:
        if k in d and d[k] not in (None, "", []):
            return d[k]
    return None


def kiem(d, vong):
    loi = []
    fs = d.get("findings")
    if not isinstance(fs, list):
        return ["findings khong phai danh sach"]
    slugs = set()
    for f in fs:
        s = f.get("class_slug")
        if not isinstance(s, str) or not SLUG.fullmatch(s):
            loi.append(f"finding {f.get('id')}: thieu/sai class_slug ({s!r})")
        else:
            slugs.add(s)
    bang = d.get("class_table")
    if fs or bang is not None:
        if not isinstance(bang, list):
            loi.append("thieu class_table")
        else:
            dem = {}
            for r in bang:
                s = r.get("slug") or r.get("class_slug")
                dem[s] = dem.get(s, 0) + 1
                can = [("bieu hien", ("finding_ids", "manifestations", "findings")),
                       ("phep kiem dong lop", ("closing_check",))]
                if s in slugs:  # lop con mo o luot nay: bat buoc muc cao nhat va cach va chung; lop lich su da dong thi khong
                    can.append(("muc cao nhat", ("highest_open_severity", "max_severity", "severity")))
                    can.append(("cach va chung", ("common_fix", "common_fix_or_reason", "common_fix_or_per_instance_reason")))
                for ten, k in can:
                    if lay(r, *k) is None:
                        loi.append(f"class_table[{s}]: thieu {ten}")
            for s in slugs:
                if dem.get(s, 0) != 1:
                    loi.append(f"class_table: slug {s} xuat hien {dem.get(s, 0)} lan (phai dung 1)")
    if vong >= 2:
        pf = d.get("prior_findings_check")
        if not isinstance(pf, list) or not pf:
            loi.append("vong >= 2 ma thieu prior_findings_check (doi chieu tung finding luot truoc)")
        else:
            for r in pf:
                if (r.get("status") or r.get("label") or r.get("classification")) not in TRANG_THAI or lay(r, "evidence") is None:
                    loi.append(f"prior_findings_check sai nhan/thieu bang chung: {json.dumps(r, ensure_ascii=False)[:120]}")
        p = d.get("prior_class_status")
        if not isinstance(p, list) or not p:
            loi.append("vong >= 2 ma thieu prior_class_status")
        else:
            for r in p:
                st = r.get("status") or r.get("label") or r.get("trang_thai")
                if not (r.get("slug") or r.get("class_slug")) or st not in TRANG_THAI:
                    loi.append(f"prior_class_status sai: {json.dumps(r, ensure_ascii=False)[:120]}")
                elif lay(r, "evidence", "measured_evidence", "bang_chung") is None:
                    loi.append(f"prior_class_status[{r.get('slug')}]: thieu bang chung")
    for f in fs:
        g = f.get("suggested_fix")
        if not (isinstance(g, dict) and all(lay(g, *k) for k in (("where", "o_dau"), ("how", "the_nao"), ("locking_test", "ca_khoa"), ("may_spawn", "what_the_fix_may_spawn", "what_fix_may_spawn", "de_ra")))):
            loi.append(f"finding {f.get('id')}: goi y va thieu du bon phan §7")
    if not isinstance(d.get("hunt_table"), list) or len(d.get("hunt_table") or []) < 6:
        loi.append("hunt_table (BANG SAN) thieu hoac < 6 huong")
    for k in ("provider", "model_family", "session_id", "reviewed_sha", "review_axes", "independent_from_executor_session"):
        if d.get(k) in (None, "", []):
            loi.append(f"thieu truong evidence §7: {k}")
    if d.get("verdict") == "approve" and fs:
        loi.append("approve ma findings khong rong")
    return loi


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    vong = 1
    if "--vong" in sys.argv:
        vong = int(sys.argv[sys.argv.index("--vong") + 1])
    try:
        d = json.load(open(sys.argv[1], encoding="utf-8"))
    except Exception as e:  # noqa: BLE001
        print(f"KHONG_DOC_DUOC: {e}")
        return 2
    loi = kiem(d, vong)
    if loi:
        print("KHONG_HOP_LE (§8.3):")
        for x in loi:
            print("  -", x)
        return 1
    print(f"HOP_LE (§8.3): {len(d.get('findings', []))} finding, {len(d.get('class_table') or [])} lop")
    return 0


if __name__ == "__main__":
    sys.exit(main())
