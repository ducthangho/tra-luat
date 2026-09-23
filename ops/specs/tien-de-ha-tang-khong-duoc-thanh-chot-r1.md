# TIEN-DE-HA-TANG-KHONG-DUOC-THANH-CHOT — revision 1

Goi #593. Tep: `ops/nhanh_don_duoc_test.py`.

## 1. Lop benh

**Vi ngu (kiem duoc):** moi cho mot ca NGOAI dung ket qua cua mot ca LONG lam
chot, ma KHONG phan biet duoc *loi tien de ha tang* voi *vi pham thuoc tinh dang
thu*.

Hai thu ay doi hai cach xu KHAC NHAU va phai ra HAI trang thai khac nhau:

| nguon do | y nghia | trang thai dung |
|---|---|---|
| thuoc tinh SAI | dung thu ma kho dang chua | `DO_CHOT` |
| tien de ha tang hong (dia day, het fd, het quyen) | KHONG DO DUOC gi ca | trang thai THU BA |

Gop chung la cap `TIN DUNG GIA` o muc CA — dung benh #568 vua dong o muc BO CHAM,
nay o mot tang thap hon. Va no xoa mat nguyen nhan: nguoi doc log thay "chot that
bai" trong khi thuc te la dia day.

## 2. Phep do da co, tai lap duoc

Tren `master` tai `18d42ca`, voi `_kenh_tam` bi lam hong bang `OSError(28)`:

    so loi HA TANG bi nuot : 2000
    cha nhan duoc          : TinHieuChotCa: 'chot cua ca r528 that bai'
    nguyen nhan 'dia day'  : KHONG con trong thong bao

Doi chung DUONG, cung bo do ga, KHONG tiem loi:

    r528 DAT (1,2 s), va chot (c1) `dem["n"] == 2000` DAT
    => vong 2000 luot THAT SU chay du; bo do ga khong tu gay ra loi

Hai chieu phan biet duoc, nen ket luan khong rong.

Ma gay ra, `ops/nhanh_don_duoc_test.py:~2670`:

    for i in range(N508):
        ...
        try:
            m.r508_ban_ghi_luot_TRUOC_chi_khac_dau_phien(thu)
        except BaseException:          # nuot moi thu, ke ca loi HA TANG
            do += 1
    chot(do == 0, "r528")

## 3. Closure

### M1 — tach NGUON DO, va tien de hong phai ra trang thai THU BA

Vong `(c2)` cua `r528` phai phan biet:

- ngoai le den TU CHOT cua ca long (`TinHieuChotCa`) => dem vao `do`, dung nhu nay;
- ngoai le ha tang (`OSError` va ho hang cua no khi phong/ghi) => KHONG duoc dem
  vao `do`, ma phai lam ca nay ra **KHONG DO DUOC**, mang theo NGUYEN NHAN;
- ngoai le khac (loi lap trinh: `NameError`, `TypeError`, ...) => KHONG duoc nuot.
  Mot vo qua rong bien loi lap trinh thanh mot con so, va do la cho mu.

Bat HEP theo loai. KHONG dung `except BaseException`, va KHONG dung
`except Exception` tran o cho nay.

### M2 — nguyen nhan phai DEN DUOC nguoi doc

Khi ra KHONG DO DUOC vi tien de, thong bao phai mang: loai ngoai le, thong diep
cua no, va SO LAN da xay ra. "chot cua ca r528 that bai" mot minh la loi khai
RONG hon phep do — no khai mot thuoc tinh sai trong khi khong do duoc thuoc tinh
nao ca.

### M3 — `stderr[-200:]` phai KHAI luong mat

`ops/nhanh_don_duoc_test.py:~649`:

    ly_do = f"{ly_do} | rc_con={p.returncode} | stderr[-200:]={p.stderr[-200:]!r}"

Cat con 200 ky tu CUOI ma khong noi da bo bao nhieu. Cung lop voi `_goi_chan_doan`
(#568 da dong, khai `…[CAT n ky tu]`), khac ham va khac HUONG cat. Phai khai so
ky tu bi bo. KHONG doi huong cat — huong cat o day la CO Y (nguyen nhan that nam
o CUOI stderr) va viec doi no nam ngoai pham vi.

## 4. Tieu chi nghiem thu

- **A1** — tiem `OSError` vao tien de ha tang cua vong `(c2)`: ca PHAI ra
  KHONG DO DUOC, PHAI mang loai + thong diep + so lan, va PHAI KHONG ra `DO_CHOT`.
- **A2** — DOI CHUNG DUONG: khong tiem gi thi `r528` van DAT, va chot `(c1)`
  `dem["n"] == N508` van DAT. Thieu chieu nay thi mot trien khai LUON tra
  KHONG DO DUOC cung se xanh o A1.
- **A3** — ngoai le do CHOT cua ca long nem ra van phai duoc dem vao `do` y nhu
  truoc, va `chot(do == 0)` van phai DO khi co mot lan chap that.
- **A4** — loi LAP TRINH (vd `NameError`) trong ca long KHONG duoc nuot thanh mot
  con so. No phai thoat ra hoac ra KHONG DO DUOC mang ten loai — khong duoc bien
  thanh `do += 1`.
- **A5** — M3: `stderr` dai hon 200 ky tu PHAI sinh mot lo khai so ky tu bi bo;
  `stderr` ngan hon thi KHONG duoc sinh nhan nao. Hai chieu.
- **A6** — moi duong moi phai co dot bien RIENG canh. Hai dot bien khong phan
  biet duoc bang dau vao la bo TUONG DUONG, khong duoc tinh.
- **A7** — luot day du xanh voi hai so BANG NHAU; `stderr` cua luot la 0 B; so
  muc bang dot bien tang dung bang so muc them vao. Do delta HAI PHIA trong MOT
  lenh.

## 5. KHONG HUA GI

- **Khong dung vao `r509`** (`dem["n"] == 2` chi dem `secrets.token_hex`, nen
  `secrets.token_bytes(16).hex()` bi bac du hop dong cho phep) — do la hinh dang
  `CHOT-CAM-THU-DAC-TA-KHONG-DOI`, no RIENG, con mo.
- **Khong quet het chin cho `except Exception`** trong tep. Hai trong so do da tu
  khai `noqa: BLE001` la co y. Goi nay chi dong DUNG lop o muc 1; muon quet het
  thi xin revision rieng, va phai do tung cho chu khong sua hang loat.
- **Khong doi huong cat** cua `stderr[-200:]` hay `_goi_chan_doan`.
- **Khong dung vao co che lease** (no rieng, issue #599).

## 6. Hinh dang ke thua — dem den luc mo goi nay

    LOI-KHAI-RONG-HON-PHEP-DO                     10
    TIN-HIEU-DO-CHINH-MA-TEST-GIA-MAO              6
    VA-DUNG-CHO-DUOC-CHI-ROI-BO-SOT-DUONG-THU-BA   2
    CHOT-CAM-THU-DAC-TA-KHONG-DOI                  2
    BO-TUONG-DUONG-DO-CHINH-EXECUTOR-DUNG          2

LOI-KHAI-RONG len 10: khi do lai `r528` tren master, executor `grep BaseException`
CHI trong 40 dong sau `def r528`, ma vong lap nam o dong thu ~65 — roi khai
"khong thay nua". Mot phep do HEP doc thanh mot ket luan RONG, lan nay o chinh
buoc di tim benh.

**Bai hoc dat nhat cua #568, chep sang day:** va HEP khong re hon. Bay vong cua
r5 cho thay moi lan sieu mot diem thay vi dong ca LOP thi vong sau phai quay lai
dong nhung diem con lai, VA sua lo hong ma ban va hep de ra. **Dong ca LOP.**
