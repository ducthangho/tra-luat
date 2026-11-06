#!/usr/bin/env python3
"""Một nguồn luật cho mốc Gate output (§10.2.2): đối chiếu tệp `gate_output/2` với provenance `ci_provenance/1` — wp1236 đợt A1.

Đặc tả `ops/specs/wp1236-r7.md` (sha256 31415a8a…), duyệt ở #1236 issuecomment-6676924904 (kèm G03/G05/G06/G07/G19/G20).
Phần ĐỌC: sổ luật chỉ-thêm, bộ phân tích `gate_output/2`, `kiem` (K1–K9), lời khai + neo, `kiem_ho_so_gate_output`, CLI. Phần SINH
(`tom`) là đợt A2. Chỉ import CHỈ ĐỌC `ops/ci_provenance.py` cùng thư mục; KHÔNG import hai cổng land (A22) — người gọi truyền `url_hop_le`.
`passed` là điều kiện CẦN cho §10.2.2 Gate output (OS: ubuntu-latest); không phủ runtime/image, artifact, job ngoài `OS_BAT_BUOC`.
Ranh giới tin cậy: dòng `BUOC` là thứ tệp tự khai; bước, kết luận, chế độ shell thì đối chiếu với provenance + workflow.
CLI: `kiem --provenance P --goc G TEP` · `kiem-ho-so --root G TEP_HO_SO`. Thoát 0 passed/ĐẠT · 1 failed/ĐỎ · 2 not_measured/đối số sai.
"""
import datetime
import hashlib
import importlib.util
import json
import re
import subprocess
import sys
from pathlib import Path

import yaml

_s = importlib.util.spec_from_file_location("ci_provenance_cho_gate_output", Path(__file__).with_name("ci_provenance.py"))
cp = importlib.util.module_from_spec(_s)
_s.loader.exec_module(cp)

CHECK_BAT_BUOC = ("gate (ubuntu-latest)", "gate-cong-cu-gop (ubuntu-latest)", "gate-ops (ubuntu-latest)",
                  "gate-packet-loop (ubuntu-latest)", "gate-registry (ubuntu-latest)")   # chép `packet_loop.py:2402`; test so lại


def _b(ten, dau, env=()):   # một bước luật: tập tên REST thay thế, khoá `env:` mức bước cho phép, dấu hiệu [(loại, regex)]
    return {"ten": [ten] if type(ten) is str else list(ten), "env": sorted(env), "dau_hieu": [list(d) for d in dau]}


def _d(r):
    return ("DONG", r)


C, J = ("CUOI", "TỔNG: ĐẠT"), ("JSON_OK", "")
LUAT_v1 = {
    "OS_BAT_BUOC": ["ubuntu-latest"], "KHONG_PHAI_GATE": ["chuan-bi"],
    "ENV_JOB_CHO_PHEP": ["PYTHONDONTWRITEBYTECODE", "PYTHONIOENCODING", "PYTHONUTF8"],
    "JOB_BAT_BUOC": [*CHECK_BAT_BUOC, "gate-nhanh-gop (ubuntu-latest)", *(f"gate-cong-cu (ubuntu-latest, {k})" for k in range(8)),
                     *(f"gate-nhanh-manh (ubuntu-latest, {k})" for k in range(8))],
    "MUC": [
        {"tien_to": "gate (", "os": "ubuntu-latest", "buoc": [
            _b("codex credential selftest (packet #300)", [C]), _b("idiom-ba-ten selftest", [C]),
            _b("eol-policy selftest", [_d(r"(\d+)/\1 dat")]), _b("pre-push selftest", [_d(r"(\d+)/\1 dat")]),
            _b("eol-policy survey", [J]), _b("bundled-fragment check (topology gói)", [J]),
            _b("gen_instructions selftest", [_d(r"== gen_instructions selftest (\d+)/\1 ==")]),
            _b("command-registry unit test (AG-T0-03)", [_d("OK")]),
            _b(("tl selftest (co bang chung exact-identity)", "tl selftest (luot PR — khong sinh bang chung)"), [
                _d(r"== tl selftest (\d+)/\1 =="),
                _d(r'\{"ok": true, "status": "pass", "name": "tl-selftest", "returncode": 0, "duration_seconds": [0-9]+\.[0-9]+, '
                   r'"evidence": "/home/runner/work/tra-luat/tra-luat/scripts/\.tl_state/gate/tl-selftest-Linux\.json"\}')]),
            _b("workflow-audit strict", [J]), _b("golden-test", [J]), _b("doc-claims-check strict", [J]),
            _b("determinism-audit strict", [J]), _b("ci-phamvi guard (bang phu thuoc khop ma)", [_d(r"OK ci_phamvi \(ve BAM\)")]),
            _b("ci-phamvi selftest (phan chung — cong co rang)", [_d(r"== ci_phamvi_test (\d+)/\1 ==")]),
            _b("release-check full", [J]), _b("release-verify strict (lane LAND — manifest committed)", [J]),
            _b("release-bundle x2 cùng SHA-256", [_d("bundle sha256 = [0-9a-f]{64}")])]},
        {"tien_to": "gate-cong-cu (", "os": "ubuntu-latest", "buoc": [_b("G5 manh ban kinh dot bien (#668)", [
            _d(r"cong_cu_test: (\d+)/\1 đạt; tổng=\1, bỏ qua=0, tiền kiểm bỏ qua=0"),
            _d(r"MẢNH [0-7]/8: (\d+)/\1 đột biến bán kính 1 · ghi manh/manh-[0-7]\.txt")], ["CONG_CU_TEST_MANH", "CONG_CU_TEST_MANH_RA"])]},
        {"tien_to": "gate-cong-cu-gop", "os": "ubuntu-latest", "buoc": [_b("G5 gom manh ban kinh dot bien (#668)", [
            _d(r"SỐ LIỆU GOM: ca=(\d+) · đột biến=(\d+) · lỗi đột biến=0")], ["CONG_CU_TEST_GOP_CHE_DO"])]},
        {"tien_to": "gate-nhanh-manh", "os": "ubuntu-latest", "buoc": [_b("chạy mảnh nhanh_don_duoc (targeted_mutant_gate)", [
            _d(r"targeted_mutant_gate MANH [0-7]/8: rc=0 · passed (\d+)/\1")], ["NHANH_DON_DUOC_DICH", "NHANH_DON_DUOC_DICH_RA"])]},
        {"tien_to": "gate-nhanh-gop", "os": "ubuntu-latest", "buoc": [_b("gộp mảnh nhanh_don_duoc (targeted_mutant_gate)", [
            _d("targeted_mutant_gate: DAT — KHONG phai full mutant audit; full_mutant_audit van BAT BUOC truoc merge/land/release")])]},
        {"tien_to": "gate-ops", "os": "ubuntu-latest", "buoc": [
            _b("ci-duong-nhanh selftest (phan loai diff + khoa cau truc if)", [("CUOI", "TONG: DAT")], ["CI_DUONG_NHANH_CHE_DO"]),
            _b("bien-nhan v2 selftest", [_d(r"bien_nhan_v2_test: (\d+)/\1 ca đạt · (\d+)/\2 đột biến thường CÓ RĂNG · (\d+)/\3 ca TỰ KIỂM"
                                            r" đạt · [0-9]+/\2 đột biến thường khai đối chứng"), C]),
            _b("lease-publish selftest (đo lại setup sau G5)", [_d(r"lease_publish: (\d+)/\1 đạt; đã chạy=\1, bỏ qua=0")], ["AL_VER"]),
            _b("don-nhanh selftest (chốt xoá nhánh)", [_d(r"don-nhanh: (\d+)/\1 dat")]),
            _b("bo ca gate chay TRONG cgroup duoc uy quyen (Linux)", [_d(r"gate lifecycle tests: (\d+)/\1 ca QUA \(bo qua 0, hong 0\)")])]},
        {"tien_to": "gate-packet-loop", "os": "ubuntu-latest", "buoc": [_b("packet-loop selftest", [C])]},
        {"tien_to": "gate-registry", "os": "ubuntu-latest", "buoc": [_b("test registry (phạm vi + các bộ chưa được nối)", [
            C, ("KHONG", r"CI_DANG_KY \S+: ĐỎ")], [f"CI_DANG_KY_{x}" for x in ("DAU", "DOT_BIEN_MANH", "GOC", "GOP_KQ", "SU_KIEN", "WORKERS")])]},
    ]}


def bam(luat):
    return hashlib.sha256(json.dumps(luat, ensure_ascii=False, separators=(",", ":")).encode()).hexdigest()


LUAT_PHIEN_BAN = {bam(LUAT_v1): LUAT_v1}   # khoá = băm của giá trị; test chép riêng khoá + băm + miền (A20b)
MIEN_HIEU_LUC = {bam(LUAT_v1): (1, None)}   # (run_id_tu, run_id_den | None), hai đầu tính cả; chỉ-thêm, cũ chỉ được ĐÓNG miền


def _muc(luat, ten):
    return [m for m in luat["MUC"] if ten.startswith(m["tien_to"])]


def kiem_so_luat():
    """Rỗng = sổ lành. G03 (chủ kho): đòi chứa đủ `CHECK_BAT_BUOC` CHỈ ở phiên bản có miền MỞ — phiên bản đã đóng không hỏng theo hằng."""
    loi = [f"khoa_khac_bam:{k[:12]}" for k, v in LUAT_PHIEN_BAN.items() if k != bam(v)]
    loi += ["khoa_thieu_mien"] * (set(LUAT_PHIEN_BAN) != set(MIEN_HIEU_LUC))
    mien = sorted(MIEN_HIEU_LUC.values(), key=lambda m: m[0])
    loi += ["mien_chong"] * any(a[1] is None or a[1] >= b[0] for a, b in zip(mien, mien[1:]))
    loi += ["mien_mo_khac_1"] * (sum(m[1] is None for m in mien) != 1)
    for k, v in LUAT_PHIEN_BAN.items():
        ds = v.get("JOB_BAT_BUOC", [])
        loi += ["job_bat_buoc_trung"] * (len(ds) != len(set(ds)))
        loi += [f"job_khong_dung_mot_muc:{t}" for t in ds if len(_muc(v, t)) != 1]
        if MIEN_HIEU_LUC.get(k, (0, 0))[1] is None and not set(CHECK_BAT_BUOC) <= set(ds):
            loi.append("mien_mo_thieu_check_bat_buoc")
    return loi


RE_DAU = re.compile(r"# gate_output/2 run=([0-9]+) attempt=([0-9]+) head=([0-9a-f]{40}) luat_sha256=([0-9a-f]{64})")
RE_JOB = re.compile(r'JOB ([0-9]+) name=("(?:[^"\\]|\\.)*") labels=(\[[^\]\n]*\]) conclusion=([a-z_]+) log_sha256=([0-9a-f]{64})'
                    r" -> (passed|not_measured|failed|ngoai_pham_vi_os)")
RE_STEP = re.compile(r'  STEP name=("(?:[^"\\]|\\.)*") conclusion=([a-z_]+)')
RE_BUOC = re.compile(r"    BUOC \[([^\]\n]+)\] (CUOI |JSON |KHONG )?(.*)")
RE_MOC = re.compile(r"MOC_GATE_OUTPUT: (passed|not_measured|failed) \(([0-9]+)/([0-9]+) job\)")
RE_ONG = re.compile(r"(?<![|])\|(?![|])")
RE_TAT_TUY_CHON = re.compile(r"errexit|(?<![\w-])\+['\"]*[A-Za-z]*e|\bset\b[^\n]*\+")   # F12: tắt errexit/pipefail, kể cả bước không ống
RE_CAU_TRUC_SHELL = re.compile(r"\b(?:set|builtin|command|shopt|function|eval|source|exec)\b|^\s*\.\s|[(){}`]|\\\s*$", re.M)   # F12


def _json_chuan(raw):   # chuỗi JSON phải đúng dạng chuẩn hoá (để tệp viết tay và `tom` A2 cùng một byte)
    v = json.loads(raw)
    if json.dumps(v, ensure_ascii=False) != raw:
        raise ValueError(raw)
    return v


def phan_tich(text):
    """(dau, jobs, moc) hoặc ValueError. jobs = [{id,name,labels,conclusion,log,mui,steps:[{name,conclusion,buoc:[(nhan,loai,nd)]}]}]."""
    dong = text.split("\n")
    if dong[-1] == "":
        dong.pop()
    if not dong or not (dau := RE_DAU.fullmatch(dong[0])) or not (moc := RE_MOC.fullmatch(dong[-1])):
        raise ValueError("dau_hoac_moc")
    jobs = []
    for d in dong[1:-1]:
        if m := RE_JOB.fullmatch(d):
            jobs.append({"id": int(m[1]), "name": _json_chuan(m[2]), "labels": _json_chuan(m[3]), "conclusion": m[4], "log": m[5],
                         "mui": m[6], "steps": []})
        elif (m := RE_STEP.fullmatch(d)) and jobs:
            jobs[-1]["steps"].append({"name": _json_chuan(m[1]), "conclusion": m[2], "buoc": []})
        elif (m := RE_BUOC.fullmatch(d)) and jobs and jobs[-1]["steps"]:
            jobs[-1]["steps"][-1]["buoc"].append((m[1], (m[2] or "").strip(), m[3]))
        else:
            raise ValueError("dong_la")
    return dau, jobs, moc


def _bo_nhay(run):   # bỏ chú thích và chuỗi nháy trước khi tìm `|`
    run = re.sub(r"'[^']*'|\"(?:[^\"\\]|\\.)*\"", "", run)
    return re.sub(r"(?m)(^|\s)#.*$", r"\1", run)


def che_do_shell(run, shell):   # F12 Review Rescue (#1236 6690900537): DANH SÁCH CHO PHÉP, không suy luận trạng thái từ `set`
    if RE_TAT_TUY_CHON.search(re.sub(r"\\\s*\n", " ", run)):
        return "tat_tuy_chon_shell"   # mọi bước: `set +e`, `set +o …`, `builtin set '+e'`… (nối dòng `\` đã gộp) ⇒ không xác lập
    if not RE_ONG.search(_bo_nhay(run)):
        return None   # bước không ống: không cần pipefail
    if shell != "bash":
        return "ong_khong_pipefail"   # chỉ `shell: bash` tường minh (`bash --noprofile --norc -eo pipefail {0}`) mới có pipefail chắc chắn
    return "ong_cau_truc_khong_do_duoc" if RE_CAU_TRUC_SHELL.search(run) else None   # quét thân THÔ, kể cả nháy/chú thích


def chan_k7(wf, k, i, env_buoc, env_job):
    """Lý do chặn (chuỗi) hoặc None — thay `cp.chan_buoc`: cho `env:` mức bước trong tập của luật; giữ mọi điều kiện khác."""
    jb, s = wf["jobs"][k], wf["jobs"][k]["steps"][i]
    for ten, d in (("workflow", wf), ("job", jb)):
        if "defaults" in d or cp._env_chan(d) or not set(d.get("env") or {}) <= set(env_job):
            return f"env_hoac_defaults_{ten}"
    if set(s) - (cp.KHOA_BUOC | {"env"}):
        return "khoa_buoc_la"
    if "env" in s and (type(s["env"]) is not dict or not set(s["env"]) <= set(env_buoc)):
        return "env_buoc_ngoai_tap"
    if s.get("shell", "bash") not in ("bash", "pwsh", "sh"):
        return "shell_la"
    if any(re.search("GITHUB_(ENV|PATH)", str(t.get("run", ""))) for t in jb["steps"][:i]):
        return "buoc_truoc_ghi_github_env"
    if s.get("continue-on-error", False) is not False:
        return "continue_on_error"
    return None


def _dat_dau_hieu(dau_hieu, buoc):
    """Lý do thiếu dấu hiệu (list) cho một bước; `buoc` = [(loai, nd)] đã lọc đúng nhãn."""
    loi, thuong = [], [nd for lo, nd in buoc if lo == ""]
    for loai, r in dau_hieu:
        if loai == "DONG" and not any((m := re.fullmatch(r, x)) and all(int(g) > 0 for g in m.groups()) for x in thuong):   # 4493205470: đếm > 0
            loi.append(f"thieu_dau_hieu:{r[:40]}")
        elif loai == "CUOI" and not ((cu := [nd for lo, nd in buoc if lo == "CUOI"]) and re.fullmatch(r, cu[-1])):
            loi.append("cuoi_khong_dat")
        elif loai == "KHONG" and [nd for lo, nd in buoc if lo == "KHONG"] != ["0"]:
            loi.append("khong_khac_0")
        elif loai == "JSON_OK":
            js = [nd for lo, nd in buoc if lo == "JSON"]
            try:
                ok = bool(js) and type(v := json.loads(js[0])) is dict and v.get("ok") is True
            except ValueError:
                ok = False
            loi += [] if ok else ["json_khong_ok"]
    return loi


def _m(d, k):   # F06: mapping lồng sai kiểu ⇒ rỗng, không ném
    v = d.get(k) if type(d) is dict else None
    return v if type(v) is dict else {}


def _l(d, k):
    v = d.get(k) if type(d) is dict else None
    return [x for x in v if type(x) is dict] if type(v) is list else []


def _sai_kieu(pv):   # F06 lượt 2: kiểm cấu trúc MỘT lần; phần tử hỏng ⇒ từ chối, không lọc âm thầm
    moc = pv.get("moc")
    if type(moc) is not dict or type(moc.get("run")) is not dict or type(moc.get("gate_output")) is not dict or type(
            moc["run"].get("loi_khai_rest_path")) is not str:
        return True
    ds, co, log = moc["gate_output"].get("jobs"), moc.get("checkout"), pv.get("log_day_du")
    if type(ds) is not list or type(co) is not list or type(log) is not dict:
        return True
    for j in ds:
        if not (type(j) is dict and type(j.get("job_id")) is int and type(j.get("name")) is str and type(j.get("conclusion")) is str
                and type(j.get("labels")) is list and all(type(x) is str for x in j["labels"])
                and (j.get("buoc") == "not_measured" or type(j.get("buoc")) is list and all(
                    type(b) is dict and type(b.get("name")) is str and type(b.get("conclusion")) is str for b in j["buoc"]))):
            return True
    return not (all(type(c) is dict and type(c.get("job_id")) is int and (c.get("sha") is None or _h40(c.get("sha"))) for c in co)
                and all(type(v) is dict and type(v.get("sha256")) is str for v in log.values()))


def kiem(text, provenance, goc):
    """(trang_thai, [lý do]) — OFFLINE. `failed` thắng `not_measured`. `goc` = kho git chứa SHA checkout."""
    if loi := kiem_so_luat():
        return "not_measured", ["so_luat_hong", *loi]
    try:
        dau, jobs, moc = phan_tich(text)
    except (ValueError, TypeError, AttributeError):
        return "not_measured", ["dinh_dang"]
    nm, fl = [], []
    pv = provenance if type(provenance) is dict else {}
    if _sai_kieu(pv):
        return "not_measured", ["provenance_sai_kieu"]
    run = _m(_m(pv, "moc"), "run")
    if (int(dau[1]), int(dau[2]), dau[3]) != (run.get("run_id"), pv.get("attempt_yeu_cau"), run.get("head_sha")):
        nm.append("neo_run")
    if run.get("trang_thai") != "passed" or run.get("repo") != "ducthangho/tra-luat":
        nm.append("run_chua_passed_hoac_sai_kho")
    if run.get("event") not in ("push", "workflow_dispatch"):
        nm.append("su_kien_ngoai_pham_vi")
    luat = LUAT_PHIEN_BAN.get(dau[4])
    a, z = MIEN_HIEU_LUC.get(dau[4], (None, None))
    if luat is None or type(run.get("run_id")) is not int or not (a <= run["run_id"] and (z is None or run["run_id"] <= z)):
        return "not_measured", nm + ["luat_ngoai_so_hoac_mien"]
    ds = _l(_m(_m(pv, "moc"), "gate_output"), "jobs")
    if len({j.get("job_id") for j in ds}) != len(ds):   # F01: dict sẽ nuốt bản ghi trùng id (có thể là bản `failure`)
        return "not_measured", nm + ["job_id_trung_provenance"]
    tp = {j.get("job_id"): j for j in ds if j.get("conclusion") != "skipped"}
    log = _m(pv, "log_day_du")
    if any(j.get("runner_id") == 0 or j.get("trang_thai") == "not_run" for j in tp.values()):
        return "not_measured", nm + ["job_chua_chay"]
    ids = [j["id"] for j in jobs]
    if len(ids) != len(set(ids)) or set(ids) != set(tp) or set(tp) != set(log):
        return "not_measured", nm + ["tap_job"]
    jj = [i for i, j in tp.items() if type(j.get("labels")) is list and set(j["labels"]) & set(luat["OS_BAT_BUOC"]) and j.get("name") not in luat["KHONG_PHAI_GATE"]]
    if not jj:
        return "not_measured", nm + ["tap_job_rong"]
    co = [c for c in _l(_m(pv, "moc"), "checkout") if c.get("trang_thai") == "passed"]
    sha = {c.get("sha") for c in co}
    wf = None
    if len(sha) != 1:
        nm.append("khong_xac_dinh_sha_checkout")
    else:
        r = subprocess.run(["git", "-C", str(goc), "show", "--end-of-options", f"{next(iter(sha))}:{run['loi_khai_rest_path']}"],
                           capture_output=True)   # F10: SHA đã buộc 40 hex ở `_sai_kieu`; `--end-of-options` chặn đọc thành tuỳ chọn
        wf = cp.doc_wf(r.stdout.decode("utf-8", "replace")) if r.returncode == 0 else None
        wf = wf if wf and all(type(x) is dict and type(x.get("steps", [])) is list and all(type(y) is dict for y in x.get("steps", []))
                              for x in wf["jobs"].values()) else None   # F06: workflow hỏng cấu trúc ⇒ như không đọc được
        nm += [] if wf else ["khong_doc_duoc_workflow"]
    for j in jobs:
        p = tp[j["id"]]
        if (j["name"], j["labels"], j["conclusion"]) != (p.get("name"), p.get("labels"), p.get("conclusion")):
            nm.append(f"danh_tinh:{j['id']}")
        if j["log"] != _m(log, j["id"]).get("sha256"):
            nm.append(f"bam_log:{j['id']}")
        if j["id"] not in jj:
            mui = "not_measured" if p.get("name") in luat["KHONG_PHAI_GATE"] else "ngoai_pham_vi_os"
            if j["steps"] or j["mui"] != mui:
                nm.append(f"dinh_dang:{j['id']}")
            continue
        if p.get("conclusion") != "success":
            fl.append(f"job_khong_success:{j['id']}")
        if j["mui"] != "passed":
            nm.append(f"mui_ten:{j['id']}")
        if not any(c.get("job_id") == j["id"] and c.get("sha") in sha for c in co):
            nm.append(f"checkout_job_chua_do:{j['id']}")
        m = _muc(luat, str(p.get("name")))
        if len(m) != 1:
            nm.append(f"khong_co_luat:{j['id']}")
            continue
        nm_, fl_ = _kiem_job(j, p, m[0], wf, luat)
        nm += nm_
        fl += fl_
    ten_j = [tp[i].get("name") for i in jj]   # K3 đủ job: ĐỘC LẬP với mọi lý do khác (G07)
    nm += [f"thieu_job_bat_buoc:{t}" for t in luat["JOB_BAT_BUOC"] if ten_j.count(t) == 0]
    nm += [f"job_trung_ten:{t}" for t in dict.fromkeys(ten_j) if ten_j.count(t) > 1]
    nm += [f"job_ngoai_luat:{t}" for t in dict.fromkeys(ten_j) if t not in luat["JOB_BAT_BUOC"]]
    if (moc[1], int(moc[2]), int(moc[3])) != ("passed", len(jj), len(jj)):
        nm.append("moc_tong")
    return ("failed", fl + nm) if fl else ("not_measured", nm) if nm else ("passed", [])


def _kiem_job(j, p, muc, wf, luat):
    nm, fl = [], []
    k = cp.ghep_job(p.get("name"), wf) if wf else None
    if wf and k is None:
        nm.append(f"job_yaml:{j['id']}")
    rest = [b for b in p.get("buoc") or [] if type(b) is dict] if type(p.get("buoc")) is list else []
    ten_luat = {t: b for b in muc["buoc"] for t in b["ten"]}
    for s in j["steps"]:
        if s["name"] not in ten_luat:
            nm.append(f"step_ngoai_luat:{j['id']}")
        rb = [b for b in rest if b.get("name") == s["name"]]
        if len(rb) != 1:
            nm.append(f"step_khong_trong_buoc:{s['name'][:30]}")
        elif rb[0].get("conclusion") != "success":
            fl.append(f"buoc_khong_success:{s['name'][:30]}")
        elif s["conclusion"] != "success":
            nm.append(f"step_conclusion:{s['name'][:30]}")
        if k is not None:
            sy = [i for i, y in enumerate(wf["jobs"][k].get("steps") or []) if type(y) is dict and cp.ten_du_kien(y) == s["name"]]
            if len(sy) != 1:
                nm.append(f"buoc_yaml:{s['name'][:30]}")
                continue
            y, lb = wf["jobs"][k]["steps"][sy[0]], ten_luat.get(s["name"])
            if ly := chan_k7(wf, k, sy[0], lb["env"] if lb else [], luat["ENV_JOB_CHO_PHEP"]):
                nm.append(f"che_do_khong_xac_dinh:{ly}:{s['name'][:30]}")
            elif ly := che_do_shell(str(y.get("run", "")), y.get("shell")):
                nm.append(f"{ly}:{s['name'][:30]}")
    for b in muc["buoc"]:
        st = [s for s in j["steps"] if s["name"] in b["ten"]]
        if len(st) != 1:
            nm.append(f"thieu_hoac_lap_buoc:{b['ten'][0][:30]}")
            continue
        if any(n != b["ten"][0] for n, _, _ in st[0]["buoc"]):
            nm.append(f"nhan_buoc:{b['ten'][0][:30]}")
        nm += _dat_dau_hieu(b["dau_hieu"], [(lo, nd) for _, lo, nd in st[0]["buoc"]])
    return nm, fl


# ---------- lời khai, neo, phạm vi land ----------
TOKEN = ("passed", "measured", "not_measured", "failed", "skipped", "not_run", "owner_waived")
DUONG = ("passed", "measured")
PHI_LOI_KHAI = {"gateoutputnguon", "gateoutputnguonvagioihan", "mocgateoutputrcdisposition"}
RE_TOKEN = re.compile(r"\s*([a-z_]+)(?=$|[\s—\-:(,.;])")
RE_TEP = re.compile(r"[A-Za-z0-9_./-]*gate-output2-[0-9]+-a[0-9]+\.txt")
RE_URL = re.compile(r"https://github\.com/ducthangho/tra-luat/\S*?#issuecomment-([0-9]+)")
RE_SHA = re.compile(r"(?<![0-9a-f])[0-9a-f]{40}(?![0-9a-f])")
RE_MIEN = re.compile(r"mien_gate_output: ([0-9a-f]{40}) os=([a-z0-9,.-]+) ly_do=(\S.*?) han=(\d{4}-\d{2}-\d{2})")
MOC_10_2_2 = {"run", "checkout", "workflow_definition", "gate_output"}
GIOI_HAN = ("điều kiện cần cho §10.2.3; giới hạn Q10: actor không tách được chủ kho với agent (cùng login), "
            "`han` chỉ kiểm dạng, không so đồng hồ")


def _chuan(k):
    return "".join(c for c in str(k).casefold() if c.isalnum())


def la_loi_khai(k):
    return "gateoutput" in _chuan(k) and _chuan(k) not in PHI_LOI_KHAI


def _h40(v):
    return v if type(v) is str and re.fullmatch("[0-9a-f]{40}", v) else None


def tap_head_land(cay_yaml):
    d = cay_yaml if type(cay_yaml) is dict else {}
    prs = d.get("prs") if type(d.get("prs")) is list else []
    return {h for h in [_h40(d.get("merge_commit")), *(_h40(p.get("merge_commit")) for p in prs if type(p) is dict)] if h}


def la_run_land(provenance):
    r = _m(_m(provenance, "moc"), "run")
    return r.get("loi_khai_rest_path") == ".github/workflows/ci.yml" and r.get("event") == "push"


def _pv_neo(prov, neo):   # MỘT luật neo cho mọi đường đọc bằng chứng dương (P2 connector 4491937587, F11 lượt 6)
    return [x for x in prov if (_m(_m(x, "moc"), "run").get("run_id"), x.get("attempt_yeu_cau"), _m(_m(x, "moc"), "run").get("head_sha")) == neo]


def _neo(m, cha):
    if type(m.get("run_id")) is int:
        h = [x for x in (_h40(m.get(k)) for k in ("sha", "head_sha", "merge_commit")) if x]
        return (m["run_id"], m["run_attempt"], h[0]) if type(m.get("run_attempt")) is int and len(h) == 1 else None
    if MOC_10_2_2 <= set(m) and type(cha) is dict and type(ci := cha.get("ci_master")) is dict:
        if type(ci.get("run_id")) is int and type(ci.get("run_attempt")) is int and _h40(cha.get("merge_commit")):
            return ci["run_id"], ci["run_attempt"], cha["merge_commit"]
    return None


def _duyet(v, duong="$", cha=None):
    if type(v) is dict:
        for k, x in v.items():
            if la_loi_khai(k):
                yield f"{duong}.{k}", x, _neo(v, cha)
            yield from _duyet(x, f"{duong}.{k}", v)
    elif type(v) is list:
        for i, x in enumerate(v):
            yield from _duyet(x, f"{duong}[{i}]", cha)


def kiem_waiver(chuoi, head, readback, url_hop_le):
    """(hợp lệ, [lý do]). Ba điều kiện chuỗi + bốn điều kiện readback (gồm ĐÚNG MỘT dòng `mien_gate_output` cho head)."""
    loi = []
    url = [u for u in RE_URL.finditer(chuoi)]
    if len(url) != 1 or url_hop_le is None or not url_hop_le(url[0][0]):
        loi.append("url")
    if head not in RE_SHA.findall(chuoi):
        loi.append("sha_khac_head")
    con = RE_SHA.sub("", RE_URL.sub("", re.sub(r"\bowner_waived\b", "", chuoi, flags=re.I)))
    if len(con.strip(" \t—-:;,.()")) < 10:
        loi.append("thieu_ly_do")
    rb = readback if type(readback) is dict else {}
    if not url or rb.get("html_url") != url[0][0]:
        loi.append("readback_html_url")
    if _m(rb, "user").get("login") != "ducthangho" or rb.get("author_association") != "OWNER":
        loi.append("readback_khong_phai_chu_kho")
    dong = [m for d in str(rb.get("body") or "").splitlines() if (m := RE_MIEN.fullmatch(d.strip())) and m[1] == head]
    if len(dong) != 1:
        loi.append("khong_dung_mot_dong_mien_gate_output")
    elif not set(LUAT_v1["OS_BAT_BUOC"]) <= set(dong[0][2].split(",")):
        loi.append("os_thieu")
    else:
        try:
            datetime.date.fromisoformat(dong[0][4])
        except ValueError:
            loi.append("han_sai_lich")
    return not loi, loi


def _an_toan(thu, ten):   # CHỈ tương đối `<hồ sơ>-provenance/`: cấm tuyệt đối, cấm `..`, cấm symlink ở mọi thành phần KỂ CẢ thư mục ấy (F02)
    p, n = thu / ten, len(Path(ten).parts)
    ok = not ten.startswith("/") and ".." not in Path(ten).parts and p.is_file() and not any(q.is_symlink() for q in [p, *p.parents][:n + 1])
    return p if ok else None


def kiem_ho_so_gate_output(tep_ho_so, cay_yaml, goc, url_hop_le):
    """Mỗi lời khai: {duong_dan, token, neo, la_land, hop_le, ly_do}. L8 và L-7 tự rút kết luận."""
    tep = Path(tep_ho_so)
    thu = tep.with_name(tep.name.removesuffix(".yaml").removesuffix("-land-evidence") + "-provenance")
    prov = []
    for f in sorted(thu.rglob("*.yaml")) if thu.is_dir() else []:
        try:
            d = yaml.safe_load(f.read_text(encoding="utf-8"))
        except Exception:   # tệp YAML không đọc được không phải provenance
            continue
        if type(d) is dict and d.get("schema") == "ci_provenance/1":
            prov.append(d)
    H, ra = tap_head_land(cay_yaml), []
    for duong, gt, neo in _duyet(cay_yaml):
        tok = m[1] if type(gt) is str and (m := RE_TOKEN.match(gt.casefold())) and m[1] in TOKEN else None
        pv = [p for p in prov if neo and _m(_m(p, "moc"), "run").get("run_id") == neo[0]]
        land = bool(neo) and neo[2] in H and (not pv or any(la_run_land(p) or not all(   # F09: thiếu dữ liệu ⇒ land (fail-closed)
            type(v := _m(_m(p, "moc"), "run").get(k)) is str and v.strip() for k in ("loi_khai_rest_path", "event")) for p in pv))
        loi = []
        if tok is None:
            loi.append("dinh_dang_loi_khai")
        elif tok in DUONG or tok == "owner_waived":
            if neo is None:
                loi.append("thieu_neo")
            elif tok == "owner_waived":
                id_ = [m[1] for m in RE_URL.finditer(gt)]
                rb = sorted(thu.rglob(f"readback-*issuecomment-{id_[0]}.json")) if id_ and thu.is_dir() else []
                try:
                    rbj = json.loads(rb[0].read_text(encoding="utf-8")) if len(rb) == 1 else None
                except ValueError:
                    rbj = None
                ok, ly = kiem_waiver(gt, neo[2], rbj, url_hop_le)
                loi += [] if ok else ["waiver_khong_co_can_cu", *ly]
            elif not prov:
                loi.append("khong_co_provenance")
            else:
                loi += _kiem_duong(gt, neo, thu, prov, goc)
                if land and not (len(n1 := _pv_neo(prov, neo)) == 1 and la_run_land(n1[0])):   # F11: land DƯƠNG chỉ do provenance ĐÚNG neo
                    loi.append("bang_chung_land_khong_dung_neo")
        elif land:
            loi.append("loi_khai_land_khong_hop_le")
        ra.append({"duong_dan": duong, "token": tok, "neo": neo, "la_land": land, "hop_le": not loi, "ly_do": loi})
    return ra


def _kiem_duong(gt, neo, thu, prov, goc):
    ten = RE_TEP.findall(gt)
    if not ten:
        return ["chi_ket_luan_check_run" if re.search(r"kiem-gate|check-runs", gt) else "khong_trich_tep_gate_output"]
    for t in ten:
        if (p := _an_toan(thu, t)) is None:
            continue
        van = p.read_text(encoding="utf-8")
        if not (d := RE_DAU.fullmatch(van.split("\n", 1)[0])) or (int(d[1]), int(d[2]), d[3]) != neo:
            continue
        if p.name != f"gate-output2-{d[1]}-a{d[2]}.txt":   # F02: tên tệp BẮT BUỘC theo run/attempt của header
            continue
        pv = _pv_neo(prov, (int(d[1]), int(d[2]), d[3]))   # P2 connector 4491937587: neo đủ (run, attempt, head)
        if len(pv) == 1 and kiem(van, pv[0], goc)[0] == "passed":
            return []
    return ["tep_gate_output_khong_dat"]


def main(argv=None):
    for s in (sys.stdout, sys.stderr):
        if hasattr(s, "reconfigure"):
            s.reconfigure(encoding="utf-8", errors="backslashreplace")
    a = list(sys.argv[1:] if argv is None else argv)
    try:
        if len(a) == 6 and a[0] == "kiem" and a[1] == "--provenance" and a[3] == "--goc":
            tt, ly = kiem(Path(a[5]).read_text(encoding="utf-8"), yaml.safe_load(Path(a[2]).read_text(encoding="utf-8")), a[4])
            print(f"GATE_OUTPUT: {tt}" + (f" — {'; '.join(ly)}" if ly else " — điều kiện cần cho §10.2.2 Gate output (OS: ubuntu-latest)"))
            return {"passed": 0, "failed": 1}.get(tt, 2)
        if len(a) == 4 and a[0] == "kiem-ho-so" and a[1] == "--root":
            tep = Path(a[3])
            # F03 lượt 2: CLI là NGƯỜI GỌI ⇒ nạp lười `_url_hop_le` của cổng L-7 ngay tại đây; thư viện vẫn không import nó (A22)
            s = importlib.util.spec_from_file_location("kiem_ho_so_land_cho_cli", Path(__file__).with_name("kiem_ho_so_land.py"))
            khl = importlib.util.module_from_spec(s)
            s.loader.exec_module(khl)
            kq = kiem_ho_so_gate_output(tep, yaml.safe_load(tep.read_text(encoding="utf-8")), a[2], khl._url_hop_le)
            for x in kq:
                print(f"{'ĐẠT' if x['hop_le'] else 'ĐỎ'} {x['duong_dan']} token={x['token']} land={x['la_land']} {' '.join(x['ly_do'])}")
            print(f"TỔNG: {'ĐẠT' if all(x['hop_le'] for x in kq) else 'ĐỎ'} ({len(kq)} lời khai; {GIOI_HAN})")
            return 0 if all(x["hop_le"] for x in kq) else 1
    except (OSError, ValueError, yaml.YAMLError) as e:
        print(f"KHÔNG ĐO ĐƯỢC: {type(e).__name__}: {e}", file=sys.stderr)
        return 2
    print("dung: gate_output_doi_chieu.py kiem --provenance P --goc G TEP | kiem-ho-so --root G TEP_HO_SO", file=sys.stderr)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
