"""Do NHAN (N1) va phan chung N2 cho ho so land PR #1414 (#387 packet B) tren cay merge 0ca331b, Linux.
Dung: python do_nhan_1414.py <cay merge sach (clone co .git)> <tep ket qua json>
- N1: moi muc W1-W4, W6 (bang DOT_BIEN, sua launcher.py) va H1-H7 (bang DOT_BIEN_HARNESS, sua launcher_test.py) lay NGUYEN VAN (tim, thay)
  tu chinh bang cua cay merge (nap module launcher_test trong mot tien trinh con), ap vao BAN SAO tam (shutil.copytree, symlinks=True) cua cay,
  moi cap phai khop DUNG MOT cho; chay `launcher_test.py --lap-ca <ca dich> --lan 1`; lay DUY NHAT dong (sau khi bo thut le) dang
  `HONG <ca dich>: <ly do>`; <ly do> phai chua nhan cot "nhan do" §4b cua dac ta. Kem doi chung: ca dich tren cay SACH phai qua.
- N2: phan chung dac ta: (a) dat lai _R387_KHOI_MOC ve dong base (bo "/Windows") => t117 DO; (b) dat lai _R387_DONG_CAY ve dong base => t117 DO.
Cay goc khong bi sua."""
import datetime, json, os, shutil, subprocess, sys, tempfile, time

CAY, RA, PY = os.path.abspath(sys.argv[1]), sys.argv[2], sys.executable
TEST, LAUNCHER = ".claude/dev/launcher_test.py", ".claude/dev/launcher.py"
NHAN = {  # spec §4b cot "ca dich & nhan do" (dac ta c67ecfa7)
    "r387_b_windows_khong_do": "r387(e8) Windows job rong phai True",
    "r387_b_windows_dung_nhom": "r387(e6) goi _thanh_vien_nhom tren Windows",
    "r387_b_job_none_thanh_rong": "r387(e7) Windows thieu job phai False ngay",
    "r387_b_windows_long_cay_da_chet": "r387(e6) goi _cay_da_chet",
    "r387_b_linux_di_nhanh_job": "r387(e9) Linux goi _pid_trong_job",
    "r387_fx_dong_truoc_khi_cho": "r387(t2) thu tu do/dong",
    "r387_fx_bao_gan_truoc_khi_gan": "r387(t4) job-da-gan ghi truoc khi gan",
    "r387_fx_bo_kiem_closehandle": "r387(t3) CloseHandle that bai khong bao",
    "r387_fx_khong_dong_job": "r387(t2) thu tu do/dong",
    "r387_fx_phat_dau_khi_gan_hong": "r387(t4b) gan that bai van phat dau",
    "r387_fx_don_dep_ngoai_finally": "r387(t5) teardown khong chay khi ne",
    "r387_fx_loi_bam_nuot_teardown": "r387(t6) loi bam nuot loi teardown",
}
LAY = r"""
import json, sys
sys.argv = ["launcher_test.py"]
sys.path.insert(0, ".claude/dev")
import launcher_test as t
ra = {}
for bang, ten_bang in ((t.DOT_BIEN, "DOT_BIEN"), (t.DOT_BIEN_HARNESS, "DOT_BIEN_HARNESS")):
    for muc in bang:
        if muc[0].startswith("r387_"):
            cap = muc[1] if isinstance(muc[1], list) else [muc[1]]
            ra[muc[0]] = {"bang": ten_bang, "cap": [list(c) for c in cap], "dich": list(muc[2]), "gioi_han": list(muc[3]) if len(muc) > 3 else None}
print(json.dumps(ra, ensure_ascii=False))
"""


def utc():
    return datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")


def chay(cay, ca):
    lenh = [PY, TEST, "--lap-ca", ca, "--lan", "1"]
    t0 = time.monotonic()
    p = subprocess.run(lenh, cwd=cay, capture_output=True, text=True, stdin=subprocess.DEVNULL, timeout=300, encoding="utf-8", errors="replace")
    out = [d.strip() for d in (p.stdout + p.stderr).splitlines()]
    return {"lenh": " ".join(lenh[1:]), "rc": p.returncode, "wall_giay": round(time.monotonic() - t0, 2),
            "dong_hong_ca": [d for d in out if d.startswith(f"HONG {ca}:")], "dong_lap": [d for d in out if d.startswith("lan ")]}


def ban_sao(cap, tep):
    d = tempfile.mkdtemp(prefix="dn1414-")
    dich = os.path.join(d, "cay")
    shutil.copytree(CAY, dich, symlinks=True)
    p = os.path.join(dich, tep)
    s = open(p, encoding="utf-8").read()
    so = []
    for tim, thay in cap:
        so.append(s.count(tim))
        if s.count(tim) != 1:
            break
        s = s.replace(tim, thay, 1)
    open(p, "w", encoding="utf-8").write(s)
    return d, dich, so


bang = json.loads(subprocess.run([PY, "-B", "-c", LAY], cwd=CAY, capture_output=True, text=True, check=True, stdin=subprocess.DEVNULL).stdout)
kq = {"bat_dau": utc(), "cay": CAY, "head": subprocess.run(["git", "rev-parse", "HEAD"], cwd=CAY, capture_output=True, text=True).stdout.strip(),
      "python": sys.version.split()[0], "N1": {}, "N1_doi_chung_sach": {}, "N2": {}}
for ten, nhan in NHAN.items():
    m = bang[ten]
    tep = LAUNCHER if m["bang"] == "DOT_BIEN" else TEST
    d, dich, so = ban_sao(m["cap"], tep)
    try:
        r = {"bang": m["bang"], "tep": tep, "so_lan_khop_tung_cap": so, "dich": m["dich"], "nhan_ky_vong": nhan}
        if so != [1] * len(m["cap"]):
            r["ket_luan"] = "SAI_MAU"
        else:
            r.update(chay(dich, m["dich"][0]))
            dh = r["dong_hong_ca"]
            r["ket_luan"] = "DUNG_NHAN" if (r["rc"] != 0 and len(dh) == 1 and nhan in dh[0]) else "SAI"
    finally:
        shutil.rmtree(d, ignore_errors=True)
    kq["N1"][ten] = r
    print(ten, r["ket_luan"], flush=True)
for ca in sorted({m["dich"][0] for t2, m in bang.items() if t2 in NHAN}):
    kq["N1_doi_chung_sach"][ca] = chay(CAY, ca)
BASE_MOC = ('_R387_KHOI_MOC = ("    if not _nen_do_cay_truoc_bam():   # #387: nền khác Linux/Windows giữ mốc',
            '_R387_KHOI_MOC = ("    if not _nen_do_cay_truoc_bam():   # #387: nền khác Linux giữ mốc')
BASE_CAY = ('_R387_DONG_CAY = (\'    cay_da_chet = (log_cay_chet and platform.system() != "Windows") if _nen_do_cay_truoc_bam() \'\n'
            '                  "else (_thanh_vien_nhom(p.pid) == [])\\n")\n',
            '_R387_DONG_CAY = "    cay_da_chet = log_cay_chet if _nen_do_cay_truoc_bam() else (_thanh_vien_nhom(p.pid) == [])\\n"\n')
for ten, cap in (("bo_cap_nhat_R387_KHOI_MOC", BASE_MOC), ("bo_cap_nhat_R387_DONG_CAY", BASE_CAY)):
    d, dich, so = ban_sao([cap], TEST)
    try:
        r = {"so_lan_khop": so}
        if so == [1]:
            r.update(chay(dich, "t117_moi_mau_dot_bien_phai_khop_DUNG_MOT_cho"))
            r["ket_luan"] = "T117_DO" if r["rc"] != 0 and r["dong_hong_ca"] else "T117_KHONG_DO"
        else:
            r["ket_luan"] = "SAI_MAU"
    finally:
        shutil.rmtree(d, ignore_errors=True)
    kq["N2"][ten] = r
    print(ten, r["ket_luan"], flush=True)
kq["N2"]["t117_cay_sach"] = chay(CAY, "t117_moi_mau_dot_bien_phai_khop_DUNG_MOT_cho")
kq["xong"] = utc()
open(RA, "w", encoding="utf-8").write(json.dumps(kq, ensure_ascii=False, indent=1) + "\n")
