#!/usr/bin/env python3
"""doc_receipt_thu_hoi_git.py — C1a1b (#1179): kiểm `receipt.json` của `thu-hoi` trên ĐỒ THỊ Git của kho.

Đặc tả `ops/specs/wp1179-c1a1b-r9.md` (sha256 `c9bc8aca…`). Gọi NGUYÊN `kiem_json` của C1a1a (nạp theo đường dẫn tệp,
không sửa `sys.path`, không viết lại K1–K5) rồi chạy G0–G9 bằng reader tự băm lại từng object (§2.3).
`ok: true` KHÔNG phải quyền land và KHÔNG chứng minh provenance của run: nó chỉ nói receipt đúng hình dạng (C1a1a) và
nhất quán với commit C mà chính receipt khai, trên đồ thị của kho tại `--goc-kho` (N7). Chứng minh C là việc của C1a2.
"""
import argparse
import hashlib
import importlib.util
import json
import os
import pathlib
import re
import subprocess
import sys
import threading
import time

_sp = importlib.util.spec_from_file_location("_c1a1a_doc_receipt", pathlib.Path(__file__).with_name("doc_receipt_thu_hoi.py"))
C1A1A = importlib.util.module_from_spec(_sp)
_sp.loader.exec_module(C1A1A)

MOC = "601a0f18c83057fa079d204122660f5697fc6389"  # merge PR #620, tách S khỏi C; hằng, không nhận ghi đè
MODE = ("100644", "100755", "120000", "160000", "40000")
NHAN = ("100644", "100755", "120000")  # tập mode G7/G8 nhận (tương thích producer, bác 160000/40000)
DUONG_BK, DUONG_WF = "ops/lease_publish.py", ".github/workflows/ops-thu-hoi-admission.yml"
TRAN_RECEIPT = 8388608
NGAN_SACH = {"max_commit_moi_phep_di": 50000, "max_object_bytes": 8388608, "max_tong_bytes": 134217728, "deadline_giay": 60.0}
LUAT = tuple(f"G{i}" for i in range(10))
_H40 = re.compile(r"[0-9a-f]{40}")
_DAU = re.compile(rb"([0-9a-f]{40}) (?:(blob|tree|commit|tag) ([0-9]+)|(missing))\n")
_CHUNG = ("E_reader_chet", "E_ngan_sach: tong", "E_ngan_sach: deadline")  # sự kiện CHUNG: không ghi vào sổ lỗi theo OID


class SuKien(Exception):
    """Một sự kiện `E` của bảng đóng §2.3; chuỗi bắt đầu bằng tên sự kiện."""


def _env():
    e = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    e.update(GIT_NO_REPLACE_OBJECTS="1", GIT_CONFIG_NOSYSTEM="1", GIT_CONFIG_GLOBAL=os.devnull, GIT_TERMINAL_PROMPT="0")
    return e


_GIT = []


def _git_exe():
    """Git THẬT trong `--exec-path`, không qua shim trên PATH: `cmd\\git.exe` của Windows sinh git con, nên kill shim KHÔNG giết
    tiến trình đang giữ ống — reader chết giả và Timer deadline không gỡ được `cat-file` treo (đo A16 07-11). Không có thì `git`."""
    if not _GIT:
        try:
            ep = subprocess.run(["git", "--exec-path"], capture_output=True, text=True, env=_env(), timeout=60).stdout.strip()
        except (OSError, subprocess.SubprocessError):
            ep = ""
        _GIT.append(next((c for c in (os.path.join(ep, "git.exe"), os.path.join(ep, "git")) if ep and os.path.isfile(c)), "git"))
    return _GIT[0]


def _git(goc, *a, timeout=60.0):
    return subprocess.run([_git_exe(), "--no-replace-objects", "-C", str(goc), *a], capture_output=True, env=_env(), timeout=timeout)


def doc_ref(goc, nhanh, timeout=60.0):
    """`refs/remotes/origin/<nhanh>` khớp ĐÚNG tên (không DWIM, không tiền tố); None khi không đúng một hex40."""
    ten = f"refs/remotes/origin/{nhanh}"
    try:
        p = _git(goc, "for-each-ref", "--format=%(refname) %(objectname)", ten, timeout=timeout)
    except (OSError, subprocess.SubprocessError):
        return None
    ds = [d.split(" ")[-1] for d in p.stdout.decode("utf-8", "replace").splitlines() if d.split(" ")[0] == ten]
    return ds[0] if p.returncode == 0 and len(ds) == 1 and _H40.fullmatch(ds[0]) else None


class Doc:
    """Reader: MỘT `cat-file --batch`, băm lại mọi object, memo `(kiểu mong đợi, OID)` chỉ lưu thành công."""

    def __init__(s, goc, ns, seam):
        s.goc, s.ns, s.seam, s.memo, s.loi = goc, ns, seam, {}, {}
        s.so_object = s.tong_bytes = 0
        s.het_tong = s.chet = False
        s.dong_ho = seam.get("dong_ho", time.monotonic)
        s.han = s.dong_ho() + ns["deadline_giay"]
        s._mo()

    def _mo(s):
        s.p = subprocess.Popen([_git_exe(), "--no-replace-objects", "-C", str(s.goc), "cat-file", "--batch"], stdin=subprocess.PIPE,
                               stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, env=_env())
        s.ra = s.seam.get("ra", lambda f: f)(s.p.stdout)
        s.hen = threading.Timer(s.ns["deadline_giay"], s.p.kill)  # tiến trình treo không giữ được caller quá hạn
        s.hen.daemon = True
        s.hen.start()

    def dong(s):
        s.hen.cancel()
        try:
            s.p.stdin.close()  # EOF trước: cat-file thoát cả khi có tiến trình trung gian
        except OSError:
            pass
        if s.p.poll() is None:
            s.p.kill()
        s.p.wait()
        for f in (s.p.stdin, s.p.stdout):
            try:
                f.close()
            except OSError:
                pass

    def kiem_han(s):
        if s.dong_ho() >= s.han:
            raise SuKien("E_ngan_sach: deadline")

    def _chet(s, ly):
        s.chet = True  # vị trí luồng không còn biết: kết thúc, KHÔNG khởi động lại
        if s.p.poll() is None:
            s.p.kill()
        raise SuKien(f"E_reader_chet: {ly}")

    def _lay(s, n, giu=True, dem=True):
        """F2: MỌI byte nội dung lấy khỏi ống đều được đếm, kể cả thân bị xả, bị bác, hay đọc dở trước khi reader chết."""
        ket, con = [], n
        while con:
            c = s.ra.read(min(con, 1 << 20))
            if not c:
                s._chet(f"than ngan {n - con}/{n}")
            con -= len(c)
            if dem:
                s.tong_bytes += len(c)
            if giu:
                ket.append(c)
        return b"".join(ket)

    def doc(s, oid, kieu):
        s.kiem_han()  # dừng sớm phép đi dài; kết quả luật đã do kiem_han đầu/cuối luật quyết định (bảng phạm vi §2.3)
        k = (kieu, oid)
        if k in s.memo:
            return s.memo[k]
        if k in s.loi:
            raise SuKien(s.loi[k])
        try:
            than = s._doc(oid, kieu)
        except SuKien as e:
            if not str(e).startswith(_CHUNG):
                s.loi[k] = str(e)
            raise
        s.memo[k] = than
        return than

    def _doc(s, oid, kieu):
        if s.chet:
            raise SuKien("E_reader_chet: da ket thuc")
        if s.het_tong:
            raise SuKien("E_ngan_sach: tong byte")
        try:
            os.write(s.p.stdin.fileno(), oid.encode("ascii") + b"\n")  # không qua bộ đệm: đóng ống không còn byte chờ flush
            dau = s.ra.readline()
        except (OSError, ValueError) as e:
            s._chet(repr(e))
        m = _DAU.fullmatch(dau)
        if not m:
            s._chet(f"dong dau sai dang {dau[:60]!r}")
        if m[4]:
            raise SuKien(f"E_vang: {oid}" if m[1] == oid.encode() else f"E_framing_lech: {oid} -> {m[1].decode()}")
        loai, n = m[2].decode(), int(m[3])
        s.so_object += 1  # mọi phản hồi có thân, không chỉ đường thành công (F2)
        vuot = ("E_ngan_sach: max_object_bytes" if n > s.ns["max_object_bytes"]
                else "E_ngan_sach: tong byte" if s.tong_bytes + n > s.ns["max_tong_bytes"] else None)
        than = s._lay(n, vuot is None)
        if s._lay(1, dem=False) != b"\n":
            s._chet("thieu LF cuoi")
        if vuot:
            s.het_tong = s.het_tong or vuot.endswith("tong byte")
            raise SuKien(f"{vuot}: {oid} {n} B")
        if m[1] != oid.encode():
            raise SuKien(f"E_framing_lech: {oid} -> {m[1].decode()}")
        if hashlib.sha1(f"{loai} {n}\0".encode("ascii") + than).hexdigest() != oid:
            raise SuKien(f"E_bam_lech: {oid}")
        if loai != kieu:
            raise SuKien(f"E_kieu_sai: {oid} la {loai}, mong doi {kieu}")
        return than

    def commit(s, oid):
        """Chép đúng producer `KhoObject.commit`: (c1) dòng `tree` vắng/không SHA40; (c2) `parent` không SHA40."""
        tree, cha = None, []
        for d in s.doc(oid, "commit").partition(b"\n\n")[0].decode("utf-8", "replace").splitlines():
            if d.startswith("tree "):
                tree = d[5:].strip()
            elif d.startswith("parent "):
                cha.append(d[7:].strip())
        if not tree or not _H40.fullmatch(tree):
            raise SuKien(f"E_hong: c1 {oid}")
        if any(not _H40.fullmatch(c) for c in cha):
            raise SuKien(f"E_hong: c2 {oid}")
        return tree, cha

    def tree(s, oid):
        """Chép đúng producer `KhoObject.tree`: tập chốt t1–t10 (§2.3), không thêm, không bớt."""
        b, i, ket = s.doc(oid, "tree"), 0, {}
        while i < len(b):
            j = b.find(b"\0", i)
            if j < 0 or j + 21 > len(b):
                raise SuKien(f"E_hong: t1 {oid}")
            mode_b, sep, ten_b = b[i:j].partition(b" ")
            mode = mode_b.decode("ascii", "replace")
            if not sep:
                raise SuKien(f"E_hong: t2 {oid}")
            if mode not in MODE:
                raise SuKien(f"E_hong: t3 {oid}")
            try:
                ten = ten_b.decode("utf-8")
            except UnicodeDecodeError:
                raise SuKien(f"E_hong: t4 {oid}") from None
            for t, sai in (("t5", not ten), ("t6", ten == "."), ("t7", ten == ".."), ("t8", "/" in ten), ("t9", ten == ".git"),
                           ("t10", ten in ket)):
                if sai:
                    raise SuKien(f"E_hong: {t} {oid}")
            ket[ten] = (mode, b[j + 1:j + 21].hex())
            i = j + 21
        return ket

    def tim(s, tree_oid, duong):
        """("co", mode, oid) | ("vang",) | ("khong_tree", mode): resolve theo entry đã băm, không đọc object entry cuối."""
        phan = duong.split("/")
        for i, p in enumerate(phan):
            e = s.tree(tree_oid).get(p)
            if e is None:
                return ("vang",)
            if i == len(phan) - 1:
                return ("co",) + e
            if e[0] != "40000":
                return ("khong_tree", e[0])
            tree_oid = e[1]

    def _dem(s, dem):
        if dem > s.ns["max_commit_moi_phep_di"]:
            raise SuKien(f"E_ngan_sach: > {s.ns['max_commit_moi_phep_di']} commit/phep di")

    def g1(s, master, c):
        x, gap, dem = master, False, 0
        while True:
            gap = gap or x == c
            if x == MOC:
                return gap, "gap MOC ma chua gap C"
            dem += 1
            s._dem(dem)
            cha = s.commit(x)[1]
            if not cha:
                return False, "het chuoi first-parent ma khong gap MOC"
            x = cha[0]

    def to_tien(s, duoi, tren):
        """`duoi` ≤ `tren` theo MỌI parent; không dùng ngày, độ sâu hay commit-graph."""
        if duoi == tren:
            return True, ""
        ngan, tham = [tren], set()
        while ngan:
            x = ngan.pop()
            if x in tham:
                continue
            tham.add(x)
            s._dem(len(tham))
            for c in s.commit(x)[1]:
                if c == duoi:
                    return True, ""
                ngan.append(c)
        return False, "khong phai to tien"

    def g6(s, S, oid_s):
        e = s.tim(s.commit(S)[0], DUONG_BK)  # mô phỏng producer: mode bất kỳ, KHÔNG đọc object của entry
        if e[0] == "khong_tree":
            return False, f"to tien mode {e[1]} khong phai tree"
        return (oid_s is None, "vang ma receipt khai OID") if e[0] == "vang" else (oid_s == e[2], f"entry {e[1]} {e[2]}")

    def g7(s, C, oid, duong=DUONG_BK, sha=None):
        e = s.tim(s.commit(C)[0], duong)  # thứ tự cố định: resolve -> mode -> so OID -> đọc blob (r3, F6)
        if e[0] != "co" or e[1] not in NHAN:
            return False, f"entry {e}"
        if e[2] != oid:
            return False, f"OID entry {e[2]} khac receipt"
        b = s.doc(oid, "blob")
        return sha is None or hashlib.sha256(b).hexdigest() == sha, "sha256 noi dung lech"


def kiem_git(raw, *, kho, nhanh, base_hien_hanh, head_hien_hanh, master, goc_kho, ngan_sach=None, _seam=None):
    seam, ns = _seam or {}, {**NGAN_SACH, **(ngan_sach or {})}
    luat, ly_do, dd = dict.fromkeys(LUAT, "khong_chay"), [], {"so_object": 0, "tong_bytes": 0}

    def ghi(g, tt, ly=""):
        luat[g] = tt
        if tt != "qua":
            ly_do.append(f"{g}: {ly}")
    if len(raw) > TRAN_RECEIPT:
        ghi("G0", "do", f"receipt {len(raw)} B > {TRAN_RECEIPT}")
        return {"ok": False, "json": None, "git": {"luat": luat, "ly_do": ly_do}, "do_dac": dd}
    ghi("G0", "qua")
    j = C1A1A.kiem_json(raw, kho=kho, nhanh=nhanh, base_hien_hanh=base_hien_hanh, head_hien_hanh=head_hien_hanh)
    if j["luat"]["K1"] != "do" and j["luat"]["K2"] != "do":
        r = json.loads(raw.decode("utf-8"))
        S, H, C = r["S"], r["H"], r["checkout_commit"]
        d, hook = Doc(goc_kho, ns, seam), seam.get("sau_luat", lambda g, d: None)

        def g9():
            seam.get("truoc_g9", lambda: None)()
            v = doc_ref(goc_kho, nhanh, timeout=min(60.0, max(d.han - d.dong_ho(), 0.001)))  # I/O ref theo phần hạn còn lại
            if v != master:
                raise SuKien(f"E_troi_ref: {v} != {master}")
            return True, ""
        try:
            hook("G0", d)
            for g, f in (("G1", lambda: d.g1(master, C)), ("G2", lambda: d.to_tien(S, C)), ("G3", lambda: d.to_tien(S, H)),
                         ("G4", lambda: (d.commit(H)[0] == r["T"], "tree(H) != T")),
                         ("G5", lambda: (d.commit(S)[0] == r["tree_S"], "tree(S) != tree_S")),
                         ("G6", lambda: d.g6(S, r["oid_bo_kiem_tai_S"])), ("G7", lambda: d.g7(C, r["oid_bo_kiem_da_chay"])),
                         ("G8", lambda: d.g7(C, r["workflow_definition_blob"], DUONG_WF, r["workflow_definition_sha256"])),
                         ("G9", g9)):
                try:  # F1: deadline ở ĐẦU và CUỐI mỗi luật — kể cả nhánh không đọc object và kết quả vừa tính xong
                    d.kiem_han()
                    dat, ly = f()
                    d.kiem_han()
                except SuKien as e:
                    ghi(g, "khong_do_duoc", str(e))
                else:
                    ghi(g, "qua" if dat else "do", ly)
                hook(g, d)
        finally:
            d.dong()
        dd = {"so_object": d.so_object, "tong_bytes": d.tong_bytes}
    ok = j["ok"] is True and all(v == "qua" for v in luat.values())
    return {"ok": ok, "json": j, "git": {"luat": luat, "ly_do": ly_do}, "do_dac": dd}


def main(argv=None):
    p = argparse.ArgumentParser(prog="doc_receipt_thu_hoi_git.py")
    k = p.add_subparsers(dest="lenh", required=True).add_parser("kiem-git")
    for ten in ("--receipt", "--kho", "--nhanh-mac-dinh", "--base-hien-hanh", "--head-hien-hanh", "--master", "--goc-kho"):
        k.add_argument(ten, required=True)
    a = p.parse_args(argv)

    def sai(ly):
        print(f"tham so sai: {ly}", file=sys.stderr)
        return 2
    nh = a.nhanh_mac_dinh
    if not a.kho or not nh:
        return sai("--kho/--nhanh-mac-dinh rong")
    if not re.fullmatch(r"[A-Za-z0-9._-]+", nh) or nh.startswith("-"):
        return sai("--nhanh-mac-dinh sai mau")
    if subprocess.run(["git", "check-ref-format", f"refs/heads/{nh}"], capture_output=True, env=_env()).returncode:
        return sai("--nhanh-mac-dinh khong qua check-ref-format")
    for ten in ("base_hien_hanh", "head_hien_hanh", "master"):
        if not _H40.fullmatch(getattr(a, ten)):
            return sai(f"--{ten.replace('_', '-')} phai la hex thuong 40 ky tu")
    if not os.path.isdir(a.goc_kho) or _git(a.goc_kho, "rev-parse", "--git-dir").returncode:
        return sai("--goc-kho khong phai kho git")
    if doc_ref(a.goc_kho, nh) != a.master:
        return sai(f"N6 ban dau: refs/remotes/origin/{nh} khong bang --master")
    try:
        with open(a.receipt, "rb") as f:
            raw = f.read(TRAN_RECEIPT + 1)
    except OSError as e:
        return sai(f"khong doc duoc receipt: {e}")
    kq = kiem_git(raw, kho=a.kho, nhanh=nh, base_hien_hanh=a.base_hien_hanh, head_hien_hanh=a.head_hien_hanh,
                  master=a.master, goc_kho=a.goc_kho)
    sys.stdout.buffer.write((json.dumps(kq, ensure_ascii=True, sort_keys=True) + "\n").encode("ascii"))
    sys.stdout.buffer.flush()
    return ma_thoat(kq)


def ma_thoat(kq):
    """§2.2, xét theo thứ tự: 12 (JSON đỏ hoặc có G `do`) trước 13 (chỉ `khong_do_duoc`); 2 chỉ sinh ở `main`."""
    tt = set(kq["git"]["luat"].values())
    if kq["json"] is None or kq["json"]["ok"] is not True or "do" in tt:
        return 12
    return 13 if "khong_do_duoc" in tt else 0


if __name__ == "__main__":
    sys.exit(main())
