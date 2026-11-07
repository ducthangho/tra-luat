"""Đề xuất vá (thu_de_xuat_v6.de_xuat) có chặn oan module HỢP LỆ khi code đã bị CPython chuyên biệt hoá (gọi nóng) hoặc đang bị
đo bởi sys.settrace / sys.monitoring (coverage) không? Chạy: python3 -I thu_chan_oan_v6.py"""
import os, sys, tempfile
D = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, D)
import khoa_ast_r8 as K, thu_s0_v6 as T6, thu_de_xuat_v6 as X
kq = {}
with tempfile.TemporaryDirectory() as d:
    m = T6.nap(X.FUT, d)
    kq["lanh"] = X.de_xuat(m)
    for i in range(200000):
        m.cu_phap_run(("python ops/a.py\n", "x | y", None, "bash ops/b.sh w")[i % 4], (None, "bash", "sh")[i % 3])
    kq["nong_200k"] = X.de_xuat(m)
    sys.settrace(lambda *a: None); kq["settrace"] = X.de_xuat(m); m.cu_phap_run("python ops/a.py", None); kq["settrace_sau_goi"] = X.de_xuat(m); sys.settrace(None)
    mon = sys.monitoring; mon.use_tool_id(3, "thu"); mon.set_events(3, mon.events.LINE | mon.events.PY_START)
    mon.register_callback(3, mon.events.LINE, lambda *a: None); mon.register_callback(3, mon.events.PY_START, lambda *a: None)
    m.cu_phap_run("python ops/a.py", None); kq["monitoring"] = X.de_xuat(m)
    mon.set_events(3, 0); mon.free_tool_id(3)
print(kq); sys.exit(1 if any(kq.values()) else 0)
