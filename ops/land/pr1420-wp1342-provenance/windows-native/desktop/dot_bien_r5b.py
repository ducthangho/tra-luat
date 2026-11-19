#!/usr/bin/env python3
"""Driver đột biến NGOÀI kho cho #1342 r5 (đặc tả §4b, M7/N7). Không sửa tệp nào của kho: mỗi đột biến chạy trên một BẢN SAO TẠM của `.claude/dev`.

    python dot_bien_r5.py <thư mục .claude/dev> [id đột biến ...]      # mặc định: mọi đột biến của NỀN đang chạy
    python dot_bien_r5.py <thư mục .claude/dev> --kiem-neo             # chỉ kiểm mỗi cặp (tìm, thay) khớp ĐÚNG MỘT chỗ + bản đột biến parse được

Khác driver r4: tệp đích có thể là `packet_loop_test.py` (e1c, f1, f2) — bản sao test ĐÃ đột biến là bản được chạy, cùng `packet_loop.py` của bản sao.
Mỗi ca chạy trong tiến trình con riêng, watchdog NGOÀI ca 120 s. Phân hạng:
  GIẾT            ⇔ ca đích ĐẠT trên bản sạch VÀ trên bản đột biến ĐỎ bằng AssertionError mang ĐỦ các chuỗi dấu hiệu VÀ mọi ca `xanh` ĐẠT trên bản đột biến.
  GIET_DOI_CHUNG  (riêng e1c) ⇔ J4 sạch ĐẠT; bản sao test đúng MỘT thay thế; J4 trên bản sao kết thúc KHÔNG ĐO bằng ĐÚNG nhãn
                  "J4 (ii): job cho phép breakaway mà lời xin vẫn bị từ chối" kèm `['loi', 5]`, khung ca không báo fixture tự kết thúc/vỡ; J1 trên bản sao ĐẠT.
  a1 chỉ được chấm khi J12 sạch cùng lượt ra nhánh (B) (đọc `observed` của dòng WP1342_NATIVE_V1); không ⇒ KHÔNG ĐO.
Mọi kết cục khác (BỎ QUA/KHÔNG ĐO ngoài e1c, lỗi import, hết hạn, đỏ nhãn khác, thiếu tệp, sai schema, mã ≠ 5) KHÔNG tính giết.
Ca trong `ghi` chỉ được GHI kết quả, không chấm (J4 dưới e2).
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

P, J = "wp1342_pure_spawn_", "wp1342_native_job_"
J1, J4, J5, J12, S6 = J + "thuan", J + "breakaway_tuong_minh", J + "breakaway_ngam", J + "long", P + "fx_mo_rong"
E = "_1174_WIN_JOB_LIMIT = 0x2000   # JOBOBJECT"
PL, TEST = "packet_loop.py", "packet_loop_test.py"
DOT_BIEN = {
    "e1": dict(nen="nt", tep=PL, cap=[(E, E.replace("0x2000", "0x2800"))], dich=J4, doi="DO", co=["J4: breakaway tường minh được nhận"],
               xanh=[J5, J1]),
    "e2": dict(nen="nt", tep=PL, cap=[(E, E.replace("0x2000", "0x3000"))], dich=J5, doi="DO", co=["J5: cháu ngoài job đích"], xanh=[J1], ghi=[J4]),
    "e1c": dict(nen="nt", tep=TEST, cap=[("0x2800", "0x2000")], dich=J4, doi="KHONG_DO", hang="GIET_DOI_CHUNG",
                co=["J4 (ii): job cho phép breakaway mà lời xin vẫn bị từ chối", "['loi', 5]]"], cam=["fixture tự kết thúc"], xanh=[J1]),
    "a1": dict(nen="nt", tep=PL, cap=[('"terminate": lambda: need(k.TerminateJobObject(job, 1), "job terminate"),', '"terminate": lambda: None,')],
               dich=J12, doi="DO", co=["J12: nhánh khác", "job not empty", "[1, 1, 0, 1, 1, 0]", "'chau'"], xanh=[J1], sach_co="(('B',"),
    "f1": dict(nen="moi", tep=TEST, cap=[("\"    elif ma == 'tach':\\n        co, khoa, viec", "\"    elif ma == 'tach'\\n        co, khoa, viec")],
               dich=S6, doi="DO", co=["S6: fixture mở rộng không biên dịch"], xanh=[P + "hang_luong"]),
    "f2": dict(nen="moi", tep=TEST, cap=[("_wp1342a1ii_FX = _wp1342a1_FX + (", "_wp1342a1ii_FX = \"x\" + _wp1342a1_FX + (")],
               dich=S6, doi="DO", co=["S6: fixture base bị đổi"], xanh=[P + "hang_luong"]),
}
VO = r'''
import json, sys, tempfile, warnings
from pathlib import Path
warnings.simplefilter("ignore")
dev, ten = sys.argv[1:3]
sys.path.insert(0, dev)
import packet_loop_test as t
for s in (sys.stdout, sys.stderr):
    s.reconfigure(encoding="utf-8", errors="backslashreplace")
with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as td:
    try:
        dict(t.CASES)[ten](t.Ctx(Path(dev) / "packet_loop.py", Path(td)))
        kq = ("DAT", "")
    except t.BoQua as ex:
        kq = ("KHONG_DO", str(ex))
    except AssertionError as ex:
        kq = ("DO", str(ex))
    except BaseException as ex:
        kq = ("KHONG_DO", "ngoại lệ khác AssertionError: " + type(ex).__name__ + ": " + str(ex))
    print("KQ_R5 " + json.dumps(kq, ensure_ascii=True), flush=True)  # r5b: in TRUOC khi don thu muc tam (WinError 32 lan 1)
'''


def chay_ca(dev, ten):
    """(trạng thái, thông điệp, observed của dòng WP1342_NATIVE_V1 hoặc '')."""
    try:
        p = subprocess.run([sys.executable, "-B", "-c", VO, str(dev), ten], capture_output=True, text=True, timeout=120,
                           encoding="utf-8", errors="backslashreplace", env=dict(os.environ, PYTHONUTF8="1", PYTHONDONTWRITEBYTECODE="1"))
    except subprocess.TimeoutExpired:
        return ("KHONG_DO", "watchdog ngoài ca 120 s", "")
    dong = [ln for ln in p.stdout.splitlines() if ln.startswith("KQ_R5 ")]
    nat = [json.loads(ln[17:]).get("observed", "") for ln in p.stdout.splitlines() if ln.startswith("WP1342_NATIVE_V1 ")]
    if not dong:
        return ("KHONG_DO", f"không có dòng kết quả: rc={p.returncode} {p.stderr[-400:]}", "")
    return (*json.loads(dong[-1][6:]), nat[-1] if nat else "")


def dot_bien(goc, cap):
    for tim, thay in cap:
        assert goc.count(tim) == 1, f"mốc khớp {goc.count(tim)} chỗ (đòi đúng 1): {tim[:90]!r}"
        goc = goc.replace(tim, thay)
    return goc


def main():
    import ast
    for s in (sys.stdout, sys.stderr):
        s.reconfigure(encoding="utf-8", errors="backslashreplace")
    dev, chon = Path(sys.argv[1]).resolve(), sys.argv[2:]
    if chon == ["--kiem-neo"]:
        for ma, v in DOT_BIEN.items():
            ast.parse(dot_bien((dev / v["tep"]).read_bytes().decode("utf-8"), v["cap"]))
            print(f"  neo OK + parse OK  {ma} ({v['tep']}, {len(v['cap'])} cặp)")
        return 0
    nen = "nt" if os.name == "nt" else "moi"
    chon = chon or [ma for ma, v in DOT_BIEN.items() if v["nen"] == "moi" or nen == "nt"]
    hong = 0
    with tempfile.TemporaryDirectory(prefix="dot_bien_r5_", ignore_cleanup_errors=True) as td:
        for ma in chon:
            v = DOT_BIEN[ma]
            ban = Path(td) / ma / "dev"   # thư mục riêng từng đột biến: không dùng chung tệp, không dùng chung bytecode
            shutil.copytree(dev, ban, ignore=shutil.ignore_patterns("__pycache__", ".packet_state", "*.pyc"))
            (ban / v["tep"]).write_bytes(dot_bien((dev / v["tep"]).read_bytes().decode("utf-8"), v["cap"]).encode("utf-8"))
            sach, do = chay_ca(dev, v["dich"]), chay_ca(ban, v["dich"])
            xanh, ghi = [chay_ca(ban, t)[0] for t in v["xanh"]], [(t, *chay_ca(ban, t)[:2]) for t in v.get("ghi", [])]
            du_dk = sach[0] == "DAT" and v.get("sach_co", "") in sach[2]
            giet = (du_dk and do[0] == v["doi"] and all(s in do[1] for s in v["co"]) and not any(s in do[1] for s in v.get("cam", []))
                    and xanh == ["DAT"] * len(xanh))
            hang = v.get("hang", "GIẾT") if giet else "SỐNG" if do[0] == "DAT" and sach[0] == "DAT" else "KHÔNG ĐO"
            hong += not giet
            print(f"{hang:14} {ma:4} tệp={v['tep']} đích={v['dich']} [sạch={sach[0]} đột biến={do[0]}] xanh={'+'.join(v['xanh'])} {xanh} dấu hiệu đòi={v['co']!r}")
            print(f"               thông điệp: {(do[1] or sach[1])[:500]}")
            print(f"               observed sạch: {sach[2][:300]}")
            for t, tt, td_ in ghi:
                print(f"               GHI (không chấm) {t}: {tt} {td_[:300]}")
    print(f"TỔNG: {len(chon) - hong}/{len(chon)} giết đúng dấu hiệu")
    return int(bool(hong))


if __name__ == "__main__":
    sys.exit(main())
