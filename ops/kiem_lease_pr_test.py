#!/usr/bin/env python3
"""Test cho `ops/kiem_lease_pr.py` + `.github/workflows/lease-pr.yml` — packet #1445 r1 (đặc tả `ops/specs/lease-pr-r1.md` §3).

Ca CHẠY THẬT `kiem_lease` trên cây thật (lease hết hạn ⇒ tiến trình con `kiem(bo_qua_han=True)`), ca đồ giả cho nhánh
lease còn hạn (`lease_publish.py check`), và khoá cấu trúc workflow. Sau đó chạy lại toàn bộ ca trên từng ĐỘT BIẾN (bản sao tạm,
không đụng tệp thật): mỗi đột biến phải làm ĐÚNG ca có tên đỏ, nếu không bộ test không có răng.

In: `CA: n/n dat`, `DOT BIEN: k/k bi giet dung ca`, `TONG: DAT|DO`. Thoát 0 chỉ khi mọi ca đạt và mọi đột biến bị giết đúng ca.
"""
from __future__ import annotations

import contextlib
import importlib.util
import io
import os
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timedelta, timezone
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
MA = HERE / "kiem_lease_pr.py"
CDN = HERE / "ci_duong_nhanh.py"
WF = ROOT / ".github" / "workflows" / "lease-pr.yml"
# Fixture CÂY THẬT. Tiền đề được kiểm lại trong ca (đổi nội dung ⇒ `fixture vo hieu`, không xanh giả).
LEASE_HONG = "ops/leases/wp1319-r1-g1-operator.yaml"     # hết hạn, thiếu `reviewed_sha_required`
LEASE_TOT = "ops/leases/px-ask-r5-g1-operator.yaml"      # hết hạn (thu hồi), đủ trường
SHA_A, SHA_B, SHA_C = "a" * 40, "b" * 40, "c" * 40


class TinHieuCa(AssertionError):
    """Chỉ `bang()` ném lớp này: lỗi vô can không giả được tín hiệu 'ca đỏ'."""


def bang(dk, msg):
    if not dk:
        raise TinHieuCa(msg)


def nap(duong: Path, ten: str):
    spec = importlib.util.spec_from_file_location(ten, duong)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


@contextlib.contextmanager
def diff_gia(m, tap):
    """Thay `doc_diff` của module ci_duong_nhanh mà `m` đã import bằng một tập cố định; trả lại bản gốc khi ra."""
    goc = m.cdn.doc_diff
    m.cdn.doc_diff = lambda env, chay_lenh=None, kho=None: (set(tap) if tap is not None else None)
    try:
        yield
    finally:
        m.cdn.doc_diff = goc


@contextlib.contextmanager
def actor(gia_tri):
    """Review r1 F1: `kiem`/`check` đọc `GITHUB_ACTOR` của TIẾN TRÌNH (tiến trình con thừa kế). Trong Actions biến này luôn có
    (người đẩy PR), nên ca cây thật phải tự đặt nó, không được ăn theo ai đang chạy selftest. None = gỡ biến."""
    cu = os.environ.get("GITHUB_ACTOR")
    if gia_tri is None:
        os.environ.pop("GITHUB_ACTOR", None)
    else:
        os.environ["GITHUB_ACTOR"] = gia_tri
    try:
        yield
    finally:
        if cu is None:
            os.environ.pop("GITHUB_ACTOR", None)
        else:
            os.environ["GITHUB_ACTOR"] = cu


def chay_m(m, env, **kw):
    ra = io.StringIO()
    rc = m.chay(env=env, ra=ra, **kw)
    return rc, ra.getvalue()


PR = {"CI_DUONG_NHANH_SU_KIEN": "pull_request", "CI_DUONG_NHANH_GOC": SHA_A, "CI_DUONG_NHANH_DAU": SHA_B,
      "CI_DUONG_NHANH_MERGE": SHA_C}


def ca_push_khong_goi_git(m, wf):
    goi = []
    rc, out = chay_m(m, {"CI_DUONG_NHANH_SU_KIEN": "push"}, chay_lenh=lambda *a, **k: goi.append(a))
    bang(rc == 0 and not goi, f"push phai rc 0 va khong goi git: rc={rc} goi={len(goi)}")
    bang("bo qua" in out, f"push phai noi ro bo qua: {out!r}")


def ca_sha_hong_thi_do(m, wf):
    for env in ({"CI_DUONG_NHANH_SU_KIEN": "pull_request"}, {**PR, "CI_DUONG_NHANH_GOC": "xyz"}, {**PR, "CI_DUONG_NHANH_MERGE": ""}):
        rc, out = chay_m(m, env, chay_lenh=lambda *a, **k: (_ for _ in ()).throw(AssertionError("khong duoc goi git")))
        bang(rc == 1 and "KHONG DO DUOC" in out, f"SHA vang/hong phai rc 1 KHONG DO DUOC: rc={rc} {out!r}")


def _tien_de(duong, can_hong):
    bang((ROOT / duong).is_file(), f"fixture vo hieu: {duong} khong con tren cay")
    d = yaml.safe_load((ROOT / duong).read_text(encoding="utf-8"))
    het = datetime.fromisoformat(str(d["lease_expires_at_utc"]).replace("Z", "+00:00")) <= datetime.now(timezone.utc)
    thieu = d.get("reviewed_sha_required") in (None, "")
    bang(het and (thieu if can_hong else not thieu), f"fixture vo hieu: {duong} (het_han={het}, thieu_reviewed_sha={thieu})")


def ca_lease_hong_that_thi_do(m, wf):
    _tien_de(LEASE_HONG, True)
    with diff_gia(m, {LEASE_HONG, "README.md"}), actor(None):
        rc, out = chay_m(m, PR, kho=ROOT)
    bang(rc == 1, f"lease hong phai rc 1, duoc {rc}: {out[-400:]!r}")
    bang("LOI" in out and LEASE_HONG in out and "reviewed_sha_required" in out, f"loi phai neu dung tep va truong: {out[-400:]!r}")


def ca_lease_tot_that_thi_dat(m, wf):
    _tien_de(LEASE_TOT, False)
    with diff_gia(m, {LEASE_TOT, "scripts/tl.py"}), actor(None):
        rc, out = chay_m(m, PR, kho=ROOT)
    bang(rc == 0 and "DAT (1 lease doi" in out, f"lease tot phai rc 0, 1 lease: rc={rc} {out[-400:]!r}")


def ca_actor_la(m, wf):
    """Review r1 F1: người ngoài danh sách cấp lease mở PR KHÔNG đụng lease ⇒ xanh; đụng lease (kể cả hết hạn) ⇒ đỏ `CHAN [4]`,
    đúng chốt thẩm quyền của `kiem` (đặc tả §2 ghi thiếu vế lease hết hạn — sửa ở VERDICT r1)."""
    with actor("nguoi-ngoai-1445"):
        with diff_gia(m, {"README.md", "scripts/tl.py"}):
            rc, out = chay_m(m, PR, kho=ROOT)
        bang(rc == 0, f"actor la + khong lease phai rc 0, duoc {rc}: {out!r}")
        _tien_de(LEASE_TOT, False)
        with diff_gia(m, {LEASE_TOT}):
            rc, out = chay_m(m, PR, kho=ROOT)
        bang(rc == 1 and "CHAN [4]" in out, f"actor la + sua lease phai rc 1 CHAN [4]: rc={rc} {out[-300:]!r}")


def ca_muc_khong_phai_tep_thuong(m, wf):
    """Review r1 F2: symlink treo / symlink tới tệp / thư mục đặt đúng tên lease ⇒ ĐỎ, không được coi là 'đã xoá'."""
    with tempfile.TemporaryDirectory() as t:
        kho = Path(t)
        d = kho / "ops" / "leases"
        d.mkdir(parents=True)
        (kho / "that.yaml").write_text("lease_id: x\n", encoding="utf-8")
        os.symlink("khong-co", d / "treo.yaml")
        os.symlink(kho / "that.yaml", d / "tro.yml")
        (d / "thu-muc.yaml").mkdir()
        for ten in ("treo.yaml", "tro.yml", "thu-muc.yaml"):
            with diff_gia(m, {f"ops/leases/{ten}"}):
                rc, out = chay_m(m, PR, kho=kho, chay_lenh=lambda *a, **k: type("R", (), {"returncode": 0, "stdout": b"", "stderr": b""})())
            bang(rc == 1 and "khong phai tep thuong" in out, f"{ten}: muc khong phai tep thuong phai rc 1: rc={rc} {out!r}")


def ca_xoa_lease_thi_dat(m, wf):
    with diff_gia(m, {"ops/leases/khong-ton-tai-1445.yaml"}):
        rc, out = chay_m(m, PR, kho=ROOT)
    bang(rc == 0 and "da xoa" in out, f"lease da xoa phai bo qua, rc 0: rc={rc} {out!r}")


def ca_khong_lease_thi_dat(m, wf):
    # Review r1 luot 2 P3: `ops/leases-extra/…` KHONG la lease (tien to phai co `/`).
    with diff_gia(m, {"scripts/tl.py", "ops/leases/README.md", "ops/leases-extra/a.yaml"}):
        rc, out = chay_m(m, PR, kho=ROOT)
    bang(rc == 0 and "DAT (0 lease doi trong 3 tep doi" in out, f"khong lease phai rc 0, 0 lease: rc={rc} {out!r}")


def ca_cli_that(m, wf):
    """Review r1 luot 2 P3: chay DUNG diem vao CLI (`python <tep>`), khong chi ham import: push => rc 0, PR thieu SHA => rc 1."""
    tep = Path(m.__file__)
    env = {k: v for k, v in os.environ.items() if not k.startswith("CI_DUONG_NHANH_")}
    r1 = subprocess.run([sys.executable, "-B", str(tep)], env={**env, "CI_DUONG_NHANH_SU_KIEN": "push"}, capture_output=True, text=True)
    r2 = subprocess.run([sys.executable, "-B", str(tep)], env={**env, "CI_DUONG_NHANH_SU_KIEN": "pull_request"}, capture_output=True, text=True)
    bang(r1.returncode == 0 and "bo qua" in r1.stdout, f"CLI push phai rc 0: rc={r1.returncode} {r1.stdout!r} {r1.stderr[-200:]!r}")
    bang(r2.returncode == 1 and "KHONG DO DUOC" in r2.stdout, f"CLI PR thieu SHA phai rc 1: rc={r2.returncode} {r2.stdout!r}")


def ca_lease_con_han_goi_check(m, wf):
    """Nhánh lease CÒN HẠN đi `lease_publish.py check` (đồ giả ghi lệnh); rc khác 0 của check ⇒ PR đỏ."""
    with tempfile.TemporaryDirectory() as t:
        kho = Path(t)
        (kho / "ops" / "leases").mkdir(parents=True)
        han = (datetime.now(timezone.utc) + timedelta(hours=3)).strftime("%Y-%m-%dT%H:%M:%SZ")
        (kho / "ops" / "leases" / "x.yml").write_text(f"lease_id: x\nlease_expires_at_utc: '{han}'\n", encoding="utf-8")
        (kho / "ops" / "leases" / "sub").mkdir()
        (kho / "ops" / "leases" / "sub" / "y.yaml").write_text(f"lease_id: y\nlease_expires_at_utc: '{han}'\n", encoding="utf-8")
        for rc_gia, rc_mong in ((0, 0), (8, 1)):
            lenh = []

            class R:
                returncode = rc_gia
                stdout = b"CHAN [8]: gia\n"
                stderr = b""

            def gia(cmd, **k):
                lenh.append(list(cmd))
                return R()
            with diff_gia(m, {"ops/leases/x.yml", "ops/leases/sub/y.yaml"}):
                rc, out = chay_m(m, PR, kho=kho, chay_lenh=gia)
            bang(sorted(c[3] for c in lenh) == ["ops/leases/sub/y.yaml", "ops/leases/x.yml"]
                 and all(c[1:3] == ["ops/lease_publish.py", "check"] for c in lenh),
                 f"lease con han (ca .yml va thu muc con) phai goi dung `lease_publish.py check <tep>`: {lenh}")
            bang("lease doi: 'ops/leases/x.yml'" in out and "lease doi: 'ops/leases/sub/y.yaml'" in out and "2 lease doi" in out,
                 f"phai liet ke ca hai lease doi: {out!r}")
            bang(rc == rc_mong, f"check rc={rc_gia} => PR rc phai {rc_mong}, duoc {rc}: {out!r}")


def ca_cau_truc_workflow(m, wf):
    d = yaml.safe_load(wf)
    on = d.get("on", d.get(True))
    bang(isinstance(on, dict) and set(on) == {"pull_request"}, f"workflow chi `on: pull_request`, duoc {on!r}")
    # Review r1 luot 2 P3: KHONG bo loc (paths/branches/types) — gate phai chay tren MOI PR mac dinh.
    bang(on["pull_request"] in (None, {}), f"`pull_request` khong duoc co bo loc, duoc {on['pull_request']!r}")
    bang(d.get("permissions") == {"contents": "read"}, f"permissions phai dung contents: read, duoc {d.get('permissions')!r}")
    jobs = d.get("jobs") or {}
    bang(list(jobs) == ["kiem-lease-pr"], f"dung mot job kiem-lease-pr, duoc {list(jobs)}")
    j = jobs["kiem-lease-pr"]
    bang("if" not in j and "continue-on-error" not in j, "job khong duoc co if/continue-on-error (check se vang mat/nuot loi)")
    st = j.get("steps") or []
    co = [s for s in st if str(s.get("uses", "")).startswith("actions/checkout@")]
    bang(len(co) == 1 and (co[0].get("with") or {}).get("fetch-depth") == 0, "checkout phai fetch-depth: 0 (merge-base + bia mo)")
    runs = [s.get("run", "").strip() for s in st if "run" in s]
    bang(runs[-2:] == ["python ops/kiem_lease_pr_test.py", "python ops/kiem_lease_pr.py"],
         f"hai lenh cuoi phai la selftest roi kiem: {runs[-2:]!r}")
    cuoi = st[-1]
    # Review r1 F3: `if: false` là `False` trong Python — kiểm SỰ CÓ MẶT của khoá, không kiểm truthiness. Áp cho MỌI bước.
    for s_ in st:
        bang("if" not in s_ and "continue-on-error" not in s_, f"buoc {s_.get('name') or s_.get('uses')!r} khong duoc co if/continue-on-error")
    bang(cuoi.get("env") == {
        "CI_DUONG_NHANH_SU_KIEN": "${{ github.event_name }}",
        "CI_DUONG_NHANH_GOC": "${{ github.event.pull_request.base.sha }}",
        "CI_DUONG_NHANH_DAU": "${{ github.event.pull_request.head.sha }}",
        "CI_DUONG_NHANH_MERGE": "${{ github.sha }}"}, f"env buoc kiem sai: {cuoi.get('env')!r}")


CA = [ca_push_khong_goi_git, ca_sha_hong_thi_do, ca_lease_hong_that_thi_do, ca_lease_tot_that_thi_dat, ca_actor_la,
      ca_muc_khong_phai_tep_thuong, ca_xoa_lease_thi_dat, ca_khong_lease_thi_dat, ca_cli_that, ca_lease_con_han_goi_check,
      ca_cau_truc_workflow]

# (ten, tep, chuoi goc, chuoi thay, ca phai do)
DOT_BIEN = [
    ("bo_chot_su_kien", "ma", 'if su_kien != "pull_request":', "if False:", "ca_push_khong_goi_git"),
    ("none_thanh_dat", "ma", "        return 1\n    lease = sorted(", "        return 0\n    lease = sorted(", "ca_sha_hong_thi_do"),
    ("nuot_loi_lease", "ma", "return 1 if loi else 0", "return 0", "ca_lease_hong_that_thi_do"),
    ("bo_fetch_depth", "wf", "          fetch-depth: 0\n", "          fetch-depth: 1\n", "ca_cau_truc_workflow"),
    ("symlink_coi_la_xoa", "ma", "elif p.is_symlink() or not p.is_file():", "elif False:", "ca_muc_khong_phai_tep_thuong"),
    ("loc_hai_gach", "ma", "loi += cdn.kiem_lease(doi,", "loi += cdn.kiem_lease({x for x in doi if x.count('/') == 2},",
     "ca_lease_con_han_goi_check"),
    ("if_false_buoc_kiem", "wf", "        run: python ops/kiem_lease_pr.py\n", "        if: false\n        run: python ops/kiem_lease_pr.py\n",
     "ca_cau_truc_workflow"),
    ("tien_to_thieu_gach", "ma", 'duong.startswith("ops/leases/")', 'duong.startswith("ops/leases")', "ca_khong_lease_thi_dat"),
    ("loc_paths", "wf", "  pull_request:\n", "  pull_request:\n    paths: [\"ops/leases/**\"]\n", "ca_cau_truc_workflow"),
    ("cli_luon_0", "ma", "raise SystemExit(chay())", "raise SystemExit(0)", "ca_cli_that"),
    ("coe_selftest", "wf", "        run: python ops/kiem_lease_pr_test.py\n",
     "        continue-on-error: true\n        run: python ops/kiem_lease_pr_test.py\n", "ca_cau_truc_workflow"),
]


def chay_ca(m, wf):
    kq = {}
    for f in CA:
        try:
            f(m, wf)
            kq[f.__name__] = None
        except TinHieuCa as e:
            kq[f.__name__] = str(e)
    return kq


def main() -> int:
    wf = WF.read_text(encoding="utf-8")
    kq = chay_ca(nap(MA, "kiem_lease_pr_that"), wf)
    for ten, loi in kq.items():
        print(("DAT " if loi is None else "DO  ") + ten + ("" if loi is None else f" :: {loi}"))
    dat = sum(1 for x in kq.values() if x is None)
    print(f"CA: {dat}/{len(kq)} dat")
    giet = 0
    for ten, tep, goc, thay, ca_dich in DOT_BIEN:
        with tempfile.TemporaryDirectory() as t:
            nguon = MA.read_text(encoding="utf-8") if tep == "ma" else wf
            bang_ok = nguon.count(goc) == 1
            if not bang_ok:
                print(f"DOT BIEN {ten}: KHONG AP DUOC (moc xuat hien {nguon.count(goc)} lan) - tinh la song")
                continue
            moi = nguon.replace(goc, thay)
            if tep == "ma":
                shutil.copy(CDN, Path(t) / "ci_duong_nhanh.py")
                (Path(t) / "kiem_lease_pr.py").write_text(moi, encoding="utf-8")
                m2, wf2 = nap(Path(t) / "kiem_lease_pr.py", f"kiem_lease_pr_dot_bien_{ten}"), wf
            else:
                m2, wf2 = nap(MA, f"kiem_lease_pr_wf_{ten}"), moi
            kq2 = chay_ca(m2, wf2)
            do = sorted(k for k, v in kq2.items() if v is not None)
            ok = ca_dich in do
            giet += ok
            print(f"DOT BIEN {ten}: {'GIET' if ok else 'SONG'} (ca do: {do}, can: {ca_dich})")
    print(f"DOT BIEN: {giet}/{len(DOT_BIEN)} bi giet dung ca")
    tong = dat == len(kq) and giet == len(DOT_BIEN)
    print(f"TONG: {'DAT' if tong else 'DO'}")
    return 0 if tong else 1


if __name__ == "__main__":
    for s in (sys.stdout, sys.stderr):
        if hasattr(s, "reconfigure"):
            s.reconfigure(encoding="utf-8", errors="backslashreplace")
    raise SystemExit(main())
