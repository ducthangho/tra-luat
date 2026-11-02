Verdict: approve
Reviewed commit: 356a27e1378b2162bbc0be2ec06ff08fdacbdead
Spec sha256: d5dd5a5df5a2dd8ce799a30442ed974fa3a0d669728446fafdbc2267a59b5b1d

**P0=0, P1=0, P2=0, P3=0 mở.** Trở ngại `snapshot-thieu-object-lich-su` của lượt 8 đã được khắc phục trong bản sao review mới, không thay đổi cây mã được review. Tôi tự đo C6 **rc=0, 0 KHÔNG ĐO ĐƯỢC, tổng 306, TỔNG: ĐẠT** và toàn suite Linux **98/98 · 153/153 · 2/2, TỔNG: ĐẠT**. c14/c40/c76 đều ĐẠT; giữ nguyên mẫu số 98. Không dùng lời khai executor thay cho các phép đo này.

C4 còn giới hạn đọc trực tiếp input dispatch gốc; C7 Windows local KHÔNG ĐO ĐƯỢC. Theo chỉ thị lượt 9, các giới hạn này tự chúng không phải finding mã và không chặn verdict khi C6/suite Linux đạt, không còn P0–P3 mở. **Verdict không cấp quyền merge/land.** Đây là lượt 9/9 theo chỉ thị hiện hành; không khởi tạo lượt review tiếp theo.

## Neo và cách tái hiện

Reviewer: OpenAI/Codex, họ `openai`, phiên độc lập với executor họ Claude. Bề mặt thực tế quan sát được: agent gọi shell trong sandbox Linux và công cụ GitHub qua API, transport máy. Không suy model ID/effort đã phục vụ từ tài khoản GitHub hoặc tự nhận có attestation launcher; không đăng verdict/receipt lên GitHub trong lượt này.

| Neo | Kết quả độc lập |
|---|---|
| HEAD | `356a27e1378b2162bbc0be2ec06ff08fdacbdead`, detached |
| Tree | `c1e160cfd5ddf1a053c2e8413e62f5881badd052`, giống lượt 8 |
| Base diff tổng | `b29da0bfe3bfb7a7be69136a1c5c40f82c088a93`, là tổ tiên HEAD |
| SPEC | SHA-256 khớp dòng 3 |
| VERDICT-LUOT8.md | SHA-256 `bd891b299d189b83973db7cde3f184b9a17bcc1d3dd5ff7a0e6ee08b068b6ece` |
| Checkout | Không nông; tracked/untracked/ignored sạch; `core.abbrev=7` |
| Write set | Chỉ `ops/bien_nhan_v2.py` và `ops/bien_nhan_v2_test.py` |
| Numstat tổng | Sản phẩm +40/−5; test +300/−2 |
| Môi trường | Linux x86_64; Python 3.13.18; Git 2.43.0; Ruff 0.16.9 |

[Preflight và các lệnh Git](evidence/14-initial.stdout.txt), [command/cwd/rc/thời gian](evidence/14-initial.json), [tóm tắt neo](evidence/initial-summary.json). Hai patch đầu vào khớp byte với git diff. So với snapshot cuối lượt 8, HEAD/tree, **toàn bộ nội dung 8.468 tệp tracked**, trạng thái và diff staged/unstaged đều bằng nhau; không đòi index của hai clone khác nhau phải có cùng byte.

| Tệp | SHA-256 lượt 8 = đầu lượt 9 = cuối lượt 9 |
|---|---|
| `ops/bien_nhan_v2.py` | `7f9a86f3fc07429877f2959ad2ecbe238ef145d08860b8f78197340a06e276a6` |
| `ops/bien_nhan_v2_test.py` | `cac81d460abd280c461cf0acf938e412fc4b1c4cb477f36b55d2c5b1b0474b87` |

`git cat-file -t 4bc94325e647ee5e32373f3af30b8f83b98a90fa` trả **commit**, rc=0. `for-each-ref --contains` trả đúng hai ref, cả hai trỏ chính commit này:

- `refs/tags/luu-tru/lease-publish-windows-do-r1-verdict`.
- `refs/remotes/origin/ops/do-lease-publish-windows-150`.

`merge-base --is-ancestor` của object với mỗi ref trả 0. Với HEAD trả 1: object được giữ qua ref lưu trữ, **không là tổ tiên HEAD**. Điều này phù hợp nội dung receipt lịch sử; không biến commit thử CI thành commit đã land. [Receipt đã đọc](evidence/37-ancestry-context.stdout.txt). Không sửa receipt, tag hoặc ref.

Từ gốc sandbox, tái hiện bằng [review_run.py](review_run.py) với nhãn mới:

```sh
export PYTHONDONTWRITEBYTECODE=1 PYTHONUTF8=1 PYTHONIOENCODING=utf-8
export GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_SYSTEM=/dev/null GIT_OPTIONAL_LOCKS=0
export TMPDIR="$PWD/evidence/tmp"
python3 review_run.py replay-c6 cay-kho python3 ops/bien_nhan_v2.py --root .
python3 review_run.py replay-suite cay-kho python3 ops/bien_nhan_v2_test.py
python3 review_run.py replay-count cay-kho python3 -c 'import os; print(sum(n.lower().endswith(".receipt.yaml") for n in os.listdir("ops/reviews")))'
python3 review_run.py replay-focused . python3 probe.py focused
python3 review_run.py replay-c1 . python3 probe.py c1
python3 review_run.py replay-comments . python3 probe.py comments
python3 review_run.py replay-ruff . python3 ruff_delta.py
```

Driver lưu command/cwd/rc/thời gian/môi trường trong `evidence/<nhãn>.json`, stdout/stderr trong hai tệp tương ứng. Các script `audit.py`, `probe.py`, `ruff_delta.py` được chép nguyên byte từ bằng chứng lượt 8 về gốc để `ROOT` trỏ đúng sandbox; [băm bản chép](evidence/13-prepare.stdout.txt). Đột biến dùng `_dot_bien_tep`, chỉ sửa bản sao trong TMPDIR, phục hồi module/CONG và dọn fixture. API GitHub lưu đầy đủ tên công cụ/đối số hoặc URL/thời gian/kết quả; trạng thái tool không được giả thành rc của tiến trình shell.

## ĐỐI CHIẾU LƯỢT TRƯỚC

| Lớp/phạm vi | Đo lại hoặc kế thừa có căn cứ | Kết luận |
|---|---|---|
| `snapshot-thieu-object-lich-su` | Object thật có mặt, ref/ancestry như trên; C6 rc=0/tổng 306/0 KHÔNG ĐO ĐƯỢC; suite 98/98, riêng c14/c40/c76 ĐẠT. | **ĐÃ KHẮC PHỤC THẬT** trở ngại snapshot; không phải sửa mã. |
| P3 lượt 7 `chu-thich-tro-sai-ca-ngoai-le-lap-trinh` | Đo mới sạch c99/c100 đều qua; m153 làm c100 `giet_that` vì nuốt RuntimeError, c99 vẫn qua; c18 sạch. Docstring sản phẩm:90 trỏ c100 chốt 7. | **ĐÃ VÁ THẬT**, vẫn đóng. |
| F1 `loi-do-liet-ke-thu-muc-thoat-traceback` | Đo riêng m147→c99; m148–m151/m154→c100, đúng `giet_that` và đối chứng sạch. Kế thừa probe CLI liệt kê hai đường của lượt 8 vì toàn tree bằng nhau. | Vẫn đóng. |
| F2 `loi-do-thieu-chot-ngoai-le-lap-trinh` | m152/m153 bị c100 giết vì nuốt RuntimeError; đối chứng nghiêm sạch khi mutant còn hiệu lực. | Vẫn đóng. |
| F3: OSError ngoài PermissionError | m154→c100 và m155→c99 chết đúng **OSError errno=5**; không lấy tín dụng từ EACCES. | Vẫn đóng. |
| P1 `bien-ngoai-cua-so-surface-chua-co-rang` / c88 | c88 sạch; m156 chết tại `ix-trich-dan-sau-hai-dong`; m157 chết tại `ii-b-trich-dan-dong-sau`; c18 sạch. | Vẫn đóng. |
| P3 `chu-thich-nang-ca-thuong-thanh-toan-suite` / m156–m157 | Kế thừa đối chiếu hiện vật lịch sử lượt 7→8; chú thích test:4764 giữ nguyên: no_clamp qua toàn suite, citation_drop_next qua 98 ca thường. | Vẫn đóng; không khai đo lại hiện vật lịch sử. |
| Giải xung đột #1037 | c98 ĐẠT trong suite mới; m142 vẫn nhắm c101. Kế thừa phép tiêm lỗi báo cáo của lượt 8 và các lượt trước. | Vẫn đóng. |

[16 đột biến riêng](evidence/focused-results.json), [đối chiếu c99/c100](evidence/comment-target-results.json), [log suite](evidence/16-suite.stdout.txt), [verdict lượt 8](VERDICT-LUOT8.md), [verdict lượt 7](VERDICT-LUOT7.md).

Phần kế thừa rõ ràng: **71/71 M4, 40 mutant biên, no_clamp toàn suite đỏ, ma trận F1/F2/F3 sâu, probe CLI liệt kê và thí nghiệm báo cáo #1037** đã được lượt 8 chấp nhận. Không chạy lại các tập sâu ấy; cơ sở kế thừa là cùng HEAD/tree và byte mọi tệp tracked, theo quyền trong prompt. Không kế thừa kết quả C6/suite thay cho lần đo mới. Audit còn xác nhận AST thực thi hai nguồn so c8a493c không đổi khi bỏ riêng docstring; không khai AST có docstring bằng nhau.

## Rà diff tổng

Đã đọc toàn [diff b29da0b..HEAD](evidence/19-diff-review.stdout.txt). Helper dùng `iterdir()` + `name.lower().endswith`, không lọc `is_file`, trả `sorted`; cả `kiem` và `_sinh_no` dùng helper. `OSError` được chuyển thành `KhongDoDuoc`, lỗi lập trình đi thẳng. Các ca và đột biến kiểm hai đường gọi, thứ tự, thư mục vắng, EACCES/EIO và RuntimeError. Phần c88/m156/m157 được đo riêng; các thay đổi chú thích khớp ca đích. Không phát hiện P0–P3 mới trong phạm vi diff tổng.

## Bảng tiêu chí

| Tiêu chí | Kết quả | Bằng chứng quyết định |
|---|---|---|
| C1a | **ĐẠT Linux; Windows CI có bằng chứng ca đạt** | Đo mới: hai YAML sai schema rc=1/tổng 2/nêu x; chỉ-x rc=1/tổng 1, không “không có tệp”. c101 ĐẠT trong log Windows. |
| C1b | **ĐẠT Linux; Windows CI có bằng chứng ca đạt** | YAML x hỏng rc=2, stderr nêu x.RECEIPT.YAML, không traceback; không đòi tổng. m142/exact làm cả ba fixture mất tiêu chí. |
| C2 | **ĐẠT Linux; Windows CI có bằng chứng ca đạt** | c89 ĐẠT, m143 lọc is_file bị đúng c89 giết; đối chứng sạch. Log Windows cũng có c89 ĐẠT. |
| C3 | **ĐẠT Linux** | Bản sao hoàn nguyên glob bị c101 `giet_that`: tổng 1 thay 2; c18 sạch. Không thêm glob vào bảng mutant thường. |
| C4 Windows CI | **Đã xác minh SHA/event/workflow/labels/runner/steps/log; input gốc KHÔNG ĐO ĐƯỢC trực tiếp** | Run 41113949578, job 124263645262; workflow_dispatch ci.yml, HEAD đúng, labels windows-latest, runner_id=1000026867; bien-nhan 98/98 · 153/153 · 2/2, TỔNG: ĐẠT; lease 255/255. Chi tiết/giới hạn bên dưới. |
| C5 Ubuntu CI | **ĐẠT run PR gắn đúng HEAD** | Run 41113943723, job 124264022785; event pull_request, head_sha đúng, labels ubuntu-latest, runner_id=1000026883; bien-nhan 98/98 · 153/153 · 2/2, TỔNG: ĐẠT; lease 268/268. Checkout merge thử được phân biệt bên dưới. |
| C6 | **ĐẠT** | rc=0, tổng 306 khớp lệnh đếm riêng 306, 0 KHÔNG ĐO ĐƯỢC, TỔNG: ĐẠT. |
| C7 Windows local | **KHÔNG ĐO ĐƯỢC / không chạy** | Không chạy test Windows từ xa, đúng chỉ thị lượt 9; không nhận lời khai executor. |
| C8 nội dung review | **ĐẠT theo ngưỡng lượt 9** | P0/P1/P2/P3 mở đều 0; C6 và suite Linux đạt trên đúng HEAD. Áp chỉ thị 9/9 hiện hành, không tự sửa SPEC đóng băng và không suy quyền merge/land. |
| C9 | **ĐẠT theo delta** | Ruff thêm 0/mất 0; doctrine sạch 10 tệp; hai diff-check rc=0; rg glob 0 dòng, đối chứng bản sao 1 dòng; numstat đúng hai tệp. |
| Toàn suite Linux | **ĐẠT** | rc=0, **98/98 · 153/153 · 2/2**, TỔNG: ĐẠT; 339.767 giây; stderr rỗng; không có BỎ QUA. |
| Đột biến riêng | **ĐẠT** | 16/16 m142–m157 `giet_that` đúng ca; 16/16 đối chứng nghiêm sạch khi mutant còn hiệu lực. |

C6 nguyên văn:

```text
bien_nhan_v2: 253 ĐẠT v2 · 11/11 miễn trừ legacy (băm khớp) · 42 NỢ đóng băng · 0 vi phạm · 0 KHÔNG ĐO ĐƯỢC · tổng 306
câu lịch sử: nợ L-REVIEW 1 · L-ANCESTRY 60 · L-SURFACE 0 · L-SURFACE chua_do_duoc 0
TỔNG: ĐẠT
```

[C6 stdout](evidence/15-c6.stdout.txt), [lệnh/rc/thời gian](evidence/15-c6.json), [đếm độc lập bằng os.listdir, không lọc is_file](evidence/17-count.json).

Suite nguyên văn:

```text
bien_nhan_v2_test: 98/98 ca đạt · 153/153 đột biến thường CÓ RĂNG · 2/2 ca TỰ KIỂM đạt · 135/153 đột biến thường khai đối chứng
TỔNG: ĐẠT
```

[Suite stdout](evidence/16-suite.stdout.txt), [lệnh/cwd/rc/thời gian](evidence/16-suite.json). Validator còn đếm riêng 98 tên ca ĐẠT, không trùng; xác nhận c14/c40/c76 và c88/c89/c98/c99/c100/c101. Ba ca từng đỏ do snapshot đều xanh, không bỏ hoặc giảm mẫu số.

C1a/C1b/C3: [ma trận 3×3 sạch/exact/glob](evidence/c1-results.json). C9: [delta Ruff](evidence/ruff-delta-results.json), [doctrine](evidence/25-doctrine.stdout.txt), [diff-check tổng](evidence/26-diff-check.json), [diff-check checkout](evidence/27-working-diff-check.json), [rg âm](evidence/28-glob-negative.json), [đối chứng rg dương](evidence/38-glob-positive.stdout.txt). Ruff dùng executable có sẵn với `--no-cache --select F`, lint blob base/head cùng cwd/config, chuẩn hóa path/code/message/nội dung dòng. Hai phía cùng một **F541** có sẵn ở test (HEAD:1681): **delta 0, không phải Ruff sạch tuyệt đối**.

## CI đọc độc lập và giới hạn

Đã đọc mới jobs/logs và API thô, không gọi workflow. Hai lần `gh api` rc=1 vì sandbox không cho mở socket được giữ ở [Windows](evidence/30-ci-raw-windows.stderr.txt), [Ubuntu](evidence/31-ci-raw-ubuntu.stderr.txt); sau đó GET qua plugin trả đầy đủ JSON gốc, giải quyết giới hạn labels/runner_id của lượt 8.

- [Windows run 41113949578 / job 124263645262](https://github.com/ducthangho/tra-luat/actions/runs/41113949578/job/124263645262): checkout đúng HEAD, OS Windows Server 2025; hai bước đều completed/success. Lease-publish **255/255; đã chạy=255, bỏ qua=13**; không viết thành 268/268 hoặc nói không có ca bỏ qua. Chính bước selftest không skipped. [Run thô](evidence/ci-raw-windows-run.json), [jobs thô](evidence/ci-raw-windows-jobs.json), [log](evidence/ci-windows-log.txt).
- [Ubuntu run 41113943723 / job 124264022785](https://github.com/ducthangho/tra-luat/actions/runs/41113943723/job/124264022785): run và job có head_sha đúng HEAD; OS Ubuntu 24.04.5; hai bước completed/success, lease 268/268, bỏ qua 0. Checkout thực tế **00c58bc70286f622914f07e36d72691d192b3949**, merge thử HEAD vào 6db934145acf6e47d01db5b2dc8c9da417c2d8eb. Đây là CI PR gắn HEAD, không khai checkout trực tiếp HEAD. [Run thô](evidence/ci-raw-ubuntu-run.json), [jobs thô](evidence/ci-raw-ubuntu-jobs.json), [log](evidence/ci-ubuntu-log.txt).

Input `runner_set` không có trong JSON run. Đã đọc đủ 16/16 job Windows, chỉ có các job ma trận Windows; [biểu thức workflow trên HEAD](evidence/33-workflow-input.stdout.txt) chỉ chọn ma trận đó cho dispatch windows-only. Đây là **suy luận từ workflow và đồ thị job độc lập**, không phải đọc được payload input gốc; vẫn giữ giới hạn ở C4. Labels/runner_id nêu trên là dữ liệu API thô, không suy từ tên job/OS. C7 không có phép đo local. Không biến các giới hạn này thành finding mã mới.

## Bảng finding

**Tổng finding mở: 0 — P0=0, P1=0, P2=0, P3=0.** Không có finding mới cần mục vị trí/tái hiện/HÌNH DẠNG/hướng vá.

| Mục | Loại | Trạng thái |
|---|---|---|
| `snapshot-thieu-object-lich-su` | Trở ngại snapshot/bằng chứng, không gán severity mã | Đã khắc phục; C6 và suite đo mới đạt |
| Các lớp P lịch sử | Finding đã đóng, chi tiết bảng đối chiếu | Giữ đóng bằng đo lại/kế thừa được phép |
| C4 input dispatch gốc; C7 local | Giới hạn phép đo | Khai rõ, không tính thành finding mã |

## Kiểm tra cuối và giới hạn

[validate_review.py](validate_review.py) kiểm rc thật, chuỗi tổng và mẫu số, 98 tên ca, riêng c14/c40/c76, từng đột biến/đối chứng, delta Ruff, dữ liệu CI thô và snapshot. Kết quả **FINAL EVIDENCE ASSERTIONS PASS** trong [final-validation.json](evidence/final-validation.json).

Snapshot [đầu](evidence/snapshot-before.json) / [cuối](evidence/snapshot-after.json) bằng nhau về HEAD/tree, index, băm 8.468 tệp tracked, diff staged/unstaged và trạng thái tracked/untracked/ignored. TMPDIR đã rỗng. Đây là so sánh hai mốc quan sát; không suy thành audit toàn bộ lịch sử ghi. Không sửa tệp trong cay-kho, không commit/push/fetch hay gọi workflow trên kho được review. Các kho fixture riêng trong sandbox do bộ test dựng không phải cây executor.

Verdict đã được tạo và cập nhật từ đầu lượt; bản tiến độ giữ ở [VERDICT-progress.md](evidence/VERDICT-progress.md). Kết luận approve chỉ áp cho exact HEAD trên và phạm vi review này; metadata/model attestation và thủ tục cấp quyền land thuộc bước giao nhận riêng, không được verdict tự cấp.
