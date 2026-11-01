#!/usr/bin/env python3
"""ci_duong_nhanh — phân loại PR theo DIFF để `ci.yml` chọn đường nhanh cho PR chỉ đổi hồ sơ.

Packet #674 `CI-DUONG-NHANH-HO-SO` (đặc tả r2, ops/specs/CI-DUONG-NHANH-HO-SO-r2.md).

VÌ SAO CÓ TỆP NÀY, VÀ VÌ SAO LOGIC KHÔNG NẰM TRONG YAML
Ruleset `bao-ve-cong-dang-lease` đòi ba check (`gate`, `gate-ops`, `gate-packet-loop`) xanh trên ĐÚNG head (theo đặc tả
r2 — cấu hình ruleset thật trên GitHub KHÔNG ĐO ĐƯỢC offline), nên PR bookkeeping chỉ thêm `ops/land/*.yaml` vẫn phải
chạy trọn gate (đo 29-09-2026: run 36518707072, job `gate (ubuntu-latest)` 52 phút). Không được dùng `paths:` /
`paths-ignore:`: workflow không chạy thì check bắt buộc VẮNG MẶT và PR kẹt chờ (hành vi GitHub theo tài liệu, chưa tự đo
trên kho này), mà "vắng mặt" nhìn giống hệt "xanh". Nên ba job vẫn KHỞI ĐỘNG và báo kết quả; chỉ các bước nặng có `if:`
mức bước theo output `che_do` của job `chuan-bi` (`y03`, `y06` khoá). Quyết định `che_do` sống ở ĐÂY (Python, có phản
chứng chạy được — ops/ci_duong_nhanh_test.py), không sống trong biểu thức YAML.

BA TRẠNG THÁI, FAIL-CLOSE (danh sách CHO PHÉP, không phải danh sách CẤM)
  · đo được diff VÀ mọi tệp đổi khớp `ALLOWLIST_TIEN_TO`  ⇒ `duong_nhanh`
  · đo được diff VÀ có ít nhất một tệp ngoài allowlist     ⇒ `day_du`
  · KHÔNG ĐO ĐƯỢC (không phải pull_request, thiếu/hỏng SHA — kể cả `github.sha` —, git lỗi/ném, đầu ra cụt) ⇒ `day_du`
Chỉ MỘT giá trị (`duong_nhanh`) mở đường bỏ bước; mọi giá trị lạ, rỗng hay vắng đều thành đầy đủ ở phía
`ci.yml` (`!= 'duong_nhanh'`; `y02`, `y03` khoá dạng biểu thức, còn output VẮNG đọc thành chuỗi rỗng là ngữ nghĩa biểu
thức GitHub Actions theo tài liệu, chưa tự đo). Diff rỗng ⇒ `duong_nhanh` (Q3 chủ kho), có dòng log riêng để phân biệt.

Diff là `base...head` (BA chấm = từ merge-base tới head), KHÔNG phải `base..head`: hai chấm tính cả việc
nhánh đích đã tiến thêm sau khi PR rẽ ra, biến PR hồ sơ thành "có tệp mã" (đo ở test t11). Ba chấm có (ít nhất)
hai chỗ mù do LỊCH SỬ, đã đo 30-09-2026 và đều đóng theo M4: (1) nhiều merge-base (criss-cross) ⇒ ba chấm dùng MỘT base,
giấu thay đổi mã mà merge thật mang vào ⇒ đòi `merge-base --all` ra ĐÚNG một SHA, không thì KHÔNG ĐO ĐƯỢC;
(2) base ĐỔI TÊN tệp/thư mục hồ sơ ra vùng mã ⇒ merge thật (ort, dò đổi tên) mang sửa đổi của PR sang đường dẫn
MỚI trong vùng mã, ba chấm vẫn chỉ thấy đường dẫn cũ ⇒ phân loại trên HỢP của ba chấm và diff `goc -> cây merge`
(`git merge-tree --write-tree`, cùng thuật toán merge với GitHub — tương đương đó theo tài liệu, chưa tự đo trên
GitHub). Mô phỏng ấy xuất phát từ `pull_request.base.sha` của SỰ KIỆN, còn commit mà các job checkout và test là
`github.sha` (merge ref: không bước `actions/checkout` nào của `ci.yml` khai `ref:` — `y13` khoá `with:` của mọi bước — và
khi ấy checkout lấy `github.sha` theo tài liệu GitHub, chưa tự đo trên runner) — hai thứ trùng nhau hay không là KHÔNG ĐO
ĐƯỢC offline. Nên hợp thêm diff `goc -> github.sha` (cross-review lượt 9): base.sha cũ hơn đầu nhánh đích mà nhánh đích
đã đổi tên hồ sơ ra vùng mã thì merge THẬT sửa mã ⇒ `day_du`. Thiếu/hỏng `github.sha` hoặc git không đọc được nó ⇒
KHÔNG ĐO ĐƯỢC ⇒ `day_du`. `--no-renames` để đổi tên KHỎI vùng cũng tính là chạm tệp cũ; nếu không,
`git mv scripts/tl.py ops/land/tl.py` chỉ hiện đường dẫn ĐÍCH và PR mã lọt vào đường nhanh (test t12). `-z` để tên tệp
có dấu/xuống dòng không bị git bọc dấu nháy.

GIỚI HẠN, NÓI THẲNG (không phải ranh giới an ninh):
  · Bộ phân loại chạy từ CÂY MERGE của PR và `ci.yml` cũng do PR mang theo (sự kiện `pull_request` chạy workflow của
    merge ref — theo tài liệu GitHub, chưa tự đo). PR sửa CHÍNH tệp này hoặc `ci.yml` tự quyết đường của mình; chốt
    cho việc đó là review (`sensitive`), không phải mã. Allowlist chặn NHẦM LẪN, không chặn tác giả cố ý.
  · Allowlist theo TIỀN TỐ, không theo phần mở rộng: một `.py` đặt dưới `ops/land/**` vẫn là đường nhanh
    (Q2 chủ kho giữ đúng bốn tiền tố).
  · `pull_request.base.sha`/`head.sha` luôn là SHA đầy đủ (khớp `MAU_SHA`) ở mọi sự kiện con: theo tài liệu GitHub,
    chưa tự đo.

LỆNH `kiem-re` (bước bù cho các bước bị bỏ, chỉ chạy khi `che_do == duong_nhanh`):
  YAML parse được · `git diff --check` · lease đổi phải qua `lease_publish` · ba ca kiểm DỮ LIỆU của lease_publish_test ·
  mọi đường dẫn đổi là TỆP THƯỜNG theo MODE TRONG GIT (`kiem_mode_git`: 100644/100755 hoặc xoá; gitlink, symlink ⇒ ĐỎ) ·
  cây ĐĨA chép được như `t82` của bước bị bỏ, kể cả ngoài diff (`kiem_symlink_treo_ca_cay`: duyệt ĐÚNG đường `t82` đi — CẢ
  cây, THEO symlink thư mục; ĐỎ khi có symlink treo, vòng symlink thư mục hay lá không phải tệp thường; bất biến, từng chốt
  và giới hạn ở docstring hàm).
Hai chỗ khác chữ trần của đặc tả r2, ĐO ngày 29-09-2026. CHỦ KHO ĐÃ DUYỆT CẢ HAI (lựa chọn (a)) — erratum của đặc tả r2,
không sửa r2: https://github.com/ducthangho/tra-luat/issues/674#issuecomment-5887720007 . Với reviewer: đây là HÀNH VI ĐƯỢC
DUYỆT, không phải finding về chính sách; vẫn tìm lỗi TRONG cách hiện thực (ví dụ `bo_qua_han` bỏ thêm chốt nào khác không,
ba loại khoảng trắng có bị tắt rộng hơn ba loại đó không).
  · D1 — `git diff --check` chạy với `core.whitespace=-blank-at-eol,-blank-at-eof,-space-before-tab`. Trên TOÀN
    BỘ 345 merge first-parent tính tới 1741e0a (lệnh lấy tối đa 400, không chạm trần — đo lại 01-10-2026: khớp), 63 lần chỉ
    đổi hồ sơ và 8/63 trượt `--check` nguyên bản (dấu cách cuối dòng trong verdict `.md`/`.patch`, dòng trống cuối tệp
    yaml). Chốt cứng sẽ chặn oan ~13% (8/63 tại 1741e0a) đúng lớp PR mà đường nhanh sinh ra để giải. Bản tinh chỉnh
    vẫn bắt dấu xung đột còn sót (`<<<<<<<`, `=======`, `>>>>>>>`): `--check` báo chúng ngoài `core.whitespace` (`t20c`,
    `t20r` đo dưới đúng cấu hình trên). Thuộc tính thì KHÁC: một `.gitattributes` do PR mang vào (ở mọi độ sâu theo tài
    liệu git; `t20p` đo ở nhiều độ sâu) được git đọc từ CÂY LÀM VIỆC và cấu hình được chính các chốt. Đo được:
    `conflict-marker-size` (cross-review lượt 8), `binary`, `-diff` (`t20p`, 01-10-2026) tắt báo dấu xung đột của
    `--check`; `diff` (set) ép tệp có NUL thành "văn bản" cho `--numstat` (cross-review lượt 9, `t20t`); `-diff` trên tệp
    CRLF làm `merge-tree` mất dò đổi tên thư mục, biến merge XUNG ĐỘT thành merge sạch (tự đo khi vá lượt 9, `t11e`).
    Nên MỌI lệnh git chạy bộ máy diff/merge của tệp này đọc thuộc tính từ cây GỐC (`--attr-source=<goc>`; git không
    có cờ này ⇒ lệnh lỗi ⇒ `day_du` / kiem-re ĐỎ, tức fail-close — phiên bản git của runner chưa đo): ba chấm
    `--name-only`, `merge-tree`, diff `goc -> cây` (cây merge-tree và `github.sha`), `--check`, `--numstat`, và
    `merge-tree` + ba `--raw` của `kiem_mode_git`. Các lệnh `--name-only --no-renames` so OID giữa hai cây và không dò
    đổi tên; chúng có đọc thuộc tính hay không là CHƯA ĐO — `--attr-source` ở đó là chốt thống nhất (`t20u` khoá đối số
    từng lời gọi), không phải vá một đường đã đo được.
    `merge-base --all` chỉ đọc đồ thị commit: không cần chốt.
    Ngoài phạm vi của câu này (không phải lệnh git của tệp này): byte trong cây làm việc do `actions/checkout` dựng
    đã chịu thuộc tính của PR (`eol`/`text`/`working-tree-encoding`/`ident`) — `kiem_yaml`/`kiem_loai_tep`/`kiem_lease`
    đọc đúng các byte ấy, cũng là byte mà các bước bị bỏ và checkout của master đọc (chưa đo riêng, kể cả trên runner).
    KHÔNG chặn `.gitattributes`: PR hồ sơ có thêm tệp như thế dưới `ops/reviews/` (`-whitespace` cho verdict chép nguyên
    byte — PR #667 merge 3fee59e, PR #670 merge dcd5fe0). Tệp NHỊ PHÂN (git đoán theo nội dung + thuộc tính GỐC) thì
    `--check` bỏ qua hẳn ⇒ `kiem_nhi_phan` coi là KHÔNG ĐO ĐƯỢC, ĐỎ (tại 3569472cb9: 0/1991 tệp dưới allowlist là nhị phân).
  · D2 — `lease_publish.py check` là cổng ĐĂNG lease: lease đã hết hạn thì nó trả rc=8 "hết hạn" theo thiết kế,
    mà bookkeeping thu hồi/đóng lease có thể chính là sửa một lease đã hết hạn. Lease CÒN HẠN đổi trong PR chạy đúng
    `check`; lease HẾT HẠN chạy `kiem(bo_qua_han=True)` — mọi chốt như `check` không `--du-bao` (đúng lời gọi của
    kiem-re), chỉ bỏ chốt hạn (`t191` của `ops/lease_publish_test.py` đòi đúng một chốt được miễn) — nên KHÔNG được
    miễn kiểm chỉ vì hết hạn. Cả hai đuôi `.yaml` và `.yml`. Giới hạn: bia mộ hai chiều của `kiem` đọc các lease khác
    trên mọi ref dưới `refs/heads` và `refs/remotes` (`_quet_lease_toan_kho` qua `_cac_ref_cuc_bo`: `for-each-ref` rồi
    `ls-tree` từng ref), KHÔNG đọc tag và KHÔNG đọc cây làm việc (`t21b` đo cả bốn vị trí trên `lease_publish` thật).
    Nên số tệp lease trượt là số CỦA PHẠM VI ref, không phải của kho: tại 3569472cb9 (119 tệp lease) một kho chỉ có
    nhánh đang checkout cho 6/119 trượt (cả 6 `CHAN [8]` bia mộ), một bản sao có 529 ref cục bộ cho 0/119 (529 chưa đối
    chiếu `ls-remote`, nên không khẳng định là đủ). Trên CI, job `gate-ops` checkout TOÀN BỘ lịch sử (`fetch-depth`
    không giới hạn); nó có nạp `refs/remotes/origin/*` của các nhánh `ops/**` hay không là KHÔNG ĐO ĐƯỢC offline — tài
    liệu `actions/checkout` nói chế độ ấy lấy mọi nhánh và tag. Nếu có, bia mộ thấy các nhánh ấy như ở bản sao nhiều
    ref; nếu không, PR hồ sơ sửa một lease hết hạn mà bia mộ chỉ nằm trên nhánh khác sẽ ĐỎ (`CHAN [8]`, fail-close).
    Hệ quả CÓ CHỦ ĐÍCH về actor (chủ kho chọn khai, không đổi chốt — Issue #674, 2026-09-30): `kiem`/`check`
    giữ chốt thẩm quyền theo `GITHUB_ACTOR`, nên PR hồ sơ THÊM/SỬA lease dưới `ops/leases/` do bot (actor khác chủ
    kho) đẩy sẽ ĐỎ ở đường nhanh (`CHAN [4]`; `GITHUB_ACTOR` là tài khoản kích hoạt lượt chạy theo tài liệu GitHub,
    chưa tự đo với bot) trong khi đường đầy đủ không chạy chốt này. XOÁ lease thì KHÔNG đỏ:
    `kiem_lease` bỏ qua tệp đã xoá (không còn gì để kiểm). Đỏ ở đây là fail-close đúng
    hướng; muốn đường nhanh cho PR lease do bot đẩy thì phải là quyết định mới về thẩm quyền, không phải nới tại chỗ.
"""
from __future__ import annotations

import os
import re
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DAY_DU, DUONG_NHANH = "day_du", "duong_nhanh"
BIEN_SU_KIEN, BIEN_GOC, BIEN_DAU = "CI_DUONG_NHANH_SU_KIEN", "CI_DUONG_NHANH_GOC", "CI_DUONG_NHANH_DAU"
BIEN_MERGE = "CI_DUONG_NHANH_MERGE"   # `github.sha`: commit merge cac job checkout va test (theo tai lieu GitHub, xem docstring)
ALLOWLIST_TIEN_TO = ("ops/land/", "ops/leases/", "ops/reviews/", "ops/specs/")
MAU_SHA = re.compile(r"[0-9a-f]{40}")
CAU_HINH_WHITESPACE = "core.whitespace=-blank-at-eol,-blank-at-eof,-space-before-tab"
TOI_DA_TEN_IN = 5
# wp1113 (dac ta CI-LAN-LUU-TRU r1): push master va workflow_dispatch cung duoc phan loai, fail-close.
SU_KIEN_PHAN_LOAI = ("pull_request", "push", "workflow_dispatch")
BIEN_CHE_DO_VAO = "CI_DUONG_NHANH_CHE_DO_VAO"           # input `che_do` cua workflow_dispatch: tu_dong | day_du
BIEN_NHANH_MAC_DINH = "CI_DUONG_NHANH_NHANH_MAC_DINH"   # github.event.repository.default_branch
MAU_TEN_NHANH = re.compile(r"[A-Za-z0-9][A-Za-z0-9._/-]{0,199}")
# Ma CAP NONG: tep dat THANG duoi mot tien to (duong dan chi gom ops/<tien to>/<ten>). `.yaml`/`.yml` KHONG o day: ops/land/*.yaml la ho so land.
DUOI_MA_CAP_NONG = (".py", ".sh", ".bash", ".ps1", ".psm1", ".bat", ".cmd", ".js", ".mjs")
MODE_MOI_VE_DAY_DU = {"100755": "tep thuc thi", "120000": "symlink", "160000": "gitlink"}
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
    (chặn giả dòng log), không thành phần rỗng / `.` / `..`. Dù git có sinh `..` trong cây hay không, bộ phân
    loại không dựa vào điều đó: khớp tiền tố trần cho `ops/land/../../scripts/tl.py` là fail-OPEN."""
    if not duong or duong.startswith("/") or "\\" in duong:
        return False
    if any(ord(c) < 32 or ord(c) == 127 for c in duong):
        return False
    return all(t not in ("", ".", "..") for t in duong.split("/"))


def khop_allowlist(duong: str) -> bool:
    return _duong_dan_sach(duong) and duong.startswith(ALLOWLIST_TIEN_TO)


def doc_diff(env=os.environ, chay=subprocess.run, kho=ROOT):
    """Tập đường dẫn đổi: HỢP của `base...head`, diff `goc -> cây merge-tree` và diff `goc -> github.sha`; hoặc None =
    KHÔNG ĐO ĐƯỢC (⇒ đầy đủ). Ba trạng thái: tập khác rỗng · tập rỗng · None. Không gọi git khi sự kiện không phải
    pull_request hoặc một trong ba SHA (goc, dau, merge ref) vắng/hỏng."""
    su_kien, goc, dau, hop = (env.get(k) or "" for k in (BIEN_SU_KIEN, BIEN_GOC, BIEN_DAU, BIEN_MERGE))
    if su_kien not in SU_KIEN_PHAN_LOAI:
        return None
    if su_kien != "pull_request" and kiem_cap_khong_pr(env, chay, kho) is not None:
        return None
    if not all(MAU_SHA.fullmatch(x) and x.strip("0") for x in (goc, dau)):
        return None
    # merge ref THAT (`github.sha`) la BAT BUOC: vang/hong thi KHONG DO DUOC, khong lui ve mo phong (cross-review luot 9).
    if not (MAU_SHA.fullmatch(hop) and hop.strip("0")):
        return None
    # Ba cham chi dung MOT merge-base. Lich su criss-cross (>1 merge-base) thi `base...head` co the GIAU thay doi
    # ma merge that mang vao base (reviewer luot 8: PR dao scripts/tl.py van ra duong_nhanh) => KHONG DO DUOC.
    try:
        mb = chay(["git", "merge-base", "--all", goc, dau], cwd=kho, capture_output=True)
    except Exception:
        return None
    ra_mb = getattr(mb, "stdout", None)
    if getattr(mb, "returncode", None) != 0 or not isinstance(ra_mb, (bytes, bytearray)) \
            or not re.fullmatch(rb"[0-9a-f]{40}\n", bytes(ra_mb)):
        return None
    try:
        r = chay(["git", "--attr-source=" + goc, "diff", "--name-only", "--no-renames", "-z", f"{goc}...{dau}"],
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
    ba_cham = {x for x in bytes(ra).decode("utf-8", "surrogateescape").split("\0") if x}
    khi_merge = doc_diff_merge(goc, dau, chay, kho)
    if khi_merge is None:
        return None
    # merge-tree mo phong tu base.sha cua SU KIEN; commit GitHub THAT SU test (github.sha) co the dung tren dau nhanh dich
    # MOI hon (base.sha cu) — chua tu do tren GitHub, nen hop them diff goc -> merge ref that. Git khong doc duoc no =>
    # KHONG DO DUOC.
    khi_merge_that = doc_diff_cay(goc, hop, chay, kho)
    if khi_merge_that is None:
        return None
    return ba_cham | khi_merge | khi_merge_that


def doc_diff_merge(goc, dau, chay=subprocess.run, kho=ROOT):
    """Tập đường dẫn mà MERGE THẬT đổi so với `goc`, hoặc None = KHÔNG ĐO ĐƯỢC. Ba chấm chỉ đo phía head; merge còn
    đọc phía base (merge-base -> goc) và phép dò ĐỔI TÊN của nó mang sửa đổi của head sang đường dẫn khác: base đổi tên
    `ops/land/f.md` -> `scripts/f.py` (hoặc cả thư mục) mà PR sửa `ops/land/f.md` thì ba chấm chỉ thấy `ops/land/f.md`
    còn merge thật SỬA `scripts/f.py`. Merge xung đột (rc=1) cũng là None: PR xung đột thì workflow `pull_request` không
    chạy (theo tài liệu GitHub, chưa tự đo)."""
    try:
        # Thuoc tinh tu cay GOC: `-diff` cua PR tren tep CRLF lam merge-tree mat do doi ten thu muc => XUNG DOT thanh merge
        # sach (do 30-09-2026, t11e). Merge driver/conflict-marker-size/renormalize cung la thuoc tinh.
        mt = chay(["git", "--attr-source=" + goc, "merge-tree", "--write-tree", "--no-messages", goc, dau],
                  cwd=kho, capture_output=True)
    except Exception:
        return None
    ra_mt = getattr(mt, "stdout", None)
    if getattr(mt, "returncode", None) != 0 or not isinstance(ra_mt, (bytes, bytearray)) \
            or not re.fullmatch(rb"[0-9a-f]{40}\n", bytes(ra_mt)):
        return None
    return doc_diff_cay(goc, bytes(ra_mt).decode("ascii").strip(), chay, kho)


def doc_diff_cay(goc, cay, chay=subprocess.run, kho=ROOT):
    """Tập đường dẫn đổi `goc -> cay` (cây merge-tree, hoặc commit merge ref), `--no-renames`; None = KHÔNG ĐO ĐƯỢC."""
    try:
        dt = chay(["git", "--attr-source=" + goc, "diff", "--no-renames", "--name-only", "-z", goc, cay],
                  cwd=kho, capture_output=True)
    except Exception:
        return None
    ra_dt = getattr(dt, "stdout", None)
    if getattr(dt, "returncode", None) != 0 or not isinstance(ra_dt, (bytes, bytearray)):
        return None
    if ra_dt and not bytes(ra_dt).endswith(b"\0"):
        return None
    return {x for x in bytes(ra_dt).decode("utf-8", "surrogateescape").split("\0") if x}


def kiem_cap_khong_pr(env, chay=subprocess.run, kho=ROOT):
    """push / workflow_dispatch: cap (goc, dau) da chuan hoa phai hop le, hoac chuoi ly do = KHONG DO DUOC. Doi `dau` BANG
    merge ref (`github.sha`) va `goc` la TO TIEN cua `dau` (force push / lich su viet lai => khong do duoc). Kiem bang OID,
    khong bang ten ref."""
    goc, dau, hop = (env.get(k) or "" for k in (BIEN_GOC, BIEN_DAU, BIEN_MERGE))
    if not all(type(x) is str and MAU_SHA.fullmatch(x) and set(x) != {"0"} for x in (goc, dau, hop)):
        return "goc/dau/merge vang, sai mau SHA hoac toan so 0"
    if dau != hop:
        return "dau khac merge ref"
    try:
        r = chay(["git", "merge-base", "--is-ancestor", goc, dau], cwd=kho, capture_output=True)
    except Exception as e:
        return f"git merge-base --is-ancestor nem {type(e).__name__}"
    rc = getattr(r, "returncode", None)
    if rc == 1:
        return "goc KHONG phai to tien cua dau (force push / lich su viet lai)"
    if rc != 0:
        return f"git merge-base --is-ancestor rc={rc}"
    return None


def chuan_hoa_cap(env, chay=subprocess.run, kho=ROOT):
    """(env da chuan hoa, None) hoac (None, ly do DAY_DU). PR: giu nguyen. push: goc = `github.event.before` (BIEN_GOC),
    dau = merge ref. workflow_dispatch: input `che_do` (vang/`tu_dong` => phan loai; `day_du` => day du; la => day du),
    goc = merge-base(origin/<nhanh mac dinh>, merge ref) — DUNG MOT merge-base, khong thi khong do duoc."""
    su_kien = env.get(BIEN_SU_KIEN) or ""
    if su_kien == "pull_request":
        return dict(env), None
    if su_kien not in SU_KIEN_PHAN_LOAI:
        return None, f"su_kien={su_kien!r} khong thuoc {SU_KIEN_PHAN_LOAI}, luon DAY_DU"
    hop = env.get(BIEN_MERGE) or ""
    if su_kien == "push":
        return {**env, BIEN_DAU: hop}, None
    vao = env.get(BIEN_CHE_DO_VAO, "")
    if type(vao) is not str or vao not in ("", "tu_dong", "day_du"):
        return None, f"input che_do={vao!r} la (chi nhan tu_dong|day_du), DAY_DU"
    if vao == "day_du":
        return None, "input che_do=day_du (chu kho yeu cau chay du), DAY_DU"
    nhanh = env.get(BIEN_NHANH_MAC_DINH) or ""
    if not (type(nhanh) is str and MAU_TEN_NHANH.fullmatch(nhanh)):
        return None, f"KHONG DO DUOC nhanh mac dinh {nhanh!r}, DAY_DU"
    if not (type(hop) is str and MAU_SHA.fullmatch(hop) and set(hop) != {"0"}):
        return None, "KHONG DO DUOC merge ref cua dispatch, DAY_DU"
    try:
        mb = chay(["git", "merge-base", "--all", "refs/remotes/origin/" + nhanh, hop], cwd=kho, capture_output=True)
    except Exception as e:
        return None, f"KHONG DO DUOC merge-base dispatch (nem {type(e).__name__}), DAY_DU"
    ra = getattr(mb, "stdout", None)
    if getattr(mb, "returncode", None) != 0 or not isinstance(ra, (bytes, bytearray)) \
            or not re.fullmatch(rb"[0-9a-f]{40}\n", bytes(ra)):
        return None, "KHONG DO DUOC merge-base dispatch (rc khac 0, khong co hoac nhieu merge-base), DAY_DU"
    return {**env, BIEN_GOC: bytes(ra).decode("ascii").strip(), BIEN_DAU: hop}, None


def doc_raw_ba_cap(env, chay=subprocess.run, kho=ROOT):
    """{duong dan: [(mode cu, mode moi, trang thai), ...]} tren DUNG ba cap cua bo phan loai, hoac chuoi loi."""
    goc, dau, hop = (env.get(k) or "" for k in (BIEN_GOC, BIEN_DAU, BIEN_MERGE))
    try:
        kq_cay_raw = chay(["git", "--attr-source=" + goc, "merge-tree", "--write-tree", "--no-messages", goc, dau],
                     cwd=kho, capture_output=True)
    except Exception as e:
        return f"KHONG DO DUOC: merge-tree (raw) nem {type(e).__name__}"
    dong_cay = getattr(kq_cay_raw, "stdout", None)
    if getattr(kq_cay_raw, "returncode", None) != 0 or not isinstance(dong_cay, (bytes, bytearray)) \
            or not re.fullmatch(rb"(?:[0-9a-f]{40}|[0-9a-f]{64})\n", bytes(dong_cay)):
        return f"KHONG DO DUOC: merge-tree (raw) rc={getattr(kq_cay_raw, 'returncode', None)}"
    cay_raw = bytes(dong_cay)[:-1].decode("ascii")
    kq = {}
    for cap in ((f"{goc}...{dau}",), (goc, cay_raw), (goc, hop)):
        ban_ghi = _doc_raw(goc, cap, chay, kho)
        if isinstance(ban_ghi, str):
            return ban_ghi
        for duong, (moi, tt, cu) in ban_ghi.items():
            kq.setdefault(duong, []).append((cu, moi, tt))
    return kq


def ly_do_ve_day_du(doi, raw):
    """Danh sach ly do dua mot diff TOAN allowlist ve DAY_DU (dac ta CI-LAN-LUU-TRU, muc luat bo phan loai); rong = khong co."""
    ly = []
    for duong in sorted(doi):
        tp = duong.split("/")
        if len(tp) == 3 and tp[2].lower().endswith(DUOI_MA_CAP_NONG):
            ly.append(f"ma cap nong {duong!r}")
    for duong, cac in sorted(raw.items()):
        for cu, moi, tt in cac:
            if moi in MODE_MOI_VE_DAY_DU:
                ly.append(f"{MODE_MOI_VE_DAY_DU[moi]} (mode {moi}) {duong!r}")
            elif cu != "000000" and moi != "000000" and cu != moi:
                ly.append(f"doi mode {cu}->{moi} {duong!r}")
            if duong.startswith("ops/specs/") and tt in ("M", "D", "T"):
                ly.append(f"sua/xoa dac ta da co ({tt}) {duong!r}")
    return sorted(set(ly))


def phan_loai_day_du(env, chay=subprocess.run, kho=ROOT):
    """(doi, che_do, ly_do) tren env DA chuan hoa (chuan_hoa_cap). Dung chung cho `chuan-bi` va `kiem-re`."""
    su_kien = env.get(BIEN_SU_KIEN) or ""
    doi = doc_diff(env, chay, kho)
    if doi is not None and not doi and su_kien != "pull_request":
        return doi, DAY_DU, f"DUONG_NHANH: diff RONG tren su_kien={su_kien} - coi la yeu cau chay du, DAY_DU"
    che_do, ly_do = phan_loai_tu_diff(doi)
    if che_do != DUONG_NHANH or not doi:
        return doi, che_do, ly_do
    raw = doc_raw_ba_cap(env, chay, kho)
    if isinstance(raw, str):
        return doi, DAY_DU, f"DUONG_NHANH: {raw} - fail-close ve DAY_DU"
    ly = ly_do_ve_day_du(doi, raw)
    if ly:
        them = f" (+{len(ly) - TOI_DA_TEN_IN} ly do nua)" if len(ly) > TOI_DA_TEN_IN else ""
        return doi, DAY_DU, "DUONG_NHANH: DAY_DU vi " + "; ".join(ly[:TOI_DA_TEN_IN]) + them
    return doi, che_do, ly_do


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


def phan_loai(env=os.environ, chay=subprocess.run, kho=ROOT, tra_env=False):
    """(che_do, ly_do) — hoac (che_do, ly_do, env chuan hoa | None) khi `tra_env`. Su kien ngoai SU_KIEN_PHAN_LOAI, hay
    dispatch voi input `day_du`/la ⇒ `day_du` ma KHONG goi git."""
    env2, ly = chuan_hoa_cap(env, chay, kho)
    if env2 is None:
        kq = (DAY_DU, "DUONG_NHANH: khong phan loai - " + ly)
    else:
        _doi, che_do, ly_do = phan_loai_day_du(env2, chay, kho)
        kq = (che_do, ly_do)
    return (*kq, env2) if tra_env else kq


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
    master trong khi mọi kiểm khác của `kiem-re` vẫn DAT. Hồ sơ không cần symlink ⇒ chặn mọi symlink, treo hay không,
    mọi đuôi tệp. (`.gitattributes` KHÔNG bị chặn ở đây — xem D1 và `kiem_diff_check`.) Chốt này đọc ĐĨA; nó không thấy
    gitlink (thư mục rỗng) hay symlink trên nền `core.symlinks=false` — `kiem_mode_git` đọc mode trong GIT và phủ cả hai."""
    return [f"tep ho so la symlink (duong nhanh chi nhan tep thuong): {duong!r}"
            for duong in sorted(doi) if (Path(kho) / duong).is_symlink()]


# Bỏ qua ĐÚNG những gì `t82` của ops/lease_publish_test.py bỏ khi `shutil.copytree` cả cây — cùng hàm `ignore_patterns`, cùng
# mẫu (ca `t20zj` đọc lại mẫu từ chính t82 và đòi khớp, để hai bên không trôi lệch).
BO_QUA_NHU_T82 = (".git", "__pycache__", "*.pyc")


def kiem_symlink_treo_ca_cay(kho=ROOT) -> list[str]:
    """Cây ĐĨA mà `t82` sẽ chép phải chép được: ở mọi chỗ bộ duyệt dưới đây tới được (không chỉ tệp trong diff), symlink
    TREO, VÒNG symlink thư mục hay một lá KHÔNG phải tệp thường ⇒ ĐỎ. Cross-review lượt 8 (P2
    `buoc-bi-bo-doc-ca-cay-khong-chi-ba-ca`): bước bị bỏ `lease-publish selftest` có `t82` `copytree` CẢ cây, theo symlink;
    `kiem_loai_tep`/`kiem_mode_git` chỉ nhìn đường dẫn ĐỔI. PR hồ sơ XOÁ/đổi tên đích của một symlink HỢP LỆ có sẵn (vào
    qua PR đầy đủ, ở `docs/`, dưới allowlist hay trong thư mục chấm) — hoặc xoá hết một thư mục hồ sơ mà đường dẫn symlink
    đi XUYÊN qua — làm symlink ấy treo trong khi nó KHÔNG nằm trong diff ⇒ PR xanh, `t82` ĐỎ trên master (đo 01-10-2026).
    Treo đo bằng `os.path.exists` (stat của nhân, theo từng thành phần), KHÔNG bằng ghép đường dẫn từ vựng: `a/b/../c` cần
    `a/b` có thật; `os.walk` xếp symlink treo vào danh sách TỆP (kể cả symlink từng trỏ thư mục).

    BẤT BIẾN (cross-review lượt 17 mở lại lớp; lượt 18 đóng theo lớp): bộ duyệt đi ĐÚNG những đường `t82` đi — `copytree`
    không `symlinks=True`, mẫu bỏ qua `BO_QUA_NHU_T82`; `t20zj` khoá cả CÁCH GỌI `copytree` của `t82` (chỉ nguồn, đích và
    `ignore=`), vì mọi tham số khác đổi ngữ nghĩa mà chốt này mô phỏng. Mỗi chỗ hai bên có thể lệch là một chốt riêng:
    · THEO symlink thư mục (`followlinks=True`): bí danh thư mục trỏ vào thư mục tên bị bỏ qua (`*.pyc`, `__pycache__`) hay
      ra ngoài cây thì `t82` chép QUA nó, nên symlink treo chỉ với tới được qua bí danh cũng làm `t82` vấp (`t20zk`).
    · Mẫu bỏ qua áp THEO TÊN MỤC ở MỌI cấp, kể cả sau khi đi qua bí danh, và KHÔNG áp lên tên ĐÍCH của bí danh — `t82` cũng
      vậy; áp rộng hơn là ĐỎ oan, hẹp hơn là lọt (`t20zl`, `t20zk`).
    · VÒNG: thư mục sắp vào trùng `(st_dev, st_ino)` với một TỔ TIÊN trên chính đường đang duyệt ⇒ ĐỎ, không đi vào. `t82`
      theo vòng tới khi nhân từ chối phân giải đường dẫn, rồi vấp; hai vòng về gốc thì số đường bùng nổ và `t82` không
      kết thúc (đo trên 41508cd cộng bản vá gợi ý lượt 17: quá hạn 15 s, bộ duyệt chỉ theo symlink cũng quá hạn).
      Chỉ so TỔ TIÊN, không so "đã thăm" toàn cục: bí danh KHÔNG vòng tới thư mục anh em vẫn được duyệt như `t82` (`t20zm`).
    · KHÔNG khử trùng thư mục đã thăm: chuỗi symlink lồng sâu (không vòng) làm nhân từ chối phân giải tuỳ ĐƯỜNG đi chứ
      không tuỳ thư mục; `t82` theo đúng đường ấy và vấp, còn tập "đã thăm" bỏ sót nó khi thứ tự tên đưa đường ngắn tới
      trước (`t20zn`). Phần tử nhân từ chối phân giải hiện ra như symlink TREO.
    · LÁ phải là TỆP THƯỜNG sau khi theo symlink (danh sách CHO PHÉP, không liệt kê loại cấm): `copytree` MỞ và ĐỌC từng
      tệp — FIFO ném `SpecialFileError`, socket ném `OSError` (đo trên 41508cd, kho tạm). Tệp thiết bị: theo mã `copyfile`
      (đọc, chưa đo) `t82` có khi chép được, nên ở đây CHẶT hơn `t82` — chấp nhận vì fail-close và git không lưu được loại
      tệp ấy (`t20zo`).
    Không đọc được một thư mục, hay không lấy được danh tính của nó ⇒ KHÔNG ĐO ĐƯỢC ⇒ ĐỎ.
    Giới hạn, nói thẳng: (a) bí danh KHÔNG vòng mà số đường bùng nổ (mỗi tầng nhiều bí danh xuống cùng tầng dưới) thì bộ
    duyệt bùng nổ y như `t82` (suy từ cách duyệt, chưa đo riêng) — không khử trùng là giá của bất biến trên; PR hồ sơ không
    thêm được symlink (`kiem_mode_git`), nên cấu trúc ấy phải có sẵn trên master, nơi `t82` đã treo trước. (b) tệp thường
    KHÔNG ĐỌC ĐƯỢC, hay đường dẫn ĐÍCH của `copytree` vượt giới hạn độ dài (tiền tố thư mục tạm của `t82` khác gốc kho), làm
    `t82` vấp mà chốt này không thấy: KHÔNG ĐO ĐƯỢC ở đây (máy đo chạy quyền root; tiền tố tạm của máy chạy chưa đo). Không
    lệnh git nào: đây là cây ĐĨA mà `t82` sẽ chép."""
    bo_qua = shutil.ignore_patterns(*BO_QUA_NHU_T82)
    loi = []

    def khong_doc_duoc(e):
        loi.append(f"KHONG DO DUOC: khong duyet duoc cay de tim symlink treo: {type(e).__name__}: {getattr(e, 'filename', '')!r}")

    def tuong_doi(p):
        return os.path.relpath(p, kho).replace(os.sep, "/")

    def danh_tinh(p):
        """`(st_dev, st_ino)` của thư mục mà `p` trỏ tới (THEO symlink); không stat được ⇒ None và một dòng KHÔNG ĐO ĐƯỢC."""
        try:
            st = os.stat(p)
        except OSError as e:
            khong_doc_duoc(e)
            return None
        return st.st_dev, st.st_ino

    goc_cay = os.fspath(kho)
    to_tien = {}   # thư mục sẽ vào -> danh tính MỌI thư mục trên đường từ gốc cây tới nó, kể cả chính nó
    for goc, thu_muc, tep in os.walk(kho, onerror=khong_doc_duoc, followlinks=True):
        tren = frozenset({danh_tinh(goc)}) if goc == goc_cay else to_tien.pop(goc)
        bo = bo_qua(goc, thu_muc + tep)
        thu_muc[:] = sorted(d for d in thu_muc if d not in bo)
        di_tiep = []
        for d in thu_muc:
            p = os.path.join(goc, d)
            dd = danh_tinh(p)
            if dd is None:
                continue
            if dd in tren:
                loi.append("VONG symlink thu muc (t82 cua lease-publish selftest theo vong toi khi nhan tu choi phan giai, se DO): "
                           f"{tuong_doi(p)!r}")
                continue
            to_tien[p] = tren | {dd}
            di_tiep.append(d)
        thu_muc[:] = di_tiep
        for ten in sorted(t for t in tep if t not in bo):
            p = os.path.join(goc, ten)
            if os.path.islink(p) and not os.path.exists(p):
                loi.append("symlink TREO trong cay (t82 cua lease-publish selftest chep CA cay se DO): "
                           f"{tuong_doi(p)!r}")
            elif not os.path.isfile(p):
                loi.append("khong phai tep thuong (FIFO/socket/thiet bi hay khong stat duoc; copytree cua t82 mo va doc tung tep, "
                           f"se DO): {tuong_doi(p)!r}")
    return loi


MODE_THUONG = {"100644", "100755"}
MAU_BAN_GHI_RAW = re.compile(r":([0-7]{6}) ([0-7]{6}) ([0-9a-f]{40}(?:[0-9a-f]{24})?) ([0-9a-f]{40}(?:[0-9a-f]{24})?) ([AMDT])")


def _doc_raw(goc, cap, chay, kho):
    """{đường dẫn: (mode mới, trạng thái)} của `git diff --raw` trên MỘT cặp; hoặc một chuỗi lỗi (KHÔNG ĐO ĐƯỢC)."""
    try:
        r = chay(["git", "--attr-source=" + goc, "diff", "--raw", "-z", "--no-renames", "--no-abbrev", *cap],
                 cwd=kho, capture_output=True)
    except Exception as e:
        return f"KHONG DO DUOC: git diff --raw {' '.join(cap)} nem {type(e).__name__}"
    ra = getattr(r, "stdout", None)
    if getattr(r, "returncode", None) != 0 or not isinstance(ra, (bytes, bytearray)):
        return f"KHONG DO DUOC: git diff --raw {' '.join(cap)} rc={getattr(r, 'returncode', None)}"
    if ra and not bytes(ra).endswith(b"\0"):
        return f"KHONG DO DUOC: git diff --raw {' '.join(cap)} dau ra cut"
    muc = bytes(ra).decode("utf-8", "surrogateescape").split("\0")[:-1]
    if len(muc) % 2:
        return f"KHONG DO DUOC: git diff --raw {' '.join(cap)} so muc le (dau ra hong)"
    kq = {}
    for dau_ghi, duong in zip(muc[0::2], muc[1::2]):
        k = MAU_BAN_GHI_RAW.fullmatch(dau_ghi)
        if not k or not duong or duong in kq:
            return f"KHONG DO DUOC: git diff --raw {' '.join(cap)} ban ghi la: {dau_ghi!r} {duong!r}"
        kq[duong] = (k.group(2), k.group(5), k.group(1))
    return kq


def kiem_mode_git(env, chay=subprocess.run, kho=ROOT, doi=frozenset()) -> list[str]:
    """Loại tệp theo MODE TRONG GIT, không theo cây làm việc (cross-review lượt 10, lớp `kiem-re-cua-fail-close-chua-co-ca`).
    Các chốt nội dung khác của kiem-re đọc ĐĨA (vd `kiem_yaml`, `kiem_loai_tep`, `kiem_lease`) hoặc đọc NỘI DUNG diff
    (`--check`, `--numstat`), và cả hai mù theo nhiều cách: gitlink (mode 160000) checkout thành THƯ MỤC rỗng (git cục bộ đo 01-10-2026:
    clone để lại thư mục rỗng — trên runner chưa đo) nên `kiem_yaml`/`kiem_lease` coi `not is_file()` là ĐÃ XOÁ và bỏ qua
    (kể cả tên `.yaml`), `--check` không có nội dung để đọc, numstat đếm được dòng (không ra `-`) nên không bị coi là nhị
    phân; symlink trên nền `core.symlinks=false` (mặc định của Git for Windows theo tài liệu) checkout thành tệp THƯỜNG
    chứa đường đích (`t20x` đo bằng git thật) nên `kiem_loai_tep` không thấy. Mode trong git thì không phụ thuộc cách
    checkout: `git diff --raw` trên ĐÚNG ba cặp mà bộ phân loại dùng
    (`goc...dau`, `goc -> cây merge-tree`, `goc -> github.sha`), thuộc tính từ cây GỐC như mọi lệnh diff khác. Chỉ nhận mode
    mới 100644/100755, hoặc XOÁ (`D`, mode mới 000000); mọi thứ khác (gitlink, symlink, trạng thái lạ) ⇒ ĐỎ. Git lỗi/ném,
    đầu ra cụt/lẻ/bản ghi lạ, hoặc tập đường dẫn của ba cặp KHÁC tập `doi` mà bộ phân loại đã đo ⇒ KHÔNG ĐO ĐƯỢC ⇒ ĐỎ.
    Thêm một chốt ĐĨA cho cặp `goc -> github.sha` (commit mà Actions checkout theo tài liệu, chưa tự đo — xem docstring
    module): đường dẫn git nói là tệp thường thì trên đĩa
    phải LÀ tệp thường — git có mà đĩa không có (va chạm tên không phân biệt hoa thường, checkout thưa…) thì các chốt đọc
    đĩa sẽ bỏ qua nó như tệp đã xoá. Tệp đổi thành thư mục cùng tên là HỢP LỆ: git báo `D` cho tệp và `A` 100644 cho tệp con."""
    goc, dau, hop = (env.get(k) or "" for k in (BIEN_GOC, BIEN_DAU, BIEN_MERGE))
    try:
        mt_mode = chay(["git", "--attr-source=" + goc, "merge-tree", "--write-tree", "--no-messages", goc, dau],
                       cwd=kho, capture_output=True)
    except Exception as e:
        return [f"KHONG DO DUOC: merge-tree (kiem mode) nem {type(e).__name__}"]
    ra_cay = getattr(mt_mode, "stdout", None)
    if getattr(mt_mode, "returncode", None) != 0 or not isinstance(ra_cay, (bytes, bytearray)) \
            or not re.fullmatch(rb"[0-9a-f]{40}(?:[0-9a-f]{24})?\n", bytes(ra_cay)):
        return [f"KHONG DO DUOC: merge-tree (kiem mode) rc={getattr(mt_mode, 'returncode', None)}"]
    cay = bytes(ra_cay).decode("ascii").strip()
    loi, thay = [], set()
    for ten_cap, cap in (("ba cham", (f"{goc}...{dau}",)), ("goc -> cay merge-tree", (goc, cay)),
                         ("goc -> merge ref", (goc, hop))):
        ban_ghi = _doc_raw(goc, cap, chay, kho)
        if isinstance(ban_ghi, str):
            return [ban_ghi]
        thay |= set(ban_ghi)
        for duong, (mode, trang_thai, _cu) in sorted(ban_ghi.items()):
            if trang_thai == "D" and mode == "000000":
                continue
            if trang_thai == "D" or mode not in MODE_THUONG:
                loi.append(f"tep ho so khong phai tep thuong theo git (mode {mode}, {trang_thai}, cap {ten_cap}) - "
                           f"kiem-re khong kiem duoc noi dung: {duong!r}")
            elif ten_cap == "goc -> merge ref" and ((Path(kho) / duong).is_symlink() or not (Path(kho) / duong).is_file()):
                loi.append(f"git (merge ref) noi {duong!r} la tep thuong nhung tren dia KHONG phai tep thuong - "
                           "cac chot doc dia se bo qua no")
    if thay != set(doi):
        lech = sorted(thay ^ set(doi))
        return loi + [f"KHONG DO DUOC: tap duong dan cua git diff --raw lech tap da phan loai: {lech[:TOI_DA_TEN_IN]!r}"]
    return loi


def kiem_diff_check(env=os.environ, chay=subprocess.run, kho=ROOT) -> list[str]:
    """`git diff --check` trên ba chấm, mọi đuôi tệp. Thuộc tính đọc từ cây GỐC (`--attr-source`), không từ cây làm
    việc: `.gitattributes` do PR thêm (vd `conflict-marker-size=40`, `binary`, `-diff` — `t20p` đo cả ba) KHÔNG tắt được báo
    dấu xung đột."""
    goc, dau = env.get(BIEN_GOC) or "", env.get(BIEN_DAU) or ""
    try:
        r = chay(["git", "--attr-source=" + goc, "-c", CAU_HINH_WHITESPACE, "diff", "--check", "--no-renames", f"{goc}...{dau}"],
                 cwd=kho, capture_output=True)
    except Exception as e:
        return [f"KHONG DO DUOC: git diff --check nem {type(e).__name__}"]
    if getattr(r, "returncode", None) == 0:
        return []
    dong = _dau_ra(r).splitlines()[:3]
    return [f"git diff --check rc={getattr(r, 'returncode', None)}: " + " | ".join(dong)]


def kiem_nhi_phan(env=os.environ, chay=subprocess.run, kho=ROOT) -> list[str]:
    """`git diff --check` BỎ QUA tệp git coi là nhị phân (NUL trong nội dung) — dấu xung đột trong đó lọt êm (đo
    30-09-2026). Hồ sơ không cần nhị phân (tại 3569472cb9: 0/1991 tệp dưới allowlist là nhị phân) ⇒ tệp nhị phân đổi
    = KHÔNG ĐO ĐƯỢC ⇒ ĐỎ.
    Thuộc tính đọc từ cây GỐC như `kiem_diff_check`: hai chốt phải phân loại nhị phân theo CÙNG một cây, không thì
    `diff` (set) do PR mang vào ép tệp có NUL thành "văn bản" cho numstat trong khi `--check` vẫn bỏ qua nó (lượt 9)."""
    goc, dau = env.get(BIEN_GOC) or "", env.get(BIEN_DAU) or ""
    try:
        ns = chay(["git", "--attr-source=" + goc, "diff", "--numstat", "-z", "--no-renames", f"{goc}...{dau}"],
                  cwd=kho, capture_output=True)
    except Exception as e:
        return [f"KHONG DO DUOC: git diff --numstat nem {type(e).__name__}"]
    ra_ns = getattr(ns, "stdout", None)
    if getattr(ns, "returncode", None) != 0 or not isinstance(ra_ns, (bytes, bytearray)):
        return [f"KHONG DO DUOC: git diff --numstat rc={getattr(ns, 'returncode', None)}"]
    if ra_ns and not bytes(ra_ns).endswith(b"\0"):
        return ["KHONG DO DUOC: git diff --numstat dau ra cut"]
    return [f"tep ho so nhi phan (diff --check khong kiem duoc): {ban_ghi[4:]!r}"
            for ban_ghi in bytes(ra_ns).decode("utf-8", "surrogateescape").split("\0") if ban_ghi.startswith("-\t-\t")]


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
    chốt khác, chỉ bỏ chốt hạn. Cả `.yaml` và `.yml`. D2 là hành vi chủ kho ĐÃ DUYỆT (issuecomment-5887720007): xem
    docstring module."""
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
    co the lam hong; bo ca suite di la mat chung. Chay nguyen ca trong tep test that, ~7 giay (do tai 3569472cb9,
    container Linux, Python 3.11; phu thuoc may, khong ngoai suy sang runner Actions)."""
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
    doi, che_do, ly_do = phan_loai_day_du(env, chay, kho)
    print(ly_do, file=ra)
    lech = False
    if che_do != DUONG_NHANH:
        lech = True
        print("DUONG_NHANH: kiem-re CHI chay khi diff toan ho so; phan loai lai khong ra DUONG_NHANH - DO "
              "(khong khop voi job chuan-bi)", file=ra)
        if not doi or not all(khop_allowlist(x) for x in doi):
            return 1
        # wp1113: luat mode/spec cua bo phan loai dua symlink, gitlink, 100755... ve DAY_DU TRUOC khi toi cac chot duoi.
        # Van chay cac chot ay de bao loi rieng cua chung (phong thu hai lop, A3 dac ta CI-LAN-LUU-TRU r1); kiem-re van DO.
    loi = (kiem_yaml(doi, kho) + kiem_loai_tep(doi, kho) + kiem_diff_check(env, chay, kho) + kiem_nhi_phan(env, chay, kho)
           + kiem_mode_git(env, chay, kho, doi)
           + kiem_symlink_treo_ca_cay(kho)
           + kiem_lease(doi, kho, chay, bay_gio, ra)
           + kiem_ca_du_lieu(kho, chay))
    for x in loi:
        print("DUONG_NHANH: LOI - " + x, file=ra)
    print(f"DUONG_NHANH: kiem-re {'DO' if loi or lech else 'DAT'} ({len(doi)} tep doi, {len(loi)} loi)", file=ra)
    return 1 if loi or lech else 0


def main(argv=None, env=os.environ, chay=subprocess.run, kho=ROOT, ra=None) -> int:
    ra = ra if ra is not None else sys.stdout
    argv = sys.argv[1:] if argv is None else list(argv)
    if argv == ["kiem-re"]:
        return lenh_kiem_re(env, chay, kho, ra)
    if argv:
        print("dung: ci_duong_nhanh.py [kiem-re]", file=sys.stderr)
        return 2
    env2 = None
    try:
        che_do, ly_do, env2 = phan_loai(env, chay, kho, tra_env=True)
    except Exception as e:
        # Lỗi nội bộ KHÔNG được làm PR kẹt đỏ oan, cũng không được mở đường nhanh: fail-close ⇒ đầy đủ.
        che_do, ly_do = DAY_DU, f"DUONG_NHANH: LOI NOI BO ({type(e).__name__}) - fail-close ve DAY_DU"
    print(ly_do, file=ra)
    print(f"che_do={che_do}", file=ra)
    # wp1113: cap (goc, dau, merge) DA DUNG de phan loai, de `kiem-re` doc lai DUNG cap ay o moi su kien. Chi xuat khi
    # duong nhanh; day du thi rong (kiem-re khong chay).
    cap = {k: (env2 or {}).get(b, "") if che_do == DUONG_NHANH else ""
           for k, b in (("goc", BIEN_GOC), ("dau", BIEN_DAU), ("hop", BIEN_MERGE))}
    tep_ra = env.get("GITHUB_OUTPUT")
    if tep_ra:
        try:
            with open(tep_ra, "a", encoding="utf-8", newline="\n") as f:
                f.write(f"che_do={che_do}\n" + "".join(f"{k}={v}\n" for k, v in cap.items()))
        except OSError as e:
            print(f"DUONG_NHANH: khong ghi duoc GITHUB_OUTPUT ({type(e).__name__}) - DO", file=sys.stderr)
            return 1
    return 0


if __name__ == "__main__":
    _ep_utf8()
    raise SystemExit(main())
