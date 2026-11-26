"""Đột biến khối tien-kiem r7 trên BẢN SAO; mỗi đột biến chạy trọn fx_tien_kiem.py (33, r6) và fx_r7.py (21).

Dùng: /usr/bin/python3 -B dot_bien_r7.py <r7> <lease_publish.py>
Môi trường của cả lượt đặt PYTHONNOUSERSITE=1: máy đo có PyYAML ở site người dùng, và đột biến M6 (bỏ tự chạy lại
với -I) sẽ nạp bản ấy rồi bị T4 từ chối ở MỌI kịch bản ĐẠT — đó là biến của máy, không phải của chốt đang đo.
"""
import datetime, os, pathlib, subprocess, sys
S, LP = pathlib.Path(sys.argv[1]).resolve(), sys.argv[2]
goc = (S / "sc/tien_kiem.py").read_text(encoding="utf-8")
DB = {
    "M1_quet_trong_cay_lam_viec": [('lp._quet_lease_toan_kho(pathlib.Path(td), ', 'lp._quet_lease_toan_kho(pathlib.Path("."), ')],
    "M2_bo_kiem_B_thuoc_anh_chup": [('    if tt.returncode:\n', '    if False:\n')],
    "M3_nap_lp_tu_cay_lam_viec": [('exec(compile(git("-C", td, "cat-file", "blob", f"{ob}:ops/lease_publish.py"), f"{ob}:ops/lease_publish.py", "exec"), lp.__dict__)',
                                   'exec(compile(open("ops/lease_publish.py", encoding="utf-8").read(), "ops/lease_publish.py", "exec"), lp.__dict__)')],
    "M4_bo_policy_tren_master_V": [('    if pol_m:\n', '    if False:\n')],
    "M5_bo_policy_doi_trong_B_master": [('    if pol_d:\n', '    if False:\n')],
    "M5b_bo_m_cua_log": [('"log", "-m", ', '"log", ')],
    "M6_bo_tu_chay_lai_voi_I": [('    os.execv(sys.executable, [sys.executable, "-I", *sys.orig_argv[1:]])\n', '    pass\n')],
    "M7_bo_kiem_vi_tri_pyyaml": [('    if sp is None or not nguon_ok(noi_nap(sp)):\n', '    if False:\n')],
    "M8_bo_kiem_moi_module": [('    if sai:\n', '    if False:\n')],
    "M9a_bo_kiem_git_truoc_T1": [('if not GIT or any(trong(GIT, c) for c in CAM):\n', 'if not GIT:\n')],
    "M9b_bo_kiem_git_sau_T1": [('    if any(trong(GIT, c) for c in CAM):\n', '    if False:\n')],
    "M10_git_cuc_bo_dung_moi_truong_nguoi_goi": [('    E_CB = {"PATH": os.path.dirname(GIT), "HOME": os.path.join(tg, "home"), "GIT_CONFIG_NOSYSTEM": "1", "GIT_CONFIG_GLOBAL": os.devnull}\n',
                                                  '    E_CB = dict(os.environ)\n')],
    "M11_bo_T6": [('    if ls_remote() != mc:\n', '    if False:\n')],
    "M12_kiem_to_tien_trong_clone": [('[GIT, "-C", td, "merge-base"', '[GIT, "merge-base"')],
}
env = dict(os.environ, PYTHONNOUSERSITE="1")
def chay(tk):
    do = []
    for fx in ("fx_tien_kiem.py", "fx_r7.py"):
        r = subprocess.run([sys.executable, "-B", str(S / "sc" / fx), str(S), LP, str(tk)], capture_output=True, text=True, env=env)
        dong = r.stdout.strip().splitlines()
        do += [d.split()[1] for d in dong if d.startswith("SAI")]
        do.append(f"[{fx}: {next((d for d in dong if d.startswith('TONG')), 'không có dòng TONG: ' + r.stderr[-200:])}]")
    return do
print("BAT_DAU", datetime.datetime.now(datetime.timezone.utc).strftime("%FT%TZ"), flush=True)
print("KHOI_R7_NGUYEN_VAN:", chay(S / "sc/tien_kiem.py"), flush=True)
for ten, thay in DB.items():
    s = goc
    for cu, moi in thay:
        assert s.count(cu) == 1, (ten, cu)
        s = s.replace(cu, moi)
    p = S / "dot" / f"{ten}.py"; p.write_text(s, encoding="utf-8")
    print(f"{ten}: đỏ {chay(p)}", flush=True)
for ten in ("tien_kiem_r6.py", "tien_kiem_r5.py"):
    print(f"KHOI_{ten}: đỏ {chay(S / 'sc' / ten)}", flush=True)
print("KET_THUC", datetime.datetime.now(datetime.timezone.utc).strftime("%FT%TZ"), flush=True)
