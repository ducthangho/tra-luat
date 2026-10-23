verdict: changes_requested
reviewed_head: 1965b71fecc5c936c2e342b109fa88a260943920
reviewed_sha: 1965b71fecc5c936c2e342b109fa88a260943920
reviewed_tree: 90f8cc13839e014525380dedacaa8e40b06288e3
review_class: sensitive
provider: openai_codex
model: gpt-6.1-sol
model_family: openai
reasoning_effort: xhigh
execution_surface: codex_cli
transport: machine
review_round: 1/5

## Kết luận

**changes_requested — đã xác nhận F868-01 (P2) trên head nguyên vẹn và hai khoảng trống test F868-02 (P2), F868-03 (P3).** Không phát hiện P0/P1 trong phạm vi đã đo. Các cổng còn chạy được ghi riêng bên dưới; verdict sẽ cập nhật khi chúng xong. Không cấp quyền merge/land/deploy.

## Neo và môi trường

Đã xác minh HEAD/tree, base `9e9a74b2a396ef458d25c51a5563efafbb45ba0c`, spec SHA-256 `0d950c2b98b9e024bf1cc43a77c5d3351b5f4c21e6307b2e36ba9cdeca7b3f69` khớp. Snapshot và PROMPT.md cùng SHA-256 `31633e0f11a5dac87ee9efcc67383d2139a3b36cca07a4a9557835501accbda7`. Linux, Bash 5.2.21, Python 3.13.16, Git 2.43.0; core.abbrev=7. Lease offline hạn 2026-10-24T06:52:00Z; không xác nhận heartbeat live. `out/review.py setup` dựng hai vế trong MỘT lệnh, thêm `base-cross` chép launcher_test.py của head vào nền. Không gọi mạng, không sửa cây nguồn. Diff thực tế: **6 tệp / 268 thêm / 93 xoá**, đúng write set PR, không có handoff; diff --check rc=0. Xem `out/evidence/anchors.*`.

## Finding

| ID | Mức | Slug lớp | Vị trí | Bằng chứng | Hướng xử lý |
|---|---|---|---|---|---|
| F868-01 | P2 | `stdout-installer-bi-nhan-lam-ket-qua-chon` (kế thừa F858-03; đường mới: lỗi đọc kênh) | `ops/cai_cong_cu.sh:135` | `python -B out/probes.py io`: kênh đã ghi DICH nhưng cat giả lỗi I/O/rc74; script **rc=0/DAT**, gọi rg ở thư mục log khác; đối chứng không lỗi không gọi rg ấy. `printf x` che mã lỗi cat. | Phân biệt đọc thành công với đọc lỗi trước khi xét kênh rỗng; lỗi đọc phải thoát khác 0, giữ fallback cho công thức thực sự không dùng bộ chọn. Thêm ca fault-injection và đối chứng. Chi tiết sẽ cập nhật sau khi đo xong. |

**F868-01 — chi tiết phản chứng.** `python -B out/probes.py io-readback` chạy toàn bộ script bằng `source` để đọc lại DICH, với lệnh cài rg nguyên văn từ YAML và stub installer vô hại. Lượt lỗi lưu được nội dung kênh THỰC: `DICH\n<fixture>/goc/usr/bin`; cat giả báo lỗi I/O và rc74. Script lại trả **rc0/DAT**, `$GITHUB_PATH=<fixture>/goc/usr/bin`, nhưng **DICH=<fixture>/xau** (thư mục log khác, có rg tốt khác), final checker gọi rg ở xau. Đối chứng không lỗi: DICH bằng ứng viên, không gọi rg ở xau. Vị trí `.claude/dev/launcher_test.py:8848` còn buộc đúng chuỗi che lỗi nên cũng cần đổi khi sửa reader. Kế thừa lớp F858-03, đường lỗi stdout bình thường đã vá nhưng lỗi đọc kênh lại mở đường dùng stdout. Phép đóng lớp phải từ chối lỗi đọc, kể cả có stdout nhìn như thư mục; giữ đúng byte/newline và fallback rỗng hợp lệ. Rủi ro bản sửa: vô tình làm mất newline cuối hoặc chặn N3; cần đối chứng cho cả hai.

| ID | Mức | Slug lớp | Vị trí | Bằng chứng | Hướng xử lý |
|---|---|---|---|---|---|
| F868-02 | P2 (test; head runtime hiện đúng) | `fixture-khong-khoa-don-kenh-khi-thoat-loi` | `.claude/dev/launcher_test.py:8755`; cleanup ở `ops/cai_cong_cu.sh:126` | Mutant `disable-exit-trap` tắt EXIT trap sau khi đăng ký, giữ cleanup đường thành công. Toàn launcher **226/239, 13 failed/10 skipped**, cùng đúng tập lỗi với control head; delta lỗi=0. Witness installer rc29: control tmp_left=[]; mutant còn `tmp/cai_cong_cu.*`. | Thêm ca installer lỗi sau tạo kênh, đo rc và thư mục thực đã tạo/phải bị xoá; giữ chiều thành công và batch. Đăng ký mutant tương ứng, đòi TinHieuChotCa. Không cần sửa runtime head cho finding này. Tránh test chỉ đếm thư mục rỗng mà không chứng minh kênh từng được tạo. |
| F868-03 | P3 (test; head runtime hiện đúng) | `fixture-fallback-khong-khoa-crlf` | `.claude/dev/launcher_test.py:8807`; reader `ops/cai_cong_cu.sh:142` | Mutant `drop-fallback-cr` bỏ đúng cắt CR ở fallback, vẫn toàn launcher **226/239, 13 failed/10 skipped**, cùng tập lỗi control. Witness công thức không bộ chọn in `log\r\n<uv>\r\n`: control **rc0/DAT**, mutant **rc2/DO**. | Giữ ca LF, thêm CRLF trên đường fallback qua script thật, đòi thư mục được dùng và DAT. Đăng ký mutant bỏ cắt CR và đòi TinHieuChotCa. Tránh strip toàn bộ nội dung gây hỏng khoảng trắng/newline hợp lệ. Không cần vá runtime head cho finding này; chưa chứng minh actionlint thật hiện phát CRLF ở dòng thư mục, nên giữ P3. |

**3 lớp / 3 finding IDs mở: 2 P2, 1 P3.** Hai finding test được chứng minh là mutant KHÔNG tương đương; không gọi chúng là lỗi runtime của head nguyên vẹn. Script đột biến và witness nằm trong `out/mutations.py`; kết quả tại `out/evidence/custom-mutation-witnesses.json` và `mutant-full-*.{stdout,json,jsonl}`. Không viết patch sản phẩm.

## Hướng săn

| Hướng | Giả thuyết | Lệnh | Output thật (rút gọn) | Kết luận |
|---|---|---|---|---|
| 1. Stdout và export | Log muộn/thiếu LF hoặc allexport có thể chi phối kết quả. | `python -B out/probes.py channel` | Nền muộn/thiếu LF: rc2, không DAT; head cả ba kiểu: rc0/DAT. Installer thấy `ABSENT ABSENT` dưới thường, `bash -a`, `SHELLOPTS=allexport`. | KHÔNG PHẢI LỖI trên head ở các đường đã đo. |
| 2. Batch/trap | Source dùng chung shell có thể rò kênh hoặc dọn nhầm. | `python -B out/probes.py batch` | 12 tổ hợp: thành công rc0; lỗi installer bash rc23; tất cả tmp_left=[]; installer không thấy hai biến kênh. | KHÔNG PHẢI LỖI. |
| 3. Errexit | Subshell mới có thể nuốt mã lỗi recipe. | `python -B out/probes.py failures` | Nền/head cùng installer rc29, checker rc1; `false; echo <uv>` cùng rc0/DAT (ngữ nghĩa cũ). | KHÔNG PHẢI LỖI ở ba đường đã đo. |
| 4. Lỗi đọc kênh | cat đọc kênh lỗi bị nhận là kênh rỗng và dùng stdout. | `python -B out/probes.py io` | Đối chứng rc0/DAT, alternative_probe_called=false; lỗi I/O rc0/DAT, alternative_probe_called=true; stderr `cat: simulated result-channel I/O error`. | LỖI F868-01. |

| 5. Writer giữ stderr | Có thể còn chờ EOF ở stderr dù stdout đã tách. | `python -B out/probes.py streams` | Shell xong 0.423–0.593s, rc0/DAT cả ba. `communicate` giữ stderr chờ 3.12–3.19s, chỉ stdout 0.593s. | KHÔNG PHẢI LỖI N2 của shell; giới hạn caller bắt stderr vẫn còn. |
| 6. Fallback CRLF | Công thức không bộ chọn in CRLF có thể không được thêm PATH. | `python -B out/probes.py crlf` | Nền/head cùng rc0/DAT, tmp_left=[]. | KHÔNG PHẢI LỖI trên head; đang đo mutant bỏ cắt CR. |

| 7. Mutant ngoài bảng | Suite có thể bỏ sót cleanup khi lỗi và CRLF fallback. | `python -B out/mutations.py setup`; `suite disable-exit-trap`; `suite drop-fallback-cr`; `witnesses` | Hai suite mutant cùng 226/239, 13 đỏ/10 bỏ qua như head control. Witness phân biệt rò temp và CRLF rc2. | LỖI độ phủ F868-02/F868-03. |
| 8. Windows rg, Q4, phạm vi | Đổi bộ chọn có thể mất chuyển đổi, guard PATH hoặc chốt cũ. | `python -B out/probes.py windows`; `python -B out/audit.py`; `python -B out/strict_mutations.py` | Links/choco DAT, hết ứng viên rc1; bare DAT không ghi PATH; GP rỗng/vắng vẫn DAT và vẫn -u; lỗi -u/-w rc1. AST không mất ca; 33 mutant hook: 18 control PASS và 62 TinHieuChotCa, không tín dụng giả. | KHÔNG PHẢI LỖI ở mô phỏng; native Windows KHÔNG ĐO ĐƯỢC. |

Các cổng cuối còn chạy; bằng chứng đầy đủ tại `out/evidence/probe-*.json` và `out/fixtures/*/{stdout,stderr}`.

## Lệnh và kết quả thật

Đã đọc đầy đủ `../runs/fe6f5deb/prompt.snapshot`.

## Không đo được

- Windows/macOS native, Git Bash/MSYS, `.exe`/PATHEXT, `mktemp`/`cygpath` thực trên Windows: hiện chỉ có Linux và mô phỏng.
- GitHub/CI/heartbeat/thread live, check run ci.yml và launcher-windows.yml: không gọi mạng theo chỉ thị, chưa xác nhận M-2/M-3.
- `/tmp/.git` chỉ đọc và `/var/tmp` ngoài writable roots làm t86/r858_goc_tam/r484 đỏ cả nền/head; giữ lỗi thật, không coi là hồi quy hoặc kill có giá trị.
- Handoff `origin/ops/wp868-r1-g1-lease:ops/handoff/wp868-g1-claude.md` vắng (git show rc128); chưa xác nhận lý do Q4 ở handoff. Không đưa handoff vào diff PR.
- Tiến trình đang chạy: full suites, selftest với môi trường sửa đúng, cong_cu_test đầy đủ, hai mutant mới. Lượt selftest đầu rc1, 1730/1731 do driver ép core.abbrev qua environment khiến chính ca đổi abbrev không đổi được; đã sửa driver ngoài cây sản phẩm và chạy lại, chưa coi đây là lỗi sản phẩm.
