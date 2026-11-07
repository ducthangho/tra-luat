#!/usr/bin/env python3
"""Phép đo profile cho đặc tả wp1179-c1a1b r1 (CHỈ ĐO, không phải verifier).

Đọc commit qua `git cat-file --batch` (GIT_NO_REPLACE_OBJECTS=1), BĂM LẠI từng object, lấy parent/tree từ bytes
đã băm, rồi đo: (1) chuỗi first-parent từ master tới MOC; (2) mọi commit tổ tiên của master (BFS mọi parent)
— trần trên của phép đi ancestry khi S không phải tổ tiên. In số commit, tổng bytes nội dung, giây.
Cách dùng: python do_profile.py <git_dir_goc_kho> <oid_master> <oid_moc>
"""
import hashlib, os, subprocess, sys, time

goc, master, moc = sys.argv[1:4]
env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
env["GIT_NO_REPLACE_OBJECTS"] = "1"
p = subprocess.Popen(["git", "-C", goc, "--no-replace-objects", "cat-file", "--batch"], stdin=subprocess.PIPE,
                     stdout=subprocess.PIPE, env=env)
dem = {"obj": 0, "bytes": 0}


def doc(oid):
    p.stdin.write(oid.encode() + b"\n"); p.stdin.flush()
    dau = p.stdout.readline().split()
    if len(dau) != 3 or dau[0].decode() != oid:
        raise SystemExit(f"framing {dau!r}")
    loai, n = dau[1], int(dau[2])
    than = p.stdout.read(n + 1)[:n]
    if hashlib.sha1(loai + b" " + str(n).encode() + b"\0" + than).hexdigest() != oid:
        raise SystemExit("bam lech " + oid)
    dem["obj"] += 1; dem["bytes"] += n
    return loai.decode(), than


def cha(oid):
    loai, than = doc(oid)
    assert loai == "commit"
    out = []
    for dong in than.split(b"\n\n", 1)[0].split(b"\n"):
        if dong.startswith(b"parent "):
            out.append(dong[7:].decode())
    return out


t = time.monotonic(); x, n = master, 0
while x != moc:
    ps = cha(x); n += 1
    if not ps:
        raise SystemExit("khong gap MOC tren first-parent")
    x = ps[0]
print(f"first_parent master->MOC: {n} commit, {dem['bytes']} byte, {time.monotonic()-t:.3f}s")
dem.update(obj=0, bytes=0); t = time.monotonic(); thay, hang = {master}, [master]
while hang:
    for q in cha(hang.pop()):
        if q not in thay:
            thay.add(q); hang.append(q)
print(f"to_tien(master) moi parent: {len(thay)} commit, {dem['bytes']} byte, {time.monotonic()-t:.3f}s")
