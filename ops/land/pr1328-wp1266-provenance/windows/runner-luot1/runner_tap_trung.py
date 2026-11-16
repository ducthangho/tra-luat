#!/usr/bin/env python3
"""Runner tập trung (đặc tả B r13 §6 bước 3) — NGOÀI kho. So mã nền với mã ứng viên bằng CÙNG tệp test của H.

Dùng: python runner_tap_trung.py <kho nguồn> <base SHA> <H SHA> <thư mục làm việc (ngoài checkout)>
Một lệnh dựng hai clone dùng một lần `nen` (base) và `ung_vien` (H), phủ hai tệp test của H lên `nen`, chạy CÙNG danh
sách ID ở cả hai, kiểm trạng thái trước/sau, ghi JSON kèm sha256.
"""
import hashlib, json, os, platform, shutil, subprocess, sys
from pathlib import Path

PHU = ("ops/lease_publish_test.py", ".claude/dev/doc_receipt_thu_hoi_test.py")
LP_HAU_TO = ["t129_", "t133_", "t137_", "t151_", "_amb01_to_tien_giu_nguyen", "_amb01b_to_tien_khong_doc_vung_S",
             "_amb01c_to_tien_committer_hong_o_commit_doc_them", "_amb02_merge_base_vung_bang_nhau", "_amb02b_merge_base_vung_khong_rong",
             "_amb03_policy_lech_sau_merge_base", "_amb03b_thu_hoi_moi_tren_master", "_amb04_append_only_qua_merge_base",
             "_amb05_criss_cross_mot_base_lech", "_amb05b_lech_gio_dua_lai_hang_doi", "_amb05c_committer_hong",
             "_amb05d_khong_nhan_ung_vien_stale", "_amb06_khong_chung_goc", "_amb07_vuot_ngan_sach_merge_base",
             "_amb08a_replace_khong_doi_merge_base", "_amb08b_bam_lech_chi_tren_nhanh_S", "_amb09_vuot_ngan_sach_khi_dem_canh",
             "_amb10_chu_thich_workflow_adr0066"]
CAM = ("TL_TOKEN", "TL_WEBAPP", "TL_MASTER_KEY", "TL_AGENT_CREDS_FILEID")
CON = r'''
import importlib.util, json, sys, os, traceback
goc, hau_to = sys.argv[1], json.loads(sys.argv[2])
sys.dont_write_bytecode = True
os.environ.pop("GITHUB_ACTOR", None)
kq = {"cam_vang": {k: (k not in os.environ) for k in %r}}
def nap(p, ten):
    sp = importlib.util.spec_from_file_location(ten, p); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m
try:
    lp = nap(goc + "/ops/lease_publish_test.py", "lp_test")
except BaseException as e:
    print(json.dumps({"nap_hong": "lease_publish_test: " + repr(e)})); sys.exit(0)
ds = {}
for h in hau_to:
    khop = [f for f in lp.CA if (f.__name__.startswith(h) if h.startswith("t") else f.__name__.endswith(h) and f.__name__[1:4].isdigit())]
    if len(khop) != 1:
        ds[h] = ("KHOP_SAI", [f.__name__ for f in khop]); continue
    fn = khop[0]
    try:
        fn(); ds[fn.__name__] = ("QUA", None)
    except lp.TinHieuChotCa as e:
        ds[fn.__name__] = ("ASSERT_CUA_CA", str(e)[:300])
    except BaseException as e:
        ds[fn.__name__] = (type(e).__name__, str(e)[:300])
kq["lease_publish_test"] = ds
try:
    dr = nap(goc + "/.claude/dev/doc_receipt_thu_hoi_test.py", "dr_test")
    m = dr._nap(dr.MODUN, "doc_receipt_thu_hoi")
    ids = [c[0] for c in dr.CA] + ["cli", "dang_ky", "thu_tu_k1", "tinh"]
    d2 = {}
    for i in ids:
        try:
            dr.chay_ca(m, dr.MODUN, {i}); d2[i] = ("QUA", None)
        except dr.TinHieuChotCa as e:
            d2[i] = ("ASSERT_CUA_CA", str(e)[:200])
        except BaseException as e:
            d2[i] = (type(e).__name__, str(e)[:200])
    kq["doc_receipt_thu_hoi_test"] = d2
except BaseException as e:
    kq["doc_receipt_thu_hoi_test"] = {"nap_hong": repr(e)}
print(json.dumps(kq, ensure_ascii=False))
''' % (CAM,)


def g(cay, *a):
    return subprocess.run(["git", "-C", str(cay), *a], capture_output=True, text=True, check=True).stdout


def trang_thai(cay):
    return {"head": g(cay, "rev-parse", "HEAD").strip(), "status": g(cay, "status", "--porcelain").splitlines()}


def main():
    nguon, base, H, lam = Path(sys.argv[1]).resolve(), sys.argv[2], sys.argv[3], Path(sys.argv[4]).resolve()
    if lam.exists():
        shutil.rmtree(lam)
    lam.mkdir(parents=True)
    nen, uv = lam / "nen", lam / "ung_vien"
    for cay, sha in ((nen, base), (uv, H)):     # hai clone trong CÙNG một lệnh
        subprocess.run(["git", "-c", "core.autocrlf=false", "clone", "-q", "--no-hardlinks", "-c", "core.autocrlf=false",
                        str(nguon), str(cay)], check=True)   # Windows: không đổi LF→CRLF, bytes test = bytes của H
        g(cay, "checkout", "-q", "--detach", sha); g(cay, "config", "core.abbrev", "7")
    oid_phu = {}
    for duong in PHU:
        oid_phu[duong] = g(uv, "rev-parse", f"{H}:{duong}").strip()
        (nen / duong).write_bytes((uv / duong).read_bytes())
    truoc = {"nen": trang_thai(nen), "ung_vien": trang_thai(uv)}
    env = {k: v for k, v in os.environ.items() if k not in CAM and not k.startswith(("TL_", "GWS_", "NLM_", "GAS_", "DRIVE_"))}
    ket = {}
    for ten, cay in (("nen", nen), ("ung_vien", uv)):
        p = subprocess.run([sys.executable, "-B", "-c", CON, str(cay), json.dumps(LP_HAU_TO)], capture_output=True, text=True, env=env, cwd=str(cay))
        dong = [d for d in p.stdout.splitlines() if d.startswith("{")]
        ket[ten] = {"rc": p.returncode, "kq": json.loads(dong[-1]) if dong else None, "stderr_cuoi": p.stderr[-1500:]}
    sau = {"nen": trang_thai(nen), "ung_vien": trang_thai(uv)}
    mong_nen = sorted(f" M {d}" for d in PHU)
    chot_tt = {
        "nen_head_la_base": truoc["nen"]["head"] == base == sau["nen"]["head"],
        "uv_head_la_H": truoc["ung_vien"]["head"] == H == sau["ung_vien"]["head"],
        "uv_status_rong": truoc["ung_vien"]["status"] == [] == sau["ung_vien"]["status"],
        "nen_status_dung_hai_dong_M": sorted(truoc["nen"]["status"]) == mong_nen == sorted(sau["nen"]["status"])}
    uv_kq = (ket["ung_vien"]["kq"] or {})
    tat_ca_uv = {**uv_kq.get("lease_publish_test", {}), **uv_kq.get("doc_receipt_thu_hoi_test", {})}
    uv_dat = bool(tat_ca_uv) and all(v[0] == "QUA" for v in tat_ca_uv.values() if isinstance(v, list))
    out = {"base": base, "H": H, "tree_base": g(nen, "rev-parse", f"{base}^{{tree}}").strip(), "tree_H": g(uv, "rev-parse", f"{H}^{{tree}}").strip(),
           "oid_phu": oid_phu, "runner_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(), "nen_may": platform.system(),
           "platform": platform.platform(), "python": sys.version.split()[0],
           "git": subprocess.run(["git", "--version"], capture_output=True, text=True).stdout.strip(), "hau_to": LP_HAU_TO,
           "chot_trang_thai": chot_tt, "ket": ket, "uv_moi_id_qua": uv_dat,
           "cam_vang_uv": uv_kq.get("cam_vang"), "rc": 0 if uv_dat and all(chot_tt.values()) else 1}
    tep = lam / f"tap-trung-{platform.system()}.json"
    tep.write_text(json.dumps(out, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    n_uv = len(tat_ca_uv); n_qua = sum(1 for v in tat_ca_uv.values() if isinstance(v, list) and v[0] == "QUA")
    print(f"tap-trung {platform.system()}: ung_vien {n_qua}/{n_uv} QUA · chot_trang_thai={chot_tt} · json={tep} "
          f"sha256={hashlib.sha256(tep.read_bytes()).hexdigest()}")
    return out["rc"]


if __name__ == "__main__":
    sys.exit(main())
