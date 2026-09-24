# TIEN-DE-HA-TANG-KHONG-DUOC-THANH-CHOT — revision 2

Goi #593. Tep: `ops/nhanh_don_duoc_test.py`. Thay revision 1 (`...-r1.md`,
sha256 `bc56d3ee...a2b24d`); r1 dung o head `3eb5bd9` tren `claude/tien-de-ha-tang-r1`.

| truong | gia tri |
|---|---|
| `packet_id` | `TIEN-DE-HA-TANG-KHONG-DUOC-THANH-CHOT` |
| `packet_issue` | 593 |
| `revision` | 2 |
| `review_class` | `sensitive` (cham bo phan hang cua bo cham tu kiem) |
| `write_set` | `ops/nhanh_don_duoc_test.py` — MOT duong |
| `start_from_sha` | `3eb5bd909ef1d64f503e95af09227a43f6498830` (head r1) |
| tran dong them | **450**, DO bang `git diff --numstat 18d42ca -- ops/nhanh_don_duoc_test.py` (ca goi, khong phai rieng r2). Chu kho chi thi 2026-09-24: "Noi tran len 450". Vuot ADR-0044:5 (300) cho class sensitive la NGOAI LE CUA CHU KHO, khong phai nguong moi. |

## 0. Nguon cap viec va chi thi

Chu kho, 2026-09-24, go van xuoi, sau khi executor bao DUNG o
issues/593#issuecomment-5806860890:

> (a) mo revision 2, soan dac ta di, phai dua het cac van de vao de xu ly trong
> revision nay. Noi tran len 450. Sau do thuc thi theo dung quy tac vong lap toi dua ra

Can cu ky thuat: cross-review codex vong 2 (tren `3c0147a`) va vong 3 (tren `3eb5bd9`),
ca hai `changes_requested` P2=2; executor tai lap tung the hien; roi TU QUET ca tep
bang ma tran o §2 — ma tran tim ra NHIEU the hien hon ca hai verdict cong lai.

## 1. Lop benh — vi ngu, KHONG doi so voi r1 §1

Moi cho mot ca NGOAI dung ket qua cua mot ca LONG (hoac cua bo cham) lam chot ma KHONG
phan biet duoc *loi tien de ha tang* voi *vi pham thuoc tinh*. Hai huong hong:

- **(A) ha tang -> CHOT**: loi ha tang bi NUOT thanh mot gia tri, roi chot tren gia tri ay
  do, ra `DO_CHOT` — khai mot thuoc tinh sai trong khi khong do duoc gi.
- **(B) ha tang -> DAT (lam tron LEN)**: loi ha tang bi nuot thanh `KHONG_DO_DUOC`, ma
  gia tri ca CHO lai chinh la `KHONG_DO_DUOC`, nen ca XANH ma khong do gi.

Trang thai dung cho ca hai: **trang thai THU BA** (`KHONG DO DUOC`, o runner la `DO_KHAC`)
mang LOAI + THONG DIEP + SO LAN.

## 2. Phep do — ma tran toan tep (do 2026-09-24T04:39Z tren `3eb5bd9`)

Script ngoai kho (sha256 `040cb028...0803c`): moi ca `TU_KIEM` (44) x nam che do:
`SACH` · `RJ` (doc `.json`/`.jsonl` nem `PermissionError`) · `R2` (chi lan doc THU HAI
cua moi tep `.json/.jsonl` nem) · `W` (ghi vao thu muc tam nem `OSError(28)`) · `M`
(`os.mkdir` nem `OSError(28)`). Don vi dem: **ca** (ten `rXXX`), mot ca dem mot lan moi che do.

| che do | ra CHOT (huong A) | ra DAT du DA tiem (huong B) |
|---|---|---|
| RJ | r501 r503 r504 r505 r509 r510 r512 r515 r516 r517 r518 r519 r520 r521 r523 r525 r530 r539 r542 — **19 ca** | r507, r532 — **2 ca** |
| R2 | r504 r505 r508 r509 r511 r519 r521 r523 r528 r543 — **10 ca** | r515 — **1 ca** |
| W | r501 r505 r509 — **3 ca** | 0 |
| M | r501 — **1 ca** | 11 ca `inj=1` — TAO TAC cua phep do (`mkdir(exist_ok=True)` tren thu muc DA CO), KHONG phai the hien |

Hop (A)+(B), dem theo TEN CA: **26 ca**.
`SACH`: 43/44 DAT; `r526` nem `KeyError` vi script do nap module KHONG dang ky
`sys.modules` — tao tac cua phep do, ca ay ngoai lop (khong co I/O).

Cong them cac the hien reviewer da neu ma ma tran khong tiem toi (loi `mkdir` THAT o tung
nhanh cua `r543`; T2 cua `r501` hong dung thu muc ngoai `run`; phan loai `cho_kdd` theo
TEN kich ban chu khong theo nguon loi).

### Diem nuot — do bang quet AST toan tep (moi `except` bat `OSError`/`Exception`)

| dong (tren `3eb5bd9`) | ham | hanh vi voi `OSError` |
|---|---|---|
| 156 | `doc_kenh` | nuot -> gia tri `KHONG_DO_DUOC` |
| 184 | `_doc_kenh_xac_thuc` | nuot -> gia tri `KHONG_DO_DUOC` |
| 502 | `chay_ca` | nuot -> them vao `do` |
| 649 | `chay_mot_mutant` | nuot -> `trang_thai = KHONG_DO_DUOC` |
| 2660 | `_chay_r508_tach_nguon_do` | gom -> `TinHieuKhongDoDuoc` (da la trang thai thu ba) |
| 4668 | `chay_dot_bien_tu_kiem` | nuot -> `proof_text = None` |
| 1762 · 2121 · 2277 · 3467 · 3574 | `r517` `r520` `r522` `r543` `r544` | bat `Exception` roi `raise TinHieuChotCa` — ha tang thanh CHOT |
| 321 | `_dau_hieu_kho_bare` | ket thuc bang `AssertionError` -> `DO_KHAC`: **CO DAY DO**, ngoai lop |
| 4745 | `chay_tu_kiem` | runner: `DO_KHAC` — trang thai thu ba, nhung KHONG xet (A)/(B) |

## 3. Closure — dong ca LOP tai CHO QUYET DINH NHAN, khong va tung ca

**M1 — So loi ha tang dung chung.** Mot so ghi (list) song MOT cho cho ca tien trinh,
dung chung giua ban goc va moi ban sao nap bang `_nap_ban_sao` (vi ca long chay trong
ban sao `m`). Moi diem nuot o §2 (156, 184, 502, 649, 2660, 4668) GHI doi tuong `OSError`
vao so truoc khi doi no thanh gia tri.

**M2 — Loi TIEM CO CHU Y duoc dang ky theo DOI TUONG**, khong theo ten kich ban hay cua so
thoi gian: fixture tao ngoai le thi dang ky chinh doi tuong ay; so bo qua doi tuong da dang
ky. Loi THAT (khong dang ky) xay ra trong cung kich ban van duoc ghi. Day la cach dong
"`cho_kdd` phan loai theo TEN" cua vong 3.

**M3 — Runner doi nhan.** `chay_tu_kiem`, voi moi ca: lay cac muc so MOI tu luc vao ca
(theo VI TRI, khong xoa so — de runner long ben trong mot ca khong xoa bang chung cua ca
ngoai), cong cac `OSError` chua dang ky tren CHUOI `__context__`/`__cause__` cua ngoai le
ca nem ra (dong 5 cho `except Exception -> raise TinHieuChotCa` ma khong sua tung cho).
Neu co it nhat mot, thi ca `DAT` HOAC `DO_CHOT` deu thanh `DO_KHAC` mang
`TinHieuKhongDoDuoc: tien de ha tang hong: <LOAI>: <thong diep> (<n> lan); ...` — dong CA
huong (A) lan (B). Khong co thi nhan GIU NGUYEN.

**M4 — Don phan va hep cua r1 bi thay the.** `r501` (bo `ha_tang` rieng cua `run_gia`),
`r508` (bo buoc doc thu), `r543` (bo `cho_kdd`, B3, B5, B6) — thay bang M1-M3. Giu: chot
ly do bac cua `r508`, `_chay_r508_tach_nguon_do`, B1, B2, B4, `r544`. Moi muc bi go phai
duoc KHAI trong commit kem ly do.

**M5 — Giu nguyen muc tieu cua r1** (M1-M3 cua r1: vong (c2) ba nguon do; `stderr` khai
so ky tu bo) — khong duoc thoai lui.

## 4. Nghiem thu — moi tieu chi neu phep do lam no DO

- **B1 (ca `r545`, co che)** — tren BAN SAO: (a) moi diem nuot M1 GHI khi gap `OSError`
  (goi thang tung ham voi dau vao lam no nem); (b) loi da dang ky KHONG ghi; (c) runner:
  ca tra DAT ma so co muc moi -> `DO_KHAC` mang loai + thong diep + so lan; ca nem chot ma
  so co muc moi -> `DO_KHAC`; ca nem chot trong `except` cua mot `OSError` -> `DO_KHAC`;
  ca sach -> DAT; ca chot that khong co loi ha tang -> `DO_CHOT`; (d) muc so cua ca TRUOC
  khong lan sang ca SAU. DO khi: go ghi o bat ky diem nao (moi diem MOT dot bien), bo loc
  dang ky, bo doi nhan DAT, bo doi nhan CHOT, bo duyet chuoi, bo tinh theo vi tri.
- **B2 (ca `r546`, ma tran TRONG suite)** — chay `chay_tu_kiem` THAT cua ban sao tren TUNG
  ca `TU_KIEM` (tru `r545`, `r546`) duoi che do RJ; DAT chi khi: khong ca nao `DO_CHOT`,
  moi ca co `inj > 0` ra `DO_KHAC` chua `tien de ha tang`, moi ca `inj == 0` ra DAT. DO khi:
  go ghi o 184 / 649 / 4668 / 502 (it nhat mot ca trong §2 doi mau).
- **B3** — doi chung DUONG: lan day du, `SACH`, van `TU KIEM N/N` voi hai so BANG NHAU.
  Thieu no thi mot trien khai "moi thu la KDD" se xanh B1/B2.
- **B4** — ma tran ngoai (§2) chay lai tren head ung vien: RJ va R2 ra **0 CHOT, 0 DAT du
  da tiem**; W va M ra 0 CHOT. Dinh kem output vao verdict. (Ngoai suite: chi phi 5 che
  do x 44 ca qua lon de chay trong moi mutant — xem §6.)
- **B5** — moi duong moi co dot bien RIENG, phan biet duoc bang DAU VAO; `dich` = DUNG tap
  ca do do tu luot day du; neo duy nhat ngoai bang.
- **B6** — luot day du `rc=0`, stderr 0 B; `SAN_NHOM` va `NHOM_BAT_BUOC` nang theo ca moi;
  delta ruff F = 0; do delta hai phia (so ca, so dot bien) trong MOT lenh.

## 5. KHONG HUA GI

- `r509`: `CHOT-CAM-THU-DAC-TA-KHONG-DOI` — no rieng, con mo (giu tu r1).
- Huong cat cua `stderr[-200:]` va `_goi_chan_doan` — khong doi.
- Co che lease — issue #599.
- Loi ha tang ben trong TIEN TRINH CON (mutant chay `python ban_sao`) chi den cha qua
  chuoi/kenh; ma tran in-process KHONG tiem duoc vao con. Nhan cua con do CHINH runner cua
  con quyet dinh (M3 chay ca o con), nhung phep do rieng cho duong ay la `CHUA DO DUOC`.
- Ca `T1..T8` cua `chay_ca` (do CONG CU `nhanh_don_duoc.py`, khong phai bo cham): nhan
  cua chung khong doi ngoai viec 502 ghi so.
- `except Exception` khac trong tep khong nam trong §2: chi khai, khong sua.

## 6. Chua do duoc

- Duong con (§5). Chi phi dua ma tran R2/W/M vao suite: moi mutant chay lai toan bo tu
  kiem, nen them 4 che do x ~5 s = ~20 s x 162+ mutant. Chon: RJ trong suite (B2), R2/W/M
  ngoai suite (B4), va khai ro gioi han nay.

## 7. Hinh dang ke thua (do toi luc mo r2)

    LOI-KHAI-RONG-HON-PHEP-DO                     10
    TIN-HIEU-DO-CHINH-MA-TEST-GIA-MAO              6
    VA-DUNG-CHO-DUOC-CHI-ROI-BO-SOT-DUONG-THU-BA   3   (+1: vong 3 va dung danh sach vong 2)
    CHOT-CAM-THU-DAC-TA-KHONG-DOI                  2
    BO-TUONG-DUONG-DO-CHINH-EXECUTOR-DUNG          2

`VA-DUNG-CHO...` da cham 3. Chu kho da duoc hoi "co nen lam viec nay khong" va tra loi
bang chi thi mo r2. Bien phap trong r2 chong lap lai: TU QUET ca tep bang ma tran TRUOC khi
va, va dong tai CHO QUYET DINH NHAN (runner) thay vi tung ca.
