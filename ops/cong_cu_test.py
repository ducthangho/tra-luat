#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""T1..T8 (đặc tả đóng băng #290, sha256 b1b7e3b0…) cho cong_cu.py+cai_cong_cu.sh. Gọi
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

def bang(dk, msg):
    if not dk: raise AssertionError(msg)

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
    with tempfile.TemporaryDirectory() as tmp:
        chi_al = Path(tmp) / "chi-al"
        chi_al.mkdir()
        shutil.copy2(al, chi_al / Path(al).name); (chi_al / Path(al).name).chmod(0o755)
        rc, out, _ = chay("kiem-tra", "--json", env=dict(os.environ, PATH=str(chi_al)))
        bang("SUY_GIAM" in out, f"shellcheck cô lập khỏi PATH mà canary không SUY_GIẢM: "
                                 f"rc={rc}\n{out[:500]}")
        bang(rc != 0, "canary SUY_GIẢM phải kéo tổng thể khỏi ĐẠT (rc=0)")

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
        "cài PyYAML (bộ cổng đăng lease cần)": (
            "python -m pip install --quiet PyYAML==6.0.3",),
        "cài actionlint cho G5": ("bash ops/cai_actionlint.sh",),
    }
    uses_setup = {"actions/checkout@v4", "actions/setup-python@v5"}
    for i, b in enumerate(buoc[:idx_kiem[0]]):
        if b.get("uses") in uses_setup and "run" not in b: continue
        lenh = tuple(x.strip() for x in str(b.get("run", "")).splitlines()
                     if x.strip() and not x.lstrip().startswith("#"))
        bang(lenh_setup.get(b.get("name")) == lenh,
             f"bước {i + 1} trước G5 không thuộc allowlist setup: '{b.get('name')}' / {lenh}")

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
def t12_canary_bat_buoc_thieu_fixture_va_optional_khong_canary():
    """V2 + đối chứng: canary kế thừa requiredness; optional không khai canary vẫn hợp lệ."""
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp); d = tmp / "bin"; bin_gia(d, "actionlint", "#!/bin/sh\necho 1.7.7\n")
        bk = ghi_ban_ke(tmp, {"actionlint": {"bat_buoc": True, "ban_ghim": "1.7.7",
            "probe": mot_probe("actionlint"), "canary": "fixture-khong-ton-tai-t12"}})
        rc, out, _ = chay("kiem-tra", "--ban-ke", str(bk), env=moi_truong(d))
        bang(json.loads(out)["trang_thai_tong"] == "KHONG_DO_DUOC" and '"bat_buoc": true' in out,
             f"canary bắt buộc thiếu fixture bị nuốt: {rc}\n{out}")
        d_bk = yaml.safe_load(bk.read_text(encoding="utf-8"))
        d_bk["cong_cu"]["actionlint"]["canary_bat_buoc"] = False
        bk.write_text(yaml.safe_dump(d_bk), encoding="utf-8")
        bang(chay("kiem-tra", "--ban-ke", str(bk), env=moi_truong(d))[0] == 0,
             "canary khai advisory tường minh bị chặn oan")
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
            "probe": mot_probe("actionlint"), "canary": "actionlint_shellcheck"}})
        rc, out, _ = chay("kiem-tra", "--ban-ke", str(bk), env=dict(os.environ, PATH=str(d)))
        bang(json.loads(out)["trang_thai_tong"] == "KHONG_DO_DUOC" and "khong goi duoc" in out,
             f"canary mất executable bị nuốt: {rc}\n{out}")

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
        "CAI_SH", ("ops/cong_cu.py",) + _PHU, "t5_cai_cong_cu_khong_thoat_som_khi_da_co_tren_PATH"),
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
    "t12_mat_requiredness_khi_thieu_fixture": ("ops/cong_cu.py",
        '        return {**goc, "trang_thai": KHONG_DO_DUOC, "chi_tiet": f"thieu fixture \'{fixture}\'"}\n',
        '        return {"ten": ten_canary, "trang_thai": KHONG_DO_DUOC, "chi_tiet": f"thieu fixture \'{fixture}\'"}  # đột biến\n',
        "SCRIPT", _PHU, "t12_canary_bat_buoc_thieu_fixture_va_optional_khong_canary"),
    "t13_mat_requiredness_khi_tool_bien_mat": ("ops/cong_cu.py",
        '        return {**goc, "trang_thai": KHONG_DO_DUOC, "chi_tiet": f"khong goi duoc \'{ten_chu}\'"}\n',
        '        return {"ten": ten_canary, "trang_thai": KHONG_DO_DUOC, "chi_tiet": "mat tool"}  # đột biến\n',
        "SCRIPT", _PHU, "t13_actionlint_bien_mat_giua_probe_va_canary"),
}

def _chay_1_ca(fn):
    # Trả (trạng_thái, chi_tiết): qua | bo_qua (thiếu môi trường, KHÔNG tính
    # là chết) | chet (ca đích PHẢI rơi vào đây).
    try:
        fn()
        return "qua", None
    except BoQuaMoiTruong as ex:
        return "bo_qua", str(ex)
    except AssertionError as ex:
        return "chet", str(ex)
    except Exception as ex:  # noqa: BLE001 — chết dưới đột biến là dữ liệu đo
        return "chet", f"{type(ex).__name__}: {ex}"

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


def main() -> int:
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

    loi_db = 0
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
        chet = sorted(t for t, (tt, _) in ket.items() if tt == "chet")
        oan = [t for t in chet if t != ca_dich]
        bk = f"{len(chet)}/{len(CA)}"
        if tt_dich == "bo_qua":
            print(f"  KHÔNG_ĐO_ĐƯỢC {ten_db}: đích '{ca_dich}' bị BỎ QUA — {ket[ca_dich][1]}")
            loi_db += 1
        elif tt_dich != "chet":
            print(f"  ĐỎ  {ten_db}: đích '{ca_dich}' vẫn XANH ⇒ đột biến không giết được gì")
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
