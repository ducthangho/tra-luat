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
import shutil
import subprocess
import sys
import tarfile
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
# GATE_OUTPUT_DOI_CHIEU_MA: tên DUY NHẤT mà bộ quét ghim của luật 9 (`quet_dot_bien.py`) biết đặt, trỏ bản đột biến của bộ kiểm này (E3).
MA = Path(os.environ.get("LAND_EVIDENCE_NGUON_MA") or os.environ.get("GATE_OUTPUT_DOI_CHIEU_MA") or HERE / "land_evidence_nguon.py")
TEN = "pr9001-thu-land-evidence.yaml"
PROV = "pr9001-thu-provenance"

# L5 — bản kỳ vọng CHÉP RIÊNG dạng VÂN TAY: sha256 của `json.dumps(sorted(MIEN_TRU_CUTOVER.items()))` đo trên `c73af7b`
# (16-10-2026), 28 tên. Thêm/đổi/bỏ một tên hay một băm trong bộ kiểm ⇒ c10 ĐỎ; danh sách đọc được nằm trong bộ kiểm.
L6_TRUONG = ("post_merge_checks", "bookkeeping")   # chép riêng, không đọc từ bộ kiểm: bỏ một trường ở đó ⇒ c16 ĐỎ
KY_VONG_SO_MIEN_TRU = 28
KY_VONG_VAN_TAY_MIEN_TRU = "5311e7557cd75ef2f3b06371c66a4830d4970613c1e98a8fd4af732d7dab2257"
# L7 — cùng cách chép riêng, đo trên `7129f7d` (27-10-2026): 3 hồ sơ khai DAT thiếu `thuc_thi`. Đổi danh sách ⇒ c19 ĐỎ.
L7_KHOA = ("sandbox_mode",)   # chép riêng: bỏ khoá ở bộ kiểm ⇒ c17/c23 ĐỎ
L7_TUY_CHON = ("model", "effort")   # #1240 ADR-0065: ghi nếu đo được (vắng được); đưa lại vào bắt buộc ⇒ c23 ĐỎ
KY_VONG_SO_MIEN_TRU_L7 = 3
KY_VONG_VAN_TAY_MIEN_TRU_L7 = "6b5ef08603e37239742fe5d7fe8cbe933b24e33174cf3af04c453b0e7be83574"
# L8 (#1236 đợt B) — chép riêng như L5/L7: 56 hồ sơ L8 cho ĐỎ trên base đợt B. Đổi bảng ⇒ c28 ĐỎ; c24 đo lại bảng trên chính base ấy.
BASE_B = "f602325574c62184caf16309631f5f680ca5cee2"
KY_VONG_SO_MIEN_TRU_L8 = 56
KY_VONG_VAN_TAY_MIEN_TRU_L8 = "8f81d90d2d6cae3a74651b30cee3c4eb0a0e3748eb498c54824b30029f31b68b"
DOI_CHIEU = (HERE / "gate_output_doi_chieu.py").read_bytes().decode("utf-8")   # module đợt A THẬT; L8 nạp nó từ gốc ĐANG KIỂM
L8_CAM = "def kiem_ho_so(du_lieu, thu_muc):\n    return []\n"   # ca L1–L7 dùng module câm: mỗi ca chỉ đo luật của nó


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
def cay(ho_so, prov=None, doi_chieu=L8_CAM, ten=TEN):
    """Cây tạm: `ops/land/<ten>` = `ho_so`; `prov` = {đường dẫn trong provenance: nội dung} (None ⇒ không tạo thư mục);
    `doi_chieu` = nguồn `ops/gate_output_doi_chieu.py` mà L8 nạp (None ⇒ vắng)."""
    # wp871: newline="" — chế độ văn bản Windows đổi \n thành \r\n, mà c09 băm kỳ vọng trên byte LF (gate-registry windows đỏ).
    with tempfile.TemporaryDirectory(prefix="len_cay_") as thu:
        goc = Path(thu) / "kho"
        pv = ten[: -len("-land-evidence.yaml")] + "-provenance"
        tep = {f"land/{ten}": ho_so} | {f"land/{pv}/{d}": nd for d, nd in (prov or {}).items()}
        tep |= {} if doi_chieu is None else {"gate_output_doi_chieu.py": doi_chieu}
        for duong, nd in tep.items():
            (goc / "ops" / duong).parent.mkdir(parents=True, exist_ok=True)
            (goc / "ops" / duong).write_bytes(nd if isinstance(nd, bytes) else nd.encode("utf-8"))   # bytes: ca sai UTF-8 (c35)
        if prov is not None:
            (goc / "ops/land" / pv).mkdir(exist_ok=True)
        yield goc


def kiem(m, goc):
    with contextlib.redirect_stdout(io.StringIO()) as buf:
        rc = m.main(["--root", str(goc)])
    return rc, buf.getvalue()


def chay(ho_so, prov=None, **kw):
    with cay(ho_so, prov, **kw) as goc:
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
    # B1 (#1236): CLI THẬT như chữ đặc tả — bộ kiểm sập giữa chừng trên cây thật là rc ≠ 0 đo được, không phải lỗi vô can của ca.
    r = subprocess.run([sys.executable, "-B", str(MA), "--root", str(ROOT_THAT)], capture_output=True)
    rc, ra = r.returncode, r.stdout.decode("utf-8", "replace")
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
DU7 = {k: "measured — run.json" for k in L7_KHOA + L7_TUY_CHON}


def hs7(muc, thuc_thi=None):
    """Hồ sơ L7: `assurance_81.reviewer_assurance_81 = muc`; `thuc_thi` dict ⇒ mapping, chuỗi ⇒ vô hướng, None ⇒ không có."""
    hs = f"assurance_81:\n  reviewer_assurance_81: {muc}\n"
    if isinstance(thuc_thi, dict):
        return hs + "  thuc_thi:\n" + "".join(f"    {k}: '{v}'\n" for k, v in thuc_thi.items())
    return hs + (f"  thuc_thi: '{thuc_thi}'\n" if thuc_thi is not None else "")


@ca
def c17_l7_khai_dat_phai_do_thuc_thi():
    """#748 L7: khai §8.1 DAT đòi `thuc_thi.sandbox_mode` là lời khai measured (connector P1 PR #934); #1240 nới model/effort."""
    ky(hs7("DAT", DU7), P7, 0, "DAT đủ ba khoá measured có nguồn")
    ky(hs7("DAT"), P7, 1, "DAT thiếu thuc_thi", "L7 $.assurance_81.thuc_thi:")
    ky(hs7("DAT", "measured — run.json"), P7, 1, "thuc_thi vô hướng", "L7 $.assurance_81.thuc_thi:")
    for k in L7_KHOA:   # review l7d P3: mapping RỖNG vẫn phải kiểm đủ khoá bắt buộc
        ky(hs7("DAT") + "  thuc_thi: {}\n", P7, 1, f"thuc_thi {{}} thiếu {k}", f"L7 $.assurance_81.thuc_thi.{k}:")
    ky(hs7("DAT") + "thuc_thi:\n" + "".join(f"  {k}: '{v}'\n" for k, v in DU7.items()), P7, 1,
       "thuc_thi ở GỐC không thay được thuc_thi dưới assurance_81", "L7 $.assurance_81.thuc_thi:")
    for k in L7_KHOA + L7_TUY_CHON:
        if k in L7_KHOA:
            ky(hs7("DAT", {x: v for x, v in DU7.items() if x != k}), P7, 1, f"thiếu {k}", f"L7 $.assurance_81.thuc_thi.{k}:")
        for sai in ("not_measured — run.json",) * (k in L7_KHOA) + ("da do — run.json", "measuredx run.json"):
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
    for hs in ("assurance_81: DAT\n", "assurance_81: {}\n", "DAT\n", "null\n"):   # review l7e P3: phạm vi áp
        try:
            rc, ra = chay(hs, P7)
        except Exception as e:   # traceback không phải ĐẠT
            rc, ra = -1, f"{type(e).__name__}: {e}"
        bang(rc == 0 and "L7" not in ra, f"L7 không áp cho {hs.strip()!r}: rc={rc} {ra[-200:]}")
    for hs, d in (("assurance_81: [{reviewer_assurance_81: DAT}]\n", "$.assurance_81[0]"), ("x: {reviewer_assurance_81: DAT}\n", "$.x"),
                  ("reviewer_assurance_81: DAT\n", "$"), ("- {assurance_81: {reviewer_assurance_81: DAT}}\n", "$[0].assurance_81")):
        # r2: bốn ca r1 "không áp" (lồng, trong list, ở gốc tài liệu) chính là lỗ r2 đóng ⇒ nay ĐỎ theo r2, KHÔNG theo luật khối gốc
        ky7(hs, 1, f"r2 đòi ĐỎ {hs.strip()!r}", [f"L7 {d}.reviewer_assurance_81" + L7_DO], ["L7 $.assurance_81.thuc_thi"])


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
        (goc / "ops/land" / TEN).write_text(hs, encoding="utf-8", newline="")   # review l7c P3: đĩa giữ byte được miễn trừ
        vp, ghi = m.kiem_ho_so(goc / "ops/land" / TEN, (hs + " ").encode(), goc, __import__("yaml"))
        bang(any(x.startswith("L7 $.assurance_81.thuc_thi:") for x in vp) and "L7 mất miễn trừ" in " ".join(ghi),
             f"băm miễn trừ phải đo CHÍNH ảnh byte đã nạp, không đọc lại đĩa: {vp} {ghi}")
        tep, yml = goc / "ops/land" / TEN, __import__("yaml")   # review l7d P3: miễn trừ gắn TÊN + băm, và chỉ bỏ qua L7
        m.MIEN_TRU_L7.clear()
        m.MIEN_TRU_L7["pr9999-khac-land-evidence.yaml"] = hashlib.sha256(hs.encode()).hexdigest()
        vp, ghi = m.kiem_ho_so(tep, hs.encode(), goc, yml)
        bang(any(x.startswith("L7 $.assurance_81.thuc_thi:") for x in vp) and not ghi,
             f"cùng byte dưới TÊN khác không được miễn trừ: {vp} {ghi}")
        for them, luat in (("x: 'measured — khong-co.json'\n", "L1"), ("trang_thai_packet: {landed: true}\n", "L6")):
            m.MIEN_TRU_L7[TEN] = hashlib.sha256((hs + them).encode()).hexdigest()
            vp, ghi = m.kiem_ho_so(tep, (hs + them).encode(), goc, yml)
            bang(any(x.startswith(luat) for x in vp) and not any(x.startswith("L7") for x in vp)
                 and "L7 miễn trừ" in " ".join(ghi), f"miễn trừ L7 không được xoá vi phạm {luat}: {vp} {ghi}")


@ca
def c19_l7_danh_sach_dong_bang():
    ds = nap().MIEN_TRU_L7
    van_tay = hashlib.sha256(json.dumps(sorted(ds.items())).encode()).hexdigest()
    bang(len(ds) == KY_VONG_SO_MIEN_TRU_L7 and van_tay == KY_VONG_VAN_TAY_MIEN_TRU_L7,
         f"MIEN_TRU_L7 trôi khỏi ảnh chụp: {len(ds)} tên, vân tay {van_tay[:12]}…")


L7_DO = ": khai DAT mà không có khối $.assurance_81 cấp gốc có thuc_thi"


def ky7(hs, mong, ly_do, chua=(), khong=()):
    """L7 r2: đòi rc `mong`, mọi chuỗi `chua` có trong đầu ra, mọi chuỗi `khong` vắng."""
    rc, ra = chay(hs, P7)
    bang(rc == mong and all(x in ra for x in chua) and not any(x in ra for x in khong),
         f"{ly_do}: mong rc={mong} chua={chua} khong={khong}, được {rc} {ra[-300:]}")


@ca
def c20_l7r2_long_mapping_khong_khoi_goc():
    """r2 §2: không có khối $.assurance_81 cấp gốc ⇒ mỗi khoá lồng (mọi độ sâu) chuẩn hoá ra DAT là MỘT vi phạm, nêu đường dẫn."""
    hs = "cap_nhat_20261026:\n  reviewer_assurance_81: {}\n"
    for muc in ("DAT", "Dat", "' DAT '", "ĐẠT", "dat", unicodedata.normalize("NFD", "đạt")):
        ky7(hs.format(muc), 1, f"lồng {muc!r}", ["L7 $.cap_nhat_20261026.reviewer_assurance_81" + L7_DO])
    ky7("reviewer_assurance_81: DAT\n", 1, "khoá ở gốc tài liệu, không phải khối", ["L7 $.reviewer_assurance_81" + L7_DO])
    ky7("a:\n  b:\n    c: {reviewer_assurance_81: DAT}\nd: {reviewer_assurance_81: dat}\n", 1, "hai khoá ⇒ hai vi phạm",
        ["L7 $.a.b.c.reviewer_assurance_81" + L7_DO, "L7 $.d.reviewer_assurance_81" + L7_DO, ": 2 vi phạm"])
    ky7("x:\n  reviewer_assurance_81: DAT\n  thuc_thi: {" + ", ".join(f"{k}: '{v}'" for k, v in DU7.items()) + "}\n", 1,
        "thuc_thi lồng không được nhận", ["L7 $.x.reviewer_assurance_81" + L7_DO])
    ky7("assurance_81: DAT\nx: {reviewer_assurance_81: DAT}\n", 1, "assurance_81 vô hướng không phải khối",
        ["L7 $.x.reviewer_assurance_81" + L7_DO])
    for muc in ("CHUA_DAT", "'chua dat'", "ĐẤT", "DAT_MOT_PHAN", "''"):
        ky7(hs.format(muc), 0, f"lồng {muc!r} không phải DAT ⇒ không áp", khong=["L7"])
    for tho, kieu in (("null", "NoneType"), ("true", "bool"), ("3", "int"), ("[DAT]", "list"), ("{a: DAT}", "dict")):
        ky7(hs.format(tho), 0, f"lồng {tho} không phải chuỗi ⇒ không áp, có ghi chú",
            [f"L7 $.cap_nhat_20261026.reviewer_assurance_81: giá trị {kieu} không phải chuỗi"], [L7_DO])
    ky7("x: {y: DAT, reviewer_assurance_8: DAT, Reviewer_Assurance_81: DAT}\n", 0, "chỉ đúng tên khoá", khong=["L7"])
    ky7("'a.b': {reviewer_assurance_81: DAT}\na: {b: {reviewer_assurance_81: DAT}}\nx: {1: {reviewer_assurance_81: DAT}}\n"
        "'k ý': {reviewer_assurance_81: DAT}\n", 1, "đường dẫn không nhập nhằng (review l7r2 lượt 1 P2)",
        ['L7 $["a.b"].reviewer_assurance_81' + L7_DO, "L7 $.a.b.reviewer_assurance_81" + L7_DO,
         "L7 $.x[int:1].reviewer_assurance_81" + L7_DO, 'L7 $["k ý"].reviewer_assurance_81' + L7_DO, ": 4 vi phạm"])


@ca
def c21_l7r2_long_trong_list():
    """r2 §2: duyệt cả phần tử list — kể cả list ở gốc tài liệu và list trong `assurance_81` vô hướng hoá."""
    ky7("lich_su:\n  - {a: 1}\n  - {reviewer_assurance_81: ' Dat '}\n", 1, "trong phần tử list",
        ["L7 $.lich_su[1].reviewer_assurance_81" + L7_DO])
    ky7("assurance_81: [{reviewer_assurance_81: DAT}]\n", 1, "assurance_81 là list ⇒ không phải khối gốc",
        ["L7 $.assurance_81[0].reviewer_assurance_81" + L7_DO])
    ky7("- {assurance_81: {reviewer_assurance_81: DAT}}\n", 1, "gốc tài liệu là list",
        ["L7 $[0].assurance_81.reviewer_assurance_81" + L7_DO])
    ky7("x: [[{y: [{reviewer_assurance_81: ĐẠT}]}]]\n", 1, "list lồng list", ["L7 $.x[0][0].y[0].reviewer_assurance_81" + L7_DO])
    ky7("x: [{reviewer_assurance_81: CHUA_DAT}]\n", 0, "trong list nhưng CHUA_DAT", khong=["L7"])


@ca
def c22_l7r2_khoi_goc_la_nguon_duy_nhat():
    """r2 §2: có khối $.assurance_81 mapping ⇒ nó là nguồn duy nhất; khoá lồng DAT chỉ là ghi chú nêu đường dẫn."""
    long = "cap_nhat_20261026:\n  reviewer_assurance_81: DAT\nds: [{reviewer_assurance_81: Dat}]\n"
    ghi = [f"L7 {d}: khai DAT lồng bị bỏ qua" for d in ("$.cap_nhat_20261026.reviewer_assurance_81",
                                                         "$.ds[0].reviewer_assurance_81")]
    ky7(hs7("DAT", DU7) + long, 0, "khối gốc DAT đủ đo + lồng DAT", ghi, [L7_DO])
    ky7(hs7("CHUA_DAT") + long, 0, "khối gốc CHUA_DAT + lồng DAT", ghi, [L7_DO])
    ky7(hs7("DAT") + long, 1, "khối gốc DAT thiếu đo vẫn ĐỎ theo r1", ["L7 $.assurance_81.thuc_thi:"] + ghi, [L7_DO])
    ky7(hs7("CHUA_DAT") + "  thuc_thi: {reviewer_assurance_81: DAT}\n", 0, "lồng bên trong chính khối gốc",
        ["L7 $.assurance_81.thuc_thi.reviewer_assurance_81: khai DAT lồng bị bỏ qua"], [L7_DO])
    ky7(hs7("DAT", DU7), 0, "khối gốc không bị ghi chú như khoá lồng", khong=["lồng bị bỏ qua", L7_DO])
    ky7(hs7("CHUA_DAT") + "'assurance_81.x': {reviewer_assurance_81: DAT}\n", 0, "ghi chú nêu đường dẫn có escape",
        ['L7 $["assurance_81.x"].reviewer_assurance_81: khai DAT lồng bị bỏ qua'], [L7_DO])
    ky7("assurance_81: {}\nx: {reviewer_assurance_81: DAT}\n", 0, "khối gốc mapping RỖNG vẫn là khối gốc",
        ["L7 $.x.reviewer_assurance_81: khai DAT lồng bị bỏ qua"], [L7_DO])


@ca
def c23_l7_model_effort_tuy_chon():
    """#1240 ADR-0065 (A4–A6): model/effort là trường ghi nếu đo được — vắng hoặc `not_measured` ⇒ 0 vi phạm L7;
    sandbox_mode vẫn bắt buộc; có mặt mà là rác ⇒ ĐỎ. Đích của m1 (bắt buộc lại), m2 (bỏ sandbox), m3 (nhận mọi giá trị)."""
    sb = {"sandbox_mode": "measured — run.json"}
    kd = {k: f"not_measured — {k} khong co trong bien nhan" for k in L7_TUY_CHON}
    ky7(hs7("DAT", sb | kd), 0, "A4 model/effort not_measured", khong=["L7"])
    ky7(hs7("DAT", sb | {k: f"NOT_MEASURED: {k}" for k in L7_TUY_CHON}), 0, "A4 not_measured hoa thường + ':'", khong=["L7"])
    ky7(hs7("DAT", sb), 0, "A5a chỉ sandbox_mode measured", khong=["L7"])
    for k in L7_TUY_CHON:
        ky7(hs7("DAT", sb | {k: "measured — run.json"}), 0, f"A5a chỉ {k} measured + sandbox", khong=["L7"])
    ky7(hs7("DAT", {k: "measured — run.json" for k in L7_TUY_CHON}), 1, "A5b thiếu sandbox_mode",
          ["L7 $.assurance_81.thuc_thi.sandbox_mode:", ": 1 vi phạm"])
    ky7(hs7("DAT", kd), 1, "A5b not_measured không thay được sandbox_mode",
          ["L7 $.assurance_81.thuc_thi.sandbox_mode:", ": 1 vi phạm"])
    ky7(hs7("DAT", {"sandbox_mode": "not_measured — x"} | kd), 1, "sandbox not_measured vẫn ĐỎ",
          ["L7 $.assurance_81.thuc_thi.sandbox_mode:", ": 1 vi phạm"])
    for k in L7_TUY_CHON:   # A6: rác vẫn ĐỎ, đúng MỘT vi phạm ở đúng khoá
        for tho in ("DAT", "''", "5", "null", "true", "[not_measured — x]", "'not_measuredx'", "'khong do duoc'", "'x not_measured — y'"):
            ky7(hs7("DAT", sb) + f"    {k}: {tho}\n", 1, f"A6 {k} = {tho}",
                  [f"L7 $.assurance_81.thuc_thi.{k}: có mặt mà không phải lời khai measured/not_measured", ": 1 vi phạm"])
    ky7(hs7("CHUA_DAT", {"model": "DAT"}), 0, "không khai DAT ⇒ L7 không áp cho rác tuỳ chọn", khong=["L7"])


NHAN = f"ops/land/{TEN}"
K8 = {"kiem-gate-output.txt": "x"}   # nguồn L1 cho lời khai không trích tệp danh-gia ⇒ chỉ L8 được phép ĐỎ
DG = "danh-gia-gate-output-44669622916.txt"
HS8 = "moc_gate_output: 'measured — kiem-gate-output.txt'\n"
VP8 = "$.moc_gate_output: duong_khong_tep_danh_gia"
L8_MIEN, L8_MAT = "L8 miễn trừ (băm khớp ảnh chụp base đợt B)", "L8 mất miễn trừ: băm lệch ảnh chụp — kiểm đủ"
REF8 = "ops/reviews/wp1236-r9-soan/do_loi_khai.txt"
URL8, SHA8 = "https://github.com/ducthangho/tra-luat/issues/1236#issuecomment-123", "d8cf2ab57f9f25a93cefedcebfb315826b6b78fe"
M8 = f"mien_gate_output: {SHA8} os=ubuntu-latest ly_do=job huy theo chi thi han=2026-12-31"
LANDED8 = "trang_thai_packet: {landed: true}\npost_merge_checks: [{name: g}]\nbookkeeping: [{item: x}]\n"


def prov_that():
    """Hai tệp của `pr1440-wp1319-provenance` (fixture T-v3-pass của đặc tả): tệp đánh giá và provenance của đúng run ấy."""
    goc = ROOT_THAT / "ops/land/pr1440-wp1319-provenance"
    return {d: (goc / d).read_bytes().decode("utf-8") for d in (DG, "ci-provenance-44669622916/provenance.yaml")}


def dong_l8(ra):
    return [x[5:] for x in ra.split("\n") if x.startswith("  L8 ")]


def ky8(ho_so, prov, mong, ly_do, l8=(), dong=(), doi_chieu=DOI_CHIEU, ten=TEN):
    """L8 qua `main` với module đợt A THẬT: đòi rc `mong`, các dòng vi phạm L8 bằng ĐÚNG danh sách `l8`, mỗi phần tử `dong` là
    NGUYÊN MỘT DÒNG của đầu ra."""
    rc, ra = chay(ho_so, prov, doi_chieu=doi_chieu, ten=ten)
    bang(rc == mong and dong_l8(ra) == list(l8) and all(x in ra.split("\n") for x in dong),
         f"{ly_do}: mong rc={mong} l8={list(l8)} dong={list(dong)}, được {rc} {ra[-400:]}")


@contextlib.contextmanager
def cay_tai(commit, *duong):
    """`git archive <commit> <đường dẫn…>` ra thư mục tạm. Không đọc được commit ⇒ ca ĐỎ, không bỏ qua (CI: fetch-depth 0)."""
    with tempfile.TemporaryDirectory(prefix="len_arc_") as thu:
        r = subprocess.run(["git", "-C", str(ROOT_THAT), "archive", "--format=tar", commit, "--", *duong], capture_output=True)
        bang(r.returncode == 0, f"git archive {commit} rc={r.returncode}: {r.stderr[-200:]!r}")
        with tarfile.open(fileobj=io.BytesIO(r.stdout)) as tf:
            tf.extractall(thu, filter="data")
        yield Path(thu)


@ca
def c24_b1_mien_tru_l8_la_dung_tap_do_tren_base():
    """B1: bỏ bảng miễn trừ rồi đo L8 trên MỌI hồ sơ của base đợt B (đầu vào bất biến, đọc bằng `git archive`): tập ĐỎ phải bằng
    `MIEN_TRU_L8` cả tên lẫn băm, và lý do TỪNG hồ sơ phải bằng danh sách của đặc tả. Hồ sơ được L5 miễn (băm khớp) không vào tập.
    Vế "cây thật rc 0" của B1 là c11."""
    m, yml, do, ly = nap(), __import__("yaml"), {}, {}
    bang_mien = dict(m.MIEN_TRU_L8)
    m.MIEN_TRU_L8.clear()
    with cay_tai(BASE_B, "ops/gate_output_doi_chieu.py", ":(glob)ops/land/**/*.yaml", ":(glob)ops/land/**/danh-gia-gate-output-*.txt",
                 ":(glob)ops/land/**/readback-*issuecomment-*.json", REF8) as goc:
        ref = {x.split(" ")[1]: sorted(tuple(v.split(":")[:2]) for v in x.split(" ", 2)[2].split("; "))   # oracle độc lập: bản tham chiếu
               for x in (goc / REF8).read_bytes().decode("utf-8").splitlines() if x.startswith("DO ")}     # của đặc tả, đo trên 8048551
        for tep in sorted((goc / "ops/land").glob("*-land-evidence.yaml")):
            byte = tep.read_bytes()
            bam = hashlib.sha256(byte).hexdigest()
            if m.MIEN_TRU_CUTOVER.get(tep.name) == bam:
                continue
            prov = tep.parent / (tep.name[: -len("-land-evidence.yaml")] + "-provenance")
            if vp := m.l8(tep, byte, m.nap_yaml(yml, byte), prov, goc)[0]:
                do[tep.name], ly[tep.name] = bam, sorted((v[3:].split(": ")[0], v.split(": ")[1].split(":")[0]) for v in vp)
    bang(do == bang_mien, f"MIEN_TRU_L8 lệch tập ĐỎ đo trên {BASE_B[:7]}: thiếu {sorted(set(do) - set(bang_mien))}, thừa "
                          f"{sorted(set(bang_mien) - set(do))}, lệch băm {sorted(t for t in do if bang_mien.get(t, do[t]) != do[t])}")
    bang(ly == ref and sum(map(len, ly.values())) == 93, f"lý do L8 TỪNG hồ sơ (đường dẫn, tên lý do) lệch bản tham chiếu {REF8}: "
                                                        f"{sorted(t for t in set(ly) | set(ref) if ly.get(t) != ref.get(t))}")


@ca
def c25_b2_l8_ho_so_moi_duong_khong_tep_danh_gia():
    ky8(HS8, K8, 1, "B2 lời khai dương chỉ trích kiem-gate", [VP8], [f"ĐỎ {NHAN}: 1 vi phạm"])
    ky8(HS8.replace("measured", "not_measured"), K8, 0, "đối chứng: not_measured không đòi gì", dong=[f"ĐẠT {NHAN}"])
    with cay("x: ok\n", K8, DOI_CHIEU) as goc:   # đĩa SẠCH, byte đưa vào mang lời khai: L8 đo CHÍNH lần nạp đã băm (L4)
        vp, ghi = nap().kiem_ho_so(goc / "ops/land" / TEN, HS8.encode(), goc, __import__("yaml"))
    bang((vp, ghi) == (["L8 " + VP8], []), f"L8 phải đo dữ liệu đã nạp, không đọc lại đĩa: {vp} {ghi}")


@ca
def c26_b6_l8_duong_khop_tep_danh_gia():
    hs, p = f"moc_gate_output: 'measured — {DG}'\n", prov_that()
    ky8(hs, p, 0, "B6 dương khớp tệp đánh giá và provenance", dong=[f"ĐẠT {NHAN}"])
    ky8(LANDED8 + hs, p, 0, "landed có lời khai dương hợp lệ", dong=[f"ĐẠT {NHAN}"])
    del p["ci-provenance-44669622916/provenance.yaml"]
    ky8(hs, p, 1, "đối chứng: thiếu provenance của run", [f"$.moc_gate_output: danh_gia_khong_passed:{DG}:not_measured:provenance_0"])


@ca
def c27_b7_l8_landed_khong_loi_khai():
    """B7 + luật 4 qua L8: ba dạng landed × `True`/`1`, thứ tự ưu tiên `trang_thai_packet`, tên khối `landed_<8 số>` khớp trọn. Hồ sơ
    chỉ có văn xuôi dưới khoá không chứa `gateoutput`; (hồ sơ, rc, landed?) — landed ⇒ đúng một dòng L8."""
    l6, vp = {"post_merge_checks": [{"name": "g"}], "bookkeeping": [{"item": "x"}], "landed_dieu_kien": "Gate output DAT 39/39"}, "$: landed_khong_loi_khai_gate_output"
    for hs, rc, landed in (({"trang_thai_packet": {"landed": True}}, 1, 1), ({"landed": True}, 1, 1),
                           ({"trang_thai_packet": {"landed": False}, "landed_20261124": {"landed": True}}, 1, 1),
                           ({"trang_thai_packet": {"landed": 1}}, 1, 0),   # rc 1 là của L6 (landed phải là bool); L8 không coi 1 là landed
                           ({"landed": 1}, 0, 0), ({"landed_20261124": {"landed": 1}}, 0, 0), ({"trang_thai_packet": {"landed": False}, "landed": True}, 0, 0),
                           ({"trang_thai_packet": "x", "landed": True}, 0, 0), ({"landed_2026112": {"landed": True}}, 0, 0),
                           ({"landed_20261124x": {"landed": True}}, 0, 0), ({"xlanded_20261124": {"landed": True}}, 0, 0),
                           ({"landed_20261124": True}, 0, 0), ({"trang_thai_packet": {"landed": False}}, 0, 0)):
        ky8(json.dumps(hs | l6), None, rc, f"landed {hs}", [vp] * landed)
    ky8(LANDED8 + HS8, K8, 1, "landed + lời khai dương VI PHẠM: cả hai vi phạm", [VP8, vp])


@ca
def c28_b5_l8_danh_sach_dong_bang():
    ds = nap().MIEN_TRU_L8
    van_tay = hashlib.sha256(json.dumps(sorted(ds.items())).encode()).hexdigest()
    bang(len(ds) == KY_VONG_SO_MIEN_TRU_L8 and van_tay == KY_VONG_VAN_TAY_MIEN_TRU_L8,
         f"MIEN_TRU_L8 trôi khỏi ảnh chụp base đợt B: {len(ds)} tên, vân tay {van_tay[:12]}…")


@ca
def c29_b3_l8_mien_tru_theo_ten_va_bam():
    ten = "pr963-wp943-land-evidence.yaml"   # có trong MIEN_TRU_L8; L8 trên nội dung ấy: đúng một vi phạm landed
    hs, nhan, vp = (ROOT_THAT / "ops/land" / ten).read_bytes().decode("utf-8"), f"ops/land/{ten}", "$: landed_khong_loi_khai_gate_output"
    ky8(hs, {}, 1, "bản sao NGUYÊN BYTE: được miễn L8 (rc 1 là của L1, bản sao không mang provenance)", [],
        [f"  ghi chú {nhan}: {L8_MIEN}"], ten=ten)
    ky8(hs + "\n", {}, 1, "B3 sửa một byte ⇒ mất miễn trừ, L8 áp", [vp], [f"  ghi chú {nhan}: {L8_MAT}"], ten=ten)
    with cay(hs, {}, DOI_CHIEU, "x" + ten) as goc:   # cùng byte dưới TÊN khác (tên bảng chỉ là CHUỖI CON) ⇒ không miễn, không ghi chú L8
        vp_, ghi_ = nap().kiem_ho_so(goc / "ops/land" / ("x" + ten), hs.encode(), goc, __import__("yaml"))
    bang([x for x in vp_ if x.startswith("L8")] == ["L8 " + vp] and "L8" not in " ".join(ghi_), f"miễn trừ L8 gắn TÊN: {vp_} {ghi_}")
    with cay(HS8, K8, DOI_CHIEU) as goc:
        m, tep, yml = nap(), goc / "ops/land" / TEN, __import__("yaml")
        m.MIEN_TRU_L8[TEN] = hashlib.sha256(HS8.encode()).hexdigest()
        rc, ra = kiem(m, goc)
        bang(rc == 0 and f"  ghi chú {NHAN}: {L8_MIEN}" in ra.split("\n") and not dong_l8(ra) and L8_MAT not in ra,
             f"băm khớp ⇒ miễn L8 có ghi nhận, rc 0: rc={rc} {ra[-300:]}")
        kq = m.kiem_ho_so(tep, (HS8 + " ").encode(), goc, yml)   # đĩa giữ byte được miễn, byte ĐÃ NẠP thì lệch
        bang(kq == (["L8 " + VP8], [L8_MAT]), f"băm miễn trừ L8 phải đo CHÍNH byte đã nạp, không đọc lại đĩa: {kq}")
        lai = "x: 'measured — khong-co.json'\n" + HS8   # miễn trừ L8 chỉ bỏ L8: vi phạm L1 cùng hồ sơ vẫn còn
        m.MIEN_TRU_L8[TEN] = hashlib.sha256(lai.encode()).hexdigest()
        vp, ghi = m.kiem_ho_so(tep, lai.encode(), goc, yml)
        bang(len(vp) == 1 and vp[0].startswith("L1 $.x:") and ghi == [L8_MIEN], f"miễn trừ L8 không được xoá vi phạm L1: {vp} {ghi}")


@ca
def c30_b4_l8_module_khong_nap_duoc_la_khong_do_duoc():
    """B4: module đối chiếu vắng / hỏng / trả sai kiểu ⇒ rc 2 KHÔNG ĐO ĐƯỢC cho hồ sơ ấy, không bao giờ ĐẠT. Mỗi đường một dòng."""
    kd = f"KHÔNG ĐO ĐƯỢC {NHAN}: L8 không nạp/chạy được gate_output_doi_chieu.py: "
    for nguon, loi in ((None, "FileNotFoundError: "), ("def (\n", "SyntaxError: "), ("x = 1\n", "AttributeError: "),
                       ("def kiem_ho_so(d, t):\n    raise RuntimeError('gia')\n", "RuntimeError: gia\n"),
                       ("raise KeyError('k')\n", "KeyError: 'k'\n"), ("raise SystemExit(0)\n", "SystemExit: 0\n"),
                       ("def kiem_ho_so(d, t):\n    return None\n", "TypeError: kiem_ho_so trả NoneType\n"),
                       ("def kiem_ho_so(d, t):\n    return ()\n", "TypeError: kiem_ho_so trả tuple\n")):
        for hs in (HS8, "x: ok\n"):   # cả hồ sơ có vi phạm L8 lẫn hồ sơ sạch đều không được ĐẠT trên gốc không đo được
            try:
                rc, ra = chay(hs, K8, doi_chieu=nguon)
            except (Exception, SystemExit) as e:   # tính chất ĐANG ĐO: lỗi của module không thoát thành traceback hay mã thoát 0
                rc, ra = -1, f"{type(e).__name__}: {e}"
            bang(rc == 2 and "\n" + kd + loi in "\n" + ra and "1 KHÔNG ĐO ĐƯỢC" in ra and ra.endswith("TỔNG: KHÔNG ĐO ĐƯỢC\n")
                 and f"ĐẠT {NHAN}" not in ra, f"module {nguon!r} ⇒ rc 2 KHÔNG ĐO ĐƯỢC: rc={rc} {ra[-300:]}")
    with cay(HS8, K8, None) as goc:   # chữ B4: chép bộ kiểm vào gốc tạm KHÔNG có module, chạy CLI thật
        (goc / "ops/land_evidence_nguon.py").write_bytes(MA.read_bytes())
        r = subprocess.run([sys.executable, "-B", str(goc / "ops/land_evidence_nguon.py"), "--root", str(goc)], capture_output=True)
        ra = (r.stdout + r.stderr).decode("utf-8", "replace")
        bang(r.returncode == 2 and kd in ra and "Traceback" not in ra, f"CLI gốc tạm thiếu module ⇒ rc 2: {r.returncode} {ra[-300:]}")
        m = nap()   # hồ sơ ĐƯỢC MIỄN L8 cũng không ĐẠT khi module vắng: nạp module đứng TRƯỚC xét miễn trừ
        m.MIEN_TRU_L8[TEN] = hashlib.sha256(HS8.encode()).hexdigest()
        rc, ra = kiem(m, goc)
        bang(rc == 2 and kd + "FileNotFoundError: " in ra, f"hồ sơ được miễn L8 trên gốc thiếu module ⇒ rc 2: rc={rc} {ra[-300:]}")
    ky8(HS8, K8, 1, "đối chứng: module CỦA GỐC ĐANG KIỂM được dùng (không phải bản cạnh bộ kiểm)", ["$: dau_rieng"],
        doi_chieu="def kiem_ho_so(d, t):\n    return ['$: dau_rieng']\n")


@ca
def c31_b8_l8_chay_sau_chot_cutover():
    ten = "pr680-wp676-land-evidence.yaml"   # mục MIEN_TRU_CUTOVER; L8 trên nội dung ấy ra dinh_dang_loi_khai (và landed)
    hs = (ROOT_THAT / "ops/land" / ten).read_bytes().decode("utf-8")
    with cay(hs, None, DOI_CHIEU, ten) as goc:
        m, tep = nap(), goc / "ops/land" / ten
        rc, ra = kiem(m, goc)
        bang(rc == 0 and f"MIỄN TRỪ ops/land/{ten} (băm khớp ảnh chụp cutover)" in ra.split("\n") and "L8" not in ra
             and "· 1/1 miễn trừ (băm khớp) · 0 vi phạm · 0 KHÔNG ĐO ĐƯỢC · tổng 1" in ra, f"B8 L5 miễn ⇒ L8 không chạy: rc={rc} {ra[-300:]}")
        vp, ghi = m.l8(tep, hs.encode(), m.nap_yaml(__import__("yaml"), hs.encode()), goc / "ops/land/x", goc)
    do = ["$.post_merge_checks[1].moc_gate_output: dinh_dang_loi_khai", "$: landed_khong_loi_khai_gate_output"]
    bang((vp, ghi) == (["L8 " + x for x in do], []), f"đối chứng: chính nội dung ấy, khi L8 CHẠY, phải ĐỎ: {vp} {ghi}")
    ky8(hs + "\n", {}, 1, "mất miễn trừ L5 (băm lệch) ⇒ kiểm đủ luật, gồm L8", do,
        [f"MẤT MIỄN TRỪ ops/land/{ten}: băm lệch ảnh chụp cutover — kiểm đủ luật"], ten=ten)


@ca
def c32_l8_ma_tran_token_va_khoa_qua_cong():
    """Luật 4 của đặc tả qua consumer của đợt B (`main` → L8), kỳ vọng suy từ luật: tập token, dấu phân cách sau token, tệp trích,
    chuẩn hoá khoá (giữ chữ SỐ), ba tên phi-lời-khai. Mỗi phần tử một ô; `mong` = phần lý do sau `<đường dẫn>: ` ("" = không vi phạm)."""
    p, sai = prov_that() | K8, "dinh_dang_loi_khai"
    o = [(f"passed — {DG}", ""), (f"Measured: ./{DG}", ""), ("failed — khong trich tep", ""), (f"failed — {DG}", f"danh_gia_khong_failed:{DG}:passed:-"),
         ("measured — kiem-gate-output.txt", "duong_khong_tep_danh_gia"), (f"passed — x/../{DG}", f"tep_danh_gia_khong_hop_le:x/../{DG}"),
         (f"passed — /{DG}", f"tep_danh_gia_khong_hop_le:/{DG}"), (f"passed — {DG} danh-gia-gate-output-1.txt", "tep_danh_gia_khong_hop_le:danh-gia-gate-output-1.txt"),
         ("owner_waived — khong co url", "waiver_khong_co_can_cu:url"), (5, sai), (None, sai), ("", sai), ("da do", sai), ("pass", sai)]
    o += [(t + s, "") for t in ("not_run", " \tNOT_MEASURED", "skipped") for s in ("", " x", "\tx", "—x", "-x", ":x", "(x", ",x", ".x", ";x", "\n")]
    o += [("not_run" + s, sai) for s in ("1", "x", "_", "!x", "/x", "=x", "\nx", "–x")] + [("\nnot_run", sai), ("x not_run", sai)]
    for gt, mong in o:
        ky8(json.dumps({"a": [{"Gate-Output": gt}]}), p, 1 if mong else 0, f"lời khai {gt!r}", [f"$.a[0].Gate-Output: {mong}"] if mong else [])
    for khoa, doc in (("gate_output", 1), ("MOC GATE-OUTPUT 2", 1), ("gate_out_put", 1), ("gate_output_nguon2", 1), ("x_gate_output_nguon", 1),
                      ("gate_output_nguon", 0), ("Gate-Output Nguon_va_gioi_han", 0), ("moc_gate_output_rc_disposition", 0), ("gate2output", 0),
                      ("gate_outpu", 0)):
        ky8(json.dumps({khoa: "da do"}), p, doc, f"khoá {khoa!r}", [f"$.{khoa}: {sai}"] * doc)


def rb8(body=M8, **k):
    return json.dumps({"html_url": URL8, "user": {"login": "ducthangho"}, "author_association": "OWNER", "body": body} | k)


@ca
def c34_l8_ma_tran_mien_qua_cong():
    """Luật 4 qua L8: số URL 0/1/2, dòng miễn khớp trọn sau `strip`, và THỨ TỰ chín điều kiện của `kiem_mien` — mỗi điều kiện một ô một
    lỗi, cạnh ô HAI lỗi đồng thời (lỗi đứng trước phải thắng). `mong` "" = miễn có căn cứ; mỗi ô đo cả hồ sơ thường lẫn hồ sơ landed."""
    kh, rb, mem = f"owner_waived — {URL8} {SHA8}", "readback-1-issuecomment-123.json", {"author_association": "MEMBER"}
    win, han = M8.replace("ubuntu", "windows"), M8.replace("12-31", "02-30")
    for khai, p, mong in (
            (kh, {rb: rb8()}, ""), (kh, {rb: rb8(f"x\n \t{M8}\t \ny")}, ""), (kh, {rb: rb8(M8.replace("os=", "os=windows-latest,"))}, ""),
            (f"owner_waived — {SHA8}", {rb: rb8()}, "url"), (f"{kh} {URL8}", {rb: rb8()}, "url"), (f"{kh} {URL8}4", {}, "url"),
            (kh, {}, "readback"), (kh, {rb: rb8(), "readback-2-issuecomment-123.json": "{"}, "readback"), (kh, {rb: "{"}, "doc_readback"),
            (kh, {rb: rb8(html_url=URL8 + "4")}, "html_url"), (kh, {rb: rb8(html_url=None, **mem)}, "html_url"),
            (kh, {rb: rb8(**mem)}, "tac_gia"), (kh, {rb: rb8(user={"login": "khac"})}, "tac_gia"), (kh, {rb: rb8("khong dong", **mem)}, "tac_gia"),
            (kh, {rb: rb8(f"chi nhac {SHA8}")}, "dong_mien"), (kh, {rb: rb8(M8 + "\n" + M8)}, "dong_mien"), (kh, {rb: rb8("x " + M8)}, "dong_mien"),
            (kh, {rb: rb8(M8 + " x")}, "dong_mien"), (kh, {rb: rb8(han + "\n" + han)}, "dong_mien"),
            (kh, {rb: rb8(han)}, "han"), (kh, {rb: rb8(han.replace("ubuntu", "windows"))}, "han"),
            (kh, {rb: rb8(win)}, "os"), (f"owner_waived — {URL8}", {rb: rb8(win)}, "os"),
            (f"owner_waived — {URL8}", {rb: rb8()}, "sha"), (kh, {rb: rb8(M8.replace(SHA8, SHA8[::-1]))}, "sha")):
        for landed in ({}, {"landed": True}):
            ky8(json.dumps({"gate_output": khai} | landed), p, 1 if mong else 0, f"miễn {mong or 'hợp lệ'}, landed={bool(landed)}: {khai[-45:]!r}",
                [f"$.gate_output: waiver_khong_co_can_cu:{mong}"] * bool(mong) + ["$: landed_khong_loi_khai_gate_output"] * bool(mong and landed))


@ca
def c35_l8_ngu_phap_tep_danh_gia_qua_cong():
    """Luật 4 qua L8: ngữ pháp TỪNG loại dòng của tệp đánh giá (đầu tệp, job, skipped hai dạng, tổng, rỗng) và luật xuống dòng. Mỗi ô
    sửa đúng một chỗ trên bản sao T-v3-pass; `mong` = lý do của `kiem_tep` suy từ K1–K7 ("" = vẫn `passed`)."""
    p = prov_that()
    dg, skip = p[DG], "\nJOB 1 x: skipped"
    job = next(d for d in dg.split("\n") if d.startswith("JOB ") and " -> passed: " in d)
    tong = next(d for d in dg.split("\n") if d.startswith("MOC_GATE_OUTPUT: "))
    for cu, moi, mong in ((dg, dg, ""), (dg, dg.replace("\n", "\r\n"), ""), (job, job + "\n", ""), ("# Danh gia", "# Danh giá", "dau_tep_sai"),
                          ("# Danh gia", "\n# Danh gia", "dau_tep_sai"), (" attempt ", " attempt x", "dau_tep_sai"),
                          (job, job.replace(" -> passed: ", " -> pass: "), "dong_la"), (job, job.replace("JOB ", "Job "), "dong_la"),
                          (job, job.replace(" conclusion=", " ket_luan="), "dong_la"), (job, job + "\n" + job, "job_lap"), (job, job + skip, "dong_la"),
                          (job, job + skip + " (khong tinh)", "tap_skip_lech,dong_skip_sai_phien_ban,moc_lech"),
                          (job, job + skip + " -> not_measured (khong suy pass)", "tap_skip_lech,moc_lech"),
                          (job, job + skip + " (khong tinh) x", "dong_la"), (job, job + skip + " -> not_measured (khong suy pass) x", "dong_la"),
                          (tong, tong.replace("MOC_GATE_OUTPUT: ", "MOC_GATE_OUTPUT "), "dong_la,thieu_moc"), (tong, "", "thieu_moc"),
                          (tong, tong + "\n" + tong, "moc_lap"), (tong, tong.replace(" job co ", " jobs co "), "dong_la,thieu_moc"),
                          (job, job + "\r", "xuong_dong_tron"), (job, job + "\rx", "cr_le")):
        bang(dg.count(cu) == 1, f"neo ô phải xuất hiện đúng một lần trong tệp đánh giá: {cu[:40]!r}")
        ky8(f"moc_gate_output: 'measured — {DG}'\n", p | {DG: dg.replace(cu, moi)}, 1 if mong else 0, f"tệp đánh giá {moi[-40:]!r}",
            [f"$.moc_gate_output: danh_gia_khong_passed:{DG}:not_measured:{mong}"] if mong else [])
    ky8(f"moc_gate_output: 'measured — {DG}'\n", p | {DG: dg.encode("utf-8") + b"\xff"}, 1, "tệp đánh giá có BYTE không phải UTF-8",
        [f"$.moc_gate_output: danh_gia_khong_passed:{DG}:not_measured:khong_phai_utf8"])


# B02 (review mã lượt 3): bảng ngữ pháp của đợt A BẮT BUỘC đi qua L8 — tiền tố ca ⇒ SÀN số phần tử (đo 24-11-2026: 1733 · 3840 · 52 · 36 ·
# 1 · 1280 · 1136 · 318). Mỗi tiền tố phải giải ra ĐÚNG MỘT ca của bộ test đợt A: bỏ, đổi tên hay nhân đôi một ca ⇒ c36 ĐỎ (c38 đo).
A_CA = {"a124": 1700, "a125": 3800, "a126": 50, "a129": 30, "a131": 1, "a132": 1250, "a133": 1100, "a134": 300}


def nap_a(ten):   # nạp theo ĐƯỜNG DẪN trong kho, không theo biến môi trường (bộ quét luật 9 trỏ biến ấy vào bản đột biến)
    spec = importlib.util.spec_from_file_location(ten.replace(".", "_") + "_cho_l8", HERE / ten)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def chon_ca_a(so_dang_ky):
    """Tên ca của bộ test đợt A cho TỪNG tiền tố bắt buộc; không đúng một ca ⇒ ĐỎ (không lọc theo "ca nào đang có")."""
    khop = {tt: [t for t in so_dang_ky if t.split("_")[0] == tt] for tt in A_CA}
    bang(all(len(v) == 1 for v in khop.values()), f"mỗi ca bắt buộc của đợt A phải giải ra ĐÚNG MỘT ca: { {k: v for k, v in khop.items() if len(v) != 1} }")
    return {tt: v[0] for tt, v in khop.items()}


@ca
def c36_l8_ngu_phap_luat_8_qua_bang_cua_dot_a():
    """Luật 8 qua consumer của đợt B: IMPORT (không chép) các ca `*_qua_ho_so` của bộ test đợt A (bộ sinh 128 ký tự ASCII mỗi vị trí + đại
    diện mỗi general category + ngoài BMP, oracle viết từ đặc tả) rồi THAY consumer `kiem_ho_so` của module A bằng `main` → L8 ở đây."""
    a, that, m, yml, dem, ma = nap_a("gate_output_doi_chieu_test.py"), nap_a("gate_output_doi_chieu.py"), nap(), __import__("yaml"), [0], {}
    chon = chon_ca_a(a.CA)   # TRƯỚC mọi việc khác: thiếu / đổi tên / trùng một ca bắt buộc thì ĐỎ ngay, không chạy bảng nào
    m.compile = lambda *x: ma.get(x) or ma.setdefault(x, compile(*x))   # nhớ đệm theo ĐỐI SỐ: cùng byte nguồn ⇒ cùng code, chỉ để nhanh

    def qua_l8(du_lieu, thu):
        byte, dem[0] = yml.safe_dump(du_lieu, allow_unicode=False).encode("ascii"), dem[0] + 1
        bang(m.nap_yaml(yml, byte) == du_lieu, f"hồ sơ YAML phải nạp lại ĐÚNG phần tử bộ sinh đưa ra: {du_lieu!r}")
        with tempfile.TemporaryDirectory(prefix="len_l8_") as tam, contextlib.redirect_stdout(io.StringIO()) as ra:
            if Path(thu) != a.ROOT:   # ca không cần tệp đưa gốc kho làm thư mục provenance: để vắng
                shutil.copytree(thu, Path(tam) / PROV)
            (Path(tam) / TEN).write_bytes(byte)
            m.main(["--root", str(ROOT_THAT), "--tep", str(Path(tam) / TEN)])
        return dong_l8(ra.getvalue())
    that.kiem_ho_so, a._M[:] = qua_l8, [that]   # hàm lá vẫn là module A THẬT; chỉ consumer đổi sang L8
    for tt, ten in chon.items():
        truoc, (rc, dong) = dem[0], a.chay_ca(ten)
        if rc == 4:   # lỗi vô can trong ca của A phải GIỮ là lỗi vô can, không được thành tín hiệu chốt của ca này
            raise RuntimeError(dong)
        bang(rc == 0 and dem[0] - truoc >= A_CA[tt], f"{ten} qua main → L8: {dem[0] - truoc} phần tử (sàn {A_CA[tt]}), rc={rc} {dong[:600]}")


@ca
def c37_l8_van_ban_tu_do_tep_danh_gia_qua_cong():
    """Luật 8 qua L8, ba vị trí VĂN BẢN TỰ DO của tệp đánh giá mà bảng của đợt A không đưa qua consumer: vùng `.*` của dòng đầu, nhãn
    (không chứa `]`), tên dòng skipped (hai dạng). Tệp mẫu mang băm bộ sinh GIẢ có chủ ý: đúng ngữ pháp ⇒ `bo_sinh_la`, sai ⇒ lý do của bộ phân
    tích. Kỳ vọng theo mệnh đề đặc tả: LF tách dòng (`dong_la`; ở dòng đầu là `dau_tep_sai`), CR lẻ ⇒ `cr_le`, nhãn không chứa `]`, tên
    không rỗng và kết thúc ở điểm SỚM NHẤT mà phần còn lại khớp trọn; mọi ký tự khác đi được qua tuyến (128 ASCII, mỗi general
    category trừ Cs, ngoài BMP) là DƯƠNG."""
    ten, cu, v3 = "danh-gia-gate-output-10.txt", ": skipped (khong tinh)", ": skipped -> not_measured (khong suy pass)"
    mau = {"dau": "# Danh gia Gate output run 10 attempt 20 head " + "a" * 40 + " — {}(danh_gia_gate.py sha256 " + "a" * 64 + ")",
           "nhan": "JOB 31 ten [{}] conclusion=success log_sha256=" + "a" * 64 + " -> passed: x",
           "cu": "JOB 42 {}" + cu, "v3": "JOB 53 {}" + v3, "tong": "MOC_GATE_OUTPUT: passed (1/2 job co dau hieu duong)"}
    goc, dung = {"dau": "", "nhan": "nhan", "cu": "x", "v3": "y", "tong": ""}, "bo_sinh_la"
    vu_tru = [*map(chr, range(128)), *nap_a("gate_output_doi_chieu_test.py")._mau_loai_unicode("\r\n", ("Cs",))]
    o = [(vt, c, "dau_tep_sai" if c == "\n" and vt == "dau" else "dong_la" if c == "\n" or c == "]" and vt == "nhan" else "cr_le" if c == "\r" else dung)
         for vt in ("dau", "nhan", "cu", "v3") for c in vu_tru]
    o += [("dau", "x (danh_gia_gate.py sha256 " + "b" * 64 + ") ", dung), ("dau", "café 𐐀 ) (", dung), ("nhan", "", dung),
          ("nhan", "ubuntu-latest, x y [", dung), ("nhan", "a]b", "dong_la"), ("nhan", "a] [b", dung), ("cu", "", "dong_la"), ("v3", "", "dong_la"),   # `a] [b`: tên job lùi thành `ten [a]`, nhãn `b`
          ("cu", "a" + cu + " b", dung), ("cu", "a" + v3 + " b", dung), ("cu", "a" + cu, dung), ("cu", "café 𐐀", dung),
          ("v3", "a" + v3 + " b", dung), ("v3", "a" + cu + " b", dung), ("v3", "a" + v3, dung), ("v3", "café 𐐀", dung)]
    bang(len(vu_tru) >= 150 and len(o) == 4 * len(vu_tru) + 16, f"vũ trụ ký tự co lại: {len(vu_tru)} ký tự, {len(o)} ô")
    for vt, gt, mong in o:
        ky8(json.dumps({"gate_output": f"measured — {ten}"}), {ten: "\n".join(d.format(gt if k == vt else goc[k]) for k, d in mau.items())}, 1,
            f"{vt} {gt!r}", [f"$.gate_output: danh_gia_khong_passed:{ten}:not_measured:{mong}"])


@ca
def c38_c36_do_khi_bang_cua_dot_a_mat_ca():
    """B02: chạy CHÍNH c36 trên sổ đăng ký ca của bộ test đợt A đã bị sửa — bỏ, đổi tên hay nhân đôi TỪNG ca bắt buộc đều phải làm c36
    ĐỎ bằng tín hiệu chốt của nó (không phải lỗi vô can, không phải xanh); sổ nguyên vẹn giải ra đủ tám ca khác nhau."""
    a = nap_a("gate_output_doi_chieu_test.py")
    so, c36 = dict(a.CA), "c36_l8_ngu_phap_luat_8_qua_bang_cua_dot_a"
    chon = chon_ca_a(so)
    bang(len(set(chon.values())) == len(A_CA) == 8, f"sổ nguyên vẹn phải giải ra tám ca khác nhau: {chon}")
    for tt, ten in chon.items():
        for bien, so_moi in (("bỏ", {k: v for k, v in so.items() if k != ten}), ("đổi tên", {("renamed_" + k if k == ten else k): v for k, v in so.items()}),
                             ("nhân đôi", so | {tt + "_ban_sao": so[ten]})):
            a.CA = so_moi
            with mock.patch.dict(CA[c36].__globals__, {"nap_a": lambda _: a}):
                rc, dong = chay_ca(c36)
            bang(rc == 3 and f"DO:{c36}:mỗi ca bắt buộc" in dong and tt in dong, f"{bien} ca {ten} của bộ test đợt A mà c36 không ĐỎ đúng chốt: rc={rc} {dong[:300]}")


@ca
def c33_tong_ket_qua_cong_ci():
    """Luật 7 của đặc tả: đầu ra `main` của CHÍNH tệp này đi qua consumer CI thật (`chay_moi`), hai chế độ nền, ca/đột biến thu nhỏ.
    Tệp này không có ca chỉ-POSIX nên đối chứng "tên chỉ-POSIX lạ" không áp; ba đối chứng còn lại phải ĐỎ."""
    import runpy
    cong = runpy.run_path(str(ROOT_THAT / ".claude/dev/ci_dang_ky_test.py"))
    duong = "ops/land_evidence_nguon_test.py"
    mau, db = {duong: cong["MOI"][duong]}, (("mot", "x", "y", "a"),)
    for windows in (False, True):
        for bien, ca_rc, hang, bang_db in (("dat", 0, "GIET", db), ("ca do", 3, "GIET", db), ("dot bien song", 0, "SONG_SOT", db),
                                           ("mau so 0", 0, "GIET", ())):
            ra = io.StringIO()
            with mock.patch.dict(main.__globals__, {"CA": {"a": None}, "DOT_BIEN": bang_db, "TU_KIEM": (),
                                                    "chay_ca": lambda _: (ca_rc, "ca thu"), "chay_dot_bien": lambda *_: (hang, "")}), \
                    contextlib.redirect_stdout(ra):
                rc = main([])
            txt = ra.getvalue()
            with contextlib.redirect_stdout(io.StringIO()):
                do = [cong["chay_moi"](moi=mau, cach_ly={}, chay_mot=lambda _: (x, txt), doc_moi_truong=lambda: None,
                                       doc_trong_ci=lambda: True, doc_nen_windows=lambda: windows) for x in (rc, 0)]
            bang((rc, do) == ((0, [0, 0]) if bien == "dat" else (1, [1, 1])), f"windows={windows}, {bien}: rc={rc} consumer={do} {txt!r}")
            bang(bien != "dat" or txt.splitlines()[-4:] == ["CA: 1/1 dat", "DOT BIEN: 1/1 bi giet dung ly do",
                                                         "TU KIEM PHAN HANG: DAT (0 dot bien)", "TONG: DAT"], repr(txt))


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
    ("L7_bo_model", 'L7_KHOA_TUY_CHON = ("model", "effort")', 'L7_KHOA_TUY_CHON = ("effort",)', "c17"),
    ("L7_bo_effort", 'L7_KHOA_TUY_CHON = ("model", "effort")', 'L7_KHOA_TUY_CHON = ("model",)', "c17"),
    ("L7_bo_sandbox_mode", 'L7_KHOA = ("sandbox_mode",)', 'L7_KHOA = ()', "c17"),
    # #1240 ADR-0065 — đột biến m1–m3 của đặc tả (A4–A6) cộng biên của mẫu not_measured
    ("m1_model_effort_bat_buoc_lai", 'L7_KHOA = ("sandbox_mode",)', 'L7_KHOA = ("model", "effort", "sandbox_mode")', "c23"),
    ("m2_bo_sandbox_khoi_bat_buoc", 'L7_KHOA = ("sandbox_mode",)', 'L7_KHOA = ()', "c23"),
    ("m3_nhan_moi_gia_tri_khi_co_mat", "for k in L7_KHOA_TUY_CHON if k in tt7 and not _khai_tuy_chon(tt7[k])]",
     "for k in L7_KHOA_TUY_CHON if False]", "c23"),
    ("L7_tuy_chon_bo_not_measured", "bool(RE_KHAI_DO.match(v) or RE_KHAI_KHONG_DO.match(v))", "bool(RE_KHAI_DO.match(v))", "c23"),
    ("L7_tuy_chon_not_measured_khong_bien", r'RE_KHAI_KHONG_DO = re.compile(r"\s*not_measured(?:\s|—|-|:)"',
     r'RE_KHAI_KHONG_DO = re.compile(r"\s*not_measured"', "c23"),
    ("L7_tuy_chon_not_measured_o_giua", "or RE_KHAI_KHONG_DO.match(v))", "or RE_KHAI_KHONG_DO.search(v))", "c23"),
    ("L7_tuy_chon_phan_biet_hoa", 'not_measured(?:\\s|—|-|:)", flags=re.IGNORECASE)', 'not_measured(?:\\s|—|-|:)")', "c23"),
    ("L7_tuy_chon_null_la_vang", "if k in tt7 and not _khai_tuy_chon", "if tt7.get(k) is not None and not _khai_tuy_chon", "c23"),
    ("L7_tuy_chon_khong_chuoi_qua", "return isinstance(v, str) and bool(", "return not isinstance(v, str) or bool(", "c23"),
    ("L7_tuy_chon_rong_la_vang", "if k in tt7 and not _khai_tuy_chon", "if tt7.get(k) and not _khai_tuy_chon", "c23"),
    ("L7_mien_tru_bo_so_bam", "mien = bam is not None and hashlib.sha256(byte).hexdigest() == bam", "mien = bam is not None", "c18"),
    ("L7_bam_doc_lai_dia", "and hashlib.sha256(byte).hexdigest() == bam", "and hashlib.sha256(tep.read_bytes()).hexdigest() == bam", "c18"),
    ("L7_map_rong_bo_kiem", "        elif not mien:\n", "        elif not mien and tt7:\n", "c17"),
    ("L7_thuc_thi_o_goc", 'a81.get("thuc_thi")', '(du_lieu.get("thuc_thi") or a81.get("thuc_thi"))', "c17"),
    ("L7_bam_bo_ten", "mien = bam is not None and hashlib.sha256(byte).hexdigest() == bam",
     "mien = hashlib.sha256(byte).hexdigest() in MIEN_TRU_L7.values()", "c18"),
    ("L7_mien_xoa_vi_pham_truoc", "        if not mien and not isinstance(tt7, dict):\n",
     "        if mien:\n            vp.clear()\n        if not mien and not isinstance(tt7, dict):\n", "c18"),
    ("L7_mien_tru_khong_ghi", '"L7 miễn trừ (băm khớp ảnh chụp, nợ NO-L7-3-HO-SO-KHAI-DAT-THIEU-DO)" if mien', '"" if mien', "c18"),
    # review l7e P3: phạm vi áp. Tương đương (reviewer đo, không cấp mutant): bỏ riêng `bam is not None`, bỏ thay khoảng
    # trắng bằng `_`, thu `elif not mien` thành `elif isinstance(tt7, dict)` (mọi ảnh miễn trừ thật đều thiếu thuc_thi).
    ("L7_dat_o_goc", 'du_lieu.get("assurance_81") if isinstance(du_lieu, dict) else None',
     'du_lieu.get("assurance_81", du_lieu) if isinstance(du_lieu, dict) else None', "c17"),
    ("L7_thieu_khoa_mac_dinh_dat", 'a81.get("reviewer_assurance_81")', 'a81.get("reviewer_assurance_81", "DAT")', "c17"),
    ("L7_goc_list_mo_goi", 'du_lieu.get("assurance_81") if isinstance(du_lieu, dict) else None',
     'du_lieu.get("assurance_81") if isinstance(du_lieu, dict) else (du_lieu[0].get("assurance_81") if isinstance(du_lieu, list)'
     ' and du_lieu and isinstance(du_lieu[0], dict) else None)', "c17"),
    ("L7_bo_kiem_goc_mapping", 'du_lieu.get("assurance_81") if isinstance(du_lieu, dict) else None', 'du_lieu.get("assurance_81")', "c17"),
    ("L7_a81_list_mo_goi", '    if isinstance(a81, dict) and _chuan_hoa_81(',
     '    a81 = a81[0] if isinstance(a81, list) and a81 and isinstance(a81[0], dict) else a81\n    if isinstance(a81, dict) and _chuan_hoa_81(', "c17"),
    ("L7_moi_muc_deu_ap", 'in L7_MUC_DAT:   # L7', 'in L7_MUC_DAT or True:   # L7', "c17"),
    ("L7_khong_chuoi_thanh_dat", "    if not isinstance(v, str):\n        return None\n",
     "    if not isinstance(v, str):\n        return \"DAT\" if v is True or v == 1 else None\n", "c17"),
    ("L7_ghi_chu_khong_can_ten", "        if bam is not None:\n            ghi.append(", "        if True:\n            ghi.append(", "c18"),
    ("L7_khong_bao_gio_mien", "mien = bam is not None and hashlib.sha256(byte).hexdigest() == bam", "mien = False", "c18"),
    ("L7_mat_mien_tru_khong_ghi", 'else "L7 mất miễn trừ: băm lệch ảnh chụp — kiểm đủ")', 'else "L7 kiểm đủ")', "c18"),
    ("L7r2_go_do_sau", "yield from _khoa_81(v, d)   # độ sâu", "pass", "c20"),
    ("L7r2_go_list", "yield from _khoa_81(v, f\"{duong}[{i}]\")   # list", "pass", "c21"),
    ("L7r2_dao_khoi_goc_nguon_duy_nhat", "co_goc = isinstance(a81, dict)", "co_goc = False", "c22"),
    ("L7r2_long_dat_chi_ghi_chu", 'vp.append(f"L7 {d}: khai DAT mà không có', 'ghi.append(f"L7 {d}: khai DAT mà không có', "c20"),
    ("L7r2_bo_chuan_hoa_long", "elif _chuan_hoa_81(v) not in L7_MUC_DAT:", "elif v not in L7_MUC_DAT:", "c20"),
    ("L7r2_khong_chuoi_khong_ghi_chu", '            ghi.append(f"L7 {d}: giá trị {type(v).__name__}', '            (f"L7 {d}: giá trị {type(v).__name__}', "c20"),
    ("L7r2_ghi_chu_long_bi_mat", 'ghi.append(f"L7 {d}: khai DAT lồng bị bỏ qua', '(f"L7 {d}: khai DAT lồng bị bỏ qua', "c22"),
    ("L7r2_khoi_goc_tu_ghi_chu", 'if d == "$.assurance_81.reviewer_assurance_81":', "if False:", "c22"),
    ("L7r2_ten_khoa_khong_chinh_xac", 'if k == "reviewer_assurance_81":', 'if "assurance_8" in str(k).lower():', "c20"),
    ("L7r2_duong_dan_khong_escape", 'return f".{k}" if re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", k) else', 'return f".{k}" if True else', "c20"),
    ("L7r2_khoa_khong_chuoi_nhu_list", 'return f"[{type(k).__name__}:{k!r}]"', 'return f"[{k!r}]"', "c20"),
    ("L7_noi_danh_sach", "MIEN_TRU_L7 = {\n", "MIEN_TRU_L7 = {\n    \"pr9999-tan-cong-land-evidence.yaml\": \"0\" * 64,\n", "c19"),
    # L8 (#1236 đợt B, đặc tả r12 mB1–mB8 + mỗi đường vào của từng chốt một đột biến riêng)
    ("mB1_xoa_muc_mien_tru_cay_that", '    "pr1023-wp1009-r4-land-evidence.yaml": "be6a19a854be2163322d216c1e1d8d725a20a55f97e795aa5428727f57b214f8",\n', "", "c11"),
    ("mB1_xoa_muc_mien_tru_tap_do", '    "pr963-wp943-land-evidence.yaml": "81395ff671200dcdcff2e0aa570be534559ede6ce02555f3da517426df428212",\n', "", "c24"),
    ("mB2_L8_khong_duoc_goi", "vp8, ghi8 = l8(tep, byte, du_lieu, prov, goc)", "vp8, ghi8 = [], []", "c25"),
    ("L8_doc_tep_lan_hai", "= l8(tep, byte, du_lieu, prov, goc)", "= l8(tep, byte, nap_yaml(yaml, tep.read_bytes()), prov, goc)", "c25"),
    ("L8_bo_tien_to_luat", 'return [f"L8 {x}" for x in kq]', 'return [f"{x}" for x in kq]', "c25"),
    ("mB3_mien_tru_theo_ten", 'if MIEN_TRU_L8.get(tep.name) == hashlib.sha256(byte).hexdigest():', "if tep.name in MIEN_TRU_L8:", "c29"),
    ("L8_mien_tru_bo_ten", 'if MIEN_TRU_L8.get(tep.name) == hashlib.sha256(byte).hexdigest():', "if hashlib.sha256(byte).hexdigest() in MIEN_TRU_L8.values():", "c29"),
    ("L8_bam_doc_lai_dia", "== hashlib.sha256(byte).hexdigest():", "== hashlib.sha256(tep.read_bytes()).hexdigest():", "c29"),
    ("L8_mat_mien_tru_khong_ghi", '["L8 mất miễn trừ: băm lệch ảnh chụp — kiểm đủ"] if tep.name in MIEN_TRU_L8 else []', "[]", "c29"),
    ("L8_mat_mien_tru_ghi_ca_ten_la", '— kiểm đủ"] if tep.name in MIEN_TRU_L8 else []', '— kiểm đủ"]', "c29"),
    ("L8_mien_tru_khong_ghi", 'return [], ["L8 miễn trừ (băm khớp ảnh chụp base đợt B)"]', "return [], []", "c29"),
    ("L8_mien_xoa_vi_pham_luat_khac", "return vp + vp8, ghi + ghi8", "return (vp8 if ghi8 else vp + vp8), ghi + ghi8", "c29"),
    ("mB4_nuot_loi_nap", '        raise KhongDoDuoc(f"L8 không nạp/chạy được', '        return [], []\n        (f"L8 không nạp/chạy được', "c30"),
    ("L8_chi_bat_loi_doc_tep", "    except (Exception, SystemExit) as e:", "    except OSError as e:", "c30"),
    ("L8_module_thoat_0_la_dat", "    except (Exception, SystemExit) as e:", "    except Exception as e:", "c30"),
    ("L8_nhan_moi_kieu_tra_ve", "        if not isinstance(kq, list):\n", "        if kq is None:\n", "c30"),
    ("L8_mien_tru_truoc_khi_nap", '    nguon = goc / "ops/gate_output_doi_chieu.py"\n    try:\n',
     '    nguon = goc / "ops/gate_output_doi_chieu.py"\n    if MIEN_TRU_L8.get(tep.name) == hashlib.sha256(byte).hexdigest():\n        return [], []\n    try:\n', "c30"),
    ("L8_nap_module_canh_bo_kiem", 'nguon = goc / "ops/gate_output_doi_chieu.py"',
     'nguon = Path(__file__).resolve().parent / "gate_output_doi_chieu.py"', "c30"),
    ("mB5_noi_danh_sach", "MIEN_TRU_L8 = {\n", "MIEN_TRU_L8 = {\n    \"pr9999-tan-cong-land-evidence.yaml\": \"0\" * 64,\n", "c28"),
    ("mB6_sai_thu_muc_provenance", 'kq = mod.kiem_ho_so(du_lieu, prov)', "kq = mod.kiem_ho_so(du_lieu, prov.parent)", "c26"),
    ("mB7_bo_qua_ho_so_khong_loi_khai", 'kq = mod.kiem_ho_so(du_lieu, prov)', "kq = mod.kiem_ho_so(du_lieu, prov) if mod.loi_khai(du_lieu) else []", "c27"),
    ("mB8_L8_truoc_chot_cutover", "        if (bam := MIEN_TRU_CUTOVER.get(tep.name)) is not None:\n",
     "        v += len(l8(tep, byte, nap_yaml(yaml, byte), tep.parent / \"x\", goc)[0])\n"
     "        if (bam := MIEN_TRU_CUTOVER.get(tep.name)) is not None:\n", "c31"),
    ("L8_ten_cutover_cung_mien_L8", "        if MIEN_TRU_L8.get(tep.name) == hashlib",
     "        if tep.name in MIEN_TRU_CUTOVER or MIEN_TRU_L8.get(tep.name) == hashlib", "c31"),
    ("L8_chi_giu_ly_do_dau", 'kq = mod.kiem_ho_so(du_lieu, prov)', "kq = mod.kiem_ho_so(du_lieu, prov)[:1]", "c24"),
    ("L8_nuot_ly_do_mien", 'kq = mod.kiem_ho_so(du_lieu, prov)', "kq = [x for x in mod.kiem_ho_so(du_lieu, prov) if \"waiver_\" not in x]", "c34"),
    ("L8_nuot_ly_do_tep_danh_gia", 'kq = mod.kiem_ho_so(du_lieu, prov)', "kq = [x for x in mod.kiem_ho_so(du_lieu, prov) if \"danh_gia_khong_passed\" not in x]", "c35"),
    ("L8_chuan_hoa_nfkc_truoc_khi_doi_chieu", 'kq = mod.kiem_ho_so(du_lieu, prov)',
     'kq = mod.kiem_ho_so(json.loads(unicodedata.normalize("NFKC", json.dumps(du_lieu, ensure_ascii=False))), prov)', "c36"),
    ("L8_nuot_ly_do_bo_sinh_la", 'kq = mod.kiem_ho_so(du_lieu, prov)', "kq = [x for x in mod.kiem_ho_so(du_lieu, prov) if \"bo_sinh_la\" not in x]", "c37"),
    ("L8_chi_chuyen_mot_so_ly_do", 'kq = mod.kiem_ho_so(du_lieu, prov)', "kq = [x for x in mod.kiem_ho_so(du_lieu, prov) if \"duong_khong\" in x or x[:3] == \"$: \"]", "c32"),
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
