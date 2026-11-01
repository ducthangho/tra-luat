# Cross-review — packet #1079 LAUNCHER-TEST-ORACLE-VA-FIXTURE (r1, lease g7) — luot Codex 6/6 (CUOI)

## Vai
Ban la Codex, reviewer khac ho voi executor (Claude). Lease `wp1079-r1-g7-claude`, review_class `sensitive`.
Tran: 6 loi goi Codex (chu kho nang 2->3->4->5->6); day la loi goi 6 (cuoi). Tran dong them da nang 300->380->480->640->720->800 (chu kho) — KHONG tinh la finding.
F04 cua luot 2 (ma cap module cua ban dot bien thay nonce truoc main) da duoc CHU KHO quyet ghi thanh no #1117 — KHONG tinh la finding chan; chi bao neu ban va lam no TE HON.

## Doi tuong
- `reviewed_sha`: `e3bcaf0b376e80367b750ccc8c41cce9b686b407`. Base `7eeb1d9a10aea8e1805b66fbf3d68549eb6778da`.
- Diff: `diff.patch` (= `git diff BASE HEAD -- .claude`; HEAD co merge origin/master, phan ngoai `.claude/` la cua master), `numstat.txt`;
  `diff-tu-luot5.patch` = thay doi tu head luot 5 `c5acb70`.
- Verdict cac luot truoc: `VERDICT-LUOT1.md` .. `VERDICT-LUOT5.md`. Commit `e3bcaf0` khai da va F08 luot 5 (kiem_registry o moi diem vao).
- Truoc do: Theo quyet dinh CHU KHO sau luot 4: `ca`/`chay_suite` TU CHOI ca trung `__code__`
  luc dang ky (F05/F08 dong theo cau truc), bo phep tru F08; commit `c5acb70` cung dinh chinh loi khai F09 va cau sai cua `5368c34`. 2 tep: `.claude/dev/launcher_test.py`, `.claude/dev/codex_cred_test.py`.
- Dac ta dong bang: `SPEC.md` (sha256 `81070fa2c5a00bc0bb63867c7173f310cba9002001b68a26d62726ec904cbf5b` — tu do lai).
- Nguon loi: `NGUON-VERDICT-484.md` muc `F01-mutation-oracle-unrelated-exception` va `F02-f04-fixture-ambient-installers`.

## Nhiem vu
0. TRUOC TIEN: F08 luot 5 (va moi finding luot 1-4) da dong chua — chay lai DUNG phan chung cua tung luot tren HEAD nay;
   `kiem_registry` con diem vao nao chay ca ma khong qua no khong, va no co chan nham ca hop le nao trong 347 ca hien co khong.
1. Moi tieu chi M1-M7 va A1-A4 cua SPEC.md: dat hay khong, bang LENH CHAY DUOC trong `cay-kho/` tai HEAD.
2. Moi khang dinh trong diff (code, comment, docstring, commit message `git log --format=%B BASE..HEAD` trong `cay-kho/`): do lai.
   Danh sach ban tu lap se thieu — ghi ro cach tim.
3. Bo cham moi (ba diem a/b/c) con duong nao cap tin dung gia? Thu it nhat: AttributeError qua mot `except` doi kieu sang
   AssertionError; AssertionError tu ma trien khai; assertion cua ca KHAC; neutral do; ca tu bo qua theo nen; output con
   gia dong `LOAI_HONG`/headline; tep khac co cung so dong `assert` (codex_cred_test). Nguoc lai: bo cham moi co chan NHAM
   mot lan giet that nao khong?
4. F02: fixture N13 con loi nao de hook cham installer/BASH_ENV/HOME cua may chay? Dung moi truong cha thu dich (rg hong,
   installer ghi log) de do; so voi base.
5. Chay: `python3 .claude/dev/launcher_test.py`, `python3 .claude/dev/launcher_test.py --dot-bien`,
   `python3 .claude/dev/codex_cred_test.py` (N/M; BO QUA ghi rieng). Dot bien them cua ban: chay tren BAN SAO TAM ngoai
   `cay-kho/`; moi chot moi phai co dot bien lam ca dich do DUNG LY DO (`TinHieuChotCa` cua chinh ca).
6. Huong thu can soan noi dung nhay cam thi MO TA BANG LOI, khong tu soan.

## Bay moi truong da biet (ghi KHONG DO DUOC kem ly do, dung doc thanh hoi quy)
- Sandbox Codex co the de lai `/tmp/.git` rong; khi ay 11 ca `r484_*` do vi "Codex home is inside a repository" — va voi bo
  cham moi, dot bien nham ca ay se bao "neutral do". Hoi `ls -d /tmp/.git` truoc khi ket luan; so voi base cung dieu kien.
- Khong co mang.

## Ghi VERDICT.md TANG DAN (thu muc hien tai, ngoai `cay-kho/`)
Dong 1 `verdict: dang_lam` ngay khi bat dau. Cuoi cung: dong 1 `verdict: approve` hoac `verdict: changes_requested`;
dong 2 `reviewed_sha: e3bcaf0b376e80367b750ccc8c41cce9b686b407`; dong 3 `spec_sha256: <tu do>`;
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
