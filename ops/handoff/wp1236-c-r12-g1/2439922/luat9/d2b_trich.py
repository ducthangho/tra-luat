# --- #1236 đợt C (`ops/specs/wp1236-r12.md`, mục *D2b chi tiết*): `moc_10_2_2.gate_output` dương của biên bản M8 phải khớp tệp đánh giá
# (hoặc readback miễn) TẠI `oid` trên remote. MÃ cổng lấy từ `origin/master`, DỮ LIỆU lấy từ `oid`; không đọc cây làm việc.
# Mỗi thành phần đường dẫn chỉ nhận ASCII in được 0x21–0x7E trừ `/` (chủ kho, #1236 issuecomment-7134458601): đường dẫn in ra luôn đúng một dòng.
D2B_MODULE = "ops/gate_output_doi_chieu.py"
D2B_TEP_RE = re.compile(r"ops/land/[!-.0-~]+-provenance/(?:[!-.0-~]+/)*danh-gia-gate-output-[0-9]+\.txt")
D2B_READBACK_RE = re.compile(r"ops/land/[!-.0-~]+-provenance(?:/[!-.0-~]+)*")


def _d2b(root: Path, bb: dict, thieu: list) -> None:
    """Thêm vào `thieu` mỗi vi phạm một dòng `D2b <lý do>` (tên CỐ ĐỊNH); đạt thì in đúng một dòng `D2b ĐẠT …`. `gate_output` ngoài
    `passed`/`owner_waived` ⇒ không chạy. Lỗi đo (module không nạp được, git lỗi, dữ liệu ném) ⇒ `_die(RC_STATE)`: không traceback, không
    gộp vào vi phạm."""
    try:
        thieu.extend(f"D2b {x}" for x in _d2b_kiem(root, bb))
    except Exception as ex:
        _die(RC_STATE, f"KHÔNG ĐO ĐƯỢC: D2b {ex!r}")  # repr: thông điệp của ngoại lệ không tách được dòng


def _d2b_blob(b: bytes) -> bytes:
    return hashlib.sha1(b"blob %d\0" % len(b) + b).hexdigest().encode()  # OID blob của git (kho sha1: `oid` 40 hex)


def _d2b_kiem(root: Path, bb: dict) -> list:
    go, ci, m_c = bb["moc_10_2_2"]["gate_output"], bb["ci_master"], bb["merge_commit"]
    passed = go == "passed"
    if not passed and go != "owner_waived":
        return []
    ng, ra = bb.get("gate_output_nguon" if passed else "gate_output_mien"), ci.get("run_attempt")
    khoa = ("oid", "tep") if passed else ("oid", "chuoi", "readback_thu_muc")
    vp = [] if isinstance(ng, dict) and all(isinstance(ng.get(k), str) for k in khoa) and SHA_RE.fullmatch(ng["oid"]) else ["thieu_nguon"]
    if passed and not (type(ra) is int and ra >= 1):
        vp.append("attempt_kieu")
    if "thieu_nguon" in vp:
        return vp
    oid, dd = ng["oid"], ng[khoa[-1]]
    if not (D2B_TEP_RE if passed else D2B_READBACK_RE).fullmatch(dd) or "." in dd.split("/") or ".." in dd.split("/"):
        return vp + ["duong_dan_sai"]  # kiểm trên chuỗi THÔ, trước mọi lệnh git và mọi dòng in

    def git(*x, hoi=False):  # đường dẫn là chuỗi THÔ, không phải pathspec. rc ≠ 0 ⇒ KHÔNG dùng stdout (bị ngắt sau khi in vẫn là lỗi):
        rc, o = _git_do(root, "--literal-pathspecs", *x)  # lệnh HỎI (`hoi`) coi như trả rỗng, lệnh còn lại là lỗi đo
        if rc and not hoi:
            raise OSError(f"git {x[0]}")
        return b"" if rc else o
    ref = git("branch", "-r", "--contains", oid, "--format=%(refname)", hoi=True)
    if git("cat-file", "-t", oid, hoi=True) != b"commit\n" or not any(r.startswith(b"refs/remotes/origin/") for r in ref.split(b"\n")):
        return vp + ["oid_khong_tren_remote"]
    cay_git = git("ls-tree", "-z", "-t", oid, "--", dd)
    tien_to = [dd[:m.start()] for m in re.finditer("/", dd)] + [dd]  # mỗi tiền tố là cây 040000, tệp đánh giá là 100644; symlink (120000) hay vắng ⇒ đỏ
    mong = [(b"100644" if passed and d == dd else b"040000") + b"\t" + d.encode() for d in tien_to]
    co = [x.split(b" ")[0] + b"\t" + x.partition(b"\t")[2] for x in cay_git.split(b"\0")]
    if sai := [d for d, m, c in zip(tien_to, mong, co + [b""] * len(mong)) if m != c]:
        return vp + [f"symlink_hoac_mode:{sai[0]}"]
    with tempfile.TemporaryDirectory() as tam, tempfile.TemporaryDirectory() as tam_cay:
        ma, cay, thu = Path(tam) / D2B_MODULE, Path(tam_cay), "/".join(dd.split("/")[:3])
        if not (b := git("show", f"refs/remotes/origin/master:{D2B_MODULE}", hoi=True)):
            _die(RC_STATE, f"KHÔNG ĐO ĐƯỢC: không đọc được {D2B_MODULE} trên origin/master")
        ma.parent.mkdir(), ma.write_bytes(b)
        mod = _nap(Path(tam), "gate_output_doi_chieu")
        with tarfile.open(fileobj=io.BytesIO(git("archive", "--format=tar", oid, "--", thu))) as t:
            t.extractall(cay, filter="data")
        # Bản bung phải ĐÚNG là cây của `oid`, từng mục: symlink vẫn là symlink (validator tự thấy và tự từ chối theo K2), tệp khớp băm blob.
        # Lệch khi `.gitattributes` của `oid` ẩn tệp (export-ignore) hay đổi byte (eol, ident), khi nền không tạo được symlink (tarfile chép
        # đích), hoặc khi hai tên chỉ khác hoa/thường hay dạng chuẩn hoá (nền không phân biệt sẽ gộp làm một).
        muc = [(x.split(b" ")[0], x.split(b"\t")[0][-40:], os.fsdecode(x.partition(b"\t")[2])) for x in filter(None, git("ls-tree", "-r", "-z", oid, "--", thu).split(b"\0"))]
        if len({unicodedata.normalize("NFC", t).casefold() for _, _, t in muc}) != len(muc) or not all(
                (cay / t).is_symlink() if mode == b"120000" else (cay / t).is_file() and _d2b_blob((cay / t).read_bytes()) == sha
                for mode, sha, t in muc):
            raise OSError("bản bung git archive không khớp cây của oid")
        if passed:
            tt, ly = mod.kiem_tep(cay / dd, cay / thu)
            if tt != "passed":
                vp.append(f"kiem_tep:{tt}:{ly[0] if ly else '-'}")
            if d := mod.doc_danh_gia((cay / dd).read_bytes())[0]:
                neo = (("neo_run", d["run"], ci["run_id"]), ("neo_attempt", d["attempt"], ra), ("neo_head", d["head"], m_c))
                vp += [k for k, x, y in neo if x != y and not (k == "neo_attempt" and "attempt_kieu" in vp)]
        else:
            vp += [f"mien:{x}" for x in mod.kiem_mien(ng["chuoi"], cay / dd, m_c)]
    if not vp:
        print(f"D2b ĐẠT {'' if passed else 'mien '}{dd}@{oid}")
    return vp
