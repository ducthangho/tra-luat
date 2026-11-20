# -*- coding: utf-8 -*-
"""Bundle tách mảnh: mỗi mảnh dưới ngưỡng WARN, nạp đúng mảnh được KHAI, kiểm cổng phát hiện mảnh lạc."""

import ast
import contextlib
import hashlib
import importlib
import io
import json
from pathlib import Path
import tempfile

TEST_ID = "wp433_bundled_tach_manh"

_WARN = 280 * 1024
# sha256 của `generate_bundled_module_bytes` trên base 0f9aa2a cho fixture `wp9001_a.py` (216 B); KHÔNG tính lại từ mã sau sửa.
_MOT_MANH_SHA256 = "73ad44659b63aea9b2f66fb1104c4c82deaa1ad1218e94adb80dcf38384441d7"
_NHAN = ("P1_mot_manh", "P2_nhieu_manh", "P3_chi_nap_manh_khai", "P4_cong_bao_manh_lac", "P5_ghi_xoa_lac",
         "P6_thieu_manh", "P7_thu_tu_xuyen_manh", "P8_trung_xuyen_manh", "P9_manh_tu_khai", "P10_kho_that")
_KQ = {}
_M1 = "tl_test_fragments_bundled.py"
_M2, _M3, _M9 = (f"tl_test_fragments_bundled_{k}.py" for k in (2, 3, 9))
_CONTRACT = "BUNDLED_MODULE_CONTRACT"


def _nguon(name, pad=0):
    return f'TEST_ID = "{name[:-3]}"\n_PAD = "{"x" * pad}"\n\n\ndef run(tl_module):\n    return True\n'


def _frag(root, name, pad=0):
    (root / name).write_text(_nguon(name, pad), encoding="utf-8", newline="\n")


def _manh(path, names, khai=None):
    """Viết TAY một mảnh data-only (không qua generator) để P3, P6–P9 không phụ thuộc generator."""
    text = "BUNDLED_FRAGMENT_SOURCES = (\n" + "".join(
        f"    ({json.dumps(n)}, {json.dumps(_nguon(n))}),\n" for n in names) + ")\n"
    if khai is not None:
        text += f"BUNDLED_FRAGMENT_SHARDS = {khai!r}\n"
    path.write_text(text, encoding="utf-8", newline="\n")


def _nap(tf, scripts):
    try:
        return [c.test_id for c in tf.load_runtime_fragment_cases(scripts)], None, ""
    except Exception as exc:  # noqa: BLE001
        return None, getattr(exc, "code", type(exc).__name__), str(exc)


def _check(tl_module, root):
    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        try:
            rc = tl_module.main(["test-fragments-check", "--root", str(root), "--json"])
        except SystemExit as exc:
            rc = int(exc.code or 0)
    try:
        return rc, json.loads(out.getvalue())
    except ValueError:
        return rc, {}


def _khai_cua(data):
    """Giá trị tuple BUNDLED_FRAGMENT_SHARDS của một mảnh (None nếu không có phép gán ấy)."""
    for node in ast.parse(data.decode("utf-8")).body:
        if isinstance(node, ast.Assign) and getattr(node.targets[0], "id", "") == "BUNDLED_FRAGMENT_SHARDS":
            return ast.literal_eval(node.value)
    return None


def _do(base, tf, tl_module):
    """Trả 10 hàm đo, mỗi hàm một tính chất; hàm nào văng thì nhãn ấy False, các nhãn khác vẫn được tính."""
    names = [f"wp9001_f{i}.py" for i in range(6)]
    ids = [n[:-3] for n in names]
    r2 = base / "r2" / "scripts"          # fixture qua generator: 6 × 40 KiB, hạn 100 KiB
    fr = r2 / "test_fragments"
    r3 = base / "r3" / "scripts"          # fixture viết tay, topology bundle (không có test_fragments/)
    stray = r2 / _M9

    def han(fn):
        old = tf._BUNDLED_SHARD_LIMIT
        tf._BUNDLED_SHARD_LIMIT = 100 * 1024
        try:
            return fn()
        finally:
            tf._BUNDLED_SHARD_LIMIT = old

    def dung_r2():
        if not fr.is_dir():
            fr.mkdir(parents=True)
            for n in names:
                _frag(fr, n, pad=40 * 1024)
        return han(lambda: tf.write_bundled_modules(fr, r2))

    def dung_r3():
        r3.mkdir(parents=True, exist_ok=True)
        _manh(r3 / _M1, names[:2], (_M2, _M3))
        _manh(r3 / _M2, names[2:4])
        _manh(r3 / _M3, names[4:])
        if (r3 / _M9).exists():
            (r3 / _M9).unlink()

    def p1():
        root = base / "r1" / "test_fragments"
        root.mkdir(parents=True)
        _frag(root, "wp9001_a.py")
        mods = tf.generate_bundled_modules(root)
        cu = tf.generate_bundled_module_bytes(root)
        return (len(mods) == 1 and _khai_cua(mods[0][1]) is None
                and hashlib.sha256(mods[0][1]).hexdigest() == _MOT_MANH_SHA256
                and hashlib.sha256(cu).hexdigest() == _MOT_MANH_SHA256)

    def p2():
        written = dung_r2()
        mods = han(lambda: tf.generate_bundled_modules(fr))
        dich = r2.parent / "nap"           # bản sao chỉ gồm các mảnh ⇒ topology bundle
        dich.mkdir()
        for name in written:
            (dich / name).write_bytes((r2 / name).read_bytes())
        got, err, _ = _nap(tf, dich)
        return (tuple(written) == (_M1, _M2, _M3) == tuple(n for n, _ in mods)
                and [d.count(b'\n    ("wp9001_f') for _, d in mods] == [2, 2, 2]
                and _khai_cua(mods[0][1]) == (_M2, _M3)
                and all(_khai_cua(d) is None for _, d in mods[1:])
                and err is None and got == ids)

    def p3():
        dung_r3()
        truoc = _nap(tf, r3)
        _manh(r3 / _M9, ["wp9001_f6.py"])
        sau = _nap(tf, r3)
        return truoc[:2] == (ids, None) and sau[:2] == (ids, None)

    def p4():
        dung_r2()
        stray.write_bytes((r2 / _M1).read_bytes())
        rc, j = han(lambda: _check(tl_module, r2.parent))
        return rc != 0 and j.get("error") == "GENERATED_BUNDLE_STALE" and j.get("extra_shards") == [_M9]

    def p5():
        dung_r2()
        stray.write_bytes(b"BUNDLED_FRAGMENT_SOURCES = ()\n")
        han(lambda: tf.write_bundled_modules(fr, r2))
        rc, j = han(lambda: _check(tl_module, r2.parent))
        return not stray.exists() and rc == 0 and j.get("ok") is True

    def p6():
        dung_r3()
        (r3 / _M2).unlink()
        _, err, msg = _nap(tf, r3)
        return err == "BUNDLED_MODULE_MISSING" and f"scripts/{_M2}" in msg

    def p7():
        dung_r3()
        _manh(r3 / _M2, names[4:])
        _manh(r3 / _M3, names[2:4])
        return _nap(tf, r3)[1] == _CONTRACT

    def p8():
        dung_r3()
        _manh(r3 / _M3, names[3:])         # f3 là cuối mảnh 2 VÀ đầu mảnh 3; thứ tự toàn chuỗi không giảm
        return _nap(tf, r3)[1] == _CONTRACT

    def p9():
        dung_r3()
        _manh(r3 / _M3, names[4:], (_M2,))
        return _nap(tf, r3)[1] == _CONTRACT

    def p10():
        repo = Path(tf.__file__).resolve().parent.parent / "test_fragments"
        real = tf.generate_bundled_modules(repo) if repo.is_dir() else ()
        return tf._BUNDLED_SHARD_LIMIT == 196608 and all(len(d) <= 0.7 * _WARN for _, d in real)

    return (p1, p2, p3, p4, p5, p6, p7, p8, p9, p10)


def run(tl_module):
    tf = importlib.import_module("tl_core.test_fragments")
    _KQ.clear()
    with tempfile.TemporaryDirectory(prefix="wp433_bt_") as tmp:
        for nhan, fn in zip(_NHAN, _do(Path(tmp), tf, tl_module)):
            try:
                _KQ[nhan] = fn() is True
            except Exception:  # noqa: BLE001 — văng ⇒ nhãn False, không bỏ dở các nhãn sau
                _KQ[nhan] = False
    return len(_KQ) == 10 and all(value is True for value in _KQ.values())
