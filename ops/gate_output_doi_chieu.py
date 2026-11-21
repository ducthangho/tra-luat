#!/usr/bin/env python3
"""Đối chiếu lời khai `gate_output` với tệp đánh giá và provenance — packet #1236, đặc tả `ops/specs/wp1236-r9.md` (sha256
e3efa593…, chủ kho duyệt issuecomment-7043381576). Đợt A: module ĐỌC, chưa nối vào cổng nào (B: L8 ở `land_evidence_nguon`;
C: D2b ở `kiem-dong-wp`). Cổng KHÔNG tự chứng minh gate đã đạt: nó chứng minh lời khai dương KHỚP một tệp
`danh-gia-gate-output-<run>.txt` (đầu ra `danh_gia_gate.py` v1/v2/v3), và tệp ấy KHỚP provenance của đúng run (K1–K8).

GIỚI HẠN (đặc tả `chua_do_duoc`): không đọc log thật — tệp đánh giá viết tay chép đúng băm log chỉ lật được `not_measured` thành
`passed` trên job provenance đã ghi `success`; provenance và readback sửa tay được; readback không chứng minh người gõ là chủ kho;
lời khai văn xuôi dưới khoá không chứa `gateoutput` không được đọc (hồ sơ landed buộc phải có lời khai cấu trúc hợp lệ).

CLI: kiem-tep <tệp> --provenance <thư mục> (rc 0 passed · 1 failed · 3 not_measured · 2 tham số sai)
     kiem-ho-so <hồ sơ>... (rc 0 sạch · 1 có vi phạm · 2 tham số sai)
"""
import argparse
import datetime
import json
import os
import re
import sys
from pathlib import Path, PurePosixPath

for _s in (sys.stdout, sys.stderr):
    if hasattr(_s, "reconfigure"):
        _s.reconfigure(encoding="utf-8", errors="backslashreplace")

BO_SINH = {"b87f9697345906e01b85e1db164d9aff2f9021db4bed1c63bc165b59583d9fcd": "v1",
           "539fed68fdd6bdeadb3b70b4ce998419b19afc408ba82bc4152b337d28010a24": "v2",
           "0ea9a5e9b5a663ea6050a934b6116b1d8fcc51b23207510fe9cd056342058faf": "v3"}
CHECK_BAT_BUOC_TEN = ("gate (ubuntu-latest)", "gate-cong-cu-gop (ubuntu-latest)", "gate-ops (ubuntu-latest)",
                      "gate-packet-loop (ubuntu-latest)", "gate-registry (ubuntu-latest)")
RE_DAU = re.compile(r"# Danh gia Gate output run (\d+) attempt (\d+) head ([0-9a-f]{40}) — .*\(danh_gia_gate\.py sha256 ([0-9a-f]{64})\)")
RE_JOB = re.compile(r"JOB (\d+) (.+?) \[([^\]]*)\] conclusion=(\w+) log_sha256=([0-9a-f]{64}) -> (passed|failed|not_measured): (.*)")
RE_SKIP_CU = re.compile(r"JOB (\d+) (.+?): skipped \(khong tinh\)")
RE_SKIP_V3 = re.compile(r"JOB (\d+) (.+?): skipped -> not_measured \(khong suy pass\)")
RE_MOC = re.compile(r"MOC_GATE_OUTPUT: (passed|failed|not_measured) \((\d+)/(\d+) job co dau hieu duong\)")
PHI_LOI_KHAI = frozenset({"gateoutputnguon", "gateoutputnguonvagioihan", "mocgateoutputrcdisposition"})
TOKEN = frozenset({"passed", "measured", "not_measured", "failed", "skipped", "not_run", "owner_waived"})
RE_TOKEN = re.compile(r"\s*([a-z_]+)(?=$|[\s—\-:(,.;])")
RE_TEP_DG = re.compile(r"[A-Za-z0-9_./-]*danh-gia-gate-output-[0-9]+\.txt")   # findall trái-nhất + tham lam ⇒ không cần lookbehind
RE_KHOI_LANDED = re.compile(r"landed_\d{8}")
RE_URL = re.compile(r"https://github\.com/ducthangho/tra-luat/\S*?#issuecomment-(\d+)")
RE_MIEN = re.compile(r"mien_gate_output: ([0-9a-f]{40}) os=([a-z0-9,.-]+) ly_do=(\S.*?) han=(\d{4}-\d{2}-\d{2})")
CHU_KHO = "ducthangho"


def doc_danh_gia(byte):
    """Bộ phân tích ĐÓNG của tệp đánh giá. Trả (dict | None, lý do)."""
    try:
        txt = byte.decode()
    except UnicodeDecodeError:
        return None, ["khong_phai_utf8"]
    dong = (txt[:-1] if txt.endswith("\n") else txt).split("\n")
    if any(d.endswith("\r") for d in dong):
        if not all(d.endswith("\r") for d in dong):
            return None, ["xuong_dong_tron"]
        dong = [d[:-1] for d in dong]
    if any("\r" in d for d in dong):
        return None, ["cr_le"]
    if not (m := RE_DAU.fullmatch(dong[0])):
        return None, ["dau_tep_sai"]
    kq = {"run": int(m[1]), "attempt": int(m[2]), "head": m[3], "bo_sinh": m[4], "jobs": {}, "skip": {}}
    ly, so_moc = [], 0
    for d in dong[1:]:
        if d == "":
            continue
        if j := RE_JOB.fullmatch(d):
            if int(j[1]) in kq["jobs"] or int(j[1]) in kq["skip"]:
                ly.append("job_lap")
            kq["jobs"][int(j[1])] = {"name": j[2], "labels": j[3], "conclusion": j[4], "sha": j[5], "tt": j[6]}
        elif s := (RE_SKIP_CU.fullmatch(d) or RE_SKIP_V3.fullmatch(d)):
            ly += ["job_lap"] if int(s[1]) in kq["jobs"] or int(s[1]) in kq["skip"] else []
            kq["skip"][int(s[1])] = {"v3": s.re is RE_SKIP_V3}
        elif mm := RE_MOC.fullmatch(d):
            so_moc, kq["moc"] = so_moc + 1, (mm[1], int(mm[2]), int(mm[3]))
        else:
            ly.append("dong_la")
    if so_moc == 0:
        ly.append("thieu_moc")
    elif so_moc > 1:
        ly.append("moc_lap")
    return (None if ly else kq), sorted(set(ly))


def _la_so(x):
    return type(x) is int


def _nem(loi):   # G01 lượt 2: lỗi duyệt thư mục KHÔNG được bỏ qua ⇒ lên kiem_tep ⇒ not_measured
    raise loi


def chon_provenance(thu_muc, run, attempt, head):
    """Đúng MỘT tệp `ci_provenance/1` khớp (run, attempt, head) dưới `thu_muc`; không theo symlink. Trả (dict | None, lý do)."""
    import yaml
    thu_muc, ly, khop = Path(thu_muc), [], []
    if thu_muc.is_symlink() or not thu_muc.is_dir():
        return None, (["symlink"] if thu_muc.is_symlink() else []) + ["provenance_0"]
    for goc, thu, tep in os.walk(thu_muc, followlinks=False, onerror=_nem):
        ly += ["symlink" for t in thu if (Path(goc) / t).is_symlink()]   # followlinks=False: KHÔNG đi vào thư mục symlink
        for p in (Path(goc) / t for t in sorted(tep) if t.endswith(".yaml")):
            if p.is_symlink():
                ly.append("symlink")
                continue
            y = yaml.safe_load(p.read_bytes().decode())   # lỗi đọc/parse ⇒ ngoại lệ lên kiem_tep ⇒ not_measured (F02 lượt 1)
            if not (isinstance(y, dict) and y.get("schema") == "ci_provenance/1"):   # F01 lượt 1: lọc kiểu/schema trước
                continue
            r = y["moc"].get("run") if isinstance(y.get("moc"), dict) else None
            if (isinstance(r, dict) and _la_so(r.get("run_id")) and r.get("run_id") == run
                    and _la_so(y.get("attempt_yeu_cau")) and y.get("attempt_yeu_cau") == attempt and r.get("head_sha") == head):
                khop.append(y)
    if len(khop) != 1:
        return None, sorted(set(ly)) + ["provenance_0" if not khop else "provenance_nhieu"]
    return khop[0], sorted(set(ly))


def kiem_tep(tep, thu_muc_provenance):
    """K1–K8. Trả (trạng thái ∈ passed · failed · not_measured, lý do). Ngoại lệ bất kỳ ⇒ not_measured, không traceback."""
    try:
        return _kiem_tep(Path(tep), Path(thu_muc_provenance))
    except Exception as e:
        return "not_measured", [type(e).__name__]


def _kiem_tep(tep, thu_muc):
    d, ly = doc_danh_gia(tep.read_bytes())                                                    # K1
    if d is None:
        return "not_measured", ly
    if d["bo_sinh"] not in BO_SINH:
        return "not_measured", ["bo_sinh_la"]
    y, ly = chon_provenance(thu_muc, d["run"], d["attempt"], d["head"])                       # K2
    if y is None:
        return "not_measured", ly
    moc = y["moc"]   # giữ lý do `symlink` của K2 (F02 lượt 1)
    r = moc["run"]
    if not (r.get("event") == "push" and r.get("loi_khai_rest_path") == ".github/workflows/ci.yml"):     # K3
        ly.append("khong_phai_run_land")
    go = moc.get("gate_output") if isinstance(moc.get("gate_output"), dict) else {}
    P = {}
    for q in (q for q in (go.get("jobs") if isinstance(go.get("jobs"), list) else []) if isinstance(q, dict)):
        ly += ["job_id_trung_provenance"] if q.get("job_id") in P else []
        P[q.get("job_id")] = q
    skip_p, co, tj = {k for k, q in P.items() if q.get("conclusion") == "skipped"}, moc.get("checkout"), go.get("tap_jobs")
    if not (r.get("trang_thai") == "passed" and isinstance(tj, dict) and tj.get("trang_thai") == "passed"
            and isinstance(co, list) and co
            and all(isinstance(c, dict) and (c.get("trang_thai") == "passed"
                                             or (c.get("trang_thai") == "skipped" and c.get("job_id") in skip_p)) for c in co)):
        ly.append("provenance_chua_du")
    if set(d["jobs"]) != set(P) - skip_p:                                                     # K4
        ly.append("tap_job_lech")
    if set(d["skip"]) != skip_p:
        ly.append("tap_skip_lech")
    ldd = y.get("log_day_du") if isinstance(y.get("log_day_du"), dict) else {}
    for k, j in sorted(d["jobs"].items()):
        if (q := P.get(k)) is None:
            continue
        if (q.get("name") != j["name"] or q.get("conclusion") != j["conclusion"]                   # K5
                or ",".join(q.get("labels") or []) != j["labels"]):
            ly.append(f"job_lech:{k}")
        if j["conclusion"] != "success" and j["tt"] != "failed":   # gồm cả tt passed (quét đột biến: vế cũ thừa)
            ly.append(f"ket_luan_lech:{k}")
        if not (isinstance(lg := ldd.get(k), dict) and str(lg.get("sha256")) == j["sha"]):         # K6
            ly.append(f"log_sha_lech:{k}")
    v3 = BO_SINH[d["bo_sinh"]] == "v3"                                                        # K7
    if any(s["v3"] != v3 for s in d["skip"].values()):
        ly.append("dong_skip_sai_phien_ban")
    tts = [j["tt"] for j in d["jobs"].values()]
    n, so_pass = len(tts) + (len(d["skip"]) if v3 else 0), tts.count("passed")   # v3 tính mỗi dòng skipped là một not_measured
    moc_tu = "passed" if n and so_pass == n else ("failed" if "failed" in tts else "not_measured")
    if d["moc"] != (moc_tu, so_pass, n):
        ly.append("moc_lech")
    if ly:
        return "not_measured", ly
    if any(j["tt"] == "failed" for j in d["jobs"].values()):                                    # K8
        return "failed", []
    if d["skip"]:
        return "not_measured", ["co_job_skipped"]
    dat = {j["name"] for j in d["jobs"].values() if j["tt"] == "passed"}
    thieu = [f"check_bat_buoc:{c}" for c in CHECK_BAT_BUOC_TEN if c not in dat]
    return ("not_measured", thieu) if thieu else (moc_tu, [])


def _chuan(k):
    return "".join(c for c in str(k).casefold() if c.isalnum())


def loi_khai(doc, duong="$", _dang=()):
    """Mọi (đường dẫn JSON, giá trị) có tên khoá chuẩn hoá chứa `gateoutput`, trừ ba tên phi-lời-khai; mọi độ sâu, kể cả list.
    Vòng tham chiếu (alias YAML) ⇒ ValueError (F03 lượt 1)."""
    if id(doc) in _dang:
        raise ValueError(f"vong_tham_chieu tại {duong}")
    kq, _dang = [], (_dang + (id(doc),) if isinstance(doc, (dict, list)) else _dang)
    for k, v in (doc.items() if isinstance(doc, dict) else enumerate(doc) if isinstance(doc, list) else ()):
        d = f"{duong}.{k}" if isinstance(doc, dict) else f"{duong}[{k}]"
        if isinstance(doc, dict):
            c = _chuan(k)
            if "gateoutput" in c and c not in PHI_LOI_KHAI:
                kq.append((d, v))
        kq += loi_khai(v, d, _dang)
    return kq


def token(gia_tri):
    m = RE_TOKEN.match(gia_tri.casefold()) if isinstance(gia_tri, str) else None
    return m[1] if m and m[1] in TOKEN else None


def tep_danh_gia(gia_tri):
    return RE_TEP_DG.findall(gia_tri) if isinstance(gia_tri, str) else []


def la_landed(du_lieu):
    """Định nghĩa landed CỦA `ops/kiem_ho_so_land.py`: kiểu a (`trang_thai_packet.landed` nếu có khoá ấy, không thì `landed`
    mức gốc) HOẶC kiểu b (khối gốc `landed_<8 số>` mang `landed is True`)."""
    if not isinstance(du_lieu, dict):
        return False
    if "trang_thai_packet" in du_lieu:
        a = du_lieu["trang_thai_packet"].get("landed") if isinstance(du_lieu["trang_thai_packet"], dict) else None
    else:
        a = du_lieu.get("landed")
    return a is True or any(isinstance(k, str) and RE_KHOI_LANDED.fullmatch(k) and isinstance(v, dict) and v.get("landed") is True
                            for k, v in du_lieu.items())


def _tep_trong(thu_muc, t):
    """Tệp trích `t` tương đối `thu_muc`: cấm tuyệt đối, thành phần `..`, symlink ở mọi thành phần; phải là tệp thường. `./tệp` HỢP LỆ
    (PurePosixPath bỏ thành phần `.`; review mã r9 lượt 6 L03)."""
    pp, p = PurePosixPath(t), Path(thu_muc)
    if pp.is_absolute() or ".." in pp.parts or p.is_symlink():
        return None
    for x in pp.parts:
        p = p / x
        if p.is_symlink():
            return None
    return p if p.is_file() else None


def kiem_mien(gia_tri, thu_muc, head):
    """Điều kiện miễn `owner_waived`. Trả [] nếu đạt, không thì [<điều kiện đầu trượt>]."""
    if len(urls := RE_URL.findall(gia_tri) if isinstance(gia_tri, str) else []) != 1:
        return ["url"]
    url, thu_muc = RE_URL.search(gia_tri)[0], Path(thu_muc)
    rb = ([p for p in thu_muc.glob(f"readback-*issuecomment-{urls[0]}.json") if p.is_file() and not p.is_symlink()]
          if not thu_muc.is_symlink() else [])   # glob trên thư mục vắng/tệp ⇒ rỗng
    if len(rb) != 1:
        return ["readback"]
    try:
        d = json.loads(rb[0].read_bytes().decode())
    except Exception:
        return ["doc_readback"]
    if not isinstance(d, dict) or d.get("html_url") != url:
        return ["html_url"]
    if not (isinstance(d.get("user"), dict) and d["user"].get("login") == CHU_KHO and d.get("author_association") == "OWNER"):
        return ["tac_gia"]
    dong = [m for x in str(d.get("body")).splitlines() if (m := RE_MIEN.fullmatch(x.strip()))]
    if len(dong) != 1:
        return ["dong_mien"]
    m = dong[0]
    try:
        datetime.date.fromisoformat(m[4])
    except ValueError:
        return ["han"]
    if "ubuntu-latest" not in m[2].split(","):
        return ["os"]
    if (m[1] != head) if head is not None else (m[1] not in gia_tri):
        return ["sha"]
    return []


def kiem_ho_so(du_lieu, thu_muc):
    """Vi phạm L8 của một hồ sơ ĐÃ NẠP; `thu_muc` = thư mục provenance của hồ sơ. Rỗng = đạt."""
    vp, hop_le = [], False
    for duong, v in loi_khai(du_lieu):
        if (tk := token(v)) is None:
            vp.append(f"{duong}: dinh_dang_loi_khai")
            continue
        if tk in ("not_measured", "skipped", "not_run"):
            continue
        truoc = len(vp)
        if tk == "owner_waived":
            vp += [f"{duong}: waiver_khong_co_can_cu:{x}" for x in kiem_mien(v, thu_muc, None)]
        else:
            teps = tep_danh_gia(v)
            if tk in ("passed", "measured") and not teps:
                vp.append(f"{duong}: duong_khong_tep_danh_gia")
            can = "failed" if tk == "failed" else "passed"
            for t in teps:
                if (p := _tep_trong(thu_muc, t)) is None:
                    vp.append(f"{duong}: tep_danh_gia_khong_hop_le:{t}")
                    continue
                tt, ly = kiem_tep(p, thu_muc)
                if tt != can:
                    vp.append(f"{duong}: danh_gia_khong_{can}:{t}:{tt}:{','.join(ly) or '-'}")
        if tk != "failed" and len(vp) == truoc:
            hop_le = True
    if la_landed(du_lieu) and not hop_le:
        vp.append("$: landed_khong_loi_khai_gate_output")
    return vp


class _ThamSo(argparse.ArgumentParser):   # review mã r10 lượt 7 M02: lỗi cú pháp cũng theo mẫu stderr `LỖI THAM SỐ:`
    def error(self, message):
        print(f"LỖI THAM SỐ: {message}", file=sys.stderr)
        raise SystemExit(2)


def main(argv=None):
    ap = _ThamSo(description="Đối chiếu gate_output với tệp đánh giá và provenance (wp1236 r10).")
    sp = ap.add_subparsers(dest="lenh", required=True)
    a1 = sp.add_parser("kiem-tep")
    a1.add_argument("tep")
    a1.add_argument("--provenance", required=True)
    sp.add_parser("kiem-ho-so").add_argument("ho_so", nargs="+")
    try:
        a = ap.parse_args(argv)
    except SystemExit as e:
        return 2 if e.code else 0
    if a.lenh == "kiem-tep":
        try:   # H02 lượt 3: stat có thể ném OSError (vd ENAMETOOLONG) ⇒ lỗi tham số, không traceback
            vang = not Path(a.tep).is_file() or not Path(a.provenance).is_dir()
        except OSError:
            vang = True
        if vang:
            print("LỖI THAM SỐ: tệp hoặc thư mục provenance vắng/không đọc được", file=sys.stderr)
            return 2
        tt, ly = kiem_tep(a.tep, a.provenance)
        print(f"{tt} {a.tep} {','.join(ly) or '-'}\nGIỚI HẠN: không đọc log thật; tệp đánh giá và provenance sửa tay được")
        return {"passed": 0, "failed": 1}.get(tt, 3)
    import yaml
    rc = 0
    for hs in map(Path, a.ho_so):
        ten = hs.name[:-len("-land-evidence.yaml")] if hs.name.endswith("-land-evidence.yaml") else hs.stem
        try:
            vp = kiem_ho_so(yaml.safe_load(hs.read_bytes().decode()), hs.parent / f"{ten}-provenance")
        except Exception as e:   # gồm vòng tham chiếu (F03 lượt 1)
            print(f"LỖI THAM SỐ: {hs}: không đọc được ({type(e).__name__})", file=sys.stderr)
            return 2
        print("".join(f"VI_PHAM {hs} {x}\n" for x in vp) + f"{'DO' if vp else 'DAT'} {hs} ({len(vp)} vi phạm)")
        rc = rc or (1 if vp else 0)
    return rc


if __name__ == "__main__":
    sys.exit(main())
