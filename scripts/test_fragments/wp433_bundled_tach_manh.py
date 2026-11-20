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

_TRAN = 0.7 * 280 * 1024   # 0,7·WARN của `_py_size_findings` = 200.704 B
# sha256 của `generate_bundled_module_bytes` trên base 0f9aa2a cho fixture `wp9001_a.py` (216 B); KHÔNG tính lại từ mã sau sửa.
_MOT_MANH_SHA256 = "73ad44659b63aea9b2f66fb1104c4c82deaa1ad1218e94adb80dcf38384441d7"
_KQ = {}   # V1–V31 của đặc tả §4, mỗi vế một khoá
_SRC, _SHA = "BUNDLED_FRAGMENT_SOURCES", "BUNDLED_FRAGMENT_SHARDS"
_M1 = "tl_test_fragments_bundled.py"
_M2, _M3, _M9 = (f"tl_test_fragments_bundled_{k}.py" for k in (2, 3, 9))
_CONTRACT, _MISSING, _STALE = "BUNDLED_MODULE_CONTRACT", "BUNDLED_MODULE_MISSING", "GENERATED_BUNDLE_STALE"
_HAN = 100 * 1024


def _nguon(name, pad=0):
    return f'TEST_ID = "{name[:-3]}"\n_PAD = "{"x" * pad}"\n\n\ndef run(tl_module):\n    return True\n'


def _co_dong(name, pad=0):
    """Số byte generator PHẢI tính cho một fragment (tính tay): dòng tuple đã render + 1 byte LF."""
    return len(f"    ({json.dumps(name)}, {json.dumps(_nguon(name, pad))}),".encode("utf-8")) + 1


def _manh(path, names, khai=None, thua=""):
    """Viết TAY một mảnh data-only (không qua generator) cho các vế loader."""
    text = f"{_SRC} = (\n" + "".join(f"    ({json.dumps(n)}, {json.dumps(_nguon(n))}),\n" for n in names) + ")\n"
    if khai is not None:
        text += f"{_SHA} = {khai!r}\n"
    path.write_text(text + thua, encoding="utf-8", newline="\n")


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
    """Đọc ĐỘC LẬP (AST) một mảnh sinh ra: (tên các phép gán theo thứ tự, tên fragment, giá trị SHARDS hoặc None)."""
    body = [n for n in ast.parse(data.decode("utf-8")).body if not isinstance(n, ast.Expr)]
    gan = {n.targets[0].id: ast.literal_eval(n.value) for n in body}
    return [n.targets[0].id for n in body], [n for n, _ in gan[_SRC]], gan.get(_SHA)


def _bam(data):
    return hashlib.sha256(data).hexdigest()


def _do(base, tf, tl_module):
    """Trả 31 hàm đo theo thứ tự V1–V31; hàm nào văng thì khoá ấy False, các khoá khác vẫn được tính."""
    names = [f"wp9001_f{i}.py" for i in range(6)]
    ids = [n[:-3] for n in names]
    deu = ("deu", [(n, 40 * 1024) for n in names])       # 6 × 40 KiB, hạn 100 KiB ⇒ 2+2+2
    mot = ("mot", [("wp9001_a.py", 0)])
    r3 = base / "r3" / "scripts"                          # mảnh viết tay, topology bundle (không có test_fragments/)

    def han(fn, limit=_HAN):
        old = tf._BUNDLED_SHARD_LIMIT
        tf._BUNDLED_SHARD_LIMIT = limit
        try:
            return fn()
        finally:
            tf._BUNDLED_SHARD_LIMIT = old

    def sinh(fixture, limit=_HAN):
        """Dựng thư mục fragment của fixture (một lần) rồi trả (thư mục, đầu ra generator)."""
        root = base / fixture[0] / "scripts" / "test_fragments"
        if not root.is_dir():
            root.mkdir(parents=True)
            for name, pad in fixture[1]:
                (root / name).write_text(_nguon(name, pad), encoding="utf-8", newline="\n")
        return root, han(lambda: tf.generate_bundled_modules(root), limit)

    def nhom(fixture, limit=_HAN):
        return [sorted(_gan(d)[1]) for _, d in sinh(fixture, limit)[1]]   # RANH mảnh; thứ tự trong mảnh là V4

    def ghi(ten, truoc=()):
        root, mods = sinh(deu)
        dest = base / ten
        dest.mkdir()
        for name in truoc:
            (dest / name).write_bytes(b"x = 0\n")
        han(lambda: tf.write_bundled_modules(root, dest))
        return mods, dest

    def loi(khai=(_M2, _M3), sua=None):
        """Dựng TAY ba mảnh hợp lệ trong r3, áp `sua`, trả (ids, mã lỗi, thông báo) của loader."""
        r3.mkdir(parents=True, exist_ok=True)
        for p in r3.iterdir():
            p.unlink()
        _manh(r3 / _M1, names[:2], khai)
        _manh(r3 / _M2, names[2:4])
        _manh(r3 / _M3, names[4:])
        if sua:
            sua()
        return _nap(tf, r3)

    def cong(fixture, sua=None):
        """Cây cổng dựng TAY: tệp mảnh = bytes generator ghi thẳng (không qua writer); `sua(scripts, mods)` làm hỏng."""
        root, mods = sinh(fixture)
        scripts = root.parent
        for p in scripts.glob("tl_test_fragments_bundled*.py"):
            p.unlink()
        for name, data in mods:
            (scripts / name).write_bytes(data)
        if sua:
            sua(scripts, mods)
        rc, j = han(lambda: _check(tl_module, scripts.parent))
        return mods, rc, j

    def v5():
        s = _co_dong("wp9001_x0.py", 100)                 # x0, x1, x2 cùng cỡ s; x3 lớn hơn đúng 1 B; hạn = 2s
        fx = ("lech", [(f"wp9001_x{i}.py", 100 + (i == 3)) for i in range(4)])
        x = [n for n, _ in fx[1]]
        return _co_dong(x[3], 101) == s + 1 and nhom(fx, 2 * s) == [x[:2], x[2:3], x[3:]]

    def v6():
        g = ["wp9001_g0.py", "wp9001_g1.py", "wp9001_g2.py"]
        return nhom(("lon", [(g[0], 0), (g[1], 150 * 1024), (g[2], 0)])) == [g[:1], g[1:2], g[2:]]

    def v10():
        root, mods = sinh(deu)
        return len(mods) > 1 and han(lambda: tf.generate_bundled_module_bytes(root)) == mods[0][1]

    def v11():
        mods, dest = ghi("w11")
        return (len(mods) == 3 and sorted(p.name for p in dest.iterdir()) == sorted(n for n, _ in mods)
                and all((dest / n).read_bytes() == d for n, d in mods))

    def v13():
        truoc = loi()
        sau = loi(sua=lambda: _manh(r3 / _M9, ["wp9001_f6.py"]))
        return truoc[:2] == (ids, None) and sau[:2] == (ids, None)

    def v16():
        def doi():
            _manh(r3 / _M2, names[4:])
            _manh(r3 / _M3, names[2:4])
        return loi(sua=doi)[1] == _CONTRACT

    def v23():
        _, rc, j = cong(deu, lambda s, m: (s / _M9).write_bytes(m[0][1]))
        return rc != 0 and j.get("error") == _STALE and j.get("extra_shards") == [_M9]

    def v24():
        _, rc, j = cong(deu, lambda s, m: (s / m[1][0]).write_bytes(m[1][1] + b"# sua\n"))
        return rc != 0 and j.get("error") == _STALE

    def v25():
        _, rc, j = cong(deu, lambda s, m: (s / m[1][0]).unlink())
        return rc != 0 and j.get("error") == _STALE and j["shards"][1]["actual_bytes"] is None

    def v27():
        mods, rc, j = cong(mot)
        d = mods[0][1]
        return (len(mods) == 1 and rc == 0 and [j.get(k) for k in ("expected_sha256", "actual_sha256", "expected_bytes",
                                                                  "actual_bytes")] == [_bam(d), _bam(d), len(d), len(d)])

    def v28():
        mods, rc, j = cong(deu)
        chuoi = b"".join(n.encode("utf-8") + b"\0" + d for n, d in mods)   # băm VÀ độ dài đều của chính chuỗi này
        bam, tong = _bam(chuoi), len(chuoi)
        return (len(mods) > 1 and rc == 0 and [j.get(k) for k in ("expected_sha256", "actual_sha256", "expected_bytes",
                                                                 "actual_bytes")] == [bam, bam, tong, tong])

    def v29():
        mods, rc, j = cong(deu)
        return len(mods) > 1 and j.get("shards") == [
            {"name": n, "expected_bytes": len(d), "actual_bytes": len(d)} for n, d in mods]

    def v31():
        scripts = Path(tf.__file__).resolve().parent.parent
        repo = scripts / "test_fragments"
        if repo.is_dir():                                  # cây dev: đo CẢ đầu ra generator LẪN tệp trên đĩa
            real = tf.generate_bundled_modules(repo)
            sizes = [len(d) for _, d in real] + [len((scripts / n).read_bytes()) for n, _ in real]
        else:                                              # gói phát hành: đo mảnh 1 và mọi mảnh nó KHAI; thiếu ⇒ văng ⇒ False
            khai = _gan((scripts / _M1).read_bytes())[2] or ()
            sizes = [len((scripts / n).read_bytes()) for n in (_M1, *khai)]
        return bool(sizes) and all(size <= _TRAN for size in sizes)

    return (
        lambda: [_bam(d) for _, d in sinh(mot)[1]] == [_MOT_MANH_SHA256],                                  # V1
        lambda: _bam(tf.generate_bundled_module_bytes(sinh(mot)[0])) == _MOT_MANH_SHA256,                  # V2
        lambda: [_gan(d)[0] for _, d in sinh(("hai", [("wp9001_a.py", 0), ("wp9001_b.py", 0)]))[1]] == [[_SRC]],  # V3
        lambda: [_gan(d)[1] for _, d in sinh(deu)[1]] == [names[:2], names[2:4], names[4:]],               # V4
        v5, v6,
        lambda: [n for n, _ in sinh(deu)[1]] == [_M1, _M2, _M3],                                           # V7
        lambda: _gan(sinh(deu)[1][0][1])[0] == [_SRC, _SHA],                                               # V8
        lambda: _gan(sinh(deu)[1][0][1])[2] == (_M2, _M3),                                                 # V9
        v10, v11,
        lambda: not (ghi("w12", truoc=(_M9,))[1] / _M9).exists(),                                          # V12
        v13,
        lambda: loi(sua=lambda: (r3 / _M2).unlink())[1] == _MISSING,                                       # V14
        lambda: f"scripts/{_M2}" in loi(sua=lambda: (r3 / _M2).unlink())[2],                               # V15
        v16,
        lambda: loi(sua=lambda: _manh(r3 / _M3, names[3:]))[1] == _CONTRACT,       # V17: f3 cuối mảnh 2 VÀ đầu mảnh 3
        lambda: loi(sua=lambda: _manh(r3 / _M3, names[4:], (_M2,)))[1] == _CONTRACT,                       # V18
        lambda: loi(khai=())[1] == _CONTRACT,                                                              # V19
        lambda: loi(khai=(_M3,))[1] == _CONTRACT,                                                          # V20
        lambda: loi(sua=lambda: _manh(r3 / _M1, names[:2], (_M2, _M3), thua="0\n"))[1] == _CONTRACT,       # V21
        lambda: loi(sua=lambda: _manh(r3 / _M3, names[4:], thua="0\n"))[1] == _CONTRACT,                   # V22
        v23, v24, v25,
        lambda: cong(mot, lambda s, m: (s / _M1).unlink())[2].get("error") == _MISSING,                    # V26
        v27, v28, v29,
        lambda: tf._BUNDLED_SHARD_LIMIT == 196608,                                                         # V30
        v31,
    )


def run(tl_module):
    tf = importlib.import_module("tl_core.test_fragments")
    _KQ.clear()
    with tempfile.TemporaryDirectory(prefix="wp433_bt_") as tmp:
        for so, fn in enumerate(_do(Path(tmp), tf, tl_module), start=1):
            try:
                _KQ[f"V{so}"] = fn() is True
            except Exception:  # noqa: BLE001 — văng ⇒ khoá False, không bỏ dở các khoá sau
                _KQ[f"V{so}"] = False
    return len(_KQ) == 31 and all(value is True for value in _KQ.values())
