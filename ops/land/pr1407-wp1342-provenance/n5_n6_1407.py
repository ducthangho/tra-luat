"""Doc lai ket qua native Windows (Desktop + VM) cua ho so land PR #1407 va do N5/N6 (dac ta r4 §5).
Dung: python -I n5_n6_1407.py <desktop-out> <vm-out>
N5: tap ID BASE == tap ID BASE-trong-HEAD; tung ID: rc, KQ_JSON (bo duong dan tam), dong WP1342_NATIVE_V1 (bo observed/os/python) bang nhau.
N6: J0..J11 tren HEAD Desktop: rc 0, KQ_JSON null, WP1342_NATIVE_V1 passed 1 + observed khac rong, giay <= 90 (giay do o vong ngoai, tren cua so 90 s
    cua ca: chi doc duoc thoi luong tien trinh); J3/J9/J10 tren VM tuong tu."""
import json, pathlib, re, sys

D, V = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
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


def doc_ca(thu_muc, nhan, cid):
    t = (thu_muc / f"{nhan}-{cid}.txt").read_text(encoding="utf-8-sig")
    return t


base = jl(D / "BASE.jsonl"); head = {r["id"]: r for r in jl(D / "HEAD.jsonl")}
lech = []
for r in base:
    h = head.get(r["id"])
    if h is None:
        lech.append((r["id"], "thieu tren HEAD")); continue
    if r["rc"] != h["rc"]:
        lech.append((r["id"], "rc", r["rc"], h["rc"]))
    a, b = chuan(doc_ca(D, "BASE", r["id"])), chuan(doc_ca(D, "HEAD", r["id"]))
    if a != b:
        lech.append((r["id"], "noi dung", a, b))
print(f"N5: {len(base)} ID base; lech {len(lech)}")
for x in lech:
    print("  LECH", x)
print("N5 rc!=0 ca hai ve (BO QUA KHONG DO DUOC):", [r["id"] for r in base if r["rc"] != 0])


def kiem_j(thu_muc, nhan, rows, nhom):
    bad = []
    for k in nhom:
        cid = J[k]
        rs = [r for r in rows if r["id"] == cid]
        if not rs:
            bad.append((k, "khong chay")); continue
        for r in rs:
            t = doc_ca(thu_muc, nhan, cid) if (thu_muc / f"{nhan}-{cid}.txt").exists() else ""
            v = [json.loads(ln.split(" ", 1)[1]) for ln in t.splitlines() if ln.startswith("WP1342_NATIVE_V1 ")]
            ok = r["rc"] == 0 and r["giay"] <= 90 and v and v[-1].get("passed") == 1 and v[-1].get("observed") not in (None, "", "None")
            if not ok:
                bad.append((k, r))
        print(f"  {nhan} {k:4} {cid}: lan={len(rs)} rc={[r['rc'] for r in rs]} giay_max={max(r['giay'] for r in rs)} observed={v[-1].get('observed') if v else None!r}")
    return bad


hrows = jl(D / "HEAD.jsonl")
b1 = kiem_j(D, "HEAD", hrows, list(J))
vrows = jl(V / "VM.jsonl")
b2 = kiem_j(V, "VM", vrows, ["J3", "J9", "J10"])
for nhan, f in (("LAP-J3", "LAP-J3.jsonl"), ("LAP-J9", "LAP-J9.jsonl")):
    rs = jl(D / f)
    print(f"  {nhan}: {sum(r['rc'] == 0 for r in rs)}/{len(rs)} rc 0, giay_max {max(r['giay'] for r in rs)}")
print("N6 Desktop:", "DAT" if not b1 else f"DO {b1}")
print("N6 VM:", "DAT" if not b2 else f"DO {b2}")
sys.exit(1 if (lech or b1 or b2) else 0)
