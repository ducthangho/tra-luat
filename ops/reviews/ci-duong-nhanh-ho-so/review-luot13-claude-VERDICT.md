verdict: changes_requested
reviewed_sha: 8e204f38b0f5435066ade75a01e8876e1acf5afb
Reviewed commit: 8e204f38b0f5435066ade75a01e8876e1acf5afb

luot: 13 (packet #674, dac ta r2 sha256 b6e719c9…da57 KHOP; PROMPT.md sha256 a28e60f1…9d9e KHOP) — luot chay TRON
TONG: P0=0 P1=0 P2=0 P3=1 — 1 lop mo (`kiem-mode-git-chot-khong-rang`, LAN THU 3 cua lop, duong vao MOI, test-only)
Reviewer: Claude Opus 5.5 subagent, CUNG HO executor => advisory_review. Model/effort duoc phuc vu: KHONG DO DUOC.

## SO DO NEN (@8e204f3, Linux, TMPDIR=$R/tmp)
- `python3 -B ops/ci_duong_nhanh_test.py`: `CA: 91/91 dat · 0 do · 0 hong` · `DOT BIEN: 262/262 bi giet dung ly do` · KIEM KE 63+16+3+9=91 · 2+68+150+42=262 · `TU KIEM PHAN HANG: DAT (5 mau rc, 3 dot bien that)` · `TONG: DAT` rc=0 (1m11s)
- `ci_dang_ky_test.py`: `PHẢN CHỨNG: 938/938 đỏ đúng` · `TỔNG: ĐẠT` rc=0 · actionlint ci.yml rc=0 · ruff F (2 tep moi) `All checks passed!`
- `git diff --stat 9f5cb77 HEAD` = CHI `ops/ci_duong_nhanh_test.py` (+37 -1) => san pham va ci.yml khong doi (khop loi khai).

## BANG SAN
HUONG 1: dot bien RIENG cua reviewer tren kiem_mode_git/_doc_raw CHUA co trong DOT_BIEN (ban sao dung_cay_tam, 91 ca --mot-ca)
  lenh   : python3 -B tmp/m13/mut.py $R
  output : GIET: raw_bo_T (t20w,t20za) · disk_chi_ba_cham (t20u,t20zb) · disk_chi_cay (t20zb) · raw_trang_thai_hang_M (5 ca) · raw_cwd_root (12) · mt_cwd_root (12).
           SONG SOT: return_bo_loi (`return loi + [...]` -> `return [...]`: van DO, chi bot thong diep => TUONG DUONG, nhu luot 12) ·
           mode_moi_la_ca_hai (`... or trang_thai == "T"`: doi-kieu sang tep thuong bi DO) => 0/91 ca do.
  ket luan: LOI (P3) — xem HUONG 2.
HUONG 2: hau qua that cua song sot `mode_moi_la_ca_hai` (git 2.43 that)
  lenh   : python3 -B tmp/m13/t_sym2file.py $R
  output : symlink->tep (`:120000 100644 ... T ops/specs/x.md`): san pham rc=0 `kiem-re DAT (1 tep doi, 0 loi)`; dot bien rc=1 `kiem-re DO (1 tep doi, 3 loi)`.
           tep->symlink: ca hai rc=1 DO (dung).
  ket luan: LOI (P3, lop `kiem-mode-git-chot-khong-rang`, LAN THU 3 cua lop — §12): nhanh CHAP NHAN cua ve boolean
           `trang_thai == "D" or mode not in MODE_THUONG` voi trang thai `T` (doi kieu symlink->tep thuong, hop le theo docstring/SPEC
           "tep thuong theo mode trong git") KHONG co ca nao ghim; mot dot bien bien no thanh DO oan song qua 91 ca. Huong fail-close
           (false-red), khong fail-open => P3.

HUONG 3: ap HINT luot 13 len ban sao (tmp/hint13 = cp -a cay-kho) roi chay suite day du
  lenh   : python3 tmp/m13/mkhint.py tmp/hint13 ; (cd tmp/hint13 && python3 -B ops/ci_duong_nhanh_test.py) ; patch -p0 --fuzz=0 -i out/HINT.patch (ban sao sach tmp/pchk)
  output : `--mot-ca t20zf...` rc=0 tren san pham that; suite: `CA: 92/92 dat` · `DOT BIEN: 263/263 bi giet dung ly do` (dot bien moi
           `mode_git_doi_kieu_thanh_tep_la_loi` -> t20zf, ops/ci_duong_nhanh.py 150->151) · `TU KIEM PHAN HANG: DAT` · `TONG: DAT` rc=0;
           ruff F `All checks passed!`; patch rc=0, `cmp` BYTE_KHOP ban da do.
  ket luan: hint co rang (ca moi co chot fixture `T 120000 -> 100644`, dot bien rieng giet dung ly do).

HUONG 4: pham vi + so (blob master-side, do_lai_so, loi khai commit)
  lenh   : git diff --stat 9f5cb77/712ef9b/89fc4fa HEAD; git rev-parse HEAD:<f> vs 89fc4fa:<f>; merge-base --is-ancestor; python3 -B ../goi/do_lai_so.py; doctrine-scan
  output : `ops/lease_publish_test.py` 694cca5b… va `ops/specs/t131-deadline-dem-spawn.md` 1a99adbf… HEAD == 89fc4fa; 1741e0a, 89fc4fa la to tien
           => phan them la CUA MASTER. `git diff 89fc4fa HEAD` = dung 4 tep packet; ci_dang_ky_test numstat `1 0`.
           do_lai_so: 345 / 63 / 8; 113 lease dat 107 truot 6 (khop). doctrine-scan rc=0 (khop khai).
           Loi khai commit: "CA 91/91" = 90 + t20ze KHOP; "DOT BIEN 262/262" = 249 + 5 (hint luot 12) + 8 (ra soat) KHOP (dem trong diff: 13 dong moi).
  ket luan: KHONG PHAI LOI

HUONG 5: doi chieu tung dot bien hint luot 12 da ap (tep test)
  lenh   : git diff 9f5cb77 HEAD (doc) + suite nen (HUONG nen)
  output : (d) merge-tree ghim `a[-2:] == [GOC_A, GOC_B]` + mode_git_merge_tree_goc_goc/dau_dau -> t20u; (e) "raw dau ghi duoi thua" +
           mode_git_raw_match_khong_full -> t20zb; (f) "A mode 000000" + mode_git_xoa_bo_ve_D -> t20zb; (g) t20ze (kho that, ten `t\xff.md`,
           chot fixture byte, `except UnicodeError` -> TinHieuChotCa) + mode_git_raw_giai_ma_chat -> t20ze. Ca 5 GIET dung ly do trong 262/262.
  ket luan: DA VA THAT (d)(e)(f)(g).

HUONG 6: ci.yml / cac `if:` / nghiem thu 6-9 (ci.yml khong doi tu 712ef9b)
  lenh   : git diff --stat 712ef9b HEAD (chi tep test); git diff 89fc4fa HEAD -- ci.yml | grep if:/needs/timeout; actionlint; ci_dang_ky_test
  output : moi `if:` bo buoc chi mo khi `che_do == 'duong_nhanh'` (gia tri la/rong => day du); khong `always()`/`cancelled()`; chuan-bi co
           timeout-minutes 20 + buoc 10/5; actionlint rc=0; ci_dang_ky 938/938 TỔNG ĐẠT; y01..y16 dat trong suite.
  ket luan: KHONG PHAI LOI (dot bien YAML da do o luot 11 tren CUNG blob ci.yml; khong chay lai).

## DOI CHIEU LUOT TRUOC (luot 12, reviewed 9f5cb77 -> nay 8e204f3)
| lop / duong vao | hang luot 12 | trang thai | bang chung TU DO |
|---|---|---|---|
| `kiem-mode-git-chot-khong-rang` (d) doi so commit merge-tree | P3 | DA VA THAT | ghim `a[-2:]`; goc_goc/dau_dau GIET (262/262) |
| (e) `fullmatch` | P3 | DA VA THAT | kich ban "duoi thua"; match_khong_full GIET |
| (f) ve `trang_thai == "D"` nhanh bo qua xoa | P3 | DA VA THAT | kich ban "A mode 000000"; xoa_bo_ve_D GIET |
| (g) `surrogateescape` | P3 | DA VA THAT | t20ze kho that; giai_ma_chat GIET |
| ca lop (loi khai "ra soat he thong moi ... ve boolean") | — | VA HO (HEP) — lan thu 3 | HUONG 1-2: nhanh CHAP NHAN cua `T` voi mode thuong khong ca nao ghim |
| 5 lop cu (`kiem-re-cua-fail-close-chua-co-ca`, `kiem-re-bi-cau-hinh-boi-du-lieu-ho-so`, `phan-loai-khong-neo-merge-ref-that`, `cau-khai-skipped-nguoc-phep-do`, `dependency-failure-skips-required-checks`) | DONG | van DONG | san pham + ci.yml khong doi; suite 262/262 |

## BANG LOP
| slug | bieu hien | hang cao nhat con mo | phuong an va chung | phep kiem dong lop |
|---|---|---|---|---|
| `kiem-mode-git-chot-khong-rang` | chot/nhanh cua `kiem_mode_git`/`_doc_raw` go/doi ma khong ca nao DO. Duong vao CON MO (tu liet ke het nhanh cua ve boolean `trang_thai == "D" or mode not in MODE_THUONG` theo tung trang thai A/M/T/D x mode): (h) `T` + mode moi 100644/100755 => CHAP NHAN, khong ca ghim. Da xet, co rang: A/M thuong (t20a...), A 100755 (t20y), D 000000 (t20y), D mode khac 0 (t20zb), A 000000 (t20zb), T->gitlink (t20w), T->symlink (HUONG 2: san pham DO). Da xet TUONG DUONG: `return loi + [...]`, `--no-messages`. Da GIET (dot bien reviewer): bo `T` khoi regex, trang thai hang "M", chot dia chi o cap khac, cwd=ROOT cho hai lenh git. | P3 | ca kho that t20zf + dot bien `mode_git_doi_kieu_thanh_tep_la_loi` | `out/HINT.patch` — do: `CA 92/92` · `DOT BIEN 263/263` · `TONG: DAT` |
| 5 lop cu | — | DONG | — | nhu luot 12 |

## BANG DO (khang dinh -> dao khai -> do duoc -> khop?)
| khang dinh | nguon | do duoc | khop? |
|---|---|---|---|
| "ra soat he thong moi doi so / regex / giai ma / ve boolean cua kiem_mode_git va _doc_raw" | commit 8e204f3 | nhanh `T` chap nhan song (HUONG 1-2) | **khong** -> finding |
| CA 91/91, DOT BIEN 262/262, TU KIEM DAT, TONG DAT | commit | 91 / 262 / DAT / DAT | co |
| "8 dot bien moi" + 5 hint | commit | 13 dong moi trong DOT_BIEN; 262-249=13 | co |
| ci_dang_ky 23/23 + 938/938; ruff F sach; doctrine-scan rc=0 | commit | 938/938 TỔNG ĐẠT; ruff sach; rc=0 | co (dong 23/23 khong in rieng trong tail; TỔNG ĐẠT) |
| "San pham va ci.yml khong doi" | commit | diff 712ef9b..HEAD chi tep test | co |
| 345 / 63 / 8; 113 / 107 / 6 | DO_LAI | do_lai_so | co |
| G5 46,5/52 phut; "4 luot that" chan PR | DO_LAI | KHONG DO DUOC (khong mang) | — |

## NGHIEM THU (r2)
| # | ket qua | bang chung |
|---|---|---|
| 1-5 | dat (kem P3 tren) | suite 91/91 · 262/262 · TONG DAT |
| 6, 7 | dat | y01..y16 trong suite; ci.yml khong doi |
| 8, 9 | dat | actionlint rc=0; ci_dang_ky 938/938 |
| 10 | KHONG CHAY LAI luot nay (scripts/ khong doi; `git diff 89fc4fa HEAD` khong co scripts/) | — |
| 11 | chua_do_duoc | can PR that; executor KHONG khai dat |

## FINDINGS

### kiem-mode-git-chot-khong-rang  [P3]  (LAN THU 3 cua lop — §12) nhanh CHAP NHAN `T` + mode tep thuong cua `kiem_mode_git` khong co ca nao ghim
TEP/DONG: `ops/ci_duong_nhanh.py` `kiem_mode_git`: `if trang_thai == "D" or mode not in MODE_THUONG:` (dong 338); `ops/ci_duong_nhanh_test.py` (khong co ca T->tep thuong).
VAN DE: tu liet ke het nhanh cua ve boolean theo (trang thai x mode): moi o co ca ghim TRU `T` voi mode moi 100644/100755 (symlink/gitlink tren nen
  -> tep thuong trong PR). San pham CHAP NHAN o nay (dung docstring + SPEC "tep thuong theo mode trong git"), nhung dot bien
  `trang_thai in ("D", "T")` (DO oan moi doi kieu) song qua CA 91 ca. Git that: symlink->tep `:120000 100644 ... T` => san pham `kiem-re DAT`,
  dot bien `kiem-re DO (3 loi)`. Loi khai "ra soat he thong ... ve boolean" rong hon phep do. Huong fail-close (false-red), khong fail-open => P3.
  Day la lan thu 3 lop nay co finding (luot 11, 12, 13); moi lan duong vao KHAC nhau va hep dan (luot 13: mot o cua bang trang thai x mode).
DA THU VA: co — TEST-ONLY `out/HINT.patch` (dong 1 mang nhan bat buoc):
```diff
+@ca
+def t20zf_kiem_re_symlink_doi_thanh_tep_thuong_dat():
+    # kho_that(); tren main: them ops/specs/that.md + symlink ops/specs/x.md -> that.md, commit (goc); nhanh pr2: thay x.md bang tep thuong, commit (dau)
+    # chot fixture: `git diff --raw` phai co `^:120000 100644 <sha> <sha> T\tops/specs/x\.md$`
+    rc, log = kiem_re(m, kho, goc, dau); bang(rc == 0, ...)
+    ('mode_git_doi_kieu_thanh_tep_la_loi', _ma('            if trang_thai == "D" or mode not in MODE_THUONG:',
+        '            if trang_thai in ("D", "T") or mode not in MODE_THUONG:'), ('t20zf_kiem_re_symlink_doi_thanh_tep_thuong_dat',)),
```
  Symlink: `symlink_to` khong tha im lang, giong t20n/t20q/t20x/t20zd (buoc selftest chi Linux).
DA THU NGHIEM: HUONG 1 (song sot 0/91), HUONG 2 (git that, hau qua), HUONG 3 (hint tren ban sao: `CA: 92/92` · `DOT BIEN: 263/263 bi giet dung ly do` ·
  `TU KIEM PHAN HANG: DAT` · `TONG: DAT`; patch -p0 --fuzz=0 rc=0, byte khop).
DO TIN: cao (hang P3: vua — neu chu kho coi nhanh chap nhan `T` la ngoai pham vi "chot" thi day la ghi chu, nhung theo chuan luot 12 (decode_strict,
  fullmatch deu fail-close va deu tinh P3) thi phai tinh).

## GHI CHU QUY TRINH
- Moi ghi chi trong $R (tmp/m13, tmp/hint13, tmp/pchk, out/). Khong commit/push/checkout trong kho that hay wt-674; `cay-kho` khong bi sua.
  Khong mang, khong GitHub. Khong con job nen. HINT-sanpham.diff: khong can (finding test-only).

TONG: P0=0 P1=0 P2=0 P3=1 — so lop: 6 (1 mo: `kiem-mode-git-chot-khong-rang`; 5 dong)
