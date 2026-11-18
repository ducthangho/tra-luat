"""Do lai ca wp1342_*/wp1174_* va dot bien thuan M7 (d)(e)(g) cua #1342 r3 tren Linux, trong ban sao tam (ngoai kho).
Dung: python dot_bien_linux_1390.py <clone_o_merge> <thu_muc_ra>
Giet khi: ca dich DO, gia tri chay_suite bat dau bang "AssertionError: <nhan mong doi>" (chay_suite luu loi dang chuoi), doi chung (wp1342_pure_seed_boot_refuse) DAT tren ca ban sach va ban dot bien.
Khong khop dung 1 lan / loi khac => KHONG_DO."""
import json, pathlib, shutil, subprocess, sys, tempfile

SRC = pathlib.Path(sys.argv[1]); RA = pathlib.Path(sys.argv[2]); RA.mkdir(parents=True, exist_ok=True)
LENH = ("import sys,tempfile,pathlib,json;sys.path.insert(0,'.claude/dev');import packet_loop_test as T;"
        "k=T.chay_suite(T.CANONICAL,pathlib.Path(tempfile.mkdtemp()),set(sys.argv[1:]));"
        "print('KQ_JSON '+json.dumps({n:(None if v is None else [type(v).__name__,str(v)[:600]]) for n,v in k.items()}))")
DICH, DOI = "wp1342_pure_seed_acl_bang", "wp1342_pure_seed_boot_refuse"
DOT_BIEN = {
    "d_bo_doi_co_P": ([(' or "P" not in found[2]', '')], "dòng 'thiếu P'"),
    "e_them_BA": ([('(user_sid, "SY", "S-1-5-18")', '(user_sid, "SY", "S-1-5-18", "BA")')], "dòng 'ACE cho BA'"),
    "g_chi_co_P": ([('D:((?:P|AI|AR)*)(', 'D:(P)(')], "dòng 'nhận: cờ DACL PAI'"),
}

def chay(goc, ca):
    p = subprocess.run([sys.executable, "-X", "utf8", "-B", "-c", LENH, *ca], cwd=goc, capture_output=True, text=True, timeout=900)
    kq = None
    for d in p.stdout.splitlines():
        if d.startswith("KQ_JSON "):
            kq = json.loads(d[8:])
    return p.returncode, kq, p.stderr[-2000:]

def ban_sao(tmp, ten):
    d = pathlib.Path(tmp) / ten
    subprocess.run(["git", "clone", "-q", "--no-hardlinks", str(SRC), str(d)], check=True)
    subprocess.run(["git", "-c", "advice.detachedHead=false", "checkout", "-q", "--detach",
                    subprocess.run(["git", "rev-parse", "HEAD"], cwd=SRC, capture_output=True, text=True).stdout.strip()], cwd=d, check=True)
    subprocess.run(["git", "config", "core.abbrev", "7"], cwd=d, check=True)
    return d

head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=SRC, capture_output=True, text=True).stdout.strip()
bao = {"src_head": head, "sach": {}, "dot_bien": {}}
with tempfile.TemporaryDirectory() as tmp:
    sach = ban_sao(tmp, "sach")
    rc, kq, err = chay(sach, [DICH, DOI])
    bao["sach"] = {"rc": rc, "kq": kq}
    for ten, (cap, nhan) in DOT_BIEN.items():
        d = ban_sao(tmp, ten)
        f = d / ".claude/dev/packet_loop.py"
        s = f.read_text(encoding="utf-8")
        khop = [s.count(a) for a, _ in cap]
        if khop != [1] * len(cap):
            bao["dot_bien"][ten] = {"ket_luan": "KHONG_DO", "ly_do": f"so lan khop {khop}"}
            continue
        for a, b in cap:
            s = s.replace(a, b, 1)
        f.write_text(s, encoding="utf-8")
        rc, kq, err = chay(d, [DICH, DOI])
        v_dich = (kq or {}).get(DICH); v_doi = (kq or {}).get(DOI, "thieu")
        giet = (isinstance(v_dich, list) and v_dich[1].startswith("AssertionError: " + nhan) and v_doi is None
                and bao["sach"]["kq"] == {DICH: None, DOI: None})
        bao["dot_bien"][ten] = {"cap": cap, "nhan_mong_doi": nhan, "rc": rc, "kq": kq,
                                "ket_luan": "GIET" if giet else ("SONG" if v_dich is None else "KHONG_DO"), "stderr_cuoi": err[-400:]}
(RA / "dot-bien-linux.json").write_text(json.dumps(bao, ensure_ascii=False, indent=1), encoding="utf-8")
print("sach", bao["sach"])
for t, v in bao["dot_bien"].items():
    print(t, v["ket_luan"], (v.get("kq") or {}).get(DICH))
