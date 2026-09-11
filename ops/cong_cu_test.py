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
CAI_SH = HERE / "cai_cong_cu.sh"
sys.path.insert(0, str(HERE))
import lease_publish_test as lpt  # noqa: E402 — tái dùng _goi_actionlint_gia/_bam_tep

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
    bash = shutil.which("bash")
    if not bash:
        raise BoQuaMoiTruong("KHÔNG ĐO ĐƯỢC: thiếu `bash` để chạy ops/cai_cong_cu.sh")
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
                          env=dict(os.environ, PATH=str(d), CONG_CU_BASH=shutil.which("bash") or ""))
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

_PHU = ("ops/cong_cu.yaml", "ops/canary/actionlint_shellcheck.yml")

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
    "t22_bash_lay_ca_system_root": ("ops/cong_cu.py",
        "        if u.is_file() and not duoi_system_root(u):\n",
        "        if u.is_file():  # đột biến: không loại SystemRoot\n",
        "SCRIPT", _PHU, "t22_bash_windows_khong_lay_bo_phong_wsl_o_system_root"),
    # #445 gen 4 — bỏ cắt CR khi đọc tên công cụ: stdout CRLF của python lại thành 'rg\r'.
    "t23_bo_cat_CR_ten_cong_cu": ("ops/cai_cong_cu.sh",
        "    cong_cu=\"${cong_cu%$'\\r'}\"\n",
        "    :  # đột biến: không cắt CR\n",
        "CAI_SH", ("ops/cong_cu.py", "ops/cai_actionlint.sh") + _PHU,
        "t23_batch_chiu_duoc_stdout_CRLF_cua_python_windows"),
    "t24_sai_pham_vi": ("ops/cong_cu.py",
        '        pham_vi = "mot-cong-cu"\n',
        '        pham_vi = "sai-pham-vi"  # đột biến\n',
        "SCRIPT", _PHU, "t24_pham_vi_mot_cong_cu_va_toan_bo"),
}

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
        return "tin_dung_gia", f"{type(ex).__name__}: {ex}"
    finally:
        _CA_DANG_CHAY = None

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
def t22_bash_windows_khong_lay_bo_phong_wsl_o_system_root():
    """`_bash_windows` phải bỏ qua `%SystemRoot%\\System32\\bash.exe` (bộ phóng WSL) dù nó
    đứng ĐẦU PATH, và tìm được Git Bash cạnh `git` khi PATH không có bash nào khác.

    Chạy trên mọi nền: hàm nhận tham số ép PATH/SystemRoot/git, còn `_chay` chỉ gọi nó
    khi `os.name == "nt"` — mặt ấy do lane windows-latest đo thật."""
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        sr = tmp / "Windows"; sys32 = sr / "System32"
        wsl = bin_gia(sys32, "bash.exe", "#!/bin/sh\necho 'Windows Subsystem for Linux has no installed distributions.'\nexit 1\n")
        git_dir = tmp / "Git"; gb_usr = git_dir / "usr" / "bin"; gb_bin = git_dir / "bin"
        gb1 = bin_gia(gb_usr, "bash.exe", "#!/bin/sh\necho 'GNU bash, version 5.2.37(1)-release (x86_64-pc-msys)'\n")
        gb2 = bin_gia(gb_bin, "bash.exe", "#!/bin/sh\necho 'GNU bash, version 5.2.37(1)-release (x86_64-pc-msys)'\n")
        git_exe = bin_gia(git_dir / "cmd", "git.exe", "#!/bin/sh\necho 'git version 2.55.0.windows.5'\n")
        ma = (
            "import runpy, sys, os\n"
            f"m = runpy.run_path({str(SCRIPT)!r})\n"
            "f = m['_bash_windows']\n"
            f"sr = {str(sr)!r}; s32 = {str(sys32)!r}; usr = {str(gb_usr)!r}; g = {str(git_exe)!r}; pf = {str(tmp / 'khong-co')!r}\n"
            "sep = os.pathsep\n"
            # (a) System32 đứng ĐẦU PATH, Git Bash đứng sau ⇒ phải chọn Git Bash
            "print('A', f(path=s32 + sep + usr, system_root=sr, program_files=pf, git=''))\n"
            # (b) PATH CHỈ có System32, không bash nào khác; `git` biết ⇒ suy Git Bash cạnh git
            "print('B', f(path=s32, system_root=sr, program_files=pf, git=g))\n"
            # (c) không có gì ngoài WSL ⇒ None, KHÔNG đoán
            "print('C', f(path=s32, system_root=sr, program_files=pf, git=''))\n"
            # (d) đối chứng: SystemRoot rỗng thì không có gì để loại, bash đầu PATH được chọn
            "print('D', f(path=usr, system_root='', program_files=pf, git=''))\n"
        )
        env = dict(os.environ); env.pop("CONG_CU_BASH", None)
        p = subprocess.run([sys.executable, "-c", ma], env=env, cwd=GOC,
                           capture_output=True, text=True, timeout=60)
        # GIÀN GIÁO, không phải chốt nghiệp vụ: đoạn `python -c` trên do CHÍNH ca này
        # soạn ra. Nó chết ⇒ bốn phép so A/B/C/D bên dưới CHƯA CHẠY ⇒ `dung()`, để
        # không ai được cấp tín dụng giết cho một crash vô can (R5-01).
        dung(p.returncode == 0, f"gọi _bash_windows hỏng: rc={p.returncode}\n{p.stdout}\n{p.stderr}")
        kq = dict(l.split(" ", 1) for l in p.stdout.splitlines() if " " in l)
        # So sau khi resolve CẢ HAI vế: trên windows-latest, tempfile trả tên ngắn 8.3
        # (`RUNNER~1`) còn `_bash_windows` resolve() thành `runneradmin` (run 33630217222, B đỏ oan).
        chuan = lambda x: os.path.normcase(str(Path(x).resolve())) if x and x != "None" else x
        bang(chuan(kq.get("A")) == chuan(gb1), f"(A) System32 đứng đầu PATH mà chọn {kq.get('A')!r}, mong {str(gb1)!r}")
        bang(chuan(kq.get("B")) == chuan(gb2), f"(B) không suy được Git Bash cạnh git: {kq.get('B')!r}, mong {str(gb2)!r}")
        bang(kq.get("C") == "None", f"(C) chỉ có WSL mà vẫn trả {kq.get('C')!r} — đoán thay vì hỏng thật")
        bang(chuan(kq.get("D")) == chuan(gb1), f"(D) đối chứng SystemRoot rỗng: {kq.get('D')!r}")
        bang(str(wsl) not in p.stdout, f"bộ phóng WSL lọt vào kết quả: {p.stdout}")

# --------------------------------------------------------------- T16/T17 (#391)
# LUẬT: thêm một công cụ/gói vào bất kỳ mã nào của kho thì phải khai nó trong
# `ops/cong_cu.yaml` kèm lệnh cài cho MỌI nền mà cổng chạy trên đó. Luật viết trong
# tài liệu KHÔNG CHẠY — nên nó nằm ở đây, dạng ca test.
#
# Sinh ra vì `from jsonschema` vào kho ở `47a50395` mà không ai khai: `gate` ĐỎ liên
# tục từ đó với `ModuleNotFoundError`, và bốn vòng cross-review không thấy vì cả bốn
# chạy trong container có sẵn gói.

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
    bash = shutil.which("bash")
    if not bash:
        raise BoQuaMoiTruong("KHÔNG ĐO ĐƯỢC batch: thiếu bash")
    with tempfile.TemporaryDirectory(prefix="cong-cu-batch-") as td:
        root = Path(td); ops = root / "ops"; ops.mkdir(); out = root / "installed"
        fake_bin = root / "fake-bin"; fake_bin.mkdir(); pip_ready = root / "pip-ready"
        shutil.copy2(CAI_SH, ops / "cai_cong_cu.sh")
        shutil.copy2(SCRIPT, ops / "cong_cu.py")
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
        (only / "python3").symlink_to(sys.executable)
        bk = ghi_ban_ke(root, {"python": {"bat_buoc": True, "ban_ghim": None,
            "probe": [{"ten": "mac_dinh", "lenh": ["python", "--version"],
                       "regex": r"Python\s+(\d+\.\d+\.\d+)"}]}})
        rc, out, _ = chay("kiem-tra", "--ban-ke", str(bk), "--json",
                          env=dict(os.environ, PATH=str(only)))
        bang(rc == 0 and '"trang_thai_tong": "DAT"' in out,
             f"máy chỉ có python3 bị probe alias python chặn: rc={rc}\n{out}")



@ca
def t24_pham_vi_mot_cong_cu_va_toan_bo():
    """Phạm vi một công cụ và toàn bộ phải có đủ pham_vi, canary_da_quet, ghi_chu_pham_vi."""
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        bk, env = bk_don(tmp, "cong-cu-t24", "#!/bin/sh\necho 1.0.0\n", ban_ghim="1.0.0")
        rc, out, _ = chay("kiem-tra", "--ban-ke", str(bk), "--json", env=env)
        bang(rc == 0, f"rc={rc} thay vi 0")
        bc = json.loads(out)
        bang(bc.get("pham_vi") == "toan-bo", f"sai pham_vi toan-bo: {bc.get('pham_vi')}")
        bang(bc.get("canary_da_quet") is True, "sai canary_da_quet toan-bo")
        bang("ghi_chu_pham_vi" in bc, "thieu ghi_chu_pham_vi")
        rc, out, _ = chay("kiem-tra", "--chi", "cong-cu-t24", "--ban-ke", str(bk), "--json", env=env)
        bang(rc == 0, f"rc={rc} thay vi 0")
        bc = json.loads(out)
        bang(bc.get("pham_vi") == "mot-cong-cu", f"sai pham_vi mot-cong-cu: {bc.get('pham_vi')}")
        bang(bc.get("canary_da_quet") is False, "sai canary_da_quet mot-cong-cu")
        bang("ghi_chu_pham_vi" in bc, "thieu ghi_chu_pham_vi")


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


def main() -> int:
    batch_behavior_test()
    python_alias_behavior_test()
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
    for ten, ly in bo_qua:
        print(f"  BỎ QUA {ten}: {ly}")
    for ten, ly in hong:
        print(f"  ĐỎ  {ten}: {ly}")
    print(f"\ncong_cu_test: {qua}/{len(CA) - len(bo_qua)} đạt; tổng={len(CA)}, bỏ qua={len(bo_qua)}")

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
        tt_dich = ket[ca_dich][0]
        chet = sorted(t for t, (tt, _) in ket.items() if tt in ("giet_that", "tin_dung_gia"))
        oan = [t for t in chet if t != ca_dich]
        bk = f"{len(chet)}/{len(CA)}"
        gia = sorted(t for t, (tt, _) in ket.items() if tt == "tin_dung_gia")
        if tt_dich == "bo_qua":
            print(f"  KHÔNG_ĐO_ĐƯỢC {ten_db}: đích '{ca_dich}' bị BỎ QUA — {ket[ca_dich][1]}")
            loi_db += 1
        elif tt_dich == "tin_dung_gia":
            print(f"  ĐỎ  {ten_db}: TÍN DỤNG GIẢ — đích '{ca_dich}' chết KHÔNG PHẢI bằng chốt của nó: "
                  f"{ket[ca_dich][1]}")
            loi_db += 1
        elif tt_dich != "giet_that":
            print(f"  ĐỎ  {ten_db}: đích '{ca_dich}' vẫn XANH ⇒ đột biến không giết được gì")
            loi_db += 1
        elif gia:
            print(f"  ĐỎ  {ten_db}: ca {gia} chết bằng lỗi VÔ CAN (tín dụng giả) ⇒ bán kính không đọc được")
            loi_db += 1
        elif oan:
            print(f"  ĐỎ  {ten_db}: giết THÊM {oan} ngoài đích '{ca_dich}' (bán kính {bk}) ⇒ trói nhầm thứ")
            loi_db += 1
        else:
            print(f"  ok  {ten_db} → giết đúng '{ca_dich}' · bán kính {bk}")
    print(f"\nSỐ LIỆU: ca={len(CA)} · đột biến={len(DOT_BIEN)} · lỗi đột biến={loi_db}")
    return 1 if (hong or loi_db) else 0

if __name__ == "__main__":
    sys.exit(main())
