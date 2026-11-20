# -*- coding: utf-8 -*-
"""Bundle tách mảnh: mỗi mảnh dưới ngưỡng WARN, nạp đúng mảnh được KHAI, kiểm cổng phát hiện mảnh lạc."""

import contextlib
import importlib
import io
import json
from pathlib import Path
import tempfile

TEST_ID = "wp433_bundled_tach_manh"

_WARN = 280 * 1024
_KQ = {}


def _frag(root, name, pad=0):
    tid = name[:-3]
    body = f'TEST_ID = "{tid}"\n_PAD = "{"x" * pad}"\n\n\ndef run(tl_module):\n    return True\n'
    (root / name).write_text(body, encoding="utf-8", newline="\n")


def _nap(tf, scripts):
    try:
        return [c.test_id for c in tf.load_runtime_fragment_cases(scripts)], None
    except Exception as exc:  # noqa: BLE001
        return None, getattr(exc, "code", type(exc).__name__)


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


def run(tl_module):
    tf = importlib.import_module("tl_core.test_fragments")
    ok = True
    with tempfile.TemporaryDirectory(prefix="wp433_bt_") as tmp:
        base = Path(tmp)
        # (1) nhỏ ⇒ một mảnh, đúng dạng một tệp cũ (không có dòng BUNDLED_FRAGMENT_SHARDS)
        r1 = base / "r1" / "scripts"
        (r1 / "test_fragments").mkdir(parents=True)
        _frag(r1 / "test_fragments", "wp9001_a.py")
        mods1 = tf.generate_bundled_modules(r1 / "test_fragments")
        _KQ["mot_manh"] = (len(mods1) == 1 and b"BUNDLED_FRAGMENT_SHARDS" not in mods1[0][1]
                           and mods1[0][1] == tf.generate_bundled_module_bytes(r1 / "test_fragments"))
        # (2) vượt hạn ⇒ nhiều mảnh, mảnh 1 khai, nạp đủ theo thứ tự, mỗi mảnh <= hạn + một dòng
        r2 = base / "r2" / "scripts"
        fr = r2 / "test_fragments"
        fr.mkdir(parents=True)
        names = [f"wp9001_f{i}.py" for i in range(6)]
        for n in names:
            _frag(fr, n, pad=40 * 1024)
        old = tf._BUNDLED_SHARD_LIMIT
        tf._BUNDLED_SHARD_LIMIT = 100 * 1024
        try:
            written = tf.write_bundled_modules(fr, r2)
            mods2 = tf.generate_bundled_modules(fr)
        finally:
            tf._BUNDLED_SHARD_LIMIT = old
        if len(written) < 3 or len(mods2) < 3:   # chốt: không đủ mảnh thì đỏ, không văng IndexError
            _KQ["nhieu_manh"] = False
            return False
        fr_moved = r2.parent / "src"
        fr.rename(fr_moved)   # topology bundle: không còn test_fragments/
        ids, err = _nap(tf, r2)
        _KQ["nhieu_manh"] = (len(written) >= 3 and err is None
                             and ids == [n[:-3] for n in names]
                             and all(len(d) <= 100 * 1024 + 42 * 1024 for _, d in mods2)
                             and b"BUNDLED_FRAGMENT_SHARDS" in mods2[0][1])
        # (3) mảnh lạc không khai: loader bỏ qua, cổng báo stale + extra_shards
        stray = r2 / "tl_test_fragments_bundled_9.py"
        stray.write_bytes(mods2[1][1])
        ids3, err3 = _nap(tf, r2)
        fr_moved.rename(fr)
        tf._BUNDLED_SHARD_LIMIT = 100 * 1024
        try:
            rc3, j3 = _check(tl_module, r2.parent)
        finally:
            tf._BUNDLED_SHARD_LIMIT = old
        _KQ["manh_lac"] = (ids3 == ids and err3 is None and rc3 != 0
                           and j3.get("error") == "GENERATED_BUNDLE_STALE"
                           and j3.get("extra_shards") == ["tl_test_fragments_bundled_9.py"])
        # (4) ghi lại xoá mảnh lạc
        tf._BUNDLED_SHARD_LIMIT = 100 * 1024
        try:
            tf.write_bundled_modules(fr, r2)
            rc4, j4 = _check(tl_module, r2.parent)
        finally:
            tf._BUNDLED_SHARD_LIMIT = old
        _KQ["ghi_xoa_lac"] = (not stray.exists() and rc4 == 0 and j4.get("ok") is True)
        fr.rename(fr_moved)
        # (5) mảnh được khai bị thiếu ⇒ BUNDLED_MODULE_MISSING
        m2 = r2 / written[1]
        keep = m2.read_bytes()
        m2.unlink()
        _, err5 = _nap(tf, r2)
        m2.write_bytes(keep)
        # (6) thứ tự xuyên mảnh sai ⇒ hợp đồng; (7) mảnh k>=2 tự khai mảnh ⇒ hợp đồng
        m3 = r2 / written[2]
        keep3 = m3.read_bytes()
        m2.write_bytes(keep3)
        m3.write_bytes(keep)
        _, err6 = _nap(tf, r2)
        m2.write_bytes(keep)
        m3.write_bytes(keep3 + b'BUNDLED_FRAGMENT_SHARDS = ("tl_test_fragments_bundled_2.py",)\n')
        _, err7 = _nap(tf, r2)
        m3.write_bytes(keep3)
        _KQ["thieu_manh"] = err5 == "BUNDLED_MODULE_MISSING"
        _KQ["thu_tu_xuyen_manh"] = err6 == "BUNDLED_MODULE_CONTRACT"
        _KQ["manh_tu_khai"] = err7 == "BUNDLED_MODULE_CONTRACT"
    # (8) kho thật: mọi mảnh dưới WARN, hạn mảnh <= 70% WARN
    repo = Path(tf.__file__).resolve().parent.parent / "test_fragments"
    if repo.is_dir():
        real = tf.generate_bundled_modules(repo)
        _KQ["kho_that"] = (tf._BUNDLED_SHARD_LIMIT <= 0.7 * _WARN
                           and all(len(d) <= _WARN for _, d in real))
    else:
        _KQ["kho_that"] = True
    for value in _KQ.values():
        ok = ok and value is True
    return ok
