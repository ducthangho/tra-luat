verdict: changes_requested
reviewed_sha: 712ef9bef610b00a6cc2574712b52ad4e23a355b
Reviewed commit: 712ef9bef610b00a6cc2574712b52ad4e23a355b

luot: 11 (packet #674 CI-DUONG-NHANH-HO-SO, dac ta r2 sha256 b6e719c9…da57 — da kiem khop; PROMPT.md sha256 12388feb…b4b3 — khop)
TONG: P0=0 P1=0 P2=0 P3=1 — 1 lop con mo (moi, test-only); lop luot 10 DA VA THAT; luot chay TRON
Reviewer: Claude Opus 5.5 subagent, CUNG HO executor => advisory_review (KHONG cross_approved). Model/effort duoc phuc vu: KHONG DO DUOC.

## SO DO NEN (tu chay tren cay-kho @712ef9b, Linux, shellcheck /usr/bin co mat)
- `python3 -B ops/ci_duong_nhanh_test.py`: `CA: 88/88 dat · 0 do · 0 hong` · `DOT BIEN: 228/228 bi giet dung ly do` · KIEM KE 60+16+3+9=88 · 2+68+116+42=228 · `TU KIEM PHAN HANG: DAT (5 mau rc, 3 dot bien that)` · `TONG: DAT` rc=0 (1m07s)
- `python3 -B .claude/dev/ci_dang_ky_test.py`: `PHẢN CHỨNG: 938/938 đỏ đúng` · `TỔNG: ĐẠT`
- `actionlint .github/workflows/ci.yml` rc=0 · ruff F hai tep moi `All checks passed!` · numstat ci_dang_ky_test 1741e0a..HEAD `1 0`
- `git diff --stat e73b266 HEAD -- .github/` rong (ci.yml khong doi) · dong `AL_VER:` 5 o 1741e0a/89fc4fa/e73b266/HEAD (delta 0)
- Pham vi: blob `ops/lease_publish_test.py` 694cca5b… va `ops/specs/t131-deadline-dem-spawn.md` 1a99adbf… o HEAD == o 89fc4fa; 1741e0a va 89fc4fa la to tien HEAD => phan them la CUA MASTER.
- `goi/do_lai_so.py`: 113 tep lease, dat 107 truot 6 (khop luot 10)

## BANG SAN (ghi tang dan)
HUONG 1: rang cua tung chot moi cua `kiem_mode_git` (dot bien RIENG cua reviewer, ban sao `tmp/m11/cay_<ten>`, 88 ca bang `--mot-ca`, CI_DUONG_NHANH_CAY)
  gia thuyet : neu mot chot/doi so cua `kiem_mode_git` go ra ma khong ca nao do thi chot do khong co rang
  lenh       : python3 -B tmp/m11/mut.py $R tmp/m11/m1.json  (log tmp/m11/run1.log)
  output     : nen: k01, k02, t91 DO o MOI dot bien ke ca `nen` = tao tac cay rut gon (thieu tep dang ky / entrypoint) — loai tru.
               GIET: dia_bo_isfile (t20z) · dia_moi_cap (t20u, t20zb) · raw_bo_no_abbrev (10 ca that) · raw_nhan_U (t20zb) · mode_cu (12 ca) ·
                     thay_gan (t20u, t20zb) · lech_chi_thieu (t20zb) · merge_tree_dung_dau (t20u, t20za) · mt_attr_dau (t20u)
               SONG SOT: raw_bo_no_renames · lech_chi_thua (`thay != set(doi)` -> `not thay <= set(doi)`) · raw_mode_trong
                     (`trang_thai == "D" or mode not in ...` -> `mode not in ...`) · dia_bo_symlink
  ket luan   : LOI (P3) -> lop moi `kiem-mode-git-chot-khong-rang` (3 song sot dau). dia_bo_symlink: TUONG DUONG o muc lenh — `kiem_loai_tep`
               da DO moi duong dan doi la symlink tren dia (t20n/t20q), nhanh `is_symlink()` trong chot dia la du thua => KHONG PHAI LOI.

HUONG 2: song sot `raw_bo_no_renames` co HAU QUA that khong (git that, clone cay-kho, PR `git mv ops/land/plat-x8-land-evidence.yaml -> ...-moi.yaml`, merge --no-ff)
  lenh       : bash tmp/m11/rename.sh <san pham>  (ban that / ban dot bien)
  output     : `git diff --raw` mac dinh => `R100` (diff.renames mac dinh bat).
               ban that: `che_do=duong_nhanh` · `kiem-re DAT (2 tep doi, 0 loi)` rc=0
               dot bien: `LOI - KHONG DO DUOC: git diff --raw <goc>...<dau> so muc le (dau ra hong)` · `kiem-re DO` rc=1
  ket luan   : LOI (P3, cung lop): go `--no-renames` khoi `_doc_raw` lam MOI PR doi ten tep ho so DO oan o required check `gate-ops`
               (fail-close, khong fail-open) ma 88 ca + 228 dot bien khong ca nao bat; t20u chi khoa `--attr-source`, khong khoa co.

HUONG 3: DOI CHIEU luot 10 tren git THAT + duong vao con lai cua lop (clone cay-kho, PR that, merge --no-ff, chay `ci_duong_nhanh.py` + `kiem-re`)
  gia thuyet : neu `kiem_mode_git` chi phu cac fixture cua executor thi gitlink duoi `ops/reviews`/`ops/leases` hoac ten tep la van lot / DO oan
  lenh       : for k in nonascii tabname newline xoa gitlink_reviews gitlink_leases_yaml; do bash tmp/m11/kb.sh $k; done
  output     : nonascii (`ops/specs/đặc-tả thử.md`) => duong_nhanh · kiem-re DAT rc=0 (raw -z va name-only -z cung giai ma, tap khop)
               tabname / newline => `day_du` (ky tu dieu khien, _duong_dan_sach) · xoa tep ho so => kiem-re DAT rc=0
               gitlink_reviews (`ops/reviews/zz-sub`) => `LOI - ... (mode 160000, A, cap goc -> merge ref)` kiem-re DO rc=1 — nay DO bang CHOT CUA
               kiem-re (luot 10 chi DO nho t27); gitlink_leases_yaml => mode 160000 DO + ca du lieu t23 cung DO
  ket luan   : KHONG PHAI LOI — cua gitlink luot 10 dong that, ke ca hai tien to luot 10 chi "do nho ca du lieu"

HUONG 4: nghiem thu 8, 9 tu do (ban sao `tmp/nt89` tu `git archive HEAD`)
  output     : NT8 chen `# chu thich ${{ }}` sau dong kiem-re => actionlint rc=1 `ci.yml:552:142: unexpected end of input ... [expression]`; ban goc rc=0
               NT9a go muc DA_NOI (dong 76) => `ĐỎ: test sống chưa đăng ký: ops/ci_duong_nhanh_test.py` · `ĐĂNG KÝ: 23/22` · `TỔNG: ĐỎ`
               NT9b thay `run: python ops/ci_duong_nhanh_test.py` (loi goi duy nhat) => `ĐỎ: CI không gọi mục đăng ký: ops/ci_duong_nhanh_test.py` · `TỔNG: ĐỎ`
  ket luan   : KHONG PHAI LOI

HUONG 5: nghiem thu 10 (clone sach `tmp/nt10b` @712ef9b, core.abbrev 7)
  output     : `== tl selftest 1715/1715 ==` rc=0 · ruff F `scripts/tl.py` `Found 12 errors.` = nen CLAUDE.md · `git diff --stat 1741e0a HEAD -- scripts/` rong => delta 0
  ket luan   : KHONG PHAI LOI

HUONG 6: so trong docstring/bang do (goi/do_lai_so.py, goi/kiem_ke.py, grep)
  output     : AL_VER regex t152 => 4 o HEAD va 1741e0a (grep tran "AL_VER:" => 5 ca hai ve, delta 0) · kiem_ke 88 ca/228 dot bien = dong KIEM KE ·
               do_lai_so 113 lease dat 107 truot 6 · t20x "gate-ops co chay Windows": ma tran gate-ops = `fromJson(needs.chuan-bi.outputs.os)` => dung ·
               t20u `SO_LOI_GOI = {"merge-tree": 2}` khop so lan goi that (dot bien mt_attr_dau bi t20u giet)
  ket luan   : KHONG PHAI LOI — khong khang dinh dinh luong moi nao lech

HUONG 7: ci.yml / pham vi
  output     : `git diff --stat e73b266 HEAD -- .github/` rong; buoc kiem-re (ci.yml:543-555) va buoc selftest (557-560) giu nguyen nhu luot 10 da xet;
               blob master-side trung 89fc4fa; numstat ci_dang_ky_test `1 0`
  ket luan   : KHONG PHAI LOI (Windows: KHONG DO DUOC — khong co runner Windows trong sandbox)

## DOI CHIEU LUOT TRUOC (luot 10, reviewed e73b266 -> nay 712ef9b)
| lop (slug) | hang luot 10 | trang thai o 712ef9b | bang chung TU DO |
|---|---|---|---|
| `kiem-re-cua-fail-close-chua-co-ca` (gitlink) | P3 | **DA VA THAT** (manh hon hint: doc MODE trong git thay heuristic thu muc; phu them symlink tren nen core.symlinks=false, doi kieu T, git-co-dia-khong) | HUONG 3: gitlink duoi ops/reviews va ops/leases nay DO bang chot rieng; HUONG 1: 9 dot bien rieng cua toi len `kiem_mode_git` bi giet dung ca (t20u/t20z/t20za/t20zb + 10 ca git that); ca 24 dot bien cua executor bi giet (suite 228/228) |
| `kiem-re-bi-cau-hinh-boi-du-lieu-ho-so` | DONG | van DONG | `--attr-source=<goc>` co o merge-tree + 3 `--raw` moi; mt_attr_dau GIET t20u |
| `phan-loai-khong-neo-merge-ref-that` | DONG | van DONG | cap `goc -> merge ref` dung `hop`; dot bien doi sang `dau` (executor) va merge_tree_dung_dau (toi) deu bi giet |
| `cau-khai-skipped-nguoc-phep-do` | DONG | van DONG | ci.yml khong doi |

## BANG LOP
| slug | bieu hien | hang cao nhat con mo | phuong an va chung | phep kiem dong lop |
|---|---|---|---|---|
| `kiem-mode-git-chot-khong-rang` (MOI, luot 11) | chot/doi so cua `kiem_mode_git` go ra ma 88 ca khong ca nao DO. Duong vao (tu liet ke het cac chot cua ham, 13 dot bien): (a) co `--no-renames` cua `_doc_raw` — SONG, hau qua that: PR doi ten tep ho so DO oan (HUONG 2); (b) chieu "thieu" cua chot tap `thay != set(doi)` — SONG (t20zb chi co chieu "thua"); (c) nhanh `trang_thai == "D" or` — SONG (kich ban "D mode khac 0" dung 160000 nen bi chot MODE giet thay). Da xet va KHONG mo: `--no-abbrev`, `-z` (moi ca git that DO), `[AMDT]`, group(2), `thay |=`, cap cay/hop, `--attr-source`, is_file dia; `is_symlink` o chot dia = tuong duong (kiem_loai_tep phu) | P3 | ca git that doi ten DAT + 2 kich ban t20zb | `out/HINT.patch`: t20zc + "tap thieu" + "D mode tep thuong" + 3 dot bien `mode_git_raw_bo_no_renames`, `mode_git_tap_chi_bat_thua`, `mode_git_xoa_chi_theo_mode` — da do tren ban sao: `CA 89/89` · `DOT BIEN 231/231` · `TONG: DAT` |
| `kiem-re-cua-fail-close-chua-co-ca` | — | DONG | — | t20v..t20zb + HUONG 3 |
| `kiem-re-bi-cau-hinh-boi-du-lieu-ho-so` | — | DONG | — | t20u + t11e/t20p/t20t |
| `phan-loai-khong-neo-merge-ref-that` | — | DONG | — | t05/t11d + y01/y08/y13 |
| `cau-khai-skipped-nguoc-phep-do` | — | DONG | — | grep rong (luot 10), ci.yml khong doi |
| `dependency-failure-skips-required-checks` | — | DONG (theo PROMPT) | — | — |

## BANG DO (khang dinh -> dao khai -> do duoc -> khop?)
| khang dinh | nguon | do duoc | khop? |
|---|---|---|---|
| "merge-tree chay HAI lan o kiem-re, cung doi so" | test SO_LOI_GOI | t20u DAT; mt_attr_dau GIET t20u | co |
| "Tep doi thanh thu muc cung ten la HOP LE: D + A 100644" | docstring kiem_mode_git | t20y DAT; mode_git_xoa_la_loi GIET t20y | co |
| "symlink tren core.symlinks=false checkout thanh tep thuong" | kiem_mode_git, t20x | fixture t20x chot va DAT tren git that | co |
| "moi cach KHONG DO DUOC => DO" (gom "tap duong dan KHAC tap doi") | kiem_mode_git, t20zb | chi chieu "thua" co ca; chieu "thieu" SONG (lech_chi_thua) | **mot nua** -> finding |
| "chi nhan mode moi 100644/100755 hoac XOA (D, 000000)" | docstring | nhanh D-voi-mode-thuong SONG (raw_mode_trong) | **khong co ca** -> finding |
| AL_VER 4 (regex t152) | DO_LAI | 4 (HEAD, 1741e0a) | co |
| CA/DOT BIEN khong ghim so | DO_LAI | 88/88 · 228/228; kiem_ke 88/228 | co |
| 23/23, 938/938, numstat `1 0` | NT9 | 938/938 · `1 0` | co |
| tl selftest N/N; ruff delta 0 | NT10 | 1715/1715; 12 = nen | co |
| G5 46,5/52 phut; "4 luot that" | DO_LAI | KHONG DO DUOC (khong mang) | — |

## NGHIEM THU (r2) — bang chung tu chay
| # | ket qua | bang chung |
|---|---|---|
| 1-5 | dat | suite `CA 88/88 · DOT BIEN 228/228 · TONG: DAT` |
| 6, 7 | dat | y01..y16 trong suite; ci.yml khong doi so e73b266 (luot 10 da dot bien YAML rieng) |
| 8 | dat | HUONG 4 |
| 9 | dat | HUONG 4 + `ĐĂNG KÝ: 23/23` · `PHẢN CHỨNG: 938/938` · `TỔNG: ĐẠT`; numstat `1 0` |
| 10 | dat | HUONG 5 |
| 11 | chua_do_duoc | can PR that; executor KHONG khai dat (dung) |

## DOT BIEN SONG SOT
`raw_bo_no_renames`, `lech_chi_thua`, `raw_mode_trong` (finding duoi); `dia_bo_symlink` = tuong duong o muc lenh (kiem_loai_tep phu), khong tinh.

## FINDINGS

### kiem-mode-git-chot-khong-rang  [P3]  ba chot/doi so cua `kiem_mode_git` khong co ca nao do; mot trong so do co hau qua DO oan that
TEP/DONG: `ops/ci_duong_nhanh.py` `_doc_raw` (doi so `"--no-renames"`, dong 284) · `kiem_mode_git` (`if thay != set(doi):`; `if trang_thai == "D" or mode not in MODE_THUONG:`);
  `ops/ci_duong_nhanh_test.py` t20u (chi khoa `--attr-source`), t20zb (kich ban "tap lech" chi chieu thua; "D mode khac 0" dung 160000).
VAN DE: (a) Go `--no-renames` khoi `_doc_raw`: 88/88 van DAT. Tren git that `git diff` mac dinh do doi ten => ban ghi `R100` hai duong dan =>
  `so muc le (dau ra hong)` => MOI PR doi ten tep ho so DO oan o `gate-ops` (required). Fail-close nen khong phai lo an ninh, nhung la hoi quy kha dung
  ma bo test khong canh. (b) Chot tap chi co ca cho chieu "raw thua ten"; chieu "doi co ten ma khong cap --raw nao liet ke" (tuc mode ten do KHONG
  duoc kiem = fail-open neu xay ra) doi thanh `not thay <= set(doi)` van 88/88. (c) Nhanh `trang_thai == "D"` voi mode tep thuong (ban ghi hong)
  khong co ca rieng: kich ban "D mode khac 0" mang 160000 nen chot MODE giet thay.
DA THU VA: co — TEST-ONLY `out/HINT.patch` (nhan bat buoc o dong 1):
```diff
@@ t20zb kich_ban
         ("tap lech", dict(raw={"ba_cham": (0, tot + raw_ghi(("100644", "A", "ops/land/them.md")))}), "lech tap da phan loai"),
+        ("tap thieu", dict(raw={"ba_cham": (0, b""), "cay": (0, b"")}), "lech tap da phan loai"),
+        ("D mode tep thuong", dict(raw={"ba_cham": (0, raw_ghi(("100644", "D", d)))}), "mode 100644, D"),
     )
+@ca
+def t20zc_kiem_re_doi_ten_tep_ho_so_dat():
+    # kho_that: nen ops/land/a.yaml, PR xoa a.yaml + them b.yaml cung noi dung; chot fixture: `git diff --raw` mac dinh co " R100\t";
+    # kiem_re(...) phai rc == 0
+    ('mode_git_raw_bo_no_renames', ... bo "--no-renames" o _doc_raw ...), ('t20zc_kiem_re_doi_ten_tep_ho_so_dat',)),
+    ('mode_git_tap_chi_bat_thua', 'if thay != set(doi):' -> 'if not thay <= set(doi):'), ('t20zb_...',)),
+    ('mode_git_xoa_chi_theo_mode', 'if trang_thai == "D" or mode not in MODE_THUONG:' -> 'if mode not in MODE_THUONG:'), ('t20zb_...',)),
```
  Chot rieng tung duong vao: (a) t20zc + `mode_git_raw_bo_no_renames`; (b) "tap thieu" + `mode_git_tap_chi_bat_thua`; (c) "D mode tep thuong" +
  `mode_git_xoa_chi_theo_mode`. Ba chot phan biet duoc bang dau vao (moi dot bien chi lam DO ca cua no — suite phan hang "dung ly do" xac nhan).
  Thay the cho (a): khoa bo co cua `--raw` trong t20u (it gia tri hon vi khong do HAU QUA).
DA THU NGHIEM: HUONG 1 (song sot), HUONG 2 (hau qua that cua (a)); ban ap hint `tmp/hint11/k` (clone @712ef9b + `patch -p0 --fuzz=0`):
  t20zc, t20zb `--mot-ca` rc=0 tren san pham that; suite day du `CA: 89/89` · `DOT BIEN: 231/231 bi giet dung ly do` · `TU KIEM PHAN HANG: DAT` · `TONG: DAT`;
  ruff F `All checks passed!`.
DO TIN: cao

## GHI CHU QUY TRINH
- Mot lan ghi ngoai $R do so suat: `cp ci.yml /tmp/x_ci.bak` (ban sao chep tu `tmp/nt89`, khong phai tep kho); da xoa ngay. Khong commit/push/checkout nao
  trong kho that hay wt-674; `cay-kho` khong bi sua (moi dot bien tren ban sao `tmp/m11`, `tmp/hint11`, `tmp/nt89`, `tmp/nt10b`).
- Khong con job nen nao chay.

TONG: P0=0 P1=0 P2=0 P3=1 — so lop: 6 (1 mo: `kiem-mode-git-chot-khong-rang`; 5 dong)
