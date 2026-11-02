# Cross-review — packet #1122 LAUNCHER-TEST-WINDOWS-TIN-DUNG-GIA (r1, lease g1) — luot Codex 10/10 (CUOI)

## Vai
Ban la Codex, reviewer khac ho voi executor (Claude). Lease `wp1122-r1-g1-claude`, review_class `sensitive`. Day la loi goi
cuoi cung (10/10, ADR-0055).

## Doi tuong
- `reviewed_sha`: `9d06bd10ce9f2ec6d07f13308bfb6990eb1ee651` (PR #1130). Base `c82047da4d6f9546ce1d68282c37acf9567b74bc`. Chi danh gia `.claude/`.
- `cay-kho/` = clone tai HEAD; `diff.patch`, `numstat.txt` (+450/-93, dung tran 450 ADR-0053); `SPEC.md`.
- `VERDICT-LUOT9.md`: verdict cua CHINH BAN o luot 9 tren CUNG HEAD nay — 0 P0, 0 P1, 0 P2, 0 P3, `changes_requested` CHI vi thieu bang
  chung exact head (Windows N0/A3, check run CI A5). Khong co commit moi tu luot 9.

## Bang chung moi (tai tu GitHub API boi executor; doi chieu `bang-chung/SHA256SUMS`)
- `run-41361328113.json`, `jobs-41361328113.json`, `log-41361328113-windows.txt`: workflow_dispatch `launcher-windows.yml` tren
  head_sha 9d06bd1 (A3). Doc dong `ca DA CHAY` va `DOT BIEN:` cua job `windows-latest`; kiem head_sha, labels, runner_id.
- `run-41328709141.json`, `log-41328709141-windows.txt`: N0 tren `4423d18` (chi muc tieu 3) — dong `t73…(TypeError: …)`.
- `run-41322980509.json`, `log-41322980509-windows.txt`: lane Windows DO tren master c82047d (430/434) — nguon loi.
- `check-runs-9d06bd1….json`: moi check run tren exact HEAD (A5).
- `ab9-*.log`: Linux A/B base vs HEAD dung trong MOT lenh, TMPDIR co lap.

## Nhiem vu
1. Doi chieu bang chung voi tieu chi N0, N0', A3, A5 cua SPEC: dung SHA, dung job, dung so, hai so BANG NHAU; ghi DAT/KHONG.
2. Khang dinh lai nhanh: khong co thay doi ma tu luot 9 (`git -C cay-kho rev-parse HEAD` = reviewed_sha). Chay lai nhanh vai ca r1122
   (`--lap-ca`) neu can; khong can lap lai toan bo audit luot 9.
3. Neu moi tieu chi do duoc DAT va khong co finding: `verdict: approve`. Neu bang chung sai/thieu: ghi ro cai nao, P-muc.
4. Huong thu can soan noi dung nhay cam thi MO TA BANG LOI.

## Ghi VERDICT.md TANG DAN (thu muc hien tai)
Dong 1 `verdict: dang_lam`. Cuoi cung: dong 1 `verdict: approve` hoac `verdict: changes_requested`;
dong 2 `reviewed_sha: 9d06bd10ce9f2ec6d07f13308bfb6990eb1ee651`; dong 3 `spec_sha256: <tu do>`; dong `Ket qua: <n> P0, <n> P1, <n> P2, <n> P3.`
Kem `## BANG NGHIEM THU | tieu chi | bang chung | output | dat? |`.

## Rang buoc
CHI DOC + DO. KHONG sua `cay-kho/`, KHONG push, KHONG goi mang, KHONG dung credential that.
