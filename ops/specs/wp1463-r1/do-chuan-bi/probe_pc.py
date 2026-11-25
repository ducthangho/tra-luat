"""Probe wp1463: tập tệp phan_chung() mở + oracle vùng. Dùng qua do_vung_pr2.sh."""
import contextlib, hashlib, importlib.util, io, json, os, sys

Z0 = {"ops/ci_provenance_test.py", "ops/ci_provenance.py", ".github/workflows/ci.yml", "requirements.txt",
      ".claude/dev/ci_dang_ky_test.py", ".github/workflows/ops-do-workflow-definition.yml", "ops/bash_nen.py",
      ".github/workflows/ci-dot-bien-du.yml", ".github/workflows/launcher-windows.yml"}
GOC = frozenset({"AGENTS.md", "CHANGELOG.md", "CLAUDE.md", "CONTEXT.md", "INSTALL.md", "README.md", "SKILL.md"})
VT0 = (".claude/dev/ci_dang_ky_test.py", ".github/workflows/ops-do-workflow-definition.yml", "ops/bash_nen.py",
       ".github/workflows/ci-dot-bien-du.yml", ".github/workflows/launcher-windows.yml")


def oracle(doi, Z):
    if doi is None:
        return "day_du"
    for x in doi:
        if x in Z or x.startswith("ops/cai_") or x.startswith("ops/cong_cu") or ("/" not in x and x not in GOC):
            return "day_du"
    return "nhe"


def ngoai_vung(tap, Z):
    return sorted(x for x in tap if oracle({x}, Z) != "day_du")


if sys.argv[1] == "--oracle":
    them = sys.argv[3:]; Z = Z0 | set(them)
    tap = [l for l in open(sys.argv[2]).read().splitlines() if l]
    print("bo_day_du", tap)
    print("NGOAI_VUNG", ngoai_vung(tap, Z), "them_Z", them)
    sys.exit(0)

root = os.path.abspath(sys.argv[1]); mode = sys.argv[2]; tracked = set(open(sys.argv[3]).read().splitlines())
them = sys.argv[4:]; Z = Z0 | set(them)
os.chdir(root); sys.path.insert(0, root + "/.claude/dev"); sys.path.insert(0, root + "/ops")
spec = importlib.util.spec_from_file_location("reg", root + "/.claude/dev/ci_dang_ky_test.py")
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
k = "ops/ci_provenance_test.py"
print("MOI_sha16", hashlib.sha256(m.MOI[k].encode()).hexdigest()[:16], "trong_NHE", k in m.NHE)
if mode != "nguyen":
    m.NHE[k] = {"CI_PROVENANCE_KHONG_DOT_BIEN": "1"}; m.MAU_DAY_DU[k] = m.MOI[k]
    m.MAU_NHE[k] = r"(?ms)\A(?!.*^(?:TONG|TU KIEM PHAN HANG): DO\b).*^CA: ([1-9]\d*)/(\1) dat\nDOT BIEN: [1-9]\d* muc CHE DO NHE — do khi diff cham vung\nTU KIEM PHAN HANG: DAT \(\d+ dot bien\)\nTONG: DAT\n?\Z"
    m.VUNG_THEM[k] = VT0 + tuple(them)
    if mode == "bon":
        # bảng 27 hàng của r6 + hàng thêm cho từng đường dẫn mới (kỳ vọng day_du)
        rows = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "bang_r6.json")))
        rows += [[f"them_{i}", [p], "day_du"] for i, p in enumerate(them)]
        bad = [n for n, d, e in rows if m.ke_hoach(d)[k][0] != e or oracle(d, Z) != e]
        print("ke_hoach_va_oracle", f"{len(rows)-len(bad)}/{len(rows)}", bad)
    else:
        for d in (m.NHE, m.MAU_DAY_DU, m.MAU_NHE, m.VUNG_THEM):
            del d[k]
opened = set()


def hook(ev, args):
    if ev == "open" and args and isinstance(args[0], (str, bytes)):
        opened.add(os.path.relpath(os.path.abspath(os.fsdecode(args[0])), root))


sys.addaudithook(hook)
buf = io.StringIO()
with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(io.StringIO()):
    r = m.phan_chung()
tap = sorted(opened & tracked)
print("phan_chung", r, [l for l in buf.getvalue().splitlines() if "PHẢN CHỨNG" in l][-1:])
print("mo", tap)
print("NHAN_CHUNG_ci_yml", ".github/workflows/ci.yml" in tap, "NGOAI_VUNG", ngoai_vung(tap, Z))
