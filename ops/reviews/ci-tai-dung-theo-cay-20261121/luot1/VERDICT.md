# Review đặc tả lượt 1 — CI-TAI-DUNG-THEO-CAY A/B r2

**Kết luận: `changes_requested`.** Có **1 P1, 6 P2 và 3 P3** mở; không có P0. Chưa nên duyệt băm hai bản r2.

Đây là review đặc tả độc lập, không phải triển khai B hay chứng nhận CI đã chạy. Reviewer: Codex, họ model OpenAI, dùng công cụ shell cục bộ qua phiên API; không có chứng thực độc lập về model phục vụ. Thẩm quyền của lượt này là `PROMPT.md` do người dùng yêu cầu thực hiện. Không dùng mạng, không đọc memory hoặc thư mục `.codex`, không sửa `cay-kho/`; toàn bộ script, bản sao, kho Git phản chứng và kết quả mới nằm dưới `out/`.

## Neo và môi trường đã kiểm

| Đối tượng | Giá trị |
|---|---|
| `SPEC-A-r2.md`, SHA-256 | `3d878fedfcbe04d58558b0ae5eb8ba15a68b2f3e5a46ef3bf3bdd6e7aa6c99b3` |
| `SPEC-B-r2.md`, SHA-256 | `587e59cf83b5db6f0289d999ab50e9fbce4abd13f454c188bbc8c4b9b6fc76fe` |
| `cay-kho` HEAD được review | `45bae8d07a8cdf06a1ca9a7a2e015a6258169379` |
| Tree của HEAD | `30d5c7dec30dc658ae04ef29a6ffafe94eb8f197` |
| SHA-256 A r1 | `b20b6081802e29aa9bd01a3de48c9a5fab03af66df3ad2700df14b66bb2a33a5` — khớp lời dẫn |
| SHA-256 B r1 | `57ccbf1d65f9ccf7061e732222d9d11cae6704e69aee06251de9e98dfce34b75` — khớp lời dẫn |
| Git history | `--is-shallow-repository=false`; `status --porcelain` rỗng |
| Môi trường kiểm | Windows, PowerShell, Python 3.13; PyYAML **6.0.3** từ `RV/py-lib`, không dùng user site-packages |
| Ngày đo | 20-11-2026; thời điểm UTC từng lệnh nằm trong `review-evidence/commands.jsonl` |

Ref cục bộ `origin/master` thực tế trỏ `a31c680c8880786848f832a35554d9e84078b270`, khác HEAD được đóng gói. Review này neo **HEAD 45bae8d0**, không đổi nền sang ref ấy. Đã đối chiếu: các tệp mã/protocol chính được review không đổi giữa hai mốc này. Không fetch và không xác nhận tình trạng máy chủ.

Ba phép đo OID land cho ADR-0053 và ADR-0055 đều đúng trên lịch sử cung cấp: tệp tồn tại tại L (`rc=0`), chưa có tại L^1 (`rc=128`), L thuộc first-parent của HEAD được review. Dòng khai chọn trần của hai đặc tả hợp lệ: sensitive tối đa **6 tệp / 450 dòng thêm**; trần lời gọi theo ADR-0055. Đây không phải xác nhận lease hay authority tương lai.

Script tái lập: [review_tools.py](review_tools.py), [review_probes.py](review_probes.py). Mọi lệnh `python -S out/review_tools.py ...` dưới đây được gọi từ `C:\r\d2`; wrapper đặt `PYTHONPATH=C:\r\d2\py-lib`, tắt bytecode và giữ TEMP/TMP trong `out/thu`. Git dùng cấu hình riêng của tiến trình, không sửa cấu hình người dùng.

## Phát hiện

### F1 — P1 — Q7 so nhầm tập diff, có thể bỏ vòng đột biến mà push phải chạy

**Vị trí:** `SPEC-B-r2.md:95`, `:113`, `:187`; `SPEC-A-r2.md:109`. Mã liên quan: `cay-kho/ops/ci_duong_nhanh.py:166`, `:213`, `:272`; `cay-kho/.claude/dev/ci_dang_ky_test.py:860`, `:889`; `cay-kho/.github/workflows/ci.yml:1108`.

B lưu `tep_doi` của **bộ phân loại**, rồi so tập ấy giữa PR và push. Nhưng registry không dùng tập đó: bộ phân loại PR lấy hợp của ba diff; registry lấy riêng `base...head`. Ngoài ra push dùng `github.event.before`, **không luôn bằng M^1** như lời mô tả ở B:187. B không yêu cầu `before == P1`.

Phản chứng Git thật: O có `docs/f.py`; P1 đổi tên thành `scripts/f.py`; P2 từ O sửa nội dung ở tên cũ. Synthetic PR và M có đúng `[P1,P2]`, cùng cây, khớp `merge-tree`. Push đưa cả P1 và M từ O lên master, nên `before=O`. Không có điều kiện nào ở B loại push nhiều commit này.

Lệnh: `python -S out/review_tools.py python out/review_probes.py diff_probe` ⇒ **rc 0**, xác nhận phản chứng:

```text
Q2 True RECOMPUTED_TREE True
CLASSIFIER_PR   ['docs/f.py', 'scripts/f.py']
CLASSIFIER_PUSH ['docs/f.py', 'scripts/f.py'] B_3F_ACCEPTS True
REGISTRY_PR     ['docs/f.py']
REGISTRY_PUSH   ['docs/f.py', 'scripts/f.py'] ACTUAL_Q7 False
pretooluse_guard_test: PR = nhe; push = day_du
```

[Output đầy đủ](review-evidence/20261120T102441667529.txt). Đã chạy các hàm diff và lập kế hoạch **hiện hữu**, không giả lập phép tính tập tệp. Chưa chạy CI đầu-cuối của fixture. Hệ quả thiết kế: nếu lượt PR xanh ở chế độ nhẹ và đủ số job, mọi điều kiện tái dùng B vẫn cho qua dù vòng đột biến mà push yêu cầu chưa chạy.

**Hướng sửa:** biên nhận phải ghi đúng đầu vào/tập diff hoặc kế hoạch thực thi của **consumer registry**, có base/head/before và định danh thuật toán. So với chính kế hoạch registry của push. Nếu bản đầu chỉ hỗ trợ push một merge, ghi và kiểm thêm `event.before == M^1`; điều đó không thay việc đối chiếu đúng consumer. Thêm ca rename + push nhiều commit và đột biến bỏ chốt, yêu cầu loại riêng nhóm `nhanh`.

### F2 — P2 — Thiếu các chốt phải cập nhật; write set và yêu cầu “giữ nguyên mọi chốt khác” không kham thay đổi

**Vị trí:** `SPEC-B-r2.md:53`, `:67`, `:132`. Mã: `cay-kho/.claude/dev/ci_dang_ky_test.py:836`, `:840`, `:922`, `:930`, `:1431`, `:1492`; `cay-kho/.claude/dev/chay-cong-windows_test.ps1:1289`, `:1343`, `:1409`.

Ngoài các chốt B liệt kê, còn `BAM_GATE_REGISTRY`, `BAM_GATE_NHANH`, `G5_GOP_IF`. Chỉ thêm đúng tám điều kiện cấp job theo mục tiêu 5 đã làm các chốt này đỏ. Mục tiêu 8 lại yêu cầu giữ nguyên mọi chốt khác. Một consumer nữa là dấu vân toàn bộ job trong `chay-cong-windows_test.ps1`, **ngoài write set**. Bước mới ở `gate` còn phải được rà với gương Windows.

Lệnh: `python -S out/review_tools.py python out/review_probes.py pins` ⇒ **rc 0**; [output](review-evidence/20261120T094758776494.txt):

```text
loi_gate_nhanh BASELINE []
loi_gate_nhanh AFTER_B_OBJECTIVE_5 ['hai job mảnh/gom nhanh_don_duoc lệch cấu hình ghim']
loi_vung_thiet_lap BASELINE []
loi_vung_thiet_lap AFTER_B_OBJECTIVE_5 ['gate-registry đổi ... cập nhật BAM_GATE_REGISTRY']
loi_g5_workflow: có lỗi G5_GOP_IF ở gate-cong-cu-gop
WINDOWS_FINGERPRINT before mismatches=0
WINDOWS_FINGERPRINT after-job-if mismatches=8
```

Đã gọi các hàm guard Python thật và trích chạy **nguyên văn bộ tính dấu vân** `Doc-DauVanCi`; không khai đã chạy trọn suite PowerShell. Theo consumer ở `:1409–1412`, các lệch dấu vân làm t32 đỏ. Việc bộ này không được gọi trực tiếp trong `ci.yml` không làm mất hồi quy của test/gương Windows.

**Hướng sửa:** bổ sung consumer bị bỏ sót vào đặc tả và write set trước khi cấp lease, theo L2; cho phép cập nhật đúng các giá trị ghim sau khi rà hành vi. Rà gương Windows của bước `kiem-tai-dung` rồi quyết định có cần thêm cả `chay-cong-windows.ps1` hay không. Không để executor phát hiện rồi dừng theo B:160; lớp lỗi này đã đo được ngay trong review spec.

### F3 — P2 — B1 đòi bằng chứng Windows từ một bước luôn bị bỏ trên Windows

**Vị trí:** `SPEC-B-r2.md:14`, `:139`; `cay-kho/.github/workflows/ci.yml:760`; `cay-kho/ops/ci_duong_nhanh_test.py:2783`.

`workflow_dispatch windows-only` không chạy `ops/ci_duong_nhanh_test.py`: bước duy nhất gọi nó có `if: runner.os == 'Linux'`. B chỉ thêm điều kiện cấp job, chưa có mục tiêu bật hoặc tạo một bước kiểm Windows cho suite này. Job Windows xanh không cung cấp dòng tổng của test bị skipped.

Lệnh: `python -S out/review_tools.py python out/review_probes.py inventory` ⇒ **rc 0**; [output](review-evidence/20261120T094757109434.txt):

```text
B1_WINDOWS_STEP ... "if": "runner.os == 'Linux'" ...
"run": "python ops/ci_duong_nhanh_test.py"
```

**Hướng sửa:** chỉ rõ lane Windows thực sự chạy suite/nhóm ca cần thiết, điều chỉnh `if:` và các ảnh chụp tương ứng trong write set; đòi step/job ID, kết quả thực thi và marker dương trên exact head. Phân biệt bằng chứng này với Windows local theo ADR-0060 M3; không nhận job xanh có bước bị skipped.

### F4 — P2 — Biên nhận của `chuan-bi` chưa chứng minh identity của những job được tái dùng

**Vị trí:** `SPEC-B-r2.md:93`, `:107`, `:110`, `:123`, `:185`; `SPEC-A-r2.md:100`, `:106`. Đối chiếu protocol `:968–983`, `:991–993`.

`image_os/image_version` lấy ở **runner của chuan-bi**; điều kiện 3e chỉ đếm job Ubuntu và xét conclusion. Không có phép đo image/runtime của từng job nặng. Do đó trường hợp PR `chuan-bi=V1`, job nặng `V2`, push `chuan-bi=V1` vẫn đạt các điều kiện đã viết, dù không thoả Q3. Một tên `ubuntu-latest` không cung cấp ImageVersion.

Đặc tả cũng chủ ý không so `run_attempt` của artefact; chưa đóng hợp đồng nối receipt → attempt → từng job khi rerun một phần. Chưa kiểm `sha`/`phien_ban` đã ghi trong receipt, và chưa xác định bằng chứng workflow-definition tương ứng. Q6 vẫn giữ bốn mốc provenance; tree/parents của một job không tự điền các mốc của job khác. Riêng mục tiêu 6 yêu cầu in `attempt=<n>` nhưng danh sách đầu vào **không truyền `tai_dung_attempt`**; `GITHUB_RUN_ATTEMPT` của push là identity khác.

Lệnh: `python -S out/review_tools.py python out/review_probes.py contract_probe` ⇒ **rc 0**; [output](review-evidence/20261120T101602085345.txt): mô hình đúng các predicate ghi ở B3c/e vẫn chấp nhận receipt attempt 1 với run attempt 2, schema lạ và bộ job nặng V2 khi receipt/push V1. Mô hình còn cho thấy “8 job success” không tự chứng minh tập chỉ số 0–7 nếu có tên lặp. **Đây là phản chứng hợp đồng đặc tả, không phải tuyên bố đã quan sát API GitHub trả dữ liệu ấy.**

**Hướng sửa:** định nghĩa identity bằng chứng cho từng nhóm/job, gắn artifact ID/hash, checkout SHA/tree, workflow identity, attempt và runtime đã đo. Hoặc chưa hỗ trợ partial rerun thì từ chối nó rõ ràng cho bản đầu. So tập job/matrix mong đợi, không chỉ tổng số. Truyền `tai_dung_attempt` sang `gate`; thêm đột biến đúng các ràng buộc mới. Nếu chỉ định so image của coordinator thì phải đổi Q3 thành đúng mức bảo đảm đó và khai giới hạn.

### F5 — P2 — Phạm vi ngoại lệ của A chưa thống nhất với luật hiện hữu và hành vi nền

**Vị trí:** `SPEC-A-r2.md:103`, `:105`, `:115`, `:120`, `:126`; `cay-kho/docs/PROTOCOL_DA_PHIEN.md:903`; `SPEC-B-r2.md:88`, `:101`.

Hai câu nối P1/P2 xử lý SHA/tree, nhưng hàng **T4** còn ghi “reuse duy nhất evidence T3 khi toàn bộ exact identity khớp”. Q1/Q6 mới cho lấy nhóm từ PR `day_du`, không đòi đó là T3; A không cho sửa hàng T4 và A6 coi hunk ấy ngoài phạm vi. Người thi hành hiện phải tự quyết ngoại lệ có thay cả điều kiện nguồn T3 hay không. Cần định tuyến rõ thay vì để hai mô tả gate canonical khác nhau.

Ngoài ra câu R khẳng định trước B “push lên master chạy đủ như cũ” là sai trên nền. Q4 “gate vẫn chạy đủ” và Q5 “thiếu biên nhận ... push chạy đủ” cũng chưa giới hạn vào nhánh xét tái dùng `che_do=day_du`, trong khi B giữ nguyên làn nhanh hiện hữu. Một push hồ sơ thiếu receipt vẫn đi `duong_nhanh`, chỉ packet-loop luôn chạy.

Lệnh: `python -S out/review_tools.py python out/review_probes.py policy_probe` ⇒ **rc 0**; [output](review-evidence/20261120T102034888989.txt). Merge hai cha chỉ đổi hồ sơ được mã nền phân loại:

```text
che_do=duong_nhanh
packet_loop=chay
```

Output cũng in nguyên hàng T4 và các mốc identity. Đây là lời khai nền sai, không phải đề xuất xoá làn nhanh.

**Hướng sửa:** giới hạn Q4/Q5 vào lượt đang xét tái dùng ở làn đầy đủ; sửa R thành “chưa áp dụng ngoại lệ tái dùng, giữ bộ phân loại hiện hành”. Ghi rõ ngoại lệ PR theo nhóm đối với T4, cập nhật phạm vi sửa/A6 nếu cần. Q3 là fallback theo nhóm; Q5 nên nói rõ các lỗi chung làm rỗng toàn bộ tập để tránh cách hiểu xoá khả năng tái dùng từng phần.

### F6 — P2 — A4/A6 không bảo vệ “không sửa câu nào khác”; một số mục tiêu ADR không có tiêu chí đo

**Vị trí:** `SPEC-A-r2.md:87–118`, `:126`, `:137–142`; luật L3/L6 và bảng đầu ra trong `cay-kho/.claude/skills/soan-spec/SKILL.md`.

A6 chỉ khoanh **vùng hunk**, không kiểm nội dung phần cũ trong vùng. Có thể xoá câu bắt fallback full ở đầu đoạn §10.1, giữ nguyên câu reuse/P1 và tree/P2: A4 vẫn xanh, A5 vẫn hai tệp, mọi hunk vẫn nằm trong ba vùng A6 cho phép. Điều này vi phạm trực tiếp mục tiêu 2d.

Lệnh:

- `python -S out/review_tools.py python out/review_probes.py a_probes` ⇒ **rc 0**, `A4_AFTER_DELETE_OTHER_SENTENCE True True`.
- `python -S out/review_tools.py python out/review_probes.py a6_git_probe` ⇒ **rc 0**, diff Git thật: protocol `+4/-5`, ADR `+23/-0`, đúng hai đường dẫn; các hunk cũ ở `906`, `910`, `977`, `1562` — đều trong vùng cho phép. [Output](review-evidence/20261120T102354190987.txt).

Một ADR tối thiểu chỉ có trạng thái Accepted, Q1–Q7 và R cũng qua `adr-song`, các phép khớp A2/A3 và `doctrine-scan`, dù thiếu **Bối cảnh, Giới hạn, Cưỡng chế**, URL duyệt và lời khai hiệu lực trên dòng trạng thái. Thêm một đoạn ngoại lệ thứ tám vẫn giữ bảy phép khớp A2 xanh. [Output phép thử A](review-evidence/20261120T102042424479.txt). Không khẳng định đã chạy A8/CI cho ADR giả; điểm thiếu là các tiêu chí tường minh không đo những mục tiêu đó.

**Hướng sửa:** chuẩn hoá rồi so toàn bộ protocol với phép biến đổi chỉ chèn P1, P2 và đúng một hàng mới, hoặc chứng minh nội dung cũ nguyên vẹn ngoài ba phép chèn. Khoá chính xác bảy đoạn Quyết định và cấm câu ngoại lệ bổ sung. Thêm tiêu chí và đột biến cho các mục tiêu ADR còn thiếu, đặc biệt Giới hạn/Cưỡng chế và ngày hiệu lực.

### F7 — P3 — B5 chưa nêu đủ điều kiện để vế dương phải tái dùng cả bốn nhóm

**Vị trí:** `SPEC-B-r2.md:143`, `:179–188`.

“PR B sửa ci.yml nên chạy packet-loop” chỉ chứng minh nhóm ấy đã chạy; chưa chứng minh tập diff của PR/push bằng nhau hoặc ImageVersion của hai lượt khớp. Vì vậy lập luận dùng để buộc output đúng cả bốn nhóm còn thiếu tiền đề. Đây là rủi ro của phép đo tương lai, **chưa chứng minh B5 chắc chắn không chạy được trên head B sẽ được tạo**.

Lệnh: `python -S out/review_tools.py python out/review_probes.py b5_probe` ⇒ **rc 0**; [output](review-evidence/20261120T102328855686.txt). Fixture dùng hai đường dẫn trong write set B, P1/P2 cùng chứa một thay đổi đã hội tụ và H sửa ci.yml:

```text
PR_DIFF   ['.github/workflows/ci.yml', 'ops/ci_duong_nhanh.py']
PUSH_DIFF ['.github/workflows/ci.yml']
PR_PACKET_LOOP = chay; B3F = False
```

Đúng Q7 phải loại `nhanh`, còn B5(i) lại chấm đỏ. Fixture đo điều kiện kỹ thuật, không khẳng định lịch sử này sẽ phát sinh dưới lease B. Windows/API/upload/redirect và tồn tại ImageOS/ImageVersion trên runner chưa đo LIVE.

**Hướng sửa:** khai precondition chọn dữ liệu dương: run/attempt đã hoàn tất, tất cả nhóm đã chạy, hai diff đúng consumer bằng nhau, runtime khớp; lưu số đo trước khi chấm. Cố định các biến còn lại cho mỗi vế âm. Nêu workflow/trigger, quyền, before/ref/SHA giả lập và hiện vật đọc lại; thiếu tiền đề là `not_measured`, không tự biến thành lỗi thuật toán hoặc E1.

### F8 — P2 — B7 không kiểm nguồn tái dùng và chưa có đột biến riêng đổi màu

**Vị trí:** `SPEC-B-r2.md:145–149`; `SPEC-A-r2.md:106–108`; `cay-kho/.claude/skills/soan-spec/SKILL.md:120–125`.

B7 kiểm các job push bị bỏ, marker của gate và hai phép Git **trên M**. Nó không đọc lại receipt/attempt/các job của PR nguồn, không kiểm Q7 hay image thực của nhóm, cũng không chỉ ra hiện vật bốn mốc của cả hai lượt theo Q6. Một lỗi chọn nhầm nguồn PR `duong_nhanh` nhưng vẫn đưa đúng parents của M xuống gate giữ nguyên tất cả phép đo được liệt kê ở B7. Như vậy B7 có thể đỏ khi cây sai, nhưng không đổi màu dưới lỗi “nhóm chưa được test mà được bỏ” — chính lớp rủi ro tính năng này cần quan sát ngoài mock.

Lệnh: `python -S out/review_tools.py python out/review_probes.py contract_probe` ⇒ **rc 0**, [output](review-evidence/20261120T101602085345.txt); đối chiếu B7 với các trường đầu vào của mô hình và F1 cho thấy phép so Git vẫn đúng khi chọn việc giữa PR/push sai. B7 còn ghi `—` ở đột biến, trái yêu cầu mỗi tiêu chí có đột biến hoặc khai chưa có cách đo của L3/L6. Đây là phân tích tiêu chí, **không phải kết quả canary sau land**.

Không xem “0 lượt tái dùng trong mười lượt” là lỗi thiết kế: B đã nói rõ trường hợp đó chưa đạt/chưa quan sát. Điểm phải sửa là tính chất được kiểm khi thực sự có tái dùng.

**Hướng sửa:** cho mỗi lượt tái dùng, lưu và kiểm độc lập run/attempt nguồn, artifact ID/hash, tập job/matrix/steps dương, checkout/runtime, diff/kế hoạch và workflow identity; nối bốn mốc với nhóm cụ thể. Thêm phép thử trên bản sao evidence: thay run/attempt, đổi PR sang làn nhanh, làm thiếu một shard hoặc làm lệch diff thì bộ chấm B7 phải đỏ. Lưu mốc chọn mười lượt bằng SHA/run ID/thời điểm; không yêu cầu huỷ hoặc gây lỗi CI thật để làm đột biến.

### F9 — P3 — Chưa có phép đo chống đỡ ước lượng 440 dòng sau khi tính đủ consumer

**Vị trí:** `SPEC-B-r2.md:76–78`, `:153`; `cay-kho/.claude/skills/soan-spec/SKILL.md:158`.

Tổng 45+160+220+15 đúng bằng 440, nhưng chỉ dư 10 dòng so với trần. Ước lượng chưa tính tệp Windows ngoài write set, các hash/guard bỏ sót, nối identity và phép đo hậu kiểm. Phần Python còn phải chứa receipt, REST có phân trang/redirect, ZIP/JSON, ngân sách 120 giây, proof Git, chọn nhóm, output và lệnh kiểm lại; phần test phải có fixture và các đột biến riêng của B2.

Đã đo Git history, không suy từ số dòng toàn tệp:

```text
git diff --numstat 7e5958e^1 7e5958e -- <4 tệp B>
ci.yml +90/-4; classifier +618/-0; test +3608/-0; registry +1/-0

git diff --numstat b8bc64f^1 b8bc64f -- <5 tệp đã ghi trong nhật ký>
ci.yml +56/-21; classifier +29/-4; test +133/-36;
registry +8/-5; wrapper packet_loop_test_manh.py +179/-0
```

Cả hai lệnh **rc 0**. Số +618/+3608 trong B là đúng. Packet #1343 gần hơn đã thêm 226 dòng vào bốn tệp B, chưa tính wrapper 179 dòng. Các số này **không chứng minh** B chắc chắn vượt 450; chúng không đủ làm căn cứ xác nhận 440 sẽ chứa hết hợp đồng.

**Hướng sửa:** lập lại bảng ước lượng theo các khối và consumer thực tế, có một phần dự phòng cho sửa test; đối chiếu numstat phạm vi tương đương. Nếu cần tách packet hoặc nâng trần, quyết định ở revision spec, không dùng việc giảm độ phủ test để vừa trần.

### F10 — P3 — Chưa khép hồ sơ L6/L7 và phép đo trước đóng băng

**Vị trí:** `SPEC-A-r2.md:117`, `:130–146`, `:152`; `SPEC-B-r2.md:139–145`, `:155`, `:162`; luật soạn spec `:114–125`, `:137–145`.

A có nối dòng theo đoạn, khớp nguyên câu và chia từng vị trí — đúng hướng L6(b,c). Nhưng chưa khai các vế không áp dụng của L6(a,d,e), chưa có phép đo đủ sáu vị trí cho lời khai **0 cổng**, và A3/A4 chưa nêu đầy đủ đột biến ngắt dòng/đổi hậu tố. B1/B7 dùng marker chuỗi nhưng chưa đóng mẫu và trường identity mà marker chứng minh. A:145 mới ghi “dự kiến” rồi giao executor đo, trong khi L6 yêu cầu đo tiêu chí đo được **trước đóng băng**.

Lệnh `python -S out/review_tools.py python out/review_probes.py policy_probe` ⇒ **rc 0**: đã quét sáu vị trí §20, chưa có các marker `ADR-0068`, `tai_dung_bo`, `bien-nhan-cay`, `kiem-tai-dung`, `TAI_DUNG:` ở nền. Đó là bằng chứng nền theo các tên tính năng, không phải tự chứng minh mọi hành vi tương đương vắng mặt. `a_probes` đã cho baseline A1/A7 xanh và mutant rc 9/6; có thể dùng các kết quả này làm đầu vào revision.

Về L7, các điểm xin quyền thực chất đã có E1/E2/E5 và hai `pham_vi_e` đều khai E4 không chạm, E5 chạm. Tuy nhiên câu chạm trần lời gọi ở A:152/B:155 chỉ ghi E2, chưa ghi mức đã dùng/còn thiếu/để làm gì; B:162–163 chưa ghi đề xuất kèm E1. Một số câu nhắc duyệt băm ở A:7/A:88 chỉ dựa vào E5 ở nơi khác. Không tìm thấy ngân sách mềm hay quy tắc tự đặt “hai lượt chưa approve thì hỏi”.

**Hướng sửa:** bổ sung bảng năm vế L6 với N/A có lý do; lưu các baseline/mutant trước đóng băng. Gắn E5 tại câu xin/chờ quyết định khi cần đọc độc lập, hoàn thiện payload E1/E2 theo ADR-0067. Các sửa này không đòi hỏi hỏi chủ kho trong lượt review hiện tại.

## Đối chiếu trích dẫn và lời khai về mã

Các số dòng dưới đây là của HEAD `45bae8d0`. Không có finding riêng về số dòng trôi trong những neo đã dẫn; các lỗi là thiếu consumer, thiếu phạm vi hoặc khẳng định mạnh hơn phép đo.

| Lời dẫn trong đặc tả | Đối chiếu đã đọc/chạy | Kết quả |
|---|---|---|
| A §10.1 `:909–910`, §10.2.2 `:975–977` | Đọc protocol, nối dòng theo đoạn | Hai câu gốc khớp; lưu ý hàng T4 tại :903, F5 |
| A §20 ADR-0067 `:1562` | Đọc bảng thật | Đúng vị trí; chưa có ADR-0068 trên HEAD |
| A/B K2 CI `packet_loop.py:3646` | Đọc lời gọi `_kiem_ci(..., h, ...)` và các gate kế cận | Đúng, đọc head PR; không phải gate đọc push |
| A `PHU_THUOC_PACKET_LOOP :138`, push `:411`; B `:406–421` | Đọc hằng/hàm, gọi thật trong probe | Đúng; push luôn `chay`, PR có `bo_qua` |
| B LAND verify `ci.yml:501` | Tên bước :501, if :502 | Đúng: ref master và `che_do != duong_nhanh`; CLAUDE deploy mục 5 ở :1129–1132 khớp |
| B selftest non-PR `ci.yml:342–374` | Bước :342, if :343 | Đúng; PR có bước selftest riêng :339–341; upload evidence :377 dùng `always()` |
| B registry diff `ci.yml:1108–1110` | Env và consumer `doc_diff :860–873`, `ke_hoach :889–900` | Đúng env; suy luận tập diff ở B chưa đúng, F1 |
| B `ci_provenance.py:385–386` | Đọc nhánh skipped | Đúng: giữ `skipped`, không crash. Không biến skipped thành positive evidence |
| B y11 `:2849` và `JOB_CO_IF_CHO_PHEP` | y11 :2849, hằng :2844–2845 | Đúng; hằng không ở :2849 mà được y11 dùng |
| B y12/`IF_BUOC_CHUAN` | y12 :2859, hằng :2620 | Đúng tên/chức năng |
| B ảnh chụp đầu job `:2711–2712` | Hai mục packet-loop trong `KHUNG_JOB` bắt đầu :2702 | Đúng; còn `KHUNG_BUOC :2714`, y13 :2879 phải được cập nhật |
| B `_if_duoc :1454`, packet-loop :1523, registry/G5_MANH_IF | Đọc :1425, :1454, :1523–1525 | Đúng tên/vị trí; danh sách chốt chưa đủ, F2 |
| B `94cbb36 → 45bae8d0` không đổi tập tệp đã nêu | `git diff --stat` đúng tập đường dẫn | Rỗng, rc 0 |
| B tám job/bốn nhóm | Parse YAML và đếm matrix Ubuntu | **8 định nghĩa job / 37 instance**: cong_cu 8+1, ops 1, nhanh 8+1+1, packet_loop 16+1. Thêm gate và chuan-bi là 39 instance Ubuntu khi chạy đủ |
| B PR làn nhanh “các job vẫn success” | `gate-cong-cu` cấp job :572; packet-loop-manh :1125 | Chỉ đúng với các job vẫn khởi động; không đúng cho mọi job. Cần viết hẹp lại: các job/required context thành công vẫn có thể đã bỏ bước nặng |
| B “giữ che_do/packet_loop” và A “push chạy đủ như cũ” | `policy_probe`, t52 :2208–2222 | Hai lời mô tả không cùng đúng nếu hiểu “đủ” cho mọi push; F5 |
| B merge squash/rebase không tái dùng | Điều kiện M có đúng hai cha | Đủ loại merge một cha; không chỉ dựa vào tên nhánh |

Đã rà mọi `if:` và đầu vào `github.*` của workflow. Các điều kiện **trực tiếp** theo ref/event đều ở gate/chuan-bi như Q4; ngoài đó có env của `gate-ops` tại :749 nhưng chỉ chạy khi `duong_nhanh`, và env registry là F1. Các điều kiện runner.os, che_do, packet_loop, `!cancelled()` và phụ thuộc job cũng đã đọc.

Còn một khác biệt **gián tiếp** cần ghi vào thiết kế: packet-loop gọi `_carrier1174`, đọc `GITHUB_EVENT_NAME` và event payload (`packet_loop_test.py:15295–15326`, `:15423–15476`). `event_probe` chạy nguyên hàm routing cho kết quả PR thường `integration_pr`, push `ci_push_snapshot`; riêng source PR1275 chọn exact-H clone thay cho checkout merge. Wrapper giữ carrier ở shard 0 (`packet_loop_test_manh.py:94–107`). Không phát hiện đây là một bypass hiện hành cho PR B: PR thường giữ cùng nhóm ca/native requirement, còn PR1275 là đường lịch sử đặc biệt. Tuy nhiên Q4 chỉ quét YAML không chứng minh mọi mã bên dưới độc lập với event; không dùng Q4 làm bằng chứng rộng hơn phạm vi nó đo.

## Các đường fail-open đã xét

| Tình huống | Đánh giá đặc tả hiện tại |
|---|---|
| PR `duong_nhanh`, job success nhưng bỏ bước | 3c đòi `day_du`, có đột biến B2: đóng ở mức hợp đồng nếu receipt thật sự gắn đúng job/attempt |
| PR packet-loop `bo_qua` | 16 shard thiếu/skipped làm 3e không đủ, push phải chạy nhóm; không dùng job gom “KHÔNG ĐO” làm evidence |
| Thiếu một job/một shard đơn lẻ | Đếm đủ + mọi success bắt được; thiếu shard đồng thời trùng shard/identity còn cần tập khoá chuẩn, F4 |
| Artefact của run khác | `run_id` khác bị chặn; producer/artifact ID/hash, attempt và checkout độc lập chưa đóng đủ, F4 |
| PR fork | Điều kiện `head_repository.full_name == GITHUB_REPOSITORY` chặn theo hợp đồng, có đột biến B2. Chưa đo field/API LIVE |
| Nhánh dùng lại tên | Truy vấn theo P2 rồi so cha/cây tránh việc chỉ tin tên nhánh; không có finding chỉ vì tên nhánh dùng lại |
| Rerun một phần | Spec tự khai chưa đo giữ artefact; chưa đủ căn cứ biến thành evidence cùng attempt, F4 |
| HTTP/JSON/ZIP/timeout | Có yêu cầu fallback rỗng và đột biến. Chưa có mã để kiểm atomic output, phân trang/timeout thật, và B5 chưa chạy |
| Push nhiều commit, rename phía base | Có phản chứng chạy được, F1 |
| Q2 cây bằng nhau | Đủ chứng minh quan hệ object Git khi nguồn checkout đáng tin. Không chứng minh chọn cùng việc, cùng runtime hoặc cùng provenance; F1/F4 |

## Kiểm L1–L7 và nghiệm thu

| Luật | A | B |
|---|---|---|
| L1 — đơn vị đếm | Bảy câu, bốn phép khớp, hai tệp rõ đơn vị | Tám định nghĩa job khác 37 instance; bảng ma trận đúng. B2 nên đánh số toàn bộ chốt/đột biến để kiểm đủ từng ánh xạ |
| L2 — mục tiêu ↔ write set | Hai nhóm mục tiêu chiếu đúng hai tệp | Chưa đủ consumer; F2. Mục tiêu 6 nên tách dòng theo ci.yml và Python để rõ trách nhiệm |
| L3 — phép đỏ và đột biến | A1/A7 đo được và có răng; A2/A3/A4 có màu nền; mục tiêu còn thiếu phép đo, F6 | B1 đường Windows thiếu; B2/B3 có đột biến cụ thể; B5/B7 còn khoảng trống, F3/F7/F8 |
| L4 — hình dạng kế thừa | `khong_ap_dung`, có giải thích không phải packet khắc phục | Tương tự; không ép chép bộ đếm của một packet không phải tiền nhiệm khắc phục |
| L5 — thời điểm và đo lại | Số đo có nguồn/thời điểm, yêu cầu đo lại khi cấp lease; vẫn cần baseline trước đóng băng | Neo 20-11, khai lease giao nhau và yêu cầu revision khi nền đổi là đúng; ước lượng cần cập nhật, F9 |
| L6 — thước đo chuỗi | (b,c) đã khai; (a,d,e) cần N/A/phép đo cụ thể, F6/F10 | Marker và canary chưa đóng đủ; F8/F10 |
| L7 — điểm hỏi/E | E4/E5 đã khai, không ngân sách mềm; cần hoàn thiện mã/payload tại câu liên quan | E1/E2/E5 có; không tự thêm checkpoint sau N review. Thiếu payload chi tiết, F10 |

Kết quả nghiệm thu **đã đo trong review**, không phải nghiệm thu hai packet:

| Tiêu chí | Trạng thái/lý do |
|---|---|
| A1 baseline | Passed trên bản sao đúng dữ liệu cần đọc: 66 ADR / 66 dòng; xoá hàng mới sau khi thêm ADR ⇒ rc **9** |
| A2/A3/A4 baseline | Chưa có ADR/P1/P2 nên không đạt hành vi mới; probe đối nghịch cho các lỗ F6 |
| A5/A6 | Chưa có diff triển khai; đã dựng diff hai tệp phản chứng để đo độ chặt của tiêu chí |
| A7 baseline/mutant | Passed, 12 adapter/tệp sạch; chép P1 sau khi nối protocol ⇒ rc **6** đúng vì chép doctrine |
| A8 | Not run: không có PR A/CI đầu-cuối trong gói offline |
| B1–B4 | Chưa có mã B để nghiệm thu. Đã kiểm cấu trúc, các guard thật và phản chứng; không chạy toàn bộ suite nặng |
| B5 | Not measured LIVE; chỉ có probe Git/diff cục bộ. Token, artefact, redirect, runner image vẫn chưa xác nhận |
| B6 | Not run trên bản B chưa tồn tại; chưa có delta actionlint để chứng nhận |
| B7 | Not measured: B chưa land; không có mười lượt push sau B để quan sát |

## Đối chiếu số đo và giới hạn nguồn

`bang-chung/master-runs-20261120.json` có 60 dòng, 40 lượt đầy đủ, **28 lượt đầy đủ xanh**. Dữ liệu đã làm tròn cho trung vị tường **30,35 phút** (phù hợp 30,4); trung vị phút runner từ cột số nguyên là **266,5**. Bản đầu ra phép đo ghi **266,1** trước làm tròn. Không dùng khác biệt độ chính xác này làm finding; không có timestamps từng job để tính lại 266,1.

Các nhóm 146,4 / 25,3 / 33,1 / 41,7 khớp tổng trung vị từng tên job trong `do-master-20261120.txt`; không phải trung vị tổng một nhóm. Gate 16,7 và hàng đợi push p99 878/PR p99 123 khớp bản đầu ra cung cấp. Không có raw jobs để kiểm độc lập các phân vị.

Số lần 1 (147 PR, 79 đầy đủ, 25/44/10, 8/8 checkout) khớp tài liệu đề xuất, nhưng không có tập REST/log đầy đủ để tái lập cả phép đo. Tương tự, 1.203 run có `pull_requests=[]`, 366/367 nhánh, lease `wp1448-r2-g1-claude`, trạng thái Issue và quyền token là lời khai lịch sử trong tài liệu, không được xác nhận lại từ máy chủ. Không đọc `D:/tlscan.git` hoặc dùng mạng để lấp chỗ thiếu. Điều kiện cấp lease và số ADR phải được đo lại tại thời điểm thật.

## Bảng lệnh

Bảng chi tiết bên dưới được tạo từ nhật ký cục bộ. `rc=0` của một **probe phản chứng** nghĩa là đã xác nhận phản chứng, không phải tính năng B đạt. Các lệnh con Git/gate của probe nằm trong mã tái lập và output; A1/A7 có mã gate riêng nêu ở trên. Các lần lỗi công cụ/fixture được giữ lại và không dùng làm finding sản phẩm.

<!-- COMMAND_TABLE_BEGIN -->
`RV = C:\r\d2`. Cột cwd ghi thư mục của lệnh con thực sự; wrapper luôn được gọi từ RV. Các bước đọc mở đầu trước khi có wrapper gồm `Get-Content PROMPT.md -Raw`, đọc các SPEC/DIFF, AGENTS.md và skill `cay-kho/.claude/skills/soan-spec/SKILL.md` (rc 0). Phần kiểm quyết định kết luận được lưu đầy đủ bên dưới. Hai lần đọc đầu ghi rc đọc là 0 trong JSONL nhưng tiến trình in console kết thúc 1 do encoding; bảng phân biệt hai mã này.

| # | Lệnh (gọi từ RV) | cwd lệnh con | rc | Kết luận và output |
|---|---|---|---|---|
| 1 | `python -S out/review_tools.py 'read' 'cay-kho/CONTEXT.md@1:120' 'cay-kho/CLAUDE.md@1:210' 'cay-kho/docs/PROTOCOL_DA_PHIEN.md@875:1050' 'cay-kho/docs/PROTOCOL_DA_PHIEN.md@1480:1580'` | `RV` | 1 console / 0 đọc | Đã đọc context/protocol; phần in console lỗi Unicode, chạy lại sau khi đặt UTF-8. Không phải lỗi kho. [Output](review-evidence/20261120T094344092606.txt) |
| 2 | `python -S out/review_tools.py 'read' 'cay-kho/.github/workflows/ci.yml@1:210' 'cay-kho/.github/workflows/ci.yml@540:1180'` | `RV` | 1 console / 0 đọc | Đã đọc workflow; phần in console lỗi Unicode, chạy lại ở lệnh kế tiếp. [Output](review-evidence/20261120T094344703854.txt) |
| 3 | `python -S out/review_tools.py 'read' 'cay-kho/.github/workflows/ci.yml@1:210' 'cay-kho/.github/workflows/ci.yml@540:1180'` | `RV` | 0 | Đọc workflow thành công sau khi đặt UTF-8; xác định các điều kiện và đầu vào. [Output](review-evidence/20261120T094355575965.txt) |
| 4 | `python -S out/review_tools.py 'read' 'cay-kho/docs/PROTOCOL_DA_PHIEN.md@875:1050' 'cay-kho/docs/PROTOCOL_DA_PHIEN.md@1480:1580'` | `RV` | 0 | Đọc câu reuse, T4, bốn mốc và bảng ADR; căn cứ F5/F6. [Output](review-evidence/20261120T094404943109.txt) |
| 5 | `python -S out/review_tools.py 'rg' 'JOB_CO_IF_CHO_PHEP&#124;IF_BUOC_CHUAN&#124;G5_MANH_IF&#124;def _if_duoc&#124;def loi_g5_workflow&#124;CI_DANG_KY_SU_KIEN&#124;def .*diff&#124;git.*diff' '.claude/dev/ci_dang_ky_test.py' 'ops/ci_duong_nhanh_test.py'` | `RV/cay-kho` | 0 | Tìm đúng tên/vị trí chốt và consumer diff. [Output](review-evidence/20261120T094434038400.txt) |
| 6 | `python -S out/review_tools.py 'rg' '-l' 'gate-packet-loop-manh&#124;gate-nhanh-gop&#124;gate-cong-cu&#124;JOB_CO_IF_CHO_PHEP' '--glob' '*test*' '--glob' '!ops/specs/**' '--glob' '!ops/reviews/**' '--glob' '!ops/land/**' '--hidden'` | `RV/cay-kho` | 1 | Không có match do tập tìm kiếm bị ignore; chưa kết luận vắng consumer. Tìm lại với --no-ignore. [Output](review-evidence/20261120T094434322222.txt) |
| 7 | `python -S out/review_tools.py 'read' 'cay-kho/.github/workflows/ci.yml@1180:1290' 'cay-kho/ops/ci_duong_nhanh.py@1:230' 'cay-kho/ops/ci_duong_nhanh.py@320:570'` | `RV` | 0 | Đọc job packet-loop, phân loại và dependency hiện hữu. [Output](review-evidence/20261120T094434804943.txt) |
| 8 | `python -S out/review_tools.py 'read' 'cay-kho/ops/ci_duong_nhanh.py@166:240' 'cay-kho/ops/ci_duong_nhanh.py@260:345' 'cay-kho/ops/ci_duong_nhanh.py@380:432' 'cay-kho/.claude/dev/ci_dang_ky_test.py@840:960'` | `RV` | 0 | Đối chiếu hai thuật toán diff; phát hiện khác biệt dẫn tới F1. [Output](review-evidence/20261120T094447340798.txt) |
| 9 | `python -S out/review_tools.py 'rg' '-l' '--hidden' '--no-ignore' '--glob' '!.git/**' '--glob' '!**/.codex/**' '--glob' '*test*' '--glob' '!ops/specs/**' '--glob' '!ops/reviews/**' '--glob' '!ops/land/**' 'gate-packet-loop-manh&#124;gate-nhanh-gop&#124;gate-cong-cu' '.'` | `RV/cay-kho` | 0 | Tìm thêm consumer workflow ở các bộ test, gồm gương Windows. [Output](review-evidence/20261120T094447728386.txt) |
| 10 | `python -S out/review_tools.py 'read' 'cay-kho/.claude/dev/ci_dang_ky_test.py@1410:1555' 'cay-kho/ops/ci_duong_nhanh_test.py@2690:2750' 'cay-kho/ops/ci_duong_nhanh_test.py@2820:2905'` | `RV` | 0 | Xác nhận G5, whitelist if và ảnh chụp job/step. [Output](review-evidence/20261120T094456184381.txt) |
| 11 | `python -S out/review_tools.py 'rg' 'gate-packet-loop-manh&#124;gate-nhanh-gop&#124;gate-cong-cu&#124;\[.if.\]&#124;get\(.if.' 'ops/cong_cu_test.py' '.claude/dev/chay-cong-windows_test.ps1' '.claude/dev/launcher_test.py' '.claude/dev/packet_loop_test.py'` | `RV/cay-kho` | 0 | Định vị fingerprint Windows và các consumer khác. [Output](review-evidence/20261120T094456539090.txt) |
| 12 | `python -S out/review_tools.py 'rg' 'github\.&#124;GITHUB_&#124;CI_DANG&#124;if:' '.github/workflows/ci.yml'` | `RV/cay-kho` | 0 | Rà tất cả dòng github.*, GITHUB_ và if trong workflow. [Output](review-evidence/20261120T094546247310.txt) |
| 13 | `python -S out/review_tools.py 'read' 'cay-kho/.claude/dev/chay-cong-windows_test.ps1@1240:1375' 'cay-kho/.claude/dev/ci_dang_ky_test.py@790:840' 'bang-chung/do-master-20261120.txt'` | `RV` | 0 | Đọc bộ tính fingerprint, hash registry và bản số đo master. [Output](review-evidence/20261120T094547020395.txt) |
| 14 | `python -S out/review_tools.py 'read' 'cay-kho/ops/ci_duong_nhanh_test.py@100:160' 'cay-kho/.claude/dev/ci_dang_ky_test.py@1:65' 'cay-kho/.github/workflows/ci.yml@740:865' 'cay-kho/docs/adr/0053-tran-kich-thuoc-sensitive-len-sau-tep.md' 'cay-kho/docs/adr/0055-tran-loi-goi-codex-len-muoi.md'` | `RV` | 0 | Đọc setup test, gate-ops và ADR trần tệp/dòng/lời gọi. [Output](review-evidence/20261120T094630345361.txt) |
| 15 | `python -S out/review_tools.py 'python' 'out/review_probes.py' 'inventory'` | `RV` | 0 | Đếm tám định nghĩa/37 instance; xác nhận bước B1 bị Linux-only, F3. [Output](review-evidence/20261120T094757109434.txt) |
| 16 | `python -S out/review_tools.py 'python' 'out/review_probes.py' 'pins'` | `RV` | 0 | Guard nền xanh; thêm job-if làm hash/G5 đỏ và tám fingerprint lệch, F2. [Output](review-evidence/20261120T094758776494.txt) |
| 17 | `python -S out/review_tools.py 'python' 'out/review_probes.py' 'diff_probe'` | `RV` | 0 | Probe diff sơ bộ; đã chạy lại với tệp .py hợp lệ ở 10:24, dùng bản cuối làm bằng chứng F1. [Output](review-evidence/20261120T094803522745.txt) |
| 18 | `python -S out/review_tools.py 'python' 'out/review_probes.py' 'b5_probe'` | `RV` | 0 | Probe B5 sơ bộ; đã thay fixture bằng đường dẫn trong write set và chạy lại ở 10:23. [Output](review-evidence/20261120T094806075577.txt) |
| 19 | `python -S out/review_tools.py 'rg' '--hidden' '--no-ignore' '--glob' '!.git/**' '--glob' '!**/.codex/**' '--glob' '*.py' '--glob' '*.ps1' '--glob' '*.sh' '--glob' '!ops/specs/**' '--glob' '!ops/reviews/**' '--glob' '!ops/land/**' 'GITHUB_EVENT_NAME&#124;GITHUB_REF&#124;GITHUB_BASE_REF&#124;GITHUB_HEAD_REF&#124;GITHUB_EVENT_PATH&#124;CI_DANG_KY_SU_KIEN' 'ops' '.claude' 'scripts' '.githooks' '.github'` | `RV/cay-kho` | 0 | Rà consumer sự kiện trong mã gọi gián tiếp; tìm carrier packet-loop. [Output](review-evidence/20261120T094816193906.txt) |
| 20 | `python -S out/review_tools.py 'read' 'SPEC-A-r2.md@95:170' 'SPEC-B-r2.md@177:217' 'cay-kho/ops/ci_provenance.py@365:400' 'cay-kho/.claude/dev/packet_loop.py@3638:3705'` | `RV` | 0 | Đối chiếu Q1–Q7, K2 và xử lý skipped của provenance. [Output](review-evidence/20261120T094816457060.txt) |
| 21 | `python -S out/review_tools.py 'read' 'cay-kho/.claude/dev/packet_loop_test.py@15270:15545' 'cay-kho/.claude/dev/packet_loop_test_manh.py@1:230'` | `RV` | 0 | Đọc carrier và wrapper chia shard; ghi giới hạn của phép rà YAML. [Output](review-evidence/20261120T094825992726.txt) |
| 22 | `python -S out/review_tools.py 'rg' 'def cmd_adr_song&#124;def cmd_doctrine_scan&#124;def .*adr&#124;def .*doctrine&#124;WP1174_SOURCE_PR&#124;DOCTRINE' '.claude/dev/packet_loop.py' '.claude/dev/packet_loop_test.py'` | `RV/cay-kho` | 0 | Định vị adr-song, doctrine-scan và carrier nguồn PR. [Output](review-evidence/20261120T094906556857.txt) |
| 23 | `python -S out/review_tools.py 'read' 'cay-kho/docs/adr/0067-danh-sach-dong-va-uy-quyen-thuong-truc.md@1:220' 'cay-kho/docs/adr/0053-tran-kich-thuoc-sensitive-len-sau-tep.md@1:47' 'DE-XUAT-20261116.md@1:125'` | `RV` | 0 | Đọc E1–E5, trần sensitive và số đo đề xuất lần 1. [Output](review-evidence/20261120T094906753144.txt) |
| 24 | `python -S out/review_tools.py 'read' 'cay-kho/.claude/dev/packet_loop.py@1700:1820' 'cay-kho/.claude/dev/packet_loop.py@1995:2045'` | `RV` | 0 | Đọc logic gate ADR và quét doctrine để dựng mutant đúng. [Output](review-evidence/20261120T094926252316.txt) |
| 25 | `python -S out/review_tools.py 'rg' 'reuse&#124;tái dùng&#124;hậu.merge&#124;tree&#124;identity&#124;skipped' 'docs/PROTOCOL_DA_PHIEN.md'` | `RV/cay-kho` | 0 | Rà các câu reuse/tree/identity trong protocol. [Output](review-evidence/20261120T094926533519.txt) |
| 26 | `python -S out/review_tools.py 'git' 'log' '--all' '--format=%H %s' '--grep=#703' '--grep=#1344' '--grep=#1113' '--grep=#1353' '-n' '15'` | `RV/cay-kho` | 128 | Git từ chối dubious ownership; chưa đo được. Đã đặt safe.directory riêng tiến trình rồi chạy lại. [Output](review-evidence/20261120T094926790542.txt) |
| 27 | `python -S out/review_tools.py 'git' 'log' '--all' '--format=%H %s' '--grep=#703' '--grep=#1344' '--grep=#1113' '--grep=#1353' '-n' '15'` | `RV/cay-kho` | 0 | Tìm được các commit lịch sử dùng kiểm lời khai và ước lượng. [Output](review-evidence/20261120T094942761898.txt) |
| 28 | `python -S out/review_tools.py 'read' 'cay-kho/ops/land/pr997-wp978-land-evidence.yaml@1:190' 'cay-kho/docs/PROTOCOL_DA_PHIEN.md@385:439'` | `RV` | 0 | Đọc evidence PR997 và yêu cầu hậu merge/provenance. [Output](review-evidence/20261120T094942953625.txt) |
| 29 | `python -S out/review_tools.py 'git' 'diff' '--stat' '94cbb36' '45bae8d0' '--' '.github/workflows/' 'ops/ci_duong_nhanh.py' 'ops/ci_duong_nhanh_test.py' '.claude/dev/ci_dang_ky_test.py' 'docs/PROTOCOL_DA_PHIEN.md' 'docs/adr/'` | `RV/cay-kho` | 0 | Diff tập tệp đã nêu giữa 94cbb36 và 45bae8d0 rỗng; lời khai đúng. [Output](review-evidence/20261120T094943228207.txt) |
| 30 | `python -S out/review_tools.py 'read' 'cay-kho/.claude/dev/packet_loop.py@40:72' 'cay-kho/.claude/dev/packet_loop.py@2044:2118'` | `RV` | 0 | Đọc cấu hình và phần còn lại của doctrine-scan. [Output](review-evidence/20261120T095005520208.txt) |
| 31 | `python -S out/review_tools.py 'rg' '-n' 'def main&#124;state_dir&#124;adr-song&#124;doctrine-scan' '.claude/dev/packet_loop.py' '--max-count' '8'` | `RV/cay-kho` | 0 | Định vị CLI/state-dir và các gate; hỗ trợ chạy trên bản sao out/thu. [Output](review-evidence/20261120T095005866935.txt) |
| 32 | `python -S out/review_tools.py 'git' 'log' '--all' '--format=%H %s' '--grep=Merge pull request #703' '--grep=CI-LAN-LUU-TRU' '-n' '15'` | `RV/cay-kho` | 0 | Tìm merge PR703 và packet làn lưu trữ để đo numstat. [Output](review-evidence/20261120T095007720790.txt) |
| 33 | `python -S out/review_tools.py 'read' 'cay-kho/ops/KE_HOACH_THI_CONG_DA_PROVIDER.md@1:70' 'cay-kho/CONTEXT.md@1:60' 'cay-kho/CLAUDE.md@1:85'` | `RV` | 0 | Đọc quy ước kho/context để xác định giới hạn review. [Output](review-evidence/20261120T095007883302.txt) |
| 34 | `python -S out/review_tools.py 'rg' 'def main&#124;parse_args&#124;state_dir =&#124;state-dir&#124;cmd_adr_song&#124;cmd_doctrine_scan' '.claude/dev/packet_loop.py'` | `RV/cay-kho` | 0 | Xác nhận cách truyền root/state-dir cho gate bản sao. [Output](review-evidence/20261120T095020582282.txt) |
| 35 | `python -S out/review_tools.py 'git' 'diff' '--numstat' '7e5958e440285c8d63d2f710cf97ba20b85f2926^1' '7e5958e440285c8d63d2f710cf97ba20b85f2926' '--' 'ops/ci_duong_nhanh.py' 'ops/ci_duong_nhanh_test.py' '.github/workflows/ci.yml' '.claude/dev/ci_dang_ky_test.py'` | `RV/cay-kho` | 0 | Đo PR703: classifier +618, test +3608, workflow +90, registry +1; số B dẫn đúng. [Output](review-evidence/20261120T095020846645.txt) |
| 36 | `python -S out/review_tools.py 'git' 'diff' '--numstat' 'b8bc64f^1' 'b8bc64f' '--' '.github/workflows/ci.yml' 'ops/ci_duong_nhanh.py' 'ops/ci_duong_nhanh_test.py' '.claude/dev/ci_dang_ky_test.py' '.claude/dev/packet_loop_test_manh.py'` | `RV/cay-kho` | 0 | Đo PR1343: bốn tệp +226, wrapper +179; căn cứ đánh giá F9. [Output](review-evidence/20261120T095021146757.txt) |
| 37 | `python -S out/review_tools.py 'python' 'out/review_probes.py' 'anchors'` | `RV` | 1 | Probe anchors lỗi do giả định JSON là object; dữ liệu thực là mảng. Sửa probe, không dùng kết quả này cho thống kê. [Output](review-evidence/20261120T101557294505.txt) |
| 38 | `python -S out/review_tools.py 'python' 'out/review_probes.py' 'event_probe'` | `RV` | 0 | Chạy nguyên hàm routing: PR integration_pr, push ci_push_snapshot; ghi khác biệt gián tiếp. [Output](review-evidence/20261120T101601582656.txt) |
| 39 | `python -S out/review_tools.py 'python' 'out/review_probes.py' 'contract_probe'` | `RV` | 0 | Mô hình predicate đặc tả cho thấy thiếu ràng buộc job/attempt/runtime; không phải thử nghiệm GitHub. [Output](review-evidence/20261120T101602085345.txt) |
| 40 | `python -S out/review_tools.py 'python' 'out/review_probes.py' 'a_probes'` | `RV` | 0 | Baseline/mutant A cho rc gate 0/9/6; bổ sung probe và chạy lại ở 10:20. [Output](review-evidence/20261120T101602878111.txt) |
| 41 | `python -S out/review_tools.py 'python' 'out/review_probes.py' 'anchors'` | `RV` | 0 | Xác nhận hash/HEAD/tree, lịch sử ADR, clone không shallow và thống kê 60 run. [Output](review-evidence/20261120T101640482512.txt) |
| 42 | `python -S out/review_tools.py 'rg' 'skipped&#124;post_merge&#124;gate_output&#124;moc_gate&#124;post.merge&#124;provenance' 'ops/land_evidence_nguon.py'` | `RV/cay-kho` | 0 | Rà source evidence reader; chưa tìm consumer chắc chắn cần sửa thêm ở tệp này. [Output](review-evidence/20261120T101701485986.txt) |
| 43 | `python -S out/review_tools.py 'read' 'cay-kho/ops/ci_duong_nhanh.py@830:930'` | `RV` | 0 | Đọc đầu ra/lối kết thúc classifier hiện tại. [Output](review-evidence/20261120T101701691482.txt) |
| 44 | `python -S out/review_tools.py 'rg' '-n' 'def main&#124;N/N&#124;TONG&#124;TỔNG&#124;CA:&#124;CI_DUONG_NHANH_CHE_DO&#124;windows' 'ops/ci_duong_nhanh_test.py' '--max-count' '35'` | `RV/cay-kho` | 0 | Kiểm vị trí test main, marker và ca Windows. [Output](review-evidence/20261120T101701958493.txt) |
| 45 | `python -S out/review_tools.py 'read' 'cay-kho/docs/PROTOCOL_DA_PHIEN.md@1628:1643' 'cay-kho/.claude/dev/chay-cong-windows_test.ps1@1380:1415'` | `RV` | 0 | Đọc bảng gate và consumer fingerprint t32 gây đỏ khi hash lệch. [Output](review-evidence/20261120T101702594217.txt) |
| 46 | `python -S out/review_tools.py 'read' 'cay-kho/ops/ci_duong_nhanh.py@790:829' 'cay-kho/ops/ci_duong_nhanh_test.py@2204:2230' 'cay-kho/ops/ci_duong_nhanh_test.py@50:100' 'cay-kho/.claude/skills/soan-spec/SKILL.md@90:170'` | `RV` | 0 | Đọc phân loại push/test nền và chính xác luật L6/L7. [Output](review-evidence/20261120T101745339074.txt) |
| 47 | `python -S out/review_tools.py 'rg' 'chay-cong-windows_test&#124;CI_DUONG_NHANH_SU_KIEN&#124;GITHUB_SHA&#124;GITHUB_RUN_ATTEMPT&#124;GITHUB_RUN_ID' '.claude/dev/ci_dang_ky_test.py' 'ops/ci_duong_nhanh.py' 'ops/cong_cu_test.py' 'ops/nhanh_don_duoc_test.py'` | `RV/cay-kho` | 0 | Rà thêm các env sự kiện/run/attempt trong nhóm test được bỏ. [Output](review-evidence/20261120T101745764146.txt) |
| 48 | `python -S out/review_tools.py 'rg' '-n' '--hidden' '--no-ignore' '--glob' '!.git/**' '--glob' '!**/.codex/**' '--glob' '!ops/specs/**' '--glob' '!ops/reviews/**' '--glob' '!ops/land/**' 'chay-cong-windows_test.ps1' '.github' '.claude/dev' 'ops' 'scripts' 'docs/adr/0060-dieu-kien-merge-va-lan-so-sach.md'` | `RV/cay-kho` | 2 | rg lỗi một đường ADR0060 đoán sai; kết quả không dùng để khẳng định vắng. Đã tìm tên đúng và chạy lại. [Output](review-evidence/20261120T101807534006.txt) |
| 49 | `python -S out/review_tools.py 'rg' 'release-verify&#124;manifest committed&#124;Quy ước deploy' 'CLAUDE.md'` | `RV/cay-kho` | 0 | Định vị quy ước release-verify trong CLAUDE.md. [Output](review-evidence/20261120T101808518191.txt) |
| 50 | `python -S out/review_tools.py 'git' 'diff' '--name-only' '45bae8d0' 'origin/master' '--' '.github/workflows/ci.yml' 'ops/ci_duong_nhanh.py' 'ops/ci_duong_nhanh_test.py' '.claude/dev/ci_dang_ky_test.py' 'docs/PROTOCOL_DA_PHIEN.md'` | `RV/cay-kho` | 0 | Năm tệp chính không đổi giữa HEAD đóng gói và origin/master cục bộ. [Output](review-evidence/20261120T101810342305.txt) |
| 51 | `python -S out/review_tools.py 'python' 'out/review_probes.py' 'policy_probe'` | `RV` | 0 | Push hồ sơ thật được phân loại duong_nhanh; in T4 và quét sáu vị trí cổng, F5/F10. [Output](review-evidence/20261120T102034888989.txt) |
| 52 | `python -S out/review_tools.py 'read' 'cay-kho/CLAUDE.md@1104:1136'` | `RV` | 0 | Xác nhận quy ước deploy mục 5 và nhánh manifest PR/master. [Output](review-evidence/20261120T102035186098.txt) |
| 53 | `python -S out/review_tools.py 'python' 'out/review_probes.py' 'a_probes'` | `RV` | 0 | Probe A cuối: gate nền 0; mutant ADR rc9, doctrine rc6; tiêu chí vẫn nhận ADR thiếu mục/câu thứ tám/xoá câu cũ. [Output](review-evidence/20261120T102042424479.txt) |
| 54 | `python -S out/review_tools.py 'read' 'cay-kho/docs/adr/0060-dieu-kien-merge-va-moc-ready.md@1:150'` | `RV` | 0 | Đọc đúng ADR0060, phân biệt Windows local M3 với bằng chứng dispatch B1. [Output](review-evidence/20261120T102231468625.txt) |
| 55 | `python -S out/review_tools.py 'rg' '-n' '--hidden' '--no-ignore' '--glob' '!.git/**' '--glob' '!**/.codex/**' '--glob' '!ops/specs/**' '--glob' '!ops/reviews/**' '--glob' '!ops/land/**' 'chay-cong-windows_test.ps1' '.github' '.claude/dev' 'ops' 'scripts' 'docs/adr/0060-dieu-kien-merge-va-moc-ready.md'` | `RV/cay-kho` | 0 | Rà lại đường dẫn Windows-test trên tập hợp hợp lệ; không thấy gọi trực tiếp trong ci.yml. [Output](review-evidence/20261120T102232762972.txt) |
| 56 | `python -S out/review_tools.py 'python' 'out/review_probes.py' 'a6_git_probe'` | `RV` | 0 | Bỏ kết quả fixture A6 lần đầu: ghi CRLF làm diff sai phạm vi. Đã sửa ghi LF và chạy lại; không dùng kết quả này làm finding. [Output](review-evidence/20261120T102328191823.txt) |
| 57 | `python -S out/review_tools.py 'python' 'out/review_probes.py' 'b5_probe'` | `RV` | 0 | Probe B5 cuối: packet-loop chay nhưng diff PR/push khác trên fixture trong write set. [Output](review-evidence/20261120T102328855686.txt) |
| 58 | `python -S out/review_tools.py 'python' 'out/review_probes.py' 'a6_git_probe'` | `RV` | 0 | Probe A6 cuối: diff thật hai tệp, hunk trong vùng cho phép vẫn xoá câu bất biến, F6. [Output](review-evidence/20261120T102354190987.txt) |
| 59 | `python -S out/review_tools.py 'python' 'out/review_probes.py' 'diff_probe'` | `RV` | 0 | Probe F1 cuối: cùng cha/cây và classifier diff nhưng registry chọn nhe/day_du khác nhau. [Output](review-evidence/20261120T102441667529.txt) |
| 60 | `python -S out/review_tools.py 'git' 'status' '--porcelain=v1' '--untracked-files=all'` | `RV/cay-kho` | 0 | Kiểm cuối: status porcelain rỗng, gồm mọi tệp chưa theo dõi; không đổi clone nguồn. [Output](review-evidence/20261120T103047403602.txt) |
| 61 | `python -S out/review_tools.py 'hash' 'SPEC-A-r2.md' 'SPEC-B-r2.md' 'SPEC-A-r1.md' 'SPEC-B-r1.md'` | `RV` | 0 | Kiểm cuối: bốn hash đặc tả giữ nguyên, hai r2 khớp neo đầu report. [Output](review-evidence/20261120T103049346777.txt) |
| 62 | `python -S out/review_tools.py 'git' 'rev-parse' 'HEAD' 'HEAD^{tree}'` | `RV/cay-kho` | 0 | Kiểm cuối: HEAD và tree giữ nguyên mốc được yêu cầu. [Output](review-evidence/20261120T103051701699.txt) |
| Cuối | `python -S out/finalize_review.py` | `RV` | 0 | Tạo bảng từ nhật ký; kiểm cấu trúc, số finding, liên kết và neo. [Kết quả](review-evidence/report-validation.json) |
<!-- COMMAND_TABLE_END -->

## Kết luận cuối

`changes_requested` cho cả A r2 và B r2. Ưu tiên sửa F1, đóng write set/chốt ghim và đường Windows (F2/F3), rồi thống nhất identity và luật ADR (F4/F5). Sau đó bổ sung tiêu chí bảo vệ nội dung protocol và quan sát nguồn tái dùng (F6/F8), cập nhật các mục P3 trong revision tiếp theo. Không sửa hai blob r2 đã neo băm trong lượt này.

KET_LUAN: changes_requested
