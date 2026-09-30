verdict: changes_requested
reviewed_sha: af1165d04977f2e3de1fa0fdbaa9a1775dd9bd30
Reviewed commit: af1165d04977f2e3de1fa0fdbaa9a1775dd9bd30

Nguong sensitive cua chu kho: **0 P0/P1/P2/P3**. Con **3 P3**, khong P0/P1/P2. Ca ba la lo RANG KIEM THU: hanh vi cua HEAD o
moi dau vao duoc neu deu DUNG (do truc tiep), nhung dot bien lam hong hanh vi do van qua TOAN BO suite (FULL rc=0, TONG DAT).

Reviewer: Claude Opus 5.5 subagent, ngu canh moi, doc lap voi executor nhung CUNG provider => assurance `same_provider`
(KHONG phai `cross_approved`). Model/effort thuc su phuc vu: KHONG DO DUOC. Verdict nay khong cap quyen land, khong xac nhan
#668 da land (do: `git log 89fc4fa` khong co commit #668 nao; SPEC-r2 Q5 dat dieu kien land sau #668 — dieu kien land, khong phai finding).

PROMPT.md sha256 da kiem khop: `ad275679dc3fdc9d80e27ac42195eb542bcb26eda52210fa52649bb34daab1ed`.
SPEC-r2 sha256 `b6e719c999d5990f987628963c248b1ac53d377dfa5b668ac06adce76981da57` khop; doc tron. Ap dung erratum D1/D2 nhu hanh vi DUOC DUYET.

Moi truong: Linux, Python 3 he thong (CI dung 3.12), actionlint 1.7.7, ShellCheck 0.9.0, Ruff 0.16.9 (workflow ghim 0.15.15).
Khong mang, khong GitHub, khong Windows. `cay/` khong bi sua: moi dot bien/fixture o `tmp/` (ban sao `tmp/head` = cp -a cua cay);
cuoi luot `git -C cay status --short` rong, HEAD van af1165d. Registry va tl selftest can `GIT_CONFIG_COUNT=1
GIT_CONFIG_KEY_0=commit.gpgsign GIT_CONFIG_VALUE_0=false` (cau hinh tien trinh, khong sua repo) — moi truong, khong phai delta.

## DOI CHIEU LUOT TRUOC

Nguon: `goi/LUOT-TRUOC-VERDICT.md` (luot 6, reviewed abcafde). Tu do lai tren af1165d:

| Finding luot 6 | Phan loai | Bang chung tu do (luot 7) |
|---|---|---|
| `chot-yaml-chi-do-su-hien-dien` P2 — runner bo `CA[ten]()` van FULL xanh | **DA VA THAT** | Dot bien tu dung (thay `CA[ten]()` bang `pass`) tren ban sao: `--mot-ca t92` rc=3 `DO:t92…runner/DAT: phai goi dung mot lan…calls=[]`; `--mot-ca t91` rc=3 `DO:t91…entry/DAT…` (khong co REVIEW_SENTINEL_CALLED). FULL rc=1 TONG DO (out/p6-runner.log). Luu y: dong `CA: 63/63 dat` van in ra vi runner hong khong goi ca nao — nhung TONG DO, rc=1; chot dung la t91/t92 qua `--mot-ca`, va chung co trong DOT_BIEN (`test_runner_khong_goi_ca`, …) bi GIET. |
| cung lop — entrypoint doi rc 1->0 | **DA VA THAT** | Dot bien `raise SystemExit(0 if _rc == 1 else _rc)`: `--mot-ca t91` rc=3 `entry/DO: rc=0…TONG: DO` (bat dung ly do: ma thoat sai). t93 van rc=0 (dung — t93 khong canh cua nay, t91 canh). out/p6-exit.log |
| `bang-do-thieu-neo-va-thieu-kiem-ke` P3 — them dong KIEM KE sai van xanh | **DA VA THAT cho nhan `KIEM KE:`**; **VA HO o cap LOP** | Dot bien them `print("KIEM KE: ca hanh_vi=999 = 999")`: `--mot-ca t94` rc=3 dung thong diep (out/p6-kiemke.log). NHUNG dong tong ket khac cung loai — `TU KIEM PHAN HANG:` (so mau rc/dot bien that, va chu DAT/DO) — khong co neo: in so sai van FULL TONG DAT. Xem finding P3 ben duoi. |
| `kiem-lease-bo-sot-duong-vao` (khong mo) | **van dong** cho lease; lop duoc TONG QUAT HOA thanh `kiem-re-bo-sot-duong-vao` | Dot bien `continue`->`break` o kiem_lease bi t21 giet (out/k3.log). Cung hai cua ay (duoi `.yml`, tep da xoa dung truoc) o `kiem_yaml` thi KHONG co chot — finding P3 moi. |
| `diff-check-tu-ha-nguong` (khong mo) | **MO LAI, P3** (khac chieu) | Luot 6 do HEAD dung o ca ba loai; KHONG do rang. Dot bien bo `-space-before-tab` khoi `CAU_HINH_WHITESPACE` => FULL 63/63 + 151/151 TONG DAT (out/d1-narrow-full.log). |
| `dac-ta-bo-mat-kiem-du-lieu-ho-so` | van dong | kiem_ke.py: ba ca du lieu that loi=[] 4.9s; t22/t22b trong suite dat. Ra soat them `packet_loop_test.py`, `gate_lifecycle_test.py`, `tl_selftest.py`: khong ca nao doc NOI DUNG ho so that cua ops/{land,leases,reviews,specs} ma bi bo o duong nhanh (packet_loop dung kho gia `_kho_gia`; tl_selftest chi nhac ops/specs trong docstring). |
| `fixture-lease-phu-thuoc-actor-ci` | van dong | t23 dat trong FULL. |
| `tin-dung-dot-bien-khong-co-ca-dich` | van dong | t97/t99 dat; dot bien `phan_hang` bo so ten ca dich => FULL rc=1 `TU KIEM PHAN HANG: DO` (out/c1.log); dot bien nhanh `--mot-ca` doi ngoai le thuong thanh rc=3/DO => FULL rc=1 (out/c2.log). |

D1/D2 khong ghi finding chinh sach. D2 hien thuc: `MA_KIEM_HET_HAN` goi `lp.kiem(_doc_yaml(tep), tep, '.', bo_qua_han=True)`,
`lenh_check` goi `kiem(_doc_yaml(tep), tep, goc='.')` qua `--root .` — khac DUY NHAT o `bo_qua_han`; trong `kiem` co dung MOT
dieu kien dung `bo_qua_han` (`if not bo_qua_han and han <= now`). Khong bo them chot nao. D1 hien thuc: dung ba loai duoc duyet,
va do chinh la TOAN BO ba loai mac dinh-bat cua git, nen "tat rong hon" khong the xay ra qua `core.whitespace`; chieu con lai
(tat HEP hon) la finding `diff-check-tu-ha-nguong`. `dependency-failure-skips-required-checks`: giu DONG theo chi thi.

## BANG LOP

| Slug | Bieu hien / duong vao da ra | Hang cao nhat con mo | Va chung | Phep kiem dong lop |
|---|---|---|---|---|
| `chot-yaml-chi-do-su-hien-dien` | top/workflow/job/buoc/if/runner/matrix/needs/coe/timeout/than run moi (y01–y16); loader; cay duoi do (t95); runner goi ca (t92); entrypoint rc (t91); main ket luan (t93); harness phan hang (tu kiem MAU_RC); nhanh `--mot-ca` (tu kiem KeyError) | **khong con** | — | dot bien runner/entry/phan_hang/--mot-ca deu DO dung ly do (out/p6-*.log, out/c1.log, out/c2.log) |
| `bang-do-thieu-neo-va-thieu-kiem-ke` | cac dong tong ket main in: `CA:` (t93) · `DOT BIEN:` (t93) · `KIEM KE:` (t94 tap dung) · **`TU KIEM PHAN HANG:` (khong neo)** · `TONG:` (t93 dong cuoi) | **P3** | doi TAP dong mang nhan tong ket == danh sach dung, moi nhan | t93 so TAP 5 dong o kich ban sach + dong TU KIEM o kich ban tu-kiem-hong; dot bien in so sai / in DAT bat ke phai do |
| `diff-check-tu-ha-nguong` | nguong D1 = dung ba loai: rong hon (khong the qua core.whitespace), hep hon: bo tung loai eol/eof/**sbt** | **P3** | fixture MOT tep cho MOI loai, kiem THO tung tep theo tung loai | ba dot bien bo tung loai deu phai giet t20d |
| `kiem-re-bo-sot-duong-vao` (tong quat hoa `kiem-lease-bo-sot-duong-vao`) | lease: duoi .yml (t20g), xoa/break (t21), het han/con han (t20e/f, t21) — du; **YAML: duoi .yml, tep da xoa dung truoc** — khong chot | **P3** | moi cua vao cua moi kiem re mot ca qua `kiem_re` that | dot bien `.yml`, `continue->break` o kiem_yaml phai giet ca moi |
| `dac-ta-bo-mat-kiem-du-lieu-ho-so` | ca du lieu lease_publish_test; cac suite bi bo khac | khong mo | — | ra soat grep + t22/t22b |
| `fixture-lease-phu-thuoc-actor-ci` | actor trong/ngoai tien trinh | khong mo | — | t23 |
| `tin-dung-dot-bien-khong-co-ca-dich` | dich rong/la/iterator/baseline/ten ca/rc | khong mo | — | t97/t99/tu kiem |

Tong: 7 lop; 3 con mo (moi lop 1 P3), 4 khong con finding trong pham vi local.

## BANG SAN

HUONG 1: Pham vi diff va phan them cua master
  gia thuyet : packet sua ngoai write set, hoac hai tep them so baseline 1741e0a khong phai cua master.
  lenh       : `git -C cay diff --name-only 89fc4fa af1165d`; `git diff --numstat 1741e0a af1165d -- .claude/dev/ci_dang_ky_test.py`; `git rev-parse 89fc4fa:F af1165d:F` cho ops/lease_publish_test.py, ops/specs/t131-deadline-dem-spawn.md; `git log -1 --format='%P' 7b112ad`
  output     : 4 tep dung write set; numstat `1 0`; blob 694cca5b… == 694cca5b…, 1a99adbf… == 1a99adbf…; merge 7b112ad cha = d7c819f + 89fc4fa.
  ket luan   : KHONG PHAI LOI.

HUONG 2: Doi chieu luot 6 bang dot bien tu dung
  gia thuyet : ba dot bien luot 6 van song.
  lenh       : `python3 -B tmp/tools/mut.py runner_no_call|exit_one|kiemke_extra ops/ci_duong_nhanh_test.py <cu> <moi> --mot-ca … [--full]`
  output     : runner: t92 rc=3, t91 rc=3, FULL rc=1; exit: t91 rc=3 (`entry/DO: rc=0`); kiemke: t94 rc=3 (out/p6-*.log).
  ket luan   : KHONG PHAI LOI (da va that).

HUONG 3: Rang cua D1 — tung loai khoang trang
  gia thuyet : neu cai dat thu hep D1 (bo mot trong ba loai) thi suite phai do; neu khong, hanh vi duoc duyet co the hoi quy im lang.
  lenh       : mut.py bo `-space-before-tab` / `-blank-at-eof` / `-blank-at-eol` + `--mot-ca t20d/t20c/t20a/t23`; sau do `--full` cho ca sbt; do truc tiep HEAD bang kho git tam (`a\n \tb\n`).
  output     : sbt: t20d rc=0, FULL rc=0 63/63 151/151 TONG DAT; eof: t20d rc=3; eol: t20d rc=3 (out/d1-narrow*.log). HEAD: `--check` tho rc=2, `kiem_diff_check` = [].
  ket luan   : LOI P3 (`diff-check-tu-ha-nguong`).

HUONG 4: Cac cua vao cua kiem-re (YAML, lease)
  gia thuyet : cua `.yml` va `tep da xoa` da duoc chot cho lease (t20g/t21) thi cung phai duoc chot cho YAML.
  lenh       : mut.py k1 (`continue`->`break` trong kiem_yaml), k2 (bo `.yml` trong kiem_yaml), k3 (`continue`->`break` trong kiem_lease), deu `--full`; do HEAD bang `kiem_yaml({"ops/land/a.yaml"(da xoa), "ops/land/b.yml"(hong)})`.
  output     : k1 FULL rc=0 TONG DAT; k2 FULL rc=0 TONG DAT; k3 FULL rc=1 (t21 do). HEAD tra `["YAML khong parse duoc: 'ops/land/b.yml': ParserError…"]` (out/k1.log, k2.log, k3.log).
  ket luan   : LOI P3 (`kiem-re-bo-sot-duong-vao`). Anh huong hien tai thap: `git ls-files` ho so co 0 tep `.yml` (land 14 yaml, leases 113, reviews 189); lich su co 9 lan xoa tep ho so.

HUONG 5: Cac dong tong ket cua main (lop bang-do)
  gia thuyet : luot 6 chi neo `KIEM KE:`; cac dong tong ket khac mang so/ket luan co the noi sai ma van xanh.
  lenh       : mut.py `tukiem_so_sai` (in `{len(MAU_RC) + 1} mau rc`) `--full`; `tukiem_luon_dat` (in `DAT` bat ke loi) `--mot-ca t93/t94/t91`.
  output     : FULL rc=0, `TU KIEM PHAN HANG: DAT (6 mau rc, 3 dot bien that)`, TONG DAT (out/b1.log); luon-DAT: t93/t94/t91 deu rc=0 (out/b2.log).
  ket luan   : LOI P3 (`bang-do-thieu-neo-va-thieu-kiem-ke`). `DO_LAI.md` dan chinh dong nay lam bang chung so mau rc/dot bien that.

HUONG 6: Harness phan hang va nhanh `--mot-ca` (lop tin-dung)
  gia thuyet : bo so ten ca dich trong phan_hang, hoac doi ngoai le thuong thanh rc=3, se cap GIET gia ma khong ai bat.
  lenh       : mut.py `ph_bo_ten`, `motca_ngoaile_thanh_do` `--full`.
  output     : ca hai FULL rc=1, `TU KIEM PHAN HANG: DO (5 mau rc, 3 dot bien that)`, TONG DO (out/c1.log, out/c2.log).
  ket luan   : KHONG PHAI LOI. (Ghi chu: t06 co `except (TypeError, ValueError, AttributeError)` doi thanh TinHieuChotCa — hep, co chu thich y do, t99 cho phep; dot bien `fail_open_dau_ra_khong_phai_bytes` chet qua duong nay. Trong san xuat `main` bat moi Exception => day_du, nen ten "fail_open" cua dot bien ay rong hon hau qua that; khong tinh P.)

HUONG 7: Nghiem thu 8/9/10 (actionlint, so dang ky, selftest, ruff)
  gia thuyet : cong do/sai so baseline.
  lenh       : `actionlint .github/workflows/ci.yml` (HEAD va tmp/base@1741e0a); ban sao chen `# ghi chu ${{ }}` vao than run kiem-re; `python3 -B .claude/dev/ci_dang_ky_test.py` o tmp/base va tmp/head; `python3 -B scripts/tl.py --selftest` o tmp/selftest-copy; `python3 -m ruff check --no-cache --select F …`.
  output     : actionlint HEAD rc=0, base rc=0, dot bien rc=1 `[expression]` dong 549; registry base `ĐĂNG KÝ: 22/22`, `PHẢN CHỨNG: 938/938`, TỔNG ĐẠT → HEAD `23/23`, `938/938`, TỔNG ĐẠT; tl selftest `1715/1715` rc=0; ruff: tep moi `All checks passed!`, tl.py 12 F821 (blob tl.py khong doi so master => delta 0).
  ket luan   : KHONG PHAI LOI.

HUONG 8: Allowlist va .gitattributes ben trong vung ho so
  gia thuyet : mot PR ho so tu mien `git diff --check` bang `.gitattributes` dat trong ops/{specs,…}/.
  lenh       : kho git tam: PR them `ops/specs/X.md` co dau xung dot + `ops/specs/.gitattributes` (`* -diff`); `phan_loai` va `kiem_diff_check`.
  output     : phan_loai = duong_nhanh; kiem_diff_check = [] (dau xung dot khong bi bat). Kho that da co 3 `.gitattributes` trong ops/reviews (chi `-whitespace`, van giu kiem dau xung dot).
  ket luan   : KHONG PHAI LOI — nam trong gioi han da khai ("Allowlist chan NHAM LAN, khong chan tac gia co y"; PR ho so qua review). Duong day du KHONG chay `git diff --check` nao, nen duong nhanh van nghiem hon. Mo ta bang loi, khong soan them noi dung.

HUONG 9: Ba cham / su kien / race giua job
  gia thuyet : gate job checkout commit khac commit ma chuan-bi phan loai.
  lenh       : doc ci.yml + hanh vi actions/checkout@v4 (fetch theo github.sha cho refs/pull/N/merge); suite t11 (ba cham), t12 (rename), t14 (xoa), t15 (thieu object) trong FULL.
  output     : ca t11–t15 DAT trong FULL 63/63.
  ket luan   : KHONG PHAI LOI trong mien do. Fork/rebase/base.sha cu tren GitHub: KHONG DO DUOC (khong mang) — dac ta chua_do_duoc 2/3.

HUONG 10: Log DUONG_NHANH theo nen va cong khong bi mat tren PR ho so
  gia thuyet : buoc liet ke noi "bo qua … vi diff chi gom" cho buoc von da bi `runner.os` bo; hoac PR ho so mat cong ma push master khong bat lai.
  lenh       : doc `IF_BUOC_CHUAN`/`BO_QUA`/than run bi khoa (y07, y14); `grep` release `_RELEASE_EXCLUDE_DIRS` chua `ops`.
  output     : tren ubuntu, dong "bo qua gate lifecycle selftest (nen khong co cgroup)" in du buoc ay von bi `runner.os != 'Linux'` bo; ten buoc tu mang nen, nen khong gay hieu nham. `ops` bi loai khoi goi phat hanh => bo release-check/bundle/golden/determinism tren PR ho so khong mat bang chung cua goi; push master van chay day du.
  ket luan   : KHONG PHAI LOI (quan sat).

HUONG 11: So dinh luong (bang do)
  gia thuyet : so trong docstring/DO_LAI troi.
  lenh       : `(cd cay && python3 -B ../goi/do_lai_so.py)`; `(cd cay && python3 -B ../goi/kiem_ke.py)`; `git for-each-ref | wc -l`.
  output     : 345 / 63 / 8; 113/113 lease dat; 565 ref hien tai; 35+16+3+9=63; 44+40+65+2=151; MAU_RC 5, TU_KIEM_DOT_BIEN 3; ba ca du lieu 4.9s.
  ket luan   : KHONG PHAI LOI cho so HEAD; xem BANG DO.

## BANG DO

| Khang dinh | Dau khai | Do duoc | Khop? |
|---|---|---|---|
| CA / DOT BIEN | output suite | 63/63; 151/151; TU KIEM DAT; TONG DAT; 41s | co |
| Phan nhom | dong KIEM KE | 35+16+3+9=63; 44+40+65+2=151 (kiem_ke.py) | co |
| `TU KIEM PHAN HANG: (5 mau rc, 3 dot bien that)` | DO_LAI "dong TU KIEM … in so … dem tu hai hang so" | 5 / 3 (kiem_ke.py) | so HEAD dung — NHUNG dong nay khong co neo: in so sai van xanh (P3) |
| 345/63/8, ~13% | docstring ci_duong_nhanh.py | 345/63/8; 8/63 = 12,7% | co (pham vi: 400 merge first-parent tu 1741e0a) |
| 6/113 clone mot nhanh vs 0/113 day du; 552 ref | docstring | 113/113 dat tren cay hien tai (565 ref); 6/113 khong tu do lai luot nay | 552 la so lich su; khong doc thanh so hien tai |
| ba ca du lieu ~6–9s / "~6 giay" | DO_LAI / docstring kiem_ca_du_lieu | 4.9s | co (xap xi, phu thuoc may) |
| Registry 22->23, 938 | DO_LAI | 22/22 -> 23/23; 938/938 hai ben | co |
| numstat 1 0 | DO_LAI | 1 0 | co |
| actionlint rc=0 / dot bien rc=1 | DO_LAI | rc=0 / rc=1 | co |
| ruff tl.py 12, delta 0 | DO_LAI | 12 F821; blob tl.py khong doi | co |
| tl selftest N/N | nghiem thu 10 | 1715/1715 rc=0 | co |
| AL_VER 4 | DO_LAI | khong doi so master (buoc AL_VER khong nam trong diff) | co |
| 52 phut / G5 46,5 phut, run 36518707072 | docstring + DO_LAI | khong mang | KHONG DO DUOC |
| `skipped` cua job phu thuoc = dat | DO_LAI | — | CHUA TU DO; lop dong theo chi thi chu kho |

Khang dinh dinh luong bang do bo sot ma toi tim ra: dong `TU KIEM PHAN HANG` (co trong DO_LAI nhung khong co neo trong suite) — da tinh vao finding P3 lop bang-do.

## DAC TA (khong bat executor sua)
- Nghiem thu 11 co nguy co khong dat tren master hien tai: buoc `G5 kiem ban ke cong cu + T1..T8` o job `gate` KHONG bi bo o duong nhanh (Q6: khong mo rong JOB_G5), ma DO_LAI khai G5 chiem 46,5/52 phut. Neu dung, `gate (ubuntu-latest)` duong nhanh chi ngan ~5 phut cho toi khi #668 dua G5 ra job rieng. Dac ta (Q5) da dat #674 land SAU #668; chua_do_duoc 1. Khong tinh P.

## NGHIEM THU (tu chay)
1. DAT — t01 + dot bien ep day_du bi giet (trong 151/151).
2. DAT — t02 + `noi_allowlist_them_scripts` bi giet.
3. DAT — t05/t06 + `fail_open_*` bi giet.
4. DAT — t03 + `git_cho_push_*` bi giet.
5. DAT — t08 + `noi_allowlist_them_github` bi giet.
6. DAT — `yml_go_dieu_kien_pull_request_khoi_buoc_phan_loai` (y01), `yml_buoc_nang_luon_bo` (y03) bi giet.
7. DAT — y05 + hai dot bien paths bi giet.
8. DAT — actionlint rc=0 co shellcheck; `${{ }}` trong comment run rc=1.
9. DAT — 22/22 -> 23/23, 938/938 ca hai; numstat 1/0; `dk_go_muc_da_noi`, `yml_go_buoc_goi_test_khoi_ci` bi giet.
10. DAT — tl selftest 1715/1715; ruff delta 0 (Ruff 0.16.9, khong phai ban ghim 0.15.15).
11. CHUA_DO_DUOC — can PR that; khong thay loi khai da dat. Xem muc DAC TA ve G5.

## FINDINGS

### bang-do-thieu-neo-va-thieu-kiem-ke  [P3]  Dong tong ket `TU KIEM PHAN HANG:` khong co neo — in so/ket luan sai van FULL xanh
TEP/DONG: `ops/ci_duong_nhanh_test.py` — `main` (dong `print(f"TU KIEM PHAN HANG: …")`), `t93_main_ket_luan_va_ma_thoat_theo_duong_goi_that`.
VAN DE: Luot 6 dong cua `KIEM KE:` (t94 doi tap dong == [dong dung]). Nhung `main` in NAM dong tong ket; `TU KIEM PHAN HANG:`
mang hai so (mau rc, dot bien that) va mot ket luan DAT/DO ma khong ca nao doi chieu. DO_LAI.md dan chinh dong nay lam bang
chung. Doi `{len(MAU_RC)}` thanh `{len(MAU_RC) + 1}` => FULL rc=0, in `(6 mau rc, …)`, TONG DAT. Doi thanh luon in `DAT` =>
t91/t93/t94 deu rc=0 (khi tu kiem hong, TONG van DO nhung dong tu kiem noi DAT — hai dong mau thuan). Day la cua con lai cua lop:
luot 6 va theo MOT nhan chu khong theo TAP nhan tong ket.
CA LOP (moi dong tong ket): `CA:` (t93) · `DOT BIEN:` (t93) · `KIEM KE:` (t94) · `TU KIEM PHAN HANG:` (**thieu**) · `TONG:` (t93 dong cuoi). Chot chung: kich ban `sach` cua t93 doi TAP dong mang 5 nhan == danh sach dung; kich ban `tu kiem hong` doi dong tu kiem noi `DO`.
DA THU VA: co — trong `out/HINT.patch` (TEST-only):
```diff
--- ops/ci_duong_nhanh_test.py
+++ ops/ci_duong_nhanh_test.py
@@
         for mong_dong in (dong_ca, dong_db):
             ...
+        tk = "TU KIEM PHAN HANG: " + ("DO" if ten == "tu kiem hong" else "DAT") + \
+            f" ({len(MAU_RC)} mau rc, {len(TU_KIEM_DOT_BIEN)} dot bien that)"
+        bang([d for d in dong if d.startswith("TU KIEM PHAN HANG:")] == [tk], f"main/{ten}: dong tu kiem phai DUNG {tk!r}")
+        if ten == "sach":
+            nhan = ("CA:", "DOT BIEN:", "KIEM KE:", "TU KIEM PHAN HANG:", "TONG:")
+            bang([d for d in dong if d.startswith(nhan)] == [dong_ca, dong_db, "KIEM KE: gia", tk, "TONG: DAT"],
+                 f"main/{ten}: tap dong tong ket phai khop DUNG: {[d for d in dong if d.startswith(nhan)]}")
@@ DOT_BIEN
+    ("test_main_tu_kiem_in_so_sai", _test("({len(MAU_RC)}" + " mau rc, {len(TU_KIEM_DOT_BIEN)} dot bien that)\")", "({len(MAU_RC) + 1} mau rc, {len(TU_KIEM_DOT_BIEN)} dot bien that)\")"), ("t93_main_ket_luan_va_ma_thoat_theo_duong_goi_that",)),
+    ("test_main_tu_kiem_luon_in_dat", _test("{'DAT' if not loi_tu_kiem" + " else 'DO'} (", "{'DAT'} ("), ("t93_main_ket_luan_va_ma_thoat_theo_duong_goi_that",)),
```
Chot rieng tung cua: so sai -> `test_main_tu_kiem_in_so_sai`; ket luan sai -> `test_main_tu_kiem_luon_in_dat`; dong thu sau/doi thu tu -> so TAP day du o kich ban `sach` (bat ca them dong sai cung nhan).
DA THU NGHIEM: HEAD: out/b1.log (FULL rc=0 TONG DAT voi so sai), out/b2.log (t91/t93/t94 rc=0 voi luon-DAT). Ban ap hint (tmp/hint/cay): FULL rc=0, CA 64/64, DOT BIEN 158/158, TU KIEM DAT, TONG DAT (out/hint-full.log) — hai dot bien moi bi GIET dung ca dich t93.
DO TIN: cao.

### diff-check-tu-ha-nguong  [P3]  Bo mien `-space-before-tab` khoi D1 van FULL xanh — t20d khong co fixture cho loai thu ba
TEP/DONG: `ops/ci_duong_nhanh.py:68` (`CAU_HINH_WHITESPACE`), `ops/ci_duong_nhanh_test.py` `t20d_kiem_re_khoang_trang_cuoi_dong_khong_do`.
VAN DE: D1 (chu kho duyet) mien DUNG ba loai: blank-at-eol, blank-at-eof, space-before-tab. Fixture t20d chi co dau cach cuoi dong
(.md, .patch) va dong trong cuoi tep (.yaml) — khong tep nao co space-before-tab; phep kiem fixture `tho.returncode != 0` la TONG
nen khong cho biet loai nao con duoc do. Dot bien `core.whitespace=-blank-at-eol,-blank-at-eof` (bo loai thu ba) => t20d/t20a/t23 rc=0,
FULL 63/63 + 151/151 TONG DAT. Hau qua neu hoi quy: PR ho so co dong ` \t…` (verdict/patch chep nguyen byte) bi DO oan o duong nhanh
(fail-close, nhung trai quyet dinh D1 da duyet), khong cong nao bao. Chieu "tat rong hon" khong xay ra duoc qua core.whitespace (ba
loai la toan bo loai mac dinh-bat), da ghi o DOI CHIEU.
DA THU VA: co — `out/HINT.patch`: them `ops/reviews/tab.md` = `"a\n \tb\n"` vao fixture; voi MOI loai, chay `git -c core.whitespace=<chi bat loai ay> diff --check … -- <tep cua loai ay>` va doi rc != 0 (fixture co rang tung loai); ba dot bien moi `diff_check_bo_mien_space_before_tab|blank_at_eof|blank_at_eol` (neo `CAU_HINH_WHITESPACE = "…"`, khong trung docstring) cung dich t20d.
```diff
+          "ops/reviews/tab.md": "a\n \tb\n",
 ...
+        for tep, loai in (("ops/reviews/v-verdict.md", "blank-at-eol"), ("ops/leases/thua-dong.yaml", "blank-at-eof"),
+                          ("ops/reviews/tab.md", "space-before-tab")):
+            chi_loai = git(kho, "-c", "core.whitespace=-" + ",-".join(
+                x for x in ("blank-at-eol", "blank-at-eof", "space-before-tab") if x != loai),
+                "diff", "--check", f"{goc}...{dau}", "--", tep, kiem=False)
+            bang(chi_loai.returncode != 0, f"fixture vo hieu: {tep} phai do DUNG loai {loai} khi chi loai ay bat")
```
DA THU NGHIEM: HEAD out/d1-narrow.log, out/d1-narrow-full.log (song sot). HEAD dung: `--check` tho rc=2, `kiem_diff_check`=[] cho ` \t`.
Ban hint: 158/158 GIET, gom ca ba dot bien bo tung loai.
DO TIN: cao.

### kiem-re-bo-sot-duong-vao  [P3]  kiem_yaml: duoi `.yml` va tep da xoa dung truoc khong co chot (cung hai cua da chot cho lease)
TEP/DONG: `ops/ci_duong_nhanh.py` `kiem_yaml` (dong 165 bo loc duoi; dong 167-168 `continue`), `ops/ci_duong_nhanh_test.py` (chi t20b: mot tep `.yaml` hong).
VAN DE: Lop tong quat hoa tu `kiem-lease-bo-sot-duong-vao` (luot truoc dong cho lease bang t20g `.yml` va t21 `da-xoa`). Hai cua ay
o `kiem_yaml` khong co ca: (a) bo `.yml` khoi bo loc => FULL TONG DAT; (b) `continue` -> `break` sau tep da xoa (sap xep truoc tep
hong) => FULL TONG DAT. Ca hai la hoi quy FAIL-OPEN cua mot kiem re BU cho buoc bi bo (YAML ho so hong lot qua duong nhanh). HEAD dung
(do truc tiep). Anh huong hien tai thap: 0 tep `.yml` trong bon thu muc ho so; co 9 lan xoa tep ho so trong lich su.
Liet ke cua vao cua lop (kiem-re): YAML {duoi, xoa, thu tu, ma hoa} · diff-check {tung loai D1, xung dot} · lease {duoi, xoa, het/con han, han hong, rc} · ca du lieu {goi, ten, cwd, rc}. Da chot: lease, ca du lieu, xung dot. Thieu: YAML duoi + xoa (finding nay), tung loai D1 (finding tren). Ma hoa: tep khong UTF-8 => `except Exception` => loi (fail-close), khong can chot rieng.
DA THU VA: co — ca moi `t20h_kiem_re_yaml_duoi_yml_va_tep_xoa_dung_truoc` qua `kiem_re` that (kho git tam): `ops/land/hong.yml` hong phai DO; `ops/land/a.yaml` bi xoa + `ops/land/b.yaml` hong phai DO; hai dot bien `kiem_yaml_bo_duoi_yml`, `kiem_yaml_break_sau_tep_xoa` dich t20h.
```diff
+@ca
+def t20h_kiem_re_yaml_duoi_yml_va_tep_xoa_dung_truoc():
+    m = nap_module()
+    for ten, nen, pr in (
+        ("duoi yml", None, {"ops/land/hong.yml": "a: [1, 2\n"}),
+        ("xoa dung truoc", {"README.md": "x\n", "ops/land/a.yaml": "a: 1\n"},
+         {"ops/land/a.yaml": None, "ops/land/b.yaml": "a: [1, 2\n"}),
+    ):
+        with kho_that(nen=nen, nhanh_pr=pr) as (kho, goc, dau):
+            rc, log = kiem_re(m, kho, goc, dau)
+            bang(rc == 1 and "YAML khong parse duoc" in log, f"{ten}: YAML hong phai DO, duoc rc={rc}: {log}")
```
DA THU NGHIEM: HEAD out/k1.log, out/k2.log (FULL rc=0 TONG DAT); out/k3.log (doi chung lease: t21 do). Ban hint: t20h DAT tren HEAD, hai dot bien moi GIET (158/158).
DO TIN: cao ve lo chot; thap ve xac suat hoi quy thuc te.

## HINT.patch
`out/HINT.patch` — chi `ops/ci_duong_nhanh_test.py`, duong dan repo-relative khong tien to, dong dau mang nhan nguyen van
"chua chay tren cay that — executor tu ap, tu do, tu chiu trach nhiem commit". `patch -p0 --fuzz=0 --dry-run` rc=0 tren ban sao
`ops/`; ap that xong `cmp` giong het ban hint da chay. Ban hint: ruff F sach; FULL CA 64/64, DOT BIEN 158/158, TU KIEM DAT, TONG DAT,
rc=0; KIEM KE `hanh_vi=36 + 16 + 3 + 9 = 64 · 2 + 65 + 49 + 42 = 158`. Executor tu tai dan xuat, khong chep mu.

## DOT BIEN SONG SOT (tren HEAD, FULL)
- `CAU_HINH_WHITESPACE` bo `-space-before-tab` (out/d1-narrow-full.log)
- `kiem_yaml` `continue` -> `break` (out/k1.log)
- `kiem_yaml` bo duoi `.yml` (out/k2.log)
- `TU KIEM PHAN HANG` in `len(MAU_RC) + 1` (out/b1.log); in `DAT` bat ke loi (song qua t91/t93/t94, out/b2.log)

TONG: P0=0 P1=0 P2=0 P3=3
So lop: 7 (3 con mo, moi lop 1 P3; 4 dong trong pham vi local da do).
