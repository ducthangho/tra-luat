# --- #1236 đợt C (`ops/specs/wp1236-r12.md`, mục *D2b chi tiết*): `moc_10_2_2.gate_output` dương của biên bản M8 phải khớp tệp đánh giá
# (hoặc readback miễn) TẠI `oid` trên remote. MÃ cổng lấy từ `origin/master`, DỮ LIỆU lấy từ `oid`; không đọc cây làm việc.
D2B_MODULE = "ops/gate_output_doi_chieu.py"
D2B_TEP_RE = re.compile(r"ops/land/[^/]+-provenance/(?:[^/]+/)*danh-gia-gate-output-[0-9]+\.txt")
D2B_READBACK_RE = re.compile(r"ops/land/[^/]+-provenance(?:/[^/]+)*")


def _d2b(root: Path, bb: dict, thieu: list) -> None:
    """Thêm vào `thieu` mỗi vi phạm một dòng `D2b <lý do>` (tên CỐ ĐỊNH); đạt thì in đúng một dòng `D2b ĐẠT …`. `gate_output` ngoài
    `passed`/`owner_waived` ⇒ không chạy. Lỗi đo (module không nạp được, git lỗi, dữ liệu ném) ⇒ `_die(RC_STATE)`: không traceback, không
    gộp vào vi phạm."""
    try:
        thieu.extend(f"D2b {x}" for x in _d2b_kiem(root, bb))
    except Exception as ex:
        _die(RC_STATE, f"KHÔNG ĐO ĐƯỢC: D2b {type(ex).__name__}: {ex}")


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

    def git(*x):  # đường dẫn là chuỗi THÔ, không phải pathspec; rc ≠ 0 ⇒ không dùng stdout (bị ngắt sau khi in vẫn là lỗi)
        rc, o = _git_do(root, "--literal-pathspecs", *x)
        return None if rc else o
    ref = git("branch", "-r", "--contains", oid, "--format=%(refname)")
    if git("cat-file", "-t", oid) != b"commit\n" or not any(r.startswith(b"refs/remotes/origin/") for r in (ref or b"").split(b"\n")):
        return vp + ["oid_khong_tren_remote"]
    if not (D2B_TEP_RE if passed else D2B_READBACK_RE).fullmatch(dd) or "." in dd.split("/") or ".." in dd.split("/"):
        return vp + ["duong_dan_sai"]
    if (cay_git := git("ls-tree", "-z", "-t", oid, "--", dd)) is None:
        raise OSError("git ls-tree")
    tien_to = [dd[:m.start()] for m in re.finditer("/", dd)] + [dd]  # mỗi tiền tố là cây 040000, tệp đánh giá là 100644; symlink (120000) hay vắng ⇒ đỏ
    mong = [(b"100644" if passed and d == dd else b"040000") + b"\t" + d.encode() for d in tien_to]
    co = [x.split(b" ")[0] + b"\t" + x.partition(b"\t")[2] for x in cay_git.split(b"\0")]
    if sai := [d for d, m, c in zip(tien_to, mong, co + [b""] * len(mong)) if m != c]:
        return vp + [f"symlink_hoac_mode:{sai[0]}"]
    with tempfile.TemporaryDirectory() as tam, tempfile.TemporaryDirectory() as tam_cay:
        ma, cay, thu = Path(tam) / D2B_MODULE, Path(tam_cay), "/".join(dd.split("/")[:3])
        if not (b := git("show", f"refs/remotes/origin/master:{D2B_MODULE}")):
            _die(RC_STATE, f"KHÔNG ĐO ĐƯỢC: không đọc được {D2B_MODULE} trên origin/master")
        ma.parent.mkdir(), ma.write_bytes(b)
        mod = _nap(Path(tam), "gate_output_doi_chieu")
        if not (tar := git("archive", "--format=tar", oid, "--", thu)):
            raise OSError("git archive")
        with tarfile.open(fileobj=io.BytesIO(tar)) as t:  # chỉ tệp thường (thư mục cha tự dựng): symlink trong `oid` KHÔNG được dựng lại
            t.extractall(cay, filter=lambda m, p: tarfile.data_filter(m, p) if m.isreg() else None)
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
