#!/usr/bin/env python3
"""Bộ test tự đứng cho `ops/kiem_ho_so_land.py` (packet #752, đặc tả `ops/specs/no-p3-cong-cu-ho-so-r4.md`).

Dựng cây tạm, gọi CLI trong tiến trình con. In ĐÚNG MỘT dòng chỉ gồm `đạt/tổng` (đơn vị: ca test) — mẫu
`^(\\d+)/(\\d+)$` mà #763 đăng ký; ca đỏ in dòng `DO <ca>: …` (không có dạng ấy). Chạy: python -B ops/kiem_ho_so_land_test.py
Phủ nghiệm thu B1 · B1b · B1c · B2 · B2b · B3 (iii)/(iv) · B7.
"""
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

for _s in (sys.stdout, sys.stderr):
    if hasattr(_s, "reconfigure"):
        _s.reconfigure(encoding="utf-8", errors="backslashreplace")

TOOL = Path(__file__).resolve().parent / "kiem_ho_so_land.py"
GLOB = "ops/land/*-land-evidence.yaml"
SHA = "0123456789abcdef0123456789abcdef01234567"
URL = "https://github.com/ducthangho/tra-luat/pull/1"
PR672 = "ops/land/pr672-wp574-land-evidence.yaml"

# Gọi main() với danh sách miễn trừ tiêm `{}`; `chan_yaml` chặn import yaml TRƯỚC khi nạp công cụ.
_TIEM = (
    "import importlib.util, sys\n"
    "{chan}"
    "s = importlib.util.spec_from_file_location('kiem_ho_so_land', {tool!r})\n"
    "m = importlib.util.module_from_spec(s); s.loader.exec_module(m)\n"
    "sys.exit(m.main(sys.argv[1:], mien_tru={{}}))\n"
)


def _chay(root, *, tiem=False, chan_yaml=False, json_out=True, tool=TOOL):
    args = ["--root", str(root)] + (["--json"] if json_out else [])
    if tiem or chan_yaml:
        code = _TIEM.format(chan="sys.modules['yaml'] = None\n" if chan_yaml else "", tool=str(tool))
        cmd = [sys.executable, "-B", "-c", code, *args]
    else:
        cmd = [sys.executable, "-B", str(TOOL), *args]
    p = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", timeout=120)
    kq = None
    if json_out and p.returncode != 2:
        try:
            kq = json.loads(p.stdout)
        except ValueError:
            kq = None
    return p.returncode, kq, p.stdout, p.stderr


def _cay(tep):
    """Dựng cây tạm: {đường dẫn tương đối: nội dung str | bytes | None (= thư mục)}. Luôn có ops/land/."""
    goc = Path(tempfile.mkdtemp(prefix="kiem-ho-so-land-"))
    (goc / "ops/land").mkdir(parents=True)
    for rel, nd in tep.items():
        p = goc / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        if nd is None:
            p.mkdir()
        elif isinstance(nd, bytes):
            p.write_bytes(nd)
        else:
            p.write_text(nd, encoding="utf-8")
    return goc


def _ho_so(sha=f"'{SHA}'", url=f"'{URL}#issuecomment-1'", landed="true", goc=False, them=""):
    dong = []
    if sha is not None:
        dong.append(f"authorized_head_sha: {sha}")
    if url is not None:
        dong.append(f"authorization_url: {url}")
    dong.append(them)
    dong.append(f"landed: {landed}" if goc else f"trang_thai_packet:\n  landed: {landed}")
    return "\n".join(d for d in dong if d) + "\n"


def _ld(ten):
    return f"ops/land/{ten}-land-evidence.yaml"


# ---- B1 + B1c: một cây, mỗi hồ sơ vi phạm đúng một mệnh đề; (tên, nội dung, trạng thái, khoá phải nêu, khoá không nêu)
B1 = [
    ("dat-ic", _ho_so(), "DAT", (), ()),
    ("dat-prr", _ho_so(url=f"'{URL}#pullrequestreview-2'"), "DAT", (), ()),
    ("dat-disc", _ho_so(url=f"'{URL}#discussion_r3'"), "DAT", (), ()),
    ("sha39", _ho_so(sha=f"'{SHA[:39]}'"), "TRUOT", ("authorized_head_sha",), ("authorization_url",)),
    ("sha-hoa", _ho_so(sha=f"'{SHA.upper()}'"), "TRUOT", ("authorized_head_sha",), ("authorization_url",)),
    ("sha-lf", _ho_so(sha=f"|\n  {SHA}"), "TRUOT", ("authorized_head_sha",), ("authorization_url",)),
    ("sha-so", _ho_so(sha="1234567890123456789012345678901234567890"), "TRUOT", ("authorized_head_sha",),
     ("authorization_url",)),
    ("long", _ho_so(sha=None, url=None, them=f"candidates:\n- authorized_head_sha: '{SHA}'\n"
                    f"  authorization_url: '{URL}#issuecomment-1'"), "TRUOT",
     ("authorized_head_sha", "authorization_url"), ()),
    ("url-ngoai", _ho_so(url="'https://gitlab.com/ducthangho/tra-luat/pull/1#issuecomment-1'"), "TRUOT",
     ("authorization_url",), ("authorized_head_sha",)),
    ("url-gia", _ho_so(url="'https://evil.example/github.com/ducthangho/tra-luat/pull/1#issuecomment-1'"), "TRUOT",
     ("authorization_url",), ("authorized_head_sha",)),
    ("url-nhung", _ho_so(url=f"'https://evil.example/?next={URL}#issuecomment-1'"), "TRUOT",
     ("authorization_url",), ("authorized_head_sha",)),
    ("url-thieu-manh", _ho_so(url="'https://github.com/ducthangho/tra-luat/pull/721'"), "TRUOT",
     ("authorization_url",), ("authorized_head_sha",)),
    ("goc-hoa", _ho_so(sha=f"'{SHA.upper()}'", goc=True), "TRUOT", ("authorized_head_sha",), ("authorization_url",)),
    ("sha41", _ho_so(sha=f"'{SHA}a'"), "TRUOT", ("authorized_head_sha",), ("authorization_url",)),
    ("sha64", _ho_so(sha=f"'{SHA}{SHA[:24]}'"), "TRUOT", ("authorized_head_sha",), ("authorization_url",)),
    ("url-anh-em", _ho_so(url="'https://github.com/ducthangho/tra-luat-evil/pull/1#issuecomment-1'"), "TRUOT",
     ("authorization_url",), ("authorized_head_sha",)),
    ("boqua-false", _ho_so(sha=None, url=None, landed="false"), "BO_QUA", (), ()),
    ("boqua-chuoi", _ho_so(sha=None, url=None, landed="'true'"), "BO_QUA", (), ()),
    ("boqua-mot", _ho_so(sha=None, url=None, landed="1"), "BO_QUA", (), ()),
]


def ca_b1_rang_l6():
    goc = _cay({_ld(t): nd for t, nd, *_ in B1})
    try:
        rc, kq, _, err = _chay(goc, tiem=True)
        assert rc == 1, f"rc {rc} (cần 1); {err[-300:]}"
        theo = {t["duong_dan"]: t for t in kq["tep"]}
        assert len(theo) == len(B1), f"{len(theo)} tệp (cần {len(B1)})"
        for ten, _, cho, phai, khong in B1:
            t = theo[_ld(ten)]
            assert t["trang_thai"] == cho, f"{ten}: {t['trang_thai']} (cần {cho}) — {t['ly_do']}"
            for k in phai:
                assert k in t["ly_do"], f"{ten}: ly_do thiếu {k}: {t['ly_do']}"
            for k in khong:
                assert k not in t["ly_do"], f"{ten}: ly_do nêu thừa {k}: {t['ly_do']}"
        n_true = sum(1 for _, _, cho, *_ in B1 if cho != "BO_QUA")
        assert (kq["n_dat"], kq["n_landed"], kq["n_mien_tru"]) == (3, n_true, 0), (kq["n_dat"], kq["n_landed"])
    finally:
        shutil.rmtree(goc)


# ---- B1b: fail-close, mỗi ca một cây riêng ⇒ rc 3, không ca nào thành BO_QUA âm thầm.
B1B = [
    ("yaml-ngoac", {_ld("a"): "authorized_head_sha: [abc\n"}),
    ("yaml-tab", {_ld("a"): "trang_thai_packet:\n\tlanded: true\n"}),
    ("rong", {_ld("a"): ""}),
    ("goc-danh-sach", {_ld("a"): "- landed: true\n"}),
    ("tp-chuoi", {_ld("a"): "trang_thai_packet: xong\n"}),
    ("tp-null", {_ld("a"): "trang_thai_packet:\n"}),
    ("tron", {_ld("a"): _ho_so(sha=None), _ld("b"): "x: [\n"}),
    ("khong-utf8", {_ld("a"): b"landed: true\nx: \xff\xfe\n"}),
    ("thu-muc", {_ld("x"): None}),
]


def ca_b1b_fail_close():
    for ten, tep in B1B:
        goc = _cay(tep)
        try:
            rc, kq, out, err = _chay(goc, tiem=True)
            assert rc == 3, f"{ten}: rc {rc} (cần 3); {err[-200:]}"
            assert "Traceback" not in err, f"{ten}: traceback"
            assert all(t["trang_thai"] != "BO_QUA" for t in kq["tep"]), f"{ten}: thành BO_QUA"
        finally:
            shutil.rmtree(goc)


def ca_b1b_the_python():
    goc = _cay({_ld("a"): "x: !!python/object/apply:builtins.print ['TAI-TRONG-CHAY']\n"})
    try:
        rc, _, out, err = _chay(goc, tiem=True)
        assert rc == 3, f"rc {rc} (cần 3)"
        assert "TAI-TRONG-CHAY" not in out + err, "tải trọng của thẻ đã chạy (hoặc bị in lại)"
    finally:
        shutil.rmtree(goc)


def ca_b1b_thieu_pyyaml():
    goc = _cay({_ld("a"): _ho_so()})
    try:
        rc, _, _, err = _chay(goc, chan_yaml=True)
        assert rc == 3, f"rc {rc} (cần 3, tiêm miễn trừ {{}}); {err[-200:]}"
    finally:
        shutil.rmtree(goc)


# ---- B2: CLI thật, KHÔNG tiêm — đo hằng của bản giao.
def ca_b2_mien_tru_hang():
    goc = _cay({PR672: _ho_so(sha=None, url=None)})
    try:
        rc, _, out, err = _chay(goc, json_out=False)
        assert rc == 0, f"ca A rc {rc} (cần 0); {out[-300:]}{err[-200:]}"
        dong = [d for d in out.splitlines() if d.split(" ", 1)[0] == "MIEN_TRU"]
        assert len(dong) == 1, f"ca A {len(dong)} dòng MIEN_TRU (cần 1)"
        assert PR672 in dong[0], dong[0]
        ly_do = dong[0].split(" — ", 1)[1] if " — " in dong[0] else ""
        assert ly_do.split(" (", 1)[0].strip(), f"ca A lý do rỗng: {dong[0]!r}"
        rc_j, kq, _, _ = _chay(goc)
        assert rc_j == 0 and kq["n_mien_tru"] == 1, (rc_j, kq and kq["n_mien_tru"])
    finally:
        shutil.rmtree(goc)
    goc = _cay({_ld("khac"): _ho_so()})
    try:
        rc, _, _, _ = _chay(goc, json_out=False)
        assert rc == 3, f"ca B (không có pr672) rc {rc} (cần 3 — miễn trừ vắng)"
    finally:
        shutil.rmtree(goc)


# ---- B2b: phạm vi quét — không đệ quy, tên tệp là quy ước.
def ca_b2b_pham_vi():
    goc = _cay({_ld("z"): _ho_so(), "ops/land/x-provenance.yaml": _ho_so(sha=None, url=None),
                "ops/land/sub/y-land-evidence.yaml": _ho_so(sha=None, url=None)})
    try:
        rc, kq, _, _ = _chay(goc, tiem=True)
        assert rc == 0, f"rc {rc} (cần 0)"
        assert [t["duong_dan"] for t in kq["tep"]] == [_ld("z")], kq["tep"]
    finally:
        shutil.rmtree(goc)


# ---- B3 (iii)/(iv) trên cây tạm: glob là một TOKEN riêng ở đầu ra chữ và bằng đúng ở JSON.
def ca_glob_token():
    goc = _cay({_ld("z"): _ho_so()})
    try:
        rc, _, out, _ = _chay(goc, tiem=True, json_out=False)
        assert rc == 0, f"rc {rc}"
        assert sum(1 for d in out.splitlines() if GLOB in d.split()) == 1, "không có đúng một dòng mang token glob"
        _, kq, _, _ = _chay(goc, tiem=True)
        assert kq["phamvi_glob"] == GLOB, kq["phamvi_glob"]
    finally:
        shutil.rmtree(goc)


# ---- B7: --root sai ⇒ rc 2, không in dòng đếm nào.
def ca_b7_root_sai():
    tam = Path(tempfile.mkdtemp(prefix="kiem-ho-so-land-root-"))
    try:
        tep = tam / "mot-tep"
        tep.write_text("x\n", encoding="utf-8")
        rong = tam / "rong"
        rong.mkdir()
        for ten, r in (("khong-ton-tai", tam / "khong-co"), ("tep", tep), ("rong", rong)):
            for js in (False, True):
                p = subprocess.run([sys.executable, "-B", str(TOOL), "--root", str(r)] + (["--json"] if js else []),
                                   capture_output=True, text=True, encoding="utf-8", timeout=60)
                assert p.returncode == 2, f"{ten}: rc {p.returncode} (cần 2)"
                assert "TỔNG" not in p.stdout and "n_dat" not in p.stdout, f"{ten}: in dòng đếm"
    finally:
        shutil.rmtree(tam)


def ca_b1b_scalar_hong():
    """PR #918 (Codex P2): lỗi DỰNG scalar không phải YAMLError — phải ra LOI/rc 3, JSON hợp lệ, tệp khác vẫn báo."""
    hong = {
        "thang-13": "recorded_at: 2026-13-01\n",
        "the-timestamp": "x: !!timestamp 'x'\n",
        "the-int": "x: !!int 'x'\n",
        "long-sau": "x: " + "[" * 3000 + "]" * 3000 + "\n",
    }
    for ten, nd in hong.items():
        goc = _cay({_ld(ten): _ho_so(them=nd.rstrip("\n")) if ten != "long-sau" else nd, _ld("zz-tot"): _ho_so()})
        try:
            rc, kq, _, err = _chay(goc, tiem=True)
            assert rc == 3, f"{ten}: rc {rc} (cần 3); {err[-200:]}"
            assert "Traceback" not in err, f"{ten}: traceback"
            assert kq is not None, f"{ten}: stdout không phải JSON"
            theo = {t["duong_dan"]: t["trang_thai"] for t in kq["tep"]}
            assert theo == {_ld(ten): "LOI", _ld("zz-tot"): "DAT"}, f"{ten}: {theo}"
        finally:
            shutil.rmtree(goc)


# ---- wp981 (spec `ops/specs/wp981-r2.md`): kiểu b — khối `landed_<8 chữ số>` ở mức gốc.
def _b(goc_url="'https://github.com/ducthangho/tra-luat/pull/1'", ten="landed_20261027", landed="true",
       tt="da_duyet", comment=f"'{URL}#issuecomment-9'", tp="false"):
    dong = [f"authorized_head_sha: '{SHA}'"]
    if goc_url is not None:
        dong.append(f"authorization_url: {goc_url}")
    dong += [f"trang_thai_packet:\n  landed: {tp}", f"{ten}:\n  landed: {landed}\n  quyet_dinh_chu_kho:\n    trang_thai: {tt}"]
    if comment is not None:
        dong.append(f"    comment: {comment}")
    return "\n".join(dong) + "\n"


KB = "landed_20261027.quyet_dinh_chu_kho"
# (tên, nội dung, trạng thái, khoá phải nêu trong ly_do); mục spec N1 ở chú thích.
WP981 = [
    ("b-du", _b(), "DAT", ("landed_20261027.landed",)),                                       # (i)
    ("b-ab", _b(tp="true", goc_url=f"'{URL}#issuecomment-1'"), "DAT", ("trang_thai_packet.landed",)),
    ("b-cmt-manh", _b(comment=f"'{URL}'"), "TRUOT", (KB + ".comment",)),                      # (ii)
    ("b-cmt-tien-to", _b(comment="'https://gitlab.com/x/pull/1#issuecomment-9'"), "TRUOT", (KB + ".comment",)),
    ("b-cmt-so", _b(comment="123"), "TRUOT", (KB + ".comment",)),
    ("b-tt", _b(tt="cho_duyet"), "TRUOT", (KB + ".trang_thai",)),                             # (iii)
    ("b-landed-chuoi", _b(landed="'true'"), "BO_QUA", ()),                                    # (iv)
    ("b-landed-mot", _b(landed="1"), "BO_QUA", ()),
    ("a-khong-manh", _b(tp="true", landed="false"), "TRUOT", ("authorization_url",)),        # (vi)
    ("b-kad", _b(goc_url="KHONG_AP_DUNG"), "DAT", ()),                                        # (viii)
    ("b-vang-url", _b(goc_url=None), "DAT", ()),
    ("b-kad-cmt-vang", _b(goc_url="KHONG_AP_DUNG", comment=None), "TRUOT", (KB + ".comment",)),
    ("ten-7so", _b(ten="landed_2026102"), "BO_QUA", ()),                                      # (vii)
    ("ten-x", _b(ten="landed_x"), "BO_QUA", ()),
]
WP981_LOI = {"khoi-chuoi": "landed_20261027: xong\n", "khoi-ds": "landed_20261027:\n- landed: true\n"}  # (v)


def _wp981_ket_qua(tool):
    """Trả {tên ca con: None (đạt) | lý do đỏ}. Dùng chung cho bản thật và bản đột biến."""
    kq = {}
    goc = _cay({_ld(t): nd for t, nd, *_ in WP981})
    try:
        rc, j, _, err = _chay(goc, tiem=True, tool=tool)
        theo = {t["duong_dan"]: t for t in (j or {}).get("tep", [])}
        for ten, _, cho, phai in WP981:
            t = theo.get(_ld(ten))
            if t is None:
                kq[ten] = f"vắng (rc {rc}; {err[-200:]})"
            elif t["trang_thai"] != cho or not all(k in t["ly_do"] for k in phai):
                kq[ten] = f"{t['trang_thai']} (cần {cho}, phải nêu {phai}) — {t['ly_do']}"
            else:
                kq[ten] = None
    finally:
        shutil.rmtree(goc)
    for ten, nd in WP981_LOI.items():
        goc = _cay({_ld(ten): f"authorized_head_sha: '{SHA}'\n" + nd})
        try:
            rc, j, _, err = _chay(goc, tiem=True, tool=tool)
            ok = rc == 3 and "Traceback" not in err and j and j["tep"][0]["trang_thai"] == "LOI"
            kq[ten] = None if ok else f"rc {rc} (cần 3, LOI); {err[-200:]}"
        finally:
            shutil.rmtree(goc)
    return kq


def ca_wp981_kieu_b():
    do = {k: v for k, v in _wp981_ket_qua(TOOL).items() if v}
    assert not do, do


# Đột biến trên BẢN SAO TẠM (CLAUDE.md: không ghi tệp thật); mỗi đột biến phải làm ĐỎ đúng ca con đích.
DOT_BIEN_WP981 = [
    ("bo_nhanh_b", 'khoi_true = [k for k in khoi if doc[k].get("landed") is True]', "khoi_true = []", "b-du"),
    ("bo_da_duyet", 'if not (isinstance(tt, str) and tt == "da_duyet"):', "if False:", "b-tt"),
    ("noi_kieu_a", "doi_url_goc=landed is True)", "doi_url_goc=False)", "a-khong-manh"),
    ("doi_url_goc_kieu_b", "doi_url_goc=landed is True)", "doi_url_goc=True)", "b-kad"),
    ("bo_kiem_comment", 'if not _url_hop_le(q.get("comment")):', "if False:", "b-cmt-manh"),
    ("ep_kieu_landed_khoi", '.get("landed") is True]', '.get("landed")]', "b-landed-chuoi"),
    ("bo_loi_khoi", "if not isinstance(doc[k], dict):", "if False:", "khoi-chuoi"),
    ("noi_ten_khoi", 'RE_KHOI = re.compile(r"landed_\\d{8}")', 'RE_KHOI = re.compile(r"landed_\\w+")', "ten-x"),
]


def ca_wp981_dot_bien():
    goc_ma = TOOL.read_text(encoding="utf-8")
    tam = Path(tempfile.mkdtemp(prefix="kiem-ho-so-land-dot-bien-"))
    try:
        song = []
        for ten, cu, moi, dich in DOT_BIEN_WP981:
            assert goc_ma.count(cu) == 1, f"{ten}: mẫu không khớp đúng một lần"
            ban = tam / f"kiem_ho_so_land_{ten}.py"
            ban.write_text(goc_ma.replace(cu, moi), encoding="utf-8")
            if _wp981_ket_qua(ban).get(dich) is None:
                song.append(f"{ten} (đích {dich})")
        assert not song, f"đột biến sống: {song}"
    finally:
        shutil.rmtree(tam)


CA = [ca_b1_rang_l6, ca_b1b_fail_close, ca_b1b_the_python, ca_b1b_scalar_hong, ca_b1b_thieu_pyyaml,
      ca_b2_mien_tru_hang, ca_b2b_pham_vi, ca_glob_token, ca_b7_root_sai, ca_wp981_kieu_b, ca_wp981_dot_bien]


def main():
    dat = 0
    for ca in CA:
        try:
            ca()
            dat += 1
        except Exception as e:  # ca đỏ vì bất kỳ lý do nào đều là đỏ; in tên ca và lý do
            print(f"DO {ca.__name__}: {type(e).__name__}: {e}")
    print(f"{dat}/{len(CA)}")
    return 0 if dat == len(CA) else 1


if __name__ == "__main__":
    sys.exit(main())
