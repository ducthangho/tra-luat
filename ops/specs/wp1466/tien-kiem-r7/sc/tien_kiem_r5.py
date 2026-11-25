import datetime, posixpath, subprocess, sys, unicodedata
WS = [".claude/dev/packet_loop.py", ".claude/dev/packet_loop_test.py", "docs/PROTOCOL_DA_PHIEN.md", "docs/adr/0068-bat-bien-protocol-va-review-theo-lop.md"]
B, sau = sys.argv[1], (sys.argv[sys.argv.index("--sau-dang") + 1] if "--sau-dang" in sys.argv else None)
dung = []
def git(*a):
    r = subprocess.run(["git", *a], capture_output=True, text=True, encoding="utf-8")
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
# T2 — base B: tệp policy change-impact (và schema của nó) VẮNG MẶT ⇒ closure của §5 là tập rỗng
pol = [p for p in git("ls-tree", "-r", "--name-only", B, "--", ".github/coordination").splitlines() if "change-impact" in p]
if pol:
    dung.append(f"policy change-impact có mặt trên base: {pol} — phải tính closure trước khi cấp lease (revision đặc tả)")
# T3 — liên kết tượng trưng trên B: không đường dẫn nào của write set hay thư mục cha của nó là liên kết, không liên kết nào trỏ vào write set
cay = [d.split("\t", 1) for d in git("ls-tree", "-r", "-t", B).splitlines()]
lk = {p: git("cat-file", "-p", m.split()[2]) for m, p in cay if m.split()[0] == "120000"}
for p, dich in lk.items():
    toi = chuan(posixpath.normpath(posixpath.join(posixpath.dirname(p), dich)))
    if any(giao(chuan(p) or p, chuan(w)) or (toi and giao(toi, chuan(w))) for w in WS):
        dung.append(f"liên kết tượng trưng chạm write set: {p} -> {dich}")
# T4 — mọi lease CÒN HIỆU LỰC trên mọi ref: write_set ∪ effective_write_set, chuẩn hoá §5, giao theo đường dẫn hay tiền tố thư mục
sys.path.insert(0, "ops")
try:
    import lease_publish as lp
    cac = lp._quet_lease_toan_kho(lp.Path(".").resolve(), chan_nhanh_tut_sau=True)
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
print(f"base {B} · {len(mc)} nhánh máy chủ · {len(cac)} bản ghi lease · {len(song)} còn hiệu lực · {len(lk)} liên kết tượng trưng · policy {len(pol)}")
print("TIỀN KIỂM: ĐẠT" if not dung else "TIỀN KIỂM: DỪNG\n  " + "\n  ".join(dung))
sys.exit(1 if dung else 0)
