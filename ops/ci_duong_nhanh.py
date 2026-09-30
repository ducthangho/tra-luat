#!/usr/bin/env python3
"""ci_duong_nhanh — phân loại PR theo DIFF để `ci.yml` chọn đường nhanh cho PR chỉ đổi hồ sơ.

Packet #674 `CI-DUONG-NHANH-HO-SO` (đặc tả r2, ops/specs/CI-DUONG-NHANH-HO-SO-r2.md).

VÌ SAO CÓ TỆP NÀY, VÀ VÌ SAO LOGIC KHÔNG NẰM TRONG YAML
Ruleset `bao-ve-cong-dang-lease` đòi ba check (`gate`, `gate-ops`, `gate-packet-loop`) xanh trên ĐÚNG head,
nên PR bookkeeping chỉ thêm `ops/land/*.yaml` vẫn phải chạy trọn gate (đo 29-09-2026: run 36518707072,
job `gate (ubuntu-latest)` 52 phút). Không được dùng `paths:` / `paths-ignore:` — workflow không chạy thì
check VẮNG MẶT, PR kẹt `blocked`, và "vắng mặt" nhìn giống hệt "xanh". Nên ba job vẫn KHỞI ĐỘNG và báo
kết quả; chỉ các bước nặng có `if:` mức bước theo output `che_do` của job `chuan-bi`. Quyết định `che_do`
sống ở ĐÂY (Python, có phản chứng chạy được — ops/ci_duong_nhanh_test.py), không sống trong biểu thức YAML.

BA TRẠNG THÁI, FAIL-CLOSE (danh sách CHO PHÉP, không phải danh sách CẤM)
  · đo được diff VÀ mọi tệp đổi khớp `ALLOWLIST_TIEN_TO`  ⇒ `duong_nhanh`
  · đo được diff VÀ có ít nhất một tệp ngoài allowlist     ⇒ `day_du`
  · KHÔNG ĐO ĐƯỢC (không phải pull_request, thiếu/hỏng SHA, git lỗi/ném, đầu ra cụt) ⇒ `day_du`
Chỉ MỘT giá trị (`duong_nhanh`) mở đường bỏ bước; mọi giá trị lạ, rỗng hay vắng đều thành đầy đủ ở phía
`ci.yml` (`!= 'duong_nhanh'`). Diff rỗng ⇒ `duong_nhanh` (Q3 chủ kho), có dòng log riêng để phân biệt.

Diff là `base...head` (BA chấm = từ merge-base tới head), KHÔNG phải `base..head`: hai chấm tính cả việc
nhánh đích đã tiến thêm sau khi PR rẽ ra, biến PR hồ sơ thành "có tệp mã" (đo ở test t11). `--no-renames`
để đổi tên KHỎI vùng cũng tính là chạm tệp cũ; nếu không, `git mv scripts/tl.py ops/land/tl.py` chỉ hiện
đường dẫn ĐÍCH và PR mã lọt vào đường nhanh (test t12). `-z` để tên tệp có dấu/xuống dòng không bị git
bọc dấu nháy.

GIỚI HẠN, NÓI THẲNG (không phải ranh giới an ninh):
  · Bộ phân loại chạy từ CÂY MERGE của PR và `ci.yml` cũng do PR mang theo. PR sửa CHÍNH tệp này hoặc
    `ci.yml` tự quyết đường của mình; chốt cho việc đó là review (`sensitive`), không phải mã. Allowlist
    chặn NHẦM LẪN, không chặn tác giả cố ý.
  · Allowlist theo TIỀN TỐ, không theo phần mở rộng: một `.py` đặt dưới `ops/land/**` vẫn là đường nhanh
    (Q2 chủ kho giữ đúng bốn tiền tố).
  · `pull_request.base.sha`/`head.sha` luôn là 40 hex ở mọi sự kiện con: theo tài liệu GitHub, chưa tự đo.

LỆNH `kiem-re` (bước bù cho các bước bị bỏ, chỉ chạy khi `che_do == duong_nhanh`):
  YAML parse được · `git diff --check` · lease đổi phải qua `lease_publish` · ba ca kiểm DỮ LIỆU của lease_publish_test.
Hai chỗ khác chữ trần của đặc tả r2, ĐO ngày 29-09-2026. CHỦ KHO ĐÃ DUYỆT CẢ HAI (lựa chọn (a)) — erratum của đặc tả r2,
không sửa r2: https://github.com/ducthangho/tra-luat/issues/674#issuecomment-5887720007 . Với reviewer: đây là HÀNH VI ĐƯỢC
DUYỆT, không phải finding về chính sách; vẫn tìm lỗi TRONG cách hiện thực (ví dụ `bo_qua_han` bỏ thêm chốt nào khác không,
ba loại khoảng trắng có bị tắt rộng hơn ba loại đó không).
  · D1 — `git diff --check` chạy với `core.whitespace=-blank-at-eol,-blank-at-eof,-space-before-tab`. Trong 345
    lần merge gần nhất (first-parent, 400 lần gần nhất tính từ 1741e0a), 63 lần chỉ đổi hồ sơ và 8/63 trượt
    `--check` nguyên bản (dấu cách cuối dòng trong verdict `.md`/`.patch`, dòng trống cuối tệp yaml). Chốt cứng
    sẽ chặn oan ~13% đúng lớp PR mà đường nhanh sinh ra để giải. Bản tinh chỉnh vẫn bắt dấu xung đột còn sót
    (`<<<<<<<`, `=======`, `>>>>>>>`), thứ `--check` báo bất kể cấu hình.
  · D2 — `lease_publish.py check` là cổng ĐĂNG lease: lease đã hết hạn thì nó trả rc=8 "hết hạn" theo thiết kế,
    mà bookkeeping thu hồi/đóng lease thường đúng là sửa lease hết hạn. Lease CÒN HẠN đổi trong PR chạy đúng
    `check`; lease HẾT HẠN chạy `kiem(bo_qua_han=True)` — mọi chốt như `check`, chỉ bỏ chốt hạn — nên KHÔNG
    được miễn kiểm chỉ vì hết hạn. Cả hai đuôi `.yaml` và `.yml`. Giới hạn: bia mộ hai chiều của `kiem`
    đọc các lease khác trong CÂY; checkout của Actions chỉ có cây PR, không có các nhánh `ops/**`. Trên một
    clone chỉ-master 6/113 tệp lease trượt `kiem(bo_qua_han=True)`, còn trên bản sao đủ 552 ref thì 0/113
    (đo bởi reviewer lượt 1): số 6 là số CỦA PHẠM VI clone-một-nhánh, không phải của kho.
    Hệ quả CÓ CHỦ ĐÍCH về actor (chủ kho chọn khai, không đổi chốt — Issue #674, 2026-09-30): `kiem`/`check`
    giữ chốt thẩm quyền theo `GITHUB_ACTOR`, nên PR hồ sơ chạm `ops/leases/` do bot (actor khác chủ kho) đẩy
    sẽ ĐỎ ở đường nhanh (`CHAN [4]`) trong khi đường đầy đủ không chạy chốt này. Đỏ ở đây là fail-close đúng
    hướng; muốn đường nhanh cho PR lease do bot đẩy thì phải là quyết định mới về thẩm quyền, không phải nới tại chỗ.
"""
from __future__ import annotations

import os
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DAY_DU, DUONG_NHANH = "day_du", "duong_nhanh"
BIEN_SU_KIEN, BIEN_GOC, BIEN_DAU = "CI_DUONG_NHANH_SU_KIEN", "CI_DUONG_NHANH_GOC", "CI_DUONG_NHANH_DAU"
ALLOWLIST_TIEN_TO = ("ops/land/", "ops/leases/", "ops/reviews/", "ops/specs/")
MAU_SHA = re.compile(r"[0-9a-f]{40}")
CAU_HINH_WHITESPACE = "core.whitespace=-blank-at-eol,-blank-at-eof,-space-before-tab"
TOI_DA_TEN_IN = 5
CA_DU_LIEU = ("t23_MOI_lease_THAT_trong_kho_phai_QUA", "t26_moi_bien_nhan_review_phai_khop_BAM_tep_no_tro_toi",
              "t27_canh_bao_trong_bien_nhan_phai_duoc_NANG_len_muc_luc")
MA_KIEM_HET_HAN = (
    "import sys\nsys.path.insert(0, 'ops')\nimport lease_publish as lp\n"
    "try:\n    lp.kiem(lp._doc_yaml(sys.argv[1]), sys.argv[1], '.', bo_qua_han=True)\n"
    "except lp.Chan as e:\n    print('CHAN [%s]: %s' % (e.ma, e.thong_diep))\n    raise SystemExit(8)\n")
MA_CHAY_CA = (
    "import runpy, sys\nm = runpy.run_path(sys.argv[1])\n"
    "for ten in sys.argv[2:]:\n    m[ten]()\n    print('DAT', ten)\n")


def _ep_utf8():
    for luong in (sys.stdout, sys.stderr):
        if hasattr(luong, "reconfigure"):
            luong.reconfigure(encoding="utf-8", errors="backslashreplace")


def _duong_dan_sach(duong: str) -> bool:
    """Đường dẫn repo-relative dạng chuẩn: khác rỗng, không `/` đầu, không `\\`, không ký tự điều khiển
    (chặn giả dòng log), không thành phần rỗng / `.` / `..`. Git không sinh `..` trong cây, nhưng bộ phân
    loại không được dựa vào điều đó: khớp tiền tố trần cho `ops/land/../../scripts/tl.py` là fail-OPEN."""
    if not duong or duong.startswith("/") or "\\" in duong:
        return False
    if any(ord(c) < 32 or ord(c) == 127 for c in duong):
        return False
    return all(t not in ("", ".", "..") for t in duong.split("/"))


def khop_allowlist(duong: str) -> bool:
    return _duong_dan_sach(duong) and duong.startswith(ALLOWLIST_TIEN_TO)


def doc_diff(env=os.environ, chay=subprocess.run, kho=ROOT):
    """Tập đường dẫn đổi trong `base...head`, hoặc None = KHÔNG ĐO ĐƯỢC (⇒ đầy đủ).
    Ba trạng thái: tập khác rỗng · tập rỗng · None. Không gọi git khi sự kiện không phải pull_request."""
    su_kien, goc, dau = (env.get(k) or "" for k in (BIEN_SU_KIEN, BIEN_GOC, BIEN_DAU))
    if su_kien != "pull_request":
        return None
    if not all(MAU_SHA.fullmatch(x) and x.strip("0") for x in (goc, dau)):
        return None
    try:
        r = chay(["git", "diff", "--name-only", "--no-renames", "-z", f"{goc}...{dau}"],
                 cwd=kho, capture_output=True)
    except Exception:
        return None
    if getattr(r, "returncode", None) != 0:
        return None
    ra = getattr(r, "stdout", None)
    if not isinstance(ra, (bytes, bytearray)):
        return None
    # `-z` kết thúc MỖI mục bằng NUL; đầu ra khác rỗng mà không kết thúc bằng NUL là bị cắt cụt giữa chừng.
    if ra and not bytes(ra).endswith(b"\0"):
        return None
    return {x for x in bytes(ra).decode("utf-8", "surrogateescape").split("\0") if x}


def phan_loai_tu_diff(doi):
    if doi is None:
        return DAY_DU, "DUONG_NHANH: KHONG DO DUOC diff (thieu SHA hop le, git loi hoac dau ra cut) - fail-close ve DAY_DU"
    if not doi:
        return DUONG_NHANH, "DUONG_NHANH: diff RONG (khong tep nao doi) - coi la khop allowlist rong (Q3), dung duong nhanh"
    ngoai = sorted(x for x in doi if not khop_allowlist(x))
    if ngoai:
        ten = ", ".join(repr(x) for x in ngoai[:TOI_DA_TEN_IN])
        them = f" (+{len(ngoai) - TOI_DA_TEN_IN} tep nua)" if len(ngoai) > TOI_DA_TEN_IN else ""
        return DAY_DU, f"DUONG_NHANH: DAY_DU vi diff co {len(ngoai)} tep ngoai allowlist: {ten}{them}"
    return DUONG_NHANH, (f"DUONG_NHANH: toan bo {len(doi)} tep doi khop allowlist "
                         "ops/{land,leases,reviews,specs}/** - dung duong nhanh")


def phan_loai(env=os.environ, chay=subprocess.run, kho=ROOT):
    """(che_do, ly_do). Sự kiện không phải pull_request ⇒ `day_du` mà KHÔNG gọi git."""
    su_kien = env.get(BIEN_SU_KIEN) or ""
    if su_kien != "pull_request":
        return DAY_DU, f"DUONG_NHANH: khong phan loai - su_kien={su_kien!r} khong phai pull_request, luon DAY_DU"
    return phan_loai_tu_diff(doc_diff(env, chay, kho))


def _dau_ra(r) -> str:
    """stdout rồi stderr của một tiến trình con, đã giải mã; đối tượng lạ ⇒ chuỗi rỗng (không ném)."""
    ra = b""
    for ten in ("stdout", "stderr"):
        gia_tri = getattr(r, ten, None)
        if isinstance(gia_tri, (bytes, bytearray)):
            ra += bytes(gia_tri)
    return ra.decode("utf-8", "replace")


def kiem_yaml(doi, kho=ROOT) -> list[str]:
    """Mọi tệp .yaml/.yml đổi (còn trong cây) phải parse được. Thiếu PyYAML ⇒ ĐỎ, không phải 'bỏ qua'."""
    try:
        import yaml
    except ImportError:
        return ["KHONG DO DUOC: thieu PyYAML - khong parse duoc YAML nen khong cho qua"]
    loi = []
    for duong in sorted(x for x in doi if x.endswith((".yaml", ".yml"))):
        tep = Path(kho) / duong
        if not tep.is_file():
            continue
        try:
            with tep.open(encoding="utf-8") as f:
                list(yaml.safe_load_all(f))
        except Exception as e:
            loi.append(f"YAML khong parse duoc: {duong!r}: {type(e).__name__}: {str(e).splitlines()[0] if str(e) else ''}")
    return loi


def kiem_loai_tep(doi, kho=ROOT) -> list[str]:
    """Mọi tệp hồ sơ đổi (còn trong cây) phải là tệp THƯỜNG, không phải symlink. Bước bị bỏ `lease-publish selftest`
    có `t82` `copytree` CẢ cây (kể cả ops/{land,leases,reviews,specs}/**): symlink treo dưới allowlist làm nó ĐỎ trên
    master trong khi mọi kiểm khác của `kiem-re` vẫn DAT. Hồ sơ không cần symlink ⇒ chặn mọi symlink, treo hay không."""
    return [f"tep ho so la symlink (duong nhanh chi nhan tep thuong): {duong!r}"
            for duong in sorted(doi) if (Path(kho) / duong).is_symlink()]


def kiem_diff_check(env=os.environ, chay=subprocess.run, kho=ROOT) -> list[str]:
    goc, dau = env.get(BIEN_GOC) or "", env.get(BIEN_DAU) or ""
    try:
        r = chay(["git", "-c", CAU_HINH_WHITESPACE, "diff", "--check", "--no-renames", f"{goc}...{dau}"],
                 cwd=kho, capture_output=True)
    except Exception as e:
        return [f"KHONG DO DUOC: git diff --check nem {type(e).__name__}"]
    if getattr(r, "returncode", None) == 0:
        return []
    dong = _dau_ra(r).splitlines()[:3]
    return [f"git diff --check rc={getattr(r, 'returncode', None)}: " + " | ".join(dong)]


def _han_lease(gia_tri):
    """datetime UTC, hoặc None nếu không đọc được (⇒ coi là CÒN HẠN và để `check` phán)."""
    if isinstance(gia_tri, datetime):
        return gia_tri if gia_tri.tzinfo else gia_tri.replace(tzinfo=timezone.utc)
    if isinstance(gia_tri, str):
        try:
            han = datetime.fromisoformat(gia_tri.strip().replace("Z", "+00:00"))
        except ValueError:
            return None
        return han if han.tzinfo else han.replace(tzinfo=timezone.utc)
    return None


def kiem_lease(doi, kho=ROOT, chay=subprocess.run, bay_gio=None, ra=None) -> list[str]:
    """Lease CÒN HẠN (hoặc hạn không đọc được) qua `lease_publish.py check`; lease HẾT HẠN qua `kiem(bo_qua_han=True)` — vẫn kiểm mọi
    chốt khác, chỉ bỏ chốt hạn. Cả `.yaml` và `.yml`. D2 (quyết định của chủ kho) còn mở: xem docstring module."""
    ra = ra if ra is not None else sys.stdout
    try:
        import yaml
    except ImportError:
        return ["KHONG DO DUOC: thieu PyYAML - khong doc duoc lease"]
    bay_gio = bay_gio or datetime.now(timezone.utc)
    loi = []
    for duong in sorted(x for x in doi if x.startswith("ops/leases/") and x.endswith((".yaml", ".yml"))):
        tep = Path(kho) / duong
        if not tep.is_file():
            continue
        try:
            with tep.open(encoding="utf-8") as f:
                lease = yaml.safe_load(f)
        except Exception as e:
            loi.append(f"lease khong parse duoc: {duong!r}: {type(e).__name__}")
            continue
        if not isinstance(lease, dict):
            loi.append(f"lease khong phai mapping: {duong!r}")
            continue
        han = _han_lease(lease.get("lease_expires_at_utc"))
        het_han = han is not None and han <= bay_gio
        if het_han:
            print(f"DUONG_NHANH: lease {duong!r} da het han - chay kiem(bo_qua_han=True): moi chot nhu `check`, "
                  "chi bo chot han", file=ra)
            lenh = [sys.executable, "-B", "-c", MA_KIEM_HET_HAN, duong]
        else:
            lenh = [sys.executable, "ops/lease_publish.py", "check", duong, "--root", "."]
        try:
            r = chay(lenh, cwd=kho, capture_output=True)
        except Exception as e:
            loi.append(f"KHONG DO DUOC: kiem lease nem {type(e).__name__} cho {duong!r}")
            continue
        if getattr(r, "returncode", None) != 0:
            cuoi = _dau_ra(r).strip().splitlines()[-1:]
            loi.append(f"kiem lease {'(het han) ' if het_han else ''}rc={getattr(r, 'returncode', None)} "
                       f"cho {duong!r}: {' '.join(cuoi)}")
    return loi


def kiem_ca_du_lieu(kho=ROOT, chay=subprocess.run) -> list[str]:
    """Ba ca kiem DU LIEU that cua bo lease-publish (t23 neo prompt cua moi lease · t26 bam bien nhan review · t27
    muc luc `ops/reviews`) thay cho ca bo `lease-publish selftest`: ba ca nay doc CAY that nen la thu ma PR ho so
    co the lam hong; bo ca suite di la mat chung. Chay nguyen ca trong tep test that, ~6 giay."""
    try:
        r = chay([sys.executable, "-B", "-c", MA_CHAY_CA, "ops/lease_publish_test.py", *CA_DU_LIEU],
                 cwd=kho, capture_output=True)
    except Exception as e:
        return [f"KHONG DO DUOC: chay ca du lieu nem {type(e).__name__}"]
    if getattr(r, "returncode", None) != 0:
        cuoi = _dau_ra(r).strip().splitlines()[-3:]
        return [f"ca du lieu cua lease_publish_test rc={getattr(r, 'returncode', None)}: " + " | ".join(cuoi)]
    return []


def lenh_kiem_re(env=os.environ, chay=subprocess.run, kho=ROOT, ra=None, bay_gio=None) -> int:
    ra = ra if ra is not None else sys.stdout
    doi = doc_diff(env, chay, kho)
    che_do, ly_do = phan_loai_tu_diff(doi)
    print(ly_do, file=ra)
    if che_do != DUONG_NHANH:
        print("DUONG_NHANH: kiem-re CHI chay khi diff toan ho so; phan loai lai khong ra DUONG_NHANH - DO "
              "(khong khop voi job chuan-bi)", file=ra)
        return 1
    loi = (kiem_yaml(doi, kho) + kiem_loai_tep(doi, kho) + kiem_diff_check(env, chay, kho) + kiem_lease(doi, kho, chay, bay_gio, ra)
           + kiem_ca_du_lieu(kho, chay))
    for x in loi:
        print("DUONG_NHANH: LOI - " + x, file=ra)
    print(f"DUONG_NHANH: kiem-re {'DO' if loi else 'DAT'} ({len(doi)} tep doi, {len(loi)} loi)", file=ra)
    return 1 if loi else 0


def main(argv=None, env=os.environ, chay=subprocess.run, kho=ROOT, ra=None) -> int:
    ra = ra if ra is not None else sys.stdout
    argv = sys.argv[1:] if argv is None else list(argv)
    if argv == ["kiem-re"]:
        return lenh_kiem_re(env, chay, kho, ra)
    if argv:
        print("dung: ci_duong_nhanh.py [kiem-re]", file=sys.stderr)
        return 2
    try:
        che_do, ly_do = phan_loai(env, chay, kho)
    except Exception as e:
        # Lỗi nội bộ KHÔNG được làm PR kẹt đỏ oan, cũng không được mở đường nhanh: fail-close ⇒ đầy đủ.
        che_do, ly_do = DAY_DU, f"DUONG_NHANH: LOI NOI BO ({type(e).__name__}) - fail-close ve DAY_DU"
    print(ly_do, file=ra)
    print(f"che_do={che_do}", file=ra)
    tep_ra = env.get("GITHUB_OUTPUT")
    if tep_ra:
        try:
            with open(tep_ra, "a", encoding="utf-8", newline="\n") as f:
                f.write(f"che_do={che_do}\n")
        except OSError as e:
            print(f"DUONG_NHANH: khong ghi duoc GITHUB_OUTPUT ({type(e).__name__}) - DO", file=sys.stderr)
            return 1
    return 0


if __name__ == "__main__":
    _ep_utf8()
    raise SystemExit(main())
