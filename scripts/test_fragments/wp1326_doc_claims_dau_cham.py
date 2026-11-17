# -*- coding: utf-8 -*-
"""wp1326 — `doc-claims-check` L1: đường dẫn bắt đầu bằng dấu chấm được kiểm ĐÚNG TÊN (#1326).

Dựng một kho git THẬT trong thư mục tạm rồi gọi đường sản xuất `_doc_claims_check(root=kho)`. Tệp giữ:
`.claude/giu.md`, `.agents/skills/x/SKILL.md`, `agents/giu.md`, `.github/giu.md`, `du-lieu/giu.md`, `SKILL.md`;
`.gitignore` có hai dòng `.claude/.state/` và `du-lieu/sinh/` (hai thư mục ấy KHÔNG có trên đĩa); `.claude/da-xoa.py`
được commit rồi `git rm` + commit. Các ca (tài liệu · token ⇒ mong đợi):
  (a)  `CONTEXT.md` · `.agents/skills/x/SKILL.md` có thật ⇒ không phát hiện (L1 cũ kiểm nhầm tên `agents/…`);
  (b)  `CONTEXT.md` · `.claude/khong-co.py` ⇒ cờ `PATH_MISSING`, claim giữ dấu chấm đầu;
  (c)  `CHANGELOG.md` lịch sử · `.claude/khong-co.py` ⇒ advisory `PATH_MISSING_IN_HISTORICAL_DOC`;
  (d)  `docs/adr/0001-t.md` · `.claude/da-xoa.py` ⇒ cờ `PATH_DELETED`;
  (e)  `CONTEXT.md` · `.claude/.state/x.json` (tệp trong thư mục bị ignore) ⇒ không phát hiện;
  (e2) `CONTEXT.md` · `.claude/.state/` (chính thư mục bị ignore, có `/` cuối) ⇒ không phát hiện;
  (e3) `references/a.md` có `.claude/.state` TRƯỚC `.claude/.state/`, `references/b.md` có hai token ấy theo thứ tự
       ngược lại ⇒ mỗi tài liệu đúng một cờ `PATH_MISSING` claim `.claude/.state`, không gì cho `.claude/.state/`
       (chuỗi hỏi `git check-ignore` và khoá cache đều giữ `/` cuối);
  (e4) `docs/adr/0002-u.md` (tài liệu trong thư mục con) · `.claude/khong-co-2.py` ⇒ cờ `PATH_MISSING`;
  (e5) `CONTEXT.md` · `du-lieu/sinh/` (đường thường, thư mục bị ignore) ⇒ không phát hiện;
  (f)  `CONTEXT.md` · `.docx/.pdf` ⇒ không phát hiện (đoạn đầu không phải mục gốc);
  (g)  `CONTEXT.md` · `./khong-co.md` và `../khong-co.md` ⇒ không phát hiện (`./`, `../` không kiểm);
  (h1) `docs/PROTOCOL_DA_PHIEN.md` · `.github/coordination/change-impact.v1.json` ⇒ advisory `PATH_MISSING_MIEN_TRU`;
  (h2) `CONTEXT.md` · cùng đường dẫn ⇒ cờ `PATH_MISSING` (miễn trừ gắn với TÀI LIỆU, không với đường dẫn).

Phạm vi so: TẬP mọi phát hiện L1 `(lớp, tài liệu, claim, mã lý do, là advisory)`. KHÔNG dùng `ok`/rc: kho tạm không có
chỉ mục test-ID (L12) và `parser_surface.json` (L8). Thông báo FAIL nêu TÊN ca lệch, tra theo (tài liệu, claim).

Tiền điều kiện (sai ⇒ FAIL có tên): `.claude`, `.agents`, `agents`, `.github`, `du-lieu` thuộc `toplevel`;
`.claude/da-xoa.py` thuộc tập đã xoá; mọi tài liệu của bảng thuộc targets mặc định; `references/a.md` được quét trước
`references/b.md`; hai thư mục bị ignore không có trên đĩa. Không dựng được fixture (git thiếu, lệnh git rc≠0) ⇒ FAIL,
không bao giờ trả True — fragment này KHÔNG có nhánh bỏ qua.
"""

import os
from pathlib import Path
import subprocess
import sys
import tempfile


TEST_ID = "wp1326_doc_claims_dau_cham"

_CO_THAT = ".agents/skills/x/SKILL.md"
_KHONG_CO = ".claude/khong-co.py"
_KHONG_CO_2 = ".claude/khong-co-2.py"
_DA_XOA = ".claude/da-xoa.py"
_TRONG_IGNORE = ".claude/.state/x.json"
_TM_TEP = ".claude/.state"
_TM = ".claude/.state/"
_TM_THUONG = "du-lieu/sinh/"
_KHONG_GOC = ".docx/.pdf"
_TUONG_DOI = ("./khong-co.md", "../khong-co.md")
_MIEN_TRU = ".github/coordination/change-impact.v1.json"
_A, _B = "references/a.md", "references/b.md"
_PROTOCOL = "docs/PROTOCOL_DA_PHIEN.md"
_GOC = (".claude", ".agents", "agents", ".github", "du-lieu")
_TAI_LIEU = ("CONTEXT.md", "CHANGELOG.md", "docs/adr/0001-t.md", "docs/adr/0002-u.md", _A, _B, _PROTOCOL)
# (lớp, tài liệu, claim, mã lý do, là advisory) -> ca
_MONG = {
    ("L1", "CONTEXT.md", _KHONG_CO, "PATH_MISSING", False): "b",
    ("L1", "CHANGELOG.md", _KHONG_CO, "PATH_MISSING_IN_HISTORICAL_DOC", True): "c",
    ("L1", "docs/adr/0001-t.md", _DA_XOA, "PATH_DELETED", False): "d",
    ("L1", _A, _TM_TEP, "PATH_MISSING", False): "e3",
    ("L1", _B, _TM_TEP, "PATH_MISSING", False): "e3",
    ("L1", "docs/adr/0002-u.md", _KHONG_CO_2, "PATH_MISSING", False): "e4",
    ("L1", _PROTOCOL, _MIEN_TRU, "PATH_MISSING_MIEN_TRU", True): "h1",
    ("L1", "CONTEXT.md", _MIEN_TRU, "PATH_MISSING", False): "h2",
}
# (tài liệu, claim) -> ca, cho phát hiện THỪA: gồm các ca mong đợi "không phát hiện" và claim mất dấu chấm của L1 cũ.
_CA_THEO_KHOA = {k[1:3]: ca for k, ca in _MONG.items()}
_CA_THEO_KHOA.update({
    ("CONTEXT.md", _CO_THAT): "a", ("CONTEXT.md", _CO_THAT[1:]): "a",
    ("CONTEXT.md", _TRONG_IGNORE): "e", ("CONTEXT.md", _TM): "e2",
    (_A, _TM): "e3", (_B, _TM): "e3",
    ("CONTEXT.md", _TM_THUONG): "e5", ("CONTEXT.md", _KHONG_GOC): "f",
    ("CONTEXT.md", _TUONG_DOI[0]): "g", ("CONTEXT.md", _TUONG_DOI[1]): "g",
})


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


def _doan(*tokens):
    return "# T\n\n" + "".join("xem `%s` nhé\n" % t for t in tokens)


def _dung_kho(kho):
    _git(kho, "init", "-q")
    for rel, nd in ((".claude/giu.md", "g\n"), (_CO_THAT, "# X\n"), ("agents/giu.md", "g\n"),
                    (".github/giu.md", "g\n"), ("du-lieu/giu.md", "g\n"), ("SKILL.md", "# S\n"),
                    (".gitignore", "%s\n%s\n" % (_TM, _TM_THUONG)), (_DA_XOA, "x = 1\n")):
        _ghi(kho, rel, nd)
    _git(kho, "add", "-A")
    _git(kho, "commit", "-q", "-m", "c1")
    _git(kho, "rm", "-q", _DA_XOA)
    _git(kho, "commit", "-q", "-m", "c2 xoa")
    _ghi(kho, "CONTEXT.md", _doan(_CO_THAT, _KHONG_CO, _TRONG_IGNORE, _TM, _TM_THUONG, _KHONG_GOC,
                                  _TUONG_DOI[0], _TUONG_DOI[1], _MIEN_TRU))
    _ghi(kho, "CHANGELOG.md", _doan(_KHONG_CO))
    _ghi(kho, "docs/adr/0001-t.md", _doan(_DA_XOA))
    _ghi(kho, "docs/adr/0002-u.md", _doan(_KHONG_CO_2))
    _ghi(kho, _A, _doan(_TM_TEP, _TM))
    _ghi(kho, _B, _doan(_TM, _TM_TEP))
    _ghi(kho, _PROTOCOL, _doan(_MIEN_TRU))
    _git(kho, "add", "-A")
    _git(kho, "commit", "-q", "-m", "c3 tai lieu")


def _tien_dieu_kien(wf, kho):
    ctx = wf._doc_claims_context(kho)
    thieu = sorted(g for g in _GOC if g not in ctx.get("toplevel", ()))
    if thieu:
        return "tiền điều kiện: mục gốc không thuộc toplevel: %s" % ", ".join(thieu)
    if _DA_XOA not in wf._doc_claims_deleted_set(ctx):
        return "tiền điều kiện: %s không thuộc tập đã xoá" % _DA_XOA
    files, _, _ = wf._doc_claims_targets(None, kho)
    rels = [Path(p).resolve().relative_to(kho.resolve()).as_posix() for p in files]
    ngoai = sorted(rel for rel in _TAI_LIEU if rel not in rels)
    if ngoai:
        return "tiền điều kiện targets: tài liệu không được quét: %s" % ", ".join(ngoai)
    if rels.index(_A) > rels.index(_B):
        return "tiền điều kiện: %s không được quét trước %s" % (_A, _B)
    co = sorted(d for d in (_TM, _TM_THUONG) if (kho / d).exists())
    if co:
        return "tiền điều kiện: thư mục bị ignore lại có trên đĩa: %s" % ", ".join(co)
    return None


def _thuc(j):
    adv_ids = {id(x) for x in (j.get("advisories") or [])}
    return {("L1", x.get("file"), x.get("claim"), x.get("reason"), id(x) in adv_ids)
            for x in list(j.get("flags") or []) + list(j.get("advisories") or []) if x.get("layer") == "L1"}


def _ca(tl_module):
    with tempfile.TemporaryDirectory() as td:
        kho = Path(td) / "kho"
        kho.mkdir()
        _dung_kho(kho)
        j = tl_module._doc_claims_check(root=kho)              # đường sản xuất (stub tl → tl_core.workflow)
        # `tl` chỉ phơi stub của các hàm trong `_STUB_MAP`; helper như `_doc_claims_deleted_set` nằm ở module thật.
        loi = _tien_dieu_kien(tl_module._tl_workflow, kho)
        if loi:
            _bao(loi)
            return False
        thuc = _thuc(j)
    mong = set(_MONG)
    if thuc == mong:
        return True
    thieu = sorted(mong - thuc)
    thua = sorted(thuc - mong)
    ca_lech = sorted({_CA_THEO_KHOA.get(t[1:3], "?%s" % (t[1:3],)) for t in thieu + thua})
    _bao("ca lệch %s; thiếu %s; thừa %s" % (ca_lech, thieu, thua))
    return False


def run(tl_module):
    try:
        return _ca(tl_module)
    except Exception as exc:                            # fixture/git hỏng ⇒ ĐỎ có chẩn đoán, không bao giờ True
        _bao("không dựng/đo được fixture: %s: %s" % (type(exc).__name__, exc))
        return False
