"""Reviewer Claude vòng 5: thử A14-S0 (khoa_ast_r8.kiem_s0 = thuật toán ĐÃ ĐO của phiên soạn) với các biến thể KHÔNG có trong BIEN_THE.
Hai nhóm: (A) biến thể ĐỔI hành vi — nếu kiem_s0 ĐẠT thì là lỗ; (B) biến thể HỢP LỆ về hành vi — nếu kiem_s0 ĐỎ thì là chặn oan.
Mỗi biến thể còn được đo HÀNH VI: so cu_phap_run của module với gram.cu_phap_run trên 112 vế âm + 7 vế dương + vài thân tự chọn.
Kèm cài đặt vế (4) theo VĂN BẢN đặc tả (ast.dump nguyên FunctionDef, chỉ bỏ docstring) để so hai cách đọc.
Chạy: python3 -I thu_s0.py (cwd = work/v5)."""
import ast, json, os, re, sys
D = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(D, "soan"))
import khoa_ast_r8 as K
import gram, probes_r8 as PR

GOC = K.GOC
def them_sau_ham(src, them):
    return src + "\n\n" + them + "\n"

BIEN = {
    # ---- (A) đổi hành vi ----
    "A_decorator_removesuffix": (GOC.replace("def cu_phap_run(run, shell):",
        "def _boc(f):\n    def cu_phap_run(run, shell):\n        if run.__class__ is ''.__class__:\n            run = run.removesuffix(' || exit 0')\n"
        "        return f(run, shell)\n    return cu_phap_run\n\n\n@_boc\ndef cu_phap_run(run, shell):"), True),
    "A_gan_lai_ten": (them_sau_ham(GOC, "def _khac(run, shell):\n    return None\n\n\ncu_phap_run = _khac"), True),
    "A_hai_def": (them_sau_ham(GOC, "def cu_phap_run(run, shell):\n    return None"), True),
    "A_doi_code": (them_sau_ham(GOC, "def _khac(run, shell):\n    return None\n\n\ncu_phap_run.__code__ = _khac.__code__"), True),
    "A_builtins": (GOC.replace("def cu_phap_run(run, shell):",
        "import builtins as _bi\n__builtins__ = dict(vars(_bi), str=bytes)\n\n\ndef cu_phap_run(run, shell):"), True),
    "A_boc_gan_lai_tinh_vi": (them_sau_ham(GOC, "_goc = cu_phap_run\n\n\ndef _boc(run, shell):\n    return _goc(run.removesuffix(' || exit 0') if run.__class__ is ''.__class__ else run, shell)\n\n\ncu_phap_run = _boc"), True),
    "A_defaults_ham": (them_sau_ham(GOC, "cu_phap_run.__defaults__ = (None,)"), False),   # vô hại: chỉ thêm mặc định, không đổi kết quả với 2 đối số
    # ---- (B) hợp lệ về hành vi ----
    "B_return_annotation": (GOC.replace("def cu_phap_run(run, shell):", "def cu_phap_run(run, shell) -> str | None:"), False),
    "B_param_annotation": (GOC.replace("def cu_phap_run(run, shell):", "def cu_phap_run(run: object, shell: object) -> str | None:"), False),
    "B_future_annotations": ("from __future__ import annotations\n" + GOC, False),
    "B_nhay_don_ngoac": (GOC.replace('return "lenh_ngoai_cu_phap"\n    if shell', "return ('lenh_ngoai_cu_phap')\n    if shell"), False),
    "B_type_trong_ham_khac": (them_sau_ham(GOC, "def _ham_khac(x):\n    type = 1\n    return type"), False),
}


def dump_van_ban(nguon, ten="cu_phap_run"):
    """Vế (4) theo VĂN BẢN đặc tả: ast.dump(include_attributes=False) của `def cu_phap_run`, chỉ bỏ docstring (giữ decorator, returns)."""
    f = next(n for n in ast.walk(ast.parse(nguon)) if isinstance(n, ast.FunctionDef) and n.name == ten)
    if f.body and isinstance(f.body[0], ast.Expr) and isinstance(f.body[0].value, ast.Constant) and isinstance(f.body[0].value.value, str):
        f.body = f.body[1:]
    return ast.dump(f, include_attributes=False)


THEM = ["python ops/hong_test.py || exit 0", "python ops/hong_test.py || exit 0\n", "python ops/a.py"]
def hanh_vi(nguon):
    ns = {"__name__": "m"}
    exec(compile(nguon, "m", "exec"), ns)
    f = ns["cu_phap_run"]
    vao = [(r, s) for r, s in PR.AM.values()] + [(r, s) for r, s in PR.DUONG.values()] + [(t, sh) for t in THEM for sh in (None, "bash", "sh")]
    lech = [(r, s, f(r, s), gram.cu_phap_run(r, s)) for r, s in vao if f(r, s) != gram.cu_phap_run(r, s)]
    return len(vao), lech


if __name__ == "__main__":
    kq = {}
    for ten, (src, doi_hanh_vi_ky_vong) in BIEN.items():
        s0 = K.kiem_s0(src)
        vb = dump_van_ban(src) == dump_van_ban(K.THAM_CHIEU)
        n, lech = hanh_vi(src)
        kq[ten] = {"kiem_s0_script": s0 or "DAT", "ve4_van_ban": "DAT" if vb else "DO", "hanh_vi_lech": len(lech), "vao": n,
                   "vi_du_lech": [repr(x) for x in lech[:2]]}
        print(f"{ten:28} script={'DAT' if not s0 else s0} ve4_vb={'DAT' if vb else 'DO'} lech={len(lech)}/{n} {[repr(x) for x in lech[:1]]}")
    json.dump(kq, open(os.path.join(D, "thu_s0.json"), "w"), ensure_ascii=False, indent=1)
