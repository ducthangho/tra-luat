# -*- coding: utf-8 -*-
"""wp1121 — `doc-claims-check`: trích dẫn tới tệp ĐÃ XOÁ (đã commit) trong tài liệu SỐNG là cờ.

Dựng một kho git THẬT trong thư mục tạm: `ops/x.md` được commit rồi `git rm` + commit, một tệp giữ `ops/giu.md` để
gốc `ops` còn trong `toplevel`. Năm tài liệu cùng trích `ops/x.md`, mỗi tài liệu một ca:
  (a) `CONTEXT.md` sống ⇒ cờ `PATH_DELETED`;
  (b) `CHANGELOG.md` lịch sử ⇒ advisory `PATH_DELETED_IN_HISTORICAL_DOC`;
  (c) `docs/adr/0001-t.md` — ADR là tài liệu sống ⇒ cờ `PATH_DELETED`;
  (d) `CONTEXT.md` trích thêm `ops/chua-tung-co.md` (chưa từng tồn tại) ⇒ vẫn `PATH_MISSING`;
  (e) `references/DOCTRINE_APPENDIX.md.live.md` — khớp TIỀN TỐ của mục lịch sử `references/DOCTRINE_APPENDIX.md`
      nhưng không phải tệp ấy ⇒ tài liệu sống ⇒ cờ `PATH_DELETED`;
  (f) `references/changelog_archive/c.md` — con của thư mục lịch sử ⇒ advisory `PATH_DELETED_IN_HISTORICAL_DOC`.
Hai ca L9 cho call site phân loại nguồn trỏ:
  (g) `references/keep.md` chỉ được (e) trỏ tới ⇒ nguồn sống ⇒ KHÔNG phát hiện L9 nào;
  (h) `references/keep2.md` chỉ được `CHANGELOG.md` trỏ tới ⇒ đúng một advisory `DOC_POINTED_ONLY_BY_HISTORICAL`.

Phạm vi so: mọi phát hiện L1, cộng phát hiện L9 có `claim` là hai tệp keep — so theo TẬP. KHÔNG dùng `ok`/rc: kho tạm
không có chỉ mục test-ID (L12) và `parser_surface.json` (L8), nên kết luận chung của lệnh không nói gì về L1/L9.

Tiền điều kiện (sai ⇒ FAIL có tên): `ops/x.md` thuộc tập đã xoá; `ops` thuộc `toplevel`; mọi tài liệu (a)–(f) thuộc
targets mặc định; L9 không nằm trong `layers_skipped`. Không dựng được fixture (git thiếu, lệnh git rc≠0) ⇒ FAIL,
không bao giờ trả True — fragment này KHÔNG có nhánh bỏ qua.
"""

import os
from pathlib import Path
import subprocess
import sys
import tempfile


TEST_ID = "wp1121_doc_claims_xoa"

_X = "ops/x.md"
_CHUA_TUNG_CO = "ops/chua-tung-co.md"
_KEEP = "references/keep.md"
_KEEP2 = "references/keep2.md"
_TAI_LIEU = {
    "a": "CONTEXT.md",
    "b": "CHANGELOG.md",
    "c": "docs/adr/0001-t.md",
    "e": "references/DOCTRINE_APPENDIX.md.live.md",
    "f": "references/changelog_archive/c.md",
}
# (lớp, tài liệu, claim, mã lý do, là advisory) -> ca
_MONG = {
    ("L1", "CONTEXT.md", _X, "PATH_DELETED", False): "a",
    ("L1", "CHANGELOG.md", _X, "PATH_DELETED_IN_HISTORICAL_DOC", True): "b",
    ("L1", "docs/adr/0001-t.md", _X, "PATH_DELETED", False): "c",
    ("L1", "CONTEXT.md", _CHUA_TUNG_CO, "PATH_MISSING", False): "d",
    ("L1", "references/DOCTRINE_APPENDIX.md.live.md", _X, "PATH_DELETED", False): "e",
    ("L1", "references/changelog_archive/c.md", _X, "PATH_DELETED_IN_HISTORICAL_DOC", True): "f",
    ("L9", _KEEP2, _KEEP2, "DOC_POINTED_ONLY_BY_HISTORICAL", True): "h",
}


def _bao(msg):
    print("[%s] FAIL %s" % (TEST_ID, msg), file=sys.stderr)


def _git(kho, *args):
    env = dict(os.environ)
    env.update(GIT_CONFIG_NOSYSTEM="1", GIT_CONFIG_GLOBAL=os.devnull, GIT_TERMINAL_PROMPT="0")
    r = subprocess.run(["git", "-c", "user.email=t@t", "-c", "user.name=t", "-c", "commit.gpgsign=false",
                        "-c", "core.autocrlf=false", *args],
                       cwd=str(kho), env=env, capture_output=True, text=True, timeout=120)
    if r.returncode != 0:
        raise RuntimeError("git %s rc=%d: %s" % (" ".join(args), r.returncode, r.stderr.strip()[:200]))
    return r.stdout


def _ghi(kho, rel, noi_dung):
    p = kho / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(noi_dung, encoding="utf-8", newline="\n")


def _dung_kho(kho):
    _git(kho, "init", "-q")
    for rel, nd in (("ops/giu.md", "giu\n"), (_X, "x\n"), ("SKILL.md", "# S\n"),
                    (_KEEP, "k\n"), (_KEEP2, "k2\n")):
        _ghi(kho, rel, nd)
    _git(kho, "add", "-A")
    _git(kho, "commit", "-q", "-m", "c1")
    _git(kho, "rm", "-q", _X)
    _git(kho, "commit", "-q", "-m", "c2 xoa")
    _ghi(kho, "CONTEXT.md", "# C\n\nxem `%s` và `%s`.\n" % (_X, _CHUA_TUNG_CO))
    _ghi(kho, "CHANGELOG.md", "# L\n\nxem `%s`; xem `%s`.\n" % (_X, _KEEP2))
    _ghi(kho, "docs/adr/0001-t.md", "# A\n\nxem `%s`.\n" % _X)
    _ghi(kho, "references/DOCTRINE_APPENDIX.md.live.md", "# D\n\nxem `%s`; xem `%s`.\n" % (_X, _KEEP))
    _ghi(kho, "references/changelog_archive/c.md", "# H\n\nxem `%s`.\n" % _X)
    _git(kho, "add", "-A")
    _git(kho, "commit", "-q", "-m", "c3 tai lieu")


def _tien_dieu_kien(wf, kho, j):
    ctx = wf._doc_claims_context(kho)
    if _X not in wf._doc_claims_deleted_set(ctx):
        return "tiền điều kiện: %s không thuộc tập đã xoá" % _X
    if "ops" not in ctx.get("toplevel", ()):
        return "tiền điều kiện: gốc `ops` không thuộc toplevel"
    files, _, _ = wf._doc_claims_targets(None, kho)
    rels = {Path(p).resolve().relative_to(kho.resolve()).as_posix() for p in files}
    ngoai = sorted("(%s) %s" % (ca, rel) for ca, rel in _TAI_LIEU.items() if rel not in rels)
    if ngoai:
        return "tiền điều kiện targets: tài liệu không được quét: %s" % ", ".join(ngoai)
    if "L9" in (j.get("layers_skipped") or {}):
        return "tiền điều kiện: L9 bị bỏ qua (%s)" % j["layers_skipped"]["L9"]
    return None


def _thuc(j):
    adv_ids = {id(x) for x in (j.get("advisories") or [])}
    out = set()
    for x in list(j.get("flags") or []) + list(j.get("advisories") or []):
        lop = x.get("layer")
        if lop == "L1" or (lop == "L9" and x.get("claim") in (_KEEP, _KEEP2)):
            out.add((lop, x.get("file"), x.get("claim"), x.get("reason"), id(x) in adv_ids))
    return out


def _ca(tl_module):
    with tempfile.TemporaryDirectory() as td:
        kho = Path(td) / "kho"
        kho.mkdir()
        _dung_kho(kho)
        j = tl_module._doc_claims_check(root=kho)              # đường sản xuất (stub tl → tl_core.workflow)
        # `tl` chỉ phơi stub của các hàm trong `_STUB_MAP`; helper như `_doc_claims_deleted_set` nằm ở module thật.
        loi = _tien_dieu_kien(tl_module._tl_workflow, kho, j)
        if loi:
            _bao(loi)
            return False
        thuc = _thuc(j)
    mong = set(_MONG)
    if thuc == mong:
        return True
    thieu = sorted(mong - thuc)
    thua = sorted(thuc - mong)
    # Ca được xác định bởi (lớp, tài liệu, claim); `CONTEXT.md` mang hai ca (a) và (d) nên không gán theo tài liệu.
    ca_theo_khoa = {k[:3]: ca for k, ca in _MONG.items()}
    ca_theo_khoa[("L9", _KEEP, _KEEP)] = "g"
    ca_lech = sorted({_MONG[t] for t in thieu} | {ca_theo_khoa.get(t[:3], "?%s" % (t[:3],)) for t in thua})
    _bao("ca lệch %s; thiếu %s; thừa %s" % (ca_lech, thieu, thua))
    return False


def run(tl_module):
    try:
        return _ca(tl_module)
    except Exception as exc:                            # fixture/git hỏng ⇒ ĐỎ có chẩn đoán, không bao giờ True
        _bao("không dựng/đo được fixture: %s: %s" % (type(exc).__name__, exc))
        return False
