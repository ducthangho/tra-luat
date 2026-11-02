#!/usr/bin/env python3
"""wp728 r2 — rig M2/M2': đếm zombie fixture qua nhiều chu kỳ keepalive của wrapper WP710.

Hợp đồng quan sát: ops/specs/wp728-do-linux-doc-lap-wp710-r2.md §Rig. Phiên điều phối dựng tệp này;
reviewer CHỈ chạy lại và đột biến (mutate.py), không sửa.

  python3 zombie_rig.py selftest
  python3 zombie_rig.py run --wrapper <ps1> --tests <Tests.ps1> [--max-cycles 5] [--interval 10] [--deadline 180]

`run` chạy wrapper ở chế độ fake `daemon` của bộ test, mỗi chu kỳ fake CLI sinh một tiến trình con (fixture)
rồi ghi pid của nó vào WP714_CHILD_PID_FILE. Một luồng poll ~50 ms đọc tệp ấy ở MỌI lần poll và đăng ký cặp
(pid, starttime) đọc từ /proc/<pid>/stat. Sau mỗi sự kiện `staged` (trừ chu kỳ cuối) luồng chính lấy một mẫu
khoảng nghỉ: trạng thái của TỪNG cặp đã đăng ký. Đầu ra: một dòng JSON mỗi khoảng + một dòng tổng kết.
Mã thoát: 0 = DO_DUOC (đọc số zombie trong tổng kết), 4 = KHONG_DO_DUOC, 2 = lỗi dùng.
Rig KHÔNG phán N2; nó báo số đếm, phán quyết thuộc người đọc theo spec.
"""
import argparse
import hashlib
import json
import os
import shutil
import signal
import subprocess
import sys
import tempfile
import threading
import time

NGUONG_GAP_S = 0.25        # một nửa tuổi sống danh nghĩa ~0,5 s của fake CLI sau khi ghi pid
CHU_KY_POLL_S = 0.05
MAU_SAU_STAGED_S = 1.0     # lấy mẫu 1 s sau `staged`
TRAN_MAU_S = 5.0           # mẫu phải xong trước nửa khoảng 10 s


class LoiDoc(Exception):
    """Đọc /proc lỗi khác ENOENT/ESRCH (vd. EACCES) ⇒ KHÔNG ĐO ĐƯỢC."""


def tach_stat(van_ban):
    # "pid (comm) S ppid ..." — comm có thể chứa dấu cách và ngoặc nên cắt ở ')' CUỐI.
    phai = van_ban.rindex(")")
    pid = int(van_ban[: van_ban.index("(")].strip())
    truong = van_ban[phai + 2:].split()
    # truong[0] là trường 3 (state) ⇒ trường 22 (starttime) là truong[19]
    return {"pid": pid, "state": truong[0], "ppid": int(truong[1]), "starttime": int(truong[19])}


def doc_proc(pid):
    """None = không còn (ENOENT/ESRCH). Ném LoiDoc cho lỗi khác."""
    try:
        with open(f"/proc/{pid}/stat", "r", encoding="ascii", errors="replace") as fh:
            van_ban = fh.read()
    except (FileNotFoundError, ProcessLookupError):
        return None
    except OSError as e:
        raise LoiDoc(f"{type(e).__name__} errno={e.errno}")
    if not van_ban:
        raise LoiDoc("stat rong")
    return tach_stat(van_ban)


def quet_proc():
    ra = []
    for ten in os.listdir("/proc"):
        if ten.isdigit():
            s = doc_proc(int(ten))
            if s is not None:
                ra.append(s)
    return ra


class Phien:
    """Lõi quan sát, tách khỏi tiến trình thật để ca tự kiểm bơm dữ liệu giả."""

    def __init__(self, so_chu_ky, doc, quet):
        self.so_chu_ky, self.doc, self.quet = so_chu_ky, doc, quet
        self.so = {}            # (pid, starttime) -> bản ghi thế hệ
        self.t_truoc = None
        self.max_gap = 0.0
        self.so_poll = 0
        self.nhieu = 0
        self.loi = []
        self.mau = []

    def quan_sat(self, t, noi_dung, chu_ky):
        """Một lần poll. `chu_ky` = số sự kiện `staged` đã đọc (chu kỳ đang chạy, đếm từ 0)."""
        if self.t_truoc is not None:
            self.max_gap = max(self.max_gap, t - self.t_truoc)
        self.t_truoc = t
        self.so_poll += 1
        s = (noi_dung or "").strip()
        if not s.isdigit():
            self.nhieu += 1          # khe tệp rỗng/đang ghi: nhiễu, KHÔNG suy là reap
            return
        pid = int(s)
        try:
            st = self.doc(pid)
        except LoiDoc as e:
            self.loi.append(f"poll: doc /proc/{pid}/stat loi {e}")
            return
        if st is None:
            self.nhieu += 1          # pid chưa có /proc hoặc đã đi: nhiễu
            return
        khoa = (pid, st["starttime"])
        if khoa not in self.so:
            self.so[khoa] = {"pid": pid, "starttime": st["starttime"], "chu_ky": chu_ky,
                             "t_thu": round(t, 3), "trang_thai_luc_thu": st["state"]}

    def lay_mau(self, khoang, t, wrapper_pid, wrapper_st):
        rec = {"loai": "mau", "khoang": khoang, "t": round(t, 3)}
        try:
            w = self.doc(wrapper_pid)
        except LoiDoc as e:
            w = None
            self.loi.append(f"khoang {khoang}: doc wrapper loi {e}")
        song = w is not None and w["starttime"] == wrapper_st and w["state"] != "Z"
        rec["wrapper"] = {"pid": wrapper_pid, "starttime": wrapper_st, "song": song}
        if not song:
            self.loi.append(f"khoang {khoang}: wrapper thoat som hoac doi starttime")
        cap, zf, con_song = [], 0, 0
        for e in sorted(self.so.values(), key=lambda x: x["t_thu"]):
            try:
                s = self.doc(e["pid"])
            except LoiDoc as x:
                tt = "LOI"
                self.loi.append(f"khoang {khoang}: doc fixture {e['pid']} loi {x}")
            else:
                if s is None:
                    tt = "ENOENT"
                elif s["starttime"] != e["starttime"]:
                    tt = "PID_TAI_DUNG"
                    self.loi.append(f"khoang {khoang}: pid {e['pid']} tai dung (starttime khac), khong tinh la fixture")
                elif s["state"] == "Z":
                    tt = "Z"
                    zf += 1
                else:
                    tt = "SONG"
                    con_song += 1
            cap.append({"pid": e["pid"], "starttime": e["starttime"], "chu_ky": e["chu_ky"], "trang_thai": tt})
        rec["so_dang_ky"] = cap
        rec["zombie_fixture_tich_luy"] = zf
        rec["fixture_con_song"] = con_song
        try:
            rec["z_con_cua_wrapper"] = sum(1 for p in self.quet() if p["state"] == "Z"
                                           and p["ppid"] == wrapper_pid and p["starttime"] >= wrapper_st)
        except LoiDoc as x:
            rec["z_con_cua_wrapper"] = None
            self.loi.append(f"khoang {khoang}: quet /proc loi {x}")
        self.mau.append(rec)
        return rec

    def ket_luan(self, so_staged, wrapper_rc=0, qua_han=False):
        ly_do = list(self.loi)
        n = self.so_chu_ky
        if qua_han:
            ly_do.append("qua thoi han cung")
        if so_staged != n:
            ly_do.append(f"staged {so_staged}/{n}")
        if wrapper_rc not in (0, None):
            ly_do.append(f"wrapper rc={wrapper_rc}")
        the_he = sorted(self.so.values(), key=lambda x: x["t_thu"])
        st_truoc = None
        for c in range(n):
            o = [e for e in the_he if e["chu_ky"] == c]
            if len(o) != 1:
                ly_do.append(f"chu ky {c}: {len(o)} the he (doi dung 1)")
            elif st_truoc is not None and o[0]["starttime"] <= st_truoc:
                ly_do.append(f"chu ky {c}: starttime khong tang")
            if len(o) == 1:
                st_truoc = o[0]["starttime"]
        ngoai = [e for e in the_he if not 0 <= e["chu_ky"] < n]
        if ngoai:
            ly_do.append(f"{len(ngoai)} the he ngoai chu ky du kien")
        if self.so_poll < 2:
            ly_do.append("qua it lan poll")
        if self.max_gap > NGUONG_GAP_S:
            ly_do.append(f"max_gap {self.max_gap * 1000:.0f} ms > {NGUONG_GAP_S * 1000:.0f} ms")
        khoang = [m["khoang"] for m in self.mau]
        if khoang != list(range(1, n)):
            ly_do.append(f"mau khoang {khoang} (doi {list(range(1, n))})")
        return {"loai": "tong_ket",
                "trang_thai": "KHONG_DO_DUOC" if ly_do else "DO_DUOC",
                "ly_do": ly_do,
                "zombie_fixture_theo_khoang": [m["zombie_fixture_tich_luy"] for m in self.mau],
                "z_con_cua_wrapper_theo_khoang": [m["z_con_cua_wrapper"] for m in self.mau],
                "max_gap_ms": round(self.max_gap * 1000, 1),
                "so_poll": self.so_poll, "nhieu": self.nhieu,
                "the_he": [{"pid": e["pid"], "starttime": e["starttime"], "chu_ky": e["chu_ky"],
                            "trang_thai_luc_thu": e["trang_thai_luc_thu"]} for e in the_he]}


# ---------------------------------------------------------------- chạy thật

def trich_fake(tests_bytes):
    """Lấy nguyên văn fake CLI từ here-string `$source = @' ... '@` trong Tests.ps1 đã neo."""
    dong = tests_bytes.decode("utf-8").splitlines()
    dau = [i for i, d in enumerate(dong) if d.strip() == "$source = @'"]
    if len(dau) != 1:
        raise SystemExit(f"KHONG_DO_DUOC: tim thay {len(dau)} dong mo here-string (doi 1)")
    cuoi = next((i for i in range(dau[0] + 1, len(dong)) if dong[i] == "'@"), None)
    if cuoi is None:
        raise SystemExit("KHONG_DO_DUOC: khong thay dong dong here-string")
    return "\n".join(dong[dau[0] + 1: cuoi]) + "\n"


def chay(a):
    pwsh = shutil.which("pwsh")
    if pwsh is None:
        print("KHONG_DO_DUOC: khong co pwsh tren PATH", file=sys.stderr)
        return 4
    with open(a.wrapper, "rb") as f:
        wrapper_b = f.read()
    with open(a.tests, "rb") as f:
        tests_b = f.read()
    fake_src = trich_fake(tests_b)
    goc = tempfile.mkdtemp(prefix="wp728-rig-")      # dưới $TMPDIR
    tmp_con = os.path.join(goc, "tmp")
    home = os.path.join(goc, "home")
    profile = os.path.join(goc, "profile")
    for d in (tmp_con, home, profile):
        os.makedirs(d)
    fake = os.path.join(goc, "fake.py")
    with open(fake, "w", encoding="utf-8", newline="\n") as f:
        f.write(fake_src)
    wrapper = os.path.join(goc, "nlm-credential-refresh.ps1")
    with open(wrapper, "wb") as f:
        f.write(wrapper_b)
    cfg = os.path.join(goc, "config.json")
    with open(cfg, "w", encoding="utf-8") as f:
        json.dump({"notebook_id": "NOTEBOOK12345", "browser_profile_path": profile}, f)
    pid_file = os.path.join(goc, "reap-child.pid")
    env = {"PATH": os.environ.get("PATH", ""), "TMPDIR": tmp_con, "HOME": home,
           "WP710_MODE": "daemon", "WP710_DELAY": "0", "WP710_LOG": os.path.join(goc, "calls.log"),
           "WP714_BEAT_FILE": os.path.join(goc, "beats.txt"), "WP714_CHILD_PID_FILE": pid_file}
    lenh = [pwsh, "-NoProfile", "-File", wrapper, "-ConfigPath", cfg, "-NlmCommand", sys.executable,
            "-NlmArgumentsPrefix", fake, "-StageCommand", sys.executable, "-StageArguments", fake,
            "-TimeoutSeconds", "5", "-EnableKeepalive", "-IntervalSeconds", str(a.interval),
            "-MaxCycles", str(a.max_cycles)]
    phien = Phien(a.max_cycles, doc_proc, quet_proc)
    khoa = threading.Lock()
    staged = []                 # thời điểm (monotonic) mỗi dòng staged
    dong_khac = []
    dung = threading.Event()
    han = time.monotonic() + a.deadline
    p = subprocess.Popen(lenh, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                         env=env, cwd=goc, start_new_session=True)

    def doc_stdout():
        for d in p.stdout:
            t = time.monotonic()
            try:
                st = json.loads(d).get("status")
            except (ValueError, AttributeError):
                st = None
            with khoa:
                if st == "staged":
                    staged.append(t)
                else:
                    dong_khac.append(st)

    def xa_stderr():
        for _ in p.stderr:
            pass

    def poll():
        while not dung.is_set():
            t0 = time.monotonic()
            try:
                with open(pid_file, "r", encoding="ascii", errors="replace") as fh:
                    nd = fh.read()
            except FileNotFoundError:
                nd = None
            with khoa:
                phien.quan_sat(t0, nd, len(staged))
            ngu = CHU_KY_POLL_S - (time.monotonic() - t0)
            if ngu > 0:
                time.sleep(ngu)

    luong = [threading.Thread(target=f, daemon=True) for f in (doc_stdout, xa_stderr, poll)]
    for th in luong:
        th.start()
    w = None
    while w is None and time.monotonic() < han and p.poll() is None:
        try:
            w = doc_proc(p.pid)
        except LoiDoc:
            w = None
        if w is None:
            time.sleep(0.01)
    qua_han = False
    if w is None:
        phien.loi.append("khong doc duoc danh tinh wrapper")
    else:
        for k in range(1, a.max_cycles):
            while time.monotonic() < han:
                with khoa:
                    if len(staged) >= k:
                        t_staged = staged[k - 1]
                        break
                if p.poll() is not None:
                    break
                time.sleep(0.01)
            else:
                qua_han = True
                break
            with khoa:
                if len(staged) < k:
                    phien.loi.append(f"khoang {k}: khong co staged (wrapper thoat som?)")
                    break
            con = t_staged + MAU_SAU_STAGED_S - time.monotonic()
            if con > 0:
                time.sleep(con)
            with khoa:
                truoc = len(staged)
                rec = phien.lay_mau(k, time.monotonic() - t_staged, w["pid"], w["starttime"])
                sau = len(staged)
            tre = time.monotonic() - t_staged
            if tre > TRAN_MAU_S:
                phien.loi.append(f"khoang {k}: mau xong sau {tre:.2f} s > {TRAN_MAU_S} s")
            if truoc != k or sau != k:
                phien.loi.append(f"khoang {k}: mau roi sang chu ky ke")
            print(json.dumps(rec, ensure_ascii=False), flush=True)
    try:
        rc = p.wait(timeout=max(0.1, han - time.monotonic()))
    except subprocess.TimeoutExpired:
        qua_han = True
        os.killpg(p.pid, signal.SIGKILL)
        rc = p.wait()
    time.sleep(0.1)
    dung.set()
    luong[2].join(timeout=2)
    with khoa:
        kl = phien.ket_luan(len(staged), rc, qua_han)
        if dong_khac:
            kl["ly_do"].append(f"dong stdout khac staged: {dong_khac}")
            kl["trang_thai"] = "KHONG_DO_DUOC"
    # dọn: chỉ giết fixture còn sống KHỚP cả pid lẫn starttime
    for e in phien.so.values():
        try:
            s = doc_proc(e["pid"])
        except LoiDoc:
            continue
        if s is not None and s["starttime"] == e["starttime"] and s["state"] != "Z":
            try:
                os.kill(e["pid"], signal.SIGKILL)
            except ProcessLookupError:
                pass
    kl.update({"wrapper_rc": rc, "so_staged": len(staged), "max_cycles": a.max_cycles,
               "interval_s": a.interval,
               "sha256_wrapper": hashlib.sha256(wrapper_b).hexdigest(),
               "sha256_tests": hashlib.sha256(tests_b).hexdigest(),
               "sha256_fake": hashlib.sha256(fake_src.encode("utf-8")).hexdigest()})
    print(json.dumps(kl, ensure_ascii=False), flush=True)
    return 0 if kl["trang_thai"] == "DO_DUOC" else 4


# ---------------------------------------------------------------- ca tự kiểm (dữ liệu giả, không tiến trình thật)

class TheGioiGia:
    def __init__(self):
        self.proc = {1000: {"state": "S", "ppid": 1, "starttime": 100}}

    def doc(self, pid):
        v = self.proc.get(pid)
        if v is None:
            return None
        if v == "EACCES":
            raise LoiDoc("PermissionError errno=13")
        return dict(v, pid=pid)

    def quet(self):
        return [dict(v, pid=p) for p, v in self.proc.items() if v != "EACCES"]


def mo_phong(n=5, pid=None, giu_zombie=(), an=(), khe_rong=(), tre_tai=None, eacces=(), tai_dung_o_khoang=None):
    """Dòng thời gian giả: chu kỳ c bắt đầu ở T_c; con sống 0,5 s, bị giết (Z), rồi bị reap trừ khi giữ zombie.
    an: chu kỳ mà con biến mất trước lần poll đầu (bị ghi đè trước khi thu)."""
    g = TheGioiGia()
    ph = Phien(n, g.doc, g.quet)
    pid = pid or [2000 + c for c in range(n)]
    T = [0.2 + c * 10.5 for c in range(n)]
    tep = None
    staged = 0
    t, buoc = 0.0, 0
    lam_xong = set()
    while t < T[-1] + 2.5:
        for c in range(n):
            st = 500 + c * 1000
            if ("ghi", c) not in lam_xong and t >= T[c]:
                lam_xong.add(("ghi", c))
                tep = str(pid[c])
                if c not in an:
                    g.proc[pid[c]] = "EACCES" if c in eacces else {"state": "S", "ppid": 1000, "starttime": st}
            if ("giet", c) not in lam_xong and t >= T[c] + 0.5 and c not in an:
                lam_xong.add(("giet", c))
                if g.proc.get(pid[c]) not in (None, "EACCES"):
                    g.proc[pid[c]] = {"state": "Z", "ppid": 1000, "starttime": st}
            if ("reap", c) not in lam_xong and t >= T[c] + 0.6:
                lam_xong.add(("reap", c))
                if c not in giu_zombie and c not in eacces:
                    g.proc.pop(pid[c], None)
            if ("staged", c) not in lam_xong and t >= T[c] + 0.8:
                lam_xong.add(("staged", c))
                staged += 1
            if c < n - 1 and ("mau", c) not in lam_xong and t >= T[c] + 1.8:
                lam_xong.add(("mau", c))
                k = c + 1
                if tai_dung_o_khoang == k:
                    g.proc[pid[0]] = {"state": "S", "ppid": 1, "starttime": 999999}
                ph.lay_mau(k, 1.0, 1000, 100)
                if tai_dung_o_khoang == k:
                    g.proc.pop(pid[0], None)
        nd = "" if buoc in khe_rong else tep
        ph.quan_sat(t, nd, staged)
        buoc += 1
        t = round(t + (0.3 if buoc == tre_tai else CHU_KY_POLL_S), 6)
    return ph, ph.ket_luan(staged)


def selftest():
    ca = []

    def ca_kiem(ten, dk):
        ca.append((ten, bool(dk)))

    ph, kl = mo_phong(giu_zombie=(0,))
    ca_kiem("1 zombie cu con lai, con moi nhat da reap => dem 1",
            kl["trang_thai"] == "DO_DUOC" and kl["zombie_fixture_theo_khoang"] == [1, 1, 1, 1])
    ph, kl = mo_phong(tai_dung_o_khoang=2)
    ca_kiem("2 pid trung starttime khac o mau => 0 zombie fixture, khong DO_DUOC",
            kl["zombie_fixture_theo_khoang"] == [0, 0, 0, 0] and kl["trang_thai"] == "KHONG_DO_DUOC"
            and any("tai dung" in x for x in kl["ly_do"]))
    ph, kl = mo_phong(pid=[2000, 2001, 2001, 2003, 2004])
    hai = [e["chu_ky"] for e in kl["the_he"] if e["pid"] == 2001]
    ca_kiem("3 hai chu ky lien cung pid starttime khac => hai ban ghi dung hai chu ky",
            kl["trang_thai"] == "DO_DUOC" and hai == [1, 2])
    ph, kl = mo_phong(an=(2,))
    ca_kiem("4 bo lo mot the he => KHONG_DO_DUOC",
            kl["trang_thai"] == "KHONG_DO_DUOC" and any("chu ky 2: 0 the he" in x for x in kl["ly_do"]))
    ph, kl = mo_phong(khe_rong=set(range(5, 9)) | set(range(215, 219)))
    ca_kiem("5 khe tep rong giua hai lan ghi => bo qua, khong dem la reap",
            kl["trang_thai"] == "DO_DUOC" and kl["nhieu"] >= 8 and kl["zombie_fixture_theo_khoang"] == [0, 0, 0, 0])
    ph, kl = mo_phong(tre_tai=100)
    ca_kiem("6 poll tre max_gap > 250 ms => KHONG_DO_DUOC",
            kl["trang_thai"] == "KHONG_DO_DUOC" and kl["max_gap_ms"] > 250)
    ph, kl = mo_phong(an=tuple(range(5)))
    ca_kiem("7 khong thu duoc danh tinh => KHONG_DO_DUOC",
            kl["trang_thai"] == "KHONG_DO_DUOC" and kl["the_he"] == [])
    ph, kl = mo_phong(eacces=(1,))
    ca_kiem("8 EACCES => KHONG_DO_DUOC",
            kl["trang_thai"] == "KHONG_DO_DUOC" and any("errno=13" in x for x in kl["ly_do"]))
    dat = sum(1 for _, ok in ca if ok)
    for ten, ok in ca:
        print(("DAT   " if ok else "TRUOT ") + ten)
    print(f"selftest {dat}/{len(ca)}")
    return 0 if dat == len(ca) == 8 else 1


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="lenh", required=True)
    sub.add_parser("selftest")
    r = sub.add_parser("run")
    r.add_argument("--wrapper", required=True)
    r.add_argument("--tests", required=True)
    r.add_argument("--max-cycles", type=int, default=5)
    r.add_argument("--interval", type=int, default=10)
    r.add_argument("--deadline", type=float, default=180.0)
    a = ap.parse_args()
    return selftest() if a.lenh == "selftest" else chay(a)


if __name__ == "__main__":
    sys.exit(main())
