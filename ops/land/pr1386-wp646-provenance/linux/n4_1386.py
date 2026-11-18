"""Do THAT N4 cua #646 (spec LEASE-TRUONG-KHAI-NGHIA-r1 §4 N4) bang `git grep` that, ngoai kho.
Dung: python -X utf8 -B n4_1386.py <clone_day_du_lich_su> <M>
  M = merge (bf47a36); moi phep chay `git grep -n <co> -e <mau> M -- <tep>`; so hit = so dong in ra, rc = rc cua git grep.
Phan chung (trong ban sao tam o M, grep tren cay lam viec): dan sai ten `cmd_kiem_dong`, `BAT_BUOC_LEASE` => -Fw 0 hit rc 1;
  go cau doc han `han = _doc_han(lease["lease_expires_at_utc"])` khoi ops/lease_publish.py => mau duong tuong ung 0 hit rc 1;
  go cau kiem dang `if not SHA40.match(sha):` => mau duong tuong ung 0 hit rc 1."""
import json, os, pathlib, subprocess, sys, tempfile
SRC, M = pathlib.Path(sys.argv[1]), sys.argv[2]
ENV = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
ENV.update(GIT_CONFIG_NOSYSTEM="1", GIT_CONFIG_GLOBAL="/dev/null")


def gg(goc, co, mau, tep, rev=None):
    lenh = ["git", "-C", str(goc), "grep", "-n", *co, "-e", mau] + ([rev] if rev else []) + ["--", *tep]
    p = subprocess.run(lenh, capture_output=True, text=True, env=ENV)
    dong = [d for d in p.stdout.splitlines() if d]
    return {"lenh": " ".join(lenh[3:]), "rc": p.returncode, "hit": len(dong), "dong": dong[:5]}


LP, CI_, PL = "ops/lease_publish.py", "ops/ci_duong_nhanh.py", ".claude/dev/packet_loop.py"
SAU = [LP, PL, ".claude/dev/launcher.py", ".claude/dev/gate_lifecycle.py", ".github/workflows/ci.yml", ".github/workflows/ops-publish-lease.yml"]
KY = []   # (nhom, co, mau, tep, hit_ky_vong, rc_ky_vong)
for t in SAU:
    KY.append(("i", ["-Fw"], "heartbeat_at", [t], 0, 1))
KY.append(("ii", ["-Fw"], "heartbeat_at", [":(glob).claude/dev/*.py", ":(glob)ops/*.py"], 1, 0))
for m in [r"^BAT_BUOC = \(", r"^def kiem\(", r"^def kiem_github\(", r"^def _phan_loai_lease\(", r'add_parser\("ai-dang-giu"']:
    KY.append(("iii", ["-E"], m, [LP], 1, 0))
KY.append(("iii", ["-Fw"], "lease_until", [LP], 0, 1))
for m in ['han = _doc_han(lease["lease_expires_at_utc"])', "if not bo_qua_han and han <= datetime.now(timezone.utc):",
          'han = _doc_han(lease.get("lease_expires_at_utc"))', 'sha = str(lease["reviewed_sha_required"]).strip()',
          "if not SHA40.match(sha):", "kiem(lease, tep, goc, bo_qua_han=True)"]:
    KY.append(("iii", ["-F"], m, [LP], 1, 0))
KY.append(("iv", ["-E"], r"^def kiem_lease\(", [CI_], 1, 0))
for m in ['han = _han_lease(lease.get("lease_expires_at_utc"))', 'lenh = [sys.executable, "-B", "-c", MA_KIEM_HET_HAN, duong]',
          "lp.kiem(lp._doc_yaml(sys.argv[1]), sys.argv[1], '.', bo_qua_han=True)"]:
    KY.append(("iv", ["-F"], m, [CI_], 1, 0))
for m in [r"^def cmd_kiem_dong_wp\(", r'add_parser\("kiem-dong-wp"', "D4 lease", r"^def cmd_kiem_merge\(", r'add_parser\("kiem-merge"',
          r'_dk\("K0 ', r'_dk\("K3 ', r'_dk\("K4 ', r"^def _human_merge\(", r"^def cmd_record_review\(", r'add_parser\("record-review"',
          r'a\.reviewed_sha != st\["reviewing_head_sha"\]']:
    KY.append(("v", ["-E"], m, [PL], 1, 0))
KY.append(("v", ["-F"], 'str(ls.get("lease_until"))', [PL], 1, 0))
KY.append(("v", ["-Fw"], "reviewed_sha_required", [PL], 0, 1))

bao = {"M": M, "phep": [], "phan_chung": {}}
for nhom, co, mau, tep, hk, rk in KY:
    r = gg(SRC, co, mau, tep, M)
    r.update(nhom=nhom, hit_ky_vong=hk, rc_ky_vong=rk, dung=(r["hit"] == hk and r["rc"] == rk))
    bao["phep"].append(r)

with tempfile.TemporaryDirectory() as tmp:
    d = pathlib.Path(tmp) / "m"
    subprocess.run(["git", "clone", "-q", "--no-hardlinks", "--no-checkout", str(SRC), str(d)], check=True)
    subprocess.run(["git", "-c", "advice.detachedHead=false", "checkout", "-q", "--detach", M], cwd=d, check=True)
    for ten in ("cmd_kiem_dong", "BAT_BUOC_LEASE"):
        r = gg(d, ["-Fw"], ten, [PL, LP])
        r["ket_qua"] = "DO_DUNG" if (r["hit"] == 0 and r["rc"] == 1) else "SONG"
        bao["phan_chung"][f"ten_sai_{ten}"] = r
    for ten, cau in (("go_cau_doc_han_kiem", 'han = _doc_han(lease["lease_expires_at_utc"])'), ("go_cau_kiem_dang", "if not SHA40.match(sha):")):
        f = d / LP
        goc = f.read_bytes()
        truoc = gg(d, ["-F"], cau, [LP])
        dong = [x for x in goc.split(b"\n") if cau.encode() in x]
        if len(dong) != 1:
            bao["phan_chung"][ten] = {"ket_qua": f"KHONG_DO: cau khop {len(dong)} dong"}
            continue
        f.write_bytes(goc.replace(dong[0] + b"\n", b"", 1))
        sau = gg(d, ["-F"], cau, [LP])
        f.write_bytes(goc)
        bao["phan_chung"][ten] = {"truoc": truoc, "sau": sau,
                                  "ket_qua": "DO_DUNG" if (truoc["hit"] == 1 and sau["hit"] == 0 and sau["rc"] == 1) else "SONG"}

ok = all(p["dung"] for p in bao["phep"]) and all(v.get("ket_qua") == "DO_DUNG" for v in bao["phan_chung"].values())
bao["so_phep"] = len(bao["phep"])
bao["so_phep_dung"] = sum(p["dung"] for p in bao["phep"])
bao["TONG"] = "DAT" if ok else "KHONG_DAT"
print(json.dumps(bao, ensure_ascii=False, indent=1))
sys.exit(0 if ok else 1)
