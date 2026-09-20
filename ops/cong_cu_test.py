#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""T1..T8 + chính sách canary (#290, sha256 b1b7e3b0…) cho cong_cu.py+cai_cong_cu.sh. Gọi
CHÍNH lệnh qua subprocess (không import) — doctrine `lease_publish_test.py`."""
from __future__ import annotations

import json, os, shutil, subprocess, sys, tempfile
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
    "t34_khoa_cache_bo_moi_truong": ("ops/bash_nen.py",
        "    khoa = json.dumps([sorted(ep.items()), bool(tat_ca), sorted(moi_truong.items())],\n"
        "                      default=str)\n",
        "    khoa = json.dumps([sorted(ep.items()), bool(tat_ca)], default=str)  # đột biến\n",
        "BASH_NEN", (), "t34_cache_tim_bash_phai_theo_doi_MOI_TRUONG"),
    # Thu pham vi ve `ops/**` => ban sao thu tu ngoai hang rao lai lot. `t35` chot (1) DO.
    "t35_thu_pham_vi_ve_ops": ("ops/bash_nen.py",
        "    thu_muc = goc\n",
        '    thu_muc = goc / "ops"  # đột biến: thu phạm vi về `ops/**` như bản r3\n',
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
        "    moi = {t: d for t, d in co_loi_goi.items()\n"
        "           if t not in CHO_PHEP and t not in CHUA_CHUYEN}\n",
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

def _ket_luan_ban_kinh(ten_db, ca_dich, ket, tong_ca):
    """Đọc một lượt đo bán kính thành (các_dòng_in, số_lỗi). Hàm THUẦN, không in, không I/O.

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
    tt_dich = ket[ca_dich][0]
    chet = sorted(t for t, (tt, _) in ket.items() if tt in ("giet_that", "tin_dung_gia"))
    oan = [t for t in chet if t != ca_dich]
    bk = f"{len(chet)}/{tong_ca}"
    gia = sorted(t for t, (tt, _) in ket.items() if tt == "tin_dung_gia")

    if tt_dich == "bo_qua":
        dau = [f"  KHÔNG_ĐO_ĐƯỢC {ten_db}: đích '{ca_dich}' bị BỎ QUA — {ket[ca_dich][1]}"]
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


def _do_ban_kinh(ten_dot_bien):
    tep, tim, thay, bp, phu_thuoc, ca_dich = DOT_BIEN[ten_dot_bien]
    cay, dich = _dung_cay_dot_bien(ten_dot_bien, tep, tim, thay, phu_thuoc)
    g, cu = globals(), globals()[bp]
    g[bp] = cay if bp == "GOC" else dich
    try:
        return {fn.__name__: _chay_1_ca(fn) for fn in CA}, ca_dich
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


def _quet(goc, bo_quet=None) -> tuple:
    """`bo_quet` cho phép chạy MỘT BẢN SAO của `bash_nen.py` thay vì bản thật — xem
    `_bash_nen_co_chua_chuyen`. Mặc định vẫn là bản thật, nên mọi ca cũ không đổi nghĩa."""
    p = subprocess.run([sys.executable, str(bo_quet or BASH_NEN), "quet", "--root", str(goc),
                        "--json"], cwd=GOC, capture_output=True, text=True, timeout=120)
    dung(p.stdout.strip().startswith("{"),
         f"`quet --json` không in JSON: rc={p.returncode}\n{p.stdout}\n{p.stderr}")
    return p.returncode, json.loads(p.stdout)


_RATCHET_GIA = "ops/muc_ratchet_gia_t26.py"


def _bash_nen_voi_chua_chuyen(tmp: Path, muc: dict, ten="bash_nen_tuy_bien.py") -> Path:
    """Bản sao `bash_nen.py` với `CHUA_CHUYEN` đặt theo `muc`. Trả đường dẫn bản ấy.

    Vì sao cần: các ca dựng cây GIẢ không thể thoả một `CHUA_CHUYEN` khoá theo đường dẫn
    THẬT của kho — chiều ngược của ratchet sẽ báo "mục đã sạch" và làm nền ĐỎ oan. Ca phải
    đo LUẬT của cổng, không đo danh sách hiện thời.
    """
    than = Path(BASH_NEN).read_text(encoding="utf-8")
    i = than.index("CHUA_CHUYEN = {")
    j = than.index("\n}\n", i) + len("\n}\n") if than[i:].startswith("CHUA_CHUYEN = {\n") \
        else than.index("\n", i) + 1
    ban = tmp / ten
    ban.write_text(than[:i] + f"CHUA_CHUYEN = {muc!r}\n" + than[j:], encoding="utf-8")
    return ban


def _bash_nen_co_chua_chuyen(tmp: Path) -> Path:
    """Bản sao `bash_nen.py` có `CHUA_CHUYEN` chứa ĐÚNG MỘT mục GIẢ.

    Từ r4 nó uỷ quyền cho `_bash_nen_voi_chua_chuyen`: mỏ neo cũ (`CHUA_CHUYEN = {}`) biến
    mất khi r4 nạp bốn mục thật vào danh sách, và một helper neo theo HÌNH DẠNG NGUỒN sẽ gãy
    mỗi lần danh sách đổi. Neo theo TÊN BIẾN thì không.
    """
    return _bash_nen_voi_chua_chuyen(tmp, {_RATCHET_GIA: "mục giả của t26"},
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
        bang(rc == 0 and bao["trang_thai"] == "DAT",
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
}
_HINH_DANG_KHONG_PHU = {
    "shell_true":      'import subprocess\nsubprocess.run("bash -c x", shell=True)\n',
    "os_system":       'import os\nos.system("bash -c x")\n',
    "bien_trung_gian": 'import shutil\nt = "bash"\nb = shutil.which(t)\n',
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
    """Đặt `CONG_CU_BASH` SAU lần gọi đầu thì lần sau phải THẤY, không bị cache nuốt.

    SINH TỪ CROSS-REVIEW (finding F3). `ung_vien()` đọc `CONG_CU_BASH`/`PATH`/`SystemRoot`/
    `ProgramFiles` từ `os.environ` khi tham số là `None`, nhưng khoá cache cũ là `[[], false]`
    — chỉ `ep` và `tat_ca`. Đo được: gọi `tim_bash()`, đặt `CONG_CU_BASH` sang một bash THẬT ở
    đường khác, gọi lại ⇒ vẫn trả đường CŨ, **không một dòng cảnh báo**. Nút ghi đè mà chính
    module tự khai bị chính cache của nó nuốt.

    Chạy trong TIẾN TRÌNH CON: ca này đụng `os.environ` và `_CACHE` toàn cục, làm bẩn tiến
    trình chạy suite thì các ca sau đo nhầm.
    """
    ma = ("import json, os, shutil, sys, tempfile, runpy\n"
          f"m = runpy.run_path({str(BASH_NEN)!r})\n"
          "that, _ = m['tim_bash']()\n"
          "if not that:\n"
          "    print('KQ ' + json.dumps(['BO_QUA', 'khong co bash nao dung duoc'])); raise SystemExit(0)\n"
          "tmp = tempfile.mkdtemp(); khac = os.path.join(tmp, 'bash')\n"
          "shutil.copy2(that, khac); os.chmod(khac, 0o755)\n"
          "os.environ['CONG_CU_BASH'] = khac\n"
          "sau, _ = m['tim_bash']()\n"
          "print('KQ ' + json.dumps(['OK', that, khac, sau]))\n")
    p = subprocess.run([sys.executable, "-c", ma], cwd=GOC, capture_output=True,
                       text=True, timeout=180)
    dung(p.returncode == 0 and "KQ " in p.stdout,
         f"giàn giáo hỏng: rc={p.returncode}\n{p.stdout}\n{p.stderr}")
    kq = json.loads([l for l in p.stdout.splitlines() if l.startswith("KQ ")][-1][3:])
    if kq[0] == "BO_QUA":
        raise BoQuaMoiTruong(f"KHÔNG_ĐO_ĐƯỢC: {kq[1]}")
    _, truoc, khac, sau = kq
    bang(sau == khac,
         f"`CONG_CU_BASH` đặt SAU lần gọi đầu bị cache NUỐT: trước={truoc!r}, đặt={khac!r}, "
         f"nhận={sau!r}. Khoá cache phải gồm môi trường (#570 r4 N19).")


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
        bang(rc == 0, f"NỀN phải SẠCH mà rc={rc}: {bao.get('ly_do')}")
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
        anh = cay / "ops" / "reviews"
        anh.mkdir(parents=True)
        (anh / "ban_cu.py").write_text('import shutil\nb = shutil.which("bash")\n',
                                       encoding="utf-8")
        rc, bao = _quet(cay, bq)
        bang(rc == 0 and bao["trang_thai"] == "DAT",
             f"(2) `ops/reviews/` là ảnh chụp ĐÔNG CỨNG, không được làm cổng đỏ: rc={rc} "
             f"{bao.get('ly_do')}")
        bang("ops/reviews/ban_cu.py" not in (bao.get("co_loi_goi_tran") or {}),
             f"(2) `ops/reviews/` phải được BỎ QUA, không phải được tha ở khâu lọc: "
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

    loi_db = _tu_kiem_phan_hang()
    loi_db += _tu_kiem_gian_giao()
    print(f"\nBÁN KÍNH ĐỘT BIẾN ({len(DOT_BIEN)} đột biến, mỗi ca đúng một):")
    for ten_db, cfg in DOT_BIEN.items():
        ca_dich = cfg[-1]
        try:
            ket, _ = _do_ban_kinh(ten_db)
        except AssertionError as ex:
            print(f"  ĐỎ  {ten_db}: {ex}")
            loi_db += 1
            continue
        cac_dong, loi = _ket_luan_ban_kinh(ten_db, ca_dich, ket, len(CA))
        for dong in cac_dong:
            print(dong)
        loi_db += loi
    print(f"\nSỐ LIỆU: ca={len(CA)} · đột biến={len(DOT_BIEN)} · lỗi đột biến={loi_db}"
          f" · tiền kiểm bỏ qua={len(tien_kiem_bo_qua)}")
    # Tien kiem bi bo qua KEO ma thoat khac 0. `KHONG_DO_DUOC` khong duoc lang le thanh XANH —
    # `None != False`. No chi thoi giet CA SUITE, chu khong thoi la mot tin hieu.
    return 1 if (hong or loi_db or tien_kiem_bo_qua) else 0

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
    if "--tu-kiem-tien-kiem" in sys.argv[1:]:
        _in_tu_kiem_tien_kiem()
        sys.exit(0)
    if "--tu-kiem-dong-ho" in sys.argv[1:]:
        _in_tu_kiem_dong_ho()
        sys.exit(0)
    sys.exit(main())
