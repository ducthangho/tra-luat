# Cross-review — PR ducthangho/tra-luat#1080 (packet #1077 DOCTOR-ENOEXEC-BI-CHE, r1/g1) — luot Codex 2/2

## Vai
Ban la Codex, reviewer khac ho voi executor (Claude). Lease `wp1077-r1-g1-claude`, review_class `sensitive`.
Tran: 2 loi goi Codex cho packet nay; day la loi goi 2 (CUOI).

## Doi tuong
- `reviewed_sha`: `dcfb0115cef9defa0af35c7aca0537d75b87dd17`. Base `086f1b7343fc1d778e50797e6c9ca0964b11a755`.
- Diff: `diff.patch` (= `git diff BASE HEAD`), `numstat.txt`. 2 tep: `.claude/dev/launcher.py`, `.claude/dev/launcher_test.py`.
- Dac ta dong bang: `SPEC.md` (sha256 `eabbb725650addad531429d48801667f2ef05a6090c00123d1d4146c7b89c3f3` — tu do lai).
- Nguon loi: review doc lap #823 F1 (tep khong shebang: bash chay lai bang /bin/sh khi ENOEXEC, subprocess thi nem OSError).

## Luot truoc
Luot 1 (tren `e61def4`) ra changes_requested: F1 P1 (probe KHA_NANG con spawn tran), F2 P1 (loi khai bash/execvp),
F3 P2 (test khong khoa doi so). Verdict day du o `VERDICT-luot1.md`; thay doi tu luot 1: `diff-tu-luot1.patch`.
Executor khai: F1 dong cho codex status, llm x3, gh auth status, gh api, claude mcp get + giai ten tran theo PATH;
NGOAI pham vi co chu dich: `_git` (duong run dung chung), `_do_codex_song` (spawn nam o codex_cred.py, ngoai write set).
Kiem lai TUNG finding (dong that hay chua, va ban va co mo lo moi khong), roi review TOAN BO diff nhu luot dau.

## Nhiem vu
1. Moi tieu chi M1-M4 va A1-A4 cua SPEC.md: dat hay khong, bang LENH CHAY DUOC trong `cay-kho/` tai HEAD.
2. Moi khang dinh trong diff (code, comment, docstring, commit message `git log -1 --format=%B HEAD` trong `cay-kho/`): do lai.
   Danh sach ban tu lap se thieu — ghi ro cach tim.
3. Liet ke HET cac duong probe cua `doctor` (va cac cho khac trong launcher.py goi mot cong cu bang duong dan ma ket qua quyet
   dinh nhan DUNG_DUOC/THIEU/BI_CHE) — co duong nao con dung `subprocess.run` tran ma le ra phai do nhu shell khong? Neu co
   va no NAM TRONG pham vi spec thi la finding; ngoai pham vi (spec muc "Ngoai pham vi") thi ghi nhan, khong tinh.
4. Ngu nghia: so sanh voi hanh vi THAT cua bash va execvp cua glibc khi ENOEXEC (dung bash that trong container de doi chieu):
   doi so, `$0`, tep co bit x nhung la nhi phan sai kien truc, tep rong 0 byte, tep chi co BOM, khi `/bin/sh` vang mat,
   timeout cua luot chay lai, Windows. Moi lech co hau qua that la finding.
5. Chay: `python3 .claude/dev/launcher_test.py` va `python3 .claude/dev/launcher_test.py --dot-bien` (N/M; BO QUA ghi rieng).
   Dot bien them cua ban: chay tren BAN SAO TAM ngoai `cay-kho/`; moi chot moi phai co dot bien lam ca dich do DUNG LY DO
   (assertion cua chinh ca — `bang(...)`/TinHieuChotCa, khong phai loi vo can).
6. Huong thu can soan noi dung nhay cam thi MO TA BANG LOI, khong tu soan.

## Bay moi truong da biet (ghi KHONG DO DUOC kem ly do, dung doc thanh hoi quy)
- Sandbox Codex co the de lai `/tmp/.git` rong; khi ay mot so ca `r484_*` do vi "Codex home is inside a repository".
  Hoi `ls -d /tmp/.git` truoc khi ket luan; so voi base cung dieu kien.
- Khong co mang.

## Ghi VERDICT.md TANG DAN (thu muc hien tai, ngoai `cay-kho/`)
Dong 1 `verdict: dang_lam` ngay khi bat dau. Cuoi cung: dong 1 `verdict: approve` hoac `verdict: changes_requested`;
dong 2 `reviewed_sha: dcfb0115cef9defa0af35c7aca0537d75b87dd17`; dong 3 `spec_sha256: <tu do>`;
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
