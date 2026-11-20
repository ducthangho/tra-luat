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
_KHOA = tuple(f"V{i}" for i in range(1, 18))   # V1–V17 của đặc tả §4, mỗi vế một khoá
_KQ = {}
_M1 = "tl_test_fragments_bundled.py"
_M2, _M3, _M9 = (f"tl_test_fragments_bundled_{k}.py" for k in (2, 3, 9))
_CONTRACT, _MISSING, _STALE = "BUNDLED_MODULE_CONTRACT", "BUNDLED_MODULE_MISSING", "GENERATED_BUNDLE_STALE"


def _nguon(name, pad=0):
    return f'TEST_ID = "{name[:-3]}"\n_PAD = "{"x" * pad}"\n\n\ndef run(tl_module):\n    return True\n'


def _frag(root, name, pad=0):
    (root / name).write_text(_nguon(name, pad), encoding="utf-8", newline="\n")


def _manh(path, names, khai=None):
    """Viết TAY một mảnh data-only (không qua generator) để các vế loader V7–V13 không phụ thuộc generator."""
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


def _gan(data):
    """Đọc ĐỘC LẬP (AST) một mảnh sinh ra: (danh sách tên fragment, giá trị SHARDS hoặc None)."""
    gan = {node.targets[0].id: ast.literal_eval(node.value)
           for node in ast.parse(data.decode("utf-8")).body if isinstance(node, ast.Assign)}
    return [n for n, _ in gan["BUNDLED_FRAGMENT_SOURCES"]], gan.get("BUNDLED_FRAGMENT_SHARDS")


def _do(base, tf, tl_module):
    """Trả 17 hàm đo theo thứ tự V1–V17; hàm nào văng thì khoá ấy False, các khoá khác vẫn được tính."""
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
        if stray.exists():
            stray.unlink()
        han(lambda: tf.write_bundled_modules(fr, r2))
        return han(lambda: tf.generate_bundled_modules(fr))

    def dung_r3(khai=(_M2, _M3)):
        r3.mkdir(parents=True, exist_ok=True)
        _manh(r3 / _M1, names[:2], khai)
        _manh(r3 / _M2, names[2:4])
        _manh(r3 / _M3, names[4:])
        if (r3 / _M9).exists():
            (r3 / _M9).unlink()

    def loi_r3():
        return _nap(tf, r3)[1]

    def v1():
        root = base / "r1" / "test_fragments"
        root.mkdir(parents=True)
        _frag(root, "wp9001_a.py")
        mods = tf.generate_bundled_modules(root)
        cu = tf.generate_bundled_module_bytes(root)
        return (len(mods) == 1 and _gan(mods[0][1])[1] is None
                and hashlib.sha256(mods[0][1]).hexdigest() == _MOT_MANH_SHA256
                and hashlib.sha256(cu).hexdigest() == _MOT_MANH_SHA256)

    def v2():
        mods = dung_r2()
        return ([n for n, _ in mods] == [_M1, _M2, _M3]
                and [_gan(d)[0] for _, d in mods] == [names[:2], names[2:4], names[4:]])

    def v3():
        return _gan(dung_r2()[0][1])[1] == (_M2, _M3)

    def v4():
        root = base / "r4" / "test_fragments"
        root.mkdir(parents=True)
        lon = ["wp9001_g0.py", "wp9001_g1.py", "wp9001_g2.py"]
        _frag(root, lon[0], pad=150 * 1024)   # một fragment đơn vượt hạn 100 KiB, đứng ĐẦU
        _frag(root, lon[1])
        _frag(root, lon[2])
        mods = han(lambda: tf.generate_bundled_modules(root))
        return [sorted(_gan(d)[0]) for _, d in mods] == [lon[:1], lon[1:]]   # V4 đo RANH mảnh; thứ tự trong mảnh là V2

    def v5():
        mods = dung_r2()
        return len(mods) > 1 and han(lambda: tf.generate_bundled_module_bytes(fr)) == mods[0][1]

    def v6():
        mods = dung_r2()
        stray.write_bytes(b"BUNDLED_FRAGMENT_SOURCES = ()\n")
        han(lambda: tf.write_bundled_modules(fr, r2))
        return not stray.exists() and all((r2 / n).read_bytes() == d for n, d in mods)

    def v7():
        dung_r3()
        truoc = _nap(tf, r3)
        _manh(r3 / _M9, ["wp9001_f6.py"])
        sau = _nap(tf, r3)
        return truoc[:2] == (ids, None) and sau[:2] == (ids, None)

    def v8():
        dung_r3()
        (r3 / _M2).unlink()
        _, err, msg = _nap(tf, r3)
        return err == _MISSING and f"scripts/{_M2}" in msg

    def v9():
        dung_r3()
        _manh(r3 / _M2, names[4:])
        _manh(r3 / _M3, names[2:4])
        return loi_r3() == _CONTRACT

    def v10():
        dung_r3()
        _manh(r3 / _M3, names[3:])         # f3 là cuối mảnh 2 VÀ đầu mảnh 3; thứ tự toàn chuỗi không giảm
        return loi_r3() == _CONTRACT

    def v11():
        dung_r3()
        _manh(r3 / _M3, names[4:], (_M2,))
        return loi_r3() == _CONTRACT

    def v12():
        dung_r3(khai=())
        return loi_r3() == _CONTRACT

    def v13():
        dung_r3(khai=(_M3,))               # khai không liên tục: bỏ qua _2
        return loi_r3() == _CONTRACT

    def v14():
        mods = dung_r2()
        stray.write_bytes(mods[0][1])
        rc, j = han(lambda: _check(tl_module, r2.parent))
        return rc != 0 and j.get("error") == _STALE and j.get("extra_shards") == [_M9]

    def v15():
        mods = dung_r2()
        (r2 / _M2).write_bytes(mods[1][1] + b"# sua\n")
        rc, j = han(lambda: _check(tl_module, r2.parent))
        return len(mods) == 3 and rc != 0 and j.get("error") == _STALE and j.get("extra_shards") == []

    def v16():
        mods = dung_r2()
        rc, j = han(lambda: _check(tl_module, r2.parent))
        bam = hashlib.sha256(b"".join(n.encode() + b"\0" + d for n, d in mods)).hexdigest()
        (r2 / _M1).unlink()
        rc2, j2 = han(lambda: _check(tl_module, r2.parent))
        return (len(mods) == 3 and rc == 0 and j.get("ok") is True
                and [s.get("name") for s in j.get("shards") or []] == [_M1, _M2, _M3]
                and j.get("expected_sha256") == bam == j.get("actual_sha256")
                and rc2 != 0 and j2.get("error") == _MISSING)

    def v17():
        repo = Path(tf.__file__).resolve().parent.parent / "test_fragments"
        real = tf.generate_bundled_modules(repo) if repo.is_dir() else ()
        return tf._BUNDLED_SHARD_LIMIT == 196608 and all(len(d) <= 0.7 * _WARN for _, d in real)

    return (v1, v2, v3, v4, v5, v6, v7, v8, v9, v10, v11, v12, v13, v14, v15, v16, v17)


def run(tl_module):
    tf = importlib.import_module("tl_core.test_fragments")
    _KQ.clear()
    with tempfile.TemporaryDirectory(prefix="wp433_bt_") as tmp:
        for khoa, fn in zip(_KHOA, _do(Path(tmp), tf, tl_module)):
            try:
                _KQ[khoa] = fn() is True
            except Exception:  # noqa: BLE001 — văng ⇒ khoá False, không bỏ dở các khoá sau
                _KQ[khoa] = False
    return len(_KQ) == 17 and all(value is True for value in _KQ.values())
