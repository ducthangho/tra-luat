"""Do lai Linux re sau merge cho ho so land PR #1414 (#387 packet B). Dung: python nghiem_thu_1414.py <clone 0ca331b> <clone 3b64746> <tep_ra>
Chi goi git/python truc tiep (khong bash). Moi lenh ghi kem rc va output tho."""
import datetime, subprocess, sys

C, B, OUT = sys.argv[1], sys.argv[2], sys.argv[3]
M, H, BASE = "0ca331b4a11835913bb91618d310a34e65599c20", "9804f642ad9c7abcc9e7ae4877c2ff133ef31f00", "3b647461db7c8ded1bddd9aafc5c6aa5eead223f"
WS = [".claude/dev/launcher.py", ".claude/dev/launcher_test.py"]
CA = ["r387_fixture_teardown_bao_loi_giu_loi_goc", "r387_m1_chau_ghi_muon_khai_pham_vi_bam", "r387_m1_doi_chung_ghi_som_lam_ve_bam_do",
      "r387_m1_con_thuong_chung_minh_cay_chet", "r387_m2_chau_ghi_trong_han_thi_bam_du", "r387_m2_khong_do_duoc_thi_khong_cho",
      "r387_m2_han_chung_cho_moi_lan_do", "r387_a_nen_khac_giu_moc_ket_thuc_base", "r387_m1_stop_trong_luc_cho_khong_bi_de",
      "r387_m1_prompt_linux_xoa_khi_cay_chet", "r387_m2_ngat_trong_luc_doi_ghi_bi_ngat", "t117_moi_mau_dot_bien_phai_khop_DUNG_MOT_cho"]
f = open(OUT, "w", encoding="utf-8")


def chay(cmd, cwd, nhan=None):
    t0 = datetime.datetime.now(datetime.timezone.utc)
    p = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    f.write(f"\n## {t0:%Y-%m-%dT%H:%M:%SZ} (cwd {nhan or cwd}) $ {' '.join(cmd)}\n{p.stdout}{p.stderr}rc={p.returncode}\n")
    f.flush()
    return p


f.write(f"# do lai Linux sau merge PR #1414, merge {M}, head {H}, base {BASE}; python {sys.version.split()[0]}\n")
chay(["git", "rev-parse", "HEAD", "HEAD^{tree}", "HEAD^1", "HEAD^2"], C, "clone-merge")
chay(["git", "diff", "--numstat", "HEAD^1", "HEAD"], C, "clone-merge")
chay(["git", "diff", "--name-only", "HEAD^1", "HEAD"], C, "clone-merge")
chay(["git", "rev-parse", *[f"{M}:{w}" for w in WS], *[f"{H}:{w}" for w in WS]], C, "clone-merge")
chay(["git", "diff", "--check", "HEAD^1", "HEAD"], C, "clone-merge")
for ca in CA:
    chay([sys.executable, ".claude/dev/launcher_test.py", "--lap-ca", ca, "--lan", "1"], C, "clone-merge")
chay([sys.executable, "-m", "ruff", "--version"], C, "clone-merge")
for d, nhan in ((B, "clone-base"), (C, "clone-merge")):
    chay([sys.executable, "-m", "ruff", "check", "--select", "F", "--output-format", "concise", *WS], d, nhan)
for d, nhan in ((B, "clone-base"), (C, "clone-merge")):
    p = chay([sys.executable, ".claude/dev/launcher.py", "doctor"], d, nhan)
f.write("\n# HET\n")
