"""Nguyên mẫu M2–M4 của đặc tả N (bản sửa lượt 1) — áp vào tl_gws.py của một bản sao; chỉ để đo neo/fragment."""
import sys

p = sys.argv[1]
s = open(p, encoding="utf-8").read()


def rep(a, b):
    global s
    assert s.count(a) == 1, a
    s = s.replace(a, b)


rep("""                os.lstat(g)
                return d
            except OSError:
                pass""", """                os.lstat(g)
                return d
            except (FileNotFoundError, NotADirectoryError):
                pass""")
rep('''def _kiem_env_w6(bundle: dict)''', '''def _chot_thu_muc(thu_muc: str) -> str | None:
    """WP433 N: None hoặc lý do — luật (b) trên mọi tiền tố gốc→`thu_muc`; không `.git`."""
    if os.name == "posix":
        c = ("/", ()) if thu_muc.startswith("/") and thu_muc.strip("/") == "" else _duong_dich_chuan(thu_muc, os.getcwd())
        goc = "/"
    else:
        c = _duong_dich_chuan_nt(thu_muc, os.getcwd())
        goc = c[0] if not isinstance(c, str) else None
    if isinstance(c, str):
        return c
    tp = c[1]
    for i in range(len(tp) + 1):
        tien_to = os.path.join(goc, *tp[:i])
        try:
            st = os.lstat(tien_to)
            la_lk = stat.S_ISLNK(st.st_mode) or bool(getattr(st, "st_file_attributes", 0) & stat.FILE_ATTRIBUTE_REPARSE_POINT)
        except (FileNotFoundError, NotADirectoryError):
            continue
        if la_lk:
            return f"là liên kết tượng trưng: {repr(tien_to)[:200]}"
    return None


def _kiem_env_w6(bundle: dict)''')
rep("""            ly_cfg = _kiem_dich_ghi(cfgp, cfgp, ())
""", """            ly_cfg = _kiem_dich_ghi(cfgp, cfgp, ())
            ly_cfg = ly_cfg or _chot_thu_muc(os.path.dirname(cfgp))
""")
rep("""        if (ly_do := _kiem_dich_ghi(os.path.join(nbase, *tp), nbase, tp)) is not None:
            return ly_do
    return None""", """        if (ly_do := _kiem_dich_ghi(os.path.join(nbase, *tp), nbase, tp)) is not None:
            return ly_do
    return _chot_thu_muc(os.path.dirname(nbase))""")
rep("""        print(f"[nlm-auth-pull] ✗ giải mã lỗi: {e}", file=sys.stderr)
        return 3
""", """        print(f"[nlm-auth-pull] ✗ giải mã lỗi: {e}", file=sys.stderr)
        return 3
    if not isinstance(bundle, dict):
        print("[nlm-auth-pull] ✗ dữ liệu không hợp lệ: bundle", file=sys.stderr)
        return 3
""")
rep("""        return 3
    print(f"[bootstrap] env={env}""", """        return 3
    if not isinstance(bundle, dict):
        print("[bootstrap] ✗ dữ liệu không hợp lệ: bundle", file=sys.stderr)
        return 3
    print(f"[bootstrap] env={env}""")
open(p, "w", encoding="utf-8").write(s)
print("ok")
