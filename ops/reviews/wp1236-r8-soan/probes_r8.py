"""Phản chứng cho K7-S (ops/specs/wp1236-r8.md): mỗi biến thể chạy Bash THẬT với chương trình hỏng (rc 1) và được phân loại bằng
cài đặt tham chiếu `gram.py`. Đòi: mọi biến thể âm -> grammar từ chối; mọi đối chứng dương -> grammar nhận VÀ Bash/sh thật trả rc != 0.
Danh mục l8_*/l9_* DỰNG LẠI từ văn bản VERDICT #1236 issuecomment-6690875449 / 6691822431; script gốc của reviewer (work/probes.py,
work/extra_shell_probes.py) không có trong kho. Chạy: python3 -I ops/reviews/wp1236-r8-soan/probes_r8.py (cwd bất kỳ)."""
import json, os, subprocess, sys, tempfile, pathlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gram import cp
X = "python ops/hong_test.py"; Y = "python ops/qua.py"
AM = {  # nhãn: (thân run, shell)
 # --- F12 lượt 8 (dựng lại từ văn bản VERDICT 6690875449 / 6690900537) ---
 "l8_01_set_trong_if_false": (f"if false; then set -o pipefail; fi\n{X} | {Y}\n", None),
 "l8_02_set_trong_ham_chua_goi": (f"f() {{ set -o pipefail; }}\n{X} | {Y}\n", None),
 "l8_03_set_trong_subshell": (f"(set -o pipefail)\n{X} | {Y}\n", None),
 "l8_04_set_trong_command_subst": (f": \"$(set -o pipefail)\"\n{X} | {Y}\n", None),
 "l8_05_builtin_set_tat": (f"builtin set +o pipefail\n{X} | {Y}\n", "bash"),
 "l8_06_command_set_tat": (f"command set +o pipefail\n{X} | {Y}\n", "bash"),
 "l8_07_tuy_chon_nhay_don": (f"set +o 'pipefail'\n{X} | {Y}\n", "bash"),
 "l8_08_tuy_chon_nhay_kep": (f"set +o \"pipefail\"\n{X} | {Y}\n", "bash"),
 "l8_09_noi_dong": (f"set \\\n +o pipefail\n{X} | {Y}\n", "bash"),
 "l8_10_set_sau_ong": (f"{X} | {Y}\nset -o pipefail\n", None),
 "l8_11_set_trong_while_khong_chay": (f"while false; do set -o pipefail; done\n{X} | {Y}\n", None),
 "l8_12_set_trong_case_khong_khop": (f"case a in b) set -o pipefail;; esac\n{X} | {Y}\n", None),
 "l8_13_eval_tat": (f"eval 'set +o pipefail'\n{X} | {Y}\n", "bash"),
 "l8_14_shopt_tat": (f"shopt -u -o pipefail\n{X} | {Y}\n", "bash"),
 "l8_15_set_tat_errexit": (f"set +e\n{X}\ntrue\n", None),
 "l8_16_set_ghep_co_tat": (f"set -euo pipefail +e\n{X}\ntrue\n", None),
 # --- F12 lượt 9 (văn bản VERDICT 6691822431) ---
 "l9_01_ong_trong_if": (f"if {X} | {Y}; then :; fi\n", "bash"),
 "l9_02_ong_trong_while": (f"while {X} | {Y}; do break; done\n", "bash"),
 "l9_03_ong_trong_until": (f"until {X} | {Y}; do break; done\n", "bash"),
 "l9_04_va_va": (f"{X} && true\n", None),
 "l9_05_hoac_hoac": (f"{X} || true\n", None),
 "l9_06_phu_dinh_ong": (f"! {X} | {Y}\n", "bash"),
 "l9_07_ong_chay_nen": (f"{X} | {Y} &\n", "bash"),
 "l9_08_for_hoac": (f"for i in 1; do {X}; done || true\n", None),
 "l9_09_trap_doi_ma": (f"trap 'exit 0' EXIT\n{X}\n", None),
 "l9_10_if_khong_ong": (f"if {X}; then :; fi\n", None),
 # --- connector ---
 "c4495417390_if_false_pipefail": (f"if false; then\n  set -o pipefail\nfi\n{X} | {Y}\n", None),
 "c4493205478_pipefail_sau_ong": (f"{X} | {Y}\nset -o pipefail\n", None),
 "c4495881317_if_ong_bash": (f"if {X} | {Y}; then :; fi\n", "bash"),
 "c4495881317_ong_hoac_true": (f"{X} | {Y} || true\n", "bash"),
 "c4495881327_thay_lenh_trong_nhay_kep": (f"echo \"$({X} | {Y})\"\n", None),
 "c4495881327_thay_lenh_doi_so_nhay_kep": (f"python ops/qua.py \"$({X} | {Y})\"\n", None),
 # --- bổ sung của grammar r8 (phiên soạn) ---
 "g_cham_phay": (f"{X}; true\n", None),
 "g_hai_dong": (f"{X}\ntrue\n", None),
 "g_hai_lf_cuoi": (f"{X}\n\n", None),
 "g_bash_c": ("bash -c 'python ops/hong_test.py || true'\n", None),
 "g_sh_c": ("sh -c 'python ops/hong_test.py || true'\n", None),
 "g_eval": ("eval python ops/hong_test.py\n", None),
 "g_exec": (f"exec {X}\n", None),
 "g_python_c": ("python -c 'import sys'\n", None),
 "g_python_stdin": ("python - <<'PY'\nprint(1)\nPY\n", None),
 "g_gan_bien_dau": (f"A=1 {X}\n", None),
 "g_chuyen_huong": (f"{X} > /dev/null\n", None),
 "g_chuyen_huong_2": (f"{X} 2>&1\n", None),
 "g_ong_va_loi": (f"{X} |& {Y}\n", "bash"),
 "g_ngoac_nhon": (f"{{ {X}; }}\n", None),
 "g_command_subst": (f"python $(echo ops/hong_test.py)\n", None),
 "g_backtick": ("python `echo ops/hong_test.py`\n", None),
 "g_bieu_thuc_actions": ("python ops/hong_test.py ${{ matrix.k }}\n", None),
 "g_bien": ("python ops/hong_test.py $X\n", None),
 "g_chu_thich": (f"{X} # || true\n", None),
 "g_tab": ("python\tops/hong_test.py\n", None),
 "g_cr": (f"{X}\r\n", None),
 "g_dau_cach_cuoi": (f"{X} \n", None),
 "g_hai_dau_cach": ("python  ops/hong_test.py\n", None),
 "g_chu_dong_hinh": ("pythοn ops/hong_test.py\n", None),
 "g_chu_so_unicode": ("python ops/hong_test١.py\n", None),
 "g_ong_khong_bash": (f"{X} | {Y}\n", None),
 "g_ong_sh": (f"{X} | {Y}\n", "sh"),
 "g_pwsh_shell": (f"{X}\n", "pwsh"),
 "g_lenh_ngoai_ds": ("cat ops/hong_test.py\n", None),
 "g_ong_toi_cat": (f"{X} | cat\n", "bash"),
 "g_glob": ("python ops/*.py\n", None),
 "g_ngoa": ("python ~/x.py\n", None),
 "g_run_khong_phai_chuoi": (None, None),
 "g_run_khong_phai_chuoi_pwsh": (None, "pwsh"),   # H04 (Codex r8 vòng 1): thứ tự bước 1–2 phân biệt được
 "g_hai_lenh_hop_le": (f"{X}\n{Y}\n", None),
 "g_python_c_tran": ("python -c pass\n", None),
 "g_bash_c_tran": ("bash -c true\n", None),
 "g_tuyet_doi": ("python /tmp/x.py\n", None),
 "g_tab_doi_so": (f"{X}\t--json\n", None),
 "g_hai_dau_cach_doi_so": (f"{X}  --json\n", None),
}
for c in ";&|!(){}$`'\"\\<>#*?[]~\t\n\r":   # họ ký tự: m-S14[c] thêm c vào W phải làm đúng ca này ĐỎ
    AM[f"kt_{ord(c):02x}"] = (f"{X} a{c}b\n", None)
DUONG = {
 "d_mot_lenh": (f"{X}\n", None), "d_mot_lenh_khong_lf": (X, None), "d_mot_lenh_bash": (f"{X}\n", "bash"),
 "d_mot_lenh_sh": (f"{X}\n", "sh"), "d_doi_so": (f"{X} --json --strict\n", None),
 "d_ong_bash_trai_hong": (f"{X} | {Y}\n", "bash"), "d_ong_bash_phai_hong": (f"{Y} | {X}\n", "bash"),
}
SHELL = {None: ["bash", "-e"], "bash": ["bash", "--noprofile", "--norc", "-eo", "pipefail"], "sh": ["sh", "-e"]}
def chay(run, shell):
    if run is None or shell == "pwsh": return None, False
    with tempfile.TemporaryDirectory() as d:
        p = pathlib.Path(d); (p/"ops").mkdir(); (p/"bin").mkdir()
        (p/"ops/hong_test.py").write_text("import pathlib, sys; pathlib.Path(sys.argv[0]).with_name(\"DA_CHAY\").touch(); sys.exit(1)\n"); (p/"ops/qua.py").write_text("import sys; sys.stdout.write(sys.stdin.read())\n")
        os.symlink(sys.executable, p/"bin/python"); (p/"s.sh").write_text(run)
        env = {"PATH": f"{p}/bin:/usr/bin:/bin", "HOME": d}
        rc = subprocess.run(SHELL[shell] + [str(p/"s.sh")], cwd=d, env=env, capture_output=True, stdin=subprocess.DEVNULL, timeout=20).returncode
        return rc, (p/"ops/DA_CHAY").exists()   # H03 (Codex r8 vòng 1): rc 0 chỉ là "nuốt lỗi" khi chương trình hỏng ĐÃ CHẠY
def main():
    kq = {"am": {}, "duong": {}}; hong = 0
    for k, (r, s) in AM.items():
        ly = cp(r, s); rc, dc = chay(r, s); kq["am"][k] = {"grammar": ly, "rc_bash": rc, "da_chay_ct_hong": dc}
        if ly is None: hong += 1; print("LOT", k)
    for k, (r, s) in DUONG.items():
        ly = cp(r, s); rc, dc = chay(r, s); kq["duong"][k] = {"grammar": ly, "rc_bash": rc, "da_chay_ct_hong": dc}
        if ly is not None or rc == 0 or not dc: hong += 1; print("DUONG HONG", k, ly, rc)
    nuot = [k for k, v in kq["am"].items() if v["rc_bash"] == 0]
    print(json.dumps({"am": len(AM), "am_bi_tu_choi": sum(v["grammar"] is not None for v in kq["am"].values()),
                      "am_bash_rc0": len(nuot), "am_nuot_loi_that": sum(v["rc_bash"] == 0 and v["da_chay_ct_hong"] for v in kq["am"].values()), "duong": len(DUONG), "hong": hong}, ensure_ascii=False))
    json.dump(kq, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "probes_r8.json"), "w"), ensure_ascii=False, indent=1)
    sys.exit(1 if hong else 0)


if __name__ == "__main__":
    main()
