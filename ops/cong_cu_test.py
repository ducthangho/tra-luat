#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""T1..T8 + chính sách canary (#290, sha256 b1b7e3b0…) cho cong_cu.py+cai_cong_cu.sh. Gọi
CHÍNH lệnh qua subprocess (không import) — doctrine `lease_publish_test.py`."""
from __future__ import annotations

import datetime as _dt
import json, os, runpy, shutil, subprocess, sys, tempfile, time
from pathlib import Path

# #671 (gộp nợ CONG-CU-TEST-EP-UTF8 của #570) — ÉP UTF-8 TRƯỚC MỌI `print`, cho CHÍNH tệp này và
# cho MỌI tiến trình con/cháu. Đo 27-09-2026 (Linux, `PYTHONIOENCODING=ascii` cho con): `t29`, `t42`,
# `t45` chết `tin_dung_gia` vì cháu in chữ Việt ra stdout ASCII; chạy tay trên Windows (cp1252/cp1258)
# ĐỎ oan, còn CI che mất vì tự đặt hai biến này. Đặt vào `os.environ` chứ không vá từng lời gọi. Phạm vi
# ĐÃ ĐO (AST, mọi Call có `env=`): giá trị là `moi_truong(…)`, `dict(os.environ, …)`, `{**os.environ, …}`, hoặc
# biến/`dict(biến, …)` truy tay về các dạng ấy hay `None` (= thừa kế) — CỐ Ý không ghi số đếm (trôi mỗi lượt); lời
# gọi không `env=` thì thừa kế. Điểm phóng viết SAU phải tự giữ điều đó — chưa ca nào khoá.
# `t61` đo từng vế trong một tiến trình con CỐ Ý ép ASCII, nên nó có răng cả khi CI đã đặt sẵn.
_BIEN_UTF8 = (("PYTHONIOENCODING", "utf-8"), ("PYTHONUTF8", "1"))


def _ep_utf8(moi_truong_con=os.environ) -> None:
    for luong in (sys.stdout, sys.stderr):
        if hasattr(luong, "reconfigure"):
            luong.reconfigure(encoding="utf-8", errors="backslashreplace")
    for ten, gia_tri in _BIEN_UTF8:
        moi_truong_con[ten] = gia_tri


_ep_utf8()

# #671 (đo 30-09-2026 trên Windows local, Python 3.13, locale cp1258) — ép CON ghi UTF-8 CHƯA ĐỦ:
# CHA vẫn giải `subprocess.run(..., text=True)` bằng mã hoá LOCALE, nên con in UTF-8 đúng mà cha đọc
# vỡ (`UnicodeDecodeError: 'charmap' … 0x90`) ⇒ `t29`/`t39`/`t42`/`t45` ĐỎ, 47/51. Linux không thấy vì
# locale ở đó đã là UTF-8. Đặt `PYTHONUTF8` lúc chạy KHÔNG đổi chế độ của tiến trình ĐANG chạy, nên
# chạy làm `__main__` ngoài chế độ UTF-8 thì phóng LẠI chính mình với `-X utf8` — đúng chế độ CI đang
# chạy (CI đặt `PYTHONUTF8=1`, nên CI không bao giờ đi nhánh này). Hợp đồng lần phóng lại, mỗi vế một
# chốt: chỉ ở `__main__` (`t61` (e)); mã thoát đi qua, `-B` còn, dấu không sót, `-X utf8=0` ra UTF-8 sau
# đúng MỘT lần, đã phóng mà vẫn ngoài UTF-8 thì DỪNG (không lặp), nguồn stdin không đọc lại được thì DỪNG
# thay vì chạy chương trình RỖNG ra `rc=0` (`t62` (1)–(6); `-c` đi cùng chốt `isfile`, không ca riêng).
# Lượt 6 — MỒ CÔI (`t64`; `8757a84`: giết bao ⇒ bộ ca sống tiếp, SIGTERM bộ ca ⇒ bao 241): POSIX `os.execve` (CÙNG PID);
# Windows tự gán Job Object KILL_ON_JOB_CLOSE TRƯỚC khi phóng; không gắn được ⇒ vẫn chạy, in `CANH_BAO_MO_COI`.
_MA_TU_KIEM_UTF8, _DAU_PHONG_LAI = 5, "CONG_CU_TEST_DA_PHONG_LAI"
_DA_PHONG_LAI = os.environ.pop(_DAU_PHONG_LAI, None) == "1"


def _phong_lai(lenh, env, nen=os.name, k32=None, popen=subprocess.Popen, execve=os.execve):
    if nen != "nt":
        for luong in (sys.stdout, sys.stderr):   # xả đệm rồi exec — KHÔNG trở về
            if luong is not None:                # None = fd 1/2 đóng lúc gọi (`>&-`, daemon): đừng nổ trước khi phóng
                luong.flush()
        return execve(lenh[0], lenh, env)
    try:
        import ctypes
        # JOBOBJECT_EXTENDED_LIMIT_INFORMATION trải phẳng dưới: x64 144 byte, x86 112; cờ LimitFlags ở offset 16.
        u32, sz, vp, i = ctypes.c_uint32, ctypes.c_size_t, ctypes.c_void_p, ctypes.c_int
        k32 = k32 or ctypes.WinDLL("kernel32", use_last_error=True)
        _GioiHan = type("_GioiHan", (ctypes.Structure,), {"_fields_": [("tg", ctypes.c_int64 * 2), ("co", u32), ("ws", sz * 2),
                        ("sl", u32), ("aff", sz), ("uu", u32 * 2), ("io", ctypes.c_uint64 * 6), ("mem", sz * 4)]})
        for f, kq, ds in ((k32.CreateJobObjectW, vp, (vp, vp)), (k32.SetInformationJobObject, i, (vp, i, vp, u32)),
                          (k32.AssignProcessToJobObject, i, (vp, vp)), (k32.GetCurrentProcess, vp, ())):
            f.restype, f.argtypes = kq, ds  # khai KIỂU: HANDLE mặc định `c_int` cắt còn 32 bit
        gh, job = _GioiHan(co=0x2000), k32.CreateJobObjectW(None, None)  # 0x2000 = LIMIT_KILL_ON_JOB_CLOSE
        if not (job and k32.SetInformationJobObject(job, 9, ctypes.byref(gh), ctypes.sizeof(gh))  # 9 = Extended
                and k32.AssignProcessToJobObject(job, k32.GetCurrentProcess())):
            raise OSError(f"GetLastError={getattr(ctypes, 'get_last_error', int)()}")
    except Exception as ex:  # noqa: BLE001 — không chặn: vẫn chạy, nhưng NÓI ra
        if sys.stderr is not None:  # stderr None (pythonw/không std handle) ⇒ vẫn phóng, không nổ khi báo
            sys.stderr.write(f"cong_cu_test: CANH_BAO_MO_COI — không gắn được Job Object ({type(ex).__name__}: {ex}); "
                             "harness giết tiến trình này thì bản phóng lại MỒ CÔI — có hạn chót thì đặt PYTHONUTF8=1\n")
    return popen(lenh, env=env).wait()


if __name__ == "__main__" and not sys.flags.utf8_mode:
    _nguon = globals().get("__file__") or ""
    if _DA_PHONG_LAI or not os.path.isfile(_nguon):
        sys.exit("cong_cu_test: KHONG_PHONG_LAI — " + ("đã phóng một lần mà vẫn ngoài UTF-8" if _DA_PHONG_LAI
                 else f"nguồn {_nguon!r} không đọc lại được") + "; chạy `python -X utf8 …` hoặc đặt PYTHONUTF8=1")
    sys.exit(_phong_lai([sys.executable, "-X", "utf8", *sys.orig_argv[1:]], {**os.environ, _DAU_PHONG_LAI: "1"}))

import yaml

HERE = Path(__file__).resolve().parent
GOC = HERE.parent
SCRIPT = HERE / "cong_cu.py"
BASH_NEN = HERE / "bash_nen.py"
# Chinh tep nay, lam DUONG DAN — de dot bien `bn_ban_kinh_giau_ly_do` co cho cam ma KHONG
# phai patch `GOC`. Do duoc 20-09-2026: patch `GOC` keo `t6` chet `tin_dung_gia` (cay tam
# thieu thu `t6` can) va lam ban kinh KHONG DOC DUOC — dung bay "co lap 3 ho" ghi o dau
# `DOT_BIEN`: moi dot bien chi duoc patch DUNG mot bien.
TEP_TEST = HERE / "cong_cu_test.py"
CAI_SH = HERE / "cai_cong_cu.sh"
sys.path.insert(0, str(HERE))
import lease_publish_test as lpt  # noqa: E402 — tái dùng _goi_actionlint_gia/_bam_tep
import bash_nen  # noqa: E402 — MỘT bộ giải `bash` dùng chung (#570)


def _bash_dung_duoc(viec: str) -> str:
    """`bash` ĐÃ CHỨNG MINH làm được việc, hoặc ném kèm CHẨN ĐOÁN.

    KHÔNG `shutil.which("bash")`. Đo 19/20-09-2026 trên Windows thật (#570): nó trả
    `C:\\Windows\\system32\\bash.EXE` — bộ phóng WSL — và ở đây nó làm
    `./cai_cong_cu.sh` TREO 60s rồi giết cả suite trong `batch_behavior_test()`, TRƯỚC
    vòng lặp ca. Tức tệp này CHƯA TỪNG chạy được trên Windows, và năm ca `T23`-`T27`
    sinh ra để đo Windows thì chưa từng đo ở đó — đúng bệnh "ca có MẶT khác ca có ĐO".
    """
    duong, chan_doan = bash_nen.tim_bash()
    if not duong:
        raise BoQuaMoiTruong(
            f"KHÔNG ĐO ĐƯỢC: không `bash` nào làm được việc cho {viec}. Chẩn đoán: "
            + "; ".join(f"{c['duong']}: {c['ly_do']}" for c in chan_doan)
            or "không có ứng viên nào")
    return duong


CA: list = []

class BoQuaMoiTruong(Exception):
    """Máy chạy test thiếu tool THẬT cho ca này — KHÔNG_ĐO_ĐƯỢC, khác ca ĐỎ, đếm riêng."""

def ca(fn):
    CA.append(fn); return fn

class TinHieuChotCa(AssertionError):
    """Tín hiệu CHỐT của một ca — CHỈ `bang()` phát ra nó.

    VÌ SAO CÓ (cross-review lượt 4 `R4-04`, đo được, không phải lo xa): bộ chấm
    đột biến cũ gom MỌI Exception thành "chết" rồi cấp tín dụng giết. Đo:
    đột biến `t13_mat_requiredness_khi_tool_bien_mat` bỏ `**goc` nên aggregator
    ném `KeyError: 'chinh_sach'`, tiến trình con chết với stdout RỖNG, và ca đích
    chết ở `json.loads(out)` bằng `JSONDecodeError` — CHƯA TỪNG chạy tới `bang()`.
    Runner vẫn in "ok … giết đúng". Tức mutant bị giết bởi một lỗi VÔ CAN.

    Chốt đúng phải là thứ mã triển khai KHÔNG GIẢ ĐƯỢC. Một `AssertionError`
    trần thì bất kỳ `except Exception: raise AssertionError(...)` nào cũng dựng
    lên được — và `CLAUDE.md` ghi rằng bản vá vòng một của một bộ phân hạng khác
    đã thua đúng cách ấy, bởi một dòng viết với ý định TỐT. Nên tín hiệu ở đây là
    một LỚP RIÊNG, cộng dấu TÊN CA: assertion của ca KHÁC cũng là tín dụng giả.
    """


class LoiDungCa(Exception):
    """Hỏng ở bước DỰNG/KHỞI CHẠY/GIẢI MÃ của một ca — KHÔNG phải tín hiệu chốt.

    VÌ SAO CÓ (cross-review lượt 5 `R5-01`, đo được): lớp `TinHieuChotCa` ở trên
    chỉ chứng minh lỗi đi qua `bang()` CỦA CA ĐANG CHẠY. Nó KHÔNG chứng minh
    **assertion nghiệp vụ đích** đã chạy. `t22` dùng chính `bang()` để kiểm tiến
    trình con khởi chạy được, TRƯỚC khi đọc bốn kết quả A/B/C/D. Reviewer bơm duy
    nhất `raise KeyError("rv5_unrelated_crash")` vào đầu `_bash_windows`: con chết
    rc=1, stdout rỗng, KHÔNG tới phép kiểm chọn Git Bash — mà `_chay_1_ca` vẫn trả
    `giet_that`. Chạy toàn bán kính: CHỈ `t22` chết, 0 ca `tin_dung_gia`; nên cả
    phép kiểm TÊN CA lẫn bán kính 1/23 đều không ngăn được tín dụng này.

    Tức bản vá `R4-04` đóng được PHẢN CHỨNG CỤ THỂ mà KHÔNG đóng được LỚP — đúng
    lớp lỗi "vá dòng được gọi tên, bỏ sót hình dạng của nó" mà `CLAUDE.md` chép
    lại nhiều lần, lần này nằm TRONG chính bản vá dựng ra để chặn nó.

    RANH GIỚI, và nó KHÔNG suy được từ mã thoát (reviewer cảnh báo thẳng: "hạ mọi
    rc khác 0 thành tín dụng giả sẽ làm mất tín dụng hợp lệ của ca kiểm mã thoát"):
    · `chay(...)`/`cai_cong_cu.sh` là SẢN PHẨM đang bị đo ⇒ `rc` là hợp đồng của
      nó ⇒ dùng `bang()`, và `t7` `t9` `t11` `t20` sống bằng đúng những `rc` ấy.
    · đoạn `python -c` do CHÍNH bộ test soạn ra để gọi vào sản phẩm là GIÀN GIÁO
      ⇒ dùng `dung()`.
    Người viết ca khai ranh giới ấy tại chỗ gọi; không có luật máy nào đoán hộ.
    """


_CA_DANG_CHAY = None


def bang(dk, msg):
    """Chốt NGHIỆP VỤ của ca đang chạy. Hỏng ở đây = đột biến bị giết THẬT.

    KHÔNG có tham số `chot=` để đặt tên từng assertion, dù reviewer có gợi ý. Bản
    nháp đã thêm một tham số như thế rồi KHÔNG chỗ gọi nào dùng — tức đúng thứ tệp
    này tồn tại để tố cáo: một thứ CÓ MẶT mà không có KHẢ NĂNG nào. Phép phân biệt
    thật sự nằm ở việc người viết chọn `bang()` hay `dung()`; `DOT_BIEN` neo theo
    CA chứ không theo chốt, nên một nhãn chốt lúc này không ai đọc. Thêm lại khi
    có phép đo cần nó, kèm phản chứng cho chính nhãn ấy."""
    if not dk:
        ex = TinHieuChotCa(msg)
        ex.ca_nguon = _CA_DANG_CHAY
        raise ex

def dung(dk, msg):
    """Chốt GIÀN GIÁO (dựng fixture / khởi chạy tiến trình con / giải mã đầu ra).

    Hỏng ở đây nghĩa là ca KHÔNG ĐO ĐƯỢC thuộc tính của nó — bộ phân hạng phải
    đọc thành `tin_dung_gia`, KHÔNG phải `giet_that`. `main()` vẫn tính nó là ĐỎ
    của suite: "không đo được" khác "đạt", và cũng khác "đột biến bị bắt"."""
    if not dk:
        raise LoiDungCa(msg)

def chay(*args, env=None):
    p = subprocess.run([sys.executable, str(SCRIPT), *args], env=env, cwd=GOC,
                        capture_output=True, text=True, timeout=60)
    return p.returncode, p.stdout, p.stderr

def moi_truong(*truoc, **them):
    e = dict(os.environ)
    if truoc: e["PATH"] = os.pathsep.join([str(x) for x in truoc] + [e.get("PATH", "")])
    e.update(them); return e

def ghi_ban_ke(tmp, cc):
    p = tmp / "ban_ke.yaml"
    p.write_text(yaml.safe_dump({"schema_version": 1, "cong_cu": cc}), encoding="utf-8")
    return p

def bin_gia(thu_muc, ten, than):
    thu_muc.mkdir(parents=True, exist_ok=True)
    p = thu_muc / ten
    p.write_text(than, encoding="utf-8"); p.chmod(0o755)
    return p

def mot_probe(ten, regex=r"(\d+\.\d+\.\d+(?:[-+][0-9A-Za-z.-]+)?)", expected_rc=None):
    pb = {"ten": "mac_dinh", "lenh": [ten, "--version"], "regex": regex}
    if expected_rc is not None: pb["expected_rc"] = expected_rc
    return [pb]

def bk_don(tmp, ten, than, bat_buoc=True, ban_ghim=None):
    """1 tool giả + 1 bản kê tối giản -> (đường_bản_kê, env trỏ PATH tới nó)."""
    d = tmp / f"bin-{ten}"; bin_gia(d, ten, than)
    bk = ghi_ban_ke(tmp, {ten: {"bat_buoc": bat_buoc, "ban_ghim": ban_ghim, "probe": mot_probe(ten)}})
    return bk, moi_truong(d)

@ca
def t1_thieu_bat_buoc_khac_ma_voi_do():
    """T1: thiếu bắt buộc ⇒ KHÔNG_ĐO_ĐƯỢC mã RIÊNG, khác mã ĐỎ."""
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        bk0 = ghi_ban_ke(tmp, {"vang-t1": {"bat_buoc": True, "ban_ghim": None,
                                            "probe": mot_probe("vang-t1-bin")}})
        rc_vang, out_vang, _ = chay("kiem-tra", "--ban-ke", str(bk0), env=moi_truong())
        bk1, env1 = bk_don(tmp, "sai-ban-t1", "#!/bin/sh\necho 0.0.0\n", ban_ghim="9.9.9")
        rc_do, _, _ = chay("kiem-tra", "--ban-ke", str(bk1), env=env1)
        bang(rc_vang != 0 and rc_do != 0, f"cả hai phải khác 0: vắng={rc_vang} sai_bản={rc_do}")
        bang(rc_vang != rc_do, f"KHÔNG_ĐO_ĐƯỢC(rc={rc_vang}) và ĐỎ(rc={rc_do}) CHUNG mã")
        bang("khong khoi chay" in out_vang, f"không phân biệt được lỗi khởi chạy: {out_vang}")

@ca
def t2_canary_thieu_shellcheck_phai_SUY_GIAM():
    """T2: actionlint CÓ, shellcheck VẮNG ⇒ canary ĐỎ (SUY_GIẢM), không sạch."""
    al = shutil.which("actionlint")
    if not al:
        raise BoQuaMoiTruong("actionlint không có trên PATH — cần HÀNH VI THẬT, không giả "
            "lập được. Chạy sau khi `ops/cai_cong_cu.sh actionlint` cài để có bằng chứng dương.")
    # Ba trạng thái: công cụ bắt buộc đã ĐỎ NGOÀI vùng cô lập là thiếu MÔI TRƯỜNG (vd container
    # dev không có jsonschema) ⇒ KHÔNG_ĐO_ĐƯỢC, không phải ĐỎ. Chỉ khi nó ĐẠT ngoài mà ĐỎ trong
    # vùng cô lập thì vùng cô lập của chính ca này hỏng — đó mới là ĐỎ (chốt ở cuối ca).
    rc0, out0, _ = chay("kiem-tra", "--json")
    try:
        # `.get("ten")`: ca này không đo vân tay `ten` (việc của t8) — đừng chết theo đột biến t8.
        hong_ngoai = [c.get("ten") for c in json.loads(out0)["cong_cu"]
                      if c["bat_buoc"] and c["trang_thai"] != "DAT"]
    except (ValueError, KeyError, TypeError):
        raise BoQuaMoiTruong(f"KHÔNG ĐO ĐƯỢC T2: kiem-tra ngoài vùng cô lập không trả JSON (rc={rc0})")
    if hong_ngoai:
        raise BoQuaMoiTruong(f"KHÔNG ĐO ĐƯỢC T2: máy này thiếu công cụ bắt buộc {hong_ngoai} "
                             f"ngay ngoài vùng cô lập — cài rồi đo lại")
    with tempfile.TemporaryDirectory() as tmp:
        # CÁCH CÔ LẬP ĐÃ ĐỔI (đo 02-09-2026, run 33631185695 lane windows-latest). Bản cũ dựng
        # PATH chỉ có bản sao actionlint rồi symlink git/rg/bash vào — sống được khi bản kê
        # chỉ có actionlint (tĩnh), chết ngay khi #446 thêm binary thật: symlink tới `.exe`
        # trên Windows chạy với "thư mục ứng dụng" là thư mục symlink nên thiếu DLL
        # (git/bash rc=0xC0000135), còn rg là shim choco đọc `.shim` cạnh nó (rc=-1). Tức
        # git/rg/bash ĐỎ vì lý do vô can, tổng ĐỎ bất kể canary, và mutant canary sống sót.
        # Nay GIỮ PATH THẬT, chỉ che shellcheck: một DECOY tên `shellcheck[.exe]` đứng đầu
        # PATH. Decoy là bản sao actionlint — tĩnh, tự đứng, chắc chắn KHÔNG phải shellcheck:
        # probe `shellcheck --version` không parse ra `version: x.y.z` ⇒ shellcheck != DAT;
        # actionlint thật tìm thấy decoy trước, gọi nó thất bại ⇒ không có SC1003. Cả hai nền
        # cùng một cơ chế, không symlink, không đụng thư mục hệ thống.
        che = Path(tmp) / "che-sc"
        che.mkdir()
        decoy = che / ("shellcheck" + Path(al).suffix)
        shutil.copy2(al, decoy); decoy.chmod(0o755)
        path_moi = str(che) + os.pathsep + os.environ.get("PATH", "")
        thay = shutil.which("shellcheck", path=path_moi)
        bang(thay and Path(thay).resolve() == decoy.resolve(),
             f"decoy không đứng đầu PATH ⇒ ca này không còn đo cái nó nói là đo: {thay!r}")
        rc, out, _ = chay("kiem-tra", "--json", env=dict(os.environ, PATH=path_moi))
        bang(rc != 0, f"shellcheck bị che mà tổng vẫn ĐẠT (rc=0):\n{out[:500]}")
        bc = json.loads(out)
        # Điều ca này ĐO: canary ĐỎ, không sạch. Hai thông điệp đều là ĐỎ — `SUY_GIAM` khi bộ
        # đo thấy shellcheck != DAT (đường bình thường với decoy), và "du shellcheck co mat"
        # khi một khuyết tật KHÁC của bộ đo (vd parse hụt, việc của t10) làm decoy thành DAT.
        # Không đòi riêng SUY_GIAM: ca sẽ chết theo đột biến t10 thay vì theo đột biến của nó.
        cn = [c for c in bc["canary"] if c.get("ten") == "actionlint_shellcheck"]
        bang(cn and cn[0]["trang_thai"] == "DO", f"canary phải ĐỎ khi shellcheck bị che: {cn}")
        bang("SUY_GIAM" in cn[0]["chi_tiet"] or "du shellcheck co mat" in cn[0]["chi_tiet"],
             f"canary ĐỎ nhưng không nói vì shellcheck: {cn[0]['chi_tiet']!r}")
        # rc≠0 phải đến TỪ canary: mọi công cụ bắt buộc phải ĐẠT, còn không thì ca này
        # xanh nhờ một lỗi khác và mất răng với chính đột biến nó sinh ra để bắt.
        vo_can = [(c.get("ten"), c["chi_tiet"]) for c in bc["cong_cu"]
                  if c["bat_buoc"] and c["trang_thai"] != "DAT"]
        bang(not vo_can, f"công cụ bắt buộc ĐỎ vì lý do vô can, tổng đỏ không còn đo canary: {vo_can}")

@ca
def t3_du_cong_cu_dung_ban_khong_canh_bao_thua():
    """T3 (chiều BẮT OAN): đủ công cụ đúng bản ⇒ ĐẠT, không cảnh báo thừa. Bản kê KHÔNG
    khai `canary` — cô lập khỏi mutation của T2."""
    with tempfile.TemporaryDirectory() as tmp:
        bk, env = bk_don(Path(tmp), "on-dinh-t3", "#!/bin/sh\necho 3.1.4\n", ban_ghim="3.1.4")
        rc, out, _ = chay("kiem-tra", "--ban-ke", str(bk), "--json", env=env)
        bang(rc == 0, f"đủ công cụ đúng bản mà rc={rc}:\n{out}")
        bang('"trang_thai": "DO"' not in out and '"trang_thai": "KHONG_DO_DUOC"' not in out,
             f"cảnh báo THỪA khi mọi thứ đúng: {out}")

@ca
def t4_sai_ban_phai_neu_ro_ban_mong_doi_va_ban_thay():
    """T4: có mặt nhưng SAI BẢN ⇒ ĐỎ, nêu cả bản mong đợi lẫn bản thấy."""
    with tempfile.TemporaryDirectory() as tmp:
        bk, env = bk_don(Path(tmp), "sai-ban-t4", "#!/bin/sh\necho 1.0.0\n", ban_ghim="2.0.0")
        rc, out, _ = chay("kiem-tra", "--ban-ke", str(bk), env=env)
        bang(rc == 2, f"sai bản phải là ĐỎ (2), được rc={rc}\n{out}")
        bang("2.0.0" in out and "1.0.0" in out, f"thiếu bản mong đợi/bản thấy: {out}")

@ca
def t5_cai_cong_cu_khong_thoat_som_khi_da_co_tren_PATH():
    """T5: `cai_cong_cu.sh` KHÔNG thoát sớm khi công cụ đã có trên PATH."""
    bash = _bash_dung_duoc("ops/cai_cong_cu.sh")
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        path_gia = tmp / "path-gia"  # actionlint SAI bản đã có sẵn TRƯỚC khi cài
        bin_gia(path_gia, "actionlint", "#!/bin/sh\necho 9.9.9\n")
        goi = lpt._goi_actionlint_gia(tmp, "1.7.7", "#!/bin/sh\necho 1.7.7\n")
        env = moi_truong(path_gia, AL_GOI=str(goi), AL_SHA256=lpt._bam_tep(goi),
                          AL_DICH=str(tmp / "dich"))
        p = subprocess.run([bash, str(CAI_SH), "actionlint"], env=env, cwd=GOC,
                            capture_output=True, text=True, timeout=120)
        bang(p.returncode == 0, f"cai_cong_cu.sh thất bại: rc={p.returncode}\n{p.stdout}\n{p.stderr}")
        bang('"1.7.7"' in p.stdout and '"trang_thai": "DAT"' in p.stdout,
             f"đo lại phải thấy bản 1.7.7 (không phải 9.9.9 có sẵn) — bằng chứng KHÔNG "
             f"thoát sớm:\n{p.stdout}")

@ca
def t6_ci_kiem_ban_ke_truoc_moi_test_nang():
    """T6: trước G5 chỉ được có allowlist SETUP theo cấu trúc, không chọn trước tên test."""
    d = yaml.safe_load((GOC / ".github" / "workflows" / "ci.yml").read_text(encoding="utf-8"))
    buoc = (d.get("jobs", {}).get("gate", {}) or {}).get("steps", [])
    idx_kiem = [i for i, b in enumerate(buoc)
                if str(b.get("name", "")).startswith("G5 ")
                and "ops/cong_cu.py kiem-tra" in str(b.get("run", ""))]
    bang(len(idx_kiem) == 1, f"G5 phải có đúng một lần, thấy {idx_kiem}")
    lenh_setup = {
        "Force LF checkout (hash parity với manifest)": (
            "git config --global core.autocrlf false", "git config --global core.eol lf",
            "git config --global core.abbrev 7"),
        "cài PyYAML + jsonschema (cổng đăng lease + validator verdict cần)": (
            "python -m pip install --quiet PyYAML==6.0.3 jsonschema==4.26.0",),
        "cài actionlint cho G5": ("bash ops/cai_actionlint.sh",),
        "cài shellcheck cho G5 (cài xong đo lại)": ("bash ops/cai_cong_cu.sh shellcheck",),
        "cài rg cho G5 (cài xong đo lại)": ("bash ops/cai_cong_cu.sh rg",),
    }
    uses_setup = {"actions/checkout@v4", "actions/setup-python@v5"}
    for i, b in enumerate(buoc[:idx_kiem[0]]):
        if b.get("uses") in uses_setup and "run" not in b: continue
        lenh = tuple(x.strip() for x in str(b.get("run", "")).splitlines()
                     if x.strip() and not x.lstrip().startswith("#"))
        bang(lenh_setup.get(b.get("name")) == lenh,
             f"bước {i + 1} trước G5 không thuộc allowlist setup: '{b.get('name')}' / {lenh}")
    sc_buoc = [b for b in buoc[:idx_kiem[0]] if str(b.get("name", "")).startswith("cài shellcheck")]
    bang(len(sc_buoc) == 1 and "if" not in sc_buoc[0], "CI phải cài shellcheck vô điều kiện trên cả hai nền")
    cai_sc = yaml.safe_load((GOC / "ops/cong_cu.yaml").read_text(encoding="utf-8"))["cong_cu"]["shellcheck"]["cai"]
    bang(all((cai_sc.get(n) or {}).get("lenh") for n in ("linux", "windows")), "thiếu công thức cài shellcheck Linux/Windows")

@ca
def t7_hai_duong_goi_khac_ban_phai_bao_khong_im():
    """T7: ≥2 đường probe khác bản ⇒ ĐỎ, ĐỘC LẬP với `ban_ghim` (ca thật: `ruff` nhị phân
    0.15.8 vs `python3 -m ruff` 0.16.4, cùng máy)."""
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        bin_gia(tmp / "a", "hai-a-t7", "#!/bin/sh\necho 1.0.0\n")
        bin_gia(tmp / "b", "hai-b-t7", "#!/bin/sh\necho 2.0.0\n")
        bk = ghi_ban_ke(tmp, {"hai-duong-t7": {"bat_buoc": False, "ban_ghim": None, "probe": [
            {"ten": "a", "lenh": ["hai-a-t7", "--version"], "regex": r"(\d+\.\d+\.\d+)"},
            {"ten": "b", "lenh": ["hai-b-t7", "--version"], "regex": r"(\d+\.\d+\.\d+)"}]}})
        rc, out, _ = chay("kiem-tra", "--ban-ke", str(bk), env=moi_truong(tmp / "a", tmp / "b"))
        bang(rc == 2, f"hai đường khác bản phải là ĐỎ (rc=2), được rc={rc}\n{out}")
        bang("1.0.0" in out and "2.0.0" in out, f"thiếu CẢ HAI bản thấy: {out}")

@ca
def t8_van_tay_cong_cu_co_trong_ho_so():
    """T8: mọi bản ghi `cong_cu` trong báo cáo JSON mang vân tay (khoá `ten`+`ban_thay`)."""
    with tempfile.TemporaryDirectory() as tmp:
        bk, env = bk_don(Path(tmp), "van-tay-t8", "#!/bin/sh\necho 1.2.3\n", ban_ghim="1.2.3")
        rc, out, _ = chay("kiem-tra", "--ban-ke", str(bk), "--json", env=env)
        bc = json.loads(out)
        bang(bc["cong_cu"], f"báo cáo rỗng: {out}")
        for kq in bc["cong_cu"]:
            bang("ten" in kq and kq["ten"], f"thiếu vân tay 'ten': {kq}")
            bang("ban_thay" in kq, f"thiếu vân tay 'ban_thay': {kq}")
        bang(bc["cong_cu"][0]["ban_thay"].get("mac_dinh") == "1.2.3", f"'ban_thay' sai: {bc}")

@ca
def t9_probe_rc_phai_hop_le_ke_ca_khong_ghim_va_mixed():
    """V1: rc mặc định chỉ 0; nới phải khai từng probe; một probe tốt không che probe hỏng."""
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp); d = tmp / "bin"
        bin_gia(d, "rc7-t9", "#!/bin/sh\necho 1.2.3\nexit 7\n")
        bk = ghi_ban_ke(tmp, {"x": {"bat_buoc": True, "ban_ghim": None,
                                     "probe": mot_probe("rc7-t9")}})
        rc, out, _ = chay("kiem-tra", "--ban-ke", str(bk), env=moi_truong(d))
        bang(rc == 2 and "rc=7" in out, f"rc hỏng không ghim phải ĐỎ: rc={rc}\n{out}")
        bk = ghi_ban_ke(tmp, {"x": {"bat_buoc": True, "ban_ghim": None,
                                     "probe": mot_probe("rc7-t9", expected_rc=7)}})
        bang(chay("kiem-tra", "--ban-ke", str(bk), env=moi_truong(d))[0] == 0,
             "expected_rc riêng của probe hợp lệ bị chặn oan")
        bin_gia(d, "ok-t9", "#!/bin/sh\necho 1.2.3\n")
        pbs = mot_probe("ok-t9") + [{**mot_probe("rc7-t9")[0], "ten": "hong"}]
        bk = ghi_ban_ke(tmp, {"x": {"bat_buoc": True, "ban_ghim": None, "probe": pbs}})
        bang(chay("kiem-tra", "--ban-ke", str(bk), env=moi_truong(d))[0] == 2,
             "probe tốt đã che probe rc hỏng trong cùng tool")

@ca
def t10_probe_phai_parse_va_bat_tron_token():
    """V1: output không parse được và tiền tố 1.7.7 của 1.7.7-rc1 đều phải ĐỎ."""
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        bk, env = bk_don(tmp, "vo-nghia-t10", "#!/bin/sh\necho khong-phai-ban\n")
        bang(chay("kiem-tra", "--ban-ke", str(bk), env=env)[0] == 2,
             "probe chạy rc=0 nhưng không parse được đã thành ĐẠT")
        bk, env = bk_don(tmp, "tien-to-t10", "#!/bin/sh\necho 1.7.7-rc1\n",
                         ban_ghim="1.7.7")
        # Cố ý dùng parser cũ để chứng minh bộ đo tự bắt việc cắt tiền tố.
        d = yaml.safe_load(bk.read_text(encoding="utf-8")); d["cong_cu"]["tien-to-t10"]["probe"][0]["regex"] = r"^(\d+\.\d+\.\d+)"
        bk.write_text(yaml.safe_dump(d), encoding="utf-8")
        bang(chay("kiem-tra", "--ban-ke", str(bk), env=env)[0] == 2,
             "1.7.7-rc1 đã bị cắt thành tiền tố ghim 1.7.7")

@ca
def t11_ban_ghim_rong_bi_tu_choi_nhung_null_hop_le():
    """V3 + đối chứng: chuỗi rỗng là schema lỗi; chỉ null mới là không ghim."""
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp); bk, env = bk_don(tmp, "ghim-t11", "#!/bin/sh\necho 9.9.9\n")
        d = yaml.safe_load(bk.read_text(encoding="utf-8")); d["cong_cu"]["ghim-t11"]["ban_ghim"] = ""
        bk.write_text(yaml.safe_dump(d), encoding="utf-8")
        rc, _, err = chay("kiem-tra", "--ban-ke", str(bk), env=env)
        bang(rc == 1 and "ban_ghim" in err, f"ghim rỗng không bị validation từ chối: {rc}/{err}")
        d["cong_cu"]["ghim-t11"]["ban_ghim"] = None; bk.write_text(yaml.safe_dump(d), encoding="utf-8")
        bang(chay("kiem-tra", "--ban-ke", str(bk), env=env)[0] == 0,
             "null (không ghim hợp lệ) bị chặn oan")

@ca
def t12_vang_chinh_sach_canary_mac_dinh_blocking():
    """Y2: canary vắng chính sách phải fail-close thành blocking."""
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp); d = tmp / "bin"; bin_gia(d, "actionlint", "#!/bin/sh\necho 1.7.7\n")
        bk = ghi_ban_ke(tmp, {"actionlint": {"bat_buoc": True, "ban_ghim": "1.7.7",
            "probe": mot_probe("actionlint"), "canary": "fixture-khong-ton-tai-t12"}})
        rc, out, _ = chay("kiem-tra", "--ban-ke", str(bk), env=moi_truong(d))
        bang(json.loads(out)["trang_thai_tong"] == "KHONG_DO_DUOC" and '"chinh_sach": "blocking"' in out,
             f"canary bắt buộc thiếu fixture bị nuốt: {rc}\n{out}")
        sai = yaml.safe_load(bk.read_text(encoding="utf-8")); sai["cong_cu"]["actionlint"]["chinh_sach"] = "khac"
        bk.write_text(yaml.safe_dump(sai), encoding="utf-8"); rc, _, err = chay("kiem-tra", "--ban-ke", str(bk), env=moi_truong(d))
        bang(rc == 1 and "blocking|advisory" in err, f"schema nhận chính sách lạ: {rc}/{err}")
        bk = ghi_ban_ke(tmp, {"optional-t12": {"bat_buoc": False, "ban_ghim": None,
                                                "probe": mot_probe("khong-co-t12")}})
        bang(chay("kiem-tra", "--ban-ke", str(bk), env=moi_truong(d))[0] == 0,
             "tool optional không khai canary bị chặn oan")

@ca
def t13_actionlint_bien_mat_giua_probe_va_canary():
    """V2: tool DAT ở probe nhưng biến mất trước canary phải kéo tổng thành KHÔNG_ĐO_ĐƯỢC."""
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp); d = tmp / "bin"
        bin_gia(d, "actionlint", "#!/bin/sh\ncase \"$1\" in -version|--version) echo 1.7.7; /bin/rm -- \"$0\"; exit 0;; esac\n")
        bk = ghi_ban_ke(tmp, {"actionlint": {"bat_buoc": True, "ban_ghim": "1.7.7",
            "probe": mot_probe("actionlint"), "canary": "actionlint_shellcheck", "chinh_sach": "blocking"}})
        rc, out, _ = chay("kiem-tra", "--ban-ke", str(bk),
                          env=dict(os.environ, PATH=str(d), CONG_CU_BASH=_bash_dung_duoc("canary") or ""))
        bang(json.loads(out)["trang_thai_tong"] == "KHONG_DO_DUOC" and "khong goi duoc" in out,
             f"canary mất executable bị nuốt: {rc}\n{out}")

@ca
def t14_advisory_giu_trang_thai_that_nhung_khong_keo_tong():
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp); d = tmp / "bin"; bin_gia(d, "actionlint", "#!/bin/sh\necho 1.7.7\n")
        bk = ghi_ban_ke(tmp, {"actionlint": {"bat_buoc": True, "ban_ghim": "1.7.7", "probe": mot_probe("actionlint"), "canary": "vang-t14", "chinh_sach": "advisory"}})
        rc, out, _ = chay("kiem-tra", "--ban-ke", str(bk), env=moi_truong(d)); bc = json.loads(out); cn = bc["canary"][0]
        bang(rc == 0 and bc["trang_thai_tong"] == "DAT", f"advisory đã kéo tổng: {out}")
        bang(cn["trang_thai"] == "KHONG_DO_DUOC" and cn["chinh_sach"] == "advisory", f"JSON che trạng thái thật: {out}")

@ca
def t15_blocking_du_cong_cu_phai_DAT_khong_bat_oan():
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp); d = tmp / "bin"
        bin_gia(d, "actionlint", '#!/bin/sh\n[ "$1" = --version ] && { echo 1.7.7; exit; }; echo SC1003; exit 1\n'); bin_gia(d, "shellcheck", "#!/bin/sh\necho 'version: 0.11.0'\n")
        cc = {"actionlint": {"bat_buoc": True, "ban_ghim": "1.7.7", "probe": mot_probe("actionlint"), "canary": "actionlint_shellcheck", "chinh_sach": "blocking"}, "shellcheck": {"bat_buoc": False, "ban_ghim": None, "probe": mot_probe("shellcheck", r"version:\s*(\d+\.\d+\.\d+)")}}
        rc, out, _ = chay("kiem-tra", "--ban-ke", str(ghi_ban_ke(tmp, cc)), env=moi_truong(d)); bc = json.loads(out)
        bang(rc == 0 and bc["trang_thai_tong"] == "DAT" and bc["canary"][0]["trang_thai"] == "DAT", f"blocking bắt oan: {out}")

# ===== BỘ ĐỘT BIẾN — 1 đột biến/ca, bán kính đo
# TOÀN suite. Rút gọn từ .claude/dev/packet_loop_test.py (MUTANTS). CÔ LẬP 3
# HỌ: t1,t2,t3,t4,t7,t8 qua biến SCRIPT (hàm chay()); t5 qua CAI_SH RIÊNG; t6
# qua GOC. Mỗi đột biến CHỈ patch ĐÚNG một biến — patch cả ba sẽ làm t5 "thấy"
# mutation của cong_cu.py qua đường gián tiếp (cai_cong_cu.sh tự suy GOC từ
# BASH_SOURCE rồi gọi cong_cu.py TRONG CÙNG CÂY), trộn lẫn hai họ lẽ ra tách.

_GOC_THAT = GOC  # snapshot bất biến, đọc nguồn LUÔN từ đây kể cả khi GOC bị patch

def _dung_cay_dot_bien(ten, tep, tim, thay, phu_thuoc=()):
    # Bản mutate + phụ thuộc vào THƯ MỤC TẠM RIÊNG (tên theo `ten` ⇒ .pyc không
    # đụng độ, CLAUDE.md "bài học lớp chạy được ở đây"). Không đụng tệp thật.
    than = (_GOC_THAT / tep).read_text(encoding="utf-8")
    if tim not in than:
        raise AssertionError(f"đột biến '{ten}': không thấy mỏ neo {tim!r} trong {tep}")
    cay = Path(tempfile.mkdtemp(prefix=f"dotbien_{ten}_"))
    dich = cay / tep
    dich.parent.mkdir(parents=True, exist_ok=True)
    dich.write_text(than.replace(tim, thay, 1), encoding="utf-8", newline="\n")
    for p in phu_thuoc:
        nguon, d2 = _GOC_THAT / p, cay / p
        d2.parent.mkdir(parents=True, exist_ok=True)
        (shutil.copytree if nguon.is_dir() else shutil.copy2)(nguon, d2)
    if tep.endswith(".sh"):
        dich.chmod(0o755)
    return cay, dich

# MOT NGUON SU THAT cho cau hoi "cay nao mang `ops/cong_cu.py` thi phai mang gi nua".
# Co HAI cho trong tep nay dung cay tam chua `cong_cu.py`: bo dot bien (`_PHU` duoi) va
# `_chay_batch`. Ban 20-09 sang va DUNG cho thu nhat — vi bao cao ban kinh chi vao no — roi
# BO SOT cho thu hai, va cho thu hai chet tren Windows (`570-do-6`). Do la lan thu hai cua
# cung hinh dang trong packet nay, va lan thu BA cua hinh dang me "va dung cho duoc chi roi
# bo sot duong ke tiep". Nen khong va diem thu ba nua: ca hai cho doc CHUNG hang duoi day,
# va `t30` lam DO neu no rong.
KEM_THEO_CONG_CU = ("ops/bash_nen.py",)
_KEM_TEP_TEST = ("ops/lease_publish_test.py", "ops/bash_nen.py", "ops/cong_cu.py")

# `ops/bash_nen.py` NAM TRONG day tu r3 (#570, N14): `ops/cong_cu.py` nay import no, nen mot
# cay dot bien thieu no se lam ban mutate chet vi ImportError — stdout RONG, va ca doc dau ra
# do chet bang `JSONDecodeError`. Do la mot cai chet VO CAN: bo phan hang xep dung la
# `tin_dung_gia`, nhung 12 bao cao ban kinh thanh khong doc duoc.
# DO DUOC 20-09-2026: thieu dong nay => `t13_actionlint_bien_mat_giua_probe_va_canary` chet
# `JSONDecodeError` duoi MOI dot bien ho SCRIPT. No chi lo ra vi bao cao ban kinh nay in LY DO
# (N16); ban truoc chi in TEN ca oan va se khong ai tim ra duoc nguyen nhan tu do.
_PHU = ("ops/cong_cu.yaml", "ops/canary/actionlint_shellcheck.yml") + KEM_THEO_CONG_CU

# ten_dot_bien -> (tep_muc_tieu, tim, thay, bien_toan_cuc_can_patch, phu_thuoc, ten_ca_dich)
DOT_BIEN = {
    "t1_rc_gop": ("ops/cong_cu.py",
        "RC = {DAT: 0, DO: 2, KHONG_DO_DUOC: 3}\n",
        "RC = {DAT: 0, DO: 2, KHONG_DO_DUOC: 0}  # đột biến: gộp\n",
        "SCRIPT", _PHU, "t1_thieu_bat_buoc_khac_ma_voi_do"),
    "t2_go_canary": ("ops/cong_cu.py",
        '    return {**goc, "trang_thai": DO, "chi_tiet": f"{ly_do} (rc={rc})"}\n',
        '    return {**goc, "trang_thai": DAT, "chi_tiet": f"{ly_do} (rc={rc})"}  # đột biến\n',
        "SCRIPT", _PHU, "t2_canary_thieu_shellcheck_phai_SUY_GIAM"),
    "t3_bao_dong_gia": ("ops/cong_cu.py",
        '    return {**goc, "trang_thai": DAT, "chi_tiet": "dat"}\n',
        '    if ten == "on-dinh-t3":\n'
        '        return {**goc, "trang_thai": DO, "chi_tiet": "bao dong gia"}  # đột biến\n'
        '    return {**goc, "trang_thai": DAT, "chi_tiet": "dat"}\n',
        "SCRIPT", _PHU, "t3_du_cong_cu_dung_ban_khong_canh_bao_thua"),
    "t4_mat_ban_mong_doi": ("ops/cong_cu.py",
        '        return {**goc, "trang_thai": DO, "chi_tiet": f"sai ban: mong \'{ban_ghim}\', thay {ban_thay}"}\n',
        '        return {"ten": ten, "bat_buoc": bat_buoc, "ban_thay": ban_thay,\n'
        '                "trang_thai": DO, "chi_tiet": f"sai ban, thay {ban_thay}"}  # đột biến\n',
        "SCRIPT", _PHU, "t4_sai_ban_phai_neu_ro_ban_mong_doi_va_ban_thay"),
    "t5_thoat_som": ("ops/cai_cong_cu.sh",
        '[ -n "$TEN" ] || { echo "cai_cong_cu: thieu ten cong cu (vi du: actionlint)" >&2; exit 2; }\n',
        '[ -n "$TEN" ] || { echo "cai_cong_cu: thieu ten cong cu (vi du: actionlint)" >&2; exit 2; }\n'
        'command -v "$TEN" >/dev/null 2>&1 && exit 0  # đột biến: thoát sớm\n',
        # `ops/cai_actionlint.sh` phải có trong cây tạm: thiếu nó thì t5 chết vì `rc=127 No such
        # file` — chết VÔ CAN, tín dụng giả (đo 02-09-2026 khi thêm t23). Có nó, t5 vẫn chết
        # đúng lý do "đo lại phải thấy bản 1.7.7".
        "CAI_SH", ("ops/cong_cu.py", "ops/cai_actionlint.sh") + _PHU,
        "t5_cai_cong_cu_khong_thoat_som_khi_da_co_tren_PATH"),
    "t6_day_g5_sau_py_compile": (".github/workflows/ci.yml",
        "      - name: G5 kiem ban ke cong cu + T1..T8 (packet #290)\n",
        "      - name: py_compile dot bien TRUOC G5\n"
        "        run: python -m py_compile ops/cong_cu.py\n"
        "      - name: G5 kiem ban ke cong cu + T1..T8 (packet #290)\n",
        "GOC", (), "t6_ci_kiem_ban_ke_truoc_moi_test_nang"),
    "t7_bo_luat_2_duong": ("ops/cong_cu.py",
        "    if len(ban_thay) > 1 and len(khac_nhau) > 1:  # T7, độc lập ban_ghim\n",
        "    if False:  # đột biến: bỏ luật hai đường khác bản\n",
        "SCRIPT", _PHU, "t7_hai_duong_goi_khac_ban_phai_bao_khong_im"),
    "t8_mat_field_ten": ("ops/cong_cu.py",
        '    goc = {"ten": ten, "bat_buoc": bat_buoc, "ban_ghim": ban_ghim, "ban_thay": ban_thay}\n',
        '    goc = {"bat_buoc": bat_buoc, "ban_ghim": ban_ghim, "ban_thay": ban_thay}  # đột biến\n',
        "SCRIPT", _PHU, "t8_van_tay_cong_cu_co_trong_ho_so"),
    "t9_bo_kiem_rc": ("ops/cong_cu.py",
        "        if rc not in erc:\n",
        "        if False:  # đột biến: mọi rc đều hợp lệ\n",
        "SCRIPT", _PHU, "t9_probe_rc_phai_hop_le_ke_ca_khong_ghim_va_mixed"),
    "t10_cho_parse_rong_va_cat_tien_to": ("ops/cong_cu.py",
        '        if not m or not m.group(1) or _cat_tien_to_token(ra, m):\n'
        '            hong.append(f"probe \'{ten_pb}\' da chay nhung khong parse tron token phien ban")\n'
        '            continue\n'
        '        ban_thay[ten_pb] = m.group(1)\n',
        '        if m:\n'
        '            ban_thay[ten_pb] = m.group(1)  # đột biến: cho rỗng/cắt tiền tố\n',
        "SCRIPT", _PHU, "t10_probe_phai_parse_va_bat_tron_token"),
    "t11_cho_ban_ghim_rong": ("ops/cong_cu.py",
        '        if bg is not None and (not isinstance(bg, str) or not bg.strip()):\n',
        '        if bg is not None and not isinstance(bg, str):  # đột biến: cho chuỗi rỗng\n',
        "SCRIPT", _PHU, "t11_ban_ghim_rong_bi_tu_choi_nhung_null_hop_le"),
    "t12_mac_dinh_advisory": ("ops/cong_cu.py",
        '           "chinh_sach": dn.get("chinh_sach", "blocking")}\n',
        '           "chinh_sach": dn.get("chinh_sach", "advisory")}  # đột biến\n',
        "SCRIPT", _PHU, "t12_vang_chinh_sach_canary_mac_dinh_blocking"),
    "t13_mat_requiredness_khi_tool_bien_mat": ("ops/cong_cu.py",
        '        return {**goc, "trang_thai": KHONG_DO_DUOC, "chi_tiet": f"khong goi duoc \'{ten_chu}\'"}\n',
        '        return {**goc, "trang_thai": DAT, "chi_tiet": "mat tool"}  # đột biến\n',
        "SCRIPT", _PHU, "t13_actionlint_bien_mat_giua_probe_va_canary"),
    "t14_advisory_keo_tong": ("ops/cong_cu.py",
        '        if kq["chinh_sach"] == "advisory":\n', '        if False:  # đột biến\n',
        "SCRIPT", _PHU, "t14_advisory_giu_trang_thai_that_nhung_khong_keo_tong"),
    "t15_blocking_bat_oan": ("ops/cong_cu.py",
        '    if "SC1003" in ra:\n', '    if False:  # đột biến\n',
        "SCRIPT", _PHU, "t15_blocking_du_cong_cu_phai_DAT_khong_bat_oan"),
    # #445 gen 4 — regex git quay về bản cắt hậu tố: `2.55.0.windows.5` lại thành token cụt.
    # Đột biến vào YAML nên patch GOC; cây tạm thiếu `.claude/dev` ⇒ t16..t20 tự BỎ QUA.
    "t21_git_regex_cat_hau_to": ("ops/cong_cu.yaml",
        r"regex: '(?m)^git version\s+(\d+\.\d+\.\d+(?:[.+-][0-9A-Za-z.+-]*)?)'}]",
        r"regex: '(?m)^git version\s+(\d+\.\d+\.\d+)'}]  # đột biến: cắt hậu tố",
        "GOC", ("ops/cong_cu.py", ".github/workflows/ci.yml", "ops/canary/actionlint_shellcheck.yml"),
        "t21_git_for_windows_hau_to_nha_cung_cap_phai_DAT_va_bat_tron"),
    # #445 gen 4 — bỏ chốt loại SystemRoot: bộ phóng WSL ở đầu PATH lại được chọn.
    # Dot bien nay TAI SINH phep loc theo TEN ma N14 vua go bo. No la phan chung cho ca lop
    # khuyet tat, khong chi cho mot dong: he co bat ky thu gi loc ung vien theo VI TRI truoc
    # khi phep nang luc chay, `t22` phai DO.
    "t22_lay_lai_loc_theo_ten": ("ops/cong_cu.py",
        "    duong, _ = bash_nen.tim_bash(**ep)\n    return duong\n",
        "    import os as _os\n"
        "    duong, _ = bash_nen.tim_bash(**ep)\n"
        "    _sr = ep.get('system_root') or _os.environ.get('SystemRoot', '')\n"
        "    if duong and _sr and _os.path.normcase(_os.path.abspath(str(duong))).startswith(\n"
        "            _os.path.normcase(_os.path.abspath(_sr)).rstrip('\\\\/')):\n"
        "        return None  # đột biến: loại lại theo ĐƯỜNG DẪN\n"
        "    return duong\n",
        "SCRIPT", _PHU, "t22_bash_windows_quyet_bang_NANG_LUC_chu_khong_bang_DUONG_DAN"),
    # Go fail-close CO LY DO, tra ve `ModuleNotFoundError` tran — dung hinh dang ma
    # `570-do-6` bat duoc tren Windows. `t30` chot (3) phai DO.
    "t30_go_fail_close_bo_giai": ("ops/cong_cu.py",
        "        raise RuntimeError(\n",
        "        raise ex  # đột biến: trả lại `ModuleNotFoundError` trần, bỏ lý do\n"
        "        raise RuntimeError(\n",
        "SCRIPT", _PHU, "t30_cay_tam_mang_cong_cu_phai_mang_ca_BO_GIAI"),
    # Nuot MOI ngoai le o `_chay_tien_kiem` — mot tien kiem hong THAT se thanh im lang.
    # `t31` chot (3) phai DO.
    "t31_tien_kiem_nuot_moi_loi": ("ops/cong_cu_test.py",
        "    except BoQuaMoiTruong as ex:\n        return (fn.__name__, str(ex))\n",
        "    except Exception as ex:  # đột biến: nuốt MỌI lỗi, kể cả chốt nghiệp vụ\n"
        "        return (fn.__name__, str(ex))\n",
        "TEP_TEST", ("ops/lease_publish_test.py", "ops/bash_nen.py"),
        "t31_tien_kiem_KHONG_DO_DUOC_khong_duoc_giet_ca_suite"),
    # Bo han phep nhan dien => thoi luong AM lai roi vao "loi vo can". `t32` chot (1) DO.
    "t32_bo_nhan_dong_ho_nhay": ("ops/cong_cu_test.py",
        "        if _la_dong_ho_nhay(ex):\n",
        "        if False:  # đột biến: bỏ hẳn phép nhận diện đồng hồ nhảy\n",
        "TEP_TEST", ("ops/lease_publish_test.py", "ops/bash_nen.py"),
        "t32_dong_ho_nhay_la_KHONG_DO_DUOC_chu_khong_phai_tin_dung_gia"),
    # NOI phep nhan dien ra MOI timeout => nuot ca qua han THAT. `t32` chot (2) DO.
    "t32_noi_ra_moi_timeout": ("ops/cong_cu_test.py",
        "            and ex.timeout is not None and ex.timeout < 0)\n",
        "            )  # đột biến: mọi TimeoutExpired đều bị coi là đồng hồ nhảy\n",
        "TEP_TEST", ("ops/lease_publish_test.py", "ops/bash_nen.py"),
        "t32_dong_ho_nhay_la_KHONG_DO_DUOC_chu_khong_phai_tin_dung_gia"),
    # Thu `_HANG_BASH` ve dung "bash" => `which("bash.exe")` lai lot. `t33` chot (1) DO.
    "t33_bo_bash_exe": ("ops/bash_nen.py",
        '_HANG_BASH = ("bash", "bash.exe")\n',
        '_HANG_BASH = ("bash",)  # đột biến: bỏ cách viết Windows\n',
        "BASH_NEN", (), "t33_do_phu_cua_cong_do_duoc_THEO_HINH_DANG"),
    # Bo doc doi so KEYWORD => `which(cmd=)` va `run(args=)` lai lot. `t33` chot (1) DO.
    "t33_bo_doi_so_keyword": ("ops/bash_nen.py",
        "    for kw in nut.keywords:\n        if kw.arg in khoa:\n            return kw.value\n",
        "    if False:  # đột biến: chỉ đọc đối số VỊ TRÍ\n        pass\n",
        "BASH_NEN", (), "t33_do_phu_cua_cong_do_duoc_THEO_HINH_DANG"),
    # Go moi truong khoi khoa cache => CONG_CU_BASH bi nuot lai. `t34` DO.
    # ── RÚT Ở r17, KÈM PHÉP ĐO ─────────────────────────────────────────────────
    # `t34_khoa_cache_bo_moi_truong` gỡ MÔI TRƯỜNG khỏi khoá cache. Từ khi có N56 (đếm lại tập
    # ứng viên ở mỗi lần trúng cache) nó KHÔNG CÒN GIẾT GÌ. Đo trên bản sao, bốn tổ hợp, đích
    # `t34`:  nguyên bản → ĐẠT · BỎ môi trường → ĐẠT · BỎ phép đếm lại → ĐẠT · BỎ CẢ HAI → ĐỎ.
    # Cơ chế: đổi môi trường thì `ung_vien()` trả một DANH SÁCH khác, mà N56 so chính danh
    # sách ấy ⇒ cache hết hiệu lực dù khoá không đổi; còn môi trường đổi mà danh sách KHÔNG
    # đổi thì kết quả cũng không thể khác.
    # Đây là lần thứ HAI một luật MỚI nuốt phép đo của một luật CŨ (lần đầu: N51 nuốt
    # `os.getcwd()` ở r16). Giữ môi trường trong khoá làm PHÒNG THỦ CHIỀU SÂU, nhưng khai là
    # **CHƯA ĐO ĐƯỢC một mình** chứ không khai là đúng. `None ≠ False`.
    # Thu pham vi ve `ops/**` => ban sao thu tu ngoai hang rao lai lot. `t35` chot (1) DO.
    "t35_thu_pham_vi_ve_ops": ("ops/bash_nen.py",
        # NEO LAI O r7. Ban cu neo vao `thu_muc = goc`, nhung tu r7 danh sach tep den tu
        # `_liet_ke_py(goc)` va `thu_muc` chi con la truong bao cao `da_quet`. Dot bien cu
        # vi the SONG SOT — do la mot LO HONG THAT cua cong (thuoc tinh PHAM VI khong con
        # dot bien nao troi), va bo ca da bat duoc no ngay luot chay dau sau ban va.
        # CHI THU PHAM VI, GIU NGUYEN `nguon_tep`. Ban dau dot bien nay goi
        # `_liet_ke_py(goc / "ops")`, va no giet THEM `t36` lan `t37` (ban kinh 3/41): doi goc
        # cung lam `(goc/"ops"/".git")` bien mat nen `nguon_tep` tut ve "rglob", tuc mot dot
        # bien cham HAI thuoc tinh. Dot bien qua rong thi ban kinh khong con doc duoc — va
        # loi ay la cua DOT BIEN, khong phai cua ca.
        "    cac_tep, nguon_tep = _liet_ke_py(goc)\n",
        # NEO LAI LAN HAI O r11: tu r11 moi muc la `(rel, che_do, sha)` chu khong con la
        # `Path`, nen ban cu goi `t.relative_to(goc)` tren mot tuple => gian giao hong =>
        # TIN DUNG GIA. Bo cham lai theo hinh dang MOI. Day la lan thu HAI dot bien nay phai
        # neo lai vi kieu du lieu doi — ghi ra vi no la CAI GIA co that cua viec doi kieu.
        '    cac_tep, nguon_tep = ([t for t in _liet_ke_py(goc)[0]\n'
        '                           if t[0].startswith("ops/")],\n'
        '                          _liet_ke_py(goc)[1])  # đột biến: thu về `ops/**` như r3\n',
        "BASH_NEN", (), "t35_cong_phai_quet_TOAN_CAY_chu_khong_chi_ops"),
    "t23_bo_cat_CR_ten_cong_cu": ("ops/cai_cong_cu.sh",
        "    cong_cu=\"${cong_cu%$'\\r'}\"\n",
        "    :  # đột biến: không cắt CR\n",
        "CAI_SH", ("ops/cong_cu.py", "ops/cai_actionlint.sh") + _PHU,
        "t23_batch_chiu_duoc_stdout_CRLF_cua_python_windows"),
    "t24_sai_pham_vi": ("ops/cong_cu.py",
        '        pham_vi = "mot-cong-cu"\n',
        '        pham_vi = "sai-pham-vi"  # đột biến\n',
        "SCRIPT", _PHU, "t24_pham_vi_mot_cong_cu_va_toan_bo"),
    "t24a_mot_cong_cu_ghi_chu_rong": ("ops/cong_cu.py",
        '        ghi_chu_pham_vi = "chua quet canary toan bo"\n',
        '        ghi_chu_pham_vi = ""  # đột biến\n',
        "SCRIPT", _PHU, "t24_pham_vi_mot_cong_cu_va_toan_bo"),
    "t24b_mot_cong_cu_ghi_chu_sai_su_that": ("ops/cong_cu.py",
        '        ghi_chu_pham_vi = "chua quet canary toan bo"\n',
        '        ghi_chu_pham_vi = "da quet canary toan bo"  # đột biến\n',
        "SCRIPT", _PHU, "t24_pham_vi_mot_cong_cu_va_toan_bo"),
    "t24c_toan_bo_ghi_chu_rong": ("ops/cong_cu.py",
        '        ghi_chu_pham_vi = "da quet canary toan bo (khong co nghia moi canary dat)"\n',
        '        ghi_chu_pham_vi = "   "  # đột biến\n',
        "SCRIPT", _PHU, "t24_pham_vi_mot_cong_cu_va_toan_bo"),
    # ── #570: mỗi ca T23..T27 đúng MỘT đột biến. `BASH_NEN` là biến được patch, nên
    # bản đột biến nằm ở thư mục tạm riêng — không bao giờ chạm tệp thật.
    "bn_bo_kiem_argv0": ("ops/bash_nen.py",
        '    if doc.get("BN0") != _NHAN_ARGV:\n',
        '    if False:  # đột biến: bỏ phép kiểm `$0`\n',
        "BASH_NEN", (), "t23_bash_nen_tu_choi_bash_nuot_argv"),
    "bn_bo_kiem_so_doi_so": ("ops/bash_nen.py",
        '    if doc.get("BNSO") != str(len(_DOI_SO)):\n',
        '    if False:  # đột biến: bỏ phép đếm đối số\n',
        "BASH_NEN", (), "t23_bash_nen_tu_choi_bash_nuot_argv"),
    "bn_bo_kiem_doi_so_1": ("ops/bash_nen.py",
        '    if doc.get("BN1") != _DOI_SO[0]:\n',
        '    if False:  # đột biến: bỏ phép kiểm `$1`\n',
        "BASH_NEN", (), "t23_bash_nen_tu_choi_bash_nuot_argv"),
    "bn_bo_kiem_mo_tep": ("ops/bash_nen.py",
        "        if rc != 0 or _DAU_CHAY not in ra:\n",
        "        if False:  # đột biến: bỏ phép mở đường dẫn bản địa\n",
        "BASH_NEN", (), "t24_bash_nen_tu_choi_bash_khong_mo_duoc_duong_dan_ban_dia"),
    "bn_cong_cho_qua_moi_noi": ("ops/bash_nen.py",
        # NEO LAI o r7 vong 2: lop A gop ba bang mien tru nen dong cu bien mat.
        "    moi = {t: d for t, d in co_loi_goi.items() if t not in _MIEN_TRU}\n",
        "    moi = {}  # đột biến: cổng không chặn lời gọi trần mới nữa\n",
        "BASH_NEN", (), "t25_cong_chan_loi_goi_bash_tran_MOI"),
    "bn_ratchet_mot_chieu": ("ops/bash_nen.py",
        "    da_sach = [t for t in CHUA_CHUYEN if t not in co_loi_goi]\n",
        "    da_sach = []  # đột biến: bỏ chiều ngược của ratchet\n",
        "BASH_NEN", (), "t26_ratchet_phai_NGAN_di_chu_khong_muc_ra"),
    "bn_bo_han_treo": ("ops/bash_nen.py",
        '        return False, f"phép argv: rc={rc} — {ra.strip()[:200]}"\n',
        '        if rc == -998:\n'
        '            return True, "đột biến: coi QUÁ HẠN là đạt"\n'
        '        return False, f"phép argv: rc={rc} — {ra.strip()[:200]}"\n',
        "BASH_NEN", (), "t28_bash_nen_tu_choi_bash_TREO_trong_han"),
    "bn_ban_kinh_giau_ly_do": ("ops/cong_cu_test.py",
        '    chi_tiet = [f"        · {t} [{tt}] {ly}" for t, (tt, ly) in sorted(ket.items()) if tt != "qua"]\n',
        '    chi_tiet = []  # đột biến: giấu LÝ DO, chỉ còn dòng đầu — đúng bản trước 20-09\n',
        "TEP_TEST", ("ops/lease_publish_test.py", "ops/bash_nen.py"),
        "t29_ban_kinh_qua_RONG_phai_neu_LY_DO_tung_ca_oan"),
    "bn_ban_kinh_gia_ve_som": ("ops/cong_cu_test.py",
        '    elif gia:\n'
        '        dau = [f"  ĐỎ  {ten_db}: ca {gia} chết bằng lỗi VÔ CAN (tín dụng giả) ⇒ bán kính "\n'
        '               f"không đọc được"]\n',
        '    elif gia:\n'
        '        return ([f"  ĐỎ  {ten_db}: ca {gia} chết bằng lỗi VÔ CAN (tín dụng giả) ⇒ bán kính "\n'
        '                 f"không đọc được"], 1)  # đột biến: nhánh `gia` về SỚM, bỏ lý do\n',
        "TEP_TEST", ("ops/lease_publish_test.py", "ops/bash_nen.py"),
        "t29_ban_kinh_qua_RONG_phai_neu_LY_DO_tung_ca_oan"),
    "bn_ratchet_tha_ca_tep": ("ops/bash_nen.py",
        # NEO LAI o r8: `thay and` da bi go (F1). Dot bien nay TAI TAO dung luat r4 — chi bat
        # luc ve 0 — nen `t36` (2→3, 2→1) chet ma `t40` (2→0) song: hai ca, hai mat, hai dot bien.
        "        if thay != cho_phep:\n",
        "        if thay == 0 and thay != cho_phep:  # đột biến: về lại luật cũ — tha CẢ TỆP, chỉ bắt lúc về 0\n",
        "BASH_NEN", (), "t36_ratchet_dem_SO_LAN_chu_khong_tha_ca_tep"),
    # r8 — F1 codex vong 3: TAI TAO dung dong r7 `if thay and …`. `t40` chet qua chot "ve 0";
    # `t36` song vi hai chot cua no deu o so KHAC 0.
    "bn_han_ngach_0_bi_bo_qua": ("ops/bash_nen.py",
        "        if thay != cho_phep:\n",
        "        if thay and thay != cho_phep:  # đột biến: về 0 thì thôi so (F1 codex vòng 3)\n",
        "BASH_NEN", (), "t40_moi_MIEN_TRU_deu_mang_HAN_NGACH_va_dem_theo_LOI_GOI"),
    # r8 — cung lop F1, thuc the tim them khi quet theo lop: mot muc CHUOI trong `CHUA_CHUYEN`
    # THAT la ve vo han, va `t40` cu khong thay vi no doc bang cua BAN SAO. Chieu nguoc phai
    # TAO RA thu no sinh ra de bat: dot bien nay CHEN mot muc chuoi vao bang that.
    "bn_muc_chuoi_trong_ratchet_that": ("ops/bash_nen.py",
        "CHUA_CHUYEN = {\n",
        'CHUA_CHUYEN = {\n    "ops/ve_vo_han_dot_bien.py": "đột biến: mục CHUỖI, không hạn ngạch",\n',
        "BASH_NEN", (), "t40_moi_MIEN_TRU_deu_mang_HAN_NGACH_va_dem_theo_LOI_GOI"),
    # THU HEP O r10, va ly do la mot PHEP DO chu khong phai khau vi. Ban cu dat `if False:`
    # len TOAN BO nhanh `.git`, tuc xoa CA duong INDEX LAN duong `git-hong`. Khi `t44` ra doi
    # no giet them `t44` => ban kinh 2/46. Doc ly do IN RA thi thay hai chot chet vi HAI LY DO
    # KHAC NHAU (`t37`: "khong khai dung git"; `t44`: "ra rc=2 DO tren cay git hong") — do la
    # chu ky cua DOT BIEN QUA RONG (nam tren duong chung cua gian giao), KHONG phai chu ky cua
    # "hai ca troi cung mot thuoc tinh". Ban nay chi cat NGHIA cua INDEX: van di duong git, van
    # khai `nguon_tep = "git"`, nhung tra danh sach rglob — tuc NOI DOI ve nguon. `t44` khong
    # dong toi vi hai chot cua no o hai cay khac (git HONG va KHONG git).
    # NEO LAI LAN HAI O r11. Ban r10 dat `if False:` len nhanh `.git` => QUA RONG (giet ca
    # `t44`), da thu hep thanh "khai `git` ma tra rglob"; nhung r11 doi `muc` thanh bo ba
    # `(rel, che_do, sha)` va `_doc_noi_dung` DOI sha that de `cat-file`, nen tra rglob khong
    # con mach lac. Ban nay giu dung THUOC TINH t37 troi — "chua `git add` thi KHONG quet" —
    # bang cach CONG THEM tep chua theo doi vao danh sach, kem sha that.
    "bn_quet_thang_bo_qua_INDEX": ("ops/bash_nen.py",
        '                return sorted(set(muc)), "git"\n',
        '                _co = {m[0] for m in muc}\n'
        '                for _x in goc.rglob("*.py"):\n'
        '                    _r = _x.relative_to(goc).as_posix()\n'
        '                    if _r in _co:\n'
        '                        continue\n'
        '                    _h = _chay_git(goc, "hash-object", "-w", str(_x),\n'
        '                                   capture_output=True, text=True,\n'
        '                                   timeout=60).stdout.strip()\n'
        '                    if _h:\n'
        '                        muc.append((_r, "100644", _h))\n'
        '                return sorted(set(muc)), "git"  # đột biến: cộng cả tệp CHƯA add\n',
        "BASH_NEN", (), "t37_danh_sach_tep_la_INDEX_da_add_thi_quet_chua_add_thi_KHONG"),
    "bn_ten_phan_biet_hoa_thuong": ("ops/bash_nen.py",
        # NEO LAI O r11: `_la_hang_bash` tach nhanh theo KIEU (str / bytes) nen dong cu
        # khong con. Neo vao nhanh `str`.
        # NEO LAI O r17: `_la_hang_bash` da la MA CHET sau N52 va da duoc go. Luat THAT
        # song o `_la_ten_bash`. Do duoc: neo cu SONG SOT vi no mutate mot ham khong ai goi.
        "    ten = _ten_tu_gia_tri(v)\n    return ten is not None and ten.casefold() in _HANG_BASH\n",
        "    ten = _ten_tu_gia_tri(v)\n    return ten is not None and ten in _HANG_BASH"
        "  # đột biến: so phân biệt hoa/thường\n",
        "BASH_NEN", (), "t33_do_phu_cua_cong_do_duoc_THEO_HINH_DANG"),
    # ── RÚT Ở r16, KÈM PHÉP ĐO ─────────────────────────────────────────────────
    # `bn_khoa_cache_bo_cwd` gỡ `os.getcwd()` khỏi khoá cache. Từ khi có VÂN TAY TỆP (N51)
    # nó KHÔNG CÒN GIẾT GÌ. Đo trên bản sao, bốn tổ hợp, `t38` là đích:
    #     nguyên bản -> ĐẠT   ·   BỎ cwd -> ĐẠT   ·   BỎ vân tay -> ĐẠT   ·   BỎ CẢ HAI -> ĐỎ
    # Cơ chế: ứng viên ở `b/` là đường TƯƠNG ĐỐI, `os.stat` nó ở `b/` ném `FileNotFoundError`
    # ⇒ vân tay lệch ⇒ đo lại. Tức N51 NUỐT phép đo của N19.
    # KẾT LUẬN THẲNG: `os.getcwd()` trong khoá nay là PHÒNG THỦ CHIỀU SÂU và KHÔNG CÒN ĐO
    # ĐƯỢC MỘT MÌNH. Giữ lại vì rẻ và vì cả hai lớp đều phải sai thì phán quyết mới sai;
    # nhưng khai là CHƯA ĐO chứ không khai là đúng — `None ≠ False`. Một đột biến không giết
    # được gì thì không phải phép đo, và giữ nó lại chỉ để bảng thống kê đẹp hơn là tự dối.
    # Đột biến gỡ CẢ HAI sẽ giết `t38` VÀ `t51` (bán kính 2), nên nó không thay thế được.
    # Tep dong hanh cua mot dot bien tren CHINH TEP TEST: no duoc CHAY nhu mot tien trinh,
    # nen cay tam phai co du thu no `import` o dau tep. Thieu `ops/lease_publish_test.py` thi
    # no chet `ModuleNotFoundError` TRUOC khi toi chot, va bo phan hang xep dung la
    # `tin_dung_gia` — do la bo phan hang lam viec, khong phai mot phien toa.
    # CHEP TU `_GOC_THAT`: mot dot bien khac co the da tro `GOC` sang cay tam (bai hoc t6/t21).

    # SAU DOT BIEN CHO NAM LOP CUA VONG 2 — moi lop it nhat mot dot bien.
    "bn_cho_phep_vo_han": ("ops/bash_nen.py",
        "    for _bang in (CHO_PHEP, CHUA_CHUYEN, ANH_CHUP_DONG_CUNG):\n",
        "    for _bang in (CHUA_CHUYEN,):  # đột biến: CHO_PHEP thành vé VÔ HẠN trở lại\n",
        "BASH_NEN", (), "t40_moi_MIEN_TRU_deu_mang_HAN_NGACH_va_dem_theo_LOI_GOI"),
    "bn_dem_theo_DONG": ("ops/bash_nen.py",
        "            ban_ghi.append((id(nut), vi_tri_cua.get(id(nut)) or (nut.lineno, nut.col_offset)))\n",
        "            ban_ghi.append((id(nut), vi_tri_cua[id(nut)]) if id(nut) in vi_tri_cua else (nut.lineno, (nut.lineno, 0)))  # đột biến: đếm theo DÒNG, gộp cùng dòng\n",
        "BASH_NEN", (), "t40_moi_MIEN_TRU_deu_mang_HAN_NGACH_va_dem_theo_LOI_GOI"),
    # r8 — kien truc "danh sach = INDEX": dot bien NGHE LAI luat ignore (cua kho lan cua may qua
    # `--exclude-standard`) bang cach tru di tap tracked-ma-bi-ignore. `t43` chot (1) chet: tep
    # `add -f` khop `.gitignore` da commit bien mat. `t37` song: tep cua no khong bi ignore.
    # NEO LAI O r11: dong `ten = [...]` khong con. Y DINH khong doi — bat cong NGHE LAI luat
    # ignore — nay viet bang `check-ignore` tren chinh danh sach INDEX.
    "bn_nghe_lai_luat_ignore": ("ops/bash_nen.py",
        '                return sorted(set(muc)), "git"\n',
        # NEO LAI O r15: ban r13 truyen duong dan dang TEXT vao tien trinh con, va tu N36
        # duong co the mang BYTE THO (surrogate) nen CHINH DOT BIEN vo => stdout rong =>
        # no giet OAN `t49`. Loi cua DOT BIEN, khong cua ca. Nay truyen BYTES.
        '                _loai = _chay_git(goc, "check-ignore", "--no-index", "--stdin",\n'
        '                                  input="\\n".join(m[0] for m in muc)\n'
        '                                        .encode("utf-8", "surrogateescape"),\n'
        '                                  capture_output=True, timeout=60\n'
        '                                  ).stdout.decode("utf-8", "surrogateescape").split()\n'
        '                return sorted({m for m in muc if m[0] not in _loai}), "git"  # đột biến: nghe lại ignore\n',
        "BASH_NEN", (), "t43_khong_luat_ignore_nao_doi_duoc_danh_sach_tep"),
    "bn_bo_executable_kw": ("ops/bash_nen.py",
        # NEO LAI o r8: `executable` (ten hoac vi tri) nay di qua MOT nhanh.
        "                dinh = _la_ten_bash(exe, tra_ten)\n",
        "                dinh = False  # đột biến: bỏ `executable=`\n",
        "BASH_NEN", (), "t33_do_phu_cua_cong_do_duoc_THEO_HINH_DANG"),
    # r8 — F4 codex vong 3: `executable=` CONG THEM thay vi GHI DE — dung ban r7. Hinh dang
    # `executable_ghi_de_khac` (chay `echo`) bi bat oan tro lai.
    "bn_executable_cong_them": ("ops/bash_nen.py",
        "            if exe is None:\n",
        # r17: `_la_hang_bash` da go (MA CHET sau N52). Dot bien nhac mot ten khong ton tai
        # thi ca dich chet bang `NameError` chu khong bang chot cua no — bo phan hang goi
        # dung ten: TIN DUNG GIA. Do duoc o luot chay r17, va no la ly do phai sua o day.
        "            if exe is None or not _la_ten_bash(exe, tra_ten):  # đột biến: cộng thêm, không ghi đè\n",
        "BASH_NEN", (), "t33_do_phu_cua_cong_do_duoc_THEO_HINH_DANG"),
    # r8 — cung lop, chieu LOT: chuoi tran `run("bash")` thoi duoc coi la ten chuong trinh.
    "bn_bo_chuoi_tran": ("ops/bash_nen.py",
        "    v = _gia_tri_hang(nut, tra_ten)          # `run(\"bash\")` — chuỗi trần cũng phóng theo TÊN\n",
        "    return False  # đột biến: chuỗi trần không phải là tên chương trình\n",
        "BASH_NEN", (), "t33_do_phu_cua_cong_do_duoc_THEO_HINH_DANG"),
    # r8 — F3 codex vong 3, HAI mat cua cung mot khuyet tat, moi mat mot dot bien:
    # (a) `import` RO RI qua pham vi — bang rang buoc xuong ca pham vi con (dung `ast.walk` cu);
    #     `import_ham_khac` bi bat oan. `pham_vi_ro_ri` nguyen van van song vi tham so con che.
    "bn_import_ro_ri_qua_pham_vi": ("ops/bash_nen.py",
        "        if isinstance(n, _NUT_PHAM_VI):\n",
        "        if False:  # đột biến: xuống cả phạm vi con — import rò rỉ như `ast.walk`\n",
        "BASH_NEN", (), "t33_do_phu_cua_cong_do_duoc_THEO_HINH_DANG"),
    # (b) ten bi CHE khong chan tim kiem — rang buoc cuc bo cua ham bi bo qua, tiep tuc ra ngoai; `tham_so_che`/`gan_che`/`ham_unbound_local` bi bat oan. (NEO LAI O r21 vao N76.)
    "bn_ten_bi_che_khong_chan": ("ops/bash_nen.py",
        "            if la_lop:\n                continue                   # thân lớp: gộp với phạm vi bao, không thay thế\n            return _mot_import(tap)\n",
        "            continue  # đột biến: tên bị che (ràng buộc cục bộ của hàm) không chặn tra ra ngoài\n",
        "BASH_NEN", (), "t33_do_phu_cua_cong_do_duoc_THEO_HINH_DANG"),
    # r10 — LOP "phan loai rang buoc theo TEN, bo qua mot TRUONG cua nut AST", HAI mat,
    # HAI CHIEU NGUOC NHAU, moi mat mot dot bien. Codex vong 4 chi mat (a); (b) ra tu phep
    # quet theo LOP.
    # (a) bo qua `ImportFrom.level` => `from .subprocess import run` bi BAT OAN.
    "bn_import_tuong_doi_la_stdlib": ("ops/bash_nen.py",
        "                if n.level == 0 and n.module in _MODULE_CHU:\n",
        "                if n.module in _MODULE_CHU:  # đột biến: bỏ qua `level`\n",
        "BASH_NEN", (), "t33_do_phu_cua_cong_do_duoc_THEO_HINH_DANG"),
    # (b) `import subprocess.x` rang buoc `subprocess` vao module that => bo qua thi BO SOT.
    "bn_import_module_con_bo_sot": ("ops/bash_nen.py",
        "                elif al.asname is None and dau in _MODULE_CHU:\n",
        "                elif False:  # đột biến: `import subprocess.x` không ràng buộc gì\n",
        "BASH_NEN", (), "t33_do_phu_cua_cong_do_duoc_THEO_HINH_DANG"),
    # r10 — N26: cua sau cua lop "phan quyet phu thuoc trang thai LOCAL cua may". Phuc hoi
    # duong LUI ve `rglob` khi git hong; `t44` chot (1) phai DO.
    "bn_git_hong_lui_ve_rglob": ("ops/bash_nen.py",
        # NEO LAI LAN HAI O r13: N36 viet lai dong nay de giai ma `stderr` tu BYTES.
        '            return [], ("git-hong: ls-files rc=%d %r"\n'
        '                        % (pc.returncode, pc.stderr.decode("utf-8", "replace").strip()[:200]))\n',
        # NEO LAI O r11: `_liet_ke_py` nay tra BAN GHI `(rel, che_do, sha)`, nen ban lui cu
        # tra `Path` lam gian giao hong => TIN DUNG GIA. Ban nay lui dung hinh dang moi.
        '            return [(x.relative_to(goc).as_posix(), None, None)\n'
        '                    for x in sorted(goc.rglob("*.py"))], "rglob"  # đột biến: lùi im lặng\n',
        "BASH_NEN", (), "t44_khong_lay_duoc_INDEX_thi_KHONG_DO_DUOC_chu_khong_lui_ve_rglob"),
    # r15 — SAU dot bien cho N39..N44, mot cho moi luat.
    # RUT O r21, kem phep do: `bn_global_doi_cho_thay_vi_chep` (N39 "CHEP chu khong DOI") SONG SOT
    # tren luot day du r21 — duoi N76, nhanh `global` cua `_giai_ten` chi doc bang MODULE, nen
    # chep hay doi rang buoc cua ham khai `global` cho CUNG ket qua. Dot bien tuong duong ma goc
    # thi khong do duoc gi.
    "bn_bo_walrus_luc_dinh_nghia": ("ops/bash_nen.py",
        "                for x in _truong_luc_dinh_nghia(n):\n",
        "                for x in []:  # đột biến: walrus lúc định nghĩa không trồi ra\n",
        "BASH_NEN", (), "t33_do_phu_cua_cong_do_duoc_THEO_HINH_DANG"),
    "bn_bo_type_params": ("ops/bash_nen.py",
        '            ngoai = [*getattr(con, "type_params", ()), *con.decorator_list, *a.defaults,\n',
        '            ngoai = [*con.decorator_list, *a.defaults,  # đột biến: bỏ PEP 695\n',
        "BASH_NEN", (), "t50_PEP695_type_params_phai_duoc_tham_va_phai_CHE_duoc"),
    "bn_giai_ma_hong_thanh_traceback": ("ops/bash_nen.py",
        "    except (OSError, UnicodeDecodeError, SyntaxError, LookupError, ValueError) as e:\n",
        "    except (OSError, UnicodeDecodeError) as e:  # đột biến: lỗi giải mã thành traceback\n",
        "BASH_NEN", (), "t47_INDEX_phai_duoc_doc_TRUNG_THUC_va_nguon_py_nhan_du_moi_cach_viet"),
    # r17 — DOI CHIEU: khoa NAY la duong NGUYEN VEN, nen dot bien la viec dung phep HIEN THI
    # (khong don anh) lam khoa. Hai duong khac nhau ve byte se de nhau.
    # ── RÚT Ở r17, KÈM PHÉP ĐO ─────────────────────────────────────────────────
    # `bn_khoa_dung_phep_hien_thi` đổi khoá báo cáo sang `_duong_bao_cao(rel)`. Từ khi N54 làm
    # phép hiển thị ĐƠN ÁNH, việc ấy không còn làm hai đường đè nhau ⇒ KHÔNG GIẾT GÌ. Thuộc
    # tính "hiển thị phải đơn ánh" vẫn được đo bằng `bn_hien_thi_khong_don_anh`.
    # KHAI THẲNG chỗ còn lệch mà CHƯA đo được: khoá đi qua phép hiển thị sẽ nhân đôi dấu chéo
    # ngược, nên một đường CHỨA dấu chéo thật sẽ thôi khớp bảng miễn trừ. Cây này không có
    # đường nào như thế nên phép đo ấy chưa dựng được.
    "bn_ngay_go_chi_la_chu": ("ops/bash_nen.py",
        "    qua_han = sorted(CHUA_CHUYEN) if (CHUA_CHUYEN and hom_nay > _dt.date.fromisoformat(_NGAY_GO)) else []\n",
        "    qua_han = []  # đột biến: NGÀY GỠ lại thành chữ trang trí\n",
        "BASH_NEN", (), "t49_duong_XAU_ra_JSON_HOP_LE_va_NGAY_GO_phai_duoc_DOC"),
    # ── r19 — DOT BIEN cho N65..N71 (cross-review codex vong 13) ─────────────────
    # N65: f-string hang thoi duoc gap.
    "bn_khong_gap_f_string": ("ops/bash_nen.py",
        "    if isinstance(nut, ast.JoinedStr):\n",
        "    if False:  # đột biến: f-string hằng không được gấp\n",
        "BASH_NEN", (), "t33_do_phu_cua_cong_do_duoc_THEO_HINH_DANG"),
    # N65: bo loc RE loai `"".join(...)` truoc khi luat that duoc hoi.
    "bn_loc_re_bo_join": ("ops/bash_nen.py",
        '            and nut.func.attr == "join":\n',
        '            and nut.func.attr == "join" and False:  # đột biến: bộ lọc rẻ bỏ `.join`\n',
        "BASH_NEN", (), "t33_do_phu_cua_cong_do_duoc_THEO_HINH_DANG"),
    # N66: `pty.spawn` bi bo khoi tap loi phong.
    "bn_bo_pty": ("ops/bash_nen.py",
        "    if (mod, ham) in _API_ARGV:\n",
        "    if False:  # đột biến: `pty.spawn` không phải lời phóng\n",
        "BASH_NEN", (), "t33_do_phu_cua_cong_do_duoc_THEO_HINH_DANG"),
    # N68 -> N73 (NEO LAI O r20): chu thich duoc LUU (ke ca hoan boi `__future__`) ma khong quet.
    "bn_chu_thich_luu_khong_quet": ("ops/bash_nen.py",
        "                       if x is not None and x.annotation is not None]]\n",
        "                       if False]]  # đột biến: chú thích được LƯU mà không quét\n",
        "BASH_NEN", (), "t33_do_phu_cua_cong_do_duoc_THEO_HINH_DANG"),
    # N68/N73: chu thich bien CUC BO trong ham van bi quet nhu loi goi that. (NEO LAI O r21.)
    "bn_chu_thich_cuc_bo_van_quet": ("ops/bash_nen.py",
        "                (len(chuoi) > 1 and not chuoi[-1][0])\n",
        "                False  # đột biến: chú thích cục bộ vẫn quét\n",
        "BASH_NEN", (), "t33_do_phu_cua_cong_do_duoc_THEO_HINH_DANG"),
    # N70: ghi de TEN TRAN khong phan giai qua PATH.
    "bn_ghi_de_ten_tran_khong_giai": ("ops/bash_nen.py",
        "        if os.sep in ghi_de or (os.altsep and os.altsep in ghi_de):\n",
        "        if True:  # đột biến: ghi đè tên trần không phân giải qua PATH\n",
        "BASH_NEN", (), "t51_cache_phai_HET_HIEU_LUC_khi_chinh_TEP_ung_vien_doi"),
    # N71: bang dong cung khong con kiem hinh dang.
    "bn_dong_cung_khong_kiem_hinh_dang": ("ops/bash_nen.py",
        "        if _oid_dong_cung(m) is None and t not in khong_khai_so:\n",
        "        if False:  # đột biến: mục đông cứng thiếu OID không bị chặn\n",
        "BASH_NEN", (), "t40_moi_MIEN_TRU_deu_mang_HAN_NGACH_va_dem_theo_LOI_GOI"),
    # N71: OID khong bi kiem la 40 hex.
    "bn_oid_khong_kiem_hex": ("ops/bash_nen.py",
        '            and isinstance(muc[1], str) and re.fullmatch(r"[0-9a-f]{40}", muc[1]):\n',
        "            and isinstance(muc[1], str):  # đột biến: OID không được kiểm là 40 hex\n",
        "BASH_NEN", (), "t40_moi_MIEN_TRU_deu_mang_HAN_NGACH_va_dem_theo_LOI_GOI"),
    # ── r18 — DOT BIEN cho N58..N64 (cross-review codex vong 12) ─────────────────
    # N58: bo tinh hang thoi gap VO BOC GIU HANG => `"bash".encode()`, `str(Path(...))` lot.
    "bn_khong_gap_vo_boc": ("ops/bash_nen.py",
        "        boc = _gap_vo_boc(nut, tra_ten, sau)\n",
        "        boc = _KHONG_BIET  # đột biến: không gấp vỏ bọc giữ hằng\n",
        "BASH_NEN", (), "t33_do_phu_cua_cong_do_duoc_THEO_HINH_DANG"),
    # N58 chieu NGUOC: `str` bi CHE ma van gap nhu ten dung san => BAT OAN.
    "bn_str_bi_che_van_gap": ("ops/bash_nen.py",
        "            and not tra_ten(f.id, hoi_rang_buoc=True)):\n",
        "            and True):  # đột biến: không hỏi `str`/`bytes` có bị che không\n",
        "BASH_NEN", (), "t33_do_phu_cua_cong_do_duoc_THEO_HINH_DANG"),
    # N58: `dict` thoi la argv.
    "bn_dict_khong_la_argv": ("ops/bash_nen.py",
        "        return bool(nut.keys) and nut.keys[0] is not None \\\n",
        "        return False and nut.keys[0] is not None \\\n",
        "BASH_NEN", (), "t33_do_phu_cua_cong_do_duoc_THEO_HINH_DANG"),
    # N59: bang API ngoai subprocess/shutil bi bo qua.
    "bn_bo_bang_api": ("ops/bash_nen.py",
        "    if (mod, ham) in _API_THEO_TEN:\n",
        "    if False:  # đột biến: bỏ các API phóng theo TÊN ngoài subprocess/shutil\n",
        "BASH_NEN", (), "t33_do_phu_cua_cong_do_duoc_THEO_HINH_DANG"),
    # N59: bo KIEU DUOC NHAN cua tung API => `os.popen(Path(...))` bi BAT OAN.
    "bn_api_bo_kieu_nhan": ("ops/bash_nen.py",
        "            dinh = _la_ten_bash(_doi_so_thu(nut, vt, kw), tra_ten, nhan=nhan)\n",
        "            dinh = _la_ten_bash(_doi_so_thu(nut, vt, kw), tra_ten)  # đột biến: bỏ kiểu được nhận\n",
        "BASH_NEN", (), "t33_do_phu_cua_cong_do_duoc_THEO_HINH_DANG"),
    # N59: vi tri doi so luon la 0 => `spawnlp(mode, "bash")` lot va `spawnlp("bash", …)` bi bat.
    "bn_api_vi_tri_luon_dau": ("ops/bash_nen.py",
        "            dinh = _la_ten_bash(_doi_so_thu(nut, vt, kw), tra_ten, nhan=nhan)\n",
        "            dinh = _la_ten_bash(_doi_so_thu(nut, 0, kw), tra_ten, nhan=nhan)  # đột biến: vị trí luôn là 0\n",
        "BASH_NEN", (), "t33_do_phu_cua_cong_do_duoc_THEO_HINH_DANG"),
    # N62: thanh phan PATH RONG lai bi bo qua.
    "bn_path_rong_bo_qua": ("ops/bash_nen.py",
        "        d = d or os.curdir\n",
        "        if not d:\n            continue  # đột biến: thành phần rỗng bị bỏ qua\n",
        "BASH_NEN", (), "t51_cache_phai_HET_HIEU_LUC_khi_chinh_TEP_ung_vien_doi"),
    # RUT O r32: bn_path_rong_mat_cham (N62: `Path('.') / 'bash'` rut thanh TEN TRAN) — N113 tuyet doi
    # hoa MOI ung vien ngay khi liet ke, va `abspath("bash") == abspath("./bash")`, nen dot bien ay
    # khong con doi duoc hanh vi nao (luot day du r32 do duoc: song sot). Ca lop "ten tran" nay chet
    # theo KIEN TRUC; chot (5b)/(9) cua `t51` canh N113.
    # N63: han ngach bi EP KIEU thay vi hoi kieu.
    "bn_quota_ep_kieu": ("ops/bash_nen.py",
        "        if not isinstance(so, int) or isinstance(so, bool) or so < 0:\n",
        "        so = int(so)  # đột biến: ép kiểu thay vì hỏi kiểu\n        if False:\n",
        "BASH_NEN", (), "t40_moi_MIEN_TRU_deu_mang_HAN_NGACH_va_dem_theo_LOI_GOI"),
    # ── r29 — DOT BIEN cho N101b..N105 (codex vong 23; soat tran theo quyet dinh chu kho) ──
    "bn_tai_qua_tran_im": ("ops/bash_nen.py",
        '        raise _VuotNganSach(f"tải `exec`/`eval` hằng dài {len(v)} > {_TRAN_EXEC}")\n',
        '        return None  # đột biến: tải quá trần bị coi như không có\n',
        "BASH_NEN", (), "t33_do_phu_cua_cong_do_duoc_THEO_HINH_DANG"),
    "bn_giai_dong_co_tran": ("ops/bash_nen.py",
        "    while hang:\n",
        "    for _v in range(len(cac_muc)):  # đột biến: trần số lần giải\n        if not hang:\n            break\n",
        "BASH_NEN", (), "t33_do_phu_cua_cong_do_duoc_THEO_HINH_DANG"),
    "bn_phan_tram_sao_tong_moi_so": ("ops/bash_nen.py",
        "    tong = 0\n    i = 0\n",
        "    tong = sum(abs(x) for x in cac if type(x) is int) if \"*\" in van else 0  # đột biến\n    i = 0\n",
        "BASH_NEN", (), "t33_do_phu_cua_cong_do_duoc_THEO_HINH_DANG"),
    # r30 — N107: do chinh xac cua chuyen doi CHUOI la tran, khong khuech dai.
    "bn_chinh_xac_chuoi_van_tinh": ("ops/bash_nen.py",
        "            tong += rong\n",
        "            tong += rong + chinh_xac  # đột biến: độ chính xác của `%s` vẫn tính là khuếch đại\n",
        "BASH_NEN", (), "t33_do_phu_cua_cong_do_duoc_THEO_HINH_DANG"),
    # r30 — N108: so loi goi trong tai `exec` duoc mang ra ngoai.
    "bn_tai_exec_co_khong": ("ops/bash_nen.py",
        "            ghi_exec.extend([vt] * so)\n",
        "            ghi_exec.extend([vt] * min(so, 1))  # đột biến: tải chỉ tính CÓ/KHÔNG\n",
        "BASH_NEN", (), "t33_do_phu_cua_cong_do_duoc_THEO_HINH_DANG"),
    # r30 — N109: giai lai THEO PHU THUOC, khong quet lai ca bang.
    "bn_giai_dong_quet_lai": ("ops/bash_nen.py",
        "            for k2 in theo_ten.get((ten, b_id), ()):\n",
        "            for k2 in range(len(cac_muc)):  # đột biến: quét lại MỌI mục (bậc hai)\n",
        "BASH_NEN", (), "t33_do_phu_cua_cong_do_duoc_THEO_HINH_DANG"),
    # r31 — N110..N112 (codex vong 25).
    "bn_kieu_b_thieu": ("ops/bash_nen.py",
        '_KIEU_TRAN = frozenset("srabc")\n',
        '_KIEU_TRAN = frozenset("srac")  # đột biến: quên `%b` của bytes\n',
        "BASH_NEN", (), "t33_do_phu_cua_cong_do_duoc_THEO_HINH_DANG"),
    "bn_phu_thuoc_moi_bang": ("ops/bash_nen.py",
        "                    for pv in c:\n",
        "                    for pv in [x for ch in chuoi_cua.values() for x in ch]:  # đột biến: khoá theo tên trần\n",
        "BASH_NEN", (), "t33_do_phu_cua_cong_do_duoc_THEO_HINH_DANG"),
    "bn_eval_khong_phu_thuoc": ("ops/bash_nen.py",
        "            ra.update(x.id for x in ast.walk(tai) if isinstance(x, ast.Name))\n",
        "            pass  # đột biến: tên trong tải `eval` không là phụ thuộc\n",
        "BASH_NEN", (), "t33_do_phu_cua_cong_do_duoc_THEO_HINH_DANG"),
    # r32 — N113/N114 (codex vong 26).
    "bn_tra_duong_goc": ("ops/bash_nen.py",
        "        ds.append(tuyet_doi)\n",
        "        ds.append(str(u))  # đột biến: trả chuỗi gốc (tương đối) thay đường đã thử\n",
        "BASH_NEN", (), "t51_cache_phai_HET_HIEU_LUC_khi_chinh_TEP_ung_vien_doi"),
    "bn_khong_han_tong": ("ops/bash_nen.py",
        "        dat, ly_do = _do_nang_luc([u], het_han=het_han)\n",
        "        dat, ly_do = _do_nang_luc([u])  # đột biến: không hạn tổng\n",
        "BASH_NEN", (), "t51_cache_phai_HET_HIEU_LUC_khi_chinh_TEP_ung_vien_doi"),
    "bn_han_tong_theo_ung_vien": ("ops/bash_nen.py",
        "        return han if het_han is None else min(han, het_han - time.monotonic())\n",
        "        return han  # đột biến: hạn tổng chỉ xét giữa các ỨNG VIÊN, không giữa các PHÉP\n",
        "BASH_NEN", (), "t51_cache_phai_HET_HIEU_LUC_khi_chinh_TEP_ung_vien_doi"),
    "bn_eval_moi_thuoc_tinh": ("ops/bash_nen.py",
        "        if _kieu_exec_cua(n, ten_exec) is None:          # N117 — CÙNG luật với bộ quét `_tai_exec`\n",
        "        if False:  # đột biến: đọc tải của MỌI `.eval`\n",
        "BASH_NEN", (), "t33_do_phu_cua_cong_do_duoc_THEO_HINH_DANG"),
    "bn_phu_thuoc_dai_dien": ("ops/bash_nen.py",
        "            for k2 in theo_ten.get((ten, b_id), ()):\n",
        "            for k2 in (*theo_ten.get((ten, b_id), ()), *[j for j, mm in enumerate(cac_muc) if 'eval' in ast.dump(mm[2][1])]):  # đột biến: khoá đại diện\n",
        "BASH_NEN", (), "t33_do_phu_cua_cong_do_duoc_THEO_HINH_DANG"),
    "bn_chinh_xac_am_tinh": ("ops/bash_nen.py",
        "            return max(v, 0) if la_chinh_xac else abs(v)\n",
        "            return abs(v)  # đột biến: độ chính xác `*` âm tính như dương\n",
        "BASH_NEN", (), "t33_do_phu_cua_cong_do_duoc_THEO_HINH_DANG"),
    # r33 — N117: bo doc phu thuoc dung CUNG luat voi bo quet.
    "bn_phu_thuoc_luat_rieng": ("ops/bash_nen.py",
        "        if _kieu_exec_cua(n, ten_exec) is None:          # N117 — CÙNG luật với bộ quét `_tai_exec`\n",
        "        if not (isinstance(n.func, ast.Name) and n.func.id in ('eval', 'exec')):  # đột biến: luật viết tay riêng\n",
        "BASH_NEN", (), "t33_do_phu_cua_cong_do_duoc_THEO_HINH_DANG"),
    # r34 — N118: khoa anh xa dem ngoac CAN BANG.
    "bn_khoa_dung_o_ngoac_dau": ("ops/bash_nen.py",
        '                if van[i] == "(":\n                    muc += 1\n',
        '                if False:  # đột biến: khoá dừng ở `)` ĐẦU (hành vi regex r33)\n                    muc += 1\n',
        "BASH_NEN", (), "t33_do_phu_cua_cong_do_duoc_THEO_HINH_DANG"),
    "bn_khoa_khong_khep_nem": ("ops/bash_nen.py",
        "                return                          # \"incomplete format key\" — Python ném trước khi dựng\n",
        "                raise _VuotNganSach('khoá không khép')  # đột biến: NÉM oan trên mẫu Python từ chối\n",
        "BASH_NEN", (), "t33_do_phu_cua_cong_do_duoc_THEO_HINH_DANG"),
    # r35 — N119/N120/N121 (codex vong 29).
    "bn_g_khong_thang_van_tinh": ("ops/bash_nen.py",
        '        elif kieu in "gG" and "#" not in co:\n',
        '        elif False:  # đột biến: `%g` không `#` vẫn tính trọn độ chính xác\n',
        "BASH_NEN", (), "t33_do_phu_cua_cong_do_duoc_THEO_HINH_DANG"),
    "bn_asyncio_bo_executable": ("ops/bash_nen.py",
        '            exe_as = _doi_so_executable_asyncio(nut) if mod == "asyncio" else None\n',
        '            exe_as = None  # đột biến: `executable=` của asyncio bị bỏ qua\n',
        "BASH_NEN", (), "t33_do_phu_cua_cong_do_duoc_THEO_HINH_DANG"),
    "bn_rglob_nuot_loi_doc": ("ops/bash_nen.py",
        "    if loi:\n        return [], \"rglob-hong: \"",
        "    if False:  # đột biến: lỗi đọc thư mục bị nuốt\n        return [], \"rglob-hong: \"",
        "BASH_NEN", (), "t46_noi_dung_lay_tu_INDEX_chu_khong_tu_cay_lam_viec"),
    "bn_quet_bo_rglob_hong": ("ops/bash_nen.py",
        '    if nguon_tep.startswith("rglob-hong"):\n',
        '    if False:  # đột biến: `quet` quét tiếp danh sách THIẾU\n',
        "BASH_NEN", (), "t46_noi_dung_lay_tu_INDEX_chu_khong_tu_cay_lam_viec"),
    # r36 — N122: phep tinh nang Bash.
    "bn_bo_phep_tinh_nang_bash": ("ops/bash_nen.py",
        '    if doc.get("BNBASH") != "1":\n',
        '    if False:  # đột biến: nhận cả shell POSIX\n',
        "BASH_NEN", (), "t23_bash_nen_tu_choi_bash_nuot_argv"),
    # r36 — N123/N124.
    "bn_khong_git_bo_kiem_oid": ("ops/bash_nen.py",
        "            thay_oid = _oid_blob_tu_dia(goc / t)\n",
        "            thay_oid = ghim  # đột biến: cây không-git coi như khớp\n",
        "BASH_NEN", (), "t46_noi_dung_lay_tu_INDEX_chu_khong_tu_cay_lam_viec"),
    "bn_khong_tran_tep": ("ops/bash_nen.py",
        "        if co > _TRAN_TEP_NGUON:\n",
        "        if False:  # đột biến: không trần mỗi tệp\n",
        "BASH_NEN", (), "t46_noi_dung_lay_tu_INDEX_chu_khong_tu_cay_lam_viec"),
    "bn_khong_tran_tong": ("ops/bash_nen.py",
        "    if tong > _TRAN_TONG_NGUON:\n",
        "    if False:  # đột biến: không trần tổng\n",
        "BASH_NEN", (), "t46_noi_dung_lay_tu_INDEX_chu_khong_tu_cay_lam_viec"),
    "bn_git_khong_kiem_tran": ("ops/bash_nen.py",
        "    _kiem_tran_doc(co_kt)\n",
        "    pass  # đột biến: nhánh git đọc không trần\n",
        "BASH_NEN", (), "t46_noi_dung_lay_tu_INDEX_chu_khong_tu_cay_lam_viec"),
    "bn_khong_git_khong_kiem_tran": ("ops/bash_nen.py",
        "        _kiem_tran_doc([(rel, (goc / rel).stat().st_size) for rel, _, _ in muc])\n",
        "        pass  # đột biến: nhánh không-git đọc không trần\n",
        "BASH_NEN", (), "t46_noi_dung_lay_tu_INDEX_chu_khong_tu_cay_lam_viec"),
    # r37 — N125: tran SO MUC nguon, do TRONG LUC liet ke, o ca hai nhanh.
    "bn_git_khong_tran_so_muc": ("ops/bash_nen.py",
        "                    if len(giu) > _TRAN_SO_TEP_NGUON:\n",
        "                    if False:  # đột biến: nhánh git không trần số mục\n",
        "BASH_NEN", (), "t46_noi_dung_lay_tu_INDEX_chu_khong_tu_cay_lam_viec"),
    "bn_git_giu_moi_ban_ghi": ("ops/bash_nen.py",
        "                    if tab and not _la_nguon_py(rel_b.decode(\"utf-8\", \"surrogateescape\")):\n",
        "                    if False:  # đột biến: giữ MỌI bản ghi INDEX (kể cả không phải nguồn)\n",
        "BASH_NEN", (), "t46_noi_dung_lay_tu_INDEX_chu_khong_tu_cay_lam_viec"),
    "bn_khong_git_khong_tran_so_muc": ("ops/bash_nen.py",
        "                        if len(ra) > _TRAN_SO_TEP_NGUON:\n",
        "                        if False:  # đột biến: nhánh không-git không trần số mục\n",
        "BASH_NEN", (), "t46_noi_dung_lay_tu_INDEX_chu_khong_tu_cay_lam_viec"),
    "bn_khong_git_khong_tran_duyet": ("ops/bash_nen.py",
        "                        if da_duyet > _TRAN_MUC_DUYET:\n",
        "                        if False:  # đột biến: không trần số mục DUYỆT\n",
        "BASH_NEN", (), "t46_noi_dung_lay_tu_INDEX_chu_khong_tu_cay_lam_viec"),
    "bn_vuot_tran_nuot_thanh_danh_sach": ("ops/bash_nen.py",
        '        return [], f"rglob-hong: vượt trần: {e}"\n',
        '        return sorted(ra), "rglob"  # đột biến: vượt trần mà trả danh sách CỤT như danh sách đủ\n',
        "BASH_NEN", (), "t46_noi_dung_lay_tu_INDEX_chu_khong_tu_cay_lam_viec"),
    "bn_ban_ghi_theo_toa_do": ("ops/bash_nen.py",
        "    theo_nut = dict(ban_ghi)\n",
        "    theo_nut = {p: p for _, p in ban_ghi}  # đột biến: khử trùng theo toạ độ\n",
        "BASH_NEN", (), "t33_do_phu_cua_cong_do_duoc_THEO_HINH_DANG"),
    "ct_gan_mot_tang": ("ops/cong_cu_test.py",
        "                gan(dd, nguon_cua(gg), gg)\n",
        "                gan(dd, {\"khac\"}, None)  # đột biến: đích lồng chỉ một tầng\n",
        "TEP_TEST", _KEM_TEP_TEST, "t39_chi_CA_PHAN_QUYET_duoc_chot_tren_rc_va_trang_thai"),
    "ct_bo_dk_sao_sao": ("ops/cong_cu_test.py",
        "                                  if isinstance(kk, _ast.Constant) and kk.value == \"dk\"), None)\n",
        "                                  if False), None)  # đột biến: `**{\"dk\": …}` không được đọc\n",
        "TEP_TEST", _KEM_TEP_TEST, "t39_chi_CA_PHAN_QUYET_duoc_chot_tren_rc_va_trang_thai"),
    # ── r28 — DOT BIEN cho N99b, N101 (codex vong 22) ──
    # N99b: chu thich chuoi QUA TRAN lai bi bo qua im lang.
    "bn_chu_thich_dai_im": ("ops/bash_nen.py",
        '                    raise _VuotNganSach(f"chú thích chuỗi dài {len(con.value)} > {_TRAN_EXEC}")\n',
        '                    continue  # đột biến: chú thích chuỗi quá trần bị bỏ qua\n',
        "BASH_NEN", (), "t33_do_phu_cua_cong_do_duoc_THEO_HINH_DANG"),
    # N101: dieu kien den bang tu khoa `dk=` thoi duoc doc.
    "ct_bo_tu_khoa_dk": ("ops/cong_cu_test.py",
        '            dieu_kien = nut.args[0] if nut.args else next(\n',
        '            dieu_kien = nut.args[0] if nut.args else None and next(  # đột biến: bỏ `dk=`\n',
        "TEP_TEST", _KEM_TEP_TEST, "t39_chi_CA_PHAN_QUYET_duoc_chot_tren_rc_va_trang_thai"),
    # ── r27 — DOT BIEN cho N92c, N96b, N97b, N99, N100 (codex vong 21; N99/N100 theo quyet dinh chu kho) ──
    # RUT O r27: bn_rglob_bo_lien_ket — phep do CHA la symlink (`_che_do`) thanh ma chet vi `rglob` khong
    # di vao thu muc symlink (do duoc tren 3.11 va 3.12); da go. Hai dot bien duoi canh luat moi.
    "bn_rglob_bo_symlink_tep": ("ops/bash_nen.py",
        "            if p.is_symlink():\n",
        "            if p.is_symlink() and p.is_dir():  # đột biến: symlink tên `*.py` (kể cả treo) không được đánh dấu\n",
        "BASH_NEN", (), "t46_noi_dung_lay_tu_INDEX_chu_khong_tu_cay_lam_viec"),
    "bn_rglob_bo_symlink_thu_muc": ("ops/bash_nen.py",
        "            if p.is_symlink():\n",
        "            if p.is_symlink() and _la_nguon_py(ten):  # đột biến: thư mục symlink bị bỏ qua im lặng\n",
        "BASH_NEN", (), "t46_noi_dung_lay_tu_INDEX_chu_khong_tu_cay_lam_viec"),
    # r30 — N106: phan loai symlink KHONG hoi dich.
    "bn_rglob_hoi_dich": ("ops/bash_nen.py",
        "            if p.is_symlink():\n",
        "            if p.is_symlink() and (_la_nguon_py(ten) or p.is_dir()):  # đột biến: luật N100, hỏi ĐÍCH\n",
        "BASH_NEN", (), "t46_noi_dung_lay_tu_INDEX_chu_khong_tu_cay_lam_viec"),
    # N99: chuoi trong chu thich duoc luu thoi duoc phan tich.
    "bn_chu_thich_chuoi_bo": ("ops/bash_nen.py",
        '                    than_chuoi = ast.parse(con.value, mode="eval").body\n',
        '                    than_chuoi = None  # đột biến: chú thích chuỗi không được quét\n',
        "BASH_NEN", (), "t33_do_phu_cua_cong_do_duoc_THEO_HINH_DANG"),
    # N99: bo loc re loai tep co chu thich chuoi TRUOC khi luat that duoc hoi.
    "bn_chu_thich_chuoi_loc_re": ("ops/bash_nen.py",
        '    if not ung_vien and not _co_chuoi_trong_chu_thich(cay):\n',
        '    if not ung_vien:  # đột biến: bộ lọc rẻ bỏ chú thích chuỗi\n',
        "BASH_NEN", (), "t33_do_phu_cua_cong_do_duoc_THEO_HINH_DANG"),
    # N96b: tu khoa trung qua `**{…}` literal thoi duoc nhan.
    "bn_trung_qua_sao_sao_bo": ("ops/bash_nen.py",
        "        if k.arg is None and isinstance(k.value, ast.Dict) and any(\n",
        "        if False and isinstance(k.value, ast.Dict) and any(  # đột biến\n",
        "BASH_NEN", (), "t33_do_phu_cua_cong_do_duoc_THEO_HINH_DANG"),
    # N97b: tai `eval` thoi bo khoang trang dau.
    "bn_eval_khong_bo_khoang_trang": ("ops/bash_nen.py",
        '            van = van.lstrip(" \\t")\n',
        '            pass  # đột biến: `eval` không bỏ khoảng trắng đầu\n',
        "BASH_NEN", (), "t33_do_phu_cua_cong_do_duoc_THEO_HINH_DANG"),
    # N92c: `_quet(…)[1]` truc tiep thoi duoc tha.
    "ct_mien_tru_quet_truc_tiep_bo": ("ops/cong_cu_test.py",
        "                      and (isinstance(g.value, _ast.Name) or la_quet(g.value))):\n",
        "                      and isinstance(g.value, _ast.Name)):  # đột biến: `_quet(…)[1]` trực tiếp không được tha\n",
        "TEP_TEST", _KEM_TEP_TEST, "t39_chi_CA_PHAN_QUYET_duoc_chot_tren_rc_va_trang_thai"),
    # ── r26 — DOT BIEN cho N92b..N98 (codex vong 20; N94/N98 theo quyet dinh chu kho) ──
    # RUT O r26, kem ly do DO DUOC: bn_khoa_bo_moi_truong, bn_khong_dem_lai_ung_vien,
    # bn_cache_khong_van_tay, bn_van_tay_chi_ke_thang — ma dich (khoa/van tay cache, N51/N56/N61)
    # DA GO theo N94. Dot bien tren ma khong con ton tai thi khong neo duoc.
    # Va bn_join_khong_ngan_sach (r22): phep kiem ngan sach `join` SAU khi gap da thanh ma CHET tu
    # N93b (song sot o luot day du r26) — nhanh ay da GO; `bn_join_ngan_sach_sau` canh luat moi.
    # N94: dung lai cache KHOA THEO MOI TRUONG + cwd (dung hinh dang r18) — tep ung vien doi tai cho
    # thi tra phan quyet cu; `t51` (1) bat.
    "bn_cache_dung_lai": ("ops/bash_nen.py",
        "    return ket, chan_doan\n",
        "    return tim_bash.__dict__.setdefault(\"_c\", {}).setdefault(repr((sorted(ep.items()), tat_ca,"
        " sorted(os.environ.items()), os.getcwd())), (ket, chan_doan))  # đột biến: cache khoá theo môi trường quay lại\n",
        "BASH_NEN", (), "t51_cache_phai_HET_HIEU_LUC_khi_chinh_TEP_ung_vien_doi"),
    # N93b: ngan sach `join` chi tinh SAU khi da gap moi phan tu.
    "bn_join_ngan_sach_sau": ("ops/bash_nen.py",
        "                if tong > _NGAN_SACH_DINH_DANG:\n                    raise _VuotNganSach(f\"`join` vượt {_NGAN_SACH_DINH_DANG} ký tự\")\n",
        "                pass  # đột biến: không dừng giữa chừng\n",
        "BASH_NEN", (), "t33_do_phu_cua_cong_do_duoc_THEO_HINH_DANG"),
    # N96: tham so chuong trinh cap HAI lan van bi bao.
    "bn_trung_doi_so_bo": ("ops/bash_nen.py",
        "        if trung:\n            continue\n",
        "        if False:  # đột biến: lời gọi Python từ chối vẫn bị báo\n            continue\n",
        "BASH_NEN", (), "t33_do_phu_cua_cong_do_duoc_THEO_HINH_DANG"),
    # N97: tai `eval` co cau lenh lai bi quet nhu `exec`.
    "bn_eval_che_do_exec": ("ops/bash_nen.py",
        "            ast.parse(van, mode=kieu)\n",
        "            ast.parse(van)  # đột biến: `eval` phân tích như `exec`\n",
        "BASH_NEN", (), "t33_do_phu_cua_cong_do_duoc_THEO_HINH_DANG"),
    # N98: chu thich LUU duoi `__future__` chi giai theo pham vi tu vung.
    "bn_chu_thich_hoan_khong_hop": ("ops/bash_nen.py",
        "                                (_giai_ten(ten, c) or _giai_ten(ten, c[:1])), vt))\n",
        "                                _giai_ten(ten, c), vt))  # đột biến: không giải theo globals module\n",
        "BASH_NEN", (), "t33_do_phu_cua_cong_do_duoc_THEO_HINH_DANG"),
    # N92b: mien tru truong co che tha CA cay con cua bo nhan.
    "ct_mien_tru_ca_cay": ("ops/cong_cu_test.py",
        "                if isinstance(g, _ast.Name):\n                    tha.add(id(g))\n",
        "                if True:\n                    tha.update(id(y) for y in _ast.walk(g))  # đột biến: tha cả cây con\n",
        "TEP_TEST", _KEM_TEP_TEST, "t39_chi_CA_PHAN_QUYET_duoc_chot_tren_rc_va_trang_thai"),
    # ── r25 — DOT BIEN cho N92/N93 (codex vong 19, sau khi chu kho quyet) ──
    # N93: ngan sach phep noi chi tinh SAU khi da gap moi ve (hanh vi r24).
    "bn_noi_ngan_sach_sau": ("ops/bash_nen.py",
        "            if tong > _NGAN_SACH_DINH_DANG:\n                raise _VuotNganSach(f\"phép nối vượt {_NGAN_SACH_DINH_DANG} ký tự\")\n",
        "            pass  # đột biến: không dừng giữa chừng\n",
        "BASH_NEN", (), "t33_do_phu_cua_cong_do_duoc_THEO_HINH_DANG"),
    # ── r24 — DOT BIEN cho N88..N91 (codex vong 18) ──
    # N88: het do sau gap hang lai coi la "khong phai bash" (fail-open, hanh vi r23).
    "bn_gap_het_sau_im": ("ops/bash_nen.py",
        "        raise _VuotNganSach(f\"biểu thức hằng lồng quá 8 tầng (dòng {getattr(nut, 'lineno', '?')})\")\n",
        "        return _KHONG_BIET  # đột biến: hết độ sâu ⇒ im\n",
        "BASH_NEN", (), "t33_do_phu_cua_cong_do_duoc_THEO_HINH_DANG"),
    # N88: chuoi `+` thoi duoc lam PHANG — moi ve tieu mot tang do sau.
    "bn_noi_khong_phang": ("ops/bash_nen.py",
        "        while isinstance(x, ast.BinOp) and isinstance(x.op, ast.Add):\n            ve.append(x.right)\n",
        "        if isinstance(x, ast.BinOp) and isinstance(x.op, ast.Add):  # đột biến: chỉ một tầng\n            ve.append(x.right)\n",
        "BASH_NEN", (), "t33_do_phu_cua_cong_do_duoc_THEO_HINH_DANG"),
    # N88: bo loc re het do sau lai loai loi goi TRUOC khi luat that duoc hoi.
    "bn_loc_re_het_sau": ("ops/bash_nen.py",
        "        return True                    # N88: hết độ sâu ⇒ để luật thật quyết (và nó NÉM)\n",
        "        return False  # đột biến: bộ lọc rẻ loại khi hết độ sâu\n",
        "BASH_NEN", (), "t33_do_phu_cua_cong_do_duoc_THEO_HINH_DANG"),
    # N89: trai `dict` thoi duoc mo.
    "bn_trai_dict_bo": ("ops/bash_nen.py",
        "                viec.extend((k, False) for k in reversed(x.keys))\n",
        "                return \"khong_biet\", None  # đột biến: trải `dict` không được mở\n",
        "BASH_NEN", (), "t33_do_phu_cua_cong_do_duoc_THEO_HINH_DANG"),
    # N89: trai `set` MOT phan tu thoi duoc mo.
    "bn_trai_set_bo": ("ops/bash_nen.py",
        "                viec.append((x.elts[0], False))\n",
        "                return \"khong_biet\", None  # đột biến: trải `set` một phần tử không được mở\n",
        "BASH_NEN", (), "t33_do_phu_cua_cong_do_duoc_THEO_HINH_DANG"),
    # N90: tu khoa `name=` cua nap dong bi bo.
    "bn_nap_dong_bo_tu_khoa": ("ops/bash_nen.py",
        '    return next((k.value for k in goi.keywords if k.arg == "name"), None)\n',
        '    return None  # đột biến: `name=` không được đọc\n',
        "BASH_NEN", (), "t33_do_phu_cua_cong_do_duoc_THEO_HINH_DANG"),
    # N90: callee TINH RA thoi duoc hoi (ca nap dong lan `exec`).
    "bn_callee_tinh_bo": ("ops/bash_nen.py",
        "    if not isinstance(f, (ast.Subscript, ast.Call)):\n        return None\n    for x in ast.walk(f):\n",
        "    if True:  # đột biến: callee tính ra không được hỏi\n        return None\n    for x in ast.walk(f):\n",
        "BASH_NEN", (), "t33_do_phu_cua_cong_do_duoc_THEO_HINH_DANG"),
    # N90: `_tai_exec` thoi hoi callee TINH RA (nap dong van hoi).
    "bn_tai_exec_bo_callee_tinh": ("ops/bash_nen.py",
        '    return _tu_trong_callee_tinh(f, ("exec", "eval"))                     # N90\n',
        '    return None  # đột biến: `exec` qua callee tính ra không được quét\n',
        "BASH_NEN", (), "t33_do_phu_cua_cong_do_duoc_THEO_HINH_DANG"),
    # ── r23 — DOT BIEN cho N83..N87 (cross-review cung nha cung cap, vong 17) ──
    # N83: rang buoc NAP DONG cho giai thoi duoc giai ⇒ moi dang gan `m = …(…)` lot.
    "bn_nap_dong_khong_giai": ("ops/bash_nen.py",
        '        if mod and ("import", mod, None) not in tap:\n',
        '        if False:  # đột biến: ràng buộc nạp động chờ giải không được giải\n',
        "BASH_NEN", (), "t33_do_phu_cua_cong_do_duoc_THEO_HINH_DANG"),
    # N83: chi giai theo CU PHAP ⇒ bi danh (`import_module as im`) lot.
    "bn_nap_dong_chi_cu_phap": ("ops/bash_nen.py",
        '        mod = _module_dong(rb[1]) or _module_dong(\n',
        '        mod = _module_dong(rb[1]) or (lambda *_a: None)(  # đột biến: chỉ cú pháp\n',
        "BASH_NEN", (), "t33_do_phu_cua_cong_do_duoc_THEO_HINH_DANG"),
    # N83: chi DICH CUOI cua phep gan day chuyen duoc rang buoc (hanh vi r22).
    "bn_gan_chi_dich_cuoi": ("ops/bash_nen.py",
        '            for dich in (n.targets if isinstance(n, ast.Assign) else [n.target]):\n',
        '            for dich in (n.targets[-1:] if isinstance(n, ast.Assign) else [n.target]):  # đột biến\n',
        "BASH_NEN", (), "t33_do_phu_cua_cong_do_duoc_THEO_HINH_DANG"),
    # N83: phep gan CO CHU THICH khong con la mot rang buoc nap dong (hanh vi r22).
    "bn_gan_bo_chu_thich": ("ops/bash_nen.py",
        '        elif isinstance(n, (ast.Assign, ast.AnnAssign, ast.NamedExpr)) \\\n',
        '        elif isinstance(n, (ast.Assign, ast.NamedExpr)) \\\n',
        "BASH_NEN", (), "t33_do_phu_cua_cong_do_duoc_THEO_HINH_DANG"),
    # N83: gia tri cua `eval` hang thoi duoc hoi.
    "bn_eval_khong_tra_module": ("ops/bash_nen.py",
        '        if isinstance(than, ast.Call):\n            return _module_dong(than, None)\n',
        '        if isinstance(than, ast.Call):\n            return None  # đột biến: `eval` hằng không trả module\n',
        "BASH_NEN", (), "t33_do_phu_cua_cong_do_duoc_THEO_HINH_DANG"),
    # N83: `importlib.__import__` roi khoi bang nap dong.
    "bn_bo_importlib_import": ("ops/bash_nen.py",
        '                 ("importlib", "__import__"): "__import__",\n',
        '',
        "BASH_NEN", (), "t33_do_phu_cua_cong_do_duoc_THEO_HINH_DANG"),
    # N83: `import builtins` khong con cho `builtins.exec` la exec.
    "bn_exec_bo_builtins": ("ops/bash_nen.py",
        '            goc.update(al.asname or "builtins" for al in n.names if al.name == "builtins")\n',
        '            pass  # đột biến: `builtins.exec` không được nhận\n',
        "BASH_NEN", (), "t33_do_phu_cua_cong_do_duoc_THEO_HINH_DANG"),
    # N83: tai `exec` KHONG gap hang — chi nhan `ast.Constant` (hanh vi r22).
    "bn_tai_khong_gap": ("ops/bash_nen.py",
        '    v = _gia_tri_hang(goi.args[0])\n',
        '    v = getattr(goi.args[0], "value", None)  # đột biến: tải không được gấp hằng\n',
        "BASH_NEN", (), "t33_do_phu_cua_cong_do_duoc_THEO_HINH_DANG"),
    # N83: tai `bytes` bi bo.
    "bn_tai_bo_bytes": ("ops/bash_nen.py",
        '    if isinstance(v, bytes):\n        from importlib.util import decode_source\n',
        '    if isinstance(v, bytes):\n        return None  # đột biến: tải `bytes` bị bỏ\n',
        "BASH_NEN", (), "t33_do_phu_cua_cong_do_duoc_THEO_HINH_DANG"),
    # N83: mo dau cua tai chi lay `import` CU PHAP muc module (hanh vi r22).
    "bn_mo_dau_cu_phap": ("ops/bash_nen.py",
        '        dau = _mo_dau_tu_bang(_bang_pham_vi_ca_cay(cay, sau))\n',
        '        dau = "".join(ast.unparse(x) + "\\n" for x in cay.body\n'
        '                      if isinstance(x, (ast.Import, ast.ImportFrom)))  # đột biến\n',
        "BASH_NEN", (), "t33_do_phu_cua_cong_do_duoc_THEO_HINH_DANG"),
    # N83 (F6): tai hang hong bi NUOT (hanh vi r22, fail-open).
    "bn_tai_hong_nuot": ("ops/bash_nen.py",
        '            raise SyntaxError(f"tải `exec`/`eval` hằng ở dòng {n.lineno} không phân tích "\n',
        '            continue  # đột biến: nuốt tải hỏng\n'
        '            raise SyntaxError(f"tải `exec`/`eval` hằng ở dòng {n.lineno} không phân tích "\n',
        "BASH_NEN", (), "t33_do_phu_cua_cong_do_duoc_THEO_HINH_DANG"),
    # N83: `exec` long qua tran thoi fail-close.
    "bn_exec_long_im": ("ops/bash_nen.py",
        '    if cac_tai and sau >= _SAU_EXEC:\n',
        '    if False:  # đột biến: lồng quá trần không ném\n',
        "BASH_NEN", (), "t33_do_phu_cua_cong_do_duoc_THEO_HINH_DANG"),
    # N84 (F5): bo duyet quay ve DE QUY Python.
    "bn_tham_de_quy": ("ops/bash_nen.py",
        '            chong.extend((x, chuoi, hop, luu, vt, sau_chuoi) for x in ast.iter_child_nodes(con))\n',
        '            [tham(x, chuoi) for x in ast.iter_child_nodes(con)]  # đột biến: đệ quy\n',
        "BASH_NEN", (), "t33_do_phu_cua_cong_do_duoc_THEO_HINH_DANG"),
    # N85 (F3): argv NOI khong con duoc mo.
    "bn_argv_khong_mo_noi": ("ops/bash_nen.py",
        '            if isinstance(x, ast.BinOp) and isinstance(x.op, ast.Add):\n',
        '            if False:  # đột biến: argv nối không được mở\n',
        "BASH_NEN", (), "t33_do_phu_cua_cong_do_duoc_THEO_HINH_DANG"),
    # N85 (F3): argv TRAI khong con duoc mo.
    "bn_argv_khong_mo_trai": ("ops/bash_nen.py",
        '        elif isinstance(x, ast.Starred):\n            viec.append((x.value, True))\n',
        '        elif isinstance(x, ast.Starred):\n            return "khong_biet", None  # đột biến\n',
        "BASH_NEN", (), "t33_do_phu_cua_cong_do_duoc_THEO_HINH_DANG"),
    # N86 (F7): `%` voi ve phai `dict` thoi duoc gap.
    "bn_phan_tram_bo_dict": ("ops/bash_nen.py",
        '                and isinstance(ph, (str, bytes, int, float, tuple, dict)):\n',
        '                and isinstance(ph, (str, bytes, int, float, tuple)):  # đột biến\n',
        "BASH_NEN", (), "t33_do_phu_cua_cong_do_duoc_THEO_HINH_DANG"),
    # N92 (r25): danh sach CHO PHEP tha MOI truong — truong co che lan truong tong hop deu im.
    "ct_bo_get_truong": ("ops/cong_cu_test.py",
        '            if isinstance(khoa, str) and khoa not in _TRUONG_TONG_HOP:\n',
        '            if False:  # đột biến: không tha trường cơ chế nào\n',
        "TEP_TEST", _KEM_TEP_TEST, "t39_chi_CA_PHAN_QUYET_duoc_chot_tren_rc_va_trang_thai"),
    # N87 (F4): bi danh TRUONG TONG HOP thoi mang nguon `tt`.
    "ct_bo_bi_danh_truong": ("ops/cong_cu_test.py",
        '            return {"tt"}                  # N87: tên mang GIÁ TRỊ một trường tổng hợp\n',
        '            return {"khac"}  # đột biến: bí danh trường tổng hợp không mang nguồn\n',
        "TEP_TEST", _KEM_TEP_TEST, "t39_chi_CA_PHAN_QUYET_duoc_chot_tren_rc_va_trang_thai"),
    # ── r22 — DOT BIEN cho N78b/c, N80..N82 (cross-review codex vong 16, sau khi DOI KIEN TRUC bo chot) ──
    # RUT O r22, kem ly do DO DUOC: 11 dot bien mo phong NHANH/PHAM VI/VI TRI cua bo chot (ct_with_nuot_khong_dieu_khien, ct_xuat_xu_gop_pham_vi, ct_xuat_xu_mot_nguon, ct_comprehension_khong_pham_vi,
    # ct_except_sao_loai_tru, ct_assert_warns_nuot, ct_finally_la_nhanh, ct_lop_nhin_thay_tu_ham,
    # ct_khong_loai_tru, ct_khong_quay_lui, ct_xuat_xu_khong_theo_vi_tri) — ma dich cua chung (N64/N69/N75/N79)
    # DA GO theo N80. Dot bien tren ma khong con ton tai thi khong neo duoc.
    # N80: walrus thoi la mot dang rang buoc ghi nguon.
    "ct_bo_walrus_rang_buoc": ("ops/cong_cu_test.py",
        "        if isinstance(nut, (_ast.AnnAssign, _ast.AugAssign, _ast.NamedExpr)):\n",
        "        if isinstance(nut, (_ast.AnnAssign, _ast.AugAssign)):  # đột biến: `:=` không ghi nguồn\n",
        "TEP_TEST", _KEM_TEP_TEST, "t39_chi_CA_PHAN_QUYET_duoc_chot_tren_rc_va_trang_thai"),
    # N80: dich comprehension thoi ghi nguon tu iterable.
    "ct_bo_comprehension_rang_buoc": ("ops/cong_cu_test.py",
        "        if isinstance(nut, (_ast.For, _ast.AsyncFor, _ast.comprehension)):\n",
        "        if isinstance(nut, (_ast.For, _ast.AsyncFor)):  # đột biến: đích comprehension không ghi nguồn\n",
        "TEP_TEST", _KEM_TEP_TEST, "t39_chi_CA_PHAN_QUYET_duoc_chot_tren_rc_va_trang_thai"),
    # N80: lap tren danh sach HANG thoi lay nguon tung phan tu.
    "ct_lap_bo_phan_tu_hang": ("ops/cong_cu_test.py",
        "            if isinstance(g, (_ast.List, _ast.Tuple, _ast.Set)):\n",
        "            if False:  # đột biến: lặp trên danh sách hằng không lấy nguồn từng phần tử\n",
        "TEP_TEST", _KEM_TEP_TEST, "t39_chi_CA_PHAN_QUYET_duoc_chot_tren_rc_va_trang_thai"),
    # N81: bo nhan NAP DONG (`__import__(…)`, `importlib.import_module(…)`) thoi duoc giai.
    "bn_bo_nap_dong_nhan": ("ops/bash_nen.py",
        "        mod = _module_dong(nut.func.value, tra_ten)          # N81 — bộ nhận NẠP ĐỘNG\n",
        "        mod = None  # đột biến: bộ nhận nạp động không được giải\n",
        "BASH_NEN", (), "t33_do_phu_cua_cong_do_duoc_THEO_HINH_DANG"),
    # N81: `__import__` bi CHE van duoc coi la ham dung san.
    "bn_nap_dong_khong_hoi_che": ("ops/bash_nen.py",
        '        if f.id in ("__import__", "eval") and (tra_ten is None\n',
        '        if f.id in ("__import__", "eval") and (True  # đột biến: không hỏi `__import__` có bị che không\n',
        "BASH_NEN", (), "t33_do_phu_cua_cong_do_duoc_THEO_HINH_DANG"),
    # N81: `m = __import__("subprocess")` thoi rang buoc `m` vao module.
    "bn_nap_dong_gan_ten_bo": ("ops/bash_nen.py",
        '                    them(dich.id, ("dong", n.value, id(pham_vi)))\n',
        '                    them(dich.id, ("khac",))  # đột biến: `m = __import__(…)` không ràng buộc module\n',
        "BASH_NEN", (), "t33_do_phu_cua_cong_do_duoc_THEO_HINH_DANG"),
    # N81: rang buoc do `exec("import …")` hang sinh ra thoi vao bang module.
    "bn_exec_khong_rang_buoc": ("ops/bash_nen.py",
        "            for ten, rb in _bang_pham_vi_ca_cay(tai, sau + 1)[id(tai)][0].items():\n",
        "            for ten, rb in {}.items():  # đột biến: ràng buộc của `exec` hằng không vào bảng module\n",
        "BASH_NEN", (), "t33_do_phu_cua_cong_do_duoc_THEO_HINH_DANG"),
    # N81: loi goi bash NAM TRONG tai `exec` hang thoi duoc quet.
    "bn_exec_khong_quet_tai": ("ops/bash_nen.py",
        "            so_tai[id(goi)] = ((goi.lineno, goi.col_offset), len(_loi_goi_tran(dau + van, sau + 1)))\n",
        "            so_tai[id(goi)] = ((goi.lineno, goi.col_offset), 0)  # đột biến: không quét lời gọi trong tải `exec`\n",
        "BASH_NEN", (), "t33_do_phu_cua_cong_do_duoc_THEO_HINH_DANG"),
    # N82: chu so huu `nonlocal` dung o ham GIUA cung khai `nonlocal`.
    "bn_nonlocal_dung_o_giua": ("ops/bash_nen.py",
        "                                         and ten not in bang[j][2]):\n",
        "                                         ):  # đột biến: dừng ở hàm giữa cũng khai `nonlocal`\n",
        "BASH_NEN", (), "t33_do_phu_cua_cong_do_duoc_THEO_HINH_DANG"),
    # N82: `global str` CHI DOC lai che ten dung san `str`.
    "bn_global_doc_khong_van_che": ("ops/bash_nen.py",
        "            return ten in chuoi[0][1]\n",
        "            return True  # đột biến: `global` chỉ đọc vẫn che tên dựng sẵn\n",
        "BASH_NEN", (), "t33_do_phu_cua_cong_do_duoc_THEO_HINH_DANG"),
    # N78b: do rong co qua nhieu chu so lai di thang vao `int()` (ValueError).
    "bn_so_dai_khong_chan": ("ops/bash_nen.py",
        "        if len(dac_ta) > len(str(_NGAN_SACH_DINH_DANG)):\n",
        "        if False:  # đột biến: không chặn số quá dài trước `int()`\n",
        "BASH_NEN", (), "t33_do_phu_cua_cong_do_duoc_THEO_HINH_DANG"),
    # ── r21 — DOT BIEN cho N76..N79 (cross-review codex vong 15, sau khi DOI KIEN TRUC) ──
    # RUT O r21, kem ly do DO DUOC: 13 dot bien mo phong THU TU/NHANH (bn_lop_neo_dau_than, bn_nhanh_khong_loai_tru, bn_khong_quay_lui, bn_finally_la_nhanh,
    # bn_lop_khong_chay_ngay, bn_lop_chua_gan_khong_gop, bn_lop_chua_gan_khong_hoi_ngoai, bn_nhanh_cung_thong_tri, bn_khong_muon_nhat_thang,
    # bn_neo_cho_viet_ten, bn_module_khong_theo_thu_tu, bn_ham_cung_theo_thu_tu, bn_ham_unbound_ra_ngoai) — ma dich cua chung
    # (N46/N53/N60/N67/N72) DA GO theo N76. Mot dot bien tren ma khong con ton tai thi khong
    # neo duoc, va giu no lai la giu mot con so khong do gi.
    # N76: than lop THAY THE pham vi bao thay vi gop ⇒ `lop_gan_SAU` (lop doc `import` toan cuc truoc khi tu gan) lot.
    "bn_lop_khong_gop_bao": ("ops/bash_nen.py",
        "            if la_lop:\n                continue                   # thân lớp: gộp với phạm vi bao, không thay thế\n",
        "",
        "BASH_NEN", (), "t33_do_phu_cua_cong_do_duoc_THEO_HINH_DANG"),
    # N76: quay ve 'mo ho ⇒ khong bao' — meo che ten tat duoc cong; `t33` (4) do dung dieu ay.
    "bn_mot_rang_buoc_thay_bat_ky": ("ops/bash_nen.py",
        "    if len(cac) == 1:\n        (rb,) = cac\n",
        "    if len(cac) == 1 and len(tap) == 1:  # đột biến: đòi MỌI ràng buộc là import (mơ hồ ⇒ im)\n        (rb,) = cac\n",
        "BASH_NEN", (), "t33_do_phu_cua_cong_do_duoc_THEO_HINH_DANG"),
    # N76 (G7 vong 15): pham vi chu thich PEP 695 trong than lop thoi nhin thay lop ay.
    "bn_alias_khong_thay_lop": ("ops/bash_nen.py",
        "    return not chuoi[i + 1][4]\n",
        "    return True  # đột biến: phạm vi chú thích PEP 695 không thấy lớp bao\n",
        "BASH_NEN", (), "t50_PEP695_type_params_phai_duoc_tham_va_phai_CHE_duoc"),
    # N76 (G6 vong 15): dich walrus trong comprehension lai thanh rang buoc CUC BO cua comprehension.
    "bn_walrus_comp_la_cuc_bo": ("ops/bash_nen.py",
        "        if id(n) in bo_qua:\n            continue\n",
        "",
        "BASH_NEN", (), "t33_do_phu_cua_cong_do_duoc_THEO_HINH_DANG"),
    # N77 (G4 vong 15): chu thich tren dich KHONG DON duoi `__future__` (khong tinh, khong luu) van bi quet.
    "bn_dich_khong_don_future_van_quet": ("ops/bash_nen.py",
        "                or (hoan_chu_thich and not con.simple)):\n",
        "                or False):  # đột biến: chú thích trên đích không đơn vẫn quét dưới `__future__`\n",
        "BASH_NEN", (), "t33_do_phu_cua_cong_do_duoc_THEO_HINH_DANG"),
    # N78 (G5 vong 15): ngan sach khuech dai tinh tung o thay vi cong don.
    "bn_ngan_sach_tung_o": ("ops/bash_nen.py",
        "            tong += rong\n",
        "            tong = max(tong, rong)  # đột biến: ngân sách tính TỪNG Ô, không cộng dồn\n",
        "BASH_NEN", (), "t33_do_phu_cua_cong_do_duoc_THEO_HINH_DANG"),
    # ── r20 — DOT BIEN cho N72..N75 (cross-review codex vong 14) ─────────────────
    # N74: `_chay_phep` quay ve LIET KE kieu ngoai le ⇒ `OverflowError` di thang ra ngoai.
    "bn_chay_phep_liet_ke": ("ops/bash_nen.py",
        "    except Exception:\n        return _KHONG_BIET\n\n\ndef _kiem_ngan_sach_dinh_dang",
        "    except (TypeError, ValueError, KeyError):  # đột biến: liệt kê kiểu ngoại lệ\n        return _KHONG_BIET\n\n\ndef _kiem_ngan_sach_dinh_dang",
        "BASH_NEN", (), "t33_do_phu_cua_cong_do_duoc_THEO_HINH_DANG"),
    # N74: bo ngan sach khuech dai ⇒ `%05000d` duoc chay thu va coi la 'khong phai bash'.
    "bn_bo_ngan_sach": ("ops/bash_nen.py",
        '    van = mau.decode("latin-1") if isinstance(mau, bytes) else mau\n',
        '    return  # đột biến: không kiểm ngân sách khuếch đại\n    van = mau.decode("latin-1") if isinstance(mau, bytes) else mau\n',
        "BASH_NEN", (), "t33_do_phu_cua_cong_do_duoc_THEO_HINH_DANG"),
    # N74: `quet` quay ve LIET KE kieu ngoai le ⇒ bo quet nem la cong SAP, khong KHONG_DO_DUOC.
    "bn_quet_liet_ke_ngoai_le": ("ops/bash_nen.py",
        "        except Exception as e:             # noqa: BLE001 — có chủ đích, xem N74\n",
        "        except (SyntaxError, ValueError) as e:  # đột biến: liệt kê kiểu ngoại lệ\n",
        "BASH_NEN", (), "t44_khong_lay_duoc_INDEX_thi_KHONG_DO_DUOC_chu_khong_lui_ve_rglob"),
    # ── r17 — DOT BIEN cho N52..N57 (cross-review codex vong 11) ─────────────────
    # N52: bo tinh hang thoi rut gon HANG DUNG SAN (list/tuple/set/chuoi) => moi hinh dang
    # bao chua deu lot, ke ca `["bash"]`.
    # ── RÚT Ở r17 — nhánh bị đột biến ĐÃ GỠ vì là MÃ CHẾT ─────────────────────
    # `bn_khong_rut_gon_bao_chua` tắt nhánh rút gọn bao chứa trong `_gia_tri_hang`. Nó SỐNG
    # SÓT, và đó là dấu hiệu ĐO ĐƯỢC rằng không đường nào đi tới nhánh ấy: `ast.literal_eval`
    # đã phủ bao chứa hằng, còn bao chứa cần GẤP thì `_la_vec_bash` mở theo CÚ PHÁP trước khi
    # tới đây. Nhánh đã gỡ khỏi `bash_nen.py`; không dựng lại đột biến cho mã không còn.
    # N52: thoi gap phep NOI hang => `"ba" + "sh"` lot.
    "bn_khong_gap_noi_hang": ("ops/bash_nen.py",
        "    if isinstance(nut, ast.BinOp) and isinstance(nut.op, ast.Add):\n",
        "    if False:  # đột biến: phép nối hằng không được gấp\n",
        "BASH_NEN", (), "t33_do_phu_cua_cong_do_duoc_THEO_HINH_DANG"),
    # N52: tap NHIEU phan tu bi coi nhu mot phan tu => BAT OAN.
    "bn_tap_nhieu_phan_tu_van_tinh": ("ops/bash_nen.py",
        "        return len(nut.elts) == 1 and _la_ten_bash(nut.elts[0], tra_ten)\n",
        "        return bool(nut.elts) and _la_ten_bash(nut.elts[0], tra_ten)"
        "  # đột biến: tập nhiều phần tử vẫn tính\n",
        "BASH_NEN", (), "t33_do_phu_cua_cong_do_duoc_THEO_HINH_DANG"),
    # N52/F3: nhanh shell lai nhan path-like => BAO DONG GIA quay lai.
    "bn_shell_ra_nhan_path": ("ops/bash_nen.py",
        "            dinh = _la_ten_bash(dau, tra_ten, cho_duong=False)\n",
        "            dinh = _la_ten_bash(dau, tra_ten)  # đột biến: helper shell nhận path-like\n",
        "BASH_NEN", (), "t33_do_phu_cua_cong_do_duoc_THEO_HINH_DANG"),
    # N52: bo loc RE hep hon luat that => luat that KHONG BAO GIO duoc hoi.
    "bn_loc_re_hep_hon_luat": ("ops/bash_nen.py",
        "    if isinstance(nut, ast.BinOp) and isinstance(nut.op, ast.Add):\n"
        "        return True                    # phép nối hằng: để luật thật quyết\n",
        "    if False:  # đột biến: bộ lọc rẻ hẹp hơn luật thật\n"
        "        return True\n",
        "BASH_NEN", (), "t33_do_phu_cua_cong_do_duoc_THEO_HINH_DANG"),
    # N54: phep hien thi thoi don anh => hai duong khac nhau de nhau o `ly_do`.
    "bn_hien_thi_khong_don_anh": ("ops/bash_nen.py",
        '    rel = rel.replace("\\\\", "\\\\\\\\")\n',
        "    pass  # đột biến: phép hiển thị thôi đơn ánh\n",
        "BASH_NEN", (), "t49_duong_XAU_ra_JSON_HOP_LE_va_NGAY_GO_phai_duoc_DOC"),
    # N57: `PATH` VANG lai bi gop vao `PATH` RONG.
    "bn_path_vang_thanh_rong": ("ops/bash_nen.py",
        '        path = env["PATH"] if "PATH" in env else os.defpath\n',
        '        path = env.get("PATH", "")  # đột biến: PATH vắng bị gộp vào PATH rỗng\n',
        "BASH_NEN", (), "t51_cache_phai_HET_HIEU_LUC_khi_chinh_TEP_ung_vien_doi"),
    # N55: ratchet thoi doc XUAT XU cua bao cao => truong co che bi bat oan.
    "ct_khong_theo_xuat_xu_bao": ("ops/cong_cu_test.py",
        '        return any(id(x) not in tha and (la_quet(x) or (isinstance(x, _ast.Name)\n',
        '        return any(id(x) not in tha and (la_quet(x) or (isinstance(x, _ast.Name) and True or isinstance(x, _ast.Name)  # đột biến: không hỏi xuất xứ của báo cáo\n',
        "TEP_TEST", _KEM_TEP_TEST, "t39_chi_CA_PHAN_QUYET_duoc_chot_tren_rc_va_trang_thai"),
    # ── r16 — DOT BIEN cho N45..N51 (cross-review codex vong 10) ─────────────────
    # N45, chieu LOT: hai helper chay qua shell roi khoi tap duoc che.
    "bn_bo_shell_ra": ("ops/bash_nen.py",
        '_TEN_SHELL_RA = ("getoutput", "getstatusoutput")\n',
        '_TEN_SHELL_RA = ()  # đột biến: helper chạy qua shell không được che\n',
        "BASH_NEN", (), "t33_do_phu_cua_cong_do_duoc_THEO_HINH_DANG"),
    # N45, chieu LOT: ten chuong trinh boc `pathlib` khong duoc tinh.
    "bn_pathlib_khong_la_ten": ("ops/bash_nen.py",
        "    if isinstance(nut, ast.Call) and tra_ten is not None:\n",
        "    if False:  # đột biến: hàm dựng `pathlib` không rút gọn ra tên được\n",
        "BASH_NEN", (), "t33_do_phu_cua_cong_do_duoc_THEO_HINH_DANG"),
    # N45, chieu BAT OAN: nhan bua moi lenh goi mot doi so, khong hoi callee tro vao dau.
    "bn_pathlib_khong_giai_callee": ("ops/bash_nen.py",
        "def _la_dung_duong(f, tra_ten):\n",
        "def _la_dung_duong(f, tra_ten):\n    return True  # đột biến: mọi callee đều là hàm dựng `pathlib`\n",
        "BASH_NEN", (), "t33_do_phu_cua_cong_do_duoc_THEO_HINH_DANG"),
    # N47: `type X[T] = ...` thoi la mot pham vi ⇒ `T` ro ri ra pham vi chua.
    "bn_alias_khong_mo_pham_vi": ("ops/bash_nen.py",
        '    x for x in (getattr(ast, "TypeAlias", None),) if x is not None)\n',
        "    x for x in () if x is not None)  # đột biến: alias generic không mở phạm vi\n",
        "BASH_NEN", (), "t50_PEP695_type_params_phai_duoc_tham_va_phai_CHE_duoc"),
    # N48, lop TRUONG: nhanh LOI nhet duong THO vao `ly_do` (lop `_ra_json` van con).
    "bn_loi_ra_duong_tho": ("ops/bash_nen.py",
        '                                      "ly_do": "không đọc/phân tích được "\n                                               f"{_duong_bao_cao(rel)}: "\n',
        '                                      "ly_do": f"không đọc/phân tích được {rel}: "  # đột biến: đường THÔ ở lối ra lỗi\n',
        "BASH_NEN", (), "t49_duong_XAU_ra_JSON_HOP_LE_va_NGAY_GO_phai_duoc_DOC"),
    # N48, lop BIEN GIOI: `_ra_json` thoi bao dam ASCII (lop `_duong_bao_cao` van con).
    "bn_json_khong_ascii": ("ops/bash_nen.py",
        "    return json.dumps(bao, ensure_ascii=True, indent=2)\n",
        "    return json.dumps(bao, ensure_ascii=False, indent=2)  # đột biến: biên giới JSON "
        "không còn thuần ASCII\n",
        "BASH_NEN", (), "t49_duong_XAU_ra_JSON_HOP_LE_va_NGAY_GO_phai_duoc_DOC"),
    # N49: `assert` tran lai thanh cua hau ra khoi ratchet.
    "ct_bo_nhanh_assert": ("ops/cong_cu_test.py",
        "        elif isinstance(nut, _ast.Assert):\n",
        "        elif False:  # đột biến: `assert` trần không còn là một phép chốt\n",
        "TEP_TEST", _KEM_TEP_TEST, "t39_chi_CA_PHAN_QUYET_duoc_chot_tren_rc_va_trang_thai"),
    # N49: ratchet quay ve khop DUNG chu `rc`, nen doi ten bien la thoat. (NEO LAI O r22 vao N80.)
    "ct_chi_ten_rc": ("ops/cong_cu_test.py",
        "                ghi(d.id, x)\n",
        '                ghi(d.id, "khac")  # đột biến: không đi theo xuất xứ của `_quet`\n',
        "TEP_TEST", _KEM_TEP_TEST, "t39_chi_CA_PHAN_QUYET_duoc_chot_tren_rc_va_trang_thai"),
    # N50: ly do mien tru tro lai thanh mot loi khai khong ai doc.
    "ct_ly_do_khong_doc": ("ops/cong_cu_test.py",
        "    return not (isinstance(v, str) and v.strip())\n",
        "    return False  # đột biến: lý do miễn trừ không được đọc\n",
        "TEP_TEST", _KEM_TEP_TEST, "t39_chi_CA_PHAN_QUYET_duoc_chot_tren_rc_va_trang_thai"),
    # r13 — ba dot bien cho N36/N37/N38.
    # THU HEP sau mot phep do: ban dau dot bien them `text=True` vao lenh git, va the la
    # `pc.stdout` thanh `str` con cho tach van `.split(b"\\0")` => TypeError => GIAN GIAO SAP,
    # giet 8 ca. Do la dot bien QUA RONG, khong phai phep do thuoc tinh. Ban nay mo phong DUNG
    # va CHI phep dich dong pho quat, tren DUONG DAN, giu nguyen moi kieu du lieu.
    "bn_khung_dich_dong": ("ops/bash_nen.py",
        '                    rel = rel_b.decode("utf-8", "surrogateescape")\n',
        '                    rel = rel_b.decode("utf-8", "surrogateescape").replace("\\r", "\\n")  # đột biến: dịch dòng phổ quát\n',
        "BASH_NEN", (), "t48_khung_INDEX_giu_BYTES_va_anh_chup_ghim_BLOB"),
    "bn_anh_chup_chi_dem_so": ("ops/bash_nen.py",
        "            if thay_oid != ghim:\n",
        "            if False:  # đột biến: ảnh chụp chỉ đếm số, không ghim blob\n",
        "BASH_NEN", (), "t48_khung_INDEX_giu_BYTES_va_anh_chup_ghim_BLOB"),
    # N37: bieu thuc luc dinh nghia (mac dinh, decorator…) giai o pham vi TRONG. (NEO LAI O r21.)
    "bn_dinh_nghia_giai_o_pham_vi_trong": ("ops/bash_nen.py",
        "                chong.extend((x, chuoi, hop or (hoan_chu_thich and id(x) in luu_ct),\n",
        "                chong.extend((x, chuoi_trong, hop or (hoan_chu_thich and id(x) in luu_ct),  # đột biến: biểu thức lúc định nghĩa giải ở phạm vi TRONG\n",
        "BASH_NEN", (), "t33_do_phu_cua_cong_do_duoc_THEO_HINH_DANG"),
    # r12 — BON dot bien cho bon mat cua "doc INDEX cho dung" (N32..N35), deu ve `t47`.
    "bn_theo_ref_thay_the": ("ops/bash_nen.py",
        # NEO LAI O r37: N125 cho `_chay_git` chon `Popen`/`run` qua `mo_luong`.
        '    env["GIT_NO_REPLACE_OBJECTS"] = "1"\n'
        '    chay = subprocess.Popen if kw.pop("mo_luong", False) else subprocess.run   # N125 — đọc THEO LUỒNG\n'
        '    return chay(["git", "--no-replace-objects", "-C", str(goc), *doi_so],\n',
        '    chay = subprocess.Popen if kw.pop("mo_luong", False) else subprocess.run\n'
        '    return chay(["git", "-C", str(goc), *doi_so],  # đột biến: nghe ref thay thế của MÁY\n',
        "BASH_NEN", (), "t47_INDEX_phai_duoc_doc_TRUNG_THUC_va_nguon_py_nhan_du_moi_cach_viet"),
    "bn_bo_qua_stage": ("ops/bash_nen.py",
        '                    if truong[2] != "0":\n',
        '                    if False:  # đột biến: nhận cả stage 1/2/3, SHA lớn nhất thắng\n',
        "BASH_NEN", (), "t47_INDEX_phai_duoc_doc_TRUNG_THUC_va_nguon_py_nhan_du_moi_cach_viet"),
    "bn_giai_ma_cung_utf8": ("ops/bash_nen.py",
        "    ma, _ = tokenize.detect_encoding(io.BytesIO(raw).readline)\n",
        '    ma = "utf-8"  # đột biến: giả định MỘT mã hoá, bỏ PEP 263 và BOM\n',
        "BASH_NEN", (), "t47_INDEX_phai_duoc_doc_TRUNG_THUC_va_nguon_py_nhan_du_moi_cach_viet"),
    "bn_duoi_theo_mot_cach_viet": ("ops/bash_nen.py",
        "    return rel.casefold().endswith(_DUOI_PY)\n",
        '    return rel.endswith(".py")  # đột biến: một cách viết, bỏ HOA và `.pyw`\n',
        "BASH_NEN", (), "t47_INDEX_phai_duoc_doc_TRUNG_THUC_va_nguon_py_nhan_du_moi_cach_viet"),
    # r11 — N28: NOI DUNG cung tu INDEX, va moi truong git bi SCRUB. Hai mat, hai dot bien.
    "bn_doc_cay_lam_viec": ("ops/bash_nen.py",
        "    if nguon_tep != \"git\":\n",
        "    if True:  # đột biến: đọc cây làm việc, symlink lại trỏ ra ngoài kho\n",
        "BASH_NEN", (), "t46_noi_dung_lay_tu_INDEX_chu_khong_tu_cay_lam_viec"),
    "bn_giu_bien_git_ke_thua": ("ops/bash_nen.py",
        "    for k in da_go:\n        moi.pop(k, None)\n",
        "    da_go = []  # đột biến: giữ nguyên GIT_INDEX_FILE/GIT_DIR kế thừa\n",
        "BASH_NEN", (), "t46_noi_dung_lay_tu_INDEX_chu_khong_tu_cay_lam_viec"),
    # r11 — N29: pham vi ton trong `global`/`nonlocal` va walrus trong comprehension.
    "bn_bo_qua_global_nonlocal": ("ops/bash_nen.py",
        "    for i in thu_tu[1:]:\n",
        "    for i in []:  # đột biến: thôi chuyển ràng buộc `global`/`nonlocal` về chủ sở hữu\n",
        "BASH_NEN", (), "t33_do_phu_cua_cong_do_duoc_THEO_HINH_DANG"),
    "bn_bo_qua_walrus_comprehension": ("ops/bash_nen.py",
        "                for x in _dich_walrus(n):\n",
        "                for x in []:  # đột biến: walrus trong comprehension không trồi ra\n",
        "BASH_NEN", (), "t33_do_phu_cua_cong_do_duoc_THEO_HINH_DANG"),
    # r11 — N30: hang chuong trinh so theo MOI KIEU BIEU DIEN.
    "bn_bo_hang_byte": ("ops/bash_nen.py",
        "    if isinstance(v, bytes):\n",
        "    if False:  # đột biến: b\"bash\" không phải hằng bash\n",
        "BASH_NEN", (), "t33_do_phu_cua_cong_do_duoc_THEO_HINH_DANG"),
    # r11 — N31: cong phai duoc NOI vao diem vao ma CI goi. Dot bien tren TEP TEST, qua cua
    # `--tu-kiem-cong-that`, nen `bp` la TEP_TEST.
    "t45_cong_khong_noi": (str(TEP_TEST.relative_to(GOC)),
        "    rc, bao = _quet(goc, bo_quet)\n",
        "    rc, bao = (0, {})  # đột biến: điểm vào KHÔNG chạy cổng trên cây thật\n",
        "TEP_TEST", _KEM_TEP_TEST, "t45_bo_ca_phai_CHAY_cong_tren_cay_THAT_chu_khong_chi_cay_gia"),
    "t45_cong_noi_ma_khong_neu_ten": (str(TEP_TEST.relative_to(GOC)),
        '    return 1, [f"CỔNG TRÊN CÂY THẬT: {nhan} (rc={rc})",\n'
        '               f"    {str(bao.get(\'ly_do\'))[:400]}"]\n',
        '    return 1, [f"CỔNG TRÊN CÂY THẬT: {nhan}"]  # đột biến: giấu tên tệp vi phạm\n',
        "TEP_TEST", _KEM_TEP_TEST, "t45_bo_ca_phai_CHAY_cong_tren_cay_THAT_chu_khong_chi_cay_gia"),
    "bn_khong_giai_callee": ("ops/bash_nen.py",
        "        loai = _loai_loi_goi(nut, tra_ten)\n",
        "        loai = _loai_theo_TEN_khong_giai_callee(nut)  # đột biến: nhận theo TÊN\n",
        "BASH_NEN", (), "t33_do_phu_cua_cong_do_duoc_THEO_HINH_DANG"),
    # r14 — THAY dot bien `t39_bo_phep_so_bang`: dong no neo (`isinstance(o, _ast.Eq)`) khong
    # con, vi luat nay khong doi phep so BANG nua. Hai dot bien duoi troi HAI CHIEU cua luat
    # MOI, va chieu thu hai moi la chieu de quen.
    # (a) THU HEP ve luat cu (chi chieu DO, chi phep so bang) => dung ba lan lap `t45`/`t47`/
    #     `t48` chui qua duoc. Mau `rc_bang_0`, `ne_rc`, `ne_tt`, `ngoai_ds` phai DOI.
    "t39_thu_hep_ve_chieu_DO": (str(TEP_TEST.relative_to(GOC)),
        '            if isinstance(n, _ast.Name) and nguon_tap(n.id, vt, dieu_kien) & {"ma", "tt"}:\n'
        '                return True\n',
        '            if isinstance(n, _ast.Name) and n.id == "rc":\n'
        '                return True  # đột biến: về luật cũ, khớp đúng CHỮ `rc`\n',
        "TEP_TEST", _KEM_TEP_TEST, "t39_chi_CA_PHAN_QUYET_duoc_chot_tren_rc_va_trang_thai"),
    # (b) NOI QUA: gom ca TRUONG CO CHE vao => `truong_co_che`/`lech_oid` bi bat OAN, va moi ca
    #     doc `co_loi_goi_tran` phai chui vao `CA_PHAN_QUYET`. Mot luat bat oan la luat se bi
    #     tat, va khi ay ca ba lan lap kia quay lai — day la chieu r7 da so, nen phai co ca giu.
    "t39_noi_qua_sang_truong_co_che": (str(TEP_TEST.relative_to(GOC)),
        '_TRUONG_TONG_HOP = ("trang_thai", "ngoai_danh_sach", "ly_do")\n',
        '_TRUONG_TONG_HOP = ("trang_thai", "ngoai_danh_sach", "ly_do",\n'
        '                    "co_loi_goi_tran", "lech_oid_dong_cung")  # đột biến: nới quá\n',
        "TEP_TEST", _KEM_TEP_TEST, "t39_chi_CA_PHAN_QUYET_duoc_chot_tren_rc_va_trang_thai"),
    # HAI DOT BIEN CHO CHINH LUAT N22 — mot luat khong the DO thi khong phai luat.
    # Chung dot bien TEP TEST, nen `bp` la `TEP_TEST` chu khong phai `BASH_NEN`.
    "t39_bo_phep_quet": (str(TEP_TEST.relative_to(GOC)),
        "    if not any(la_quet(n) for n in _ast.walk(cay)):\n        return []\n",
        "    return []  # đột biến: luật N22 thôi quét, ca nào cũng lọt\n",
        "TEP_TEST", _KEM_TEP_TEST, "t39_chi_CA_PHAN_QUYET_duoc_chot_tren_rc_va_trang_thai"),
    # CHIEU NGUOC khong the do bang cach GO phep kiem: tren cay SACH khong co ten chet nao
    # de no bat, nen go di van xanh — dung bai toan `t26` da gap voi ratchet. Nen dot bien nay
    # TAO ra thu chieu nguoc sinh ra de bat: mot ten nam trong danh sach ma KHONG con chot DO
    # nao. `t27` la ca AM (khang dinh cong KHONG do) nen no dung la mot "bia mo" hoan hao.
    "t39_de_ten_chet_trong_danh_sach": (str(TEP_TEST.relative_to(GOC)),
        "CA_PHAN_QUYET = {\n",
        'CA_PHAN_QUYET = {\n    "t27_cong_khong_bao_dong_gia_tren_CHU_THICH": "đột biến: tên CHẾT",\n',
        "TEP_TEST", _KEM_TEP_TEST, "t39_chi_CA_PHAN_QUYET_duoc_chot_tren_rc_va_trang_thai"),
    # r8 — BA dot bien cho co che "ca do o NEN" (`t42`), tren TEP TEST, qua cua `--tu-kiem-nen-do`.
    "bn_nen_do_van_tinh_vao_ban_kinh": (str(TEP_TEST.relative_to(GOC)),
        "    ket = {t: v for t, v in ket.items() if t not in loai}\n",
        "    ket = dict(ket)  # đột biến: ca đỏ ở nền vẫn tính vào bán kính\n",
        "TEP_TEST", _KEM_TEP_TEST, "t42_ca_do_o_NEN_bi_loai_khoi_ban_kinh_va_van_keo_ma_thoat"),
    "bn_nen_do_dich_khong_nhan_ra": (str(TEP_TEST.relative_to(GOC)),
        "    if ca_dich in loai:\n",
        "    if False:  # đột biến: đích đỏ ở nền không được nhận ra, rơi vào nhánh chung\n",
        "TEP_TEST", _KEM_TEP_TEST, "t42_ca_do_o_NEN_bi_loai_khoi_ban_kinh_va_van_keo_ma_thoat"),
    "bn_nen_do_lang_le_xanh": (str(TEP_TEST.relative_to(GOC)),
        "    return dong_nen, 1\n",
        "    return dong_nen, 0  # đột biến: đỏ ở nền lặng lẽ thành xanh\n",
        "TEP_TEST", _KEM_TEP_TEST, "t42_ca_do_o_NEN_bi_loai_khoi_ban_kinh_va_van_keo_ma_thoat"),
    "bn_quet_theo_chuoi": ("ops/bash_nen.py",
        "            dong = _loi_goi_tran(than)\n",
        "            dong = [i for i, l in enumerate(than.splitlines(), 1)\n"
        "                    if 'which(\"bash\")' in l]  # đột biến: đo CHUỖI, không đo cấu trúc\n",
        "BASH_NEN", (), "t27_cong_khong_bao_dong_gia_tren_CHU_THICH"),
    # #668 CI-G5-CONG-CU-CHIA-MANH: mỗi chốt gom/ghi/chế độ một đột biến riêng; ca đích đòi THẺ riêng của chốt.
    'f6_main_mat_gia_tri': ("ops/cong_cu_test.py",
        '            ket.update(nhan or {})\n',
        '            ket.update({t: None for t in (nhan or {})})  # đột biến: đủ tên, mất giá trị\n',
        "TEP_TEST", _KEM_TEP_TEST, 't54_main_chon_DUNG_vong_ban_kinh_theo_che_do'),
    'f6_main_mat_van_tay': ("ops/cong_cu_test.py",
        '        dong, loi = _ket_thuc_manh(k, n, ra, ten, None if ly_con else ket, ly_con, _van_tay())\n',
        '        dong, loi = _ket_thuc_manh(k, n, ra, ten, None if ly_con else ket, ly_con, {})  # đột biến: mất vân tay\n',
        "TEP_TEST", _KEM_TEP_TEST, 't54_main_chon_DUNG_vong_ban_kinh_theo_che_do'),
    'f6_main_bo_tien_kiem': ("ops/cong_cu_test.py",
        '        if hong or tien_kiem_bo_qua:\n',
        '        if hong:  # đột biến: tiền kiểm bỏ qua vẫn đo\n',
        "TEP_TEST", _KEM_TEP_TEST, 't54_main_chon_DUNG_vong_ban_kinh_theo_che_do'),
    'f6_main_manh_mot_tien_trinh': ("ops/cong_cu_test.py",
        '        for nhom, rc, ra_con in _phong_con(ten, (), _so_tien_trinh_ban_kinh()) if ten else ():\n',
        '        for nhom, rc, ra_con in _phong_con(ten, (), 1) if ten else ():  # đột biến: bỏ số tiến trình\n',
        "TEP_TEST", _KEM_TEP_TEST, 't54_main_chon_DUNG_vong_ban_kinh_theo_che_do'),
    'f5_main_bo_nhan': ("ops/cong_cu_test.py",
        '            ket.update(nhan or {})\n',
        '            pass  # đột biến: bỏ nhận bản ghi\n',
        "TEP_TEST", _KEM_TEP_TEST, 't54_main_chon_DUNG_vong_ban_kinh_theo_che_do'),
    'f5_main_bo_ghi': ("ops/cong_cu_test.py",
        '        dong, loi = _ket_thuc_manh(k, n, ra, ten, None if ly_con else ket, ly_con, _van_tay())\n',
        '        dong, loi = [], 0  # đột biến: bỏ gọi bộ ghi\n',
        "TEP_TEST", _KEM_TEP_TEST, 't54_main_chon_DUNG_vong_ban_kinh_theo_che_do'),
    'f5_main_bo_truyen_loi': ("ops/cong_cu_test.py",
        '        return 1 if loi else 0\n',
        '        return 0  # đột biến: nuốt lỗi mảnh\n',
        "TEP_TEST", _KEM_TEP_TEST, 't54_main_chon_DUNG_vong_ban_kinh_theo_che_do'),
    'f5_main_bo_loi_con': ("ops/cong_cu_test.py",
        '            if nhan is None:\n                ly_con = ly_con or',
        '            if False:\n                ly_con = ly_con or',
        "TEP_TEST", _KEM_TEP_TEST, 't54_main_chon_DUNG_vong_ban_kinh_theo_che_do'),
    'f5_main_nen_do_van_do': ("ops/cong_cu_test.py",
        '[M-nen]: nền KHÔNG xanh — không đo bán kính, không ghi tệp")\n            return 1\n',
        '[M-nen]: nền KHÔNG xanh — không đo bán kính, không ghi tệp")\n            pass  # đột biến: nền đỏ vẫn đo\n',
        "TEP_TEST", _KEM_TEP_TEST, 't54_main_chon_DUNG_vong_ban_kinh_theo_che_do'),
    'f2_main_du_bo_ban_kinh': ("ops/cong_cu_test.py",
        '    if che_do == "gate":\n',
        '    if che_do in ("gate", "du"):  # đột biến: Codex lượt 1 F2\n',
        "TEP_TEST", _KEM_TEP_TEST, 't54_main_chon_DUNG_vong_ban_kinh_theo_che_do'),
    'f2_main_gate_van_do': ("ops/cong_cu_test.py",
        '    if che_do == "gate":\n',
        '    if False:  # đột biến: gate vẫn đo trọn\n',
        "TEP_TEST", _KEM_TEP_TEST, 't54_main_chon_DUNG_vong_ban_kinh_theo_che_do'),
    'f2_main_manh_do_ca_bang': ("ops/cong_cu_test.py",
        '        ten = _phan_manh(k, n)\n',
        '        ten = list(DOT_BIEN)  # đột biến: mảnh đo cả bảng\n',
        "TEP_TEST", _KEM_TEP_TEST, 't54_main_chon_DUNG_vong_ban_kinh_theo_che_do'),
    'g668_gom_bo_thu_muc': ("ops/cong_cu_test.py",
        '    if muc is None:\n',
        '    if False:  # đột biến: thư mục vắng lọt\n',
        "TEP_TEST", _KEM_TEP_TEST, 't52_gom_manh_phai_DO_khi_thieu_trung_lech_va_moi_chot_co_THE_RIENG'),
    'g668_gom_bo_rong': ("ops/cong_cu_test.py",
        '    if not muc:\n        return [f"  ĐỎ  gom [G-rong]',
        '    if False:\n        return [f"  ĐỎ  gom [G-rong]',
        "TEP_TEST", _KEM_TEP_TEST, 't52_gom_manh_phai_DO_khi_thieu_trung_lech_va_moi_chot_co_THE_RIENG'),
    'g668_gom_bo_head': ("ops/cong_cu_test.py",
        '    if van_tay.get("head") is None:\n        return ["  ĐỎ  gom [G-head]',
        '    if False:\n        return ["  ĐỎ  gom [G-head]',
        "TEP_TEST", _KEM_TEP_TEST, 't52_gom_manh_phai_DO_khi_thieu_trung_lech_va_moi_chot_co_THE_RIENG'),
    'g668_gom_bo_tep_thuong': ("ops/cong_cu_test.py",
        '        if p.is_symlink() or not p.is_file():\n',
        '        if False:  # đột biến: nhận mục không phải tệp thường\n',
        "TEP_TEST", _KEM_TEP_TEST, 't52_gom_manh_phai_DO_khi_thieu_trung_lech_va_moi_chot_co_THE_RIENG'),
    'g668_gom_nhan_khoa_thua': ("ops/cong_cu_test.py",
        '            if not isinstance(dau, dict) or set(dau) != _KHOA_DAU_MANH:\n',
        '            if not isinstance(dau, dict) or not _KHOA_DAU_MANH <= set(dau):  # đột biến: nhận khoá thừa\n',
        "TEP_TEST", _KEM_TEP_TEST, 't52_gom_manh_phai_DO_khi_thieu_trung_lech_va_moi_chot_co_THE_RIENG'),
    'g668_gom_bo_kieu_int': ("ops/cong_cu_test.py",
        '            if any(type(dau[x]) is not int for x in ("phien_ban", "manh", "so_manh")):\n',
        '            if False:  # đột biến: bool lọt thành số\n',
        "TEP_TEST", _KEM_TEP_TEST, 't52_gom_manh_phai_DO_khi_thieu_trung_lech_va_moi_chot_co_THE_RIENG'),
    'g668_gom_bo_phien_ban': ("ops/cong_cu_test.py",
        '        if dau["phien_ban"] != _PHIEN_BAN_MANH:\n',
        '        if False:  # đột biến: phiên bản lạ lọt\n',
        "TEP_TEST", _KEM_TEP_TEST, 't52_gom_manh_phai_DO_khi_thieu_trung_lech_va_moi_chot_co_THE_RIENG'),
    'g668_gom_bo_sha': ("ops/cong_cu_test.py",
        '        if dau["sha256_test"] != van_tay["sha256_test"] or dau["head"] != van_tay["head"]:\n',
        '        if dau["head"] != van_tay["head"]:  # đột biến: bỏ so sha256_test\n',
        "TEP_TEST", _KEM_TEP_TEST, 't52_gom_manh_phai_DO_khi_thieu_trung_lech_va_moi_chot_co_THE_RIENG'),
    'g668_gom_bo_head_manh': ("ops/cong_cu_test.py",
        '        if dau["sha256_test"] != van_tay["sha256_test"] or dau["head"] != van_tay["head"]:\n',
        '        if dau["sha256_test"] != van_tay["sha256_test"]:  # đột biến: bỏ so head\n',
        "TEP_TEST", _KEM_TEP_TEST, 't52_gom_manh_phai_DO_khi_thieu_trung_lech_va_moi_chot_co_THE_RIENG'),
    'g668_gom_bo_dong_la': ("ops/cong_cu_test.py",
        '        if la:\n',
        '        if False:  # đột biến: dòng ngoài hợp đồng lọt\n',
        "TEP_TEST", _KEM_TEP_TEST, 't52_gom_manh_phai_DO_khi_thieu_trung_lech_va_moi_chot_co_THE_RIENG'),
    'g668_gom_bo_so_manh': ("ops/cong_cu_test.py",
        '    if len(cac_n) != 1:\n',
        '    if False:  # đột biến: số mảnh khác nhau lọt\n',
        "TEP_TEST", _KEM_TEP_TEST, 't52_gom_manh_phai_DO_khi_thieu_trung_lech_va_moi_chot_co_THE_RIENG'),
    'g668_gom_bo_n': ("ops/cong_cu_test.py",
        '    if not 2 <= n <= _TRAN_MANH:\n',
        '    if False:  # đột biến: N ngoài phạm vi lọt\n',
        "TEP_TEST", _KEM_TEP_TEST, 't52_gom_manh_phai_DO_khi_thieu_trung_lech_va_moi_chot_co_THE_RIENG'),
    'g668_gom_bo_tap': ("ops/cong_cu_test.py",
        '    if sorted(than_cac) != list(range(n)):\n',
        '    if False:  # đột biến: tập mảnh lệch lọt\n',
        "TEP_TEST", _KEM_TEP_TEST, 't52_gom_manh_phai_DO_khi_thieu_trung_lech_va_moi_chot_co_THE_RIENG'),
    'g668_gom_bo_phan_hoach': ("ops/cong_cu_test.py",
        '    if sum(map(len, phan)) != len(DOT_BIEN) or set().union(*phan) != set(DOT_BIEN):\n',
        '    if False:  # đột biến: phân hoạch chồng lấn lọt\n',
        "TEP_TEST", _KEM_TEP_TEST, 't52_gom_manh_phai_DO_khi_thieu_trung_lech_va_moi_chot_co_THE_RIENG'),
    'g668_gom_bo_dem': ("ops/cong_cu_test.py",
        '        if len(cua_k) != 1:\n',
        '        if not cua_k:  # đột biến: mảnh trùng lọt, lấy tệp đầu\n',
        "TEP_TEST", _KEM_TEP_TEST, 't52_gom_manh_phai_DO_khi_thieu_trung_lech_va_moi_chot_co_THE_RIENG'),
    'g668_gom_tin_ten_cua_manh': ("ops/cong_cu_test.py",
        '        nhan, ly_do = _nhan_ket_qua_con(phan[k], 0, than, ())\n',
        '        nhan, ly_do = _nhan_ket_qua_con([json.loads(x[6:])[1] for x in than.split("\\n") if x], 0, than, ())  # đột biến: tin tên do mảnh tự khai\n',
        "TEP_TEST", _KEM_TEP_TEST, 't52_gom_manh_phai_DO_khi_thieu_trung_lech_va_moi_chot_co_THE_RIENG'),
    'g668_phan_manh_chong': ("ops/cong_cu_test.py",
        '    return [t for i, t in enumerate(DOT_BIEN if ten is None else ten) if i % n == k]\n',
        '    return [t for i, t in enumerate(DOT_BIEN if ten is None else ten) if i % n <= k]  # đột biến\n',
        "TEP_TEST", _KEM_TEP_TEST, 't52_gom_manh_phai_DO_khi_thieu_trung_lech_va_moi_chot_co_THE_RIENG'),
    'g668_ghi_bo_xoa_cu': ("ops/cong_cu_test.py",
        '    if tep.exists() or tep.is_symlink():\n        tep.unlink()\n',
        '    if False:  # đột biến: để lại tệp mảnh cũ\n        tep.unlink()\n',
        "TEP_TEST", _KEM_TEP_TEST, 't52_gom_manh_phai_DO_khi_thieu_trung_lech_va_moi_chot_co_THE_RIENG'),
    'g668_ghi_bo_con': ("ops/cong_cu_test.py",
        '    if ket is None:\n        return [f"  ĐỎ  mảnh {k}/{n} [M-con]',
        '    if False:\n        return [f"  ĐỎ  mảnh {k}/{n} [M-con]',
        "TEP_TEST", _KEM_TEP_TEST, 't52_gom_manh_phai_DO_khi_thieu_trung_lech_va_moi_chot_co_THE_RIENG'),
    'g668_ghi_bo_head': ("ops/cong_cu_test.py",
        '    if van_tay.get("head") is None:\n        return [f"  ĐỎ  mảnh {k}/{n} [M-head]',
        '    if False:\n        return [f"  ĐỎ  mảnh {k}/{n} [M-head]',
        "TEP_TEST", _KEM_TEP_TEST, 't52_gom_manh_phai_DO_khi_thieu_trung_lech_va_moi_chot_co_THE_RIENG'),
    'g668_ghi_bo_loi': ("ops/cong_cu_test.py",
        '    if loi:\n        return dong + [f"  ĐỎ  mảnh {k}/{n} [M-loi]',
        '    if False:\n        return dong + [f"  ĐỎ  mảnh {k}/{n} [M-loi]',
        "TEP_TEST", _KEM_TEP_TEST, 't52_gom_manh_phai_DO_khi_thieu_trung_lech_va_moi_chot_co_THE_RIENG'),
    'g668_che_do_bo_ra_le': ("ops/cong_cu_test.py",
        '        if ra is not None:\n            raise ValueError(f"[C-ra-le]',
        '        if False:\n            raise ValueError(f"[C-ra-le]',
        "TEP_TEST", _KEM_TEP_TEST, 't53_che_do_doc_FAIL_CLOSED_moi_cau_hinh_la_co_THE_RIENG_va_van_tay_bam_NGUON'),
    'g668_che_do_rong_la_vang': ("ops/cong_cu_test.py",
        '        if bk != "manh":\n',
        '        if bk not in ("manh", ""):  # đột biến: rỗng coi như đúng\n',
        "TEP_TEST", _KEM_TEP_TEST, 't53_che_do_doc_FAIL_CLOSED_moi_cau_hinh_la_co_THE_RIENG_va_van_tay_bam_NGUON'),
    'g668_che_do_bo_ca_hai': ("ops/cong_cu_test.py",
        '    if bk is not None:\n        raise ValueError(f"[C-ca-hai]',
        '    if False:\n        raise ValueError(f"[C-ca-hai]',
        "TEP_TEST", _KEM_TEP_TEST, 't53_che_do_doc_FAIL_CLOSED_moi_cau_hinh_la_co_THE_RIENG_va_van_tay_bam_NGUON'),
    'g668_che_do_match_khong_full': ("ops/cong_cu_test.py",
        '    m = re.fullmatch(r"(0|[1-9][0-9]?)/([1-9][0-9]?)", mh)\n',
        '    m = re.match(r"(0|[1-9][0-9]?)/([1-9][0-9]?)", mh)  # đột biến: bỏ neo cuối\n',
        "TEP_TEST", _KEM_TEP_TEST, 't53_che_do_doc_FAIL_CLOSED_moi_cau_hinh_la_co_THE_RIENG_va_van_tay_bam_NGUON'),
    'g668_che_do_chu_so_unicode': ("ops/cong_cu_test.py",
        '    m = re.fullmatch(r"(0|[1-9][0-9]?)/([1-9][0-9]?)", mh)\n',
        '    m = re.fullmatch(r"(0|[1-9]\\d?|\\d)/([1-9][0-9]?)", mh)  # đột biến: \\d nhận chữ số Unicode\n',
        "TEP_TEST", _KEM_TEP_TEST, 't53_che_do_doc_FAIL_CLOSED_moi_cau_hinh_la_co_THE_RIENG_va_van_tay_bam_NGUON'),
    'g668_che_do_nhan_n_1': ("ops/cong_cu_test.py",
        '    if not (2 <= n <= _TRAN_MANH and k < n):\n',
        '    if not (1 <= n <= _TRAN_MANH and k < n):  # đột biến\n',
        "TEP_TEST", _KEM_TEP_TEST, 't53_che_do_doc_FAIL_CLOSED_moi_cau_hinh_la_co_THE_RIENG_va_van_tay_bam_NGUON'),
    'g668_che_do_nhan_k_bang_n': ("ops/cong_cu_test.py",
        '    if not (2 <= n <= _TRAN_MANH and k < n):\n',
        '    if not (2 <= n <= _TRAN_MANH and k <= n):  # đột biến\n',
        "TEP_TEST", _KEM_TEP_TEST, 't53_che_do_doc_FAIL_CLOSED_moi_cau_hinh_la_co_THE_RIENG_va_van_tay_bam_NGUON'),
    'g668_che_do_bo_tran_tren': ("ops/cong_cu_test.py",
        '    if not (2 <= n <= _TRAN_MANH and k < n):\n',
        '    if not (2 <= n and k < n):  # đột biến: bỏ trần trên\n',
        "TEP_TEST", _KEM_TEP_TEST, 't53_che_do_doc_FAIL_CLOSED_moi_cau_hinh_la_co_THE_RIENG_va_van_tay_bam_NGUON'),
    'g668_che_do_ra_rong_lot': ("ops/cong_cu_test.py",
        '    if not ra:\n',
        '    if ra is None:  # đột biến: tệp ra rỗng lọt\n',
        "TEP_TEST", _KEM_TEP_TEST, 't53_che_do_doc_FAIL_CLOSED_moi_cau_hinh_la_co_THE_RIENG_va_van_tay_bam_NGUON'),
}

# #668 F7/F8/F9 (Codex lượt 4): đột biến dây nối `main`, CLI `--gop` và NGUỒN vân tay, sinh từ BẢNG (cùng khuôn 6 trường
# như mọi mục `DOT_BIEN`, chỉ gọn dòng). Cố ý KHÔNG có đột biến cho `loi_db += loi_nen` và vế `hong` của mã thoát cuối:
# `hong` khác rỗng ⇒ `_bao_cao_nen_do` trả 1 ⇒ `loi_db ≥ 1`, nên gỡ riêng một trong hai là đột biến TƯƠNG ĐƯƠNG (chúng
# rào lẫn nhau) — một ca "giết" được nó sẽ phải khẳng định điều sai.
_CA_668 = {"t52_": 't52_gom_manh_phai_DO_khi_thieu_trung_lech_va_moi_chot_co_THE_RIENG',
           "t53_": 't53_che_do_doc_FAIL_CLOSED_moi_cau_hinh_la_co_THE_RIENG_va_van_tay_bam_NGUON',
           "t54_": 't54_main_chon_DUNG_vong_ban_kinh_theo_che_do'}
# F44: neo TRỌN DÒNG (kèm xuống dòng) của nhánh nền đỏ trong `main` — không trùng chính bảng này (thay ở lần xuất hiện ĐẦU).
_NEN_M = '            _ket_thuc_manh(k, n, ra, ten, None, "nền đỏ hoặc tiền kiểm bị bỏ qua — không đo", _van_tay())\n'
_NEN_IN = '            print(f"  ĐỎ  mảnh {k}/{n} [M-nen]: nền KHÔNG xanh — không đo bán kính, không ghi tệp")\n'
_D45 = 'if not _CO_SYMLINK:\n'   # F45: neo ĐỘC LẬP với dòng quan sát — gỡ chốt quan sát thì neo vẫn còn
for _ten, _ca, _tim, _thay in (
    ('f7_cau_hinh_nuot', 't54_',
     '        print(f"  ĐỎ  cấu hình chế độ: {ex}")\n        return 2\n',
     '        print(f"  ĐỎ  cấu hình chế độ: {ex}")\n        che_do, tham_so = "du", None\n'),
    ('f7_tk_chi_batch', 't54_',
     '                                    _chay_tien_kiem(python_alias_behavior_test)) if x]\n',
     '                                    None) if x]\n'),
    ('f7_tk_chi_alias', 't54_',
     '    tien_kiem_bo_qua = [x for x in (_chay_tien_kiem(batch_behavior_test),\n',
     '    tien_kiem_bo_qua = [x for x in (None,\n'),
    ('f7_ca_do_nuot', 't54_',
     '        except AssertionError as ex:\n            hong.append((fn.__name__, str(ex)))\n',
     '        except AssertionError as ex:\n            qua += 1\n'),
    ('f7_ca_loi_khac_nuot', 't54_',
     '            hong.append((fn.__name__, f"{type(ex).__name__}: {ex}"))\n',
     '            qua += 1\n'),
    ('f7_bo_qua_thanh_hong', 't54_',
     '            bo_qua.append((fn.__name__, str(ex)))\n',
     '            hong.append((fn.__name__, str(ex)))\n'),
    ('f7_con_rc_bo', 't54_',
     '            nhan, ly = _nhan_ket_qua_con(nhom, rc, ra_con, ())\n',
     '            nhan, ly = _nhan_ket_qua_con(nhom, 0, ra_con, ())\n'),
    ('f7_ghi_ket_du_loi', 't54_',
     '        dong, loi = _ket_thuc_manh(k, n, ra, ten, None if ly_con else ket, ly_con, _van_tay())\n',
     '        dong, loi = _ket_thuc_manh(k, n, ra, ten, ket, ly_con, _van_tay())\n'),
    ('f7_bo_cong', 't54_',
     '    loi_cong, dong_cong = _cong_tren_cay_that(GOC)\n',
     '    loi_cong, dong_cong = 0, []\n'),
    ('f7_cong_goc_sai', 't54_',
     '    loi_cong, dong_cong = _cong_tren_cay_that(GOC)\n',
     '    loi_cong, dong_cong = _cong_tren_cay_that(HERE)\n'),
    ('f7_bo_phan_hang', 't54_',
     '    loi_db = _tu_kiem_phan_hang()\n',
     '    loi_db = 0\n'),
    ('f7_bo_gian_giao', 't54_',
     '    loi_db += _tu_kiem_gian_giao()\n',
     '    loi_db += 0\n'),
    ('f7_nen_rong', 't54_',
     '    dong_nen, loi_nen = _bao_cao_nen_do(do_o_nen)\n',
     '    dong_nen, loi_nen = _bao_cao_nen_do([])\n'),
    ('f7_bo_song_song', 't54_',
     '    loi_db += _tu_kiem_song_song(do_o_nen)\n',
     '    loi_db += 0\n'),
    ('f7_song_song_nen_rong', 't54_',
     '    loi_db += _tu_kiem_song_song(do_o_nen)\n',
     '    loi_db += _tu_kiem_song_song([])\n'),
    ('f7_du_nen_rong', 't54_',
     '        for cac_dong, loi in _ban_kinh_moi_dot_bien(list(DOT_BIEN), do_o_nen, so_tien_trinh):\n',
     '        for cac_dong, loi in _ban_kinh_moi_dot_bien(list(DOT_BIEN), [], so_tien_trinh):\n'),
    ('f7_du_nuot_loi', 't54_',
     '            loi_db += loi\n',
     '            loi_db += 0\n'),
    ('f7_du_mot_tien_trinh', 't54_',
     '    so_tien_trinh = _so_tien_trinh_ban_kinh()\n',
     '    so_tien_trinh = 1\n'),
    ('f7_ket_bo_tien_kiem', 't54_',
     '    return 1 if (hong or loi_db or tien_kiem_bo_qua or loi_cong) else 0\n',
     '    return 1 if (hong or loi_db or loi_cong) else 0\n'),
    ('f7_ket_bo_cong', 't54_',
     '    return 1 if (hong or loi_db or tien_kiem_bo_qua or loi_cong) else 0\n',
     '    return 1 if (hong or loi_db or tien_kiem_bo_qua) else 0\n'),
    ('f7_ket_bo_loi_db', 't54_',
     '    return 1 if (hong or loi_db or tien_kiem_bo_qua or loi_cong) else 0\n',
     '    return 1 if (hong or tien_kiem_bo_qua or loi_cong) else 0\n'),
    ('f8_gop_nuot_ma', 't52_',
     '        print(d)\n    return 1 if loi else 0\n',
     '        print(d)\n    return 0\n'),
    ('f8_gop_bo_goi', 't52_',
     '    dong, loi = _gom_manh(sys.argv[i + 1], _van_tay())\n',
     '    dong, loi = ["GOM MẢNH 3/3"], 0\n'),
    ('f8_gop_van_tay_hang', 't52_',
     '    dong, loi = _gom_manh(sys.argv[i + 1], _van_tay())\n',
     '    dong, loi = _gom_manh(sys.argv[i + 1], {"sha256_test": "a" * 64, "head": "b" * 40})\n'),
    ('f8_gop_bo_doi_so', 't52_',
     '    if len(sys.argv) != i + 2:\n',
     '    if False:\n'),
    ('f9_sha_hang', 't53_',
     '    return {"sha256_test": hashlib.sha256(Path(TEP_TEST).read_bytes()).hexdigest(),\n',
     '    return {"sha256_test": "0" * 64,\n'),
    ('f9_head_hang', 't53_',
     '            "head": head if re.fullmatch(r"[0-9a-f]{40}|[0-9a-f]{64}", head) else None}\n',
     '            "head": "b" * 40}\n'),
    ('f12_ca_lap', 't54_',
     '    for fn in CA:\n        try:\n            fn()\n',
     '    for fn in CA[:3] + CA[2:3] + CA[4:]:\n        try:\n            fn()\n'),
    ('f12_bk_gan_de', 't54_',
     '            loi_db += loi\n',
     '            loi_db = loi\n'),
    ('f12_bk_chi_dau', 't54_',
     '        for cac_dong, loi in _ban_kinh_moi_dot_bien(list(DOT_BIEN), do_o_nen, so_tien_trinh):\n',
     '        for cac_dong, loi in _ban_kinh_moi_dot_bien(list(DOT_BIEN), do_o_nen, so_tien_trinh)[:1]:\n'),
    ('f12_dem_qua', 't54_',
     '            qua += 1\n',
     '            qua += 2\n'),
    ('f12_dem_bo_qua', 't54_',
     '          f"bỏ qua={len(bo_qua)}, tiền kiểm bỏ qua={len(tien_kiem_bo_qua)}")\n',
     '          f"bỏ qua=0, tiền kiểm bỏ qua={len(tien_kiem_bo_qua)}")\n'),
    ('f12_bo_in_bk', 't54_',
     '            for dong in cac_dong:\n                print(dong)\n',
     '            for dong in cac_dong:\n                pass\n'),
    ('f12_bo_in_ghi', 't54_',
     '        for d in dong:\n            print(d)\n        return 1 if loi else 0\n',
     '        for d in dong:\n            pass\n        return 1 if loi else 0\n'),
    ('f13_dispatcher_nuot', 't52_',
     '        sys.exit(_main_gop())\n',
     '        sys.exit(0)\n'),
    ('f15_ghi_bang_mot', 't54_',
     '        return 1 if loi else 0\n',
     '        return 1 if loi == 1 else 0\n'),
    ('f15_ket_db_bang_mot', 't54_',
     '    return 1 if (hong or loi_db or tien_kiem_bo_qua or loi_cong) else 0\n',
     '    return 1 if (hong or loi_db == 1 or tien_kiem_bo_qua or loi_cong) else 0\n'),
    ('f15_nen_chi_dau', 't54_',
     '    do_o_nen = sorted(t for t, _ in hong)\n',
     '    do_o_nen = sorted(t for t, _ in hong)[:1]\n'),
    ('f15_tk_chi_dau', 't54_',
     '                                    _chay_tien_kiem(python_alias_behavior_test)) if x]\n',
     '                                    _chay_tien_kiem(python_alias_behavior_test)) if x][:1]\n'),
    ('f15_ly_cuoi', 't54_',
     '                ly_con = ly_con or f"{ly}; rc={rc}, đuôi đầu ra: {ra_con[-300:]!r}"\n',
     '                ly_con = f"{ly}; rc={rc}, đuôi đầu ra: {ra_con[-300:]!r}"\n'),
    ('f15_so_lieu_loi_0', 't54_',
     '          + (" (giao mảnh)" if che_do == "gate" else "") + f" · lỗi đột biến={loi_db}"\n',
     '          + (" (giao mảnh)" if che_do == "gate" else "") + f" · lỗi đột biến={0}"\n'),
    ('f15_so_lieu_cong_dat', 't54_',
     'cổng cây thật={\'ĐẠT\' if not loi_cong else \'HỎNG\'}")\n',
     'cổng cây thật={\'ĐẠT\'}")\n'),
    ('f15_bo_in_do', 't54_',
     '        print(f"  ĐỎ  {ten}: {ly}")\n',
     '        str(f"  ĐỎ  {ten}: {ly}")\n'),
    ('f15_bo_in_tk', 't54_',
     '        print(f"  BỎ QUA (TIỀN KIỂM) {ten}: {ly}")\n',
     '        str(f"  BỎ QUA (TIỀN KIỂM) {ten}: {ly}")\n'),
    ('f15_bo_in_bq', 't54_',
     '        print(f"  BỎ QUA {ten}: {ly}")\n',
     '        str(f"  BỎ QUA {ten}: {ly}")\n'),
    ('f15_bo_thong_bao_giao', 't54_',
     '        print(f"\\nBÁN KÍNH ĐỘT BIẾN ({len(DOT_BIEN)} đột biến): GIAO cho job `gate-cong-cu` (mảnh) + "\n',
     '        str(f"\\nBÁN KÍNH ĐỘT BIẾN ({len(DOT_BIEN)} đột biến): GIAO cho job `gate-cong-cu` (mảnh) + "\n'),
    ('f16_gom_bo_ket_luan', 't52_',
     '    for ten in DOT_BIEN:\n        d, l = _ket_luan_ban_ghi(ket[ten], ())\n        dong += d\n        loi += l\n',
     '    for ten in DOT_BIEN:\n        d, l = [], 0\n        dong += d\n        loi += l\n'),
    ('f16_gom_bo_cong_loi', 't52_',
     '    for ten in DOT_BIEN:\n        d, l = _ket_luan_ban_ghi(ket[ten], ())\n        dong += d\n        loi += l\n',
     '    for ten in DOT_BIEN:\n        d, l = _ket_luan_ban_ghi(ket[ten], ())\n        dong += d\n        loi += 0\n'),
    ('f16_gom_gan_de', 't52_',
     '    for ten in DOT_BIEN:\n        d, l = _ket_luan_ban_ghi(ket[ten], ())\n        dong += d\n        loi += l\n',
     '    for ten in DOT_BIEN:\n        d, l = _ket_luan_ban_ghi(ket[ten], ())\n        dong += d\n        loi = l\n'),
    ('f16_gom_chi_dau', 't52_',
     '    for ten in DOT_BIEN:\n        d, l = _ket_luan_ban_ghi(ket[ten], ())\n        dong += d\n        loi += l\n',
     '    for ten in list(DOT_BIEN)[:1]:\n        d, l = _ket_luan_ban_ghi(ket[ten], ())\n        dong += d\n        loi += l\n'),
    ('f16_gom_bo_bang', 't52_',
     '    for ten in DOT_BIEN:\n        d, l = _ket_luan_ban_ghi(ket[ten], ())\n        dong += d\n        loi += l\n',
     '    for ten in DOT_BIEN:\n        d, l = _ket_luan_ban_ghi(ket[ten], ())\n        loi += l\n'),
    ('f17_cli_bang_mot', 't52_',
     '    for d in dong:\n        print(d)\n    return 1 if loi else 0\n',
     '    for d in dong:\n        print(d)\n    return 1 if loi == 1 else 0\n'),
    ('f17_cli_in_dau', 't52_',
     '    for d in dong:\n        print(d)\n    return 1 if loi else 0\n',
     '    for d in dong[:1]:\n        print(d)\n    return 1 if loi else 0\n'),
    ('f18_ghi_lon_hon_mot', 't54_',
     '        return 1 if loi else 0\n',
     '        return 1 if loi > 1 else 0\n'),
    ('f18_ket_db_lon_hon_mot', 't54_',
     '    return 1 if (hong or loi_db or tien_kiem_bo_qua or loi_cong) else 0\n',
     '    return 1 if (hong or loi_db > 1 or tien_kiem_bo_qua or loi_cong) else 0\n'),
    ('f18_manh_n_co_dinh', 't54_',
     '        k, n, ra = tham_so\n',
     '        k, n, ra = tham_so[0], 8, tham_so[2]\n'),
    ('f18_bk_dong_dau', 't54_',
     '            for dong in cac_dong:\n                print(dong)\n',
     '            for dong in cac_dong[:1]:\n                print(dong)\n'),
    ('f18_ghi_dong_dau', 't54_',
     '        for d in dong:\n            print(d)\n        return 1 if loi else 0\n',
     '        for d in dong[:1]:\n            print(d)\n        return 1 if loi else 0\n'),
    ('f18_bo_in_cong', 't54_',
     '    for d in dong_cong:\n        print(d)\n',
     '    for d in dong_cong[:0]:\n        print(d)\n'),
    ('f18_bo_in_nen', 't54_',
     '    for d in dong_nen:\n        print(d)\n',
     '    for d in dong_nen[:0]:\n        print(d)\n'),
    ('f19_gom_dao', 't52_',
     '    for ten in DOT_BIEN:\n        d, l = _ket_luan_ban_ghi(ket[ten], ())\n        dong += d\n        loi += l\n',
     '    for ten in reversed(DOT_BIEN):\n        d, l = _ket_luan_ban_ghi(ket[ten], ())\n        dong += d\n        loi += l\n'),
    ('f19_gom_lap_mot_ten', 't52_',
     '    for ten in DOT_BIEN:\n        d, l = _ket_luan_ban_ghi(ket[ten], ())\n        dong += d\n        loi += l\n',
     '    for ten in DOT_BIEN:\n        d, l = _ket_luan_ban_ghi(ket[next(iter(ket))], ())\n        dong += d\n        loi += l\n'),
    ('f19_gom_bo_chi_tiet', 't52_',
     '    for ten in DOT_BIEN:\n        d, l = _ket_luan_ban_ghi(ket[ten], ())\n        dong += d\n        loi += l\n',
     '    for ten in DOT_BIEN:\n        d, l = _ket_luan_ban_ghi(ket[ten], ())\n        dong += d[:1]\n        loi += l\n'),
    ('f20_cli_dao_bang', 't52_',
     '    for d in dong:\n        print(d)\n    return 1 if loi else 0\n',
     '    for d in reversed(dong):\n        print(d)\n    return 1 if loi else 0\n'),
    ('f21_ghi_chi_loai_loi', 't52_',
     '    for ten in cac_ten:\n        bg = (ket or {}).get(ten)\n        d, l = _ket_luan_ban_ghi(bg, ()) if bg else ([f"  ĐỎ  {ten}: thiếu bản ghi"], 1)\n',
     '    for ten in cac_ten:\n        bg = (ket or {}).get(ten)\n        d, l = (_ket_luan_ban_ghi(bg, ()) if bg[0] == "loi" else ([], 0)) if bg else ([f"  ĐỎ  {ten}: thiếu bản ghi"], 1)\n'),
    ('f21_ghi_chi_ban_ghi_dau', 't52_',
     '    for ten in cac_ten:\n        bg = (ket or {}).get(ten)\n        d, l = _ket_luan_ban_ghi(bg, ()) if bg else ([f"  ĐỎ  {ten}: thiếu bản ghi"], 1)\n',
     '    for ten in cac_ten[:1]:\n        bg = (ket or {}).get(ten)\n        d, l = _ket_luan_ban_ghi(bg, ()) if bg else ([f"  ĐỎ  {ten}: thiếu bản ghi"], 1)\n'),
    ('f23_bq_chi_in_dau', 't54_',
     '    for ten, ly in bo_qua:\n        print(f"  BỎ QUA {ten}: {ly}")\n',
     '    for ten, ly in bo_qua[:1]:\n        print(f"  BỎ QUA {ten}: {ly}")\n'),
    ('f23_bq_dem_bool', 't54_',
     '    print(f"\\ncong_cu_test: {qua}/{len(CA) - len(bo_qua)} đạt; tổng={len(CA)}, "\n',
     '    print(f"\\ncong_cu_test: {qua}/{len(CA) - bool(bo_qua)} đạt; tổng={len(CA)}, "\n'),
    ('f23_ly_bo_duoi', 't54_',
     '                ly_con = ly_con or f"{ly}; rc={rc}, đuôi đầu ra: {ra_con[-300:]!r}"\n',
     '                ly_con = ly_con or f"; rc={rc}"\n'),
    ('f24_kieu_phien_ban', 't52_',
     '            if any(type(dau[x]) is not int for x in ("phien_ban", "manh", "so_manh")):\n',
     '            if any(type(dau[x]) is not int for x in ("manh", "so_manh")):\n'),
    ('f24_kieu_so_manh', 't52_',
     '            if any(type(dau[x]) is not int for x in ("phien_ban", "manh", "so_manh")):\n',
     '            if any(type(dau[x]) is not int for x in ("phien_ban", "manh")):\n'),
    ('f25_cua_moi_vi_tri', 't52_',
     '    cua = sys.argv[1] if len(sys.argv) > 1 else None\n',
     '    cua = next((c for c in reversed(sys.argv[1:]) if c in _CUA or c == "--gop"), None)\n'),
    ('f25_bo_chot_doi_so_la', 't52_',
     '    if cua is not None:\n        print(f"  ĐỎ  đối số lạ',
     '    if False:\n        print(f"  ĐỎ  đối số lạ'),
    ('f26_bq_ly_ca_dau', 't54_',
     '        print(f"  BỎ QUA {ten}: {ly}")\n',
     '        print(f"  BỎ QUA {ten}: {bo_qua[0][1]}")\n'),
    ('f26_do_ly_ca_dau', 't54_',
     '        print(f"  ĐỎ  {ten}: {ly}")\n',
     '        print(f"  ĐỎ  {ten}: {hong[0][1]}")\n'),
    ('f26_tk_ly_dau', 't54_',
     '        print(f"  BỎ QUA (TIỀN KIỂM) {ten}: {ly}")\n',
     '        print(f"  BỎ QUA (TIỀN KIỂM) {ten}: {tien_kiem_bo_qua[0][1]}")\n'),
    ('f26_con_sau_rc0', 't54_',
     '            nhan, ly = _nhan_ket_qua_con(nhom, rc, ra_con, ())\n',
     '            nhan, ly = _nhan_ket_qua_con(nhom, rc if not ket else 0, ra_con, ())\n'),    # F26/F27 (Codex lượt 10): cửa CLI mặc định + miền tham số của `main` (k=0, đường ra, worker, lỗi tự kiểm ở `du`).
    ('f27_entry_drop', 't54_', '    sys.exit(main())\n', '    sys.exit(0)\n'),
    ('f27_entry_rc', 't54_', '    sys.exit(main())\n', '    main()\n    sys.exit(0)\n'),
    ('f27_shard_zero', 't54_', '        ten = _phan_manh(k, n)\n', '        ten = _phan_manh(k or 1, n)\n'),
    ('f27_fixed_path', 't54_', '        dong, loi = _ket_thuc_manh(k, n, ra, ten, None if ly_con else ket, ly_con, _van_tay())\n',
     '        dong, loi = _ket_thuc_manh(k, n, "x", ten, None if ly_con else ket, ly_con, _van_tay())\n'),
    ('f27_fixed_workers_manh', 't54_', '        for nhom, rc, ra_con in _phong_con(ten, (), _so_tien_trinh_ban_kinh()) if ten else ():\n',
     '        for nhom, rc, ra_con in _phong_con(ten, (), 3) if ten else ():\n'),
    ('f27_fixed_workers_du', 't54_', '    so_tien_trinh = _so_tien_trinh_ban_kinh()\n', '    so_tien_trinh = 3\n'),
    ('f28_can_cau_hinh', 't54_', '    sys.exit(main())\n',
     '    sys.exit(main() if os.environ.get(_BIEN_BAN_KINH) or os.environ.get(_BIEN_MANH) else 0)\n'),
    ('f28_gate_di_tat', 't54_', '    sys.exit(main())\n',
     '    sys.exit(0 if os.environ.get(_BIEN_BAN_KINH) == "manh" else main())\n'),
    ('f28_du_nuot_ma', 't54_', '    sys.exit(main())\n',
     '    sys.exit(main() if os.environ.get(_BIEN_BAN_KINH) or os.environ.get(_BIEN_MANH) else (main() and 0))\n'),
    ('f28_nen_ma', 't54_', '    sys.exit(main())\n', '    sys.exit(1 if main() else 0)\n'),
    # F29/F30 (Codex lượt 12): rỗng ≠ vắng ở từng chốt `_doc_che_do`; hai chốt nguồn HEAD của `_van_tay`.
    ('f29_bk_truthy', 't53_', '    if bk is not None:\n', '    if bk:\n'),
    ('f29_ra_truthy', 't53_', '        if ra is not None:\n', '        if ra:\n'),
    ('f29_mh_truthy', 't53_', '    if mh is None:\n', '    if not mh:\n'),
    ('f30_bo_rc', 't53_', '        head = p.stdout.strip() if p.returncode == 0 else ""\n', '        head = p.stdout.strip()\n'),
    ('f30_bo_dinh_dang', 't53_', '            "head": head if re.fullmatch(r"[0-9a-f]{40}|[0-9a-f]{64}", head) else None}\n',
     '            "head": head or None}\n'),
    ('f31_trim_gate', 't53_', '        if bk != "manh":\n', '        if bk.strip() != "manh":\n'),
    ('f32_do_dai', 't53_', '            "head": head if re.fullmatch(r"[0-9a-f]{40}|[0-9a-f]{64}", head) else None}\n', '            "head": head if re.fullmatch(r"[0-9a-f]{40,64}", head) else None}\n'),
    ('f32_bang_chu', 't53_', '            "head": head if re.fullmatch(r"[0-9a-f]{40}|[0-9a-f]{64}", head) else None}\n', '            "head": head if re.fullmatch(r"[0-9a-z]{40}|[0-9a-z]{64}", head) else None}\n'),
    ('f32_hoa', 't53_', '            "head": head if re.fullmatch(r"[0-9a-f]{40}|[0-9a-f]{64}", head) else None}\n', '            "head": head if re.fullmatch(r"[0-9a-fA-F]{40}|[0-9a-fA-F]{64}", head) else None}\n'),
    # F33/F34/F35 (Codex lượt 14, theo LỚP): miền chế độ, nguồn HEAD hai nhánh + ngoại lệ + bytes, phân hoạch/gom/bộ ghi.
    ('f33_k_width', 't53_',
     '    m = re.fullmatch(r"(0|[1-9][0-9]?)/([1-9][0-9]?)", mh)\n',
     '    m = re.fullmatch(r"(0|[1-9][0-9]*)/([1-9][0-9]?)", mh)\n'),
    ('f33_n_width', 't53_',
     '    m = re.fullmatch(r"(0|[1-9][0-9]?)/([1-9][0-9]?)", mh)\n',
     '    m = re.fullmatch(r"(0|[1-9][0-9]?)/([1-9][0-9]*)", mh)\n'),
    ('f33_n_zero', 't53_',
     '    m = re.fullmatch(r"(0|[1-9][0-9]?)/([1-9][0-9]?)", mh)\n',
     '    m = re.fullmatch(r"(0|[1-9][0-9]?)/([0-9][0-9]?)", mh)\n'),
    ('f33_n_unicode_first', 't53_',
     '    m = re.fullmatch(r"(0|[1-9][0-9]?)/([1-9][0-9]?)", mh)\n',
     '    m = re.fullmatch(r"(0|[1-9][0-9]?)/(\\d[0-9]?)", mh)\n'),
    ('f33_n_unicode_tail', 't53_',
     '    m = re.fullmatch(r"(0|[1-9][0-9]?)/([1-9][0-9]?)", mh)\n',
     '    m = re.fullmatch(r"(0|[1-9][0-9]?)/([1-9]\\d?)", mh)\n'),
    ('f33_k_unicode_tail', 't53_',
     '    m = re.fullmatch(r"(0|[1-9][0-9]?)/([1-9][0-9]?)", mh)\n',
     '    m = re.fullmatch(r"(0|[1-9]\\d?)/([1-9][0-9]?)", mh)\n'),
    ('f33_k_sign', 't53_',
     '    m = re.fullmatch(r"(0|[1-9][0-9]?)/([1-9][0-9]?)", mh)\n',
     '    m = re.fullmatch(r"([+-]?(?:0|[1-9][0-9]?))/([1-9][0-9]?)", mh)\n'),
    ('f33_n_sign', 't53_',
     '    m = re.fullmatch(r"(0|[1-9][0-9]?)/([1-9][0-9]?)", mh)\n',
     '    m = re.fullmatch(r"(0|[1-9][0-9]?)/([+-]?[1-9][0-9]?)", mh)\n'),
    ('f33_separator', 't53_',
     '    m = re.fullmatch(r"(0|[1-9][0-9]?)/([1-9][0-9]?)", mh)\n',
     '    m = re.fullmatch(r"(0|[1-9][0-9]?)[/:]([1-9][0-9]?)", mh)\n'),
    ('f33_output_trim', 't53_',
     '    return "manh", (k, n, ra)\n',
     '    return "manh", (k, n, ra.strip())\n'),
    ('f33_output_space', 't53_',
     '    if not ra:\n',
     '    if not ra or not ra.strip():\n'),
    ('f34_head_64_alpha', 't53_',
     '            "head": head if re.fullmatch(r"[0-9a-f]{40}|[0-9a-f]{64}", head) else None}\n',
     '            "head": head if re.fullmatch(r"[0-9a-f]{40}|[0-9a-z]{64}", head) else None}\n'),
    ('f34_head_64_case', 't53_',
     '            "head": head if re.fullmatch(r"[0-9a-f]{40}|[0-9a-f]{64}", head) else None}\n',
     '            "head": head if re.fullmatch(r"[0-9a-f]{40}|[0-9a-fA-F]{64}", head) else None}\n'),
    ('f34_head_64_ascii_extra', 't53_',
     '            "head": head if re.fullmatch(r"[0-9a-f]{40}|[0-9a-f]{64}", head) else None}\n',
     '            "head": head if re.fullmatch(r"[0-9a-f]{40}|[0-9a-f_]{64}", head) else None}\n'),
    ('f34_head_40_ascii_extra', 't53_',
     '            "head": head if re.fullmatch(r"[0-9a-f]{40}|[0-9a-f]{64}", head) else None}\n',
     '            "head": head if re.fullmatch(r"[0-9a-f_]{40}|[0-9a-f]{64}", head) else None}\n'),
    ('f34_head_64_narrow', 't53_',
     '            "head": head if re.fullmatch(r"[0-9a-f]{40}|[0-9a-f]{64}", head) else None}\n',
     '            "head": head if re.fullmatch(r"[0-9a-f]{40}|[0-9a-e]{64}", head) else None}\n'),
    ('f34_head_64_decimal_only', 't53_',
     '            "head": head if re.fullmatch(r"[0-9a-f]{40}|[0-9a-f]{64}", head) else None}\n',
     '            "head": head if re.fullmatch(r"[0-9a-f]{40}|[a-f]{64}", head) else None}\n'),
    ('f34_head_strip_left', 't53_',
     '        head = p.stdout.strip() if p.returncode == 0 else ""\n',
     '        head = p.stdout.rstrip() if p.returncode == 0 else ""\n'),
    ('f34_head_rc_two', 't53_',
     '        head = p.stdout.strip() if p.returncode == 0 else ""\n',
     '        head = p.stdout.strip() if p.returncode != 1 else ""\n'),
    ('f34_head_no_oserror', 't53_',
     '    except (OSError, subprocess.SubprocessError):\n',
     '    except subprocess.SubprocessError:\n'),
    ('f34_head_no_subprocesserror', 't53_',
     '    except (OSError, subprocess.SubprocessError):\n',
     '    except OSError:\n'),
    ('f34_head_timeout', 't53_',
     '        p = subprocess.run(["git", "-C", str(GOC), "rev-parse", "HEAD"], capture_output=True, text=True, timeout=60)\n',
     '        p = subprocess.run(["git", "-C", str(GOC), "rev-parse", "HEAD"], capture_output=True, text=True, timeout=None)\n'),
    ('f34_source_text_bytes', 't53_',
     '    return {"sha256_test": hashlib.sha256(Path(TEP_TEST).read_bytes()).hexdigest(),\n',
     '    return {"sha256_test": hashlib.sha256(Path(TEP_TEST).read_text().encode()).hexdigest(),\n'),
    ('f35_gom_n_min', 't52_',
     '    if not 2 <= n <= _TRAN_MANH:\n',
     '    if not 3 <= n <= _TRAN_MANH:\n'),
    ('f35_gom_n_max_low', 't52_',
     '    if not 2 <= n <= _TRAN_MANH:\n',
     '    if not 2 <= n < _TRAN_MANH:\n'),
    ('f35_gom_n_max_high', 't52_',
     '    if not 2 <= n <= _TRAN_MANH:\n',
     '    if not 2 <= n <= _TRAN_MANH + 1:\n'),
    ('f35_gom_n_no_upper', 't52_',
     '    if not 2 <= n <= _TRAN_MANH:\n',
     '    if not 2 <= n:\n'),
    ('f35_gom_drop_head_prefix', 't52_',
     '            if not dong0.startswith("MANH "):\n',
     '            if False:\n'),
    ('f35_gom_manh_float', 't52_',
     '            if any(type(dau[x]) is not int for x in ("phien_ban", "manh", "so_manh")):\n',
     '            if any(type(dau[x]) is not int and not (x == "manh" and type(dau[x]) is float) for x in ("phien_ban", "manh", "so_manh")):\n'),
    ('f35_gom_drop_oserror', 't52_',
     '        except (OSError, UnicodeDecodeError, ValueError) as ex:\n',
     '        except (UnicodeDecodeError, ValueError) as ex:\n'),
    ('f35_writer_parents', 't52_',
     '    tep.parent.mkdir(parents=True, exist_ok=True)\n',
     '    tep.parent.mkdir(parents=False, exist_ok=True)\n'),
    ('f35_writer_path_trim', 't52_',
     '    tep = Path(ra)\n',
     '    tep = Path(str(ra).strip())\n'),
    ('f35_phan_hoach_xoay', 't52_',
     '    return [t for i, t in enumerate(DOT_BIEN if ten is None else ten) if i % n == k]\n',
     '    return [t for i, t in enumerate(DOT_BIEN if ten is None else ten) if (i + 1) % n == k]\n'),
    ('f35_phan_hoach_dao_nguon', 't52_',
     '    return [t for i, t in enumerate(DOT_BIEN if ten is None else ten) if i % n == k]\n',
     '    return [t for i, t in enumerate(list(DOT_BIEN if ten is None else ten)[::-1]) if i % n == k]\n'),
    # F37 (Codex lượt 15): đăng ký theo NĂNG LỰC — điều kiện, và từng phép đăng ký, phải bị chốt siêu dữ liệu của t52 bắt.
    ('f37_dk_dao', 't52_', 'if _CO_SYMLINK:   # F24: chỉ đo được ở nền có symlink (xem `_do_co_symlink`)\n',
     'if not _CO_SYMLINK:   # đột biến\n'),
    # F42 (Codex lượt 19): `main` phải truyền NGUYÊN miền giá trị k/N/đường ra/worker (lưới `_luoi_noi_main` của t54).
    ('f42_k_mod_8', 't54_', '        k, n, ra = tham_so\n', '        k, n, ra = tham_so; k %= 8\n'),
    ('f42_n_luy_thua_2', 't54_', '        k, n, ra = tham_so\n', '        k, n, ra = tham_so; n = 1 << (n.bit_length() - 1)\n'),
    ('f42_ra_strip', 't54_', '        k, n, ra = tham_so\n', '        k, n, ra = tham_so; ra = ra.strip()\n'),
    ('f42_ra_lower', 't54_', '        k, n, ra = tham_so\n', '        k, n, ra = tham_so; ra = ra.lower()\n'),
    ('f42_worker_manh_tran_3', 't54_', '        for nhom, rc, ra_con in _phong_con(ten, (), _so_tien_trinh_ban_kinh()) if ten else ():\n', '        for nhom, rc, ra_con in _phong_con(ten, (), min(3, _so_tien_trinh_ban_kinh())) if ten else ():\n'),
    ('f42_worker_du_tran_3', 't54_', '    so_tien_trinh = _so_tien_trinh_ban_kinh()\n', '    so_tien_trinh = min(3, _so_tien_trinh_ban_kinh())\n'),
    # F44 (review lượt 20): nhánh NỀN ĐỎ `[M-nen]` của `main` cũng phải nhận NGUYÊN k/N/đường ra (ô `noi-nen-*` của t54).
    ('f44_nen_k_mod_8', 't54_', _NEN_M, _NEN_M.replace('(k, n, ra, ten,', '(k % 8, n, ra, ten,')),
    ('f44_nen_n_luy_thua_2', 't54_', _NEN_M, _NEN_M.replace('(k, n, ra,', '(k, 1 << (n.bit_length() - 1), ra,')),
    ('f44_nen_ra_strip', 't54_', _NEN_M, _NEN_M.replace('n, ra, ten', 'n, ra.strip(), ten')),
    ('f44_nen_ra_lower', 't54_', _NEN_M, _NEN_M.replace('n, ra, ten', 'n, ra.lower(), ten')),
    ('f44_nen_ten_n8', 't54_', _NEN_M, _NEN_M.replace('ra, ten, None', 'ra, _phan_manh(k, 8), None')),
    ('f44_nen_in_k_mod_8', 't54_', _NEN_IN, _NEN_IN.replace('mảnh {k}/{n}', 'mảnh {k % 8}/{n}')),
    ('f44_nen_chi_tien_kiem', 't54_', '        if hong or tien_kiem_bo_qua:\n            _ket_thuc_manh(', '        if tien_kiem_bo_qua:\n            _ket_thuc_manh('),
    # F45 (review lượt 20): bộ quan sát registry năng lực phải thấy THÊM tên ngoài oracle, XOÁ và GHI ĐÈ tên có sẵn
    # trong cửa sổ hai ảnh — vô điều kiện, cùng một phép trên cả hai nền (không thêm tên có điều kiện).
    ('f45_them_ten_la', 't52_', _D45, 'DOT_BIEN["f45_ten_la"] = DOT_BIEN["f45_xoa_ten"]\n' + _D45),
    ('f45_xoa_ten', 't52_', _D45, 'DOT_BIEN.pop("f45_them_ten_la")\n' + _D45),
    ('f45_ghi_de_ten', 't52_', _D45, 'DOT_BIEN["f45_them_ten_la"] = DOT_BIEN["f45_xoa_ten"]\n' + _D45),
    ('f27_full_seed', 't54_', '    else:\n        print(f"\\nBÁN KÍNH ĐỘT BIẾN ({len(DOT_BIEN)} đột biến, mỗi ca đúng một"',
     '    else:\n        loi_db = loi_nen\n        print(f"\\nBÁN KÍNH ĐỘT BIẾN ({len(DOT_BIEN)} đột biến, mỗi ca đúng một"'),
    # #698: 54 CANH thường trực (16 r1 · 27 r2 · 11 r3) — cùng mỏ neo, phép thay, ca đích với dò cùng tên của spec wp698
    # (Phụ lục A, C, H); mỏ neo không có xuống dòng viết NỐI CHUỖI để không tự va chạm. Tập dò đóng 419 chỉ đo ở nghiệm thu.
    ('w698_e49_nfkc_bk', 't53_', '    import re\n    bk, mh, ra = env.get(_BIEN_BAN_KINH), env.get(_BIEN_MANH), env.get(_BIEN_MANH_RA)\n', '    import re\n    bk, mh, ra = env.get(_BIEN_BAN_KINH), env.get(_BIEN_MANH), env.get(_BIEN_MANH_RA)\n    import unicodedata\n    bk = None if bk is None else unicodedata.normalize("NFKC", bk)\n'),
    ('w698_e49_nfkc_mh', 't53_', '    import re\n    bk, mh, ra = env.get(_BIEN_BAN_KINH), env.get(_BIEN_MANH), env.get(_BIEN_MANH_RA)\n', '    import re\n    bk, mh, ra = env.get(_BIEN_BAN_KINH), env.get(_BIEN_MANH), env.get(_BIEN_MANH_RA)\n    import unicodedata\n    mh = None if mh is None else unicodedata.normalize("NFKC", mh)\n'),
    ('w698_e49_nfkc_head', 't53_', '        head = p.stdout.strip() if p.returncode == 0 else ""\n', '        import unicodedata\n        head = unicodedata.normalize("NFKC", p.stdout).strip() if p.returncode == 0 else ""\n'),
    ('w698_e49_cf_bk', 't53_', '    import re\n    bk, mh, ra = env.get(_BIEN_BAN_KINH), env.get(_BIEN_MANH), env.get(_BIEN_MANH_RA)\n', '    import re\n    bk, mh, ra = env.get(_BIEN_BAN_KINH), env.get(_BIEN_MANH), env.get(_BIEN_MANH_RA)\n    import unicodedata\n    bk = None if bk is None else "".join(c for c in bk if unicodedata.category(c) != "Cf")\n'),
    ('w698_e49_cf_mh', 't53_', '    import re\n    bk, mh, ra = env.get(_BIEN_BAN_KINH), env.get(_BIEN_MANH), env.get(_BIEN_MANH_RA)\n', '    import re\n    bk, mh, ra = env.get(_BIEN_BAN_KINH), env.get(_BIEN_MANH), env.get(_BIEN_MANH_RA)\n    import unicodedata\n    mh = None if mh is None else "".join(c for c in mh if unicodedata.category(c) != "Cf")\n'),
    ('w698_e49_cf_head', 't53_', '        head = p.stdout.strip() if p.returncode == 0 else ""\n', '        import unicodedata\n        head = "".join(c for c in p.stdout if unicodedata.category(c) != "Cf").strip() if p.returncode == 0 else ""\n'),
    ('w698_x46_tab_bk', 't53_', '    import re\n    bk, mh, ra = env.get(_BIEN_BAN_KINH), env.get(_BIEN_MANH), env.get(_BIEN_MANH_RA)\n', '    import re\n    bk, mh, ra = env.get(_BIEN_BAN_KINH), env.get(_BIEN_MANH), env.get(_BIEN_MANH_RA)\n    bk = None if bk is None else bk.replace(chr(9), "")\n'),
    ('w698_x46_tab_mh', 't53_', '    import re\n    bk, mh, ra = env.get(_BIEN_BAN_KINH), env.get(_BIEN_MANH), env.get(_BIEN_MANH_RA)\n', '    import re\n    bk, mh, ra = env.get(_BIEN_BAN_KINH), env.get(_BIEN_MANH), env.get(_BIEN_MANH_RA)\n    mh = None if mh is None else mh.replace(chr(9), "")\n'),
    ('w698_x46_tab_head', 't53_', '        head = p.stdout.strip() if p.returncode == 0 else ""\n', '        head = p.stdout.replace(chr(9), "").strip() if p.returncode == 0 else ""\n'),
    ('w698_e49_ra_normpath', 't53_', '    return "manh", (k, n, ra)\n', '    return "manh", (k, n, os.path.normpath(ra))\n'),
    ('w698_e49_ra_expanduser', 't53_', '    return "manh", (k, n, ra)\n', '    return "manh", (k, n, os.path.expanduser(ra))\n'),
    ('w698_e50_bang_2', 't54_', '        if hong or tien_kiem_bo_qua:\n            _ket_thuc_manh(', '        if hong or tien_kiem_bo_qua or len(bo_qua) == 2:\n            _ket_thuc_manh('),
    ('w698_e50_tu_2', 't54_', '        if hong or tien_kiem_bo_qua:\n            _ket_thuc_manh(', '        if hong or tien_kiem_bo_qua or len(bo_qua) >= 2:\n            _ket_thuc_manh('),
    ('w698_x50_bang_n_tru_1', 't54_', '        if hong or tien_kiem_bo_qua:\n            _ket_thuc_manh(', '        if hong or tien_kiem_bo_qua or len(bo_qua) == len(CA) - 1:\n            _ket_thuc_manh('),
    ('w698_x47_hong_bang_1', 't54_', '        if hong or tien_kiem_bo_qua:\n            _ket_thuc_manh(', '        if len(hong) == 1 or tien_kiem_bo_qua:\n            _ket_thuc_manh('),
    ('w698_x47_tk_bang_1', 't54_', '        if hong or tien_kiem_bo_qua:\n            _ket_thuc_manh(', '        if hong or len(tien_kiem_bo_qua) == 1:\n            _ket_thuc_manh('),
    ('w698_s_ra_nfkc', 't53_', '    return "manh", (k, n, ra)\n', '    import unicodedata\n    return "manh", (k, n, unicodedata.normalize("NFKC", ra))\n'),
    ('w698_s_ra_cf', 't53_', '    return "manh", (k, n, ra)\n', '    import unicodedata\n    return "manh", (k, n, "".join(c for c in ra if unicodedata.category(c) != "Cf"))\n'),
    ('w698_s_ra_tab', 't53_', '    return "manh", (k, n, ra)\n', '    return "manh", (k, n, ra.replace(chr(9), ""))\n'),
    ('w698_s_ra_rstrip_slash', 't53_', '    return "manh", (k, n, ra)\n', '    return "manh", (k, n, ra.rstrip("/"))\n'),
    ('w698_s_ra_lstrip_dot', 't53_', '    return "manh", (k, n, ra)\n', '    return "manh", (k, n, ra[2:] if ra.startswith("./") else ra)\n'),
    ('w698_s_ra_expandvars', 't53_', '    return "manh", (k, n, ra)\n', '    import unicodedata\n    ra = os.path.expandvars(ra)\n    return "manh", (k, n, ra)\n'),
    ('w698_q_cf_mid_ra', 't53_', '    return "manh", (k, n, ra)\n', '    import unicodedata\n    ra = ra if len(ra) < 3 else ra[:1] + "".join(c for c in ra[1:-1] if not (unicodedata.category(c) == "Cf")) + ra[-1:]\n    return "manh", (k, n, ra)\n'),
    ('w698_m_cf_tag_ra', 't53_', '    return "manh", (k, n, ra)\n', '    import unicodedata\n    ra = "".join(c for c in ra if not (0xE0000 <= ord(c) <= 0xE007F))\n    return "manh", (k, n, ra)\n'),
    ('w698_q_cf_lead_bk', 't53_', '    import re\n    bk, mh, ra = env.get(_BIEN_BAN_KINH), env.get(_BIEN_MANH), env.get(_BIEN_MANH_RA)\n', '    import re\n    bk, mh, ra = env.get(_BIEN_BAN_KINH), env.get(_BIEN_MANH), env.get(_BIEN_MANH_RA)\n    import unicodedata\n    while bk and unicodedata.category(bk[0]) == "Cf":\n        bk = bk[1:]\n'),
    ('w698_q_cf_mid_head', 't53_', '        head = p.stdout.strip() if p.returncode == 0 else ""\n', '        import unicodedata\n        _s = p.stdout.strip()\n        _s = _s[:1] + "".join(c for c in _s[1:-1] if unicodedata.category(c) != "Cf") + _s[-1:]\n        head = _s if p.returncode == 0 else ""\n'),
    ('w698_q_tab_lead_mh', 't53_', '    import re\n    bk, mh, ra = env.get(_BIEN_BAN_KINH), env.get(_BIEN_MANH), env.get(_BIEN_MANH_RA)\n', '    import re\n    bk, mh, ra = env.get(_BIEN_BAN_KINH), env.get(_BIEN_MANH), env.get(_BIEN_MANH_RA)\n    mh = mh if mh is None else mh.lstrip(chr(9))\n'),
    ('w698_p_cf_head_17', 't53_', '        head = p.stdout.strip() if p.returncode == 0 else ""\n', '        import unicodedata\n        _s = p.stdout\n        _s = (_s[:17] + _s[17 + 1:]) if len(_s) > 17 and (lambda c: unicodedata.category(c) == "Cf")(_s[17]) else _s\n        head = _s.strip() if p.returncode == 0 else ""\n'),
    ('w698_m_cf_tag_bk', 't53_', '    import re\n    bk, mh, ra = env.get(_BIEN_BAN_KINH), env.get(_BIEN_MANH), env.get(_BIEN_MANH_RA)\n', '    import re\n    bk, mh, ra = env.get(_BIEN_BAN_KINH), env.get(_BIEN_MANH), env.get(_BIEN_MANH_RA)\n    bk = bk if bk is None else "".join(c for c in bk if not 0xE0000 <= ord(c) <= 0xE007F)\n'),
    ('w698_m_cf_061c_bk', 't53_', '    import re\n    bk, mh, ra = env.get(_BIEN_BAN_KINH), env.get(_BIEN_MANH), env.get(_BIEN_MANH_RA)\n', '    import re\n    bk, mh, ra = env.get(_BIEN_BAN_KINH), env.get(_BIEN_MANH), env.get(_BIEN_MANH_RA)\n    bk = bk if bk is None else bk.replace(chr(0x61C), "")\n'),
    ('w698_m_nfkc_ngoai_bmp_mh', 't53_', '    import re\n    bk, mh, ra = env.get(_BIEN_BAN_KINH), env.get(_BIEN_MANH), env.get(_BIEN_MANH_RA)\n', '    import re\n    bk, mh, ra = env.get(_BIEN_BAN_KINH), env.get(_BIEN_MANH), env.get(_BIEN_MANH_RA)\n    import unicodedata\n    mh = None if mh is None else "".join(unicodedata.normalize("NFKC", c) if (ord(c) >= 0x10000) else c for c in mh)\n'),
    ('w698_m_bodau_bk', 't53_', '    import re\n    bk, mh, ra = env.get(_BIEN_BAN_KINH), env.get(_BIEN_MANH), env.get(_BIEN_MANH_RA)\n', '    import re\n    bk, mh, ra = env.get(_BIEN_BAN_KINH), env.get(_BIEN_MANH), env.get(_BIEN_MANH_RA)\n    import unicodedata\n    bk = None if bk is None else "".join(c for c in unicodedata.normalize("NFD", bk) if unicodedata.category(c) != "Mn")\n'),
    ('w698_m_cc_head', 't53_', '        head = p.stdout.strip() if p.returncode == 0 else ""\n', '        import unicodedata\n        _s = p.stdout\n        _s = "".join(c for c in _s if not ((unicodedata.category(c) == "Cc" and c != chr(9))))\n        head = _s.strip() if p.returncode == 0 else ""\n'),
    ('w698_m_co_bk', 't53_', '    import re\n    bk, mh, ra = env.get(_BIEN_BAN_KINH), env.get(_BIEN_MANH), env.get(_BIEN_MANH_RA)\n', '    import re\n    bk, mh, ra = env.get(_BIEN_BAN_KINH), env.get(_BIEN_MANH), env.get(_BIEN_MANH_RA)\n    import unicodedata\n    bk = None if bk is None else "".join(c for c in bk if not (unicodedata.category(c) == "Co"))\n'),
    ('w698_s_bk_drop_zs', 't53_', '    import re\n    bk, mh, ra = env.get(_BIEN_BAN_KINH), env.get(_BIEN_MANH), env.get(_BIEN_MANH_RA)\n', '    import re\n    bk, mh, ra = env.get(_BIEN_BAN_KINH), env.get(_BIEN_MANH), env.get(_BIEN_MANH_RA)\n    bk = bk if bk is None else bk.translate({0xA0: None, 0x2003: None, 0x3000: None})\n'),
    ('w698_s_mh_drop_zs', 't53_', '    import re\n    bk, mh, ra = env.get(_BIEN_BAN_KINH), env.get(_BIEN_MANH), env.get(_BIEN_MANH_RA)\n', '    import re\n    bk, mh, ra = env.get(_BIEN_BAN_KINH), env.get(_BIEN_MANH), env.get(_BIEN_MANH_RA)\n    mh = mh if mh is None else mh.translate({0xA0: None, 0x2003: None, 0x3000: None})\n'),
    ('w698_s_head_strip_ascii', 't53_', '        head = p.stdout.strip() if p.returncode == 0 else ""\n', '        head = p.stdout.strip(" " + chr(9) + chr(10) + chr(11) + chr(12) + chr(13)) if p.returncode == 0 else ""\n'),
    ('w698_z_exc_all', 't53_', '    except (OSError, subprocess.SubprocessError):\n        head = ""\n', '    except Exception:\n        head = ""\n'),
    ('w698_z_exc_them_valueerror', 't53_', '    except (OSError, subprocess.SubprocessError):\n        head = ""\n', '    except (OSError, subprocess.SubprocessError, ValueError):\n        head = ""\n'),
    ('w698_s2_hong_va_khong_bq', 't54_', '        if hong or tien_kiem_bo_qua:\n            _ket_thuc_manh(', '        if (hong and not bo_qua) or tien_kiem_bo_qua:\n            _ket_thuc_manh('),
    ('w698_s2_hong_gt_bq', 't54_', '        if hong or tien_kiem_bo_qua:\n            _ket_thuc_manh(', '        if len(hong) > len(bo_qua) or tien_kiem_bo_qua:\n            _ket_thuc_manh('),
    ('w698_s2_tk_va_khong_bq', 't54_', '        if hong or tien_kiem_bo_qua:\n            _ket_thuc_manh(', '        if hong or (tien_kiem_bo_qua and not bo_qua):\n            _ket_thuc_manh('),
    ('w698_s3_xor', 't54_', '        if hong or tien_kiem_bo_qua:\n            _ket_thuc_manh(', '        if (hong and not tien_kiem_bo_qua) or (tien_kiem_bo_qua and not hong):\n            _ket_thuc_manh('),
    ('w698_x_exc_typeerror', 't53_', '    except (OSError, subprocess.SubprocessError):\n        head = ""\n', '    except (OSError, subprocess.SubprocessError, TypeError):\n        head = ""\n'),
    ('w698_x3_exc_kbint', 't53_', '    except (OSError, subprocess.SubprocessError):\n        head = ""\n', '    except (OSError, subprocess.SubprocessError, KeyboardInterrupt):\n        head = ""\n'),
    ('w698_x3_exc_re_error', 't53_', '    except (OSError, subprocess.SubprocessError):\n        head = ""\n', '    except (OSError, subprocess.SubprocessError, re.error):\n        head = ""\n'),
    ('w698_x_head_nl_last', 't53_', '        head = p.stdout.strip() if p.returncode == 0 else ""\n', '        head = p.stdout.strip().split(chr(10))[-1].strip() if p.returncode == 0 else ""\n'),
    ('w698_x3_head_emsp_last', 't53_', '        head = p.stdout.strip() if p.returncode == 0 else ""\n', '        head = p.stdout.strip().split(chr(0x2003))[-1].strip() if p.returncode == 0 else ""\n'),
    ('w698_x_cat_mc_bk', 't53_', '    import re\n    bk, mh, ra = env.get(_BIEN_BAN_KINH), env.get(_BIEN_MANH), env.get(_BIEN_MANH_RA)\n', '    import re\n    bk, mh, ra = env.get(_BIEN_BAN_KINH), env.get(_BIEN_MANH), env.get(_BIEN_MANH_RA)\n    import unicodedata\n    bk = None if bk is None else "".join(c for c in bk if not (unicodedata.category(c) == "Mc"))\n'),
    ('w698_x_main_ra_normpath', 't54_', '        k, n, ra = tham_so\n', '        import unicodedata\n        k, n, ra = tham_so\n        ra = os.path.normpath(ra)\n'),
    ('w698_x3_m3a_ra_nfkc', 't54_', '            _ket_thuc_manh(k, n, ra, ten, None, "nền đỏ hoặc tiền kiểm bị bỏ qua — không đo", _van_tay())\n', '            import unicodedata\n            _ket_thuc_manh(k, n, unicodedata.normalize("NFKC", ra), ten, None, "nền đỏ hoặc tiền kiểm bị bỏ qua — không đo", _van_tay())\n'),
    ('w698_x3_m3b_ra_cf', 't54_', '        dong, loi = _ket_thuc_manh(k, n, ra, ten, None if ly_con else ket, ly_con, _van_tay())\n', '        import unicodedata\n        dong, loi = _ket_thuc_manh(k, n, "".join(c for c in ra if unicodedata.category(c) != "Cf"), ten, None if ly_con else ket, ly_con, _van_tay())\n'),
    ('w698_x_wr_ra_nfkc', 't52_', '    tep = Path(ra)\n', '    import unicodedata\n    tep = Path(unicodedata.normalize("NFKC", ra))\n'),
    ('w698_x3_wr5_nfkc', 't52_', '    tep.' + 'write_bytes((', '    import unicodedata\n    Path(unicodedata.normalize("NFKC", str(tep))).write_bytes(('),
):
    DOT_BIEN[_ten] = ("ops/cong_cu_test.py", _tim, _thay, "TEP_TEST", _KEM_TEP_TEST, _CA_668[_ca])
# F36 (Codex lượt 15): nguồn vân tay — bảy cách băm SAI BYTES của TEP_TEST; con băm bảng byte cố định, cha tự băm lại.
_A36 = '    return {"sha256_test": hashlib.sha256(Path(TEP_TEST).read_bytes()).hexdigest(),\n'
for _ten, _doi in (("prefix_4096", "[:4096]"), ("prefix_64", "[:64]"), ("suffix_4096", "[-4096:]"), ("suffix_64", "[-64:]"),
                   ("ascii_ignore", '.decode("utf-8").encode("ascii", errors="ignore")'), ("casefold", ".lower()"),
                   ("bo_khoang_trang", '.replace(b" ", b"")')):
    DOT_BIEN["f36_" + _ten] = ("ops/cong_cu_test.py", _A36, _A36.replace("read_bytes()", "read_bytes()" + _doi),
                               "TEP_TEST", _KEM_TEP_TEST, _CA_668["t53_"])


def _la_dong_ho_nhay(ex) -> bool:
    """`TimeoutExpired` mang thời lượng ÂM — chữ ký của ĐỒNG HỒ NHẢY LÙI, không phải quá hạn.

    `TimeoutExpired.timeout` là con số `subprocess` in ra trong thông điệp. Một lượt chờ THẬT
    không thể hết hạn sau một khoảng ÂM: nó nghĩa là phép trừ hạn chót đi ngược, tức mốc thời
    gian nhảy lùi giữa chừng.

    ĐO ĐƯỢC 20-09-2026, nghiệm thu Windows `570-do-8` (máy chủ kho, 22:18 giờ máy, HEAD
    05ec2eb): `t28_bash_nen_tu_choi_bash_TREO_trong_han` chết
        TimeoutExpired: ... timed out after -232.95556909999868 seconds
    trên một `subprocess.run(..., timeout=120)`. Kho đã có sổ một bài học họ hàng — đo hạn chót
    XUYÊN TRẠNG THÁI NGỦ của máy trên Windows cần `QueryUnbiasedInterruptTime` — và chữ ký này
    KHỚP hình dạng ấy.

    NHƯNG KHỚP HÌNH DẠNG KHÔNG PHẢI ĐÃ ĐO. Vì sao mốc thời gian nhảy vẫn là `KHÔNG ĐO ĐƯỢC`:
    lượt ấy không ghi lại trạng thái nguồn của máy, và không có phản chứng. Hàm này KHÔNG
    khẳng định nguyên nhân — nó chỉ tách một cái chết ĐO ĐƯỢC LÀ BẤT THƯỜNG ra khỏi đống "lỗi
    vô can" chung chung, để lượt sau đọc được ngay thay vì đi truy con số âm.

    HẸP CÓ CHỦ ĐÍCH. Chỉ thời lượng ÂM mới tính. Một `timeout` DƯƠNG là quá hạn THẬT — có thể
    là đúng thứ ca đang đo — và nuốt nó sẽ biến cổng thành trang trí. `t32` chốt cả hai chiều.
    """
    return (isinstance(ex, subprocess.TimeoutExpired)
            and ex.timeout is not None and ex.timeout < 0)


def _chay_1_ca(fn):
    """Trả (trạng_thái, chi_tiết) với BỐN trạng thái, không phải hai.

    `giet_that`   — ca chết bằng CHỐT CỦA CHÍNH NÓ (`TinHieuChotCa` mang đúng tên ca).
    `tin_dung_gia` — ca chết vì thứ KHÁC: crash, parse hỏng, fixture sai, một
                    `AssertionError` trần do đường nào đó dựng lên, hoặc một chốt
                    GIÀN GIÁO (`dung()`) không qua — trường hợp cuối là R5-01, nơi
                    tiến trình con chết trước khi ca kịp đo thuộc tính của mình.
                    Đây KHÔNG phải bằng chứng đột biến bị chốt bắt.
    `bo_qua`      — thiếu môi trường. `qua` — sống sót.
    """
    global _CA_DANG_CHAY
    _CA_DANG_CHAY = fn.__name__
    try:
        fn()
        return "qua", None
    except BoQuaMoiTruong as ex:
        return "bo_qua", str(ex)
    except LoiDungCa as ex:
        # R5-01: giàn giáo hỏng ⇒ thuộc tính đích CHƯA CHẠY ⇒ không có gì để cấp tín dụng.
        return "tin_dung_gia", f"giàn giáo hỏng (chưa tới chốt nghiệp vụ): {ex}"
    except TinHieuChotCa as ex:
        nguon = getattr(ex, "ca_nguon", None)
        if nguon != fn.__name__:
            # Chốt của ca KHÁC lọt vào đây: vẫn là tín dụng giả.
            return "tin_dung_gia", f"chốt của ca khác ({nguon!r}): {ex}"
        return "giet_that", str(ex)
    except Exception as ex:  # noqa: BLE001 — chết dưới đột biến là DỮ LIỆU, không phải kết luận
        if _la_dong_ho_nhay(ex):
            # KHÔNG ĐO ĐƯỢC, không phải tín dụng giả: ca này chưa chạy xong vì MỐC THỜI GIAN
            # nhảy, nên quy nó vào bán kính của một đột biến là quy sai nguyên nhân.
            # `bo_qua` cho ca ĐÍCH vẫn làm `_ket_luan_ban_kinh` báo KHÔNG_ĐO_ĐƯỢC và tính lỗi —
            # cổng KHÔNG bị nới, chỉ thôi đổ tội cho đột biến.
            return "bo_qua", (
                f"KHÔNG ĐO ĐƯỢC: `{type(ex).__name__}` mang thời lượng ÂM ({ex.timeout}s) — "
                f"mốc thời gian nhảy lùi giữa lượt chờ, ca chưa chạy xong. Nguyên nhân của cú "
                f"nhảy: CHƯA ĐO. Chạy lại khi máy không ngủ để biến nó thành một phép đo. "
                f"Lệnh: {ex.cmd!r}")
        return "tin_dung_gia", f"{type(ex).__name__}: {ex}"
    finally:
        _CA_DANG_CHAY = None

def _bao_cao_nen_do(do_o_nen):
    """(dòng in, số lỗi) — báo MỘT LẦN các ca đã ĐỎ Ở NỀN, trước vòng lặp đột biến. Hàm THUẦN.

    SINH TỪ NGHIỆM THU WINDOWS `570-do-14` (ghim `1253e3a`): `t38` đỏ ở nền ⇒ 45/46 đột biến in
    "giết THÊM ['t38_…']", `lỗi đột biến=45`. Bốn mươi lăm dòng ấy là hệ quả của MỘT ca, và người
    đọc phải lội qua chúng mới thấy điều duy nhất có thật. Lần thứ HAI của hình dạng này (lần
    đầu `570-do-10`, `t34`, spec r6 §0) ⇒ chữa bằng CƠ CHẾ: ca đỏ ở nền bị LOẠI khỏi phép tính
    bán kính của mọi đột biến (`_ket_luan_ban_kinh(..., do_o_nen)`), được báo Ở ĐÂY đúng một
    lần, và VẪN là lỗi — `KHÔNG ĐO ĐƯỢC` không được lặng lẽ thành xanh, `None ≠ False`.
    """
    ds = sorted(set(do_o_nen))
    if not ds:
        return [], 0
    dong_nen = [f"  KHÔNG_ĐO_ĐƯỢC bán kính cho {ds}: ca đã ĐỎ Ở NỀN, trước mọi đột biến. Loại "
                f"khỏi phép tính bán kính của MỌI đột biến (chúng chết vì nền, không vì đột "
                f"biến), và vẫn tính là LỖI — một ca đỏ ở nền là một ca chưa đo được gì."]
    return dong_nen, 1


def _ket_luan_ban_kinh(ten_db, ca_dich, ket, tong_ca, do_o_nen=()):
    """Đọc một lượt đo bán kính thành (các_dòng_in, số_lỗi). Hàm THUẦN, không in, không I/O.

    `do_o_nen`: tên các ca đã ĐỎ Ở NỀN (r8, xem `_bao_cao_nen_do`). Chúng bị LOẠI khỏi cả tử
    số lẫn mẫu số của bán kính; đích nằm trong đó ⇒ KHÔNG_ĐO_ĐƯỢC và tính lỗi. `t42` trói.

    TÁCH KHỎI `main()` có lý do đo được, không phải cho gọn: bản cũ nằm inline nên đây là
    mảnh DUY NHẤT của bộ đo mà không ca nào gọi được — tức phần PHÁN QUYẾT không có phản
    chứng, đúng chỗ dễ sai nhất. Nay `t29` gọi thẳng vào đây.

    VÀ nó sửa một lời khai RỘNG HƠN PHÉP ĐO mà nghiệm thu Windows 20-09-2026 phơi ra
    (bộ đo `570-do-3`, log của chủ kho, HEAD 42dd49db). Trên Windows, đột biến
    `t22_bash_lay_ca_system_root` giết đích CỘNG 8 ca khác (bán kính 9/31) trong khi trên
    Linux nó đúng 1/31. Bản cũ in thẳng "⇒ trói nhầm thứ" — một KẾT LUẬN VỀ NGUYÊN NHÂN
    cho thứ nó mới chỉ ĐẾM. Có ít nhất hai nguyên nhân cho cùng con số ấy:
      (a) ca đích trói nhầm thuộc tính — đột biến rơi vào chỗ nhiều ca cùng đo;
      (b) đột biến nằm trên ĐƯỜNG CHUNG của giàn giáo — `_bash_windows()` là thứ `_chay()`
          dùng để phóng MỌI công cụ giả khi `os.name == "nt"`, nên gỡ chốt của nó thì mọi
          ca có subprocess đều chết, và chúng chết bằng CHỐT CỦA CHÍNH MÌNH nên vẫn xếp
          `giet_that`, không phải `tin_dung_gia`.
    Hai thứ ấy đòi hai cách chữa ngược nhau, và bản cũ KHÔNG in đủ dữ liệu để phân biệt:
    nó chỉ in TÊN ca oan, không in ca ấy chết vì gì. Nên lượt Windows kế tiếp sẽ lại đọc
    được đúng chừng ấy. `CLAUDE.md`: "ghi một nguyên nhân sai vào doctrine còn tệ hơn
    không ghi gì".

    ĐỎ vẫn là ĐỎ — hàm này KHÔNG nới cổng, nó chỉ thôi khẳng định thứ chưa đo và in kèm
    lý do từng ca oan để lượt sau CHẨN ĐOÁN được thay vì đoán.
    """
    loai = set(do_o_nen)
    if ca_dich in loai:
        return ([f"  KHÔNG_ĐO_ĐƯỢC {ten_db}: đích '{ca_dich}' đã ĐỎ Ở NỀN — nó chết trước khi "
                 f"đột biến chạm tới, nên không có gì để giết"], 1)
    ket = {t: v for t, v in ket.items() if t not in loai}
    tong = tong_ca - len(loai)
    # Đích vắng khỏi `ket` (bị `_do_ban_kinh` bỏ chạy) là KHÔNG ĐO ĐƯỢC, không phải KeyError.
    tt_dich = ket.get(ca_dich, ("bo_qua", "không có trong kết quả đo"))[0]
    chet = sorted(t for t, (tt, _) in ket.items() if tt in ("giet_that", "tin_dung_gia"))
    oan = [t for t in chet if t != ca_dich]
    bk = f"{len(chet)}/{tong}"
    gia = sorted(t for t, (tt, _) in ket.items() if tt == "tin_dung_gia")

    if tt_dich == "bo_qua":
        dau = [f"  KHÔNG_ĐO_ĐƯỢC {ten_db}: đích '{ca_dich}' bị BỎ QUA — "
               f"{ket.get(ca_dich, (None, 'không có trong kết quả đo'))[1]}"]
    elif tt_dich == "tin_dung_gia":
        dau = [f"  ĐỎ  {ten_db}: TÍN DỤNG GIẢ — đích '{ca_dich}' chết KHÔNG PHẢI bằng chốt "
               f"của nó: {ket[ca_dich][1]}"]
    elif tt_dich != "giet_that":
        dau = [f"  ĐỎ  {ten_db}: đích '{ca_dich}' vẫn XANH ⇒ đột biến không giết được gì"]
    elif gia:
        dau = [f"  ĐỎ  {ten_db}: ca {gia} chết bằng lỗi VÔ CAN (tín dụng giả) ⇒ bán kính "
               f"không đọc được"]
    elif oan:
        dau = [f"  ĐỎ  {ten_db}: giết THÊM {oan} ngoài đích '{ca_dich}' (bán kính {bk}). "
               f"CHƯA phân biệt được 'ca đích trói nhầm thuộc tính' với 'đột biến nằm trên "
               f"ĐƯỜNG CHUNG của giàn giáo' — đọc lý do dưới đây rồi mới kết luận:"]
    else:
        return ([f"  ok  {ten_db} → giết đúng '{ca_dich}' · bán kính {bk}"], 0)

    # MỘT đường ra cho MỌI nhánh ĐỎ: đổ toàn bộ ca không `qua`, kèm LÝ DO.
    #
    # Bản 20-09 sáng chỉ gắn lý do vào nhánh `oan` — đúng nhánh mà log Windows lượt 3 chỉ
    # ra — rồi lượt 5 rơi vào nhánh `gia` và lai KHÔNG đọc được gì: `t22_bash_lay_ca_system_root`
    # in ra ca `t2_canary_thieu_shellcheck_phai_SUY_GIAM` chết "bằng lỗi VÔ CAN" mà không nói
    # lỗi ấy là gì. Tức bản vá ĐÚNG nhưng HẸP, và khuyết tật sống nguyên ở nhánh anh em.
    # `CLAUDE.md` goi dung ten no: "va dung cho duoc chi roi bo sot duong thu ba" — chua theo
    # danh sach nguoi khac liet ke, phai TU liet ke het duong roi dong ca loat.
    # Nen do KHONG con la dac quyen cua mot nhanh: he ĐỎ thi in het.
    chi_tiet = [f"        · {t} [{tt}] {ly}" for t, (tt, ly) in sorted(ket.items()) if tt != "qua"]
    return (dau + chi_tiet, 1)


def _do_ban_kinh(ten_dot_bien, bo_qua_ca=()):
    """`bo_qua_ca`: ca đã ĐỎ Ở NỀN — không chạy lại dưới đột biến (chúng chết vì nền, chạy chỉ
    thêm nhiễu); `_ket_luan_ban_kinh` vẫn tự loại chúng nếu có mặt, nên hai lớp không mâu thuẫn."""
    tep, tim, thay, bp, phu_thuoc, ca_dich = DOT_BIEN[ten_dot_bien]
    cay, dich = _dung_cay_dot_bien(ten_dot_bien, tep, tim, thay, phu_thuoc)
    g, cu = globals(), globals()[bp]
    g[bp] = cay if bp == "GOC" else dich
    try:
        return {fn.__name__: _chay_1_ca(fn) for fn in CA
                if fn.__name__ not in set(bo_qua_ca)}, ca_dich
    finally:
        g[bp] = cu
        shutil.rmtree(cay, ignore_errors=True)


# --------------------------------------------------------------- T21/T22 (#445 gen 4)
# Hai ca ĐỎ THẬT trên lane windows-latest của master ngay sau khi #446 merge (run
# 33612364175, bước G5, `python ops/cong_cu.py kiem-tra --json` rc=2). Sổ land ghi MỘT
# nguyên nhân (git); log ghi HAI (git + bash). Mỗi ca dưới đây neo đúng một.

@ca
def t21_git_for_windows_hau_to_nha_cung_cap_phai_DAT_va_bat_tron():
    """Bản kê THẬT phải nhận `git version 2.55.0.windows.5` là MỘT token, không cắt.

    Regex cũ bắt `2.55.0` rồi `_cat_tien_to_token` từ chối vì ký tự kế là `.` — hành vi
    từ chối ấy ĐÚNG (t10) nên chỗ sửa là regex, không phải chốt. Ba đầu ra thật của ba
    nền đi qua cùng một regex đọc từ `ops/cong_cu.yaml`, KHÔNG chép regex vào test."""
    goc_yaml = GOC / "ops" / "cong_cu.yaml"
    if not goc_yaml.is_file():
        raise BoQuaMoiTruong("cây đang chạy thiếu ops/cong_cu.yaml — KHÔNG_ĐO_ĐƯỢC")
    regex = yaml.safe_load(goc_yaml.read_text(encoding="utf-8"))["cong_cu"]["git"]["probe"][0]["regex"]
    mau = (("git version 2.55.0.windows.5", "2.55.0.windows.5"),   # Git for Windows
           ("git version 2.43.0", "2.43.0"),                        # Linux
           ("git version 2.39.3 (Apple Git-146)", "2.39.3"))         # macOS
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        for i, (dong, mong) in enumerate(mau):
            d = tmp / f"bin{i}"; ten = f"git-gia-t21-{i}"
            bin_gia(d, ten, f"#!/bin/sh\necho '{dong}'\n")
            bk = ghi_ban_ke(tmp, {"git": {"bat_buoc": True, "ban_ghim": None,
                "probe": [{"ten": "mac_dinh", "lenh": [ten, "--version"], "regex": regex}]}})
            rc, out, _ = chay("kiem-tra", "--ban-ke", str(bk), "--json", env=moi_truong(d))
            bang(rc == 0, f"{dong!r} bị bản kê thật từ chối: rc={rc}\n{out}")
            thay = json.loads(out)["cong_cu"][0]["ban_thay"]["mac_dinh"]
            bang(thay == mong, f"{dong!r}: mong token {mong!r}, bản kê đọc thành {thay!r}")

@ca
def t22_bash_windows_quyet_bang_NANG_LUC_chu_khong_bang_DUONG_DAN():
    """`_bash_windows` phải NHẬN một `bash` POSIX THẬT nằm dưới `%SystemRoot%`.

    CA NÀY THAY THẾ `t22_bash_windows_khong_lay_bo_phong_wsl_o_system_root`, và phép đo nó
    đòi là phép **ĐẢO NGƯỢC** của ca cũ. Ca cũ khẳng định: ứng viên dưới `%SystemRoot%` bị
    LOẠI. Sau N14 mệnh đề ấy KHÔNG còn đúng, và không đúng có chủ đích — `CLAUDE.md`:
    *"danh sách CẤM không bao giờ đủ"*. Loại theo vị trí phân biệt CHỖ ĐỨNG chứ không phân
    biệt NĂNG LỰC: nó từ chối oan một `bash` thật đặt nhầm chỗ, và nhận một bộ phóng WSL đặt
    đúng chỗ. Thứ ra quyết định nay là `_do_nang_luc`.

    Giữ nguyên ca cũ là CẤM (spec r3 N15): một ca còn MẶT mà không còn ĐO chính là bệnh `t24`
    kho đã ghi sổ — nó vẫn được đếm ĐẠT trong khi không khẳng định gì về mã đang chạy.

    Ba chốt, phân biệt được bằng ĐẦU VÀO:
      (A) `bash` THẬT đặt dưới `%SystemRoot%` ⇒ được NHẬN. Mã cũ trả `None` ở đây.
      (B) `_bash_windows` trả ĐÚNG thứ `tim_bash` trả — tức nó uỷ quyền, không tự quyết.
      (C) một tệp TÊN là `bash` nhưng KHÔNG chạy được ⇒ `None`. Chốt (A) mà thiếu (C) thì
          chỉ chứng minh "nhận bừa", không chứng minh "quyết bằng năng lực".
    """
    that, _ = bash_nen.tim_bash()
    if not that:
        raise BoQuaMoiTruong("máy chạy test không có `bash` nào làm được việc — KHÔNG_ĐO_ĐƯỢC; "
                             "ca này cần một bash THẬT để đặt vào vị trí bị cấm cũ")
    sr = str(Path(that).resolve().parent)
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        xau = tmp / "khong-chay-duoc"
        xau.mkdir()
        for ten in ("bash", "bash.exe"):
            t = xau / ten
            t.write_text("khong phai chuong trinh\n", encoding="utf-8")
            try:
                t.chmod(0o755)
            except OSError:
                pass
        ma = ("import runpy, sys, json\n"
              f"sys.path.insert(0, {str(HERE)!r})\n"
              f"m = runpy.run_path({str(SCRIPT)!r})\n"
              "f = m['_bash_windows']\n"
              "import bash_nen\n"
              f"sr = {sr!r}; xau = {str(xau)!r}\n"
              "print('A ' + json.dumps(f(path=sr, system_root=sr, program_files=xau, git='')))\n"
              "print('B ' + json.dumps(bash_nen.tim_bash(path=sr, system_root=sr,"
              " program_files=xau, git='')[0]))\n"
              "print('C ' + json.dumps(f(path=xau, system_root=sr, program_files=xau, git='')))\n")
        env = dict(os.environ); env.pop("CONG_CU_BASH", None)
        p = subprocess.run([sys.executable, "-c", ma], env=env, cwd=GOC,
                           capture_output=True, text=True, timeout=300)
        dung(p.returncode == 0 and "A " in p.stdout,
             f"gọi _bash_windows hỏng: rc={p.returncode}\n{p.stdout}\n{p.stderr}")
        doc = {l[0]: json.loads(l[2:]) for l in p.stdout.splitlines()
               if l[:2] in ("A ", "B ", "C ")}
        bang(doc.get("A") is not None,
             f"(A) `bash` THẬT ({that!r}) đặt dưới %SystemRoot% bị TỪ CHỐI — đó là quyết theo "
             f"ĐƯỜNG DẪN, đúng thứ N14 gỡ bỏ. Nhận về: {doc.get('A')!r}\n{p.stdout}")
        bang(Path(doc["A"]).resolve().parent == Path(sr).resolve(),
             f"(A) nhận một đường KHÁC chỗ đã dựng: {doc['A']!r}, mong dưới {sr!r}")
        bang(doc.get("A") == doc.get("B"),
             f"(B) `_bash_windows` KHÔNG uỷ quyền: nó trả {doc.get('A')!r} còn `tim_bash` trả "
             f"{doc.get('B')!r}. Hai câu trả lời khác nhau nghĩa là còn một bộ giải thứ hai.")
        bang(doc.get("C") is None,
             f"(C) một tệp chỉ TÊN là `bash` mà không chạy được vẫn được nhận: {doc.get('C')!r} "
             f"⇒ không phải 'quyết bằng năng lực', chỉ là 'thôi không lọc nữa'")

_THU_MUC_QUET = (".claude/dev", "ops")

def _goi_ngoai(goc: Path, thu_muc=_THU_MUC_QUET) -> dict:
    """Tự dẫn xuất tập module BÊN THỨ BA mà kho import. KHÔNG ghi cứng tên nào.

    Ghi cứng `"jsonschema"` là danh sách CẤM trá hình: đóng đúng lần này rồi mù với
    gói kế tiếp. Ở đây quét AST, loại stdlib, loại stem tệp nội bộ — nên gói mới tự
    lọt vào tầm mắt mà không ai phải nhớ cập nhật danh sách.
    """
    import ast
    noi_bo = set()
    tep = []
    for d in thu_muc:
        thu = goc / d
        if not thu.is_dir():
            continue
        for q in sorted(thu.glob("*.py")):
            noi_bo.add(q.stem)
            tep.append(q)
    ra: dict = {}
    for q in tep:
        try:
            cay = ast.parse(q.read_text(encoding="utf-8"))
        except (SyntaxError, UnicodeDecodeError):
            continue
        for n in ast.walk(cay):
            if isinstance(n, ast.Import):
                tens = [a.name.split(".")[0] for a in n.names]
            elif isinstance(n, ast.ImportFrom) and n.level == 0 and n.module:
                tens = [n.module.split(".")[0]]
            else:
                continue
            for t in tens:
                if t in sys.stdlib_module_names or t in noi_bo:
                    continue
                ra.setdefault(t, []).append(str(q.relative_to(goc)))
    return ra

# Tên gói phân phối khác tên module import ở một số gói; ánh xạ ĐÚNG chỗ lệch, không
# nới phép so. Thiếu ánh xạ mà tên lệch thì ca ĐỎ — đó là hành vi mong muốn.
_MODULE_SANG_BAN_KE = {"yaml": "PyYAML"}


def _doi_cay_day_du(goc: Path) -> None:
    """Ba trạng thái: cây THIẾU thứ để đo là KHÔNG_ĐO_ĐƯỢC, không phải ĐỎ.

    Phân biệt hai chuyện khác hẳn nhau: (a) thư mục vắng HẲN ⇒ đang chạy trên cây tạm
    của bộ đột biến, ca này không đo được ở đây; (b) thư mục CÓ mà không tìm ra gì ⇒
    vấn đề thật, phải ĐỎ. Trộn hai cái là tự cấp tín dụng giả.
    """
    thieu = [str(x) for x in (goc / "ops" / "cong_cu.yaml",
                              goc / ".github" / "workflows" / "ci.yml")
             if not x.is_file()]
    thieu += [d for d in _THU_MUC_QUET if not (goc / d).is_dir()]
    if thieu:
        raise BoQuaMoiTruong(
            "cây đang chạy KHÔNG đầy đủ (thiếu: " + ", ".join(thieu) + ") — ca này đo "
            "quan hệ giữa bản kê, ci.yml và mã nguồn, nên ở đây là KHÔNG_ĐO_ĐƯỢC")


@ca
def t16_moi_goi_ben_thu_ba_phai_duoc_khai_trong_ban_ke():
    """Luật công cụ, dạng đo được. Không ghi cứng tên gói nào."""
    # Bộ chạy đột biến gán lại `GOC` sang một cây TẠM chỉ chứa tệp bị đột biến
    # (`_do_ban_kinh` d.416). Cây ấy không có thứ ca này đo ⇒ KHÔNG_ĐO_ĐƯỢC, KHÔNG phải
    # ĐỎ. Đọc sự VẮNG MẶT thành bằng chứng phủ định là đúng bệnh "chết vì lý do vô can":
    # nó sẽ khiến mọi đột biến `ci.yml` trông như bị ca này bắt được.
    _doi_cay_day_du(GOC)
    ban_ke = yaml.safe_load((GOC / "ops" / "cong_cu.yaml").read_text(encoding="utf-8"))
    khai = set(ban_ke["cong_cu"])
    ci = (GOC / ".github" / "workflows" / "ci.yml").read_text(encoding="utf-8")

    ngoai = _goi_ngoai(GOC)
    bang(ngoai, "phép quét không thấy gói bên thứ ba NÀO — bộ quét hỏng, không phải kho sạch")
    for ten, cac_tep in sorted(ngoai.items()):
        ten_ke = _MODULE_SANG_BAN_KE.get(ten, ten)
        # KHÔNG có cửa thoát "hoặc thấy tên trong ci.yml": bản kê là nguồn DUY NHẤT.
        # Bản đầu của ca này có mệnh đề ấy và ĐO ĐƯỢC là nó vô hiệu hoá cả ca — gỡ
        # `jsonschema` khỏi bản kê mà ca vẫn XANH vì tên còn trong ci.yml.
        bang(ten_ke in khai,
             f"gói bên thứ ba {ten!r} (import ở {cac_tep[0]}) chưa được khai trong "
             f"ops/cong_cu.yaml — thêm công cụ thì phải bảo đảm nền cài nó")

    # CHỐT CÓ RĂNG, chạy được NGAY HÔM NAY: phụ thuộc thật có thể chưa xuất hiện, nên
    # nếu không tự dựng một ca đỏ thì ca này xanh mà chưa đo gì — đúng bệnh "có MẶT
    # khác có ĐO".
    with tempfile.TemporaryDirectory(prefix="quet-goi-") as td:
        gia = Path(td)
        (gia / "ops").mkdir()
        (gia / "ops" / "mot_tep.py").write_text(
            "import mot_goi_khong_ai_khai\n", encoding="utf-8")
        thay = _goi_ngoai(gia, ("ops",))
        bang("mot_goi_khong_ai_khai" in thay,
             "bộ quét KHÔNG thấy import giả ⇒ nó không có răng, mọi cái xanh ở trên vô nghĩa")


@ca
def t17_ban_ghim_trong_ban_ke_khop_ban_ghim_trong_ci():
    """Hai chỗ ghim lệch nhau là hai bản trôi — cổng phải bắt được."""
    _doi_cay_day_du(GOC)          # xem chú thích ở t16
    ban_ke = yaml.safe_load((GOC / "ops" / "cong_cu.yaml").read_text(encoding="utf-8"))
    ci = (GOC / ".github" / "workflows" / "ci.yml").read_text(encoding="utf-8")
    do_duoc = 0
    for ten, dn in sorted(ban_ke["cong_cu"].items()):
        ghim = dn.get("ban_ghim")
        if not ghim:
            continue
        if f"{ten}=={ghim}" in ci:
            do_duoc += 1
            continue
        # Tên có mặt trong ci.yml nhưng KHÁC bản ghim ⇒ trôi. Tên vắng hẳn thì công cụ
        # ấy do đường khác cài (vd script riêng), không phải chuyện của ca này.
        bang(f"{ten}==" not in ci,
             f"{ten}: bản ghim trong cong_cu.yaml là {ghim!r} nhưng ci.yml ghim khác")
    bang(do_duoc >= 1,
         "không đo được cặp ghim nào — ca này đang xanh mà chưa đo gì")


@ca
def t18_inventory_bat_buoc_cua_launcher_phai_nam_trong_ban_ke():
    """Launcher và preflight CI không được giữ hai danh sách bắt buộc bị trôi."""
    _doi_cay_day_du(GOC)
    import runpy
    p = GOC / ".claude" / "dev" / "launcher.py"
    launcher_ns = runpy.run_path(str(p), run_name="launcher_inventory_t18")
    launcher = {x["ten"] for x in launcher_ns["CONG_CU"] if x.get("bat_buoc") is True}
    ban_ke = yaml.safe_load((GOC / "ops" / "cong_cu.yaml").read_text(encoding="utf-8"))
    chung = set(ban_ke["cong_cu"])
    thieu = launcher - chung
    bang(not thieu, f"launcher khai bắt buộc nhưng bản kê chung bỏ sót: {sorted(thieu)}")
    bang({"rg", "bash"} <= launcher, "đối chứng launcher mất rg/bash nên t18 không còn răng")


@ca
def t19_moi_cong_cu_bat_buoc_co_cong_thuc_ba_nen():
    """Bỏ một recipe nền phải đỏ trước khi môi trường đó cần cài thật."""
    _doi_cay_day_du(GOC)
    ban_ke = yaml.safe_load((GOC / "ops" / "cong_cu.yaml").read_text(encoding="utf-8"))
    for ten, dn in ban_ke["cong_cu"].items():
        if not (dn["bat_buoc"] or dn.get("chuan_bi")):
            continue
        cai = dn.get("cai") or {}
        if "lenh" in cai:  # công thức portable dùng chung ba nền
            continue
        thieu = {n for n in ("linux", "macos", "windows") if not (cai.get(n) or {}).get("lenh")}
        bang(not thieu, f"{ten}: thiếu công thức cài cho {sorted(thieu)}")


@ca
def t20_che_do_cai_tat_ca_bootstrap_pyyaml_dung_ban_ghim():
    """Lệnh chuẩn bị chung phải tồn tại và pin bootstrap khớp CI/bản kê."""
    _doi_cay_day_du(GOC)
    sh = CAI_SH.read_text(encoding="utf-8")
    bk = yaml.safe_load((GOC / "ops" / "cong_cu.yaml").read_text(encoding="utf-8"))
    ci = (GOC / ".github" / "workflows" / "ci.yml").read_text(encoding="utf-8")
    bang('TEN" = "--bat-buoc"' in sh and 'for cong_cu in "${BAT_BUOC[@]}"' in sh,
         "cai_cong_cu.sh chưa có đường cài mọi công cụ bắt buộc")
    import re
    pins = set(re.findall(r"PyYAML==(\d+(?:\.\d+)+)", sh + "\n" + ci))
    bang(pins == {"6.0.3"}, f"bootstrap PyYAML trôi phiên bản giữa script và CI: {pins}")
    bang(bk["cong_cu"]["PyYAML"]["bat_buoc"] is True,
         "PyYAML bootstrap mà không bắt buộc trong bản kê")


def _chay_batch(crlf: bool):
    """Dựng cây tạm + python giả rồi chạy `cai_cong_cu.sh --bat-buoc`. Trả (p, pip_ready).

    `crlf=True` cho python giả in CRLF — đúng thứ Git Bash trên Windows nhận từ python
    native (text mode). Tái hiện được trên Linux, nên t23 đo được ở đây, không đợi lane
    windows-latest."""
    bash = _bash_dung_duoc("batch")
    with tempfile.TemporaryDirectory(prefix="cong-cu-batch-") as td:
        root = Path(td); ops = root / "ops"; ops.mkdir(); out = root / "installed"
        fake_bin = root / "fake-bin"; fake_bin.mkdir(); pip_ready = root / "pip-ready"
        shutil.copy2(CAI_SH, ops / "cai_cong_cu.sh")
        shutil.copy2(SCRIPT, ops / "cong_cu.py")
        for rel in KEM_THEO_CONG_CU:
            # `_GOC_THAT` chu KHONG `GOC`: `GOC` bi mot so dot bien tro sang cay tam, va cay ay
            # chi mang dung nhung tep dot bien ay khai. Doc phu thuoc qua `GOC` bien mot dot
            # bien cua HO KHAC thanh `FileNotFoundError` o day — mot cai chet VO CAN lam ban
            # kinh khong doc duoc. DO DUOC 20-09-2026: `t6_day_g5_sau_py_compile` va
            # `t21_git_regex_cat_hau_to` (ca hai bp=GOC, phu_thuoc RIENG khong co bash_nen.py)
            # keo `t23_batch...` va `t30` chet nhu the.
            # Va day la ly do KHONG them ten vao hai danh sach ay: lam the la va DIEM thu tu
            # cua cung mot hinh dang. Doc tu snapshot bat bien thi moi dot bien tuong lai — ke
            # ca dot bien chua ai viet — deu khong dung toi duoc cho nay.
            shutil.copy2(_GOC_THAT / rel, ops / Path(rel).name)
        name = "batch-path-t21"
        manifest = {"schema_version": 1, "cong_cu": {name: {
            "bat_buoc": True, "ban_ghim": "1.2.3",
            "probe": [{"ten": "mac_dinh", "lenh": [name, "--version"],
                       "regex": r"(\d+\.\d+\.\d+)"}],
            "cai": {"lenh": (f"mkdir -p '{out}'; printf '#!/bin/sh\\necho 1.2.3\\n' "
                                f"> '{out / name}'; chmod +x '{out / name}'; echo '{out}'")}}}}
        (ops / "cong_cu.yaml").write_text(yaml.safe_dump(manifest), encoding="utf-8")
        fake_python = fake_bin / "python"
        # Nhánh CRLF: đi qua ống `sed` để mỗi dòng stdout kết thúc bằng \r\n, giữ rc của python.
        duoi = ('"$REAL" "$@" | sed \'s/$/\\r/\'; exit "${PIPESTATUS[0]}"\n' if crlf
                else "exec \"$REAL\" \"$@\"\n")
        fake_python.write_text(
            "#!/bin/bash\n"
            f"MARKER='{pip_ready}'\nREAL='{sys.executable}'\n"
            "[ \"${1:-}\" = -c ] && [ \"${2:-}\" = 'import yaml' ] && "
            "[ ! -e \"$MARKER\" ] && exit 1\n"
            "[ \"${1:-}\" = -c ] && [ \"${2:-}\" = 'import pip' ] && "
            "[ ! -e \"$MARKER\" ] && exit 1\n"
            "[ \"${1:-}\" = -m ] && [ \"${2:-}\" = ensurepip ] && "
            "{ : > \"$MARKER\"; exit 0; }\n"
            "[ \"${1:-}\" = -m ] && [ \"${2:-}\" = pip ] && exit 0\n"
            + duoi, encoding="utf-8")
        fake_python.chmod(0o755)
        env = dict(os.environ, PATH=str(fake_bin) + os.pathsep + os.environ.get("PATH", ""))
        p = subprocess.run([bash, "./cai_cong_cu.sh", "--bat-buoc"], cwd=ops,
                           env=env, capture_output=True, text=True, timeout=60)
        return p, pip_ready.is_file()


def batch_behavior_test() -> None:
    """Batch giữ PATH từ installer con và chạy được từ CWD ngoài root.

    Không đưa vào `CA`: đây là integration control cho wrapper, không được dùng để
    nhận công giết thêm các mutation đơn vị T1..T15.
    """
    p, pip_ready = _chay_batch(crlf=False)
    bang(p.returncode == 0 and '"trang_thai_tong": "DAT"' in p.stdout,
         f"batch không giữ PATH/caller-CWD: rc={p.returncode}\n{p.stdout}\n{p.stderr}")
    bang(pip_ready, "batch gọi pip trước khi bootstrap ensurepip")


@ca
def t23_batch_chiu_duoc_stdout_CRLF_cua_python_windows():
    """Git Bash trên Windows nhận stdout CRLF từ python native; `read -r` giữ `\r`.

    Đo thật: run 33629605694 lane windows-latest, `batch_behavior_test` rc=3 với
    "khong biet cong cu 'batch-path-t21\r'" — lỗi có sẵn trong #446, bị che vì master chưa
    từng chạy tới bước này (G5 chết trước ở git/bash). Tái hiện trên Linux bằng python giả
    in CRLF; ca ĐỎ trước bản vá, XANH sau."""
    p, _ = _chay_batch(crlf=True)
    bang(p.returncode == 0 and '"trang_thai_tong": "DAT"' in p.stdout,
         f"stdout CRLF làm batch hỏng: rc={p.returncode}\n{p.stdout}\n{p.stderr}")
    bang("\\r" not in p.stderr and "khong biet cong cu" not in p.stderr,
         f"vẫn lọt \\r vào tên công cụ: {p.stderr}")


@ca
def t60_import_bash_nen_khong_in_gi_ra_stderr():
    """#671 — nạp `bash_nen.py` KHÔNG được in gì ra stderr, trên MỌI nền.

    Đo thật: run 36454930689 lane windows-latest, `t23_batch...` ĐỎ với stderr
    `C:\\Users\\runneradmin\\...\\bash_nen.py:900: SyntaxWarning: invalid escape sequence '\\('`
    — docstring `_tach_dinh_dang` không raw. Đường dẫn Windows mang `\\r` (`\\runneradmin`)
    nên chốt "không lọt `\\r`" của `t23` bắt nhầm cảnh báo. Linux không thấy vì `bash_nen`
    chỉ được import trong `_bash_windows`, và vì 3.11 xếp lỗi này vào `DeprecationWarning`
    (ẩn mặc định) chứ không phải `SyntaxWarning`. Nên ca đo HAI thứ, không phụ thuộc nền:
    (1) biên dịch nguồn với mọi cảnh báo thành LỖI; (2) nạp THẬT trong tiến trình con với
    `-W default` và đòi stderr RỖNG."""
    import warnings
    nguon = Path(BASH_NEN).read_text(encoding="utf-8")
    with warnings.catch_warnings():
        warnings.simplefilter("error")
        try:
            compile(nguon, str(BASH_NEN), "exec")
        except (SyntaxError, SyntaxWarning, DeprecationWarning) as e:
            bang(False, f"(1) bash_nen.py biên dịch kèm cảnh báo: {type(e).__name__}: {e}")
    # Nạp từ BẢN SAO trong thư mục tạm MỚI + `-B`: một `.pyc` còn hợp lệ cạnh nguồn thật sẽ
    # bỏ qua biên dịch và làm chốt này CÂM (đo được khi soạn: chốt (2) một mình XANH trên nền
    # đỏ chỉ vì `__pycache__/bash_nen.cpython-312.pyc` có sẵn).
    with tempfile.TemporaryDirectory(prefix="bn-import-") as td:
        shutil.copy2(BASH_NEN, Path(td) / "bash_nen.py")
        p = subprocess.run(
            [sys.executable, "-B", "-W", "default", "-c",
             "import sys; sys.path.insert(0, sys.argv[1]); import bash_nen", td],
            capture_output=True, text=True, timeout=60)
    bang(p.returncode == 0 and p.stderr == "",
         f"(2) import bash_nen rc={p.returncode}, stderr không rỗng: {p.stderr[:300]!r}")


_NAP_UTF8 = """import importlib.util, io, subprocess, sys
print('(0) nap', flush=True)
spec = importlib.util.spec_from_file_location('cct_utf8', sys.argv[1])
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
print('NAP_OK', flush=True)
print('(a) chữ Việt', flush=True)
print('(c) chữ Việt', file=sys.stderr, flush=True)
chau = ("import json, os, sys; print('(b) ch' + chr(0x1eef) + ' Vi' + chr(0x1ec7) + 't'); print('(d)', json.dumps("
        "[sys.flags.utf8_mode, os.environ.get('PYTHONUTF8'), os.environ.get('PYTHONIOENCODING')]))")
p = subprocess.run([sys.executable, '-c', chau], capture_output=True)
sys.stdout.flush(); sys.stdout.buffer.write(p.stdout); sys.stdout.buffer.flush()
o = sys.stdout, sys.stderr
sys.stdout = sys.stderr = io.StringIO()
try:
    m._ep_utf8({}); f = 'ok'
except Exception as x:
    f = type(x).__name__
sys.stdout, sys.stderr = o
print('(f)', f, flush=True)
print('(g)', chr(0xdcff), flush=True)
"""


@ca
def t61_ep_UTF8_phai_co_RANG_ca_khi_moi_truong_ngoai_la_ASCII():
    """#671 (nợ CONG-CU-TEST-EP-UTF8) — nạp tệp này trong một tiến trình con CỐ Ý ép ASCII rồi đo BYTE, mỗi
    vế một chốt: (a) stdout, (c) stderr của nó mang chữ Việt UTF-8 THẬT; (b) cháu phóng KHÔNG `env=` in byte
    UTF-8 thật và (d) báo `utf8_mode=1`, `PYTHONUTF8=1`, `PYTHONIOENCODING=utf-8`; (f) luồng thiếu
    `reconfigure` không làm `_ep_utf8` ném; (g) surrogate lạc ra chữ thoát, không ném; (e) NẠP không phóng
    lại người nạp. Dựng ASCII NGAY TẠI ĐÂY vì CI tự đặt biến UTF-8. Lượt 4: bản cũ suy từ MÃ THOÁT nên sáu
    đột biến sống (review lượt 2+3), và mã `-c` mang chữ Việt làm con chết lúc giải mã argv dưới `LC_ALL=C`
    — ĐỎ oan, quy nhầm cho (a). Nay mã con thuần ASCII (thoát lúc chạy), mã cháu viết bằng `chr`."""
    env = dict(os.environ, PYTHONIOENCODING="ascii", PYTHONUTF8="0")
    p = subprocess.run([sys.executable, "-B", "-c", _NAP_UTF8.encode("ascii", "backslashreplace").decode(),
                        str(TEP_TEST)], env=env, cwd=GOC, capture_output=True, timeout=120)
    ra, loi = p.stdout, p.stderr
    tom = f"rc={p.returncode} stdout={ra[-300:]!r} stderr={loi[-300:]!r}"
    dung(b"(0) nap" in ra, f"giàn giáo: tiến trình nạp không khởi chạy được: {tom}")
    bang(ra.count(b"(0) nap") == 1, f"(e) NẠP cong_cu_test.py mà người nạp bị PHÓNG LẠI — chốt `__main__` mất: {tom}")
    dung(b"NAP_OK" in ra, f"giàn giáo: nạp cong_cu_test.py hỏng, chưa tới chốt nào: {tom}")
    bang("(a) chữ Việt".encode() in ra, f"(a) stdout của tiến trình nạp không mang chữ Việt UTF-8: {tom}")
    bang("(c) chữ Việt".encode() in loi, f"(c) stderr của tiến trình nạp không mang chữ Việt UTF-8 THẬT: {tom}")
    bang("(b) chữ Việt".encode() in ra, f"(b) cháu (không `env=`) không in được byte UTF-8 thật: {tom}")
    bang(b'(d) [1, "1", "utf-8"]' in ra, f"(d) cháu phải ở UTF-8 mode, PYTHONUTF8=1, PYTHONIOENCODING=utf-8: {tom}")
    bang(b"(f) ok" in ra, f"(f) luồng KHÔNG có `reconfigure` làm `_ep_utf8` ném: {tom}")
    bang(b"(g) " + bytes([92]) + b"udcff" in ra, f"(g) in surrogate lạc phải ra chữ thoát, không ném: {tom}")


@ca
def t62_chay_lam_main_phai_o_che_do_UTF8_ca_khi_PYTHONUTF8_0():
    """#671 — chạy tệp này làm `__main__` với `PYTHONUTF8=0` thì tiến trình CHẠY BỘ CA vẫn phải ở chế
    độ UTF-8. Đo CỜ (`sys.flags.utf8_mode`) chứ không đo một lần giải mã: trên Linux locale đã là UTF-8
    nên phép giải mã xanh cả khi gỡ bản vá, còn cờ thì phân biệt được trên MỌI nền. Hậu quả đo được
    khi cờ tắt (Windows cp1258): `t29`/`t39`/`t42`/`t45` ĐỎ vì cha đọc `text=True` bằng locale.
    Lượt 4 (đột biến sống 56/56 ở review lượt 2+3): khoá TỪNG vế còn lại của hợp đồng phóng lại — (1) mã
    thoát (cửa trả mã RIÊNG, nuốt thành 0 là đỏ); (2) `-B` còn; (3) dấu phóng lại không sót sang con; (4)
    `-X utf8=0` vẫn ra UTF-8 sau đúng MỘT lần; (5) đã mang dấu mà vẫn ngoài UTF-8 thì DỪNG; (6) nguồn stdin
    (`-` và trần) thì DỪNG ồn ào, không `rc=0` rỗng. `t62` không phụ thuộc bộ ca có tự phóng lại hay không.
    `env` đã gỡ `PYTHONDONTWRITEBYTECODE` ⇒ MỌI lời gọi mang `-B`, (0)(4) đòi `B=1`: không ghi `.pyc` vào cây."""
    env = dict(os.environ, PYTHONUTF8="0", PYTHONIOENCODING="ascii")
    for k in (_DAU_PHONG_LAI, "PYTHONDONTWRITEBYTECODE"):
        env.pop(k, None)

    def hoi(*lenh, nhap=None, **them):
        p = subprocess.run([sys.executable, *lenh], input=nhap, env=dict(env, **them), cwd=HERE,
                           capture_output=True, timeout=120)
        return p.returncode, p.stdout.decode("utf-8", "replace"), p.stderr.decode("utf-8", "replace")[-300:]

    rc, ra, loi = hoi("-B", str(TEP_TEST), "--tu-kiem-che-do-utf8")
    dung("UTF8_MODE=" in ra, f"cửa --tu-kiem-che-do-utf8 không in gì: rc={rc} {loi!r}")
    bang("UTF8_MODE=1" in ra,
         f"chạy làm __main__ với PYTHONUTF8=0 mà tiến trình chạy bộ ca KHÔNG ở chế độ UTF-8: {ra.strip()!r}")
    bang(rc == _MA_TU_KIEM_UTF8, f"(1) mã thoát KHÔNG đi qua lần phóng lại: rc={rc}, chờ {_MA_TU_KIEM_UTF8}")
    bang("B=1" in ra, f"(2) cờ `-B` mất ở lần phóng lại: {ra.strip()!r}")
    bang("DAU_SOT=0" in ra, f"(3) dấu phóng lại còn trong môi trường của bản phóng lại: {ra.strip()!r}")
    rc, ra, loi = hoi("-B", "-X", "utf8=0", str(TEP_TEST), "--tu-kiem-che-do-utf8")
    bang(rc == _MA_TU_KIEM_UTF8 and "UTF8_MODE=1" in ra and "DA_PHONG_LAI=1" in ra and "B=1" in ra,
         f"(4) gọi `-X utf8=0` mà không ra UTF-8 (giữ `-B`) sau đúng MỘT lần phóng: rc={rc} {ra.strip()!r} {loi!r}")
    rc, ra, loi = hoi("-B", str(TEP_TEST), "--tu-kiem-che-do-utf8", **{_DAU_PHONG_LAI: "1"})
    bang(rc not in (0, _MA_TU_KIEM_UTF8) and "KHONG_PHONG_LAI" in loi and "UTF8_MODE" not in ra,
         f"(5) đã mang dấu phóng lại mà vẫn ngoài UTF-8 phải DỪNG, không phóng tiếp: rc={rc} {ra.strip()!r} {loi!r}")
    for co in (("-B", "-", "--tu-kiem-che-do-utf8"), ("-B",)):
        rc, ra, loi = hoi(*co, nhap=TEP_TEST.read_bytes())
        bang(rc != 0 and "KHONG_PHONG_LAI" in loi,
             f"(6) `python {' '.join(co)} < cong_cu_test.py` ngoài UTF-8 phải DỪNG ồn ào, không chạy chương "
             f"trình RỖNG: rc={rc} stdout={len(ra)} ký tự {loi!r}")


def _k32_gia(hong=""):
    """kernel32 GIẢ cho `t64` — giữ TRẠNG THÁI (bảng job, cờ đọc từ BYTE cấu trúc, thành viên, kế thừa lúc phóng),
    KHÔNG diễn kịch bản: `cha_chet()` giết ai là do trạng thái `_phong_lai` đã dựng. Mỗi API là HÀM C thật
    (`CFUNCTYPE`, chữ ký Win32) nên ctypes CHUYỂN KIỂU theo argtypes/restype SẢN PHẨM khai — handle giả > 32 bit
    (restype sai thì bị cắt), thiếu/lệch `byref` thì lỗi ở BIÊN, không lọt. `hong` = tên API bị bắt trả 0."""
    import ctypes, threading, types
    vp, i = ctypes.c_void_p, ctypes.c_int
    H = 1 << (8 * ctypes.sizeof(vp) - 4)       # handle nền > 32 bit: restype mặc định `c_int` cắt còn 32 là HỎNG THẬT
    M = ctypes.c_void_p(-1).value              # GetCurrentProcess() giả trả pseudo-handle (giá trị -1 ép qua c_void_p)
    k = types.SimpleNamespace(job={}, con=[], exec=[], co=threading.Event(), giu=[])

    def api(ten, f, kq, *ds):  # `f` bọc thành hàm C (chữ ký Win32 `kq, *ds`) rồi ép về con trỏ CFUNCTYPE(c_int) TRẦN
        cb = ctypes.CFUNCTYPE(kq, *ds)(lambda *a: 0 if ten == hong else f(*a))
        k.giu.append(cb)       # SẢN PHẨM tự gán argtypes/restype như với WinDLL; `k.giu` giữ callback sống kẻo treo
        setattr(k, ten, ctypes.CFUNCTYPE(i)(ctypes.cast(cb, vp).value))

    def dat(h, lop, p, n):     # `p` = ĐỊA CHỈ ctypes thật truyền sang; đọc cờ LimitFlags tại p+16 (4 byte)
        ok = h in k.job and lop == 9 and p and n == (144 if ctypes.sizeof(vp) == 8 else 112)
        if ok:
            k.job[h].update(co=int.from_bytes(ctypes.string_at(p + 16, 4), "little"))
        return int(bool(ok))

    def popen(lenh, **kw):
        k.con.append(subprocess.Popen(lenh, **kw))  # phóng từ thành viên ⇒ con thuộc job, trừ khi job cho thoát lặng
        [j["tv"].add(k.con[-1]) for j in k.job.values() if "cha" in j["tv"] and not j["co"] & 0x1000]
        return k.co.set() or k.con[-1]  # báo hiệu SAU khi đã ghi thành viên — trước thì `cha_chet` đua với dòng trên
    api("CreateJobObjectW", lambda *_: k.job.setdefault(H + len(k.job) + 1, dict(co=0, tv=set())) and max(k.job), vp, vp, vp)
    api("SetInformationJobObject", dat, i, vp, i, vp, ctypes.c_uint32)
    api("AssignProcessToJobObject", lambda h, p: h in k.job and p == M and not k.job[h]["tv"].add("cha"), i, vp, vp)
    api("GetCurrentProcess", lambda: -1, vp)
    k.popen, k.execve = popen, lambda *a: (k.exec.append(a), k.co.set())
    k.cha_chet = lambda: [p.kill() for j in k.job.values() if j["co"] & 0x2000 for p in j["tv"] - {"cha"}]  # handle cuối đóng
    return k


@ca
def t64_phong_lai_KHONG_de_MO_COI_khi_bi_giet_va_ma_thoat_giu_TIN_HIEU():
    """#671 lượt 6 — MỒ CÔI. Chạy PHẦN ĐẦU chính tệp này (tới `import yaml`: `_phong_lai` + khối phóng lại) + cửa chờ stdin,
    `PYTHONUTF8=0` ⇒ phóng lại THẬT: (k1) harness `kill()` pid nó biết ⇒ stdout EOF ≤10s, mọi nền (Windows: Job THẬT). POSIX:
    (k2) SIGTERM tới pid CHẠY BỘ CA ⇒ harness thấy -15 (`subprocess` ra 241); (k3) bộ ca KHÔNG lờ SIGINT (SIG_IGN trước exec KẾ
    THỪA) — đọc TRẠNG THÁI: GỬI SIGINT thì đua (tới trước khi `read()` chặn ⇒ treo: ĐUA hiếm, đo trên Python trần); con khởi đầu với
    SIGINT/SIGTERM mặc định (chạy nền `&` là SIG_IGN — bỏ `preexec_fn` thì LUÔN đỏ oan, đo được). Mô phỏng `_k32_gia`: (w0) nt KHÔNG exec; (w1) cha chết ⇒
    con chết; (w2) Job hỏng ⇒ vẫn chạy + nói ra."""
    import contextlib, io, signal, threading
    nguon, cat = TEP_TEST.read_text(encoding="utf-8"), "\nimport yaml\n"
    dung(nguon.count(cat) == 1, "giàn giáo: không cắt được phần đầu tại `import yaml`")
    env = dict({k: v for k, v in os.environ.items() if k != _DAU_PHONG_LAI}, PYTHONUTF8="0")
    mac_dinh = (lambda: [signal.signal(s, signal.SIG_DFL) for s in (signal.SIGINT, signal.SIGTERM)]) if os.name == "posix" else None
    with tempfile.TemporaryDirectory(prefix="t64-") as td:
        (tep := Path(td) / "dau.py").write_text(nguon.split(cat)[0] + "\nimport signal\nprint(f'PID={os.getpid()} U8={sys.flags.utf8_mode} PL="
                                                "{int(_DA_PHONG_LAI)} INT={signal.getsignal(2) is signal.default_int_handler:d}', flush=True)"
                                                "\nsys.stdin.read()\n", encoding="utf-8")
        for sig in (None,) + ((signal.SIGTERM,) if os.name == "posix" else ()):
            with subprocess.Popen([sys.executable, str(tep)], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE, env=env, preexec_fn=mac_dinh) as p:
                (hen := threading.Timer(120, p.kill)).start()  # treo không in ⇒ giết ⇒ `dung` dưới ĐỎ, không treo tới trần job
                dau, rc = p.stdout.readline().decode("utf-8", "replace"), None
                hen.cancel()
                dung("U8=1 PL=1" in dau, f"giàn giáo: phần đầu không phóng lại sang UTF-8 — không đo gì: {dau!r}")
                pid = int(dau.split()[0][4:])
                bang(os.name != "posix" or "INT=1" in dau, f"(k3) tiến trình chạy bộ ca {pid} LỜ SIGINT/Ctrl-C: {dau!r}")
                if sig is None:
                    p.kill(); (doc := threading.Thread(target=p.stdout.read)).start(); doc.join(10)
                    song = doc.is_alive(); p.stdin.close(); doc.join(60)
                    bang(not song, f"(k1) harness kill() pid {p.pid} mà tiến trình chạy bộ ca {pid} vẫn giữ pipe sau 10s — MỒ CÔI")
                    continue
                os.kill(pid, sig)
                with contextlib.suppress(subprocess.TimeoutExpired):
                    rc = p.wait(10)  # (còn sống thì `__exit__` đóng stdin ⇒ EOF ⇒ tự thoát)
                bang(rc == -sig, f"(k2) SIGTERM tới tiến trình chạy bộ ca {pid} (harness biết {p.pid}) mà harness thấy rc={rc}, chờ {-sig}")
        for fd in (1, 2) if os.name == "posix" else ():  # (k4) fd ĐÓNG lúc gọi ⇒ sys.stdout/stderr None: phần đầu VẪN phóng
            r = subprocess.run([sys.executable, str(tep)], input=b"", capture_output=True, env=env, timeout=120,
                               preexec_fn=lambda: os.close(fd))
            bang(r.returncode == 0, f"(k4) fd {fd} đóng ⇒ nổ trước khi phóng lại: rc={r.returncode} {r.stderr[-99:]!r}")

    def phong(k, lenh, gia=True):
        with contextlib.redirect_stderr(loi := io.StringIO()):
            try:
                rc = _phong_lai(lenh, dict(os.environ), nen="nt", k32=k if gia else None, popen=k.popen, execve=k.execve)
            except Exception as ex:  # noqa: BLE001 — sản phẩm NÉM thay vì chạy là KẾT QUẢ cho chốt đọc, không phải giàn giáo
                rc = ex
        return rc, loi.getvalue()

    k, kq = _k32_gia(), {}
    (th := threading.Thread(target=lambda: kq.update(zip("rl", phong(k, [sys.executable, "-c", "import time; time.sleep(60)"]))))).start()
    k.co.wait(15); k.cha_chet(); th.join(10)
    song = th.is_alive(); [p.kill() for p in k.con]; th.join(60)
    bang(not k.exec, f"(w0) nhánh Windows gọi exec — trên nt `os.exec*` phóng MỚI rồi thoát cha ⇒ MỒ CÔI: {k.exec}")
    bang(k.con and not song and not kq.get("l"), f"(w1) cha chết mà con còn sống: job={k.job} stderr={kq.get('l')!r}")
    for hong in ("CreateJobObjectW", "SetInformationJobObject", "AssignProcessToJobObject") + ("WinDLL",) * (os.name != "nt"):
        rc, loi = phong(k := _k32_gia(hong), [sys.executable, "-c", "raise SystemExit(7)"], gia=hong != "WinDLL")
        bang(rc == 7 and "CANH_BAO_MO_COI" in loi and len(k.con) == 1, f"(w2) Job hỏng ở {hong} (nt KHÔNG thử WinDLL: Job THẬT "
             f"sẽ gắn vào CHÍNH bộ test): phải VẪN chạy đúng một lần, mã 7 đi qua, và NÓI ra: rc={rc} {loi!r}")


def python_alias_behavior_test() -> None:
    """Probe `python` dùng interpreter chạy cong_cu.py, không đòi alias trên PATH."""
    with tempfile.TemporaryDirectory(prefix="cong-cu-python3-") as td:
        root = Path(td); only = root / "bin"; only.mkdir()
        try:
            (only / "python3").symlink_to(sys.executable)
        except OSError as ex:
            # Windows doi SeCreateSymbolicLinkPrivilege (Developer Mode hoac shell nang quyen).
            # Thieu no thi day la KHONG DO DUOC, KHONG phai DO — va nhat dinh khong phai ly do
            # de giet ca suite. ĐO ĐƯỢC 20-09-2026 tren may chu kho: cung ma nay chay TRON luc
            # 13:33 (`570-do-5`, 32/32) roi `WinError 1314` luc 18:07 (`570-do-7`) — ham GIONG
            # HET tung byte o ca hai lan, nen khac biet la TRANG THAI MAY, khong phai ma.
            # Vi sao doi trang thai: KHONG DO DUOC, va khong dung gia thuyet cho no.
            raise BoQuaMoiTruong(
                f"khong tao duoc symlink de dung cay chi-co-python3: {type(ex).__name__}: {ex}. "
                f"Tren Windows can Developer Mode hoac shell nang quyen. KHONG_DO_DUOC.") from ex
        bk = ghi_ban_ke(root, {"python": {"bat_buoc": True, "ban_ghim": None,
            "probe": [{"ten": "mac_dinh", "lenh": ["python", "--version"],
                       "regex": r"Python\s+(\d+\.\d+\.\d+)"}]}})
        rc, out, _ = chay("kiem-tra", "--ban-ke", str(bk), "--json",
                          env=dict(os.environ, PATH=str(only)))
        bang(rc == 0 and '"trang_thai_tong": "DAT"' in out,
             f"máy chỉ có python3 bị probe alias python chặn: rc={rc}\n{out}")



@ca
def t24_pham_vi_mot_cong_cu_va_toan_bo():
    """Phạm vi một công cụ và toàn bộ phải có đủ pham_vi, canary_da_quet, ghi_chu_pham_vi, không rỗng và đúng ngữ nghĩa."""
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        bk, env = bk_don(tmp, "cong-cu-t24", "#!/bin/sh\necho 1.0.0\n", ban_ghim="1.0.0")
        rc, out, _ = chay("kiem-tra", "--ban-ke", str(bk), "--json", env=env)
        bang(rc == 0, f"rc={rc} thay vi 0")
        bc = json.loads(out)
        bang(bc.get("pham_vi") == "toan-bo", f"sai pham_vi toan-bo: {bc.get('pham_vi')}")
        bang(bc.get("canary_da_quet") is True, "sai canary_da_quet toan-bo")
        ghi_chu_tb = bc.get("ghi_chu_pham_vi", "")
        bang(bool(ghi_chu_tb.strip()), "ghi_chu_pham_vi toan-bo bi rong")
        bang("da quet" in ghi_chu_tb.lower() or "đã quét" in ghi_chu_tb.lower(), "ghi_chu_pham_vi toan-bo khong mang y nghia da quet")
        rc, out, _ = chay("kiem-tra", "--chi", "cong-cu-t24", "--ban-ke", str(bk), "--json", env=env)
        bang(rc == 0, f"rc={rc} thay vi 0")
        bc = json.loads(out)
        bang(bc.get("pham_vi") == "mot-cong-cu", f"sai pham_vi mot-cong-cu: {bc.get('pham_vi')}")
        bang(bc.get("canary_da_quet") is False, "sai canary_da_quet mot-cong-cu")
        ghi_chu_1 = bc.get("ghi_chu_pham_vi", "")
        bang(bool(ghi_chu_1.strip()), "ghi_chu_pham_vi mot-cong-cu bi rong")
        bang("chua quet" in ghi_chu_1.lower() or "chưa quét" in ghi_chu_1.lower(), "ghi_chu_pham_vi mot-cong-cu khong mang y nghia chua quet")

@ca
def t25_optional_khong_do_duoc_giu_nguyen_trang_thai_tong():
    """Optional KHONG_DO_DUOC không kéo trạng thái tổng xuống KHONG_DO_DUOC."""
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        bk = ghi_ban_ke(tmp, {"optional-hong": {"bat_buoc": False, "ban_ghim": None, "probe": mot_probe("khong-ton-tai-bin")}})
        rc, out, _ = chay("kiem-tra", "--ban-ke", str(bk), "--json", env=moi_truong())
        bang(rc == 0, f"rc={rc} thay vi 0")
        bc = json.loads(out)
        bang(bc.get("trang_thai_tong") == "DAT", "optional KHONG_DO_DUOC keo trang thai tong")
        cc = bc["cong_cu"][0]
        bang(cc["trang_thai"] == "KHONG_DO_DUOC", "optional tool khong phai KHONG_DO_DUOC")


def _tu_kiem_phan_hang() -> int:
    """Ca tự kiểm CHO CHÍNH bộ phân hạng — bộ chấm cũng là mã, cũng sai được.

    `CLAUDE.md` ghi một ca đã trả giá: bản vá vòng một của một bộ phân hạng khác
    phân loại theo CHUỖI `AssertionError`, và thua vì trong bộ test có một
    `except Exception as e: raise AssertionError(...)` viết với ý định ĐÚNG —
    nó dựng lên đúng tín hiệu mà bộ phân hạng tin. Ca `d` dưới đây là phản chứng
    cho đúng cái bẫy ấy: nếu ai đó hạ `TinHieuChotCa` xuống `AssertionError`
    trần thì `d` phải ĐỎ.
    """
    import json as _json

    def a_chot_that():
        bang(False, "chốt của chính ca này")

    def b_parse_hong():
        _json.loads("")                      # JSONDecodeError — lỗi VÔ CAN

    def c_thieu_khoa():
        {}["chinh_sach"]                     # KeyError — đúng đường chết của R4-04

    def d_wrapper_doi_kieu():
        try:
            {}["chinh_sach"]
        except Exception as e:               # noqa: BLE001
            raise AssertionError(f"bọc lại: {type(e).__name__}")   # Ý ĐỊNH TỐT, VẪN LÀ TÍN DỤNG GIẢ

    def e_chot_cua_ca_khac():
        ex = TinHieuChotCa("chốt mang tên ca khác")
        ex.ca_nguon = "mot_ca_khac_hoan_toan"
        raise ex

    def f_gian_giao_khoi_chay_hong():
        # R5-01: tiến trình con của ca chết ⇒ chốt nghiệp vụ bên dưới CHƯA CHẠY.
        p = subprocess.run([sys.executable, "-c", "raise KeyError('rv5_unrelated_crash')"],
                           capture_output=True, text=True, timeout=60)
        dung(p.returncode == 0, f"giàn giáo chết: rc={p.returncode}")
        bang(False, "KHÔNG ĐƯỢC tới đây — nếu tới thì `dung()` đã mất răng")

    def g_chot_ma_thoat_van_la_giet_that():
        # ĐỐI CHỨNG NGƯỢC, và nó là cái đắt: reviewer cảnh báo thẳng rằng "hạ mọi rc
        # khác 0 thành tín dụng giả sẽ làm mất tín dụng hợp lệ của ca kiểm mã thoát".
        # `t7` `t9` `t11` `t20` sống bằng đúng những `rc` ấy. Ca này phải là `giet_that`.
        p = subprocess.run([sys.executable, "-c", "raise SystemExit(3)"],
                           capture_output=True, text=True, timeout=60)
        bang(p.returncode == 0, f"sản phẩm trả rc={p.returncode} — rc LÀ hợp đồng của nó")

    mong = {"a_chot_that": "giet_that", "b_parse_hong": "tin_dung_gia",
            "c_thieu_khoa": "tin_dung_gia", "d_wrapper_doi_kieu": "tin_dung_gia",
            "e_chot_cua_ca_khac": "tin_dung_gia",
            "f_gian_giao_khoi_chay_hong": "tin_dung_gia",
            "g_chot_ma_thoat_van_la_giet_that": "giet_that"}
    loi = 0
    print(f"\nTỰ KIỂM BỘ PHÂN HẠNG ({len(mong)} ca):")
    for fn in (a_chot_that, b_parse_hong, c_thieu_khoa, d_wrapper_doi_kieu, e_chot_cua_ca_khac,
               f_gian_giao_khoi_chay_hong, g_chot_ma_thoat_van_la_giet_that):
        tt, ct = _chay_1_ca(fn)
        if tt != mong[fn.__name__]:
            print(f"  ĐỎ  {fn.__name__}: mong {mong[fn.__name__]!r}, thực {tt!r} — {ct}")
            loi += 1
        else:
            print(f"  ok  {fn.__name__} → {tt}")
    return loi


def _tu_kiem_gian_giao() -> int:
    """Chạy LẠI đúng phản chứng của reviewer lượt 5 cho `R5-01`, trên bản sao tạm.

    Năm ca tự kiểm ở trên đều nằm TRONG CÙNG TIẾN TRÌNH — chính vì thế chúng bỏ sót
    đường này (reviewer nói thẳng như vậy). Phép đo dưới đây đi qua ranh giới tiến
    trình THẬT: bơm duy nhất `raise KeyError("rv5_unrelated_crash")` vào đầu
    `_bash_windows` của `ops/cong_cu.py`, rồi hỏi bộ phân hạng xem `t22` chết kiểu gì.

    TRƯỚC bản vá: `giet_that` (tín dụng giả — thuộc tính WSL chưa hề được đo).
    SAU bản vá:   `tin_dung_gia`.
    Gỡ `dung()` ở `t22` về `bang()` ⇒ phép đo này phải ĐỎ. Đó là RĂNG của bản vá."""
    ten = "rv5_gian_giao_crash"
    neo = "def _bash_windows(path=None, system_root=None, program_files=None, git=None):\n"
    thay = neo + '    raise KeyError("rv5_unrelated_crash")  # đột biến R5-01: crash VÔ CAN\n'
    ds = [f for f in CA if f.__name__.startswith("t22_")]
    print("\nTỰ KIỂM GIÀN GIÁO (phản chứng R5-01 qua ranh giới TIẾN TRÌNH):")
    if len(ds) != 1:
        print(f"  KHÔNG_ĐO_ĐƯỢC: tìm thấy {len(ds)} ca t22_*, đòi đúng 1 — ca đã đổi tên?")
        return 1
    t22 = ds[0]
    tt, ct = _chay_1_ca(t22)
    if tt == "bo_qua":
        print(f"  BỎ QUA control t22: {ct}")
        return 0
    if tt != "qua":
        print(f"  KHÔNG_ĐO_ĐƯỢC: control t22 → {tt!r} ({ct}) — mong 'qua'; đột biến bên dưới vô nghĩa")
        return 1
    print("  ok  control t22 → qua")
    cay, dich = _dung_cay_dot_bien(ten, "ops/cong_cu.py", neo, thay, _PHU)
    g, cu = globals(), globals()["SCRIPT"]
    g["SCRIPT"] = dich
    try:
        tt, ct = _chay_1_ca(t22)
    finally:
        g["SCRIPT"] = cu
        shutil.rmtree(cay, ignore_errors=True)
    if tt != "tin_dung_gia":
        print(f"  ĐỎ  crash VÔ CAN trong `_bash_windows` được phân hạng {tt!r} — {str(ct)[:200]}\n"
              f"      Đây là R5-01: mutant chết TRƯỚC khi ca kịp đo thuộc tính của nó mà vẫn "
              f"được cấp tín dụng giết.")
        return 1
    print(f"  ok  crash vô can → tin_dung_gia ({str(ct).splitlines()[0][:90]})")
    return 0


# --------------------------------------------------------- T23..T27 (#570) bash_nen
# Issue #570, đo 19-09-2026 trên Windows thật: `shutil.which("bash")` trả
# `C:\Windows\system32\bash.EXE` — bộ phóng WSL — nên `t35`-`t40` của
# `ops/lease_publish_test.py` chết TRƯỚC dòng đầu của `ops/cai_actionlint.sh` với
# `rc=127`, và sáu lời khai của chúng là QUY SAI NGUYÊN NHÂN.
#
# Đó là lần thứ BA cùng khuyết tật (`t32` · `_bash_windows` · nay sáu ca kia), và lần
# thứ ba nó được chữa bằng một bộ giải RIÊNG. `ops/bash_nen.py` là bộ giải DÙNG CHUNG
# cộng một CỔNG chặn bản sao thứ tư. Năm ca dưới đây neo năm thuộc tính khác nhau của
# nó; mỗi ca có ĐÚNG MỘT đột biến trong `DOT_BIEN`.

_BASH_NEN_GIA_DUNG = '''import sys
a = sys.argv[1:]
if a and a[0] == "-c":
    nhan, con = a[2], a[3:]
    print("BN0=%s" % nhan); print("BNSO=%s" % len(con))
    print("BN1=%s" % (con[0] if con else ""))
    print("BNBASH=1")
    raise SystemExit(0)
try:
    t = open(a[0], encoding="utf-8").read()
except OSError:
    print("/bin/bash: %s: No such file or directory" % a[0], file=sys.stderr)
    raise SystemExit(127)
for d in t.splitlines():
    if "BN_DA_CHAY_TU_TEP" in d and not d.startswith("#"):
        print("BN_DA_CHAY_TU_TEP")
raise SystemExit(0)
'''

_BN_IN_GOC = ('    print("BN0=%s" % nhan); print("BNSO=%s" % len(con))\n'
              '    print("BN1=%s" % (con[0] if con else ""))\n')


def _bn_gia_doi_in(moi: str) -> str:
    return _BASH_NEN_GIA_DUNG.replace(_BN_IN_GOC, moi)


# BA con giả, mỗi con hỏng ĐÚNG MỘT chốt con của phép argv. Vì sao cần cả ba: đột biến
# đầu tiên viết cho ca này chỉ gỡ phép đếm `$#` và nó SỐNG SÓT — hai chốt kia vẫn bắt
# được con giả mang trọn chữ ký WSL. Tức "phép argv" không phải MỘT cửa mà là BA, và
# `CLAUDE.md` đã ghi đúng hình dạng ấy: vá/đo theo cửa được gọi tên rồi bỏ sót cửa kế
# tiếp. Mỗi cửa nay có một đột biến riêng; gỡ cửa nào thì ca này ĐỎ vì con giả của cửa ấy.
_BASH_NEN_GIA_SAI_ARGV0 = _bn_gia_doi_in(
    '    print("BN0=/bin/bash"); print("BNSO=%s" % len(con))\n'
    '    print("BN1=%s" % (con[0] if con else ""))\n')
_BASH_NEN_GIA_SAI_SO = _bn_gia_doi_in(
    '    print("BN0=%s" % nhan); print("BNSO=0")\n'
    '    print("BN1=%s" % (con[0] if con else ""))\n')
_BASH_NEN_GIA_SAI_DOI_SO_1 = _bn_gia_doi_in(
    '    print("BN0=%s" % nhan); print("BNSO=%s" % len(con))\n'
    '    print("BN1=lac-de")\n')

# Chữ ký ĐO ĐƯỢC của bộ phóng WSL (#570 lượt 2): `-c <thân> <nhãn> A B C` cho
# `$0=/bin/bash`, `$#=0`, `$1` rỗng — đối số bị nối vào THÂN SCRIPT thay vì truyền làm
# tham số. Nhưng nó VẪN mở được tệp, nên chỉ phép (1) bắt được nó.
_BASH_NEN_GIA_NUOT_ARGV = _BASH_NEN_GIA_DUNG.replace(
    '    print("BN0=%s" % nhan); print("BNSO=%s" % len(con))\n'
    '    print("BN1=%s" % (con[0] if con else ""))\n',
    '    print("BN0=/bin/bash"); print("BNSO=0"); print("BN1=")\n')

# Mặt kia của cùng bộ phóng ấy: argv đúng nhưng KHÔNG mở nổi đường dẫn bản địa
# (`rc=127 No such file or directory`). Chỉ phép (2) bắt được. Hai đột biến riêng ở dưới
# chứng minh hai phép KHÔNG suy ra nhau — gỡ phép nào thì ca của phép ấy ĐỎ.
_BASH_NEN_GIA_KHONG_MO_TEP = _BASH_NEN_GIA_DUNG.replace(
    'try:\n    t = open(a[0], encoding="utf-8").read()\nexcept OSError:\n',
    'if True:\n')


# Mat hong THU BA cua cung bo phong WSL, do duoc o `570-do-3` (20-09-2026, Windows that):
# no KHONG tra `rc=127` ma TREO — `subprocess.run([bash, "./cai_cong_cu.sh", "--bat-buoc"])`
# het han 60s, roi `TemporaryDirectory` chet tiep bang `WinError 32`, va ca suite nay chet
# trong `batch_behavior_test()` TRUOC vong lap ca. Han cua `_do_nang_luc` la thu DUY NHAT
# chan mat ay, va truoc r2 no dung do MAY — khong ca nao canh.
# N122 (r36, codex vòng 30) — một shell POSIX (sh/dash) TRUYỀN ĐÚNG argv và MỞ ĐƯỢC tệp, chỉ thiếu tính năng Bash.
_BASH_NEN_GIA_POSIX = _BASH_NEN_GIA_DUNG.replace('    print("BNBASH=1")\n', '')

_BASH_NEN_GIA_TREO = '''import time
time.sleep(600)
'''


def _goi_do_nang_luc(gia_than: str, tmp: Path, han=None):
    """Chạy `_do_nang_luc` của `BASH_NEN` (có thể ĐÃ ĐỘT BIẾN) trên một `bash` giả.

    Ứng viên giả là `[python, gia.py]` chứ không phải một tệp thực thi: Windows không
    tạo được `.exe` giả, mà ca này phải đo được trên CHÍNH nền sinh ra khuyết tật.
    """
    gia = tmp / f"bash_gia_{abs(hash(gia_than)) % 10 ** 8}.py"
    gia.write_text(gia_than, encoding="utf-8")
    ma = ("import runpy, json, sys\n"
          f"m = runpy.run_path({str(BASH_NEN)!r})\n"
          f"dat, ly_do = m['_do_nang_luc']([{sys.executable!r}, {str(gia)!r}], han={han!r})\n"
          "print('KQ ' + json.dumps([dat, ly_do]))\n")
    p = subprocess.run([sys.executable, "-c", ma], cwd=GOC, capture_output=True,
                       text=True, timeout=120)
    # GIÀN GIÁO: đoạn `python -c` do CHÍNH ca này soạn. Nó chết ⇒ chưa đo được gì.
    dung(p.returncode == 0 and "KQ " in p.stdout,
         f"gọi _do_nang_luc hỏng: rc={p.returncode}\n{p.stdout}\n{p.stderr}")
    dong = [l for l in p.stdout.splitlines() if l.startswith("KQ ")][-1]
    return json.loads(dong[3:])


@ca
def t23_bash_nen_tu_choi_bash_nuot_argv():
    """Phép NĂNG LỰC phải TỪ CHỐI một `bash` không truyền đúng đối số vị trí.

    Đây là chữ ký đo được của `C:\\Windows\\system32\\bash.EXE` ở #570 lượt 2, và là thứ
    KHÔNG lọc theo tên nào diễn tả nổi — nên ca này đo HÀNH VI, không đo đường dẫn.
    Có CA DƯƠNG: một `bash` giả trung thực phải được NHẬN, nếu không thì "luôn từ chối"
    cũng qua hết ca âm.
    """
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        dat_dung, ly_do_dung = _goi_do_nang_luc(_BASH_NEN_GIA_DUNG, tmp)
        bang(dat_dung, f"bash giả TRUNG THỰC mà bị từ chối: {ly_do_dung!r} — "
                       f"mọi ca âm bên dưới sẽ vô nghĩa")
        for ten, than in (("chữ ký WSL đầy đủ", _BASH_NEN_GIA_NUOT_ARGV),
                          ("chỉ sai `$0`", _BASH_NEN_GIA_SAI_ARGV0),
                          ("chỉ sai `$#`", _BASH_NEN_GIA_SAI_SO),
                          ("chỉ sai `$1`", _BASH_NEN_GIA_SAI_DOI_SO_1)):
            dat_xau, ly_do_xau = _goi_do_nang_luc(than, tmp)
            bang(not dat_xau,
                 f"bash giả ({ten}) mà vẫn được NHẬN — đúng bộ phóng WSL đã làm "
                 f"`t35`-`t40` đỏ ở #570")
            bang("argv" in (ly_do_xau or ""),
                 f"từ chối ĐÚNG ({ten}) nhưng LÝ DO không nêu phép argv: "
                 f"{ly_do_xau!r} — mã thoát đúng mà lý do sai thì người gọi khẳng "
                 f"định nhầm chuyện")
        # N122 (r36) — shell POSIX truyền đúng argv, mở được tệp, chỉ THIẾU tính năng Bash: phải bị từ chối,
        # và lý do phải nêu đúng phép. Kèm `/bin/dash` THẬT khi máy có.
        dat_p, ly_do_p = _goi_do_nang_luc(_BASH_NEN_GIA_POSIX, tmp)
        bang(not dat_p and "Bash" in (ly_do_p or ""),
             f"shell POSIX (thiếu pipefail/mảng) mà được NHẬN, hay lý do sai: {dat_p!r} {ly_do_p!r}")
        if Path("/bin/dash").exists():
            m23 = runpy.run_path(str(BASH_NEN))
            dat_d, ly_do_d = m23["_do_nang_luc"](["/bin/dash"])
            bang(not dat_d and "Bash" in (ly_do_d or ""),
                 f"`/bin/dash` THẬT mà được NHẬN làm bash, hay bị từ chối với lý do sai: {ly_do_d!r}")


@ca
def t24_bash_nen_tu_choi_bash_khong_mo_duoc_duong_dan_ban_dia():
    """Phép NĂNG LỰC phải TỪ CHỐI một `bash` không mở nổi đường dẫn bản địa.

    Mặt thứ hai của cùng bộ phóng WSL: `bash D:\\...\\x.sh` ⇒ `rc=127 No such file or
    directory`. Ứng viên giả ở đây TRUYỀN ĐÚNG argv, nên chỉ phép (2) bắt được nó —
    đó là bằng chứng hai phép không suy ra nhau.
    """
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        dat_dung, ly_do_dung = _goi_do_nang_luc(_BASH_NEN_GIA_DUNG, tmp)
        bang(dat_dung, f"bash giả TRUNG THỰC mà bị từ chối: {ly_do_dung!r}")
        dat_xau, ly_do_xau = _goi_do_nang_luc(_BASH_NEN_GIA_KHONG_MO_TEP, tmp)
        bang(not dat_xau,
             "bash giả KHÔNG mở được đường dẫn bản địa mà vẫn được NHẬN — đúng cách "
             "`t35`-`t40` nhận `rc=127` ở #570")
        bang("đường dẫn bản địa" in (ly_do_xau or ""),
             f"từ chối ĐÚNG nhưng LÝ DO không nêu phép mở đường dẫn: {ly_do_xau!r}")


@ca
def t28_bash_nen_tu_choi_bash_TREO_trong_han():
    '''Phep NANG LUC phai TU CHOI mot `bash` KHONG BAO GIO TRA — trong han, khong treo theo.

    Day la mat hong THU BA cua bo phong WSL va la mat DAT nhat: no khong tra `rc=127` ma
    TREO, nen no khong lam mot ca do — no giet CA SUITE truoc khi ca nao kip chay. Do duoc
    o `570-do-3`: `ops/cong_cu_test.py` chet trong `batch_behavior_test()` dung nhu the, va
    vi the `T23`-`T27` chua tung chay tren Windows du chung sinh ra de do Windows.

    Han truyen vao ngan de suite chay nhanh; con so SAN PHAM la `_HAN_GIAY`, va ca nay doi
    no la mot so duong huu han — mot han bi go thi khong phai "cham hon", ma la mat chot.
    '''
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        dat, ly_do = _goi_do_nang_luc(_BASH_NEN_GIA_TREO, tmp, han=3)
        bang(not dat, "bash gia TREO ma van duoc NHAN — han khong chan duoc mat treo")
        bang("rc=-998" in (ly_do or "") or "qua han" in (ly_do or "") or "quá hạn" in (ly_do or ""),
             f"tu choi DUNG nhung LY DO khong neu QUA HAN: {ly_do!r} — doc nham mat treo "
             f"thanh mot loi khac thi lan sau khong ai tim dung cho")
        ma = ("import runpy\n"
              f"m = runpy.run_path({str(BASH_NEN)!r})\n"
              "print('HAN', m['_HAN_GIAY'])\n")
        p = subprocess.run([sys.executable, "-c", ma], cwd=GOC, capture_output=True,
                           text=True, timeout=60)
        dung(p.returncode == 0 and "HAN " in p.stdout,
             f"khong doc duoc `_HAN_GIAY`: rc={p.returncode} {p.stderr}")
        han = float(p.stdout.split("HAN ")[-1].strip())
        bang(0 < han < 3600,
             f"`_HAN_GIAY` = {han!r} — han san pham phai la so duong huu han; go no ra la "
             f"mat chot DUY NHAT chan mat treo, khong phai 'chay cham hon'")


@ca
def t29_ban_kinh_qua_RONG_phai_neu_LY_DO_tung_ca_oan():
    """Phán quyết bán kính phải in LÝ DO của từng ca oan, không chỉ TÊN.

    Ca này sinh ra từ một phép đo, không từ lo xa. Nghiệm thu Windows 20-09-2026 (bộ đo
    `570-do-3`, HEAD 42dd49db) cho `t22_bash_lay_ca_system_root` bán kính **9/31** trong
    khi Linux cho **1/31**. Bản cũ in đúng một dòng — danh sách 8 TÊN — rồi khẳng định
    "⇒ trói nhầm thứ". Cầm dòng ấy trong tay vẫn KHÔNG trả lời được câu hỏi quyết định
    cách chữa: 8 ca ấy chết vì ca đích trói nhầm thuộc tính, hay vì đột biến nằm trên
    ĐƯỜNG CHUNG mà giàn giáo phóng mọi công cụ giả đi qua? Không in lý do thì lượt
    Windows sau cũng chỉ đọc được đúng chừng ấy — một phép đo KHÔNG SỐNG SÓT qua chính
    cái nó định chẩn đoán.

    LƯỢT 5 CHO THẤY BẢN VÁ ĐẦU CỦA CHÍNH CA NÀY LÀ HẸP, và đó là lý do ca có hình dạng hôm
    nay. Bản sáng 20-09 chỉ gắn lý do vào nhánh `oan` — đúng nhánh log lượt 3 chỉ ra. Lượt 5
    rơi vào nhánh ANH EM (`gia`, ca oan chết bằng lỗi vô can) và lại không đọc được gì:
    `t22_bash_lay_ca_system_root` in ra `t2_canary_thieu_shellcheck_phai_SUY_GIAM` "chết bằng
    lỗi VÔ CAN" mà không nói lỗi ấy là gì. `CLAUDE.md` gọi đúng tên: *"vá đúng chỗ được chỉ
    rồi bỏ sót đường thứ ba"* — bản vá ĐÚNG mà HẸP. Nên nay lý do thuộc MỌI nhánh ĐỎ.

    Hai nhánh, mỗi nhánh có đột biến RIÊNG nên phân biệt được bằng ĐẦU VÀO (không phải một
    bộ tương đương đội lốt hai chốt):
      (1) nhánh `oan` — `bn_ban_kinh_giau_ly_do` xoá khối chi tiết;
      (2) nhánh `gia` — `bn_ban_kinh_gia_ve_som` cho nhánh ấy về SỚM, bỏ qua khối chi tiết.
    Mỗi nhánh đòi ba thứ: vẫn ĐỎ (không nới cổng) · nêu TÊN ca oan · nêu LÝ DO nó chết.
    Kèm đối chứng âm: bán kính đúng 1 thì XANH, để các chốt trên không phải thứ luôn đỏ."""
    p = subprocess.run([sys.executable, str(TEP_TEST), "--tu-kiem-ban-kinh"],
                       cwd=GOC, capture_output=True, text=True, timeout=120)
    dung(p.returncode == 0 and "LOI=" in p.stdout,
         f"không chạy được cửa tự kiểm: rc={p.returncode}\n{p.stdout}\n{p.stderr}")
    khuc = p.stdout.split("LOI=")
    dung(len(khuc) == 4, f"cửa tự kiểm phải in ĐÚNG ba kịch bản, đọc được {len(khuc)-1}:\n{p.stdout}")
    kh_rong, kh_vo_can, kh_hep = khuc[1], khuc[2], khuc[3]

    # (1) nhánh `oan` — bán kính rộng, mọi ca chết bằng chốt của chính nó
    bang(kh_rong.startswith("1"),
         f"bán kính 2/3 mà KHÔNG tính lỗi ⇒ cổng đã bị nới:\n{p.stdout}")
    bang("ca_oan_gia" in kh_rong, f"nhánh `oan` không nêu TÊN ca oan:\n{p.stdout}")
    bang("giàn giáo phóng công cụ giả hỏng: rc=1" in kh_rong,
         "nhánh `oan` nêu tên ca oan nhưng KHÔNG nêu LÝ DO nó chết — đúng khuyết tật mà "
         f"nghiệm thu Windows lượt 3 phơi ra:\n{p.stdout}")
    bang("trói nhầm thứ" not in kh_rong,
         "báo cáo vẫn KHẲNG ĐỊNH nguyên nhân là 'trói nhầm thứ' trong khi nó mới chỉ "
         f"ĐẾM — lời khai rộng hơn phép đo:\n{p.stdout}")

    # (2) nhánh `gia` — ca oan chết bằng lỗi VÔ CAN. Đây là nhánh mà bản vá sáng 20-09 BỎ SÓT,
    #     và nghiệm thu Windows lượt 5 rơi đúng vào nó: in tên ca mà không nói lỗi là gì.
    bang(kh_vo_can.startswith("1"),
         f"nhánh `gia` KHÔNG tính lỗi ⇒ cổng đã bị nới:\n{p.stdout}")
    bang("ca_oan_vo_can" in kh_vo_can, f"nhánh `gia` không nêu TÊN ca oan:\n{p.stdout}")
    bang("gọi _bash_windows hỏng: rc=1" in kh_vo_can,
         "nhánh `gia` nêu tên ca chết bằng lỗi VÔ CAN nhưng KHÔNG nêu lỗi ấy là gì. Đúng "
         "hình dạng 'vá đúng chỗ được chỉ rồi bỏ sót đường thứ ba': lý do phải thuộc MỌI "
         f"nhánh ĐỎ, không phải đặc quyền của nhánh `oan`:\n{p.stdout}")

    # (3) đối chứng âm — bán kính đúng 1 thì XANH, để (1) và (2) không phải thứ luôn đỏ
    bang(kh_hep.startswith("0"),
         f"bán kính đúng 1 mà vẫn báo lỗi ⇒ các chốt trên luôn đỏ, tức không đo gì:\n{p.stdout}")


def _quet(goc, bo_quet=None, env=None) -> tuple:
    """`bo_quet` cho phép chạy MỘT BẢN SAO của `bash_nen.py` thay vì bản thật — xem
    `_bash_nen_co_chua_chuyen`. Mặc định vẫn là bản thật, nên mọi ca cũ không đổi nghĩa.
    `env` tiêm môi trường cho tiến trình con — `t41` dùng nó để giả một cấu hình git TOÀN CỤC
    mà không đụng `~/.gitconfig` thật của máy."""
    p = subprocess.run([sys.executable, str(bo_quet or BASH_NEN), "quet", "--root", str(goc),
                        "--json"], cwd=GOC, capture_output=True, text=True, timeout=120, env=env)
    dung(p.stdout.strip().startswith("{"),
         f"`quet --json` không in JSON: rc={p.returncode}\n{p.stdout}\n{p.stderr}")
    return p.returncode, json.loads(p.stdout)


_RATCHET_GIA = "ops/muc_ratchet_gia_t26.py"


def _thay_bang_trong_nguon(than: str, ten: str, gia_tri: dict) -> str:
    """Thay ĐỊNH NGHĨA bảng `ten = {...}` trong mã nguồn bằng `gia_tri`. Neo theo TÊN BIẾN, không
    theo hình dạng nguồn — bảng nhiều dòng kết bằng `\n}\n`, bảng một dòng kết ở cuối dòng."""
    dau = f"{ten} = {{"
    i = than.index(dau)
    j = than.index("\n}\n", i) + len("\n}\n") if than[i:].startswith(dau + "\n") \
        else than.index("\n", i) + 1
    return than[:i] + f"{ten} = {gia_tri!r}\n" + than[j:]


def _bash_nen_voi_chua_chuyen(tmp: Path, muc: dict, ten="bash_nen_tuy_bien.py",
                              anh_chup=None) -> Path:
    """Bản sao `bash_nen.py` với `CHUA_CHUYEN` đặt theo `muc` và `ANH_CHUP_DONG_CUNG` đặt theo
    `anh_chup` (mặc định RỖNG). Trả đường dẫn bản ấy.

    Vì sao cần: các ca dựng cây GIẢ không thể thoả một danh sách khoá theo đường dẫn THẬT của
    kho — chiều ngược của ratchet sẽ báo "mục đã sạch" và làm nền ĐỎ oan. Ca phải đo LUẬT của
    cổng, không đo danh sách hiện thời. `ANH_CHUP_DONG_CUNG` vào đây từ r8: hạn ngạch nay so đủ
    hai vế kể cả về 0 (F1), nên một ảnh chụp VẮNG trên cây giả là "khai 7, đo 0" và ĐỎ — đúng
    trên kho thật, oan trên cây giả. `CHO_PHEP` giữ nguyên: hạn ngạch 0, vắng là ĐÚNG.
    """
    than = Path(BASH_NEN).read_text(encoding="utf-8")
    than = _thay_bang_trong_nguon(than, "CHUA_CHUYEN", muc)
    than = _thay_bang_trong_nguon(than, "ANH_CHUP_DONG_CUNG", anh_chup or {})
    ban = tmp / ten
    ban.write_text(than, encoding="utf-8")
    return ban


def _bash_nen_co_chua_chuyen(tmp: Path) -> Path:
    """Bản sao `bash_nen.py` có `CHUA_CHUYEN` chứa ĐÚNG MỘT mục GIẢ.

    Từ r4 nó uỷ quyền cho `_bash_nen_voi_chua_chuyen`: mỏ neo cũ (`CHUA_CHUYEN = {}`) biến
    mất khi r4 nạp bốn mục thật vào danh sách, và một helper neo theo HÌNH DẠNG NGUỒN sẽ gãy
    mỗi lần danh sách đổi. Neo theo TÊN BIẾN thì không.
    """
    # `(1, …)` chứ không còn là CHUỖI: từ r8 một mục không khai hạn ngạch số làm cổng
    # KHÔNG_ĐO_ĐƯỢC (vé vô hạn — xem `_so_cho_phep`), và `_cay_quet` viết đúng MỘT lời gọi.
    return _bash_nen_voi_chua_chuyen(tmp, {_RATCHET_GIA: (1, "mục giả của t26")},
                                     ten="bash_nen_co_muc.py")


def _cay_quet(tmp: Path, them=None, bo_loi_goi_o=None, bo_quet=None):
    """Cây giả để quét: đủ các tệp `CHUA_CHUYEN` mà BỘ QUÉT ĐANG DÙNG khai.

    Đọc danh sách TỪ MODULE chứ không chép cứng — ratchet sinh ra để NGẮN đi, và một
    ca chép cứng danh sách sẽ đỏ oan đúng lúc ai đó vá xong một mục.
    """
    (tmp / "ops").mkdir(parents=True, exist_ok=True)
    _, bao = _quet(tmp, bo_quet)   # lượt này chỉ để đọc `chua_chuyen` của module
    dung(isinstance(bao.get("chua_chuyen"), list) and bao["chua_chuyen"],
         f"không đọc được `chua_chuyen` từ module: {bao}")
    for rel in bao["chua_chuyen"]:
        p = tmp / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        than = "import shutil\n"
        than += "X = 1\n" if rel == bo_loi_goi_o else 'b = shutil.which("bash")\n'
        p.write_text(than, encoding="utf-8")
    for ten, than in (them or {}).items():
        p = tmp / "ops" / ten
        p.write_text(than, encoding="utf-8")
    return bao["chua_chuyen"]


@ca
def t25_cong_chan_loi_goi_bash_tran_MOI():
    """Cổng phải ĐỎ khi có lời gọi `bash` trần ở một tệp ngoài danh sách cho phép.

    Không có ca này thì `ops/bash_nen.py` chỉ là bộ giải thứ BA nằm cạnh hai bộ cũ, và
    bản sao thứ tư sẽ lặng lẽ ra đời — đúng thứ chủ kho quyết phải chặn ở #570.
    """
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        # Cây `ops/` RỖNG là nền đúng cho ca này. Bản cũ gọi `_cay_quet`, tức dựng sẵn các tệp
        # `CHUA_CHUYEN` mà kho đang khai — từ r3 danh sách ấy RỖNG nên lời gọi ấy chỉ còn là
        # một phụ thuộc vào trạng thái nhất thời của kho, không thêm gì cho điều ca này đo.
        #
        # GỐC QUÉT là `cay`, KHÔNG phải `tmp`: từ r4 cổng quét TOÀN CÂY, nên bản sao bộ quét
        # đặt trong gốc quét sẽ bị chính nó quét. Dưới mã thật vô hại (`ast` không thấy lời
        # gọi nào), nhưng nó khiến MỌI đột biến của bộ quét chạm vào ca này qua đường giàn
        # giáo chứ không qua chốt — `bn_quet_theo_chuoi` giết oan t25 và t35 đúng vì thế.
        cay = tmp / "cay"
        (cay / "ops").mkdir(parents=True, exist_ok=True)
        # `CHUA_CHUYEN` RỖNG cho cây giả: danh sách thật khoá theo đường dẫn THẬT của kho,
        # nên trên cây này mọi mục đều "đã sạch" và chiều ngược của ratchet làm nền ĐỎ oan.
        bq = _bash_nen_voi_chua_chuyen(tmp, {})
        rc, bao = _quet(cay, bq)
        bang(rc == 0 and bao["trang_thai"] == "DAT",
             f"NỀN đã phải SẠCH mà cổng báo {bao.get('trang_thai')} rc={rc}: "
             f"{bao.get('ly_do')} — ca âm bên dưới sẽ vô nghĩa")
        (cay / "ops" / "tep_moi.py").write_text(
            'import shutil\nb = shutil.which("bash")\n', encoding="utf-8")
        rc, bao = _quet(cay, bq)
        bang(rc == 2 and bao["trang_thai"] == "DO",
             f"thêm lời gọi trần MỚI mà cổng vẫn rc={rc} {bao.get('trang_thai')}")
        bang("ops/tep_moi.py" in json.dumps(bao.get("ngoai_danh_sach"), ensure_ascii=False),
             f"cổng ĐỎ nhưng không nêu ĐÚNG tệp vi phạm: {bao.get('ngoai_danh_sach')}")


@ca
def t26_ratchet_phai_NGAN_di_chu_khong_muc_ra():
    """Cổng phải ĐỎ khi một mục `CHUA_CHUYEN` KHÔNG còn lời gọi trần nào.

    Chiều ngược của ratchet. Thiếu nó thì danh sách thành nghĩa trang: ai vá xong cũng
    quên xoá tên mình, cổng dần hết ý nghĩa mà vẫn xanh — đúng hình dạng "cổng vắng mặt
    trông giống cổng xanh" mà kho đã ghi sổ.
    """
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        # Danh sách RIÊNG của ca, không phải `CHUA_CHUYEN` hiện thời của kho — từ r3 nó RỖNG,
        # và một ca chỉ ĐỎ được khi kho còn bẩn thì tắt đúng lúc ratchet thành công.
        bq = _bash_nen_co_chua_chuyen(tmp)
        cay = Path(tempfile.mkdtemp(dir=tmp))
        ds = _cay_quet(cay, bo_quet=bq)
        bang(ds == [_RATCHET_GIA], f"bản sao không mang đúng mục giả: {ds}")
        rc, _ = _quet(cay, bq)
        bang(rc == 0, f"NỀN đã phải SẠCH mà rc={rc}")
        cay2 = Path(tempfile.mkdtemp(dir=tmp))
        _cay_quet(cay2, bo_loi_goi_o=ds[0], bo_quet=bq)
        rc, bao = _quet(cay2, bq)
        bang(rc == 2 and bao["trang_thai"] == "DO",
             f"mục ratchet {ds[0]!r} đã sạch mà cổng vẫn rc={rc} {bao.get('trang_thai')}")
        bang(ds[0] in bao.get("muc_ratchet_da_sach", []),
             f"cổng ĐỎ nhưng không nêu đúng mục đã sạch: {bao.get('muc_ratchet_da_sach')}")


@ca
def t27_cong_khong_bao_dong_gia_tren_CHU_THICH():
    """Cổng KHÔNG được ĐỎ vì một tệp chỉ NHẮC TỚI lời gọi trần trong chú thích/docstring.

    Bản đầu của cổng khớp regex trên văn bản thô và đếm luôn hai lần nhắc trong chính
    docstring của `ops/bash_nen.py`. `t43` của kho đã ĐỎ oan y hệt vì một câu văn xuôi
    có nhắc cụm marker, và `CLAUDE.md` chép lại: một cổng báo động giả là cổng sẽ bị
    tắt, rồi cả ca chết theo. Nên cổng đo CẤU TRÚC bằng `ast`, không đo chuỗi.
    """
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        cay = tmp / "cay"                         # gốc quét ≠ chỗ để bản sao — xem `t25`
        (cay / "ops").mkdir(parents=True, exist_ok=True)
        bq = _bash_nen_voi_chua_chuyen(tmp, {})   # xem chú thích ở `t25`
        (cay / "ops" / "chi_nhac.py").write_text(
            '"""Tài liệu có nhắc shutil.which("bash") để giải thích."""\n'
            '# và shutil.which("bash") trong một chú thích\n'
            'GHI_CHU = \'shutil.which("bash")\'\n', encoding="utf-8")
        rc, bao = _quet(cay, bq)
        bang(not (bao.get("co_loi_goi_tran") or {}),
             f"tệp chỉ NHẮC TỚI trong chú thích/chuỗi mà cổng ĐỎ: rc={rc} "
             f"{bao.get('ly_do')} — báo động giả")


@ca
def t30_cay_tam_mang_cong_cu_phai_mang_ca_BO_GIAI():
    """Một cây chỉ có `cong_cu.py` mà thiếu `bash_nen.py` phải hỏng CÓ LÝ DO, không âm thầm.

    CA NÀY SINH TỪ MỘT PHÉP ĐO, và phép đo ấy phải chạy trên Windows mới thấy. Bộ đo
    `570-do-6` (20-09-2026, máy chủ kho, HEAD 785ef33): `_chay_batch` chép `cong_cu.py` sang
    cây tạm mà KHÔNG chép `bash_nen.py`; nhánh dự phòng của `_chay` nổ `ModuleNotFoundError`
    và giết cả suite TRƯỚC vòng lặp ca — đúng khuyết tật N12 vừa chữa xong, tái sinh bởi N14.

    VÌ SAO LINUX MÙ: nhánh ấy nằm trong `except OSError`, mà trên Linux `subprocess.run` chạy
    được script shebang nên nó KHÔNG BAO GIỜ tới. Cả suite Linux xanh 31/31 trong khi mã đang
    hỏng trên nền mà packet này sinh ra để phục vụ.

    Ba chốt:
      (1) `KEM_THEO_CONG_CU` khác rỗng — nếu ai làm nó rỗng thì hai cây tạm lại thiếu;
      (2) cây ĐỦ: `_bash_windows` chạy được, trả chuỗi hoặc None, KHÔNG ném;
      (3) cây THIẾU: ném `RuntimeError` NÊU TÊN `bash_nen`, chứ không phải `ModuleNotFoundError`
          trần. Fail-close có lý do — `None ≠ False`, và một cây hỏng khác một máy không có bash.
    """
    bang(bool(KEM_THEO_CONG_CU),
         "`KEM_THEO_CONG_CU` RỖNG ⇒ mọi cây tạm mang `cong_cu.py` sẽ lại thiếu bộ giải; "
         "đó đúng là cách khuyết tật `570-do-6` quay lại")
    ma = ("import runpy, sys, json\n"
          "m = runpy.run_path(sys.argv[1])\n"
          "try:\n"
          "    r = m['_bash_windows']()\n"
          "    print('KQ ' + json.dumps(['ok', r]))\n"
          "except RuntimeError as ex:\n"
          "    print('KQ ' + json.dumps(['RuntimeError', str(ex)]))\n"
          "except Exception as ex:\n"
          "    print('KQ ' + json.dumps([type(ex).__name__, str(ex)]))\n")

    def hoi(ops_dir: Path):
        p = subprocess.run([sys.executable, "-c", ma, str(ops_dir / "cong_cu.py")],
                           cwd=GOC, capture_output=True, text=True, timeout=180)
        dung(p.returncode == 0 and "KQ " in p.stdout,
             f"giàn giáo hỏng khi hỏi cây {ops_dir}: rc={p.returncode}\n{p.stdout}\n{p.stderr}")
        return json.loads([l for l in p.stdout.splitlines() if l.startswith("KQ ")][-1][3:])

    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        du = tmp / "du" / "ops"; du.mkdir(parents=True)
        shutil.copy2(SCRIPT, du / "cong_cu.py")
        for rel in KEM_THEO_CONG_CU:
            shutil.copy2(_GOC_THAT / rel, du / Path(rel).name)   # xem chu thich o `_chay_batch`
        thieu = tmp / "thieu" / "ops"; thieu.mkdir(parents=True)
        shutil.copy2(SCRIPT, thieu / "cong_cu.py")

        kieu, chi_tiet = hoi(du)
        bang(kieu == "ok",
             f"cây ĐỦ phụ thuộc mà `_bash_windows` vẫn hỏng: {kieu}: {chi_tiet}")

        kieu, chi_tiet = hoi(thieu)
        bang(kieu == "RuntimeError",
             f"cây THIẾU `bash_nen.py` phải hỏng bằng RuntimeError CÓ LÝ DO, nhận được "
             f"{kieu}: {chi_tiet} — một `ModuleNotFoundError` trần đẩy người đọc đi truy "
             f"nhầm chỗ, đúng thứ `570-do-6` bắt được")
        bang("bash_nen" in chi_tiet,
             f"RuntimeError không nêu tên tệp thiếu: {chi_tiet!r}")


@ca
def t31_tien_kiem_KHONG_DO_DUOC_khong_duoc_giet_ca_suite():
    """Tiền kiểm thiếu MÔI TRƯỜNG thì bỏ qua có ghi nhận; hỏng NGHIỆP VỤ thì vẫn giết.

    BA LẦN suite này báo cáo ĐÚNG BẰNG KHÔNG trên Windows, và cả ba đều vì một tiền kiểm
    chết TRƯỚC vòng lặp ca — không lần nào vì một ca đo được điều gì:
      · `570-do-3` — `batch_behavior_test`, WSL bash làm `./cai_cong_cu.sh` treo 60s;
      · `570-do-6` — `batch_behavior_test`, cây tạm thiếu `bash_nen.py` (N14 gây ra);
      · `570-do-7` — `python_alias_behavior_test`, `WinError 1314` thiếu đặc quyền symlink.
    Ba nguyên nhân khác hẳn nhau, một chỗ hỏng: LỜI GỌI nằm ngoài mọi khung bắt lỗi. Nên chữa
    ở chỗ gọi, không chữa từng nguyên nhân — nguyên nhân thứ tư sẽ lại khác.

    `None ≠ False`: bỏ qua KHÔNG được lặng lẽ thành xanh. Nó phải hiện ra VÀ kéo mã thoát.
    Ba chốt, mỗi chốt một đầu vào riêng:
      (1) `BoQuaMoiTruong` ⇒ trả (tên, lý do), KHÔNG ném — suite đi tiếp;
      (2) chạy trót lọt ⇒ trả None;
      (3) chốt NGHIỆP VỤ hỏng ⇒ VẪN ném — một tiền kiểm hỏng thật thì phải giết, đó là việc
          của nó, và nếu (3) mất thì hàm này biến mọi hỏng hóc thành im lặng.
    """
    p = subprocess.run([sys.executable, str(TEP_TEST), "--tu-kiem-tien-kiem"],
                       cwd=GOC, capture_output=True, text=True, timeout=120)
    dung(p.returncode == 0 and "TK1 " in p.stdout,
         f"không chạy được cửa tự kiểm tiền kiểm: rc={p.returncode}\n{p.stdout}\n{p.stderr}")
    doc = {l[:3]: json.loads(l[4:]) for l in p.stdout.splitlines()
           if l[:3] in ("TK1", "TK2", "TK3")}

    bang(doc.get("TK1") and doc["TK1"][0] == "thieu_moi_truong",
         f"(1) `BoQuaMoiTruong` phải được GHI NHẬN, nhận về {doc.get('TK1')!r}\n{p.stdout}")
    bang("thiếu thứ để đo" in (doc["TK1"][1] or ""),
         f"(1) không giữ lý do: {doc['TK1']!r}")
    bang(doc.get("TK2") is None,
         f"(2) tiền kiểm chạy trót lọt mà vẫn bị đếm là bỏ qua: {doc.get('TK2')!r}")
    bang(doc.get("TK3", [None])[0] == "NEM",
         "(3) chốt NGHIỆP VỤ hỏng mà `_chay_tien_kiem` NUỐT — một tiền kiểm hỏng thật phải "
         f"giết; nuốt nó là biến cổng thành trang trí: {doc.get('TK3')!r}")


@ca
def t32_dong_ho_nhay_la_KHONG_DO_DUOC_chu_khong_phai_tin_dung_gia():
    """Thời lượng ÂM ⇒ KHÔNG ĐO ĐƯỢC; thời lượng DƯƠNG ⇒ vẫn là tín dụng giả.

    SINH TỪ PHÉP ĐO, không từ lo xa. Nghiệm thu Windows `570-do-8` (HEAD 05ec2eb):
        t28_bash_nen_tu_choi_bash_TREO_trong_han [tin_dung_gia]
        TimeoutExpired: ... timed out after -232.95556909999868 seconds
    trên một `subprocess.run(..., timeout=120)`. Một lượt chờ THẬT không thể hết hạn sau một
    khoảng ÂM — đó là phép trừ hạn chót đi ngược, tức mốc thời gian nhảy lùi. Xếp nó chung với
    "lỗi vô can" làm mất đúng thứ đọc được, và đổ cái chết ấy vào bán kính của một đột biến
    vô can là QUY SAI NGUYÊN NHÂN.

    CHỐT (2) LÀ CHỐT QUAN TRỌNG HƠN. Nới phép nhận diện ra mọi `TimeoutExpired` sẽ nuốt luôn
    quá hạn THẬT — mà quá hạn thật chính là thứ `t28` sinh ra để đo (bash giả treo 600s). Lúc
    ấy cổng thành trang trí. Nên hai chốt có hai đột biến RIÊNG, phân biệt bằng ĐẦU VÀO.

    KHÔNG NỚI CỔNG: `bo_qua` cho ca ĐÍCH vẫn làm `_ket_luan_ban_kinh` báo KHÔNG_ĐO_ĐƯỢC và
    tính lỗi. Bản vá chỉ thôi đổ tội cho đột biến, không thôi báo động.
    """
    p = subprocess.run([sys.executable, str(TEP_TEST), "--tu-kiem-dong-ho"],
                       cwd=GOC, capture_output=True, text=True, timeout=120)
    dung(p.returncode == 0 and "DH1 " in p.stdout,
         f"không chạy được cửa tự kiểm đồng hồ: rc={p.returncode}\n{p.stdout}\n{p.stderr}")
    doc = {l[:3]: json.loads(l[4:]) for l in p.stdout.splitlines() if l[:3] in ("DH1", "DH2")}

    tt, ly = doc.get("DH1", [None, None])
    bang(tt == "bo_qua",
         f"(1) thời lượng ÂM phải là KHÔNG ĐO ĐƯỢC (`bo_qua`), nhận về {tt!r}\n{p.stdout}")
    bang("ÂM" in (ly or "") and "-232.95" in (ly or ""),
         f"(1) lý do không nêu chữ ký đo được (thời lượng ÂM + con số): {ly!r}")

    tt2, ly2 = doc.get("DH2", [None, None])
    bang(tt2 == "tin_dung_gia",
         f"(2) quá hạn THẬT (thời lượng dương) bị NUỐT thành {tt2!r} — phép nhận diện quá "
         f"rộng thì nó nuốt đúng thứ `t28` sinh ra để đo, và cổng thành trang trí\n{p.stdout}")


_HINH_DANG_PHU = {
    "which_chuoi":     'import shutil\nb = shutil.which("bash")\n',
    "which_bash_exe":  'import shutil\nb = shutil.which("bash.exe")\n',
    "which_keyword":   'import shutil\nb = shutil.which(cmd="bash")\n',
    "run_list":        'import subprocess\nsubprocess.run(["bash", "-c", "x"])\n',
    "run_keyword":     'import subprocess\nsubprocess.run(args=["bash", "-c", "x"])\n',
    "popen_list":      'import subprocess\nsubprocess.Popen(["bash", "-c", "x"])\n',
    # HOA/thuong — them o r7 sau mot phep do. Tren Windows ten tep thuc thi KHONG phan biet
    # hoa/thuong, nen hai dong duoi phong ra DUNG mot tep nhu `bash.exe`. Ban truoc tra `[]`
    # cho ca hai: cong vua mo ra toan cay bi di vong bang MOT PHIM SHIFT.
    "which_HOA":       'import shutil\nb = shutil.which("BASH.EXE")\n',
    "run_hoa_thuong":  'import subprocess\nsubprocess.run(["Bash.exe"])\n',
    # LOP E, vong 2. `executable=` GHI DE chuong trinh that su chay, du `args[0]` ghi ten khac.
    "executable_kw":   'import subprocess\nsubprocess.run(["x"], executable="bash")\n',
    "executable_HOA":  'import subprocess\nsubprocess.Popen(["x"], executable="BASH.EXE")\n',
    "alias_module":    'import subprocess as sp\nsp.run(["bash"])\n',
    "from_import":     'from shutil import which\nwhich("bash")\n',
    "from_import_as":  'from shutil import which as w\nw("bash")\n',
    # r8 — LOP "do phu theo hinh dang sai CA HAI HUONG", chieu LOT. Cross-review codex vong 3
    # chi F3/F4; quet theo lop tim them hai hinh dang duoi (ca hai do duoc `[]` truoc va).
    "run_chuoi_tran":  'import subprocess\nsubprocess.run("bash")\n',
    "executable_vi_tri": 'import subprocess\nsubprocess.Popen(["x"], 0, "bash")\n',
    # Pham vi tu vung, chieu BAT: import o module, goi trong ham; va import ngay trong ham.
    "goi_trong_ham":   'import subprocess\ndef f():\n    subprocess.run(["bash"])\n',
    "import_trong_ham": 'def f():\n    import shutil\n    shutil.which("bash")\n',
    # r10 — LOP "phan loai rang buoc theo TEN, bo qua mot TRUONG cua nut AST", chieu LOT.
    # `import subprocess.x` RANG BUOC ten `subprocess` vao CHINH module stdlib ay (luat
    # Python). Ban r9 gan `("khac",)` cho no nen hinh dang nay do duoc `[]`. Codex vong 4
    # KHONG chi mat nay — no ra tu phep quet theo LOP tu mat codex co chi.
    "import_module_con": 'import subprocess.x\nsubprocess.run(["bash"])\n',
    # r11 — N30, hang byte. `shutil.which(b"bash")` CHAY bash that; ban r10 loai chung chi vi
    # khong phai `str`, tuc mot duong vong khong can phan tich luong du lieu nao.
    "byte_which":      'import shutil\nshutil.which(b"bash")\n',
    "byte_HOA":        'import shutil\nshutil.which(b"BASH.EXE")\n',
    "byte_run_list":   'import subprocess\nsubprocess.run([b"bash"])\n',
    "byte_executable": 'import subprocess\nsubprocess.run(["sh"], executable=b"bash")\n',
    # r11 — N29, `global` chuyen rang buoc ve pham vi SO HUU. Ca CO LAP: module khong co rang
    # buoc nao khac, nen `import` trong than ham la rang buoc DUY NHAT cua ten o module.
    "global_import":   'def f():\n    global subprocess\n    import subprocess\n    subprocess.run(["bash"])\n',
    # Chieu nguoc cua ban va walrus: mot comprehension THUONG khong che duoc gi.
    "comprehension_thuong": 'import subprocess\n[x for x in [0]]\nsubprocess.run(["bash"])\n',
    # r13 — N37: bieu thuc LUC DINH NGHIA tinh o pham vi NGOAI, chi THAN moi o pham vi moi.
    # Ban r12 giai ca hai o pham vi TRONG, nen chinh tham so che ten module thi lot.
    "mac_dinh_che_ten_module": 'import shutil\ndef f(shutil=shutil.which("bash")):\n    pass\n',
    "ham_LONG_trong_ham":      'def run():\n    def f():\n        import shutil as sh\n        return sh.which("bash")\n',
    # r15 — N39: pham vi KHAI `global` ma TU no `import` thi trong than la MODULE that.
    "global_roi_import": 'subprocess = object()\ndef f():\n    global subprocess\n    import subprocess\n    subprocess.run(["bash"])\n',
    # r16 — N45, HAI HELPER CHAY QUA SHELL. `getstatusoutput("bash -c ...")` do duoc la CHAY
    # THAT (tra `(0, "XIN_CHAO")`), nhung ca hai vang khoi tap callee duoc che nen ra `[]`.
    "shell_ra_getoutput":  'import subprocess\nsubprocess.getoutput("bash")\n',
    "shell_ra_trang_thai": 'import subprocess\nsubprocess.getstatusoutput("bash")\n',
    "shell_ra_keyword":    'import subprocess\nsubprocess.getoutput(cmd="bash")\n',
    "shell_ra_from_import":'from subprocess import getstatusoutput\ngetstatusoutput("BASH.EXE")\n',
    # r16 — N45, TEN CHUONG TRINH BOC `pathlib`. `run([Path("bash")])` chay bash THAT (do
    # duoc: in ra `OK`), `Path` chi la mot lop vo quanh DUNG cai ten ay.
    "duong_pathlib_which": 'import shutil\nfrom pathlib import Path\nshutil.which(Path("bash"))\n',
    "duong_pathlib_argv":  'import subprocess\nfrom pathlib import Path\nsubprocess.run([Path("bash")])\n',
    "duong_pathlib_exec":  'import subprocess\nfrom pathlib import Path\nsubprocess.run(["x"], executable=Path("bash"))\n',
    "duong_pathlib_pure":  'import subprocess, pathlib\nsubprocess.run([pathlib.PurePath("bash.exe")])\n',
    # r16 — N46, MODULE va THAN LOP chay theo THU TU CAU LENH. Loi goi o dong 2 CHAY THAT
    # tren module da `import`; phep gan o dong 3 chua xay ra.
    "module_gan_SAU":      'import subprocess\nsubprocess.run(["bash"])\nsubprocess = runner\n',
    "lop_gan_SAU":         'import subprocess\nclass C:\n    subprocess.run(["bash"])\n    subprocess = runner\n',
    "lop_rang_buoc_SAU_ra_module": 'import subprocess\nclass C:\n    subprocess.run(["bash"])\n',
    # r17 — N52, BO TINH HANG. Bon revision truoc them TUNG HINH DANG; vong 10 va 11 van ra
    # hinh dang moi. Nay rut gon bieu thuc ve GIA TRI roi moi hoi. Ca ba dang duoi deu ra
    # dung chuoi `bash`, va `Path("", "bash")` CHAY THAT (do duoc: in ra `OK`).
    "duong_pathlib_rong_dau":  'import subprocess\nfrom pathlib import Path\nsubprocess.run([Path("", "bash")])\n',
    "duong_pathlib_cham":      'import subprocess\nfrom pathlib import Path\nsubprocess.run([Path(".", "bash")])\n',
    "duong_pathlib_rong_cuoi": 'import subprocess\nfrom pathlib import Path\nsubprocess.run([Path("bash", "")])\n',
    # r17 — N52: TAP HOP MOT phan tu. `run({"bash"})` CHAY bash that (do duoc: rc=0).
    "tap_mot_phan_tu":         'import subprocess\nsubprocess.run({"bash"})\n',
    "tap_mot_phan_tu_args":    'import subprocess\nsubprocess.run(args={"bash"})\n',
    # r17 — N52: phep NOI hang. Bo liet ke khong the doan truoc cach chia mot chuoi.
    "noi_hang_cong":           'import subprocess\nsubprocess.run(["ba" + "sh"])\n',
    "noi_hang_lien_ke":        'import subprocess\nsubprocess.run(["ba" "sh"])\n',
    "noi_hang_byte":           'import shutil\nshutil.which(b"ba" + b"sh")\n',
    # r17 — N53: rang buoc HOAN TAT muon nhat thang. Ca hai deu CHAY BASH THAT.
    "re_import_sau_gan":       'subprocess = object()\nimport subprocess\nsubprocess.run(["bash"])\n',
    "gan_tu_chinh_RHS":        'import subprocess\nsubprocess = subprocess.run(["bash"])\n',
    "mac_dinh_cung_dong":      'import subprocess\ndef subprocess(x=subprocess.run(["bash"])):\n    pass\n',
    "lop_re_import":           'subprocess = object()\nclass C:\n    import subprocess\n    subprocess.run(["bash"])\n',
    # r18 — N58: `dict` lam argv (KHOA DAU TIEN la chuong trinh; thu tu khoa XAC DINH) va
    # VO BOC GIU HANG. Ca nam dang duoi deu CHAY BASH THAT tren nen nay (in ra `OK`).
    "dict_lam_argv":           'import subprocess\nsubprocess.run({"bash": None})\n',
    "boc_encode":              'import subprocess\nsubprocess.run(["bash".encode(), "-c", "x"])\n',
    "boc_str_path":            'import subprocess\nfrom pathlib import Path\nsubprocess.run([str(Path("bash"))])\n',
    "boc_os_fspath":           'import subprocess, os\nfrom pathlib import Path\nsubprocess.run([os.fspath(Path("bash"))])\n',
    "boc_bytes":               'import subprocess\nsubprocess.run([bytes("bash", "ascii")])\n',
    # r18 — N59: API KHAC phong bash THEO TEN. Tu r8 day la NO CO TEN; vong 12 do ba, phien
    # do them sau — ca CHIN deu CHAY THAT.
    "os_execvp":               'import os\nos.execvp("bash", ["bash"])\n',
    "os_execlp":               'import os\nos.execlp("bash", "bash")\n',
    "os_posix_spawnp":         'import os\nos.posix_spawnp("bash", ["bash"], {})\n',
    "os_spawnlp_mode_dau":     'import os\nos.spawnlp(os.P_WAIT, "bash", "bash")\n',
    "os_spawnvp":              'import os\nos.spawnvp(os.P_WAIT, "bash", ["bash"])\n',
    "os_system":               'import os\nos.system("bash")\n',
    "os_system_path":          'import os\nfrom pathlib import Path\nos.system(Path("bash"))\n',
    "os_popen":                'import os\nos.popen("bash")\n',
    "asyncio_exec":            'import asyncio\nasyncio.create_subprocess_exec("bash")\n',
    "asyncio_exec_tu_khoa":    'import asyncio\nasyncio.create_subprocess_exec(program="bash")\n',
    "asyncio_shell":           'import asyncio\nasyncio.create_subprocess_shell("bash")\n',
    "from_os_import":          'from os import execvp\nexecvp("bash", ["bash"])\n',
    "popen_qua_fspath":        'import os\nfrom pathlib import Path\nos.popen(os.fspath(Path("bash")))\n',
    # r19 — N67, DOI NGUOC doctrine r8: pham vi HAM truc tiep chua loi goi cung theo THU TU
    # THUC THI. Ca ba deu CHAY BASH THAT tren 3.12.3 (in ra `OK`).
    "ham_goi_TRUOC_khi_che": 'def f():\n    import subprocess\n    subprocess.run(["bash"])\n    subprocess = runner\n',
    "ham_re_import":       'def f():\n    subprocess = object()\n    import subprocess\n    subprocess.run(["bash"])\n',
    "ham_goi_trong_RHS":   'def f():\n    import subprocess\n    subprocess = subprocess.run(["bash"])\n',
    # r19 — N65: bon toan tu giu hang nua; ca bon CHAY THAT.
    "hang_f_string":       'import subprocess\nsubprocess.run([f"bash", "-c", "x"])\n',
    "hang_phan_tram":      'import subprocess\nsubprocess.run(["%s" % "bash", "-c", "x"])\n',
    "hang_join":           'import subprocess\nsubprocess.run(["".join(["ba", "sh"]), "-c", "x"])\n',
    "hang_cat_lat":        'import subprocess\nsubprocess.run(["hsab"[::-1], "-c", "x"])\n',
    # r19 — N68: chu thich KHONG co `__future__` o module/lop thi CO chay.
    "chu_thich_tham_so":   'import subprocess\ndef f(x: subprocess.run(["bash"])):\n    pass\n',
    "chu_thich_bien_module": 'import subprocess\nx: subprocess.run(["bash"]) = 1\n',
    "mac_dinh_van_chay_co_future": 'from __future__ import annotations\nimport subprocess\ndef f(x=subprocess.run(["bash"])):\n    pass\n',
    # r20 — N73 DOI NGUOC mot phan N68: chu thich HOAN van duoc LUU, va `typing.get_type_hints`
    # / `eval(f.__annotations__[...])` TINH LAI duoc — do tren 3.12.3 THAT, in ra `OK`.
    "chu_thich_future":    'from __future__ import annotations\nimport subprocess\ndef f(x: subprocess.run(["bash"])):\n    pass\n',
    "chu_thich_tra_ve_future": 'from __future__ import annotations\nimport subprocess\ndef f() -> subprocess.run(["bash"]):\n    pass\n',
    "chu_thich_bien_lop_future": 'from __future__ import annotations\nimport subprocess\nclass C:\n    x: subprocess.run(["bash"])\n',
    # r20 — N72: RANG BUOC TOI DUOC LOI GOI theo NHANH. Moi ca duoi CHAY BASH THAT tren 3.12.3.
    # (M1) loi goi trong THAN HAM khong theo thu tu voi module — ham chay SAU `import`.
    "ham_goi_truoc_import_module": 'def f():\n    subprocess.run(["bash"])\nimport subprocess\n',
    # canh QUAY LUI: vong thu hai thay `import` cua vong truoc.
    "quay_lui_vong_lap_ham": 'def f():\n    for i in range(2):\n        if i:\n            subprocess.run(["bash"])\n        import subprocess\n',
    "quay_lui_vong_lap_module": 'for i in range(2):\n    if i:\n        subprocess.run(["bash"])\n    import subprocess\n',
    # `try` roi `except`: than `try` chay TRUOC handler, khong loai tru.
    "try_import_except_goi": 'def f():\n    try:\n        import subprocess\n        raise E\n    except E:\n        subprocess.run(["bash"])\n',
    # `finally` LUON chay ⇒ `import` trong no che phep gan cu.
    "finally_import_goi_sau": 'def f():\n    subprocess = None\n    try:\n        pass\n    finally:\n        import subprocess\n    subprocess.run(["bash"])\n',
    # than lop: loi con lai (chua gan) la `NameError` vi module KHONG rang buoc ten ay.
    "lop_nhanh_import_module_trong": 'import os\nclass C:\n    if os.sep:\n        import subprocess\n    subprocess.run(["bash"])\n',
    # generator chay LUC KHAC ⇒ module khong theo thu tu voi no.
    "genexp_goi_import_sau": 'g = (subprocess.run(["bash"]) for _ in [0])\nimport subprocess\n',
    # r21 — N76, vong 15: `except*` CO THE chay NHIEU nhanh; walrus trong comprehension thuoc
    # pham vi CHUA. Ca hai CHAY BASH THAT tren 3.12 ma r20 tra `[]`.
    "except_sao_cung_chay": 'def f():\n    try:\n        pass\n    except* ValueError:\n        import subprocess\n    except* TypeError:\n        subprocess.run(["bash"])\n',
    "walrus_trong_comprehension": 'import subprocess\n[(subprocess.run(["bash"]), (subprocess := object())) for _ in [0]]\n',
    # r22 — N81, vong 16 H3/H4: NAP DONG voi ten HANG. Ca sau deu CHAY BASH THAT (do tren 3.12).
    "nap_dong_import":         '__import__("subprocess").run(["bash"])\n',
    "nap_dong_builtins":       '__builtins__.__import__("subprocess").run(["bash"])\n',
    "nap_dong_importlib":      'import importlib\nimportlib.import_module("subprocess").run(["bash"])\n',
    "nap_dong_gan_ten":        'm = __import__("subprocess")\nm.run(["bash"])\n',
    "exec_import_roi_goi":     'exec("import subprocess")\nsubprocess.run(["bash"])\n',
    "exec_tai_co_loi_goi":     'exec("import subprocess\\nsubprocess.run([\'bash\'])")\n',
    # r23 — N83 (F1/F2 vong 17): nap dong qua BI DANH, moi dich gan, `AnnAssign`, `importlib.__import__`,
    # `builtins.exec`, gia tri cua `eval` hang; tai `exec` GAP hang (`bytes`, `+`, f-string) va
    # doc rang buoc cua CA TEP (ham chua `exec`, nap dong, `exec` truoc). Ca hai muoi dang deu CHAY
    # BASH THAT tren 3.12 ma r22 tra `[]`.
    "nap_dong_from_import_module": 'from importlib import import_module\nm = import_module("subprocess")\nm.run(["bash"])\n',
    "nap_dong_bi_danh_import_module": 'from importlib import import_module as im\nm = im("subprocess")\nm.run(["bash"])\n',
    "nap_dong_importlib_bi_danh": 'import importlib as il\nm = il.import_module("subprocess")\nm.run(["bash"])\n',
    "nap_dong_builtins_bi_danh": 'from builtins import __import__ as imp\nm = imp("subprocess")\nm.run(["bash"])\n',
    "nap_dong_gan_day_chuyen": 'a = b = __import__("subprocess")\na.run(["bash"])\n',
    "nap_dong_gan_chu_thich": 'm: object = __import__("subprocess")\nm.run(["bash"])\n',
    "nap_dong_importlib_import": 'import importlib\nimportlib.__import__("subprocess").run(["bash"])\n',
    "nap_dong_hai_tang": 'il = __import__("importlib")\nm = il.import_module("subprocess")\nm.run(["bash"])\n',
    "builtins_exec":        'import builtins\nbuiltins.exec("import subprocess\\nsubprocess.run([\'bash\'])")\n',
    "eval_tra_module":      'eval("__import__(\'subprocess\')").run(["bash"])\n',
    "exec_tai_bytes":       'exec(b"import subprocess\\nsubprocess.run([\'bash\'])")\n',
    "exec_tai_noi":         'exec("import subprocess\\n" + "subprocess.run([\'bash\'])")\n',
    "exec_tai_f_string":    'exec(f"import subprocess\\nsubprocess.run([\'bash\'])")\n',
    "exec_trong_ham_doc_cuc_bo": 'def f():\n    import subprocess\n    exec("subprocess.run([\'bash\'])")\n',
    "exec_doc_nap_dong":    'm = __import__("subprocess")\nexec("m.run([\'bash\'])")\n',
    "exec_doc_exec_truoc":  'exec("import subprocess")\nexec("subprocess.run([\'bash\'])")\n',
    # r23 — N85 (F3 vong 17): argv NOI / TRAI, phan tu DAU la hang cua bao chua viet tai loi goi.
    "argv_noi_list":        'import subprocess, sys\nsubprocess.run(["bash", "-c"] + sys.argv[1:] + ["x"])\n',
    "argv_noi_list_don":    'import subprocess\nsubprocess.run(["bash"] + ["-c", "x"])\n',
    "argv_trai_tuple":      'import subprocess\nsubprocess.run([*("bash", "-c"), "x"])\n',
    "argv_noi_tuple":       'import subprocess\nsubprocess.run(("bash",) + ("-c", "x"))\n',
    "argv_noi_rong_truoc":  'import subprocess\nsubprocess.run([] + ["bash"])\n',
    # r24 — N88..N90 (codex vong 18): trai `dict`/`set` MOT phan tu, chuoi `+` dai, `name=`, callee
    # TINH RA cho `exec`/`__import__`. Ca muoi dang deu CHAY BASH THAT tren 3.12 ma r23 tra `[]`.
    "argv_trai_dict":       'import subprocess\nsubprocess.run([*{"bash": None}, "-c", "x"])\n',
    "argv_trai_set_mot":    'import subprocess\nsubprocess.run([*{"bash"}, "-c", "x"])\n',
    "hang_noi_chin_tang":   'import subprocess\nsubprocess.run(["" + "" + "" + "" + "" + "" + "" + "" + "" + "bash"])\n',
    "nap_dong_tu_khoa_name": 'import importlib\nimportlib.import_module(name="subprocess").run(["bash"])\n',
    "nap_dong_gan_tu_khoa": 'import importlib\nm = importlib.import_module(name="subprocess")\nm.run(["bash"])\n',
    "exec_qua_dict_builtins": 'import builtins\nbuiltins.__dict__["exec"]("import subprocess\\nsubprocess.run([\'bash\'])")\n',
    "exec_qua_getattr":     'import builtins\ngetattr(builtins, "exec")("import subprocess\\nsubprocess.run([\'bash\'])")\n',
    "nap_dong_qua_dict_builtins": 'import builtins\nbuiltins.__dict__["__import__"]("subprocess").run(["bash"])\n',
    # r26 — N98 (codex vong 20): chu thich LUU duoi `__future__` duoc tinh trong GLOBALS cua module
    # — ham bao che ten khong che duoc `get_type_hints` (do: phong bash that).
    "chu_thich_hoan_ham_bao_che": 'from __future__ import annotations\nimport subprocess\ndef o():\n    subprocess = object()\n    def i(x: subprocess.run(["bash"])):\n        pass\n    return i\n',
    # r27 — N99 (codex vong 21): chu thich la CHUOI tham chieu toi — `get_type_hints` TINH no, co
    # hay khong `__future__`. N97b: `eval` bo khoang trang dau truoc khi phan tich.
    "chu_thich_chuoi":      'import subprocess\ndef f(x: "subprocess.run([\'bash\'])"):\n    pass\n',
    "chu_thich_chuoi_future": 'from __future__ import annotations\nimport subprocess\ndef f(x: "subprocess.run([\'bash\'])"):\n    pass\n',
    "chu_thich_chuoi_bien_lop": 'import subprocess\nclass C:\n    x: "subprocess.run([\'bash\'])" = 1\n',
    "eval_khoang_trang_dau": 'eval("  __import__(\'subprocess\').run([\'bash\'])")\n',
    # r29 — N102 (codex vong 23): chuoi NAP DONG ba tang, giai toi bat dong diem (ban r28 dung sau
    # 2 vong va lot). N104: hai loi goi trong MOT chu thich chuoi la HAI ban ghi (chot (1m)).
    # r30 — N107: do chinh xac cua `%s` la TRAN; ca ba ra dung `bash` va CHAY BASH THAT.
    "phan_tram_chinh_xac_sao_chu":  'import subprocess\nsubprocess.run(["%.*s" % (5000, "bash")])\n',
    "phan_tram_rong_chinh_xac_sao": 'import subprocess\nsubprocess.run(["%*.*s" % (1, 5000, "bash")])\n',
    "phan_tram_chinh_xac_tinh_chu": 'import subprocess\nsubprocess.run(["%.5000s" % "bash"])\n',
    # r31 — N110: `%b` cua bytes, do chinh xac la TRAN; ca ba ra dung `b"bash"` va CHAY BASH THAT.
    "phan_tram_b_chinh_xac_sao":  'import subprocess\nsubprocess.run([b"%.*b" % (5000, b"bash")])\n',
    "phan_tram_b_rong_chinh_xac": 'import subprocess\nsubprocess.run([b"%*.*b" % (1, 5000, b"bash")])\n',
    "phan_tram_b_chinh_xac_tinh": 'import subprocess\nsubprocess.run([b"%.5000b" % b"bash"])\n',
    # r31 — N112: phu thuoc nam TRONG tai `eval("b")` hang; vong lap hai luot chay bash that (codex vong 25).
    "nap_dong_eval_vong_lap": 'import importlib as il\nfor i in range(2):\n    if i:\n        a = eval("b")\n        a.run(["bash"])\n    b = il.import_module("subprocess")\n',
    # r33 — N117: phu thuoc trong tai `eval` qua BI DANH dung san (codex vong 27; chay bash that).
    "nap_dong_eval_bi_danh_goc":  'import builtins as bi, importlib as il\nfor i in range(2):\n    if i:\n        a = bi.eval("b")\n        a.run(["bash"])\n    b = il.import_module("subprocess")\n',
    "nap_dong_eval_bi_danh_thang": 'from builtins import eval as ev\nimport importlib as il\nfor i in range(2):\n    if i:\n        a = ev("b")\n        a.run(["bash"])\n    b = il.import_module("subprocess")\n',
    # r34 — N118: khoa anh xa co ngoac LONG (codex vong 28); ra dung `bash` va CHAY BASH THAT.
    "phan_tram_khoa_ngoac_long":   'import subprocess\nsubprocess.run(["%((a))s" % {"(a)": "bash"}])\n',
    "phan_tram_khoa_ngoac_giua":   'import subprocess\nsubprocess.run(["%(a(b)c)s" % {"a(b)c": "bash"}])\n',
    # r35 — N119: `executable=` cua asyncio GHI DE chuong trinh (codex vong 29; chay bash that).
    "asyncio_exec_executable":  'import asyncio\nasyncio.create_subprocess_exec("x", "-c", "true", executable="bash")\n',
    "asyncio_shell_executable": 'import asyncio\nasyncio.create_subprocess_shell("true", executable="bash")\n',
    "nap_dong_ba_tang":     'a = __import__("importlib")\nb = a.import_module("importlib")\nc = b.import_module("subprocess")\nc.run(["bash"])\n',
    # r23 — N86 (F7 vong 17): `%` voi ve phai `dict`.
    "hang_phan_tram_dict":  'import subprocess\nsubprocess.run(["%(a)s" % {"a": "bash"}])\n',
    # r22 — N82, vong 16 H1/H2: `nonlocal` di toi DUNG chu so huu; `global str` CHI DOC khong che.
    "nonlocal_ba_tang":        'def o():\n    x = 1\n    def m():\n        nonlocal x\n        x = object()\n        def i():\n            nonlocal x\n            import subprocess as x\n            x.run(["bash"])\n',
    "global_str_chi_doc":      'import subprocess\ndef f():\n    global str\n    subprocess.run([str("bash")])\n',
    # r20 — N74: `%` voi do rong NHO van gap duoc.
    "hang_phan_tram_do_rong": 'import subprocess\nsubprocess.run(["%4s" % "bash"])\n',
    # r19 — N66: `pty.spawn` kieu ARGV; chuoi tran CUNG chay (do duoc rc 0).
    "pty_spawn_argv":      'import pty\npty.spawn(["bash", "-c", "x"])\n',
    "pty_spawn_chuoi":     'import pty\npty.spawn("bash")\n',
    "pty_from_import":     'from pty import spawn\nspawn(["bash"])\n',
    # r18 — N60: THAN LOP chay ngay luc dinh nghia, nen ten LOP chi rang buoc SAU ca than.
    "lop_cung_ten_goi_trong_than": 'import subprocess\nclass subprocess:\n    x = 1\n    subprocess.run(["bash"])\n',
    # r16 — N47, PEP 695: `type X[T] = ...` co pham vi chu thich RIENG (chay qua `t50`).
    "global_doc_khong":  'import subprocess\ndef f():\n    global subprocess\n    subprocess.run(["bash"])\n',
    # r15 — N40 chieu BAT: `:=` trong THAN la cua than, khong che duoc gi o ngoai.
    "walrus_trong_than": 'import subprocess\ndef f():\n    y = (subprocess := runner)\nsubprocess.run(["bash"])\n',
}
# `executable=` GHI DE, nen ca hai cung ten `bash` van la DUNG MOT ban ghi (F4, chieu dem).
_HINH_DANG_MOT_BAN_GHI = 'import subprocess\nsubprocess.run(["bash"], executable="bash")\n'
_HINH_DANG_KHONG_PHU = {
    "shell_true":      'import subprocess\nsubprocess.run("bash -c x", shell=True)\n',
    "os_system":       'import os\nos.system("bash -c x")\n',
    "bien_trung_gian": 'import shutil\nt = "bash"\nb = shutil.which(t)\n',
    # HUONG NGUOC cua lop E: nhan dien theo TEN ma khong giai CALLEE thi bat OAN. Hai dong
    # duoi KHONG goi stdlib nao — chung la API cua nguoi khac trung ten.
    "run_khong_stdlib":   'runner.run(["bash"])\n',
    "which_khong_stdlib": 'matcher.which("bash")\n',
    # r8 — F4 codex vong 3: `executable=` GHI DE `argv[0]`. Lenh nay chay `echo`, khong chay
    # `bash`; ban truoc CONG THEM nen bat oan `[(2, 0)]`.
    "executable_ghi_de_khac": 'import subprocess\nsubprocess.run(["bash"], executable="/bin/echo")\n',
    # r8 — F3 codex vong 3: `_bang_ten_stdlib` `ast.walk` ca cay vao MOT bang, nen `import`
    # trong ham A "co hieu luc" o ham B, va tham so tren `subprocess` o B khong che duoc gi.
    # Bon hinh dang, moi cai troi MOT mat: (a) F3 nguyen van; (b) chi ro ri, khong che;
    # (c) chi tham so che; (d) phep gan che trong ham. Hai dot bien tach duoc (b) khoi (c)/(d).
    "pham_vi_ro_ri":   'def a():\n    import subprocess\n\n\ndef b(subprocess):\n    subprocess.run(["bash"])\n',
    "import_ham_khac": 'def a():\n    import subprocess\ndef b():\n    subprocess.run(["bash"])\n',
    "tham_so_che":     'import subprocess\ndef b(subprocess):\n    subprocess.run(["bash"])\n',
    "gan_che":         'import shutil\ndef f():\n    shutil = gia()\n    shutil.which("bash")\n',
    # r10 — CUNG LOP, chieu BAT OAN. `level` la MOT PHAN CUA Y NGHIA: `from .subprocess import
    # run` tro vao module CUNG GOI, khong phai stdlib. Codex vong 4 chi mat nay; do duoc
    # `[(2, 0)]` truoc va. `from . import subprocess` von da dung (n.module is None) nen giu
    # lai lam chieu thu ba, de mot ban va cho `level` khong am tham lam hong no.
    "from_tuong_doi":  'from .subprocess import run\nrun(args=["bash"])\n',
    "from_tuong_doi_2": 'from ..shutil import which\nwhich("bash")\n',
    "from_cham_module": 'from . import subprocess\nsubprocess.run(["bash"])\n',
    # `import subprocess.x as y` KHONG rang buoc `subprocess` — chi `y` ← module con. Day la
    # chieu nguoc cua `import_module_con`: mot ban va "cu co cham thi nhan" se bat oan o day.
    "import_con_co_as": 'import subprocess.x as y\ny.run(["bash"])\n',
    # r11 — N30 chieu nguoc: byte NGOAI ASCII khong duoc giai ma bua.
    "byte_ngoai_ascii": 'import shutil\nshutil.which(b"\\xff\\xfe")\n',
    # r16 — N45 chieu NGUOC. `Path` bi che boi mot ham cuc bo thi day la API cua nguoi khac.
    "pathlib_bi_che":      'import subprocess\ndef Path(x):\n    return x\nsubprocess.run([Path("bash")])\n',
    "pathlib_khong_stdlib":'import subprocess\nfrom x import Path\nsubprocess.run([Path("bash")])\n',
    "shell_ra_khong_stdlib": 'import x\nx.getoutput("bash")\n',
    # NO CO TEN, khai ra chu khong de tuong da kin: mot DONG LENH SHELL nhieu tu.
    "shell_ra_nhieu_tu":   'import subprocess\nsubprocess.getoutput("bash -c x")\n',
    # `Path("/usr/bin/bash")` la mot DUONG, khong phai phan giai theo TEN — dung ky luat
    # da dung cho chuoi: `which("/usr/bin/bash")` cung khong bi bat.
    "pathlib_duong_tuyet_doi": 'import subprocess\nfrom pathlib import Path\nsubprocess.run([Path("/usr/bin/bash")])\n',
    "pathlib_hai_doi_so":  'import subprocess\nfrom pathlib import Path\nsubprocess.run([Path("bash", "x")])\n',
    # r16 — N46 chieu NGUOC. (a)(b): gan TRUOC loi goi ⇒ ten da bi che that.
    # MAT (c) CU — `ham_gan_SAU_van_mo_ho` — DA CHUYEN SANG `_HINH_DANG_PHU` o r19 (N67). Nó ma
    # hoa mot doctrine SAI tu r8: "trong ham, `import` roi goi roi gan van la mo ho". Do tren
    # 3.12 that: loi goi ay IN RA `OK`. Thay no bang chieu NGUOC DUNG cua N67:
    # `UnboundLocalError` — ten cuc bo chua ghi lan nao thi KHONG doc sang pham vi ngoai.
    # (r21 — N76: mot phan cac hinh dang cua khoi nay DA CHUYEN sang `_HINH_DANG_BAO_THAN_TRONG`.)
    "ham_unbound_local":   'import subprocess\ndef f():\n    subprocess.run(["bash"])\n    subprocess = runner\n',
    # r17 — N52 chieu NGUOC. Tap NHIEU phan tu: thu tu duyet cua `set` KHONG xac dinh nen
    # khong biet phan tu nao la chuong trinh; doan bua la bat oan.
    "tap_nhieu_phan_tu":    'import subprocess\nsubprocess.run({"bash", "sh"})\n',
    # Hai thanh phan noi lai thanh mot DUONG, khong con la phan giai theo TEN.
    "pathlib_noi_thanh_duong": 'import subprocess\nfrom pathlib import Path\nsubprocess.run([Path("usr", "bash")])\n',
    # r17 — F3 vong 11: BAO DONG GIA do chinh ban va r16 de ra. `Popen(shell=True)` TU CHOI
    # doi so path-like; do duoc: `subprocess.getoutput(Path("bash"))` nem
    # `TypeError: path-like args is not allowed when shell is true`. Mot cong bat oan la cong
    # se bi tat — nen hai dong nay la chot giu cho N52 khong tran sang nhanh shell.
    "shell_ra_path_like":   'import subprocess\nfrom pathlib import Path\nsubprocess.getoutput(Path("bash"))\n',
    "shell_ra_path_like_2": 'import subprocess\nfrom pathlib import Path\nsubprocess.getstatusoutput(Path("bash"))\n',
    # r18 — N58 chieu NGUOC. `**x` o dau `dict` — khong biet no mang gi; `str` bi che thi la
    # ham nguoi dung; `str(b"bash")` ra `"b'bash'"` nhu Python lam, khong phai ten `bash`.
    "dict_trai_dau":        'import subprocess\nsubprocess.run({**x, "bash": 1})\n',
    "boc_str_bi_che":       'import subprocess\nfrom pathlib import Path\ndef str(x):\n    return x\nsubprocess.run([str(Path("bash"))])\n',
    "boc_str_cua_bytes":    'import subprocess\nsubprocess.run([str(b"bash")])\n',
    # r18 — N59 chieu NGUOC. KIEU DUOC NHAN la cua TUNG API, do rieng: `os.popen` tu choi ca
    # path-like lan bytes; `create_subprocess_shell` tu choi path-like. Bat chung la bat OAN.
    "os_popen_path":        'import os\nfrom pathlib import Path\nos.popen(Path("bash"))\n',
    "os_popen_bytes":       'import os\nos.popen(b"bash")\n',
    "asyncio_shell_path":   'import asyncio\nfrom pathlib import Path\nasyncio.create_subprocess_shell(Path("bash"))\n',
    # bien the KHONG `p` KHONG tim theo PATH — `execv("bash")` do duoc nem FileNotFoundError.
    "os_execv_khong_p":     'import os\nos.execv("bash", ["bash"])\n',
    "os_posix_spawn_khong_p": 'import os\nos.posix_spawn("bash", ["bash"], {})\n',
    # `spawnlp` mang CHE DO o vi tri 0; `"bash"` o do khong phai ten chuong trinh.
    # (r21 — N76: mot phan cac hinh dang cua khoi nay DA CHUYEN sang `_HINH_DANG_BAO_THAN_TRONG`.)
    "os_spawnlp_bash_o_mode": 'import os\nos.spawnlp("bash", "sh", "sh")\n',
    # r19 — N65 chieu NGUOC: gia tri phu thuoc BIEN thi khong doan.
    "hang_f_string_co_bien": 'import subprocess\nsubprocess.run([f"{x}"])\n',
    "hang_join_bien":      'import subprocess\nsubprocess.run(["".join(xs)])\n',
    "hang_cat_lat_khac":   'import subprocess\nsubprocess.run(["bashx"[:3]])\n',
    # r19 — N68 chieu NGUOC, con dung o r20 (N73): chu thich bien CUC BO khong duoc LUU o dau
    # ca, nen khong ai tinh lai duoc. Do tren 3.12 that, khong in gi. (Hai ca `__future__` cu
    # o day DA CHUYEN sang `_HINH_DANG_PHU` — xem N73.)
    "chu_thich_bien_cuc_bo": 'import subprocess\ndef f():\n    x: subprocess.run(["bash"]) = 1\n',
    # r20 — N74: phep that NEM vi GIA TRI thi chuong trinh that cung nem ⇒ khong chay.
    "hang_phan_tram_tran": 'import subprocess\nsubprocess.run(["%c" % 999999999999999999999999999])\n',
    # r21 — N77, vong 15 G4: chu thich tren DICH KHONG DON voi `__future__` — khong tinh, khong
    # luu. Do tren 3.12: khong in gi, `__annotations__` rong.
    # r21 — N76: walrus o gia tri mac dinh / trong comprehension RANG BUOC o pham vi CHUA — tuc
    # lam ten thanh CUC BO cua ham chua no. Duoi N76 thu tu khong con quan trong, nhung PHAM VI
    # van quyet: ham `o` co rang buoc rieng ⇒ ten cuc bo ⇒ khong doc `import` o module.
    "walrus_mac_dinh_cuc_bo_ham": 'import subprocess\ndef o():\n    def f(x=(subprocess := runner)):\n        pass\n    subprocess.run(["bash"])\n',
    "walrus_comprehension_cuc_bo_ham": 'import subprocess\ndef o():\n    [(subprocess := runner) for _ in [0]]\n    subprocess.run(["bash"])\n',
    # r22 — N81/N82 chieu NGUOC.
    "nap_dong_bi_che":         'def __import__(x):\n    return x\n__import__("subprocess").run(["bash"])\n',
    "nap_dong_ten_bien":       '__import__(ten).run(["bash"])\n',
    "exec_vo_hai":             'exec("x = 1")\nsubprocess.run(["bash"])\n',
    "global_str_bi_gan_module": 'import subprocess\nstr = f\ndef f():\n    global str\n    subprocess.run([str("bash")])\n',
    "chu_thich_dich_khong_don_future": 'from __future__ import annotations\nimport subprocess\nholder.x: subprocess.run(["bash"]) = None\n',
    # r23 — N83/N85/N86 chieu NGUOC. Hai dang `argv_*_bien_dau` la NO LUONG DU LIEU, KHONG phai an
    # toan: `xs`/`sys.argv[1:]` rong thi bash CHAY THAT (do duoc) — phan tu dau la mot BIEN.
    "import_module_thu_vien_khac": 'from mylib import import_module\nm = import_module("subprocess")\nm.run(["bash"])\n',
    "gan_goi_ham_thuong":   'm = f("subprocess")\nm.run(["bash"])\n',
    "eval_doi_tuong_khac":  'import subprocess as s\npage.eval("s.run([\'bash\'])")\n',
    "eval_tra_khong_phai_module": 'eval("1").run(["bash"])\n',
    "argv_noi_dau_khac":    'import subprocess\nsubprocess.run(["x"] + ["bash"])\n',
    "argv_trai_bien_dau":   'import subprocess\nsubprocess.run([*xs, "bash"])\n',
    "argv_noi_bien_dau":    'import subprocess, sys\nsubprocess.run(sys.argv[1:] + ["bash"])\n',
    "hang_phan_tram_dict_khac": 'import subprocess\nsubprocess.run(["%(a)s" % {"a": "sh"}])\n',
    # r24 — N89 chieu NGUOC: `set` NHIEU phan tu (thu tu khong xac dinh), `dict` mo dau bang `**x`.
    "argv_trai_set_nhieu":  'import subprocess\nsubprocess.run([*{"bash", "sh"}, "-c", "x"])\n',
    "argv_trai_dict_sao":   'import subprocess\nsubprocess.run([*{**x, "bash": 1}, "-c", "x"])\n',
    # r26 — N96/N97 (codex vong 20): Python TU CHOI loi goi truoc khi phong gi — bao la bao dong gia.
    "trung_doi_so_which":   'import shutil\nshutil.which("bash", cmd="sh")\n',
    "trung_doi_so_run":     'import subprocess\nsubprocess.run(["bash"], args=["sh"])\n',
    "trung_doi_so_async":   'import asyncio\nasyncio.create_subprocess_exec("bash", program="sh")\n',
    "eval_tai_cau_lenh":    'eval("import subprocess\\nsubprocess.run([\'bash\'])")\n',
    # r27 — N96b/N99 chieu NGUOC: tu khoa trung qua `**{…}` literal; chuoi chu thich KHONG phan
    # tich duoc (chu tu do); chu thich CUC BO trong ham khong duoc luu.
    "trung_doi_so_sao_sao": 'import subprocess\nsubprocess.run(["bash"], **{"args": ["sh"]})\n',
    "chu_thich_chuoi_tu_do": 'import subprocess\ndef f(x: "chạy bash (tự do"):\n    pass\n',
    "chu_thich_chuoi_cuc_bo": 'import subprocess\ndef f():\n    x: "subprocess.run([\'bash\'])" = 1\n',
    # r29 — N103 chieu NGUOC: `*` la CHU thuong, va so nguyen la GIA TRI chu khong phai do rong.
    "phan_tram_sao_la_chu":  'import subprocess\nsubprocess.run(["%s*" % 100000])\n',
    "phan_tram_sao_gia_tri": 'import subprocess\nsubprocess.run(["%*s" % (1, 100000)])\n',
    # r25 — LOP DA KHEP (quyet dinh chu kho, dieu kien dung cham lan BA o codex vong 19): cach viet
    # CO Y che giau cua nap dong/`exec` va argv trai. Ca nam CHAY BASH THAT; chung la NO CO TEN, va
    # chot nay giu cho loi khai ay DUNG — ai phu duoc thi chuyen sang `_HINH_DANG_PHU`.
    # r30 — LOP DA KHEP (chu kho, codex vong 24 — chu thich lan CHIN): chuoi chu thich duoc TINH RA
    # (`+`, `%`, `join`, f-string) — cach viet CO Y che giau, cung ly do lop r25. `get_type_hints` chay
    # bash that; cong KHONG phu. Ai phu duoc thi chuyen sang PHU.
    "khep_chu_thich_tinh_cong":  'import subprocess\ndef f(x: "subprocess" + ".run([\'bash\'])"):\n    pass\n',
    "khep_chu_thich_tinh_phan_tram": 'import subprocess\ndef f(x: "%s.run([\'bash\'])" % "subprocess"):\n    pass\n',
    "khep_chu_thich_tinh_join":  'import subprocess\ndef f(x: "".join(["subprocess.run(", "[\'bash\']", ")"])):\n    pass\n',
    "khep_chu_thich_tinh_fstring": 'import subprocess\ndef f(x: f"{\'subprocess\'}.run([\\"bash\\"])"):\n    pass\n',
    # r33 — N117 chieu NGUOC: `.eval` tren doi tuong KHAC khong phai `eval` dung san — khong phu thuoc.
    "eval_thuoc_tinh_khong_phu_thuoc": 'import importlib as il\nfor i in range(2):\n    if i:\n        a = page.eval("b")\n        a.run(["bash"])\n    b = il.import_module("subprocess")\n',
    # r35 — N119 chieu NGUOC: `executable=` khac bash thi `argv[0] == "bash"` chi la trang tri.
    "asyncio_exec_executable_khac": 'import asyncio\nasyncio.create_subprocess_exec("bash", "x", executable="/bin/echo")\n',
    # r36 — LOP DA KHEP mo rong (chu kho, codex vong 30): moi doi so cap qua `**` TRAI — ke ca `executable`
    # (asyncio lan Popen). Chay bash that; cong KHONG phu. Ai phu duoc thi chuyen sang PHU.
    "khep_executable_trai_asyncio": 'import asyncio\nasyncio.create_subprocess_exec("x", "-c", "true", **{"executable": "bash"})\n',
    "khep_executable_trai_popen":   'import subprocess\nsubprocess.run(["x", "-c", "true"], **{"executable": "bash"})\n',
    "khep_callee_dieu_kien": 'import builtins\n(builtins.exec if True else print)("import subprocess\\nsubprocess.run([\'bash\'])")\n',
    "khep_callee_ten_gap":  'import builtins\ngetattr(builtins, "ex" + "ec")("import subprocess\\nsubprocess.run([\'bash\'])")\n',
    "khep_nap_dong_trai":   'import importlib\nimportlib.import_module(*["subprocess"]).run(["bash"])\n',
    "khep_nap_dong_trai_kw": 'import importlib\nimportlib.import_module(**{"name": "subprocess"}).run(["bash"])\n',
    "khep_argv_trai_rong":  'import subprocess\nsubprocess.run([*{**{}, "bash": None}, "-c", "x"])\n',
    "eval_thuoc_tinh_ten_khac": 'import subprocess as s\ngetattr(page, "evaluate")("s.run([\'bash\'])")\n',
}

# r21 — N76: BAO DONG GIA CO CHU DICH. Moi hinh dang duoi day la mot meo CHE TEN (gan de, nhanh
# loai tru, `global`/`nonlocal` tu ham khac, walrus, lop cung ten…) ma r16..r20 da co MO PHONG thu
# tu thuc thi de khong bao. Sau lan lap thu SAU cua lop ay, chu kho chon DOI KIEN TRUC: bo giai ten
# KHONG theo thu tu, KHONG theo nhanh — co bat ky rang buoc `import` theo doi trong pham vi thang
# ⇒ BAO. Nen ca nhom nay PHAI bi bao: mot ban va quay ve mo phong thu tu se lam chung im lang, va
# `t33` (4) do dung dieu ay. Muon tat cong o mot cho nhu vay thi DOI TEN hoac khai MIEN TRU — ca
# hai de lai dau trong ma, con mot phep che ten thi khong.
_HINH_DANG_BAO_THAN_TRONG = {
    # r11 — N29 chieu BAT OAN. Ca ba deu la phep CHE hop le ma ban r10 van bao.
    "global_gan_che":  'import subprocess\ndef f():\n    global subprocess\n    subprocess = gia()\nsubprocess.run(["bash"])\n',
    "nonlocal_che":    'def o():\n    import subprocess\n    def i():\n        nonlocal subprocess\n        subprocess = gia()\n    subprocess.run(["bash"])\n',
    "walrus_comprehension_che": 'import subprocess\n[(subprocess := runner) for _ in [0]]\nsubprocess.run(["bash"])\n',
    # r15 — N40 chieu BAT OAN: `:=` trong TRUONG LUC DINH NGHIA che ten o pham vi CHUA.
    "walrus_mac_dinh_che": 'import subprocess\ndef f(x=(subprocess := runner)):\n    pass\nsubprocess.run(["bash"])\n',
    # r15 — N39 chieu BAT OAN: `global x; x = gia()` la mot phep che hop le.
    "global_roi_gan_che": 'import subprocess\ndef f():\n    global subprocess\n    subprocess = gia()\nsubprocess.run(["bash"])\n',
    "module_gan_TRUOC":    'import subprocess\nsubprocess = runner\nsubprocess.run(["bash"])\n',
    "lop_gan_TRUOC":       'import subprocess\nclass C:\n    subprocess = runner\n    subprocess.run(["bash"])\n',
    "ham_gan_TRUOC":       'def f():\n    import subprocess\n    subprocess = runner\n    subprocess.run(["bash"])\n',
    "ham_bao_ngoai_khong_loc": 'def o():\n    import subprocess\n    def i():\n        subprocess.run(["bash"])\n    subprocess = runner\n',
    "module_gan_trong_if":  'import subprocess\nif x:\n    subprocess = runner\nsubprocess.run(["bash"])\n',
    # r17 — N53 chieu NGUOC: hai rang buoc HOAN TAT cung mot cho ⇒ van mo ho.
    "gan_day_chuyen_che":   'import subprocess\nsubprocess = other = runner\nsubprocess.run(["bash"])\n',
    "os_bi_che":            'import os\nos = runner\nos.system("bash")\n',
    # r18 — N60 chieu NGUOC: goi SAU lop cung ten thi ten da la LOP.
    "lop_cung_ten_goi_sau": 'import subprocess\nclass subprocess:\n    x = 1\nsubprocess.run(["bash"])\n',
    # r19 — N66 chieu NGUOC.
    "pty_bi_che":          'import pty\npty = x\npty.spawn(["bash"])\n',
    # r20 — N72 chieu NGUOC: NHANH LOAI TRU — chon nhanh sau thi nhanh truoc KHONG chay, va
    # ten cuc bo la `UnboundLocalError` / `NameError`. Do tren 3.12.3 THAT: khong in gi.
    "except_anh_em":       'def f():\n    try:\n        pass\n    except ValueError:\n        import subprocess\n    except KeyError:\n        subprocess.run(["bash"])\n',
    "match_case_anh_em":   'def f(x):\n    match x:\n        case 1:\n            import subprocess\n        case _:\n            subprocess.run(["bash"])\n',
    "if_else_anh_em":      'def f(x):\n    if x:\n        import subprocess\n    else:\n        subprocess.run(["bash"])\n',
    "except_voi_else":     'def f():\n    try:\n        pass\n    except E:\n        import subprocess\n    else:\n        subprocess.run(["bash"])\n',
    "module_except_anh_em": 'try:\n    pass\nexcept ValueError:\n    import subprocess\nexcept KeyError:\n    subprocess.run(["bash"])\n',
    # `finally` luon chay ⇒ phep che trong no thang `import` truoc do.
    "finally_che_sau":     'def f():\n    import subprocess\n    try:\n        pass\n    finally:\n        subprocess = None\n    subprocess.run(["bash"])\n',
    # than lop / list comprehension CHAY NGAY ⇒ `import` o duoi chua xay ra (`NameError`).
    "lop_goi_import_sau":  'class C:\n    subprocess.run(["bash"])\nimport subprocess\n',
    "listcomp_goi_import_sau": 'x = [subprocess.run(["bash"]) for _ in [0]]\nimport subprocess\n',
    # than lop: nhanh `import` va module CHE bang thu khac ⇒ hai gia tri ⇒ mo ho ⇒ khong bao.
    "lop_nhanh_import_module_che": 'subprocess = None\nclass C:\n    if x:\n        import subprocess\n    subprocess.run(["bash"])\n',
    # r21 — vong 15, G1/G2: thu tu gan DICH va `match` gan truoc `guard` — CHAY THAT thi nem
    # `AttributeError`, nhung day dung la loai mo phong ma N76 da bo.
    "dich_gan_theo_thu_tu": 'import subprocess\nx = {}\nsubprocess, x[subprocess.run(["bash"])] = (object(), 1)\n',
    "match_bat_truoc_guard": 'import subprocess\nmatch object():\n    case subprocess if subprocess.run(["bash"]):\n        pass\n',
    # r28 — LOP DA KHEP (chu kho, codex vong 22): tham so cap TRUNG ma N96/N96b chua nhan — Python TU
    # CHOI chay (TypeError), cong BAO THUA co ten; va chuoi trong `Literal`/`Annotated` la DU LIEU ma N99
    # van quet — BAO THUA CO CHU DICH kieu N76.
    "khep_trung_tu_khoa_sao_sao_run":   'import subprocess\nsubprocess.run(args=["bash"], **{"args": ["sh"]})\n',
    "khep_trung_tu_khoa_sao_sao_which": 'import shutil\nshutil.which(cmd="bash", **{"cmd": "sh"})\n',
    "khep_literal_du_lieu":   'import subprocess\nfrom typing import Literal\ndef f(x: Literal["subprocess.run([\'bash\'])"]):\n    pass\n',
    # r29 — LOP DA KHEP mo rong (chu kho, codex vong 23): moi loi goi Python TU CHOI vi sai quy uoc
    # truyen doi so — `posix_spawnp` chi nhan VI TRI.
    "khep_posix_spawnp_tu_khoa": 'import os\nos.posix_spawnp(path="bash", argv=["bash"], env={})\n',
    # r35 — LOP DA KHEP mo rong (chu kho, codex vong 29): `__import__(…, level≠0)` la nhap TUONG DOI —
    # ngoai package Python nem `ImportError`, trong package no nap module CUNG TEN cua package. Bao thua co ten.
    "khep_import_tuong_doi_vi_tri": '__import__("subprocess", globals(), locals(), (), 1).run(["bash"])\n',
    "khep_import_tuong_doi_tu_khoa": '__import__("subprocess", level=1).run(["bash"])\n',
    "khep_annotated_du_lieu": 'import subprocess\nfrom typing import Annotated\ndef f(x: Annotated[int, "subprocess.run([\'bash\'])"]):\n    pass\n',
}
if sys.version_info >= (3, 12):
    # r29 — LOP DA KHEP (chu kho, codex vong 23): chu thich cua ham generic THAY tham so kieu tren 3.12
    # (khong `__future__`) nen Python nem `AttributeError` — cong BAO THUA CO CHU DICH. Chi them khi trinh
    # thong dich parse duoc PEP 695 (CI ghim 3.12). Ghim nay tung nam o `t50` va do do giet THEM hai dot
    # bien cua `t33` (ban kinh 2/53: moi phep do tren hinh dang nay deu cham bo duyet chu thich) — nen no
    # song o day, cung ca voi dot bien dich.
    _HINH_DANG_BAO_THAN_TRONG["khep_chu_thich_thay_tham_so_kieu"] = (
        'import subprocess\ndef f[subprocess](x: subprocess.run(["bash"])):\n    pass\n')


@ca
def t33_do_phu_cua_cong_do_duoc_THEO_HINH_DANG():
    """Mỗi hình dạng lời gọi một khẳng định riêng — và docstring phải khai ĐÚNG phạm vi.

    SINH TỪ CROSS-REVIEW trên `05ec2eb5` (finding F1). Bản cũ khai *"số dòng của MỌI lời gọi
    phân giải `bash` theo TÊN"*. Reviewer cho ăn 12 hình dạng: **BẮT 3 / LỌT 9**. Phiên này
    đo lại và ra **y hệt** — không nhận lời khai, đo lại.

    Hình dạng lọt đáng kể nhất là `shutil.which("bash.exe")`: đúng CÁCH VIẾT Windows của đúng
    khuyết tật Windows mà packet này sinh ra để chặn, và `ung_vien()` ngay trong `bash_nen.py`
    cũng dùng `("bash.exe", "bash")`. `t25` chỉ đo ĐÚNG MỘT hình dạng, nên độ phủ chưa từng
    được đo — *"nghĩ ra được phép thử mà không chạy thì phép thử ấy không tồn tại"*.

    BA CHỐT:
      (1) mọi hình dạng ĐƯỢC KHAI LÀ PHỦ đều bị bắt;
      (2) hình dạng KHÔNG phủ vẫn lọt — và docstring phải NÓI RA. Chốt này chống việc khai
          rộng hơn phép đo: nếu ai mở rộng hàm mà quên sửa docstring, (2) không bắt được,
          nhưng (3) bắt;
      (3) docstring KHÔNG được chứa chữ "mọi lời gọi" — lời khai phải khớp phép đo.
    """
    # NAP TU `BASH_NEN` chu khong dung `bash_nen` da import: bo dot bien tro `BASH_NEN` sang
    # mot ban sao da mutate, ma module da nap thi khong doi theo. Do la ly do
    # `t33_bo_bash_exe` SONG SOT o luot do dau — dung bay da mac o `t29`/`t31`/`t32`.
    import runpy
    _m = runpy.run_path(str(BASH_NEN))
    _loi_goi_tran = _m["_loi_goi_tran"]

    # N74 (r20) — MỖI hình dạng phải TRẢ VỀ một danh sách. Bộ quét NÉM thì ca đỏ qua `bang`
    # và nói tên ngoại lệ, chứ không chết ngoài `bang` — chết ngoài `bang` là TÍN DỤNG GIẢ
    # cho mọi đột biến làm bộ gấp hằng ném (bài học `TinHieuChotCa`).
    def _do(than):
        try:
            return _loi_goi_tran(than)
        except Exception as e:           # noqa: BLE001 — đổi thành phép đo, có chủ đích
            return f"NÉM {type(e).__name__}: {e}"

    for ten, than in _HINH_DANG_PHU.items():
        kq = _do(than)
        bang(isinstance(kq, list) and bool(kq),
             f"(1) hình dạng `{ten}` ĐƯỢC KHAI là phủ mà cổng KHÔNG bắt ({kq!r}):\n{than}")
    for ten, than in _HINH_DANG_KHONG_PHU.items():
        kq = _do(than)
        bang(kq == [],
             f"(2) hình dạng `{ten}` được khai là KHÔNG phủ mà cổng lại bắt ({kq!r}) — nếu đã "
             f"mở rộng được thì phải sửa docstring VÀ chuyển nó sang `_HINH_DANG_PHU`:\n{than}")
    # (4) N76 (r21) — BÁO ĐỘNG GIẢ CÓ CHỦ ĐÍCH: mọi mẹo che tên PHẢI bị báo. Một bản vá quay
    # về mô phỏng thứ tự thực thi sẽ làm nhóm này im lặng, và chốt này đỏ.
    for ten, than in _HINH_DANG_BAO_THAN_TRONG.items():
        kq = _do(than)
        bang(isinstance(kq, list) and bool(kq),
             f"(4) mẹo che tên `{ten}` KHÔNG bị báo ({kq!r}) — N76 đã bỏ mô phỏng thứ tự; tắt "
             f"cổng bằng cách che tên là đúng thứ không được phép:\n{than}")
    # (1b) `executable=` GHI ĐÈ, không cộng dồn: hai tên `bash` trong MỘT lời gọi là MỘT bản ghi.
    # Chốt riêng vì (1) chỉ hỏi "có bắt không" — hai bản ghi cũng qua (1), và một mục miễn trừ
    # khai theo SỐ LẦN sẽ lệch oan.
    mot = _loi_goi_tran(_HINH_DANG_MOT_BAN_GHI)
    bang(len(mot) == 1,
         f"(1b) `run([\"bash\"], executable=\"bash\")` phải là ĐÚNG MỘT bản ghi, đo được {mot}")
    # (1c) N74 — phép KHUẾCH ĐẠI vượt ngân sách KHÔNG được chạy thử, cũng KHÔNG được coi là
    # "không phải bash": nó phải NÉM `_VuotNganSach` để `quet` ra `KHONG_DO_DUOC`. Độ rộng 5000
    # vừa đủ vượt ngân sách 4096 mà vẫn rẻ nếu một đột biến lỡ cho nó chạy.
    kq_ns = _do('import subprocess\nsubprocess.run(["%05000d" % 1])\n')
    bang(isinstance(kq_ns, str) and "_VuotNganSach" in kq_ns,
         f"(1c) `\"%05000d\" % 1` phải NÉM `_VuotNganSach` (fail-close), đo được {kq_ns!r}")
    # (1e) N78b/N78c (r22, H5/H6 vòng 16) — số độ rộng QUÁ DÀI (vượt giới hạn chuyển chuỗi của
    # `int`) và `join` TÁI DÙNG dấu phân cách đều phải NÉM `_VuotNganSach` TRƯỚC khi dựng.
    for nhan, than_ns in (("số 5000 chữ số", 'import subprocess\nsubprocess.run(["%' + "9" * 5000
                                             + 's" % "x"])\n'),
                          ("join khuếch đại", 'import subprocess\nsubprocess.run([("' + "a" * 100
                                              + '").join([' + ",".join(['""'] * 100) + '])])\n')):
        kq_e = _do(than_ns)
        bang(isinstance(kq_e, str) and "_VuotNganSach" in kq_e,
             f"(1e) {nhan} phải NÉM `_VuotNganSach` trước khi dựng, đo được {kq_e!r}")
    # (1d) N78 (r21, G5 vòng 15) — ngân sách là TỔNG: hai ô 4096 mỗi ô đều hợp lệ riêng lẻ.
    kq_td = _do('import subprocess\nsubprocess.run(["%4096s%4096s" % ("", "")])\n')
    bang(isinstance(kq_td, str) and "_VuotNganSach" in kq_td,
         f"(1d) `\"%4096s%4096s\"` phải NÉM `_VuotNganSach` (ngân sách cộng dồn), đo được {kq_td!r}")
    # (1f) N84 (r23, F5 vòng 17) — biểu thức lồng SÂU hợp lệ phải QUÉT ĐƯỢC, không ném
    # `RecursionError`. 2000 tầng: gấp đôi giới hạn đệ quy mặc định, và DƯỚI trần của chính
    # `ast.parse` trên MỌI bản đã đo — đo được ~2984 trên 3.11, ~9991 trên 3.12. Bản đầu dùng 3000
    # và đỏ ở NỀN trên 3.11 vì `ast.parse` ném trước khi cổng kịp duyệt; tiền đề dưới đây tách hai
    # nguyên nhân ấy ra, để chốt không bao giờ đổ cho cổng một giới hạn của trình thông dịch.
    than_sau = "import subprocess\nx = " + "+".join(["1"] * 2000) + '\nsubprocess.run(["bash"])\n'
    try:
        import ast as _ast_tien_de
        _ast_tien_de.parse(than_sau)
    except RecursionError:
        bang(False, "(1f) TIỀN ĐỀ: chính `ast.parse` của trình thông dịch này không dựng nổi cây "
                    "2000 tầng — đây là giới hạn của Python, không phải của cổng; hạ độ sâu của chốt")
    kq_sau = _do(than_sau)
    bang(kq_sau == [(3, 0)],
         f"(1f) biểu thức 2000 tầng phải quét ĐƯỢC và bắt đúng lời gọi, đo được {kq_sau!r}")
    # (1g) N83 (r23, F6 vòng 17) — tải `exec` HẰNG không phân tích được ⇒ NÉM (fail-close), không
    # lặng lẽ bỏ qua: cùng sự kiện ở tệp ngoài cho `KHONG_DO_DUOC`.
    kq_hong = _do('exec("import subprocess\\nsubprocess.run([")\n')
    bang(isinstance(kq_hong, str) and "SyntaxError" in kq_hong,
         f"(1g) tải `exec` hằng hỏng phải NÉM `SyntaxError`, đo được {kq_hong!r}")
    # (1h) `exec` hằng lồng QUÁ `_SAU_EXEC` tầng ⇒ NÉM `_VuotNganSach`, không thôi quét trong im lặng.
    tai4 = "import subprocess\nsubprocess.run(['bash'])"
    for _ in range(4):
        tai4 = "exec(" + repr(tai4) + ")"
    kq_long = _do(tai4 + "\n")
    bang(isinstance(kq_long, str) and "_VuotNganSach" in kq_long,
         f"(1h) `exec` lồng 4 tầng phải NÉM `_VuotNganSach`, đo được {kq_long!r}")
    # (1i) N88 (r24, codex vòng 18) — HẾT độ sâu gấp hằng mà biểu thức vẫn có thể là hằng ⇒ NÉM
    # `_VuotNganSach` (fail-close), không coi là "không phải bash". Hai đường: bộ gấp (chín lớp `%`)
    # và bộ lọc rẻ (chín lớp `str(…)` — nó phải CHO QUA để luật thật được hỏi và ném).
    for nhan, than_ht in (("chín lớp `%`", 'import subprocess\nsubprocess.run([' + "'%s' % (" * 9
                                          + "'bash'" + ")" * 9 + '])\n'),
                          ("chín lớp `str`", 'import shutil\nshutil.which(' + "str(" * 9 + '"bash"'
                                            + ")" * 9 + ')\n')):
        kq_ht = _do(than_ht)
        bang(isinstance(kq_ht, str) and "_VuotNganSach" in kq_ht,
             f"(1i) {nhan}: hết độ sâu gấp hằng phải NÉM `_VuotNganSach`, đo được {kq_ht!r}")
    # (1j) N93 (r25, codex vòng 19) — ngân sách phép nối tính TRONG LÚC gấp: 1000 vế `("%4096s" % "")`
    # phải NÉM `_VuotNganSach` mà bộ gấp KHÔNG dựng các vế sau ngưỡng. Đo RIÊNG bộ gấp trên nút đã phân
    # tích sẵn — bản đầu của chốt này đo cả `_loi_goi_tran` và `tracemalloc` tính luôn cây AST (~2,5 MB),
    # tức đo trình phân tích chứ không đo bản vá. Đo bản r24 trên đúng nút này: đỉnh ~4,2 MB; trần 256 KB.
    import ast as _ast_noi
    import tracemalloc
    nut_noi = _ast_noi.parse(" + ".join(['("%4096s" % "")'] * 1000), mode="eval").body
    tracemalloc.start()
    try:
        try:
            _m["_gia_tri_hang"](nut_noi)
            kq_noi = "không ném"
        except Exception as e:           # noqa: BLE001 — đổi thành phép đo
            kq_noi = type(e).__name__
        _, dinh_noi = tracemalloc.get_traced_memory()
    finally:
        tracemalloc.stop()
    bang(kq_noi == "_VuotNganSach" and dinh_noi < 256 * 1024,
         f"(1j) bộ gấp phép nối 1000 vế phải NÉM sớm (đỉnh < 256 KB), đo được {kq_noi}, "
         f"đỉnh {dinh_noi} byte")
    # (1k) N93b (r26, codex vòng 20) — cùng phép đo (1j) cho `"".join([...])`: bản r25 dựng ~4 MB.
    nut_join = _ast_noi.parse('"".join([' + ",".join(['("%4096s" % "")'] * 1000) + '])',
                              mode="eval").body
    tracemalloc.start()
    try:
        try:
            _m["_gia_tri_hang"](nut_join)
            kq_join = "không ném"
        except Exception as e:           # noqa: BLE001 — đổi thành phép đo
            kq_join = type(e).__name__
        _, dinh_join = tracemalloc.get_traced_memory()
    finally:
        tracemalloc.stop()
    bang(kq_join == "_VuotNganSach" and dinh_join < 256 * 1024,
         f"(1k) bộ gấp `join` 1000 phần tử phải NÉM sớm (đỉnh < 256 KB), đo được {kq_join}, "
         f"đỉnh {dinh_join} byte")
    # (1l) N99b (r28, codex vòng 22) — chú thích chuỗi ĐÚNG trần vẫn quét được; VƯỢT trần một ký tự
    # thì NÉM `_VuotNganSach`, không bỏ qua im lặng.
    loi = "subprocess.run(['bash'])"
    for dai, mong in ((100_000, "bat"), (100_001, "nem")):
        than_ct = ("import subprocess\ndef f(x: " + repr(loi + " " * (dai - len(loi)))
                   + "):\n    pass\n")
        kq_ct = _do(than_ct)
        ok = (isinstance(kq_ct, list) and bool(kq_ct)) if mong == "bat" else \
            (isinstance(kq_ct, str) and "_VuotNganSach" in kq_ct)
        bang(ok, f"(1l) chú thích chuỗi dài {dai}: mong {mong}, đo được {str(kq_ct)[:120]!r}")
    # (1m) N102/N104 (r29, codex vòng 23) — tải `exec` ĐÚNG trần vẫn quét, VƯỢT trần một ký tự thì NÉM,
    # cho cả `str` lẫn `bytes`; và hai lời gọi trong MỘT chú thích chuỗi là HAI bản ghi.
    tai_goc = "import subprocess\nsubprocess.run(['bash'])\n#"
    for dai, mong in ((100_000, "bat"), (100_001, "nem")):
        tai_n = tai_goc + "x" * (dai - len(tai_goc))
        for nhan_t, bieu in (("str", repr(tai_n)), ("bytes", "b" + repr(tai_n))):
            kq_t = _do("exec(" + bieu + ")\n")
            ok = (isinstance(kq_t, list) and bool(kq_t)) if mong == "bat" else \
                (isinstance(kq_t, str) and "_VuotNganSach" in kq_t)
            bang(ok, f"(1m) tải `exec` {nhan_t} dài {dai}: mong {mong}, đo được {str(kq_t)[:120]!r}")
    hai = _do("import subprocess\ndef f(x: \"(subprocess.run(['bash']), subprocess.run(['bash']))\"):\n"
              "    pass\n")
    bang(isinstance(hai, list) and len(hai) == 2,
         f"(1m) hai lời gọi trong MỘT chú thích chuỗi phải là HAI bản ghi, đo được {hai!r}")
    for mau_so in ('"%.5000f" % 1', '"%.*f" % (5000, 1)', '"%*.*s" % (5000, 1, "x")'):
        kq_so = _do('import subprocess\nsubprocess.run([' + mau_so + '])\n')
        bang(isinstance(kq_so, str) and "_VuotNganSach" in kq_so,
             f"(1m) N107: {mau_so} — độ rộng hay độ chính xác SỐ vẫn khuếch đại, phải NÉM; đo được {kq_so!r}")
    # N108 (r30, codex vòng 24) — mỗi lời gọi TRONG một tải `exec`/`eval` hằng là một bản ghi.
    for mau_tai, mong_so in (
            ('exec("import subprocess\\nsubprocess.run([\'bash\'])")\n', 1),
            ('exec("import subprocess\\nsubprocess.run([\'bash\'])\\nsubprocess.run([\'bash\'])")\n', 2),
            ('import subprocess\neval("(subprocess.run([\'bash\']),\\n subprocess.run([\'bash\']))")\n', 2)):
        kq_tai = _do(mau_tai)
        bang(isinstance(kq_tai, list) and len(kq_tai) == mong_so,
             f"(1m) N108: tải {mau_tai!r} chứa {mong_so} lời gọi phải ra {mong_so} bản ghi, đo được {kq_tai!r}")
    # N109 (r30, codex vòng 24) — chuỗi n bí danh NẠP ĐỘNG giải TUYẾN TÍNH: đếm số lần giải (không đo
    # giờ — giờ máy không phải phép đo ổn định). Kèm hai đối chứng: vòng TRÒN phải dừng và không báo;
    # nạp ở module, dùng trong hàm phải vẫn bắt.
    _g_bn = _loi_goi_tran.__globals__     # CHÍNH mô-đun mà ca đang đo (bản đột biến nếu có)
    n_chuoi = 400
    chuoi = ('a0 = __import__("importlib")\n'
             + "".join(f'a{i} = a{i - 1}.import_module("importlib")\n' for i in range(1, n_chuoi))
             + f'c = a{n_chuoi - 1}.import_module("subprocess")\nc.run(["bash"])\n')
    d0 = _g_bn["_DEM_GIAI_DONG"]
    kq_chuoi = _do(chuoi)
    so_giai = _g_bn["_DEM_GIAI_DONG"] - d0
    bang(kq_chuoi == [(n_chuoi + 2, 0)] and so_giai <= 3 * n_chuoi,
         f"(1m) N109: chuỗi {n_chuoi} bí danh phải bắt đúng và giải ≤ {3 * n_chuoi} lần, đo được "
         f"{kq_chuoi!r} sau {so_giai} lần giải")
    bang(_do('a = b.import_module("importlib")\nb = a.import_module("subprocess")\n'
                               'b.run(["bash"])\n') == [],
         "(1m) N109: vòng TRÒN bí danh không có `__import__` thật phải DỪNG và không báo")
    kq_pv = _do('il = __import__("importlib")\ndef f():\n    m = il.import_module("subprocess")\n'
                               '    m.run(["bash"])\n')
    bang(isinstance(kq_pv, list) and [d for d, _c in kq_pv] == [4],
         "(1m) N109: nạp ở module, giải trong hàm (qua ranh giới phạm vi) phải vẫn bắt")
    # N111 (r31, codex vòng 25) — n hàm ĐỘC LẬP, mỗi hàm một chuỗi nạp động hai tầng cùng tên `x`: giải
    # một `x` không được xếp lại mục của các hàm khác. Đếm số lần giải, phải TUYẾN TÍNH theo số mục.
    n_ham = 400
    nhieu_ham = "".join(f'def f{i}():\n    x = __import__("importlib")\n    y = x.import_module("subprocess")\n'
                        for i in range(n_ham))
    # Kèm MỘT lời gọi bash thật: không có hằng `bash` thì cổng thoát trước khi dựng bảng phạm vi.
    nhieu_ham += 'import subprocess\nsubprocess.run(["bash"])\n'
    d1 = _g_bn["_DEM_GIAI_DONG"]
    _do(nhieu_ham)
    so_giai_ham = _g_bn["_DEM_GIAI_DONG"] - d1
    bang(so_giai_ham <= 3 * 2 * n_ham,
         f"(1m) N111: {n_ham} hàm độc lập (mỗi hàm 2 mục nạp động) phải giải ≤ {6 * n_ham} lần, đo được "
         f"{so_giai_ham}")
    # N115 (r32, codex vòng 26) — tải KHÔNG phải hằng (`page.eval(x)`) không có phụ thuộc: n mục như thế
    # ĐỨNG TRƯỚC một chuỗi n bí danh không được bị xếp lại theo mỗi bí danh (r31: 800 + 800 ⇒ 642 401).
    n_dd = 400
    dai_dien = ("".join(f"p{i} = page.eval(x)\n" for i in range(n_dd)) + 'a0 = __import__("importlib")\n'
                + "".join(f'a{i} = a{i - 1}.import_module("importlib")\n' for i in range(1, n_dd))
                + f'c = a{n_dd - 1}.import_module("subprocess")\nc.run(["bash"])\n')
    d2 = _g_bn["_DEM_GIAI_DONG"]
    kq_dd = _do(dai_dien)
    so_giai_dd = _g_bn["_DEM_GIAI_DONG"] - d2
    bang(isinstance(kq_dd, list) and len(kq_dd) == 1 and so_giai_dd <= 3 * 2 * n_dd,
         f"(1m) N115: {n_dd} `page.eval(x)` + chuỗi {n_dd} bí danh phải bắt đúng và giải ≤ {6 * n_dd} lần, "
         f"đo được {kq_dd!r} sau {so_giai_dd} lần giải")
    # N115 — `.eval` trên một đối tượng KHÁC không phải `eval` dựng sẵn: tải dài của nó không được chạm
    # trần `exec` (r31 NÉM cả tệp), và lời gọi bash sau đó phải vẫn bị bắt. (Chốt riêng thay vì một mục
    # `_HINH_DANG_PHU` để các bảng hình dạng giữ dạng LITERAL thuần.)
    kq_pe = _do('result = page.eval(' + repr("x" * 100_001) + ')\nimport subprocess\nsubprocess.run(["bash"])\n')
    bang(isinstance(kq_pe, list) and [d for d, _c in kq_pe] == [3],
         f"(1m) N115: `page.eval(<100 001 ký tự>)` rồi `subprocess.run(['bash'])` phải ra dòng 3, đo được "
         f"{str(kq_pe)[:200]!r}")
    # (1n) N110 (r31, chủ kho: đóng theo BẢNG) — bảng kiểu chuyển đổi của cổng được đo bằng CHÍNH `%` của
    # Python: mọi chữ cái mà `%` của `str` hay `bytes` nhận phải có trong bảng; kiểu TRẦN thì độ chính xác
    # 5000 KHÔNG dựng chuỗi dài; kiểu KHUẾCH ĐẠI thì có cách viết (có/không `#`) dựng ≥ 5000 ký tự.
    tran, kd = _g_bn["_KIEU_TRAN"], _g_bn["_KIEU_KHUECH_DAI"]
    for ch in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ":
        nhan = []
        for loai, mau_ch, gia in (("str", "%" + ch, None), ("bytes", ("%" + ch).encode(), None)):
            for thu in (1, 1.0, "x", b"x"):
                try:
                    mau_ch % thu
                except (ValueError, TypeError):
                    continue
                nhan.append((loai, thu))
                break
        if not nhan:
            continue
        bang(ch in tran or ch in kd, f"(1n) N110: `%{ch}` được Python nhận ({nhan}) mà KHÔNG có trong bảng")
        dai = 0
        for loai, thu in nhan:
            for co in ("", "#"):
                mau_ch = "%" + co + ".5000" + ch
                try:
                    dai = max(dai, len((mau_ch.encode() if loai == "bytes" else mau_ch) % thu))
                except (ValueError, TypeError):
                    pass
        if ch in tran:
            bang(dai < 100, f"(1n) N110: `%{ch}` khai là TRẦN mà độ chính xác 5000 dựng {dai} ký tự")
        elif ch in kd:
            bang(dai >= 5000, f"(1n) N110: `%{ch}` khai là KHUẾCH ĐẠI mà độ chính xác 5000 chỉ dựng {dai}")
    # (1o) N116 (r32, chủ kho: "đóng bằng phép đo SAI PHÂN") — ngân sách `%` của cổng so với độ dài THẬT
    # mà `%` của Python dựng, trên một LƯỚI: cờ × độ rộng (tĩnh/`*`, kể cả ÂM) × độ chính xác (tĩnh/`*`,
    # kể cả ÂM) × mọi kiểu trong bảng × str/bytes. Hai chiều: thật > ngân sách sản phẩm ⇒ cổng PHẢI NÉM
    # (không lọt); thật ≤ `_CHAT` ký tự ⇒ cổng KHÔNG được NÉM (không báo oan cả cây). "Thật" là độ dài LỚN NHẤT
    # trên một TẬP giá trị của kiểu ấy: `%.5000g` ra 3 ký tự với 1.5 mà hơn 5000 với 1/3 — cổng không
    # biết giá trị sẽ là gì trong mọi trường hợp, nên chỉ bị đòi chặt khi KHÔNG giá trị nào khuếch đại.
    # N120 (r35, chủ kho: "siết phép đo") — ngưỡng CHẶT nâng 64 → 1000: bản r32–r34 chỉ đòi "thật ≤ 64 ⇒ không
    # NÉM", nên `%.5000g` (thật ≤ ~760 với mọi `double`) lọt qua phép đo dù cổng NÉM oan — codex vòng 29 bắt.
    # Ở ngưỡng 1000, mọi báo thừa cùng hình dạng lộ ra trong MỘT lượt đo thay vì từng vòng review.
    _CHAT = 1000
    kiem_ns = _g_bn["_kiem_ngan_sach_dinh_dang"]
    dai_g = max(len(("%" + c + ".5000" + k) % v) for c in ("", "+", " ") for k in "gG"
                for v in (5e-324, -5e-324, 2.2250738585072014e-308, 1e-300, 1 / 3, 1e300, 1.7976931348623157e308))
    bang(dai_g <= _g_bn["_TRAN_CHU_SO_G"],
         f"(1o) N120: `%.5000g` không `#` dựng tới {dai_g} ký tự > trần {_g_bn['_TRAN_CHU_SO_G']} của cổng")
    vuot = _g_bn["_VuotNganSach"]
    tran_ns = _g_bn["_NGAN_SACH_DINH_DANG"]
    gia_tri = {"s": ("x",), "r": ("x",), "a": ("x",), "c": (65,), "b": (b"x",)}
    gia_so = {"e": (1.5, 1 / 3, 1e300, -1e-300, 5e-324, 2.2250738585072014e-308), "i": (7, -7, 10 ** 30)}
    lech = []
    so_o = 0
    for kieu in sorted(_g_bn["_KIEU_TRAN"] | _g_bn["_KIEU_KHUECH_DAI"]):
        for la_bytes in (False, True):
            for co in ("", "#", "-", "0"):
                for rong in ("", "5", "5000", "*"):
                    for cx in ("", ".5", ".5000", ".*"):
                        for r_dong in ((-5000, -5, 0, 5, 5000) if rong == "*" else (None,)):
                            for c_dong in ((-5000, -5, 0, 5, 5000) if cx == ".*" else (None,)):
                                mau_o = "%" + co + rong + cx + kieu
                                if la_bytes:
                                    mau_o = mau_o.encode()
                                cac_gt = gia_tri.get(kieu) or gia_so["e" if kieu in "eEfFgG" else "i"]
                                that = -1
                                for gt in cac_gt:
                                    if la_bytes and isinstance(gt, str):
                                        gt = gt.encode()
                                    doi_o = tuple(x for x in (r_dong, c_dong) if x is not None) + (gt,)
                                    doi_o = doi_o if len(doi_o) > 1 else doi_o[0]
                                    try:
                                        that = max(that, len(mau_o % doi_o))
                                    except (ValueError, TypeError, OverflowError):
                                        continue
                                    try:
                                        kiem_ns(mau_o, doi_o)
                                        nem = False
                                    except vuot:
                                        nem = True
                                if that < 0:
                                    continue
                                so_o += 1
                                if (that > tran_ns and not nem) or (that <= _CHAT and nem):
                                    lech.append((mau_o, doi_o, that, nem))
    # N118 (r34, codex vòng 28) — lưới mở sang KHOÁ ÁNH XẠ: khoá thường, rỗng, lồng ngoặc (`(a)`, `a(b)c`,
    # `((x))`), kèm cờ × độ rộng/độ chính xác TĨNH (Python cấm `*` cùng khoá ánh xạ) × mọi kiểu × str/bytes.
    # Và chiều khoá HỎNG: không khép ngoặc ⇒ Python ném `ValueError` trước khi dựng gì ⇒ cổng không được NÉM.
    so_khoa = 0
    for khoa in ("a", "", "(a)", "a(b)c", "((x))"):
        for kieu in sorted(_g_bn["_KIEU_TRAN"] | _g_bn["_KIEU_KHUECH_DAI"]):
            for la_bytes in (False, True):
                for co in ("", "#", "-"):
                    for rong in ("", "5", "5000"):
                        for cx in ("", ".5", ".5000"):
                            mau_o = "%(" + khoa + ")" + co + rong + cx + kieu
                            k_o = khoa
                            if la_bytes:
                                mau_o, k_o = mau_o.encode(), khoa.encode()
                            cac_gt = gia_tri.get(kieu) or gia_so["e" if kieu in "eEfFgG" else "i"]
                            that, nem = -1, False
                            for gt in cac_gt:
                                if la_bytes and isinstance(gt, str):
                                    gt = gt.encode()
                                try:
                                    that = max(that, len(mau_o % {k_o: gt}))
                                except (ValueError, TypeError, OverflowError):
                                    continue
                                try:
                                    kiem_ns(mau_o, {k_o: gt})
                                    nem = False
                                except vuot:
                                    nem = True
                            if that < 0:
                                continue
                            so_o += 1
                            so_khoa += 1
                            if (that > tran_ns and not nem) or (that <= _CHAT and nem):
                                lech.append((mau_o, khoa, that, nem))
    for hong in ("%((a)s", "%(a", "%(a(b)s"):
        try:
            kiem_ns(hong, {"a": "x"})
        except vuot:
            lech.append((hong, "khoá hỏng", "Python ném ValueError", True))
    bang(so_o > 1000 and so_khoa > 500 and not lech,
         f"(1o) N116/N118: {len(lech)} ô lệch trên {so_o} ô của lưới sai phân ({so_khoa} ô khoá ánh xạ) "
         f"(mẫu, đối/khoá, dài thật, cổng ném): {lech[:6]}")
    # LỚP ĐÃ KHÉP (r36, chủ kho — ngân sách `%` lần BẢY, codex vòng 30): độ rộng + độ chính xác của MỘT chuyển
    # đổi CHỒNG nhau mà cổng CỘNG — `"%3000.3000f" % 1.0` dài 3002 mà cổng NÉM. Báo thừa FAIL-CLOSE có tên
    # (KHONG_DO_DUOC, không lọt); ghim để ai làm cận sát hơn phải chủ động đổi dòng này.
    kq_chong = _do('import subprocess\nsubprocess.run(["%3000.3000f" % 1.0])\n')
    bang(isinstance(kq_chong, str) and "_VuotNganSach" in kq_chong,
         f"(1m) LỚP ĐÃ KHÉP r36: `%3000.3000f` là báo thừa fail-close CÓ TÊN (cổng NÉM), đo được {kq_chong!r}")
    kq_sao = _do('import subprocess\nsubprocess.run(["%*s" % (5000, "x")])\n')
    bang(isinstance(kq_sao, str) and "_VuotNganSach" in kq_sao,
         f"(1m) `%*s` với độ rộng 5000 vẫn phải NÉM (N103 chỉ bỏ số KHÔNG phải độ rộng), đo được "
         f"{kq_sao!r}")
    tai_lieu = (_loi_goi_tran.__doc__ or "")
    tom_tat = tai_lieu.strip().splitlines()[0].lower() if tai_lieu.strip() else ""
    # ĐO DÒNG TÓM TẮT, KHÔNG ĐO CẢ THÂN. Bản đầu của chốt này cấm chuỗi "mọi lời gọi" trên
    # TOÀN docstring — và nó ĐỎ oan ngay, vì docstring mới TRÍCH DẪN chính câu cũ để giải
    # thích vì sao câu ấy sai. Đúng bẫy `CLAUDE.md` đã ghi: dấu bỏ-qua-CI trong commit
    # message vẫn kích hoạt KỂ CẢ khi đang trích dẫn để giải thích; nháy ngược không phải
    # hàng rào. Lời KHAI của một hàm nằm ở DÒNG TÓM TẮT; phần sau là diễn giải.
    bang("mọi lời gọi" not in tom_tat,
         f"(3) DÒNG TÓM TẮT của docstring lại khai `mọi lời gọi` — lời khai RỘNG HƠN phép đo, "
         f"đúng lớp lỗi cross-review vừa bắt: {tom_tat!r}")
    bang("phủ" in tom_tat,
         f"(3) dòng tóm tắt không nói rõ đây là PHẠM VI ĐƯỢC PHỦ: {tom_tat!r}")
    bang("KHÔNG PHỦ" in tai_lieu,
         "(3) docstring không liệt kê thứ nó KHÔNG phủ — người đọc sẽ tưởng đã kín")


@ca
def t34_cache_tim_bash_phai_theo_doi_MOI_TRUONG():
    """THUỘC TÍNH CA NÀY TRÓI: **khoá cache có gồm môi trường không** — không phải "trả về gì".

    SINH TỪ CROSS-REVIEW (finding F3). `ung_vien()` đọc `CONG_CU_BASH`/`PATH`/`SystemRoot`/
    `ProgramFiles` từ `os.environ` khi tham số là `None`, nhưng khoá cache cũ là `[[], false]`
    — chỉ `ep` và `tat_ca`. Nút ghi đè mà chính module tự khai bị chính cache của nó nuốt.

    VIẾT LẠI Ở r6 (N20), và lý do là một PHÉP ĐO WINDOWS. Bản r4 chốt `sau == khac` — một
    **kết quả**, trong khi thuộc tính là một **cơ chế**. Hai thứ ấy trùng nhau trên Linux và
    TÁCH RA trên Windows: bộ đo `570-do-10` (máy chủ kho, HEAD `c0bc5a5`, chốt cây ĐẠT) đo được
    `trước='C:\\Program Files\\Git\\bin\\bash.exe'`, `đặt='…\\Temp\\tmppjuaw8uq\\bash'`,
    `nhận=trước` ⇒ ca ĐỎ. Và vì nó đỏ ĐỘC LẬP với mọi đột biến, nó tự cộng vào bán kính của
    TỪNG đột biến: 19 dòng `ĐỎ … bán kính 2/38` — hệ quả của MỘT ca đỏ, không phải 19 khuyết tật.

    Bản cũ KHÔNG nói được vì sao, vì nó vứt `chan_doan` đi (`sau, _ = tim_bash()`). Hai nguyên
    nhân cùng dự đoán `nhận == trước`: (a) cache vẫn nuốt; (b) cache ĐÃ tính lại, có XÉT ứng
    viên mới, nhưng ứng viên bị NĂNG LỰC từ chối nên bộ giải lùi về — tức `tim_bash` làm ĐÚNG.
    Đây là lần thứ TƯ trong packet này một ca khẳng định KẾT QUẢ trong khi cần đo CƠ CHẾ
    (`_ket_luan_ban_kinh`, `t33` chốt 3, `t35` chốt 1). Xem lease g6 `hinh_dang_ke_thua`.

    BA CHỐT, theo đúng thứ tự:
      (1) CHÍNH, độc lập nền — `chan_doan` của lần gọi THỨ HAI phải CHỨA đường ghi đè như một
          ứng viên ĐÃ ĐƯỢC XÉT. Khoá cũ trả bản nhớ mà không hỏi ứng viên nào, nên nó sẽ vắng
          mặt. `t34_khoa_cache_bo_moi_truong` giết ca này QUA CHỐT NÀY (đã đo, bán kính 1/38).
      (2) ứng viên ghi đè được CHẤP NHẬN ⇒ chốt thêm `sau == khac`.
      (3) bị TỪ CHỐI ⇒ KHÔNG ĐO ĐƯỢC, kèm `ly_do` lấy TỪ `chan_doan`. `None ≠ False`.

    Và bản ghi đè phải được dựng cho CHẠY ĐƯỢC trước đã — ƯU TIÊN một `bash` THẬT KHÁC đã có
    sẵn trên máy (`tim_bash(tat_ca=True)`), chỉ CHÉP khi không có. Bỏ qua bước ấy là tự chế một
    ứng viên hỏng rồi đổ cho bộ giải.

    ĐO ĐƯỢC TRÊN WINDOWS (`570-do-12`, HEAD `2ae2a75`, chốt cây ĐẠT): bản chép bị từ chối vì
    `C:\\Program Files\\Git\\bin\\bash.exe` là một **SHIM** giải `..\\usr\\bin\\bash.exe` TƯƠNG ĐỐI
    với chính nó — chép đi chỗ khác thì đường tương đối trỏ ra hư vô. Giả thuyết trước đó
    ("thiếu `msys-2.0.dll` bên cạnh") **ĐÃ BỊ BÁC** bằng chính phép đo ấy: `F_dll_chep_kem: []`.
    Giữ lại cả giả thuyết sai lẫn lý do bác nó — `CLAUDE.md`: ghi một nguyên nhân sai vào
    doctrine còn tệ hơn không ghi gì.

    Chạy trong TIẾN TRÌNH CON: ca này đụng `os.environ` toàn cục (r26 đã gỡ `_CACHE`), làm bẩn tiến
    trình chạy suite thì các ca sau đo nhầm.
    """
    ma = ("import json, os, shutil, sys, tempfile, runpy, glob\n"
          f"m = runpy.run_path({str(BASH_NEN)!r})\n"
          "that, _ = m['tim_bash']()\n"
          "if not that:\n"
          "    print('KQ ' + json.dumps(['BO_QUA', 'khong co bash nao dung duoc'])); raise SystemExit(0)\n"
          # BAN GHI DE PHAI CHAY DUOC, khong phai mot tep tro — N20 doi the. Uu tien MOT
          # `bash` THAT KHAC da co san tren may, va chi CHEP khi khong co.
          #
          # VI SAO DOI CACH: ban dau ca nay chi CHEP `that` sang thu muc tam. Tren Linux ban
          # sao chay duoc nen chot (2) co chay; tren Windows thi KHONG, va `570-do-12` do
          # duoc LY DO THAT:
          #     "Skipping command-line '...\\do570i-env-XXXX\\..\\usr\\bin\\bash.exe'
          #      ('...' not found) Need a valid command-line"
          # `C:\\Program Files\\Git\\bin\\bash.exe` la mot SHIM: no giai `..\\usr\\bin\\bash.exe`
          # TUONG DOI voi CHINH NO. Chep no di cho khac thi duong tuong doi tro ra hu vo.
          # (Gia thuyet truoc do — "thieu `msys-2.0.dll` ben canh" — DA BI BAC bang chinh
          #  phep do ay: `F_dll_chep_kem: []`, thu muc `Git\\bin` khong co dll nao de chep.
          #  Ghi lai ca gia thuyet sai lan ly do bac no, chu khong lang le thay chu.)
          "ung = m['tim_bash'](tat_ca=True)[1]\n"
          "khac = next((c['duong'] for c in ung if c.get('dat') and c['duong'] != that), None)\n"
          "tu_chep = khac is None\n"
          "if tu_chep:\n"
          "    tmp = tempfile.mkdtemp()\n"
          "    khac = os.path.join(tmp, os.path.basename(that))\n"
          "    shutil.copy2(that, khac); os.chmod(khac, 0o755)\n"
          "    for d in glob.glob(os.path.join(os.path.dirname(that), '*.dll')):\n"
          "        try: shutil.copy2(d, tmp)\n"
          "        except OSError: pass\n"
          "os.environ['CONG_CU_BASH'] = khac\n"
          "sau, cd = m['tim_bash']()\n"
          "print('KQ ' + json.dumps(['OK', that, khac, sau, cd, tu_chep]))\n")
    p = subprocess.run([sys.executable, "-c", ma], cwd=GOC, capture_output=True,
                       text=True, timeout=180)
    dung(p.returncode == 0 and "KQ " in p.stdout,
         f"giàn giáo hỏng: rc={p.returncode}\n{p.stdout}\n{p.stderr}")
    kq = json.loads([l for l in p.stdout.splitlines() if l.startswith("KQ ")][-1][3:])
    if kq[0] == "BO_QUA":
        raise BoQuaMoiTruong(f"KHÔNG_ĐO_ĐƯỢC: {kq[1]}")
    _, truoc, khac, sau, chan_doan, tu_chep = kq

    # CHOT CHINH — doc lap NEN. Thu N19 sua la KHOA CACHE, nen thu phai đo la "lần gọi thứ hai
    # có XÉT ứng viên mới không", chứ không phải "nó trả về đường nào". Khoá cũ trả bản nhớ mà
    # không hỏi ứng viên nào, nên đường ghi đè sẽ KHÔNG có mặt trong `chan_doan`.
    cung = {os.path.normcase(os.path.abspath(str(x.get("duong")))) for x in chan_doan}
    khac_chuan = os.path.normcase(os.path.abspath(khac))
    bang(khac_chuan in cung,
         f"`chan_doan` của lần gọi THỨ HAI KHÔNG chứa đường ghi đè ⇒ cache trả bản nhớ mà "
         f"không xét ứng viên nào: đặt={khac!r}, đã xét={sorted(cung)}. "
         f"Khoá cache phải gồm môi trường (#570 r6 N20).")

    muc = next(x for x in chan_doan
               if os.path.normcase(os.path.abspath(str(x.get("duong")))) == khac_chuan)
    if not muc.get("dat"):
        # BA TRANG THAI, khong phai hai. Ung vien ghi de bi NANG LUC tu choi thi bo giai lui ve
        # ung vien khac — do la `tim_bash` LAM DUNG viec cua no, khong phai cache nuot. Ly do
        # lay TU `chan_doan`, tuc DO DUOC, chu khong phai mot suy doan dan vao.
        raise BoQuaMoiTruong(
            f"KHÔNG_ĐO_ĐƯỢC: bản ghi đè ĐÃ ĐƯỢC XÉT nhưng bị NĂNG LỰC từ chối nên không thể "
            f"chốt `sau == khac`. đặt={khac!r} ({'bản SAO' if tu_chep else 'bash THẬT khác'}), "
            f"lý do={muc.get('ly_do')!r}. Chốt chính (cache có tính lại) ĐÃ ĐẠT ở trên.")

    bang(sau == khac,
         f"bản ghi đè ĐẠT cả hai phép mà `tim_bash` vẫn không trả nó: trước={truoc!r}, "
         f"đặt={khac!r}, nhận={sau!r}.")


@ca
def t35_cong_phai_quet_TOAN_CAY_chu_khong_chi_ops():
    """Cổng phải thấy lời gọi trần ở NGOÀI `ops/**`.

    SINH TỪ CROSS-REVIEW (finding F2), và nó bác một câu của chính packet này. PR mở đầu bằng
    *"một bộ giải dùng chung + một CỔNG chặn bản sao thứ tư"*. Nhưng bản sao thứ tư **đã sống
    sẵn ngoài hàng rào**: `.claude/dev/launcher_test.py:6004` phân giải `bash` bằng
    `shutil.which` cộng một đường Git Bash **GHI CỨNG** — đúng hình dạng vừa bị gỡ khỏi
    `_bash_posix` (r2) và `_bash_windows` (r3).

    Hai chốt:
      (1) máy quét phải TỚI ĐƯỢC một tệp ngoài `ops/` — bản r3 quét `ops/**` nên nó lọt;
      (2) `ops/reviews/` vẫn được bỏ qua (ảnh chụp đông cứng), kẻo mở phạm vi kéo theo báo
          động giả trên mã đã chết.

    CA NÀY ĐO PHẠM VI, KHÔNG ĐO PHÁN QUYẾT — và đó là một sửa lỗi có số đo, không phải
    khẩu vị. Bản đầu của chốt (1) khẳng định `rc == 2` và tên tệp có trong `ngoai_danh_sach`,
    tức nó khẳng định lại ĐÚNG thuộc tính mà `t25` đã trói: "cổng chặn được lời gọi trần mới".
    Hệ quả đo được: đột biến `bn_cong_cho_qua_moi_noi` (`moi = {}`) giết CẢ `t25` lẫn ca này,
    bán kính 2/38 — hai ca cùng trói một thuộc tính thì bán kính không còn đọc được, và
    `_ket_luan_ban_kinh` ĐỎ đúng lý.
    Nên chốt (1) nay đọc `co_loi_goi_tran` — thứ có TRƯỚC bộ lọc danh sách cho phép. Nó hỏng
    khi và chỉ khi máy quét KHÔNG TỚI tệp ấy, tức đúng thuộc tính phạm vi (`t35_thu_pham_vi_ve_ops`
    giết nó, bán kính 1/38) và không hỏng vì phán quyết đổi.

    NỢ CÓ TÊN, khai thẳng: phép hợp "bẩn NGOÀI `ops/` ⇒ cổng ĐỎ" không còn ca NÀO đo trọn
    trong một lượt. Nó là hội của hai sự kiện có cổng riêng — phạm vi (ca này) và phán quyết
    (`t25`) — nên một khuyết tật chỉ tha tệp ngoài `ops/` ở KHÂU LỌC sẽ lọt cả hai. Chưa đo
    được khuyết tật ấy; ghi ra đây thay vì giả vờ đã trói.
    """
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        cay = tmp / "cay"                        # gốc quét ≠ chỗ để bản sao — xem `t25`
        (cay / "ops").mkdir(parents=True)
        # `CHUA_CHUYEN` RỖNG: cây giả không có tệp thật nào của kho, nên giữ danh sách thật
        # sẽ làm chiều ngược của ratchet báo "mục đã sạch" và nền ĐỎ oan.
        bq = _bash_nen_voi_chua_chuyen(tmp, {})
        rc, bao = _quet(cay, bq)
        bang(not (bao.get("co_loi_goi_tran") or {}), f"NỀN phải SẠCH mà rc={rc}: {bao.get('ly_do')}")
        bang(bao.get("pham_vi") == "toan-cay",
             f"báo cáo không khai phạm vi toàn cây: {bao.get('pham_vi')!r}")

        ngoai = cay / ".claude" / "dev"
        ngoai.mkdir(parents=True)
        (ngoai / "mot_bo_giai_rieng.py").write_text(
            'import shutil\nb = shutil.which("bash")\n', encoding="utf-8")
        rc, bao = _quet(cay, bq)
        bang(".claude/dev/mot_bo_giai_rieng.py" in (bao.get("co_loi_goi_tran") or {}),
             f"(1) máy quét KHÔNG TỚI tệp ngoài `ops/` — bản sao thứ tư mọc ngoài hàng rào "
             f"đúng như cross-review đo được. Đã thấy: "
             f"{sorted((bao.get('co_loi_goi_tran') or {}))}")

        (ngoai / "mot_bo_giai_rieng.py").unlink()
        # (2) ĐỔI Ở r7 VÒNG 2. Trước đây chốt này dùng `ops/reviews/` — nhưng lớp A vừa GỠ
        # miễn trừ theo TIỀN TỐ của `ops/reviews/` và thay bằng KIỂM KÊ tường minh, nên một
        # tệp review MỚI nay phải ĐỎ (đó là `t40`). Thứ còn lại là bỏ qua đúng nghĩa: `.git/`
        # — không phải mã nguồn, không ai review nó, và mở phạm vi toàn cây không được kéo
        # theo báo động giả trên đó.
        gitdir = cay / ".git"
        gitdir.mkdir(parents=True, exist_ok=True)
        (gitdir / "hook_cu.py").write_text('import shutil\nb = shutil.which("bash")\n',
                                           encoding="utf-8")
        rc, bao = _quet(cay, bq)
        bang(".git/hook_cu.py" not in (bao.get("co_loi_goi_tran") or {}),
             f"(2) `.git/` phải được BỎ QUA — nó không phải mã nguồn: "
             f"{sorted((bao.get('co_loi_goi_tran') or {}))}")


def _chay_tien_kiem(fn):
    """Chay mot TIEN KIEM (ngoai `CA`) voi BA trang thai, tra (ten, ly_do) neu bo qua.

    VI SAO CO HAM NAY — do duoc, khong phai lo xa. `main()` ban cu goi hai tien kiem NGOAI
    moi khung bat loi, nen bat ky thu gi chung nem deu giet CA SUITE truoc vong lap ca. Hai
    lan da xay ra that, ca hai deu tren Windows va ca hai deu KHONG phai loi nghiep vu:
      · `570-do-3`/`570-do-6`: `batch_behavior_test` chet (WSL bash treo, roi thieu `bash_nen`);
      · `570-do-7`: `python_alias_behavior_test` chet `WinError 1314` — thieu dac quyen symlink.
    Moi lan, mot suite 33 ca bao cao DUNG BANG KHONG. Do chinh la benh N12 sinh ra de giet,
    va no quay lai bang mot nguyen nhan khac — nen chua o CHO GOI chu khong chua tung nguyen
    nhan mot.

    `BoQuaMoiTruong` => bo qua, DEM RIENG va IN RA (khong duoc lang le bo). Moi thu khac VAN
    nem: mot tien kiem hong vi ly do NGHIEP VU thi phai giet, do la viec cua no.
    """
    try:
        fn()
        return None
    except BoQuaMoiTruong as ex:
        return (fn.__name__, str(ex))


@ca
def t36_ratchet_dem_SO_LAN_chu_khong_tha_ca_tep():
    """THUỘC TÍNH: một mục `CHUA_CHUYEN` là hạn ngạch ĐẾM ĐƯỢC, không phải vé miễn trừ cả tệp.

    SINH TỪ CROSS-REVIEW CODEX trên `55f9bce` (P2), và executor ĐO LẠI thấy đúng y nguyên:
    thêm lời gọi trần THỨ HAI vào `.claude/hooks/session_start.py` — mục khai đúng 1 lời gọi —
    mà cổng vẫn `rc=0 DAT`. Vì `moi` loại CẢ ĐƯỜNG DẪN, còn `da_sach` chỉ bắt lúc về 0.
    Hệ quả đắt: đúng những tệp mang nợ cũ, nơi rủi ro cao nhất, là nơi bản sao thứ năm mọc
    thêm mà không ai thấy — trong khi packet này tồn tại để chặn bản sao thứ TƯ.

    Ba chốt, và chốt (3) là chiều ngược:
      (1) nền đúng SỐ KHAI ⇒ DAT;
      (2) THÊM một lời gọi ⇒ ĐỎ, nêu đúng tệp, số khai và số đo được;
      (3) BỚT đi mà chưa về 0 ⇒ cũng ĐỎ — một con số không còn đúng thì lần sau không ai
          dám tin nó, và đó đúng là bệnh `t24` (ghi chú sai sự thật) ở dạng số.
    """
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        cay = tmp / "cay"
        (cay / "ops").mkdir(parents=True, exist_ok=True)
        # Tệp nợ đặt TRONG `ops/`: ca này trói PHÉP ĐẾM, không trói phạm vi quét.
        # Để nó ngoài `ops/` thì đột biến thu-phạm-vi giết ca này luôn, và bán kính
        # hết đọc được — đúng bệnh `t35` vừa mắc ở trên.
        muc = {"ops/no_cu.py": (2, "hai lời gọi, ngày gỡ 2026-12-31")}
        bq = _bash_nen_voi_chua_chuyen(tmp, muc)
        goi = 'import shutil\nb = shutil.which("bash")\n'
        tep = cay / "ops" / "no_cu.py"

        tep.write_text("import shutil\n" + 'b = shutil.which("bash")\n' * 2, encoding="utf-8")
        rc, bao = _quet(cay, bq)
        bang(rc == 0 and bao["trang_thai"] == "DAT",
             f"(1) NỀN đúng số khai mà cổng báo {bao.get('trang_thai')} rc={rc}: "
             f"{bao.get('ly_do')}")

        tep.write_text("import shutil\n" + 'b = shutil.which("bash")\n' * 3, encoding="utf-8")
        rc, bao = _quet(cay, bq)
        bang(rc == 2 and bao["trang_thai"] == "DO",
             f"(2) THÊM lời gọi thứ ba vào mục khai 2 mà cổng vẫn rc={rc} "
             f"{bao.get('trang_thai')} — tệp mang nợ cũ là nơi bản sao mới mọc không ai thấy")
        bang("ops/no_cu.py" in (bao.get("lech_so_loi_goi") or {}),
             f"(2) cổng ĐỎ nhưng không nêu ĐÚNG mục lệch: {bao.get('lech_so_loi_goi')}")

        tep.write_text("import shutil\n" + goi, encoding="utf-8")
        rc, bao = _quet(cay, bq)
        bang(rc == 2 and bao["trang_thai"] == "DO",
             f"(3) BỚT còn 1 mà mục khai 2, cổng vẫn rc={rc} {bao.get('trang_thai')} — "
             f"một con số không còn đúng thì lần sau không ai dám tin nó")


@ca
def t37_danh_sach_tep_la_INDEX_da_add_thi_quet_chua_add_thi_KHONG():
    """THUỘC TÍNH: danh sách tệp là INDEX của git — đã `git add` thì quét, chưa add thì KHÔNG.

    SINH TỪ CROSS-REVIEW CODEX trên `55f9bce` (P2), executor ĐO LẠI trên cây giả:
        thêm `node_modules/x.py`    ⇒ rc=2 DO            — báo động giả
        thêm `node_modules/hong.py` ⇒ rc=3 KHONG_DO_DUOC — fail-close CẢ KHO vì một tệp rác
    Kho này ignore `node_modules/`, `dist/`, `reports/`, `references/golden/fixtures/` và các
    cache; từ r4 cổng quét TOÀN CÂY nên `rglob` chạm hết. Một cổng đọc khác nhau trên hai máy
    là cổng sẽ bị tắt — đúng bệnh `t43` của kho, chỉ khác nguồn.

    ĐÁNH ĐỔI CÓ CHỦ ĐỊNH (r8, quyết định của chủ kho) — KHÔNG phải một tính chất tự nhiên.
    Bản r7 của ca này chốt "tệp CHƯA add mà không bị ignore phải ĐƯỢC QUÉT TỚI". Để trả lời
    được câu ấy, cổng phải tự hỏi "tệp mới nào bị ignore", và câu hỏi ấy luôn có một tầng MÁY
    nữa: ba bản vá nối tiếp (`--exclude-standard` → `--exclude-per-directory` → blob đã theo
    dõi) lộ ra BỐN mặt của cùng một lớp (xem `_liet_ke_py`). Chủ kho chọn giết lớp bằng kiến
    trúc: danh sách = `ls-files --cached`, không còn luật ignore nào để nghe. GIÁ: tệp chưa
    `add` không được quét. Trong CI cây luôn đã commit nên độ phủ không giảm; tại chỗ, ai quên
    `add` sẽ thấy ở PR. Chốt (3)/(4) trói ĐÚNG đánh đổi ấy ở CẢ HAI chiều, để ai đổi lại thiết
    kế phải đổi ca — không đổi lặng lẽ.
    """
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        cay = tmp / "cay"
        (cay / "ops").mkdir(parents=True)
        for lenh in (["init", "-q"], ["config", "user.email", "t@t"],
                     ["config", "user.name", "t"]):
            subprocess.run(["git", "-C", str(cay)] + lenh, capture_output=True, timeout=60)
        (cay / ".gitignore").write_text("node_modules/\n", encoding="utf-8")
        (cay / "ops" / "sach.py").write_text("X = 1\n", encoding="utf-8")
        subprocess.run(["git", "-C", str(cay), "add", "-A"], capture_output=True, timeout=60)
        bq = _bash_nen_voi_chua_chuyen(tmp, {})

        rc, bao = _quet(cay, bq)
        bang(not (bao.get("co_loi_goi_tran") or {}),
             f"(1) NỀN phải SẠCH mà rc={rc}: {bao.get('ly_do')}")
        bang(bao.get("nguon_tep") == "git",
             f"(1) cây LÀ kho git mà cổng không khai dùng git: {bao.get('nguon_tep')!r}")

        ban = cay / "node_modules"
        ban.mkdir()
        (ban / "x.py").write_text('import shutil\nb = shutil.which("bash")\n', encoding="utf-8")
        (ban / "hong.py").write_text("def (\n", encoding="utf-8")
        rc, bao = _quet(cay, bq)
        bang(not (bao.get("co_loi_goi_tran") or {}),
             f"(2) tệp rác `node_modules/**` (chưa theo dõi) vẫn làm cổng rc={rc} "
             f"{bao.get('trang_thai')}: {str(bao.get('ly_do'))[:150]} — phán quyết đang phụ "
             f"thuộc MÁY AI CHẠY chứ không phụ thuộc INDEX của kho")

        # (3)/(4) ĐỌC `co_loi_goi_tran`, KHÔNG chốt `rc == 2` (N22): thuộc tính là "máy quét
        # TỚI tệp nào", còn "tới được thì ĐỎ" là của `t25`.
        moi = cay / "ops" / "that_ban.py"
        moi.write_text('import shutil\nb = shutil.which("bash")\n', encoding="utf-8")
        rc, bao = _quet(cay, bq)
        bang("ops/that_ban.py" not in (bao.get("co_loi_goi_tran") or {}),
             f"(3) tệp CHƯA `git add` lại ĐƯỢC quét: {sorted((bao.get('co_loi_goi_tran') or {}))} "
             f"— danh sách không còn là INDEX; đổi thiết kế thì đổi ca này, đừng để nó im")
        subprocess.run(["git", "-C", str(cay), "add", "ops/that_ban.py"], capture_output=True,
                       timeout=60)
        rc, bao = _quet(cay, bq)
        bang("ops/that_ban.py" in (bao.get("co_loi_goi_tran") or {}),
             f"(4) tệp ĐÃ `git add` (trong INDEX, chưa commit) phải ĐƯỢC QUÉT TỚI: đã thấy "
             f"{sorted((bao.get('co_loi_goi_tran') or {}))}")


@ca
def t38_khoa_cache_gom_THU_MUC_LAM_VIEC():
    """THUỘC TÍNH: khoá cache gồm cả `cwd`, vì một mục TƯƠNG ĐỐI giải theo thư mục hiện tại.

    SINH TỪ CROSS-REVIEW CODEX trên `55f9bce` (P2). `t34` đã trói "khoá gồm MÔI TRƯỜNG", và
    `cwd` là một đầu vào NGẦM khác: `CONG_CU_BASH=bash` với `PATH=.` cho hai ứng viên khác
    nhau ở hai thư mục khác nhau, trong khi bốn chuỗi môi trường KHÔNG đổi.
    Executor ĐO LẠI trên Linux: gọi ở `a/` rồi gọi ở `b/` ⇒ trả CÙNG một kết quả — cache nuốt.

    Chạy trong TIẾN TRÌNH CON: ca này đụng `os.chdir` và `os.environ` toàn cục (r26 đã gỡ `_CACHE`).

    TIỀN ĐỀ PHẢI ĐƯỢC CHỐT TRƯỚC, VÀ CHỐT BẰNG `chan_doan` — sinh từ nghiệm thu Windows
    `570-do-14` (ghim `1253e3a`). Log in: *"ở `b/` KHÔNG có `bash` nào mà `tim_bash` vẫn trả
    'C:\\Program Files\\Git\\bin\\bash.exe' ⇒ … khoá cache không gồm `os.getcwd()`. cwd=a →
    'C:\\Program Files\\Git\\bin\\bash.exe'"*. Đọc `cwd=a`: ở `a/` bộ giải đã trả Git Bash chứ
    KHÔNG phải bản ghi đè — bản sao `bash.exe` là SHIM, chép đi thì không chạy (bài học `t34`),
    nên bị năng lực từ chối và bộ giải lùi về Git Bash qua một đường khác. Tiền đề của ca chưa
    bao giờ được lập, và thông điệp đổ cho cache là MỘT NGUYÊN NHÂN CHƯA ĐO — đúng hình dạng
    `_ket_luan_ban_kinh` đã mắc ở r4. Tái hiện được trên Linux: bản sao `chmod 644` cộng
    `/usr/bin` trên PATH ⇒ bản r7 in đúng câu ấy trong khi cache vô can.
    Nay: `t1` chuẩn hoá (`normcase(abspath)`, tính NGAY trong tiến trình con khi cwd còn là
    `a/`) phải BẰNG bản ghi đè; không thì `BoQuaMoiTruong` kèm `chan_doan` của lần gọi ở `a/`
    (ứng viên nào được xét, bị từ chối vì gì) — không kèm suy đoán. KHAI THẲNG giới hạn: tên
    ứng viên là TƯƠNG ĐỐI, nên phép so nói "bộ giải đã CHỌN tên trỏ vào `a/`", không nói
    "TỆP ấy đã chạy"; với `PATH='.'` hai câu trùng nhau, và đó là lý do PATH phải là `.`.

    CÔ LẬP ĐƯỜNG DỰ PHÒNG trên Windows — đọc mã `ung_vien()`, CHƯA ĐO trên nền ấy: (a)
    `CONG_CU_BASH` = tên tương đối ⇒ giải theo cwd; (b) `PATH='.'` ⇒ chỉ cwd; (c)
    `shutil.which("git", path=PATH)` ⇒ chỉ tìm `git` trong cwd (Windows còn tự chèn `.` —
    vẫn là cwd), `a/`/`b/` không có `git.exe` nên đường `..\\bin\\bash.exe` chết; (d)
    `ProgramFiles` ⇒ thư mục rỗng nên `Git\\bin\\bash.exe` không `is_file`; `SystemRoot` ⇒
    rỗng. Không còn nhánh nào khác đọc môi trường. Nếu lượt Windows kế tiếp vẫn thấy Git Bash
    ở `b/` thì đó là đường CHƯA LIỆT KÊ — báo cáo phải in `chan_doan` để chỉ ra nó.
    """
    ma = ("import json, os, shutil, sys, tempfile, runpy\n"
          f"m = runpy.run_path({str(BASH_NEN)!r})\n"
          "that, _ = m['tim_bash']()\n"
          "if not that:\n"
          "    print('KQ ' + json.dumps(['BO_QUA', 'khong co bash nao dung duoc'])); raise SystemExit(0)\n"
          # `a/` CO mot `bash` chay duoc, `b/` KHONG CO GI. Nen mot muc TUONG DOI giai
          # duoc o `a/` va KHONG giai duoc o `b/` — do la thu phan biet duoc, khac han
          # viec so hai CHUOI TRA VE (ca hai deu la ten tuong doi, luon giong nhau).
          "goc = tempfile.mkdtemp()\n"
          "duong = []\n"
          "for ten in ('a', 'b'):\n"
          "    d = os.path.join(goc, ten); os.makedirs(d)\n"
          "if True:\n"
          "    d = os.path.join(goc, 'a')\n"
          "    dich = os.path.join(d, os.path.basename(that))\n"
          "    shutil.copy2(that, dich); os.chmod(dich, 0o755)\n"
          "    for x in os.listdir(os.path.dirname(that)):\n"
          "        if x.lower().endswith('.dll'):\n"
          "            try: shutil.copy2(os.path.join(os.path.dirname(that), x), d)\n"
          "            except OSError: pass\n"
          "    duong.append(dich)\n"
          # CÔ LẬP MỌI ĐƯỜNG DỰ PHÒNG. Trên Windows, `b/` KHÔNG thật sự trống nếu
          # `ung_vien()` còn tìm lại được Git Bash qua `git` trên PATH hay qua
          # `%ProgramFiles%` — khi ấy chốt `t2 is None` hỏng vì bộ giải làm ĐÚNG, không
          # phải vì cache. Cross-review codex trên `1253e3a` chỉ ra chỗ này.
          "trong = tempfile.mkdtemp()\n"
          "os.environ['CONG_CU_BASH'] = os.path.basename(that)\n"
          "os.environ['PATH'] = '.'\n"
          "os.environ['ProgramFiles'] = trong\n"
          "os.environ['ProgramFiles(x86)'] = trong\n"
          "os.environ['SystemRoot'] = trong\n"
          "os.chdir(os.path.join(goc, 'a')); t1, cd1 = m['tim_bash']()\n"
          # Chuẩn hoá NGAY tại `a/` — `t1` là tên TƯƠNG ĐỐI, `abspath` ở nơi khác là sai.
          "t1_abs = os.path.normcase(os.path.abspath(t1)) if t1 else None\n"
          "os.chdir(os.path.join(goc, 'b')); t2, cd2 = m['tim_bash']()\n"
          "print('KQ ' + json.dumps(['OK', t1, t1_abs, t2, duong, cd1, cd2]))\n")
    p = subprocess.run([sys.executable, "-c", ma], cwd=GOC, capture_output=True,
                       text=True, timeout=180)
    dung(p.returncode == 0 and "KQ " in p.stdout,
         f"giàn giáo hỏng: rc={p.returncode}\n{p.stdout}\n{p.stderr}")
    kq = json.loads([l for l in p.stdout.splitlines() if l.startswith("KQ ")][-1][3:])
    if kq[0] == "BO_QUA":
        raise BoQuaMoiTruong(f"KHÔNG_ĐO_ĐƯỢC: {kq[1]}")
    _, t1, t1_abs, t2, duong, cd1, cd2 = kq
    ghi_de = os.path.normcase(os.path.abspath(duong[0]))
    # TIỀN ĐỀ, trước mọi chốt khác: ở `a/` bộ giải phải CHỌN bản ghi đè. `t1` khác None chưa đủ
    # — `570-do-14` cho `t1` = Git Bash (bản ghi đè bị năng lực từ chối) và ca đổ oan cho cache.
    if t1_abs != ghi_de:
        raise BoQuaMoiTruong(
            f"KHÔNG_ĐO_ĐƯỢC: tiền đề chưa lập — ở `a/` `tim_bash` phải trả bản ghi đè "
            f"{duong[0]!r} mà trả {t1!r} (chuẩn hoá {t1_abs!r}). Chẩn đoán lần gọi ở `a/` — "
            f"ứng viên nào được xét, bị từ chối vì gì: {json.dumps(cd1, ensure_ascii=False)}. "
            f"Bản sao `bash` không chạy được trên nền này thì xem `t34` (SHIM của Git for "
            f"Windows); bộ giải lùi về một `bash` KHÁC thì đó là đường dự phòng CHƯA bịt.")
    # CHOT: o `b/` KHONG co `bash` nao, nen `tim_bash` phai tra None. Neu no van tra mot
    # duong thi do la BAN NHO cua lan goi truoc — tuc khoa cache khong gom `cwd`.
    #
    # KHONG chot `t1 != t2` (ban dau da viet the va ca DO ngay tren Linux): `tim_bash` tra
    # CHUOI UNG VIEN, ma chuoi ay la ten TUONG DOI nen giong nhau o ca hai thu muc du no
    # phong ra hai tep khac nhau. Do la khang dinh KET QUA trong khi thu can do la CO CHE —
    # dung hinh dang `t34` da mac o r6 va `t35` da mac o r4. Bat duoc truoc khi day.
    bang(t2 is None,
         f"ở `b/` KHÔNG có `bash` nào mà `tim_bash` vẫn trả {t2!r} trong khi tiền đề đã lập "
         f"(cwd=a → {t1!r} == bản ghi đè). Chẩn đoán ở `b/`: {json.dumps(cd2, ensure_ascii=False)} "
         f"— rỗng nghĩa là KHÔNG ứng viên nào được xét, tức đây là BẢN NHỚ của lần gọi ở `a/`: "
         f"khoá cache không gồm `os.getcwd()` (#570 r7); có ứng viên nghĩa là một đường dự "
         f"phòng chưa bịt, KHÔNG phải cache.")



# ---------------------------------------------------------------------------
# N22 — DANH SÁCH CA ĐƯỢC PHÉP CHỐT TRÊN PHÁN QUYẾT CỦA CỔNG.
#
# SINH TỪ MỘT HÌNH DẠNG ĐÃ LẶP SÁU LẦN, không phải từ một ý hay. Một ca khẳng định KẾT QUẢ
# (`rc == 2`, `trang_thai == "DO"`) trong khi thuộc tính nó phải trói là một CƠ CHẾ, hoặc là
# thứ ca khác ĐÃ trói:
#   1  `_ket_luan_ban_kinh` in NGUYÊN NHÂN khi mới chỉ ĐẾM                       (r4)
#   2  `t33` chốt (3) cấm một chuỗi trên TOÀN docstring                          (r4)
#   3  `t35` chốt (1) khẳng định `rc == 2` — thuộc tính của `t25`                (r4)
#   4  `t34` khẳng định `sau == khac` — cơ chế là KHOÁ CACHE                     (r6)
#   5  `t38` khẳng định `t1 != t2` — giá trị trả về là chuỗi TƯƠNG ĐỐI           (r7)
#   6  `t37` chốt (3) khẳng định `rc == 2` — lại thuộc tính của `t25`            (r7)
# Ba trong sáu lần là do CHÍNH phiên vừa ghi nguyên tắc ấy vào docstring. Một nguyên tắc chỉ
# sống trong docstring thì không phải hàng rào — nó là lời nhắc mà người đang vội đi qua.
# Và mỗi lần chỉ lộ ra SAU một lượt đột biến 55 phút.
#
# PHẠM VI: chỉ ca nào GỌI `_quet(...)` — tức đang chạy cổng `bash_nen` — và chỉ chiều ĐỎ.
# Ca phán quyết của `ops/cong_cu.py kiem-tra` (`t1`, `t2`, `t4`, `t12`…) không thuộc luật này.
CA_PHAN_QUYET = {
    "t25_cong_chan_loi_goi_bash_tran_MOI":
        "ca ĐỊNH NGHĨA phán quyết ĐỎ của cổng: lời gọi trần MỚI ⇒ rc=2.",
    "t26_ratchet_phai_NGAN_di_chu_khong_muc_ra":
        "chiều ngược của ratchet: mục đã SẠCH mà còn trong danh sách ⇒ rc=2.",
    "t36_ratchet_dem_SO_LAN_chu_khong_tha_ca_tep":
        "phán quyết MỚI ở r7: số lời gọi LỆCH với số khai ⇒ rc=2. Không ca nào khác trói nó.",
    # r14 — HAI ca được khai TƯỜNG MINH sau khi nới luật. Cả hai trói PHÁN QUYẾT thật sự:
    # fail-close LÀ thuộc tính của chúng, không phải một chốt mượn tạm.
    "t44_khong_lay_duoc_INDEX_thi_KHONG_DO_DUOC_chu_khong_lui_ve_rglob":
        "cây có `.git` mà không lấy được INDEX ⇒ rc=3 KHONG_DO_DUOC. Phán quyết CHÍNH LÀ "
        "thuộc tính ca này trói: không có danh sách thì không có phán quyết. Từ r20 (N74) "
        "trói thêm: bộ quét NÉM trên một tệp ⇒ rc=3, không traceback.",
    "t45_bo_ca_phai_CHAY_cong_tren_cay_THAT_chu_khong_chi_cay_gia":
        "phán quyết MỚI ở r11 (N31, finding P1 duy nhất của packet): điểm vào mà CI gọi phải "
        "phản ánh ĐÚNG phán quyết của cổng. Ca này buộc phải ĐỌC `rc_cong` vì thuộc tính nó "
        "trói CHÍNH LÀ sự khớp giữa hai đường ấy — không có trường CƠ CHẾ nào thay thế được. "
        "Nó lọt khỏi ratchet từ r11 tới r15 chỉ vì đặt tên biến là `rc_cong` thay vì `rc`; "
        "N49 (r16) đi theo ràng buộc của `_quet` nên nay thấy.",
    "t47_INDEX_phai_duoc_doc_TRUNG_THUC_va_nguon_py_nhan_du_moi_cach_viet":
        "INDEX chưa hoà giải ⇒ rc=3. Chọn bừa một stage là tự bịa ra một cây chưa từng tồn "
        "tại, nên fail-close là thuộc tính, không phải hệ quả.",
}
# DANH SÁCH NÀY LÀ MỘT KIỂM KÊ, KHÔNG PHẢI MỘT LỆNH CẤM — đọc lại ở r14 cho đúng. Trước r14
# nó khai mình là "ai được khẳng định ĐỎ", và đúng câu ấy là chỗ ba lần lặp chui qua: `t45`
# (r11) chốt "điểm vào phải hỏng", `t47` (r12) đọc `ngoai_danh_sach`, `t48` (r13) chốt
# `rc == 0` — không cái nào "khẳng định ĐỎ" nên không cái nào bị hỏi.
# Nay nó là: "ai được trói PHÁN QUYẾT của cổng — chiều nào cũng vậy". Bốn ca khác đã viết lại
# theo TRƯỜNG CƠ CHẾ thay vì vào đây; `t27` là một trong số đó (nó chốt `co_loi_goi_tran` rỗng,
# đúng thuộc tính nó trói: chú thích KHÔNG sinh ra lời gọi nào).

_TT_DO = "DO"


# TRƯỜNG TỔNG HỢP: giá trị của chúng là hàm của MỌI luật trong cổng. Một ca chốt lên đây là
# trói lại phán quyết, không trói cơ chế của chính nó. Đối lập là TRƯỜNG CƠ CHẾ —
# `co_loi_goi_tran`, `lech_so_loi_goi`, `lech_oid_dong_cung`, `nguon_tep`, `nguon_noi_dung`,
# `bien_git_da_go`, `lien_ket_tuong_trung`, `muc_ratchet_da_sach`, `so_cho_phep` — mỗi trường
# một luật, nên chốt lên chúng thì bán kính đột biến còn đọc được.
_TRUONG_TONG_HOP = ("trang_thai", "ngoai_danh_sach", "ly_do")


def _chot_DO_cua_cong_trong(than: str):
    """Số dòng các chốt trói PHÁN QUYẾT của cổng trong thân một ca. Đo bằng `ast`, không đo chuỗi.

    NỚI RỘNG Ở r14 — chỉ thị chủ kho, sau khi cùng một hình dạng lỗi lặp BA revision liên tiếp:
        r11 `t45` chốt "cây bẩn ⇒ điểm vào hỏng"   — trói lại thuộc tính `t25`
        r12 `t47` chốt trên `ngoai_danh_sach`      — trường có SAU bộ lọc miễn trừ
        r13 `t48` chốt `rc == 0`                   — phán quyết, phụ thuộc MỌI luật khác
    Cả ba **lọt qua** luật cũ, vì luật cũ chỉ phủ `rc == 2` và `trang_thai == "DO"`. Lặp lần
    thứ ba thì chữa bằng CƠ CHẾ: nay phủ **mọi** phép chạm tới `rc` hoặc tới một TRƯỜNG TỔNG
    HỢP (`trang_thai`, `ngoai_danh_sach`, `ly_do`) — mọi toán tử, mọi giá trị.

    VÌ SAO LẦN NÀY NỚI ĐƯỢC mà r7 thì không. r7 ghi: *"chiều XANH là NỀN của gần như mọi ca —
    cấm nó thì không ca nào viết được."* Câu ấy chưa từng được ĐO. r14 đo: trong **13** ca có
    gọi `_quet`, nới rộng bắt thêm **SÁU** — không phải gần hết. Sáu ca ấy đã đi đúng hai
    đường: bốn viết lại theo TRƯỜNG CƠ CHẾ (`co_loi_goi_tran`, `lien_ket_tuong_trung`…), hai
    khai tường minh vào `CA_PHAN_QUYET` vì fail-close **là** thuộc tính của chúng.

    Danh sách này là một KIỂM KÊ, không phải một lệnh cấm: ca nào thật sự trói phán quyết thì
    khai ra kèm lý do. Trước r14 nó là danh sách ba mục **bỏ sót sáu**.

    GIỮ NGUYÊN thu hẹp (a) của r7: CHỈ ca có gọi `_quet(...)`. Bản đầu quét mọi ca và tóm luôn
    `t2`, `t4`, `t7`… — những ca phán quyết của `ops/cong_cu.py kiem-tra`, chẳng liên quan tới
    cổng `bash_nen`. Một luật bắt oan là luật sẽ bị tắt.

    Docstring NHẮC TỚI `rc` và `trang_thai` để giải thích, mà KHÔNG bị tính: chỉ đọc đối số
    ĐIỀU KIỆN của `bang(...)`/`dung(...)`, không đọc thông điệp, không đọc chú thích. Đúng bài
    học `t27`.
    """
    import ast as _ast
    cay = _ast.parse(than)

    def la_quet(n):
        return (isinstance(n, _ast.Call) and isinstance(n.func, _ast.Name)
                and n.func.id == "_quet")

    if not any(la_quet(n) for n in _ast.walk(cay)):
        return []

    # ── N55 (r17) — XUẤT XỨ, KHÔNG PHẢI TRÙNG TÊN ────────────────────────────
    # N49 (r16) đi theo ràng buộc của `_quet` thay vì khớp chữ `rc` — đúng hướng, nhưng nó
    # GIEO SẴN `rc` vào tập tên và so TRÙNG CHUỖI cho trường tổng hợp, nên nó BẮT OAN. Đo
    # được ở vòng 11, bốn ca, tất cả là báo động giả do chính bản vá r16 đẻ ra:
    #   `rc = other()` rồi `ma, bao = _quet(…)` rồi `bang(rc == 0, …)`   ⇒ [4]   (mong [])
    #   `bang(config["trang_thai"] == "ok", …)`                          ⇒ [3]   (mong [])
    #   `rc, bao = _quet(…)` rồi `rc = khac()` rồi `bang(rc == 2, …)`    ⇒ [4]   (mong [])
    #   `kq = _quet(…)` rồi `bang(not kq[1]["co_loi_goi_tran"], …)`      ⇒ [3]   (mong [])
    # *"Một luật bắt oan là luật sẽ bị tắt"* — và một ratchet bị tắt thì ba lần lặp mà r14 vá
    # sẽ quay lại hết. Nên nay theo XUẤT XỨ có VỊ TRÍ: mỗi tên mang một danh sách ràng buộc
    # `(vị trí, nguồn)`, và tại một phép chốt thì ràng buộc MUỘN NHẤT TRƯỚC nó mới tính —
    # cùng một cơ chế N53 dùng cho phạm vi module, vì đây cũng đúng câu hỏi ấy.
    #   `ma`     — mang MÃ THOÁT của `_quet`      ⇒ chạm tới là chốt phán quyết
    #   `bao`    — mang BÁO CÁO của `_quet`       ⇒ chỉ TRƯỜNG TỔNG HỢP mới tính
    #   `bo_doi` — mang CẢ bộ đôi                 ⇒ `[0]` là mã, `[1]` là báo cáo
    #   `khac`   — mọi thứ còn lại                ⇒ KHÔNG tính, kể cả khi tên là `rc`
    def _ket(n):
        return (getattr(n, "end_lineno", None) or n.lineno,
                getattr(n, "end_col_offset", None) or n.col_offset)

    # ── N80 (r22) — XUẤT XỨ THEO TÊN, KHÔNG THEO PHẠM VI / VỊ TRÍ / NHÁNH ─────────────
    # Năm revision liền (r18 N64 → r19 N69 → r20 N75 → r21 N79 → vòng 16) vá CÙNG MỘT lớp: "nguồn
    # nào TỚI ĐƯỢC phép chốt". Mỗi vòng mô phỏng thêm một mảnh ngữ nghĩa — nhánh có điều kiện,
    # `with` nuốt ngoại lệ, phạm vi từ vựng, cạnh quay lui, comprehension — và vòng sau tìm ra mảnh
    # kế tiếp: iterable ĐẦU của comprehension tính ở phạm vi bao, biểu thức lúc định nghĩa (mặc
    # định, decorator, cơ sở lớp) cũng thế, tham số lambda/async, và năm dạng ràng buộc chưa ghi
    # (walrus, `with … as`, `except … as`, `case`, `+=`). ĐIỀU KIỆN DỪNG của lease chạm ở lần thứ
    # NĂM; chủ kho chọn ĐỔI KIẾN TRÚC sau khi đọc phép đo, cùng hướng N76 đã làm cho bộ giải tên:
    #   hợp mọi ràng buộc cùng tên, giữ luật nhãn trường ⇒ trên CÂY THẬT bắt đúng 6 ca như cũ,
    #   THÊM 0 · MẤT 0; 9 mẫu CHE TÊN trong `_MAU_TOAN_TU` chuyển thành BỊ BẮT — bắt thừa có chủ
    #   đích, và bắt thừa ở đây chỉ đẩy một ca vào BẢN KIỂM KÊ, không làm cổng lọt.
    # Luật: NGUỒN của một tên là HỢP nguồn của MỌI ràng buộc cùng tên trong cả tệp ca, mọi dạng
    # ràng buộc có giá trị (gán, gán có chú thích, `+=`, `:=`, `for`/comprehension — kể cả phần
    # tử của danh sách hằng, `with … as`). Không hỏi phạm vi, vị trí hay nhánh.
    rang_buoc = {}                      # ten -> {nguon}

    def ghi(ten, nguon):
        if ten:
            rang_buoc.setdefault(ten, set()).add(nguon)

    def nguon_tap(ten, *_):
        """Tập NGUỒN của `ten` — hợp mọi ràng buộc cùng tên (N80). Tham số thừa giữ chữ ký cũ."""
        return rang_buoc.get(ten, set())

    def cac_dich_va_gia(nut):
        """[(đích, biểu thức giá trị, là_vòng_lặp)] cho MỌI dạng ràng buộc CÓ giá trị."""
        if isinstance(nut, _ast.Assign):
            return [(d, nut.value, False) for d in nut.targets]
        if isinstance(nut, (_ast.AnnAssign, _ast.AugAssign, _ast.NamedExpr)):
            return [(nut.target, nut.value, False)] if nut.value is not None else []
        if isinstance(nut, (_ast.For, _ast.AsyncFor, _ast.comprehension)):
            return [(nut.target, nut.iter, True)]
        if isinstance(nut, (_ast.With, _ast.AsyncWith)):
            return [(it.optional_vars, it.context_expr, False) for it in nut.items
                    if it.optional_vars is not None]
        return []

    def doc_truong_tong_hop(n):
        """Biểu thức `n` có CHẠM tới báo cáo của `_quet` theo cách nào KHÁC đọc một trường CƠ CHẾ.

        N87 (r23) liệt kê cách đọc; N91 (r24) hỏi "nhắc tới hằng tên trường tổng hợp". Codex vòng 19 đo
        được cách viết THỨ BA của cùng hình dạng — tên trường GẤP (`bao.__getitem__("trang_" + "thai")`,
        `operator.itemgetter("ly_" + "do")(bao)`) ⇒ kiểm kê rỗng. ĐIỀU KIỆN DỪNG chạm; chủ kho chọn ĐẢO
        SANG DANH SÁCH CHO PHÉP (N92, r25): mọi lần một tên mang báo cáo (`bao`/`bo_doi`, hay chính lời
        gọi `_quet`) xuất hiện trong biểu thức đều là CHẠM PHÁN QUYẾT, TRỪ đúng một hình dạng được tha:
        `x["<trường cơ chế>"]` / `x.get("<trường cơ chế>"[, mặc định])` với tên trường là HẰNG CHỮ không
        thuộc `_TRUONG_TONG_HOP`. Danh sách cho phép chỉ phải liệt kê MỘT hình dạng biết trước; danh
        sách cấm phải đoán mọi cách viết. Đo trên tệp ca thật trước khi chọn: THÊM 0 · MẤT 0.
        """
        tha = set()
        for x in _ast.walk(n):
            khoa, g = None, None
            if isinstance(x, _ast.Subscript) and isinstance(x.slice, _ast.Constant):
                khoa, g = x.slice.value, x.value
            elif (isinstance(x, _ast.Call) and isinstance(x.func, _ast.Attribute)
                  and x.func.attr == "get" and 1 <= len(x.args) <= 2 and not x.keywords
                  and isinstance(x.args[0], _ast.Constant)):
                khoa, g = x.args[0].value, x.func.value
            # N92b (r26, codex vòng 20) — chỉ tha ĐÚNG tên báo cáo nhận trực tiếp (`bao`, hay
            # `kq` trong `kq[1]`), KHÔNG tha cả cây con của bộ nhận: `(bao if bao["trang_thai"]
            # else bao)["co_loi_goi_tran"]` đọc `trang_thai` khi TÍNH bộ nhận, mà bản r25 tha cả nó.
            if isinstance(khoa, str) and khoa not in _TRUONG_TONG_HOP:
                if isinstance(g, _ast.Name):
                    tha.add(id(g))
                elif (isinstance(g, _ast.Subscript) and isinstance(g.slice, _ast.Constant)
                      and g.slice.value == 1
                      and (isinstance(g.value, _ast.Name) or la_quet(g.value))):
                    # N92c (r27, codex vòng 21): cả `_quet(…)[1]` TRỰC TIẾP — chỉ tha chính lời gọi
                    # và phép lấy phần tử 1, không tha đối số hay bộ nhận phức tạp nào khác.
                    tha.update((id(g), id(g.value)))
        return any(id(x) not in tha and (la_quet(x) or (isinstance(x, _ast.Name)
                                                         and nguon_tap(x.id) & {"bao", "bo_doi"}))
                   for x in _ast.walk(n))

    def nguon_cua(g, lap=False):
        """Tập nguồn mà một biểu thức đặt ra; `lap` ⇒ nguồn của MỖI PHẦN TỬ khi lặp trên nó."""
        if lap:
            if isinstance(g, (_ast.List, _ast.Tuple, _ast.Set)):
                ra_ = set()
                for e in g.elts:
                    ra_ |= nguon_cua(e)
                return ra_ or {"khac"}
            # lặp trên một BỘ ĐÔI `_quet(…)` ⇒ lần lượt nhận mã rồi báo cáo
            return {"ma", "bao"} if "bo_doi" in nguon_cua(g) else {"khac"}
        if isinstance(g, _ast.NamedExpr):
            return nguon_cua(g.value)
        if la_quet(g):
            return {"bo_doi"}
        if isinstance(g, _ast.Subscript) and isinstance(g.slice, _ast.Constant):
            if la_quet(g.value) or (isinstance(g.value, _ast.Name)
                                    and "bo_doi" in nguon_tap(g.value.id)):
                return {{0: "ma", 1: "bao"}.get(g.slice.value, "khac")}
        if isinstance(g, _ast.Name):
            return set(nguon_tap(g.id)) or {"khac"}
        if doc_truong_tong_hop(g):
            return {"tt"}                  # N87: tên mang GIÁ TRỊ một trường tổng hợp
        return {"khac"}

    def gan(d, ng, gia):
        """Ghi nguồn cho ĐÍCH `d` nhận giá trị có nguồn `ng` (biểu thức `gia` nếu biết).

        N105 (r29, codex vòng 23) — đích LỒNG NHIỀU TẦNG: `((rc, bao),) = (_quet(cay),)` hợp lệ mà bản
        r28 chỉ nhìn một tầng tên trực tiếp ⇒ kiểm kê rỗng. Nay đi đệ quy: đích bộ và giá trị bộ LITERAL
        cùng độ dài, không `*` ⇒ ghép từng cặp; đích bộ nhận một BỘ ĐÔI `_quet` ⇒ phần tử 0 là mã, 1 là
        báo cáo (đệ quy cả khi phần tử ấy lại là một bộ); còn lại ⇒ mọi tên bên trong là `khac`.
        """
        if isinstance(d, _ast.Name):
            for x in ng:
                ghi(d.id, x)
            return
        if not isinstance(d, (_ast.Tuple, _ast.List)):
            return
        if (isinstance(gia, (_ast.Tuple, _ast.List)) and len(gia.elts) == len(d.elts)
                and not any(isinstance(x, _ast.Starred) for x in (*gia.elts, *d.elts))):
            for dd, gg in zip(d.elts, gia.elts):
                gan(dd, nguon_cua(gg), gg)
            return
        for k, ph in enumerate(d.elts):
            # `ma, bao = _quet(…)` — CHỈ phần tử 0 là phán quyết.
            nguon_ph = {0: "ma", 1: "bao"}.get(k, "khac") if "bo_doi" in ng else "khac"
            gan(ph.value if isinstance(ph, _ast.Starred) else ph, {nguon_ph}, None)

    kich = -1
    while kich != sum(len(v) for v in rang_buoc.values()):     # bất động điểm: bí danh nhiều tầng
        kich = sum(len(v) for v in rang_buoc.values())
        for nut in _ast.walk(cay):
            for d, gia, lap in cac_dich_va_gia(nut):
                gan(d, nguon_cua(gia, lap), None if lap else gia)

    def cham_phan_quyet(dieu_kien):
        vt = _ket(dieu_kien)
        # `bang(_quet(…)[0] == 2, …)` — lời gọi `_quet` TRỰC TIẾP: từ N92 luật cho phép bên dưới đã
        # tính nó (một lời gọi `_quet` không nằm trong hình dạng được tha là chạm phán quyết). Luật
        # "có `_quet(` là tính" của bản cũ che mất phần tha của N92c nên đã gỡ ở r27.
        if doc_truong_tong_hop(dieu_kien):
            return True                  # N92: CẢ điều kiện, không từng nút con (luật cho phép cần ngữ cảnh)
        for n in _ast.walk(dieu_kien):
            # N87 (r23): `tt` — bí danh của một trường tổng hợp — là chạm phán quyết như `ma`.
            if isinstance(n, _ast.Name) and nguon_tap(n.id, vt, dieu_kien) & {"ma", "tt"}:
                return True
            if (isinstance(n, _ast.Subscript) and isinstance(n.slice, _ast.Constant)
                    and n.slice.value == 0 and isinstance(n.value, _ast.Name)
                    and "bo_doi" in nguon_tap(n.value.id, vt, dieu_kien)):
                return True
        return False

    # ── N49 — `assert` TRẦN cũng là một phép chốt ─────────────────────────────
    # Bản r14 chỉ soi `bang(...)`/`dung(...)`. Đo được: `assert rc == 2` sau `_quet` ⇒ `[]`.
    # Một ca chỉ cần viết `assert` thay vì `bang` là ra khỏi tầm ratchet — cửa hậu ấy rộng
    # bằng đúng cả luật. CHỈ đọc ĐIỀU KIỆN, không đọc thông điệp: đúng bài học `t27`
    # ("một cổng báo động giả là cổng sẽ bị tắt").
    ra = []
    for nut in _ast.walk(cay):
        if isinstance(nut, _ast.Call) and isinstance(nut.func, _ast.Name) \
                and nut.func.id in ("bang", "dung"):
            # N101 (r28, codex vòng 22) — ĐIỀU KIỆN đến bằng VỊ TRÍ hay bằng từ khoá `dk=`: bản r27 chỉ
            # đọc `args[0]`, nên `bang(dk=bao["trang_thai"] == "DO", msg="x")` ra khỏi kiểm kê.
            dieu_kien = nut.args[0] if nut.args else next(
                (k.value for k in nut.keywords if k.arg == "dk"), None)
            if dieu_kien is None:
                # N101b (r29, codex vòng 23) — `dk` đến qua `**{…}` LITERAL: khoá hằng biết được.
                # `**x` không phải literal thì không biết — không đoán.
                # LỚP ĐÃ KHÉP (r30, chủ kho — lần BA của hình dạng "`dk`/xuất xứ tới bằng cách viết
                # mới"): `**` LỒNG (`**{**{"dk": …}}`) và đích lồng trong VÒNG LẶP là nợ có tên, ghim ở
                # `_MAU_TOAN_TU` (`khep_*`, mong False). Bộ chốt chỉ nhận cú pháp TRỰC TIẾP. r32: mở rộng
                # cho mọi DẠNG RÀNG BUỘC mới — `match`/`case` (codex vòng 26), walrus, `with … as`….
                dieu_kien = next((v for k in nut.keywords
                                  if k.arg is None and isinstance(k.value, _ast.Dict)
                                  for kk, v in zip(k.value.keys, k.value.values)
                                  if isinstance(kk, _ast.Constant) and kk.value == "dk"), None)
            if dieu_kien is None:
                continue
        elif isinstance(nut, _ast.Assert):
            dieu_kien = nut.test
        else:
            continue
        if cham_phan_quyet(dieu_kien):
            ra.append(dieu_kien.lineno)
    return ra


def _nhan(nut) -> str:
    """Mọi khoá chuỗi và tên thuộc tính trong một nút — để nhận ra `bao["trang_thai"]`."""
    import ast as _ast
    return " ".join(
        n.value if isinstance(n, _ast.Constant) and isinstance(n.value, str) else n.attr
        for n in _ast.walk(nut)
        if (isinstance(n, _ast.Constant) and isinstance(n.value, str))
        or isinstance(n, _ast.Attribute))


_MAU_TOAN_TU = {
    # PHAI bat: moi phep cham toi `rc` hoac mot TRUONG TONG HOP — MOI toan tu, MOI gia tri.
    # Truoc r14 chi hai mau `eq_*` la True, va DUNG CHO DO la cho ba lan lap chui qua:
    # `t45` (r11) chot "diem vao phai hong", `t47` (r12) doc `ngoai_danh_sach`, `t48` (r13)
    # chot `rc == 0`. Khong cai nao "khang dinh DO" nen khong cai nao bi hoi.
    "eq_rc":   "def f():\n    rc, bao = _quet(a, b)\n    bang(rc == 2, 'x')\n",
    "eq_tt":   'def f():\n    rc, bao = _quet(a, b)\n    bang(bao["trang_thai"] == "DO", "x")\n',
    "ne_rc":   "def f():\n    rc, bao = _quet(a, b)\n    bang(rc != 2, 'x')\n",
    "ne_tt":   'def f():\n    rc, bao = _quet(a, b)\n    bang(bao["trang_thai"] != "DO", "x")\n',
    "rc_bang_0": "def f():\n    rc, bao = _quet(a, b)\n    bang(rc == 0, 'x')\n",
    "ngoai_ds":  'def f():\n    rc, bao = _quet(a, b)\n    bang(not bao["ngoai_danh_sach"], "x")\n',
    # KHONG duoc bat: TRUONG CO CHE — moi truong mot luat, nen ban kinh dot bien con doc duoc.
    "truong_co_che": 'def f():\n    rc, bao = _quet(a, b)\n    bang(not bao["co_loi_goi_tran"], "x")\n',
    "lech_oid":      'def f():\n    rc, bao = _quet(a, b)\n    bang(not bao["lech_oid_dong_cung"], "x")\n',
    # PHAI bat — CO CHE moi cua N49 (r16): `assert` tran, bi danh cua ma thoat, goi long.
    "assert_tran":  "def f():\n    rc, bao = _quet(a, b)\n    assert rc == 2\n",
    "assert_tt":    "def f():\n    rc, bao = _quet(a, b)\n    assert bao['trang_thai'] == 'DO'\n",
    "bi_danh":      "def f():\n    rc_cong, bao = _quet(a, b)\n    bang(rc_cong != 0, 'x')\n",
    "lay_phan_tu_0": "def f():\n    ma = _quet(a, b)[0]\n    bang(ma == 2, 'x')\n",
    "goi_long":     "def f():\n    bang(_quet(a, b)[0] == 2, 'x')\n",
    # r17 — N55: XUAT XU, khong phai TRUNG TEN. Bon mau duoi la BAO DONG GIA do chinh ban
    # va r16 de ra, do duoc o vong 11. Khong co chung thi `ct_khong_theo_xuat_xu` SONG SOT.
    "xuat_xu_bo_doi":  "def f():\n    kq = _quet(a, b)\n    bang(kq[0] == 2, 'x')\n",
    "xuat_xu_bao_doi": "def f():\n    bao = _quet(a, b)[1]\n    bang(bao['ngoai_danh_sach'], 'x')\n",
    # PHAI bat, va CHI phep loc THEO VI TRI moi doc duoc: chot nam TRUOC lan ghi de sau no.
    # Khong co mau nay thi `ct_xuat_xu_khong_theo_vi_tri` SONG SOT — `max()` khong loc van
    # chon dung "khac" cho mau `bi_danh_ghi_de`, nen ca hai mau ra cung ket qua.
    "chot_truoc_khi_ghi_de":
        "def f():\n    rc, bao = _quet(a, b)\n    bang(rc == 2, 'x')\n    rc = khac()\n",
    # r18 — N64: TAP NGUON CON TOI DUOC. Phep ghi de nam trong nhanh CO THE KHONG CHAY thi
    # khong duoc xoa xuat xu con song. Khong co mau nay thi mot ban va quay ve "muon nhat
    # thang" se SONG SOT.
    "ghi_de_co_dieu_kien":
        "def f():\n    rc, bao = _quet(a, b)\n    if x:\n        rc = other()\n    bang(rc == 2, 'x')\n",
    "ghi_de_trong_vong_lap":
        "def f():\n    rc, bao = _quet(a, b)\n    for _ in xs:\n        rc = other()\n    bang(rc == 2, 'x')\n",
    # r19 — N69: `with` NUOT ngoai le, va xuat xu tach theo PHAM VI tu vung.
    "with_nuot_truoc_ghi_de":
        "def f():\n    rc, bao = _quet(a, b)\n    with suppress(E):\n        raise E()\n"
        "        rc = other()\n    bang(rc == 2, 'x')\n",
    "helper_long_che":
        "def f():\n    rc, bao = _quet(a, b)\n    def h():\n        rc = other()\n    bang(rc == 2, 'x')\n",
    # r20 — N75: NHANH, khong phai NUT; than lop khong nhin thay tu ham long; canh quay lui.
    # PHAI bat: phuong thuc doc `rc` cua ham bao — thuoc tinh lop CUNG TEN khong che duoc.
    "lop_long_phuong_thuc":
        "def f():\n    rc, bao = _quet(a, b)\n    class K:\n        rc = 1\n"
        "        def m(self):\n            bang(rc == 2, 'x')\n",
    # PHAI bat: `_quet` ghi SAU phep chot trong cung than vong lap ⇒ co hieu luc tu vong hai.
    "quay_lui_vong_lap":
        "def f():\n    rc = 0\n    for _ in xs:\n        bang(rc == 2, 'x')\n        rc, bao = _quet(a, b)\n",
    # KHONG duoc bat: `assertWarns` BAT CANH BAO, khong nuot ngoai le ⇒ ghi de chac chan chay.
    "assert_warns_ghi_de":
        "def f(self):\n    rc, bao = _quet(a, b)\n    with self.assertWarns(W):\n"
        "        warn()\n        rc = other()\n    bang(rc == 2, 'x')\n",
    # KHONG duoc bat: `finally` LUON chay ⇒ ghi de trong no che `_quet`.
    "finally_ghi_de":
        "def f():\n    rc, bao = _quet(a, b)\n    try:\n        pass\n    finally:\n"
        "        rc = other()\n    bang(rc == 2, 'x')\n",
    # KHONG duoc bat: `_quet` o nhanh `if`, phep chot o nhanh `else` — khong bao gio cung chay.
    "nhanh_loai_tru":
        "def f():\n    if x:\n        rc, bao = _quet(a, b)\n    else:\n        bang(rc == 2, 'x')\n",
    # KHONG duoc bat: `_quet` o SAU phep chot, khong co vong lap ⇒ khong toi duoc.
    "quet_sau_chot":
        "def f():\n    rc = khac()\n    bang(rc == 2, 'x')\n    rc, bao = _quet(a, b)\n",
    # r21 — N79: KHONG duoc bat: comprehension co `rc` RIENG (dich lap), phep chot doc chinh no.
    "comprehension_rc_rieng":
        "def f():\n    rc, bao = _quet(a, b)\n    [bang(rc == 2, 'x') for rc in [0]]\n",
    # PHAI bat: comprehension KHONG rang buoc `rc` ⇒ doc `rc` cua `_quet` o pham vi bao.
    "comprehension_doc_bao":
        "def f():\n    rc, bao = _quet(a, b)\n    [bang(rc == 2, 'x') for _ in [0]]\n",
    # r22 — N80: MOI dang rang buoc co gia tri ghi nguon; pham vi/vi tri/nhanh khong con hoi.
    "walrus_tu_quet":
        "def f():\n    (rc := _quet(a, b)[0])\n    bang(rc == 2, 'x')\n",
    "comprehension_dich_tu_quet":
        "def f():\n    [bang(rc == 2, 'x') for rc, bao in [_quet(a, b)]]\n",
    "iterable_dau_o_pham_vi_bao":
        "def f():\n    rc, bao = _quet(a, b)\n    [0 for rc in [bang(rc == 2, 'x')]]\n",
    "mac_dinh_o_pham_vi_bao":
        "def f():\n    rc, bao = _quet(a, b)\n    def g(rc=bang(rc == 2, 'x')):\n        pass\n",
    # BAT THUA CO CHU DICH (N80): tham so lambda CHE `rc` — nay van bi bat, chi day ca vao kiem ke.
    "lambda_tham_so_che":
        "def f():\n    rc, bao = _quet(a, b)\n    (lambda rc: bang(rc == 2, 'x'))(0)\n",
    # PHAI bat: hai `except*` CO THE cung chay ⇒ `_quet` o nhanh truoc toi phep chot nhanh sau.
    "except_sao_cung_chay":
        "def f():\n    try:\n        pass\n    except* ValueError:\n        rc, bao = _quet(a, b)\n"
        "    except* TypeError:\n        bang(rc == 2, 'x')\n",
    # KHONG duoc bat: `with` THUONG khong nuot ngoai le — ghi de chac chan chay.
    "with_thuong_ghi_de":
        "def f():\n    rc, bao = _quet(a, b)\n    with open(p) as fh:\n        rc = other()\n    bang(rc == 2, 'x')\n",
    # KHONG duoc bat: ham phu co `rc` RIENG, va phep chot doc chinh `rc` ay.
    "helper_rc_rieng":
        "def f():\n    rc, bao = _quet(a, b)\n    def h():\n        rc = khac()\n        bang(rc == 2, 'x')\n",
    # KHONG duoc bat: phep ghi de nam CUNG nhanh voi phep chot ⇒ chac chan chay truoc no.
    "ghi_de_cung_nhanh":
        "def f():\n    rc, bao = _quet(a, b)\n    if x:\n        rc = other()\n        bang(rc == 2, 'x')\n",
    # KHONG duoc bat: ten `rc` GIEO SAN, khong tu `_quet`.
    "rc_gieo_san":     "def f():\n    rc = other()\n    ma, bao = _quet(a, b)\n    bang(rc == 0, 'x')\n",
    # KHONG duoc bat: mot chuoi TRUNG TEN truong, tren mot doi tuong chang lien quan.
    "chuoi_trung_ten": "def f():\n    ma, bao = _quet(a, b)\n    bang(config['trang_thai'] == 'ok', 'x')\n",
    # KHONG duoc bat: bi danh DA BI GHI DE bang thu khac truoc khi chot.
    "bi_danh_ghi_de":  "def f():\n    rc, bao = _quet(a, b)\n    rc = khac()\n    bang(rc == 2, 'x')\n",
    # KHONG duoc bat: phan tu 1 cua bo doi la BAO CAO, va truong CO CHE cua no khong tinh.
    "bo_doi_truong_co_che":
        "def f():\n    kq = _quet(a, b)\n    bang(not kq[1]['co_loi_goi_tran'], 'x')\n",
    # KHONG duoc bat: THONG DIEP cua `assert` chi la van xuoi, du no co nhac `rc`.
    "assert_thong_diep":
        "def f():\n    rc, bao = _quet(a, b)\n"
        "    assert bao['co_loi_goi_tran'], 'rc va trang_thai chi duoc nhac o day'\n",
    # KHONG duoc bat: khong dung toi cong
    "khong_quet": "def f():\n    bang(rc == 2, 'x')\n",
    # r23 — N87 (F4 vong 17): `.get(<truong tong hop>)` va BI DANH TRUONG la cung mot phep doc.
    "get_truong_tong_hop": "def f():\n    rc, bao = _quet(a, b)\n    bang(bao.get('trang_thai') == 'DO', 'x')\n",
    "bi_danh_truong":      "def f():\n    rc, bao = _quet(a, b)\n    tt = bao['trang_thai']\n    bang(tt == 'DO', 'x')\n",
    "get_qua_bo_doi":      "def f():\n    kq = _quet(a, b)\n    bang(not kq[1].get('ngoai_danh_sach'), 'x')\n",
    "bi_danh_truong_get":  "def f():\n    rc, bao = _quet(a, b)\n    ld = bao.get('ly_do')\n    bang(ld, 'x')\n",
    # KHONG duoc bat (chieu nguoc N87): `.get` cua TRUONG CO CHE, va bi danh cua no.
    "get_truong_co_che":   "def f():\n    rc, bao = _quet(a, b)\n    bang(not bao.get('co_loi_goi_tran'), 'x')\n",
    "bi_danh_truong_co_che": "def f():\n    rc, bao = _quet(a, b)\n    c = bao['co_loi_goi_tran']\n    bang(not c, 'x')\n",
    # r24 — N91 (vong 18): moi CACH doc mot truong tong hop — khong liet ke, hoi "co nhac toi".
    "getitem_truong":      "def f():\n    rc, bao = _quet(a, b)\n    bang(bao.__getitem__('trang_thai') == 'DO', 'x')\n",
    "itemgetter_truong":   "def f():\n    rc, bao = _quet(a, b)\n    bang(operator.itemgetter('ly_do')(bao), 'x')\n",
    "bi_danh_getattr_get": "def f():\n    kq = _quet(a, b)\n    t = getattr(kq[1], 'get')('trang_thai')\n    bang(t == 'DO', 'x')\n",
    # r25 — N92 (codex vong 19): ten truong GAP — danh sach CHO PHEP bat theo cau truc.
    "ten_truong_gap":      "def f():\n    rc, bao = _quet(a, b)\n    bang(bao.__getitem__('trang_' + 'thai') == 'DO', 'x')\n",
    "itemgetter_ten_gap":  "def f():\n    rc, bao = _quet(a, b)\n    bang(operator.itemgetter('ly_' + 'do')(bao), 'x')\n",
    "get_co_che_mac_dinh": "def f():\n    rc, bao = _quet(a, b)\n    bang(not bao.get('co_loi_goi_tran', []), 'x')\n",
    "len_truong_co_che":   "def f():\n    kq = _quet(a, b)\n    bang(len(kq[1]['co_loi_goi_tran']) == 1, 'x')\n",
    # r26 — N92b (codex vong 20): bo nhan PHUC TAP tu no doc truong tong hop.
    "bo_nhan_doc_truong":  "def f():\n    rc, bao = _quet(a, b)\n    bang((bao if bao['trang_thai'] else bao)['co_loi_goi_tran'], 'x')\n",
    # r27 — N92c (codex vong 21): truong CO CHE doc thang tren `_quet(…)[1]` khong phai phan quyet.
    "quet_truc_tiep_co_che": "def f():\n    bang(not _quet(a, b)[1]['co_loi_goi_tran'], 'x')\n",
    "quet_truc_tiep_get_co_che": "def f():\n    bang(not _quet(a, b)[1].get('co_loi_goi_tran'), 'x')\n",
    "quet_truc_tiep_tong_hop": "def f():\n    bang(_quet(a, b)[1]['trang_thai'] == 'DO', 'x')\n",
    # r28 — N101 (codex vong 22): dieu kien den bang tu khoa `dk=`.
    "bang_tu_khoa_dk":     "def f():\n    rc, bao = _quet(a, b)\n    bang(dk=bao['trang_thai'] == 'DO', msg='x')\n",
    "dung_tu_khoa_dk":     "def f():\n    rc, bao = _quet(a, b)\n    dung(dk=rc == 2, msg='x')\n",
    "bang_tu_khoa_co_che": "def f():\n    rc, bao = _quet(a, b)\n    bang(dk=not bao['co_loi_goi_tran'], msg='x')\n",
    # r29 — N105 / N101b (codex vong 23).
    "dich_long_hai_tang":  "def f():\n    ((rc, bao),) = (_quet(a, b),)\n    bang(rc == 2, 'x')\n",
    "dich_long_bao":       "def f():\n    (ma, (rc, bao)) = (1, _quet(a, b))\n    bang(bao['trang_thai'] == 'DO', 'x')\n",
    "dich_long_nguon_khac": "def f():\n    ((rc, bao),) = (khac(),)\n    bang(rc == 2, 'x')\n",
    "bang_sao_sao_dk":     "def f():\n    rc, bao = _quet(a, b)\n    bang(**{'dk': bao['trang_thai'] == 'DO', 'msg': 'x'})\n",
    "bang_sao_sao_co_che": "def f():\n    rc, bao = _quet(a, b)\n    bang(**{'dk': not bao['co_loi_goi_tran'], 'msg': 'x'})\n",
    # r30 — LOP DA KHEP (chu kho, codex vong 24 — cach `dk`/xuat xu toi, lan BA): `**` LONG va dich
    # LONG trong VONG LAP. No co ten: bo chot KHONG bat (mong False). Ai phu duoc thi dao sang True.
    "khep_dk_sao_sao_long": "def f():\n    rc, bao = _quet(a, b)\n    bang(**{**{'dk': bao['trang_thai'] == 'DO'}, 'msg': 'x'})\n",
    "khep_vong_lap_dich_long": "def f():\n    for ((rc, bao),) in [(_quet(a, b),)]:\n        bang(rc == 2, 'x')\n",
    # r32 — LOP DA KHEP mo rong (chu kho, codex vong 26): xuat xu qua `match` — mot dang RANG BUOC moi
    # cua cung lop r30. Bo chot KHONG bat (mong False); reviewer khong bao them dang rang buoc moi nao.
    "khep_match_anh_xa": "def f():\n    rc, bao = _quet(a, b)\n    match bao:\n        case {'trang_thai': tt}:\n            bang(tt == 'DO', 'x')\n",
    "khep_match_bo": "def f():\n    match _quet(a, b):\n        case (rc, bao):\n            dung(rc == 2, 'x')\n",
    "get_tren_doi_tuong_khac": "def f():\n    rc, bao = _quet(a, b)\n    bang(config.get('trang_thai') == 'ok', 'x')\n",
}
def _ly_do_khong_doc_duoc(v) -> bool:
    """Lý do miễn trừ KHÔNG đọc được: không phải chuỗi, hay chỉ có khoảng trắng (N50, r16)."""
    return not (isinstance(v, str) and v.strip())


# MAU THU cho chinh luat tren. KHONG CO CHUNG thi `ct_ly_do_khong_doc` SONG SOT: hom nay moi
# muc cua `CA_PHAN_QUYET` deu co ly do that, nen mot ban va lam luat thoi doc CHANG DOI GI CA.
# Dung bai toan `_MAU_TOAN_TU` da gap o r7 — thu chieu nguoc sinh ra de bat phai duoc TAO RA,
# khong the cho no tinh co xuat hien tren cay that.
_MAU_LY_DO = {"rong": "", "khoang_trang": "   \t\n", "khong_phai_chuoi": None,
              "con_so": 123, "danh_sach": ["vì sao"],
              "that": "vì sao đo được", "co_le_trang": "  vì sao  "}
_MAU_LY_DO_MONG = {"rong": True, "khoang_trang": True, "khong_phai_chuoi": True,
                   "con_so": True, "danh_sach": True,
                   "that": False, "co_le_trang": False}

# r22 — N80: CHIN mau duoi day doi tu False sang True CO CHU DICH — chung la meo CHE TEN (gan de,
# `finally`, nhanh loai tru, `_quet` sau phep chot, comprehension/ham phu co `rc` rieng…) ma
# r18..r21 da mo phong nhanh/pham vi/vi tri de khong bat. Chu kho chon DOI KIEN TRUC: bat thua o day
# chi day mot ca vao BAN KIEM KE, khong lam cong lot. Tren cay that: THEM 0 (do duoc).
_MAU_MONG = {"eq_rc": True, "eq_tt": True, "ne_rc": True, "ne_tt": True,
             "rc_bang_0": True, "ngoai_ds": True,
             "assert_tran": True, "assert_tt": True, "bi_danh": True,
             "lay_phan_tu_0": True, "goi_long": True,
             "xuat_xu_bo_doi": True, "xuat_xu_bao_doi": True,
             "chot_truoc_khi_ghi_de": True,
             "ghi_de_co_dieu_kien": True, "ghi_de_trong_vong_lap": True,
             "ghi_de_cung_nhanh": True,
             "with_nuot_truoc_ghi_de": True, "helper_long_che": True,
             "with_thuong_ghi_de": True, "helper_rc_rieng": True,
             "lop_long_phuong_thuc": True, "quay_lui_vong_lap": True,
             "assert_warns_ghi_de": True, "finally_ghi_de": True,
             "nhanh_loai_tru": True, "quet_sau_chot": True,
             "comprehension_rc_rieng": True, "comprehension_doc_bao": True,
             "except_sao_cung_chay": True,
             "walrus_tu_quet": True, "comprehension_dich_tu_quet": True,
             "iterable_dau_o_pham_vi_bao": True, "mac_dinh_o_pham_vi_bao": True,
             "lambda_tham_so_che": True,
             "truong_co_che": False, "lech_oid": False,
             "rc_gieo_san": False, "chuoi_trung_ten": False, "bi_danh_ghi_de": True,
             "bo_doi_truong_co_che": False,
             "assert_thong_diep": False, "khong_quet": False,
             "get_truong_tong_hop": True, "bi_danh_truong": True, "get_qua_bo_doi": True,
             "bi_danh_truong_get": True,
             "get_truong_co_che": False, "bi_danh_truong_co_che": False,
             "get_tren_doi_tuong_khac": False,
             "khep_dk_sao_sao_long": False, "khep_vong_lap_dich_long": False,
             "khep_match_anh_xa": False, "khep_match_bo": False,
             "getitem_truong": True, "itemgetter_truong": True, "bi_danh_getattr_get": True,
             "ten_truong_gap": True, "itemgetter_ten_gap": True,
             "get_co_che_mac_dinh": False, "len_truong_co_che": False,
             "bo_nhan_doc_truong": True,
             "quet_truc_tiep_co_che": False, "quet_truc_tiep_get_co_che": False,
             "quet_truc_tiep_tong_hop": True,
             "bang_tu_khoa_dk": True, "dung_tu_khoa_dk": True, "bang_tu_khoa_co_che": False,
             "dich_long_hai_tang": True, "dich_long_bao": True, "dich_long_nguon_khac": False,
             "bang_sao_sao_dk": True, "bang_sao_sao_co_che": False}


def _in_tu_kiem_luat_phan_quyet():
    """In (ca_ngoai_danh_sach, ten_trong_danh_sach_ma_rong) dưới dạng JSON một dòng.

    CHẠY QUA TIẾN TRÌNH CON có lý do đo được, không phải cho gọn. `t39` bản đầu gọi thẳng
    `_chot_DO_cua_cong_trong` ĐÃ NẠP TRONG TIẾN TRÌNH, nên hai đột biến của chính luật ấy
    (`t39_bo_phep_quet`, `t39_bo_chieu_nguoc`) mutate tệp trên đĩa mà KHÔNG cắn được gì —
    cả hai SỐNG SÓT. Đó là lần thứ NĂM trong packet này mắc đúng bẫy ấy (`t33` là lần trước,
    chữa bằng `runpy.run_path`). Một luật mà đột biến của chính nó không giết được thì không
    phải luật, nó là một đoạn mã chưa ai thử.
    """
    import ast as _ast
    than = TEP_TEST.read_text(encoding="utf-8")
    ten_ca = {f.__name__ for f in CA}
    co_chot, ngoai = {}, {}
    for nut in _ast.parse(than).body:
        if not isinstance(nut, _ast.FunctionDef) or nut.name not in ten_ca:
            continue
        dong = _chot_DO_cua_cong_trong(_ast.get_source_segment(than, nut) or "")
        if dong:
            co_chot[nut.name] = dong
            if nut.name not in CA_PHAN_QUYET:
                ngoai[nut.name] = dong
    # MỌI khoá vắng khỏi `co_chot` đều là CHẾT — kể cả khoá mà HÀM đã bị xoá hoặc đổi tên.
    # Bản đầu lọc `t in ten_ca` trước, nên xoá một ca vẫn để lại miễn trừ chết mà tự kiểm
    # không thấy: codex đo được `KQ [{}, []]` rc=0 sau khi gỡ `t25` khỏi một bản sao.
    # Hệ quả có chủ đích: một tên GÕ SAI trong danh sách sẽ ĐỎ ngay, thay vì im lặng.
    rong = [t for t in CA_PHAN_QUYET if t not in co_chot]
    # N50 (r16) — LY DO PHAI DUOC DOC. Ban r14 chi kiem TU CACH THANH VIEN cua khoa, chua
    # bao gio cham toi gia tri. Do duoc tren `8180970`: thay ly do cua mot muc bat ky bang
    # `""`, `"   "`, `None` hay `123` thi ca `ngoai` lan `rong` deu RONG va cong van rc=0 —
    # tuc "moi mien tru phai kem ly do do duoc" la mot LOI KHAI, khong phai mot phep do.
    # Dung lop "LOI KHAI RONG HON PHEP DO" (N6) va dung lop "mot cong khong the DO thi khong
    # phai cong". Day la lan thu TU packet nay gap chinh no.
    ly_do_hong = sorted(t for t, v in CA_PHAN_QUYET.items() if _ly_do_khong_doc_duoc(v))
    # MAU THU TOAN TU. Khong co chung thi dot bien `t39_bo_phep_so_bang` SONG SOT: hom nay
    # khong ca that nao viet `bang(rc != 2, ...)`, nen go phep doi `==` chang doi gi ca.
    # Dung bai toan `t26`/`t39_de_ten_chet` da gap — thu chieu nguoc sinh ra de bat phai
    # duoc TAO RA, khong the cho no tinh co xuat hien.
    mau = {k: bool(_chot_DO_cua_cong_trong(v)) for k, v in _MAU_TOAN_TU.items()}
    mau_ly = {k: bool(_ly_do_khong_doc_duoc(v)) for k, v in _MAU_LY_DO.items()}
    print("KQ " + json.dumps([ngoai, sorted(rong), mau, ly_do_hong, mau_ly],
                             ensure_ascii=False))


@ca
def t40_moi_MIEN_TRU_deu_mang_HAN_NGACH_va_dem_theo_LOI_GOI():
    """THUỘC TÍNH: miễn trừ là HẠN NGẠCH ĐẾM ĐƯỢC, và đơn vị đếm là LỜI GỌI chứ không phải DÒNG.

    SINH TỪ CROSS-REVIEW CODEX vòng 2 trên `1253e3a`, và từ một lượt QUÉT THEO LỚP của
    executor — hai nguồn độc lập ra **cùng ba thực thể**. Chủ kho chỉ thị: *"cross-review tìm
    kiếm, phân theo lớp, không phải từng lỗi riêng lẻ"*.

    LỚP: *miễn trừ khai theo TƯ CÁCH THÀNH VIÊN thay vì theo HẠN NGẠCH*. Vòng 1 mới vá MỘT
    thực thể (`CHUA_CHUYEN`); lớp có BA, và cả ba đều đo được trên cây giả:
      · `CHO_PHEP`          thêm bản sao thứ NĂM vào CHÍNH bộ giải  ⇒ `rc=0 DAT`
      · `_BO_QUA_TOAN_CAY`  ba tệp bẩn trong `ops/reviews/`         ⇒ `rc=0 DAT`, báo cáo RỖNG
      · đơn vị đếm          hai lời gọi CÙNG MỘT DÒNG               ⇒ đếm thành MỘT
    `CHO_PHEP` là chỗ đau nhất: packet này tồn tại để chặn BẢN SAO THỨ TƯ, mà nơi được miễn
    trừ vô hạn lại đúng là nơi BẢN SAO THỨ NĂM mọc — trong tệp không ai nghi ngờ nhất.
    """
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        cay = tmp / "cay"
        (cay / "ops").mkdir(parents=True)
        # Ảnh chụp GIẢ có hạn ngạch > 0 — để đo hạn ngạch ở CẢ HAI vế, kể cả vế 0.
        anh_gia = "ops/reviews/anh_gia_t40.py"
        bq = _bash_nen_voi_chua_chuyen(tmp, {}, anh_chup={anh_gia: (2, "0" * 40, "ảnh chụp giả của t40")})
        # r19 — bộ BA với OID giả hợp lệ về hình dạng: N71 coi bộ ĐÔI là mục đông cứng HỎNG.
        # Cây của ca này không phải kho git nên OID không được so — chỉ hình dạng bảng được kiểm.
        bn = runpy.run_path(str(bq))

        # MỌI bảng miễn trừ phải mang hạn ngạch SỐ. Đọc từ BẢN THẬT (`BASH_NEN`), không từ bản
        # sao `bq` — bản sao đã thay `CHUA_CHUYEN`/`ANH_CHUP_DONG_CUNG` bằng bảng của ca, nên đọc
        # nó là kiểm bảng của CHÍNH MÌNH. Đo được ở r8: một mục CHUỖI trong `CHUA_CHUYEN` thật
        # (= vé vô hạn, 9 lời gọi ⇒ DAT) đi qua chốt này vì nó chưa từng nhìn bảng thật.
        # Một bảng mới thêm sau này cũng phải đi qua đây; không chép cứng.
        bn_that = runpy.run_path(str(BASH_NEN))
        moi_muc = {}
        for ten_bang in ("CHO_PHEP", "CHUA_CHUYEN", "ANH_CHUP_DONG_CUNG"):
            for duong, muc in bn_that[ten_bang].items():
                moi_muc[f"{ten_bang}:{duong}"] = bn_that["_so_cho_phep"](muc)[0]
        thieu = sorted(k for k, v in moi_muc.items() if not isinstance(v, int))
        bang(not thieu,
             f"có mục miễn trừ KHÔNG mang hạn ngạch số: {thieu}. Một miễn trừ khai theo TƯ "
             f"CÁCH THÀNH VIÊN là lớp khuyết tật vòng này tìm ra BA thực thể.")

        (cay / "ops" / "reviews").mkdir(parents=True)
        tep_anh = cay / anh_gia
        tep_anh.write_text("import shutil\n" + 'shutil.which("bash")\n' * 2, encoding="utf-8")
        rc0, bao0 = _quet(cay, bq)
        bang("ops/bash_nen.py" in (bao0.get("so_cho_phep") or {}),
             f"`CHO_PHEP` KHÔNG nằm trong bảng hạn ngạch gộp — nó lại thành vé VÔ HẠN: "
             f"{sorted((bao0.get('so_cho_phep') or {}))}. Đây là nơi BẢN SAO THỨ NĂM mọc.")
        # HẠN NGẠCH LÀ HẠN NGẠCH Ở MỌI GIÁ TRỊ, KỂ CẢ 0 — r8, F1 codex vòng 3, điều phối viên đo
        # lại: ảnh chụp khai N còn N ⇒ `lech_so=[]` (đúng); về 0 ⇒ CŨNG `lech_so=[]` (sai), vì
        # r7 viết `if thay and …` — về 0 thì thôi so, và `da_sach` chỉ phủ `CHUA_CHUYEN`.
        # Đọc `lech_so_loi_goi`, KHÔNG chốt `rc`/`trang_thai` (N22): thuộc tính là PHÉP ĐẾM.
        lech0 = bao0.get("lech_so_loi_goi") or {}
        bang(anh_gia not in lech0 and "ops/bash_nen.py" not in lech0,
             f"NỀN: đúng số khai (ảnh 2/2, `CHO_PHEP` 0/0) mà đã lệch: {lech0}")
        tep_anh.write_text("import shutil\n", encoding="utf-8")
        _, bao_0 = _quet(cay, bq)
        lech = bao_0.get("lech_so_loi_goi") or {}
        bang(anh_gia in lech and lech[anh_gia].get("do_duoc") == 0,
             f"ảnh chụp khai 2 mà VỀ 0 phải nằm trong `lech_so_loi_goi` — hạn ngạch 0 bị bỏ qua: "
             f"{lech}")
        bang("ops/bash_nen.py" not in lech,
             f"`CHO_PHEP` khai 0 và ĐANG 0 bị ĐỎ OAN: {lech} — so đủ hai vế, đừng hỏi 'có thấy gì'")
        tep_anh.write_text("import shutil\n" + 'shutil.which("bash")\n' * 2, encoding="utf-8")

        # đơn vị đếm là LỜI GỌI: hai lời gọi trên MỘT dòng phải ra HAI bản ghi
        hai = bn["_loi_goi_tran"](
            'import shutil\nb = (shutil.which("bash"), shutil.which("bash"))\n')
        bang(len(hai) == 2,
             f"hai lời gọi CÙNG MỘT DÒNG phải là HAI bản ghi, đo được {hai} — tập DÒNG gộp "
             f"chúng thành một, nên một bản sao thêm vào đúng dòng cũ sẽ vô hình")

        # `ops/reviews/` không còn là miễn trừ theo TIỀN TỐ
        (cay / "ops" / "reviews" / "moi").mkdir(parents=True)
        (cay / "ops" / "reviews" / "moi" / "helper.py").write_text(
            'import shutil\nshutil.which("bash")\n', encoding="utf-8")
        rc, bao = _quet(cay, bq)
        bang("ops/reviews/moi/helper.py" in (bao.get("co_loi_goi_tran") or {}),
             f"tệp review MỚI phải ĐƯỢC QUÉT TỚI, không được tha theo tiền tố: đã thấy "
             f"{sorted((bao.get('co_loi_goi_tran') or {}))}")

        # N63 (r18) — HẠN NGẠCH HỎNG phải FAIL-CLOSE, không NÉM. Bản trước gọi `int(muc[0])` vô
        # điều kiện, nên `("not-a-number", "lý do")` ném `ValueError` TRƯỚC khi `quet()` kịp vào
        # nhánh KHONG_DO_DUOC đã khai — đo được ở vòng 12: CLI thoát 1 kèm traceback. Đo CƠ CHẾ
        # (hàm đọc hạn ngạch trả `None`; `quet` không ném), KHÔNG chốt `rc`/`trang_thai` — N22.
        # `True` bị loại tường minh: trong Python nó LÀ `int` và bằng 1, nên một hạn ngạch
        # gõ nhầm thành `True` sẽ lặng lẽ thành "được phép một lần".
        hong = {"chuoi_so": ("not-a-number", "lý do"), "bool": (True, "lý do"),
                "am": (-1, "lý do"), "so_thuc": (1.5, "lý do"), "none": (None, "lý do")}
        # BỌC lời gọi: một phép đọc NÉM chính là khuyết tật đang đo, nên nó phải đi tới CHỐT
        # của ca này chứ không được thoát ra như một ngoại lệ thô. Đo được lý do: bản đầu gọi
        # thẳng, và đột biến `bn_quota_ep_kieu` bị bộ phân hạng gắn TÍN DỤNG GIẢ — ca chết vì
        # `ValueError` TRƯỚC khi tới `bang(...)`, tức không phải bị chốt của nó giết.
        def _doc(v):
            try:
                return bn["_so_cho_phep"](v)[0]
            except Exception as e:                                    # noqa: BLE001
                return f"NÉM {type(e).__name__}"
        doc_sai = {k: _doc(v) for k, v in hong.items()}
        bang(all(v is None for v in doc_sai.values()),
             f"hạn ngạch HỎNG phải đọc ra `None` (⇒ KHONG_DO_DUOC), đọc được {doc_sai}")
        bang(bn["_so_cho_phep"]((3, "lý do"))[0] == 3
             and bn["_so_cho_phep"]((0, "oid", "lý do"))[0] == 0,
             "chiều ngược: hạn ngạch HỢP LỆ (kể cả 0, kể cả mục ba phần tử) phải đọc đúng")
        bq_hong = _bash_nen_voi_chua_chuyen(tmp, {"ops/gia_t40.py": ("not-a-number", "lý do")},
                                            ten="bash_nen_quota_hong.py")
        try:
            runpy.run_path(str(bq_hong))["quet"](cay)
            nem = None
        except Exception as e:                                        # noqa: BLE001
            nem = f"{type(e).__name__}: {e}"
        bang(nem is None,
             f"một hạn ngạch gõ nhầm làm `quet()` NÉM thay vì báo cáo: {nem} — cổng mất tiếng "
             f"nói, CI chỉ thấy traceback và không biết mục nào hỏng")

        # N71 (r19) — mục ĐÔNG CỨNG phải ghim một OID blob HỢP LỆ, sai thì FAIL-CLOSE. Bản r18
        # `continue` khi không có OID, nên một mục lỡ bị sửa thành `(số, lý do)` TẮT IM LẶNG
        # phép ghim blob — đo được ở vòng 13: `quet()` ra `DAT`, `lech_oid_dong_cung` RỖNG. Đo
        # qua TRƯỜNG CƠ CHẾ `mien_tru_hong`, không chốt `trang_thai` (N22).
        oid = bn["_oid_dong_cung"]
        bang(oid((7, "a" * 40, "lý do")) == "a" * 40
             and all(oid(m) is None for m in ((7, "lý do"), (7, "xyz", "lý do"),
                                              (7, "A" * 40, "lý do"), (7, None, "lý do"))),
             "`_oid_dong_cung` phải CHỈ nhận bộ ba với OID 40 hex thường; nhận được "
             f"{[oid(m) for m in ((7, 'lý do'), (7, 'xyz', 'lý do'))]}")
        bq_anh = _bash_nen_voi_chua_chuyen(tmp, {}, anh_chup={anh_gia: (2, "thiếu OID")},
                                           ten="bash_nen_anh_thieu_oid.py")
        _, bao_anh = runpy.run_path(str(bq_anh))["quet"](cay)
        bang(anh_gia in (bao_anh.get("mien_tru_hong") or []),
             f"mục ĐÔNG CỨNG không ghim OID phải vào `mien_tru_hong` (⇒ KHONG_DO_DUOC), thấy "
             f"{bao_anh.get('mien_tru_hong')} — không thì 'không được sửa một byte' là lời khai "
             f"rộng hơn phép đo")


@ca
def t43_khong_luat_ignore_nao_doi_duoc_danh_sach_tep():
    """THUỘC TÍNH: danh sách tệp KHÔNG đổi dưới BẤT KỲ luật ignore nào — của kho hay của máy —
    vì cổng chỉ đọc INDEX, không đọc luật ignore.

    THAY CHO `t41` (r7 vòng 2, "chỉ tôn trọng luật ignore CỦA KHO") — gỡ ở r8. `t41` sinh ra
    để tách "luật của KHO thì có hiệu lực" khỏi "luật của MÁY thì không"; khi cổng không đọc
    luật nào nữa, mọi chốt của nó thành thứ không thể ĐỎ, và một ca không thể đỏ giữ lại chỉ để
    người sau tưởng có hàng rào. Lớp khuyết tật nó canh — *phán quyết phụ thuộc trạng thái LOCAL*
    — lộ BỐN mặt qua ba bản vá (xem `_liet_ke_py`); chủ kho quyết giết lớp bằng kiến trúc.
    Ca này chốt CHÍNH tính chất kiến trúc ấy, và có răng nhờ một đột biến nghe lại luật ignore
    (`bn_nghe_lai_luat_ignore`): một tệp ĐÃ ADD mà khớp `.gitignore` đã commit phải vẫn có mặt
    — đó là mặt duy nhất còn ĐO ĐƯỢC của `t41`, giữ lại làm chốt (1). Các mặt của MÁY (2)–(6)
    chốt "danh sách y hệt nền", không chốt phán quyết (N22).
    Ranh giới với `t37`: `t37` = tệp chưa add thì KHÔNG quét; ở đây mọi tệp đều ĐÃ add.
    """
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        cay = tmp / "cay"
        (cay / "ops").mkdir(parents=True)
        for l in (["init", "-q"], ["config", "user.email", "t@t"], ["config", "user.name", "t"]):
            subprocess.run(["git", "-C", str(cay)] + l, capture_output=True, timeout=60)
        bq = _bash_nen_voi_chua_chuyen(tmp, {})
        (cay / ".gitignore").write_text("*.py\n", encoding="utf-8")   # luật CỦA KHO, đã commit
        (cay / "ops" / "ban.py").write_text('import shutil\nshutil.which("bash")\n', encoding="utf-8")
        subprocess.run(["git", "-C", str(cay), "add", "-f", ".gitignore", "ops/ban.py"],
                       capture_output=True, timeout=60)

        def danh_sach(env=None):
            return sorted((_quet(cay, bq, env=env)[1].get("co_loi_goi_tran") or {}))

        nen = danh_sach()
        bang("ops/ban.py" in nen,
             f"(1) tệp ĐÃ ADD (`add -f`) khớp `.gitignore` ĐÃ COMMIT vẫn phải trong danh sách — "
             f"cổng đang nghe luật ignore trở lại: {nen}")
        (cay / "ops" / ".gitignore").write_text("ban.py\n", encoding="utf-8")   # CHƯA theo dõi
        bang(danh_sach() == nen, "(2) `.gitignore` CHƯA theo dõi đổi được danh sách")
        (cay / ".git" / "info").mkdir(exist_ok=True)
        (cay / ".git" / "info" / "exclude").write_text("ban.py\n", encoding="utf-8")
        bang(danh_sach() == nen, "(3) `.git/info/exclude` đổi được danh sách")
        ngoai = tmp / "gitignore_toan_cuc"
        ngoai.write_text("ban.py\n", encoding="utf-8")
        subprocess.run(["git", "-C", str(cay), "config", "core.excludesFile", str(ngoai)],
                       capture_output=True, timeout=60)
        bang(danh_sach() == nen, "(4) `core.excludesFile` cục bộ đổi được danh sách")
        gc = tmp / "gitconfig_toan_cuc"
        gc.write_text(f"[core]\n\texcludesFile = {ngoai}\n", encoding="utf-8")
        bang(danh_sach(dict(os.environ, GIT_CONFIG_GLOBAL=str(gc))) == nen,
             "(5) `core.excludesFile` trong `~/.gitconfig` (qua `GIT_CONFIG_GLOBAL`) đổi được danh sách")
        xdg = tmp / "xdg" / "git"
        xdg.mkdir(parents=True)
        (xdg / "ignore").write_text("ban.py\n", encoding="utf-8")
        rong = tmp / "gitconfig_rong"
        rong.write_text("", encoding="utf-8")
        bang(danh_sach(dict(os.environ, XDG_CONFIG_HOME=str(tmp / "xdg"),
                            GIT_CONFIG_GLOBAL=str(rong))) == nen,
             "(6) `$XDG_CONFIG_HOME/git/ignore` — đường ignore MẶC ĐỊNH của git — đổi được danh sách")


@ca
def t50_PEP695_type_params_phai_duoc_tham_va_phai_CHE_duoc():
    """THUỘC TÍNH: tham số kiểu PEP 695 phải được THĂM (không sập) và phải CHE được tên ngoài.

    SINH TỪ CROSS-REVIEW CODEX vòng 8 trên `f6189e3`. Đo trên **Python 3.12.3 THẬT**:
        `def f[T: shutil.which("bash")](): pass`        ⇒ **KeyError** — CLI thoát 1
        `class C[T: subprocess.run(["bash"])]: pass`    ⇒ **KeyError**
        `def f[subprocess](): subprocess.run(["bash"])` ⇒ `[(3, 4)]` — **BẮT OAN**, vì
                                                           `subprocess` ở đó là TypeVar
    Lời gọi ở `bound` được `ast.walk` tìm thấy (nên nó vào `ung_vien`) mà bộ duyệt phạm vi
    KHÔNG thăm (nên không có mục trong bảng tra) ⇒ `KeyError`. Đó là **sập**, không phải bỏ sót.

    CA NÀY CÓ MỘT NỀN RIÊNG, và nó tự khai: máy soạn bản vá chạy **Python 3.11**, nơi cú pháp
    PEP 695 còn chưa parse nổi — `SyntaxError`, chưa tới `KeyError`. Nên ca đi tìm một trình
    thông dịch **>= 3.12** và chạy phép đo QUA TIẾN TRÌNH CON của nó. Không tìm thấy thì
    `BoQuaMoiTruong` kèm chẩn đoán ĐO ĐƯỢC — `KHÔNG ĐO ĐƯỢC` không được lặng lẽ thành xanh,
    và bộ chấm sẽ ghi đột biến đích là KHÔNG_ĐO_ĐƯỢC chứ không phải "giết đúng".
    CI ghim `python-version: "3.12"` ở cả ba chỗ gọi bộ ca này, nên trên CI nó CHẠY.
    """
    ung = [x for x in (shutil.which("python3.12"), shutil.which("python3.13"),
                       "/usr/bin/python3.12", "/usr/bin/python3.13") if x and Path(x).exists()]
    if sys.version_info >= (3, 12):
        ung.insert(0, sys.executable)
    py = next((x for x in ung if subprocess.run(
        [x, "-c", "import sys;raise SystemExit(0 if sys.version_info>=(3,12) else 1)"],
        capture_output=True, timeout=60).returncode == 0), None)
    if py is None:
        raise BoQuaMoiTruong(
            f"không có trình thông dịch >= 3.12 trên máy này (đang chạy "
            f"{'.'.join(map(str, sys.version_info[:3]))}); cú pháp PEP 695 chưa parse được nên "
            f"KHÔNG ĐO ĐƯỢC. CI ghim 3.12 nên ở đó ca này chạy.")

    ma = (
        "import json, runpy, sys\n"
        "m = runpy.run_path(sys.argv[1])\n"
        "ra = {}\n"
        "for ten, than in json.loads(sys.argv[2]).items():\n"
        "    try:\n"
        "        ra[ten] = ['ok', m['_loi_goi_tran'](than)]\n"
        "    except Exception as ex:\n"
        "        ra[ten] = [type(ex).__name__, str(ex)[:120]]\n"
        "print('KQ ' + json.dumps(ra))\n")
    hd = {
        "bound":   'import shutil\ndef f[T: shutil.which("bash")]():\n    pass\n',
        "co_so":   'import subprocess\nclass C[T: subprocess.run(["bash"])]:\n    pass\n',
        "che_ten": 'import subprocess\ndef f[subprocess]():\n    subprocess.run(["bash"])\n',
        # CHỨNG (control) cho chốt (3): phép CHE bằng THAM SỐ THƯỜNG, không dính PEP 695.
        # Nếu chính nó cũng hỏng thì cơ chế giải tên CHUNG đã hỏng — thứ `t33` trói — và ca
        # này KHÔNG ĐO ĐƯỢC chứ không phải ĐỎ.
        "chung_che_thuong": 'import subprocess\ndef f(subprocess):\n    subprocess.run(["bash"])\n',
        "chung_bat_thuong": 'import subprocess\nsubprocess.run(["bash"])\n',
        # Mặt TIỀN ĐỀ thứ BA, thêm ở r16 sau một phép đo: `bn_import_ro_ri_qua_pham_vi`
        # (đích `t33`) giết ca này ⇒ bán kính 2/53. Lý do đo được: chốt (4) hỏi "tham số kiểu
        # của alias có RÒ ra phạm vi chứa không", mà khi `import` đã rò qua MỌI phạm vi thì
        # câu hỏi ấy vô nghĩa — nó nói về cơ chế CÔ LẬP PHẠM VI chung, thứ `t33` trói.
        "chung_pham_vi_co_lap": 'def a():\n    import subprocess\ndef b():\n    subprocess.run(["bash"])\n',
        # N47 (r16) — `type X[T] = ...` MO MOT PHAM VI CHU THICH RIENG. Ban r15 chi ghi TEN
        # alias roi duyet tiep XUONG, nen `T` cua alias ro ri ra pham vi CHUA va nuot mot
        # lan phong bash THAT o dong duoi. Do duoc tren 3.12.3: `[]`, mong `[[3, 0]]`.
        "alias_khong_ro_ri": 'import subprocess\ntype X[subprocess] = int\nsubprocess.run(["bash"])\n',
        # Chieu NGUOC: trong CHINH gia tri cua alias thi `subprocess` LA TypeVar ⇒ khong bat.
        "alias_che_trong_gia_tri": 'import subprocess\ntype X[subprocess] = subprocess.run(["bash"])\n',
        # Gia tri alias KHONG co tham so kieu thi van la module that ⇒ bat.
        "alias_gia_tri_that": 'import subprocess\ntype X = subprocess.run(["bash"])\n',
        # N76 (r21, G7 vong 15) — pham vi CHU THICH cua `type` trong than lop NHIN THAY lop ay.
        # Do tren 3.12: `C.X.__value__` IN RA `OK`, ma r20 tra `[]` (bo qua than lop).
        # KHONG che ten o module, co chu dich: `t50` do TAM NHIN cua pham vi chu thich, khong do
        # luat "bat ky rang buoc import" cua N76 (ban dau co `subprocess = object()` o module va
        # dot bien `bn_mot_rang_buoc_thay_bat_ky` giet THEM ca nay — ban kinh 2/53).
        "alias_thay_lop_import": 'class C:\n    import subprocess\n    type X = subprocess.run(["bash"])\n',
    }
    pc = subprocess.run([py, "-c", ma, str(BASH_NEN), json.dumps(hd)],
                        capture_output=True, text=True, timeout=180)
    dong = [l for l in pc.stdout.splitlines() if l.startswith("KQ ")]
    dung(dong, f"giàn giáo hỏng trên {py}: rc={pc.returncode}\n{pc.stdout[-500:]}\n{pc.stderr[-500:]}")
    kq = json.loads(dong[-1][3:])

    bang(all(v[0] == "ok" for v in kq.values()),
         f"(1) tham số kiểu PEP 695 làm bộ giải SẬP: "
         f"{ {k: v for k, v in kq.items() if v[0] != 'ok'} } — lời gọi ở `bound` được `ast.walk` "
         f"thấy mà bộ duyệt không thăm thì bảng tra thiếu mục, và đó là `KeyError`, không phải "
         f"một phép đo")
    bang(kq["bound"][1] and kq["co_so"][1],
         f"(2) lời gọi `bash` trong `bound` của tham số kiểu bị BỎ SÓT: "
         f"bound={kq['bound'][1]} co_so={kq['co_so'][1]}")
    # N25 — CHỐT TIỀN ĐỀ TRƯỚC KẾT LUẬN. Chốt (3) chỉ đọc được khi cơ chế giải tên CHUNG còn
    # chạy: tham số thường phải che được, và lời gọi trần thường phải bắt được. Thiếu tiền đề
    # ấy thì việc `che_ten` ra `[]` không nói gì về PEP 695 — nó nói về `t33`.
    # Đo được: `bn_ten_bi_che_khong_chan` và `bn_khong_giai_callee` (đích `t33`) giết ca này
    # ⇒ bán kính 2/52, vì bản đầu kết luận thẳng mà không hỏi tiền đề.
    if (kq["chung_che_thuong"][1] or not kq["chung_bat_thuong"][1]
            or kq["chung_pham_vi_co_lap"][1]):
        raise BoQuaMoiTruong(
            f"KHÔNG ĐO ĐƯỢC: cơ chế giải tên CHUNG đã hỏng trên nền này — tham số thường "
            f"che={kq['chung_che_thuong'][1]} (mong []), lời gọi trần thường "
            f"bắt={kq['chung_bat_thuong'][1]} (mong khác rỗng), `import` trong hàm A rò sang "
            f"hàm B={kq['chung_pham_vi_co_lap'][1]} (mong []). Thuộc tính PEP 695 nói về một "
            f"phạm vi RIÊNG, nên nó không đọc được khi chính phép cô lập phạm vi đã đổ; đó "
            f"là chuyện của `t33`.")
    bang(not kq["che_ten"][1],
         f"(3) tên tham số kiểu KHÔNG che được tên ngoài: {kq['che_ten'][1]} — "
         f"`def f[subprocess]()` thì `subprocess` trong thân là TypeVar, không phải module")
    bang(bool(kq["alias_khong_ro_ri"][1]) and bool(kq["alias_gia_tri_that"][1])
         and not kq["alias_che_trong_gia_tri"][1],
         f"(4) phạm vi của `type X[T] = …` KHÔNG đúng (N47): "
         f"không_rò_rỉ={kq['alias_khong_ro_ri'][1]} (mong khác rỗng — `T` của alias không "
         f"được che tên ở dòng SAU nó), giá_trị_thật={kq['alias_gia_tri_that'][1]} (mong "
         f"khác rỗng), che_trong_giá_trị={kq['alias_che_trong_gia_tri'][1]} (mong rỗng — "
         f"BÊN TRONG giá trị của alias thì `subprocess` mới là TypeVar). Alias generic có "
         f"phạm vi chú thích RIÊNG; coi nó là một phép gán thường thì tham số kiểu rò ra "
         f"ngoài và nuốt lời gọi bash thật ở dòng dưới.")
    bang(bool(kq["alias_thay_lop_import"][1]),
         f"(5) phạm vi chú thích của `type X = …` trong THÂN LỚP không nhìn thấy lớp ấy (N76, "
         f"G7 vòng 15): {kq['alias_thay_lop_import'][1]} (mong khác rỗng — `import subprocess` "
         f"trong thân lớp là thứ `C.X.__value__` đọc, và nó chạy bash thật)")


@ca
def t51_cache_phai_HET_HIEU_LUC_khi_chinh_TEP_ung_vien_doi():
    """THUỘC TÍNH: khoá cache gom mọi ĐẦU VÀO, nhưng kết quả sinh ra từ một TỆP — nên tệp đổi
    thì câu trả lời cũ phải hết hiệu lực.

    SINH TỪ CROSS-REVIEW CODEX vòng 10 trên `8180970`. `tim_bash()` không đọc đầu vào để ra
    phán quyết; nó CHẠY một phép thử NĂNG LỰC trên một tệp. Thay chính tệp ấy tại chỗ — một
    trình cài ghi đè thứ `CONG_CU_BASH` trỏ tới — thì khoá không đổi một bit. Tái hiện được
    CẢ HAI CHIỀU trước khi vá:
      tốt → xấu: cache trả `/tmp/f1cache/bash` trong khi đo lại trả `None` ("phép argv: rc=7");
      xấu → tốt: cache trả `None` trong khi đo lại trả đúng đường ấy.
    Chiều THỨ HAI mới là chiều độc: cổng báo "KHÔNG CÓ bash" trên một máy ĐÃ CÓ, và người đọc
    log không có cách nào biết mình đang đọc một câu trả lời quá hạn.

    N94 (r26) — CACHE ĐÃ GỠ theo quyết định chủ kho, sau lần thứ SÁU cùng hình dạng (codex vòng 20:
    NỘI DUNG tệp mà `BASH_ENV` trỏ tới đổi, cache vẫn trả đường cũ). Đo trước khi chọn: trúng
    cache 3,0 ms, đo lại 5,7 ms. Chốt (3) nay ĐẢO CHIỀU: mọi lần gọi phải ĐO LẠI. Các chốt (1),
    (2), (4), (6), (7) giữ nguyên làm hàng rào: một cache dựng lại sẽ làm chúng đỏ. Chốt (8) đo
    đúng ca vòng 20. Tên ca giữ nguyên vì mỏ neo đột biến trỏ tới nó.
    """
    if not Path("/bin/sh").exists():
        raise BoQuaMoiTruong("nền này không có `/bin/sh` để dựng ứng viên giả — KHÔNG ĐO ĐƯỢC")
    m = runpy.run_path(str(BASH_NEN))
    tim = m["tim_bash"]
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        w = tmp / "bash"
        rong = tmp / "rong"
        rong.mkdir()

        def viet(than):
            w.write_text(than, encoding="utf-8")
            w.chmod(0o755)

        TOT = '#!/bin/sh\nexec /bin/bash "$@"\n'
        XAU = "#!/bin/sh\nexit 7\n"
        cu_env = {k: os.environ.get(k) for k in ("CONG_CU_BASH", "PATH", "BASH_ENV")}
        # `finally` phải khôi phục CẢ HAI kể cả khi chúng vốn VẮNG — chốt (5) gỡ `PATH`.
        try:
            os.environ["CONG_CU_BASH"] = str(w)
            os.environ["PATH"] = str(rong)          # cô lập: KHÔNG ứng viên nào khác

            viet(TOT)
            tot1 = tim()[0]
            if tot1 != str(w):
                raise BoQuaMoiTruong(
                    f"không dựng được ứng viên `bash` giả trên nền này: `tim_bash()` trả "
                    f"{tot1!r}, mong {str(w)!r}. Không có tiền đề thì không có phép đo.")

            viet(XAU)
            xau_cache = tim()[0]
            xau_do_lai = tim(dung_cache=False)[0]
            bang(xau_cache == xau_do_lai,
                 f"(1) TỐT → XẤU: cache trả {xau_cache!r} còn phép đo lại trả "
                 f"{xau_do_lai!r} — cùng một đường, cùng một môi trường, mà hai câu trả lời "
                 f"khác nhau. Khoá gom đủ mọi đầu vào vẫn không cứu được, vì phán quyết "
                 f"không sinh ra từ đầu vào: nó sinh ra từ phép thử NĂNG LỰC trên một TỆP.")

            viet(XAU)
            tim()
            viet(TOT)
            tot_cache = tim()[0]
            tot_do_lai = tim(dung_cache=False)[0]
            bang(tot_cache == tot_do_lai,
                 f"(2) XẤU → TỐT: cache trả {tot_cache!r} còn phép đo lại trả "
                 f"{tot_do_lai!r} — đây là chiều độc: cổng báo KHÔNG CÓ `bash` trên một máy "
                 f"ĐÃ CÓ. `None` ở đây nghĩa là KHÔNG ĐO ĐƯỢC, nên người gọi phải ĐỎ, và "
                 f"nó sẽ ĐỎ vì một câu trả lời quá hạn.")

            viet(TOT)
            dem = [0]
            that = tim.__globals__["_do_nang_luc"]

            def dem_phep(*a, **k):
                dem[0] += 1
                return that(*a, **k)

            tim.__globals__["_do_nang_luc"] = dem_phep
            try:
                tim()
                dau = dem[0]
                for _ in range(20):
                    tim()
                sau = dem[0]
            finally:
                tim.__globals__["_do_nang_luc"] = that
            # (4) N56 (r17) — VÂN TAY PHẢI PHỦ CẢ TẬP ỨNG VIÊN, không chỉ những cái ĐÃ THỬ.
            #     N51 chụp vân tay của `chan_doan`; một `bash` MỚI xuất hiện trong một thư mục
            #     `PATH` KHÔNG đổi thì không ứng viên cũ nào đổi ⇒ vân tay khớp ⇒ trả lời cũ.
            #     Đo được ở vòng 11: thư mục rỗng ⇒ cache `(None, [])`; thêm một symlink
            #     `bash`; cache vẫn `None` còn `dung_cache=False` tìm thấy. Chiều VẮNG → CÓ
            #     là chiều độc: cổng báo KHÔNG CÓ `bash` trên máy ĐÃ CÓ.
            trong = tmp / "trong"
            trong.mkdir()
            os.environ.pop("CONG_CU_BASH", None)
            os.environ["PATH"] = str(trong)
            if tim()[0] is not None:
                raise BoQuaMoiTruong(
                    "không dựng được một `PATH` KHÔNG có `bash` nào trên nền này — "
                    "không có tiền đề thì không có phép đo")
            (trong / "bash").symlink_to(w)
            them_cache = tim()[0]
            them_moi = tim(dung_cache=False)[0]
            bang(them_cache == them_moi,
                 f"(4) VẮNG → CÓ: cache trả {them_cache!r} còn phép đo lại trả {them_moi!r}. "
                 f"Ứng viên MỚI không làm ứng viên CŨ nào đổi, nên vân tay từng tệp vẫn "
                 f"khớp — phải ĐẾM LẠI tập ứng viên, không chỉ soát những cái đã thử.")

            # (5) N57 (r17) + N62 (r18) — `PATH` VẮNG ≠ `PATH` RỖNG, và RỖNG là THƯ MỤC HIỆN TẠI.
            #     SỬA LẠI Ở r18, và bản cũ của chính chốt này là thứ phải sửa. r17 khẳng định
            #     *"một `PATH=""` tường minh nghĩa là đừng tìm ở đâu cả"*, gán nó cho HỆ ĐIỀU
            #     HÀNH, rồi KHOÁ nó bằng `bang(... and not rong)` — mà KHÔNG ĐO. Vòng 12 đo:
            #     `os.get_exec_path({"PATH": ""})` ⇒ `['']`, và `subprocess.run(["bash"],
            #     env={"PATH": ""})` ở thư mục có `bash` ⇒ `rc=0`. Một chốt khoá cứng một ngữ
            #     nghĩa SAI thì tệ hơn không có chốt: nó làm bản vá ĐÚNG thành ĐỎ.
            #     Nay đo cả ba mặt, và mặt RỖNG đo bằng một thư mục hiện tại THẬT SỰ có `bash`.
            os.environ.pop("CONG_CU_BASH", None)
            os.environ.pop("PATH", None)
            vang = m["ung_vien"]()
            cho_bash = tmp / "cwd_co_bash"
            cho_bash.mkdir()
            (cho_bash / "bash").symlink_to(w)
            cu_cwd = os.getcwd()
            try:
                os.chdir(cho_bash)
                rong = m["ung_vien"](path="")
            finally:
                os.chdir(cu_cwd)
            bang(bool(vang),
                 f"(5a) `PATH` VẮNG cho {len(vang)} ứng viên — mong lùi về `os.defpath` = "
                 f"{os.defpath!r} như `os.get_exec_path()` làm. Gộp VẮNG vào RỖNG là để cổng "
                 f"báo KHÔNG ĐO ĐƯỢC trên một máy chạy `bash` được.")
            bang(rong == [os.path.abspath(cho_bash / "bash")],
                 f"(5b) `PATH=\"\"` ở thư mục CÓ `bash` cho {rong!r} — mong "
                 f"{[os.path.abspath(cho_bash / 'bash')]!r}. Thành phần RỖNG là thư mục HIỆN TẠI "
                 f"(`os.get_exec_path({{'PATH': ''}})` ⇒ `['']`). Chuỗi KHÔNG được thành TÊN TRẦN "
                 f"`bash` (phép thử sẽ đi tìm theo PATH), và từ N113 (r32) nó là đường TUYỆT ĐỐI "
                 f"tính theo cwd LÚC ĐO — `./bash` trả ra ngoài sẽ trỏ tệp khác khi người gọi đổi cwd.")

            # (9) N113 (r32, codex vòng 26 — P1) — đường TRẢ VỀ phải là đúng tệp ĐÃ THỬ, bất kể cwd
            #     của người gọi về sau. Đo được trên r31: `tim_bash(path="")` ở thư mục A (có
            #     `bash` tốt) trả `./bash`; chạy nó với `cwd` = B (có một `bash` khác) in
            #     `WRONG_CANDIDATE`.
            b9 = tmp / "cwd_khac"
            b9.mkdir()
            (b9 / "bash").write_text("#!/bin/sh\necho WRONG_CANDIDATE\n", encoding="utf-8")
            (b9 / "bash").chmod(0o755)
            viet(TOT)
            try:
                os.chdir(cho_bash)
                duong9 = tim(path="")[0]
            finally:
                os.chdir(cu_cwd)
            ra9 = (subprocess.run([duong9, "-c", "echo DUNG"], cwd=b9, capture_output=True,
                                  text=True, timeout=60).stdout.strip() if duong9 else None)
            bang(duong9 is not None and os.path.isabs(duong9) and ra9 == "DUNG",
                 f"(9) N113: `tim_bash(path='')` phải trả đường TUYỆT ĐỐI của tệp đã thử, và chạy nó "
                 f"từ một cwd KHÁC vẫn là tệp ấy: trả {duong9!r}, chạy ra {ra9!r}")

            # (6) N61 (r18) — khoá cache theo TOÀN BỘ môi trường. `bash` đọc môi trường của
            #     CHÍNH NÓ; đo được ở vòng 12: cache `/bin/bash` xong, đặt `BASH_ENV` trỏ vào
            #     một tệp `exit 7` ⇒ cache vẫn trả đường cũ, còn đo lại trả `None`.
            #     Ứng viên giữ NGUYÊN, nên N56 (đếm lại ứng viên) KHÔNG cứu được ca này — đó
            #     là lý do chốt này tách được N61 khỏi N56.
            os.environ["CONG_CU_BASH"] = str(w)
            rong_dir = tmp / "rong2"
            rong_dir.mkdir()
            os.environ["PATH"] = str(rong_dir)
            viet(TOT)
            if tim()[0] != str(w):
                raise BoQuaMoiTruong("không dựng lại được ứng viên giả cho chốt (6)")
            env_xau = tmp / "bash_env_xau.sh"
            env_xau.write_text("exit 7\n", encoding="utf-8")
            os.environ["BASH_ENV"] = str(env_xau)
            try:
                env_cache = tim()[0]
                env_moi = tim(dung_cache=False)[0]
            finally:
                os.environ.pop("BASH_ENV", None)
            bang(env_cache == env_moi,
                 f"(6) `BASH_ENV` đổi mà cache trả {env_cache!r} còn đo lại trả {env_moi!r}. "
                 f"Phán quyết sinh ra từ phép thử NĂNG LỰC, mà `bash` đọc môi trường của chính "
                 f"nó — danh sách biến 'có ảnh hưởng' không bao giờ đủ, nên khoá phải băm TOÀN "
                 f"BỘ môi trường.")

            # (8) N94 (r26, codex vòng 20) — NỘI DUNG tệp mà `BASH_ENV` trỏ tới đổi: lần gọi sau
            #     phải thấy. Đo được trên r25: tệp rỗng ⇒ `/usr/bin/bash` được cache; ghi `exit 7`
            #     vào CHÍNH tệp ấy ⇒ cache vẫn trả đường cũ, đo lại trả `None`.
            env_tep = tmp / "bash_env_doi.sh"
            env_tep.write_text("", encoding="utf-8")
            os.environ["BASH_ENV"] = str(env_tep)
            try:
                truoc = tim()[0]
                env_tep.write_text("exit 7\n", encoding="utf-8")
                sau_doi = tim()[0]
            finally:
                os.environ.pop("BASH_ENV", None)
            bang(truoc == str(w) and sau_doi is None,
                 f"(8) nội dung tệp `BASH_ENV` đổi sang `exit 7`: trước {truoc!r}, sau {sau_doi!r} "
                 f"— mong `{w}` rồi `None`. Phán quyết cũ sống qua một thay đổi mà `bash` đọc.")

            # (10) N114 (r32, codex vòng 26) — HẠN TỔNG. Bốn ứng viên TREO ngay ở phép đầu; hạn riêng 2s,
            #     hạn tổng 2,5s. Có hạn tổng (tính cho TỪNG PHÉP) thì dừng quanh 2,5s và trả None kèm chẩn
            #     đoán "hết hạn TỔNG"; hạn chỉ tính giữa ỨNG VIÊN thì ~4s; không có thì ~8s. Treo ở phép
            #     ĐẦU chứ không ở phép mở đường dẫn: chốt này không được phụ thuộc phép thứ hai (đo được ở
            #     lượt đầy đủ r32: `bn_bo_kiem_mo_tep` giết thêm nó khi ứng viên treo ở phép hai).
            if not Path("/bin/sleep").exists():
                raise BoQuaMoiTruong("nền này không có `/bin/sleep` để dựng ứng viên TREO — KHÔNG ĐO ĐƯỢC")
            g = tim.__globals__
            cu_han = (g["_HAN_GIAY"], g["_HAN_TONG_GIAY"])
            treo = []
            for i10 in range(4):
                d10 = tmp / f"treo{i10}"
                d10.mkdir()
                (d10 / "bash").write_text("#!/bin/sh\nexec /bin/sleep 10\n", encoding="utf-8")
                (d10 / "bash").chmod(0o755)
                treo.append(str(d10))
            os.environ.pop("CONG_CU_BASH", None)
            g["_HAN_GIAY"], g["_HAN_TONG_GIAY"] = 2, 2.5
            try:
                t10 = time.monotonic()
                kq10, cd10 = tim(path=os.pathsep.join(treo), tat_ca=True)
                lau10 = time.monotonic() - t10
            finally:
                g["_HAN_GIAY"], g["_HAN_TONG_GIAY"] = cu_han
            # CHỈ đo hạn TỔNG: thời gian và chẩn đoán. KHÔNG khẳng định `kq10 is None` — "quá hạn là bị từ
            # chối" là thuộc tính của `t28` (đo được ở lượt đầy đủ r32: `bn_bo_han_treo` giết thêm chốt
            # này khi nó còn khẳng định cả kết quả). `tat_ca=True` để mọi ứng viên đều đi qua hạn tổng.
            bang(lau10 < 3.3 and any("hết hạn TỔNG" in c["ly_do"] for c in cd10),
                 f"(10) N114: bốn ứng viên treo, hạn riêng 2s, hạn tổng 2,5s: trả {kq10!r} sau "
                 f"{lau10:.2f}s, chẩn đoán {[c['ly_do'][:40] for c in cd10]}")

            # (7) N70 (r19) — ghi đè bằng TÊN TRẦN phải phân giải qua PATH, và phép thử CÙNG vân
            #     tay phải canh CÙNG một tệp. Đo được ở vòng 13: `./bash` giữ chỗ ở thư mục hiện
            #     tại, PATH trỏ bash thật, `CONG_CU_BASH=bash` — thay bash trong PATH bằng bản
            #     `exit 7` thì cache vẫn trả `bash`: vân tay đang `stat` NHẦM tệp giữ chỗ.
            khu = tmp / "ten_tran"
            (khu / "p").mkdir(parents=True)
            giu_cho = khu / "bash"
            # N113 (r32) — tệp giữ chỗ là một `bash` CHẠY ĐƯỢC: từ khi mọi ứng viên được tuyệt đối hoá,
            # một ghi đè tên trần KHÔNG phân giải qua PATH thành `<cwd>/bash`, và chỉ khi tệp ấy ĐẠT phép
            # thử thì sai lầm ấy mới lộ ra ở đường trả về (7a).
            giu_cho.write_text(TOT, encoding="utf-8")
            giu_cho.chmod(0o755)
            that_su = khu / "p" / "bash"
            that_su.write_text(TOT, encoding="utf-8")
            that_su.chmod(0o755)
            os.environ["CONG_CU_BASH"] = "bash"
            os.environ["PATH"] = str(khu / "p")
            cu_cwd7 = os.getcwd()
            try:
                os.chdir(khu)
                ten_tot = tim()[0]
                that_su.write_text(XAU, encoding="utf-8")
                ten_cache = tim()[0]
                ten_moi = tim(dung_cache=False)[0]
            finally:
                os.chdir(cu_cwd7)
            # (7a) N70 — đường TRẢ VỀ phải là đúng tệp đã được thử, đã phân giải qua PATH. Trước
            #      N94, thuộc tính này chỉ lộ qua vân tay cache; không còn cache thì đo thẳng nó.
            bang(ten_tot == str(that_su),
                 f"(7a) `CONG_CU_BASH=bash` (tên trần) trả {ten_tot!r} — mong đường ĐÃ PHÂN GIẢI "
                 f"{str(that_su)!r}. Trả tên trần là trả một thứ sẽ được tìm LẠI theo PATH lúc chạy, "
                 f"không phải tệp phép thử năng lực đã chứng minh.")
            bang(ten_cache == ten_moi,
                 f"(7) `CONG_CU_BASH=bash` (tên trần): cache trả {ten_cache!r} còn đo lại trả "
                 f"{ten_moi!r}. Phép thử chạy tên ấy QUA PATH, còn vân tay `stat` tệp `./bash` "
                 f"giữ chỗ — hai phép canh hai tệp khác nhau. Phải phân giải MỘT lần, rồi cả "
                 f"hai dùng chung đường đã phân giải.")

            bang(dau > 0 and sau - dau >= 20,
                 f"(3) N94 (r26) — MỌI lần gọi phải ĐO LẠI: lần đầu {dau} phép thử năng lực, "
                 f"sau 20 lượt nữa thành {sau}. Chủ kho đã GỠ cache sau sáu revision cùng hình "
                 f"dạng 'cache trả phán quyết cũ'; một cache dựng lại — dù có vân tay — là mở lại "
                 f"đúng lớp ấy.")
        finally:
            for k, v in cu_env.items():
                if v is None:
                    os.environ.pop(k, None)
                else:
                    os.environ[k] = v


@ca
def t49_duong_XAU_ra_JSON_HOP_LE_va_NGAY_GO_phai_duoc_DOC(goi_git=subprocess.run, nap=runpy.run_path):
    """THUỘC TÍNH: biên giới BÁO CÁO ra JSON hợp lệ, và NGÀY GỠ là một hạn ĐỌC ĐƯỢC.

    SINH TỪ CROSS-REVIEW CODEX vòng 8 trên `f6189e3`, ba trong sáu P2:
      (2) đường mang byte không giải mã được đi thẳng ra `json.dumps(ensure_ascii=False)` ⇒
          stdout phát lại byte thô và **một bộ đọc JSON UTF-8 nghiêm từ chối**. Đây đúng món
          **verdict r13 đã tự khai là CHƯA ĐO** — nợ đến hạn.
      (3) `_NGAY_GO` chỉ được nội suy vào chuỗi LÝ DO, **không mã nào so sánh nó**: đo được
          trên `f6189e3` — chỉ xuất hiện ở `Assign` và `FormattedValue`, không một `Compare`
          nào, không `import datetime`. Sau 2026-12-31 mọi mục ratchet pass VÔ HẠN. Lại đúng
          họ **N6-LOI-KHAI-RONG-HON-PHEP-DO**, lần thứ BA trong packet.
    Mặt (1) — cookie mã hoá lạ ⇒ `rc=3` chứ không traceback — nằm ở `t47` chứ không ở đây, và
    đó là một phép đo: fixture ấy chỉ nổ KHI `detect_encoding` được dùng, mà cơ chế ấy là của
    `t47`. Đặt ở đây thì `bn_giai_ma_cung_utf8` (đích `t47`) giết luôn ca này ⇒ bán kính 2/52.
    Mặt (4) — PEP 695 — nằm ở `t50`, vì nó cần một nền Python >= 3.12 riêng.

    Mỗi chốt kèm CHIỀU NGƯỢC: (3) ĐÚNG ngày gỡ vẫn phải qua; (2) đường Unicode thường vẫn
    phải đọc được nguyên vẹn.
    """
    def _add(d, rel):        # #671: `goi_git` cho `t63` tráo bằng chứng TỪNG bước stage; `rc` PHẢI được đo
        ga = goi_git(["git", "-C", str(d), "add", "--", rel], capture_output=True, text=True, timeout=60)
        if ga.returncode:
            raise BoQuaMoiTruong(f"KHÔNG ĐO ĐƯỢC: git add {rel} rc={ga.returncode} {ga.stderr[:200]!r}")

    def _kho(tmp, ten):
        d = tmp / ten
        (d / "ops").mkdir(parents=True)
        for l in (["init", "-q"], ["config", "user.email", "t@t"], ["config", "user.name", "t"]):
            subprocess.run(["git", "-C", str(d)] + l, capture_output=True, timeout=60)
        return d

    def _stage_byte(d, ten: bytes, than: str):
        """#671 — đặt tên BYTE THÔ thẳng vào INDEX, KHÔNG qua hệ tệp.

        `quet` đọc từ INDEX (`t46`), nên cây làm việc không cần mang tên ấy. Đi qua đĩa thì
        đo HỆ TỆP chứ không đo cổng: windows-latest (run 36454930689) ra `[]` ở chiều ngược
        — tái hiện đúng chữ trên Linux bằng `git add -A` hỏng cả lượt. `rc` PHẢI được đo:
        không stage được là KHÔNG ĐO ĐƯỢC, không phải một cây rỗng xanh/đỏ oan."""
        # Cây làm việc CŨNG mang tệp khi nền cho phép: t49 đo biên giới BÁO CÁO, không đo
        # nguồn đọc — thiếu tệp trên đĩa thì đột biến `bn_doc_cay_lam_viec` (đích `t46`)
        # giết luôn t49 (đo được: t49 vào bán kính của đột biến ấy). Nền từ chối tên ấy thì INDEX vẫn đủ.
        try:
            (d / ten.decode("utf-8", "surrogateescape")).write_text(than, encoding="utf-8")
        except (OSError, UnicodeError):
            pass
        oid = goi_git(["git", "-C", str(d), "hash-object", "-w", "--stdin"],
                      input=than.encode("utf-8"), capture_output=True, timeout=60)
        r = goi_git(["git", "-C", str(d), "update-index", "--add", "-z", "--index-info"],
                    input=b"100644 " + oid.stdout.strip() + b"\t" + ten + b"\0",
                    capture_output=True, timeout=60)
        co = ten in goi_git(["git", "-C", str(d), "ls-files", "-z"], capture_output=True,
                            timeout=60).stdout.split(b"\0")
        if oid.returncode or r.returncode or not co:
            raise BoQuaMoiTruong(f"KHÔNG ĐO ĐƯỢC: INDEX không nhận tên {ten!r}: "
                                 f"rc={oid.returncode}/{r.returncode} {r.stderr[:200]!r}")

    BAN = 'import shutil\nb = shutil.which("bash")\n'
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        bq = _bash_nen_voi_chua_chuyen(tmp, {})

        # (2) đường mang byte xấu ⇒ JSON vẫn đọc được bằng UTF-8 nghiêm. Chiều ngược: đường
        #     Unicode thường vẫn nguyên vẹn.
        d = _kho(tmp, "duong")
        (d / "ops" / "bình_thường.py").write_text(BAN, encoding="utf-8")
        _add(d, "ops/bình_thường.py")
        _stage_byte(d, b"ops/xau_\xff.py", BAN)
        pc = subprocess.run([sys.executable, str(bq), "quet", "--root", str(d), "--json"],
                            capture_output=True, timeout=180)
        try:
            bao = json.loads(pc.stdout.decode("utf-8"))
            doc_duoc, ly = True, ""
        except Exception as e:                                        # noqa: BLE001
            bao, doc_duoc, ly = {}, False, f"{type(e).__name__}: {e}"
        bang(doc_duoc, f"(2) đường mang byte thô làm JSON KHÔNG đọc được: {ly} — giữ byte cho "
                       f"việc đối chiếu INDEX là đúng, nhưng biên giới BÁO CÁO phải an toàn")
        bang("ops/bình_thường.py" in (bao.get("co_loi_goi_tran") or {}),
             f"(2) chiều ngược: đường Unicode THƯỜNG bị bóp méo: "
             f"{sorted(bao.get('co_loi_goi_tran') or {})}")

        # (2b)(2c) N48 (r16) — HAI LỚP, và MỖI LỚP PHẢI ĐO ĐƯỢC MỘT MÌNH.
        #   lớp (a) `_duong_bao_cao` làm sạch TỪNG TRƯỜNG;  lớp (b) `_ra_json` làm sạch CẢ
        #   bản báo cáo. Cả hai cùng che lối `--json`, nên nếu chỉ đo lối ấy thì một bản vá
        #   gỡ (a) đi vẫn xanh — đo được: hai đột biến `bn_duong_xau_ra_JSON_tho` và
        #   `bn_loi_ra_duong_tho` KHÔNG GIẾT GÌ khi ca này chỉ đọc JSON.
        #   Lối NGƯỜI ĐỌC cũng KHÔNG đo được (a): nền này có `sys.stdout.errors ==
        #   'surrogateescape'`, nên `print` một surrogate lạc KHÔNG ném. Đo được, và đó là lý
        #   do bản đầu của chốt (2c) im lặng. Nên (a) được đo THẲNG trên TRƯỜNG, gọi `quet`
        #   trong tiến trình — không qua một lối ra nào cả.
        def _co_surrogate(x):
            if isinstance(x, str):
                return any(0xD800 <= ord(c) <= 0xDFFF for c in x)
            if isinstance(x, dict):
                return any(_co_surrogate(k) or _co_surrogate(v) for k, v in x.items())
            if isinstance(x, (list, tuple)):
                return any(_co_surrogate(v) for v in x)
            return False

        d_loi = _kho(tmp, "loi")
        _stage_byte(d_loi, b"ops/hong_\xff.py", "def f(:\n")
        mq = runpy.run_path(str(bq))
        _, bao_ok = mq["quet"](d)              # cây đường XẤU, cú pháp LÀNH  ⇒ lối thành công
        rc_l, bao_l = mq["quet"](d_loi)        # cây đường XẤU, cú pháp HỎNG ⇒ lối fail-close
        # r17 — ĐỔI ĐỐI TƯỢNG ĐO theo N54. KHOÁ nay CỐ Ý giữ đường NGUYÊN VẸN (kể cả
        # surrogate), vì dùng phép hiển thị làm khoá thì hai đường khác nhau ĐÈ nhau — xem
        # chốt (2d). Thứ phải sạch là trường HIỂN THỊ `ly_do`, và biên giới stdout.
        bang(not _co_surrogate(bao_ok.get("ly_do", "")),
             f"(2b) lối THÀNH CÔNG: trường HIỂN THỊ `ly_do` còn mang surrogate lạc — "
             f"{bao_ok.get('ly_do', '')!r}")
        # N25 — CHỐT TIỀN ĐỀ TRƯỚC KẾT LUẬN. Cây này chỉ đi vào nhánh fail-close khi CƠ CHẾ
        # phân tích cú pháp còn chạy; đó là thứ `t27`/`t25` trói, không phải ca này. Đo được:
        # `bn_quet_theo_chuoi` (đích `t27`) làm cây ra `rc=0 DAT` và giết ca này ⇒ bán kính
        # 2/53, vì bản đầu kết luận thẳng mà không hỏi tiền đề.
        if rc_l == 0 or bao_l.get("trang_thai") != "KHONG_DO_DUOC":
            raise BoQuaMoiTruong(
                f"KHÔNG ĐO ĐƯỢC: cây có tệp cú pháp HỎNG mà cổng không fail-close — "
                f"rc={rc_l} trạng_thái={bao_l.get('trang_thai')}. Ranh giới BÁO CÁO của lối "
                f"lỗi không đọc được khi lối lỗi chưa được đi vào; đó là chuyện của `t27`.")
        bang(not _co_surrogate(bao_l.get("ly_do", "")),
             f"(2b) lối LỖI: trường HIỂN THỊ `ly_do` còn mang surrogate lạc — "
             f"{bao_l.get('ly_do', '')!r}. Lối thành công sạch mà lối lỗi thô thì hàng rào "
             f"chỉ che được lối đi đẹp; luật phải đi theo TRƯỜNG, không theo nhánh.")
        pl = subprocess.run([sys.executable, str(bq), "quet", "--root", str(d_loi), "--json"],
                            capture_output=True, timeout=180)
        bang(not any(b > 127 for b in pl.stdout),
             f"(2c) stdout JSON còn byte ngoài ASCII (vị trí đầu: "
             f"{next((i for i, b in enumerate(pl.stdout) if b > 127), None)}) — `_ra_json` là "
             f"hàng rào THỨ HAI và phải bảo đảm stdout LUÔN giải mã được bằng UTF-8 nghiêm "
             f"ngặt, độc lập với việc từng trường đã sạch hay chưa.")

        # (3) NGÀY GỠ là một HẠN đọc được, không phải chữ trong lý do.
        d = _kho(tmp, "ngay")
        (d / "ops" / "no_cu.py").write_text(BAN, encoding="utf-8")
        _add(d, "ops/no_cu.py")
        bq2 = _bash_nen_voi_chua_chuyen(tmp, {"ops/no_cu.py": (1, "nợ giả")},
                                        ten="bash_nen_ngay_go.py")
        m = runpy.run_path(str(bq2))
        han = _dt.date.fromisoformat(m["_NGAY_GO"])
        rc_dung, _ = m["quet"](d, hom_nay=han)
        rc_qua, bao_qua = m["quet"](d, hom_nay=han + _dt.timedelta(days=1))
        bang(rc_dung == 0,
             f"(3) ĐÚNG ngày gỡ mà cổng đã đỏ: rc={rc_dung} — hạn là hạn, không phải hạn trừ một")
        bang(rc_qua != 0 and "ops/no_cu.py" in (bao_qua.get("ratchet_qua_han") or []),
             f"(3) QUA ngày gỡ một ngày mà ratchet vẫn pass: rc={rc_qua} "
             f"qua_han={bao_qua.get('ratchet_qua_han')} — ngày gỡ đang là chữ trang trí")

        # (2d) N54 (r17) — PHÉP HIỂN THỊ PHẢI ĐƠN ÁNH, và khoá báo cáo thì không dùng nó.
        #      Đặc tả r15 tự khai chỗ chưa đo: *"hai đường khác nhau về byte CÓ THỂ in ra
        #      giống nhau — chưa đo trường hợp ấy"*. Vòng 11 đo được: `ops/bad_<0xff>.py` và
        #      một đường chứa đúng bốn ký tự ASCII `\`,`x`,`f`,`f` cùng ra `ops/bad_\xff.py`.
        #      Chuỗi ấy LÀ KHOÁ của `co_loi_goi_tran`, nên một tệp ĐÈ vị trí của tệp kia và
        #      hạn ngạch đếm sai — một vi phạm tàng hình, đúng lớp `t48` đã gặp với `\r`/`\n`.
        d_va = _kho(tmp, "vacham")
        hai = [b"ops/va_\xff.py".decode("utf-8", "surrogateescape"), "ops/va_\\xff.py"]
        mv = nap(str(bq))                      # `nap`: `t63` thấy hai chốt THUẦN chạy TRƯỚC stage
        # #671 (S5, chủ kho 30-09) — (3) ở trên và hai chốt THUẦN dưới đây KHÔNG cần tên mang `\` trong INDEX
        # nên chạy TRƯỚC; phần stage đứng CUỐI ca, `BoQuaMoiTruong` nổ tự nhiên (Git for Windows bỏ tên ấy với
        # `Ignoring path` — lời khai trong thân `bd6ad5d`): không cơ chế hoãn nào để nuốt/ném sớm. `t63` khoá thứ tự.
        bang(mv["_duong_bao_cao"](hai[0]) != mv["_duong_bao_cao"](hai[1]),
             f"(2d) `_duong_bao_cao` vẫn KHÔNG đơn ánh: "
             f"{mv['_duong_bao_cao'](hai[0])!r} == {mv['_duong_bao_cao'](hai[1])!r}")
        bang(mv["_duong_bao_cao"]("ops/bình_thường.py") == "ops/bình_thường.py",
             "(2d) chiều ngược: đường Unicode THƯỜNG phải nguyên vẹn sau khi làm đơn ánh")
        # Tên thứ hai mang `\` NGUYÊN VĂN — trên Windows đó là dấu phân cách thư mục, nên
        # đi qua đĩa là đo sai thứ. Đi thẳng INDEX như hai cây trên.
        for ten in hai:
            _stage_byte(d_va, ten.encode("utf-8", "surrogateescape"), BAN)
        _, bao_va = mv["quet"](d_va)
        khoa = bao_va.get("co_loi_goi_tran") or {}
        bang(len(khoa) == 2,
             f"(2d) HAI đường khác nhau về byte chỉ còn MỘT khoá trong báo cáo: "
             f"{sorted(map(repr, khoa))} — phép hiển thị không đơn ánh mà lại được dùng làm "
             f"khoá, nên một tệp ĐÈ tệp kia và hạn ngạch đếm hụt. Khoá phải giữ đường NGUYÊN "
             f"VẸN; `_ra_json` lo phần an toàn ở biên giới.")


@ca
def t63_t49_hong_STAGE_tung_buoc_phai_BO_QUA_dung_buoc():
    """#671 (CA-KHOA-STAGING, review lượt 1–3: gỡ riêng từng chốt `rc`/`co` mà `t49` vẫn xanh, vì Linux
    luôn stage được) — chạy lại `t49` với git THẬT, chỉ TRÁO bằng chứng của ĐÚNG MỘT bước, đòi `t49` BỎ QUA
    mang dấu bước ấy. Ca `bo_ten` mô phỏng điều phiên Windows đo: Git for Windows bỏ tên mang dấu chéo ngược
    (`Ignoring path`, rc=0) — `t49` phải đo xong (3) và hai chốt THUẦN (2d) rồi MỚI bỏ qua (stage đứng CUỐI), không
    nuốt, không ném sớm; `bo_hong` bỏ riêng `hong_` (2b) — chỗ gọi mà mọi phép tráo khác dừng trước khi tới.
    ĐỐI CHỨNG: `t49` KHÔNG tráo chạy trước. Nó XANH mà `t49` ĐỎ dưới phép tráo ⇒ ĐỎ OAN khi stage hỏng (spec §2B)
    ⇒ giết; nó ĐỎ ⇒ KHÔNG ĐO ĐƯỢC (đột biến đích `t49` giữ bán kính 1/N); nó BỎ QUA (nền không stage được) ⇒
    chiều ĐỎ oan không đo ở nền ấy. `t49` bỏ qua vì lý do KHÁC dưới phép tráo ⇒ KHÔNG ĐO ĐƯỢC."""
    nhat_ky = []

    def trao(buoc, cach):
        def goi(lenh, **kw):
            nhat_ky.append(lenh)
            if buoc not in lenh:
                return subprocess.run(lenh, **kw)
            bo = {"bo_ten": bytes([92]), "bo_hong": b"hong_"}.get(cach)
            if bo is not None and bo in kw["input"]:
                return subprocess.CompletedProcess(lenh, 0, b"", b"Ignoring path")
            p = subprocess.run(lenh, **kw)
            return subprocess.CompletedProcess(lenh, 128 if cach == "rc" else p.returncode,
                                               b"" if cach == "rong" else p.stdout, p.stderr)
        return goi

    def nap(duong):
        m = runpy.run_path(duong); goc = m["_duong_bao_cao"]
        m["_duong_bao_cao"] = lambda s: nhat_ky.append(("(2d)", s)) or goc(s)
        return m

    try:
        t49_duong_XAU_ra_JSON_HOP_LE_va_NGAY_GO_phai_duoc_DOC()
        doi_chung_xanh = True
    except BoQuaMoiTruong:
        doi_chung_xanh = False
    except TinHieuChotCa as ex:
        raise BoQuaMoiTruong(f"KHÔNG ĐO ĐƯỢC: t49 ĐỎ cả khi KHÔNG tráo: {ex}") from ex
    for buoc, cach, dau in (("hash-object", "rc", "rc=128/0"), ("update-index", "rc", "rc=0/128"),
                            ("ls-files", "rong", "xau_"), ("add", "rc", "bình_thường"),
                            ("ops/no_cu.py", "rc", "no_cu"), ("update-index", "bo_ten", "va_"),
                            ("update-index", "bo_hong", "hong_")):
        nhat_ky.clear()
        try:
            t49_duong_XAU_ra_JSON_HOP_LE_va_NGAY_GO_phai_duoc_DOC(goi_git=trao(buoc, cach), nap=nap)
            ly = None
        except BoQuaMoiTruong as ex:
            ly = str(ex)
        except TinHieuChotCa as ex:
            bang(not doi_chung_xanh, f"({buoc}/{cach}) stage hỏng mà t49 ĐỎ thay vì BỎ QUA — ĐỎ OAN: {ex}")
            raise BoQuaMoiTruong(f"KHÔNG ĐO ĐƯỢC: t49 ĐỎ khi tráo {buoc}/{cach}, đối chứng không XANH: {ex}") from ex
        if ly is not None and not ly.startswith(("KHÔNG ĐO ĐƯỢC: INDEX", "KHÔNG ĐO ĐƯỢC: git add")):
            raise BoQuaMoiTruong(f"KHÔNG ĐO ĐƯỢC: t49 bỏ qua vì lý do khác khi tráo {buoc}/{cach}: {ly}")
        bang(ly is not None and dau in ly,
             f"({buoc}/{cach}) bằng chứng stage hỏng mà t49 không BỎ QUA đúng bước (chờ {dau!r}): {ly!r}")
        bang(cach != "bo_ten" or any("ops/no_cu.py" in lenh for lenh in nhat_ky),
             "(bo_ten) t49 BỎ QUA trước khi đo (3) — phần stage phải đứng CUỐI ca")
        bang(cach != "bo_ten" or any(lenh[0] == "(2d)" for lenh in nhat_ky),
             "(bo_ten) t49 BỎ QUA trước hai chốt THUẦN (2d) — phần stage phải đứng CUỐI ca")


@ca
def t48_khung_INDEX_giu_BYTES_va_anh_chup_ghim_BLOB():
    """THUỘC TÍNH: khung `ls-files -z` tách trên BYTES, và ảnh chụp đông cứng ghim BLOB.

    SINH TỪ CROSS-REVIEW CODEX vòng 7 trên `cf6e6cb` — hai P2, tái hiện cả hai:
      (1) `text=True` dịch dòng phổ quát TRƯỚC khi tách khung `\0`/`\t`, nên `ops/va\r.py` và
          `ops/va\n.py` — HAI đường khác nhau trong INDEX — gộp thành MỘT `rel`, và
          `_doc_noi_dung` ghi đè im lặng. Đo: tệp `\r` mang lời gọi trần, tệp `\n` sạch với OID
          cao hơn ⇒ `rc=0 DAT`, `co_loi_goi_tran` **RỖNG**. Vi phạm tàng hình.
      (2) `ANH_CHUP_DONG_CUNG` KHAI "không được sửa một byte" mà chỉ ĐO số lời gọi. Đo: đổi HẾT
          bảy `shutil.which("bash")` sang `subprocess.run(["bash"])`, giữ nguyên số 7 ⇒ vẫn
          `rc=0 DAT`, `lech_so` RỖNG. Đây đúng hình dạng kho đã đặt tên ở packet
          **N6-LOI-KHAI-RONG-HON-PHEP-DO**: lời khai rộng hơn phép đo.

    CHIỀU NGƯỢC nằm ngay trong chốt (2): ảnh chụp NGUYÊN BẢN phải cho `lech_oid` RỖNG, kẻo một
    bản vá "lúc nào cũng lệch" vẫn xanh ở đây.
    """
    def _g(d, *a):
        return subprocess.run(["git", "-C", str(d)] + list(a), capture_output=True,
                              text=True, timeout=60)

    BAN = 'import shutil\nb = shutil.which("bash")\n'
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)

        # (1) KHUNG tách trên BYTES — hai đường chỉ khác ký tự điều khiển.
        cay = tmp / "khung"
        (cay / "ops").mkdir(parents=True)
        for lenh in (["init", "-q"], ["config", "user.email", "t@t"], ["config", "user.name", "t"]):
            subprocess.run(["git", "-C", str(cay)] + lenh, capture_output=True, timeout=60)
        try:
            (cay / "ops" / "va\r.py").write_bytes(BAN.encode("utf-8"))
            (cay / "ops" / "va\n.py").write_bytes(b"X = 1\n" * 40)
        except OSError as e:
            raise BoQuaMoiTruong(f"nền này không đặt được tên tệp có ký tự điều khiển: {e}") from e
        _g(cay, "add", "-A")
        bq = _bash_nen_voi_chua_chuyen(tmp, {})
        _, bao = _quet(cay, bq)
        thay = sorted(bao.get("co_loi_goi_tran") or {})
        bang(thay == ["ops/va\r.py"],
             f"(1) hai đường KHÁC NHAU trong INDEX bị gộp làm một: thấy {thay!r}, mong "
             f"['ops/va\\r.py'] — dịch dòng phổ quát đang chạy TRƯỚC khi tách khung, nên một "
             f"blob ghi đè blob kia và vi phạm thành tàng hình")

        # (2) ẢNH CHỤP ghim BLOB: đổi hình dạng mà giữ nguyên SỐ vẫn phải ĐỎ.
        cay2 = tmp / "anhchup"
        (cay2 / "ops").mkdir(parents=True)
        for lenh in (["init", "-q"], ["config", "user.email", "t@t"], ["config", "user.name", "t"]):
            subprocess.run(["git", "-C", str(cay2)] + lenh, capture_output=True, timeout=60)
        (cay2 / "ops" / "anh.py").write_text(
            "import shutil, subprocess\n" + 'b = shutil.which("bash")\n' * 7, encoding="utf-8")
        _g(cay2, "add", "-A")
        oid = _g(cay2, "rev-parse", ":ops/anh.py").stdout.strip()
        bq2 = _bash_nen_voi_chua_chuyen(
            tmp, {}, ten="bash_nen_anh_chup.py",
            anh_chup={"ops/anh.py": (7, oid, "ảnh chụp đông cứng")})
        # CHỐT TRÊN CƠ CHẾ (`lech_oid_dong_cung`), KHÔNG trên `rc`. Bản đầu chốt `rc == 0` và
        # thế là trói lại phán quyết — thứ phụ thuộc MỌI luật khác của cổng, trong đó có thuộc
        # tính `t40` trói. Đây là lần thứ BA liên tiếp (r11 `t45`, r12 `t47`, r13 `t48`) cùng
        # một hình dạng: chốt trên KẾT QUẢ thay vì CƠ CHẾ. `t39`/N22 chỉ phủ `rc == 2` và
        # `trang_thai == "DO"`, nên `rc == 0` lọt qua nó — NỢ CÓ TÊN, đã trình chủ kho.
        _, bao = _quet(cay2, bq2)
        bang(not (bao.get("lech_oid_dong_cung") or {}),
             f"(2) ảnh chụp NGUYÊN BẢN mà cổng đã báo lệch OID: "
             f"{bao.get('lech_oid_dong_cung')} — một cổng lúc nào cũng đỏ thì không ai bật nó")
        (cay2 / "ops" / "anh.py").write_text(
            "import shutil, subprocess\n" + 'subprocess.run(["bash"])\n' * 7, encoding="utf-8")
        _g(cay2, "add", "-A")
        _, bao = _quet(cay2, bq2)
        bang(bool(bao.get("lech_oid_dong_cung") or {}),
             f"(2) đổi HẾT bảy lời gọi sang hình dạng khác mà GIỮ số 7: "
             f"lech_oid={bao.get('lech_oid_dong_cung')} — mục khai "
             f"'không được sửa một byte' mà chỉ đo SỐ là lời khai rộng hơn phép đo")


@ca
def t47_INDEX_phai_duoc_doc_TRUNG_THUC_va_nguon_py_nhan_du_moi_cach_viet():
    """THUỘC TÍNH: bốn mặt của "đọc INDEX cho đúng" — ref thay thế, stage, mã hoá, hậu tố.

    SINH TỪ CROSS-REVIEW CODEX vòng 6 trên `1d63f80` — BỐN P2, tái hiện cả bốn:
      (1) `git replace <xấu> <sạch>` là ref CỦA MÁY, `cat-file` trả bytes thay thế trong suốt.
          Đo: sau `git replace`, `ngoai_danh_sach` RỖNG; đặt `GIT_NO_REPLACE_OBJECTS=1` ra
          `['vi_pham.py']`. MẶT THỨ TÁM của lớp *phán quyết phụ thuộc trạng thái LOCAL của máy*
          — và là đúng món NỢ spec r11 đã KHAI TRƯỚC: *"danh sách biến git gỡ KHÔNG BAO GIỜ ĐỦ"*.
      (2) `ls-files -s` phát stage 1/2/3 cho đường chưa hoà giải; bản r11 vứt trường stage, nên
          ba bản ghi cùng đường rơi vào cùng một khoá và blob SHA lớn nhất thắng. Đo: xung đột
          có stage 1/2 mang lời gọi trần, stage 3 sạch ⇒ cổng CHO QUA.
      (3) PEP 263: `# coding: latin-1` và BOM UTF-8 đều là Python HỢP LỆ. Bản r11 giải mã cứng
          `utf-8` ⇒ cả hai ra `rc=3 KHONG_DO_DUOC`, tức một tệp hợp lệ CHẶN VĨNH VIỄN cả kho.
      (4) pathspec `*.py` so theo MỘT cách viết ⇒ `VI_PHAM.PY` và `w.pyw` vô hình. Thực thể
          THỨ BA của lớp ấy (sau hoa/thường ở r7 và byte ở r11), nên nó ra một HÀM riêng.

    MỌI chốt đọc `co_loi_goi_tran`, KHÔNG đọc `ngoai_danh_sach` — và đó cũng là một phép đo:
    `ngoai_danh_sach` là thứ có SAU bộ lọc miễn trừ, nên `bn_cong_cho_qua_moi_noi` (đích `t25`)
    làm nó rỗng và giết luôn ca này ⇒ **bán kính 2/49**. Thuộc tính ca này trói là *"máy quét
    ĐỌC ĐÚNG bytes nào"*, còn *"đọc ra rồi thì ĐỎ"* là của `t25`. `t35` đã chữa đúng cách này
    ở r4; đây là lần thứ hai cùng một bài học trong packet.

    MỌI tệp của ca này nằm TRONG `ops/`, và đó là một phép đo chứ không phải khẩu vị: bản đầu
    đặt chúng ở GỐC cây, và `t35_thu_pham_vi_ve_ops` (đột biến thu phạm vi cổng về `ops/**`,
    đích `t35`) xoá sạch chúng ⇒ **bán kính 2/49**. Ca này không trói thuộc tính PHẠM VI, nên
    việc nó chết dưới đột biến ấy là tình cờ của GIÀN GIÁO. `t36` đã gặp và chữa đúng cách này.

    Mỗi chốt kèm CHIỀU NGƯỢC ngay tại chỗ: (3) tệp BOM MANG vi phạm vẫn phải bị bắt; (4) `.txt`
    mang lời gọi trần vẫn KHÔNG được quét.
    """
    def _kho(tmp, ten):
        d = tmp / ten
        (d / "ops").mkdir(parents=True)
        for lenh in (["init", "-q"], ["config", "user.email", "t@t"], ["config", "user.name", "t"]):
            subprocess.run(["git", "-C", str(d)] + lenh, capture_output=True, timeout=60)
        return d

    def _g(d, *a):
        return subprocess.run(["git", "-C", str(d)] + list(a), capture_output=True,
                              text=True, timeout=60)

    BAN = 'import shutil\nb = shutil.which("bash")\n'
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        bq = _bash_nen_voi_chua_chuyen(tmp, {})

        # (1) REF THAY THẾ của máy không được đổi bytes cổng đọc.
        d = _kho(tmp, "ref")
        (d / "ops" / "vi_pham.py").write_text(BAN, encoding="utf-8")
        _g(d, "add", "-A")
        xau = _g(d, "rev-parse", ":ops/vi_pham.py").stdout.strip()
        (d / "ops" / "sach.py").write_text("X = 1\n", encoding="utf-8")
        _g(d, "add", "-A")
        rep = _g(d, "replace", xau, _g(d, "rev-parse", ":ops/sach.py").stdout.strip())
        if rep.returncode != 0:
            raise BoQuaMoiTruong(f"git replace không chạy được: {rep.stderr[:200]}")
        _, bao = _quet(d, bq)
        bang("ops/vi_pham.py" in (bao.get("co_loi_goi_tran") or {}),
             f"(1) `git replace` của MÁY giấu được vi phạm: co_loi_goi_tran="
             f"{sorted(bao.get('co_loi_goi_tran') or {})} — cổng đang đọc bytes thay thế chứ "
             f"không đọc blob mà INDEX ghim")

        # (2) INDEX chưa hoà giải KHÔNG có blob nào để duyệt ⇒ fail-close, nêu tên.
        d = _kho(tmp, "stage")
        (d / "ops" / "x.py").write_text(BAN, encoding="utf-8")
        _g(d, "add", "-A"); _g(d, "commit", "-q", "-m", "a")
        _g(d, "checkout", "-q", "-b", "nh")
        (d / "ops" / "x.py").write_text(BAN + "# nh\n", encoding="utf-8")
        _g(d, "add", "-A"); _g(d, "commit", "-q", "-m", "b")
        _g(d, "checkout", "-q", "-")
        (d / "ops" / "x.py").write_text("X = 1\n# c\n", encoding="utf-8")
        _g(d, "add", "-A"); _g(d, "commit", "-q", "-m", "c")
        _g(d, "merge", "nh")
        stage = {l.split()[2] for l in _g(d, "ls-files", "-s").stdout.splitlines() if len(l.split()) > 2}
        if stage == {"0"}:
            raise BoQuaMoiTruong(f"không dựng được INDEX chưa hoà giải trên máy này: stage={stage}")
        rc, bao = _quet(d, bq)
        bang(rc == 3 and "chưa hoà giải" in str(bao.get("nguon_tep", "")) + str(bao.get("ly_do", "")),
             f"(2) INDEX chưa hoà giải mà cổng vẫn ra phán quyết: rc={rc} "
             f"{bao.get('trang_thai')} nguon_tep={str(bao.get('nguon_tep'))[:120]!r} — chọn bừa "
             f"một stage là tự bịa ra một cây chưa từng tồn tại")

        # (3) MÃ HOÁ theo khai báo của chính tệp, và chiều ngược: BOM mang vi phạm VẪN bị bắt.
        d = _kho(tmp, "ma")
        (d / "ops" / "latin.py").write_bytes("# coding: latin-1\ns = 'caf\xe9'\n".encode("latin-1"))
        (d / "ops" / "bom.py").write_bytes(b"\xef\xbb\xbfX = 1\n")
        _g(d, "add", "-A")
        rc, bao = _quet(d, bq)
        bang(not (bao.get("co_loi_goi_tran") or {}),
             f"(3) Python HỢP LỆ (PEP 263 latin-1 / BOM) làm cổng CHẶN cả kho: rc={rc} "
             f"{bao.get('trang_thai')} — {str(bao.get('ly_do'))[:180]}")
        (d / "ops" / "bom_ban.py").write_bytes(b"\xef\xbb\xbf" + BAN.encode("utf-8"))
        _g(d, "add", "-A")
        _, bao = _quet(d, bq)
        bang("ops/bom_ban.py" in (bao.get("co_loi_goi_tran") or {}),
             f"(3) chiều ngược: tệp có BOM MANG lời gọi trần lại lọt: "
             f"{sorted(bao.get('co_loi_goi_tran') or {})}")

        # (3c) COOKIE LẠ ⇒ `rc=3` kèm JSON, KHÔNG traceback (N42, r15). Chốt này ở ĐÂY chứ
        # không ở `t49`: fixture chỉ nổ KHI `detect_encoding` được dùng, mà cơ chế ấy là của
        # ca này. Đặt ở `t49` thì `bn_giai_ma_cung_utf8` (đích là ca này) giết luôn `t49` —
        # đo được: bán kính 2/52.
        d = _kho(tmp, "cookie")
        (d / "ops" / "xau.py").write_bytes(b"# coding: khong-ton-tai\nX = 1\n")
        _g(d, "add", "-A")
        pc = subprocess.run([sys.executable, str(bq), "quet", "--root", str(d), "--json"],
                            capture_output=True, timeout=180)
        bang(pc.returncode == 3 and pc.stdout[:1] == b"{" and b"Traceback" not in pc.stderr,
             f"(3c) cookie mã hoá lạ làm CLI vỡ: rc={pc.returncode} "
             f"stdout_dau={pc.stdout[:40]!r} traceback={b'Traceback' in pc.stderr} — tài liệu "
             f"khai BA trạng thái thì trạng thái thứ ba phải ĐỌC ĐƯỢC, không phải một vết đổ")

        # (4) HẬU TỐ nhận đủ mọi cách viết, và chiều ngược: `.txt` vẫn KHÔNG được quét.
        d = _kho(tmp, "duoi")
        (d / "ops" / "VI_PHAM.PY").write_text(BAN, encoding="utf-8")
        (d / "ops" / "w.pyw").write_text(BAN, encoding="utf-8")
        (d / "ops" / "khong_phai.txt").write_text(BAN, encoding="utf-8")
        _g(d, "add", "-A")
        _, bao = _quet(d, bq)
        thay = sorted(bao.get("co_loi_goi_tran") or {})
        bang(thay == ["ops/VI_PHAM.PY", "ops/w.pyw"],
             f"(4) hậu tố so theo MỘT cách viết: thấy {thay}, mong ['ops/VI_PHAM.PY', 'ops/w.pyw'] — "
             f"thiếu là lọt, thừa `.txt` là quét cả thứ không phải nguồn Python")


@ca
def t46_noi_dung_lay_tu_INDEX_chu_khong_tu_cay_lam_viec():
    """THUỘC TÍNH: cả DANH SÁCH lẫn NỘI DUNG đều từ INDEX, và không biến git kế thừa nào đổi
    được INDEX nào trả lời.

    SINH TỪ CROSS-REVIEW CODEX vòng 5 trên `6131cbd` — HAI finding P2, và cả hai là **mặt thứ
    sáu và bảy** của lớp *phán quyết phụ thuộc trạng thái LOCAL của máy*. r9 giết được "tệp
    NÀO" bằng cách lấy danh sách từ INDEX; nhưng lớp còn phủ "BYTE nào" và "INDEX nào":
      symlink       mục `*.py` trong INDEX là symlink ⇒ `read_text()` đi theo RA NGOÀI kho.
                    Đo được: sửa tệp đích ngoài kho làm phán quyết đổi `['ops/lien_ket.py']`
                    → `[]` trong khi INDEX **không đổi một byte**, và `nguon_tep` vẫn khai `git`.
      GIT_INDEX_FILE  `git -C <goc>` đúng thư mục mà INDEX lại là tệp khác. Đo được: cùng một
                    kho, index THẬT trả `['bad.py']`, đặt `GIT_INDEX_FILE` trả `[]` — cả hai
                    lần đều khai `nguon_tep=git`.
    Chủ kho quyết ở r11: **nội dung cũng lấy từ INDEX** (`cat-file --batch` trên blob đã stage)
    và **gỡ mọi biến git chọn kho/chọn index/tiêm cấu hình** khỏi tiến trình con.

    ĐÁNH ĐỔI CÓ CHỦ ĐỊNH, không phải tính chất tự nhiên: tệp đã `git add` rồi sửa tiếp trên đĩa
    được quét ở DẠNG ĐÃ STAGE — chốt (3) trói đúng điều ấy, để ai đổi lại thiết kế phải đổi ca.
    """
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        bq = _bash_nen_voi_chua_chuyen(tmp, {})
        cay = tmp / "cay"
        (cay / "ops").mkdir(parents=True)
        for lenh in (["init", "-q"], ["config", "user.email", "t@t"], ["config", "user.name", "t"]):
            subprocess.run(["git", "-C", str(cay)] + lenh, capture_output=True, timeout=60)
        (cay / "ops" / "sach.py").write_text("X = 1\n", encoding="utf-8")
        subprocess.run(["git", "-C", str(cay), "add", "-A"], capture_output=True, timeout=60)

        # (3) NỘI DUNG là blob ĐÃ STAGE: sửa tiếp trên đĩa KHÔNG đổi phán quyết.
        (cay / "ops" / "sach.py").write_text(
            'import shutil\nb = shutil.which("bash")\n', encoding="utf-8")
        rc, bao = _quet(cay, bq)
        bang(not (bao.get("co_loi_goi_tran") or {}),
             f"(3) sửa tệp trên ĐĨA sau khi `git add` lại đổi được phán quyết: "
             f"{sorted(bao.get('co_loi_goi_tran') or {})} — nội dung đang đọc từ cây làm việc "
             f"chứ không từ INDEX (nguon_noi_dung={bao.get('nguon_noi_dung')!r})")
        subprocess.run(["git", "-C", str(cay), "checkout", "--", "ops/sach.py"],
                       capture_output=True, timeout=60)

        # (2) GIT_INDEX_FILE kế thừa KHÔNG đổi được danh sách.
        (cay / "ban.py").write_text('import shutil\nb = shutil.which("bash")\n', encoding="utf-8")
        subprocess.run(["git", "-C", str(cay), "add", "-A"], capture_output=True, timeout=60)
        _, nen = _quet(cay, bq)
        alt = tmp / "index_khac"
        subprocess.run(["git", "-C", str(cay), "add", "ops/sach.py"], capture_output=True,
                       timeout=60, env={**os.environ, "GIT_INDEX_FILE": str(alt)})
        _, voi_alt = _quet(cay, bq, env={**os.environ, "GIT_INDEX_FILE": str(alt)})
        bang(sorted(voi_alt.get("co_loi_goi_tran") or {}) == sorted(nen.get("co_loi_goi_tran") or {}),
             f"(2) `GIT_INDEX_FILE` kế thừa đổi được danh sách: nền "
             f"{sorted(nen.get('co_loi_goi_tran') or {})} → {sorted(voi_alt.get('co_loi_goi_tran') or {})}"
             f" — `git -C` KHÔNG ghim được kho, phải gỡ biến khỏi tiến trình con")

        # (1) Mục `*.py` là SYMLINK ⇒ KHÔNG ĐO ĐƯỢC, nêu tên. `None ≠ False`.
        ngoai = tmp / "ngoai_kho.py"
        ngoai.write_text('import shutil\nb = shutil.which("bash")\n', encoding="utf-8")
        try:
            (cay / "ops" / "lien_ket.py").symlink_to(ngoai)
        except OSError as e:
            raise BoQuaMoiTruong(f"không tạo được symlink trên máy này: {e}") from e
        subprocess.run(["git", "-C", str(cay), "add", "-A"], capture_output=True, timeout=60)
        rc, bao = _quet(cay, bq)
        bang(any("lien_ket.py" in x for x in (bao.get("lien_ket_tuong_trung") or [])),
             f"(1) mục `*.py` là SYMLINK mà cổng vẫn ra phán quyết: {bao.get('trang_thai')} "
             f"lien_ket_tuong_trung={bao.get('lien_ket_tuong_trung')} — nội dung thật nằm NGOÀI "
             f"thứ INDEX ghim, nên nó KHÔNG ĐO ĐƯỢC chứ không phải sạch")

        # (4) N95 (r26, codex vòng 20) — cây KHÔNG phải kho (`rglob`) cũng fail-close với SYMLINK.
        #     Bản r25 đọc thẳng qua liên kết: đổi tệp ĐÍCH ngoài cây đổi phán quyết của một tệp
        #     trong cây không đổi một byte.
        khong_kho = tmp / "khong_kho"
        (khong_kho / "ops").mkdir(parents=True)
        (khong_kho / "ops" / "lien_ket.py").symlink_to(ngoai)
        rc4, bao4 = _quet(khong_kho, bq)
        bang(bao4.get("nguon_tep") == "rglob"
             and any("lien_ket.py" in x for x in (bao4.get("lien_ket_tuong_trung") or [])),
             f"(4) cây không-git có SYMLINK mà cổng vẫn đọc qua nó: nguon_tep="
             f"{bao4.get('nguon_tep')!r}, lien_ket_tuong_trung={bao4.get('lien_ket_tuong_trung')}")

        # (5) N100 (r27, codex vòng 21) — symlink TREO tên `*.py`, và THƯ MỤC symlink (mà `rglob`
        #     không đi vào — đo được), cũng phải fail-close ở cây không-git.
        for ten5, dung5 in (("treo", lambda d: (d / "treo.py").symlink_to(d / "khong_co.py")),
                           ("thu_muc", lambda d: (d / "tm").symlink_to(ngoai.parent,
                                                                      target_is_directory=True))):
            k5 = tmp / f"khong_kho_{ten5}"
            (k5 / "ops").mkdir(parents=True)       # cổng đòi `ops/` ở gốc, nếu không nó từ chối cây
            dung5(k5 / "ops")
            _, bao5 = _quet(k5, bq)
            bang(bool(bao5.get("lien_ket_tuong_trung")),
                 f"(5) cây không-git có symlink {ten5} mà cổng không fail-close: "
                 f"trang_thai={bao5.get('trang_thai')!r}, "
                 f"lien_ket_tuong_trung={bao5.get('lien_ket_tuong_trung')}")

        # (6) N106 (r30, codex vòng 24) — symlink TREO tên KHÔNG phải nguồn Python: phán quyết không
        #     được phụ thuộc ĐÍCH ngoài gốc. Đo HAI lần trên cùng liên kết, trước và sau khi đích xuất
        #     hiện: cả hai lần đều phải fail-close (bản N100 bỏ nó ở lần đầu, bắt ở lần sau).
        k6 = tmp / "khong_kho_vendor"
        (k6 / "ops").mkdir(parents=True)
        dich6 = tmp / "dich_ngoai_vendor"
        (k6 / "ops" / "vendor").symlink_to(dich6, target_is_directory=True)
        ket6 = {}
        for lan in ("truoc", "sau"):
            if lan == "sau":
                dich6.mkdir()
            _, bao6 = _quet(k6, bq)
            ket6[lan] = bao6.get("lien_ket_tuong_trung")
        bang(all(bool(v) for v in ket6.values()),
             f"(6) symlink `vendor` treo phải fail-close BẤT KỂ đích ngoài gốc có tồn tại hay không: {ket6}")

        # (7) N121 (r35, codex vòng 29) — thư mục KHÔNG đọc được ở cây không-git phải fail-close, không bị
        #     bỏ qua im lặng như `rglob`. Root bỏ qua `chmod 000`, nên chốt TIÊM lỗi đọc thư mục vào chính
        #     bản cổng đang đo (`bq`) — không phụ thuộc người chạy; và khi KHÔNG phải root thì đo thêm bằng
        #     `chmod 000` thật qua tiến trình con.
        k7 = tmp / "khong_kho_an"
        (k7 / "ops").mkdir(parents=True)
        (k7 / "an").mkdir()
        (k7 / "an" / "bad.py").write_text('import shutil\nshutil.which("bash")\n', encoding="utf-8")
        m7 = runpy.run_path(str(bq))
        g7 = m7["_liet_ke_py"].__globals__
        os_that = g7["os"]

        class _OsLoiDoc:
            def __getattr__(self, ten):
                return getattr(os_that, ten)

            # N125 (r37): bộ duyệt nay là `os.scandir` lười thay `os.walk`, nên lỗi được tiêm vào đúng chỗ ấy.
            def scandir(self, duong):
                if Path(duong).name == "an":
                    raise PermissionError(13, "Permission denied", str(duong))
                return os_that.scandir(duong)
        g7["os"] = _OsLoiDoc()
        try:
            ds7, nguon7 = m7["_liet_ke_py"](k7)
            rc7, bao7 = m7["quet"](k7)
        finally:
            g7["os"] = os_that
        bang(nguon7.startswith("rglob-hong") and not ds7,
             f"(7) N121: thư mục không đọc được ở cây không-git phải cho `rglob-hong`, đo được "
             f"{nguon7!r} với {len(ds7)} tệp")
        # Đọc TRƯỜNG CƠ CHẾ, không đọc phán quyết (`t39`): nhánh fail-close KHÔNG quét gì nên báo cáo không có
        # `co_loi_goi_tran`; một bản quét tiếp danh sách THIẾU sẽ trả `co_loi_goi_tran = []`.
        bang(nguon7.startswith("rglob-hong") and bao7.get("co_loi_goi_tran") is None,
             f"(7) N121: `quet` không được QUÉT TIẾP một danh sách THIẾU: co_loi_goi_tran="
             f"{bao7.get('co_loi_goi_tran')!r}, nguon_tep={str(bao7.get('nguon_tep'))[:80]!r}")
        # (8) N123 (r36, codex vòng 30) — cây KHÔNG-git vẫn phải kiểm BYTE đông cứng: bản r35 bỏ hẳn phép kiểm
        #     OID ở nhánh này. Dựng một ảnh chụp đông cứng ghim đúng OID, quét cây giải nén (không `.git`):
        #     byte nguyên ⇒ không lệch; đổi byte (vẫn đúng một lời gọi) ⇒ PHẢI lệch.
        import hashlib as _hl
        k8 = tmp / "khong_kho_dong_cung"
        (k8 / "ops").mkdir(parents=True)
        than8 = b'import shutil\nshutil.which("bash")\n'
        (k8 / "ops" / "dong.py").write_bytes(than8)
        oid8 = _hl.sha1(b"blob %d\0" % len(than8) + than8).hexdigest()
        bq8 = _bash_nen_voi_chua_chuyen(tmp, {}, ten="bash_nen_dong_cung_t46.py",
                                        anh_chup={"ops/dong.py": (1, oid8, "ảnh chụp đông cứng giả của t46 (8)")})
        _, bao8a = _quet(k8, bq8)
        (k8 / "ops" / "dong.py").write_bytes(than8 + b"# doi byte\n")
        _, bao8b = _quet(k8, bq8)
        bang(not bao8a.get("lech_oid_dong_cung") and bool(bao8b.get("lech_oid_dong_cung")),
             f"(8) N123: cây không-git phải so OID đông cứng từ byte thật: byte nguyên ⇒ "
             f"{bao8a.get('lech_oid_dong_cung')!r}, byte đổi ⇒ {bao8b.get('lech_oid_dong_cung')!r}")

        # (9) N124 (r36, codex vòng 30) — TRẦN ĐỌC nguồn, đo TRƯỚC khi đọc, ở CẢ HAI nhánh và HAI phía biên:
        #     đúng bằng trần ⇒ đọc; vượt một byte ⇒ `_VuotTranDoc`. Trần được hạ tạm trong CHÍNH bản cổng đang đo.
        m9 = runpy.run_path(str(bq))
        g9 = m9["_doc_noi_dung"].__globals__
        vuot9 = g9["_VuotTranDoc"]
        cu9 = (g9["_TRAN_TEP_NGUON"], g9["_TRAN_TONG_NGUON"])
        muc_kg = [("ops/dong.py", None, None)]
        # Nhánh git đo trên một kho git NHỎ dựng tại chỗ, không trên `GOC`: bộ đột biến chạy ca này trên bản
        # sao cây KHÔNG đầy đủ (không `.git`) — đo được ở lượt đầy đủ r36, bản đầu dựa vào INDEX của `GOC` nên
        # `muc_git` rỗng và ca chết `IndexError` (tín dụng giả dưới hai đột biến vô can).
        k9 = tmp / "kho_git_tran"
        (k9 / "ops").mkdir(parents=True)
        (k9 / "ops" / "dong.py").write_bytes(than8)
        for lenh9 in (["init", "-q"], ["add", "ops/dong.py"]):
            subprocess.run(["git", "-C", str(k9), *lenh9], capture_output=True, check=True, timeout=60)
        muc_git, nguon_git9 = m9["_liet_ke_py"](k9)
        dung(nguon_git9 == "git" and len(muc_git) == 1,
             f"(9) GIÀN GIÁO: kho git nhỏ phải cho đúng một mục từ INDEX, đo được {nguon_git9!r} {muc_git!r}")
        ket9 = {}
        try:
            for nhan, goc9, muc9, nguon9 in (("khong-git", k8, muc_kg, "rglob"), ("git", k9, muc_git, "git")):
                co9 = len(than8) if nguon9 == "git" else (goc9 / muc9[0][0]).stat().st_size
                for ten_tran, gia_tri in (("tep", co9), ("tep", co9 - 1), ("tong", co9), ("tong", co9 - 1)):
                    g9["_TRAN_TEP_NGUON"], g9["_TRAN_TONG_NGUON"] = cu9
                    g9["_TRAN_TEP_NGUON" if ten_tran == "tep" else "_TRAN_TONG_NGUON"] = gia_tri
                    try:
                        g9["_doc_noi_dung"](goc9, muc9, nguon9)
                        ket9[(nhan, ten_tran, gia_tri - co9)] = "doc"
                    except vuot9:
                        ket9[(nhan, ten_tran, gia_tri - co9)] = "nem"
        finally:
            g9["_TRAN_TEP_NGUON"], g9["_TRAN_TONG_NGUON"] = cu9
        mong9 = {(n, t, d): ("doc" if d == 0 else "nem") for n in ("khong-git", "git")
                 for t in ("tep", "tong") for d in (0, -1)}
        bang(ket9 == mong9, f"(9) N124: trần đọc ở hai nhánh, hai phía biên: đo {ket9}, mong {mong9}")

        # (10) N125 (r37, codex vòng 31) — trần SỐ MỤC, đo TRONG LÚC liệt kê, ở cả hai nhánh và hai phía biên.
        #      Mỗi cây có BA mục `.py` cộng một mục KHÔNG phải nguồn: mục ấy KHÔNG được tính vào trần nguồn (nhánh
        #      git không giữ nó lại). Trần = 3 ⇒ liệt kê đủ ba; trần = 2 ⇒ fail-close có tên. Nhánh không-git còn
        #      đo trần số mục DUYỆT: đúng bằng số mục của cây ⇒ liệt kê; bớt một ⇒ fail-close.
        k10 = tmp / "kho_git_so_muc"
        k10b = tmp / "khong_kho_so_muc"
        for goc10 in (k10, k10b):
            (goc10 / "ops").mkdir(parents=True)
            for i10 in range(3):
                (goc10 / "ops" / f"m{i10}.py").write_bytes(b"")
            (goc10 / "ops" / "ghi_chu.txt").write_bytes(b"")
        for lenh10 in (["init", "-q"], ["add", "ops"]):
            subprocess.run(["git", "-C", str(k10), *lenh10], capture_output=True, check=True, timeout=60)
        so_muc10 = sum(1 for _ in k10b.rglob("*"))
        cu10 = (g9["_TRAN_SO_TEP_NGUON"], g9["_TRAN_MUC_DUYET"])
        ket10 = {}
        try:
            for nhan10, goc10, ten_tran10, dung_bang in (("git", k10, "_TRAN_SO_TEP_NGUON", 3),
                                                         ("khong-git", k10b, "_TRAN_SO_TEP_NGUON", 3),
                                                         ("khong-git", k10b, "_TRAN_MUC_DUYET", so_muc10)):
                for lech10 in (0, -1):
                    g9["_TRAN_SO_TEP_NGUON"], g9["_TRAN_MUC_DUYET"] = cu10
                    g9[ten_tran10] = dung_bang + lech10
                    ds10, nguon10 = g9["_liet_ke_py"](goc10)
                    ket10[(nhan10, ten_tran10, lech10)] = (
                        "du" if len(ds10) == 3 and nguon10 in ("git", "rglob")
                        else "vuot-tran" if ("vượt trần" in nguon10 or "_VuotTranDoc" in nguon10) and not ds10
                        else f"khac: {nguon10[:60]} {len(ds10)}")
        finally:
            g9["_TRAN_SO_TEP_NGUON"], g9["_TRAN_MUC_DUYET"] = cu10
        mong10 = {k: ("du" if k[2] == 0 else "vuot-tran") for k in ket10}
        bang(len(ket10) == 6 and ket10 == mong10,
             f"(10) N125: trần số mục ở hai nhánh, hai phía biên: đo {ket10}")

        if hasattr(os, "geteuid") and os.geteuid() != 0:
            (k7 / "an").chmod(0)
            try:
                _, bao7b = _quet(k7, bq)
            finally:
                (k7 / "an").chmod(0o755)
            bang(str(bao7b.get("nguon_tep")).startswith("rglob-hong") and bao7b.get("co_loi_goi_tran") is None,
                 f"(7) N121: `chmod 000` THẬT phải fail-close: nguon_tep={str(bao7b.get('nguon_tep'))[:80]!r}")


@ca
def t45_bo_ca_phai_CHAY_cong_tren_cay_THAT_chu_khong_chi_cay_gia():
    """THUỘC TÍNH: điểm vào mà CI gọi phải CHẠY cổng trên cây thật — sạch thì qua, bẩn thì hỏng.

    SINH TỪ CROSS-REVIEW CODEX vòng 5 trên `6131cbd`, và đây là finding **P1** đầu tiên của
    packet. `.github/workflows/ci.yml` gọi `python ops/cong_cu_test.py` ở BA chỗ và KHÔNG chỗ
    nào gọi `ops/bash_nen.py quet`; còn `main()` chỉ chạy ca trên cây GIẢ cộng bán kính đột
    biến. Đo lại trên một BẢN SAO kho, có bằng chứng dương:
        `bash_nen.py quet --root .` ⇒ rc=2 DO, ngoai_danh_sach=['vi_pham_moi.py']
        `cong_cu_test.py`           ⇒ rc=1 (nền), tên tệp vi phạm xuất hiện **0 lần**
    Tức cái cổng cả packet sinh ra để dựng chưa từng được nối vào chỗ nó gác. Một cổng không
    ai gọi thì không phải cổng.

    HAI CHIỀU, và chiều SẠCH là chiều dễ quên: nếu thiếu nó thì một bản vá "lúc nào cũng hỏng"
    vẫn xanh ở ca này. Đi qua CỬA TIẾN TRÌNH CON `--tu-kiem-cong-that` để đột biến trên đĩa
    cắn được — lần thứ SÁU của cái bẫy "đột biến tệp không cắn nổi mã đã nạp trong tiến trình".
    """
    def _do(ban, bq):
        p = subprocess.run([sys.executable, str(TEP_TEST), "--tu-kiem-cong-that", str(ban), str(bq)],
                           cwd=GOC, capture_output=True, text=True, timeout=180)
        dong = [l for l in p.stdout.splitlines() if l.startswith("KQ ")]
        dung(dong, f"cửa tự kiểm hỏng: rc={p.returncode}\n{p.stdout[-600:]}\n{p.stderr[-600:]}")
        return p.returncode, json.loads(dong[-1][3:])

    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        bq = _bash_nen_voi_chua_chuyen(tmp, {})
        cay = tmp / "cay"
        (cay / "ops").mkdir(parents=True)
        for lenh in (["init", "-q"], ["config", "user.email", "t@t"], ["config", "user.name", "t"]):
            subprocess.run(["git", "-C", str(cay)] + lenh, capture_output=True, timeout=60)
        (cay / "ops" / "sach.py").write_text("X = 1\n", encoding="utf-8")
        subprocess.run(["git", "-C", str(cay), "add", "-A"], capture_output=True, timeout=60)
        rc_sach, (loi_sach, _) = _do(cay, bq)
        bang(rc_sach == 0 and loi_sach == 0,
             f"(1) cây SẠCH mà điểm vào vẫn báo hỏng: rc={rc_sach} lỗi={loi_sach} — "
             f"một cổng lúc nào cũng đỏ thì không ai bật nó")

        (cay / "ops" / "ban.py").write_text(
            'import shutil\nb = shutil.which("bash")\n', encoding="utf-8")
        subprocess.run(["git", "-C", str(cay), "add", "-A"], capture_output=True, timeout=60)
        rc_cong, bao_cong = _quet(cay, bq)          # phán quyết của CỔNG, gọi thẳng
        rc_ban, (loi_ban, dong_ban) = _do(cay, bq)  # điểm vào mà CI gọi
        bang((loi_ban != 0) == (rc_cong != 0) and (rc_ban != 0) == (loi_ban != 0),
             f"(2) điểm vào KHÔNG phản ánh phán quyết của cổng: cổng rc={rc_cong} "
             f"({bao_cong.get('trang_thai')}) mà điểm vào lỗi={loi_ban} mã={rc_ban} — "
             f"CI gọi đúng điểm vào này, nên một bên nói ĐỎ mà bên kia nói qua là cổng KHÔNG "
             f"được nối. (Đây KHÔNG phải ca gác tính ĐÚNG của cổng — đó là `t25`.)")
        if rc_cong != 0:
            bang(any("ban.py" in d for d in dong_ban),
                 f"(3) điểm vào có báo hỏng nhưng KHÔNG nêu tên tệp vi phạm: {dong_ban} — "
                 f"người đọc log CI phải biết sửa gì, không phải chỉ biết là có chuyện")


@ca
def t44_khong_lay_duoc_INDEX_thi_KHONG_DO_DUOC_chu_khong_lui_ve_rglob():
    """THUỘC TÍNH: cây LÀ kho git mà không lấy được INDEX ⇒ KHÔNG ĐO ĐƯỢC — không lùi, không
    phán quyết. Cây KHÔNG phải kho git thì vẫn quét thẳng được.

    SINH TỪ CROSS-REVIEW CODEX vòng 4 trên `e290f99` (P2), executor ĐO LẠI và tái hiện chính
    xác: cây có `.git` GIẢ ⇒ `_liet_ke_py` trả `rac_bi_ignore.py` kèm `rglob-git-hong`, và
    `quet` ra **rc=2 DO** — báo động giả sinh từ một tệp CHƯA THEO DÕI của máy.

    VÌ SAO ĐÂY KHÔNG PHẢI "MỘT LỖI NỮA" MÀ LÀ CỬA SAU CỦA MỘT LỚP ĐÃ TƯỞNG GIẾT XONG. Lớp
    *phán quyết phụ thuộc trạng thái LOCAL của máy* đã lộ BỐN mặt qua ba bản vá nối tiếp, và
    ở r9 chủ kho giết nó bằng kiến trúc: danh sách = INDEX, không còn luật ignore nào để
    nghe. Nhưng r9 vẫn giữ một đường LÙI khi git hỏng — và trên đường ấy danh sách lại là
    `rglob`, tức lại nghe trạng thái máy. r9 ĐẶT TÊN cho đường lùi (`rglob-git-hong`) với lý
    lẽ "người đọc phải thấy". Một TRƯỜNG cho người đọc không phải một CỔNG: đúng thứ kho gọi
    là *lời dặn bằng miệng không phải hàng rào*, lần này nằm trong chính mã của packet.

    HAI CHIỀU:
      (1) `.git` có mà git hỏng ⇒ `rc=3`, `nguon_tep` khai `git-hong`, và một tệp CHƯA theo
          dõi mang lời gọi trần KHÔNG được biến nó thành `DO`. Chốt trên `rc=3` chứ không
          trên `rc=2`, nên ca này KHÔNG thuộc `CA_PHAN_QUYET` (N22).
      (2) cây KHÔNG có `.git` vẫn `rglob` và vẫn phán quyết được — thiếu chiều này thì một
          đột biến "lúc nào cũng KHÔNG_ĐO_ĐƯỢC" sẽ sống, và toàn bộ bộ ca dựng cây giả chết.
    """
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        bq = _bash_nen_voi_chua_chuyen(tmp, {})

        # (1) `.git` LÀ THƯ MỤC nhưng không phải kho ⇒ `git ls-files` rc=128. Cách làm git
        # hỏng này độc lập nền: không cần gỡ git khỏi PATH, không cần quyền gì.
        cay = tmp / "cay-git-hong"
        (cay / "ops").mkdir(parents=True)
        (cay / ".git").mkdir()
        (cay / "rac_chua_theo_doi.py").write_text(
            'import shutil\nb = shutil.which("bash")\n', encoding="utf-8")
        rc, bao = _quet(cay, bq)
        bang(rc == 3 and bao.get("trang_thai") == "KHONG_DO_DUOC",
             f"(1) cây có `.git` mà git hỏng lại ra rc={rc} {bao.get('trang_thai')!r} "
             f"(nguon_tep={bao.get('nguon_tep')!r}, ngoai_danh_sach="
             f"{sorted(bao.get('ngoai_danh_sach') or {})}) — cổng đã LÙI về `rglob` và để một "
             f"tệp CHƯA THEO DÕI của máy quyết phán quyết. `None ≠ False`.")
        bang(str(bao.get("nguon_tep", "")).startswith("git-hong"),
             f"(1) trạng thái phải KHAI ra là `git-hong: …` để đọc được VÌ SAO, "
             f"đang là {bao.get('nguon_tep')!r}")

        # (2) CHIỀU NGƯỢC: không `.git` thì vẫn quét thẳng được — bộ ca dựng cây giả sống nhờ
        # đường này, nên nó phải có ca giữ.
        cay2 = tmp / "cay-khong-git"
        (cay2 / "ops").mkdir(parents=True)
        (cay2 / "ops" / "sach.py").write_text("X = 1\n", encoding="utf-8")
        rc2, bao2 = _quet(cay2, bq)
        bang(rc2 == 0 and bao2.get("nguon_tep") == "rglob",
             f"(2) cây KHÔNG phải kho git mà cổng không quét được: rc={rc2} "
             f"nguon_tep={bao2.get('nguon_tep')!r} — {str(bao2.get('ly_do'))[:200]}")

        # (3) N74 (r20) — BỘ QUÉT NÉM BẤT KỲ GÌ trên một tệp ⇒ `KHONG_DO_DUOC`, không traceback.
        # Vòng 14 đo được `"%c" % <số quá lớn>` làm `quet --json` THOÁT 1: `OverflowError`
        # không nằm trong bộ `except` liệt kê. Ở đây TIÊM đúng `OverflowError` ấy vào đầu
        # `_loi_goi_tran` của một bản sao — để chốt đo CỬA `quet`, không đo bộ gấp hằng. Bản
        # đầu dùng một phép khuếch đại vượt ngân sách làm mồi, và đột biến `bn_bo_ngan_sach`
        # giết THÊM ca này (bán kính 2/53): hai chốt đo chồng lên nhau.
        neo = "def _loi_goi_tran(than: str, sau=0):\n"
        than3 = bq.read_text(encoding="utf-8")
        dung(than3.count(neo) == 1, f"mỏ neo tiêm `{neo.strip()}` phải có đúng một lần")
        bq3 = tmp / "bash_nen_tiem_nem.py"
        dau = tmp / "dau_da_toi_diem_tiem"
        bq3.write_text(than3.replace(
            neo, neo + f"    open({str(dau)!r}, 'w').close()\n"
                       "    raise OverflowError('tiem: bo quet nem')\n", 1), encoding="utf-8")
        cay3 = tmp / "cay-bo-quet-nem"
        (cay3 / "ops").mkdir(parents=True)
        (cay3 / "ops" / "sach.py").write_text("X = 1\n", encoding="utf-8")
        try:
            rc3, bao3 = _quet(cay3, bq3)
        except Exception as e:           # noqa: BLE001 — sập chính là điều đang đo
            rc3, bao3 = None, {"ly_do": f"SẬP {type(e).__name__}: {e}"}
        # CHỐT TIỀN ĐỀ TRƯỚC KẾT LUẬN (N25, cùng bài với `t49`): chốt này chỉ đo được khi
        # `quet` THẬT SỰ đi qua điểm tiêm. Đo được: `bn_quet_theo_chuoi` (đích `t27`) thay
        # hẳn lời gọi `_loi_goi_tran` bằng phép dò chuỗi ⇒ điểm tiêm không bao giờ tới, cổng
        # ra `DAT`, và bản đầu kết luận thẳng ⇒ bán kính 2/53.
        if not dau.exists():
            raise BoQuaMoiTruong(
                f"KHÔNG ĐO ĐƯỢC (3): `quet` không đi qua `_loi_goi_tran` nên điểm tiêm không tới "
                f"(rc={rc3} {bao3.get('trang_thai')!r}). Cổng đo bằng cơ chế gì là chuyện của `t27`.")
        bang(rc3 == 3 and bao3.get("trang_thai") == "KHONG_DO_DUOC"
             and "OverflowError" in str(bao3.get("ly_do")),
             f"(3) bộ quét ném mà cổng không ra KHONG_DO_DUOC có tên ngoại lệ: rc={rc3} "
             f"{bao3.get('trang_thai')!r} — {str(bao3.get('ly_do'))[:200]}")


@ca
def t42_ca_do_o_NEN_bi_loai_khoi_ban_kinh_va_van_keo_ma_thoat():
    """THUỘC TÍNH: ca đã ĐỎ Ở NỀN bị LOẠI khỏi bán kính của MỌI đột biến, báo MỘT lần, vẫn là LỖI.

    SINH TỪ NGHIỆM THU WINDOWS `570-do-14` (máy chủ kho, ghim `1253e3a`): `t38` đỏ ở nền ⇒
    45/46 đột biến in "giết THÊM ['t38_…']", `lỗi đột biến=45`. Cả 45 dòng là hệ quả của MỘT
    ca; người đọc phải lội hết mới thấy điều duy nhất có thật. Lần thứ HAI của hình dạng này
    (lần đầu `570-do-10`, `t34`, spec r6 §0) ⇒ chữa bằng cơ chế, đừng để lần thứ ba.

    Đo TRƯỚC (hàm thuần của r7, một ca đỏ ở nền trong `ket`): MỌI đột biến ra `loi=1`,
    "giết THÊM ['ca_do_o_nen'] … bán kính 2/3". Đo SAU: xem bốn chốt.
    Qua cửa tiến trình con `--tu-kiem-nen-do` — đột biến trên tệp không cắn mã đã nạp (bài học
    `t29`/`t39`); cửa RIÊNG vì `t29` chốt cửa `--tu-kiem-ban-kinh` in đúng ba kịch bản.
      (1) ca đỏ ở nền KHÔNG bị tính "giết THÊM", mẫu số trừ nó (1/2, không phải 2/3), lỗi = 0;
      (2) ĐÍCH đỏ ở nền ⇒ KHÔNG_ĐO_ĐƯỢC, nêu rõ "Ở NỀN", lỗi = 1 — không có gì để giết;
      (3) báo cáo nền nêu TÊN ca và mang lỗi ≥ 1 — mã thoát không được lặng lẽ xanh;
      (4) đối chứng âm: không ca nào đỏ ⇒ không in gì, lỗi = 0.
    """
    p = subprocess.run([sys.executable, str(TEP_TEST), "--tu-kiem-nen-do"],
                       cwd=GOC, capture_output=True, text=True, timeout=120)
    dung(p.returncode == 0 and "ND4 " in p.stdout,
         f"không chạy được cửa tự kiểm: rc={p.returncode}\n{p.stdout}\n{p.stderr}")
    doc = {l[:3]: json.loads(l[4:]) for l in p.stdout.splitlines()
           if l[:4] in ("ND1 ", "ND2 ", "ND3 ", "ND4 ")}
    dung(len(doc) == 4, f"cửa tự kiểm phải in ĐÚNG bốn kịch bản, đọc được {sorted(doc)}:\n{p.stdout}")
    l1, d1 = doc["ND1"]
    van1 = "\n".join(d1)
    bang(l1 == 0 and "ca_do_o_nen" not in van1 and "1/2" in van1,
         f"(1) ca đỏ ở nền vẫn bị tính vào bán kính (lỗi={l1}):\n{van1}")
    l2, d2 = doc["ND2"]
    van2 = "\n".join(d2)
    bang(l2 == 1 and "KHÔNG_ĐO_ĐƯỢC" in van2 and "NỀN" in van2,
         f"(2) đích đỏ ở nền phải là KHÔNG_ĐO_ĐƯỢC nêu rõ 'Ở NỀN' và tính lỗi (lỗi={l2}):\n{van2}")
    l3, d3 = doc["ND3"]
    bang(l3 >= 1 and "ca_do_o_nen" in "\n".join(d3),
         f"(3) báo cáo nền phải nêu TÊN ca và kéo lỗi khác 0 (lỗi={l3}):\n{d3}")
    l4, d4 = doc["ND4"]
    bang(l4 == 0 and d4 == [],
         f"(4) không ca nào đỏ ở nền mà vẫn in/tính lỗi (lỗi={l4}): {d4}")


@ca
def t39_chi_CA_PHAN_QUYET_duoc_chot_tren_rc_va_trang_thai():
    """THUỘC TÍNH: không ca nào ngoài `CA_PHAN_QUYET` được chốt trên phán quyết của cổng.

    Xem khối chú thích của `CA_PHAN_QUYET` ở trên: SÁU lần cùng một hình dạng, ba trong số đó
    do chính phiên vừa ghi nguyên tắc vào docstring. r7 đổi nó thành LUẬT ĐO ĐƯỢC.

    HAI CHIỀU, như mọi ratchet của packet này:
      (1) một ca NGOÀI danh sách mà có chốt phán quyết ⇒ ĐỎ, nêu tên hàm và số dòng;
      (2) một tên TRONG danh sách mà KHÔNG còn chốt phán quyết nào ⇒ cũng ĐỎ — kẻo danh sách
          thành nghĩa trang, đúng bệnh N5 sinh ra để chặn.

    NỢ CÓ TÊN: luật này bắt theo HÌNH DẠNG CÚ PHÁP. Nó KHÔNG bắt được một ca trói lại phán
    quyết bằng đường vòng — gọi qua hàm phụ, so chuỗi `ly_do`, hay đọc `ngoai_danh_sach` rồi
    suy ra. Nó THU HẸP CỬA, không đóng cửa. Ghi ra thay vì để người sau tưởng đã kín.
    """
    p = subprocess.run([sys.executable, str(TEP_TEST), "--tu-kiem-luat-phan-quyet"],
                       cwd=GOC, capture_output=True, text=True, timeout=180)
    dung(p.returncode == 0 and "KQ " in p.stdout,
         f"giàn giáo hỏng: rc={p.returncode}\n{p.stdout[-800:]}\n{p.stderr[-800:]}")
    ngoai, rong, mau, ly_do_hong, mau_ly = json.loads(
        [l for l in p.stdout.splitlines() if l.startswith("KQ ")][-1][3:])
    lech = {k: v for k, v in mau.items() if v != _MAU_MONG[k]}
    # THÔNG ĐIỆP SINH RA TỪ BẢNG, không viết tay. Bản r14 nới luật để `!=` CŨNG bị bắt,
    # nhưng thông điệp hỏng vẫn dặn người sửa rằng *"`!=` là một ca ÂM hợp lệ và KHÔNG được
    # ép vào `CA_PHAN_QUYET`"* — tức nó dạy đúng cái luật r14 vừa bỏ. Ai gặp ĐỎ mà làm theo
    # sẽ khôi phục luật cũ. Một lời dặn trái với luật nó đang gác thì nguy hơn không có lời
    # dặn nào. Chữa bằng CƠ CHẾ: hai danh sách dưới đây ĐỌC TỪ `_MAU_MONG`, nên không thể
    # lệch khỏi luật nữa — đổi luật là thông điệp tự đổi theo.
    _phai = sorted(k for k, v in _MAU_MONG.items() if v)
    _khong = sorted(k for k, v in _MAU_MONG.items() if not v)
    bang(not lech,
         f"(0) luật đọc SAI mẫu thử: {lech}. Chính sách hiện hành là MỌI phép chạm tới mã "
         f"thoát của `_quet` hay tới một TRƯỜNG TỔNG HỢP {list(_TRUONG_TONG_HOP)} đều phải "
         f"vào bản kiểm kê — mọi toán tử, mọi tên, `bang`/`dung` hay `assert` trần. "
         f"PHẢI bắt: {_phai}. KHÔNG được bắt: {_khong}. "
         f"Đây là một BẢN KIỂM KÊ, không phải lệnh cấm: ca nào thật sự trói phán quyết thì "
         f"khai vào `CA_PHAN_QUYET` kèm lý do đo được. Một luật bắt oan là luật sẽ bị tắt.")
    bang(not ngoai,
         f"(1) ca NGOÀI `CA_PHAN_QUYET` mà chốt trên phán quyết ĐỎ của cổng: {ngoai}. "
         f"Ca ấy phải đo THUỘC TÍNH của riêng nó — `t35` đọc `co_loi_goi_tran`, `t34` đọc "
         f"`chan_doan` — chứ không khẳng định lại thứ `t25` đã trói. Nếu nó THẬT SỰ là một "
         f"phán quyết mới, khai tên vào `CA_PHAN_QUYET` kèm lý do đo được.")
    bang(not rong,
         f"(2) tên trong `CA_PHAN_QUYET` mà KHÔNG còn chốt ĐỎ nào: {rong}. Hoặc ca ấy đã "
         f"thôi khẳng định ĐỎ, hoặc HÀM đã bị xoá/đổi tên, hoặc tên gõ SAI — cả ba đều để "
         f"lại một miễn trừ CHẾT. Xoá khỏi danh sách; nó phải NGẮN đi, không thành nghĩa trang.")
    lech_ly = {k: v for k, v in mau_ly.items() if v != _MAU_LY_DO_MONG[k]}
    bang(not lech_ly,
         f"(3a) luật ĐỌC LÝ DO đọc sai mẫu thử: {lech_ly} (mong {_MAU_LY_DO_MONG}). Phải coi "
         f"là HỎNG: chuỗi rỗng, chỉ khoảng trắng, `None`, số, danh sách. Phải coi là ĐƯỢC: "
         f"một chuỗi có chữ, kể cả khi kèm khoảng trắng hai đầu. Không có bảng mẫu này thì "
         f"một bản vá làm luật thôi đọc sẽ SỐNG SÓT, vì hôm nay mọi mục đều có lý do thật.")
    bang(not ly_do_hong,
         f"(3) miễn trừ KHÔNG mang lý do đọc được: {ly_do_hong}. Mỗi mục của "
         f"`CA_PHAN_QUYET` phải ánh xạ tới một CHUỖI KHÔNG RỖNG nói VÌ SAO ca ấy được phép "
         f"trói phán quyết. Trước r16 nhánh này chỉ đếm khoá, nên `\"\"`, khoảng trắng, "
         f"`None` hay một con số đều lọt — và cả yêu cầu 'mọi miễn trừ đều có lý do kiểm "
         f"toán được' chỉ là một câu viết trong docstring, chưa bao giờ là một phép đo.")



def _doc_kq_tu_kiem(cua):
    """`KQ` của một cửa tự kiểm `--tu-kiem-…` chạy qua `TEP_TEST` (để đột biến trên đĩa cắn được)."""
    p = subprocess.run([sys.executable, str(TEP_TEST), cua], cwd=GOC, capture_output=True, text=True, timeout=300)
    dong = [l for l in p.stdout.splitlines() if l.startswith("KQ ")]
    dung(p.returncode == 0 and dong, f"cửa {cua} hỏng: rc={p.returncode}\n{p.stdout[-600:]}\n{p.stderr[-600:]}")
    return json.loads(dong[-1][3:])


@ca
def t52_gom_manh_phai_DO_khi_thieu_trung_lech_va_moi_chot_co_THE_RIENG():
    """#668 M3/M4: job gom ĐỎ khi bộ mảnh sai — mỗi cách sai bị ĐÚNG chốt của nó bắt (thẻ `[G-…]`).

    Bộ mảnh dựng bằng CHÍNH `_ket_thuc_manh` (phía ghi) rồi làm hỏng từng cách, nên ca đo cả hợp đồng hai phía.
    Đòi THẺ chứ không chỉ đòi ĐỎ: gỡ một chốt thì kịch bản của nó hoặc lọt, hoặc bị chốt KHÁC bắt với thẻ khác — cả
    hai đều ĐỎ ở đây. Đối chứng hai chiều: bộ ĐÚNG phải XANH (N=3 và N=1-bị-từ-chối), để "từ chối tất cả" cũng HỎNG.
    Phía ghi: mảnh không đạt KHÔNG để lại tệp, kể cả tệp cũ cùng tên — job gom không được thấy mảnh cũ.
    """
    kq = _doc_kq_tu_kiem("--tu-kiem-gom")
    loi, dau, cuoi = kq["dung"]
    bang(loi == 0 and dau == "GOM MẢNH 3/3" and "lỗi đột biến=0" in cuoi,
         f"bộ mảnh ĐÚNG phải gom XANH: {kq['dung']}")
    mong = {"thieu": "G-tap", "thua": "G-dem", "trung": "G-tap", "chuyen": "G-ban-ghi", "xoa": "G-ban-ghi",
            "sha": "G-van-tay", "head": "G-van-tay", "so_manh": "G-so-manh", "phien_ban": "G-phien-ban",
            "kieu_bool": "G-dau", "khoa_thua": "G-dau", "dau_hong": "G-dau", "dong_la": "G-dong-la",
            "ban_ghi": "G-ban-ghi", "tep_la": "G-tep", "rong": "G-rong", "khong_co": "G-thu-muc",
            "head_gom_none": "G-head", "n_1": "G-n", "phan_chong": "G-phan-hoach",
            "kieu_phien_ban_bool": "G-dau", "kieu_phien_ban_so_thuc": "G-dau", "kieu_so_manh_so_thuc": "G-dau",
            **({"symlink_tep": "G-tep"} if _CO_SYMLINK else {}), "bien_17_None": "G-n", "bien_3_0": "G-n",
            "tien_to": "G-dau", "doc_loi": "G-dau",
            **{f"kieu_{tr}_{j}": "G-dau" for tr in ("phien_ban", "manh", "so_manh") for j in range(6)}}
    sai = {t: kq.get(t) for t, the in mong.items()
           if not (kq.get(t) and kq[t][0] >= 1 and f"[{the}]" in kq[t][1])}
    bang(not sai, f"kịch bản hỏng KHÔNG bị đúng chốt bắt (mong thẻ {mong}): {sai}")
    mong_sl = [True, sorted(_TEN_SL)] if _CO_SYMLINK else [False, sorted(_TEN_SL_FALSE)]
    bang(kq["nang_luc"] == mong_sl, f"đột biến symlink phải theo NĂNG LỰC (mong {mong_sl}): {kq['nang_luc']}")
    ghi = {t: kq.get(t) for t, the in (("ghi_loi", "M-loi"), ("ghi_con", "M-con"), ("ghi_head", "M-head"),
                                       ("ghi_do_cuoi", "M-loi"), ("ghi_do_hai", "M-loi"))
           if not (kq.get(t) and kq[t][0] >= 1 and f"[{the}]" in kq[t][1] and kq[t][2] == "khong-tep")}
    bang(not ghi, f"mảnh KHÔNG đạt phải ĐỎ đúng thẻ và KHÔNG để lại tệp: {ghi}")
    # F35 (Codex lượt 14): N=2/16 gom XANH, bảng NGUYÊN VĂN; bộ ghi tạo cha nhiều tầng, giữ nguyên tên, gỡ symlink gãy;
    # phân hoạch ĐÚNG danh tính `i % N == k` — oracle `nguon[k::N]` tự tính ở đây, không gọi `_phan_manh`.
    bien = {t: kq.get(t) for t in ("bien_2_None", "bien_16_None")
            if not (kq.get(t) and kq[t][0] == 0 and kq[t][1] == f"GOM MẢNH {t.split('_')[1]}/{t.split('_')[1]}" and kq[t][3])}
    bang(not bien and kq["ghi_duong"] == [True, True] and kq.get("ghi_gay", [False]) == [False],
         f"biên N / bộ ghi sai: {bien} {kq['ghi_duong']} {kq.get('ghi_gay')}")
    so_ten, nhom = kq["phan_hoach"]
    lech = [x for x in [f"{k}/{m}" for m in range(2, 17) for k in range(m)]
            if nhom.get(x) != list(range(int(x.split("/")[0]), so_ten, int(x.split("/")[1])))]
    bang(not lech, f"`_phan_manh` sai DANH TÍNH (nhóm k/N ≠ nguon[k::N]): {lech[:5]} / {len(lech)}")
    # F21: bộ ghi phải KẾT LUẬN mọi bản ghi `do` (đích sống ở cuối; ở cả đầu và cuối ⇒ ĐÚNG 2 lỗi) và in NGUYÊN bảng.
    bang(kq["ghi_do_cuoi"][0] == 1 and kq["ghi_do_hai"][0] == 2 and kq["ghi_do_cuoi"][3] and kq["ghi_do_hai"][3]
         and "[M-loi]: 2 lỗi" in kq["ghi_do_hai"][1], f"bộ ghi bỏ sót bản ghi sai kết quả: {kq['ghi_do_cuoi']} {kq['ghi_do_hai']}")
    cli = {"cli_dung": (0, "GOM MẢNH 3/3", 1), "cli_thieu": (1, "[G-tap]", 1), "cli_doi_so": (2, "[G-doi-so]", 0),
           "cli_tt_rong": (1, "[G-rong]", 0), "cli_tt_doi_so": (2, "[G-doi-so]", 0),
           "cli_tt_ten_cua": (1, "[G-thu-muc]", 0), "cli_tt_cua_sau": (2, "[G-doi-so]", 0),
           "cli_tt_la": (2, "đối số lạ", 0)}
    cli_sai = {t: kq.get(t) for t, (rc, dau_ra, vt) in cli.items()
               if not (kq.get(t) and kq[t][0] == rc and dau_ra in kq[t][1] and kq[t][2] == vt)}
    bang(not cli_sai, f"CLI `--gop` phải gọi gom + `_van_tay` đúng một lần + truyền mã (mong {cli}): {cli_sai}")
    # F16: bộ ĐÚNG cấu trúc, SAI kết quả (đích sống ở đầu mảnh 0, tín dụng giả ở giữa mảnh 1, bán kính 2 ở cuối mảnh 2)
    # ⇒ ĐÚNG 3 lỗi, bảng ĐỦ (N−3 dòng `ok` + 3 dòng ĐỎ), SỐ LIỆU nói đúng 3. F17: cùng thứ ấy qua CLI THẬT, cộng đường
    # DƯƠNG (rc=0, N dòng `ok`) trên kho git tạm có vân tay khớp.
    nn = kq["N"]
    so = lambda loi: f"SỐ LIỆU GOM: ca={len(CA)} · đột biến={nn} · lỗi đột biến={loi}"
    # F19/F20: hai cờ cuối = bảng NGUYÊN VĂN bằng bảng lắp lại độc lập; tổng lỗi / mã thoát khớp.
    f16 = {"kq_nhieu": [3, nn - 3, 3, so(3), True, True], "kq_mot": [1, nn - 1, 1, so(1), True, True],
           "cli_git_dung": [0, nn, 0, so(0), "GOM MẢNH 3/3", True, True],
           "cli_git_nhieu": [1, nn - 3, 3, so(3), "GOM MẢNH 3/3", True, True]}
    sai16 = {t: kq.get(t) for t, m in f16.items() if kq.get(t) != m}
    bang(not sai16, f"gom phải KẾT LUẬN đủ mọi bản ghi, cộng ĐỦ lỗi, in ĐỦ bảng — trực tiếp và qua CLI thật "
                    f"([rc/lỗi, số ok, số ĐỎ, SỐ LIỆU(, dòng đầu)], mong {f16}): {sai16}")
    # #698 M2b T4/T5: bộ ghi THẬT trên mọi ô (> 60: 60 đường + khúc tên tệp) — tập mục, hai dòng in, HOME rỗng.
    # PR #721: trên Windows khối không chạy (tên Windows cấm) ⇒ đúng [0, [], 0].
    bang(kq["ghi698"] == [0, [], 0] if os.name == "nt" else kq["ghi698"][0] > 60 and kq["ghi698"][1:] == [[], 0],
         f"bộ ghi #698 [số ô, ô lệch đầu, tổng lệch]: {kq['ghi698']}")
    # Chốt nền của khối, đo không cần Windows: `ten_nen="nt"` ⇒ KHÔNG lời gọi bộ ghi nào mang ký tự Windows cấm.
    goi, g = [], globals()
    cu, g["_ket_thuc_manh"] = g["_ket_thuc_manh"], lambda *a: (goi.append(a[2]), [["x"], 0])[1]
    try:
        with tempfile.TemporaryDirectory(prefix="t52nt_") as d:
            ra_nt = _ghi698(Path(d), 3, {}, list(DOT_BIEN)[:1], ten_nen="nt")
    finally:
        g["_ket_thuc_manh"] = cu
    cam = [ascii(p)[:40] for p in goi if any(ord(c) < 32 or c in '"*:?|<>' + chr(92) for c in p)]
    bang(ra_nt == [0, [], 0] and not cam, f"khối #698 M2b trên `nt` gọi bộ ghi với tên Windows cấm: {ra_nt} {cam[:3]}")


@ca
def t53_che_do_doc_FAIL_CLOSED_moi_cau_hinh_la_co_THE_RIENG_va_van_tay_bam_NGUON():
    """#668 M1/M2: `_doc_che_do` nhận ĐÚNG ba chế độ; mọi cấu hình lạ ⇒ lỗi mang ĐÚNG thẻ `[C-…]`.

    #698: "mọi" chỉ đúng tới MIỀN ĐO — bảng, lưới, D698 ∪ N698 × mọi vị trí (M1), 12 ô `ra` cấu trúc (M2); `head`: D698 chỉ ở ba
    neo, thành viên ngoài R698 × vị trí khác KHÔNG đo; điểm mã ngoài D698 ∪ N698 ngoài ba đại diện KHÔNG đo (spec wp698 §10).

    Chuỗi rỗng KHÔNG phải "vắng": `gate` rơi nhầm về `du` thì chỉ chậm, còn một biến mảnh hỏng rơi về `gate` thì không
    ai đo bán kính. `\\u0661` (chữ số Ả Rập) và `\\n` cuối là hai lối `\\d`/`$` từng lọt ở kho này. Phân hoạch
    `i % N == k` do `t52` gác (kịch bản `dung` + `phan_chong`): đặt thêm chốt ở đây là cho một đột biến bán kính 2.
    """
    kq = _doc_kq_tu_kiem("--tu-kiem-che-do")
    mong = {"vang": ["du", None], "gate": ["gate", None], "manh": ["manh", [7, 8, "x"]],
            "manh_16": ["manh", [15, 16, "x"]],
            "gate_rong": ["loi", "[C-ban-kinh]"], "gate_la": ["loi", "[C-ban-kinh]"],
            "k_bang_n": ["loi", "[C-pham-vi]"], "n_1": ["loi", "[C-pham-vi]"], "n_17": ["loi", "[C-pham-vi]"],
            "chu": ["loi", "[C-hinh-dang]"], "so_0_dau": ["loi", "[C-hinh-dang]"], "cach": ["loi", "[C-hinh-dang]"],
            "xuong_dong": ["loi", "[C-hinh-dang]"], "so_la": ["loi", "[C-hinh-dang]"],
            "thieu_ra": ["loi", "[C-thieu-ra]"], "ra_rong": ["loi", "[C-thieu-ra]"],
            "ca_hai": ["loi", "[C-ca-hai]"], "ra_le": ["loi", "[C-ra-le]"], "bk_rong_manh": ["loi", "[C-ca-hai]"],
            "ra_rong_le": ["loi", "[C-ra-le]"], "ra_rong_gate": ["loi", "[C-ra-le]"], "manh_rong": ["loi", "[C-hinh-dang]"],
            "manh_rong_gate": ["loi", "[C-ca-hai]"], "gate_cach": ["loi", "[C-ban-kinh]"],
            "gate_xuong_dong": ["loi", "[C-ban-kinh]"], "luoi": [_mong_che_do(e) for e in _luoi_che_do()],
            "luoi_git": [_mong_git(*o) for o in _luoi_git()]}
    sai = {t: [kq.get(t), m] if t not in ("luoi", "luoi_git") else
           [(i, x, y) for i, (x, y) in enumerate(zip(kq.get(t) or [], m)) if x != y][:5] + [len(kq.get(t) or []), len(m)]
           for t, m in mong.items() if kq.get(t) != m}
    bang(not sai, f"`_doc_che_do`/nguồn HEAD sai (thấy, mong | lưới: [(ô, thấy, mong)…, số ô thấy, số ô mong]): {sai}")
    # #698 M1/M1b: số ô bằng CÔNG THỨC từ kích thước miền mà cha TỰ dẫn xuất (biểu thức riêng, không gọi `_d698`) — bớt vị trí
    # hay bớt điểm mã ở con thì lệch. M5b: 0 ô lệch, không lớp nào không dựng được, khoá đã đo ⊇ B698 (mọi lớp ngoại lệ builtins).
    import builtins
    import unicodedata as u
    trong = lambda c: u.category(chr(c)) not in ("Lo", "Co", "Cn") or u.normalize("NFKC", chr(c)) != chr(c)
    nd, nt = 0, 1   # nt: mọi `c.isspace()` (trừ surrogate) cộng CR LF
    for c in (c for c in range(0x110000) if not 0xD800 <= c <= 0xDFFF):
        nd, nt = nd + trong(c), nt + chr(c).isspace()
    s1 = (nd + len(_N698)) * sum(2 * len(v) + 1 for v in ("manh", "3/8", "15/16", "a/b"))
    s2 = 2 * 3 * nd + (sum(map(trong, _R698)) + len(_N698)) * sum(2 * h + 1 for h in (40, 64)) + 2 * 2 * nt
    bang(kq["m1"] == [s1, s2, [], 0], f"M1/M1b #698 [ô doc, ô head, ô lệch đầu, tổng lệch]: {kq['m1']} ≠ [{s1}, {s2}, [], 0]")
    b698 = {f"{v.__module__}.{v.__qualname__}" for v in vars(builtins).values()
            if isinstance(v, type) and issubclass(v, BaseException)}
    bang(kq["m5b"][1:] == [[], 0, []] and b698 <= set(kq["m5b"][0]),
         f"M5b #698 [ô lệch, tổng lệch, không dựng được]: {kq['m5b'][1:]}; B698 thiếu {sorted(b698 - set(kq['m5b'][0]))[:5]}")
    # F34: lời gọi `git` — đúng argv trên CHÍNH `GOC` của tiến trình con, đủ capture/text và timeout 60.
    bang(kq["goi_git"] == [[["git", "-C", kq["goi_git"][1], "rev-parse", "HEAD"],
                            [["capture_output", True], ["text", True], ["timeout", 60]]], kq["goi_git"][1]],
         f"`_van_tay` gọi git sai tham số: {kq['goi_git']}")
    import hashlib
    sha = lambda b: hashlib.sha256(b).hexdigest()
    bang(kq["byte"]["luoi"] == [sha(b) for b in _luoi_byte()] and kq["byte"]["thuc"] == sha(Path(kq["byte"]["tep"]).read_bytes()),
         f"`_van_tay` phải băm TRỌN bytes (bảng biên/lớn/non-ASCII/hoa/khoảng trắng + TEP_TEST thật): {kq['byte']['luoi'][:3]}")
    dung(kq["van_tay"][0], f"giàn giáo git tạm không dựng được commit: {kq['van_tay']}")
    bang(kq["van_tay"] == [True] * 6, "`_van_tay` phải bám BYTES của TEP_TEST và HEAD thật của GOC, không git ⇒ None "
                                      f"(không-git, head, sha, đổi-byte-giữ-head, đổi-head): {kq['van_tay'][1:]}")


@ca
def t54_main_chon_DUNG_vong_ban_kinh_theo_che_do():
    """#668 F2 (Codex lượt 1, P2): `main()` phải đo TRỌN `DOT_BIEN` ở `du`, KHÔNG đo gì ở `gate`, ĐÚNG phần mảnh ở `manh`.

    Trước ca này, đột biến `if che_do in ("gate", "du")` sống sót qua mọi ca: CLI mặc định rc=0 mà bỏ trọn vòng bán
    kính — `t53` chỉ đo bộ ĐỌC chế độ, không đo `main` DÙNG chế độ ấy thế nào. Đo qua cửa `--tu-kiem-main` (chạy chính
    `main` với giàn giáo rẻ) nên đột biến trên đĩa cắn được.
    """
    kq = _doc_kq_tu_kiem("--tu-kiem-main")
    dung(kq["mong_du"] and kq["mong_manh"] and kq["ten_ca"], f"giàn giáo không dựng được kỳ vọng: {str(kq)[:300]}")
    so, cac, nd = kq["so"], kq["ten_ca"], kq["mong_du"]
    n, c0, c1, cn = len(cac), cac[0], cac[1], cac[-1]
    tb, ta = "batch_behavior_test", "python_alias_behavior_test"
    dau = [f"tk:{tb}", f"tk:{ta}"] + [f"ca:{t}" for t in cac]
    ghi = lambda gt, ly, kn="3/8", r="d con/manh 3.txt": [f"ghi:{kn}:{r}:True:{gt}:{ly}:True"]
    phong, ghi_dung, ghi_nen = [f"phong:True:[]:{so}"], ghi("dung", "none"), ghi("None", "nen")
    hai = lambda ten: [f"  DONG-{ten}-668", f"  DONG-{ten}-668-B"]   # mọi hàm giả in HAI dòng (F18: "chỉ dòng đầu")

    def day(do=(), du=True):   # nhánh đủ/gate: cổng cây thật → hai tự kiểm → báo cáo nền → song song → (bán kính đủ)
        return (dau + ["cong:True:None", "phan_hang:", "gian_giao:", f"nen:{list(do)}", f"song_song:{list(do)}"]
                + ([f"du:True:{list(do)}:{so}"] if du else []))

    def ra(tk=(), bq=(), do=(), loi=(), duoi=()):   # stdout (bỏ dòng trống) mà `main` PHẢI in, đúng thứ tự
        return ([f"  BỎ QUA (TIỀN KIỂM) {t}: bỏ qua có chủ đích {t}" for t in tk]
                + [f"  BỎ QUA {t}: ca giả {t}" for t in bq] + [f"  ĐỎ  {t}: ca giả {t}" for t in do]
                + [f"  ĐỎ  {t}: RuntimeError: ca giả {t}" for t in loi]
                + [f"cong_cu_test: {n - len(bq) - len(do) - len(loi)}/{n - len(bq)} đạt; tổng={n}, bỏ qua={len(bq)}, "
                   f"tiền kiểm bỏ qua={len(tk)}"] + list(duoi))

    def so_lieu(loi_db, tk=0, cong="ĐẠT", gate=False):
        return (f"SỐ LIỆU: ca={n} · đột biến={nd}" + (" (giao mảnh)" if gate else "") + f" · lỗi đột biến={loi_db}"
                f" · tiền kiểm bỏ qua={tk} · cổng cây thật={cong}")

    def chung(nen):   # dòng của cổng cây thật + báo cáo nền, in trước bán kính ở nhánh đủ/gate
        return hai("CONG") + (hai("NEN") if nen else [])

    def du_ra(loi_db, nen=0, tk=0, cong="ĐẠT"):
        return chung(nen) + ([f"BÁN KÍNH ĐỘT BIẾN ({nd} đột biến, mỗi ca đúng một" + (f"; LOẠI {nen} ca đỏ ở nền" if nen else "")
                              + f"; {so} tiến trình):"] + hai("BK1") + hai("BK2") + [so_lieu(loi_db, tk, cong)])

    def gate_ra(loi_db, nen=0, tk=0, cong="ĐẠT"):
        return chung(nen) + [f"BÁN KÍNH ĐỘT BIẾN ({nd} đột biến): GIAO cho job `gate-cong-cu` (mảnh) + `gate-cong-cu-gop` "
                             f"(gom) — KHÔNG đo trong tiến trình này (CONG_CU_TEST_BAN_KINH=manh)",
                             so_lieu(loi_db, tk, cong, gate=True)]

    def manh_ra(kn="3/8"):
        return [f"BÁN KÍNH ĐỘT BIẾN — MẢNH {kn} ({kq['mong_manh'][kn]}/{nd} đột biến; {so} tiến trình):"] + hai("BO-GHI")
    nen_ra = ["  ĐỎ  mảnh 3/8 [M-nen]: nền KHÔNG xanh — không đo bán kính, không ghi tệp"]
    # [mã thoát, nhật ký NGUYÊN (tên từng ca, thứ tự, tham số), stdout NGUYÊN (mọi dòng mang nghĩa, đúng thứ tự)].
    # Lỗi ĐÚNG 1 và ≥ 2, NHIỀU nguồn cùng lúc, N ≠ 8, hàm giả in nhiều dòng (F15/F18).
    mong = {
        "du": [0, day(), ra(duoi=du_ra(0))], "gate": [0, day(du=False), ra(duoi=gate_ra(0))],
        "manh": [0, dau + phong + ghi_dung, ra(duoi=manh_ra())], "cau_hinh_sai": [2, [], [
            "  ĐỎ  cấu hình chế độ: [C-ban-kinh] CONG_CU_TEST_BAN_KINH='x': chỉ nhận đúng 'manh'"]],
        "du_tk_batch": [1, day(), ra(tk=[tb], duoi=du_ra(0, tk=1))],
        "du_tk_alias": [1, day(), ra(tk=[ta], duoi=du_ra(0, tk=1))],
        "du_tk_ca_hai": [1, day(), ra(tk=[tb, ta], duoi=du_ra(0, tk=2))],
        "manh_tk_batch": [1, dau + ghi_nen, ra(tk=[tb], duoi=nen_ra)],
        "manh_tk_alias": [1, dau + ghi_nen, ra(tk=[ta], duoi=nen_ra)],
        "manh_ca_do": [1, dau + ghi_nen, ra(do=[cn], duoi=nen_ra)],
        "manh_ca_loi": [1, dau + ghi_nen, ra(loi=[c0], duoi=nen_ra)],
        "manh_ca_bq": [0, dau + phong + ghi_dung, ra(bq=[c1], duoi=manh_ra())],
        "du_ca_do": [1, day([cn]), ra(do=[cn], duoi=du_ra(1, nen=1))],
        "du_hai_ca_do": [1, day([c1, cn]), ra(do=[c1, cn], duoi=du_ra(1, nen=2))],
        "gate_ca_loi": [1, day([c0], du=False), ra(loi=[c0], duoi=gate_ra(1, nen=1))],
        "du_ca_bq": [0, day(), ra(bq=[c1], duoi=du_ra(0))],
        "du_hai_ca_bq": [0, day(), ra(bq=[c1, cac[2]], duoi=du_ra(0))],
        "con_rc": [1, dau + phong + ghi("None", "dung-rc3"), ra(duoi=manh_ra())],
        "con_rong": [1, dau + phong + ghi("None", "dung-rc0"), ra(duoi=manh_ra())],
        "con_hai": [1, dau + phong + ghi("None", "dung-rc3"), ra(duoi=manh_ra())],
        "con_sau": [1, dau + phong + ghi("None", "dung-rc5"), ra(duoi=manh_ra())],
        "ghi_do": [1, dau + phong + ghi_dung, ra(duoi=manh_ra())],
        "ghi_do_1": [1, dau + phong + ghi_dung, ra(duoi=manh_ra())],
        "du_cong_do": [1, day(), ra(duoi=du_ra(0, cong="HỎNG"))],
        "gate_cong_do": [1, day(du=False), ra(duoi=gate_ra(0, cong="HỎNG"))],
        "gate_ph_do": [1, day(du=False), ra(duoi=gate_ra(2))], "gate_gg_do": [1, day(du=False), ra(duoi=gate_ra(2))],
        "gate_ss_do": [1, day(du=False), ra(duoi=gate_ra(2))], "gate_ph_do_1": [1, day(du=False), ra(duoi=gate_ra(1))],
        "gate_nhieu_nguon": [1, day([cn], du=False), ra(do=[cn], duoi=gate_ra(5, nen=1, cong="HỎNG"))],
        "du_bk_do": [1, day(), ra(duoi=du_ra(2))], "du_bk_do_cuoi": [1, day(), ra(duoi=du_ra(2))],
        "du_bk_hai": [1, day(), ra(duoi=du_ra(4))], "du_bk_do_1": [1, day(), ra(duoi=du_ra(1))],
        "manh_516": [0, dau + phong + ghi("dung", "none", "5/16", "x"), ra(duoi=manh_ra("5/16"))],
        "manh_12": [0, dau + phong + ghi("dung", "none", "1/2", "x"), ra(duoi=manh_ra("1/2"))],
        "manh_0": [0, dau + phong + ghi("dung", "none", "0/8", "x"), ra(duoi=manh_ra("0/8"))],
        "du_nhieu_nguon": [1, day([cn]), ra(do=[cn], duoi=du_ra(55, nen=1))]}
    for h, b, t in _luoi_m3(n):   # #698 M3: kỳ vọng bằng CHÍNH các hàm dựng sẵn — ĐỎ ⇔ h > 0 hoặc t ≠ ∅, độc lập với b
        mong[f"m3698-{h}-{b}-{'+'.join(t)}"] = (
            [1, dau + ghi_nen, ra(tk=list(t), bq=cac[h:h + b], do=cac[:h], duoi=nen_ra)] if h or t
            else [0, dau + phong + ghi_dung, ra(bq=cac[h:h + b], duoi=manh_ra())])
    for name, mode, ki, ni, path, workers in _luoi_noi_main():
        so = workers
        if mode == "du":
            mong[name] = [0, day(), ra(duoi=du_ra(0))]
        elif mode in ("nen", "nen_do"):   # F44: nền đỏ do TIỀN KIỂM bỏ qua / do CA đỏ (`hong or tien_kiem_bo_qua`)
            kn = f"{ki}/{ni}"
            mong[name] = [1, dau + ghi("None", "nen", kn, path),
                          ra(**({"tk": [tb]} if mode == "nen" else {"do": [cn]}), duoi=[f"  ĐỎ  mảnh {kn} [M-nen]: nền KHÔNG xanh — không đo bán kính, không ghi tệp"])]
        else:
            kn = f"{ki}/{ni}"
            mong[name] = [0, dau + [f"phong:True:[]:{so}"] + ghi("dung", "none", kn, path), ra(duoi=manh_ra(kn))]
    so = kq["so1"]   # F27: closure đọc `so` lúc GỌI ⇒ hai kịch bản worker=1 dựng lại kỳ vọng với 1
    phong = [f"phong:True:[]:{so}"]
    mong.update({"manh_w1": [0, dau + phong + ghi_dung, ra(duoi=manh_ra())], "du_w1": [0, day(), ra(duoi=du_ra(0))]})
    sai = {t: str(kq.get(t))[:300] for t, m in mong.items() if kq.get(t) != m}
    bang(not sai, f"`main` nối SAI (kịch bản: thấy [rc, nhật ký, stdout]): {sai}")
    # F26 (Codex lượt 10): cửa CLI KHÔNG đối số — đúng thứ workflow chạy — phải VÀO `main` và TRUYỀN mã. Ở ĐÂY chứ không ở
    # `t52`: đột biến nuốt lỗi cấu hình trong `main` (`f7_cau_hinh_nuot`) đã chết ở phép so trên, không tới đây mà chạy
    # trọn suite. Ba lỗi cấu hình CHỒNG nhau (`C-ca-hai` → `C-hinh-dang` → `int` ném): gỡ một chốt của `_doc_che_do`
    # (việc của `t53`) vẫn dừng rc=2, không giết oan ca này.
    p = subprocess.run([sys.executable, str(TEP_TEST)], capture_output=True, text=True, timeout=120, cwd=str(GOC),
                       env={**os.environ, _BIEN_BAN_KINH: "hong", _BIEN_MANH: "a/b", _BIEN_MANH_RA: ""})
    bang(p.returncode == 2 and (p.stdout.splitlines() or [""])[0].startswith("  ĐỎ  cấu hình chế độ: ["),
         f"CLI không đối số phải vào `main` và trả rc=2 cấu hình: rc={p.returncode}, {p.stdout[:200]!r}")
    # F28 (Codex lượt 11): phép trên chỉ đo cấu hình HỎNG. Miền DƯƠNG (du/gate/mảnh hợp lệ × rc 0/1/2) chạy `main` thật
    # thì tốn cả suite mỗi đột biến, nên chạy CHÍNH khối `__main__` trích từ `TEP_TEST` (bản đột biến nếu có) với `main`
    # giả ghi lời gọi: dispatcher phải gọi `main` ĐÚNG một lần và trả NGUYÊN mã của nó, ở mọi chế độ.
    import types
    nguon = Path(TEP_TEST).read_text(encoding="utf-8")
    khoi = compile(nguon[nguon.index('\nif __name__ == "__main__":') + 1:], str(TEP_TEST), "exec")
    cu_env, sai = dict(os.environ), []

    def thoat(ma=0):
        raise SystemExit(ma)
    try:
        for ten, env in (("du", {}), ("gate", {_BIEN_BAN_KINH: "manh"}), ("manh", {_BIEN_MANH: "3/8", _BIEN_MANH_RA: "x"})):
            for ma in (0, 1, 2):
                for bien in (_BIEN_BAN_KINH, _BIEN_MANH, _BIEN_MANH_RA):
                    os.environ.pop(bien, None)
                os.environ.update(env)
                goi = []
                ns = {**globals(), "__name__": "__main__", "main": lambda: goi.append(1) or ma,
                      "sys": types.SimpleNamespace(argv=[str(TEP_TEST)], exit=thoat)}
                try:
                    exec(khoi, ns)
                    thay = "không thoát"
                except SystemExit as ex:
                    thay = ex.code
                if (thay, len(goi)) != (ma, 1):
                    sai.append((ten, ma, thay, len(goi)))
    finally:
        os.environ.clear()
        os.environ.update(cu_env)
    bang(not sai, f"dispatcher không đối số phải gọi `main` đúng 1 lần và trả nguyên mã (chế độ, mã main, thấy, số lời gọi): {sai}")


def _cong_tren_cay_that(goc, bo_quet=None):
    """(mã, dòng báo) — CHẠY chính cổng `bash_nen quet` trên cây THẬT.

    N31 — SINH TỪ r11, cross-review codex vòng 5, và đây là finding **P1** đầu tiên của packet.
    CI gọi `python ops/cong_cu_test.py` ở BA chỗ trong `.github/workflows/ci.yml` và KHÔNG chỗ
    nào gọi `ops/bash_nen.py quet`. Còn `main()` thì chỉ chạy ca trên cây GIẢ cộng bán kính đột
    biến. Tức cái cổng mà cả packet này sinh ra để dựng **chưa từng được nối vào chỗ nó gác**.

    ĐO ĐƯỢC, bằng chứng dương, trên một BẢN SAO kho (không chạm tệp ngoài write set): thêm
    `vi_pham_moi.py` có `shutil.which("bash")` rồi `git add`:
        `python3 ops/bash_nen.py quet --root .` ⇒ rc=2 DO, ngoai_danh_sach=['vi_pham_moi.py']
        `python3 ops/cong_cu_test.py`            ⇒ rc=1 (chỉ là nền t2_go_canary), và tên tệp
                                                   vi phạm xuất hiện **0 lần** trong cả báo cáo.

    BA TRẠNG THÁI, không phải hai: `DAT` ⇒ 0 · `DO` ⇒ lỗi · `KHONG_DO_DUOC` ⇒ CŨNG lỗi, kèm
    nhãn riêng. Gộp hai cái sau làm một là xoá đúng phân biệt packet này tồn tại để giữ.
    """
    # `bo_quet` CHỈ cho ca đo dùng. Một cây GIẢ không thoả bảng miễn trừ THẬT (ảnh chụp khai
    # 7 lời gọi, cây giả có 0 ⇒ lệch ⇒ ĐỎ OAN) — đúng cái bẫy `_bash_nen_voi_chua_chuyen` sinh
    # ra để chặn, và đây là lần thứ TƯ nó cắn trong packet này. Đường THẬT (`main()`) không
    # truyền gì, nên nó vẫn chạy đúng bộ quét thật trên cây thật.
    rc, bao = _quet(goc, bo_quet)
    if rc == 0:
        return 0, [f"CỔNG TRÊN CÂY THẬT: ĐẠT · nguon_tep={bao.get('nguon_tep')} "
                   f"· nguon_noi_dung={bao.get('nguon_noi_dung')}"]
    nhan = "ĐỎ" if bao.get("trang_thai") == "DO" else "KHÔNG_ĐO_ĐƯỢC"
    return 1, [f"CỔNG TRÊN CÂY THẬT: {nhan} (rc={rc})",
               f"    {str(bao.get('ly_do'))[:400]}"]


def _do_mot(ten_db, do_o_nen):
    """BẢN GHI ĐO của MỘT đột biến — DỮ LIỆU, không phải văn bản báo cáo.

    `["do", tên, ca_đích, {ca: [trạng_thái, lý_do]}]`, hoặc `["loi", tên, thông_điệp]` khi `_do_ban_kinh` ném
    `AssertionError`. Cùng một hàm cho đường tuần tự lẫn tiến trình con.
    """
    try:
        ket, ca_dich = _do_ban_kinh(ten_db, bo_qua_ca=do_o_nen)
    except AssertionError as ex:
        return ["loi", ten_db, str(ex)]
    return ["do", ten_db, ca_dich, {t: [tt, ly] for t, (tt, ly) in ket.items()}]


def _ket_luan_ban_ghi(ban_ghi, do_o_nen):
    """(dòng báo, số lỗi) từ một bản ghi ĐÃ KIỂM — do CHÍNH tiến trình này dựng, qua `_ket_luan_ban_kinh`."""
    if ban_ghi[0] == "loi":
        return [f"  ĐỎ  {ban_ghi[1]}: {ban_ghi[2]}"], 1
    _, ten_db, ca_dich, ket = ban_ghi
    return _ket_luan_ban_kinh(ten_db, ca_dich, {t: tuple(v) for t, v in ket.items()}, len(CA), do_o_nen)


def _ban_kinh_mot(ten_db, do_o_nen):
    """(dòng báo, số lỗi) của MỘT đột biến, đường tuần tự — ĐÚNG hai hàm mà đường song song dùng."""
    return _ket_luan_ban_ghi(_do_mot(ten_db, do_o_nen), do_o_nen)


_TRAN_TIEN_TRINH = 16   # N128 — trần CỨNG cho số tiến trình, bất kể biến môi trường nói gì


def _so_tien_trinh_ban_kinh():
    """Số tiến trình đo bán kính. `CONG_CU_TEST_TIEN_TRINH` ghi đè; mặc định số lõi, trần 4; trần cứng 16.

    N126 (r38): job `gate` có trần 60 phút mà vòng bán kính TUẦN TỰ (53 ca × 212 đột biến) đã vượt nó —
    run 36286651867 (r34) và 36299153762 (r36) đều bị HUỶ ở phút 60,2. Mỗi đột biến vốn chạy cô lập (cây
    tạm riêng theo tên, `globals()` tráo rồi trả), nên tách thành tiến trình con là an toàn; KHÔNG dùng luồng
    vì phép tráo `globals()` là của cả tiến trình. Giá trị không đọc được ⇒ 1, không đoán.
    N128 (r40, codex vòng 34 — S1): giá trị ghi đè cực lớn (`1000000000`) từng được dùng NGUYÊN để dựng nhóm;
    nay kẹp ở `_TRAN_TIEN_TRINH`, và `_ban_kinh_moi_dot_bien` kẹp tiếp theo số đột biến.
    """
    tho = os.environ.get("CONG_CU_TEST_TIEN_TRINH")
    if tho is not None:
        so = int(tho) if tho.strip().isdigit() and int(tho) >= 1 else 1
    else:
        so = max(1, min(4, os.cpu_count() or 1))
    return min(so, _TRAN_TIEN_TRINH)


_SO_LAN_PHONG = [0]     # đếm số tiến trình con đã phóng — chỉ tự kiểm (3) đọc


def _ban_kinh_moi_dot_bien(cac_ten, do_o_nen, so_tien_trinh):
    """[(dòng báo, số lỗi)] theo ĐÚNG thứ tự `cac_ten`: tuần tự trong tiến trình này, hay chia cho tiến trình con.

    FAIL-CLOSE: đột biến nào tiến trình con KHÔNG trả bản ghi hợp lệ thì thành một dòng `ĐỎ` kèm lý do và tính MỘT
    lỗi — không bao giờ biến mất khỏi bảng.

    N129 — ĐỔI THIẾT KẾ (chủ kho, 2026-09-27, r44): con chỉ gửi DỮ LIỆU ĐO, cha tự dựng dòng báo và số lỗi. Ba vòng
    codex liên tiếp (36 · 37 · 38: U1 mã thoát, V1 danh sách rỗng, W1 dòng `ok` nhiều dòng) cùng một gốc: cha TIN
    VĂN BẢN của con rồi đoán văn bản ấy có hợp lệ không, và lần nào cũng còn một hình dạng lọt. Nay không văn bản
    nào của con quyết định số lỗi: cha kiểm bản ghi theo những gì CHÍNH NÓ biết (`DOT_BIEN`, `CA`, bộ từ vựng
    trạng thái) rồi gọi CÙNG `_ket_luan_ban_kinh` mà đường tuần tự gọi. Lý do trong bản ghi chỉ để HIỂN THỊ.

    LỚP ĐÃ KHÉP (chủ kho, 2026-09-27, r41): TIẾN TRÌNH CON TREO. Ba vòng codex liên tiếp (33 · 34 · 35) tìm ra khe
    mới trong chính bộ máy hạn giờ/giết cây dựng để in dòng `ĐỎ` trước trần job (N127, N128). Chủ kho khép lớp và
    GỠ bộ máy ấy: một con treo thì job `gate` bị GitHub HUỶ ở trần 60 phút, mà huỷ KHÔNG phải success, nên land
    vẫn bị chặn — fail-close do CI. Cái mất đi chỉ là dòng `ĐỎ` chẩn đoán; không có đường nào để một con treo cho
    ra XANH. Đây là nợ có tên, không phải lỗ chưa biết.
    """
    if not cac_ten:
        return []
    so = max(1, min(int(so_tien_trinh), len(cac_ten), _TRAN_TIEN_TRINH))
    if so == 1:
        return [_ban_kinh_mot(t, do_o_nen) for t in cac_ten]
    kq = {}
    for n, rc, ra in _phong_con(cac_ten, do_o_nen, so):
        nhan, ly_do = _nhan_ket_qua_con(n, rc, ra, do_o_nen)
        if nhan is None:
            for ten in n:
                kq[ten] = ([f"  ĐỎ  {ten}: tiến trình con KHÔNG trả kết quả hợp lệ ({ly_do}; rc={rc}, "
                            f"đuôi đầu ra: {ra[-300:]!r})"], 1)
        else:
            for ten, ban_ghi in nhan.items():
                kq[ten] = _ket_luan_ban_ghi(ban_ghi, do_o_nen)
    return [kq[t] for t in cac_ten]


def _phong_con(cac_ten, do_o_nen, so):
    """[(nhóm, mã thoát, đầu ra)] — chia `cac_ten` cho `so` tiến trình con `--ban-kinh-con`, đợi hết. KHÔNG kết luận gì.

    #668: tách khỏi `_ban_kinh_moi_dot_bien` để chế độ MẢNH dùng ĐÚNG đường phóng + bộ nhận của đường song song.
    """
    so = max(1, min(int(so), len(cac_ten), _TRAN_TIEN_TRINH))
    cac_con = []
    for n in [cac_ten[i::so] for i in range(so)]:
        tep_ra = tempfile.TemporaryFile()
        p = subprocess.Popen([sys.executable, str(TEP_TEST), "--ban-kinh-con",
                              json.dumps(sorted(do_o_nen)), *n],
                             stdout=tep_ra, stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL,
                             cwd=str(GOC))
        _SO_LAN_PHONG[0] += 1
        cac_con.append((n, p, tep_ra))
    kq = []
    for n, p, tep_ra in cac_con:
        rc = p.wait()
        tep_ra.seek(0)
        kq.append((n, rc, tep_ra.read().decode("utf-8", "replace")))
        tep_ra.close()
    return kq


_TRANG_THAI_CA = ("qua", "bo_qua", "giet_that", "tin_dung_gia")   # đúng bộ `_chay_1_ca` trả


def _nhan_ket_qua_con(n, rc, ra, do_o_nen):
    """(bản ghi theo tên, None) khi đầu ra của MỘT tiến trình con hợp lệ TRỌN VẸN; (None, lý do) nếu không.

    Mỗi đường làm CẢ NHÓM thành `ĐỎ`:
      (a) mã thoát khác 0;  (b) dòng `BKCON` không phân tích được, hoặc sai số phần tử/loại;  (c) tên ngoài nhóm;
      (d) tên lặp;  (e) bản ghi sai so với điều CHA biết — xem `_ban_ghi_sai`;  (f) thiếu bản ghi.
    """
    if rc != 0:
        return None, f"mã thoát {rc}"
    kq = {}
    # X3 (r45, codex vòng 39): tách CHỈ theo `\n` mà con thực sự viết. `splitlines()` còn cắt ở U+2028, U+2029,
    # U+0085, `\x0b`… nên một lý do HỢP LỆ chứa các ký tự ấy từng xé đôi bản ghi — chỉ ở đường song song.
    for dong in ra.split("\n"):
        dong = dong.rstrip("\r")
        if not dong.startswith("BKCON "):
            continue
        try:
            ban_ghi = json.loads(dong[6:])
            ten = ban_ghi[1]
            if not ((ban_ghi[0] == "do" and len(ban_ghi) == 4) or (ban_ghi[0] == "loi" and len(ban_ghi) == 3)):
                raise ValueError("loại/độ dài")
        except (ValueError, TypeError, KeyError, IndexError):
            return None, f"dòng BKCON hỏng: {dong[:120]!r}"
        if ten not in n:
            return None, f"tên ngoài nhóm: {ten!r}"
        if ten in kq:
            return None, f"tên lặp: {ten!r}"
        sai = _ban_ghi_sai(ban_ghi, do_o_nen)
        if sai:
            return None, f"bản ghi sai cho {ten!r}: {sai}"
        kq[ten] = ban_ghi
    thieu = [t for t in n if t not in kq]
    if thieu:
        return None, f"thiếu kết quả: {thieu!r}"
    return kq, None


def _ban_ghi_sai(ban_ghi, do_o_nen):
    """Lý do bản ghi SAI so với điều CHA tự biết, hoặc `None`. Không đọc văn bản nào của con để quyết định:
      (e1) ca đích ≠ ca đích mà `DOT_BIEN` của CHÍNH tiến trình này khai cho tên ấy;
      (e2) tập ca ≠ đúng tập ca đã chạy (`CA` trừ ca đỏ ở nền) — thiếu hay thừa đều sai;
      (e3) trạng thái ngoài `_TRANG_THAI_CA`;  (e4) lý do không phải chuỗi hay `None`;
      (e5) bản ghi `loi` mà thông điệp không phải chuỗi.
    """
    if ban_ghi[0] == "loi":
        return None if isinstance(ban_ghi[2], str) else "(e5) thông điệp không phải chuỗi"
    _, ten, ca_dich, ket = ban_ghi
    if ca_dich != _dich_mong(ten, do_o_nen):
        return f"(e1) ca đích {ca_dich!r} ≠ {_dich_mong(ten, do_o_nen)!r}"
    if not isinstance(ket, dict) or set(ket) != _cac_ca_da_chay(do_o_nen):
        return "(e2) tập ca không đúng tập ca đã chạy"
    for v in ket.values():
        if not isinstance(v, list) or len(v) != 2 or v[0] not in _TRANG_THAI_CA:
            return f"(e3) trạng thái lạ: {v!r}"[:200]
        if not (v[1] is None or isinstance(v[1], str)):
            return f"(e4) lý do không phải chuỗi: {v!r}"[:200]
    return None


def _cac_ca_da_chay(do_o_nen):
    return {fn.__name__ for fn in CA} - set(do_o_nen)


# Tên GIẢ chỉ cửa tiến trình con nhận ra — dùng cho tự kiểm, không bao giờ nằm trong `DOT_BIEN`.
_TIEN_TO_GIA = "__gia_"   # tiền tố DÀNH RIÊNG: tự kiểm đòi 0 tên `DOT_BIEN` mang nó (X2)
_TEN_GIA_NHANH = "__gia_nhanh_n126__"
# N129: mỗi con giả vi phạm ĐÚNG MỘT chốt và lọt qua MỌI chốt còn lại — không thế thì gỡ chốt của nó vẫn bị chốt
# khác bắt, và chốt ấy không có răng riêng (đo được ở r43). (f) không in gì.
_GIA_BAT_THUONG = {
    "__gia_thoat7_n129__": "a",
    "__gia_hong_n129__": "b",
    "__gia_ngoai_n129__": "c",
    "__gia_lap_n129__": "d",
    "__gia_dich_n129__": "e1",
    "__gia_thieu_ca_n129__": "e2",
    "__gia_thua_ca_n129__": "e2b",
    "__gia_trang_thai_n129__": "e3",
    "__gia_ly_do_n129__": "e4",
    "__gia_thong_diep_n129__": "e5",
    "__gia_thieu_n129__": "f",
}
# X3: bản ghi HỢP LỆ mà lý do chứa U+2028, U+2029, U+0085 — in NGUYÊN VĂN (không thoát), phải được NHẬN.
_TEN_GIA_PHAN_DONG = "__gia_phan_dong_n129__"
# X2 (r45, codex vòng 39): tập tên giả ĐÓNG, liệt kê ĐỦ. Bản r44 nhận diện tên giả bằng TIỀN TỐ, nên một đột biến
# THẬT tên `__gia_…` sẽ được dựng bản ghi đạt mà không hề đo. Nay chỉ tên trong tập này — và KHÔNG có trong
# `DOT_BIEN` — mới đi nhánh giả; tên thật luôn qua `_do_mot`.
_TEN_GIA_TAT_CA = frozenset({_TEN_GIA_NHANH, _TEN_GIA_NHANH + "b", _TEN_GIA_PHAN_DONG, *_GIA_BAT_THUONG,
                             *(t + "_la" for t in _GIA_BAT_THUONG)})


def _la_ten_gia(ten):
    return ten not in DOT_BIEN and ten in _TEN_GIA_TAT_CA


def _dich_mong(ten, do_o_nen):
    """Ca đích mà CHA chờ cho một tên: của `DOT_BIEN`, hay — với tên giả `__gia_*` — ca đầu tiên đã chạy.

    MỌI tên giả đều có đích, kể cả tên ngoài nhóm của con giả (c): không thế thì (e1) bắt trước (c) và (c) mất răng.
    """
    if ten in DOT_BIEN:
        return DOT_BIEN[ten][5]
    if _la_ten_gia(ten):
        return sorted(_cac_ca_da_chay(do_o_nen))[0]
    return None


def _ban_ghi_gia(ten, do_o_nen):
    """Bản ghi `ok` hợp lệ của con giả: đích `giet_that`, mọi ca khác `qua`."""
    dich = _dich_mong(ten, do_o_nen)
    return ["do", ten, dich, {t: ["giet_that" if t == dich else "qua", "giả" if t == dich else None]
                              for t in _cac_ca_da_chay(do_o_nen)}]


def _in_ban_kinh_con():
    """Cửa tiến trình con của N126: đo bán kính các đột biến được giao, in mỗi BẢN GHI một dòng `BKCON`."""
    i = sys.argv.index("--ban-kinh-con")
    do_o_nen = json.loads(sys.argv[i + 1])
    ma_thoat = 0
    # ASCII thuần: stdout của con đổ vào tệp, mà trên Windows mã hoá mặc định của nó KHÔNG phải UTF-8 — chữ Việt
    # trong lý do sẽ làm `print` ném. Thoát hết thì đường vận chuyển không phụ thuộc mã hoá của nền.
    in_ = lambda bg: print("BKCON " + json.dumps(bg, ensure_ascii=True), flush=True)
    for ten in sys.argv[i + 2:]:
        kieu = _GIA_BAT_THUONG.get(ten)
        if not _la_ten_gia(ten):
            in_(_do_mot(ten, do_o_nen))
            continue
        if ten == _TEN_GIA_PHAN_DONG:
            bg = _ban_ghi_gia(ten, do_o_nen)
            bg[3][bg[2]][1] = "giả\u2028giữa\u2029cuối\u0085hết"
            # Y1 (r46, codex vòng 40): ghi BYTE UTF-8 thẳng vào `buffer`, KHÔNG qua `print`. Qua `print` thì mã hoá
            # stdout của con (Windows cục bộ, `PYTHONIOENCODING=ascii`) ném trước khi phép thử kịp đo cách TÁCH —
            # tức chính phép thử lại mang về phụ thuộc mã hoá mà đường thật đã gỡ.
            sys.stdout.flush()
            sys.stdout.buffer.write(("BKCON " + json.dumps(bg, ensure_ascii=False) + "\n").encode("utf-8"))
            sys.stdout.buffer.flush()
            continue
        if kieu == "f":
            continue
        bg = _ban_ghi_gia(ten, do_o_nen)
        khac = sorted(t for t in bg[3] if t != bg[2])[0]
        if kieu == "b":
            in_(bg)
            print("BKCON " + json.dumps(bg)[:-1], flush=True)
            continue
        if kieu == "c":
            in_(bg)
            in_(_ban_ghi_gia(ten + "_la", do_o_nen))
            continue
        if kieu == "e1":
            bg[2] = khac
            bg[3][khac], bg[3][_dich_mong(ten, do_o_nen)] = ["giet_that", "giả"], ["qua", None]
        elif kieu == "e2":
            del bg[3][khac]
        elif kieu == "e2b":
            bg[3]["t999_ca_khong_co"] = ["qua", None]
        elif kieu == "e3":
            bg[3][khac] = ["xanh", None]
        elif kieu == "e4":
            bg[3][khac] = ["qua", 5]
        elif kieu == "e5":
            bg = ["loi", ten, 5]
        in_(bg)
        if kieu == "d":
            in_(bg)
        if kieu == "a":
            ma_thoat = 7
    sys.exit(ma_thoat)


def _tu_kiem_song_song(do_o_nen):
    """Số lỗi của phép tự kiểm N126 — chạy TRƯỚC bảng bán kính.

    Sáu chốt:
      (1) ba đột biến thật đo SONG SONG (2 tiến trình) phải cho ĐÚNG dòng báo, số lỗi và THỨ TỰ như TUẦN TỰ — hai
          đường dùng CÙNG `_do_mot` + `_ket_luan_ban_ghi`, nên chốt này đo cả đường vận chuyển bản ghi;
      (2) một tên KHÔNG có trong `DOT_BIEN` phải thành dòng `ĐỎ` + 1 lỗi, không biến mất khỏi bảng;
      (3) N128 S1: số tiến trình `10**9` với hai tên giả phải xong ngay và phóng ĐÚNG hai tiến trình;
      (4) N129: mỗi con giả bất thường phải thành dòng `ĐỎ` mang ĐÚNG lý do từ chối + 1 lỗi, trong khi con BÌNH
          THƯỜNG chạy cùng lượt vẫn `ok` đúng thứ tự — chốt hai chiều, để bản vá "từ chối tất cả" cũng HỎNG;
      (5) X3: bản ghi hợp lệ có U+2028/U+2029/U+0085 NGUYÊN VĂN trong lý do phải được NHẬN;
      (6) X2: 0 tên `DOT_BIEN` mang tiền tố dành riêng, và một tên `__gia_…` KHÔNG thuộc tập giả phải được ĐO
          thật (`_do_mot` ⇒ không có trong `DOT_BIEN` ⇒ con chết ⇒ `ĐỎ`), không được dựng bản ghi đạt.
    """
    # BA đột biến cho HAI tiến trình ⇒ một nhóm có hai tên (`[a, c]`, `[b]`): bản ráp theo thứ tự NHÓM
    # thay vì thứ tự GỐC sẽ lệch ở đây. Hai tên cho hai tiến trình thì không phân biệt được hai cách ráp.
    mau = [t for t in ("t1_rc_gop", "bn_khong_tran_tep", "bn_khong_git_bo_kiem_oid") if t in DOT_BIEN]
    loi = 0
    tuan_tu = _ban_kinh_moi_dot_bien(mau, do_o_nen, 1)
    song_song = _ban_kinh_moi_dot_bien(mau, do_o_nen, 2)
    if len(mau) != 3 or tuan_tu != song_song or any(l for _, l in tuan_tu):
        print(f"  ĐỎ  tự kiểm song song (1): tuần tự {tuan_tu!r} ≠ song song {song_song!r}")
        loi += 1
    ma = "__khong_ton_tai_n126__"
    ket = _ban_kinh_moi_dot_bien([_TEN_GIA_NHANH, ma], do_o_nen, 2)
    if len(ket) != 2 or ket[1][1] != 1 or not ket[1][0][0].startswith(f"  ĐỎ  {ma}:"):
        print(f"  ĐỎ  tự kiểm song song (2): tên lạ không thành dòng ĐỎ: {ket!r}")
        loi += 1
    ok_gia = _ket_luan_ban_ghi(_ban_ghi_gia(_TEN_GIA_NHANH, do_o_nen), do_o_nen)
    if ok_gia[1] != 0:
        print(f"  ĐỎ  tự kiểm song song: bản ghi giả hợp lệ không ra `ok`: {ok_gia!r}")
        loi += 1
    truoc, t0 = _SO_LAN_PHONG[0], time.monotonic()
    ket = _ban_kinh_moi_dot_bien([_TEN_GIA_NHANH, _TEN_GIA_NHANH + "b"], do_o_nen, 10 ** 9)
    phong, giay = _SO_LAN_PHONG[0] - truoc, time.monotonic() - t0
    if phong != 2 or giay > 60 or ket[0] != ok_gia:
        print(f"  ĐỎ  tự kiểm song song (3): 10**9 tiến trình phải kẹp về 2: phóng {phong}, {giay:.1f}s")
        loi += 1
    for gia, kieu in _GIA_BAT_THUONG.items():
        ket = _ban_kinh_moi_dot_bien([_TEN_GIA_NHANH, gia], do_o_nen, 2)
        # Đòi LÝ DO từ chối, không chỉ nhãn ĐỎ: bản ghi `loi` tự ra nhãn ĐỎ, nên nhãn thôi không phân biệt được
        # "bị từ chối" với "được nhận nhầm".
        if (len(ket) != 2 or ket[0] != ok_gia or ket[1][1] != 1
                or not ket[1][0][0].startswith(f"  ĐỎ  {gia}: tiến trình con KHÔNG trả kết quả hợp lệ")):
            print(f"  ĐỎ  tự kiểm song song (4{kieu}): con bất thường không thành dòng ĐỎ: {ket!r}"[:600])
            loi += 1
    ket = _ban_kinh_moi_dot_bien([_TEN_GIA_NHANH, _TEN_GIA_PHAN_DONG], do_o_nen, 2)
    mong = _ket_luan_ban_ghi(_ban_ghi_gia(_TEN_GIA_PHAN_DONG, do_o_nen), do_o_nen)
    if len(ket) != 2 or ket[0] != ok_gia or ket[1] != mong or mong[1] != 0:
        print(f"  ĐỎ  tự kiểm song song (5): bản ghi có ký tự phân dòng Unicode bị từ chối: {ket!r}"[:600])
        loi += 1
    trung = sorted(t for t in DOT_BIEN if t.startswith(_TIEN_TO_GIA))
    tuong_lai = _TIEN_TO_GIA + "tuong_lai_that_n129__"
    ket = _ban_kinh_moi_dot_bien([_TEN_GIA_NHANH, tuong_lai], do_o_nen, 2)
    if trung or len(ket) != 2 or ket[1][1] != 1 or not ket[1][0][0].startswith(f"  ĐỎ  {tuong_lai}:"):
        print(f"  ĐỎ  tự kiểm song song (6): tên dành riêng trong DOT_BIEN {trung!r}, hay tên `__gia_` lạ "
              f"được dựng bản ghi đạt: {ket!r}"[:600])
        loi += 1
    print(f"TỰ KIỂM SONG SONG (N126): {'ĐẠT' if not loi else 'HỎNG'}")
    return loi


# ----------------------------------------------------- #668 CI-G5-CONG-CU-CHIA-MANH: gate · mảnh · gom
# Đo 28-09-2026: vòng bán kính là ~93 % bước G5 (~43/46 phút) vì mỗi đột biến chạy lại TRỌN `CA`, và runner chỉ có
# 2 lõi. Nhanh lên được chỉ bằng nhiều RUNNER. Ba chế độ, đọc từ biến môi trường bằng MỘT hàm thuần:
#   · vắng mọi biến ⇒ `du`   — hành vi cũ, đo trọn bán kính tại chỗ;
#   · `CONG_CU_TEST_BAN_KINH=manh` ⇒ `gate` — không đo bán kính ở đây, job `gate-cong-cu`+`gate-cong-cu-gop` đo;
#   · `CONG_CU_TEST_MANH=k/N` + `CONG_CU_TEST_MANH_RA=<tệp>` ⇒ `manh` — đo đột biến `i % N == k`, ghi bản ghi `BKCON`.
# Tệp mảnh chứa ĐÚNG các dòng `BKCON` mà tiến trình con vẫn in (hợp đồng N129: con gửi DỮ LIỆU, cha kết luận), nên
# `--gop` kiểm lại bằng CÙNG `_nhan_ket_qua_con` + `_ket_luan_ban_ghi` — không có đường phân hạng thứ hai.
_BIEN_BAN_KINH, _BIEN_MANH, _BIEN_MANH_RA = "CONG_CU_TEST_BAN_KINH", "CONG_CU_TEST_MANH", "CONG_CU_TEST_MANH_RA"
_TRAN_MANH = 16
_PHIEN_BAN_MANH = 1
_KHOA_DAU_MANH = frozenset({"phien_ban", "manh", "so_manh", "sha256_test", "head"})


def _do_co_symlink():
    """Nền này tạo được symlink không (Windows không đặc quyền thì KHÔNG). Kịch bản + đột biến symlink chỉ đăng ký khi CÓ:
    đăng ký mà không dựng được kịch bản thì đột biến ấy sống trên nền đó và làm ĐỎ oan cả vòng bán kính."""
    try:
        with tempfile.TemporaryDirectory() as d:
            os.symlink(os.path.join(d, "a"), os.path.join(d, "b"))
        return True
    except (OSError, NotImplementedError, AttributeError):
        return False


_TRUOC_NANG_LUC = dict(DOT_BIEN)   # F43/F45: ảnh DOT_BIEN (tên VÀ định nghĩa) TRƯỚC mọi đăng ký theo năng lực
_CO_SYMLINK = _do_co_symlink()
if _CO_SYMLINK:   # F24: chỉ đo được ở nền có symlink (xem `_do_co_symlink`)
    DOT_BIEN["f24_nhan_symlink"] = ("ops/cong_cu_test.py", '        if p.is_symlink() or not p.is_file():\n', '        if not p.is_file():  # đột biến: nhận symlink\n',
                                    "TEP_TEST", _KEM_TEP_TEST, _CA_668["t52_"])
    # F37 (Codex lượt 15): đột biến theo NĂNG LỰC, cùng điều kiện với f24 — nền không symlink thì fixture `ghi_gay` không chạy.
    DOT_BIEN["f35_writer_broken_link"] = ("ops/cong_cu_test.py", '    if tep.exists() or tep.is_symlink():\n',
                                          '    if tep.exists():\n', "TEP_TEST", _KEM_TEP_TEST, _CA_668["t52_"])
    # F37: bỏ TỪNG đăng ký chỉ đo được khi nhánh có năng lực chạy — đăng ký vô điều kiện thì nền không symlink sống.
    for _ten, _ca, _tim, _thay in (
        ('f37_bo_f24', 't52_', '    DOT_BIEN["f24_nhan_symlink"] = ("ops/cong_cu_test.py", \'        if p.is_symlink() or not p.is_file():\\n\', \'        if not p.is_file():  # đột biến: nhận symlink\\n\',\n',
         '    _bo = ("ops/cong_cu_test.py", \'        if p.is_symlink() or not p.is_file():\\n\', \'        if not p.is_file():  # đột biến: nhận symlink\\n\',\n'),
        ('f37_bo_f35', 't52_', '    DOT_BIEN["f35_writer_broken_link"] = ("ops/cong_cu_test.py", \'    if tep.exists() or tep.is_symlink():\\n\',\n',
         '    _bo = ("ops/cong_cu_test.py", \'    if tep.exists() or tep.is_symlink():\\n\',\n'),
        # F40 (Codex lượt 18): khối đăng ký phía False cũng phải có ĐIỀU KIỆN THẬT — `if True:` chỉ khác bản gốc trên nền CÓ symlink
        # (khi đó khối phía False đăng ký thêm `f37_dk_luon_dung` ⇒ ô năng lực của t52 lệch).
        ('f40_false_luon', 't52_', 'if not _CO_SYMLINK:\n', 'if True:\n'),
        # F41 (Codex lượt 19): danh TÍNH từng tên có điều kiện — chỉ đăng ký ở miền phép đổi thực sự khác gốc.
        ('f41_bo_f40_luon', 't52_', "        ('f40_false_luon', 't52_', 'if not _CO_SYMLINK:\\n', 'if True:\\n'),\n", '\n'),
        ('f41_f40_khong_ra_ngoai', 't52_', '    DOT_BIEN["f40_false_khong"] = ("ops/cong_cu_test.py", \'if not _CO_SYMLINK:\\n\', \'if False:\\n\', "TEP_TEST", _KEM_TEP_TEST, _CA_668["t52_"])\n', 'DOT_BIEN["f40_false_khong"] = ("ops/cong_cu_test.py", \'if not _CO_SYMLINK:\\n\', \'if False:\\n\', "TEP_TEST", _KEM_TEP_TEST, _CA_668["t52_"])\n'),
    ):
        DOT_BIEN[_ten] = ("ops/cong_cu_test.py", _tim, _thay, "TEP_TEST", _KEM_TEP_TEST, _CA_668[_ca])
if not _CO_SYMLINK:
    # `if True:` chỉ KHÁC bản gốc khi nền không có symlink (khi đó chốt registry của t52 bắt: False mà có tên).
    DOT_BIEN["f37_dk_luon_dung"] = ("ops/cong_cu_test.py", 'if _CO_SYMLINK:   # F24: chỉ đo được ở nền có symlink (xem `_do_co_symlink`)\n',
                                    'if True:   # đột biến\n', "TEP_TEST", _KEM_TEP_TEST, _CA_668["t52_"])
    # F41 (Codex lượt 19): bỏ / đẩy ra ngoài TỪNG đăng ký phía False — chỉ khác gốc trên nền KHÔNG symlink. F40 (dòng cuối khối):
    # `if False:` chỉ khác bản gốc trên nền KHÔNG symlink (khối phía False không chạy ⇒ tên phía False mất).
    DOT_BIEN["f41_bo_f40_khong"] = ("ops/cong_cu_test.py", '    DOT_BIEN["f40_false_khong"] = ("ops/cong_cu_test.py", \'if not _CO_SYMLINK:\\n\', \'if False:\\n\', "TEP_TEST", _KEM_TEP_TEST, _CA_668["t52_"])\n', '    pass\n', "TEP_TEST", _KEM_TEP_TEST, _CA_668["t52_"])
    DOT_BIEN["f41_f40_luon_ra_ngoai"] = ("ops/cong_cu_test.py", '    DOT_BIEN["f40_false_khong"] = ("ops/cong_cu_test.py", \'if not _CO_SYMLINK:\\n\', \'if False:\\n\', "TEP_TEST", _KEM_TEP_TEST, _CA_668["t52_"])\n', '    DOT_BIEN["f40_false_khong"] = ("ops/cong_cu_test.py", \'if not _CO_SYMLINK:\\n\', \'if False:\\n\', "TEP_TEST", _KEM_TEP_TEST, _CA_668["t52_"])\n' + 'DOT_BIEN["f40_false_luon"] = DOT_BIEN["f40_false_khong"]\n',
                                         "TEP_TEST", _KEM_TEP_TEST, _CA_668["t52_"])
    DOT_BIEN["f40_false_khong"] = ("ops/cong_cu_test.py", 'if not _CO_SYMLINK:\n', 'if False:\n', "TEP_TEST", _KEM_TEP_TEST, _CA_668["t52_"])
# F43: tên đăng ký theo năng lực = HIỆU hai ảnh — quan sát KHÔNG lọc theo oracle, tên mới ngoài oracle ⇒ t52 ĐỎ.
# F45: tên THÊM, BỚT hay ĐỔI định nghĩa giữa hai ảnh — hiệu tập khoá bỏ sót xoá/ghi đè trong cửa sổ.
_TEN_NANG_LUC = frozenset(t for t in DOT_BIEN.keys() | _TRUOC_NANG_LUC.keys() if DOT_BIEN.get(t) != _TRUOC_NANG_LUC.get(t))
# NỢ (KHÔNG ĐO ĐƯỢC): nền VẮNG thuộc tính `os.symlink` (nhánh AttributeError của `_do_co_symlink`) không được đo trong bộ này —
# quyết định chủ kho sau review lượt 17 (F39); runner chuẩn Ubuntu/Windows có `os.symlink`; không mô phỏng.


def _doc_che_do(env):
    """(chế độ, tham số) từ `env`; cấu hình sai ⇒ `ValueError` mang THẺ `[C-…]`. Hàm THUẦN, không đọc `os.environ`.

    Fail-closed: giá trị lạ — kể cả chuỗi RỖNG — là lỗi, không phải "coi như vắng". Một biến đặt nhầm mà lặng lẽ rơi
    về `du` thì job mảnh chạy TRỌN bán kính (chậm nhưng xanh), còn rơi về `gate` thì không ai đo bán kính cả.
    """
    import re
    bk, mh, ra = env.get(_BIEN_BAN_KINH), env.get(_BIEN_MANH), env.get(_BIEN_MANH_RA)
    if mh is None:
        if ra is not None:
            raise ValueError(f"[C-ra-le] {_BIEN_MANH_RA} đặt mà vắng {_BIEN_MANH}")
        if bk is None:
            return "du", None
        if bk != "manh":
            raise ValueError(f"[C-ban-kinh] {_BIEN_BAN_KINH}={bk!r}: chỉ nhận đúng 'manh'")
        return "gate", None
    if bk is not None:
        raise ValueError(f"[C-ca-hai] {_BIEN_MANH} và {_BIEN_BAN_KINH} không được cùng đặt")
    m = re.fullmatch(r"(0|[1-9][0-9]?)/([1-9][0-9]?)", mh)
    if not m:
        raise ValueError(f"[C-hinh-dang] {_BIEN_MANH}={mh!r}: phải đúng dạng k/N, số thập phân không số 0 dẫn đầu")
    k, n = int(m.group(1)), int(m.group(2))
    if not (2 <= n <= _TRAN_MANH and k < n):
        raise ValueError(f"[C-pham-vi] {_BIEN_MANH}={mh!r}: cần 2 ≤ N ≤ {_TRAN_MANH} và 0 ≤ k < N")
    if not ra:
        raise ValueError(f"[C-thieu-ra] {_BIEN_MANH} đặt mà thiếu {_BIEN_MANH_RA}")
    return "manh", (k, n, ra)


def _phan_manh(k, n, ten=None):
    """Tên đột biến của mảnh k/N theo THỨ TỰ `DOT_BIEN`: chỉ số `i % n == k`."""
    return [t for i, t in enumerate(DOT_BIEN if ten is None else ten) if i % n == k]


def _van_tay():
    """{sha256_test, head} của tiến trình ĐANG CHẠY. `head` không đọc được ⇒ `None` (người gọi fail-close)."""
    import hashlib
    import re
    try:
        p = subprocess.run(["git", "-C", str(GOC), "rev-parse", "HEAD"], capture_output=True, text=True, timeout=60)
        head = p.stdout.strip() if p.returncode == 0 else ""
    except (OSError, subprocess.SubprocessError):
        head = ""
    return {"sha256_test": hashlib.sha256(Path(TEP_TEST).read_bytes()).hexdigest(),
            "head": head if re.fullmatch(r"[0-9a-f]{40}|[0-9a-f]{64}", head) else None}


def _ket_thuc_manh(k, n, ra, cac_ten, ket, ly_con, van_tay):
    """(dòng in, số lỗi). Ghi tệp mảnh CHỈ khi mảnh ĐẠT trọn; không đạt thì KHÔNG để lại tệp nào ở `ra`.

    `ket`: {tên: bản ghi} đã qua `_nhan_ket_qua_con`, hoặc `None` kèm `ly_con`. Tách khỏi `main()` để ca tự kiểm gọi
    được bằng bản ghi dựng sẵn — chạy trọn `CA` trong một ca là nhân thời gian mỗi đột biến lên gấp đôi.
    """
    tep = Path(ra)
    if tep.exists() or tep.is_symlink():
        tep.unlink()
    if ket is None:
        return [f"  ĐỎ  mảnh {k}/{n} [M-con]: tiến trình con KHÔNG trả kết quả hợp lệ ({ly_con})"], 1
    if van_tay.get("head") is None:
        return [f"  ĐỎ  mảnh {k}/{n} [M-head]: không đọc được HEAD — KHÔNG ĐO ĐƯỢC, không ghi tệp"], 1
    dong, loi = [], 0
    for ten in cac_ten:
        bg = (ket or {}).get(ten)
        d, l = _ket_luan_ban_ghi(bg, ()) if bg else ([f"  ĐỎ  {ten}: thiếu bản ghi"], 1)
        dong += d
        loi += l
    if loi:
        return dong + [f"  ĐỎ  mảnh {k}/{n} [M-loi]: {loi} lỗi đột biến — không ghi tệp"], loi
    dau = {"phien_ban": _PHIEN_BAN_MANH, "manh": k, "so_manh": n, **van_tay}
    tep.parent.mkdir(parents=True, exist_ok=True)
    tep.write_bytes(("MANH " + json.dumps(dau, ensure_ascii=True, sort_keys=True) + "\n" + "".join(
        "BKCON " + json.dumps(ket[t], ensure_ascii=True) + "\n" for t in cac_ten)).encode("utf-8"))
    return dong + [f"MẢNH {k}/{n}: {len(cac_ten)}/{len(cac_ten)} đột biến bán kính 1 · ghi {tep}"], 0


def _gom_manh(thu_muc, van_tay):
    """(dòng in, số lỗi) — GOM mọi tệp mảnh trong `thu_muc`. KHÔNG tin phán quyết nào của mảnh.

    Mỗi đường hỏng mang MỘT thẻ `[G-…]` riêng, để đột biến gỡ một chốt thì kịch bản của chốt ấy đổi thẻ (bị chốt
    khác bắt) hoặc lọt — cả hai đều làm ca tự kiểm ĐỎ. Chốt không có thẻ riêng là chốt không đo được răng.
    """
    goc = Path(thu_muc)
    muc = sorted(goc.iterdir()) if goc.is_dir() else None
    if muc is None:
        return [f"  ĐỎ  gom [G-thu-muc]: không có thư mục {goc}"], 1
    if not muc:
        return [f"  ĐỎ  gom [G-rong]: {goc} không có mảnh nào"], 1
    if van_tay.get("head") is None:
        return ["  ĐỎ  gom [G-head]: không đọc được HEAD của chính tiến trình gom — KHÔNG ĐO ĐƯỢC"], 1
    dau_cac, than_cac = {}, {}
    for p in muc:
        if p.is_symlink() or not p.is_file():
            return [f"  ĐỎ  gom [G-tep]: {p.name} không phải tệp thường"], 1
        try:
            dong0, _, than = p.read_bytes().decode("utf-8").partition("\n")
            if not dong0.startswith("MANH "):
                raise ValueError("thiếu dòng MANH đầu tệp")
            dau = json.loads(dong0[5:])
            if not isinstance(dau, dict) or set(dau) != _KHOA_DAU_MANH:
                raise ValueError(f"khoá {sorted(dau) if isinstance(dau, dict) else type(dau).__name__}")
            if any(type(dau[x]) is not int for x in ("phien_ban", "manh", "so_manh")):
                raise ValueError("phien_ban/manh/so_manh phải là số nguyên")
        except (OSError, UnicodeDecodeError, ValueError) as ex:
            return [f"  ĐỎ  gom [G-dau]: đầu tệp {p.name} hỏng: {ex}"], 1
        if dau["phien_ban"] != _PHIEN_BAN_MANH:
            return [f"  ĐỎ  gom [G-phien-ban]: {p.name} phien_ban={dau['phien_ban']}"], 1
        if dau["sha256_test"] != van_tay["sha256_test"] or dau["head"] != van_tay["head"]:
            return [f"  ĐỎ  gom [G-van-tay]: {p.name} đo trên mã KHÁC tiến trình gom "
                    f"({dau['head']}/{str(dau['sha256_test'])[:12]} ≠ {van_tay['head']}/{van_tay['sha256_test'][:12]})"], 1
        la = [d for d in than.split("\n") if d and not d.startswith("BKCON ")]
        if la:
            return [f"  ĐỎ  gom [G-dong-la]: {p.name} có dòng ngoài hợp đồng: {la[0][:80]!r}"], 1
        dau_cac[p.name] = dau
        than_cac.setdefault(dau["manh"], []).append((p.name, than))
    cac_n = sorted({d["so_manh"] for d in dau_cac.values()})
    if len(cac_n) != 1:
        return [f"  ĐỎ  gom [G-so-manh]: các mảnh khai số mảnh khác nhau {cac_n}"], 1
    n = cac_n[0]
    if not 2 <= n <= _TRAN_MANH:
        return [f"  ĐỎ  gom [G-n]: số mảnh {n} ngoài 2..{_TRAN_MANH}"], 1
    if sorted(than_cac) != list(range(n)):
        return [f"  ĐỎ  gom [G-tap]: tập mảnh {sorted(than_cac)} ≠ 0..{n - 1}"], 1
    phan = [_phan_manh(k, n) for k in range(n)]
    if sum(map(len, phan)) != len(DOT_BIEN) or set().union(*phan) != set(DOT_BIEN):
        return [f"  ĐỎ  gom [G-phan-hoach]: phân hoạch {n} mảnh không phủ ĐÚNG {len(DOT_BIEN)} đột biến, rời nhau"], 1
    ket = {}
    for k in range(n):
        cua_k = than_cac.get(k, [])
        if len(cua_k) != 1:
            return [f"  ĐỎ  gom [G-dem]: mảnh {k} có {len(cua_k)} tệp: {[t for t, _ in cua_k]}"], 1
        ten_tep, than = cua_k[0]
        nhan, ly_do = _nhan_ket_qua_con(phan[k], 0, than, ())
        if nhan is None:
            return [f"  ĐỎ  gom [G-ban-ghi]: mảnh {k} ({ten_tep}): {ly_do}"], 1
        ket.update(nhan)
    # Dự phòng, KHÔNG có đột biến riêng: với `G-tap` + `G-dem` + `G-ban-ghi` + `G-phan-hoach` đứng trước, không đầu vào đơn nào
    # tới được đây mà thiếu tên. Nó chỉ đổi `KeyError` ở vòng dưới thành một dòng ĐỎ đọc được khi chốt trên bị gỡ.
    if set(ket) != set(DOT_BIEN):
        return [f"  ĐỎ  gom [G-tong]: {len(ket)} bản ghi cho {len(DOT_BIEN)} đột biến"], 1
    dong, loi = [f"GOM MẢNH {n}/{n}", f"BÁN KÍNH ĐỘT BIẾN ({len(DOT_BIEN)} đột biến, mỗi ca đúng một; {n} mảnh):"], 0
    for ten in DOT_BIEN:
        d, l = _ket_luan_ban_ghi(ket[ten], ())
        dong += d
        loi += l
    return dong + [f"SỐ LIỆU GOM: ca={len(CA)} · đột biến={len(DOT_BIEN)} · lỗi đột biến={loi}"], loi


def _main_gop():
    """Điểm vào `--gop <thư mục>` của job `gate-cong-cu-gop`."""
    i = sys.argv.index("--gop")
    if len(sys.argv) != i + 2:
        print(f"  ĐỎ  gom [G-doi-so]: cần đúng một thư mục sau --gop, thấy {sys.argv[i + 1:]!r}")
        return 2
    dong, loi = _gom_manh(sys.argv[i + 1], _van_tay())
    for d in dong:
        print(d)
    return 1 if loi else 0


def _ban_ghi_du_gia(ten):
    """Bản ghi `ok` hợp lệ cho một tên THẬT của `DOT_BIEN`: đích `giet_that`, mọi ca khác `qua` — chỉ cho tự kiểm."""
    dich = DOT_BIEN[ten][5]
    return ["do", ten, dich, {t: ["giet_that" if t == dich else "qua", "giả" if t == dich else None]
                              for t in _cac_ca_da_chay(())}]


_TEN_SL = ("f24_nhan_symlink", "f35_writer_broken_link", "f37_bo_f24", "f37_bo_f35", "f40_false_luon",
           "f41_bo_f40_luon", "f41_f40_khong_ra_ngoai")
_TEN_SL_FALSE = ("f37_dk_luon_dung", "f40_false_khong", "f41_bo_f40_khong", "f41_f40_luon_ra_ngoai")   # F40: đăng ký CHỈ ở nền KHÔNG symlink


def _ghi698(d, n, vt, t1, ten_nen=os.name):
    # #698 M2b T4/T5 (dò x_wr_ra_*, x3_wr*, x4_t4/t5_*, y4_t4_*, x6_t4_ra): bộ ghi THẬT trên 60 đường của `_duong698` cộng khúc
    # tên tệp phủ D698 ∪ N698 (bỏ NUL và "/", khúc 50 ký tự mở bằng "k"); gọi HAI lần (lần hai gặp tệp cũ ⇒ nhánh gỡ chạy),
    # `cwd` riêng từng ô, HOME rỗng. Kỳ vọng ĐỘC LẬP (không gọi bộ ghi): tập mục = `Path(p)` và các cha, ghép `cwd`, giải `..`;
    # dòng in của mỗi lần dựng từ `Path(p)`. Mọi BaseException của bộ ghi là DỮ LIỆU (M6). Chỉ đo POSIX (nợ Windows, Q8).
    # PR #721 (Codex P1): tên ô chứa U+0001–U+001F, chéo ngược và `"*:?|<>` — Windows cấm ⇒ bộ ghi ném, ô lệch. Nên trên
    # `nt` KHÔNG chạy, trả [0, [], 0]; `t52` đòi đúng giá trị ấy trên `nt` và đo chốt bằng `ten_nen="nt"` (không cần Windows).
    if ten_nen == "nt":
        return [0, [], 0]
    nha, cu_cwd, cu_nha, lech = d / "nha698", os.getcwd(), {x: os.environ.get(x) for x in ("HOME", "USERPROFILE")}, []
    nha.mkdir()
    tv = [c for c in sorted(set(_d698() + list(_N698))) if c not in (0, 47)]
    cac_p = _duong698()[:60] + ["k" + "".join(map(chr, tv[i:i + 50])) for i in range(0, len(tv), 50)]
    os.environ.update(HOME=str(nha), USERPROFILE=str(nha))
    try:
        for j, p in enumerate(cac_p):
            o = d / "o698" / str(j)
            o.mkdir(parents=True)
            os.chdir(o)
            try:
                thay = [None, [_ket_thuc_manh(0, n, p, t1, {t1[0]: _ban_ghi_du_gia(t1[0])}, None, vt)[0][-1] for _ in "12"]]
                thay[0] = sorted(str(x.relative_to(o)) for x in o.rglob("*"))
            except BaseException as ex:  # noqa: BLE001
                thay = ["NEM:" + type(ex).__name__]
            q = Path(p)
            mong = [sorted({os.path.relpath(os.path.normpath(o / x), o) for x in (q, *q.parents)} - {"."}),
                    [f"MẢNH 0/{n}: 1/1 đột biến bán kính 1 · ghi {q}"] * 2]
            if thay != mong or any(nha.iterdir()):
                lech.append([j, ascii(p)[:60], str(thay)[:160]])
    finally:
        os.chdir(cu_cwd)
        for x, v in cu_nha.items():
            os.environ.pop(x, None) if v is None else os.environ.update({x: v})
    return [len(cac_p), lech[:10], len(lech)]


def _in_tu_kiem_gom():
    """Cửa tiến trình con cho `t52`: dựng bộ mảnh bằng CHÍNH `_ket_thuc_manh`, làm hỏng từng cách, gom, in `KQ`."""
    n = 3
    # Vân tay CỐ ĐỊNH, không `_van_tay()`: dưới đột biến `GOC` là cây tạm, không phải kho git, nên HEAD đọc được
    # hay không là chuyện của RIG — mọi kịch bản sẽ ĐỎ vì `G-head` và ca "giết" mọi đột biến sai lý do.
    vt = {"sha256_test": "a" * 64, "head": "b" * 40}
    kq = {}
    with tempfile.TemporaryDirectory(prefix="gom668_") as d:
        d = Path(d)

        def dung_bo(ten, sua=None, v=None):
            thu = d / ten
            thu.mkdir()
            for k in range(n):
                cac = _phan_manh(k, n)
                _ket_thuc_manh(k, n, str(thu / f"manh-{k}.txt"), cac, {t: _ban_ghi_du_gia(t) for t in cac}, None,
                               v or vt)
            if sua:
                sua(thu)
            if v is None:
                try:   # ngoại lệ lọt khỏi gom là DỮ LIỆU (ca đích đỏ đúng chốt), không phải con chết (tín dụng giả)
                    dong, loi = _gom_manh(thu, vt)
                    kq[ten] = [loi, dong[0], dong[-1]]
                except Exception as ex:  # noqa: BLE001
                    kq[ten] = [1, f"NEM:{type(ex).__name__}", ""]
            return thu

        def sua_kq(thu, chi=3):
            """F16: bộ ĐÚNG cấu trúc nhưng SAI kết quả đo — sửa SAU bộ ghi (bộ ghi cố ý không ghi mảnh có lỗi), ở ĐẦU
            mảnh 0 (đích sống), GIỮA mảnh 1 (tín dụng giả), CUỐI mảnh 2 (giết thêm một ca ⇒ bán kính 2)."""
            for k, vi_tri, kieu in ((0, 0, "song"), (1, None, "gia"), (2, -1, "rong"))[:chi]:
                p = thu / f"manh-{k}.txt"
                la = p.read_text(encoding="utf-8").split("\n")
                i = 1 + (len(la) - 2) // 2 if vi_tri is None else (1 if vi_tri == 0 else len(la) - 2)
                bg = json.loads(la[i][6:])
                khac = sorted(t for t in bg[3] if t != bg[2])[0]
                if kieu == "song":
                    bg[3][bg[2]] = ["qua", None]
                elif kieu == "gia":
                    bg[3][bg[2]] = ["tin_dung_gia", "giả"]
                else:
                    bg[3][khac] = ["giet_that", "giả"]
                la[i] = "BKCON " + json.dumps(bg)
                p.write_text("\n".join(la), encoding="utf-8", newline="\n")

        def bang_kq(dong, loi):
            return [loi, sum(x.startswith("  ok  ") for x in dong), sum(x.startswith("  ĐỎ  ") for x in dong), dong[-1]]

        def ky_vong(thu, nm):
            """F19/F20 (Codex lượt 7): bảng gom PHẢI bằng NGUYÊN VĂN bảng lắp lại TẠI ĐÂY từ chính các bản ghi trong tệp
            mảnh + `_ket_luan_ban_ghi` — danh tính, thứ tự, dòng chi tiết, tổng lỗi. Dùng CÙNG `_ket_luan_ban_ghi` của
            tiến trình này, nên đột biến vào định dạng của nó (việc của `t29`) đổi cả hai vế như nhau; chỉ lỗi LẮP RÁP
            của gom/CLI làm hai vế lệch."""
            rec = {}
            for tep in sorted(thu.glob("manh-*.txt")):
                for x in tep.read_text(encoding="utf-8").split("\n")[1:]:
                    if x.startswith("BKCON "):
                        bg = json.loads(x[6:])
                        rec[bg[1]] = bg
            dong, loi = [f"GOM MẢNH {nm}/{nm}", f"BÁN KÍNH ĐỘT BIẾN ({len(DOT_BIEN)} đột biến, mỗi ca đúng một; {nm} mảnh):"], 0
            for t in DOT_BIEN:
                d_, l_ = _ket_luan_ban_ghi(rec[t], ())
                dong, loi = dong + d_, loi + l_
            return dong + [f"SỐ LIỆU GOM: ca={len(CA)} · đột biến={len(DOT_BIEN)} · lỗi đột biến={loi}"], loi

        def sua_dong(k, f):
            def _s(thu):
                p = thu / f"manh-{k}.txt"
                p.write_text(f(p.read_text(encoding="utf-8")), encoding="utf-8", newline="\n")
            return _s

        def sua_dau(k, **doi):
            def _f(chu):
                dong0, _, than = chu.partition("\n")
                dau = json.loads(dong0[5:])
                dau.update(doi)
                return "MANH " + json.dumps(dau) + "\n" + than
            return sua_dong(k, _f)

        def chuyen(thu):   # dòng BKCON đầu của mảnh 0 chuyển sang mảnh 1
            a, b = thu / "manh-0.txt", thu / "manh-1.txt"
            la = a.read_text(encoding="utf-8").split("\n")
            b.write_text(b.read_text(encoding="utf-8") + la.pop(1) + "\n", encoding="utf-8", newline="\n")
            a.write_text("\n".join(la), encoding="utf-8", newline="\n")

        dung_bo("dung")
        dung_bo("thieu", lambda t: (t / "manh-2.txt").unlink())
        dung_bo("thua", lambda t: shutil.copy(t / "manh-0.txt", t / "manh-0b.txt"))
        dung_bo("trung", lambda t: shutil.copy(t / "manh-0.txt", t / "manh-2.txt"))
        dung_bo("chuyen", chuyen)
        dung_bo("xoa", sua_dong(1, lambda c: "\n".join(c.split("\n")[:1] + c.split("\n")[2:])))
        dung_bo("sha", sua_dau(0, sha256_test="0" * 64))
        dung_bo("head", sua_dau(2, head="0" * 40))
        dung_bo("so_manh", sua_dau(1, so_manh=4))
        dung_bo("phien_ban", sua_dau(1, phien_ban=2))
        dung_bo("kieu_bool", sua_dau(0, manh=False))
        # F24 (Codex lượt 8): kiểu từng trường riêng — gỡ chốt kiểu của MỘT trường phải có kịch bản của CHÍNH trường ấy.
        dung_bo("kieu_phien_ban_bool", sua_dau(1, phien_ban=True))
        dung_bo("kieu_phien_ban_so_thuc", sua_dau(1, phien_ban=1.0))
        dung_bo("kieu_so_manh_so_thuc", sua_dau(2, so_manh=3.0))
        dung_bo("khoa_thua", sua_dau(0, them=1))
        dung_bo("dau_hong", sua_dong(0, lambda c: "MANH {" + c.partition("\n")[1] + c.partition("\n")[2]))
        dung_bo("dong_la", sua_dong(0, lambda c: c + "rac\n"))
        dung_bo("ban_ghi", sua_dong(2, lambda c: c.replace('["giet_that", "gi', '["xanh", "gi', 1)))
        dung_bo("tep_la", lambda t: (t / "thu_muc_con").mkdir())

        def symlink(thu):   # F24: symlink tới một tệp mảnh HỢP LỆ — chỉ chốt `is_symlink` bắt được, `is_file` thì không
            dich = d / f"ngoai-{thu.name}.txt"
            (thu / "manh-0.txt").replace(dich)
            os.symlink(dich, thu / "manh-0.txt")
        if _CO_SYMLINK:
            dung_bo("symlink_tep", symlink)
        for ten, sua in (("kq_nhieu", sua_kq), ("kq_mot", lambda t: sua_kq(t, chi=1))):
            thu = dung_bo(ten + "_goc", sua, vt)
            dong, loi = _gom_manh(thu, vt)
            kv, kv_loi = ky_vong(thu, n)
            kq[ten] = bang_kq(dong, loi) + [dong == kv, loi == kv_loi]
        kq["N"] = len(DOT_BIEN)
        mot = d / "n_1"
        mot.mkdir()
        _ket_thuc_manh(0, 1, str(mot / "manh-0.txt"), list(DOT_BIEN), {t: _ban_ghi_du_gia(t) for t in DOT_BIEN},
                       None, vt)
        dong, loi = _gom_manh(mot, vt)
        kq["n_1"] = [loi, dong[0], dong[-1]]
        # Phân hoạch CHỒNG LẤN (mảnh k lấy mọi i % n <= k): mỗi mảnh tự nhất quán, hợp các mảnh vẫn đủ tên — chỉ
        # phép đếm tổng của `G-phan-hoach` bắt được. Tráo `_phan_manh` ở CẢ HAI phía, như một đột biến vào nó.
        g, goc_pm = globals(), _phan_manh
        g["_phan_manh"] = lambda k, n, ten=None: [t for i, t in enumerate(DOT_BIEN if ten is None else ten)
                                                   if i % n <= k]
        try:
            dung_bo("phan_chong")
        finally:
            g["_phan_manh"] = goc_pm
        # F35 (Codex lượt 14): biên N (2/16 XANH + bảng nguyên văn; 17 và 0-khai-đồng-loạt ⇒ G-n), tiền tố sai mà JSON
        # hợp lệ, kiểu SAI trên TỪNG trường đầu tệp, lỗi ĐỌC tệp — mỗi thứ một chốt riêng của `_gom_manh`.
        for nm, khai in ((2, None), (16, None), (17, None), (3, 0)):
            thu = d / f"bien_{nm}_{khai}"
            thu.mkdir()
            for k in range(nm):
                cac = _phan_manh(k, nm)
                _ket_thuc_manh(k, nm, str(thu / f"manh-{k}.txt"), cac, {t: _ban_ghi_du_gia(t) for t in cac}, None, vt)
                if khai is not None:
                    sua_dau(k, so_manh=khai)(thu)
            dong, loi = _gom_manh(thu, vt)
            kq[thu.name] = [loi, dong[0], dong[-1], dong == ky_vong(thu, nm)[0]]
        dung_bo("tien_to", sua_dong(0, lambda c: "ABCDE" + c[5:]))
        for tr in ("phien_ban", "manh", "so_manh"):
            for j, gt in enumerate((True, "1", None, [], {}, "so_thuc")):
                def _kieu(chu, tr=tr, gt=gt):
                    dau = json.loads(chu.partition("\n")[0][5:])
                    dau[tr] = float(dau[tr]) if gt == "so_thuc" else gt
                    return "MANH " + json.dumps(dau) + "\n" + chu.partition("\n")[2]
                dung_bo(f"kieu_{tr}_{j}", sua_dong(0, _kieu))
        cu_rb = Path.read_bytes
        Path.read_bytes = lambda self: (_ for _ in ()).throw(OSError("giả đọc hỏng")) if (
            self.name == "manh-1.txt" and self.parent.name == "doc_loi") else cu_rb(self)
        try:
            dung_bo("doc_loi")
        finally:
            Path.read_bytes = cu_rb
        # F35: danh TÍNH phân hoạch — chỉ số từng nhóm theo nguồn của CHÍNH tiến trình này; cha so với `nguon[k::N]`.
        nguon = list(DOT_BIEN)
        vi = {t: i for i, t in enumerate(nguon)}
        kq["phan_hoach"] = [len(nguon), {f"{k}/{m}": [vi[t] for t in _phan_manh(k, m)] for m in range(2, 17)
                                         for k in range(m)}]
        rong = d / "rong"
        rong.mkdir()
        kq["rong"] = [_gom_manh(rong, vt)[1], _gom_manh(rong, vt)[0][0], ""]
        kq["khong_co"] = [_gom_manh(d / "khong_co", vt)[1], _gom_manh(d / "khong_co", vt)[0][0], ""]
        kq["head_gom_none"] = [_gom_manh(d / "dung", {**vt, "head": None})[1],
                               _gom_manh(d / "dung", {**vt, "head": None})[0][0], ""]
        # F8 (Codex lượt 4): điểm vào CLI `--gop` THẬT (`_main_gop`) phải GỌI gom, lấy vân tay từ `_van_tay`, và TRUYỀN
        # phán quyết thành mã thoát — `t52` trước đây chỉ gọi `_gom_manh` trực tiếp.
        import contextlib
        import io
        g, cu_vt, argv, goi_vt, goc_cu = globals(), _van_tay, sys.argv, [], (GOC, TEP_TEST)
        g["_van_tay"] = lambda: goi_vt.append(1) or dict(vt)
        try:
            for ten, doi in (("cli_dung", [str(d / "dung")]), ("cli_thieu", [str(d / "thieu")]),
                             ("cli_doi_so", [str(d / "dung"), "thua"])):
                goi_vt.clear()
                sys.argv, buf = ["cong_cu_test.py", "--gop", *doi], io.StringIO()
                with contextlib.redirect_stdout(buf):
                    rc = _main_gop()
                kq[ten] = [rc, (buf.getvalue().splitlines() or [""])[0], len(goi_vt)]
        finally:
            g["_van_tay"], sys.argv = cu_vt, argv
        # F13 (Codex lượt 5): cả dây DISPATCHER trong `__main__` — gọi CHÍNH tệp này làm CLI (đúng thứ workflow chạy).
        # Đường dương cần vân tay thật khớp, không dựng được dưới đột biến (cây tạm không phải git), nên đo hai đường âm.
        # F25: giá trị của `--gop` trùng tên một cửa tự kiểm vẫn là THƯ MỤC; cửa đứng SAU `--gop` là đối số thừa; đối
        # số lạ ⇒ rc=2 (env chế độ hỏng để nếu chốt ấy bị gỡ thì `main` dừng ngay ở rc=2 với thông điệp KHÁC).
        for ten, doi in (("cli_tt_rong", ["--gop", str(rong)]), ("cli_tt_doi_so", ["--gop"]),
                         ("cli_tt_ten_cua", ["--gop", "--tu-kiem-che-do"]),
                         ("cli_tt_cua_sau", ["--gop", str(rong), "--tu-kiem-che-do"]), ("cli_tt_la", ["--khong-co"])):
            p = subprocess.run([sys.executable, str(TEP_TEST), *doi], capture_output=True, text=True,
                               timeout=120, cwd=str(GOC), env={**os.environ, _BIEN_BAN_KINH: "hong"})
            kq[ten] = [p.returncode, (p.stdout.splitlines() or [""])[0], 0]
        # F17 (Codex lượt 6): CLI THẬT trên đường DƯƠNG và trên bộ ≥ 2 lỗi. Vân tay phải khớp đúng tiến trình CLI được
        # đo, nên dựng một kho git TẠM từ CHÍNH tệp đang chạy (kể cả khi nó là bản đột biến) và lấy vân tay tại đó.
        kho = d / "kho"
        (kho / "ops").mkdir(parents=True)
        # CHỈ đúng thứ `--gop` import (F22, Codex lượt 7, P1): cây của đột biến `TEP_TEST` cũ chỉ mang hai tệp kèm này;
        # đòi thêm `cong_cu.py` làm `t52` chết VÔ CAN (tín dụng giả) dưới 5 đột biến cũ ⇒ cổng bán kính hồi quy.
        for ten in ("cong_cu_test.py", "lease_publish_test.py", "bash_nen.py"):
            shutil.copy2(Path(TEP_TEST).parent / ten, kho / "ops" / ten)
        git = lambda *a: subprocess.run(["git", "-C", str(kho), "-c", "user.email=t@t", "-c", "user.name=t", "-c",
                                         "commit.gpgsign=false", *a], capture_output=True, text=True, timeout=60)
        git("init", "-q"), git("add", "-A"), git("commit", "-q", "-m", "kho tạm #668")
        # Vân tay lấy bằng CHÍNH `_van_tay` trỏ vào kho tạm — đúng hàm CLI sẽ gọi. Tự băm ở đây thì một đột biến vào
        # NGUỒN vân tay (việc của `t53`) cũng giết `t52` ⇒ bán kính 2 (đo được: `f9_*` lúc đầu 2/56).
        g["GOC"], g["TEP_TEST"] = kho, kho / "ops" / "cong_cu_test.py"
        try:
            vt_kho = _van_tay()
        finally:
            g["GOC"], g["TEP_TEST"] = goc_cu
        dung(vt_kho["head"], f"giàn giáo kho git tạm không có HEAD: {git('log', '-1').stderr[-300:]}")
        for ten, sua in (("cli_git_dung", None), ("cli_git_nhieu", sua_kq)):
            thu = dung_bo(ten, sua, vt_kho)
            p = subprocess.run([sys.executable, str(kho / "ops" / "cong_cu_test.py"), "--gop", str(thu)],
                               capture_output=True, text=True, timeout=180, cwd=str(kho))
            dong = p.stdout.splitlines()
            kv, kv_loi = ky_vong(thu, n)
            kq[ten] = ([p.returncode] + (bang_kq(dong, None)[1:] if dong else [0, 0, ""]) + [(dong or [""])[0]]
                       + [dong == kv, p.returncode == (1 if kv_loi else 0)])
        # Phía GHI: mảnh không đạt KHÔNG được để lại tệp — kể cả tệp cũ cùng tên.
        ghi = d / "ghi"
        ghi.mkdir()
        cac = _phan_manh(0, n)
        hong = {t: _ban_ghi_du_gia(t) for t in cac}
        hong[cac[0]] = ["loi", cac[0], "giả hỏng"]
        # F21 (Codex lượt 7): bản ghi loại `do` ĐÚNG cấu trúc SAI kết quả (đích sống) ở CUỐI, và ở cả ĐẦU lẫn CUỐI.
        sai_ket = lambda *vi: {t: (["do", t, _ban_ghi_du_gia(t)[2], {**_ban_ghi_du_gia(t)[3], _ban_ghi_du_gia(t)[2]:
                                                                ["qua", None]}] if i in vi else _ban_ghi_du_gia(t))
                               for i, t in enumerate(cac)}
        for ten, ket, ly, v in (("ghi_loi", hong, None, vt), ("ghi_con", None, "giả", vt),
                                ("ghi_head", {t: _ban_ghi_du_gia(t) for t in cac}, None, {**vt, "head": None}),
                                ("ghi_do_cuoi", sai_ket(len(cac) - 1), None, vt),
                                ("ghi_do_hai", sai_ket(0, len(cac) - 1), None, vt)):
            p = ghi / f"{ten}.txt"
            p.write_text("cũ\n", encoding="utf-8")
            dong, loi = _ket_thuc_manh(0, n, str(p), cac, ket, ly, v)
            kv = [x for t in cac for x in _ket_luan_ban_ghi(ket[t], ())[0]] if ket else []
            kq[ten] = [loi, dong[-1], "con-tep" if p.exists() else "khong-tep", dong[:-1] == kv if ket else None]
        # F35: bộ ghi — đường cha NHIỀU tầng chưa có + tên có khoảng trắng cuối (ghi đúng NGUYÊN đường); symlink GÃY
        # cũ ở nhánh không đạt phải bị gỡ.
        p = ghi / "a" / "b c" / "manh-0.txt "
        try:
            _ket_thuc_manh(0, n, str(p), cac, {t: _ban_ghi_du_gia(t) for t in cac}, None, vt)
            kq["ghi_duong"] = [p.is_file(), p.is_file() and p.read_text(encoding="utf-8").startswith("MANH ")]
        except Exception as ex:  # noqa: BLE001
            kq["ghi_duong"] = [f"NEM:{type(ex).__name__}"]
        kq["ghi698"] = _ghi698(d, n, vt, cac[:1])
        if _CO_SYMLINK:
            gay = ghi / "gay.txt"
            os.symlink(ghi / "khong-co", gay)
            _ket_thuc_manh(0, n, str(gay), cac, None, "giả", vt)
            kq["ghi_gay"] = [gay.exists() or gay.is_symlink()]
    # Chủ kho sau review lượt 17: MỘT ô — năng lực symlink ↔ tên đột biến symlink đã đăng ký (không nạp lại, không mô phỏng).
    kq["nang_luc"] = [_CO_SYMLINK, sorted(_TEN_NANG_LUC)]
    print("KQ " + json.dumps(kq, ensure_ascii=True))


def _luoi_noi_main():
    rows = [(f"noi-k{k}-n{n}", "manh", k, n, "x", 3) for n in range(2, 17) for k in range(n)]
    rows += [(f"noi-{mode}-w{w}", mode, 9, 16, "x", w) for mode in ("du", "manh") for w in range(1, 17)]
    rows += [(f"noi-path-{i}", "manh", 9, 16, path, 3) for i, path in enumerate(
        ("x", " space ", "Mixed.TXT", "dir/Sub Dir/Mảnh.TXT", "  ", "d con/manh 3.txt"))]
    # F44: nhánh NỀN ĐỎ `[M-nen]` của main cũng nhận NGUYÊN k/N/đường ra (k>=8, N không lũy thừa 2, đường khoảng trắng/hoa).
    rows += [(f"noi-nen-{i}", "nen", k, n, path, 3) for i, (k, n, path) in enumerate(
        ((9, 16, " space "), (15, 16, "Mixed.TXT"), (4, 5, "dir/Sub Dir/Mảnh.TXT"), (10, 11, "x"), (0, 2, "  ")))]
    rows += [("noi-nen-do", "nen_do", 10, 11, " Đỏ Sub/Mixed.TXT ", 3)]
    # #698 M2b (dò x_main_ra_*, x3_main_ra_*, x3_m3a/m3b_ra_*, x4/y4/x6_t2/t3*): 61 đường × `manh` (T2+T3b) và `nen` (T2+T3a).
    return rows + [(f"noi698-{md}-{i}", md, 9, 16, p, 3) for md in ("manh", "nen") for i, p in enumerate(_duong698())]


def _in_tu_kiem_main():
    """Cửa tiến trình con cho `t54` (#668 F2→F5→F6→F7): chạy CHÍNH `main()` trên giàn giáo, in NHẬT KÝ mọi lời gọi.

    F7 (Codex lượt 4, lần thứ TƯ cùng lớp): vá theo từng đường reviewer chỉ ra thì lượt sau lại có đường khác. Nên
    ở đây KHÔNG chọn đường: MỌI thứ `main` gọi đều bị thay bằng bộ ghi sự kiện kèm tham số (tiền kiểm batch/alias,
    từng ca, phóng con, bộ nhận thật, bộ ghi mảnh, cổng cây thật, ba tự kiểm, báo cáo nền, bán kính đủ), và MỖI nguồn
    lỗi có một kịch bản riêng lẻ — nhưng #698 (F50) đo được: một kịch bản mỗi nguồn KHÔNG phủ LỰC LƯỢNG; nay `bo_qua`/`hong`/
    tiền kiểm theo TRỤC trọn + TÍCH BIÊN (`_luoi_m3`), không trọn tích. `t54` so NGUYÊN nhật ký + mã thoát. Kỳ vọng tên (`list(DOT_BIEN)`, `_phan_manh`) in
    từ CHÍNH tiến trình này: ca đo DÂY NỐI, tính đúng của phân hoạch là việc của `t52`.
    """
    import contextlib
    import hashlib
    import io
    g, ten_ca, kb, log = globals(), [fn.__name__ for fn in CA], {}, []
    bam = lambda x: hashlib.sha256(json.dumps(x, sort_keys=True).encode()).hexdigest()
    vt_gia, phat, phat_nho = {"sha256_test": "a" * 64, "head": "b" * 40}, {}, {}

    def ca_gia(t):
        def f():
            log.append(f"ca:{t}")   # F12: TÊN từng ca, không nén — ca lặp / bỏ / đảo đều lộ ra
            for khoa, loai in (("ca_do", AssertionError), ("ca_loi", RuntimeError), ("ca_bq", BoQuaMoiTruong)):
                if t in kb.get(khoa, ()):   # F15: TẬP tên — nhiều ca đỏ cùng lúc
                    raise loai(f"ca giả {t}")   # lý do RIÊNG từng ca: "in lý do của ca đầu cho mọi ca" phải lộ
        f.__name__ = t
        return f

    def phong(ten, do_o_nen, so):
        log.append(f"phong:{ten == phat['mong']}:{list(do_o_nen)}:{so}")
        # #698 M8: đầu ra giả của con và kỳ vọng `gt`/`ly` chỉ phụ thuộc (tên, kb["con"]) ⇒ dựng MỘT lần mỗi khoá trong tiến trình.
        khoa = (tuple(ten), kb.get("con"))
        if khoa not in phat_nho:
            phat_nho[khoa] = phong_dung(ten)
        phat["gt"], kq_con, phat["ly"] = phat_nho[khoa]
        return [(list(n), rc, ra) for n, rc, ra in kq_con]   # bản sao mới mỗi lời gọi, như bản dựng lại

    def phong_dung(ten):   # thân cũ của `phong`, `phat` cục bộ
        phat = {}
        nhom, phat["gt"] = [ten[0::2], ten[1::2]], bam({t: _ban_ghi_du_gia(t) for t in ten})
        # "rc": nhóm 0 rc=3 mà stdout ĐỦ; "rong": nhóm 0 rc=0 mà stdout rỗng; "hai": nhóm 0 rc=3 VÀ nhóm 1 rc=5
        # (F15: rc khác nhau để biết `main` giữ lý do của nhóm hỏng ĐẦU TIÊN).
        rc_nhom = {"rc": (3, 0), "hai": (3, 5), "sau": (0, 5)}.get(kb.get("con"), (0, 0))   # "sau": nhóm ĐẦU lành
        kq_con = [(n, rc_nhom[i], "" if kb.get("con") == "rong" and i == 0 else
                   "".join("BKCON " + json.dumps(_ban_ghi_du_gia(t)) + "\n" for t in n)) for i, n in enumerate(nhom)]
        # F23 (Codex lượt 8): lý do `main` trao bộ ghi phải là NGUYÊN VĂN lý do của nhóm hỏng ĐẦU TIÊN (từ chính
        # `_nhan_ket_qua_con`) + rc + đuôi đầu ra — so nguyên chuỗi, không nén thành rc.
        phat["ly"] = next((f"{ly}; rc={rc}, đuôi đầu ra: {ra[-300:]!r}" for n, rc, ra in kq_con
                           for _, ly in [_nhan_ket_qua_con(n, rc, ra, ())] if ly), None)
        return phat["gt"], kq_con, phat["ly"]

    def ghi(k, n, ra, ten, ket, ly, vt):
        gt = "None" if ket is None else ("dung" if bam(ket) == phat.get("gt") else "sai")
        rc_cuoi = re.findall(r"rc=(\d+)", str(ly))
        rc_ly = ("none" if ly is None else "nen" if ly == "nền đỏ hoặc tiền kiểm bị bỏ qua — không đo" else
                 "dung-rc" + rc_cuoi[-1] if ly == phat.get("ly") and rc_cuoi else "sai")
        log.append(f"ghi:{k}/{n}:{ra}:{ten == phat['mong']}:{gt}:{rc_ly}:{vt == vt_gia}")
        # F15/F18: số lỗi theo kịch bản — ĐÚNG 1 và ≥ 2 đều có (`if loi` → `== 1` và → `> 1` cùng phải chết); HAI dòng.
        return ["  DONG-BO-GHI-668", "  DONG-BO-GHI-668-B"], (2 if ket is None else kb.get("ghi_do", 0))

    def tu_kiem(ten, loi):
        return lambda *a: log.append(f"{ten}:{list(a[0]) if a else ''}") or kb.get(loi, 0)

    def du(ten, do_o_nen, so):
        # F12: HAI kết quả, lỗi đặt ở đầu hoặc cuối — một kết quả thì "gán đè" và "chỉ đọc đầu" không phân biệt được.
        log.append(f"du:{ten == list(DOT_BIEN)}:{list(do_o_nen)}:{so}")
        return [(["  DONG-BK1-668", "  DONG-BK1-668-B"], kb.get("bk1", 0)),
                (["  DONG-BK2-668", "  DONG-BK2-668-B"], kb.get("bk2", 0))]

    g["_chay_tien_kiem"] = lambda fn: log.append(f"tk:{fn.__name__}") or (
        (fn.__name__, f"bỏ qua có chủ đích {fn.__name__}") if fn.__name__ in kb.get("tk", ()) else None)
    g["_cong_tren_cay_that"] = lambda goc, bo_quet=None: log.append(f"cong:{goc == GOC}:{bo_quet}") or (
        kb.get("cong_do", 0), ["  DONG-CONG-668", "  DONG-CONG-668-B"])
    g["_tu_kiem_phan_hang"], g["_tu_kiem_gian_giao"] = tu_kiem("phan_hang", "ph_do"), tu_kiem("gian_giao", "gg_do")
    g["_tu_kiem_song_song"] = tu_kiem("song_song", "ss_do")
    g["_bao_cao_nen_do"] = lambda d: log.append(f"nen:{list(d)}") or (
        (["  DONG-NEN-668", "  DONG-NEN-668-B"], 1) if d else ([], 0))
    g["_ban_kinh_moi_dot_bien"], g["_phong_con"], g["_ket_thuc_manh"] = du, phong, ghi
    g["_van_tay"] = lambda: dict(vt_gia)
    # F27 (Codex lượt 10): số worker là DỮ LIỆU của kịch bản — 3 mặc định, 1 ở hai kịch bản `_w1`. Kỳ vọng lấy từ CHÍNH
    # `_so_tien_trinh_ban_kinh` dưới cùng env (đột biến vào hàm ấy là việc của ca khác), nên hằng trong `main` lộ ra.
    tt = "CONG_CU_TEST_TIEN_TRINH"
    os.environ[tt] = "1"
    so1 = _so_tien_trinh_ban_kinh()
    os.environ[tt] = "3"
    kq = {"mong_du": len(DOT_BIEN), "mong_manh": {m: len(_phan_manh(*m)) for m in ((k, n) for n in range(2, 17) for k in range(n))},
          "ten_ca": ten_ca, "so": _so_tien_trinh_ban_kinh(), "so1": so1}
    kq["mong_manh"] = {f"{k}/{n}": v for (k, n), v in kq["mong_manh"].items()}
    import re
    # F27: đường ra KHÁC nhau giữa các kịch bản (có thư mục con + khoảng trắng) — một hằng `ra` trong `main` phải lộ.
    manh, gate = {_BIEN_MANH: "3/8", _BIEN_MANH_RA: "d con/manh 3.txt"}, {_BIEN_BAN_KINH: "manh"}
    tb, ta, c0, c1, cn = "batch_behavior_test", "python_alias_behavior_test", ten_ca[0], ten_ca[1], ten_ca[-1]
    kich_ban = {
        "du": ({}, {}), "gate": (gate, {}), "manh": (manh, {}), "cau_hinh_sai": ({_BIEN_BAN_KINH: "x"}, {}),
        "du_tk_batch": ({}, {"tk": {tb}}), "du_tk_alias": ({}, {"tk": {ta}}), "du_tk_ca_hai": ({}, {"tk": {tb, ta}}),
        "manh_tk_batch": (manh, {"tk": {tb}}), "manh_tk_alias": (manh, {"tk": {ta}}),
        "manh_ca_do": (manh, {"ca_do": {cn}}), "manh_ca_loi": (manh, {"ca_loi": {c0}}),
        "manh_ca_bq": (manh, {"ca_bq": {c1}}), "du_ca_do": ({}, {"ca_do": {cn}}), "du_hai_ca_do": ({}, {"ca_do": {c1, cn}}),
        "du_hai_ca_bq": ({}, {"ca_bq": {c1, ten_ca[2]}}),
        "gate_ca_loi": (gate, {"ca_loi": {c0}}), "du_ca_bq": ({}, {"ca_bq": {c1}}),
        "con_rc": (manh, {"con": "rc"}), "con_rong": (manh, {"con": "rong"}), "con_hai": (manh, {"con": "hai"}),
        "con_sau": (manh, {"con": "sau"}),
        "ghi_do": (manh, {"ghi_do": 2}), "ghi_do_1": (manh, {"ghi_do": 1}),
        "manh_516": ({_BIEN_MANH: "5/16", _BIEN_MANH_RA: "x"}, {}), "manh_12": ({_BIEN_MANH: "1/2", _BIEN_MANH_RA: "x"}, {}),
        "du_cong_do": ({}, {"cong_do": 1}), "gate_cong_do": (gate, {"cong_do": 1}),
        "gate_ph_do": (gate, {"ph_do": 2}), "gate_gg_do": (gate, {"gg_do": 2}), "gate_ss_do": (gate, {"ss_do": 2}),
        "gate_ph_do_1": (gate, {"ph_do": 1}),
        "gate_nhieu_nguon": (gate, {"ph_do": 1, "gg_do": 2, "ss_do": 1, "cong_do": 1, "ca_do": {cn}}),
        "du_bk_do": ({}, {"bk1": 2}), "du_bk_do_cuoi": ({}, {"bk2": 2}), "du_bk_hai": ({}, {"bk1": 2, "bk2": 2}),
        "du_bk_do_1": ({}, {"bk1": 1}),
        # F27: k=0 (giá trị FALSY) · worker=1 ở cả hai nhánh · lỗi tự kiểm ở nhánh ĐỦ, mỗi nguồn một lũy thừa 2 (nền=1)
        # để bỏ/gán đè BẤT KỲ nguồn nào cũng ra tổng khác.
        "manh_0": ({_BIEN_MANH: "0/8", _BIEN_MANH_RA: "x"}, {}), "manh_w1": ({**manh, tt: "1"}, {}),
        "du_w1": ({tt: "1"}, {}), "du_nhieu_nguon": ({}, {"ph_do": 2, "gg_do": 4, "ss_do": 16, "bk1": 32, "ca_do": {cn}}),
    }
    noi = {name: (mode, k, n, path, workers) for name, mode, k, n, path, workers in _luoi_noi_main()}
    for name, (mode, k, n, path, workers) in noi.items():
        env = {_BIEN_MANH: f"{k}/{n}", _BIEN_MANH_RA: path} if mode != "du" else {}
        kich_ban[name] = ({**env, tt: str(workers)}, {"tk": {tb}} if mode == "nen" else {"ca_do": {cn}} if mode == "nen_do" else {})
    for h, b, t in _luoi_m3(len(ten_ca)):   # #698 M3: hong = h ca ĐẦU, bo_qua = b ca KẾ TIẾP (rời nhau), tiền kiểm bỏ = t
        kich_ban[f"m3698-{h}-{b}-{'+'.join(t)}"] = (manh, {"ca_do": set(ten_ca[:h]), "ca_bq": set(ten_ca[h:h + b]), "tk": set(t)})
    for ten, (env, dat) in kich_ban.items():
        kb.clear()
        kb.update(dat)
        log.clear()
        CA[:] = [ca_gia(t) for t in ten_ca]
        phat.pop("ly", None)
        km = env.get(_BIEN_MANH, "3/8").split("/")
        phat["mong"] = _phan_manh(int(km[0]), int(km[1]))
        for bien in (_BIEN_BAN_KINH, _BIEN_MANH, _BIEN_MANH_RA):
            os.environ.pop(bien, None)
        os.environ.update({tt: "3", **env})
        buf = io.StringIO()
        cu_doc, cu_so = g["_doc_che_do"], g["_so_tien_trinh_ban_kinh"]
        if ten in noi:
            mode, ki, ni, path, workers = noi[ten]
            g["_doc_che_do"] = lambda env: ("du", None) if mode == "du" else ("manh", (ki, ni, path))
            g["_so_tien_trinh_ban_kinh"] = lambda: workers
        try:
            with contextlib.redirect_stdout(buf):
                rc = main()
        except BaseException as ex:  # noqa: BLE001 — #698 M6: ngoại lệ của `main` là DỮ LIỆU (mã thoát `NEM:`), không giết con
            rc = "NEM:" + type(ex).__name__
        finally:
            g["_doc_che_do"], g["_so_tien_trinh_ban_kinh"] = cu_doc, cu_so
        # F12/F15: stdout cũng là đầu ra — MỌI dòng mang nghĩa hợp đồng (chẩn đoán, đếm, giao mảnh, bảng, SỐ LIỆU),
        # nguyên văn và đúng thứ tự; dòng trống bỏ.
        kq[ten] = [rc, list(log), [x for x in buf.getvalue().splitlines() if x.strip()]]
    print("KQ " + json.dumps(kq, ensure_ascii=True))


def _luoi_che_do():
    """#668 F33 (Codex lượt 14): miền ĐẦU VÀO của `_doc_che_do` — dữ liệu cố định; kỳ vọng do `_mong_che_do` tính ĐỘC LẬP."""
    B, M, R = _BIEN_BAN_KINH, _BIEN_MANH, _BIEN_MANH_RA
    o = [{x: v for x, v in ((B, bk), (M, mh), (R, ra)) if v is not None}
         for bk in (None, "", "manh") for mh in (None, "", "3/8") for ra in (None, "", "x")]
    so = [f"{k}/{n}" for n in range(2, 17) for k in range(n)] + [f"{k}/{n}" for n in (0, 1, 17, 99) for k in (0, 1)]
    so += ["16/16", "17/16", "00/8", "0/08", "01/8", "1/08", "100/8", "1/100", "0/016", "+1/8", "-1/8", "1/+8", "1/-8",
           "1:8", "1\\8", "1 /8", "1/ 8", "1//8", "1/8/", "/8", "1/", "1/8x"]
    so += ["12/16"[:i] + chr(0x660 + int("12/16"[i])) + "12/16"[i + 1:] for i in (0, 1, 3, 4)]
    return (o + [{M: x, R: "x"} for x in so] + [{M: "3/8", R: r} for r in ("y z", " y ", "  ", "a/b c/manh 3.txt")]
            + [{M: "3/8", R: r} for r in _RA698])   # #698 M2: 12 ô `ra` có cấu trúc (dò `s_ra_*`, `e49_ra_*`)


# #698 M2 (dò `s_ra_*`, `e49_ra_*`): mỗi phép — normpath, expanduser, expandvars, bỏ `./` đầu, bỏ `/` cuối, gộp `//`, chéo ngược,
# lower/casefold, NFD, NFC, Zs cuối — có ô RIÊNG làm đổi giá trị. Ký tự ngoài ASCII dựng bằng chr() (A1-iv của spec wp698).
_RA698 = ("a/./b//c", "a/../b", "~/x", "$HOME/x", "./x", "x/", "a//b", "a" + chr(92) + "b", "X/Y.TXT",
          "M" + chr(0x1EA3) + "nh", "Ma" + chr(0x309) + "nh", "x" + chr(0xA0))
# #698 M1: đại diện R698 (Cf, TAB, Zs, Mn, Cc, NFKC khác chính nó) và N698 (một điểm mã mỗi nhóm Lo/Co/Cn bị loại khỏi D698).
_R698 = (0x200B, 0xFEFF, 0x200E, 0xAD, 0x61C, 0xE0001, 0x9, 0xA0, 0x3000, 0x301, 0xB, 0xB2, 0xFF10)
_N698 = (0x4E00, 0xE000, 0x378)


def _d698(_nho=[]):
    """#698 M1: `D698` DẪN XUẤT lúc chạy (luật CHO PHÉP thử, không liệt kê): mọi điểm mã trừ surrogate, không thuộc Lo/Co/Cn
    HOẶC có NFKC khác chính nó. Cha (`t53`) đếm lại bằng biểu thức RIÊNG, không gọi hàm này. Nhớ đệm trong tiến trình (A4-g)."""
    import unicodedata as u
    _nho[:] = _nho or [[c for c in range(0x110000) if not 0xD800 <= c <= 0xDFFF and (
        u.category(chr(c)) not in ("Lo", "Co", "Cn") or not u.is_normalized("NFKC", chr(c)))]]
    return list(_nho[0])


def _duong698():
    """#698 M2b: đường ra ở MỌI tầng sau `_doc_che_do` — (i) 12 đường `_RA698`; (ii) mỗi điểm mã R698 ∪ N698 ở đầu, giữa, cuối
    của `a/b` (48); (iii) MỘT đường chứa mọi điểm mã D698 ∪ N698 tăng dần, trừ U+0000 (biến môi trường không chứa được NUL)."""
    cs = [chr(c) for c in _R698 + _N698]
    return (list(_RA698) + [x for c in cs for x in (c + "a/b", "a" + c + "/b", "a/b" + c)]
            + ["".join(chr(c) for c in sorted(set(_d698() + list(_N698))) if c)])


def _luoi_m3(n):
    """#698 M3 (dò `s2_*`, `s3_*`, `x_f50_*`, `e50_*`, `x47_*`): (hong, bo_qua, tiền kiểm bỏ) của nhánh mảnh — TRỤC trọn
    (bo_qua 0…n, hong 1…n, tiền kiểm cả hai) cộng TÍCH BIÊN (h, b ∈ {0, 1, 2, n−1, n}, h + b ≤ n, ≥ 2 toạ độ khác 0).
    KHÔNG phải quét trọn miền: tích đầy đủ 6612 kịch bản (spec wp698 §5 M3, §7); hằng giữa của `bo_qua` là giới hạn đã khai."""
    tk, bien = ("batch_behavior_test", "python_alias_behavior_test"), (0, 1, 2, n - 1, n)
    return ([(0, b, ()) for b in range(n + 1)] + [(h, 0, ()) for h in range(1, n + 1)] + [(0, 0, tk)]
            + [(h, b, t) for h in bien for b in bien for t in ((), tk[:1], tk[1:], tk)
               if h + b <= n and (h > 0) + (b > 0) + (t != ()) >= 2])


def _mong_che_do(env):
    """Oracle của `t53` — viết lại bằng so sánh ký tự, KHÔNG dùng regex/`int` tự do của `_doc_che_do`."""
    bk, mh, ra = env.get(_BIEN_BAN_KINH), env.get(_BIEN_MANH), env.get(_BIEN_MANH_RA)
    if mh is None:   # oracle, KHÔNG phải neo f29
        return (["loi", "[C-ra-le]"] if ra is not None else ["du", None] if bk is None else
                ["gate", None] if bk == "manh" else ["loi", "[C-ban-kinh]"])
    if bk is not None:   # oracle, KHÔNG phải neo f29
        return ["loi", "[C-ca-hai]"]
    a, gach, b = mh.partition("/")
    so = lambda x, dau: 0 < len(x) <= 2 and all(c in "0123456789" for c in x) and x[0] in dau
    if not (gach and (a == "0" or so(a, "123456789")) and so(b, "123456789")):
        return ["loi", "[C-hinh-dang]"]
    k, n = int(a), int(b)
    return (["loi", "[C-pham-vi]"] if not (2 <= n <= _TRAN_MANH and k < n) else ["loi", "[C-thieu-ra]"] if not ra
            else ["manh", [k, n, ra]])


def _luoi_git():
    """#668 F34: (rc, stdout, ngoại lệ) cho nguồn HEAD — HAI nhánh 40/64 ĐỘC LẬP; kỳ vọng do `_mong_git` tính."""
    o = []
    for dai in (40, 64):
        hop = ("0123456789abcdef" * 4)[:dai]
        bien = [hop, hop[:-1], hop + "a", " " + hop + "\n", hop + " " + hop]
        bien += [hop[:i] + c + hop[i + 1:] for i in (0, dai // 2, dai - 1) for c in ("A", "F", "g", "z", "_", "\u0660")]
        o += [(0, x, None) for x in bien] + [(rc, hop, None) for rc in (1, 2, -9)]
    # #698 M5 (dò `z_exc_*`): ba kiểu NGOÀI tập bắt — phía mở rộng; ba kiểu sẵn có đo phía thu hẹp.
    return o + [(0, "", None), (0, "not-a-head", None)] + [(0, "", e) for e in (
        "OSError", "SubprocessError", "TimeoutExpired", "ValueError", "UnicodeDecodeError", "RuntimeError")]


def _mong_git(rc, ra, loi):
    s = ra.strip()
    if loi in ("ValueError", "UnicodeDecodeError", "RuntimeError"):   # #698 M5: `_van_tay` KHÔNG được bắt ⇒ lọt thành dữ liệu
        return "NEM:" + loi
    return s if loi is None and rc == 0 and len(s) in (40, 64) and all(c in "0123456789abcdef" for c in s) else None


def _luoi_byte():
    """#668 F36: bảng BYTES cho `_van_tay` — biên 63/64/65 và 4095/4096/4097/8193, cặp chung tiền tố/hậu tố (>4096),
    hoa/thường, non-ASCII, khoảng trắng đầu/giữa/cuối, CR LF. Cha tự băm lại từ CHÍNH bảng này."""
    d = b"x" * 5000
    return ([b"", b"a\r\nb\n", b" a b ", "é".encode() * 40, b"Ab" * 40, b"ab" * 40, d + b"1", d + b"2", b"1" + d, b"2" + d]
            + [b"a" * n for n in (63, 64, 65, 4095, 4096, 4097, 8193)])


def _in_tu_kiem_che_do():
    """Cửa tiến trình con cho `t53`: `_doc_che_do` trên bảng môi trường cố định, in `KQ`."""
    bang_env = {
        "vang": {}, "gate": {_BIEN_BAN_KINH: "manh"}, "gate_rong": {_BIEN_BAN_KINH: ""},
        "gate_la": {_BIEN_BAN_KINH: "MANH"}, "manh": {_BIEN_MANH: "7/8", _BIEN_MANH_RA: "x"},
        "manh_16": {_BIEN_MANH: "15/16", _BIEN_MANH_RA: "x"}, "k_bang_n": {_BIEN_MANH: "8/8", _BIEN_MANH_RA: "x"},
        "n_1": {_BIEN_MANH: "0/1", _BIEN_MANH_RA: "x"}, "n_17": {_BIEN_MANH: "0/17", _BIEN_MANH_RA: "x"},
        "chu": {_BIEN_MANH: "a/8", _BIEN_MANH_RA: "x"}, "so_0_dau": {_BIEN_MANH: "01/8", _BIEN_MANH_RA: "x"},
        "cach": {_BIEN_MANH: " 0/8", _BIEN_MANH_RA: "x"}, "xuong_dong": {_BIEN_MANH: "0/8\n", _BIEN_MANH_RA: "x"},
        "so_la": {_BIEN_MANH: "١/8", _BIEN_MANH_RA: "x"}, "thieu_ra": {_BIEN_MANH: "0/8"},
        "ra_rong": {_BIEN_MANH: "0/8", _BIEN_MANH_RA: ""}, "ca_hai": {_BIEN_MANH: "0/8", _BIEN_MANH_RA: "x",
                                                                       _BIEN_BAN_KINH: "manh"},
        "ra_le": {_BIEN_MANH_RA: "x"},
        # F29 (Codex lượt 12): RỖNG ≠ VẮNG khi PHỐI HỢP biến — đổi `is None` thành truthiness phải lộ ở từng chốt.
        "bk_rong_manh": {_BIEN_BAN_KINH: "", _BIEN_MANH: "0/8", _BIEN_MANH_RA: "x"}, "ra_rong_le": {_BIEN_MANH_RA: ""},
        "ra_rong_gate": {_BIEN_MANH_RA: "", _BIEN_BAN_KINH: "manh"}, "manh_rong": {_BIEN_MANH: "", _BIEN_MANH_RA: "x"},
        "manh_rong_gate": {_BIEN_MANH: "", _BIEN_BAN_KINH: "manh"},
        # F31 (Codex lượt 13): gate khớp ĐÚNG chuỗi — chuẩn hoá khoảng trắng không được biến cấu hình sai thành gate.
        "gate_cach": {_BIEN_BAN_KINH: " manh"}, "gate_xuong_dong": {_BIEN_BAN_KINH: "manh\n"},
    }
    kq = {}

    def doc(env):
        try:
            return list(_doc_che_do(env))
        except ValueError as ex:
            return ["loi", str(ex).split("]")[0] + "]"]
        except BaseException as ex:  # noqa: BLE001 — #698 M6: ngoại lệ KHÁC của mã bị đo là DỮ LIỆU (dò x4/y4/x6_t1_ra)
            return ["NEM", type(ex).__name__]
    for ten, env in bang_env.items():
        kq[ten] = doc(env)
    # #698 M1/M2: HOME ghim (không có HOME thì `expanduser("~/x")` trả nguyên ⇒ dò expanduser thành tương đương vì máy).
    # M1 (dò e49_*, x46_*, q_*, p_cf_*, m_*, s_*_drop_zs, x_cat_*/x3_cat_*): D698 ∪ N698 × MỌI vị trí chèn/thay của `manh`,
    # `3/8`, `15/16`, `a/b`, qua CHÍNH `doc`; so sau vòng JSON với
    # `_mong_che_do`. Con trả SỐ ô + ô lệch; cha đòi số ô bằng CÔNG THỨC (thu hẹp miền ⇒ ĐỎ).
    cu_nha, lech = {x: os.environ.get(x) for x in ("HOME", "USERPROFILE")}, []
    os.environ.update(HOME="/nha698", USERPROFILE="/nha698")
    try:
        kq["luoi"] = [doc(env) for env in _luoi_che_do()]
        D, B, M, R = _d698(), _BIEN_BAN_KINH, _BIEN_MANH, _BIEN_MANH_RA
        o1 = 0
        for nh, f, v in (("bk", lambda s: {B: s}, "manh"), ("mh", lambda s: {M: s, R: "x"}, "3/8"),
                         ("mh", lambda s: {M: s, R: "x"}, "15/16"), ("ra", lambda s: {M: "3/8", R: s}, "a/b")):
            for e in (f(v[:i // 2] + c + v[i // 2 + i % 2:]) for c in map(chr, D + list(_N698)) for i in range(2 * len(v) + 1)):
                o1 += 1   # i chẵn: CHÈN tại i//2 (0…len); i lẻ: THAY tại i//2 (0…len−1)
                x, m = doc(e), _mong_che_do(e)   # bằng nhau TRƯỚC vòng JSON (kể cả dạng tuple) ⇒ bằng nhau sau; lệch mới đi vòng
                if x != m and not (m[0] == "manh" and x == ["manh", tuple(m[1])]) and json.loads(json.dumps(x)) != m:
                    lech.append([nh, ascii(e)[:90], x, m])
    finally:
        for x, v in cu_nha.items():
            os.environ.pop(x, None) if v is None else os.environ.update({x: v})
    # F9 (Codex lượt 4): NGUỒN vân tay — `sha256_test` bám BYTES của `TEP_TEST`, `head` bám HEAD thật của `GOC`, không git
    # ⇒ `None`. Mọi ca khác dùng vân tay giả, nên thay nguồn bằng hằng số từng sống qua mọi ca.
    import hashlib
    g, cu = globals(), (GOC, TEP_TEST)
    with tempfile.TemporaryDirectory(prefix="vt668_") as d:
        d = Path(d)
        tep = d / "t.py"
        tep.write_bytes(b"a\r\n")   # F34: CR trước LF — băm BYTES, không băm văn bản đã chuẩn hoá xuống dòng
        git = lambda *a: subprocess.run(["git", "-C", str(d), "-c", "user.email=t@t", "-c", "user.name=t", "-c",
                                         "commit.gpgsign=false", *a], capture_output=True, text=True, timeout=60)
        g["GOC"], g["TEP_TEST"] = d, tep
        try:
            khong_git = _van_tay()
            git("init", "-q"), git("add", "-A"), git("commit", "-q", "-m", "a")
            v1, h1 = _van_tay(), git("rev-parse", "HEAD").stdout.strip()
            tep.write_bytes(b"b\n")
            v2 = _van_tay()
            git("add", "-A"), git("commit", "-q", "-m", "b")
            v3, h3 = _van_tay(), git("rev-parse", "HEAD").stdout.strip()
        finally:
            g["GOC"], g["TEP_TEST"] = cu
    # F30/F32/F34 (Codex lượt 12–14): lưới nguồn HEAD `_luoi_git` (rc × stdout × ngoại lệ, hai nhánh 40/64) qua
    # `subprocess` giả của module; spy ghi argv/kwargs của lời gọi. Ngoại lệ lọt ra thành DỮ LIỆU, không giết con.
    import types
    cu_sp, goi, kq["luoi_git"] = g["subprocess"], [], []
    nem = {"OSError": lambda: OSError("giả"), "SubprocessError": lambda: cu_sp.SubprocessError("giả"),
           "TimeoutExpired": lambda: cu_sp.TimeoutExpired("git", 60), "ValueError": lambda: ValueError("giả"),
           "UnicodeDecodeError": lambda: UnicodeDecodeError("utf-8", bytes([255]), 0, 1, "giả"),
           "RuntimeError": lambda: RuntimeError("giả")}   # #698 M5 (dò z_exc_*): ba kiểu ngoài tập bắt

    def dau_head(run):   # #698 M6: CHỖ GỌI `_van_tay` chung của `_luoi_git`, quét `head` (M1/M1b) và M5b
        g["subprocess"] = types.SimpleNamespace(run=run, SubprocessError=cu_sp.SubprocessError)
        try:
            return _van_tay()["head"]
        except BaseException as ex:  # noqa: BLE001 — MỌI lớp, kể cả lớp ngoài Exception (dò y4/x5/x6 head, luoi_git)
            return "NEM:" + type(ex).__name__
        finally:
            g["subprocess"] = cu_sp
    for rc, ra, loi in _luoi_git():
        def run(*a, **kw):
            goi.append([list(a[0]), sorted(kw.items())])
            if loi:
                raise nem[loi]()
            return types.SimpleNamespace(returncode=rc, stdout=ra)
        kq["luoi_git"].append(dau_head(run))
    kq["goi_git"] = [goi[0], str(GOC)]
    # #698 M1/M1b: stdout giả = `h` (40/64 hex) với D698 ở ba neo (chèn đầu, chèn cuối, thay ở len//2), R698 ∩ D698 ∪ N698 ở
    # MỌI vị trí, và "x"+s+h / h+s+"x" với s ∈ T698 (mọi `c.isspace()` cộng CR LF, dẫn xuất) — kỳ vọng `_mong_git(0, v, None)`.
    # Giới hạn ĐÃ KHAI: thành viên ngoài R698 × vị trí ngoài ba neo KHÔNG đo. TEP_TEST trỏ tệp vài byte (A4-g của spec wp698).
    with tempfile.TemporaryDirectory(prefix="h698_") as d:
        g["TEP_TEST"] = Path(d) / "t.py"
        g["TEP_TEST"].write_bytes(b"698")
        # #698 M8: bytes của TEP_TEST cấp TỪ BỘ NHỚ trong lúc quét (`head` không phụ thuộc chúng; F36 đo băm ở bảng byte dưới) —
        # đổi MÔI TRƯỜNG giàn kiểm soát, không đổi thân `_van_tay`; khôi phục ở `finally`. Cùng lối thay `Path.read_bytes` của F35 ở `--tu-kiem-gom`.
        cu_rb, Path.read_bytes = Path.read_bytes, lambda self, _b=g["TEP_TEST"].read_bytes(): _b
        try:
            DS, o2 = set(D), 0
            T = [chr(c) for c in range(0x110000) if not 0xD800 <= c <= 0xDFFF and chr(c).isspace()] + [chr(13) + chr(10)]
            for h in (("0123456789abcdef" * 4)[:40], ("0123456789abcdef" * 4)[:64]):
                L, rn = len(h), [c for c in _R698 if c in DS] + list(_N698)
                o = [(c, i) for c in D for i in (0, 2 * L, L // 2 * 2 + 1)] + [(c, i) for c in rn for i in range(2 * L + 1)]
                for v in [h[:i // 2] + chr(c) + h[i // 2 + i % 2:] for c, i in o] + [y for s in T for y in ("x" + s + h, h + s + "x")]:
                    o2 += 1
                    x, m = dau_head(lambda *a, **kw: types.SimpleNamespace(returncode=0, stdout=v)), _mong_git(0, v, None)
                    if x != m:
                        lech.append(["head", ascii(v)[:90], x, m])
            # #698 M5b: miền KIỂU dẫn xuất E698 = bao đóng bắc cầu BaseException.__subclasses__() LÚC QUÉT (+ chính nó; danh sách
            # lớn dần trong vòng). Hợp đồng — luật CHO PHÉP đóng: `_van_tay` bắt E ⇔ issubclass(E, (OSError, SubprocessError)).
            import builtins
            E, k5, l5, h5 = [BaseException], [], [], []
            for e in E:
                E += [z for z in e.__subclasses__() if z not in E]
                try:
                    x = (e("698", [(Exception if issubclass(e, Exception) else BaseException)("698")])
                         if issubclass(e, getattr(builtins, "BaseExceptionGroup", ())) else e.__new__(e))
                except Exception:  # noqa: BLE001 — không dựng được ⇒ vào danh sách riêng, cha đòi RỖNG
                    x = None
                (k5 if type(x) is e else h5).append(f"{e.__module__}.{e.__qualname__}")

                def nem5(*a, **kw):
                    raise x
                y, m = dau_head(nem5), None if issubclass(e, (OSError, cu_sp.SubprocessError)) else "NEM:" + e.__name__
                if type(x) is e and y != m:
                    l5.append([k5[-1], y, m])
            kq["m5b"] = [k5, l5[:10], len(l5), h5]
        finally:
            g["TEP_TEST"], Path.read_bytes = cu[1], cu_rb
    kq["m1"] = [o1, o2, lech[:10], len(lech)]
    # F36 (Codex lượt 15): NGUỒN băm trên bảng byte lớn/biên — lệnh ngoài giả (không cần `head`); ngoại lệ thành dữ liệu.
    kq["byte"] = {"tep": str(cu[1]), "thuc": None, "luoi": []}
    g["subprocess"] = types.SimpleNamespace(run=lambda *a, **kw: types.SimpleNamespace(returncode=1, stdout=""),
                                            SubprocessError=cu_sp.SubprocessError)
    try:
        kq["byte"]["thuc"] = _van_tay()["sha256_test"]
        with tempfile.TemporaryDirectory(prefix="vb668_") as d:
            for b in _luoi_byte():
                (Path(d) / "t.py").write_bytes(b)
                g["TEP_TEST"] = Path(d) / "t.py"
                kq["byte"]["luoi"].append(_van_tay()["sha256_test"])
    except Exception as ex:  # noqa: BLE001
        kq["byte"]["luoi"].append("NEM:" + type(ex).__name__)
    finally:
        g["subprocess"], g["TEP_TEST"] = cu_sp, cu[1]
    sha = lambda b: hashlib.sha256(b).hexdigest()
    kq["van_tay"] = [bool(h1 and h3), khong_git["head"] is None, v1["head"] == h1, v1["sha256_test"] == sha(b"a\r\n"),
                     v2["sha256_test"] == sha(b"b\n") and v2["head"] == h1, v3["head"] == h3 != h1]
    print("KQ " + json.dumps(kq, ensure_ascii=True))


def _in_tu_kiem_cong_that():
    """Cửa tiến trình con cho `t45`: chạy phép nối cổng trên MỘT gốc cho trước rồi in ra."""
    i = sys.argv.index("--tu-kiem-cong-that")
    goc = sys.argv[i + 1]
    bq = sys.argv[i + 2] if len(sys.argv) > i + 2 else None
    loi, dong = _cong_tren_cay_that(Path(goc), bq)
    print("KQ " + json.dumps([loi, dong], ensure_ascii=False))
    sys.exit(0 if loi == 0 else 9)


def main() -> int:
    try:
        che_do, tham_so = _doc_che_do(os.environ)
    except ValueError as ex:
        # TRƯỚC mọi ca: cấu hình sai thì không có kết quả nào đáng tin để in (#668).
        print(f"  ĐỎ  cấu hình chế độ: {ex}")
        return 2
    tien_kiem_bo_qua = [x for x in (_chay_tien_kiem(batch_behavior_test),
                                    _chay_tien_kiem(python_alias_behavior_test)) if x]
    # TACH KHOI `bo_qua` cua CA: `bo_qua` la MAU SO (`len(CA) - len(bo_qua)`), ma tien kiem
    # KHONG nam trong `CA`. Gop vao la lam con so noi doi — dung loai loi ma tep nay ton tai
    # de to cao. In rieng, dem rieng.
    qua, hong, bo_qua = 0, [], []
    for fn in CA:
        try:
            fn()
            qua += 1
        except BoQuaMoiTruong as ex:
            bo_qua.append((fn.__name__, str(ex)))
        except AssertionError as ex:
            hong.append((fn.__name__, str(ex)))
        except Exception as ex:  # noqa: BLE001
            hong.append((fn.__name__, f"{type(ex).__name__}: {ex}"))
    for ten, ly in tien_kiem_bo_qua:
        print(f"  BỎ QUA (TIỀN KIỂM) {ten}: {ly}")
    for ten, ly in bo_qua:
        print(f"  BỎ QUA {ten}: {ly}")
    for ten, ly in hong:
        print(f"  ĐỎ  {ten}: {ly}")
    print(f"\ncong_cu_test: {qua}/{len(CA) - len(bo_qua)} đạt; tổng={len(CA)}, "
          f"bỏ qua={len(bo_qua)}, tiền kiểm bỏ qua={len(tien_kiem_bo_qua)}")

    if che_do == "manh":
        # Mảnh CHỈ đo bán kính của phần mình. Cổng cây thật + các tự kiểm chạy ở job `gate` (chế độ `gate`), một lần.
        k, n, ra = tham_so
        ten = _phan_manh(k, n)
        if hong or tien_kiem_bo_qua:
            _ket_thuc_manh(k, n, ra, ten, None, "nền đỏ hoặc tiền kiểm bị bỏ qua — không đo", _van_tay())
            print(f"  ĐỎ  mảnh {k}/{n} [M-nen]: nền KHÔNG xanh — không đo bán kính, không ghi tệp")
            return 1
        print(f"\nBÁN KÍNH ĐỘT BIẾN — MẢNH {k}/{n} ({len(ten)}/{len(DOT_BIEN)} đột biến; "
              f"{_so_tien_trinh_ban_kinh()} tiến trình):")
        # Không `break`: nhóm hỏng ĐẦU TIÊN quyết định lý do, mọi nhóm vẫn được nhận — một nhóm hỏng đứng trước nhóm
        # lành không được làm `ket` thành `None` rồi để vòng sau ném (F7, Codex lượt 4).
        ket, ly_con = {}, None
        for nhom, rc, ra_con in _phong_con(ten, (), _so_tien_trinh_ban_kinh()) if ten else ():
            nhan, ly = _nhan_ket_qua_con(nhom, rc, ra_con, ())
            if nhan is None:
                ly_con = ly_con or f"{ly}; rc={rc}, đuôi đầu ra: {ra_con[-300:]!r}"
            ket.update(nhan or {})
        dong, loi = _ket_thuc_manh(k, n, ra, ten, None if ly_con else ket, ly_con, _van_tay())
        for d in dong:
            print(d)
        return 1 if loi else 0

    # N31 — CỔNG PHẢI ĐƯỢC NỐI VÀO CHỖ NÓ GÁC. Chạy MỘT lần, trên cây THẬT, TRƯỚC bộ đột
    # biến: đột biến dựng cây SAO và tráo `BASH_NEN`, nên chạy sau sẽ đo nhầm bản sao.
    loi_cong, dong_cong = _cong_tren_cay_that(GOC)
    print()
    for d in dong_cong:
        print(d)

    loi_db = _tu_kiem_phan_hang()
    loi_db += _tu_kiem_gian_giao()
    # MỘT ca đỏ ở NỀN không được làm hỏng phép đo bán kính của TOÀN BỘ bộ đột biến (r8, xem
    # `_bao_cao_nen_do`): báo một lần, loại khỏi mọi bán kính, vẫn kéo mã thoát khác 0.
    do_o_nen = sorted(t for t, _ in hong)
    dong_nen, loi_nen = _bao_cao_nen_do(do_o_nen)
    for d in dong_nen:
        print(d)
    loi_db += loi_nen
    so_tien_trinh = _so_tien_trinh_ban_kinh()
    loi_db += _tu_kiem_song_song(do_o_nen)
    if che_do == "gate":
        print(f"\nBÁN KÍNH ĐỘT BIẾN ({len(DOT_BIEN)} đột biến): GIAO cho job `gate-cong-cu` (mảnh) + "
              f"`gate-cong-cu-gop` (gom) — KHÔNG đo trong tiến trình này ({_BIEN_BAN_KINH}=manh)")
    else:
        print(f"\nBÁN KÍNH ĐỘT BIẾN ({len(DOT_BIEN)} đột biến, mỗi ca đúng một"
              + (f"; LOẠI {len(do_o_nen)} ca đỏ ở nền" if do_o_nen else "")
              + f"; {so_tien_trinh} tiến trình):")
        for cac_dong, loi in _ban_kinh_moi_dot_bien(list(DOT_BIEN), do_o_nen, so_tien_trinh):
            for dong in cac_dong:
                print(dong)
            loi_db += loi
    print(f"\nSỐ LIỆU: ca={len(CA)} · đột biến={len(DOT_BIEN)}"
          + (" (giao mảnh)" if che_do == "gate" else "") + f" · lỗi đột biến={loi_db}"
          f" · tiền kiểm bỏ qua={len(tien_kiem_bo_qua)} · cổng cây thật={'ĐẠT' if not loi_cong else 'HỎNG'}")
    # Tien kiem bi bo qua KEO ma thoat khac 0. `KHONG_DO_DUOC` khong duoc lang le thanh XANH —
    # `None != False`. No chi thoi giet CA SUITE, chu khong thoi la mot tin hieu.
    return 1 if (hong or loi_db or tien_kiem_bo_qua or loi_cong) else 0

_KET_GIA_RONG = {
    "ca_dich_gia": ("giet_that", "chốt của chính nó"),
    "ca_oan_gia": ("giet_that", "giàn giáo phóng công cụ giả hỏng: rc=1"),
    "ca_xanh_gia": ("qua", None),
}
_KET_GIA_VO_CAN = {
    # Nhanh `gia`: mot ca oan chet bang LOI VO CAN. Luot do Windows `570-do-5` roi dung vao
    # day, va ban truoc in ten ca ma KHONG in loi ay la gi.
    "ca_dich_gia": ("giet_that", "chốt của chính nó"),
    "ca_oan_vo_can": ("tin_dung_gia", "giàn giáo hỏng: gọi _bash_windows hỏng: rc=1"),
    "ca_xanh_gia": ("qua", None),
}
_KET_GIA_HEP = {
    "ca_dich_gia": ("giet_that", "chốt của chính nó"),
    "ca_xanh_gia": ("qua", None),
}


def _in_tu_kiem_dong_ho():
    """Cua de DOT BIEN cham toi duoc phep nhan dien dong ho nhay (xem `_in_tu_kiem_ban_kinh`)."""
    def am():
        raise subprocess.TimeoutExpired(cmd=["gia-am"], timeout=-232.95)

    def duong():
        raise subprocess.TimeoutExpired(cmd=["gia-duong"], timeout=120)

    print("DH1 " + json.dumps(_chay_1_ca(am)))
    print("DH2 " + json.dumps(_chay_1_ca(duong)))


def _in_tu_kiem_tien_kiem():
    """Cua de DOT BIEN cham toi duoc `_chay_tien_kiem` — cung ly do voi cua ban kinh:
    `t31` goi ham ay, ma bo dot bien mutate mot BAN SAO tren dia, nen phai hoi qua tien
    trinh con doc ma tu `TEP_TEST` thi `t31_tien_kiem_nuot_moi_loi` moi co cho can."""
    def thieu_moi_truong():
        raise BoQuaMoiTruong("thiếu thứ để đo")

    def chay_duoc():
        return None

    def hong_nghiep_vu():
        bang(False, "chốt nghiệp vụ hỏng")

    print("TK1 " + json.dumps(_chay_tien_kiem(thieu_moi_truong)))
    print("TK2 " + json.dumps(_chay_tien_kiem(chay_duoc)))
    try:
        r = _chay_tien_kiem(hong_nghiep_vu)
        print("TK3 " + json.dumps(["NUOT", r]))
    except BaseException as ex:                     # noqa: BLE001 — ĐO cái gì thoát ra
        print("TK3 " + json.dumps(["NEM", type(ex).__name__]))


_KET_GIA_NEN_DO = {
    "ca_dich_gia": ("giet_that", "chốt của chính nó"),
    "ca_do_o_nen": ("giet_that", "chốt của chính nó — nhưng nó đã ĐỎ SẴN ở nền"),
    "ca_xanh_gia": ("qua", None),
}


def _in_tu_kiem_nen_do():
    """Cửa để ĐỘT BIẾN chạm tới cơ chế loại ca đỏ ở nền — cùng lý do với `_in_tu_kiem_ban_kinh`:
    `t42` đọc qua tiến trình con vì đột biến trên tệp không cắn mã đã nạp. Cửa RIÊNG, không nối
    vào `--tu-kiem-ban-kinh`, vì `t29` chốt cửa ấy in ĐÚNG ba kịch bản."""
    d1, l1 = _ket_luan_ban_kinh("db_gia", "ca_dich_gia", _KET_GIA_NEN_DO, 3,
                                do_o_nen=("ca_do_o_nen",))
    print("ND1 " + json.dumps([l1, d1], ensure_ascii=False))
    d2, l2 = _ket_luan_ban_kinh("db_gia", "ca_dich_gia", _KET_GIA_NEN_DO, 3,
                                do_o_nen=("ca_dich_gia",))
    print("ND2 " + json.dumps([l2, d2], ensure_ascii=False))
    d3, l3 = _bao_cao_nen_do(["ca_do_o_nen"])
    print("ND3 " + json.dumps([l3, d3], ensure_ascii=False))
    d4, l4 = _bao_cao_nen_do([])
    print("ND4 " + json.dumps([l4, d4], ensure_ascii=False))


def _in_tu_kiem_ban_kinh():
    """Cửa để ĐỘT BIẾN chạm tới được phần phán quyết.

    `t29` gọi `_ket_luan_ban_kinh` TRONG TIẾN TRÌNH, mà bộ đột biến của tệp này mutate
    một BẢN SAO trên đĩa rồi trỏ `GOC` vào đó — mutate đĩa không đổi được hàm đã nạp.
    Tức nếu chỉ có lời gọi trong tiến trình thì `t29` là ca KHÔNG CÓ ĐỘT BIẾN NÀO, đúng
    thứ tệp này tồn tại để tố cáo. Cửa này cho `t29` hỏi lại chính câu ấy QUA một tiến
    trình con đọc mã từ `GOC`, nên `bn_ban_kinh_giau_ly_do` mới có chỗ cắn."""
    for ket, tong in ((_KET_GIA_RONG, 3), (_KET_GIA_VO_CAN, 3), (_KET_GIA_HEP, 2)):
        dong, loi = _ket_luan_ban_kinh("db_gia", "ca_dich_gia", ket, tong)
        print(f"LOI={loi}")
        for d in dong:
            print(d)


def _in_tu_kiem_che_do_utf8():
    """Cửa `t62` (#671), mã thoát RIÊNG; phải ở TRONG `_CUA` (ngoài bảng ⇒ `f25_cua_moi_vi_tri` tín dụng giả)."""
    print(f"UTF8_MODE={sys.flags.utf8_mode} B={sys.flags.dont_write_bytecode} "
          f"DA_PHONG_LAI={int(_DA_PHONG_LAI)} DAU_SOT={int(_DAU_PHONG_LAI in os.environ)}")
    sys.exit(_MA_TU_KIEM_UTF8)


if __name__ == "__main__":
    # #668 F25 (Codex lượt 8): cửa CHỈ đọc ở argv[1]. Bản trước dò MỌI vị trí, nên `--gop --tu-kiem-che-do` chạy cửa tự
    # kiểm, rc=0, KHÔNG gom — một giá trị đối số chiếm quyền chọn chế độ. Đối số lạ ⇒ rc=2, không lặng lẽ chạy `main`.
    _CUA = {"--tu-kiem-ban-kinh": _in_tu_kiem_ban_kinh, "--tu-kiem-nen-do": _in_tu_kiem_nen_do,
            "--tu-kiem-tien-kiem": _in_tu_kiem_tien_kiem, "--tu-kiem-dong-ho": _in_tu_kiem_dong_ho,
            "--tu-kiem-luat-phan-quyet": _in_tu_kiem_luat_phan_quyet, "--tu-kiem-cong-that": _in_tu_kiem_cong_that,
            "--ban-kinh-con": _in_ban_kinh_con, "--tu-kiem-gom": _in_tu_kiem_gom,
            "--tu-kiem-che-do": _in_tu_kiem_che_do, "--tu-kiem-main": _in_tu_kiem_main,
            "--tu-kiem-che-do-utf8": _in_tu_kiem_che_do_utf8}
    cua = sys.argv[1] if len(sys.argv) > 1 else None
    if cua == "--gop":
        sys.exit(_main_gop())
    if cua in _CUA:
        _CUA[cua]()
        sys.exit(0)
    if cua is not None:
        print(f"  ĐỎ  đối số lạ {sys.argv[1:]!r}: chỉ nhận MỘT cửa ở vị trí đầu, hoặc không đối số")
        sys.exit(2)
    sys.exit(main())
