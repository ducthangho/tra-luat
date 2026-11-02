verdict: changes_requested
reviewed_sha: fc610c2ee2a4ab424a566bb9b267ccc676be6340
Reviewed commit: fc610c2ee2a4ab424a566bb9b267ccc676be6340

luot: 9 (packet #674 CI-DUONG-NHANH-HO-SO, dac ta r2 sha256 b6e719c9…da57 — da kiem khop; PROMPT.md sha256 84fc367c…b47b — khop)

TONG: P0=0 P1=0 P2=0 P3=3 — 3 lop con mo
Reviewer: Claude Opus 5.5 subagent, cung ho executor => advisory_review (khong cross_approved). Model/effort duoc phuc vu: KHONG DO DUOC.

## SO DO NEN (tu chay tren cay-kho @fc610c2, Linux, git 2.43.0, shellcheck /usr/bin co mat)
- `python3 -B ops/ci_duong_nhanh_test.py`: `CA: 77/77 dat · 0 do · 0 hong` · `DOT BIEN: 189/189 bi giet dung ly do` · KIEM KE 49+16+3+9=77 · 2+65+80+42=189 · `TU KIEM PHAN HANG: DAT (5 mau rc, 3 dot bien that)` · `TONG: DAT` rc=0 (51,7s)
- `python3 -B .claude/dev/ci_dang_ky_test.py`: `ĐĂNG KÝ: 23/23` · `PHẢN CHỨNG: 938/938 đỏ đúng` · `TỔNG: ĐẠT` rc=0
- `actionlint .github/workflows/ci.yml` rc=0 · ruff 0.16.9 F hai tep moi: `All checks passed!`
- `goi/do_lai_so.py`: 345; 63; 8 · 113 tep lease, dat 107, truot 6 (clone nay 45 ref) · `goi/kiem_ke.py`: 77 ca / 189 dot bien, ba ca du lieu loi=[] 5,2s

## DOI CHIEU LUOT TRUOC (4 lop luot 8, reviewed 57b6578 -> nay fc610c2)
| lop (slug) | hang luot 8 | trang thai o fc610c2 | bang chung TU DO |
|---|---|---|---|
| `phan-loai-ba-cham-mu-voi-nhieu-merge-base` | P2 | **DA VA THAT** (ca hai cua: nhieu merge-base + goc doi ten; them hop voi `merge-tree`) | t11b/t11c DAT trong 77/77; dot bien RIENG cua toi (`tmp/mut9/run1.log`): `mb_cho_nhieu_dong` (regex nhan nhieu dong) => `[DO] t11b hai merge-base: phai la day_du`; `merge_tree_cho_rc1` => `[DO] t11c merge-tree xung dot rc=1`; `merge_tree_dung_merge_base` (dau,dau) => `[DO] t11`; `diff_cay_hai_cham_dau` => `[DO] t11` |
| `kiem-re-cua-fail-close-chua-co-ca` | P3 | **DA VA THAT** cho hai cua luot 8 (symlink hop le/moi duoi; `--check` moi duoi) + cua moi tu khai (nhi phan, t20s) | ba dot bien SONG cua luot 8 (`loai_tep_chi_chan_treo`, `loai_tep_chi_md`, `diff_check_chi_md`) nay nam trong DOT_BIEN va bi giet (189/189); toi: `numstat_chi_dong_dau` => `[DO] t20s` |
| `kiem-re-bi-cau-hinh-boi-du-lieu-ho-so` | P3 | **VA HO** — `--attr-source=<goc>` cho `--check` la quyet dinh DUNG (khong chan `.gitattributes`: master co dung 3 tep `-whitespace` duoi `ops/reviews/`, da dem; `-whitespace` van de `--check` bat dau xung dot, da do `tmp/h1/ws.sh` rc=2) va co rang (`attr_source_dau` => `[DO] t20p`). NHUNG `kiem_nhi_phan` MOI THEM goi `git diff --numstat` KHONG `--attr-source` => thuoc tinh cua PR lai cau hinh duoc chot kiem ho so (finding duoi) | `tmp/h1/attr.sh '* diff'` |
| `kiem-re-phu-thuoc-actor-su-kien` | P3 | **DA VA THAT** (cau khai D2 nay noi ro THEM/SUA do, XOA khong do — khop hanh vi do o luot 8) | doc dong 65-68 `ops/ci_duong_nhanh.py` |

## BANG SAN (dang ghi tang dan)
HUONG 1: thuoc tinh `diff` cua PR bien tep NUL thanh "van ban" cho `kiem_nhi_phan` (cua con lai cua lop `kiem-re-bi-cau-hinh-boi-du-lieu-ho-so`)
  gia thuyet : `kiem_nhi_phan` goi `git diff --numstat` KHONG `--attr-source` => doc `.gitattributes` cua cay lam viec (cay PR); `* diff` ep tep co NUL la van ban cho numstat, trong khi `--check` (doc thuoc tinh GOC) van coi no la nhi phan va BO QUA => dau xung dot trong tep co NUL lot ca hai chot
  lenh       : bash rv9/tmp/h1/attr.sh '' ; bash rv9/tmp/h1/attr.sh '* diff' ; bash rv9/tmp/h1/attr.sh 'x.md diff'
  output     : khong attr: numstat `-^I-^Iops/land/x.md` · check rc=0 · `kiem_nhi_phan ["tep ho so nhi phan ...'ops/land/x.md'"]` (DO dung)
               `* diff`   : numstat `6^I0^Iops/land/x.md` · check rc=0 · phan_loai duong_nhanh · kiem_diff_check [] · kiem_nhi_phan [] · kiem_yaml [] · kiem_loai_tep []
               `x.md diff`: y het (kiem_nhi_phan [])
  ket luan   : LOI -> `kiem-re-bi-cau-hinh-boi-du-lieu-ho-so` [P3] (va ho cua luot 8; cau khai D1 "du lieu ho so khong cau hinh duoc chot kiem ho so" SAI cho kiem_nhi_phan)

HUONG 2: rang cua cac chot MOI o bo phan loai (dot bien RIENG cua reviewer, ban sao `rv9/tmp/mut9/<ten>/ops/ci_duong_nhanh.py`, chay moi ca t* (tru t9x can cay day du) bang `--mot-ca`)
  lenh       : python3 -B rv9/tmp/mut9/mut9.py (log rv9/tmp/mut9/run1.log)
  output     : nen_khong_doi SONG 49/49 (doi chung) · mb_cho_nhieu_dong GIET `t11b hai merge-base` · merge_tree_cho_rc1 GIET `t11c merge-tree xung dot rc=1` ·
               merge_tree_dung_merge_base GIET t11 · diff_cay_hai_cham_dau GIET t11 · numstat_chi_dong_dau GIET t20s · attr_source_dau GIET t20p ·
               diff_cay_co_renames GIET t11c (qua do gia dinh tuyen theo argv — ve NGU NGHIA dot bien nay TUONG DUONG vi hop voi ba cham --no-renames da phu; khong phai loi) ·
               numstat_co_attr_source_goc SONG 49/49 (= chinh ban va cua HUONG 1: khong ca nao phan biet => xac nhan lo chot)
  ket luan   : KHONG PHAI LOI (tru dieu HUONG 1 da ghi)

HUONG 3: dot bien tang YAML (NT6 va cac `if:` sai lop) — rv9/tmp/mut9y/mut9y.py, ca y*/k* (k01/k02 do SAN trong cay rut gon cua harness — tao tac, bo qua; doi chung `nen`)
  output     : phan_loai_bo_if_su_kien GIET y01 y12 y13 · output_bo_gac_su_kien GIET y02 y13 · output_mac_dinh_nhanh GIET y02 y13 · golden_luon_bo (`${{ false }}`) GIET y03 y04 y12 y13 ·
               golden_eq_day_du GIET y03 y04 y12 y13 · kiem_re_always (`always() && ...`) GIET y04 y08 y12 y13 · kiem_re_coe (continue-on-error Windows) GIET y08 y10 y13 ·
               selftest_windows GIET y09 y12 y13 · kiem_re_bo_set_e (`|| true`) GIET y08 y14 · kiem_re_goc_la_dau GIET y08 y13 · checkout_chuan_bi_nong GIET y01 y13 ·
               gate_job_if_cancelled (`!cancelled()` cap job) GIET y06 y11 y13
  ket luan   : KHONG PHAI LOI

HUONG 4: `merge-tree(base.sha, head)` co khop merge ref THAT cua GitHub khong
  gia thuyet : phan loai mo phong merge tu `pull_request.base.sha`; commit GitHub that su test (`github.sha`, checkout cua moi job) co cha 1 = dau nhanh dich LUC DUNG merge. Neu hai thu lech (base.sha cu hon) va nhanh dich da doi ten tep ho so ra vung ma, merge ref sua ma trong khi phan loai ra duong_nhanh
  lenh       : bash rv9/tmp/h4/stale.sh
  output     : `merge ref ^1=6a69d78 (B1) ; base.sha gia dinh cu = 705999f` · `merge that doi so voi ^1: scripts/f.py` ·
               `goc=705999f ('duong_nhanh', ...)` · `goc=6a69d78 ('day_du', "... 'scripts/f.py'")`
  ket luan   : LOI (co che do duoc tai cho; tan suat tren GitHub KHONG DO DUOC) -> `phan-loai-khong-neo-merge-ref-that` [P3]. merge-tree == ort cua GitHub: KHONG DO DUOC offline (docstring da khai trung thuc). Git cu thieu `merge-tree --write-tree` (<2.38) / `--attr-source` => rc!=0 => day_du / kiem-re DO: huong fail-close, khong mo (phien ban git cua runner KHONG DO DUOC)

HUONG 5: nghiem thu 8, 9 tu do (clone rv9/tmp/nt89 @fc610c2)
  output     : NT8 chen `# chu thich ${{ }}` vao than run kiem-re => actionlint rc=1 `ci.yml:549:48: unexpected end of input ... [expression]`; ban goc rc=0.
               NT9a go muc DA_NOI => `ĐỎ: test sống chưa đăng ký: ops/ci_duong_nhanh_test.py` · `ĐĂNG KÝ: 23/22` · `TỔNG: ĐỎ` rc=1
               NT9b go `run: python ops/ci_duong_nhanh_test.py` => `ĐỎ: CI không gọi mục đăng ký: ops/ci_duong_nhanh_test.py` rc=1 · numstat `1 0`
  ket luan   : KHONG PHAI LOI

HUONG 6: cau khai ve `skipped` — hai noi trong packet noi NGUOC nhau
  lenh       : grep -n skipped ops/ci_duong_nhanh_test.py .github/workflows/ci.yml
  output     : ci.yml:58 `chuan-bi do thi job phu thuoc skipped ... context bat buoc (ubuntu-latest) khong duoc tao ⇒ PR bi CHAN` (khai DO 4 luot that)
               ci_duong_nhanh_test.py:1099 `chuan-bi do => ba job bat buoc skipped (GitHub tinh la dat)`; goi/DO_LAI.md cung con dong "`skipped` ... tinh la dat ... la co so cua continue-on-error"
  ket luan   : LOI (cau khai) -> `cau-khai-skipped-nguoc-phep-do` [P3]

Pham vi: `git diff 1741e0a fc610c2` co them `ops/lease_publish_test.py` + `ops/specs/t131-deadline-dem-spawn.md` — blob o HEAD TRUNG blob o master 89fc4fa
(`694cca5b…`, `1a99adbf…`), 89fc4fa va 1741e0a deu la to tien cua HEAD => phan them do la CUA MASTER (#680), khong phai cua packet.
Chi ghi trong `rv9/out` va `rv9/tmp` (ngoai le: mot lan ghi nham `/tmp/null` tu chuyen huong stdout, da xoa ngay). Khong mang, khong GitHub, khong Windows,
khong cham `cay-kho` (moi dot bien tren ban sao `rv9/tmp/...`). Khong con tien trinh nen.

## BANG LOP
| slug | bieu hien | hang cao nhat con mo | phuong an va chung | phep kiem dong lop |
|---|---|---|---|---|
| `kiem-re-bi-cau-hinh-boi-du-lieu-ho-so` (luot 8, VA HO) | moi lenh git cua kiem-re doc THUOC TINH phai doc tu cay GOC. Duong vao: (a) `--check` — DA dong bang `--attr-source`; (b) `--numstat` cua `kiem_nhi_phan` MOI — MO (`* diff` ep tep NUL thanh van ban); (c) `doc_diff`/`merge-tree` `--name-only` — thuoc tinh khong doi TAP DUONG DAN (merge driver chi doi noi dung/xung dot; xung dot => day_du), khong mo; (d) kiem_yaml/kiem_loai_tep doc tep truc tiep — `eol` da xet luot 8, khong mo | P3 | `--attr-source=<goc>` cho MOI lenh `git diff` cua kiem-re (hien chi con numstat) | t20t (hai do sau, chung minh fixture: numstat cay-lam-viec coi la van ban + `--check` bo qua) + dot bien `nhi_phan_bo_attr_source` |
| `phan-loai-khong-neo-merge-ref-that` (MOI) | goc cua phan loai la `pull_request.base.sha`; `merge-tree` MO PHONG merge tu goc do; commit GitHub that su test (`github.sha`, cai moi job checkout) khong duoc doi chieu. Base.sha cu hon cha-1 cua merge ref + nhanh dich doi ten ho so ra vung ma => duong_nhanh cho merge sua ma | P3 | dua `github.sha` vao env hai buoc; hop them `diff goc -> github.sha` (bien co ma hong / git loi => KHONG DO DUOC) | t11d (fixture git that co 2 chot chung minh) + dot bien `merge_ref_bo_hop`, `merge_ref_lac_dang_bo_qua`; y01/y08/y13 khoa env moi |
| `cau-khai-skipped-nguoc-phep-do` (MOI) | thong diep y01 (va dong DO_LAI) khai "`chuan-bi` do => job bat buoc `skipped` (GitHub tinh la dat)"; ci.yml:58 khai DO 4 luot that: context bat buoc khong duoc tao, PR bi CHAN | P3 | sua thong diep cho khop phep do da ghi trong ci.yml | doc lai; grep `skipped` |

## BANG DO (khang dinh -> dao khai -> do duoc -> khop?)
| khang dinh | nguon | do duoc | khop? |
|---|---|---|---|
| 345 / 63 / 8, ~13% | docstring D1 | `do_lai_so.py`: 345; 63; 8 (8/63 = 12,7%) | co |
| 6/113 (clone mot ref) | docstring D2 | 113 tep, truot 6 (clone nay 45 ref); 0/113 tren 552 ref KHONG DO DUOC | co (phan do duoc) |
| "master co ba tep `.gitattributes` duoi `ops/reviews/`" | docstring D1 | `git ls-files` => 3 (pr667, pr670, land-doc-receipt-thu-hoi-c1a1a), ca ba `-whitespace` | co |
| "master: 0 tep nhi phan duoi allowlist" | D1, `kiem_nhi_phan` | numstat cay rong -> 89fc4fa va -> HEAD tren 4 tien to: 0 (ca co `--attr-source`) | co |
| "`-whitespace` khong tat bao dau xung dot" (ham y cua quyet dinh khong chan .gitattributes) | D1 | `tmp/h1/ws.sh`: `leftover conflict marker` x3, rc=2 | co |
| "du lieu ho so khong cau hinh duoc chot kiem ho so" | D1 | SAI cho `kiem_nhi_phan` (HUONG 1) | **khong** |
| "`.gitattributes` do PR them (`conflict-marker-size`, `binary`, `-diff`) KHONG tat duoc bao dau xung dot" | `kiem_diff_check` | dung cho `--check`; nhung `diff` (set) tat duoc chot BU `kiem_nhi_phan` => tong the kiem-re van lot (HUONG 1) | mot phan |
| "merge-tree cung thuat toan voi GitHub — theo tai lieu, chua tu do" | D (doc_diff) | KHONG DO DUOC offline; khai trung thuc; nhung GOC cua mo phong khong neo merge ref that (HUONG 4) | khai co / neo khong |
| "`chuan-bi` do => skipped (GitHub tinh la dat)" | test y01 dong 1099 | nguoc ci.yml:58 (khai do 4 luot that) | **khong** (tu mau thuan) |
| ba ca du lieu ~6 giay | `kiem_ca_du_lieu` | 5,2s | co |
| 23/23, 938/938; numstat `1 0` | DO_LAI / NT9 | 23/23 · 938/938 · `1 0` | co |
| G5 46,5/52 phut; 360 phut mac dinh; "4 luot that" | ci.yml / DO_LAI | KHONG DO DUOC (khong mang) | — |

## NGHIEM THU (r2) — bang chung tu chay
| # | ket qua | bang chung |
|---|---|---|
| 1-5 | dat | suite `CA 77/77 · DOT BIEN 189/189 · TONG: DAT`; dot bien rieng (HUONG 2) |
| 6, 7 | dat | ca y01..y16; 12 dot bien YAML rieng cua toi deu bi giet dung ca (HUONG 3) |
| 8 | dat | actionlint rc=0 (shellcheck co mat); chen `${{ }}` => rc=1 (HUONG 5) |
| 9 | dat | 23/23, 938/938; numstat `1 0`; hai dot bien NT9 DO dung thong diep (HUONG 5) |
| 10 | dat | `== tl selftest 1715/1715 ==` rc=0 (clone sach `rv9/tmp/nt` @fc610c2, core.abbrev 7); `scripts/` khong doi so 1741e0a, ruff F tl.py 12 (= nen CLAUDE.md) => delta 0 |
| 11 | chua_do_duoc | can PR that; executor KHONG khai dat (dung) |
| M1/M4 | LECH nhe o duong vao merge ref (P3 duoi) | HUONG 4 |

## DOT BIEN SONG SOT
- `numstat_co_attr_source_goc` (HUONG 2): song vi CHINH la ban va cua finding 1 — khong ca nao phan biet. Tren ban hint, dot bien nguoc (`nhi_phan_bo_attr_source`) bi giet boi t20t.
- `diff_cay_co_renames`: bi giet qua do gia dinh tuyen argv, ve ngu nghia TUONG DUONG (hop voi ba cham `--no-renames`) — khong phai loi.

## FINDINGS

### kiem-re-bi-cau-hinh-boi-du-lieu-ho-so  [P3]  `kiem_nhi_phan` doc thuoc tinh cua cay PR: `* diff` lam tep co NUL (chua dau xung dot) qua ca hai chot
TEP/DONG: `ops/ci_duong_nhanh.py` `kiem_nhi_phan` dong 258-272 (loi goi `git diff --numstat` dong 263); cau khai D1 dong 53-57.
VAN DE: Luot 8 chot `--check` bang `--attr-source=<goc>` (dung, co rang). Nhung chot BU moi cho tep nhi phan (`kiem_nhi_phan`) goi `--numstat`
  KHONG `--attr-source`, nen doc `.gitattributes` cua cay lam viec (= merge ref cua PR). PR them `ops/land/.gitattributes` = `* diff` (thuoc tinh `diff`
  SET ep git coi tep la van ban ke ca co NUL) + tep co NUL chua dau xung dot: numstat bao `6 0` (khong phai `- -`) => `kiem_nhi_phan` = [];
  `--check` doc thuoc tinh GOC => tep la nhi phan => bo qua => rc=0. Ket qua: kiem-re DAT (`t20t` tren HEAD: `rc=0 ... dung duong nhanh`). Hai chot
  doc thuoc tinh tu HAI cay khac nhau — chinh su khong nhat quan do la cua vao. Cau D1 "du lieu ho so khong cau hinh duoc chot kiem ho so" sai.
  P3 (khong P2) vi cung muc voi luot 8: can PR co y dat `.gitattributes` + tep NUL; docstring module da khai allowlist khong chan tac gia co y;
  push master chay day du sau merge. Chieu nguoc (`binary`/`-diff` cua PR tren tep van ban => numstat `- -` => DO oan) la fail-close, ban va cung het.
DA THU VA: co — san pham:
```diff
diff --git ops/ci_duong_nhanh.py ops/ci_duong_nhanh.py
index 2ce03801..4d373ab6 100644
--- ops/ci_duong_nhanh.py
+++ ops/ci_duong_nhanh.py
@@ -257,10 +272,13 @@ def kiem_diff_check(env=os.environ, chay=subprocess.run, kho=ROOT) -> list[str]:
 
 def kiem_nhi_phan(env=os.environ, chay=subprocess.run, kho=ROOT) -> list[str]:
     """`git diff --check` BỎ QUA tệp git coi là nhị phân (NUL trong nội dung) — dấu xung đột trong đó lọt êm (đo
-    30-09-2026). Hồ sơ không cần nhị phân (master: 0 tệp dưới allowlist) ⇒ tệp nhị phân đổi = KHÔNG ĐO ĐƯỢC ⇒ ĐỎ."""
+    30-09-2026). Hồ sơ không cần nhị phân (master: 0 tệp dưới allowlist) ⇒ tệp nhị phân đổi = KHÔNG ĐO ĐƯỢC ⇒ ĐỎ.
+    Thuộc tính đọc từ cây GỐC như `kiem_diff_check`: `* diff` do PR mang vào ép tệp có NUL thành "văn bản" cho numstat
+    trong khi `--check` (thuộc tính gốc) vẫn bỏ qua nó (cross-review lượt 9)."""
     goc, dau = env.get(BIEN_GOC) or "", env.get(BIEN_DAU) or ""
     try:
-        ns = chay(["git", "diff", "--numstat", "-z", "--no-renames", f"{goc}...{dau}"], cwd=kho, capture_output=True)
+        ns = chay(["git", "--attr-source=" + goc, "diff", "--numstat", "-z", "--no-renames", f"{goc}...{dau}"],
+                  cwd=kho, capture_output=True)
     except Exception as e:
         return [f"KHONG DO DUOC: git diff --numstat nem {type(e).__name__}"]
     ra_ns = getattr(ns, "stdout", None)
```
  Test (trong `out/HINT.patch`): ca `t20t_kiem_re_thuoc_tinh_diff_cua_pr_khong_bien_nhi_phan_thanh_van_ban` — hai do sau (`ops/land` `* diff`,
  `ops/reviews/a/b` `x.md diff`), moi cai hai chot chung minh fixture (numstat cay-lam-viec KHONG `- -`; `--check` thuoc tinh goc rc=0) roi doi kiem-re rc=1
  + `nhi phan` + ten tep; dot bien `nhi_phan_bo_attr_source` dich t20t. Neo cua dot bien co san `diff_check_bo_attr_source` phai doi (chuoi
  `"--attr-source=" + goc, ` nay xuat hien 2 lan => `HONG RuntimeError: neo ... thay 2` — da do; patch doi sang neo `["git", "--attr-source=" + goc, "-c", CAU_HINH_WHITESPACE`).
DA THU NGHIEM: HEAD: `tmp/h1/attr.sh` (HUONG 1); chi ap HINT.patch len clone HEAD: `DO:t20t...: ops/land: tep co NUL phai DO du PR mang diff: rc=0`. Ban ap du
  (`rv9/tmp/hint9` = san pham + test): `CA: 79/79 dat` · `DOT BIEN: 192/192 bi giet dung ly do` · `TU KIEM PHAN HANG: DAT` · `TONG: DAT` rc=0; ruff F sach;
  actionlint rc=0; ci_dang_ky 23/23 · 938/938.
DO TIN: cao (co che, do tren git that); thap (tan suat).

### phan-loai-khong-neo-merge-ref-that  [P3]  Phan loai mo phong merge tu `base.sha`, khong doi chieu commit merge GitHub THAT SU test (`github.sha`)
TEP/DONG: `ops/ci_duong_nhanh.py` `doc_diff` dong 151-154, `doc_diff_merge` dong 157-180; `.github/workflows/ci.yml` env buoc `phan loai diff` (dong 73-76) va buoc kiem-re (dong 545-548).
VAN DE: Luot 9 them `merge-tree --write-tree goc dau` de bat duong vao "goc doi ten ho so ra vung ma". Nhung `goc` = `pull_request.base.sha` cua su kien,
  con cai GitHub test (checkout cua moi job) la `github.sha` — merge commit ma cha 1 la dau nhanh dich LUC GitHub dung no. Hai thu co trung nhau o moi su
  kien hay khong la KHONG DO DUOC offline (dac ta `chua_do_duoc` 2/3 cung chua do). Neu lech (base.sha cu hon) va nhanh dich da doi ten tep ho so ra
  vung ma trong khoang do, merge that SUA ma trong khi phan loai ra `duong_nhanh` — da do co che tren git that (HUONG 4: goc cu => duong_nhanh;
  cha-1 cua merge => day_du `scripts/f.py`). Commit merge THAT da co san trong checkout (`fetch-depth: 0`), nen thay vi TIN "merge-tree tuong duong
  GitHub theo tai lieu" co the DO thang: hop them `diff goc -> github.sha`. Khi base.sha cu va nhanh dich co them ma, tap nay lam PR ra `day_du` —
  bao thu dung chieu (M4), va chi xay ra dung trong ca lech ma finding nay noi toi.
  Neu executor chon khong va: sua cau khai (docstring doc_diff_merge + GIOI HAN) de noi ro GOC mo phong la base.sha cua su kien, khong phai cha-1 cua merge ref.
DA THU VA: co — san pham (hai tep):
```diff
diff --git .github/workflows/ci.yml .github/workflows/ci.yml
index 06acadae..40034014 100644
--- .github/workflows/ci.yml
+++ .github/workflows/ci.yml
@@ -74,6 +74,7 @@ jobs:
           CI_DUONG_NHANH_SU_KIEN: ${{ github.event_name }}
           CI_DUONG_NHANH_GOC: ${{ github.event.pull_request.base.sha }}
           CI_DUONG_NHANH_DAU: ${{ github.event.pull_request.head.sha }}
+          CI_DUONG_NHANH_MERGE: ${{ github.sha }}
         run: python3 ops/ci_duong_nhanh.py
       - name: che do (push / workflow_dispatch luon day du)
         if: ${{ github.event_name != 'pull_request' }}
@@ -546,6 +547,7 @@ jobs:
           CI_DUONG_NHANH_SU_KIEN: ${{ github.event_name }}
           CI_DUONG_NHANH_GOC: ${{ github.event.pull_request.base.sha }}
           CI_DUONG_NHANH_DAU: ${{ github.event.pull_request.head.sha }}
+          CI_DUONG_NHANH_MERGE: ${{ github.sha }}
         run: |
           set -euo pipefail
           python .claude/dev/packet_loop.py doctrine-scan --root .
--- ops/ci_duong_nhanh.py
+++ ops/ci_duong_nhanh.py
@@ -80,6 +80,7 @@ from pathlib import Path
 ROOT = Path(__file__).resolve().parents[1]
 DAY_DU, DUONG_NHANH = "day_du", "duong_nhanh"
 BIEN_SU_KIEN, BIEN_GOC, BIEN_DAU = "CI_DUONG_NHANH_SU_KIEN", "CI_DUONG_NHANH_GOC", "CI_DUONG_NHANH_DAU"
+BIEN_MERGE = "CI_DUONG_NHANH_MERGE"   # github.sha: commit merge THAT ma moi job checkout (cross-review luot 9)
 ALLOWLIST_TIEN_TO = ("ops/land/", "ops/leases/", "ops/reviews/", "ops/specs/")
 MAU_SHA = re.compile(r"[0-9a-f]{40}")
 CAU_HINH_WHITESPACE = "core.whitespace=-blank-at-eol,-blank-at-eof,-space-before-tab"
@@ -151,7 +152,17 @@ def doc_diff(env=os.environ, chay=subprocess.run, kho=ROOT):
     khi_merge = doc_diff_merge(goc, dau, chay, kho)
     if khi_merge is None:
         return None
-    return ba_cham | khi_merge
+    # merge-tree mo phong merge tu base.sha; commit GitHub THAT SU test (github.sha) co the dung dau nhanh dich MOI hon
+    # (base.sha cu) => doi them diff goc -> merge that. Co bien ma hong / git loi => KHONG DO DUOC.
+    hop = env.get(BIEN_MERGE) or ""
+    khi_merge_that = set()
+    if hop:
+        if not (MAU_SHA.fullmatch(hop) and hop.strip("0")):
+            return None
+        khi_merge_that = doc_diff_cay(goc, hop, chay, kho)
+        if khi_merge_that is None:
+            return None
+    return ba_cham | khi_merge | khi_merge_that
 
 
 def doc_diff_merge(goc, dau, chay=subprocess.run, kho=ROOT):
@@ -167,7 +178,11 @@ def doc_diff_merge(goc, dau, chay=subprocess.run, kho=ROOT):
     if getattr(mt, "returncode", None) != 0 or not isinstance(ra_mt, (bytes, bytearray)) \
             or not re.fullmatch(rb"[0-9a-f]{40}\n", bytes(ra_mt)):
         return None
-    cay = bytes(ra_mt).decode("ascii").strip()
+    return doc_diff_cay(goc, bytes(ra_mt).decode("ascii").strip(), chay, kho)
+
+
+def doc_diff_cay(goc, cay, chay=subprocess.run, kho=ROOT):
+    """Tap duong dan doi `goc -> cay` (--no-renames), hoac None = KHONG DO DUOC."""
     try:
         dt = chay(["git", "diff", "--no-renames", "--name-only", "-z", goc, cay], cwd=kho, capture_output=True)
     except Exception:

```
  (Hunk `kiem_nhi_phan` nam o finding truoc; ban day du ca hai finding: `rv9/tmp/hint9_sanpham.diff`.)
  Test (trong `out/HINT.patch`): ca `t11d_merge_ref_that_dung_base_moi_hon_day_du` — fixture git that (goc cu B0, nhanh dich doi ten `ops/land/f.md`->
  `scripts/f.py`, merge ref tren B1) voi hai chot chung minh (merge that sua `scripts/f.py`; KHONG co bien merge thi goc cu cho duong_nhanh), doi `day_du`
  + `scripts/f.py` trong ly do; do gia: merge ref hop le + khong doi them => duong_nhanh (doi chung), `xyz`/toan 0/HOA => day_du. Dot bien
  `merge_ref_bo_hop`, `merge_ref_lac_dang_bo_qua` dich t11d; dot bien co san `merge_that_bo_hop` doi neo theo dong return moi. y01/y08/y13 khoa them
  `CI_DUONG_NHANH_MERGE: ${{ github.sha }}` o hai buoc.
DA THU NGHIEM: `tmp/h4/stale.sh` (HUONG 4); chi ap HINT.patch len HEAD: `DO:t11d...: merge ref that sua ma: phai day_du, duoc 'duong_nhanh'`; ban ap du 79/79 · 192/192 · TONG: DAT.
  KHONG DO DUOC: GitHub co bao gio phat su kien voi base.sha != cha-1 cua github.sha; parents cua refs/pull/N/merge la (base, head) theo tai lieu.
DO TIN: cao (co che); thap (tan suat tren GitHub — tien de chua do).

### cau-khai-skipped-nguoc-phep-do  [P3]  Thong diep y01 khai "`skipped` (GitHub tinh la dat)", nguoc voi phep do ghi trong ci.yml
TEP/DONG: `ops/ci_duong_nhanh_test.py` dong 1098-1099 (thong diep `bang` cua y01); doi chieu `.github/workflows/ci.yml` dong 55-59. (Dong tuong tu trong
  `rv9/goi/DO_LAI.md` la tai lieu cua goi review, ngoai cay — chi bao de phien dieu phoi sua.)
VAN DE: ci.yml khai DO 4 luot that (Issue #674 comment 5889459132): `chuan-bi` do => context bat buoc `(ubuntu-latest)` KHONG duoc tao => PR bi CHAN.
  Thong diep y01 noi nguoc: "ba job bat buoc `skipped` (GitHub tinh la dat)" — tuc `chuan-bi` do la FAIL-OPEN. Hai cau trong cung packet, ve dung co so
  an toan cua `continue-on-error`, tu mau thuan; nguoi sua sau doc thong diep test (thu hien ra dung luc test do) se hieu sai he qua cua viec go chot.
  Khong doi hanh vi, nen P3.
DA THU VA: co — trong `out/HINT.patch` (tep test):
```diff
-         "buoc phan loai phai co `continue-on-error: true`: chuan-bi do => ba job bat buoc `skipped` (GitHub tinh la dat)")
+         "buoc phan loai phai co `continue-on-error: true`: chuan-bi do => ba context bat buoc KHONG duoc tao, PR bi CHAN (xem ci.yml)")
```
  Chot: khong can dot bien (van ban). Phep kiem dong lop: `grep -n "tinh la dat" ops/ci_duong_nhanh_test.py` => rong.
DA THU NGHIEM: grep (HUONG 6); ban hint: y01 DAT, 79/79.
DO TIN: cao (mau thuan van ban); hanh vi GitHub that KHONG DO DUOC.

## DAC TA (khong bat executor sua)
- M1 chi noi "diff base...head"; khong noi goc la base.sha cua su kien hay cha-1 cua merge ref. Hai thu co the lech (chua do) — xem finding 2.
- NT11: G5 khong nam trong danh sach bo (Q6) => "ngan hon ro ret" phu thuoc #668 (giu nhan xet luot 8).

## GIOI HAN / CHUA DO DUOC
GitHub that (merge ref, base.sha cu, fork, required check khi `chuan-bi` do), phien ban git cua runner (can >=2.38 cho `merge-tree --write-tree`, co
`--attr-source` — thieu thi rc!=0 => day_du / kiem-re DO, tuc fail-close), Windows, thoi gian runner, 552 ref, served model/effort cua luot nay.

## TEP
- `rv9/out/VERDICT.md` (tep nay) · `rv9/out/HINT.patch` (chi `ops/ci_duong_nhanh_test.py`; `patch -p0 --fuzz=0` tu goc cay => ap sach, `cmp` khop ban da do;
  sha256 92e122269a3b2ace8fd21e4816b6be275c136be1a8e41642a3dde336489d31d2) · ban san pham day du `rv9/tmp/hint9_sanpham.diff` · cay da ap `rv9/tmp/hint9`
- Phep do: `rv9/tmp/h1/attr.sh` `h1/ws.sh` `h4/stale.sh` `mut9/mut9.py` (+ `run1.log`) `mut9y/mut9y.py` (+ `run1.log`); log `rv9/tmp/nen_suite.log` `nen_dk.log` `nt_selftest.log` `hint9_suite.log`.

TONG: P0=0 P1=0 P2=0 P3=3
So lop: 3 con mo (0 P2, 3 P3); luot 8: 3 lop DA VA THAT, 1 lop VA HO (chinh la lop mo dau tien).
