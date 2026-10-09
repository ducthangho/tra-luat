verdict: changes_requested
reviewed_sha: 9f5cb77a87c528b90783c14292e2fcf498d886c6
Reviewed commit: 9f5cb77a87c528b90783c14292e2fcf498d886c6

luot: 12 (packet #674, dac ta r2 sha256 b6e719c9…da57 KHOP; PROMPT.md sha256 a95f9767…6e106c KHOP)
Reviewer: Claude Opus 5.5 subagent, CUNG HO executor => advisory_review (KHONG cross_approved). Model/effort duoc phuc vu: KHONG DO DUOC.
TONG: P0=0 P1=0 P2=0 P3=1 — 1 lop mo (kiem-mode-git-chot-khong-rang, duong vao MOI, test-only); luot chay TRON

## SO DO NEN (@9f5cb77, Linux)
- `python3 -B ops/ci_duong_nhanh_test.py`: `CA: 90/90 dat · 0 do · 0 hong` · `DOT BIEN: 249/249 bi giet dung ly do` · KIEM KE 62+16+3+9=90 · 2+68+137+42=249 · `TU KIEM PHAN HANG: DAT (5 mau rc, 3 dot bien that)` · `TONG: DAT` rc=0 (1m09s)
- `ci_dang_ky_test.py`: `PHẢN CHỨNG: 938/938 đỏ đúng` · `TỔNG: ĐẠT` · actionlint rc=0 · ruff F `All checks passed!`
- `git diff --stat 712ef9b 9f5cb77` = CHI `ops/ci_duong_nhanh_test.py` (+61) => san pham va ci.yml khong doi (khop loi khai).

## BANG SAN
HUONG 1: dot bien RIENG cua reviewer tren chot cua `kiem_mode_git`/`_doc_raw` CHUA co trong DOT_BIEN (ban sao tmp/m12/cay_<ten>, 90 ca `--mot-ca`)
  lenh   : python3 -B tmp/m12/mut.py $R (log tmp/m12/run1..3.log)
  output : nen: 0 ca do. SONG SOT: mt_goc_goc (merge-tree kiem mode `goc, dau` -> `goc, goc`) · mt_dau_dau · decode_strict
           (`decode("utf-8","surrogateescape")` -> `decode("utf-8")` trong _doc_raw) · regex_match_khong_full (`fullmatch` -> `match`) ·
           xoa_chi_theo_mode000 (`trang_thai == "D" and mode == "000000"` -> `mode == "000000"`) · mt_bo_no_messages · regex_bo_nhom_sha64 ·
           return_bo_loi_khi_lech · elif_thanh_if.
           GIET: split_khong_cat (15 ca) · ba_cham_thanh_hai_cham (t20u,t20zb) · cap_cay_doc_dau (t20u,t20za) · pl_mt_goc_goc (merge-tree CUA BO PHAN LOAI: t11e)
  ket luan: LOI (P3, lop `kiem-mode-git-chot-khong-rang` — loi khai commit "liet ke du doi so/moi chot" RONG HON phep do). Tuong duong / khong phai loi:
           mt_bo_no_messages (HUONG 2), regex_bo_nhom_sha64 (kho SHA-256, GitHub khong dung), return_bo_loi_khi_lech / elif_thanh_if (van DO, chi doi thong diep).

HUONG 2: hau qua that cua cac song sot (git 2.43.0 that)
  lenh   : python3 -B tmp/m12/mt_msg.py tmp/g1 · python3 -B tmp/m12/nonutf8.py (san pham that) · python3 -B tmp/m12/dec.py $R (ban dot bien decode_strict)
  output : merge-tree sach co/khong `--no-messages` => CUNG `15ef4e86…\n` (mt_bo_no_messages TUONG DUONG; xung dot thi rc=1 => DO ca hai).
           PR them `ops/specs/t\xff.md` (ten khong UTF-8): san pham that `DUONG_NHANH ... dung duong nhanh` · `kiem-re DAT (1 tep doi, 0 loi)` rc=0;
           ban decode_strict: `UnicodeDecodeError ... _doc_raw line 293` (traceback) => kiem-re DO oan o required check `gate-ops` — 90 ca khong ca nao bat.
           mt_goc_goc: cap "goc -> cay merge-tree" thanh diff goc->goc RONG => cap ay VANG MAT ma van DAT (tap `thay` van du nho hai cap kia);
           fake `chay_gia` tra CAY_GIA bat ke doi so, t20u chi ghim `--attr-source`, t20za ghim doi so cua `--raw` chu khong ghim merge-tree.
  ket luan: LOI (P3, cung lop). Tat ca deu fail-close hoac vang-mat-cua-cap-du-thua (cap hop phu trong van hanh thuong) => KHONG co fail-open do duoc; hang P3.

HUONG 3: ap HINT luot 12 len ban sao (tmp/hint12, copytree cay-kho @9f5cb77) roi chay suite day du
  lenh   : python3 -B tmp/m12/mkhint.py $R ; (cd tmp/hint12 && python3 -B ops/ci_duong_nhanh_test.py) ; python3 -B tmp/m12/mkpatch.py $R
  output : lan 1: `DOT BIEN: 253/254` — `mode_git_raw_giai_ma_chat: TIN_DUNG_GIA ... UnicodeDecodeError` (bo phan hang cua executor BAT DUNG tin dung gia
           cua chinh hint cua toi — chot `TinHieuChotCa` co rang). Sua hint: chi `except UnicodeError` -> TinHieuChotCa (loi khac van HONG).
           lan 2: `CA: 91/91 dat` · `DOT BIEN: 254/254 bi giet dung ly do` · `TU KIEM PHAN HANG: DAT` · `TONG: DAT` rc=0; ruff F `All checks passed!`;
           `patch -p0 --fuzz=0 -i out/HINT.patch` tren ban sao sach rc=0, byte KHOP ban da do.
  ket luan: hint co rang, moi duong vao mot chot rieng (5 dot bien -> 3 ca dich / kich ban rieng).

HUONG 4: pham vi + so (do_lai_so, blob master-side, kiem ke)
  output : blob `ops/lease_publish_test.py` 694cca5b… va `ops/specs/t131-deadline-dem-spawn.md` 1a99adbf… HEAD == 89fc4fa; 1741e0a, 89fc4fa la to tien HEAD
           => phan them la CUA MASTER. `git diff --stat 89fc4fa HEAD` = dung 4 tep packet. do_lai_so: 113 lease, dat 107 truot 6 (khop luot 11).
           Loi khai commit "18 dot bien moi": dem 18 (+3 cua hint luot 11) = 249-228 = 21 KHOP; "CA 90/90" = 88 + t20zc + t20zd KHOP.
  ket luan: KHONG PHAI LOI

HUONG 5: t20zd tren Windows / nen khong symlink
  output : buoc `ci-duong-nhanh selftest` co `if: runner.os == 'Linux'` (ci.yml:558-560) => `symlink_to` khong tha im lang la dung, giong t20n/t20q/t20x.
  ket luan: KHONG PHAI LOI (Windows that: KHONG DO DUOC — khong co runner)

HUONG 6: nghiem thu 6-9 (ci.yml, dang ky)
  output : ci.yml khong doi so 712ef9b (`git diff --stat 712ef9b HEAD` chi tep test); actionlint rc=0; ci_dang_ky_test 938/938 TỔNG ĐẠT.
           Dot bien YAML/NT8/NT9 da do o luot 11 tren CUNG blob ci.yml — khong chay lai.
  ket luan: KHONG PHAI LOI

## DOI CHIEU LUOT TRUOC (luot 11, reviewed 712ef9b -> nay 9f5cb77)
| lop | hang luot 11 | trang thai | bang chung TU DO |
|---|---|---|---|
| `kiem-mode-git-chot-khong-rang` (a) `--no-renames` | P3 | DA VA THAT | t20zc co mat; `mode_git_raw_bo_no_renames` GIET dung ly do (suite 249/249) |
| (b) chieu "thieu" cua chot tap | P3 | DA VA THAT | kich ban "tap thieu"; `mode_git_tap_chi_bat_thua` + `mode_git_tap_chi_bat_thieu` giet |
| (c) nhanh `trang_thai == "D" or` | P3 | DA VA THAT | "D mode tep thuong"; `mode_git_xoa_chi_theo_mode` giet |
| ca lop (loi khai "liet ke du doi so/moi chot") | — | VA HO (HEP) | HUONG 1-2: con 4 duong vao khong rang, 2 co hau qua do duoc (mt_goc_goc vang-mat cap; decode_strict DO oan) |
| `kiem-re-cua-fail-close-chua-co-ca`, `kiem-re-bi-cau-hinh-boi-du-lieu-ho-so`, `phan-loai-khong-neo-merge-ref-that`, `cau-khai-skipped-nguoc-phep-do`, `dependency-failure-skips-required-checks` | DONG | van DONG | san pham + ci.yml khong doi; suite 249/249 |

## BANG LOP
| slug | bieu hien | hang cao nhat con mo | phuong an va chung | phep kiem dong lop |
|---|---|---|---|---|
| `kiem-mode-git-chot-khong-rang` | chot/doi so cua `kiem_mode_git`/`_doc_raw` go ra ma khong ca nao DO. Duong vao CON MO (tu liet ke het doi so merge-tree + moi phep giai ma/khop): (d) commit cua merge-tree kiem mode `goc, dau` (-> `goc, goc` lam cap cay RONG; -> `dau, dau`); (e) `fullmatch` cua MAU_BAN_GHI_RAW; (f) ve `trang_thai == "D"` cua nhanh bo qua xoa; (g) `surrogateescape` cua `_doc_raw`. Da xet TUONG DUONG: `--no-messages`, nhom SHA-256, `return loi +`, `elif`->`if`. | P3 | ghim doi so merge-tree; 2 kich ban t20zb; ca git that t20ze | `out/HINT.patch` (5 dot bien) — do: `CA 91/91` · `DOT BIEN 254/254` · `TONG: DAT` |
| 5 lop cu | — | DONG | — | nhu luot 11 |

## BANG DO (khang dinh -> dao khai -> do duoc -> khop?)
| khang dinh | nguon | do duoc | khop? |
|---|---|---|---|
| "liet ke du doi so git ... va moi chot" | commit 9f5cb77 | 4 duong vao con song (HUONG 1) | **khong** -> finding |
| "18 dot bien moi", CA 90/90, DOT BIEN 249/249 | commit | 18 / 90 / 249 | co |
| "San pham va ci.yml khong doi" | commit | diff 712ef9b..HEAD chi tep test | co |
| "merge-tree chay HAI lan" (t20u SO_LOI_GOI) | test | dem 2 dung, doi so COMMIT khong ghim (mt_goc_goc song) | **mot nua** -> finding (d) |
| "Git loi/nem, dau ra ... ban ghi la => KHONG DO DUOC" | docstring kiem_mode_git | ten khong UTF-8 + giai ma chat => traceback, khong co ca | **khong co ca** -> finding (g) |
| 113 lease / 107 / 6 | do_lai_so | 113/107/6 | co |
| G5 phut, "4 luot that" | DO_LAI | KHONG DO DUOC (khong mang) | — |

## NGHIEM THU (r2)
| # | ket qua | bang chung |
|---|---|---|
| 1-5 | dat (kem P3 tren) | suite 90/90 · 249/249 · TONG DAT |
| 6, 7 | dat | y01..y16 trong suite; ci.yml khong doi |
| 8, 9 | dat | actionlint rc=0; ci_dang_ky 938/938; luot 11 da dot bien tren cung blob ci.yml |
| 10 | KHONG CHAY LAI luot nay (scripts/ khong doi; luot 11 do 1715/1715) | `git diff --stat 89fc4fa HEAD` khong co scripts/ |
| 11 | chua_do_duoc | can PR that; executor KHONG khai dat |

## FINDINGS

### kiem-mode-git-chot-khong-rang  [P3]  con 4 duong vao khong rang cua `kiem_mode_git`/`_doc_raw` (loi khai "liet ke du" rong hon phep do)
TEP/DONG: `ops/ci_duong_nhanh.py` `kiem_mode_git` (merge-tree `... "--no-messages", goc, dau]`; `if trang_thai == "D" and mode == "000000":`),
  `_doc_raw` (`MAU_BAN_GHI_RAW.fullmatch`, `decode("utf-8", "surrogateescape")` dong 293); `ops/ci_duong_nhanh_test.py` LOI_GOI_DOC_THUOC_TINH["merge-tree"] (dong 967), t20zb.
VAN DE: (d) doi so commit cua merge-tree kiem mode khong bi ghim: `goc, goc` lam cap "goc -> cay merge-tree" RONG — cap ay VANG MAT ma kiem-re
  van DAT (ho "cong vang mat trong nhu xanh"; hau qua han che vi cap `goc -> merge ref` thuong trung cay); `dau, dau` cung song. (e) `fullmatch` -> `match`
  song. (f) ve `trang_thai == "D"` cua nhanh bo qua xoa song (mode 000000 voi A/M bi bo qua im lang) — ban doi xung cua (c) luot 11. (g) giai ma chat
  trong `_doc_raw` song; tren git that PR them ten tep KHONG UTF-8 duoi allowlist (bo phan loai nhan, san pham that DAT) thi ban dot bien nem
  UnicodeDecodeError => DO oan o required check. Moi duong deu fail-close hoac vang-mat-cua-cap-du-thua => P3.
DA THU VA: co — TEST-ONLY `out/HINT.patch` (dong 1 mang nhan bat buoc). Chot rieng tung duong vao:
```diff
-    "merge-tree": lambda a: a[1:3] == ["merge-tree", "--write-tree"],
+    "merge-tree": lambda a: a[1:3] == ["merge-tree", "--write-tree"] and a[-2:] == [GOC_A, GOC_B],      # (d) -> t20u
+        ("raw dau ghi duoi thua", dict(raw={"ba_cham": (0, raw_ghi(("100644", "Mx", d)))}), "ban ghi la"),   # (e) -> t20zb
+        ("A mode 000000", dict(raw={"ba_cham": (0, raw_ghi(("000000", "A", d)))}), "mode 000000, A"),         # (f) -> t20zb
+@ca
+def t20ze_kiem_re_ten_tep_khong_utf8_dat():   # (g) kho_that, ten os.fsdecode(b"ops/specs/t\xff.md"); chot fixture byte \xff trong --raw;
+    ...   except UnicodeError -> TinHieuChotCa (CHI loi giai ma; loi khac van HONG); bang(rc == 0)
+    dot bien: mode_git_merge_tree_goc_goc, mode_git_merge_tree_dau_dau -> t20u · mode_git_raw_match_khong_full, mode_git_xoa_bo_ve_D -> t20zb ·
+              mode_git_raw_giai_ma_chat -> t20ze
```
  Tuy chon san pham (KHONG bat buoc, khong co HINT-sanpham): bat `UnicodeError` quanh phep giai ma trong `_doc_raw` => "KHONG DO DUOC" thay traceback.
DA THU NGHIEM: HUONG 1 (song sot), HUONG 2 (hau qua that cua d, g), HUONG 3 (hint tren ban sao: `CA: 91/91` · `DOT BIEN: 254/254 bi giet dung ly do` ·
  `TU KIEM PHAN HANG: DAT` · `TONG: DAT`; ban dau thieu `except UnicodeError` thi bo phan hang bao dung TIN_DUNG_GIA — chot van co rang).
DO TIN: cao

## GHI CHU QUY TRINH
- Moi ghi chi trong $R (tmp/m12, tmp/hint12, tmp/g1, out/). Khong commit/push/checkout trong kho that hay wt-674; `cay-kho` khong bi sua
  (git status sach). Commit trong tmp/g1 va cac kho_that tam la kho scratch. Khong mang, khong GitHub. Khong con job nen.

TONG: P0=0 P1=0 P2=0 P3=1 — so lop: 6 (1 mo: `kiem-mode-git-chot-khong-rang`; 5 dong)
