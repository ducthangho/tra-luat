import os, sys
# T0 — trình thông dịch: quyết định chỉ chạy trong một tiến trình `python -I` (bỏ PYTHON*, site người dùng, thư mục
# script, thư mục hiện hành khỏi đường nạp). Chạy thiếu `-I` thì tự chạy lại chính tệp này với `-I`, giữ cờ gốc, TRƯỚC
# mọi import khác (`os`, `sys` đã nạp sẵn lúc khởi động, không tra sys.path).
if not sys.flags.isolated:
    if os.name != "posix" or not os.path.isfile(sys.argv[0]) or not getattr(sys, "orig_argv", None):
        sys.exit("TIỀN KIỂM: DỪNG\n  KHÔNG ĐO ĐƯỢC: phải chạy bằng `python -I <tệp>`")
    os.execv(sys.executable, [sys.executable, "-I", *sys.orig_argv[1:]])
import datetime, importlib.util, pathlib, posixpath, re, shutil, site, subprocess, sysconfig, tempfile, types, unicodedata
WS = [".claude/dev/packet_loop.py", ".claude/dev/packet_loop_test.py", "docs/PROTOCOL_DA_PHIEN.md", "docs/adr/0068-bat-bien-protocol-va-review-theo-lop.md"]
B, sau = sys.argv[1], (sys.argv[sys.argv.index("--sau-dang") + 1] if "--sau-dang" in sys.argv else None)
dung = []
def ngung(ly):
    sys.exit(f"TIỀN KIỂM: DỪNG\n  {ly}")
def trong(p, goc, f=os.path.realpath):  # vị trí trong CAM xét theo đích thật; trong TIN xét theo đường dẫn nạp
    try:
        return os.path.commonpath([f(p), f(goc)]) == f(goc)
    except ValueError:
        return False
d = os.getcwd()  # gốc clone tìm như git: thư mục gần nhất có `.git`; không thấy thì "/" (cấm hết, fail-closed)
while not os.path.exists(os.path.join(d, ".git")) and os.path.dirname(d) != d:
    d = os.path.dirname(d)
CAM = {os.getcwd(), d, os.path.dirname(os.path.realpath(__file__))}  # thêm gốc clone và thư mục chung theo git sau T1
TIN = {os.path.abspath(x) for x in [sysconfig.get_path("stdlib"), sysconfig.get_path("platstdlib"), *site.getsitepackages()] if x}
def nguon_ok(noi):
    return bool(noi) and all(x in ("built-in", "frozen") or (any(trong(x, t, os.path.abspath) for t in TIN) and not any(trong(x, c) for c in CAM)) for x in noi)
def noi_nap(sp):
    return [sp.origin] if sp is not None and sp.origin else list(getattr(sp, "submodule_search_locations", None) or [])
# T0 — chương trình git: đường dẫn tuyệt đối, ngoài clone, cwd và thư mục script; mọi lời gọi git dùng đúng tệp ấy
GIT = os.path.realpath(shutil.which("git")) if shutil.which("git") else None
if not GIT or any(trong(GIT, c) for c in CAM):
    ngung(f"KHÔNG ĐO ĐƯỢC: chương trình git {GIT!r} vắng hoặc nằm trong clone, cwd hay thư mục script")
# T0 — môi trường git: E_MANG chỉ cho `ls-remote` (người gọi, bỏ mọi GIT_* trừ nhóm vận chuyển và xác thực);
# E_CB cho MỌI lời gọi cục bộ: dựng từ rỗng, không cấu hình hệ thống và toàn cục, HOME tạm, không GIT_* nào khác
MANG = re.compile(r"GIT_(CONFIG_(COUNT|KEY_\d+|VALUE_\d+|GLOBAL|SYSTEM|NOSYSTEM)|ASKPASS|TERMINAL_PROMPT|SSH|SSH_COMMAND|SSH_VARIANT|PROXY_COMMAND|HTTP_\w+|SSL_\w+)")
E_MANG = {k: v for k, v in os.environ.items() if not k.startswith("GIT_") or MANG.fullmatch(k)}
def git(*a, vao=None, env=None):
    r = subprocess.run([GIT, *a], capture_output=True, text=True, encoding="utf-8", input=vao, env=env or E_CB)
    if r.returncode:
        ngung(f"KHÔNG ĐO ĐƯỢC: git {' '.join(a)[:80]} rc={r.returncode}: {r.stderr.strip()[:200]}")
    return r.stdout
def chuan(p):
    """§5 bước 1–4: `\\` thành `/`; từ chối tuyệt đối, `.`, `..`; NFC; casefold. Trả None nếu bị từ chối."""
    p = unicodedata.normalize("NFC", p.replace("\\", "/")).casefold()
    tho = p.rstrip("/")
    return None if not tho or tho.startswith("/") or ":" in tho.split("/")[0] or {".", ".."} & set(tho.split("/")) else p
def giao(x, y):
    """Bằng nhau, hay một bên là tiền tố THƯ MỤC của bên kia (§5: write set nhận đường dẫn và tiền tố thư mục)."""
    x, y = x.rstrip("/"), y.rstrip("/")
    return x == y or y.startswith(x + "/") or x.startswith(y + "/")
def ls_remote():
    return {tuple(d.split("\t")[::-1]) for d in git("ls-remote", "--heads", "origin", env=E_MANG).splitlines()}
with tempfile.TemporaryDirectory(prefix="tien-kiem-") as tg:
    os.mkdir(os.path.join(tg, "home"))
    E_CB = {"PATH": os.path.dirname(GIT), "HOME": os.path.join(tg, "home"), "GIT_CONFIG_NOSYSTEM": "1", "GIT_CONFIG_GLOBAL": os.devnull}
    # T1 — độ mới ref: tập cặp (tên nhánh, SHA) của máy chủ và của bộ đệm bằng nhau theo cả hai chiều (bỏ HEAD)
    mc = ls_remote()
    cb = {(r.replace("refs/remotes/origin/", "refs/heads/", 1), s) for s, r in (d.split(" ") for d in git("for-each-ref", "--format=%(objectname) %(refname)", "refs/remotes/origin").splitlines()) if r != "refs/remotes/origin/HEAD"}
    if not mc or mc != cb or git("rev-parse", "--is-shallow-repository").strip() != "false":
        ngung(f"ref chưa mới hoặc clone shallow: máy chủ có mà bộ đệm thiếu {len(mc - cb)} cặp, bộ đệm thừa {len(cb - mc)} cặp (fetch đủ nhánh rồi chạy lại)")
    CAM |= {git("rev-parse", "--show-toplevel").strip(), os.path.dirname(git("rev-parse", "--path-format=absolute", "--git-common-dir").strip())}
    if any(trong(GIT, c) for c in CAM):
        ngung(f"KHÔNG ĐO ĐƯỢC: chương trình git {GIT} nằm trong clone")
    # T5 — nguồn dữ liệu quyết định (bất biến I-NGUON): mọi byte mà T2–T4 đọc đến từ object của ảnh chụp máy chủ
    # V = mc đã xác minh ở T1, trong một kho trần TẠM mà ref duy nhất là đúng các cặp của V; B thuộc V
    ob, mm = git("rev-parse", "--verify", "--end-of-options", B).strip(), dict(mc).get("refs/heads/master")
    td = os.path.join(tg, "kho")
    git("init", "-q", "--bare", td)
    pathlib.Path(td, "objects/info/alternates").write_text(git("rev-parse", "--path-format=absolute", "--git-path", "objects").strip() + "\n", encoding="utf-8")
    git("-C", td, "update-ref", "--stdin", vao="".join(f"create {r.replace('refs/heads/', 'refs/remotes/origin/', 1)} {s}\n" for r, s in sorted(mc)))
    if {(r.replace("refs/remotes/origin/", "refs/heads/", 1), s) for s, r in (d.split(" ") for d in git("-C", td, "for-each-ref", "--format=%(objectname) %(refname)").splitlines())} != mc:
        ngung("KHÔNG ĐO ĐƯỢC: kho tạm không có đúng tập ref của ảnh chụp máy chủ")
    tt = subprocess.run([GIT, "-C", td, "merge-base", "--is-ancestor", ob, mm or "-"], capture_output=True, text=True, encoding="utf-8", env=E_CB)
    if tt.returncode:
        ngung(f"B={B} giải ra {ob}: không phải master của máy chủ trong ảnh chụp T1 hay tổ tiên của nó" if tt.returncode == 1 and mm else f"KHÔNG ĐO ĐƯỢC: merge-base B/master rc={tt.returncode}: {tt.stderr.strip()[:200]}")
    # T2 — policy change-impact: đường dẫn liên quan là mọi đường dẫn dưới `.github/coordination` có chuỗi `change-impact`
    # (gồm hai tệp §5 nêu tên). Đo trên master của V và trên MỌI commit của B..master (`-m`: cả diff của commit gộp và
# không rút gọn nhánh phụ); có ⇒ DỪNG để re-evaluate theo §5.
    # Trên B không đo riêng: B là tổ tiên của master (T5), nên policy có trên B thì hoặc còn trên master, hoặc bị đổi trong B..master.
    pol_m = sorted(p for p in git("-C", td, "ls-tree", "-r", "-z", "--name-only", mm, "--", ".github/coordination").split("\0") if "change-impact" in p)
    pol_d = sorted({p.strip("\n") for p in git("-C", td, "log", "-m", "--no-renames", "--name-only", "-z", "--format=", f"{ob}..{mm}", "--", ".github/coordination").split("\0") if "change-impact" in p})
    if pol_m:
        dung.append(f"policy change-impact có mặt trên master của ảnh chụp: {pol_m} — re-evaluate theo §5 (revision đặc tả)")
    if pol_d:
        dung.append(f"policy change-impact đổi giữa B và master của ảnh chụp: {pol_d} — re-evaluate theo §5 (revision đặc tả)")
    # T3 — liên kết tượng trưng trên B: không đường dẫn nào của write set hay thư mục cha của nó là liên kết, không liên kết nào trỏ vào write set
    cay = [d.split("\t", 1) for d in git("-C", td, "ls-tree", "-r", "-t", "-z", ob).split("\0") if d]
    lk = {p: git("-C", td, "cat-file", "-p", m.split()[2]) for m, p in cay if m.split()[0] == "120000"}
    for p, dich in lk.items():
        toi = chuan(posixpath.normpath(posixpath.join(posixpath.dirname(p), dich)))
        if any(giao(chuan(p) or p, chuan(w)) or (toi and giao(toi, chuan(w))) for w in WS):
            dung.append(f"liên kết tượng trưng chạm write set: {p} -> {dich}")
    # T4 — mọi lease CÒN HIỆU LỰC trên mọi ref của kho tạm. Mã quét nạp từ blob `<B>:ops/lease_publish.py`; PyYAML chỉ
    # được nạp sau khi vị trí của nó đã kiểm (trong stdlib hay site-packages của trình thông dịch, ngoài CAM)
    sp = importlib.util.find_spec("yaml")
    if sp is None or not nguon_ok(noi_nap(sp)):
        ngung(f"KHÔNG ĐO ĐƯỢC: PyYAML {'vắng' if sp is None else 'sẽ nạp từ ' + repr(noi_nap(sp))}; phải nằm trong stdlib hay site-packages của trình thông dịch, ngoài clone, cwd và thư mục script")
    import yaml  # noqa: F401 — nạp đúng bản vừa kiểm; scanner `import yaml` lấy lại từ sys.modules
    os.environ.clear()
    os.environ.update(E_CB)  # git mà scanner gọi cũng chạy trong E_CB
    try:
        lp = types.ModuleType("lease_publish")
        sys.modules["lease_publish"] = lp
        exec(compile(git("-C", td, "cat-file", "blob", f"{ob}:ops/lease_publish.py"), f"{ob}:ops/lease_publish.py", "exec"), lp.__dict__)
        cac = lp._quet_lease_toan_kho(pathlib.Path(td), doi_chieu_ref=False, chan_nhanh_tut_sau=True)
        bay_gio = datetime.datetime.now(datetime.timezone.utc)
        song = [m for m in cac if lp._phan_loai_lease(m["lease"], bay_gio) == "CÒN_HẠN" and lp._bia_mo_doi_xung(m["lease"], cac) is not True]
    except Exception as ex:  # thiếu hàm, YAML hỏng, ref thiếu, hạn không đọc được: đều là KHÔNG ĐO ĐƯỢC
        ngung(f"KHÔNG ĐO ĐƯỢC: quét lease toàn kho: {type(ex).__name__}: {str(ex)[:300]}")
    # T7 — mọi module đang nạp (khởi động, import bắc cầu của PyYAML và của mã quét) phải đến từ stdlib hay site-packages
    sai = [f"{t}: {noi_nap(getattr(m, '__spec__', None))}" for t, m in list(sys.modules.items()) if t not in ("__main__", "lease_publish") and not nguon_ok(noi_nap(getattr(m, "__spec__", None)))]
    if sai:
        ngung(f"KHÔNG ĐO ĐƯỢC: module nạp ngoài stdlib/site-packages hay trong clone, cwd, thư mục script: {sai[:5]}")
    # T6 — ảnh chụp V còn đúng ở cuối phép đo: máy chủ hỏi lại phải trả đúng tập cặp của T1
    if ls_remote() != mc:
        ngung("máy chủ đổi trong lúc đo (ls-remote cuối khác ảnh chụp T1): làm mới ref rồi chạy lại")
giu = set()
for m in song:
    l, lid = m["lease"], lp._lease_id_quet(m["lease"].get("lease_id"))
    ws, ews = l.get("write_set"), l.get("effective_write_set")
    if lid is None or not isinstance(ws, list) or not isinstance(ews, (list, type(None))) or any(not isinstance(x, str) for x in ws + (ews or [])):
        dung.append(f"lease không đọc được write set: {m['ref']}:{m['path']}")
        continue
    muc = ws + (ews or [])
    for x in muc:
        cx = chuan(x.strip().removeprefix("planned:"))
        if cx is None:
            dung.append(f"đường dẫn bị §5 từ chối trong lease {lid}: {x!r}")
        elif any(giao(cx, chuan(w)) for w in WS) and lid != sau:
            giu.add(lid)
if giu:
    dung.append(f"lease còn hiệu lực giao write set wp1466: {sorted(giu)}")
if sau and not any(lp._lease_id_quet(m["lease"].get("lease_id")) == sau for m in song):
    dung.append(f"--sau-dang {sau}: không thấy lease ấy còn hiệu lực trên ref nào")
print(f"base {B} = {ob[:12]} · master V = {(mm or '-')[:12]} · {len(mc)} nhánh máy chủ = {len(mc)} ref kho tạm · {len(cac)} bản ghi lease · {len(song)} còn hiệu lực · {len(lk)} liên kết tượng trưng · policy {len(pol_m)}+{len(pol_d)} · {len(sys.modules)} module")
print("TIỀN KIỂM: ĐẠT" if not dung else "TIỀN KIỂM: DỪNG\n  " + "\n  ".join(dung))
sys.exit(1 if dung else 0)
