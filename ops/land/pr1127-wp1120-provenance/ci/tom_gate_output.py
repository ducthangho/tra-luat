#!/usr/bin/env python3
"""Tom tat moc gate_output (§10.2.2) tu log REST tung job cua MOT run, va tu kiem tom tat ay.

Dung:
  tom_gate_output.py tom  --jobs jobs.json --logs <thu muc log> --tieu-de "<dong #>" > gate-output-<run>.txt
  tom_gate_output.py kiem gate-output-<run>.txt      # rc 0 = moi job gate co marker hoan tat duong

Vi sao co tep nay (Codex P1 tren PR #1235, comment 4482143157): ban dau tom bang mot regex rong,
17/37 job khong co dong marker nao, 8 manh gate-cong-cu chi co dong MO DAU manh, gate-cong-cu-gop
khong co gi — tuc lai lay conclusion + so ##[error] lam bang chung hoan tat. Ban nay:
  * moi marker la mot mau NEO CA DONG, va mau dang N/M doi N == M (backref), khong nhan dong mo dau;
  * moi job ghi cac lenh `Run` (buoc khong phai `uses: actions/...`) de co CAU LENH chu khong chi ket luan;
  * `kiem` DO: job nao (tru `chuan-bi`, khong phai gate: chi dung ma tran) thieu marker hoan tat ⇒ rc 1.
Ma thoat cua lenh: moi buoc `run` cua ci.yml chay duoi `bash -e -o pipefail` (Ubuntu) / pwsh (Windows),
nen job success ⇒ moi lenh rc 0; marker `rc=0` co mat o noi chuong trinh tu in.
"""
import json
import re
import sys
from pathlib import Path

TS = re.compile(r"^\d{4}-\d\d-\d\dT[\d:.]+Z ")
ANSI = re.compile(r"\x1b\[[0-9;]*m")
KHONG_PHAI_GATE = {"chuan-bi"}  # chi dung ma tran `os`; khong chay test nao

# Mau hoan tat: neo ca dong; (?P<a>\d+)/(?P=a) ép tử = mẫu.
MAU = [re.compile(p) for p in (
    r"TỔNG: ĐẠT",
    r"TỔNG: CA (?P<a>\d+)/(?P=a) đạt · .*",
    r"== [\w ]+ (?P<a>\d+)/(?P=a) ==",
    r"nền: (?P<a>\d+)/(?P=a) đạt(?: · BỎ QUA: \d+)?",
    r"ĐỘT BIẾN +: đã đo (?P<a>\d+)/(?P=a).*",
    r"DOT BIEN (?P<a>\d+)/(?P=a).*",
    r"targeted_mutant_gate MANH \d+/8: rc=0 · passed (?P<a>\d+)/(?P=a)",
    r"targeted_mutant_gate GOP 8/8 manh · head [0-9a-f]{40}",
    r"targeted_mutant_gate: DAT — KHONG phai full mutant audit; .*",
    r"MẢNH \d+/8: (?P<a>\d+)/(?P=a) đột biến bán kính 1 · ghi .*",
    r"GOM MẢNH 8/8",
    r"SỐ LIỆU GOM: ca=\d+ · đột biến=\d+ · lỗi đột biến=0",
    r"(?:\[[AB]\] )?lease_publish: (?P<a>\d+)/(?P=a) đạt; đã chạy=(?P=a), bỏ qua=0",
    r"don-nhanh: (?P<a>\d+)/(?P=a) dat",
    r"gate lifecycle tests: (?P<a>\d+)/(?P=a) ca QUA \(bo qua 0, hong 0\)",
)]


def _dong(p: Path):
    for d in p.read_bytes().decode("utf-8", "replace").splitlines():
        yield ANSI.sub("", TS.sub("", d)).rstrip()


def tom(jobs_json: Path, logs: Path, tieu_de: str) -> int:
    import hashlib
    jobs = json.loads(jobs_json.read_text(encoding="utf-8"))
    jobs = jobs.get("jobs", jobs)
    print(f"# {tieu_de}")
    for j in sorted(jobs, key=lambda x: x["name"]):
        p = logs / f"{j['id']}.log"
        b = p.read_bytes()
        loi = sum(1 for d in _dong(p) if d.startswith("##[error]"))
        print(f"JOB {j['id']} {j['name']} [{','.join(j.get('labels', []))}] conclusion={j['conclusion']} "
              f"bytes={len(b)} sha256={hashlib.sha256(b).hexdigest()} ##[error]={loi}")
        thay = []
        for d in _dong(p):
            if d.startswith("##[group]Run ") and not d.startswith("##[group]Run actions/"):
                print(f"    CMD {d[len('##[group]Run '):]}")
            elif any(m.fullmatch(d) for m in MAU) and d not in thay:
                thay.append(d)
                print(f"    OK  {d}")
    return 0


def kiem(tep: Path) -> int:
    job, thieu, n = None, [], 0
    def chot():
        if job and job[1] not in KHONG_PHAI_GATE and not job[2]:
            thieu.append(job[1])
    for d in tep.read_text(encoding="utf-8").splitlines():
        m = re.match(r"JOB (\d+) (.+?) \[.*\] conclusion=(\w+) .* ##\[error\]=(\d+)$", d)
        if m:
            chot()
            n += 1
            if m.group(3) != "success" or m.group(4) != "0":
                thieu.append(f"{m.group(2)} (conclusion={m.group(3)}, ##[error]={m.group(4)})")
            job = [m.group(1), re.sub(r" \(.*", "", m.group(2)), 0]
        elif d.startswith("    OK  ") and job:
            if any(mm.fullmatch(d[8:]) for mm in MAU):
                job[2] += 1
    chot()
    if n == 0 or thieu:
        print(f"KIEM: DO — {n} job, thieu marker hoan tat: {thieu or 'khong co job nao'}")
        return 1
    print(f"KIEM: DAT — {n} job, moi job gate co >=1 marker hoan tat neo ca dong ({sorted(KHONG_PHAI_GATE)} khong phai gate)")
    return 0


if __name__ == "__main__":
    a = sys.argv[1:]
    if a[:1] == ["kiem"] and len(a) == 2:
        sys.exit(kiem(Path(a[1])))
    if a[:1] == ["tom"] and len(a) == 7:
        o = dict(zip(a[1::2], a[2::2]))
        sys.exit(tom(Path(o["--jobs"]), Path(o["--logs"]), o["--tieu-de"]))
    sys.exit(__doc__)
