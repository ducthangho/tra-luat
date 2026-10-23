#!/usr/bin/env python3
"""Phản chứng cho `ops/ci_duong_nhanh.py` và cho các `if:` đường nhanh trong `.github/workflows/ci.yml`.

Packet #674 `CI-DUONG-NHANH-HO-SO` (đặc tả r2). Bốn tầng, mỗi tầng có ĐỘT BIẾN riêng chạy trên BẢN SAO TẠM. Danh sách và
số lượng ca/đột biến KHÔNG ghi ở đây (đã trôi hai lượt liền): nguồn duy nhất là `CA`, `DOT_BIEN` và dòng `CA:`/`DOT BIEN:` in ra.
  · ca `t*`: hành vi bộ phân loại và bước kiểm rẻ (đồ giả cho ca thuần + KHO GIT THẬT cho ca cần ngữ nghĩa git);
  · ca `y*`: cấu trúc `ci.yml`, canh `if:` cấp job của `gate-ops` và `if:` cấp bước sau G5. "Duy nhất" chỉ ĐO tới hai cổng
    dưới đây (đọc mã, chưa chạy đột biến trên mọi bộ đọc `ci.yml`). Nợ có tên
    `ci-if-cap-job-gate-ops-va-buoc-sau-g5-khong-co-cong-canh` (Q6-i chủ kho): `JOB_G5` của `ci_dang_ky_test.py` KHÔNG chứa
    `gate-ops` (đo lại sau khi #668 land: thêm `gate-cong-cu`, `gate-cong-cu-gop`, vẫn không có `gate-ops`), và
    `cong_cu_test.t6` chỉ soi các bước TRƯỚC G5;
  · ca `k*`: nối vào sổ test sống (mục `DA_NOI` và lời gọi thật trong `run:`);
  · ca khai `@ca_tu_kiem`: tự kiểm của chính bộ test (harness, phân hoạch, docstring, cây dưới đo). Nhóm KHAI tại chỗ,
    không suy từ tiền tố; `t96` đối chiếu với dấu hiệu AST độc lập, và dòng `KIEM KE:` in số từng nhóm.

CÁCH ĐO ĐỘT BIẾN — bài học CLAUDE.md "đột biến bị giết không phải bị giết ĐÚNG LÝ DO":
  · Ca đích chỉ báo ĐỎ bằng `TinHieuChotCa` (con của AssertionError) do CHÍNH `bang()` ném. Lỗi vô can trong mã
    bị đột biến (TypeError, KeyError, ...) đi ra dưới TÊN THẬT ⇒ tiến trình con thoát rc=4 ⇒ `TIN_DUNG_GIA`, không
    tính là giết. Ca KHÔNG được có `except Exception: raise TinHieuChotCa` (ca t99 quét AST canh điều đó).
  · Mỗi đột biến: neo `count == 1` (không thì lỗi hạ tầng), kiểm bản đột biến KHÁC bản gốc, chạy trên tệp tạm với
    tên riêng, bytecode tắt; ca đích còn phải XANH trên bản gốc (chứng minh lượt giết là do đột biến).
  · Đột biến cũng áp cho CHÍNH tệp test (`--nguon-test`): helper fixture (cô lập actor...) có đột biến riêng; và cho BẢN
    SAO `ops/lease_publish.py` trong cây tạm, chỉ để đo phạm vi bia mộ mà docstring D2 khai (`t21b`).
  · Phân hạng có phần tự kiểm (`tu_kiem_phan_hang`, dữ liệu ở `MAU_RC` và `TU_KIEM_DOT_BIEN`; dòng `TU KIEM PHAN HANG:` in số
    lượng ĐẾM TỪ HAI HẰNG SỐ ấy): rc=3 đúng tên ⇒ GIẾT; rc=3 sai tên ⇒ TÍN DỤNG GIẢ; rc=4 ⇒ TÍN DỤNG GIẢ; rc=0 ⇒ SỐNG SÓT;
    rc=-9 ⇒ HỎNG; đột biến KeyError vô can ⇒ TÍN DỤNG GIẢ; chỉ thêm chú thích ⇒ SỐNG SÓT; nới allowlist ⇒ GIẾT. "Sai tên ca"
    chỉ được kiểm bằng mẫu rc, chưa có đột biến thật. Không có bằng chứng dương (tập ca đích rỗng/lạ) thì KHÔNG BAO GIỜ GIẾT (`t97`).

Ra: `CA: N/N dat` · `DOT BIEN: M/M bi giet` · `TONG: DAT`. Thoát 0 chỉ khi N>0, mọi ca đạt, M>0, mọi đột biến bị giết
ĐÚNG LÝ DO, mọi ca tự kiểm đạt — `rc=0` một mình không phải bằng chứng.
"""
from __future__ import annotations

import ast
import concurrent.futures
import contextlib
import importlib.util
import json
import os
import re
import shutil
import socket
import stat
import subprocess
import sys
import tempfile
from pathlib import Path
from unittest import mock

sys.dont_write_bytecode = True
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"

import yaml  # noqa: E402  (PyYAML đã được cài ở vùng setup của job gate-ops)

for _luong in (sys.stdout, sys.stderr):
    if hasattr(_luong, "reconfigure"):
        _luong.reconfigure(encoding="utf-8", errors="backslashreplace")

HERE = Path(__file__).resolve().parent
ROOT_THAT = HERE.parent
# Cây dưới đo: mặc định là kho thật; tiến trình con của một đột biến trỏ vào bản sao tạm qua biến này.
CAY = Path(os.environ.get("CI_DUONG_NHANH_CAY") or ROOT_THAT)
GOC_A, GOC_B = "a" * 40, "b" * 40
FAST = "needs.chuan-bi.outputs.che_do != 'duong_nhanh'"
NHANH = "needs.chuan-bi.outputs.che_do == 'duong_nhanh'"
DUOI_LOG = "vi diff chi gom ops/{land,leases,reviews,specs}/**"
BAT_BUOC = ("gate", "gate-ops", "gate-packet-loop")
# Danh sách bước BỎ ở đường nhanh, theo đặc tả r2 mục M2 ("phải gồm"). Đây là LUẬT của bộ test, không đọc lại từ ci.yml.
BO_QUA = {
    "gate": {"tl selftest (luot PR — khong sinh bang chung)": "github.event_name == 'pull_request' && " + FAST,
             "golden-test": FAST, "determinism-audit strict": FAST, "release-check full": FAST,
             "release-bundle x2 cùng SHA-256": FAST},
    "gate-ops": {"lease-publish selftest (đo lại setup sau G5)": FAST,
                 "bo ca gate chay TRONG cgroup duoc uy quyen (Linux)": "runner.os == 'Linux' && " + FAST,
                 "gate lifecycle selftest (nen khong co cgroup)": "runner.os != 'Linux' && " + FAST},
    "gate-packet-loop": {"packet-loop selftest": FAST},
}
DA_NOI_MUC = "ops/ci_duong_nhanh_test.py"
# LUAT cua bo test (khong doc lai tu ma duoi do): ba ca du lieu ma `kiem-re` phai chay that.
CA_DU_LIEU_CHUAN = ("t23_MOI_lease_THAT_trong_kho_phai_QUA", "t26_moi_bien_nhan_review_phai_khop_BAM_tep_no_tro_toi",
                    "t27_canh_bao_trong_bien_nhan_phai_duoc_NANG_len_muc_luc")
DONG_GOI_TEST = "python ops/ci_duong_nhanh_test.py"


class TinHieuChotCa(AssertionError):
    """Chỉ `bang()` ném lớp này. Mã triển khai và lỗi vô can KHÔNG ném được nó ⇒ phân biệt được giết thật/giả."""


class KhongCoFixture(RuntimeError):
    """Rieng cho viec khong chon duoc fixture lease sach; ca chi bat DUNG lop nay de doi thanh tin hieu."""


class SuDoGia(Exception):
    """Ngoại lệ do CHÍNH ca dựng để đồ giả ném ra; ca chỉ bắt đúng lớp này (không bắt Exception trần)."""


def bang(dieu_kien, thong_diep):
    if not dieu_kien:
        raise TinHieuChotCa(thong_diep)


CA: dict = {}
TU_KIEM_KHAI: set = set()   # nhom KHAI TUONG MINH tai cho dinh nghia (luot 5: phan nhom theo TIEN TO da xep t96 vao "hanh vi")


def ca(f):
    CA[f.__name__] = f
    return f


def ca_tu_kiem(f):
    """Ca tu kiem CUA CHINH bo test (harness, phan hoach, docstring...). t96 doi chieu voi dau hieu AST doc lap."""
    TU_KIEM_KHAI.add(f.__name__)
    return ca(f)


# Dau hieu DOC LAP cua ca tu kiem (t96): than ca cham MOT trong cac ten noi tang nay cua chinh bo test.
DAU_HIEU_TU_KIEM = frozenset({"CA", "DOT_BIEN", "TU_KIEM_KHAI", "phan_hoach_ca", "dong_kiem_ke", "chay_mot_dot_bien",
                              "chay_tap_dot_bien", "phan_hang", "loi_cay_duoi_do", "__doc__",
                              "ci_duong_nhanh_test.py"})


def nap_module():
    spec = importlib.util.spec_from_file_location("ci_duong_nhanh_duoi_test", CAY / "ops" / "ci_duong_nhanh.py")
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


class KQ:
    def __init__(self, rc=0, out=b""):
        self.returncode, self.stdout, self.stderr = rc, out, b""


def nul(*duong):
    return b"".join(x.encode("utf-8", "surrogateescape") + b"\0" for x in duong)


CAY_GIA = "c" * 40
HOP_GIA = "e" * 40   # `github.sha` gia (merge ref)


def bo_attr_source(argv):
    """argv khong co `--attr-source=...` ngay sau `git` — de dinh tuyen do gia doc lap voi chot thuoc tinh (t20u do rieng)."""
    argv = list(argv)
    return argv[:1] + argv[2:] if len(argv) > 1 and str(argv[1]).startswith("--attr-source=") else argv


def _tra_gia(gia_tri):
    """Mot gia tri do gia: ngoai le => nem; (rc, out) => dung nhu vay; bytes => rc=0 neu khac rong, rc=1 neu rong."""
    if isinstance(gia_tri, BaseException):
        raise gia_tri
    if isinstance(gia_tri, tuple):
        return KQ(*gia_tri)
    return KQ(0 if gia_tri else 1, gia_tri or b"")


def _raw_tu_ten(kq):
    """`git diff --raw -z` gia dung tu dau ra `--name-only -z`: moi ten mot ban ghi `M` 100644 -> 100644 (tep thuong)."""
    ra = kq.stdout if isinstance(kq.stdout, (bytes, bytearray)) else b""
    if kq.returncode != 0 or (ra and not ra.endswith(b"\0")):
        return kq
    return KQ(0, b"".join(b":100644 100644 " + b"0" * 40 + b" " + b"1" * 40 + b" M\0" + x + b"\0" for x in ra.split(b"\0") if x))


def raw_ghi(*ban_ghi):
    """Dau ra `--raw -z` gia: moi phan tu (mode_moi, trang_thai, duong)."""
    return b"".join(f":100644 {mode} {'0' * 40} {'1' * 40} {tt}".encode() + b"\0" + d.encode() + b"\0" for mode, tt, d in ban_ghi)


def chay_gia(out=b"", rc=0, nem=None, log=None, merge_base=(GOC_A + "\n").encode(),
             merge_tree=(CAY_GIA + "\n").encode(), diff_cay=(0, b""), merge_ref=(0, b""), raw=None):
    """Do gia git. `--raw` (kiem_mode_git) mac dinh DUNG tu cung nguon `--name-only` cua cap do (tep thuong); `raw` = {"ba_cham" |
    "cay" | "hop": gia tri} ghi de rieng tung cap. `merge-base --all`, `merge-tree`, `diff goc -> cay merge` va `diff goc -> merge ref` (`HOP_GIA`) co gia tri
    RIENG, doc lap voi `out`/`rc`/`nem` cua ba cham (mac dinh: MOT base, merge sach, merge va merge ref khong doi them gi) —
    de moi chot cua ba cham van co rang rieng thay vi bi chot cua `doc_diff_merge` che. `log` ghi argv NGUYEN VAN."""
    def chay(argv, **kw):
        if log is not None:
            log.append(list(argv))
        a = bo_attr_source(argv)
        if a[:3] == ["git", "merge-base", "--all"]:
            return _tra_gia(merge_base)
        if a[:3] == ["git", "merge-tree", "--write-tree"]:
            return _tra_gia(merge_tree)
        if a[:3] == ["git", "diff", "--raw"]:
            khoa = "hop" if a[-1] == HOP_GIA else "cay" if a[-1] == CAY_GIA else "ba_cham"
            if raw and khoa in raw:
                return _tra_gia(raw[khoa])
            if khoa == "ba_cham":
                if nem is not None:
                    raise nem
                return _raw_tu_ten(KQ(rc, out))
            return _raw_tu_ten(_tra_gia(merge_ref if khoa == "hop" else diff_cay))
        if a[:4] == ["git", "diff", "--no-renames", "--name-only"]:
            return _tra_gia(merge_ref if a[-1] == HOP_GIA else diff_cay)
        if nem is not None:
            raise nem
        return KQ(rc, out)
    return chay


def env_pr(su_kien="pull_request", goc=GOC_A, dau=GOC_B, **them):
    e = {"CI_DUONG_NHANH_SU_KIEN": su_kien, "CI_DUONG_NHANH_GOC": goc, "CI_DUONG_NHANH_DAU": dau,
         "CI_DUONG_NHANH_MERGE": HOP_GIA}
    e.update(them)
    return e


def phan_loai_gia(m, duong, **kw):
    return m.phan_loai(env_pr(), chay_gia(nul(*duong), **kw))


# ---------------------------------------------------------------- tầng 1: hành vi bộ phân loại (đồ giả)
@ca
def t01_toan_ho_so_duong_nhanh():
    m = nap_module()
    for tep in ("ops/land/x.yaml", "ops/leases/y.yaml", "ops/reviews/z/verdict.md", "ops/specs/S.md"):
        che_do, ly_do = phan_loai_gia(m, [tep])
        bang(che_do == "duong_nhanh", f"{tep} phai la duong nhanh, duoc {che_do!r}: {ly_do}")
    che_do, _ = phan_loai_gia(m, ["ops/land/a.yaml", "ops/leases/b.yaml", "ops/reviews/c.md", "ops/specs/d.md"])
    bang(che_do == "duong_nhanh", "bon tien to ho so cung mot PR phai la duong nhanh")


@ca
def t02_co_tep_ma_day_du():
    m = nap_module()
    for ngoai in ("scripts/tl.py", "SKILL.md", "ops/cong_cu.py", "references/API_CONTRACT.md"):
        che_do, ly_do = phan_loai_gia(m, ["ops/leases/y.yaml", ngoai])
        bang(che_do == "day_du", f"lease + {ngoai} phai la day_du, duoc {che_do!r}")
        bang(ngoai in ly_do, f"ly do phai nen ten tep ngoai allowlist: {ly_do!r}")


@ca
def t03_push_va_dispatch_khong_goi_git():
    m = nap_module()
    for su_kien in ("push", "workflow_dispatch", "", "schedule", "PULL_REQUEST", "pull_request_target"):
        log = []
        che_do, ly_do = m.phan_loai(env_pr(su_kien), chay_gia(nul("ops/land/x.yaml"), log=log))
        bang(che_do == "day_du", f"su_kien={su_kien!r} phai la day_du, duoc {che_do!r}")
        bang(not log, f"su_kien={su_kien!r} khong duoc goi git: {log}")
        bang("khong phan loai" in ly_do, f"ly do phai noi khong phan loai: {ly_do!r}")
        bang(m.doc_diff(env_pr(su_kien), chay_gia(nul("ops/land/x.yaml"), log=log)) is None and not log,
             f"doc_diff cho su_kien={su_kien!r} phai la None va khong goi git")
    log = []
    bang(m.phan_loai({}, chay_gia(log=log))[0] == "day_du" and not log, "moi truong rong phai la day_du, khong git")


@ca
def t05_thieu_hoac_hong_sha_day_du():
    m = nap_module()
    tot = nul("ops/land/x.yaml")
    hong = {
        "thieu goc": env_pr(goc=""), "thieu dau": env_pr(dau=""),
        "goc toan 0": env_pr(goc="0" * 40), "dau toan 0": env_pr(dau="0" * 40),
        "goc ngan": env_pr(goc="abc1234"), "dau 41 ky tu": env_pr(dau="b" * 41),
        "goc chu hoa": env_pr(goc="A" * 40), "dau co khoang trang": env_pr(dau=" " + "b" * 39),
        "goc khong phai hex": env_pr(goc="g" * 40), "vang bien": {"CI_DUONG_NHANH_SU_KIEN": "pull_request"},
        # cross-review luot 9: merge ref (`github.sha`) BAT BUOC — vang/hong thi KHONG DO DUOC, khong lui ve mo phong
        "thieu merge ref": env_pr(CI_DUONG_NHANH_MERGE=""), "merge ref toan 0": env_pr(CI_DUONG_NHANH_MERGE="0" * 40),
        "merge ref chu hoa": env_pr(CI_DUONG_NHANH_MERGE="E" * 40), "merge ref ngan": env_pr(CI_DUONG_NHANH_MERGE="e" * 7),
        "merge ref lac dang": env_pr(CI_DUONG_NHANH_MERGE="xyz"),
        "vang bien merge ref": {k: v for k, v in env_pr().items() if k != "CI_DUONG_NHANH_MERGE"},
    }
    for ten, env in hong.items():
        log = []
        che_do, _ = m.phan_loai(env, chay_gia(tot, log=log))
        bang(che_do == "day_du", f"{ten}: phai la day_du (fail-close), duoc {che_do!r}")
        bang(not log, f"{ten}: SHA hong thi khong duoc goi git: {log}")


@ca
def t06_git_loi_hoac_dau_ra_hong_day_du():
    m = nap_module()
    ho_so = nul("ops/land/x.yaml")
    cac = {
        "rc 128 kem dau ra sach": chay_gia(ho_so, rc=128),
        "rc 1": chay_gia(ho_so, rc=1),
        "dau ra cut (thieu NUL cuoi)": chay_gia(b"ops/land/x.yaml"),
        "dau ra khong phai bytes": chay_gia("ops/land/x.yaml\0"),
        "dau ra None": chay_gia(None),
    }
    for ten, chay in cac.items():
        try:
            che_do, _ = m.phan_loai(env_pr(), chay)
        except (TypeError, ValueError, AttributeError) as e:
            # Dau ra lac kieu la CHINH lop loi ma phan_loai phai tu xu ly (fail-close), khong duoc de no ra ngoai.
            raise TinHieuChotCa(f"{ten}: phan_loai ne {type(e).__name__} thay vi fail-close ve day_du: {e}") from e
        bang(che_do == "day_du", f"{ten}: phai la day_du (fail-close), duoc {che_do!r}")
    try:
        che_do, _ = m.phan_loai(env_pr(), chay_gia(nem=SuDoGia("git no")))
    except SuDoGia as e:
        raise TinHieuChotCa(f"git nem ngoai le ma phan loai KHONG bat: {e}") from e
    bang(che_do == "day_du", f"git nem ngoai le: phai la day_du, duoc {che_do!r}")


@ca
def t07_diff_rong_duong_nhanh_co_dong_log_rieng():
    m = nap_module()
    che_do, ly_do = m.phan_loai(env_pr(), chay_gia(b""))
    bang(che_do == "duong_nhanh", f"diff rong (Q3) phai la duong nhanh, duoc {che_do!r}")
    bang("RONG" in ly_do, f"diff rong phai co dong log rieng phan biet: {ly_do!r}")
    _, ly_khac = phan_loai_gia(m, ["ops/land/x.yaml"])
    bang("RONG" not in ly_khac, "dong log cua diff khong rong khong duoc mang chu RONG")


@ca
def t08_doi_workflow_hoac_bo_phan_loai_day_du():
    m = nap_module()
    for ngoai in (".github/workflows/ci.yml", ".github/workflows/x.yml", "ops/ci_duong_nhanh.py",
                  "ops/ci_duong_nhanh_test.py", ".claude/dev/ci_dang_ky_test.py"):
        for tap in ([ngoai], ["ops/land/x.yaml", ngoai]):
            che_do, _ = phan_loai_gia(m, tap)
            bang(che_do == "day_du", f"{tap}: phai la day_du (tep {ngoai} ngoai allowlist), duoc {che_do!r}")


@ca
def t09_ranh_gioi_tien_to():
    m = nap_module()
    for la in ("ops/land_extra.py", "ops/landing/x.yaml", "ops/leases.yaml", "ops/specs", "ops/reviewsX/y.md",
               "ops/speclike/a", "OPS/land/x.yaml", "ops/Land/x.yaml", "xops/land/x.yaml", "ops/land"):
        che_do, _ = phan_loai_gia(m, [la])
        bang(che_do == "day_du", f"{la!r} khong thuoc tien to allowlist, phai la day_du, duoc {che_do!r}")


@ca
def t10a_duong_dan_len_ngoai_day_du():
    m = nap_module()
    bang(phan_loai_gia(m, ["ops/land/../../scripts/tl.py"])[0] == "day_du", "'..' trong duong dan phai la day_du")


@ca
def t10b_thanh_phan_rong_day_du():
    m = nap_module()
    bang(phan_loai_gia(m, ["ops/land//scripts/tl.py"])[0] == "day_du", "thanh phan rong '//' phai la day_du")


@ca
def t10c_thanh_phan_cham_day_du():
    m = nap_module()
    bang(phan_loai_gia(m, ["ops/land/./x.yaml"])[0] == "day_du", "thanh phan '.' phai la day_du")


@ca
def t10d_dau_cheo_nguoc_day_du():
    m = nap_module()
    bang(phan_loai_gia(m, ["ops/land/a\\..\\scripts"])[0] == "day_du", "dau cheo nguoc trong duong dan phai la day_du")


@ca
def t10e_ky_tu_dieu_khien_day_du():
    m = nap_module()
    for tep in ("ops/land/a\nDUONG_NHANH: gia\n.yaml", "ops/land/a\x7f.yaml", "ops/land/a\r.yaml"):
        bang(phan_loai_gia(m, [tep])[0] == "day_du", f"ky tu dieu khien trong {tep!r} phai la day_du")
    che_do, ly_do = phan_loai_gia(m, ["ops/leases/y.yaml", "scripts/a\nDUONG_NHANH: gia.py"])
    bang(che_do == "day_du" and "\n" not in ly_do, f"ly do khong duoc chua xuong dong (gia dong log): {ly_do!r}")


@ca
def t10f_duong_dan_tuyet_doi_day_du():
    m = nap_module()
    bang(phan_loai_gia(m, ["/ops/land/x.yaml"])[0] == "day_du", "duong dan tuyet doi phai la day_du")


# ---------------------------------------------------------------- kho git thật
def _env_git():
    # GITHUB_ACTOR bi loai: `lease_publish.kiem` doi actor thuoc nguoi cap lease; fixture SACH khong duoc do theo ai bam nut CI.
    e = {k: v for k, v in os.environ.items() if not k.startswith("GIT_") and k != "GITHUB_ACTOR"}
    e.update(GIT_CONFIG_GLOBAL=os.devnull, GIT_CONFIG_NOSYSTEM="1", GIT_TERMINAL_PROMPT="0",
             GIT_AUTHOR_NAME="t", GIT_AUTHOR_EMAIL="t@e.x", GIT_COMMITTER_NAME="t", GIT_COMMITTER_EMAIL="t@e.x",
             GIT_CONFIG_COUNT="1", GIT_CONFIG_KEY_0="core.symlinks", GIT_CONFIG_VALUE_0="true")
    return e


def git(kho, *doi, kiem=True):
    r = subprocess.run(["git", "-c", "commit.gpgsign=false", "-c", "core.autocrlf=false",
                        "-c", "core.symlinks=true", *doi],
                       cwd=kho, capture_output=True, env=_env_git())
    if kiem and r.returncode:
        raise RuntimeError(f"ha tang: git {' '.join(doi)} rc={r.returncode}: {r.stderr.decode('utf-8', 'replace')[:300]}")
    return r


def _symlink(link, target, target_is_directory=False):
    """Tao symlink di dong."""
    p = Path(link)
    p.parent.mkdir(parents=True, exist_ok=True)
    if sys.platform == "win32":
        tgt = str(target).replace("/", "\\")
        p.symlink_to(tgt, target_is_directory=target_is_directory)
    else:
        p.symlink_to(target, target_is_directory=target_is_directory)


def chay_that(argv, **kw):
    kw.setdefault("env", _env_git())
    return subprocess.run(argv, **kw)


def viet(kho, duong, noi_dung):
    tep = Path(kho) / duong
    tep.parent.mkdir(parents=True, exist_ok=True)
    tep.write_bytes(noi_dung if isinstance(noi_dung, bytes) else noi_dung.encode("utf-8"))


@contextlib.contextmanager
def kho_that(nen=None, nhanh_pr=None, nen_tien=None, sao_lease_publish=False):
    """Dựng kho: commit A (nền) → nhánh `pr` (H) → `main` tiến thêm (B). Trả (kho, goc=B hoặc A, dau=H)."""
    tam = tempfile.mkdtemp(prefix="cdn_kho_")
    kho = Path(tam) / "kho"
    kho.mkdir()
    try:
        git(kho, "init", "-q", "-b", "main")
        for d, nd in (nen or {"README.md": "x\n"}).items():
            viet(kho, d, nd)
        if sao_lease_publish:
            (kho / "ops").mkdir(exist_ok=True)
            shutil.copyfile(ROOT_THAT / "ops" / "lease_publish.py", kho / "ops" / "lease_publish.py")
        git(kho, "add", "-A")
        git(kho, "commit", "-q", "-m", "nen")
        a = git(kho, "rev-parse", "HEAD").stdout.decode().strip()
        git(kho, "checkout", "-q", "-b", "pr")
        for d, nd in (nhanh_pr or {}).items():
            if nd is None:
                git(kho, "rm", "-q", "-f", d)
            elif isinstance(nd, tuple):
                (kho / d).parent.mkdir(parents=True, exist_ok=True)
                git(kho, "mv", nd[0], d)
            else:
                viet(kho, d, nd)
        git(kho, "add", "-A")
        git(kho, "commit", "-q", "--allow-empty", "-m", "pr")
        h = git(kho, "rev-parse", "HEAD").stdout.decode().strip()
        b = a
        if nen_tien:
            git(kho, "checkout", "-q", "main")
            for d, nd in nen_tien.items():
                viet(kho, d, nd)
            git(kho, "add", "-A")
            git(kho, "commit", "-q", "-m", "main tien")
            b = git(kho, "rev-parse", "HEAD").stdout.decode().strip()
            git(kho, "checkout", "-q", "pr")
        yield kho, b, h
    finally:
        shutil.rmtree(tam, ignore_errors=True)


def merge_ref_that(kho, goc, dau):
    """Commit merge mo phong merge ref (cha THU NHAT = goc, cha THU HAI = dau; thu tu cha cua GitHub chua tu do) dung tu cay
    `merge-tree` cua CAY LAM VIEC hien tai — ke ca khi xung dot (theo tai lieu GitHub PR xung dot khong chay workflow
    `pull_request`, chua tu do; phan loai tu fail-close o merge-tree). Khong dung duoc
    (thieu object) => SHA khong ton tai (phan loai phai tu KHONG DO DUOC)."""
    mt = git(kho, "merge-tree", "--write-tree", "--no-messages", goc, dau, kiem=False)
    cay = mt.stdout.decode("ascii", "replace").split("\n", 1)[0].strip()
    if not re.fullmatch(r"[0-9a-f]{40}", cay):
        return "f" * 40
    return git(kho, "commit-tree", cay, "-p", goc, "-p", dau, "-m", "merge ref").stdout.decode().strip()


def phan_loai_that(m, kho, goc, dau, hop=None):
    return m.phan_loai(env_pr(goc=goc, dau=dau, CI_DUONG_NHANH_MERGE=hop or merge_ref_that(kho, goc, dau)), chay_that, kho)


@ca
def t11_ba_cham_khong_tinh_nhanh_dich_da_tien():
    m = nap_module()
    with kho_that(nhanh_pr={"ops/land/x.yaml": "a: 1\n"}, nen_tien={"scripts/y.py": "print(1)\n"}) as (kho, goc, dau):
        hai_cham = git(kho, "diff", "--name-only", "-z", f"{goc}..{dau}").stdout.decode().split("\0")
        bang("scripts/y.py" in hai_cham,
             f"fixture vo hieu: base..head phai chua scripts/y.py (chung minh hai cham SAI), duoc {hai_cham}")
        che_do, ly_do = phan_loai_that(m, kho, goc, dau)
        bang(che_do == "duong_nhanh", f"base...head phai bo qua thay doi cua nhanh dich, duoc {che_do!r}: {ly_do}")


@ca
def t11b_nhieu_merge_base_la_khong_do_duoc():
    """Cross-review luot 8 (`phan-loai-ba-cham-mu-voi-nhieu-merge-base`): criss-cross => ba cham giau thay doi ma."""
    m = nap_module()
    ho_so = nul("ops/land/x.yaml")
    for ten, mb in (("hai merge-base", f"{GOC_A}\n{GOC_B}\n".encode()), ("khong merge-base", b""),
                    ("merge-base nem", SuDoGia("git no")), ("merge-base lac dang", b"xyz\n"),
                    ("merge-base rc=1 ma dau ra dung dang", (1, (GOC_A + "\n").encode()))):
        try:
            che_do = m.phan_loai(env_pr(), chay_gia(ho_so, merge_base=mb))[0]
        except SuDoGia as e:
            raise TinHieuChotCa(f"{ten}: merge-base nem ma phan loai KHONG bat: {e}") from e
        bang(che_do == "day_du", f"{ten}: phai la day_du (fail-close), duoc {che_do!r}")
    bang(m.phan_loai(env_pr(), chay_gia(ho_so))[0] == "duong_nhanh", "doi chung: mot merge-base + ho so phai duong nhanh")
    with kho_that(nhanh_pr={"ops/land/x1.yaml": "a: 1\n"}, nen={"README.md": "x\n", "scripts/tl.py": "v1\n"}) as (kho, a, x1):
        git(kho, "checkout", "-q", "main")
        viet(kho, "scripts/tl.py", "v2\n")
        git(kho, "commit", "-q", "-am", "m1")
        m1 = git(kho, "rev-parse", "HEAD").stdout.decode().strip()
        git(kho, "merge", "-q", "--no-ff", x1, "-m", "m2")
        goc = git(kho, "rev-parse", "HEAD").stdout.decode().strip()
        git(kho, "checkout", "-q", "pr")
        git(kho, "merge", "-q", "--no-ff", m1, "-m", "x2")
        viet(kho, "scripts/tl.py", "v1\n")
        viet(kho, "ops/land/y.yaml", "b: 1\n")
        git(kho, "add", "-A")
        git(kho, "commit", "-q", "-m", "x3 dao ma + ho so")
        dau = git(kho, "rev-parse", "HEAD").stdout.decode().strip()
        bang(len(git(kho, "merge-base", "--all", goc, dau).stdout.split()) == 2, "fixture vo hieu: phai co hai merge-base")
        git(kho, "checkout", "-q", "--detach", goc)
        git(kho, "merge", "-q", "--no-ff", dau, "-m", "merge that")
        doi_that = git(kho, "diff", "--name-only", goc, "HEAD").stdout.decode().split()
        bang("scripts/tl.py" in doi_that, f"fixture vo hieu: merge that phai doi scripts/tl.py, duoc {doi_that}")
        che_do, ly_do = phan_loai_that(m, kho, goc, dau)
        bang(che_do == "day_du", f"criss-cross (merge that doi scripts/tl.py) phai la day_du, duoc {che_do!r}: {ly_do}")


def _kho_doi_ten_phia_goc(kho, cu, moi):
    """Nhanh `main` (goc) doi ten `cu` -> `moi` SAU khi PR re ra; tra SHA goc moi."""
    git(kho, "checkout", "-q", "main")
    (kho / moi).parent.mkdir(parents=True, exist_ok=True)
    git(kho, "mv", cu, moi)
    git(kho, "commit", "-q", "-m", "goc doi ten")
    goc = git(kho, "rev-parse", "HEAD").stdout.decode().strip()
    git(kho, "checkout", "-q", "pr")
    return goc


def _doi_khi_merge_that(kho, goc, dau):
    cay = git(kho, "merge-tree", "--write-tree", "--no-messages", goc, dau).stdout.decode().strip()
    return set(git(kho, "diff", "--name-only", "-z", "--no-renames", goc, cay).stdout.decode().split("\0")) - {""}


@ca
def t11c_goc_doi_ten_ho_so_ra_vung_ma_day_du():
    """Luot 9 (lop `phan-loai-ba-cham-mu-voi-nhieu-merge-base`, duong vao thu hai: MOT merge-base van noi doi): nhanh
    goc doi ten tep/thu muc ho so ra vung ma; PR sua tep ho so => merge that (ort, do doi ten) SUA tep trong vung ma,
    ba cham chi thay duong dan ho so. Phai la day_du. Kem cac cua fail-close cua `doc_diff_merge` (do gia)."""
    m = nap_module()
    dong = "".join(f"dong {i}\n" for i in range(20))
    # (a) doi ten TEP phia goc
    with kho_that(nen={"README.md": "x\n", "ops/land/f.md": dong},
                  nhanh_pr={"ops/land/f.md": dong.replace("dong 5", "dong NAM")}) as (kho, _a, dau):
        goc = _kho_doi_ten_phia_goc(kho, "ops/land/f.md", "scripts/f.py")
        bang(len(git(kho, "merge-base", "--all", goc, dau).stdout.split()) == 1, "fixture vo hieu: phai MOT merge-base")
        ba_cham = set(git(kho, "diff", "--name-only", "-z", "--no-renames", f"{goc}...{dau}").stdout.decode().split("\0")) - {""}
        bang(ba_cham == {"ops/land/f.md"}, f"fixture vo hieu: ba cham phai chi thay ho so, duoc {ba_cham}")
        bang("scripts/f.py" in _doi_khi_merge_that(kho, goc, dau), "fixture vo hieu: merge that phai SUA scripts/f.py")
        che_do, ly_do = phan_loai_that(m, kho, goc, dau)
        bang(che_do == "day_du" and "scripts/f.py" in ly_do, f"goc doi ten tep ho so ra vung ma: phai day_du, duoc {che_do!r}: {ly_do}")
    # (b) doi ten THU MUC phia goc: ort mac dinh (`merge.directoryRenames=conflict`) bao XUNG DOT (rc=1) — theo tai lieu
    # GitHub (chua tu do) PR xung dot khong chay workflow `pull_request`, nen day khong phai duong lot;
    # van phai la day_du (git THAT, khong do gia).
    nen = {"README.md": "x\n", **{f"ops/land/{t}.md": f"{t} noi dung dai dong mot\n" for t in "abc"}}
    with kho_that(nen=nen, nhanh_pr={"ops/land/moi.md": "moi\n"}) as (kho, _a, dau):
        git(kho, "checkout", "-q", "main")
        (kho / "scripts").mkdir(exist_ok=True)
        git(kho, "mv", "ops/land", "scripts/land")
        git(kho, "commit", "-q", "-m", "goc doi ten thu muc")
        goc = git(kho, "rev-parse", "HEAD").stdout.decode().strip()
        git(kho, "checkout", "-q", "pr")
        mt = git(kho, "merge-tree", "--write-tree", "--no-messages", goc, dau, kiem=False)
        bang(mt.returncode == 1 and b"scripts/land/moi.md" in mt.stdout,
             f"fixture vo hieu: doi ten thu muc phai la XUNG DOT dua tep moi vao scripts/land/, rc={mt.returncode}")
        che_do, ly_do = phan_loai_that(m, kho, goc, dau)
        bang(che_do == "day_du", f"goc doi ten thu muc ho so (merge xung dot): phai day_du, duoc {che_do!r}: {ly_do}")
    # (c) cua fail-close cua doc_diff_merge (do gia); doi chung mac dinh la duong nhanh
    ho_so = nul("ops/land/x.yaml")
    bang(m.phan_loai(env_pr(), chay_gia(ho_so))[0] == "duong_nhanh", "doi chung: merge sach + ho so phai duong nhanh")
    cac = {
        "merge doi tep ma": dict(diff_cay=nul("ops/land/x.yaml", "scripts/f.py")),
        "merge-tree xung dot rc=1": dict(merge_tree=(1, (CAY_GIA + "\n").encode())),
        "merge-tree nem": dict(merge_tree=SuDoGia("git no")),
        "merge-tree lac dang": dict(merge_tree=b"xyz\n"),
        "diff cay rc=128": dict(diff_cay=(128, b"")),
        "diff cay nem": dict(diff_cay=SuDoGia("git no")),
        "diff cay cut": dict(diff_cay=(0, b"ops/land/x.yaml\0ops/land/y")),
    }
    for ten, kw in cac.items():
        try:
            che_do = m.phan_loai(env_pr(), chay_gia(ho_so, **kw))[0]
        except SuDoGia as e:
            raise TinHieuChotCa(f"{ten}: git nem ma phan loai KHONG bat: {e}") from e
        bang(che_do == "day_du", f"{ten}: phai la day_du (fail-close), duoc {che_do!r}")


@ca
def t11d_merge_ref_that_dung_base_moi_hon_day_du():
    """Cross-review luot 9 (`phan-loai-khong-neo-merge-ref-that`): merge-tree mo phong tu `pull_request.base.sha`; commit GitHub
    test THAT (`github.sha`) co the dung tren dau nhanh dich MOI hon (chua tu do tren GitHub; ca nay dung kho that). Nhanh dich doi ten tep ho so ra vung ma SAU base.sha
    => merge that sua ma => phai `day_du`. Kem cac cua fail-close cua diff `goc -> merge ref` (do gia)."""
    m = nap_module()
    dong = "".join(f"dong {i}\n" for i in range(20))
    with kho_that(nen={"README.md": "x\n", "ops/land/f.md": dong},
                  nhanh_pr={"ops/land/f.md": dong.replace("dong 5", "dong NAM")}) as (kho, goc_cu, dau):
        goc_moi = _kho_doi_ten_phia_goc(kho, "ops/land/f.md", "scripts/f.py")
        git(kho, "checkout", "-q", "--detach", goc_moi)
        git(kho, "merge", "-q", "--no-ff", dau, "-m", "merge ref")
        hop = git(kho, "rev-parse", "HEAD").stdout.decode().strip()
        git(kho, "checkout", "-q", "pr")
        bang("scripts/f.py" in set(git(kho, "diff", "--name-only", f"{hop}^1", hop).stdout.decode().split()),
             "fixture vo hieu: merge that phai SUA scripts/f.py")
        bang(phan_loai_that(m, kho, goc_cu, dau)[0] == "duong_nhanh",
             "fixture vo hieu: merge ref dung tren base.sha cu phai cho duong nhanh (khong thi ca nay khong do gi)")
        che_do, ly_do = phan_loai_that(m, kho, goc_cu, dau, hop)
        bang(che_do == "day_du" and "scripts/f.py" in ly_do, f"merge ref that sua ma: phai day_du, duoc {che_do!r}: {ly_do}")
    ho_so = nul("ops/land/x.yaml")
    bang(m.phan_loai(env_pr(), chay_gia(ho_so))[0] == "duong_nhanh", "doi chung: merge ref khong doi them => duong nhanh")
    cac = {
        "merge ref doi tep ma": dict(merge_ref=nul("ops/land/x.yaml", "scripts/f.py")),
        "merge ref rc=128": dict(merge_ref=(128, b"")),
        "merge ref nem": dict(merge_ref=SuDoGia("git no")),
        "merge ref cut": dict(merge_ref=(0, b"ops/land/x.yaml\0ops/land/y")),
    }
    for ten, kw in cac.items():
        try:
            che_do = m.phan_loai(env_pr(), chay_gia(ho_so, **kw))[0]
        except SuDoGia as e:
            raise TinHieuChotCa(f"{ten}: git nem ma phan loai KHONG bat: {e}") from e
        bang(che_do == "day_du", f"{ten}: phai la day_du (fail-close), duoc {che_do!r}")


@ca
def t11e_thuoc_tinh_cua_pr_khong_cau_hinh_duoc_merge_tree():
    """Lop `kiem-re-bi-cau-hinh-boi-du-lieu-ho-so`, cua `merge-tree` (tu do khi va luot 9): PR mang `ops/land/.gitattributes`
    `* -diff`; tep hien co duoi `ops/land/d/` la CRLF, nhanh goc doi ten thu muc ra `scripts/d/` va doi sang LF. Doc thuoc
    tinh cay lam viec thi phep do doi ten tinh bam kieu NHI PHAN => mat doi ten thu muc => merge XUNG DOT thanh merge
    SACH, tep moi cua PR o lai `ops/land/d/` => duong nhanh. Thuoc tinh GOC => xung dot => `day_du`."""
    m = nap_module()
    crlf = {f"ops/land/d/{t}.md": "".join(f"{t} dong so {i} noi dung kha dai de dem\r\n" for i in range(30)).encode()
            for t in "abc"}
    pr = {"ops/land/d/moi.md": "moi\n", "ops/land/.gitattributes": "* -diff\n"}
    with kho_that(nen={"README.md": "x\n", **crlf}, nhanh_pr=pr) as (kho, _a, dau):
        git(kho, "checkout", "-q", "main")
        (kho / "scripts").mkdir(exist_ok=True)
        git(kho, "mv", "ops/land/d", "scripts/d")
        for t in "abc":
            tep = kho / "scripts" / "d" / f"{t}.md"
            tep.write_bytes(tep.read_bytes().replace(b"\r\n", b"\n"))
        git(kho, "add", "-A")
        git(kho, "commit", "-q", "-m", "goc doi ten thu muc + LF")
        goc = git(kho, "rev-parse", "HEAD").stdout.decode().strip()
        git(kho, "checkout", "-q", "pr")
        cay_lam_viec = git(kho, "merge-tree", "--write-tree", "--no-messages", goc, dau, kiem=False)
        bang(cay_lam_viec.returncode == 0,
             f"fixture vo hieu: thuoc tinh cay lam viec (PR) phai lam merge SACH, rc={cay_lam_viec.returncode}")
        bang(git(kho, f"--attr-source={goc}", "merge-tree", "--write-tree", "--no-messages", goc, dau, kiem=False).returncode == 1,
             "fixture vo hieu: thuoc tinh GOC phai cho merge XUNG DOT (doi ten thu muc dua tep moi vao scripts/d/)")
        che_do, ly_do = phan_loai_that(m, kho, goc, dau)
        bang(che_do == "day_du", f"thuoc tinh cua PR khong duoc bien merge xung dot thanh duong nhanh: {che_do!r}: {ly_do}")


@ca
def t12_doi_ten_ra_khoi_vung_ma_day_du():
    m = nap_module()
    noi = "def f():\n    return 1\n" * 20
    with kho_that(nen={"scripts/tl.py": noi}, nhanh_pr={"ops/land/tl.py": ("scripts/tl.py",)}) as (kho, goc, dau):
        co_rename = git(kho, "diff", "--name-only", "-z", f"{goc}...{dau}").stdout.decode().split("\0")
        bang("scripts/tl.py" not in co_rename,
             f"fixture vo hieu: phat hien doi ten phai giau duong dan cu, duoc {co_rename}")
        che_do, ly_do = phan_loai_that(m, kho, goc, dau)
        bang(che_do == "day_du", f"doi ten scripts/tl.py -> ops/land/ phai la day_du, duoc {che_do!r}: {ly_do}")

    # Luot 9: `doc_diff_merge` cung bat duong that o tren (diff goc -> cay merge co `--no-renames`), nen ca that KHONG
    # con do rieng `--no-renames` cua BA CHAM. Do gia mo phong dung ngu nghia vua chung minh bang fixture: thieu co thi
    # git chi in duong dan DICH; merge (gia) khong doi them gi — chi ba cham quyet dinh.
    def chay_doi_ten(argv, **kw):
        argv = bo_attr_source(argv)
        if argv[:3] == ["git", "merge-base", "--all"]:
            return KQ(0, (GOC_A + "\n").encode())
        if argv[:3] == ["git", "merge-tree", "--write-tree"]:
            return KQ(0, (CAY_GIA + "\n").encode())
        if argv[:4] == ["git", "diff", "--no-renames", "--name-only"]:
            return KQ(0, b"")
        return KQ(0, nul("ops/land/tl.py", "scripts/tl.py") if "--no-renames" in argv else nul("ops/land/tl.py"))
    che_do, ly_do = m.phan_loai(env_pr(), chay_doi_ten)
    bang(che_do == "day_du", f"ba cham PHAI tu tat do doi ten (khong dua vao merge): duoc {che_do!r}: {ly_do}")


@ca
def t13_ten_tep_co_dau_van_duong_nhanh():
    m = nap_module()
    with kho_that(nhanh_pr={"ops/land/tệp-có-dấu.yaml": "a: 1\n", "ops/reviews/bản ghi 1.md": "x\n"}) as (kho, goc, dau):
        che_do, ly_do = phan_loai_that(m, kho, goc, dau)
        bang(che_do == "duong_nhanh", f"ten tep co dau/khoang trang trong allowlist phai la duong nhanh: {che_do!r} {ly_do}")


@ca
def t14_hoso_lan_ma_that_va_xoa_tep():
    m = nap_module()
    with kho_that(nen={"scripts/a.py": "x\n", "ops/land/old.yaml": "a: 1\n"},
                  nhanh_pr={"ops/land/old.yaml": None, "ops/specs/S.md": "s\n"}) as (kho, goc, dau):
        bang(phan_loai_that(m, kho, goc, dau)[0] == "duong_nhanh", "xoa tep ho so + them spec phai la duong nhanh")
    with kho_that(nen={"scripts/a.py": "x\n"}, nhanh_pr={"scripts/a.py": None, "ops/specs/S.md": "s\n"}) as (kho, goc, dau):
        bang(phan_loai_that(m, kho, goc, dau)[0] == "day_du", "XOA tep ma (scripts/a.py) phai la day_du")


@ca
def t15_thieu_object_day_du():
    m = nap_module()
    with kho_that(nhanh_pr={"ops/land/x.yaml": "a: 1\n"}) as (kho, _, dau):
        che_do, _ = phan_loai_that(m, kho, "c" * 40, dau)
        bang(che_do == "day_du", f"SHA dung dinh dang nhung khong co object phai la day_du, duoc {che_do!r}")
    che_do, _ = m.phan_loai(env_pr(), chay_that, Path(tempfile.gettempdir()) / "khong-ton-tai-cdn")
    bang(che_do == "day_du", "thu muc kho khong ton tai phai la day_du")


@ca
def t16_main_ghi_output_dung_che_do():
    m = nap_module()
    tam = Path(tempfile.mkdtemp(prefix="cdn_out_"))
    try:
        for ten, env, chay, mong in (
            ("hoso", env_pr(), chay_gia(nul("ops/land/x.yaml")), "duong_nhanh"),
            ("ma", env_pr(), chay_gia(nul("scripts/tl.py")), "day_du"),
            ("push", env_pr("push"), chay_gia(nul("ops/land/x.yaml")), "day_du"),
        ):
            ra = tam / f"out_{ten}.txt"
            ra.write_text("da co\n", encoding="utf-8")
            env = dict(env, GITHUB_OUTPUT=str(ra))
            bo_dem = tempfile.TemporaryFile("w+", encoding="utf-8")
            rc = m.main([], env, chay, ROOT_THAT, bo_dem)
            bo_dem.seek(0)
            log = bo_dem.read()
            bang(rc == 0, f"{ten}: main phai thoat 0, duoc {rc}")
            bang(ra.read_text(encoding="utf-8") == f"da co\nche_do={mong}\n", f"{ten}: GITHUB_OUTPUT sai: {ra.read_text()!r}")
            bang("DUONG_NHANH" in log, f"{ten}: log phai co dong DUONG_NHANH: {log!r}")
    finally:
        shutil.rmtree(tam, ignore_errors=True)


class EnvNemKhiDocSuKien(dict):
    def get(self, khoa, mac_dinh=None):
        if khoa == "CI_DUONG_NHANH_SU_KIEN":
            raise SuDoGia("loi noi bo gia")
        return super().get(khoa, mac_dinh)


@ca
def t17_main_loi_noi_bo_fail_close():
    m = nap_module()
    tam = Path(tempfile.mkdtemp(prefix="cdn_out_"))
    try:
        ra = tam / "out.txt"
        env = EnvNemKhiDocSuKien(GITHUB_OUTPUT=str(ra))
        bo_dem = tempfile.TemporaryFile("w+", encoding="utf-8")
        try:
            rc = m.main([], env, chay_gia(nul("ops/land/x.yaml")), ROOT_THAT, bo_dem)
        except SuDoGia as e:
            raise TinHieuChotCa(f"loi noi bo cua phan loai lot ra ngoai main (main phai fail-close ve day_du): {e}") from e
        bang(rc == 0, f"loi noi bo: main van phai thoat 0 (khong lam PR do oan), duoc {rc}")
        bang(ra.read_text(encoding="utf-8") == "che_do=day_du\n", f"loi noi bo phai ghi day_du: {ra.read_text()!r}")
    finally:
        shutil.rmtree(tam, ignore_errors=True)


@ca
def t18_main_khong_ghi_duoc_output_thi_do():
    m = nap_module()
    tam = Path(tempfile.mkdtemp(prefix="cdn_out_"))
    try:
        bo_dem = tempfile.TemporaryFile("w+", encoding="utf-8")
        rc = m.main([], env_pr(GITHUB_OUTPUT=str(tam)), chay_gia(nul("ops/land/x.yaml")), ROOT_THAT, bo_dem)
        bang(rc == 1, f"khong ghi duoc GITHUB_OUTPUT (la thu muc) phai thoat 1, duoc {rc}")
        bang(m.main(["la"], env_pr(), chay_gia(), ROOT_THAT, bo_dem) == 2, "doi so la phai thoat 2")
    finally:
        shutil.rmtree(tam, ignore_errors=True)


# ---------------------------------------------------------------- `kiem-re`
CA_DU_LIEU_GOI: list = []


def chay_that_bo_ca_du_lieu(argv, **kw):
    """Kho tam trong ca kiem-re khong co lease_publish_test.py: chi CHAN dung lenh ca-du-lieu (ghi lai), con lai chay that."""
    if "ops/lease_publish_test.py" in argv:
        CA_DU_LIEU_GOI.append(list(argv))
        return KQ(0, b"DAT\n")
    return chay_that(argv, **kw)


def kiem_re(m, kho, goc, dau, bay_gio=None):
    bo_dem = tempfile.TemporaryFile("w+", encoding="utf-8")
    CA_DU_LIEU_GOI.clear()
    env = env_pr(goc=goc, dau=dau, CI_DUONG_NHANH_MERGE=merge_ref_that(kho, goc, dau))
    rc = m.lenh_kiem_re(env, chay_that_bo_ca_du_lieu, kho, bo_dem, bay_gio)
    bo_dem.seek(0)
    return rc, bo_dem.read()


LEASE_HET_HAN = "lease_id: cu\nlease_expires_at_utc: '2020-01-01T00:00:00Z'\nghi_chu: chi de doc\n"   # THIEU truong bat buoc: KHONG hop le


def lease_that_het_han_hop_le():
    """Nguyên văn một lease THẬT đã hết hạn, không neo prompt, không bia mộ, và qua `kiem(bo_qua_han=True)` trong kho."""
    sys.path.insert(0, str(ROOT_THAT / "ops"))
    import lease_publish as lp
    for tep in sorted((ROOT_THAT / "ops" / "leases").glob("*.yaml")):
        vb = tep.read_text(encoding="utf-8")
        if any(k in vb for k in ("prompt_path", "prompt_sha256_required", "thay_the_cho", "da_bi_thay_the")):
            continue
        try:
            with mock.patch.dict(os.environ, {k: v for k, v in os.environ.items() if k != "GITHUB_ACTOR"}, clear=True):
                lp.kiem(lp._doc_yaml(str(tep)), str(tep), str(ROOT_THAT), bo_qua_han=True)
                lp.kiem(lp._doc_yaml(str(tep)), str(tep), str(ROOT_THAT))
        except lp.Chan as e:
            if "het han" in str(e) or "hết hạn" in str(e):
                return vb
        except Exception:
            continue
    raise KhongCoFixture("khong tim thay lease that het han hop le de lam fixture")
LEASE_CON_HAN_THIEU = "schema_version: 2\nlease_id: moi\nlease_expires_at_utc: '2099-01-01T00:00:00Z'\n"


def _kiem_re_gia(m, env, chay):
    bo_dem = tempfile.TemporaryFile("w+", encoding="utf-8")
    return m.lenh_kiem_re(env, chay, ROOT_THAT, bo_dem)


@ca
def t19a_kiem_re_co_tep_ma_thi_do():
    """Phan loai lai o kiem-re khong ra DUONG_NHANH (co tep ma) thi PHAI do — neu khong, kiem-re la 'DAT' gia."""
    m = nap_module()
    rc = _kiem_re_gia(m, env_pr(), chay_gia(nul("scripts/tl.py")))
    bang(rc == 1, f"co tep ma: kiem-re khong khop chuan-bi phai DO (rc=1), duoc {rc}")


@ca
def t19b_kiem_re_khong_do_duoc_thi_do():
    m = nap_module()
    for ten, env in (("push", env_pr("push")), ("thieu sha", env_pr(goc=""))):
        rc = _kiem_re_gia(m, env, chay_gia(nul("ops/land/x.yaml")))
        bang(rc == 1, f"{ten}: kiem-re khong do duoc diff phai DO (rc=1), duoc {rc}")


@ca
def t20a_kiem_re_ho_so_sach_dat():
    m = nap_module()
    pr = {"ops/land/x.yaml": "a: 1\nb: [1, 2]\n", "ops/leases/cu.yaml": lease_that_het_han_hop_le(), "ops/specs/S.md": "# s\n"}
    with kho_that(nhanh_pr=pr, sao_lease_publish=True) as (kho, goc, dau):
        rc, log = kiem_re(m, kho, goc, dau)
        bang(rc == 0, f"ho so sach (lease het han HOP LE) phai DAT, duoc rc={rc}: {log}")
        bang("da het han" in log, f"lease het han phai in dong giai thich: {log}")
        bang("kiem-re DAT" in log, f"phai in dong tong ket DAT: {log}")
        bang(len(CA_DU_LIEU_GOI) == 1, f"kiem-re phai chay ba ca du lieu DUNG MOT lan, thay {len(CA_DU_LIEU_GOI)}")


@ca
def t20b_kiem_re_yaml_hong_do():
    m = nap_module()
    with kho_that(nhanh_pr={"ops/land/hong.yaml": "a: [1, 2\nb: : :\n"}) as (kho, goc, dau):
        rc, log = kiem_re(m, kho, goc, dau)
        bang(rc == 1 and "YAML khong parse duoc" in log, f"YAML hong phai DO, duoc rc={rc}: {log}")


@ca
def t20c_kiem_re_dau_xung_dot_do():
    m = nap_module()
    with kho_that(nhanh_pr={"ops/specs/X.md": "a\n<<<<<<< HEAD\nb\n=======\nc\n>>>>>>> nhanh\n"}) as (kho, goc, dau):
        rc, log = kiem_re(m, kho, goc, dau)
        bang(rc == 1 and "diff --check" in log, f"dau xung dot con sot phai DO, duoc rc={rc}: {log}")


@ca
def t20d_kiem_re_khoang_trang_cuoi_dong_khong_do():
    m = nap_module()
    pr = {"ops/reviews/v-verdict.md": "dong co khoang trang cuoi   \nsau\n",
          "ops/reviews/goi-y.patch": "@@ -1 +1 @@\n-a  \n+b \n \n",
          "ops/reviews/tab.md": "a\n \tb\n",
          "ops/leases/thua-dong.yaml": lease_that_het_han_hop_le() + "\n"}
    with kho_that(nhanh_pr=pr, sao_lease_publish=True) as (kho, goc, dau):
        tho = git(kho, "diff", "--check", f"{goc}...{dau}", kiem=False)
        bang(tho.returncode != 0, "fixture vo hieu: `git diff --check` nguyen ban phai bat cac tep nay")
        # D1 duyet DUNG ba loai; moi loai mot tep, moi tep phai tu no lam `--check` tho do (khong thi loai ay mat chot).
        for tep, loai in (("ops/reviews/v-verdict.md", "blank-at-eol"), ("ops/leases/thua-dong.yaml", "blank-at-eof"),
                          ("ops/reviews/tab.md", "space-before-tab")):
            chi_loai = git(kho, "-c", "core.whitespace=-" + ",-".join(
                x for x in ("blank-at-eol", "blank-at-eof", "space-before-tab") if x != loai),
                "diff", "--check", f"{goc}...{dau}", "--", tep, kiem=False)
            bang(chi_loai.returncode != 0, f"fixture vo hieu: {tep} phai do DUNG loai {loai} khi chi loai ay bat")
        rc, log = kiem_re(m, kho, goc, dau)
        bang(rc == 0, f"khoang trang cuoi dong / dong trong cuoi tep khong duoc chan oan (lop PR ma D1 sinh ra de giai, xem docstring ci_duong_nhanh.py): rc={rc}: {log}")


@ca
def t20e_kiem_re_lease_con_han_loi_do():
    m = nap_module()
    with kho_that(nhanh_pr={"ops/leases/moi.yaml": LEASE_CON_HAN_THIEU}, sao_lease_publish=True,
                  nen={"README.md": "x\n"}) as (kho, goc, dau):
        rc, log = kiem_re(m, kho, goc, dau)
        bang(rc == 1 and "kiem lease rc=" in log and "het han" not in log.split("kiem lease rc=")[0].splitlines()[-1], f"lease CON HAN thieu truong phai DO qua check: rc={rc}: {log}")


@ca
def t20f_kiem_re_lease_het_han_sai_schema_van_do():
    """Cross-review luot 1 (P2): het han KHONG duoc mien kiem. Lease het han thieu truong bat buoc phai DO."""
    m = nap_module()
    with kho_that(nhanh_pr={"ops/leases/cu.yaml": LEASE_HET_HAN}, sao_lease_publish=True) as (kho, goc, dau):
        rc, log = kiem_re(m, kho, goc, dau)
        bang(rc == 1 and "het han" in log and "CHAN" in log, f"lease HET HAN thieu truong phai DO qua kiem(bo_qua_han): rc={rc}: {log}")


@ca
def t20g_kiem_re_lease_duoi_yml_van_duoc_kiem():
    m = nap_module()
    for ten, vb in (("con-han", LEASE_CON_HAN_THIEU), ("het-han", LEASE_HET_HAN)):
        with kho_that(nhanh_pr={f"ops/leases/{ten}.yml": vb}, sao_lease_publish=True) as (kho, goc, dau):
            rc, log = kiem_re(m, kho, goc, dau)
            bang(rc == 1, f"lease `.yml` {ten} thieu truong phai DO (cung doi xu voi `.yaml`): rc={rc}: {log}")


@ca
def t20n_kiem_re_symlink_ho_so_do():
    """Cross-review luot 7 (P2 `buoc-bi-bo-doc-ca-cay`): symlink treo duoi allowlist DAT o kiem-re cu nhung lam `t82`
    (lease-publish selftest, bi bo o duong nhanh) DO tren master. Doi chung: cung PR khong symlink phai DAT."""
    m = nap_module()
    with kho_that(nhanh_pr={"ops/specs/S.md": "# s\n"}) as (kho, goc, dau):
        rc0, log0 = kiem_re(m, kho, goc, dau)
        bang(rc0 == 0, f"doi chung khong symlink phai DAT: rc={rc0}: {log0}")
        (kho / "ops" / "specs" / "treo.md").symlink_to("khong-ton-tai")
        git(kho, "add", "-A")
        git(kho, "commit", "-q", "-m", "symlink")
        dau2 = git(kho, "rev-parse", "HEAD").stdout.decode().strip()
        rc, log = kiem_re(m, kho, goc, dau2)
        # Chuoi RIENG cua `kiem_loai_tep`: `kiem_symlink_treo_ca_cay` cung bat symlink treo nay ("symlink TREO trong cay") nen
        # chi doi "symlink" thi chot ca cay CHE mat dot bien go `kiem_loai_tep` (luot 8b, HINT F2).
        bang(rc == 1 and "tep ho so la symlink" in log and "treo.md" in log, f"symlink ho so phai DO kiem-re: rc={rc}: {log}")


@ca
def t20p_kiem_re_gitattributes_trong_ho_so_khong_cau_hinh_duoc_diff_check():
    """Cross-review luot 8 (`kiem-re-bi-cau-hinh-boi-du-lieu-ho-so`): `.gitattributes` do PR mang vao (moi do sau) voi
    `conflict-marker-size` tat bao dau xung dot cua `diff --check` doc thuoc tinh tu cay lam viec. Chot: `--attr-source`
    = cay GOC; `binary` va `-diff` tat duoc y het (do 01-10-2026) nen moi thuoc tinh mot vong. Doi chung: KHONG chan
    `.gitattributes` — PR ho so co them tep nhu the duoi `ops/reviews/` (`-whitespace`: PR #667 merge 3fee59e, PR #670
    merge dcd5fe0)."""
    m = nap_module()
    xung_dot = "a\n<<<<<<< HEAD\nb\n=======\nc\n>>>>>>> nhanh\n"
    for thu_muc, thuoc_tinh in (("ops/land", "* conflict-marker-size=40"), ("ops/reviews/a/b/c", "* conflict-marker-size=40"),
                                ("ops/specs", "* binary"), ("ops/leases/d", "* -diff")):
        pr = {f"{thu_muc}/.gitattributes": thuoc_tinh + "\n", f"{thu_muc}/x.md": xung_dot}
        with kho_that(nhanh_pr=pr) as (kho, goc, dau):
            tho = git(kho, "-c", "core.whitespace=-blank-at-eol,-blank-at-eof,-space-before-tab",
                      "diff", "--check", f"{goc}...{dau}", kiem=False)
            bang(tho.returncode == 0, f"fixture vo hieu ({thu_muc}, {thuoc_tinh}): thuoc tinh cua PR phai TAT duoc `--check` doc cay lam viec")
            rc, log = kiem_re(m, kho, goc, dau)
            bang(rc == 1 and "diff --check" in log and f"{thu_muc}/x.md" in log,
                 f"{thu_muc}: dau xung dot phai DO du PR mang .gitattributes: rc={rc}: {log}")
    pr = {"ops/reviews/r/.gitattributes": "luot*-VERDICT.md -whitespace\n",
          "ops/reviews/r/luot1-VERDICT.md": "verdict chep nguyen byte   \n\tdong\n\n"}
    with kho_that(nhanh_pr=pr) as (kho, goc, dau):
        rc, log = kiem_re(m, kho, goc, dau)
        bang(rc == 0, f"doi chung: PR ho so them .gitattributes `-whitespace` (nhu PR #667, #670) phai DAT: rc={rc}: {log}")


@ca
def t20s_kiem_re_tep_nhi_phan_la_khong_do_duoc():
    """Luot 9 (lop `kiem-re-cua-fail-close-chua-co-ca`, pham vi `diff --check`): git coi tep co NUL la nhi phan va
    `--check` BO QUA no — dau xung dot trong do lot. Tai 3569472cb9: 0/1991 tep duoi allowlist la nhi phan ⇒ nhi phan
    = DO."""
    m = nap_module()
    with kho_that(nhanh_pr={"ops/land/x.md": b"a\0\n<<<<<<< HEAD\nb\n=======\nc\n>>>>>>> nhanh\n"}) as (kho, goc, dau):
        bang(git(kho, "diff", "--check", f"{goc}...{dau}", kiem=False).returncode == 0,
             "fixture vo hieu: `--check` phai BO QUA tep nhi phan (khong thi ca nay khong do gi)")
        rc, log = kiem_re(m, kho, goc, dau)
        bang(rc == 1 and "nhi phan" in log and "ops/land/x.md" in log, f"tep ho so nhi phan phai DO kiem-re: rc={rc}: {log}")
    with kho_that(nhanh_pr={"ops/land/x.md": "van ban\n"}) as (kho, goc, dau):
        bang(m.kiem_nhi_phan(env_pr(goc=goc, dau=dau), chay_that, kho) == [], "doi chung: tep van ban khong phai nhi phan")
    for ten, chay, can in (("nem", chay_gia(nem=SuDoGia("git no")), "KHONG DO DUOC"),
                           ("rc=128", chay_gia(b"", rc=128), "rc=128"),
                           ("dau ra cut", chay_gia(b"1\t0\tops/land/a.md"), "cut")):
        try:
            loi = m.kiem_nhi_phan(env_pr(), chay)
        except SuDoGia as e:
            raise TinHieuChotCa(f"{ten}: numstat nem ma kiem_nhi_phan KHONG bat: {e}") from e
        bang(len(loi) == 1 and can in loi[0], f"numstat {ten} phai thanh loi, duoc {loi}")


@ca
def t20t_kiem_re_thuoc_tinh_diff_cua_pr_khong_bien_nhi_phan_thanh_van_ban():
    """Cross-review luot 9 (`kiem-re-bi-cau-hinh-boi-du-lieu-ho-so`, cua `--numstat`): `diff` (set) do PR mang vao ep tep co
    NUL la van ban cho `--numstat` doc thuoc tinh cay lam viec, trong khi `--check` (thuoc tinh GOC) van bo qua no."""
    m = nap_module()
    noi = b"a\0\n<<<<<<< HEAD\nb\n=======\nc\n>>>>>>> nhanh\n"
    for thu_muc, attr in (("ops/land", "* diff\n"), ("ops/reviews/a/b", "x.md diff\n")):
        with kho_that(nhanh_pr={f"{thu_muc}/.gitattributes": attr, f"{thu_muc}/x.md": noi}) as (kho, goc, dau):
            ns = git(kho, "diff", "--numstat", f"{goc}...{dau}").stdout.decode()
            bang(f"\t{thu_muc}/x.md" in ns and f"-\t-\t{thu_muc}/x.md" not in ns,
                 f"fixture vo hieu ({thu_muc}): thuoc tinh cua PR phai ep numstat cay-lam-viec coi tep la van ban: {ns!r}")
            bang(git(kho, f"--attr-source={goc}", "diff", "--check", f"{goc}...{dau}", kiem=False).returncode == 0,
                 f"fixture vo hieu ({thu_muc}): `--check` doc thuoc tinh goc phai BO QUA tep nhi phan")
            rc, log = kiem_re(m, kho, goc, dau)
            bang(rc == 1 and "nhi phan" in log and f"{thu_muc}/x.md" in log,
                 f"{thu_muc}: tep co NUL phai DO du PR mang `diff`: rc={rc}: {log}")


# Hop dong doi so (lop `kiem-re-bi-cau-hinh-boi-du-lieu-ho-so`): MOI loi goi git chay bo may diff/merge cua bo phan loai
# va kiem-re doc thuoc tinh tu cay GOC. `merge-base --all` chi doc do thi commit nen KHONG thuoc tap nay (khai rieng).
LOI_GOI_DOC_THUOC_TINH = {
    "ba cham --name-only": lambda a: a[1:3] == ["diff", "--name-only"] and a[-1] == f"{GOC_A}...{GOC_B}",
    # Cross-review luot 12: ghim CA hai commit cua merge-tree — `goc, goc` lam cap "goc -> cay merge-tree" RONG ma van DAT.
    "merge-tree": lambda a: a[1:3] == ["merge-tree", "--write-tree"] and a[-2:] == [GOC_A, GOC_B],
    "diff goc -> cay merge-tree": lambda a: a[1:4] == ["diff", "--no-renames", "--name-only"] and a[-1] == CAY_GIA,
    "diff goc -> merge ref": lambda a: a[1:4] == ["diff", "--no-renames", "--name-only"] and a[-1] == HOP_GIA,
    "diff --check": lambda a: "--check" in a,
    "diff --numstat": lambda a: "--numstat" in a,
    "raw ba cham (kiem_mode_git)": lambda a: a[1:3] == ["diff", "--raw"] and a[-1] == f"{GOC_A}...{GOC_B}",
    "raw goc -> cay merge-tree (kiem_mode_git)": lambda a: a[1:3] == ["diff", "--raw"] and a[-2:] == [GOC_A, CAY_GIA],
    "raw goc -> merge ref (kiem_mode_git)": lambda a: a[1:3] == ["diff", "--raw"] and a[-2:] == [GOC_A, HOP_GIA],
}
# So loi goi mong doi != 1: `merge-tree` chay HAI lan o kiem-re (bo phan loai + kiem_mode_git), cung doi so.
SO_LOI_GOI = {"merge-tree": 2}


@ca
def t20u_moi_loi_goi_git_doc_thuoc_tinh_tu_goc():
    """Khoa tung DUONG VAO cua lop: moi loi goi git (tru `merge-base`) mang `--attr-source=<goc>` NGAY SAU `git`. Ba duong
    (`merge-tree`, `--check`, `--numstat`) co ca hanh vi rieng (t11e, t20p, t20t); ba duong `--name-only --no-renames` so OID,
    khong do doi ten — co doc thuoc tinh hay khong la CHUA DO — nen chi hop dong nay canh — go chot o do khong doi hanh vi hom nay, nhung mo cua neu ai bo `--no-renames`."""
    m = nap_module()
    log = []
    rc = _kiem_re_gia(m, env_pr(), chay_gia(nul("ops/land/khong-co-trong-cay.md"), log=log))
    bang(rc == 0, f"fixture vo hieu: kiem-re do gia phai DAT, duoc rc={rc}")
    goi_git = [a for a in log if a[:1] == ["git"]]
    for ten, khop in LOI_GOI_DOC_THUOC_TINH.items():
        thay = [a for a in goi_git if khop(bo_attr_source(a))]
        can = SO_LOI_GOI.get(ten, 1)
        bang(len(thay) == can, f"{ten}: phai co DUNG {can} loi goi, thay {len(thay)}: {goi_git}")
        for mot in thay:
            bang(mot[1] == f"--attr-source={GOC_A}", f"{ten}: thuoc tinh phai doc tu cay GOC (--attr-source ngay sau git): {mot}")
    con_lai = [a for a in goi_git if not any(k(bo_attr_source(a)) for k in LOI_GOI_DOC_THUOC_TINH.values())]
    bang([a[1:3] for a in con_lai] == [["merge-base", "--all"]],
         f"loi goi git ngoai hop dong (phai xep vao LOI_GOI_DOC_THUOC_TINH hoac khai mien): {con_lai}")


def _commit_gitlink(kho, goc, duong):
    """Them tree entry gitlink (mode 160000) tai `duong` (thay tep cu neu co) va commit; dung THU MUC rong — thu git clone cuc bo
    de lai cho gitlink chua init (do 01-10-2026; actions/checkout khong init submodule theo tai lieu, chua do tren runner).
    Tra SHA dau moi."""
    git(kho, "rm", "-q", "--cached", "--ignore-unmatch", duong)
    if (kho / duong).is_file():
        (kho / duong).unlink()
    git(kho, "update-index", "--add", "--cacheinfo", f"160000,{goc},{duong}")
    git(kho, "commit", "-q", "-m", "gitlink")
    (kho / duong).mkdir(parents=True, exist_ok=True)
    return git(kho, "rev-parse", "HEAD").stdout.decode().strip()


@ca
def t20v_kiem_re_gitlink_ho_so_do():
    """Cross-review luot 10 (`kiem-re-cua-fail-close-chua-co-ca`, cua gitlink THEM MOI): tree entry mode 160000 duoi allowlist;
    checkout khong init submodule de lai THU MUC rong (git cuc bo: do; actions/checkout: theo tai lieu, chua do tren runner).
    `kiem_loai_tep` chi hoi symlink; `kiem_yaml`/`kiem_lease` coi
    `not is_file()` la DA XOA (ke ca ten `.yaml`); `--check` khong co noi dung, numstat dem duoc dong (khong ra `-`).
    Chot: mode TRONG GIT."""
    m = nap_module()
    # WP748 r6/g6: ten khong duoi tung la `con` — ten THIET BI danh rieng tren Windows, git tu choi (`Invalid path`) => fixture
    # HONG o ha tang; doi ten khac van giu dung dieu do (ten khong duoi `.yaml` duoi allowlist).
    for duong in ("ops/land/zz.yaml", "ops/specs/conl"):
        with kho_that(nhanh_pr={"ops/specs/S.md": "# s\n"}) as (kho, goc, dau):
            dau2 = _commit_gitlink(kho, goc, duong)
            bang(git(kho, "ls-tree", dau2, "--", duong).stdout.decode().startswith("160000 commit "),
                 f"fixture vo hieu: {duong} phai la gitlink")
            bang(m.kiem_yaml({duong}, kho) == [] and m.kiem_loai_tep({duong}, kho) == []
                 and m.kiem_nhi_phan(env_pr(goc=goc, dau=dau2), chay_that, kho) == []
                 and git(kho, f"--attr-source={goc}", "diff", "--check", f"{goc}...{dau2}", kiem=False).returncode == 0,
                 f"fixture vo hieu ({duong}): moi chot doc dia/noi dung phai cung KHONG thay gitlink (khong thi ca nay khong do gi)")
            rc, log = kiem_re(m, kho, goc, dau2)
            bang(rc == 1 and "mode 160000, A" in log and duong in log, f"{duong}: gitlink ho so phai DO kiem-re: rc={rc}: {log}")


@ca
def t20w_kiem_re_tep_ho_so_doi_thanh_gitlink_do():
    """Luot 10, cua DOI KIEU (git bao `T`, khong phai `A`): tep ho so da co o goc bi thay bang gitlink cung ten."""
    m = nap_module()
    with kho_that(nen={"README.md": "x\n", "ops/land/a.yaml": "a: 1\n"}, nhanh_pr={"ops/specs/S.md": "# s\n"}) as (kho, goc, dau):
        dau2 = _commit_gitlink(kho, goc, "ops/land/a.yaml")
        raw = git(kho, "diff", "--raw", "--no-abbrev", goc, dau2, "--", "ops/land/a.yaml").stdout.decode()
        bang(raw.startswith(":100644 160000 ") and raw.split("\t")[0].endswith(" T"), f"fixture vo hieu: phai la doi kieu T: {raw!r}")
        bang(m.kiem_yaml({"ops/land/a.yaml"}, kho) == [], "fixture vo hieu: kiem_yaml phai coi thu muc rong la da xoa")
        rc, log = kiem_re(m, kho, goc, dau2)
        bang(rc == 1 and "mode 160000, T" in log and "ops/land/a.yaml" in log, f"tep doi thanh gitlink phai DO kiem-re: rc={rc}: {log}")


@ca
def t20x_kiem_re_symlink_tren_nen_khong_symlink_do():
    """Luot 10, cua SYMLINK TREN DIA LA TEP THUONG: `core.symlinks=false` (mac dinh Git for Windows theo tai lieu, chua do;
    gate-ops chay Windows khi ma tran co `windows-latest`)
    checkout symlink thanh tep thuong chua duong dich => `kiem_loai_tep` (doc dia) KHONG thay. Mode trong git van la 120000."""
    m = nap_module()
    duong = "ops/land/l.yaml"
    with kho_that(nhanh_pr={"ops/specs/S.md": "# s\n"}) as (kho, goc, dau):
        (kho / duong).parent.mkdir(parents=True, exist_ok=True)
        (kho / duong).symlink_to("../../README.md")
        git(kho, "add", "-A")
        git(kho, "commit", "-q", "-m", "symlink")
        dau2 = git(kho, "rev-parse", "HEAD").stdout.decode().strip()
        (kho / duong).unlink()
        git(kho, "-c", "core.symlinks=false", "checkout", "--", duong)
        bang((kho / duong).is_file() and not (kho / duong).is_symlink() and m.kiem_loai_tep({duong}, kho) == [],
             "fixture vo hieu: core.symlinks=false phai checkout symlink thanh tep thuong ma kiem_loai_tep khong thay")
        rc, log = kiem_re(m, kho, goc, dau2)
        bang(rc == 1 and "mode 120000" in log and duong in log, f"symlink (dia la tep thuong) phai DO kiem-re: rc={rc}: {log}")


@ca
def t20y_kiem_re_mode_755_va_tep_thanh_thu_muc_dat():
    """Doi chung cua `kiem_mode_git` (khong chan oan): 100755 la tep thuong; tep ho so doi thanh THU MUC cung ten la `D` cho
    tep cu + `A` 100644 cho tep con — ca hai phai DAT."""
    m = nap_module()
    with kho_that(nen={"README.md": "x\n", "ops/land/a.md": "a\n"}, nhanh_pr={"ops/specs/S.md": "# s\n"}) as (kho, goc, dau):
        (kho / "ops/land/a.md").chmod(0o755)
        git(kho, "add", "-A")
        # WP748 r6/g6: Windows `core.filemode` tat => `chmod` khong vao index; dat bit thuc thi THANG trong index (moi nen).
        git(kho, "update-index", "--chmod=+x", "ops/land/a.md")
        git(kho, "commit", "-q", "-m", "755")
        dau2 = git(kho, "rev-parse", "HEAD").stdout.decode().strip()
        bang(git(kho, "ls-tree", dau2, "--", "ops/land/a.md").stdout.decode().startswith("100755 "), "fixture vo hieu: phai la 100755")
        rc, log = kiem_re(m, kho, goc, dau2)
        bang(rc == 0, f"doi chung: tep ho so 100755 la tep thuong, phai DAT: rc={rc}: {log}")
    with kho_that(nen={"README.md": "x\n", "ops/land/a.md": "a\n"}, nhanh_pr={"ops/land/a.md": None}) as (kho, goc, _d):
        viet(kho, "ops/land/a.md/x.md", "x\n")
        git(kho, "add", "-A")
        git(kho, "commit", "-q", "-m", "tep thanh thu muc")
        dau2 = git(kho, "rev-parse", "HEAD").stdout.decode().strip()
        rc, log = kiem_re(m, kho, goc, dau2)
        bang(rc == 0, f"doi chung: tep ho so doi thanh thu muc cung ten KHONG phai gitlink, phai DAT: rc={rc}: {log}")


@ca
def t20z_kiem_re_git_co_tep_ma_dia_khong_co_do():
    """Luot 10, cua GIT CO - DIA KHONG: merge ref noi `ops/land/x.yaml` la tep thuong nhung checkout khong co no (va cham ten
    khong phan biet hoa thuong, checkout thua...). `kiem_yaml` coi `not is_file()` la da xoa => bo qua trong im lang."""
    m = nap_module()
    with kho_that(nhanh_pr={"ops/land/x.yaml": "a: [1, 2\n"}) as (kho, goc, dau):
        (kho / "ops/land/x.yaml").unlink()
        bang(m.kiem_yaml({"ops/land/x.yaml"}, kho) == [], "fixture vo hieu: kiem_yaml phai bo qua tep vang tren dia")
        rc, log = kiem_re(m, kho, goc, dau)
        bang(rc == 1 and "tren dia KHONG phai tep thuong" in log and "ops/land/x.yaml" in log,
             f"git co ma dia khong co phai DO kiem-re: rc={rc}: {log}")


@ca
def t20za_kiem_mode_git_doc_du_ba_cap():
    """Luot 10, cua CAP DIFF: duong dan co trong merge ref ma khong co trong head (va nguoc lai) — moi cap (`goc...dau`,
    `goc -> cay merge-tree`, `goc -> merge ref`) la mot cua rieng. Cung MOT duong dan o ca ba cap (tap khop), chi MOT cap
    mang mode 160000: bo cap do thi khong con gi DO."""
    m = nap_module()
    duong = "ops/land/g"
    thuong, gl = raw_ghi(("100644", "M", duong)), raw_ghi(("160000", "T", duong))
    with _cay_tam({duong: "g\n"}) as kho:   # dia CO tep thuong: chot dia cua cap merge ref khong xen vao phep do
        for cap, ten in (("ba_cham", "ba cham"), ("cay", "goc -> cay merge-tree"), ("hop", "goc -> merge ref")):
            raw = {k: (0, gl if k == cap else thuong) for k in ("ba_cham", "cay", "hop")}
            loi = m.kiem_mode_git(env_pr(), chay_gia(raw=raw), kho, {duong})
            bang(len(loi) == 1 and f"cap {ten}" in loi[0] and "mode 160000" in loi[0], f"{ten}: gitlink chi o cap nay phai DO: {loi}")
        raw = {k: (0, b"") for k in ("ba_cham", "cay")}
        raw["hop"] = (0, raw_ghi(("160000", "A", duong)))
        loi = m.kiem_mode_git(env_pr(), chay_gia(raw=raw), kho, {duong})
        bang(any("cap goc -> merge ref" in x for x in loi), f"gitlink CHI o merge ref (khong o head) phai DO: {loi}")


@ca
def t20zb_kiem_mode_git_khong_do_duoc_thi_do():
    """Luot 10: moi cach `kiem_mode_git` KHONG DO DUOC (git nem/loi, dau ra cut/le/ban ghi la, trang thai la, tap lech) => DO."""
    m = nap_module()
    d = "ops/land/a.md"
    tot = raw_ghi(("100644", "M", d))
    kich_ban = (
        ("merge-tree nem", dict(merge_tree=SuDoGia("mt")), "merge-tree (kiem mode) nem"),
        ("merge-tree rc=1", dict(merge_tree=(1, (CAY_GIA + "\n").encode())), "merge-tree (kiem mode) rc=1"),
        ("merge-tree dau ra la", dict(merge_tree=(0, b"khong-phai-sha\n")), "merge-tree (kiem mode) rc=0"),
        ("raw nem", dict(raw={"ba_cham": SuDoGia("raw")}), "nem SuDoGia"),
        ("raw rc=128", dict(raw={"ba_cham": (128, tot)}), "rc=128"),
        ("raw cut", dict(raw={"ba_cham": (0, tot[:-1])}), "dau ra cut"),
        ("raw le", dict(raw={"ba_cham": (0, tot + b":100644 100644\0")}), "so muc le"),
        ("raw dau ghi la", dict(raw={"ba_cham": (0, b":100644 100644 xx yy M\0" + d.encode() + b"\0")}), "ban ghi la"),
        ("raw trang thai U", dict(raw={"ba_cham": (0, raw_ghi(("100644", "U", d)))}), "ban ghi la"),
        ("raw trung duong", dict(raw={"ba_cham": (0, tot + tot)}), "ban ghi la"),
        ("D mode khac 0", dict(raw={"ba_cham": (0, raw_ghi(("160000", "D", d)))}), "mode 160000, D"),
        ("tap lech", dict(raw={"ba_cham": (0, tot + raw_ghi(("100644", "A", "ops/land/them.md")))}), "lech tap da phan loai"),
        # Cross-review luot 11 (`kiem-mode-git-chot-khong-rang`): chieu NGUOC cua chot tap — duong dan da phan loai ma KHONG cap
        # `--raw` nao liet ke thi mode cua no KHONG duoc kiem; va `D` mang mode tep thuong (khong phai 000000) la ban ghi hong.
        ("tap thieu", dict(raw={"ba_cham": (0, b""), "cay": (0, b"")}), "lech tap da phan loai"),
        ("D mode tep thuong", dict(raw={"ba_cham": (0, raw_ghi(("100644", "D", d)))}), "mode 100644, D"),
        # Luot 12 (liet ke het chot cua `_doc_raw`/`kiem_mode_git`, moi chot mot dot bien rieng): stdout KHONG phai bytes ma
        # `bytes()` van nhan (memoryview) => chot kieu la thu DUY NHAT chan; duong dan RONG trong ban ghi; bo qua loi cua mot cap.
        ("raw stdout khong phai bytes", dict(raw={"ba_cham": (0, memoryview(tot))}), "--raw " + GOC_A + "..." + GOC_B + " rc=0"),
        ("merge-tree stdout khong phai bytes", dict(merge_tree=(0, memoryview((CAY_GIA + "\n").encode()))), "merge-tree (kiem mode) rc=0"),
        ("raw duong rong", dict(raw={"ba_cham": (0, tot.split(b"\0")[0] + b"\0\0")}), "ban ghi la"),
        # Cross-review luot 12: dau ghi co DUOI THUA sau trang thai (chot `fullmatch`); mode moi 000000 ma KHONG phai `D`
        # (ve `trang_thai == "D"` cua nhanh bo qua xoa — ve `mode == "000000"` da co `mode_git_xoa_bo_kiem_mode`).
        ("raw dau ghi duoi thua", dict(raw={"ba_cham": (0, raw_ghi(("100644", "Mx", d)))}), "ban ghi la"),
        ("A mode 000000", dict(raw={"ba_cham": (0, raw_ghi(("000000", "A", d)))}), "mode 000000, A"),
    )
    for ten, kw, can in kich_ban:
        kw.setdefault("raw", {})
        kw["raw"] = {"ba_cham": (0, tot), "cay": (0, tot), "hop": (0, b""), **kw["raw"]}
        try:
            loi = m.kiem_mode_git(env_pr(), chay_gia(**kw), ROOT_THAT, {d})
        except SuDoGia as e:
            raise TinHieuChotCa(f"{ten}: git nem ma kiem_mode_git KHONG bat: {e}") from e
        bang(loi and any(can in x for x in loi), f"{ten}: phai DO voi '{can}', duoc {loi}")
    bang(m.kiem_mode_git(env_pr(), chay_gia(raw={"ba_cham": (0, tot), "cay": (0, tot), "hop": (0, b"")}), ROOT_THAT, {d}) == [],
         "doi chung: ba cap sach, tap khop phai DAT")


@ca
def t20zd_kiem_mode_git_dia_la_symlink_do():
    """Luot 12: chot DIA cua cap `goc -> merge ref` co HAI ve — `not is_file()` (t20z) va `is_symlink()`. Symlink tro toi tep
    thuong co `is_file()` DUNG nen chi ve `is_symlink()` chan; o muc `kiem-re` ve ay trung voi `kiem_loai_tep` (t20n/t20q), nen
    phep do nay goi THANG `kiem_mode_git` de ve ay co rang rieng theo dung hop dong docstring ("tren dia phai LA tep thuong")."""
    m = nap_module()
    duong = "ops/land/s.md"
    tot = raw_ghi(("100644", "M", duong))
    with _cay_tam({"ops/land/that.md": "t\n"}) as kho:
        (kho / duong).symlink_to("that.md")   # nhu t20n/t20q/t20x: khong tha im lang khi nen khong tao duoc symlink
        bang((kho / duong).is_file(), "fixture vo hieu: symlink phai tro toi tep thuong (is_file DUNG)")
        loi = m.kiem_mode_git(env_pr(), chay_gia(raw={k: (0, tot) for k in ("ba_cham", "cay", "hop")}), kho, {duong})
        bang(len(loi) == 1 and "tren dia KHONG phai tep thuong" in loi[0], f"git noi tep thuong ma dia la symlink phai DO: {loi}")


@ca
def t20ze_kiem_re_ten_tep_khong_utf8_dat():
    """Cross-review luot 12: bo phan loai giai ma `-z` bang `surrogateescape` nen ten tep KHONG phai UTF-8 duoi allowlist di
    duong nhanh; `_doc_raw` phai giai ma CUNG cach, khong thi `kiem_mode_git` nem UnicodeDecodeError (traceback, DO oan).
    Windows (WP748 r6/g6): `os.fsdecode` o do giai ma CHAT nen khong dung duoc ten qua cay lam viec; commit dung bang plumbing
    (`update-index -z --index-info` nhan BYTE ten tu stdin) va tep dia mang dung ten `surrogateescape` ma san pham se hoi."""
    m = nap_module()
    ten_b = b"ops/specs/t\xff.md"
    ten = ten_b.decode("utf-8", "surrogateescape")   # = os.fsdecode tren posix
    with kho_that(nhanh_pr=None if os.name == "nt" else {ten: "# s\n"}) as (kho, goc, dau):
        if os.name == "nt":
            def vao(du_lieu, *doi):
                r = subprocess.run(["git", "-c", "commit.gpgsign=false", *doi], cwd=kho, input=du_lieu, capture_output=True,
                                   env=_env_git())
                if r.returncode:
                    raise RuntimeError(f"ha tang: git {' '.join(doi)} rc={r.returncode}: {r.stderr[:300]!r}")
                return r.stdout.strip()
            blob = vao(b"# s\n", "hash-object", "-w", "--stdin")
            vao(b"100644 " + blob + b"\t" + ten_b + b"\0", "update-index", "-z", "--index-info")
            git(kho, "commit", "-q", "-m", "ten khong utf8")
            dau = git(kho, "rev-parse", "HEAD").stdout.decode().strip()
            viet(kho, ten, "# s\n")
        raw = git(kho, "diff", "--raw", "-z", "--no-abbrev", f"{goc}...{dau}").stdout
        bang(b"t\xff.md" in raw, f"fixture vo hieu: ten tep phai giu byte khong UTF-8: {raw!r}")
        try:
            rc, log = kiem_re(m, kho, goc, dau)
        except UnicodeError as e:   # CHI loi giai ma — dung dieu ca nay do; loi khac van la HONG (khong cap tin dung)
            raise TinHieuChotCa(f"kiem-re nem {type(e).__name__} tren ten tep khong UTF-8: {e}") from e
        bang(rc == 0, f"PR ten tep khong UTF-8 phai DAT kiem-re: rc={rc}: {log}")


@ca
def t20zf_kiem_re_symlink_doi_thanh_tep_thuong_dat():
    """Cross-review luot 13 (`kiem-mode-git-chot-khong-rang`, nhanh CHAP NHAN cua ve `trang_thai == "D" or mode not in
    MODE_THUONG`): trang thai `T` voi mode moi 100644 (symlink tren nen -> tep thuong trong PR) LA tep thuong theo git => DAT.
    Khong co ca nay thi dot bien coi moi `T` la loi (DO oan mot PR hop le) song qua moi ca."""
    m = nap_module()
    with kho_that() as (kho, _goc, _dau):
        git(kho, "checkout", "-q", "main")
        (kho / "ops" / "specs").mkdir(parents=True, exist_ok=True)
        (kho / "ops" / "specs" / "that.md").write_text("# t\n", encoding="utf-8")
        (kho / "ops" / "specs" / "x.md").symlink_to("that.md")   # nhu t20n/t20q/t20x: khong tha im lang khi nen khong tao duoc symlink
        git(kho, "add", "-A")
        git(kho, "commit", "-q", "-m", "nen co symlink")
        goc = git(kho, "rev-parse", "HEAD").stdout.decode().strip()
        git(kho, "checkout", "-q", "-b", "pr2")
        (kho / "ops" / "specs" / "x.md").unlink()
        (kho / "ops" / "specs" / "x.md").write_text("# x\n", encoding="utf-8")
        git(kho, "add", "-A")
        git(kho, "commit", "-q", "-m", "symlink thanh tep thuong")
        dau = git(kho, "rev-parse", "HEAD").stdout.decode().strip()
        raw = git(kho, "diff", "--raw", "--no-abbrev", f"{goc}...{dau}").stdout.decode()
        bang(re.search(r"^:120000 100644 [0-9a-f]+ [0-9a-f]+ T\tops/specs/x\.md$", raw, re.M) is not None,
             f"fixture vo hieu: phai la doi kieu T 120000 -> 100644: {raw!r}")
        rc, log = kiem_re(m, kho, goc, dau)
        bang(rc == 0, f"symlink -> tep thuong (T, 100644) phai DAT kiem-re: rc={rc}: {log}")


@ca
def t20zg_kiem_re_o_chap_nhan_con_lai_dat():
    """Luot 14 (`kiem-mode-git-chot-khong-rang`, tu liet ke nhanh CHAP NHAN theo trang thai x mode moi): cac o chua co ca git
    that ghim — `A` 100755 (tep ho so MOI co bit thuc thi), `M` 100644 (sua noi dung tep thuong), `T` 120000 -> 100755
    (symlink tren nen -> tep thuc thi). Ca ba LA tep thuong theo git => DAT. Moi o mot dot bien rieng coi DUNG o do la loi."""
    m = nap_module()
    with kho_that() as (kho, _goc, _dau):
        git(kho, "checkout", "-q", "main")
        (kho / "ops" / "specs").mkdir(parents=True, exist_ok=True)
        (kho / "ops" / "specs" / "that.md").write_text("# t\n", encoding="utf-8")
        (kho / "ops" / "specs" / "sua.md").write_text("# a\n", encoding="utf-8")
        (kho / "ops" / "specs" / "y.md").symlink_to("that.md")   # nhu t20zf: khong tha im lang khi nen khong tao duoc symlink
        git(kho, "add", "-A")
        git(kho, "commit", "-q", "-m", "nen")
        goc = git(kho, "rev-parse", "HEAD").stdout.decode().strip()
        git(kho, "checkout", "-q", "-b", "pr3")
        (kho / "ops" / "specs" / "sua.md").write_text("# b\n", encoding="utf-8")
        (kho / "ops" / "specs" / "y.md").unlink()
        (kho / "ops" / "specs" / "y.md").write_text("# y\n", encoding="utf-8")
        (kho / "ops" / "specs" / "y.md").chmod(0o755)
        (kho / "ops" / "specs" / "moi.md").write_text("# m\n", encoding="utf-8")
        (kho / "ops" / "specs" / "moi.md").chmod(0o755)
        git(kho, "add", "-A")
        # WP748 r6/g6: nhu t20y — Windows `core.filemode` tat, dat bit thuc thi THANG trong index (moi nen).
        git(kho, "update-index", "--chmod=+x", "ops/specs/y.md", "ops/specs/moi.md")
        git(kho, "commit", "-q", "-m", "ba o chap nhan")
        dau = git(kho, "rev-parse", "HEAD").stdout.decode().strip()
        raw = git(kho, "diff", "--raw", "--no-abbrev", "--no-renames", f"{goc}...{dau}").stdout.decode()
        for mau, o in ((r"^:000000 100755 [0-9a-f]+ [0-9a-f]+ A\tops/specs/moi\.md$", "A 100755"),
                       (r"^:100644 100644 [0-9a-f]+ [0-9a-f]+ M\tops/specs/sua\.md$", "M 100644"),
                       (r"^:120000 100755 [0-9a-f]+ [0-9a-f]+ T\tops/specs/y\.md$", "T 120000 -> 100755")):
            bang(re.search(mau, raw, re.M) is not None, f"fixture vo hieu: thieu o {o}: {raw!r}")
        rc, log = kiem_re(m, kho, goc, dau)
        bang(rc == 0, f"A 100755 / M 100644 / T -> 100755 deu la tep thuong, phai DAT kiem-re: rc={rc}: {log}")


# LUAT (lop `kiem-mode-git-chot-khong-rang`, dong theo CAU TRUC o luot 14): bang quyet dinh DAY DU cua `kiem_mode_git` tren
# (trang thai, mode MOI). San pham chi quyet theo hai truong nay, nen tich duoi day la TOAN BO khong gian dau vao cua nhanh quyet
# dinh. CHI bay o CHAP NHAN; moi o con lai TU CHOI. Day la luat cua bo test, KHONG doc lai tu ma duoi do.
TRANG_THAI_BANG = ("A", "M", "T", "D")
MODE_BANG = ("000000", "100644", "100755", "120000", "160000")
O_CHAP_NHAN = frozenset({("A", "100644"), ("A", "100755"), ("M", "100644"), ("M", "100755"),
                         ("T", "100644"), ("T", "100755"), ("D", "000000")})


@ca
def t20zh_kiem_mode_git_bang_quyet_dinh_day_du():
    """Cross-review luot 14 (`kiem-mode-git-chot-khong-rang`, LAN THU 4 — chu kho chot: dong bang MOT ca bang quyet dinh roi
    DUNG lop): duyet TOAN BO {A,M,T,D} x {000000,100644,100755,120000,160000} = hai muoi o qua `kiem_mode_git` voi ban ghi `--raw`
    gia (cung dang byte voi git that — t20zf/t20zg ghim dang ay tren git that) o CA BA cap. O CHAP NHAN ⇒ khong loi; o TU CHOI
    ⇒ DUNG ba loi, moi cap mot loi, moi loi neu dung `mode <mode>, <trang thai>`.
    Bay o git KHONG sinh duoc van nam trong bang, ky vong TU CHOI (ban ghi hong ⇒ fail-close): `A`/`M`/`T` voi mode moi 000000
    (chi `D` co mode moi 000000) va `D` voi mode moi khac 000000 (git luon ghi 000000 cho phia moi cua `D`). Muoi ba o con lai
    git sinh duoc (bay CHAP NHAN; sau TU CHOI: A/M/T x 120000/160000 — them, doi dich/nang con tro, doi kieu thanh symlink/gitlink).
    Kich thuoc va phan ra ay (hai muoi = bay + muoi ba; muoi ba = bay + sau) do o dong `ha tang bang` cua chinh ca nay.
    Moi o co mot dot bien LAT RIENG (`mode_git_lat_o_*`, sinh tu chinh bang nay), cong dot bien mien tru trang thai `M` (dot bien
    X1 cua reviewer luot 14, SONG SOT toan suite truoc ca nay) — ca nay la dich DUY NHAT cua tat ca."""
    m = nap_module()
    duong = "ops/land/g"
    cap_mong = {"ba cham", "goc -> cay merge-tree", "goc -> merge ref"}
    sai = []
    with _cay_tam({duong: "g\n"}) as kho:   # dia CO tep thuong: chot dia cua cap merge ref khong xen vao phep do
        for tt in TRANG_THAI_BANG:
            for mode in MODE_BANG:
                ghi = raw_ghi((mode, tt, duong))
                loi = m.kiem_mode_git(env_pr(), chay_gia(raw={k: (0, ghi) for k in ("ba_cham", "cay", "hop")}), kho, {duong})
                if (tt, mode) in O_CHAP_NHAN:
                    if loi != []:
                        sai.append(f"({tt}, {mode}) phai CHAP NHAN, duoc {loi}")
                    continue
                cap = {k.group(1) for k in (re.search(rf"\(mode {mode}, {tt}, cap ([^)]+)\)", x) for x in loi) if k}
                if not (len(loi) == 3 and cap == cap_mong):
                    sai.append(f"({tt}, {mode}) phai TU CHOI o DUNG ba cap, duoc {loi}")
    tich = {(t, x) for t in TRANG_THAI_BANG for x in MODE_BANG}
    khong_sinh = {(t, "000000") for t in TRANG_THAI_BANG if t != "D"} | {("D", x) for x in MODE_BANG if x != "000000"}
    bang(len(tich) == 20 and O_CHAP_NHAN < tich and khong_sinh < tich and not (khong_sinh & O_CHAP_NHAN)
         and (len(khong_sinh), len(tich - khong_sinh), len(O_CHAP_NHAN), len(tich - khong_sinh - O_CHAP_NHAN)) == (7, 13, 7, 6),
         "ha tang bang: tich phai du 20 o, moi o chap nhan thuoc tich, phan ra 7 o git khong sinh + 13 o sinh duoc "
         "(7 chap nhan + 6 tu choi) phai khop docstring")
    bang(not sai, f"bang quyet dinh kiem_mode_git lech {len(sai)} o: {sai}")


@ca
def t20zc_kiem_re_doi_ten_tep_ho_so_dat():
    """Cross-review luot 11 (`kiem-mode-git-chot-khong-rang`): `git diff` mac dinh DO doi ten (`diff.renames`), ban ghi `--raw`
    khi do la `R100` kem HAI duong dan => `_doc_raw` bao dau ra hong. `--no-renames` la dieu kien de PR doi ten tep ho so
    (thao tac hop le) khong DO OAN o required check; khong ca nao khoa co ay."""
    m = nap_module()
    with kho_that(nen={"README.md": "x\n", "ops/land/a.yaml": "a: 1\nb: 2\n"},
                  nhanh_pr={"ops/land/a.yaml": None, "ops/land/b.yaml": "a: 1\nb: 2\n"}) as (kho, goc, dau):
        raw = git(kho, "diff", "--raw", "--no-abbrev", f"{goc}...{dau}").stdout.decode()
        bang(" R100\t" in raw, f"fixture vo hieu: git diff mac dinh phai do doi ten (R100): {raw!r}")
        rc, log = kiem_re(m, kho, goc, dau)
        bang(rc == 0, f"PR doi ten tep ho so phai DAT kiem-re: rc={rc}: {log}")


@ca
def t20q_kiem_re_symlink_hop_le_moi_duoi_do():
    """Cross-review luot 8: docstring khai chan MOI symlink "treo hay khong"; t20n chi co symlink TREO duoi `.md`."""
    m = nap_module()
    for ten, duong in (("hop le .md", "ops/reviews/hop-le.md"), ("hop le .yaml", "ops/land/l.yaml")):
        with kho_that(nhanh_pr={"ops/specs/S.md": "# s\n"}) as (kho, goc, dau):
            _symlink(kho / duong, "../../README.md")
            bang((kho / duong).exists(), f"fixture vo hieu: {duong} phai la symlink HOP LE")
            git(kho, "add", "-A")
            git(kho, "commit", "-q", "-m", "symlink")
            dau2 = git(kho, "rev-parse", "HEAD").stdout.decode().strip()
            rc, log = kiem_re(m, kho, goc, dau2)
            bang(rc == 1 and "tep ho so la symlink" in log, f"{ten}: symlink phai DO kiem-re: rc={rc}: {log}")


# Lop `buoc-bi-bo-doc-ca-cay-khong-chi-ba-ca` (cross-review luot 8b, P2): moi DUONG VAO mot nhanh rieng cua t20zi, moi nhanh mot
# dot bien rieng chi nhanh ay bat. Symlink HOP LE co san tren goc (vao qua PR day du); PR ho so chi XOA => symlink TREO ngoai diff.
SYMLINK_GOC = {   # duong symlink -> dich (tuong doi thu muc cha cua symlink)
    "docs/l1.md": "../ops/specs/D1.md",                      # E1: ngoai allowlist, dich la TEP
    "docs/tm": "../ops/specs/tm",                            # E1b: ngoai allowlist, dich la THU MUC (os.walk xep symlink treo vao TEP)
    "ops/land/l3.md": "../specs/D3.md",                      # E3: DUOI allowlist nhung KHONG trong diff
    "docs/xuyen.md": ("../ops/specs/qua/q.md" if sys.platform == "win32" else "../ops/specs/qua/../../../README.md"),  # E4: dich ngoai ho so, DUONG DI xuyen thu muc ho so
    ".claude/l5.md": "../ops/specs/D5.md",                   # E5: trong thu muc CHAM (t82 chep ca thu muc cham, tru .git)
}
NHANH_XOA = {   # nhanh PR -> (lenh git rm, symlink phai bi bao TREO)
    "e1-xoa-dich-tep": (("ops/specs/D1.md",), "docs/l1.md"),
    "e1b-xoa-thu-muc-dich": (("-r", "ops/specs/tm"), "docs/tm"),
    "e3-xoa-dich-trong-allowlist": (("ops/specs/D3.md",), "ops/land/l3.md"),
    "e4-xoa-thu-muc-tren-duong-di": (("-r", "ops/specs/qua"), "docs/xuyen.md"),
    "e5-xoa-dich-cua-thu-muc-cham": (("ops/specs/D5.md",), ".claude/l5.md"),
}


@ca
def t20zi_kiem_re_symlink_treo_ngoai_diff_do():
    """Cross-review luot 8b (P2 `buoc-bi-bo-doc-ca-cay-khong-chi-ba-ca`): `kiem_loai_tep`/`kiem_mode_git` chi nhin duong dan DOI,
    con `t82` (bi bo o duong nhanh) `copytree` CA cay va theo symlink. Do tren HEAD 680301261e TRUOC khi va (rig kho tam, hai ve mot
    lenh): ca nam nhanh duoi deu `kiem-re rc=0` va `t82 rc=1 shutil.Error`. Doi chung (PR sua tep KHAC; symlink treo CHUA THEO DOI
    trong `.git/`, `__pycache__/`, `*.pyc` — t82 bo qua chung) phai DAT. Khong phai duong vao (do, khong co delta): dich doi tu
    tep thanh THU MUC (t82 van chep duoc, rc=0); ten trung tep ma t82 GHI vao ban sao (`ops/leases/hong.yaml/` la thu muc) —
    `kiem-re` DA DO nho ca du lieu t23 (glob `*.yaml`). E1b dung chung duong voi E1 (symlink treo luon nam trong danh sach TEP
    cua `os.walk`), nen khong co dot bien rieng."""
    m = nap_module()
    nen = {"README.md": "x\n", "ops/specs/E.md": "# e\n", "ops/specs/D1.md": "# 1\n", "ops/specs/tm/a.md": "a\n",
           "ops/specs/D3.md": "# 3\n", "ops/specs/qua/q.md": "q\n", "ops/specs/D5.md": "# 5\n", "ops/land/x.yaml": "a: 1\n"}
    with kho_that(nen=nen) as (kho, _a, _h):
        git(kho, "checkout", "-q", "main")
        for duong, dich in SYMLINK_GOC.items():
            _symlink(kho / duong, dich, target_is_directory=(duong == "docs/tm"))
        # WP748 r6/g6 (do tai 397fc2a tren Windows native): Windows giai `..` trong dich symlink theo TU VUNG nen E4 o tren
        # khong phan biet duoc nhan voi tu vung, dot bien `symlink_treo_doc_tu_vung` SONG SOT. Nen chung chung cho moi nen:
        # symlink TUONG DOI `ops/land/sub/l -> ../Y.md` HOP LE, toi qua bi danh thu muc `ops/specs/bd -> ../land/sub`. Nhan
        # giai dich theo thu muc VAT LY cua symlink (land) => ton tai; ghep tu vung theo duong bi danh (specs) => khong ton tai
        # => ban tu vung DO OAN o doi chung.
        _symlink(kho / "ops" / "land" / "sub" / "l", "../Y.md")
        viet(kho, "ops/land/Y.md", "y\n")
        _symlink(kho / "ops" / "specs" / "bd", "../land/sub", target_is_directory=True)
        git(kho, "add", "-A")
        git(kho, "commit", "-q", "-m", "PR day du: symlink hop le")
        goc = git(kho, "rev-parse", "HEAD").stdout.decode().strip()
        bang(all((kho / d).is_symlink() and (kho / d).exists() for d in SYMLINK_GOC),
             "fixture vo hieu: moi symlink tren goc phai HOP LE (khong thi ca nay do mot cay da hong san)")
        qua_bd = kho / "ops" / "specs" / "bd" / "l"
        bang(os.path.exists(qua_bd) and not os.path.exists(os.path.normpath(os.path.join(qua_bd.parent, os.readlink(qua_bd)))),
             "fixture vo hieu: symlink qua bi danh phai HOP LE theo nhan nhung TREO theo ghep tu vung")
        git(kho, "checkout", "-q", "-b", "doi-chung", goc)
        viet(kho, "ops/specs/E.md", "# e2\n")
        git(kho, "commit", "-q", "-am", "PR ho so sua tep khac")
        dau0 = git(kho, "rev-parse", "HEAD").stdout.decode().strip()
        rac = (kho / ".git" / "zz-treo", kho / "docs" / "__pycache__" / "zz", kho / "docs" / "zz.pyc")
        for p in rac:
            _symlink(p, "khong-co-dich")
        try:
            rc0, log0 = kiem_re(m, kho, goc, dau0)
        finally:
            for p in rac:
                p.unlink()
        bang(rc0 == 0, f"doi chung (symlink van hop le; rac treo dung cho t82 bo qua) phai DAT: rc={rc0}: {log0}")
        for nhanh, (rm, mong) in NHANH_XOA.items():
            git(kho, "checkout", "-q", "-b", nhanh, goc)
            git(kho, "rm", "-q", *rm)
            git(kho, "commit", "-q", "-m", "PR ho so xoa")
            dau = git(kho, "rev-parse", "HEAD").stdout.decode().strip()
            bang(phan_loai_that(m, kho, goc, dau)[0] == m.DUONG_NHANH, f"fixture vo hieu ({nhanh}): PR phai ra duong nhanh")
            bang(mong not in git(kho, "diff", "--name-only", f"{goc}...{dau}").stdout.decode().split("\n")
                 and os.path.islink(kho / mong) and not os.path.exists(kho / mong),
                 f"fixture vo hieu ({nhanh}): {mong} phai TREO tren dia ma KHONG nam trong diff")
            rc, log = kiem_re(m, kho, goc, dau)
            treo = [d for d in log.splitlines() if "symlink TREO trong cay" in d]
            bang(rc == 1 and len(treo) == 1 and repr(mong) in treo[0],
                 f"{nhanh}: symlink {mong!r} treo NGOAI diff phai DO kiem-re, dung mot dong: rc={rc}: {log}")


def loi_goi_copytree_t82(nguon):
    """(mau bo qua | None, [ly do lech]) cua loi goi `copytree` DUY NHAT trong ham `t82_*` cua `nguon`. Danh sach CHO PHEP
    cach goi: dung hai doi so vi tri (nguon, dich), khong doi so sao, dung mot tu khoa `ignore=` la `ignore_patterns(<hang>...)`.
    Moi tham so khac (`symlinks`, `ignore_dangling_symlinks`, `copy_function`, `**`, doi so vi tri thu ba = `symlinks`...) doi
    ngu nghia ma `kiem_symlink_treo_ca_cay` mo phong (theo symlink, vap o symlink treo, mo va doc tung tep) nen la LECH."""
    cay = ast.parse(nguon)
    t82 = [n for n in cay.body if isinstance(n, ast.FunctionDef) and n.name.startswith("t82_")]
    if len(t82) != 1:
        return None, [f"phai co dung mot ham t82_, thay {len(t82)}"]
    chep = [n for n in ast.walk(t82[0]) if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute) and n.func.attr == "copytree"]
    if len(chep) != 1:
        return None, [f"t82 phai co dung mot copytree, thay {len(chep)}"]
    goi, lech = chep[0], []
    if len(goi.args) != 2 or any(isinstance(a, ast.Starred) for a in goi.args):
        lech.append(f"doi so vi tri phai DUNG (nguon, dich), khong sao: {ast.unparse(goi)}")
    kw = {k.arg: k.value for k in goi.keywords}
    if set(kw) != {"ignore"}:
        lech.append(f"tu khoa phai DUNG ignore=: {sorted(map(str, kw))}")
    mau = kw.get("ignore")
    if not (isinstance(mau, ast.Call) and getattr(mau.func, "attr", None) == "ignore_patterns" and not mau.keywords
            and all(isinstance(a, ast.Constant) for a in mau.args)):
        return None, lech + [f"ignore= phai la ignore_patterns(<hang>...): {ast.unparse(goi)}"]
    return tuple(a.value for a in mau.args), lech


def mau_bo_qua_t82():
    """Mau bo qua doc tu CHINH `t82` (khong tu san pham): fixture do `t82` bang du lieu cua `t82`."""
    mau, lech = loi_goi_copytree_t82((ROOT_THAT / "ops" / "lease_publish_test.py").read_text(encoding="utf-8"))
    if mau is None:
        raise RuntimeError(f"ha tang: khong doc duoc mau bo qua cua t82: {lech}")
    return mau


def chep_nhu_t82(kho):
    """`copytree` THAT, dung cach goi cua `t82` (khong `symlinks=True`, mau bo qua cua `t82`) => "CHEP_DUOC" hoac "VAP"."""
    dich = Path(tempfile.mkdtemp(prefix="cdn_t82_"))
    try:
        shutil.copytree(kho, dich / "ban", ignore=shutil.ignore_patterns(*mau_bo_qua_t82()))
        return "CHEP_DUOC"
    except shutil.Error:
        return "VAP"
    finally:
        shutil.rmtree(dich, ignore_errors=True)


LOAI_DONG_CAY = (("symlink TREO trong cay", "TREO"), ("VONG symlink thu muc", "VONG"), ("khong phai tep thuong", "LA"))


def phan_dong(loi):
    """[(loai, duong tuong doi)] cua tung dong `kiem_symlink_treo_ca_cay`; dong khong khop loai nao => ("?", dong)."""
    ra = []
    for x in loi:
        loai = next((ten for tien_to, ten in LOAI_DONG_CAY if x.startswith(tien_to)), None)
        ra.append((loai, ast.literal_eval(x.rsplit(": ", 1)[-1])) if loai else ("?", x))
    return ra


NEN_DIA = {"README.md": "x\n", "ops/specs/E.md": "# e\n", "ops/land/x.yaml": "a: 1\n"}


@ca
def t20zj_symlink_treo_khong_duyet_duoc_va_dong_bo_t82():
    """Hai chot con lai cua `kiem_symlink_treo_ca_cay`: (a) `os.walk` loi (thu muc khong doc duoc) => KHONG DO DUOC, khong nuot;
    (b) tap bo qua phai BANG DUNG tap `t82` bo qua, va CACH GOI `copytree` cua `t82` phai nam trong danh sach cho phep
    (`loi_goi_copytree_t82`) — doc lai tu chinh `ops/lease_publish_test.py` (kho that: ban sao toi thieu cua dot bien chi co
    tep cho). Cross-review luot 17 dong theo lop o luot 18: chot nay mo phong ca `followlinks`, vap o symlink treo lan mo va
    doc tung tep — them BAT KY tham so nao cho `copytree` cua `t82` (khong chi `symlinks=True`) la doi ngu nghia ay. (c) tu
    kiem bo doc cach goi: moi cach goi lech mot mau phai bi bao, cach goi dung thi khong."""
    m = nap_module()
    loi = m.kiem_symlink_treo_ca_cay(Path(tempfile.gettempdir()) / "cdn-khong-ton-tai-4f1c")
    bang(len(loi) == 1 and "KHONG DO DUOC" in loi[0], f"khong duyet duoc cay phai DO (khong nuot loi os.walk), duoc {loi}")
    mau, lech = loi_goi_copytree_t82((ROOT_THAT / "ops" / "lease_publish_test.py").read_text(encoding="utf-8"))
    bang(not lech and mau == tuple(m.BO_QUA_NHU_T82),
         f"tap bo qua lech t82 hoac cach goi copytree cua t82 doi ngu nghia: t82={mau} lech={lech} vs {m.BO_QUA_NHU_T82}")
    khung = 'def t82_x():\n    shutil.copytree({})\n'
    dung = 'HERE.parent, goc, ignore=shutil.ignore_patterns(".git", "__pycache__", "*.pyc")'
    _, lech0 = loi_goi_copytree_t82(khung.format(dung))
    bang(not lech0, f"doi chung: cach goi DUNG nhu t82 khong duoc bi bao lech: {lech0}")
    for ten, doi in (("symlinks", dung + ", symlinks=True"), ("ignore_dangling_symlinks", dung + ", ignore_dangling_symlinks=True"),
                     ("copy_function", dung + ", copy_function=shutil.copy"), ("**", dung + ", **kw"),
                     ("vi tri thu ba", dung.replace("goc, ", "goc, True, ")), ("sao", dung.replace("goc, ", "*goc, "))):
        _, l = loi_goi_copytree_t82(khung.format(doi))
        bang(l, f"cach goi copytree doi ngu nghia ({ten}) phai bi bao LECH: {doi}")


# Lop `buoc-bi-bo-doc-ca-cay-khong-chi-ba-ca` (cross-review luot 17 mo lai; luot 18 dong THEO LOP): bat bien la bo duyet cua
# `kiem_symlink_treo_ca_cay` di DUNG nhung duong `t82` di. Moi cho hai ben co the lech la mot ca rieng — `t20zk` bi danh thu
# muc · `t20zl` mau bo qua ap theo ten muc o moi cap · `t20zm` vong · `t20zn` chuoi khong vong · `t20zo` la khong phai tep
# thuong · `t20zj` cach goi copytree cua `t82` — moi chot mot dot bien rieng. Moi fixture tu chung minh `t82` VAP hay CHEP_DUOC
# bang `copytree` THAT voi mau bo qua doc tu CHINH `t82` (`chep_nhu_t82`), roi doi ket qua cua chot KHOP tung dong.
@ca
def t20zk_kiem_re_symlink_treo_qua_bi_danh_thu_muc_do():
    """Cross-review luot 17 (`buoc-bi-bo-doc-ca-cay-khong-chi-ba-ca`, duong vao BI DANH THU MUC): `t82` copytree KHONG
    `symlinks=True` nen THEO symlink thu muc, con `os.walk` mac dinh thi khong. Symlink treo nam trong thu muc ten bi bo qua
    (`*.pyc`, `__pycache__`), chi voi toi qua mot bi danh thu muc TRONG cay => `t82` vap, kiem-re phai DO. Mau bo qua ap len
    TEN MUC cua bi danh, KHONG len ten DICH: moi ten dich mot nhanh con (dot bien ap mau len ten dich chi lam DO dung nhanh ay).
    Doi chung: khong bi danh (ca hai cung bo qua thu muc ay), hoac PR sua tep khac => DAT. Bien the bi danh tro RA NGOAI cay
    cung co che nay; ca rieng can dung mot symlink tro ra ngoai kho tam nen KHONG dung o day — de lai cho phien dieu phoi soan."""
    m = nap_module()
    for ten_tm, co_bi_danh in (("kho.pyc", True), ("__pycache__", True), ("kho.pyc", False)):
        nhan = f"{ten_tm}, bi danh={co_bi_danh}"
        with kho_that(nen={"README.md": "x\n", f"ops/land/{ten_tm}/f.yaml": "a: 1\n", "ops/specs/E.md": "# e\n"}) as (kho, _a, _h):
            git(kho, "checkout", "-q", "main")
            (kho / "ops" / "land" / ten_tm / "s").symlink_to("f.yaml")
            if co_bi_danh:
                (kho / "ops" / "land" / "bd").symlink_to(ten_tm)
            git(kho, "add", "-A", "-f")
            git(kho, "commit", "-q", "-m", "PR day du: symlink hop le")
            goc = git(kho, "rev-parse", "HEAD").stdout.decode().strip()
            bang(chep_nhu_t82(kho) == "CHEP_DUOC", f"fixture vo hieu ({nhan}): t82 phai chep duoc cay goc")
            git(kho, "checkout", "-q", "-b", "doi-chung", goc)
            viet(kho, "ops/specs/E.md", "# e2\n")
            git(kho, "commit", "-q", "-am", "PR ho so sua tep khac")
            rc0, log0 = kiem_re(m, kho, goc, git(kho, "rev-parse", "HEAD").stdout.decode().strip())
            bang(rc0 == 0, f"doi chung ({nhan}, PR sua tep khac) phai DAT: rc={rc0}: {log0}")
            git(kho, "checkout", "-q", "-b", "xoa", goc)
            git(kho, "rm", "-q", f"ops/land/{ten_tm}/f.yaml")
            git(kho, "commit", "-q", "-m", "PR ho so xoa dich")
            dau = git(kho, "rev-parse", "HEAD").stdout.decode().strip()
            bang(phan_loai_that(m, kho, goc, dau)[0] == m.DUONG_NHANH, f"fixture vo hieu ({nhan}): PR phai ra duong nhanh")
            bang(chep_nhu_t82(kho) == ("VAP" if co_bi_danh else "CHEP_DUOC"),
                 f"fixture vo hieu ({nhan}): t82 phai vap KHI VA CHI KHI co bi danh")
            rc, log = kiem_re(m, kho, goc, dau)
            treo = [d for d in log.splitlines() if "symlink TREO trong cay" in d]
            if co_bi_danh:
                bang(rc == 1 and len(treo) == 1 and repr("ops/land/bd/s") in treo[0],
                     f"{nhan}: symlink treo chi voi toi qua bi danh thu muc phai DO kiem-re, dung mot dong: rc={rc}: {log}")
            else:
                bang(rc == 0, f"doi chung ({nhan}): khong bi danh thi t82 va kiem-re cung bo qua thu muc ay, phai DAT: rc={rc}: {log}")


@ca
def t20zl_mau_bo_qua_ap_theo_ten_muc_o_moi_cap_nhu_t82():
    """Duong vao THU TU AP MAU BO QUA: `t82` goi `ignore` voi TEN MUC o MOI cap no vao, ke ca cap o sau mot bi danh, va mot bi
    danh mang ten bi bo qua thi `t82` khong theo. Ap hep hon (khong ap sau bi danh, hay theo bi danh ten bi bo qua) la DO oan
    dung cay `t82` chep duoc — chot nay doi DAT tren cay ay. Nhanh: symlink treo trong `sub.pyc/` va `__pycache__/` chi voi
    toi qua bi danh `bd`, `bd2`; bi danh `bd.pyc` va `__pycache__` (ten bi bo qua) tro vao thu muc chua symlink treo."""
    m = nap_module()
    with _cay_tam(NEN_DIA) as kho:
        land = kho / "ops" / "land"
        for tm in ("kho.pyc/sub.pyc", "that/__pycache__", "tm.pyc"):
            (land / tm).mkdir(parents=True)
            (land / tm / "s").symlink_to("khong-co")
        (land / "bd").symlink_to("kho.pyc")
        (land / "bd2").symlink_to("that")
        (land / "bd.pyc").symlink_to("tm.pyc")
        (land / "__pycache__").symlink_to("tm.pyc")
        bang(chep_nhu_t82(kho) == "CHEP_DUOC", "fixture vo hieu: t82 phai chep duoc (moi symlink treo nam duoi ten bi bo qua)")
        loi = m.kiem_symlink_treo_ca_cay(kho)
        bang(loi == [], f"t82 chep duoc thi chot phai DAT (mau bo qua ap theo TEN MUC o moi cap, ke ca sau bi danh): {loi}")


CON_DUYET_CAY = ("import importlib.util, json, sys\n"
                 "s = importlib.util.spec_from_file_location('m', sys.argv[1]); m = importlib.util.module_from_spec(s)\n"
                 "s.loader.exec_module(m); print(json.dumps(m.kiem_symlink_treo_ca_cay(sys.argv[2])))\n")


@ca
def t20zm_vong_symlink_thu_muc_do_va_khong_bung_no():
    """Duong vao VONG: `t82` theo vong toi khi nhan tu choi phan giai duong dan, roi vap; chot phai DO NGAY o bi danh khep
    vong — so danh tinh `(st_dev, st_ino)` voi TO TIEN tren chinh duong dang duyet — khong lap. Nhanh, theo thu tu: (i) doi
    chung bi danh KHONG vong toi thu muc anh em => DAT (so voi "da tham" toan cuc la DO oan); (ii) tu vong `vong -> .`;
    (iii) vong ve GOC `len -> ../..` (so moi thu muc cha la sot); (iv) vong hai buoc qua thu muc anh em; (v) khong lay duoc
    danh tinh mot thu muc => KHONG DO DUOC; (vi) HAI vong ve goc — `t82` khong ket thuc (do ngoai suite tren 41508cd cong ban
    va goi y luot 17: qua han 15 s, bo duyet chi theo symlink cung qua han) — chot chay trong tien trinh con co tran thoi gian,
    phai ra dung hai dong VONG. (vi) dung CUOI: dot bien go chot vong lam (ii) DO truoc khi toi day."""
    m = nap_module()
    with _cay_tam(dict(NEN_DIA, **{"ops/specs/a/x.md": "x\n"})) as kho:
        _symlink(kho / "ops" / "land" / "al", "../specs/a", target_is_directory=True)
        bang(chep_nhu_t82(kho) == "CHEP_DUOC", "fixture vo hieu: bi danh khong vong thi t82 phai chep duoc")
        loi = m.kiem_symlink_treo_ca_cay(kho)
        bang(loi == [], f"doi chung: bi danh KHONG vong toi thu muc anh em la duong t82 di binh thuong, phai DAT: {loi}")
    for nhan, tao, mong in (
            ("tu vong", {"ops/specs/vong": "."}, [("VONG", "ops/specs/vong")]),
            ("vong ve goc", {"ops/specs/len": "../.."}, [("VONG", "ops/specs/len")]),
            ("vong hai buoc", {"ops/specs/a/sang": "../b", "ops/specs/b/ve": "../a"},
             [("VONG", "ops/specs/a/sang/ve"), ("VONG", "ops/specs/b/ve/sang")])):
        with _cay_tam(NEN_DIA) as kho:
            for duong, dich in tao.items():
                _symlink(kho / duong, dich, target_is_directory=True)
            bang(chep_nhu_t82(kho) == "VAP", f"fixture vo hieu ({nhan}): vong symlink thu muc phai lam t82 vap")
            loi = m.kiem_symlink_treo_ca_cay(kho)
            bang(phan_dong(loi) == mong, f"{nhan}: chot phai DO dung o bi danh khep vong, moi vong mot dong VONG: {loi}")
    with _cay_tam(NEN_DIA) as kho:
        dich_hong = os.path.join(os.fspath(kho), "ops", "specs")
        that = os.stat

        def stat_gia(p, *a, **k):
            if os.fspath(p) == dich_hong:
                raise PermissionError(13, "gia: khong stat duoc", os.fspath(p))
            return that(p, *a, **k)
        with mock.patch.object(os, "stat", stat_gia):
            loi = m.kiem_symlink_treo_ca_cay(kho)
        bang(len(loi) == 1 and loi[0].startswith("KHONG DO DUOC") and repr(dich_hong) in loi[0],
             f"khong lay duoc danh tinh mot thu muc phai la KHONG DO DUOC, dung mot dong: {loi}")
    with _cay_tam(NEN_DIA) as kho:
        _symlink(kho / "ops" / "specs" / "len", "../..", target_is_directory=True)
        _symlink(kho / "ops" / "land" / "len", "../..", target_is_directory=True)
        try:
            r = subprocess.run([sys.executable, "-B", "-c", CON_DUYET_CAY, str(CAY / "ops" / "ci_duong_nhanh.py"), str(kho)],
                               capture_output=True, timeout=60)
        except subprocess.TimeoutExpired:
            r = None
        bang(r is not None, "hai vong ve goc: chot khong ket thuc trong tran thoi gian (phai DO ngay o bi danh khep vong)")
        loi = json.loads(r.stdout.decode("utf-8")) if r.returncode == 0 else [f"tien trinh con rc={r.returncode}"]
        bang(phan_dong(loi) == [("VONG", "ops/land/len"), ("VONG", "ops/specs/len")],
             f"hai vong ve goc: phai dung hai dong VONG: {loi}")


@ca
def t20zn_chuoi_symlink_khong_vong_qua_gioi_han_phan_giai_do():
    """Duong vao KHU TRUNG: chuoi bi danh KHONG vong (moi `d_i/l` tro toi thu muc KE TIEP cua chuoi) du dai de nhan tu choi phan giai duong dan di qua ca
    chuoi. `t82` di dung duong ay va vap; chot cung phai DO, dung mot dong TREO tai phan tu nhan tu choi. Chot KHONG duoc khu
    trung thu muc "da tham": khi thu tu ten dua thu muc cuoi chuoi toi TRUOC (nhanh `nguoc`), tap da tham toan cuc bo qua
    duong dai va lot. Moi thu tu ten la mot nhanh; nhanh xuoi la doi chung cho thay loi khu trung chi lo theo thu tu."""
    m = nap_module()
    so_pt = 65 if sys.platform == "win32" else 42
    for nhan, nguoc in (("xuoi", False), ("nguoc", True)):
        with _cay_tam(NEN_DIA) as kho:
            ten = [f"d{i:02d}" for i in range(so_pt)]
            if nguoc:
                ten.reverse()
            c = kho / "ops" / "specs" / "c"
            for t in ten:
                (c / t).mkdir(parents=True)
            for a, b in zip(ten, ten[1:]):
                _symlink(c / a / "l", f"../{b}", target_is_directory=True)
            bang(chep_nhu_t82(kho) == "VAP", f"fixture vo hieu ({nhan}): chuoi phai qua gioi han phan giai, t82 phai vap")
            pd = phan_dong(m.kiem_symlink_treo_ca_cay(kho))
            bang(len(pd) == 1 and pd[0][0] == "TREO" and re.fullmatch(rf"ops/specs/c/{ten[0]}(?:/l)+", pd[0][1]),
                 f"{nhan}: chuoi khong vong qua gioi han phan giai phai DO, dung mot dong TREO tu dau chuoi: {pd}")


def _tao_socket(thu_muc, ten):
    """Socket UNIX tai `thu_muc/ten`; bind bang ten TUONG DOI vi duong dan socket co tran do dai."""
    cu = os.getcwd()
    os.chdir(thu_muc)
    try:
        s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        try:
            s.bind(ten)
        finally:
            s.close()
    finally:
        os.chdir(cu)


# WP748 r6/g6 (Windows native, do 14-10-2026 tai 397fc2a: `os.mkfifo` va `socket.AF_UNIX` KHONG ton tai => t20zo HONG
# AttributeError) — fix: FIFO tren Windows la symlink toi mot named pipe `\\.\pipe\...` dang mo. Do tai cho: `os.stat` theo
# symlink tra S_IFIFO, `os.path.isfile` False. Moi lan stat MO mot dau client va tieu mot instance (het instance => loi "All
# pipe instances are busy" => `exists` False => doc nham thanh TREO), nen giu SO_INSTANCE_ONG du rong cho mot nhanh.
# Ong PIPE_ACCESS_INBOUND (khach chi GHI): `copy2` cua t82 thu CopyFile2 => ERROR_ACCESS_DENIED => lui ve `copyfile` =>
# stat S_IFIFO => `SpecialFileError` "is a named pipe" — VAP DUNG ly do loai tep nhu posix (do 14-10-2026 tai 397fc2a, ca ba
# hinh dang FIFO, 64 instance: VAP "named pipe" ca lan 1 lan lan 2; chot ra `LA`). Ong DUPLEX thi CopyFile2 CHEP DUOC.
# Duoi ~8 instance (do 14-10-2026 tai 397fc2a) thi VAP doi sang "All pipe instances are busy" (sai ly do) va chot doc thanh TREO.
SO_INSTANCE_ONG = 64


def _tao_fifo(duong, don):
    """La FIFO THAT tai `duong`: posix `mkfifo`; Windows symlink toi named pipe, handle server dong khi `don` (ExitStack) dong."""
    if hasattr(os, "mkfifo"):
        os.mkfifo(duong)
        return
    import _winapi
    import uuid
    ong = "\\\\.\\pipe\\cdn-t20zo-" + uuid.uuid4().hex
    for _ in range(SO_INSTANCE_ONG):
        h = _winapi.CreateNamedPipe(ong, _winapi.PIPE_ACCESS_INBOUND, 0, _winapi.PIPE_UNLIMITED_INSTANCES, 0, 0, 0, _winapi.NULL)
        don.callback(_winapi.CloseHandle, h)
    os.symlink(ong, duong)


@ca
def t20zo_la_khong_phai_tep_thuong_do():
    """Duong vao LA: `t82` MO va DOC tung tep (copy2) — FIFO nem `SpecialFileError`, socket nem `OSError` — nen moi la ma no
    toi duoc, sau khi theo symlink, phai la TEP THUONG (danh sach CHO PHEP). Nhanh, moi nhanh mot dong LA dung duong dan:
    FIFO · socket · symlink toi FIFO nam trong thu muc ten bi bo qua (doc la THEO symlink) · FIFO chi voi toi qua bi danh thu
    muc. Doi chung: tep thuong va symlink toi tep thuong => DAT.
    Windows (khong mkfifo/AF_UNIX): FIFO = named pipe INBOUND THAT (`_tao_fifo`); tien de "t82 phai vap" GIU NGUYEN, vap vi
    "is a named pipe" (xem SO_INSTANCE_ONG). Socket: socket AF_UNIX THAT tren Windows (WinSock family 1 do tai 397fc2a, bind qua
    ws2_32; do 14-10-2026) la reparse point 0x80000023 ma `os.stat` tra S_IFREG, `isfile` True, `copytree` CHEP DUOC: tien de
    "t82 vap" KHONG dung duoc bang socket that. Nhanh socket Windows duoi day theo ngoai le chu kho
    duyet (comment 6171400658): ong THAT de t82 vap + GIA `os.stat` S_IFSOCK CHI cho dung leaf `sk`, tuc do LOGIC danh sach cho
    phep cua bo kiem, KHONG phai bang chung tao hay tu choi socket THAT tren Windows; posix van dung FIFO va socket AF_UNIX THAT."""
    m = nap_module()
    with _cay_tam(NEN_DIA) as kho:
        (kho / "ops" / "land" / "sx").symlink_to("x.yaml")
        bang(chep_nhu_t82(kho) == "CHEP_DUOC", "fixture vo hieu: tep thuong va symlink toi tep thuong thi t82 chep duoc")
        loi = m.kiem_symlink_treo_ca_cay(kho)
        bang(loi == [], f"doi chung: tep thuong va symlink toi tep thuong phai DAT: {loi}")

    def fifo(land, don):
        _tao_fifo(land / "p", don)
        return land / "p", None

    def sock(land, don):
        if hasattr(socket, "AF_UNIX"):
            _tao_socket(land, "sk")
            return land / "sk", None
        _tao_fifo(land / "sk", don)
        return land / "sk", land / "sk"

    def symlink_toi_fifo(land, don):
        (land / "kho.pyc").mkdir()
        _tao_fifo(land / "kho.pyc" / "p", don)
        _symlink(land / "sp", "kho.pyc/p")
        return land / "sp", None

    def fifo_qua_bi_danh(land, don):
        (land / "kho.pyc").mkdir()
        _tao_fifo(land / "kho.pyc" / "p", don)
        _symlink(land / "bd", "kho.pyc", target_is_directory=True)
        return land / "bd" / "p", None
    for nhan, tao, mong in (("FIFO", fifo, "ops/land/p"), ("socket", sock, "ops/land/sk"),
                            ("symlink toi FIFO", symlink_toi_fifo, "ops/land/sp"),
                            ("FIFO qua bi danh", fifo_qua_bi_danh, "ops/land/bd/p")):
        with _cay_tam(NEN_DIA) as kho, contextlib.ExitStack() as don:
            la, gia_sock = tao(kho / "ops" / "land", don)
            bang(chep_nhu_t82(kho) == "VAP", f"fixture vo hieu ({nhan}): t82 phai vap")
            if gia_sock is None:
                loi = m.kiem_symlink_treo_ca_cay(kho)
            else:
                dich_gia, that = os.path.normcase(os.fspath(gia_sock)), os.stat

                def stat_sock(p, *a, **k):
                    if os.path.normcase(os.path.abspath(os.fspath(p))) == dich_gia:
                        return os.stat_result((stat.S_IFSOCK | 0o644, 0, 0, 1, 0, 0, 0, 0, 0, 0))
                    return that(p, *a, **k)
                with mock.patch.object(os, "stat", stat_sock):
                    loi = m.kiem_symlink_treo_ca_cay(kho)
            bang(phan_dong(loi) == [("LA", mong)], f"{nhan}: la khong phai tep thuong phai DO, dung mot dong: {loi}")


@ca
def t20r_kiem_re_dau_xung_dot_moi_duoi_tep_do():
    """Cross-review luot 8: t20c chi co dau xung dot trong `.md`; `--check` thu hep ve `*.md` van xanh. Tep KHONG phai
    YAML (kiem_yaml khong bat ho) phai tu DO qua diff --check."""
    m = nap_module()
    for duong in ("ops/reviews/goi-y.patch", "ops/land/ghi.json", "ops/specs/ghi.txt"):
        with kho_that(nhanh_pr={duong: "a\n<<<<<<< HEAD\nb\n=======\nc\n>>>>>>> nhanh\n"}) as (kho, goc, dau):
            rc, log = kiem_re(m, kho, goc, dau)
            bang(rc == 1 and "diff --check" in log and duong in log, f"{duong}: dau xung dot phai DO qua diff --check: rc={rc}: {log}")


@ca
def t20o_kiem_re_yaml_nhieu_tai_lieu_hong_o_sau_do():
    """Cross-review luot 7 (P2 `kiem-re-cua-fail-close-chua-co-ca`): tai lieu DAU hop le, tai lieu SAU hong — kiem_yaml
    phai tieu thu HET `safe_load_all`, khong chi lay tai lieu dau."""
    m = nap_module()
    with kho_that(nhanh_pr={"ops/land/nhieu.yaml": "a: 1\n---\nb: [1, 2\n"}) as (kho, goc, dau):
        rc, log = kiem_re(m, kho, goc, dau)
        bang(rc == 1 and "YAML khong parse duoc" in log and "nhieu.yaml" in log, f"tai lieu sau hong phai DO: rc={rc}: {log}")


@ca
def t23_fixture_sach_khong_phu_thuoc_actor_ci():
    """Cross-review luot 2 (P2): selftest chay tren MOI PR — actor khac nguoi cap lease khong duoc lam fixture SACH do oan.
    Hai duong vao: chon fixture trong tien trinh (mock.patch.dict) va validator con (loc o `_env_git`)."""
    truoc = os.environ.get("GITHUB_ACTOR")
    os.environ["GITHUB_ACTOR"] = "notebyme88"
    try:
        try:
            lease_that_het_han_hop_le()
        except KhongCoFixture as e:
            raise TinHieuChotCa(f"duoi actor la khong chon duoc fixture sach: {e}") from e
        t20a_kiem_re_ho_so_sach_dat()
        t20d_kiem_re_khoang_trang_cuoi_dong_khong_do()
    finally:
        if truoc is None:
            os.environ.pop("GITHUB_ACTOR", None)
        else:
            os.environ["GITHUB_ACTOR"] = truoc
    bang(os.environ.get("GITHUB_ACTOR") == truoc, "actor cua tien trinh cha phai duoc khoi phuc")


@ca
def t22b_ca_du_lieu_phai_thuc_thi_tung_ca():
    """Cross-review luot 2 (P2): t22 chi do argv/rc qua do gia. O day ba ham gia mang DUNG TEN; moi lan chi MOT ham ne
    sentinel, qua chinh subprocess cua checker: no-call, bo tung ten, cwd sai deu phai lam ca nay do."""
    m = nap_module()
    with tempfile.TemporaryDirectory(prefix="cdn_data_calls_") as d:
        goc = Path(d)
        (goc / "ops").mkdir()
        for dich in CA_DU_LIEU_CHUAN:
            marker = "CHOT_DU_LIEU_" + dich
            (goc / "ops" / "lease_publish_test.py").write_text("\n".join(
                "def " + ten + "():\n    " + ("raise AssertionError(" + repr(marker) + ")" if ten == dich else "pass")
                for ten in CA_DU_LIEU_CHUAN) + "\n", encoding="utf-8")
            loi = m.kiem_ca_du_lieu(goc, chay_that)
            bang(len(loi) == 1 and marker in loi[0], f"{dich}: ca do phai thuc su duoc GOI va truyen loi, duoc {loi}")


@ca
def t22_ca_du_lieu_thay_bo_lease_publish_selftest():
    """Bo `lease-publish selftest` lam mat t23/t26/t27 (doc CAY that). kiem-re giu ba ca do; chay that tren kho that."""
    m = nap_module()
    bang(tuple(m.CA_DU_LIEU) == CA_DU_LIEU_CHUAN, f"danh sach ca du lieu sai: {m.CA_DU_LIEU}")
    bang(m.kiem_ca_du_lieu(ROOT_THAT, chay_that) == [], "ba ca du lieu phai DAT tren kho that")
    log = []
    bang(m.kiem_ca_du_lieu(ROOT_THAT, chay_gia(log=log)) == [], "chay gia rc=0 khong loi")
    bang(len(log) == 1 and log[0][-3:] == list(m.CA_DU_LIEU) and "ops/lease_publish_test.py" in log[0],
         f"lenh phai truyen du ba ten ca cua ops/lease_publish_test.py: {log}")
    loi = m.kiem_ca_du_lieu(ROOT_THAT, chay_gia(b"CA DO", rc=1))
    bang(len(loi) == 1 and "rc=1" in loi[0], f"ca du lieu do phai thanh loi: {loi}")
    loi = m.kiem_ca_du_lieu(ROOT_THAT, chay_gia(nem=SuDoGia("no")))
    bang(len(loi) == 1 and "KHONG DO DUOC" in loi[0], f"ngoai le khi chay ca du lieu phai thanh loi KHONG DO DUOC: {loi}")


@ca
def t21_kiem_lease_phan_biet_con_han_het_han_va_duoi_tep():
    """Lease CON HAN (hoac han khong doc duoc) => `lease_publish.py check`; HET HAN => kiem(bo_qua_han=True) qua `-c`.
    Ca hai duoi `.yaml`/`.yml`; tep da xoa va tep khong phai yaml bi bo qua. KHONG co nhanh nao la 'khong kiem'."""
    m = nap_module()
    tam = Path(tempfile.mkdtemp(prefix="cdn_lease_"))
    try:
        viet(tam, "ops/leases/het.yaml", LEASE_HET_HAN)
        viet(tam, "ops/leases/het2.yml", LEASE_HET_HAN)
        viet(tam, "ops/leases/con.yaml", LEASE_CON_HAN_THIEU)
        viet(tam, "ops/leases/con2.yml", LEASE_CON_HAN_THIEU)
        viet(tam, "ops/leases/hong-han.yaml", "lease_id: x\nlease_expires_at_utc: 'khong-phai-ngay'\n")
        viet(tam, "ops/leases/khong-han.yaml", "lease_id: y\n")
        doi = {"ops/leases/het.yaml", "ops/leases/het2.yml", "ops/leases/con.yaml", "ops/leases/con2.yml",
               "ops/leases/hong-han.yaml", "ops/leases/khong-han.yaml", "ops/leases/da-xoa.yaml", "ops/leases/ghi-chu.md"}
        log = []
        bo_dem = tempfile.TemporaryFile("w+", encoding="utf-8")
        loi = m.kiem_lease(doi, tam, chay_gia(log=log), None, bo_dem)
        het = sorted(a[-1] for a in log if a[1:3] == ["-B", "-c"])
        con = sorted(a[3] for a in log if a[1:3] == ["ops/lease_publish.py", "check"])
        bang(het == ["ops/leases/het.yaml", "ops/leases/het2.yml"], f"lease HET HAN phai qua kiem(bo_qua_han): {het}")
        bang(con == ["ops/leases/con.yaml", "ops/leases/con2.yml", "ops/leases/hong-han.yaml", "ops/leases/khong-han.yaml"],
             f"lease CON HAN hoac han khong doc duoc phai qua `check`: {con}")
        bang(len(log) == len(het) + len(con), f"moi lenh phai thuoc mot trong hai dang: {log}")
        bang(loi == [], f"rc=0 thi khong co loi: {loi}")
        loi2 = m.kiem_lease({"ops/leases/con.yaml"}, tam, chay_gia(rc=8), None, bo_dem)
        loi3 = m.kiem_lease({"ops/leases/het.yaml"}, tam, chay_gia(rc=8), None, bo_dem)
        bang(len(loi2) == 1 and "rc=8" in loi2[0], f"check rc!=0 phai thanh loi: {loi2}")
        bang(len(loi3) == 1 and "rc=8" in loi3[0] and "het han" in loi3[0], f"kiem het han rc!=0 phai thanh loi: {loi3}")
    finally:
        shutil.rmtree(tam, ignore_errors=True)


# LUAT (cross-review luot 16, lop `khang-dinh-dinh-tinh-rong-hon-phep-do`): pham vi bia mo ma docstring D2 cua san pham KHAI.
# Vi tri cua lease CU mang `da_bi_thay_the` -> bia mo cua `lease_publish` THAY no hay khong. Doc lai bang HANH VI, khong doc ma.
PHAM_VI_BIA_MO = {"refs/heads": True, "refs/remotes": True, "refs/tags": False, "cay lam viec": False}
CAU_PHAM_VI_BIA_MO = ("mọi ref dưới `refs/heads` và `refs/remotes`", "KHÔNG đọc tag và KHÔNG đọc cây làm việc")


def _nap_lease_publish_cua_cay():
    """`ops/lease_publish.py` cua CAY duoi do (ban sao tam cua dot bien co ban rieng), KHONG phai ban cua kho that."""
    spec = importlib.util.spec_from_file_location("lease_publish_cua_cay_duoi_do", CAY / "ops" / "lease_publish.py")
    lp = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(lp)
    return lp


@ca
def t21b_bia_mo_D2_doc_dung_pham_vi_ref_ma_docstring_khai():
    """Cross-review luot 16 (`khang-dinh-dinh-tinh-rong-hon-phep-do`): docstring D2 tung khai bia mo doc "moi REF cuc bo" trong
    khi `_cac_ref_cuc_bo` chi doc `refs/heads` + `refs/remotes`. Ca nay DO pham vi tren `lease_publish` THAT: lease cu mang
    `da_bi_thay_the` dat lan luot o nhanh, ref remote, tag, va chi tren dia (khong commit) — bia mo thay hai cho dau, khong
    thay hai cho sau — roi doi docstring san pham noi DUNG pham vi ay. Lech mot trong hai chieu (ma doi pham vi, hoac docstring
    noi rong ra) => DO. Khong noi gi ve checkout cua runner: cau ay o docstring mang nhan KHONG DO DUOC."""
    lp = _nap_lease_publish_cua_cay()
    moi = {"lease_id": "moi-t21b", "thay_the_cho": ["cu-t21b"]}
    cu = "lease_id: cu-t21b\nda_bi_thay_the: moi-t21b\n"
    thay = {}
    for vi_tri in PHAM_VI_BIA_MO:
        with tempfile.TemporaryDirectory(prefix="cdn_bia_mo_") as d:
            kho = Path(d)
            git(kho, "init", "-q", "-b", "main")
            viet(kho, "README.md", "x\n")
            git(kho, "add", "-A")
            git(kho, "commit", "-q", "-m", "nen")
            git(kho, "checkout", "-q", "-b", "tam")
            viet(kho, "ops/leases/cu-t21b.yaml", cu)
            git(kho, "add", "-A")
            git(kho, "commit", "-q", "-m", "lease cu")
            x = git(kho, "rev-parse", "HEAD").stdout.decode().strip()
            git(kho, "checkout", "-q", "main")
            git(kho, "branch", "-q", "-D", "tam")
            bang(not (kho / "ops" / "leases" / "cu-t21b.yaml").exists(), f"fixture vo hieu ({vi_tri}): main khong duoc co lease cu")
            if vi_tri == "cay lam viec":
                viet(kho, "ops/leases/cu-t21b.yaml", cu)
            else:
                git(kho, "update-ref", {"refs/heads": "refs/heads/ops/x", "refs/remotes": "refs/remotes/origin/ops/x",
                                        "refs/tags": "refs/tags/t-bia-mo"}[vi_tri], x)
            with mock.patch.dict(os.environ, _env_git(), clear=True):
                try:
                    lp._kiem_bia_mo(moi, str(kho / "ops" / "leases" / "moi-t21b.yaml"), str(kho))
                    thay[vi_tri] = True
                except lp.Chan as e:
                    thay[vi_tri] = False if e.ma == lp.RC_NOI_DUNG and "da_bi_thay_the" in e.thong_diep else f"Chan la: {e}"
    bang(thay == PHAM_VI_BIA_MO, f"pham vi bia mo cua lease_publish lech LUAT ma docstring D2 khai: do {thay}, luat {PHAM_VI_BIA_MO}")
    doc = " ".join((ast.get_docstring(ast.parse((CAY / "ops" / "ci_duong_nhanh.py").read_text(encoding="utf-8"))) or "").split())
    thieu = [c for c in CAU_PHAM_VI_BIA_MO if c not in doc]
    bang(not thieu, f"docstring D2 phai noi DUNG pham vi bia mo da do, thieu: {thieu}")


# Cross-review luot 7 (lop kiem-re-cua-fail-close-chua-co-ca): moi CUA cua ba helper kiem-re mot chot rieng,
# do tren HANH VI (dau vao that/do gia), khong do chuoi. Moi ca co dot bien dich rieng trong DOT_BIEN.
@contextlib.contextmanager
def _cay_tam(tep):
    tam = Path(tempfile.mkdtemp(prefix="cdn_cua_"))
    try:
        for d, nd in tep.items():
            viet(tam, d, nd)
        yield tam
    finally:
        shutil.rmtree(tam, ignore_errors=True)


@ca
def t20h_kiem_yaml_duoi_yml_ngoai_lease_do():
    m = nap_module()
    with _cay_tam({"ops/land/hong.yml": "a: [1, 2\n"}) as tam:
        loi = m.kiem_yaml({"ops/land/hong.yml"}, tam)
        bang(len(loi) == 1 and "hong.yml" in loi[0], f"`.yml` ngoai lease hong phai thanh loi YAML, duoc {loi}")


@ca
def t20i_tep_da_xoa_khong_cat_vong_kiem_yaml():
    m = nap_module()
    with _cay_tam({"ops/land/b-hong.yaml": "a: [1, 2\n"}) as tam:
        loi = m.kiem_yaml({"ops/land/a-da-xoa.yaml", "ops/land/b-hong.yaml"}, tam)
        bang(len(loi) == 1 and "b-hong.yaml" in loi[0],
             f"tep da xoa xep TRUOC khong duoc cat vong: tep hong xep sau van phai thanh loi, duoc {loi}")


@ca
def t20j_thieu_pyyaml_la_khong_do_duoc():
    m = nap_module()
    with _cay_tam({"ops/land/x.yaml": "a: 1\n", "ops/leases/l.yaml": "lease_id: l\n"}) as tam:
        log = []
        with mock.patch.dict(sys.modules, {"yaml": None}):
            loi_y = m.kiem_yaml({"ops/land/x.yaml"}, tam)
            loi_l = m.kiem_lease({"ops/leases/l.yaml"}, tam, chay_gia(log=log), None, tempfile.TemporaryFile("w+"))
        bang(len(loi_y) == 1 and "KHONG DO DUOC" in loi_y[0], f"kiem_yaml thieu PyYAML phai DO, duoc {loi_y}")
        bang(len(loi_l) == 1 and "KHONG DO DUOC" in loi_l[0] and not log,
             f"kiem_lease thieu PyYAML phai DO va khong goi validator, duoc {loi_l} / {log}")


@ca
def t20k_kiem_lease_nem_va_nhieu_tai_lieu_do():
    m = nap_module()
    with _cay_tam({"ops/leases/con.yaml": LEASE_CON_HAN_THIEU, "ops/leases/hai.yaml": "lease_id: a\n---\nlease_id: b\n"}) as tam:
        bo_dem = tempfile.TemporaryFile("w+")
        loi = m.kiem_lease({"ops/leases/con.yaml"}, tam, chay_gia(nem=SuDoGia("spawn no")), None, bo_dem)
        bang(len(loi) == 1 and "KHONG DO DUOC" in loi[0], f"validator lease NEM phai thanh loi, duoc {loi}")
        bang(m.kiem_yaml({"ops/leases/hai.yaml"}, tam) == [], "fixture vo hieu: kiem_yaml (safe_load_all) phai CHO QUA tep nhieu tai lieu")
        log = []
        loi = m.kiem_lease({"ops/leases/hai.yaml"}, tam, chay_gia(log=log), None, bo_dem)
        bang(len(loi) == 1 and "khong parse duoc" in loi[0] and not log,
             f"lease NHIEU tai lieu: chi nhanh parse cua kiem_lease bat duoc, phai DO, duoc {loi} / {log}")


@ca
def t20l_han_lease_timestamp_yaml_khong_nhay_ngoac():
    """Lease that `quy-trinh-lap-review-r15-g16-claude.yaml` ghi han KHONG nhay ngoac => PyYAML tra datetime, khong phai str."""
    m = nap_module()
    with _cay_tam({"ops/leases/tran.yaml": "lease_id: t\nlease_expires_at_utc: 2020-01-01T00:00:00Z\n"}) as tam:
        log = []
        m.kiem_lease({"ops/leases/tran.yaml"}, tam, chay_gia(log=log), None, tempfile.TemporaryFile("w+"))
        bang(len(log) == 1 and log[0][1:3] == ["-B", "-c"],
             f"han datetime da qua phai di nhanh HET HAN (kiem bo_qua_han), khong phai `check`: {log}")


@ca
def t20m_diff_check_nem_hoac_git_loi_do():
    m = nap_module()
    loi = m.kiem_diff_check(env_pr(), chay_gia(nem=SuDoGia("git no")))
    bang(len(loi) == 1 and "KHONG DO DUOC" in loi[0], f"git diff --check NEM phai thanh loi, duoc {loi}")
    loi = m.kiem_diff_check(env_pr(), chay_gia(b"fatal: bad object", rc=128))
    bang(len(loi) == 1 and "rc=128" in loi[0], f"git diff --check rc=128 phai thanh loi, duoc {loi}")


# ---------------------------------------------------------------- tầng 2: cấu trúc ci.yml
class YamlKhacGitHub(ValueError):
    """Cau truc PyYAML CO THE doc KHAC GitHub (chua do tren GitHub — loader nghiem tu choi ca hai dang cho chac): khoa trung
    (PyYAML lay ban CUOI, im lang) hoac khoa gop `<<`."""


class _LoaderNghiem(yaml.SafeLoader):
    def construct_mapping(self, node, deep=False):
        for k, _ in node.value:
            if k.tag == "tag:yaml.org,2002:merge" or getattr(k, "value", None) == "<<":
                raise YamlKhacGitHub(f"khoa gop `<<` o dong {k.start_mark.line + 1}")
        thay = set()
        for k, _ in node.value:
            if k.tag == "tag:yaml.org,2002:merge":
                continue   # chi den day khi chot tren bi go (dot bien): de PyYAML gop im lang nhu ban goc cua no
            khoa = self.construct_object(k, deep=deep)
            if khoa in thay:
                raise YamlKhacGitHub(f"khoa trung {khoa!r} o dong {k.start_mark.line + 1}")
            thay.add(khoa)
        return super().construct_mapping(node, deep=deep)


def doc_wf_tu(van_ban):
    """Luot 5 (lop chot-yaml, cua 'bo phan tich cua test khac GitHub' — chua do tren GitHub): moi ca `y*` doc qua loader NGHIEM
    nay."""
    try:
        return yaml.load(van_ban, Loader=_LoaderNghiem)
    except YamlKhacGitHub as e:
        bang(False, f"ci.yml: {e} — ca `y*` co the do mot cau truc KHAC cai GitHub chay")


def doc_wf():
    return doc_wf_tu((CAY / ".github" / "workflows" / "ci.yml").read_text(encoding="utf-8"))


def chuan_hoa_if(gia_tri):
    if isinstance(gia_tri, bool):
        return str(gia_tri).lower()
    s = str(gia_tri).strip()
    m = re.fullmatch(r"\$\{\{(.*)\}\}", s, re.S)
    return re.sub(r"\s+", " ", (m.group(1) if m else s).strip())


def buoc(wf, job):
    return (wf["jobs"][job].get("steps") or [])


def ten_buoc(b):
    return b.get("name") or ""


def tim_buoc(wf, job, ten):
    r = [b for b in buoc(wf, job) if ten_buoc(b) == ten]
    bang(len(r) == 1, f"{job}: phai co DUNG MOT buoc ten {ten!r}, thay {len(r)}")
    return r[0]


@ca
def y01_chuan_bi_phan_loai_chi_pull_request_va_khong_lam_do_job():
    wf = doc_wf()
    pl = [b for b in buoc(wf, "chuan-bi") if b.get("id") == "phan-loai"]
    bang(len(pl) == 1, f"chuan-bi phai co dung mot buoc id phan-loai, thay {len(pl)}")
    b = pl[0]
    bang(chuan_hoa_if(b.get("if")) == "github.event_name == 'pull_request'",
         f"buoc phan loai phai bi chan boi `github.event_name == 'pull_request'`, if={b.get('if')!r}")
    bang(str(b.get("run", "")).strip() == "python3 ops/ci_duong_nhanh.py", f"buoc phan loai goi sai lenh: {b.get('run')!r}")
    env = b.get("env") or {}
    bang(env.get("CI_DUONG_NHANH_SU_KIEN") == "${{ github.event_name }}"
         and env.get("CI_DUONG_NHANH_GOC") == "${{ github.event.pull_request.base.sha }}"
         and env.get("CI_DUONG_NHANH_DAU") == "${{ github.event.pull_request.head.sha }}"
         and env.get("CI_DUONG_NHANH_MERGE") == "${{ github.sha }}", f"env buoc phan loai sai: {env}")
    bang(b.get("continue-on-error") is True,
         "buoc phan loai phai co `continue-on-error: true`: phan loai loi phai roi ve day_du; chuan-bi DO thi context bat buoc "
         "`(ubuntu-latest)` KHONG duoc tao va PR bi CHAN (da do tren luot that: Issue #674 comment 5889459132)")
    co = [x for x in buoc(wf, "chuan-bi") if str(x.get("uses", "")).startswith("actions/checkout")]
    bang(len(co) == 1 and (co[0].get("with") or {}).get("fetch-depth") == 0, f"chuan-bi phai checkout fetch-depth 0: {co}")
    bang(chuan_hoa_if(co[0].get("if")) == "github.event_name == 'pull_request'" and co[0].get("continue-on-error") is True,
         "checkout cua chuan-bi phai chi chay o pull_request va co continue-on-error: true")


@ca
def y02_output_che_do_fail_close():
    wf = doc_wf()
    ra = wf["jobs"]["chuan-bi"].get("outputs") or {}
    bang(chuan_hoa_if(ra.get("che_do")) == "github.event_name == 'pull_request' && steps.phan-loai.outputs.che_do || 'day_du'",
         f"output che_do phai ve day_du khi khong phai PR hoac rong: {ra.get('che_do')!r}")
    bang("os" in ra and "fromjson" not in str(ra.get("che_do")).lower(), "output os phai con, che_do khong boc fromJson")


@ca
def y03_buoc_nang_mang_if_bo_theo_che_do():
    wf = doc_wf()
    for job, ten_ds in BO_QUA.items():
        for ten, mong in ten_ds.items():
            b = tim_buoc(wf, job, ten)
            bang("if" in b and chuan_hoa_if(b["if"]) == mong,
                 f"{job}/{ten}: `if:` phai la DUNG {mong!r} (giu dieu kien nen cu, them dieu kien che_do), duoc {b.get('if')!r}")


# wp892 (#892, spec r2 — chu kho chon "Nới y04 hẹp, spec r2"): DUNG hai ngoai le, so NGUYEN VAN. Luat goc giu nguyen
# cho moi cho khac: bo CA job theo che_do thi check VANG MAT. `gate-cong-cu` (8 manh) KHONG la context bat buoc; context
# bat buoc `gate-cong-cu-gop` van chay va doc che_do qua DUNG mot bien env de noi KHONG DO thay vi `skipped`.
Y04_IF_JOB_CHE_DO = {"gate-cong-cu": "needs.chuan-bi.outputs.che_do != 'duong_nhanh'"}
Y04_ENV_BUOC_CHE_DO = {("gate-cong-cu-gop", "G5 gom manh ban kinh dot bien (#668)"):
                       {"CONG_CU_TEST_GOP_CHE_DO": "${{ needs.chuan-bi.outputs.che_do }}"}}


@ca
def y04_tap_buoc_mang_if_che_do_khop_dung():
    wf = doc_wf()
    for job, cau_hinh in wf["jobs"].items():
        if_job = str(cau_hinh.get("if", ""))
        bang(("che_do" not in if_job or (job in Y04_IF_JOB_CHE_DO and chuan_hoa_if(cau_hinh["if"]) == Y04_IF_JOB_CHE_DO[job]))
             and "che_do" not in str(cau_hinh.get("strategy", "")),
             f"{job}: `che_do` khong duoc xuat hien o `if:`/strategy cap JOB (bo ca job = check VANG MAT) — ngoai le "
             f"duy nhat {Y04_IF_JOB_CHE_DO}")
        thay = set()
        for b in cau_hinh.get("steps") or []:
            if "che_do" in str(b.get("if", "")):
                nd = chuan_hoa_if(b["if"])
                if " != 'duong_nhanh'" in nd:
                    thay.add(ten_buoc(b))
                    bang(BO_QUA.get(job, {}).get(ten_buoc(b)) == nd, f"{job}/{ten_buoc(b)}: dang `if:` khong thuoc danh sach cho phep: {nd!r}")
                else:
                    bang(nd == NHANH, f"{job}/{ten_buoc(b)}: dang `if:` theo che_do khong thuoc danh sach cho phep: {nd!r}")
            env_ok = "che_do" not in str(b.get("env", "")) or b.get("env") == Y04_ENV_BUOC_CHE_DO.get((job, ten_buoc(b)))
            bang(env_ok and "che_do" not in str(b.get("with", "")),
                 f"{job}/{ten_buoc(b)}: che_do khong duoc chay vao env/with cua buoc — ngoai le duy nhat {Y04_ENV_BUOC_CHE_DO}")
        mong = set(BO_QUA.get(job, {}))
        bang(thay == mong, f"{job}: tap buoc bi bo theo che_do phai KHOP DUNG danh sach: thua {sorted(thay - mong)}, thieu {sorted(mong - thay)}")


@ca
def y05_khong_paths_khong_paths_ignore():
    wf = doc_wf()
    thay = []

    def di(nut, vet):
        if isinstance(nut, dict):
            for k, v in nut.items():
                if k in ("paths", "paths-ignore"):
                    thay.append("/".join(map(str, vet + [k])))
                di(v, vet + [k])
        elif isinstance(nut, list):
            for i, v in enumerate(nut):
                di(v, vet + [i])
    di(wf, [])
    bang(not thay, f"ci.yml KHONG duoc dung paths:/paths-ignore: (workflow khong chay => required check VANG MAT): {thay}")
    bang(any(k in wf for k in (True, "on")), "ci.yml phai con khoi `on:` (kiem hop le cua chinh ca nay)")


@ca
def y06_job_bat_buoc_khong_bi_bo_ca_job():
    wf = doc_wf()
    for job in ("chuan-bi", *BAT_BUOC):
        bang(job in wf["jobs"], f"thieu job bat buoc {job}")
        bang("if" not in wf["jobs"][job], f"{job}: KHONG duoc co `if:` cap job — check se VANG MAT thay vi bao ket qua")
        bang(wf["jobs"][job].get("continue-on-error", False) is False, f"{job}: job bat buoc khong duoc nuot loi")


@ca
def y07_buoc_bi_bo_tu_noi_ly_do():
    wf = doc_wf()
    for job in BAT_BUOC:
        an = [b for b in buoc(wf, job) if ten_buoc(b).startswith("DUONG_NHANH - liet ke buoc bo qua")]
        bang(len(an) == 1, f"{job}: phai co dung mot buoc liet ke buoc bo qua, thay {len(an)}")
        bang(chuan_hoa_if(an[0].get("if")) == NHANH, f"{job}: buoc liet ke chi chay khi duong nhanh, if={an[0].get('if')!r}")
        dong = [d.strip() for d in str(an[0].get("run", "")).splitlines() if d.strip()]
        ten = set()
        for d in dong:
            m = re.fullmatch(r'echo "DUONG_NHANH: bo qua (.+?) ' + re.escape(DUOI_LOG) + r'"', d)
            bang(m is not None, f"{job}: dong liet ke sai dang: {d!r}")
            ten.add(m.group(1))
        bang(len(dong) == len(ten) and ten == set(BO_QUA[job]),
             f"{job}: cac buoc duoc noi 'bo qua' phai KHOP DUNG cac buoc bi bo: thua {sorted(ten - set(BO_QUA[job]))}, "
             f"thieu {sorted(set(BO_QUA[job]) - ten)}")


@ca
def y08_buoc_kiem_re_o_gate_ops():
    wf = doc_wf()
    kr = [b for b in buoc(wf, "gate-ops") if "ci_duong_nhanh.py kiem-re" in str(b.get("run", ""))]
    bang(len(kr) == 1, f"gate-ops phai co dung mot buoc kiem re, thay {len(kr)}")
    b = kr[0]
    bang(chuan_hoa_if(b.get("if")) == NHANH, f"buoc kiem re chi chay khi duong nhanh, if={b.get('if')!r}")
    run = str(b.get("run", ""))
    bang(b.get("continue-on-error", False) is False, "buoc kiem re khong duoc nuot loi (continue-on-error)")
    bang(b.get("shell") == "bash", f"buoc kiem re phai dung shell bash, duoc {b.get('shell')!r}")
    bang([d.strip() for d in run.splitlines() if d.strip()] == [
        "set -euo pipefail", "python .claude/dev/packet_loop.py doctrine-scan --root .", "python ops/ci_duong_nhanh.py kiem-re"],
        f"buoc kiem re phai chay DUNG ba dong nay (khong chap nhan comment / them bot lenh): {run!r}")
    env = b.get("env") or {}
    bang(env.get("CI_DUONG_NHANH_GOC") == "${{ github.event.pull_request.base.sha }}"
         and env.get("CI_DUONG_NHANH_DAU") == "${{ github.event.pull_request.head.sha }}"
         and env.get("CI_DUONG_NHANH_SU_KIEN") == "${{ github.event_name }}"
         and env.get("CI_DUONG_NHANH_MERGE") == "${{ github.sha }}", f"env buoc kiem re sai: {env}")


@ca
def y09_buoc_goi_test_cua_packet_khong_bi_bo():
    wf = doc_wf()
    goi = [(j, b) for j, cau in wf["jobs"].items() for b in (cau.get("steps") or [])
           if DONG_GOI_TEST in [x.strip() for x in str(b.get("run", "")).splitlines()]]
    bang(len(goi) == 1 and goi[0][0] == "gate-ops", f"phai co dung mot buoc `{DONG_GOI_TEST}` o gate-ops, thay {[(j, ten_buoc(b)) for j, b in goi]}")
    b = goi[0][1]
    bang("che_do" not in str(b.get("if", "")) and chuan_hoa_if(b.get("if", "runner.os == 'Linux'")) == "runner.os == 'Linux'",
         f"buoc goi test CUA CHINH PACKET khong duoc bi bo theo che_do (no la cong duy nhat canh cac `if:`): if={b.get('if')!r}")
    bang(b.get("continue-on-error", False) is False, "buoc goi test khong duoc co continue-on-error")


# LUAT: MOI `if:` cap buoc cua ci.yml (ten buoc -> bieu thuc chuan hoa) theo tung job. Buoc nao them/bo/doi `if:` deu do.
# Chi cac buoc mang che_do la do packet nay; con lai la `if:` co san tu truoc (khong duoc tu y them `if: false` vao buoc giu).
IF_BUOC_CHUAN = {
    'chuan-bi': {
        'actions/checkout@v4': "github.event_name == 'pull_request'",
        'phan loai diff (duong nhanh ho so - chi pull_request)': "github.event_name == 'pull_request'",
        'che do (push / workflow_dispatch luon day du)': "github.event_name != 'pull_request'",
    },
    'gate': {
        'DUONG_NHANH - liet ke buoc bo qua (job gate)': "needs.chuan-bi.outputs.che_do == 'duong_nhanh'",
        'PR head contains required EOL base': "github.event_name == 'pull_request'",
        'tl selftest (luot PR — khong sinh bang chung)': "github.event_name == 'pull_request' && needs.chuan-bi.outputs.che_do != 'duong_nhanh'",
        'tl selftest (co bang chung exact-identity)': "github.event_name != 'pull_request'",
        'tai len gate-evidence': 'always()',
        'golden-test': "needs.chuan-bi.outputs.che_do != 'duong_nhanh'",
        'determinism-audit strict': "needs.chuan-bi.outputs.che_do != 'duong_nhanh'",
        'ci-phamvi selftest (phan chung — cong co rang)': "runner.os != 'Windows'",
        'release-check full': "needs.chuan-bi.outputs.che_do != 'duong_nhanh'",
        'release-verify strict (lane LAND — manifest committed)': "github.ref == 'refs/heads/master'",
        'release-verify strict (lane WORKER — manifest TẠM ngoài repo)': "github.ref != 'refs/heads/master'",
        'release-bundle x2 cùng SHA-256': "needs.chuan-bi.outputs.che_do != 'duong_nhanh'",
    },
    # #668: hai job G5 chia manh KHONG co `if:` cap buoc nao (do 01-10-2026 tren ci.yml sau merge 20ec8d5).
    # wp879 (#879): Windows chi chay ca nen, khong ghi tep manh ⇒ buoc tai len CHI chay ngoai Windows.
    'gate-cong-cu': {
        'actions/upload-artifact@v4': "runner.os != 'Windows'",
    },
    'gate-cong-cu-gop': {
    },
    'gate-ops': {
        'DUONG_NHANH - liet ke buoc bo qua (job gate-ops)': "needs.chuan-bi.outputs.che_do == 'duong_nhanh'",
        'DUONG_NHANH - kiem re thay cho buoc bi bo (doctrine-scan, YAML, diff --check, lease check)': "needs.chuan-bi.outputs.che_do == 'duong_nhanh'",
        'ci-duong-nhanh selftest (phan loai diff + khoa cau truc if)': "runner.os == 'Linux'",
        'lease-publish selftest (đo lại setup sau G5)': "needs.chuan-bi.outputs.che_do != 'duong_nhanh'",
        'don-nhanh selftest (chốt xoá nhánh)': "runner.os != 'Windows'",
        'bo ca gate chay TRONG cgroup duoc uy quyen (Linux)': "runner.os == 'Linux' && needs.chuan-bi.outputs.che_do != 'duong_nhanh'",
        'gate lifecycle selftest (nen khong co cgroup)': "runner.os != 'Linux' && needs.chuan-bi.outputs.che_do != 'duong_nhanh'",
    },
    'gate-nhanh-manh': {},
    'gate-nhanh-gop': {},
    'gate-registry': {
    },
    'gate-packet-loop': {
        'DUONG_NHANH - liet ke buoc bo qua (job gate-packet-loop)': "needs.chuan-bi.outputs.che_do == 'duong_nhanh'",
        'packet-loop selftest': "needs.chuan-bi.outputs.che_do != 'duong_nhanh'",
    },
}


# LUAT (khoa topology): moi thu KHAC thân `run:` cua ci.yml. `run:` cua buoc co san ngoai pham vi packet nay (do cong khac + review canh);
# `run:` cua buoc do packet them thi duoc khoa nguyen van o y08/y09. Doi bat ky muc nao duoi day => y13 do => cap nhat CUNG review.
KHUNG_TOP = {'name': 'gate', True: {'push': {'branches': ['master']}, 'pull_request': None, 'workflow_dispatch': {'inputs': {'runner_set': {'description': 'windows-and-ubuntu (mặc định) hoặc windows-only (bỏ các job ma trận Ubuntu)', 'required': False, 'default': 'windows-and-ubuntu', 'type': 'choice', 'options': ['windows-and-ubuntu', 'windows-only']}}}}, 'concurrency': {'group': '${{ github.workflow }}-${{ github.event.pull_request.number || github.ref }}', 'cancel-in-progress': "${{ github.ref != 'refs/heads/master' }}"}}
KHUNG_JOB = {
    'chuan-bi': {'runs-on': 'ubuntu-latest', 'timeout-minutes': 20, 'outputs': {'os': '${{ (github.event_name == \'workflow_dispatch\' && inputs.runner_set == \'windows-only\') && \'["windows-latest"]\' || (github.event_name == \'workflow_dispatch\' || contains(github.event.pull_request.labels.*.name, \'windows\')) && \'["ubuntu-latest","windows-latest"]\' || \'["ubuntu-latest"]\' }}', 'che_do': "${{ github.event_name == 'pull_request' && steps.phan-loai.outputs.che_do || 'day_du' }}"}},
    'gate': {'needs': 'chuan-bi', 'strategy': {'fail-fast': False, 'matrix': {'os': '${{ fromJson(needs.chuan-bi.outputs.os) }}'}}, 'runs-on': '${{ matrix.os }}', 'timeout-minutes': 60, 'env': {'PYTHONIOENCODING': 'utf-8', 'PYTHONUTF8': '1', 'PYTHONDONTWRITEBYTECODE': '1'}},
    # #668 (land truoc #674, tich hop o g4): hai job G5 chia manh. KHONG mang `if:` theo `che_do` (chay du = fail-close).
    'gate-cong-cu': {'needs': 'chuan-bi', 'if': "${{ needs.chuan-bi.outputs.che_do != 'duong_nhanh' }}", 'strategy': {'fail-fast': False, 'matrix': {'os': '${{ fromJson(needs.chuan-bi.outputs.os) }}', 'manh': [0, 1, 2, 3, 4, 5, 6, 7], 'exclude': [{'os': 'windows-latest', 'manh': 1}, {'os': 'windows-latest', 'manh': 2}, {'os': 'windows-latest', 'manh': 3}, {'os': 'windows-latest', 'manh': 4}, {'os': 'windows-latest', 'manh': 5}, {'os': 'windows-latest', 'manh': 6}, {'os': 'windows-latest', 'manh': 7}]}}, 'runs-on': '${{ matrix.os }}', 'timeout-minutes': 150, 'env': {'PYTHONIOENCODING': 'utf-8', 'PYTHONUTF8': '1', 'PYTHONDONTWRITEBYTECODE': '1'}},
    'gate-cong-cu-gop': {'needs': ['chuan-bi', 'gate-cong-cu'], 'if': "${{ !cancelled() && contains(fromJson(needs.chuan-bi.outputs.os), 'ubuntu-latest') }}", 'strategy': {'fail-fast': False, 'matrix': {'os': '${{ fromJson(needs.chuan-bi.outputs.os) }}', 'exclude': [{'os': 'windows-latest'}]}}, 'runs-on': '${{ matrix.os }}', 'timeout-minutes': 10, 'env': {'PYTHONIOENCODING': 'utf-8', 'PYTHONUTF8': '1', 'PYTHONDONTWRITEBYTECODE': '1'}},
    'gate-ops': {'needs': 'chuan-bi', 'strategy': {'fail-fast': False, 'matrix': {'os': '${{ fromJson(needs.chuan-bi.outputs.os) }}'}}, 'runs-on': '${{ matrix.os }}', 'timeout-minutes': 60, 'env': {'PYTHONIOENCODING': 'utf-8', 'PYTHONUTF8': '1', 'PYTHONDONTWRITEBYTECODE': '1'}},
    'gate-nhanh-manh': {'needs': 'chuan-bi', 'strategy': {'fail-fast': False, 'matrix': {'os': '${{ fromJson(needs.chuan-bi.outputs.os) }}', 'manh': [0, 1, 2, 3, 4, 5, 6, 7]}}, 'runs-on': '${{ matrix.os }}', 'timeout-minutes': 30, 'env': {'PYTHONIOENCODING': 'utf-8', 'PYTHONUTF8': '1', 'PYTHONDONTWRITEBYTECODE': '1'}},
    'gate-nhanh-gop': {'needs': ['chuan-bi', 'gate-nhanh-manh'], 'if': '${{ !cancelled() }}', 'strategy': {'fail-fast': False, 'matrix': {'os': '${{ fromJson(needs.chuan-bi.outputs.os) }}'}}, 'runs-on': '${{ matrix.os }}', 'timeout-minutes': 10, 'env': {'PYTHONIOENCODING': 'utf-8', 'PYTHONUTF8': '1', 'PYTHONDONTWRITEBYTECODE': '1'}},
    'gate-registry': {'needs': ['chuan-bi', 'gate-nhanh-gop'], 'if': '${{ !cancelled() }}', 'strategy': {'fail-fast': False, 'matrix': {'os': '${{ fromJson(needs.chuan-bi.outputs.os) }}'}}, 'runs-on': '${{ matrix.os }}', 'timeout-minutes': 105, 'env': {'PYTHONIOENCODING': 'utf-8', 'PYTHONUTF8': '1', 'PYTHONDONTWRITEBYTECODE': '1'}},
    'gate-packet-loop': {'needs': 'chuan-bi', 'strategy': {'fail-fast': False, 'matrix': {'os': '${{ fromJson(needs.chuan-bi.outputs.os) }}'}}, 'runs-on': '${{ matrix.os }}', 'timeout-minutes': 120, 'env': {'PYTHONIOENCODING': 'utf-8', 'PYTHONUTF8': '1', 'PYTHONDONTWRITEBYTECODE': '1'}},
}
KHUNG_BUOC = {
    'chuan-bi': [
        ('actions/checkout@v4', {'uses': 'actions/checkout@v4', 'if': "${{ github.event_name == 'pull_request' }}", 'continue-on-error': True, 'timeout-minutes': 10, 'with': {'fetch-depth': 0}}),
        ('phan loai diff (duong nhanh ho so - chi pull_request)', {'id': 'phan-loai', 'if': "${{ github.event_name == 'pull_request' }}", 'continue-on-error': True, 'timeout-minutes': 5, 'env': {'CI_DUONG_NHANH_SU_KIEN': '${{ github.event_name }}', 'CI_DUONG_NHANH_GOC': '${{ github.event.pull_request.base.sha }}', 'CI_DUONG_NHANH_DAU': '${{ github.event.pull_request.head.sha }}', 'CI_DUONG_NHANH_MERGE': '${{ github.sha }}'}}),
        ('che do (push / workflow_dispatch luon day du)', {'if': "${{ github.event_name != 'pull_request' }}", 'env': {'SU_KIEN': '${{ github.event_name }}'}}),
    ],
    'gate': [
        ('Force LF checkout (hash parity với manifest)', {}),
        ('actions/checkout@v4', {'uses': 'actions/checkout@v4', 'with': {'fetch-depth': 0}}),
        ('actions/setup-python@v5', {'uses': 'actions/setup-python@v5', 'with': {'python-version': '3.12'}}),
        ('cài PyYAML + jsonschema (cổng đăng lease + validator verdict cần)', {}),
        ('cài actionlint cho G5', {'shell': 'bash', 'env': {'AL_VER': '1.7.7'}}),
        ('cài shellcheck cho G5 (cài xong đo lại)', {'shell': 'bash'}),
        ('cài rg cho G5 (cài xong đo lại)', {'shell': 'bash'}),
        ('G5 kiem ban ke cong cu + T1..T8 (packet', {'shell': 'bash', 'env': {'CONG_CU_TEST_BAN_KINH': 'manh'}}),
        ('cài Ruff 0.15.15 và in probe dương', {}),
        ('DUONG_NHANH - liet ke buoc bo qua (job gate)', {'if': "${{ needs.chuan-bi.outputs.che_do == 'duong_nhanh' }}"}),
        ('PR head contains required EOL base', {'if': "${{ github.event_name == 'pull_request' }}", 'shell': 'bash', 'env': {'PR_HEAD_SHA': '${{ github.event.pull_request.head.sha }}', 'EOL_BASE_SHA': '1880346d2be3c0be9a93de7624ee108d99b6c88c'}}),
        ('py_compile', {}),
        ('codex credential selftest (packet #300)', {}),
        ('idiom-ba-ten selftest', {}),
        ('eol-policy selftest', {}),
        ('pre-push selftest', {}),
        ('eol-policy survey', {}),
        ('bundled-fragment check (topology gói)', {}),
        ('gen_instructions selftest', {}),
        ('command-registry unit test (AG-T0-03)', {}),
        ('tl selftest (luot PR — khong sinh bang chung)', {'if': "${{ github.event_name == 'pull_request' && needs.chuan-bi.outputs.che_do != 'duong_nhanh' }}"}),
        ('tl selftest (co bang chung exact-identity)', {'if': "${{ github.event_name != 'pull_request' }}", 'shell': 'bash'}),
        ('tai len gate-evidence', {'if': 'always()', 'uses': 'actions/upload-artifact@v4', 'with': {'name': 'gate-evidence-${{ matrix.os }}-${{ github.run_attempt }}', 'path': 'scripts/.tl_state/gate/', 'if-no-files-found': 'warn'}}),
        ('workflow-audit strict', {}),
        ('golden-test', {'if': "${{ needs.chuan-bi.outputs.che_do != 'duong_nhanh' }}"}),
        ('doc-claims-check strict', {}),
        ('determinism-audit strict', {'if': "${{ needs.chuan-bi.outputs.che_do != 'duong_nhanh' }}"}),
        ('ci-phamvi guard (bang phu thuoc khop ma)', {}),
        ('ci-phamvi selftest (phan chung — cong co rang)', {'if': "runner.os != 'Windows'"}),
        ('release-check full', {'if': "${{ needs.chuan-bi.outputs.che_do != 'duong_nhanh' }}"}),
        ('release-verify strict (lane LAND — manifest committed)', {'if': "github.ref == 'refs/heads/master'"}),
        ('release-verify strict (lane WORKER — manifest TẠM ngoài repo)', {'if': "github.ref != 'refs/heads/master'", 'shell': 'bash'}),
        ('release-bundle x2 cùng SHA-256', {'if': "${{ needs.chuan-bi.outputs.che_do != 'duong_nhanh' }}", 'shell': 'bash'}),
        ('tl_boot smoke', {}),
    ],
    'gate-cong-cu': [
        ('Force LF checkout (hash parity với manifest)', {}),
        ('actions/checkout@v4', {'uses': 'actions/checkout@v4', 'with': {'fetch-depth': 0}}),
        ('actions/setup-python@v5', {'uses': 'actions/setup-python@v5', 'with': {'python-version': '3.12'}}),
        ('cài PyYAML + jsonschema (cổng đăng lease + validator verdict cần)', {}),
        ('cài actionlint cho G5', {'shell': 'bash', 'env': {'AL_VER': '1.7.7'}}),
        ('cài shellcheck cho G5 (cài xong đo lại)', {'shell': 'bash'}),
        ('cài rg cho G5 (cài xong đo lại)', {'shell': 'bash'}),
        ('G5 manh ban kinh dot bien (#668)', {'shell': 'bash', 'env': {'CONG_CU_TEST_MANH': '${{ matrix.manh }}/8', 'CONG_CU_TEST_MANH_RA': 'manh/manh-${{ matrix.manh }}.txt'}}),
        ('actions/upload-artifact@v4', {'if': "runner.os != 'Windows'", 'uses': 'actions/upload-artifact@v4', 'with': {'name': 'gate-cong-cu-manh-${{ matrix.os }}-${{ matrix.manh }}', 'path': 'manh/manh-${{ matrix.manh }}.txt', 'if-no-files-found': 'error'}}),
    ],
    'gate-cong-cu-gop': [
        ('Force LF checkout (hash parity với manifest)', {}),
        ('actions/checkout@v4', {'uses': 'actions/checkout@v4'}),
        ('actions/setup-python@v5', {'uses': 'actions/setup-python@v5', 'with': {'python-version': '3.12'}}),
        ('cài PyYAML + jsonschema (cổng đăng lease + validator verdict cần)', {}),
        ('actions/download-artifact@v4', {'uses': 'actions/download-artifact@v4', 'with': {'pattern': 'gate-cong-cu-manh-${{ matrix.os }}-*', 'path': 'manh', 'merge-multiple': True}}),
        ('G5 gom manh ban kinh dot bien (#668)', {'shell': 'bash', 'env': {'CONG_CU_TEST_GOP_CHE_DO': '${{ needs.chuan-bi.outputs.che_do }}'}}),
    ],
    'gate-ops': [
        ('Force LF checkout (hash parity với manifest)', {}),
        ('actions/checkout@v4', {'uses': 'actions/checkout@v4', 'with': {'fetch-depth': 0}}),
        ('actions/setup-python@v5', {'uses': 'actions/setup-python@v5', 'with': {'python-version': '3.12'}}),
        ('cài PyYAML + jsonschema (cổng đăng lease + validator verdict cần)', {}),
        ('cài shellcheck cho G5 (cài xong đo lại)', {'shell': 'bash'}),
        ('cài rg cho G5 (cài xong đo lại)', {'shell': 'bash'}),
        ('DUONG_NHANH - liet ke buoc bo qua (job gate-ops)', {'if': "${{ needs.chuan-bi.outputs.che_do == 'duong_nhanh' }}"}),
        ('DUONG_NHANH - kiem re thay cho buoc bi bo (doctrine-scan, YAML, diff --check, lease check)', {'if': "${{ needs.chuan-bi.outputs.che_do == 'duong_nhanh' }}", 'shell': 'bash', 'env': {'CI_DUONG_NHANH_SU_KIEN': '${{ github.event_name }}', 'CI_DUONG_NHANH_GOC': '${{ github.event.pull_request.base.sha }}', 'CI_DUONG_NHANH_DAU': '${{ github.event.pull_request.head.sha }}', 'CI_DUONG_NHANH_MERGE': '${{ github.sha }}'}}),
        ('ci-duong-nhanh selftest (phan loai diff + khoa cau truc if)', {'if': "runner.os == 'Linux'"}),
        ('bien-nhan v2 selftest', {}),
        ('lease-publish selftest (đo lại setup sau G5)', {'if': "${{ needs.chuan-bi.outputs.che_do != 'duong_nhanh' }}", 'shell': 'bash', 'env': {'AL_VER': '1.7.7'}}),
        ('don-nhanh selftest (chốt xoá nhánh)', {'if': "runner.os != 'Windows'", 'shell': 'pwsh'}),
        ('bo ca gate chay TRONG cgroup duoc uy quyen (Linux)', {'if': "${{ runner.os == 'Linux' && needs.chuan-bi.outputs.che_do != 'duong_nhanh' }}"}),
        ('gate lifecycle selftest (nen khong co cgroup)', {'if': "${{ runner.os != 'Linux' && needs.chuan-bi.outputs.che_do != 'duong_nhanh' }}"}),
    ],
    'gate-nhanh-manh': [
        ('Force LF checkout (hash parity với manifest)', {}),
        ('actions/checkout@v4', {'uses': 'actions/checkout@v4', 'with': {'fetch-depth': 0}}),
        ('actions/setup-python@v5', {'uses': 'actions/setup-python@v5', 'with': {'python-version': '3.12'}}),
        # WP748 r16: targeted_mutant_gate (khong phai full mutant audit); tran job xem timeout-minutes trong ci.yml.
        ('chạy mảnh nhanh_don_duoc (targeted_mutant_gate)', {'env': {'NHANH_DON_DUOC_DICH': '${{ matrix.manh }}/8', 'NHANH_DON_DUOC_DICH_RA': 'manh/manh-${{ matrix.manh }}.json'}}),
        ('actions/upload-artifact@v4', {'uses': 'actions/upload-artifact@v4', 'with': {'name': 'gate-nhanh-${{ matrix.os }}-${{ matrix.manh }}', 'path': 'manh/manh-${{ matrix.manh }}.json', 'if-no-files-found': 'error'}}),
    ],
    'gate-nhanh-gop': [
        ('Force LF checkout (hash parity với manifest)', {}),
        ('actions/checkout@v4', {'uses': 'actions/checkout@v4', 'with': {'fetch-depth': 0}}),
        ('actions/setup-python@v5', {'uses': 'actions/setup-python@v5', 'with': {'python-version': '3.12'}}),
        ('actions/download-artifact@v4', {'uses': 'actions/download-artifact@v4', 'with': {'pattern': 'gate-nhanh-${{ matrix.os }}-*', 'path': 'manh', 'merge-multiple': True}}),
        ('gộp mảnh nhanh_don_duoc (targeted_mutant_gate)', {}),
    ],
    'gate-registry': [
        ('Force LF checkout (hash parity với manifest)', {}),
        ('actions/checkout@v4', {'uses': 'actions/checkout@v4', 'with': {'fetch-depth': 0}}),
        ('actions/setup-python@v5', {'uses': 'actions/setup-python@v5', 'with': {'python-version': '3.12'}}),
        ('cài PyYAML + jsonschema (cổng đăng lease + validator verdict cần)', {}),
        ('cài actionlint cho G5', {'shell': 'bash', 'env': {'AL_VER': '1.7.7'}}),
        ('cài shellcheck cho G5 (cài xong đo lại)', {'shell': 'bash'}),
        ('cài rg cho G5 (cài xong đo lại)', {'shell': 'bash'}),
        ('G5 probe ban ke cong cu (#290; selftest T1..T8 chi o job gate, chot M6', {'shell': 'bash'}),
        ('cài Ruff 0.15.15 và in probe dương', {}),
        ('test registry (phạm vi + các bộ chưa được nối)', {'env': {'CI_DANG_KY_WORKERS': '2', 'CI_DANG_KY_SU_KIEN': '${{ github.event_name }}', 'CI_DANG_KY_GOC': '${{ github.event.pull_request.base.sha || github.event.before }}', 'CI_DANG_KY_DAU': '${{ github.event.pull_request.head.sha || github.sha }}', 'CI_DANG_KY_DOT_BIEN_MANH': 'ops/nhanh_don_duoc_test.py', 'CI_DANG_KY_GOP_KQ': '${{ needs.gate-nhanh-gop.result }}'}}),
    ],
    'gate-packet-loop': [
        ('Force LF checkout (hash parity với manifest)', {}),
        ('actions/checkout@v4', {'uses': 'actions/checkout@v4', 'with': {'fetch-depth': 0}}),
        ('actions/setup-python@v5', {'uses': 'actions/setup-python@v5', 'with': {'python-version': '3.12'}}),
        ('cài PyYAML + jsonschema (cổng đăng lease + validator verdict cần)', {}),
        ('cài actionlint cho G5', {'shell': 'bash', 'env': {'AL_VER': '1.7.7'}}),
        ('cài shellcheck cho G5 (cài xong đo lại)', {'shell': 'bash'}),
        ('cài rg cho G5 (cài xong đo lại)', {'shell': 'bash'}),
        ('G5 probe ban ke cong cu (#290; selftest T1..T8 chi o job gate, chot M6', {'shell': 'bash'}),
        ('cài Ruff 0.15.15 và in probe dương', {}),
        ('DUONG_NHANH - liet ke buoc bo qua (job gate-packet-loop)', {'if': "${{ needs.chuan-bi.outputs.che_do == 'duong_nhanh' }}"}),
        ('packet-loop selftest', {'if': "${{ needs.chuan-bi.outputs.che_do != 'duong_nhanh' }}"}),
    ],
}


# LUAT: job -> bieu thuc `if:` cap job CHUAN HOA, khop DUNG (khong phai chi "job co trong danh sach"). #668 land truoc #674
# (tich hop g4, master 20ec8d5): `gate-cong-cu-gop` can `!cancelled()` de manh DO thi gom van chay va DO vi thieu manh —
# `needs` mac dinh se cho no `skipped`, ma `skipped` doc nhu xanh (ngu nghia GitHub Actions theo tai lieu, chua tu do).
# wp879 (#879): gom them `contains(... 'ubuntu-latest')` — luot `windows-only` khong con manh nao de gom.
# Doi bieu thuc (vd `always()`), bo no, hay them `if:` cap job vao job KHAC (ke ca cung bieu thuc) deu phai DO. `ci_dang_ky_test.loi_g5_workflow` canh cung khoa ay tu phia #668.
JOB_CO_IF_CHO_PHEP = {"gate-cong-cu": "needs.chuan-bi.outputs.che_do != 'duong_nhanh'", "gate-cong-cu-gop": "!cancelled() && contains(fromJson(needs.chuan-bi.outputs.os), 'ubuntu-latest')", "gate-nhanh-gop": "!cancelled()", "gate-registry": "!cancelled()"}


@ca
def y11_khong_job_nao_co_if_cap_job_ngoai_danh_sach_cho_phep():
    """Cross-review luot 3 (P2): y06 chi nhin ba job bat buoc + chuan-bi; job phu khac (gate-registry...) cung khong duoc bi bo
    hoac sua ket qua bang `if:` cap job. Quet MOI job; anh xa {job: `if:` chuan hoa} phai BANG DUNG `JOB_CO_IF_CHO_PHEP`."""
    thuc = {job: chuan_hoa_if(cau["if"]) for job, cau in doc_wf()["jobs"].items() if "if" in cau}
    bang(thuc == JOB_CO_IF_CHO_PHEP,
         f"`if:` cap job lech danh sach cho phep: thua/doi {sorted((j, v) for j, v in thuc.items() if JOB_CO_IF_CHO_PHEP.get(j) != v)}, "
         f"thieu {sorted(j for j in JOB_CO_IF_CHO_PHEP if j not in thuc)}")


@ca
def y12_moi_if_cap_buoc_khop_dung_danh_sach_cho_phep():
    """Cross-review luot 3 (lop chot-yaml): danh sach CHO PHEP toan bo `if:` cap buoc, khong chi cac buoc mang `che_do`.
    Them `if: false` vao mot buoc GIU (py_compile, eol survey...) hay doi mot `if:` co san deu phai do."""
    wf = doc_wf()
    thuc = {}
    for job, cau in wf["jobs"].items():
        thuc[job] = {}
        for b in cau.get("steps") or []:
            if "if" in b:
                khoa = b.get("name") or b.get("uses")
                bang(khoa not in thuc[job], f"{job}: hai buoc trung ten {khoa!r}")
                thuc[job][khoa] = chuan_hoa_if(b["if"])
    bang(set(thuc) == set(IF_BUOC_CHUAN), f"tap job lech: thua {sorted(set(thuc) - set(IF_BUOC_CHUAN))}, thieu {sorted(set(IF_BUOC_CHUAN) - set(thuc))}")
    for job, mong in IF_BUOC_CHUAN.items():
        bang(thuc[job] == mong, f"{job}: tap `if:` cap buoc lech danh sach cho phep: "
             f"thua/doi {sorted((k, v) for k, v in thuc[job].items() if mong.get(k) != v)}, "
             f"thieu {sorted(k for k in mong if k not in thuc[job])}")


@ca
def y13_khoa_topology_cua_ci_yml_ngoai_than_run():
    """Cross-review luot 4 (P2): doi `gate-ops.runs-on` sang windows-latest van qua suite. Goc: khoa DINH TUYEN va MOI khoa
    khac ngoai than `run:` — cap workflow, cap job (runs-on, needs, strategy/matrix gom include/exclude, timeout, env, outputs,
    permissions...), cap buoc (tap khoa, uses/with/env/shell/working-directory/timeout/id/if/continue-on-error), THU TU buoc."""
    wf = doc_wf()
    top = {k: v for k, v in wf.items() if k != "jobs"}
    bang(top == KHUNG_TOP, f"cap workflow lech khung: {top} != {KHUNG_TOP}")
    bang(list(wf["jobs"]) == list(KHUNG_JOB), f"tap/thu tu job lech: {list(wf['jobs'])} != {list(KHUNG_JOB)}")
    for j, cau in wf["jobs"].items():
        khung = {k: v for k, v in cau.items() if k != "steps"}
        bang(khung == KHUNG_JOB[j], f"{j}: cau hinh cap job lech khung (runs-on/needs/strategy/timeout/env/...): "
             f"khac {sorted(k for k in set(khung) | set(KHUNG_JOB[j]) if khung.get(k) != KHUNG_JOB[j].get(k))}")
        thuc = [(b.get("name") or b.get("uses"), {k: v for k, v in b.items() if k not in ("run", "name")}) for b in cau.get("steps") or []]
        bang(thuc == KHUNG_BUOC[j], f"{j}: danh sach/thu tu/khoa cua buoc lech khung; buoc dau tien lech: "
             f"{next((i for i, (a, b2) in enumerate(zip(thuc, KHUNG_BUOC[j])) if a != b2), min(len(thuc), len(KHUNG_BUOC[j])))}")


# LUAT (luot 5, lop chot-yaml): THAN `run:` cua MOI buoc DO PACKET NAY THEM duoc khoa NGUYEN VAN. Truoc do y09 chi doi dong goi test
# CO MAT trong than ⇒ `exit 0` dat TRUOC no van qua; buoc `che do` cua `chuan-bi` them `exit 1` ⇒ chuan-bi do ⇒ ba job bat buoc
# `skipped`, context bat buoc khong duoc tao ⇒ PR bi CHAN (da do tren luot that: Issue #674 comment 5889459132). Than `run:` cua buoc CO SAN ngoai pham vi packet (bien gioi khai o y13).
RUN_BUOC_PACKET = {
    ('chuan-bi', 'phan loai diff (duong nhanh ho so - chi pull_request)'): 'python3 ops/ci_duong_nhanh.py',
    ('chuan-bi', 'che do (push / workflow_dispatch luon day du)'): 'echo "DUONG_NHANH: khong phan loai - su_kien=${SU_KIEN} khong phai pull_request, luon DAY_DU"\n',
    ('gate', 'DUONG_NHANH - liet ke buoc bo qua (job gate)'): 'echo "DUONG_NHANH: bo qua tl selftest (luot PR — khong sinh bang chung) vi diff chi gom ops/{land,leases,reviews,specs}/**"\necho "DUONG_NHANH: bo qua golden-test vi diff chi gom ops/{land,leases,reviews,specs}/**"\necho "DUONG_NHANH: bo qua determinism-audit strict vi diff chi gom ops/{land,leases,reviews,specs}/**"\necho "DUONG_NHANH: bo qua release-check full vi diff chi gom ops/{land,leases,reviews,specs}/**"\necho "DUONG_NHANH: bo qua release-bundle x2 cùng SHA-256 vi diff chi gom ops/{land,leases,reviews,specs}/**"\n',
    ('gate-ops', 'DUONG_NHANH - liet ke buoc bo qua (job gate-ops)'): 'echo "DUONG_NHANH: bo qua lease-publish selftest (đo lại setup sau G5) vi diff chi gom ops/{land,leases,reviews,specs}/**"\necho "DUONG_NHANH: bo qua bo ca gate chay TRONG cgroup duoc uy quyen (Linux) vi diff chi gom ops/{land,leases,reviews,specs}/**"\necho "DUONG_NHANH: bo qua gate lifecycle selftest (nen khong co cgroup) vi diff chi gom ops/{land,leases,reviews,specs}/**"\n',
    ('gate-ops', 'DUONG_NHANH - kiem re thay cho buoc bi bo (doctrine-scan, YAML, diff --check, lease check)'): 'set -euo pipefail\npython .claude/dev/packet_loop.py doctrine-scan --root .\npython ops/ci_duong_nhanh.py kiem-re\n',
    ('gate-ops', 'ci-duong-nhanh selftest (phan loai diff + khoa cau truc if)'): 'python ops/ci_duong_nhanh_test.py',
    ('gate-packet-loop', 'DUONG_NHANH - liet ke buoc bo qua (job gate-packet-loop)'): 'echo "DUONG_NHANH: bo qua packet-loop selftest vi diff chi gom ops/{land,leases,reviews,specs}/**"\n',
}


@ca
def y14_than_run_cua_buoc_packet_them_khop_nguyen_van():
    wf = doc_wf()
    for (job, ten), mong in RUN_BUOC_PACKET.items():
        bang(tim_buoc(wf, job, ten).get("run") == mong, f"{job}/{ten}: than `run:` lech nguyen van da khoa")
    them = {(j, b.get("name")) for j, c in wf["jobs"].items() for b in c.get("steps") or []
            if "run" in b and any(d in f"{b.get('name')}\n{b.get('run')}" for d in ("DUONG_NHANH", "ci_duong_nhanh"))}
    bang(them == set(RUN_BUOC_PACKET), f"buoc cham duong nhanh ngoai bang khoa: thua {sorted(them - set(RUN_BUOC_PACKET))}, "
         f"thieu {sorted(set(RUN_BUOC_PACKET) - them)}")


@ca
def y15_loader_nghiem_tu_choi_khoa_trung_va_khoa_gop():
    """PyYAML lay ban CUOI cua khoa trung, im lang: `runs-on: windows-latest` roi `runs-on: ${{ matrix.os }}` qua het y13 (thay
    ban cuoi) trong khi GitHub co the doc KHAC (chua do tren GitHub). Loader nghiem phai do ca hai dang tren chinh van ban ci.yml, va ban that phai sach."""
    goc = (CAY / ".github" / "workflows" / "ci.yml").read_text(encoding="utf-8")
    doc_wf_tu(goc)
    neo = "    runs-on: ${{ matrix.os }}\n"
    bang(neo in goc, "ha tang y15: khong thay neo runs-on matrix")
    for ten, vb in (("khoa trung", goc.replace(neo, "    runs-on: windows-latest\n" + neo, 1)),
                    ("khoa gop", goc.replace("jobs:\n", "x-mau: &mau\n  a: 1\njobs:\n  <<: *mau\n", 1))):
        bat = False
        # Di qua reader THAT cua moi ca y*, ke ca khi helper nghiem van con.
        with tempfile.TemporaryDirectory(prefix="cdn_yaml_reader_") as d:
            cay_tam = Path(d)
            tep = cay_tam / ".github" / "workflows" / "ci.yml"
            tep.parent.mkdir(parents=True)
            tep.write_text(vb, encoding="utf-8")
            with mock.patch.dict(globals(), {"CAY": cay_tam}, clear=False):
                with contextlib.suppress(TinHieuChotCa):
                    doc_wf()
                    bat = True
        bang(not bat, f"loader phai DO khi ci.yml co {ten}")


@ca
def y16_chuan_bi_co_tran_thoi_gian_buoc_va_job():
    """Chu kho (Issue #674 comment 5889513175): buoc checkout / phan-loai cua `chuan-bi` treo thi PR bi chan toi 360 phut.
    Hai buoc phai co `timeout-minutes` nho (<= 10) VA `continue-on-error: true` (het gio => roi `day_du`, khong lam job do);
    tran cap job phai lon hon tong hai tran buoc (khong thi job het gio TRUOC buoc, tuc do thay vi roi `day_du`). Ngu nghia
    het gio + `continue-on-error` o day la cua GitHub Actions theo tai lieu, chua tu do; ca nay chi khoa CAU HINH."""
    wf = doc_wf()
    cb = wf["jobs"]["chuan-bi"]
    tong = 0
    for b in buoc(wf, "chuan-bi"):
        if b.get("if") and chuan_hoa_if(b["if"]) == "github.event_name == 'pull_request'":
            tm = b.get("timeout-minutes")
            bang(isinstance(tm, int) and not isinstance(tm, bool) and 1 <= tm <= 10,
                 f"chuan-bi/{b.get('name') or b.get('uses')}: timeout-minutes phai la so nguyen 1..10, duoc {tm!r}")
            bang(b.get("continue-on-error") is True, f"chuan-bi/{b.get('name') or b.get('uses')}: het gio phai roi day_du")
            tong += tm
    bang(tong > 0, "chuan-bi: khong thay buoc phan loai nao")
    tj = cb.get("timeout-minutes")
    bang(isinstance(tj, int) and not isinstance(tj, bool) and tong < tj <= 30,
         f"chuan-bi: timeout-minutes cap job phai > {tong} (tong tran buoc) va <= 30, duoc {tj!r}")


CHO_PHEP_NUOT_LOI = {("chuan-bi", "actions/checkout@v4"), ("chuan-bi", "phan loai diff (duong nhanh ho so - chi pull_request)")}


@ca
def y10_khong_continue_on_error_ngoai_danh_sach_cho_phep():
    """Cross-review luot 2 (P2): moi cua nuot loi phai dong bang MOT ca — o TOAN ci.yml, moi job va moi buoc, moi dang
    (literal, `${{ true }}`, chuoi, bieu thuc dieu kien). Chi hai buoc phan loai cua `chuan-bi` PHAI la literal True."""
    wf = doc_wf()
    for job, cau in wf["jobs"].items():
        bang(cau.get("continue-on-error", False) is False, f"{job}: continue-on-error cap job phai vang hoac false, duoc {cau.get('continue-on-error')!r}")
        for b in cau.get("steps") or []:
            khoa = (job, b.get("name") or b.get("uses"))
            gia_tri = b.get("continue-on-error", False)
            if khoa in CHO_PHEP_NUOT_LOI:
                bang(gia_tri is True, f"{khoa}: phai la literal true (fail-close ve day_du), duoc {gia_tri!r}")
            else:
                bang(gia_tri is False, f"{khoa}: continue-on-error phai vang hoac literal false, duoc {gia_tri!r}")


# ---------------------------------------------------------------- tầng 3: nối vào sổ test sống
def nap_so_dang_ky():
    import runpy
    return runpy.run_path(str(CAY / ".claude" / "dev" / "ci_dang_ky_test.py"))


@ca
def k01_so_dang_ky_nhan_muc_da_noi():
    m = nap_so_dang_ky()
    bang(DA_NOI_MUC in m["DANG_KY"], f"ci_dang_ky_test.DA_NOI phai co {DA_NOI_MUC!r}")
    loi, song, dang_ky = m["kiem"]()
    bang(not loi, f"so dang ky phai sach, duoc {loi}")
    bang(song == dang_ky and song > 0, f"so test song ({song}) phai BANG so dang ky ({dang_ky}) va > 0")


@ca
def k02_da_noi_dung_mot_lan_va_test_song_khop_tep():
    m = nap_so_dang_ky()
    song, _, _ = m["tim"](CAY)
    bang(DA_NOI_MUC in song, f"tep {DA_NOI_MUC} phai ton tai o muc dinh ops/ (vi tri chuan cua test song)")
    src = (CAY / ".claude" / "dev" / "ci_dang_ky_test.py").read_text(encoding="utf-8")
    bang(src.count(f'"{DA_NOI_MUC}"') == 1, f"muc {DA_NOI_MUC!r} phai xuat hien dung mot lan trong ci_dang_ky_test.py")


@ca
def k03_ci_goi_that_muc_da_noi():
    m = nap_so_dang_ky()
    loi, _, _ = m["kiem"]()
    bang(f"CI không gọi mục đăng ký: {DA_NOI_MUC}" not in loi, f"CI phai goi that {DA_NOI_MUC}: {loi}")


@ca_tu_kiem
def t91_ma_thoat_that_khi_ca_dat_do_va_hong():
    """Exec chính stanza __main__ trong tiến trình con; giữ main/runner thật, cô lập công việc nặng."""
    chuong_trinh = """
import ast, runpy, sys
tep, ket_qua = sys.argv[1:]
g = runpy.run_path(tep)["main"].__globals__
def sentinel():
    print("REVIEW_SENTINEL_CALLED")
    if ket_qua == "DO":
        raise g["TinHieuChotCa"]("review sentinel")
    if ket_qua == "HONG":
        raise RuntimeError("review sentinel")
g.update(CA={"t_fixture": sentinel}, CAY=g["ROOT_THAT"],
         chay_tap_dot_bien=lambda _: (len(g["DOT_BIEN"]), []),
         tu_kiem_phan_hang=lambda: [], dong_kiem_ke=lambda: "KIEM KE: fixture")
with open(tep, encoding="utf-8") as f:
    tree = ast.parse(f.read())
entry = tree.body[-1]
assert isinstance(entry, ast.If) and "__name__" in ast.unparse(entry.test)
g["__name__"] = "__main__"
sys.argv = [tep]
exec(compile(ast.Module(body=[entry], type_ignores=[]), tep, "exec"), g)
"""
    for ket_qua, rc_mong in (("DAT", 0), ("DO", 1), ("HONG", 1)):
        r = subprocess.run([sys.executable, "-B", "-c", chuong_trinh,
                            str(CAY / "ops" / "ci_duong_nhanh_test.py"), ket_qua],
                           capture_output=True, text=True, timeout=60)
        bang(r.returncode == rc_mong and r.stdout.count("REVIEW_SENTINEL_CALLED") == 1
             and r.stdout.rstrip().endswith("TONG: DAT" if rc_mong == 0 else "TONG: DO"),
             f"entry/{ket_qua}: rc={r.returncode}, stdout={r.stdout[-700:]!r}, stderr={r.stderr[-300:]!r}")


@ca_tu_kiem
def t92_runner_thuc_su_goi_ca_va_phan_biet_loi():
    goi = []
    for ket_qua in ("DAT", "DO", "HONG"):
        def sentinel():
            goi.append(ket_qua)
            if ket_qua == "DO":
                raise TinHieuChotCa("review sentinel DO")
            if ket_qua == "HONG":
                raise RuntimeError("review sentinel HONG")
        with mock.patch.dict(CA, {"t_fixture": sentinel}, clear=True):
            hang, chi_tiet = chay_ca_trong_tien_trinh("t_fixture")
        bang(hang == ket_qua and goi.count(ket_qua) == 1,
             f"runner/{ket_qua}: phai goi dung mot lan va giu phan hang, duoc {hang}/{chi_tiet}, calls={goi}")
        bang(ket_qua == "DAT" or "review sentinel" in chi_tiet,
             f"runner/{ket_qua}: mat ly do goc {chi_tiet!r}")


@ca_tu_kiem
def t93_main_ket_luan_va_ma_thoat_theo_duong_goi_that():
    """Luot 6 (lop chot-yaml, tang 'duong goi that' tiep theo — executor tu liet ke): CI chi doc MA THOAT cua tien trinh (buoc `run` cua GitHub Actions theo tai lieu).
    (1) `main` phai tra rc=1 + `TONG: DO` khi BAT KY dieu kien nao hong (ca do, dot bien khong giet, xau, tu kiem, ten trung),
    va dong `CA:`/`DOT BIEN:` in dung tu so/mau. (2) `__main__` phai chuyen ma cua `main` ra ma thoat that (tien trinh con)."""
    import io
    n, m = len(CA), len(DOT_BIEN)
    ds_trung = list(DOT_BIEN) + list(DOT_BIEN[:1])
    kich_ban = (
        ("sach", {}, 0),
        ("mot ca do", {"chay_ca_trong_tien_trinh": lambda t: ("DO", "gia") if t == next(iter(CA)) else ("DAT", "")}, 1),
        ("dot bien thieu giet", {"chay_tap_dot_bien": lambda _: (m - 1, [])}, 1),
        ("co xau", {"chay_tap_dot_bien": lambda _: (m, ["x: HONG"])}, 1),
        ("tu kiem hong", {"tu_kiem_phan_hang": lambda: ["gia"]}, 1),
        ("ten dot bien trung", {"DOT_BIEN": ds_trung, "TEN_DOT_BIEN": [d[0] for d in ds_trung],
                                "chay_tap_dot_bien": lambda _: (len(ds_trung), [])}, 1),
    )
    for ten, va, mong in kich_ban:
        ra = io.StringIO()
        goc = {"CAY": ROOT_THAT, "chay_ca_trong_tien_trinh": lambda _: ("DAT", ""),
               "chay_tap_dot_bien": lambda _: (m, []), "tu_kiem_phan_hang": lambda: [], "dong_kiem_ke": lambda: "KIEM KE: gia"}
        with mock.patch.dict(globals(), {**goc, **va}, clear=False), contextlib.redirect_stdout(ra):
            rc = main([])
        dong = ra.getvalue().splitlines()
        bang(rc == mong and dong[-1] == ("TONG: DAT" if mong == 0 else "TONG: DO"), f"main/{ten}: rc={rc} mong {mong}, dong cuoi {dong[-1:]}")
        dong_ca = {"sach": f"CA: {n}/{n} dat · 0 do · 0 hong", "mot ca do": f"CA: {n - 1}/{n} dat · 1 do · 0 hong"}.get(ten)
        dong_db = {"sach": f"DOT BIEN: {m}/{m} bi giet dung ly do", "dot bien thieu giet": f"DOT BIEN: {m - 1}/{m} bi giet dung ly do"}.get(ten)
        for mong_dong in (dong_ca, dong_db):
            bang(mong_dong is None or mong_dong in dong,
                 f"main/{ten}: thieu dong {mong_dong!r} (tu so phai la so dem THAT, khong phai mau): "
                 f"{[d for d in dong if d.startswith(('CA:', 'DOT BIEN:'))]}")
        tk = "TU KIEM PHAN HANG: " + ("DO" if ten == "tu kiem hong" else "DAT") + \
            f" ({len(MAU_RC)} mau rc, {len(TU_KIEM_DOT_BIEN)} dot bien that)"
        bang([d for d in dong if d.startswith("TU KIEM PHAN HANG:")] == [tk], f"main/{ten}: dong tu kiem phai DUNG {tk!r}")
        if ten == "sach":
            nhan = ("CA:", "DOT BIEN:", "KIEM KE:", "TU KIEM PHAN HANG:", "TONG:")
            bang([d for d in dong if d.startswith(nhan)] == [dong_ca, dong_db, "KIEM KE: gia", tk, "TONG: DAT"],
                 f"main/{ten}: tap dong tong ket phai khop DUNG: {[d for d in dong if d.startswith(nhan)]}")
    r = subprocess.run([sys.executable, "-B", str(CAY / "ops" / "ci_duong_nhanh_test.py"), "doi-so-la"],
                       capture_output=True, timeout=60, env=dict(os.environ, PYTHONDONTWRITEBYTECODE="1"))
    bang(r.returncode == 2, f"__main__ phai chuyen ma cua main (2 voi doi so la) ra ma thoat that, duoc rc={r.returncode}")


@ca_tu_kiem
def t94_main_in_dong_kiem_ke_that():
    """Do output cua main voi runner con gia de tranh de quy; so dem van tu CA/DOT_BIEN that."""
    import io
    ra = io.StringIO()
    with mock.patch.dict(globals(), {
        "CAY": ROOT_THAT,
        "chay_ca_trong_tien_trinh": lambda _: ("DAT", ""),
        "chay_tap_dot_bien": lambda _: (len(DOT_BIEN), []),
        "tu_kiem_phan_hang": lambda: [],
    }, clear=False), contextlib.redirect_stdout(ra):
        rc = main([])
    dong = [d for d in ra.getvalue().splitlines() if d.startswith("KIEM KE:")]
    bang(rc == 0 and dong == [dong_kiem_ke()],
         "main phai in dung mot dong KIEM KE duoc doi chieu doc lap boi t96")


@ca_tu_kiem
def t95_lan_chay_day_du_chi_do_kho_chua_test():
    bang(loi_cay_duoi_do(ROOT_THAT, ROOT_THAT) == "", "kho that phai duoc nhan")
    bang(loi_cay_duoi_do(Path(tempfile.gettempdir()), ROOT_THAT) != "", "cay khac kho chua test phai bi tu choi o lan chay day du")
    # Kiem DUONG GOI main, khong chi helper; vo hieu hoa bo ca de khong de quy.
    import io
    with tempfile.TemporaryDirectory(prefix="cdn_main_scope_") as d:
        ra, err = io.StringIO(), io.StringIO()
        with mock.patch.dict(globals(), {"CAY": Path(d), "CA": {}}, clear=False), \
             mock.patch.dict(globals(), {"chay_tap_dot_bien": lambda _: (0, []),
                                         "tu_kiem_phan_hang": lambda: []}, clear=False), \
             contextlib.redirect_stdout(ra), contextlib.redirect_stderr(err):
            rc = main([])
        bang(rc == 2 and "CAY DUOI DO KHAC KHO CHUA TEST" in err.getvalue()
             and "CA:" not in ra.getvalue() and "TONG:" not in ra.getvalue(),
             "main phai tu choi cay ngoai TRUOC khi chay/in ket qua suite")


# ---------------------------------------------------------------- tự kiểm của chính bộ test
@ca_tu_kiem
def t96_phan_hoach_ca_khong_giao_nhau_va_phu_kin():
    """Lop bang-do (P3 luot 4, va luot 5 tu do): phan nhom theo TIEN TO da tu lech hai lan (tai 7b8c856 kiem ke theo tien to
    khai 38/12/3, do that 35/12/3/3; roi t96 — mot ca tu kiem — bi dem la "hanh vi"). Nay nhom `tu_kiem` KHAI tai cho
    (`@ca_tu_kiem`) va duoc doi chieu voi DAU HIEU AST DOC LAP: ca nao cham noi tang cua chinh bo test (`CA`, `DOT_BIEN`, phan
    hang, docstring, tep test) la tu kiem, va nguoc lai. Dong `KIEM KE:` in ra (neo cua moi bang so) phai khop so dem doc lap."""
    nhom = phan_hoach_ca()
    moi = [ten for ds in nhom.values() for ten in ds]
    bang(len(moi) == len(set(moi)) == len(CA) and set(moi) == set(CA), "phan hoach phai phu kin va khong giao nhau")
    cay = ast.parse((HERE / "ci_duong_nhanh_test.py").read_text(encoding="utf-8"))
    cham_noi_tang = set()
    for nut in cay.body:
        if isinstance(nut, ast.FunctionDef) and nut.name in CA:
            for x in ast.walk(nut):
                ten_x = x.id if isinstance(x, ast.Name) else (x.value if isinstance(x, ast.Constant) else None)
                if ten_x in DAU_HIEU_TU_KIEM:
                    cham_noi_tang.add(nut.name)
    bang(set(nhom["tu_kiem"]) == cham_noi_tang,
         f"nhom tu_kiem lech dau hieu AST: khai ma khong cham noi tang {sorted(set(nhom['tu_kiem']) - cham_noi_tang)}, "
         f"cham noi tang ma khong khai {sorted(cham_noi_tang - set(nhom['tu_kiem']))}")
    con_lai = [n for n in CA if n not in cham_noi_tang]
    doc_lap = {"hanh_vi": [n for n in con_lai if n.startswith("t")], "cau_truc_yaml": [n for n in con_lai if n.startswith("y")],
               "so_dang_ky": [n for n in con_lai if n.startswith("k")], "tu_kiem": [n for n in CA if n in cham_noi_tang]}
    bang(nhom == doc_lap, f"phan hoach lech quy tac doc lap: {[(k, len(v), len(doc_lap[k])) for k, v in nhom.items()]}")
    dem_tep = {}
    for d in DOT_BIEN:
        dem_tep[d[1][0]] = dem_tep.get(d[1][0], 0) + 1
    so = dict(re.findall(r"([\w./-]+)=(\d+)", dong_kiem_ke()))
    mong = {**{k: str(len(v)) for k, v in doc_lap.items()}, **{t: str(n) for t, n in dem_tep.items()}}
    bang(so == mong and dong_kiem_ke().count(f"= {len(CA)} ·") == 1 and dong_kiem_ke().endswith(f"= {len(DOT_BIEN)}"),
         f"dong KIEM KE lech so dem doc lap: {dong_kiem_ke()!r} != {mong}")


@ca_tu_kiem
def t97_harness_khong_cap_giet_khi_khong_co_bang_chung_duong():
    """Cross-review luot 3 (P2): `dich=()` va iterator bi tieu thu deu ra GIET gia (`all([])`). Kiem o BA cua: callee
    (`chay_mot_dot_bien`), caller (`chay_tap_dot_bien`), va ten ca khong ton tai."""
    vo_hai = (MA, lambda vb: thay_mot(vb, "TOI_DA_TEN_IN = 5\n", "TOI_DA_TEN_IN = 5  # vo hai\n"))
    that = (MA, lambda vb: thay_mot(vb, '"ops/reviews/", "ops/specs/")\nMAU_SHA', '"ops/reviews/", "ops/specs/", "scripts/")\nMAU_SHA'))
    t01, t02 = "t01_toan_ho_so_duong_nhanh", "t02_co_tep_ma_day_du"
    for ten, dich in (("rong", ()), ("ten la", ("ca_khong_ton_tai",)), ("iterator rong", iter(()))):
        hang, _ = chay_mot_dot_bien("vo_hai_" + ten, vo_hai, dich)
        bang(hang == "HONG", f"callee: dich {ten} phai la HONG (khong co bang chung duong), duoc {hang}")
    for ten, dich in (("tuple", (t01,)), ("iterator", iter((t01,))), ("generator", (x for x in (t01,)))):
        hang, _ = chay_mot_dot_bien("vo_hai_" + ten, vo_hai, dich)
        bang(hang == "SONG_SOT", f"callee: dot bien VO HAI voi dich {ten} phai SONG_SOT (khong bao gio GIET), duoc {hang}")
        hang, _ = chay_mot_dot_bien("that_" + ten, that, (x for x in (t02,)) if ten == "generator" else (iter((t02,)) if ten == "iterator" else (t02,)))
        bang(hang == "GIET", f"callee: dot bien THAT voi dich {ten} phai GIET, duoc {hang}")
    # ca dich DO san tren ban goc thi lượt giet khong quy duoc cho dot bien => HONG, khong duoc GIET
    do_san = lambda ten_ca, cay: (3, f"DO:{ten_ca}:do san")   # noqa: E731
    hang, _ = chay_mot_dot_bien("do_san", that, (t02,), chay=do_san)
    bang(hang == "HONG", f"ca dich do san tren ban goc phai la HONG (kiem chung ban goc), duoc {hang}")
    giet, xau = chay_tap_dot_bien([("a_rong", vo_hai, ()), ("b_iter_vo_hai", vo_hai, iter((t01,))), ("c_ten_la", vo_hai, ("khong_co",))])
    bang(giet == 0 and all(any(x.startswith(t) for x in xau) for t in ("a_rong", "b_iter_vo_hai", "c_ten_la")),
         f"caller: ba muc khong co bang chung phai deu KHONG bi giet va deu vao danh sach xau: giet={giet} xau={xau}")
    giet, xau = chay_tap_dot_bien([("d_iter_that", that, iter((t02,)))])
    bang(giet == 1 and not xau, f"caller: iterator hop le + dot bien that phai GIET dung 1: giet={giet} xau={xau}")


@ca_tu_kiem
def t98_docstring_khong_ghim_so_ca_va_khoang_ten():
    """Bang giao/docstring troi so HAI luot lien (P3 luot 1 va luot 2): so ca, so dot bien va khoang `tNN..tMM` chi nguon
    duy nhat la `CA`/`DOT_BIEN`. Docstring cua module va cua `ops/ci_duong_nhanh.py` khong duoc ghim chung."""
    mau = re.compile(r"\b\d+\s*/\s*\d+\s*(?:ca|dot bien|đột biến)|`?t\d\d`?\s*(?:\.\.|–|-)\s*`?t\d\d"
                     r"|\b(?:\d+|NĂM|BA|BỐN|SÁU|BẢY|TÁM|năm|ba|bốn|sáu|bảy|tám)\s+(?:mẫu rc|đột biến (?:thật|thực))")
    ma_sp = ast.get_docstring(ast.parse((CAY / "ops" / "ci_duong_nhanh.py").read_text(encoding="utf-8"))) or ""
    for ten, doc in (("ci_duong_nhanh_test.py (module dang chay)", globals().get("__doc__") or ""), ("ci_duong_nhanh.py", ma_sp)):
        thay = mau.findall(doc)
        bang(not thay, f"{ten}: docstring ghim so ca/khoang ten (se troi): {thay}")


# ---- lop `bang-do-thieu-neo-va-thieu-kiem-ke` (cross-review luot 15): con so trong van xuoi la PHEP DO tai MOT thoi diem; khong
# neo thi no troi khi merge master ma khong ai thay. Don vi neo la CAU, trong MOI doan docstring va MOI khoi chu thich, o CA hai tep.
MAU_TACH_DOAN = re.compile(r"\n[ \t]*\n|\n[ \t]*(?=·\s)")
MAU_TACH_CAU = re.compile(r"(?<=[.;!?])\s+")
MAU_SO_TRONG_VAN = re.compile(r"\d+(?:[.,/]\d+)*")
MAU_NGAY = re.compile(r"(?<!\d)(?:\d{1,2}-\d{1,2}-\d{4}|\d{4}-\d{1,2}-\d{1,2})(?!\d)")
MODE_GIT_HOP_LE = frozenset({"000000", "100644", "100755", "120000", "160000"})
# Danh sach CHO PHEP (khong phai danh sach CAM): ngu canh NGAY TRUOC con so lam no thanh DINH DANH hay MA, khong phai so do.
# Con so khong khop dang nao o day la SO DO, va CHINH cau chua no phai co neo.
TRUOC_KHONG_PHAI_SO_DO = re.compile(
    r"(?:[^\W\d]-?"                                                            # dinh danh: t20zh, r2, F821, UTF-8
    r"|#|\bissues/|\bpull/|\brun |\bcomment "                                   # so hieu Issue/PR/run/comment
    r"|(?i:\b(?:lượt|luot|lần thứ|lan thu|lan|tầng|nghiệm thu|nghiem thu)) "     # so thu tu luot/tang/nghiem thu
    r"|[^\W\d]=-?"                                                             # khoa=gia tri: rc=8, rc=-9, size=40
    r"|(?:==|!=|<=|>=|<|>) ?"                                                  # phep so sanh
    r"|(?i:\b(?:exit|thoát|thoat)) )$")                                         # ma thoat
# Neo: SHA (bay toi bon muoi ky tu hex, co CA chu a-f LAN chu so) hoac dinh danh BEN cua nguon ngoai (run CI, comment).
MAU_NEO_SO_DO = re.compile(r"(?<![0-9A-Za-z_])(?=[0-9a-f]*[a-f])(?=[0-9a-f]*[0-9])[0-9a-f]{7,40}(?![0-9A-Za-z_])"
                           r"|\brun \d{6,}|\bcomment \d{6,}|\bissuecomment-\d{6,}")
# So do ve KHO viet bang CHU (cross-review luot 16): tu-so dung NGAY truoc danh tu thuc the kho van la so do va phai co neo;
# `ca`/`cả` dung truoc (`CA hai tep` = ca hai, dem cau truc) thi khong. Quy uoc khong doi: so do ve kho viet bang chu so.
MAU_SO_CHU_KHO = re.compile(r"(?i)(?<!\bca )(?<!\bcả )(?<![\w-])(?:hai|ba|bốn|bon|năm|sáu|bảy|tám|chín|mười|mươi|muoi|trăm|tram)"
                            r"\s+(?:tệp|tep|lease|merge|PR|ref|nhánh|nhanh)(?![\w-])")
# So do trong THONG BAO `bang(...)` (cross-review luot 16): chi so dung NGAY sau dau hieu do viet thuong (`do `/`đo `); so cau
# truc trong thong bao (gia tri `fetch-depth`, ma `rc`, kich thuoc bang) khong phai so do.
MAU_SO_DO_THONG_BAO = re.compile(r"(?<![\w])(?:do|đo) (\d+(?:[.,/]\d+)*)(?![\w/])")
# LUAT cua bo test (doc lap voi MAU_SO_CHU_KHO, KHONG sinh bieu thuc tu day): moi tu-so va moi danh tu kho bieu thuc phai bat —
# mau tu kiem cua t98b sinh tu hai bo nay, nen go mot nhanh khoi bieu thuc thi mau cua nhanh ay lech.
SO_CHU_LUAT = ("hai", "ba", "bốn", "bon", "năm", "sáu", "bảy", "tám", "chín", "mười", "mươi", "muoi", "trăm", "tram")
DANH_TU_KHO_LUAT = ("tệp", "tep", "lease", "merge", "PR", "ref", "nhánh", "nhanh")


def cau_tai_lieu(nguon):
    """(dong, loai, cau) cho MOI cau cua MOI doan docstring (module/class/def; doan tach theo dong trong va gach `·`) va cua
    MOI khoi chu thich (cac dong `#` lien tiep)."""
    import io
    import tokenize
    doan = []
    for nut in ast.walk(ast.parse(nguon)):
        if isinstance(nut, (ast.Module, ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
            d = ast.get_docstring(nut, clean=False)
            if d:
                doan += [(nut.body[0].lineno, "docstring", p) for p in MAU_TACH_DOAN.split(d)]
    khoi = []
    for tok in tokenize.generate_tokens(io.StringIO(nguon).readline):
        if tok.type == tokenize.COMMENT:
            if khoi and khoi[-1][3] == tok.start[0] - 1:
                khoi[-1] = (khoi[-1][0], "chu thich", khoi[-1][2] + "\n" + tok.string, tok.start[0])
            else:
                khoi.append((tok.start[0], "chu thich", tok.string, tok.start[0]))
    doan += [k[:3] for k in khoi]
    return [(dong, loai, cau) for dong, loai, p in doan for cau in MAU_TACH_CAU.split(p) if cau.strip()]


def cau_thong_bao(nguon):
    """(dong, loai, cau) cho MOI cau cua phan TINH cua doi so thu hai cua MOI loi goi `bang(...)` (chuoi hoac f-string)."""
    ra = []
    for nut in ast.walk(ast.parse(nguon)):
        if isinstance(nut, ast.Call) and isinstance(nut.func, ast.Name) and nut.func.id == "bang" and len(nut.args) >= 2:
            a = nut.args[1]
            phan = [a] if isinstance(a, ast.Constant) else list(a.values) if isinstance(a, ast.JoinedStr) else []
            txt = " ".join(p.value for p in phan if isinstance(p, ast.Constant) and isinstance(p.value, str))
            ra += [(nut.lineno, "thong bao", cau) for cau in MAU_TACH_CAU.split(txt) if cau.strip()]
    return ra


def so_do_trong_cau(cau):
    """Con so trong `cau` KHONG thuoc dang cho phep (dinh danh, ngay, so hieu, ma, mode git, danh so `(N)`/`[N]`)."""
    ngay = [k.span() for k in MAU_NGAY.finditer(cau)]
    so = []
    for k in MAU_SO_TRONG_VAN.finditer(cau):
        a, b = k.span()
        truoc, sau = cau[:a], cau[b:]
        if (any(x <= a and b <= y for x, y in ngay) or sau[:1].isalpha() or sau[:1] == "_"
                or TRUOC_KHONG_PHAI_SO_DO.search(truoc[-30:])
                or (truoc[-1:], sau[:1]) in (("(", ")"), ("[", "]"))
                or set(re.split(r"[/,]", k.group())) <= MODE_GIT_HOP_LE):
            continue
        so.append(k.group())
    so += [k.group() for k in MAU_SO_CHU_KHO.finditer(cau)]
    return so


def so_do_khong_neo(nguon):
    """(so con so do tim thay, [(dong, loai, cac so, cau)] cua moi cau co so do ma KHONG co neo trong CHINH cau ay)."""
    tong, thieu = 0, []
    for dong, loai, cau in cau_tai_lieu(nguon) + cau_thong_bao(nguon):
        so = MAU_SO_DO_THONG_BAO.findall(cau) if loai == "thong bao" else so_do_trong_cau(cau)
        tong += len(so)
        if so and not MAU_NEO_SO_DO.search(cau):
            thieu.append((dong, loai, so, " ".join(cau.split())[:120]))
    return tong, thieu


@ca_tu_kiem
def t98b_moi_so_do_trong_docstring_va_chu_thich_phai_co_neo():
    """Cross-review luot 15 (`bang-do-thieu-neo-va-thieu-kiem-ke`): con so trong van xuoi la PHEP DO tai MOT commit. Khong neo
    thi no troi khi merge master: ti le lease cua D2 giu mau so cu sau merge 20ec8d5 trong khi tu so dung NGAU NHIEN (cung
    sau tep cu). Cau nao co so do thi CHINH cau ay phai co neo: SHA (co ca chu a-f lan chu so) hoac dinh danh ben cua nguon
    ngoai (`run <id>`, `comment <id>`).

    Duong vao, moi duong mot mau tu kiem va mot dot bien rieng: docstring MODULE · docstring HAM/CLASS · CHU THICH · neo o
    CAU KHAC · so tran khong phai ti le (thoi gian, phan tram, so dem) · so thuan bi nham la neo · tep TEST (khong chi san
    pham) · so viet bang CHU dung truoc danh tu thuc the kho (MOI tu-so va MOI danh tu cua mau mot mau tu kiem, sinh tu
    `SO_CHU_LUAT`/`DANH_TU_KHO_LUAT` doc lap voi bieu thuc) · so dung sau dau hieu do (`do`/`đo`) trong THONG BAO `bang(...)` ·
    neo phai co CHU SO (tu hex toan chu khong phai neo) · `;` la ranh gioi CAU, gach dau dong la ranh gioi DOAN. Dang KHONG
    phai so do (dinh danh, ngay, so hieu, ma thoat, mode git, danh so) la danh sach CHO PHEP `TRUOC_KHONG_PHAI_SO_DO`, khong
    phai danh sach don vi doan truoc.

    Gioi han, noi thang: (a) so viet bang CHU ngoai mau tu-so + danh tu kho (vd dem ca, buoc, lop; tu-so khong dau `nam`
    `sau` `bay` `tam` `chin` vi trung tu thuong) ca nay KHONG thay — quy uoc: so do ve KHO viet bang chu so, so dem CAU TRUC
    viet bang chu thi do o ca so huu no (vd `t20zh`); (b) chot do su CO MAT cua neo, khong kiem SHA ton tai (clone nong se
    do oan), cung KHONG kiem so hang, luong tu hay NGUON (ai do) cua cau co neo — neo chi de do lai duoc; (c) mot neo phu moi
    so trong cung cau; (d) trong thong bao `bang(...)` chi so dung NGAY sau `do `/`đo ` moi bi bat, so do viet kieu khac
    (khong dau hieu) thi khong."""
    # (1) Tu kiem bo quet: moi DUONG VAO mot mau phai bi bao; mau co neo hoac toan dang cho phep thi khong.
    mau = (
        ('"""Kho co 6/119 lease."""\n', True),                                      # ti le, docstring MODULE
        ('def f():\n    """Ba ca chay mat 7 giay."""\n', True),                     # docstring HAM, so tran (thoi gian)
        ('class K:\n    """Chiem 13% so PR."""\n', True),                            # docstring CLASS, phan tram
        ('x = 1  # 3 tep .gitattributes duoi ops/reviews\n', True),                 # CHU THICH
        ('"""Do tai 20ec8d5c. Kho co 119 lease."""\n', True),                       # neo o CAU KHAC
        ('"""HEAD 6803012: chay 5 nhanh."""\n', True),                              # so thuan KHONG phai neo
        ('"""Kho co 6/119 lease tai 3569472cb9, run 36518707072 mat 52 phut."""\n', False),
        ('"""Luot 15, LAN THU 4, rc=3, rc=-9, N>0, mode 100644, #674, 01-10-2026, (1), CHAN [8], UTF-8, t20zh."""\n', False),
        # cross-review luot 16: moi nhanh moi cua bo quet mot mau (go nhanh ay thi mau ay lech)
        ('"""Kho co 119 lease (xem effaced)."""\n', True),                     # neo phai co CHU SO
        ('"""Do tai 3569472cb9; kho co 119 lease."""\n', True),                # `;` la ranh gioi CAU
        ('"""Do tai 3569472cb9:\n  · kho co 119 lease\n"""\n', True),          # gach dau dong la ranh gioi DOAN
        ('"""Master co ba tep lease."""\n', True),                             # so do ve KHO viet bang CHU
        ('"""Quet CA hai tep."""\n', False),                                   # `ca hai` la dem cau truc
        ('bang(x, f"loi (do 8/63 lan merge): {y}")\n', True),                  # so do trong THONG BAO
        ('bang(x, f"chuan-bi DO thi fetch-depth 0, rc={y}, 20 o")\n', False),  # so cau truc trong thong bao
        ('bang(x, "loi (đo 8/63 lan merge)")\n', True),                      # dau hieu `đo` (co dau), chuoi THUONG
    ) + tuple((f'"""Kho co {so} tep."""\n', True) for so in SO_CHU_LUAT) \
      + tuple((f'"""Kho co ba {dt}."""\n', True) for dt in DANH_TU_KHO_LUAT)
    bang(len(SO_CHU_LUAT) > 1 and len(DANH_TU_KHO_LUAT) > 1, "ha tang: luat tu-so/danh tu kho rong")
    lech = [(nguon, mong) for nguon, mong in mau if bool(so_do_khong_neo(nguon)[1]) is not mong]
    bang(not lech, f"bo quet so do lech mau tu kiem (nguon, mong bi bao): {lech}")
    # (2) Cay duoi do: CA hai tep; moi tep phai CON so do (ca co MAT phai co DO) va moi so do phai co neo trong cung cau.
    dem, thieu = {}, []
    for tep in (CAY / "ops" / "ci_duong_nhanh.py", CAY / "ops" / "ci_duong_nhanh_test.py"):
        dem[tep.name], th = so_do_khong_neo(tep.read_text(encoding="utf-8"))
        thieu += [(tep.name, *x) for x in th]
    bang(set(dem) == {"ci_duong_nhanh.py", "ci_duong_nhanh_test.py"} and all(dem.values()),
         f"ha tang: phai quet DUNG hai tep va moi tep phai con so do (khong thi ca khong do gi): {dem}")
    bang(not thieu, f"so do trong docstring/chu thich KHONG co neo trong cung cau (se troi khi merge master): {thieu}")


# ---- lop `khang-dinh-dinh-tinh-rong-hon-phep-do` (cross-review luot 16): cau nhac nen CI (GitHub, Actions, actions/checkout,
# ruleset) noi ve mot he thong ma ca offline khong chay duoc, nen chinh cau ay phai mang nhan muc bao dam (KHONG DO DUOC, chua
# tu do, theo tai lieu, khong ngoai suy) hoac neo mot phep do that. Don vi la CAU, nhu t98b.
MAU_NHAC_NEN = re.compile(r"\bGitHub\b|\bActions\b|actions/checkout|\b[Rr]uleset\b")
MAU_NHAN_BAO_DAM = re.compile(r"(?i:không đo được|chưa (?:tự )?đo|theo tài liệu|không ngoại suy)"
                              r"|KHONG DO DUOC|CHUA DO\b|chua tu do|chua do tren|theo tai lieu|khong ngoai suy")


def nhac_nen_khong_nhan(nguon):
    """(so cau nhac nen CI, [(dong, loai, cau)] cua moi cau nhac nen ma KHONG co nhan muc bao dam hay neo trong CHINH cau ay)."""
    tong, thieu = 0, []
    for dong, loai, cau in cau_tai_lieu(nguon):
        if MAU_NHAC_NEN.search(cau):
            tong += 1
            if not (MAU_NHAN_BAO_DAM.search(cau) or MAU_NEO_SO_DO.search(cau)):
                thieu.append((dong, loai, " ".join(cau.split())[:140]))
    return tong, thieu


@ca_tu_kiem
def t98c_khang_dinh_ve_nen_ci_phai_mang_nhan_bao_dam():
    """Cross-review luot 16 (`khang-dinh-dinh-tinh-rong-hon-phep-do`): docstring D2 khai nhu SU THAT mot dieu CHUA DO ve
    checkout cua runner, trong khi cac cau khac ve GitHub cung tep da mang nhan. Lop nay khong co phep do offline,
    nen chot la NHAN: cau nao nhac nen CI thi CHINH cau ay phai noi muc bao dam (KHONG DO DUOC, chua tu do, theo tai lieu,
    khong ngoai suy) hoac neo phep do that (SHA, run, comment) — o CA hai tep.

    Duong vao, moi duong mot mau tu kiem va mot dot bien rieng: tung nhanh cua `MAU_NHAC_NEN` · nhan o CAU KHAC · docstring HAM · CHU THICH. Doc docstring/chu thich bang CHINH `cau_tai_lieu` cua t98b, nen dot bien
    bo quet chung (chi docstring module, bo chu thich, khong tach cau) phai lam CA HAI ca do.

    Gioi han, noi thang: (a) cau noi ve hanh vi nen CI ma KHONG goi ten nen (vd chi noi `merge ref`, `skipped`, `context`) ca
    nay khong thay — quy uoc: khang dinh ve hanh vi nen thi goi ten nen; (b) chot do su CO MAT cua nhan, khong do khang dinh
    dung hay sai, theo tai lieu GitHub hay khong (khong mang thi KHONG DO DUOC); (c) `github.sha`, `.github/` chu thuong la
    dinh danh, khong tinh la nhac nen."""
    mau = (
        ('"""GitHub khong dung merge ref cho PR xung dot."""\n', True),           # MAU_NHAC_NEN (1)
        ('"""Checkout cua Actions chi co ref cua PR."""\n', True),                 # MAU_NHAC_NEN (2)
        ('x = 1  # actions/checkout lay moi nhanh\n', True),                       # MAU_NHAC_NEN (3), CHU THICH
        ('def f():\n    """Ruleset doi ba check."""\n', True),                     # MAU_NHAC_NEN (4), docstring HAM
        ('"""GitHub lam vay. Dieu nay theo tai lieu."""\n', True),                # nhan o CAU KHAC
        ('"""GitHub khong chay workflow khi PR xung dot (theo tai lieu, chua tu do)."""\n', False),
        ('"""Checkout cua Actions: KHÔNG ĐO ĐƯỢC offline."""\n', False),
        ('"""Do tren GitHub: run 36518707072."""\n', False),                      # neo phep do that
        ('"""Lay `github.sha` tu `.github/workflows/ci.yml`."""\n', False),        # chu thuong: dinh danh
    )
    lech = [(nguon, mong) for nguon, mong in mau if bool(nhac_nen_khong_nhan(nguon)[1]) is not mong]
    bang(not lech, f"bo quet khang dinh nen CI lech mau tu kiem (nguon, mong bi bao): {lech}")
    dem, thieu = {}, []
    for tep in (CAY / "ops" / "ci_duong_nhanh_test.py", CAY / "ops" / "ci_duong_nhanh.py"):
        dem[tep.name], th = nhac_nen_khong_nhan(tep.read_text(encoding="utf-8"))
        thieu += [(tep.name, *x) for x in th]
    bang(set(dem) == {"ci_duong_nhanh.py", "ci_duong_nhanh_test.py"} and all(dem.values()),
         f"ha tang: phai quet DUNG hai tep va moi tep phai con cau nhac nen CI (khong thi ca khong do gi): {dem}")
    bang(not thieu, f"cau nhac nen CI KHONG mang nhan muc bao dam hay neo trong cung cau: {thieu}")


@ca_tu_kiem
def t99_khong_doi_kieu_ngoai_le_thanh_tin_hieu():
    """Bộ phân hạng tin `TinHieuChotCa`; nên KHÔNG có `except` nào bắt ngoại lệ RỘNG mà lại ném/gọi tín hiệu ấy —
    làm vậy thì lỗi vô can của bản đột biến (TypeError...) hoá thành 'giết thật' (đã trả giá ở #355/#359)."""
    cay = ast.parse((HERE / "ci_duong_nhanh_test.py").read_text(encoding="utf-8"))
    xau = []
    for nut in ast.walk(cay):
        if isinstance(nut, ast.ExceptHandler):
            ten = nut.type
            ten_ds = [ten] if not isinstance(ten, ast.Tuple) else list(ten.elts)
            rong = ten is None or any(isinstance(t, ast.Name) and t.id in ("Exception", "BaseException", "AssertionError")
                                      for t in ten_ds)
            dung_tin_hieu = any(
                (isinstance(n, ast.Raise) and n.exc is not None and "TinHieuChotCa" in ast.unparse(n.exc))
                or (isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id == "bang")
                for n in ast.walk(nut))
            if rong and dung_tin_hieu:
                xau.append(nut.lineno)
    bang(not xau, f"except RONG ma ném/goi TinHieuChotCa o dong {xau}")


# ---------------------------------------------------------------- chạy ca và đột biến
def phan_hoach_ca():
    """Phan hoach `CA` thanh cac nhom KHONG GIAO NHAU (nguon duy nhat cho moi bang kiem ke; `goi/kiem_ke.py` goi ham nay)."""
    nhom = {"hanh_vi": [], "cau_truc_yaml": [], "so_dang_ky": [], "tu_kiem": []}
    for ten in CA:
        if ten in TU_KIEM_KHAI:
            nhom["tu_kiem"].append(ten)
        elif ten[0] == "t":
            nhom["hanh_vi"].append(ten)
        elif ten[0] == "y":
            nhom["cau_truc_yaml"].append(ten)
        elif ten[0] == "k":
            nhom["so_dang_ky"].append(ten)
        else:
            raise RuntimeError(f"ha tang: ca {ten!r} khong thuoc nhom nao")
    return nhom


def dong_kiem_ke(nhom=None):
    """Dong KIEM KE in ra cung ket qua suite: moi bang/lo khai so nhom phai trich TU dong nay (neo = output suite)."""
    nhom = phan_hoach_ca() if nhom is None else nhom
    theo_tep = {}
    for _, (tep, _), _ in DOT_BIEN:
        theo_tep[tep] = theo_tep.get(tep, 0) + 1
    return ("KIEM KE: ca " + " + ".join(f"{k}={len(v)}" for k, v in nhom.items()) + f" = {sum(len(v) for v in nhom.values())}"
            + " · dot bien " + " + ".join(f"{t}={n}" for t, n in sorted(theo_tep.items())) + f" = {sum(theo_tep.values())}")


def chay_ca_trong_tien_trinh(ten):
    try:
        CA[ten]()
    except TinHieuChotCa as e:
        return "DO", str(e)
    except Exception as e:
        return "HONG", f"{type(e).__name__}: {e}"
    return "DAT", ""


def phan_hang(rc, dau_ra, ten_dich):
    """rc của tiến trình con chạy ca đích trên bản đột biến → GIET · TIN_DUNG_GIA · SONG_SOT · HONG."""
    if rc == 0:
        return "SONG_SOT"
    if rc == 3:
        return "GIET" if f"DO:{ten_dich}:" in dau_ra else "TIN_DUNG_GIA"
    if rc == 4:
        return "TIN_DUNG_GIA"
    return "HONG"


def chay_con(ten_ca, cay, thoi_han=120):
    env = dict(os.environ, CI_DUONG_NHANH_CAY=str(cay), PYTHONDONTWRITEBYTECODE="1")
    r = subprocess.run([sys.executable, "-B", str(HERE / "ci_duong_nhanh_test.py"),
                        "--nguon-test", str(Path(cay) / "ops" / "ci_duong_nhanh_test.py"), "--mot-ca", ten_ca],
                       capture_output=True, env=env, timeout=thoi_han)
    return r.returncode, (r.stdout + r.stderr).decode("utf-8", "replace")


def dung_cay_tam(thay):
    """Bản sao TỐI THIỂU của cây: chỉ những tệp mà các ca đọc. `thay` = {đường dẫn: văn bản mới}."""
    goc = Path(tempfile.mkdtemp(prefix="cdn_cay_"))
    for dp in ("ops/ci_duong_nhanh.py", "ops/ci_duong_nhanh_test.py", ".claude/dev/ci_dang_ky_test.py", "ops/lease_publish.py"):
        (goc / dp).parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT_THAT / dp, goc / dp)
    (goc / ".github/workflows").mkdir(parents=True, exist_ok=True)
    for tep in (ROOT_THAT / ".github/workflows").glob("*.yml"):
        shutil.copyfile(tep, goc / ".github/workflows" / tep.name)
    m = nap_so_dang_ky_tu(ROOT_THAT)
    song, _, _ = m["tim"](ROOT_THAT)
    for dp in song | {DA_NOI_MUC}:
        if not (goc / dp).exists():
            (goc / dp).parent.mkdir(parents=True, exist_ok=True)
            (goc / dp).write_text("# cho\n", encoding="utf-8")
    for dp, vb in thay.items():
        (goc / dp).write_text(vb, encoding="utf-8")
    return goc


def nap_so_dang_ky_tu(goc):
    import runpy
    return runpy.run_path(str(goc / ".claude" / "dev" / "ci_dang_ky_test.py"))


def doc(dp):
    return (ROOT_THAT / dp).read_text(encoding="utf-8")


def thay_mot(vb, cu, moi):
    n = vb.count(cu)
    if n != 1:
        raise RuntimeError(f"ha tang: neo dot bien phai xuat hien DUNG MOT lan, thay {n}: {cu[:70]!r}")
    kq = vb.replace(cu, moi)
    if kq == vb:
        raise RuntimeError("ha tang: dot bien khong doi gi")
    return kq


def thay_regex(vb, mau, moi, co=re.S):
    kq, n = re.subn(mau, moi, vb, count=0, flags=co)
    if n != 1:
        raise RuntimeError(f"ha tang: neo regex phai khop DUNG MOT lan, thay {n}: {mau[:70]!r}")
    return kq


MA, YML, DK = "ops/ci_duong_nhanh.py", ".github/workflows/ci.yml", ".claude/dev/ci_dang_ky_test.py"
TEST = "ops/ci_duong_nhanh_test.py"
LP = "ops/lease_publish.py"   # chi dot bien PHAM VI bia mo ma docstring D2 khai (t21b), tren ban sao tam


def _test(cu, moi):
    return (TEST, lambda vb: thay_mot(vb, cu, moi))


def _ma(cu, moi):
    return (MA, lambda vb: thay_mot(vb, cu, moi))


def _lp(cu, moi):
    return (LP, lambda vb: thay_mot(vb, cu, moi))


def _yml(cu, moi):
    return (YML, lambda vb: thay_mot(vb, cu, moi))


_NEO_TREN = "        tren = frozenset({danh_tinh(goc)}) if goc == goc_cay else to_tien.pop(goc)\n"
IF_XOA = "        if: ${{ needs.chuan-bi.outputs.che_do != 'duong_nhanh' }}\n"
TAT_CA_BUOC_GOLDEN = "      - name: golden-test\n" + IF_XOA
DOT_BIEN = [
    # (tên, (tệp, hàm biến đổi), (ca đích phải ĐỎ ...))
    ("noi_allowlist_them_scripts", _ma('"ops/reviews/", "ops/specs/")\nMAU_SHA', '"ops/reviews/", "ops/specs/", "scripts/")\nMAU_SHA'), ("t02_co_tep_ma_day_du",)),
    ("noi_allowlist_them_github", _ma('"ops/reviews/", "ops/specs/")\nMAU_SHA', '"ops/reviews/", "ops/specs/", ".github/")\nMAU_SHA'), ("t08_doi_workflow_hoac_bo_phan_loai_day_du",)),
    ("noi_allowlist_them_ops_tran", _ma('"ops/reviews/", "ops/specs/")\nMAU_SHA', '"ops/reviews/", "ops/specs/", "ops/")\nMAU_SHA'), ("t08_doi_workflow_hoac_bo_phan_loai_day_du",)),
    ("tien_to_khong_dau_gach", _ma('ALLOWLIST_TIEN_TO = ("ops/land/",', 'ALLOWLIST_TIEN_TO = ("ops/land",'), ("t09_ranh_gioi_tien_to",)),
    ("fail_open_khong_do_duoc", _ma("    if doi is None:\n        return DAY_DU,", "    if doi is None:\n        return DUONG_NHANH,"), ("t05_thieu_hoac_hong_sha_day_du",)),
    ("fail_open_rc_khong_kiem", _ma('    if getattr(r, "returncode", None) != 0:\n        return None\n    ra = ',
                                     '    if False:\n        return None\n    ra = '), ("t06_git_loi_hoac_dau_ra_hong_day_du",)),
    ("fail_open_bat_ngoai_le_bi_go", _ma("    except Exception:\n        return None\n    if getattr(r,",
                                          "    except ZeroDivisionError:\n        return None\n    if getattr(r,"), ("t06_git_loi_hoac_dau_ra_hong_day_du",)),
    ("fail_open_dau_ra_cut", _ma('    if ra and not bytes(ra).endswith(b"\\0"):\n        return None\n', ""), ("t06_git_loi_hoac_dau_ra_hong_day_du",)),
    ("fail_open_dau_ra_khong_phai_bytes", _ma("    if not isinstance(ra, (bytes, bytearray)):\n        return None\n", ""), ("t06_git_loi_hoac_dau_ra_hong_day_du",)),
    ("git_cho_push_doc_diff", _ma('    if su_kien != "pull_request":\n        return None\n    if not all(MAU_SHA', "    if not all(MAU_SHA"), ("t03_push_va_dispatch_khong_goi_git",)),
    ("git_cho_push_phan_loai", _ma('    if su_kien != "pull_request":\n        return DAY_DU, f"DUONG_NHANH: khong phan loai', '    if False:\n        return DAY_DU, f"DUONG_NHANH: khong phan loai'), ("t03_push_va_dispatch_khong_goi_git",)),
    ("diff_rong_thanh_day_du", _ma("    if not doi:\n        return DUONG_NHANH,", "    if not doi:\n        return DAY_DU,"), ("t07_diff_rong_duong_nhanh_co_dong_log_rieng",)),
    ("hai_cham_thay_ba_cham", _ma('"-z", f"{goc}...{dau}"]', '"-z", f"{goc}..{dau}"]'), ("t11_ba_cham_khong_tinh_nhanh_dich_da_tien",)),
    ("bo_no_renames", _ma('"--name-only", "--no-renames", "-z"', '"--name-only", "-z"'), ("t12_doi_ten_ra_khoi_vung_ma_day_du",)),
    ("bo_z", _ma('"--no-renames", "-z", f"{goc}...{dau}"]', '"--no-renames", f"{goc}...{dau}"]'), ("t13_ten_tep_co_dau_van_duong_nhanh",)),
    ("bo_kiem_sha_toan_0", _ma("MAU_SHA.fullmatch(x) and x.strip(\"0\")", "MAU_SHA.fullmatch(x)"), ("t05_thieu_hoac_hong_sha_day_du",)),
    ("noi_kiem_sha_khong_du_40", _ma('MAU_SHA = re.compile(r"[0-9a-f]{40}")', 'MAU_SHA = re.compile(r"[0-9a-fA-F]{4,64}")'), ("t05_thieu_hoac_hong_sha_day_du",)),
    ("bo_kiem_len_ngoai_duong_dan", _ma('("", ".", "..")', '("", ".")'), ("t10a_duong_dan_len_ngoai_day_du",)),
    ("bo_kiem_thanh_phan_rong", _ma('("", ".", "..")', '(".", "..")'), ("t10b_thanh_phan_rong_day_du",)),
    ("bo_kiem_thanh_phan_cham", _ma('("", ".", "..")', '("", "..")'), ("t10c_thanh_phan_cham_day_du",)),
    ("bo_kiem_cheo_nguoc", _ma('or "\\\\" in duong:', ":"), ("t10d_dau_cheo_nguoc_day_du",)),
    ("bo_kiem_ky_tu_dieu_khien", _ma("    if any(ord(c) < 32 or ord(c) == 127 for c in duong):\n        return False\n", ""), ("t10e_ky_tu_dieu_khien_day_du",)),
    ("main_ghi_cung_duong_nhanh", _ma('f.write(f"che_do={che_do}\\n")', 'f.write("che_do=duong_nhanh\\n")'), ("t16_main_ghi_output_dung_che_do",)),
    ("main_nuot_loi_thanh_duong_nhanh", _ma('che_do, ly_do = DAY_DU, f"DUONG_NHANH: LOI NOI BO', 'che_do, ly_do = DUONG_NHANH, f"DUONG_NHANH: LOI NOI BO'), ("t17_main_loi_noi_bo_fail_close",)),
    ("main_nuot_loi_ghi_output", _ma('        except OSError as e:\n            print(f"DUONG_NHANH: khong ghi duoc GITHUB_OUTPUT ({type(e).__name__}) - DO", file=sys.stderr)\n            return 1',
                                    '        except OSError:\n            return 0'), ("t18_main_khong_ghi_duoc_output_thi_do",)),
    ("kiem_re_khong_doi_khop", _ma("    if che_do != DUONG_NHANH:\n        print(\"DUONG_NHANH: kiem-re CHI", "    if False:\n        print(\"DUONG_NHANH: kiem-re CHI"), ("t19a_kiem_re_co_tep_ma_thi_do",)),
    ("kiem_re_bo_yaml", _ma("loi = (kiem_yaml(doi, kho) +", "loi = ([] +"), ("t20b_kiem_re_yaml_hong_do",)),
    ("kiem_re_bo_diff_check", _ma("kiem_diff_check(env, chay, kho) + kiem_nhi_phan(", "[] + kiem_nhi_phan("), ("t20c_kiem_re_dau_xung_dot_do",)),
    ("kiem_re_bo_lease", _ma("+ kiem_lease(doi, kho, chay, bay_gio, ra)", "+ []"), ("t20e_kiem_re_lease_con_han_loi_do",)),
    ("diff_check_bo_tinh_chinh_whitespace", _ma('"-c", CAU_HINH_WHITESPACE, "diff", "--check"', '"diff", "--check"'), ("t20d_kiem_re_khoang_trang_cuoi_dong_khong_do",)),
    ("diff_check_bo_check", _ma('"diff", "--check", "--no-renames"', '"diff", "--no-renames"'), ("t20c_kiem_re_dau_xung_dot_do",)),
    ("lease_het_han_coi_nhu_con_han", _ma("        het_han = han is not None and han <= bay_gio\n", "        het_han = False\n"), ("t21_kiem_lease_phan_biet_con_han_het_han_va_duoi_tep",)),
    ("lease_het_han_duoc_mien_kiem", _ma("        if het_han:\n            print(", "        if het_han:\n            continue\n            print("), ("t20f_kiem_re_lease_het_han_sai_schema_van_do",)),
    ("lease_bo_duoi_yml", _ma('x.startswith("ops/leases/") and x.endswith((".yaml", ".yml"))', 'x.startswith("ops/leases/") and x.endswith(".yaml")'), ("t20g_kiem_re_lease_duoi_yml_van_duoc_kiem",)),
    ("kiem_re_bo_ca_du_lieu", _ma("\n           + kiem_ca_du_lieu(kho, chay))", ")"), ("t20a_kiem_re_ho_so_sach_dat",)),
    ("ca_du_lieu_bo_t27", _ma(',\n              "t27_canh_bao_trong_bien_nhan_phai_duoc_NANG_len_muc_luc")', ")"), ("t22_ca_du_lieu_thay_bo_lease_publish_selftest",)),
    ("ca_du_lieu_bo_qua_rc", _ma("    if getattr(r, \"returncode\", None) != 0:\n        cuoi = _dau_ra(r).strip().splitlines()[-3:]", "    if False:\n        cuoi = _dau_ra(r).strip().splitlines()[-3:]"), ("t22_ca_du_lieu_thay_bo_lease_publish_selftest",)),
    ("lease_han_hong_coi_la_het_han", _ma('        except ValueError:\n            return None\n        return han if', '        except ValueError:\n            return datetime(1970, 1, 1, tzinfo=timezone.utc)\n        return han if'), ("t21_kiem_lease_phan_biet_con_han_het_han_va_duoi_tep",)),
    ("lease_check_rc_khong_kiem", _ma('        if getattr(r, "returncode", None) != 0:\n            cuoi', '        if False:\n            cuoi'), ("t21_kiem_lease_phan_biet_con_han_het_han_va_duoi_tep",)),
    # ---- lop fixture-lease-phu-thuoc-actor-ci (luot 2): hai duong vao, moi duong mot chot
    ("test_bo_loc_actor_o_env_git", _test('if not k.startswith("GIT_") and k != "GITHUB_ACTOR"}\n', 'if not k.startswith("GIT_")}\n'), ("t23_fixture_sach_khong_phu_thuoc_actor_ci",)),
    ("test_bo_patch_dict_o_helper_fixture", _test('            with mock.patch.dict(os.environ, {k: v for k, v in os.environ.items() if k != "GITHUB_ACTOR"}, clear=True):\n', '            with contextlib.nullcontext():\n'), ("t23_fixture_sach_khong_phu_thuoc_actor_ci",)),
    # ---- lop chot-yaml-chi-do-su-hien-dien (luot 2): moi dang nuot loi o MOI buoc/job
    ("yml_nuot_loi_selftest_literal", _yml("        if: runner.os == 'Linux'\n        run: python ops/ci_duong_nhanh_test.py\n", "        if: runner.os == 'Linux'\n        continue-on-error: true\n        run: python ops/ci_duong_nhanh_test.py\n"), ("y09_buoc_goi_test_cua_packet_khong_bi_bo",)),
    ("yml_nuot_loi_selftest_bieu_thuc_true", _yml("        if: runner.os == 'Linux'\n        run: python ops/ci_duong_nhanh_test.py\n", "        if: runner.os == 'Linux'\n        continue-on-error: ${{ true }}\n        run: python ops/ci_duong_nhanh_test.py\n"), ("y09_buoc_goi_test_cua_packet_khong_bi_bo",)),
    ("yml_nuot_loi_selftest_bieu_thuc_dieu_kien", _yml("        if: runner.os == 'Linux'\n        run: python ops/ci_duong_nhanh_test.py\n", "        if: runner.os == 'Linux'\n        continue-on-error: ${{ github.event_name == 'pull_request' }}\n        run: python ops/ci_duong_nhanh_test.py\n"), ("y09_buoc_goi_test_cua_packet_khong_bi_bo",)),
    ("yml_nuot_loi_buoc_nang_literal", _yml("      - name: golden-test\n" + IF_XOA, "      - name: golden-test\n" + IF_XOA + "        continue-on-error: true\n"), ("y10_khong_continue_on_error_ngoai_danh_sach_cho_phep",)),
    ("yml_nuot_loi_buoc_nang_chuoi", _yml("      - name: release-check full\n" + IF_XOA, "      - name: release-check full\n" + IF_XOA + "        continue-on-error: 'true'\n"), ("y10_khong_continue_on_error_ngoai_danh_sach_cho_phep",)),
    ("yml_nuot_loi_job_gate_registry", _yml("  gate-registry:\n    # packet #463", "  gate-registry:\n    continue-on-error: true\n    # packet #463"), ("y10_khong_continue_on_error_ngoai_danh_sach_cho_phep",)),
    ("yml_buoc_phan_loai_bieu_thuc", _yml("        id: phan-loai\n        if: ${{ github.event_name == 'pull_request' }}\n        continue-on-error: true\n", "        id: phan-loai\n        if: ${{ github.event_name == 'pull_request' }}\n        continue-on-error: ${{ true }}\n"), ("y10_khong_continue_on_error_ngoai_danh_sach_cho_phep",)),
    ("test_docstring_ghim_so_ca", _test("(đã trôi hai lượt " + "liền): nguồn", "(đã trôi hai lượt " + "liền; hien 43/55 ca): nguồn"), ("t98_docstring_khong_ghim_so_ca_va_khoang_ten",)),
    # ---- cross-review luot 15 (`bang-do-thieu-neo-va-thieu-kiem-ke`): MOI duong vao mot dot bien — tai lieu mat neo / chen so
    # khong neo (D1, D2 la hai dot bien cua HINT), roi go TUNG chot cua bo quet (moi chot do mot mau tu kiem cua ca dich)
    ("docstring_ti_le_D1_mat_neo", _ma("first-parent tính tới 1741e0a (lệnh", "first-parent tính tới HEAD (lệnh"), ("t98b_moi_so_do_trong_docstring_va_chu_thich_phai_co_neo",)),
    ("docstring_ti_le_D2_mat_neo", _ma("không phải của kho: tại " + "3569472cb9 (119", "không phải của kho: tại HEAD (119"), ("t98b_moi_so_do_trong_docstring_va_chu_thich_phai_co_neo",)),
    ("docstring_ham_mat_neo_nhi_phan", _ma("Hồ sơ không cần nhị phân (tại 3569472cb9: 0/1991", "Hồ sơ không cần nhị phân (master: 0/1991"), ("t98b_moi_so_do_trong_docstring_va_chu_thich_phai_co_neo",)),
    ("docstring_ham_mat_neo_thoi_gian", _ma("~7 giay (do tai 3569472cb9,", "~7 giay (do tren may dev,"), ("t98b_moi_so_do_trong_docstring_va_chu_thich_phai_co_neo",)),
    ("chu_thich_san_pham_so_khong_neo", _ma("TOI_DA_TEN_IN = 5\n", "TOI_DA_TEN_IN = 5\n# Kho co 119 tep lease.\n"), ("t98b_moi_so_do_trong_docstring_va_chu_thich_phai_co_neo",)),
    ("docstring_test_mat_neo_kiem_ke", _test("(tai 7b8c856 kiem ke " + "theo tien to", "(tai luot 4 kiem ke " + "theo tien to"), ("t98b_moi_so_do_trong_docstring_va_chu_thich_phai_co_neo",)),
    ("chu_thich_test_so_khong_neo", _test("\nclass SuDoGia(Exception):\n", "\n# Kho co 6/119 lease truot.\nclass SuDoGia(Exception):\n"), ("t98b_moi_so_do_trong_docstring_va_chu_thich_phai_co_neo",)),
    ("bo_quet_so_chi_docstring_module", _test("(ast.Module, ast.ClassDef, " + "ast.FunctionDef, ast.AsyncFunctionDef)", "(ast.Module,)"), ("t98b_moi_so_do_trong_docstring_va_chu_thich_phai_co_neo", "t98c_khang_dinh_ve_nen_ci_phai_mang_nhan_bao_dam")),
    ("bo_quet_so_bo_chu_thich", _test("if tok.type == tokenize." + "COMMENT:", "if False:"), ("t98b_moi_so_do_trong_docstring_va_chu_thich_phai_co_neo", "t98c_khang_dinh_ve_nen_ci_phai_mang_nhan_bao_dam")),
    ("bo_quet_so_khong_tach_cau", _test("for cau in MAU_TACH_CAU." + "split(p)", "for cau in [p]"), ("t98b_moi_so_do_trong_docstring_va_chu_thich_phai_co_neo", "t98c_khang_dinh_ve_nen_ci_phai_mang_nhan_bao_dam")),
    ("bo_quet_so_chi_ti_le", _test("MAU_SO_TRONG_VAN = " + "re.compile(", 'MAU_SO_TRONG_VAN = ' + 're.compile(r"\\d{1,4}/\\d{1,4}") or re.compile('), ("t98b_moi_so_do_trong_docstring_va_chu_thich_phai_co_neo",)),
    ("bo_quet_so_neo_nhan_so_thuan", _test("(?=[0-9a-f]*[a-f])" + "(?=[0-9a-f]*[0-9])", "(?=[0-9a-f]*[0-9])"), ("t98b_moi_so_do_trong_docstring_va_chu_thich_phai_co_neo",)),
    # ---- cross-review luot 16 (`bang-do-thieu-neo-va-thieu-kiem-ke`): moi duong vao/nhanh moi cua bo quet mot dot bien
    ("bo_quet_so_neo_khong_doi_chu_so", _test("(?=[0-9a-f]*[a-f])" + "(?=[0-9a-f]*[0-9])[0-9a-f]{7,40}", "(?=[0-9a-f]*[a-f])[0-9a-f]{7,40}"), ("t98b_moi_so_do_trong_docstring_va_chu_thich_phai_co_neo",)),
    ("bo_quet_so_tach_cau_bo_cham_phay", _test('MAU_TACH_CAU = re.compile(r"(?<=[.' + ';!?])', 'MAU_TACH_CAU = re.compile(r"(?<=[.!?])'), ("t98b_moi_so_do_trong_docstring_va_chu_thich_phai_co_neo",)),
    ("bo_quet_so_tach_doan_bo_gach", _test('|\\n[ \\t]*(?=' + '·\\s)")', '")'), ("t98b_moi_so_do_trong_docstring_va_chu_thich_phai_co_neo",)),
    ("bo_quet_so_bo_so_chu", _test("    so += [k.group() for k in MAU_SO_CHU_KHO" + ".finditer(cau)]\n", ""), ("t98b_moi_so_do_trong_docstring_va_chu_thich_phai_co_neo",)),
    ("bo_quet_so_chu_bo_mien_ca", _test("(?i)(?<!\\bca )" + "(?<!\\bcả )", "(?i)"), ("t98b_moi_so_do_trong_docstring_va_chu_thich_phai_co_neo",)),
    ("bo_quet_thong_diep_bang", _test("cau_tai_lieu(nguon) + " + "cau_thong_bao(nguon)", "cau_tai_lieu(nguon)"), ("t98b_moi_so_do_trong_docstring_va_chu_thich_phai_co_neo",)),
    ("docstring_test_so_chu_khong_neo", _test("    `.gitattributes` — PR ho so co them tep " + "nhu the duoi `ops/reviews/`", "    `.gitattributes` — master co ba tep nhu the; PR ho so co them tep nhu the duoi `ops/reviews/`"), ("t98b_moi_so_do_trong_docstring_va_chu_thich_phai_co_neo",)),
    ("thong_diep_bang_mat_neo", _test("khong duoc chan oan (lop PR " + "ma D1", "khong duoc chan oan (do 8/63 lan merge; lop PR ma D1"), ("t98b_moi_so_do_trong_docstring_va_chu_thich_phai_co_neo",)),
    ("bo_quet_so_bo_tep_test", _test('CAY / "ops" / "ci_duong_nhanh.py", CAY / "ops" / ' + '"ci_duong_nhanh_test.py")', 'CAY / "ops" / "ci_duong_nhanh.py",)'), ("t98b_moi_so_do_trong_docstring_va_chu_thich_phai_co_neo",)),
    # ---- luot 17 (executor, lop `bang-do-thieu-neo-va-thieu-kiem-ke`): duong vao A1 (dem/luong tu ve kho phai co neo de do lai)
    # va moi nhanh con lai cua bo quet thong bao (`do`/`đo`, chuoi thuong/f-string); nhanh tu-so/danh tu sinh o duoi `_lat_o`
    ("docstring_D1_gitattributes_dem_khong_neo", _ma("KHÔNG chặn `.gitattributes`: PR " + "hồ sơ có thêm", "KHÔNG chặn `.gitattributes`: master có 3 tệp như thế, do chính PR hồ sơ thêm vào. PR hồ sơ có thêm"), ("t98b_moi_so_do_trong_docstring_va_chu_thich_phai_co_neo",)),
    ("bo_quet_thong_bao_bo_dau_do_co_dau", _test("(?:do|" + "đo) (", "(?:do) ("), ("t98b_moi_so_do_trong_docstring_va_chu_thich_phai_co_neo",)),
    ("bo_quet_thong_bao_bo_dau_do_khong_dau", _test("(?:do" + "|đo) (", "(?:đo) ("), ("t98b_moi_so_do_trong_docstring_va_chu_thich_phai_co_neo",)),
    ("bo_quet_thong_bao_bo_chuoi_thuong", _test("phan = [a] if isinstance(a, " + "ast.Constant) else", "phan = [] if isinstance(a, ast.Constant) else"), ("t98b_moi_so_do_trong_docstring_va_chu_thich_phai_co_neo",)),
    ("bo_quet_thong_bao_bo_f_string", _test("list(a.values) if isinstance(a, " + "ast.JoinedStr) else []", "[] if isinstance(a, ast.JoinedStr) else []"), ("t98b_moi_so_do_trong_docstring_va_chu_thich_phai_co_neo",)),
    # ---- cross-review luot 16, lop `khang-dinh-dinh-tinh-rong-hon-phep-do`: (i) cau nhac nen CI khong nhan — moi nhanh mot dot bien
    ("docstring_D2_checkout_khang_dinh_tran", _ma("Trên CI, job `gate-ops` checkout " + "TOÀN BỘ lịch sử", "Checkout của Actions chỉ có ref của PR, không có các nhánh `ops/**`. Trên CI, job `gate-ops` checkout TOÀN BỘ lịch sử"), ("t98c_khang_dinh_ve_nen_ci_phai_mang_nhan_bao_dam",)),
    ("bo_quet_nen_bo_github", _test('r"\\bGitHub\\b|' + '\\bActions\\b|', 'r"\\bActions\\b|'), ("t98c_khang_dinh_ve_nen_ci_phai_mang_nhan_bao_dam",)),
    ("bo_quet_nen_bo_actions", _test('|\\bActions' + '\\b|actions/checkout|', '|actions/checkout|'), ("t98c_khang_dinh_ve_nen_ci_phai_mang_nhan_bao_dam",)),
    ("bo_quet_nen_bo_checkout", _test('|actions/checkout' + '|\\b[Rr]uleset', '|\\b[Rr]uleset'), ("t98c_khang_dinh_ve_nen_ci_phai_mang_nhan_bao_dam",)),
    ("bo_quet_nen_bo_ruleset", _test('actions/checkout|' + '\\b[Rr]uleset\\b")', 'actions/checkout")'), ("t98c_khang_dinh_ve_nen_ci_phai_mang_nhan_bao_dam",)),
    ("bo_quet_nen_nhan_o_cau_khac", _test("if not (MAU_NHAN_BAO_DAM.search(" + "cau) or", "if not (MAU_NHAN_BAO_DAM.search(nguon) or"), ("t98c_khang_dinh_ve_nen_ci_phai_mang_nhan_bao_dam",)),
    ("bo_quet_nen_bo_tep_test", _test('for tep in (CAY / "ops" / "ci_duong_nhanh_test.py", ' + 'CAY / "ops" / "ci_duong_nhanh.py"):', 'for tep in (CAY / "ops" / "ci_duong_nhanh.py",):'), ("t98c_khang_dinh_ve_nen_ci_phai_mang_nhan_bao_dam",)),
    # (ii) pham vi quet khai rong hon ma: bia mo D2 — docstring noi rong ra, hoac `lease_publish` doi pham vi (ban sao tam)
    ("docstring_D2_pham_vi_ref_rong", _ma("trên mọi ref dưới `refs/heads` " + "và `refs/remotes`", "trên mọi REF cục bộ"), ("t21b_bia_mo_D2_doc_dung_pham_vi_ref_ma_docstring_khai",)),
    ("lease_publish_quet_ca_tag", _lp('"refs/heads", ' + '"refs/remotes")', '"refs/heads", "refs/remotes", "refs/tags")'), ("t21b_bia_mo_D2_doc_dung_pham_vi_ref_ma_docstring_khai",)),
    ("lease_publish_bo_refs_remotes", _lp('"refs/heads", ' + '"refs/remotes")', '"refs/heads")'), ("t21b_bia_mo_D2_doc_dung_pham_vi_ref_ma_docstring_khai",)),
    ("lease_publish_doc_ca_cay_lam_viec", _lp("cac_lease = _quet_lease_toan_kho(" + "root, doi_chieu_ref=False)", "cac_lease = _quet_lease_toan_kho(root, doi_chieu_ref=False) + [{\"lease\": __import__(\"yaml\").safe_load(x.read_text(encoding=\"utf-8\"))} for x in (root / \"ops\" / \"leases\").glob(\"*.yaml\")]"), ("t21b_bia_mo_D2_doc_dung_pham_vi_ref_ma_docstring_khai",)),
    # ---- lop dac-ta-bo-mat-kiem-du-lieu-ho-so (luot 2): thao tac GOI ca that
    ("ca_du_lieu_khong_goi_ham", _ma("m[ten]()", "m[ten]"), ("t22b_ca_du_lieu_phai_thuc_thi_tung_ca",)),
    ("ca_du_lieu_bo_t23", _ma('CA_DU_LIEU = ("t23_MOI_lease_THAT_trong_kho_phai_QUA", ', "CA_DU_LIEU = ("), ("t22b_ca_du_lieu_phai_thuc_thi_tung_ca",)),
    ("ca_du_lieu_bo_t26", _ma('"t26_moi_bien_nhan_review_phai_khop_BAM_tep_no_tro_toi",\n              ', ""), ("t22b_ca_du_lieu_phai_thuc_thi_tung_ca",)),
    ("ca_du_lieu_cwd_sai", _ma('"ops/lease_publish_test.py", *CA_DU_LIEU],\n                 cwd=kho,', '"ops/lease_publish_test.py", *CA_DU_LIEU],\n                 cwd=ROOT,'), ("t22b_ca_du_lieu_phai_thuc_thi_tung_ca",)),
    ("ca_du_lieu_nuot_ngoai_le_trong_con", _ma("m[ten]()", r"try:\n        m[ten]()\n    except AssertionError:\n        pass"), ("t22b_ca_du_lieu_phai_thuc_thi_tung_ca",)),
    # ---- lop chot-yaml-chi-do-su-hien-dien (luot 3): job tien nhiem va moi job
    ("yml_chuan_bi_if_false_literal", _yml("    timeout-minutes: 20\n    outputs:\n      os:", "    if: false\n    timeout-minutes: 20\n    outputs:\n      os:"), ("y06_job_bat_buoc_khong_bi_bo_ca_job",)),
    ("yml_chuan_bi_if_false_bieu_thuc", _yml("    timeout-minutes: 20\n    outputs:\n      os:", "    if: ${{ false }}\n    timeout-minutes: 20\n    outputs:\n      os:"), ("y06_job_bat_buoc_khong_bi_bo_ca_job",)),
    ("yml_chuan_bi_if_dieu_kien_su_kien", _yml("    timeout-minutes: 20\n    outputs:\n      os:", "    if: ${{ github.event_name == 'push' }}\n    timeout-minutes: 20\n    outputs:\n      os:"), ("y06_job_bat_buoc_khong_bi_bo_ca_job",)),
    ("yml_chuan_bi_nuot_loi_cap_job", _yml("    timeout-minutes: 20\n    outputs:\n      os:", "    continue-on-error: true\n    timeout-minutes: 20\n    outputs:\n      os:"), ("y06_job_bat_buoc_khong_bi_bo_ca_job",)),
    ("yml_gate_registry_if_false", _yml("  gate-registry:\n    # packet #463", "  gate-registry:\n    if: false\n    # packet #463"), ("y11_khong_job_nao_co_if_cap_job_ngoai_danh_sach_cho_phep",)),
    # ---- g4, tich hop #668: y11 so DUNG bieu thuc theo job (khong chi membership); khoa job moi o y12/y13
    ("yml_gop_if_doi_always", _yml("    needs: [chuan-bi, gate-cong-cu]\n    if: ${{ !cancelled() && contains(fromJson(needs.chuan-bi.outputs.os), 'ubuntu-latest') }}\n", "    needs: [chuan-bi, gate-cong-cu]\n    if: ${{ always() }}\n"), ("y11_khong_job_nao_co_if_cap_job_ngoai_danh_sach_cho_phep",)),
    ("yml_gop_bo_if", _yml("    needs: [chuan-bi, gate-cong-cu]\n    if: ${{ !cancelled() && contains(fromJson(needs.chuan-bi.outputs.os), 'ubuntu-latest') }}\n", "    needs: [chuan-bi, gate-cong-cu]\n"), ("y11_khong_job_nao_co_if_cap_job_ngoai_danh_sach_cho_phep",)),
    # wp879: bo dieu kien ubuntu khoi `if` cua gom ⇒ luot windows-only gom DO oan vi thieu manh.
    ("yml_gop_if_bo_ubuntu", _yml("    needs: [chuan-bi, gate-cong-cu]\n    if: ${{ !cancelled() && contains(fromJson(needs.chuan-bi.outputs.os), 'ubuntu-latest') }}\n", "    needs: [chuan-bi, gate-cong-cu]\n    if: ${{ !cancelled() }}\n"), ("y11_khong_job_nao_co_if_cap_job_ngoai_danh_sach_cho_phep",)),
    ("yml_them_if_cung_bieu_thuc_vao_job_manh", _yml("  gate-cong-cu:\n    needs: chuan-bi\n    if: ${{ needs.chuan-bi.outputs.che_do != 'duong_nhanh' }}\n", "  gate-cong-cu:\n    needs: chuan-bi\n    if: ${{ !cancelled() }}\n"), ("y11_khong_job_nao_co_if_cap_job_ngoai_danh_sach_cho_phep",)),
    # wp892: bo `if:` duong nhanh cua job manh ⇒ PR ho so van dot du cac manh.
    # wp892 r2: nhung dang nam NGOAI hai ngoai le cua y04 — moi cai phai DO dung y04.
    ("y04_if_che_do_vao_job_gate", _yml("  gate:\n    needs: chuan-bi\n", "  gate:\n    needs: chuan-bi\n    if: ${{ needs.chuan-bi.outputs.che_do != 'duong_nhanh' }}\n"), ("y04_tap_buoc_mang_if_che_do_khop_dung",)),
    ("y04_if_che_do_vao_job_gom", _yml("    needs: [chuan-bi, gate-cong-cu]\n    if: ${{ !cancelled() && contains(fromJson(needs.chuan-bi.outputs.os), 'ubuntu-latest') }}\n", "    needs: [chuan-bi, gate-cong-cu]\n    if: ${{ !cancelled() && needs.chuan-bi.outputs.che_do != 'duong_nhanh' }}\n"), ("y04_tap_buoc_mang_if_che_do_khop_dung",)),
    ("y04_if_manh_doi_dang", _yml("  gate-cong-cu:\n    needs: chuan-bi\n    if: ${{ needs.chuan-bi.outputs.che_do != 'duong_nhanh' }}\n", "  gate-cong-cu:\n    needs: chuan-bi\n    if: ${{ needs.chuan-bi.outputs.che_do == 'day_du' }}\n"), ("y04_tap_buoc_mang_if_che_do_khop_dung",)),
    ("y04_env_ten_khac", _yml("        env:\n          CONG_CU_TEST_GOP_CHE_DO: ${{ needs.chuan-bi.outputs.che_do }}\n", "        env:\n          CONG_CU_TEST_CHE_DO: ${{ needs.chuan-bi.outputs.che_do }}\n"), ("y04_tap_buoc_mang_if_che_do_khop_dung",)),
    ("y04_env_them_khoa", _yml("        env:\n          CONG_CU_TEST_GOP_CHE_DO: ${{ needs.chuan-bi.outputs.che_do }}\n", "        env:\n          CONG_CU_TEST_GOP_CHE_DO: ${{ needs.chuan-bi.outputs.che_do }}\n          PHU: ${{ needs.chuan-bi.outputs.che_do }}\n"), ("y04_tap_buoc_mang_if_che_do_khop_dung",)),
    ("y04_env_vao_buoc_khac", _yml("      - name: G5 manh ban kinh dot bien (#668)\n        shell: bash\n", "      - name: G5 manh ban kinh dot bien (#668)\n        shell: bash\n        env:\n          CONG_CU_TEST_GOP_CHE_DO: ${{ needs.chuan-bi.outputs.che_do }}\n"), ("y04_tap_buoc_mang_if_che_do_khop_dung",)),
    ("yml_manh_bo_if_duong_nhanh", _yml("  gate-cong-cu:\n    needs: chuan-bi\n    if: ${{ needs.chuan-bi.outputs.che_do != 'duong_nhanh' }}\n", "  gate-cong-cu:\n    needs: chuan-bi\n"), ("y11_khong_job_nao_co_if_cap_job_ngoai_danh_sach_cho_phep",)),
    ("yml_them_if_false_vao_buoc_gom", _yml("      - name: G5 gom manh ban kinh dot bien (#668)\n", "      - name: G5 gom manh ban kinh dot bien (#668)\n        if: false\n"), ("y12_moi_if_cap_buoc_khop_dung_danh_sach_cho_phep",)),
    ("yml_bot_manh_g5", _yml("  gate-cong-cu:\n    needs: chuan-bi\n    if: ${{ needs.chuan-bi.outputs.che_do != 'duong_nhanh' }}\n    strategy:\n      fail-fast: false\n      matrix:\n        os: ${{ fromJson(needs.chuan-bi.outputs.os) }}\n        manh: [0, 1, 2, 3, 4, 5, 6, 7]\n", "  gate-cong-cu:\n    needs: chuan-bi\n    if: ${{ needs.chuan-bi.outputs.che_do != 'duong_nhanh' }}\n    strategy:\n      fail-fast: false\n      matrix:\n        os: ${{ fromJson(needs.chuan-bi.outputs.os) }}\n        manh: [0, 1, 2, 3]\n"), ("y13_khoa_topology_cua_ci_yml_ngoai_than_run",)),
    ("yml_g5_gate_bo_env_ban_kinh", _yml("        env:\n          CONG_CU_TEST_BAN_KINH: manh\n", ""), ("y13_khoa_topology_cua_ci_yml_ngoai_than_run",)),
    # ---- lop tin-dung-dot-bien-khong-co-ca-dich (luot 3): moi cua mot chot
    ("test_go_kiem_rong_o_callee", _test('    if not dich:\n        return "HONG", "tap ca dich rong: khong co bang chung duong thi khong duoc cap GIET"\n', ""), ("t97_harness_khong_cap_giet_khi_khong_co_bang_chung_duong",)),
    ("test_go_vat_hoa_o_callee", _test("    dich = tuple(dich)   # vat hoa " + "TRUOC lan doc dau", "    dich = dich   # vat hoa " + "TRUOC lan doc dau"), ("t97_harness_khong_cap_giet_khi_khong_co_bang_chung_duong",)),
    ("test_go_vat_hoa_o_caller", _test("    for ten, tv, dich in tap:\n        dich = tuple(dich)\n", "    for ten, tv, dich in tap:\n"), ("t97_harness_khong_cap_giet_khi_khong_co_bang_chung_duong",)),
    # ---- y12: moi `if:` cap buoc; kiem chung ban goc
    ("yml_them_if_false_vao_buoc_giu", _yml("      - name: py_compile\n", "      - name: py_compile\n        if: false\n"), ("y12_moi_if_cap_buoc_khop_dung_danh_sach_cho_phep",)),
    ("yml_doi_if_co_san_thanh_always", _yml("        if: runner.os != 'Windows'\n        run: python .github/checks/ci_phamvi_test.py\n", "        if: always()\n        run: python .github/checks/ci_phamvi_test.py\n"), ("y12_moi_if_cap_buoc_khop_dung_danh_sach_cho_phep",)),
    ("yml_bo_if_co_san", _yml("        if: runner.os != 'Windows'\n        run: python .github/checks/ci_phamvi_test.py\n", "        run: python .github/checks/ci_phamvi_test.py\n"), ("y12_moi_if_cap_buoc_khop_dung_danh_sach_cho_phep",)),
    ("yml_them_if_false_vao_buoc_gate_registry", _yml("      - name: test registry (phạm vi + các bộ chưa được nối)\n", "      - name: test registry (phạm vi + các bộ chưa được nối)\n        if: false\n"), ("y12_moi_if_cap_buoc_khop_dung_danh_sach_cho_phep",)),
    ("test_go_kiem_chung_ban_goc", _test('            if rc != 0:\n                return "HONG", f"ca dich {ten_ca} khong xanh tren ban goc', '            if False:\n                return "HONG", f"ca dich {ten_ca} khong xanh tren ban goc'), ("t97_harness_khong_cap_giet_khi_khong_co_bang_chung_duong",)),
    # ---- y13: topology/dinh tuyen — moi khoa khac ngoai than run
    ("yml_gate_ops_runs_on_windows", (YML, lambda vb: thay_regex(vb, r"(\n  gate-ops:\n.*?\n    runs-on: )\$\{\{ matrix\.os \}\}", r"\1windows-latest")), ("y13_khoa_topology_cua_ci_yml_ngoai_than_run",)),
    ("yml_gate_ops_matrix_chi_windows", (YML, lambda vb: thay_regex(vb, r"(\n  gate-ops:\n.*?\n        os: )\$\{\{ fromJson\(needs\.chuan-bi\.outputs\.os\) \}\}", r"\1[windows-latest]")), ("y13_khoa_topology_cua_ci_yml_ngoai_than_run",)),
    ("yml_packet_loop_matrix_exclude_linux", (YML, lambda vb: thay_regex(vb, r"(\n  gate-packet-loop:\n.*?\n        os: \$\{\{ fromJson\(needs\.chuan-bi\.outputs\.os\) \}\}\n)", r"\1        exclude:\n          - os: ubuntu-latest\n")), ("y13_khoa_topology_cua_ci_yml_ngoai_than_run",)),
    ("yml_gate_needs_doi_dang", (YML, lambda vb: thay_regex(vb, r"(\n  gate:\n)    needs: chuan-bi\n", r"\1    needs: [chuan-bi]\n")), ("y13_khoa_topology_cua_ci_yml_ngoai_than_run",)),
    ("yml_gate_timeout_1_phut", (YML, lambda vb: thay_regex(vb, r"(\n  gate:\n.*?\n    timeout-minutes: )60\n", r"\g<1>1\n")), ("y13_khoa_topology_cua_ci_yml_ngoai_than_run",)),
    ("yml_gate_ops_env_doi", (YML, lambda vb: thay_regex(vb, r"(\n  gate-ops:\n.*?\n      PYTHONDONTWRITEBYTECODE: )\"1\"\n", r'\g<1>"0"\n')), ("y13_khoa_topology_cua_ci_yml_ngoai_than_run",)),
    ("yml_buoc_giu_them_working_directory", _yml("      - name: py_compile\n", "      - name: py_compile\n        working-directory: /tmp\n"), ("y13_khoa_topology_cua_ci_yml_ngoai_than_run",)),
    ("yml_buoc_giu_doi_shell_pwsh", _yml("      - name: py_compile\n", "      - name: py_compile\n        shell: pwsh\n"), ("y13_khoa_topology_cua_ci_yml_ngoai_than_run",)),
    ("yml_buoc_nang_them_timeout_1", _yml("      - name: golden-test\n" + IF_XOA, "      - name: golden-test\n" + IF_XOA + "        timeout-minutes: 1\n"), ("y13_khoa_topology_cua_ci_yml_ngoai_than_run",)),
    ("yml_gate_checkout_nong", (YML, lambda vb: thay_regex(vb, r"(\n  gate:\n.*?\n          fetch-depth: )0\n", r"\g<1>1\n")), ("y13_khoa_topology_cua_ci_yml_ngoai_than_run",)),
    ("yml_go_buoc_giu_py_compile", (YML, lambda vb: thay_regex(vb, r"      - name: py_compile\n        run: [^\n]*\n", "")), ("y13_khoa_topology_cua_ci_yml_ngoai_than_run",)),
    ("yml_concurrency_luon_huy", _yml("  cancel-in-progress: ${{ github.ref != 'refs/heads/master' }}\n", "  cancel-in-progress: true\n"), ("y13_khoa_topology_cua_ci_yml_ngoai_than_run",)),
    ("yml_them_permissions_cap_workflow", _yml("\njobs:\n  chuan-bi:", "\npermissions: {}\njobs:\n  chuan-bi:"), ("y13_khoa_topology_cua_ci_yml_ngoai_than_run",)),
    ("yml_doi_thu_tu_job", (YML, lambda vb: thay_regex(vb, r"(\n  gate-packet-loop:\n.*)$", "") + "\n  zz-job-them:\n    runs-on: ubuntu-latest\n    steps:\n      - run: 'true'\n"), ("y13_khoa_topology_cua_ci_yml_ngoai_than_run",)),
    # ---- t96: phan hoach ca cho bang kiem ke
    ("test_phan_hoach_bo_qua_khai_tu_kiem", _test("        if ten in TU_KIEM_KHAI:\n", "        if False:\n"), ("t96_phan_hoach_ca_khong_giao_nhau_va_phu_kin",)),
    ("test_t96_khong_khai_tu_kiem", _test("@ca_tu_kiem\ndef t96_", "@ca\ndef t96_"), ("t96_phan_hoach_ca_khong_giao_nhau_va_phu_kin",)),
    ("test_khai_nham_hanh_vi_la_tu_kiem", _test("@ca\ndef t01_", "@ca_tu_kiem\ndef t01_"), ("t96_phan_hoach_ca_khong_giao_nhau_va_phu_kin",)),
    ("test_dong_kiem_ke_lech_so", _test('" + ".join(f"{k}={len(v)' + '}" for k, v in nhom.items())', '" + ".join(f"{k}={len(v) + (k == \'tu_kiem\')}" for k, v in nhom.items())'), ("t96_phan_hoach_ca_khong_giao_nhau_va_phu_kin",)),
    ("test_dong_kiem_ke_bo_dot_bien_mot_tep", _test("        theo_tep[tep] = theo_tep.get(tep, 0) + 1\n", "        theo_tep[tep] = theo_tep.get(tep, 0) + (tep != TEST)\n"), ("t96_phan_hoach_ca_khong_giao_nhau_va_phu_kin",)),
    ("test_phan_hoach_nhanh_else_tra_lai_nhom_cu", _test('        elif ten[0] == "y":\n            nhom["cau_truc_yaml"].append(ten)\n', '        elif ten[0] == "y":\n            nhom["hanh_vi"].append(ten)\n'), ("t96_phan_hoach_ca_khong_giao_nhau_va_phu_kin",)),
    # ---- tầng YAML (đặc tả nghiệm thu 6 và nghiệm thu 7)
    ("yml_go_dieu_kien_pull_request_khoi_buoc_phan_loai", _yml("        id: phan-loai\n        if: ${{ github.event_name == 'pull_request' }}\n", "        id: phan-loai\n"), ("y01_chuan_bi_phan_loai_chi_pull_request_va_khong_lam_do_job",)),
    ("yml_go_continue_on_error_buoc_phan_loai", _yml("        id: phan-loai\n        if: ${{ github.event_name == 'pull_request' }}\n        continue-on-error: true\n", "        id: phan-loai\n        if: ${{ github.event_name == 'pull_request' }}\n"), ("y01_chuan_bi_phan_loai_chi_pull_request_va_khong_lam_do_job",)),
    ("yml_output_che_do_fail_open", _yml("steps.phan-loai.outputs.che_do || 'day_du' }}", "steps.phan-loai.outputs.che_do || 'duong_nhanh' }}"), ("y02_output_che_do_fail_close",)),
    ("yml_buoc_nang_luon_bo", _yml(TAT_CA_BUOC_GOLDEN, "      - name: golden-test\n        if: false\n"), ("y03_buoc_nang_mang_if_bo_theo_che_do",)),
    ("yml_buoc_nang_dao_dau_so_sanh", _yml("      - name: release-check full\n" + IF_XOA, "      - name: release-check full\n        if: ${{ needs.chuan-bi.outputs.che_do == 'duong_nhanh' }}\n"), ("y03_buoc_nang_mang_if_bo_theo_che_do",)),
    ("yml_go_if_buoc_nang", _yml("      - name: determinism-audit strict\n" + IF_XOA, "      - name: determinism-audit strict\n"), ("y03_buoc_nang_mang_if_bo_theo_che_do",)),
    ("yml_buoc_nang_doi_sang_day_du", _yml("      - name: release-check full\n" + IF_XOA, "      - name: release-check full\n        if: ${{ needs.chuan-bi.outputs.che_do != 'day_du' }}\n"), ("y03_buoc_nang_mang_if_bo_theo_che_do",)),
    ("yml_buoc_cgroup_mat_dieu_kien_nen", _yml("        if: ${{ runner.os == 'Linux' && needs.chuan-bi.outputs.che_do != 'duong_nhanh' }}\n", "        if: ${{ needs.chuan-bi.outputs.che_do != 'duong_nhanh' }}\n"), ("y03_buoc_nang_mang_if_bo_theo_che_do",)),
    ("yml_buoc_packet_loop_luon_bo", _yml("      - name: packet-loop selftest\n" + IF_XOA, "      - name: packet-loop selftest\n        if: false\n"), ("y03_buoc_nang_mang_if_bo_theo_che_do",)),
    ("yml_them_if_che_do_vao_g5", (YML, lambda vb: thay_mot(vb, "      - name: G5 kiem ban ke cong cu + T1..T8 (packet #290)\n", "      - name: G5 kiem ban ke cong cu + T1..T8 (packet #290)\n" + IF_XOA)), ("y04_tap_buoc_mang_if_che_do_khop_dung",)),
    ("yml_them_paths_ignore_pull_request", _yml("  pull_request:\n  # r226", "  pull_request:\n    paths-ignore: ['ops/**']\n  # r226"), ("y05_khong_paths_khong_paths_ignore",)),
    ("yml_them_paths_push", _yml("  push:\n    branches: [master]\n", "  push:\n    branches: [master]\n    paths: ['scripts/**']\n"), ("y05_khong_paths_khong_paths_ignore",)),
    ("yml_if_cap_job_gate_ops", (YML, lambda vb: thay_regex(vb, r"(\n  gate-ops:\n(?:    #[^\n]*\n)+)(    needs: chuan-bi\n)", r"\1    if: ${{ needs.chuan-bi.outputs.che_do != 'duong_nhanh' }}\n\2")), ("y06_job_bat_buoc_khong_bi_bo_ca_job",)),
    ("yml_go_buoc_liet_ke_packet_loop", _yml("      - name: DUONG_NHANH - liet ke buoc bo qua (job gate-packet-loop)\n        if: ${{ needs.chuan-bi.outputs.che_do == 'duong_nhanh' }}\n        run: |\n          echo \"DUONG_NHANH: bo qua packet-loop selftest " + DUOI_LOG + "\"\n", ""), ("y07_buoc_bi_bo_tu_noi_ly_do",)),
    ("yml_liet_ke_thieu_mot_buoc", _yml("          echo \"DUONG_NHANH: bo qua golden-test " + DUOI_LOG + "\"\n", ""), ("y07_buoc_bi_bo_tu_noi_ly_do",)),
    ("yml_kiem_re_nuot_loi", _yml("        shell: bash\n        env:\n          CI_DUONG_NHANH_SU_KIEN: ${{ github.event_name }}\n", "        continue-on-error: true\n        shell: bash\n        env:\n          CI_DUONG_NHANH_SU_KIEN: ${{ github.event_name }}\n"), ("y08_buoc_kiem_re_o_gate_ops",)),
    ("yml_phan_loai_bo_bien_merge", _yml("          CI_DUONG_NHANH_MERGE: ${{ github.sha }}\n        run: python3 ops/ci_duong_nhanh.py\n", "        run: python3 ops/ci_duong_nhanh.py\n"), ("y01_chuan_bi_phan_loai_chi_pull_request_va_khong_lam_do_job", "y13_khoa_topology_cua_ci_yml_ngoai_than_run")),
    ("yml_phan_loai_merge_la_head", _yml("          CI_DUONG_NHANH_MERGE: ${{ github.sha }}\n        run: python3 ops/ci_duong_nhanh.py\n", "          CI_DUONG_NHANH_MERGE: ${{ github.event.pull_request.head.sha }}\n        run: python3 ops/ci_duong_nhanh.py\n"), ("y01_chuan_bi_phan_loai_chi_pull_request_va_khong_lam_do_job", "y13_khoa_topology_cua_ci_yml_ngoai_than_run")),
    ("yml_kiem_re_bo_bien_merge", _yml("          CI_DUONG_NHANH_MERGE: ${{ github.sha }}\n        run: |\n          set -euo pipefail\n", "        run: |\n          set -euo pipefail\n"), ("y08_buoc_kiem_re_o_gate_ops", "y13_khoa_topology_cua_ci_yml_ngoai_than_run")),
    ("yml_kiem_re_shell_pwsh", _yml("        shell: bash\n        env:\n          CI_DUONG_NHANH_SU_KIEN: ${{ github.event_name }}\n", "        shell: pwsh\n        env:\n          CI_DUONG_NHANH_SU_KIEN: ${{ github.event_name }}\n"), ("y08_buoc_kiem_re_o_gate_ops",)),
    ("yml_kiem_re_comment_doctrine", _yml("          python .claude/dev/packet_loop.py doctrine-scan --root .\n", "          # python .claude/dev/packet_loop.py doctrine-scan --root .\n"), ("y08_buoc_kiem_re_o_gate_ops",)),
    ("yml_kiem_re_comment_kiem_re", _yml("          python ops/ci_duong_nhanh.py kiem-re\n", "          # python ops/ci_duong_nhanh.py kiem-re\n"), ("y08_buoc_kiem_re_o_gate_ops",)),
    ("yml_gate_nuot_loi", _yml("  gate:\n    needs: chuan-bi\n", "  gate:\n    needs: chuan-bi\n    continue-on-error: true\n"), ("y06_job_bat_buoc_khong_bi_bo_ca_job",)),
    ("yml_gate_ops_nuot_loi", (YML, lambda vb: thay_regex(vb, r"(\n  gate-ops:\n(?:    #[^\n]*\n)+)(    needs: chuan-bi\n)", r"\1\2    continue-on-error: true\n")), ("y06_job_bat_buoc_khong_bi_bo_ca_job",)),
    ("yml_gate_packet_loop_nuot_loi", (YML, lambda vb: thay_regex(vb, r"(\n  gate-packet-loop:\n(?:    #[^\n]*\n)+)(    needs: chuan-bi\n)", r"\1\2    continue-on-error: true\n")), ("y06_job_bat_buoc_khong_bi_bo_ca_job",)),
    ("yml_go_buoc_kiem_re", (YML, lambda vb: thay_regex(vb, r"      - name: DUONG_NHANH - kiem re thay cho buoc bi bo.*?(?=      # Phản chứng của bộ phân loại)", ""),), ("y08_buoc_kiem_re_o_gate_ops",)),
    ("yml_buoc_kiem_re_luon_chay", _yml("      - name: DUONG_NHANH - kiem re thay cho buoc bi bo (doctrine-scan, YAML, diff --check, lease check)\n        if: ${{ needs.chuan-bi.outputs.che_do == 'duong_nhanh' }}\n", "      - name: DUONG_NHANH - kiem re thay cho buoc bi bo (doctrine-scan, YAML, diff --check, lease check)\n"), ("y08_buoc_kiem_re_o_gate_ops",)),
    ("yml_buoc_test_bi_bo_theo_che_do", _yml("        if: runner.os == 'Linux'\n        run: python ops/ci_duong_nhanh_test.py\n", "        if: ${{ needs.chuan-bi.outputs.che_do != 'duong_nhanh' }}\n        run: python ops/ci_duong_nhanh_test.py\n"), ("y09_buoc_goi_test_cua_packet_khong_bi_bo",)),
    # ---- luot 5, lop chot-yaml: than `run:` cua buoc packet, loader nghiem, cay duoi do
    ("yml_goi_test_exit0_truoc", _yml("        run: python ops/ci_duong_nhanh_test.py\n", "        run: |\n          exit 0\n          python ops/ci_duong_nhanh_test.py\n"), ("y14_than_run_cua_buoc_packet_them_khop_nguyen_van",)),
    ("yml_che_do_exit1", _yml('pull_request, luon DAY_DU"\n', 'pull_request, luon DAY_DU"\n          exit 1\n'), ("y14_than_run_cua_buoc_packet_them_khop_nguyen_van",)),
    ("yml_phan_loai_nuot_loi_trong_run", _yml("        run: python3 ops/ci_duong_nhanh.py\n", "        run: python3 ops/ci_duong_nhanh.py || true\n"), ("y14_than_run_cua_buoc_packet_them_khop_nguyen_van", "y01_chuan_bi_phan_loai_chi_pull_request_va_khong_lam_do_job")),
    ("yml_them_buoc_duong_nhanh_ngoai_bang", _yml("      - name: packet-loop selftest\n", "      - name: DUONG_NHANH - buoc moi ngoai bang\n        run: echo x\n      - name: packet-loop selftest\n"), ("y14_than_run_cua_buoc_packet_them_khop_nguyen_van",)),
    ("test_loader_bo_kiem_khoa_trung", _test("            if khoa in thay:\n", "            if False:\n"), ("y15_loader_nghiem_tu_choi_khoa_trung_va_khoa_gop",)),
    ("test_loader_bo_kiem_khoa_gop", _test('            if k.tag == "tag:yaml.org,2002:merge" or getattr(k, "value", None) == "<<":\n', "            if False:\n"), ("y15_loader_nghiem_tu_choi_khoa_trung_va_khoa_gop",)),
    ("test_doc_wf_dung_safe_load", _test("        return yaml.load(van_ban, Loader=_LoaderNghiem)\n", "        return yaml.safe_load(van_ban)\n"), ("y15_loader_nghiem_tu_choi_khoa_trung_va_khoa_gop",)),
    ("test_bo_chot_cay_duoi_do", _test("    if Path(cay).resolve() != Path(goc).resolve():\n", "    if False:\n"), ("t95_lan_chay_day_du_chi_do_kho_chua_test",)),
    # ---- luot 5 (Codex P2/P3): chot phai do DUONG GOI THAT (main / doc_wf / dong in), khong chi helper
    ("test_main_khong_goi_chot_cay", _test("    loi_cay = loi_cay_duoi_do(CAY, ROOT_THAT)\n", "    loi_cay = ''\n"), ("t95_lan_chay_day_du_chi_do_kho_chua_test",)),
    ("test_main_chot_cay_sai_toan_hang", _test("    loi_cay = loi_cay_duoi_do(CAY, ROOT_THAT)\n", "    loi_cay = loi_cay_duoi_do(ROOT_THAT, ROOT_THAT)\n"), ("t95_lan_chay_day_du_chi_do_kho_chua_test",)),
    ("test_main_chot_cay_bo_return", _test("        print(loi_cay, file=sys.stderr)\n        return 2\n    dat = do = hong = 0\n", "        print(loi_cay, file=sys.stderr)\n    dat = do = hong = 0\n"), ("t95_lan_chay_day_du_chi_do_kho_chua_test",)),
    ("test_doc_wf_that_dung_safe_load", _test('    return doc_wf_tu((CAY / ".github" / "workflows" / "ci.yml").read_text(encoding="utf-8"))\n', '    return yaml.safe_load((CAY / ".github" / "workflows" / "ci.yml").read_text(encoding="utf-8"))\n'), ("y15_loader_nghiem_tu_choi_khoa_trung_va_khoa_gop",)),
    ("test_main_khong_in_kiem_ke", _test("    print(dong_kiem_ke())\n", ""), ("t94_main_in_dong_kiem_ke_that",)),
    ("test_main_in_kiem_ke_hai_lan", _test("    print(dong_kiem_ke())\n", "    print(dong_kiem_ke())\n    print(dong_kiem_ke())\n"), ("t94_main_in_dong_kiem_ke_that",)),
    ("test_main_in_kiem_ke_bi_doi", _test("    print(dong_kiem_ke())\n", "    print(dong_kiem_ke().replace('tu_kiem', 'tu kiem'))\n"), ("t94_main_in_dong_kiem_ke_that",)),
    # ---- chu kho (comment 5889513175): tran thoi gian cua chuan-bi
    ("yml_go_timeout_checkout_chuan_bi", _yml("        continue-on-error: true\n        timeout-minutes: 10\n", "        continue-on-error: true\n"), ("y16_chuan_bi_co_tran_thoi_gian_buoc_va_job", "y13_khoa_topology_cua_ci_yml_ngoai_than_run")),
    ("yml_go_timeout_phan_loai", _yml("        continue-on-error: true\n        timeout-minutes: 5\n", "        continue-on-error: true\n"), ("y16_chuan_bi_co_tran_thoi_gian_buoc_va_job", "y13_khoa_topology_cua_ci_yml_ngoai_than_run")),
    ("yml_go_timeout_job_chuan_bi", _yml("    timeout-minutes: 20\n    outputs:\n", "    outputs:\n"), ("y16_chuan_bi_co_tran_thoi_gian_buoc_va_job", "y13_khoa_topology_cua_ci_yml_ngoai_than_run")),
    ("yml_timeout_job_nho_hon_buoc", _yml("    timeout-minutes: 20\n    outputs:\n", "    timeout-minutes: 12\n    outputs:\n"), ("y16_chuan_bi_co_tran_thoi_gian_buoc_va_job",)),
    ("yml_timeout_checkout_qua_lon", _yml("        continue-on-error: true\n        timeout-minutes: 10\n", "        continue-on-error: true\n        timeout-minutes: 60\n"), ("y16_chuan_bi_co_tran_thoi_gian_buoc_va_job",)),
    # ---- luot 6 (executor tu liet ke): ket luan va ma thoat cua main / __main__
    ("test_main_ok_luon_dung", _test("    ok = (dat == len(CA) " + "> 0 and giet", "    ok = True or (dat == len(CA) " + "> 0 and giet"), ("t93_main_ket_luan_va_ma_thoat_theo_duong_goi_that",)),
    ("test_main_bo_kiem_ca_dat", _test("    ok = (dat == len(CA) " + "> 0 and giet", "    ok = (len(CA) " + "> 0 and giet"), ("t93_main_ket_luan_va_ma_thoat_theo_duong_goi_that",)),
    ("test_main_bo_kiem_so_giet", _test("and giet == len(DOT_BIEN) " + "> 0 and not xau", "and len(DOT_BIEN) " + "> 0 and not xau"), ("t93_main_ket_luan_va_ma_thoat_theo_duong_goi_that",)),
    ("test_main_bo_kiem_xau", _test("> 0 and not xau " + "and not loi_tu_kiem", "> 0 " + "and not loi_tu_kiem"), ("t93_main_ket_luan_va_ma_thoat_theo_duong_goi_that",)),
    ("test_main_bo_kiem_tu_kiem", _test("and not loi_tu_kiem " + "and trung == 0)", "and trung == 0)"), ("t93_main_ket_luan_va_ma_thoat_theo_duong_goi_that",)),
    ("test_main_bo_kiem_ten_trung", _test("and not loi_tu_kiem and trung " + "== 0)", "and not loi_tu_kiem)"), ("t93_main_ket_luan_va_ma_thoat_theo_duong_goi_that",)),
    ("test_main_in_ca_sai_tu_so", _test('    print(f"CA: {dat}' + '/{len(CA)} dat', '    print(f"CA: {len(CA)}' + '/{len(CA)} dat'), ("t93_main_ket_luan_va_ma_thoat_theo_duong_goi_that",)),
    ("test_main_in_dot_bien_sai_tu_so", _test('    print(f"DOT BIEN: {giet}' + '/{len(DOT_BIEN)}', '    print(f"DOT BIEN: {len(DOT_BIEN)}' + '/{len(DOT_BIEN)}'), ("t93_main_ket_luan_va_ma_thoat_theo_duong_goi_that",)),
    ("test_dunder_main_nuot_ma_thoat", _test("    raise SystemExit(main(sys.argv" + "[1:]))\n", "    main(sys.argv" + "[1:])\n    raise SystemExit(0)\n"), ("t93_main_ket_luan_va_ma_thoat_theo_duong_goi_that",)),
    # ---- luot 6 (Codex P2/P3): runner that goi ca, entrypoint that, tap neo KIEM KE
    ("test_runner_khong_goi_ca", _test("    try:\n        CA[ten]" + "()\n    except TinHieuChotCa", "    try:\n        pass\n    except TinHieuChotCa"), ("t92_runner_thuc_su_goi_ca_va_phan_biet_loi", "t91_ma_thoat_that_khi_ca_dat_do_va_hong")),
    ("test_runner_goi_ca_hai_lan", _test("    try:\n        CA[ten]" + "()\n    except TinHieuChotCa", "    try:\n        CA[ten]()\n        CA[ten]()\n    except TinHieuChotCa"), ("t92_runner_thuc_su_goi_ca_va_phan_biet_loi",)),
    ("test_runner_hong_thanh_do", _test('    except Exception as e:\n        return "HONG", f"{type(e).__name__}' + ': {e}"', '    except Exception as e:\n        return "DO", f"{type(e).__name__}: {e}"'), ("t92_runner_thuc_su_goi_ca_va_phan_biet_loi",)),
    ("test_runner_nuot_tin_hieu_do", _test('    except TinHieuChotCa as e:\n        return "DO", str(e)' + '\n    except Exception', '    except TinHieuChotCa as e:\n        return "DAT", ""\n    except Exception'), ("t92_runner_thuc_su_goi_ca_va_phan_biet_loi", "t91_ma_thoat_that_khi_ca_dat_do_va_hong")),
    ("test_entrypoint_rc1_thanh_0", _test("    raise SystemExit(main(sys.argv" + "[1:]))\n", "    _rc = main(sys.argv[1:])\n    raise SystemExit(0 if _rc == 1 else _rc)\n"), ("t91_ma_thoat_that_khi_ca_dat_do_va_hong",)),
    ("test_main_in_them_dong_kiem_ke_sai", _test("    print(dong_kiem_ke())" + "\n    for x in xau", "    print(dong_kiem_ke())\n    print('KIEM KE: ca hanh_vi=999 = 999')\n    for x in xau"), ("t94_main_in_dong_kiem_ke_that",)),
    ("test_main_in_dong_kiem_ke_sai_truoc", _test("    print(dong_kiem_ke())" + "\n    for x in xau", "    print('KIEM KE: sai')\n    print(dong_kiem_ke())\n    for x in xau"), ("t94_main_in_dong_kiem_ke_that",)),
    # ---- luot 7 (Claude, lop kiem-re-cua-fail-close-chua-co-ca): moi cua mot mutant, moi mutant mot ca dich
    ("kiem_yaml_bo_duoi_yml", _ma('for duong in sorted(x for x in doi if x.endswith((".yaml", ".yml"))):', 'for duong in sorted(x for x in doi if x.endswith(".yaml")):'), ("t20h_kiem_yaml_duoi_yml_ngoai_lease_do",)),
    ("kiem_yaml_tep_xoa_cat_vong", _ma("        if not tep.is_file():\n            continue\n        try:\n            with tep.open(encoding=\"utf-8\") as f:\n                list(", "        if not tep.is_file():\n            break\n        try:\n            with tep.open(encoding=\"utf-8\") as f:\n                list("), ("t20i_tep_da_xoa_khong_cat_vong_kiem_yaml",)),
    ("kiem_yaml_thieu_pyyaml_cho_qua", _ma('return ["KHONG DO DUOC: thieu PyYAML - khong parse duoc YAML nen khong cho qua"]', "return []"), ("t20j_thieu_pyyaml_la_khong_do_duoc",)),
    ("kiem_lease_thieu_pyyaml_cho_qua", _ma('return ["KHONG DO DUOC: thieu PyYAML - khong doc duoc lease"]', "return []"), ("t20j_thieu_pyyaml_la_khong_do_duoc",)),
    ("kiem_lease_nem_bo_qua", _ma('            loi.append(f"KHONG DO DUOC: kiem lease nem {type(e).__name__} cho {duong!r}")\n', ""), ("t20k_kiem_lease_nem_va_nhieu_tai_lieu_do",)),
    ("kiem_lease_parse_loi_bo_qua", _ma('            loi.append(f"lease khong parse duoc: {duong!r}: {type(e).__name__}")\n', ""), ("t20k_kiem_lease_nem_va_nhieu_tai_lieu_do",)),
    ("han_lease_bo_nhanh_datetime", _ma("        return gia_tri if gia_tri.tzinfo else gia_tri.replace(tzinfo=timezone.utc)\n    if isinstance(gia_tri, str):", "        return None\n    if isinstance(gia_tri, str):"), ("t20l_han_lease_timestamp_yaml_khong_nhay_ngoac",)),
    ("diff_check_nem_thanh_dat", _ma('        return [f"KHONG DO DUOC: git diff --check nem {type(e).__name__}"]', "        return []"), ("t20m_diff_check_nem_hoac_git_loi_do",)),
    ("diff_check_rc128_cho_qua", _ma('    if getattr(r, "returncode", None) == 0:\n        return []\n    dong', '    if getattr(r, "returncode", None) in (0, 128):\n        return []\n    dong'), ("t20m_diff_check_nem_hoac_git_loi_do",)),
    # ---- luot 7 (g3 Opus, P3): D1 thu hep tung loai; dong TU KIEM PHAN HANG co neo
    ("diff_check_bo_mien_space_before_tab", _ma('CAU_HINH_WHITESPACE = "core.whitespace=-blank-at-eol,-blank-at-eof,-space-before-tab"', 'CAU_HINH_WHITESPACE = "core.whitespace=-blank-at-eol,-blank-at-eof"'), ("t20d_kiem_re_khoang_trang_cuoi_dong_khong_do",)),
    ("diff_check_bo_mien_blank_at_eof", _ma('CAU_HINH_WHITESPACE = "core.whitespace=-blank-at-eol,-blank-at-eof,-space-before-tab"', 'CAU_HINH_WHITESPACE = "core.whitespace=-blank-at-eol,-space-before-tab"'), ("t20d_kiem_re_khoang_trang_cuoi_dong_khong_do",)),
    ("diff_check_bo_mien_blank_at_eol", _ma('CAU_HINH_WHITESPACE = "core.whitespace=-blank-at-eol,-blank-at-eof,-space-before-tab"', 'CAU_HINH_WHITESPACE = "core.whitespace=-blank-at-eof,-space-before-tab"'), ("t20d_kiem_re_khoang_trang_cuoi_dong_khong_do",)),
    ("test_main_tu_kiem_in_so_sai", _test("({len(MAU_RC)}" + " mau rc, {len(TU_KIEM_DOT_BIEN)} dot bien that)\")", "({len(MAU_RC) + 1} mau rc, {len(TU_KIEM_DOT_BIEN)} dot bien that)\")"), ("t93_main_ket_luan_va_ma_thoat_theo_duong_goi_that",)),
    ("test_main_tu_kiem_luon_in_dat", _test("{'DAT' if not loi_tu_kiem" + " else 'DO'} (", "{'DAT'} ("), ("t93_main_ket_luan_va_ma_thoat_theo_duong_goi_that",)),
    # ---- nghiệm thu 9: nối vào sổ test sống
    ("yml_go_buoc_goi_test_khoi_ci", _yml("      - name: ci-duong-nhanh selftest (phan loai diff + khoa cau truc if)\n        if: runner.os == 'Linux'\n        run: python ops/ci_duong_nhanh_test.py\n", ""), ("y09_buoc_goi_test_cua_packet_khong_bi_bo", "k03_ci_goi_that_muc_da_noi")),
    ("dk_go_muc_da_noi", (DK, lambda vb: thay_mot(vb, f'    "{DA_NOI_MUC}",\n', "")), ("k01_so_dang_ky_nhan_muc_da_noi",)),
    ("dk_go_muc_da_noi_kiem_dem_so", (DK, lambda vb: thay_mot(vb, f'    "{DA_NOI_MUC}",\n', "")), ("k02_da_noi_dung_mot_lan_va_test_song_khop_tep",)),
    # ---- cross-review luot 7: loai tep ho so (symlink)
    ("kiem_re_bo_loai_tep", _ma("kiem_yaml(doi, kho) + kiem_loai_tep(doi, kho) + ", "kiem_yaml(doi, kho) + "), ("t20n_kiem_re_symlink_ho_so_do",)),
    ("mot_merge_base_bo_chot_dang", _ma('            or not re.fullmatch(rb"[0-9a-f]{40}\\n", bytes(ra_mb)):', '            or False:'), ("t11b_nhieu_merge_base_la_khong_do_duoc",)),
    ("mot_merge_base_bo_goi", _ma('        mb = chay(["git", "merge-base", "--all", goc, dau], cwd=kho, capture_output=True)', '        mb = type("K", (), {"returncode": 0, "stdout": (goc + "\\n").encode()})()'), ("t11b_nhieu_merge_base_la_khong_do_duoc",)),
    ("mot_merge_base_bo_kiem_rc", _ma('    if getattr(mb, "returncode", None) != 0 or not isinstance(ra_mb,', '    if not isinstance(ra_mb,'), ("t11b_nhieu_merge_base_la_khong_do_duoc",)),
    ("mot_merge_base_nem_lot", _ma("    except Exception:\n        return None\n    ra_mb", "    except ZeroDivisionError:\n        return None\n    ra_mb"), ("t11b_nhieu_merge_base_la_khong_do_duoc",)),
    # ---- luot 9: duong vao thu hai cua lop ba-cham (goc doi ten ho so ra vung ma) — moi cua mot dot bien
    ("merge_that_bo_hop", _ma("    return ba_cham | khi_merge | khi_merge_that\n", "    return ba_cham | khi_merge_that\n"), ("t11c_goc_doi_ten_ho_so_ra_vung_ma_day_du",)),
    # ---- cross-review luot 9, lop `phan-loai-khong-neo-merge-ref-that`: moi cua mot dot bien
    ("merge_ref_bo_hop", _ma("    return ba_cham | khi_merge | khi_merge_that\n", "    return ba_cham | khi_merge\n"), ("t11d_merge_ref_that_dung_base_moi_hon_day_du",)),
    ("merge_ref_bo_kiem_dang", _ma('    if not (MAU_SHA.fullmatch(hop) and hop.strip("0")):\n        return None\n', ""), ("t05_thieu_hoac_hong_sha_day_du",)),
    ("merge_ref_chi_kiem_hex", _ma('    if not (MAU_SHA.fullmatch(hop) and hop.strip("0")):', "    if not MAU_SHA.fullmatch(hop):"), ("t05_thieu_hoac_hong_sha_day_du",)),
    ("merge_ref_loi_thanh_rong", _ma("    khi_merge_that = doc_diff_cay(goc, hop, chay, kho)\n", "    khi_merge_that = doc_diff_cay(goc, hop, chay, kho) or set()\n"), ("t11d_merge_ref_that_dung_base_moi_hon_day_du",)),
    ("merge_ref_doc_nham_dau", _ma("    khi_merge_that = doc_diff_cay(goc, hop, chay, kho)\n", "    khi_merge_that = doc_diff_cay(goc, dau, chay, kho)\n"), ("t11d_merge_ref_that_dung_base_moi_hon_day_du",)),
    ("merge_ref_doc_sai_bien", _ma('BIEN_MERGE = "CI_DUONG_NHANH_MERGE"', 'BIEN_MERGE = "CI_DUONG_NHANH_DAU"'), ("t11d_merge_ref_that_dung_base_moi_hon_day_du",)),
    ("merge_tree_bo_kiem_rc", _ma('    if getattr(mt, "returncode", None) != 0 or not isinstance(ra_mt,', '    if not isinstance(ra_mt,'), ("t11c_goc_doi_ten_ho_so_ra_vung_ma_day_du",)),
    ("merge_tree_bo_kiem_dang", _ma('            or not re.fullmatch(rb"[0-9a-f]{40}\\n", bytes(ra_mt)):', "            or False:"), ("t11c_goc_doi_ten_ho_so_ra_vung_ma_day_du",)),
    ("merge_tree_nem_thanh_rong", _ma("    except Exception:\n        return None\n    ra_mt", "    except Exception:\n        return set()\n    ra_mt"), ("t11c_goc_doi_ten_ho_so_ra_vung_ma_day_du",)),
    ("diff_cay_bo_kiem_rc", _ma('    if getattr(dt, "returncode", None) != 0 or not isinstance(ra_dt,', '    if not isinstance(ra_dt,'), ("t11c_goc_doi_ten_ho_so_ra_vung_ma_day_du",)),
    ("diff_cay_nem_thanh_rong", _ma("    except Exception:\n        return None\n    ra_dt", "    except Exception:\n        return set()\n    ra_dt"), ("t11c_goc_doi_ten_ho_so_ra_vung_ma_day_du",)),
    ("diff_cay_bo_kiem_cut", _ma('    if ra_dt and not bytes(ra_dt).endswith(b"\\0"):\n        return None\n', ""), ("t11c_goc_doi_ten_ho_so_ra_vung_ma_day_du",)),
    # ---- luot 9: lop kiem-re-bi-cau-hinh-boi-du-lieu-ho-so — thuoc tinh doc tu cay GOC; va phan chung: khong chan .gitattributes
    ("diff_check_bo_attr_source", _ma('["git", "--attr-source=" + goc, "-c", CAU_HINH_WHITESPACE', '["git", "-c", CAU_HINH_WHITESPACE'), ("t20p_kiem_re_gitattributes_trong_ho_so_khong_cau_hinh_duoc_diff_check", "t20u_moi_loi_goi_git_doc_thuoc_tinh_tu_goc")),
    # ---- cross-review luot 9, lop `kiem-re-bi-cau-hinh-boi-du-lieu-ho-so`: MOI duong vao doc thuoc tinh mot dot bien
    ("nhi_phan_bo_attr_source", _ma('ns = chay(["git", "--attr-source=" + goc, "diff", "--numstat"', 'ns = chay(["git", "diff", "--numstat"'), ("t20t_kiem_re_thuoc_tinh_diff_cua_pr_khong_bien_nhi_phan_thanh_van_ban", "t20u_moi_loi_goi_git_doc_thuoc_tinh_tu_goc")),
    ("merge_tree_bo_attr_source", _ma('mt = chay(["git", "--attr-source=" + goc, "merge-tree"', 'mt = chay(["git", "merge-tree"'), ("t11e_thuoc_tinh_cua_pr_khong_cau_hinh_duoc_merge_tree", "t20u_moi_loi_goi_git_doc_thuoc_tinh_tu_goc")),
    ("ba_cham_bo_attr_source", _ma('r = chay(["git", "--attr-source=" + goc, "diff", "--name-only"', 'r = chay(["git", "diff", "--name-only"'), ("t20u_moi_loi_goi_git_doc_thuoc_tinh_tu_goc",)),
    ("diff_cay_bo_attr_source", _ma('dt = chay(["git", "--attr-source=" + goc, "diff", "--no-renames"', 'dt = chay(["git", "diff", "--no-renames"'), ("t20u_moi_loi_goi_git_doc_thuoc_tinh_tu_goc",)),
    ("nhi_phan_attr_source_la_dau", _ma('ns = chay(["git", "--attr-source=" + goc, "diff", "--numstat"', 'ns = chay(["git", "--attr-source=" + dau, "diff", "--numstat"'), ("t20t_kiem_re_thuoc_tinh_diff_cua_pr_khong_bien_nhi_phan_thanh_van_ban", "t20u_moi_loi_goi_git_doc_thuoc_tinh_tu_goc")),
    ("merge_tree_attr_source_la_dau", _ma('mt = chay(["git", "--attr-source=" + goc, "merge-tree"', 'mt = chay(["git", "--attr-source=" + dau, "merge-tree"'), ("t11e_thuoc_tinh_cua_pr_khong_cau_hinh_duoc_merge_tree", "t20u_moi_loi_goi_git_doc_thuoc_tinh_tu_goc")),
    ("loai_tep_chan_gitattributes", _ma("            for duong in sorted(doi) if (Path(kho) / duong).is_symlink()]", "            for duong in sorted(doi) if (Path(kho) / duong).is_symlink() or duong.endswith('.gitattributes')]"), ("t20p_kiem_re_gitattributes_trong_ho_so_khong_cau_hinh_duoc_diff_check",)),
    # ---- luot 9: pham vi diff --check — tep nhi phan
    ("kiem_re_bo_nhi_phan", _ma(" + kiem_nhi_phan(env, chay, kho)\n", "\n"), ("t20s_kiem_re_tep_nhi_phan_la_khong_do_duoc",)),
    ("nhi_phan_bo_nhan_dien", _ma('if ban_ghi.startswith("-\\t-\\t")]', "if False]"), ("t20s_kiem_re_tep_nhi_phan_la_khong_do_duoc",)),
    ("nhi_phan_nem_thanh_dat", _ma('        return [f"KHONG DO DUOC: git diff --numstat nem {type(e).__name__}"]', "        return []"), ("t20s_kiem_re_tep_nhi_phan_la_khong_do_duoc",)),
    ("nhi_phan_rc_cho_qua", _ma('    if getattr(ns, "returncode", None) != 0 or not isinstance(ra_ns,', '    if not isinstance(ra_ns,'), ("t20s_kiem_re_tep_nhi_phan_la_khong_do_duoc",)),
    ("nhi_phan_cut_cho_qua", _ma('        return ["KHONG DO DUOC: git diff --numstat dau ra cut"]', "        return []"), ("t20s_kiem_re_tep_nhi_phan_la_khong_do_duoc",)),
    ("loai_tep_chi_chan_treo", _ma("for duong in sorted(doi) if (Path(kho) / duong).is_symlink()]", "for duong in sorted(doi) if (Path(kho) / duong).is_symlink() and not (Path(kho) / duong).exists()]"), ("t20q_kiem_re_symlink_hop_le_moi_duoi_do",)),
    ("loai_tep_chi_md", _ma("for duong in sorted(doi) if (Path(kho) / duong).is_symlink()]", "for duong in sorted(doi) if (Path(kho) / duong).is_symlink() and duong.endswith('.md')]"), ("t20q_kiem_re_symlink_hop_le_moi_duoi_do",)),
    ("diff_check_chi_md", _ma('diff", "--check", "--no-renames", f"{goc}...{dau}"]', 'diff", "--check", "--no-renames", f"{goc}...{dau}", "--", "*.md"]'), ("t20r_kiem_re_dau_xung_dot_moi_duoi_tep_do",)),
    ("kiem_yaml_chi_tai_lieu_dau", _ma("list(yaml.safe_load_all(f))", "next(yaml.safe_load_all(f), None)"), ("t20o_kiem_re_yaml_nhieu_tai_lieu_hong_o_sau_do",)),
    ("loai_tep_cho_symlink_qua", _ma("for duong in sorted(doi) if (Path(kho) / duong).is_symlink()]", "for duong in sorted(doi) if False]"), ("t20n_kiem_re_symlink_ho_so_do",)),
    # ---- cross-review luot 10, lop `kiem-re-cua-fail-close-chua-co-ca`: loai tep theo MODE TRONG GIT — moi cua mot dot bien
    ('kiem_re_bo_mode_git', _ma('           + kiem_mode_git(env, chay, kho, doi)\n', ''), ('t20v_kiem_re_gitlink_ho_so_do',)),
    ('mode_git_nhan_gitlink', _ma('MODE_THUONG = {"100644", "100755"}', 'MODE_THUONG = {"100644", "100755", "160000"}'), ('t20v_kiem_re_gitlink_ho_so_do',)),
    ('mode_git_chi_kiem_them_moi', _ma('            if trang_thai == "D" or mode not in MODE_THUONG:', '            if trang_thai == "A" and mode not in MODE_THUONG:'), ('t20w_kiem_re_tep_ho_so_doi_thanh_gitlink_do',)),
    ('mode_git_nhan_symlink', _ma('MODE_THUONG = {"100644", "100755"}', 'MODE_THUONG = {"100644", "100755", "120000"}'), ('t20x_kiem_re_symlink_tren_nen_khong_symlink_do',)),
    ('mode_git_chan_755', _ma('MODE_THUONG = {"100644", "100755"}', 'MODE_THUONG = {"100644"}'), ('t20y_kiem_re_mode_755_va_tep_thanh_thu_muc_dat',)),
    ('mode_git_xoa_la_loi', _ma('            if trang_thai == "D" and mode == "000000":\n                continue\n', ''), ('t20y_kiem_re_mode_755_va_tep_thanh_thu_muc_dat',)),
    ('mode_git_bo_kiem_dia', _ma('            elif ten_cap == "goc -> merge ref" and (', '            elif False and ('), ('t20z_kiem_re_git_co_tep_ma_dia_khong_co_do',)),
    ('mode_git_bo_cap_ba_cham', _ma('    for ten_cap, cap in (("ba cham", (f"{goc}...{dau}",)), ', '    for ten_cap, cap in ('), ('t20za_kiem_mode_git_doc_du_ba_cap',)),
    ('mode_git_bo_cap_cay', _ma('("goc -> cay merge-tree", (goc, cay)),\n', '\n'), ('t20za_kiem_mode_git_doc_du_ba_cap',)),
    ('mode_git_bo_cap_hop', _ma(',\n                         ("goc -> merge ref", (goc, hop))):', ',):'), ('t20za_kiem_mode_git_doc_du_ba_cap',)),
    ('mode_git_cap_hop_doc_dau', _ma('("goc -> merge ref", (goc, hop))', '("goc -> merge ref", (goc, dau))'), ('t20za_kiem_mode_git_doc_du_ba_cap',)),
    ('mode_git_raw_bo_attr_source', _ma('r = chay(["git", "--attr-source=" + goc, "diff", "--raw"', 'r = chay(["git", "diff", "--raw"'), ('t20u_moi_loi_goi_git_doc_thuoc_tinh_tu_goc',)),
    ('mode_git_merge_tree_bo_attr_source', _ma('mt_mode = chay(["git", "--attr-source=" + goc, "merge-tree"', 'mt_mode = chay(["git", "merge-tree"'), ('t20u_moi_loi_goi_git_doc_thuoc_tinh_tu_goc',)),
    ('mode_git_raw_rc_cho_qua', _ma('    if getattr(r, "returncode", None) != 0 or not isinstance(ra, (bytes, bytearray)):\n        return f"KHONG DO DUOC: git diff --raw', '    if not isinstance(ra, (bytes, bytearray)):\n        return f"KHONG DO DUOC: git diff --raw'), ('t20zb_kiem_mode_git_khong_do_duoc_thi_do',)),
    ('mode_git_raw_nem_lot', _ma('    except Exception as e:\n        return f"KHONG DO DUOC: git diff --raw', '    except ZeroDivisionError as e:\n        return f"KHONG DO DUOC: git diff --raw'), ('t20zb_kiem_mode_git_khong_do_duoc_thi_do',)),
    ('mode_git_raw_cut_cho_qua', _ma('    if ra and not bytes(ra).endswith(b"\\0"):\n        return f"KHONG DO DUOC: git diff --raw {\' \'.join(cap)} dau ra cut"\n', ''), ('t20zb_kiem_mode_git_khong_do_duoc_thi_do',)),
    ('mode_git_bo_kiem_le', _ma('    if len(muc) % 2:\n', '    if False:\n'), ('t20zb_kiem_mode_git_khong_do_duoc_thi_do',)),
    ('mode_git_dau_ghi_long', _ma('r":([0-7]{6}) ([0-7]{6}) ([0-9a-f]{40}(?:[0-9a-f]{24})?) ([0-9a-f]{40}(?:[0-9a-f]{24})?) ([AMDT])"', 'r":([0-7]{6}) ([0-7]{6}) (\\S+) (\\S+) ([A-Z])"'), ('t20zb_kiem_mode_git_khong_do_duoc_thi_do',)),
    ('mode_git_bo_kiem_trung', _ma(' or not duong or duong in kq:', ' or not duong:'), ('t20zb_kiem_mode_git_khong_do_duoc_thi_do',)),
    ('mode_git_xoa_bo_kiem_mode', _ma('            if trang_thai == "D" and mode == "000000":', '            if trang_thai == "D":'), ('t20zb_kiem_mode_git_khong_do_duoc_thi_do',)),
    ('mode_git_bo_kiem_tap', _ma('    if thay != set(doi):', '    if False:'), ('t20zb_kiem_mode_git_khong_do_duoc_thi_do',)),
    # ---- cross-review luot 11, lop `kiem-mode-git-chot-khong-rang`
    ('mode_git_raw_bo_no_renames', _ma('"diff", "--raw", "-z", "--no-renames", "--no-abbrev"', '"diff", "--raw", "-z", "--no-abbrev"'), ('t20zc_kiem_re_doi_ten_tep_ho_so_dat',)),
    ('mode_git_tap_chi_bat_thua', _ma('    if thay != set(doi):', '    if not thay <= set(doi):'), ('t20zb_kiem_mode_git_khong_do_duoc_thi_do',)),
    ('mode_git_xoa_chi_theo_mode', _ma('            if trang_thai == "D" or mode not in MODE_THUONG:', '            if mode not in MODE_THUONG:'), ('t20zb_kiem_mode_git_khong_do_duoc_thi_do',)),
    # ---- luot 12: liet ke het chot/doi so cua `_doc_raw` + `kiem_mode_git`, MOI chot mot dot bien rieng
    ('mode_git_raw_bo_z', _ma('"diff", "--raw", "-z", "--no-renames", "--no-abbrev"', '"diff", "--raw", "--no-renames", "--no-abbrev"'), ('t20zc_kiem_re_doi_ten_tep_ho_so_dat',)),
    ('mode_git_raw_bo_no_abbrev', _ma('"diff", "--raw", "-z", "--no-renames", "--no-abbrev"', '"diff", "--raw", "-z", "--no-renames"'), ('t20zc_kiem_re_doi_ten_tep_ho_so_dat',)),
    ('mode_git_raw_bo_co_raw', _ma('"diff", "--raw", "-z", "--no-renames", "--no-abbrev"', '"diff", "-z", "--no-renames", "--no-abbrev"'), ('t20zc_kiem_re_doi_ten_tep_ho_so_dat',)),
    ('mode_git_raw_attr_la_dau', _ma('r = chay(["git", "--attr-source=" + goc, "diff", "--raw"', 'r = chay(["git", "--attr-source=" + cap[-1], "diff", "--raw"'), ('t20u_moi_loi_goi_git_doc_thuoc_tinh_tu_goc',)),
    ('mode_git_merge_tree_attr_la_dau', _ma('mt_mode = chay(["git", "--attr-source=" + goc, "merge-tree"', 'mt_mode = chay(["git", "--attr-source=" + dau, "merge-tree"'), ('t20u_moi_loi_goi_git_doc_thuoc_tinh_tu_goc',)),
    ('mode_git_raw_bo_kiem_kieu', _ma('    if getattr(r, "returncode", None) != 0 or not isinstance(ra, (bytes, bytearray)):', '    if getattr(r, "returncode", None) != 0:'), ('t20zb_kiem_mode_git_khong_do_duoc_thi_do',)),
    ('mode_git_merge_tree_bo_kiem_kieu', _ma('    if getattr(mt_mode, "returncode", None) != 0 or not isinstance(ra_cay, (bytes, bytearray)) \\', '    if getattr(mt_mode, "returncode", None) != 0 \\'), ('t20zb_kiem_mode_git_khong_do_duoc_thi_do',)),
    ('mode_git_raw_rong_la_cut', _ma('    if ra and not bytes(ra).endswith(b"\\0"):\n        return f"KHONG DO DUOC: git diff --raw', '    if not bytes(ra).endswith(b"\\0"):\n        return f"KHONG DO DUOC: git diff --raw'), ('t20zb_kiem_mode_git_khong_do_duoc_thi_do',)),
    ('mode_git_raw_trang_thai_long', _ma('r":([0-7]{6}) ([0-7]{6}) ([0-9a-f]{40}(?:[0-9a-f]{24})?) ([0-9a-f]{40}(?:[0-9a-f]{24})?) ([AMDT])"', 'r":([0-7]{6}) ([0-7]{6}) ([0-9a-f]{40}(?:[0-9a-f]{24})?) ([0-9a-f]{40}(?:[0-9a-f]{24})?) ([A-Z])"'), ('t20zb_kiem_mode_git_khong_do_duoc_thi_do',)),
    ('mode_git_raw_sha_long', _ma('r":([0-7]{6}) ([0-7]{6}) ([0-9a-f]{40}(?:[0-9a-f]{24})?) ([0-9a-f]{40}(?:[0-9a-f]{24})?) ([AMDT])"', 'r":([0-7]{6}) ([0-7]{6}) (\\S+) (\\S+) ([AMDT])"'), ('t20zb_kiem_mode_git_khong_do_duoc_thi_do',)),
    ('mode_git_raw_nhan_duong_rong', _ma(' or not duong or duong in kq:', ' or duong in kq:'), ('t20zb_kiem_mode_git_khong_do_duoc_thi_do',)),
    ('mode_git_raw_doc_mode_cu', _ma('kq[duong] = (k.group(2), k.group(5))', 'kq[duong] = (k.group(1), k.group(5))'), ('t20zc_kiem_re_doi_ten_tep_ho_so_dat',)),
    ('mode_git_loi_cap_bo_qua', _ma('        if isinstance(ban_ghi, str):\n            return [ban_ghi]', '        if isinstance(ban_ghi, str):\n            continue'), ('t20zb_kiem_mode_git_khong_do_duoc_thi_do',)),
    ('mode_git_thay_gan_de', _ma('        thay |= set(ban_ghi)', '        thay = set(ban_ghi)'), ('t20zb_kiem_mode_git_khong_do_duoc_thi_do',)),
    ('mode_git_tap_chi_bat_thieu', _ma('    if thay != set(doi):', '    if not thay >= set(doi):'), ('t20zb_kiem_mode_git_khong_do_duoc_thi_do',)),
    ('mode_git_dia_bo_is_file', _ma('((Path(kho) / duong).is_symlink() or not (Path(kho) / duong).is_file())', '((Path(kho) / duong).is_symlink())'), ('t20z_kiem_re_git_co_tep_ma_dia_khong_co_do',)),
    ('mode_git_dia_bo_is_symlink', _ma('((Path(kho) / duong).is_symlink() or not (Path(kho) / duong).is_file())', '(not (Path(kho) / duong).is_file())'), ('t20zd_kiem_mode_git_dia_la_symlink_do',)),
    ('mode_git_dia_moi_cap', _ma('            elif ten_cap == "goc -> merge ref" and (', '            elif ('), ('t20zb_kiem_mode_git_khong_do_duoc_thi_do',)),
    # ---- cross-review luot 12: doi so commit cua merge-tree (kiem mode), fullmatch, ve D cua nhanh xoa, giai ma surrogateescape
    ('mode_git_merge_tree_goc_goc', _ma('"--no-messages", goc, dau],\n                       cwd=kho, capture_output=True)\n    except Exception as e:\n        return [f"KHONG DO DUOC: merge-tree (kiem mode)', '"--no-messages", goc, goc],\n                       cwd=kho, capture_output=True)\n    except Exception as e:\n        return [f"KHONG DO DUOC: merge-tree (kiem mode)'), ('t20u_moi_loi_goi_git_doc_thuoc_tinh_tu_goc',)),
    ('mode_git_merge_tree_dau_dau', _ma('"--no-messages", goc, dau],\n                       cwd=kho, capture_output=True)\n    except Exception as e:\n        return [f"KHONG DO DUOC: merge-tree (kiem mode)', '"--no-messages", dau, dau],\n                       cwd=kho, capture_output=True)\n    except Exception as e:\n        return [f"KHONG DO DUOC: merge-tree (kiem mode)'), ('t20u_moi_loi_goi_git_doc_thuoc_tinh_tu_goc',)),
    ('mode_git_raw_match_khong_full', _ma('k = MAU_BAN_GHI_RAW.fullmatch(dau_ghi)', 'k = MAU_BAN_GHI_RAW.match(dau_ghi)'), ('t20zb_kiem_mode_git_khong_do_duoc_thi_do',)),
    ('mode_git_xoa_bo_ve_D', _ma('            if trang_thai == "D" and mode == "000000":', '            if mode == "000000":'), ('t20zb_kiem_mode_git_khong_do_duoc_thi_do',)),
    ('mode_git_raw_giai_ma_chat', _ma('muc = bytes(ra).decode("utf-8", "surrogateescape")', 'muc = bytes(ra).decode("utf-8")'), ('t20ze_kiem_re_ten_tep_khong_utf8_dat',)),
    # ---- luot 12, luot ra soat he thong cuoi (executor): moi doi so / chuoi / phep giai ma con lai cua kiem_mode_git va _doc_raw
    ('mode_git_merge_tree_bo_write_tree', _ma('"merge-tree", "--write-tree", "--no-messages", goc, dau],\n                       cwd=kho, capture_output=True)\n    except Exception as e:\n        return [f"KHONG DO DUOC: merge-tree (kiem mode)', '"merge-tree", "--no-messages", goc, dau],\n                       cwd=kho, capture_output=True)\n    except Exception as e:\n        return [f"KHONG DO DUOC: merge-tree (kiem mode)'), ('t20u_moi_loi_goi_git_doc_thuoc_tinh_tu_goc',)),
    ('mode_git_cay_bo_strip', _ma('    cay = bytes(ra_cay).decode("ascii").strip()', '    cay = bytes(ra_cay).decode("ascii")'), ('t20u_moi_loi_goi_git_doc_thuoc_tinh_tu_goc',)),
    ('mode_git_merge_tree_dang_bo_xuong_dong', _ma('re.fullmatch(rb"[0-9a-f]{40}(?:[0-9a-f]{24})?\\n", bytes(ra_cay))', 're.fullmatch(rb"[0-9a-f]{40}(?:[0-9a-f]{24})?", bytes(ra_cay))'), ('t20zc_kiem_re_doi_ten_tep_ho_so_dat',)),
    ('mode_git_cap_cay_doc_dau', _ma('("goc -> cay merge-tree", (goc, cay))', '("goc -> cay merge-tree", (goc, dau))'), ('t20za_kiem_mode_git_doc_du_ba_cap',)),
    ('mode_git_ba_cham_thanh_hai_cham', _ma('("ba cham", (f"{goc}...{dau}",))', '("ba cham", (f"{goc}..{dau}",))'), ('t20u_moi_loi_goi_git_doc_thuoc_tinh_tu_goc',)),
    ('mode_git_raw_split_khong_cat', _ma('decode("utf-8", "surrogateescape").split("\\0")[:-1]', 'decode("utf-8", "surrogateescape").split("\\0")'), ('t20zc_kiem_re_doi_ten_tep_ho_so_dat',)),
    ('mode_git_raw_zip_dao', _ma('zip(muc[0::2], muc[1::2])', 'zip(muc[1::2], muc[0::2])'), ('t20zc_kiem_re_doi_ten_tep_ho_so_dat',)),
    ('mode_git_bo_644', _ma('MODE_THUONG = {"100644", "100755"}', 'MODE_THUONG = {"100755"}'), ('t20zc_kiem_re_doi_ten_tep_ho_so_dat',)),
    # ---- cross-review luot 13: nhanh CHAP NHAN cua trang thai `T` voi mode tep thuong
    ('mode_git_doi_kieu_thanh_tep_la_loi', _ma('            if trang_thai == "D" or mode not in MODE_THUONG:', '            if trang_thai in ("D", "T") or mode not in MODE_THUONG:'), ('t20zf_kiem_re_symlink_doi_thanh_tep_thuong_dat',)),
    # ---- luot 14: moi o CHAP NHAN (trang thai x mode moi) mot dot bien rieng coi dung o do la loi
    ('mode_git_o_A_644_la_loi', _ma('            if trang_thai == "D" or mode not in MODE_THUONG:', '            if trang_thai == "D" or mode not in MODE_THUONG or (trang_thai == "A" and mode == "100644"):'), ('t20a_kiem_re_ho_so_sach_dat',)),
    ('mode_git_o_A_755_la_loi', _ma('            if trang_thai == "D" or mode not in MODE_THUONG:', '            if trang_thai == "D" or mode not in MODE_THUONG or (trang_thai == "A" and mode == "100755"):'), ('t20zg_kiem_re_o_chap_nhan_con_lai_dat',)),
    ('mode_git_o_M_644_la_loi', _ma('            if trang_thai == "D" or mode not in MODE_THUONG:', '            if trang_thai == "D" or mode not in MODE_THUONG or (trang_thai == "M" and mode == "100644"):'), ('t20zg_kiem_re_o_chap_nhan_con_lai_dat',)),
    ('mode_git_o_M_755_la_loi', _ma('            if trang_thai == "D" or mode not in MODE_THUONG:', '            if trang_thai == "D" or mode not in MODE_THUONG or (trang_thai == "M" and mode == "100755"):'), ('t20y_kiem_re_mode_755_va_tep_thanh_thu_muc_dat',)),
    ('mode_git_o_T_644_la_loi', _ma('            if trang_thai == "D" or mode not in MODE_THUONG:', '            if trang_thai == "D" or mode not in MODE_THUONG or (trang_thai == "T" and mode == "100644"):'), ('t20zf_kiem_re_symlink_doi_thanh_tep_thuong_dat',)),
    ('mode_git_o_T_755_la_loi', _ma('            if trang_thai == "D" or mode not in MODE_THUONG:', '            if trang_thai == "D" or mode not in MODE_THUONG or (trang_thai == "T" and mode == "100755"):'), ('t20zg_kiem_re_o_chap_nhan_con_lai_dat',)),
    # ---- cross-review luot 14 (lop `kiem-mode-git-chot-khong-rang`, LAN 4): dot bien X1 cua reviewer — mien tru trang thai `M`
    # khoi chot mode (FAIL-OPEN: doi dich symlink / nang con tro gitlink da co tren nen). Cac o lat rieng: `mode_git_lat_o_*`.
    ('mode_git_mien_tru_M', _ma('            if trang_thai == "D" or mode not in MODE_THUONG:', '            if trang_thai == "D" or (mode not in MODE_THUONG and trang_thai != "M"):'), ('t20zh_kiem_mode_git_bang_quyet_dinh_day_du',)),
    ('mode_git_merge_tree_rc_cho_qua', _ma('    if getattr(mt_mode, "returncode", None) != 0 or not isinstance(ra_cay,', '    if not isinstance(ra_cay,'), ('t20zb_kiem_mode_git_khong_do_duoc_thi_do',)),
    ('mode_git_merge_tree_nem_lot', _ma('    except Exception as e:\n        return [f"KHONG DO DUOC: merge-tree (kiem mode) nem', '    except ZeroDivisionError as e:\n        return [f"KHONG DO DUOC: merge-tree (kiem mode) nem'), ('t20zb_kiem_mode_git_khong_do_duoc_thi_do',)),
    ('mode_git_merge_tree_bo_kiem_dang', _ma('            or not re.fullmatch(rb"[0-9a-f]{40}(?:[0-9a-f]{24})?\\n", bytes(ra_cay)):', '            or False:'), ('t20zb_kiem_mode_git_khong_do_duoc_thi_do',)),
    # ---- cross-review luot 8b (P2 `buoc-bi-bo-doc-ca-cay-khong-chi-ba-ca`): symlink TREO ngoai diff — moi duong vao mot dot bien
    ("kiem_re_bo_symlink_treo_ca_cay", _ma("           + kiem_symlink_treo_ca_cay(kho)\n", ""), ("t20zi_kiem_re_symlink_treo_ngoai_diff_do",)),
    ("symlink_treo_vi_tu_luon_sai", _ma("            if os.path.islink(p) and not os.path.exists(p):\n", "            if False:\n"), ("t20zi_kiem_re_symlink_treo_ngoai_diff_do",)),
    ("symlink_treo_chi_cap_goc", _ma("    for goc, thu_muc, tep in os.walk(kho, onerror=khong_doc_duoc, followlinks=True):\n", "    for goc, thu_muc, tep in [next(os.walk(kho, onerror=khong_doc_duoc, followlinks=True), (str(kho), [], []))]:\n"), ("t20zi_kiem_re_symlink_treo_ngoai_diff_do",)),
    ("symlink_treo_bo_qua_allowlist", _ma("        thu_muc[:] = sorted(d for d in thu_muc if d not in bo)\n", "        thu_muc[:] = sorted(d for d in thu_muc if d not in bo and not (os.path.relpath(os.path.join(goc, d), kho).replace(os.sep, '/') + '/').startswith(ALLOWLIST_TIEN_TO))\n"), ("t20zi_kiem_re_symlink_treo_ngoai_diff_do",)),
    ("symlink_treo_doc_tu_vung", _ma("            if os.path.islink(p) and not os.path.exists(p):\n", "            if os.path.islink(p) and not os.path.exists(os.path.normpath(os.path.join(goc, os.readlink(p)))):\n"), ("t20zi_kiem_re_symlink_treo_ngoai_diff_do",)),
    ("symlink_treo_bo_qua_thu_muc_cham", _ma("        bo = bo_qua(goc, thu_muc + tep)\n", "        bo = bo_qua(goc, thu_muc + tep) | {x for x in thu_muc if x.startswith('.')}\n"), ("t20zi_kiem_re_symlink_treo_ngoai_diff_do",)),
    ("symlink_treo_khong_bo_git", _ma('BO_QUA_NHU_T82 = (".git", "__pycache__", "*.pyc")', 'BO_QUA_NHU_T82 = ("__pycache__", "*.pyc")'), ("t20zi_kiem_re_symlink_treo_ngoai_diff_do",)),
    ("symlink_treo_khong_bo_pycache", _ma('BO_QUA_NHU_T82 = (".git", "__pycache__", "*.pyc")', 'BO_QUA_NHU_T82 = (".git", "*.pyc")'), ("t20zi_kiem_re_symlink_treo_ngoai_diff_do",)),
    ("symlink_treo_khong_bo_pyc", _ma('BO_QUA_NHU_T82 = (".git", "__pycache__", "*.pyc")', 'BO_QUA_NHU_T82 = (".git", "__pycache__")'), ("t20zi_kiem_re_symlink_treo_ngoai_diff_do",)),
    ("symlink_treo_nuot_loi_duyet", _ma("os.walk(kho, onerror=khong_doc_duoc, followlinks=True)", "os.walk(kho, followlinks=True)"), ("t20zj_symlink_treo_khong_duyet_duoc_va_dong_bo_t82",)),
    ("symlink_treo_bo_qua_rong_hon_t82", _ma('BO_QUA_NHU_T82 = (".git", "__pycache__", "*.pyc")', 'BO_QUA_NHU_T82 = (".git", "__pycache__", "*.pyc", "*.md")'), ("t20zj_symlink_treo_khong_duyet_duoc_va_dong_bo_t82",)),
    # ---- lop `buoc-bi-bo-doc-ca-cay-khong-chi-ba-ca` (cross-review luot 17 mo lai, luot 18 dong THEO LOP): bo duyet phai di DUNG
    # duong `t82` di. Moi duong vao mot chot, moi chot mot dot bien chi ca cua duong vao ay bat (xem khoi chu thich truoc `t20zk`).
    # (1) bi danh thu muc: thoi theo symlink thu muc; ap mau bo qua len TEN DICH cua bi danh (moi ten dich mot dot bien)
    ("symlink_treo_khong_theo_bi_danh", _ma("onerror=khong_doc_duoc, followlinks=True)", "onerror=khong_doc_duoc)"), ("t20zk_kiem_re_symlink_treo_qua_bi_danh_thu_muc_do", "t20zo_la_khong_phai_tep_thuong_do")),
    ("symlink_treo_ap_mau_len_ten_dich_pycache", _ma("            di_tiep.append(d)\n", "            if not (os.path.islink(p) and os.path.basename(os.path.realpath(p)) == '__pycache__'):\n                di_tiep.append(d)\n"), ("t20zk_kiem_re_symlink_treo_qua_bi_danh_thu_muc_do",)),
    ("symlink_treo_ap_mau_len_ten_dich_pyc", _ma("            di_tiep.append(d)\n", "            if not (os.path.islink(p) and os.path.realpath(p).endswith('.pyc')):\n                di_tiep.append(d)\n"), ("t20zk_kiem_re_symlink_treo_qua_bi_danh_thu_muc_do",)),
    # (2) thu tu ap mau bo qua: khong ap o cap sau bi danh; theo bi danh mang ten bi bo qua
    ("symlink_treo_bo_qua_khong_ap_sau_bi_danh", _ma("        bo = bo_qua(goc, thu_muc + tep)\n", "        bo = bo_qua(goc, thu_muc + tep) if os.path.realpath(goc) == os.path.abspath(goc) else set()\n"), ("t20zl_mau_bo_qua_ap_theo_ten_muc_o_moi_cap_nhu_t82",)),
    ("symlink_treo_theo_bi_danh_ten_bi_bo_qua", _ma("        thu_muc[:] = sorted(d for d in thu_muc if d not in bo)\n", "        thu_muc[:] = sorted(d for d in thu_muc if d not in bo or os.path.islink(os.path.join(goc, d)))\n"), ("t20zl_mau_bo_qua_ap_theo_ten_muc_o_moi_cap_nhu_t82",)),
    # (3) vong: khong phat hien; chi so thu muc cha (sot vong ve to tien); bao ca lan tham lai KHONG vong; nuot loi lay danh tinh
    ("vong_khong_phat_hien", _ma("            if dd in tren:\n", "            if False:\n"), ("t20zm_vong_symlink_thu_muc_do_va_khong_bung_no",)),
    ("vong_chi_so_thu_muc_cha", _ma("            if dd in tren:\n", "            if dd == danh_tinh(goc):\n"), ("t20zm_vong_symlink_thu_muc_do_va_khong_bung_no",)),
    ("vong_bao_ca_tham_lai_khong_vong", _ma("            if dd in tren:\n", "            da = to_tien.setdefault('', set())\n            moi = dd not in da\n            da.add(dd)\n            if dd in tren or not moi:\n"), ("t20zm_vong_symlink_thu_muc_do_va_khong_bung_no",)),
    ("vong_danh_tinh_nuot_loi", _ma("            khong_doc_duoc(e)\n            return None\n", "            return None\n"), ("t20zm_vong_symlink_thu_muc_do_va_khong_bung_no",)),
    # (4) khu trung thu muc DA VAO (toan cuc, im lang): lot chuoi khong vong khi thu tu ten dua duong ngan toi truoc
    ("chuoi_khu_trung_da_vao_toan_cuc", (MA, lambda vb: thay_mot(thay_mot(vb, _NEO_TREN, _NEO_TREN + "        to_tien.setdefault('', set()).update(tren)\n"), "            if dd in tren:\n", "            if dd in to_tien[''] and dd not in tren:\n                continue\n            if dd in tren:\n")), ("t20zn_chuoi_symlink_khong_vong_qua_gioi_han_phan_giai_do",)),
    # (5) la: bo chot tep thuong; noi danh sach cho phep them FIFO / socket; doc la KHONG theo symlink
    ("la_bo_chot_tep_thuong", _ma("            elif not os.path.isfile(p):\n", "            elif False:\n"), ("t20zo_la_khong_phai_tep_thuong_do",)),
    ("la_cho_phep_fifo", _ma("            elif not os.path.isfile(p):\n", "            elif not (os.path.isfile(p) or __import__('stat').S_ISFIFO(os.stat(p).st_mode)):\n"), ("t20zo_la_khong_phai_tep_thuong_do",)),
    ("la_cho_phep_socket", _ma("            elif not os.path.isfile(p):\n", "            elif not (os.path.isfile(p) or __import__('stat').S_ISSOCK(os.stat(p).st_mode)):\n"), ("t20zo_la_khong_phai_tep_thuong_do",)),
    ("la_khong_theo_symlink", _ma("            elif not os.path.isfile(p):\n", "            elif not os.path.islink(p) and not os.path.isfile(p):\n"), ("t20zo_la_khong_phai_tep_thuong_do",)),
    # (6) cach goi copytree cua t82 (danh sach cho phep, tren CHINH tep test): noi tu khoa; bo chot doi so vi tri thu ba; bo chot sao
    ("dong_bo_t82_cho_tu_khoa_la", _test('    if set(kw) != {"ignore"}:\n', '    if "symlinks" in kw:\n'), ("t20zj_symlink_treo_khong_duyet_duoc_va_dong_bo_t82",)),
    ("dong_bo_t82_cho_vi_tri_thu_ba", _test("    if len(goi.args) != 2 or any(isinstance(a, ast.Starred) for a in goi.args):\n", "    if any(isinstance(a, ast.Starred) for a in goi.args):\n"), ("t20zj_symlink_treo_khong_duyet_duoc_va_dong_bo_t82",)),
    ("dong_bo_t82_cho_doi_so_sao", _test("    if len(goi.args) != 2 or any(isinstance(a, ast.Starred) for a in goi.args):\n", "    if len(goi.args) != 2:\n"), ("t20zj_symlink_treo_khong_duyet_duoc_va_dong_bo_t82",)),
]
# Lop `kiem-mode-git-chot-khong-rang` (luot 14, dong theo CAU TRUC): moi o cua bang quyet dinh mot dot bien LAT dung o ay — o
# CHAP NHAN thanh TU CHOI, o TU CHOI thanh CHAP NHAN — chen ngay dau vong quyet dinh nen KHONG o nao khac doi. Dich: t20zh.
# Bo sot mot o trong vong lap cua ca, hay ky vong sai mot o, thi dot bien cua o ay SONG.
_NEO_O_BANG = "        for duong, (mode, trang_thai) in sorted(ban_ghi.items()):\n"


def _lat_o(tt, mode):
    than = ('                loi.append("dot bien: o chap nhan bi lat thanh tu choi")\n                continue\n'
            if (tt, mode) in O_CHAP_NHAN else "                continue\n")
    return _ma(_NEO_O_BANG, _NEO_O_BANG + f'            if (trang_thai, mode) == ("{tt}", "{mode}"):\n' + than)


DOT_BIEN += [(f"mode_git_lat_o_{tt}_{mode}", _lat_o(tt, mode), ("t20zh_kiem_mode_git_bang_quyet_dinh_day_du",))
             for tt in TRANG_THAI_BANG for mode in MODE_BANG]


def _bo_nhanh(nhom, tu):
    """Dot bien go MOT nhanh `tu` khoi nhom `(?:a|b|...)` cua `MAU_SO_CHU_KHO` (neo dung tu LUAT: lech thu tu => ha tang)."""
    return _test(nhom, "(?:" + "|".join(x for x in nhom[3:-1].split("|") if x != tu) + ")")


# Lop `bang-do-thieu-neo-va-thieu-kiem-ke` (luot 17): MOI tu-so va MOI danh tu kho cua `MAU_SO_CHU_KHO` mot dot bien go rieng no.
DOT_BIEN += [(f"bo_quet_so_chu_bo_tu_so_{i:02d}", _bo_nhanh("(?:" + "|".join(SO_CHU_LUAT) + ")", tu),
              ("t98b_moi_so_do_trong_docstring_va_chu_thich_phai_co_neo",)) for i, tu in enumerate(SO_CHU_LUAT)]
DOT_BIEN += [(f"bo_quet_so_chu_bo_danh_tu_{i:02d}", _bo_nhanh("(?:" + "|".join(DANH_TU_KHO_LUAT) + ")", tu),
              ("t98b_moi_so_do_trong_docstring_va_chu_thich_phai_co_neo",)) for i, tu in enumerate(DANH_TU_KHO_LUAT)]
TEN_DOT_BIEN = [d[0] for d in DOT_BIEN]


def chay_mot_dot_bien(ten, tep_va_ham, dich, chay=None):
    chay = chay or chay_con
    dich = tuple(dich)   # vat hoa TRUOC lan doc dau: iterator/generator bi vong baseline tieu thu thi `all([])` ra GIET gia
    if not dich:
        return "HONG", "tap ca dich rong: khong co bang chung duong thi khong duoc cap GIET"
    tep, ham = tep_va_ham
    goc = dung_cay_tam({})
    try:
        # điều kiện tiên quyết: ca đích XANH trên bản gốc (không thì lượt giết không quy được cho đột biến)
        for ten_ca in dich:
            rc, ra = chay(ten_ca, goc)
            if rc != 0:
                return "HONG", f"ca dich {ten_ca} khong xanh tren ban goc (rc={rc}): {ra[-300:]}"
        vb = (goc / tep).read_text(encoding="utf-8")
        moi = ham(vb)
        (goc / tep).write_text(moi, encoding="utf-8")
        hang = []
        for ten_ca in dich:
            rc, ra = chay(ten_ca, goc)
            hang.append((ten_ca, phan_hang(rc, ra, ten_ca), ra[-200:].strip().splitlines()[-1:] or [""]))
        if all(h[1] == "GIET" for h in hang):
            return "GIET", ""
        return [h[1] for h in hang if h[1] != "GIET"][0], "; ".join(f"{a}={b} {c}" for a, b, c in hang)
    finally:
        shutil.rmtree(goc, ignore_errors=True)


def chay_tap_dot_bien(tap):
    """(so bi giet, danh sach xau) cho mot tap (ten, tep_va_ham, dich). `dich` co the la iterator: vat hoa MOT LAN o day."""
    giet, xau = 0, []
    muc = []
    for ten, tv, dich in tap:
        dich = tuple(dich)
        for d in dich:
            if d not in CA:
                xau.append(f"{ten}: ca dich {d!r} khong ton tai")
        muc.append((ten, tv, dich))

    def mot(m):
        try:
            return chay_mot_dot_bien(m[0], m[1], m[2])
        except Exception as e:
            return "HONG", f"{type(e).__name__}: {e}"
    # Moi dot bien dung cay tam RIENG + tien trinh con RIENG => song song an toan; ket qua doc theo THU TU khai bao.
    with concurrent.futures.ThreadPoolExecutor(max_workers=max(1, min(4, os.cpu_count() or 1))) as pool:
        kq = list(pool.map(mot, muc))
    for (ten, _, _), (hang, chi_tiet) in zip(muc, kq):
        if hang == "GIET":
            giet += 1
        else:
            xau.append(f"{ten}: {hang} {chi_tiet}")
    return giet, xau


MAU_RC = ((3, "DO:t01:vi sao", "t01", "GIET"), (3, "DO:t02:vi sao", "t01", "TIN_DUNG_GIA"),
          (4, "Traceback", "t01", "TIN_DUNG_GIA"), (0, "", "t01", "SONG_SOT"), (-9, "", "t01", "HONG"))
TU_KIEM_DOT_BIEN = [
    ("sinh_ngoai_le_vo_can_KeyError",
     (MA, lambda vb: thay_mot(vb, "def phan_loai_tu_diff(doi):\n", "def phan_loai_tu_diff(doi):\n    raise KeyError('vo can')\n")),
     ("t01_toan_ho_so_duong_nhanh",), "TIN_DUNG_GIA"),
    ("tuong_duong_chi_them_chu_thich",
     (MA, lambda vb: thay_mot(vb, "TOI_DA_TEN_IN = 5\n", "TOI_DA_TEN_IN = 5  # vo hai\n")),
     ("t01_toan_ho_so_duong_nhanh",), "SONG_SOT"),
    ("dot_bien_that_de_doi_chieu",
     (MA, lambda vb: thay_mot(vb, '"ops/reviews/", "ops/specs/")\nMAU_SHA', '"ops/reviews/", "ops/specs/", "scripts/")\nMAU_SHA')),
     ("t02_co_tep_ma_day_du",), "GIET"),
]


def tu_kiem_phan_hang():
    """Bo phan hang tu kiem: cac mau rc (`MAU_RC`) va cac dot bien that (`TU_KIEM_DOT_BIEN`); so luong doc tu hai hang so."""
    loi = []
    for rc, ra, ten, mong in MAU_RC:
        thuc = phan_hang(rc, ra, ten)
        if thuc != mong:
            loi.append(f"phan_hang({rc}, {ra!r}, {ten!r}) = {thuc}, mong {mong}")
    for ten, tv, dich, mong in TU_KIEM_DOT_BIEN:
        hang, chi_tiet = chay_mot_dot_bien(ten, tv, dich)
        if hang != mong:
            loi.append(f"tu kiem {ten}: mong {mong}, duoc {hang} {chi_tiet}")
    return loi


def loi_cay_duoi_do(cay, goc):
    """Luot 5 (lop chot-yaml, cua 'test co MAT nhung do CAY KHAC'): lan chay DAY DU (buoc CI) chi duoc do chinh kho chua tep
    test. `CI_DUONG_NHANH_CAY` chi danh cho tien trinh con `--mot-ca` cua mot dot bien; dat no cho lan chay day du (vd qua
    `GITHUB_ENV` o mot buoc truoc) la tro bo test sang cay gia ma van in TONG: DAT."""
    if Path(cay).resolve() != Path(goc).resolve():
        return f"CAY DUOI DO KHAC KHO CHUA TEST: {cay} != {goc} — lan chay day du khong nhan CI_DUONG_NHANH_CAY"
    return ""


def main(argv):
    if len(argv) == 4 and argv[0] == "--nguon-test":
        # Chay CA tu BAN SAO (co the bi dot bien) cua chinh tep test; `__file__` giu la tep that de HERE/ROOT_THAT khong doi.
        g = {"__name__": "cdn_test_dot_bien", "__file__": str(HERE / "ci_duong_nhanh_test.py")}
        exec(compile(Path(argv[1]).read_text(encoding="utf-8"), str(HERE / "ci_duong_nhanh_test.py"), "exec"), g)
        return g["main"](argv[2:])
    if len(argv) == 2 and argv[0] == "--mot-ca":
        if argv[1] not in CA:
            print(f"khong co ca {argv[1]!r}", file=sys.stderr)
            return 2
        try:
            CA[argv[1]]()
        except TinHieuChotCa as e:
            print(f"DO:{argv[1]}:{e}")
            return 3
        except Exception as e:
            import traceback
            traceback.print_exc()
            print(f"HONG:{argv[1]}:{type(e).__name__}: {e}")
            return 4
        return 0
    if argv:
        print("dung: ci_duong_nhanh_test.py [--mot-ca TEN]", file=sys.stderr)
        return 2
    loi_cay = loi_cay_duoi_do(CAY, ROOT_THAT)
    if loi_cay:
        print(loi_cay, file=sys.stderr)
        return 2
    dat = do = hong = 0
    for ten in CA:
        kq, ly_do = chay_ca_trong_tien_trinh(ten)
        if kq == "DAT":
            dat += 1
        else:
            do += kq == "DO"
            hong += kq == "HONG"
            print(f"[{kq}] {ten}: {ly_do}")
    print(f"CA: {dat}/{len(CA)} dat · {do} do · {hong} hong")

    giet, xau = chay_tap_dot_bien(DOT_BIEN)
    trung = len(TEN_DOT_BIEN) - len(set(TEN_DOT_BIEN))
    print(f"DOT BIEN: {giet}/{len(DOT_BIEN)} bi giet dung ly do")
    print(dong_kiem_ke())
    for x in xau:
        print(f"[DOT BIEN KHONG BI GIET DUNG] {x}")
    loi_tu_kiem = tu_kiem_phan_hang()
    print(f"TU KIEM PHAN HANG: {'DAT' if not loi_tu_kiem else 'DO'} ({len(MAU_RC)} mau rc, {len(TU_KIEM_DOT_BIEN)} dot bien that)")
    for x in loi_tu_kiem:
        print(f"[TU KIEM] {x}")
    ok = (dat == len(CA) > 0 and giet == len(DOT_BIEN) > 0 and not xau and not loi_tu_kiem and trung == 0)
    print(f"TONG: {'DAT' if ok else 'DO'}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
