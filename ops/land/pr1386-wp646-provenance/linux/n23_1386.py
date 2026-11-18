"""Do THAT phan chung N2/N3 cua #646 (spec LEASE-TRUONG-KHAI-NGHIA-r1 §4) tren cay merge, ban sao tam ngoai kho.
Dung: python -X utf8 -B n23_1386.py <clone_day_du_lich_su> <M>
N2: doi chung `doctrine-scan --root .` va `adr-song --root .` rc 0 tren M; phan chung: hai ca mau dac ta chi dinh
    `case_doctrine_scan_chep_tron_5_1_bi_chan` (chep doan §5.1 vao adapter => doctrine-scan rc khac 0) va
    `case_adr_song_thieu_dong_thi_do` (bo mot dong ADR khoi §20 => adr-song rc khac 0) chay qua chay_suite tren M: phai DAT
    (ca DAT nghia la phan chung DO dung nhu ca khang dinh). Ten ca dang `case_<ten>`; chay_suite nhan ten khong co tien to.
N3: doi chung `scripts/tl.py doc-claims-check --strict --json` rc 0, ok true, flags 0 tren M (core.abbrev 7);
    phan chung: them doan van moi (ngoai rao) cuoi docs/PROTOCOL_DA_PHIEN.md chua `ops/khong_ton_tai_dot_bien.py`
    => rc 2 va co PATH_MISSING dung dong ay."""
import json, pathlib, subprocess, sys, tempfile
SRC, M = pathlib.Path(sys.argv[1]), sys.argv[2]
LENH = ("import sys,tempfile,pathlib,json;sys.path.insert(0,'.claude/dev');import packet_loop_test as T;"
        "k=T.chay_suite(T.CANONICAL,pathlib.Path(tempfile.mkdtemp()),set(sys.argv[1:]));"
        "print('KQ_JSON '+json.dumps({n:(None if v is None else [type(v).__name__,str(v)[:900]]) for n,v in k.items()}))")
bao = {"M": M, "n2": {}, "n3": {}}


def run(goc, *a, timeout=900):
    p = subprocess.run([sys.executable, "-X", "utf8", "-B", *a], cwd=goc, capture_output=True, text=True, timeout=timeout)
    return p


with tempfile.TemporaryDirectory() as tmp:
    d = pathlib.Path(tmp) / "m"
    subprocess.run(["git", "clone", "-q", "--no-hardlinks", "--no-checkout", str(SRC), str(d)], check=True)
    subprocess.run(["git", "-c", "advice.detachedHead=false", "checkout", "-q", "--detach", M], cwd=d, check=True)
    subprocess.run(["git", "config", "core.abbrev", "7"], cwd=d, check=True)
    for lenh in ("doctrine-scan", "adr-song"):
        p = run(d, ".claude/dev/packet_loop.py", lenh, "--root", ".")
        bao["n2"][f"doi_chung_{lenh}"] = {"rc": p.returncode, "stdout_cuoi": p.stdout[-400:]}
    ca = ["doctrine_scan_chep_tron_5_1_bi_chan", "adr_song_thieu_dong_thi_do"]
    p = run(d, "-c", LENH, *ca)
    kq = None
    for x in p.stdout.splitlines():
        if x.startswith("KQ_JSON "):
            kq = json.loads(x[8:])
    bao["n2"]["phan_chung_hai_ca_mau"] = {"rc": p.returncode, "kq": kq, "stderr_cuoi": p.stderr[-600:],
                                          "ket_qua": "DO_DUNG" if (kq and set(kq) == set(ca) and all(v is None for v in kq.values())) else "KHONG_DO"}

    def dcc():
        p = run(d, "scripts/tl.py", "doc-claims-check", "--strict", "--json")
        try:
            j = json.loads(p.stdout[p.stdout.index("{"):])
        except ValueError:
            j = None
        return p.returncode, j
    rc, j = dcc()
    bao["n3"]["doi_chung"] = {"rc": rc, "ok": (j or {}).get("ok"), "flags": (j or {}).get("flags")}
    f = d / "docs/PROTOCOL_DA_PHIEN.md"
    goc = f.read_bytes()
    them = b"\nDot bien N3: `ops/khong_ton_tai_dot_bien.py`.\n"
    f.write_bytes(goc + them)
    dong = goc.count(b"\n") + 2
    rc2, j2 = dcc()
    f.write_bytes(goc)
    s = json.dumps(j2, ensure_ascii=False) if j2 is not None else ""
    co = "PATH_MISSING" in s and "khong_ton_tai_dot_bien" in s
    bao["n3"]["phan_chung"] = {"rc": rc2, "ok": (j2 or {}).get("ok"), "flags": (j2 or {}).get("flags"), "dong_them": dong,
                               "co_PATH_MISSING_ten_dot_bien": co, "trich": [x for x in s.split("},") if "khong_ton_tai_dot_bien" in x][:2],
                               "ket_qua": "DO_DUNG" if (rc2 == 2 and co) else "SONG"}

ok = (all(v["rc"] == 0 for k, v in bao["n2"].items() if k.startswith("doi_chung")) and bao["n2"]["phan_chung_hai_ca_mau"]["ket_qua"] == "DO_DUNG"
      and bao["n3"]["doi_chung"]["rc"] == 0 and bao["n3"]["doi_chung"]["ok"] is True and bao["n3"]["phan_chung"]["ket_qua"] == "DO_DUNG")
bao["TONG"] = "DAT" if ok else "KHONG_DAT"
print(json.dumps(bao, ensure_ascii=False, indent=1))
sys.exit(0 if ok else 1)
