verdict: changes_requested
reviewed_sha: e73b266111141543cd48775c28fb0de8a20622ee
Reviewed commit: e73b266111141543cd48775c28fb0de8a20622ee

luot: 10 (packet #674 CI-DUONG-NHANH-HO-SO, dac ta r2 sha256 b6e719c9…da57 — da kiem khop; PROMPT.md sha256 774e45cc…6a89c — khop)
TONG: P0=0 P1=0 P2=0 P3=1 — 1 lop con mo (luot chay TRON; 3 lop luot 9 DA VA THAT)
Reviewer: Claude Opus 5.5 subagent, CUNG HO executor => advisory_review (KHONG cross_approved). Model/effort duoc phuc vu: KHONG DO DUOC.

## SO DO NEN (tu chay tren cay-kho @e73b266, Linux, git 2.43.0, shellcheck /usr/bin co mat)
- `python3 -B ops/ci_duong_nhanh_test.py`: `CA: 81/81 dat · 0 do · 0 hong` · `DOT BIEN: 204/204 bi giet dung ly do` · KIEM KE 53+16+3+9=81 · 2+68+92+42=204 · `TU KIEM PHAN HANG: DAT (5 mau rc, 3 dot bien that)` · `TONG: DAT` rc=0 (69,5s)
- `python3 -B .claude/dev/ci_dang_ky_test.py`: `ĐĂNG KÝ: 23/23` · `PHẢN CHỨNG: 938/938 đỏ đúng` · `TỔNG: ĐẠT` rc=0
- `actionlint .github/workflows/ci.yml` rc=0 · ruff 0.16.9 F hai tep moi: `All checks passed!`
- `goi/do_lai_so.py`: 345; 63; 8 · 113 tep lease, dat 107, truot 6 · `goi/kiem_ke.py`: 81 ca / 204 dot bien; ba ca du lieu loi=[] 5,7s
- numstat `.claude/dev/ci_dang_ky_test.py` 1741e0a..HEAD = `1 0` · AL_VER 4 (nen 1741e0a cung 4)


## DOI CHIEU LUOT TRUOC (3 lop luot 9, reviewed fc610c2 -> nay e73b266)
| lop (slug) | hang luot 9 | trang thai o e73b266 | bang chung TU DO |
|---|---|---|---|
| `kiem-re-bi-cau-hinh-boi-du-lieu-ho-so` | P3 | **DA VA THAT** — `--attr-source=<goc>` nay o MOI lenh git chay bo may diff/merge (ba cham, merge-tree, diff goc->cay, diff goc->github.sha, --check, --numstat); `merge-base` mien co ly do; t20u khoa tung loi goi + "khong loi goi ngoai hop dong" | dot bien RIENG (HUONG 1): attr_numstat_bo GIET t20t+t20u; attr_merge_tree_bo / attr_merge_tree_dau GIET t11e+t20u (t11e do tren git that: thuoc tinh PR bien xung dot thanh merge sach); attr_ba_cham_bo, attr_diff_cay_bo GIET t20u. Duong vao con lai da xet: eol/working-tree-encoding/ident chi doi byte cay lam viec ma cac buoc bi bo cung doc (khai trung thuc la "chua do rieng") — khong phai cua vao; `.gitmodules` chi o goc => day_du |
| `phan-loai-khong-neo-merge-ref-that` | P3 | **DA VA THAT** (manh hon hint: `github.sha` BAT BUOC, vang/hong => day_du, khong lui ve mo phong) | merge_bo_bat_buoc / merge_bo_strip0 GIET t05; merge_bo_hop / merge_none_bo_qua GIET t11d (git that); yaml bo/doi `CI_DUONG_NHANH_MERGE` (head.sha, merge_commit_sha, base.sha) o ca hai buoc GIET y01/y08 + y13; HUONG 4 tren git that |
| `cau-khai-skipped-nguoc-phep-do` | P3 | **DA VA THAT** | `grep -n "tinh la dat"` => rong o test/san pham/ci.yml/DO_LAI.md; y01 nay noi "context bat buoc KHONG duoc tao va PR bi CHAN"; RUN_BUOC_PACKET chu thich (test:1555) cung sua |

Pham vi: `git diff 1741e0a e73b266` co them `ops/lease_publish_test.py` + `ops/specs/t131-deadline-dem-spawn.md` — blob o HEAD TRUNG blob o master 89fc4fa
(`694cca5b…`, `1a99adbf…`), 89fc4fa va 1741e0a deu la to tien cua HEAD => phan them do la CUA MASTER (#680), khong phai cua packet. `scripts/` khong doi so 1741e0a.

## BANG SAN (ghi tang dan)
HUONG 1: rang cua MOI chot moi o e73b266 (dot bien RIENG cua reviewer tren cay toi thieu `tmp/mut10/cay_<ten>`, chay 81 ca bang `--mot-ca`)
  lenh       : python3 -B tmp/mut10/mut.py tmp/mut10/m1.json  (log tmp/mut10/run1.log)
  output     : nen: chi k01 DO (tao tac cay rut gon — thieu tep dang ky; co mat o MOI dot bien, bo qua)
               merge_bo_bat_buoc GIET t05 `thieu merge ref` · merge_bo_strip0 GIET t05 `merge ref toan 0` · merge_bo_hop GIET t11d (git that) ·
               merge_none_bo_qua GIET t11d `merge ref rc=128` · merge_bo_mo_phong (chi giu diff goc->github.sha) GIET t11c ·
               attr_ba_cham_bo GIET t20u · attr_merge_tree_bo GIET t11e + t20u · attr_merge_tree_dau (--attr-source=dau) GIET t11e + t20u ·
               attr_diff_cay_bo GIET t20u · attr_numstat_bo GIET t20t + t20u ·
               yaml_chuanbi_bo_merge / _merge_head / _merge_mcs (merge_commit_sha) GIET y01 + y13 · yaml_kiemre_bo_merge / _merge_base GIET y08 + y13
  ket luan   : KHONG PHAI LOI — 15/15 dot bien bi giet dung ca dich, 0 song sot

HUONG 2: gitlink (mode 160000) duoi allowlist — duong vao con lai cua lop `kiem-re-cua-fail-close-chua-co-ca` (loai tep)
  gia thuyet : `kiem_loai_tep` chi hoi `is_symlink()`; `kiem_yaml`/`kiem_lease` coi `not is_file()` la DA XOA; gitlink checkout thanh THU MUC rong
               => khong chot nao thay no, trai voi cau khai "duong nhanh chi nhan tep thuong" va voi cach xu tep nhi phan (khong kiem duoc => DO)
  lenh       : bash tmp/h1/gitlink.sh <duong...> (clone tam cua cay-kho, update-index --cacheinfo 160000, merge ref --no-ff, chay that
               `ops/ci_duong_nhanh.py` va `kiem-re` voi du 4 bien)
  output     : master/HEAD: `git ls-files -s` => 0 gitlink, 0 symlink toan kho; duoi allowlist 1874x100644 + 1x100755
               numstat gitlink `1 0` (khong phai `- -`) · `--check` rc=0
               [ops/leases/zz-gitlink.yaml, ops/land/zz-sub] => kiem-re DO — CHI nho ca du lieu t23 (IsADirectoryError), khong phai chot cua kiem-re
               [ops/land/zz-sub, ops/land/zz.yaml, ops/reviews/zz-verdict.md] => DO — chi nho t27 (muc luc README)
               [ops/land/zz-sub, ops/land/zz.yaml, ops/specs/zz.md] => `phan loai duong_nhanh` · `kiem-re DAT (3 tep doi, 0 loi)` rc=0
               lease_publish_test tren merge do (buoc bi bo): `187/187 đạt` rc=0 (gitlink khong lam do buoc nay)
  ket luan   : LOI (P3, cau khai rong hon phep do + chot fail-close thieu cua) -> `kiem-re-cua-fail-close-chua-co-ca`. Cac buoc nang khac tren
               merge do: dang do (packet_loop / golden / determinism / release-check), ket qua ghi o HUONG 2b.

HUONG 3: nghiem thu 8, 9 tu do (ban sao `tmp/nt89` tu `git archive HEAD`)
  output     : NT8 chen `# chu thich ${{ }}` sau dong kiem-re => actionlint rc=1 `ci.yml:552:142: unexpected end of input ... [expression]`; ban goc rc=0.
               NT9a go muc DA_NOI => `ĐỎ: test sống chưa đăng ký: ops/ci_duong_nhanh_test.py` · `ĐĂNG KÝ: 23/22` · `TỔNG: ĐỎ` rc=1
               NT9b thay `run: python ops/ci_duong_nhanh_test.py` (dong 560, loi goi duy nhat trong moi workflow) => `ĐỎ: CI không gọi mục đăng ký: ops/ci_duong_nhanh_test.py` rc=1
               numstat 1741e0a..HEAD `.claude/dev/ci_dang_ky_test.py` = `1 0`
  ket luan   : KHONG PHAI LOI

HUONG 2b: cac buoc NANG bi bo, chay tren chinh merge co gitlink (`tmp/h1/gl-4708` @9be4b09: ops/land/zz-sub, ops/land/zz.yaml, ops/specs/zz.md)
  lenh       : bash tmp/h1/heavy.sh (log tmp/h1/heavy.log; phan doi chung `goc` bi dung chu dong vi ve `hop` da xanh het)
  output     : lease_publish_test `187/187 đạt` · packet_loop_test `TỔNG: ĐẠT` rc=0 · golden-test `"ok": true` · determinism-audit strict `"ok": true` ·
               release-check full `"ok": true`
  ket luan   : duong nhanh KHONG yeu hon duong day du cho gitlink (duong day du cung cho qua) => khong P2. Con lai la cau khai
               ("duong nhanh chi nhan tep thuong", "moi tep .yaml doi con trong cay phai parse duoc") rong hon hanh vi + chot fail-close
               khong nhat quan voi quyet dinh cua chinh lop (nhi phan khong kiem duoc => DO) => P3.

HUONG 4: bien the merge ref THAT (tmp/h1/gl-4708, git that)
  lenh       : chay `ops/ci_duong_nhanh.py` voi MERGE = merge that / SHA khong ton tai / = base.sha; va base.sha CU (89fc4fa) voi merge that
  output     : merge that => duong_nhanh (3 tep) · SHA khong co object => `KHONG DO DUOC ... fail-close ve DAY_DU` · MERGE=base.sha => duong_nhanh
               (diff rong, hop khong them gi — chi dat duoc khi sua env; y01/y08 khoa gia tri `${{ github.sha }}`, dot bien doi thanh head/base/merge_commit_sha deu bi giet — HUONG 1)
               base.sha cu => `DAY_DU vi diff co 4 tep ngoai allowlist` (thay doi cua nhanh dich lot vao hop => fail-close dung chieu)
  ket luan   : KHONG PHAI LOI. Tan suat base.sha != cha-1 cua github.sha tren GitHub: KHONG DO DUOC (chi anh huong hieu qua, khong an toan).

HUONG 5: ruff / actionlint / so trong docstring
  output     : actionlint rc=0; ruff F sach (2 tep, ca ban hint); `do_lai_so.py` 345/63/8, 113 lease dat 107 truot 6; "ba tep .gitattributes duoi ops/reviews" =>
               `git ls-files` 3; "master: 0 tep nhi phan duoi allowlist" => numstat cay rong->HEAD tren 4 tien to: 0/0/0/0; AL_VER 4 = nen
  ket luan   : KHONG PHAI LOI

## BANG LOP
| slug | bieu hien | hang cao nhat con mo | phuong an va chung | phep kiem dong lop |
|---|---|---|---|---|
| `kiem-re-cua-fail-close-chua-co-ca` (luot 8, MO LAI o cua moi) | loai "tep" ma kiem-re khong kiem duoc noi dung phai DO. Duong vao: (a) symlink — DONG (t20n/t20q); (b) nhi phan — DONG (t20s/t20t); (c) **gitlink mode 160000 — MO**: checkout thanh thu muc rong, `kiem_loai_tep` chi hoi symlink, `kiem_yaml`/`kiem_lease` coi `not is_file()` la da xoa, numstat `1 0`, `--check` rc=0; (d) tep doi thanh thu muc cung ten — KHONG phai loi (cac tep con duoc kiem), phai la doi chung khong chan oan; (e) mode 100755 — tep thuong, khong mo | P3 | `kiem_loai_tep` DO moi duong dan trong diff la THU MUC ma khong co tep con (con trong cay) nam trong diff; HOAC thu hep cau khai | t20v (2 gitlink: `.yaml` duoi land + khong duoi duoi specs, 3 chot chung minh fixture; doi chung tep->thu muc DAT) + 3 dot bien `loai_tep_cho_gitlink_qua`, `loai_tep_gitlink_chi_yaml`, `loai_tep_gitlink_chan_oan_thu_muc` |
| `kiem-re-bi-cau-hinh-boi-du-lieu-ho-so` | — | DONG | — | t20u + t11e/t20p/t20t |
| `phan-loai-khong-neo-merge-ref-that` | — | DONG | — | t05/t11d + y01/y08/y13 |
| `cau-khai-skipped-nguoc-phep-do` | — | DONG | — | grep rong |

## BANG DO (khang dinh -> dao khai -> do duoc -> khop?)
| khang dinh | nguon | do duoc | khop? |
|---|---|---|---|
| 345 / 63 / 8 | docstring D1 | `do_lai_so.py`: 345; 63; 8 | co |
| 6/113 (clone mot ref) | docstring D2 | 113 tep, dat 107 truot 6 (clone nay); 0/113 tren 552 ref KHONG DO DUOC | co (phan do duoc) |
| ba tep `.gitattributes` duoi `ops/reviews/` | D1 | `git ls-files` => 3 | co |
| master: 0 tep nhi phan duoi allowlist | D1, kiem_nhi_phan | numstat cay rong->HEAD 4 tien to: 0 | co |
| `-diff` tren CRLF lam merge-tree mat doi ten thu muc, xung dot thanh sach | D1, t11e | hai chot fixture cua t11e DAT tren git 2.43 (rc 0 vs rc 1) | co |
| "--name-only --no-renames khong doc thuoc tinh" | D1 | dot bien go attr o 2 lenh do chi bi t20u giet (hop dong), khong ca hanh vi nao — khop voi cau khai "khong phai va duong da do" | co |
| `github.sha` = commit moi job checkout va test | ci.yml, D | KHONG DO DUOC offline (theo tai lieu actions/checkout) — khai trung thuc | — |
| "duong nhanh chi nhan tep thuong" / "moi tep .yaml doi con trong cay phai parse duoc" | kiem_loai_tep, kiem_yaml | gitlink `ops/land/zz.yaml` qua kiem-re DAT (HUONG 2) | **khong** |
| CA / DOT BIEN khong ghim so; DO_LAI | bo test | 81/81 · 204/204; kiem_ke 81/204 | co |
| 23/23, 938/938, numstat `1 0`, AL_VER 4 | NT9 / DO_LAI | 23/23 · 938/938 · `1 0` · 4 | co |
| G5 46,5/52 phut; "4 luot that" | ci.yml / DO_LAI | KHONG DO DUOC (khong mang) | — |

## NGHIEM THU (r2) — bang chung tu chay
| # | ket qua | bang chung |
|---|---|---|
| 1-5 | dat | suite `CA 81/81 · DOT BIEN 204/204 · TONG: DAT`; 15 dot bien rieng (HUONG 1) |
| 6, 7 | dat | y01..y16; dot bien YAML rieng o HUONG 1 deu bi giet dung ca |
| 8 | dat | actionlint rc=0 (shellcheck co mat); chen `${{ }}` => rc=1 (HUONG 3) |
| 9 | dat | 23/23, 938/938; numstat `1 0`; NT9a/NT9b DO dung thong diep (HUONG 3) |
| 10 | dat | `== tl selftest 1715/1715 ==` rc=0 (clone sach `tmp/nt10` @e73b266, core.abbrev 7); ruff F `scripts/tl.py` `Found 12 errors` = nen CLAUDE.md; `scripts/` khong doi so 1741e0a => delta 0 |
| 11 | chua_do_duoc | can PR that; executor KHONG khai dat (dung) |

## DOT BIEN SONG SOT
Khong co. 15/15 dot bien rieng cua toi bi giet dung ca dich (k01 DO o MOI dot bien ke ca doi chung `nen` = tao tac cay rut gon, loai tru). Ban hint: `DOT BIEN: 207/207`.

## FINDINGS

### kiem-re-cua-fail-close-chua-co-ca  [P3]  gitlink (mode 160000) duoi allowlist qua kiem-re; `kiem_yaml` coi gitlink ten `.yaml` la "da xoa"
TEP/DONG: `ops/ci_duong_nhanh.py` `kiem_loai_tep` (dong 262-271), `kiem_yaml` (`if not tep.is_file(): continue`), `kiem_lease` (cung mau).
VAN DE: PR them tree entry gitlink duoi `ops/{land,specs}/**` (vd `ops/land/zz.yaml`). actions/checkout (khong submodule) dung thu muc rong.
  `kiem_loai_tep` chi hoi `is_symlink()`; `kiem_yaml`/`kiem_lease` nhan `not is_file()` la tep DA XOA va bo qua; numstat `1 0` (khong bi coi nhi phan);
  `--check` rc=0. Do tren git that: `phan loai duong_nhanh` · `kiem-re DAT (3 tep doi, 0 loi)` rc=0. Duoi `ops/leases/`/`ops/reviews/` chi DO NHO ca du
  lieu t23/t27 (IsADirectoryError / muc luc), khong nho chot cua kiem-re. Trai voi cau khai "duong nhanh chi nhan tep thuong" va voi quyet dinh cua
  chinh lop nay o luot 9 (tep nhi phan khong kiem duoc noi dung => KHONG DO DUOC => DO). Master: 0 gitlink, 0 symlink toan kho => ho so khong can.
  P3, khong P2: da chay moi buoc nang bi bo tren chinh merge do (HUONG 2b) — lease_publish 187/187, packet_loop DAT, golden/determinism/release-check ok —
  tuc duong day du cung cho qua; duong nhanh khong yeu hon duong day du, loi la cau khai + chot fail-close thieu cua.
DA THU VA: co — san pham (`out/HINT-sanpham.diff`):
```diff
-    return [f"tep ho so la symlink (duong nhanh chi nhan tep thuong): {duong!r}"
+    return ([f"tep ho so la symlink (duong nhanh chi nhan tep thuong): {duong!r}"
             for duong in sorted(doi) if (Path(kho) / duong).is_symlink()]
+            # Cross-review luot 10: gitlink (mode 160000) duoi allowlist checkout thanh THU MUC — kiem_yaml/kiem_lease coi
+            # `not is_file()` la DA XOA va bo qua, `--check`/`--numstat` khong co noi dung de kiem. Master: 0 gitlink.
+            # Mot duong dan trong diff la THU MUC ma khong co con nao con trong cay nam trong diff = gitlink; tep doi thanh
+            # thu muc cung ten thi cac tep con (con trong cay) nam trong diff => khong chan oan.
+            + [f"tep ho so khong phai tep thuong (gitlink/thu muc - kiem-re khong kiem duoc noi dung): {duong!r}"
+               for duong in sorted(doi) if not (Path(kho) / duong).is_symlink() and (Path(kho) / duong).is_dir()
+               and not any(x.startswith(duong + "/") and (Path(kho) / x).is_file() for x in doi)])
```
  (Giu nguyen neo `for duong in sorted(doi) if (Path(kho) / duong).is_symlink()]` cua 4 dot bien co san.) Ban dau cua toi dung `is_dir()` tran va DO
  OAN PR doi tep ho so thanh thu muc cung ten (da do: `tmp/h1/tepthanhdir.py`) — nen co doi chung rieng.
  Chot rieng tung duong vao (test, `out/HINT.patch`): ca `t20v_kiem_re_gitlink_ho_so_do` — hai gitlink (`ops/land/zz.yaml`, `ops/specs/con`), moi cai
  3 chot chung minh fixture (ls-tree `160000 commit`; `kiem_yaml`, `kiem_nhi_phan`, `--check` goc cung KHONG thay), doi kiem-re rc=1 + `khong phai tep
  thuong` + ten; doi chung tep->thu muc cung ten phai DAT. Dot bien: `loai_tep_cho_gitlink_qua` (tat chot), `loai_tep_gitlink_chi_yaml` (chi chan `.yaml`
  => `ops/specs/con` lot), `loai_tep_gitlink_chan_oan_thu_muc` (bo dieu kien tep con => doi chung DO).
  Phuong an thay the neu executor khong muon doi hanh vi: thu hep cau khai (thong diep kiem_loai_tep, docstring kiem_yaml) cho dung "chi symlink bi chan;
  gitlink di qua nhu duong day du" — ban ghi ro rang cung dong duoc lop.
  Lua chon manh hon (khong lam): doc mode tu git (`ls-files -s`) thay vi tu cay lam viec — doc lap nen (Windows `core.symlinks=false` checkout symlink
  thanh tep thuong) nhung them mot loi goi git phai xep vao hop dong t20u.
DA THU NGHIEM: HEAD: `bash tmp/h1/gitlink.sh ops/land/zz-sub ops/land/zz.yaml ops/specs/zz.md` => kiem-re DAT rc=0; test hint tren san pham HEAD
  (`CI_DUONG_NHANH_CAY=cay-kho`) => `DO:t20v...: ops/land/zz.yaml: gitlink ho so phai DO kiem-re: rc=0` rc=3. Ban ap du (`tmp/hint10`):
  `CA: 82/82 dat` · `DOT BIEN: 207/207 bi giet dung ly do` · `TU KIEM PHAN HANG: DAT` · `TONG: DAT` rc=0; ruff F sach. Hai tep hint ap sach bang
  `patch -p0 --fuzz=0` len `git archive HEAD` va `cmp` khop ban da do.
DO TIN: cao (co che, git that); muc do nghiem trong thap (duong day du cung cho qua).

## DAC TA (khong bat executor sua)
- M1 chi noi "diff base...head"; hop voi diff goc->merge-tree va goc->github.sha la SIEU TAP (chi them day_du) — khong mau thuan M4.
- NT11: G5 khong nam trong danh sach bo (Q6) => "ngan hon ro ret" phu thuoc #668 (giu nhan xet luot 8/9).
- Dac ta khong noi loai tep (symlink/gitlink) nao duoc phep duoi allowlist; Q2 chi noi tien to.

## GIOI HAN / CHUA DO DUOC
GitHub that (merge ref, base.sha cu, fork, required check khi `chuan-bi` do), phien ban git cua runner (can `--attr-source`, `merge-tree --write-tree`;
thieu => fail-close), Windows, thoi gian runner, 552 ref, served model/effort cua luot nay. Khong mang, khong GitHub, khong cham `cay-kho`
(git status sach, HEAD e73b266), moi dot bien tren ban sao duoi `tmp/`. Khong con tien trinh nen.

## TEP
- `out/VERDICT.md` · `out/HINT.patch` (chi `ops/ci_duong_nhanh_test.py`, sha256 c7e1af08…9f74) · `out/HINT-sanpham.diff` (`ops/ci_duong_nhanh.py`, sha256 d78551e3…22cb)
- Phep do: `tmp/mut10/{mut.py,mk1.py,m1.json,run1.log}` · `tmp/h1/{gitlink.sh,heavy.sh,heavy.log,tepthanhdir.py,t20v_head2.log}` · `tmp/nen_suite.log` `tmp/nen_dk.log`
  `tmp/nt10_selftest.log` `tmp/hint10_suite2.log` · cay hint `tmp/hint10`

TONG: P0=0 P1=0 P2=0 P3=1
So lop: 1 con mo (`kiem-re-cua-fail-close-chua-co-ca`, P3); 3 lop luot 9 DA VA THAT.
