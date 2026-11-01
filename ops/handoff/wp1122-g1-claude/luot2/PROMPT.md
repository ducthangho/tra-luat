# Cross-review — packet #1122 LAUNCHER-TEST-WINDOWS-TIN-DUNG-GIA (r1, lease g1) — luot Codex 2/10

## Vai
Ban la Codex, reviewer khac ho voi executor (Claude). Lease `wp1122-r1-g1-claude`, review_class `sensitive`.
Tran 10 loi goi Codex (ADR-0055); day la loi goi 2.

## Doi tuong
- `reviewed_sha`: `6cf0cc5231adc6b4fd5bd63c4e97f6aeee30ecdb` (PR #1130). Base `c82047da4d6f9546ce1d68282c37acf9567b74bc`.
  HEAD la merge master `180039c` vao nhanh; master chi them `ops/reviews/**`, nen `.claude/` cua HEAD == `fd1f82e`.
- `diff.patch` = `git diff BASE HEAD -- .claude` (1 tep), `numstat.txt`; `diff-tu-luot1.patch` = thay doi tu head luot 1 `30ee4ae`.
- Verdict luot 1: `VERDICT-LUOT1.md` (F01 P1 reporter-thong-diep, F02 P2 khoa-encoding-chi-kiem-khoa). Commit `fd1f82e`
  khai ap NGUYEN VAN `HINT.patch` cua ban luot 1.
- Dac ta: `SPEC.md` (sha256 `198e06f0f7ef6659fb711ef02ff3558ba5c4a63da1c7127b559c5fd8b0fdacb8`). Hai mo rong pham vi da
  duoc chu kho duyet (xem VERDICT-LUOT1 muc dau va prompt luot 1): `raise AssertionError` + moi con Python khai encoding.

## Bang chung executor (do lai neu nghi ngo; Windows ban khong chay duoc)
- Windows run 41333516059 tren `fd1f82e`, job `windows-latest` runner_id 1000033117: `DOT BIEN: 446/446 dat (118 khong do
  duoc)`, suite `282/282 (bo qua 74, hong 0)`.
- Linux A/B dung hai ve trong MOT lenh (clone sach tu GitHub): base `340/350` hong 10, `--dot-bien 523/548`; `fd1f82e`
  `344/354` hong 10, `--dot-bien 535/560`. Tap ca hong va tap dong SAI TRUNG KHIT (delta 0). 10 ca hong deu duong
  `launcher.py run` (r09, r15, r925_*, r926_*, r927_*), do san o container.

## Nhiem vu
0. TRUOC TIEN: F01, F02 da dong chua — chay lai dung phep do cua ban tren HEAD; ban va co mo lo moi khong.
1. Moi tieu chi N0, N0', A1-A5 cua SPEC.md (tinh mo rong da duyet): dat hay khong, bang LENH CHAY DUOC.
2. Moi khang dinh trong diff tu luot 1 (code, comment, commit message `git log --format=%B 30ee4ae..HEAD`): do lai.
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
dong 2 `reviewed_sha: 6cf0cc5231adc6b4fd5bd63c4e97f6aeee30ecdb`; dong 3 `spec_sha256: <tu do>`;
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
