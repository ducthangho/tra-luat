verdict: changes_requested
reviewed_sha: 5ec951c007c48fb88efb6b261973be54e293c4a4
Reviewed commit: 5ec951c007c48fb88efb6b261973be54e293c4a4

luot: 14 (packet #674, dac ta r2 sha256 b6e719c9…da57 KHOP; PROMPT.md sha256 7365fdc2…f17f KHOP)
Reviewer: Claude Opus 5.5 subagent, CUNG HO executor => advisory_review (KHONG phai cross_approved). Model/effort thuc chay: KHONG DO DUOC.
TRANG THAI LUOT: BI CAT THEO HOP THOI GIAN (bat dau 10:10:48Z, dong ho tuong 11:19Z khi viet ban nay — vuot hop 20 phut).
=> theo PROMPT, luot bi cat KHONG phai approve. HUONG 6 DA DO (11:20-11:21Z): dot bien X1 SONG 93/93, doi chung CTRL bi giet 5 ca
=> 1 finding P3 (lop `kiem-mode-git-chot-khong-rang`, LAN THU 4) => verdict `changes_requested`. Hint CHUA DO (lenh dung hint bi he thong quyen tu choi, va het hop).

## SO DO NEN (@5ec951c, Linux, TMPDIR=$R/tmp)
- `python3 -B ops/ci_duong_nhanh_test.py`: `CA: 93/93 dat · 0 do · 0 hong` · `DOT BIEN: 269/269 bi giet dung ly do` ·
  `KIEM KE: 65+16+3+9 = 93 · 2+68+157+42 = 269` · `TU KIEM PHAN HANG: DAT (5 mau rc, 3 dot bien that)` · `TONG: DAT` · rc=0 (real 2m22s)
- `python3 -B .claude/dev/ci_dang_ky_test.py`: `PHẢN CHỨNG: 938/938 đỏ đúng` · `TỔNG: ĐẠT` · rc=0
- `actionlint .github/workflows/ci.yml` rc=0 (shellcheck /usr/bin/shellcheck co mat) · ruff F (2 tep moi) `All checks passed!` rc=0
- `goi/do_lai_so.py`: `[1] ... 345; toan allowlist: 63; ... --check NGUYEN BAN do: 8` · `[2] ... 113 tep; dat 107, truot 6`

## DOI CHIEU LUOT TRUOC (luot 13, reviewed 8e204f3 -> nay 5ec951c)
| lop / duong vao | hang luot 13 | trang thai | bang chung TU DO |
|---|---|---|---|
| `kiem-mode-git-chot-khong-rang` (h) nhanh CHAP NHAN `T` + mode 100644 | P3 | DA VA THAT | t20zf co trong cay (chot fixture `^:120000 100644 ... T\tops/specs/x\.md$`); dot bien `mode_git_doi_kieu_thanh_tep_la_loi` + `mode_git_o_T_644_la_loi` -> t20zf nam trong `DOT BIEN: 269/269 bi giet dung ly do` |
| mo rong: moi o CHAP NHAN (trang thai x mode moi) | — | DA VA (theo bang quyet dinh cua san pham) | tu liet ke: san pham chi quyet theo (trang_thai, mode MOI) => 7 o chap nhan: A644->t20a, A755->t20zg, M644->t20zg, M755->t20y, T644->t20zf, T755->t20zg, D000000->t20y (`mode_git_xoa_la_loi`). Moi o co dot bien rieng trong DOT_BIEN (doc diff + 269/269). t20zg ghim fixture ca ba o bang regex tren `git diff --raw` that. |
| 5 lop cu (`kiem-re-cua-fail-close-chua-co-ca`, `kiem-re-bi-cau-hinh-boi-du-lieu-ho-so`, `phan-loai-khong-neo-merge-ref-that`, `cau-khai-skipped-nguoc-phep-do`, `dependency-failure-skips-required-checks`) | DONG | van DONG | `git diff --stat 712ef9b 5ec951c -- ops/ci_duong_nhanh.py .github/workflows/ci.yml` = RONG (san pham + ci.yml khong doi); suite 269/269 |

## BANG LOP
| slug | bieu hien | hang cao nhat con mo | phuong an va chung | phep kiem dong lop |
|---|---|---|---|---|
| `kiem-mode-git-chot-khong-rang` | phia CHAP NHAN: DONG (7/7 o co dot bien rieng, giet trong 269/269). Phia TU CHOI theo TRANG THAI: o `M` x {120000,160000} (doi dich symlink / nang con tro gitlink DA CO tren nen) khong ca nao ghim; dot bien X1 mien tru `M` song 93/93 (HUONG 6). Da xet co rang: A x 160000 (t20v), A x 120000 tren core.symlinks=false (t20x), T x 160000 (t20w), cap rieng (t20za), D x khac 0 / A x 000000 (t20zb). | P3 (LAN THU 4 cua lop) | DONG LOP THEO CAU TRUC: mot ca don vi duyet TOAN BO bang quyet dinh {A,M,T,D} x {000000,100644,100755,120000,160000} qua `chay_gia(raw=...)` (nhu t20za/t20zb), moi o mot ky vong CHAP NHAN/TU CHOI — het phai liet ke tung o bang git that; kem ca git that `M 120000` tren core.symlinks=false cho hau qua | dot bien X1 + `mode_git_mien_tru_M_120000` + `mode_git_mien_tru_M_160000` phai DO dung ca moi; KHONG DO DUOC luot nay |
| 5 lop cu | — | DONG | — | nhu luot 13 |

## BANG SAN
HUONG 1: so nen cua bo test / loi khai commit
  gia thuyet : neu "CA 93/93, DOT BIEN 269/269, TU KIEM DAT, TONG DAT" la loi khai rong hon phep do thi so in ra se khac
  lenh       : cd cay-kho && python3 -B ops/ci_duong_nhanh_test.py
  output     : CA: 93/93 dat · 0 do · 0 hong / DOT BIEN: 269/269 bi giet dung ly do / KIEM KE ... = 93 · ... = 269 / TU KIEM PHAN HANG: DAT (5 mau rc, 3 dot bien that) / TONG: DAT / rc=0
  ket luan   : KHONG PHAI LOI (93 = 91 + t20zf + t20zg; 269 = 262 + 1 (hint 13) + 6 (mode_git_o_*); san pham 150->157 dot bien = +7 KHOP)

HUONG 2: pham vi diff + phan them cua master
  gia thuyet : neu ban va luot 14 dong vao san pham/ci.yml hoac tep master bi packet sua thi blob se lech
  lenh       : git diff --stat 8e204f3 5ec951c; git diff --stat 712ef9b 5ec951c -- ops/ci_duong_nhanh.py .github/workflows/ci.yml; git rev-parse 5ec951c:<f> vs 89fc4fa:<f>; merge-base --is-ancestor; git diff --name-only 89fc4fa 5ec951c; numstat ci_dang_ky_test
  output     : 8e204f3..5ec951c = CHI ops/ci_duong_nhanh_test.py (+70); 712ef9b..5ec951c san pham+ci.yml RONG; lease_publish_test.py 694cca5b8ddb == 694cca5b8ddb; t131 spec 1a99adbfe4e5 == 1a99adbfe4e5; 89fc4fa, 1741e0a la to tien; diff 89fc4fa..HEAD = dung 4 tep packet; ci_dang_ky_test `1 0`
  ket luan   : KHONG PHAI LOI

HUONG 3: cong phu (ci_dang_ky, actionlint, ruff)
  gia thuyet : neu dong DA_NOI hoac ci.yml lam vo cong dang ky / lint thi rc != 0
  lenh       : python3 -B .claude/dev/ci_dang_ky_test.py; actionlint .github/workflows/ci.yml; python3 -m ruff check --no-cache --select F ops/ci_duong_nhanh.py ops/ci_duong_nhanh_test.py
  output     : PHẢN CHỨNG: 938/938 đỏ đúng · TỔNG: ĐẠT rc=0; actionlint rc=0 (co shellcheck); ruff All checks passed! rc=0
  ket luan   : KHONG PHAI LOI (dong `DANG KY: 23/23` khong nam trong phan tail toi doc; TỔNG ĐẠT)

HUONG 4: so dinh luong trong DO_LAI
  gia thuyet : neu 345/63/8 hoac 113/107/6 da troi thi do_lai_so ra so khac
  lenh       : cd cay-kho && python3 -B ../goi/do_lai_so.py | grep -v CẢNH
  output     : [1] ... 345; toan allowlist: 63; ... NGUYEN BAN do: 8 · [2] 113 tep; dat 107, truot 6
  ket luan   : KHONG PHAI LOI; G5 46,5/52 phut va "4 luot that": KHONG DO DUOC (khong mang)

HUONG 5: rang cua 6 dot bien mode_git_o_* + t20zf/t20zg (doc + so do)
  gia thuyet : neu mot o chap nhan chi duoc "ghim" boi fixture khong sinh ra o do thi dot bien cua o ay song
  lenh       : git diff 8e204f3 5ec951c (doc) + HUONG 1 (269/269 dung ly do, phan hang TinHieuChotCa neo ten ca)
  output     : t20zg ghim ca ba dong raw bang regex (A 100755, M 100644, T 120000->100755) truoc khi `bang(rc == 0)`; t20zf ghim `:120000 100644 ... T`; t20y ghim ls-tree 100755 (khong ghim trang thai M — nen 100644 tu kho_that nen o M 755 van sinh ra); t20a khong ghim raw (tep moi tu Python tren Linux = 100644)
  ket luan   : KHONG PHAI LOI (ghi chu: t20a/t20y ghim fixture yeu hon t20zf/t20zg, nhung dot bien cua ho da giet dung ly do tren nen do)

HUONG 6: phia TU CHOI theo trang thai — o `M` x {120000, 160000} (ra soat doc lap cua vao con lai)
  gia thuyet : neu dot bien X1 `if trang_thai == "D" or (mode not in MODE_THUONG and trang_thai != "M"):` (mien TRU trang thai M khoi chot mode — FAIL-OPEN cho doi dich symlink / nang gitlink) song qua 93 ca thi phia tu choi co o khong rang
  lenh       : grep -n 'raw_ghi((.*"M"\|120000\|160000' ops/ci_duong_nhanh_test.py ;
               tmp/m14/mut.sh X1 <dong 338> <X1>  (ban sao cp -a -> tmp/m14/X1; runner tmp/m14/run_cases.py chay MOI ca qua chay_ca_trong_tien_trinh)
               tmp/m14/mut.sh CTRL <dong 338> `... and trang_thai not in ("M", "A", "T")`  (doi chung: rig phai DO duoc)
  output     : grep: moi fixture 120000/160000 la A (t20v, t20x, t20za), T (t20w, t20za, t20zf, t20zg) hoac D (t20zb); KHONG co o M x {120000,160000}.
               X1: dong 338 da doi (grep xac nhan) -> `CA chay=93 khong_dat=0` (16,9s)  => SONG SOT
               CTRL: `CA chay=93 khong_dat=5` (t20v, t20w, t20x, t20za, t20zb) — rig co rang. Dang chu y: duoi CTRL, t20x (symlink tren
               `core.symlinks=false`, dia la tep thuong) ra `rc=0: ... kiem-re DAT (2 tep doi, 0 loi)` => khi chot mode mien tru trang thai
               cua mot symlink thi KHONG con chot nao khac bat duoc tren nen do.
  ket luan   : LOI (P3) — finding `kiem-mode-git-chot-khong-rang` ben duoi.

## BANG DO (khang dinh -> dao khai -> do duoc -> khop?)
| khang dinh | nguon | do duoc | khop? |
|---|---|---|---|
| CA 93/93, DOT BIEN 269/269, TU KIEM DAT, TONG DAT, rc=0 | commit 5ec951c | 93 / 269 / DAT / DAT / 0 | co |
| "6 dot bien mode_git_o_* moi" + hint 13 | commit | diff: 1 + 6 dong moi trong DOT_BIEN; san pham 150->157 | co |
| "t20zg dung ba o con thieu tren git that (A 755, M 644, T 755) co chot fixture" | commit | 3 regex tren `git diff --raw --no-renames goc...dau` truoc `bang(rc==0)` | co |
| "San pham va ci.yml khong doi" | commit | diff 712ef9b..5ec951c rong | co |
| ci_dang_ky_test 23/23 + 938/938 | commit | 938/938 TỔNG ĐẠT (23/23 khong doc duoc trong tail) | mot phan (TỔNG ĐẠT) |
| ruff F sach | commit | All checks passed! | co |
| doctrine-scan rc=0 | commit | KHONG DO DUOC luot nay (hop thoi gian) | — |
| 345 / 63 / 8; 113 / 107 / 6 | DO_LAI | do_lai_so | co |
| G5 46,5/52 phut; "4 luot that" | DO_LAI | KHONG DO DUOC (khong mang) | — |

## NGHIEM THU (r2)
| # | ket qua | bang chung |
|---|---|---|
| 1-5 | dat theo bo test (93/93 · 269/269 · TONG DAT) | HUONG 1 |
| 6, 7 | dat theo y01..y16 trong suite; ci.yml khong doi tu 712ef9b | HUONG 1-2 |
| 8, 9 | dat | actionlint rc=0; ci_dang_ky 938/938 TỔNG ĐẠT |
| 10 | KHONG CHAY LAI luot nay (scripts/ khong nam trong diff 89fc4fa..HEAD) | — |
| 11 | chua_do_duoc | can PR that; commit KHONG khai dat |

## FINDINGS

### kiem-mode-git-chot-khong-rang  [P3]  (LAN THU 4 cua lop — §12) phia TU CHOI cua `kiem_mode_git` khong ghim o trang thai `M` x {120000, 160000}
TEP/DONG: `ops/ci_duong_nhanh.py` `kiem_mode_git` dong 338 `if trang_thai == "D" or mode not in MODE_THUONG:`; `ops/ci_duong_nhanh_test.py` (khong ca nao co `M` voi mode 120000/160000).
VAN DE: luot 14 da liet ke het o CHAP NHAN (7/7 co dot bien, dung), nhung chua liet ke phia TU CHOI theo trang thai. San pham hom nay DUNG (tu choi
  moi mode ngoai 100644/100755 bat ke trang thai). Nhung dot bien X1 mien tru trang thai `M` khoi chot mode (tuc CHAP NHAN doi dich symlink da co
  tren nen, va nang con tro gitlink da co tren nen) song qua CA 93 ca. Huong cua dot bien song la FAIL-OPEN: doi chung CTRL cho thay tren nen
  `core.symlinks=false` (dia la tep thuong — mac dinh Git for Windows, dung kich ban t20x) khi chot mode mien tru trang thai cua symlink thi
  `kiem-re DAT`, khong chot doc dia nao bat lai. Voi gitlink, chot dia cap merge ref (`not is_file()`) van bat, nen chi symlink la duong hoan toan mo.
  Hang P3 vi day la lo RANG cua test (san pham dung), cung chuan luot 12-13; huong fail-open nang hon luot 13 (fail-close) — chu kho can nhac.
  Lan thu 4 lop nay co finding (luot 11, 12, 13, 14): moi luot lap mot o ma nguoi viet nghi toi. Theo §12 ("dem hinh dang loi"): nen dong lop
  bang MOT ca duyet toan bo bang quyet dinh thay vi them ca git that cho tung o.
DA THU VA: co — TEST-ONLY, khoi diff duoi (CHUA CHAY: lenh dung ban sao de do hint bi he thong quyen tu choi va het hop thoi gian; KHONG ghi
  `out/HINT.patch` vi khong kiem duoc `patch -p0 --fuzz=0` — "chua chay tren cay that — executor tu ap, tu do, tu chiu trach nhiem commit").
```diff
--- ops/ci_duong_nhanh_test.py
+++ ops/ci_duong_nhanh_test.py
+@ca
+def t20zh_kiem_mode_git_bang_quyet_dinh_day_du():
+    """Cross-review luot 14 (`kiem-mode-git-chot-khong-rang`, dong lop THEO CAU TRUC): ghim TOAN BO bang quyet dinh
+    (trang thai x mode moi) o muc don vi. San pham chi quyet theo (trang thai, mode moi) nen bang nay la day du."""
+    m = nap_module()
+    duong = "ops/land/g"
+    CHAP_NHAN = {("A", "100644"), ("A", "100755"), ("M", "100644"), ("M", "100755"),
+                 ("T", "100644"), ("T", "100755"), ("D", "000000")}
+    with _cay_tam({duong: "g\n"}) as kho:   # dia CO tep thuong: chot dia cap merge ref khong xen vao phep do
+        for tt in "AMTD":
+            for mode in ("000000", "100644", "100755", "120000", "160000"):
+                ghi = raw_ghi((mode, tt, duong))
+                loi = m.kiem_mode_git(env_pr(), chay_gia(raw={k: (0, ghi) for k in ("ba_cham", "cay", "hop")}), kho, {duong})
+                if (tt, mode) in CHAP_NHAN:
+                    bang(loi == [], f"o ({tt}, {mode}) phai CHAP NHAN: {loi}")
+                else:
+                    bang(len(loi) == 3 and all(f"mode {mode}, {tt}" in x for x in loi),
+                         f"o ({tt}, {mode}) phai TU CHOI o ca ba cap: {loi}")
@@ DOT_BIEN (sau mode_git_o_T_755_la_loi)
+    # ---- cross-review luot 14: phia TU CHOI theo trang thai (moi o mot dot bien rieng)
+    ('mode_git_mien_tru_M', _ma('            if trang_thai == "D" or mode not in MODE_THUONG:', '            if trang_thai == "D" or (mode not in MODE_THUONG and trang_thai != "M"):'), ('t20zh_kiem_mode_git_bang_quyet_dinh_day_du',)),
+    ('mode_git_mien_tru_M_120000', _ma('            if trang_thai == "D" or mode not in MODE_THUONG:', '            if trang_thai == "D" or (mode not in MODE_THUONG and (trang_thai, mode) != ("M", "120000")):'), ('t20zh_kiem_mode_git_bang_quyet_dinh_day_du',)),
+    ('mode_git_mien_tru_M_160000', _ma('            if trang_thai == "D" or mode not in MODE_THUONG:', '            if trang_thai == "D" or (mode not in MODE_THUONG and (trang_thai, mode) != ("M", "160000")):'), ('t20zh_kiem_mode_git_bang_quyet_dinh_day_du',)),
```
  Kem (khuyen nghi, cung tep test): mot ca GIT THAT `M 120000 -> 120000` (nen co `ops/land/l.md -> a.md`, PR doi dich sang `b.md`), sau commit
  checkout lai duong ay bang `git -c core.symlinks=false checkout -- ops/land/l.md` nhu t20x; chot fixture `^:120000 120000 <sha> <sha> M\tops/land/l\.md$`
  + chot `kiem_loai_tep(...) == []`; ky vong `rc == 1 and "mode 120000, M" in log`. Tuong tu cho gitlink bang `_commit_gitlink` hai lan (M 160000).
  Can kiem truoc khi ap: `raw_ghi` co nhan mode 000000 voi trang thai A/M/T khong (t20zb dung "A mode 000000" nen co ve co), va so dong loi
  moi o tu choi la 3 (ba cap) hay khac — chinh ky vong `len(loi) == 3` theo so do that.
DA THU NGHIEM: X1 `CA chay=93 khong_dat=0` (song); CTRL `CA chay=93 khong_dat=5` (rig co rang; t20x duoi CTRL `kiem-re DAT` = hau qua fail-open).
  Hint: KHONG DO DUOC (lenh dung ban sao bi tu choi quyen + het hop thoi gian).
DO TIN: cao cho viec dot bien song va co che hau qua (doi chung CTRL do duoc); vua cho hang P3 (P2 neu chu kho coi dot bien fail-open song la
  cong co the bi lua); hint: thap-vua (chua chay).

## GHI CHU QUY TRINH
- Moi ghi chi trong $R (tmp/, tmp/m14/, out/). Khong commit/push/checkout trong kho that; `cay-kho` khong bi sua. Khong mang, khong GitHub.
- HINT.patch: KHONG ghi — hint chua kiem duoc (`patch -p0 --fuzz=0` + do rang) vi lenh dung ban sao bi he thong quyen tu choi va het hop; khoi diff nam trong finding.
- Ban sao do: tmp/m14/X1 (dot bien X1), tmp/m14/CTRL (doi chung), runner tmp/m14/run_cases.py + tmp/m14/mut.sh. Khong con job nen.
- doctrine-scan: KHONG DO DUOC luot nay.

TONG: P0=0 P1=0 P2=0 P3=1 — so lop: 6 (1 mo: `kiem-mode-git-chot-khong-rang`, LAN THU 4, phia TU CHOI theo trang thai `M`; 5 lop cu DONG). Luot vuot hop thoi gian => khong phai approve.
