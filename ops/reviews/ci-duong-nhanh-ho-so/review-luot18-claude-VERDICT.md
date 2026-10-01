verdict: approve
reviewed_sha: 46bc11de82fab227e29e1bc0e057fcf3895e5fe1
Reviewed commit: 46bc11de82fab227e29e1bc0e057fcf3895e5fe1

> luot 18 (packet #674, g4; dac ta r2 sha256 b6e719c9…da57 KHOP; r1 e6949841…c64c KHOP). TRANG THAI: XONG — 11 huong + doi chieu.
> Ket luan: 0 finding xep hang. Finding P3 duy nhat cua luot 17 (`buoc-bi-bo-doc-ca-cay-khong-chi-ba-ca`, bi danh thu muc trong cay)
> DA VA THAT (bien the cua toi do tren HEAD va 41508cd); bat bien moi "bo duyet di DUNG duong copytree cua t82" dung tren 6400 cay ngau
> nhien. Con 3 dot bien CUA TOI song, deu nam tren gioi han da tu khai / khong co duong vao tu PR (xem DOT BIEN SONG SOT) — khong xep hang.
> Reviewer: Claude Opus 5.5, CUNG HO voi executor => `advisory_review`, KHONG phai cross_approved; packet `sensitive` van can Codex
> `cross_approved` hoac `human_audited` o cong land. Model/effort thuc chay: KHONG DO DUOC.

## DOI CHIEU LUOT TRUOC
Moi dong co phep do CUA TOI (bien the khac ca cua executor / dot bien khac harness), tren ban sao hoac kho tam; cay-kho khong bi sua.

| luot · finding · duong vao | hang cu | trang thai | bang chung TU DO |
|---|---|---|---|
| 17 · `buoc-bi-bo-doc-ca-cay-khong-chi-ba-ca` (b) bi danh thu muc TRONG cay toi thu muc ten bi bo qua (`*.pyc`, `__pycache__`) | P3 | **DA VA THAT** | tmp/r18/doi_chieu_l17.py, ba bien the KHAC t20zk: V1 bi danh NGOAI allowlist (`docs/bd -> kho.pyc`), V2 bi danh HAI tang (`a1 -> a2 -> tm.pyc`), V3 bi danh trong thu muc CHAM (`.cham/bd -> ../ops/reviews/__pycache__`); PR ho so `git rm` dich. HEAD: `duong_nhanh`, t82 `VAP`, kiem-re rc=1, dong TREO dung tung cai (`'docs/bd/s'` · `'ops/specs/a1/s'`+`'ops/specs/a2/s'` · `'.cham/bd/s'`), doi chung PR sua tep khac rc=0. CUNG kich ban tren 41508cd: kiem-re rc=0, 0 dong TREO (lot) => loi co that truoc va, da dong (HUONG 9) |
| 17 · cung lop (c) bi danh -> `.git` | — (cung co che) | DONG theo kien truc | cung phep duyet `followlinks=True`; PR khong tao duoc symlink trong `.git` (khong ca rieng, noi thang nhu luot 17) |
| 17 · cung lop (d) bi danh tro RA NGOAI cay | — (giao phien dieu phoi o luot 17) | **VAN CHUA CO CA** — dung gioi han executor tu khai, KHONG xep hang | dot bien CUA TOI H11b (bo theo bi danh co realpath ngoai goc cay, bien chat) SONG truoc ca 7 ca lop (HUONG 8): khong ca nao do duong vao nay. Mo ta bang loi cho phien dieu phoi: xem muc GHI CHU CHO PHIEN DIEU PHOI |
| 17 · cung lop (e) vong symlink thu muc | — | **DA VA THAT** (nang cap: phat hien theo to tien) | do HUONG 6: hai vong ve goc — copytree va bo duyet goi y luot 17 deu HET_GIO 15 s, HEAD 2 dong VONG trong 0,0006 s; dot bien CUA TOI H4b/H9/H10/H13/H16 deu GIET o t20zm (HUONG 8) |
| 17 · gioi han tu khai cu ("chi bien the tro ra ngoai cay") | P3 (mot phan cua finding) | **DA VA THAT** | docstring moi liet ke bat bien + tung chot + gioi han (a)(b); moi so/khang dinh moi do lai KHOP (HUONG 6) |
| 16/15/14/8b va cac lop dong khac (`bang-do-thieu-neo-va-thieu-kiem-ke`, `khang-dinh-dinh-tinh-rong-hon-phep-do`, 7 lop cu) | DONG | van DONG | `ci.yml`, `ci_dang_ky_test.py` khong doi tu 41508cd; san pham ngoai `kiem_symlink_treo_ca_cay` khong doi (diff 41508cd..HEAD chi o ham ay + docstring module 3 dong); suite 104/104 · 383/383 tren 3.11 VA 3.12 (HUONG 1, 8); nghiem thu 1-10 bang dot bien cua toi (HUONG 4, 7) |
| GHI CHU luot 17 cho phien dieu phoi: `goi/DO_LAI.md` 4 dong cu | (ngoai kho) | **CHUA VA** (ngoai write set executor) | van "AL_VER: 4 dong" (do: 5), "938/938" (do: 1025/1025), "lease 6/113 vs 0/113" (do: 119 tep, 113 dat / 6 truot), "numstat 1741e0a HEAD (mong 1 0)" (do: `172 6`; so master `1 0`) |

## BANG LOP
| slug | bieu hien (duong vao da liet ke) | hang cao nhat con mo | phuong an va chung | phep kiem dong lop |
|---|---|---|---|---|
| `buoc-bi-bo-doc-ca-cay-khong-chi-ba-ca` | Bat bien: bo duyet cua `kiem_symlink_treo_ca_cay` di DUNG nhung duong `copytree(..., ignore=ignore_patterns(".git","__pycache__","*.pyc"))` cua t82 di, DO khi t82 vap. Duong vao co the gay lech, liet ke DOC LAP: (a) symlink treo ngoai diff o thu muc thuong/cham/allowlist/xuyen duong — DONG tu 8b (t20zi); (b) bi danh thu muc TRONG cay (toi ten bi bo qua, ngoai allowlist, hai tang, trong thu muc cham) — DA VA THAT (t20zk + HUONG 9); (c) bi danh -> `.git` — cung co che; (d) bi danh RA NGOAI cay — cung co che, CHUA CO CA (tu khai, giao phien dieu phoi tu luot 17; H11b song); (e) vong (tu vong, ve goc, hai buoc, hai vong ve goc) — DONG (t20zm, HUONG 6); (f) thu tu ap mau bo qua (ten muc o moi cap, khong len ten dich) — DONG (t20zl); (g) khu trung "da tham" — DONG (t20zn); (h) la phi-thuong (FIFO, socket, symlink->FIFO, qua bi danh) — DONG (t20zo), khong co duong vao tu PR; (i) cach goi copytree cua t82 troi — DONG (t20zj); (j) gioi han tu khai: tep khong doc duoc (do: co that, khong co duong vao tu git), thiet bi (chat hon, do), bung no khong vong (do: 2^k ca hai), duong dich qua dai (Linux: dich ngan hon nguon; Windows: KHONG DO DUOC), Windows junction (git khong tao). Buoc bi bo KHAC: golden/determinism/release-check chay that tren PR ho so — xanh (HUONG 11) | — (0) | — | fuzz vi sai 6400 cay: 0 do oan, 0 lot (HUONG 5); 21/21 cap dot bien harness chet o assertion KET QUA (HUONG 3); dot bien CUA TOI H3b/H4b/H8/H9/H10/H13/H16 GIET (HUONG 8); 3 bien the doi chieu do tren HEAD (rc=1) va 41508cd (rc=0) (HUONG 9) |
| `bang-do-thieu-neo-va-thieu-kiem-ke` | so moi trong van ban them luot nay: "qua han 15 s" (neo 41508cd + ban va goi y l17), chuoi 41/42 — deu do lai KHOP; t98b xanh | DONG | — | t98b trong 104/104; BANG DO |
| `khang-dinh-dinh-tinh-rong-hon-phep-do` | khang dinh dinh tinh moi: FIFO/socket, thiet bi "chua do", bung no "chua do", "khong doc duoc: KHONG DO DUOC" — nay deu DO DUOC va dung huong khai; cau ly do "git khong luu duoc loai tep ay" bo sot symlink->thiet bi (GHI CHU, khong dan toi hanh dong co hai) | DONG | (tuy chon) xem GHI CHU | HUONG 6, 10 |
| 7 lop cu (`kiem-mode-git-chot-khong-rang`, `kiem-re-cua-fail-close-chua-co-ca`, `kiem-re-bi-cau-hinh-boi-du-lieu-ho-so`, `phan-loai-khong-neo-merge-ref-that`, `cau-khai-skipped-nguoc-phep-do`, `dependency-failure-skips-required-checks`, `kiem-re-phu-thuoc-actor-su-kien`) | `ci.yml`, `ci_dang_ky_test.py`, phan loai khong doi tu 41508cd (AST: chi `kiem_symlink_treo_ca_cay` khac) | DONG | — | suite 104/104 · 383/383 (3.11 va 3.12); nghiem thu 1-10 bang dot bien cua toi (HUONG 4, 7) |

## SO DO NEN (@46bc11d, Linux, Python 3.11.15, git 2.43.0, actionlint 1.7.7 + shellcheck 0.9.0, ruff 0.16.9, TMPDIR=$R/tmp)
- `python3 -B ops/ci_duong_nhanh_test.py`: `CA: 104/104 dat · 0 do · 0 hong` · `DOT BIEN: 383/383 bi giet dung ly do` ·
  `KIEM KE: ca hanh_vi=74 + cau_truc_yaml=16 + so_dang_ky=3 + tu_kiem=11 = 104 · dot bien ci_dang_ky_test.py=2 + ci.yml=74 +
  ci_duong_nhanh.py=211 + ci_duong_nhanh_test.py=93 + lease_publish.py=3 = 383` · `TU KIEM PHAN HANG: DAT (5 mau rc, 3 dot bien that)` ·
  `TONG: DAT` · rc=0 · real 2m49s. `git status --short` truoc/sau: rong (0 byte ca hai).
- `python3 -B .claude/dev/ci_dang_ky_test.py`: `ĐĂNG KÝ: 23/23` · `PHẢN CHỨNG: 1025/1025 đỏ đúng` · `TỔNG: ĐẠT` · rc=0
- `actionlint .github/workflows/ci.yml` rc=0 · ruff F hai tep moi `All checks passed!` · tl.py `Found 12 errors` (= nen CLAUDE.md)
- `ci.yml`, `ci_dang_ky_test.py` KHONG doi tu 41508cd (`git diff --quiet` rc=0); 41508cd..46bc11d chi doi `ops/ci_duong_nhanh.py` (numstat `66 11`) va `ops/ci_duong_nhanh_test.py` (`307 15`); AST san pham bo docstring: 44 muc top-level, khac DUNG `kiem_symlink_treo_ca_cay`.

## BANG SAN
HUONG 1: so nen + loi khai commit 46bc11d ("CA 104/104, DOT BIEN 383/383, registry 23/23 + 1025/1025, ruff F delta 0")
  gia thuyet : neu loi khai rong hon phep do thi so in ra khac
  lenh       : python3 -B ops/ci_duong_nhanh_test.py ; python3 -B .claude/dev/ci_dang_ky_test.py ; actionlint ; ruff (xem SO DO NEN)
  output     : 104/104 · 383/383 · TU KIEM DAT · TONG DAT rc=0 ; 23/23 · 1025/1025 ; actionlint rc=0 ; ruff sach, tl.py 12 F821
  ket luan   : KHONG PHAI LOI

HUONG 2: chot "la phai la tep thuong" + chot vong co false-red tren cay THAT / PR ho so binh thuong khong (PROMPT: `.git`, `__pycache__`,
         tep rong, thu muc cham)
  gia thuyet : neu chot moi bao DO tren cay binh thuong (master, clone moi, cay co pycache that, FIFO/socket trong vung bo qua) thi moi
               PR ho so DO oan
  lenh       : git ls-tree -r <HEAD|20ec8d5|1741e0a> (dem mode) ; find cay-kho ! -type f ! -type d (ngoai .git) ;
               tmp/r18/cay_that.py (goi kiem_symlink_treo_ca_cay tren cay-kho, median 7 lan; so voi ban 41508cd) ;
               tmp/r18/e2e: git clone cay-kho, nhanh pr them `ops/specs/zz-e2e-luot18.md`, merge ref = merge-tree + commit-tree, checkout
               --detach merge ref, `python3 -B ops/ci_duong_nhanh.py` + `... kiem-re` voi 4 bien CI_DUONG_NHANH_* ;
               tmp/r18/vi_tri_bo_qua.py (clone MOI moi kich ban): import khong -B (pycache that), FIFO + socket trong `.git/`, socket trong
               `ops/__pycache__/`, FIFO ten `ops/zz.pyc`, tep rong, thu muc cham `.cham-zz/con/.an`; doi chung duong: FIFO trong `ops/specs/`
  output     : mode HEAD `2547 100644 + 14 100755`, master `2545 + 14`, 1741e0a `2428 + 13` — 0 symlink, 0 gitlink ; 0 muc phi-thuong ngoai .git ·
               cay that: `loi: []`, 147 thu muc / 2561 tep duyet, 0,0237 s (41508cd: 0,0208 s) · e2e: `che_do=duong_nhanh`, `kiem-re DAT (1 tep
               doi, 0 loi)`, real 7,98 s · K1 (moi vi tri bo qua cung luc): `[]` (pycache that co mat: `ops/__pycache__`) · K2 FIFO trong
               `ops/specs`: dung MOT dong `khong phai tep thuong ... 'ops/specs/zz-fifo'`
  ket luan   : KHONG PHAI LOI — khong false-red o moi vi tri PROMPT neu; doi chung duong DO dung. (Buoc truoc kiem-re trong gate-ops chi cai qua
               apt/pip vao he thong; `t82` chep vao `tempfile.mkdtemp` ngoai cay; actionlint vao `$RUNNER_TEMP` — doc ops/cai_cong_cu.sh,
               ops/cong_cu.yaml, ops/chay_lease_publish_test.sh.) Thoi gian khai trong commit "0,021s -> 0,028s": do 0,021 -> 0,024 s
               (cung bac, phu thuoc may; so chi o thong diep commit, khong o ma).

HUONG 3: moi dot bien MOI/neo lai cua harness chet DUNG ly do (harness chi doi `DO:<ca dich>:`, nen mot assertion "fixture vo hieu" trong
         cung ca cung duoc tinh GIET — tin dung gia tiem nang)
  gia thuyet : neu mot dot bien san pham lam ca dich do o assertion FIXTURE (vd `chep_nhu_t82(...)`, `phan_loai_that(...)`) thay vi
               assertion ve ket qua cua chot, thi "GIET" la tin dung gia
  lenh       : tmp/r18/ly_do.py (exec CHINH tep test; dung_cay_tam + chay_con + phan_hang cua no) cho 19 dot bien: 17 moi + 2 neo lai
               (`symlink_treo_chi_cap_goc`, `symlink_treo_nuot_loi_duyet`); in dong `DO:` cuoi cua tung ca dich
  output     : 21/21 cap (dot bien, ca dich) `GIET`, dong DO deu la assertion KET QUA cua chot: vd `symlink_treo_khong_theo_bi_danh` ->
               t20zk "kho.pyc, bi danh=True: ... phai DO kiem-re ... rc=0" va t20zo "FIFO qua bi danh: ... []" · `vong_khong_phat_hien` ->
               t20zm "tu vong: ... [symlink TREO ... 'ops/specs/vong/vong/.../vong']" (41 phan tu) · `vong_chi_so_thu_muc_cha` -> "vong ve
               goc" · `vong_bao_ca_tham_lai_khong_vong` -> "doi chung: bi danh KHONG vong ... phai DAT: [VONG ... 'ops/specs/a']" ·
               `chuoi_khu_trung_da_vao_toan_cuc` -> t20zn "nguoc: ... []" · `la_cho_phep_socket` -> "socket: ... []" · `la_khong_theo_symlink`
               -> "symlink toi FIFO: ... []" · ba `dong_bo_t82_*` -> dung nhanh tu kiem (c) tuong ung. KHONG dot bien nao chet o "fixture vo hieu".
  ket luan   : KHONG PHAI LOI (tep tmp/r18/ly_do_1.jsonl, ly_do_2.jsonl)

HUONG 4: nghiem thu 1-9 cua SPEC-r2 bang phep do CUA TOI + pham vi diff + chu ky
  gia thuyet : neu mot nghiem thu khong co rang thi dot bien cua toi (khac harness) song; neu diff mang tep la thi blob lech master
  lenh       : tmp/r18/nt.py (dot bien N1..N7 cua toi tren dung_cay_tam, doi chung ca dich xanh truoc) ; tmp/nt8 (git archive HEAD) chen dong chu
               thich chua bieu thuc rong (dau `$` dung bang chr(36)) vao than run buoc kiem-re roi actionlint ; tmp/nt9a go dong DA_NOI ;
               tmp/nt9b doi `run: python ops/ci_duong_nhanh_test.py` ; tmp/nt9m = git archive 20ec8d5 ; numstat ; so blob HEAD:<f> vs 20ec8d5:<f>
               cho moi tep cua `git diff 1741e0a HEAD` ngoai 4 tep packet ; git cat-file -p HEAD
  output     : N1 (toan allowlist -> DAY_DU) t01 GIET · N2 (`or startswith('scripts/')`) t02 GIET (t09 SONG — t09 do ranh gioi tien to, dung thiet
               ke) · N3 (KHONG DO DUOC -> DUONG_NHANH) t05, t06 GIET · N4 (goi `git rev-parse` truoc kiem su kien) t03 GIET · N5 (`.github/`) t08
               GIET · N6a (go `if:` pull_request buoc phan loai) y01 GIET · N6b (release-check full `${{ false }}`) y03, y04, y12 GIET · N6c
               (packet-loop selftest `== 'day_du'`) y03, y12 GIET · N7 (`paths-ignore`) y05 GIET ·
               nt8 actionlint rc=1 `ci.yml:654:51: unexpected end of input ... [expression]` (goc rc=0) · nt9a `ĐỎ: test sống chưa đăng ký:
               ops/ci_duong_nhanh_test.py` `ĐĂNG KÝ: 23/22` `TỔNG: ĐỎ` · nt9b `ĐỎ: CI không gọi mục đăng ký: ops/ci_duong_nhanh_test.py` ·
               nen master 20ec8d5 `22/22` `1025/1025` -> HEAD `23/23` `1025/1025` · numstat so master `1 0` (so 1741e0a `172 6`) ·
               20ec8d5 la to tien HEAD; 20ec8d5..HEAD dung 4 tep packet; 127 tep ngoai packet trong diff 1741e0a..HEAD lech blob master: 0 ·
               head co 1 khoi `BEGIN SSH SIGNATURE`, cha 41508cd; xac minh chu ky KHONG DO DUOC (khong allowedSignersFile)
  ket luan   : KHONG PHAI LOI

HUONG 5: phep thu VI SAI bo duyet <-> `copytree` that (bat bien cua lop: "di DUNG nhung duong t82 di")
  gia thuyet : neu con mot cau truc TRONG cay ma hai ben lech (bo duyet DO ma t82 chep duoc = do oan; t82 vap ma bo duyet DAT = lot), cay ngau
               nhien nho se tim ra
  lenh       : tmp/r18/vi_sai.py <ma> <N> <seed>: moi cay mot thu muc tam; ten thu muc gom ten bi bo qua (`x.pyc`, `__pycache__`, `.git`) va
               thu muc cham; tep thuong + FIFO (8%); 0-3 symlink, dich chon trong cay (thu muc ke ca goc/to tien => vong, tep, symlink khac => chuoi,
               duong khong ton tai => treo), dich viet bang relpath tu thu muc cha (KHONG dich nao ra ngoai goc); so `kiem_symlink_treo_ca_cay(goc)
               == []` voi `shutil.copytree(goc, dich, ignore=ignore_patterns(".git","__pycache__","*.pyc"))`; het gio 5 s = DO/VAP.
               seed 1 (N=400) + seed 11..14 (N=1500 moi seed)
  output     : 6400 cay: khop 6400 · do_oan 0 · lot 0 · het gio bo duyet 0 · het gio t82 111 (vong/bung no; bo duyet DO tuc thi o ca 111)
  ket luan   : KHONG PHAI LOI — trong pham vi sinh (cay nho, moi dich TRONG cay), bo duyet tuong duong t82. Ngoai pham vi phep thu: chuoi >= 40
               (t20zn phu), bi danh RA NGOAI cay (khong dung theo luat), tep thiet bi/khong doc duoc (gioi han tu khai), Windows.

HUONG 6: khang dinh MOI cua ban va (docstring `kiem_symlink_treo_ca_cay`, t20zm/t20zn/t20zo, thong diep commit) — do lai tung cai
  gia thuyet : neu "qua han 15 s", "FIFO nem SpecialFileError, socket nem OSError", "tep thiet bi t82 co khi chep duoc", "bung no khong vong
               thi bo duyet bung no y nhu t82" sai thi phep do cho ket qua khac
  lenh       : tmp/r18/khang_dinh.py (cwd rieng tmp/r18/cwd; moi cay trong $R/tmp; moi symlink tro TRONG cay): (1) NEN_DIA + `ops/specs/len -> ../..`
               + `ops/land/len -> ../..`: copytree (cach goi t82) han 15 s; bo duyet "goi y luot 17" = 41508cd + `followlinks=True` (tmp/r18/
               ma_goi_y_l17.py) han 15 s; bo duyet HEAD · (2) FIFO, socket UNIX · (3) `os.mknod` thiet bi ky tu (1,3) TRONG cay · (4) chuoi 41 bi
               danh · (5) k tang x hai bi danh/tang (2^k duong, khong vong), k = 8..14
  output     : (1) copytree `HET_GIO` 15,02 s (12335 tep da ghi) · goi y l17 `HET_GIO` 15,02 s · HEAD 0,0006 s, dung 2 dong `VONG ... 'ops/land/len'`,
               `'ops/specs/len'` · (2) FIFO: `shutil.Error ... is a named pipe`; socket: `shutil.Error ... [Errno 6] No such device or address`;
               HEAD: moi loai MOT dong `khong phai tep thuong` · (3) thiet bi: copytree `CHEP_DUOC`, HEAD DO (chat hon t82 — dung gioi han tu khai,
               nay DO DUOC thay vi "doc ma, chua do") · (4) HEAD 1 dong TREO tu `ops/specs/c/d00/l/l/...`; copytree `[Errno 40] Too many levels` ·
               (5) bo duyet 0,057 / 0,20 / 1,03 / 4,84 s; copytree 1,1 / 5,0 / 19,8 / 55,4 s (k = 8/10/12/14) — ca hai x4 moi 2 tang
  ket luan   : KHONG PHAI LOI — moi khang dinh do duoc deu dung. Gioi han (a) "chua do rieng" nay co so: bung no 2^k o CA HAI ben; tren runner,
               tran 60 phut cua `gate-ops` bien bung no thanh DO (fail-close), va cau truc phai co san tren master (PR ho so khong them duoc symlink).
               GHI CHU RIG: lan chay dau cua script nay cho bo duyet `rc=1` — TAO TAC cua toi (tep `nt.py` cua toi o cwd che module chuan `nt` cho
               tien trinh con `-c`); doi ten tep + cwd rieng => so tren. Cac phep do khac chay che do script (sys.path[0] = thu muc script), khong bi.

HUONG 7: nghiem thu 10 + doc lap phien ban Python (CI ghim 3.12 cho `gate-ops`, noi buoc `ci-duong-nhanh selftest` chay)
  lenh       : (tmp/nt10 = git clone cay-kho, core.abbrev 7) `python3 scripts/tl.py --selftest` ; ruff F `--output-format concise` tren 4 tep packet
               + tl.py, HEAD vs tmp/nt9m (master 20ec8d5) ; `python3.11|3.13 -B ops/ci_duong_nhanh_test.py --mot-ca <t20zi..t20zo>` (7 ca x 2) ;
               ca khong ton tai ; tron bo bang python3.12 (xem HUONG 8)
  output     : `== tl selftest 1715/1715 ==` rc=0 (5m21s), `git status` sau: rong · ruff F: tl.py 12 = 12, ci_dang_ky_test.py 0 = 0, hai tep moi 0 ·
               14/14 rc=0 · ca khong ton tai rc=2 (=> `--mot-ca` co chay ca)
               · kiem-re e2e (tmp/r18/e2e, cung 4 bien) bang python3.12: `kiem-re DAT (1 tep doi, 0 loi)` rc=0
  ket luan   : KHONG PHAI LOI

HUONG 8: tron bo test duoi Python 3.12 (phien ban CI cua `gate-ops`) + dot bien CUA TOI len chot cay (khac 17 dot bien harness)
  gia thuyet : neu bo test chi xanh tren 3.11, hoac mot bien the dot bien KHAC harness song, thi chot co lo
  lenh       : `python3.12 -B ops/ci_duong_nhanh_test.py` (tron bo) ; tmp/r18/dot_bien_toi.py + dot_bien_toi_h11b.py (dung_cay_tam + chay_con cua
               harness; moi dot bien chay CA 7 ca lop t20zi..t20zo)
  output     : 3.12: `CA: 104/104` · `DOT BIEN: 383/383 bi giet dung ly do` · `TU KIEM PHAN HANG: DAT` · `TONG: DAT` rc=0 (3m43s) ·
               H3b (bo moi bi danh sau khi tinh danh tinh) GIET o t20zk, t20zm, t20zn, t20zo · H4b (vong: bo nhanh im lang) GIET t20zm ·
               H8 (chot la khong ap sau bi danh) GIET t20zo "FIFO qua bi danh" · H9 (to tien khong chua goc) GIET t20zm "vong ve goc" ·
               H10 (danh tinh bang lstat) GIET t20zm · H13 (bao VONG nhung van di vao) GIET t20zm · H16 (to tien khong cong don) GIET t20zm ·
               H11 (bo bi danh "ngoai cay", bien LONG: goc cay bi tinh la ngoai) GIET t20zm — TAO TAC bien cua toi; H11b (bien chat) **SONG 7/7** ·
               H17 (chot la bo qua thu muc cham) **SONG 7/7** · H18 (chot la chi duoi allowlist) **SONG 7/7**
  ket luan   : KHONG PHAI LOI cho packet (xem DOT BIEN SONG SOT: H11b = duong vao (d) da tu khai + da giao phien dieu phoi tu luot 17;
               H17/H18 thu hep VI TRI chot la — khong co duong vao tu PR: git khong luu FIFO/socket/thiet bi, PR ho so khong them duoc symlink
               (kiem_mode_git), nen la phi-thuong chi den tu cau truc co san tren master/may chay; ghi lai, khong nang hang)

HUONG 9: DOI CHIEU finding luot 17 bang bien the CUA TOI (ngoai allowlist, hai tang, thu muc cham) tren HEAD va 41508cd
  lenh       : tmp/r18/doi_chieu_l17.py <cay-kho> <ma> (kho git tam; kiem_re/phan_loai_that/chep_nhu_t82 cua CHINH harness; moi dich trong cay)
  output     : xem dong 17 (b) cua DOI CHIEU LUOT TRUOC: HEAD rc=1 dung dong TREO ca 3; 41508cd rc=0 ca 3; t82 VAP ca 3; doi chung rc=0
  ket luan   : KHONG PHAI LOI (finding luot 17 DA VA THAT). `doctrine-scan` tren clone: rc=0, "sạch — đã quét 10 tệp, 0 chỗ chép doctrine".

HUONG 10: gioi han TU KHAI cua chot cay — bien "KHONG DO DUOC (may root)" thanh phep do; symlink (luu duoc trong git) toi thiet bi;
          he tep inode khong on dinh; Windows
  gia thuyet : neu gioi han khai la that thi phep do cho lech dung huong khai; neu con duong vao khac thi lech o cho chua khai
  lenh       : tmp/r18/khong_doc_duoc.py (fork + setuid 65534 SAU khi chdir vao cay tam — cha cua $R la 0700 root; dich chep o `dich.pyc/`, ten bi
               bo qua): tep thuong mode 000 · tmp/r18/symlink_thiet_bi.py: `ops/land/tat -> ../../tb.pyc/nul`, `nul` = mknod (1,3) — CA HAI trong cay ·
               /proc/mounts (loai he tep san co) · `ls *.py` o goc kho + doi chieu `sys.stdlib_module_names` (rui ro che module cho tien trinh con
               `-c` cua t20zm, cung co che voi tao tac rig cua toi o HUONG 6)
  output     : uid 65534: chot `[]` (DAT), copytree `[Errno 13] Permission denied: './ops/land/khoa.yaml'` (VAP) => gioi han (b) CO THAT, dung huong
               khai; git chi luu 100644/100755 nen checkout khong sinh duoc tep ay (khong co duong vao tu PR) · symlink -> thiet bi: chot DO
               (`khong phai tep thuong ... 'ops/land/tat'`), copytree CHEP_DUOC (ban sao la tep thuong 0 byte) · chi co ext4 (`/dev/vda / ext4`), khong
               overlay => chot (st_dev, st_ino) tren he tep inode khong on dinh: KHONG DO DUOC; runner Linux cua job la VM ext4, `gate-ops` khong khai
               `container:` · goc kho: 0 tep `.py`, 0 module trung ten stdlib · Windows (kiem-re chay o `windows-latest` khi PR gan nhan `windows` —
               buoc khong co `runner.os`): KHONG DO DUOC (khong co Windows); checkout Windows `core.symlinks=false` => khong symlink, chot chi con
               `os.stat` thu muc + `isfile` tep thuong
  ket luan   : KHONG PHAI LOI cho packet. GHI CHU (khong xep hang): cau ly do "chap nhan vi fail-close va git khong luu duoc loai tep ay" dung tung
               chu nhung bo sot symlink LUU DUOC trong git tro toi thiet bi (thanh ngu `-> /dev/null`): master co mot symlink nhu the thi MOI PR ho so
               DO o kiem-re trong khi t82 chep duoc (fail-close, khong nguy hiem; master hien 0 symlink; khong cong nao cua kho cam symlink — manifest
               chi BO QUA symlink, `scripts/tl_core/release.py:589`). Lop tai lieu da DONG, khong dan nguoi doc toi hanh dong co hai => khong nang hang.

HUONG 11: ra soat doc lap cac buoc BI BO khac (ngoai t82) tren PR ho so that — co buoc nao doc ca cay va do sau merge khong
  gia thuyet : neu golden/determinism/release-check dem hay bam ca cay (ke ca ho so) thi PR ho so them tep se lam chung DO tren master
               (dung hinh dang lop `buoc-bi-bo-doc-ca-cay-khong-chi-ba-ca`)
  lenh       : tren tmp/r18/e2e/kho (commit merge 2ef9d05 cua PR them `ops/specs/zz-e2e-luot18.md`, core.abbrev 7, PYTHONDONTWRITEBYTECODE=1):
               `python3 scripts/tl.py golden-test --json` ; `determinism-audit --strict --json` ; `release-check --full --json`
  output     : ca ba rc=0, `ok=True`; `git status --short` rong
  ket luan   : KHONG PHAI LOI (mot PR ho so dien hinh khong lam do ba buoc bi bo nay; kiem toan cac buoc bi bo do luot 15 lam bang audit hook,
               khong doi tu 20ec8d5).

## BANG DO (khang dinh -> nguon khai -> do duoc -> khop?)
| khang dinh | nguon khai | do duoc (HUONG) | khop? |
|---|---|---|---|
| CA 104/104, DOT BIEN 383/383, TU KIEM DAT, TONG DAT | commit 46bc11d, PROMPT | 3.11 va 3.12: 104/104 · 383/383 · DAT · DAT, rc=0 (1, 8) | co |
| registry 23/23 + 1025/1025; numstat `ci_dang_ky_test.py` so master `1 0` | commit, nghiem thu 9 | 23/23 · 1025/1025; master 22/22 · 1025/1025; `1 0` (so 1741e0a `172 6`) (4) | co |
| ruff F delta 0 | commit | tl.py 12 = 12 (master); ci_dang_ky_test 0 = 0; hai tep moi 0 (7) | co |
| doctrine-scan rc=0 | commit | rc=0, "10 tệp, 0 chỗ chép doctrine" (9) | co |
| thay doi CHI o `kiem_symlink_treo_ca_cay` (+docstring) va tep test | PROMPT | `git diff --stat 41508cd HEAD` 2 tep; AST bo docstring: 44 muc, khac dung `kiem_symlink_treo_ca_cay` (ghi o SO DO NEN / HUONG 9) | co |
| thoi gian tren cay that 0,021 s -> 0,028 s | thong diep commit | 0,0208 -> 0,0237 s (median 7, may nay) (2) | co (cung bac; phu thuoc may) |
| hai vong ve goc: t82 va bo duyet goi y l17 qua han 15 s; chot DO tuc thi | docstring ham, t20zm | ca hai `HET_GIO` 15,02 s; HEAD 0,0006 s, 2 dong VONG (6) | co |
| FIFO nem SpecialFileError, socket nem OSError | docstring ham | "is a named pipe"; `[Errno 6]` (6) | co |
| thiet bi: t82 "co khi chep duoc" (doc ma, chua do) | docstring ham | thiet bi (1,3) va symlink->thiet bi: copytree CHEP_DUOC, chot DO (6, 10) | co (nay do duoc) |
| (a) bung no khong vong "y nhu t82" (chua do) | docstring ham | 2^k ca hai, k = 8..14 (6) | co |
| (b) tep thuong khong doc duoc: KHONG DO DUOC (may root) | docstring ham | uid 65534: chot DAT, copytree `Errno 13` (10) | co (gioi han co that) |
| chuoi 41 bi danh khong vong qua gioi han phan giai | commit, t20zn | 42 thu muc / 41 symlink; HEAD 1 dong TREO; copytree `Errno 40` (6) | co |
| moi duong vao mot chot, moi chot mot dot bien rieng | chu thich truoc t20zk | 17 dot bien moi, ly do chet dung tung cai (3) | co |
| t20zj khoa cach goi copytree (chi nguon, dich, `ignore=`) | docstring ham, t20zj | 3 dot bien `dong_bo_t82_*` chet o dung nhanh tu kiem (3) | co (khong khoa GIA TRI nguon — khong khai) |
| bi danh KHONG vong toi thu muc anh em van duoc duyet nhu t82 | docstring ham | t20zm (i) + fuzz 6400 cay: 0 do oan (5) | co |
| 345 / 63 / 8 merge (D1) | docstring module | `do_lai_so.py`: 345; 63; 8 (do_lai_so log) | co |
| 119 tep lease; mot ref 6/119 truot | D2 | 119 tep; 113 dat / 6 truot tren clone it ref (do_lai_so log) | co |
| ba ca du lieu ~7 giay | `kiem_ca_du_lieu` | 8,2 s (`kiem_ke.py`); kiem-re e2e 7,98 s (2) | co (phu thuoc may) |
| 52 phut `gate (ubuntu-latest)` (run 36518707072) | docstring module | KHONG DO DUOC (khong mang) | — |
| DO_LAI "AL_VER: 4 dong" | goi/DO_LAI.md | 5 (regex t152) | KHONG (ngoai kho) |
| DO_LAI "938/938" | goi/DO_LAI.md | 1025/1025 | KHONG (ngoai kho) |
| DO_LAI "lease 6/113 vs 0/113" | goi/DO_LAI.md | 119 tep | KHONG (ngoai kho) |
| DO_LAI "numstat 1741e0a HEAD (mong 1 0)" | goi/DO_LAI.md | `172 6`; so master `1 0` | KHONG (ngoai kho) |

## NGHIEM THU (SPEC-r2) — bang chung TU CHAY luot nay
| # | ket qua | bang chung |
|---|---|---|
| 1 | dat | N1 (toan allowlist -> DAY_DU) -> t01 GIET (HUONG 4) |
| 2 | dat | N2 (`or startswith('scripts/')`) -> t02 GIET |
| 3 | dat | N3 (KHONG DO DUOC -> DUONG_NHANH) -> t05, t06 GIET |
| 4 | dat | N4 (goi git truoc kiem su kien) -> t03 GIET |
| 5 | dat | N5 (`.github/`) -> t08 GIET |
| 6 | dat | N6a -> y01; N6b -> y03, y04, y12; N6c -> y03, y12 (GIET); + 74 dot bien ci.yml trong 383/383 |
| 7 | dat | N7 (`paths-ignore`) -> y05 GIET |
| 8 | dat | actionlint rc=0 (shellcheck 0.9.0); bieu thuc rong trong chu thich than `run:` -> rc=1 `[expression]` |
| 9 | dat | nen master 22/22 -> HEAD 23/23 (1025/1025 ca hai); go DA_NOI -> `test sống chưa đăng ký` (23/22); go loi goi CI -> `CI không gọi mục đăng ký`; numstat so master `1 0` |
| 10 | dat | `== tl selftest 1715/1715 ==` rc=0 (clone, core.abbrev 7); ruff F delta 0 |
| 11 | chua_do_duoc | can PR that; commit KHONG khai dat |

## FINDINGS
Khong co finding xep hang (P0..P3) o luot nay. Vi vay khong co `out/HINT.patch` (HINT chi bat buoc cho finding).

## DOT BIEN SONG SOT
- Harness: 383/383 `bi giet dung ly do` (3.11 va 3.12); 21/21 cap (dot bien moi/neo lai, ca dich) chet o assertion KET QUA (HUONG 3).
- Cua toi (HUONG 8), KHONG xep hang:
  · H11b — bo theo bi danh co realpath NGOAI goc cay (bien chat): SONG 7/7. Dung duong vao (d) executor tu khai "chua co ca", luot 17 da giao
    phien dieu phoi soan (reviewer khong duoc dung duong thoat cay). Kien truc hien tai khong phan biet trong/ngoai cay (mot loi `os.walk(...,
    followlinks=True)`), nen hoi quy TU NHIEN (go `followlinks`) da bi t20zk giet; H11b la dot bien THEM logic. Mo ta ca can viet: GHI CHU
    CHO PHIEN DIEU PHOI.
  · H17 (chot la bo qua thu muc cham), H18 (chot la chi duoi allowlist): SONG 7/7 — moi ca LA dat duoi `ops/land/`. Khong co duong vao tu PR:
    git khong luu FIFO/socket/thiet bi, PR ho so khong them duoc symlink (`kiem_mode_git`), va chi doi/xoa tep thuong — nen la phi-thuong (va
    vong) chi den tu cau truc co san tren master/may chay. Muon dong (tuy chon): them nhanh FIFO o `docs/` va o thu muc cham vao t20zo.
- Tao tac rig cua toi (da loai, khong phai dot bien song): H11 bien LONG bi t20zm giet vi bien coi goc cay la "ngoai"; HUONG 6 lan dau
  bo duyet `rc=1` vi tep `nt.py` cua toi che module `nt`.

## GHI CHU CHO PHIEN DIEU PHOI (ngoai kho / ngoai write set, khong tinh vao packet)
1. Ca rieng cho duong vao (d) — MO TA BANG LOI (reviewer khong soan noi dung dung duong thoat cay): trong mot thu muc tam, dung kho git va mot
   thu muc ANH EM cua kho (ngoai cay kho). Trong thu muc anh em dat mot symlink tro toi mot tep duoi `ops/land/` cua kho; commit vao kho mot
   symlink THU MUC tro toi thu muc anh em ay (PR day du). PR ho so `git rm` tep dich. Mong: phan loai `duong_nhanh`; `copytree` kieu t82 vap;
   kiem-re DO dung MOT dong TREO duoi duong dan bi danh. Doi chung: PR sua tep khac -> DAT. Dot bien phai lam ca ay DO: H11b (bo theo bi danh
   co realpath ngoai goc cay — bien: goc cay tinh la TRONG) va `followlinks=True` -> mac dinh.
2. `goi/DO_LAI.md` van 4 dong cu (luot 15, 16, 17 da chi): "AL_VER: 4 dong" -> 5; "938/938" -> 1025/1025; "lease 6/113 vs 0/113" -> 119 tep
   (113 dat / 6 truot tren clone it ref); "`git diff --numstat 1741e0a HEAD ...` (mong 1 0)" -> so `20ec8d5` (mong `1 0`; so 1741e0a `172 6`).
3. Khang dinh dinh luong MOI ma bang do bo sot (PROMPT: tinh la finding THONG TIN): "qua han 15 s" (docstring ham, t20zm), chuoi 41/42 (t20zn,
   commit), "0,021 s -> 0,028 s" (commit), FIFO/socket/thiet bi (docstring ham) — tat ca da do o HUONG 2/6/10 va KHOP; khong co loi packet di kem.

## GHI CHU (khong xep hang)
- Cau ly do o docstring ham (`ops/ci_duong_nhanh.py`, bullet LA): "chap nhan vi fail-close va git khong luu duoc loai tep ay" dung tung chu nhung
  bo sot: git LUU duoc symlink tro toi thiet bi (thanh ngu `-> /dev/null`); master co mot symlink nhu the thi MOI PR ho so DO o kiem-re trong
  khi t82 chep duoc (do HUONG 10; master hien 0 symlink; khong cong nao cam symlink). Fail-close, khong nguy hiem. Neu executor muon (tuy chon):
```diff
--- ops/ci_duong_nhanh.py
+++ ops/ci_duong_nhanh.py
@@
-      (đọc, chưa đo) `t82` có khi chép được, nên ở đây CHẶT hơn `t82` — chấp nhận vì fail-close và git không lưu được loại
-      tệp ấy (`t20zo`).
+      (đọc, chưa đo) `t82` có khi chép được, nên ở đây CHẶT hơn `t82` — chấp nhận vì fail-close. Git không lưu được tệp thiết
+      bị nhưng LƯU được symlink trỏ tới nó (vd `-> /dev/null`): master có thứ ấy thì mọi PR hồ sơ ĐỎ ở đây (`t20zo`).
```
- Gioi han (b) "duong dan dich qua dai": tren Linux dich cua t82 (`/tmp/lp_*/repo`) NGAN hon goc checkout nen khong lech; tren Windows (dich
  trong `%TEMP%`, nguon `D:\a\...`) dich co the DAI hon — PR ho so them duong dan dai co the lam t82 Windows vap o luot day du sau. KHONG DO
  DUOC (khong Windows; tien to runner theo hieu biet, chua do); Windows CI ngoai pham vi theo chu kho.

## GHI CHU QUY TRINH
- Moi ghi chi trong $R (tmp/, out/). `cay-kho` khong bi sua (`git status --short` rong truoc/sau suite). Khong commit/push/checkout trong kho
  that; khong mang; khong cong cu GitHub.
- Ban sao: tmp/nt10, tmp/dl, tmp/r18/e2e/kho, tmp/r18/vt/k1, k2 (git clone); tmp/nt8, nt9a, nt9b, nt9m (git archive); cay tam cua harness va
  cua rig tu xoa (shutil.rmtree trong script). Mot lenh co `rm -rf` bi he quyen tu choi -> bo, viet lai bang script khong xoa.
- Rig: tmp/r18/{cay_that,vi_tri_bo_qua,vi_sai,ly_do,nghiem_thu_1_7,khang_dinh,dot_bien_toi,dot_bien_toi_h11b,doi_chieu_l17,khong_doc_duoc,
  symlink_thiet_bi}.py; log tmp/logs/*.log|txt|json; ket qua tmp/r18/*.json(l).
- SU CO: mot lenh chan doan (go `export` sai) da in toan bo bien moi truong cua tien trinh — gom bien chua credential — ra output cong cu cua
  phien reviewer. KHONG ghi vao tep nao, KHONG gui di dau; khong chep lai gia tri nao o day.
- KHONG DO DUOC: hanh vi that tren GitHub Actions (PR that, nghiem thu 11, windows-latest), he tep inode khong on dinh (chi co ext4), chu ky
  SSH cua head (khong allowedSignersFile), so 52 phut, model/effort thuc chay cua chinh luot nay.
- Danh tinh: Claude Opus 5.5, CUNG HO executor => `advisory_review`, KHONG phai cross_approved.

So lop: 10 — 0 MO; 10 DONG: `buoc-bi-bo-doc-ca-cay-khong-chi-ba-ca`, `bang-do-thieu-neo-va-thieu-kiem-ke`, `khang-dinh-dinh-tinh-rong-hon-phep-do`, `kiem-mode-git-chot-khong-rang`, `kiem-re-cua-fail-close-chua-co-ca`, `kiem-re-bi-cau-hinh-boi-du-lieu-ho-so`, `phan-loai-khong-neo-merge-ref-that`, `cau-khai-skipped-nguoc-phep-do`, `dependency-failure-skips-required-checks`, `kiem-re-phu-thuoc-actor-su-kien`.

TONG: P0=0 P1=0 P2=0 P3=0 — so lop: 10 (0 mo, 10 dong)
