"""Phan chung cho packet #329 pha 2 — may phat hien ghi cua subagent read-only.

Chay: python3 .claude/hooks/subagent_ghi_detect_test.py
Thoat 0 khi VA CHI KHI moi ca DAT va moi dot bien BI GIET.

Doc truoc khi sua: bo test nay do DETECTOR, khong do hook runtime cua nen. Ranh gioi ay
duoc ghi thang o `A10` cuoi tep — dung doc "N/N dat" thanh "chot da co hieu
luc that". (KHONG ghi so tong o day: no troi moi lan them ca, va ban truoc da noi "22/22"
trong khi runner in "24/24" — mot con so trong docstring khong the tu cap nhat.)
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


def _la_cau_hinh_pham_vi_lenh(k):
    """`GIT_CONFIG_COUNT` + `GIT_CONFIG_KEY_<n>`/`VALUE_<n>` — kenh cau hinh PHAM VI LENH."""
    if k == "GIT_CONFIG_COUNT":
        return True
    for tien_to in ("GIT_CONFIG_KEY_", "GIT_CONFIG_VALUE_"):
        # Xoa MOI cap danh so, khong chi nhung cap duoi `COUNT` hien tai: bo sot mot cap
        # roi de `COUNT` moi tro toi no con te hon khong xoa gi.
        if k.startswith(tien_to) and k[len(tien_to):].isdigit():
            return True
    return False


def _moi_truong_git_dong(env=None):
    """Moi truong KHONG doc cau hinh git ngoai nao. Nhan `env` lam DOI SO de `t22b` goi
    duoc voi mot nen THU DICH dung san — mot ham chi sua `os.environ` thi khong co cach
    nao cho no mot ca biet truoc dap an."""
    e = dict(os.environ if env is None else env)
    for k in [k for k in e if _la_cau_hinh_pham_vi_lenh(k)]:
        del e[k]
    e.update({"GIT_CONFIG_GLOBAL": os.devnull, "GIT_CONFIG_SYSTEM": os.devnull,
              "GIT_AUTHOR_NAME": "tl329", "GIT_AUTHOR_EMAIL": "tl329@invalid",
              "GIT_COMMITTER_NAME": "tl329", "GIT_COMMITTER_EMAIL": "tl329@invalid"})
    return e


def _cay(ten_con=None):
    """Dung mot worktree git TAM co mot commit. Tra duong dan.

    `ten_con` khac None => dung cay trong mot THU MUC CON mang ten ay. Them cho `t25`:
    khuyet tat #412 CHI can khi duong dan chua ky tu ngoai ASCII, ma `mkdtemp` luon cho
    ten thuan ASCII — nen mot ca dung `_cay()` tran KHONG THE do duoc no. Day dung la
    hinh dang "ca co MAT khac ca co DO".
    """
    d = tempfile.mkdtemp(prefix="tl329-cay-")
    if ten_con:
        d = str(pathlib.Path(d) / ten_con)
        pathlib.Path(d).mkdir()
    env = _moi_truong_git_dong()

    def sh(*a):
        # KIEM MA THOAT. Ban truoc dung `lambda` VUT ma thoat, nen mot buoc fixture hong
        # di qua im lang va ca do vi ly do KHONG lien quan gi toi detector.
        r = subprocess.run(a, cwd=d, capture_output=True, text=True, env=env)
        if r.returncode != 0:
            raise AssertionError(f"fixture hong o {' '.join(a)!r}: rc={r.returncode} "
                                 f"stderr={(r.stderr or '').strip()[:200]}")
        return r

    sh("git", "init", "-q")
    sh("git", "config", "user.email", "t@t"); sh("git", "config", "user.name", "t")
    # HERMETIC — VA BAN LUOT 2 CHI DUNG DUOC MOT NUA. Cross-review luot 2 do duoc:
    #   env COUNT=1 KEY_0=commit.gpgsign VALUE_0=true  ->  fixture commit rc=128
    # tuc cau hinh PHAM VI LENH THANG ca repo-local `git config` o duoi, va ghim khoa o
    # day khong cuu duoc. Ghim khoa cung la DANH SACH CAM: `core.hooksPath`, `include.path`,
    # `core.fsmonitor`, `merge.*` deu pha duoc fixture ma khong ai liet het.
    # DAO LAI: chan ca BA NGUON git doc cau hinh (system · global · pham vi lenh) —
    # tap NGUON la tap DONG va biet truoc; tap KHOA thu dich moi la thu vo han.
    # Container nay DANG dat `GIT_CONFIG_COUNT=3`, nen kenh ay khong phai gia dinh.
    # Ghim khoa GIU LAI lam lop hai: no vo hai va no noi ro y dinh.
    for k, v in (("commit.gpgsign", "false"), ("tag.gpgsign", "false"),
                 ("core.autocrlf", "false"), ("core.eol", "lf"), ("gc.auto", "0")):
        sh("git", "config", k, v)
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


# ── #412: DIEU KIEN DO DUOC cua khuyet tat codepage ───────────────────────────────────
# Khuyet tat #412 CHI bieu hien khi encoding mac dinh cua tien trinh KHAC utf-8. Tren Ubuntu
# CI ambient LA utf-8, nen `m20`/`m21`/`m22` hanh xu Y HET ban da va va SONG SOT — runner tinh
# mutant song la DO, tuc commit dung van lam cong Linux do. Cross-review codex bat dung ca nay
# tren PR #419 (P1), va ho da chay thu tung mutant duoi utf-8 de chung minh.
#
# Chua bang HAI lop, khong phai mot:
#   1. THU EP mot moi truong khong-utf8 cho tien trinh con (tren Linux `LC_ALL=C` cong
#      `PYTHONCOERCECLOCALE=0` cong `PYTHONUTF8=0` tat ca PEP 538/540);
#   2. DO xem ep co AN khong bang cach HOI CHINH tien trinh con, roi moi quyet dinh.
# Do 30-08-2026 tren Windows: ep KHONG doi gi (cp1258 truoc va sau) vi Windows dung ACP chu
# khong dung locale POSIX — nhung o do ambient DA khac utf-8 nen van do duoc. Nen phep quyet
# dinh phai la THUOC TINH DO DUOC ("con giai ma bang gi"), KHONG phai ten nen: mot may Windows
# dat UTF-8 code page phai bi tinh la KHONG DO DUOC, va mot may Linux ep duoc thi phai DO.
_EP_CODEPAGE = {"LC_ALL": "C", "LANG": "C", "PYTHONCOERCECLOCALE": "0", "PYTHONUTF8": "0"}
_PROBE_ENC = ("import codecs,locale;"
              "print(codecs.lookup(locale.getpreferredencoding(False)).name)")


def _encoding_cua_con(env):
    """HOI chinh tien trinh con no se giai ma bang gi. Khong suy tu ten nen."""
    try:
        r = subprocess.run([sys.executable, "-c", _PROBE_ENC],
                           capture_output=True, text=True, env=env, timeout=60)
    except (OSError, subprocess.SubprocessError):
        return ""
    return (r.stdout or "").strip()


def moi_truong_do_duoc_codepage():
    """Tra (env, encoding). env=None nghia la KHONG DO DUOC tren nen nay.

    Uu tien moi truong DA EP; neu ep khong an thi thu ambient; ca hai deu utf-8 thi chiu.
    """
    da_ep = {**os.environ, **_EP_CODEPAGE}
    enc = _encoding_cua_con(da_ep)
    if enc and enc != "utf-8":
        return da_ep, enc
    thuong = dict(os.environ)
    enc2 = _encoding_cua_con(thuong)
    if enc2 and enc2 != "utf-8":
        return thuong, enc2
    return None, (enc or enc2 or "(khong hoi duoc)")


def goi_byte(su_kien, agent, aid, cwd, snap, hook=None, env=None):
    """Nhu `goi` nhung gui stdin dang BYTE utf-8 va doc stderr dang BYTE.

    BAT BUOC cho `t25`, khong phai cho gon: `goi` dung `text=True`, nen Python MA HOA stdin
    bang encoding cua LOCALE (cp1258 tren may chu kho). Ky tu `o.` (U+1ECD) KHONG ma hoa
    duoc bang cp1258, nen CHINH BO TEST se nem UnicodeEncodeError truoc khi hook kip chay —
    ca se do vi ly do KHONG lien quan gi toi khuyet tat dang do. Harness that gui BYTE utf-8.

    Tra (rc, ket_qua, ly_do, chi_tiet).
    """
    tho = json.dumps({"hook_event_name": su_kien, "agent_type": agent,
                      "agent_id": aid, "cwd": cwd}, ensure_ascii=False).encode("utf-8")
    p = subprocess.run([sys.executable, "-B", str(hook or HOOK)], input=tho,
                       capture_output=True,
                       env={**(env if env is not None else os.environ),
                            "TL_SUBAGENT_SNAP_DIR": snap})
    err = p.stderr.decode("utf-8", "replace").strip()
    if not err:
        return p.returncode, None, "", {}
    try:
        d = json.loads(err.splitlines()[-1])
    except Exception:
        return p.returncode, "KHONG-PHAI-JSON", err[:200], {}
    return p.returncode, d.get("ket_qua"), d.get("ly_do", ""), (d.get("chi_tiet") or {})


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


def t4b_XOA_tep_da_theo_doi_thi_changed(h):
    """A4 — XOA cung la GHI. Cross-review luot 2: danh sach `CA` khong co ca nao dung
    tracked delete / rename / staged, nen ba dang GHI ay chua tung duoc nghiem thu."""
    c, s = _cay(), _snap()
    goi("SubagentStart", "tl-auditor", "a4b", c, s, h)
    (pathlib.Path(c) / "a.txt").unlink()
    rc, kq, _ = goi("SubagentStop", "tl-auditor", "a4b", c, s, h)
    shutil.rmtree(c, ignore_errors=True)
    return (kq == "changed", f"xoa tep da theo doi -> {kq} (mong doi changed)")


def t4c_DOI_TEN_tep_da_theo_doi_thi_changed(h):
    """A4 — doi ten sinh MOT ban ghi mat va MOT ban ghi them; ca hai deu la GHI."""
    c, s = _cay(), _snap()
    goi("SubagentStart", "tl-auditor", "a4c", c, s, h)
    (pathlib.Path(c) / "a.txt").rename(pathlib.Path(c) / "a-doi-ten.txt")
    rc, kq, _ = goi("SubagentStop", "tl-auditor", "a4c", c, s, h)
    shutil.rmtree(c, ignore_errors=True)
    return (kq == "changed", f"doi ten tep da theo doi -> {kq} (mong doi changed)")


def t4d_STAGE_thay_doi_thi_changed(h):
    """A4 — `git add` la GHI vao index. Ca nay do rieng duong STAGED: noi dung tep doi VA
    duoc dua vao index, nen porcelain doi tu ` M` sang `M `."""
    c, s = _cay(), _snap()
    goi("SubagentStart", "tl-auditor", "a4d", c, s, h)
    (pathlib.Path(c) / "a.txt").write_text("staged\n", encoding="utf-8")
    subprocess.run(["git", "add", "a.txt"], cwd=c, capture_output=True,
                   env=_moi_truong_git_dong())
    rc, kq, _ = goi("SubagentStop", "tl-auditor", "a4d", c, s, h)
    shutil.rmtree(c, ignore_errors=True)
    return (kq == "changed", f"stage thay doi -> {kq} (mong doi changed)")


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


def t19_de_len_tep_DA_CO_TRUOC_Start_van_changed(h):
    """P1 `status-on-dinh-che-giau-lan-ghi` (cross-review PR #342, DA TAI HIEN).

    Mot tep ignored DA co mat truoc Start bi GHI DE: dong porcelain KHONG doi, `.git/index`
    KHONG doi => ban truoc bao `clean` trong khi byte da khac. Do duoc: `TRUOC` ->
    `SAU-DA-BI-DE`, ket qua `clean`. Vung mu nam DUNG o `.tl_state/` — noi D3 vua mo ra."""
    c, sn = _cay(), _snap()
    d = pathlib.Path(c) / ".tl_state"; d.mkdir()
    (d / "plan.json").write_text("TRUOC\n", encoding="utf-8")      # TON TAI truoc Start
    goi("SubagentStart", "tl-auditor", "a19", c, sn, h)
    (d / "plan.json").write_text("SAU-DA-BI-DE\n", encoding="utf-8")  # GHI DE, cung trang thai
    rc, kq, _ = goi("SubagentStop", "tl-auditor", "a19", c, sn, h)
    shutil.rmtree(c, ignore_errors=True)
    return (kq == "changed", f"de len tep ignored da co -> {kq} (mong doi changed)")


def t19b_de_len_tep_UNTRACKED_da_co_van_changed(h):
    """Cung lop voi t19 nhung o trang thai `??` thay vi `!!` — de chot khong chi dung cho
    mot trang thai."""
    c, sn = _cay(), _snap()
    f = pathlib.Path(c) / "rac.txt"
    f.write_text("TRUOC\n", encoding="utf-8")
    goi("SubagentStart", "tl-auditor", "a19b", c, sn, h)
    f.write_text("SAU\n", encoding="utf-8")
    rc, kq, _ = goi("SubagentStop", "tl-auditor", "a19b", c, sn, h)
    shutil.rmtree(c, ignore_errors=True)
    return (kq == "changed", f"de len tep untracked da co -> {kq} (mong doi changed)")


def t20_duong_KHONG_bam_duoc_thi_UNKNOWN_khong_phai_clean(h):
    """`None != False`. Mot duong quan sat duoc ma KHONG noi-dung-hoa duoc thi khong duoc
    khang dinh `clean` — va bao cao phai GOI TEN no, khong dem.

    Dung tep VUOT TRAN, khong dung symlink va khong dung FIFO — ca hai deu KHONG toi duoc
    cho bam:
      · symlink VAN bam duoc (bam theo link target), nen khong sinh duong MU nao;
      · FIFO thi `git status --porcelain -uall --ignored` KHONG HE liet ke (do truc tiep:
        chi `?? to.bin` hien ra, `ong` bien mat) — nen no khong bao gio toi duoc ma bam.
    Tep vuot tran thi git CO liet ke va ma CO chay qua nhanh `qua tran`. Do la khac biet
    giua mot ca do DUONG DI va mot ca chi do y dinh."""
    c, sn = _cay(), _snap()
    (pathlib.Path(c) / "to.bin").write_bytes(b"\0" * (9 * 1024 * 1024))
    goi("SubagentStart", "tl-auditor", "a20", c, sn, h)
    p2 = subprocess.run([sys.executable, "-B", str(h or HOOK)],
                        input=json.dumps({"hook_event_name": "SubagentStop",
                                          "agent_type": "tl-auditor", "agent_id": "a20",
                                          "cwd": c}),
                        capture_output=True, text=True,
                        env={**os.environ, "TL_SUBAGENT_SNAP_DIR": sn})
    shutil.rmtree(c, ignore_errors=True)
    try:
        d = json.loads((p2.stderr or "").strip().splitlines()[-1])
    except Exception:
        return (False, "khong doc duoc JSON bao cao")
    mu = (d.get("chi_tiet") or {}).get("khong_bam_duoc") or []
    ok = d.get("ket_qua") == "unknown" and any("to.bin" in x for x in mu)
    return (ok, f"tep vuot tran -> {d.get('ket_qua')} · khong_bam_duoc={mu} "
                f"(mong doi unknown + co ten duong)")


_VAN_TAY_DA_IN = []      # in DUNG MOT LAN moi tien trinh — ly do o cuoi `t21`


def _bash_tuyet_doi():
    """Phan giai `bash` thanh DUONG DAN TUYET DOI truoc khi phong. `(duong, None)` hoac
    `(None, ly_do)` — KHONG bao gio im lang cho qua.

    Vi sao khong dung ten tran (do 03:5xZ 30-08-2026, job `99198878779`): tren Windows
    `subprocess.run(["bash", ...])` di qua `CreateProcess`, ma `CreateProcess` do THU MUC
    HE THONG (`System32`) TRUOC moi muc cua `PATH`. Runner `windows-latest` co
    `System32\\bash.exe` — VO WSL — nen ten tran phong ra vo WSL, in
    "Windows Subsystem for Linux has no installed distributions." ra STDOUT (khong phai
    stderr, va bang UTF-16) roi thoat 1 TRUOC khi lenh hook chay mot byte nao.

    Chinh su BAT DONG giua hai cach do la bang chung: `shutil.which("bash")` (do theo
    `PATH`) tra ve `C:\\Program Files\\Git\\bin\\bash.EXE`, con `CreateProcess` tra ve vo
    WSL. Hai ket qua khac nhau cho cung mot ten ⇒ day la TAO TAC CUA VO BOC, khong phai
    tinh chat cua lenh hook. Dung duong dan tuyet doi lam ca TRUNG THUC HON voi thu no
    von phai do: lenh hook co chay duoc duoi mot shell POSIX that hay khong. Day KHONG
    phai rut ruot ca — khang dinh van doi du `4/4`, xem `t21`.
    """
    duong = shutil.which("bash")
    if not duong:
        return None, "khong phan giai duoc `bash` tren PATH"
    if not pathlib.Path(duong).is_file():
        return None, f"`bash` phan giai ve {duong} nhung do khong phai mot tep"
    return duong, None


def _van_tay_nen_chay():
    """VAN TAY cua nen chay, TRA VE danh sach dong (khong tu in) — N5, packet #405.

    Vi sao ca nay tung KHONG chan doan duoc: no bat `capture_output` roi chi giu
    `stderr`, va tren `windows-latest` ca bon to hop cho `rc=1` voi `stderr` RONG.
    `stderr` rong khong phai "khong co loi" — no la KENH SAI. Ba manh duoi day la
    thu toi thieu de biet CAI GI dang chay:
      - `bash` phan giai ve dau (Git Bash hay `System32/bash.exe` vo WSL);
      - `bash --version`;
      - `stdout` cua chinh lenh hook.
    VANG MAT va RONG la hai ket luan khac nhau, nen chuoi rong van phai in ra chu.
    """
    duong = shutil.which("bash")
    ra = ["VANTAY bash-which  : " + (duong if duong else "KHONG TIM THAY")]
    # GOI HAI LAN CO CHU Y: ten tran (di qua `CreateProcess`) va duong dan tuyet doi.
    # Hai dong khac nhau CHINH LA con bo — xem `_bash_tuyet_doi`. Giu ca hai thi lan sau
    # ai doc log cung thay ngay, khong phai suy dien lai tu dau.
    for nhan, argv in (("bash-version    ", ["bash", "--version"]),
                       ("bash-version-abs", [duong, "--version"] if duong else None)):
        if argv is None:
            ra.append(f"VANTAY {nhan}: KHONG PHAN GIAI DUOC -> khong goi duoc")
            continue
        try:
            r = subprocess.run(argv, capture_output=True, text=True)
            dong = (r.stdout or "").split("\n")[0].strip()
            ra.append(f"VANTAY {nhan}: " + (dong if dong else "STDOUT RONG")
                      + f" (rc={r.returncode})")
        except OSError as e:
            ra.append(f"VANTAY {nhan}: KHONG GOI DUOC ({type(e).__name__}: {e})")
    return ra


def _van_tay_lenh(nhan, r):
    """rc + CA HAI kenh cua mot lan chay lenh hook. Rong thi NOI LA RONG."""
    out = (r.stdout or "").strip()
    err = (r.stderr or "").strip()
    return [f"VANTAY {nhan}: rc={r.returncode}",
            f"VANTAY {nhan}: stdout=" + (out[:400] if out else "RONG"),
            f"VANTAY {nhan}: stderr=" + (err[:400] if err else "RONG")]


def t21_lenh_hook_chay_duoc_khi_CLAUDE_PROJECT_DIR_KHONG_DAT(h, doi_lenh=None):
    """P1 `hook-khong-co-fallback-project-dir` (cross-review PR #342, DA TAI HIEN).

    `CLAUDE_PROJECT_DIR` KHONG duoc dat trong phien remote — chinh `CLAUDE.md:541` ghi lai
    phep do ay, va toi do lai trong phien nay: bien CHUA DAT. Lenh cu no thanh
    `/.claude/hooks/...` va thoat 2 TRUOC khi detector doc duoc payload.

    Ca nay doc lenh TU `.claude/settings.json` chu khong chep lai — chep lai la hai ban se
    troi lech, va ca se do mot dieu khong con dung.

    `doi_lenh` la moc cua KENH DOT BIEN THU BA (`DOT_BIEN_SETTINGS`): mot ham nhan chuoi
    lenh va tra ve ban da doi. Chi `_chay_dot_bien_settings` truyen no; nen that luon
    `None`. No ton tai de chinh ca nay CHUNG MINH duoc minh con do duoc."""
    goc = HERE.parent.parent
    bash, ly_do = _bash_tuyet_doi()
    if bash is None:
        return (False, f"KHONG DO DUOC: {ly_do} -> khong phong duoc lenh hook. Trang thai "
                       f"thu ba CO TEN: khong phan quyet duoc thi la DO, KHONG lam tron len.")
    d = json.loads((goc / ".claude" / "settings.json").read_text(encoding="utf-8"))
    van_tay = []
    xau = []
    for su_kien in ("SubagentStart", "SubagentStop"):
        nhom = (d.get("hooks") or {}).get(su_kien) or []
        if not nhom:
            xau.append(f"{su_kien}: CHUA DANG KY")
            continue
        lenh = nhom[0]["hooks"][0]["command"]
        if doi_lenh is not None:
            lenh = doi_lenh(lenh)
        for nhan, moi_truong in (("khong dat", {}),
                                 ("co dat", {"CLAUDE_PROJECT_DIR": str(goc)})):
            env = {k: v for k, v in os.environ.items() if k != "CLAUDE_PROJECT_DIR"}
            env.update(moi_truong)
            env["TL_SUBAGENT_SNAP_DIR"] = _snap()
            r = subprocess.run([bash, "-c", lenh], cwd=str(goc / ".claude" / "dev"),
                               input=json.dumps({"hook_event_name": "SubagentStart",
                                                 "agent_type": "tl-auditor",
                                                 "agent_id": f"t21{nhan}{su_kien}",
                                                 "cwd": str(goc)}),
                               capture_output=True, text=True, env=env)
            van_tay += _van_tay_lenh(f"{su_kien}/{nhan}", r)
            if r.returncode != 0:
                xau.append(f"{su_kien}/{nhan}: rc={r.returncode} "
                           f"stdout={(r.stdout or '').strip()[:80] or 'RONG'} "
                           f"stderr={(r.stderr or '').strip()[:80] or 'RONG'}")
    # IN VAN TAY CHI KHI CO TO HOP HONG. Ly do do duoc, khong phai gu thoi quen:
    # `get_job_logs` tra 500 dong tren `original_length: 1180` (do 21:5xZ 29-08-2026) va
    # cat o DAU. Bo test nay chay lai trong moi dot bien, nen in vo dieu kien sinh 266
    # dong — du de day chinh bang chung can doc ra khoi cua so con lai. Chan doan chi co
    # gia tri o luot HONG; o luot xanh no la nhieu nuot mat tin hieu.
    # HAI cua chan, do 04:3xZ 30-08-2026 tren mot cay CO DOT BIEN THAT:
    #   · `doi_lenh` khac None  -> DO la ket qua MONG DOI, van tay khong chan doan gi;
    #   · `_VAN_TAY_DA_IN`      -> bo CA chay LAI trong TUNG dot bien `DOT_BIEN`, nen mot
    #     `t21` do sinh 19 khoi x 17 dong = 333 dong. RIENG no da vuot cua so 500 dong ma
    #     `get_job_logs` tra ve (do: `original_length: 1904` -> 500 dong), tuc chinh phep
    #     chan doan day bang chung can doc ra khoi cua so. In MOT lan la du: ca 19 khoi
    #     giong het nhau.
    if xau and doi_lenh is None and not _VAN_TAY_DA_IN:
        _VAN_TAY_DA_IN.append(1)
        for dong in _van_tay_nen_chay() + van_tay:
            print(dong)
    return (not xau, f"lenh hook chay duoc o 2 su kien x 2 nen -> dung {4 - len(xau)}/4"
                     + (f"; SAI: {xau}" if xau else ""))


def t23_doi_ten_anh_chup_la_UNKNOWN(h):
    """Cross-review luot 2: Start `A`, doi ten `A.json` -> `B.json`, Stop `B` => `clean`.

    Khoa noi nam trong TEN TEP, ma ten tep la thu ke khac doi duoc. Nay `agent_id` phai
    nam TRONG anh chup va bi doi chieu o Stop.

    NOI RO PHAM VI: day KHONG phai bien toan ven — ke doi duoc ten thi cung sua duoc noi
    dung. No dong dung MOT ca: doi ten thuan tuy. Ca rong hon van mo, xem `A11`.
    """
    c, s = _cay(), _snap()
    goi("SubagentStart", "tl-auditor", "a23", c, s, h)
    cu = pathlib.Path(s) / "a23.json"
    if not cu.is_file():
        shutil.rmtree(c, ignore_errors=True)
        return (False, f"fixture hong: khong thay anh chup {cu}")
    cu.rename(pathlib.Path(s) / "b23.json")
    rc, kq, ly = goi("SubagentStop", "tl-auditor", "b23", c, s, h)
    shutil.rmtree(c, ignore_errors=True)
    return (kq == "unknown", f"Stop tren anh chup DOI TEN -> {kq} (mong doi unknown) {ly[:60]}")


def t24_index_cua_LINKED_WORKTREE_van_duoc_dinh_vi(h):
    """`<top>/.git/index` KHONG ton tai trong linked worktree — `.git` o do la mot TEP.

    Ban truoc dung `is_file()` nen van tay thanh RONG trong IM LANG: mat mot chot ma
    khong ai biet. Nay hoi `git rev-parse --git-path index`, va khong hoi duoc thi GOI TEN
    vao danh sach MU chu khong tra chuoi rong.
    """
    c, s = _cay(), _snap()
    wt = tempfile.mkdtemp(prefix="tl329-wt-")
    env = _moi_truong_git_dong()
    r = subprocess.run(["git", "worktree", "add", "--detach", wt, "HEAD"],
                       cwd=c, capture_output=True, text=True, env=env)
    if r.returncode != 0:
        shutil.rmtree(c, ignore_errors=True)
        return (True, f"KHONG DO DUOC: khong dung duoc linked worktree ({r.returncode})")
    if (pathlib.Path(wt) / ".git").is_dir():
        shutil.rmtree(c, ignore_errors=True)
        return (True, "KHONG DO DUOC: `.git` cua worktree la THU MUC -> khong phai ca can do")
    goi("SubagentStart", "tl-auditor", "a24", wt, s, h)
    anh = pathlib.Path(s) / "a24.json"
    ok, ly = False, "khong thay anh chup"
    if anh.is_file():
        d = json.loads(anh.read_text(encoding="utf-8"))
        vt = d.get("index_sha256_16", "")
        mu = [x for x in d.get("mu_noi_dung", []) if str(x).startswith("<index>")]
        # DOI VAN TAY THAT, khong chap nhan "MU cung duoc". Ban dau toi viet
        # `bool(vt) or bool(mu)` va dot bien `m18` (quay ve ghep chuoi `<top>/.git/index`)
        # SONG SOT: trong linked worktree duong ay khong ton tai, nen no roi vao nhanh MU
        # va ca van xanh. Tuc ca do "khong im lang" chu khong do "dinh vi dung" — chinh
        # cai no sinh ra de do. MU chi la loi thoat khi that su khong hoi duoc git.
        ok = bool(vt)
        ly = f"van_tay_index={vt!r} mu_index={mu}"
    shutil.rmtree(c, ignore_errors=True)
    shutil.rmtree(wt, ignore_errors=True)
    return (ok, f"linked worktree: {ly}")


# ── PHEP CHAM DIEM, tach thanh HAM THUAN de co the do duoc ──────────────────────────────
# Ban luot 2 kiem hai chot nay bang cach TIM CHUOI trong chinh tep nguon cua no. Ca hai
# chuoi ay nam trong literal cua chinh cau `if` di tim chung, nen phep kiem LUON XANH du
# runner co con logic hay khong — cross-review luot 2 do duoc: tren ban sao bo han nhanh
# tu choi, `t22` van `ok` va runner van in diem.
#
# Cung MOT LOP loi voi `MOC_MO_HO_CO_SAN` cua PR #343: mot phep kiem tu bao ve minh bang
# chinh thu can duoc bao ve. Duong ra giong het: tach VI TU khoi DU LIEU, cho no nhan doi
# so, roi cho no mot ca BIET TRUOC DAP AN. Khong tim chuoi trong ma nua.
# ── #412: BA DOT BIEN NAY CHI DO DUOC KHI NEN KHAC utf-8 ─────────────────────────────
# Chung lat nguoc dung duong giai ma, nen duoi utf-8 ban da va va ban chua va cho KET QUA
# Y HET — mutant SONG SOT ma khong chung minh duoc gi. Neu de nguyen thi commit DUNG van lam
# cong Linux DO (cross-review codex, P1 tren PR #419, ho da chay thu tung mutant duoi utf-8).
#
# BA trang thai, khong phai hai: GIET · SONG · KHONG DO DUOC. Trang thai thu ba KHONG duoc
# tinh la giet (khong thoi phong diem) va KHONG tinh la song (khong lam do gia), nhung PHAI
# duoc GOI TEN va noi ro no duoc do o dau — mot ca lang le bo qua la mot cong khong ton tai.
_DOT_BIEN_PHU_THUOC_CODEPAGE = frozenset({
    "m20_git_tro_lai_text_True",
    "m21_git_giai_ma_bang_LOCALE_thay_vi_utf8",
    "m22_stdin_tro_lai_json_load",
})


def phan_loai_dot_bien(ten, env_cp):
    """`"khong_do_duoc"` hoac `"do_duoc"`. Ham THUAN, nhan `env_cp` lam DOI SO chu khong tu
    hoi moi truong — de `t26` goi duoc voi mot ca biet truoc dap an. Mot vi cham diem chi
    song trong `main()` thi khong ca nao cham toi, va no se am tham troi."""
    if ten in _DOT_BIEN_PHU_THUOC_CODEPAGE and env_cp is None:
        return "khong_do_duoc"
    return "do_duoc"


def giet_duoc(do_san, ket_qua):
    """Ca bi dot bien GIET = PASS o NEN ma FAIL o MUTANT. Hieu so, khong phai tap tho.

    `do_san`  : ten cac ca DA DO o nen.
    `ket_qua` : {ten_ca: dat_hay_khong} khi chay tren mutant.
    """
    return sorted(t for t, ok in ket_qua.items() if t not in do_san and not ok)


def duoc_cong_bo_diem(do_san):
    """Nen do thi KHONG duoc cong bo ty le dot bien.

    Mot ty le tinh tren nen do khong phai "so nho hon su that" — no KHONG CO NGHIA, va in
    no ra la moi nguoi doc nham.
    """
    return not do_san


def t25_duong_dan_NGOAI_ASCII_van_bam_duoc_noi_dung(h):
    """#412 loi B — CA HAI duong giai ma (`sys.stdin` va `_git`) phai doc utf-8 TUONG MINH.

    CHOT BAT BUOC, chep tu #412: ca nay PHAI chay tren duong dan CO KY TU NGOAI ASCII. Tren
    duong dan ASCII khuyet tat VO HINH, nen mot ca dat o `/tmp/abc` se XANH ma KHONG DO GI.

    Phu HAI lop ky tu, va su khac nhau ay la CO THAT chu khong phai trang tri:
      MEO      `o'`(U+1ED1) `o.`(U+1ED9)  -> byte tiep dien 0x91 0x99, cp1258 CO dinh nghia
                                            => giai ma sai AM THAM, khong nem.
      O_TRONG  `o.`(U+1ECD) `e`(U+1EC1)   -> byte 0x8d 0x81 la O TRONG cua cp1258
                                            => `strict` NEM; `surrogateescape` cho surrogate.
    Dung mot minh "Quoc hoi" la chi cham lop MEO, tuc do HUT mot nua.

    KHANG DINH BANG SO, KHONG bang `rc`: `_MA_CLEAN`, `_MA_CHANGED`, `_MA_UNKNOWN` deu bang 0
    (D1 = CHI TO CAO), nen `rc` la 0 KE CA KHI MU. Hai so la tieu chi:
        so_duong_da_bam_noi_dung > 0        so duong MU == 0
    Ve so thu hai: `clean` CHI dat toi duoc khi `mu_nd` rong — nhanh fail-close ngay tren no
    tra `unknown` neu con bat ky duong nao khong bam duoc. Nen `ket_qua == "clean"` CHINH LA
    phep khang dinh "0 duong MU"; khi ca do, thong diep in ra danh sach `khong_bam_duoc` that
    de nguoi doc thay so ay chu khong phai doan.
    """
    env, enc = moi_truong_do_duoc_codepage()
    for nhan, lop in (("Quốc hội", "MEO"), ("Học ề ọ", "O_TRONG")):
        c, s = _cay(nhan), _snap()
        # PHAI co it nhat MOT duong xuat hien trong `git status` o CA HAI anh chup, neu
        # khong thi `noi_dung` rong va `so_duong_da_bam_noi_dung` bang 0 — ca se DO du ban
        # va DUNG. Do duoc khi viet ca nay: cay `_cay()` tran la cay SACH, status rong.
        # Tep nay co TRUOC Start va KHONG doi toi Stop => ket qua van `clean`, nhung duong
        # ay duoc bam noi dung, dung thu ca dang khang dinh.
        # Dat duoi `.tl_state/` vi no bi ignore, va D3 mo `--ignored` chinh cho vung nay.
        (pathlib.Path(c) / ".tl_state").mkdir(exist_ok=True)
        (pathlib.Path(c) / ".tl_state" / "ke-hoach.json").write_text(
            '{"x": 1}' + chr(10), encoding="utf-8")
        goi_byte("SubagentStart", "tl-auditor", "a25" + lop, c, s, h, env=env)
        rc, kq, ly, ct = goi_byte("SubagentStop", "tl-auditor", "a25" + lop, c, s, h,
                                  env=env)
        shutil.rmtree(c, ignore_errors=True)
        if kq != "clean":
            mu = (ct.get("khong_bam_duoc") or [])
            return (False, f"[{lop}] duong dan ngoai ASCII -> {kq}; so duong MU={len(mu)} "
                           f"(mong doi ket_qua=clean, MU=0); ly do: {ly[:100]}")
        bam = ct.get("so_duong_da_bam_noi_dung")
        if not isinstance(bam, int) or bam <= 0:
            return (False, f"[{lop}] so_duong_da_bam_noi_dung={bam!r} (mong doi > 0) — "
                           "cay do duoc nhung khong bam noi dung duong nao")
    return (True, "ca hai lop ky tu duoi encoding %r: bam noi dung > 0, 0 duong MU"
                  % enc)


def t26_dot_bien_phu_thuoc_codepage_khong_bi_tinh_la_SONG(h):
    """Trang thai THU BA cua cham diem dot bien phai TU NO duoc do.

    Vi sao ca nay ton tai: `m20`/`m21`/`m22` lat nguoc duong giai ma, nen duoi utf-8 ban da va
    va ban chua va cho ket qua Y HET va mutant SONG SOT. Runner tinh mutant song la DO ⇒ commit
    DUNG van lam cong Linux do (cross-review codex, P1 tren PR #419). Ba trang thai — GIET ·
    SONG · KHONG DO DUOC — la cach chua, nhung mot vi cham diem KHONG CO CA NAO CHAM TOI thi
    se am tham troi. Nen ca nay do CHINH vi cham diem ay, khong do detector.

    Hai chieu, va can ca hai: nen utf-8 ⇒ ba dot bien ay `khong_do_duoc`; nen khac utf-8 ⇒
    `do_duoc`. Thieu chieu thu hai thi mot vi "luon tra khong_do_duoc" van qua — tuc chot mat
    rang va moi dot bien codepage se duoc tha vinh vien.
    """
    loi = []
    for ten in sorted(_DOT_BIEN_PHU_THUOC_CODEPAGE):
        if phan_loai_dot_bien(ten, None) != "khong_do_duoc":
            loi.append(f"{ten}: nen utf-8 (env=None) phai la khong_do_duoc")
        if phan_loai_dot_bien(ten, {"LC_ALL": "C"}) != "do_duoc":
            loi.append(f"{ten}: nen khac utf-8 phai la do_duoc")
    # Dot bien KHONG thuoc tap ay thi KHONG BAO GIO duoc tha, ke ca tren nen utf-8.
    for ten, _, _ in DOT_BIEN:
        if ten in _DOT_BIEN_PHU_THUOC_CODEPAGE:
            continue
        if phan_loai_dot_bien(ten, None) != "do_duoc":
            loi.append(f"{ten}: khong phu thuoc codepage ma bi tha tren nen utf-8")
    if loi:
        return (False, "; ".join(loi[:3]))
    return (True, f"3 trang thai dung: {len(_DOT_BIEN_PHU_THUOC_CODEPAGE)} dot bien duoc tha "
                  f"DUNG tren nen utf-8, {len(DOT_BIEN) - len(_DOT_BIEN_PHU_THUOC_CODEPAGE)} "
                  f"dot bien khac KHONG bao gio duoc tha")


def t22_cham_diem_dot_bien_CO_RANG(h):
    """Ca BIET TRUOC DAP AN cho hai ham tren — bon chieu, ca tha lan to."""
    xau = []
    if giet_duoc({"a"}, {"a": False, "b": False}) != ["b"]:
        xau.append("`giet_duoc` khong loai ca DA DO o nen")
    if giet_duoc(set(), {"a": False, "b": True}) != ["a"]:
        xau.append("`giet_duoc` khong bat ca PASS-nen FAIL-mutant")
    if giet_duoc(set(), {"a": True, "b": True}) != []:
        xau.append("`giet_duoc` to oan khi mutant khong lam do ca nao")
    if duoc_cong_bo_diem(set()) is not True:
        xau.append("nen SACH ma khong cho cong bo")
    if duoc_cong_bo_diem({"a"}) is not False:
        xau.append("nen DO ma van cho cong bo")
    return (not xau, "phep cham diem dung o 5 chieu" if not xau else f"SAI: {xau}")


def t22b_fixture_KHONG_an_cau_hinh_git_ngoai(h):
    """Ca BIET TRUOC DAP AN cho `_moi_truong_git_dong`, HAI CHIEU.

    Khong co chieu DOI CHUNG thi ca nay xanh ca khi ham co lap la mot `pass` — vi nen cua
    may dang chay co the von da lanh. Chieu doi chung chung minh nen thu dich THAT SU giet
    duoc commit; chi khi ay chieu con lai moi noi len dieu gi.
    """
    thu = {"GIT_CONFIG_COUNT": "1", "GIT_CONFIG_KEY_0": "commit.gpgsign",
           "GIT_CONFIG_VALUE_0": "true"}

    def commit_thu(env):
        d = tempfile.mkdtemp(prefix="tl329-gitcfg-")
        for a in (["init", "-q"], ["config", "user.email", "t@t"],
                  ["config", "user.name", "t"]):
            subprocess.run(["git", *a], cwd=d, capture_output=True, env=env)
        (pathlib.Path(d) / "a.txt").write_text("x\n", encoding="utf-8")
        subprocess.run(["git", "add", "a.txt"], cwd=d, capture_output=True, env=env)
        r = subprocess.run(["git", "commit", "-qm", "x"], cwd=d, capture_output=True,
                           text=True, env=env)
        return r.returncode

    ban = dict(os.environ, **thu, GIT_CONFIG_GLOBAL=os.devnull,
               GIT_CONFIG_SYSTEM=os.devnull)
    if commit_thu(ban) == 0:
        return (True, "KHONG DO DUOC: nen thu dich van commit duoc (may nay thieu gpg?) "
                      "-> chieu doi chung vo nghia, khong ket luan gi")
    rc = commit_thu(_moi_truong_git_dong(ban))
    return (rc == 0, "cat duoc CA BA nguon cau hinh git"
                     if rc == 0 else f"cau hinh PHAM VI LENH van lot: rc={rc}")


CA = [t1_khong_ghi_thi_clean, t2_ghi_tep_theo_doi_thi_changed,
      t3_ghi_tep_BI_IGNORE_van_changed, t4_sua_tep_da_theo_doi_thi_changed,
      t4b_XOA_tep_da_theo_doi_thi_changed, t4c_DOI_TEN_tep_da_theo_doi_thi_changed,
      t4d_STAGE_thay_doi_thi_changed,
      t5_thieu_anh_chup_la_UNKNOWN_khong_phai_clean, t6_cwd_khong_phai_git_la_UNKNOWN,
      t7_agent_ngoai_tap_khong_bi_ap_luat, t8_ca_hai_agent_deu_duoc_do,
      t9_trung_khoa_agent_id_la_UNKNOWN, t10_agent_id_doc_hai_bi_tu_choi,
      t11_sieu_du_lieu_lech_la_UNKNOWN, t11b_agent_type_lech_tren_CUNG_cay_la_UNKNOWN,
      t12_anh_chup_KHONG_nam_trong_cay_dang_do,
      t13_index_byte_khong_doi_khi_chi_DOC, t14_D1_chi_TO_CAO_khong_chan,
      t15_bao_cao_KHAI_TEN_vung_MU, t16_delta_neu_ten_tep_NGUYEN_VAN_khong_phai_so_dem,
      t17_anh_chup_bi_don_sau_khi_dung, t18_HEAD_doi_giua_Start_va_Stop_la_UNKNOWN,
      # --- luot 2: BA P1 cua cross-review codex tren PR #342 ---
      t19_de_len_tep_DA_CO_TRUOC_Start_van_changed,
      t19b_de_len_tep_UNTRACKED_da_co_van_changed,
      t20_duong_KHONG_bam_duoc_thi_UNKNOWN_khong_phai_clean,
      t21_lenh_hook_chay_duoc_khi_CLAUDE_PROJECT_DIR_KHONG_DAT,
      t22_cham_diem_dot_bien_CO_RANG, t22b_fixture_KHONG_an_cau_hinh_git_ngoai,
      t23_doi_ten_anh_chup_la_UNKNOWN,
      t24_index_cua_LINKED_WORKTREE_van_duoc_dinh_vi,
      # --- #412 loi B: giai ma utf-8 tuong minh o ca hai duong ---
      t25_duong_dan_NGOAI_ASCII_van_bam_duoc_noi_dung,
      t26_dot_bien_phu_thuoc_codepage_khong_bi_tinh_la_SONG]

# --- DOT BIEN: moi cai go DUNG MOT tinh chat, va phai lam it nhat mot ca DO ---
DOT_BIEN = [
    # --- #412 loi B: MOI duong va co MOT dot bien RIENG. Hai duong hong DOC LAP nhau,
    # nen mot dot bien chung se khong phan biet duoc duong nao con rang.
    # --- #412 loi B: MOI duong co MOT dot bien RIENG, va moi dot bien la mot ban LUI
    # TRUNG THANH ve ma TRUOC khi va — KHONG phai mot sua doi mot phan.
    # DA TRA GIA khi viet ca nay: ban dau `m22` chi thay DONG giai ma va giu lai doan doc
    # byte o tren, nen mutant doc het stdin roi moi goi `json.load(sys.stdin)` tren mot
    # luong DA CAN. No chet vi stdin RONG, khong phai vi codepage — dung hinh dang TIN
    # DUNG GIA cua #355/#359: dot bien BI GIET nhung khong bi giet DUNG LY DO. `m20` cung
    # vay: doi mot minh loi goi sang `text=True` thi dong duoi con `.decode()` tren mot
    # `str` => `AttributeError`, cung la mot cai chet VO CAN.
    ("m20_git_tro_lai_text_True",
     '''capture_output=True, timeout=120)
    except (OSError, subprocess.SubprocessError) as e:
        return 128, "loi goi git: %s" % e
    return p.returncode, p.stdout.decode("utf-8", "surrogateescape")''',
     '''capture_output=True, text=True, timeout=120)
    except (OSError, subprocess.SubprocessError) as e:
        return 128, "loi goi git: %s" % e
    return p.returncode, p.stdout'''),
    ("m21_git_giai_ma_bang_LOCALE_thay_vi_utf8",
     '''p.stdout.decode("utf-8", "surrogateescape")''',
     '''p.stdout.decode(__import__("locale").getpreferredencoding(False),
                     "surrogateescape")'''),
    ("m22_stdin_tro_lai_json_load",
     '''        luong = getattr(sys.stdin, "buffer", None)
        if luong is not None:
            tho = luong.read()
        else:
            tho = sys.stdin.read().encode(sys.stdin.encoding or "utf-8", "surrogateescape")
        data = json.loads(tho.decode("utf-8"))''',
     '''        data = json.load(sys.stdin)'''),
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
    # MO NEO DOI o luot 3: cau `if` nay duoc them ve `agent_id`, nen moc cu chet. GIU dot
    # bien va RETARGET — mot dot bien mat moc la mot phep do KHONG CHAY, va no bao "SONG"
    # y het mot chot khong co rang. `m17` nham RIENG ve `agent_id`; `m7` van nham CA cau.
    ("m7_bo_kiem_sieu_du_lieu",
     '    if (truoc.get("agent_type") != agent or truoc.get("cwd") != cwd\n'
     '            or truoc.get("agent_id") != aid):',
     "    if False:"),
    # Dot bien nay ban dau nham nhanh `changed`, ma `t15` chay nhanh `clean` => no khong
    # bao gio duoc cham toi va SONG. Nay nham dung nhanh `clean`.
    # Moc cu bien mat khi nhanh `clean` them `so_duong_da_bam_noi_dung` (luot 2). Neo lai
    # vao chinh khoa `MU` — ngan hon va it troi hon.
    ("m8_bo_khai_vung_MU",
     '        "MU": ["ghi ngoai git top-level", "tac dung phu MANG",\n               "ghi roi hoan tac trong cung mot luot"]})',
     '        })'),
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
    # --- luot 2: dot bien cho ba chot moi ---
    ("m14_bo_bam_noi_dung", "    noi_dung, mu = _van_tay_noi_dung(top, st)",
     "    noi_dung, mu = {}, []"),
    ("m15_bo_so_sanh_noi_dung",
     "    doi_noi_dung = sorted(k for k in set(nd_t) & set(nd_s) if nd_t[k] != nd_s[k])",
     "    doi_noi_dung = []"),
    ("m16_duong_MU_doc_thanh_clean", "    if mu_nd:", "    if False:"),
    ("m13_delta_rut_ve_so_dem", '"them": them, "mat": mat,',
     '"them": len(them), "mat": len(mat),'),
    # Bo rang buoc `agent_id` trong NOI DUNG anh chup -> doi ten tep lai qua duoc.
    ("m17_bo_rang_buoc_agent_id", '            or truoc.get("agent_id") != aid):',
     "            or False):"),
    # Quay ve ghep chuoi `<top>/.git/index` -> linked worktree mat van tay TRONG IM LANG.
    ("m18_index_ghep_chuoi_top_git_index",
     '    rc_idx, duong_idx = _git(cwd, "rev-parse", "--git-path", "index")',
     '    rc_idx, duong_idx = 0, ".git/index"'),
]


# ── DOT BIEN NHAM CHINH BO TEST NAY ─────────────────────────────────────────────────────
# `DOT_BIEN` o tren chi sua TEP SAN PHAM (`HOOK`), nen no khong the chung minh rang cac
# chot cua CHINH runner co rang. Ban luot 2 lap khoang trong ay bang cach TIM CHUOI trong
# ma — va do la cach mot phep kiem tu bao ve minh bang chinh thu can duoc bao ve. Nay ba
# chot ay co dot bien THAT: sua ban sao CUA TEP NAY, chay lai nhu mot tien trinh rieng, va
# doi ca dich phai hien `DO`.
DOT_BIEN_NHAM_TEST = [
    ("mt1_giet_khong_loai_do_san",
     "    return sorted(t for t, ok in ket_qua.items() if t not in do_san and not ok)\n",
     "    return sorted(t for t, ok in ket_qua.items() if not ok)\n",
     "t22_cham_diem_dot_bien_CO_RANG"),
    ("mt2_cong_bo_du_NEN_DO",
     "    return not do_san\n",
     "    return True  # dot bien: cong bo diem ke ca khi nen do\n",
     "t22_cham_diem_dot_bien_CO_RANG"),
    ("mt3_bo_cat_kenh_pham_vi_lenh",
     "    for k in [k for k in e if _la_cau_hinh_pham_vi_lenh(k)]:\n        del e[k]\n",
     "    pass  # dot bien: bo sot kenh cau hinh pham vi lenh\n",
     "t22b_fixture_KHONG_an_cau_hinh_git_ngoai"),
]


# ── DOT BIEN NHAM `.claude/settings.json` — KENH THU BA ─────────────────────────────────
# Do 04:2xZ 30-08-2026: `DOT_BIEN` chi sua TEP SAN PHAM (`HOOK`), `DOT_BIEN_NHAM_TEST` chi
# sua TEP TEST. KHONG kenh nao cham toi `.claude/settings.json` — nghia la bat bien ma
# `t21` sinh ra de canh (nhanh du phong `CLAUDE_PROJECT_DIR` NGAY TRONG lenh hook) truoc
# nay KHONG AI CANH. Rut ruot `t21` thi khong phep do nao trong kho doi mau, va "ca xanh"
# se doc thanh "bat bien con day" trong khi hai chuyen ay da roi nhau.
DOT_BIEN_SETTINGS = [
    ("ms1_bo_nhanh_du_phong_project_dir",
     '[ -n "$D" ] || D="$(git rev-parse --show-toplevel 2>/dev/null)"; '
     '[ -n "$D" ] || D="$PWD"; ',
     "",
     "t21_lenh_hook_chay_duoc_khi_CLAUDE_PROJECT_DIR_KHONG_DAT"),
]


def _chay_dot_bien_settings():
    """Tra danh sach dot bien SONG (khong lam ca dich do). Rong = chot co rang.

    Ap dot bien len CHUOI LENH DA PHAN GIAI tu JSON, KHONG len van ban JSON tho: moc o do
    khong troi theo cach escape dau nhay. Moc khong khop DUNG MOT CHO tren CA HAI su kien
    thi khai SONG chu khong im — mot moc troi bao "SONG" y het mot chot khong co rang,
    trong khi that ra dot bien CHUA TUNG CHAY, va do la benh "ca co MAT khac ca co DO".
    """
    d = json.loads((HERE.parent.parent / ".claude" / "settings.json")
                   .read_text(encoding="utf-8"))
    lenh = [n["hooks"][0]["command"]
            for su in ("SubagentStart", "SubagentStop")
            for n in ((d.get("hooks") or {}).get(su) or [])[:1]]
    song = []
    for ten, cu, moi, dich in DOT_BIEN_SETTINGS:
        if len(lenh) != 2 or any(x.count(cu) != 1 for x in lenh):
            print(f"  MOC KHOP {[x.count(cu) for x in lenh]} CHO (mong doi [1, 1]): {ten} "
                  f"-> dot bien nay KHONG do gi")
            song.append(ten)
            continue
        try:
            ok, msg = globals()[dich](None, doi_lenh=lambda c: c.replace(cu, moi, 1))
        except Exception as e:                       # ban dot bien no = ca dich CHET
            ok, msg = False, f"{type(e).__name__}: {e}"
        if not ok:
            print(f"  GIET {ten:34} lam DO: {dich} ({msg[:60]})")
        else:
            print(f"  SONG {ten:34} KHONG lam do {dich} -> chot nay KHONG CO RANG")
            song.append(ten)
    return song


def _chay_dot_bien_nham_test():
    """Tra danh sach dot bien SONG (khong lam ca dich do). Rong = ca ba chot co rang.

    NAP BAN DOT BIEN BANG `exec`, KHONG spawn tien trinh con — va day la lan sua thu BA
    cua chinh cho nay, nen ghi lai ly do:
      · chep 1 tep vao temp  -> ban sao khong thay `HOOK`, `t21` chet;
      · chep 2 tep phang     -> `FileNotFoundError: /tmp/.claude/settings.json`;
      · chep them settings   -> `FileNotFoundError: .../.claude/dev`.
    Ca ba lan suite CHET TRUOC khi toi ca dich, va ca ba lan bang ket qua in ra `SONG` —
    tuc "chot khong co rang" — trong khi that ra dot bien CHUA TUNG CHAY. Dung benh
    "ca co MAT khac ca co DO", va no gia dang thanh mot phat hien.
    Duong ra khong phai chep them tep: la BO tien trinh con di. `exec` voi `__file__` tro
    ve THU MUC HOOK THAT thi moi duong dan trong ban sao deu giai dung, va `__name__` khac
    `"__main__"` nen `sys.exit(chay())` o cuoi tep khong chay — chi ca dich chay.
    """
    goc = pathlib.Path(__file__).read_text(encoding="utf-8")
    song = []
    for ten, cu, moi, dich in DOT_BIEN_NHAM_TEST:
        if goc.count(cu) != 1:
            print(f"  MOC KHOP {goc.count(cu)} CHO: {ten} -> dot bien nay KHONG do gi")
            song.append(ten)
            continue
        ns = {"__file__": __file__, "__name__": f"tl329_mutant_{ten}"}
        try:
            exec(compile(goc.replace(cu, moi, 1), f"<{ten}>", "exec"), ns)
            ok, msg = ns[dich](None)
        except Exception as e:                       # ban dot bien no = ca dich CHET
            ok, msg = False, f"{type(e).__name__}: {e}"
        if not ok:
            print(f"  GIET {ten:34} lam DO: {dich} ({msg[:60]})")
        else:
            print(f"  SONG {ten:34} KHONG lam do {dich} -> chot nay KHONG CO RANG")
            song.append(ten)
    return song


def chay():
    do_san = set()          # ca DA DO o NEN — doc chu thich duoi truoc khi sua
    do = 0
    for f in CA:
        ok, msg = f(None)
        if not ok:
            do += 1
            do_san.add(f.__name__)
            print(f"  DO   {f.__name__:52} {msg}")
        else:
            print(f"  ok   {f.__name__:52} {msg}")
    goc = HOOK.read_text(encoding="utf-8")
    song = []
    khong_do = []
    # ── DOT BIEN CHI CO NGHIA KHI NEN XANH ───────────────────────────────────────────────
    # Ban truoc dem `giet = [f for f in CA if not f(tep)[0]]` — KHONG he tham chieu `do_san`.
    # Nen khi nen do, MOI dot bien "giet" tam thuong bang chinh cac ca da do san, va runner
    # in `13/13 bi giet` NGAY CANH `CA 10/19 dat`. Cross-review codex tren PR #342 do duoc
    # dung cap so ay.
    # Hai chot, can CA HAI:
    #   1. "giet" chi tinh ca PASS o nen ma FAIL o mutant — HIEU SO, khong phai tap tho;
    #   2. nen do thi TU CHOI cong bo diem dot bien. Mot ty le tinh tren nen do khong phai
    #      "so nho hon su that" — no KHONG CO NGHIA, va in no ra la moi nguoi doc nham.
    # Dung bai hoc "dot bien bi giet boi mot ca DA DO thi phep do ay vo nghia" ma packet
    # #336 phai ap BANG TAY tung luot; nay may cuong che.
    print("--- DOT BIEN ---")
    with tempfile.TemporaryDirectory() as d:
        env_cp, enc_cp = moi_truong_do_duoc_codepage()
        for ten, cu, moi in DOT_BIEN:
            if phan_loai_dot_bien(ten, env_cp) == "khong_do_duoc":
                print(f"  KHONG DO DUOC {ten:30} nen giai ma bang {enc_cp!r}; khuyet tat #412"
                      f" khong bieu hien duoi utf-8 -> do o lane windows")
                khong_do.append(ten)
                continue
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
            giet = giet_duoc(do_san, {f.__name__: f(tep)[0] for f in CA})
            if giet:
                print(f"  GIET {ten:34} lam DO: {', '.join(giet[:3])}")
            else:
                print(f"  SONG {ten:34} KHONG ca nao do -> chot nay KHONG CO RANG")
                song.append(ten)
    # Dot bien nham CHINH bo test — chi co nghia khi nen xanh, y het tap tren.
    song_test = []
    song_st = []
    if duoc_cong_bo_diem(do_san) and "TL329_KHONG_LAP" not in os.environ:
        print("--- DOT BIEN NHAM BO TEST ---")
        song_test = _chay_dot_bien_nham_test()
        song.extend(song_test)
        print("--- DOT BIEN NHAM settings.json ---")
        song_st = _chay_dot_bien_settings()
        song.extend(song_st)
    # `tap_giet` co Y CHI dem rieng `DOT_BIEN`: hai kenh kia co bo dem rieng, cong chung
    # vao mot ty le se lam con so `18/18` cua nen troi ma khong ai biet vi sao.
    tap_giet = (len(DOT_BIEN) - len(khong_do) - len(song)
                + len(song_test) + len(song_st))
    if not duoc_cong_bo_diem(do_san):
        print(f"TONG: CA {len(CA) - do}/{len(CA)} dat")
        print(f"TONG: DIEM DOT BIEN BI TU CHOI — nen co {len(do_san)} ca DO SAN "
              f"({', '.join(sorted(do_san)[:3])}{'...' if len(do_san) > 3 else ''}). "
              f"Sua nen xanh truoc, roi moi doc duoc so dot bien.")
    else:
        print(f"TONG: CA {len(CA) - do}/{len(CA)} dat · "
              f"DOT BIEN {tap_giet}/{len(DOT_BIEN) - len(khong_do)} bi giet"
              + (f" · {len(khong_do)} KHONG DO DUOC tren nen nay" if khong_do else ""))
    if khong_do:
        # Goi TEN, va noi ro do o DAU. "Khong do duoc" khac "dat"; giau no di la bien mot
        # cho mu thanh mot con so dep.
        print("TONG: KHONG DO DUOC tren nen nay: " + ", ".join(sorted(khong_do)))
        print("      Ba dot bien ay lat nguoc duong giai ma, chi phan biet duoc khi encoding")
        print("      mac dinh KHAC utf-8. Lane `windows` cua `ci.yml` la noi chung duoc do.")
    dat = (len(CA) > 0 and do == 0 and len(DOT_BIEN) > 0 and not song)
    print("TONG:", "DAT" if dat else "DO")
    # ── A10 — RANH GIOI CUA CHINH BO TEST NAY, khai o day chu khong giau trong PR ──
    print("A10 : hieu luc cua `SubagentStop` exit 2 tren nen — KHONG DO DUOC trong bo nay.")
    print("      Bo nay do DETECTOR bang payload tong hop; no KHONG chung minh hook that su")
    print("      duoc nen goi, cung khong chung minh ma thoat 2 co tac dung. Muon do phai")
    print("      phong mot subagent THAT. D1 (CHI TO CAO) chon chinh vi phep do ay chua co.")
    # ── NO CO TEN, khai o DAY chu khong giau trong PR ────────────────────────────────────
    # Cross-review luot 2 (PR #342) doi bon tieu chi; luot 3 dong duoc HAI, con HAI khong
    # dong duoc bang mot ca test va noi thang vi sao, thay vi de trong.
    print("NO  : `snapshot-ngoai-cay-KHONG-co-bien-toan-ven` — anh chup nam NGOAI cay nhung")
    print("      subagent VAN ghi de duoc no. `agent_id` nay da nam TRONG anh chup (t23),")
    print("      nhung do la chot chong DOI TEN, khong phai bien toan ven: ke sua duoc tep")
    print("      thi sua duoc ca truong ay. Bien toan ven that doi mot KHOA ma subagent")
    print("      khong doc duoc, va D1 khong co thu ay. Khong va bang bam dai hon.")
    print("NO  : `A3/A8/A11-chua-co-ca-dong` — `install`, `tl nlm-reconcile`, ghi NGOAI kho,")
    print("      mo phong mang: bo nay dung payload TONG HOP nen khong dieu khien duoc mot")
    print("      agent THAT lam nhung viec ay. Ba dang GHI cua A4 (xoa · doi ten · staged)")
    print("      DA co ca rieng tu luot 3 — xem t4b/t4c/t4d.")
    return 0 if dat else 1


if __name__ == "__main__":
    sys.exit(chay())
