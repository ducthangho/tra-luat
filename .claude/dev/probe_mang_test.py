#!/usr/bin/env python3
"""Phản chứng cho `probe_mang.py` — CHẠY ĐƯỢC, không cần mạng, mỗi ca một đột biến.

Mọi thao tác mạng thật bị thay bằng giả lập (`unittest.mock`): bộ này đo LOGIC
quy đổi kết quả sang mã thoát, KHÔNG đo môi trường đang chạy có mạng hay
không (đo môi trường thật thì chạy chính probe_mang.py — xem
docs/MANG_SANDBOX_CODEX.md). Mỗi kênh có MỘT ca gộp ba mệnh đề: (a) thành
công → MA_LOT, (b) bị chặn → MA_CHAN, (c) một lỗi KHÁC chính sách mạng (bug
trong chính probe) VẪN bị nuốt thành MA_CHAN chứ không được lọt ra làm sập
tiến trình — sập thì các kênh SAU không còn cơ hội chạy (xem ca main).
Nạp module động, mỗi đột biến ra module TÊN RIÊNG (không ghi tệp thật, không
đụng .pyc dùng chung) — xem giải thích đầy đủ ở đầu codex_cred_test.py.
"""
from __future__ import annotations

import contextlib
import importlib.util
import io
import os
import sys
import tempfile
import urllib.error
from pathlib import Path
from unittest import mock

sys.dont_write_bytecode = True

GOC = Path(__file__).with_name("probe_mang.py")
_dem = 0


def nap(nguon: str, nhan: str):
    global _dem
    _dem += 1
    d = Path(tempfile.mkdtemp(prefix="pm-test-"))
    t = d / f"pm_{nhan}_{_dem}.py"
    t.write_text(nguon, encoding="utf-8")
    importlib.invalidate_caches()
    spec = importlib.util.spec_from_file_location(t.stem, t)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    assert not list(d.glob("__pycache__/*")), "đã ghi .pyc — chốt chống va chạm hỏng"
    return m


def t1_bind_hanh_vi_dung(M):
    with mock.patch.object(M.socket, "socket", return_value=mock.MagicMock()):
        assert M.kenh_bind_loopback() == 0
    with mock.patch.object(M.socket, "socket", side_effect=OSError("bi chan")):
        assert M.kenh_bind_loopback() == 1
    with mock.patch.object(M.socket, "socket", side_effect=ValueError("bug")):
        assert M.kenh_bind_loopback() == 1


def t2_urlopen_hanh_vi_dung(M):
    cm = mock.MagicMock()
    cm.__enter__.return_value = cm
    with mock.patch.object(M.urllib.request, "urlopen", return_value=cm):
        assert M.kenh_urlopen() == 0
    with mock.patch.object(M.urllib.request, "urlopen",
                            side_effect=urllib.error.URLError("bi chan")):
        assert M.kenh_urlopen() == 1
    with mock.patch.object(M.urllib.request, "urlopen", side_effect=TypeError("bug")):
        assert M.kenh_urlopen() == 1


def t3_lsremote_hanh_vi_dung(M):
    with mock.patch.object(M.subprocess, "run", return_value=mock.MagicMock(returncode=0)):
        assert M.kenh_git_ls_remote() == 0
    with mock.patch.object(M.subprocess, "run", return_value=mock.MagicMock(returncode=128)):
        assert M.kenh_git_ls_remote() == 1
    with mock.patch.object(M.subprocess, "run", side_effect=TypeError("bug")):
        assert M.kenh_git_ls_remote() == 1


def t4_main_goi_du_ba_kenh_dung_mot_lan(M):
    """`main()` phải GỌI cả ba kênh, đúng một lần — không bỏ sót im lặng."""
    dem = {"bind_loopback": 0, "urlopen": 0, "git_ls_remote": 0}

    def dem_goi(ten):
        def f(*_a, **_k):
            dem[ten] += 1
            return 0
        return f

    M.kenh_bind_loopback = dem_goi("bind_loopback")
    M.kenh_urlopen = dem_goi("urlopen")
    M.kenh_git_ls_remote = dem_goi("git_ls_remote")

    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        rc = M.main()
    dong = [d for d in buf.getvalue().splitlines() if d]
    assert rc == 0
    assert dem == {"bind_loopback": 1, "urlopen": 1, "git_ls_remote": 1}, dem
    assert len(dong) == 3, dong
    assert {d.split("=")[0] for d in dong} == set(dem), dong


def t5_hang_so_MA_LOT_MA_CHAN_dung_gia_tri(M):
    assert M.MA_LOT == 0 and M.MA_CHAN == 1 and M.MA_LOT != M.MA_CHAN


CA = [t1_bind_hanh_vi_dung, t2_urlopen_hanh_vi_dung, t3_lsremote_hanh_vi_dung,
      t4_main_goi_du_ba_kenh_dung_mot_lan, t5_hang_so_MA_LOT_MA_CHAN_dung_gia_tri]

# (nhãn, mỏ neo — PHẢI xuất hiện đúng 1 lần trong nguồn gốc, chuỗi thay, ca phải chết)
DOT_BIEN = [
    ("m1_bind_thu_hep_except", "except Exception:  # bind", "except OSError:  # bind",
     "t1_bind_hanh_vi_dung"),
    ("m2_urlopen_thu_hep_except", "except Exception:  # urlopen", "except OSError:  # urlopen",
     "t2_urlopen_hanh_vi_dung"),
    ("m3_lsremote_thu_hep_except", "except Exception:  # ls_remote",
     "except OSError:  # ls_remote", "t3_lsremote_hanh_vi_dung"),
    ("m4_main_bo_sot_mot_kenh", '        "git_ls_remote": kenh_git_ls_remote(),\n', "",
     "t4_main_goi_du_ba_kenh_dung_mot_lan"),
    ("m5_dao_hang_so_MA_LOT", "MA_LOT = 0", "MA_LOT = 1",
     "t5_hang_so_MA_LOT_MA_CHAN_dung_gia_tri"),
]


def chay_suite(M, chi_chay: set[str] | None = None) -> set[str]:
    do = set()
    for ca in CA:
        if chi_chay is not None and ca.__name__ not in chi_chay:
            continue
        Mi = nap(M.__nguon__, M.__nhan__)
        Mi.__nguon__, Mi.__nhan__ = M.__nguon__, M.__nhan__
        try:
            ca(Mi)
        except Exception as e:
            do.add(ca.__name__)
            if os.environ.get("PM_CHI_TIET"):
                print(f"    ĐỎ {ca.__name__}: {type(e).__name__}: {e}")
    return do


def main() -> int:
    goc = GOC.read_text(encoding="utf-8")
    M = nap(goc, "goc")
    M.__nguon__, M.__nhan__ = goc, "goc"

    do = chay_suite(M)
    n = len(CA)
    print(f"nền: {n - len(do)}/{n} đạt")
    for t in sorted(do):
        print(f"  ĐỎ  {t}")
    if do:
        print("TỔNG: ĐỎ (nền chưa xanh — không đo đột biến khi nền đã đỏ)")
        return 1

    print("\nĐỘT BIẾN — bán kính CHỈ đo trong phạm vi phai_chet:")
    xau = []
    for nhan, cu, moi, dich in DOT_BIEN:
        if goc.count(cu) != 1:
            print(f"  ĐỎ  {nhan}: mỏ neo xuất hiện {goc.count(cu)} lần, cần đúng 1")
            xau.append(nhan)
            continue
        nguon_m = goc.replace(cu, moi, 1)
        try:
            Mm = nap(nguon_m, nhan)
        except SyntaxError as e:
            print(f"  ĐỎ  {nhan:26} KHÔNG BIÊN DỊCH ĐƯỢC: {e}")
            xau.append(f"{nhan}: đột biến không parse")
            continue
        Mm.__nguon__, Mm.__nhan__ = nguon_m, nhan
        phai_chet = {dich}
        chet = chay_suite(Mm, phai_chet)
        ok = chet == phai_chet
        print(f"  {'ok ' if ok else 'ĐỎ '} {nhan:26} giết {len(chet)}/{len(phai_chet)}"
              " trong phai_chet")
        if not ok:
            xau.append(f"{nhan}: chết {sorted(chet)}, phải chết {sorted(phai_chet)}")

    print(f"\nSỐ LIỆU:  ca {n}  ·  đột biến {len(DOT_BIEN)}")
    if xau:
        print("TỔNG: ĐỎ")
        for x in xau:
            print(f"  - {x}")
        return 1
    print("TỔNG: ĐẠT")
    return 0


if __name__ == "__main__":
    sys.exit(main())
