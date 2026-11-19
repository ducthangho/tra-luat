"""Doc lai lan do native Windows tren CAY MERGE a2c7d75 (Desktop, wp1342r4c-out) va doi chieu voi lan tren HEAD 46d3907 (wp1342r4b-out).
Dung: python -I n6_merge_1407.py <wp1342r4b-out (HEAD)> <wp1342r4c-out (MERGE)>
(a) tap ID MERGE == tap ID HEAD; tung ID: rc, KQ_JSON (bo duong dan tam), WP1342_NATIVE_V1 (bo observed/os/python) bang nhau.
(b) N6 tren MERGE: J0..J11 rc 0, KQ_JSON null, passed 1, observed khac rong, thoi luong tien trinh <= 90 s; LAP-J3/LAP-J9 moi lan nhu vay.
(c) N5 tren MERGE: 41 ID base (cung tap voi BASE.jsonl cua lan HEAD) rc/noi dung bang BASE."""
import json, pathlib, re, sys

H, M = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
J = {"J0": "wp1342_native_job_abi", "J1": "wp1342_native_job_thuan", "J2": "wp1342_native_job_han",
     "J3": "wp1342_native_job_mo_coi", "J6": "wp1342_native_job_treo_truoc_gan", "J7": "wp1342_native_job_khong_ke_thua",
     "J8": "wp1342_native_job_loi_truoc_gan", "J9": "wp1342_native_job_loi_sau_gan", "J10": "wp1342_native_job_cha_chet_sau_gan",
     "J10b": "wp1342_native_job_cha_chet_truoc_gan", "J11": "wp1342_native_job_query_loi"}


def jl(p):
    return [json.loads(x) for x in p.read_text(encoding="utf-8-sig").splitlines() if x.strip()]


def chuan(t):
    out = []
    for ln in t.splitlines():
        if ln.startswith("KQ_JSON "):
            out.append(re.sub(r"tmp[A-Za-z0-9_]{8}\\\\\\\\wp1342_n-[0-9a-f]+", "<TAM>", ln))
        elif ln.startswith("WP1342_NATIVE_V1 "):
            d = json.loads(ln.split(" ", 1)[1])
            for k in ("observed", "os", "python"):
                d.pop(k, None)
            out.append("WP1342_NATIVE_V1 " + json.dumps(d, sort_keys=True))
    return out


def doc(d, nhan, cid):
    return (d / f"{nhan}-{cid}.txt").read_text(encoding="utf-8-sig")


def v1(t):
    v = [json.loads(ln.split(" ", 1)[1]) for ln in t.splitlines() if ln.startswith("WP1342_NATIVE_V1 ")]
    return v[-1] if v else {}


hd = {r["id"]: r for r in jl(H / "HEAD.jsonl")}; md = {r["id"]: r for r in jl(M / "MERGE.jsonl")}
lech = []
if set(hd) != set(md):
    lech.append(("tap ID", sorted(set(hd) ^ set(md))))
for cid in sorted(set(hd) & set(md)):
    if hd[cid]["rc"] != md[cid]["rc"] or chuan(doc(H, "HEAD", cid)) != chuan(doc(M, "MERGE", cid)):
        lech.append((cid, hd[cid]["rc"], md[cid]["rc"]))
print(f"(a) MERGE {len(md)} ID vs HEAD {len(hd)} ID; lech {len(lech)}", lech)
print("    rc != 0 tren MERGE:", sorted(c for c, r in md.items() if r["rc"] != 0))

base = jl(H / "BASE.jsonl"); l5 = []
for r in base:
    m = md.get(r["id"])
    if m is None or m["rc"] != r["rc"] or chuan(doc(H, "BASE", r["id"])) != chuan(doc(M, "MERGE", r["id"])):
        l5.append(r["id"])
print(f"(c) N5 tren MERGE: {len(base)} ID base; lech so BASE e2c3b82: {len(l5)}", l5)

bad = []
for k, cid in J.items():
    r = md.get(cid); v = v1(doc(M, "MERGE", cid)) if r else {}
    ok = bool(r) and r["rc"] == 0 and r["giay"] <= 90 and v.get("passed") == 1 and v.get("observed") not in (None, "", "None")
    bad += [] if ok else [k]
    print(f"(b) MERGE {k:4} {cid}: rc={r and r['rc']} giay={r and r['giay']} observed={v.get('observed')!r}")
for nhan in ("LAP-J3", "LAP-J9"):
    rs = jl(M / f"{nhan}.jsonl"); v = v1(doc(M, nhan, rs[0]["id"]))
    ok = all(r["rc"] == 0 and r["giay"] <= 90 for r in rs) and v.get("passed") == 1
    bad += [] if ok else [nhan]
    print(f"(b) {nhan}: {sum(r['rc'] == 0 for r in rs)}/{len(rs)} rc 0, giay_max {max(r['giay'] for r in rs)}, lan cuoi observed={v.get('observed')!r}")
print("KET QUA:", "DAT" if not (lech or l5 or bad) else f"DO lech={lech} n5={l5} n6={bad}")
sys.exit(1 if (lech or l5 or bad) else 0)
