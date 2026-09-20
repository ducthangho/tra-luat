#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ops/cong_cu.py — G1..G6 packet #290: probe+canary+cổng BA trạng thái (ĐẠT/ĐỎ/
KHÔNG_ĐO_ĐƯỢC, mã riêng) cho `ops/cong_cu.yaml`. `cai-lenh` chỉ TRA CỨU rồi in lệnh cài
(dòng 1) + biến môi trường (dòng sau) — thực thi thuộc `ops/cai_cong_cu.sh`."""
from __future__ import annotations

import argparse, json, os, platform, re, shutil, subprocess, sys
from pathlib import Path

import yaml

GOC = Path(__file__).resolve().parent.parent
DAT, DO, KHONG_DO_DUOC = "DAT", "DO", "KHONG_DO_DUOC"
RC = {DAT: 0, DO: 2, KHONG_DO_DUOC: 3}
CHINH_SACH_CANARY = {"blocking", "advisory"}
KY_TU_TOKEN_BAN = re.compile(r"[0-9A-Za-z._+-]")

def doc_ban_ke(duong):
    d = yaml.safe_load(open(duong, encoding="utf-8")) or {}
    if not isinstance(d.get("cong_cu"), dict) or not d["cong_cu"]:
        raise SystemExit(f"ban ke '{duong}' rong hoac thieu khoa 'cong_cu'")
    for ten, dn in d["cong_cu"].items():
        if not isinstance(dn, dict) or not isinstance(dn.get("bat_buoc"), bool):
            raise SystemExit(f"ban ke '{ten}': 'bat_buoc' phai la bool")
        if "chuan_bi" in dn and not isinstance(dn["chuan_bi"], bool):
            raise SystemExit(f"ban ke '{ten}': 'chuan_bi' phai la bool")
        bg = dn.get("ban_ghim")
        if bg is not None and (not isinstance(bg, str) or not bg.strip()):
            raise SystemExit(f"ban ke '{ten}': 'ban_ghim' chi nhan chuoi khac rong hoac null")
        cn = dn.get("canary")
        if cn is not None and (not isinstance(cn, str) or not cn.strip()):
            raise SystemExit(f"ban ke '{ten}': 'canary' phai la chuoi khac rong")
        if "chinh_sach" in dn and (cn is None or not isinstance(dn["chinh_sach"], str)
                                    or dn["chinh_sach"] not in CHINH_SACH_CANARY):
            raise SystemExit(f"ban ke '{ten}': 'chinh_sach' chi nhan blocking|advisory va doi hoi canary")
        probe = dn.get("probe")
        if not isinstance(probe, list) or not probe:
            raise SystemExit(f"ban ke '{ten}': 'probe' phai la danh sach khac rong")
        for pb in probe:
            erc = pb.get("expected_rc", 0) if isinstance(pb, dict) else None
            erc = [erc] if isinstance(erc, int) and not isinstance(erc, bool) else erc
            if (not isinstance(pb, dict) or not isinstance(pb.get("lenh"), list)
                    or not pb["lenh"] or not all(isinstance(x, str) and x for x in pb["lenh"])
                    or not isinstance(pb.get("regex"), str)
                    or not isinstance(erc, list) or not erc
                    or not all(isinstance(x, int) and not isinstance(x, bool) for x in erc)):
                raise SystemExit(f"ban ke '{ten}': probe/lenh/regex/expected_rc khong hop le")
            try:
                if re.compile(pb["regex"]).groups < 1:
                    raise ValueError
            except (re.error, ValueError):
                raise SystemExit(f"ban ke '{ten}': regex probe phai hop le va co nhom bat")
    return d

def nen_hien_tai():
    t = (os.environ.get("CONG_CU_NEN") or os.environ.get("RUNNER_OS") or platform.system() or "").lower()
    if t.startswith("linux"): return "linux"
    if t in ("macos", "darwin"): return "macos"
    if t.startswith("win") or t in ("mingw", "msys", "cygwin"): return "windows"
    return t or "unknown"

def _bash_windows(path=None, system_root=None, program_files=None, git=None):
    """`bash` ĐÃ CHỨNG MINH làm được việc — uỷ quyền cho `ops/bash_nen.py::tim_bash()`.

    HỢP NHẤT (#570 revision 3, N14). Thân cũ của hàm này là bộ giải RIÊNG thứ HAI trong ba
    bộ giải độc lập cho cùng một khuyết tật, và là bộ cuối cùng còn sót sau khi `_bash_posix`
    hợp nhất ở r2. Nó quyết bằng ĐƯỜNG DẪN: loại mọi ứng viên nằm dưới `%SystemRoot%`.

    VÌ SAO BỎ CÁCH ẤY — đo được, không phải sở thích:
    · `CLAUDE.md`: *"danh sách CẤM không bao giờ đủ — phải đảo thành danh sách CHO PHÉP"*.
      Loại theo vị trí là một danh sách cấm đội lốt; nó phân biệt CHỖ ĐỨNG, không phân biệt
      NĂNG LỰC. Một `bash` POSIX thật đặt dưới `%SystemRoot%` bị nó từ chối oan, còn một bộ
      phóng WSL đặt chỗ khác thì nó nhận.
    · Nghiệm thu Windows `570-do-5` (20-09-2026, máy chủ kho) cho thấy phép NĂNG LỰC bắt
      đúng thứ cần bắt, và nêu được LÝ DO: `C:\\Windows\\system32\\bash.exe` ⇒ `dat=false`,
      *"phép argv: `$0` là '/bin/bash', mong 'bn-argv-probe' — đối số vị trí KHÔNG tới nơi"*.
      Còn `C:\\Program Files\\Git\\bin\\bash.exe` ⇒ `dat=true`. Tên không nói được điều đó.

    `ung_vien()` VẪN xếp ứng viên dưới `%SystemRoot%` xuống CUỐI — nhưng đó là THỨ TỰ THỬ
    (để phép đắt ít phải chạy), KHÔNG phải quyết định. Thứ loại là `_do_nang_luc`.

    Trả `None` khi không ứng viên nào làm được việc, giữ nguyên HỢP ĐỒNG cũ: người gọi
    fail-close chứ không đoán. Bốn tham số chỉ để test ép nền — chúng đi thẳng sang
    `ung_vien()`, nơi có đúng bốn tham số cùng tên và cùng nghĩa."""
    import sys as _sys
    _here = Path(__file__).resolve().parent
    if str(_here) not in _sys.path:
        _sys.path.insert(0, str(_here))
    try:
        import bash_nen
    except ImportError as ex:
        # FAIL-CLOSE CO LY DO, khong phai `ModuleNotFoundError` tran.
        # ĐO ĐƯỢC 20-09-2026 tren Windows that (bo do `570-do-6`): `_chay_batch` cua bo test
        # chep `cong_cu.py` sang mot cay tam MA KHONG chep `bash_nen.py`, nen nhanh du phong
        # duoi day no `ModuleNotFoundError` va giet ca suite TRUOC vong lap ca. Linux khong
        # bat duoc: nhanh ay nam trong `except OSError`, ma tren Linux `subprocess.run` chay
        # duoc script shebang nen no KHONG BAO GIO toi.
        # Mot cay thieu bo giai la cay HONG, khong phai cay "khong co bash" — nen noi ro ra
        # thay vi de nguoi doc di truy mot `ImportError` khong ten.
        raise RuntimeError(
            f"thieu bo giai dung chung: khong import duoc `bash_nen` tu {_here}. "
            f"Moi cay mang `ops/cong_cu.py` phai mang ca `ops/bash_nen.py` (#570 N14). "
            f"Goc: {type(ex).__name__}: {ex}") from ex
    ep = {k: v for k, v in (("path", path), ("system_root", system_root),
                            ("program_files", program_files), ("git", git))
          if v is not None}
    duong, _ = bash_nen.tim_bash(**ep)
    return duong

def _chay(argv, timeout=20):
    """Trả (rc, output, lỗi-khởi-chạy); timeout là ĐÃ chạy nhưng hỏng, khác không mở được."""
    # `cai_cong_cu.sh` chấp nhận python/python3/py. Probe module và probe `python`
    # phải đo đúng interpreter đã chọn để máy chỉ có python3 không đỏ sau khi vừa cài.
    argv = [sys.executable, *argv[1:]] if argv and argv[0] == "python" else argv
    if os.name == "nt" and argv and argv[0] == "bash":
        # Xem `_bash_windows`: đường dẫn TUYỆT ĐỐI để CreateProcess không rẽ vào System32.
        # Cửa gọi THỨ NHẤT trong hai cửa — cửa kia ở nhánh dự phòng dưới. Cả hai phải xử lý
        # `RuntimeError` như nhau, kẻo một cây thiếu `bash_nen.py` làm hỏng ĐÚNG MỘT cửa và
        # ta lại đi vá cửa được chỉ rồi bỏ sót cửa còn lại — hình dạng kho đã ghi sổ.
        try:
            bash_gb = _bash_windows()
        except RuntimeError as ex_bn:
            return None, "", f"thieu_bo_giai:{ex_bn}"
        argv = [bash_gb, *argv[1:]] if bash_gb else argv
    try:
        p = subprocess.run(argv, capture_output=True, text=True, timeout=timeout)
        return p.returncode, (p.stdout or "") + (p.stderr or ""), None
    except subprocess.TimeoutExpired as ex:
        ra = (ex.stdout or "") + (ex.stderr or "")
        return None, ra if isinstance(ra, str) else "", "qua_han"
    except OSError as ex:
        # Python native tren Windows khong chay truc tiep script shebang khong co `.exe`;
        # duong lui nay giu probe script dung duoc trong Git Bash, binary that van di duong tren.
        # MOT bo giai (#570 r3, N14). Ban cu re nhanh: Windows thi qua `_bash_windows`, con
        # lai thi `shutil.which("bash")` TRAN — tuc nen khong sinh ra khuyet tat van phan giai
        # theo TEN, va do la cho bo giai thu tu se moc len.
        # Ban cu con MOT loi nua, chi thay khi doc ky: gia tri tinh o nhanh `else` ay KHONG BAO
        # GIO duoc dung, vi vong lap duoi bi chan boi `os.name == "nt"`. Tuc no la ma chet dang
        # tinh toan. Nay chi tinh khi SE dung.
        if os.name == "nt":
            try:
                bash = _bash_windows()
            except RuntimeError as ex_bn:
                return None, "", f"thieu_bo_giai:{ex_bn}"
            for d in (os.environ.get("PATH", "").split(os.pathsep) if bash else []):
                ung = Path(d) / argv[0]
                if ung.is_file():
                    try:
                        p = subprocess.run([bash, str(ung), *argv[1:]], capture_output=True,
                                           text=True, timeout=timeout)
                        return p.returncode, (p.stdout or "") + (p.stderr or ""), None
                    except subprocess.TimeoutExpired as ex2:
                        ra = (ex2.stdout or "") + (ex2.stderr or "")
                        return None, ra if isinstance(ra, str) else "", "qua_han"
                    except OSError:
                        break
        return None, "", f"khong_khoi_chay:{type(ex).__name__}"

def _cat_tien_to_token(ra, m):
    """Regex phải bắt trọn token; `1.7.7` trong `1.7.7-rc1` không phải một phiên bản."""
    dau, cuoi = m.start(1), m.end(1)
    return ((dau and KY_TU_TOKEN_BAN.fullmatch(ra[dau - 1]))
            or (cuoi < len(ra) and KY_TU_TOKEN_BAN.fullmatch(ra[cuoi])))

def kiem_tra_1(ten, dn):
    bat_buoc, ban_ghim, ban_thay = dn["bat_buoc"], dn.get("ban_ghim"), {}
    khong_mo, hong = [], []
    for pb in dn.get("probe") or []:
        ten_pb = pb.get("ten", "mac_dinh")
        rc, ra, loi = _chay(pb["lenh"])
        ban_thay[ten_pb] = None
        if loi and loi.startswith("khong_khoi_chay"):
            khong_mo.append(ten_pb)
            continue
        if loi == "qua_han":
            hong.append(f"probe '{ten_pb}' da chay nhung qua han")
            continue
        erc = pb.get("expected_rc", 0)
        erc = [erc] if isinstance(erc, int) else erc
        if rc not in erc:
            hong.append(f"probe '{ten_pb}' da chay nhung rc={rc}, mong {erc}")
            continue
        m = re.search(pb["regex"], ra)
        if not m or not m.group(1) or _cat_tien_to_token(ra, m):
            hong.append(f"probe '{ten_pb}' da chay nhung khong parse tron token phien ban")
            continue
        ban_thay[ten_pb] = m.group(1)
    goc = {"ten": ten, "bat_buoc": bat_buoc, "ban_ghim": ban_ghim, "ban_thay": ban_thay}
    if hong:
        return {**goc, "trang_thai": DO, "chi_tiet": "; ".join(hong)}
    if khong_mo:
        return {**goc, "trang_thai": KHONG_DO_DUOC,
                "chi_tiet": f"khong khoi chay duoc probe {khong_mo} cua '{ten}'"}
    khac_nhau = set(ban_thay.values())
    if len(ban_thay) > 1 and len(khac_nhau) > 1:  # T7, độc lập ban_ghim
        return {**goc, "trang_thai": DO,
                "chi_tiet": f"cac duong goi khac ban: {ban_thay} — co mat khong phai cung ban"}
    if ban_ghim is not None and any(v != ban_ghim for v in ban_thay.values()):
        return {**goc, "trang_thai": DO, "chi_tiet": f"sai ban: mong '{ban_ghim}', thay {ban_thay}"}
    return {**goc, "trang_thai": DAT, "chi_tiet": "dat"}

def kiem_tra_canary(ten_canary, ten_chu, dn, theo_ten, thu_muc_goc):
    chu = theo_ten[ten_chu]
    goc = {"ten": ten_canary, "chu_so_huu": ten_chu,
           "chinh_sach": dn.get("chinh_sach", "blocking")}
    if chu["trang_thai"] != DAT:
        return {**goc, "trang_thai": chu["trang_thai"],
                "chi_tiet": f"tool chu so huu '{ten_chu}' chua DAT"}
    fixture = thu_muc_goc / "ops" / "canary" / f"{ten_canary}.yml"
    if not fixture.is_file():
        return {**goc, "trang_thai": KHONG_DO_DUOC, "chi_tiet": f"thieu fixture '{fixture}'"}
    lenh = [dn["probe"][0]["lenh"][0], str(fixture)]
    rc, ra, loi = _chay(lenh, timeout=30)
    if loi and loi.startswith("khong_khoi_chay"):
        return {**goc, "trang_thai": KHONG_DO_DUOC, "chi_tiet": f"khong goi duoc '{ten_chu}'"}
    if loi == "qua_han":
        return {**goc, "trang_thai": DO, "chi_tiet": f"canary '{ten_canary}' qua han"}
    if "SC1003" in ra:
        return {**goc, "trang_thai": DAT, "chi_tiet": f"canary bat dung SC1003 (rc={rc})"}
    sc_thieu = (theo_ten.get("shellcheck") or {}).get("trang_thai") != DAT
    ly_do = ("SUY_GIAM: thieu shellcheck nen actionlint am tham bo lop luat SC*" if sc_thieu else
             "canary KHONG bat duoc SC1003 du shellcheck co mat — kiem fixture/ban actionlint")
    return {**goc, "trang_thai": DO, "chi_tiet": f"{ly_do} (rc={rc})"}

def tong_hop(ban_ke, thu_muc_goc=None, chi=None):
    cc = ban_ke["cong_cu"]
    theo_ten = {t: kiem_tra_1(t, cc[t]) for t in ([chi] if chi else cc.keys())}
    canary_kq, da_chay = [], set()
    # NỢ (r362, 10-09-2026). HAI HẠNG NGUỒN, đừng trộn: CƠ CHẾ dưới đây ĐO ĐƯỢC (đọc chính hàm
    # này, và đọc `cai_cong_cu.sh` gọi kèm `--chi`); còn mọi câu về MỘT LƯỢT CI CỤ THỂ là THUẬT
    # LẠI — không log job nào trong kho, không ai tái đo được offline. Cấu hình CHO PHÉP diễn
    # biến ấy; cho phép không phải đã xảy ra.
    # `chi` có giá trị ⇒ KHÔNG canary nào chạy, nên bản tóm tắt của
    # một lệnh MỘT-CÔNG-CỤ có thể in `trang_thai_tong: DAT` ngay cạnh `shellcheck: KHONG_DO_DUOC`,
    # kèm `"canary": []`. CI gọi đúng kiểu ấy ở hai bước (`cai_cong_cu.sh shellcheck` / `… rg`), nên
    # ai đọc RIÊNG một bước sẽ kết luận công cụ lành trong khi nó hỏng.
    #   ĐỘ PHỦ VẪN CÒN: bước `#9 G5` gọi `kiem-tra` KHÔNG kèm `--chi`, và canary
    #   `actionlint_shellcheck` là `blocking`. Đo một biến, cùng cây, chỉ khác PATH:
    #     có shellcheck   -> canary DAT ("canary bat dung SC1003")
    #     thiếu shellcheck-> canary DO  ("SUY_GIAM: thieu shellcheck nen actionlint am tham bo SC*")
    #   Nên đây là MÀU XANH GÂY HIỂU LẦM Ở MỨC BƯỚC, KHÔNG phải lỗ độ phủ — trừ khi `#9` bị skip vì
    #   một bước trước đó đỏ. (`rg` đỏ ⇒ `#9` skip: đây là THUẬT LẠI về một lượt CI, không phải
    #   phép đo; thứ đo được là `rg` có `bat_buoc: true` trong `ops/cong_cu.yaml` và `#9` đứng SAU
    #   `#8` trong `ci.yml` — tức cấu hình CHO PHÉP nó, không phải nó đã xảy ra.)
    # XUẤT XỨ: packet #290 / `ops/specs/HA-TANG-CONG-CU-TAT-DINH.md` — ĐÃ LAND, đặc tả ĐÓNG BĂNG,
    # nên nó KHÔNG còn generation/lease/write authority để ai đó "đi qua"
    # (docs/PROTOCOL_DA_PHIEN.md DÒNG 28/116/164 — số DÒNG, không phải số mục: tệp chỉ có tới §20;
    # AGENTS.md:22-23). Sửa hành vi ở đây đòi một packet KẾ NHIỆM/corrective được cấp thẩm quyền —
    # nợ đã mở thành Issue #498, liên đới #249 — THUẬT LẠI: việc mở Issue và trạng thái hiện tại
    # của nó nằm NGOÀI kho, không hiện vật nào ở đây chứng thực, và không ai tái đo được offline.
    # `chinh_sach`/`bat_buoc` là hợp đồng của đặc tả, không phải chi tiết nội bộ: đừng đụng.
    if chi is None:
        for ten, dn in cc.items():
            cn = dn.get("canary")
            if cn and cn not in da_chay:
                da_chay.add(cn)
                canary_kq.append(kiem_tra_canary(cn, ten, dn, theo_ten, thu_muc_goc or GOC))
    tong = DAT
    for kq in theo_ten.values():
        if kq["trang_thai"] == KHONG_DO_DUOC and kq.get("bat_buoc"):
            tong = KHONG_DO_DUOC
        elif kq["trang_thai"] == DO and tong != KHONG_DO_DUOC:
            tong = DO
    for kq in canary_kq:
        if kq["chinh_sach"] == "advisory":
            continue
        if kq["trang_thai"] == KHONG_DO_DUOC:
            tong = KHONG_DO_DUOC
        elif kq["trang_thai"] == DO and tong != KHONG_DO_DUOC:
            tong = DO
    if chi is not None:
        pham_vi = "mot-cong-cu"
        canary_da_quet = False
        ghi_chu_pham_vi = "chua quet canary toan bo"
    else:
        pham_vi = "toan-bo"
        canary_da_quet = True
        ghi_chu_pham_vi = "da quet canary toan bo (khong co nghia moi canary dat)"
    return {"trang_thai_tong": tong, "pham_vi": pham_vi, "canary_da_quet": canary_da_quet, "ghi_chu_pham_vi": ghi_chu_pham_vi, "cong_cu": list(theo_ten.values()), "canary": canary_kq}

def _cai_lenh(ten, ban_ke, nen):
    dn = ban_ke["cong_cu"].get(ten)
    if dn is None: raise SystemExit(f"khong biet cong cu '{ten}'")
    cai = dn.get("cai") or {}
    ct = cai if "lenh" in cai else cai.get(nen)  # {lenh:..} dung chung MOI nen, hoac theo-nen
    if not ct: raise SystemExit(f"'{ten}' chua co cong thuc cai cho nen '{nen}'")
    print(ct["lenh"])
    for k, v in (ct.get("moi_truong") or {}).items():
        print(f"{k}={v}")
    return 0

def main(argv=None):
    ap = argparse.ArgumentParser(prog="cong_cu.py")
    sub = ap.add_subparsers(dest="lenh", required=True)
    p1 = sub.add_parser("kiem-tra")
    p1.add_argument("--chi"); p1.add_argument("--json", action="store_true"); p1.add_argument("--ban-ke")
    p2 = sub.add_parser("cai-lenh")
    p2.add_argument("ten"); p2.add_argument("--nen"); p2.add_argument("--ban-ke")
    a = ap.parse_args(argv)
    duong_ban_ke = Path(a.ban_ke) if a.ban_ke else GOC / "ops" / "cong_cu.yaml"
    ban_ke = doc_ban_ke(duong_ban_ke)
    if a.lenh == "cai-lenh":
        return _cai_lenh(a.ten, ban_ke, a.nen or nen_hien_tai())
    bc = tong_hop(ban_ke, chi=a.chi)  # T8: JSON mang van tay ten+ban_thay cho MOI ban ghi
    print(json.dumps(bc, ensure_ascii=False, indent=2 if a.json else None))
    return RC[bc["trang_thai_tong"]]

if __name__ == "__main__":
    sys.exit(main())
