#!/usr/bin/env python3
"""wp1448 r2 — doi chieu A/B "khong doi hanh vi" (dac ta ops/specs/wp1448-r2/SPEC.md, nghiem thu 1). CHI DOC kho nguon.

Hai ve (`nen` = base, `sau` = head) duoc DUNG TRONG MOT LENH, cung cac buoc, tu CUNG mot kho nguon (clone cuc bo roi checkout
dung SHA), de rig khong de ra khac biet gia:

  --dung --kho <kho nguon> --base <sha> --head <sha> --ra <thu muc NGOAI kho>
        clone hai ve vao <ra>/nen va <ra>/sau (cung vong lap), ghim core.abbrev 7.
  --output --ra <thu muc>
        (a) chay `ops/ci_duong_nhanh.py` cua TUNG ve tren cung luoi su kien/OID lay tu lich su THAT (merge first-parent truoc
        base: moi merge cho mot o pull_request va mot o push; cong workflow_dispatch va cac o khong do duoc); so BYTE cua
        `GITHUB_OUTPUT` va ma thoat.
  --g5 --ra <thu muc> [--manh 0,1,…]
        (b) chay du cac manh ban kinh cua `ops/cong_cu_test.py` o CA hai ve (xen ke nen/sau tung manh), log va tep manh ra <ra>.
  --so --ra <thu muc>
        kiem RIENG nguon goc that cua tung ve (head, sha256_test dung tep dang chay), roi so PHEP CHIEU: voi moi dinh danh dot
        bien, ca dich + phan quyet tung ca + lop ngoai le phan hang; bo truong nguon goc, ly do tu do va dong `G5_THOI_GIAN`.
        Bao rieng dinh danh thieu, trung, them. (c) cung du lieu phan quyet di qua bo ket luan cua hai ve phai ra cung dong.
Thoat 0 chi khi moi phep so bat buoc co mat va khop; thieu mot phep so => thoat 1 (khong phai "bo qua").
"""
import argparse
import hashlib
import json
import os
import pathlib
import re
import runpy
import subprocess
import sys
import tempfile

SO_MANH = 8
VE = ("nen", "sau")
RE_LOP = re.compile(r"([A-Za-z_][A-Za-z0-9_.]*)(?::|$)")


def chay(lenh, **kw):
    return subprocess.run(lenh, capture_output=True, **kw)


def git(kho, *doi):
    r = chay(["git", "-C", str(kho), *doi])
    if r.returncode != 0:
        raise SystemExit(f"git {' '.join(doi)} rc={r.returncode}: {r.stderr.decode('utf-8', 'replace')[:300]}")
    return r.stdout.decode("utf-8", "replace").strip()


def lenh_dung(ns):
    ra = pathlib.Path(ns.ra).resolve()
    nguon = pathlib.Path(ns.kho).resolve()
    if ra == nguon or nguon in ra.parents:
        raise SystemExit("thu muc --ra phai nam NGOAI kho nguon")
    ra.mkdir(parents=True, exist_ok=True)
    kq = {}
    for ve, sha in (("nen", ns.base), ("sau", ns.head)):      # MOT vong lap, cung cac buoc cho ca hai ve
        dich = ra / ve
        if dich.exists():
            raise SystemExit(f"{dich} da ton tai — dung hai ve phai bat dau tu thu muc sach")
        r = chay(["git", "clone", "--quiet", "--no-checkout", str(nguon), str(dich)])
        if r.returncode != 0:
            raise SystemExit(f"clone {ve} rc={r.returncode}: {r.stderr.decode('utf-8', 'replace')[:300]}")
        git(dich, "checkout", "--quiet", "--detach", sha)
        git(dich, "config", "core.abbrev", "7")
        kq[ve] = {"sha": git(dich, "rev-parse", "HEAD"), "sach": git(dich, "status", "--porcelain") == ""}
        if kq[ve]["sha"] != sha or not kq[ve]["sach"]:
            raise SystemExit(f"ve {ve}: HEAD {kq[ve]['sha']} khac {sha} hoac cay khong sach")
    (ra / "DUNG.json").write_text(json.dumps(kq, indent=1) + "\n", encoding="utf-8")
    print("DUNG:", json.dumps(kq))
    return 0


def doc_dung(ra):
    return json.loads((ra / "DUNG.json").read_text(encoding="utf-8"))


def luoi_output(kho, base, so_merge):
    """[(ten o, env)] — su kien/OID GIONG HET cho hai ve. OID lay tu lich su that truoc `base`."""
    dong = git(kho, "rev-list", "--first-parent", "--merges", "--parents", "-n", str(so_merge), base).split("\n")
    o = []
    for d in dong:
        tp = d.split()
        if len(tp) != 3:
            continue
        hop, p1, p2 = tp
        o.append((f"pull_request {hop[:7]}", {"SU_KIEN": "pull_request", "GOC": p1, "DAU": p2, "MERGE": hop}))
        o.append((f"push {hop[:7]}", {"SU_KIEN": "push", "GOC": p1, "DAU": "", "MERGE": hop}))
    if not o:
        raise SystemExit("khong tim thay merge first-parent nao truoc base")
    hop, p1, p2 = dong[0].split()
    cu = dong[-1].split()[1]                                  # goc CU hon nhieu merge: nhanh dich da tien sau base.sha
    o += [("pull_request goc cu", {"SU_KIEN": "pull_request", "GOC": cu, "DAU": p2, "MERGE": hop}),
          ("pull_request thieu goc", {"SU_KIEN": "pull_request", "GOC": "", "DAU": p2, "MERGE": hop}),
          ("pull_request goc toan 0", {"SU_KIEN": "pull_request", "GOC": "0" * 40, "DAU": p2, "MERGE": hop}),
          ("pull_request merge khong ton tai", {"SU_KIEN": "pull_request", "GOC": p1, "DAU": p2, "MERGE": "f" * 40}),
          ("pull_request dau khong ton tai", {"SU_KIEN": "pull_request", "GOC": p1, "DAU": "e" * 40, "MERGE": hop}),
          ("pull_request thieu merge", {"SU_KIEN": "pull_request", "GOC": p1, "DAU": p2, "MERGE": ""}),
          ("push before toan 0", {"SU_KIEN": "push", "GOC": "0" * 40, "DAU": "", "MERGE": hop}),
          ("push goc khong phai to tien", {"SU_KIEN": "push", "GOC": p2, "DAU": "", "MERGE": p1}),
          ("workflow_dispatch tu_dong", {"SU_KIEN": "workflow_dispatch", "GOC": "", "DAU": "", "MERGE": hop, "CHE_DO_VAO": "tu_dong",
                                         "NHANH_MAC_DINH": "master"}),
          ("workflow_dispatch day_du", {"SU_KIEN": "workflow_dispatch", "GOC": "", "DAU": "", "MERGE": hop, "CHE_DO_VAO": "day_du",
                                        "NHANH_MAC_DINH": "master"}),
          ("workflow_dispatch input la", {"SU_KIEN": "workflow_dispatch", "GOC": "", "DAU": "", "MERGE": hop, "CHE_DO_VAO": "nhanh",
                                          "NHANH_MAC_DINH": "master"}),
          ("workflow_dispatch nhanh la", {"SU_KIEN": "workflow_dispatch", "GOC": "", "DAU": "", "MERGE": hop, "CHE_DO_VAO": "",
                                          "NHANH_MAC_DINH": "khong/co nhanh nay"}),
          ("schedule", {"SU_KIEN": "schedule", "GOC": p1, "DAU": p2, "MERGE": hop})]
    return o


def lenh_output(ns):
    ra = pathlib.Path(ns.ra).resolve()
    dung = doc_dung(ra)
    luoi = luoi_output(ra / "nen", dung["nen"]["sha"], ns.so_merge)
    lech, bang, dem = [], [], {}
    with tempfile.TemporaryDirectory(prefix="wp1448_ab_") as tam:
        for i, (ten, o) in enumerate(luoi):
            kq = {}
            for ve in VE:
                tep = pathlib.Path(tam) / f"{ve}_{i}.txt"
                env = {k: v for k, v in os.environ.items() if not k.startswith(("CI_DUONG_NHANH_", "GITHUB_"))}
                env.update({"CI_DUONG_NHANH_" + k: v for k, v in o.items()}, GITHUB_OUTPUT=str(tep), GITHUB_RUN_ID="1448", GITHUB_RUN_ATTEMPT="1",
                           PYTHONDONTWRITEBYTECODE="1", PYTHONIOENCODING="utf-8", PYTHONUTF8="1")
                r = chay([sys.executable, "-B", "ops/ci_duong_nhanh.py"], cwd=str(ra / ve), env=env)
                kq[ve] = (r.returncode, tep.read_bytes() if tep.exists() else None,
                          sum(1 for x in r.stdout.decode("utf-8", "replace").splitlines() if x.startswith("BONG_")))
            giong = kq["nen"][:2] == kq["sau"][:2] and kq["nen"][1] is not None
            che_do = (kq["nen"][1] or b"?=?").split(b"\n")[0].decode("ascii", "replace")
            dem[(o["SU_KIEN"], che_do)] = dem.get((o["SU_KIEN"], che_do), 0) + 1
            bang.append({"o": ten, "giong": giong, "rc": [kq["nen"][0], kq["sau"][0]], "output_nen": (kq["nen"][1] or b"").decode("ascii", "replace"),
                         "so_dong_bong": [kq["nen"][2], kq["sau"][2]]})
            if not giong:
                lech.append(ten)
    kq = {"so_o": len(luoi), "so_giong": sum(1 for b in bang if b["giong"]), "lech": lech,
          "phu": {f"{a} | {b}": n for (a, b), n in sorted(dem.items())},
          "dong_bong_chi_o_ve_sau": all(b["so_dong_bong"] == [0, 2] for b in bang), "bang": bang}
    su_kien = {a for a, _ in dem}
    che_do = {b for _, b in dem}
    du = (len(luoi) >= 12 and {"pull_request", "push", "workflow_dispatch"} <= su_kien and {"che_do=duong_nhanh", "che_do=day_du"} <= che_do)
    kq["dat"] = bool(du and not lech and kq["dong_bong_chi_o_ve_sau"])
    (ra / "AB_OUTPUT.json").write_text(json.dumps(kq, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"AB OUTPUT: {kq['so_giong']}/{kq['so_o']} o GITHUB_OUTPUT trung BYTE · lech {lech} · phu {kq['phu']} · "
          f"dong bong chi o ve sau: {kq['dong_bong_chi_o_ve_sau']} · {'DAT' if kq['dat'] else 'DO'}")
    return 0 if kq["dat"] else 1


def lenh_g5(ns):
    ra = pathlib.Path(ns.ra).resolve()
    doc_dung(ra)
    cac = [int(x) for x in ns.manh.split(",")] if ns.manh else list(range(SO_MANH))
    for k in cac:
        for ve in VE:                                         # xen ke hai ve: troi cua may chia deu cho ca hai
            tep = ra / "g5" / ve / f"manh-{k}.txt"
            log = ra / "g5" / ve / f"manh-{k}.log"
            if log.exists() and tep.exists():
                print(f"g5 {ve} manh {k}: da co, bo qua", flush=True)
                continue
            tep.parent.mkdir(parents=True, exist_ok=True)
            env = {x: v for x, v in os.environ.items() if not x.startswith(("CONG_CU_TEST_", "CI_DUONG_NHANH_", "GITHUB_"))}
            env.update(CONG_CU_TEST_MANH=f"{k}/{SO_MANH}", CONG_CU_TEST_MANH_RA=str(tep), PYTHONDONTWRITEBYTECODE="1",
                       PYTHONIOENCODING="utf-8", PYTHONUTF8="1")
            with open(log, "wb") as f:
                rc = subprocess.run([sys.executable, "ops/cong_cu_test.py"], cwd=str(ra / ve), env=env, stdout=f, stderr=subprocess.STDOUT).returncode
            with open(log, "ab") as f:
                f.write(f"\nAB_RC={rc}\n".encode())
            print(f"g5 {ve} manh {k}: rc={rc}", flush=True)
    return 0


def lop_ngoai_le(trang_thai, ly_do):
    """Lop ngoai le PHAN HANG cua mot ca: `giet_that` = chot cua chinh ca (TinHieuChotCa); `tin_dung_gia` = ten lop loi dung dau ly do
    (hoac nhan co dinh cua bo phan hang); con lai khong co lop."""
    if trang_thai == "giet_that":
        return "TinHieuChotCa"
    if trang_thai != "tin_dung_gia" or not isinstance(ly_do, str):
        return None
    if ly_do.startswith("giàn giáo hỏng"):
        return "LoiDungCa"
    if ly_do.startswith("chốt của ca khác"):
        return "TinHieuChotCa(ca khac)"
    m = RE_LOP.match(ly_do)
    return m.group(1) if m else "?"


def doc_ve(ra, ve, dung):
    """Du lieu phan quyet cua mot ve + kiem nguon goc THAT cua chinh ve ay. Tra (ban ghi theo ten, loi)."""
    loi, ban_ghi, trung = [], {}, []
    sha_test = hashlib.sha256((ra / ve / "ops" / "cong_cu_test.py").read_bytes()).hexdigest()
    for k in range(SO_MANH):
        tep = ra / "g5" / ve / f"manh-{k}.txt"
        log = ra / "g5" / ve / f"manh-{k}.log"
        if not tep.is_file() or not log.is_file():
            loi.append(f"{ve}: thieu tep manh {k} (manh khong dat hoac chua chay)")
            continue
        if b"\nAB_RC=0\n" not in log.read_bytes():
            loi.append(f"{ve}: manh {k} khong thoat 0")
        dong = tep.read_text(encoding="utf-8").split("\n")
        dau = json.loads(dong[0][5:]) if dong[0].startswith("MANH ") else {}
        if dau.get("head") != dung[ve]["sha"] or dau.get("sha256_test") != sha_test or (dau.get("manh"), dau.get("so_manh")) != (k, SO_MANH):
            loi.append(f"{ve}: nguon goc manh {k} sai: {dau} (mong head {dung[ve]['sha']}, sha256_test {sha_test})")
        for d in dong[1:]:
            if not d:
                continue
            if not d.startswith("BKCON "):
                loi.append(f"{ve}: manh {k} co dong ngoai hop dong: {d[:60]!r}")
                continue
            bg = json.loads(d[6:])
            if bg[1] in ban_ghi:
                trung.append(bg[1])
            ban_ghi[bg[1]] = bg
    if trung:
        loi.append(f"{ve}: dinh danh TRUNG: {sorted(trung)[:10]}")
    return ban_ghi, loi


def chieu(bg):
    """Phep chieu cua mot ban ghi: (loai, ca dich, {ca: (phan quyet, lop ngoai le phan hang)}); ban ghi `loi` => ('loi',)."""
    if bg[0] != "do":
        return ("loi",)
    return ("do", bg[2], tuple(sorted((ca, v[0], lop_ngoai_le(v[0], v[1])) for ca, v in bg[3].items())))


def nap_bang(goc):
    """Module `cong_cu_test` cua mot ve (nap khong chay `__main__`)."""
    cu, cwd = list(sys.path), os.getcwd()
    try:
        os.chdir(goc)
        return runpy.run_path(str(goc / "ops" / "cong_cu_test.py"), run_name="wp1448_ab")
    finally:
        os.chdir(cwd)
        sys.path[:] = cu
        for m in ("lease_publish_test", "bash_nen", "lease_publish"):
            sys.modules.pop(m, None)


def lenh_so(ns):
    ra = pathlib.Path(ns.ra).resolve()
    dung = doc_dung(ra)
    mod = {ve: nap_bang(ra / ve) for ve in VE}
    ten = {ve: list(mod[ve]["DOT_BIEN"]) for ve in VE}
    phan = {ve: [mod[ve]["_phan_manh"](k, SO_MANH) for k in range(SO_MANH)] for ve in VE}
    loi, du_lieu = [], {}
    for ve in VE:
        du_lieu[ve], l = doc_ve(ra, ve, dung)
        loi += l
        if sorted(t for p in phan[ve] for t in p) != sorted(ten[ve]):
            loi.append(f"{ve}: phan hoach manh khong phu dung bang dot bien")
        thieu = sorted(set(ten[ve]) - set(du_lieu[ve]))
        if thieu:
            loi.append(f"{ve}: {len(thieu)} dinh danh hien hanh THIEU ban ghi: {thieu[:10]}")
        thua = sorted(set(du_lieu[ve]) - set(ten[ve]))
        if thua:
            loi.append(f"{ve}: ban ghi cho dinh danh ngoai bang: {thua[:10]}")
    chung = [t for t in ten["nen"] if t in set(ten["sau"])]
    mat = sorted(set(ten["nen"]) - set(ten["sau"]))
    them = [t for t in ten["sau"] if t not in set(ten["nen"])]
    if mat:
        loi.append(f"dinh danh cua ve nen MAT o ve sau: {mat[:10]}")
    doi_dinh_nghia = [t for t in chung if mod["nen"]["DOT_BIEN"][t] != mod["sau"]["DOT_BIEN"][t]]
    if doi_dinh_nghia:
        loi.append(f"dinh nghia dot bien DOI giua hai ve: {doi_dinh_nghia[:10]}")
    doi_manh = [t for k in range(SO_MANH) for t in phan["nen"][k] if t not in phan["sau"][k]]
    if doi_manh:
        loi.append(f"dot bien doi manh giua hai ve: {doi_manh[:10]}")
    lech, so_sanh, trung_byte = [], 0, 0
    for t in chung:
        a, b = du_lieu["nen"].get(t), du_lieu["sau"].get(t)
        if a is None or b is None:
            continue
        so_sanh += 1
        trung_byte += a == b
        if chieu(a) != chieu(b):
            ca = sorted(set(a[3]) | set(b[3])) if a[0] == b[0] == "do" else []
            lech.append({"ten": t, "ca_lech": [(c, a[3].get(c), b[3].get(c)) for c in ca if (a[3].get(c) or [None])[0] != (b[3].get(c) or [None])[0]][:5]})
    if so_sanh != len(ten["nen"]):
        loi.append(f"chi so duoc {so_sanh}/{len(ten['nen'])} dinh danh cua ve nen")
    if lech:
        loi.append(f"{len(lech)} dinh danh LECH phep chieu: {[x['ten'] for x in lech][:10]}")
    # (c) cung du lieu phan quyet (cua ve nen) qua bo ket luan cua HAI ve => cung dong bao va so loi
    lech_kl = [t for t in chung if t in du_lieu["nen"]
               and mod["nen"]["_ket_luan_ban_ghi"](du_lieu["nen"][t], ()) != mod["sau"]["_ket_luan_ban_ghi"](du_lieu["nen"][t], ())]
    if lech_kl:
        loi.append(f"(c) bo ket luan cua hai ve ra khac nhau tren CUNG du lieu: {lech_kl[:10]}")
    pq = {}
    for ve in VE:
        for bg in du_lieu[ve].values():
            for v in (bg[3].values() if bg[0] == "do" else ()):
                pq[(ve, v[0])] = pq.get((ve, v[0]), 0) + 1
    them_kq = {t: (chieu(du_lieu["sau"][t])[0], sum(1 for _c, tt, _l in chieu(du_lieu["sau"][t])[2] if tt == "giet_that"),
                   sum(1 for _c, tt, _l in chieu(du_lieu["sau"][t])[2] if tt == "tin_dung_gia")) for t in them if t in du_lieu["sau"]}
    kq = {"dung": dung, "so_dinh_danh": {ve: len(ten[ve]) for ve in VE}, "so_ca": {ve: len(mod[ve]["CA"]) for ve in VE},
          "so_dinh_danh_so_duoc": so_sanh, "so_ban_ghi_trung_tung_byte": trung_byte, "thieu_o_ve_sau": mat, "them_o_ve_sau": them,
          "them_o_ve_sau_[loai, so giet_that, so tin_dung_gia]": them_kq, "lech_phep_chieu": lech, "lech_bo_ket_luan": lech_kl,
          "so_phan_quyet_theo_ve": {f"{a} | {b}": n for (a, b), n in sorted(pq.items())}, "loi": loi, "dat": not loi}
    (ra / "AB_G5.json").write_text(json.dumps(kq, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"AB G5: so {so_sanh}/{len(ten['nen'])} dinh danh cua ve nen · lech phep chieu {len(lech)} · trung tung byte {trung_byte} · "
          f"them o ve sau {len(them)} · thieu {len(mat)} · (c) lech {len(lech_kl)} · loi {len(loi)} · {'DAT' if not loi else 'DO'}")
    for x in loi:
        print("  LOI", x[:400])
    return 0 if not loi else 1


def main():
    for s in (sys.stdout, sys.stderr):
        if hasattr(s, "reconfigure"):
            s.reconfigure(encoding="utf-8", errors="backslashreplace")
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    for co in ("--dung", "--output", "--g5", "--so"):
        ap.add_argument(co, action="store_true")
    for co in ("--kho", "--base", "--head", "--ra", "--manh"):
        ap.add_argument(co)
    ap.add_argument("--so-merge", type=int, default=30)
    ns = ap.parse_args()
    if sum((ns.dung, ns.output, ns.g5, ns.so)) != 1 or not ns.ra:
        ap.error("chon DUNG MOT trong --dung | --output | --g5 | --so, kem --ra")
    if ns.dung:
        if not (ns.kho and ns.base and ns.head):
            ap.error("--dung can --kho, --base, --head")
        return lenh_dung(ns)
    return lenh_output(ns) if ns.output else lenh_g5(ns) if ns.g5 else lenh_so(ns)


if __name__ == "__main__":
    sys.exit(main())
