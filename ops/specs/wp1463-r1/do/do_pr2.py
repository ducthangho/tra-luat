#!/usr/bin/env python3
"""wp1463 (PR2) — bằng chứng đo trước merge của SPEC r17. KHÔNG phải `*_test.py`, không đăng ký vào registry. Chạy bằng `python3 -B`:
  do_pr2.py ab <SHA_BASE> [--root KHO] [--luu DIR]   Nghiệm thu 1, 2, 5 (hai clone dựng trong MỘT lệnh; chín phép của bộ so)
  do_pr2.py registry [--root KHO] [--tu DIR]         Nghiệm thu 3 (`--tu` = thư mục `--luu` của `ab`, khỏi chạy lại bộ)
  do_pr2.py tu-kiem [--dot-bien] [--root KHO]        tự kiểm bộ so và các chốt rc của bộ chạy (không cần cây git)
Giới hạn (SPEC r17 Nghiệm thu 4): script này KHÔNG đo vùng và KHÔNG quan sát cây tiến trình — cả hai chuyển gói kế nhiệm NO-PR2-DO-CAP-HDH; mỗi
lệnh con in đúng một dòng `GIOI_HAN_PR2` (chẩn đoán, không làm cổng). `ab` và `registry` chạy bộ bằng `chay_bo` (`subprocess.run`, không nhóm
tiến trình riêng): PR2 KHÔNG bảo đảm dọn tiến trình con của bộ khi lệnh bị ngắt hay hết giờ.
"""
import ast
import contextlib
import hashlib
import importlib.util
import inspect
import io
import json
import os
import re
import subprocess
import sys
import tempfile
import time
import types

K = "ops/ci_provenance_test.py"
GIOI_HAN_PR2 = "GIOI_HAN_PR2: khong do vung, khong quan sat cay tien trinh — chuyen goi ke nhiem NO-PR2-DO-CAP-HDH"   # SPEC r17 Nghiệm thu 4 (c): CHẨN ĐOÁN, không làm cổng

def bam_tep(root, p):
    try:
        with open(os.path.join(root, p), "rb") as f:
            return hashlib.sha256(f.read()).hexdigest()
    except OSError:
        return None

# ====================================================================== bộ so A/B (Nghiệm thu 2)
PHEP_SO = ("ca_bo_day_du", "cung_bang", "khong_thieu_ten", "ast_phan_hang", "luoi_phan_hang", "cung_blob_san_pham", "cong_thuc_cu_dong",
           "tong_hai_chieu", "kho_va_ben_doc_cu")
BA_BANG = ("DOT_BIEN", "DOT_BIEN_TEST", "TU_KIEM")

def _n(x):   # neo của đột biến viết có dấu `¦` để KHÔNG tự xuất hiện lần hai trong tệp này
    return x.replace("¦", "")

def xem(m):
    """Module test đã nạp → cái bộ so đọc: ba bảng, tên ca, kế hoạch đột biến của lượt đủ, `phan_hang` và mã nguồn của nó."""
    return {"bang": {b: tuple(getattr(m, b)) for b in BA_BANG}, "ca": list(m.CA), "ph": m.phan_hang, "ph_src": inspect.getsource(m.phan_hang),
            "ke_hoach": [d[0] for b in ("DOT_BIEN", "DOT_BIEN_TEST", "DOT_BIEN_DK") for d in getattr(m, b, ())]}

def doc_luot(ra):
    """Đầu ra một lượt → (dòng, kết cục A+3 hoặc None)."""
    dong = ra.rstrip("\n").split("\n")
    kc = [d[len("KET_CUC_A3: "):] for d in dong if d.startswith("KET_CUC_A3: ")]
    try:
        return dong, (json.loads(kc[0]) if len(kc) == 1 else None)
    except ValueError:
        return dong, None

def _tong_dat(dong):   # dòng `TONG:` CUỐI CÙNG của đầu ra (không đòi nó là dòng cuối: việc ấy do mẫu `MOI` canh)
    return ([d for d in dong if d.startswith("TONG: ")] or [""])[-1] == "TONG: DAT"

def _hop_le(E, ten):
    m = E.get(ten)
    return isinstance(m, dict) and all(isinstance(m.get(k), str) and m.get(k).strip() for k in ("ly_do", "nguoi_xac_nhan"))

def cong_thuc_cu(vh, kc, E):
    """Công thức cũ của `main` ở blob base `21b23dbc` (biểu thức `dat`, `du`, `xau`, `loi_tk`, `ok` chép NGUYÊN VĂN), tính CHỈ từ
    khối `cu`, KHÔNG căn theo kế hoạch; kế hoạch và hạng mong đợi đọc từ module H. `ok` None = không tính được."""
    CA, DOT_BIEN, TU_KIEM, ten_kh, cu = vh["ca"], vh["bang"]["DOT_BIEN"], vh["bang"]["TU_KIEM"], vh["ke_hoach"], kc["cu"]
    kq, kq_db = [(rc, "") for _, rc in cu["ca"]], [(t, h, "") for t, h in cu["dot_bien"]]
    tinh_duoc = [t for t, _ in cu["ca"]] == CA and [t for t, _ in cu["tu_kiem"]] == [d[0] for d in TU_KIEM]
    dat = sum(rc == 0 for rc, _ in kq)
    du = len(set(ten_kh)) == len(ten_kh) and [t for t, _, _ in kq_db] == ten_kh
    xau = [f"{t}: {h} {ct}" for t, h, ct in kq_db if h != "GIET"]
    loi_tk = [f"{ten}: mong {mong}, duoc {h}" for (ten, cu_, moi, dich, mong), (_, h) in zip(TU_KIEM, cu["tu_kiem"]) if h != mong]
    ok = dat == len(CA) > 0 and len(DOT_BIEN) > 0 and du and not xau and not loi_tk
    xau_e = [t for t, h, _ in kq_db if h != "GIET" and not (h == "SONG_SOT" and _hop_le(E, t))]
    ok_e = dat == len(CA) > 0 and len(DOT_BIEN) > 0 and du and not xau_e and not loi_tk
    return {"tinh_duoc": tinh_duoc, "ok": ok if tinh_duoc else None, "ok_e": ok_e if tinh_duoc else None, "dat": dat, "du": du, "xau": xau,
            "loi_tk": loi_tk, "g": sum(h == "GIET" for _, h, _ in kq_db)}

def so_sanh(vb, vh, ra_b, ra_h, ra_nhe, oid_b, oid_h, moi_b, E):
    """Chín phép ĐỘC LẬP (SPEC Nghiệm thu 2 a–e): mỗi phép tính từ đúng miền đọc của nó, không phép nào nhận kết quả phép khác."""
    kq, b, h = {}, vb["bang"], vh["bang"]
    def o_dau(ten):
        return [bg for bg in BA_BANG if any(d[0] == ten for d in h[bg])]
    kq["ca_bo_day_du"] = (all(len({d[0] for d in v[bg]}) == len(v[bg]) for v in (b, h) for bg in BA_BANG)
                          and all(d in h[bg] for bg in BA_BANG for d in b[bg] if any(x[0] == d[0] for x in h[bg])))
    kq["cung_bang"] = all(o_dau(d[0]) in ([], [bg]) for bg in BA_BANG for d in b[bg])
    kq["khong_thieu_ten"] = all(o_dau(d[0]) for bg in BA_BANG for d in b[bg])
    kq["ast_phan_hang"] = ast.dump(ast.parse(vb["ph_src"])) == ast.dump(ast.parse(vh["ph_src"]))
    kq["luoi_phan_hang"] = all(vb["ph"](rc, ct, "cA") == vh["ph"](rc, ct, "cA") for rc in (-9, 0, 1, 2, 3, 4, 124, 125)
                               for ct in ("", "DO:cA:x", "DO:cB:x", "HONG:cA:x"))
    kq["cung_blob_san_pham"] = bool(oid_b) and oid_b == oid_h
    dong, kc = doc_luot(ra_h)
    c = cong_thuc_cu(vh, kc, E) if kc else None
    tong_dat, tk = _tong_dat(dong), vh["bang"]["TU_KIEM"]
    kq["cong_thuc_cu_dong"] = bool(
        c and c["tinh_duoc"] and f"CA: {c['dat']}/{len(vh['ca'])} dat" in dong and f"DOT BIEN: {c['g']}/{len(vh['ke_hoach'])} bi giet dung ly do" in dong
        and c["du"] == (not any(d.startswith("[DOT BIEN THIEU/LAP/DAO VIEC]") for d in dong))
        and len(c["xau"]) == sum(d.startswith("[DOT BIEN KHONG BI GIET DUNG]") for d in dong)
        and f"TU KIEM PHAN HANG: {'DAT' if not c['loi_tk'] else 'DO'} ({len(tk)} dot bien)" in dong and len(c["loi_tk"]) == sum(d.startswith("[TU KIEM]") for d in dong))
    T = bool(kc) and all(x["trang_thai_thuc_thi"] == "hoan_tat" for x in kc["ca"] + kc["dot_bien"] + kc["tu_kiem"]) and len(tk) > 0 \
        and len({d[0] for d in tk}) == len(tk) and not E
    kq["tong_hai_chieu"] = bool(c) and (not tong_dat or c["ok_e"] is True) and (bool(E) or not (c["ok"] is True and T) or tong_dat)
    giet = {x["ten"] for x in kc["dot_bien"] if x["phan_hang_dot_bien"] == "giet"} if kc else set()
    kq["kho_va_ben_doc_cu"] = (_tong_dat(ra_b.split("\n")) and _tong_dat(ra_h.split("\n")) and set(vb["ke_hoach"]) <= giet
                               and bool(re.search(moi_b, ra_h, re.M)) and not re.search(moi_b, ra_nhe, re.M))
    return kq   # hết so_sanh

def nap_tep(duong, ten):
    spec = importlib.util.spec_from_file_location(ten, duong)
    m = importlib.util.module_from_spec(spec)
    sys.modules[ten] = m
    spec.loader.exec_module(m)
    return m

def nap_dang_ky(root):
    m = types.ModuleType("dang_ky_do_pr2")
    m.__file__ = os.path.join(root, ".claude", "dev", "ci_dang_ky_test.py")
    with open(m.__file__, encoding="utf-8") as f:
        exec(compile(f.read(), m.__file__, "exec"), m.__dict__)
    return m

def chay_bo(root, nhe):
    env = {k: v for k, v in os.environ.items() if k != "CI_PROVENANCE_KHONG_DOT_BIEN"}
    t0 = time.monotonic()
    r = subprocess.run([sys.executable, "-B", K], cwd=root, env=dict(env, CI_PROVENANCE_KHONG_DOT_BIEN="1") if nhe else env, capture_output=True)
    return r.returncode, (r.stdout + r.stderr).decode("utf-8", "replace"), round(time.monotonic() - t0, 1)

def _git(root, *a):
    r = subprocess.run(["git", "-C", root, *a], capture_output=True, text=True)
    return r.stdout.strip() if r.returncode == 0 else None

LUOT_AB = (("base", "day_du"), ("H", "day_du"), ("H", "nhe"))   # ba lượt = ba ranh giới tiến trình của `ab`

def do_ab(cay, oid, sha_base, chay=chay_bo, luu=None):
    """Phần ĐO của `ab` trên hai cây đã dựng: ba lượt, chín phép, kết luận. R15-1: `DAT` đòi CẢ BA lượt thoát rc 0, xét SAU kết quả dương; mã
    thoát thuộc BỘ CHẠY và KHÔNG gộp vào chín phép so ngữ nghĩa. rc khác 0 được in nguyên (`LUOT … rc=`, `RC_LUOT`), lưu nguyên (`.rc`) cùng
    đầu ra chẩn đoán, và lệnh thoát 1. `chay` là tham số để tự kiểm bơm rc ở TỪNG ranh giới."""
    kq = {luot: chay(cay[luot[0]], luot[1] == "nhe") for luot in LUOT_AB}
    vb, vh = xem(nap_tep(os.path.join(cay["base"], K), "cpt_base")), xem(nap_tep(os.path.join(cay["H"], K), "cpt_h"))
    moi_b, E = nap_dang_ky(cay["base"]).MOI[K], sys.modules["cpt_h"].TUONG_DUONG_A3
    phep = so_sanh(vb, vh, kq["base", "day_du"][1], kq["H", "day_du"][1], kq["H", "nhe"][1], oid["base"], oid["H"], moi_b, E)
    for p in (K, ".claude/dev/ci_dang_ky_test.py"):
        print(f"SHA256 {p}: {bam_tep(cay['H'], p)}")
    print(f"AB base={sha_base} blob ops/ci_provenance.py base={oid['base']} H={oid['H']} (H = HEAD cua kho do, khong ghi o day)")
    for ten, che in LUOT_AB:
        rc, ra, giay = kq[ten, che]
        print(f"LUOT {ten} {che}: rc={rc} · {giay} s · {' · '.join(d for d in ra.splitlines() if d.startswith(('TIEN TRINH', 'CHE DO')))} · CPU {os.cpu_count()}")
        print("  " + " · ".join(ra.rstrip("\n").split("\n")[-4:]))
        for duoi, nd in ((".out", ra), (".rc", f"{rc}\n")) if luu else ():
            with open(os.path.join(luu, f"{ten}.{che}{duoi}"), "w", encoding="utf-8") as f:
                f.write(nd)
    print(f"KE HOACH DOT BIEN: base {len(vb['ke_hoach'])} viec · H {len(vh['ke_hoach'])} viec · ten base ⊆ H: {set(vb['ke_hoach']) <= set(vh['ke_hoach'])}")
    for p in PHEP_SO:
        print(f"PHEP {p}: {'DUNG' if phep.get(p) is True else 'SAI'}")
    rc_luot = [(f"{ten}/{che}", kq[ten, che][0]) for ten, che in LUOT_AB]
    print("RC_LUOT: " + " · ".join(f"{k}={v}" for k, v in rc_luot) + " (ca ba phai bang 0)")
    hong = [k for k, v in rc_luot if v != 0]
    dat = all(phep.get(p) is True for p in PHEP_SO) and set(phep) == set(PHEP_SO) and not hong
    print(GIOI_HAN_PR2)
    print(f"KET_LUAN_AB: {'DAT' if dat else 'DO'} ({sum(phep.get(p) is True for p in PHEP_SO)}/{len(PHEP_SO)} phep dung{' · rc khac 0 o luot ' + ', '.join(hong) if hong else ''})")
    return 0 if dat else 1

def lenh_ab(root, sha_base, luu=None):
    """Hai clone (base của lease và HEAD của `root`) dựng trong MỘT lệnh, cùng các bước, XONG cả hai rồi mới đo (`do_ab`)."""
    cay, oid = {}, {}
    with tempfile.TemporaryDirectory(prefix="wp1463-ab-") as tam:
        for ten, sha in (("base", sha_base), ("H", _git(root, "rev-parse", "HEAD"))):
            d = cay[ten] = os.path.join(tam, ten)
            for c in (["git", "clone", "-q", "--no-hardlinks", root, d], ["git", "-C", d, "-c", "advice.detachedHead=false", "checkout", "-q", sha], ["git", "-C", d, "config", "core.abbrev", "7"]):
                if subprocess.run(c).returncode:
                    print(GIOI_HAN_PR2)
                    print(f"KET_LUAN_AB: KHONG_DO_DUOC (lenh hong: {' '.join(c)})")
                    return 3
            oid[ten] = _git(d, "rev-parse", "HEAD:ops/ci_provenance.py")
        return do_ab(cay, oid, _git(cay["base"], "rev-parse", "HEAD"), luu=luu)

def lenh_registry(root, tu=None):
    """Nghiệm thu 3: đầu ra THẬT của lượt nhẹ và lượt đủ trên H đi qua `chay_moi` THẬT của registry H với bộ chạy giả trả lại nó."""
    ra = {}
    for che in ("nhe", "day_du"):
        if tu:   # R15-1 (quét cùng lớp): rc là rc THẬT của lượt mà `ab` đã lưu, không mặc định 0; thiếu tệp `.rc` ⇒ lệnh hỏng, không ĐẠT
            with open(os.path.join(tu, f"H.{che}.out"), encoding="utf-8") as f, open(os.path.join(tu, f"H.{che}.rc"), encoding="utf-8") as g:
                ra[che] = (int(g.read()), f.read())
        else:
            ra[che] = chay_bo(root, che == "nhe")[:2]
    m, dat = nap_dang_ky(root), True
    for che_ra, che_kh, mong in (("nhe", "nhe", True), ("day_du", "day_du", True), ("day_du", "nhe", False), ("nhe", "day_du", False)):
        with contextlib.redirect_stdout(io.StringIO()) as log:
            do = m.chay_moi(moi={K: m.MOI[K]}, cach_ly={}, chay_mot=lambda p: ra[che_ra], doc_moi_truong=lambda: "github-actions/linux",
                            doc_trong_ci=lambda: True, doc_nen_windows=lambda: False, kh={K: (che_kh, "do_pr2 registry")})
        dong = [d for d in log.getvalue().splitlines() if d.startswith("CI_DANG_KY ")]
        dat = dat and (do == 0) is mong
        print(f"REGISTRY dau ra {che_ra} / ke hoach {che_kh}: {'ĐẠT' if do == 0 else 'ĐỎ'} (mong {'ĐẠT' if mong else 'ĐỎ'}) · {' | '.join(dong)}")
    print(GIOI_HAN_PR2)
    print(f"KET_LUAN_REGISTRY: {'DAT' if dat else 'DO'} (dau ra {'doc tu ' + tu if tu else 'chay tai cho'})")
    return 0 if dat else 1

# ====================================================================== tự kiểm bộ so (không cần cây git)
MOI_GIA = (r"(?ms)\A(?!.*^(?:TONG|TU KIEM PHAN HANG): DO\b).*^CA: ([1-9]\d*)/(\1) dat\nDOT BIEN: ([1-9]\d*)/\3 bi giet dung ly do\n"
           r"TU KIEM PHAN HANG: DAT \(\d+ dot bien\)\nTONG: DAT\n?\Z")   # chép mẫu `MOI` của bộ tại base (chỉ cho đầu vào tổng hợp)
HT = "hoan_tat"

def luot_gia(bo, v, kq_db=None, kq_tk=None, E=None, che="day_du"):
    """Đầu ra của MỘT lượt tổng hợp, dựng bằng CHÍNH các hàm của bộ H theo cách `main` in — nhất quán với view `v` như lượt thật."""
    ten_kh, tk, E = v["ke_hoach"], [(d[0], d[4]) for d in v["bang"]["TU_KIEM"]], E or {}
    kq_db = ([(t, "GIET", HT) for t in ten_kh] if che != "nhe" else []) if kq_db is None else kq_db
    kq_tk, kq_ca = [(t, m, HT) for t, m in tk] if kq_tk is None else kq_tk, [(t, 0, HT, "passed") for t in v["ca"]]
    kc = bo.tinh_ket_cuc(che, v["ca"], ten_kh, tk, kq_ca, kq_db, kq_tk, E, v["bang"]["DOT_BIEN"])
    cu = bo.cong_thuc_cu(v["ca"], v["bang"]["DOT_BIEN"], tk, ten_kh, [x[:2] for x in kq_ca], kq_db, kq_tk, E)
    dong = ["TIEN TRINH: 1", f"CHE DO: {che}"] + ["[DOT BIEN THIEU/LAP/DAO VIEC] x"] * (not cu["du"] and che != "nhe") \
        + [f"[DOT BIEN KHONG BI GIET DUNG] {t}: {h} " for t, h, _ in cu["xau"]] + [f"[TU KIEM] {x}" for x in cu["loi_tk"]] \
        + ["KET_CUC_A3: " + json.dumps(kc, ensure_ascii=False, sort_keys=True, separators=(",", ":"))] \
        + bo.dong_ket_luan(che, cu["dat"], len(v["ca"]), sum(h == "GIET" for _, h, _ in kq_db), len(ten_kh), not cu["loi_tk"], len(tk), kc["ket_luan_tong"])
    return "\n".join(dong) + "\n"

def _sua_kc(ra, f):   # đổi ĐÚNG khối KET_CUC_A3 của một đầu ra, mọi dòng khác giữ nguyên
    dong, kc = doc_luot(ra)
    f(kc)
    return "\n".join("KET_CUC_A3: " + json.dumps(kc, ensure_ascii=False, sort_keys=True, separators=(",", ":")) if d.startswith("KET_CUC_A3: ") else d
                     for d in dong) + "\n"

def dau_vao_so(bo):
    """[(tên đầu vào, đối số của `so_sanh`, TẬP phép phải sai)] — mỗi đầu vào là nền khoẻ đổi ĐÚNG trường nó nêu (SPEC Nghiệm thu 2)."""
    src = inspect.getsource(bo.phan_hang)
    def view(db=None, dbt=None, tk=None, src=src):
        ns = {}
        exec(src, ns)
        bang = {"DOT_BIEN": (("A1_xoa_co_attempt", "neo1", "thay1", "c01"), ("m2", "neo2", "thay2", "c02")) if db is None else db,
                "DOT_BIEN_TEST": (("T1", "neo3", "thay3", "c03"),) if dbt is None else dbt, "TU_KIEM": (("k1", "neo4", "thay4", "c01", "TIN_DUNG_GIA"),) if tk is None else tk}
        return {"bang": bang, "ca": ["c01_a", "c02_b", "c03_c"], "ph": ns["phan_hang"], "ph_src": src, "ke_hoach": [d[0] for b in BA_BANG[:2] for d in bang[b]]}
    VB = view()
    def dv(vh=None, E=None, sua=None, **kw):   # nền khoẻ: lượt H nhất quán với CHÍNH module H của đầu vào
        vh = vh or view()
        a = {"vb": VB, "vh": vh, "ra_b": luot_gia(bo, VB), "ra_h": luot_gia(bo, vh, E=E, **kw), "ra_nhe": luot_gia(bo, vh, che="nhe"), "oid_b": "a" * 40,
             "oid_h": "a" * 40, "moi_b": MOI_GIA, "E": E or {}}
        a.update(sua(a) if sua else {})
        return a
    A1, m2, T1, k1 = VB["bang"]["DOT_BIEN"] + VB["bang"]["DOT_BIEN_TEST"] + VB["bang"]["TU_KIEM"]
    def loi(kq_db=None, **kw):   # đối chứng của (d): lượt dựng NHẤT QUÁN theo công thức cũ
        return dv(kq_db=[(t, *(kq_db or {}).get(t, ("GIET", HT))) for t in VB["ke_hoach"]], **kw)
    def tk_lech(a):
        ra = _sua_kc(a["ra_h"], lambda kc: kc["cu"]["tu_kiem"][0].__setitem__(1, "GIET"))
        return {"ra_h": ra.replace("KET_CUC_A3: ", "[TU KIEM] k1: mong TIN_DUNG_GIA, duoc GIET\nKET_CUC_A3: ").replace("TU KIEM PHAN HANG: DAT", "TU KIEM PHAN HANG: DO")}
    ca_bo, d_, t_, kho = {"ca_bo_day_du"}, "cong_thuc_cu_dong", "tong_hai_chieu", "kho_va_ben_doc_cu"
    return [
        ("nen_khoe", dv(), set()),
        ("a_doi_thay_the", dv(view(db=((*A1[:2], "thay KHAC", A1[3]), m2))), ca_bo), ("a_doi_neo", dv(view(db=((A1[0], "neo KHAC", *A1[2:]), m2))), ca_bo),
        ("a_doi_tien_to_ca_dich", dv(view(db=((*A1[:3], "c02"), m2))), ca_bo), ("a_doi_hang_mong_tu_kiem", dv(view(tk=((*k1[:4], "SONG_SOT"),))), ca_bo),
        ("a_chuyen_bang", dv(view(db=(A1,), dbt=(m2, T1))), {"cung_bang"}), ("a_thieu_ten_base", dv(view(db=(A1,))), {"khong_thieu_ten", kho}),
        ("b_phan_hang_rc4_HONG", dv(view(src=src.replace('"TIN_DUNG_GIA" if rc == 4 else "HONG"', '"HONG"'))), {"ast_phan_hang", "luoi_phan_hang"}),
        ("c_oid_khac", dv(sua=lambda a: {"oid_h": "b" * 40}), {"cung_blob_san_pham"}),
        ("d_dong_dot_bien_tu_so_M_tru_1", dv(sua=lambda a: {"ra_h": a["ra_h"].replace("DOT BIEN: 3/3", "DOT BIEN: 2/3")}), {d_, kho}),
        ("d_cu_dot_bien_doi_cho", dv(sua=lambda a: {"ra_h": _sua_kc(a["ra_h"], lambda kc: kc["cu"]["dot_bien"].reverse())}), {d_, t_}),
        ("d_bo_tu_kiem_khoi_cu", dv(sua=lambda a: {"ra_h": _sua_kc(a["ra_h"], lambda kc: kc["cu"]["tu_kiem"].clear())}), {d_, t_}),
        ("d_cu_tu_kiem_lech_hang_ma_TONG_DAT", dv(sua=tk_lech), {t_, kho}),
        ("d_TONG_DO_tren_nen_khoe", dv(sua=lambda a: {"ra_h": a["ra_h"][:-len("TONG: DAT\n")] + "TONG: DO\n"}), {t_, kho}),
        ("e_them_dong_sau_TONG", dv(sua=lambda a: {"ra_h": a["ra_h"] + "dong thua\n"}), {kho}),
        ("e_hang_A3_cua_ten_base_thanh_song", dv(sua=lambda a: {"ra_h": _sua_kc(a["ra_h"], lambda kc: kc["dot_bien"][0].__setitem__("phan_hang_dot_bien", "song"))}), {kho}),
        ("e_dau_ra_nhe_khop_MOI_base", dv(sua=lambda a: {"ra_nhe": a["ra_h"]}), {kho}),
        ("duong_them_muc_moi", dv(view(db=(A1, m2, ("m9", "neo9", "thay9", "c02")))), set()),
        ("duong_phan_hang_doi_khoang_trang_chu_thich", dv(view(src=src.replace("    if rc == 0:", "    # chu thich\n    if rc  ==  0:"))), set()),
        *[(f"doi_chung_d_phan_tu_ha_tang_cu_{h}", loi({"m2": (h, "infrastructure_error")}), {kho}) for h in ("GIET", "TIN_DUNG_GIA", "SONG_SOT")],
        ("doi_chung_d_tu_kiem_het_han_trong_ca", dv(kq_tk=[("k1", "TIN_DUNG_GIA", "timed_out")]), {kho}),
        ("doi_chung_d_thieu_ket_qua_dot_bien", dv(kq_db=[("A1_xoa_co_attempt", "GIET", HT)]), {kho}),
        ("doi_chung_d_E_khac_rong_XANH", loi({"m2": ("SONG_SOT", HT)}, E={"m2": {"ly_do": "x", "nguoi_xac_nhan": "A"}}), {kho}),
        ("doi_chung_d_thieu_tu_kiem_TONG_DO", dv(kq_tk=[]), {d_, kho})]

def tu_kiem_so(bo):
    """[(tên, tập sai KHAI, véc-tơ chín phép)]."""
    return [(ten, khai, so_sanh(**a)) for ten, a, khai in dau_vao_so(bo)]

DOT_BIEN_SO = [(f"go_{p}", "    return kq   # hết ¦so_sanh", f'    kq["{p}"] = True\n    return kq', (p,)) for p in PHEP_SO] + [
    ("d_tinh_cong_thuc_cu_tu_tang_A3", 'kq, kq_db = [(rc, "") for _, rc in cu["ca"]], ¦[(t, h, "") for t, h in cu["dot_bien"]]',
     'kq, kq_db = [(rc, "") for _, rc in cu["ca"]], [(x["ten"], {"giet": "GIET", "song": "SONG_SOT", "tin_dung_gia": "TIN_DUNG_GIA"}.get(x["phan_hang_dot_bien"], "HONG"), "") for x in kc["dot_bien"]]',
     PHEP_SO[6:8]),
    ("d_so_TONG_bang_dang_thuc_voi_ok_cu", 'and (bool(E) or not (c["ok"] is True ¦and T) or tong_dat)', 'and tong_dat == (c["ok"] is True)', PHEP_SO[6:8]),
    ("d_du_cu_tren_cu_da_can_theo_ke_hoach", 'and [t for t, _, _ in kq_db] ¦== ten_kh', 'and sorted(t for t, _, _ in kq_db) == sorted(ten_kh)', PHEP_SO[6:8]),
    ("d_luat_thuan_dung_ok_cu_thay_ok_cu_E", '(not tong_dat or c["ok_e"] ¦is True)', '(not tong_dat or c["ok"] is True)', PHEP_SO[6:8]),
    ("d_ok_cu_khong_tinh_duoc_coi_la_True", '(not tong_dat or c["ok_e"] ¦is True)', '(not tong_dat or c["ok_e"] is not False)', PHEP_SO[6:8]),
    ("d_E_khac_rong_ep_khong_xanh", '(not tong_dat or c["ok_e"] ¦is True)', '(not tong_dat or (c["ok_e"] is True and not E))', PHEP_SO[6:8])]

# ====================================================================== tự kiểm BỘ CHẠY: chốt rc của `ab`/`registry --tu` (R15-1)
def tu_kiem_chay(bo, root):
    """[(tên, mong, được)] — sáu ca, không ca nào sinh tiến trình. (i) `do_ab` THẬT trên nền khoẻ (base = H = `root`, không cần git) với bộ chạy
    giả trả đầu ra KHOẺ kèm rc 42 ở ĐÚNG MỘT trong ba ranh giới ⇒ lệnh thất bại mà chín phép vẫn 9/9; đối chứng rc 0 ⇒ DAT. (ii) `registry --tu`
    đọc rc ĐÃ LƯU."""
    kq, v, cay = [], xem(bo), {"base": root, "H": os.path.join(root, "")}   # hai cách viết của CÙNG cây: bộ chạy giả phân biệt base với H
    def ab(bom, luu=None):
        def chay(r, nhe):
            luot = ("H" if r == cay["H"] else "base", "nhe" if nhe else "day_du")
            return (42 if luot == bom else 0), luot_gia(bo, v, che=luot[1]), 0.0
        with contextlib.redirect_stdout(io.StringIO()) as ra:
            rc = do_ab(cay, dict.fromkeys(cay, "a" * 40), "tu-kiem", chay, luu)
        cuoi = ra.getvalue().splitlines()[-1]
        return rc, cuoi.split(" (")[0], cuoi.split("(")[1].split(" ")[0]
    def reg(tu):
        with contextlib.redirect_stdout(io.StringIO()):
            return lenh_registry(root, tu)
    with tempfile.TemporaryDirectory(prefix="wp1463-chay-") as tam:
        kq.append(("ab_rc0_doi_chung", (0, "KET_LUAN_AB: DAT", "9/9"), ab(None, tam)))
        kq += [(f"ab_rc42_{ten}_{che}", (1, "KET_LUAN_AB: DO", "9/9"), ab((ten, che))) for ten, che in LUOT_AB]
        kq.append(("registry_tu_rc0_doi_chung", 0, reg(tam)))
        with open(os.path.join(tam, "H.nhe.rc"), "w", encoding="utf-8") as f:
            f.write("42\n")
        kq.append(("registry_tu_rc42_luot_nhe", 1, reg(tam)))
    return kq

DOT_BIEN_CHAY = [(f"ab_bo_chot_rc_luot_{ten}_{che}", "hong = [k for k, v in rc_luot ¦if v != 0]", f'hong = [k for k, v in rc_luot if v != 0 and k != "{ten}/{che}"]',
                  f"ab_rc42_{ten}_{che}") for ten, che in LUOT_AB] + [
    ("registry_tu_mac_dinh_rc_0", "ra[che] = (¦int(g.read()), f.read())", "ra[che] = (0, f.read())", "registry_tu_rc42_luot_nhe")]

def lenh_tu_kiem(root, dot_bien):
    bo = nap_tep(os.path.join(root, K), "cpt_tu_kiem")
    so, chay = tu_kiem_so(bo), tu_kiem_chay(bo, root)
    so_sai = [(t, sorted(k), sorted(p for p in PHEP_SO if v.get(p) is not True)) for t, k, v in so if {p for p in PHEP_SO if v.get(p) is not True} != k or set(v) != set(PHEP_SO)]
    chay_sai = [x for x in chay if x[1] != x[2]]
    for t, k, v in so:
        print(f"SO {t}: khai sai {sorted(k)} · vec-to {''.join('1' if v.get(p) is True else '0' for p in PHEP_SO)}")
    thieu = [p for p in PHEP_SO if not any(p in k for _, k, _ in so)]
    for x in so_sai + chay_sai:
        print(f"LECH: {x}")
    print(f"TU_KIEM_SO: {len(so) - len(so_sai)}/{len(so)} dat · moi phep co dau vao am: {not thieu}")
    for x in chay:
        print(f"CHAY {x[0]}: mong {x[1]} · duoc {x[2]}")
    print(f"TU_KIEM_CHAY: {sum(x[1] == x[2] for x in chay)}/{len(chay)} dat")
    ok, bat = not (so_sai or chay_sai or thieu), 0
    if dot_bien and ok:
        with open(os.path.abspath(__file__), encoding="utf-8") as f:
            src = f.read()
        sys.dont_write_bytecode = True
        with tempfile.TemporaryDirectory(prefix="wp1463-db-") as tam:
            for nhom, ds in (("SO", DOT_BIEN_SO), ("CHAY", DOT_BIEN_CHAY)):
                for ten, cu, moi, dich in ds:
                    cu = _n(cu)
                    if src.count(cu) != 1:
                        print(f"DB_{nhom} {ten}: HONG — neo thay {src.count(cu)} lan")
                        continue
                    duong = os.path.join(tam, f"db_{ten}.py")
                    with open(duong, "w", encoding="utf-8") as f:
                        f.write(src.replace(cu, moi))
                    m = nap_tep(duong, f"do_pr2_db_{ten}")
                    if nhom == "SO":   # chỉ tính là BẮT khi véc-tơ lệch véc-tơ khai ĐÚNG ở phép bị gỡ/bị đổi
                        lech = [(t, p, p not in k, v.get(p) is True) for t, k, v in m.tu_kiem_so(bo) for p in dich if (v.get(p) is True) != (p not in k)]
                        mo_ta = "; ".join(f"{t}: {p} {'DUNG' if truoc else 'SAI'}→{'DUNG' if sau else 'SAI'}" for t, p, truoc, sau in lech[:4])
                    else:      # phải đổi kết quả ở ĐÚNG đầu vào tương ứng
                        lech = [x for x in m.tu_kiem_chay(bo, root) if x[1] != x[2] and x[0] == dich]
                        mo_ta = "; ".join(f"{x[0]}: mong {x[1]} duoc {x[2]}" for x in lech)
                    bat += bool(lech)
                    print(f"DB_{nhom} {ten}: {'BAT' if lech else 'SONG'} · {mo_ta}")
        tong = len(DOT_BIEN_SO) + len(DOT_BIEN_CHAY)
        print(f"DOT_BIEN_TU_KIEM: {bat}/{tong} bi bat dung cho ({len(DOT_BIEN_SO)} cua bo so, {len(DOT_BIEN_CHAY)} cua bo chay)")
        ok = bat == tong
    print(GIOI_HAN_PR2)
    print(f"KET_LUAN_TU_KIEM: {'DAT' if ok else 'DO'}")
    return 0 if ok else 1

def main(argv):
    lenh = argv[1] if len(argv) > 1 else ""
    root = os.path.abspath(argv[argv.index("--root") + 1] if "--root" in argv else os.path.join(os.path.dirname(os.path.abspath(__file__)), *[os.pardir] * 4))
    luu = argv[argv.index("--luu") + 1] if "--luu" in argv else None
    if lenh == "ab" and len(argv) > 2:
        return lenh_ab(root, argv[2], luu)
    if lenh == "registry":
        return lenh_registry(root, argv[argv.index("--tu") + 1] if "--tu" in argv else None)
    if lenh == "tu-kiem":
        return lenh_tu_kiem(root, "--dot-bien" in argv)
    print(__doc__)
    return 2

if __name__ == "__main__":
    sys.exit(main(sys.argv))
