# Cross-review — packet #1122 LAUNCHER-TEST-WINDOWS-TIN-DUNG-GIA (r1, lease g1) — luot Codex 9/10

## Vai
Ban la Codex, reviewer khac ho voi executor (Claude). Lease `wp1122-r1-g1-claude`, review_class `sensitive`.
Tran 10 loi goi Codex (ADR-0055); day la loi goi 9 (loi goi 7 bi bo loc noi dung cat; con 1 loi goi sau luot nay). Tran dong them 450 (ADR-0053) dang o DUNG 450: ban va de xuat phai giu duoc tran nay hoac noi ro can nang_tran. Chu kho: chay toi khi HET P1/P2/P3 (P3 cung phai bao neu co).

## Doi tuong
- `reviewed_sha`: `9d06bd10ce9f2ec6d07f13308bfb6990eb1ee651` (PR #1130). Base `c82047da4d6f9546ce1d68282c37acf9567b74bc`.
  Lich su nhanh co merge master `180039c` (chi them `ops/reviews/**`); danh gia CHI phan `.claude/`.
- `diff.patch` = `git diff BASE HEAD -- .claude` (1 tep), `numstat.txt`; `diff-tu-luot8.patch` = thay doi tu head luot 8 `cccc5eb` (chi test + 2 dot bien, ap nguyen van HINT luot 8; bo dong trong de giu tran 450).
- Verdict luot 1: `VERDICT-LUOT1.md` (F01 P1, F02 P2; va o `fd1f82e`). Verdict luot 2: `VERDICT-LUOT2.md` (F01 P1 con 4 duong:
  nhat ky `ket`, chot ca khac, loi bien dich dot bien; commit `4c6f933` ap NGUYEN VAN HINT luot 2). Executor khai: da tu liet
  ke MOI duong in chi tiet loi trong tep (grep `type(e).__name__|e.msg|{e}|str(e)` + moi `except ... as` trong chay_dot_bien)
  va thay trung dung 4 duong cua ban — loi khai do SAI (ban bat o luot 3; commit 93a9afe dinh chinh).
- Verdict luot 3: `VERDICT-LUOT3.md` (F01 P1: Unicode tren console khong UTF-8 + reporter `_tu_tach_nhom_neu_can`). Commit
  `93a9afe` ap NGUYEN VAN HINT luot 3, va khai: liet ke lai bang AST TOAN TEP moi `except ... as e` co dung `e` de dung
  chuoi = 30 khoi; 18 trong ham @ca (logic ca), 12 ha tang = 8 reporter (nay du) + 4 logic fixture (`_wp1077_llm`,
  `_CsNhan`, `_CsSeam`, `_review6_registry_raw_phai_tu_choi`). KIEM lai phep liet ke nay — va cac duong reporter KHONG di
  qua `except` (vd ham nhan exception lam doi so, `traceback.format_exc`, `repr(e)`, sys.excepthook, threading.excepthook).
- Verdict luot 4: `VERDICT-LUOT4.md` (F01 P1: kenh --lap-ca phat lai chi tiet cu tu `CHI_TIET_HONG`; loi I/O nhat ky thoat
  ra traceback). Commit `365c751` ap NGUYEN VAN HINT luot 4. Ghi chu: packet #1117 (dang tam dung) se BO HAN kenh --lap-ca;
  khong dua viec do vao day.
- Verdict luot 5: `VERDICT-LUOT5.md` (F01 P1: kenh doc map toan cuc, ca long ghi de). HINT luot 5 lam diff +455 > tran 450 (ADR-0053)
  nen CHU KHO CHOT (AskUserQuestion): GO truong thong diep khoi kenh --lap-ca (bo `CHI_TIET_HONG`, `ten_loai`, `thong_diep`);
  `loai` la anh chup cua lan lap NGOAI co hong. Day la QUYET DINH PHAM VI da duyet, khong tinh la finding: chi tiet `loi` cua
  nhanh harness qua `cham_lap_ca` chi con LOAI (khong thong diep); #1117 se mang chi tiet qua runner. KIEM: con duong nao
  doc `LOAI_HONG` song (live) de dua vao ket qua cham, va ca long co the doi loai cua mot ca dich thanh giet khong.
- Verdict luot 6: `VERDICT-LUOT6.md` (F01 P1: `__str__` cua loi ngoai goi long chay_bo_ca, ghi de LOAI_HONG truoc khi main chup).
  Commit `cccc5eb`: ap HINT test luot 6 nguyen van; producer: `chay_bo_ca` dinh dang `tin = mo_ta_loi(e)` MOT lan o dau moi nhanh
  except, ghi `LOAI_HONG` SAU moi loi goi dinh dang; them dot bien `wp1122_dinh_dang_lai_sau_ghi_map`.
- Verdict luot 8: `VERDICT-LUOT8.md` (0 P0, 0 P1, 1 P2: khoa thu tu chua phu nhanh AssertionError) — da va o `9d06bd1`.
- CACH LAM LUOT NAY (phan cong lai sau khi luot 7 bi bo loc nen chan): CHAY cac ca va dot bien DA CO trong cay, va DOT BIEN BAN VA
  (doi thu tu dong ghi map / goi lai mo_ta_loi) de do rang. KHONG tu soan lop ngoai le moi co hanh vi dac biet. Neu thay can mot
  huong thu loai do (vd thu tu doc/ghi trong `chay_bo_ca`, `cham_mot_ca`, nhanh hook) thi DOC MA va MO TA BANG LOI duong co the
  sai cung dong code, de executor tu dung phan chung.
- Dac ta: `SPEC.md` (sha256 `198e06f0f7ef6659fb711ef02ff3558ba5c4a63da1c7127b559c5fd8b0fdacb8`). Hai mo rong pham vi da
  duoc chu kho duyet (xem VERDICT-LUOT1 muc dau va prompt luot 1): `raise AssertionError` + moi con Python khai encoding.

## Bang chung executor (do lai neu nghi ngo; Windows ban khong chay duoc). Tren `cccc5eb`: Linux A/B (TMPDIR co lap) base `340/350` `523/548`, head `352/362` `548/573`, tap hong/SAI trung khit. Tren `9d06bd1` dang do.
- Windows run 41333516059 tren `fd1f82e`, job `windows-latest` runner_id 1000033117: `DOT BIEN: 446/446 dat (118 khong do
  duoc)`, suite `282/282 (bo qua 74, hong 0)`.
- Linux A/B dung hai ve trong MOT lenh (clone sach tu GitHub): base `340/350` hong 10, `--dot-bien 523/548`; `fd1f82e`
  `344/354` hong 10, `--dot-bien 535/560`. Tap ca hong va tap dong SAI TRUNG KHIT (delta 0). 10 ca hong deu duong
  `launcher.py run` (r09, r15, r925_*, r926_*, r927_*), do san o container.

## Nhiem vu
0. TRUOC TIEN: F01 (moi duong cua luot 1-6, 8) va F02 da dong chua — chay lai dung phep do cua ban tren HEAD; ban va co mo lo moi khong.
1. Moi tieu chi N0, N0', A1-A5 cua SPEC.md (tinh mo rong da duyet): dat hay khong, bang LENH CHAY DUOC.
2. Moi khang dinh trong diff tu luot 8 (code, comment, commit message `git log --format=%B cccc5eb..HEAD`): do lai.
3. LOP LOI cua F01: con reporter/duong in chi tiet nao CHUA cat hoac lap ten loai (vd nhat ky NhatKyCa, nhanh hook,
   chay_dot_bien SAI dong, `CHI_TIET_HONG` ro ri giua cac ca, ca khong hong ma van con muc cu trong CHI_TIET_HONG cho kenh
   --lap-ca lan sau)? Liet ke HET cac duong roi do tung duong.
4. Lop loi cua F02: khoa encoding con chap nhan gi sai?
5. Chay `python3 .claude/dev/launcher_test.py` va `--dot-bien` (N/M; BO QUA ghi rieng). Dot bien them: chay tren BAN SAO
   TAM ngoai `cay-kho/`; moi chot moi phai co dot bien lam ca dich do DUNG LY DO (`TinHieuChotCa` cua chinh ca).
6. Huong thu can soan noi dung nhay cam thi MO TA BANG LOI, khong tu soan.

## Bay moi truong da biet
- `/tmp/.git` rong do sandbox Codex: 11 ca `r484_*` do. Hoi `ls -d /tmp/.git` truoc khi ket luan; so voi base cung dieu kien.
- 10 ca duong `launcher.py run` do san tren base. Khong co mang. Dia: don ban sao tam cua chinh ban.

## Ghi VERDICT.md TANG DAN (thu muc hien tai, ngoai `cay-kho/`)
Dong 1 `verdict: dang_lam` ngay khi bat dau. Cuoi cung: dong 1 `verdict: approve` hoac `verdict: changes_requested`;
dong 2 `reviewed_sha: 9d06bd10ce9f2ec6d07f13308bfb6990eb1ee651`; dong 3 `spec_sha256: <tu do>`;
mot dong `Ket qua: <n> P0, <n> P1, <n> P2, <n> P3.`
```
## BANG NGHIEM THU   | tieu chi | lenh | output | dat? |
## BANG DO           | khang dinh | diff khai | do duoc (lenh) | khop? |
## BANG TEST         | bo | N/M | bo qua |
## BANG SAN          (>= 6 huong DOC LAP, moi huong co LENH + OUTPUT THAT; LOI | KHONG PHAI LOI | KHONG DO DUOC)
### <slug>  [P0|P1|P2|P3]  <tieu de>
TEP/DONG: / VAN DE: / DA THU NGHIEM: / DO TIN:
```
P0/P1 = sai hanh vi hoac khang dinh sai do duoc; P2 = khai rong hon phep do / chot thieu rang; P3 = dien dat.
Goi y va vao `HINT.patch` (patch -p0 tu `cay-kho/`).

## Rang buoc
CHI DOC + DO. KHONG sua `cay-kho/`, KHONG push, KHONG goi mang, KHONG dung credential that.
