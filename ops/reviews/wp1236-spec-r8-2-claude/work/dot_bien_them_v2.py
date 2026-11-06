"""Đột biến bổ sung của reviewer Claude r8 vòng 2 — chạy trên bản sao trong work/soan. Đo: đột biến có làm vế âm nào ĐỔI lý do,
vế dương nào hỏng không; và nếu đột biến nhận một thân mới (dựng từ lệnh vô hại), Bash thật cho rc gì."""
import os, re, sys, json
sys.path.insert(0, os.getcwd())
import gram
from probes_r8 import AM, DUONG, chay
from dot_bien_r8 import dung
P, W = gram.P, gram.W
LENH = rf"(?:python {P}\.py|bash {P}\.sh|pwsh -NoProfile -File {P}\.ps1)(?: {W})*"

def tu_dung(don_re=None, ong_re=None):
    don = re.compile(don_re or LENH, re.ASCII); ong = re.compile(ong_re or rf"{LENH}(?: \| {LENH})+", re.ASCII)
    def f(run, shell):
        if type(run) is not str: return "lenh_ngoai_cu_phap"
        if shell not in (None, "bash", "sh"): return "shell_ngoai_cu_phap"
        b = run[:-1] if run.endswith("\n") else run
        if don.fullmatch(b): return None
        if ong.fullmatch(b): return None if shell == "bash" else "ong_khong_bash_tuong_minh"
        return "lenh_ngoai_cu_phap"
    return f

X = "python ops/hong_test.py"; Y = "python ops/qua.py"
DB = {
 "y1_ong_sep_hai_gach": (dung(ong_sep=r" \|\|? "), (f"{X} || {Y}\n", "bash")),
 "y1b_ong_sep_gach_cong": (dung(ong_sep=r" \|+ "), (f"{X} || {Y}\n", "bash")),
 "y2_ong_sep_va_nen": (dung(ong_sep=r" [|&] "), (f"{X} & {Y}\n", "bash")),
 "y3_ong_sep_cham_phay": (dung(ong_sep=r" [|;] "), (f"{X} ; {Y}\n", "bash")),
 "y3b_ong_sep_va_va": (dung(ong_sep=r" (?:\||&&) "), (f"{X} && {Y}\n", "bash")),
 "y4_don_nhan_nen_cuoi": (tu_dung(don_re=rf"{LENH}(?: &)?"), (f"{X} &\n", None)),
 "y5_don_nhan_phu_dinh": (tu_dung(don_re=rf"(?:! )?{LENH}"), (f"! {X}\n", None)),
 "y6_don_hoac_lenh": (tu_dung(don_re=rf"{LENH}(?: \|\| {LENH})*"), (f"{X} || {Y}\n", None)),
}
for c in ";&|!(){}$`'\"\\<>#*?[]~+,@%^=:":
    Pm = r"[A-Za-z0-9_.][A-Za-z0-9_./" + re.escape(c) + "-]*"
    DB[f"yP[{c}]"] = (dung(P=Pm), None)
kq = []
for ten, (f, moi) in DB.items():
    doi = [k for k, (r, s) in AM.items() if f(r, s) != gram.cu_phap_run(r, s)]
    dh = [k for k, (r, s) in DUONG.items() if f(r, s) is not None]
    dong = {"dot_bien": ten, "ve_am_doi_ly_do": doi, "ve_duong_hong": dh}
    if moi:
        r, s = moi; dong["than_moi"] = r; dong["shell"] = s; dong["grammar_goc"] = gram.cu_phap_run(r, s); dong["dot_bien_nhan"] = f(r, s)
        dong["rc_bash"], dong["da_chay"] = chay(r, s)
    kq.append(dong)
    print(json.dumps(dong, ensure_ascii=False))
