# -*- coding: utf-8 -*-
"""wp433 — `secrets-set` (`tl_gws.py`): bundle giải mã không phải object ⇒ rc 3 ngay sau giải mã, TRƯỚC mọi cờ/export/canary;
`token` không phải str ⇒ coi như thiếu, không lấy repr làm khoá public (spec SECRETS-SET-BUNDLE-KIEU r5).
Mọi lượt chạy trên bản `tl_gws` nạp TRONG BỘ NHỚ (nguồn của cây, hoặc nguồn truyền vào `run(tl, nguon)`), HOME/TL_* tạm, dữ liệu GIẢ;
mọi hàm tải/ghi/mạng là đồ giả CÓ ĐẾM (`_gas` giả ném lỗi), `encrypt` bọc để ghi khoá.
Quy tắc vế r5 §4: danh mục khoá ĐÓNG `ca.luot.quan_sat` (346), mỗi khoá MỘT hành vi, kỳ vọng chép cứng; `run()` trả True/False và
ghi BẢN ĐỒ ĐẦY ĐỦ `{khoa: bool}` của chính lần chạy ra tệp `$WP433_SS_BAN_DO` (không có biến thì không ghi). Khoá vắng = ĐỎ.
Ma trận đột biến N4 (mỗi đột biến một tiến trình MỚI) nằm ở rig ngoài fragment; fragment chỉ cung cấp bản đồ."""
import argparse, contextlib, io, json, os, pathlib, shutil, subprocess, sys, tempfile, types, urllib.request  # noqa: E401
TEST_ID = "wp433_secrets_set_bundle"
_MK = "wp433-ss-master-gia-0123456789abcdefghijklmnop"   # >= 32 ký tự; KHÔNG phải khoá thật
_DONG = "[secrets-set] ✗ dữ liệu không hợp lệ: bundle"
_GAN = 'bundle["token"] = a.gas_token; changed.append("token")'      # câu gán ĐẦU TIÊN vào bundle ở cờ --gas-token (cơ chế đột biến 1–2)
_GIA = (("fetch", "_secrets_fetch"), ("upload", "_secrets_upload"), ("stage_enc", "_stage_enc_upload"), ("gws_export", "_gws_export_cred"),
        ("nlm_refresh", "_refresh_nlm_auth"), ("canary", "_nlm_files_after_live_canary"), ("gas", "_gas"))
_KIEU = (("list", [1, 2]), ("str", "chuoi"), ("int", 7), ("null", None), ("true", True))
_TOKEN = (("list", [1]), ("dict", {"a": 1}), ("int", 7))
_CO = {"gas_token": dict(gas_token="tok-moi"), "webapp": dict(webapp="https://gia.invalid/exec"), "gws": dict(gws=True), "nlm": dict(nlm=True), "khong_co": {}}
_HOP_LE = {"token": "tok-cu", "webappUrl": "u"}
# ---- danh mục khoá ĐÓNG, chép cứng (spec r5 §4): lượt theo ca, loại quan sát theo ca
_LUOT = {
    "kieu": tuple("kieu.%s.%s" % (k, c) for k in ("list", "str", "int", "null", "true") for c in ("gas_token", "webapp", "gws", "nlm", "khong_co")),
    "token_kieu": tuple("token_kieu.%s.%s" % (k, c) for k in ("list", "dict", "int") for c in ("gws", "nlm")),
    "hoi_quy": ("hoi_quy.gas_token", "hoi_quy.webapp", "hoi_quy.gws", "hoi_quy.nlm", "hoi_quy.khong_co", "hoi_quy.env_token.gws"),
}
_QS = {
    "kieu": ("rc3", "dong", "fetch1", "upload0", "stage_enc0", "gws_export0", "nlm_refresh0", "canary0", "gas0", "encrypt0"),
    "token_kieu": ("rc0", "upload1", "stage_enc0", "khoa_public_rong", "canh_bao_co", "khong_dong_loi"),
    "hoi_quy": ("rc", "fetch", "gas", "upload", "stage_enc", "gws_export", "nlm_refresh", "canary", "encrypt", "khoa_public"),
}
_DANH_MUC = frozenset("%s.%s" % (luot, qs) for ca in _LUOT for luot in _LUOT[ca] for qs in _QS[ca])
_SO_KHOA = 346                                                         # 250 + 36 + 60
_HQ = {  # bảng kỳ vọng `hoi_quy` (spec r5 §4), theo thứ tự lượt _LUOT["hoi_quy"]
    "rc": (0, 0, 0, 0, 1, 0), "fetch": (1, 1, 1, 1, 1, 1), "gas": (0, 0, 0, 0, 0, 0), "upload": (1, 1, 1, 1, 0, 1),
    "stage_enc": (0, 0, 1, 1, 0, 1), "gws_export": (0, 0, 1, 0, 0, 1), "nlm_refresh": (0, 0, 0, 1, 0, 0), "canary": (0, 0, 0, 1, 0, 0),
    "encrypt": (1, 1, 2, 2, 0, 2), "khoa_public": ([], [], ["tok-cu"], ["tok-cu"], [], ["tok-env"]),
}
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
           "canary": ({"auth.json": "gia"}, 0, None), "gas": lambda *a, **k: _nem(RuntimeError("MANG_BI_CHAN"))}
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
    """Các lượt trên một bản nạp `m`; mỗi LƯỢT có thư mục tạm, HOME/USERPROFILE/TL_*/cwd riêng, khôi phục khi ra. `ghi` đưa quan sát
    của lượt vào bản đồ chung: khoá = `<lượt>.<loại quan sát>`, giá trị = đạt hay không."""
    def __init__(self, m, store, ban_do):
        self.m, self.store, self.ban_do = m, store, ban_do
    def luot(self, ten, bundle_obj, co, env_token=None):
        """Một lượt `cmd_secrets_set`: chặn tiến trình con/mạng (`MANG_BI_CHAN`), stdout/stderr RIÊNG; trả quan sát (rc, bộ đếm, khoá, stderr, vt)."""
        m = self.m
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
        return types.SimpleNamespace(rc=rc, dem=dict(m.dem), khoa=list(m.khoa), err=err.getvalue().splitlines(), vt=list(m.vt))
    def ghi(self, luot, qs):
        for k, v in qs.items():
            self.ban_do["%s.%s" % (luot, k)] = v is True
def kieu(r):
    for luot in _LUOT["kieu"]:
        _ca, kt, ct = luot.split(".")
        q = r.luot(luot, dict(_KIEU)[kt], _CO[ct])
        d = q.dem
        r.ghi(luot, dict(rc3=q.rc == 3, dong=q.err == [_DONG], fetch1=d["fetch"] == 1, upload0=d["upload"] == 0, stage_enc0=d["stage_enc"] == 0,
                         gws_export0=d["gws_export"] == 0, nlm_refresh0=d["nlm_refresh"] == 0, canary0=d["canary"] == 0, gas0=d["gas"] == 0,
                         encrypt0=len(q.khoa) == 0))
def token_kieu(r):
    for luot in _LUOT["token_kieu"]:
        _ca, tt, ct = luot.split(".")
        q = r.luot(luot, {"token": dict(_TOKEN)[tt], "webappUrl": "u"}, _CO[ct])
        r.ghi(luot, dict(rc0=q.rc == 0, upload1=q.dem["upload"] == 1, stage_enc0=q.dem["stage_enc"] == 0, khoa_public_rong=set(q.khoa) <= {_MK},
                         canh_bao_co=sum("thiếu webapp token" in d for d in q.err) == 1, khong_dong_loi=not any("✗" in d for d in q.err)))
def hoi_quy(r):
    for i, luot in enumerate(_LUOT["hoi_quy"]):
        if luot == "hoi_quy.env_token.gws":
            q = r.luot(luot, {"token": [1], "webappUrl": "u"}, _CO["gws"], env_token="tok-env")
        else:
            q = r.luot(luot, dict(_HOP_LE), _CO[luot.split(".")[1]])
        do = dict(q.dem, rc=q.rc, encrypt=len(q.khoa), khoa_public=[k for k in q.khoa if k != _MK])
        r.ghi(luot, {t: do[t] == _HQ[t][i] for t in _QS["hoi_quy"]})
_CA = (kieu, token_kieu, hoi_quy)
def _dung_co_che(q):
    """Đột biến 1–2 (§4 N4 ii): rc 5 qua `_nlm_contained` với đúng một dòng `TypeError`, và frame phát sinh là `_secrets_set_body` của
    CHÍNH nguồn đang chạy, câu `_GAN`. Rig N4 gọi hàm này trong tiến trình của chính đột biến."""
    return (q is not None and q.rc == 5 and len(q.err) == 1 and q.err[0].startswith("[secrets-set] ✗ dừng vì lỗi TypeError ")
            and q.vt == [("_secrets_set_body", True, _GAN)])
def _do(tl_module, nguon=None):
    """Chạy ba ca, trả bản đồ `{khoa: bool}`. `nguon=None` ⇒ nguồn `tl_gws.py` của chính cây; ca văng ngoại lệ thì các khoá chưa ghi VẮNG."""
    goc = tl_module._imp("tl_gws"); goc.bind(tl_module)  # noqa: E702
    store = tl_module._imp("gws_cred_store")
    nguon = pathlib.Path(goc.__file__).read_text(encoding="utf-8") if nguon is None else nguon
    m, ban_do = _nap(nguon, tl_module, goc, store), {}
    for ca in _CA:
        try:
            ca(_Rig(m, store, ban_do))
        except Exception as e:  # noqa: BLE001
            print("[%s] ĐỎ ca %s: văng %s" % (TEST_ID, ca.__name__, type(e).__name__), file=sys.stderr)
    return ban_do
def run(tl_module, nguon=None):
    ra = io.StringIO()                      # fragment in mọi thứ ra STDERR (driver bundle đọc stdout làm JSON)
    with contextlib.redirect_stdout(ra):
        ban_do = _do(tl_module, nguon)
    p = os.environ.get("WP433_SS_BAN_DO")
    if p:
        pathlib.Path(p).write_text(json.dumps(ban_do, ensure_ascii=False, sort_keys=True), encoding="utf-8")
    sai, thua = sorted(k for k in _DANH_MUC if ban_do.get(k) is not True), sorted(set(ban_do) - _DANH_MUC)
    for ca in _LUOT:
        n = sum(k.startswith(ca + ".") for k in _DANH_MUC)
        print("[%s] ca %s: khoá đạt %d/%d" % (TEST_ID, ca, n - sum(k.startswith(ca + ".") for k in sai), n), file=sys.stderr)
    for k in (sai + thua)[:20]:
        print("[%s] ĐỎ %s: %s" % (TEST_ID, k, "thừa" if k in thua else "vắng" if k not in ban_do else "sai"), file=sys.stderr)
    return len(_DANH_MUC) == _SO_KHOA and not sai and not thua and not ra.getvalue()
