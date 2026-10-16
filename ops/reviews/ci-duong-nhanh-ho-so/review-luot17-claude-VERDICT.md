verdict: changes_requested
reviewed_sha: 41508cdead6e2b000626ca0260707d5056eff83f
Reviewed commit: 41508cdead6e2b000626ca0260707d5056eff83f

> luot 17 (packet #674, dac ta r2 sha256 b6e719c9…da57 KHOP; r1 e6949841…c64c KHOP). TRANG THAI: XONG 11 huong + doi chieu.
> Ket luan: 1 finding P3 — lop `buoc-bi-bo-doc-ca-cay-khong-chi-ba-ca` MO LAI voi bang chung moi (duong vao bi danh thu muc TRONG cay toi
> thu muc ten bi bo qua; gioi han executor tu khai tro dung co che nhung chi ra bien the KHONG dung duoc tren runner va bo sot bien the dung
> duoc). Hai lop tai lieu cua luot 16 DA VA THAT. San pham khong doi hanh vi so voi 91cd2f7/3569472 (AST bo docstring giong het).
> Nguong chu kho 0/0/0 => KHONG approve.
> Reviewer: Claude Opus 5.5, CUNG HO voi executor => `advisory_review`, KHONG phai cross_approved; packet `sensitive` van can Codex
> `cross_approved` hoac `human_audited` o cong land. Model/effort thuc chay: KHONG DO DUOC.

## DOI CHIEU LUOT TRUOC
Moi dong co phep do CUA TOI (dot bien chu KHAC harness / do lai so hang / doc lai neo), chay tren ban sao hoac kho tam; cay-kho khong bi sua.

| luot · finding · duong vao | hang cu | trang thai | bang chung TU DO |
|---|---|---|---|
| 16 · `bang-do-thieu-neo-va-thieu-kiem-ke` (1) luong tu sai du co neo (D1 + t20p "do chinh PR ho so them vao", do 2/3) | P3 | **DA VA THAT** | D1/t20p viet lai thanh khang dinh TON TAI "PR ho so co them tep nhu the ... (PR #667 merge 3fee59e, PR #670 merge dcd5fe0)": 3fee59e = `Merge PR #667`, dcd5fe0 = `Merge PR #670`, moi merge them dung mot `.gitattributes` `-whitespace` duoi `ops/reviews/`, diff ca hai toan allowlist (HUONG 11). Khong co chot may cho TINH DUNG luong tu — nay KHAI thang o t98b (b) ("KHONG kiem so hang, luong tu hay NGUON"); dot bien B9 cua toi (luong tu sai "MỌI tệp ... đều do PR ho so them") SONG dung gioi han khai |
| 16 · cung lop (2) so ve KHO viet bang CHU, neo `master` (t20p "master co ba tep") | P3 | **DA VA THAT** | cau t20p bo so; `MAU_SO_CHU_KHO` + 22 dot bien go tung tu-so/danh tu (sinh tu `SO_CHU_LUAT`/`DANH_TU_KHO_LUAT` doc lap). Dot bien CUA TOI: B1 (`bốn nhánh` trong docstring HAM san pham) GIET, B2 (`ba\n    tep` xuong dong trong docstring test) GIET (HUONG 6) |
| 16 · cung lop (3) so trong CHUOI thong bao `bang()` (t20d `8/63`, y01 `4 luot`) | P3 | **DA VA THAT** | t20d bo so; y01 neo `Issue #674 comment 5889459132`; bo quet `cau_thong_bao` phu 50 Constant + 204 JoinedStr = MOI loi goi `bang` (do AST: khong co BinOp/format). Dot bien CUA TOI B4 (`(đo 3 lượt)` vao mot `bang` KHAC), B6 (sai ten ham), B7 (>= 3 doi so) GIET |
| 16 · cung lop (4) gan NGUON do (D2 "reviewer luot 1 do ... 6/113") | P3 | **DA VA THAT** | D2 bo gan nguon, neo lai tai 3569472cb9: do lai MOT ref `tong 119 dat 113 truot 6`, theo (ma, bia_mo) `{(8, True): 6}` (HUONG 8). Khong co chot may cho NGUON — khai o t98b (b); dot bien B8 cua toi SONG dung gioi han khai |
| 16 · cung lop (5) 3 nhanh t98b KHONG RANG (neo co chu so, `;` ranh gioi cau, `·` ranh gioi doan) | P3 | **DA VA THAT** | 3 mau tu kiem + 3 dot bien harness moi; bien the CUA TOI B10 (`[0-9]?`), B11 (`;` chi tach khi >= 2 khoang trang), B12 (`·` chi tach khi khong thut) GIET |
| 16 · cung lop (6) `goi/DO_LAI.md` (NGOAI kho, phien dieu phoi) | P3 | **CHUA VA** (ngoai write set executor) | van "AL_VER: 4 dong" (HEAD 5), "938/938" (1025/1025), "lease 6/113 vs 0/113" (119 tep), "numstat 1741e0a HEAD (mong 1 0)" (do `172 6`; so master `1 0`). Khong tinh vao packet — xem muc GHI CHU CHO PHIEN DIEU PHOI |
| 16 · `khang-dinh-dinh-tinh-rong-hon-phep-do` (1) D2 khai nhu su that "checkout cua Actions chi co ref cua PR" | P3 | **DA VA THAT** | cau moi: `fetch-depth` khong gioi han (ci.yml gate-ops `fetch-depth: 0`, do bang yaml), "co nap `refs/remotes/origin/*` ... KHONG ĐO ĐƯỢC offline — tai lieu `actions/checkout` noi ... moi nhanh va tag" + hai nhanh he qua (do luot 16). Chot may t98c: 29 cau nhac nen deu co nhan/neo; dot bien CUA TOI C1 (cau GitHub khong nhan, docstring HAM), C2 (chu thich test actions/checkout khong nhan) GIET |
| 16 · cung lop (2) "moi REF cuc bo" rong hon ma (bo tag) | P3 | **DA VA THAT** | D2: "moi ref duoi `refs/heads` va `refs/remotes` ... KHÔNG đọc tag và KHÔNG đọc cây làm việc (`t21b` ...)"; t21b do 4 vi tri tren `lease_publish` THAT. Dot bien CUA TOI D1 (lease_publish bo moi ref chua `/ops/`) GIET, D3 (docstring "doc ca tag") GIET. Con: D2 (THEM cau mau thuan, giu nguyen hai cum) SONG — t21b chi do su CO MAT cua cum; ghi chu, khong nang hang (xem BANG DO) |
| 16 · 8 lop DONG | DONG | 7 van DONG; **`buoc-bi-bo-doc-ca-cay-khong-chi-ba-ca` MO LAI** | 7 lop: ci.yml, `ci_dang_ky_test.py`, AST san pham khong doi tu 3569472; suite 99/99 · 366/366 gom moi dot bien cu; nghiem thu 1-7 bang dot bien cua toi (HUONG 2). Lop symlink: bang chung MOI do duoc — duong vao bi danh thu muc TRONG cay (HUONG 5) |
| 15/14/8b · cac finding cu (F1/F2, X1, ...) | DA VA THAT (luot 15) | van DA VA THAT | dot bien tuong ung nam trong 366/366 `bi giet dung ly do`; san pham khong doi hanh vi |

## BANG LOP
| slug | bieu hien (duong vao da liet ke) | hang cao nhat con mo | phuong an va chung | phep kiem dong lop |
|---|---|---|---|---|
| `buoc-bi-bo-doc-ca-cay-khong-chi-ba-ca` (MO LAI) | Bat bien: tap symlink ma kiem-re duyet phai BANG tap ma `t82` (copytree khong `symlinks=True`) cham toi. Duong vao: (a) symlink treo NGOAI diff trong thu muc thuong — DA DONG (t20zi, 5 nhanh); (b) bi danh thu muc TRONG cay -> thu muc ten bi bo qua (`*.pyc`, `__pycache__`) chua symlink; PR ho so xoa dich -> `duong_nhanh`, kiem-re rc=0, t82 `shutil.Error` — **MO, DO DUOC** (HUONG 5); (c) bi danh -> `.git` (walker bo `.git`, t82 chep qua bi danh) — cung co che, PR khong tao duoc symlink trong `.git` nen khong phai duong vao thuc te; (d) bi danh tro RA NGOAI cay (executor khai) — cung co che; bi danh treo da bi bat (t20zi E1b), noi dung thu muc ngoai cay PR khong quyet => khong dung duoc tu noi dung kho tren runner (SUY LUAN; khong dung duong thoat cay theo luat => KHONG DO DUOC bang phep thu); (e) vong symlink thu muc — walker hien khong theo nen DAT, t82 vap; master co vong thi t82 da do truoc => khong do PR ho so gay ra. Da ra va SACH: cac buoc bi bo khac (audit hook luot 15, khong doi tu 20ec8d5) | **P3** | MOT tu khoa: `os.walk(..., followlinks=True)` — duyet DUNG phep duyet cua t82, dong (b)(c)(d) bang KIEN TRUC; vong -> nhan tu choi phan giai -> phan tu cuoi la symlink TREO -> DO (do). Khoi diff san pham trong finding + `out/HINT.patch` | t20zk (bien the `kho.pyc` va `__pycache__` co bi danh -> DO; khong bi danh -> DAT; PR sua tep khac -> DAT; vong -> DO) DO tren HEAD, XANH sau va; dot bien harness moi `symlink_treo_khong_theo_bi_danh` + dot bien CUA TOI H3..H7 deu GIET (moi nhanh con mot dot bien rieng); suite ban sao 100/100 · 367/367 (HUONG 10) |
| `bang-do-thieu-neo-va-thieu-kiem-ke` | 5 duong vao trong kho luot 16 DA VA THAT (DOI CHIEU); dot bien song B3 (`\s+` -> 1 khoang trang) la RANG bo kiem, khong che khang dinh sai nao | DONG (cho packet) | — | t98b + 22 dot bien tu-so/danh tu + B1/B2/B4/B6/B7/B10/B11/B12 cua toi GIET; moi so do lai KHOP (HUONG 8) |
| `khang-dinh-dinh-tinh-rong-hon-phep-do` | 2 duong vao luot 16 DA VA THAT; nhan cua 29 cau nhac nen khong mau thuan tai lieu (HUONG 4); dot bien song C4/C5/C6/D2 la RANG bo kiem, khong che khang dinh sai nao | DONG | — | t98c + t21b; C1/C2/D1/D3 cua toi GIET |
| 7 lop cu (`kiem-mode-git-chot-khong-rang`, `kiem-re-cua-fail-close-chua-co-ca`, `kiem-re-bi-cau-hinh-boi-du-lieu-ho-so`, `phan-loai-khong-neo-merge-ref-that`, `cau-khai-skipped-nguoc-phep-do`, `dependency-failure-skips-required-checks`, `kiem-re-phu-thuoc-actor-su-kien`) | — | DONG | — | suite 99/99 · 366/366; nghiem thu 1-10 (HUONG 2, 3) |

## SO DO NEN (@41508cd, Linux, Python 3.11.15, git 2.43.0, actionlint 1.7.7 + shellcheck 0.9.0, ruff 0.16.9, TMPDIR=$R/tmp)
- `python3 -B ops/ci_duong_nhanh_test.py`: `CA: 99/99 dat · 0 do · 0 hong` · `DOT BIEN: 366/366 bi giet dung ly do` ·
  `KIEM KE: ca hanh_vi=69 + cau_truc_yaml=16 + so_dang_ky=3 + tu_kiem=11 = 99 · dot bien ci_dang_ky_test.py=2 + ci.yml=74 +
  ci_duong_nhanh.py=197 + ci_duong_nhanh_test.py=90 + lease_publish.py=3 = 366` · `TU KIEM PHAN HANG: DAT (5 mau rc, 3 dot bien that)` ·
  `TONG: DAT` · rc=0 · real 2m16s. `git status --short` truoc/sau: rong.
- `python3 -B .claude/dev/ci_dang_ky_test.py`: `ĐĂNG KÝ: 23/23` · `PHẢN CHỨNG: 1025/1025 đỏ đúng` · `TỔNG: ĐẠT` · rc=0
- `actionlint .github/workflows/ci.yml` rc=0 · ruff F hai tep moi `All checks passed!` · tl.py 12 F821 (= nen CLAUDE.md)
- AST san pham bo docstring (tmp/ast/so_ast.py): 3569472 = 91cd2f7 = 41508cd = `cf27fd5f9f81` => san pham KHONG doi hanh vi;
  `ci.yml`, `ci_dang_ky_test.py` khong doi tu 3569472 (`git diff --quiet` rc=0).

## BANG SAN
HUONG 1: so nen + loi khai commit 41508cd ("CA 99/99, DOT BIEN 366/366", "san pham CHI docstring/chu thich, AST bo docstring GIONG HET")
  gia thuyet : neu loi khai rong hon phep do thi so in ra khac / AST san pham khac
  lenh       : python3 -B ops/ci_duong_nhanh_test.py ; python3 -B .claude/dev/ci_dang_ky_test.py ; actionlint ; ruff ; tmp/ast/so_ast.py 3569472 91cd2f7 41508cd
  output     : xem SO DO NEN
  ket luan   : KHONG PHAI LOI

HUONG 2: nghiem thu 1-7 cua SPEC-r2 do DOC LAP (dot bien CHU cua toi, khac harness; ban sao tam qua dung_cay_tam/chay_con/phan_hang cua chinh bo test)
  gia thuyet : neu mot ca nghiem thu khong co rang thi dot bien cua toi (khong nam trong DOT_BIEN) song
  lenh       : python3 -B tmp/m17/nt.py tmp/m17/nt.json (rig tmp/m17/rig.py; CTRL = ban sao khong dot bien)
  output     : CTRL 11 ca dich rc=0 · N1 (toan allowlist -> DAY_DU) t01 rc=3 GIET · N2 (khop them `scripts/` qua `or startswith`) t02 GIET ·
               N3 (KHONG DO DUOC -> DUONG_NHANH) t05, t06 GIET · N4 (goi `git rev-parse --git-dir` truoc kiem su kien) t03 GIET ·
               N5 (them `.github/`) t08 GIET · N6a (go `if:` pull_request cua buoc phan loai) y01 GIET · N6b (release-check full `if: ${{ false }}`)
               y03, y04, y12 GIET · N6c (packet-loop selftest `== 'day_du'`: output VANG => bo buoc = fail-open) y03, y12 GIET ·
               N7 (`paths-ignore` duoi pull_request) y05 GIET · `LECH so voi mong: []`
  ket luan   : KHONG PHAI LOI

HUONG 3: nghiem thu 8-10 + pham vi diff (phan them so 1741e0a co DUNG la cua master) + chu ky head
  lenh       : (tmp/nt8, nt9a, nt9b = git archive 41508cd; nt9m = git archive 20ec8d5) chen dong chu thich chua bieu thuc rong
               (dau `$` dung bang chr(36) SAU phan tich) vao than run buoc kiem-re roi actionlint goc/dot bien ; go dong DA_NOI ;
               doi `run: python ops/ci_duong_nhanh_test.py` ; numstat ; (tmp/nt10 = cp -a, core.abbrev 7) python3 scripts/tl.py --selftest ;
               vong so blob HEAD:<f> vs 20ec8d5:<f> cho moi tep cua `git diff 1741e0a HEAD` ngoai 4 tep packet ; git cat-file -p HEAD
  output     : actionlint goc rc=0 · dot bien rc=1 `ci.yml:654:66: unexpected end of input while parsing ... [expression]` ·
               nt9a `ĐỎ: test sống chưa đăng ký: ops/ci_duong_nhanh_test.py` `ĐĂNG KÝ: 23/22` `TỔNG: ĐỎ` · nt9b `ĐỎ: CI không gọi mục đăng ký:
               ops/ci_duong_nhanh_test.py` `TỔNG: ĐỎ` · nen master 20ec8d5 `ĐĂNG KÝ: 22/22` `PHẢN CHỨNG: 1025/1025` -> HEAD 23/23, 1025/1025 ·
               numstat so master `1 0` (so 1741e0a `172 6` = 171 dong cua #668 + 1) · `== tl selftest 1715/1715 ==` rc=0 (4m55s) ·
               20ec8d5..HEAD dung 4 tep packet; 127 tep ngoai packet trong diff 1741e0a..HEAD lech blob voi master: 0; 20ec8d5 la to tien HEAD ·
               head 41508cd co khoi `gpgsig` SSH, cha 91cd2f7 (xac minh chu ky: KHONG DO DUOC — khong allowedSignersFile)
  ket luan   : KHONG PHAI LOI

HUONG 4: t98b/t98c/t21b co false-red theo phien ban Python (CI ghim 3.12 cho gate-ops: ci.yml `python-version: "3.12"`) + nhan
         "theo tai lieu" co bi dung de chuyen khang dinh SAI khong
  gia thuyet : neu tokenize/ast khac giua 3.11/3.12/3.13 thi bo quet cho ket qua khac (do oan tren CI); neu mot cau mang nhan
               "theo tai lieu" ma tai lieu noi KHAC thi nhan thanh loi thoat
  lenh       : python3.11|3.12|3.13 -B ops/ci_duong_nhanh_test.py --mot-ca <t98b|t98c|t21b> ; (ca khong ton tai -> rc=2: --mot-ca CO chay ca) ;
               tmp/m17/liet_ke.py (exec tep test, dung cau_tai_lieu/cau_thong_bao/so_do_trong_cau/MAU_NHAC_NEN cua CHINH no) duoi ca ba ban, sha256 JSON
  output     : 9/9 rc=0 · JSON 3.11 = 3.12 = 3.13 (`cc15f82b265e7a36`) · san pham: 140 cau, 7 cau co so do (17 so), 15 cau nhac nen ·
               tep test: 669 cau, 3 cau co so do (4 so), 14 cau nhac nen · 29 cau nhac nen deu co nhan/neo. Doi chieu NOI DUNG tung nhan voi
               tai lieu (theo hieu biet cua reviewer — KHONG DO DUOC truc tiep, khong mang): paths/paths-ignore -> check bat buoc Pending/chan
               merge; dereference thuoc tinh vang -> chuoi rong; checkout mac dinh ref/SHA cua su kien; `fetch-depth: 0` = moi nhanh + tag;
               `GITHUB_ACTOR` = nguoi/app khoi chay; PR xung dot -> workflow `pull_request` khong chay; checkout mac dinh khong init submodule;
               skipped do dieu kien -> bao Success; buoc that bai theo ma thoat khac 0: KHONG thay cau nao noi NGUOC tai lieu. Cau "cung thuat
               toan merge voi GitHub — theo tai lieu" dua tren bai blog ky thuat cua GitHub hon la tai lieu chinh thuc; da kem "chua tu do".
  ket luan   : KHONG PHAI LOI (khong false-red theo phien ban; nhan khong dang che khang dinh sai nao reviewer nhan ra duoc)

HUONG 5: gioi han MOI executor tu khai (symlink treo chi voi toi QUA symlink thu muc tro ra ngoai cay; `t82` vap, `os.walk` khong thay)
         — co phai lo that tren duong nhanh khong, PR ho so co dung duoc khong, tu master co san
  gia thuyet : neu bo duyet cua `kiem_symlink_treo_ca_cay` (os.walk, khong theo symlink thu muc) va `t82` (copytree, symlinks=False ->
               THEO symlink thu muc) phu hai tap KHAC nhau ngay TRONG cay, thi PR ho so xoa dich lam `t82` do tren master ma kiem-re DAT
  lenh       : git ls-tree -r HEAD | awk '$1=="120000"' (dem symlink tren HEAD) ; doc t82 (`ops/lease_publish_test.py:3159`) ;
               python3 -B tmp/m17/symlink_bidanh.py — kho tam (kho_that/kiem_re/phan_loai_that cua CHINH bo test), MOI duong dich TRONG cay:
               thu muc ten bi bo qua (`kho.pyc` | `__pycache__`) chua symlink `s` -> `../ops/land/f.yaml`, symlink THU MUC bi danh `bidanh` ->
               thu muc ay; PR ho so `git rm ops/land/f.yaml`; so `kiem-re` voi `shutil.copytree(..., ignore=ignore_patterns(".git",
               "__pycache__", "*.pyc"))` (dung loi goi cua t82); doi chung: PR them tep khac; doi chung: KHONG co bi danh
  output     : HEAD co 0 symlink · t82 goi copytree khong `symlinks=True`, khong try ·
               [kho.pyc, co bi danh]  goc: t82-chep OK · doi chung kiem-re rc=0, t82-chep OK · PR xoa dich: phan loai `duong_nhanh`,
               kiem-re rc=0, dong TREO = [], t82-chep `shutil.Error (1 loi)` ·
               [__pycache__, co bi danh] y het: `duong_nhanh`, kiem-re rc=0, t82-chep `shutil.Error` ·
               [kho.pyc, KHONG bi danh] PR xoa dich: kiem-re rc=0, t82-chep OK (hai ben cung bo qua thu muc ay — khong lech)
  ket luan   : LOI (P3) — lop `buoc-bi-bo-doc-ca-cay-khong-chi-ba-ca` MO LAI voi bang chung moi: con mot duong vao TRONG cay (bi danh thu muc ->
               thu muc ten bi bo qua) ma docstring KHONG khai; bien the executor khai (tro RA NGOAI cay) thi KHONG dung duoc tu noi dung kho
               tren runner (bi danh treo da bi bat — t20zi E1b; noi dung thu muc ngoai cay PR khong doi duoc). PR ho so KHONG tu dung duoc tinh
               huong (khong them duoc symlink: kiem_mode_git chan 120000 tren ca ba cap, kiem_loai_tep chan tren dia); can master co SAN hai
               symlink (bi danh + symlink trong thu muc ten bi bo qua) vao qua PR day du — HEAD co 0 symlink. Hau qua: PR xanh, `t82` DO tren
               master o luot push (luon day du) — cung hinh dang lop P2 luot 8b, them dieu kien tien quyet hiem. Xem finding.

HUONG 6: DOI CHIEU tung duong vao luot 16 bang dot bien CHU CUA TOI (khac 366 dot bien harness), ban sao tam qua rig tmp/m17
  gia thuyet : neu ban va chi dong DUNG chuoi/vi tri luot 16 chi ra (va dot bien harness neo vao chuoi ay) thi mot bien the khac cua cung
               duong vao se SONG
  lenh       : python3 -B tmp/m17/dc.py tmp/m17/dc.json (CTRL: t98b, t98c, t21b rc=0 tren ban sao khong dot bien)
  output     : GIET dung ca: B1 (so chu `bốn nhánh` trong docstring HAM san pham) · B2 (so chu XUONG DONG `ba\n    tep` trong docstring test) ·
               B4 (`(đo 3 lượt)` trong thong bao bang() KHAC) · B6 (cau_thong_bao sai ten ham) · B7 (doi >= 3 doi so) · B10 (dieu kien chu so cua
               neo thanh tuy chon `[0-9]?`) · B11 (`;` chi tach khi >= 2 khoang trang) · B12 (gach `·` chi tach khi KHONG thut dong) ·
               C1 (cau "Runner cua GitHub ..." khong nhan, docstring HAM) · C2 (chu thich test "actions/checkout ..." khong nhan) ·
               D1 (lease_publish bo moi ref chua `/ops/`) · D3 (docstring "doc ca tag") — tat ca rc=3 dung ten ca dich.
               SONG, DUNG gioi han TU KHAI: B8 (gan nguon "reviewer luot 1 do" — t98b (b) khong kiem NGUON) · B9 (luong tu sai "MỌI tệp ... đều do PR
               ho so them" — t98b (b)) · C3 (khang dinh SAI co nhan "theo tài liệu" — t98c (b)).
               SONG, ngoai danh sach duong vao ca tu khai (khong co mau tu kiem): B3 (`MAU_SO_CHU_KHO` `\s+` -> 1 khoang trang: tu-so cuoi dong +
               danh tu dau dong sau thoat) · C4 (t98c nhan MOI con so la neo: `MAU_SO_TRONG_VAN` thay `MAU_NEO_SO_DO`) · C5 (t98c nhan chu `do`/`đo`
               tran la nhan) · C6 (`Github` viet hoa khac lot `MAU_NHAC_NEN`) · D2 (giu nguyen hai cum t21b doi, THEM cau mau thuan "bia mo cung
               doc tag" — t21b chi do su CO MAT cua cum).
  ket luan   : Duong vao luot 16: DA VA THAT (xem DOI CHIEU). Dot bien song B3/C4/C5/C6/D2: KHONG nang hang — chung la do RANG cua bo
               kiem tai lieu, hien KHONG che khang dinh SAI nao trong hai tep (t98b/t98c xanh, quet tay HUONG 4/8 khong thay cau sai), va
               PROMPT luot 17 chi cho nang hang hai lop tai lieu khi co khang dinh SAI lam nguoi doc hanh dong sai. Ghi lai de executor biet;
               D2 la cau tu khai cua t21b rong hon phep do (xem BANG DO), muc do: ghi chu.

HUONG 7: t98b/t98c co QUA CHAT (chan sua tai lieu hop le) hoac de vo khong
  gia thuyet : neu hai bo quet bao nham cau hop le (khong phai khang dinh ve kho/nen) thi moi PR sua hai tep phai lach chu; neu ket qua phu
               thuoc moi truong thi cong de vo
  lenh       : python3 -B tmp/m17/chat.py (goi so_do_khong_neo / nhac_nen_khong_nhan cua CHINH tep test tren 8 cau mau hop le)
  output     : "Quyết định Q2 ... Issue #674 trên GitHub." -> t98c BAO · "Bộ quét đọc hai tệp của packet." -> t98b BAO · "Hàm này có ba nhánh `if`."
               (nhanh MA, dong am) -> t98b BAO · "Hàm trả 3 giá trị." -> t98b BAO (thiet ke chu so tu luot 15) · "Biến `ruleset` giữ tên ruleset." -> t98c BAO ·
               "... CẢ hai tệp ..." -> khong bao · `bang(x, f"loi: do {y} khong dat")` -> khong bao · `bang(x, "loi do 2 nhanh cung sai")` -> t98b BAO
  ket luan   : KHONG PHAI LOI — chat CO CHU DICH, quy uoc da khai (t98b "so dem CAU TRUC viet bang chu thi do o ca so huu no", mien `ca`/`cả`;
               t98c "khang dinh ve hanh vi nen thi goi ten nen" + nhan); chi quet DUNG hai tep cua packet; ket qua tat dinh, giong nhau tren
               3.11/3.12/3.13 (HUONG 4); thong bao chi dung cau. Gia cua quy uoc: nguoi sua hai tep phai them neo/nhan hoac viet `CẢ` — ghi de chu kho biet.

HUONG 8: do lai MOI so hang trong docstring/chu thich (17 so san pham, 4 so tep test — danh sach do CHINH bo quet t98b liet ke, HUONG 4)
  lenh       : goi/do_lai_so.py (tren ban sao nt10) ; git log --merges --first-parent 1741e0a (khong -n) ; ls-tree/numstat cay rong -> 3569472cb9
               (co/khong --attr-source) ; (tmp/lease17: git archive 3569472cb9 + alternates, DUNG MOT ref `chi-mot`) tmp/lease17/do17.py =
               lp.kiem(bo_qua_han=True) tung tep lease (GITHUB_ACTOR go) ; exec tep test tai 7b8c856, dem ca theo tien to ; goi/kiem_ke.py x3 (thoi gian)
  output     : `[1] ... do duoc diff: 345; toan allowlist: 63; ... NGUYEN BAN do: 8` · khong -n: 345, 345/345 hai cha · 8/63 = 12,7% (~13%) ·
               1991 tep duoi allowlist tai 3569472cb9, nhi phan 0 (co va khong --attr-source) · 119 tep lease (3569472cb9 va HEAD) ·
               MOT ref: `tong 119 dat 113 truot 6 | theo (ma, bia_mo): {(8, True): 6}` · 7b8c856: 53 ca `{'t': 38, 'y': 12, 'k': 3}`, t97/t98/t99
               tu kiem -> 35/12/3/3 · ba ca du lieu `loi = []` 7,4 / 7,7 / 7,9 s (4 CPU, Python 3.11.15) · ref cuc bo: cay-kho 5, kho.git 4
  ket luan   : KHONG PHAI LOI — moi so do lai duoc deu KHOP; "529 ref" va "52 phut (run 36518707072)", "360 phut" (comment 5889513175): KHONG DO DUOC
               (khong mang; mirror chi 4-5 ref) — deu da gan neo/nhan.

HUONG 9: ci.yml doc lap (khong doi tu 3569472) + cac khang dinh dinh tinh MOI cua ban va ve ci.yml/kho
  gia thuyet : neu "y13 khoa `with:` cua moi buoc", "khong checkout nao khai `ref:`", "`t191` doi dung mot chot duoc mien", "cong DUY NHAT
               canh `if:` sau G5" (chu thich ci.yml) sai thi do duoc; neu actionlint toan workflow lech master thi co hoi quy
  lenh       : yaml.safe_load ci.yml liet ke `with:` moi buoc checkout ; tmp/m17/y13.py (them `ref: ${{ github.event.pull_request.head.sha }}` vao
               checkout gate-ops) ; doc t191 (`ops/lease_publish_test.py:9782`) ; (tmp/duynhat = archive, tmp/dn2 = cp -a) doi `if:` cua
               `lease-publish selftest (đo lại setup sau G5)` thanh `${{ false }}` roi chay ci_dang_ky_test, `tl.py workflow-audit --strict`,
               `.github/checks/ci_phamvi_test.py` (tren BAN GIT; ban archive do vi `git worktree` — tao tac rig, doi chung nt10 cung lenh), doctrine-scan ;
               actionlint .github/workflows/*.yml HEAD vs 20ec8d5
  output     : 7 buoc checkout, `with:` chi `fetch-depth: 0` hoac rong, khong `ref:` · Y13 dot bien: y13 rc=3 GIET · t191 docstring "Đúng MỘT chốt được
               miễn sẵn (chốt hạn)" · dot bien `if:` sau G5: ci_dang_ky_test `TỔNG: ĐẠT`, workflow-audit `ok= True issues= 0`, ci_phamvi_test
               `7/7` (ca doi chung nt10 `7/7`), doctrine-scan sach => khong cong nao trong bon cong ay bat (y03/y12 cua packet bat — HUONG 2 N6b
               cung loai) · actionlint toan workflow: HEAD rc=1 / master rc=1, cung 1 dong `ops-don-ref.yml ... SC1003:info` => delta 0
               · chong chen lenh: yaml 41508cd vs 20ec8d5 -> 8 buoc do packet them; than `run:` cua ca 8 KHONG chua bieu thuc noi tuyen;
               du lieu su kien (SHA, ten su kien) di qua `env:` (CI_DUONG_NHANH_*, SU_KIEN) — y14 khoa nguyen van than run
  ket luan   : KHONG PHAI LOI — cac khang dinh do duoc deu dung; "DUY NHAT" khong bi bac boi bon cong da chay (khong phai mot phep do vet can).

HUONG 10: HINT cua luot nay co rang va khong lam vo cong (tu kiem chinh HINT truoc khi giao)
  gia thuyet : neu ca moi khong DO tren san pham HEAD thi no khong do gi; neu ban va lam do ca/dot bien/registry/ruff cu thi HINT la no moi
  lenh       : (tmp/hint17 = cp -a cay-kho) tmp/m17/lam_hint.py tmp/hint17 [ca_hai] ; --mot-ca t20zk TRUOC va SAU khi ap phan san pham ;
               python3 -B ops/ci_duong_nhanh_test.py (tron bo) ; ci_dang_ky_test ; ruff F ; doctrine-scan ; so AST san pham bo docstring ;
               THAT_DIR=tmp/hint17 tmp/m17/hint_rang.py (H3, H4, H5 — dot bien CUA TOI, khac dot bien harness) ; vong symlink goi thang
               `kiem_symlink_treo_ca_cay` ; (tmp/hint_chk17 = git archive 41508cd) patch -p0 --fuzz=0 < out/HINT.patch ; patch -p0 --fuzz=0
               < tmp/hint17_sanpham.diff ; cmp
  output     : t20zk tren san pham HEAD: rc=3 `DO:t20zk_...:kho.pyc, bi danh=True: symlink treo chi voi toi qua bi danh thu muc phai DO kiem-re,
               dung mot dong: rc=0: ... kiem-re DAT (1 tep doi, 0 loi)` (chot fixture `t82_vap(...) is co_bi_danh` da QUA => t82 that su vap) ·
               sau va: t20zk rc=0; t98b, t98c, t20zi, t20zj, t96, t98, t99 rc=0 · tron bo: `CA: 100/100 dat · 0 do · 0 hong` · `DOT BIEN: 367/367
               bi giet dung ly do` · `KIEM KE: ... hanh_vi=70 ... ops/ci_duong_nhanh.py=198 ... = 367` · `TU KIEM PHAN HANG: DAT` · `TONG: DAT` rc=0
               (2m30s) · registry `23/23`, `1025/1025` · ruff `All checks passed!` · doctrine-scan sach · AST san pham chi khac `followlinks=True` ·
               H3 (theo link nhung loc bo symlink thu muc) GIET · H4 (nuot vong im lang) GIET · H5 (bo moi bi danh tro thu muc ten bi bo qua) GIET ·
               H6 (CHI khong theo bi danh toi `__pycache__`) GIET o nhanh `__pycache__` · H7 (CHI ten `*.pyc`) GIET o nhanh `kho.pyc` (tmp/m17/hint_rang2.py) ·
               vong `ops/specs/vong -> .`: 1 dong TREO tai phan tu thu 41 (nhan tu choi phan giai), 0,003 s · patch ap sach, cmp == ban da thu ·
               sha256(out/HINT.patch) = d6a4b71f39660ce09019f8146bd352d48eee7ed3c46b5a4c159bc174d3d42f19 ·
               sha256(tmp/hint17_sanpham.diff) = 5305c50655b3109f64226dde683f47e56f65ad095003e163f5a69e8b7e38af1f
  ket luan   : KHONG PHAI LOI (HINT do duoc, da thu tren ban sao; chua chay tren cay that)

HUONG 11: khang dinh dinh tinh MOI cua ban va do duoc TAI CHO (neo PR trong D1/t20p, gitlink, t20x)
  gia thuyet : neu neo "PR #667 merge 3fee59e, PR #670 merge dcd5fe0" khong phai merge cua hai PR ay, hoac hai PR khong them `.gitattributes`
               `-whitespace`, hoac clone khong de lai thu muc rong cho gitlink, thi cau moi SAI
  lenh       : git log -1 --format='%H %P%n%s' 3fee59e|dcd5fe0 ; git diff --name-only --no-renames <c>^1...<c>^2 (dem, loc `.gitattributes`,
               loc ngoai allowlist) ; git show 41508cd:<hai .gitattributes> ; (tmp/gl17, GIT_CONFIG_GLOBAL=/dev/null) git init; update-index
               --add --cacheinfo 160000,<sha>,ops/specs/con; commit; git clone; ls -la ; doc than t20x
  output     : 3fee59e = `Merge PR #667: bookkeeping(#650) ...` (20 tep, `ops/reviews/bookkeeping-650-pr667/.gitattributes`, 0 tep ngoai allowlist) ·
               dcd5fe0 = `Merge PR #670: bookkeeping(#650) ...` (28 tep, `ops/reviews/bookkeeping-650-pr670/.gitattributes`, 0 ngoai) · ca hai tep:
               `luot*-VERDICT.md -whitespace`, `luot*-verdict-day-du.md -whitespace` · tep thu ba `land-doc-receipt-thu-hoi-c1a1a/.gitattributes`
               KHONG duoc cau moi nhac (cau la khang dinh TON TAI, khong phai "ca ba") · gitlink: `ops/specs/con` la thu muc, 0 muc ben trong ·
               t20x: `git -c core.symlinks=false checkout -- <duong>` roi kiem-re
  ket luan   : KHONG PHAI LOI

## BANG DO (khang dinh -> nguon khai -> do duoc -> khop?)
Danh sach khang dinh dinh luong/dinh tinh do duoc lay tu CHINH bo quet t98b/t98c (tmp/m17/liet_ke.py: 17 so san pham + 4 so tep test, 29 cau nhac nen)
cong cac cau dinh tinh moi cua ban va va chu thich ci.yml do packet them (t98b/t98c KHONG quet ci.yml).

| khang dinh | nguon khai | do duoc (HUONG) | khop? |
|---|---|---|---|
| CA 99/99, DOT BIEN 366/366, TU KIEM DAT, TONG DAT | commit 41508cd, PROMPT | 99/99 · 366/366 · DAT (5 mau rc, 3 dot bien that) · DAT, rc=0 (1) | co |
| registry 23/23 + 1025/1025; numstat `ci_dang_ky_test.py` so master `1 0` | commit, nghiem thu 9 | 23/23 · 1025/1025; nen master 22/22 · 1025/1025; `1 0` (so 1741e0a `172 6`) (3) | co |
| san pham CHI docstring/chu thich, AST bo docstring giong het | commit 41508cd | `cf27fd5f9f81` tai 3569472 = 91cd2f7 = 41508cd (1) | co |
| ruff F delta 0 | commit | tl.py 12 F821 (= nen; tl.py khong doi); hai tep moi sach (1) | co |
| TOAN BO 345 merge first-parent toi 1741e0a, 63 chi ho so, 8/63 truot `--check` | D1 | 345 (khong -n) = 345 (-n 400), 345/345 hai cha; 63; 8 (8) | co |
| ~13% (8/63 tai 1741e0a) | D1 | 12,7% | co |
| 0/1991 tep duoi allowlist la nhi phan tai 3569472cb9 | D1, `kiem_nhi_phan`, t20s | 1991; 0 co va khong `--attr-source` (8) | co |
| 119 tep lease tai 3569472cb9; MOT ref 6/119 truot, ca 6 `CHAN [8]` bia mo | D2 | 119; `{(8, True): 6}` tren kho dung mot ref (8) | co |
| 529 ref cuc bo cho 0/119 | D2 | KHONG DO DUOC (cay-kho 5 ref, kho.git 4) — da khai "chua doi chieu ls-remote" | — |
| PR #667 merge 3fee59e, PR #670 merge dcd5fe0 them `.gitattributes` `-whitespace` duoi `ops/reviews/` | D1, t20p | dung ca hai: subject merge, tep them, noi dung `-whitespace`, diff toan allowlist (11) | co |
| ~7 giay ba ca du lieu (Python 3.11, phu thuoc may) | `kiem_ca_du_lieu` | 7,4 / 7,7 / 7,9 s, 4 CPU, 3.11.15 (8) | co |
| khai 38/12/3, do 35/12/3/3 tai 7b8c856 | t96 docstring | 53 ca `{'t': 38, 'y': 12, 'k': 3}`; t97/t98/t99 tu kiem -> 35/12/3/3 (8) | co |
| 52 phut `gate (ubuntu-latest)` (run 36518707072) | docstring module | KHONG DO DUOC (khong mang); co neo run | — |
| 360 phut (comment 5889513175); "360 phut mac dinh" | y16; chu thich ci.yml | KHONG DO DUOC; mac dinh 360 phut khop tai lieu GitHub theo hieu biet reviewer | — |
| "ba context bat buoc" | chu thich ci.yml `chuan-bi` | theo dac ta r2 (BAT_BUOC = gate, gate-ops, gate-packet-loop); ruleset that KHONG DO DUOC | co (theo dac ta) |
| "4 luot that" (Issue #674 comment 5889459132) | chu thich ci.yml, y01, RUN_BUOC_PACKET | KHONG DO DUOC; co neo comment | — |
| gitlink: clone de lai THU MUC rong (git cuc bo) | `kiem_mode_git`, `_commit_gitlink`, t20v | clone cuc bo: `ops/specs/con` la thu muc, 0 muc (11) | co |
| `t20x` do bang git that (`core.symlinks=false`) | `kiem_mode_git` | than t20x: `git -c core.symlinks=false checkout` roi kiem-re (11) | co |
| `t191` doi DUNG MOT chot duoc mien | D2 | docstring t191 `ops/lease_publish_test.py:9782`: "Đúng MỘT chốt được miễn sẵn (chốt hạn)" (9) | co |
| khong buoc `actions/checkout` nao khai `ref:`; `y13` khoa `with:` moi buoc | docstring module | 7 checkout, `with:` chi `fetch-depth: 0`/rong; dot bien them `ref:` -> y13 GIET (9) | co |
| `y02`, `y03`, `y06` khoa dang bieu thuc / buoc nang mang if / job khong bi bo | docstring module | N6b, N6c -> y03 GIET (2); dot bien harness y02 (1), y06 (8) trong 366/366 | co |
| `t20c`, `t20r` do duoi dung `core.whitespace` cua kiem-re; `t20p` do nhieu do sau, `binary`/`-diff` tat `--check` | D1 | ca hai goi `kiem_re` (CAU_HINH_WHITESPACE); t20p 4 thu muc (do sau 1-4 duoi `ops/`), fixture doi `--check` tho rc=0 voi tung thuoc tinh | co |
| `t21b` do ca bon vi tri tren `lease_publish` that | D2 | PHAM_VI_BIA_MO 4 khoa; D1, D3 cua toi GIET (6) | co |
| "Lech mot trong hai chieu (ma doi pham vi, HOAC docstring noi rong ra) => DO" | docstring t21b | ma doi pham vi -> DO; docstring THAY cum -> DO; docstring THEM cau mau thuan, giu nguyen hai cum -> XANH (D2) (6) | **mot phan** — ghi chu, khong nang hang |
| "symlink treo chi voi toi QUA symlink thu muc tro ra ngoai cay thi t82 vap ma chot nay khong thay"; "pham vi duyet va cho no khong toi duoc ghi o docstring ham" | docstring ham `kiem_symlink_treo_ca_cay`, docstring module | co che DUNG; liet ke THIEU bien the TRONG cay (bi danh -> thu muc ten bi bo qua) do duoc kiem-re rc=0 / t82 vap; bien the ra ngoai cay khong dung duoc tu noi dung kho tren runner (5) | **KHONG** -> finding P3 |
| ci.yml "cong DUY NHAT canh `if:` cap job/buoc sau G5"; test "\"Duy nhat\" chi DO toi hai cong" | chu thich ci.yml, docstring module test | dot bien `if:` sau G5 lot ci_dang_ky_test, workflow-audit, ci_phamvi_test, doctrine-scan (9) | co (khong vet can) |
| 29 cau nhac nen co nhan "theo tai lieu"/"chua tu do"/"KHONG DO DUOC" | hai tep | khong cau nao nguoc tai lieu theo hieu biet reviewer (4) | KHONG DO DUOC truc tiep (khong mang) |
| t98b/t98c on dinh theo phien ban Python | — | JSON quet giong het 3.11/3.12/3.13 (4) | co |
| head 41508cd la commit co chu ky | PROMPT | khoi `gpgsig` SSH co mat; xac minh KHONG DO DUOC (khong allowedSignersFile) | mot phan |
| DO_LAI "AL_VER: 4 dong" | goi/DO_LAI.md | HEAD 5 = master 20ec8d5 (1741e0a: 4) | KHONG (ngoai kho) |
| DO_LAI "938/938" | goi/DO_LAI.md | 1025/1025 HEAD va master | KHONG (ngoai kho) |
| DO_LAI "lease 6/113 (clone MOT ref) vs 0/113 (552 ref)" | goi/DO_LAI.md | 119 tep; 6/119 mot ref | KHONG (ngoai kho) |
| DO_LAI "`git diff --numstat 1741e0a HEAD -- ci_dang_ky_test.py` (mong 1 0)" | goi/DO_LAI.md | `172 6`; so master `1 0` | KHONG (ngoai kho) |
| DO_LAI "G5 chiem 46,5 phut / 52 phut" | goi/DO_LAI.md | KHONG DO DUOC (khong mang) | — |

## NGHIEM THU (SPEC-r2) — bang chung TU CHAY luot nay
| # | ket qua | bang chung |
|---|---|---|
| 1 | dat | N1 (toan allowlist -> DAY_DU) -> t01 rc=3 GIET (HUONG 2) |
| 2 | dat | N2 (khop them `scripts/` qua `or startswith`) -> t02 GIET; harness `noi_allowlist_them_scripts` trong 366/366 |
| 3 | dat | N3 (KHONG DO DUOC -> DUONG_NHANH) -> t05, t06 GIET |
| 4 | dat | N4 (goi `git rev-parse --git-dir` truoc kiem su kien) -> t03 GIET |
| 5 | dat | N5 (them `.github/`) -> t08 GIET |
| 6 | dat | N6a (go `if:` pull_request buoc phan loai) -> y01; N6b (`release-check full` `if: ${{ false }}`) -> y03, y04, y12; N6c (`== 'day_du'`) -> y03, y12; + 74 dot bien ci.yml trong 366/366 |
| 7 | dat | N7 (`paths-ignore` duoi pull_request) -> y05 GIET |
| 8 | dat | actionlint rc=0 (shellcheck 0.9.0); bieu thuc rong trong chu thich than `run:` -> rc=1 `[expression]` (HUONG 3); toan workflow delta 0 (HUONG 9) |
| 9 | dat | nen master 22/22 -> HEAD 23/23 (1025/1025 ca hai); go DA_NOI -> `test sống chưa đăng ký` (23/22); go loi goi CI -> `CI không gọi mục đăng ký`; numstat so master `1 0` |
| 10 | dat | `== tl selftest 1715/1715 ==` rc=0 (ban sao nt10, core.abbrev 7); ruff F tl.py 12 = nen |
| 11 | chua_do_duoc | can PR that; commit KHONG khai dat |

## FINDINGS

### buoc-bi-bo-doc-ca-cay-khong-chi-ba-ca  [P3]  Bo duyet symlink treo KHONG theo symlink thu muc trong khi `t82` theo: bi danh thu muc TRONG cay toi thu muc ten bi bo qua de lot symlink treo (PR ho so xanh, t82 do tren master); gioi han tu khai chi ra bien the khong dung duoc va bo sot bien the dung duoc
TEP/DONG: `ops/ci_duong_nhanh.py:317` (`os.walk(kho, onerror=khong_doc_duoc)` — mac dinh `followlinks=False`); docstring ham `:300-310` (cau
  "Giới hạn, chưa có ca" `:307-309`); docstring module `:51-52` ("phạm vi duyệt và chỗ nó không tới được ghi ở docstring hàm");
  `ops/ci_duong_nhanh_test.py` (khong ca nao co bi danh thu muc; DOT_BIEN `:3130`, `:3137` neo vao dong `os.walk`).
VAN DE: Bat bien cua lop (luot 8b/15): tap symlink ma kiem-re duyet phai BANG tap ma `t82` cua `lease-publish selftest` (buoc bi bo) cham toi.
  `t82` goi `shutil.copytree(HERE.parent, goc, ignore=ignore_patterns(".git", "__pycache__", "*.pyc"))` khong `symlinks=True`
  (`ops/lease_publish_test.py:3159`), nen THEO symlink thu muc va ap mau bo qua THEO TEN o tung cap; `os.walk` mac dinh KHONG theo.
  Hai bo duyet trung nhau khi cay khong co symlink thu muc, lech nhau khi co. Do (HUONG 5, kho tam, moi duong dich TRONG cay):
  thu muc ten bi bo qua (`kho.pyc` hoac `__pycache__`) chua symlink `s` toi tep allowlist + symlink thu muc bi danh toi thu muc ay; PR ho so
  `git rm` tep dich -> phan loai `duong_nhanh`, kiem-re rc=0 (0 dong TREO), copytree kieu t82 `shutil.Error`. Doi chung khong bi danh: ca
  hai cung bo qua, khop. Tuc PR ho so XANH, `t82` DO tren master o luot push — dung hinh dang P2 cua lop luot 8b.
  Gioi han executor tu khai dung CO CHE nhung chi ra bien the "symlink thu muc tro RA NGOAI cay" — bien the nay KHONG dung duoc tu noi dung
  kho tren runner (bi danh treo da bi t20zi E1b bat; noi dung thu muc ngoai cay PR khong quyet; SUY LUAN — khong dung duong thoat cay theo
  luat) — va BO SOT bien the TRONG cay dung duoc, trong khi docstring module noi danh sach "cho no khong toi duoc" nam o docstring ham.
  Dieu kien tien quyet (ly do hang P3, khong P2): PR ho so KHONG tu tao duoc (khong them duoc symlink — `kiem_mode_git` chan 120000 tren
  ca ba cap, `kiem_loai_tep` chan tren dia: t20n/t20q); master phai co SAN hai symlink (bi danh + symlink trong thu muc ten bi `.gitignore`
  bo qua, can `git add -f`) vao qua PR day du — HEAD hien co 0 symlink (do). Hau qua phat hien duoc o luot push master (luon day du).
DA THU VA: co — mot tu khoa san pham + docstring (khoi diff duoi, executor tu ap) VA `out/HINT.patch` (CHI tep test, nhan nguyen van
  "chua chay tren cay that — executor tu ap, tu do, tu chiu trach nhiem commit"). HAI phan PHAI ap CUNG nhau: ba dot bien
  `symlink_treo_chi_cap_goc`, `symlink_treo_nuot_loi_duyet`, `symlink_treo_khong_theo_bi_danh` neo vao dong `os.walk` MOI.
```diff
--- ops/ci_duong_nhanh.py
+++ ops/ci_duong_nhanh.py
@@ -48,8 +48,8 @@
 LỆNH `kiem-re` (bước bù cho các bước bị bỏ, chỉ chạy khi `che_do == duong_nhanh`):
   YAML parse được · `git diff --check` · lease đổi phải qua `lease_publish` · ba ca kiểm DỮ LIỆU của lease_publish_test ·
   mọi đường dẫn đổi là TỆP THƯỜNG theo MODE TRONG GIT (`kiem_mode_git`: 100644/100755 hoặc xoá; gitlink, symlink ⇒ ĐỎ) ·
-  KHÔNG symlink treo trong cây ĐĨA, kể cả ngoài diff (`kiem_symlink_treo_ca_cay`: `t82` của bước bị bỏ chép CẢ cây; phạm vi
-  duyệt và chỗ nó không tới được ghi ở docstring hàm).
+  KHÔNG symlink treo trong cây ĐĨA, kể cả ngoài diff (`kiem_symlink_treo_ca_cay`: duyệt như `t82` của bước bị bỏ — CẢ cây,
+  THEO symlink thư mục; chi tiết ở docstring hàm).
 Hai chỗ khác chữ trần của đặc tả r2, ĐO ngày 29-09-2026. CHỦ KHO ĐÃ DUYỆT CẢ HAI (lựa chọn (a)) — erratum của đặc tả r2,
 không sửa r2: https://github.com/ducthangho/tra-luat/issues/674#issuecomment-5887720007 . Với reviewer: đây là HÀNH VI ĐƯỢC
 DUYỆT, không phải finding về chính sách; vẫn tìm lỗi TRONG cách hiện thực (ví dụ `bo_qua_han` bỏ thêm chốt nào khác không,
@@ -303,10 +303,12 @@
     qua PR đầy đủ, ở `docs/`, dưới allowlist hay trong thư mục chấm) — hoặc xoá hết một thư mục hồ sơ mà đường dẫn symlink
     đi XUYÊN qua — làm symlink ấy treo trong khi nó KHÔNG nằm trong diff ⇒ PR xanh, `t82` ĐỎ trên master (đo 01-10-2026).
     Treo đo bằng `os.path.exists` (stat của nhân, theo từng thành phần), KHÔNG bằng ghép đường dẫn từ vựng: `a/b/../c` cần
-    `a/b` có thật. `os.walk` xếp symlink treo vào danh sách TỆP (kể cả symlink từng trỏ thư mục) và không đi vào symlink thư
-    mục. Giới hạn, chưa có ca: `t82` (copytree không `symlinks=True`) thì CÓ theo vào symlink thư mục, nên symlink treo chỉ
-    với tới được QUA một symlink thư mục trỏ ra ngoài cây thì `t82` vấp mà chốt này không thấy (đo 01-10-2026 trên kho tạm:
-    copytree ném `shutil.Error`, os.walk không liệt kê). Không đọc được một thư mục ⇒ KHÔNG ĐO ĐƯỢC ⇒ ĐỎ. Không lệnh git
+    `a/b` có thật. `os.walk` xếp symlink treo vào danh sách TỆP (kể cả symlink từng trỏ thư mục). Duyệt THEO symlink thư mục
+    (`followlinks=True`) vì `t82` (copytree không `symlinks=True`) cũng theo: symlink treo chỉ với tới được qua một bí danh
+    thư mục — trỏ vào thư mục tên bị bỏ qua (`*.pyc`, `__pycache__`) hay ra ngoài cây — làm `t82` vấp, nên ở đây cũng ĐỎ
+    (`t20zk` đo bí danh trong cây, cross-review lượt 17). Vòng symlink thư mục: đường dẫn dài dần tới khi nhân từ chối phân
+    giải, phần tử cuối hiện ra như symlink TREO ⇒ ĐỎ, không lặp vô hạn (`t20zk` đo; `t82` cũng vấp). Không đọc được một thư
+    mục ⇒ KHÔNG ĐO ĐƯỢC ⇒ ĐỎ. Không lệnh git
     nào: đây là cây ĐĨA mà `t82` sẽ chép."""
     bo_qua = shutil.ignore_patterns(*BO_QUA_NHU_T82)
     loi = []
@@ -314,7 +316,7 @@
     def khong_doc_duoc(e):
         loi.append(f"KHONG DO DUOC: khong duyet duoc cay de tim symlink treo: {type(e).__name__}: {getattr(e, 'filename', '')!r}")
 
-    for goc, thu_muc, tep in os.walk(kho, onerror=khong_doc_duoc):
+    for goc, thu_muc, tep in os.walk(kho, onerror=khong_doc_duoc, followlinks=True):
         bo = bo_qua(goc, thu_muc + tep)
         thu_muc[:] = sorted(d for d in thu_muc if d not in bo)
         for ten in sorted(t for t in tep if t not in bo):
```
  CHOT RIENG cho tung duong vao (ca `t20zk_kiem_re_symlink_treo_qua_bi_danh_thu_muc_do` trong HINT.patch, chen truoc t20r):
  (b) bi danh -> `kho.pyc` (khop `*.pyc`): nhanh con `("kho.pyc", True)` — fixture tu chung minh `t82_vap(...) is co_bi_danh` (copytree THAT),
      roi doi kiem-re rc=1 voi DUNG mot dong TREO `'ops/land/bd/s'`. Dot bien: `symlink_treo_khong_theo_bi_danh` (harness, `followlinks=True`
      -> mac dinh) GIET; H3 cua toi (theo link nhung loc bo symlink thu muc) GIET; H5 (bo moi bi danh tro thu muc ten bi bo qua) GIET.
  (b') bi danh -> `__pycache__`: nhanh con `("__pycache__", True)`. Rang RIENG: H6 cua toi (CHI khong theo bi danh toi `__pycache__`) DO
      dung nhanh `__pycache__, bi danh=True`; doi xung H7 (CHI khong theo bi danh toi ten `*.pyc`) DO dung nhanh `kho.pyc, bi danh=True`.
  (c) bi danh -> `.git`: cung phep duyet nen dong theo kien truc; PR khong tao duoc symlink trong `.git` => khong co ca rieng (noi thang).
  (d) bi danh RA NGOAI cay (bien the executor khai): cung phep duyet nen dong theo kien truc. Ca rieng can dung mot symlink tro ra ngoai kho
      tam — reviewer KHONG soan; MO TA BANG LOI cho phien dieu phoi: trong ca, tao mot thu muc ANH EM cua kho tam (ngoai cay) chua mot symlink
      tro toi mot tep duoi `ops/land/` cua kho; commit vao kho mot symlink thu muc tro toi thu muc anh em ay; PR ho so xoa tep dich; mong:
      kiem-re DO dung mot dong TREO duoi duong dan bi danh, copytree kieu t82 vap; dot bien `followlinks=True` -> mac dinh phai lam ca ay DO.
  (e) vong symlink thu muc: nhanh con cuoi (`ops/specs/vong -> .`): fixture doi t82 vap; mong kiem-re co dong DO chua `ops/specs/vong`, KHONG
      lap vo han (do: 1 dong TREO o phan tu thu 41, 0,003 s). Dot bien H4 cua toi (nuot vong im lang) GIET.
  Doi chung (chong bao thua): `("kho.pyc", False)` khong bi danh -> DAT; PR sua tep khac (co bi danh) -> DAT.
DA THU NGHIEM: (truoc va) t20zk tren san pham HEAD rc=3 dung chot bi danh; (sau va, ban sao tmp/hint17) `CA: 100/100` · `DOT BIEN: 367/367 bi
  giet dung ly do` · `TU KIEM PHAN HANG: DAT` · `TONG: DAT` rc=0; t20zi/t20zj/t98b/t98c/t96/t98/t99 xanh; registry 23/23 · 1025/1025; ruff sach;
  doctrine-scan sach; AST san pham chi khac `followlinks=True`; H3/H4/H5/H6/H7 GIET; `patch -p0 --fuzz=0` hai tep ap sach tren `git archive 41508cd`,
  cmp == ban da thu (HUONG 10). sha256(out/HINT.patch) = d6a4b71f39660ce09019f8146bd352d48eee7ed3c46b5a4c159bc174d3d42f19.
  Gioi han cua HINT: khong ca nao cho (d) (ly do o tren); khong do tren Windows (buoc selftest packet chi Linux; nen Windows checkout
  symlink thanh tep thuong); hanh vi t82 tren runner KHONG DO DUOC (do bang copytree cung loi goi tren may nay).
DO TIN: cao (moi phep do chay that; co che doc tu ma t82 va do bang copytree that); hang P3 la danh gia (dieu kien tien quyet hiem, hau qua
  lo ra o luot push master).

## KHANG DINH BANG DO (`goi/DO_LAI.md`) BO SOT — finding THONG TIN cho phien dieu phoi, KHONG xep hang vao packet
Theo PROMPT, moi khang dinh dinh luong bang do bo sot duoc bao o day; tat ca da DO (BANG DO) va KHOP, hoac KHONG DO DUOC co neo/nhan, nen
khong co loi nao cua packet di kem: 0/1991 nhi phan tai 3569472cb9 · 119 tep lease + 6/119 mot ref (bang do van ghi 6/113 vs 0/113) · neo
PR #667/#670 · ~7 giay ba ca du lieu · 38/12/3 vs 35/12/3/3 tai 7b8c856 · 360 phut (y16, chu thich ci.yml) · "ba context bat buoc" ·
"4 luot that" · gitlink clone -> thu muc rong · `t191` dung mot chot mien · khong checkout nao khai `ref:` + `y13` khoa `with:` · t21b bon
vi tri · "cong DUY NHAT" sau G5 · 29 nhan "theo tai lieu". Chu thich ci.yml do packet them KHONG nam trong pham vi t98b/t98c (chi quet hai
tep Python) — hien khong co so do sai trong do.

## GHI CHU CHO PHIEN DIEU PHOI (ngoai kho, khong tinh vao packet)
`goi/DO_LAI.md` van 4 dong cu ma luot 15 va 16 da chi (CHUA VA): "AL_VER: 4 dong" -> 5 (HEAD = master 20ec8d5; 1741e0a: 4); "938/938" ->
1025/1025 (HEAD va master); "lease 6/113 (clone MOT ref) vs 0/113 (552 ref)" -> "6/119 tai 3569472cb9 (mot ref); 6/113 tai 1741e0a";
"`git diff --numstat 1741e0a HEAD ...` (mong 1 0)" -> `git diff --numstat 20ec8d5 HEAD -- .claude/dev/ci_dang_ky_test.py` (mong `1 0`; so
1741e0a la `172 6`).

## DOT BIEN SONG SOT (cua toi, tren HEAD)
- Dung gioi han executor TU KHAI: B8 (gan nguon, t98b (b)), B9 (luong tu, t98b (b)), C3 (khang dinh sai co nhan "theo tai lieu", t98c (b)).
- Ngoai danh sach duong vao tu khai, KHONG nang hang (rang bo kiem tai lieu; khong che khang dinh sai nao): B3 (`MAU_SO_CHU_KHO` `\s+` ->
  mot khoang trang: tu-so cuoi dong + danh tu dong sau), C4 (t98c nhan MOI con so la neo), C5 (t98c nhan chu `do`/`đo` tran la nhan),
  C6 (`Github` lot `MAU_NHAC_NEN`), D2 (t21b chi do su CO MAT cua hai cum; them cau mau thuan thi xanh).
- Mutant cua harness: 366/366 `bi giet dung ly do` (khong song sot).
- Truoc HINT, bien the symlink bi danh (HUONG 5) la mot "dot bien hanh vi" SONG o muc he thong (kiem-re rc=0, t82 vap); sau HINT: GIET.

## GHI CHU QUY TRINH
- Moi ghi chi trong $R (tmp/, out/). `cay-kho` khong bi sua (`git status --short` rong truoc/sau suite). Khong commit/push/checkout trong kho
  that; khong mang; khong cong cu GitHub. Mot lenh co `rm -rf` bi he thong quyen tu choi -> bo, dung thu muc moi.
- Ban sao: tmp/nt10, tmp/hint17, tmp/dn2 (cp -a); tmp/nt8, nt9a, nt9b, nt9m, tmp/duynhat, tmp/hint_chk17 (git archive); tmp/lease17 (archive
  + alternates, DUNG mot ref, khong checkout); tmp/gl17 (kho git tam gitlink); cay tam cua harness (dung_cay_tam) tu xoa.
- Rig cua toi: tmp/ast/so_ast.py, tmp/m17/{rig,nt,dc,y13,hint_rang,hint_rang2,liet_ke,chat,symlink_bidanh,lam_hint}.py, tmp/lease17/do17.py.
  Log: tmp/logs/{suite_head,selftest,suite_hint17,do_lai_so,t20zk_head,t20zk_fix,phamvi_*,al_*}.log/txt; ket qua dot bien tmp/m17/*.json.
- KHONG DO DUOC: hanh vi that tren GitHub Actions (ref cua checkout fetch-depth 0, PR that, nghiem thu 11, windows-latest), noi dung tai lieu
  GitHub (khong mang — doi chieu theo hieu biet), so 529/552 ref, chu ky SSH cua head, model/effort thuc chay cua chinh luot nay.
- Danh tinh: Claude Opus 5.5, CUNG HO executor => `advisory_review`, KHONG phai cross_approved.

So lop: 10 — 1 MO: `buoc-bi-bo-doc-ca-cay-khong-chi-ba-ca` (P3, mo lai voi bang chung moi); 9 DONG: `bang-do-thieu-neo-va-thieu-kiem-ke`, `khang-dinh-dinh-tinh-rong-hon-phep-do`, `kiem-mode-git-chot-khong-rang`, `kiem-re-cua-fail-close-chua-co-ca`, `kiem-re-bi-cau-hinh-boi-du-lieu-ho-so`, `phan-loai-khong-neo-merge-ref-that`, `cau-khai-skipped-nguoc-phep-do`, `dependency-failure-skips-required-checks`, `kiem-re-phu-thuoc-actor-su-kien`.

TONG: P0=0 P1=0 P2=0 P3=1 — so lop: 10 (1 mo, 9 dong)
