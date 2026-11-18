#!/usr/bin/env python3
"""Do tay N1/N2/N3 cho ho so land pr1388-wp387 (#387 packet A) tren cay merge e4fdf09.

Cach dung: python do_tay_1388.py <cay merge sach> <tep ket qua json>
- Moi phep do chay launcher_test.py --lap-ca <ca> --lan 1 trong mot BAN SAO tam cua cay (shutil.copytree),
  khong sua cay goc. Dot bien tay: mot cap (tim, thay) phai khop DUNG MOT cho.
- N1: (a), (a') DAT tren cay sach; xoa ve bam khoi than (a) => (a') DO.
- N2: (b) DAT; xoa dong gan log_bam_luc_utc trong launcher.py => (b) DO bang TinHieuChotCa, khong KeyError.
- N3: muoi mot ca moi chay tren cay sach, do tong wall (< 25 s).
"""
import json, os, shutil, subprocess, sys, tempfile, time, datetime

CAY = os.path.abspath(sys.argv[1])
RA = sys.argv[2]
PY = sys.executable
TEST = ".claude/dev/launcher_test.py"
LAUNCHER = ".claude/dev/launcher.py"

CA_A = "r387_m1_chau_ghi_muon_khai_pham_vi_bam"
CA_A2 = "r387_m1_doi_chung_ghi_som_lam_ve_bam_do"
CA_B = "r387_m1_con_thuong_chung_minh_cay_chet"
CA_N3 = [
    "r387_fixture_teardown_bao_loi_giu_loi_goc",  # (t)
    "r387_m2_chau_ghi_trong_han_thi_bam_du",      # (c)
    "r387_m2_khong_do_duoc_thi_khong_cho",        # (d)
    "r387_m2_han_chung_cho_moi_lan_do",           # (e)
    "r387_a_nen_khac_giu_moc_ket_thuc_base",      # (i)
    "r387_m1_stop_trong_luc_cho_khong_bi_de",     # (f)
    "r387_m1_prompt_linux_xoa_khi_cay_chet",      # (g)
    "r387_m2_ngat_trong_luc_doi_ghi_bi_ngat",     # (h)
]


def utc():
    return datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")


def chay(cay, ca):
    lenh = [PY, TEST, "--lap-ca", ca, "--lan", "1"]
    t0 = time.monotonic()
    p = subprocess.run(lenh, cwd=cay, capture_output=True, text=True, stdin=subprocess.DEVNULL, timeout=300)
    dt = time.monotonic() - t0
    out = (p.stdout + p.stderr).strip().splitlines()
    return {"ca": ca, "lenh": " ".join(lenh[1:]), "rc": p.returncode, "wall_giay": round(dt, 2),
            "dong_hong": [d.strip() for d in out if d.strip().startswith("HONG")],
            "dong_lap": [d.strip() for d in out if d.strip().startswith("LAP ")]}


def ban_sao(tim, thay, tep):
    d = tempfile.mkdtemp(prefix="dt1388-")
    dich = os.path.join(d, "cay")
    shutil.copytree(CAY, dich, symlinks=True)
    p = os.path.join(dich, tep)
    s = open(p, encoding="utf-8").read()
    n = s.count(tim)
    if n != 1:
        raise SystemExit(f"mau khong khop dung mot cho ({n}) trong {tep}: {tim!r}")
    open(p, "w", encoding="utf-8").write(s.replace(tim, thay, 1))
    return d, dich


kq = {"bat_dau_utc": utc(), "cay": CAY, "python": sys.version.split()[0], "do": []}

# Doi chung tren cay sach
for ca in [CA_A, CA_A2, CA_B]:
    r = chay(CAY, ca); r["bien_the"] = "sach"; r["ky_vong"] = "rc 0"; r["dat"] = r["rc"] == 0
    kq["do"].append(r)

# N1 tay: xoa ve bam khoi than (a) => (a') DO
VE_BAM = '            bang(bam_dia != so["stdout_sha256"], "r387(a) ve bam: bam so == bam dia, chau khong ghi SAU luc bam")\n'
d, cay = ban_sao(VE_BAM, "", TEST)
try:
    r = chay(cay, CA_A2); r["bien_the"] = "N1 tay: xoa ve bam khoi than (a)"; r["ky_vong"] = "rc != 0, HONG (a')"
    r["dat"] = r["rc"] != 0 and any(CA_A2 in h for h in r["dong_hong"])
    kq["do"].append(r)
finally:
    shutil.rmtree(d, ignore_errors=True)

# N2 tay: xoa dong gan log_bam_luc_utc => (b) DO bang TinHieuChotCa, khong KeyError
GAN = '    ban_ghi["log_bam_luc_utc"] = _bay_gio().isoformat()   # #387: gán NGAY TRƯỚC vòng băm\n'
d, cay = ban_sao(GAN, "", LAUNCHER)
try:
    r = chay(cay, CA_B); r["bien_the"] = "N2 tay: xoa dong gan log_bam_luc_utc"
    r["ky_vong"] = "rc != 0, HONG (b) bang TinHieuChotCa, khong KeyError"
    h = " ".join(r["dong_hong"])
    r["dat"] = r["rc"] != 0 and "TinHieuChotCa" in h and "KeyError" not in h
    kq["do"].append(r)
finally:
    shutil.rmtree(d, ignore_errors=True)

# N3: muoi mot ca moi (t,a,a',b,c,d,e,i,f,g,h) tren cay sach, tong wall
tong = sum(x["wall_giay"] for x in kq["do"][:3])
for ca in CA_N3:
    r = chay(CAY, ca); r["bien_the"] = "sach (N3)"; r["ky_vong"] = "rc 0"; r["dat"] = r["rc"] == 0
    kq["do"].append(r); tong += r["wall_giay"]
kq["n3_tong_wall_11_ca_giay"] = round(tong, 2)
kq["n3_ghi_chu"] = "wall do theo tung tien trinh --lap-ca (gom khoi dong interpreter); tieu chi < 25 s"
kq["ket_thuc_utc"] = utc()
kq["tat_ca_dat"] = all(x["dat"] for x in kq["do"]) and tong < 25
json.dump(kq, open(RA, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print(json.dumps({"tat_ca_dat": kq["tat_ca_dat"], "n3_tong": kq["n3_tong_wall_11_ca_giay"],
                  "do": [(x["bien_the"], x["ca"], x["rc"], x["dat"]) for x in kq["do"]]}, ensure_ascii=False, indent=1))
sys.exit(0 if kq["tat_ca_dat"] else 1)
