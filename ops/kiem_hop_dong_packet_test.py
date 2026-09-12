#!/usr/bin/env python3
"""Phan chung cho `ops/kiem_hop_dong_packet.py`. Mot cong chua ai do la mot cong khong
ton tai; va mot cong tu viet la thu de tin nhat nen nguy nhat — nen hoi no nhung ca da
biet truoc dap an, ca DUONG lan ca AM."""
import hashlib, pathlib, subprocess, sys, tempfile

HERE = pathlib.Path(__file__).resolve().parent
CONG = HERE / "kiem_hop_dong_packet.py"

SPEC_OK = """# Đặc tả packet — X (revision 7)

- `packet_id`: **X**
- `revision`: **7** · `generation`: 1

**A8 (toàn packet).** `git diff --numstat` chỉ hiện đúng **2** đường dẫn, cột
`additions` ≤ **430** (ngoại lệ CÓ PHẠM VI).
"""
LEASE_OK = """schema_version: 2
revision: 7
spec_hash: {h}
viec_trong_lease:
  - 'A8 — đúng 2 đường dẫn; trần dòng thêm theo `A8` của đặc tả đã ghim bằng `spec_hash`.'
  - 'M1 — tách job, giữ nguyên ma trận nền.'
dieu_kien_dung:
  - 'Vượt trần `A8` của đặc tả ⇒ DỪNG và hỏi chủ kho.'
  - 'Viết cú pháp biểu thức trong comment của run — kho đã bị từ chối (run 31971137920).'
run_minutes: 1440
"""

def chay(spec_van, lease_van, sua_hash=True):
    with tempfile.TemporaryDirectory() as d:
        g = pathlib.Path(d)
        sp = g / "spec.md"; sp.write_text(spec_van, encoding="utf-8")
        h = hashlib.sha256(sp.read_bytes()).hexdigest() if sua_hash else "0" * 64
        lp = g / "lease.yaml"; lp.write_text(lease_van.replace("{h}", h), encoding="utf-8")
        p = subprocess.run([sys.executable, str(CONG), "--spec", str(sp), "--lease", str(lp)],
                           text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        return p.returncode, p.stdout

CA = [
    ("t1-cap-khop-phai-DAT", SPEC_OK, LEASE_OK, True, 0),
    ("t2-revision-truong-lech-tieu-de",
     SPEC_OK.replace("- `revision`: **7**", "- `revision`: **5**"), LEASE_OK, True, 2),
    ("t3-dac-ta-neu-tran-HAI-lan",
     SPEC_OK + "\nNhac lai: `additions` ≤ **430**.\n", LEASE_OK, True, 3),
    ("t4-lease-CHEP-nguong-vao-muc-A8", SPEC_OK,
     LEASE_OK.replace("trần dòng thêm theo `A8` của đặc tả đã ghim bằng `spec_hash`",
                      "cột `additions` ≤ 400"), True, 4),
    ("t5-spec_hash-khong-khop", SPEC_OK, LEASE_OK, False, 5),
    ("t6-thieu-truong-revision-o-lease", SPEC_OK,
     LEASE_OK.replace("revision: 7\n", ""), True, 6),
    # ── ca AM: tham chieu KHONG duoc tinh la nguong (chong duong tinh gia) ──────
    ("t8-dinh-danh-ADR-KHONG-bi-bat", SPEC_OK,
     LEASE_OK.replace("- 'A8 — đúng 2 đường dẫn;",
                      "- 'A8 — đúng 2 đường dẫn; KHÔNG đổi ADR-0044;"), True, 0),
    # Chot cho chinh lan noi danh sach CHO PHEP o tren: dinh danh duoc tha, nhung mot
    # NGUONG THAT nam trong CUNG mot muc thi VAN phai bi bat — noi khong duoc nuot nguong.
    ("t9-ADR-tha-nhung-nguong-cung-muc-VAN-bi-bat", SPEC_OK,
     LEASE_OK.replace("trần dòng thêm theo `A8` của đặc tả đã ghim bằng `spec_hash`",
                      "KHÔNG đổi ADR-0044, cột `additions` ≤ 400"), True, 4),
    # `R6-F03` — tham chieu va nguong CUNG mot gia tri: tha lan xuat hien la dinh danh,
    # nhung lan sau dau `≤` VAN phai bi bat. Ban tru theo GIA TRI tha ca hai.
    ("t10-tham-chieu-cung-so-voi-nguong", SPEC_OK,
     LEASE_OK.replace("trần dòng thêm theo `A8` của đặc tả đã ghim bằng `spec_hash`",
                      "căn cứ Issue #400, cột `additions` ≤ 400"), True, 4),
    # `R6-F04` — vi pham chi nam trong `dieu_kien_dung`, khoi kia SACH: neu khoi ay khong
    # duoc quet thi ca nay xanh, va do dung la ca thieu ma reviewer bat duoc.
    ("t11-vi-pham-CHI-o-dieu_kien_dung", SPEC_OK,
     LEASE_OK.replace("  - 'Vượt trần `A8` của đặc tả ⇒ DỪNG và hỏi chủ kho.'",
                      "  - 'A8 — vượt 400 dòng thêm ⇒ DỪNG và hỏi chủ kho.'"), True, 4),
    ("t7-tham-chieu-trong-muc-A8-KHONG-bi-bat", SPEC_OK,
     LEASE_OK.replace("- 'A8 — đúng 2 đường dẫn;",
                      "- 'A8 — căn cứ Issue #463, comment 5645742072, run 34680281474;"), True, 0),
]

def main():
    hong = []
    for ten, sp, lp, h, mong in CA:
        rc, out = chay(sp, lp, h)
        ok = rc == mong
        hong += [] if ok else [ten]
        print(f"{'ĐẠT ' if ok else 'HỎNG'}  {ten:44s} rc={rc} (mong {mong})")
        if not ok:
            print("      " + out.strip().replace("\n", "\n      ")[:400])

    # ── DOT BIEN vao CHINH bo canh: noi danh sach CHO PHEP de nuot mot nguong ────
    # Doctrine: "dot bien noi danh sach cho phep de chua ten tan cong phai lam ca dich DO".
    # Khong co dot bien nay thi khong biet t4 dang do DANH SACH hay do thu khac.
    # Dinh vi khoi THAM_CHIEU bang HAI MOC thay vi mot chuoi nguyen van: mau regex se con
    # duoc sua, va mot dot bien mat mo neo la mot dot bien khong chay (bai hoc "ca co MAT
    # khac ca co DO"). Neu khong dinh vi duoc thi BAO HONG, khong im lang bo qua.
    goc = CONG.read_text(encoding="utf-8")
    mo, dong = "THAM_CHIEU = re.compile(", "re.I)"
    i = goc.find(mo)
    j = goc.find(dong, i) + len(dong) if i >= 0 else -1
    if i < 0 or j <= i:
        print("HỎNG  dot-bien-noi-danh-sach: khong dinh vi duoc khoi THAM_CHIEU")
        hong.append("dot-bien-noi-danh-sach")
    else:
        CONG.write_text(goc[:i] + 'THAM_CHIEU = re.compile(r"(\\d{3,})", re.I)' + goc[j:],
                        encoding="utf-8")
        try:
            rc, _ = chay(SPEC_OK,
                         LEASE_OK.replace("trần dòng thêm theo `A8` của đặc tả đã ghim bằng `spec_hash`",
                                          "cột `additions` ≤ 400"), True)
        finally:
            CONG.write_text(goc, encoding="utf-8")
        ok = rc != 4
        hong += [] if ok else ["dot-bien-noi-danh-sach"]
        print(f"{'ĐẠT ' if ok else 'HỎNG'}  {'dot-bien-noi-danh-sach-CHO-PHEP':44s} rc={rc} "
              f"(nới danh sách ⇒ t4 phải THÔI đỏ; nếu vẫn 4 thì t4 đang đo thứ khác)")
    # DOT BIEN 2 (`R6-F04`): bo mot phan tu khoi `KHOI_NGHIA_VU` — chot 5 phai bat.
    goc2 = CONG.read_text(encoding="utf-8")
    cu2 = 'KHOI_NGHIA_VU = ("viec_trong_lease", "dieu_kien_dung")\n#'
    if goc2.count(cu2) != 1:
        print("HỎNG  dot-bien-bo-khoi-nghia-vu: khong dinh vi duoc"); hong.append("dot-bien-bo-khoi")
    else:
        CONG.write_text(goc2.replace(cu2, 'KHOI_NGHIA_VU = ("viec_trong_lease",)\n#', 1),
                        encoding="utf-8")
        try:
            rc, out = chay(SPEC_OK, LEASE_OK, True)
        finally:
            CONG.write_text(goc2, encoding="utf-8")
        ok = rc == 4 and "KHOI_NGHIA_VU" in out
        hong += [] if ok else ["dot-bien-bo-khoi"]
        print(f"{'ĐẠT ' if ok else 'HỎNG'}  {'dot-bien-bo-khoi-nghia-vu':44s} rc={rc} "
              f"(bo mot khoi ⇒ chot 5 phai CHAN [4])")
    print(f"\nPHẢN CHỨNG CỔNG: {len(CA) + 2 - len(hong)}/{len(CA) + 2} đạt"
          + (f" · HỎNG: {hong}" if hong else ""))
    return 1 if hong else 0

if __name__ == "__main__":
    sys.exit(main())
