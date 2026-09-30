#!/usr/bin/env python3
"""Phản chứng cho `ops/ci_duong_nhanh.py` và cho các `if:` đường nhanh trong `.github/workflows/ci.yml`.

Packet #674 `CI-DUONG-NHANH-HO-SO` (đặc tả r2). Bốn tầng, mỗi tầng có ĐỘT BIẾN riêng chạy trên BẢN SAO TẠM. Danh sách và
số lượng ca/đột biến KHÔNG ghi ở đây (đã trôi hai lượt liền): nguồn duy nhất là `CA`, `DOT_BIEN` và dòng `CA:`/`DOT BIEN:` in ra.
  · ca `t*`: hành vi bộ phân loại và bước kiểm rẻ (đồ giả cho ca thuần + KHO GIT THẬT cho ca cần ngữ nghĩa git);
  · ca `y*`: cấu trúc `ci.yml`. ĐÂY LÀ CỔNG DUY NHẤT canh `if:` cấp job của `gate-ops` và `if:` cấp bước sau G5. Nợ có tên
    `ci-if-cap-job-gate-ops-va-buoc-sau-g5-khong-co-cong-canh` (Q6-i chủ kho): `JOB_G5` của `ci_dang_ky_test.py` chỉ có
    `gate`, `gate-registry`, `gate-packet-loop`, và `cong_cu_test.t6` chỉ soi các bước TRƯỚC G5;
  · ca `k*`: nối vào sổ test sống (mục `DA_NOI` và lời gọi thật trong `run:`);
  · ca khai `@ca_tu_kiem`: tự kiểm của chính bộ test (harness, phân hoạch, docstring, cây dưới đo). Nhóm KHAI tại chỗ,
    không suy từ tiền tố; `t96` đối chiếu với dấu hiệu AST độc lập, và dòng `KIEM KE:` in số từng nhóm.

CÁCH ĐO ĐỘT BIẾN — bài học CLAUDE.md "đột biến bị giết không phải bị giết ĐÚNG LÝ DO":
  · Ca đích chỉ báo ĐỎ bằng `TinHieuChotCa` (con của AssertionError) do CHÍNH `bang()` ném. Lỗi vô can trong mã
    bị đột biến (TypeError, KeyError, ...) đi ra dưới TÊN THẬT ⇒ tiến trình con thoát rc=4 ⇒ `TIN_DUNG_GIA`, không
    tính là giết. Ca KHÔNG được có `except Exception: raise TinHieuChotCa` (ca t99 quét AST canh điều đó).
  · Mỗi đột biến: neo `count == 1` (không thì lỗi hạ tầng), kiểm bản đột biến KHÁC bản gốc, chạy trên tệp tạm với
    tên riêng, bytecode tắt; ca đích còn phải XANH trên bản gốc (chứng minh lượt giết là do đột biến).
  · Đột biến cũng áp cho CHÍNH tệp test (`--nguon-test`): helper fixture (cô lập actor...) có đột biến riêng.
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
import os
import re
import shutil
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


def _tra_gia(gia_tri):
    """Mot gia tri do gia: ngoai le => nem; (rc, out) => dung nhu vay; bytes => rc 0 neu khac rong, rc 1 neu rong."""
    if isinstance(gia_tri, BaseException):
        raise gia_tri
    if isinstance(gia_tri, tuple):
        return KQ(*gia_tri)
    return KQ(0 if gia_tri else 1, gia_tri or b"")


def chay_gia(out=b"", rc=0, nem=None, log=None, merge_base=(GOC_A + "\n").encode(),
             merge_tree=(CAY_GIA + "\n").encode(), diff_cay=(0, b"")):
    """Do gia git. `merge-base --all`, `merge-tree` va `diff goc -> cay merge` co gia tri RIENG, doc lap voi `out`/`rc`/`nem`
    cua ba cham (mac dinh: MOT base, merge sach, merge khong doi them gi) — de moi chot cua ba cham van co rang rieng
    thay vi bi chot cua `doc_diff_merge` che."""
    def chay(argv, **kw):
        if log is not None:
            log.append(list(argv))
        if list(argv[:3]) == ["git", "merge-base", "--all"]:
            return _tra_gia(merge_base)
        if list(argv[:3]) == ["git", "merge-tree", "--write-tree"]:
            return _tra_gia(merge_tree)
        if list(argv[:4]) == ["git", "diff", "--no-renames", "--name-only"]:
            return _tra_gia(diff_cay)
        if nem is not None:
            raise nem
        return KQ(rc, out)
    return chay


def env_pr(su_kien="pull_request", goc=GOC_A, dau=GOC_B, **them):
    e = {"CI_DUONG_NHANH_SU_KIEN": su_kien, "CI_DUONG_NHANH_GOC": goc, "CI_DUONG_NHANH_DAU": dau}
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
             GIT_AUTHOR_NAME="t", GIT_AUTHOR_EMAIL="t@e.x", GIT_COMMITTER_NAME="t", GIT_COMMITTER_EMAIL="t@e.x")
    return e


def git(kho, *doi, kiem=True):
    r = subprocess.run(["git", "-c", "commit.gpgsign=false", "-c", "core.autocrlf=false", *doi],
                       cwd=kho, capture_output=True, env=_env_git())
    if kiem and r.returncode:
        raise RuntimeError(f"ha tang: git {' '.join(doi)} rc={r.returncode}: {r.stderr.decode('utf-8', 'replace')[:300]}")
    return r


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


def phan_loai_that(m, kho, goc, dau):
    return m.phan_loai(env_pr(goc=goc, dau=dau), chay_that, kho)


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
    # (b) doi ten THU MUC phia goc: ort mac dinh (`merge.directoryRenames=conflict`) bao XUNG DOT (rc=1) — GitHub khong
    # dung merge ref cho PR xung dot, nen day khong phai duong lot; van phai la day_du (git THAT, khong do gia).
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
        if list(argv[:3]) == ["git", "merge-base", "--all"]:
            return KQ(0, (GOC_A + "\n").encode())
        if list(argv[:3]) == ["git", "merge-tree", "--write-tree"]:
            return KQ(0, (CAY_GIA + "\n").encode())
        if list(argv[:4]) == ["git", "diff", "--no-renames", "--name-only"]:
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
    rc = m.lenh_kiem_re(env_pr(goc=goc, dau=dau), chay_that_bo_ca_du_lieu, kho, bo_dem, bay_gio)
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
        bang(rc == 0, f"khoang trang cuoi dong / dong trong cuoi tep khong duoc chan oan (do 8/63 lan merge): rc={rc}: {log}")


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
        bang(rc == 1 and "symlink" in log and "treo.md" in log, f"symlink ho so phai DO kiem-re: rc={rc}: {log}")


@ca
def t20p_kiem_re_gitattributes_trong_ho_so_khong_cau_hinh_duoc_diff_check():
    """Cross-review luot 8 (`kiem-re-bi-cau-hinh-boi-du-lieu-ho-so`): `.gitattributes` do PR mang vao (moi do sau) voi
    `conflict-marker-size` tat bao dau xung dot cua `diff --check` doc thuoc tinh tu cay lam viec. Chot: `--attr-source`
    = cay GOC. Doi chung: KHONG chan `.gitattributes` — master co ba tep `-whitespace` duoi `ops/reviews/` do PR ho so them."""
    m = nap_module()
    xung_dot = "a\n<<<<<<< HEAD\nb\n=======\nc\n>>>>>>> nhanh\n"
    for thu_muc in ("ops/land", "ops/reviews/a/b/c"):
        pr = {f"{thu_muc}/.gitattributes": "* conflict-marker-size=40\n", f"{thu_muc}/x.md": xung_dot}
        with kho_that(nhanh_pr=pr) as (kho, goc, dau):
            tho = git(kho, "-c", "core.whitespace=-blank-at-eol,-blank-at-eof,-space-before-tab",
                      "diff", "--check", f"{goc}...{dau}", kiem=False)
            bang(tho.returncode == 0, f"fixture vo hieu ({thu_muc}): thuoc tinh cua PR phai TAT duoc `--check` doc cay lam viec")
            rc, log = kiem_re(m, kho, goc, dau)
            bang(rc == 1 and "diff --check" in log and f"{thu_muc}/x.md" in log,
                 f"{thu_muc}: dau xung dot phai DO du PR mang .gitattributes: rc={rc}: {log}")
    pr = {"ops/reviews/r/.gitattributes": "luot*-VERDICT.md -whitespace\n",
          "ops/reviews/r/luot1-VERDICT.md": "verdict chep nguyen byte   \n\tdong\n\n"}
    with kho_that(nhanh_pr=pr) as (kho, goc, dau):
        rc, log = kiem_re(m, kho, goc, dau)
        bang(rc == 0, f"doi chung: PR ho so them .gitattributes `-whitespace` (quy uoc cua master) phai DAT: rc={rc}: {log}")


@ca
def t20s_kiem_re_tep_nhi_phan_la_khong_do_duoc():
    """Luot 9 (lop `kiem-re-cua-fail-close-chua-co-ca`, pham vi `diff --check`): git coi tep co NUL la nhi phan va
    `--check` BO QUA no — dau xung dot trong do lot. Master: 0 tep nhi phan duoi allowlist ⇒ nhi phan = DO."""
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
def t20q_kiem_re_symlink_hop_le_moi_duoi_do():
    """Cross-review luot 8: docstring khai chan MOI symlink "treo hay khong"; t20n chi co symlink TREO duoi `.md`."""
    m = nap_module()
    for ten, duong in (("hop le .md", "ops/reviews/hop-le.md"), ("hop le .yaml", "ops/land/l.yaml")):
        with kho_that(nhanh_pr={"ops/specs/S.md": "# s\n"}) as (kho, goc, dau):
            (kho / duong).parent.mkdir(parents=True, exist_ok=True)
            (kho / duong).symlink_to("../../README.md")
            bang((kho / duong).exists(), f"fixture vo hieu: {duong} phai la symlink HOP LE")
            git(kho, "add", "-A")
            git(kho, "commit", "-q", "-m", "symlink")
            dau2 = git(kho, "rev-parse", "HEAD").stdout.decode().strip()
            rc, log = kiem_re(m, kho, goc, dau2)
            bang(rc == 1 and "symlink" in log, f"{ten}: symlink phai DO kiem-re: rc={rc}: {log}")


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
    """Cau truc PyYAML doc KHAC GitHub: khoa trung (PyYAML lay ban CUOI, im lang) hoac khoa gop `<<`."""


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
    """Luot 5 (lop chot-yaml, cua 'bo phan tich cua test khac GitHub'): moi ca `y*` doc qua loader NGHIEM nay."""
    try:
        return yaml.load(van_ban, Loader=_LoaderNghiem)
    except YamlKhacGitHub as e:
        bang(False, f"ci.yml: {e} — ca `y*` se do mot cau truc KHAC cai GitHub chay")


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
         and env.get("CI_DUONG_NHANH_DAU") == "${{ github.event.pull_request.head.sha }}", f"env buoc phan loai sai: {env}")
    bang(b.get("continue-on-error") is True,
         "buoc phan loai phai co `continue-on-error: true`: chuan-bi do => ba job bat buoc `skipped` (GitHub tinh la dat)")
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


@ca
def y04_tap_buoc_mang_if_che_do_khop_dung():
    wf = doc_wf()
    for job, cau_hinh in wf["jobs"].items():
        bang("che_do" not in str(cau_hinh.get("if", "")) and "che_do" not in str(cau_hinh.get("strategy", "")),
             f"{job}: `che_do` khong duoc xuat hien o `if:`/strategy cap JOB (bo ca job = check VANG MAT)")
        thay = set()
        for b in cau_hinh.get("steps") or []:
            if "che_do" in str(b.get("if", "")):
                nd = chuan_hoa_if(b["if"])
                if " != 'duong_nhanh'" in nd:
                    thay.add(ten_buoc(b))
                    bang(BO_QUA.get(job, {}).get(ten_buoc(b)) == nd, f"{job}/{ten_buoc(b)}: dang `if:` khong thuoc danh sach cho phep: {nd!r}")
                else:
                    bang(nd == NHANH, f"{job}/{ten_buoc(b)}: dang `if:` theo che_do khong thuoc danh sach cho phep: {nd!r}")
            bang("che_do" not in str(b.get("env", "")) and "che_do" not in str(b.get("with", "")),
                 f"{job}/{ten_buoc(b)}: che_do khong duoc chay vao env/with cua buoc")
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
         and env.get("CI_DUONG_NHANH_SU_KIEN") == "${{ github.event_name }}", f"env buoc kiem re sai: {env}")


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
    'gate-ops': {
        'DUONG_NHANH - liet ke buoc bo qua (job gate-ops)': "needs.chuan-bi.outputs.che_do == 'duong_nhanh'",
        'DUONG_NHANH - kiem re thay cho buoc bi bo (doctrine-scan, YAML, diff --check, lease check)': "needs.chuan-bi.outputs.che_do == 'duong_nhanh'",
        'ci-duong-nhanh selftest (phan loai diff + khoa cau truc if)': "runner.os == 'Linux'",
        'lease-publish selftest (đo lại setup sau G5)': "needs.chuan-bi.outputs.che_do != 'duong_nhanh'",
        'don-nhanh selftest (chốt xoá nhánh)': "runner.os != 'Windows'",
        'bo ca gate chay TRONG cgroup duoc uy quyen (Linux)': "runner.os == 'Linux' && needs.chuan-bi.outputs.che_do != 'duong_nhanh'",
        'gate lifecycle selftest (nen khong co cgroup)': "runner.os != 'Linux' && needs.chuan-bi.outputs.che_do != 'duong_nhanh'",
    },
    'gate-registry': {
    },
    'gate-packet-loop': {
        'DUONG_NHANH - liet ke buoc bo qua (job gate-packet-loop)': "needs.chuan-bi.outputs.che_do == 'duong_nhanh'",
        'packet-loop selftest': "needs.chuan-bi.outputs.che_do != 'duong_nhanh'",
    },
}


# LUAT (khoa topology): moi thu KHAC thân `run:` cua ci.yml. `run:` cua buoc co san ngoai pham vi packet nay (do cong khac + review canh);
# `run:` cua buoc do packet them thi duoc khoa nguyen van o y08/y09. Doi bat ky muc nao duoi day => y13 do => cap nhat CUNG review.
KHUNG_TOP = {'name': 'gate', True: {'push': {'branches': ['master']}, 'pull_request': None, 'workflow_dispatch': None}, 'concurrency': {'group': '${{ github.workflow }}-${{ github.event.pull_request.number || github.ref }}', 'cancel-in-progress': "${{ github.ref != 'refs/heads/master' }}"}}
KHUNG_JOB = {
    'chuan-bi': {'runs-on': 'ubuntu-latest', 'timeout-minutes': 20, 'outputs': {'os': '${{ (github.event_name == \'workflow_dispatch\' || contains(github.event.pull_request.labels.*.name, \'windows\')) && \'["ubuntu-latest","windows-latest"]\' || \'["ubuntu-latest"]\' }}', 'che_do': "${{ github.event_name == 'pull_request' && steps.phan-loai.outputs.che_do || 'day_du' }}"}},
    'gate': {'needs': 'chuan-bi', 'strategy': {'fail-fast': False, 'matrix': {'os': '${{ fromJson(needs.chuan-bi.outputs.os) }}'}}, 'runs-on': '${{ matrix.os }}', 'timeout-minutes': 60, 'env': {'PYTHONIOENCODING': 'utf-8', 'PYTHONUTF8': '1', 'PYTHONDONTWRITEBYTECODE': '1'}},
    'gate-ops': {'needs': 'chuan-bi', 'strategy': {'fail-fast': False, 'matrix': {'os': '${{ fromJson(needs.chuan-bi.outputs.os) }}'}}, 'runs-on': '${{ matrix.os }}', 'timeout-minutes': 60, 'env': {'PYTHONIOENCODING': 'utf-8', 'PYTHONUTF8': '1', 'PYTHONDONTWRITEBYTECODE': '1'}},
    'gate-registry': {'needs': 'chuan-bi', 'strategy': {'fail-fast': False, 'matrix': {'os': '${{ fromJson(needs.chuan-bi.outputs.os) }}'}}, 'runs-on': '${{ matrix.os }}', 'timeout-minutes': 90, 'env': {'PYTHONIOENCODING': 'utf-8', 'PYTHONUTF8': '1', 'PYTHONDONTWRITEBYTECODE': '1'}},
    'gate-packet-loop': {'needs': 'chuan-bi', 'strategy': {'fail-fast': False, 'matrix': {'os': '${{ fromJson(needs.chuan-bi.outputs.os) }}'}}, 'runs-on': '${{ matrix.os }}', 'timeout-minutes': 60, 'env': {'PYTHONIOENCODING': 'utf-8', 'PYTHONUTF8': '1', 'PYTHONDONTWRITEBYTECODE': '1'}},
}
KHUNG_BUOC = {
    'chuan-bi': [
        ('actions/checkout@v4', {'uses': 'actions/checkout@v4', 'if': "${{ github.event_name == 'pull_request' }}", 'continue-on-error': True, 'timeout-minutes': 10, 'with': {'fetch-depth': 0}}),
        ('phan loai diff (duong nhanh ho so - chi pull_request)', {'id': 'phan-loai', 'if': "${{ github.event_name == 'pull_request' }}", 'continue-on-error': True, 'timeout-minutes': 5, 'env': {'CI_DUONG_NHANH_SU_KIEN': '${{ github.event_name }}', 'CI_DUONG_NHANH_GOC': '${{ github.event.pull_request.base.sha }}', 'CI_DUONG_NHANH_DAU': '${{ github.event.pull_request.head.sha }}'}}),
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
        ('G5 kiem ban ke cong cu + T1..T8 (packet', {'shell': 'bash'}),
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
    'gate-ops': [
        ('Force LF checkout (hash parity với manifest)', {}),
        ('actions/checkout@v4', {'uses': 'actions/checkout@v4', 'with': {'fetch-depth': 0}}),
        ('actions/setup-python@v5', {'uses': 'actions/setup-python@v5', 'with': {'python-version': '3.12'}}),
        ('cài PyYAML + jsonschema (cổng đăng lease + validator verdict cần)', {}),
        ('cài shellcheck cho G5 (cài xong đo lại)', {'shell': 'bash'}),
        ('cài rg cho G5 (cài xong đo lại)', {'shell': 'bash'}),
        ('DUONG_NHANH - liet ke buoc bo qua (job gate-ops)', {'if': "${{ needs.chuan-bi.outputs.che_do == 'duong_nhanh' }}"}),
        ('DUONG_NHANH - kiem re thay cho buoc bi bo (doctrine-scan, YAML, diff --check, lease check)', {'if': "${{ needs.chuan-bi.outputs.che_do == 'duong_nhanh' }}", 'shell': 'bash', 'env': {'CI_DUONG_NHANH_SU_KIEN': '${{ github.event_name }}', 'CI_DUONG_NHANH_GOC': '${{ github.event.pull_request.base.sha }}', 'CI_DUONG_NHANH_DAU': '${{ github.event.pull_request.head.sha }}'}}),
        ('ci-duong-nhanh selftest (phan loai diff + khoa cau truc if)', {'if': "runner.os == 'Linux'"}),
        ('bien-nhan v2 selftest', {}),
        ('lease-publish selftest (đo lại setup sau G5)', {'if': "${{ needs.chuan-bi.outputs.che_do != 'duong_nhanh' }}", 'shell': 'bash', 'env': {'AL_VER': '1.7.7'}}),
        ('don-nhanh selftest (chốt xoá nhánh)', {'if': "runner.os != 'Windows'", 'shell': 'pwsh'}),
        ('bo ca gate chay TRONG cgroup duoc uy quyen (Linux)', {'if': "${{ runner.os == 'Linux' && needs.chuan-bi.outputs.che_do != 'duong_nhanh' }}"}),
        ('gate lifecycle selftest (nen khong co cgroup)', {'if': "${{ runner.os != 'Linux' && needs.chuan-bi.outputs.che_do != 'duong_nhanh' }}"}),
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
        ('test registry (phạm vi + các bộ chưa được nối)', {'env': {'CI_DANG_KY_WORKERS': '2', 'CI_DANG_KY_SU_KIEN': '${{ github.event_name }}', 'CI_DANG_KY_GOC': '${{ github.event.pull_request.base.sha || github.event.before }}', 'CI_DANG_KY_DAU': '${{ github.event.pull_request.head.sha || github.sha }}'}}),
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


JOB_CO_IF_CHO_PHEP = frozenset()   # sau khi #668 land: them `gate-cong-cu-gop` (if: !cancelled()) qua review


@ca
def y11_khong_job_nao_co_if_cap_job_ngoai_danh_sach_cho_phep():
    """Cross-review luot 3 (P2): y06 chi nhin ba job bat buoc + chuan-bi; job phu khac (gate-registry...) cung khong duoc bi bo
    hoac sua ket qua bang `if:` cap job. Quet MOI job; danh sach cho phep hien la RONG."""
    for job, cau in doc_wf()["jobs"].items():
        bang(not ("if" in cau and job not in JOB_CO_IF_CHO_PHEP), f"{job}: `if:` cap job khong duoc phep, duoc {cau.get('if')!r}")


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
# `skipped`. Than `run:` cua buoc CO SAN ngoai pham vi packet (bien gioi khai o y13).
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
    ban cuoi) trong khi cai GitHub doc KHAC. Loader nghiem phai do ca hai dang tren chinh van ban ci.yml, va ban that phai sach."""
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
    tran cap job phai lon hon tong hai tran buoc (khong thi job het gio TRUOC buoc, tuc do thay vi roi `day_du`)."""
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
    """Luot 6 (lop chot-yaml, tang 'duong goi that' tiep theo — executor tu liet ke): CI chi doc MA THOAT cua tien trinh.
    (1) `main` phai tra 1 + `TONG: DO` khi BAT KY dieu kien nao hong (ca do, dot bien khong giet, xau, tu kiem, ten trung),
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
    """Lop bang-do (P3 luot 4, va luot 5 tu do): phan nhom theo TIEN TO da tu lech hai lan (38/12/3; roi t96 — mot ca tu kiem —
    bi dem la "hanh vi"). Nay nhom `tu_kiem` KHAI tai cho (`@ca_tu_kiem`) va duoc doi chieu voi DAU HIEU AST DOC LAP: ca nao
    cham noi tang cua chinh bo test (`CA`, `DOT_BIEN`, phan hang, docstring, tep test) la tu kiem, va nguoc lai. Dong `KIEM KE:`
    in ra (neo cua moi bang so) phai khop so dem doc lap."""
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
    """Bang giao/docstring troi so HAI luot lien (P3 luot 1 va 2): so ca, so dot bien va khoang `tNN..tMM` chi nguon
    duy nhat la `CA`/`DOT_BIEN`. Docstring cua module va cua `ops/ci_duong_nhanh.py` khong duoc ghim chung."""
    mau = re.compile(r"\b\d+\s*/\s*\d+\s*(?:ca|dot bien|đột biến)|`?t\d\d`?\s*(?:\.\.|–|-)\s*`?t\d\d"
                     r"|\b(?:\d+|NĂM|BA|BỐN|SÁU|BẢY|TÁM|năm|ba|bốn|sáu|bảy|tám)\s+(?:mẫu rc|đột biến (?:thật|thực))")
    ma_sp = ast.get_docstring(ast.parse((CAY / "ops" / "ci_duong_nhanh.py").read_text(encoding="utf-8"))) or ""
    for ten, doc in (("ci_duong_nhanh_test.py (module dang chay)", globals().get("__doc__") or ""), ("ci_duong_nhanh.py", ma_sp)):
        thay = mau.findall(doc)
        bang(not thay, f"{ten}: docstring ghim so ca/khoang ten (se troi): {thay}")


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
    for dp in ("ops/ci_duong_nhanh.py", "ops/ci_duong_nhanh_test.py", ".claude/dev/ci_dang_ky_test.py"):
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


def _test(cu, moi):
    return (TEST, lambda vb: thay_mot(vb, cu, moi))


def _ma(cu, moi):
    return (MA, lambda vb: thay_mot(vb, cu, moi))


def _yml(cu, moi):
    return (YML, lambda vb: thay_mot(vb, cu, moi))


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
    # ---- tầng YAML (đặc tả nghiệm thu 6, 7)
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
    # ---- chu kho 5889513175: tran thoi gian cua chuan-bi
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
    ("merge_that_bo_hop", _ma("    return ba_cham | khi_merge\n", "    return ba_cham\n"), ("t11c_goc_doi_ten_ho_so_ra_vung_ma_day_du",)),
    ("merge_tree_bo_kiem_rc", _ma('    if getattr(mt, "returncode", None) != 0 or not isinstance(ra_mt,', '    if not isinstance(ra_mt,'), ("t11c_goc_doi_ten_ho_so_ra_vung_ma_day_du",)),
    ("merge_tree_bo_kiem_dang", _ma('            or not re.fullmatch(rb"[0-9a-f]{40}\\n", bytes(ra_mt)):', "            or False:"), ("t11c_goc_doi_ten_ho_so_ra_vung_ma_day_du",)),
    ("merge_tree_nem_thanh_rong", _ma("    except Exception:\n        return None\n    ra_mt", "    except Exception:\n        return set()\n    ra_mt"), ("t11c_goc_doi_ten_ho_so_ra_vung_ma_day_du",)),
    ("diff_cay_bo_kiem_rc", _ma('    if getattr(dt, "returncode", None) != 0 or not isinstance(ra_dt,', '    if not isinstance(ra_dt,'), ("t11c_goc_doi_ten_ho_so_ra_vung_ma_day_du",)),
    ("diff_cay_nem_thanh_rong", _ma("    except Exception:\n        return None\n    ra_dt", "    except Exception:\n        return set()\n    ra_dt"), ("t11c_goc_doi_ten_ho_so_ra_vung_ma_day_du",)),
    ("diff_cay_bo_kiem_cut", _ma('    if ra_dt and not bytes(ra_dt).endswith(b"\\0"):\n        return None\n', ""), ("t11c_goc_doi_ten_ho_so_ra_vung_ma_day_du",)),
    # ---- luot 9: lop kiem-re-bi-cau-hinh-boi-du-lieu-ho-so — thuoc tinh doc tu cay GOC; va phan chung: khong chan .gitattributes
    ("diff_check_bo_attr_source", _ma('"--attr-source=" + goc, ', ""), ("t20p_kiem_re_gitattributes_trong_ho_so_khong_cau_hinh_duoc_diff_check",)),
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
]
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
