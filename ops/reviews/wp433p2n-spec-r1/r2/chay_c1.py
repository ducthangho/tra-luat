"""Chay fragment C1 (wp433_gws_cred_win_duong) voi bien the duoc chon tren cay chon, moi lan mot tien trinh. argv: cay bien_the(goc|moi|chan) nhan"""
import importlib.util, shutil, sys, os, hashlib
RIG, CAY, BT, NHAN = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
sp = importlib.util.spec_from_file_location("rig", RIG); rig = importlib.util.module_from_spec(sp); sp.loader.exec_module(rig)
dich = os.path.join(CAY, "scripts", "test_fragments", "wp433_gws_cred_win_duong.py")
nguon = os.path.join(os.path.dirname(os.path.abspath(__file__)), "c1_%s.py" % BT)
shutil.copyfile(nguon, dich)
print("=== %s cay=%s bien_the=%s sha=%s" % (NHAN, CAY, BT, hashlib.sha256(open(dich, "rb").read()).hexdigest()[:16]))
kq, ra = rig.chay_fr(CAY, "wp433_gws_cred_win_duong")
print("run=%r" % (kq,)); print(ra)
