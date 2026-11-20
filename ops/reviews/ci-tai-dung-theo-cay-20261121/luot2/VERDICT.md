# Review đặc tả lượt 2 — CI-TAI-DUNG-THEO-CAY

**Kết luận: `changes_requested`.** Còn **7 P2 và 3 P3** được liệt kê dưới đây; không phát hiện P0/P1 mới. Cả A r3, B1 r1 và B2 r1 đều cần revision trước khi duyệt băm.

Reviewer: Codex, họ model OpenAI; review đặc tả, chưa có mã triển khai B1/B2. Thực hiện theo `PROMPT.md`: chỉ đọc trong RV, không mạng, không đọc `.codex`/memory; mọi script, bản sao, kho Git thử và kết quả mới nằm trong `out/`. Luật L1–L7 được lấy từ bản `cay-kho/.claude/skills/soan-spec/SKILL.md` được chỉ định trong đề bài. Không thực hiện quy trình soạn spec, cấp lease, push hay gửi thông điệp ra ngoài.

## Neo đã kiểm

| Đối tượng | Giá trị |
|---|---|
| SHA-256 `SPEC-A-r3.md` | `957c4bec3bd5f18d5804fccb5c721f854420e800129fd1af765b8f1adf27f0d5` |
| SHA-256 `SPEC-B1-r1.md` | `fd24105a394ea8a4a020c3f3af08964a82d4a8c81658991f6acfff8e3512ebf2` |
| SHA-256 `SPEC-B2-r1.md` | `f705edcff5dfea3a00040361f53a3a694438ababa01dc2fe1f7db400f86e6d77` |
| `cay-kho` HEAD | `45bae8d07a8cdf06a1ca9a7a2e015a6258169379` |
| HEAD tree | `30d5c7dec30dc658ae04ef29a6ffafe94eb8f197` |
| Ref cục bộ `origin/master` | `a31c680c8880786848f832a35554d9e84078b270` — khác HEAD đóng gói; review neo HEAD, không đổi nền |
| Lịch sử và working tree | `--is-shallow-repository=false`; `git status --porcelain` rỗng trước và sau các phép thử |
| Môi trường | Windows, Python 3.13, `python -S`; PyYAML 6.0.3 từ `RV/py-lib` |
| Ngày đo | 20-11-2026; thời điểm UTC từng lệnh trong `review-evidence/commands.jsonl` |

Băm A r2/B r2 khớp verdict cũ. Hai OID land ADR-0053/0055 đều qua ba phép: có tệp tại L (`rc=0`), chưa có tại L^1 (`rc=128`), L thuộc first-parent của HEAD. Trần sensitive là **6 tệp / 450 dòng thêm**, không phải dòng thêm cộng xoá. Không có thay đổi trong tập đường dẫn B1:218–220 giữa `94cbb36` và HEAD.

Script tái lập: [review_r2.py](review_r2.py), [review_probes.py](review_probes.py) sao từ lượt 1, [review_tools.py](review_tools.py). Wrapper đặt `PYTHONPATH`, tắt bytecode, đặt TEMP/TMP dưới `out/thu`, vô hiệu cấu hình Git người dùng và ghi command/cwd/rc/output. Các mô hình hợp đồng bên dưới **không phải** kết quả chạy GitHub Actions hay mã B1/B2 chưa tồn tại. Hàm REST thật chỉ được thử với opener giả trong bộ nhớ, không kết nối mạng.

## Trạng thái F1–F10 của lượt 1

| Finding cũ | Trạng thái lượt 2 | Phép đo và kết quả |
|---|---|---|
| F1 P1 — so nhầm consumer, push nhiều commit | **Đóng phản chứng cũ.** Còn vấn đề mới ở phép xử lý lỗi, N6. | `review_r2.py rename`: chạy lại fixture Git cũ; với `before=O`, chốt mới loại. Dựng lại `before=P1`: PR diff `docs/f.py`, push diff `scripts/f.py`; kế hoạch thực cho pretooluse là `nhe` / `day_du`, nên loại `nhanh`. Cùng cha và cây không còn làm phản chứng này lọt. |
| F2 P2 — thiếu chốt ghim/write set | **Chưa đóng**, N2. | `pins`: tám dấu vân Windows vẫn đổi đúng như lượt 1, nay đã có trong B2; nhưng B1 còn thiếu `y14/RUN_BUOC_PACKET`, B2 còn thiếu `y03/y04/y06/y07/y14` và các bảng liên quan. |
| F3 P2 — đòi suite Windows từ bước Linux-only | **Đóng ở mức thiết kế.** | `inventory` xác nhận bước vẫn Linux-only; B1:16–19,157 và B2:14–17,91 nay yêu cầu chạy trực tiếp trên máy Windows chủ kho theo M3, không dùng job skipped làm bằng chứng. Chưa chạy M3 cho triển khai tương lai. |
| F4 P2 — attempt/schema/matrix/runtime/provenance | **Đóng một phần; chưa đủ để đóng toàn finding.** | `contract`: attempt 2, schema 999, SHA sai định dạng và shard lặp bị loại; image từng job được thu hẹp công khai thành image `chuan-bi` ở A G3; B2 đã truyền attempt. Nhưng hậu kiểm vẫn không ràng lại nội dung/identity bằng chứng được ghi, N3. SHA 40 hex khác vẫn qua phép 4d; không coi kiểm định dạng là chứng minh checkout/workflow definition. |
| F5 P2 — T4 và phạm vi fallback mâu thuẫn | **Đóng.** | `policy_probe` vẫn đo push hồ sơ = `duong_nhanh`, packet-loop = `chay`; Q4/R mới không còn phủ nhận nền đó. `a_check` xác nhận T4 mới là một trong bốn thay đổi bắt buộc, Q5 phân biệt lỗi chung/lỗi nhóm. |
| F6 P2 — thước đo A bỏ lọt nội dung | **Đóng phần protocol; chưa đóng toàn finding**, N5. | `a_check`: xoá câu khác của §10.1, bỏ P2, nhân đôi DONG20 đều đỏ; nhưng bảng ngoại lệ trong Quyết định và Bối cảnh rỗng vẫn qua A2/A3/A4/A6, `adr-song`, `doctrine-scan` và A5 hai tệp. |
| F7 P3 — thiếu tiền đề cho phép đo dương | **Đóng thiếu sót cũ.** Có vấn đề hậu kiểm mới N1/N3/N7. | `f7_closure` chạy lại fixture cũ: diff PR/push khác nhau nhưng kế hoạch registry thật bằng nhau, nên fixture này không còn bác vế dương mới. B1:170–176 cũng đã yêu cầu run/attempt hoàn tất, đủ nhóm, kế hoạch và image bằng nhau; thiếu thì `not_measured`. |
| F8 P2 — canary không kiểm nguồn | **Chưa đóng**, N1/N3. | Đã thêm replay từ REST/git, nhưng hợp đồng chỉ so tập nhóm. Đổi source run, sửa kế hoạch hoặc bỏ danh sách job trong bằng chứng có thể không đổi kết quả; B2 đúng thiết kế lại bị replay báo `LECH_BONG`. |
| F9 P3 — ước kích thước thiếu cơ sở/consumer | **Đóng phần bảng và số tham chiếu; vẫn mở**, N9. | `anchor` đo lại numstat #674/#1343; `runtime_and_size` cộng B1 đúng 450, dư 0. Các consumer mới tìm được chưa nằm trong khối sửa chốt; phương án chuyển replay sang B2 phải sửa cả thứ tự phụ thuộc. |
| F10 P3 — L6/L7 và đo trước đóng băng | **Đóng phần lớn L6; còn L7**, N8. | Có bảng năm vế, 0 marker tại sáu cổng + classifier, script A trùng bản tác giả và đã chạy lại. A:100 vẫn nhắc duyệt băm không mang E; các câu E5 chưa khai đủ hồ sơ theo ADR-0067, câu E3 thiếu quyết định bị đảo/hậu quả giữ nguyên. |

“Đóng” ở đây là đóng lỗi **đặc tả** đã được đo, không chứng nhận mã tương lai hoặc phép đo LIVE đã đạt.

## Phát hiện còn mở

### N1 — P2 — B2 D5 yêu cầu một kết quả mà lệnh B1 bắt buộc chấm đỏ

**Vị trí:** `SPEC-B2-r1.md:61`, `:95`; `SPEC-B1-r1.md:143–147`.

B2 D5 đòi các job thuộc nhóm tái dùng có kết luận `skipped` **và** `kiem-lai-tai-dung --run <id>` rc 0. B1 mục tiêu 5 bắt mọi job trong nhóm được đánh dấu tái dùng khác `success` thành `LECH_BONG`, rồi trả rc 1. B2 lại tuyên bố lệnh này thuộc B1, B2 chỉ dùng. Vì thế bất kỳ lượt B2 có tái dùng thật đều không thể đạt D5, kể cả hoạt động hoàn toàn đúng.

**Lệnh:** `python -S out/review_tools.py python out/review_r2.py contract` ⇒ rc 0 của probe; mô hình đúng câu chữ in:

```text
B1_GOAL5_LITERAL ["B2_correctly_skips", 1, ["LECH_BONG: ops gate-ops skipped"]]
B2_D5_CAN_BE_GREEN_WITH_REUSE false
```

**Hướng sửa:** tách kiểm bằng chứng nguồn khỏi kiểm kết quả thực thi của push. Chế độ bóng đòi đủ job `success`; chế độ bật đòi đúng nhóm skipped, phần còn lại thực thi đúng chính sách. Định nghĩa cách chọn chế độ có neo run/attempt/phiên bản, ca dương/âm riêng, và ghi rõ packet sở hữu sửa lệnh. C5 chạy thử trên workflow đo chỉ có bộ xét cũng cần chế độ phù hợp, không được dùng thiếu job làm một lần bóng đạt.

### N2 — P2 — Danh sách chốt vẫn thiếu ở cả B1 và B2

**Vị trí:** `SPEC-B1-r1.md:48–53`, `:148`, `:233`; `SPEC-B2-r1.md:32–39`, `:79–82`. Mã: `ops/ci_duong_nhanh_test.py:75`, `:2506`, `:2515`, `:2559`, `:2569`, `:2899`, `:2926`.

Đã cập nhật đủ các bảng mà B1 gọi tên trong bộ nhớ của probe, vẫn còn `y14` đỏ: mọi bước có tên/lệnh chứa `ci_duong_nhanh` phải có trong `RUN_BUOC_PACKET`. Hai lệnh mới của B1 đều thỏa điều kiện này. Việc B1 liệt kê y13/KHUNG_JOB không thay được bảng khóa thân `run` của y14.

Ở B2, chỉ thêm tám `if:` như mục tiêu 2 đã làm `y04` đỏ vì `Y04_IF_JOB_CHE_DO` khóa nguyên biểu thức của `gate-cong-cu`; `y06` cấm `if` ở `gate-ops`. Thêm bước gate có đúng điều kiện mà mục tiêu 3 yêu cầu làm `y03`, `y04`, `y07` đỏ vì bộ allowlist làn lưu trữ tự đưa bước mới vào tập bước phải có FAST/được liệt kê bỏ; `y14` cũng đỏ. Các chốt này không có trong kế hoạch sửa B2.

**Lệnh:** `python -S out/review_tools.py python out/review_r2.py pins` ⇒ rc 0; dùng hàm guard **thật**, chỉ thay đầu vào YAML bằng bản sao:

```text
Y_BASE: 15 guard y* được gọi đều DAT
Y_B1_AFTER_LISTED_PINS: còn y14 đỏ, thừa bien-nhan-cay và xet-tai-dung
Y_B2_JOB_IF: y04, y06, y11, y13 đỏ
Y_B2_WITH_GATE_STEP: thêm y03, y07, y12, y14 đỏ
WINDOWS_FINGERPRINT after-job-if mismatches=8
```

Không tính `y15` vào số 15: đó là self-test của loader, không hợp lệ khi mock chính loader. Lượt thử đầu đã bộc lộ giới hạn harness này; đã sửa probe và chạy lại, không báo lỗi đó thành lỗi sản phẩm.

**Hướng sửa:** bổ sung `RUN_BUOC_PACKET/y14` cho B1; bổ sung chốt và ngoại lệ hẹp cho B2, kể cả allowlist/lời khai của làn lưu trữ. Không xóa guard chung. Các tệp chứa các lỗi đã chứng minh đều đã nằm trong write set mới; chưa chứng minh bắt buộc thêm tệp thứ bảy. `ops/cong_cu_test.py:t6` còn khóa vùng trước G5: đặt bước mới sau G5 để không cần sửa tệp ngoài write set. B1 không làm đổi guard registry hay dấu vân Windows khi chỉ sửa `chuan-bi`; phần mở rộng write set Windows của B2 là đúng.

### N3 — P2 — Replay chỉ so tập nhóm nên chưa là thước đo kín cho Q8 và cho bằng chứng nguồn

**Vị trí:** `SPEC-B1-r1.md:140–147`, `:158`, `:162`; `SPEC-B2-r1.md:7–10`. Đối chiếu `docs/PROTOCOL_DA_PHIEN.md:968–993`.

Mục tiêu 5 chỉ đòi tập nhóm tính lại bằng tập nhóm đã ghi. Không yêu cầu các trường đã ghi — run/attempt nguồn, artifact ID/hash, job ID, kế hoạch, cây — bằng kết quả dựng lại tương ứng. Vì vậy bản sao evidence đổi **kế hoạch** nhưng giữ tập nhóm vẫn đạt đúng hợp đồng mục tiêu 5, dù C2 mục (5) đòi nó rc 1. Đổi source run sang một run khác mà việc tính lại chọn lại được nguồn cũ, hoặc sang nguồn khác hợp lệ cho cùng nhóm, cũng không bị phép so tập nhóm phân biệt.

Phía push còn thiếu yêu cầu kiểm đủ tập job/matrix và attempt. Câu “job nào khác success” là phép phủ định trên danh sách trả về; danh sách rỗng hoặc thiếu job không tự tạo `LECH_BONG`. Phép 4f chỉ kiểm tập job **PR nguồn**, không kiểm tập job push. HTTP/JSON đọc được nhưng trả thiếu job khác với lỗi không đọc được. Q8 lại lấy rc 0 này làm điều kiện cấp lease B2.

**Lệnh:** `python -S out/review_tools.py python out/review_r2.py contract` ⇒ rc 0; mô hình nguyên hợp đồng cho `source_run_tamper`, `plan_tamper`, `job_evidence_removed`, `push_jobs_missing` đều rc 0; thêm job `failure` mới rc 1. Hai mươi bản ghi có nhóm `ops` và inventory push rỗng đều được mô hình nhận. Đây là phản chứng về điều kiện đã viết, **không** khẳng định GitHub đã trả bộ dữ liệu ấy.

**Hướng sửa:** tái dựng trên đúng source run/attempt đã neo, so toàn bộ phần chứng minh có ý nghĩa, không chỉ verdict. Kiểm tập job push đúng và đủ theo nhóm, phân trang, run/attempt đã hoàn tất; thiếu dữ liệu ⇒ chưa đo/rc 2, tuyệt đối không pass trên tập rỗng. Định nghĩa thu lịch sử bóng đầy đủ, neo danh sách lượt và phiên bản bộ xét để tránh thay nguồn hoặc mất lượt lỗi. Đòi các đột biến C2 thực sự đổi màu bộ đo.

Bốn mốc provenance của A Q6 vẫn là nghĩa vụ. Trường `sha` “40 hex” ở 4d chỉ kiểm dạng; danh sách JSON B1:140–142 chưa chứa exact workflow-definition OID/blob/hash và bằng chứng output của từng job. Không được dùng rc 0 của replay hiện mô tả làm bằng chứng thay thế các mốc còn thiếu khi ghi `landed`.

### N4 — P2 — Chạy bóng chưa cô lập lỗi của các bước mới khỏi `chuan-bi`

**Vị trí:** `SPEC-B1-r1.md:28–29`, `:39–42`, `:109–117`, `:159`. Mã nền: `ci.yml:75–117`, `ops/ci_duong_nhanh_test.py:2961–2979`.

Đặc tả đặt `continue-on-error` rõ ràng cho lệnh tạo receipt và lệnh xét, nhưng không quy định cùng hợp đồng cho setup Python, pip và upload artifact của push. `if: always()` chỉ quyết định có chạy upload, không làm lỗi upload thành lỗi được bỏ qua. Một cấu hình làm đúng các thuộc tính liệt kê có thể làm `chuan-bi` đỏ do pip/setup/upload, kéo theo các job phụ thuộc bị ảnh hưởng trước khi bộ xét có cơ hội trả “không nhóm nào”. Điều đó trái mục tiêu chỉ chạy bóng và giữ hành vi CI khi lỗi đo.

**Lệnh:** `python -S out/review_tools.py python out/review_r2.py pins`, rồi `... runtime_and_size` ⇒ đều rc 0. Bản YAML chứng kiến là `out/thu/b1-witness.yml`: tổng timeout bước 25 < timeout job 30, không job khác đọc output bóng. Mô hình failure của các thuộc tính YAML cho `setup-python`, `PyYAML`, `upload-bien-nhan-tai-dung` kết luận job `failure`; lỗi `xet-tai-dung` mới được dung thứ. Upload receipt PR cũng cần được ràng buộc riêng để thực hiện câu “bước hỏng không làm chuan-bi đỏ”. Chưa chạy một runner GitHub thật.

PR đúng là không thêm setup Python/pip; nhưng vẫn thêm tạo receipt + upload vào `chuan-bi`, là dependency chung của các nhóm. Trong bản chứng kiến, riêng hai bước đó thêm giới hạn 2 phút trên đường chờ; **đây là giới hạn cấu hình minh họa, không phải thời gian đo thật**. Không thể suy “PR không chậm” từ việc chỉ đặt setup ở push. C5 chỉ khai đo thời gian push.

**Hướng sửa:** quy định failure/timeout/fallback cho toàn chuỗi đo và upload, cập nhật y16 để cộng đủ các bước mới, chặn output chưa hoàn tất. Thêm đột biến lỗi pip/setup/upload và đo latency PR. Nếu mục tiêu là không tăng thời gian chờ PR, cần bố trí receipt/upload ngoài đường chờ của các job nặng hoặc thay đổi rõ mục tiêu và chấp nhận số đo.

### N5 — P2 — `kiem_a.py` bỏ qua bảng trong Quyết định và không kiểm dữ liệu Bối cảnh

**Vị trí:** `SPEC-A-r3.md:103–104`, `:116–120`, `:268–297`, `:318–325`.

`doan()` loại tất cả khối `BANG` trước khi so danh sách Q. Thêm bảng chứa quy tắc ngoại lệ thứ chín vào mục Quyết định vẫn tạo cùng danh sách tám đoạn; A2 xanh. A6 chỉ kiểm tiêu đề Bối cảnh có mặt, không kiểm số đo/thời điểm/nguồn mà mục tiêu 1c yêu cầu. Bối cảnh rỗng cũng xanh.

**Lệnh:** `python -S out/review_tools.py python out/review_r2.py a_check` và `... a_write_set` ⇒ rc 0 của các probe. Script trích từ phụ lục **trùng nội dung** `tacgia/kiem_a.py`; ứng viên do reviewer tự dựng, URL trong ứng viên là giá trị giả có đúng cú pháp để thử offline, không phải duyệt thật.

```text
candidate: A2 DAT, A3 DAT, A4 DAT, A6 DAT; rc 0
table_exception: A2 DAT, A3 DAT, A4 DAT, A6 DAT; rc 0
empty_background: A2 DAT, A3 DAT, A4 DAT, A6 DAT; rc 0
adr-song / doctrine-scan: cả hai đột biến đều rc 0
A5_REAL_GIT: cả hai đột biến vẫn đúng 2 đường dẫn
```

Đã kiểm các đối chứng âm: xoá câu `Top-level path filter…` hoặc câu fallback cũ ⇒ A4 đỏ; đoạn Q thứ chín dạng văn xuôi ⇒ A2 đỏ; từng Q1–Q8 đổi hậu tố ⇒ A2 đỏ; bỏ G3/URL ⇒ A6 đỏ; đổi R sang B1 ⇒ A3 đỏ; bỏ P2/nhân đôi DONG20 ⇒ A4 đỏ. Ngắt dòng Q1 giữ xanh. Bỏ DONG20 làm `adr-song` rc 9; chép P1 vào adapter làm `doctrine-scan` rc 6. Thêm tệp thứ ba làm A5 sai. Như vậy đã xác nhận phần sửa F6 có hiệu lực, và xác định đúng phần còn hở.

**Hướng sửa:** so toàn bộ các khối của Quyết định, cấm khối ngoài tám Q thay vì lọc chúng đi. Thêm tiêu chí/đột biến cho Bối cảnh, ít nhất số đo, thời điểm và nguồn bắt buộc. Giữ cơ chế so protocol toàn văn đã sửa đúng. A8/CI của ADR giả chưa được chạy; không khai các witness đã đạt toàn bộ CI.

### N6 — P2 — Công thức Q7 làm mất tín hiệu `doc_diff` không đo được

**Vị trí:** `SPEC-B1-r1.md:133–136`, `:158`; mã `.claude/dev/ci_dang_ky_test.py:860–873`, `:889–900`.

Hàm `doc_diff` thật không ném exception cho lỗi Git: nó trả `None`. `ke_hoach(None)` trả một dictionary kế hoạch đầy đủ hợp lệ. Do đó công thức viết nguyên văn `ke_hoach(doc_diff(pr)) == ke_hoach(doc_diff(push))` trả True nếu cả hai lần đọc diff lỗi. Đến lúc so, caller không còn phân biệt “hai kế hoạch đã đo bằng nhau” với “hai fallback vì chưa đo”. Câu “nạp hay tính lỗi ⇒ loại” cần được nối với sentinel này, không thể chỉ bắt exception. C2 hiện thử nạp lỗi, chưa thử `doc_diff` trả `None`.

**Lệnh:** `python -S out/review_tools.py python out/review_r2.py q7_consumer` ⇒ rc 0; gọi **hai hàm thật**, tiêm subprocess rc 1, không viết lại thuật toán:

```text
DOC_DIFF_ERROR_SENTINEL null
PLAN_ERROR_SENTINEL_IS_VALID_DICT {... day_du, không đo được diff ...}
TWO_DIFF_ERRORS_COMPARE_EQUAL true
```

**Hướng sửa:** tách đọc hai diff; nếu bên nào `is None` thì loại riêng `nhanh`, trước khi gọi `ke_hoach`. Thêm đột biến cho một/hai diff không đo được và ca diff rỗng thật để không đồng nhất rỗng với lỗi. Nên truyền cả `manh=doc_bien_manh(env)` như registry thật: `ci.yml:1111` đặt `CI_DANG_KY_DOT_BIEN_MANH`, còn công thức hiện bỏ tham số này. Probe cũng đo được một cặp kế hoạch thực bằng nhau nhưng công thức thiếu `manh` cho khác nhau; phần sau gây từ chối tái dùng an toàn, không phải bỏ thiếu test.

### N7 — P2 — Đột biến cây của D4 không đi vào giao diện `kiem-tai-dung`

**Vị trí:** `SPEC-B2-r1.md:73–77`, `:94`.

D4 đòi sửa trường cây trong bản sao artifact thì `kiem-tai-dung` rc khác 0. Nhưng mục tiêu 3 chỉ truyền nhóm, run, attempt, cha và `github.sha`; không truyền cây kỳ vọng hoặc artifact để lệnh đọc. Lệnh tự so cây M với `merge-tree(P1,P2)` vẫn thấy hai giá trị cũ bằng nhau khi người thử chỉ sửa cây của artifact. Đột biến được nêu không tác động đến đầu vào của bộ đo.

**Lệnh:** `python -S out/review_tools.py python out/review_r2.py b2_tree_input` ⇒ rc 0; mô hình giao diện mục tiêu 3 dùng lệnh Git thật trên kho fixture:

```text
original: rc 0
artifact_tree_changed: rc 0
artifact_parents_reversed: rc 1
```

**Hướng sửa:** truyền cây kỳ vọng và neo artifact/hash vào lệnh, hoặc sửa D4 thành đột biến trên cây **commit M thực được truyền vào** và giao việc kiểm nội dung artifact cho replay có hợp đồng rõ. Không gọi phép Git trên M là đã phát hiện sửa một trường JSON mà nó không đọc.

### N8 — P3 — Hồ sơ L7 chưa đủ mã tại từng câu và payload E3/E5

**Vị trí:** `SPEC-A-r3.md:100`, `:153–155`; `SPEC-B1-r1.md:198–199`; `SPEC-B2-r1.md:112–114`, `:120–121`. Chuẩn: skill soạn spec L7 và `docs/adr/0067-...md:24–35`.

A:100 tiếp tục nói tới comment chủ kho duyệt băm nhưng không gắn E5 tại câu ấy. Những câu E5 của ba bản đã nêu loại hành động/lý do thuộc E5, nhưng chưa khai thứ mang theo khi hỏi theo bảng ADR: **diff, lý do, ai được thêm quyền gì**. E3 của B2 mang danh sách lệch và phân tích gốc rễ, còn thiếu chỉ rõ **quyết định nào** bị đảo và **hậu quả nếu giữ nguyên**. E2 lời gọi nay có mức đã dùng/finding/số xin thêm, đã sửa đúng điểm thiếu cũ; không tìm thấy ngân sách mềm hay luật “hai lượt chưa approve thì hỏi”.

**Lệnh:** `python -S out/review_tools.py python out/review_r2.py audit` ⇒ rc 0, in các câu `L7_SENTENCE`; đọc bảng ADR-0067 qua wrapper, rc 0. Đây là kiểm đối chiếu văn bản, không phải đề nghị hỏi chủ kho trong review này.

**Hướng sửa:** thêm E5 ở A:100; chuẩn hóa payload E5 chung được dẫn tại từng lần hỏi; bổ sung hai trường còn thiếu của E3. Với E1 B1:192–193, làm rõ gốc rễ/vì sao các cách đã thử hỏng bên cạnh lệnh/HTTP/phương án đã có.

### N9 — P3 — Ước 450 của B1 không còn dư cho phần phạm vi vừa bỏ sót

**Vị trí:** `SPEC-B1-r1.md:72–92`, `:184–185`; `SPEC-B2-r1.md:7–10`.

Bảng đã tốt hơn r2: cộng đúng **450**, có đối chiếu numstat và thừa nhận không có dư địa. Tuy nhiên 15 dòng cập nhật chốt chưa tính N2, hợp đồng replay chưa chứa các phép so/ca thiếu của N3 và chế độ dùng của N1. Đây vẫn là ước lượng chưa được cập nhật theo phạm vi thực, không phải chứng minh B1 chắc chắn vượt 450.

**Lệnh:** `... review_r2.py anchor`, `... runtime_and_size` ⇒ rc 0. #674: ci.yml +90, classifier +618, test +3608, registry +1. #1343: +56/+29/+133/+8 = **226** trên bốn tệp được so; khớp lời dẫn. B1 cộng 450, dư 0; B2 cộng 143, phù hợp chữ “khoảng 145”.

Phương án “chuyển `kiem-lai-tai-dung` cùng ca sang B2” chưa dùng được nguyên trạng: C5/C6 của B1 cần lệnh ấy, và điều kiện **trước cấp lease B2** cũng cần lệnh đã có để chấm toàn bộ giai đoạn bóng. Chuyển mà giữ các phụ thuộc hiện tại sẽ tạo vòng chờ.

**Hướng sửa:** ước lại sau khi chốt N1–N7, có khoản cho các chốt/ca thật. Nếu tách tiếp, đặt công cụ đo trước packet có điều kiện phụ thuộc vào nó, hoặc revision đồng bộ C5/C6/Q8/điều kiện lease. Không giảm độ phủ để vừa trần.

### N10 — P3 — `contains` không thực hiện đầy đủ lời hứa “chuỗi lạ ⇒ chạy”

**Vị trí:** `SPEC-B2-r1.md:70–72`, `:92`.

Vế `contains(..., ',ops,')` đúng là tránh khớp nhầm `ops` bên trong một tên nhóm khác. Nhưng chuỗi sai hợp đồng như `garbage,ops,garbage` hoặc `,ops,unknown,` vẫn làm `gate-ops` nghỉ. Vì vậy câu “lạ ⇒ chạy” rộng hơn phép đo, và đột biến đổi `',ops,'` thành `'ops'` chưa bao phủ sai serialization. Mức P3 vì producer B1 dự kiến chỉ phát các nhóm hợp lệ; chưa chứng minh có đường tạo dữ liệu lạ trong triển khai.

**Lệnh:** `... review_r2.py contract` ⇒ rc 0; `B2_CONTAINS` trả True cho cả hai chuỗi lạ trên, False cho rỗng và `,nhanh,`.

**Hướng sửa:** kiểm toàn bộ chuỗi/tập nhóm tại ranh giới output trước khi công bố cho job, thêm ca unknown/duplicate/malformed; hoặc giới hạn lời hứa vào loại sai mà biểu thức thật sự chặn được, cùng hợp đồng producer bảo đảm phần còn lại.

## Đối chiếu trích dẫn, lời khai mã và số đo

Đã kiểm **34 cụm neo dòng duy nhất** được liệt kê trong [citation-audit.json](citation-audit.json), có trích nguyên dòng và vị trí. Tất cả khớp nội dung được trỏ trên HEAD `45bae8d0`. Các lần dẫn lại cùng vị trí dùng cùng blob.

| Lời dẫn/khẳng định | Kết quả kiểm trên vật liệu được cấp |
|---|---|
| A:47–48, classifier `:138`, `:411` | Hằng phụ thuộc packet-loop và nhánh push luôn `chay` đúng; gọi classifier thật xác nhận PR/push hồ sơ khác nhau ở packet-loop. |
| A:52–62,69–71, protocol `:903`, `:909–910`, `:975–977`, `:1562` | T4/câu reuse/câu tree/hàng ADR-0067 đều đúng; A4 mới bao toàn bộ protocol cộng bốn thay đổi. |
| A:87, `packet_loop.py:3646` | `_kiem_ci(..., h, ...)` đọc head PR, đúng phạm vi K2 được giữ. |
| A ví dụ land pr997, §10.2.2 | Hồ sơ neo `post_merge_checks` và tách các mốc; protocol cấm suy checkout/workflow definition từ REST head. Vẫn phải thu đủ mốc khi land theo Q6. |
| B1:36, registry `:860–878`, `:889–901`; YAML `:1108–1110` | Đúng hàm/diff/đầu vào sự kiện. Hàm có sentinel `None` và tham số `manh`; N6 chỉ ra phần công thức chưa bám hết consumer. |
| B1:39, registry `:24`; setup Python/PyYAML | Import `yaml` ngay đầu đúng. Thử `python -S` không PYTHONPATH ⇒ rc 1 `ModuleNotFoundError`; thêm `RV/py-lib` ⇒ rc 0. Chứng minh phụ thuộc import, **không** chứng minh image GitHub hiện tại không cài sẵn PyYAML. |
| B1:44, `goi_that :79–96` | GET/redirect đúng; gọi hàm thật với opener giả ⇒ 200, request thứ hai không Authorization. Timeout của từng request là 120 giây; triển khai vẫn phải áp ngân sách tổng 120 giây riêng, không suy từ timeout từng request. |
| B1:48–53 và B2:32–39 | Mọi chốt được nêu có đúng vị trí. Danh sách không đầy đủ; N2. B1 nói registry “chỉ đọc output os” đúng trong phạm vi consumer cấu hình chuan-bi được dẫn, không có nghĩa toàn module chỉ có một chức năng đọc YAML. |
| B1:19 và Windows M3 | `ci_duong_nhanh_test.py` được gọi trong bước `runner.os == 'Linux'`. Phương án Windows local mới phù hợp M3; không khai đã chạy trọn các suite đó trong review spec. |
| Bảng bốn nhóm/tám job | **8 định nghĩa job, 37 instance Ubuntu**: 9 công cụ, 1 ops, 10 nhanh, 17 packet-loop. Số shard 8/8/16 khớp YAML. Thêm gate và chuan-bi là 39 instance khi chạy đủ. |
| Q4 về `if` theo ref/event | Quét YAML nền: năm bước trực tiếp theo `github.ref`/`github.event_name`, đều trong gate. Env registry phụ thuộc sự kiện là lý do phải kiểm Q7. |
| “0 cổng” | 0 marker tại đủ sáu vị trí §20 mà ADR-0054 dùng, cộng `ops/ci_duong_nhanh.py`. Đây là phép tìm tên tính năng ở nền, không phải chứng minh mọi hành vi tương đương vắng mặt. |
| Không đổi mã giữa `94cbb36` và `45bae8d0` | Diff đúng tập đường dẫn B1 nêu rỗng, rc 0. |
| Số đo lần 1: 147/79/25/44/10 và kiểm chéo 8/8 | Khớp `DE-XUAT-20261116.md`. Không có đủ dữ liệu REST/log từng PR để tự tái tính toàn bộ các số này offline; phân biệt đối chiếu tài liệu với đo lại LIVE. |
| Lần 2: 60 lượt, 28 đầy đủ xanh | Tái tính JSON: đúng 60/28, median wall 30,35 phút, runner 266,5 từ các giá trị đã làm tròn trong JSON. `do-master` ghi từ số gốc 30,4 và 266,1; spec làm tròn thành 30,4/266. Không coi khác biệt do mức làm tròn này là finding. |
| Trung vị các nhóm và hàng đợi | Từ bảng `do-master`: 146,2+0,2=146,4; 25,3; 9,2+0,3+23,6=33,1; 41,5+0,2=41,7; queue 2/878/123 khớp. Không có dữ liệu job thô để tái tính percentile độc lập. |
| Lease, 366/367 nhánh máy chủ, số ADR chưa ai chiếm | Chỉ là số đo có thời điểm do tác giả cung cấp. Không truy cập `D:/tlscan.git` hay mạng; không xác minh lại lease/server hiện tại. Điều kiện yêu cầu quét lại trước cấp lease phải giữ. |

## Kiểm L1–L7

| Luật | A r3 | B1 r1 | B2 r1 |
|---|---|---|---|
| L1 — đơn vị đếm | Tám Q, bốn thay đổi, hai tệp rõ. | Bốn nhóm, shard và 450 **dòng thêm** rõ; tám job là định nghĩa, không phải instance. | Sáu tệp, tám job, 20 lượt bóng và 10 lượt canary rõ. |
| L2 — mục tiêu/write set | Hai đường dẫn đủ cho thay đổi văn bản. | Tệp đủ cho phần đã đo, nhưng danh sách sửa chốt thiếu N2. | Sáu tệp đã bao phủ Windows/registry cũ; N2 và N1 đòi sửa mục tiêu trong các tệp đã có. |
| L3 — phép đo đỏ | A4 và các mutant cũ đã có răng; A2/A6 còn hở N5. | C2 có đột biến riêng nhưng mục tiêu 5 không đủ để làm các mutant evidence đỏ, N3; lỗi setup/upload chưa thử, N4. | D5 mâu thuẫn N1, mutant tree D4 không đi vào input N7. |
| L4 — kế thừa | Có `khong_ap_dung`; không có hồ sơ packet đã land cần kế thừa bộ đếm được cung cấp. | Có `khong_ap_dung`, ghi lớp lỗi cũ. Việc sửa draft sau review không tự biến thành packet khắc phục đã land. | Tương tự B1. |
| L5 — thời điểm/đo lại | Neo mã và số đo có ngày; số server tương lai chưa đo được. | Số tham chiếu đo lại khớp; kích thước cần ước lại N9. | Mốc sau B1/#1448 được khai sẽ đo lại; 145 là ước, không phải numstat ứng viên. |
| L6 — thước đo chuỗi | Có bảng năm vế và đo thử; N5 vẫn là witness xanh giả. | N/N/marker có mô tả; marker chưa cứu được hợp đồng hậu kiểm N3. | N/N/marker có mô tả; N1/N7/N10 còn sai phạm vi đo. |
| L7 — điểm hỏi | E2 đã có payload; A:100/E5 còn N8. | Không có ngân sách mềm; E1/E2 có phần lớn payload, E5 cần N8. | E3/E5 cần N8; thiếu phụ thuộc/chờ lease là điều kiện thi hành, không tự tạo câu hỏi chủ kho. |

Không yêu cầu hỏi chủ kho ở lượt review này. Những câu dẫn §12/ADR-0037 là dẫn điểm dừng sẵn có; không coi chúng là một ngưỡng hỏi mới.

## Bảng lệnh đã chạy

Các lệnh kiểm có ý nghĩa và mọi rc (kể cả lỗi harness/đường dẫn) được giữ trong bảng tự sinh dưới đây. `RV = C:\r\d2`; `REPO = C:\r\d2\cay-kho`. Wrapper luôn được gọi từ RV; cột cwd là nơi lệnh con thực thi. Lệnh `read` chỉ đọc, `rg` mặc định loại `.codex`. Các lệnh Git dựng fixture/`kiem_a.py`/gate con được in hoặc mô tả trong probe và có đầu vào lưu tại `out/thu`.

<!-- COMMAND_TABLE_BEGIN -->
| # | Lệnh (gọi từ RV) | cwd lệnh con | rc | Kết luận và output |
|---|---|---|---|---|
| 1 | <code>python -S out/review_tools.py 'hash' 'SPEC-A-r3.md' 'SPEC-B1-r1.md' 'SPEC-B2-r1.md'</code> | RV | 0 | Neo SHA-256 ba đặc tả. [log](review-evidence/20261120T105051287753.txt) |
| 2 | <code>python -S out/review_tools.py 'git' 'rev-parse' 'HEAD' 'HEAD^{tree}' 'origin/master'</code> | REPO | 0 | HEAD/tree/ref cục bộ. [log](review-evidence/20261120T105052043921.txt) |
| 3 | <code>python -S out/review_tools.py 'read' 'cay-kho/.github/workflows/ci.yml@1:165' 'cay-kho/ops/ci_provenance.py@1:110' 'cay-kho/.claude/dev/ci_dang_ky_test.py@560:680' 'cay-kho/.claude/dev/ci_dang_ky_test.py@820:940'</code> | RV | 0 | Đọc/tìm/đối chiếu dữ liệu cục bộ. [log](review-evidence/20261120T105052539061.txt) |
| 4 | <code>python -S out/review_tools.py 'read' 'cay-kho/ops/ci_duong_nhanh_test.py@2440:2515' 'cay-kho/ops/ci_duong_nhanh_test.py@2590:2735' 'cay-kho/ops/ci_duong_nhanh_test.py@2830:3020'</code> | RV | 0 | Đọc/tìm/đối chiếu dữ liệu cục bộ. [log](review-evidence/20261120T105056216984.txt) |
| 5 | <code>python -S out/review_tools.py 'rg' 'chuan-bi&#124;timeout-minutes&#124;setup-python&#124;PHU_THUOC&#124;ci_provenance&#124;importlib&#124;KHUNG_BUOC' '.claude/dev/ci_dang_ky_test.py' 'ops/ci_duong_nhanh_test.py' 'ops/ci_duong_nhanh.py'</code> | REPO | 0 | Đọc/tìm/đối chiếu dữ liệu cục bộ. [log](review-evidence/20261120T105058048456.txt) |
| 6 | <code>python -S out/review_tools.py 'read' 'cay-kho/ops/ci_duong_nhanh_test.py@1:100' 'cay-kho/ops/ci_duong_nhanh_test.py@2450:2485' 'cay-kho/ops/ci_duong_nhanh_test.py@2740:2790' 'cay-kho/ops/ci_duong_nhanh_test.py@2875:2897' 'cay-kho/ops/ci_duong_nhanh_test.py@2960:3005' 'cay-kho/.claude/dev/ci_dang_ky_test.py@575:665' 'cay-kho/.claude/dev/ci_dang_ky_test.py@850:905'</code> | RV | 0 | Đọc/tìm/đối chiếu dữ liệu cục bộ. [log](review-evidence/20261120T105141145436.txt) |
| 7 | <code>python -S out/review_tools.py 'rg' 'def y04&#124;def y06&#124;def doc_yml&#124;def doc_ci&#124;def bang&#124;def k03&#124;^if __name__' 'ops/ci_duong_nhanh_test.py'</code> | REPO | 0 | Đọc/tìm/đối chiếu dữ liệu cục bộ. [log](review-evidence/20261120T105145013161.txt) |
| 8 | <code>python -S out/review_tools.py 'rg' 'chuan-bi&#124;BAM_GATE_REGISTRY&#124;gate-packet-loop-manh' '--files-with-matches' '.github/checks' '.claude/dev' 'ops' '-g' '*.py' '-g' '*.ps1' '-g' '!packet_loop_test.py'</code> | REPO | 0 | Đọc/tìm/đối chiếu dữ liệu cục bộ. [log](review-evidence/20261120T105145723713.txt) |
| 9 | <code>python -S out/review_tools.py 'python' 'out/review_r2.py' 'anchor'</code> | RV | 0 | Băm/HEAD/ADR land/numstat/số đo nền. [log](review-evidence/20261120T153415701751.txt) |
| 10 | <code>python -S out/review_tools.py 'python' 'out/review_r2.py' 'a_check'</code> | RV | 0 | Lượt đầu có mutant xoá câu không tác động; đã sửa bằng neo thật và chạy lại. Chỉ dùng lượt sau cho phép xoá câu. [log](review-evidence/20261120T153430722977.txt) |
| 11 | <code>python -S out/review_tools.py 'python' 'out/review_r2.py' 'pins'</code> | RV | 0 | Guard thật trên YAML chứng kiến; N2. Lượt đầu mock loader làm y15 không hợp lệ; bỏ tự kiểm đó khỏi probe, chạy lại 15 guard. [log](review-evidence/20261120T153417767037.txt) |
| 12 | <code>python -S out/review_tools.py 'python' 'out/review_r2.py' 'rename'</code> | RV | 0 | F1: fixture Git cũ và before=P1; nhanh bị loại. [log](review-evidence/20261120T153421399683.txt) |
| 13 | <code>python -S out/review_tools.py 'python' 'out/review_r2.py' 'contract'</code> | RV | 0 | Mô hình hợp đồng; N1/N3/N10 và phần sửa F4. [log](review-evidence/20261120T153418914833.txt) |
| 14 | <code>python -S out/review_tools.py 'read' 'cay-kho/ops/ci_duong_nhanh_test.py@2490:2580' 'cay-kho/ops/ci_duong_nhanh_test.py@2894:2960' 'cay-kho/ops/cong_cu_test.py@1:70' 'cay-kho/docs/adr/0067-danh-sach-dong-va-uy-quyen-thuong-truc.md@1:145' 'cay-kho/docs/PROTOCOL_DA_PHIEN.md@900:915'</code> | RV | 0 | Đọc/tìm/đối chiếu dữ liệu cục bộ. [log](review-evidence/20261120T153457770271.txt) |
| 15 | <code>python -S out/review_tools.py 'rg' 'chuan-bi&#124;ci_duong_nhanh&#124;ci_provenance&#124;ci_dang_ky_test' '.github/checks/ci_phamvi.py' '.github/checks/ci_phamvi_test.py' 'ops/cong_cu_test.py'</code> | REPO | 0 | Đọc/tìm/đối chiếu dữ liệu cục bộ. [log](review-evidence/20261120T153459796647.txt) |
| 16 | <code>python -S out/review_tools.py 'rg' 'ci_provenance.py&#124;ci_duong_nhanh.py&#124;ci_dang_ky_test.py' '.claude/dev/ci_dang_ky_test.py' 'ops/ci_duong_nhanh.py'</code> | REPO | 0 | Đọc/tìm/đối chiếu dữ liệu cục bộ. [log](review-evidence/20261120T153500176993.txt) |
| 17 | <code>python -S out/review_tools.py 'read' 'bang-chung/master-runs-20261120.json@1:12'</code> | RV | 0 | Đọc/tìm/đối chiếu dữ liệu cục bộ. [log](review-evidence/20261120T153500365062.txt) |
| 18 | <code>python -S out/review_tools.py 'read' 'cay-kho/docs/adr/0067-danh-sach-dong-va-uy-quyen-thuong-truc.md@12:57' 'cay-kho/ops/ci_duong_nhanh_test.py@2925:2936' 'cay-kho/ops/cong_cu_test.py@335:390'</code> | RV | 0 | Đọc/tìm/đối chiếu dữ liệu cục bộ. [log](review-evidence/20261120T153518796172.txt) |
| 19 | <code>python -S out/review_tools.py 'rg' 'head_sha&#124;run_attempt&#124;filter=latest&#124;before&#124;ImageVersion&#124;workflow.definition&#124;workflow definition' 'SPEC-NONEXISTENT'</code> | REPO | 2 | Lỗi đường dẫn của reviewer; đã tìm lại trên ../SPEC-B1/B2 đúng. Không dùng làm finding. [log](review-evidence/20261120T153519673549.txt) |
| 20 | <code>python -S out/review_tools.py 'python' 'out/review_probes.py' 'policy_probe'</code> | RV | 0 | F5: push hồ sơ vẫn làn nhanh, packet-loop chay; sáu cổng. [log](review-evidence/20261120T153707946741.txt) |
| 21 | <code>python -S out/review_tools.py 'python' 'out/review_r2.py' 'pins'</code> | RV | 0 | Guard thật trên YAML chứng kiến; N2. [log](review-evidence/20261120T153708028843.txt) |
| 22 | <code>python -S out/review_tools.py 'python' 'out/review_r2.py' 'audit'</code> | RV | 0 | Neo tệp:dòng, Q4, 0 cổng, import PyYAML, câu L7. [log](review-evidence/20261120T153709971500.txt) |
| 23 | <code>python -S out/review_tools.py 'python' 'out/review_probes.py' 'inventory'</code> | RV | 0 | YAML/job/matrix/Windows/guard inventory. [log](review-evidence/20261120T153708629840.txt) |
| 24 | <code>python -S out/review_tools.py 'python' 'out/review_r2.py' 'a_check'</code> | RV | 0 | A: ứng viên/đột biến và hai gate thật; N5. [log](review-evidence/20261120T153722713893.txt) |
| 25 | <code>python -S out/review_tools.py 'rg' 'head_sha&#124;run_attempt&#124;filter=latest&#124;before&#124;ImageVersion' '../SPEC-B1-r1.md' '../SPEC-B2-r1.md'</code> | REPO | 0 | Đọc/tìm/đối chiếu dữ liệu cục bộ. [log](review-evidence/20261120T153709613556.txt) |
| 26 | <code>python -S out/review_tools.py 'python' 'out/review_r2.py' 'q7_consumer'</code> | RV | 0 | Hàm thật trả None rồi kế hoạch bằng nhau; N6. [log](review-evidence/20261120T153710922307.txt) |
| 27 | <code>python -S out/review_tools.py 'read' 'bang-chung/do-master-20261120.txt'</code> | RV | 0 | Đọc/tìm/đối chiếu dữ liệu cục bộ. [log](review-evidence/20261120T153711100764.txt) |
| 28 | <code>python -S out/review_tools.py 'read' 'SPEC-A-r3.md@65:125' 'SPEC-A-r3.md@140:156' 'SPEC-B1-r1.md@105:151' 'SPEC-B2-r1.md@68:95' 'cay-kho/docs/PROTOCOL_DA_PHIEN.md@961:995'</code> | RV | 0 | Đọc/tìm/đối chiếu dữ liệu cục bộ. [log](review-evidence/20261120T153829692292.txt) |
| 29 | <code>python -S out/review_tools.py 'python' 'out/review_r2.py' 'runtime_and_size'</code> | RV | 1 | Lỗi chữ ký opener GIẢ của probe; sửa và chạy lại rc 0, không phải lỗi sản phẩm; không mạng. [log](review-evidence/20261120T153830675342.txt) |
| 30 | <code>python -S out/review_tools.py 'git' 'status' '--porcelain'</code> | REPO | 0 | Working tree cay-kho sạch. [log](review-evidence/20261120T153830583270.txt) |
| 31 | <code>python -S out/review_tools.py 'python' 'out/review_probes.py' 'b5_probe'</code> | RV | 0 | Fixture F7 cũ: diff PR/push khác nhau. [log](review-evidence/20261120T153832906555.txt) |
| 32 | <code>python -S out/review_tools.py 'python' 'out/review_r2.py' 'runtime_and_size'</code> | RV | 0 | Mô hình lỗi chuỗi bóng, kích thước; goi_that với opener giả. [log](review-evidence/20261120T153927272751.txt) |
| 33 | <code>python -S out/review_tools.py 'python' 'out/review_r2.py' 'b2_tree_input'</code> | RV | 0 | Git thật + giao diện mô hình: đổi cây artifact không đổi rc; N7. [log](review-evidence/20261120T153928196907.txt) |
| 34 | <code>python -S out/review_tools.py 'read' 'cay-kho/ops/ci_provenance.py@79:96' 'cay-kho/docs/adr/0053-tran-kich-thuoc-sensitive-len-sau-tep.md@15:55' 'cay-kho/docs/adr/0060-dieu-kien-merge-va-moc-ready.md@22:60'</code> | RV | 0 | Đọc/tìm/đối chiếu dữ liệu cục bộ. [log](review-evidence/20261120T153928318538.txt) |
| 35 | <code>python -S out/review_tools.py 'python' 'out/review_r2.py' 'a_write_set'</code> | RV | 0 | A5: Git diff đúng hai tệp; thêm tệp thứ ba thành ba. [log](review-evidence/20261120T154032371490.txt) |
| 36 | <code>python -S out/review_tools.py 'read' 'cay-kho/ops/land/pr997-wp978-land-evidence.yaml@1:70' 'cay-kho/.claude/dev/chay-cong-windows_test.ps1@1403:1425'</code> | RV | 0 | Đọc/tìm/đối chiếu dữ liệu cục bộ. [log](review-evidence/20261120T154033014015.txt) |
| 37 | <code>python -S out/review_tools.py 'git' 'status' '--porcelain'</code> | REPO | 0 | Working tree cay-kho sạch. [log](review-evidence/20261120T154545734464.txt) |
| 38 | <code>python -S out/review_tools.py 'python' 'out/review_r2.py' 'audit'</code> | RV | 0 | Neo tệp:dòng, Q4, 0 cổng, import PyYAML, câu L7. [log](review-evidence/20261120T154547862642.txt) |
| 39 | <code>python -S out/review_tools.py 'hash' 'SPEC-A-r3.md' 'SPEC-B1-r1.md' 'SPEC-B2-r1.md'</code> | RV | 0 | Neo SHA-256 ba đặc tả. [log](review-evidence/20261120T154546174791.txt) |
| 40 | <code>python -S out/review_tools.py 'python' 'out/review_r2.py' 'f7_closure'</code> | RV | 0 | Chạy lại fixture F7 với hàm kế hoạch mới. [log](review-evidence/20261120T154552877414.txt) |
<!-- COMMAND_TABLE_END -->

Trước khi dựng wrapper, đã đọc `PROMPT.md`, ba spec, verdict cũ, skill soạn spec, script lượt 1 và vật liệu tác giả bằng `Get-Content`; dùng `rg --files` giới hạn trong RV và loại `.codex` để kiểm kê. Các lệnh này rc 0. Chỉ tạo thư mục/copy script vào `out/`; các lần chỉnh sửa dùng `apply_patch` trong `out/`. Phần đọc đầu có output bị cắt đã được đọc lại theo vùng cần kiểm; không lấy phần bị cắt làm bằng chứng.

## Giới hạn và kết luận

Chưa chạy CI thật, actionlint trên ứng viên B1/B2 chưa tồn tại, toàn suite Windows M3, tải artifact giữa hai lượt bằng token thật, hay canary sau land. Không đo lại server/lease/runner image hoặc đọc nguồn ngoài RV. Các mục đó vẫn **chưa đo được**, không ghi thành đạt.

F1 đã có bằng chứng đóng đúng phản chứng cũ; việc chia A/B1/B2 và sửa A4 là tiến bộ có thể kiểm. Tuy nhiên N1–N7 còn mở ở mức P2: hậu kiểm B2 mâu thuẫn, các chốt bị bỏ sót, Q8/bằng chứng chưa được kiểm kín, lỗi chạy bóng chưa cô lập, thước đo A còn lọt, sentinel Q7 và đột biến cây D4. Cần revision ba đặc tả và chạy lại các phép phản chứng tương ứng trước khi approve.

KET_LUAN: changes_requested
