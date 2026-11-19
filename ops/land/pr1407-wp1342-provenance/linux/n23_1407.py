"""Do THAT phan chung N2 (packet_loop.py) va N3 cua #1342 r4 (spec WP1174-WINDOWS-BACKEND-r4 §5) tren Linux, ban sao tam.
Dung: python -X utf8 -B n23_1407.py <clone_day_du_lich_su> <B> <H> <P> <M>
N2: _additive1342r2(B,H), (P,M) phai [] (doi chung); phan chung tren blob H, moi bien the doi MOT thu:
    (n2a) sua mot byte than ham cu `_1174_process` (r0); (n2b) them decorator vao ham moi r4 `_1174_win_note` => phai KHAC [].
N3: (doi chung) `wp1342_additive_byte_preserved` tren cay lam viec o M phai DAT, va tap ten moi muc module = muoi ten;
    (n3a) chen loi goi `_1174_win_spawn_job` vao than `_1174_process` cua cay lam viec => ca phai DO (assertion ve N3);
    (n3b) bo khoi bat buoc `def _1174_win_note` => ve duong (tap ten moi) phai DO.
Moi cap (tim, thay) phai khop DUNG MOT cho; khong khop => KHONG_DO (khong tinh)."""
import ast, json, pathlib, subprocess, sys, tempfile, warnings
warnings.simplefilter("ignore", SyntaxWarning)
SRC, B, H, P, M = sys.argv[1:6]
SRC = pathlib.Path(SRC)
F = ".claude/dev/packet_loop.py"
g = lambda r: subprocess.run(["git", "-C", str(SRC), "show", f"{r}:{F}"], capture_output=True, check=True).stdout
sys.path.insert(0, str(SRC / ".claude/dev"))
import packet_loop_test as T  # noqa: E402
KY_VONG = sorted({"_1174_WIN_JOB_LIMIT", "_1174_WIN_SPAWN_FLAGS", "_1174_WIN_RESUME_OK", "_1174_win_api_job", "_1174_win_pick_thread",
                  "_1174_win_resume_ok", "_1174_win_cleanup", "_1174_win_note", "_1174_win_job_empty", "_1174_win_spawn_job"})


def ten_module(src):
    s = set()
    for n in ast.parse(src).body:
        if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            s.add(n.name)
        elif isinstance(n, ast.Assign):
            s.update(t.id for t in n.targets if isinstance(t, ast.Name))
        elif isinstance(n, ast.AnnAssign) and isinstance(n.target, ast.Name):
            s.add(n.target.id)
    return s


def doi(buf, tim, thay):
    n = buf.count(tim)
    return (None, f"KHONG_DO: mau khop {n} lan") if n != 1 else (buf.replace(tim, thay), None)


bao = {"B": B, "H": H, "P": P, "M": M, "n2": {}, "n3": {}}
hb, bb = g(H), g(B)
bao["n2"]["doi_chung_B_H"] = T._additive1342r2(bb, hb)
bao["n2"]["doi_chung_P_M"] = T._additive1342r2(g(P), g(M))
N2 = {
    "n2a_mot_byte_than_ham_cu__1174_process": (b"    temporary file so that a child which never reads it cannot block us.\"\"\"\n",
                                               b"    temporary file so that a child which never reads it cannot black us.\"\"\"\n"),
    "n2b_decorator_vao_ham_moi_r4__1174_win_note": (b"\ndef _1174_win_note(err, ma_buoc):\n", b"\n@staticmethod\ndef _1174_win_note(err, ma_buoc):\n"),
}
for ten, (tim, thay) in N2.items():
    bien, loi = doi(hb, tim, thay)
    if loi:
        bao["n2"][ten] = {"ket_qua": loi}
        continue
    kq = T._additive1342r2(bb, bien)
    bao["n2"][ten] = {"additive": kq, "ket_qua": "DO_DUNG" if kq else "SONG"}
moi = sorted(ten_module(hb) - ten_module(bb))
bao["n3"]["ve_duong_doi_chung"] = {"ten_moi": moi, "dung": moi == KY_VONG}
bien, loi = doi(hb, b"\ndef _1174_win_note(err, ma_buoc):\n", b"\ndef _wp_bo_khoi(err, ma_buoc):\n")
if loi:
    bao["n3"]["n3b_bo_khoi_bat_buoc__1174_win_note"] = {"ket_qua": loi}
else:
    m2 = sorted(ten_module(bien) - ten_module(bb))
    bao["n3"]["n3b_bo_khoi_bat_buoc__1174_win_note"] = {"ten_moi": m2, "ket_qua": "DO_DUNG" if m2 != KY_VONG else "SONG"}

LENH = ("import sys,tempfile,pathlib,json;sys.path.insert(0,'.claude/dev');import packet_loop_test as T;"
        "k=T.chay_suite(T.CANONICAL,pathlib.Path(tempfile.mkdtemp()),set(sys.argv[1:]));"
        "print('KQ_JSON '+json.dumps({n:(None if v is None else [type(v).__name__,str(v)[:900]]) for n,v in k.items()}))")
CA = "wp1342_additive_byte_preserved"


def chay(goc):
    p = subprocess.run([sys.executable, "-X", "utf8", "-B", "-c", LENH, CA], cwd=goc, capture_output=True, text=True, timeout=900)
    kq = None
    for d in p.stdout.splitlines():
        if d.startswith("KQ_JSON "):
            kq = json.loads(d[8:])
    return {"rc": p.returncode, "kq": kq, "stderr_cuoi": p.stderr[-800:]}


with tempfile.TemporaryDirectory() as tmp:
    d = pathlib.Path(tmp) / "m"
    subprocess.run(["git", "clone", "-q", "--no-hardlinks", str(SRC), str(d)], check=True)
    subprocess.run(["git", "-c", "advice.detachedHead=false", "checkout", "-q", "--detach", M], cwd=d, check=True)
    subprocess.run(["git", "config", "core.abbrev", "7"], cwd=d, check=True)
    bao["n3"]["doi_chung_sach"] = chay(d)
    f = d / F
    goc = f.read_bytes()
    bien, loi = doi(goc, b"    temporary file so that a child which never reads it cannot block us.\"\"\"\n",
                    b"    temporary file so that a child which never reads it cannot block us.\"\"\"\n    _1174_win_spawn_job\n")
    if loi:
        bao["n3"]["n3a_chen_goi__1174_win_spawn_job_trong__1174_process"] = {"ket_qua": loi}
    else:
        f.write_bytes(bien)
        r = chay(d)
        v = (r["kq"] or {}).get(CA)
        dung = bool(v) and "N3" in v[1]
        r["ket_qua"] = "DO_DUNG" if dung else ("SONG" if v is None and r["kq"] else "KHONG_DO")
        r["wired_bien"] = T._wired1342(bien)
        bao["n3"]["n3a_chen_goi__1174_win_spawn_job_trong__1174_process"] = r
        f.write_bytes(goc)

print(json.dumps(bao, ensure_ascii=False, indent=1))
