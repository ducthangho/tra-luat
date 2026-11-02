# Cross-review — packet #1117 HARNESS-KET-QUA-NGOAI-MA-DOT-BIEN (r2, lease g2) — luot Codex 5/10

## Vai
Ban la Codex, reviewer khac ho voi executor (Claude). Lease `wp1117-r2-g2-claude`, review_class `sensitive`. Tran 10 loi goi
(ADR-0055). Chu kho: chay toi khi HET P0/P1/P2/P3. Tran dong them 450 (ADR-0053); hien +329.

## Doi tuong
- `reviewed_sha`: `8f0dfcf35c8ee92a9a754bde82846eb11430bd0e` (head cuoi cua PR #1142, nhanh `agent/wp1117-g1-claude`).
  Base `c7174bfe03b3acd22cfa055b5fce176129d29542`.
- Luot 4 (`VERDICT-L4.md`) approve 0/0/0/0 tren `6f4b889`. Sau do connector Codex bao P2 `r4438879478`: runner GIA trong
  `r1079_cham_lap_ca_doi_dung_TinHieuChotCa` tach stdin bang `.split()` => duong kenh co dau cach vo. `diff-tu-l4.patch` = `git diff 6f4b889 HEAD`.
- `diff.patch` = `git diff BASE HEAD -- .claude`. Dac ta `SPEC.md` (r2, sha256 `c34d5066…`) ke thua `SPEC-R1.md`.

## Bang chung executor (do lai neu nghi ngo)
- Va P2: runner gia doc `sys.stdin.buffer.read().decode('utf-8').splitlines()`; ca dat `tempfile.tempdir` vao thu muc `co dau cach`.
  Ca 1/1 voi TMPDIR thuong va TMPDIR `/var/tmp/co dau cach`. Phan chung: tra `.split()` giu tempdir moi => 0/1.
- Nhom 14 dot bien (moi `wp1117_*` + `wp1079_*` nham ca nay) qua `chay_dot_bien` that => `(0, 0)`.
- Windows `ci.yml` windows-only va `launcher-windows.yml` tren HEAD: DANG CHAY (KHONG DO DUOC trong bundle). Tren `6f4b889` ca hai xanh.

## Nhiem vu
1. Dong P2 connector: do bang TMPDIR/`tempfile.tempdir` co dau cach (va co dau tieng Viet) tren HEAD va tren `6f4b889`.
   Con runner gia/khung stdin nao khac trong `launcher_test.py` tach bang khoang trang khong? Tim BANG DOC MA toan tep.
2. Chay lai cac ca/dot bien tap trung cua luot 1-4 tren HEAD. Giu dong F01/F02/F03.
3. Do lai A/B neu du thoi gian (TMPDIR ngoai /tmp neu ghi duoc; khong thi ghi KHONG DO DUOC).

## CACH LAM (tranh bo loc noi dung cua nen)
CHAY ca/dot bien DA CO; dot bien ban va tren BAN SAO TAM ngoai `cay-kho/`. KHONG tu soan ma gia kenh / lop ngoai le moi;
huong thu nhay cam thi MO TA BANG LOI.

## Bay moi truong da biet
- `/tmp/.git` rong do sandbox Codex: 11 ca `r484_*` do. 10 ca duong `launcher.py run` do san tren base. Khong co mang.

## Ghi VERDICT.md TANG DAN (thu muc hien tai, ngoai `cay-kho/`)
Dong 1 `verdict: dang_lam`. Cuoi cung: dong 1 `verdict: approve` hoac `verdict: changes_requested`;
dong 2 `reviewed_sha: 8f0dfcf35c8ee92a9a754bde82846eb11430bd0e`; dong 3 `spec_sha256: <tu do>`; dong `Ket qua: <n> P0, <n> P1, <n> P2, <n> P3.`
Kem `## BANG NGHIEM THU`, `## BANG DO`, `## BANG TEST`. P0/P1 = sai hanh vi; P2 = khai rong hon phep do / chot thieu rang; P3 = dien dat.
Goi y va vao `HINT.patch` (patch -p0 tu `cay-kho/`).

## Rang buoc
CHI DOC + DO. KHONG sua `cay-kho/`, KHONG push, KHONG goi mang, KHONG dung credential that.
