"""Danh gia moc Gate output §10.2.2 cho MOT run: moi job (tru job bi skipped) phai co DONG KET QUA DUONG khop luat cua loai job.

Thieu dau hieu duong => job `not_measured` => moc `not_measured` (khong bao gio suy pass tu conclusion + ##[error]=0).
Cach goi: python3 danh_gia_gate.py <run_id> <thu_muc_ra> [--am TEN_JOB_CON]
--am: phan chung — xoa dong dau hieu duong khoi log cua job co ten bat dau bang TEN_JOB_CON roi danh gia lai; phai ra not_measured.
"""
import hashlib, json, os, re, sys, urllib.request

TOK = os.environ["GITHUB_PAT"]
API = "https://api.github.com/repos/ducthangho/tra-luat/"


def raw(u):
    req = urllib.request.Request(API + u, headers={"Authorization": "Bearer " + TOK, "Accept": "application/vnd.github+json"})
    return urllib.request.urlopen(req, timeout=120).read()


# (tien to ten job, regex dau hieu duong BAT BUOC — tat ca phai co mat)
LUAT = [
    ("chuan-bi", [r"^che_do=(day_du|duong_nhanh)$"]),
    ("gate-cong-cu-gop", [r"^SỐ LIỆU GOM: ca=(\d+) · đột biến=(\d+) · lỗi đột biến=0$"]),
    ("gate-cong-cu (", [r"^cong_cu_test: (\d+)/\1 đạt;", r"^MẢNH \d+/\d+: (\d+)/\1 đột biến bán kính 1"]),
    ("gate-nhanh-manh", [r"^targeted_mutant_gate MANH \d+/\d+: rc=0 · passed (\d+)/\1$"]),
    ("gate-nhanh-gop", [r"^targeted_mutant_gate: DAT"]),
    ("gate-packet-loop", [r"^TỔNG: ĐẠT$"]),
    ("gate-ops", [r"^TỔNG: ĐẠT$"]),
    ("gate-registry", [r"^TONG: DAT$|^TỔNG: ĐẠT$"]),
    ("gate (", [r"^TỔNG: ĐẠT$"]),
    ("launcher (", [r"^(\d+)/\1 ca DA CHAY QUA", r"^DOT BIEN: (\d+)/\1 dat"]),
]


def dong(b):
    out = []
    for l in b.decode("utf-8", "replace").splitlines():
        l = re.sub(r"^\d{4}-\d\d-\d\dT[\d:.]+Z ", "", l)
        if "\x1b[36;1m" in l:          # dong lenh duoc in lai (echo), khong phai ket qua
            continue
        out.append(l.rstrip("\r"))
    return out


def danh_gia(ten, lines):
    for tien_to, pats in LUAT:
        if ten.startswith(tien_to):
            khop = []
            for p in pats:
                m = next((l for l in lines if re.search(p, l)), None)
                if m is None:
                    return "not_measured", f"thieu dau hieu duong /{p}/"
                khop.append(m.strip())
            return "passed", " | ".join(k[:150] for k in khop)
    return "not_measured", "khong co luat cho loai job nay"


def main():
    run_id, ra = sys.argv[1], sys.argv[2]
    am = sys.argv[4] if len(sys.argv) > 4 and sys.argv[3] == "--am" else None
    run = json.loads(raw(f"actions/runs/{run_id}"))
    jobs = json.loads(raw(f"actions/runs/{run_id}/jobs?per_page=100"))["jobs"]
    kq, out = [], [f"# Danh gia Gate output run {run_id} attempt {run['run_attempt']} head {run['head_sha']} — luat dau hieu duong tung loai job"
                   f" (danh_gia_gate.py sha256 {hashlib.sha256(open(__file__, 'rb').read()).hexdigest()})", ""]
    for j in sorted(jobs, key=lambda j: j["name"]):
        if j["conclusion"] == "skipped":
            out.append(f"JOB {j['id']} {j['name']}: skipped (khong tinh)")
            continue
        b = raw(f"actions/jobs/{j['id']}/logs")
        lines = dong(b)
        if am and j["name"].startswith(am):
            pats = next(p for t, p in LUAT if j["name"].startswith(t))
            lines = [l for l in lines if not any(re.search(p, l) for p in pats)]
        tt, ct = danh_gia(j["name"], lines)
        if j["conclusion"] != "success":
            tt, ct = "failed", f"conclusion={j['conclusion']}"
        kq.append(tt)
        out.append(f"JOB {j['id']} {j['name']} [{','.join(j['labels'])}] conclusion={j['conclusion']} log_sha256={hashlib.sha256(b).hexdigest()} -> {tt}: {ct}")
    moc = "passed" if kq and all(x == "passed" for x in kq) else ("failed" if "failed" in kq else "not_measured")
    out += ["", f"MOC_GATE_OUTPUT: {moc} ({kq.count('passed')}/{len(kq)} job co dau hieu duong)"]
    if am:
        print("\n".join(out[-1:]))
        return 0 if moc != "passed" else 1
    open(ra, "w", encoding="utf-8").write("\n".join(out) + "\n")
    print(out[-1])
    return 0


if __name__ == "__main__":
    sys.exit(main())
