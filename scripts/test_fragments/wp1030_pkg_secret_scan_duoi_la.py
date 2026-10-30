# -*- coding: utf-8 -*-
"""wp1030 — `pkg_secret_scan`: tệp có đuôi lạ đi cùng phép lọc nhị phân như tệp không đuôi.

Chạy BẢN THẬT của `scripts/pkg_secret_scan.py` (đọc nguồn rồi `exec`, không qua bộ đệm `.pyc`) trên một fixture
trong thư mục tạm. Khoá giả dựng lúc chạy từ các mảnh, nên chính tệp này không thành hit của bộ quét. So bằng TẬP
đường dẫn hit, không bằng số đếm. Fixture biên riêng khoá hai phía của trần `MAX_BYTES` và của cửa sổ kiểm NUL
8192 byte, cùng việc tệp `TEXT_SUFFIXES` (kể cả đuôi viết HOA) vẫn được miễn cả hai phép lọc. Tên tệp trong fixture
khác nhau cả khi bỏ phân biệt hoa thường, để ca đo đúng trên hệ tệp Windows/macOS.

Topo phát hành: bundle của fragment nằm trong gói, còn bộ quét thì bị loại khỏi gói. Chỉ tha (in `BỎ QUA`, trả True)
khi đủ ba điều: (i) bộ quét vắng; (ii) chính sách phát hành loại nó THEO THIẾT KẾ, đo trên một sentinel CÓ THẬT
(`_release_should_include` kết thúc bằng `path.is_file()`, nên gọi trên tệp vắng luôn ra False bất kể chính sách);
(iii) gốc không có `.git`. Mọi lỗi khi kiểm ⇒ False.
"""

import contextlib
import io
import os
from pathlib import Path
import sys
import tempfile
import types


TEST_ID = "wp1030_pkg_secret_scan_duoi_la"

_MAU = "google_oauth_client_secret"


def _bao(msg):
    print("[%s] FAIL %s" % (TEST_ID, msg), file=sys.stderr)


def _khoa():
    # Dựng từ mảnh: không có nguyên chuỗi khớp mẫu trong mã nguồn.
    return "GOC" + "SPX" + "-" + "".join(chr(ord("a") + (i % 26)) for i in range(28))


def _nap(quet):
    mod = types.ModuleType("_wp1030_pkg_secret_scan")
    mod.__file__ = str(quet)
    exec(compile(quet.read_bytes(), str(quet), "exec"), mod.__dict__)
    return mod


def _co_mat(path):
    # Chỉ ENOENT chứng minh vắng; lỗi quyền/I/O/độ dài phải tới catch fail-closed của run.
    try:
        os.lstat(path)                    # giữ ngữ nghĩa symlink hỏng là CÓ MẶT
    except FileNotFoundError:
        return False
    return True


def _ly_do_tha(tl_module, kho):
    """Trả lý do tha khi (ii) và (iii) cùng đúng; None nếu không được tha. Lỗi ném ra ngoài ⇒ người gọi trả False."""
    if _co_mat(kho / ".git"):
        return None                                     # (iii): checkout có .git mà thiếu bộ quét ⇒ ĐỎ
    with tempfile.TemporaryDirectory() as tam:
        goc = Path(tam)
        sentinel = goc / "scripts" / "pkg_secret_scan.py"
        sentinel.parent.mkdir(parents=True)
        sentinel.write_bytes(b"")
        if not sentinel.is_file():
            return None
        if tl_module._release_should_include(sentinel, goc) is not False:
            return None                                 # (ii): chính sách GIỮ bộ quét trong gói mà gói lại thiếu ⇒ ĐỎ
    return "bộ quét vắng, chính sách phát hành loại nó (sentinel), cây không có .git"


def _hit(mod, goc):
    return list(mod.scan(goc))


def _tap(hits):
    return {h.split(":", 1)[0].replace(os.sep, "/") for h in hits}


def _main(mod, goc):
    with contextlib.redirect_stdout(io.StringIO()):
        return mod.main(["pkg_secret_scan.py", str(goc)])


def _ca(mod):
    ok = True
    khoa = _khoa()
    dong = ("dong 1\n%s\ndong 3\n" % khoa).encode("utf-8")
    with tempfile.TemporaryDirectory() as tam:
        goc = Path(tam) / "a1"
        goc.mkdir()
        for ten in ("a.log", "b.patch", "c.csv", "d.txt"):
            (goc / ten).write_bytes(dong)
        (goc / "e.dat").write_bytes(b"\x00\x01" + khoa.encode("ascii") + b"\n")
        tran = int(mod.MAX_BYTES)
        dau = (khoa + "\n").encode("ascii")
        (goc / "f.log").write_bytes(dau + b"x" * (tran + 1 - len(dau)))
        if (goc / "f.log").stat().st_size != tran + 1:
            _bao("A1 fixture f.log lệch kích thước")
            return False

        # A1 — ca dương theo từng vị trí, khẳng định bằng TẬP.
        hits = _hit(mod, goc)
        mong = {"a.log", "b.patch", "c.csv", "d.txt"}
        thuc = _tap(hits)
        if thuc != mong:
            _bao("A1 tập hit lệch: thiếu %s, thừa %s" % (sorted(mong - thuc), sorted(thuc - mong)))
            ok = False
        sai_dong = sorted(h for h in hits if not h.endswith(":2: " + _MAU))
        if sai_dong:
            _bao("A1 hit sai dòng/mẫu: %s" % sai_dong)
            ok = False
        if _main(mod, goc) != 1:
            _bao("A1 main(thư mục có khoá) != 1")
            ok = False

        am = Path(tam) / "a1_am"
        am.mkdir()
        (am / "e.dat").write_bytes((goc / "e.dat").read_bytes())
        (am / "f.log").write_bytes((goc / "f.log").read_bytes())
        rc_am = _main(mod, am)
        if rc_am != 0:
            _bao("A1 main(chỉ e.dat + f.log) = %r != 0; hit: %s" % (rc_am, sorted(_tap(_hit(mod, am)))))
            ok = False

        # A2 — nhánh cũ không đổi, trên CÙNG fixture.
        (goc / "credentials").write_bytes(dong)
        (goc / "pkg_secret_scan.py").write_bytes(dong)
        hits2 = _hit(mod, goc)
        mong2 = mong | {"credentials"}
        thuc2 = _tap(hits2)
        if thuc2 != mong2:
            _bao("A2 tập hit lệch: thiếu %s, thừa %s" % (sorted(mong2 - thuc2), sorted(thuc2 - mong2)))
            ok = False
    return ok


def _ca_bien(mod):
    """Hai phía của mỗi biên lọc, và nhánh `TEXT_SUFFIXES` được miễn cả hai phép lọc (đuôi thường lẫn HOA)."""
    khoa = _khoa().encode("ascii")
    dong = b"dong 1\n" + khoa + b"\n"
    tran = int(mod.MAX_BYTES)
    cua_so = 8192
    tep = {
        "dung_tran.log": dong + b"x" * (tran - len(dong)),          # = trần ⇒ quét
        "qua_tran.log": dong + b"x" * (tran + 1 - len(dong)),       # trần + 1 ⇒ bỏ
        "nul_cuoi_cua_so.log": b"x" * (cua_so - 1) + b"\x00\n" + khoa + b"\n",   # NUL ở byte thứ 8192 ⇒ bỏ
        "nul_ngoai_cua_so.log": b"x" * cua_so + b"\x00\n" + khoa + b"\n",        # NUL ở byte thứ 8193 ⇒ quét
        "dung_tran_khong_duoi": dong + b"x" * (tran - len(dong)),
        "qua_tran_khong_duoi": dong + b"x" * (tran + 1 - len(dong)),
        "nul_khong_duoi": b"\x00\n" + khoa + b"\n",
        "nul_cuoi_cua_so_khong_duoi": b"x" * (cua_so - 1) + b"\x00\n" + khoa + b"\n",
        "nul_ngoai_cua_so_khong_duoi": b"x" * cua_so + b"\x00\n" + khoa + b"\n",
        "lon.txt": dong + b"x" * tran,                              # TEXT_SUFFIXES: không trần
        "nul.txt": b"\x00\n" + khoa + b"\n",                        # TEXT_SUFFIXES: không kiểm NUL
        "hoa_lon.TXT": dong + b"x" * tran,                          # đuôi HOA vẫn thuộc TEXT_SUFFIXES
        "hoa_nul.TXT": b"\x00\n" + khoa + b"\n",
    }
    mong = {"dung_tran.log", "nul_ngoai_cua_so.log", "dung_tran_khong_duoi", "nul_ngoai_cua_so_khong_duoi",
            "lon.txt", "nul.txt", "hoa_lon.TXT", "hoa_nul.TXT"}
    with tempfile.TemporaryDirectory() as tam:
        goc = Path(tam) / "bien"
        goc.mkdir()
        for ten, noi_dung in tep.items():
            (goc / ten).write_bytes(noi_dung)
        co_mat = {p.name for p in goc.iterdir()}
        if co_mat != set(tep):
            _bao("BIÊN fixture lệch (hệ tệp gộp tên?): %s" % sorted(set(tep) ^ co_mat))
            return False
        thuc = _tap(_hit(mod, goc))
    if thuc != mong:
        _bao("BIÊN tập hit lệch: thiếu %s, thừa %s" % (sorted(mong - thuc), sorted(thuc - mong)))
        return False
    return True


def run(tl_module):
    try:
        kho = Path(tl_module.__file__).resolve().parent.parent
        quet = kho / "scripts" / "pkg_secret_scan.py"
        if not _co_mat(quet):                           # (i)
            ly_do = _ly_do_tha(tl_module, kho)
            if ly_do is None:
                _bao("bộ quét vắng mà không đủ điều kiện tha: %s" % quet)
                return False
            print("[%s] BỎ QUA (%s)" % (TEST_ID, ly_do), file=sys.stderr)
            return True
        mod = _nap(quet)
    except Exception as exc:                            # fail-closed
        _bao("không kiểm được topo/nạp bộ quét: %s" % type(exc).__name__)
        return False
    try:
        a = _ca(mod)
        b = _ca_bien(mod)
    except Exception as exc:                            # fixture/thư mục tạm hỏng ⇒ ĐỎ có chẩn đoán, không bao giờ True
        _bao("không dựng/đo được fixture: %s: %s" % (type(exc).__name__, exc))
        return False
    return a and b
