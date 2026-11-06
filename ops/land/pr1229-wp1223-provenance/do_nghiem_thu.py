"""Do lai A1–A6 cua dac ta ops/specs/cloud-setup-p3c-contract-r1.md §4 tren blob merge 50baf89 (va base c5a1c3d de so),
phien ghi so land session_015GtxrZk7fu1wjDZjWqyg2R — tra loi finding P1 r4485646618 tren PR #1251 (luot offline 4 chi review delta).

Moi tieu chi = mot ham vi tu tren noi dung tep; VE DUONG chay tren blob merge (phai True), VE AM chay tren ban da dot bien theo
cot "dot bien lam DO" cua dac ta (phai False). Dot bien la sua CHUOI trong bo nho, khong ghi tep.
A1 con chay that `scripts/contract_check.py --audit` trong mot ban git archive cua merge (truyen qua --cay).
A5 (tl selftest) KHONG chay o day: xem gate output cua run push master (danh-gia-gate-output-42073104862.txt).
Cach goi: python3 do_nghiem_thu.py --kho <goc kho> --cay <thu muc git archive 50baf89>
"""
import argparse, re, subprocess, sys

M, B = "50baf894216504d4bb975690ceb9dee4835a2ad7", "c5a1c3d1230b347333d4ca10f7dc514b817f7a9d"
ap = argparse.ArgumentParser(); ap.add_argument("--kho", required=True); ap.add_argument("--cay", required=True); a = ap.parse_args()


def blob(rev, path):
    return subprocess.run(["git", "-C", a.kho, "show", f"{rev}:{path}"], check=True, capture_output=True).stdout.decode("utf-8")


ket = []


def ghi(ten, duong, am):
    """duong: bool tren blob merge; am: list (mo_ta, bool) tren ban dot bien — phai False."""
    ok = duong and all(v is False for _, v in am)
    ket.append(ok)
    print(f"{ten}: {'DAT' if ok else 'DO'} — duong={duong}" + "".join(f" | am[{m}]={v}" for m, v in am))


api_m, api_b = blob(M, "references/API_CONTRACT.md"), blob(B, "references/API_CONTRACT.md")

# A1
def a1(t):
    dau = t.encode("utf-8")[:400].decode("utf-8", "ignore")
    return "`2.21.2q`" in dau and "(LIVE): `2.21.2p`" not in dau
r = subprocess.run([sys.executable, "scripts/contract_check.py", "--audit"], cwd=a.cay, capture_output=True, text=True)
print(f"# contract_check.py --audit (cay {M[:7]}): rc={r.returncode}; dong co 2.21.2q: "
      + repr([x for x in (r.stdout + r.stderr).splitlines() if "2.21.2q" in x][:3]))
d3 = api_m.splitlines()[2]
ghi("A1", a1(api_m) and r.returncode == 0 and "2.21.2q" in r.stdout + r.stderr,
    [("dong3 (LIVE) ve 2p", a1(api_m.replace(d3, d3.replace("(LIVE): `2.21.2q`", "(LIVE): `2.21.2p`"), 1)))])

# A2 — sau cum lich su, dem tung cum, bang base
CUM = ["**2.21.2p ATOMIC registry RMW**", "v2.21.2p tự khai `expect_shrink`", "**v2.21.2p KI-27** CHỈ ĐỌC",
       "**v2.21.2p KI-27**: thay TOÀN BỘ registry", "v2.21.2p (r198/ADR-0014)", "feature-detect ≥2.21.2p",
       "`regen2` (v2.21.2p: nhận thêm"]
def a2(t):
    return all(t.count(c) == api_b.count(c) and api_b.count(c) >= 1 for c in CUM) and not any(c.replace("2p", "2q") in t for c in CUM)
print("# dem cum (base/merge): " + "; ".join(f"{c!r} {api_b.count(c)}/{api_m.count(c)}" for c in CUM))
ghi("A2", a2(api_m), [("bump 2p->2q khong tra tay", a2(api_m.replace("2.21.2p", "2.21.2q"))),
                      ("sot mot cum (cum 3)", a2(api_m.replace(CUM[2], CUM[2].replace("2p", "2q"), 1)))])

# A3 — dong agent_creds_put + phep do S3
gs = blob(M, "references/Code.2.21.2q.gs")
TEN = set(re.findall(r"case '([^']+)'", gs))
MA = ["AGENT_CREDS_NOT_CONFIGURED", "AGENT_CREDS_FILEID_MISMATCH", "EXPECT_MD5_REQUIRED", "BLOB_SIZE", "LOCK_BUSY", "CAS_CONFLICT"]
def thieu(t):
    return {n for n in TEN if f"`{n}`" not in t}
def a3(t):
    d = [x for x in t.splitlines() if x.startswith("| `agent_creds_put` |")]
    return (len(d) == 1 and "POST" in d[0] and all(p in d[0] for p in ("fileId", "expect_md5", "b64"))
            and all(d[0].count(m) >= 1 for m in MA) and thieu(t) == {"configView", "regenRegistry"})
dong = [x for x in api_m.splitlines() if x.startswith("| `agent_creds_put` |")]
print(f"# so ten case trong Code.2.21.2q.gs: {len(TEN)}; thieu(base)={sorted(thieu(api_b))}; thieu(merge)={sorted(thieu(api_m))}; so dong agent_creds_put={len(dong)}")
ghi("A3", a3(api_m), [("xoa dong", a3("\n".join(x for x in api_m.splitlines() if not x.startswith("| `agent_creds_put` |")))),
                      ("bo CAS_CONFLICT", a3(api_m.replace(dong[0], dong[0].replace("CAS_CONFLICT", "X")) if dong else api_m))])

# A4
tl_m, tl_b = blob(M, "scripts/tl.py"), blob(B, "scripts/tl.py")
def a4(t):
    L = t.splitlines()
    return (L.count('EXPECT_VERSION = "2.21.2q"') == 1 and 'EXPECT_VERSION = "2.21.2p"' not in L
            and [x for x in L if x.startswith("VERSION = ")] == [x for x in tl_b.splitlines() if x.startswith("VERSION = ")])
ghi("A4", a4(tl_m), [("doi lai 2p", a4(tl_m.replace('EXPECT_VERSION = "2.21.2q"', 'EXPECT_VERSION = "2.21.2p"')))])

# A5 — chi kiem SU CO MAT cua ba ca trong tl_selftest.py cua merge; N/N lay tu gate output
st = blob(M, "scripts/tl_selftest.py")
CA = ["r119_api_contract_version_stamp_matches_expect", '"expect_version"', "r210_skill_tro_kich_ban_va_gas_dung_ban"]
print("# A5 su co mat ten ca trong tl_selftest.py@merge: " + ", ".join(f"{c}={c in st}" for c in CA)
      + "; vi tu r210 tren merge: " + repr([x.strip() for x in st.splitlines() if 'sk.count("2.21.2q")' in x][:2]))

# A6
sk_m, ins_m = blob(M, "SKILL.md"), blob(M, "INSTALL.md")
LS = "Các bản `.gs` tới 2.21.2p là lịch sử"
def a6(sk, ins):
    L = ins.splitlines()
    chi_dan = [x for x in L if "2.21.2q" in x and ("deploy" in x.lower() or "ping" in x)]
    p_dong = [x for x in L if "2.21.2p" in x]
    return (sk.count("2.21.2p") == 0 and sk.count("2.21.2q") >= 4 and ins.count("2.21.2p") == 1 and len(p_dong) == 1
            and LS in p_dong[0] and ins.count("2.21.2q") >= 3 and _ba_chi_dan(ins))
def _ba_chi_dan(ins):
    L = ins.splitlines()
    dep = [x for x in L if "Code.2.21.2q.gs" in x and "deploy" in x.lower()]
    png = [x for x in L if "ping" in x and "2.21.2q" in x]
    wa = [x for x in L if "Webapp cần deploy" in x]
    return bool(dep) and bool(png) and len(wa) >= 1 and all("2.21.2q" in x for x in wa)
print(f"# SKILL.md 2p={sk_m.count('2.21.2p')} 2q={sk_m.count('2.21.2q')}; INSTALL.md 2p={ins_m.count('2.21.2p')} 2q={ins_m.count('2.21.2q')}")
for x in ins_m.splitlines():
    if "2.21.2p" in x or "2.21.2q" in x:
        print("#   INSTALL: " + x.strip()[:200])
wa = [x for x in ins_m.splitlines() if "Webapp cần deploy" in x]
ghi("A6", a6(sk_m, ins_m), [("sot dong 'Webapp cần deploy' o 2p", a6(sk_m, ins_m.replace(wa[0], wa[0].replace("2.21.2q", "2.21.2p")) if wa else ins_m)),
                            ("xoa cum lich su", a6(sk_m, ins_m.replace(LS, "Các bản cũ là lịch sử")))])

print(f"TONG: {sum(ket)}/{len(ket)} tieu chi DAT (A1–A4, A6; A5 xem gate output)")
sys.exit(0 if all(ket) else 1)
