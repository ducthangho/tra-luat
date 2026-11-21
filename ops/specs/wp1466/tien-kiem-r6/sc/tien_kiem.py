import datetime, pathlib, posixpath, subprocess, sys, tempfile, types, unicodedata
WS = [".claude/dev/packet_loop.py", ".claude/dev/packet_loop_test.py", "docs/PROTOCOL_DA_PHIEN.md", "docs/adr/0068-bat-bien-protocol-va-review-theo-lop.md"]
B, sau = sys.argv[1], (sys.argv[sys.argv.index("--sau-dang") + 1] if "--sau-dang" in sys.argv else None)
dung = []
def git(*a, vao=None):
    r = subprocess.run(["git", *a], capture_output=True, text=True, encoding="utf-8", input=vao)
    if r.returncode:
        sys.exit(f"TIỀN KIỂM: DỪNG\n  KHÔNG ĐO ĐƯỢC: git {' '.join(a)[:80]} rc={r.returncode}: {r.stderr.strip()[:200]}")
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
# T1 — độ mới ref: tập cặp (tên nhánh, SHA) của máy chủ và của bộ đệm bằng nhau theo cả hai chiều (bỏ HEAD)
mc = {tuple(d.split("\t")[::-1]) for d in git("ls-remote", "--heads", "origin").splitlines()}
cb = {(r.replace("refs/remotes/origin/", "refs/heads/", 1), s) for s, r in (d.split(" ") for d in git("for-each-ref", "--format=%(objectname) %(refname)", "refs/remotes/origin").splitlines()) if r != "refs/remotes/origin/HEAD"}
if not mc or mc != cb or git("rev-parse", "--is-shallow-repository").strip() != "false":
    sys.exit(f"TIỀN KIỂM: DỪNG\n  ref chưa mới hoặc clone shallow: máy chủ có mà bộ đệm thiếu {len(mc - cb)} cặp, bộ đệm thừa {len(cb - mc)} cặp (fetch đủ nhánh rồi chạy lại)")
# T5 — nguồn dữ liệu quyết định (bất biến I-NGUON, cùng một bất biến cho 3d và 3e): mọi byte mà T2–T4 đọc đến từ
# object của ảnh chụp máy chủ V = mc đã xác minh ở T1. B phải là `master` của V hay tổ tiên của nó. T2–T4 chạy trong
# một kho trần TẠM mà ref duy nhất là đúng các cặp của V (object mượn qua alternates); mã quét lease nạp từ blob
# `<B>:ops/lease_publish.py`, không từ cây làm việc. Nhánh cục bộ, remote khác, tag, ref origin thừa, packed-refs,
# replace ref và tệp `.py`/`.pyc` của cây làm việc vì thế không tới được quyết định.
ob, mm = git("rev-parse", "--verify", "--end-of-options", B).strip(), dict(mc).get("refs/heads/master")
url, od = git("config", "--get", "remote.origin.url").strip(), git("rev-parse", "--path-format=absolute", "--git-path", "objects").strip()
with tempfile.TemporaryDirectory(prefix="tien-kiem-") as td:
    git("init", "-q", "--bare", td)
    pathlib.Path(td, "objects/info/alternates").write_text(od + "\n", encoding="utf-8")
    git("-C", td, "remote", "add", "origin", url)
    git("-C", td, "update-ref", "--stdin", vao="".join(f"create {r.replace('refs/heads/', 'refs/remotes/origin/', 1)} {s}\n" for r, s in sorted(mc)))
    if {(r.replace("refs/remotes/origin/", "refs/heads/", 1), s) for s, r in (d.split(" ") for d in git("-C", td, "for-each-ref", "--format=%(objectname) %(refname)").splitlines())} != mc:
        sys.exit("TIỀN KIỂM: DỪNG\n  KHÔNG ĐO ĐƯỢC: kho tạm không có đúng tập ref của ảnh chụp máy chủ")
    tt = subprocess.run(["git", "-C", td, "merge-base", "--is-ancestor", ob, mm or "-"], capture_output=True, text=True, encoding="utf-8")
    if tt.returncode:
        sys.exit(f"TIỀN KIỂM: DỪNG\n  " + (f"B={B} giải ra {ob}: không phải master của máy chủ trong ảnh chụp T1 hay tổ tiên của nó" if tt.returncode == 1 and mm else f"KHÔNG ĐO ĐƯỢC: merge-base B/master rc={tt.returncode}: {tt.stderr.strip()[:200]}"))
    # T2 — base B: tệp policy change-impact (và schema của nó) VẮNG MẶT ⇒ closure của §5 là tập rỗng
    pol = [p for p in git("-C", td, "ls-tree", "-r", "--name-only", ob, "--", ".github/coordination").splitlines() if "change-impact" in p]
    if pol:
        dung.append(f"policy change-impact có mặt trên base: {pol} — phải tính closure trước khi cấp lease (revision đặc tả)")
    # T3 — liên kết tượng trưng trên B: không đường dẫn nào của write set hay thư mục cha của nó là liên kết, không liên kết nào trỏ vào write set
    cay = [d.split("\t", 1) for d in git("-C", td, "ls-tree", "-r", "-t", ob).splitlines()]
    lk = {p: git("-C", td, "cat-file", "-p", m.split()[2]) for m, p in cay if m.split()[0] == "120000"}
    for p, dich in lk.items():
        toi = chuan(posixpath.normpath(posixpath.join(posixpath.dirname(p), dich)))
        if any(giao(chuan(p) or p, chuan(w)) or (toi and giao(toi, chuan(w))) for w in WS):
            dung.append(f"liên kết tượng trưng chạm write set: {p} -> {dich}")
    # T4 — mọi lease CÒN HIỆU LỰC trên mọi ref của kho tạm: write_set ∪ effective_write_set, chuẩn hoá §5, giao theo đường dẫn hay tiền tố thư mục
    try:
        lp = types.ModuleType("lease_publish")
        sys.modules["lease_publish"] = lp
        exec(compile(git("-C", td, "cat-file", "blob", f"{ob}:ops/lease_publish.py"), f"{ob}:ops/lease_publish.py", "exec"), lp.__dict__)
        cac = lp._quet_lease_toan_kho(pathlib.Path(td), chan_nhanh_tut_sau=True)
        bay_gio = datetime.datetime.now(datetime.timezone.utc)
        song = [m for m in cac if lp._phan_loai_lease(m["lease"], bay_gio) == "CÒN_HẠN" and lp._bia_mo_doi_xung(m["lease"], cac) is not True]
    except Exception as ex:  # thiếu hàm, YAML hỏng, ref thiếu, hạn không đọc được: đều là KHÔNG ĐO ĐƯỢC
        sys.exit(f"TIỀN KIỂM: DỪNG\n  KHÔNG ĐO ĐƯỢC: quét lease toàn kho: {type(ex).__name__}: {str(ex)[:300]}")
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
print(f"base {B} = {ob[:12]} · {len(mc)} nhánh máy chủ = {len(mc)} ref kho tạm · {len(cac)} bản ghi lease · {len(song)} còn hiệu lực · {len(lk)} liên kết tượng trưng · policy {len(pol)}")
print("TIỀN KIỂM: ĐẠT" if not dung else "TIỀN KIỂM: DỪNG\n  " + "\n  ".join(dung))
sys.exit(1 if dung else 0)
