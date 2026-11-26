"""Gỡ TỪNG chốt mới trên BẢN SAO tệp test (clone rời, không đụng kho), chạy ca phản chứng: phải rc=3 kèm DO:<ca phản chứng>:."""
import subprocess
import sys
from pathlib import Path

root = Path(sys.argv[1])
B, A = "ops/land_evidence_nguon_test.py", "ops/gate_output_doi_chieu_test.py"
c39, c40, a136 = "c39_c37_do_khi_bo_sinh_lech_mien", "c40_c36_do_khi_bang_cua_dot_a_mat_mien_hoac_o", "a136_a135_do_khi_bo_sinh_lech_mien"
C37 = "bang(len(vu_tru) == 158 and len(set(vu_tru)) == 158 and not lech,"
M = [("c36 so phan tu", B, "bang(rc == 0 and dem[0] - truoc == mong,", "bang(rc == 0,", c40),
     ("c36 tap category", B, "bang(not thieu,", "bang(True,", c40),
     ("c36 ngoai BMP", B, "bang(any(ord(c) > 0xFFFF for c in thay),", "bang(True,", c40),
     ("c37 tong 158", B, C37, "bang(len(set(vu_tru)) == len(vu_tru) and not lech,", c39),
     ("c37 khac nhau", B, C37, "bang(len(vu_tru) == 158 and not lech,", c39),
     ("c37 category", B, C37, "bang(len(vu_tru) == 158 and len(set(vu_tru)) == 158,", c39)]
M += [(f"a135 {ten}", A, f'("{ten}", ', f'("{ten}", True or ', a136)
      for ten in ("so_phan_tu", "category_vang", "lap_category", "thuoc_cam", "tu_0080", "cuoi_ngoai_bmp")]
xau = 0
for ten, tep, cu, moi, ca in M:
    p = root / tep
    goc = p.read_text(encoding="utf-8")
    assert goc.count(cu) == 1, (ten, goc.count(cu))
    try:
        p.write_text(goc.replace(cu, moi), encoding="utf-8", newline="")
        r = subprocess.run([sys.executable, "-B", tep, "--mot-ca", ca], cwd=root, capture_output=True, text=True, encoding="utf-8")
    finally:
        p.write_text(goc, encoding="utf-8", newline="")
    ok = r.returncode == 3 and r.stdout.startswith(f"DO:{ca}:")
    xau += not ok
    print(f"{'GIET' if ok else 'SONG'} | {ten} | {ca} | rc={r.returncode} | {r.stdout.strip()[:260]}", flush=True)
r = subprocess.run(["git", "status", "--porcelain"], cwd=root, capture_output=True, text=True)
print(f"GO CHOT: {len(M) - xau}/{len(M)} bi giet dung ca; cay sau khi do: {r.stdout.strip() or 'sach'}")
sys.exit(1 if xau else 0)
