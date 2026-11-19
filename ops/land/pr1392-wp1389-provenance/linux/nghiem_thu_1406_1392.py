"""Do lai Linux re sau merge cho ho so land PR #1406 (#1404) va PR #1392 (#1389), tren clone detached 4eda94e (chua ca hai merge).
Dung: python nghiem_thu_1406_1392.py <clone> <goc kho chinh (de nap ops.bash_nen)> <tep_ra_1406> <tep_ra_1392>
Bash goi qua ops.bash_nen.tim_bash() (khong bash tran). Moi lenh ghi rc va output tho."""
import datetime, os, subprocess, sys, tempfile
C, GOC, R1, R2 = sys.argv[1:5]
sys.path.insert(0, GOC)
from ops.bash_nen import tim_bash  # noqa: E402
BASH = tim_bash()[0]


def chay(f, cmd, nhan=None):
    t0 = datetime.datetime.now(datetime.timezone.utc)
    p = subprocess.run(cmd, cwd=C, capture_output=True, text=True, encoding="utf-8", errors="replace", stdin=subprocess.DEVNULL, timeout=1800)
    f.write(f"\n## {t0:%Y-%m-%dT%H:%M:%SZ} $ {nhan or ' '.join(cmd)}\n{p.stdout}{p.stderr}rc={p.returncode}\n"); f.flush()
    return p


for ra, m, ten, ws, extra in (
        (R1, "cad9b1fa95da303b085a4555e85608c0b77b8ae0", "#1406 (#1404)", [".claude/dev/launcher_test.py", "ops/acceptance/wp1404/RESULTS.md",
         "ops/acceptance/wp1404/VERDICT.md", "ops/cai_cong_cu.sh", "ops/leases/wp1404-r1-g1-claude.yaml", "ops/specs/wp1404-r1.md"], "1404"),
        (R2, "11bd0336d00b4a9544e70dcbbe049d372053a3ec", "#1392 (#1389)", [".agents/skills/playwright-browser/SKILL.md", "ops/acceptance/wp1389/REVIEW-PROMPT.md",
         "ops/acceptance/wp1389/RESULTS.md", "ops/acceptance/wp1389/VERDICT.md", "ops/acceptance/wp1389/residue_matrix.ps1",
         "ops/acceptance/wp1389/residue_matrix.sh", "ops/leases/wp1389-r1-g1-claude.yaml", "ops/specs/wp1389-r1.md"], "1389")):
    f = open(ra, "w", encoding="utf-8")
    f.write(f"# do lai Linux sau merge {ten}, merge {m}; clone detached {subprocess.run(['git','rev-parse','HEAD'],cwd=C,capture_output=True,text=True).stdout.strip()}; python {sys.version.split()[0]}; bash {BASH}\n")
    chay(f, ["git", "rev-parse", m, f"{m}^{{tree}}", f"{m}^1", f"{m}^2", f"{m}^2^{{tree}}"])
    chay(f, ["git", "diff", "--numstat", f"{m}^1", m])
    chay(f, ["git", "diff", "--numstat", f"{m}^2", m])   # rong khi tree merge = tree head
    chay(f, ["git", "diff", "--check", f"{m}^1", m])
    chay(f, ["git", "rev-parse", *[f"{m}:{w}" for w in ws], *[f"{m}^2:{w}" for w in ws], *[f"HEAD:{w}" for w in ws]])
    chay(f, ["git", "diff", "--numstat", f"{m}", "HEAD", "--", *ws])   # write set khong doi tu merge toi 4eda94e
    if extra == "1404":
        for ca in ("r1404_cai_apt_update_roi_thu_lai", "r1404_thu_lai_chot_chi_tiet", "r886_ten_python_khop_cai_cong_cu_sh"):
            chay(f, [sys.executable, "-B", ".claude/dev/launcher_test.py", "--lap-ca", ca, "--lan", "1"])
        chay(f, [BASH, "-n", "ops/cai_cong_cu.sh"])
    else:
        d = tempfile.mkdtemp(prefix="rm1389-")
        chay(f, [BASH, "ops/acceptance/wp1389/residue_matrix.sh", ".agents/skills/playwright-browser/SKILL.md", d],
             f"{BASH} ops/acceptance/wp1389/residue_matrix.sh .agents/skills/playwright-browser/SKILL.md <scratch rong tam>")
        chay(f, [BASH, "-n", "ops/acceptance/wp1389/residue_matrix.sh"])
    f.write("\n# HET\n"); f.close()
