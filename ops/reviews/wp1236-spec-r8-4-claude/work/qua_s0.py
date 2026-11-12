"""Vòng 4: biến thể LOGIC của `cu_phap_run` giữ NGUYÊN VĂN sáu hằng (nên qua phần so byte + flags của A14-S0).
Đo cho mỗi biến thể: (1) A14-S0 phần `ast` theo HAI cách đọc câu chữ của đặc tả
    - S0_chat: mọi tên toàn cục mà thân cu_phap_run đọc ⊆ {RE_DON, RE_ONG} ∪ builtin {type, str}; mọi thuộc tính trên RE_DON/RE_ONG là `fullmatch`
    - S0_long: thân không đọc tên `re`, và mọi tên `RE_*` ∈ {RE_DON, RE_ONG}  (đủ để giết m-S0g "thêm một re.fullmatch")
(2) A14-S1 (109 AM đổi lý do?), A14-S2 (7 DUONG hỏng?), A14-S4 (kiểu), g1 52 vế (có vế được nhận?), A14-S6 (a) (61 530 đầu vào lệch tham chiếu),
    thân `run` của ci.yml@fe84620 (78) + 6 VL-F.
Biến thể nào qua A14-S0 VÀ 0 ở mọi ca hành vi = SỐNG SÓT; với nó, chạy Bash thật trên vài đầu vào ngoài kho để xem có nuốt lỗi không."""
import ast, json, os, re, subprocess, sys, tempfile, pathlib
S = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "soan"); sys.path.insert(0, S)
import gram, sinh_r8
from probes_r8 import AM, DUONG

HANG = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "spec_block.txt")).read()   # khối NGUYÊN VĂN của SPEC.md:390-395
REF = '''
def cu_phap_run(run, shell):
    if type(run) is not str:
        return "lenh_ngoai_cu_phap"
    if shell not in (None, "bash", "sh"):
        return "shell_ngoai_cu_phap"
    b = run[:-1] if run.endswith("\\n") else run
    if RE_DON.fullmatch(b):
        return None
    if RE_ONG.fullmatch(b):
        return None if shell == "bash" else "ong_khong_bash_tuong_minh"
    return "lenh_ngoai_cu_phap"
'''
def bien(**thay):
    s = REF
    for a, b in thay.items():
        a = {"b": '    b = run[:-1] if run.endswith("\\n") else run\n', "don": "    if RE_DON.fullmatch(b):\n",
             "ong": "    if RE_ONG.fullmatch(b):\n", "kieu": '    if type(run) is not str:\n        return "lenh_ngoai_cu_phap"\n'}[a]
        assert a in s, a
        s = s.replace(a, b)
    return s

V = {
 "L0_tham_chieu": REF,
 "L1_ong_match": bien(ong="    if RE_ONG.match(b):\n"),
 "L2_don_match(m-S4)": bien(don="    if RE_DON.match(b):\n"),
 "L3_rstrip(m-S2)": bien(b='    b = run.rstrip("\\n")\n'),
 "L4_strip(m-S3)": bien(b="    b = run.strip()\n"),
 "L5_bo_chu_thich": bien(b='    b = run[:-1] if run.endswith("\\n") else run\n    b = b.split(" #")[0]\n'),
 "L6_bo_va_cuoi": bien(don='    if RE_DON.fullmatch(b.removesuffix(" &")):\n'),
 "L7_bo_cham_than_dau": bien(don='    if RE_DON.fullmatch(b.removeprefix("! ")):\n'),
 "L8_splitlines": bien(b='    ls = run.splitlines()\n    b = ls[0] if len(ls) == 1 else "\\n"\n'),
 "L9_crlf": bien(b='    b = run.replace("\\r\\n", "\\n")\n    b = b[:-1] if b.endswith("\\n") else b\n'),
 "L10_ong_tung_doan": bien(ong='    if " | " in b and all(RE_DON.fullmatch(x) for x in b.split(" | ")):\n'),
 "L11_ong_pipe_amp": bien(ong='    if RE_ONG.fullmatch(b.replace(" |& ", " | ")):\n'),
 "L12_dong_cuoi": bien(b='    b = run[:-1] if run.endswith("\\n") else run\n    b = b.split("\\n")[-1]\n'),
 "L13_cham_phay_dau": bien(don='    if RE_DON.fullmatch(b.split("; ")[0]):\n'),
 "L14_hoac_vo_hai": bien(don='    if RE_DON.fullmatch(b.removesuffix(" || :")):\n'),
 "L15_tro_giup": REF.replace("    if RE_DON.fullmatch(b):\n", "    if _nhan(b):\n") +
    '\ndef _nhan(b):\n    return RE_DON.fullmatch(b) or re.fullmatch(LENH + r"(?: &)?", b, re.ASCII)\n',
 "L16_khong_str_None": bien(kieu='    if type(run) is not str:\n        return None\n'),
 "L17_ong_shell_khac_sh": REF.replace('None if shell == "bash"', 'None if shell != "sh"'),
}

BUILTIN = {"type", "str", "None"}
def s0(src, ns):
    t = ast.parse(src); fn = next(n for n in t.body if isinstance(n, ast.FunctionDef) and n.name == "cu_phap_run")
    loc = {a.arg for a in fn.args.args} | {n.id for n in ast.walk(fn) if isinstance(n, ast.Name) and isinstance(n.ctx, ast.Store)}
    doc = {n.id for n in ast.walk(fn) if isinstance(n, ast.Name) and isinstance(n.ctx, ast.Load)} - loc
    attr = {n.attr for n in ast.walk(fn) if isinstance(n, ast.Attribute) and isinstance(n.value, ast.Name) and n.value.id in ("RE_DON", "RE_ONG")}
    hang_ok = all(ns[k] == g for k, g in (("P", gram.P), ("W", gram.W), ("DANG", gram.DANG), ("LENH", gram.LENH))) and \
        ns["RE_DON"].pattern == gram.RE_DON.pattern and ns["RE_ONG"].pattern == gram.RE_ONG.pattern and \
        ns["RE_DON"].flags == ns["RE_ONG"].flags == re.compile("", re.ASCII).flags
    chat = hang_ok and doc <= {"RE_DON", "RE_ONG"} | BUILTIN and attr <= {"fullmatch"}
    long_ = hang_ok and "re" not in doc and {d for d in doc if d.startswith("RE_")} <= {"RE_DON", "RE_ONG"}
    return chat, long_

def g1_cases():
    CMD = "python .claude/dev/packet_loop_test.py"; PIPE = CMD + " | cat"; out = []
    for f in ("g1/rv-a1-8/work/probes.py", "g1/rv-a1-9/work/extra_shell_probes.py"):
        cs = next(eval(compile(ast.Expression(n.value), f, "eval"), {"CMD": CMD, "PIPE": PIPE})
                  for n in ast.walk(ast.parse(open(os.path.join(S, f), encoding="utf-8").read()))
                  if isinstance(n, ast.Assign) and getattr(n.targets[0], "id", None) == "cases")
        out += [(c[2] + "\n", c[1]) if "rv-a1-8" in f else (c[1] + "\n", c[2]) for c in cs]
    return out

def than_ci():
    import yaml
    R = os.path.join(S, "..", "..", "repo")
    y = yaml.safe_load(subprocess.run(["git", "-C", R, "show", "fe84620:.github/workflows/ci.yml"], capture_output=True, text=True, check=True).stdout)
    out = [(st["run"], st.get("shell")) for j in y["jobs"].values() for st in j.get("steps", []) if "run" in st]
    vlf = [("bash .github/checks/tl_selftest_bang_chung.sh\n", None), ("bash .github/checks/release_bundle_x2.sh\n", "bash"),
           ("python ops/cong_cu_test.py\n", "bash"), ("bash ops/chay_lease_publish_test.sh\n", "bash"),
           ("pwsh -NoProfile -File scripts/don-nhanh_test.ps1\n", None), ("bash ops/ci/gate_cgroup.sh\n", None)]
    return out, vlf

def bash(run, sh):
    """Chạy Bash thật: ops/hong_test.py hỏng (ghi DA_CHAY, thoát 1), ops/qua.py chép stdin."""
    with tempfile.TemporaryDirectory() as d:
        p = pathlib.Path(d); (p / "bin").mkdir(); (p / "ops").mkdir(); os.symlink(sys.executable, p / "bin/python")
        (p / "ops/hong_test.py").write_text(sinh_r8.HONG); (p / "ops/qua.py").write_text(sinh_r8.QUA)
        (p / "s.sh").write_text(run)
        rc = subprocess.run(sinh_r8.SHELL_LENH[sh] + [str(p / "s.sh")], cwd=d, env={"PATH": f"{p}/bin:/usr/bin:/bin", "HOME": d},
                            capture_output=True, stdin=subprocess.DEVNULL, timeout=20).returncode
        return rc, (p / "DA_CHAY").exists()

KIEU = [None, 1, 1.5, True, ["a"], {"a": 1}]
kho = sinh_r8.kho(); g1 = g1_cases(); ci, vlf = than_ci(); ref = gram.cu_phap_run
X = "python ops/hong_test.py"
NGOAI_KHO = [(f"{X} || :\n", None), (f"{X} &\n", None), (f"! {X}\n", None), (f"{X}; true\n", None), (f"{X} #c\n", None)]
kq = {}
for ten, src in V.items():
    ns = {"re": re}; exec(HANG + src, ns); f = ns["cu_phap_run"]
    chat, long_ = s0(HANG + src, ns)
    s1 = sum(f(r, s) != ref(r, s) for r, s in AM.values())
    s2 = sum(f(r, s) is not None for r, s in DUONG.values())
    s4 = sum(f(k, s) != "lenh_ngoai_cu_phap" for k in KIEU for s in (None, "bash"))
    g = sum(f(r, s) is None for r, s in g1)
    a = sum(f(r, s) != ref(r, s) for t in kho for s in sinh_r8.SHELL for r in (t, t + "\n"))
    c = sum(f(r, s) != ref(r, s) for r, s in ci + vlf)
    hv = s1 + s2 + s4 + g + a + c
    nk = [(r, s, *bash(r, s)) for r, s in NGOAI_KHO if f(r, s) is None and ref(r, s) is not None]
    kq[ten] = {"S0_chat": chat, "S0_long": long_, "A14_S1": s1, "A14_S2": s2, "A14_S4": s4, "g1_nhan": g, "A14_S6a_lech": a,
               "ci_vlf_lech": c, "song_sot_S0_chat_va_hanh_vi": chat and hv == 0, "song_sot_S0_long_va_hanh_vi": long_ and hv == 0,
               "ngoai_kho_nhan_bash(rc,DA_CHAY)": [(repr(r), s, rc, da) for r, s, rc, da in nk]}
    print(ten, kq[ten])
json.dump(kq, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "qua_s0.json"), "w"), ensure_ascii=False, indent=1)
