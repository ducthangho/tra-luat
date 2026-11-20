# probe_db2.py - tu chua, khong can kho. Tai hien luot W5.bit cua N1 duoi dot bien 2 (ve thuoc tinh thanh "!= 0").
import os, stat, tempfile, types
T = os.path.realpath(tempfile.mkdtemp(prefix="wp433r-probe-")); T = T[:1].upper() + T[1:]
cfg = os.path.join(T, "cfg"); os.makedirs(cfg)
o, duoi = os.path.splitdrive(cfg); goc = o + os.sep; tp = tuple(t for t in duoi.split(os.sep) if t) + ("credentials.json",)
that = os.lstat
def ls(q):   # bo boc cua N1: DUNG mot duong (cfg) nhan bit 1024, duong khac di ham that
    return types.SimpleNamespace(st_mode=stat.S_IFDIR | 0o700, st_file_attributes=1024) if os.path.normcase(os.path.normpath(q)) == os.path.normcase(cfg) else that(q)
def vong(ve):  # vong tien to cua _kiem_dich_ghi (M1), ve thuoc tinh thay duoc
    for i in range(len(tp) + 1):
        tien_to = os.path.join(goc, *tp[:i])
        try:
            st = ls(tien_to)
            if stat.S_ISLNK(st.st_mode) or ve(getattr(st, "st_file_attributes", 0)):
                return tien_to
        except (FileNotFoundError, NotADirectoryError):
            pass
print("os.name=%s attr(goc)=%r attr(T)=%r" % (os.name, getattr(that(goc), "st_file_attributes", None), getattr(that(T), "st_file_attributes", None)))
a, b = vong(lambda x: x & 1024), vong(lambda x: x != 0)
print("candidate chan tai: %r (ky vong cfg: %s)" % (a, a == cfg))
print("dot bien 2 chan tai: %r (== cfg: %s)" % (b, b == cfg))
print("KET LUAN:", "dot bien 2 chet SAI LUOT o W5.bit (TIN_DUNG_GIA)" if a == cfg and b != cfg else "dot bien 2 KHONG chet o W5.bit (du doan cua executor SAI)" if a == cfg else "probe hong")
os.rmdir(cfg); os.rmdir(T)
