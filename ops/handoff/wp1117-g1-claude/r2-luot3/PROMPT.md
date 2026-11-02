# Cross-review — packet #1117 HARNESS-KET-QUA-NGOAI-MA-DOT-BIEN (r2, lease g2) — luot Codex 3/10

## Vai
Ban la Codex, reviewer khac ho voi executor (Claude). Lease `wp1117-r2-g2-claude`, review_class `sensitive`. Tran 10 loi goi
(ADR-0055). Chu kho: chay toi khi HET P1/P2/P3. Tran dong them 450 (ADR-0053); hien +326.

## Doi tuong
- `reviewed_sha`: `4a0d45d3c689600f749866f7b27e83b9d6039c00` (nhanh `agent/wp1117-g1-claude`). Base `c7174bfe03b3acd22cfa055b5fce176129d29542`
  (master sau #1122). Luot 2 xet `b9f010b`; `diff-tu-l2.patch` = `git diff b9f010b HEAD` (ap NGUYEN HINT-L2 cho F03).
- `diff.patch` = `git diff BASE HEAD -- .claude` (2 tep), `numstat.txt`.
- Dac ta: `SPEC.md` (r2, sha256 `c34d5066…` — tu do lai), ke thua `SPEC-R1.md` (sha256 `48710a9b…`) o moi muc r2 khong sua.
- Luot truoc: `VERDICT-L1.md` (F01/F02 P1), `VERDICT-L2.md` (F01/F02 da vá; F03 P2 chot-kieu-record-chua-co-dot-bien-dung-tin-hieu), `HINT-L2.patch`.
- Nguon loi: `VERDICT-1079-LUOT2.md` (F04 cua #1079: ma cap module cua ban dot bien doc nonce tu env, gia kenh ket qua).

## Bang chung executor (do lai neu nghi ngo)
- F03: ap NGUYEN HINT-L2. Ca `r1079_cham_lap_ca_doi_dung_TinHieuChotCa` 1/1 qua; nhom 7 dot bien kenh/lap_ca qua `chay_dot_bien` that
  (wp1117_lap_ca_bo_kiem_kieu_record, wp1079_lap_ca_bo_kiem_nonce, wp1079_lap_ca_tin_stdout, wp1079_bao_cao_theo_ten_lop,
  wp1079_bo_tien_to_khac, wp1117_runner_doc_stdin_theo_codec_moi_truong, wp1117_bo_kiem_loai) => `(0, 0)`, moi cai OK dung ca dich.
- Windows `b6fe853` (run 41368402146): DOT BIEN 466/468, 2 SAI = hai dot bien F02. Windows `b9f010b`, `4a0d45d` va Linux A/B
  `c7174bf`/`b9f010b`: DANG DO. Ruff F 5 = nen.

## Diem can kiem ky
0. DONG F03 cua `VERDICT-L2.md` va giu dong F01/F02: do lai bang dung phep do luot 1/2 (ma tran encoding, A/B dot bien, bo guard kieu record). Ban va co tao loi moi khong (thu tu dong stdin/fd 0, EOF, khung 2 dong, Windows)?
1. Runner (`.claude/dev/launcher_test_runner.py`) va hop dong (i)-(v) cua SPEC-R1 muc 1: thu tu doc stdin truoc khi nap, khong
   du lieu kenh trong env/argv, chi ghi kenh SAU `cham_mot_ca`. Gioi han co ten `RUNNER-CUNG-TIEN-TRINH` (can thiep CO Y trong
   cung tien trinh, ghi de tep tren dia) la quyet dinh chu kho — KHONG tinh la finding; nhung moi cua gia THU DONG (doc env/argv/
   stdin, ghi kenh truoc khi ca chay, doan duong kenh + nonce) thi la finding.
2. Lech spec da duyet: `cham_lap_ca` chay runner trong `thu_muc` (do `_dung_cay_harness` THAT chep), de chot trong runner dot bien
   duoc qua DOT_BIEN_HARNESS. Kiem: ban dot bien co cach nao lam cay long nhan runner CUA NO thay vi runner that ma ca dich van xanh?
3. Muc 8 r2: cac ca `r1122_kenh_*` nay do qua runner — bao dam (a) ca long cung ten/`__str__` long khong doi ket qua ca ngoai,
   (b) chi tiet `loi` = `<Loai>: <160>`, (c) ket qua qua khong mang loi cu. Doi chieu voi y nghia goc o #1122 (PR #1130).
4. Muc 9 r2: dot bien moi `wp1117_*` va cac dot bien bi bo/neo lai. Moi chot moi phai co dot bien lam ca dich DO bang
   `TinHieuChotCa` cua chinh ca. Danh sach dot bien ban tu lap se thieu — ghi ro cach tim.
5. Chay `python3 .claude/dev/launcher_test.py` va `--dot-bien` (N/M; BO QUA ghi rieng; so voi base cung dieu kien).

## CACH LAM (tranh bo loc noi dung cua nen)
CHAY cac ca phan chung va dot bien DA CO trong cay; DOT BIEN BAN VA tren BAN SAO TAM ngoai `cay-kho/`. KHONG tu soan ma gia kenh /
lop ngoai le co hanh vi dac biet moi. Neu thay can mot huong thu loai do, DOC MA va MO TA BANG LOI duong co the sai cung dong code,
de executor tu dung phan chung.

## Bay moi truong da biet
- Sandbox Codex co the de lai `/tmp/.git` rong: 11 ca `r484_*` do ("Codex home is inside a repository"). Dat TMPDIR ngoai /tmp khi do.
- 10 ca duong `launcher.py run` (r09, r15, r925_*, r926_*, r927_*) do san tren base trong container. Khong co mang.

## Ghi VERDICT.md TANG DAN (thu muc hien tai, ngoai `cay-kho/`)
Dong 1 `verdict: dang_lam`. Cuoi cung: dong 1 `verdict: approve` hoac `verdict: changes_requested`;
dong 2 `reviewed_sha: 4a0d45d3c689600f749866f7b27e83b9d6039c00`; dong 3 `spec_sha256: <tu do>`; dong `Ket qua: <n> P0, <n> P1, <n> P2, <n> P3.`
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
