#!/usr/bin/env python3
"""Driver đột biến NGOÀI kho cho #1342 r4 (đặc tả §4b, M8/N7). Không sửa tệp nào của kho: mỗi đột biến ghi ra một BẢN SAO TẠM tên riêng.

    python dot_bien_r4.py <thư mục .claude/dev> [id đột biến ...]      # mặc định: mọi đột biến của NỀN đang chạy
    python dot_bien_r4.py <thư mục .claude/dev> --kiem-neo             # chỉ kiểm mỗi cặp (tìm, thay) khớp ĐÚNG MỘT chỗ + bản đột biến compile

Mỗi cặp (tìm, thay) phải khớp đúng một chỗ. Mỗi ca chạy trong tiến trình con riêng, watchdog NGOÀI ca 120 s.
Phân hạng: GIẾT ⇔ ca đích ĐỎ bằng AssertionError mang ĐÚNG nhãn VÀ ca đối chứng ĐẠT trên chính bản đột biến VÀ ca đích ĐẠT trên bản sạch.
Mọi kết cục khác (BỎ QUA/KHÔNG ĐO, lỗi import, hết hạn, đỏ nhãn khác) KHÔNG tính giết.
"""
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

ARGS = ('''    _1174_require(
        type(argv) is list and bool(argv) and all(type(x) is str for x in argv) and type(cwd) is str and
        type(deadline) in (int, float) and (type(deadline) is int or math.isfinite(deadline)) and
        time.monotonic() < deadline <= time.monotonic() + 86400 and
        (env is None or type(env) is dict and all(type(a) is str and type(b) is str for a, b in env.items())) and
        all(x is None or callable(x) for x in (truoc_gan, between)), "spawn arguments")
''', '''    _1174_require(os.name == "nt", "native Windows required")
''')
B7 = '''            snap = k.CreateToolhelp32Snapshot(0x4, 0)   # TH32CS_SNAPTHREAD: CPython closed the primary thread handle
            need(snap and snap != c.c_void_p(-1).value, "thread snapshot")
            dang_ky["close_snap"] = lambda: need(k.CloseHandle(snap), "handle close")
            te, entries = s.THREADENTRY32(), []
            te.dwSize = c.sizeof(te)
            more = k.Thread32First(snap, c.byref(te))
            while more:
                entries.append((te.th32OwnerProcessID, te.th32ThreadID))
                more = k.Thread32Next(snap, c.byref(te))
            need(c.get_last_error() == 18, "thread snapshot")   # only ERROR_NO_MORE_FILES ends the walk (or means an empty list)
            th = k.OpenThread(0x2 | 0x800, False, _1174_win_pick_thread(entries, proc.pid))   # SUSPEND_RESUME | QUERY_LIMITED_INFORMATION
            need(th, "suspended start")
            dang_ky["close_thread"] = lambda: need(k.CloseHandle(th), "handle close")
            _1174_require(0 != k.GetProcessIdOfThread(th) == proc.pid, "suspended start")   # the thread id was not reused meanwhile
            _1174_win_resume_ok(k.ResumeThread(th))
'''
B5 = '''            need(k.AssignProcessToJobObject(job, proc._handle), "job assignment")
            da_gan = True
            if between is not None:
                between(job)
'''
B_CHO = '''            _het_b = time.monotonic() + 5   # đột biến b: chờ ĐÚNG tệp marker của con (argv[7]) trước khi gán
            while not os.path.exists(argv[7]):
                if time.monotonic() > _het_b:
                    raise RuntimeError("DOT_BIEN_B_KHONG_DO: marker khong xuat hien trong 5 s")
                time.sleep(0.02)
'''
P = "wp1342_pure_spawn_"
J = "wp1342_native_job_"
# id: (nền, [(tìm, thay)...], ca đích, nhãn phải có trong thông điệp AssertionError, ca đối chứng HOẶC bộ ca đối chứng)
# b và abi làm hỏng CHÍNH đường spawn mà J1 đi qua (đo native 19-11) ⇒ đối chứng của chúng là J11 + S1 (đặc tả bản 13 §4b).
DOT_BIEN = {
    "a1": ("nt", [('"terminate": lambda: need(k.TerminateJobObject(job, 1), "job terminate"),', '"terminate": lambda: None,')],
           J + "mo_coi", "job not empty", J + "thuan"),
    "a2": ("nt", [("_1174_WIN_JOB_LIMIT = 0x2000", "_1174_WIN_JOB_LIMIT = 0")], J + "cha_chet_sau_gan", "J10: con/cháu sống sau khi cha chết", J + "thuan"),
    "a3": ("nt", [('''        if not k.QueryInformationJobObject(job, 1, ctypes.byref(info), ctypes.sizeof(info), None):
            raise _1174Error("job query") from ctypes.WinError(ctypes.get_last_error())
''', '''        if not k.QueryInformationJobObject(job, 1, ctypes.byref(info), ctypes.sizeof(info), None):
            return None
''')], J + "query_loi", "J11: handle tệp được nhận là job rỗng", J + "thuan"),
    "b": ("nt", [(B5 + B7, B7 + B_CHO + B5)], J + "treo_truoc_gan", "J6 (ii): marker đã có lúc between", (J + "query_loi", P + "hang_luong")),
    "c": ("moi", [("_1174_WIN_SPAWN_FLAGS = 0x204", "_1174_WIN_SPAWN_FLAGS = 0x200")], P + "hang_luong", "S1 SPAWN_FLAGS == 0x204", P + "arguments"),
    "h": ("nt", [('    need(job, "job create")\n', '    need(job, "job create")\n'
                  '    k.SetHandleInformation.argtypes, k.SetHandleInformation.restype = [w.HANDLE, w.DWORD, w.DWORD], w.BOOL\n'
                  '    need(k.SetHandleInformation(job, 1, 1), "dot bien h")\n')], J + "khong_ke_thua", "J7: job handle có HANDLE_FLAG_INHERIT", J + "thuan"),
    "k1": ("nt", [('            dang_ky["kill_truoc_gan"] = proc.kill\n', '')], J + "loi_truoc_gan", "J8: bản sao con chưa signaled trong 5 s", J + "thuan"),
    "k2": ("nt", [('''            da_gan = True
            if between is not None:
''', '''            if between is not None:
'''), ('''            _1174_win_resume_ok(k.ResumeThread(th))
''', '''            _1174_win_resume_ok(k.ResumeThread(th))
            da_gan = True
''')], J + "loi_sau_gan", "J9: tiến trình phụ chưa signaled trong 5 s VÀ j9 không có ghi chú cleanup:xac_nhan", J + "mo_coi"),
    "k3": ("moi", [('''            failed.append((code, error))
''', '''            failed.append((code, error))
            break
''')], P + "cleanup_note", "S4: bước 2 không chạy", P + "hang_luong"),
    "t1": ("moi", [('    _1174_require(len(found) == 1, "suspended start")\n', '    _1174_require(len(found) >= 1, "suspended start")\n')],
           P + "hang_luong", "S2: hai ứng viên được nhận", P + "cleanup_note"),
    "t2": ("moi", [("== _1174_WIN_RESUME_OK", "in (1, 2)")], P + "hang_luong", "S3 count=2", P + "cleanup_note"),
    "d0": ("nt", [("proc.wait(timeout=min(con_lai, 60.0))", "proc.wait()")], J + "han", "J2: không ném lifecycle deadline trong 6–11 s", J + "thuan"),
    "g0": ("moi", [(ARGS[0] + ARGS[1], ARGS[1] + ARGS[0])], P + "arguments", "S5 argv=[] phải là spawn arguments", P + "hang_luong"),
    "abi": ("nt", [('("th32OwnerProcessID", I)', '("th32OwnerProcessID", c.c_uint64)')], J + "abi", "J0 THREADENTRY32 offset th32OwnerProcessID == 12", (J + "query_loi", P + "hang_luong")),
    "d1": ("moi", [("time.monotonic() < deadline <= time.monotonic() + 86400 and", "time.monotonic() < deadline and")],
           P + "arguments", "S5 deadline ngoài miền nhận (now+10**6) phải là spawn arguments", P + "hang_luong"),
}
VO = r'''
import json, sys, tempfile, warnings
from pathlib import Path
warnings.simplefilter("ignore")
dev, script, ten = sys.argv[1:4]
sys.path.insert(0, dev)
import packet_loop_test as t
for s in (sys.stdout, sys.stderr):
    s.reconfigure(encoding="utf-8", errors="backslashreplace")
with tempfile.TemporaryDirectory() as td:
    try:
        dict(t.CASES)[ten](t.Ctx(Path(script), Path(td)))
        kq = ("DAT", "")
    except t.BoQua as ex:
        kq = ("KHONG_DO", str(ex))
    except AssertionError as ex:
        kq = ("DO", str(ex))
    except BaseException as ex:
        kq = ("KHONG_DO", "ngoại lệ khác AssertionError: " + type(ex).__name__ + ": " + str(ex))
print("KQ_R4 " + json.dumps(kq, ensure_ascii=True))
'''


def chay_ca(dev, script, ten):
    try:
        p = subprocess.run([sys.executable, "-B", "-c", VO, str(dev), str(script), ten], capture_output=True, text=True, timeout=120,
                           encoding="utf-8", errors="backslashreplace", env=dict(os.environ, PYTHONUTF8="1"))
    except subprocess.TimeoutExpired:
        return ("KHONG_DO", "watchdog ngoài ca 120 s")
    dong = [ln for ln in p.stdout.splitlines() if ln.startswith("KQ_R4 ")]
    return tuple(json.loads(dong[-1][6:])) if dong else ("KHONG_DO", f"không có dòng kết quả: rc={p.returncode} {p.stderr[-400:]}")


def dot_bien(goc, cap):
    for tim, thay in cap:
        assert goc.count(tim) == 1, f"mốc khớp {goc.count(tim)} chỗ (đòi đúng 1): {tim[:90]!r}"
        goc = goc.replace(tim, thay)
    return goc


def main():
    for s in (sys.stdout, sys.stderr):
        s.reconfigure(encoding="utf-8", errors="backslashreplace")
    dev, chon = Path(sys.argv[1]).resolve(), sys.argv[2:]
    goc = (dev / "packet_loop.py").read_text(encoding="utf-8")
    if chon == ["--kiem-neo"]:
        for ma, (_, cap, *_r) in DOT_BIEN.items():
            compile(dot_bien(goc, cap), ma, "exec")
            print(f"  neo OK + compile OK  {ma} ({len(cap)} cặp)")
        return 0
    nen = "nt" if os.name == "nt" else "moi"
    chon = chon or [ma for ma, v in DOT_BIEN.items() if v[0] == "moi" or nen == "nt"]
    hong = 0
    with tempfile.TemporaryDirectory(prefix="dot_bien_r4_") as td:
        for ma in chon:
            _, cap, dich, nhan, doi_chung = DOT_BIEN[ma]
            ban = Path(td) / f"packet_loop_{ma}.py"
            ban.write_text(dot_bien(goc, cap), encoding="utf-8", newline="\n")
            doi_chung = (doi_chung,) if isinstance(doi_chung, str) else doi_chung
            sach, do, dc = chay_ca(dev, dev / "packet_loop.py", dich), chay_ca(dev, ban, dich), [chay_ca(dev, ban, t)[0] for t in doi_chung]
            giet = sach[0] == "DAT" and do[0] == "DO" and nhan in do[1] and dc == ["DAT"] * len(dc)
            hang = "GIẾT" if giet else "SỐNG" if do[0] == "DAT" and sach[0] == "DAT" else "KHÔNG ĐO"
            hong += not giet
            print(f"{hang:9} {ma:4} đích={dich} [sạch={sach[0]} đột biến={do[0]}] đối chứng={'+'.join(doi_chung)} {dc} nhãn đòi={nhan!r}")
            print(f"          thông điệp: {(do[1] or sach[1])[:300]}")
    print(f"TỔNG: {len(chon) - hong}/{len(chon)} giết đúng dấu hiệu")
    return int(bool(hong))


if __name__ == "__main__":
    sys.exit(main())
