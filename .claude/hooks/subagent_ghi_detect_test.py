"""Phan chung cho packet #329 pha 2 — may phat hien ghi cua subagent read-only.

Chay: python3 .claude/hooks/subagent_ghi_detect_test.py
Thoat 0 khi VA CHI KHI moi ca DAT va moi dot bien BI GIET.

Doc truoc khi sua: bo test nay do DETECTOR, khong do hook runtime cua nen. Ranh gioi ay
duoc ghi thang o `A10` cuoi tep — dung doc "22/22 dat" thanh "chot da co hieu luc that".
Moi ca dung cay git TAM (khong bao gio cham kho that), va anh chup di sang thu muc tam
RIENG qua `TL_SUBAGENT_SNAP_DIR`.
"""
import json
import os
import pathlib
import shutil
import subprocess
import sys
import tempfile

HERE = pathlib.Path(__file__).resolve().parent
HOOK = HERE / "subagent_ghi_detect.py"


def _cay():
    """Dung mot worktree git TAM co mot commit. Tra duong dan."""
    d = tempfile.mkdtemp(prefix="tl329-cay-")
    sh = lambda *a: subprocess.run(a, cwd=d, capture_output=True, text=True)
    sh("git", "init", "-q")
    sh("git", "config", "user.email", "t@t"); sh("git", "config", "user.name", "t")
    (pathlib.Path(d) / "a.txt").write_text("x\n", encoding="utf-8")
    sh("git", "add", "a.txt"); sh("git", "commit", "-qm", "khoi tao")
    (pathlib.Path(d) / ".gitignore").write_text(".tl_state/\n", encoding="utf-8")
    sh("git", "add", ".gitignore"); sh("git", "commit", "-qm", "ignore")
    return d


def goi(su_kien, agent, aid, cwd, snap, hook=None):
    """Tra (rc, ket_qua, ly_do). ket_qua=None khi hook khong in gi."""
    p = subprocess.run(
        [sys.executable, "-B", str(hook or HOOK)],
        input=json.dumps({"hook_event_name": su_kien, "agent_type": agent,
                          "agent_id": aid, "cwd": cwd}),
        capture_output=True, text=True,
        env={**os.environ, "TL_SUBAGENT_SNAP_DIR": snap})
    err = (p.stderr or "").strip()
    if not err:
        return p.returncode, None, ""
    try:
        d = json.loads(err.splitlines()[-1])
    except Exception:
        return p.returncode, "KHONG-PHAI-JSON", err[:200]
    return p.returncode, d.get("ket_qua"), d.get("ly_do", "")


def _snap():
    return tempfile.mkdtemp(prefix="tl329-snap-")


# ─────────────────────────── CA ───────────────────────────

def t1_khong_ghi_thi_clean(h):
    c, s = _cay(), _snap()
    goi("SubagentStart", "tl-auditor", "a1", c, s, h)
    rc, kq, _ = goi("SubagentStop", "tl-auditor", "a1", c, s, h)
    shutil.rmtree(c, ignore_errors=True)
    return (kq == "clean", f"khong ghi -> {kq} (mong doi clean)")


def t2_ghi_tep_theo_doi_thi_changed(h):
    c, s = _cay(), _snap()
    goi("SubagentStart", "tl-auditor", "a2", c, s, h)
    (pathlib.Path(c) / "moi.txt").write_text("agent da ghi\n", encoding="utf-8")
    rc, kq, _ = goi("SubagentStop", "tl-auditor", "a2", c, s, h)
    shutil.rmtree(c, ignore_errors=True)
    return (kq == "changed", f"ghi tep moi -> {kq} (mong doi changed)")


def t3_ghi_tep_BI_IGNORE_van_changed(h):
    """D3 — ly do DUY NHAT them `--ignored`. `.tl_state/` bi ignore, va do la noi duong
    ghi THAT da do duoc rot xuong. Khong co co ay thi ca nay bao `clean` VI LY DO SAI."""
    c, s = _cay(), _snap()
    goi("SubagentStart", "tl-auditor", "a3", c, s, h)
    d = pathlib.Path(c) / ".tl_state"; d.mkdir()
    (d / "reconcile_plan.json").write_text("{}\n", encoding="utf-8")
    rc, kq, _ = goi("SubagentStop", "tl-auditor", "a3", c, s, h)
    shutil.rmtree(c, ignore_errors=True)
    return (kq == "changed", f"ghi vao thu muc BI IGNORE -> {kq} (mong doi changed)")


def t4_sua_tep_da_theo_doi_thi_changed(h):
    c, s = _cay(), _snap()
    goi("SubagentStart", "tl-auditor", "a4", c, s, h)
    (pathlib.Path(c) / "a.txt").write_text("da bi sua\n", encoding="utf-8")
    rc, kq, _ = goi("SubagentStop", "tl-auditor", "a4", c, s, h)
    shutil.rmtree(c, ignore_errors=True)
    return (kq == "changed", f"sua tep -> {kq} (mong doi changed)")


def t5_thieu_anh_chup_la_UNKNOWN_khong_phai_clean(h):
    """`None != False`. Thieu phep do KHONG duoc doc thanh 'khong co gi'."""
    c, s = _cay(), _snap()
    rc, kq, _ = goi("SubagentStop", "tl-auditor", "a5", c, s, h)   # khong co Start
    shutil.rmtree(c, ignore_errors=True)
    return (kq == "unknown", f"Stop khong co Start -> {kq} (mong doi unknown)")


def t6_cwd_khong_phai_git_la_UNKNOWN(h):
    d = tempfile.mkdtemp(prefix="tl329-khonggit-")
    s = _snap()
    rc, kq, _ = goi("SubagentStart", "tl-auditor", "a6", d, s, h)
    shutil.rmtree(d, ignore_errors=True)
    return (kq == "unknown", f"cwd khong phai git -> {kq} (mong doi unknown)")


def t7_agent_ngoai_tap_khong_bi_ap_luat(h):
    """Doi KHONG CO ANH CHUP nao duoc tao, khong chi doi im lang. Ban dau ca nay chi kiem
    `ket_qua is None` — ma noi rong tap agent VAN cho `None` o duong Start thanh cong, nen
    dot bien `m11` song. Ban ghi tren dia la thu phan biet duoc hai truong hop."""
    c, s = _cay(), _snap()
    rc, kq, _ = goi("SubagentStart", "general-purpose", "a7", c, s, h)
    anh = len(list(pathlib.Path(s).glob("*.json")))
    shutil.rmtree(c, ignore_errors=True)
    return (kq is None and rc == 0 and anh == 0,
            f"agent ngoai tap -> ket_qua={kq} rc={rc} anh_chup={anh} (mong doi None/0/0)")


def t8_ca_hai_agent_deu_duoc_do(h):
    xau = []
    for i, a in enumerate(("tl-auditor", "tl-rasoat")):
        c, s = _cay(), _snap()
        goi("SubagentStart", a, f"a8{i}", c, s, h)
        (pathlib.Path(c) / "z.txt").write_text("w\n", encoding="utf-8")
        _, kq, _ = goi("SubagentStop", a, f"a8{i}", c, s, h)
        if kq != "changed":
            xau.append(f"{a}->{kq}")
        shutil.rmtree(c, ignore_errors=True)
    return (not xau, f"2 agent x ghi -> changed {2 - len(xau)}/2" + (f"; {xau}" if xau else ""))


def t9_trung_khoa_agent_id_la_UNKNOWN(h):
    c, s = _cay(), _snap()
    goi("SubagentStart", "tl-auditor", "a9", c, s, h)
    rc, kq, _ = goi("SubagentStart", "tl-auditor", "a9", c, s, h)   # Start lan hai
    shutil.rmtree(c, ignore_errors=True)
    return (kq == "unknown", f"Start trung agent_id -> {kq} (mong doi unknown)")


def t10_agent_id_doc_hai_bi_tu_choi(h):
    """`agent_id` di thang vao TEN TEP. Duong dan thoat khoi thu muc anh phai bi chan."""
    c, s = _cay(), _snap()
    xau = []
    for aid in ("../thoat", "a/b", "..", "."):
        rc, kq, _ = goi("SubagentStart", "tl-auditor", aid, c, s, h)
        if kq != "unknown":
            xau.append(f"{aid!r}->{kq}")
    shutil.rmtree(c, ignore_errors=True)
    return (not xau, f"agent_id doc hai -> unknown {4 - len(xau)}/4" + (f"; {xau}" if xau else ""))


def t11_sieu_du_lieu_lech_la_UNKNOWN(h):
    c, c2, s = _cay(), _cay(), _snap()
    goi("SubagentStart", "tl-auditor", "a11", c, s, h)
    rc, kq, _ = goi("SubagentStop", "tl-auditor", "a11", c2, s, h)   # cwd KHAC
    shutil.rmtree(c, ignore_errors=True); shutil.rmtree(c2, ignore_errors=True)
    return (kq == "unknown", f"cwd lech Start/Stop -> {kq} (mong doi unknown)")


def t11b_agent_type_lech_tren_CUNG_cay_la_UNKNOWN(h):
    """Tach rieng chot SIEU DU LIEU. `t11` dung HAI cay nen `top` da khac => chot `top`
    bat truoc va chot sieu du lieu khong bao gio duoc cham toi; dot bien `m7` song chinh
    vi vay. Ca nay giu NGUYEN cwd, chi doi `agent_type`."""
    c, s = _cay(), _snap()
    goi("SubagentStart", "tl-auditor", "a11b", c, s, h)
    rc, kq, _ = goi("SubagentStop", "tl-rasoat", "a11b", c, s, h)   # CUNG cwd, KHAC agent
    shutil.rmtree(c, ignore_errors=True)
    return (kq == "unknown", f"agent_type lech tren cung cay -> {kq} (mong doi unknown)")


def t12_anh_chup_KHONG_nam_trong_cay_dang_do(h):
    """Neu anh chup nam trong worktree thi may TU TAO dung thay doi ma no to cao."""
    c, s = _cay(), _snap()
    goi("SubagentStart", "tl-auditor", "a12", c, s, h)
    trong_cay = list(pathlib.Path(c).rglob("*.json"))
    _, kq, _ = goi("SubagentStop", "tl-auditor", "a12", c, s, h)
    shutil.rmtree(c, ignore_errors=True)
    return (not trong_cay and kq == "clean",
            f"anh chup trong cay={len(trong_cay)} (mong doi 0) · ket_qua={kq}")


def t13_index_byte_khong_doi_khi_chi_DOC(h):
    """A12 cua dac ta — `--no-optional-locks`. `git status` TRAN refresh stat data va GHI
    `.git/index` ma porcelain khong lo; thieu co ay thi chinh detector la mot duong ghi.

    PHAI lam BAN stat data truoc, khong thi khong tai hien duoc: tren mot cay vua tao,
    stat data da khop nen `git status` khong co gi de refresh va dot bien `m2` SONG. Ghi
    lai NGUYEN VAN noi dung cu roi day mtime len => stat lech, noi dung khong lech."""
    import time
    c, s = _cay(), _snap()
    a = pathlib.Path(c) / "a.txt"
    noi_dung = a.read_bytes()
    a.write_bytes(noi_dung)                       # noi dung Y HET, mtime MOI
    os.utime(a, (time.time() + 10, time.time() + 10))
    idx = pathlib.Path(c) / ".git" / "index"
    truoc = idx.read_bytes()
    goi("SubagentStart", "tl-auditor", "a13", c, s, h)
    goi("SubagentStop", "tl-auditor", "a13", c, s, h)
    sau = idx.read_bytes()
    shutil.rmtree(c, ignore_errors=True)
    return (truoc == sau, f"index byte doi={truoc != sau} (mong doi False)")


def t14_D1_chi_TO_CAO_khong_chan(h):
    """D1 da chot: CHI TO CAO. Ma thoat phai la 0 ke ca khi `changed` — mot ma khac 0 o
    day la CHAN, va hieu luc cua no CHUA AI DO (xem A10)."""
    c, s = _cay(), _snap()
    goi("SubagentStart", "tl-auditor", "a14", c, s, h)
    (pathlib.Path(c) / "w.txt").write_text("w\n", encoding="utf-8")
    rc, kq, _ = goi("SubagentStop", "tl-auditor", "a14", c, s, h)
    shutil.rmtree(c, ignore_errors=True)
    return (rc == 0 and kq == "changed", f"changed -> rc={rc} (mong doi 0), ket_qua={kq}")


def t15_bao_cao_KHAI_TEN_vung_MU(h):
    """Bao cao phai tu khai cai no KHONG thay. Khong khai = doc gia tuong da phu het."""
    c, s = _cay(), _snap()
    goi("SubagentStart", "tl-auditor", "a15", c, s, h)
    p = subprocess.run([sys.executable, "-B", str(h or HOOK)],
                       input=json.dumps({"hook_event_name": "SubagentStop",
                                         "agent_type": "tl-auditor", "agent_id": "a15",
                                         "cwd": c}),
                       capture_output=True, text=True,
                       env={**os.environ, "TL_SUBAGENT_SNAP_DIR": s})
    shutil.rmtree(c, ignore_errors=True)
    try:
        d = json.loads((p.stderr or "").strip().splitlines()[-1])
    except Exception:
        return (False, "khong doc duoc JSON bao cao")
    mu = (d.get("chi_tiet") or {}).get("MU") or []
    return (len(mu) >= 3, f"bao cao khai {len(mu)} vung MU (mong doi >= 3): {mu}")


def t16_delta_neu_ten_tep_NGUYEN_VAN_khong_phai_so_dem(h):
    c, s = _cay(), _snap()
    goi("SubagentStart", "tl-auditor", "a16", c, s, h)
    (pathlib.Path(c) / "dau-vet.txt").write_text("w\n", encoding="utf-8")
    p = subprocess.run([sys.executable, "-B", str(h or HOOK)],
                       input=json.dumps({"hook_event_name": "SubagentStop",
                                         "agent_type": "tl-auditor", "agent_id": "a16",
                                         "cwd": c}),
                       capture_output=True, text=True,
                       env={**os.environ, "TL_SUBAGENT_SNAP_DIR": s})
    shutil.rmtree(c, ignore_errors=True)
    return ("dau-vet.txt" in (p.stderr or ""),
            "bao cao co NEU TEN tep da doi" if "dau-vet.txt" in (p.stderr or "")
            else "bao cao KHONG neu ten tep — chi dem thi khong tra cuu duoc")


def t17_anh_chup_bi_don_sau_khi_dung(h):
    c, s = _cay(), _snap()
    goi("SubagentStart", "tl-auditor", "a17", c, s, h)
    con_truoc = len(list(pathlib.Path(s).glob("*.json")))
    goi("SubagentStop", "tl-auditor", "a17", c, s, h)
    con_sau = len(list(pathlib.Path(s).glob("*.json")))
    shutil.rmtree(c, ignore_errors=True)
    return (con_truoc == 1 and con_sau == 0,
            f"anh chup truoc Stop={con_truoc} sau Stop={con_sau} (mong doi 1 -> 0)")


def t18_HEAD_doi_giua_Start_va_Stop_la_UNKNOWN(h):
    c, s = _cay(), _snap()
    goi("SubagentStart", "tl-auditor", "a18", c, s, h)
    (pathlib.Path(c) / "b.txt").write_text("y\n", encoding="utf-8")
    subprocess.run(["git", "add", "b.txt"], cwd=c, capture_output=True)
    subprocess.run(["git", "-c", "user.email=t@t", "-c", "user.name=t",
                    "commit", "-qm", "commit giua chung"], cwd=c, capture_output=True)
    rc, kq, _ = goi("SubagentStop", "tl-auditor", "a18", c, s, h)
    shutil.rmtree(c, ignore_errors=True)
    return (kq == "unknown", f"HEAD doi -> {kq} (mong doi unknown — khong the so hai anh khac nen)")


CA = [t1_khong_ghi_thi_clean, t2_ghi_tep_theo_doi_thi_changed,
      t3_ghi_tep_BI_IGNORE_van_changed, t4_sua_tep_da_theo_doi_thi_changed,
      t5_thieu_anh_chup_la_UNKNOWN_khong_phai_clean, t6_cwd_khong_phai_git_la_UNKNOWN,
      t7_agent_ngoai_tap_khong_bi_ap_luat, t8_ca_hai_agent_deu_duoc_do,
      t9_trung_khoa_agent_id_la_UNKNOWN, t10_agent_id_doc_hai_bi_tu_choi,
      t11_sieu_du_lieu_lech_la_UNKNOWN, t11b_agent_type_lech_tren_CUNG_cay_la_UNKNOWN,
      t12_anh_chup_KHONG_nam_trong_cay_dang_do,
      t13_index_byte_khong_doi_khi_chi_DOC, t14_D1_chi_TO_CAO_khong_chan,
      t15_bao_cao_KHAI_TEN_vung_MU, t16_delta_neu_ten_tep_NGUYEN_VAN_khong_phai_so_dem,
      t17_anh_chup_bi_don_sau_khi_dung, t18_HEAD_doi_giua_Start_va_Stop_la_UNKNOWN]

# --- DOT BIEN: moi cai go DUNG MOT tinh chat, va phai lam it nhat mot ca DO ---
DOT_BIEN = [
    ("m1_bo_co_ignored",
     '"status", "--porcelain=v1", "-uall", "--ignored"',
     '"status", "--porcelain=v1", "-uall"'),
    ("m2_bo_no_optional_locks", '"git", "--no-optional-locks", "-C"', '"git", "-C"'),
    ("m3_thieu_anh_doc_thanh_clean",
     '_bao("unknown", "thieu anh chup cho agent_id nay", {"agent_id": aid})\n        return _MA_UNKNOWN',
     '_bao("clean", "khong co anh chup"); return 0'),
    ("m4_cho_agent_id_doc_hai",
     'if not aid or "/" in aid or "\\\\" in aid or aid in (".", ".."):',
     "if not aid:"),
    ("m5_bo_kiem_trung_khoa", "if dich.exists():", "if False:"),
    ("m6_bo_kiem_HEAD", 'if sau["head"] != truoc["head"]:', "if False:"),
    ("m7_bo_kiem_sieu_du_lieu",
     'if truoc.get("agent_type") != agent or truoc.get("cwd") != cwd:', "if False:"),
    # Dot bien nay ban dau nham nhanh `changed`, ma `t15` chay nhanh `clean` => no khong
    # bao gio duoc cham toi va SONG. Nay nham dung nhanh `clean`.
    ("m8_bo_khai_vung_MU",
     '_bao("clean", "khong thay doi nao trong cay quan sat duoc", {\n        "MU": ["ghi ngoai git top-level", "tac dung phu MANG",\n               "ghi roi hoan tac trong cung mot luot"]})',
     '_bao("clean", "khong thay doi nao trong cay quan sat duoc")'),
    ("m9_anh_chup_vao_TRONG_cay",
     'd = pathlib.Path(os.environ.get("TL_SUBAGENT_SNAP_DIR")',
     'd = pathlib.Path(os.environ.get("TL_SUBAGENT_SNAP_DIR_KHONG_TON_TAI")'),
    ("m10_bien_to_cao_thanh_CHAN", "_MA_CLEAN, _MA_CHANGED, _MA_UNKNOWN = 0, 0, 0",
     "_MA_CLEAN, _MA_CHANGED, _MA_UNKNOWN = 0, 2, 2"),
    ("m11_rong_tap_agent",
     '_AGENT = frozenset({"tl-auditor", "tl-rasoat"})',
     '_AGENT = frozenset({"tl-auditor", "tl-rasoat", "general-purpose"})'),
    ("m12_bo_don_anh_chup", 'dich.unlink(missing_ok=True)\n    return _MA_CLEAN',
     "return _MA_CLEAN"),
    ("m13_delta_rut_ve_so_dem", '"them": them, "mat": mat,',
     '"them": len(them), "mat": len(mat),'),
]


def chay():
    do = 0
    for f in CA:
        ok, msg = f(None)
        if not ok:
            do += 1
            print(f"  DO   {f.__name__:52} {msg}")
        else:
            print(f"  ok   {f.__name__:52} {msg}")
    goc = HOOK.read_text(encoding="utf-8")
    song = []
    print("--- DOT BIEN ---")
    with tempfile.TemporaryDirectory() as d:
        for ten, cu, moi in DOT_BIEN:
            cap = [(cu, moi)] if isinstance(cu, str) else list(zip(cu, moi))
            if any(c not in goc for c, _ in cap):
                print(f"  MOC KHONG CON TRONG MA: {ten} -> dot bien nay CHUA TUNG CHAY")
                song.append(ten)
                continue
            ma = goc
            for c, m in cap:
                ma = ma.replace(c, m, 1)
            tep = pathlib.Path(d) / f"hook_{ten}.py"
            tep.write_text(ma, encoding="utf-8")
            giet = [f.__name__ for f in CA if not f(tep)[0]]
            if giet:
                print(f"  GIET {ten:34} lam DO: {', '.join(giet[:3])}")
            else:
                print(f"  SONG {ten:34} KHONG ca nao do -> chot nay KHONG CO RANG")
                song.append(ten)
    tap_giet = len(DOT_BIEN) - len(song)
    print(f"TONG: CA {len(CA) - do}/{len(CA)} dat · DOT BIEN {tap_giet}/{len(DOT_BIEN)} bi giet")
    dat = (len(CA) > 0 and do == 0 and len(DOT_BIEN) > 0 and not song)
    print("TONG:", "DAT" if dat else "DO")
    # ── A10 — RANH GIOI CUA CHINH BO TEST NAY, khai o day chu khong giau trong PR ──
    print("A10 : hieu luc cua `SubagentStop` exit 2 tren nen — KHONG DO DUOC trong bo nay.")
    print("      Bo nay do DETECTOR bang payload tong hop; no KHONG chung minh hook that su")
    print("      duoc nen goi, cung khong chung minh ma thoat 2 co tac dung. Muon do phai")
    print("      phong mot subagent THAT. D1 (CHI TO CAO) chon chinh vi phep do ay chua co.")
    return 0 if dat else 1


if __name__ == "__main__":
    sys.exit(chay())
