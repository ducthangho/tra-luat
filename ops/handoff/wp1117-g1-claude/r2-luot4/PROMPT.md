# Cross-review — packet #1117 HARNESS-KET-QUA-NGOAI-MA-DOT-BIEN (r2, lease g2) — luot Codex 4/10

## Vai
Ban la Codex, reviewer khac ho voi executor (Claude). Lease `wp1117-r2-g2-claude`, review_class `sensitive`. Tran 10 loi goi
(ADR-0055). Chu kho: chay toi khi HET P0/P1/P2/P3. Tran dong them 450 (ADR-0053); hien +326.

## Doi tuong
- `reviewed_sha`: `6f4b88991b14f1a15ceafdf4b4b3b564039449a1` (head cuoi cua PR #1142, nhanh `agent/wp1117-g1-claude`).
  Base `c7174bfe03b3acd22cfa055b5fce176129d29542`.
- Luot 3 (`VERDICT-L3.md`) approve 0/0/0/0 tren `4a0d45d`. HEAD = merge `origin/master` `9091cf5` vao `4a0d45d`;
  `diff-tu-l3.stat` = `git diff --stat 4a0d45d HEAD` (chi them `ops/specs/CHANGELOG-D-NGOAI-GOI-r2.md`).
- `diff.patch` = `git diff BASE HEAD -- .claude`. Dac ta `SPEC.md` (r2, sha256 `c34d5066…`) ke thua `SPEC-R1.md`.

## Bang chung executor (do lai neu nghi ngo)
- Linux A/B c7174bf vs 4a0d45d, hai ve dung trong MOT lenh, TMPDIR=/var/tmp: `ab-{nen,sau}-{suite,db}.txt`; tap ca HONG va dot bien
  SAI theo ten o `ab1117c-{nen,sau}-{hong,sai}.txt` (bang nhau => delta 0).
- Windows `launcher-windows.yml` tren `4a0d45d`: run 41372451716 success (job windows-latest). Tren `b9f010b`: 469/469.
  `ci.yml` workflow_dispatch runner_set=windows-only tren HEAD: run 41376440756 DANG CHAY (KHONG DO DUOC trong bundle).
- Connector Codex tren HEAD: `Reviewed commit: 6f4b88991b`, khong finding.

## Nhiem vu
1. Xac nhan `.claude/` cua HEAD trung byte voi `4a0d45d` (`git diff --quiet 4a0d45d HEAD -- .claude`) va merge master khong
   doi hanh vi: chay lai cac ca/dot bien tap trung cua luot 1-3 tren HEAD (r1117_*, r1122_kenh_*, r1079_*kenh/lap_ca/harness*,
   7 dot bien kenh/lap_ca qua `chay_dot_bien` that).
2. Do lai A/B neu du thoi gian (TMPDIR ngoai /tmp neu ghi duoc; khong thi ghi KHONG DO DUOC va dung so cua executor).
3. Moi finding moi -> slug/P-level nhu luot truoc. Giu dong F01/F02/F03.

## CACH LAM (tranh bo loc noi dung cua nen)
CHAY ca/dot bien DA CO; dot bien ban va tren BAN SAO TAM ngoai `cay-kho/`. KHONG tu soan ma gia kenh / lop ngoai le moi;
huong thu nhay cam thi MO TA BANG LOI.

## Bay moi truong da biet
- `/tmp/.git` rong do sandbox Codex: 11 ca `r484_*` do. 10 ca duong `launcher.py run` do san tren base. Khong co mang.

## Ghi VERDICT.md TANG DAN (thu muc hien tai, ngoai `cay-kho/`)
Dong 1 `verdict: dang_lam`. Cuoi cung: dong 1 `verdict: approve` hoac `verdict: changes_requested`;
dong 2 `reviewed_sha: 6f4b88991b14f1a15ceafdf4b4b3b564039449a1`; dong 3 `spec_sha256: <tu do>`; dong `Ket qua: <n> P0, <n> P1, <n> P2, <n> P3.`
Kem `## BANG NGHIEM THU`, `## BANG DO`, `## BANG TEST`. P0/P1 = sai hanh vi; P2 = khai rong hon phep do / chot thieu rang; P3 = dien dat.
Goi y va vao `HINT.patch` (patch -p0 tu `cay-kho/`).

## Rang buoc
CHI DOC + DO. KHONG sua `cay-kho/`, KHONG push, KHONG goi mang, KHONG dung credential that.
