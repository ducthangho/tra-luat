# Cross-review — PR ducthangho/tra-luat#1080 (packet #1077 DOCTOR-ENOEXEC-BI-CHE, r1/g1) — luot Codex 8/10

## Vai
Ban la Codex, reviewer khac ho voi executor (Claude). Lease `wp1077-r1-g5-claude`, review_class `sensitive`.
Tran: 10 loi goi Codex (chu kho nang 2->4->5->10, lease wp1077-r1-g4-claude); day la loi goi 8.

## Doi tuong
- `reviewed_sha`: `7879902ac11f14c5f67708ee058f6cb0e7916b55`. Base `086f1b7343fc1d778e50797e6c9ca0964b11a755`.
- Diff: `diff.patch` (= `git diff BASE HEAD`), `numstat.txt`. 2 tep: `.claude/dev/launcher.py`, `.claude/dev/launcher_test.py`.
- Dac ta dong bang: `SPEC.md` (sha256 `eabbb725650addad531429d48801667f2ef05a6090c00123d1d4146c7b89c3f3` — tu do lai).
- Nguon loi: review doc lap #823 F1 (tep khong shebang: bash chay lai bang /bin/sh khi ENOEXEC, subprocess thi nem OSError).

## Luot truoc va QUYET DINH PHAM VI cua chu kho
- Luot 1 (`e61def4`): F1 P1, F2 P1, F3 P2 — `VERDICT-luot1.md`. Luot 2 (`dcfb011`): F1 P1 (con lai), F4 P1, F5 P1 — `VERDICT-luot2.md`.
- Thay doi tu luot 2 toi luot 3: commit `e6bf386`, `57e2d4a` (doc commit message bang `git log`).
- CHU KHO da quyet dinh (31-10-2026, nang tran + THU HEP PHAM VI): F1 phan con lai — `_git` (dung chung voi duong run) va
  `_do_codex_song` (spawn trong `codex_cred.py`, ngoai write set) — KHONG va trong packet nay; da tach thanh Issue #1083.
  Vi vay: KHONG tinh hai duong do la finding mo cua packet NAY; NHUNG moi loi khai trong diff/commit/docstring noi "moi
  probe"/"phu toan doctor" ma khong neu gioi han ay thi VAN la finding. Kiem docstring helper va ca cau truc noi dung khong.
- F5: so dong dinh chinh se ghi o handoff; commit `e6bf386` co ghi so do tai head do — do lai.
- Luot 3 (`57e2d4a`): F4 P1 (PATH rong = cwd), F6 P1 (loi khai t103) — `VERDICT-luot3.md`; thay doi tu luot 3: `diff-tu-luot3.patch` (commit `1027f85`, ap HINT luot 3).
- Luot 4 (`1027f85`): F4 P1 (abspath xoa `..` truoc symlink), F1 P2 (chu thich bang dot bien) — `VERDICT-luot4.md`; thay doi tu luot 4: `diff-tu-luot4.patch` (commit `4fa4720`, ap HINT luot 4).
- Tran dong them: chu kho nang 300 -> 330 (lease g3/g4); do lai so dong them BASE..HEAD.
- Luot 5 (`4fa4720`): F4 P1 lan thu tu (ghep cwd: ENAMETOOLONG, doi `$0`, dung o ban thieu interpreter) — `VERDICT-luot5.md`.
  Executor DOI THIET KE (commit `01b9734`, `diff-tu-luot5.patch`): helper tu duyet `os.get_exec_path(env)` nhu execvp glibc,
  ung vien giu nguyen dang, `executable=` giu argv[0], loi tim kiem => ung vien sau, ENOEXEC => /bin/sh chinh ung vien.
  Kiem DOI CHIEU thiet ke moi voi glibc execvp va bash THAT tren ma tran day du (PATH rong/tuong doi/`..`/symlink/vang,
  env=None/env thieu PATH, EACCES/ENOENT/ENOTDIR/ENOEXEC/interpreter vang, ten co `/`, cwd dai, `$0`, thu tu loi ném cuoi,
  /bin/sh vang), va kiem cac caller (doctor) khong doi phan loai. Cac sua do gia luot 2 da GO (argv[0] lai la ten tran).
- Luot 6 (`01b9734`): F4 P1 (nuot loi exec ETXTBSY/ELOOP, chuoi ung vien lech glibc, $0) — `VERDICT-luot6.md`.
  Executor (commit `c4af726`, `diff-tu-luot6.patch`) cai theo `__execvpe` glibc: tap errno tiep, chuoi `<phan tu>/<ten>`,
  phan tu rong => `<ten>` (execve qua `./<ten>`), bo phan tu dai, uu tien EACCES. Docstring khai GIOI HAN con lai.
  Gom ca de giu tran 330 dong; kiem cac ca gop van do DUNG tung tinh chat (dot bien rieng cho moi tinh chat).
- Luot 7 (`c4af726`): F4 P1 hai mat — `VERDICT-luot7.md`. Mat UTF-8 (str.encode strict) da va bang os.fsencode (commit
  `2320f27`). Mat `$0` cua shebang qua phan tu PATH RONG (`./<ten>` thay `<ten>`): CHU KHO MIEN TRU W-1077-1 (lease g5,
  tep `LEASE-g5.yaml`, khoa `mien_tru`, `reviewer_khong_tinh_la_finding: true`) — KHONG tinh la finding. Pham vi mien tru
  CHI truong hop do; moi lech glibc khac van la finding. Tran dong them nang 330 -> 345 (lease g5).
- Thay doi tu luot 7: `diff-tu-luot7.patch` (commit `2320f27`, `7879902`).
- F4 da mo lai 3 luot lien tiep (luot 2, 3, 4) — moi lan mot bien the duong dan. Truoc khi ket luan, LIET KE HET cac dang PATH/ten ma execvp glibc xu ly (rong, tuong doi, `..`, symlink, ten co `/`, PATH vang, env=None, thu muc khong doc duoc, tep khong co quyen x o ban dau) va DO tung dang voi bash + glibc execvp that, de luot nay dong ca lop chu khong chi mot bien the.
Kiem lai TUNG finding cu (dong that hay chua, va ban va co mo lo moi khong), roi review TOAN BO diff.

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
dong 2 `reviewed_sha: 7879902ac11f14c5f67708ee058f6cb0e7916b55`; dong 3 `spec_sha256: <tu do>`;
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
