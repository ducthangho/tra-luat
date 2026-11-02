# Cross-review — packet #825 CODEX-REJECTED-STATE-KHONG-GHI-DUOC-ADR (r1, lease g1) — luot Codex 2/10

## Vai
Ban la Codex, reviewer khac ho voi executor (Claude). Lease `wp825-r1-g1-claude`, review_class `sensitive` (sua bang §20 cua
`docs/PROTOCOL_DA_PHIEN.md`). Tran 10 loi goi (ADR-0055). Chu kho: chay toi khi HET P1/P2/P3.

## Doi tuong
- `reviewed_sha`: `df3e103b6b0c8ac9259c040a518c7baf99f46790` (PR #1138). Luot 1 xet `46421d7`; `diff-tu-l1.patch` = `git diff 46421d7 HEAD`. Base `c7174bfe03b3acd22cfa055b5fce176129d29542`.
- `diff.patch` (2 tep: ADR-0061 moi + 1 dong §20). `SPEC.md` (sha256 `dee36a11…` — tu do lai).
- Luot truoc: `VERDICT-L1.md` (F1 P1 loi-ghi-khong-suy-ra-probe-lap, F2 P2 grep-ten-khong-do-khai-niem), `HINT-L1.patch`.
  Executor: bo backtick o 3 con tro doc-claims-check (17d3606, gate-ops do vi L1 PATH_MISSING + 2 L12 TEST_ID_UNKNOWN), roi ap
  NGUYEN HINT-L1 (df3e103). Executor do A4 voi TMPDIR=/var/tmp co lap tren df3e103: hai ca r484_g7_* `1/1 qua`, codex_cred_test
  `ca 18 · dot bien 18 · TONG: DAT`. doc-claims-check strict ok, adr-song 60/60, doctrine-scan rc=0.
- Issue #825 cho phep dong bang ADR chap nhan gioi han vinh vien; chu kho da chon loi do (khong tinh la finding).

## Nhiem vu
0. DONG F1/F2 cua VERDICT-L1 tren HEAD moi bang dung phep do luot 1 (script luot 1 chep o `evidence-l1/`, chay lai tren cay HEAD; ma runtime KHONG doi).
   Cau chu moi co khai rong hon phep do khong (vd 'moi luot ... goi helper probe mot lan', 'luong ma suy ra')? Spec muc 'Su that da
   do' con ghi 'dung 1': co phai lech spec can ghi vao handoff khong (tieu chi A1-A5 co doi 'dung 1' khong)?
1. Moi tieu chi A1–A5 cua SPEC: dat hay khong, bang LENH CHAY DUOC trong `cay-kho/` (A5 = CI, ghi KHONG DO DUOC neu offline).
2. DO LAI moi khang dinh su that trong ADR bang ma tai base/HEAD: ten ham, dong code, chuoi ly do CHAN, ten ca/dot bien va ca
   ba loi (`launcher._do_codex_song`, materializer `chuan_bi_xac_thuc`, `codex_cred.cmd_kiem`) — loi nao KHONG bao loi to hoac
   khong co ca/dot bien khoa thi la finding. Chay cac ca duoc dan (`launcher_test.py --lap-ca …`, `codex_cred_test.py`).
3. Hau qua "moi lan goi ton them 1 lan probe": doi chieu voi ma (co duong nao probe NHIEU hon 1, hoac ghi SAI trang thai?).
4. Muc Cuong che: do lai `rg -c` tren du sau vi tri cong; dong §20 co dung khuon va noi dung khop ADR khong.
5. Loi khai rong hon phep do (L6/§20): cau nao noi "da do" ma khong co lenh; cau "suy luan chua do" co duoc ghi dung khong.

## Bay moi truong da biet
- Sandbox Codex co the de lai `/tmp/.git` rong: 11 ca `r484_*` do. Dat TMPDIR ngoai /tmp khi chay test. Khong co mang.

## Ghi VERDICT.md TANG DAN (thu muc hien tai, ngoai `cay-kho/`)
Dong 1 `verdict: dang_lam`. Cuoi cung: dong 1 `verdict: approve` hoac `verdict: changes_requested`;
dong 2 `reviewed_sha: df3e103b6b0c8ac9259c040a518c7baf99f46790`; dong 3 `spec_sha256: <tu do>`; dong `Ket qua: <n> P0, <n> P1, <n> P2, <n> P3.`
Kem `## BANG NGHIEM THU`, `## BANG DO` (khang dinh | do duoc (lenh) | khop?), va finding dang `### <slug> [P0|P1|P2|P3] <tieu de>`.
P0/P1 = khang dinh sai do duoc; P2 = khai rong hon phep do / chot thieu rang; P3 = dien dat. Goi y va vao `HINT.patch` (patch -p0 tu `cay-kho/`).

## Rang buoc
CHI DOC + DO. KHONG sua `cay-kho/`, KHONG push, KHONG goi mang, KHONG dung credential that.
