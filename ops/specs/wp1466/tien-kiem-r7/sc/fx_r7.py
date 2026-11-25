"""Răng của khối `tien-kiem` r7 cho danh sách cho phép đóng của đầu vào (F11.e, F11.f và các đầu vào người soạn tự liệt kê).

Dùng: /usr/bin/python3 -B fx_r7.py <thư mục r7> <tệp ops/lease_publish.py của master> [<tệp khối thay cho sc/tien_kiem.py>]
Mượn các hàm dựng kho của fx_tien_kiem.py (r6, không sửa). Mỗi kịch bản đòi rc, một chuỗi lý do, và với các
kịch bản Python hay git, đòi tệp đánh dấu KHÔNG được tạo (mã ngoài danh sách cho phép không được chạy).
"""
import ast, datetime, os, pathlib, py_compile, shutil, subprocess, sys
S, LP = pathlib.Path(sys.argv[1]).resolve(), str(pathlib.Path(sys.argv[2]).resolve())
TK = pathlib.Path(sys.argv[3]).resolve() if len(sys.argv) > 3 else S / "sc/tien_kiem.py"
src = (S / "sc/fx_tien_kiem.py").read_text(encoding="utf-8")
stop = next(n.lineno for n in ast.parse(src).body if isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "KB" for t in n.targets))
sys.argv = ["fx", str(S), LP, str(TK)]
h = {}
exec(compile("\n".join(src.splitlines()[:stop - 1]), "fx_tien_kiem_helpers", "exec"), h)
FX = h["FX"] = S / "tmp/fx7"
FX.mkdir(parents=True, exist_ok=True)
g, dung, lease, L, P1, A, ENV, dang_rieng = h["g"], h["dung"], h["lease"], h["L"], h["P1"], h["A"], h["ENV"], h["dang_rieng"]
REALGIT = shutil.which("git")
POL, SCH = ".github/coordination/change-impact.v1.json", ".github/coordination/schemas/change-impact.v1.schema.json"
W = "wp1466-r6-g1-claude"
import yaml as _y
YAML_DIR = pathlib.Path(_y.__file__).parent

def chay(k, B="origin/master", sau=None, py=sys.executable, flags=("-B",), env=None, cwd=None, script=None):
    lenh = [py, *flags, str(script or TK), B] + (["--sau-dang", sau] if sau else [])
    r = subprocess.run(lenh, cwd=cwd or k, capture_output=True, text=True, env=env or ENV)
    return r.returncode, (r.stdout + r.stderr).strip().splitlines()
def commit_push(k, msg):
    g(k, "add", "-A"); g(k, "commit", "-q", "-m", msg); g(k, "push", "-q", "origin", "master"); g(k, "fetch", "-q", "origin", "+refs/heads/*:refs/remotes/origin/*")
def ghi(k, p, nd="{}\n"):
    (k / p).parent.mkdir(parents=True, exist_ok=True); (k / p).write_text(nd, encoding="utf-8")
def yaml_danh_dau(dich, dau):
    shutil.copytree(YAML_DIR, dich, ignore=shutil.ignore_patterns("__pycache__"))
    p = dich / "__init__.py"; p.write_text(f"open({str(dau)!r}, 'w').close()\n" + p.read_text(encoding="utf-8"), encoding="utf-8")
def venv(noi, he_thong=True):
    if not noi.exists():
        subprocess.run(["/usr/bin/python3", "-m", "venv", *(["--system-site-packages"] if he_thong else []), str(noi)], check=True)
    sp = subprocess.run([str(noi / "bin/python"), "-I", "-c", "import site;print(site.getsitepackages()[0])"], capture_output=True, text=True, check=True).stdout.strip()
    return noi / "bin/python", pathlib.Path(sp)
def kho(ten, **kw):
    rc, out = dung(ten, **kw)
    return FX / ten / "kho", rc, out

# ---- F11.e: policy change-impact phải đo trên master của V và trên B..master (T2) ----
def them_sau_B(p, dang=False):
    def f(k):
        cu = g(k, "rev-parse", "master").strip()
        if dang:
            dang_rieng(k)
        ghi(k, p); commit_push(k, "policy moi")
        return cu
    return f
def xoa_sau_B(k):
    cu = g(k, "rev-parse", "master").strip(); g(k, "rm", "-q", POL); commit_push(k, "bo policy"); return cu
def them_roi_xoa(k):
    cu = g(k, "rev-parse", "master").strip(); ghi(k, POL); commit_push(k, "them"); g(k, "rm", "-q", POL); commit_push(k, "xoa"); return cu
def nhanh_phu_merge(k):
    cu = g(k, "rev-parse", "master").strip()
    g(k, "checkout", "-q", "-b", "phu"); ghi(k, POL); g(k, "add", "-A"); g(k, "commit", "-q", "-m", "them")
    g(k, "rm", "-q", POL); g(k, "commit", "-q", "-m", "xoa"); g(k, "checkout", "-q", "master")
    g(k, "merge", "-q", "--no-ff", "-m", "gop", "phu"); g(k, "branch", "-q", "-D", "phu")
    g(k, "push", "-q", "origin", "master"); g(k, "fetch", "-q", "origin", "+refs/heads/*:refs/remotes/origin/*")
    return cu
def gop_xoa(k):
    """Commit gộp tự xoá policy (thay đổi chỉ thấy trong diff của commit gộp)."""
    cu = g(k, "rev-parse", "master").strip()
    g(k, "checkout", "-q", "-b", "phu"); ghi(k, "notes.txt", "x\n"); g(k, "add", "-A"); g(k, "commit", "-q", "-m", "phu"); g(k, "checkout", "-q", "master")
    g(k, "merge", "-q", "--no-ff", "--no-commit", "phu"); g(k, "rm", "-q", POL); g(k, "commit", "-q", "-m", "gop xoa policy"); g(k, "branch", "-q", "-D", "phu")
    g(k, "push", "-q", "origin", "master"); g(k, "fetch", "-q", "origin", "+refs/heads/*:refs/remotes/origin/*")
    return cu
def khong_lien_quan(dang):
    def f(k):
        cu = g(k, "rev-parse", "master").strip()
        if dang:
            dang_rieng(k)
        ghi(k, "notes.txt", "ghi chu\n"); ghi(k, "docs/change-impact-ghi-chu.md", "x\n"); ghi(k, ".github/workflows/change-impact.yml", "x: 1\n"); commit_push(k, "khong lien quan")
        return cu
    return f

KQ = []
def ghi_kq(ten, rc, out, doi_rc, chuoi=None, khong_chuoi=None, dau=None, ghi_chu=""):
    van = "\n".join(out)
    ok = rc == doi_rc and (chuoi is None or chuoi in van) and (khong_chuoi is None or khong_chuoi not in van) and (dau is None or not dau.exists())
    KQ.append(ok)
    ly = next((d.strip() for d in out if d.startswith("  ")), out[-1] if out else "")
    print(f"{'OK ' if ok else 'SAI'} {ten:38s} rc={rc} (đòi {doi_rc}){' đánh dấu=' + ('CÓ' if dau.exists() else 'không') if dau else ''} {ly[:120]} {ghi_chu}", flush=True)

print("BAT_DAU", datetime.datetime.now(datetime.timezone.utc).strftime("%FT%TZ"), "python", sys.executable, flush=True)
for ten, kw, doi_rc, chuoi, khong in [
    ("e_policy_them_sau_B", dict(them=them_sau_B(POL)), 1, "policy change-impact", None),
    ("e_policy_them_sau_B_sau_dang", dict(them=them_sau_B(POL, True), sau=W), 1, "policy change-impact", None),
    ("e_schema_them_sau_B_sau_dang", dict(them=them_sau_B(SCH, True), sau=W), 1, "policy change-impact", None),
    ("e_policy_xoa_sau_B", dict(master_them=[(POL, "{}\n")], them=xoa_sau_B), 1, "đổi giữa B và master", "có mặt trên master"),
    ("e_policy_them_roi_xoa_sau_B", dict(them=them_roi_xoa), 1, "đổi giữa B và master", "có mặt trên master"),
    ("e_policy_qua_nhanh_phu_merge", dict(them=nhanh_phu_merge), 1, "đổi giữa B và master", "có mặt trên master"),
    ("e_policy_xoa_trong_commit_gop", dict(master_them=[(POL, "{}\n")], them=gop_xoa), 1, "đổi giữa B và master", "có mặt trên master"),
    ("e_khong_lien_quan_sau_B", dict(them=khong_lien_quan(False)), 0, "TIỀN KIỂM: ĐẠT", None),
    ("e_khong_lien_quan_sau_dang", dict(them=khong_lien_quan(True), sau=W), 0, "TIỀN KIỂM: ĐẠT", None),
]:
    k, rc, out = kho(ten, **kw)
    ghi_kq(ten, rc, out, doi_rc, chuoi, khong)

# ---- F11.f: đường nạp Python (T0 tự chạy lại với -I; T4 kiểm vị trí PyYAML TRƯỚC khi nạp; T7 kiểm mọi module) ----
nen = dict(ENV, PYTHONNOUSERSITE="1")  # chỉ để PyYAML ở site người dùng của máy đo không lẫn vào kịch bản (mục 18)
k, rc, out = kho("f_khong_I_pythonpath_clone")
dau = FX / "f_khong_I_pythonpath_clone/DAU"; yaml_danh_dau(k / "yaml", dau)
rc, out = chay(k, env=dict(nen, PYTHONPATH=str(k))); ghi_kq("f_khong_I_pythonpath_clone", rc, out, 0, "TIỀN KIỂM: ĐẠT", None, dau)
k, rc, out = kho("f_khong_I_script_trong_clone")
dau = FX / "f_khong_I_script_trong_clone/DAU"; yaml_danh_dau(k / "yaml", dau); shutil.copyfile(TK, k / "tk.py")
rc, out = chay(k, env=nen, script=k / "tk.py"); ghi_kq("f_khong_I_script_trong_clone", rc, out, 0, "TIỀN KIỂM: ĐẠT", None, dau)
k, rc, out = kho("f_khong_I_pyc_khong_nguon")
dau = FX / "f_khong_I_pyc_khong_nguon/DAU"; yaml_danh_dau(k / "yaml", dau); shutil.copyfile(TK, k / "tk.py")
py_compile.compile(str(k / "yaml/__init__.py"), cfile=str(k / "yaml/__init__.pyc"), doraise=True); (k / "yaml/__init__.py").unlink()
rc, out = chay(k, env=nen, script=k / "tk.py"); ghi_kq("f_khong_I_pyc_khong_nguon", rc, out, 0, "TIỀN KIỂM: ĐẠT", None, dau)
for ten, yaml_clone, nhap_mod, doi_rc, chuoi in [
    ("f_pth_yaml_trong_clone", True, False, 1, "PyYAML sẽ nạp từ"),
    ("f_pth_import_module_clone", False, True, 1, "module nạp ngoài"),
    ("f_pth_chi_duong_dan", False, False, 0, "TIỀN KIỂM: ĐẠT"),
]:
    k, rc, out = kho(ten)
    py, sp = venv(FX / ten / "venv")
    dau = FX / ten / "DAU"
    if yaml_clone:
        yaml_danh_dau(k / "yaml", dau)
    if nhap_mod:
        (k / "tk_probe_r7.py").write_text("X = 1\n")
    (sp / "zz_tk_r7.pth").write_text(str(k) + "\n" + ("import tk_probe_r7\n" if nhap_mod else ""))
    rc, out = chay(k, py=str(py), flags=("-I", "-B"))
    ghi_kq(ten, rc, out, doi_rc, chuoi, None, dau if yaml_clone else None)
k, rc, out = kho("f_thieu_pyyaml")
py, sp = venv(FX / "f_thieu_pyyaml/venv", he_thong=False)
rc, out = chay(k, py=str(py), flags=("-I", "-B")); ghi_kq("f_thieu_pyyaml", rc, out, 1, "PyYAML vắng")

# ---- chương trình git (T0 trước T1 và lại sau T1) ----
def bo_boc(noi, dau):
    noi.mkdir(parents=True, exist_ok=True)
    (noi / "git").write_text(f"#!/bin/sh\n: > {str(dau)!r}\nexec {REALGIT} \"$@\"\n"); (noi / "git").chmod(0o755)
k, rc, out = kho("g_git_trong_clone")
dau = FX / "g_git_trong_clone/DAU"; bo_boc(k / ".bin", dau)
rc, out = chay(k, env=dict(ENV, PATH=f"{k / '.bin'}:{ENV['PATH']}")); ghi_kq("g_git_trong_clone", rc, out, 1, "chương trình git", None, dau)
k, rc, out = kho("g_git_cay_chinh_tu_worktree_phu")
wt = FX / "g_git_cay_chinh_tu_worktree_phu/wt"; g(k, "worktree", "add", "-q", "--detach", str(wt), "master")
dau = FX / "g_git_cay_chinh_tu_worktree_phu/DAU"; bo_boc(k / ".bin", dau)
rc, out = chay(k, cwd=wt, env=dict(ENV, PATH=f"{k / '.bin'}:{ENV['PATH']}")); ghi_kq("g_git_cay_chinh_tu_worktree_phu", rc, out, 1, "nằm trong clone", None, None, "(git ngoài cwd chạy ở T1 rồi mới bị chặn: mục 18)")

# ---- môi trường git: GIT_* của người gọi và grafts của clone không tới kho tạm ----
def mo_coi(k):
    """Commit mồ côi CHƯA CÔNG BỐ, ops/lease_publish.py sửa cho mọi bia mộ là hai chiều; trả OID."""
    g(k, "checkout", "-q", "--detach", "master")
    p = k / "ops/lease_publish.py"; s = p.read_text(encoding="utf-8")
    dau = "def _bia_mo_doi_xung(lease: dict, cac_lease: list[dict]) -> bool | None:\n"
    p.write_text(s.replace(dau, dau + "    return True\n"), encoding="utf-8"); g(k, "add", "-A")
    x = g(k, "commit-tree", g(k, "write-tree").strip(), "-m", "mo coi").strip()
    g(k, "checkout", "-q", "-f", "master")
    return x
GIU = [("ops/a", [(L + "a.yaml", lease(A, [P1]))])]
k, rc, out = kho("v_graft_qua_bien_moi_truong", nhanh=GIU)
x = mo_coi(k); gf = FX / "v_graft_qua_bien_moi_truong/grafts"; gf.write_text(g(k, "rev-parse", "origin/master").strip() + " " + x + "\n")
rc, out = chay(k, B=x, env=dict(ENV, GIT_GRAFT_FILE=str(gf))); ghi_kq("v_graft_qua_bien_moi_truong", rc, out, 1, "không phải master", None)
k, rc, out = kho("v_graft_trong_clone", nhanh=GIU)
x = mo_coi(k); (k / ".git/info").mkdir(exist_ok=True); (k / ".git/info/grafts").write_text(g(k, "rev-parse", "origin/master").strip() + " " + x + "\n")
rc, out = chay(k, B=x); ghi_kq("v_graft_trong_clone", rc, out, 1, "không phải master", None)

# ---- T6: máy chủ đổi giữa lần hỏi T1 và lần hỏi cuối ----
k, rc, out = kho("t6_may_chu_doi_trong_luc_do")
goc = FX / "t6_may_chu_doi_trong_luc_do"; arm, dem = goc / "ARM", goc / "DEM"
up = goc / "up.sh"
up.write_text(f"""#!/bin/sh
if [ -f {str(arm)!r} ]; then
  n=$(cat {str(dem)!r} 2>/dev/null || echo 0); n=$((n+1)); echo $n > {str(dem)!r}
  if [ "$n" -eq 2 ]; then
    O={str(goc / 'origin.git')!r}
    T=$(env -u GIT_DIR {REALGIT} --git-dir="$O" rev-parse refs/heads/master^{{tree}})
    C=$(echo moi | env -u GIT_DIR GIT_AUTHOR_NAME=fx GIT_AUTHOR_EMAIL=fx@example.invalid GIT_COMMITTER_NAME=fx GIT_COMMITTER_EMAIL=fx@example.invalid {REALGIT} --git-dir="$O" commit-tree "$T" -p refs/heads/master)
    env -u GIT_DIR {REALGIT} --git-dir="$O" update-ref refs/heads/master "$C"
  fi
fi
exec {REALGIT} upload-pack "$@"
"""); up.chmod(0o755)
g(k, "config", "remote.origin.uploadpack", str(up)); arm.write_text("")
rc, out = chay(k); arm.unlink()
ghi_kq("t6_may_chu_doi_trong_luc_do", rc, out, 1, "máy chủ đổi trong lúc đo", None, None, f"(số lần hỏi máy chủ: {dem.read_text().strip() if dem.exists() else 0})")

print(f"TONG {len(KQ)} kịch bản r7: đúng {sum(KQ)} · sai {len(KQ) - sum(KQ)}")
print("KET_THUC", datetime.datetime.now(datetime.timezone.utc).strftime("%FT%TZ"))
sys.exit(0 if all(KQ) else 1)
