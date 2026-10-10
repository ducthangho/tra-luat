"""B4: ước lượng TĨNH (cận dưới) số mục DOT_BIEN không đo được trên Windows: ca trả chuỗi ở đầu thân dưới
`if LA_WINDOWS` / `os.name == 'nt'` / `platform.system() != 'Linux'` (hay == 'Windows'), cộng mục mang giới hạn
('posix', …). Dùng: python3 -B san_windows.py <launcher_test.py>"""
import ast, sys, importlib.util
from pathlib import Path
p = Path(sys.argv[1]); src = p.read_text(encoding="utf-8"); cay = ast.parse(src)
def la_dieu_kien(t):
    s = ast.unparse(t)
    return ("LA_WINDOWS" in s and "not LA_WINDOWS" not in s) or "os.name == 'nt'" in s or \
        "platform.system() != 'Linux'" in s or "platform.system() == 'Windows'" in s
bo = set()
for n in cay.body:
    if isinstance(n, ast.FunctionDef) and n.name.startswith("t"):
        than = n.body[1:] if n.body and isinstance(n.body[0], ast.Expr) and isinstance(getattr(n.body[0], "value", None), ast.Constant) else n.body
        for st in than[:3]:
            if isinstance(st, ast.If) and la_dieu_kien(st.test) and any(
                    isinstance(x, ast.Return) and isinstance(x.value, (ast.Constant, ast.JoinedStr)) for x in st.body):
                bo.add(n.name); break
sys.argv = ["x"]
sp = importlib.util.spec_from_file_location("lt_san", p); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m)
kd = 0
for muc in m.DOT_BIEN:
    gh = muc[3] if len(muc) > 3 else None
    if (gh and gh[0] == "posix") or all(t in bo for t in muc[2]):
        kd += 1
for muc in m.DOT_BIEN_HARNESS:
    gh = muc[3] if len(muc) > 3 else None
    if (gh and gh[0] == "posix") or all(t in bo for t in muc[2]):
        kd += 1
tong = len(m.DOT_BIEN) + len(m.DOT_BIEN_HARNESS)
print(f"ca bo qua tinh tren Windows: {len(bo)}; muc khong do duoc: {kd}/{tong}; do duoc {100*(tong-kd)/tong:.2f}%; "
      f"_dot_bien_du_san={m._dot_bien_du_san(tong, kd)}; bien={max(k for k in range(0, tong) if m._dot_bien_du_san(tong, k)) - kd}")
