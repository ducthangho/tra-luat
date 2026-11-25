#!/usr/bin/env python3
"""wp1463 (PR2) — chốt vùng trước lease: đo tệp được theo dõi mà registry và bộ mở, kết luận BA trạng thái.

Lệnh:
  python3 do_vung_pr2.py do <SHA40> <thư_mục_ra> [đường_dẫn_thêm_vào_Z ...]
  python3 do_vung_pr2.py tu-kiem [--dot-bien]
Mã thoát của `do`: 0 = SACH · 4 = NGOAI_VUNG · 3 = KHONG_DO_DUOC (chỉ 0 được phép cấp lease).

Bốn phép quan sát, mỗi phép một tiến trình con riêng, một nhật ký riêng: `phan_chung_nguyen`, `phan_chung_bon`,
`phan_chung_go` (registry nạp nguyên · bơm bốn khoá mục 3 · bơm rồi gỡ bốn khoá) và `bo_day_du` (lượt đủ của bộ).
Hook `hook/sitecustomize.py` được nạp qua PYTHONPATH, nên MỌI tiến trình Python con cháu (thừa kế môi trường) cũng
ghi; `os.open(..., dir_fd=…)` giải theo /proc/self/fd chứ không theo cwd. Giới hạn: tiến trình KHÔNG phải Python
(git, bash) và tiến trình con xoá môi trường không được quan sát.
Một phép chỉ được tính khi: rc 0 · có dòng BAT_DAU của chính tiến trình gốc · kết quả dương của chính phép
(`phan_chung` trả True; bảng 30 hàng khớp ở `bon`; dòng cuối `TONG: DAT` ở `bo_day_du`) · tập quan sát khác rỗng ·
có nhân chứng của chính phép · không có mở dir_fd nào không giải được. Thiếu bất kỳ điều nào ⇒ KHONG_DO_DUOC.
"""
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
HOOK = os.path.join(HERE, "hook")
K = "ops/ci_provenance_test.py"
Z0 = frozenset({"ops/ci_provenance_test.py", "ops/ci_provenance.py", ".github/workflows/ci.yml", "requirements.txt",
                ".claude/dev/ci_dang_ky_test.py", ".github/workflows/ops-do-workflow-definition.yml", "ops/bash_nen.py",
                ".github/workflows/ci-dot-bien-du.yml", ".github/workflows/launcher-windows.yml"})
GOC = frozenset({"AGENTS.md", "CHANGELOG.md", "CLAUDE.md", "CONTEXT.md", "INSTALL.md", "README.md", "SKILL.md"})
VT0 = (".claude/dev/ci_dang_ky_test.py", ".github/workflows/ops-do-workflow-definition.yml", "ops/bash_nen.py",
       ".github/workflows/ci-dot-bien-du.yml", ".github/workflows/launcher-windows.yml")
MAU_NHE = (r"(?ms)\A(?!.*^(?:TONG|TU KIEM PHAN HANG): DO\b).*^CA: ([1-9]\d*)/(\1) dat\nDOT BIEN: [1-9]\d* muc CHE DO NHE"
           r" — do khi diff cham vung\nTU KIEM PHAN HANG: DAT \(\d+ dot bien\)\nTONG: DAT\n?\Z")
NHAN_CHUNG = {"phan_chung_nguyen": ".github/workflows/ci.yml", "phan_chung_bon": ".github/workflows/ci.yml",
              "phan_chung_go": ".github/workflows/ci.yml", "bo_day_du": "ops/ci_provenance.py"}
THEM_R7 = ("ops/specs/wp1460-r1/hop_dong/bien_nhan_audit.v1.schema.json", "ops/specs/wp1460-r1/hop_dong/fixture.json")
SACH, NGOAI, KDD = "SACH", "NGOAI_VUNG", "KHONG_DO_DUOC"
MA = {SACH: 0, NGOAI: 4, KDD: 3}


def oracle(doi, Z):
    if doi is None:
        return "day_du"
    for x in doi:
        if x in Z or x.startswith("ops/cai_") or x.startswith("ops/cong_cu") or ("/" not in x and x not in GOC):
            return "day_du"
    return "nhe"


BAM_BANG = "0aba13e7b73bee2a09d4a5aac541dfba76dbe4497edde2d77a938ac04a375e58"  # bảng 30 hàng mục 3, revision 7/8


def bang(_them=(), tep=None):
    """Bảng fixture vùng của đặc tả, đúng thứ tự; băm phải khớp BAM_BANG (lệch ⇒ ném, phép ấy không đo được)."""
    with open(tep or os.path.join(HERE, "bang_r7.json"), encoding="utf-8") as f:
        rows = json.load(f)
    bam = hashlib.sha256("".join(f"{n}\t{json.dumps(d)}\t{e}\n" for n, d, e in rows).encode()).hexdigest()
    if bam != BAM_BANG:
        raise ValueError(f"bang fixture lech bam: {bam}")
    return rows


# ---------- tiến trình con: một phép quan sát registry ----------
def probe(root, mode, them):
    import contextlib
    import importlib.util
    import io
    Z = Z0 | set(them)
    os.chdir(root)
    sys.path[:0] = [os.path.join(root, ".claude", "dev"), os.path.join(root, "ops")]
    spec = importlib.util.spec_from_file_location("reg_do", os.path.join(root, ".claude", "dev", "ci_dang_ky_test.py"))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    kq = {"che_do": mode}
    if mode != "nguyen":
        m.NHE[K] = {"CI_PROVENANCE_KHONG_DOT_BIEN": "1"}
        m.MAU_DAY_DU[K] = m.MOI[K]
        m.MAU_NHE[K] = MAU_NHE
        m.VUNG_THEM[K] = VT0 + tuple(them)
        if mode == "bon":
            rows = bang(them)
            kq["so_hang"] = len(rows)
            kq["hang_lech"] = [n for n, d, e in rows if m.ke_hoach(d)[K][0] != e or oracle(d, Z) != e]
        else:
            for d in (m.NHE, m.MAU_DAY_DU, m.MAU_NHE, m.VUNG_THEM):
                del d[K]
    with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
        kq["phan_chung"] = m.phan_chung()
    print("PROBE_KQ " + json.dumps(kq, ensure_ascii=False), flush=True)


# ---------- phía đo ----------
def chay_quan_sat(cmd, cwd, log, timeout=5400):
    env = dict(os.environ)
    env["PYTHONPATH"] = HOOK + (os.pathsep + env["PYTHONPATH"] if env.get("PYTHONPATH") else "")
    env["AUDIT_OPEN_LOG"] = log
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    open(log, "w").close()
    try:
        p = subprocess.Popen(cmd, cwd=cwd, env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        out, _ = p.communicate(timeout=timeout)
        return p.pid, p.returncode, out.decode("utf-8", "replace")
    except Exception as e:  # không chạy được / quá hạn ⇒ không đo được
        return None, None, f"LOI_CHAY: {type(e).__name__}: {e}"


def doc_log(log, root, tracked, pid_goc):
    tap, khong_giai, bat_dau = set(), [], False
    try:
        with open(log, encoding="utf-8", errors="surrogateescape") as f:
            dong = f.read().splitlines()
    except OSError:
        return None, ["khong doc duoc nhat ky"], False
    for d in dong:
        parts = d.split("\t", 2)
        if len(parts) != 3:
            continue
        pid, kieu, p = parts
        if kieu == "BAT_DAU":
            bat_dau = bat_dau or (pid_goc is not None and pid == str(pid_goc))
        elif kieu == "DIRFD_KHONG_GIAI":
            khong_giai.append(p)
        elif kieu in ("MO", "DIRFD"):
            r = os.path.relpath(p, root)
            if r in tracked:  # chỉ tệp được theo dõi: tạo tác/scratch không theo dõi không vào tập
                tap.add(r)
    return tap, khong_giai, bat_dau


def phan_loai(obs, Z, so_hang_ky_vong):
    """obs: list dict(ten, rc, bat_dau, tap, khong_giai, ket, dong_cuoi). Trả (kết luận, chi tiết từng phép)."""
    chi_tiet = []
    for o in obs:
        ly_do = []
        ten = o["ten"]
        if o["rc"] != 0:
            ly_do.append(f"rc={o['rc']}")
        if not o["bat_dau"]:
            ly_do.append("hook khong chay o tien trinh goc")
        if ten == "bo_day_du":
            if o.get("dong_cuoi") != "TONG: DAT":
                ly_do.append(f"dong cuoi={o.get('dong_cuoi')!r}")
        else:
            ket = o.get("ket")
            if not isinstance(ket, dict):
                ly_do.append("thieu PROBE_KQ")
            else:
                if ket.get("phan_chung") is not True:
                    ly_do.append(f"phan_chung={ket.get('phan_chung')!r}")
                if ten == "phan_chung_bon" and (ket.get("hang_lech") != [] or ket.get("so_hang") != so_hang_ky_vong):
                    ly_do.append(f"bang lech={ket.get('hang_lech')} so_hang={ket.get('so_hang')}")
        tap = o["tap"]
        if not tap:
            ly_do.append("tap quan sat rong")
        if tap and NHAN_CHUNG[ten] not in tap:
            ly_do.append(f"thieu nhan chung {NHAN_CHUNG[ten]}")
        if o["khong_giai"]:
            ly_do.append(f"dir_fd khong giai duoc: {o['khong_giai'][:5]}")
        ngoai = sorted(x for x in (tap or ()) if oracle({x}, Z) != "day_du")
        chi_tiet.append({"ten": ten, "do_duoc": not ly_do, "ly_do": ly_do, "tap": sorted(tap or ()), "ngoai_vung": ngoai})
    if any(not c["do_duoc"] for c in chi_tiet) or len(chi_tiet) != len(NHAN_CHUNG):
        return KDD, chi_tiet
    return (NGOAI if any(c["ngoai_vung"] for c in chi_tiet) else SACH), chi_tiet


def do_cay(root, out, them, tracked):
    Z = Z0 | set(them)
    obs = []
    for mode in ("nguyen", "bon", "go"):
        ten = f"phan_chung_{mode}"
        log = os.path.join(out, ten + ".log")
        pid, rc, txt = chay_quan_sat([sys.executable, "-B", os.path.abspath(__file__), "probe", root, mode, *them], root, log)
        with open(os.path.join(out, ten + ".out"), "w", encoding="utf-8") as f:
            f.write(txt)
        ket = None
        for d in txt.splitlines():
            if d.startswith("PROBE_KQ "):
                try:
                    ket = json.loads(d[9:])
                except ValueError:
                    ket = None
        tap, kg, bd = doc_log(log, root, tracked, pid)
        obs.append({"ten": ten, "rc": rc, "bat_dau": bd, "tap": tap, "khong_giai": kg, "ket": ket})
    log = os.path.join(out, "bo_day_du.log")
    pid, rc, txt = chay_quan_sat([sys.executable, "-B", K], root, log)
    with open(os.path.join(out, "bo_day_du.out"), "w", encoding="utf-8") as f:
        f.write(txt)
    dong = [d for d in txt.splitlines() if d.strip()]
    tap, kg, bd = doc_log(log, root, tracked, pid)
    obs.append({"ten": "bo_day_du", "rc": rc, "bat_dau": bd, "tap": tap, "khong_giai": kg, "dong_cuoi": dong[-1] if dong else None,
                "khoi_cuoi": dong[-5:]})
    kl, ct = phan_loai(obs, Z, len(bang(them)))
    return kl, ct, obs


def git_tracked(root):
    r = subprocess.run(["git", "-C", root, "ls-files", "-z"], capture_output=True)
    if r.returncode:
        return None
    return {x for x in r.stdout.decode("utf-8", "surrogateescape").split("\0") if x}


def lenh_do(sha, out, them):
    out = os.path.abspath(out)
    os.makedirs(out, exist_ok=True)
    for cc in ("actionlint", "shellcheck"):
        if not shutil.which(cc):
            print(f"KET_LUAN: {KDD} (thieu {cc})")
            return MA[KDD]
    root = os.path.join(out, "kho")
    for c in (["git", "clone", "-q", "https://github.com/ducthangho/tra-luat.git", root],
              ["git", "-C", root, "checkout", "-q", sha], ["git", "-C", root, "config", "core.abbrev", "7"]):
        if subprocess.run(c).returncode:
            print(f"KET_LUAN: {KDD} (lenh hong: {' '.join(c)})")
            return MA[KDD]
    head = subprocess.run(["git", "-C", root, "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
    tracked = git_tracked(root)
    if head != sha or not tracked:
        print(f"KET_LUAN: {KDD} (head={head} tracked={len(tracked or ())})")
        return MA[KDD]
    kl, ct, obs = do_cay(root, out, them, tracked)
    bc = {"sha": head, "them_Z": them, "ket_luan": kl, "phep": ct,
          "bo_day_du_khoi_cuoi": obs[-1].get("khoi_cuoi"), "so_tep_theo_doi": len(tracked)}
    with open(os.path.join(out, "KET_QUA.json"), "w", encoding="utf-8") as f:
        json.dump(bc, f, ensure_ascii=False, indent=1)
    print(json.dumps(bc, ensure_ascii=False, indent=1))
    print(f"KET_LUAN: {kl}")
    return MA[kl]


# ---------- tự kiểm: cây giả, kết luận kỳ vọng từng ca ----------
REG_GIA = r'''
import os, subprocess, sys
CA = os.environ.get("CA_TU_KIEM", "khoe")
MOI = {"ops/ci_provenance_test.py": "x"}
NHE, MAU_DAY_DU, MAU_NHE, VUNG_THEM = {}, {}, {}, {}
GOC = frozenset({"AGENTS.md", "CHANGELOG.md", "CLAUDE.md", "CONTEXT.md", "INSTALL.md", "README.md", "SKILL.md"})
CHUNG = {"ops/ci_provenance_test.py", "ops/ci_provenance.py", ".github/workflows/ci.yml", "requirements.txt"}
def ke_hoach(doi):
    kq = {}
    for k in NHE:
        vung = CHUNG | set(VUNG_THEM.get(k, ()))
        if CA == "hang_lech" or doi is None or any(x in vung or x.startswith(("ops/cai_", "ops/cong_cu")) or ("/" not in x and x not in GOC) for x in doi):
            kq[k] = ("day_du",) if CA != "hang_lech" else ("nhe",)
        else:
            kq[k] = ("nhe",)
    return kq
def phan_chung():
    if CA != "thieu_nhan_chung":
        open(".github/workflows/ci.yml").read()
    if CA == "doc_thang":
        open("ops/x_ngoai.txt").read()
    if CA == "doc_con":
        subprocess.run([sys.executable, "-c", "open('ops/x_ngoai.txt').read()"], check=True)
    if CA == "doc_dirfd":
        fd = os.open("ops", os.O_RDONLY)
        f = os.open("x_ngoai.txt", os.O_RDONLY, dir_fd=fd)
        os.close(f); os.close(fd)
    if CA == "doc_khong_theo_doi":
        with open("tam_khong_theo_doi.txt", "w") as f:
            f.write("x")
        open("tam_khong_theo_doi.txt").read()
    return CA != "phan_chung_sai"
'''
BO_GIA = r'''
import os, sys
CA = os.environ.get("CA_TU_KIEM", "khoe")
if CA != "thieu_nhan_chung_bo":
    open("ops/ci_provenance.py").read()
if CA == "bo_doc_ngoai":
    open("ops/x_ngoai.txt").read()
print("TIEN TRINH: 1")
print("TONG: DO" if CA in ("bo_do", "bo_tong_do_rc0") else "TONG: DAT")
sys.exit(1 if CA in ("bo_do", "bo_rc") else 0)
'''
CA_KY_VONG = {"khoe": SACH, "doc_thang": NGOAI, "doc_con": NGOAI, "doc_dirfd": NGOAI, "bo_doc_ngoai": NGOAI,
              "phan_chung_sai": KDD, "hang_lech": KDD, "thieu_nhan_chung": KDD, "thieu_nhan_chung_bo": KDD,
              "bo_rc": KDD, "bo_do": KDD, "bo_tong_do_rc0": KDD, "doc_khong_theo_doi": SACH}


def dung_cay_gia(d):
    tep = {".claude/dev/ci_dang_ky_test.py": REG_GIA, K: BO_GIA, "ops/ci_provenance.py": "# dich\n",
           ".github/workflows/ci.yml": "on: push\n", "ops/x_ngoai.txt": "ngoai vung\n", "ops/bash_nen.py": "\n"}
    for p, n in tep.items():
        os.makedirs(os.path.join(d, os.path.dirname(p)), exist_ok=True)
        with open(os.path.join(d, p), "w", encoding="utf-8") as f:
            f.write(n)
    subprocess.run(["git", "init", "-q", d], check=True)
    subprocess.run(["git", "-C", d, "add", "-A"], check=True)
    return git_tracked(d)


def tu_kiem():
    loi = []
    with tempfile.TemporaryDirectory() as td:
        root = os.path.join(td, "kho")
        tracked = dung_cay_gia(root)
        for ca, ky_vong in CA_KY_VONG.items():
            out = os.path.join(td, "ra-" + ca)
            os.makedirs(out)
            os.environ["CA_TU_KIEM"] = ca
            kl, ct, _ = do_cay(root, out, list(THEM_R7), tracked)
            ok = kl == ky_vong
            print(f"{'DAT' if ok else 'DO '} {ca}: {kl} (ky vong {ky_vong})")
            if not ok:
                loi.append(ca)
        os.environ.pop("CA_TU_KIEM", None)
    # đơn vị: phân loại không nhận quan sát rỗng / thiếu BAT_DAU / dir_fd không giải được
    nen = [{"ten": t, "rc": 0, "bat_dau": True, "tap": {NHAN_CHUNG[t]}, "khong_giai": [],
            "ket": {"phan_chung": True, "hang_lech": [], "so_hang": 1}, "dong_cuoi": "TONG: DAT"} for t in NHAN_CHUNG]
    for ten, sua, ky_vong in (("don_vi_khoe", {}, SACH), ("don_vi_rong", {"tap": set()}, KDD),
                              ("don_vi_khong_bat_dau", {"bat_dau": False}, KDD),
                              ("don_vi_khong_giai", {"khong_giai": ["x"]}, KDD), ("don_vi_rc_none", {"rc": None}, KDD)):
        obs = [dict(o) for o in nen]
        obs[3].update(sua)
        kl, _ = phan_loai(obs, Z0, 1)
        ok = kl == ky_vong
        print(f"{'DAT' if ok else 'DO '} {ten}: {kl} (ky vong {ky_vong})")
        if not ok:
            loi.append(ten)
    # đơn vị: bảng fixture đổi một ô ⇒ bang() ném (phép bon không đo được), bảng đúng ⇒ 30 hàng
    with tempfile.TemporaryDirectory() as td:
        rows = bang()
        rows[0][2] = "nhe"
        sai = os.path.join(td, "b.json")
        with open(sai, "w", encoding="utf-8") as f:
            json.dump(rows, f)
        try:
            bang(tep=sai)
            ok = False
        except ValueError:
            ok = len(bang()) == 30
    print(f"{'DAT' if ok else 'DO '} don_vi_bang_sai_bam: {'nem' if ok else 'khong nem'}")
    if not ok:
        loi.append("don_vi_bang_sai_bam")
    print(f"TU_KIEM: {len(CA_KY_VONG) + 6 - len(loi)}/{len(CA_KY_VONG) + 6} dat")
    return 0 if not loi else 1


DOT_BIEN = [  # (tên, tệp, chuỗi cũ, chuỗi mới) — mỗi chuỗi cũ phải xuất hiện đúng một lần
    ("bo_rc", "do_vung_pr2.py", 'if o["rc"] != 0:', "if False:"),
    ("nhan_quan_sat_rong", "do_vung_pr2.py", "if not tap:\n            ly_do.append", "if False:\n            ly_do.append"),
    ("bo_nhan_chung", "do_vung_pr2.py", "if tap and NHAN_CHUNG[ten] not in tap:", "if False:"),
    ("bo_bat_dau", "do_vung_pr2.py", 'if not o["bat_dau"]:', "if False:"),
    ("bo_phan_chung_true", "do_vung_pr2.py", 'if ket.get("phan_chung") is not True:', "if False:"),
    ("bo_bang_lech", "do_vung_pr2.py", 'if ten == "phan_chung_bon" and (', "if False and ("),
    ("bo_tong_dat", "do_vung_pr2.py", 'if o.get("dong_cuoi") != "TONG: DAT":', "if False:"),
    ("bo_khong_giai", "do_vung_pr2.py", 'if o["khong_giai"]:', "if False:"),
    ("khong_lan_truyen_con", "hook/sitecustomize.py", "_tl = threading.local()",
     "_tl = threading.local(); os.environ.pop('AUDIT_OPEN_LOG', None); os.environ.pop('PYTHONPATH', None)"),
    ("dirfd_giai_theo_cwd", "hook/sitecustomize.py", 'goc = os.readlink(f"/proc/self/fd/{dir_fd}")', 'goc = os.getcwd()'),
    ("bo_kiem_bam_bang", "do_vung_pr2.py", "if bam != BAM_BANG:", "if False:"),
    ("ngoai_vung_thanh_sach", "do_vung_pr2.py", "return (NGOAI if any(", "return (SACH if any("),
]


def tu_kiem_dot_bien():
    song = []
    for ten, tep, cu, moi in DOT_BIEN:
        with tempfile.TemporaryDirectory() as td:
            for p in ("do_vung_pr2.py", "bang_r7.json", "hook/sitecustomize.py"):
                os.makedirs(os.path.join(td, os.path.dirname(p)), exist_ok=True)
                shutil.copy(os.path.join(HERE, p), os.path.join(td, p))
            dich = os.path.join(td, tep)
            with open(dich, encoding="utf-8") as f:
                s = f.read()
            dau, moc, duoi = s.partition("\nDOT_BIEN = [")  # chỉ đột biến phần mã, không đụng bảng này
            if dau.count(cu) != 1:
                print(f"HONG {ten}: chuoi cu xuat hien {dau.count(cu)} lan")
                song.append(ten)
                continue
            with open(dich, "w", encoding="utf-8") as f:
                f.write(dau.replace(cu, moi) + moc + duoi)
            r = subprocess.run([sys.executable, "-B", os.path.join(td, "do_vung_pr2.py"), "tu-kiem"], capture_output=True, text=True)
            do = [d for d in r.stdout.splitlines() if d.startswith("DO ")]
            giet = r.returncode != 0 and bool(do)
            print(f"{'GIET' if giet else 'SONG'} {ten}: rc={r.returncode} ca_do={[d.split(':')[0][3:] for d in do]}")
            if not giet:
                song.append(ten)
    print(f"DOT_BIEN: {len(DOT_BIEN) - len(song)}/{len(DOT_BIEN)} bi giet")
    return 0 if not song else 1


if __name__ == "__main__":
    a = sys.argv[1:]
    if a[:1] == ["probe"]:
        probe(a[1], a[2], a[3:])
    elif a[:1] == ["do"] and len(a) >= 3:
        sys.exit(lenh_do(a[1], a[2], a[3:]))
    elif a == ["tu-kiem"]:
        sys.exit(tu_kiem())
    elif a == ["tu-kiem", "--dot-bien"]:
        sys.exit(tu_kiem() or tu_kiem_dot_bien())
    else:
        print(__doc__)
        sys.exit(2)
