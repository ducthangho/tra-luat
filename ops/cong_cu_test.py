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

def mot_probe(ten, regex=r"(\d+\.\d+\.\d+)"):
    return [{"ten": "mac_dinh", "lenh": [ten, "--version"], "regex": regex}]

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
        rc_vang, _, _ = chay("kiem-tra", "--ban-ke", str(bk0), env=moi_truong())
        bk1, env1 = bk_don(tmp, "sai-ban-t1", "#!/bin/sh\necho 0.0.0\n", ban_ghim="9.9.9")
        rc_do, _, _ = chay("kiem-tra", "--ban-ke", str(bk1), env=env1)
        bang(rc_vang != 0 and rc_do != 0, f"cả hai phải khác 0: vắng={rc_vang} sai_bản={rc_do}")
        bang(rc_vang != rc_do, f"KHÔNG_ĐO_ĐƯỢC(rc={rc_vang}) và ĐỎ(rc={rc_do}) CHUNG mã")

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
    """T6: bước kiểm bản kê đứng TRƯỚC mọi bước test NẶNG (neo TÊN bước, không số dòng)."""
    d = yaml.safe_load((GOC / ".github" / "workflows" / "ci.yml").read_text(encoding="utf-8"))
    buoc = (d.get("jobs", {}).get("gate", {}) or {}).get("steps", [])
    idx_kiem = [i for i, b in enumerate(buoc)
                if "ops/cong_cu.py" in str(b.get("run", "")) and "kiem-tra" in str(b.get("run", ""))]
    bang(idx_kiem, "không thấy bước gọi `ops/cong_cu.py kiem-tra` trong job `gate`")
    # KHÔNG "selftest" trần: khớp cả bước NHẸ ("eol-policy/pre-push") LẪN "lease-publish
    # selftest" (bước TỰ cài actionlint mà G5 đứng NGAY SAU để tái dùng).
    NANG = ("tl selftest", "release-check", "release-verify", "release-bundle", "golden-test",
            "doc-claims-check", "determinism-audit", "workflow-audit", "ci-phamvi",
            "bundled-fragment", "gate lifecycle", "don-nhanh", "command-registry", "tl_boot")
    idx_nang = [i for i, b in enumerate(buoc) if any(n in str(b.get("name", "")) for n in NANG)]
    bang(idx_nang, "không thấy bước test NẶNG nào để đối chiếu (danh sách NANG trôi?)")
    bang(min(idx_kiem) < min(idx_nang),
         f"bước kiểm ở vị trí {min(idx_kiem)} không trước bước nặng sớm nhất "
         f"{min(idx_nang)} ('{buoc[min(idx_nang)].get('name')}')")

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

# ===== BỘ ĐỘT BIẾN T1..T8 (packet #290 lượt 2) — 1 đột biến/ca, bán kính đo
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
        "                canary_kq.append(kiem_tra_canary(cn, theo_ten, thu_muc_goc or GOC))\n",
        "                pass  # đột biến: gỡ lời gọi kiem_tra_canary\n",
        "SCRIPT", _PHU, "t2_canary_thieu_shellcheck_phai_SUY_GIAM"),
    "t3_bao_dong_gia": ("ops/cong_cu.py",
        '    return {**goc, "trang_thai": DAT, "chi_tiet": "dat"}\n',
        '    return {**goc, "trang_thai": DO, "chi_tiet": "dat"}  # đột biến\n',
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
    "t6_ten_buoc_trung_tu_khoa": (".github/workflows/ci.yml",
        "      - name: eol-policy selftest\n",
        "      - name: eol-policy selftest tl selftest\n",
        "GOC", (), "t6_ci_kiem_ban_ke_truoc_moi_test_nang"),
    "t7_bo_luat_2_duong": ("ops/cong_cu.py",
        "    if len(ban_thay) > 1 and len(khac_nhau) > 1:\n",
        "    if False:  # đột biến: bỏ luật hai đường khác bản\n",
        "SCRIPT", _PHU, "t7_hai_duong_goi_khac_ban_phai_bao_khong_im"),
    "t8_mat_field_ten": ("ops/cong_cu.py",
        '    goc = {"ten": ten, "bat_buoc": bat_buoc, "ban_ghim": ban_ghim, "ban_thay": ban_thay}\n',
        '    goc = {"bat_buoc": bat_buoc, "ban_ghim": ban_ghim, "ban_thay": ban_thay}  # đột biến\n',
        "SCRIPT", _PHU, "t8_van_tay_cong_cu_co_trong_ho_so"),
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
    print(f"\nBÁN KÍNH ĐỘT BIẾN ({len(DOT_BIEN)} đột biến, mỗi ca t1..t8 đúng một):")
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
