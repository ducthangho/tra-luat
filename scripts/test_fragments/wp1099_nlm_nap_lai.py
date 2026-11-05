# -*- coding: utf-8 -*-
"""wp1099 — `nlm_cli._run` tự nạp lại jar NLM có điều kiện ở phiên cloud (ADR-0063, spec cloud-setup-p3b-nlm-401-r9). `nlm_cli`
THẬT (hoặc đột biến) chạy với `tl.py`/`nlm` GIẢ giữ trạng thái; đột biến chỉ tính GIẾT khi đúng ca ném `TinHieuChotCa`."""

import contextlib, hashlib, importlib.util, inspect, io, json, os, subprocess, sys, tempfile, threading, time
from pathlib import Path

TEST_ID = "wp1099_nlm_nap_lai"
_BASE = "358451e80b573d148807717bece3fd973915fbad"   # base của lease wp1099-cloud-setup-p3b-r9-g1-claude
_CANH = "SENTINEL-COOKIE-wp1099"
_CAU = ("Ngoại lệ duy nhất: cơ chế tự nạp có điều kiện bên trong `nlm_cli` ở phiên cloud (`ADR-0063`) — agent vẫn không tự gõ "
        "lệnh nạp.")
_RA, _QT, _PR = "references/RASOAT_HOSO_LOOP.md", "references/QUY_TRINH_RA_SOAT_3_TANG.md", "docs/PROTOCOL_DA_PHIEN.md"
_ADR = "docs/adr/0063-nlm-tu-nap-lai-co-dieu-kien-phien-cloud.md"
class TinHieuChotCa(AssertionError):
    def __init__(self, ca, msg):
        super().__init__("%s: %s" % (ca, msg))
        self.ca = ca
_TL_GIA = r'''
import json, os, sys, time
_ST, _LOG, _CANH = os.environ["WP1099_ST"], os.environ["WP1099_LOG"], os.environ["WP1099_CANH"]
_st = lambda: json.load(open(_ST, encoding="utf-8"))
_ghi = lambda dong: open(_LOG, "a", encoding="utf-8").write(dong + "\n")
bind = lambda _m: None
_nlm_canary_notebook = lambda nb: "NB"
def _imp(name):                              # A13: trả tl_gws THẬT với nlm_cli giả (lỗi lần thử 1/2/3 lấy từ trạng thái)
    if "a13" not in _st():
        return sys.modules[__name__]
    import importlib.util as _u
    sp = _u.spec_from_file_location("_tl_that", os.path.join(os.environ["WP1099_KHO"], "scripts", "tl.py"))
    _that = _u.module_from_spec(sp); sys.modules["_tl_that"] = _that; sp.loader.exec_module(_that)
    tg = _that._imp("tl_gws"); tg.bind(_that)
    seq, i = _st()["a13"], [0]
    def _run(args, timeout=30):
        i[0] += 1
        return 1, "", seq[min(i[0], 3) - 1]
    tg._imp = lambda n: type("NC", (), {"AUTH_FIX_HINT": "auth", "nlm_available": staticmethod(lambda: True),
                                        "_run": staticmethod(_run)})
    time.sleep = lambda s: None
    return tg
def _nlm_auth_alive(nb, require_notebook_body=False):
    st = _st()
    _ghi("canary TAT=%s" % os.environ.get("TL_NLM_NAP_LAI_TAT"))
    print(_CANH)
    che_do = st.get("canary", "jar")
    if che_do == "loi":
        raise RuntimeError(_CANH)
    time.sleep(5 if che_do == "ngu" else st.get("cham", 0))
    return (None if che_do == "none" else st["jar"] == "song"), "x"
if __name__ == "__main__":
    st, lenh = _st(), sys.argv[1:]
    dau = os.path.join(os.path.expanduser("~"), ".notebooklm-mcp-cli", ".tra-luat-nap-lai.json")
    _ghi("tl %s TAT=%s dau_co=%d" % (" ".join(lenh), os.environ.get("TL_NLM_NAP_LAI_TAT"), os.path.exists(dau)))
    print(_CANH), print(_CANH, file=sys.stderr)
    if lenh[:1] == ["nlm-auth-status"]:            # mô hình lệnh thật: mọi lỗi probe gộp thành chết (nlm_ops.py:1424–1430)
        sys.exit(3 if "a13" in st else 0)
    if st.get("goi_nguoc"):                        # A4: con gọi ngược nlm_cli với lỗi auth — phải KHÔNG đệ quy
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        import nlm_cli
        nlm_cli._run(["source", "list", "NB", "-j"], 30)
    if st["bundle"] == "cu_hon":
        print("TỪ CHỐI HẠ CẤP"); sys.exit(2)
    if st["bundle"] == "song":
        json.dump({**st, "jar": "song"}, open(_ST, "w", encoding="utf-8"))
    sys.exit(0)
'''
_NLM_GIA = r'''
import json, os, sys
st = json.load(open(os.environ["WP1099_ST"], encoding="utf-8"))
open(os.environ["WP1099_LOG"], "a", encoding="utf-8").write("nlm %s TAT=%s\n" % (" ".join(sys.argv[1:]), os.environ.get("TL_NLM_NAP_LAI_TAT")))
if "nlm_rc" in st:
    print(st.get("nlm_err", ""), file=sys.stderr); sys.exit(st["nlm_rc"])
if st["jar"] == "chet":
    print("Authentication expired", file=sys.stderr); sys.exit(1)
print("[]")
'''
class _Cay:
    """Một cây tạm + môi trường; `moi()` nạp một bản `nlm_cli` MỚI (= tiến trình mới đối với trạng thái mô-đun)."""
    def __init__(self, td, nguon, kho):
        self.td = Path(td)
        (self.td / "s").mkdir()
        (self.td / "s" / "nlm_cli.py").write_text(nguon, encoding="utf-8")
        (self.td / "s" / "tl.py").write_text(_TL_GIA, encoding="utf-8")
        (self.td / "nlm.py").write_text(_NLM_GIA, encoding="utf-8")
        exe = self.td / ("nlm" if os.name == "posix" else "nlm.cmd")
        exe.write_text("#!" + sys.executable + "\n" + _NLM_GIA if os.name == "posix"
                       else '@"%s" "%s" %%*\r\n' % (sys.executable, self.td / "nlm.py"), encoding="utf-8")
        exe.chmod(0o755)
        (self.td / "home").mkdir()
        self.tep_dau = self.td / "home" / ".notebooklm-mcp-cli" / ".tra-luat-nap-lai.json"
        self.st, self.log, self.n = self.td / "st.json", self.td / "log.txt", 0
        self.env = {"HOME": str(self.td / "home"), "USERPROFILE": str(self.td / "home"), "TL_NLM_BIN": str(exe),
                    "WP1099_ST": str(self.st), "WP1099_LOG": str(self.log), "WP1099_CANH": _CANH,
                    "WP1099_KHO": str(kho), "PYTHONDONTWRITEBYTECODE": "1",
                    "CLAUDE_CODE_REMOTE": "true", "TL_NLM_NAP_LAI_TAT": None}
    def dat(self, **st):                          # trạng thái mới cho một ca; xoá dấu (cần dấu thì `dau()` SAU `dat()`)
        self.tep_dau.unlink(missing_ok=True)
        self.st.write_text(json.dumps({"jar": "chet", "bundle": "song", **st}), encoding="utf-8")
        self.log.write_text("", encoding="utf-8")
    def moi(self):
        self.n += 1
        spec = importlib.util.spec_from_file_location("_wp1099_nlm_cli_%d" % self.n, self.td / "s" / "nlm_cli.py")
        m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
        return m
    def goi(self, m, args, ham=None):
        """Một lời gọi `_run` (hoặc `ham`) với stderr/stdout RIÊNG; kiểm A11 ngay trên lời gọi ấy. Trả (kq, stderr)."""
        cu_err, cu_out, truoc = sys.stderr, sys.stdout, len(self.nhat_ky())
        sys.stderr, sys.stdout = io.StringIO(), io.StringIO()
        try:
            kq = (ham or m._run)(args) if ham else m._run(args, 30)
            err, out = sys.stderr.getvalue(), sys.stdout.getvalue()
        finally:
            sys.stderr, sys.stdout = cu_err, cu_out
        toi = m.NAP_LAI_GAN_NHAT is not None or any(c.startswith("canary") for c in self.nhat_ky()[truoc:])
        dong = _dong(err)
        _chot("A11", len(dong) == (1 if toi else 0), "lời gọi tới Giới hạn=%s mà có %d dòng" % (toi, len(dong)))
        tra = json.dumps(kq, ensure_ascii=False)
        _chot("A11", "nlm_nap_lai:" not in out + tra and _CANH not in err + out + tra, "dòng báo lọt ra / lộ đầu ra con")
        return kq, err
    def nhat_ky(self):
        return self.log.read_text(encoding="utf-8").splitlines()
    def dau(self, ts):
        (self.td / "home" / ".notebooklm-mcp-cli").mkdir(exist_ok=True)
        self.tep_dau.write_text(json.dumps(ts if isinstance(ts, list) else {"ts": ts}), encoding="utf-8")
def _chot(ca, dk, msg):
    if not dk:
        raise TinHieuChotCa(ca, msg)
_dong = lambda err: [d for d in err.splitlines() if d.startswith("nlm_nap_lai:")]
def _mot(cay, ca, args, **st):
    cay.dat(**st)
    kq, err = cay.goi(cay.moi(), args)
    return kq, err, cay.nhat_ky()
_SL = ["source", "list", "NB", "-j"]
def _a1(cay):
    for ten, them in (("vang", {"CLAUDE_CODE_REMOTE": None}), ("false", {"CLAUDE_CODE_REMOTE": "false"}), ("tat", {"TL_NLM_NAP_LAI_TAT": "1"})):
        with _Env({**cay.env, **them}):
            cay.dat(), (m := cay.moi())
            goc = m._run_mot(_SL, 30)                 # thân `_run` của base, giữ nguyên byte (chỉ đổi tên)
            cay.dat()
            kq, err = cay.goi(m, _SL)
            _chot("A1", kq == goc and not any(c.startswith("tl ") for c in cay.nhat_ky()) and not _dong(err),
                  "%s: cơ chế chạy khi cổng tắt" % ten)
def _a2(cay):
    for rc, e in ((1, "boom"), (124, "auth timeout"), (127, "auth missing")):
        kq, err, log = _mot(cay, "A2", _SL, nlm_rc=rc, nlm_err=e)
        _chot("A2", not any(c.startswith(("tl ", "canary")) for c in log) and not _dong(err), "ứng viên sai: rc %d" % rc)
def _a3(cay):
    kq, err, log = _mot(cay, "A3", _SL)
    loai = [c.split()[0] if not c.startswith("tl ") else "tl " + c.split()[1] for c in log]
    _chot("A3", loai == ["nlm", "canary", "tl nlm-auth-load", "canary", "nlm"], "thứ tự %r" % loai)
    _chot("A3", kq[0] == 0 and _dong(err) and _dong(err)[0].startswith("nlm_nap_lai: ĐÃ NẠP, THỬ LẠI ĐẠT — "), "%r" % err)
    cay.dat()
    m = cay.moi()
    d = cay.goi(m, "NB", ham=m.source_list)[0]
    _chot("A3", isinstance(d, dict) and (d.get("nap_lai") or {}).get("trang_thai") == "ĐÃ NẠP, THỬ LẠI ĐẠT", "%r" % d)
def _a4(cay):
    kq, err, log = _mot(cay, "A4", _SL, goi_nguoc=True)
    tl = [c for c in log if c.startswith("tl ")]
    _chot("A4", tl and all("TAT=1" in c for c in tl) and sum("nlm-auth-load" in c for c in tl) == 1, "%r" % log)
def _a5(cay):
    for che_do, mong in (("song", "BỎ QUA — canary sống"), ("none", "KHÔNG ĐO ĐƯỢC — canary"),
                         ("loi", "KHÔNG ĐO ĐƯỢC — canary"), ("ngu", "KHÔNG ĐO ĐƯỢC — canary")):
        cay.dat(canary="jar" if che_do == "song" else che_do, jar="chet")
        (m := cay.moi())._NAP_LAI_HAN_CANARY = 1
        if che_do == "song":                         # canary sống trong khi nlm vẫn báo auth: lỗi không do auth
            cay.dat(nlm_rc=1, nlm_err="unauthorized", jar="song")
        kq, err = cay.goi(m, _SL)
        _chot("A5", not any("nlm-auth-load" in c for c in cay.nhat_ky()) and _dong(err)
              and _dong(err)[0].startswith("nlm_nap_lai: " + mong), "%s: %r" % (che_do, err))
def _a6(cay, ca="A6", bundle="chet", mong="BUNDLE CŨNG CHẾT — "):     # A7: bundle cũ hơn ⇒ TỪ CHỐI HẠ CẤP, không --force
    kq, err, log = _mot(cay, ca, _SL, bundle=bundle)
    _chot(ca, sum("nlm-auth-load" in c for c in log) == 1 and sum(c.startswith("nlm ") for c in log) == 1 and kq[0] == 1
          and _dong(err)[0].startswith("nlm_nap_lai: " + mong) and not any("--force" in c for c in log), "%r %r" % (log, err))
def _a8(cay):
    ghi = "ĐÃ NẠP, KHÔNG THỬ LẠI (lệnh ghi)"
    for args, lai, mong in ((["source", "add", "NB", "--url", "x"], 1, ghi), (["source", "sync", "S"], 1, ghi),
                            (["notebook", "query", "NB", "q", "-j"], 2, "ĐÃ NẠP, THỬ LẠI ĐẠT")):
        kq, err, log = _mot(cay, "A8", args)
        _chot("A8", sum(c.startswith("nlm ") for c in log) == lai and _dong(err)[0].startswith("nlm_nap_lai: " + mong),
              "%r: %r" % (args, log))
def _a9(cay):
    cay.dat(bundle="chet")
    m = cay.moi()
    d1, d2 = cay.goi(m, _SL)[1], cay.goi(m, _SL)
    _chot("A9", _dong(d1)[0].startswith("nlm_nap_lai: BUNDLE CŨNG CHẾT") and len(_dong(d2[1])) == 1
          and _dong(d2[1])[0].startswith("nlm_nap_lai: BỎ QUA — đã nạp"), "hai lời gọi: %r %r" % (d1, d2[1]))
    cay.dat(bundle="chet", cham=0.5)              # hai LUỒNG cùng tiến trình: canary chậm để cả hai vào cùng lúc (F02)
    m, cu, sys.stderr = cay.moi(), sys.stderr, io.StringIO()
    ts = [threading.Thread(target=m._run, args=(_SL, 30)) for _ in range(2)]
    try:
        [x.start() for x in ts], [x.join() for x in ts]
    finally:
        sys.stderr = cu
    _chot("A9", sum("nlm-auth-load" in c for c in cay.nhat_ky()) == 1, "hai luồng ⇒ nạp khác 1 lần")
    if hasattr(os, "mkfifo"):                     # dấu là FIFO không có bên ghi ⇒ đọc dấu không được treo (F06)
        cay.dat(), os.mkfifo(cay.tep_dau)
        x = threading.Thread(target=cay.moi()._doc_dau, daemon=True)
        x.start(), x.join(5), x.is_alive() and os.close(os.open(cay.tep_dau, os.O_WRONLY | os.O_NONBLOCK))  # gỡ kẹt
        _chot("A9", not x.is_alive(), "đọc dấu FIFO treo"), cay.tep_dau.unlink()
    for dau, nap in ((-300, 0), (-700, 1), (3600, 1), ([1], 1)):
        cay.dat(bundle="chet")
        cay.dau(dau if isinstance(dau, list) else int(time.time()) + dau)
        cay.goi(cay.moi(), _SL)
        _chot("A9", sum("nlm-auth-load" in c for c in cay.nhat_ky()) == nap, "dấu %r ⇒ nạp %d" % (dau, 1 - nap))
def _a10(cay):
    kq, err, log = _mot(cay, "A10", _SL)
    tep = cay.tep_dau
    _chot("A10", any("nlm-auth-load" in c and "dau_co=1" in c for c in log)
          and (os.name != "posix" or (tep.stat().st_mode & 0o777) == 0o600), "dấu chưa có lúc nạp / quyền: %r" % log)
    cay.dat()                                     # rename LẪN dọn đều lỗi ⇒ vẫn trả tuple gốc + đúng 1 dòng (F05)
    cu, os.replace, os.unlink = (os.replace, os.unlink), *[lambda *a: os.chmod("/nonexistent-wp1099", 0)] * 2
    try:
        kq, err = cay.goi(cay.moi(), _SL)
    except Exception as e:
        _chot("A10", False, "lỗi dọn tệp tạm thoát khỏi _run: %s" % type(e).__name__)
    finally:
        os.replace, os.unlink = cu
    _chot("A10", kq[0] == 1 and "không ghi được tệp dấu" in err, "lỗi kép: %r %r" % (kq, err))
    [x.unlink() for x in tep.parent.glob(".nap-lai-*")], cay.dat()   # rác do OS (giả) từ chối xoá — không phải của ca sau
    tep.mkdir()                                   # dấu là THƯ MỤC ⇒ không ghi được ⇒ không nạp, không rác (F01), không rò fd (F07)
    m, fd = cay.moi(), (lambda: len(os.listdir("/dev/fd")) if os.path.isdir("/dev/fd") else 0)
    truoc, (kq, err) = fd(), cay.goi(m, _SL)
    [m._doc_dau() for _ in range(20)]
    _chot("A10", not any("nlm-auth-load" in c for c in cay.nhat_ky()) and "không ghi được tệp dấu" in err and fd() == truoc
          and not list(tep.parent.glob(".nap-lai-*")), "dấu là thư mục: nạp/để rác/rò fd: %r" % err)

# sha256 của json.dumps(bốn hằng) đọc từ `git show _BASE:scripts/nlm_cli.py` — đo được cả ở gói phát hành không có git.
_A12_BAM = "57ec1837153e8d1a796f852249ac23695990c3c1f20a5af6a86a55488ea34211"
def _a12(cay, kho):
    m = cay.moi()
    v = [getattr(m, ten) for ten in ("AUTH_FIX_HINT", "AUTH_FIX_HINT_SHORT", "_AUTH_FIX_ORDER", "_AUTH_FIX_RASOAT_CARVE")]
    _chot("A12", hashlib.sha256(json.dumps(v, ensure_ascii=False).encode("utf-8")).hexdigest() == _A12_BAM,
          "bốn hằng auth lệch bản base")
_A13 = (("connection refused", None, 2), ("HTTP 403 permission denied", None, 2), ("Authentication expired", False, 3),
        (["connection refused", "connection refused", "Authentication expired"], False, 3),
        (["Authentication expired", "connection refused", "Authentication expired"], False, 3),
        (["Authentication expired", "Authentication expired", "connection refused"], None, 2))
def _NC(seq):
    it = iter(seq + seq[-1:] * 3)
    return type("NC", (), {"AUTH_FIX_HINT": "auth", "nlm_available": lambda s: True, "_run": lambda s, a, timeout=30: (1, "", next(it))})()
def _a13(cay, tl_module, ham=None):
    tg = tl_module._imp("tl_gws")
    tg.bind(tl_module)
    ham = ham or tg._nlm_auth_alive
    g = ham.__globals__
    cu_imp, cu_sleep = g.get("_imp"), time.sleep
    try:
        time.sleep = lambda s: None
        for loi, mong, _ in _A13:
            nc = _NC(loi if isinstance(loi, list) else [loi] * 3)
            g["_imp"] = lambda n: nc
            _chot("A13", ham("NB", require_notebook_body=True)[0] is mong, "%r ⇒ khác %r" % (loi, mong))
    finally:
        g["_imp"], time.sleep = cu_imp, cu_sleep
    m = cay.moi()
    for loi, _, ma in _A13:
        cay.dat(a13=loi if isinstance(loi, list) else [loi] * 3)
        _chot("A13", m._canary() == ma, "canary con %r ⇒ khác %d" % (loi, ma))
def _d(kho, doc=None):
    """D1/D2/D3 — chỉ cây dev có git (gói phát hành không mang docs/); `doc` thay nội dung tệp cho đột biến."""
    doc, git = doc or {}, ["git", "-C", str(kho), "show"]
    doc_tep = lambda p: doc[p] if p in doc else (kho / p).read_text(encoding="utf-8")
    for tep in (_RA, _QT):
        b = subprocess.run(git + [_BASE + ":" + tep], capture_output=True)
        _chot("D1", b.returncode == 0, "không đọc được base %s" % tep)
        nb, nh = " ".join(b.stdout.decode("utf-8").split()), " ".join(doc_tep(tep).split())
        i = nh.find(_CAU)
        _chot("D1", nb.count(_CAU) == 0 and nh.count(_CAU) == 1 and nh[:i - 1] + nh[i + len(_CAU):] == nb, tep)
    _chot("D2", sum(d.startswith("| `ADR-0063` |") for d in doc_tep(_PR).splitlines()) == 1, "dòng §20")
    import re
    tt = re.compile(r"^[-*]\s*\*\*Tr[aạ]ng th[aá]i:?\*\*:?\s*(\S.*)$", re.M | re.I)
    _chot("D3", [x.group(0).strip() for x in tt.finditer(doc_tep(_ADR))] == ["- **Trạng thái:** Accepted"], "trạng thái")
@contextlib.contextmanager
def _Env(env):
    dat = lambda d: [os.environ.pop(k, None) if v is None else os.environ.__setitem__(k, v) for k, v in d.items()]
    cu = {k: os.environ.get(k) for k in env}
    dat(env)
    try:
        yield
    finally:
        dat(cu)
_CA = {"A1": _a1, "A2": _a2, "A3": _a3, "A4": _a4, "A5": _a5, "A6": _a6, "A7": lambda c: _a6(c, "A7", "cu_hon", "TỪ CHỐI HẠ CẤP"), "A8": _a8, "A9": _a9, "A10": _a10}

# (tên, chuỗi cũ, chuỗi mới, ca chạy, ca phải bắn) — chuỗi cũ phải có ĐÚNG 1 lần trong nlm_cli.py, không thì ĐỎ
_DOT_BIEN = (
    ("bo_cong_remote", 'os.environ.get("CLAUDE_CODE_REMOTE") == "true" and ', "", "A1", "A1"),
    ("bo_cong_tat", ' and os.environ.get("TL_NLM_NAP_LAI_TAT") != "1"', "", "A1", "A1"),
    ("rc124_la_ung_vien", "rc not in (0, 124, 127)", "rc not in (0, 127)", "A2", "A2"),
    ("bo_chay_lai", "lai = _run_mot(args, timeout)", "lai = dau", "A3", "A3"),
    ("con_khong_tat", 'env["TL_NLM_NAP_LAI_TAT"] = "1"', "pass", "A4", "A4"),
    ("ma_khac_0_la_chet", '    if ma != 3:\n        _bao("KHÔNG ĐO ĐƯỢC", f"canary {ma}"); return dau\n', "", "A5", "A5"),
    ("chay_lai_bat_ke_canary_sau", "    ma = _canary()\n    if ma != 0:", "    ma = 0\n    if ma != 0:", "A6", "A6"),
    ("them_force", '"tl.py"), "nlm-auth-load"]', '"tl.py"), "nlm-auth-load", "--force"]', "A7", "A7"),
    ("danh_sach_cam", "if tuple(args[:2]) not in _NAP_LAI_CHO_PHEP:", 'if tuple(args[:2]) == ("source", "add"):', "A8", "A8"),
    ("ghi_dau_hong_van_nap", 'if not _ghi_dau(int(now), "dang_nap"):', 'if not (_ghi_dau(int(now), "dang_nap") or 1):', "A10", "A10"),
    ("de_rac_tam", ", lambda: tam and os.unlink(tam))", ")", "A10", "A10"),
    ("don_khong_bao_ve", "        except OSError:\n            pass", "        except ZeroDivisionError:\n            pass", "A10", "A10"),
    ("doc_dau_ro_fd", "        _don(lambda: fd is not None and os.close(fd))\n\ndef _don", "        pass\n\ndef _don", "A10", "A10"),
    ("bo_khoa_luong", "    with _NAP_LAI_KHOA:", "    if True:", "A9", "A9"),
    ("doc_dau_chan", ' | getattr(os, "O_NONBLOCK", 0)', "", "A9", "A9"),
    ("cua_so_60", "= 120, 60, 600", "= 120, 60, 60", "A9", "A9"),
    ("bo_chot_dong_ho_lech", "ts <= now + 60 and ", "", "A9", "A9"),
    ("ghi_dau_sau_nap", 'if not _ghi_dau(int(now), "dang_nap"):', "if False:", "A10", "A10"),
    ("chuyen_tiep_dau_ra_con", "        return p.returncode, (p.stdout or \"\")", "        print(p.stdout, file=sys.stderr)\n        return p.returncode, (p.stdout or \"\")", "A5", "A11"),
    ("in_hai_dong", '    print(f"nlm_nap_lai: {trang_thai} — {chi_tiet}", file=sys.stderr)', '    print(f"nlm_nap_lai: {trang_thai} — {chi_tiet}", file=sys.stderr)\n    print("nlm_nap_lai: x", file=sys.stderr)', "A3", "A11"),
    ("ghi_thang_fd2", '    print(f"nlm_nap_lai: {trang_thai} — {chi_tiet}", file=sys.stderr)', '    os.write(2, f"nlm_nap_lai: {trang_thai} — {chi_tiet}\\n".encode("utf-8"))', "A3", "A11"),
    ("canary_la_nlm_auth_status", '_con([sys.executable, "-c", _CANARY, _NAP_LAI_THU_MUC]', '_con([sys.executable, os.path.join(_NAP_LAI_THU_MUC, "tl.py"), "nlm-auth-status"]', "A13", "A13"),
    ("sua_cau_tru", "KHÔNG tự chạy (1)/(2) ", "tự chạy (1)/(2) ", "A12", "A12"),
)

# đột biến TÀI LIỆU (chỉ cây dev): (tên, tệp, chuỗi cũ, chuỗi mới, ca phải bắn)
_DOT_BIEN_D = (("d1_xoa_cau", _RA, " " + _CAU, "", "D1"), ("d1_lap_cau", _QT, _CAU, _CAU + " " + _CAU, "D1"),
               ("d1_sua_chu_cu", _QT, "**CẤM** tự", "CẤM tự", "D1"),
               ("d2_xoa_dong", _PR, "| `ADR-0063` |", "| ADR-0063 |", "D2"),
               ("d3_them_proposed", _ADR, "- **Trạng thái:** Accepted\n", "- **Trạng thái:** Accepted\n- **Trạng thái:** Proposed\n", "D3"))
def _chay(nguon, ten_ca, tl_module, kho, ham=None):
    with tempfile.TemporaryDirectory(prefix="wp1099_") as td:
        cay = _Cay(td, nguon, kho)
        with _Env(cay.env):
            {"A12": lambda: _a12(cay, kho), "A13": lambda: _a13(cay, tl_module, ham)}.get(ten_ca, lambda: _CA[ten_ca](cay))()

_bao_loi = lambda msg: print("[%s] FAIL %s" % (TEST_ID, msg), file=sys.stderr)
def run(tl_module):
    kho = Path(tl_module.__file__).resolve().parent.parent
    nguon = (kho / "scripts" / "nlm_cli.py").read_text(encoding="utf-8")
    try:
        for ten_ca in list(_CA) + ["A12", "A13"]:
            _chay(nguon, ten_ca, tl_module, kho)
        (kho / ".git").exists() and _d(kho)      # D chỉ trên cây dev: gói phát hành không mang docs/ lẫn .git
    except Exception as e:                            # mọi lỗi của bản THẬT ⇒ ĐỎ có chẩn đoán
        _bao_loi("%s: %s" % (type(e).__name__, e))
        return False
    tg, co_git = tl_module._imp("tl_gws"), (kho / ".git").exists()
    src = inspect.getsource(tg._nlm_auth_alive)

    def _gws():                                   # tl_gws "lần thử ĐẦU quyết định" trên BẢN SAO hàm ⇒ A13 ĐỎ
        g = dict(tg._nlm_auth_alive.__globals__)
        exec(compile(src.replace("if _att < 2:", "if False:"), "mutant", "exec"), g)
        _chay(nguon, "A13", tl_module, kho, ham=g["_nlm_auth_alive"])
    doc = lambda tep: (kho / tep).read_text(encoding="utf-8")
    viec = [(ten, dich, nguon.count(cu), lambda cu=cu, moi=moi, c=c: _chay(nguon.replace(cu, moi), c, tl_module, kho))
            for ten, cu, moi, c, dich in _DOT_BIEN] + [("tl_gws_lan_dau", "A13", src.count("if _att < 2:"), _gws)]
    viec += [(ten, dich, doc(tep).count(cu), lambda tep=tep, cu=cu, moi=moi: _d(kho, {tep: doc(tep).replace(cu, moi)}))
             for ten, tep, cu, moi, dich in (_DOT_BIEN_D if co_git else ())]
    song = []
    for ten, dich, so_lan, fn in viec:
        try:
            _chot("ĐỘT BIẾN", so_lan == 1, "chuỗi cũ xuất hiện %d lần" % so_lan)
            fn()
            song.append(ten + " (SỐNG)")
        except TinHieuChotCa as e:
            if e.ca != dich:
                song.append("%s (giết bởi %s, đích %s)" % (ten, e.ca, dich))
        except Exception as e:
            song.append("%s (tín dụng giả: %s)" % (ten, type(e).__name__))
    if song:
        _bao_loi("đột biến không bị giết đúng lý do: %s" % "; ".join(song))
        return False
    print("[%s] CA A: %d/%d · D: %s · DOT BIEN: %d/%d bị giết đúng ca" % ((TEST_ID,) + (len(_CA) + 2,) * 2 + (
        "3/3" if co_git else "BỎ QUA (không có .git)",) + (len(viec),) * 2), file=sys.stderr)
    return True
