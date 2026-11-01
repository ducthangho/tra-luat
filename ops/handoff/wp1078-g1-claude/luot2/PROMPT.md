# Cross-review — PR ducthangho/tra-luat#1097 (packet #1078 CAI-CONG-CU-PYTHON-HAM-KE-THUA, r1/g1) — luot Codex 2/2

## Vai
Ban la Codex, reviewer khac ho voi executor (Claude). Lease `wp1078-r1-g1-claude`, review_class `sensitive`. Tran: 2 loi goi; day la loi goi 2 (CUOI).

## Doi tuong
- `reviewed_sha`: `0311db45d5786c3d4a1c05fec1375aec9e727249`. Base `90c101b8d1f8895b66607de8582a18c5e72d834c`.
- Diff: `diff.patch`, `numstat.txt`. 2 tep: `ops/cai_cong_cu.sh`, `.claude/dev/launcher_test.py`.
- Dac ta dong bang: `SPEC.md` (sha256 `2fb1b2633ae09e4b737f97d601186389fd801cc294a5217ea07b3e761c3bf13b` — tu do lai). Spec ghi base
  `086f1b7` (luc soan); so dong trong spec tinh tai do — doi chieu tai base that `90c101b`.
- Nguon loi: review doc lap #832 F03 tai mo; HINT goc cua reviewer ay: `HINT-review-832.patch`.

## Luot truoc
Luot 1 (`47b873a`): 2 P2 (F01 ham co the bi goi ma ca M3 khong thay; F02 chot tuyet doi o nhanh dung lai chua co ca hanh vi)
— `VERDICT-luot1.md`. Thay doi: `diff-tu-luot1.patch` (commit `0311db4`, ap HINT luot 1, chi test).
Kiem lai tung finding (dong that chua, co mo lo moi khong), roi review TOAN BO diff.

## Nhiem vu
1. Moi tieu chi M1-M4, A1-A4 cua SPEC.md: dat hay khong, bang LENH CHAY DUOC trong `cay-kho/` tai HEAD.
2. Moi khang dinh trong diff (code, comment, commit message `git log --format=%B BASE..HEAD`): do lai. Ghi ro cach tim.
3. Liet ke HET cac duong vao cua lop loi "PY[0] khong phai tep Python that / doi interpreter giua chung": ham, alias (khong
   kich hoat trong script khong tuong tac — kiem), builtin, `py -3` tren Windows/Git Bash (`type -P py`), PY dung lai tu
   luot cha (`CAI_CONG_CU_PY_CUA`, `exec`, `bash -a`, `SHELLOPTS`), `hash -p`, PATH co phan tu rong/tuong doi (`type -P` tra
   duong tuong doi => chot `/*` xu ly ra sao?), `BASH_ENV`, `CDPATH`. Do tung duong bang bash that. Ngoai pham vi spec thi ghi
   nhan, khong tinh.
4. Chay: `python3 .claude/dev/launcher_test.py`, `python3 .claude/dev/launcher_test.py --dot-bien`, `bash -n ops/cai_cong_cu.sh`,
   `bash ops/cai_cong_cu.sh rg`. `ops/cong_cu_test.py` rat dai (ban kinh 490 dot bien); chay neu kip, khong thi ghi KHONG DO DUOC.
   Dot bien them cua ban chay tren BAN SAO TAM ngoai `cay-kho/`; moi chot moi phai co dot bien lam ca dich do DUNG LY DO
   (assertion cua chinh ca — `bang(...)`/TinHieuChotCa, khong phai loi vo can).
5. Huong thu can soan noi dung nhay cam thi MO TA BANG LOI, khong tu soan.

## Bay moi truong da biet (ghi KHONG DO DUOC kem ly do)
- Sandbox Codex co the de lai `/tmp/.git` rong; khi ay 11 ca `r484_*` do vi "Codex home is inside a repository". Hoi
  `ls -d /tmp/.git` truoc khi ket luan; so voi base cung dieu kien.
- Khong co mang.

## Ghi VERDICT.md TANG DAN (thu muc hien tai, ngoai `cay-kho/`)
Dong 1 `verdict: dang_lam` ngay khi bat dau. Cuoi cung: dong 1 `verdict: approve` hoac `verdict: changes_requested`;
dong 2 `reviewed_sha: 0311db45d5786c3d4a1c05fec1375aec9e727249`; dong 3 `spec_sha256: <tu do>`; mot dong `Ket qua: <n> P0, <n> P1, <n> P2, <n> P3.`
```
## BANG NGHIEM THU   | tieu chi | lenh | output | dat? |
## BANG DO           | khang dinh | diff khai | do duoc (lenh) | khop? |
## BANG TEST         | bo | N/M | bo qua |
## BANG SAN          (>= 6 huong DOC LAP, moi huong co LENH + OUTPUT THAT; LOI | KHONG PHAI LOI | KHONG DO DUOC)
### <slug>  [P0|P1|P2|P3]  <tieu de>
TEP/DONG: / VAN DE: / DA THU NGHIEM: / DO TIN:
```
P0/P1 = sai hanh vi hoac khang dinh sai do duoc; P2 = khai rong hon phep do / chot thieu rang; P3 = dien dat.
Goi y va (CHI tep TEST, packet sensitive) vao `HINT.patch` (patch -p0 tu `cay-kho/`).

## Rang buoc
CHI DOC + DO. KHONG sua `cay-kho/`, KHONG push, KHONG goi mang, KHONG dung credential that.
