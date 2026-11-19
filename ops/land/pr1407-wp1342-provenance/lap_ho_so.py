"""Lap cay provenance ho so land PR #1407 tu cac tep da thu trong scratchpad. Dung: python lap_ho_so.py <scratchpad>"""
import pathlib, shutil, sys

S = pathlib.Path(sys.argv[1]); L = S / "land1407"
P = L / "ops/land/pr1407-wp1342-provenance"
assert not (L / "ops").exists(), "ops/ da ton tai"
CHEP = [
    # (nguon, dich tuong doi trong P)
    (L / "wdtmp/ci", "ci"),
    (L / "ci0/ci-provenance-thu.log", "ci-provenance-thu.log"),
    (L / "wdtmp/ci-provenance-thu-wd-44448900232.log", "wd/ci-provenance-thu-wd-44448900232.log"),
    (S / "desk1407/x", "windows-native/desktop/wp1342r4b-out"),
    (S / "vm1407/x", "windows-native/vm/wp1342r4b-vm-out"),
    (S / "win1342r4b/vm/TOM-TAT.txt", "windows-native/vm/TOM-TAT-phien-dieu-phoi.txt"),
    (S / "win1342r4b/desktop/do_r4.py", "windows-native/desktop/do_r4.py"),
    (S / "win1342r4b/desktop/chay-1342r4b.ps1", "windows-native/desktop/chay-1342r4b.ps1"),
    (L / "drv/dot_bien_r4_ban2.py", "windows-native/desktop/dot_bien_r4_ban2.py"),
    (S / "win1342r4/TOM-TAT.txt", "windows-native/desktop/luot1-728ecca/TOM-TAT.txt"),
    (S / "win1342r4/desktop/chay-1342r4.ps1", "windows-native/desktop/luot1-728ecca/chay-1342r4.ps1"),
    (S / "win1342r4/desktop/do_r4.py", "windows-native/desktop/luot1-728ecca/do_r4.py"),
    (S / "win1342r4/desktop/dot_bien_r4.py", "windows-native/desktop/luot1-728ecca/dot_bien_r4.py"),
    (L / "drv/suite-out.txt", "linux/suite-wp1342-wp1174.txt"),
    (L / "lease-wp1342-r4-g1-claude-sau-rut-han.yaml.txt", "lease-wp1342-r4-g1-claude-sau-rut-han.yaml.txt"),
    (L / "ai-dang-giu-sau-rut-han.txt", "ai-dang-giu-sau-rut-han.txt"),
]
for f in (L / "wdtmp/wd").iterdir():
    CHEP.append((f, "wd/" + f.name))
for d in ("rb", "lwtmp"):
    for f in (L / d).iterdir():
        CHEP.append((f, f.name))
for n in ("danh-gia-gate-output-44445202862.txt", "danh_gia_gate.py", "phan-chung-buoc-44445202862.txt",
          "readback_1407.py", "wd_dl.py", "trich_launcher.py", "lap_ho_so.py"):
    CHEP.append((L / "drv" / n, n))
for n in ("do_python_1407.py", "dot-bien-linux-a2c7d75.txt", "dot_bien_r4_ban1.py", "dot_bien_r4_ban2.py",
          "va_driver_ban2.py", "eol-policy-all-a2c7d75.json", "n2-test-46d3907.txt", "n23-phan-chung-a2c7d75.json",
          "n23_1407.py", "n2_test_r4.py", "nghiem-thu-a2c7d75.txt", "nghiem_thu_1407.py"):
    CHEP.append((L / "drv" / n, "linux/" + n))
for src, dst in CHEP:
    d = P / dst
    d.parent.mkdir(parents=True, exist_ok=True)
    if src.is_dir():
        shutil.copytree(src, d)
    else:
        shutil.copyfile(src, d)
(P / "windows-native/.gitattributes").write_bytes(b"* -text -whitespace\n")
print(sum(1 for f in P.rglob("*") if f.is_file()), "tep")
