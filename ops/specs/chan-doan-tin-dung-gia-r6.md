# CHAN-DOAN-TIN-DUNG-GIA — revision 6

Goi #568. Revision nay MO CLOSURE sang **bo cham cua chinh bo tu kiem**
(`chay_dot_bien_tu_kiem`), sau khi BON luot cross-review doc lap tren codex
deu tra `changes_requested` voi CUNG mot P1, va executor TAI LAP duoc no tren
bo cham THAT.

## 1. Benh

Bo cham cap `GIET` cho mot dot bien khi va chi khi:

    do_khac rong  VA  p.returncode == 1  VA  do_chot == set(dich)

CA BA dieu kien deu doc tu **van ban con in ra**. Khong dieu kien nao chung to
con DA THUC SU CHAY mot ca nao. Do duoc tren bo cham that, tien trinh con that,
ban sao tep that — ba dot bien MOT CHUOI, moi cai them mot dong in gia roi chet
o MUC MODULE:

    gia-mao-thoat-he-thong | r515 | 1/1     (raise SystemExit(1))
    gia-mao-chia-khong     | r515 | 1/1     (1/0)
    gia-mao-thoat-cung     | r515 | 1/1     (os._exit(1))

    (giet, hong) = (3, 0)

KHONG ca nao chay. Ca ba deu duoc cong nhan la "dot bien bi giet dung dich".

Lap luan CU cua executor — "`rc=1` chi den tu mot ca hong THAT, ma ca hong that
thi lot vao `do_chot`" — SAI. Ngoai le o muc module cung cho `rc=1`; `SystemExit`
khong bi `except Exception` bat; `os._exit(1)` di vong qua moi bo chay. Ca ba deu
xay ra TRUOC khi bat ky ca nao chay. Executor da dinh chinh cong khai.

Day la hinh dang `TIN-HIEU-DO-CHINH-MA-TEST-GIA-MAO` lan thu 6, va lan nay no o
TRUNG TAM phep cham chu khong o ria.

## 2. Closure

### M15 — cap `GIET` phai co BANG CHUNG DUONG rang con DA CHAY bo ca

Bo cham KHONG duoc cap `GIET` neu thieu bang chung duong rang tien trinh con da
chay bo ca den HET. "Khong thay dau hieu bat thuong" KHONG phai bang chung.

Bang chung phai KHONG GIA MAO DUOC bang mot chuoi ky tu ma nguoi viet bang dot
bien go san — tuc no phai phu thuoc vao mot gia tri do CHA sinh ra tai luc chay
va truyen cho con, chu khong phai mot hang so nam trong tep.

Thieu bang chung thi trang thai la **KHONG DO DUOC** (trang thai thu ba), lam
cong DO. KHONG duoc lam tron thanh `GIET` lan `hong`.

### M16 — SO HANG phai khop, va lech thi la KHONG DO DUOC

Con in mot dong tong ket mang so ca DAT tren tong so ca. So ca hong doc duoc tu
dong ay phai BANG DUNG so khoi chan doan (`DO_CHOT` + `DO_KHAC`) ma cha trich
duoc. Lech la mot mau thuan trong chinh bao cao cua con, va mau thuan thi khong
duoc quy ve mot trong hai phia: no la **KHONG DO DUOC**.

Tong so ca con khai cung phai bang so ca cha biet. Con chay mot bo ca KHAC voi
bo cha dang do thi moi con so deu vo nghia.

## 3. Tieu chi nghiem thu

- **A37** — ba dot bien phan chung cua muc 1 (`SystemExit`, loi tinh, `os._exit`)
  PHAI khong con duoc cap `GIET`. Moi cai mot muc RIENG trong bang, phan biet
  duoc bang dau vao. Do bang bo cham THAT, tien trinh con THAT.
- **A38** — dau vao BINH THUONG (dot bien that, ca that do dung dich) PHAI van
  duoc cap `GIET` y nhu truoc. Thieu chieu nay thi mot trien khai luon tra
  KHONG DO DUOC cung se xanh o A37.
- **A39** — bang chung cua M15 phai do duoc la KHONG GIA MAO DUOC: mot dot bien
  in DUNG dinh dang bang chung nhung voi gia tri TU NGHI ra PHAI khong duoc cap
  `GIET`. Ca nay phai phan biet duoc voi A37 bang dau vao.
- **A40** — lech so hang (M16) PHAI cho `KHONG DO DUOC`, KHONG phai `GIET` va
  KHONG phai `hong` im lang. Hai chieu: lech thi do, khop thi khong.
- **A41** — moi duong moi phai co dot bien RIENG canh. Hai dot bien khong phan
  biet duoc bang dau vao la bo TUONG DUONG va khong duoc tinh.
- **A42** — luot day du phai xanh voi hai so BANG NHAU, va so muc bang dot bien
  phai tang dung bang so muc them vao. Do delta HAI PHIA trong MOT lenh.
- **A43** — `stderr` cua luot day du phai la 0 B. Mot dong canh bao cung an mat
  ngan sach chan doan, va do la benh goi nay sinh ra de chua.

## 4. KHONG HUA GI

- **Khong chua duong "con da bao chot roi chet tiep".** Van ngoai pham vi, y het
  r5. Chua no doi dinh dang dau ra ma r516/r524/r530 dang do.
- **Khong dung vao `r509`** (`CHOT-CAM-THU-DAC-TA-KHONG-DOI` lan 2) — thuoc #593.
- **Khong dung vao lop `TIEN-DE-CA-LONG-HONG-BI-DOI-THANH-CHOT`** (`r528` gom moi
  `BaseException`; 2000 loi ha tang thanh MOT chot) — thuoc #593.
- **Khong chua `stderr[-200:]`** cat ma khong khai luong mat — no rieng, con mo.
- **Khong doi huong cat** cua `_goi_chan_doan`.
- **Khong dung vao co che lease.** No rieng, issue #599.

## 5. Hinh dang ke thua — dem den luc mo r6

    LOI-KHAI-RONG-HON-PHEP-DO                     9
    TIN-HIEU-DO-CHINH-MA-TEST-GIA-MAO             6
    VA-DUNG-CHO-DUOC-CHI-ROI-BO-SOT-DUONG-THU-BA  2
    CHOT-CAM-THU-DAC-TA-KHONG-DOI                 2
    BO-TUONG-DUONG-DO-CHINH-EXECUTOR-DUNG         2

Ba hinh dang dau deu da vuot nguong BA lan cua CLAUDE.md. Chu kho da duoc bao
va van chi thi chay tiep; ghi lai o day de khong ai doc nham la chua ai biet.

**Bai hoc dat nhat cua r5, chep sang day:** va HEP khong re hon. Luot 1 chi siet
MOT ho tien to; luot 2 phai quay lai siet ba ho con lai VA sua mot lo hong do
chinh ban va hep ay de ra. Luot 3 dung tien to DAI HON; luot 4 phai thay bang
NGU PHAP DAY DU. **Dong ca LOP, dung dong mot diem.**
