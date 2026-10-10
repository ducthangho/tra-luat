#Requires -Version 7.1
# Phản chứng cho `.claude/dev/chay-cong-windows.ps1` — dựng một kho GIẢ (đích cổng là stub) rồi chạy
# script THẬT, byte-identical, trong tiến trình riêng. Mỗi ca khoá một lớp của cross-review PR #602:
#   t1 trang-thai-lac-quan-song-sot-cau-lenh-nem  release-bundle rc=0 mà không ghi zip / zip CŨ ⇒ ĐỎ
#   t2 bo-giai-cong-cu-theo-ten-thu-tu            `bash`/`bash.exe` nuốt argv đầu PATH ⇒ không được ĐẠT
#   t3 runner-tu-nhiem-cay-dang-do                sau một lượt, `git status` của kho giả SẠCH
#   t4 nhan-noi-hon-phep-do (nếp git)             `.git/config.lock` ⇒ rc=4, không in "→ 7" suông
#   t5 nhan-noi-hon-phep-do (khởi động)           Start-Process hỏng ⇒ không in "TREO"
#   t6 guong-ci-bo-dieu-kien-nen                  bước ci.yml `runner.os != 'Windows'` ⇒ script bỏ trên Windows
#   t7 sua-moi-truong-phien-goi                   PATH dùng dấu phân cách của nền, không chèn lặp AL_DICH; AL_DICH CHÍNH LÀ
#                                                 `dist/actionlint` (samefile — kể cả khi TEMP có sẵn `actionlint/`)
#   t8 bo-giai-cong-cu-theo-ten-thu-tu            `python` thoát 0 cho mọi lời gọi ⇒ không được ĐẠT
#   t9 han-mac-dinh-duoi-thoi-luong-da-do         mặc định -HanGiay ≥ `timeout-minutes` LỚN NHẤT của MỌI job `gate*` trong ci.yml
#   t10 duong-dan-du-lieu-thanh-mau-wildcard      gốc kho dưới `…[1]…` ⇒ rc=2 + nói "wildcard", không "không tìm thấy gốc"
#   t11 nhan-noi-hon-phep-do (giết)               `Kill` ném, tiến trình còn sống ⇒ không in "ĐÃ GIẾT"
#   t12 nhan-noi-hon-phep-do (tham số)            `-HanGiay 0` bị từ chối, không thành "TREO > 0s"
#   t13 do-loi-goi-khong-do-hieu-qua (git)        biến môi trường, `[include]`, biến `GIT_CONFIG` (legacy) che `core.abbrev` ⇒ rc=4 (mỗi đường một chốt)
#   t14 cong-chay-ngoai-hop-dong-chay-cong        bundle treo quá `-HanGiay` ⇒ không ĐẠT, không chờ trọn
#   t15 do-loi-goi-khong-do-hieu-qua (zip)        zip cũ KHÔNG xoá được + bundle rc=0 không ghi ⇒ không ĐẠT
#   t16 treo-ngoai-han-gio                        cổng thoát ngay, CHÁU giữ stdout ⇒ chờ THÊM < 15 s so với lượt nền; ngoài Windows rc=4
#   t17 khoa-hep-hon-hop-dong (tất định)          hai zip KHÁC nhau ⇒ tất định ĐỎ
#   t18 xa-qua-han-nuot-cong-do                   cổng rc=1 + CHÁU giữ stdout ⇒ vẫn ĐỎ (rc=1), in log cổng; cổng thoát ở giây 3 ⇒ thời
#                                                 lượng trong [HanGiay−0,5; HanGiay+2,5] (gồm phần chờ, xả chỉ bằng phần hạn CÒN LẠI)
#   t19 mot-du-lieu-hai-nhan                      `ExitCode` KHÔNG đọc được ở đường chung ⇒ KHÔNG ĐO ĐƯỢC, không ĐỎ; cột rc in `-`
#   t20 tep-test-khong-kin-moi-truong-may         console code page 437 ⇒ vẫn đọc đúng output UTF-8 của script
#   t21 bo-giai-cong-cu-theo-ten-thu-tu (PATH)    `python` giả trong `<TEMP>/actionlint` (TEMP dùng chung) ⇒ cổng Python không ĐẠT
#   t22 bo-giai-cong-cu-theo-ten-thu-tu (tách)    gốc kho chứa dấu phân cách PATH (AL_DICH vỡ đôi, tiền tố lên đầu PATH) ⇒ rc=2
#   t23 bo-giai-cong-cu-theo-ten-thu-tu (tuyệt đối) Tim-Python trả ĐƯỜNG DẪN của tệp đã kiểm, không trả TÊN (hàm nạp từ AST)
#   t24 bo-giai-cong-cu-theo-ten-thu-tu (theo dõi) tệp THEO DÕI dưới `dist/actionlint` (đầu PATH của wrapper lease) ⇒ rc=2
#   t25 bo-giai-cong-cu-theo-ten-thu-tu (cho phép) `dist/actionlint` chứa thứ installer không sinh ra — `python` chưa theo dõi;
#                                                 symlink `dist` CHƯA theo dõi trỏ sang thư mục có `actionlint/python` ⇒ rc=2
#   t26 duong-dan-du-lieu-thanh-mau-wildcard (FilePath) đường dẫn công cụ chứa `[ ]` ⇒ KHÔNG gọi Start-Process, KHÔNG ĐO ĐƯỢC
#   t27 bo-giai-cong-cu-theo-ten-thu-tu (mục dist) `dist` THEO DÕI ở dạng mà `ls-files -- dist/actionlint` không thấy — symlink `dist`;
#                                                 `DIST/…` — kèm `actionlint` giả (TÊN được phép) ⇒ rc=2; `GIT_LITERAL_PATHSPECS` ⇒ rc=2
#   t28 bo-giai-cong-cu-theo-ten-thu-tu (nền)     danh sách CHO PHÉP là của NỀN ĐANG CHẠY: tên installer chỉ sinh ra ở nền KHÁC
#                                                 (`actionlint` không đuôi trên Windows, `actionlint.exe` ngoài Windows) ⇒ rc=2; đúng bộ
#                                                 tên của nền này ⇒ KHÔNG bị chặn
#   t29 chot-dat-sau-diem-dung                    `dist` THEO DÕI (symlink sang `tools`) ⇒ rc=2 và KHÔNG gì được ghi qua nó trước khi bị
#                                                 từ chối (thư mục nhật ký từng được tạo TRƯỚC chốt `ls-files`)
#   t30 guong-lenh-bo-env-buoc                    `env:` của bước cổng: mọi khoá `env` (workflow/job/bước) của job `gate*` trong ci.yml và
#                                                 của `ci-dot-bien-du.yml` có mặt trong script; MỌI khoá ấy RÒ từ phiên gọi đều bị xoá
#                                                 trước khi tới cổng; `test registry` mang env `pull_request` (GOC/DAU đúng) khi cây
#                                                 SẠCH + HEAD đi trước `origin/master`, vắng (ĐỦ) khi bẩn, khi có mục assume-unchanged /
#                                                 skip-worktree bị sửa, hoặc khi không đi trước
#   t31 env-cong-cu-phien-goi-lot-qua             `PYTHON*` lạ (`PYTHONOPTIMIZE` gỡ `assert` trần), biến git cục bộ của kho (tập lấy từ
#                                                 `git rev-parse --local-env-vars` — `GIT_WORK_TREE` đổi cây mà `git status` đo, `GIT_DIR`
#                                                 đổi kho nhận nếp git), `BASH_ENV` và hàm bash export `BASH_FUNC_*` (hàm che cả lệnh
#                                                 nội trú `exit`/`exec`) RÒ từ phiên gọi đều bị xoá trước khi tới cổng
#   t32 guong-ci-troi-theo-master                 mọi bước của ci.yml (mọi job trừ `chuan-bi`; trừ bước chỉ chạy ở chế độ `duong_nhanh`) có LỆNH trong
#                                                 script — mỗi (đích `.py/.sh/.ps1` + MỌI đối số sau nó) BẰNG đuôi của một mảng/lệnh, đối số script lấy từ
#                                                 BIẾN là hằng có mặt trong script — hoặc có TÊN ĐÚNG trong một hằng chuỗi `KHÔNG CHẠY…`/`THAY BẰNG…`; bước
#                                                 không đích, bước `uses:` lạ và ghim phiên bản phải khớp danh sách CHO PHÉP / hằng của script (bước mới ⇒ ĐỎ).
#                                                 VÀ dấu vân từng job (`$DauVanCi`: thân `run`, env, with, uses, if…) khớp bảng ghim ⇒ đổi MỘT chữ ở bước nào cũng ĐỎ
#   t33 bo-giai-cong-cu-theo-ten-thu-tu (wrapper) `python` giả (thoát 0) ĐẦU PATH, `python3` thật sau nó ⇒ cổng lease (wrapper THẬT
#                                                 chọn Python theo TÊN) không ĐẠT; `python` in `TLPY=` rồi thoát khác 0 ⇒ cổng lease
#                                                 không chạy (vế `$LASTEXITCODE` của thăm dò)
#   t34 guong-ci-troi-theo-master (bộ so)         bộ so của t32 chạy trên kho GIẢ: nền sạch ⇒ rỗng; mỗi chốt CHẶN của bộ so một hàng đột biến (chốt chỉ giảm nhiễu — cắt `2>&1`, bỏ env có `{{`, `install` trước ghim, `posix` — và so hoa/thường của giá trị `$env:` không có hàng; neo đầu chuỗi và so hoa/thường của dòng `KHÔNG CHẠY` CÓ hàng từ lượt 20) (cờ, bước trùng cặp,
#                                                 `uses:` lạ, ghim, `env`, job không `gate`, bước không tên/không đích, nối dòng, nháy không cân, đối số mới qua biến,
#                                                 tên trong chuỗi lạ); ci.yml đổi ở kênh bộ so không thấy ⇒ chỉ dấu vân bắt; chú thích / dòng trống / CRLF ⇒ dấu vân KHÔNG đổi
#   t35 guong-co-mat-khong-do-chay                script CHẠY đủ các cổng trên kho giả — ba lượt: MẶC ĐỊNH (không `-Muc`) · `nhanh` · `day-du` —: tên cổng in ra khớp bảng ghim `$CongDayDu` (t32 chỉ thấy VĂN BẢN);
#                                                 bộ so của t35 (`Tim-CongLech`) có hàng đột biến SCRIPT riêng: `if ($false)`, cổng rơi khỏi `nhanh`, đổi tên, cổng thừa, đổi mức mặc định
#   t36 dist-symlink-ra-ngoai-kho (Codex #602)    `dist` hoặc `dist/cong-windows` CHƯA theo dõi là symlink/junction tới thư mục NGOÀI kho ⇒ rc=2
#                                                 trước mọi lần ghi; thư mục đích giữ nguyên (`a.zip`, `b.zip`, không `cong-windows/`)
# Bộ này KÍN với config git của máy chạy, với biến git trỏ kho khác (khối ngay dưới `$script:Rac`), với code page của
# console (`Doc-Utf8`), với dấu thập phân của locale (t18 nhận `5,1s`) và với `<TEMP>/actionlint` của máy (t7, t21 tự đặt TEMP).
# ĐỘT BIẾN để đo răng (đo trên pwsh 7.4.6/Linux, bộ 28 ca, TMPDIR sạch): `-Script` trỏ f2392df ⇒ 2/28 (đạt t17 — bản ấy đã so băm —
# và t21 — dấu `;` ghim cứng dán AL_DICH vào mục PATH kế nên nó không thành một mục); 8b82d40 ⇒ 13/28 (đỏ t7 t13 t14 t15 t16 t18 t19
# t21 t22 t23 t24 t25 t26 t27 t28); 66efc78 ⇒ 15/28 (đỏ t7 t13 t16 t18 t19 t21 t22 t23 t24 t25 t26 t27 t28); 131c608 ⇒ 16/28 (đỏ t7
# t13 t18 t19 t21 t22 t23 t24 t25 t26 t27 t28); bd62cad ⇒ 18/28 (đỏ t7 t19 t21 t22 t23 t24 t25 t26 t27 t28); 131c2e7 ⇒ 19/28 (đỏ t7
# t21 t22 t23 t24 t25 t26 t27 t28); c8c2c6a ⇒ 21/28 (đỏ t22 t23 t24 t25 t26 t27 t28); 623864e ⇒ 24/28 (đỏ t25 t26 t27 t28); f1f753b ⇒
# 26/28 (đỏ t27 t28); 543f2e8 ⇒ 27/28 (chỉ t28).
# Lượt 11: bộ 29 ca — mỗi hàng ở trên đỏ thêm t29 (eba9b1d ⇒ 28/29, chỉ t29: `New-Item $NhatKy` đứng TRƯỚC chốt `dist`).
# Lượt 12: bộ 30 ca — mỗi hàng ở trên đỏ thêm t30 (87eea22 ⇒ 29/30, chỉ t30: thiếu khoá `env` của bước `gate*`, ở cả cây nhánh lẫn
# cây merge). Đột biến bản vá, mỗi chốt một lượt của t30: bỏ `CONG_CU_TEST_BAN_KINH` khỏi danh sách xoá ⇒ lượt 1 (cây merge: vế tĩnh);
# bỏ `CI_DANG_KY_DOT_BIEN_MANH` ⇒ lượt 1; bỏ `CI_DANG_KY_SU_KIEN` ⇒ lượt 2; bỏ vế cây SẠCH ⇒ lượt 2; bỏ vế đi TRƯỚC ⇒ lượt 3; đảo
# GOC/DAU ⇒ lượt 1.
# Lượt 13: b5a9f79 ⇒ chỉ t30 (cây merge: vế tĩnh thiếu `NHANH_DON_DUOC_MANH(_RA)` của `ci-dot-bien-du.yml`; cây nhánh: lượt 1 — biến ấy
# rò tới cổng). Giữ tên trong danh sách nhưng bỏ xoá `CONG_CU_TEST_MANH*` ⇒ t30 lượt 1 (trước lượt này: SỐNG 30/30 cả hai cây); bỏ
# chốt cờ index ⇒ t30 lượt 3 (assume-unchanged); chốt chỉ nhận thẻ thường (bỏ `S`) ⇒ lượt 4 (skip-worktree); bỏ riêng
# `NHANH_DON_DUOC_MANH_RA` khỏi danh sách ⇒ lượt 1. Từ lượt này t30 có NĂM lượt `Chay`: sạch+trước · bẩn · assume-unchanged ·
# skip-worktree · không đi trước — nên "bỏ vế đi TRƯỚC ⇒ lượt 3" của dòng Lượt 12 nay là lượt 5 (đo: thông báo "HEAD khong di truoc").
# Lượt 14: bộ 31 ca — 34e7a9d ⇒ chỉ t31 (vế tĩnh: thiếu 12 biến git cục bộ + `BASH_ENV`; cả cây nhánh lẫn cây merge). Đột biến bản vá,
# mỗi cửa một lượt: bỏ xoá `PYTHON*` ⇒ t31 "assert tran bi go"; xoá `PYTHON*` theo danh sách CẤM chỉ có `PYTHONOPTIMIZE` ⇒ t31 "ro toi
# cong_cu_test" (`PYTHONWARNINGS`); giữ tên mà bỏ xoá `GIT_WORK_TREE` / `GIT_DIR` / `BASH_ENV` / `GIT_SHALLOW_FILE` ⇒ t31 "ro toi
# cong_cu_test". Bỏ vế THẤY TÊN của đồ giả (`STUB_KHOA_RO` không trùng biến nào) thì ba đột biến đầu vẫn chết ở vế HỆ QUẢ: `GIT_WORK_TREE`
# ⇒ registry mang env diff trên cây BẨN; `GIT_DIR` ⇒ `core.abbrev=7` trong config kho khác; `BASH_ENV` ⇒ bash nạp tệp ấy 3 lần.
# Lượt 15: bộ 32 ca — ad4e724 ⇒ cây nhánh 30/32 (t30: khoá `CI_DUONG_NHANH_*` của danh sách cố định rò tới `cong_cu_test`; t31: vế tĩnh
# `BASH_FUNC_*`), cây merge 7e5958e 29/32 (t30 vế tĩnh, t31, t32 `ci-duong-nhanh selftest`). Đột biến bản vá: giữ hằng `BASH_FUNC_*` mà
# bỏ xoá ⇒ t31 "ro toi cong_cu_test", kèm bỏ vế THẤY TÊN ⇒ t31 "ham export che lenh noi tru exit"; bỏ xoá `CI_DUONG_NHANH_MERGE` (giữ
# hằng) ⇒ t30 "ro toi cong_cu_test" ở cả hai cây; bỏ dòng `KHÔNG CHẠY` của `ci-duong-nhanh selftest` ⇒ t32 (cây merge); bỏ cổng
# `bien-nhan v2 selftest` ⇒ t32 (cây nhánh).
# Lượt 16: bộ 33 ca — 9b8a420 ⇒ chỉ t32 (cặp `scripts/tl.py release-manifest` của lane WORKER không có trong script và tên dòng
# `KHÔNG CHẠY` không ĐÚNG tên bước; cây merge thêm `ops/cong_cu_test.py --gop`) và t33. Trước lượt này t32 so theo TỆP: `scripts/tl.py`
# là đích của 11 bước, nên bỏ `golden-test` ⇒ SỐNG 32/32, bỏ chín cổng dùng chung tệp ⇒ SỐNG 32/32 (cả hai cây); ci.yml thêm bước
# `scripts/tl.py new-audit`, `ruff check … scripts/tl.py`, `actionlint` ⇒ t32 vẫn ĐẠT.
# Lượt 17: bộ 34 ca — 2b8f000 (bộ 33 ca, t32 so theo (đích, đối số đầu)) sống sót bảy đột biến: thêm `--strict` vào `golden-test` ở ci.yml,
# thêm bước `tl.py doc-claims-check --lane-moi`, bỏ `--strict` ở script, bước `uses: ./.github/actions/…`, đổi ghim `PyYAML`/`AL_VER`, đổi tên job
# `gate-ops` + bước mới, và `CI_DANG_KY_WORKERS` 2→4 ở ci.yml (cả bảy: t32 ĐẠT). Nay mỗi đột biến ấy là một dòng của t34 và ra ĐỎ; bỏ riêng từng
# chốt của `Tim-ThieuGuong` (so đuôi / `uses:` / ghim / `env` hằng / lọc job / tên rỗng) ⇒ t34 ĐỎ.
# Vế `$LASTEXITCODE -eq 0` của thăm dò `python` của wrapper lease (t33) sống sót ở 2b8f000 (bỏ vế ấy ⇒ t33 vẫn ĐẠT); nay có lượt thứ ba của t33.
# Lượt 18: bộ 34 ca — c848fee (t32 so đuôi) sống sót mười sáu đột biến ở ci.yml / script, mỗi cái t32 ĐẠT: tiền tố trước đích (`python -O …`), lệnh không đích
# thêm vào bước đã gương (`actionlint -color`), `env` kiểu số (`CI_DANG_KY_WORKERS: 4`), dòng `git config` của bước "Force LF" (bước không đích được tha theo
# TÊN: `core.abbrev 7`→`8`, bỏ `core.eol lf`), đối số mới mà script nhận qua BIẾN (`bash ops/cai_cong_cu.sh jq`), `with: python-version`, `pip install … pytest` (ghim
# thiếu `==`), job `uses:` tái dùng, `if: runner.os == 'Linux'` / `matrix.os != 'windows-latest'` (t6 chỉ đọc cách viết `!= 'Windows'`), `env` cấp workflow, `defaults`/`container`/`continue-on-error` cấp job,
# và script giữ tên bước trong một chuỗi bất kỳ (`Noi 'ghi chu "<tên>"'` thay dòng gương). Nay: dấu vân từng job (`$DauVanCi`) bắt mọi đột biến phía ci.yml (kể cả `defaults`/`container`/`services`/
# `continue-on-error` cấp job và `env`/`defaults` cấp workflow); vị từ "tên trong dòng KHÔNG CHẠY" đòi hằng chuỗi BẮT ĐẦU bằng `KHÔNG CHẠY`/`THAY BẰNG`; đối số-từ-biến
# phải là hằng có mặt trong script. t34 thêm hàng cho tám chốt trước đây không có răng riêng trong t34 (ghim `AL_VER`, `env` cấp job, nối dòng, `$BIEN`→`*`, nháy không
# cân, chú thích, bước `duong_nhanh`, `&&`) và cho từng chốt của dấu vân: gỡ riêng từng chốt CHẶN ⇒ t32 hoặc t34 ĐỎ (lượt 18 đo 33 chốt; lượt 20 đo 64 đột biến gỡ chốt/nối dây trên d53e681, ICU — sau các hàng của lượt này chỉ còn ĐẠT ở cả t32 lẫn t34: nhóm khai ở dòng 57 và các chốt tương đương — lookbehind của `mau`, `punctuation_chars`, dấu nháy ngược, dòng cuối nối dòng, `sorted(jobs)`). Lượt 19 đo thêm trên 72dc360: t32 gọi thiếu `$DauVanCi` / `$DauVanCi = $null` ⇒ 34/34 (nay: `Tim-ThieuGuong` từ chối ở chỗ TIÊU THỤ; lượt 20: `$null` viết thẳng ở lời gọi của t32 cũng 35/35 — cờ `-ChiBoSoTungDong` thay `$null`); dấu vân không có hàng cho `defaults` cấp workflow, `with`/`env`/`if` cấp job, `chuan-bi`, khoảng trắng cuối dòng, job biến mất; bộ so không có hàng cho `-cne`, `-ccontains`, tên chứa tên (nay có). Trên bộ 34 ca của lượt 17, gỡ chốt ghim `AL_VER` /
# `env` cấp job / nối dòng / `$BIEN` / nháy không cân / chú thích ⇒ t34 ĐẠT (sáu chốt không răng); gỡ chốt bước `duong_nhanh` / `&&` chỉ ĐỎ ở t32 trên ci.yml THẬT.
# Lượt 10: danh sách hợp hai nền (543f2e8) ⇒ chỉ t28 (lượt 1); đảo nền ⇒ chỉ t28 (lượt 1); danh sách của nền này rỗng / thiếu `goi.gz`
# ⇒ chỉ t28 (lượt 2); bỏ danh sách CHO PHÉP nay ⇒ t25 t28; nhánh Windows của t27 ép chạy trên Linux: fixture mới ⇒ 28/28, fixture dẫn
# `'tools'` qua ống (blob 6 byte) ⇒ chỉ t27 (chốt tự kiểm KHÔNG ĐO ĐƯỢC).
# Lượt 9: hỏi lại `ls-files -- dist/actionlint` ⇒ chỉ t27; bỏ `--icase-pathspecs` ⇒ chỉ t27 (lượt
# `DIST/…`); `:(icase)dist` thay cờ ⇒ chỉ t27 (lượt `GIT_LITERAL_PATHSPECS`); gỡ vế `$LASTEXITCODE -ne 0` của chốt `ls-files` ⇒ chỉ t27
# (cùng lượt ấy — đo trên bộ 27 lẫn 28 ca); bộ này bỏ lượt 1 của t25 × bỏ CHO PHÉP ⇒ t25 (lượt symlink
# CHƯA theo dõi). Lượt 8, mỗi chốt một ca: bỏ chốt wildcard của Chay-Cong ⇒ chỉ t26; bỏ danh sách CHO PHÉP ⇒ chỉ t25 (riêng đường symlink cũng làm
# t25 đỏ trên 623864e); so tên KHÔNG phân biệt hoa thường ⇒ SỐNG 26/26 (TƯƠNG ĐƯƠNG: tên chỉ khác hoa thường là CÙNG tệp trên hệ tệp
# không phân biệt, còn trên hệ tệp phân biệt thì PATH không đọc nó thành `actionlint`). Lượt 7: Tim-Python trả TÊN ⇒ chỉ t23; bỏ chốt
# phân cách PATH ⇒ chỉ t22; bỏ chốt tệp theo dõi ⇒ chỉ t24; AL_DICH về TEMP ⇒ t7 t21 t25 (danh sách CHO PHÉP nay soi `<TEMP>/actionlint`;
# bỏ vế samefile của t7 thì t7 SỐNG trước đột biến ấy); TÊN + TEMP ⇒ t7 t21 t23 t25. Lượt 6: cột rc in TRỐNG thay cho `-` ⇒ t19. 29 đột biến trên script (lượt 4): 25 đỏ ÍT NHẤT ca
# của mảnh nó gỡ, 4 sống đúng là bốn mảnh khai ở cuối đoạn này. Lượt 5 đo lại trên bộ 20 ca: gỡ nhánh rc≠0 của xả / `$giay` trước xả / bỏ trừ phần hạn đã trôi /
# xả 2×HanGiay / sàn 12 s ⇒ chỉ t18; xả cố định 30 s ⇒ t16 t18; nhánh xả đếm ĐẠT ⇒ t16; rc=null đếm ĐỎ ⇒ t19; giải bash
# theo tên ⇒ t2; bỏ `$env:GIT_CONFIG = $null` ⇒ t13; sàn 0 ⇒ SỐNG (đã khai). Trên chính bộ này: `Doc-Utf8` rỗng ⇒ t20;
# bộ đọc thời lượng chỉ nhận dấu chấm ⇒ t18. Ca chung chốt thì khai: gỡ `exit 4` của nếp git đỏ t4 lẫn t13; `$td` khởi
# ĐẠT đỏ t1 t14 t15; bỏ xả luồng có hạn (bỏ hẳn / vô hạn / `WaitForExit()` / cố định 30 s) đỏ t16 lẫn t18 (vế thời
# lượng). Gỡ khối kín config của chính bộ này, dưới config toàn cục của ci.yml ⇒ t4 lẫn t20 (cùng dựng `config.lock`).
# Từng SỐNG rồi mới có ca: `$ha -eq $hb` (nay t17); nhánh xả-quá-hạn in "TREO" mà vẫn đếm ĐẠT (nay t16 đọc rc);
# giải `bash` theo tên trên Linux (nay t2 đặt cả `bash`); xả KHÔNG trừ phần hạn đã trôi / xả 2×HanGiay / sàn 12 s (18/18
# khi cổng thoát ngay — nay t18 cho cổng thoát ở giây 3); cột rc in `-` (20/20 — nay t19). Mảnh KHÔNG ca nào đo được trên
# nền này — khai thẳng: `$null -eq $rc` của nhánh xả (TƯƠNG ĐƯƠNG từ lượt 5: rc=null rơi xuống đường chung cũng ra KHÔNG ĐO
# ĐƯỢC — gỡ ra vẫn 24/24);
# `[bool]$ha`, `[string]$ban`, `-ErrorAction Stop` của Start-Process (tương đương: nó vốn ném lỗi kết thúc);
# `$null = $tt.Handle` và `catch { $xa = $false }` (chỉ có tác dụng khi `.Handle`/`WaitForExitAsync` ném — Windows,
# pwsh 7.0); `#Requires -Version 7.1` (bộ này chạy bằng pwsh ≥ 7.1); sàn 1 s của `$conMs` (chỉ đổi kết quả khi cổng
# thoát sát hạn); phần khối kín cho `GIT_INDEX_FILE`/`GIT_DIR` (đo bằng chạy dưới biến ấy — gỡ ra ⇒ index kho khác
# 2144 → 34 mục — không có ca); dòng ép UTF-8 trong harness t11/t19 (chỉ có tác dụng khi console của tiến trình con là
# code page cũ — Windows); `try/catch` quanh danh sách CHO PHÉP (chỉ khi không liệt kê được thư mục); vế `$LASTEXITCODE -eq 0` của
# chốt `ls-files -v` (`git status` vừa chạy được mà `ls-files` hỏng là ca không dựng được — gỡ ra ⇒ SỐNG ở mọi bộ đã đo: 30/30 bộ 30
# ca, 31/31 bộ 31 ca, 32/32 bộ 32 ca). CHƯA ĐÓNG — khai thẳng:
# `ops/chay_lease_publish_test.sh` (ngoài write set) vẫn gọi `python` theo tên SAU khi chèn AL_DICH; script chỉ bảo đảm thư mục ấy
# không có mục THEO DÕI và chỉ chứa TÊN installer sinh ra TẠI LÚC chèn — một cổng chạy trước wrapper (mã của nhánh) vẫn ghi được vào
# đó, và một `actionlint[.exe]` (tên của NỀN NÀY) chưa theo dõi mà installer không ghi (lượt trước) vẫn qua tới lượt installer thành
# công kế tiếp.
[CmdletBinding()]
param([string]$Script)
Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$GocKho = (Resolve-Path -LiteralPath (Join-Path $PSScriptRoot (Join-Path '..' '..'))).Path
if (-not $Script) { $Script = Join-Path $PSScriptRoot 'chay-cong-windows.ps1' }
$Script = (Resolve-Path -LiteralPath $Script).Path
$PwshExe = (Get-Process -Id $PID).Path
$Sep = [IO.Path]::PathSeparator

$Stub = 'import os,sys; sys.exit(int(os.environ.get("STUB_RC_"+os.path.basename(sys.argv[0]).replace(".","_").replace("-","_"),"0")))'
$TlStub = @'
import os, sys
a = sys.argv[1:]
if a and a[0] == "release-bundle":
    out = a[a.index("--out") + 1]
    m = os.environ.get("STUB_BUNDLE", "same")
    if m == "ngu":
        import time; time.sleep(float(os.environ.get("STUB_NGU", "30")))
    if m in ("same", "ghi-rc1", "ngu"):
        open(out, "wb").write(b"ZIP-CO-DINH")
    if m == "khac":
        open(out, "wb").write(b"ZIP-" + out.encode())
    sys.exit(1 if m == "ghi-rc1" else 0)
sys.exit(0)
'@

$script:Rac = @()
# KÍN với config git của MÁY CHẠY: `ci.yml` đặt `core.autocrlf/eol/abbrev` bằng `--global` ở cả ba job gate, nên khi ghi
# `--local` trượt (t4) giá trị CÓ HIỆU LỰC vẫn đúng và script chạy tiếp ⇒ t4 ĐỎ oan đúng nơi bộ này sẽ được nối (đo:
# 14/15 dưới config toàn cục của ci.yml). Mọi git — của bộ test lẫn của script đang đo — đọc config toàn cục RỖNG,
# bỏ tầng system, bỏ tham số truyền qua biến.
$GitRong = Join-Path ([IO.Path]::GetTempPath()) ('ccw-' + [guid]::NewGuid().ToString('N').Substring(0, 10) + '.gitconfig')
Set-Content -LiteralPath $GitRong -Value '' -Encoding utf8NoBOM
$script:Rac += $GitRong
$env:GIT_CONFIG_GLOBAL = $GitRong; $env:GIT_CONFIG_NOSYSTEM = '1'
$env:GIT_CONFIG_COUNT = $null; $env:GIT_CONFIG_PARAMETERS = $null
# …và KÍN với biến git trỏ KHO KHÁC: hook `pre-commit` của `git commit -a` xuất `GIT_INDEX_FILE` TUYỆT ĐỐI, khi ấy
# `git -C <kho giả> add -A` ghi đè index của kho THẬT (đo: 2144 → 34 mục, index trỏ blob không có); `GIT_DIR` cùng họ
# (đo: `git -C <kho giả> commit` ghi vào kho mà biến trỏ tới). t13 tự đặt lại `GIT_CONFIG` qua `Chay`.
foreach ($n in 'GIT_DIR', 'GIT_WORK_TREE', 'GIT_INDEX_FILE', 'GIT_OBJECT_DIRECTORY', 'GIT_ALTERNATE_OBJECT_DIRECTORIES',
               'GIT_COMMON_DIR', 'GIT_CONFIG') { [Environment]::SetEnvironmentVariable($n, $null) }
# …và KÍN với code page của console: pwsh GIẢI MÃ output lệnh ngoài bằng `[Console]::OutputEncoding` của tiến trình NÀY — trên
# Windows mặc định là code page OEM/ANSI (437/1252; chính script khai ở `.DESCRIPTION`) — còn script và harness GHI UTF-8. Không ép
# thì mọi regex tiếng Việt thành rác (giả lập console 437 trên Linux: 13/18, t1 t4 t11 t13 t17 ĐỎ oan, vế phủ định `tất định … rc=0`
# của t14/t15 mù). Ép UTF-8 quanh lời gọi rồi trả lại (trên Windows setter đổi code page của CẢ console). Setter ném (máy không
# có console) thì đi tiếp: giải mã sai làm ca đòi KHỚP thành ĐỎ nhưng làm MÙ vế phủ định (đo, 437 + setter gỡ + `$td` khởi ĐẠT ⇒
# t14 ĐẠT) — cả bộ vẫn ĐỎ vì t20 đỏ trong đúng tình huống ấy.
function Doc-Utf8 { param([scriptblock]$Lam)
    $enc = [Console]::OutputEncoding
    try { [Console]::OutputEncoding = [Text.UTF8Encoding]::new($false) } catch { }
    try { & $Lam } finally { try { [Console]::OutputEncoding = $enc } catch { } } }
function Dung-Kho { param([string]$Scr = $Script)
    $d = Join-Path ([IO.Path]::GetTempPath()) ('ccw-' + [guid]::NewGuid().ToString('N').Substring(0, 10))
    $script:Rac += $d
    $k = Join-Path $d 'k'
    foreach ($t in 'ops', '.claude/dev', 'scripts/tl_core', '.githooks', '.github/checks') {
        New-Item -ItemType Directory -Force -Path (Join-Path $k $t) | Out-Null
    }
    Copy-Item -LiteralPath $Scr -Destination (Join-Path $k '.claude/dev/chay-cong-windows.ps1')
    Copy-Item -LiteralPath (Join-Path $GocKho 'ops/bash_nen.py') -Destination (Join-Path $k 'ops/bash_nen.py')
    Copy-Item -LiteralPath (Join-Path $GocKho '.gitignore') -Destination (Join-Path $k '.gitignore')
    foreach ($f in 'ops/lease_publish_test.py', 'ops/cong_cu.py', 'ops/cong_cu_test.py',
                   '.claude/dev/packet_loop_test.py', '.claude/dev/ci_dang_ky_test.py',
                   '.claude/dev/codex_cred_test.py', 'ops/bien_nhan_v2_test.py', '.claude/dev/idiom_py_test.py',
                   '.githooks/eol_policy_test.py', '.githooks/pre_push_test.py', '.claude/dev/gate_lifecycle_test.py',
                   '.githooks/eol_policy.py', '.github/checks/bundle_fragment_check.py', 'scripts/gen_instructions.py',
                   'scripts/tl_core/command_registry_test.py', '.github/checks/ci_phamvi.py',
                   '.github/checks/ci_phamvi_test.py', 'scripts/tl_boot.py', 'scripts/tl_core/__init__.py',
                   'scripts/tl_core/deterministic.py', 'scripts/tl_core/jsonio.py', 'scripts/tl_core/workflow.py',
                   'scripts/tl_core/release.py', 'scripts/tl_core/live.py', 'scripts/tl_core/zip_ingest.py',
                   'scripts/tl_core/ocr.py', 'scripts/tl_core/chunking.py', 'scripts/tl_core/command_registry.py') {
        Set-Content -LiteralPath (Join-Path $k $f) -Value $Stub -Encoding utf8NoBOM
    }
    Set-Content -LiteralPath (Join-Path $k 'scripts/tl.py') -Value $TlStub -Encoding utf8NoBOM
    Set-Content -LiteralPath (Join-Path $k 'ops/chay_lease_publish_test.sh') -Value "exit `${STUB_RC_LEASE:-0}" -Encoding utf8NoBOM
    Set-Content -LiteralPath (Join-Path $k 'scripts/don-nhanh_test.ps1') -Value 'exit 0' -Encoding utf8NoBOM
    & git -C $k init -q
    & git -C $k add -A
    & git -C $k -c user.email=t@t -c user.name=t commit -qm fx
    return $k
}

function Chay {
    param([string]$Kho, [string[]]$Doi = @(), [hashtable]$Env = @{})
    $cu = @{}
    foreach ($n in $Env.Keys) { $cu[$n] = [Environment]::GetEnvironmentVariable($n); [Environment]::SetEnvironmentVariable($n, $Env[$n]) }
    try {
        $ra = Doc-Utf8 { & $PwshExe -NoProfile -File (Join-Path $Kho '.claude/dev/chay-cong-windows.ps1') @Doi 2>&1 }
        $rc = $LASTEXITCODE
    } finally { foreach ($n in $cu.Keys) { [Environment]::SetEnvironmentVariable($n, $cu[$n]) } }
    $txt = (($ra | ForEach-Object { "$_" }) -join "`n") -replace "\x1b\[[0-9;]*m", ''
    return @{ rc = $rc; ra = $txt }
}

# Python cho t6/t9: chọn theo NĂNG LỰC (in được `TLYAML=ok` sau `import yaml`), không lấy tên đầu tiên —
# đúng lớp `bo-giai-cong-cu-theo-ten-thu-tu` mà bộ này khoá (alias Store `python.exe` trên Windows).
function Tim-PyYaml {
    foreach ($u in @([pscustomobject]@{ Ten = 'py'; Dau = @('-3') }, [pscustomobject]@{ Ten = 'python'; Dau = @() },
                     [pscustomobject]@{ Ten = 'python3'; Dau = @() })) {
        if (Get-Command $u.Ten -ErrorAction SilentlyContinue) {
            $d = $u.Dau
            $ra = @(& $u.Ten @d -c "import yaml; print('TLYAML=ok')" 2>$null)
            if ($LASTEXITCODE -eq 0 -and @($ra -match '^TLYAML=ok$').Count -gt 0) { return $u }
        }
    }
    throw 'KHONG DO DUOC: khong co Python nao import duoc yaml'
}

$script:KetQua = @()
function Ca { param([string]$Ten, [scriptblock]$Than)
    try { & $Than; $script:KetQua += "DAT  $Ten" }
    catch { $script:KetQua += "DO   $Ten — $($_.Exception.Message)" } }

Ca 't1 bundle rc=0 khong ghi zip / zip cu => DO' {
    $k = Dung-Kho
    $a = Chay $k @('-Muc', 'day-du') @{ STUB_BUNDLE = 'none' }
    if ($a.ra -notmatch 'release-bundle tất định\s+rc=1') { throw "khong zip: van khong DO (rc_script=$($a.rc))" }
    $b = Chay $k @('-Muc', 'day-du') @{ STUB_BUNDLE = 'same' }
    if ($b.rc -ne 0) { throw "nen: luot same phai DAT, rc=$($b.rc)" }
    $c = Chay $k @('-Muc', 'day-du') @{ STUB_BUNDLE = 'none' }
    if ($c.ra -notmatch 'release-bundle tất định\s+rc=1') { throw "luot none sau luot same: tat dinh khong ra rc=1 — zip CU bi bam hoac khong xoa duoc (rc_script=$($c.rc))" }
    $e = Chay $k @('-Muc', 'day-du') @{ STUB_BUNDLE = 'ghi-rc1' }
    if ($e.ra -match 'release-bundle tất định\s+rc=0' -or $e.rc -eq 0) { throw "bundle rc=1 (da ghi zip) ma tat dinh DAT (rc_script=$($e.rc))" }
}

Ca 't2 bash.exe nuot argv dau PATH => lease khong DAT' {
    $k = Dung-Kho
    $shim = Join-Path (Split-Path $k) 'shim'
    New-Item -ItemType Directory -Force -Path $shim | Out-Null
    if ($IsWindows) {
        Set-Content -LiteralPath (Join-Path $shim 'bash.cmd') -Value '@exit /b 0' -Encoding ascii
    } else {
        # Cả tên TRẦN `bash`: chỉ đặt `bash.exe` thì ca chỉ bắt bộ giải thử `bash.exe` trước — bộ giải `Get-Command bash`
        # (cùng lớp "theo tên") sống qua cả bộ trên Linux (đo: 18/18).
        foreach ($n in 'bash.exe', 'bash') {
            Set-Content -LiteralPath (Join-Path $shim $n) -Value "#!/bin/sh`nexit 0" -Encoding utf8NoBOM
            & chmod +x (Join-Path $shim $n)
        }
    }
    $a = Chay $k @() @{ STUB_RC_LEASE = '1'; PATH = "$shim$Sep$env:PATH" }
    if ($a.ra -match 'lease-publish selftest\s+rc=0') { throw 'shim duoc chon, cong lease DAT ma khong chay gi' }
}

Ca 't3 luot chay khong de rac trong cay' {
    $k = Dung-Kho
    $null = Chay $k @('-Muc', 'day-du') @{ STUB_BUNDLE = 'same' }
    $rac = @(& git -C $k status --porcelain --untracked-files=all)
    if ($rac.Count -gt 0) { throw "git status ban: $($rac -join ' | ')" }
}

Ca 't4 .git/config.lock => rc=4, khong in "→ 7" suong' {
    $k = Dung-Kho
    New-Item -ItemType File -Path (Join-Path $k '.git/config.lock') | Out-Null
    $a = Chay $k
    Remove-Item -LiteralPath (Join-Path $k '.git/config.lock') -Force
    if ($a.rc -ne 4) { throw "rc=$($a.rc), mong 4" }
    if ($a.ra -notmatch 'KHÔNG ĐẶT ĐƯỢC') { throw 'khong bao nep hong' }
}

Ca 't5 Start-Process hong => khong goi la TREO' {
    $k = Dung-Kho
    foreach ($d in (Join-Path $k 'dist/cong-windows'), (Join-Path $k '.cong-windows')) {
        New-Item -ItemType Directory -Force -Path (Join-Path $d 'cong_cu_kiem-tra.out') | Out-Null
    }
    $a = Chay $k
    if ($a.ra -match 'cong_cu kiem-tra\s+TREO') { throw 'khoi dong hong ma in TREO/DA GIET' }
    if ($a.rc -eq 0) { throw 'rc=0 cho mot cong khong chay' }
}

# Đo được trên MỌI nền (không cần `$IsWindows` thật): đọc `if:` từ ci.yml, rồi đòi mỗi đích của
# bước `runner.os != 'Windows'` chỉ xuất hiện trong nhánh `else` của một `if ($IsWindows)`.
Ca 't6 buoc ci.yml bo tren Windows => script cung bo tren Windows' {
    $ci = Join-Path $GocKho '.github/workflows/ci.yml'
    $py = Tim-PyYaml; $pd = $py.Dau
    $ma = "import re,sys,yaml`nd=yaml.safe_load(open(sys.argv[1],encoding='utf-8'))`n" +
          "for j in d['jobs'].values():`n for s in j.get('steps',[]):`n  c=str(s.get('if',''))`n" +
          "  if 'Windows' in c and '!=' in c:`n   [print(t) for t in re.findall(r'[\w./-]+\.(?:py|sh|ps1)', s.get('run') or '')]"
    $dich = @(& $py.Ten @pd -c $ma $ci)
    if ($LASTEXITCODE -ne 0 -or $dich.Count -eq 0) { throw "khong doc duoc ci.yml (rc=$LASTEXITCODE, $($dich.Count) dich)" }
    $ast = [System.Management.Automation.Language.Parser]::ParseFile($Script, [ref]$null, [ref]$null)
    foreach ($t in $dich) {
        $hits = @($ast.FindAll({ param($n) $n -is [System.Management.Automation.Language.StringConstantExpressionAst] -and $n.Value -eq $t }, $true))
        # 0 lần khớp = ca KHÔNG ĐO gì (tên viết bằng phép nối / Join-Path lọt qua) ⇒ ĐỎ, không ĐẠT êm.
        if ($hits.Count -eq 0) { throw "KHONG DO DUOC: '$t' khong xuat hien NGUYEN VAN trong script — viet dich thanh hang chuoi" }
        foreach ($h in $hits) {
            $p = $h.Parent; $gac = $false
            while ($p) {
                if ($p -is [System.Management.Automation.Language.IfStatementAst] -and $p.ElseClause -and
                    $p.Clauses[0].Item1.Extent.Text -match '^\$IsWindows$' -and
                    $p.ElseClause.Extent.StartOffset -le $h.Extent.StartOffset -and
                    $h.Extent.EndOffset -le $p.ElseClause.Extent.EndOffset) { $gac = $true; break }
                $p = $p.Parent
            }
            if (-not $gac) { throw "'$t' chay vo dieu kien trong khi ci.yml bo no tren Windows" }
        }
    }
}

Ca 't7 PATH: dau phan cach cua NEN, khong chen lap AL_DICH' {
    $k = Dung-Kho
    $al = Join-Path $k (Join-Path 'dist' 'actionlint')
    New-Item -ItemType Directory -Force -Path $al | Out-Null
    Set-Content -LiteralPath (Join-Path $k 'ops/cong_cu.py') -Encoding utf8NoBOM -Value @'
import os, sys
al = os.environ.get("AL_DICH", "")
ds = os.environ.get("PATH", "").split(os.pathsep)
# pwsh tự chèn thư mục của nó vào ĐẦU PATH lúc khởi động, nên trên nền không phải Windows
# `"$AlDich;$env:PATH"` dán AL_DICH vào thư mục ấy chứ không đụng mục AL_DICH có sẵn —
# chỉ đếm `ds.count(al)` là ca KHÔNG CÓ RĂNG trên Linux (đã đo: bản gốc vẫn qua).
dan = os.name != "nt" and any(";" in d for d in ds)
# AL_DICH phải CHÍNH LÀ `dist/actionlint` của gốc (cwd của cổng) — so bằng samefile, không so chuỗi. Thiếu vế này thì
# AL_DICH về TEMP vẫn qua t7 trên máy CÓ SẴN `<TEMP>/actionlint` (đo: 131c2e7 ⇒ 20/21, chỉ t21 đỏ).
dung = bool(al) and os.path.isdir(al) and os.path.samefile(al, os.path.join(os.getcwd(), "dist", "actionlint"))
sys.exit(0 if dung and ds.count(al) == 1 and not dan else 7)
'@
    # PATH đã có sẵn AL_DICH = lượt thứ hai trong cùng một phiên. TEMP CÓ SẴN `actionlint/` (như máy đã từng chạy installer
    # với mặc định `/tmp/actionlint`) ⇒ kết quả ca không phụ thuộc máy chạy.
    $tam = Join-Path (Split-Path $k) 'tmp'
    New-Item -ItemType Directory -Force -Path (Join-Path $tam 'actionlint') | Out-Null
    $a = Chay $k @() @{ PATH = "$al$Sep$env:PATH"; TMPDIR = $tam; TEMP = $tam; TMP = $tam }
    if ($a.ra -notmatch 'cong_cu kiem-tra\s+rc=0') { throw 'PATH sai dau phan cach hoac chen lap AL_DICH' }
}

Ca 't8 python gia thoat 0 dau PATH => cong Python khong DAT' {
    $k = Dung-Kho
    $shim = Join-Path (Split-Path $k) 'shimpy'
    New-Item -ItemType Directory -Force -Path $shim | Out-Null
    foreach ($n in 'py', 'python', 'python3') {
        if ($IsWindows) { Set-Content -LiteralPath (Join-Path $shim "$n.cmd") -Value '@exit /b 0' -Encoding ascii }
        else {
            $f = Join-Path $shim $n
            Set-Content -LiteralPath $f -Value "#!/bin/sh`nexit 0" -Encoding utf8NoBOM
            & chmod +x $f
        }
    }
    $a = Chay $k @() @{ STUB_RC_cong_cu_py = '1'; PATH = "$shim$Sep$env:PATH" }
    if ($a.ra -match 'cong_cu kiem-tra\s+rc=0') { throw 'python gia duoc chon, cong Python DAT ma khong chay gi' }
}

# Hạn mặc định cho MỘT cổng không được thấp hơn trần job CI chạy chính cổng ấy: thấp hơn thì mức
# mặc định có thể KHÔNG BAO GIỜ ra ĐẠT (đo: `test registry` > 900 s cả trên CI Windows lẫn ở đây). Đọc MỌI job `gate*`, không
# ghim ba tên: master fc852ff đã tách cổng sang `gate-ops`/`gate-cong-cu`, và ba tên ghim cứng là danh sách sẽ trôi.
Ca 't9 han mac dinh >= timeout-minutes cua job CI' {
    $ci = Join-Path $GocKho '.github/workflows/ci.yml'
    $py = Tim-PyYaml; $pd = $py.Dau
    $ma = "import sys,yaml`nd=yaml.safe_load(open(sys.argv[1],encoding='utf-8'))`n" +
          "print(max(int(d['jobs'][j]['timeout-minutes']) for j in d['jobs'] if j.startswith('gate')))"
    $phut = @(& $py.Ten @pd -c $ma $ci)
    if ($LASTEXITCODE -ne 0 -or $phut.Count -ne 1) { throw "khong doc duoc timeout-minutes (rc=$LASTEXITCODE)" }
    $ast = [System.Management.Automation.Language.Parser]::ParseFile($Script, [ref]$null, [ref]$null)
    $p = @($ast.ParamBlock.Parameters | Where-Object { $_.Name.VariablePath.UserPath -eq 'HanGiay' })
    if ($p.Count -ne 1 -or -not $p[0].DefaultValue) { throw 'khong thay mac dinh cua -HanGiay' }
    $mac = [int]$p[0].DefaultValue.SafeGetValue()
    if ($mac -lt [int]$phut[0] * 60) { throw "HanGiay mac dinh $mac s < $([int]$phut[0] * 60) s cua job CI" }
}

Ca 't10 goc kho co [ ] => bao dung nguyen nhan, khong bao "khong tim thay goc"' {
    $k = Dung-Kho
    $moi = Join-Path (Split-Path $k) 'b[1]'
    New-Item -ItemType Directory -Force -Path $moi | Out-Null
    & git clone -q $k (Join-Path $moi 'k')
    if ($LASTEXITCODE -ne 0) { throw "git clone vao duong dan co [ ] that bai (rc=$LASTEXITCODE)" }
    $a = Chay (Join-Path $moi 'k')
    if ($a.ra -match 'không tìm thấy gốc kho') { throw 'goc CO THAT ma bao "khong tim thay goc" (Test-Path doc [1] thanh mau)' }
    if ($a.rc -ne 2 -or $a.ra -notmatch 'wildcard') { throw "khong noi dung nguyen nhan wildcard (rc=$($a.rc))" }
}

# Nạp NGUYÊN VĂN `Chay-Cong` từ AST, cho `Start-Process` một đồ giả GIỮ TRẠNG THÁI: không bao giờ thoát,
# `Kill` ném (ca `taskkill Access denied` của CLAUDE.md). Trên nền thật không dựng được tiến trình giết-không-chết.
Ca 't11 Kill nem + tien trinh con song => khong in "DA GIET"' {
    $ast = [System.Management.Automation.Language.Parser]::ParseFile($Script, [ref]$null, [ref]$null)
    $fn = $ast.Find({ param($n) $n -is [System.Management.Automation.Language.FunctionDefinitionAst] -and $n.Name -eq 'Chay-Cong' }, $true)
    if (-not $fn) { throw 'khong thay ham Chay-Cong trong script' }
    $d = Join-Path ([IO.Path]::GetTempPath()) ('ccw-' + [guid]::NewGuid().ToString('N').Substring(0, 10))
    $script:Rac += $d
    New-Item -ItemType Directory -Force -Path $d | Out-Null
    $h = Join-Path $d 'h.ps1'
    Set-Content -LiteralPath $h -Encoding utf8NoBOM -Value (@'
Set-StrictMode -Version Latest
[Console]::OutputEncoding = [Text.UTF8Encoding]::new($false)
$KetQua = New-Object System.Collections.ArrayList
$NhatKy = $PSScriptRoot; $Goc = $PSScriptRoot; $HanGiay = 1; $ChiTiet = $false
$script:SoKill = 0
function Start-Process {
    $o = [pscustomobject]@{ HasExited = $false; ExitCode = $null }
    $o | Add-Member -MemberType ScriptMethod -Name WaitForExit -Value { $false }
    $o | Add-Member -MemberType ScriptMethod -Name Kill -Value { $script:SoKill++; throw 'Access is denied' }
    return $o
}
'@ + "`n" + $fn.Extent.Text + "`n" + @'
Chay-Cong -Ten 'gia' -Tep 'khong-co' -DoiSo @()
Write-Host ("TRANG_THAI=" + $KetQua[0].TrangThai + " SO_KILL=" + $script:SoKill)
'@)
    $ra = (Doc-Utf8 { & $PwshExe -NoProfile -File $h 2>&1 } | ForEach-Object { "$_" }) -join "`n"
    if ($ra -notmatch 'TRANG_THAI=KHÔNG ĐO ĐƯỢC SO_KILL=[1-9]') { throw "harness khong chay toi Kill: $ra" }
    if ($ra -match 'ĐÃ GIẾT') { throw 'Kill nem, tien trinh con song ma van in "DA GIET"' }
}

Ca 't12 -HanGiay 0 bi tu choi, khong thanh "TREO > 0s"' {
    $k = Dung-Kho
    $a = Chay $k @('-HanGiay', '0')
    if ($a.ra -match 'TREO\s+>\s*0s') { throw 'HanGiay 0 duoc nhan: moi cong "TREO > 0s"' }
    if ($a.rc -eq 0 -or $a.ra -notmatch 'HanGiay') { throw "HanGiay 0 khong bi tu choi dung cho (rc=$($a.rc))" }
}

Ca 't13 bien moi truong / [include] de core.abbrev => rc=4, khong in "→ 7" suong' {
    $k = Dung-Kho
    $a = Chay $k @() @{ GIT_CONFIG_COUNT = '1'; GIT_CONFIG_KEY_0 = 'core.abbrev'; GIT_CONFIG_VALUE_0 = '8' }
    if ($a.rc -ne 4 -or $a.ra -notmatch 'KHÔNG ĐẶT ĐƯỢC') { throw "git dung abbrev 8 ma script bao nep dung (rc=$($a.rc))" }
    # Đường thứ hai, chốt riêng: `[include]` nằm SAU `[core]` trong `.git/config` ⇒ thắng giá trị `--local` vừa ghi.
    $k2 = Dung-Kho
    $inc = Join-Path (Split-Path $k2) 'inc.gitconfig'
    Set-Content -LiteralPath $inc -Value "[core]`n`tabbrev = 8" -Encoding utf8NoBOM
    & git -C $k2 config --local include.path $inc
    $b = Chay $k2
    if ($b.rc -ne 4 -or $b.ra -notmatch 'KHÔNG ĐẶT ĐƯỢC') { throw "[include] de abbrev 8 ma script bao nep dung (rc=$($b.rc))" }
    # Đường thứ ba, chốt riêng: biến `GIT_CONFIG` (legacy) làm `--local` ghi trượt (rc=129) và `--get` CHỈ đọc tệp ấy —
    # tệp nói 7 trong khi mọi lệnh git khác dùng 8 từ `[include]`.
    $k3 = Dung-Kho
    $inc3 = Join-Path (Split-Path $k3) 'inc.gitconfig'
    Set-Content -LiteralPath $inc3 -Value "[core]`n`tabbrev = 8" -Encoding utf8NoBOM
    & git -C $k3 config --local include.path $inc3
    $leg = Join-Path (Split-Path $k3) 'legacy.gitconfig'
    Set-Content -LiteralPath $leg -Value "[core]`n`tautocrlf = false`n`teol = lf`n`tabbrev = 7" -Encoding utf8NoBOM
    $c = Chay $k3 @() @{ GIT_CONFIG = $leg }
    if ($c.rc -ne 4 -or $c.ra -notmatch 'KHÔNG ĐẶT ĐƯỢC') { throw "GIT_CONFIG legacy che abbrev 8 ma script bao nep dung (rc=$($c.rc))" }
}

Ca 't14 bundle treo qua HanGiay => khong DAT, khong cho tron' {
    $k = Dung-Kho
    $w = [Diagnostics.Stopwatch]::StartNew()
    $a = Chay $k @('-Muc', 'day-du', '-HanGiay', '3') @{ STUB_BUNDLE = 'ngu'; STUB_NGU = '30' }
    $w.Stop()
    if ($a.ra -match 'release-bundle tất định\s+rc=0') { throw 'bundle treo ma tat dinh DAT' }
    if ($w.Elapsed.TotalSeconds -ge 45) { throw "bundle khong co han gio: cho $([math]::Round($w.Elapsed.TotalSeconds))s voi HanGiay 3" }
}

Ca 't15 zip cu KHONG xoa duoc + bundle rc=0 khong ghi => khong DAT' {
    $k = Dung-Kho
    $b = Chay $k @('-Muc', 'day-du') @{ STUB_BUNDLE = 'same' }
    if ($b.rc -ne 0) { throw "nen: luot same phai DAT, rc=$($b.rc)" }
    $dist = Join-Path $k 'dist'
    $zip = @((Join-Path $dist 'a.zip'), (Join-Path $dist 'b.zip'))
    $do = Join-Path $dist 'do.zip'
    Set-Content -LiteralPath $do -Value 'x'
    $mo = @(); $go = $null
    try {
        if ($IsWindows) {
            foreach ($f in $zip + $do) { $mo += [IO.File]::Open($f, 'Open', 'Read', 'Read') }   # không FileShare.Delete
        } elseif ((& id -u) -eq '0') {
            & chattr +i @($zip + $do) 2>$null; $go = { & chattr -i @($zip + $do) 2>$null }
        } else {
            & chmod 0555 $dist; $go = { & chmod 0755 $dist }
        }
        # TỆP DÒ: khoá không có tác dụng trên nền này thì ca KHÔNG ĐO ĐƯỢC — ĐỎ, không bỏ qua êm.
        Remove-Item -LiteralPath $do -Force -ErrorAction SilentlyContinue
        if (-not (Test-Path -LiteralPath $do)) { throw 'KHONG DO DUOC: khong dung duoc tep khong xoa duoc tren nen nay' }
        $a = Chay $k @('-Muc', 'day-du') @{ STUB_BUNDLE = 'none' }
    } finally {
        foreach ($m in $mo) { $m.Dispose() }
        if ($go) { & $go }
    }
    if ($a.ra -match 'release-bundle tất định\s+rc=0') { throw "zip CU khong xoa duoc ma tat dinh DAT (rc_script=$($a.rc))" }
    if ($a.rc -eq 0) { throw 'rc=0 khi tat dinh khong do duoc' }
}

# Cổng thoát NGAY nhưng để lại CHÁU giữ stdout: hạn giờ phải phủ cả phần xả luồng (Start-Process trên Unix đọc qua
# ỐNG, `WaitForExit()` không hạn chờ EOF). Windows chuyển hướng bằng handle tệp ⇒ vế trạng thái chỉ đòi ngoài Windows.
# Đo phần chờ THÊM so với một lượt nền cùng tham số: trần tuyệt đối 40 s để lọt một bản xả cố định 30 s — gấp 6 lần
# `-HanGiay 5` (đo: 34 s vẫn ĐẠT). Vế trạng thái đọc MÃ THOÁT, không chỉ đọc chữ: một bản in "TREO" mà vẫn đếm ĐẠT
# thì script thoát 0 (đo).
Ca 't16 cong thoat ngay, CHAU giu stdout => khong treo qua -HanGiay' {
    $k0 = Dung-Kho
    $w0 = [Diagnostics.Stopwatch]::StartNew(); $null = Chay $k0 @('-HanGiay', '5'); $w0.Stop()
    $k = Dung-Kho
    $pidf = Join-Path (Split-Path $k) 'chau.pid'
    Set-Content -LiteralPath (Join-Path $k 'ops/cong_cu.py') -Encoding utf8NoBOM -Value @'
import os, subprocess, sys
if sys.argv[1:2] == ["kiem-tra"]:
    p = subprocess.Popen([sys.executable, "-c", "import time; time.sleep(60)"])
    open(os.environ["STUB_CHAU_PID"], "w").write(str(p.pid))
sys.exit(0)
'@
    $w = [Diagnostics.Stopwatch]::StartNew()
    try { $a = Chay $k @('-HanGiay', '5') @{ STUB_CHAU_PID = $pidf } }
    finally {
        $w.Stop()
        if (Test-Path -LiteralPath $pidf) { Stop-Process -Id ([int](Get-Content -LiteralPath $pidf)) -Force -ErrorAction SilentlyContinue }
    }
    $them = $w.Elapsed.TotalSeconds - $w0.Elapsed.TotalSeconds
    if ($them -ge 15) { throw "cong thoat roi ma cho CHAU them $([math]::Round($them))s so voi luot nen $([math]::Round($w0.Elapsed.TotalSeconds))s (HanGiay 5)" }
    if (-not $IsWindows -and $a.ra -match 'cong_cu kiem-tra\s+rc=0') { throw 'CHAU con giu stdout ma cong van DAT' }
    if (-not $IsWindows -and $a.rc -ne 4) { throw "CHAU con giu stdout ma rc_script=$($a.rc), mong 4 (KHONG DO DUOC)" }
}

# Lõi của cổng: hai lần build ra zip KHÁC nhau ⇒ ĐỎ. Mọi ca khác dùng stub ghi CÙNG byte, nên bỏ `$ha -eq $hb` không ca nào thấy.
Ca 't17 hai zip KHAC nhau => tat dinh DO' {
    $k = Dung-Kho
    $a = Chay $k @('-Muc', 'day-du') @{ STUB_BUNDLE = 'khac' }
    if ($a.ra -notmatch 'release-bundle tất định\s+rc=1' -or $a.rc -eq 0) { throw "a.zip khac b.zip ma tat dinh khong DO (rc_script=$($a.rc))" }
}

# Cổng ĐỎ (rc=1) mà để lại CHÁU giữ stdout — hai sự cố hay đi cùng nhau (ca hỏng bỏ dở phần dọn). rc đã đọc từ chính
# tiến trình ⇒ vẫn ĐỎ; hạ thành KHÔNG ĐO ĐƯỢC là exit 4 + "ĐỎ 0" + log cổng không in (đo trên 131c608).
Ca 't18 cong rc=1 + CHAU giu stdout => van DO, in log' {
    $k = Dung-Kho
    $pidf = Join-Path (Split-Path $k) 'chau.pid'
    Set-Content -LiteralPath (Join-Path $k 'ops/cong_cu.py') -Encoding utf8NoBOM -Value @'
import os, subprocess, sys
if sys.argv[1:2] == ["kiem-tra"]:
    import time
    print("DONG-LOI-CUA-CONG-T18", flush=True)
    p = subprocess.Popen([sys.executable, "-c", "import time; time.sleep(60)"])
    open(os.environ["STUB_CHAU_PID"], "w").write(str(p.pid))
    time.sleep(3)
    sys.exit(1)
sys.exit(0)
'@
    try { $a = Chay $k @('-HanGiay', '5') @{ STUB_CHAU_PID = $pidf } }
    finally { if (Test-Path -LiteralPath $pidf) { Stop-Process -Id ([int](Get-Content -LiteralPath $pidf)) -Force -ErrorAction SilentlyContinue } }
    if ($a.rc -ne 1) { throw "cong rc=1 ma rc_script=$($a.rc), mong 1 (DO)" }
    if ($a.ra -notmatch 'DONG-LOI-CUA-CONG-T18') { throw 'cong DO ma log cua no khong duoc in' }
    # Ngoài Windows script chờ cháu tới hạn 5 s. Cổng thoát ở giây 3 nên hạn CÒN LẠI ≈ 2 s: cột thời lượng ≈ 5 s — không phải 3
    # (bỏ phần chờ), không phải 3 + 5 (xả bằng CẢ hạn: đo 8,1 s), 13 s (xả 2×HanGiay), 15 s (sàn 12 s). Số in theo văn hoá của máy:
    # locale vi_VN in `5,1s` (đo: regex chỉ nhận dấu chấm ĐỎ oan 1/6 lượt dưới tải) — lỗi ấy chập chờn theo phép làm tròn, nên bộ
    # đọc tự kiểm trên một dòng CỐ ĐỊNH trước khi đọc dòng thật.
    $reGiay = 'cong_cu kiem-tra\s+rc=1\s+(\d+(?:[.,]\d+)?)s'
    if ('  cong_cu kiem-tra   rc=1        5,1s  ĐỎ' -notmatch $reGiay) { throw 'bo doc cot thoi luong khong nhan dau phay thap phan (locale vi_VN)' }
    if (-not $IsWindows) {
        $m = [regex]::Match($a.ra, $reGiay)
        if (-not $m.Success) { throw 'khong thay cot thoi luong cua cong_cu kiem-tra' }
        $g = [double]($m.Groups[1].Value -replace ',', '.')
        if ($g -lt 4.5 -or $g -gt 7.5) { throw "cot thoi luong ${g}s ngoai [4.5; 7.5] (HanGiay 5, cong thoat o giay 3)" }
    }
}

# rc KHÔNG đọc được (`ExitCode` = $null — lỗi handle của Start-Process trên Windows; getter ném cũng ra $null) phải là KHÔNG ĐO ĐƯỢC
# ở đường CHUNG, không chỉ ở nhánh xả-quá-hạn (đo trên bd62cad: `rc=  0.1s ĐỎ`, exit 1). Nạp NGUYÊN VĂN `Chay-Cong` như t11.
Ca 't19 ExitCode khong doc duoc => KHONG DO DUOC, khong DO' {
    $ast = [System.Management.Automation.Language.Parser]::ParseFile($Script, [ref]$null, [ref]$null)
    $fn = $ast.Find({ param($n) $n -is [System.Management.Automation.Language.FunctionDefinitionAst] -and $n.Name -eq 'Chay-Cong' }, $true)
    if (-not $fn) { throw 'khong thay ham Chay-Cong trong script' }
    $d = Join-Path ([IO.Path]::GetTempPath()) ('ccw-' + [guid]::NewGuid().ToString('N').Substring(0, 10))
    $script:Rac += $d
    New-Item -ItemType Directory -Force -Path $d | Out-Null
    $h = Join-Path $d 'h.ps1'
    Set-Content -LiteralPath $h -Encoding utf8NoBOM -Value (@'
Set-StrictMode -Version Latest
[Console]::OutputEncoding = [Text.UTF8Encoding]::new($false)
$KetQua = New-Object System.Collections.ArrayList
$NhatKy = $PSScriptRoot; $Goc = $PSScriptRoot; $HanGiay = 5; $ChiTiet = $false
function Start-Process {
    $o = [pscustomobject]@{ HasExited = $true; ExitCode = $null }
    $o | Add-Member -MemberType ScriptMethod -Name WaitForExit -Value { $true }
    $o | Add-Member -MemberType ScriptMethod -Name WaitForExitAsync -Value { [Threading.Tasks.Task]::CompletedTask }
    return $o
}
'@ + "`n" + $fn.Extent.Text + "`n" + @'
Chay-Cong -Ten 'gia' -Tep 'khong-co' -DoiSo @()
Write-Host ("TRANG_THAI=" + $(switch ($KetQua[0].TrangThai) { 'ĐẠT' { 'DAT' } 'ĐỎ' { 'DO' } 'KHÔNG ĐO ĐƯỢC' { 'KDD' } default { '?' } }))
'@)
    $ra = (Doc-Utf8 { & $PwshExe -NoProfile -File $h 2>&1 } | ForEach-Object { "$_" }) -join "`n"
    if ($ra -notmatch 'TRANG_THAI=') { throw "harness khong chay toi het Chay-Cong: $ra" }
    if ($ra -notmatch 'TRANG_THAI=KDD') { throw "ExitCode null o duong chung ma khong ra KHONG DO DUOC: $ra" }
    # Cột rc in `-`, không in TRỐNG (bản vá lượt 5 khai vậy; thiếu vế này thì gỡ nó vẫn 20/20).
    if ($ra -notmatch 'gia\s+rc=-\s') { throw "ExitCode null ma cot rc khong in '-': $ra" }
}

# Đo được trên MỌI nền: đặt console 437 (mặc định kiểu Windows) ngay trong ca rồi đòi `Chay` vẫn thấy chữ tiếng Việt của script.
Ca 't20 console code page 437 => van doc dung output UTF-8 cua script' {
    $k = Dung-Kho
    New-Item -ItemType File -Path (Join-Path $k '.git/config.lock') | Out-Null
    $enc = [Console]::OutputEncoding
    try {
        try { [Console]::OutputEncoding = [Text.Encoding]::GetEncoding(437) } catch { throw "KHONG DO DUOC: khong dat duoc code page 437 ($($_.Exception.Message))" }
        $a = Chay $k
    } finally {
        [Console]::OutputEncoding = $enc
        Remove-Item -LiteralPath (Join-Path $k '.git/config.lock') -Force -ErrorAction SilentlyContinue
    }
    if ($a.ra -notmatch 'KHÔNG ĐẶT ĐƯỢC') { throw 'console 437: output UTF-8 cua script bi giai ma thanh rac' }
}

# `AL_DICH` lên ĐẦU PATH SAU khi Tim-Python đã kiểm Python, mà cổng Python gọi theo TÊN: nếu nó là TEMP dùng chung (`/tmp/` 1777
# trên Linux) thì ai cũng đặt được `python` vào `<TEMP>/actionlint` ⇒ Python đã kiểm ≠ Python được chạy (cùng lớp t8, đường thứ ba).
Ca 't21 python gia trong <TEMP>/actionlint => cong Python khong DAT' {
    $k = Dung-Kho
    $tam = Join-Path (Split-Path $k) 'tmp'
    $al = Join-Path $tam 'actionlint'
    New-Item -ItemType Directory -Force -Path $al | Out-Null
    foreach ($n in 'py', 'python', 'python3') {
        if ($IsWindows) { Set-Content -LiteralPath (Join-Path $al "$n.cmd") -Value '@exit /b 0' -Encoding ascii }
        else {
            $f = Join-Path $al $n
            Set-Content -LiteralPath $f -Value "#!/bin/sh`nexit 0" -Encoding utf8NoBOM
            & chmod +x $f
        }
    }
    $a = Chay $k @() @{ TMPDIR = $tam; TEMP = $tam; TMP = $tam; STUB_RC_cong_cu_py = '1' }
    if ($a.ra -notmatch 'cong_cu kiem-tra\s+rc=1') { throw "python gia trong TEMP/actionlint duoc chon, cong Python khong chay that (rc_script=$($a.rc))" }
}

# Gốc kho chứa dấu phân cách PATH của nền ⇒ AL_DICH (DẪN TỪ gốc) vỡ đôi trên PATH: tiền tố lên ĐẦU PATH của script VÀ của
# wrapper lease. Đo trên c8c2c6a: `python` giả trong tiền tố ⇒ 6/6 cổng ĐẠT, rc=0. Từ chối như gốc có wildcard (t10).
Ca 't22 goc kho co dau phan cach PATH => rc=2, noi dung nguyen nhan' {
    $k = Dung-Kho
    $moi = Join-Path (Split-Path $k) ('a' + $Sep + 'b')
    New-Item -ItemType Directory -Force -Path $moi | Out-Null
    & git clone -q $k (Join-Path $moi 'k')
    if ($LASTEXITCODE -ne 0) { throw "git clone vao duong dan co dau phan cach PATH that bai (rc=$LASTEXITCODE)" }
    New-Item -ItemType Directory -Force -Path (Join-Path $moi (Join-Path 'k' (Join-Path 'dist' 'actionlint'))) | Out-Null
    $a = Chay (Join-Path $moi 'k')
    if ($a.rc -ne 2 -or $a.ra -notmatch 'phân cách PATH') { throw "goc co dau phan cach PATH ma khong bi tu choi dung cho (rc=$($a.rc))" }
}

# Tim-Python trả `.Source` của tệp ĐÃ KIỂM, không trả TÊN: sau nó `dist/actionlint` lên ĐẦU PATH, nên `python` theo tên lúc chạy cổng
# có thể là tệp KHÁC (đo trên c8c2c6a: `python` giả trong `dist/actionlint` ⇒ 6/6 ĐẠT, rc=0). Đường vào ấy nay bị danh sách CHO PHÉP
# chặn trước (t25), nên ca đo THẲNG trên hàm — nạp NGUYÊN VĂN `Tim-Python` từ AST như t11 — để chốt này có ca riêng.
Ca 't23 Tim-Python tra DUONG DAN tep da kiem, khong tra TEN' {
    $ast = [System.Management.Automation.Language.Parser]::ParseFile($Script, [ref]$null, [ref]$null)
    $fn = $ast.Find({ param($n) $n -is [System.Management.Automation.Language.FunctionDefinitionAst] -and $n.Name -eq 'Tim-Python' }, $true)
    if (-not $fn) { throw 'khong thay ham Tim-Python trong script' }
    $d = Join-Path ([IO.Path]::GetTempPath()) ('ccw-' + [guid]::NewGuid().ToString('N').Substring(0, 10))
    $script:Rac += $d
    New-Item -ItemType Directory -Force -Path $d | Out-Null
    $h = Join-Path $d 'h.ps1'
    Set-Content -LiteralPath $h -Encoding utf8NoBOM -Value ("Set-StrictMode -Version Latest`n" + $fn.Extent.Text + "`n" +
        '$p = Tim-Python; Write-Host ("TEN=" + $(if ($p) { $p.Ten } else { "(null)" }))')
    $ra = (Doc-Utf8 { & $PwshExe -NoProfile -File $h 2>&1 } | ForEach-Object { "$_" }) -join "`n"
    $m = [regex]::Match($ra, '(?m)^TEN=(.+)$')
    if (-not $m.Success -or $m.Groups[1].Value.Trim() -eq '(null)') { throw "harness khong tim duoc Python: $ra" }
    # Có dấu cheo ⇒ đường dẫn (`.Source` tuyệt đối, hoặc tương đối khi PATH có mục tương đối); không có ⇒ TÊN.
    $ten = $m.Groups[1].Value.Trim()
    if ($ten.IndexOfAny([char[]]@('/', '\')) -lt 0) { throw "Tim-Python tra TEN '$ten', khong tra duong dan tep da kiem" }
}

# Tệp THEO DÕI dưới `dist/actionlint` (bị `.gitignore`, chỉ vào được bằng `git add -f`) là dữ liệu của NHÁNH, mà thư mục ấy lên
# ĐẦU PATH của wrapper lease (gọi `python` theo tên). Đo trên c8c2c6a với wrapper thật: lease ĐẠT dù bộ test thoát 1.
Ca 't24 tep THEO DOI duoi dist/actionlint => rc=2' {
    $k = Dung-Kho
    $al = Join-Path $k (Join-Path 'dist' 'actionlint')
    New-Item -ItemType Directory -Force -Path $al | Out-Null
    Set-Content -LiteralPath (Join-Path $al 'python') -Value "#!/bin/sh`nexit 0" -Encoding utf8NoBOM
    & git -C $k add -f -- dist/actionlint
    & git -C $k -c user.email=t@t -c user.name=t commit -qm theo-doi
    $a = Chay $k
    if ($a.rc -ne 2 -or $a.ra -notmatch 'THEO DÕI') { throw "dist/actionlint co tep theo doi ma khong bi tu choi (rc=$($a.rc))" }
}

# Thư mục đầu PATH (của script lẫn wrapper lease, vốn gọi `python` theo tên) chỉ được chứa TÊN mà installer sinh ra — danh sách
# CHO PHÉP. Hai đường git KHÔNG thấy (tệp, symlink `dist` CHƯA theo dõi), mỗi đường một lượt. Lượt 8 đo trên 623864e với wrapper +
# installer thật: symlink `dist` THEO DÕI ⇒ `lease-publish selftest` ĐẠT dù bộ test thoát 1 (131c2e7: ĐỎ) — dạng THEO DÕI nay do
# chốt `ls-files` chặn trước (t27).
Ca 't25 dist/actionlint chua thu installer khong sinh ra => rc=2' {
    $k = Dung-Kho
    $al = Join-Path $k (Join-Path 'dist' 'actionlint')
    New-Item -ItemType Directory -Force -Path $al | Out-Null
    Set-Content -LiteralPath (Join-Path $al 'python') -Value "#!/bin/sh`nexit 0" -Encoding utf8NoBOM
    $a = Chay $k
    if ($a.rc -ne 2 -or $a.ra -notmatch 'installer không sinh ra') { throw "python CHUA theo doi trong dist/actionlint ma khong bi tu choi (rc=$($a.rc))" }
    # Symlink/junction `dist` CHƯA theo dõi — thứ git không thấy (`ls-files -- dist` rỗng), nên chỉ danh sách CHO PHÉP chặn được.
    # (Symlink `dist` THEO DÕI thì chốt `ls-files` chặn trước — t27.)
    $k2 = Dung-Kho
    $t = Join-Path $k2 (Join-Path 'tools' 'actionlint')
    New-Item -ItemType Directory -Force -Path $t | Out-Null
    Set-Content -LiteralPath (Join-Path $t 'python') -Value "#!/bin/sh`nexit 0" -Encoding utf8NoBOM
    if ($IsWindows) { New-Item -ItemType Junction -Path (Join-Path $k2 'dist') -Target (Join-Path $k2 'tools') | Out-Null }
    else { & ln -s tools (Join-Path $k2 'dist') }
    if (@(& git -C $k2 ls-files -- 'dist').Count -ne 0 -or
        -not (Test-Path -LiteralPath (Join-Path $k2 (Join-Path 'dist' (Join-Path 'actionlint' 'python'))))) {
        throw 'KHONG DO DUOC: kho gia khong dung duoc symlink dist CHUA theo doi tro toi actionlint/python' }
    $b = Chay $k2
    # Từ lượt Codex 5479765901 chốt reparse-point (t36) chặn TRƯỚC danh sách CHO PHÉP: symlink `dist` chưa theo dõi bị từ chối dù đích có gì.
    if ($b.rc -ne 2 -or $b.ra -notmatch 'symlink/junction') { throw "symlink dist tro sang thu muc co python ma khong bi tu choi (rc=$($b.rc))" }
}

# `-FilePath` của Start-Process là MẪU: đường dẫn công cụ chứa `[ ]` làm nó chạy tệp KHÁC tệp đã kiểm (đo trên 623864e: đã kiểm
# `…/p[1]/python`, chạy `…/p1/python` ⇒ 6/6 ĐẠT, rc=0; bash dưới `b[1]` cũng vậy, có sẵn từ trước). Nạp NGUYÊN VĂN `Chay-Cong` như
# t19; Start-Process giả ĐẾM lời gọi và trả rc=0, nên thiếu chốt thì ca thấy `ĐẠT` + một lời gọi.
Ca 't26 duong dan cong cu co wildcard => khong goi Start-Process, KHONG DO DUOC' {
    $ast = [System.Management.Automation.Language.Parser]::ParseFile($Script, [ref]$null, [ref]$null)
    $fn = $ast.Find({ param($n) $n -is [System.Management.Automation.Language.FunctionDefinitionAst] -and $n.Name -eq 'Chay-Cong' }, $true)
    if (-not $fn) { throw 'khong thay ham Chay-Cong trong script' }
    $d = Join-Path ([IO.Path]::GetTempPath()) ('ccw-' + [guid]::NewGuid().ToString('N').Substring(0, 10))
    $script:Rac += $d
    New-Item -ItemType Directory -Force -Path $d | Out-Null
    $h = Join-Path $d 'h.ps1'
    Set-Content -LiteralPath $h -Encoding utf8NoBOM -Value (@'
Set-StrictMode -Version Latest
[Console]::OutputEncoding = [Text.UTF8Encoding]::new($false)
$KetQua = New-Object System.Collections.ArrayList
$NhatKy = $PSScriptRoot; $Goc = $PSScriptRoot; $HanGiay = 5; $ChiTiet = $false
$script:SoGoi = 0
function Start-Process {
    $script:SoGoi++
    $o = [pscustomobject]@{ HasExited = $true; ExitCode = 0 }
    $o | Add-Member -MemberType ScriptMethod -Name WaitForExit -Value { $true }
    $o | Add-Member -MemberType ScriptMethod -Name WaitForExitAsync -Value { [Threading.Tasks.Task]::CompletedTask }
    return $o
}
'@ + "`n" + $fn.Extent.Text + "`n" + @'
Chay-Cong -Ten 'gia' -Tep (Join-Path (Join-Path $PSScriptRoot 'p[1]') 'python') -DoiSo @()
Write-Host ("TRANG_THAI=" + $(switch ($KetQua[0].TrangThai) { 'ĐẠT' { 'DAT' } 'ĐỎ' { 'DO' } 'KHÔNG ĐO ĐƯỢC' { 'KDD' } default { '?' } }) + " SO_GOI=" + $script:SoGoi)
'@)
    $ra = (Doc-Utf8 { & $PwshExe -NoProfile -File $h 2>&1 } | ForEach-Object { "$_" }) -join "`n"
    if ($ra -notmatch 'TRANG_THAI=') { throw "harness khong chay toi het Chay-Cong: $ra" }
    if ($ra -notmatch 'TRANG_THAI=KDD SO_GOI=0') { throw "duong dan co wildcard van duoc dua cho Start-Process: $ra" }
}

# `dist` THEO DÕI ở hai dạng mà `ls-files -- dist/actionlint` không thấy, mỗi dạng một lượt, kèm `actionlint` giả — TÊN nằm trong danh
# sách CHO PHÉP, nên chỉ chốt `ls-files` cản được. Đo trên f1f753b với cổng `cong_cu kiem-tra` THẬT và symlink `dist` theo dõi: ĐẠT,
# script rc=0 (không có actionlint: cổng rc=3 ĐỎ). Windows: symlink theo dõi đòi `core.symlinks`, nên lượt ấy ghi mục 120000 vào index.
Ca 't27 dist THEO DOI (symlink dist, DIST/...) kem actionlint gia => rc=2' {
    $k = Dung-Kho
    $t = Join-Path $k (Join-Path 'tools' 'actionlint')
    New-Item -ItemType Directory -Force -Path $t | Out-Null
    Set-Content -LiteralPath (Join-Path $t 'actionlint') -Value "#!/bin/sh`nexit 0" -Encoding utf8NoBOM
    & git -C $k add -A
    if ($IsWindows) {
        # Blob của symlink phải đúng 5 byte `tools`: dẫn chuỗi qua ỐNG vào lệnh ngoài thì pwsh THÊM dấu xuống dòng của nền (đo trên
        # Linux: blob 6 byte, checkout ra symlink trỏ tới `tools` + LF — treo). Ghi tệp tạm KHÔNG xuống dòng rồi băm nó.
        $dich = Join-Path (Split-Path $k) 'dich-symlink'
        [IO.File]::WriteAllBytes($dich, [Text.Encoding]::ASCII.GetBytes('tools'))
        $sha = @(& git -C $k hash-object -w --no-filters -- $dich)[0]
        & git -C $k update-index --add --cacheinfo "120000,$sha,dist"
    } else {
        & ln -s tools (Join-Path $k 'dist')
        & git -C $k add -A
    }
    & git -C $k -c user.email=t@t -c user.name=t commit -qm symlink
    if (@(& git -C $k ls-files -- 'dist/actionlint').Count -ne 0 -or @(& git -C $k ls-files -- 'dist').Count -ne 1 -or
        [string]@(& git -C $k cat-file -s ':dist')[0] -ne '5') {
        throw 'KHONG DO DUOC: kho gia khong dung duoc symlink dist -> tools THEO DOI ma ls-files dist/actionlint rong' }
    $a = Chay $k
    if ($a.rc -ne 2 -or $a.ra -notmatch 'THEO DÕI') { throw "symlink dist THEO DOI kem actionlint gia ma khong bi tu choi (rc=$($a.rc))" }
    # `GIT_LITERAL_PATHSPECS` đọc pathspec NGUYÊN VĂN: dạng `:(icase)dist` thành tên tệp lạ ⇒ rỗng ⇒ lọt; cờ `--icase-pathspecs` thì
    # git từ chối (rc=128) ⇒ phải rc=2.
    $c = Chay $k @() @{ GIT_LITERAL_PATHSPECS = '1' }
    if ($c.rc -ne 2 -or $c.ra -notmatch 'không hỏi được git') { throw "GIT_LITERAL_PATHSPECS lam chot ls-files mu (rc=$($c.rc))" }
    # `DIST/…` theo dõi: trên hệ tệp không phân biệt hoa thường (NTFS, APFS) nó CHÍNH LÀ `dist/actionlint`.
    $k2 = Dung-Kho
    $al = Join-Path $k2 (Join-Path 'DIST' 'actionlint')
    New-Item -ItemType Directory -Force -Path $al | Out-Null
    Set-Content -LiteralPath (Join-Path $al 'actionlint') -Value "#!/bin/sh`nexit 0" -Encoding utf8NoBOM
    & git -C $k2 add -f -- DIST
    & git -C $k2 -c user.email=t@t -c user.name=t commit -qm hoa-thuong
    if (@(& git -C $k2 ls-files -- 'dist/actionlint').Count -ne 0 -or @(& git -C $k2 ls-files -- 'DIST').Count -ne 1) {
        throw 'KHONG DO DUOC: kho gia khong dung duoc DIST/actionlint THEO DOI ma ls-files dist/actionlint rong' }
    $b = Chay $k2
    if ($b.rc -ne 2 -or $b.ra -notmatch 'THEO DÕI') { throw "DIST/actionlint THEO DOI ma khong bi tu choi (rc=$($b.rc))" }
}

# Danh sách CHO PHÉP là của NỀN ĐANG CHẠY, không phải hợp hai nền. Gói Windows ghim chỉ có `actionlint.exe`, nên `actionlint` KHÔNG
# đuôi ở đó không bao giờ bị lượt cài giải nén đè — và `ops/cai_actionlint.sh` còn chọn nó TRƯỚC `.exe` để đối chiếu bản (đo trên
# 543f2e8: installer thật, `AL_NEN=Windows`, gói Windows thật, `actionlint` giả in `1.7.7` ⇒ rc=0, băm tệp giả không đổi; danh sách
# hợp hai nền cho nó qua). Lượt 1: tên chỉ nền KHÁC sinh ra ⇒ rc=2. Lượt 2 (đối chứng): đúng bộ tên installer sinh ra trên nền này
# ⇒ KHÔNG bị chặn — thiếu lượt này thì một danh sách RỖNG hay thiếu tên vẫn qua ca.
Ca 't28 dist/actionlint chua ten cua NEN KHAC => rc=2; ten cua nen nay => qua' {
    $khac = if ($IsWindows) { 'actionlint' } else { 'actionlint.exe' }
    $nay  = if ($IsWindows) { @('actionlint.exe', 'goi.zip', 'goi_giai_nen.zip') } else { @('actionlint', 'goi.gz', 'goi_giai_nen.tar.gz') }
    $k = Dung-Kho
    $al = Join-Path $k (Join-Path 'dist' 'actionlint')
    New-Item -ItemType Directory -Force -Path $al | Out-Null
    Set-Content -LiteralPath (Join-Path $al $khac) -Value "#!/bin/sh`necho 1.7.7" -Encoding utf8NoBOM
    $a = Chay $k
    if ($a.rc -ne 2 -or $a.ra -notmatch "installer không sinh ra: $([regex]::Escape($khac))") {
        throw "ten cua nen khac '$khac' trong dist/actionlint ma khong bi tu choi (rc=$($a.rc))" }
    $k2 = Dung-Kho
    $al2 = Join-Path $k2 (Join-Path 'dist' 'actionlint')
    foreach ($d in 'docs', 'man') { New-Item -ItemType Directory -Force -Path (Join-Path $al2 $d) | Out-Null }
    foreach ($f in @('LICENSE.txt', 'README.md') + $nay) { Set-Content -LiteralPath (Join-Path $al2 $f) -Value 'x' -Encoding utf8NoBOM }
    $b = Chay $k2
    if ($b.rc -ne 0 -or $b.ra -match 'installer không sinh ra') { throw "bo ten installer sinh ra tren nen nay bi chan (rc=$($b.rc))" }
}

# `dist` THEO DÕI là dữ liệu của nhánh: script phải từ chối nó TRƯỚC khi ghi bất cứ gì qua nó. Đo trên eba9b1d: thư mục nhật ký
# `dist/cong-windows` được tạo TRƯỚC chốt `ls-files` ⇒ symlink `dist` theo dõi sang `tools` làm `tools/cong-windows` mọc ra, rồi
# mới rc=2. Windows: mục 120000 trong index (như t27) cộng junction `dist` → `tools`, để cây làm việc đi qua đúng đích ấy.
Ca 't29 dist THEO DOI => tu choi TRUOC khi ghi qua no' {
    $k = Dung-Kho
    $t = Join-Path $k 'tools'
    New-Item -ItemType Directory -Force -Path $t | Out-Null
    Set-Content -LiteralPath (Join-Path $t 'giu') -Value 'x' -Encoding utf8NoBOM
    & git -C $k add -A
    if ($IsWindows) {
        $dich = Join-Path (Split-Path $k) 'dich-symlink'
        [IO.File]::WriteAllBytes($dich, [Text.Encoding]::ASCII.GetBytes('tools'))
        $sha = @(& git -C $k hash-object -w --no-filters -- $dich)[0]
        & git -C $k update-index --add --cacheinfo "120000,$sha,dist"
        New-Item -ItemType Junction -Path (Join-Path $k 'dist') -Target $t | Out-Null
    } else {
        & ln -s tools (Join-Path $k 'dist')
        & git -C $k add -A
    }
    & git -C $k -c user.email=t@t -c user.name=t commit -qm symlink
    if (@(& git -C $k ls-files -- 'dist').Count -ne 1 -or -not (Test-Path -LiteralPath (Join-Path $k (Join-Path 'dist' 'giu')))) {
        throw 'KHONG DO DUOC: kho gia khong dung duoc dist THEO DOI di qua tools' }
    $a = Chay $k
    if ($a.rc -ne 2 -or $a.ra -notmatch 'THEO DÕI') { throw "dist THEO DOI ma khong bi tu choi (rc=$($a.rc))" }
    $sot = @(Get-ChildItem -LiteralPath $t -Force | Where-Object { $_.Name -ne 'giu' } | ForEach-Object Name)
    if ($sot.Count -gt 0) { throw "script ghi qua dist THEO DOI TRUOC khi tu choi: tools/$($sot -join ', tools/')" }
}

# `env:` của bước cổng là một phần của lệnh. Vế tĩnh (đúng ở cả hai phía merge): mọi khoá `env` — tầng workflow, job VÀ bước — của
# job `gate*` trong ci.yml và của mọi job trong `ci-dot-bien-du.yml` (lượt tuần; nhánh gốc d553efa chưa có tệp ấy) phải có mặt trong
# script (hằng chuỗi hoặc `$env:`) — thêm khoá mà quên script thì ĐỎ. Vế hành vi: MỌI khoá ấy (cộng danh sách cố định dưới đây, để vế
# này có răng cả ở cây không có tệp lượt tuần) RÒ từ phiên gọi; đồ giả THOÁT 0 CHỈ KHI env nó thấy đúng kỳ vọng. Đo trên cây merge
# 20ec8d5 với 87eea22: vắng env ⇒ registry ĐỦ ×3 (`nhanh_don_duoc_test` ĐỦ > 540 s, NHẸ 2 s); `CONG_CU_TEST_BAN_KINH=manh` rò ⇒
# `cong_cu_test` rc=0 mà bỏ trọn bán kính 416 đột biến. Đo với b5a9f79: `CONG_CU_TEST_MANH=15/16` rò ⇒ `cong_cu_test` rc=0, 26/416,
# bỏ cổng cây thật; `NHANH_DON_DUOC_MANH=7/8` rò ⇒ `nhanh_don_duoc_test` chạy MẢNH 783 s thay vì NHẸ 2 s, registry ĐỎ vì máy.
Ca 't30 env cua buoc cong: khoa ci.yml co mat, bien ro bi xoa, registry mang env pull_request khi do duoc diff' {
    $ci = Join-Path $GocKho '.github/workflows/ci.yml'
    $py = Tim-PyYaml; $pd = $py.Dau
    $ma = "import os,sys,yaml`ndef k(p,chon):`n d=yaml.safe_load(open(p,encoding='utf-8')); s=set(d.get('env') or {})`n" +
          " for j,v in (d.get('jobs') or {}).items():`n  if chon(j): s|=set(v.get('env') or {})|{x for b in (v.get('steps') or []) for x in (b.get('env') or {})}`n return s`n" +
          "s=k(sys.argv[1],lambda j:j.startswith('gate'))`nt=os.path.join(os.path.dirname(sys.argv[1]),'ci-dot-bien-du.yml')`n" +
          "s|=k(t,lambda j:True) if os.path.exists(t) else set()`nprint(chr(10).join(sorted(s)))"
    $khoa = @(& $py.Ten @pd -c $ma $ci | Where-Object { $_ })
    if ($LASTEXITCODE -ne 0 -or $khoa.Count -eq 0) { throw "KHONG DO DUOC: khong doc duoc khoa env cua job gate* trong ci.yml (rc=$LASTEXITCODE)" }
    $ast = [System.Management.Automation.Language.Parser]::ParseFile($Script, [ref]$null, [ref]$null)
    $co = @{}
    foreach ($n in $ast.FindAll({ param($x) $x -is [System.Management.Automation.Language.StringConstantExpressionAst] }, $true)) { $co[$n.Value] = 1 }
    foreach ($n in $ast.FindAll({ param($x) $x -is [System.Management.Automation.Language.VariableExpressionAst] -and $x.VariablePath.DriveName -eq 'env' }, $true)) {
        $co[$n.VariablePath.UserPath.Substring(4)] = 1 }
    $thieu = @($khoa | Where-Object { -not $co.ContainsKey($_) })
    if ($thieu.Count -gt 0) { throw "khoa env cua job gate* / luot tuan khong co trong script: $($thieu -join ', ')" }
    # Khoá RÒ: tập đọc từ workflow ∪ danh sách cố định; trừ PYTHON* (script tự đặt, job CI cũng đặt). AL_VER và CI_DANG_KY_* script
    # đặt lại sau khi xoá, nên đồ giả `cong_cu_test` (chạy TRƯỚC registry) đòi vắng mọi khoá trừ AL_VER, đồ giả registry đòi vắng mọi
    # khoá trừ AL_VER và bốn khoá nó tự đặt.
    $tenRo = @(@($khoa) + @('CONG_CU_TEST_BAN_KINH', 'CONG_CU_TEST_MANH', 'CONG_CU_TEST_MANH_RA', 'CI_DANG_KY_DOT_BIEN_MANH',
                            'NHANH_DON_DUOC_MANH', 'NHANH_DON_DUOC_MANH_RA', 'PR_HEAD_SHA', 'EOL_BASE_SHA', 'CI_DUONG_NHANH_SU_KIEN',
                            'CI_DUONG_NHANH_GOC', 'CI_DUONG_NHANH_DAU', 'CI_DUONG_NHANH_MERGE') |
               Where-Object { $_ -notlike 'PYTHON*' } | Sort-Object -Unique)
    $k = Dung-Kho
    Set-Content -LiteralPath (Join-Path $k '.claude/dev/ci_dang_ky_test.py') -Encoding utf8NoBOM -Value @'
import os, sys
g = lambda n: os.environ.get(n) or ""
thay = "|".join(g(n) for n in ("CI_DANG_KY_WORKERS", "CI_DANG_KY_SU_KIEN", "CI_DANG_KY_GOC", "CI_DANG_KY_DAU", "CI_DANG_KY_DOT_BIEN_MANH"))
dat = {"AL_VER", "CI_DANG_KY_WORKERS", "CI_DANG_KY_SU_KIEN", "CI_DANG_KY_GOC", "CI_DANG_KY_DAU"}
ro = [n for n in os.environ.get("STUB_KHOA_RO", "").split(",") if n and n not in dat and n in os.environ]
print("REG_ENV=" + thay + " RO=" + ",".join(ro))
sys.exit(0 if thay == os.environ.get("STUB_REG_MONG") and not ro else 7)
'@
    Set-Content -LiteralPath (Join-Path $k 'ops/cong_cu_test.py') -Encoding utf8NoBOM -Value @'
import os, sys
ro = [n for n in os.environ.get("STUB_KHOA_RO", "").split(",") if n and n != "AL_VER" and n in os.environ]
print("CC_RO=" + ",".join(ro))
sys.exit(7 if ro else 0)
'@
    & git -C $k add -A
    & git -C $k -c user.email=t@t -c user.name=t commit -qm stub-env
    & git -C $k update-ref refs/remotes/origin/master HEAD
    Set-Content -LiteralPath (Join-Path $k 'di-truoc-t30') -Value 'x' -Encoding utf8NoBOM
    & git -C $k add -A
    & git -C $k -c user.email=t@t -c user.name=t commit -qm di-truoc
    $goc = @(& git -C $k rev-parse 'refs/remotes/origin/master')[0]; $dau = @(& git -C $k rev-parse HEAD)[0]
    # Biến RÒ từ phiên gọi — MỌI khoá ở trên; GOC/DAU cố ý đảo — phải bị xoá hoặc đè ở mọi lượt.
    $ro = @{ STUB_KHOA_RO = ($tenRo -join ',') }
    foreach ($n in $tenRo) { $ro[$n] = 'ro' }
    $ro['CONG_CU_TEST_BAN_KINH'] = 'manh'; $ro['CI_DANG_KY_DOT_BIEN_MANH'] = 'ops/nhanh_don_duoc_test.py'; $ro['CI_DANG_KY_SU_KIEN'] = 'push'
    $ro['CI_DANG_KY_GOC'] = $dau; $ro['CI_DANG_KY_DAU'] = $goc
    $a = Chay $k @() ($ro + @{ STUB_REG_MONG = "2|pull_request|$goc|$dau|" })
    if ($a.ra -notmatch 'cong_cu_test\s+rc=0') { throw "bien che do ro tu phien goi toi cong_cu_test (rc_script=$($a.rc))" }
    if ($a.ra -notmatch 'registry test\s+rc=0') { throw "cay SACH + di truoc origin/master ma registry khong mang env pull_request dung GOC/DAU, hoac bien ro toi registry (rc_script=$($a.rc))" }
    Set-Content -LiteralPath (Join-Path $k 'ban-t30') -Value 'x' -Encoding utf8NoBOM
    try { $b = Chay $k @() ($ro + @{ STUB_REG_MONG = '2||||' }) } finally { Remove-Item -LiteralPath (Join-Path $k 'ban-t30') -Force }
    if ($b.ra -notmatch 'registry test\s+rc=0') { throw "cay BAN ma registry van mang env diff (rc_script=$($b.rc))" }
    # `git status` TIN cờ index: tệp THEO DÕI bị sửa mà mang cờ assume-unchanged / skip-worktree thì status RỖNG — mỗi cờ một lượt.
    foreach ($coIdx in '--assume-unchanged', '--skip-worktree') {
        Set-Content -LiteralPath (Join-Path $k 'di-truoc-t30') -Value 'sua' -Encoding utf8NoBOM
        & git -C $k update-index $coIdx -- 'di-truoc-t30'
        try {
            if (@(& git -C $k status --porcelain --untracked-files=all).Count -ne 0) { throw "KHONG DO DUOC: $coIdx khong che duoc sua doi" }
            $e = Chay $k @() ($ro + @{ STUB_REG_MONG = '2||||' })
        } finally {
            & git -C $k update-index ($coIdx -replace '^--', '--no-') -- 'di-truoc-t30'
            & git -C $k checkout -q -- 'di-truoc-t30'
        }
        if ($e.ra -notmatch 'registry test\s+rc=0') { throw "tep sua mang co $coIdx (status rong) ma registry van mang env diff (rc_script=$($e.rc))" }
    }
    & git -C $k update-ref refs/remotes/origin/master HEAD
    $c = Chay $k @() ($ro + @{ STUB_REG_MONG = '2||||' })
    if ($c.ra -notmatch 'registry test\s+rc=0') { throw "HEAD khong di truoc origin/master ma registry van mang env diff (rc_script=$($c.rc))" }
}

# Biến của TRÌNH THÔNG DỊCH / git / bash từ phiên gọi — job CI không có biến nào trong số đó, nên chúng là một phần của lệnh như `env:`
# của bước (t30). Đo với 34e7a9d: `PYTHONOPTIMIZE=1` gỡ mọi `assert` trần ⇒ cổng `assert False` ĐẠT, script rc=0 (đích THẬT:
# `lease_publish_test.py --chi-ca=t33_` với workflow actionlint ĐỎ ⇒ rc=0 `1/1 đạt`); `GIT_WORK_TREE` trỏ bản sạch ⇒ `git status` đo
# cây KHÁC ⇒ registry mang env `pull_request` trên cây BẨN; `GIT_DIR` trỏ kho khác ⇒ nếp git ghi vào config kho ấy; `BASH_ENV` ⇒ bash
# nạp tệp ấy trước wrapper lease. Tập biến git lấy từ CHÍNH git (`rev-parse --local-env-vars`, trừ `GIT_CONFIG*` — t13 khoá đường ấy
# bằng giá trị CÓ HIỆU LỰC); mỗi biến mang giá trị LÀNH trừ hai biến đo hệ quả, nên đột biến bỏ một tên chết vì đồ giả THẤY tên ấy.
Ca 't31 bien trinh thong dich / git / bash cua phien goi bi xoa truoc cong' {
    $gitCucBo = @(& git rev-parse --local-env-vars | Where-Object { $_ -and $_ -notlike 'GIT_CONFIG*' })
    if ($LASTEXITCODE -ne 0 -or $gitCucBo.Count -eq 0) { throw "KHONG DO DUOC: git rev-parse --local-env-vars (rc=$LASTEXITCODE)" }
    $ast = [System.Management.Automation.Language.Parser]::ParseFile($Script, [ref]$null, [ref]$null)
    $co = @{}
    foreach ($n in $ast.FindAll({ param($x) $x -is [System.Management.Automation.Language.StringConstantExpressionAst] }, $true)) { $co[$n.Value] = 1 }
    $thieu = @(@($gitCucBo) + 'BASH_ENV' + 'BASH_FUNC_*' | Where-Object { -not $co.ContainsKey($_) })
    if ($thieu.Count -gt 0) { throw "bien git cuc bo cua kho / BASH_ENV / BASH_FUNC_* khong co trong script: $($thieu -join ', ')" }
    $k = Dung-Kho
    $d = Split-Path $k
    $ktRo = "import os, sys`nro = [n for n in os.environ.get('STUB_KHOA_RO', '').split(',') if n and n in os.environ]`n" +
            "ro += [n for n in os.environ if n.upper().startswith('PYTHON') and n.upper() not in ('PYTHONUTF8', 'PYTHONIOENCODING', 'PYTHONUNBUFFERED', 'PYTHONDONTWRITEBYTECODE')]`n"
    Set-Content -LiteralPath (Join-Path $k 'ops/cong_cu_test.py') -Encoding utf8NoBOM -Value ($ktRo + "print('CC_RO=' + ','.join(ro)); sys.exit(7 if ro else 0)")
    Set-Content -LiteralPath (Join-Path $k '.claude/dev/ci_dang_ky_test.py') -Encoding utf8NoBOM -Value ($ktRo +
        "thay = '|'.join(os.environ.get(n) or '' for n in ('CI_DANG_KY_WORKERS', 'CI_DANG_KY_SU_KIEN', 'CI_DANG_KY_GOC', 'CI_DANG_KY_DAU'))`n" +
        "print('REG_ENV=' + thay + ' RO=' + ','.join(ro)); sys.exit(0 if thay == '2|||' and not ro else 7)")
    # Cổng Python chỉ ĐỎ được qua `assert` trần.
    Set-Content -LiteralPath (Join-Path $k '.claude/dev/packet_loop_test.py') -Encoding utf8NoBOM -Value "assert False, 'assert phai chay'"
    & git -C $k add -A
    & git -C $k -c user.email=t@t -c user.name=t commit -qm stub-t31
    & git -C $k update-ref refs/remotes/origin/master HEAD
    Set-Content -LiteralPath (Join-Path $k 'vung-t31') -Value 'x' -Encoding utf8NoBOM
    & git -C $k add -A
    & git -C $k -c user.email=t@t -c user.name=t commit -qm di-truoc
    $sach = Join-Path $d 'sach'
    & git clone -q $k $sach
    Set-Content -LiteralPath (Join-Path $k 'vung-t31') -Value 'sua' -Encoding utf8NoBOM
    if (@(& git -C $k status --porcelain).Count -eq 0) { throw 'KHONG DO DUOC: kho gia khong BAN' }
    $khac = Join-Path $d 'khac'
    & git init -q $khac
    $dau = Join-Path $d 'dau-bash-env'
    $benv = Join-Path $d 'benv.sh'
    Set-Content -LiteralPath $benv -Value ("echo nap >> '" + $dau.Replace([string][char]92, '/') + "'") -Encoding utf8NoBOM
    $rong = Join-Path $d 'obj-rong'
    New-Item -ItemType Directory -Force -Path $rong | Out-Null
    $lanh = @{ GIT_INDEX_FILE = (Join-Path $k '.git/index'); GIT_OBJECT_DIRECTORY = (Join-Path $k '.git/objects')
               GIT_ALTERNATE_OBJECT_DIRECTORIES = $rong; GIT_COMMON_DIR = (Join-Path $k '.git'); GIT_IMPLICIT_WORK_TREE = '1'
               GIT_GRAFT_FILE = (Join-Path $d 'graft-khong-co'); GIT_SHALLOW_FILE = (Join-Path $d 'shallow-khong-co')
               GIT_NO_REPLACE_OBJECTS = '1'; GIT_REPLACE_REF_BASE = 'refs/replace/'; GIT_PREFIX = 'x/' }
    # Hàm bash EXPORT mang tên lệnh NỘI TRÚ `exit` (wrapper giả kết thúc bằng `exit`): ghi tệp đánh dấu rồi `builtin exit` giữ rc.
    $dauHam = Join-Path $d 'dau-bash-func'
    $ro = @{ PYTHONOPTIMIZE = '1'; PYTHONWARNINGS = 'ignore'; PYTHONHASHSEED = '0'; BASH_ENV = $benv
             GIT_DIR = (Join-Path $khac '.git'); GIT_WORK_TREE = $sach
             STUB_KHOA_RO = (@(@($gitCucBo) + 'BASH_ENV' + 'BASH_FUNC_exit%%') -join ',') }
    $ro['BASH_FUNC_exit%%'] = '() { echo nap >> ''' + $dauHam.Replace([string][char]92, '/') + '''; builtin exit "$@"; }'
    foreach ($n in $gitCucBo) { if (-not $ro.ContainsKey($n)) { $ro[$n] = if ($lanh.ContainsKey($n)) { $lanh[$n] } else { Join-Path $d "khong-co-$n" } } }
    $a = Chay $k @() $ro
    if ($a.ra -notmatch 'packet-loop selftest +rc=1' -or $a.ra -notmatch 'assert phai chay') {
        throw "PYTHON* ro tu phien goi: assert tran bi go, cong khong do gi (rc_script=$($a.rc))" }
    if ($a.ra -notmatch 'cong_cu_test +rc=0') { throw "bien trinh thong dich / git / BASH_ENV ro toi cong_cu_test (rc_script=$($a.rc))" }
    if ($a.ra -notmatch 'registry test +rc=0') {
        throw "GIT_WORK_TREE ro: cay BAN duoc do la SACH nen registry mang env diff, hoac bien ro toi registry (rc_script=$($a.rc))" }
    if ($a.ra -notmatch 'lease-publish selftest +rc=') { throw 'KHONG DO DUOC: cong bash khong chay, ve BASH_ENV khong co rang' }
    if (Test-Path -LiteralPath $dau) { throw "BASH_ENV ro tu phien goi: bash nap tep ay truoc cong ($(@(Get-Content -LiteralPath $dau).Count) lan)" }
    if (Test-Path -LiteralPath $dauHam) { throw "BASH_FUNC_* ro tu phien goi: ham export che lenh noi tru exit ($(@(Get-Content -LiteralPath $dauHam).Count) lan)" }
    $ab = @(& git -C $khac config --local --get core.abbrev)
    if ($ab.Count -gt 0) { throw "GIT_DIR ro tu phien goi: nep git ghi vao config cua KHO KHAC (core.abbrev=$($ab -join ''))" }
}

# Gương CI trôi theo master: `ci.yml` thêm một bước `gate*` mà script không gương và không khai `KHÔNG CHẠY` thì không ca nào ở trên ĐỎ
# (t6 chỉ đọc bước bỏ trên Windows, t30 chỉ đọc khoá `env`). Đo: cây merge ad4e724 với master 7e5958e có bước `ci-duong-nhanh selftest`
# (`ops/ci_duong_nhanh_test.py`, chỉ Linux) — script ad4e724 im lặng, bộ 31 ca chỉ đỏ t30. Bước chỉ chạy ở chế độ `duong_nhanh` thì
# bỏ: script luôn chạy ĐỦ. Python in UTF-8 (tên bước có tiếng Việt; console Windows không phải UTF-8); mã Python không dùng dấu chéo
# ngược lẫn dấu nháy kép (đối số `-c` đi qua lớp trích dẫn của Windows).
# Hai lớp canh, mỗi lớp một việc — lớp thứ hai tồn tại vì lớp thứ nhất là PHÉP CHIẾU, và phép chiếu nào cũng có kênh nó không chiếu:
#   (1) Bộ so TỪNG DÒNG (`Doc-DichCi` + `Tim-ThieuGuong`) nói bước nào thiếu gương. So LỆNH, không so TỆP (`scripts/tl.py` là đích của 11 bước): mỗi (đích + MỌI đối
#       số sau nó, tới toán tử shell đầu tiên) của ci.yml phải BẰNG đuôi của một mảng/lệnh trong script; đối số script lấy từ BIẾN phải là hằng CÓ MẶT trong script;
#       phần tử nội suy ⇒ khớp mọi giá trị; bước `uses:` ngoài checkout/setup-python/artifact, ghim phiên bản (`pkg==x.y.z`, `AL_VER`), giá trị HẰNG của `env:` (khoá script
#       ĐẶT bằng hằng) và mọi job KHÁC `chuan-bi` đều bị so; bước KHÔNG đích phải có tên trong `$NepCaiDat`; tên chỉ được tha bằng một hằng chuỗi BẮT ĐẦU bằng
#       `KHÔNG CHẠY`/`THAY BẰNG`, tên rỗng thì không bao giờ. KHÔNG thấy: tiền tố trước đích, lệnh không đích nằm trong bước đã gương, `env` kiểu số, nội dung bước không đích
#       (`git config` của "Force LF"), `with:`, job `uses:`, `if:` theo nền, đối số sau toán tử shell, mã Python nhúng (heredoc) — kênh thứ mười ba sẽ lại có kênh thứ mười bốn.
#   (2) Dấu vân từng job (`$DauVanCi`) thấy MỌI thay đổi ở các kênh trên nhưng không nói gì về gương: nó chỉ buộc người sửa `ci.yml` dừng lại rà script rồi ghim lại.
#       `ops/ci_duong_nhanh_test.py` (ca `y13`) đã khoá mọi thứ NGOÀI thân `run:` ở phía CI; dấu vân này khoá luôn THÂN `run:` — chỗ không ca nào khác canh — và cho gương
#       Windows một cò riêng. Lượt 17 nâng từ so (đích, đối số đầu) lên so đuôi; lượt 18 không thêm kênh nào cho (1) mà thêm (2). t34 khoá CẢ HAI lớp bằng kho GIẢ.
$NepCaiDat = @('Force LF checkout (hash parity với manifest)', 'cài PyYAML + jsonschema (cổng đăng lease + validator verdict cần)',
               'cài Ruff 0.15.15 và in probe dương', '<USES>actions/checkout', '<USES>actions/setup-python',
               '<USES>actions/upload-artifact', '<USES>actions/download-artifact')
function Doc-DichCi { param([string]$Ci)
    $py = Tim-PyYaml; $pd = $py.Dau
    $ma = @'
import re, shlex, sys, yaml
sys.stdout.reconfigure(encoding='utf-8')
d = yaml.safe_load(open(sys.argv[1], encoding='utf-8'))
mau = re.compile('(?<![A-Za-z0-9_./-])[A-Za-z0-9_./-]+[.](?:py|sh|ps1)(?![A-Za-z0-9_.])')
pin = re.compile('[A-Za-z][A-Za-z0-9_.-]*==[0-9][A-Za-z0-9.]*')
tab, us, bs = chr(9), chr(31), chr(92)
def duoi(rest):
    try:
        lx = shlex.shlex(rest, posix=True, punctuation_chars=True)
        lx.whitespace_split = True
        tk = list(lx)
    except ValueError:
        return '<KHONG-PHAN-TICH-DUOC>'
    ra = []
    for i, t in enumerate(tk):
        if re.fullmatch('[();<>|&]+', t) or (re.fullmatch('[0-9]+', t) and i + 1 < len(tk) and re.fullmatch('[<>&|]+', tk[i + 1])):
            break
        ra.append('*' if ('$' in t or chr(96) in t) else t)
    return us.join(ra)
def lenh(run):
    ds, cur = [], ''
    for l in run.splitlines():
        if l.strip().startswith('#'):
            continue
        if l.rstrip().endswith(bs):
            cur += l.rstrip()[:-1] + ' '
            continue
        ds.append(cur + l)
        cur = ''
    return ds + ([cur] if cur else [])
def envs(ten, e):
    for k, val in (e or {}).items():
        if isinstance(val, str) and '{{' not in val:
            print(ten + tab + '<ENV>' + tab + k + '=' + val)
            if k == 'AL_VER':
                print(ten + tab + '<PIN>' + tab + val)
for j, v in (d.get('jobs') or {}).items():
    if j == 'chuan-bi':
        continue
    envs('', v.get('env'))
    for b in v.get('steps') or []:
        ten = str(b.get('name') or '')
        if '== ' + chr(39) + 'duong_nhanh' + chr(39) in str(b.get('if', '')):
            continue
        envs(ten, b.get('env'))
        if not b.get('run'):
            print(ten + tab + '<USES>' + str(b.get('uses') or '').split('@')[0] + tab)
            continue
        cap, pins = set(), set()
        for dong in lenh(b['run']):
            for m in mau.finditer(dong):
                cap.add((m.group(0), duoi(dong[m.end():])))
            if 'install' in dong:
                pins.update(pin.findall(dong))
        for t, s in sorted(cap) or [('<KHONG-DICH>', '')]:
            print(ten + tab + t + tab + s)
        for p in sorted(pins):
            print(ten + tab + '<PIN>' + tab + p)
'@
    $r = @(Doc-Utf8 { & $py.Ten @pd -c $ma $Ci } | Where-Object { $_ })
    if ($LASTEXITCODE -ne 0 -or $r.Count -eq 0) { throw "KHONG DO DUOC: khong doc duoc dich cua buoc gate* trong $Ci (rc=$LASTEXITCODE)" }
    return $r
}
function Khop-Duoi { param([string[]]$A, [string[]]$B, [string[]]$Hang)
    $A = @($A); $B = @($B); $Hang = @($Hang)   # $null (đuôi rỗng) không có .Count dưới StrictMode
    if ($A.Count -ne $B.Count) { return $false }
    $bien = [string][char]30
    for ($k = 0; $k -lt $A.Count; $k++) {
        if ($A[$k] -eq '*' -or $B[$k] -eq '*') { continue }
        # Đối số script lấy từ BIẾN (`$t` trong `foreach ($t in 'shellcheck', 'rg')`) khớp được MỌI giá trị — kể cả giá trị mà script không
        # hề có (đo trên c848fee: ci.yml thêm `bash ops/cai_cong_cu.sh jq` ⇒ t32 ĐẠT). Chỉ nhận giá trị ci.yml là một HẰNG có mặt trong script.
        # Ordinal: `StartsWith(string)` so theo VĂN HOÁ, mà ký tự điều khiển (U+001E) là ignorable ⇒ trả True cho MỌI chuỗi (đo trên ICU/pwsh 7.4.6).
        if ($B[$k].StartsWith($bien, [System.StringComparison]::Ordinal)) { if ($Hang -ccontains $A[$k]) { continue } else { return $false } }
        if ($A[$k] -cne $B[$k]) { return $false }
    }
    return $true
}
# Dấu vân từng job: sha256[:12] của JSON chuẩn hoá (khoá xếp thứ tự) của MỌI trường của bước — `run` (bỏ dòng chú thích / dòng trống /
# khoảng trắng cuối dòng), `env`, `with`, `uses`, `if`, `shell`, `working-directory`… — cộng `uses`/`with`/`env`/`if`/`defaults`/`container`/`services`/`continue-on-error` cấp job và `env`/`defaults` cấp workflow (dòng `<workflow>`). Bỏ: job
# `chuan-bi`, bước chỉ chạy ở chế độ `duong_nhanh`, và `timeout-minutes`/`strategy`/`needs`/`runs-on` cấp job (t9 canh trần giờ). Mã Python
# không có dấu nháy kép lẫn dấu chéo ngược (đối số `-c` đi qua lớp trích dẫn của Windows).
function Doc-DauVanCi { param([string]$Ci)
    $py = Tim-PyYaml; $pd = $py.Dau
    $ma = @'
import hashlib, json, sys, yaml
d = yaml.safe_load(open(sys.argv[1], encoding='utf-8'))
def nor(x):
    if isinstance(x, dict):
        return {str(k): nor(v) for k, v in x.items()}
    if isinstance(x, list):
        return [nor(i) for i in x]
    return x if isinstance(x, (str, int, float, bool, type(None))) else str(x)
def buoc(b):
    b = nor(b)
    if isinstance(b.get('run'), str):
        b['run'] = [l.rstrip() for l in b['run'].splitlines() if l.strip() and not l.strip().startswith('#')]
    return b
print('<workflow>' + chr(9) + hashlib.sha256(json.dumps(nor({k: d[k] for k in ('env', 'defaults') if k in d}), sort_keys=True).encode('utf-8')).hexdigest()[:12])
for j, v in sorted((d.get('jobs') or {}).items()):
    if j == 'chuan-bi':
        continue
    goc = nor({k: v[k] for k in ('uses', 'with', 'env', 'if', 'defaults', 'container', 'services', 'continue-on-error') if k in v})
    bs = [buoc(b) for b in v.get('steps') or [] if '== ' + chr(39) + 'duong_nhanh' + chr(39) not in str(b.get('if', ''))]
    print(j + chr(9) + hashlib.sha256(json.dumps([goc, bs], sort_keys=True).encode('utf-8')).hexdigest()[:12])
'@
    $r = @(Doc-Utf8 { & $py.Ten @pd -c $ma $Ci } | Where-Object { $_ })
    if ($LASTEXITCODE -ne 0 -or $r.Count -eq 0) { throw "KHONG DO DUOC: khong tinh duoc dau van job cua $Ci (rc=$LASTEXITCODE)" }
    $h = @{}
    foreach ($x in $r) { $kv = $x -split "`t", 2; $h[$kv[0]] = $kv[1].Trim() }
    return $h
}
# Dấu vân các job của ci.yml trên master 8b59185 (cây merge của PR này không đụng ci.yml). ĐỎ ở đây = một bước `gate*` ĐÃ ĐỔI (thân `run`, env,
# with, uses, if, shell…) — không nói bước nào: đọc `git diff 8b59185 -- .github/workflows/ci.yml`, rà gương trong chay-cong-windows.ps1 (lệnh, tiền tố,
# đối số, ghim, nếp `git config`, `if:` theo nền), RỒI mới dán dòng ghim mới mà thông báo lỗi in sẵn. Bộ so từng dòng (`Tim-ThieuGuong`) chỉ thấy
# những kênh nó biết; dấu vân thấy MỌI kênh (đo trên c848fee: tiền tố `python -O`, lệnh `actionlint` thêm vào bước đã gương, `env` kiểu số, dòng
# `git config` của bước "Force LF", `with: python-version`, job `uses:` tái dùng, `if: runner.os == 'Linux'` — t32 ĐẠT cả chín). Đổi `ci.yml` là
# việc của packet khác: bảng này là CHỖ BUỘC người đó dừng lại một nhịp, không phải chỗ chứng minh gương đúng.
$DauVanCi = @{ '<workflow>' = '44136fa355b3'; 'gate' = '08bfa89def0a'; 'gate-cong-cu' = '527d4291b599'; 'gate-cong-cu-gop' = '4f1198c4ace4'
               'gate-ops' = '7bc725418208'; 'gate-packet-loop' = 'b90eef359184'; 'gate-registry' = 'b836a4f366e1' }
# Trả về các hàng "tên :: đích đuôi" của ci.yml mà script KHÔNG gương và KHÔNG khai tên, cộng các job có dấu vân lệch bảng ghim
# (`$DauVan`; $null = chỉ bộ so từng dòng — t34 dùng để đo răng riêng từng chốt). Rỗng = gương đủ.
function Tim-ThieuGuong { param([string]$Ci, [string]$Tep, [string[]]$Nep, [hashtable]$DauVan, [switch]$ChiBoSoTungDong)
    # Lớp dấu vân tắt được LẶNG LẼ bằng bao nhiêu cách thì kiểm ở chỗ TIÊU THỤ đối số, không ở chỗ gán biến (đo trên d53e681: bỏ đối số ở t32, `$DauVanCi = $null`
    # ⇒ t32 từ chối; nhưng `$null` hay một biến khác viết thẳng ở lời gọi của t32 ⇒ t32 ĐẠT, cả bộ 35/35 — chốt kiểm BIẾN, lời gọi dùng thứ khác).
    # Muốn CHỈ bộ so từng dòng thì phải gọi TÊN cờ `-ChiBoSoTungDong` (chỉ t34 dùng); `$null`, `@{}`, bảng thiếu `<workflow>` hay thiếu đối số đều bị từ chối.
    if (-not $ChiBoSoTungDong -and ($null -eq $DauVan -or -not $DauVan.ContainsKey('<workflow>'))) {
        throw 'KHONG DO DUOC: Tim-ThieuGuong thieu bang dau van (null / rong / thieu <workflow>) — lop dau van bi tat; CHI bo so tung dong thi goi -ChiBoSoTungDong' }
    $dong = @(Doc-DichCi $Ci)
    $tStr = [System.Management.Automation.Language.StringConstantExpressionAst]
    $tVar = [System.Management.Automation.Language.VariableExpressionAst]
    $bien = [string][char]30
    $ast = [System.Management.Automation.Language.Parser]::ParseFile($Tep, [ref]$null, [ref]$null)
    $nut = @($ast.FindAll({ param($x) $x -is [System.Management.Automation.Language.StringConstantExpressionAst] }, $true))
    $hang = @($nut | ForEach-Object Value)
    # Đuôi LIỀN SAU mỗi hằng trong mảng / lệnh của script: hằng ⇒ giá trị, BIẾN ⇒ dấu hiệu `$bien` + tên (chỉ khớp một hằng CÓ MẶT trong
    # script), thứ khác (chuỗi nội suy, biểu thức) ⇒ '*'.
    $cap = @{}
    foreach ($n in $nut) {
        $p = $n.Parent
        $ds = @(if ($p -is [System.Management.Automation.Language.ArrayLiteralAst]) { $p.Elements }
                elseif ($p -is [System.Management.Automation.Language.CommandAst]) { $p.CommandElements } else { $n })
        $i = [array]::IndexOf($ds, $n)
        $duoi = @(for ($k = $i + 1; $k -lt $ds.Count; $k++) {
            if ($ds[$k] -is $tStr) { $ds[$k].Value } elseif ($ds[$k] -is $tVar) { $bien + $ds[$k].VariablePath.UserPath } else { '*' } })
        if (-not $cap.ContainsKey($n.Value)) { $cap[$n.Value] = @() }
        $cap[$n.Value] += , $duoi
    }
    # `$env:KHOA = 'hằng'` của script: khoá mà ci.yml đặt bằng hằng thì script (nếu ĐẶT nó, không chỉ xoá) phải đặt đúng giá trị ấy.
    $gan = @{}
    foreach ($a in $ast.FindAll({ param($x) $x -is [System.Management.Automation.Language.AssignmentStatementAst] }, $true)) {
        if ($a.Left -is [System.Management.Automation.Language.VariableExpressionAst] -and $a.Left.VariablePath.DriveName -eq 'env' -and
            $a.Right -is [System.Management.Automation.Language.CommandExpressionAst] -and $a.Right.Expression -is $tStr) {
            $kh = $a.Left.VariablePath.UserPath.Substring(4)
            if (-not $gan.ContainsKey($kh)) { $gan[$kh] = @() }
            $gan[$kh] += $a.Right.Expression.Value
        }
    }
    $thieu = @(foreach ($x in $dong) {
        $ten, $dich, $sau = $x -split "`t", 3
        $c = @(if ($sau) { $sau -split [char]31 })
        $co = $false
        if ($dich -eq '<PIN>') { $co = $hang -ccontains $sau }
        elseif ($dich -eq '<ENV>') { $kv = $sau -split '=', 2; $co = (-not $gan.ContainsKey($kv[0])) -or ($gan[$kv[0]] -ccontains $kv[1]) }
        elseif ($dich -like '<USES>*') { $co = $Nep -ccontains $dich }
        elseif ($dich -eq '<KHONG-DICH>') { $co = $Nep -ccontains $ten }
        elseif ($cap.ContainsKey($dich)) { $co = @($cap[$dich] | Where-Object { Khop-Duoi $c $_ $hang }).Count -gt 0 }
        # "Có TÊN ĐÚNG trong một dòng KHÔNG CHẠY/THAY BẰNG": hằng chuỗi BẮT ĐẦU bằng một trong hai cụm ấy và chứa tên trong nháy kép — không
        # phải MỌI hằng chuỗi chứa tên (đo trên c848fee: thay dòng gương bằng `Noi 'ghi chu "<tên bước>"'` ⇒ t32 ĐẠT).
        $khai = [bool]$ten -and @($hang | Where-Object { $_ -cmatch '^ *(KHÔNG CHẠY|THAY BẰNG)' -and $_.Contains('"' + $ten + '"') }).Count -gt 0
        if (-not $co -and -not $khai) { "$ten :: $dich $($c -join ' ')" }
    })
    if ($null -ne $DauVan) {
        $nay = Doc-DauVanCi $Ci
        $thieu += @(foreach ($j in ($nay.Keys | Sort-Object)) {
            if (-not $DauVan.ContainsKey($j)) { "job $j :: <DAU-VAN> job MOI chua ghim — ghim: '$j' = '$($nay[$j])'" }
            elseif ($DauVan[$j] -cne $nay[$j]) { "job $j :: <DAU-VAN> da DOI ($($DauVan[$j]) -> $($nay[$j])) — ra gương rồi ghim: '$j' = '$($nay[$j])'" }
        })
        $thieu += @(foreach ($j in ($DauVan.Keys | Sort-Object)) { if (-not $nay.ContainsKey($j)) { "job $j :: <DAU-VAN> job da MAT khoi ci.yml — bo dong ghim" } })
    }
    return @($thieu | Select-Object -Unique)
}
Ca 't32 moi buoc gate* co guong trong script hoac co ten trong dong KHONG CHAY' {
    # Nối dây của lớp dấu vân: `Tim-ThieuGuong` TỰ từ chối bảng null / rỗng / thiếu `<workflow>` / thiếu đối số (chốt ở chỗ tiêu thụ; t34 khoá bằng bốn lời gọi).
    $thieu = @(Tim-ThieuGuong (Join-Path $GocKho '.github/workflows/ci.yml') $Script $NepCaiDat $DauVanCi)
    if ($thieu.Count -gt 0) { throw "ci.yml lech guong / dau van (buoc khong co guong, khong co ten trong dong KHONG CHAY, hoac job doi): $($thieu -join ' | ')" }
}

# t34 khoá CHÍNH bộ so của t32 bằng kho GIẢ: nền sạch phải ra RỖNG, mỗi đột biến (ci.yml hoặc script) phải ra KHÁC RỖNG. Không có ca
# này thì t32 chỉ "có mặt" — chạy trên ci.yml thật nó đúng khi và chỉ khi master chưa trôi, tức không bao giờ ĐỎ trong bộ.
# Ba nhóm hàng, mỗi nhóm một lý do:
#   · SO TỪNG DÒNG (không truyền dấu vân): mỗi chốt của `Doc-DichCi` / `Tim-ThieuGuong` có MỘT hàng đột biến, và nền sạch chứa đúng thứ chốt ấy
#     phải bỏ qua (bước nối dòng, dòng chú thích mang tên tệp, `$BIEN` trong lệnh, `&&` sau lệnh, bước `duong_nhanh`, `env` cấp job, `AL_VER`) —
#     bỏ riêng chốt nào thì nền sạch HOẶC hàng của nó ĐỎ (đo 33 chốt; xem "Lượt 18" ở đầu tệp).
#   · CHỈ DẤU VÂN: đột biến ở ci.yml mà bộ so từng dòng KHÔNG thấy (tiền tố, lệnh không đích, `env` kiểu số, `git config`, `with`, job `uses:`,
#     `if:` theo nền) — phải khác rỗng khi có dấu vân; và chú thích / dòng trống / CRLF KHÔNG được làm dấu vân đổi (không ồn).
Ca 't34 bo so guong: ci.yml / script bi dot bien => t32 phai DO' {
    $d = Join-Path ([IO.Path]::GetTempPath()) ('ccw-' + [guid]::NewGuid().ToString('N').Substring(0, 10))
    $script:Rac += $d
    New-Item -ItemType Directory -Force -Path $d | Out-Null
    $scrNen = @'
param([string]$AlVer = '1.7.7')
Chay-Py 'alpha' @('scripts/a.py', 'sub', '--json')
Chay-Py 'beta' @('ops/b_test.py')
Chay-Bash 'gamma' @('ops/c.sh', 'x')
$env:WORKERS = '2'
$env:JOBENV = '7'
foreach ($t in 'rg', 'shellcheck') { & $Bash 'ops/d.sh' $t }
& $PyTen -m pip install --quiet PyYAML==6.0.3
Chay-Py 'cont' @('scripts/g.py', 'x', '--json')
Chay-Py 'opc' @('ops/h_test.py')
Chay-Py 'flag' @('scripts/f.py', '--json')
Chay-Bash 'alver' @('ops/e.sh')
Noi 'KHÔNG CHẠY: "delta"'
Noi 'KHÔNG CHẠY: ""'
'@
    $ciNen = @'
jobs:
  chuan-bi:
    steps:
      - run: python ops/chi_o_chuan_bi.py
  tai-dung:
    uses: ./.github/workflows/x.yml
  gate:
    env:
      JOBENV: "7"
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      - name: alpha
        run: python scripts/a.py sub --json
      - name: beta
        run: python ops/b_test.py
      - name: gamma
        env:
          WORKERS: "2"
        run: bash ops/c.sh x
      - name: dd
        run: |
          bash ops/d.sh rg
          bash ops/d.sh shellcheck
      - name: pip
        run: python -m pip install --quiet PyYAML==6.0.3
      - name: nep
        run: git config --global core.abbrev 7
      - name: cont
        run: |
          # python scripts/zzz.py chi nam trong chu thich
          python scripts/g.py @@BS@@
            x --json
      - name: opc
        run: python ops/h_test.py && echo xong
      - name: flag
        run: python scripts/f.py $FLAG
      - name: alver
        shell: bash
        env:
          AL_VER: 1.7.7
        run: bash ops/e.sh
      - name: dn
        if: ${{ needs.chuan-bi.outputs.che_do == 'duong_nhanh' }}
        run: python scripts/zz_chi_duong_nhanh.py
      - name: delta
        run: python ops/delta.py
'@
    $ciNen = $ciNen.Replace('@@BS@@', [string][char]92)
    $nep = @('pip', 'nep', '<USES>actions/checkout')
    $thu = { param($ci, $scr, $dv)
        Set-Content -LiteralPath (Join-Path $d 'ci.yml') -Value $ci -Encoding utf8NoBOM
        Set-Content -LiteralPath (Join-Path $d 's.ps1') -Value $scr -Encoding utf8NoBOM
        if ($null -eq $dv) { @(Tim-ThieuGuong (Join-Path $d 'ci.yml') (Join-Path $d 's.ps1') $nep -ChiBoSoTungDong) }
        else { @(Tim-ThieuGuong (Join-Path $d 'ci.yml') (Join-Path $d 's.ps1') $nep $dv) } }
    $nen = @(& $thu $ciNen $scrNen $null)
    # Chốt ở chỗ TIÊU THỤ: lớp dấu vân không tắt được lặng lẽ bằng thiếu đối số / `$null` / `@{}` / bảng thiếu `<workflow>` (mỗi lời gọi phải ném).
    $cF = Join-Path $d 'ci.yml'; $sF = Join-Path $d 's.ps1'
    $tuChoi = [ordered]@{
        'thieu doi so DauVan'      = { Tim-ThieuGuong $cF $sF $nep }
        'DauVan = $null'           = { Tim-ThieuGuong $cF $sF $nep $null }
        'DauVan = @{}'             = { Tim-ThieuGuong $cF $sF $nep @{} }
        'DauVan thieu <workflow>'  = { Tim-ThieuGuong $cF $sF $nep @{ gate = 'x'; 'gate-ops' = 'y' } }
    }
    foreach ($ten in $tuChoi.Keys) {
        $nem = $false
        try { $null = & $tuChoi[$ten] } catch { $nem = $true }
        if (-not $nem) { throw "dau van: '$ten' KHONG bi tu choi — lop dau van tat duoc lang le" }
    }
    if ($nen.Count -ne 0) { throw "KHONG DO DUOC: kho gia sach ma bo so van bao thieu: $($nen -join ' | ')" }
    $dau = Doc-DauVanCi (Join-Path $d 'ci.yml')
    $nenDv = @(& $thu $ciNen $scrNen $dau)
    if ($nenDv.Count -ne 0) { throw "KHONG DO DUOC: kho gia sach ma dau van van bao lech: $($nenDv -join ' | ')" }
    $dotBien = [ordered]@{
        'them co --strict vao buoc da guong'       = @($ciNen.Replace('sub --json', 'sub --strict --json'), $scrNen)
        'buoc moi trung (dich, doi so dau)'      = @(($ciNen + "`n      - name: alpha2`n        run: python scripts/a.py sub --lane-moi`n"), $scrNen)
        'lenh con moi cua cung dich'             = @($ciNen.Replace('a.py sub --json', 'a.py newsub --json'), $scrNen)
        'script bo co --json'                    = @($ciNen, $scrNen.Replace("'sub', '--json'", "'sub'"))
        'script bo han buoc alpha'               = @($ciNen, $scrNen.Replace("Chay-Py 'alpha' @('scripts/a.py', 'sub', '--json')", ''))
        'buoc uses: cuc bo moi'                  = @(($ciNen + "`n      - uses: ./.github/actions/gate-moi`n"), $scrNen)
        'doi ghim PyYAML o ci.yml'               = @($ciNen.Replace('PyYAML==6.0.3', 'PyYAML==6.0.4'), $scrNen)
        'doi ghim AL_VER o ci.yml'               = @($ciNen.Replace('AL_VER: 1.7.7', 'AL_VER: 1.7.8'), $scrNen)
        'job moi khong mang tien to gate'        = @(($ciNen + "`n  kiem-moi:`n    steps:`n      - name: moi`n        run: python scripts/moi.py`n"), $scrNen)
        'buoc moi KHONG TEN, dich la'            = @(($ciNen + "`n      - run: python scripts/moi.py`n"), $scrNen)
        'doi gia tri env o ci.yml'               = @($ciNen.Replace('WORKERS: "2"', 'WORKERS: "4"'), $scrNen)
        'doi gia tri env cap job o ci.yml'       = @($ciNen.Replace('JOBENV: "7"', 'JOBENV: "8"'), $scrNen)
        'script doi gia tri env'                 = @($ciNen, $scrNen.Replace("WORKERS = '2'", "WORKERS = '4'"))
        'buoc moi khong co dich (actionlint)'    = @(($ciNen + "`n      - name: lint`n        run: actionlint -color`n"), $scrNen)
        'them co vao lenh noi dong'              = @($ciNen.Replace('x --json', 'x --strict --json'), $scrNen)
        'doi thu tu doi so (moi doi so deu la hang cua script)' = @($ciNen.Replace('sub --json', '--json sub'), $scrNen)
        'nhay kep khong can bang sau lenh'       = @($ciNen.Replace('ops/h_test.py && echo xong', 'ops/h_test.py "xong'), $scrNen)
        'doi so MOI qua bien cua script (jq)'    = @(($ciNen + "`n      - name: jq`n        run: bash ops/d.sh jq`n"), $scrNen)
        'script bo gia tri khoi vong lap bien'   = @($ciNen, $scrNen.Replace("foreach (`$t in 'rg', 'shellcheck')", "foreach (`$t in 'rg')"))
        'script giu ten buoc trong chuoi la'     = @($ciNen, $scrNen.Replace('KHÔNG CHẠY: "delta"', 'ghi chu: "delta"'))
        'doi so khac HOA/thuong (--JSON)'        = @($ciNen.Replace('sub --json', 'sub --JSON'), $scrNen)
        'doi so qua bien khac HOA/thuong (RG)'   = @(($ciNen + "`n      - name: rg`n        run: bash ops/d.sh RG`n"), $scrNen)
        'ten buoc la chuoi con cua ten da khai'  = @(($ciNen + "`n      - name: del`n        run: echo hi`n"), $scrNen)
        'ten buoc trong chuoi co KHONG CHAY giua chuoi' = @($ciNen, $scrNen.Replace('KHÔNG CHẠY: "delta"', 'ghi chu: KHÔNG CHẠY "delta"'))
        'ten buoc trong dong khong chay viet thuong' = @($ciNen, $scrNen.Replace('KHÔNG CHẠY: "delta"', 'không chạy: "delta"'))
    }
    foreach ($ten in $dotBien.Keys) {
        $ci, $sc = $dotBien[$ten]
        if ($ci -ceq $ciNen -and $sc -ceq $scrNen) { throw "KHONG DO DUOC: dot bien '$ten' khong doi gi (chuoi thay khong co mat)" }
        $r = @(& $thu $ci $sc $null)
        if ($r.Count -eq 0) { throw "bo so guong MU: dot bien '$ten' khong lam t32 DO" }
    }
    # Chỉ dấu vân: ci.yml đổi ở kênh bộ so từng dòng không thấy. Không khẳng định bộ so từng dòng RỖNG ở đây (nếu sau này nó học thêm kênh
    # thì hàng này vẫn đúng) — chỉ đòi dấu vân bắt được.
    $chiDau = [ordered]@{
        'tien to truoc dich (python -O)'         = $ciNen.Replace('python scripts/a.py sub --json', 'python -O scripts/a.py sub --json')
        'lenh khong dich them vao buoc da guong' = $ciNen.Replace('run: python scripts/a.py sub --json', "run: |`n          python scripts/a.py sub --json`n          actionlint -color")
        'env kieu so thay chuoi'                 = $ciNen.Replace('WORKERS: "2"', 'WORKERS: 4')
        'dong git config cua buoc khong dich'    = $ciNen.Replace('core.abbrev 7', 'core.abbrev 8')
        'with: doi gia tri'                      = $ciNen.Replace('fetch-depth: 0', 'fetch-depth: 1')
        'job uses: them job tai dung'            = $ciNen + "`n  tai-dung-moi:`n    uses: ./.github/workflows/x.yml`n"
        'job uses: doi duong dan'                = $ciNen.Replace('workflows/x.yml', 'workflows/y.yml')
        'if: Linux-only o buoc da guong'         = $ciNen.Replace("- name: alpha`n", "- name: alpha`n        if: runner.os == 'Linux'`n")
        'buoc ghim thieu =='                     = $ciNen.Replace('PyYAML==6.0.3', 'PyYAML==6.0.3 pytest')
        'defaults.run cap job (cwd cua moi buoc)' = $ciNen.Replace("  gate:`n    env:", "  gate:`n    defaults:`n      run:`n        working-directory: ops`n    env:")
        'container cap job'                      = $ciNen.Replace("  gate:`n    env:", "  gate:`n    container: python:3.13`n    env:")
        'services cap job'                       = $ciNen.Replace("  gate:`n    env:", "  gate:`n    services:`n      db:`n        image: postgres`n    env:")
        'continue-on-error cap job'              = $ciNen.Replace("  gate:`n    env:", "  gate:`n    continue-on-error: true`n    env:")
        'env cap workflow'                       = "env:`n  FOO: 1`n" + $ciNen
        'shell: doi bash sang pwsh'              = $ciNen.Replace('shell: bash', 'shell: pwsh')
        'defaults cap workflow'                  = "defaults:`n  run:`n    working-directory: ops`n" + $ciNen
        'with cap job (job uses:)'               = $ciNen.Replace("    uses: ./.github/workflows/x.yml`n", "    uses: ./.github/workflows/x.yml`n    with:`n      k: 1`n")
        'env cap job kieu so thay chuoi'         = $ciNen.Replace('JOBENV: "7"', 'JOBENV: 7')
        'if cap job'                             = $ciNen.Replace("  gate:`n    env:", "  gate:`n    if: github.event_name == 'push'`n    env:")
        'job bien mat khoi ci.yml'               = $ciNen.Replace("  tai-dung:`n    uses: ./.github/workflows/x.yml`n", '')
    }
    foreach ($ten in $chiDau.Keys) {
        $ci = $chiDau[$ten]
        if ($ci -ceq $ciNen) { throw "KHONG DO DUOC: dot bien dau van '$ten' khong doi gi (chuoi thay khong co mat)" }
        if (@(& $thu $ci $scrNen $dau).Count -eq 0) { throw "dau van MU: dot bien '$ten' o ci.yml khong lam t32 DO" }
    }
    # Không ồn: chú thích trong thân `run`, dòng trống, CRLF không phải thay đổi của bước.
    $khongDoi = [ordered]@{
        'them chu thich trong than run'          = $ciNen.Replace("bash ops/d.sh rg`n", "# ghi chu moi`n          bash ops/d.sh rg`n")
        'them dong trong trong than run'         = $ciNen.Replace("bash ops/d.sh rg`n", "bash ops/d.sh rg`n`n")
        'doi dau dong sang CRLF'                 = $ciNen.Replace("`n", "`r`n")
        'doi buoc chi chay o duong_nhanh'        = $ciNen.Replace('zz_chi_duong_nhanh.py', 'zz_khac.py')
        'doi thu tu khoa trong buoc'             = $ciNen.Replace("        shell: bash`n        env:`n          AL_VER: 1.7.7`n", "        env:`n          AL_VER: 1.7.7`n        shell: bash`n")
        'doi buoc cua job chuan-bi'              = $ciNen.Replace('python ops/chi_o_chuan_bi.py', 'python ops/chi_o_chuan_bi_moi.py')
        'them khoang trang cuoi dong trong than run' = $ciNen.Replace("bash ops/d.sh rg`n", "bash ops/d.sh rg   `n")
    }
    foreach ($ten in $khongDoi.Keys) {
        $ci = $khongDoi[$ten]
        if ($ci -ceq $ciNen) { throw "KHONG DO DUOC: hang khong-on '$ten' khong doi gi (chuoi thay khong co mat)" }
        $r = @(& $thu $ci $scrNen $dau)
        if ($r.Count -gt 0) { throw "dau van ON: '$ten' khong phai thay doi cua buoc ma van lam t32 DO: $($r -join ' | ')" }
    }
}

# Wrapper lease THẬT (`ops/chay_lease_publish_test.sh`) chọn Python THEO TÊN trên PATH của phiên gọi. `python` giả (thoát 0) ĐẦU PATH,
# `python3` thật sau nó: Tim-Python bỏ nó, wrapper thì chạy nó ⇒ đo trên 9b8a420: `lease-publish selftest` rc=0 ĐẠT, script rc=0, bộ
# test (giả, thoát 1) không chạy. Lượt đối chứng không shim: wrapper THẬT phải tới được bộ test (dấu in ra, rc=1) — không thế thì ca
# không có răng. Windows: shim là bản chép `whoami.exe` (thoát 0, không in `TLPY=`) — KHÔNG ĐO ĐƯỢC trên nền này.
Ca 't33 python gia chi o ten python dau PATH => cong lease (wrapper chon theo TEN) khong DAT' {
    $k = Dung-Kho
    Copy-Item -LiteralPath (Join-Path $GocKho 'ops/chay_lease_publish_test.sh') -Destination (Join-Path $k 'ops/chay_lease_publish_test.sh') -Force
    Set-Content -LiteralPath (Join-Path $k 'ops/cai_actionlint.sh') -Encoding utf8NoBOM -Value @'
mkdir -p "$AL_DICH"
echo '#!/bin/sh' > "$AL_DICH/actionlint"
echo 'echo 1.7.7' >> "$AL_DICH/actionlint"
chmod +x "$AL_DICH/actionlint"
'@
    Set-Content -LiteralPath (Join-Path $k 'ops/lease_publish_test.py') -Encoding utf8NoBOM -Value "import sys; print('THAT-CHAY-LEASE-T33'); sys.exit(1)"
    & git -C $k add -A
    & git -C $k -c user.email=t@t -c user.name=t commit -qm wrapper-that
    $a = Chay $k
    if ($a.ra -notmatch 'lease-publish selftest +rc=1' -or $a.ra -notmatch 'THAT-CHAY-LEASE-T33') {
        throw "KHONG DO DUOC: wrapper THAT khong toi duoc bo test o luot doi chung (rc_script=$($a.rc))" }
    Remove-Item -LiteralPath (Join-Path $k 'dist') -Recurse -Force -ErrorAction SilentlyContinue
    $shim = Join-Path (Split-Path $k) 'shim-python'
    New-Item -ItemType Directory -Force -Path $shim | Out-Null
    if ($IsWindows) { Copy-Item -LiteralPath (Join-Path $env:SystemRoot 'System32/whoami.exe') -Destination (Join-Path $shim 'python.exe') }
    else {
        Set-Content -LiteralPath (Join-Path $shim 'python') -Value "#!/bin/sh`nexit 0" -Encoding utf8NoBOM
        & chmod +x (Join-Path $shim 'python')
    }
    $b = Chay $k @() @{ PATH = "$shim$Sep$env:PATH" }
    if ($b.ra -match 'lease-publish selftest +rc=0' -or $b.rc -eq 0) {
        throw "python gia chi o ten python: wrapper chon no, cong lease DAT ma bo test khong chay (rc_script=$($b.rc))" }
    # Lượt 3 — vế `$LASTEXITCODE -eq 0` của thăm dò: `python` in `TLPY=3.12.0` RỒI thoát 3 không phải bằng chứng. Bỏ vế ấy thì cổng lease
    # CHẠY shim và ra `lease-publish selftest rc=3 ĐỎ` (thay vì BỎ QUA/KHÔNG ĐO ĐƯỢC). Nền Windows: shim cần `.exe` in được `TLPY=` — KHÔNG ĐO ĐƯỢC.
    if (-not $IsWindows) {
        Set-Content -LiteralPath (Join-Path $shim 'python') -Value "#!/bin/sh`necho TLPY=3.12.0`nexit 3" -Encoding utf8NoBOM
        $c = Chay $k @() @{ PATH = "$shim$Sep$env:PATH" }
        if ($c.ra -match 'lease-publish selftest +rc=' -or $c.rc -eq 0) {
            throw "python in TLPY= roi thoat 3: tham do van tin no, cong lease chay shim (rc_script=$($c.rc))" }
    }
}

# t35 khoá cái mà t32 KHÔNG đo (cả mức mặc định, `nhanh` lẫn `day-du`): t32 đọc VĂN BẢN script (mọi hằng chuỗi trong AST) nên một cổng chỉ cần CÒN CHỮ là "có gương". Đo trên 72dc360:
# bọc `Chay-Py 'golden-test' …` trong `if ($false) { }` / `if ($Muc -eq 'khong-co') { }`, đổi nó thành một mảng không dùng, hoặc đặt trong
# một hàm không ai gọi ⇒ t32 ĐẠT và cả bộ 34/34 — script không còn chạy `golden-test` mà không ca nào đỏ. Ca này chạy script THẬT trên kho giả
# (mọi cổng là stub thoát 0) và đòi tên cổng IN RA khớp bảng ghim: cổng biến mất khỏi lượt chạy ⇒ ĐỎ; thêm cổng mà quên khai ⇒ ĐỎ.
# Lượt MẶC ĐỊNH chạy KHÔNG `-Muc` (đo trên d53e681: đổi `[string]$Muc = 'nhanh'` thành `'day-du'` ⇒ cả bộ 35/35, vì chỉ có lượt `-Muc nhanh` tường minh).
# Bộ so (`Tim-CongLech`) có hàng đột biến SCRIPT riêng như t34 có cho t32 — không có hàng thì gỡ `thua`/`thieu`/lượt mặc định khỏi t35 vẫn 35/35 vì script nền sạch.
# Giới hạn: đo TÊN cổng đã chạy, không đo đối số lúc chạy (stub bỏ qua đối số; đối số do t32 so với ci.yml). Windows: KHÔNG ĐO ĐƯỢC ở đây — bảng
# bỏ hai cổng ci.yml cũng bỏ trên Windows (`don-nhanh selftest (ps1)`, `ci-phamvi selftest`), phần còn lại chưa chạy trên Windows thật.
$CongDayDu = @('cong_cu kiem-tra', 'cong_cu_test', 'lease-publish selftest', 'packet-loop selftest', 'registry test', 'don-nhanh selftest (ps1)',
               'py_compile', 'codex credential selftest', 'bien-nhan v2 selftest', 'idiom-ba-ten selftest', 'eol-policy selftest', 'pre-push selftest',
               'gate lifecycle selftest', 'eol-policy survey', 'bundled-fragment check', 'gen_instructions selftest', 'command-registry unit',
               'tl selftest', 'workflow-audit strict', 'golden-test', 'doc-claims-check strict', 'determinism-audit strict', 'ci-phamvi guard',
               'ci-phamvi selftest', 'release-check full', 'release-verify strict', 'tl_boot smoke', 'release-bundle a', 'release-bundle b',
               'release-bundle tất định')
# Chạy script `$Scr` trên kho giả với đối số `$DoiMuc`; trả về cổng THIẾU so với `$Bang` và cổng THỪA (in ra mà bảng không khai).
function Tim-CongLech { param([string]$Scr, [string[]]$DoiMuc, [string[]]$Bang)
    $k = Dung-Kho $Scr
    $a = Chay $k $DoiMuc
    $co = @(foreach ($d in ($a.ra -split "`n")) { if ($d -cmatch '^  ([^ ].*?) +rc=[^ ]* +') { $Matches[1] } })
    if ($co.Count -eq 0) { throw "KHONG DO DUOC: khong doc duoc dong cong nao trong output (rc_script=$($a.rc))" }
    $can = @($Bang | Where-Object { -not $IsWindows -or ($_ -cne 'don-nhanh selftest (ps1)' -and $_ -cne 'ci-phamvi selftest') })
    return @{ thieu = @($can | Where-Object { $co -cnotcontains $_ }); thua = @($co | Where-Object { $can -cnotcontains $_ }) }
}
Ca 't35 script CHAY du cac cong (ten cong in ra khop bang ghim, khong chi co mat trong van ban)' {
    # `nhanh` là mức MẶC ĐỊNH (sáu cổng đầu của bảng); `day-du` là toàn bảng. Lượt `mac dinh` KHÔNG truyền `-Muc`.
    $nhanh = @($CongDayDu[0..5])
    $luot = [ordered]@{
        'mac dinh' = @{ Doi = @();                  Bang = $nhanh }
        'nhanh'    = @{ Doi = @('-Muc', 'nhanh');   Bang = $nhanh }
        'day-du'   = @{ Doi = @('-Muc', 'day-du');  Bang = $CongDayDu }
    }
    foreach ($ten in $luot.Keys) {
        $r = Tim-CongLech $Script $luot[$ten].Doi $luot[$ten].Bang
        if ($r.thieu.Count -gt 0 -or $r.thua.Count -gt 0) {
            throw "muc $($ten): cong khong khop bang ghim — KHONG CHAY: [$($r.thieu -join ' | ')]; CHAY MA CHUA KHAI: [$($r.thua -join ' | ')]" }
    }
    # Hàng đột biến của chính bộ so: script bị đổi ⇒ `Tim-CongLech` phải ra ĐÚNG hiệu số (không chỉ "ném lỗi"): `Thieu` = cổng phải nằm trong THIẾU, `Thua` = cổng phải nằm trong THỪA.
    $nen = [IO.File]::ReadAllText($Script)
    $vong = "(?m)^([ \t]*)(Chay-Py[ \t]+'{0}'[ \t][^\r\n]*)$"
    $dot = [ordered]@{
        'cong golden-test boc trong if false (day-du)' = @{ Luot = 'day-du'; Mau = ($vong -f 'golden-test'); Thay = '${1}if ($$false) { ${2} }'; Thieu = 'golden-test' }
        'cong packet-loop chi con o day-du (nhanh)'    = @{ Luot = 'nhanh'; Mau = ($vong -f 'packet-loop selftest'); Thay = '${1}if ($$Muc -eq ''day-du'') { ${2} }'; Thieu = 'packet-loop selftest' }
        'cong golden-test doi ten (day-du)'            = @{ Luot = 'day-du'; Mau = "(?m)^([ \t]*Chay-Py[ \t]+)'golden-test'"; Thay = '${1}''golden-test2'''; Thieu = 'golden-test'; Thua = 'golden-test2' }
        'cong moi chua khai bang (day-du)'             = @{ Luot = 'day-du'; Mau = ($vong -f 'golden-test'); Thay = ('${1}${2}' + "`n" + '${1}Chay-Py ''cong-moi'' @(''ops/cong_cu.py'', ''kiem-tra'')'); Thua = 'cong-moi' }
        'muc mac dinh doi sang day-du'                 = @{ Luot = 'mac dinh'; Mau = '(\[string\]\$Muc = )''nhanh'''; Thay = '${1}''day-du'''; Thua = 'golden-test' }
    }
    $dr = Join-Path ([IO.Path]::GetTempPath()) ('ccw-' + [guid]::NewGuid().ToString('N').Substring(0, 10))
    $script:Rac += $dr
    New-Item -ItemType Directory -Force -Path $dr | Out-Null
    foreach ($ten in $dot.Keys) {
        $h = $dot[$ten]
        if (-not $luot.Contains($h.Luot)) { throw "KHONG DO DUOC: hang '$ten' goi luot '$($h.Luot)' khong co" }
        if ([regex]::Matches($nen, $h.Mau).Count -ne 1) { throw "KHONG DO DUOC: dot bien '$ten' khong khop dung 1 cho trong script (mau khong co mat / khong duy nhat)" }
        $tep = Join-Path $dr 'chay-cong-windows.ps1'
        Set-Content -LiteralPath $tep -Value ([regex]::Replace($nen, $h.Mau, $h.Thay)) -Encoding utf8NoBOM -NoNewline
        $r = Tim-CongLech $tep $luot[$h.Luot].Doi $luot[$h.Luot].Bang
        $dung = $(if ($h['Thieu']) { $r.thieu -ccontains $h['Thieu'] } else { $true }) -and $(if ($h['Thua']) { $r.thua -ccontains $h['Thua'] } else { $true })
        if (-not $dung) { throw "bo so cua t35 MU: dot bien '$ten' khong ra dung hieu so (thieu=[$($r.thieu -join ' | ')]; thua=[$($r.thua -join ' | ')])" }
    }
}

# `dist` CHƯA theo dõi là symlink/junction tới thư mục NGOÀI kho, đích KHÔNG có `actionlint/` (nên danh sách CHO PHÉP qua) và có sẵn
# `a.zip`/`b.zip`. Trước bản vá (16522a9): script đi tiếp, `cong-windows/` mọc ra ở đích (và `-Muc day-du` xoá hai zip ở đó). Sau: rc=2
# TRƯỚC mọi lần ghi — đích không có `cong-windows/`, hai zip còn nguyên. Ca `dist/cong-windows` là symlink: cùng chốt, mục con.
Ca 't36 dist chua theo doi la symlink ra ngoai kho => rc=2, khong ghi/xoa gi o dich' {
    foreach ($kieu in 'dist', 'dist/cong-windows') {
        $k = Dung-Kho
        $ngoai = Join-Path (Split-Path -Parent $k) 'ngoai-kho'
        New-Item -ItemType Directory -Force -Path $ngoai | Out-Null
        foreach ($z in 'a.zip', 'b.zip') { Set-Content -LiteralPath (Join-Path $ngoai $z) -Value 'giu' -Encoding utf8NoBOM }
        $lk = Join-Path $k $kieu
        New-Item -ItemType Directory -Force -Path (Split-Path -Parent $lk) | Out-Null
        if ($IsWindows) { New-Item -ItemType Junction -Path $lk -Target $ngoai | Out-Null } else { & ln -s $ngoai $lk }
        if (@(& git -C $k ls-files -- 'dist').Count -ne 0 -or -not ((Get-Item -LiteralPath $lk -Force).Attributes -band [IO.FileAttributes]::ReparsePoint)) {
            throw "KHONG DO DUOC: kho gia khong dung duoc $kieu la symlink CHUA theo doi" }
        $a = Chay $k
        if ($a.rc -ne 2 -or $a.ra -notmatch 'symlink/junction') { throw "$kieu symlink ra ngoai kho ma khong bi tu choi (rc=$($a.rc))" }
        $moc = @(Get-ChildItem -LiteralPath $ngoai -Force | ForEach-Object Name | Sort-Object)
        if (($moc -join ',') -cne 'a.zip,b.zip') { throw "${kieu}: script da ghi/xoa o thu muc ngoai kho (con: $($moc -join ', '))" }
    }
}

foreach ($d in $script:Rac) { Remove-Item -LiteralPath $d -Recurse -Force -ErrorAction SilentlyContinue }
$script:KetQua | ForEach-Object { Write-Host $_ }
$dat = @($script:KetQua | Where-Object { $_ -like 'DAT *' }).Count
Write-Host ("chay-cong-windows: {0}/{1} dat" -f $dat, $script:KetQua.Count)
if ($dat -ne $script:KetQua.Count -or $script:KetQua.Count -eq 0) { exit 1 }
exit 0
