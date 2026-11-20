"""Phản chứng Linux: giả lập hình dạng đường của nt — `expanduser("~/x")` trả `<HOME>/./x` (khác CHUỖI, cùng tệp), như ntpath giữ '/'."""
import os, posixpath, runpy, sys
_that = posixpath.expanduser
def gia(p):
    r = _that(p)
    return r.replace("/.tra_luat_config.json", "/./.tra_luat_config.json") if p == "~/.tra_luat_config.json" else r
posixpath.expanduser = os.path.expanduser = gia
sys.argv = [sys.argv[0]] + sys.argv[1:]
runpy.run_path(os.path.join(os.path.dirname(os.path.abspath(__file__)), "chay_p2b.py"), run_name="__main__")
