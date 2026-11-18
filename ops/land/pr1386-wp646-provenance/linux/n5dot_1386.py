"""Do THAT dot bien bat buoc cua N5 (#646, spec LEASE-TRUONG-KHAI-NGHIA-r1 §4 N5): noi phep so tu "bang" (`vung!=ky_vong`)
thanh "chua" (`ky_vong not in vung`) => nam ca am phai doi tu rc 1 sang rc 0; ban sach phai rc 1 voi ca nam.
Dung: python -X utf8 -B n5dot_1386.py <clone_day_du_lich_su> <M> <n5.py>
Doi chung: blob docs/PROTOCOL_DA_PHIEN.md tai M => n5 sach rc 0, n5 noi rc 0. Nam ca am (moi ca doi MOT thu tren blob M, moi cap
tim/thay khop DUNG MOT cho): boc rao quanh khoi; them cau khong ten truong trong vung; them cau dao nghia trong vung;
dong trong thua o cuoi vung; cau them sat truoc "Lease `role: reviewer`"."""
import json, pathlib, subprocess, sys, tempfile
SRC, M, N5 = pathlib.Path(sys.argv[1]), sys.argv[2], pathlib.Path(sys.argv[3])
blob = subprocess.run(["git", "-C", str(SRC), "show", f"{M}:docs/PROTOCOL_DA_PHIEN.md"], capture_output=True, check=True).stdout
sach = N5.read_bytes()
CU, MOI = b"if vung!=ky_vong: chet(", b"if ky_vong not in vung: chet("
assert sach.count(CU) == 1, "mau so sanh khong khop dung mot cho"
noi = sach.replace(CU, MOI)
M1 = "`heartbeat_at` là lời khai: trong kho không có cổng nào đọc trực tiếp trường này.".encode()
M7 = "`record-review` so `--reviewed-sha` với head đã ghi khi vào `reviewing`.".encode()
RV = "\nLease `role: reviewer`".encode()
CA = {
    "boc_rao": (b"\n" + M1, b"\n```text\n" + M1),
    "them_cau_khong_ten_truong": (M7 + b"\n", M7 + "\n\nCâu thêm không nhắc tên trường nào.\n".encode()),
    "them_cau_dao_nghia": (M7 + b"\n", M7 + "\n\nMọi cổng đều đọc trực tiếp trường lời khai.\n".encode()),
    # dong trong thua o CUOI vung dich (sat truoc doan reviewer); chen giua hai menh de thi pha luon chuoi con => ca hai ban cung do
    "dong_trong_thua": (M7 + b"\n" + RV, M7 + b"\n\n" + RV),
    "cau_sat_truoc_role_reviewer": (RV, "\nCâu thêm sát trước.\n".encode() + RV),
}


def chay(script, du_lieu, d):
    s, f = d / "n5.py", d / "PROTOCOL.md"
    s.write_bytes(script)
    f.write_bytes(du_lieu)
    p = subprocess.run([sys.executable, "-X", "utf8", "-B", str(s), str(f)], capture_output=True, text=True)
    return {"rc": p.returncode, "out": (p.stdout + p.stderr).strip()[-200:]}


bao = {"M": M, "n5_sha256_sach": __import__("hashlib").sha256(sach).hexdigest(), "doi_chung": {}, "ca_am": {}}
with tempfile.TemporaryDirectory() as tmp:
    d = pathlib.Path(tmp)
    bao["doi_chung"] = {"sach": chay(sach, blob, d), "noi": chay(noi, blob, d)}
    for ten, (tim, thay) in CA.items():
        if blob.count(tim) != 1:
            bao["ca_am"][ten] = {"ket_qua": f"KHONG_DO: mau khop {blob.count(tim)} lan"}
            continue
        b2 = blob.replace(tim, thay)
        a, b = chay(sach, b2, d), chay(noi, b2, d)
        bao["ca_am"][ten] = {"sach": a, "noi": b, "ket_qua": "DOT_BIEN_LO_RANG" if (a["rc"] == 1 and b["rc"] == 0) else "KHONG_PHAN_BIET"}
ok = (bao["doi_chung"]["sach"]["rc"] == 0 and bao["doi_chung"]["noi"]["rc"] == 0
      and all(v.get("ket_qua") == "DOT_BIEN_LO_RANG" for v in bao["ca_am"].values()))
bao["TONG"] = "DAT" if ok else "KHONG_DAT"
print(json.dumps(bao, ensure_ascii=False, indent=1))
sys.exit(0 if ok else 1)
