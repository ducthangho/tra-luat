# NHIEM VU REVIEWER — packet #674 CI-DUONG-NHANH-HO-SO (ban dac ta r2), luot {{ROUND}}

Ban la REVIEWER (Codex, doc lap voi executor la Claude). Khong tu sua gi trong cay kho de "va". Ban co bo nho lam viec
`{{R}}` (workspace-write, KHONG co mang). Dat `export TMPDIR={{R}}/tmp` truoc khi chay bat ky lenh nao dung thu muc tam.

## Doi tuong review
- Cay kho (clone day du, DA checkout dung head): `{{R}}/cay`, head = `{{SHA}}` (detached). Mirror bare: `{{R}}/kho.git`.
- Diff can review: `git -C {{R}}/cay diff 1741e0a1ab7ebce4b26912aefadca56ddfcdc691 {{SHA}}` — 4 tep: `.github/workflows/ci.yml`,
  `ops/ci_duong_nhanh.py`, `ops/ci_duong_nhanh_test.py`, `.claude/dev/ci_dang_ky_test.py` (dung MOT dong them vao `DA_NOI`).
- Dac ta DA DONG BANG (LUAT, khong duoc sua, khong duoc "cai thien"): `{{R}}/goi/SPEC-r2.md` (sha256 {{SPEC_SHA}}). Doc TRON. Protocol:
  `{{R}}/cay/docs/PROTOCOL_DA_PHIEN.md` muc 8 va 8.3; quy ta cua kho: `{{R}}/cay/CLAUDE.md`.
- Packet la `sensitive` (workflow/CI authority). Chu kho yeu cau ngưỡng: **0 P1, 0 P2, 0 P3** moi duoc `approve`.
- {{PREV_DOAN}}

## Hai truc
1. **Spec**: M1–M4 va nghiem thu 1–11 cua SPEC-r2 (muc 11 chi do duoc tren PR that: neu executor khai dat thi la finding).
   Chi ra cho nao code LECH dac ta, hoac dac ta tu mau thuan / thieu (ghi la "DAC TA", khong bat executor sua dac ta).
2. **Standards/Security**: fail-open, cong khong noi doi (vang mat trong nhu xanh), if: sai lop, bo phan loai bi lam sai duoc,
   test khong co rang, dot bien bi "giet" khong dung ly do (tin dung gia), doc lap nen (Linux/Windows), shell/YAML injection.

## Phan chung DA DAT SAN trong cay — CHAY CHUNG, roi DOT BIEN ban va de do rang (KHONG can soan noi dung moi)
Trong `{{R}}/cay` (moi lenh KHONG can mang):
- `python3 -B ops/ci_duong_nhanh_test.py`  (mong `CA: N/N` va `DOT BIEN: M/M` bang nhau, `TU KIEM PHAN HANG: DAT`, `TONG: DAT`; ~1-1,5 phut.)
- `python3 -B .claude/dev/ci_dang_ky_test.py`  (mong `DANG KY: 23/23`, `PHAN CHUNG: 938/938`, `TONG: DAT`)
- `actionlint .github/workflows/ci.yml` (co shellcheck)  ·  `python3 -m ruff check --no-cache --select F ops/ci_duong_nhanh.py ops/ci_duong_nhanh_test.py`
- `python3 -B {{R}}/goi/do_lai_so.py` (do lai cac so trong docstring; xem `{{R}}/goi/DO_LAI.md` — bang do nay TU KHAI gioi han cua no;
  **moi khang dinh dinh luong ban tim ra ma bang do bo sot deu tinh la finding**).
"DOT BIEN ban va" nghia la: tren MOT BAN SAO TAM (`cp -r` mot phan cay vao `{{R}}/tmp/...`, khong dong vao `cay/`), doi mot dieu kien/
allowlist/`if:` roi chay lai bo test de xem no co DO dung ly do khong. Liet ke dot bien SONG SOT (neu co) trong verdict.
**Huong nao can ban tu soan noi dung mang tinh tan cong/dung duong thoat khoi cay thu muc thi KHONG soan — MO TA BANG LOI**
de phien dieu phoi viet; moi phan chung can thiet DA co trong `ops/ci_duong_nhanh_test.py`.

## Tim theo PHAN LOP, khong tim theo tung loi
Moi finding thuoc dung MOT lop co `slug` kebab-case on dinh (giu slug qua cac luot). Bang lop: slug · cac bieu hien · hang cao nhat con mo ·
phuong an vá chung · phep kiem dong lop. Tu liet ke HET cac duong vao cua mot lop (khong dung lai o duong ban tim thay dau tien).
Moi finding kem **HINT VA CU THE**: tep, ham/doan, cach chot, va CHOT RIENG cho tung duong vao (kem dot bien lam chot do do).
Hint dang khoi `diff -u` ngay trong finding; KHONG ghi de tep nao trong `cay/`. Tep `HINT.patch` (tuy chon) chi cho tep TEST
(`patch -p0 --fuzz=0` tu goc cay, duong dan repo-relative, khong tien to a/ b/) va phai mang nhan nguyen van:
"chua chay tren cay that — executor tu ap, tu do, tu chiu trach nhiem commit". Voi `ci.yml`: chi mo ta huong + khoi diff trong finding.
Thieu hint thi finding chua day du.

## Bang san (>= 6 huong DOC LAP, moi huong co LENH + OUTPUT THAT)
```
HUONG <n>: <ten>
  gia thuyet : <neu ... thi ... sai>
  lenh       : <lenh da chay>
  output     : <output that, cat gon>
  ket luan   : LOI | KHONG PHAI LOI | KHONG DO DUOC
```
Goi y huong (KHONG phai tran — nghi them): ba cham vs GitHub that (base.sha cu, rebase, fork); `skipped` == dat cua required check khi
`chuan-bi` do; PR sua chinh bo phan loai/ci.yml tu chung thuc; `.py` duoi `ops/land/**`; symlink/mode; `if:` dung `always()`/`cancelled()`;
gate-registry / gate-registry khong bi bo tren PR ho so (co dung y khong); tren PR ho so mat cong nao (vd. `t27` chi muc `ops/reviews`
README) va push master co bat lai khong; ma tran `windows` gan nhan; concurrency/cancel; `kiem-re` sai duong (false-red / false-green);
tinh dung cua so 345/63/8; cac `if:` cua gate-ops khi `runner.os` la Windows; log `DUONG_NHANH` dung y dac ta.

## Ket qua — GHI DAN VAO `{{R}}/out/VERDICT.md` (tao ngay tu dau, cap nhat sau moi huong; luot bi cat van con phan da ghi)
Dong 1-3 dung dang:
```
verdict: approve|changes_requested|blocked
reviewed_sha: {{SHA}}
Reviewed commit: {{SHA}}
```
Roi: `## DOI CHIEU LUOT TRUOC` (tu luot 2: tung finding luot truoc -> DA VA THAT / VA HO / VA SINH LOI MOI / CHUA VA, kem bang chung ban TU DO),
`## BANG LOP`, `## BANG SAN`, `## BANG DO` (khang dinh -> dao khai -> do duoc -> khop?), roi tung finding:
```
### <slug>  [P0|P1|P2|P3]  <tieu de mot dong>
TEP/DONG:
VAN DE:
DA THU VA: co/khong — <mo ta HINT>
DA THU NGHIEM: <lenh + ket qua, hoac KHONG DO DUOC + ly do>
DO TIN: cao/vua/thap
```
Cuoi cung: dong `TONG: P0=<n> P1=<n> P2=<n> P3=<n>` va so lop. `approve` chi khi P0=P1=P2=P3=0 va moi nghiem thu 1–10 co bang chung
ban tu chay. Neu bi ngan giua chung, phan da ghi van la du lieu — nhung mot luot bi cat KHONG phai `approve`.
Khong dung `PONG`/tra loi chung chung; khong khai da chay lenh ma ban chua chay.
