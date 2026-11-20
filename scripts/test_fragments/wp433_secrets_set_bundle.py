# -*- coding: utf-8 -*-
"""wp433 — `secrets-set` (`tl_gws.py`): bundle giải mã không phải object ⇒ rc 3 ngay sau giải mã, TRƯỚC mọi cờ/export/canary;
`token` không phải str ⇒ coi như thiếu, không lấy repr làm khoá public (spec SECRETS-SET-BUNDLE-KIEU r1).
Mọi lượt chạy trên bản `tl_gws` nạp TRONG BỘ NHỚ (nguồn thật hoặc đột biến), HOME/TL_* tạm, dữ liệu GIẢ; mọi hàm tải/ghi/mạng là
đồ giả CÓ ĐẾM (`_gas` giả ném lỗi), `encrypt` bọc để ghi khoá. Đột biến chỉ GIẾT khi ca ném `TinHieuChotCa` đúng (ca, lượt, nhãn);
đột biến 1–2 còn đòi đúng CƠ CHẾ (rc 5 + `TypeError` phát sinh ở câu gán `--gas-token`) — bảng `_DB` chép §4b của spec."""
import argparse, contextlib, io, json, os, pathlib, shutil, subprocess, sys, tempfile, types, urllib.request  # noqa: E401
TEST_ID = "wp433_secrets_set_bundle"
_MK = "wp433-ss-master-gia-0123456789abcdefghijklmnop"   # >= 32 ký tự; KHÔNG phải khoá thật
_DONG = "[secrets-set] ✗ dữ liệu không hợp lệ: bundle"
_GIA = (("fetch", "_secrets_fetch"), ("upload", "_secrets_upload"), ("stage_enc", "_stage_enc_upload"), ("gws_export", "_gws_export_cred"),
        ("nlm_refresh", "_refresh_nlm_auth"), ("canary", "_nlm_files_after_live_canary"), ("gas", "_gas"))
_KIEU = (("list", [1, 2]), ("str", "chuoi"), ("int", 7), ("null", None), ("true", True))
_TOKEN = (("list", [1]), ("dict", {"a": 1}), ("int", 7))
_CO = {"gas_token": dict(gas_token="tok-moi"), "webapp": dict(webapp="https://gia.invalid/exec"), "gws": dict(gws=True), "nlm": dict(nlm=True), "khong_co": {}}
_HOP_LE = {"token": "tok-cu", "webappUrl": "u"}
_LUOT_DU_KIEN = {  # sổ lượt viết RIÊNG khỏi hàm ca: ca chạy thiếu/thừa/sai thứ tự một lượt ⇒ đỏ `so_luot`
    "kieu": ("kieu.list.gas_token kieu.list.webapp kieu.list.gws kieu.list.nlm kieu.list.khong_co kieu.str.gas_token kieu.str.webapp kieu.str.gws "
             "kieu.str.nlm kieu.str.khong_co kieu.int.gas_token kieu.int.webapp kieu.int.gws kieu.int.nlm kieu.int.khong_co kieu.null.gas_token "
             "kieu.null.webapp kieu.null.gws kieu.null.nlm kieu.null.khong_co kieu.true.gas_token kieu.true.webapp kieu.true.gws kieu.true.nlm "
             "kieu.true.khong_co").split(),
    "token_kieu": "token_kieu.list.gws token_kieu.list.nlm token_kieu.dict.gws token_kieu.dict.nlm token_kieu.int.gws token_kieu.int.nlm".split(),
    "hoi_quy": "hoi_quy.gas_token hoi_quy.webapp hoi_quy.gws hoi_quy.nlm hoi_quy.khong_co hoi_quy.env_token.gws".split(),
}
_HQ = {  # spec §0 (3), chép cứng: lượt → (rc, fetch, gas, upload, stage_enc, gws_export, nlm_refresh, canary, khoá public)
    "hoi_quy.gas_token": (0, 1, 0, 1, 0, 0, 0, 0, []), "hoi_quy.webapp": (0, 1, 0, 1, 0, 0, 0, 0, []),
    "hoi_quy.gws": (0, 1, 0, 1, 1, 1, 0, 0, ["tok-cu"]), "hoi_quy.nlm": (0, 1, 0, 1, 1, 0, 1, 1, ["tok-cu"]),
    "hoi_quy.khong_co": (1, 1, 0, 0, 0, 0, 0, 0, []), "hoi_quy.env_token.gws": (0, 1, 0, 1, 1, 1, 0, 0, ["tok-env"]),
}
class TinHieuChotCa(AssertionError):
    def __init__(self, ca, luot, nhan, qs=None):
        super().__init__("%s · %s · %s" % (ca, luot, nhan)); self.ca, self.luot, self.nhan, self.qs = ca, luot, nhan, qs  # noqa: E702
def _nem(e):
    raise e
def _nap(nguon, tl_module, goc, store):
    """`compile`+`exec` nguồn vào module MỚI rồi `bind`; thay đường tải/ghi/mạng bằng đồ giả CÓ ĐẾM (`m.dem`), `encrypt` ghi khoá vào
    `m.khoa`, `_safe_exc` bọc để GHI frame cuối của ngoại lệ (tên hàm, có thuộc module này không, dòng nguồn đã strip) vào `m.vt`."""
    m = types.ModuleType("wp433ss_tl_gws"); m.__file__ = goc.__file__  # noqa: E702
    exec(compile(nguon, goc.__file__, "exec"), m.__dict__)
    m.bind(tl_module)
    m.dem, m.khoa, m.vt, m.blob, dong, that_imp, that_safe = {}, [], [], None, nguon.splitlines(), m._imp, m._safe_exc
    tra = {"fetch": lambda a, fid: (m.blob, "gia"), "upload": ("fid-gia", None), "stage_enc": None, "gws_export": b'{"cred":"gia"}', "nlm_refresh": True,
           "canary": ({"auth.json": "gia"}, 0, None), "gas": lambda: _nem(RuntimeError("MANG_BI_CHAN"))}
    def gia(ten, ham):
        def f(*a, **k):
            m.dem[ten] += 1
            return tra[ten](*a, **k) if callable(tra[ten]) else tra[ten]
        setattr(m, ham, f)
    for ten, ham in _GIA:
        gia(ten, ham)
    def safe(exc):
        tb = exc.__traceback__
        while tb is not None and tb.tb_next is not None:
            tb = tb.tb_next
        if tb is not None:
            m.vt.append((tb.tb_frame.f_code.co_name, tb.tb_frame.f_globals is m.__dict__, dong[tb.tb_lineno - 1].strip()))
        return that_safe(exc)
    proxy = types.SimpleNamespace(encrypt=lambda data, key: (m.khoa.append(key), store.encrypt(data, key))[1], decrypt=store.decrypt)
    m._safe_exc, m._imp = safe, lambda n: proxy if n == "gws_cred_store" else that_imp(n)
    m._nlm_auth_files, m._nlm_auth_age_days, m.load_creds = (lambda: {"auth.json": 1}), (lambda n: None), (lambda *a, **k: None)
    return m
class _Rig:
    """Một ca trên một bản nạp `m`; mỗi LƯỢT có thư mục tạm, HOME/USERPROFILE/TL_*/cwd riêng, khôi phục khi ra."""
    def __init__(self, m, ca, store):
        self.m, self.ca, self.store, self.da, self.dat, self.ten, self.q = m, ca, store, [], 0, "-", None
    def luot(self, ten, bundle_obj, co, env_token=None):
        """Một lượt `cmd_secrets_set`: chặn tiến trình con/mạng (`MANG_BI_CHAN`), stdout/stderr RIÊNG; trả quan sát (rc, bộ đếm, khoá, stderr, vt)."""
        m = self.m
        self.ten = ten; self.da.append(ten)  # noqa: E702
        m.dem, m.khoa, m.vt = dict.fromkeys((t for t, _h in _GIA), 0), [], []
        m.blob = self.store.encrypt(json.dumps(bundle_obj).encode("utf-8"), _MK)
        td, cu_env, cu_cwd, out, err = tempfile.mkdtemp(prefix="wp433ss-"), dict(os.environ), os.getcwd(), io.StringIO(), io.StringIO()
        cu = (subprocess.run, subprocess.Popen, urllib.request.urlopen)
        try:
            for k in [k for k in os.environ if k.startswith("TL_")]:
                os.environ.pop(k)
            os.environ.update(HOME=td, USERPROFILE=td, TL_MASTER_KEY=_MK, **({"TL_TOKEN": env_token} if env_token else {}))
            os.chdir(td)
            subprocess.run = subprocess.Popen = urllib.request.urlopen = lambda *a, **k: _nem(RuntimeError("MANG_BI_CHAN"))
            a = argparse.Namespace(secrets_id="fid-gia", config=None, profile=None, gas_token=None, webapp=None, gws=False, nlm=False,
                                   no_public=False, folder=None, secrets_file=None, env=None)
            for k, v in co.items():
                setattr(a, k, v)
            with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
                rc = m.cmd_secrets_set(a)
        finally:
            subprocess.run, subprocess.Popen, urllib.request.urlopen = cu
            os.chdir(cu_cwd); os.environ.clear(); os.environ.update(cu_env); shutil.rmtree(td, ignore_errors=True)  # noqa: E702
        self.q = types.SimpleNamespace(rc=rc, dem=dict(m.dem), khoa=list(m.khoa), err=err.getvalue().splitlines(), vt=list(m.vt))
        return self.q
    def xs(self, **nhan):
        """Hậu điều của lượt vừa chạy, theo thứ tự khai: nhãn đỏ ĐẦU TIÊN thành tín hiệu (mang kèm quan sát của lượt)."""
        for n, dk in nhan.items():
            if not dk:
                raise TinHieuChotCa(self.ca, self.ten, n, self.q)
        self.dat += 1
def kieu(r):
    for kt, kv in _KIEU:
        for ct, cv in _CO.items():
            q = r.luot("kieu.%s.%s" % (kt, ct), kv, cv)
            r.xs(rc3=q.rc == 3, dong=q.err == [_DONG],
                 khong_goi=q.dem == dict(dict.fromkeys((t for t, _h in _GIA), 0), fetch=1) and q.khoa == [])
def token_kieu(r):
    for tt, tv in _TOKEN:
        for ct in ("gws", "nlm"):
            q = r.luot("token_kieu.%s.%s" % (tt, ct), {"token": tv, "webappUrl": "u"}, _CO[ct])
            r.xs(rc0=q.rc == 0, upload1=q.dem["upload"] == 1, khong_public=q.dem["stage_enc"] == 0 and set(q.khoa) <= {_MK},
                 canh_bao=sum("thiếu webapp token" in d for d in q.err) == 1 and not any("✗" in d for d in q.err))
def hoi_quy(r):
    def bang(q):
        return (q.rc, *(q.dem[t] for t in ("fetch", "gas", "upload", "stage_enc", "gws_export", "nlm_refresh", "canary")), [k for k in q.khoa if k != _MK])
    for ct, cv in _CO.items():
        q = r.luot("hoi_quy." + ct, dict(_HOP_LE), cv)
        r.xs(bang=bang(q) == _HQ[r.ten])
    q = r.luot("hoi_quy.env_token.gws", {"token": [1], "webappUrl": "u"}, _CO["gws"], env_token="tok-env")
    r.xs(bang=bang(q) == _HQ[r.ten])
_CA = (kieu, token_kieu, hoi_quy)
_M1_NEU = "    if not isinstance(bundle, dict):   # WP433 SS: không phải object ⇒ từ chối như giải mã lỗi, TRƯỚC mọi cờ/export/canary\n"
_M1_IN = '        print("[secrets-set] ✗ dữ liệu không hợp lệ: bundle", file=sys.stderr)\n'
_M1 = _M1_NEU + _M1_IN + "        return 3\n"
_M2 = '_tok = os.environ.get("TL_TOKEN") or (_bt if isinstance(_bt, str) else "")'
_GAN = 'bundle["token"] = a.gas_token; changed.append("token")'      # câu gán ĐẦU TIÊN vào bundle ở cờ --gas-token (spec §0, §4b)
_VAO = '    _entry_nb = os.environ.get("TL_NOTEBOOK_ID")      # WP714: ghim TRƯỚC load_creds của lệnh\n    return _nlm_contained("secrets-set"'
_L0 = ("kieu", "kieu.list.gas_token", "rc3")
_DB = (  # §4b: (đột biến, [(neo khớp ĐÚNG MỘT lần, thay)…], ca đích, lượt, nhãn, đòi cơ chế TypeError-đúng-vị-trí)
    ("db_bo_kiem_kieu", [(_M1, "")], *_L0, True),
    ("db_kieu_chi_list", [(_M1_NEU, _M1_NEU.replace("isinstance(bundle, dict)", "isinstance(bundle, (dict, str))"))], "kieu", "kieu.str.gas_token", "rc3", True),
    ("db_kieu_thong_diep", [(_M1_IN, _M1_IN.replace("dữ liệu không hợp lệ: bundle", "giải mã lỗi: bundle"))], "kieu", "kieu.list.gas_token", "dong", False),
    ("db_token_repr", [(_M2, '_tok = os.environ.get("TL_TOKEN") or str(bundle.get("token") or "")')], "token_kieu", "token_kieu.list.gws", "khong_public", False),
)
_TU_KIEM = (  # §4b: bộ phân hạng KHÔNG được cấp tín dụng — (tên, cặp, ca, lượt, nhãn, đòi cơ chế, hạng mong đợi)
    ("tu_kiem_a_attributeerror", [(_M1, _M1_NEU + '        raise AttributeError("wp433-tu-kiem")\n')], *_L0, True, "TIN_DUNG_GIA"),
    ("tu_kiem_a2_typeerror_vo_can", [(_M1, _M1_NEU + "        len(7)\n")], *_L0, True, "TIN_DUNG_GIA"),
    ("tu_kiem_b_except_doi_kieu", [(_VAO, "    try:\n        os.environ.wp433_khong_co\n    except AttributeError as e:\n"
                                    "        raise AssertionError(type(e).__name__)\n" + _VAO)], *_L0, False, "TIN_DUNG_GIA"),
    ("tu_kiem_c_chu_thich", [(_M1_NEU, "    # vô hại\n" + _M1_NEU)], *_L0, False, "SONG_SOT"),
    # phản chứng bộ đo (PC1, PC2): mỗi cái phải ĐỎ đúng chỗ, còn nguồn thật đạt lượt ấy
    ("pc1_dong_stderr_thua", [(_M1_IN, _M1_IN + '        print("[secrets-set] xem thêm", file=sys.stderr)\n')], "kieu", "kieu.list.gas_token", "dong", False, "GIET"),
    ("pc2_export_truoc_tu_choi", [(_M1_NEU, _M1_NEU + '        if getattr(a, "gws", False):\n            _gws_export_cred()\n')], "kieu", "kieu.list.gws", "khong_goi", False, "GIET"),
)
def _chay(m, store, ca):
    r = _Rig(m, ca.__name__, store)
    try:
        ca(r)
        if r.da != _LUOT_DU_KIEN[r.ca]:
            raise TinHieuChotCa(r.ca, "-", "so_luot")
    finally:
        _chay.dat = r.dat
    return r.dat
def _dung_co_che(q):
    """§4b: rc 5 qua `_nlm_contained` với đúng một dòng `TypeError`, và frame phát sinh là `_secrets_set_body` của CHÍNH nguồn đang chạy, câu `_GAN`."""
    return (q is not None and q.rc == 5 and len(q.err) == 1 and q.err[0].startswith("[secrets-set] ✗ dừng vì lỗi TypeError ")
            and q.vt == [("_secrets_set_body", True, _GAN)])
def _hang(nguon, tl_module, goc, store, cap, ca, luot, nhan, co_che):
    """Phân hạng MỘT đột biến trên bản sao trong bộ nhớ: HONG (neo ≠ 1 lần / không nạp được) · SONG_SOT · GIET (đúng lớp tín hiệu, đúng
    (ca, lượt, nhãn), và đúng cơ chế khi `co_che`) · TIN_DUNG_GIA (chết vì lý do khác, kể cả `AssertionError` không phải tín hiệu)."""
    for neo, thay in cap:
        if nguon.count(neo) != 1 or neo == thay:
            return "HONG"
        nguon = nguon.replace(neo, thay)
    try:
        m = _nap(nguon, tl_module, goc, store)
    except Exception:  # noqa: BLE001
        return "HONG"
    try:
        _chay(m, store, next(c for c in _CA if c.__name__ == ca))
        return "SONG_SOT"
    except TinHieuChotCa as e:
        return "GIET" if (e.ca, e.luot, e.nhan) == (ca, luot, nhan) and (not co_che or _dung_co_che(e.qs)) else "TIN_DUNG_GIA"
    except Exception:  # noqa: BLE001
        return "TIN_DUNG_GIA"
def _run(tl_module, nguon=None):
    """`nguon=None` ⇒ nguồn `tl_gws.py` của chính cây; truyền nguồn khác (vd. của base) để đo fragment này trên nguồn ấy."""
    goc = tl_module._imp("tl_gws"); goc.bind(tl_module)  # noqa: E702
    store = tl_module._imp("gws_cred_store")
    nguon = pathlib.Path(goc.__file__).read_text(encoding="utf-8") if nguon is None else nguon
    m, dat, luot = _nap(nguon, tl_module, goc, store), 0, 0
    for ca in _CA:
        try:
            _chay(m, store, ca); dat += 1  # noqa: E702
        except Exception as e:  # noqa: BLE001
            print("[%s] ĐỎ %s: %r" % (TEST_ID, ca.__name__, e), file=sys.stderr)
        luot += _chay.dat
        print("[%s] ca %s: lượt đạt %d/%d" % (TEST_ID, ca.__name__, _chay.dat, len(_LUOT_DU_KIEN[ca.__name__])), file=sys.stderr)
    kq = {d[0]: _hang(nguon, tl_module, goc, store, *d[1:]) for d in _DB}
    tk = [(d[0], _hang(nguon, tl_module, goc, store, *d[1:6]), d[6]) for d in _TU_KIEM]
    for ten, hang in list(kq.items()) + [(t, "tự kiểm %s ≠ %s" % (h, mong)) for t, h, mong in tk if h != mong]:
        if hang != "GIET":
            print("[%s] ĐỘT BIẾN %s: %s" % (TEST_ID, ten, hang), file=sys.stderr)
    giet, hong, tk_dat, tong = sum(h == "GIET" for h in kq.values()), sum(h == "HONG" for h in kq.values()), sum(h == mong for _t, h, mong in tk), sum(map(len, _LUOT_DU_KIEN.values()))
    print("[%s] CA %d/%d · LUOT %d/%d · DOT BIEN %d/%d · HONG %d · TU_KIEM %d/%d"
          % (TEST_ID, dat, len(_CA), luot, tong, giet, len(_DB), hong, tk_dat, len(tk)), file=sys.stderr)
    return dat == len(_CA) and luot == tong and giet == len(_DB) and hong == 0 and tk_dat == len(tk)
def run(tl_module):
    ra = io.StringIO()                      # fragment in mọi thứ ra STDERR (driver bundle đọc stdout làm JSON)
    with contextlib.redirect_stdout(ra):
        ok = _run(tl_module)
    return ok and not ra.getvalue()
