"""Driver dot bien M6 + phan chung B1 cua #1342 r2 (ngoai kho). Dung: python dot-bien-1342r2.py <src_head> <thu_muc_ra>
Moi dot bien: ca dich + doi chung tren ban SACH (phai dat), roi ban sao MOI, ap MOI cap tim/thay (moi cap khop dung 1 lan),
chay lai hai ca. Giet khi: ca dich DO vi assertion (AssertionError/Hong/TinHieuChotCa), doi chung DAT. Loi import/fixture => KHONG DO."""
import json, os, subprocess, sys, pathlib, hashlib

SRC = pathlib.Path(sys.argv[1]); RA = pathlib.Path(sys.argv[2]); RA.mkdir(parents=True, exist_ok=True)
TEP = ".claude/dev/packet_loop.py"
LENH = ("import sys,tempfile,pathlib,json;sys.path.insert(0,'.claude/dev');import packet_loop_test as T;"
        "k=T.chay_suite(T.CANONICAL,pathlib.Path(tempfile.mkdtemp()),{sys.argv[1]});"
        "print('KQ_JSON '+json.dumps({n:(None if v is None else [type(v).__name__,str(v)[:600]]) for n,v in k.items()}));"
        "sys.exit(0 if list(k.values())==[None] else 1)")
S12 = " " * 12
DOT_BIEN = [
    ("a_khoa_chia_se", [("k.LockFileEx(handle, 2, 0, 0xFFFFFFFF", "k.LockFileEx(handle, 0, 0, 0xFFFFFFFF")],
     "wp1342_native_lock_exclusive", "wp1342_native_lock_names", "L1"),
    ("b_khong_xoa_tam", [(S12 + "if not k.DeleteFileW(temporary):", S12 + "if False:"),
                          (S12 + "# Only our own temporary image is removed, never a published final image.\n" + S12 + "os.unlink(temporary)",
                           S12 + "# Only our own temporary image is removed, never a published final image.\n" + S12 + "pass")],
     "wp1342_native_persist_create", "wp1342_native_persist_update", "P1"),
    ("c_bo_replace_existing", [("k.MoveFileExW(temporary, text, 1 | 8)", "k.MoveFileExW(temporary, text, 8)")],
     "wp1342_native_persist_update", "wp1342_native_persist_create", "P3"),
    ("d_b1_bo_signature_ghi", [('("DeleteFileW", [S], B),\n' + S12 + '("GetHandleInformation", [H, c.POINTER(D)], B)):', '("DeleteFileW", [S], B)):')],
     "wp1342_native_persist_bindings", "wp1342_native_lock_names", "B1"),
    # tu kiem driver: chuoi tim khong ton tai => phai ra KHONG_DO, khong phai GIET
    ("z_tu_kiem_khong_khop", [("CHUOI_KHONG_TON_TAI_1342R2", "x")], "wp1342_native_lock_names", "wp1342_native_persist_create", ""),
]

def chay(goc, ca):
    p = subprocess.run([sys.executable, "-X", "utf8", "-B", "-c", LENH, ca], cwd=goc, capture_output=True, text=True,
                       encoding="utf-8", errors="replace", timeout=900)
    kq = None
    for d in p.stdout.splitlines():
        if d.startswith("KQ_JSON "):
            kq = json.loads(d[8:]).get(ca)
    return p.returncode, kq, (p.stdout + p.stderr)[-3000:]

def phan_loai(rc, kq):
    if rc == 0 and kq is None:
        return "DAT"
    lop = kq[0] if kq and kq[0] != "str" else (kq[1].split(":", 1)[0] if kq else "")
    if lop in ("AssertionError", "Hong", "TinHieuChotCa"):
        return "DO_ASSERT"
    return "KHONG_DO"

bao = {"src_head": subprocess.run(["git", "rev-parse", "HEAD"], cwd=SRC, capture_output=True, text=True).stdout.strip(),
       "python": sys.version, "driver_sha256": hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest(), "dot_bien": []}
for ten, cap, dich, dc, nhan in DOT_BIEN:
    r = {"ten": ten, "dich": dich, "doi_chung": dc, "nhan_assert_mong_doi": nhan}
    for ca in (dich, dc):
        rc, kq, ra = chay(SRC, ca); r[f"sach_{ca}"] = [rc, kq, phan_loai(rc, kq)]
    cl = pathlib.Path(os.environ.get("MUT_GOC", str(RA))) / ten[:1]
    if not cl.exists():
        subprocess.run(["git", "-c", "core.longpaths=true", "clone", "-q", "--no-hardlinks", str(SRC), str(cl)], check=True)
        subprocess.run(["git", "config", "core.longpaths", "true"], cwd=cl, check=True)
    subprocess.run(["git", "-c", "advice.detachedHead=false", "checkout", "-q", "--detach", bao["src_head"]], cwd=cl, check=True)
    subprocess.run(["git", "checkout", "-q", "--", TEP], cwd=cl, check=True)
    p = cl / TEP; s = p.read_bytes().decode("utf-8")
    r["so_lan_khop"] = [s.count(t) for t, _ in cap]
    if any(n != 1 for n in r["so_lan_khop"]):
        r["ket_luan"] = "KHONG_DO (chuoi tim khong khop dung 1 lan)"; bao["dot_bien"].append(r); continue
    for t, th in cap:
        s = s.replace(t, th)
    p.write_bytes(s.encode("utf-8"))
    r["diff"] = subprocess.run(["git", "diff", "--", TEP], cwd=cl, capture_output=True, text=True, encoding="utf-8").stdout
    for ca in (dich, dc):
        rc, kq, ra = chay(cl, ca); r[f"dot_bien_{ca}"] = [rc, kq, phan_loai(rc, kq)]; r[f"ra_{ca}"] = ra
    sach_ok = r[f"sach_{dich}"][2] == "DAT" and r[f"sach_{dc}"][2] == "DAT"
    kd = r[f"dot_bien_{dich}"]
    dung_nhan = bool(nhan) and kd[1] is not None and nhan in str(kd[1])
    if not sach_ok:
        r["ket_luan"] = "KHONG_DO (ban sach khong dat)"
    elif kd[2] == "DO_ASSERT" and r[f"dot_bien_{dc}"][2] == "DAT":
        r["ket_luan"] = "GIET" if dung_nhan else "GIET (assertion khong mang nhan " + nhan + ")"
    elif kd[2] == "DAT":
        r["ket_luan"] = "SONG"
    else:
        r["ket_luan"] = "KHONG_DO (ca dich do khong vi assertion, hoac doi chung do)"
    bao["dot_bien"].append(r)
(RA / "dot-bien.json").write_text(json.dumps(bao, ensure_ascii=False, indent=1), encoding="utf-8")
for r in bao["dot_bien"]:
    print(r["ten"], r.get("so_lan_khop"), r["ket_luan"])
