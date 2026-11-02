# ---------------------------------------------------------------------------------------------
# B8 — ca khoá lớp `sua-124-trong-packet` (MÃ TEST THUẦN của đặc tả r12; executor tự dẫn xuất lại,
# tự đo). Bất biến: "124 ⇔ cả cây ĐÃ CHẾT" và "stop rc=0 ⇔ cây đã sạch" không phụ thuộc cách giải
# mã `comm`. Kích hoạt THẬT: kernel cắt `comm` ở 15 byte, nên tên tiếng Việt thành UTF-8 hỏng.
# ---------------------------------------------------------------------------------------------
_K124_COMM = bytes.fromhex("6b69e1bb836d5f7472615f7469e1ba")   # 'kiểm_tra_tiến_trình'.encode()[:15]
# Cháu của t160/t161 (r11): comm có `) ` (tên thật kiểu `tep (1).sh`) + đuôi UTF-8 hỏng — phủ trục S ở ba hàm ngoài:
# phép tách theo `)` ĐẦU (index/partition/split) lệch trường ở _khoa_danh_tinh, _thanh_vien_nhom, _chup_cay.
_K124_COMM_CHAU = b"tep (1) " + _K124_COMM[8:]                 # 15 byte: 'tep (1) ra_ti' + e1 ba
_NL = chr(10)

# Dạng đọc /proc/<pid>/stat theo Q-A.7 mà ứng viên KHAI (một chỗ, helper t156/t157 và B8 dùng chung):
# (tên phương thức Path, args, kwargs) — ví dụ ("read_bytes", (), {}) nếu chọn đọc bytes.
DANG_DOC_QA7 = ("read_text", (), {"encoding": "latin-1"})


def _k124_song(pid: int) -> bool:
    """Sống THẬT theo /proc đọc BYTES — không giải mã `comm`; zombie = đã chết."""
    try:
        with open(f"/proc/{pid}/stat", "rb") as f:
            nd = f.read()
    except (FileNotFoundError, ProcessLookupError):
        return False
    return nd[nd.rindex(b")") + 2:].split()[0] != b"Z"


def _k124_locale_giai_ma_duoc() -> bool:
    """`read_text()` không đối số giải mã theo mã hoá này; giải mã được 15 byte hỏng thì lỗi 124 KHÔNG tái hiện được."""
    import locale
    try:
        _K124_COMM.decode(locale.getpreferredencoding(False))
    except (UnicodeDecodeError, LookupError):
        return False
    return True


def _k124_don_con(tn):
    """Dọn con B8 bằng PID do CHÍNH con ghi (không tin PID launcher-đang-thử báo), chỉ khi cmdline mang đường nhịp."""
    tp = Path(str(tn) + ".pid")
    _k124_cho_tep(tp, 2.0)
    try:
        pid = int(tp.read_text())
        with open(f"/proc/{pid}/cmdline", "rb") as f:
            cua_ta = str(tn).encode() in f.read()
    except (OSError, ValueError):
        return
    if cua_ta:
        with contextlib.suppress(OSError):
            os.kill(pid, signal.SIGKILL)


_K124_MO = {"cai": False, "bat": False, "trong": 0, "ngoai": []}


def _k124_audit(ev, args):
    """Cửa sổ B8: mọi sự kiện audit `open` trên `/proc/…`, trên đường tương đối (`dir_fd`) hay trên fd số phải nằm
    TRONG một lời đọc Path đã ghi — danh sách cho phép ở tầng API (`open()`, `Path.open()`, `os.open`, đường
    `/proc/<pid>/task/…`, và ống PIPE mà `subprocess` bọc bằng `io.open` trên fd số, đều là `open` NGOÀI). Thước đo
    này KHÔNG thấy đường tuyệt đối ngoài `/proc` (`//proc/…`, tệp tạm) hay ống `os.pipe` đọc bằng `os.read` (đo) —
    phần ấy do chốt tĩnh và seam đếm đọc giữ. Đường tuyệt đối ngoài `/proc` không tính vì máy nạp module mở `.pyc`
    của codec một cách lười, ngay trong cửa sổ (đo)."""
    if _K124_MO["bat"] and ev == "open" and not _K124_MO["trong"]:
        p = args[0] if isinstance(args[0], int) else os.fsdecode(args[0])
        if isinstance(p, int) or not p.startswith("/") or p.startswith("/proc/"):
            _K124_MO["ngoai"].append(p)


@contextlib.contextmanager
def _k124_ghi_doc():
    """Ghi (phương thức, args, kwargs) của MỌI lời đọc Path trên /proc/<số>/stat trong cửa sổ, và ghi mọi sự kiện
    audit `open` xảy ra NGOÀI các lời đọc ấy: lời đọc Path đã ghi là đường mở tệp DUY NHẤT được phép."""
    if not _K124_MO["cai"]:
        sys.addaudithook(_k124_audit)          # không gỡ được; ngoài cửa sổ hook không làm gì
        _K124_MO["cai"] = True
    ghi = []
    goc = {t: (t in Path.__dict__, getattr(Path, t)) for t in ("read_text", "read_bytes")}

    def boc(ten, g):
        def f(self, *a, **k):
            p = str(self)
            if not (p.startswith("/proc/") and p.endswith("/stat") and p[6:-5].isdigit()):
                return g(self, *a, **k)
            ghi.append((ten, a, k))
            _K124_MO["trong"] += 1
            try:
                return g(self, *a, **k)
            finally:
                _K124_MO["trong"] -= 1
        return f
    for t, (_co, g) in goc.items():
        setattr(Path, t, boc(t, g))
    _K124_MO.update(bat=True, trong=0, ngoai=[])
    try:
        yield ghi
    finally:
        _K124_MO["bat"] = False
        for t, (co, g) in goc.items():
            if co:
                setattr(Path, t, g)
            else:
                delattr(Path, t)


def _k124_ma_con(tep_comm, tep_nhip, cho: float, doi_comm: bool) -> str:
    """Con: ghi PID của chính nó, (tuỳ chọn) chờ `cho` giây rồi đổi comm thành 15 byte hỏng, ghi comm THẬT
    (bytes) ra tệp, rồi ghi nhịp mỗi 0,1 s — tối đa 1200 nhịp (khoảng 120 s) rồi tự thoát: hạn sống. Mọi lối
    thoát KHÔNG do tín hiệu ghi `<tệp nhịp>.tu_thoat` (`han_song` / `ngoai_le`) — ca không phải cha của con."""
    dong = ["import ctypes, os, time",
            f"open({str(tep_nhip) + '.pid'!r}, 'w').write(str(os.getpid()))",
            "ly_do = 'ngoai_le'",
            "try:",
            f"    time.sleep({cho})"]
    if doi_comm:
        dong.append(f"    ctypes.CDLL(None).prctl(15, bytes.fromhex({_K124_COMM.hex()!r}), 0, 0, 0)")
    dong += ["    nd = open('/proc/%d/stat' % os.getpid(), 'rb').read()",
             f"    open({str(tep_comm)!r}, 'wb').write(nd[nd.index(b'(') + 1:nd.rindex(b')')])",
             f"    f = open({str(tep_nhip)!r}, 'a')",
             "    for _ in range(1200):",
             "        f.write('.'); f.flush(); time.sleep(0.1)",
             "    ly_do = 'han_song'",
             "finally:",
             f"    open({str(tep_nhip) + '.tu_thoat'!r}, 'w').write(ly_do)"]
    return _NL.join(dong) + _NL


def _k124_tu_thoat(tep):
    """Dấu TỰ THOÁT mà chính tiến trình ghi ở `finally`: `han_song`, `ngoai_le`; None = không tự thoát (tín hiệu
    giết nó, hay nó còn sống). Tín hiệu mặc định giết tiến trình KHÔNG chạy `finally`, nên dấu phân biệt được hai
    đường mà "đã chết" gộp làm một."""
    try:
        return Path(str(tep) + ".tu_thoat").read_text()
    except FileNotFoundError:
        return None


def _k124_tu_thoat_vo_can(ten, tu):
    if tu not in (None, "han_song"):
        raise RuntimeError(f"dieu kien dung: {ten} tien trinh do ca sinh chet vi {tu} - khong bi giet, khong het han")


def _k124_cho_tep(p, han=10.0):
    het = time.time() + han
    while time.time() < het:
        if p.exists() and p.stat().st_size:
            return True
        time.sleep(0.05)
    return False


def _k124_run(s, lenh):
    """`launcher.py run --deadline-utc` thật (hạn 3 s); trả (rc, sổ run.json dạng --json)."""
    repo = tao_repo(s)
    r = chay("run", "--workspace", str(repo), "--run-root", str(s / "runs"), "--json",
             "--deadline-utc", mai_sau(3), "--", *lenh)
    so = {}
    dong = [d for d in r.stdout.splitlines() if d.startswith("{")]
    if dong:
        so = json.loads(dong[-1])
    if not so.get("pid") or r.returncode not in (MA_QUA_HAN, 125, MA_DANH_TINH):
        raise RuntimeError(f"dieu kien dung: launcher khong ket thuc bang ma han chot 124/125/10 kem so JSON: "
                           f"rc={r.returncode}, stderr={r.stderr[-160:]!r}")
    return r.returncode, so


def _k124_ket_luan(ten, rc, pid, tn):
    """Hai assertion, đúng thứ tự: (1) 124 KHÔNG đi cùng cây còn sống; (2) quá hạn phải GIẾT — con TỰ THOÁT ở hạn
    sống là KHÔNG bị giết (ĐỎ); con chết vì ngoại lệ là lỗi điều kiện dựng (không phải TinHieuChotCa)."""
    n1 = tn.stat().st_size if tn.exists() else 0
    time.sleep(1.0)
    n2 = tn.stat().st_size if tn.exists() else 0
    tu = _k124_tu_thoat(tn)
    _k124_tu_thoat_vo_can(ten, tu)
    song = bool(pid) and _k124_song(pid)
    bang(not (rc == MA_QUA_HAN and (song or n2 != n1)),
         f"{ten} 124 noi doi: rc={rc}, con {pid} song={song}, nhip {n1}->{n2}")
    bang(rc == MA_QUA_HAN and not song and n2 == n1 and tu is None,
         f"{ten} qua han khong giet duoc: rc={rc}, con {pid} song={song}, nhip {n1}->{n2}, tu thoat={tu}")


def _k124_dang_doc(ten, ghi):
    """(3) `read args`: mọi lời đọc /proc/<pid>/stat trong cửa sổ đúng DANG_DOC_QA7, và không `open` nào ngoài chúng."""
    if not ghi:
        raise RuntimeError(f"dieu kien dung: {ten} khong co loi doc /proc/<pid>/stat nao")
    lech = sorted({repr(x) for x in ghi if x != DANG_DOC_QA7})
    if _K124_MO["ngoai"]:                      # mở tệp ngoài lời đọc Path đã ghi: danh sách cho phép đóng ở MỌI API
        lech.insert(0, f"open ngoai loi doc Path: {len(_K124_MO['ngoai'])} su kien, vd {_K124_MO['ngoai'][:2]}")
    bang(not lech, f"{ten} read args {lech[:3]}")


def _k124_khoa_that(pid: int) -> str:
    """Khoá theo ĐỊNH DẠNG NỀN `linux:<starttime>` (trường 22), đọc BYTES độc lập — neo định dạng khoá của Q-A.7."""
    bat, _K124_MO["bat"] = _K124_MO["bat"], False      # lời đọc của CHÍNH ca: không đếm vào `open` của cửa sổ
    try:
        with open(f"/proc/{pid}/stat", "rb") as f:
            nd = f.read()
    finally:
        _K124_MO["bat"] = bat
    return "linux:" + nd[nd.rindex(b")") + 2:].split()[19].decode("ascii")


@ca
def t158_comm_hong_SAU_luc_sinh_qua_han_khong_duoc_124_khi_con_song():
    """`run --deadline-utc`: con đổi comm thành UTF-8 hỏng SAU khi launcher lấy khoá (nền 89fc4fa:
    rc=124, `giet_tron_ven=True`, con vẫn sống)."""
    if platform.system() != "Linux":
        return "bo qua: comm/prctl/proc chi co tren Linux"
    if _k124_locale_giai_ma_duoc():
        return "bo qua: locale hien hanh giai ma duoc 15 byte comm hong - loi 124 khong tai hien duoc o day"
    with San() as s:
        tc, tn = s / "comm.bin", s / "nhip.txt"
        try:
            rc, so = _k124_run(s, [PY, "-c", _k124_ma_con(tc, tn, 0.5, True)])
            pid = so.get("pid")
            if not (_k124_cho_tep(tc, 1) and tc.read_bytes() == _K124_COMM):
                raise RuntimeError("dieu kien dung: con chua doi comm thanh 15 byte hong")
            if not so.get("khoa_danh_tinh"):
                raise RuntimeError("dieu kien dung: comm hong TRUOC luc lay khoa (ca nay can SAU)")
            _k124_ket_luan("B8-sau-sinh", rc, pid, tn)
        finally:
            _k124_don_con(tn)


@ca
def t159_chuong_trinh_ten_tieng_Viet_qua_han_phai_giet_duoc():
    """Tên chương trình tiếng Việt ⇒ comm hỏng NGAY LÚC SINH (kernel cắt 15 byte), không cần prctl
    (nền 89fc4fa: `khoa=None`, rc=10, con vẫn sống)."""
    if platform.system() != "Linux":
        return "bo qua: comm/proc chi co tren Linux"
    if _k124_locale_giai_ma_duoc():
        return "bo qua: locale hien hanh giai ma duoc 15 byte comm hong - loi 124 khong tai hien duoc o day"
    with San() as s:
        ten = s / "kiểm_tra_tiến_trình"
        try:
            os.symlink(PY, ten)
        except (OSError, UnicodeEncodeError) as e:
            raise RuntimeError(f"dieu kien dung: khong tao duoc ten tieng Viet: {e}")
        tc, tn = s / "comm.bin", s / "nhip.txt"
        try:
            rc, so = _k124_run(s, [str(ten), "-c", _k124_ma_con(tc, tn, 0.0, False)])
            pid = so.get("pid")
            if not (_k124_cho_tep(tc, 1) and tc.read_bytes() == _K124_COMM):
                raise RuntimeError("dieu kien dung: comm luc sinh khong phai 15 byte hong")
            _k124_ket_luan("B8-luc-sinh", rc, pid, tn)
        finally:
            _k124_don_con(tn)


_K124_MA_CHAU = _NL.join([
    "import ctypes, os, signal, sys, time",
    "signal.signal(signal.SIGTERM, signal.SIG_IGN)",
    "ly_do = 'ngoai_le'",
    "try:",
    "    ctypes.CDLL(None).prctl(15, bytes.fromhex(sys.argv[2]), 0, 0, 0)",
    "    open(sys.argv[1], 'w').write(str(os.getpid()))",
    "    time.sleep(120)",
    "    ly_do = 'han_song'",
    "finally:",
    "    open(sys.argv[1] + '.tu_thoat', 'w').write(ly_do)"]) + _NL
_K124_MA_ME = _NL.join([
    "import subprocess, sys, time",
    "subprocess.Popen([sys.executable, '-c', sys.argv[5], sys.argv[2], sys.argv[3]],",
    "                 start_new_session=(sys.argv[1] == '1'))",
    "if sys.argv[4] == 'thoat':",
    "    sys.stdin.readline()",
    "    sys.exit(0)",
    "time.sleep(120)"]) + _NL


def _k124_me_chau(s, setsid: bool, me_thoat: bool):
    tp = s / "chau.pid"
    me = subprocess.Popen([PY, "-c", _K124_MA_ME, "1" if setsid else "0", str(tp), _K124_COMM_CHAU.hex(),
                           "thoat" if me_thoat else "o_lai", _K124_MA_CHAU],
                          start_new_session=True, stdin=subprocess.PIPE)
    chau = None
    try:
        if not _k124_cho_tep(tp):
            raise RuntimeError("dieu kien dung: chau chua ghi pid")
        chau = int(tp.read_text())
        with open(f"/proc/{chau}/stat", "rb") as f:
            nd = f.read()
        if nd[nd.index(b"(") + 1:nd.rindex(b")")] != _K124_COMM_CHAU:
            raise RuntimeError("dieu kien dung: comm cua chau chua doi")
    except BaseException:
        if chau:
            with contextlib.suppress(OSError):
                os.kill(chau, signal.SIGKILL)
        with contextlib.suppress(OSError):
            me.kill()
        me.wait()
        raise
    return me, chau


@ca
def t160_giet_cay_chau_setsid_comm_hong_phot_lo_SIGTERM():
    """Cháu `setsid()` (killpg không với tới), comm hỏng, phớt lờ SIGTERM: chỉ ẢNH CHỤP + kiểm
    sống/khoá từng pid giết được nó. Phủ `_chup_cay`, `_con_song` nhánh tệp có, `_khoa_danh_tinh`."""
    if platform.system() != "Linux":
        return "bo qua: setsid/proc chi co tren Linux"
    m = _tai_launcher_thu()
    with San() as s:
        me, chau = _k124_me_chau(s, True, False)
        try:
            with _k124_ghi_doc() as ghi:
                khoa = _k124_khoa_that(me.pid)
                kg = m._giet_cay(me.pid, khoa)
            song = _k124_song(chau)
            me_rc = me.poll()   # mẹ là con TRỰC TIẾP của ca: None = còn sống; < 0 = tín hiệu giết; >= 0 = tự thoát
            tu = _k124_tu_thoat(s / "chau.pid")
            _k124_tu_thoat_vo_can("B8-setsid", tu)
            bang(not (kg.tron_ven and (song or me_rc is None)),
                 f"B8-setsid 124 noi doi: {kg.mo_ta}; chau {chau} song={song}, me rc={me_rc}")
            bang(kg.tron_ven and not song and tu is None and me_rc is not None and me_rc < 0,
                 f"B8-setsid khong giet duoc: tron_ven={kg.tron_ven}, chau song={song}, chau tu thoat={tu}, "
                 f"me rc={me_rc}, {kg.mo_ta}")
            _k124_dang_doc("B8-setsid", ghi)
        finally:
            with contextlib.suppress(OSError):
                os.kill(chau, signal.SIGKILL)
            with contextlib.suppress(OSError):
                me.kill()
            me.wait()


@ca
def t161_giet_cay_me_da_thoat_chau_cung_nhom_comm_hong():
    """Mẹ đã thoát, cháu CÙNG NHÓM comm hỏng còn sống: `_khoa_danh_tinh(me)` = None là ĐÚNG (mẹ đã
    biến mất) và chỉ phép quét nhóm còn thấy cháu. Phủ `_thanh_vien_nhom` (và `_chup_cay` theo nhóm)."""
    if platform.system() != "Linux":
        return "bo qua: nhom tien trinh/proc chi co tren Linux"
    m = _tai_launcher_thu()
    with San() as s:
        me, chau = _k124_me_chau(s, False, True)
        try:
            with _k124_ghi_doc() as ghi:
                khoa = _k124_khoa_that(me.pid)
                me.stdin.write(b"x" + _NL.encode())
                me.stdin.close()
                me.wait(timeout=10)
                kg = m._giet_cay(me.pid, khoa)
            song = _k124_song(chau)
            tu = _k124_tu_thoat(s / "chau.pid")
            _k124_tu_thoat_vo_can("B8-me-thoat", tu)
            bang(not (kg.tron_ven and song), f"B8-me-thoat 124 noi doi: {kg.mo_ta}; chau {chau} song")
            bang(kg.tron_ven and not song and tu is None, f"B8-me-thoat khong giet duoc: tron_ven={kg.tron_ven}, "
                                                          f"chau song={song}, chau tu thoat={tu}, {kg.mo_ta}")
            _k124_dang_doc("B8-me-thoat", ghi)
        finally:
            with contextlib.suppress(OSError):
                os.kill(chau, signal.SIGKILL)
            with contextlib.suppress(OSError):
                me.kill()
            me.wait()
