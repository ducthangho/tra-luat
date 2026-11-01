# Cross-review — packet #1122 LAUNCHER-TEST-WINDOWS-TIN-DUNG-GIA (r1, lease g1) — luot Codex 1/10

## Vai
Ban la Codex, reviewer khac ho voi executor (Claude). Lease `wp1122-r1-g1-claude`, review_class `sensitive`.
Tran 10 loi goi Codex (ADR-0055); day la loi goi 1.

## Doi tuong
- `reviewed_sha`: `30ee4ae1b62170c86b8c75e6b0c73663ab934d88`. Base `c82047da4d6f9546ce1d68282c37acf9567b74bc`.
- `cay-kho/` = clone tai HEAD. `diff.patch` = `git diff BASE HEAD`, `numstat.txt` (1 tep: `.claude/dev/launcher_test.py`).
- Dac ta dong bang: `SPEC.md` (sha256 `198e06f0f7ef6659fb711ef02ff3558ba5c4a63da1c7127b559c5fd8b0fdacb8` — tu do lai).
- Commit message: `git -C cay-kho log --format=%B BASE..HEAD`.

## LECH SPEC DA DUOC CHU KHO DUYET (khong tinh la finding; nhung KIEM xem lam co dung khong)
SPEC muc tieu 1-2 chi noi `assert` tran. Sau khi do N0 tren Windows, chu kho duyet MO RONG qua AskUserQuestion:
(a) `raise AssertionError(...)` tuong minh trong ca @ca cung la tin dung gia (dong SAI `g2_windows_directory_pin_access`
den tu duong nay) => doi sang `bang(False, ...)`, ca khoa AST cam ca hai duong, danh sach cho phep 3 ca co y;
(b) goc t73 DA DO (run 41328709141, log co `UnicodeDecodeError` cp1252 trong `_readerthread`): `chay()` `text=True`
khong `encoding` => `r.stdout` None => `json.loads` TypeError. Va MOI loi goi subprocess `text=True` co con la Python
(`PY`/`py`) — 14 cho — them `encoding="utf-8", errors="replace"`; ca khoa AST + dot bien. Con shell/git/he thong de nguyen.

## Bang chung executor da co (do lai neu nghi ngo; Windows ban KHONG chay duoc — doc mo ta)
- N0 Windows run 41328709141 (head 4423d18, chi muc tieu 3): `432/436`, dong `doctor_bo_do_bash` co
  `t73(TypeError: the JSON object must be str, bytes or bytearray, not NoneType)`.
- A3 Windows run 41330126129 (head 30ee4ae, job nhan windows-latest, runner_id 1000032894): `DOT BIEN: 440/440 dat
  (118 khong do duoc)`, suite `281/281 (bo qua 74, hong 0)`.
- Linux N0' base c82047d: `340/350 (bo qua 2, hong 10)`, `--dot-bien 523/548`. 10 ca hong deu duong `launcher.py run`
  (r09, r15, r925_*, r926_*, r927_*) rc=1 — do moi truong container, do san tren base. Executor dang do lai A/B cung lenh.

## Nhiem vu
1. Moi tieu chi N0, N0', A1-A5 cua SPEC.md (tinh ca phan mo rong da duyet): dat hay khong, bang LENH CHAY DUOC trong
   `cay-kho/` tai HEAD.
2. Moi khang dinh trong diff (code, comment, docstring, commit message): do lai. Danh sach ban tu lap se thieu — ghi ro
   cach tim.
3. LOP LOI "nhieu duong vao": con DUONG NAO KHAC de mot ca @ca chet bang AssertionError KHONG phai `TinHieuChotCa` cua
   chinh no ma ca khoa AST khong bat? Thu it nhat: helper (khong @ca) bi ca goi co `assert`/`raise AssertionError`;
   `raise AssertionError` dang `Name` khong goi; bien bi gan `AssertionError` roi raise; ham long trong ca; `pytest`/
   `unittest` style (`self.fail`, `assertEqual`); ca dang ky KHONG qua decorator `@ca` (vd `CA.append`, gan thang) ma co
   assert. Voi moi duong: co ton tai trong cay HEAD khong (dem), va ca khoa co bat duoc khong.
4. Giai ma: con loi goi nao co con la Python (hoac launcher) ma ca khoa `r1122_con_python_giai_ma_utf8` bo sot (vd
   `[sys.executable, ...]`, bien list dung san roi truyen, `Popen` voi `universal_newlines=True`, `check_output`)?
   `errors="replace"` co che mat mot lan giet that nao khong (ca nao do dung byte/ky tu thay the)?
5. Thong diep `loi` cat 160: co lam vo khop `phai_chet`/neutral (vd so sanh chuoi chi tiet o dau do), hoac lam lo noi dung
   nhay cam vao log CI (thong diep ngoai le co the chua gi)?
6. Chay: `python3 .claude/dev/launcher_test.py`, `python3 .claude/dev/launcher_test.py --dot-bien` (N/M; BO QUA ghi rieng).
   Dot bien them cua ban: chay tren BAN SAO TAM ngoai `cay-kho/`; moi chot moi phai co dot bien lam ca dich do DUNG LY DO
   (`TinHieuChotCa` cua chinh ca).
7. Huong thu can soan noi dung nhay cam thi MO TA BANG LOI, khong tu soan.

## Bay moi truong da biet (ghi KHONG DO DUOC kem ly do, dung doc thanh hoi quy)
- Sandbox Codex co the de lai `/tmp/.git` rong; khi ay 11 ca `r484_*` do vi "Codex home is inside a repository". Hoi
  `ls -d /tmp/.git` truoc khi ket luan; so voi base cung dieu kien.
- 10 ca duong `launcher.py run` do san tren base trong container (xem tren). Khong co mang.
- Neu dia day: don ban sao tam cua chinh ban.

## Ghi VERDICT.md TANG DAN (thu muc hien tai, ngoai `cay-kho/`)
Dong 1 `verdict: dang_lam` ngay khi bat dau. Cuoi cung: dong 1 `verdict: approve` hoac `verdict: changes_requested`;
dong 2 `reviewed_sha: 30ee4ae1b62170c86b8c75e6b0c73663ab934d88`; dong 3 `spec_sha256: <tu do>`;
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
