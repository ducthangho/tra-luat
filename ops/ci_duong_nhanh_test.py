#!/usr/bin/env python3
"""Phản chứng cho `ops/ci_duong_nhanh.py` và cho các `if:` đường nhanh trong `.github/workflows/ci.yml`.

Packet #674 `CI-DUONG-NHANH-HO-SO` (đặc tả r2). Ba tầng, mỗi tầng có ĐỘT BIẾN riêng chạy trên BẢN SAO TẠM:
  1. Hành vi bộ phân loại và bước kiểm rẻ (các ca `t01`..`t21`, gồm nhánh a-g): đồ giả cho ca thuần + KHO GIT THẬT
     cho ca cần ngữ nghĩa git (ba chấm, đổi tên, tên tệp có dấu, thiếu object, dấu xung đột, lease, ca dữ liệu).
  2. Cấu trúc `ci.yml` (các ca `y01`..`y09`): ĐÂY LÀ CỔNG DUY NHẤT canh `if:` cấp job của `gate-ops` và `if:` cấp bước
     sau G5. Nợ có tên `ci-if-cap-job-gate-ops-va-buoc-sau-g5-khong-co-cong-canh` (Q6-i chủ kho): `JOB_G5` của
     `ci_dang_ky_test.py` chỉ có `gate`, `gate-registry`, `gate-packet-loop`, và `cong_cu_test.t6` chỉ soi các bước
     TRƯỚC G5 — nên KHÔNG có cổng máy nào khác đối chiếu độc lập các `if:` mà packet này thêm.
  3. Nối vào sổ test sống (các ca `k01`, `k02`, `k03`): mục `DA_NOI`, vị trí tệp và lời gọi thật trong `run:`.

CÁCH ĐO ĐỘT BIẾN — bài học CLAUDE.md "đột biến bị giết không phải bị giết ĐÚNG LÝ DO":
  · Ca đích chỉ báo ĐỎ bằng `TinHieuChotCa` (con của AssertionError) do CHÍNH `bang()` ném. Lỗi vô can trong mã
    bị đột biến (TypeError, KeyError, ...) đi ra dưới TÊN THẬT ⇒ tiến trình con thoát rc=4 ⇒ `TIN_DUNG_GIA`, không
    tính là giết. Ca KHÔNG được có `except Exception: raise TinHieuChotCa` (ca t99 quét AST canh điều đó).
  · Mỗi đột biến: neo `count == 1` (không thì lỗi hạ tầng), kiểm bản đột biến KHÁC bản gốc, chạy trên tệp tạm với
    tên riêng, bytecode tắt; ca đích còn phải XANH trên bản gốc (chứng minh lượt giết là do đột biến).
  · Phân hạng có phần tự kiểm (`tu_kiem_phan_hang`): NĂM mẫu rc (rc=3 đúng tên ⇒ GIẾT; rc=3 sai tên ⇒ TÍN DỤNG GIẢ;
    rc=4 ⇒ TÍN DỤNG GIẢ; rc=0 ⇒ SỐNG SÓT; rc=-9 ⇒ HỎNG) và BA đột biến thật (KeyError vô can ⇒ TÍN DỤNG GIẢ;
    chỉ thêm chú thích ⇒ SỐNG SÓT; nới allowlist ⇒ GIẾT). "Sai tên ca" chỉ được kiểm bằng mẫu rc, chưa có đột biến thật.

Ra: `CA: N/N dat` · `DOT BIEN: M/M bi giet` · `TONG: DAT`. Thoát 0 chỉ khi N>0, mọi ca đạt, M>0, mọi đột biến bị giết
ĐÚNG LÝ DO, mọi ca tự kiểm đạt — `rc=0` một mình không phải bằng chứng.
"""
from __future__ import annotations

import ast
import contextlib
import importlib.util
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

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
DONG_GOI_TEST = "python ops/ci_duong_nhanh_test.py"


class TinHieuChotCa(AssertionError):
    """Chỉ `bang()` ném lớp này. Mã triển khai và lỗi vô can KHÔNG ném được nó ⇒ phân biệt được giết thật/giả."""


class SuDoGia(Exception):
    """Ngoại lệ do CHÍNH ca dựng để đồ giả ném ra; ca chỉ bắt đúng lớp này (không bắt Exception trần)."""


def bang(dieu_kien, thong_diep):
    if not dieu_kien:
        raise TinHieuChotCa(thong_diep)


CA: dict = {}


def ca(f):
    CA[f.__name__] = f
    return f


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


def chay_gia(out=b"", rc=0, nem=None, log=None):
    def chay(argv, **kw):
        if log is not None:
            log.append(list(argv))
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
    e = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
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
def t12_doi_ten_ra_khoi_vung_ma_day_du():
    m = nap_module()
    noi = "def f():\n    return 1\n" * 20
    with kho_that(nen={"scripts/tl.py": noi}, nhanh_pr={"ops/land/tl.py": ("scripts/tl.py",)}) as (kho, goc, dau):
        co_rename = git(kho, "diff", "--name-only", "-z", f"{goc}...{dau}").stdout.decode().split("\0")
        bang("scripts/tl.py" not in co_rename,
             f"fixture vo hieu: phat hien doi ten phai giau duong dan cu, duoc {co_rename}")
        che_do, ly_do = phan_loai_that(m, kho, goc, dau)
        bang(che_do == "day_du", f"doi ten scripts/tl.py -> ops/land/ phai la day_du, duoc {che_do!r}: {ly_do}")


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
            lp.kiem(lp._doc_yaml(str(tep)), str(tep), str(ROOT_THAT), bo_qua_han=True)
            lp.kiem(lp._doc_yaml(str(tep)), str(tep), str(ROOT_THAT))
        except lp.Chan as e:
            if "het han" in str(e) or "hết hạn" in str(e):
                return vb
        except Exception:
            continue
    raise RuntimeError("ha tang: khong tim thay lease that het han hop le de lam fixture")
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
          "ops/leases/thua-dong.yaml": lease_that_het_han_hop_le() + "\n"}
    with kho_that(nhanh_pr=pr, sao_lease_publish=True) as (kho, goc, dau):
        tho = git(kho, "diff", "--check", f"{goc}...{dau}", kiem=False)
        bang(tho.returncode != 0, "fixture vo hieu: `git diff --check` nguyen ban phai bat cac tep nay")
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
def t22_ca_du_lieu_thay_bo_lease_publish_selftest():
    """Bo `lease-publish selftest` lam mat t23/t26/t27 (doc CAY that). kiem-re giu ba ca do; chay that tren kho that."""
    m = nap_module()
    bang(tuple(m.CA_DU_LIEU) == ("t23_MOI_lease_THAT_trong_kho_phai_QUA",
                                 "t26_moi_bien_nhan_review_phai_khop_BAM_tep_no_tro_toi",
                                 "t27_canh_bao_trong_bien_nhan_phai_duoc_NANG_len_muc_luc"), f"danh sach ca du lieu sai: {m.CA_DU_LIEU}")
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


# ---------------------------------------------------------------- tầng 2: cấu trúc ci.yml
def doc_wf():
    return yaml.safe_load((CAY / ".github" / "workflows" / "ci.yml").read_text(encoding="utf-8"))


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
    for job in BAT_BUOC:
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
    bang(b.get("continue-on-error") is not True, "buoc goi test khong duoc co continue-on-error")


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


# ---------------------------------------------------------------- tự kiểm của chính bộ test
@ca
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
    r = subprocess.run([sys.executable, "-B", str(HERE / "ci_duong_nhanh_test.py"), "--mot-ca", ten_ca],
                       capture_output=True, env=env, timeout=thoi_han)
    return r.returncode, (r.stdout + r.stderr).decode("utf-8", "replace")


def dung_cay_tam(thay):
    """Bản sao TỐI THIỂU của cây: chỉ những tệp mà các ca đọc. `thay` = {đường dẫn: văn bản mới}."""
    goc = Path(tempfile.mkdtemp(prefix="cdn_cay_"))
    for dp in ("ops/ci_duong_nhanh.py", ".claude/dev/ci_dang_ky_test.py"):
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
    ("kiem_re_bo_diff_check", _ma("kiem_diff_check(env, chay, kho) + kiem_lease(", "[] + kiem_lease("), ("t20c_kiem_re_dau_xung_dot_do",)),
    ("kiem_re_bo_lease", _ma("+ kiem_lease(doi, kho, chay, bay_gio, ra)", "+ []"), ("t20e_kiem_re_lease_con_han_loi_do",)),
    ("diff_check_bo_tinh_chinh_whitespace", _ma('["git", "-c", CAU_HINH_WHITESPACE, "diff", "--check"', '["git", "diff", "--check"'), ("t20d_kiem_re_khoang_trang_cuoi_dong_khong_do",)),
    ("diff_check_bo_check", _ma('"diff", "--check", "--no-renames"', '"diff", "--no-renames"'), ("t20c_kiem_re_dau_xung_dot_do",)),
    ("lease_het_han_coi_nhu_con_han", _ma("        het_han = han is not None and han <= bay_gio\n", "        het_han = False\n"), ("t21_kiem_lease_phan_biet_con_han_het_han_va_duoi_tep",)),
    ("lease_het_han_duoc_mien_kiem", _ma("        if het_han:\n            print(", "        if het_han:\n            continue\n            print("), ("t20f_kiem_re_lease_het_han_sai_schema_van_do",)),
    ("lease_bo_duoi_yml", _ma('x.startswith("ops/leases/") and x.endswith((".yaml", ".yml"))', 'x.startswith("ops/leases/") and x.endswith(".yaml")'), ("t20g_kiem_re_lease_duoi_yml_van_duoc_kiem",)),
    ("kiem_re_bo_ca_du_lieu", _ma("\n           + kiem_ca_du_lieu(kho, chay))", ")"), ("t20a_kiem_re_ho_so_sach_dat",)),
    ("ca_du_lieu_bo_t27", _ma(',\n              "t27_canh_bao_trong_bien_nhan_phai_duoc_NANG_len_muc_luc")', ")"), ("t22_ca_du_lieu_thay_bo_lease_publish_selftest",)),
    ("ca_du_lieu_bo_qua_rc", _ma("    if getattr(r, \"returncode\", None) != 0:\n        cuoi = _dau_ra(r).strip().splitlines()[-3:]", "    if False:\n        cuoi = _dau_ra(r).strip().splitlines()[-3:]"), ("t22_ca_du_lieu_thay_bo_lease_publish_selftest",)),
    ("lease_han_hong_coi_la_het_han", _ma('        except ValueError:\n            return None\n        return han if', '        except ValueError:\n            return datetime(1970, 1, 1, tzinfo=timezone.utc)\n        return han if'), ("t21_kiem_lease_phan_biet_con_han_het_han_va_duoi_tep",)),
    ("lease_check_rc_khong_kiem", _ma('        if getattr(r, "returncode", None) != 0:\n            cuoi', '        if False:\n            cuoi'), ("t21_kiem_lease_phan_biet_con_han_het_han_va_duoi_tep",)),
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
    # ---- nghiệm thu 9: nối vào sổ test sống
    ("yml_go_buoc_goi_test_khoi_ci", _yml("      - name: ci-duong-nhanh selftest (phan loai diff + khoa cau truc if)\n        if: runner.os == 'Linux'\n        run: python ops/ci_duong_nhanh_test.py\n", ""), ("y09_buoc_goi_test_cua_packet_khong_bi_bo", "k03_ci_goi_that_muc_da_noi")),
    ("dk_go_muc_da_noi", (DK, lambda vb: thay_mot(vb, f'    "{DA_NOI_MUC}",\n', "")), ("k01_so_dang_ky_nhan_muc_da_noi",)),
    ("dk_go_muc_da_noi_kiem_dem_so", (DK, lambda vb: thay_mot(vb, f'    "{DA_NOI_MUC}",\n', "")), ("k02_da_noi_dung_mot_lan_va_test_song_khop_tep",)),
]
TEN_DOT_BIEN = [d[0] for d in DOT_BIEN]


def chay_mot_dot_bien(ten, tep_va_ham, dich):
    tep, ham = tep_va_ham
    goc = dung_cay_tam({})
    try:
        # điều kiện tiên quyết: ca đích XANH trên bản gốc (không thì lượt giết không quy được cho đột biến)
        for ten_ca in dich:
            rc, ra = chay_con(ten_ca, goc)
            if rc != 0:
                return "HONG", f"ca dich {ten_ca} khong xanh tren ban goc (rc={rc}): {ra[-300:]}"
        vb = (goc / tep).read_text(encoding="utf-8")
        moi = ham(vb)
        (goc / tep).write_text(moi, encoding="utf-8")
        hang = []
        for ten_ca in dich:
            rc, ra = chay_con(ten_ca, goc)
            hang.append((ten_ca, phan_hang(rc, ra, ten_ca), ra[-200:].strip().splitlines()[-1:] or [""]))
        if all(h[1] == "GIET" for h in hang):
            return "GIET", ""
        return [h[1] for h in hang if h[1] != "GIET"][0], "; ".join(f"{a}={b} {c}" for a, b, c in hang)
    finally:
        shutil.rmtree(goc, ignore_errors=True)


def tu_kiem_phan_hang():
    """Năm mẫu rc cho bộ phân hạng, cộng ba đột biến thật: lỗi vô can · chỉ thêm chú thích (sống sót) · nới allowlist (giết)."""
    loi = []
    for rc, ra, ten, mong in ((3, "DO:t01:vi sao", "t01", "GIET"), (3, "DO:t02:vi sao", "t01", "TIN_DUNG_GIA"),
                              (4, "Traceback", "t01", "TIN_DUNG_GIA"), (0, "", "t01", "SONG_SOT"), (-9, "", "t01", "HONG")):
        thuc = phan_hang(rc, ra, ten)
        if thuc != mong:
            loi.append(f"phan_hang({rc}, {ra!r}, {ten!r}) = {thuc}, mong {mong}")
    kiem = [
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
    for ten, tv, dich, mong in kiem:
        hang, chi_tiet = chay_mot_dot_bien(ten, tv, dich)
        if hang != mong:
            loi.append(f"tu kiem {ten}: mong {mong}, duoc {hang} {chi_tiet}")
    return loi


def main(argv):
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

    giet, xau = 0, []
    for ten, tv, dich in DOT_BIEN:
        for d in dich:
            if d not in CA:
                xau.append(f"{ten}: ca dich {d!r} khong ton tai")
        try:
            hang, chi_tiet = chay_mot_dot_bien(ten, tv, dich)
        except Exception as e:
            hang, chi_tiet = "HONG", f"{type(e).__name__}: {e}"
        if hang == "GIET":
            giet += 1
        else:
            xau.append(f"{ten}: {hang} {chi_tiet}")
    trung = len(TEN_DOT_BIEN) - len(set(TEN_DOT_BIEN))
    print(f"DOT BIEN: {giet}/{len(DOT_BIEN)} bi giet dung ly do")
    for x in xau:
        print(f"[DOT BIEN KHONG BI GIET DUNG] {x}")
    loi_tu_kiem = tu_kiem_phan_hang()
    print(f"TU KIEM PHAN HANG: {'DAT' if not loi_tu_kiem else 'DO'}")
    for x in loi_tu_kiem:
        print(f"[TU KIEM] {x}")
    ok = (dat == len(CA) > 0 and giet == len(DOT_BIEN) > 0 and not xau and not loi_tu_kiem and trung == 0)
    print(f"TONG: {'DAT' if ok else 'DO'}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
