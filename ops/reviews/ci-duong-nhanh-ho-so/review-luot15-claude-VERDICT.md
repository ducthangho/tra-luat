verdict: changes_requested
reviewed_sha: 3569472cb9b11e71b3c791725a2ffb416802f975
Reviewed commit: 3569472cb9b11e71b3c791725a2ffb416802f975

> luot 15 (packet #674, dac ta r2 sha256 b6e719c9…da57 KHOP). TRANG THAI: XONG cac huong (12 huong + doi chieu). Ket luan:
> 1 finding P3 (`bang-do-thieu-neo-va-thieu-kiem-ke`, so khai troi sau merge g4) — nguong chu kho 0/0/0 nen KHONG approve.
> Reviewer: Claude Opus 5.5 (cung ho voi executor) => `advisory_review`, KHONG phai cross_approved.
> Model/effort thuc chay: KHONG DO DUOC (tu khai effort max).

## DOI CHIEU LUOT TRUOC
Moi dong co phep do CUA TOI (dot bien chu KHAC harness hoac nguyen van dot bien song cua luot truoc), chay tren ban sao/cay mini.

| luot · finding | hang cu | trang thai | bang chung TU DO |
|---|---|---|---|
| luot 14 · `kiem-mode-git-chot-khong-rang` (o `M` x {120000,160000} khong ghim; dot bien X1 song 93/93) | P3 (lan 4) | DA VA THAT | X1 NGUYEN VAN luot 14 -> do DUNG `t20zh` (60 ca t1*/t2*, CTRL 0 do); bien hep `mien_tru_M_120000` -> `t20zh`; `mien_tru_M_160000` -> `t20zh` (HUONG 11). Them 7 dot bien bang cua toi P1..P7 (HUONG 4): moi dot bien hanh vi bi giet; P3 song nhung TUONG DUONG (git chuan hoa mode, do duoc). Lop DONG theo S3. |
| luot 8b · `buoc-bi-bo-doc-ca-cay-khong-chi-ba-ca` (F1: symlink co san ngoai diff thanh treo khi PR ho so xoa dich) | P2 | DA VA THAT | Truoc va (san pham HEAD bo dong `+ kiem_symlink_treo_ca_cay(kho)`): 5/5 kich ban t20zi `kiem-re rc=0 DAT (1 tep doi, 0 loi)`; HEAD: 5/5 `rc=1 DO (1 tep doi, 1 loi)` (tmp/truoc_va_kiem_re.py). t82 THAT tren ban sao cay: 5/5 doi chung rc=0, 5/5 xoa dich rc=1 shutil.Error. Walk tren cay that: dung 1 dong/kich ban, rac .git/__pycache__/*.pyc khong bao. S1..S6 cua toi deu bi giet dung ca (HUONG 4/6). Kiem ke LAI toan bo buoc bi bo tai HEAD bang audit hook: khong con duong doc-noi-dung-ho-so nao ngoai t23/t26/t27/t82 (HUONG 5). Khong sinh loi moi: master 0 symlink, walk tren cay that [] 0.02s, khong false-red tu cai dat/doctrine-scan, Windows `core.symlinks=false` delta 0 (HUONG 8, 12). |
| luot 8b · `kiem-re-cua-fail-close-chua-co-ca` (F2: ve symlink HOP LE cua `kiem_loai_tep` khong co ca, tin dung gia) | P3 | DA VA THAT | F2a go `kiem_loai_tep` khoi `lenh_kiem_re` -> do `t20n`, `t20q` (chuoi rieng "tep ho so la symlink" — walk toan cay KHONG che duoc); F2b `is_symlink() and not exists()` (dot bien `loai_tep_chi_chan_treo` cua luot 8b) -> do `t20q` (HUONG 11). |
| 5 lop cu khac (`kiem-re-bi-cau-hinh-boi-du-lieu-ho-so`, `phan-loai-khong-neo-merge-ref-that`, `cau-khai-skipped-nguoc-phep-do`, `dependency-failure-skips-required-checks`, `kiem-re-phu-thuoc-actor-su-kien`) | DONG | van DONG | san pham doi o g4 CHI them `kiem_symlink_treo_ca_cay` + 1 dong goi (`git diff 6803012 HEAD -- ops/ci_duong_nhanh.py`); ci.yml khong doi so voi 5ec951c+master; suite 307/307. |
| `bang-do-thieu-neo-va-thieu-kiem-ke` (luot 2: "6/113 ... chi bang chua cap nhat dieu kien do") | P3 (DONG o luot 8b) | VA HO — ban va luot 2/3 them PHAM VI refs nhung KHONG neo commit, nen merge g4 lam so troi lai | Merge 20ec8d5 dua so tep lease 113 -> 119; docstring van "6/113 … 0/113" khong neo commit (HUONG 7). Finding ben duoi. |


## BANG LOP
| slug | bieu hien (duong vao da liet ke) | hang cao nhat con mo | phuong an va chung | phep kiem dong lop |
|---|---|---|---|---|
| `bang-do-thieu-neo-va-thieu-kiem-ke` | (1) docstring SAN PHAM `ops/ci_duong_nhanh.py:78-80` "6/113 … 0/113" khong neo commit -> troi khi merge g4 (do: 119 tep; tu so 6 dung ngau nhien). (2) bang khai DO_LAI ("khai cua executor"): "AL_VER: 4 dong" (do 5), "938/938 … so 938 khong doi" (do 1025), "6/113 vs 0/113". Da quet het ti le trong docstring san pham: chi 3 (8/63 co neo 1741e0a; 6/113, 0/113 khong). Cac so khac trong docstring/commit/test deu khop (HUONG 7). | **P3** | neo MOI so do vao commit (va ghi lai so moi sau moi lan merge master); ca test chot "moi ti le trong docstring san pham co SHA trong cung doan" | `t98b` (HINT.patch) DO tren san pham hien tai (`[['6/113', '0/113']]`), XANH sau sua; 2 dot bien mat neo (D1, D2) bi `t98b` giet dung ly do (309/309) |
| `kiem-mode-git-chot-khong-rang` | bang 20 o phu tron mien (trang thai x mode moi); git chuan hoa mode (do); chot cap/dia/tap-lech co ca rieng (P1..P7) | DONG (S3) | — | X1 + X1a + X1b + P1,P2,P4..P7 bi giet; P3 tuong duong (do) |
| `buoc-bi-bo-doc-ca-cay-khong-chi-ba-ca` | da kiem ke LAI bang audit hook tai HEAD: doc-noi-dung-ho-so = {t23,t26,t27} + {t82}; rglob loai `ops`, khong theo symlink; packet_loop chi doc git/status (khong phu thuoc do sach); git doc-claims tren fixture ngoai allowlist | DONG | — | truoc-va 5/5 rc=0 -> HEAD 5/5 rc=1; t82 that 5/5 do; S1..S6 bi giet |
| `kiem-re-cua-fail-close-chua-co-ca` | ve symlink hop le (F2) | DONG | — | F2a, F2b bi giet |
| 5 lop cu khac (xem DOI CHIEU) | — | DONG | — | suite 307/307 |


## SO DO NEN (@3569472, Linux, Python 3.11.15, git 2.43.0, actionlint 1.7.7 + shellcheck 0.9.0, ruff 0.16.9, TMPDIR=$R/tmp)
- `python3 -B ops/ci_duong_nhanh_test.py`: `CA: 96/96 dat · 0 do · 0 hong` · `DOT BIEN: 307/307 bi giet dung ly do` ·
  `KIEM KE: ca hanh_vi=68 + cau_truc_yaml=16 + so_dang_ky=3 + tu_kiem=9 = 96 · dot bien ci_dang_ky_test.py=2 + ci.yml=74 + ci_duong_nhanh.py=189 + ci_duong_nhanh_test.py=42 = 307` ·
  `TU KIEM PHAN HANG: DAT (5 mau rc, 3 dot bien that)` · `TONG: DAT` · rc=0 · real 1m39s. `git status --short` sau khi chay: rong.
  Doi chieu luot 14: 93+3 (t20zh,t20zi,t20zj) = 96; 269 + 6 (yml g4) + 1 (mien_tru_M) + 11 (symlink) + 20 (lat_o) = 307; san pham 157+1+11+20 = 189 — KHOP.
- `python3 -B .claude/dev/ci_dang_ky_test.py`: `ĐĂNG KÝ: 23/23` · `PHẢN CHỨNG: 1025/1025 đỏ đúng` · `TỔNG: ĐẠT` · rc=0
- `actionlint .github/workflows/ci.yml` rc=0 (shellcheck co mat) · `ruff check --no-cache --select F` hai tep moi: `All checks passed!` rc=0

## BANG SAN
HUONG 1: so nen cua bo test / loi khai commit g4
  gia thuyet : neu "CA 96/96, DOT BIEN 307/307, TU KIEM DAT, TONG DAT" rong hon phep do thi so in ra khac / kiem ke lech
  lenh       : cd cay-kho && python3 -B ops/ci_duong_nhanh_test.py ; python3 -B .claude/dev/ci_dang_ky_test.py ; actionlint ; ruff
  output     : xem SO DO NEN (96/96 · 307/307 · DAT · DAT · rc=0; 23/23 · 1025/1025 · ĐẠT; actionlint rc=0; ruff sach)
  ket luan   : KHONG PHAI LOI (93+3 ca; 269+6+1+11+20 dot bien — khop tung so hang)

HUONG 2: pham vi diff + phan them cua master + merge 6803012 co trung thuc khong
  gia thuyet : neu merge g4 giau sua tay, hoac tep master bi packet dong vao, thi blob/cay se lech
  lenh       : vong `git diff -z --name-only 1741e0a HEAD` so blob HEAD:<f> vs 20ec8d5:<f> (bo 4 tep packet);
               git diff --name-only 20ec8d5 HEAD; git diff --numstat 20ec8d5 HEAD -- .claude/dev/ci_dang_ky_test.py;
               (tren BAN SAO tmp/dl) git merge-tree --write-tree 5ec951c 20ec8d5 vs 6803012^{tree}
  output     : 127 tep ngoai packet, lech 0; 20ec8d5..HEAD = DUNG 4 tep packet; numstat `1 0` (vs 1741e0a: `172 6` — 171 dong la cua #668);
               merge-tree rc=0 tree=5628d964… == 6803012^{tree} 5628d964… (merge sach, khong sua tay)
  ket luan   : KHONG PHAI LOI

HUONG 3: quyet dinh (1) — hai job #668 KHONG co `if:` theo `che_do`; khoa y11/y12/y13 co rang voi dot bien KHAC CHU harness
  gia thuyet : neu y11 chi so membership, hoac y12/y13 khong phu job moi, thi doi/them `if:` cap job/buoc cho gate-cong-cu* se SONG
  lenh       : python3 -B tmp/mut_yml.py (cay mini $R/tmp/m15/<ten>: ci.yml dot bien + ops/ci_duong_nhanh.py; chay MOI ca y* cua tmp/dl qua
               CI_DUONG_NHANH_CAY; moi neo DUNG 1 lan; actionlint tung ban)
  output     : CTRL 0/16 do · gop `if: success() || failure()` -> y11,y13 · registry them `if: !cancelled()` -> y11,y13 ·
               buoc "G5 manh ban kinh dot bien" them `if:` theo che_do -> y04,y12,y13 · gop bo needs manh -> y13 ·
               output che_do bo dieu kien su kien -> y02,y13 · release-check `!contains(che_do,'nhanh')` -> y03,y04,y12,y13 ·
               kiem-re bo `set -euo pipefail` -> y08,y14 · GOC=`github.event.before` -> y08,y13 · matrix manh `exclude` -> y13.
               Tat ca do rc=3 (TinHieuChotCa); actionlint rc=0 ca 10 ban (tuc chi bo test bat duoc).
  ket luan   : KHONG PHAI LOI. Doi chieu SPEC-r2: M2 chi buoc `if:` buoc nang o gate/gate-ops/gate-packet-loop; ngoai_pham_vi cam mo rong
               JOB_G5 va doi required checks; Q5/chua_do_duoc-5 du lieu #668 land truoc. Khong gate G5 = chay DU = fail-close; khong mau thuan.
               Fail-open `!cancelled()`: (a) chuan-bi DO -> gate-cong-cu `skipped` (ten tran) va gop VAN chay, ma tran tu output `os`
               (bieu thuc khong phu thuoc buoc) — neu output vang thi `fromJson('')` loi danh gia => gop DO/khong tao context
               `gate-cong-cu-gop (ubuntu-latest)`; neu co output thi gop chay va DO vi thieu manh — ca hai FAIL-CLOSE. (b) luot bi huy
               (concurrency) -> gop `skipped` ten TRAN, khong tao context co hau to => PR bi chan, khong mo. Hanh vi that tren Actions:
               KHONG DO DUOC (khong mang). Packet khong doi hai job nay (y13 khoa tu khung).
               Them: quyet dinh nay BI EP boi SPEC-r2 Q4 — ban sao tmp/nt1 them `if:` theo che_do vao buoc "G5 manh ban kinh dot bien
               (#668)" -> `python3 -B .claude/dev/ci_dang_ky_test.py`: `ĐỎ: G5 (M6): gate-cong-cu: bước G5 có điều kiện hoặc được phép bỏ
               qua lỗi` · `TỔNG: ĐỎ` rc=1. Muon gate G5 theo che_do thi phai sua LOGIC ci_dang_ky_test (`loi_g5_workflow`) — Q4 cam.

HUONG 5: lop `buoc-bi-bo-doc-ca-cay-khong-chi-ba-ca` — kiem ke LAI tai HEAD (sau merge master: lease_publish_test +615 dong tu #677)
  gia thuyet : neu mot buoc bi bo (ngoai t23/t26/t27/t82) doc noi dung ho so cua CAY THAT, hoac git cua kho that theo cach ho so doi duoc,
               thi con cua vao lop chua dong
  lenh       : audit hook `sys.addaudithook` (tmp/aud/hook/sitecustomize.py, PYTHONPATH -> moi tien trinh con) ghi open/scandir/listdir/
               glob/copytree duoi ops/{land,leases,reviews,specs} + moi lenh git, gan ten ca test trong cung; chay TUNG buoc bi bo tren
               ban sao cp -a cua cay-kho (tmp/aud/repo, repo2): lease_publish_test, packet_loop_test, gate_lifecycle_test, tl --selftest,
               golden-test, determinism-audit --strict, release-check --full, release-bundle
  output     : lease_publish 195/195 rc=0: doc noi dung CHI t23 (leases 357 open + specs 60), t26 (reviews 1296), t27 (reviews 651),
               t82 (copytree CA cay); moi lenh git khac nham kho tam do ca tu dung. · packet_loop 291/291 (bo qua 1) rc=0: 0 lan doc duoi
               4 thu muc; git tren kho that chi la status/rev-parse/log --merges/show origin/master (khong phai noi dung ho so) ·
               gate_lifecycle 28/28: 0 su kien · tl selftest 1715/1715 rc=0: 0 open, chi scandir (rglob cua manifest) + git doc-claims
               (cat-file, log --diff-filter=D, rev-parse --short) · golden/determinism rc=0: chi git doc-claims tren FIXTURE
               (references/golden/fixtures — duong dan khong thuoc allowlist) + scandir · release-check/bundle rc=0: chi scandir.
  ket luan   : KHONG PHAI LOI — tap doc-noi-dung-ho-so cua buoc bi bo tai HEAD = {t23,t26,t27} (kiem_ca_du_lieu chay) + {t82}
               (kiem_symlink_treo_ca_cay). Traversal rglob loai theo `"ops" in rel.parts`; luot 8b do 8 loai thay doi -> delta 0.

HUONG 4: bang quyet dinh 20 o cua `kiem_mode_git` — con o/duong vao NAO bang chua phu? (lop `kiem-mode-git-chot-khong-rang`)
  gia thuyet : (a) neu git sinh duoc mode moi ngoai {000000,100644,100755,120000,160000} thi bang thieu hang; (b) neu chot theo CAP /
               chot DIA / chot tap-lech khong phu boi bang thi dot bien o do song
  lenh       : (a) kho tam tmp/gm/k: `git mktree` voi mode 100664/100600/100775/100000 VA `git hash-object -t tree --literally` (bo qua
               kiem tra cua mktree) roi `git diff --raw --no-abbrev --no-renames <cay rong> <cay>`;
               (b) python3 -B tmp/mut_py.py — 14 dot bien SAN PHAM chu KHAC harness, cay mini tmp/m15p/<ten>, chay 77 ca t* qua
               CI_DUONG_NHANH_CAY (doi chung CTRL: 1 ca t91 do san tren cay mini -> loai khoi danh gia)
  output     : (a) 100664/100600/100000 -> `:000000 100644`, 100775 -> `:000000 100755` (ca cay literal) => git CHUAN HOA mode; mien gia tri
               5 mode cua bang la DU. (b) P1 D-moi-mode -> t20zb,t20zh · P2 gitlink mien cap merge ref -> t20za,t20zh · P4 regex nhan U
               -> t20zb · P5 bo chot dia khi A -> t20z · P6 tap lech mot chieu -> t20zb · P7 bo loi lap theo duong -> t20zh ·
               P3 MODE_THUONG + "100664" -> 0 do (SONG) — dot bien TUONG DUONG: (a) chung minh git khong the phat ra 100664.
  ket luan   : KHONG PHAI LOI — khong tim duoc o/duong vao nao bang chua phu; lop `kiem-mode-git-chot-khong-rang` DONG.

HUONG 6: loi khai "do truoc va: ca nam nhanh t20zi deu kiem-re rc=0 va t82 rc=1" + doi xung walk <-> t82 tren CAY THAT
  gia thuyet : neu mot kich ban khong lam t82 do (hoac doi chung hop le cung do) thi chot moi bao sai/thua; neu walk khong bat dung
               ca kich ban tren cay that thi fixture t20zi khong dai dien
  lenh       : python3 -B tmp/t82_kich_ban.py tmp/aud/repo2 (chay t82 THAT qua runpy cho E1,E1b,E3,E4,E5: symlink hop le roi xoa dich);
               E4 chay lai voi dich cuoi `VERSION` (cay that khong co README.md goc); roi `kiem_symlink_treo_ca_cay` tren cung cay
  output     : E1/E1b/E3/E4/E5 doi chung: t82 rc=0 `DAT t82`; xoa dich: t82 rc=1 `shutil.Error` (ca 5). Walk: nen [] · moi kich ban
               dung 1 dong dung ten · chi rac .git/__pycache__/*.pyc -> [] . Mutant S1..S6 cua toi (lexists, readlink tu cwd, chi quet ops,
               bo qua chi cho thu muc, khong xuong docs, loi duyet thanh print) -> t20zi/t20zj do dung ca.
               Ve con lai cua loi khai (kiem-re rc=0 TRUOC va): python3 -B tmp/truoc_va_kiem_re.py — dung dung kich ban t20zi (git that),
               chay lenh_kiem_re cua san pham HEAD va cua HEAD bo dong goi walk (ca du lieu stub rc=0 nhu bo test):
               E1/E1b/E3/E4/E5: `truoc-va rc=0 [kiem-re DAT (1 tep doi, 0 loi)]` · `HEAD rc=1 [kiem-re DO (1 tep doi, 1 loi)]`.
  ket luan   : KHONG PHAI LOI — loi khai dung ca hai ve (commit ghi "4/4 kich ban" vi E1b dung chung duong voi E1; t20zi do 5 nhanh).

HUONG 7: cac con so dinh luong (docstring san pham + bang DO_LAI "khai cua executor") — do lai sau merge g4
  gia thuyet : neu merge master 20ec8d5 lam troi so hang ma khong ai do lai thi khang dinh se lech so do (bai hoc "bat bien con dung
               khong chung minh so hang con dung")
  lenh       : (trong ban sao tmp/dl) python3 -B ../goi/do_lai_so.py ; python3 -B ../goi/kiem_ke.py ; grep -cE '^\s*AL_VER:...' ci.yml
               tai HEAD/20ec8d5/1741e0a ; git ls-tree ops/leases/ dem *.yaml tai 1741e0a/89fc4fa/20ec8d5/HEAD ; vong kiem(bo_qua_han=True)
               liet ke 6 tep truot ; numstat cay rong->HEAD duoi allowlist ('-') ; git ls-files 'ops/reviews/**/.gitattributes' ;
               (tmp/base20 = git archive 20ec8d5) python3 -B .claude/dev/ci_dang_ky_test.py
  output     : 345 / 63 / 8 KHOP · `ops/leases/*.yaml`: 119 tep, dat 113, truot 6 — 6 tep truot DEU co tu 89fc4fa, cung ly do bia mo
               (`CHAN [8] lease moi thay_the_cho=[...] nhung lease cu ... chua mang da_bi_thay_the`), 6 lease MOI cua master deu dat ·
               so lease: 1741e0a=113, 89fc4fa=113, 20ec8d5=119, HEAD=119 · AL_VER: HEAD=5, 20ec8d5=5, 1741e0a=4 · kiem_ke: 96 = 68+16+3+9;
               307 = 189+42+74+2; MAU_RC 5; TU_KIEM_DOT_BIEN 3; ba ca du lieu 6.7s · nhi phan duoi allowlist: 0 · .gitattributes
               duoi ops/reviews: 3 · registry tai master 20ec8d5: `ĐĂNG KÝ: 22/22`, `PHẢN CHỨNG: 1025/1025`; tai HEAD 23/23, 1025/1025.
  ket luan   : LOI (P3) — docstring san pham `ops/ci_duong_nhanh.py:79-80` con khai "6/113 … 0/113" (mau so 113 da troi thanh 119 tu
               merge g4; tu so 6 dung NGAU NHIEN — cung 6 tep cu). Bang khai DO_LAI cung troi: "AL_VER: 4 dong" (do: 5),
               "938/938 phan chung … so 938 khong doi" (do: 1025), "6/113 vs 0/113". Xem finding `so-khai-troi-sau-hop-nhat-master`.

HUONG 8: Windows `core.symlinks=false` — walk moi va t82 co lech nhau khong
  gia thuyet : neu tren checkout kieu Windows walk bao do ma t82 xanh (hoac nguoc lai) thi duong nhanh tren chan windows sai lech
  lenh       : kho tam tmp/gm/w8 (symlink docs/l1.md -> ../ops/specs/D1.md, commit 2 xoa dich), clone `-c core.symlinks=false` (w8win);
               chay kiem_symlink_treo_ca_cay + shutil.copytree kieu t82 tren ca hai
  output     : core.symlinks=false: islink=False · walk=[] · copytree OK ; core.symlinks=true: islink=True · walk=[1 dong 'docs/l1.md'] ·
               copytree LOI (shutil.Error). Duong dan dai nhat trong cay 175 ky tu (+23 tien to Windows = 198 < 260).
  ket luan   : KHONG PHAI LOI — delta 0 tren ca hai kieu checkout (chan ubuntu luon co trong ma tran). Hanh vi that tren windows-latest:
               KHONG DO DUOC.

HUONG 9: packet_loop_test (bi bo) phu thuoc `git status` cua CAY THAT — ho so co lam ban checkout khong?
  gia thuyet : `case_void_*` goi `launcher.py run --workspace ROOT` -> `git status --porcelain=v1 --untracked-files=all`; neu ket qua phu
               thuoc do sach cua cay thi mot PR ho so lam "ban" checkout (thuoc tinh eol) se do o master ma duong nhanh khong thay
  lenh       : tren ban sao tmp/aud/repo: them tep untracked + sua mot tep ops/specs (status: ` M ops/specs/...`, `?? zz-...`), chay
               python3 -B .claude/dev/packet_loop_test.py
  output     : `nền: 291/291 đạt · BỎ QUA: 1` · `TỔNG: ĐẠT` · rc=0 (giong het khi cay sach). Goc .gitattributes `* text=auto eol=lf`.
  ket luan   : KHONG PHAI LOI — ket qua khong phu thuoc do sach cua cay.

HUONG 10: nghiem thu 1-5, 8, 9 cua SPEC-r2 do DOC LAP (dot bien chu cua reviewer)
  lenh       : LOC='^t(0|1)' python3 -B tmp/mut_py.py N1..N5 ; actionlint tren ban ci.yml chen `# ${{ }}` vao than run kiem-re (dau `$`
               dung SAU phan tich) ; hai ban sao tmp/nt9a (go dong DA_NOI), tmp/nt9b (doi `run: python ops/ci_duong_nhanh_test.py`)
  output     : N1 toan-allowlist->day_du: t01 (+7 ca khac) · N2 allowlist+scripts/: t02 (+6) · N3 khong-do-duoc->nhanh: t05,t06 (+6) ·
               N4 push goi git: t03 · N5 allowlist+.github/: t08 · actionlint dot bien rc=1 ("unexpected end of input ... [expression]"),
               goc rc=0 · nt9a: `ĐỎ: test sống chưa đăng ký: ops/ci_duong_nhanh_test.py` `ĐĂNG KÝ: 23/22` rc=1 · nt9b: `ĐỎ: CI không gọi
               mục đăng ký: ops/ci_duong_nhanh_test.py` rc=1
  ket luan   : KHONG PHAI LOI

HUONG 11: doi chieu luot truoc bang dot bien (X1 nguyen van luot 14 + bien hep; F2a/F2b cua luot 8b)
  lenh       : LOC='^t(1|2)' python3 -B tmp/mut_py.py X1_luot14_mien_tru_M X1a_mien_tru_M_120000 X1b_mien_tru_M_160000 F2a_bo_kiem_loai_tep
               F2b_loai_tep_chi_chan_treo (cay mini tmp/m15p/<ten>, 60 ca, CTRL 0 do)
  output     : X1 -> [t20zh] · X1a -> [t20zh] · X1b -> [t20zh] · F2a -> [t20n, t20q] · F2b -> [t20q]
  ket luan   : KHONG PHAI LOI — ca ba finding luot truoc DA VA THAT, co rang, khong tin dung gia (moi dot bien do dung ca dich).

HUONG 12: kiem-re false-red tren master/PR binh thuong + cua vao "noi dung ho so chay vao goi" qua symlink HOP LE
  gia thuyet : (a) neu cay/master co symlink treo, hoac buoc truoc kiem-re (cai cong cu, doctrine-scan) de lai symlink trong workspace,
               moi PR duong nhanh se DO oan; (b) neu manifest/rglob theo symlink thi symlink HOP LE tu thu muc trong goi vao ho so cho
               PR ho so doi noi dung goi ma release-check (bi bo) moi bat
  lenh       : git ls-files -s | awk '$1=="120000"' (HEAD, 20ec8d5) ; kiem_symlink_treo_ca_cay tren cay that (+ thoi gian) ;
               ops/cong_cu.yaml cong thuc cai shellcheck/rg ; (tmp/nt1) find -type l truoc/sau doctrine-scan ;
               doc scripts/tl_core/release.py `_release_should_include` + rglob
  output     : 0 symlink tracked (HEAD va master) · walk [] 0.018s · cai dat = apt/brew/choco (ngoai workspace) · doctrine-scan rc=0,
               symlink 0 -> 0 · manifest loai MOI symlink (`if path.is_symlink(): return False`, v1.33.56 F4) va rglob khong di xuong
               symlink thu muc (3.11 `not entry.is_symlink()`; 3.12 `walk(follow_symlinks=False)`)
  ket luan   : KHONG PHAI LOI


## BANG DO (khang dinh -> dao khai -> do duoc -> khop?)
| khang dinh | nguon khai | do duoc (lenh o BANG SAN) | khop? |
|---|---|---|---|
| CA 96/96, DOT BIEN 307/307, TU KIEM DAT (5 mau rc, 3 dot bien that), TONG DAT | commit 3569472 | 96/96 · 307/307 · DAT · DAT · rc=0 (1m39s) | co |
| registry 23/23 + 1025/1025 | commit | 23/23 · 1025/1025 · ĐẠT; nen master 20ec8d5: 22/22 · 1025/1025 | co |
| actionlint rc=0, ruff F delta 0, doctrine-scan rc=0 | commit | rc=0 (shellcheck co) · All checks passed (2 tep moi) + tl.py 12 F821 = CLAUDE.md nen (scripts/ khong doi) · `doctrine-scan: sạch` rc=0 | co |
| "4/4 kich ban kiem-re rc=0 ma t82 do" (do truoc va) / t20zi "ca nam nhanh" | commit / docstring t20zi | 5/5 truoc-va rc=0; HEAD 5/5 rc=1; t82 that 5/5 rc=1 | co |
| "21 dot bien" (t20zh), "11 dot bien" (symlink) | commit | kiem_ke: t20zh dich dau 21; t20zi 9 + t20zj 2 = 11 | co |
| bang 20 o: 7 chap nhan, 13 git sinh duoc (7 chap nhan, 6 tu choi) | docstring t20zh | tinh tay + do git chuan hoa mode | co |
| 345 / 63 / 8 (8/63 ~13%) | docstring D1 | 345 / 63 / 8 | co |
| "6/113 … 0/113" (lease) | docstring D2 + DO_LAI | 119 tep; dat 113, truot 6 (cung 6 tep cu); 552 ref: KHONG DO DUOC (mirror 45 ref) | **KHONG** (mau so troi) |
| AL_VER: 4 dong | DO_LAI | HEAD 5, master 20ec8d5 5, 1741e0a 4 (delta so master = 0 — bat bien spec van dung) | **KHONG** (so troi) |
| ci_dang_ky "938/938 … so 938 khong doi" | DO_LAI | 1025/1025 (ca nen master) | **KHONG** (so troi) |
| ci_dang_ky_test.py dung 1 dong them | DO_LAI / spec NT9 | `git diff --numstat 20ec8d5 HEAD` = `1 0` (so voi 1741e0a la 172/6 vi #668) | co (so voi master) |
| master co ba `.gitattributes` duoi ops/reviews | docstring D1 | 3 | co |
| master: 0 tep nhi phan duoi allowlist | docstring kiem_nhi_phan | 0 (numstat cay rong -> HEAD) | co |
| ba ca du lieu ~6 giay | docstring kiem_ca_du_lieu | 6.7s (may nay) | co (khac may) |
| `JOB_G5` khong chua gate-ops (sau #668) | docstring test | JOB_G5 = (gate, gate-registry, gate-packet-loop, MANH, GOP) | co |
| `loi_g5_workflow` canh `!cancelled()` cua gop | chu thich JOB_CO_IF_CHO_PHEP | `G5_GOP_IF = "${{ !cancelled() }}"` | co |
| head la commit co chu ky | PROMPT | co khoi `gpgsig` SSH; xac minh: KHONG DO DUOC (khong allowedSignersFile) | mot phan |
| G5 46,5/52 phut; "4 luot that" (Issue #674 comment 5889459132) | DO_LAI / chu thich ci.yml | KHONG DO DUOC (khong mang) | — |

## NGHIEM THU (SPEC-r2)
| # | ket qua | bang chung TU CHAY |
|---|---|---|
| 1 | dat | N1 (toan allowlist -> day_du) do `t01` (HUONG 10) |
| 2 | dat | N2 (allowlist + `scripts/`) do `t02` (HUONG 10) |
| 3 | dat | N3 (khong do duoc -> nhanh) do `t05`, `t06` (HUONG 10) |
| 4 | dat | N4 (push goi git) do `t03` (HUONG 10) |
| 5 | dat | N5 (allowlist + `.github/`) do `t08` (HUONG 10) |
| 6 | dat | 10 dot bien YAML cua toi bi y* bat (HUONG 3) + 74 dot bien ci.yml cua harness trong 307/307 |
| 7 | dat | y05 trong 96/96; harness co 2 dot bien dich y05 |
| 8 | dat | actionlint rc=0 (shellcheck co); chen `${{ }}` rong vao comment `run:` -> rc=1 (HUONG 10) |
| 9 | dat | nen master 22/22 -> HEAD 23/23 (1025/1025 ca hai); go DA_NOI -> `test sống chưa đăng ký`; go loi goi CI -> `CI không gọi mục đăng ký`; numstat `1 0` |
| 10 | dat | `tl --selftest` 1715/1715 rc=0 (ban sao repo2, co audit hook); ruff F tl.py 12 = nen, 2 tep moi sach |
| 11 | chua_do_duoc | can PR that; commit KHONG khai dat |


## FINDINGS

### bang-do-thieu-neo-va-thieu-kiem-ke  [P3]  So khai trong docstring san pham (6/113, 0/113) khong neo commit — troi khi merge master g4; bang khai DO_LAI troi ba so
TEP/DONG: `ops/ci_duong_nhanh.py:78-80` (docstring module, muc D2); bang khai cua executor `goi/DO_LAI.md` (dong lease 6/113, dong
  ci_dang_ky 938/938, dong AL_VER 4).
VAN DE: Docstring D2 khai "Trên một clone chỉ-master 6/113 tệp lease trượt `kiem(bo_qua_han=True)`, còn trên bản sao đủ 552 ref thì
  0/113 (đo bởi reviewer lượt 1)". Con so do tai 1741e0a (113 tep lease) nhung KHONG ghi commit. Merge g4 (6803012 <- master 20ec8d5)
  dua so tep lease len 119; do tai HEAD: `119 tep; dat 113, truot 6`. Tu so 6 van dung chi vi NGAU NHIEN (dung 6 tep cu, cung ly do
  bia mo; 6 lease moi cua master deu dat) — dung hinh dang bai hoc CLAUDE.md "MOT BAT BIEN CON DUNG KHONG CHUNG MINH CAC SO HANG CON
  DUNG": mot nguoi doc HEAD se tin kho co 113 lease. Luot 2 da xep chinh con so nay vao lop nay ("chi bang chua cap nhat dieu kien do");
  ban va luc do them pham vi refs nhung khong them NEO COMMIT, nen lan merge master dau tien lam no troi lai. Cung lan merge, bang khai
  DO_LAI troi them hai so: "AL_VER: 4 dong" (HEAD = master = 5; bat bien "delta so master = 0" cua spec van dung) va "938/938 phan chung
  … so 938 khong doi" (nen master va HEAD deu 1025/1025). Khong anh huong hanh vi; la lo cua phep KHAI dinh luong (P3).
DA THU VA: co — (a) SAN PHAM (khoi diff, executor tu ap; KHONG nam trong HINT.patch vi khong phai tep test):
```diff
--- ops/ci_duong_nhanh.py
+++ ops/ci_duong_nhanh.py
@@ -77,7 +77,9 @@ ba loại khoảng trắng có bị tắt rộng hơn ba loại đó không).
     được miễn kiểm chỉ vì hết hạn. Cả hai đuôi `.yaml` và `.yml`. Giới hạn: bia mộ hai chiều của `kiem`
     đọc các lease khác trong CÂY; checkout của Actions chỉ có cây PR, không có các nhánh `ops/**`. Trên một
     clone chỉ-master 6/113 tệp lease trượt `kiem(bo_qua_han=True)`, còn trên bản sao đủ 552 ref thì 0/113
-    (đo bởi reviewer lượt 1): số 6 là số CỦA PHẠM VI clone-một-nhánh, không phải của kho.
+    (đo bởi reviewer lượt 1 tại 1741e0a, khi kho có 113 tệp lease; sau merge master 20ec8d5 kho có 119
+    tệp, clone 6 ref vẫn trượt đúng 6 tệp cũ ấy — đo lại cross-review lượt 15): số 6 là số CỦA PHẠM VI
+    clone-một-nhánh, không phải của kho.
```
  (b) TEST — `out/HINT.patch` (nhan nguyen van "chua chay tren cay that — executor tu ap, tu do, tu chiu trach nhiem commit"):
  ca `t98b_ti_le_trong_docstring_san_pham_phai_co_neo_commit` (`@ca`, nhom hanh_vi theo dau hieu AST cua t96): moi doan docstring
  san pham (tach dong trong / gach `·`) co ti le `\d{1,4}/\d{1,4}` phai co SHA 7-40 hex (co it nhat mot chu a-f) trong CUNG doan;
  khong con ti le nao thi DO (ca co MAT phai co DO). CHOT RIENG cho tung duong vao: `docstring_ti_le_D1_mat_neo` (bo neo `1741e0a`
  cua 8/63) va `docstring_ti_le_D2_mat_neo` (hoan tac sua (a)) — ca hai dich `t98b`.
  (c) bang khai DO_LAI (ngoai kho, cua phien dieu phoi): AL_VER 4 -> 5 (ghi ca nen 20ec8d5), 938 -> 1025 (ghi ca nen 20ec8d5 =
  22/22·1025), lease 6/113 -> "6/113 tai 1741e0a; 6/119 tai 20ec8d5 (clone 6 ref)".
DA THU NGHIEM: ban sao tmp/hint_chk (cp -a cay-kho): `patch -p0 --fuzz=0 < out/HINT.patch` -> ap sach, `cmp` giong het ban da do;
  CHI ap HINT (san pham chua sua): `--mot-ca t98b…` -> `DO:… [['6/113', '0/113']]` rc=3 (chot bat dung loi hien tai);
  ap them sua (a): `t98b` rc=0; suite DAY DU: `CA: 97/97` · `DOT BIEN: 309/309 bi giet dung ly do` · `KIEM KE: … hanh_vi=69 … = 97 ·
  … ops/ci_duong_nhanh.py=191 … = 309` · `TU KIEM PHAN HANG: DAT` · `TONG: DAT` rc=0 (1m42s); registry 23/23 · 1025/1025 ĐẠT;
  ruff F sach. sha256(out/HINT.patch) = ae861091d45ad7bd610668c8ccac8ac2c8760ba92fb0d497fba03586e8a63b05.
  Gioi han chot: do su CO MAT cua neo, khong kiem SHA ton tai (clone nong se do oan); so 552 ref / 0/113 KHONG DO DUOC o day.
DO TIN: cao (so do lai duoc tren cay that va mirror); hang P3 la danh gia — chu kho co the coi la ghi chu, nhung nguong 0/0/0 khong cho approve.

## GHI CHU QUY TRINH
- Moi ghi chi trong $R (tmp/, out/). `cay-kho` khong bi sua (`git status --short` rong sau moi lan chay). Khong commit/push/checkout
  trong kho that; khong mang; khong cong cu GitHub. Ban sao: tmp/aud/repo, tmp/aud/repo2 (audit), tmp/dl (do so + test chay dot bien),
  tmp/nt1, tmp/nt9a, tmp/nt9b, tmp/hint, tmp/hint_chk, cay mini tmp/m15/*, tmp/m15p/*; kho tam tmp/gm/*. Lenh `git clone`+`checkout`
  trong tmp bi he thong quyen tu choi mot lan -> dung `cp -a` va `git archive` thay the.
- Rig cua toi: tmp/aud/hook/sitecustomize.py, tmp/run_cases.py, tmp/mut_yml.py, tmp/mut_py.py, tmp/t82_kich_ban.py, tmp/truoc_va_kiem_re.py.
- Dot bien SONG SOT cua toi: P3 `MODE_THUONG + "100664"` — TUONG DUONG (git chuan hoa mode, do o HUONG 4). Khong co dot bien song nao khac.
- KHONG DO DUOC: hanh vi that tren GitHub Actions (PR that, NT 11, ten context khi `skipped`, timeout, windows-latest), chu ky SSH cua
  head, so 552 ref, model/effort thuc chay cua chinh luot nay.
- Danh tinh: Claude Opus 5.5, CUNG HO executor => `advisory_review`, KHONG phai cross_approved; packet `sensitive` van can Codex
  `cross_approved` hoac `human_audited` o cong land.

TONG: P0=0 P1=0 P2=0 P3=1 — so lop: 9 (1 MO: `bang-do-thieu-neo-va-thieu-kiem-ke` P3; 8 DONG: `kiem-mode-git-chot-khong-rang`,
`buoc-bi-bo-doc-ca-cay-khong-chi-ba-ca`, `kiem-re-cua-fail-close-chua-co-ca`, `kiem-re-bi-cau-hinh-boi-du-lieu-ho-so`,
`phan-loai-khong-neo-merge-ref-that`, `cau-khai-skipped-nguoc-phep-do`, `dependency-failure-skips-required-checks`,
`kiem-re-phu-thuoc-actor-su-kien`).
