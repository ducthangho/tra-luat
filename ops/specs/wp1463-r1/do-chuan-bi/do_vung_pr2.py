#!/usr/bin/env python3
"""wp1463 (PR2) — chốt vùng trước lease: đo tệp được theo dõi mà registry và bộ mở, kết luận BA trạng thái.

Lệnh:
  python3 do_vung_pr2.py do <SHA40> <thư_mục_ra> [đường_dẫn_thêm_vào_Z ...]
  python3 do_vung_pr2.py tu-kiem [--dot-bien]
Mã thoát của `do`: 0 = SACH · 4 = NGOAI_VUNG · 3 = KHONG_DO_DUOC (chỉ 0 được phép cấp lease).

Bốn phép, tập ĐÓNG, mỗi phép đúng MỘT lần, mỗi phép một tiến trình con riêng và một nhật ký riêng:
`phan_chung_nguyen`, `phan_chung_bon`, `phan_chung_go` (registry nạp nguyên · bơm bốn khoá mục 3 · bơm rồi gỡ)
và `bo_day_du` (lượt đủ của bộ). Hook `hook/sitecustomize.py` nạp qua PYTHONPATH trước mọi import của mã được đo.
Hook ghi: lần mở (đường dẫn theo chữ VÀ đường dẫn sau realpath, nên đọc qua symlink không theo dõi vẫn ra tệp
được theo dõi), `os.open(..., dir_fd=…)` giải theo fd, và mọi sự kiện tạo tiến trình con.
Một phép chỉ ĐO ĐƯỢC khi đủ: rc 0 · dòng BAT_DAU của chính tiến trình gốc · kết quả dương của chính phép
(`phan_chung` True; ở `bon` đủ 30 hàng và KHÔNG hàng nào lệch; ở `bo_day_du` dòng cuối `TONG: DAT`) · tập quan sát
khác rỗng · có nhân chứng của chính phép · không có `dir_fd` không giải được · số dòng BAT_DAU của tiến trình con
≥ số tiến trình Python con được sinh (một con Python chạy không có hook — `-I`, `-S`, `-E`, môi trường bị xoá — thì
thiếu dòng BAT_DAU ⇒ không đo được). Giới hạn còn lại, khai thẳng: tiến trình KHÔNG phải Python (git, bash, actionlint,
shellcheck) và Python được gọi gián tiếp qua shell không được quan sát.
"""
import hashlib
import json
import os
import re
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
THEM_R7 = ("ops/specs/wp1460-r1/hop_dong/bien_nhan_audit.v1.schema.json", "ops/specs/wp1460-r1/hop_dong/fixture.json")
MAU_NHE = (r"(?ms)\A(?!.*^(?:TONG|TU KIEM PHAN HANG): DO\b).*^CA: ([1-9]\d*)/(\1) dat\nDOT BIEN: [1-9]\d* muc CHE DO NHE"
           r" — do khi diff cham vung\nTU KIEM PHAN HANG: DAT \(\d+ dot bien\)\nTONG: DAT\n?\Z")
PHEP = ("phan_chung_nguyen", "phan_chung_bon", "phan_chung_go", "bo_day_du")  # tập ĐÓNG, đúng thứ tự chạy
NHAN_CHUNG = {"phan_chung_nguyen": ".github/workflows/ci.yml", "phan_chung_bon": ".github/workflows/ci.yml",
              "phan_chung_go": ".github/workflows/ci.yml", "bo_day_du": "ops/ci_provenance.py"}
SACH, NGOAI, KDD = "SACH", "NGOAI_VUNG", "KHONG_DO_DUOC"
MA = {SACH: 0, NGOAI: 4, KDD: 3}
BAM_BANG = "0aba13e7b73bee2a09d4a5aac541dfba76dbe4497edde2d77a938ac04a375e58"  # bảng 30 hàng mục 3, revision 7+
SO_HANG = 30
_RE_PY = re.compile(r"python[0-9.]*(\.exe)?$")


def oracle(doi, Z):
    if doi is None:
        return "day_du"
    for x in doi:
        if x in Z or x.startswith("ops/cai_") or x.startswith("ops/cong_cu") or ("/" not in x and x not in GOC):
            return "day_du"
    return "nhe"


def bang(tep=None):
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
            kq["so_hang"], kq["hang_lech"] = 0, []
            for n, d, e in bang():
                kq["so_hang"] += 1
                if m.ke_hoach(d)[K][0] != e or oracle(d, Z) != e:
                    kq["hang_lech"].append(n)
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


def la_python(sinh):
    for x in (sinh.get("exe"), (sinh.get("argv") or [None])[0]):
        if x and _RE_PY.search(os.path.basename(x)):
            return True
        if x and os.path.realpath(x) == os.path.realpath(sys.executable):
            return True
    return False


def doc_log(log, root, tracked, pid_goc):
    """Trả dict quan sát của MỘT phép. tap = tệp được theo dõi khớp đường dẫn theo chữ HOẶC sau realpath."""
    q = {"tap": set(), "khong_giai": [], "bat_dau_goc": False, "bat_dau_con": 0, "python_con": 0, "doc_duoc": True}
    try:
        with open(log, encoding="utf-8", errors="surrogateescape") as f:
            dong = f.read().splitlines()
    except OSError:
        q["doc_duoc"] = False
        return q
    for d in dong:
        parts = d.split("\t", 2)
        if len(parts) != 3:
            continue
        pid, kieu, p = parts
        if kieu == "BAT_DAU":
            if pid_goc is not None and pid == str(pid_goc) and not q["bat_dau_goc"]:
                q["bat_dau_goc"] = True
            else:
                q["bat_dau_con"] += 1
        elif kieu == "DIRFD_KHONG_GIAI":
            q["khong_giai"].append(p)
        elif kieu == "SINH":
            try:
                if la_python(json.loads(p)):
                    q["python_con"] += 1
            except ValueError:
                q["python_con"] += 1  # không đọc được sự kiện sinh ⇒ coi như một con chưa chứng minh có hook
        elif kieu in ("MO", "DIRFD", "THAT"):
            r = os.path.relpath(p, root)
            if r in tracked:  # chỉ tệp được theo dõi: tạo tác/scratch không theo dõi không vào tập
                q["tap"].add(r)
    return q


def kiem_phep(o, Z):
    """Một phép: trả (danh sách lý do không đo được, danh sách tệp ngoài vùng)."""
    ly_do, ten = [], o["ten"]
    if o["rc"] != 0:
        ly_do.append(f"rc={o['rc']}")
    if not o["doc_duoc"]:
        ly_do.append("khong doc duoc nhat ky")
    if not o["bat_dau_goc"]:
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
            if ten == "phan_chung_bon" and (ket.get("hang_lech") != [] or ket.get("so_hang") != SO_HANG):
                ly_do.append(f"bang lech={ket.get('hang_lech')} so_hang={ket.get('so_hang')}")
    tap = o["tap"]
    if not tap:
        ly_do.append("tap quan sat rong")
    if tap and NHAN_CHUNG[ten] not in tap:
        ly_do.append(f"thieu nhan chung {NHAN_CHUNG[ten]}")
    if o["khong_giai"]:
        ly_do.append(f"dir_fd khong giai duoc: {o['khong_giai'][:5]}")
    if o["bat_dau_con"] < o["python_con"]:
        ly_do.append(f"python con khong hook: sinh {o['python_con']}, bat_dau {o['bat_dau_con']}")
    return ly_do, sorted(x for x in tap if oracle({x}, Z) != "day_du")


def phan_loai(obs, Z):
    """obs: list quan sát. Trả (kết luận, chi tiết theo phép). Tên phép phải ĐÚNG tập PHEP, mỗi tên đúng một lần."""
    chi_tiet, ten = [], [o.get("ten") for o in obs]
    for o in obs:
        ly_do, ngoai = kiem_phep(o, Z)
        chi_tiet.append({"ten": o.get("ten"), "do_duoc": not ly_do, "ly_do": ly_do, "tap": sorted(o["tap"]), "ngoai_vung": ngoai})
    if sorted(ten) != sorted(PHEP):
        chi_tiet.append({"ten": "_tap_phep", "do_duoc": False, "ly_do": [f"tap phep {ten} != {list(PHEP)}"], "tap": [], "ngoai_vung": []})
    if any(not c["do_duoc"] for c in chi_tiet):
        return KDD, chi_tiet
    return (NGOAI if any(c["ngoai_vung"] for c in chi_tiet) else SACH), chi_tiet


def do_cay(root, out, them, tracked):
    obs = []
    for ten in PHEP:
        log = os.path.join(out, ten + ".log")
        if ten == "bo_day_du":
            cmd = [sys.executable, "-B", K]
        else:
            cmd = [sys.executable, "-B", os.path.abspath(__file__), "probe", root, ten[len("phan_chung_"):], *them]
        pid, rc, txt = chay_quan_sat(cmd, root, log)
        with open(os.path.join(out, ten + ".out"), "w", encoding="utf-8") as f:
            f.write(txt)
        o = {"ten": ten, "rc": rc, **doc_log(log, root, tracked, pid)}
        if ten == "bo_day_du":
            dong = [d for d in txt.splitlines() if d.strip()]
            o["dong_cuoi"], o["khoi_cuoi"] = (dong[-1] if dong else None), dong[-5:]
        else:
            o["ket"] = None
            for d in txt.splitlines():
                if d.startswith("PROBE_KQ "):
                    try:
                        o["ket"] = json.loads(d[9:])
                    except ValueError:
                        o["ket"] = None
        obs.append(o)
    kl, ct = phan_loai(obs, Z0 | set(them))
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
    bc = {"sha": head, "them_Z": them, "ket_luan": kl, "phep": ct, "python_con": {o["ten"]: [o["python_con"], o["bat_dau_con"]] for o in obs},
          "bo_day_du_khoi_cuoi": obs[-1].get("khoi_cuoi"), "so_tep_theo_doi": len(tracked)}
    with open(os.path.join(out, "KET_QUA.json"), "w", encoding="utf-8") as f:
        json.dump(bc, f, ensure_ascii=False, indent=1)
    print(json.dumps(bc, ensure_ascii=False, indent=1))
    print(f"KET_LUAN: {kl}")
    return MA[kl]


# ---------- tự kiểm: cây giả; mỗi ca nhắm MỘT phép (CA_PHEP), kiểm kết luận VÀ kết quả từng phép ----------
_CHUNG_GIA = r'''
import atexit, os, subprocess, sys
CA = os.environ.get("CA_TU_KIEM", "khoe")
PHEP = sys.argv[3] if len(sys.argv) > 3 and sys.argv[1:2] == ["probe"] else "bo"
BAT = os.environ.get("CA_PHEP", "*") in ("*", PHEP)
def doc_ngoai():
    if not BAT:
        return
    if CA == "doc_thang":
        open("ops/x_ngoai.txt").read()
    elif CA in ("doc_con", "con_I", "con_S", "con_E"):
        co = {"doc_con": [], "con_I": ["-I"], "con_S": ["-S"], "con_E": ["-E"]}[CA]
        subprocess.run([sys.executable, *co, "-c", "open('ops/x_ngoai.txt').read()"], check=True)
    elif CA == "doc_dirfd":
        fd = os.open("ops", os.O_RDONLY)
        f = os.open("x_ngoai.txt", os.O_RDONLY, dir_fd=fd)
        os.close(f); os.close(fd)
    elif CA == "doc_alias":
        p = "/tmp/wp1463-alias-" + str(os.getpid())
        os.symlink(os.path.abspath("ops/x_ngoai.txt"), p)
        open(p).read(); os.unlink(p)
    elif CA == "doc_khong_theo_doi":
        with open("tam_khong_theo_doi.txt", "w") as f:
            f.write("x")
        open("tam_khong_theo_doi.txt").read()
    elif CA == "rc_sau":
        atexit.register(lambda: os._exit(42))
    elif CA == "log_rong":
        atexit.register(lambda: open(os.environ["AUDIT_OPEN_LOG"], "w").close())
'''
REG_GIA = _CHUNG_GIA + r'''
MOI = {"ops/ci_provenance_test.py": "x"}
NHE, MAU_DAY_DU, MAU_NHE, VUNG_THEM = {}, {}, {}, {}
GOC = frozenset({"AGENTS.md", "CHANGELOG.md", "CLAUDE.md", "CONTEXT.md", "INSTALL.md", "README.md", "SKILL.md"})
CHUNG = {"ops/ci_provenance_test.py", "ops/ci_provenance.py", ".github/workflows/ci.yml", "requirements.txt"}
HANG_CUOI = ["ops/specs/wp1460-r1/hop_dong/khac.json", "ops/specs/wp1460-r1/fixture.json", "ops/specs/wp1460-r1/hop_dong/fixture.json.bak"]
def ke_hoach(doi):
    kq = {}
    for k in NHE:
        vung = CHUNG | set(VUNG_THEM.get(k, ()))
        dd = doi is None or any(x in vung or x.startswith(("ops/cai_", "ops/cong_cu")) or ("/" not in x and x not in GOC) for x in doi)
        if BAT and ((CA == "hang_cuoi_lech" and doi == HANG_CUOI) or (CA == "hang_dau_lech" and doi is None)):
            dd = not dd
        kq[k] = ("day_du" if dd else "nhe",)
    return kq
def phan_chung():
    if not (BAT and CA == "thieu_nhan_chung"):
        open(".github/workflows/ci.yml").read()
    doc_ngoai()
    return not (BAT and CA == "phan_chung_sai")
'''
BO_GIA = _CHUNG_GIA + r'''
if not (BAT and CA == "thieu_nhan_chung"):
    open("ops/ci_provenance.py").read()
doc_ngoai()
print("TIEN TRINH: 1")
print("TONG: DO" if BAT and CA in ("bo_do", "bo_tong_do_rc0") else "TONG: DAT")
sys.exit(1 if BAT and CA in ("bo_do", "bo_rc") else 0)
'''
_PROBE = ("phan_chung_nguyen", "phan_chung_bon", "phan_chung_go")
_GOI = {"phan_chung_nguyen": "nguyen", "phan_chung_bon": "bon", "phan_chung_go": "go", "bo_day_du": "bo"}
# (ca, các phép áp dụng, kết luận kỳ vọng khi nhắm MỘT phép). Phép bị nhắm phải ra đúng kỳ vọng ở mức phép;
# mọi phép khác phải do_duoc và không ngoài vùng.
CA_KY_VONG = [("doc_thang", PHEP, NGOAI), ("doc_con", PHEP, NGOAI), ("doc_dirfd", PHEP, NGOAI), ("doc_alias", PHEP, NGOAI),
              ("con_I", PHEP, KDD), ("con_S", PHEP, KDD), ("con_E", PHEP, KDD), ("rc_sau", PHEP, KDD),
              ("log_rong", PHEP, KDD), ("thieu_nhan_chung", PHEP, KDD), ("doc_khong_theo_doi", PHEP, SACH),
              ("phan_chung_sai", _PROBE, KDD), ("hang_cuoi_lech", ("phan_chung_bon",), KDD),
              ("hang_dau_lech", ("phan_chung_bon",), KDD), ("bo_rc", ("bo_day_du",), KDD), ("bo_do", ("bo_day_du",), KDD),
              ("bo_tong_do_rc0", ("bo_day_du",), KDD)]


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


def _don_vi(loi):
    """Đơn vị của bộ phân loại: mỗi điều kiện, ở TỪNG phép; và tập phép đóng. Trả số ca đã chạy."""
    def nen():
        return [{"ten": t, "rc": 0, "doc_duoc": True, "bat_dau_goc": True, "bat_dau_con": 0, "python_con": 0,
                 "tap": {NHAN_CHUNG[t]}, "khong_giai": [], "ket": {"phan_chung": True, "hang_lech": [], "so_hang": SO_HANG},
                 "dong_cuoi": "TONG: DAT"} for t in PHEP]
    ca = [("khoe", None, {}, SACH)]
    for i, t in enumerate(PHEP):
        for ten, sua in (("rong", {"tap": set()}), ("khong_bat_dau", {"bat_dau_goc": False}), ("khong_giai", {"khong_giai": ["x"]}),
                         ("rc_none", {"rc": None}), ("rc_42", {"rc": 42}), ("python_khong_hook", {"python_con": 1}),
                         ("khong_doc_log", {"doc_duoc": False})):
            ca.append((f"{ten}@{t}", i, sua, KDD))
    for t in _PROBE:
        ca.append((f"thieu_probe_kq@{t}", PHEP.index(t), {"ket": None}, KDD))
    ca.append(("thieu_hang@phan_chung_bon", 1, {"ket": {"phan_chung": True, "hang_lech": [], "so_hang": SO_HANG - 1}}, KDD))
    ca.append(("python_co_hook@bo_day_du", 3, {"python_con": 2, "bat_dau_con": 2}, SACH))
    for ten, obs_f, ky in (("lap_bon_bo_go", lambda o: [o[0], o[1], o[1], o[3]], KDD), ("bon_lan_nguyen", lambda o: [o[0]] * 4, KDD),
                           ("thieu_go", lambda o: [o[0], o[1], o[3]], KDD), ("du_dao_thu_tu", lambda o: o[::-1], SACH)):
        kl, _ = phan_loai(obs_f(nen()), Z0)
        ok = kl == ky
        print(f"{'DAT' if ok else 'DO '} don_vi_{ten}: {kl} (ky vong {ky})")
        if not ok:
            loi.append("don_vi_" + ten)
    for ten, i, sua, ky in ca:
        obs = nen()
        if i is not None:
            obs[i].update(sua)
        kl, ct = phan_loai(obs, Z0)
        ok = kl == ky and all(c["do_duoc"] == (j != i or ky != KDD) for j, c in enumerate(ct))
        print(f"{'DAT' if ok else 'DO '} don_vi_{ten}: {kl} (ky vong {ky})")
        if not ok:
            loi.append("don_vi_" + ten)
    with tempfile.TemporaryDirectory() as td:  # bảng đổi một ô ⇒ ném
        rows = bang()
        rows[0][2] = "nhe"
        sai = os.path.join(td, "b.json")
        with open(sai, "w", encoding="utf-8") as f:
            json.dump(rows, f)
        try:
            bang(tep=sai)
            ok = False
        except ValueError:
            ok = len(bang()) == SO_HANG
    print(f"{'DAT' if ok else 'DO '} don_vi_bang_sai_bam")
    if not ok:
        loi.append("don_vi_bang_sai_bam")
    return 4 + len(ca) + 1


def tu_kiem():
    loi, dem = [], 0
    with tempfile.TemporaryDirectory() as td:
        root = os.path.join(td, "kho")
        tracked = dung_cay_gia(root)
        os.environ.pop("CA_PHEP", None)
        os.environ["CA_TU_KIEM"] = "khoe"
        os.makedirs(os.path.join(td, "ra"))
        kl, ct, _ = do_cay(root, os.path.join(td, "ra"), list(THEM_R7), tracked)
        ok = kl == SACH and all(c["do_duoc"] and not c["ngoai_vung"] for c in ct)
        dem += 1
        print(f"{'DAT' if ok else 'DO '} khoe: {kl}")
        if not ok:
            loi.append("khoe")
        for ca, cac_phep, ky in CA_KY_VONG:
            for t in cac_phep:
                out = os.path.join(td, f"ra-{ca}-{t}")
                os.makedirs(out)
                os.environ["CA_TU_KIEM"], os.environ["CA_PHEP"] = ca, _GOI[t]
                kl, ct, _ = do_cay(root, out, list(THEM_R7), tracked)
                theo = {c["ten"]: c for c in ct}
                dich = theo.get(t, {})
                ok_dich = (dich.get("do_duoc") is False) if ky == KDD else (dich.get("do_duoc") is True and bool(dich.get("ngoai_vung")) == (ky == NGOAI))
                ok_khac = all(c["do_duoc"] and not c["ngoai_vung"] for n, c in theo.items() if n != t)
                ok = kl == ky and ok_dich and ok_khac
                dem += 1
                print(f"{'DAT' if ok else 'DO '} {ca}@{t}: {kl} (ky vong {ky}) {dich.get('ly_do')}")
                if not ok:
                    loi.append(f"{ca}@{t}")
        os.environ.pop("CA_TU_KIEM", None)
        os.environ.pop("CA_PHEP", None)
    tong = dem + _don_vi(loi)
    print(f"TU_KIEM: {tong - len(loi)}/{tong} dat")
    return 0 if not loi else 1


DOT_BIEN = [  # (tên, tệp, chuỗi cũ, chuỗi mới) — chuỗi cũ phải xuất hiện đúng một lần trong phần MÃ (trước bảng này)
    ("bo_rc", "do_vung_pr2.py", 'if o["rc"] != 0:', "if False:"),
    ("nhan_quan_sat_rong", "do_vung_pr2.py", "if not tap:\n        ly_do.append", "if False:\n        ly_do.append"),
    ("bo_nhan_chung", "do_vung_pr2.py", "if tap and NHAN_CHUNG[ten] not in tap:", "if False:"),
    ("bo_bat_dau", "do_vung_pr2.py", 'if not o["bat_dau_goc"]:', "if False:"),
    ("bo_phan_chung_true", "do_vung_pr2.py", 'if ket.get("phan_chung") is not True:', "if False:"),
    ("bo_bang_lech", "do_vung_pr2.py", 'if ten == "phan_chung_bon" and (', "if False and ("),
    ("bo_hang_cuoi", "do_vung_pr2.py", "for n, d, e in bang():", "for n, d, e in bang()[:-1]:"),
    ("bo_so_hang_cuoi_van_dem", "do_vung_pr2.py", "if m.ke_hoach(d)[K][0] != e or oracle(d, Z) != e:",
     "if kq[\"so_hang\"] < SO_HANG and (m.ke_hoach(d)[K][0] != e or oracle(d, Z) != e):"),
    ("chay_bon_thay_go", "do_vung_pr2.py", "    for ten in PHEP:\n        log", "    for ten in (PHEP[0], PHEP[1], PHEP[1], PHEP[3]):\n        log"),
    ("bo_dem_hang", "do_vung_pr2.py", 'or ket.get("so_hang") != SO_HANG)', ")"),
    ("bo_tong_dat", "do_vung_pr2.py", 'if o.get("dong_cuoi") != "TONG: DAT":', "if False:"),
    ("bo_khong_giai", "do_vung_pr2.py", 'if o["khong_giai"]:', "if False:"),
    ("bo_dem_python_con", "do_vung_pr2.py", 'if o["bat_dau_con"] < o["python_con"]:', "if False:"),
    ("bo_doc_log", "do_vung_pr2.py", 'if not o["doc_duoc"]:', "if False:"),
    ("tap_phep_chi_dem", "do_vung_pr2.py", "if sorted(ten) != sorted(PHEP):", "if len(ten) != len(PHEP):"),
    ("bo_realpath", "hook/sitecustomize.py", '_ghi("THAT", that)', "pass"),
    ("khong_lan_truyen_con", "hook/sitecustomize.py", "_tl = threading.local()",
     "_tl = threading.local(); os.environ.pop('AUDIT_OPEN_LOG', None); os.environ.pop('PYTHONPATH', None)"),
    ("dirfd_giai_theo_cwd", "hook/sitecustomize.py", 'goc = os.readlink(f"/proc/self/fd/{dir_fd}")', "goc = os.getcwd()"),
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
            do = [d.split(":")[0][3:].strip() for d in r.stdout.splitlines() if d.startswith("DO ")]
            giet = r.returncode != 0 and bool(do)
            print(f"{'GIET' if giet else 'SONG'} {ten}: rc={r.returncode} ca_do={do}")
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
