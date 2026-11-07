"""Đột biến KHÔNG tương đương ở các vị trí kho sinh A14-S6 chưa phủ. Đo: A14-S1 (109 AM: đổi lý do?), A14-S2 (7 DUONG: hỏng?),
52 vế gen 1 (có vế được nhận?), A14-S6 (a) (lệch tham chiếu trên 11 838 đầu vào), 30 thân bước luật thật của ci.yml@fe84620 + 6 giá trị VL-F.
Vế (b) của A14-S6 chỉ chạy trên thân được nhận; khi (a) = 0 lệch thì tập thân nhận = tập của tham chiếu nên (b) = 0 theo cấu trúc."""
import os, re, sys, json, ast, subprocess
S = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "soan"); sys.path.insert(0, S)
import gram, sinh_r8
from probes_r8 import AM, DUONG
G = gram

def lam(DANG=None, ong=None, don=None):
    DANG = DANG or G.DANG
    L = rf"{DANG}(?: {G.W})*"
    re_don = re.compile(don(L) if don else L, re.ASCII)
    re_ong = re.compile(ong(L) if ong else rf"{L}(?: \| {L})+", re.ASCII)
    def f(run, shell):
        if type(run) is not str: return "lenh_ngoai_cu_phap"
        if shell not in (None, "bash", "sh"): return "shell_ngoai_cu_phap"
        b = run[:-1] if run.endswith("\n") else run
        if re_don.fullmatch(b): return None
        if re_ong.fullmatch(b): return None if shell == "bash" else "ong_khong_bash_tuong_minh"
        return "lenh_ngoai_cu_phap"
    return f

P, W = G.P, G.W
WG = r"[A-Za-z0-9_./=:|-]+"   # W có thêm '|'
MUT = {
 "v3a_bash_P_khong_trang": lam(DANG=rf"(?:python {P}\.py|bash \S+\.sh|pwsh -NoProfile -File {P}\.ps1)"),
 "v3b_pwsh_P_khong_trang": lam(DANG=rf"(?:python {P}\.py|bash {P}\.sh|pwsh -NoProfile -File \S+\.ps1)"),
 "v3c_bash_tuy_chon_truoc_P": lam(DANG=rf"(?:python {P}\.py|bash(?: -[a-z]+)* {P}\.sh|pwsh -NoProfile -File {P}\.ps1)"),
 "v3d_python_tuy_chon_truoc_P": lam(DANG=rf"(?:python(?: -[A-Za-z]+)* {P}\.py|bash {P}\.sh|pwsh -NoProfile -File {P}\.ps1)"),
 "v3e_ong_va_cuoi": lam(ong=lambda L: rf"{L}(?: \| {L})+(?: &)?"),
 "v3f_ong_hoac_lenh_cuoi": lam(ong=lambda L: rf"{L}(?: \| {L})+(?: \|\| {L})?"),
 "v3g_ong_ve_phai_W_co_gach": lam(ong=lambda L: rf"{L}(?: \| {G.DANG}(?: {WG})*)+"),
 "v3h_ong_cham_than_ve_phai": lam(ong=lambda L: rf"{L}(?: \| (?:! )?{L})+"),
}

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
    R = os.path.join(S, "..", "..", "repo") if False else "/tmp/claude-0/-home-user-tra-luat/caf22779-10f3-5574-a917-7d9657c1fb93/scratchpad/review/r8-3-claude/repo"
    y = yaml.safe_load(subprocess.run(["git", "-C", R, "show", "fe84620:.github/workflows/ci.yml"], capture_output=True, text=True, check=True).stdout)
    out = []
    for j in y["jobs"].values():
        for st in j.get("steps", []):
            if "run" in st: out.append((st["run"], st.get("shell")))
    vlf = ["bash .github/checks/tl_selftest_bang_chung.sh\n", "bash .github/checks/release_bundle_x2.sh\n", "python ops/cong_cu_test.py\n",
           "bash ops/chay_lease_publish_test.sh\n", "pwsh -NoProfile -File scripts/don-nhanh_test.ps1\n", "bash ops/ci/gate_cgroup.sh\n"]
    return out, vlf

kho = sinh_r8.kho(); g1 = g1_cases(); ci, vlf = than_ci()
kq = {}
for ten, f in MUT.items():
    s1 = [k for k, (r, s) in AM.items() if f(r, s) != G.cu_phap_run(r, s)]
    s2 = [k for k, (r, s) in DUONG.items() if f(r, s) is not None]
    g = sum(f(r, s) is None for r, s in g1)
    a = sum(f(r, s) != G.cu_phap_run(r, s) for t in kho for s in sinh_r8.SHELL for r in (t, t + "\n"))
    c = sum(f(r, s) != G.cu_phap_run(r, s) for r, s in ci)
    v = sum(f(r, None if r.startswith("pwsh") else None) is not None for r in vlf)
    kq[ten] = {"A14_S1_doi_ly_do": len(s1), "A14_S2_hong": len(s2), "g1_nhan": g, "A14_S6a_lech": a, "ci_fe84620_lech": c, "VL-F_hong": v,
               "song_sot": not (s1 or s2 or g or a or c or v)}
    print(ten, kq[ten])
json.dump(kq, open("song_sot_v3.json", "w"), ensure_ascii=False, indent=1)
print("song_sot", sum(x["song_sot"] for x in kq.values()), "/", len(kq), "| ci than:", len(ci))
