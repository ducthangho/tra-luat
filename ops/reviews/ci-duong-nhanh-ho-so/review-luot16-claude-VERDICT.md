verdict: changes_requested
reviewed_sha: 91cd2f78942aec423c1a003c65e81b474bfc7fc9
Reviewed commit: 91cd2f78942aec423c1a003c65e81b474bfc7fc9

> luot 16 (packet #674, dac ta r2 sha256 b6e719c9…da57 KHOP; r1 e6949841…c64c KHOP). TRANG THAI: XONG 11 huong + doi chieu.
> Ket luan: 2 finding P3 (`bang-do-thieu-neo-va-thieu-kiem-ke` con 5 duong vao trong kho + bang DO_LAI ngoai kho; lop MOI
> `khang-dinh-dinh-tinh-rong-hon-phep-do`). San pham va ci.yml KHONG doi hanh vi (AST/byte). Nguong chu kho 0/0/0 => KHONG approve.
> Reviewer: Claude Opus 5.5, CUNG HO voi executor => `advisory_review`, KHONG phai cross_approved; packet `sensitive` van can Codex
> `cross_approved` hoac `human_audited` o cong land. Model/effort thuc chay: KHONG DO DUOC.

## DOI CHIEU LUOT TRUOC
Moi dong co phep do CUA TOI (dot bien chu KHAC harness / do lai so hang), chay tren ban sao hoac cay mini; cay-kho khong bi sua.

| luot · finding | hang cu | trang thai | bang chung TU DO |
|---|---|---|---|
| luot 15 · `bang-do-thieu-neo-va-thieu-kiem-ke` (docstring D2 "6/113 … 0/113" khong neo commit; bang DO_LAI troi 3 so) | P3 | **VA HO** (duong duoc chi da dong THAT; lop con 5 duong vao trong kho + 1 ngoai kho) **+ VA SINH LOI MOI nho** | Dong THAT: 12/12 cau co so do trong docstring/chu thich hai tep co neo; 6/6 neo SHA ton tai (`rev-parse --verify`); so hang do lai KHOP: 345 (toan bo, -n 400 khong cham tran)/63/8, 1991/0 nhi phan, 3 `.gitattributes`, 113 + 6 truot (1741e0a, 1 ref), 119 + 6 truot cung 6 tep CHAN 8 (3569472, 1 ref), 38/12/3 vs 35/12/3/3 (7b8c856), ~7 s (7,08–7,51 s o day) (HUONG 2, 3). t98b: 13/13 dot bien harness chet dung chot con (HUONG 7); khong false-red tren 3.11/3.12/3.13 (HUONG 4). CON MO: luong tu "do chinh PR ho so them vao" = 2/3 (PR #666 la PR MA); t20p "master co ba tep" (so bang chu, neo `master`); thong bao `bang` t20d "8/63" khong neo; gan nguon 6/113 cho reviewer luot 1; 3 nhanh bo quet khong rang (B1/B2/B3 SONG); DO_LAI.md (ngoai kho) van "AL_VER 4", "938/938", "6/113", numstat 1741e0a "mong 1 0" (HUONG 2, 3, 5, 6). Ban va SINH: cau D2 moi "moi REF cuc bo" rong hon ma (tag khong quet — do) -> lop moi. |
| luot 15 · 8 lop DONG (`kiem-mode-git-chot-khong-rang`, `buoc-bi-bo-doc-ca-cay-khong-chi-ba-ca`, `kiem-re-cua-fail-close-chua-co-ca`, `kiem-re-bi-cau-hinh-boi-du-lieu-ho-so`, `phan-loai-khong-neo-merge-ref-that`, `cau-khai-skipped-nguoc-phep-do`, `dependency-failure-skips-required-checks`, `kiem-re-phu-thuoc-actor-su-kien`) | DONG | van DONG | AST san pham (bo 17 docstring) 3569472 == HEAD (dump `cf27fd5f9f81`); `ci.yml`, `ci_dang_ky_test.py` khong doi tu 3569472; AST tep test chi doi `DOT_BIEN` + chot ha tang t20zh (THEM phan ra 7/13/7/6 — siet) + nut t98b; suite 97/97 · 320/320 (gom 20 `mode_git_lat_o_*` + X1 `mien_tru_M`, 11 dot bien symlink cua 8b); nghiem thu 1-7 do lai bang dot bien cua toi (HUONG 8). Khong bang chung moi => khong mo lai. |
| luot 14 · X1 (`kiem-mode-git-chot-khong-rang`) · luot 8b · F1/F2 | DA VA THAT (luot 15) | van DA VA THAT | cac dot bien tuong ung nam trong 320/320 `bi giet dung ly do`; san pham khong doi hanh vi |

## BANG LOP
| slug | bieu hien (duong vao da liet ke) | hang cao nhat con mo | phuong an va chung | phep kiem dong lop |
|---|---|---|---|---|
| `bang-do-thieu-neo-va-thieu-kiem-ke` | (1) LUONG TU sai du co neo: docstring D1 san pham + t20p "do chinh PR ho so them vao" — do 2/3 (#667, #670 `duong_nhanh`; #666 `day_du`, 3 tep `.claude/dev/**`). (2) So do ve KHO viet bang CHU, neo `master`: `ops/ci_duong_nhanh_test.py:907` "master co ba tep" — trai quy uoc executor tu khai, lot t98b. (3) So do trong CHUOI thong bao `bang(...)`: `:855` "(do 8/63 lan merge)" khong neo; `:1682` "(do 4 luot that, xem ci.yml)" neo gian tiep — duong NAY KHONG nam trong gioi han tu khai. (4) Gan NGUON do: D2 "reviewer luot 1 do … 6/113" — 6/113 la so executor, luot 1 (1687c69) do 0/113 tren 552 ref va ghi "khong tai lap". (5) Phep kiem dong lop t98b co 3 nhanh KHONG RANG: neo phai co chu so; `;` la ranh gioi cau; gach `·` la ranh gioi doan (dot bien noi long SONG ca suite). (6) Ngoai kho (phien dieu phoi): `goi/DO_LAI.md` 4 dong cu. Da quet va SACH: ten ca/ten dot bien, chuoi tran, so bi danh sach cho phep loai, chu thich ci.yml do packet them. Tu khai, hien sach, KHONG tinh: neo gia (6/6 SHA ton tai) | **P3** | `out/HINT.patch` (tep test: +7 mau tu kiem; quet tu-so truoc danh tu kho; quet so sau dau hieu do trong thong bao `bang`; sua t20p/t20d/y01; +8 dot bien; doi dot bien D2 theo van ban moi) + khoi diff san pham (D1 luong tu, D2 nguon) + sua DO_LAI (phien dieu phoi) | tren ban sao: 97/97 · 328/328 · TU KIEM DAT · TONG DAT; 8 dot bien moi chet dung chot con; dot bien cua toi A5b/A7b/B1/B2/B3 tu SONG -> GIET (HUONG 10) |
| `khang-dinh-dinh-tinh-rong-hon-phep-do` (MOI) | (1) D2 "checkout cua Actions chi co ref cua PR, khong co cac nhanh `ops/**`" — khai nhu su that; chua ai do; kho TU ghi la CHUA DO (`ops/reviews/thu-hoi-lease-va-cap-lai-spec/spec-r1.md` muc 6, `spec-r2.md` muc 5); trai tai lieu `actions/checkout` cho `fetch-depth: 0` (gate-ops, `ci.yml:622-625`). (2) "moi REF cuc bo" rong hon ma: `_cac_ref_cuc_bo` chi `refs/heads` + `refs/remotes`, tag KHONG quet (do). Da ra moi khang dinh ve GitHub/runner khac trong docstring san pham: deu da gan "KHONG DO DUOC"/"chua do"/"theo tai lieu" | **P3** | sua cau D2 (khoi diff trong finding) | phep do: bia mo chi tren tag -> CHAN 8; tren `refs/remotes/pull/1/merge` hoac `refs/remotes/origin/ops/x` -> DAT; chi tren dia -> CHAN 8 (HUONG 3, 11). Hanh vi runner: nhan CHUA DO cho toi khi do tren PR that (nghiem thu 11) |
| 8 lop cu (xem DOI CHIEU) | — | DONG | — | suite 97/97 · 320/320 |

## SO DO NEN (@91cd2f7, Linux, Python 3.11.15, git 2.43.0, actionlint 1.7.7 + shellcheck 0.9.0, ruff 0.16.9, TMPDIR=$R/tmp)
- `python3 -B ops/ci_duong_nhanh_test.py`: `CA: 97/97 dat · 0 do · 0 hong` · `DOT BIEN: 320/320 bi giet dung ly do` ·
  `KIEM KE: ca hanh_vi=68 + cau_truc_yaml=16 + so_dang_ky=3 + tu_kiem=10 = 97 · dot bien ci_dang_ky_test.py=2 + ci.yml=74 +
  ci_duong_nhanh.py=194 + ci_duong_nhanh_test.py=50 = 320` · `TU KIEM PHAN HANG: DAT (5 mau rc, 3 dot bien that)` · `TONG: DAT` ·
  rc=0 · real 1m49s. `git status --short` truoc/sau: rong.
  Doi chieu luot 15 (96 / 307; san pham 189, test 42): +1 ca (t98b, nhom tu_kiem 9->10); +13 dot bien (san pham +5, test +8) — KHOP loi khai commit.
- `python3 -B .claude/dev/ci_dang_ky_test.py`: `ĐĂNG KÝ: 23/23` · `PHẢN CHỨNG: 1025/1025 đỏ đúng` · `TỔNG: ĐẠT` · rc=0
- `actionlint .github/workflows/ci.yml` rc=0 (shellcheck 0.9.0 co mat) · ruff F hai tep moi: `All checks passed!` · tl.py 12 F821 (= nen CLAUDE.md; scripts/ khong doi)
- AST san pham (bo 17 docstring) 3569472 vs 91cd2f7: GIONG HET (sha dump cf27fd5f9f81 ca hai) => khong doi hanh vi. ci.yml, ci_dang_ky_test.py: khong doi tu 3569472.

## BANG SAN
HUONG 1: so nen cua bo test + loi khai commit 91cd2f7 ("CA 97/97, DOT BIEN 320/320, registry 23/23 + 1025/1025, ruff F delta 0")
  gia thuyet : neu loi khai rong hon phep do thi so in ra khac / kiem ke lech so hang
  lenh       : cd cay-kho && python3 -B ops/ci_duong_nhanh_test.py ; python3 -B .claude/dev/ci_dang_ky_test.py ; actionlint ; ruff ;
               so AST bo docstring (tmp/ast/so_ast.py) 3569472 vs HEAD
  output     : xem SO DO NEN
  ket luan   : KHONG PHAI LOI


HUONG 2: tung so hang CO NEO (12 cau ma chinh bo quet t98b coi la "co so do") — do lai bang phep do THAT, khong chi quan he
  gia thuyet : neu t98b chi do su CO MAT cua neo thi mot so hang co neo van co the sai/troi; neu bo quet bo sot cau co so do thi con duong vao
  lenh       : tmp/neo/liet_ke.py (exec tep test, dung cau_tai_lieu/so_do_trong_cau/MAU_NEO_SO_DO cua CHINH no) -> 12 cau, 0 khong neo;
               git rev-parse --verify <neo>^{commit} tren kho.git cho 6 neo SHA; git log --merges --first-parent 1741e0a (khong -n);
               goi/do_lai_so.py; git ls-tree -r 3569472 -- <4 tien to> | wc -l; numstat cay-rong->3569472 (co/khong --attr-source);
               noi dung + commit them 3 tep .gitattributes; merge master dua chung vao; `python3 -B ops/ci_duong_nhanh.py` (san pham)
               voi env GOC=m^1 DAU=m^2 MERGE=m cho ba merge ay
  output     : neo 1741e0a/20ec8d5/3569472cb9/7b8c856/680301261e TON TAI (ca 6) ·
               merge first-parent toi 1741e0a: 345 (khong -n) = 345 (-n 400) — 345/345 la merge 2 cha, khong cham tran => "TOAN BO 345" DUNG ·
               do_lai_so: 345 / 63 / 8 ; 8/63 = 12,7% (~13%) DUNG ·
               tep duoi allowlist tai 3569472: 1991 ; nhi phan 0 (co va khong --attr-source) => 0/1991 DUNG ·
               .gitattributes duoi allowlist tai 3569472: 3, ca 3 duoi ops/reviews/, ca 3 `-whitespace` => DUNG ·
               "do chinh PR ho so them vao": bookkeeping-650-pr667 <- Merge PR #667 (20 tep, 0 ngoai) -> san pham `duong_nhanh`;
               bookkeeping-650-pr670 <- Merge PR #670 (28 tep, 0 ngoai) -> `duong_nhanh`; land-doc-receipt-thu-hoi-c1a1a <- Merge PR #666
               (f8a7829cc4): `DAY_DU vi diff co 3 tep ngoai allowlist: '.claude/dev/ci_dang_ky_test.py', '.claude/dev/doc_receipt_thu_hoi.py',
               '.claude/dev/doc_receipt_thu_hoi_test.py'` -> `day_du`
  ket luan   : LOI (P3) — loi khai dinh luong "3 tep ... do chinh PR ho so them vao" (doc la ca 3) do duoc 2/3; tep thu ba vao qua PR MA #666.
               Finding `bang-do-thieu-neo-va-thieu-kiem-ke` (bieu hien moi: so hang dung, LUONG TU sai). Cac so con lai cua nhom nay KHOP.

HUONG 3: so lease cua D2 (113 / 6/113 / 552 / 119 / 6/119 / 529) + cau D2 moi ve pham vi ref — do bang kho tam DUNG mot ref
  gia thuyet : neu "6/119 tren mot ref, dung 6 tep cu, CHAN [8]" hay "113 tai 1741e0a" sai thi so khai lech; neu `_quet_lease_toan_kho`
               khong doc "moi REF cuc bo" (nhu docstring khai) thi cau D2 rong hon ma
  lenh       : (tmp/lease1) git archive <C> | tar -x ; git init ; alternates -> kho.git ; update-ref refs/heads/chi-mot <C> (KHONG checkout) ;
               tmp/lease1/do.py = lp.kiem(..., bo_qua_han=True) tung tep ops/leases/*.y*ml ; roi tren ban sao m2_tag dung commit tong hop X
               (them lease cu `thu-hoi-lease-exec-1-codex-20260828` mang `da_bi_thay_the: bo-ghi-nguoc-exec-1-claude-20260829`), dat X
               lan luot o refs/tags/, refs/remotes/pull/1/merge, refs/remotes/origin/ops/x ; doc luot1-verdict.md (reviewed 1687c69)
  output     : 1741e0a, 1 ref: `tong 113 dat 107 truot 6` (6 tep, ca 6 CHAN 8 bia mo) · 3569472, 1 ref: `tong 119 dat 113 truot 6` — DUNG 6
               tep ay, ca 6 CHAN 8 => KHOP. cay-kho (47 ref) cung 6 truot; 529/552 ref: KHONG DO DUOC (mirror 45 ref).
               X chi tren TAG: `CHAN 8` · X duoi refs/remotes/pull/1/merge: `DAT` · X duoi refs/remotes/origin/ops/x: `DAT`
               => `_cac_ref_cuc_bo` chi doc refs/heads + refs/remotes (bo tag, bo */HEAD): "moi REF cuc bo" rong hon ma (tag khong duoc quet).
               luot 1 (reviewed 1687c69, cay ops/leases == 1741e0a: `git diff --stat` rong): do `113 dat 113 truot 0` tren 552 ref va ghi
               "6/113 ... Khong tai lap" — tuc 6/113 la so CUA EXECUTOR (toi tai lap duoc bang 1 ref), khong phai "reviewer luot 1 do".
               gate-ops (noi chay kiem-re) checkout `actions/checkout@v4` + `fetch-depth: 0` (ci.yml:622-625). Kho TU ghi cau hoi
               "fetch-depth: 0 nap du refs/remotes/origin/*?" la CHUA DO (ops/reviews/thu-hoi-lease-va-cap-lai-spec/spec-r1.md muc 6,
               spec-r2.md muc 5); tai lieu actions/checkout: "0 indicates all history for all branches and tags" (KHONG DO DUOC o day:
               khong mang, khong co ban actions/checkout cuc bo — `grep -r getRefSpecForAllHistory /` rong).
  ket luan   : LOI (P3) — cau D2 moi khang dinh nhu SU THAT "checkout cua Actions chi co ref cua PR, khong co cac nhanh ops/**" (chua ai do,
               nguoc tai lieu checkout voi fetch-depth 0; phep do cua toi cho thay NEU runner co refs/remotes/origin/* thi bia mo DAT,
               tuc gioi han D2 khong xay ra tren gate-ops) + "moi REF cuc bo" rong hon ma (tag bi bo) + gan nguon 6/113 cho reviewer luot 1.
               So hang 113/119/6 KHOP.

HUONG 4: t98b co false-red / qua chat theo phien ban Python (CI ghim 3.12) khong
  gia thuyet : neu tokenize/ast khac giua 3.11 (may dev) va 3.12 (CI) thi t98b DO oan tren CI hoac quet khac cau
  lenh       : python3.11|3.12|3.13 -B ops/ci_duong_nhanh_test.py --mot-ca t98b_… ; tmp/neo/liet_ke.py duoi ca ba ban, cmp JSON
  output     : rc=0 ca ba; `cau co so do: 12 | khong neo: 0` ca ba; JSON 3.11 == 3.12 == 3.13 (cmp byte)
  ket luan   : KHONG PHAI LOI (khong false-red theo phien ban; chi quet hai tep cua packet nen PR khac khong lam vo t98b)

HUONG 5: duong vao CON LAI cua lop (ngoai docstring/chu thich bang chu so) — so viet bang CHU, so trong CHUOI thong bao, so trong TEN ca,
         neo GIA, chuoi tran khong phai docstring
  gia thuyet : neu t98b chi quet chu so trong docstring/chu thich thi mot so do ve KHO viet bang chu hoac nam trong chuoi `bang(...)` se troi
               ma ca van xanh
  lenh       : tmp/neo/loai.py (moi chu so bi loai + ly do) ; tmp/neo/chu.py, chu2.py (tu-so + danh tu / tu-so trong cau nhac master|kho|do) ;
               tmp/neo/chuoi.py (hang chuoi khong phai docstring co so + ngu canh kho) ; quet ten ham/ten dot bien ; dem chuoi tran
  output     : so bi loai: 0 so do bi giau (dinh danh/neo/ngay/danh so/mode) · ten ca/ten dot bien: chi `755` (mode) va `t82` (ten ca) ·
               chuoi tran khong phai docstring: 0 ca hai tep · SO BANG CHU ve KHO, khong neo: ops/ci_duong_nhanh_test.py:907 (docstring t20p)
               "master co ba tep `-whitespace` duoi `ops/reviews/` do PR ho so them" — neo `master` (ref troi), luong tu do duoc 2/3 (HUONG 2) ·
               SO TRONG CHUOI: :855 (t20d) `bang(..., f"... (do 8/63 lan merge): ...")` KHONG neo; :1682 (y01) "(do 4 luot that, xem ci.yml)"
               neo gian tiep (khong co id comment) · neo cua 12 cau: ca 6 SHA ton tai (HUONG 2)
  ket luan   : LOI (P3) — hai duong vao song: (a) so do ve KHO viet bang chu (trai quy uoc executor tu khai "so do ve KHO viet bang chu so")
               o docstring test t20p; (b) so do trong chuoi thong bao `bang(...)` (t20d `8/63` khong neo) — duong (b) KHONG nam trong gioi han
               tu khai cua t98b.

HUONG 6: rang cua t98b — dot bien CUA TOI (chu KHAC 13 dot bien harness), cay mini tmp/m16/<ten>, --nguon-test + --mot-ca t98b
  gia thuyet : neu mot nhanh cua bo quet khong co mau tu kiem rieng thi dot bien NOI LONG nhanh do song toan suite
  lenh       : R=$R python3 -B tmp/m16/mut_t98b.py (CTRL + A1..A13 + B1..B10) ; mau truc tiep goc-vs-dot-bien cho B1/B2/B3
  output     : CTRL rc=0 · GIET dung ca: A1 (neo->master), A2 (docstring ham them so), A3 (chu thich giua ham), A4 (neo sang CAU khac, tach `.`),
               A8 (neo chi chu hex `defaced`), A9 (docstring ham LONG), A13 (chu thich cuoi dong ma), B4 (bo ngay ISO), B7 (neo ca nguon),
               B9 (quet chuoi rong -> chot ha tang bat) ·
               SONG: A5 so bang chu khong neo (gioi han TU KHAI a) · A6 neo gia `abc1234` (gioi han TU KHAI b) · A7 so trong chuoi thong bao
               (KHONG tu khai) · B1 bo dieu kien "co chu so" cua neo · B2 MAU_TACH_CAU bo `;` · B3 MAU_TACH_DOAN bo gach `·` · B5 khong gop
               khoi chu thich (SIET CHAT, vo hai) · B6 bo loai "so dinh chu" (SIET CHAT, vo hai) · B8 bo chot ha tang (tuong duong tren du lieu
               hien tai; B9 chung minh chot co rang) · B10 = B8+B9 (mong song).
               Mau truc tiep: B1 `Kho co 119 lease (xem effaced).` goc bao=True, dot bien bao=False · B2 `Do tai 3569472cb9; kho co 119 lease.`
               goc True / dot bien False · B3 `Do tai 3569472cb9:\n  · kho co 119 lease` goc True / dot bien False => ba dot bien NOI LONG that.
  ket luan   : LOI (P3) — ba nhanh cua bo quet (doi chu so trong neo, `;` la ranh gioi cau, `·` la ranh gioi doan) khong co mau tu kiem nao:
               go chung, t98b va ca suite van xanh (dung hinh dang "chot khong rang" — lop `bang-do-thieu-neo-va-thieu-kiem-ke`, phep kiem dong lop).

HUONG 7: 13 dot bien moi cua harness — giet o DUNG chot con cua t98b (tin dung gia muc chot con)
  lenh       : python3 -B tmp/m16/harness13.py (dung_cay_tam + chay_con + phan_hang cua chinh bo test)
  output     : 13/13 GIET: 7 dot bien tai lieu -> chot CAY ("KHONG co neo trong cung cau", dung tep/dong/cau bi doi) · 5 dot bien bo quet
               -> mau tu kiem tuong ung (docstring ham/class, chu thich, neo o cau khac, so tran, so thuan) · bo_tep_test -> chot ha tang.
               So AST tep test (bo docstring) 3569472 vs HEAD: chi doi `DOT_BIEN`, `t20zh` (chot ha tang bang) + 10 nut moi cua t98b.
  ket luan   : KHONG PHAI LOI

HUONG 8: nghiem thu 1-7 cua SPEC-r2 do DOC LAP (dot bien chu cua toi, cay tam cua chinh bo test)
  lenh       : python3 -B tmp/m16/nghiem_thu.py
  output     : CTRL 8 ca rc=0 · N1 (toan allowlist -> DAY_DU) -> t01 GIET · N2 (khop them `scripts/` qua tham so startswith) -> t02 GIET ·
               N3 (`if doi is None and False` => None roi xuong nhanh rong) -> t05, t06 GIET · N4 (goi `git rev-parse` truoc kiem su kien) ->
               t03 GIET `[['git', 'rev-parse', 'HEAD']]` · N5 (them `.github/`) -> t08 GIET · N6a (`if: github.event_name != 'push'`) -> y01, y13
               GIET · N6b (golden-test `if: ${{ false }}`) -> y03, y04, y12, y13 GIET · N7 (`paths: ['**']` duoi pull_request) -> y05 GIET
  ket luan   : KHONG PHAI LOI

HUONG 9: nghiem thu 8-10 + pham vi diff (phan them so voi 1741e0a co DUNG la cua master)
  lenh       : (tmp/nt8) chen dong chu thich chua `${{ }}` (dau `$` dung bang chr(36) SAU phan tich) vao than run buoc kiem-re, actionlint goc/dot bien ;
               (tmp/nt9a, nt9b, nt9m = git archive HEAD / 20ec8d5) go dong DA_NOI / doi `run: python ops/ci_duong_nhanh_test.py` ;
               git diff --numstat 20ec8d5|1741e0a HEAD -- .claude/dev/ci_dang_ky_test.py ; (tmp/nt10 = cp -a, core.abbrev 7) python3 scripts/tl.py --selftest ;
               vong so blob HEAD:<f> vs 20ec8d5:<f> cho moi tep cua `git diff 1741e0a HEAD` ngoai 4 tep packet
  output     : actionlint goc rc=0 · dot bien rc=1 `unexpected end of input while parsing ... [expression]` ·
               nt9a `ĐỎ: test sống chưa đăng ký: ops/ci_duong_nhanh_test.py` `ĐĂNG KÝ: 23/22` rc=1 · nt9b `ĐỎ: CI không gọi mục đăng ký:
               ops/ci_duong_nhanh_test.py` rc=1 · nen master 20ec8d5 `ĐĂNG KÝ: 22/22` `PHẢN CHỨNG: 1025/1025` ĐẠT -> HEAD 23/23, 1025/1025 ·
               numstat so master `1 0` (so 1741e0a `172 6` — 171 dong cua #668) · `== tl selftest 1715/1715 ==` rc=0 (4m35s) ·
               ruff F tl.py 12 F821 (= nen; tl.py khong doi) · 20ec8d5..HEAD dung 4 tep packet; 127 tep ngoai packet lech blob voi master: 0 ·
               doctrine-scan `sạch — đã quét 10 tệp` rc=0
  ket luan   : KHONG PHAI LOI

HUONG 10: HINT cua luot nay co rang va khong lam vo cong (tu kiem chinh HINT truoc khi giao)
  gia thuyet : neu HINT them chot ma chot khong do dung ly do, hoac lam suite/registry/ruff do, thi HINT la no moi
  lenh       : (tmp/hint2 = cp -a cay-kho) python3 -B tmp/lam_hint.py tmp/hint2 ca_hai ; python3 -B ops/ci_duong_nhanh_test.py ; registry ; ruff ;
               doctrine-scan ; tmp/m16/harness13.py (21 dot bien dich t98b) ; THAT_DIR=tmp/hint2 tmp/m16/mut_t98b.py (A5b, A7b, B1, B2, B3, A6, B5, B6) ;
               (tmp/hint_chk = git archive HEAD) patch -p0 --fuzz=0 < out/HINT.patch ; patch -p0 --fuzz=0 < tmp/hint_sanpham.diff ; cmp
  output     : `CA: 97/97` · `DOT BIEN: 328/328 bi giet dung ly do` · `KIEM KE: ... ops/ci_duong_nhanh_test.py=58 = 328` · `TU KIEM PHAN HANG: DAT` ·
               `TONG: DAT` rc=0 (1m53s) · registry 23/23 · 1025/1025 ĐẠT · ruff `All checks passed!` · doctrine-scan sach ·
               8 dot bien moi + D2 cap nhat: moi cai chet o DUNG chot con (5 nhanh bo quet -> dung mau tu kiem moi; t20p `['ba tep']`,
               t20d `thong bao ['8/63']`) · dot bien cua toi: A5b `['ba tệp']` GIET, A7b `thong bao ['9/70']` GIET, B1/B2/B3 GIET (truoc HINT: SONG);
               A6 (neo gia) van SONG — gioi han tu khai (b), khong doi; B5/B6 SONG (SIET CHAT, vo hai) · patch ap sach, cmp == ban da thu ·
               sha256 out/HINT.patch 6f9bc81e22fcd2e840f53a6489557fcf3ce05bbb0ef99355763f8b89067ce4c2
  ket luan   : KHONG PHAI LOI (HINT do duoc, da thu tren ban sao; chua chay tren cay that)

HUONG 11: khang dinh dinh tinh MOI cua ban va (khong phai so) — do bang hanh vi
  lenh       : (tmp/lease1/m3_wt) bia mo chi tren DIA (tep chua commit), 1 ref ; (tmp/gl1) git update-index --cacheinfo 160000 + commit-tree,
               git diff --numstat / --raw
  output     : bia mo chi tren dia -> `CHAN 8` => "khong doc cay lam viec" DUNG · gitlink them moi: numstat `1	0	ops/specs/con`, raw `:000000 160000 ... A`
               => "numstat dem duoc dong (khong ra `-`)" (docstring kiem_mode_git, t20v) DUNG
  ket luan   : KHONG PHAI LOI

## BANG DO (khang dinh -> nguon khai -> do duoc -> khop?)
| khang dinh | nguon khai | do duoc (lenh o BANG SAN) | khop? |
|---|---|---|---|
| CA 97/97, DOT BIEN 320/320, TU KIEM DAT, TONG DAT | commit 91cd2f7 | 97/97 · 320/320 · DAT (5 mau rc, 3 dot bien that) · DAT, rc=0 (HUONG 1) | co |
| registry 23/23 + 1025/1025 | commit | 23/23 · 1025/1025; nen master 20ec8d5 22/22 · 1025/1025 (HUONG 9) | co |
| ruff F delta 0, doctrine-scan rc=0 | commit | tl.py 12 F821 (= nen; tl.py khong doi); 2 tep moi sach; doctrine-scan `sạch` rc=0 | co |
| "13 dot bien" cho t98b | commit | 13 dot bien dich t98b (harness13) | co |
| "chi docstring san pham doi, hanh vi khong doi" | commit | AST bo docstring giong het (`cf27fd5f9f81`) | co |
| lease 119; "6 truot o pham vi mot ref" | commit + D2 | 119 tep; 1 ref: 113 dat / 6 truot, dung 6 tep cu, ca 6 CHAN 8 (HUONG 3) | co |
| "0/119 o 529 ref cuc bo" | commit + D2 | KHONG DO DUOC (mirror 45 ref; cay-kho 47 ref -> van 6 truot) | — |
| "0/1991 nhi phan" tai 3569472cb9 | commit + docstring D1, kiem_nhi_phan, t20s | 1991 tep; 0 nhi phan (co/khong `--attr-source`) | co |
| 345 / 63 / 8 tai 1741e0a; "TOAN BO 345 … khong cham tran" | commit + D1 | 345 (khong -n) = 345 (-n 400), 345/345 hai cha; 63; 8 | co |
| ~13% (8/63) | D1 | 12,7% | co |
| 3 `.gitattributes` duoi allowlist, ca 3 duoi `ops/reviews/`, `-whitespace` | D1 | 3 / 3 / ca 3 `-whitespace` | co |
| "… do chinh PR ho so them vao" (ca 3) | D1 + t20p | **2/3**: #667, #670 `duong_nhanh`; #666 `day_du` (`.claude/dev/ci_dang_ky_test.py`, `doc_receipt_thu_hoi.py`, `doc_receipt_thu_hoi_test.py`) | **KHONG** |
| "master co ba tep `-whitespace`" | t20p (so bang chu) | 3 tai HEAD/master — so dung hom nay, nhung neo `master` (troi) va lot t98b | so co / neo **KHONG** |
| "(do 8/63 lan merge)" | thong bao t20d | 8/63 dung TAI 1741e0a; chuoi khong neo | so co / neo **KHONG** |
| "reviewer luot 1 do tai 1741e0a … 6/113 … 552 ref 0/113" | D2 | 113 (1741e0a); 6/113 tai lap bang 1 ref; luot 1 reviewed 1687c69 (cay ops/leases == 1741e0a), do 0/113 tren 552 ref, ghi 6/113 "khong tai lap" | so co / nguon **KHONG** |
| "bia mo doc moi REF cuc bo …, khong doc cay lam viec" | D2 + commit | doc refs/heads + refs/remotes (ca `refs/remotes/pull/*`); tag KHONG; dia KHONG | **mot phan** (tag) |
| "checkout cua Actions chi co ref cua PR, khong co cac nhanh ops/**" | D2 | KHONG DO DUOC; kho ghi CHUA DO; tai lieu `actions/checkout` fetch-depth 0 = moi nhanh + tag | **KHONG** (khai nhu su that) |
| "~7 giay … 4 vCPU, Python 3.11: 6,6-6,8 giay" | docstring kiem_ca_du_lieu | 7,51 / 7,08 / 7,08 s (4 CPU, 3.11.15) | co (phu thuoc may) |
| "khai 38/12/3, do 35/12/3/3 tai 7b8c856" | docstring t96 | 53 ca: t=38, y=12, k=3; tach t97/t98/t99 -> 35/12/3/3 | co |
| bang 20 o = 7 + 13; 13 = 7 + 6 | t20zh | chot ha tang moi `(7, 13, 7, 6)`, suite xanh | co |
| gitlink: numstat dem duoc dong (khong `-`) | docstring kiem_mode_git, t20v | `1	0	ops/specs/con` (HUONG 11) | co |
| `pull_request.base.sha`/`head.sha` luon khop MAU_SHA | D (chua tu do) | KHONG DO DUOC (khong mang) — da gan nhan | — |
| 52 phut (run 36518707072); 360 phut; "4 luot that" (comment 5889459132) | D1 / t20zh docstring / ci.yml + y01 | KHONG DO DUOC (khong mang) | — |
| DO_LAI "AL_VER: 4 dong" | goi/DO_LAI.md | HEAD 5, master 20ec8d5 5, 1741e0a 4 (delta so master 0) | **KHONG** |
| DO_LAI "938/938" | goi/DO_LAI.md | 1025/1025 (HEAD va master) | **KHONG** |
| DO_LAI "lease 6/113 vs 0/113" | goi/DO_LAI.md | 119 tep (6/119 tren 1 ref) | **KHONG** |
| DO_LAI "numstat 1741e0a HEAD (mong 1 0)" | goi/DO_LAI.md | `172 6` so 1741e0a; `1 0` so master 20ec8d5 | **KHONG** |
| head la commit co chu ky | PROMPT | khoi `gpgsig` SSH co mat; xac minh: KHONG DO DUOC (khong allowedSignersFile) | mot phan |

## NGHIEM THU (SPEC-r2)
| # | ket qua | bang chung TU CHAY |
|---|---|---|
| 1 | dat | N1 (toan allowlist -> DAY_DU) -> t01 GIET (HUONG 8) |
| 2 | dat | N2 (khop them `scripts/` qua tham so `startswith`) -> t02 GIET; harness `noi_allowlist_them_scripts` trong 320/320 |
| 3 | dat | N3 (`if doi is None and False`: KHONG DO DUOC roi xuong nhanh rong) -> t05, t06 GIET |
| 4 | dat | N4 (goi `git rev-parse` truoc khi kiem su kien) -> t03 GIET `[['git', 'rev-parse', 'HEAD']]` |
| 5 | dat | N5 (them `.github/`) -> t08 GIET |
| 6 | dat | N6a (`if: github.event_name != 'push'` o buoc phan loai) -> y01, y13; N6b (golden-test `if: ${{ false }}`) -> y03, y04, y12, y13; + 74 dot bien ci.yml trong 320/320 |
| 7 | dat | N7 (`paths: ['**']` duoi pull_request) -> y05 GIET |
| 8 | dat | actionlint rc=0 (shellcheck 0.9.0); `${{ }}` rong trong chu thich than run -> rc=1 `[expression]` (HUONG 9) |
| 9 | dat | nen master 22/22 -> HEAD 23/23 (1025/1025 ca hai); go DA_NOI -> `test sống chưa đăng ký` (23/22); go loi goi CI -> `CI không gọi mục đăng ký`; numstat so master `1 0` |
| 10 | dat | `== tl selftest 1715/1715 ==` rc=0 (ban sao, core.abbrev 7); ruff F tl.py 12 = nen, 2 tep moi sach |
| 11 | chua_do_duoc | can PR that; commit KHONG khai dat |

## FINDINGS

### bang-do-thieu-neo-va-thieu-kiem-ke  [P3]  Lop con 5 duong vao trong kho: luong tu sai du co neo (2/3), so ve kho viet bang chu, so trong thong bao `bang`, gan sai nguon, 3 nhanh t98b khong rang (+ DO_LAI ngoai kho)
TEP/DONG: `ops/ci_duong_nhanh.py:72-73` (D1 `.gitattributes`), `:78-82` (D2 nguon 6/113); `ops/ci_duong_nhanh_test.py:907` (t20p), `:855` (t20d),
  `:1682` (y01), `:2350-2455` (hang so + bo quet + ca t98b); `goi/DO_LAI.md` (ngoai kho).
VAN DE: Ban va luot 15 dong DUNG duong da chi (12/12 cau co so do deu co neo, 6/6 neo ton tai, moi so hang do lai KHOP — HUONG 2, 3),
  nhung lop con mo theo nam duong ma t98b khong canh hoac canh khong rang:
  (1) LUONG TU sai du co neo — D1 khai 3 `.gitattributes` "do chinh PR ho so them vao"; do: 2/3 (`bookkeeping-650-pr667` <- PR #667,
      `bookkeeping-650-pr670` <- PR #670 deu `duong_nhanh`), `land-doc-receipt-thu-hoi-c1a1a` vao qua PR #666 (f8a7829cc4) ma chinh san
      pham phan loai `DAY_DU vi diff co 3 tep ngoai allowlist`. t98b chi do neo CO MAT, nen so hang/luong tu sai van xanh.
  (2) So do ve KHO viet bang CHU, neo `master` — docstring t20p:907 "master co ba tep `-whitespace` duoi `ops/reviews/` do PR ho so them":
      dung cau ma D1 vua duoc neo ("tai 3569472cb9 co 3 tep"), nhung ban trong tep test viet "ba" nen lot t98b; trai chinh quy uoc t98b tu
      khai ("so do ve KHO viet bang chu so"); va mang cung luong tu sai (1).
  (3) So do trong CHUOI thong bao `bang(...)` — t20d:855 `f"... (do 8/63 lan merge): ..."` (8/63 chi dung tai 1741e0a, khong neo); y01:1682
      "(do 4 luot that, xem ci.yml)" (neo gian tiep). Duong nay KHONG nam trong gioi han tu khai cua t98b (chi khai (a) so bang chu, (b) neo gia).
  (4) Gan NGUON do — D2 "reviewer luot 1 do tai 1741e0a (113 tep lease) — clone chi-master 6/113 truot …, ban sao du 552 ref 0/113": luot 1
      (reviewed 1687c69, cay `ops/leases` trung 1741e0a) chi do 0/113 tren 552 ref va ghi ro "6/113 … Khong tai lap"; 6/113 la so CUA EXECUTOR
      (toi tai lap duoc bang kho dung mot ref). So dung, nguon sai.
  (5) Phep kiem dong lop co 3 nhanh KHONG RANG — bo dieu kien "neo co chu so" (B1), bo `;` khoi `MAU_TACH_CAU` (B2), bo gach `·` khoi
      `MAU_TACH_DOAN` (B3): ca ba la dot bien NOI LONG that (mau truc tiep: goc bao, dot bien im) va SONG toan t98b vi khong mau tu kiem nao
      ghim chung (HUONG 6) — nguyen tac "moi duong mot mau tu kiem va mot dot bien rieng" cua chinh t98b chi phu cac duong no liet ke
      (co "so thuan bi nham la neo", KHONG co doi xung "tu hex toan chu bi nham la neo"), khong phu ba nhanh thiet ke nay.
  (6) Ngoai kho (phien dieu phoi, khong phai executor): `goi/DO_LAI.md` van ghi "AL_VER: 4 dong" (do 5), "938/938" (do 1025), "lease 6/113 vs
      0/113" (kho 119), "numstat 1741e0a HEAD (mong 1 0)" (do 172 6; so master 1 0) — dung ba so luot 15 da chi, CHUA VA.
  Khong anh huong hanh vi gate (san pham khong doi AST); la lo cua phep KHAI dinh luong => P3.
DA THU VA: co —
  (a) TEP TEST — `out/HINT.patch` (nhan nguyen van "chua chay tren cay that — executor tu ap, tu do, tu chiu trach nhiem commit"):
      sua t20p (chu so + neo 3569472cb9 + luong tu 2/3, 1/3), t20d (them `tai 1741e0a`), y01 (`Issue #674 comment 5889459132`); t98b them
      `MAU_SO_CHU_KHO` (tu-so dung ngay truoc danh tu thuc the kho: tep/lease/merge/PR/ref/nhanh; mien `ca`/`cả` = "ca hai", dem cau truc),
      `MAU_SO_DO_THONG_BAO` + `cau_thong_bao` (so dung sau dau hieu do viet thuong trong doi so thu hai cua `bang(...)`; so cau truc trong thong
      bao — gia tri fetch-depth, ma rc, kich thuoc bang — khong bi bat), 7 mau tu kiem moi. CHOT RIENG cho tung duong vao (moi cai mot dot bien,
      deu dich t98b, da do chet o DUNG chot con): (1)+(2) `docstring_test_so_chu_khong_neo` (t20p ve "master co ba tep") -> chot cay `['ba tep']`;
      (2) `bo_quet_so_bo_so_chu`, `bo_quet_so_chu_bo_mien_ca` -> mau tu kiem; (3) `thong_diep_bang_mat_neo` -> chot cay `thong bao ['8/63']`,
      `bo_quet_thong_diep_bang` -> mau tu kiem; (5) `bo_quet_so_neo_khong_doi_chu_so`, `bo_quet_so_tach_cau_bo_cham_phay`,
      `bo_quet_so_tach_doan_bo_gach` -> ba mau tu kiem moi. Dot bien harness `docstring_ti_le_D2_mat_neo` doi neo theo van ban moi cua D2.
      HINT.patch va khoi diff san pham duoi day PHAI ap CUNG nhau (dot bien D2 neo vao van ban moi).
  (b) SAN PHAM (khoi diff, executor tu ap; khong nam trong HINT.patch) — (1) luong tu D1 va (4) nguon D2; cung khoi sua cau D2 cua finding sau:
```diff
--- ops/ci_duong_nhanh.py
+++ ops/ci_duong_nhanh.py
@@ -70,16 +70,19 @@
     đã chịu thuộc tính của PR (`eol`/`text`/`working-tree-encoding`/`ident`) — `kiem_yaml`/`kiem_loai_tep`/`kiem_lease`
     đọc đúng các byte ấy, cũng là byte mà các bước bị bỏ và checkout của master đọc; chưa đo riêng. KHÔNG chặn
     `.gitattributes` — tại 3569472cb9 có 3 tệp như thế dưới allowlist, cả 3 dưới `ops/reviews/` (`-whitespace` cho verdict
-    chép nguyên byte), do chính PR hồ sơ thêm vào. Tệp NHỊ PHÂN (git đoán theo nội dung + thuộc tính GỐC) thì `--check`
+    chép nguyên byte): 2/3 do PR hồ sơ thêm (#667, #670), 1/3 đi kèm PR mã (#666). Tệp NHỊ PHÂN (git đoán theo nội dung + thuộc tính GỐC) thì `--check`
     bỏ qua hẳn ⇒ `kiem_nhi_phan` coi là KHÔNG ĐO ĐƯỢC, ĐỎ (tại 3569472cb9: 0/1991 tệp dưới allowlist là nhị phân).
   · D2 — `lease_publish.py check` là cổng ĐĂNG lease: lease đã hết hạn thì nó trả rc=8 "hết hạn" theo thiết kế,
     mà bookkeeping thu hồi/đóng lease thường đúng là sửa lease hết hạn. Lease CÒN HẠN đổi trong PR chạy đúng
     `check`; lease HẾT HẠN chạy `kiem(bo_qua_han=True)` — mọi chốt như `check`, chỉ bỏ chốt hạn — nên KHÔNG
     được miễn kiểm chỉ vì hết hạn. Cả hai đuôi `.yaml` và `.yml`. Giới hạn: bia mộ hai chiều của `kiem`
-    đọc các lease khác trên mọi REF cục bộ (`_quet_lease_toan_kho`: `for-each-ref` rồi `ls-tree` từng ref), không đọc cây
-    làm việc; checkout của Actions chỉ có ref của PR, không có các nhánh `ops/**`. Nên số tệp trượt là số CỦA PHẠM VI ref,
-    không phải của kho: reviewer lượt 1 đo tại 1741e0a (113 tệp lease) — clone chỉ-master 6/113 trượt
-    `kiem(bo_qua_han=True)`, bản sao đủ 552 ref 0/113. Đo lại tại 3569472cb9 (119 tệp lease, sau merge master 20ec8d5):
+    đọc các lease khác trên mọi ref dưới `refs/heads` và `refs/remotes` (`_quet_lease_toan_kho` qua `_cac_ref_cuc_bo`:
+    `for-each-ref` rồi `ls-tree` từng ref), KHÔNG đọc tag và KHÔNG đọc cây làm việc (đo cross-review lượt 16). Checkout của
+    job `gate-ops` lấy TOÀN BỘ lịch sử; nó có nạp `refs/remotes/origin/*` của các nhánh `ops/**` hay không là CHƯA ĐO —
+    tài liệu `actions/checkout` nói chế độ ấy lấy mọi nhánh và tag, mà nếu đúng thế thì bia mộ thấy các nhánh ấy và giới
+    hạn này không xảy ra trên CI. Nên số tệp trượt là số CỦA PHẠM VI ref, không phải của kho: tại 1741e0a (113 tệp lease)
+    một clone chỉ-master cho 6/113 trượt `kiem(bo_qua_han=True)` (số của executor, cross-review lượt 16 tái lập bằng kho
+    đúng một ref), bản sao đủ 552 ref cho 0/113 (reviewer lượt 1 đo trên 1687c69, cây `ops/leases` trùng 1741e0a). Đo lại tại 3569472cb9 (119 tệp lease, sau merge master 20ec8d5):
     một ref (chỉ nhánh đang checkout) 6/119 trượt — đúng 6 tệp cũ, cùng `CHAN [8]` bia mộ — còn trên 529 ref cục bộ thì
     0/119 (529 chưa đối chiếu `ls-remote`, nên không khẳng định là đủ).
     Hệ quả CÓ CHỦ ĐÍCH về actor (chủ kho chọn khai, không đổi chốt — Issue #674, 2026-09-30): `kiem`/`check`
```
  (c) DO_LAI (phien dieu phoi): "AL_VER: 4 dong" -> "5 dong (HEAD = master 20ec8d5; 1741e0a: 4)"; "938/938" -> "1025/1025 (HEAD va master)";
      "6/113 vs 0/113" -> "6/113 tai 1741e0a; 6/119 tai 3569472 (1 ref)"; lenh numstat -> `git diff --numstat 20ec8d5 HEAD -- …` (mong `1 0`).
  Phep kiem dong lop: (1)(4) khong co chot may re cho TINH DUNG cua so hang co neo — chot la neo (de do lai) + dong BANG DO cua reviewer;
  (2)(3)(5) co chot may (t98b mo rong) va moi duong mot dot bien.
DA THU NGHIEM: ban sao tmp/hint2 (cp -a): HINT + diff san pham -> `CA: 97/97` · `DOT BIEN: 328/328 bi giet dung ly do` · `TU KIEM PHAN HANG: DAT` ·
  `TONG: DAT` rc=0; registry 23/23 · 1025/1025; ruff sach; doctrine-scan sach; dot bien cua toi A5b/A7b/B1/B2/B3 SONG truoc HINT -> GIET sau HINT;
  `patch -p0 --fuzz=0` ap sach tren `git archive HEAD`, cmp == ban da thu. sha256(out/HINT.patch) = 6f9bc81e22fcd2e840f53a6489557fcf3ce05bbb0ef99355763f8b89067ce4c2.
  Gioi han cua HINT: tu-so chi bat khi dung NGAY truoc danh tu thuc the kho (vd "ba ca" khong bat — dem cau truc); thong bao chi bat so sau
  "do "/"đo " viet thuong; neo gia (A6) van khong bat — gioi han (b) cua executor, khong doi.
DO TIN: cao (moi so do lai duoc; moi dot bien chay that); hang P3 la danh gia.

### khang-dinh-dinh-tinh-rong-hon-phep-do  [P3]  Cau D2 moi khai nhu SU THAT "checkout cua Actions chi co ref cua PR" (chua ai do, trai tai lieu checkout) va "moi REF cuc bo" (ma bo tag)
TEP/DONG: `ops/ci_duong_nhanh.py:78-80` (docstring module, D2 "Giới hạn"; cau bat dau o dong 78, menh de runner o dong 80).
VAN DE: Ban va viet lai cau D2: "bia mo hai chieu cua `kiem` doc cac lease khac tren moi REF cuc bo (`_quet_lease_toan_kho`: `for-each-ref`
  roi `ls-tree` tung ref), khong doc cay lam viec; checkout cua Actions chi co ref cua PR, khong co cac nhanh `ops/**`."
  (1) Ve "checkout cua Actions": `kiem-re` chay o `gate-ops`, checkout `actions/checkout@v4` + `fetch-depth: 0` (`ci.yml:622-625`). Tai lieu
      actions/checkout: `fetch-depth: 0` = "all history for all branches and tags" (KHONG DO DUOC o day — khong mang, khong co ban checkout cuc bo);
      chinh kho ghi cau hoi nay la CHUA DO (`ops/reviews/thu-hoi-lease-va-cap-lai-spec/spec-r1.md` muc 6, `spec-r2.md` muc 5). Phep do cua toi
      (tmp/lease1/m2_tag): NEU runner co `refs/remotes/origin/*` thi bia mo DAT (`refs/remotes/origin/ops/x` -> DAT; ca `refs/remotes/pull/1/merge`
      -> DAT), tuc "gioi han" D2 KHONG xay ra tren gate-ops. Cau khai mot dieu chua do nhu su that — trong khi CUNG commit nay da gan nhan
      "KHONG DO DUOC offline" cho cau ruleset va "chua tu do" cho cau 40-hex: day la cau duy nhat ve GitHub/runner con thieu nhan.
  (2) Ve "moi REF cuc bo": `_cac_ref_cuc_bo` chi `for-each-ref refs/heads refs/remotes` (bo `*/HEAD`); do: bia mo chi tren TAG -> `CHAN 8`.
      Cau moi rong hon ma (do ban va nay SINH; ban cu viet "trong CAY", cung sai nhung theo chieu khac). Ve "khong doc cay lam viec": DUNG (bia mo
      chi tren dia -> CHAN 8).
  Khong anh huong hanh vi (ca hai chieu deu fail-close); la khang dinh rong hon phep do => P3. Cung hinh dang lop da dong `cau-khai-skipped-nguoc-phep-do`
  nhung cau khac, doi tuong khac — khong mo lai slug cu.
DA THU VA: co — khoi diff san pham o finding tren (hunk `@@ -70,16 +70,19 @@`), cac dong lien quan:
```diff
-    đọc các lease khác trên mọi REF cục bộ (`_quet_lease_toan_kho`: `for-each-ref` rồi `ls-tree` từng ref), không đọc cây
-    làm việc; checkout của Actions chỉ có ref của PR, không có các nhánh `ops/**`. Nên số tệp trượt là số CỦA PHẠM VI ref,
+    đọc các lease khác trên mọi ref dưới `refs/heads` và `refs/remotes` (`_quet_lease_toan_kho` qua `_cac_ref_cuc_bo`:
+    `for-each-ref` rồi `ls-tree` từng ref), KHÔNG đọc tag và KHÔNG đọc cây làm việc (đo cross-review lượt 16). Checkout của
+    job `gate-ops` lấy TOÀN BỘ lịch sử; nó có nạp `refs/remotes/origin/*` của các nhánh `ops/**` hay không là CHƯA ĐO —
+    tài liệu `actions/checkout` nói chế độ ấy lấy mọi nhánh và tag, mà nếu đúng thế thì bia mộ thấy các nhánh ấy và giới
+    hạn này không xảy ra trên CI. Nên số tệp trượt là số CỦA PHẠM VI ref, không phải của kho: tại 1741e0a (113 tệp lease)
```
  CHOT RIENG: (1) khong co chot may offline — chot la NHAN "CHUA DO" + phep do tren PR that (cung dot voi nghiem thu 11): in TAP ten
  `git for-each-ref --format='%(refname:lstrip=3)' refs/remotes/origin` (bo `HEAD`) va so TAP voi `git ls-remote --heads origin` (CLAUDE.md:
  so bang tap ten, khong bang `wc -l`; khong chay duoc ls-remote => KHONG XAC DINH) trong log buoc kiem-re, roi chot cau D2 theo ket qua — doi than `run:` thi `y14` (khop nguyen van) phai doi theo, nen day la lua chon cua executor/chu kho, khong bat buoc.
  (2) phep do hanh vi tai lap duoc (tmp/lease1: kho tam dung mot ref, commit tong hop mang `da_bi_thay_the`, dat lan luot o tag / refs/remotes /
  dia) — muon thanh ca test thi them vao `ops/ci_duong_nhanh_test.py` mot ca dung `kho_that(..., sao_lease_publish=True)` + `MA_KIEM_HET_HAN`
  doi ba vi tri ay (mong rc 8 / 0 / 8); dot bien lam no DO: doi danh sach namespace cua `_cac_ref_cuc_bo` trong ban sao lease_publish (harness
  hien chi dot bien MA/TEST/YML/DK nen can them mot loai tep dich) — mo ta bang loi, chua dung.
DA THU NGHIEM: tmp/lease1/m2_tag: 1 ref -> `CHAN 8`; X chi tren `refs/tags/t-bia-mo` -> `CHAN 8`; X duoi `refs/remotes/pull/1/merge` -> `DAT`;
  X duoi `refs/remotes/origin/ops/x` -> `DAT`; tmp/lease1/m3_wt: bia mo chi tren dia -> `CHAN 8`. Khoi diff (cung khoi o finding tren) da ap tren
  tmp/hint2: t98b DAT, suite 97/97 · 328/328 · TONG DAT. Hanh vi that cua runner: KHONG DO DUOC.
DO TIN: vua-cao (phan ma: cao, do duoc; phan runner: dua tai lieu + so chua-do cua chinh kho, KHONG DO DUOC).

## GHI CHU QUY TRINH
- Moi ghi chi trong $R (tmp/, out/). `cay-kho` khong bi sua (`git status --short` rong sau moi lan chay). Khong commit/push/checkout trong kho
  that; khong mang; khong cong cu GitHub. Mot lenh co `rm -rf` + `git checkout` trong tmp bi he thong quyen tu choi -> thay bang
  `git archive` + `update-ref` + alternates (khong checkout).
- Ban sao: tmp/nt10, tmp/hint2 (cp -a); tmp/nt9a, nt9b, nt9m, tmp/hint, tmp/hint_chk (git archive); tmp/lease1/m1_*, m2_tag, m3_wt (archive +
  alternates -> kho.git, dung mot ref); tmp/gl1 (kho git tam); cay mini tmp/m16/*, tmp/m16h/*; cay tam cua harness (dung_cay_tam) tu xoa.
- Rig cua toi: tmp/ast/so_ast.py, tmp/neo/{liet_ke,loai,chu,chu2,chuoi}.py, tmp/lease1/{do,mot}.py, tmp/m16/{mut_t98b,harness13,nghiem_thu}.py,
  tmp/lam_hint.py. Log: tmp/logs/{suite_head,selftest,suite_hint2}.log.
- Dot bien SONG SOT cua toi tren HEAD: A5 (so bang chu), A6 (neo gia), A7 (so trong thong bao), B1, B2, B3 (noi long bo quet) — thanh finding;
  B5, B6 (SIET CHAT, vo hai), B8 (chot ha tang — tuong duong tren du lieu hien tai; B9 chung minh chot co rang), B10 (mong song).
  Sau HINT: con A6 (gioi han tu khai b), B5, B6, B8, B10.
- KHONG DO DUOC: hanh vi that tren GitHub Actions (ref cua checkout fetch-depth 0, PR that, nghiem thu 11, windows-latest), so 529/552 ref,
  chu ky SSH cua head, model/effort thuc chay cua chinh luot nay.
- Danh tinh: Claude Opus 5.5, CUNG HO executor => `advisory_review`, KHONG phai cross_approved.

So lop: 10 — 2 MO: `bang-do-thieu-neo-va-thieu-kiem-ke` (P3), `khang-dinh-dinh-tinh-rong-hon-phep-do` (P3, moi); 8 DONG: `kiem-mode-git-chot-khong-rang`, `buoc-bi-bo-doc-ca-cay-khong-chi-ba-ca`, `kiem-re-cua-fail-close-chua-co-ca`, `kiem-re-bi-cau-hinh-boi-du-lieu-ho-so`, `phan-loai-khong-neo-merge-ref-that`, `cau-khai-skipped-nguoc-phep-do`, `dependency-failure-skips-required-checks`, `kiem-re-phu-thuoc-actor-su-kien`.

TONG: P0=0 P1=0 P2=0 P3=2 — so lop: 10 (2 mo, 8 dong)
