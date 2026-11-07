"""Reviewer Claude vòng 5: đề xuất siết vế (3)/(4) của A14-S0 — so ast trên NGUỒN CỦA CHÍNH ĐỐI TƯỢNG đang gắn tên (inspect.getsource),
đòi decorator rỗng, không closure/defaults, builtins chuẩn. Đo trên các biến thể của thu_s0.py: biến thể A_* phải ĐỎ (trừ A_defaults_ham
vô hại về kết quả nhưng vẫn đổi đối tượng), B_* (trừ chú thích tham số) phải ĐẠT. Nạp module từ TỆP thật để inspect đọc được nguồn."""
import ast, builtins, importlib.util, inspect, json, os, sys, tempfile, pathlib
D = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, D); sys.path.insert(0, os.path.join(D, "soan"))
import khoa_ast_r8 as K
from thu_s0 import BIEN

def dump(nguon):
    f = ast.parse(nguon).body[0]
    if not isinstance(f, ast.FunctionDef) or f.decorator_list:
        return "decorator_hoac_khong_phai_def"
    than = f.body[1:] if isinstance(f.body[0], ast.Expr) and isinstance(f.body[0].value, ast.Constant) and isinstance(f.body[0].value.value, str) else f.body
    f.body, f.returns = than, None
    return ast.dump(f, include_attributes=False)

def kiem_de_xuat(src):
    loi = []
    with tempfile.TemporaryDirectory() as d:
        p = pathlib.Path(d) / "mod_thu.py"; p.write_text(src)
        spec = importlib.util.spec_from_file_location("mod_thu", p); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
        f = m.cu_phap_run
        loi += ["globals"] * (getattr(f, "__globals__", None) is not vars(m))
        loi += ["builtins"] * (getattr(f, "__builtins__", None) is not vars(builtins))
        loi += ["closure_defaults"] * any(getattr(f, a, None) is not None for a in ("__closure__", "__defaults__", "__kwdefaults__"))
        try:
            loi += ["ast_doi_tuong"] * (dump(inspect.getsource(f).lstrip()) != dump(K.THAM_CHIEU.lstrip()))
        except (OSError, TypeError) as e:
            loi.append(f"khong_lay_nguon:{type(e).__name__}")
    return loi

kq = {}
for ten, (src, _) in BIEN.items():
    kq[ten] = kiem_de_xuat(src); print(f"{ten:28} {kq[ten] or 'DAT'}")
for ten in ("goc", "dinh_dang_chu_thich"):
    kq[ten] = kiem_de_xuat(K.BIEN_THE[ten][0]); print(f"{ten:28} {kq[ten] or 'DAT'}")
json.dump(kq, open(os.path.join(D, "thu_de_xuat.json"), "w"), ensure_ascii=False, indent=1)
