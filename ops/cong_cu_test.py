#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""T1..T8 + chính sách canary (#290, sha256 b1b7e3b0…) cho cong_cu.py+cai_cong_cu.sh. Gọi
CHÍNH lệnh qua subprocess (không import) — doctrine `lease_publish_test.py`."""
from __future__ import annotations

import datetime as _dt
import json, os, runpy, shutil, subprocess, sys, tempfile
from pathlib import Path

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
        "            ban_ghi.append((nut.lineno, nut.col_offset))\n",
        "            ban_ghi.append((nut.lineno, 0))  # đột biến: đếm theo DÒNG, gộp cùng dòng\n",
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
    # (b) ten bi CHE khong chan tim kiem — tham so/phep gan bi bo qua, tiep tuc ra ngoai;
    #     `tham_so_che` va `gan_che` bi bat oan.
    "bn_ten_bi_che_khong_chan": ("ops/bash_nen.py",
        "        if ten in bang:\n            if _loc_truoc(bang[ten], truoc):\n"
        "                return _tra_import(bang[ten], truoc)\n",
        "        if ten in bang:\n            if _tra_import(bang[ten], truoc):  # đột biến: tên bị che không chặn\n"
        "                return _tra_import(bang[ten], truoc)\n",
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
    "bn_global_doi_cho_thay_vi_chep": ("ops/bash_nen.py",
        "            rb = rieng.get(ten)\n            if rb:\n",
        "            rb = rieng.pop(ten, None)  # đột biến: DỜI thay vì CHÉP\n            if rb:\n",
        "BASH_NEN", (), "t33_do_phu_cua_cong_do_duoc_THEO_HINH_DANG"),
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
    # N53: quay ve "dung mot rang buoc" thay vi "muon nhat thang".
    "bn_khong_muon_nhat_thang": ("ops/bash_nen.py",
        "    dinh = max(x[1] for x in truoc_do)\n    return {x for x in truoc_do if x[1] == dinh}\n",
        "    return set(truoc_do)  # đột biến: không lấy ràng buộc muộn nhất\n",
        "BASH_NEN", (), "t33_do_phu_cua_cong_do_duoc_THEO_HINH_DANG"),
    # N53: rang buoc neo vao CHO VIET TEN thay vi cho HOAN TAT.
    "bn_neo_cho_viet_ten": ("ops/bash_nen.py",
        "    if isinstance(n, (ast.Assign, ast.AugAssign)):\n        return _ket_nut(n.value)\n",
        "    if isinstance(n, (ast.Assign, ast.AugAssign)):\n"
        "        return (n.lineno, n.col_offset)  # đột biến: neo vào chỗ VIẾT tên\n",
        "BASH_NEN", (), "t33_do_phu_cua_cong_do_duoc_THEO_HINH_DANG"),
    # N54: phep hien thi thoi don anh => hai duong khac nhau de nhau o `ly_do`.
    "bn_hien_thi_khong_don_anh": ("ops/bash_nen.py",
        '    rel = rel.replace("\\\\", "\\\\\\\\")\n',
        "    pass  # đột biến: phép hiển thị thôi đơn ánh\n",
        "BASH_NEN", (), "t49_duong_XAU_ra_JSON_HOP_LE_va_NGAY_GO_phai_duoc_DOC"),
    # N56: cache thoi DEM LAI tap ung vien.
    "bn_khong_dem_lai_ung_vien": ("ops/bash_nen.py",
        "        ds_moi = ung_vien(**ep)\n",
        "        ds_moi = ds_cu  # đột biến: cache không đếm lại tập ứng viên\n",
        "BASH_NEN", (), "t51_cache_phai_HET_HIEU_LUC_khi_chinh_TEP_ung_vien_doi"),
    # N57: `PATH` VANG lai bi gop vao `PATH` RONG.
    "bn_path_vang_thanh_rong": ("ops/bash_nen.py",
        '        path = env["PATH"] if "PATH" in env else os.defpath\n',
        '        path = env.get("PATH", "")  # đột biến: PATH vắng bị gộp vào PATH rỗng\n',
        "BASH_NEN", (), "t51_cache_phai_HET_HIEU_LUC_khi_chinh_TEP_ung_vien_doi"),
    # N55: ratchet thoi doc XUAT XU cua bao cao => truong co che bi bat oan.
    "ct_khong_theo_xuat_xu_bao": ("ops/cong_cu_test.py",
        '                if ng == "bao" and khoa in _TRUONG_TONG_HOP:\n',
        '                if khoa in _TRUONG_TONG_HOP:  # đột biến: không hỏi xuất xứ của báo cáo\n',
        "TEP_TEST", _KEM_TEP_TEST, "t39_chi_CA_PHAN_QUYET_duoc_chot_tren_rc_va_trang_thai"),
    # N55: rang buoc MUON NHAT khong con thang => bi danh bi ghi de van bi tinh.
    "ct_xuat_xu_khong_theo_vi_tri": ("ops/cong_cu_test.py",
        "        cac = [x for x in rang_buoc.get(ten, ()) if x[0] < vt]\n",
        "        cac = list(rang_buoc.get(ten, ()))  # đột biến: xuất xứ không theo vị trí\n",
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
    # N46, chieu LOT: module/than lop quay ve luat "rang buoc la thuoc tinh CA pham vi".
    "bn_module_khong_theo_thu_tu": ("ops/bash_nen.py",
        "        truoc = vi_tri if (vi_tri is not None and (la_lop or i == 0)) else None\n",
        "        truoc = None  # đột biến: module và thân lớp không đọc theo thứ tự câu lệnh\n",
        "BASH_NEN", (), "t33_do_phu_cua_cong_do_duoc_THEO_HINH_DANG"),
    # N46, chieu BAT OAN: dem luat thu tu cau lenh sang ca pham vi HAM, noi Python KHONG the.
    "bn_ham_cung_theo_thu_tu": ("ops/bash_nen.py",
        "        truoc = vi_tri if (vi_tri is not None and (la_lop or i == 0)) else None\n",
        "        truoc = vi_tri  # đột biến: phạm vi HÀM cũng đọc theo thứ tự câu lệnh\n",
        "BASH_NEN", (), "t33_do_phu_cua_cong_do_duoc_THEO_HINH_DANG"),
    # N47: `type X[T] = ...` thoi la mot pham vi ⇒ `T` ro ri ra pham vi chua.
    "bn_alias_khong_mo_pham_vi": ("ops/bash_nen.py",
        '    x for x in (getattr(ast, "TypeAlias", None),) if x is not None)\n',
        "    x for x in () if x is not None)  # đột biến: alias generic không mở phạm vi\n",
        "BASH_NEN", (), "t50_PEP695_type_params_phai_duoc_tham_va_phai_CHE_duoc"),
    # N48, lop TRUONG: nhanh LOI nhet duong THO vao `ly_do` (lop `_ra_json` van con).
    "bn_loi_ra_duong_tho": ("ops/bash_nen.py",
        '                                      "ly_do": "không đọc/phân tích được "\n'
        '                                               f"{_duong_bao_cao(rel)}: {e}"}\n',
        '                                      "ly_do": f"không đọc/phân tích được {rel}: {e}"}'
        "  # đột biến: đường THÔ ở lối ra lỗi\n",
        "BASH_NEN", (), "t49_duong_XAU_ra_JSON_HOP_LE_va_NGAY_GO_phai_duoc_DOC"),
    # N48, lop BIEN GIOI: `_ra_json` thoi bao dam ASCII (lop `_duong_bao_cao` van con).
    "bn_json_khong_ascii": ("ops/bash_nen.py",
        "    return json.dumps(bao, ensure_ascii=True, indent=2)\n",
        "    return json.dumps(bao, ensure_ascii=False, indent=2)  # đột biến: biên giới JSON "
        "không còn thuần ASCII\n",
        "BASH_NEN", (), "t49_duong_XAU_ra_JSON_HOP_LE_va_NGAY_GO_phai_duoc_DOC"),
    # N51: cache thoi so van tay ⇒ tra lai phan quyet qua han.
    "bn_cache_khong_van_tay": ("ops/bash_nen.py",
        "        if ds_moi == ds_cu and van_tay_cu == _van_tay_ung_vien(kq_cu[1]):\n",
        "        if ds_moi == ds_cu:  # đột biến: cache không soát lại vân tay tệp\n",
        "BASH_NEN", (), "t51_cache_phai_HET_HIEU_LUC_khi_chinh_TEP_ung_vien_doi"),
    # N51: van tay CHI phu ke thang ⇒ khi khong co ke thang nao thi no thanh hang so.
    "bn_van_tay_chi_ke_thang": ("ops/bash_nen.py",
        '    return tuple((c["duong"], _van_tay_tep(c["duong"])) for c in chan_doan)\n',
        '    return tuple((c["duong"], _van_tay_tep(c["duong"])) for c in chan_doan if c["dat"])'
        "  # đột biến: vân tay bỏ qua ứng viên TRƯỢT\n",
        "BASH_NEN", (), "t51_cache_phai_HET_HIEU_LUC_khi_chinh_TEP_ung_vien_doi"),
    # N49: `assert` tran lai thanh cua hau ra khoi ratchet.
    "ct_bo_nhanh_assert": ("ops/cong_cu_test.py",
        "        elif isinstance(nut, _ast.Assert):\n",
        "        elif False:  # đột biến: `assert` trần không còn là một phép chốt\n",
        "TEP_TEST", _KEM_TEP_TEST, "t39_chi_CA_PHAN_QUYET_duoc_chot_tren_rc_va_trang_thai"),
    # N49: ratchet quay ve khop DUNG chu `rc`, nen doi ten bien la thoat.
    "ct_chi_ten_rc": ("ops/cong_cu_test.py",
        "                    ghi(d.id, vt, ng)\n",
        "                    ghi(d.id, vt, \"khac\")  # đột biến: không đi theo xuất xứ của `_quet`\n",
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
    "bn_dinh_nghia_giai_o_pham_vi_trong": ("ops/bash_nen.py",
        "            for x in ngoai:\n                tham(x, chuoi)\n",
        "            for x in ngoai:\n                tham(x, chuoi_trong)  # đột biến: biểu thức lúc định nghĩa giải ở phạm vi TRONG\n",
        "BASH_NEN", (), "t33_do_phu_cua_cong_do_duoc_THEO_HINH_DANG"),
    # r12 — BON dot bien cho bon mat cua "doc INDEX cho dung" (N32..N35), deu ve `t47`.
    "bn_theo_ref_thay_the": ("ops/bash_nen.py",
        '    env["GIT_NO_REPLACE_OBJECTS"] = "1"\n'
        '    return subprocess.run(["git", "--no-replace-objects", "-C", str(goc), *doi_so],\n',
        '    return subprocess.run(["git", "-C", str(goc), *doi_so],  # đột biến: nghe ref thay thế của MÁY\n',
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
        '            if isinstance(n, _ast.Name) and nguon_tai(n.id, vt) == "ma":\n'
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
}

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
    # r11 — N29 chieu BAT OAN. Ca ba deu la phep CHE hop le ma ban r10 van bao.
    "global_gan_che":  'import subprocess\ndef f():\n    global subprocess\n    subprocess = gia()\nsubprocess.run(["bash"])\n',
    "nonlocal_che":    'def o():\n    import subprocess\n    def i():\n        nonlocal subprocess\n        subprocess = gia()\n    subprocess.run(["bash"])\n',
    "walrus_comprehension_che": 'import subprocess\n[(subprocess := runner) for _ in [0]]\nsubprocess.run(["bash"])\n',
    # r15 — N40 chieu BAT OAN: `:=` trong TRUONG LUC DINH NGHIA che ten o pham vi CHUA.
    "walrus_mac_dinh_che": 'import subprocess\ndef f(x=(subprocess := runner)):\n    pass\nsubprocess.run(["bash"])\n',
    # r15 — N39 chieu BAT OAN: `global x; x = gia()` la mot phep che hop le.
    "global_roi_gan_che": 'import subprocess\ndef f():\n    global subprocess\n    subprocess = gia()\nsubprocess.run(["bash"])\n',
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
    # r16 — N46 chieu NGUOC, BA mat. (a)(b): gan TRUOC loi goi ⇒ ten da bi che that.
    # (c): trong HAM thi luat KHAC — phep gan lam ten thanh cuc bo ngay tu luc BIEN DICH,
    # nen `import` roi goi roi gan van la mo ho. Mat (c) la chot giu cho ban va N46 khong
    # tran sang pham vi ham; go no ra thi `t33` DO.
    "module_gan_TRUOC":    'import subprocess\nsubprocess = runner\nsubprocess.run(["bash"])\n',
    "lop_gan_TRUOC":       'import subprocess\nclass C:\n    subprocess = runner\n    subprocess.run(["bash"])\n',
    "ham_gan_SAU_van_mo_ho": 'def f():\n    import subprocess\n    subprocess.run(["bash"])\n    subprocess = runner\n',
    "module_gan_trong_if":  'import subprocess\nif x:\n    subprocess = runner\nsubprocess.run(["bash"])\n',
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
    # r17 — N53 chieu NGUOC: hai rang buoc HOAN TAT cung mot cho ⇒ van mo ho.
    "gan_day_chuyen_che":   'import subprocess\nsubprocess = other = runner\nsubprocess.run(["bash"])\n',
}


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

    for ten, than in _HINH_DANG_PHU.items():
        bang(bool(_loi_goi_tran(than)),
             f"(1) hình dạng `{ten}` ĐƯỢC KHAI là phủ mà cổng KHÔNG bắt:\n{than}")
    for ten, than in _HINH_DANG_KHONG_PHU.items():
        bang(not _loi_goi_tran(than),
             f"(2) hình dạng `{ten}` được khai là KHÔNG phủ mà cổng lại bắt — nếu đã mở rộng "
             f"được thì phải sửa docstring VÀ chuyển nó sang `_HINH_DANG_PHU`:\n{than}")
    # (1b) `executable=` GHI ĐÈ, không cộng dồn: hai tên `bash` trong MỘT lời gọi là MỘT bản ghi.
    # Chốt riêng vì (1) chỉ hỏi "có bắt không" — hai bản ghi cũng qua (1), và một mục miễn trừ
    # khai theo SỐ LẦN sẽ lệch oan.
    mot = _loi_goi_tran(_HINH_DANG_MOT_BAN_GHI)
    bang(len(mot) == 1,
         f"(1b) `run([\"bash\"], executable=\"bash\")` phải là ĐÚNG MỘT bản ghi, đo được {mot}")
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

    Chạy trong TIẾN TRÌNH CON: ca này đụng `os.environ` và `_CACHE` toàn cục, làm bẩn tiến
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

    Chạy trong TIẾN TRÌNH CON: ca này đụng `os.chdir`, `os.environ` và `_CACHE` toàn cục.

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
        "thuộc tính ca này trói: không có danh sách thì không có phán quyết.",
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

    rang_buoc = {}                      # ten -> [(vi_tri_hoan_tat, nguon)]

    def ghi(ten, vt, nguon):
        if ten:
            rang_buoc.setdefault(ten, []).append((vt, nguon))

    def nguon_tai(ten, vt):
        cac = [x for x in rang_buoc.get(ten, ()) if x[0] < vt]
        return max(cac)[1] if cac else None

    doi = True
    while doi:                          # tới bất động điểm: bí danh nhiều tầng
        doi = False
        truoc = {k: list(v) for k, v in rang_buoc.items()}
        rang_buoc.clear()
        for nut in _ast.walk(cay):
            if isinstance(nut, _ast.FunctionDef):
                for a in (*nut.args.posonlyargs, *nut.args.args, *nut.args.kwonlyargs,
                          nut.args.vararg, nut.args.kwarg):
                    if a is not None:
                        ghi(a.arg, (0, 0), "khac")
            if not isinstance(nut, (_ast.Assign, _ast.AnnAssign, _ast.For, _ast.AsyncFor)):
                continue
            gia = getattr(nut, "value", None) or getattr(nut, "iter", None)
            dich = nut.targets if isinstance(nut, _ast.Assign) else [nut.target]
            vt = _ket(gia) if gia is not None else _ket(nut)
            if gia is None:
                continue

            def nguon_cua(g):
                """Nguồn mà một biểu thức đặt ra, theo bảng ràng buộc của VÒNG TRƯỚC."""
                if la_quet(g):
                    return "bo_doi"
                if (isinstance(g, _ast.Subscript) and la_quet(g.value)
                        and isinstance(g.slice, _ast.Constant)):
                    return {0: "ma", 1: "bao"}.get(g.slice.value, "khac")
                if isinstance(g, _ast.Name):
                    cac = [x for x in truoc.get(g.id, ()) if x[0] < _ket(g)]
                    return max(cac)[1] if cac else "khac"
                if (isinstance(g, _ast.Subscript) and isinstance(g.value, _ast.Name)
                        and isinstance(g.slice, _ast.Constant)):
                    cac = [x for x in truoc.get(g.value.id, ()) if x[0] < _ket(g)]
                    if cac and max(cac)[1] == "bo_doi":
                        return {0: "ma", 1: "bao"}.get(g.slice.value, "khac")
                return "khac"

            ng = nguon_cua(gia)
            for d in dich:
                if isinstance(d, (_ast.Tuple, _ast.List)):
                    # `ma, bao = _quet(…)` — CHỈ phần tử 0 là phán quyết.
                    for k, ph in enumerate(d.elts):
                        if isinstance(ph, _ast.Name):
                            ghi(ph.id, vt,
                                {0: "ma", 1: "bao"}.get(k, "khac") if ng == "bo_doi" else "khac")
                elif isinstance(d, _ast.Name):
                    ghi(d.id, vt, ng)
        if {k: sorted(v) for k, v in rang_buoc.items()} != {k: sorted(v) for k, v in truoc.items()}:
            doi = True

    def cham_phan_quyet(dieu_kien):
        vt = _ket(dieu_kien)
        if any(la_quet(n) for n in _ast.walk(dieu_kien)):
            return True                  # `bang(_quet(…)[0] == 2, …)` — không đi qua tên nào
        for n in _ast.walk(dieu_kien):
            if isinstance(n, _ast.Name) and nguon_tai(n.id, vt) == "ma":
                return True
            if not (isinstance(n, _ast.Subscript) and isinstance(n.slice, _ast.Constant)):
                continue
            khoa = n.slice.value
            g = n.value
            if isinstance(g, _ast.Name):
                ng = nguon_tai(g.id, vt)
                if ng == "bao" and khoa in _TRUONG_TONG_HOP:
                    return True
                if ng == "bo_doi" and khoa == 0:
                    return True
            elif (isinstance(g, _ast.Subscript) and isinstance(g.value, _ast.Name)
                  and isinstance(g.slice, _ast.Constant) and g.slice.value == 1
                  and nguon_tai(g.value.id, vt) == "bo_doi"
                  and khoa in _TRUONG_TONG_HOP):
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
                and nut.func.id in ("bang", "dung") and nut.args:
            dieu_kien = nut.args[0]
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

_MAU_MONG = {"eq_rc": True, "eq_tt": True, "ne_rc": True, "ne_tt": True,
             "rc_bang_0": True, "ngoai_ds": True,
             "assert_tran": True, "assert_tt": True, "bi_danh": True,
             "lay_phan_tu_0": True, "goi_long": True,
             "xuat_xu_bo_doi": True, "xuat_xu_bao_doi": True,
             "chot_truoc_khi_ghi_de": True,
             "truong_co_che": False, "lech_oid": False,
             "rc_gieo_san": False, "chuoi_trung_ten": False, "bi_danh_ghi_de": False,
             "bo_doi_truong_co_che": False,
             "assert_thong_diep": False, "khong_quet": False}


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
        bq = _bash_nen_voi_chua_chuyen(tmp, {}, anh_chup={anh_gia: (2, "ảnh chụp giả của t40")})
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

    CHỐT (3) LÀ CHIỀU NGƯỢC và nó BẮT BUỘC: cách chữa rẻ tiền là bỏ cache đi, và làm thế thì
    ca này vẫn xanh trong khi mỗi lượt `quet` lại đẻ thêm hàng chục tiến trình con. Nên phải
    đo rằng cache VẪN LÀ cache khi không có gì đổi.

    KHE CÒN LẠI, khai thẳng: tệp vẫn có thể bị thay GIỮA lúc so vân tay và lúc thật sự chạy.
    Đó là đua ở mức hệ điều hành; vân tay thu hẹp cửa sổ chứ không đóng được nó.
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
        cu_env = {k: os.environ.get(k) for k in ("CONG_CU_BASH", "PATH")}
        # `finally` phải khôi phục CẢ HAI kể cả khi chúng vốn VẮNG — chốt (5) gỡ `PATH`.
        try:
            os.environ["CONG_CU_BASH"] = str(w)
            os.environ["PATH"] = str(rong)          # cô lập: KHÔNG ứng viên nào khác
            m["_CACHE"].clear()

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

            m["_CACHE"].clear()
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

            m["_CACHE"].clear()
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
            m["_CACHE"].clear()
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

            # (5) N57 (r17) — `PATH` VẮNG ≠ `PATH` RỖNG, và luật ấy là của HỆ ĐIỀU HÀNH.
            #     `os.get_exec_path()`/`execvp` dùng `os.defpath` khi biến VẮNG; một `PATH=""`
            #     tường minh nghĩa là "đừng tìm ở đâu cả". Bản trước gộp hai ca vào `""` nên
            #     trên máy không đặt `PATH` thì `ung_vien()` trả `[]` và cổng báo
            #     KHONG_DO_DUOC — trong khi `subprocess.run(["bash"])` trên CHÍNH máy ấy vẫn
            #     tìm thấy `/bin/bash`. `None ≠ ""`, cùng họ với `None ≠ False`.
            os.environ.pop("CONG_CU_BASH", None)
            os.environ.pop("PATH", None)
            vang = m["ung_vien"]()
            rong = m["ung_vien"](path="")
            bang(bool(vang) and not rong,
                 f"(5) `PATH` VẮNG cho {len(vang)} ứng viên và `PATH=\"\"` cho {len(rong)} — "
                 f"mong VẮNG khác rỗng (lùi về `os.defpath` = {os.defpath!r}) và RỖNG tường "
                 f"minh thì rỗng. Gộp hai ca lại là để cổng báo KHÔNG ĐO ĐƯỢC trên một máy "
                 f"chạy `bash` được.")

            bang(dau > 0 and sau == dau,
                 f"(3) CHIỀU NGƯỢC — cache đã CHẾT: lần đầu {dau} phép thử năng lực, sau 20 "
                 f"lượt nữa thành {sau}. Vá bằng cách bỏ cache thì (1) và (2) vẫn xanh trong "
                 f"khi mỗi lượt `quet` đẻ thêm hàng chục tiến trình con. Vân tay tệp phải "
                 f"làm cache HẾT HIỆU LỰC ĐÚNG LÚC, không phải làm nó thôi tồn tại.")
        finally:
            for k, v in cu_env.items():
                if v is None:
                    os.environ.pop(k, None)
                else:
                    os.environ[k] = v
            m["_CACHE"].clear()


@ca
def t49_duong_XAU_ra_JSON_HOP_LE_va_NGAY_GO_phai_duoc_DOC():
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
    def _g(d, *a):
        return subprocess.run(["git", "-C", str(d)] + list(a), capture_output=True,
                              text=True, timeout=60)

    def _kho(tmp, ten):
        d = tmp / ten
        (d / "ops").mkdir(parents=True)
        for l in (["init", "-q"], ["config", "user.email", "t@t"], ["config", "user.name", "t"]):
            subprocess.run(["git", "-C", str(d)] + l, capture_output=True, timeout=60)
        return d

    BAN = 'import shutil\nb = shutil.which("bash")\n'
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        bq = _bash_nen_voi_chua_chuyen(tmp, {})

        # (2) đường mang byte xấu ⇒ JSON vẫn đọc được bằng UTF-8 nghiêm. Chiều ngược: đường
        #     Unicode thường vẫn nguyên vẹn.
        d = _kho(tmp, "duong")
        try:
            (d / "ops" / b"xau_\xff.py".decode("utf-8", "surrogateescape")).write_text(
                BAN, encoding="utf-8")
        except OSError as e:
            raise BoQuaMoiTruong(f"nền này không đặt được tên tệp có byte thô: {e}") from e
        (d / "ops" / "bình_thường.py").write_text(BAN, encoding="utf-8")
        _g(d, "add", "-A")
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
        (d_loi / "ops" / b"hong_\xff.py".decode("utf-8", "surrogateescape")).write_text(
            "def f(:\n", encoding="utf-8")
        _g(d_loi, "add", "-A")
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

        # (2d) N54 (r17) — PHÉP HIỂN THỊ PHẢI ĐƠN ÁNH, và khoá báo cáo thì không dùng nó.
        #      Đặc tả r15 tự khai chỗ chưa đo: *"hai đường khác nhau về byte CÓ THỂ in ra
        #      giống nhau — chưa đo trường hợp ấy"*. Vòng 11 đo được: `ops/bad_<0xff>.py` và
        #      một đường chứa đúng bốn ký tự ASCII `\`,`x`,`f`,`f` cùng ra `ops/bad_\xff.py`.
        #      Chuỗi ấy LÀ KHOÁ của `co_loi_goi_tran`, nên một tệp ĐÈ vị trí của tệp kia và
        #      hạn ngạch đếm sai — một vi phạm tàng hình, đúng lớp `t48` đã gặp với `\r`/`\n`.
        d_va = _kho(tmp, "vacham")
        hai = [b"ops/va_\xff.py".decode("utf-8", "surrogateescape"), "ops/va_\\xff.py"]
        try:
            for ten in hai:
                (d_va / ten).write_text(BAN, encoding="utf-8")
        except OSError as e:
            raise BoQuaMoiTruong(f"nền này không đặt được hai tên ấy cạnh nhau: {e}") from e
        _g(d_va, "add", "-A")
        mv = runpy.run_path(str(bq))
        _, bao_va = mv["quet"](d_va)
        khoa = bao_va.get("co_loi_goi_tran") or {}
        bang(len(khoa) == 2,
             f"(2d) HAI đường khác nhau về byte chỉ còn MỘT khoá trong báo cáo: "
             f"{sorted(map(repr, khoa))} — phép hiển thị không đơn ánh mà lại được dùng làm "
             f"khoá, nên một tệp ĐÈ tệp kia và hạn ngạch đếm hụt. Khoá phải giữ đường NGUYÊN "
             f"VẸN; `_ra_json` lo phần an toàn ở biên giới.")
        bang(mv["_duong_bao_cao"](hai[0]) != mv["_duong_bao_cao"](hai[1]),
             f"(2d) `_duong_bao_cao` vẫn KHÔNG đơn ánh: "
             f"{mv['_duong_bao_cao'](hai[0])!r} == {mv['_duong_bao_cao'](hai[1])!r}")
        bang(mv["_duong_bao_cao"]("ops/bình_thường.py") == "ops/bình_thường.py",
             "(2d) chiều ngược: đường Unicode THƯỜNG phải nguyên vẹn sau khi làm đơn ánh")

        # (3) NGÀY GỠ là một HẠN đọc được, không phải chữ trong lý do.
        d = _kho(tmp, "ngay")
        (d / "ops" / "no_cu.py").write_text(BAN, encoding="utf-8")
        _g(d, "add", "-A")
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


def _in_tu_kiem_cong_that():
    """Cửa tiến trình con cho `t45`: chạy phép nối cổng trên MỘT gốc cho trước rồi in ra."""
    i = sys.argv.index("--tu-kiem-cong-that")
    goc = sys.argv[i + 1]
    bq = sys.argv[i + 2] if len(sys.argv) > i + 2 else None
    loi, dong = _cong_tren_cay_that(Path(goc), bq)
    print("KQ " + json.dumps([loi, dong], ensure_ascii=False))
    sys.exit(0 if loi == 0 else 9)


def main() -> int:
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
    print(f"\nBÁN KÍNH ĐỘT BIẾN ({len(DOT_BIEN)} đột biến, mỗi ca đúng một"
          + (f"; LOẠI {len(do_o_nen)} ca đỏ ở nền" if do_o_nen else "") + "):")
    for ten_db, cfg in DOT_BIEN.items():
        ca_dich = cfg[-1]
        try:
            ket, _ = _do_ban_kinh(ten_db, bo_qua_ca=do_o_nen)
        except AssertionError as ex:
            print(f"  ĐỎ  {ten_db}: {ex}")
            loi_db += 1
            continue
        cac_dong, loi = _ket_luan_ban_kinh(ten_db, ca_dich, ket, len(CA), do_o_nen)
        for dong in cac_dong:
            print(dong)
        loi_db += loi
    print(f"\nSỐ LIỆU: ca={len(CA)} · đột biến={len(DOT_BIEN)} · lỗi đột biến={loi_db}"
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


if __name__ == "__main__":
    if "--tu-kiem-ban-kinh" in sys.argv[1:]:
        _in_tu_kiem_ban_kinh()
        sys.exit(0)
    if "--tu-kiem-nen-do" in sys.argv[1:]:
        _in_tu_kiem_nen_do()
        sys.exit(0)
    if "--tu-kiem-tien-kiem" in sys.argv[1:]:
        _in_tu_kiem_tien_kiem()
        sys.exit(0)
    if "--tu-kiem-dong-ho" in sys.argv[1:]:
        _in_tu_kiem_dong_ho()
        sys.exit(0)
    if "--tu-kiem-luat-phan-quyet" in sys.argv[1:]:
        _in_tu_kiem_luat_phan_quyet()
        sys.exit(0)
    if "--tu-kiem-cong-that" in sys.argv[1:]:
        _in_tu_kiem_cong_that()
    sys.exit(main())
