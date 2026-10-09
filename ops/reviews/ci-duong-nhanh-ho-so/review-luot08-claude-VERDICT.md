verdict: changes_requested
reviewed_sha: 57b6578398a63c2afe4e583061440b3156aec155
Reviewed commit: 57b6578398a63c2afe4e583061440b3156aec155
luot: 8 (packet #674 CI-DUONG-NHANH-HO-SO, dac ta r2 sha256 b6e719c9…da57 — da kiem khop)

TONG: P0=0 P1=0 P2=1 P3=3 — 4 lop con mo (bang lop duoi)

## Danh tinh va muc bao dam
- Reviewer: Claude Opus 5.5 (subagent, ngu canh moi), CUNG HO voi executor => `advisory_review`, KHONG phai `cross_approved`.
  Model/effort thuc chay cua luot nay: KHONG DO DUOC (khong co receipt runtime doc lap). Packet `sensitive` => cong land
  van can `human_audited`/Codex; verdict nay khong cap quyen land.
- PROMPT.md sha256 = c7c2b02b…2e877 (khop). Chi ghi trong `rv8/out` va `rv8/tmp`; cay-kho khong bi sua (moi dot bien/hint
  chay tren `git clone` rieng trong `rv8/tmp`). Khong mang, khong GitHub, khong Windows.

## SO DO NEN (tu chay tren cay-kho @57b6578, Linux, git 2.43.0, shellcheck co mat)
| lenh | ket qua |
|---|---|
| `python3 -B ops/ci_duong_nhanh_test.py` | `CA: 71/71 dat · 0 do · 0 hong` · `DOT BIEN: 168/168 bi giet dung ly do` · `KIEM KE: ca hanh_vi=43 + cau_truc_yaml=16 + so_dang_ky=3 + tu_kiem=9 = 71 · dot bien ...=2 + ...=65 + ...=59 + ...=42 = 168` · `TU KIEM PHAN HANG: DAT (5 mau rc, 3 dot bien that)` · `TONG: DAT` · 44,6s |
| `python3 -B .claude/dev/ci_dang_ky_test.py` | `ĐĂNG KÝ: 23/23` · `PHẢN CHỨNG: 938/938 đỏ đúng` · `TỔNG: ĐẠT` · rc=0 |
| `actionlint .github/workflows/ci.yml` | rc=0 (shellcheck /usr/bin/shellcheck co mat) |
| ruff F (0.16.9) hai tep moi · `scripts/tl.py` | `All checks passed!` · 12 F821 (= nen CLAUDE.md; diff khong cham tl.py => delta 0) |
| `git diff --numstat 1741e0a HEAD -- .claude/dev/ci_dang_ky_test.py` | `1 0` (dong duy nhat `+    "ops/ci_duong_nhanh_test.py",`) |
| `git diff 89fc4fa 57b6578 -- ops/lease_publish_test.py ops/specs/` | rong => hai tep them so voi 1741e0a la CUA MASTER (#680, 819d6b0/4864d99), khong phai cua packet |
| `python3 -B scripts/tl.py --selftest` (clone sach @57b6578, ve `nen` cua tmp/gl2.sh) | `== tl selftest 1715/1715 ==` rc=0 |
| `goi/do_lai_so.py` | `345; 63; 8` khop docstring; `113 tep, dat 107, truot 6` — khop "6/113 tren clone mot-pham-vi" (clone nay co 45 ref; so "0/113 tren 552 ref" KHONG DO DUOC o day) |
| `goi/kiem_ke.py` | 71 ca / 168 dot bien / BO_QUA gate 5 · gate-ops 3 · gate-packet-loop 1; ba ca du lieu tren kho that `loi = []`, 5,1s |

## DOI CHIEU LUOT TRUOC (HOP ba verdict luot 7 tren af1165d)
| lop (slug) | nguon luot 7 | trang thai o 57b6578 | bang chung TU DO |
|---|---|---|---|
| `buoc-bi-bo-doc-ca-cay-khong-chi-ba-ca` P2 (symlink TREO lam t82 do tren master) | 91b942b F1 | **DA VA THAT** cho duong symlink treo; cua gitlink do KHONG co delta; hai duong vao moi tim duoc thuoc lop KHAC (xem duoi) | `tmp/gl.sh`: symlink hop le `ops/reviews/zz-link.md` => kiem-re `LOI - tep ho so la symlink ... DO`; `tmp/gl2.sh` (gitlink `ops/land/zz-sub`, hai ve trong MOT lenh): golden/determinism/release-check rc=0 ca hai ve, packet_loop `TỔNG: ĐẠT` ca hai, lease_publish `187/187` ca hai, tl selftest `1715/1715` ca hai => delta 0 |
| `kiem-re-cua-fail-close-chua-co-ca` P2 (9 cua + cua `safe_load_all`) | 14fa441 + 91b942b F2 | **DA VA THAT** cho cac cua da neu; **VA HO o cap lop** — con 2 cua khong rang (finding P3 duoi) | dot bien rieng cua toi: `yaml_xoa_break` => `[DO] t20i…` CA 70/71; `diffcheck_128_qua` => `[DO] t20m…` CA 70/71; `cadulieu_dat_trong_log_la_qua` => `[DO] t22b…`; `kiem_yaml_chi_tai_lieu_dau` co trong 168 (t20o). SONG: `loai_tep_chi_chan_treo`, `loai_tep_chi_md`, `diffcheck_chi_md` (CA 71/71) |
| `kiem-re-phu-thuoc-actor-su-kien` P3 | ca hai | **DA KHAI** (chu kho chon khai D2) — nhung cau khai rong hon hanh vi (finding P3 duoi, ve CACH KHAI, khong ve chinh sach) | `GITHUB_ACTOR='claude[bot]'`: xoa lease => `kiem_lease` = `[]`; sua lease that => `kiem lease (het han) rc=8 …` |
| `bang-do-thieu-neo-va-thieu-kiem-ke` P3 (dong `TU KIEM PHAN HANG:` khong neo) | g3 | **DA VA THAT** | hai dot bien `test_main_tu_kiem_in_so_sai`, `test_main_tu_kiem_luon_in_dat` nam trong 168 va bi giet dung ca dich t93 (dong 1839-1840) |
| `diff-check-tu-ha-nguong` P3 (bo `-space-before-tab` van xanh) | g3 | **DA VA THAT** | `d1_bo_space_before_tab` => `[DO] t20d…` `[DO] t23…` CA 69/71 TONG DO |
| `kiem-re-bo-sot-duong-vao` P3 (`.yml` + tep xoa trong kiem_yaml) | g3 | **DA VA THAT** (trung voi dong hai) | `yaml_xoa_break` => t20i DO; `.yml` => t20h co trong 168 |
| `chot-yaml-chi-do-su-hien-dien`, `bang-do-...` (no #694) | luot 6 | khong hoi quy | `yml_kiemre_chi_linux` (them `&& runner.os == 'Linux'` vao if kiem-re) => `[DO] y04 y08 y12 y13` CA 67/71 |

## BANG LOP
| slug | bieu hien | hang cao nhat con mo | phuong an va chung | phep kiem dong lop |
|---|---|---|---|---|
| `phan-loai-ba-cham-mu-voi-nhieu-merge-base` (MOI) | `git diff base...head` khi >1 merge-base chi dung MOT base (git in `warning: … multiple merge bases, using …`) => thay doi ma ma merge that mang vao base bi giau => `duong_nhanh`. Cung duong vao do `kiem_diff_check` (ba cham) | **P2** | `doc_diff` doi `git merge-base --all goc dau` tra DUNG MOT SHA 40 hex; khac (0, >=2, rc!=0, nem, lac dang) => None => `day_du` (M4 "khong do duoc") | t11b: 4 do gia (hai base / khong base / nem / lac dang) + fixture criss-cross git THAT co chung minh fixture (hai merge-base, merge that doi `scripts/tl.py`); 2 dot bien (bo chot dang, bo loi goi) |
| `kiem-re-cua-fail-close-chua-co-ca` | cua cua kiem-re khong co ca: (a) symlink HOP LE / symlink khong `.md` (docstring khai "treo hay khong"); (b) pham vi `diff --check` — dau xung dot trong tep ho so KHONG phai `.md`/YAML | P3 | moi cua mot ca hanh vi + mot dot bien thu hep | t20q (2 symlink hop le: `.md`, `.yaml`) + dot bien `loai_tep_chi_chan_treo`, `loai_tep_chi_md`; t20r (`.patch` `.json` `.txt`) + dot bien `diff_check_chi_md` |
| `kiem-re-bi-cau-hinh-boi-du-lieu-ho-so` (MOI) | `.gitattributes` duoi allowlist (`conflict-marker-size`) tat bao dau xung dot cua `kiem_diff_check`; docstring D1 khai "bat ke cau hinh" | P3 | `kiem_loai_tep` chan moi tep ten `.gitattributes` trong diff; sua cau khai | t20p (co chung minh fixture: attr TAT duoc diff-check) + dot bien `loai_tep_bo_gitattributes` |
| `kiem-re-phu-thuoc-actor-su-kien` | cau khai D2 "PR ho so cham `ops/leases/` do bot … se DO" — XOA lease do bot van DAT | P3 | sua cau khai (khong doi chinh sach) | doc lai docstring; (tuy chon) ca khoa "xoa lease khong kiem" |

## BANG SAN
HUONG 1: ba cham voi lich su criss-cross (nhieu merge-base)
  gia thuyet : neu base va head co >1 merge-base thi `git diff base...head` dung MOT base, giau thay doi ma merge that mang vao => fail-OPEN
  lenh       : bash rv8/tmp/cc.sh (kho tam: X1 merge vao master (m2) cheo voi M1 merge vao X (x2); X dao `scripts/tl.py` v2->v1; them `ops/land/y.yaml`)
  output     : `merge-base --all`: 2 SHA; `warning: 32bfbc6…148aff7: multiple merge bases, using 7be55a9`;
               diff base...head = `ops/land/y.yaml`; merge that so base = `ops/land/y.yaml` + `scripts/tl.py` (tren merge = v1, tren base = v2);
               `phan_loai: ('duong_nhanh', 'DUONG_NHANH: toan bo 1 tep doi khop allowlist ops/{land,leases,reviews,specs}/** - dung duong nhanh')`
  ket luan   : LOI -> `phan-loai-ba-cham-mu-voi-nhieu-merge-base` [P2]

HUONG 2: gitlink (mode 160000) duoi allowlist — cua vao khac cua `buoc-bi-bo-doc-ca-cay-khong-chi-ba-ca`
  gia thuyet : gitlink `ops/land/zz-sub` (checkout thanh thu muc rong) qua kiem-re ma lam mot buoc bi bo DO => fail-open
  lenh       : bash rv8/tmp/gl.sh ; bash rv8/tmp/gl2.sh (hai ve nen/gitlink dung trong MOT lenh, chay moi buoc bi bo)
  output     : phan loai `duong_nhanh`; kiem-re `DAT (1 tep doi, 0 loi)`; t82 `DAT`; ca hai ve: golden 0 · determinism 0 · release-check 0 ·
               packet_loop `TỔNG: ĐẠT` · lease_publish `187/187 đạt` · tl selftest `1715/1715`
  ket luan   : KHONG PHAI LOI (delta 0 tren moi buoc bi bo)

HUONG 3: symlink HOP LE + rang cua chot symlink (va 91b942b)
  gia thuyet : docstring `kiem_loai_tep` khai "chan moi symlink, treo hay khong"; dot bien thu hep ve "chi treo"/"chi .md" van xanh => chot thieu rang
  lenh       : bash rv8/tmp/gl.sh (bien symhople) ; python3 -B rv8/tmp/mut8.py loai_tep_chi_chan_treo loai_tep_chi_md
  output     : HEAD dung: `DUONG_NHANH: LOI - tep ho so la symlink ... 'ops/reviews/zz-link.md'` `kiem-re DO`. t82 voi symlink hop le `DAT` (khong delta).
               Hai dot bien: `CA: 71/71 dat · 0 do · 0 hong` · `DOT BIEN: 167/168` · `TONG: DO` — DO CHI vi neo cua dot bien co san
               `loai_tep_cho_symlink_qua` hong (`HONG RuntimeError: ha tang: neo dot bien phai xuat hien DUNG MOT lan, thay 0`) = TIN DUNG GIA
  ket luan   : LOI -> `kiem-re-cua-fail-close-chua-co-ca` [P3]

HUONG 4: tiem lenh workflow / gia dong log qua ten tep
  gia thuyet : ten tep chua U+2028/U+0085 hoac `::…::` lam gia dong log/GITHUB_OUTPUT
  lenh       : python3 -c (phan_loai_tu_diff voi ten ngoai allowlist chua U+2028/U+0085; `ops/land/a b.yaml`)
  output     : ten ngoai allowlist in qua repr => ` `/`\x85` bi thoat; ten ho so chua U+2028 duoc nhan (khong < 32) nhung moi noi in
               ten trong kiem-re qua `!r` va thong diep loi qua `splitlines()` (tach ca U+2028); `che_do` la hang
  ket luan   : KHONG PHAI LOI

HUONG 5: nghiem thu 8 va 9 tu do
  lenh       : actionlint tren ban sao ci.yml chen `# chu thich ${{ }}` vao than run kiem-re ; python3 -B rv8/tmp/nt9.py
  output     : NT8 rc=1 `ci.yml:549:48: unexpected end of input while parsing … [expression]`; PyYAML van parse ban goc.
               NT9: bo muc DA_NOI => `ĐỎ: test sống chưa đăng ký: ops/ci_duong_nhanh_test.py` `ĐĂNG KÝ: 23/22` `TỔNG: ĐỎ` rc=1;
               bo `run: python ops/ci_duong_nhanh_test.py` => `ĐỎ: CI không gọi mục đăng ký: ops/ci_duong_nhanh_test.py` rc=1
  ket luan   : KHONG PHAI LOI

HUONG 6: `.gitattributes` duoi allowlist cau hinh lai `kiem-re`
  gia thuyet : docstring D1 khai dau xung dot la "thu `--check` bao bat ke cau hinh"; neu du lieu ho so cau hinh duoc `--check` thi khai sai va kiem-re co cua
  lenh       : bash rv8/tmp/ga.sh (PR them `ops/land/x.md` co dau xung dot 7 ky tu; bien `co-attr` them `ops/land/.gitattributes` = `* conflict-marker-size=40`)
  output     : khong-attr: `kiem_diff_check= ['git diff --check rc=2: ops/land/x.md:2: leftover conflict marker | …']`
               co-attr   : `phan_loai= duong_nhanh kiem_diff_check= []`
  ket luan   : LOI -> `kiem-re-bi-cau-hinh-boi-du-lieu-ho-so` [P3]

HUONG 7: rang cua cac cua kiem-re (dot bien rieng cua reviewer, `rv8/tmp/mut8.py`, moi cai mot clone)
  output     : xem bang DOT BIEN duoi. Song theo hanh vi: `diffcheck_chi_md` (`--check` chi `*.md`) => `CA: 71/71`, TONG DO chi vi dot bien co san
               `diff_check_bo_mien_blank_at_eof` bi keo thanh SONG_SOT = tin dung gia
  ket luan   : LOI -> `kiem-re-cua-fail-close-chua-co-ca` [P3] (cua (b))

HUONG 8: chinh sach actor — tim loi trong CACH KHAI
  lenh       : `GITHUB_ACTOR='claude[bot]' python3 -c "... m.kiem_lease({'ops/leases/da-xoa-khong-con.yaml'}) ; m.kiem_lease({<lease that>})"`
  output     : `xoa: []` · `sua: ["kiem lease (het han) rc=8 cho 'ops/leases/ci-noi-bang-vao-gate-exec-1-claude-20260822.yaml…"]`
  ket luan   : LOI (cach khai) -> `kiem-re-phu-thuoc-actor-su-kien` [P3]

HUONG 9: G5 va nghiem thu 11 (cua so 52/46,5 phut)
  lenh       : grep cac `if:` trong job `gate` (dong 147 `G5 kiem ban ke cong cu + T1..T8 (packet #290)` khong co `if:` theo `che_do`)
  output     : G5 van chay tren duong nhanh; docstring/khai G5 = 46,5/52 phut (KHONG DO DUOC offline)
  ket luan   : DAC TA (khong tinh P): neu so 46,5/52 dung thi NT11 "ngan hon ro ret" KHONG dat duoc bang packet nay mot minh — no phu
               thuoc #668 chia G5 (dac ta r2 da buoc #674 land sau #668; Q6 cam mo rong JOB_G5). Can do lai tren PR that sau #668.

## BANG DO (khang dinh -> dao khai -> do duoc -> khop?)
| khang dinh | nguon | do duoc | khop? |
|---|---|---|---|
| 345 / 63 / 8 | docstring D1 | `do_lai_so.py`: 345; 63; 8 | co |
| ~13% | docstring D1 | 8/63 = 12,7% | co |
| 6/113 (clone mot ref) vs 0/113 (552 ref) | docstring D2 | 113 tep, truot 6, clone nay co 45 ref (`for-each-ref` = 45); 552 ref KHONG DO DUOC | co (phan do duoc) |
| ba ca du lieu ~6 giay | docstring `kiem_ca_du_lieu` | 5,1s (may nay) | co |
| ci_dang_ky 22/22 -> 23/23, 938/938 | DO_LAI | 23/23, 938/938 (nen 22/22 KHONG tu do lai o luot nay) | co (ve sau) |
| AL_VER 4 dong | DO_LAI | khong doi so voi master (diff ci.yml khong cham AL_VER) | co |
| dau xung dot bi bat "bat ke cau hinh" | docstring D1 | SAI: `conflict-marker-size` trong `.gitattributes` tat duoc (HUONG 6) | **khong** |
| "chan moi symlink, treo hay khong" | docstring `kiem_loai_tep` | hanh vi dung; RANG chi phu symlink treo `.md` (HUONG 3) | hanh vi co / rang khong |
| "PR ho so cham `ops/leases/` do bot … se DO" | docstring D2 | xoa lease do bot => DAT (HUONG 8) | **khong** (rong hon) |
| G5 46,5/52 phut; `skipped` = dat cho required check | DO_LAI | KHONG DO DUOC (khong mang/PR that) | — |

## NGHIEM THU (r2) — bang chung tu chay
| # | ket qua | bang chung |
|---|---|---|
| 1-5 | dat | suite `CA 71/71 · DOT BIEN 168/168` (ca t1/t2/t9/t3/t5/t6/t8/t10 + dot bien); dot bien rieng `yml_kiemre_chi_linux` bi giet dung |
| 6, 7 | dat | ca y01..y16 trong 71/71; dot bien ci.yml 65/65 trong 168 |
| 8 | dat | actionlint rc=0 (co shellcheck); chen `${{ }}` => rc=1 |
| 9 | dat | 23/23, 938/938; numstat `1 0`; hai dot bien cua NT9 DO dung thong diep |
| 10 | dat | tl selftest 1715/1715 (clone sach); ruff tl.py 12 F821, packet khong cham tl.py => delta 0 |
| 11 | chua_do_duoc | can PR that; xem HUONG 9 (DAC TA) |
| M1/M4 | **LECH** o ca criss-cross | finding P2 duoi |

## DOT BIEN CUA REVIEWER (rv8/tmp/mut8.py; log o rv8/tmp/mut8/*.log)
| dot bien | ket qua |
|---|---|
| loai_tep_chi_chan_treo | **SONG** (CA 71/71; TONG DO chi do neo co san hong = tin dung gia) |
| loai_tep_chi_md | **SONG** (nhu tren) |
| diffcheck_chi_md | **SONG** (CA 71/71; tin dung gia qua dot bien co san) |
| d1_bo_space_before_tab | GIET — t20d, t23 |
| yaml_xoa_break | GIET — t20i |
| diffcheck_128_qua | GIET — t20m |
| cadulieu_dat_trong_log_la_qua | GIET — t22b |
| yml_kiemre_chi_linux | GIET — y04 y08 y12 y13 |
| d1_them_cr_at_eol | song, TUONG DUONG (blank-at-eol da tat thi cr-at-eol khong doi gi) |
| han_chuoi_khong_tz_none | song, TUONG DUONG (`lease_publish` tu choi han khong mui gio o ca hai duong; kho: 112 nhay ngoac co `Z`, 1 khong nhay) |
| het_han_bien_nhat (`<=` -> `<`) | song, TUONG DUONG thuc te (chi khac khi han == bay gio den micro giay) |
| tukiem_so_sai | khong chay duoc rieng (neo xuat hien 2 lan vi CHINH dot bien nay da co trong DOT_BIEN — `test_main_tu_kiem_in_so_sai`, bi giet trong 168) |

## FINDINGS

### phan-loai-ba-cham-mu-voi-nhieu-merge-base  [P2]  Criss-cross: `base...head` giau thay doi ma cua merge that => PR doi `scripts/tl.py` ra `duong_nhanh`
TEP/DONG: `ops/ci_duong_nhanh.py` `doc_diff` (dong 106-127; loi goi `git diff … f"{goc}...{dau}"` dong 115); cung duong vao: `kiem_diff_check` (dong 192).
VAN DE: Ba cham = diff tu MOT merge-base toi head. Khi base va head co >=2 merge-base (lich su criss-cross: nhanh tai dung sau khi
  da merge, hoac merge master cu vao nhanh trong khi master da merge nhanh), git in `warning: …: multiple merge bases, using X` va
  lay MOT base; con merge that cua GitHub (refs/pull/N/merge, ort) dung base AO de quy. Thay doi ma nam "giua" hai base bien mat
  khoi `base...head` nhung VAN vao base khi merge. Do duoc: merge that doi `scripts/tl.py` (v2 -> v1), `phan_loai` tra `duong_nhanh`.
  Day la fail-OPEN cua dung bat bien loi cua packet (tep ngoai allowlist => day_du), va kiem-re cung dung ba cham nen khong bu.
  Hau qua: tl selftest/golden/release-*… bi bo tren PR mang ma; master push chay day du sau merge (thay duoc), nen P2 chu khong P1.
  Xac suat thap (can criss-cross), nhung phep va re va nam TRONG M4 ("git khong do duoc => day_du").
  DAC TA: M1 ghi "diff base...head (ba cham)" ma khong noi gi ve nhieu merge-base — ba cham khong xac dinh duy nhat trong ca ay; `chua_do_duoc` muc 2
  ghi "chi do duoc tren GitHub" nhung phan git la do duoc tai cho (HUONG 1).
DA THU VA: co — san pham (ap tay):
```diff
--- a/ops/ci_duong_nhanh.py
+++ b/ops/ci_duong_nhanh.py
@@ -111,6 +112,16 @@ def doc_diff(env=os.environ, chay=subprocess.run, kho=ROOT):
         return None
     if not all(MAU_SHA.fullmatch(x) and x.strip("0") for x in (goc, dau)):
         return None
+    # Ba cham chi dung MOT merge-base. Lich su criss-cross (>1 merge-base) thi `base...head` co the GIAU thay doi
+    # ma merge that mang vao base (reviewer luot 8: PR dao scripts/tl.py van ra duong_nhanh) => KHONG DO DUOC.
+    try:
+        mb = chay(["git", "merge-base", "--all", goc, dau], cwd=kho, capture_output=True)
+    except Exception:
+        return None
+    ra_mb = getattr(mb, "stdout", None)
+    if getattr(mb, "returncode", None) != 0 or not isinstance(ra_mb, (bytes, bytearray)) \
+            or not re.fullmatch(rb"[0-9a-f]{40}\n", bytes(ra_mb)):
+        return None
     try:
         r = chay(["git", "diff", "--name-only", "--no-renames", "-z", f"{goc}...{dau}"],
                  cwd=kho, capture_output=True)
```
  Test (trong `out/HINT.patch`): `chay_gia` them tham so `merge_base` (mac dinh mot SHA hop le; `BaseException` => nem; rong => rc=1);
  ca `t11b_nhieu_merge_base_la_khong_do_duoc`: 4 do gia (hai base / khong base / nem / lac dang) moi cai => day_du, doi chung mot base
  => duong_nhanh, va fixture criss-cross git THAT co hai chot chung minh fixture (dung 2 merge-base; merge that doi `scripts/tl.py`).
  Chot rieng tung duong vao: dot bien `mot_merge_base_bo_chot_dang` (gõ phep so dang) va `mot_merge_base_bo_goi` (khong goi git) — ca hai dich t11b.
  `kiem_diff_check` duoc bao ho vi `lenh_kiem_re` chi goi no khi `doc_diff` da ra duong_nhanh.
DA THU NGHIEM: HEAD: `tmp/cc.sh` (output o HUONG 1). Chi ap phan TEST len clone HEAD (`tmp/chi_test.py`): `t11b … rc=3
  DO:t11b…:hai merge-base: phai la day_du (fail-close)`; t01, t06 van rc=0. Ban ap du hint (`tmp/hint8`, gom ca ba finding duoi):
  `CA: 75/75` · `DOT BIEN: 174/174 bi giet dung ly do` · `KIEM KE: … = 75 · … ops/ci_duong_nhanh.py=65 … = 174` · `TU KIEM PHAN HANG: DAT` · `TONG: DAT` · rc=0; ruff F sach.
  KHONG DO DUOC: hanh vi GitHub that voi criss-cross (base.sha cua su kien, merge ref) — phan git la tat dinh va da do.
DO TIN: cao (co che); thap (tan suat thuc te).

### kiem-re-cua-fail-close-chua-co-ca  [P3]  Hai cua cua kiem-re khong co rang: symlink HOP LE/khong `.md`, va pham vi `diff --check` ngoai `.md`
TEP/DONG: `ops/ci_duong_nhanh.py` `kiem_loai_tep` (dong 181-186), `kiem_diff_check` (dong 189-199); `ops/ci_duong_nhanh_test.py` `t20n`, `t20c`.
VAN DE: (a) docstring khai "chan moi symlink, treo hay khong" nhung t20n chi co MOT symlink TREO duoi `.md`; dot bien chi chan symlink
  treo, hoac chi chan `.md`, cho `CA: 71/71`. (b) t20c chi co dau xung dot trong `.md`; dot bien gioi han `--check` ve `*.md` cho
  `CA: 71/71` — dau xung dot trong `.patch`/`.json`/`.txt` ho so (kiem_yaml khong bat ho) se lot. Ca ba dot bien bao `TONG: DO` CHI vi
  lam hong neo/doi ket qua cua dot bien co san => tin dung gia (dung hinh dang CLAUDE.md "dot bien bi giet khong dung ly do").
  Liet ke cua cua lop (kiem-re): YAML {duoi, xoa, nhieu tai lieu, PyYAML} · diff-check {tung loai D1, xung dot, nem, rc, **pham vi tep**} ·
  lease {duoi, xoa, het/con han, han hong, nem, parse} · ca du lieu {goi, ten, rc} · loai tep {treo, **hop le**, **moi duoi**}. Da chot tat ca tru hai muc in dam.
DA THU VA: co — chi tep test, trong `out/HINT.patch`: ca `t20q_kiem_re_symlink_hop_le_moi_duoi_do` (symlink HOP LE `ops/reviews/hop-le.md`
  va `ops/land/l.yaml` -> `../../README.md`, co chot fixture `exists()`), dot bien `loai_tep_chi_chan_treo`, `loai_tep_chi_md` dich t20q;
  ca `t20r_kiem_re_dau_xung_dot_moi_duoi_tep_do` (`.patch`, `.json`, `.txt`), dot bien `diff_check_chi_md` dich t20r.
DA THU NGHIEM: HEAD: `tmp/mut8/loai_tep_chi_chan_treo.log`, `loai_tep_chi_md.log`, `diffcheck_chi_md.log` (CA 71/71). Ban hint: 174/174 GIET dung ly do.
DO TIN: cao (lo chot); thap (hoi quy thuc te).

### kiem-re-bi-cau-hinh-boi-du-lieu-ho-so  [P3]  `.gitattributes` duoi allowlist tat bao dau xung dot cua kiem-re; docstring D1 khai "bat ke cau hinh"
TEP/DONG: `ops/ci_duong_nhanh.py` docstring D1 (dong 44-45), `kiem_loai_tep` (dong 181-186), `kiem_diff_check` (dong 189-199).
VAN DE: `git diff --check` doc thuoc tinh tu cay lam viec; `ops/land/.gitattributes` = `* conflict-marker-size=40` lam dau xung dot 7 ky tu
  khong con la "marker" => `kiem_diff_check` = `[]`, PR van `duong_nhanh`, kiem-re DAT. Cau "thu `--check` bao bat ke cau hinh" SAI
  (dung voi `core.whitespace`, sai voi thuoc tinh). Docstring module da khai allowlist khong chan tac gia co y, nen P3 — nhung cau khai
  sai la loi doc lap voi y do. Duong vao khac cung lop (da xet): thuoc tinh `whitespace=` (bat lai loai D1 da tat => DO oan, huong dong),
  `text eol=` (doi byte checkout cua tep ho so — t26 cung doc cung checkout nen kiem-re va duong day du thay nhu nhau).
DA THU VA: co — san pham:
```diff
@@ -42,7 +42,8 @@
     sẽ chặn oan ~13% đúng lớp PR mà đường nhanh sinh ra để giải. Bản tinh chỉnh vẫn bắt dấu xung đột còn sót
-    (`<<<<<<<`, `=======`, `>>>>>>>`), thứ `--check` báo bất kể cấu hình.
+    (`<<<<<<<`, `=======`, `>>>>>>>`), thứ `--check` báo bất kể `core.whitespace` — NHƯNG không bất kể thuộc tính
+    `conflict-marker-size` trong `.gitattributes`, nên `kiem_loai_tep` chặn `.gitattributes` dưới allowlist.
@@ -181,9 +192,13 @@ def kiem_yaml(doi, kho=ROOT) -> list[str]:
 def kiem_loai_tep(doi, kho=ROOT) -> list[str]:
     """…
-    master trong khi mọi kiểm khác của `kiem-re` vẫn DAT. Hồ sơ không cần symlink ⇒ chặn mọi symlink, treo hay không."""
-    return [f"tep ho so la symlink (duong nhanh chi nhan tep thuong): {duong!r}"
+    master trong khi mọi kiểm khác của `kiem-re` vẫn DAT. Hồ sơ không cần symlink ⇒ chặn mọi symlink, treo hay không.
+    `.gitattributes` dưới allowlist đổi cách git ĐỌC/KIỂM hồ sơ (vd `conflict-marker-size` tắt báo dấu xung đột của
+    `kiem_diff_check` — reviewer lượt 8 đo) ⇒ hồ sơ không cần nó, chặn."""
+    loi = [f"tep ho so la symlink (duong nhanh chi nhan tep thuong): {duong!r}"
             for duong in sorted(doi) if (Path(kho) / duong).is_symlink()]
+    return loi + [f"tep ho so la .gitattributes (doi cach git kiem ho so): {duong!r}"
+                  for duong in sorted(doi) if duong.rsplit("/", 1)[-1] == ".gitattributes"]
```
  (Dong `for duong in sorted(doi) if (Path(kho) / duong).is_symlink()]` giu NGUYEN de neo dot bien co san khong hong.)
  Test trong `out/HINT.patch`: ca `t20p_kiem_re_gitattributes_trong_ho_so_do` — chot fixture doi `kiem_diff_check(...) == []` (chung minh
  thuoc tinh TAT duoc bao) roi doi kiem-re rc=1 va log co `.gitattributes`; dot bien `loai_tep_bo_gitattributes` dich t20p.
DA THU NGHIEM: HEAD: `tmp/ga.sh` (HUONG 6). Ban hint: t20p DAT, dot bien GIET (trong 174/174).
DO TIN: cao.

### kiem-re-phu-thuoc-actor-su-kien  [P3]  Cau khai D2 rong hon hanh vi: "PR ho so cham `ops/leases/` do bot … se DO" — xoa lease do bot van DAT
TEP/DONG: `ops/ci_duong_nhanh.py` docstring dong 53-56; hanh vi `kiem_lease` dong 226-228 (`if not tep.is_file(): continue`).
VAN DE: Chinh sach (giu chot actor, khai thay vi doi) la cua chu kho, KHONG phai finding. Loi nam o cau chu: "cham" gom ca XOA, ma
  `kiem_lease` bo qua tep da xoa => PR bot chi xoa lease di duong nhanh XANH. Nguoi doc theo cau khai se ky vong DO. Do:
  `GITHUB_ACTOR='claude[bot]'` => xoa `[]`, sua lease that `rc=8 … CHAN [4]`-duong.
DA THU VA: co — chi sua cau khai (khong doi hanh vi):
```diff
-    giữ chốt thẩm quyền theo `GITHUB_ACTOR`, nên PR hồ sơ chạm `ops/leases/` do bot (actor khác chủ kho) đẩy
-    sẽ ĐỎ ở đường nhanh (`CHAN [4]`) trong khi đường đầy đủ không chạy chốt này. Đỏ ở đây là fail-close đúng
+    giữ chốt thẩm quyền theo `GITHUB_ACTOR`, nên PR hồ sơ THÊM/SỬA lease dưới `ops/leases/` do bot (actor khác chủ
+    kho) đẩy sẽ ĐỎ ở đường nhanh (`CHAN [4]`) trong khi đường đầy đủ không chạy chốt này (XOÁ lease thì `kiem_lease`
+    bỏ qua tệp đã xoá, nên không đỏ). Đỏ ở đây là fail-close đúng
```
  Chot tuy chon: mot ca khoa "tep lease da xoa khong goi validator" da co (t21 phan `da-xoa`) — chi can dan chieu trong cau khai.
DA THU NGHIEM: lenh HUONG 8. Khong can dot bien (sua van ban).
DO TIN: cao.

## DAC TA (khong bat executor sua)
- M1 "ba cham" khong xac dinh duy nhat khi >1 merge-base; phep va de nghi o tren nam trong M4, khong can revision.
- NT11: G5 (`ops/cong_cu_test.py`, khai 46,5/52 phut) khong nam trong danh sach bo va Q6 cam mo rong => "ngan hon ro ret" phu thuoc #668;
  can do lai tren PR that SAU #668.

## GIOI HAN / CHUA DO DUOC
GitHub that (merge ref, base.sha cu, fork, required check `skipped`), Windows, thoi gian runner, 552 ref, served model/effort cua luot nay.
Dot bien `tukiem_so_sai` cua toi khong chay rieng (trung dot bien co san da bi giet). Lan cho tien trinh nen `bmwwk2o2t` bi ngat do het han
cho (khong anh huong ket qua — cac log da doc truc tiep).

## TEP
- `rv8/out/VERDICT.md` (tep nay) · `rv8/out/HINT.patch` (chi `ops/ci_duong_nhanh_test.py`; `patch -p0 --fuzz=0` tu goc cay => ap sach, `cmp` khop ban da do;
  sha256 b2f4fbce9e8647ff656fdb21c987f9a2be7d5073e24d0cd80c43afa58f6932b4)
- Phep do: `rv8/tmp/cc.sh` `gl.sh` `gl2.sh` `ga.sh` `nt9.py` `mut8.py` `lam_hint.py` `chi_test.py`; ban ap hint `rv8/tmp/hint8`; log `rv8/tmp/*.log`, `rv8/tmp/mut8/*.log`.

TONG: P0=0 P1=0 P2=1 P3=3
So lop: 4 con mo (1 P2, 3 P3); 5 lop luot 7 da va that (xem DOI CHIEU).
