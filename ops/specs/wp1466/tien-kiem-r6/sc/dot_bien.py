"""Đột biến khối tien-kiem r6 trên BẢN SAO; mỗi đột biến chạy trọn fx_tien_kiem.py. Dùng: python -B dot_bien.py <r6> <lease_publish.py>"""
import pathlib, subprocess, sys
S, LP = pathlib.Path(sys.argv[1]).resolve(), sys.argv[2]
goc = (S / "sc/tien_kiem.py").read_text(encoding="utf-8")
DB = {
    "M1_quet_trong_cay_lam_viec": ('lp._quet_lease_toan_kho(pathlib.Path(td), ', 'lp._quet_lease_toan_kho(pathlib.Path("."), '),
    "M2_bo_kiem_B_thuoc_anh_chup": ('    if tt.returncode:\n', '    if False:\n'),
    "M3_nap_lp_tu_cay_lam_viec": ('exec(compile(git("-C", td, "cat-file", "blob", f"{ob}:ops/lease_publish.py"), f"{ob}:ops/lease_publish.py", "exec"), lp.__dict__)',
                                  'exec(compile(open("ops/lease_publish.py", encoding="utf-8").read(), "ops/lease_publish.py", "exec"), lp.__dict__)'),
}
for ten, (cu, moi) in DB.items():
    assert goc.count(cu) == 1, ten
    p = S / "dot" / f"{ten}.py"; p.write_text(goc.replace(cu, moi), encoding="utf-8")
    r = subprocess.run([sys.executable, "-B", str(S / "sc/fx_tien_kiem.py"), str(S), LP, str(p)], capture_output=True, text=True)
    sai = [d.split()[1] for d in r.stdout.splitlines() if d.startswith("SAI")]
    print(f"{ten}: rc={r.returncode} · {r.stdout.strip().splitlines()[-1]} · đỏ: {sai}", flush=True)
r = subprocess.run([sys.executable, "-B", str(S / "sc/fx_tien_kiem.py"), str(S), LP, str(S / "sc/tien_kiem_r5.py")], capture_output=True, text=True)
print(f"KHOI_R5_NGUYEN_VAN: rc={r.returncode} · {r.stdout.strip().splitlines()[-1]} · đỏ: {[d.split()[1] for d in r.stdout.splitlines() if d.startswith('SAI')]}")
