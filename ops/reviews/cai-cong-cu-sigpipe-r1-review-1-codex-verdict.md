# Cross-review độc lập — packet #675 r1 g1 — lượt 1
verdict: changes_requested
reviewed_sha: 41d03d8c0ab3374adef6e3d159ac568ae67bc429

Kết luận: cần sửa W4 theo F1/F2/F3. Ba dòng vá W1–W3 giữ đúng giá trị trên tập đầu vào đã đo.
reviewed_tree: 226d18f74262b3f0bf348f01e0e52afbbf6ee2bd
baseline_sha: cd23c7dbc7833d64a8e87e8ffd94f194c18e0060
provider: OpenAI; execution_surface: Codex qua API với shell cục bộ; transport: công cụ trực tiếp.
Không sửa cây ứng viên/nền, không push, không đăng GitHub. Mọi phép thử và đột biến chạy trên bản sao dưới `tam/`.

HƯỚNG 1: Neo nguồn và phạm vi
  giả thuyết : HEAD, baseline, SPEC và write set đúng packet.
  lệnh       : `git -C cay-kho rev-parse HEAD; git -C cay-nen rev-parse HEAD; sha256sum SPEC.md; git -C cay-kho diff cd23c7d --numstat; git -C cay-kho status --short; git -C cay-nen status --short`
  output     : HEAD=41d03d8c0ab3374adef6e3d159ac568ae67bc429; baseline=cd23c7dbc7833d64a8e87e8ffd94f194c18e0060; SPEC=17a5fee7c12ecab33c870668e762eb0775f253349f57dcdbe60dfd3a4056cd45. Numstat: cai_actionlint.sh 2/1; cai_cong_cu.sh 3/1; do_sigpipe.sh 143/0; dung_goi_review.sh 2/1 (thêm/xóa). Hai status rỗng; mọi lệnh rc=0.
  kết luận   : KHÔNG PHẢI LỖI. Đúng W1–W4; tổng 150 dòng thêm, không vượt S5 (>150). W1–W3 chỉ đổi ba phép gán và chú thích liền kề.

HƯỚNG 2: Tương đương giá trị của W1–W3 (§5, §6a)
  giả thuyết : mẫu `${X%%$'\n'*}` có thể xử lý sai nội dung chứa glob hoặc CR.
  lệnh       : `cd tam/tmp.1TQdJ7ghPz && python review_checks.py equivalence` (mã và kết quả lưu tại `logs/equivalence.json`).
  output     : 604 đầu vào × 3 điểm × 3 chế độ = 5.436 so sánh; mọi tiến trình rc=0, mọi `mismatches=[]`. Ba chế độ: `set -u`, thêm `set -f`, thêm `shopt -s nullglob extglob`. Có rỗng, chỉ LF, nhiều LF, không LF cuối, CRLF, CR giữa dòng, dòng đầu rỗng, `* ? [ ] %`, khoảng trắng, dấu gạch chéo và Unicode; thêm toàn bộ chuỗi độ dài 1–3 trên bảng chữ `a LF CR * ? [ ] %`. Đối chiếu cả dòng baseline và oracle độc lập: lấy trước LF đầu, bỏ mọi CR ở W2/W3.
  kết luận   : KHÔNG PHẢI LỖI. Ký tự glob trong GIÁ TRỊ không trở thành mẫu mới; mẫu cắt chỉ là LF + `*`. `//CR/` giữ đúng hành vi `tr -d`, kể cả CR giữa dòng. W1 giữ CR ở riêng phép gán như baseline; dòng trước đó vẫn bỏ CR cho toàn bộ DAU_RA. Đây là bằng chứng trên tập đo, không phải tuyên bố vét cạn mọi chuỗi Bash.

HƯỚNG 3: Chạy W4, baseline và ba điểm độc lập (§6b–c, A1)
  giả thuyết : W4 xanh trên head, đỏ đúng rc=141 trên từng điểm baseline.
  lệnh       : `cd tam/tmp.1TQdJ7ghPz && python review_checks.py mutations`; hàm `w4()` gọi `bash head/ops/do_sigpipe.sh --goc <bản-sao>` qua `subprocess.run` mặc định `restore_signals=True`. Nhật ký đầy đủ: `logs/w4-*.stdout`, `logs/w4-*.stderr`, `logs/mutations.jsonl`.
  output     : head `42/42 DAT`, rc=0; ba W1–W3 baseline `39/42`, rc=1, mỗi điểm `(b)/dong-trich rc0=0 rc141=10 khac=0`. Chỉ trả riêng từng W1, W2 hoặc W3 về baseline: mỗi lần `41/42`, rc=1 và đúng điểm đó rc141=10/10. Môi trường: bash 5.2.21(1)-release, Linux, 4 lõi, 10 lần, 20.000 dòng.
  kết luận   : KHÔNG PHẢI LỖI cho A1 và phản chứng quay lại pipeline. Các phép `(a)` chạy đủ 33 lần; `(b)` 6 lần và `(c)` 3 lần; tổng 42 khớp số khai báo.

  Ghi chú môi trường: lần gọi trực tiếp từ shell công cụ cho head 36/42, baseline 33/42. Đo riêng cùng pipeline bằng Python: `restore_signals=True` → rc=141, stderr rỗng; `False` → rc=1, `printf: write error: Broken pipe`. Shell công cụ thừa kế SIGPIPE bị bỏ qua. Không tính đây là lỗi sản phẩm; W4 đã từ chối cấp tín dụng rc=141 khi điều kiện đo không đúng. Các kết quả sau dùng tín hiệu mặc định.

HƯỚNG 4: Chốt trích dòng có thực sự neo vào mã được thực thi?
  giả thuyết : regex `^[[:space:]]*BIEN=` có thể trích mã chết và vẫn báo xanh.
  lệnh       : `python review_checks.py mutations` như trên; đột biến W1 trên bản sao: bọc nguyên dòng LENH vào `unused() { ...; }` không gọi, hoặc vào `: <<'REVIEW_COMMENT' ... REVIEW_COMMENT`. Chạy W4 rồi chạy nguyên `cai_cong_cu.sh actionlint` với producer Python cục bộ, không mạng.
  output     : cả `w4-mut-unused-function` lẫn `w4-mut-heredoc`: `42/42 DAT`, rc=0. Chạy chính hai script đột biến: rc=1, `LENH: unbound variable`, trước khi probe. Nhật ký `logs/behavior-mut-{unused-function,heredoc}.stderr`.
  kết luận   : LỖI (P2) F1 — `ops/do_sigpipe.sh:65–70` chỉ chứng minh văn bản khớp, không chứng minh phép gán còn nằm trên đường chạy. Ca có mặt trong tệp nhưng không được sản phẩm đo/thực thi vẫn xanh. Đây là lỗi sức bắt hồi quy của W4; chưa tìm thấy sai hành vi tương ứng trong W1–W3 hiện hành.

HƯỚNG 5: Quét toàn bộ `ops/*.sh`, ngữ cảnh `errexit` và `source`
  giả thuyết : còn pipeline người đọc thoát sớm trên đường CI/review hoặc lời loại trừ trong SPEC sai.
  lệnh       : `rg -n 'head|grep|sed|awk|read|set |source|\|' cay-kho/ops/*.sh`; tìm caller bằng `rg -n -F -e 'kiem_trang_quyet_dinh_test.sh' -e 'don_ref_chot_test.sh' -e 'source ' -e '. "$KICH"' cay-kho/ops/*.sh cay-kho/.github/workflows/*.yml`; `cd tam/tmp.1TQdJ7ghPz && python scan_measure.py`.
  output     : đã đọc/quét đủ 8 tệp: cai_actionlint, cai_cong_cu, chay_lease_publish_test, do_sigpipe, don_ref_chot_test, dung_goi_review, kiem_trang_quyet_dinh, kiem_trang_quyet_dinh_test. Nguồn đầy đủ lưu `logs/all-ops-sh.txt`, phép đo lưu `logs/scan-measure.jsonl`.

| Điểm | Ngữ cảnh và phép đo | Kết luận |
|---|---|---|
| W1:66, W2:189, W3:164 | Không còn pipeline tại ba phép gán; kiểm tất định ở HƯỚNG 3 | Đã vá |
| cai_cong_cu:69,73 | `tail -n +2`/`tail -1` đọc hết; đầu vào 20.000 dòng → rc=0, đầu phần còn lại=2, dòng cuối=20000 | KHÔNG PHẢI LỖI |
| cai_cong_cu:43,67; dung_goi_review:95 | `while read` lặp đến EOF, không `break`/`return` sớm; rig đọc đủ 20.000/20.000 | KHÔNG PHẢI LỖI |
| dung_goi_review:180 | Pipeline có `grep -m1` nhưng nằm trong `|| true`; đo banner + CRLF + 20.000 dòng → rc=0, `ban=<1.2.3>` | KHÔNG PHẢI LỖI; lý do giữ trong commit đúng |
| kiem_trang_quyet_dinh_test:34,37 | Chạy độc lập không `-e`; đầu vào lớn cho assignment rc=141 nhưng vẫn sống và giá trị đầu đúng | KHÔNG PHẢI LỖI ở ngữ cảnh caller tìm được |
| don_ref_chot_test:327,333 | `if ! ... grep -q`; không giết script dù có `-e`, nhưng SIGPIPE ĐẢO kết quả nhánh | Xem phản chứng dưới |
| kiem_trang_quyet_dinh.sh | `grep -nE`, `wc`, hai `awk` đọc hết; `read` dùng here-string, không producer qua pipe | KHÔNG PHẢI LỖI |
| cai_actionlint.sh | `sha256sum/shasum` → `cut` đọc hết; `od -N4` đọc tệp trực tiếp | KHÔNG PHẢI LỖI |
| do_sigpipe.sh | Pipeline cũ nằm trong dữ liệu here-doc đối chứng, chạy ở con; `head -n` trong dựng mutant đọc tệp trực tiếp | Có chủ ý, không bỏ sót sản phẩm |
| chay_lease_publish_test.sh | Gọi installer bằng bash riêng rồi exec Python; không pipeline đọc sớm | KHÔNG PHẢI LỖI |

  `set -uo pipefail` KHÔNG tắt `-e` thừa kế: rig `set -euo pipefail; source sourced.sh` (tệp con chỉ `set -uo pipefail` rồi pipeline đầu) → rc=141. Tuy nhiên, không tìm thấy caller source hai script test này trong tập caller kiểm tra; source thực trong ops là `. "$KICH" "$cong_cu"` ở cai_cong_cu:54, gọi lại chính W1 đã vá. Không kết luận “không ghi set -e” đồng nghĩa miễn nhiễm khi source; cũng không nâng một caller source giả định thành lỗi PR.

  Phản chứng lời loại trừ của SPEC §3: `if ! printf ... | grep -q '^GIA_REF_STATE='` với match ở đầu và 20.000 dòng → `WRONG_fallback_branch`, rc=0, cả có lẫn không `-e`. Trích nguyên hàm `lam()` từ don_ref_chot_test.sh, truyền `GIA_REF_STATE=explicit`, `NEO_TEP=explicit` và 20.000 đối số đệm; thay riêng lệnh `env` bằng recorder để không thực hiện thao tác thật. Output: `GIA_REF_STATE=explicit`, `NEO_TEP=explicit`, rồi thêm `GIA_REF_STATE=.../refstate` và `NEO_TEP=.../neo_auto`. Như vậy giá trị explicit bị fallback ghi đè, không phải nhánh “đã thấy” như SPEC viết.
  kết luận   : LỖI (P2) B1 — lời kết luận an toàn trong SPEC §3 sai; lỗi hành vi có sẵn ở baseline `ops/don_ref_chot_test.sh:327,333`, không do PR này tạo. Không thấy điểm mới gây thoát bởi `-e`+pipefail trên đường source/caller thực đã tìm được. B1 cần handoff cho điều phối/successor, không tự sửa tệp ngoài W1–W4 và không yêu cầu mở write set của PR hiện tại.

HƯỚNG 6: Fail-close và độ phủ đầu vào của W4
  giả thuyết : mất phép đo bị bỏ qua hoặc có ca chỉ được đếm mà không chạy.
  lệnh       : `python review_checks.py mutations`; xem `logs/mutations.jsonl` và các `logs/w4-mut-*.{stdout,stderr}`.
  output     : xóa dòng, thêm `#` trước dòng, đổi tên biến, hai dòng cùng tên, không tham chiếu input, dòng nối bằng `\`, `--lan 0`, thiếu giá trị option, gốc không tồn tại → rc=2, có `KHÔNG ĐO ĐƯỢC`. Xóa tệp W2 thì chết sớm tại lệnh `cp` trong tự kiểm W1: rc=1, `cp: cannot stat .../cai_actionlint.sh`; không in tổng kết xanh.
  kết luận   : KHÔNG PHẢI LỖI về fail-close: mọi trường hợp không đo được vừa thử đều khác 0. Có lệch nhỏ về chẩn đoán, ghi F2 dưới đây. Dấu `#` thông thường và tên biến trùng/sai bị bắt; here-doc/hàm không gọi lọt là F1. Không thấy `return` sớm hay phép so sánh luôn đúng trong 42 ca hiện hành; số ca đơn thuần không chứng minh mã sản phẩm đã chạy (F1).

  Đột biến nội dung bổ sung: nối `; LENH="${LENH//\*/}"` vào dòng W1, W4 vẫn `42/42`, rc=0 (`logs/w4-mut-strip-star.stdout`). Bộ 11 đầu vào W4 không có `*`, nên không phân biệt được mất ký tự đó. Đây là giới hạn cụ thể của corpus W4, không phải lỗi glob của phép khai triển hiện hành (5.436 ca độc lập đã xanh). Nên đưa các đầu vào glob/`%`/chỉ LF của HƯỚNG 2 vào tập đo lâu dài; không diễn giải 42/42 thành chứng minh mọi nội dung.

  kết luận chẩn đoán : LỖI (P3) F2 — `ops/do_sigpipe.sh:121` đọc/copy toàn bộ ba tệp trước khi `trich()` kiểm tệp thứ hai/thứ ba. Vì vậy hợp đồng mã thoát ở dòng 18 (“2 = ... thiếu tệp”) không đúng cho W2/W3 thiếu. Vẫn fail-close, không phải xanh giả.

HƯỚNG 7: Tự kiểm (c) có đo việc (b) thực sự báo ĐỎ?
  giả thuyết : (c) chỉ kiểm lại rc của pipeline, không đi qua chốt phân loại của (b).
  lệnh       : `cd tam/tmp.1TQdJ7ghPz && python additional_measure.py`. Chỉ trên bản sao W4, thay đúng nhánh `if [ "$DEM_0" -eq "$LAN" ]; then ghi 0 "" ""` ở dòng 116 bằng `if true; then ghi 0 "" ""`; chạy bản sao ấy với W1–W3 baseline. Mã/nhật ký: `w4-b-score-disabled.sh`, `logs/w4-selfcheck-score-disabled.stdout`.
  output     : W4 thật + baseline → `39/42`, rc=1 (HƯỚNG 3); W4 vô hiệu hóa chốt (b) + cùng baseline → `42/42 DAT`, rc=0; cả ba ca tự kiểm (c) vẫn đạt dù không điểm sản phẩm nào được chấm ĐỎ.
  kết luận   : LỖI (P2) F3 — `ops/do_sigpipe.sh:127–131` không kiểm hợp đồng “(b) phải đỏ” của §6c/dòng 119. Nó gọi `dem_rc` rồi chấp nhận 141 riêng, nên nhánh quyết định của (b) có thể hỏng mà tự kiểm vẫn xanh. Không nói W4 hiện tại bỏ lọt baseline: HƯỚNG 3 đã chứng minh nó bắt được; finding là tự kiểm không khóa được chốt mà nó tuyên bố khóa.

  Bổ sung phép đo HƯỚNG 6: `additional_measure.py` với `DAU_RA=$'a*b\nnext'` → baseline `<a*b>`, head `<a*b>`, mutant strip-star `<ab>`, đều rc=0. Chạy nguyên W1 với producer 20.000 dòng (lệnh `:` + 19.999 biến môi trường hợp lệ): head rc=0 và `PROBED`, baseline rc=141 và stdout rỗng. `--lan 1` trên head vẫn `42/42`, rc=0. Xóa W1 → rc=2 + KHÔNG ĐO ĐƯỢC; xóa W3 → rc=1 ở `cp`, cùng F2 như W2.

HƯỚNG 8: Hồi quy trên cả head và baseline (§7 A2–A4)
  giả thuyết : thay đổi gây delta ở gate hiện có hoặc còn rc=141 trên đường cài thực.
  lệnh       : trong `tam/tmp.1TQdJ7ghPz`, chạy `python review_checks.py regression`, `python regression_retry.py`, `TMPDIR="$PWD/temp" PYTHONDONTWRITEBYTECODE=1 python t5_repeat.py`; mã ghi đầy đủ argv, env fixture và rc. Mỗi lệnh bên dưới chạy với cwd lần lượt `head/` và `base/`.

| Phép đo | Head | Baseline | Kết luận/delta |
|---|---|---|---|
| `python ops/bash_nen.py quet --root .` | rc=0, `DAT: không có lời gọi trần mới`, 19,543 s | cùng output, rc=0, 18,842 s | KHÔNG PHẢI LỖI, delta=0 |
| `python .claude/dev/ci_dang_ky_test.py` mặc định, Git fixture không ký | rc=0, đăng ký 22/22; phản chứng 938/938 đỏ đúng; `TỔNG: ĐẠT`, 6,773 s | cùng output, rc=0, 6,799 s | KHÔNG PHẢI LỖI, delta=0; output 54.062 byte giống hệt |
| `actionlint .github/workflows/*.yml`, actionlint 1.7.7, ShellCheck 0.11.0 trên PATH | rc=1, một SC1003 ở ops-don-ref.yml:117 | rc=1, đúng cùng cảnh báo | KHÔNG PHẢI LỖI phát sinh; output 224 byte giống hệt, delta=0 |
| `shellcheck --format=json W1 W2 W3 [W4 trên head]`, 0.11.0 | rc=1, chỉ SC1090 ở cai_cong_cu.sh:54 | đúng cùng SC1090 | KHÔNG PHẢI LỖI phát sinh; output 216 byte giống hệt, delta=0; W4 không cảnh báo |
| `bash -n ops/*.sh` (từng tệp) | 8/8 rc=0 | 7/7 rc=0 | KHÔNG PHẢI LỖI |
| Gọi thẳng `bash ops/cai_cong_cu.sh actionlint` trong fixture t5, 200 lần/cây | 200/200 rc=0 và JSON DAT/1.7.7; rc141=0; 42,171 s | 200/200 tương tự; rc141=0; 43,131 s | A2 phần lặp t5 đạt; mẫu nhỏ baseline không phủ định race |
| `python -m ruff check --select F --no-cache` | rc=1, `No module named ruff` | cùng lỗi | KHÔNG ĐO ĐƯỢC lint F; không gọi thiếu tool là đạt |
| `python ops/cong_cu_test.py` toàn bộ, mặc định | not_run | not_run | KHÔNG ĐO ĐƯỢC: không chạy bộ dài ~20–30 phút/cây trong lượt này; không có N/N/thời gian để chứng nhận A2 toàn bộ |

  Điều kiện hồi quy: Python 3.11.15. t5 dùng đúng helper `_goi_actionlint_gia`, `AL_GOI`, `AL_SHA256`, `AL_DICH`, actionlint sai 9.9.9 có sẵn trên PATH và gói cài 1.7.7; mỗi lần kiểm cả mã thoát lẫn dữ liệu DAT/1.7.7. Không tải/cài qua mạng.

  Lần đầu ci_dang_ky_test trên cả hai cây rc=1 vì Git fixture kế thừa ký commit bằng dịch vụ localhost không truy cập được trong sandbox, không phải assertion do patch. Phép đo lại chỉ thêm cấu hình môi trường tiến trình `GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=commit.gpgsign GIT_CONFIG_VALUE_0=false` để commit fixture cục bộ; không đổi git config hay nguồn hai cây. ShellCheck không có trên PATH ban đầu; tìm thấy binary ELF 0.11.0 có sẵn và sao chép vào `tam/tmp.1TQdJ7ghPz/bin/shellcheck` trước lượt đo lại. Actionlint ban đầu không có ShellCheck cho rc=0 ở cả hai cây; kết luận cuối dùng lượt có ShellCheck, không lấy xanh thiếu phép đo.

  Nhật ký: `logs/regression.jsonl`, `logs/regression-retry.jsonl`, `logs/t5-repeat.jsonl`, từng stdout/stderr đầy đủ trong `logs/`. `additional_measure.py` so byte output xác nhận `stdout_equal=true` cho bash_nen, ci_dang_ky, actionlint+ShellCheck và shellcheck.

HƯỚNG 9: Commit message, chú thích và xuất xứ lời khai
  giả thuyết : lời khai đo rộng hơn bằng chứng có thể kiểm độc lập.
  lệnh       : `git -C cay-kho log cd23c7d..HEAD --format=fuller`; `git -C cay-kho diff cd23c7d -- ops/cai_cong_cu.sh ops/cai_actionlint.sh ops/dung_goi_review.sh ops/do_sigpipe.sh`; `strace -e trace=write bash -c "printf ..."` qua `run('strace-capability', ...)`.
  output     : một commit 41d03d8..., tự khai bash 5.2.21, 2/3000 pipeline hai dòng, 0/3000 khai triển và 10/10 rc141 trên 20.000 dòng. Những số này trùng SPEC §2 (bằng chứng phiên điều phối). W1:64 và W4:5–7 chép số/cơ chế, không nêu lại nguồn điều phối. Không có log của phép chạy 3.000 lần hay attestation executor trong vật liệu chỉ định. Strace reviewer rc=1: `PTRACE_TRACEME: Operation not permitted`; nhật ký `logs/strace-capability.stderr`.
  kết luận   : KHÔNG ĐO ĐƯỢC nguồn gốc “executor tự đo lại” của 2/3000 và 0/3000, cũng không xác nhận được khẳng định “một write() mỗi dòng” bằng strace trong sandbox. Không gọi các số ấy là giả chỉ vì thiếu log. Phần 20.000 dòng/10 lần và cơ chế rc141 đã được đo độc lập ở HƯỚNG 3; lý do giữ grep-m1 được xác nhận ở HƯỚNG 5. Nên gắn rõ số 3.000 lần với nguồn §2 hoặc kèm log đo lại. Chú thích mới W1–W3 là ASCII không dấu, gắn #675 và chỉ phép đo; không thấy lỗi idiom riêng. Lời “(b) phải đỏ” của W4 rộng hơn tự kiểm thực tế là F3, “thiếu tệp →2” là F2.

HƯỚNG 10: Đối chiếu từng tiêu chí §5–§7 và chốt phạm vi
  giả thuyết : đủ điều kiện approve theo SPEC.
  lệnh       : tập lệnh các HƯỚNG 1–9; cuối lượt `git -C cay-kho diff cd23c7d --check`, status hai cây, SHA-256 SPEC và HEAD.
  output     : diff --check rc=0; hai worktree vẫn sạch; SPEC hash giữ nguyên. Tổng kết đối chiếu:

| Tiêu chí | Trạng thái |
|---|---|
| §5 khai triển tham số; CR tương đương; không đổi ngoài dòng vá/chú thích | Đạt trên tập đo; diff đúng ba điểm |
| §5 idiom chú thích | Đạt; provenance các số lịch sử chưa xác nhận |
| §6 Linux, `set -euo pipefail`, đo trong con, `--lan N` | Đạt ở môi trường nêu trên |
| §6 trích chính script, không thấy phải đỏ | Có trích thật; phần mã chết bị lọt F1; thiếu tệp vẫn fail-close nhưng mã/chẩn đoán lệch F2 |
| §6a tương đương 11 đầu vào yêu cầu | W4 đạt; reviewer mở rộng 5.436 so sánh đạt; giới hạn glob corpus đã nêu |
| §6b ≥20.000 dòng, cũ luôn141, mới luôn0 | Đạt 10/10 từng điểm |
| §6c tự kiểm buộc (b) đỏ khi đột biến | Bắt baseline ở phép đo ngoài; tự kiểm không khóa chốt phân loại, F3 |
| §6 tổng N/N và điều kiện đo | 42/42; có bash/lõi/lần/dòng |
| A1 | Đạt trên head/baseline và từng điểm riêng |
| A2 | t5 200/200 đạt; suite mặc định KHÔNG ĐO ĐƯỢC |
| A3 | bash_nen, actionlint, shellcheck không delta; ruff KHÔNG ĐO ĐƯỢC |
| A4 | 938/938 phản chứng, rc=0 hai cây sau cô lập ký Git fixture; delta=0 |
| A5 | Review độc lập đã thực hiện nhưng chưa 0 P2/P3; không đăng GitHub theo chỉ thị lượt này |

  kết luận   : LỖI (P2) F1, F3 và LỖI (P3) F2 còn mở trong W4 ⇒ `changes_requested`. Không phát hiện P1 mới ở ba dòng vá W1–W3. B1 là vấn đề nền/lời loại trừ SPEC cần handoff riêng; không tự mở write set. Không chứng nhận các gate ghi KHÔNG ĐO ĐƯỢC là pass.

Bảng findings (gợi ý để executor tự sửa và tự đo; reviewer không vá mã sản phẩm):

| ID | Hạng | Tệp:dòng | Mô tả | Đề xuất vá, ca khóa, rủi ro |
|---|---|---|---|---|
| F1 | P2 | `ops/do_sigpipe.sh:67` | Trích dòng từ here-doc hoặc hàm không gọi vẫn 42/42, trong khi script thật chết vì chưa gán biến. | **Ở đâu/cách:** giữ trích từ nguồn, bổ sung phép đo đường chạy thực với producer/binary giả và sentinel/giá trị đầu ra; hoặc phân tích cú pháp rồi từ chối ngữ cảnh không được chứng minh. Không chỉ thêm regex để bỏ `#`. **Khóa:** head phải xanh; hai mutant `unused-function`/`heredoc` phải đỏ vì phép gán không chạy; baseline vẫn đỏ141. **Rủi ro:** gọi script thật có thể cài/mirror; dùng cây và fixture offline trong thư mục tạm, không chạy mạng hay thao tác thật. |
| F2 | P3 | `ops/do_sigpipe.sh:121` (hợp đồng ở :18) | Thiếu W2/W3 trả1 từ cp, không có KHÔNG ĐO ĐƯỢC, trái hợp đồng mã2. | **Ở đâu/cách:** kiểm đủ ba tệp trước vòng đo hoặc chuyển lỗi cp/trích thành `khong_do` có tên tệp; không nuốt lỗi. **Khóa:** xóa riêng W1/W2/W3 đều phải rc2, thông báo thiếu tệp và không tổng kết xanh. **Rủi ro:** preflight không loại được lỗi đọc phát sinh sau đó; vẫn xử lý lỗi ngay tại thao tác. |
| F3 | P2 | `ops/do_sigpipe.sh:129` | Tự kiểm chỉ xác nhận pipeline mutant trả141, không xác nhận bộ chấm (b) từ chối nó. Nhánh chấm b bị đổi thành luôn đúng mà (c) vẫn xanh. | **Ở đâu/cách:** dùng chung một hàm phán quyết (b); self-check đưa mutant vào chính hàm ấy và đòi kết quả đỏ với lý do141, hoặc chạy chế độ con chỉ (a)/(b) để tránh tự kiểm đệ quy. **Khóa:** mutant dòng116 `if true` phải làm self-check đỏ; code thật/baseline vẫn lần lượt xanh/đỏ; phân biệt lỗi dựng fixture với SIGPIPE. **Rủi ro:** tránh tạo kiểm tra đệ quy vô hạn hay sửa bộ đếm của phép đo cha để cấp tín dụng giả. |
| B1 | P2, có sẵn ở nền; handoff riêng | `SPEC.md:32`; `ops/don_ref_chot_test.sh:327,333` | SPEC nói rc141 đi nhánh “đã thấy” nhưng `if !` thực tế đi fallback, thêm biến mặc định đè cấu hình explicit. | **Ở đâu/cách:** điều phối đính chính lời loại trừ; successor cho test helper duyệt trực tiếp từng đối số bằng `case` hoặc dùng phép đọc hết thay grep-q. Không sửa ngoài write set ở packet này. **Khóa:** match ở đầu + payload lớn vẫn giữ đúng explicit, không append fallback; không-match vẫn tạo mặc định. **Rủi ro:** giữ nguyên quy tắc match theo đầu từng đối số và cách xử lý biến lặp, không vô tình mở rộng match chuỗi con. |

Ngưỡng áp dụng: 0 P1 / 0 P2 / 0 P3 theo prompt/SPEC, chặt hơn mặc định của repository. Findings trong diff: 0 P1, 2 P2, 1 P3; bổ sung B1 P2 có sẵn ở baseline. Gợi ý vá có thể làm vượt mức 150 dòng thêm đang chạm trần; executor/điều phối cần giữ trong giới hạn hoặc sửa SPEC trước khi mở rộng, reviewer không tự cấp quyền.

Model/effort đang chạy: GPT-6 / effort KHÔNG ĐO ĐƯỢC — tự khai theo chỉ dẫn phiên; không có attestation runtime độc lập để chứng nhận biến thể model hay mức effort. Provider OpenAI; bề mặt thực quan sát được là Codex qua API với công cụ shell, transport machine/tool trực tiếp; không tự nhận ChatGPT Web hoặc danh tính tài khoản đăng GitHub. Không đăng verdict lên GitHub.
