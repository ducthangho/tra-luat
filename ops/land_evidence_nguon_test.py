#!/usr/bin/env python3
"""Phản chứng CHẠY ĐƯỢC cho `ops/land_evidence_nguon.py` — packet #773, đặc tả r1 mục `nghiem_thu`.

Ca `c*` dựng cây tạm (không chạm `ops/land/**` thật, Q5), dựng lại lượt 1 và 2 của connector trên #771; `c11` chạy CÂY
THẬT (rc 0, m ≤ k). ĐỘT BIẾN sửa BẢN SAO TẠM của bộ kiểm (neo đúng một lần), ca đích chạy ở tiến trình con và phải XANH trên bản
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
import unicodedata
from unittest import mock
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
L6_TRUONG = ("post_merge_checks", "bookkeeping")   # chép riêng, không đọc từ bộ kiểm: bỏ một trường ở đó ⇒ c16 ĐỎ
KY_VONG_SO_MIEN_TRU = 28
KY_VONG_VAN_TAY_MIEN_TRU = "5311e7557cd75ef2f3b06371c66a4830d4970613c1e98a8fd4af732d7dab2257"
# L7 — cùng cách chép riêng, đo trên `f577ab5` (27-10-2026): 3 hồ sơ khai DAT thiếu `thuc_thi`. Đổi danh sách ⇒ c19 ĐỎ.
L7_KHOA = ("model", "effort", "sandbox_mode")   # chép riêng: bỏ một khoá ở bộ kiểm ⇒ c17 ĐỎ
KY_VONG_SO_MIEN_TRU_L7 = 3
KY_VONG_VAN_TAY_MIEN_TRU_L7 = "f70596f243a6da93b79e01c50cee6f4ae9932bf04d399fb674cbc12c44aa5e78"


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
    # wp871: newline="" — chế độ văn bản Windows đổi \n thành \r\n, mà c09 băm kỳ vọng trên byte LF (gate-registry windows đỏ).
    with tempfile.TemporaryDirectory(prefix="len_cay_") as thu:
        goc = Path(thu) / "kho"
        tep = {TEN: ho_so} | {f"{PROV}/{d}": nd for d, nd in (prov or {}).items()}
        for duong, nd in tep.items():
            (goc / "ops/land" / duong).parent.mkdir(parents=True, exist_ok=True)
            (goc / "ops/land" / duong).write_text(nd, encoding="utf-8", newline="")
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


def ky(ho_so, prov, mong, ly_do, chua=""):
    """Một phép đo: hồ sơ + provenance ⇒ đòi đúng rc `mong` và chuỗi `chua` trong đầu ra."""
    rc, ra = chay(ho_so, prov)
    bang(rc == mong and chua in ra, f"{ly_do}: mong rc={mong}, được {rc} {ra[-300:]}")


@ca
def c01_l1_luot1_mergeable_clean_khong_nguon():
    p = {"readback-pr-9001.json": RB_PR}
    ky("dieu_kien:\n  khong_xung_dot: 'measured — mergeable_state clean'\n", p, 1, "lượt 1 #771", "L1 $.dieu_kien.khong_xung_dot")
    ky("x: 'measured — readback-pr-9001.json: mergeable_state unknown'\n", p, 0, "token nguồn CÓ THẬT")
    ky("x: 'measured — readback-pr-9999.json'\n", p, 1, "token trỏ tệp KHÔNG có", "L1")
    ky(f"x: 'measured: ops/land/{PROV}/readback-pr-9001.json'\n", p, 0, "token tương đối gốc kho")
    for tk in (TEN, "../", "ops/land/", "../ops/land/"):   # connector P1 #778: chính hồ sơ và thư mục CHỨA nó không là nguồn
        ky(f"x: 'measured — {tk}'\n", p, 1, f"lời khai chỉ trỏ {tk!r} (tự chứng minh)", "L1")
    ky("x: [{positive: '195/195 hong 0', nguon_positive: " + TEN + "}]\n", p, 1, "nguon_positive trỏ chính hồ sơ", "L2")


@ca
def c02_l1_glob_va_thu_muc():
    for khai, mong in (("trich-log-job/*.txt", 0), ("trich-log-job/*.log", 1), ("trich-log-job/", 0), ("khong-co/", 1)):
        ky(f"x: 'measured - {khai}'\n", {"trich-log-job/a.txt": LOG}, mong, khai)
    with cay("x: 'measured - *.json'\n", {"a.txt": ""}) as goc:   # review F03: glob khớp THƯ MỤC mang đuôi tệp
        (goc / "ops/land" / PROV / "thu-muc.json").mkdir()
        rc, ra = kiem(nap(), goc)
    bang(rc == 1 and "L1" in ra, f"glob chỉ khớp thư mục `thu-muc.json` phải ĐỎ: rc={rc}")


@ca
def c03_l1_token_khong_duoc_thoat_goc():
    with cay("x: 'measured — ../ngoai-goc.json'\n", {"a.json": "{}"}) as goc:   # chỉ nền GỐC KHO phân giải được
        (goc.parent / "ngoai-goc.json").write_text("{}", encoding="utf-8")
        rc, ra = kiem(nap(), goc)
    bang(rc == 1 and "L1" in ra, f"token trỏ RA NGOÀI gốc kho phải ĐỎ: rc={rc} {ra[-200:]}")


@ca
def c04_l1_measured_hoa_thuong_va_khong_phai_khai():
    ky("x: 'Measured — khong nguon'\n", {"a.json": "{}"}, 1, "`Measured —` không được đi vòng L1")
    ky("a: measured\nb: 'not_measured — khong do duoc'\nc: 'measuredx khong'\n", {"a.json": "{}"}, 0,
       "`measured` trần / not_measured / measuredx KHÔNG phải lời khai đo")


@ca
def c05_l2_luot2_positive_phai_co_nguon_chua_nguyen_van():
    p = {"readback-run-1.json": RB_RUN, "trich/u.txt": LOG}
    hs = "post_merge_checks:\n  - {{name: g, positive: 'ubuntu 195/195 hong 0'{}}}\n"
    ky(hs.format(""), p, 1, "thiếu nguon_positive", "thiếu nguon_positive")
    ky(hs.format(", nguon_positive: readback-run-1.json"), p, 1, "lượt 2 #771 (chỉ metadata)", "'195/195'")
    ky(hs.format(", nguon_positive: readback-run-1.json"), p, 1, "lượt 2 #771 (chỉ metadata)", "'hong 0'")
    ky(hs.format(", nguon_positive: [readback-run-1.json, trich/u.txt]"), p, 0, "nguồn chứa nguyên văn")
    for log in (LOG.replace("195/195", "194/195"), LOG.replace("195/195", "195/1950"), LOG.replace("hong 0", "hong 01")):
        ky(hs.format(", nguon_positive: trich/u.txt"), {"trich/u.txt": log}, 1, f"đổi số trong nguồn {log!r}", "L2")
    ky(hs.format(", nguon_positive: trich/khong-co.txt"), p, 1, "nguon_positive vắng tệp", "không có tệp")
    for cao, thap in ((f"ops/land/{PROV}", "ops/land"), ("ops/land", ".")):   # F07 (lượt 5, 6): Q3 TỪNG CẶP nền liền kề —
        with cay(hs.format(", nguon_positive: r.txt"), {}) as goc:   # nền CAO mang số sai, nền THẤP số đúng ⇒ phải ĐỎ L2
            (goc / cao / "r.txt").write_text("1/1", encoding="utf-8")
            (goc / thap / "r.txt").write_text(LOG, encoding="utf-8")
            rc, ra = kiem(nap(), goc)
        bang(rc == 1 and "'195/195'" in ra, f"Q3: {cao} phải được phân giải trước {thap}: rc={rc} {ra[-200:]}")


@ca
def c06_l3_luot2_moc_sau_merged_at():
    p = {"readback-pr-9001.json": RB_PR}
    # 02:58:54Z là mốc thật của connector #771; mốc BẰNG merged_at và mốc YAML không nháy (datetime) cũng phải ĐỎ.
    for khoa, moc, mong in (("pre", "'2026-10-16T02:58:54Z'", 1), ("post", "'2026-10-16T02:58:54Z'", 0),
                            ("pre", "'2026-10-16T02:58:26Z'", 1), ("pre", "2026-10-16T02:59:00Z", 1), ("pre", "'x 2026-10-16T02:49:19Z'", 0)):
        ky(f"pre_merge_checks: []\n{khoa}_merge_checks:\n  - {{name: connector, luc: {moc}}}\n".replace("[]\npre_merge_checks:", ""),
           p, mong, f"{khoa} {moc}")
    for pmc in ("{'2026-10-16T02:59:00Z': ok}", "{c: '2026-10-16T02:59:00Z'}", "{2026-10-16T02:59:00Z: ok}"):   # review F02
        ky(f"pre_merge_checks: {pmc}\n", p, 1, f"pre_merge_checks dạng mapping {pmc}", "L3")
    for moc in ("+00:00", "+0000", "-00:00", "z", " naive"):   # connector P2 #778: mọi dạng múi giờ (thiếu ⇒ UTC) đều phải được so
        hs = f"2026-10-16T03:00:00{moc}".replace(" naive", "")
        ky(f"pre_merge_checks: ['{hs}', '{hs.replace('T', ' ').replace('03:00', '02:00')}']\n", p, 1, f"mốc {hs!r} sau merge", "L3")
    ky("pre_merge_checks: ['2026-10-16 02:00:00+00:00', '2026-10-16t02:00:00Z', '2026-10-16T03:00:00+0100']\n", p, 0,
       "mốc trước merge mọi dạng (03:00+0100 = 02:00Z: độ lệch phải được QUY ĐỔI)")
    for moc in ("2026-10-16T02:00:00-01:00", "2026-10-16T02:00:00-0100"):   # lượt 8 F01: = 03:00Z, sau merge 02:58:26Z
        ky(f"pre_merge_checks: ['{moc}']\n", p, 1, f"độ lệch âm {moc} phải quy đổi sang UTC", "L3")
    ky("pre_merge_checks:\n  - {name: c, luc: '2026-10-16T03:00:00Z'}\n", {"a.json": "{}"}, 0, "không readback", "L3 không áp dụng")


@ca
def c07_l3_chi_doc_readback_cua_chinh_pr():
    p = {"readback-pr-9001.json": RB_PR, "readback-pr-9002.json": RB_PR.replace("02:58:26", "01:00:00"), "readback-pr-9001-commits.json": "[]"}
    ky("pre_merge_checks:\n  - {name: c, luc: '2026-10-16T02:00:00Z'}\n", p, 0, "readback PR lân cận/-commits chen vào L3")


@ca
def c14_cli_moi_to_hop_duong_dan():
    """Review lượt 4 F06: root tương đối/tuyệt đối × tệp tương đối/tuyệt đối — CLI thật, cả bốn phải kiểm và ĐẠT."""
    with cay("x: 'measured — a.json'\n", {"a.json": "{}"}) as goc:
        rel, tuyet = f"ops/land/{TEN}", str(goc / "ops/land" / TEN)
        for root, tep in ((".", rel), (".", tuyet), (str(goc), rel), (str(goc), tuyet)):
            r = subprocess.run([sys.executable, "-B", str(MA), "--root", root, "--tep", tep], capture_output=True, text=True, cwd=goc)
            bang(r.returncode == 0 and "1 ĐẠT" in r.stdout and r.stdout.rstrip().endswith("TỔNG: ĐẠT"),
                 f"--root {root} --tep {tep}: rc={r.returncode} {(r.stdout + r.stderr)[-200:]}")
    with cay("x: ok\n", {}) as goc:   # tên KHÔNG `pr<N>-` ⇒ mọi readback-pr-<số> mang merged_at phải cùng giá trị
        for duong, nd in (("plat-y-land-evidence.yaml", "pre_merge_checks: ['2026-10-16T00:00:00Z']\n"),
                          ("plat-y-provenance/readback-pr-1.json", RB_PR), ("plat-y-provenance/readback-pr-2.json",
                                                                          RB_PR.replace("02:58:26", "01:00:00"))):
            (goc / "ops/land" / duong).parent.mkdir(parents=True, exist_ok=True)
            (goc / "ops/land" / duong).write_text(nd, encoding="utf-8", newline="")
        rc, ra = kiem(nap(), goc)
    bang(rc == 2 and "merged_at khác nhau" in ra, f"readback mâu thuẫn ⇒ rc=2: rc={rc} {ra[-200:]}")


@ca
def c08_l4_khong_do_duoc_khong_bao_gio_dat():
    ky("x: [khong dong\n", {"a.json": "{}"}, 2, "YAML hỏng", "KHÔNG ĐO ĐƯỢC")
    ky("x: 'measured — readback-pr-9001.json'\n", None, 2, "provenance vắng khi có lời khai đo", "provenance")
    ky("pre_merge_checks:\n  - {name: c, luc: '2026-10-16T02:00:00Z'}\n", {"readback-pr-9001.json": "{hong"}, 2, "readback hỏng")
    for hs, rb in (("'2026-99-16T02:00:00Z'", RB_PR), ("'2026-10-16T02:00:00Z'", RB_PR.replace("10-16", "13-16"))):   # F04
        with cay(f"pre_merge_checks: [{hs}]\n", {"readback-pr-9001.json": rb}) as goc:   # đo CLI THẬT: rc + dòng cuối
            r = subprocess.run([sys.executable, "-B", str(MA), "--root", str(goc)], capture_output=True, text=True)
        bang(r.returncode == 2 and r.stdout.rstrip().endswith("TỔNG: KHÔNG ĐO ĐƯỢC"), f"ngày sai {hs} ⇒ rc=2: {r.returncode}")
    for hs in ("x: 'measured — khong nguon'\nx: ok\n", "a: {x: 'measured — khong', x: ok}\n",   # review F01 (lượt 1, 2)
               "null: 'measured — khong'\n~: ok\n", "a: {null: 'measured — khong', null: ok}\n"):
        ky(hs, {"a.json": "{}"}, 2, f"khoá YAML trùng che lời khai {hs!r}", "khoá trùng")
    for hs, ly in (("x: {<<: {a: 'measured — khong', a: ok}}\n", "merge"), ("x: {<<: {null: 'measured — k', null: ok}}\n", "merge"),
                   ("a: &n {x: 1}\nb: {<<: *n, y: 'measured — a.json'}\n", "merge"),   # review lượt 3 F01: merge ngoài mô hình
                   ("a: &n 'measured — khong'\nb: *n\n", "alias"), ("a: &n [*n]\n", "alias")):
        ky(hs, {"a.json": "{}"}, 2, f"{ly} {hs!r}", "ngoài mô hình")
    for hs in ("x: 2026-02-30\n", "pre_merge_checks: [2026-99-16T02:00:00Z]\n", "x: !!int abc\n",   # lượt 3 F04 + lồng sâu
               "x: " + "[" * 1000 + "]" * 1000 + "\n"):
        with cay(hs, {"readback-pr-9001.json": RB_PR}) as goc:   # đo CLI THẬT
            r = subprocess.run([sys.executable, "-B", str(MA), "--root", str(goc)], capture_output=True, text=True)
        bang(r.returncode == 2 and r.stdout.rstrip().endswith("TỔNG: KHÔNG ĐO ĐƯỢC"), f"YAML sai/lồng sâu {hs[:40]!r}: {r.returncode}")
    hs = "x: [{positive: '1/1', nguon_positive: u.txt}]\n"   # lượt 3: lỗi ĐỌC nguồn L2 là KHÔNG ĐO ĐƯỢC
    goc_doc = Path.read_bytes
    with cay(hs, {"u.txt": "1/1"}) as goc, mock.patch.object(Path, "read_bytes", lambda self: (_ for _ in ()).throw(
            OSError("gia")) if self.name == "u.txt" else goc_doc(self)):
        rc, ra = kiem(nap(), goc)
    bang(rc == 2 and "đọc nguon_positive" in ra, f"lỗi đọc nguồn L2 ⇒ rc=2: rc={rc} {ra[-200:]}")
    for hs in ("x: !!set {'measured — khong': null}\n", "x: !!omap [{a: 'measured — khong'}]\n",   # review lượt 2 F05
               "x: !!pairs [{a: 'measured — khong'}]\n", "x: !!binary bWVhc3VyZWQgLSBraG9uZw==\n"):
        ky(hs, {"a.json": "{}"}, 2, f"kiểu YAML ngoài dict/list {hs!r}", "ngoài mô hình")
    ky("pre_merge_checks: ['2026-10-16T02:00:00Z']\n", {"readback-pr-9001.json": RB_PR.replace('"2026-10-16T02:58:26Z"', "null")},
       2, "readback CỦA CHÍNH PR có merged_at null", "merged_at")
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
        def ghi(nd):   # wp871 P3 (Codex lượt 1): CRLF cũng "lệch hash", nên đo chính byte đã ghi
            (goc / "ops/land" / TEN).write_text(nd, encoding="utf-8", newline="")
            bang((goc / "ops/land" / TEN).read_bytes() == nd.encode(), f"byte ghi phải đúng nguyên văn (LF): {nd!r}")
        ghi(hs + " ")
        rc, ra = kiem(m, goc)
        bang(rc == 1 and "MẤT MIỄN TRỪ" in ra and "0/1 miễn trừ" in ra, f"lệch một byte ⇒ kiểm đủ luật: rc={rc} {ra[-300:]}")
        ghi("x: 'measured — a.json'\n")
        rc, ra = kiem(m, goc)
        bang(rc == 0 and "0/1 miễn trừ" in ra, f"mất miễn trừ mà vẫn ĐẠT luật ⇒ xanh: rc={rc} {ra[-300:]}")


@ca
def c13_bam_va_luat_tren_cung_mot_lan_doc():
    with cay("x: ok\n", {"a.json": "{}"}) as goc:   # tệp trên đĩa SẠCH; byte đưa vào (bản đã băm) có lời khai không nguồn
        vp, _ = nap().kiem_ho_so(goc / "ops/land" / TEN, b"x: 'measured - khong'\n", goc, __import__("yaml"))
    bang(any(x.startswith("L1") for x in vp), f"luật phải đo CHÍNH byte đã băm, không đọc lại tệp: {vp}")


@ca
def c10_l5_danh_sach_dong_bang():
    ds = nap().MIEN_TRU_CUTOVER
    van_tay = hashlib.sha256(json.dumps(sorted(ds.items())).encode()).hexdigest()
    bang(len(ds) == KY_VONG_SO_MIEN_TRU and van_tay == KY_VONG_VAN_TAY_MIEN_TRU,
         f"MIEN_TRU_CUTOVER trôi khỏi ảnh chụp cutover: {len(ds)} tên, vân tay {van_tay[:12]}…")


def _cay_that_dat(rc, ra, n):
    """rc 0 và `· m/n miễn trừ` với m ≤ n. m < n hợp lệ: hồ sơ miễn trừ đổi byte mất miễn trừ mà vẫn ĐẠT luật (Q2)."""
    import re
    m = re.search(rf"· (\d+)/{n} miễn trừ", ra)
    return rc == 0 and bool(m) and int(m.group(1)) <= n


@ca
def c11_cay_that_dat_va_mien_tru_du():
    rc, ra = kiem(nap(), ROOT_THAT)
    n = KY_VONG_SO_MIEN_TRU   # c10 khoá danh sách; c15 khoá chính phép so này
    bang(_cay_that_dat(rc, ra, n), f"cây thật phải ĐẠT, mẫu số {n} miễn trừ: rc={rc} {ra[-400:]}")


@ca
def c15_c11_tu_kiem_qua_dau_ra_gia():
    """Phản chứng cho phép so của c11 bằng đầu ra GIẢ — không phụ thuộc hồ sơ thật (review #778 g2 lượt 2 F1)."""
    t = "land_evidence_nguon: 2 ĐẠT · {}/{} miễn trừ (băm khớp) · 0 vi phạm · 0 KHÔNG ĐO ĐƯỢC · tổng 30\nTỔNG: ĐẠT\n"
    nhan = {"m=k": (0, t.format(28, 28)), "m<k": (0, t.format(27, 28))}
    tu_choi = {"m>k": (0, t.format(29, 28)), "mau_so_sai": (0, t.format(27, 27)), "rc_1": (1, t.format(28, 28)),
               "khong_dong": (0, "TỔNG: ĐẠT\n")}
    sai = [k for k, (rc, ra) in nhan.items() if not _cay_that_dat(rc, ra, 28)]
    sai += [k for k, (rc, ra) in tu_choi.items() if _cay_that_dat(rc, ra, 28)]
    bang(not sai, f"phép so c11 sai ở: {sai}")


@ca
def c16_l6_landed_true_phai_co_phan_hoan_tat():
    """#845 spec r1 Q1: landed true đòi post_merge_checks/bookkeeping là list mapping khác rỗng, không chuỗi CHO_DIEN."""
    hs = "trang_thai_packet: {{landed: {}}}\npost_merge_checks: {}\nbookkeeping: {}\n"
    tot, bk = "[{name: g, conclusion: success}]", "[{item: dong issue}]"
    ky(hs.format("true", tot, bk), None, 0, "landed true đủ phần hoàn tất")
    ky(hs.format("true", "'CHO_DIEN — POST_MERGE'", "'CHO_DIEN — BOOKKEEPING'"), None, 1, "ca #840 head 473d56a",
       "L6 $.post_merge_checks")
    ky(hs.format("true", "'chua dien'", bk), None, 1, "chuỗi KHÔNG mang dấu đứng chỗ danh sách", "L6 $.post_merge_checks")
    ky(hs.format("true", "[]", bk), None, 1, "danh sách rỗng", "L6 $.post_merge_checks")
    ky(hs.format("true", "[chuoi]", bk), None, 1, "phần tử không phải mapping", "L6 $.post_merge_checks")
    ky(f"trang_thai_packet: {{landed: true}}\npost_merge_checks: {tot}\n", None, 1, "thiếu bookkeeping", "L6 $.bookkeeping")
    ky(hs.format("true", tot, bk) + "lease: {thu_hoi_cuoi: 'CHO_DIEN — THU_HOI'}\n", None, 1, "dấu trong trường chuỗi",
       "dấu giữ chỗ")
    ky(hs.format("true", "[{CHO_DIEN: x}]", bk), None, 1, "dấu nằm ở KHOÁ", "dấu giữ chỗ")
    # Review #845 lượt 1–2: vá theo từng biên được chỉ thì luôn sót biên kế (A/B/C rồi D–H). Nên đo MA TRẬN: mọi hình dạng sai ×
    # CẢ HAI trường, mọi vị trí dấu, để mỗi chốt có ca riêng bất kể đột biến nhắm vào trường nào.
    sai = (None, "null", "[]", "{a: 1}", "'chua dien'", "[{a: 1}, chuoi]", "[chuoi, {a: 1}]", "[{a: 1}, chuoi, {b: 2}]",
           "[{a: 1}, null]", "[{a: 1}, 3]", "[{a: 1}, 1.5]", "[{a: 1}, []]", "[{a: 1}, true]")   # lượt 3 K/O/P: phần tử sai mọi KIỂU
    for khoa in L6_TRUONG:
        for hinh in sai:
            hop = {"post_merge_checks": tot, "bookkeeping": bk} | {khoa: hinh}
            ho_so = "trang_thai_packet: {landed: true}\n" + "".join(f"{k}: {v}\n" for k, v in hop.items() if v is not None)
            ky(ho_so, None, 1, f"{khoa} = {hinh}", f"L6 $.{khoa}")
    for them in ("x: 'CHO_DIEN dau'\n", "x: 'giua CHO_DIEN giua'\n", "x: 'cuoi CHO_DIEN'\n", "x: [ok, 'a CHO_DIEN']\n",
                 "x: {a: {b: [{c: {d: 'sau CHO_DIEN sau'}}]}}\n", "x: {a: {b: [{c: {CHO_DIEN: 1}}]}}\n", "x: {a: [{ten_CHO_DIEN: 1}]}\n"):
        ky(hs.format("true", tot, bk) + them, None, 1, f"dấu ở {them.strip()}", "dấu giữ chỗ")
    for ho_so, mong in (("trang_thai_packet: {merged: true}\npost_merge_checks: 'CHO_DIEN'\n", 0),   # có mà thiếu landed
                        ("trang_thai_packet: 'landed true'\npost_merge_checks: 'CHO_DIEN'\n", 0),   # không phải mapping
                        ("trang_thai_packet: [landed]\npost_merge_checks: 'CHO_DIEN'\n", 0),   # lượt 3 Q: list cũng không
                        ("trang_thai_packet: {landed: false}\n", 0),   # lượt 3 N: bản nháp thiếu hẳn phần hoàn tất
                        ("trang_thai_packet: {landed: true}\npost_merge_checks: [{}]\nbookkeeping: [{}]\n", 0),   # L: mapping rỗng ĐÚNG Q1.2
                        (hs.format("true", tot, bk) + "x: 'cho_dien Cho_Dien viet thuong'\n", 0),   # M: Q1.3 là NGUYÊN VĂN, phân biệt hoa
                        (hs.format("true", tot, bk) + "x: {1: a, 2026-10-19: b, null: c}\n", 0)):   # khoá không phải chuỗi
        try:   # L6 không áp / không vi phạm, và KHÔNG được ném (traceback không phải ĐỎ)
            rc, ra = chay(ho_so)
        except Exception as e:
            rc, ra = -1, f"{type(e).__name__}: {e}"
        bang(rc == mong and "L6" not in ra, f"{ho_so.splitlines()[0]!r}: rc={rc} {ra[-200:]}")
    for ld in ("'true'", "1", "null", "0", "0.0", "1.0", "[true]", "{a: 1}"):   # lượt 3 I/J: số bằng False/True vẫn không phải bool
        ky(hs.format(ld, tot, bk), None, 1, f"landed {ld} không phải bool", "phải là bool")
    ky(hs.format("false", "'CHO_DIEN — POST_MERGE'", "'CHO_DIEN — BOOKKEEPING'"), None, 0, "bản nháp landed false được giữ chỗ")
    ky("post_merge_checks: 'CHO_DIEN'\n", None, 0, "không có trang_thai_packet.landed ⇒ L6 không áp")


P7 = {"run.json": "{}"}
DU7 = {k: "measured — run.json" for k in L7_KHOA}


def hs7(muc, thuc_thi=None):
    """Hồ sơ L7: `assurance_81.reviewer_assurance_81 = muc`; `thuc_thi` dict ⇒ mapping, chuỗi ⇒ vô hướng, None ⇒ không có."""
    hs = f"assurance_81:\n  reviewer_assurance_81: {muc}\n"
    if isinstance(thuc_thi, dict):
        return hs + "  thuc_thi:\n" + "".join(f"    {k}: '{v}'\n" for k, v in thuc_thi.items())
    return hs + (f"  thuc_thi: '{thuc_thi}'\n" if thuc_thi is not None else "")


@ca
def c17_l7_khai_dat_phai_do_thuc_thi():
    """#748 L7: khai §8.1 DAT đòi `thuc_thi.{model,effort,sandbox_mode}` là lời khai measured (connector P1 PR #934)."""
    ky(hs7("DAT", DU7), P7, 0, "DAT đủ ba khoá measured có nguồn")
    ky(hs7("DAT"), P7, 1, "DAT thiếu thuc_thi", "L7 $.assurance_81.thuc_thi:")
    ky(hs7("DAT", "measured — run.json"), P7, 1, "thuc_thi vô hướng", "L7 $.assurance_81.thuc_thi:")
    for k in L7_KHOA:
        ky(hs7("DAT", {x: v for x, v in DU7.items() if x != k}), P7, 1, f"thiếu {k}", f"L7 $.assurance_81.thuc_thi.{k}:")
        for sai in ("not_measured — run.json", "da do — run.json", "measuredx run.json"):
            ky(hs7("DAT", DU7 | {k: sai}), P7, 1, f"{k} = {sai!r}", f"L7 $.assurance_81.thuc_thi.{k}:")
        for tho in ("null", "true", "3", "['measured — run.json']", "{a: 'measured — run.json'}"):   # review l7a P3: có mặt, không phải chuỗi
            hs = hs7("DAT", {x: v for x, v in DU7.items() if x != k}) + f"    {k}: {tho}\n"
            ky(hs, P7, 1, f"{k} = {tho} (không phải chuỗi)", f"L7 $.assurance_81.thuc_thi.{k}:")
    ky(hs7("DAT", DU7 | {"model": "measured — khong-co.json"}), P7, 1, "measured không nguồn thì L1 bắt", "L1 $.assurance_81")
    nfd = unicodedata.normalize("NFD", "đạt")
    for muc in ("Dat", "' DAT '", "dat", "ĐẠT", "Đạt", "'  đạt  '", nfd):   # chuẩn hoá: hoa thường, khoảng trắng, NFC/NFD
        ky(hs7(muc), P7, 1, f"biến thể {muc!r}", "L7 $.assurance_81.thuc_thi:")
    for muc in ("CHUA_DAT", "CHUA DAT", "'chua dat'", "CHƯA ĐẠT", "DAT_MOT_PHAN", "1", "true", "null", "[DAT]",
                "ĐẤT", "DẠT", "ĐAT", "dát"):   # review l7a P2: chữ khác dấu là giá trị KHÁC, không phải DAT
        ky(hs7(muc), P7, 0, f"{muc!r} không phải DAT ⇒ L7 không áp")
    for hs in ("assurance_81: DAT\n", "assurance_81: [{reviewer_assurance_81: DAT}]\n", "x: {reviewer_assurance_81: DAT}\n"):
        ky(hs, P7, 0, f"không phải mapping assurance_81 ở gốc ⇒ L7 không áp: {hs.strip()!r}")


@ca
def c18_l7_mien_tru_theo_bam():
    hs = hs7("DAT")
    with cay(hs, P7) as goc:
        m = nap()
        m.MIEN_TRU_L7[TEN] = hashlib.sha256(hs.encode()).hexdigest()
        rc, ra = kiem(m, goc)
        bang(rc == 0 and "L7 miễn trừ" in ra, f"băm khớp ⇒ miễn trừ L7 có ghi nhận: rc={rc} {ra[-200:]}")
        for nd, mong in ((hs + " ", 1), (hs7("DAT", DU7), 0)):
            (goc / "ops/land" / TEN).write_text(nd, encoding="utf-8", newline="")
            rc, ra = kiem(m, goc)
            bang(rc == mong and "L7 mất miễn trừ" in ra and "L7 miễn trừ" not in ra,
                 f"băm lệch ⇒ mất miễn trừ, kiểm đủ (mong rc={mong}): rc={rc} {ra[-300:]}")


@ca
def c19_l7_danh_sach_dong_bang():
    ds = nap().MIEN_TRU_L7
    van_tay = hashlib.sha256(json.dumps(sorted(ds.items())).encode()).hexdigest()
    bang(len(ds) == KY_VONG_SO_MIEN_TRU_L7 and van_tay == KY_VONG_VAN_TAY_MIEN_TRU_L7,
         f"MIEN_TRU_L7 trôi khỏi ảnh chụp: {len(ds)} tên, vân tay {van_tay[:12]}…")


@ca
def c12_dong_cuoi_dung_dinh_dang():
    import re
    rc, ra = chay("x: 'measured — a.json'\n", {"a.json": "{}"})
    dong = ra.rstrip("\n").splitlines()[-2:]
    bang(len(dong) == 2 and re.fullmatch(r"land_evidence_nguon: \d+ ĐẠT · \d+/\d+ miễn trừ \(băm khớp\) · \d+ vi phạm · "
                                         r"\d+ KHÔNG ĐO ĐƯỢC · tổng \d+", dong[0]) and dong[1] == "TỔNG: ĐẠT",
         f"định dạng dòng cuối (Q6): {dong}")


# (tên, chuỗi gốc, chuỗi thay, ca đích). Mỗi chốt một đột biến; chuỗi gốc phải xuất hiện ĐÚNG MỘT lần.
DOT_BIEN = (   # (tên, chuỗi gốc, chuỗi thay, TIỀN TỐ ca đích). Chuỗi gốc phải xuất hiện ĐÚNG MỘT lần.
    ("L1_chi_can_co_token", "if not any(phan_giai(t, goc, prov, tep) for t in tk):", "if not tk:", "c01"),
    ("P1_tu_tro_tep_la_nguon", "return r != tep.resolve() and not", "return not", "c01"),
    ("P1_thu_muc_chua_ho_so_la_nguon", "and not (r.is_dir() and _trong_goc(tep, r))", "", "c01"),
    ("P2_chi_nhan_Z", "(?:[Zz]|[+-]\\d{2}:?\\d{2})?(?![\\d:])", "Z", "c06"),
    ("P2_bo_quy_doi_do_lech", "return t if t.tzinfo else t.replace(tzinfo=datetime.timezone.utc)",
     "return t.replace(tzinfo=datetime.timezone.utc)", "c06"),
    ("P2_thieu_mui_gio_khong_khop", "(?:[Zz]|[+-]\\d{2}:?\\d{2})?(?![\\d:])", "(?:[Zz]|[+-]\\d{2}:?\\d{2})(?![\\d:])", "c06"),
    ("L1_glob_rong_van_qua", "            if khop:\n                return khop[0]", "            return nen", "c02"),
    ("L1_bo_chot_trong_goc", "else p.is_file()) and _trong_goc(p, goc)):", "else p.is_file())):", "c03"),
    ("L1_phan_biet_hoa_thuong", ", re.IGNORECASE)", ")", "c04"),
    ("L2_bo_doi_nguon", "            vp.append(f\"L2 {d}: có positive mà thiếu", "            continue  # (f\"L2 {d}: có positive", "c05"),
    ("L2_bo_bien_chu_so", 'else r"(?<![\\d/])" + re.escape(so) + r"(?![\\d/])")', "else re.escape(so))", "c05"),
    ("L3_bang_nhau_la_truoc", "if _thoi_diem(x) >= moc_merge:", "if _thoi_diem(x) > moc_merge:", "c06"),
    ("L3_bo_datetime_khong_nhay", "moc = [v] if isinstance(v, datetime.datetime)", "moc = [] if isinstance(v, datetime.datetime)", "c06"),
    ("L3_doc_moi_readback", 'so = re.match(r"pr(\\d+)-", goc_ten)', "so = None", "c07"),
    ("L4_provenance_vang_van_kiem", "if (khai or co_pos) and not prov.is_dir():", "if False:", "c08"),
    ("L4_khong_do_duoc_thanh_dat", "rc = 1 if v else 2 if u else 0", "rc = 1 if v else 0", "c08"),
    ("L4_rong_thanh_dat", "    if not teps:\n        u += 1", "    if False:\n        u += 1", "c08"),
    ("F01_bo_chot_khoa_trung", "if khoa in da:", "if False:", "c08"),
    ("F01_null_lam_dau_bo_qua", "                if khoa in da:", "                if khoa is not None and khoa in da:", "c08"),
    ("R3_cho_merge", 'isinstance(n, yaml.MappingNode) and any(k.tag ==', 'False and any(k.tag ==', "c08"),
    ("R3_cho_alias", "            if id(n) in da:", "            if False:", "c08"),
    ("R3_vo_huong_sai_traceback", "(yaml.YAMLError, ValueError, TypeError,", "(yaml.YAMLError, TypeError,", "c08"),
    ("R3_long_sau_traceback", "TypeError, OverflowError, RecursionError)", "TypeError, OverflowError)", "c08"),
    ("R3_loi_doc_nguon_thanh_dat", 'raise KhongDoDuoc(f"đọc nguon_positive: {e}")', "return [], []", "c08"),
    ("F05_bo_tu_choi_kieu_la", "if isinstance(nut, (set, frozenset, tuple, bytes, bytearray)):", "if False:", "c08"),
    ("L3_readback_null_bo_qua", "is None and (not so or not t.exists()):", "is None:", "c08"),
    ("F02_bo_khoa_mapping", "[{k: v} for k, v in pmc.items()] if", "list(pmc.values()) if", "c06"),
    ("F02_khoa_khong_chuoi", "        if isinstance(nut, dict):\n            yield d", "        if isinstance(k, str):\n            yield d", "c06"),
    ("F03_glob_chi_can_ton_tai", "khop = [x for x in khop if _la_nguon(x, token, goc, tep)]", "khop = [x for x in khop if x.exists()]", "c02"),
    ("F04_ngay_sai_traceback", "    except ValueError as e:   # regex", "    except KeyError as e:   # regex", "c08"),
    ("L5_doc_tep_lan_hai", "du_lieu = nap_yaml(yaml, byte)", "du_lieu = nap_yaml(yaml, tep.read_bytes())", "c13"),
    ("F06_root_khong_resolve", "goc = Path(a.root).resolve()", "goc = Path(a.root)", "c14"),
    ("L3_readback_mau_thuan_bo_qua", "    if len(gia_tri) > 1:", "    if False:", "c14"),
    ("Q3_ops_land_truoc_prov", "for nen in (prov, goc / THU_MUC, goc):", "for nen in (goc / THU_MUC, prov, goc):", "c05"),
    ("Q3_goc_truoc_ops_land", "for nen in (prov, goc / THU_MUC, goc):", "for nen in (prov, goc, goc / THU_MUC):", "c05"),
    ("L5_bo_so_bam", "if hashlib.sha256(byte).hexdigest() == bam:", "if bam:", "c09"),
    ("L5_noi_danh_sach", "MIEN_TRU_CUTOVER = {\n", "MIEN_TRU_CUTOVER = {\n    \"pr9999-tan-cong-land-evidence.yaml\": \"0\" * 64,\n", "c10"),
    ("L6_bo_ca_luat", 'if isinstance(tt, dict) and "landed" in tt:   # L6', "if False:   # L6", "c16"),
    ("L6_bo_kiem_bool", 'if not isinstance(tt["landed"], bool):', "if False:", "c16"),
    ("L6_ban_nhap_van_kiem", 'elif tt["landed"]:', "else:", "c16"),
    ("L6_chuoi_thay_danh_sach", "if not (isinstance(ds, list) and ds and all(isinstance(x, dict) for x in ds)):", "if not ds:", "c16"),
    ("L6_danh_sach_rong_hop_le", "isinstance(ds, list) and ds and all(", "isinstance(ds, list) and all(", "c16"),
    ("L6_phan_tu_bat_ky", " and all(isinstance(x, dict) for x in ds)", "", "c16"),
    ("L6_bo_bookkeeping", 'L6_PHAN_HOAN_TAT = ("post_merge_checks", "bookkeeping")', 'L6_PHAN_HOAN_TAT = ("post_merge_checks",)', "c16"),
    ("L6_bo_dau_giu_cho", "for d, v in nut if isinstance(v, str) and L6_DAU_GIU_CHO in v]", "for d, v in nut if False]", "c16"),
    ("L6_moi_thanh_mot", " and all(isinstance(x, dict) for x in ds)", " and any(isinstance(x, dict) for x in ds)", "c16"),
    ("L6_bookkeeping_chi_co_mat", "                ds = du_lieu.get(khoa)\n",
     "                ds = du_lieu.get(khoa)\n                if khoa == \"bookkeeping\" and ds:\n                    continue\n", "c16"),
    ("L6_dau_gioi_han_do_sau", "for d, v in nut if isinstance(v, str) and L6_DAU_GIU_CHO in v]",
     "for d, v in nut if d.count(\".\") + d.count(\"[\") <= 3 and isinstance(v, str) and L6_DAU_GIU_CHO in v]", "c16"),
    ("L6_dau_chi_o_dau_chuoi", "and L6_DAU_GIU_CHO in v]", "and v.startswith(L6_DAU_GIU_CHO)]", "c16"),
    ("L6_thieu_pmc_mac_dinh_hop_le", "ds = du_lieu.get(khoa)\n",
     "ds = du_lieu.get(khoa, [{}] if khoa == \"post_merge_checks\" else None)\n", "c16"),
    ("L6_bookkeeping_rong_hop_le", "isinstance(ds, list) and ds and all(",
     "isinstance(ds, list) and (ds or khoa == \"bookkeeping\") and all(", "c16"),
    ("L6_chi_kiem_phan_tu_cuoi", "all(isinstance(x, dict) for x in ds)", "all(isinstance(x, dict) for x in ds[-1:])", "c16"),
    ("L6_bo_kiem_co_landed", 'if isinstance(tt, dict) and "landed" in tt:   # L6', "if isinstance(tt, dict):   # L6", "c16"),
    ("L6_bo_kiem_mapping", 'if isinstance(tt, dict) and "landed" in tt:   # L6', 'if tt and "landed" in tt:   # L6', "c16"),
    ("L6_dau_bo_kiem_chuoi", "for d, v in nut if isinstance(v, str) and L6_DAU_GIU_CHO in v]",
     "for d, v in nut if not isinstance(v, (bool, int, float, list, dict, type(None))) and L6_DAU_GIU_CHO in v]", "c16"),
    # lượt 3 I–Q (review #845): mỗi biên một đột biến
    ("L6_I_nhan_so_0", 'if not isinstance(tt["landed"], bool):', 'if not (isinstance(tt["landed"], bool) or tt["landed"] == 0):', "c16"),
    ("L6_J_nhan_float", 'if not isinstance(tt["landed"], bool):', 'if not isinstance(tt["landed"], (bool, float)):', "c16"),
    ("L6_K_loc_null", "all(isinstance(x, dict) for x in ds)", "all(isinstance(x, dict) for x in ds if x is not None)", "c16"),
    ("L6_L_doi_mapping_khac_rong", "all(isinstance(x, dict) for x in ds)", "all(isinstance(x, dict) and x for x in ds)", "c16"),
    ("L6_M_khong_phan_biet_hoa", "and L6_DAU_GIU_CHO in v]", "and L6_DAU_GIU_CHO in v.upper()]", "c16"),
    ("L6_N_ban_nhap_doi_truong", 'elif tt["landed"]:', 'elif tt["landed"] or not all(k in du_lieu for k in L6_PHAN_HOAN_TAT):', "c16"),
    ("L6_O_null_thanh_hop_le", "ds = du_lieu.get(khoa)\n",
     "ds = du_lieu.get(khoa)\n                ds = [{}] if ds is None and khoa in du_lieu else ds\n", "c16"),
    ("L6_P_phan_tu_so", "all(isinstance(x, dict) for x in ds)", "all(isinstance(x, (dict, int, float)) for x in ds)", "c16"),
    ("L6_Q_list_la_trang_thai", 'if isinstance(tt, dict) and "landed" in tt:   # L6',
     'if isinstance(tt, (dict, list)) and "landed" in tt:   # L6', "c16"),
    ("L7_bo_ca_luat", 'in L7_MUC_DAT:   # L7', 'in ():   # L7', "c17"),
    ("L7_bo_strip", 'normalize("NFC", v).strip().upper()', 'normalize("NFC", v).upper()', "c17"),
    ("L7_bo_viet_hoa", ".strip().upper())", ".strip())", "c17"),
    ("L7_bo_nfc", 'unicodedata.normalize("NFC", v).strip()', 'v.strip()', "c17"),
    ("L7_bo_cach_viet_co_dau", 'L7_MUC_DAT = ("DAT", "ĐẠT")', 'L7_MUC_DAT = ("DAT",)', "c17"),
    ("L7_bo_dau_dai_tra", 'unicodedata.normalize("NFC", v).strip()',
     '"".join(c for c in unicodedata.normalize("NFD", v.replace("đ", "d").replace("Đ", "D")) if not unicodedata.combining(c)).strip()', "c17"),
    ("L7_thieu_thuc_thi_chi_ghi_chu", 'vp.append(f"L7 $.assurance_81.thuc_thi: khai', 'ghi.append(f"L7 $.assurance_81.thuc_thi: khai', "c17"),
    ("L7_bo_kiem_khoa", "        elif not mien:\n", "        elif False:\n", "c17"),
    ("L7_khong_doi_measured", " and RE_KHAI_DO.match(tt7[k]))]", ")]", "c17"),
    ("L7_nhan_khong_phai_chuoi", "if not (isinstance(tt7.get(k), str) and RE_KHAI_DO.match(tt7[k]))]",
     "if not (k in tt7 and (not isinstance(tt7[k], str) or RE_KHAI_DO.match(tt7[k])))]", "c17"),
    ("L7_bo_model", 'L7_KHOA = ("model", "effort", "sandbox_mode")', 'L7_KHOA = ("effort", "sandbox_mode")', "c17"),
    ("L7_bo_effort", 'L7_KHOA = ("model", "effort", "sandbox_mode")', 'L7_KHOA = ("model", "sandbox_mode")', "c17"),
    ("L7_bo_sandbox_mode", 'L7_KHOA = ("model", "effort", "sandbox_mode")', 'L7_KHOA = ("model", "effort")', "c17"),
    ("L7_mien_tru_bo_so_bam", "mien = bam is not None and hashlib.sha256(byte).hexdigest() == bam", "mien = bam is not None", "c18"),
    ("L7_mat_mien_tru_khong_ghi", 'else "L7 mất miễn trừ: băm lệch ảnh chụp — kiểm đủ")', 'else "L7 kiểm đủ")', "c18"),
    ("L7_noi_danh_sach", "MIEN_TRU_L7 = {\n", "MIEN_TRU_L7 = {\n    \"pr9999-tan-cong-land-evidence.yaml\": \"0\" * 64,\n", "c19"),
)
TU_KIEM = (   # (tên, gốc, thay, ca đích, hạng mong đợi)
    ("vo_can_KeyError", "def token_nguon(chuoi):\n", "def token_nguon(chuoi):\n    raise KeyError('vo can')\n", "c01", "TIN_DUNG_GIA"),
    ("chi_them_chu_thich", 'THU_MUC = "ops/land"\n', 'THU_MUC = "ops/land"  # vo hai\n', "c01", "SONG_SOT"),
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


def chay_dot_bien(ten, cu, moi, tien_to):
    khop = [c for c in CA if c.split("_")[0] == tien_to]
    if len(khop) != 1:
        return "HONG", f"tiền tố ca đích {tien_to!r} phải khớp ĐÚNG MỘT ca, khớp {khop}"
    ten_ca = khop[0]
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
