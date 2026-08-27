#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Phản chứng CHẠY ĐƯỢC cho hợp đồng IDIOM BA TÊN — packet #345, kế nhiệm #337.

`CLAUDE.md` cấm giả định Windows có `python3`, nên tài liệu/skill của kho phải gọi python
qua idiom BA TÊN:

    PY="$(command -v python3 || command -v python || command -v py)"
    "$PY" <lệnh>

Packet #337 dọn 18 dòng gọi trần trong 4 tệp. Tệp này là thứ GIỮ mức ấy — và nó tồn tại
vì bộ phản chứng của #337 sống ở thư mục tạm, ngoài kho, không cổng CI, tức sẽ chết theo
container. Guard không nối vào đường TỰ ĐỘNG thì guard chỉ là tài liệu (bài học r225).

BA KHUYẾT TẬT ĐO ĐƯỢC của bản ngoài kho, cross-review codex lượt 2 trên PR #340 tìm ra —
chúng định nghĩa thiết kế ở đây:

 · F1 `phan-chung-bo-sot-lenh-tran-trong-khoi-nhieu-lenh` — bản cũ chỉ đòi mỗi khối có MỘT
   lần dùng `"$PY"` rồi xét phép gán so với lần dùng ĐẦU TIÊN. Khôi phục MỘT dòng trần
   trong khối nhiều lệnh ⇒ vẫn `12/12 ĐẠT`. Tức nó mù với chính lỗi packet sinh ra để
   chặn. Bất biến đúng là **KHÔNG CÒN LỜI GỌI TRẦN NÀO**, không phải "mỗi khối có phép gán".
 · F2 `phan-chung-dem-muoi-tam-bang-hang-so` — ca đếm viết `len(lech) + (18 - len(lech))`
   rồi so với `18`: biểu thức ấy ĐỒNG NHẤT bằng 18. Một ca không thể đỏ thì không phải
   bằng chứng. Bỏ hẳn; "18 dòng" là phép đo LỊCH SỬ neo vào một diff, không phải bất biến.
 · F3 `phan-chung2-khong-nhan-co-kho` — script lấy thẳng `sys.argv[1]`, nên `--kho X` ném
   `FileNotFoundError` trước khi vào ca nào. Ở đây có `argparse`.

VÀ MỘT BÀI HỌC MƯỢN TỪ PR #343 (cùng phiên, cùng hình dạng): **vị từ XANH-THEO-CẤU-TẠO
không thể tự chứng minh có răng.** Trên dữ liệu thật phạm vi có 0 lời gọi trần, nên nhánh
"báo xấu" của C1 CHƯA TỪNG CHẠY — đột biến làm vị từ luôn-tha sẽ không giết được ca nào.
Nên vị từ nhận DỮ LIỆU LÀM ĐỐI SỐ (`_goi_tran`, `_loi_hop_dong_khoi`) và có ca BIẾT TRƯỚC
ĐÁP ÁN riêng, hai chiều. Đó là chỗ duy nhất răng ĐO ĐƯỢC thay vì suy ra.
"""

from __future__ import annotations

import argparse
import os
import platform
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):        # console cp1258 giết cả lượt chạy trước khi
    sys.stdout.reconfigure(encoding="utf-8")  # logic kịp sai — bài học 12-08-2026
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]

IDIOM = 'PY="$(command -v python3 || command -v python || command -v py)"'

_RE_HANG_RAO = re.compile(r"^\s*```")
_RE_GAN = re.compile(r"^\s*PY=")
_RE_DUNG = re.compile(r'"\$PY"')
# Lời gọi TRẦN: tên trình thông dịch ở đầu dòng, sau `|`/`;`/`&`/`(`, hoặc trong `$(`.
# Chỉ quét TRONG khối hàng rào, nên văn xuôi không lọt vào đây.
_RE_TRAN = re.compile(r"(^|[|;&(]\s*|\$\(\s*)(python3?|py)\s+\S")


class BoQua(Exception):
    """Ca KHÔNG ĐO ĐƯỢC trên nền này — phải được ĐẾM RIÊNG, không được lẫn vào ĐẠT."""


# --- PHẠM VI: LUẬT, không phải danh sách chép tay -----------------------------------
#
# Chép tay 4 tên tệp thì một skill MỚI thêm vào sẽ nằm ngoài cổng mà không ai biết — đúng
# lỗi "danh sách không bao giờ đủ". Luật: mọi `*.md` dưới `.claude/skills/**`, cộng
# `docs/PROTOCOL_DA_PHIEN.md`. Đo 27-08-2026 trên `2d1c074`: 7 tệp, cả 7 đều 0 lời gọi
# trần — tức luật rộng hơn danh sách 4 tệp của #337 mà vẫn xanh, nên rộng là MIỄN PHÍ.
def pham_vi(goc: Path) -> list[Path]:
    ra = sorted((goc / ".claude" / "skills").rglob("*.md"))
    p = goc / "docs" / "PROTOCOL_DA_PHIEN.md"
    if p.is_file():
        ra.append(p)
    return ra


# --- VỊ TỪ THUẦN — nhận dữ liệu làm ĐỐI SỐ để có ca biết trước đáp án ----------------
def khoi_hang_rao(van: str) -> list[tuple[int, list[str]]]:
    """[(số dòng đầu khối, [dòng…])] cho MỌI khối hàng rào."""
    d, ra, i = van.split("\n"), [], 0
    while i < len(d):
        if _RE_HANG_RAO.match(d[i]):
            j = i + 1
            while j < len(d) and not _RE_HANG_RAO.match(d[j]):
                j += 1
            ra.append((i + 2, d[i + 1:j]))
            i = j + 1
            continue
        i += 1
    return ra


def goi_tran(van: str) -> list[tuple[int, str]]:
    """[(số dòng, nội dung)] cho mọi lời gọi python TRẦN trong khối hàng rào."""
    ra = []
    for dau, than in khoi_hang_rao(van):
        for k, dong in enumerate(than):
            if '"$PY"' in dong:
                continue
            if _RE_TRAN.search(dong):
                ra.append((dau + k, dong.strip()))
    return ra


def loi_hop_dong_khoi(van: str) -> list[tuple[int, str]]:
    """[(số dòng đầu khối, lý do)] cho mỗi khối dùng `"$PY"` mà sai hợp đồng.

    Ba lỗi TÁCH BIỆT, vì chúng hỏng theo ba cách khác nhau:
      · THIẾU_GÁN  — khối thoát 127;
      · GÁN_MUỘN   — khối in `command not found` rồi THOÁT 0, vì phép gán CUỐI che mã lỗi.
                     Đây là ca độc: một bộ test chỉ đọc mã thoát của cả khối sẽ báo XANH;
      · SAI_DẠNG   — gán có mặt, đúng thứ tự, nhưng không phải idiom BA TÊN.
    """
    ra = []
    for dau, than in khoi_hang_rao(van):
        i_dung = next((k for k, x in enumerate(than) if _RE_DUNG.search(x)), None)
        if i_dung is None:
            continue
        i_gan = next((k for k, x in enumerate(than) if _RE_GAN.match(x)), None)
        if i_gan is None:
            ra.append((dau, "THIẾU_GÁN"))
        elif i_gan > i_dung:
            ra.append((dau, "GÁN_MUỘN"))
        elif IDIOM not in than[i_gan]:
            ra.append((dau, "SAI_DẠNG"))
    return ra


def idiom_phan_biet(goc: Path) -> list[str]:
    return sorted({x.strip()
                   for p in pham_vi(goc)
                   for _, than in khoi_hang_rao(p.read_text(encoding="utf-8"))
                   for x in than if _RE_GAN.match(x)})


# --- Nền PATH một-tên, dùng cho chiều ĐỘNG ------------------------------------------
def _nen_mot_ten(ten: str) -> str:
    """Thư mục chỉ chứa DUY NHẤT một tên trình thông dịch."""
    d = tempfile.mkdtemp(prefix=f"idiom-{ten}-")
    that = shutil.which("python3") or shutil.which("python") or sys.executable
    os.symlink(that, os.path.join(d, ten))
    return d


def _chay(path_nen: str, kich: str) -> int:
    p = subprocess.run(
        ["env", "-i", "PATH=" + path_nen, "HOME=" + os.environ.get("HOME", "/tmp"),
         "/bin/bash", "-c", kich], capture_output=True)
    return p.returncode


def _doi_posix():
    if os.name != "posix" or not Path("/bin/bash").exists():
        raise BoQua(f"chiều ĐỘNG cần POSIX + /bin/bash; nền này là {platform.system()!r}")


# --- CA -----------------------------------------------------------------------------
def ca_pham_vi_khong_rong(goc: Path):
    """Một cổng chạy trên tập RỖNG là một cổng không tồn tại."""
    n = len(pham_vi(goc))
    if n < 2:
        raise AssertionError(f"phạm vi chỉ {n} tệp — cổng gần như không đo gì")


def ca_khong_con_goi_tran(goc: Path):
    """C1 — bất biến CHÍNH. Đây là ca mà đột biến `restore-one-bare-python` phải giết."""
    xau = [f"{p.relative_to(goc)}:{ln}  {s[:70]}"
           for p in pham_vi(goc) for ln, s in goi_tran(p.read_text(encoding="utf-8"))]
    if xau:
        raise AssertionError(
            f"{len(xau)} lời gọi python TRẦN còn trong phạm vi (phải dùng idiom BA TÊN): "
            + " | ".join(xau[:8]))


def ca_hop_dong_khoi(goc: Path):
    """C2 — khối dùng `"$PY"` phải có phép gán ĐÚNG DẠNG và NẰM TRƯỚC lần dùng."""
    xau = [f"{p.relative_to(goc)}:{ln} {ly}"
           for p in pham_vi(goc)
           for ln, ly in loi_hop_dong_khoi(p.read_text(encoding="utf-8"))]
    if xau:
        raise AssertionError(f"{len(xau)} khối sai hợp đồng: " + " | ".join(xau[:8]))


def ca_ba_nen_path(goc: Path):
    """C3 — chiều ĐỘNG: mỗi idiom PHÂN BIỆT phải chạy được trên CẢ BA nền một-tên."""
    _doi_posix()
    ds = idiom_phan_biet(goc)
    if not ds:
        raise AssertionError("không tìm được idiom nào — phạm vi hoặc regex sai")
    xau = []
    for k, idi in enumerate(ds, 1):
        for ten in ("python3", "python", "py"):
            rc = _chay(_nen_mot_ten(ten), idi + '\n"$PY" -c pass\n')
            if rc != 0:
                xau.append(f"idiom#{k} trên nền chỉ có {ten}: rc={rc}")
    if xau:
        raise AssertionError("; ".join(xau))


def ca_doi_chung_dong(goc: Path):
    """Nếu ba chiều trên xanh vì RIG hỏng thì chúng vô nghĩa. Bốn phép đo chốt lại rig."""
    _doi_posix()
    n3, npy = _nen_mot_ten("python3"), _nen_mot_ten("py")
    do = [("một-tên `python` trên nền chỉ có python3", _chay(n3, "python -c pass"), 127),
          ("một-tên `python3` trên nền chỉ có py", _chay(npy, "python3 -c pass"), 127),
          ("RIG còn sống: /bin/true trên nền python3", _chay(n3, "/bin/true"), 0),
          ("mã thoát KHÔNG bị phép gán che",
           _chay(n3, IDIOM + '\n"$PY" -c \'import sys;sys.exit(3)\'\n'), 3)]
    xau = [f"{n}: rc={t} (mong {m})" for n, t, m in do if t != m]
    if xau:
        raise AssertionError("; ".join(xau))


def ca_vi_tu_goi_tran_co_rang(goc: Path):
    """Ca BIẾT TRƯỚC ĐÁP ÁN cho `goi_tran` — hai chiều, vì một vị từ luôn-tố cũng vô dụng
    y như một vị từ luôn-tha. Không có ca này thì C1 xanh-theo-cấu-tạo và không đột biến
    nào giết được nó (bài học PR #343)."""
    xau = "```\nPY=\"x\"\npython a.py\n\"$PY\" b.py\npython3 c.py\n```\n"
    ra = goi_tran(xau)
    if len(ra) != 2 or ra[0][0] != 3 or ra[1][0] != 5:
        raise AssertionError(f"phải tố ĐÚNG 2 dòng trần (3 và 5), nhận: {ra!r}")

    sach = "```\n" + IDIOM + '\n"$PY" a.py\n"$PY" b.py\n```\n'
    if goi_tran(sach):
        raise AssertionError(f"khối SẠCH bị tố oan: {goi_tran(sach)!r}")

    ngoai = 'python a.py\n\n```\n"$PY" b.py\n```\n'   # dòng trần NGOÀI hàng rào
    if goi_tran(ngoai):
        raise AssertionError(f"văn xuôi ngoài hàng rào không được tính: {goi_tran(ngoai)!r}")

    for m in ("cat x | python a.py", "true; python a.py", "$(python a.py)"):
        if not goi_tran("```\n" + m + "\n```\n"):
            raise AssertionError(f"dạng gọi trần bị bỏ sót: {m!r}")


def ca_vi_tu_hop_dong_co_rang(goc: Path):
    """Ca BIẾT TRƯỚC ĐÁP ÁN cho `loi_hop_dong_khoi` — đủ BA lý do, cộng chiều tha."""
    def mot(than: str) -> list[str]:
        return [ly for _, ly in loi_hop_dong_khoi("```\n" + than + "\n```\n")]

    if mot('"$PY" a.py') != ["THIẾU_GÁN"]:
        raise AssertionError("THIẾU_GÁN không bị tố: %r" % (mot('"$PY" a.py'),))
    if mot('"$PY" a.py\n' + IDIOM) != ["GÁN_MUỘN"]:
        raise AssertionError("GÁN_MUỘN không bị tố")
    if mot('PY="python3"\n"$PY" a.py') != ["SAI_DẠNG"]:
        raise AssertionError("SAI_DẠNG không bị tố")
    if mot(IDIOM + '\n"$PY" a.py') != []:
        raise AssertionError("khối ĐÚNG bị tố oan")
    if mot("echo khong dung PY") != []:
        raise AssertionError("khối không dùng `$PY` không được xét")


CA = [
    ("pham_vi_khong_rong", ca_pham_vi_khong_rong),
    ("khong_con_goi_tran", ca_khong_con_goi_tran),
    ("hop_dong_khoi", ca_hop_dong_khoi),
    ("ba_nen_path", ca_ba_nen_path),
    ("doi_chung_dong", ca_doi_chung_dong),
    ("vi_tu_goi_tran_co_rang", ca_vi_tu_goi_tran_co_rang),
    ("vi_tu_hop_dong_co_rang", ca_vi_tu_hop_dong_co_rang),
]

# --- ĐỘT BIẾN ------------------------------------------------------------------------
#
# Hai HỌ, và phải tách vì chúng sửa hai thứ khác nhau:
#   `tai_lieu` — sửa một tệp TRONG PHẠM VI trên BẢN SAO của cây (không bao giờ sửa tệp
#                thật rồi khôi phục trong `finally`: một cú SIGTERM giữa chừng để lại tệp
#                méo, và lượt sau đọc bản méo làm bản gốc — bài học 12-08-2026);
#   `chinh_no` — sửa CHÍNH tệp test, để chứng minh từng vị từ có răng.
# MỐC PHẢI CHÉP TỪ TỆP THẬT, KHÔNG GÕ LẠI TỪ TRÍ NHỚ. Bản đầu của bảng này viết
# `"$PY" .claude/…` một dấu cách, trong khi tệp thật có HAI (chính là chỗ #337 giữ cột đối
# số), nên hai đột biến báo `MỐC KHÔNG CÒN TRONG PHẠM VI` — và nếu bảng chỉ cảnh báo thay
# vì ĐỎ thì đó là hai đột biến MẤT RĂNG trong im lặng.
_HAI_CACH = '"$PY"  '
DOT_BIEN_TAI_LIEU = {
    # Đột biến của reviewer trên PR #340: bản ngoài kho SỐNG SÓT qua nó (12/12 ĐẠT).
    # Đây là ca nghiệm thu chính của packet #345.
    "restore-one-bare-python": (
        _HAI_CACH + ".claude/dev/packet_loop.py record-lease",
        "python .claude/dev/packet_loop.py record-lease",
        ["khong_con_goi_tran"]),
    "drop-name": (
        IDIOM,
        'PY="$(command -v python3 || command -v python)"',
        ["hop_dong_khoi", "ba_nen_path"]),
    # Xoá phép gán nhưng GIỮ phần chú thích phía sau: dòng còn lại không khớp `^\s*PY=`
    # nữa nên khối mất phép gán => THIẾU_GÁN, và khối thật sẽ thoát 127.
    "drop-py-assign": (
        IDIOM,
        "",
        ["hop_dong_khoi"]),
    # Ca ĐỘC của reviewer: khối in `command not found` rồi THOÁT 0 vì phép gán CUỐI che mã
    # lỗi. Đảo đúng hai dòng liền nhau trong `land-packets/SKILL.md`.
    "late-py-assign": (
        IDIOM + "   # CLAUDE.md: nhận CẢ BA tên\n"
        + _HAI_CACH + ".claude/dev/packet_loop.py doctrine-scan --root .\n",
        _HAI_CACH + ".claude/dev/packet_loop.py doctrine-scan --root .\n"
        + IDIOM + "   # đột biến: gán MUỘN\n",
        ["hop_dong_khoi"]),
}
DOT_BIEN_CHINH_NO = {
    "vi_tu_goi_tran_luon_rong": (
        "            if _RE_TRAN.search(dong):\n",
        "            if False:  # đột biến: không bao giờ tố\n",
        ["vi_tu_goi_tran_co_rang"]),
    # Bản đầu của đột biến này gỡ nhánh `if '"$PY"' in dong: continue` — và nó SỐNG, vì
    # `_RE_TRAN` vốn không khớp dòng `"$PY" …` nên gỡ chỗ ấy chẳng đổi gì. Một đột biến
    # KHÔNG-TÁC-DỤNG trông y hệt một ca yếu; chỉ chạy mới biết. Bản này tố MỌI dòng.
    "vi_tu_goi_tran_luon_to": (
        "            if _RE_TRAN.search(dong):\n",
        "            if dong.strip():  # đột biến: tố mọi dòng\n",
        ["vi_tu_goi_tran_co_rang"]),
    "hop_dong_bo_kiem_thu_tu": (
        "        elif i_gan > i_dung:\n",
        "        elif False:  # đột biến: gán muộn cũng tha\n",
        ["vi_tu_hop_dong_co_rang"]),
    "hop_dong_bo_kiem_dang": (
        "        elif IDIOM not in than[i_gan]:\n",
        "        elif False:  # đột biến: dạng nào cũng tha\n",
        ["vi_tu_hop_dong_co_rang"]),
    "pham_vi_thu_hep_ve_rong": (
        '    ra = sorted((goc / ".claude" / "skills").rglob("*.md"))\n',
        "    ra = []  # đột biến: phạm vi rỗng\n",
        ["pham_vi_khong_rong"]),
}


def _cay_tam(goc: Path) -> Path:
    """Bản sao CHỈ phần phạm vi — đủ để đột biến tài liệu, và không đụng cây thật."""
    d = Path(tempfile.mkdtemp(prefix="idiom-cay-"))
    for p in pham_vi(goc):
        dich = d / p.relative_to(goc)
        dich.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(p, dich)
    return d


def _chay_bo_ca(goc: Path, chi=None) -> tuple[dict, dict, dict]:
    """(đạt, bỏ qua, lý do đỏ) — BA bảng RIÊNG.

    Bản đầu nhét lý do vào chính bảng `đạt` dưới khoá `_ly_do`, nên bảng ấy vừa mang bool
    vừa mang dict và `len()` của nó đếm lẫn một khoá không phải ca. Nó chạy đúng, và đó
    mới là vấn đề: một bảng không đồng nhất kiểu là chỗ bug sau này rơi vào lặng lẽ.
    """
    dat, bo, ly_do = {}, {}, {}
    for ten, f in CA:
        if chi and ten not in chi:
            continue
        try:
            f(goc)
            dat[ten] = True
        except BoQua as e:
            bo[ten] = str(e)
        except Exception as e:                      # noqa: BLE001 — ca đỏ là DỮ LIỆU
            dat[ten] = False
            ly_do[ten] = f"{type(e).__name__}: {e}"
    return dat, bo, ly_do


def _ap_dot_bien(van: str, tim: str, thay: str) -> str:
    if van.count(tim) < 1:
        raise AssertionError(f"MỐC KHÔNG CÒN TRONG MÃ: {tim[:60]!r}")
    return van.replace(tim, thay, 1)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--kho", default=str(ROOT), help="gốc kho cần đo (mặc định: kho này)")
    a = ap.parse_args()
    goc = Path(a.kho).resolve()

    dat, bo, ly_do = _chay_bo_ca(goc)
    do_san = sorted(k for k, v in dat.items() if v is False)
    print(f"nền: {sum(1 for v in dat.values() if v)}/{len(dat)} đạt · "
          f"BỎ QUA: {len(bo)}")
    for k, v in sorted(bo.items()):
        print(f"  BỎ QUA {k}: {v}")
    for k in do_san:
        print(f"  ĐỎ    {k}: {ly_do.get(k, '')}")

    # CHẨN ĐOÁN, KHÔNG phải cổng: lời gọi trần NGOÀI phạm vi. Nói ra số thay vì để nó nằm
    # mù — nhưng KHÔNG chặn, vì phần lớn nằm trong hiện vật ĐÓNG BĂNG (`ops/prompts/**`,
    # `ops/reviews/**`, `rasoat/**`): sửa chúng là làm sai lệch hồ sơ, không phải dọn dẹp.
    # Nợ có tên: `no-idiom-ba-ten-tai-lieu-song`.
    trong = {p.resolve() for p in pham_vi(goc)}
    bo_qua_tm = {".git", "node_modules", "claude-code-best-practice"}
    ngoai = 0
    for p in goc.rglob("*.md"):
        if p.resolve() in trong or any(x in p.parts for x in bo_qua_tm):
            continue
        try:
            ngoai += len(goi_tran(p.read_text(encoding="utf-8")))
        except (OSError, UnicodeDecodeError):
            continue
    print(f"CHẨN ĐOÁN (không phải cổng): {ngoai} lời gọi trần NGOÀI phạm vi "
          f"— nợ `no-idiom-ba-ten-tai-lieu-song`")

    if do_san:
        # Nền đỏ thì MỌI đột biến "giết" tầm thường bằng chính các ca đỏ sẵn. Một tỷ lệ
        # tính trên nền đỏ không phải "số nhỏ hơn sự thật" — nó KHÔNG CÓ NGHĨA.
        print(f"\nTỪ CHỐI công bố điểm đột biến: nền có {len(do_san)} ca ĐỎ "
              f"({', '.join(do_san)})")
        return 1

    print("\ntự chứng minh KHÔNG RỖNG (ca đích ĐỎ · nền vẫn phải xanh trước đó):")
    hong = []
    goc_test = Path(__file__).read_text(encoding="utf-8")
    for ten, (tim, thay, dich) in sorted(DOT_BIEN_TAI_LIEU.items()):
        cay = _cay_tam(goc)
        sua = 0
        for p in sorted(cay.rglob("*.md")):
            van = p.read_text(encoding="utf-8")
            if tim in van:
                p.write_text(_ap_dot_bien(van, tim, thay), encoding="utf-8")
                sua += 1
                break
        if sua == 0:
            hong.append(f"{ten}: MỐC KHÔNG CÒN TRONG PHẠM VI")
            continue
        d2, bo2, _ = _chay_bo_ca(cay, chi=set(dich))
        chet = sorted(k for k, v in d2.items() if v is False)
        # CA ĐÍCH BỊ BỎ QUA TRÊN NỀN NÀY KHÔNG PHẢI "CÒN SỐNG". `drop-name` nhắm cả
        # `hop_dong_khoi` (tĩnh) lẫn `ba_nen_path` (ĐỘNG, cần POSIX). Trên Windows ca động
        # tự báo BỎ QUA, và bản đầu tính nó vào `thiếu` ⇒ suite ĐỎ trên nền mà chính packet
        # #337 sinh ra để bảo vệ. Đó là "ca có MẶT khác ca có ĐO" ở chiều ngược: một ca
        # KHÔNG ĐO ĐƯỢC bị đọc thành một chốt hỏng.
        # Gọi TÊN cái bị bỏ, đừng nuốt: nếu MỌI ca đích đều bị bỏ thì đột biến ấy không đo
        # gì trên nền này, và đó vẫn phải là LỖI.
        thieu = [x for x in dich if x not in chet and x not in bo2]
        bo_ten = [x for x in dich if x in bo2]
        if bo_ten and not chet:
            hong.append(f"{ten}: MỌI ca đích bị BỎ QUA trên nền này ({bo_ten}) — "
                        f"đột biến không đo gì")
        nhan = "ok " if not thieu and (chet or not bo_ten) else "LỖI"
        print(f"  {nhan} {ten} → giết {chet or 'KHÔNG CA NÀO'}"
              + (f" · BỎ QUA {bo_ten}" if bo_ten else ""))
        if thieu:
            hong.append(f"{ten}: ca đích còn sống: {thieu}")

    with tempfile.TemporaryDirectory(prefix="idiom-mut-") as tmp:
        for ten, (tim, thay, dich) in sorted(DOT_BIEN_CHINH_NO.items()):
            f = Path(tmp) / f"{ten}.py"
            f.write_text(_ap_dot_bien(goc_test, tim, thay), encoding="utf-8")
            p = subprocess.run([sys.executable, str(f), "--kho", str(goc)],
                               capture_output=True, text=True,
                               env=dict(os.environ, PYTHONDONTWRITEBYTECODE="1"))
            ra = p.stdout
            chet = [x for x in dich if f"ĐỎ    {x}" in ra]
            thieu = [x for x in dich if x not in chet]
            print(f"  {'ok ' if not thieu else 'LỖI'} {ten} → giết {chet or 'KHÔNG CA NÀO'}")
            if thieu:
                hong.append(f"{ten}: ca đích còn sống: {thieu}")

    print(f"\nSỐ LIỆU (đếm bằng máy):\n  ca              : {len(dat)}\n"
          f"  bỏ qua          : {len(bo)}\n"
          f"  đột biến        : {len(DOT_BIEN_TAI_LIEU) + len(DOT_BIEN_CHINH_NO)}\n"
          f"  tệp trong phạm vi: {len(pham_vi(goc))}")
    if hong:
        print("TỔNG: " + f"{len(hong)} lỗi")
        for x in hong:
            print("   " + x)
        return 1
    print("TỔNG: ĐẠT")
    return 0


if __name__ == "__main__":
    sys.exit(main())
