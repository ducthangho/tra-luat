#!/usr/bin/env python3
"""Phản chứng CHẠY ĐƯỢC cho `ops/land_evidence_nguon.py` — packet #773, đặc tả r1 mục `nghiem_thu`.

Ca `c*` dựng cây tạm (không chạm `ops/land/**` thật, Q5), dựng lại lượt 1 và 2 của connector trên #771; `c11` chạy CÂY
THẬT (m = k). ĐỘT BIẾN sửa BẢN SAO TẠM của bộ kiểm (neo đúng một lần), ca đích chạy ở tiến trình con và phải XANH trên bản
gốc trước. Chỉ `bang()` ném `TinHieuChotCa` (con in `DO:<ca>:`, thoát 3); lỗi vô can thoát 4 ⇒ TÍN DỤNG GIẢ, không tính
giết (bài học CLAUDE.md "bị giết không phải bị giết ĐÚNG LÝ DO"). `TU_KIEM` kiểm chính bộ phân hạng.

Ra: `CA: N/N dat` · `DOT BIEN: M/M bi giet dung ly do` · `TONG: DAT`. Thoát 0 chỉ khi cả ba.
"""
import contextlib
import hashlib
import importlib.util
import io
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

sys.dont_write_bytecode = True
for _s in (sys.stdout, sys.stderr):
    if hasattr(_s, "reconfigure"):
        _s.reconfigure(encoding="utf-8", errors="backslashreplace")

HERE = Path(__file__).resolve().parent
ROOT_THAT = HERE.parent
MA = Path(os.environ.get("LAND_EVIDENCE_NGUON_MA") or HERE / "land_evidence_nguon.py")
TEN = "pr9001-thu-land-evidence.yaml"
PROV = "pr9001-thu-provenance"

# L5 — bản kỳ vọng CHÉP RIÊNG dạng VÂN TAY: sha256 của `json.dumps(sorted(MIEN_TRU_CUTOVER.items()))` đo trên `c73af7b`
# (16-10-2026), 28 tên. Thêm/đổi/bỏ một tên hay một băm trong bộ kiểm ⇒ c10 ĐỎ; danh sách đọc được nằm trong bộ kiểm.
KY_VONG_SO_MIEN_TRU = 28
KY_VONG_VAN_TAY_MIEN_TRU = "5311e7557cd75ef2f3b06371c66a4830d4970613c1e98a8fd4af732d7dab2257"


class TinHieuChotCa(AssertionError):
    """Chỉ `bang()` ném lớp này ⇒ phân biệt được giết thật (chốt) với chết vì lỗi vô can."""


CA = {}


def bang(dieu_kien, thong_diep):
    if not dieu_kien:
        raise TinHieuChotCa(thong_diep)


def ca(f):
    CA[f.__name__] = f
    return f


def nap():
    spec = importlib.util.spec_from_file_location("land_evidence_nguon_duoi_test", MA)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


@contextlib.contextmanager
def cay(ho_so, prov=None):
    """Cây tạm: `ops/land/<TEN>` = `ho_so`; `prov` = {đường dẫn trong provenance: nội dung} (None ⇒ không tạo thư mục)."""
    with tempfile.TemporaryDirectory(prefix="len_cay_") as thu:
        goc = Path(thu) / "kho"
        tep = {TEN: ho_so} | {f"{PROV}/{d}": nd for d, nd in (prov or {}).items()}
        for duong, nd in tep.items():
            (goc / "ops/land" / duong).parent.mkdir(parents=True, exist_ok=True)
            (goc / "ops/land" / duong).write_text(nd, encoding="utf-8")
        if prov is not None:
            (goc / "ops/land" / PROV).mkdir(exist_ok=True)
        yield goc


def kiem(m, goc):
    with contextlib.redirect_stdout(io.StringIO()) as buf:
        rc = m.main(["--root", str(goc)])
    return rc, buf.getvalue()


def chay(ho_so, prov=None):
    with cay(ho_so, prov) as goc:
        return kiem(nap(), goc)


RB_PR = '{"number": 9001, "merged": true, "merged_at": "2026-10-16T02:58:26Z"}'
RB_RUN = '{"id": 1, "status": "completed", "conclusion": "success"}'
LOG = "# trich log\n195/195 ca DA CHAY QUA (tong 196, bo qua 1, hong 0)\n"


@ca
def c01_l1_luot1_mergeable_clean_khong_nguon():
    rc, ra = chay("dieu_kien:\n  khong_xung_dot: 'measured — mergeable_state clean'\n", {"readback-pr-9001.json": RB_PR})
    bang(rc == 1 and "L1 $.dieu_kien.khong_xung_dot" in ra, f"lượt 1 #771 phải ĐỎ L1: rc={rc} {ra[-300:]}")
    rc, ra = chay("x: 'measured — readback-pr-9001.json: mergeable_state unknown'\n", {"readback-pr-9001.json": RB_PR})
    bang(rc == 0, f"có token nguồn CÓ THẬT phải ĐẠT: rc={rc} {ra[-300:]}")
    rc, ra = chay("x: 'measured — readback-pr-9999.json'\n", {"readback-pr-9001.json": RB_PR})
    bang(rc == 1 and "L1" in ra, f"token trỏ tệp KHÔNG có phải ĐỎ: rc={rc}")
    rc, ra = chay("x: 'measured: ops/land/" + PROV + "/readback-pr-9001.json'\n", {"readback-pr-9001.json": RB_PR})
    bang(rc == 0, f"token tương đối gốc kho phải ĐẠT: rc={rc} {ra[-300:]}")
    rc, ra = chay(f"x: 'measured — {TEN}'\n", {"a.json": "{}"})
    bang(rc == 1 and "L1" in ra, f"lời khai chỉ trỏ CHÍNH hồ sơ phải ĐỎ: rc={rc}")


@ca
def c02_l1_glob_va_thu_muc():
    p = {"trich-log-job/a.txt": LOG}
    for khai, mong in (("trich-log-job/*.txt", 0), ("trich-log-job/*.log", 1), ("trich-log-job/", 0), ("khong-co/", 1)):
        rc, ra = chay(f"x: 'measured - {khai}'\n", p)
        bang(rc == mong, f"{khai}: mong rc={mong}, được {rc} {ra[-200:]}")


@ca
def c03_l1_token_khong_duoc_thoat_goc():
    with cay("x: 'measured — ../ngoai-goc.json'\n", {"a.json": "{}"}) as goc:   # chỉ nền GỐC KHO phân giải được
        (goc.parent / "ngoai-goc.json").write_text("{}", encoding="utf-8")
        rc, ra = kiem(nap(), goc)
    bang(rc == 1 and "L1" in ra, f"token trỏ RA NGOÀI gốc kho phải ĐỎ: rc={rc} {ra[-200:]}")


@ca
def c04_l1_measured_hoa_thuong_va_khong_phai_khai():
    rc, ra = chay("x: 'Measured — khong nguon'\n", {"a.json": "{}"})
    bang(rc == 1, f"`Measured —` không được đi vòng L1: rc={rc}")
    rc, ra = chay("a: measured\nb: 'not_measured — khong do duoc'\nc: 'measuredx khong'\n", {"a.json": "{}"})
    bang(rc == 0, f"`measured` trần / not_measured / measuredx KHÔNG phải lời khai đo: rc={rc} {ra[-300:]}")


@ca
def c05_l2_luot2_positive_phai_co_nguon_chua_nguyen_van():
    p = {"readback-run-1.json": RB_RUN, "trich/u.txt": LOG}
    hs = "post_merge_checks:\n  - {{name: g, positive: 'ubuntu 195/195 hong 0'{}}}\n"
    rc, ra = chay(hs.format(""), p)
    bang(rc == 1 and "thiếu nguon_positive" in ra, f"thiếu nguon_positive phải ĐỎ: rc={rc} {ra[-300:]}")
    rc, ra = chay(hs.format(", nguon_positive: readback-run-1.json"), p)
    bang(rc == 1 and "'195/195'" in ra and "'hong 0'" in ra, f"lượt 2 #771 (chỉ metadata) phải ĐỎ L2: {ra[-300:]}")
    rc, ra = chay(hs.format(", nguon_positive: [readback-run-1.json, trich/u.txt]"), p)
    bang(rc == 0, f"nguồn chứa nguyên văn phải ĐẠT: rc={rc} {ra[-300:]}")
    for log in (LOG.replace("195/195", "194/195"), LOG.replace("195/195", "195/1950"), LOG.replace("hong 0", "hong 01")):
        rc, ra = chay(hs.format(", nguon_positive: trich/u.txt"), {"trich/u.txt": log})
        bang(rc == 1 and "L2" in ra, f"đổi số trong nguồn phải ĐỎ: rc={rc} {log!r}")
    rc, ra = chay(hs.format(", nguon_positive: trich/khong-co.txt"), p)
    bang(rc == 1 and "không có tệp" in ra, f"nguon_positive vắng tệp phải ĐỎ: rc={rc}")


@ca
def c06_l3_luot2_moc_sau_merged_at():
    p = {"readback-pr-9001.json": RB_PR}
    # 02:58:54Z là mốc thật của connector #771; mốc BẰNG merged_at và mốc YAML không nháy (datetime) cũng phải ĐỎ.
    for khoa, moc, mong in (("pre", "'2026-10-16T02:58:54Z'", 1), ("post", "'2026-10-16T02:58:54Z'", 0),
                            ("pre", "'2026-10-16T02:58:26Z'", 1), ("pre", "2026-10-16T02:59:00Z", 1), ("pre", "'x 2026-10-16T02:49:19Z'", 0)):
        rc, ra = chay(f"pre_merge_checks: []\n{khoa}_merge_checks:\n  - {{name: connector, luc: {moc}}}\n".replace("[]\npre_merge_checks:", ""), p)
        bang(rc == mong, f"{khoa} {moc}: mong rc={mong}, được {rc} {ra[-300:]}")
    rc, ra = chay("pre_merge_checks:\n  - {name: c, luc: '2026-10-16T03:00:00Z'}\n", {"a.json": "{}"})
    bang(rc == 0 and "L3 không áp dụng" in ra, f"không readback ⇒ ghi 'không áp dụng': rc={rc} {ra[-200:]}")


@ca
def c07_l3_chi_doc_readback_cua_chinh_pr():
    p = {"readback-pr-9001.json": RB_PR, "readback-pr-9002.json": RB_PR.replace("02:58:26", "01:00:00"),
         "readback-pr-9001-commits.json": "[]"}
    rc, ra = chay("pre_merge_checks:\n  - {name: c, luc: '2026-10-16T02:00:00Z'}\n", p)
    bang(rc == 0, f"readback PR lân cận/-commits không được chen vào L3: rc={rc} {ra[-300:]}")


@ca
def c08_l4_khong_do_duoc_khong_bao_gio_dat():
    rc, ra = chay("x: [khong dong\n", {"a.json": "{}"})
    bang(rc == 2 and "KHÔNG ĐO ĐƯỢC" in ra, f"YAML hỏng ⇒ rc=2: rc={rc}")
    rc, ra = chay("x: 'measured — readback-pr-9001.json'\n", None)
    bang(rc == 2 and "provenance" in ra, f"provenance vắng khi có lời khai đo ⇒ rc=2: rc={rc}")
    rc, ra = chay("pre_merge_checks:\n  - {name: c, luc: '2026-10-16T02:00:00Z'}\n", {"readback-pr-9001.json": "{hong"})
    bang(rc == 2, f"readback hỏng ⇒ rc=2: rc={rc}")
    with tempfile.TemporaryDirectory() as rong:
        rc, ra = kiem(nap(), Path(rong))
    bang(rc == 2 and "tổng 0" in ra, f"không thấy hồ sơ nào ⇒ rc=2, không ĐẠT 0 tệp: rc={rc}")


@ca
def c09_l5_mien_tru_theo_bam():
    hs = "x: 'measured — khong nguon'\n"
    with cay(hs, {"a.json": "{}"}) as goc:
        m = nap()
        m.MIEN_TRU_CUTOVER[TEN] = hashlib.sha256(hs.encode()).hexdigest()
        rc, ra = kiem(m, goc)
        bang(rc == 0 and "1/1 miễn trừ" in ra, f"băm khớp ⇒ miễn trừ có ghi nhận: rc={rc} {ra[-200:]}")
        (goc / "ops/land" / TEN).write_text(hs + " ", encoding="utf-8")
        rc, ra = kiem(m, goc)
        bang(rc == 1 and "MẤT MIỄN TRỪ" in ra and "0/1 miễn trừ" in ra, f"lệch một byte ⇒ kiểm đủ luật: rc={rc} {ra[-300:]}")


@ca
def c10_l5_danh_sach_dong_bang():
    ds = nap().MIEN_TRU_CUTOVER
    van_tay = hashlib.sha256(json.dumps(sorted(ds.items())).encode()).hexdigest()
    bang(len(ds) == KY_VONG_SO_MIEN_TRU and van_tay == KY_VONG_VAN_TAY_MIEN_TRU,
         f"MIEN_TRU_CUTOVER trôi khỏi ảnh chụp cutover: {len(ds)} tên, vân tay {van_tay[:12]}…")


@ca
def c11_cay_that_dat_va_mien_tru_du():
    rc, ra = kiem(nap(), ROOT_THAT)
    n = KY_VONG_SO_MIEN_TRU
    bang(rc == 0 and f"· {n}/{n} miễn trừ" in ra, f"cây thật phải ĐẠT với {n}/{n} miễn trừ: rc={rc} {ra[-400:]}")


@ca
def c12_dong_cuoi_dung_dinh_dang():
    import re
    rc, ra = chay("x: 'measured — a.json'\n", {"a.json": "{}"})
    dong = ra.rstrip("\n").splitlines()[-2:]
    bang(len(dong) == 2 and re.fullmatch(r"land_evidence_nguon: \d+ ĐẠT · \d+/\d+ miễn trừ \(băm khớp\) · \d+ vi phạm · "
                                         r"\d+ KHÔNG ĐO ĐƯỢC · tổng \d+", dong[0]) and dong[1] == "TỔNG: ĐẠT",
         f"định dạng dòng cuối (Q6): {dong}")


# (tên, chuỗi gốc, chuỗi thay, ca đích). Mỗi chốt một đột biến; chuỗi gốc phải xuất hiện ĐÚNG MỘT lần.
DOT_BIEN = (
    ("L1_chi_can_co_token", "        if not thay:", "        if not tk:", "c01_l1_luot1_mergeable_clean_khong_nguon"),
    ("L1_tu_tro_la_nguon", "if p and p.resolve() != tep.resolve()]", "if p]", "c01_l1_luot1_mergeable_clean_khong_nguon"),
    ("L1_glob_rong_van_qua", "            if khop:\n                return khop[0]", "            return nen",
     "c02_l1_glob_va_thu_muc"),
    ("L1_bo_chot_trong_goc", "else p.is_file()) and _trong_goc(p, goc):", "else p.is_file()):", "c03_l1_token_khong_duoc_thoat_goc"),
    ("L1_phan_biet_hoa_thuong", ", re.IGNORECASE)", ")", "c04_l1_measured_hoa_thuong_va_khong_phai_khai"),
    ("L2_bo_doi_nguon", "            vp.append(f\"L2 {d}: có positive mà thiếu", "            continue  # (f\"L2 {d}: có positive mà thiếu",
     "c05_l2_luot2_positive_phai_co_nguon_chua_nguyen_van"),
    ("L2_bo_bien_chu_so", 'else r"(?<![\\d/])" + re.escape(so) + r"(?![\\d/])")', "else re.escape(so))",
     "c05_l2_luot2_positive_phai_co_nguon_chua_nguyen_van"),
    ("L3_bang_nhau_la_truoc", "if _thoi_diem(x) >= moc_merge:", "if _thoi_diem(x) > moc_merge:", "c06_l3_luot2_moc_sau_merged_at"),
    ("L3_bo_datetime_khong_nhay", "moc = [v] if isinstance(v, datetime.datetime) else RE_MOC",
     "moc = [] if isinstance(v, datetime.datetime) else RE_MOC", "c06_l3_luot2_moc_sau_merged_at"),
    ("L3_doc_moi_readback", 'so = re.match(r"pr(\\d+)-", goc_ten)', "so = None", "c07_l3_chi_doc_readback_cua_chinh_pr"),
    ("L4_provenance_vang_van_kiem", "if (khai or co_pos) and not prov.is_dir():", "if False:", "c08_l4_khong_do_duoc_khong_bao_gio_dat"),
    ("L4_khong_do_duoc_thanh_dat", "rc = 1 if v else 2 if u else 0", "rc = 1 if v else 0", "c08_l4_khong_do_duoc_khong_bao_gio_dat"),
    ("L4_rong_thanh_dat", "    if not teps:\n        u += 1", "    if False:\n        u += 1", "c08_l4_khong_do_duoc_khong_bao_gio_dat"),
    ("L5_bo_so_bam", "if hashlib.sha256(byte).hexdigest() == bam:", "if bam:", "c09_l5_mien_tru_theo_bam"),
    ("L5_noi_danh_sach", "MIEN_TRU_CUTOVER = {\n", "MIEN_TRU_CUTOVER = {\n    \"pr9999-tan-cong-land-evidence.yaml\": \"0\" * 64,\n",
     "c10_l5_danh_sach_dong_bang"),
)
TU_KIEM = (   # (tên, gốc, thay, ca đích, hạng mong đợi)
    ("vo_can_KeyError", "def token_nguon(chuoi):\n", "def token_nguon(chuoi):\n    raise KeyError('vo can')\n",
     "c01_l1_luot1_mergeable_clean_khong_nguon", "TIN_DUNG_GIA"),
    ("chi_them_chu_thich", 'THU_MUC = "ops/land"\n', 'THU_MUC = "ops/land"  # vo hai\n', "c01_l1_luot1_mergeable_clean_khong_nguon",
     "SONG_SOT"),
)


def chay_con(ten_ca, ma):
    r = subprocess.run([sys.executable, "-B", str(HERE / "land_evidence_nguon_test.py"), "--mot-ca", ten_ca],
                       capture_output=True, env=dict(os.environ, LAND_EVIDENCE_NGUON_MA=str(ma), PYTHONDONTWRITEBYTECODE="1"),
                       timeout=300)
    return r.returncode, (r.stdout + r.stderr).decode("utf-8", "replace")


def phan_hang(rc, ra, ten_ca):
    if rc == 0:
        return "SONG_SOT"
    if rc == 3:
        return "GIET" if f"DO:{ten_ca}:" in ra else "TIN_DUNG_GIA"
    return "TIN_DUNG_GIA" if rc == 4 else "HONG"


def chay_dot_bien(ten, cu, moi, ten_ca):
    goc = (HERE / "land_evidence_nguon.py").read_text(encoding="utf-8")
    if goc.count(cu) != 1 or cu == moi:
        return "HONG", f"neo phải xuất hiện đúng 1 lần và đột biến phải đổi mã (thấy {goc.count(cu)})"
    with tempfile.TemporaryDirectory(prefix="len_db_") as thu:
        ban_goc, ban_db = Path(thu) / "goc.py", Path(thu) / f"db_{ten}.py"
        ban_goc.write_text(goc, encoding="utf-8")
        ban_db.write_text(goc.replace(cu, moi), encoding="utf-8")
        rc, ra = chay_con(ten_ca, ban_goc)
        if rc != 0:
            return "HONG", f"ca đích không xanh trên bản gốc (rc={rc}): {ra[-200:]}"
        rc, ra = chay_con(ten_ca, ban_db)
        return phan_hang(rc, ra, ten_ca), ra.strip()[-200:]


def chay_ca(ten):
    """(rc, dòng): 0 đạt · 3 `DO:<ca>:` (chỉ `TinHieuChotCa`) · 4 lỗi vô can — KHÔNG đổi lỗi vô can thành tín hiệu chốt."""
    try:
        CA[ten]()
    except TinHieuChotCa as e:
        return 3, f"DO:{ten}:{e}"
    except Exception as e:
        return 4, f"HONG:{ten}:{type(e).__name__}: {e}"
    return 0, ""


def main(argv):
    if len(argv) == 2 and argv[0] == "--mot-ca" and argv[1] in CA:
        rc, dong = chay_ca(argv[1])
        print(dong)
        return rc
    if argv:
        print("dung: land_evidence_nguon_test.py [--mot-ca TEN]", file=sys.stderr)
        return 2
    kq = [chay_ca(ten) for ten in CA]
    print("".join(f"[{dong}]\n" for rc, dong in kq if rc), end="")
    dat = sum(rc == 0 for rc, _ in kq)
    print(f"CA: {dat}/{len(CA)} dat")
    xau = [f"{ten}: {h} {ct}" for ten, cu, moi, dich in DOT_BIEN for h, ct in [chay_dot_bien(ten, cu, moi, dich)] if h != "GIET"]
    for x in xau:
        print(f"[DOT BIEN KHONG BI GIET DUNG] {x}")
    print(f"DOT BIEN: {len(DOT_BIEN) - len(xau)}/{len(DOT_BIEN)} bi giet dung ly do")
    loi_tk = [f"{ten}: mong {mong}, duoc {h}" for ten, cu, moi, dich, mong in TU_KIEM
              for h in [chay_dot_bien(ten, cu, moi, dich)[0]] if h != mong]
    for x in loi_tk:
        print(f"[TU KIEM] {x}")
    print(f"TU KIEM PHAN HANG: {'DAT' if not loi_tk else 'DO'} ({len(TU_KIEM)} dot bien)")
    ok = dat == len(CA) > 0 and len(DOT_BIEN) > 0 and not xau and not loi_tk
    print(f"TONG: {'DAT' if ok else 'DO'}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
