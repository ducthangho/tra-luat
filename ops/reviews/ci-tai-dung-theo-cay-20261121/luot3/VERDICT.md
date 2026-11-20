# Review đặc tả lượt 3 — CI-TAI-DUNG-THEO-CAY

**Kết luận chung: `changes_requested`.** Còn **6 P2 và 3 P3** trong R1–R9 dưới đây; không có P0/P1 được chứng minh trong lượt này. A r4 có thể approve riêng ở phạm vi văn bản; B1 r2 và B2 r2 cần revision. Không coi việc approve A là cho phép bật B2.

Reviewer: Codex, họ model OpenAI, độc lập với tác giả. Đây là review đặc tả, chưa có triển khai B1/B2. Chỉ đọc trong RV, không truy cập mạng, không đọc `.codex` hay memory; tất cả bản sao, kho Git thử, script và đầu ra mới nằm trong `RV/out/`. Dùng L1–L7 của **bản được đề bài chỉ định** `cay-kho/.claude/skills/soan-spec/SKILL.md` làm chuẩn đối chiếu; không thực hiện quy trình soạn spec/cấp lease/land.

## Neo đã kiểm

| Đối tượng | Giá trị |
|---|---|
| SHA-256 `SPEC-A-r4.md` | `0400723011a4a2f0362736de6872a177537e36aeb403e5a4ce59cf8bbd96dacc` |
| SHA-256 `SPEC-B1-r2.md` | `940f6a2e307ada5807d9a8b4f0ad204cd155d1e8f898f7c53ab8e63a0783e677` |
| SHA-256 `SPEC-B2-r2.md` | `17cfb8c2f3c81a918c7960cc83ec0abfda247c4fe36816a4dd448f2bea8ee1e1` |
| `cay-kho` HEAD | `45bae8d07a8cdf06a1ca9a7a2e015a6258169379` |
| HEAD tree | `30d5c7dec30dc658ae04ef29a6ffafe94eb8f197` |
| `origin/master` cục bộ | `a31c680c8880786848f832a35554d9e84078b270` — khác HEAD đóng gói; mọi kết luận về mã neo HEAD, không đổi nền |
| Lịch sử/working tree | Không shallow; `git status --porcelain` rỗng trước và sau kiểm |
| Môi trường | Windows; Python với `-S`, `PYTHONPATH=RV/py-lib`; PyYAML 6.0.3; tắt ghi bytecode |
| Thời điểm | 20-11-2026; thời điểm UTC từng lệnh trong `review-evidence/commands.jsonl` |

Băm các bản lượt 1/2 khớp verdict trước. Hai OID land ADR-0053/0055 qua đủ ba phép trên lịch sử HEAD: có tệp ở L (`rc=0`), chưa có ở L^1 (`rc=128`), L thuộc first-parent. Đây không thay thế việc fetch/đo lại ref lúc công bố trong tương lai. [Neo và số đo](review-evidence/20261120T155639245443.txt).

Script tái lập chính: [review_r3.py](review_r3.py), dùng lại [review_r2.py](review_r2.py), [review_probes.py](review_probes.py) của lượt trước; [review_tools.py](review_tools.py) ghi command/cwd/rc/output, đặt TEMP/TMP dưới `out/thu`, vô hiệu cấu hình Git người dùng. Nhãn `REAL`, `Y_*`, `REGISTRY`, `ACTUAL_GATE` chỉ hàm/mã thật được chạy; các nhãn `LITERAL`, `MODEL`, `R2_FIXED_REPLAY` là mô hình câu chữ đặc tả. **Không có kết quả Actions LIVE hay bộ triển khai tương lai nào được khai là đã chạy.** Những dòng đầu của probe `contract` cố ý chạy lại hợp đồng r1; kết quả r2 bắt đầu từ `R2_FIXED_*`.

## Trạng thái từng phát hiện lượt 2

| Finding | Trạng thái tại lượt 3 | Phép đo cùng loại và kết quả |
|---|---|---|
| N1 P2 — bóng/bật mâu thuẫn | **Đóng phản chứng cũ; còn lỗi mới của hợp đồng `bat`, R3/R4.** | `contract`: r1 chấm đúng lượt skipped thành rc 1; mô hình r2 có hai chế độ, đối chứng dương mỗi chế độ rc 0, sai kết quả rc 1. Tuy nhiên đối chứng này giả định đã có đủ instance; không chứng nhận hình dạng REST thật. |
| N2 P2 — thiếu chốt ghim | **Chưa đóng, R1.** | `pins`: YAML r2 có job biên nhận riêng và env thật. Sau tất cả họ chốt B1 đã nêu, vẫn đỏ `y04`, `y11`. B2: sau sửa các họ đã nêu trên nền B1 đã sửa, 15 guard y* và bốn hàm guard registry đều đạt. |
| N3 P2 — replay chỉ so nhóm | **Đóng lỗi so thiếu trường/tập rỗng cũ; chưa đóng Q8 và provenance, R2/R5.** | `contract`: đổi source, kế hoạch, source jobs, zip hash ⇒ rc 1; push jobs rỗng ⇒ rc 2. Nhưng lịch sử 20 lượt tốt + 1 lượt không artefact vẫn đạt dòng tổng D0 theo mục 1f. |
| N4 P2 — lỗi setup/upload ảnh hưởng bóng | **Đóng phần failure isolation đã nêu; phần latency còn R7 P3.** | `runtime_and_size`: tất cả bước push đã gọi tên đều COE; tổng timeout minh họa 23 < 30; receipt job COE, không job khác đọc output bóng hay needs receipt. Cấu hình này không tự bảo đảm thời điểm hoàn tất toàn lượt PR. |
| N5 P2 — A bỏ bảng/Bối cảnh | **Đóng.** | `a_check`: script trích A r4 trùng `tacgia/kiem_a.py`; ứng viên tự dựng rc 0; `table_exception` ⇒ A2 đỏ, `empty_background` ⇒ A6 đỏ. Các phản chứng protocol của F6 vẫn đỏ. |
| N6 P2 — mất sentinel None | **Đóng.** | `q7_consumer`: hàm thật vẫn trả None và kế hoạch fallback bằng nhau; predicate r2 loại một/hai None, nhận hai diff rỗng thật; truyền `manh` khôi phục đúng consumer. Fixture rename thật vẫn loại `nhanh`. |
| N7 P2 — đột biến cây không vào giao diện | **Đóng.** | `b2_tree_input`: dùng Git thật; giao diện cũ nhận cây artefact sửa tay vẫn rc 0; giao diện r2 nhận `tai_dung_cay` ⇒ baseline rc 0, cây sửa rc 1, đảo cha rc 1. |
| N8 P3 — L7 thiếu mã/payload | **Đóng các payload cũ; còn hai câu mới của B1, R8.** | `audit` + đọc ADR-0067: A:101 có E5; ba payload E5 đủ diff/lý do/quyền; B1 E1 và B2 E3 đã bổ sung phần thiếu. B1:103 và :198 vẫn nói việc duyệt mà chính câu không mang E. |
| N9 P3 — kích thước/vòng phụ thuộc | **Đóng ở mức đặc tả.** | `runtime_and_size`/`anchor`: B1 cộng đúng 455, xin 550 còn 95 dự phòng; B2 cộng 333 phù hợp “khoảng 335”. D0 chuyển sang trước merge B2, nên không còn phải dùng lệnh chưa tồn tại để cấp lease B2. `nang_tran` đủ bốn trường, chưa được coi là đã duyệt. |
| N10 P3 — contains và chuỗi lạ | **Đóng lời hứa sai cũ.** | `contract` vẫn cho thấy contains không kiểm toàn chuỗi; B2:102–103 đã thu hẹp lời hứa, B1:155–156/C2 bắt producer chuẩn. Đây là đóng lỗi hợp đồng, chưa chứng nhận implementation. R6 là lỗi khác ở ranh giới nhận output của bước hỏng. |

## Những F của lượt 1

| Finding | Trạng thái lượt 3 |
|---|---|
| F1 P1 | Giữ đóng. `rename` dựng lại phản chứng Git: before khác P1 bị loại; before=P1 thì diff PR/push chọn kế hoạch khác nhau nên không tái dùng `nhanh`. |
| F2 P2 | Còn mở ở B1, R1; phần thiếu consumer B2 của hai lượt trước đã được nêu đủ trong revision này. |
| F3 P2 | Giữ đóng ở mức thiết kế: C1/D1 yêu cầu chạy trực tiếp trên Windows theo M3; bước CI cũ vẫn Linux-only. Không khai đã chạy M3 cho mã chưa có. |
| F4 P2 | **Còn mở một phần, R5.** Attempt nguồn/schema/tập chỉ số đã sửa, giới hạn image `chuan-bi` đã được A khai công khai. Identity checkout và workflow definition thực chưa được hợp đồng mới chứng minh. |
| F5 P2 | Giữ đóng trong A: T4/P1/P2/R đã nhất quán. `policy_probe` vẫn xác nhận push hồ sơ là làn nhanh, packet-loop chạy. Mâu thuẫn mới nằm ở replay B2, R3. |
| F6 P2 | Đóng hoàn toàn phản chứng đã dựng. A4 giữ toàn bộ protocol; A2 bắt bảng/đoạn dư; A6 bắt Bối cảnh rỗng. A5 Git thật đúng hai đường dẫn; thêm tệp thứ ba bị nhận ra. |
| F7 P3 | Giữ đóng thiếu tiền đề cũ. `f7_closure`: diff khác nhưng kế hoạch hàm thật bằng nhau; C5 nay khai rõ đủ nhóm/attempt/image/diff trước khi chấm. C5 LIVE còn chưa đo. |
| F8 P2 | Chưa đóng toàn bộ: nguồn và từng trường được kiểm tốt hơn; nhưng Q8, fallback, job skipped và identity còn R2–R5. |
| F9 P3 | Đóng vấn đề ước 440/450 thiếu dư và vòng chờ cũ; xem N9. Numstat ứng viên chưa có, phải đo lại trước công bố. |
| F10 P3 | Phần thước đo A/L6 đã đóng; phần mỗi câu L7 còn R8. |

## Phát hiện còn mở và phát hiện mới

### R1 — P2 — B1 vẫn bỏ sót y11 và đường env của y04

**Vị trí:** `SPEC-B1-r2.md:59–65`, `:122–132`, `:161–165`. Mã: `ops/ci_duong_nhanh_test.py:2515–2534`, `:2849–2855`.

Job mới bắt buộc có `if: github.event_name == 'pull_request'`, trong khi `JOB_CO_IF_CHO_PHEP/y11` khóa tập và nguyên biểu thức của mọi job có if. B1 không liệt kê y11. Truyền `che_do` qua env vào `xet-tai-dung`/`bien-nhan-cay` còn bị `Y04_ENV_BUOC_CHE_DO/y04` chặn; danh sách B1 cũng thiếu họ này. Riêng y11 là xung đột tất yếu của job mới; y04 là xung đột của cách truyền env hợp lệ theo mục tiêu, cần chốt cách nối dữ liệu thay vì để executor tự phát hiện.

**Lệnh:** `python -S out/review_tools.py python out/review_r3.py pins` ⇒ rc 0 của harness. [Output đầy đủ](review-evidence/20261120T160248247621.txt).

```text
Y_BASE: 15/15 DAT
Y_B1_R2_AFTER_ALL_LISTED_FAMILIES: y04 DO, y11 DO
Y_B1_R2_AFTER_MISSING_Y04_Y11: 15/15 DAT
Y_B2_R2_AFTER_LISTED_FAMILIES_AND_FIXED_B1: 15/15 DAT
B2_REGISTRY_AFTER_LISTED: loi_gate_nhanh, loi_vung_thiet_lap,
                         loi_g5_workflow, loi_ruff_ci đều không lỗi
```

YAML chứng kiến: [B1](thu/b1-r2-witness.yml), [B2](thu/b2-r2-witness.yml). Harness cập nhật các bảng đã được đặc tả cho phép; với y10 cấp job và y06 của B2, chỉ thay đúng predicate ngoại lệ hẹp được nêu, không tắt guard. `y15` không được tính vì nó tự kiểm loader, không hợp lệ khi mock loader. Hai helper thật của t161 và t6 thật đều đạt trên baseline/B1/B2. Tám dấu vân Windows vẫn lệch trước cập nhật, đúng phạm vi B2 đã khai.

**Hướng sửa:** bổ sung y11/JOB_CO_IF_CHO_PHEP và y04/Y04_ENV_BUOC_CHE_DO vào B1, ghim đúng job/biểu thức/env mới; đột biến ngoại lệ rộng hơn phải đỏ. Những chốt này đều trong write set hiện có.

### R2 — P2 — Q8 có thể bỏ mất lượt chưa đo, và filter=latest che attempt bóng đã đỏ

**Vị trí:** `SPEC-B2-r2.md:81–97`, `:121`, `:143–146`, `:167`; nghĩa Q8 ở `SPEC-A-r4.md:246–248`.

Mục 1f chỉ chạy (a)–(e) cho lượt **có artefact**; lượt khác mang nhãn `khong_bien_nhan`. D0 chỉ khóa a/b và rc1/rc2, không khóa số lượt mang nhãn đó. Vì thế có thể giữ đủ danh sách run mà vẫn loại một lượt chưa đo khỏi mẫu chấm. Câu :167 xử lý artefact **quá hạn** thành rc2 chưa đóng đường artefact không được upload, bị mất hoặc bị xoá. C6 của B1 chỉ quan sát mười lượt đầu, không bảo vệ toàn giai đoạn bóng.

Jobs push còn dùng `filter=latest`, chỉ “ghi run_attempt”, không ràng bằng chứng push theo attempt bất biến hoặc xét attempt trước. Một lượt bóng có nhóm đã đánh dấu nhưng job failure ở attempt 1, rerun xanh ở attempt 2, không được giữ lại như một vi phạm Q8. Source PR bị khóa attempt 1 không giải quyết attempt của push.

**Lệnh:** `python -S out/review_tools.py python out/review_r3.py contract` ⇒ rc 0. [Output](review-evidence/20261120T160337635060.txt), [fixture lịch sử](thu/q8-history.json).

```text
twenty_good:                  a=20 b=20 rc1=0 rc2=0 D0=true
missing_21st_artifact:         a=20 b=20 rc1=0 rc2=0 khong_bien_nhan=1 D0=true
failed_21st_with_artifact:     a=20 b=21 rc1=1 rc2=0 D0=false
Q8_LATEST_ATTEMPT: attempt 1 failure, attempt 2 success;
                  chấm latest => a=21 b=21 rc1=0 rc2=0 D0=true
```

Đây là mô hình câu chữ, không phải dữ liệu API được quan sát. Nó chỉ ra nơi điều kiện phải được định nghĩa thêm, không khẳng định implementation tương lai chắc chắn chọn cách bỏ qua. Mô hình cũng đếm 20 bản ghi `bat` như 20 lượt bóng vì công thức chưa lọc chế độ; trước merge bình thường nguồn B1 chỉ phát `bong`, nhưng công cụ vẫn nên tự kiểm điều đó.

**Hướng sửa:** mỗi run/attempt trong danh sách đóng phải có một trạng thái chấm; mọi artefact thiếu/không đọc được ⇒ rc2, không loại khỏi mẫu. Neo danh sách đầy đủ, thời điểm cắt, workflow/bộ xét đã chạy, chế độ `bong` và attempt; đọc endpoint theo attempt hoặc từ chối push rerun trong bản đầu. Đòi D0 đỏ khi mất artefact, khi rerun che failure, và khi mode khác bong; không chỉ khi “bỏ sót lượt có artefact”.

### R3 — P2 — Chế độ bat chấm đỏ một push làn nhanh đúng chính sách

**Vị trí:** `SPEC-B2-r2.md:84–93`, `:123`, `:126`; đối chiếu `SPEC-B1-r2.md:134`, `SPEC-A-r4.md:250–251`.

Mục 1c đòi mọi job thuộc nhóm không tái dùng phải có mặt và **không skipped**. Nhưng làn `duong_nhanh` hiện hữu cho `gate-cong-cu` nghỉ cả job. B1 4a chủ ý không tái dùng làn này; B2 không sửa chính sách đó. D5 lại gọi replay cho cả mười lượt push đầu tiên, không giới hạn làn. Đột biến D2 “mọi skipped ngoài nhóm ⇒ rc1” cũng củng cố sai luật này.

**Lệnh:** `python -S out/review_tools.py python out/review_r3.py contract` ⇒ rc 0. [Output](review-evidence/20261120T160337635060.txt).

```text
classifier thật trên merge chỉ sửa hồ sơ:
  che_do=duong_nhanh; packet_loop=chay; rc=0
R2_BAT_FAST_LANE_EVEN_IF_EXPANDED: replay_rc=1
R2_BAT_EXISTING_FAST_LANE: forbidden_skipped=[gate-cong-cu], replay_rc=2
```

Dòng thứ hai cố ý cho đủ instance giả để tách lỗi luật “không skipped” khỏi lỗi hình dạng matrix ở R4. Ngoài ra, mục 1b chưa có nhánh dữ liệu cho **không tìm thấy nguồn**: khi fallback hợp lệ do không có PR receipt, không thể đòi nguồn/id zip/hai kế hoạch đầy đủ như một quyết định tái dùng dương rồi mặc nhiên coi tất cả là thiếu dữ liệu.

**Hướng sửa:** replay tính kết quả mong đợi theo chính sách nền của đúng event/làn rồi chỉ áp thay đổi tái dùng lên đó. Phân biệt `khong_tai_dung` có lý do kiểm lại được với `KHONG_DO_DUOC` của chính công cụ. Bổ sung đối chứng dương cho push hồ sơ, merge một cha, before khác P1, không có nguồn hợp lệ và image không khớp; nhóm không tái dùng không đồng nghĩa mọi job phải chạy.

### R4 — P2 — Đòi đủ instance Ubuntu của nhóm bị bỏ ở cấp job chưa khớp hợp đồng skipped

**Vị trí:** `SPEC-B2-r2.md:88–92`, `:100–103`, `:123`, `:125–126`.

Mục 1c dùng cùng yêu cầu “đúng tập chỉ số ma trận, job ubuntu-latest” cho `bong` và `bat`, trong khi mục tiêu 3 làm job nghỉ tại `jobs.<id>.if`. Job bị bỏ trước khi tạo instance ma trận không cung cấp tập shard đã chạy trên Ubuntu. Chính nền kho đã ghi trường hợp job phụ thuộc bị skipped mang tên trần, không tạo context `(ubuntu-latest)` (`ci.yml:94–95`); protocol :995 cũng phân biệt skipped chưa được cấp runner. Không được suy các instance đó đã tồn tại từ bảng ma trận.

**Lệnh:** `python -S out/review_tools.py python out/review_r3.py contract` ⇒ rc 0. [Output](review-evidence/20261120T160337635060.txt).

```text
R2_BAT_JOB_LEVEL_SKIP_SHAPE:
  nhóm cong_cu kỳ vọng 9 instance (8 shard + 1 gom)
  fixture trả 2 job-definition skipped, không shard
  replay_rc=2
```

Phản chứng này là fixture theo hình dạng job chưa nở matrix, **không phải lần gọi REST LIVE ở lượt review này**. Nó chứng minh đối chứng `bat` hiện viết với đủ instance giả không đủ để nghiệm thu đường tích hợp thật. C5 chạy bóng và D4 chỉ chạy lệnh `kiem-tai-dung`; chưa phép nào trước land xác nhận hình dạng skip mà D5 sẽ nhận.

**Hướng sửa:** định nghĩa riêng inventory cho mode bat: neo workflow/job definition, điều kiện skip và hình dạng REST thực khi không nở ma trận; vẫn đòi đủ shard cho nguồn PR và mode bong đã thực thi. Thêm phép đo trên workflow tạm thực sự bỏ job ở cấp job trước merge và đưa dữ liệu REST ấy vào fixture D2. Không tự tạo job/runner chưa hề tồn tại để làm đủ số.

### R5 — P2 — F4 còn mở: SHA biên nhận chỉ được kiểm dạng, blob tại M chưa là workflow-definition của nguồn

**Vị trí:** `SPEC-B1-r2.md:139–142`, `:157–160`; `SPEC-B2-r2.md:84–87`; đối chiếu `SPEC-A-r4.md:232–243`, `:253–254` và protocol :968–983.

4d kiểm `sha` là 40 hex, nhưng không kiểm commit ấy tồn tại và có parents/tree đúng lời khai. 4e tính lại cây của **M**, không ràng lại checkout SHA của nguồn. Replay tải lại ZIP và so toàn nội dung vẫn có thể lặp lại chính lời khai sai của ZIP; tải lại không trở thành nguồn chứng minh độc lập cho checkout.

Trường workflow mới chỉ là blob `ci.yml` tại **M**. Không trường/phép đo nào xác nhận exact workflow-definition commit/blob/hash của **run/attempt PR nguồn**, trong khi A G1 đòi định nghĩa workflow bằng nhau, Q6 giữ đủ bốn mốc. Việc thu bốn mốc khi ghi landed vẫn là nghĩa vụ riêng, chưa được hoàn tất bởi rc0 replay.

**Lệnh:** `python -S out/review_tools.py python out/review_r3.py provenance` ⇒ rc 0. [Output](review-evidence/20261120T160250342109.txt), [receipt thử](thu/receipt-nonexistent-sha.json).

```text
B1_4d_accepts=true với sha=ffffffffffffffffffffffffffffffffffffffff
git cat-file -e <sha>^{commit} trên kho fixture => rc=128
```

Các cha/cây trong fixture là giá trị Git thật; chỉ SHA checkout là sai. Các đột biến cũ attempt/schema/duplicate-shard nay đã bị loại; kết quả này không phủ nhận phần sửa đó. Không khẳng định đã làm giả được artefact trên GitHub: đây là phép thử răng của hợp đồng xác minh identity.

**Hướng sửa:** kiểm Git parents/tree của checkout SHA được neo; nếu object không còn thì phải có bằng chứng checkout có nguồn và phép kiểm được định nghĩa, không coi chuỗi hex là đạt. Thu/nhập workflow-definition đúng run/attempt qua cơ chế provenance sẵn có rồi so với push; chỉ rõ nơi lưu bốn mốc Q6 theo nhóm. Thêm đột biến SHA tồn tại nhưng sai cha/cây, SHA không tồn tại, workflow-definition nguồn khác/không đo được.

### R6 — P2 — Output dùng để bỏ job chưa ràng với outcome của bước xét

**Vị trí:** `SPEC-B1-r2.md:128–132`, `:154–160`; `SPEC-B2-r2.md:98–108`.

Bước xét dùng `continue-on-error: true`; B2 nối trực tiếp output của bước ấy ra job rồi dùng contains để bỏ các nhóm. Chưa quy định phải xét **outcome thực** của bước, hay thời điểm công bố quyết định so với lúc ghi xong bằng chứng. Một tiến trình ghi đủ output rồi lỗi/timeout ở đoạn cuối để lại output không rỗng dù bước hỏng; COE không xóa file output. `kiem-tai-dung` chỉ kiểm Git, không kiểm bước xét đã kết thúc thành công. D5 phát hiện sau land không phải cơ chế fallback lúc cấp job.

**Lệnh:** `python -S out/review_tools.py python out/review_r3.py runtime_and_size` ⇒ rc 0; tiến trình con thật ghi file rồi ném lỗi. [Output](review-evidence/20261120T160706936009.txt), [file output còn lại](thu/failed-evaluator-output.txt).

```text
evaluator rc=1; output tai_dung_bo=,ops, vẫn còn
job output = ${{ steps.xet-tai-dung.outputs.tai_dung_bo }}
checks_step_outcome=false; gate_ops_skipped_by_predicate=true
Git gate trên cha/cây/M thật vẫn rc=0
```

Đây là phản chứng tại ranh giới process/output và biểu thức YAML, không giả vờ đã chạy Actions. Nó khác ca HTTP/ZIP/None trả về trước khi phát output: lỗi ở sau khi ghi output hoặc do runner dừng bước không bảo đảm đi qua nhánh xóa output của Python.

**Hướng sửa:** chỉ xuất quyết định thật khi `steps.<id>.outcome == 'success'` và đủ trường chứng minh đã hoàn tất; dùng outcome, không dùng conclusion đã được COE chuyển màu. Ghi bằng chứng xong mới công bố output; thêm ca lỗi/timeout sau ghi output và kiểm các nhóm quay về chính sách chạy nền. Nếu upload là điều kiện của bằng chứng bền, khai rõ phải thành công trước khi output thật được chấp nhận.

### R7 — P3 — “Không làm chậm PR” vẫn rộng hơn điều bố trí job riêng chứng minh

**Vị trí:** `SPEC-B1-r2.md:52–54`, `:122–125`, `:176`, `:188–190`.

Job riêng và không needs chỉ loại dependency trực tiếp của các job nặng. Nó vẫn nằm trong lượt PR; thời điểm run chuyển completed là tối đa thời điểm kết thúc các job. Với PR làn nhanh hoặc receipt xếp hàng lâu, biên nhận có thể là job kết thúc cuối. C5 chỉ đo thời gian job đó, chưa có chuẩn nào làm tuyên bố “PR không chậm thêm” đỏ.

**Lệnh:** `python -S out/review_tools.py python out/review_r3.py runtime_and_size` ⇒ rc 0. [Output](review-evidence/20261120T160706936009.txt).

```text
Mô hình DAG hợp lệ: chuan-bi xong ở giây 30; các job cũ xong ở giây 90;
receipt chạy 299 giây (< timeout 5 phút), xong ở giây 329.
Hoàn tất lượt: 90 -> 329, tăng 239 giây; không job cũ nào needs receipt.
```

Những giây này là phản chứng mô hình, không phải thời gian CI đo thật. Phần lỗi setup/upload làm chuan-bi đỏ của N4 đã được sửa; xếp phần còn lại P3 vì chưa chứng minh một run thật bị chậm.

**Hướng sửa:** chốt đại lượng là thời gian check bắt buộc hay toàn run, nêu giới hạn chấp nhận và đo cả PR đầy đủ/làn nhanh cùng hàng đợi. Nếu giữ yêu cầu tuyệt đối không kéo dài toàn run, phải đổi vị trí thực thi phù hợp; không suy điều đó từ needs.

### R8 — P3 — Hai câu mới của B1 nói duyệt băm nhưng chưa mang E tại câu

**Vị trí:** `SPEC-B1-r2.md:103`, `:198`; chuẩn L7 trong skill được chỉ định.

`:103` “khối nang_tran … xin trần 550 cùng lần duyệt băm” và `:198` “550 … nếu chủ kho duyệt băm đặc tả này” không mang E tại chính câu. Khối đầu đã có E2 gộp E5 và payload đầy đủ; lỗi còn lại là tính tự đủ của từng câu theo L7, không phải tạo một ngưỡng hỏi mới. Câu lịch sử :261–262 có E2 ngay trong cùng câu nên không tính thêm.

**Lệnh:** `python -S out/review_tools.py python out/review_r3.py audit` ⇒ rc 0, các dòng `L7_SENTENCE`; đối chiếu bảng ADR-0067 :24–35. [Output](review-evidence/20261120T160101874786.txt).

**Hướng sửa:** gắn `(E2 gộp E5; hồ sơ ở nang_tran và pham_vi_e)` tại hai câu, hoặc bỏ sự lặp đó và dẫn thẳng điều kiện đã có mã. Payload E1/E2/E3/E5 còn lại của cả ba bản đã đủ; không cần hỏi chủ kho trong review này.

### R9 — P3 — B1 đếm năm bước mới nhưng chỉ định danh bốn

**Vị trí:** `SPEC-B1-r2.md:94`, `:128–132`, `:173`, `:188–189`.

Danh sách mục tiêu 3 gồm setup-python, cài PyYAML, xet-tai-dung và upload: **bốn** bước mới. Bước phân loại là bước cũ được giữ, còn receipt đã chuyển sang job riêng. “Cả năm bước”, bảng kích thước, C3 và C5 vẫn dùng năm mà không chỉ ra bước thứ năm là gì. Điều này làm phạm vi tổng timeout/đột biến COE không tự đủ theo L1/L3.

**Lệnh:** `python -S out/review_tools.py python out/review_r3.py runtime_and_size` ⇒ rc 0, `named_new_push_steps=4`. [Output](review-evidence/20261120T160706936009.txt). YAML chứng kiến thể hiện đủ bốn hành động được nêu; không tự thêm một bước mà đặc tả chưa định danh.

**Hướng sửa:** sửa đồng bộ số đếm thành bốn, hoặc nêu tên/nhiệm vụ bước thứ năm cùng timeout, COE, bảng ghim và phép đo. Nếu bước thứ năm là bước công bố output đã kiểm outcome theo R6, cần ghi rõ thay vì để suy đoán.

## Trích dẫn, lời khai mã và số đo

[citation-audit.json](citation-audit.json) lưu **47 mục đối chiếu neo dòng** gồm cả dẫn lại ở nhiều vị trí, trích nội dung thật và keyword mong đợi: tất cả khớp. Không đồng nhất “neo dòng đúng” với “danh sách consumer đủ”. Các neo đã kiểm gồm toàn bộ mốc protocol/classifier của A; doc_diff/ke_hoach, env registry, goi_that, y02/y03/y04/y06/y07/y10–y14/y16, các bảng ghim, t6, và các mốc registry/Windows của B1/B2. Lời khai t161 không có số dòng trong spec được kiểm riêng bằng hàm thật.

| Lời khai | Kết quả |
|---|---|
| Không đổi vùng mã giữa `94cbb36` và HEAD | `git diff --stat` đúng tập B1:236–238 rỗng. |
| Bốn nhóm/tám job | Đúng **8 định nghĩa job**, **37 instance Ubuntu** khi chạy đủ: 9 công cụ, 1 ops, 10 nhanh, 17 packet-loop; thêm gate và chuan-bi là 39. Job biên nhận mới ngoài nhóm. |
| Q4 không event/ref if trong nhóm | Quét cả cấp job và các bước nền: năm bước trực tiếp theo event/ref đều ở gate; các job nhóm không có event/ref if. Các điều kiện che_do/packet_loop không bị nhầm là event/ref. |
| Nguồn kế hoạch Q7 | Hàm thật, `--no-renames`, sentinel None, tham số `manh` và env YAML đúng neo; r2 đã gọi đúng consumer. |
| `goi_that` | Chạy hàm thật với opener giả: redirect nhận 200, request sang host khác không mang Authorization. Không kết nối mạng. Timeout 120 giây của mỗi request không tự chứng minh deadline tổng 120 giây; C2 phải giữ ca tổng timeout. |
| PyYAML trong chuan-bi | Import registry bằng `python -S` thiếu PYTHONPATH lỗi; thêm `RV/py-lib` thì đạt. Đây chỉ chứng minh phụ thuộc import; **không** đo image hệ thống GitHub có/không có PyYAML. Câu B1:48–49 cần đọc trong giới hạn đó; việc provision cụ thể vẫn hợp lý. |
| Job riêng không đụng t161 | Hai helper thật của t161 đều trả `[]` trên B1/B2. `strategy.matrix.os` không được thêm riêng; output mới vẫn là chuỗi. |
| G5/t6 và registry/Windows | Bước gate mới sau G5 ⇒ t6 thật đạt. B1 không làm đổi bốn guard registry đã kiểm. B2 sửa đủ các họ registry đã nêu thì đạt; tám fingerprint Windows trước sửa lệch đúng dự kiến. Chưa chạy trọn PowerShell suite của mã tương lai. |
| A “0 cổng” | 0 marker tại đủ sáu vị trí §20 mà ADR-0054 dùng, cộng classifier. Chỉ là đo các tên tính năng ở nền, không phải chứng minh mọi hành vi tương đương vắng mặt. |
| #674/#1343 | #674: ci.yml +90, classifier +618, test +3608, registry +1. #1343: +56/+29/+133/+8 = **226** ở bốn tệp được dẫn; khớp. |
| `nang_tran` | Parse YAML được; đúng bốn khóa `ai_nang`, `can_cu`, `tran_cu`, `tran_moi`. Chủ kho được nêu, có lý do không tách và numstat tham chiếu; cặp 6/450 → 6/550 đúng đơn vị ADR-0053. **550 là trần xin, chưa là quyền đã được cấp.** Khi có code phải đo numstat thật và chép khối vào lease theo ADR:34–44. |
| Lần đo 1, 147/79/25/44/10 và 8/8 | Khớp `DE-XUAT-20261116.md`. Không có đầy đủ dữ liệu run/log thô để tái tính độc lập; chỉ đối chiếu nguồn đã cấp. |
| Lần đo 2, 60/28 | Tái tính JSON: 60 lượt, 28 đầy đủ xanh; median wall 30,35 và runner 266,5 từ dữ liệu đã làm tròn. Bản tổng từ số gốc ghi 30,4/266,1, spec làm tròn 30,4/266; không coi độ chính xác khác nhau này là lỗi. |
| Nhóm/queue | 146,2+0,2=146,4; 25,3; 9,2+0,3+23,6=33,1; 41,5+0,2=41,7. Queue 2/878/123 khớp bản đo; chưa có job data thô để tự tính percentile. |
| Hồ sơ pr997 | `post_merge_checks` :42–53 thực sự tách run/attempt, checkout, workflow definition, gate output; không dùng REST head thay các mốc kia. |
| Lease, 366/367 nhánh, số ADR còn trống | Là số đo phía tác giả có thời điểm. Không đọc `D:/tlscan.git`, không mạng nên không xác minh trạng thái server hiện tại; phải quét lại trước cấp lease như spec đã yêu cầu. |
| Mặc định lưu artefact 90 ngày | Không có cấu hình dịch vụ hiện tại trong vật liệu để xác minh thời hạn thực; không dựa vào 90 ngày để chấm Q8. Hợp đồng thiếu dữ liệu phải đúng với mọi hạn lưu. |

## Kiểm L1–L7

| Luật | A r4 | B1 r2 | B2 r2 |
|---|---|---|---|
| L1 — con số đếm gì | Rõ tám Q, ba K, bốn phép chèn, hai tệp. | Dòng thêm và nhóm/job rõ; năm bước không khớp bốn hành động, R9. | Tám job/sáu tệp/20 lượt bóng/10 canary rõ; instance khi skipped cần R4. |
| L2 — mục tiêu/write set | Hai tệp đủ cho đổi văn bản. | Ba tệp đủ cho phần đo được nhưng danh sách chốt thiếu R1; chưa chứng minh phải thêm tệp thứ tư. | Sáu tệp bao các consumer đã đo; phải sửa mục tiêu replay/đầu ra trước thi hành. |
| L3 — phép làm đỏ | A2/A3/A4/A6 chạy trên nền/ứng viên/đột biến đúng màu; A1/A7 có mutant gate thật. | C2/C3 có bảng; còn đường lỗi sau output R6, latency R7. | D0 còn xanh giả R2; D5 đỏ oan R3/R4; cần thêm ca identity R5. |
| L4 — kế thừa | `khong_ap_dung` có lý do. | Có ghi lớp lỗi cũ. | Có ghi lớp lỗi cũ. Không có biên nhận packet khắc phục đã land mới nào buộc chép số đếm; revision draft không tự thành packet khắc phục. |
| L5 — thời điểm/đo lại | Neo mã/số đo có ngày; số server là chưa đo lại trong review offline. | Numstat tham chiếu đo lại khớp; 455 là ước. Trần 550 có điều kiện duyệt. | 333≈335 là ước; Q8 cần danh sách/attempt bất biến R2. |
| L6 — thước đo | Năm vế đã khai; A2 bắt bảng, A6 bắt K; ngắt dòng Q1 vẫn xanh; marker/zero-gate đo đủ vị trí. | Dòng N/N và marker được phân biệt; nội dung hậu kiểm giao B2. C6 chưa có LIVE. | Marker không thay identity; mode/rc và mẫu lịch sử chưa khép R2–R5. |
| L7 — hỏi chủ kho | Các câu hành động có E2/E5 và payload. | Khối nâng trần E2 gộp E5 đủ hồ sơ; còn :103/:198, R8. | E2/E3/E5 đủ mã và payload; không thấy ngân sách mềm hay ngưỡng “hai lượt chưa approve”. |

A1/A7 trên baseline và ứng viên đều rc 0; bỏ dòng §20 ⇒ adr-song rc 9; chép P1 vào adapter ⇒ doctrine-scan rc 6. A2/A3/A4/A6 trên baseline đều đỏ, trên ứng viên đều xanh; 19 đột biến nội dung trong probe đều đỏ, ngắt dòng Q1 giữ xanh. URL comment của ADR ứng viên là **giá trị giả để thử cú pháp offline**, không phải duyệt thật. [Output A](review-evidence/20261120T155901062422.txt).

## Bảng lệnh đã chạy

`RV=C:\r\d2`; `REPO=RV/cay-kho`. Các lệnh wrapper gọi từ RV; cột cwd ghi nơi lệnh con chạy. Rc 0 của probe chỉ có nghĩa harness chạy xong, không có nghĩa đặc tả đạt. Rc con của các đối chứng âm được lưu trong output. Lệnh đọc ban đầu trước khi dựng wrapper và thao tác tạo bản sao đều ở RV, rc 0: đọc PROMPT, ba spec mới, hai verdict cũ, skill chuẩn, các script lượt 2 và ADR; `rg --files` đã loại `.codex`. Không thực thi lệnh tác giả tại `tacgia/`.

<!-- COMMAND_TABLE_BEGIN -->
| # | Lệnh (từ RV) | cwd lệnh con | rc | Kết luận và bằng chứng |
|---|---|---|---|---|
| B1 | <code>Get-Content -LiteralPath 'C:\r\d2\PROMPT.md' -Raw</code> | RV | 0 | Đọc đầy đủ phạm vi và yêu cầu trước khi làm. Output đọc ban đầu ở transcript công cụ. |
| B2 | <code>rg --files -g '!cay-kho/**' -g '!py-lib/**' -g '!.codex/**' -g '!out/**'</code> | RV | 0 | Liệt kê vật liệu trong RV. Output đọc ban đầu ở transcript công cụ. |
| B3 | <code>Get-Content VERDICT-luot2.md -Raw; Get-Content VERDICT-luot1.md -Raw</code> | RV | 0 | Hai lệnh đọc riêng; sau đó đọc lại các phần cần thiết có số dòng qua wrapper. Output đọc ban đầu ở transcript công cụ. |
| B4 | <code>Get-Content cay-kho/.claude/skills/soan-spec/SKILL.md -Raw</code> | RV | 0 | Đọc chuẩn L1–L7 được đề bài chỉ định. Output đọc ban đầu ở transcript công cụ. |
| B5 | <code>$n=0; Get-Content SPEC-<A-r4&#124;B1-r2&#124;B2-r2>.md &#124; ForEach-Object { $n++; '{0,4} {1}' -f $n, $_ }</code> | RV | 0 | Ba lệnh riêng đọc ba bản mới có số dòng; đọc tiếp phụ lục A từ dòng 208. Output đọc ban đầu ở transcript công cụ. |
| B6 | <code>Get-Content luot2/out/review_tools.py -Raw; Get-Content luot2/out/review_r2.py; Get-Content luot2/out/review_probes.py</code> | RV | 0 | Các lần đọc riêng kiểm script trước khi sao/chạy; đọc tiếp phần còn lại của review_r2. Output đọc ban đầu ở transcript công cụ. |
| B7 | <code>Get-Content cay-kho/docs/adr/0053-tran-kich-thuoc-sensitive-len-sau-tep.md -Raw; Get-Content cay-kho/docs/adr/0067-danh-sach-dong-va-uy-quyen-thuong-truc.md -Raw</code> | RV | 0 | Đọc hợp đồng nâng trần và mã E; sau đó đọc lại đoạn liên quan bằng wrapper. Output đọc ban đầu ở transcript công cụ. |
| B8 | <code>New-Item -ItemType Directory -Force -Path out,out/thu,out/review-evidence; Copy-Item luot2/out/{review_tools.py,review_probes.py,review_r2.py} -Destination out</code> | RV | 0 | Dòng rút gọn mô tả hai lệnh chuẩn bị: chỉ tạo thư mục và chép ba script trong out; không chạy bản gốc. Output đọc ban đầu ở transcript công cụ. |
| 1 | <code>python -S out/review_tools.py 'hash' 'SPEC-A-r4.md' 'SPEC-B1-r2.md' 'SPEC-B2-r2.md'</code> | RV | 0 | Neo/kiểm lại SHA-256 ba đặc tả; khớp giá trị đã review. [Output](review-evidence/20261120T155623784154.txt) |
| 2 | <code>python -S out/review_tools.py 'read' 'cay-kho/ops/ci_duong_nhanh_test.py@45:115' 'cay-kho/ops/ci_duong_nhanh_test.py@2440:2635' 'cay-kho/ops/ci_duong_nhanh_test.py@2700:2760' 'cay-kho/ops/ci_duong_nhanh_test.py@2820:3010'</code> | RV | 0 | Đọc/tìm/đối chiếu vật liệu; không sửa nguồn. [Output](review-evidence/20261120T155636200314.txt) |
| 3 | <code>python -S out/review_tools.py 'read' 'cay-kho/docs/adr/0053-tran-kich-thuoc-sensitive-len-sau-tep.md@1:100' 'cay-kho/docs/adr/0067-danh-sach-dong-va-uy-quyen-thuong-truc.md@20:58' 'cay-kho/.github/workflows/ci.yml@1:190' 'cay-kho/ops/ci_provenance.py@1:125'</code> | RV | 0 | Đọc/tìm/đối chiếu vật liệu; không sửa nguồn. [Output](review-evidence/20261120T155636653536.txt) |
| 4 | <code>python -S out/review_tools.py 'python' 'out/review_r2.py' 'anchor'</code> | RV | 0 | Băm bản cũ, HEAD/tree/ref, trạng thái sạch, ADR land, numstat tham chiếu và số đo JSON. [Output](review-evidence/20261120T155639245443.txt) |
| 5 | <code>python -S out/review_tools.py 'read' 'cay-kho/ops/ci_duong_nhanh_test.py@2840:3010' 'cay-kho/docs/adr/0053-tran-kich-thuoc-sensitive-len-sau-tep.md@1:96' 'cay-kho/docs/adr/0067-danh-sach-dong-va-uy-quyen-thuong-truc.md@24:42'</code> | RV | 0 | Đọc/tìm/đối chiếu vật liệu; không sửa nguồn. [Output](review-evidence/20261120T155649852681.txt) |
| 6 | <code>python -S out/review_tools.py 'rg' 'skipped.*(matrix&#124;ma trận&#124;ma tran&#124;ten TRAN)&#124;ten TRAN.*skipped&#124;job.*if.*matrix&#124;if.*ma trận&#124;khong_bien_nhan' '.github' '.claude/dev' 'ops' 'docs' '-g' '*.py' '-g' '*.md' '-g' '*.yml' '-g' '!ops/specs/**' '-g' '!ops/reviews/**' '-g' '!ops/land/**'</code> | REPO | 0 | Đọc/tìm/đối chiếu vật liệu; không sửa nguồn. [Output](review-evidence/20261120T155711452572.txt) |
| 7 | <code>python -S out/review_tools.py 'read' 'VERDICT-luot1.md@70:205' 'cay-kho/.claude/dev/ci_dang_ky_test.py@560:680' 'cay-kho/.claude/dev/ci_dang_ky_test.py@830:915' 'cay-kho/docs/PROTOCOL_DA_PHIEN.md@965:1018'</code> | RV | 0 | Đọc/tìm/đối chiếu vật liệu; không sửa nguồn. [Output](review-evidence/20261120T155732316390.txt) |
| 8 | <code>python -S out/review_tools.py 'python' 'out/review_r2.py' 'rename'</code> | RV | 0 | Fixture Git F1: before=P1 không cứu được kế hoạch khác; loại nhanh đúng. [Output](review-evidence/20261120T155851027373.txt) |
| 9 | <code>python -S out/review_tools.py 'python' 'out/review_r3.py' 'pins'</code> | RV | 0 | Guard thật trên YAML r2; B1 còn y04/y11; B2 sau sửa các họ đã nêu đạt. Fingerprint Windows. [Output](review-evidence/20261120T155852030920.txt) |
| 10 | <code>python -S out/review_tools.py 'python' 'out/review_r3.py' 'q7_consumer'</code> | RV | 0 | Sentinel None thật; r2 loại một/hai lỗi, giữ diff rỗng và tham số manh. [Output](review-evidence/20261120T155852587959.txt) |
| 11 | <code>python -S out/review_tools.py 'python' 'out/review_r3.py' 'a_check'</code> | RV | 0 | Nền đỏ/ứng viên xanh; 19 đột biến nội dung đỏ, reflow xanh; adr-song/doctrine-scan và mutant thật. [Output](review-evidence/20261120T155901062422.txt) |
| 12 | <code>python -S out/review_tools.py 'rg' 'tai_dung&#124;outcome&#124;conclusion&#124;nguyên tử&#124;atomic&#124;timeout&#124;120&#124;goc&#124;dau' '../SPEC-B1-r2.md' '../SPEC-B2-r2.md'</code> | REPO | 0 | Đọc/tìm/đối chiếu vật liệu; không sửa nguồn. [Output](review-evidence/20261120T155925087826.txt) |
| 13 | <code>python -S out/review_tools.py 'python' 'out/review_r3.py' 'contract'</code> | RV | 0 | Đối chứng hai mode/so trường; Q8 thiếu artefact, rerun, fast lane và skipped matrix. [Output](review-evidence/20261120T160100208944.txt) |
| 14 | <code>python -S out/review_tools.py 'python' 'out/review_r3.py' 'audit'</code> | RV | 0 | Neo dòng, inventory, marker 0 cổng, import PyYAML và câu L7. [Output](review-evidence/20261120T160101874786.txt) |
| 15 | <code>python -S out/review_tools.py 'python' 'out/review_r3.py' 'runtime_and_size'</code> | RV | 0 | Bóng/timeout/needs; process lỗi sau output; DAG latency; nang_tran và ước kích thước. [Output](review-evidence/20261120T160103863945.txt) |
| 16 | <code>python -S out/review_tools.py 'python' 'out/review_r3.py' 'b2_tree_input'</code> | RV | 0 | Git thật: cây truyền vào r2 sửa thì rc 1, baseline rc 0. [Output](review-evidence/20261120T160106476345.txt) |
| 17 | <code>python -S out/review_tools.py 'python' 'out/review_r2.py' 'a_write_set'</code> | RV | 0 | A5 bằng Git thật: ứng viên/đột biến vẫn hai tệp, thêm tệp thứ ba thì ba đường dẫn. [Output](review-evidence/20261120T160124242237.txt) |
| 18 | <code>python -S out/review_tools.py 'read' 'bang-chung/do-master-20261120.txt' 'DE-XUAT-20261116.md@1:165' 'cay-kho/ops/land/pr997-wp978-land-evidence.yaml@1:115'</code> | RV | 0 | Đọc/tìm/đối chiếu vật liệu; không sửa nguồn. [Output](review-evidence/20261120T160124772804.txt) |
| 19 | <code>python -S out/review_tools.py 'python' 'out/review_r2.py' 'f7_closure'</code> | RV | 0 | Fixture F7 cũ: diff khác nhưng kế hoạch thực bằng nhau; tiền đề C5 đã sửa. [Output](review-evidence/20261120T160127409312.txt) |
| 20 | <code>python -S out/review_tools.py 'rg' '_kiem_tra_nguon_duy_nhat_os_ci&#124;def t161&#124;bien-nhan-cay&#124;head_repository&#124;workflow.definition&#124;oid_dinh_nghia' 'ops/lease_publish_test.py' 'ops/ci_provenance.py' '-g' '*.py'</code> | REPO | 0 | Đọc/tìm/đối chiếu vật liệu; không sửa nguồn. [Output](review-evidence/20261120T160128701326.txt) |
| 21 | <code>python -S out/review_tools.py 'read' 'cay-kho/ops/lease_publish_test.py@8495:8548' 'cay-kho/ops/lease_publish_test.py@8625:8662' 'cay-kho/.claude/dev/ci_dang_ky_test.py@1415:1534' 'cay-kho/ops/cong_cu_test.py@335:387'</code> | RV | 0 | Đọc/tìm/đối chiếu vật liệu; không sửa nguồn. [Output](review-evidence/20261120T160137149288.txt) |
| 22 | <code>python -S out/review_tools.py 'read' 'DIFF-B1-r1-r2.patch' 'DIFF-B2-r1-r2.patch'</code> | RV | 0 | Đọc/tìm/đối chiếu vật liệu; không sửa nguồn. [Output](review-evidence/20261120T160247590724.txt) |
| 23 | <code>python -S out/review_tools.py 'python' 'out/review_r3.py' 'pins'</code> | RV | 0 | Guard thật trên YAML r2; B1 còn y04/y11; B2 sau sửa các họ đã nêu đạt. Fingerprint Windows. [Output](review-evidence/20261120T160248247621.txt) |
| 24 | <code>python -S out/review_tools.py 'python' 'out/review_r3.py' 'provenance'</code> | RV | 0 | SHA checkout không tồn tại vẫn qua 4d; hàm redirect thật thử offline, không chuyển token. [Output](review-evidence/20261120T160250342109.txt) |
| 25 | <code>python -S out/review_tools.py 'python' 'out/review_r3.py' 'ancillary'</code> | RV | 0 | Hai helper t161 và t6 thật đạt nền/B1/B2; SyntaxWarning từ AST mã nền không làm sai phép đo. [Output](review-evidence/20261120T160251079386.txt) |
| 26 | <code>python -S out/review_tools.py 'python' 'out/review_r3.py' 'contract'</code> | RV | 0 | Đối chứng hai mode/so trường; Q8 thiếu artefact, rerun, fast lane và skipped matrix. [Output](review-evidence/20261120T160337635060.txt) |
| 27 | <code>python -S out/review_tools.py 'git' 'status' '--porcelain'</code> | REPO | 0 | Đọc trạng thái/HEAD/tree; working tree sạch, neo không đổi. [Output](review-evidence/20261120T160704780356.txt) |
| 28 | <code>python -S out/review_tools.py 'hash' 'SPEC-A-r4.md' 'SPEC-B1-r2.md' 'SPEC-B2-r2.md'</code> | RV | 0 | Neo/kiểm lại SHA-256 ba đặc tả; khớp giá trị đã review. [Output](review-evidence/20261120T160705345870.txt) |
| 29 | <code>python -S out/review_tools.py 'python' 'out/review_r3.py' 'runtime_and_size'</code> | RV | 0 | Bóng/timeout/needs; process lỗi sau output; DAG latency; nang_tran và ước kích thước. [Output](review-evidence/20261120T160706936009.txt) |
| 30 | <code>python -S out/review_tools.py 'git' 'rev-parse' 'HEAD' 'HEAD^{tree}'</code> | REPO | 0 | Đọc trạng thái/HEAD/tree; working tree sạch, neo không đổi. [Output](review-evidence/20261120T160707639731.txt) |
| Cuối | `python -S out/finalize_review.py` | RV | 0 | Sinh bảng từ nhật ký; kiểm băm, số finding, đầy đủ N/F, liên kết, kết luận. [Validation](review-evidence/report-validation.json) |
<!-- COMMAND_TABLE_END -->

## Kết luận cuối

Approve riêng **A r4** ở phạm vi sửa văn bản và các tiêu chí đã kiểm. **B1 r2 và B2 r2: changes_requested**. Cần đóng R1–R6 trước khi approve bộ ba; R7–R9 là P3 còn mở. `nang_tran` đúng hình thức, nhưng review này không cấp quyền trần 550 hay thay quyết định chủ kho. Không có yêu cầu hỏi/chờ xác nhận nào được đặt thêm bởi reviewer.

KET_LUAN: changes_requested
