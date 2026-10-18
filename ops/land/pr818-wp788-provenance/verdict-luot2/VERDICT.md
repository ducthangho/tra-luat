verdict: changes_requested

# Cross-review lượt 2 — wp788

Đang xác minh preflight và chạy review phân lớp theo prompt.snapshot.
Provider: OpenAI; execution surface: Codex agent với công cụ shell cục bộ; transport: tool-mediated. Không phải ChatGPT Web/human-mediated.

## Preflight

- HEAD đúng `4ffae005eb1c434d660cbfb713ad21ed92115a8a`; tree `f6aeed236145682acc26dbb310f0cada5f6f33d8`; detached, origin `https://github.com/ducthangho/tra-luat`.
- `sha256sum .review/SPEC.md .review/VERDICT_LUOT1.md` rc=0: lần lượt `82dc170446c3a4431739a3effbec8cb55adadc13d69f5c510f8782a2b45eb54e` và `a56b90bafebf4e1669b60d148b359ed5e88b6b345ac650d42c3bac44be4208d3` (khớp).
- Spec r1; nhánh executor ghi trong lịch sử merge là `agent/wp788-r1-g1-claude` (g1). Authority cho review offline và tiếp tục sau checkpoint H3=4 là assignment `prompt.snapshot`, SHA-256 `d6ac787a253e83139975bae0fe6ee54de779b4fd0bfcd74fb918b8d1c41555be`. Không đo lại lease/state/refs trên máy chủ vì assignment cấm mạng/GitHub; không nhận prompt là lease viết hay quyền land.
- Effective write set sản phẩm: `.claude/dev/packet_loop.py`, `.claude/dev/packet_loop_test.py`; Review Class `sensitive`; reviewer chỉ ghi `.review/VERDICT.md` và `.review/suite.out` được assignment yêu cầu, mọi scratch ngoài kho.
- Cặp khai báo: executor `anthropic_claude / claude-opus-5-5 / claude_code / machine/local`, họ `claude` (spec; chưa được cấp runtime receipt executor để đo lại). Reviewer `openai_codex / codex_cli / machine`, họ `openai`; header đúng run `b211e5387ca246dc9ba646e14f7a6a4d`: Codex v0.163.0, `model: gpt-6.1-sol`, `reasoning effort: xhigh`, session `01a14c65-44bf-7641-a8fe-e3d60a4c942d`. Header chỉ là CLI công bố, không chứng minh model từng request. Context reviewer mới; không dùng context executor.
- Runtime Linux, Python 3.13.16, core.abbrev=7, ripgrep 15.2.0. Sandbox `workspace-write`, không giả OS read-only. `doctor/chuan-bi` không chạy vì có hoạt động mạng/credential ngoài assignment; capability cần dùng đo trực tiếp bằng Git/Python/bash.
- Suite đã khởi chạy sớm: `python -B .claude/dev/packet_loop_test.py > .review/suite.out 2>&1`, exec session `41695`; pending, chưa tính pass.
- Scratch: `/tmp/wp788-r2.AITtnb`. Snapshot `start.json`: Git HEAD/tree, diff/index đều rc=0; diff/index rỗng; untracked chỉ `.review/*`, ignored `.codex/`. Băm 3680 tệp tracked không nhạy cảm; không đọc 2 tên nhạy cảm để tạo cleanliness claim. Snapshot này lấy sau bootstrap suite; phạm vi quan sát là checkout được giao, không phải kho executor nguồn.

## Lớp A — ĐỐI CHIẾU LƯỢT TRƯỚC

Fixture được dựng bằng `python -B -c 'import json,pathlib; …'` ngoài kho (JSON nguyên văn lưu ở scratch). Dùng lại cấu trúc probe F01/F02 lượt 1: head=`"ab"*20`, id=1, total_count=1, suite=1, status=completed, conclusion=success. Command/argv/output đầy đủ, kể cả đối số 4301 chữ số, ở `/tmp/wp788-r2.AITtnb/layer-a.json`.

Command chung (mỗi ca một subprocess độc lập):

```bash
python -B .claude/dev/packet_loop.py kiem-gate --head abababababababababababababababababababab --check-suite <suite> --bat-buoc gate [--bat-buoc gate2] --check-runs /tmp/wp788-r2.AITtnb/<case>.json
```

**identity-suite-conflict** — suite=`1`; rc=12

```text
KHÔNG ĐO ĐƯỢC: /tmp/wp788-r2.AITtnb/identity-suite-conflict.json: id 1 mang hai danh tính ('gate', 1, 'abababababababababababababababababababab') và ('gate', 9, 'abababababababababababababababababababab') — bằng chứng mâu thuẫn
```

**identity-name-conflict** — suite=`1`; rc=12

```text
KHÔNG ĐO ĐƯỢC: /tmp/wp788-r2.AITtnb/identity-name-conflict.json: id 1 mang hai danh tính ('gate', 1, 'abababababababababababababababababababab') và ('khac', 1, 'abababababababababababababababababababab') — bằng chứng mâu thuẫn
```

**identity-two-required** — suite=`1`; rc=12

```text
KHÔNG ĐO ĐƯỢC: /tmp/wp788-r2.AITtnb/identity-two-required.json: id 1 mang hai danh tính ('gate', 1, 'abababababababababababababababababababab') và ('gate2', 1, 'abababababababababababababababababababab') — bằng chứng mâu thuẫn
```

**identity-name-suite-pages** — suite=`1`; rc=12

```text
KHÔNG ĐO ĐƯỢC: /tmp/wp788-r2.AITtnb/identity-name-suite-pages.json: id 1 mang hai danh tính ('gate', 1, 'abababababababababababababababababababab') và ('gate', 9, 'abababababababababababababababababababab') — bằng chứng mâu thuẫn
```

**same-id-consistent-pages** — suite=`1`; rc=0

```text
gate XANH trên abababababababababababababababababababab (suite 1): gate id=1
```

**long-suite** — suite=`"1"*4301`; rc=12

```text
CẢNH BÁO: 'gate' có 1 run ở suite khác (1) — bỏ qua
  ĐỎ  'gate': VẮNG — không check-run nào mang đúng tên này trong suite 11111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111
gate KHÔNG xanh trên abababababababababababababababababababab: 1/1 tên bắt buộc đỏ
```

**same-id-same-suite-failure** — suite=`1`; rc=12

```text
  ĐỎ  'gate' id=1: status='completed' conclusion='failure' head_sha='abababababababababababababababababababab'
gate KHÔNG xanh trên abababababababababababababababababababab: 1/1 tên bắt buộc đỏ
```

| Finding lượt 1 | Kết luận trên head hiện tại | Đo độc lập |
|---|---|---|
| F01 `check-run-id-identity-conflict`, P1, H3 | **ĐÃ ĐÓNG / ĐÃ VÁ THẬT** đối với các biểu hiện lượt trước | Bốn probe mâu thuẫn đều 12 + KHÔNG ĐO ĐƯỢC; một ID hai tên bắt buộc không còn xanh. Duplicate nhất quán nhiều trang vẫn 0; conflict conclusion cùng identity vẫn 12. Kết luận toàn lớp chờ lớp C. |
| F02 `check-suite-decimal-conversion-limit`, P3 | **ĐÃ ĐÓNG / ĐÃ VÁ THẬT** đối với probe lượt trước | Suite 4301 chữ số: rc=12 + VẮNG, không Traceback; không đổi thành suite 1. Kiểm đường dự phòng tiếp ở C/D. |

## Lớp B — Diff MỚI

Đã đọc toàn bộ `git diff e995730464da03223cf636e49ad32e220c6ec720 HEAD -- .claude/dev` (rc=0). Mã mới chỉ thêm chốt identity trước lọc, tách regex khỏi int/catch; tests thêm 5 ca F01, 1 ca F02, 5 mutant mới và cập nhật 2 mutant bị ảnh hưởng. Không sửa máy trạng thái/lệnh khác. Raw command/rc/output: `/tmp/wp788-r2.AITtnb/layer-b.json`.

`git diff --numstat d347d426334bbe1bbb1161184ab0acffee9be054 HEAD` rc=0

```text
52	10	.claude/dev/packet_loop.py
243	16	.claude/dev/packet_loop_test.py
```

`git diff d347d426334bbe1bbb1161184ab0acffee9be054 HEAD --stat` rc=0

```text
 .claude/dev/packet_loop.py      |  62 ++++++++--
 .claude/dev/packet_loop_test.py | 259 +++++++++++++++++++++++++++++++++++++---
 2 files changed, 295 insertions(+), 26 deletions(-)
```

`git diff --name-status d8b15cb0730c85e7019aee627c3bfa645a6d3eaf d347d426334bbe1bbb1161184ab0acffee9be054` rc=0

```text
M	.claude/skills/soan-spec/SKILL.md
```

`git diff e995730464da03223cf636e49ad32e220c6ec720 49a47badfefb944a7bb4f037c0a34e78f77355b9 --stat` rc=0

```text
 .claude/skills/soan-spec/SKILL.md | 56 +++++++++++++++++++++++++++++++++++++--
 1 file changed, 54 insertions(+), 2 deletions(-)
```

`git diff --check d347d426334bbe1bbb1161184ab0acffee9be054 HEAD` rc=0

```text
```

**Đo thực: 2 tệp, 295 dòng thêm / 26 dòng xoá**, trong trần ≤3 tệp / ≤300 thêm (còn 5 dòng thêm). Hai path đúng write set. Parents merge `49a47badfefb944a7bb4f037c0a34e78f77355b9` là head lượt 1 và `d347d426334bbe1bbb1161184ab0acffee9be054`; delta từ head lượt 1 đến merge chỉ `.claude/skills/soan-spec/SKILL.md`, cùng path với delta baseline cũ→d347. Diff d347→HEAD chỉ hai tệp write set, không có nội dung merge ngoài drift đã khai.

## Lớp C — Săn H3 trên code mới

`PYTHONDONTWRITEBYTECODE=1 python -B /tmp/wp788-r2.AITtnb/probe_c.py "$PWD"` rc=0:

```text
PROBES 99 PASS 99 UNEXPECTED 0
```

Đây là probe độc lập trên JSON + CLI, không mock code sản phẩm. Dữ liệu, argv, runtime int limit, rc/stdout/stderr từng lần ở `layer-c.json`, script ở scratch. Phủ từng trường identity, đảo thứ tự, một/nhiều trang, run không bắt buộc; trạng thái/kết luận ở từng bản trùng được chọn; mutable state của id cũ; metadata không dùng; bool/string; số suite 639/640/641/4300/4301/6000 chữ số dưới runtime limit 640/4300/0; số suite sai dạng. Hai probe kiểu check_suite dùng trùng tên artifact đầu vào (bool/string); cả hai subprocess đã chạy, raw output được giữ; artifact bool sẽ tái dựng riêng bên dưới, không dùng file đã ghi đè làm bằng chứng bytes của lượt bool.

| Trường/đầu vào lệnh thực đọc để quyết XANH | Chốt danh tính / kiểm độc lập | Đánh giá đường vào H3 |
|---|---|---|
| CLI `head` | Regex 40 hex thường; đối chiếu `head_sha` từng run được chọn | Identity có `head_sha`; không lọc mất bản ghi cùng id đổi head |
| CLI `check_suite` | ASCII regex trước int; `ValueError` chỉ bọc int | Identity có `check_suite.id`; sau schema chỉ int không bool |
| CLI `bat_buoc` | argparse required append, khử trùng giữ thứ tự, cấm tên rỗng, so tên tuyệt đối | Identity có `name`; một id không thể chứng minh hai tên |
| JSON shape: root/trang/`check_runs` | Decoder cấm khóa trùng/hằng ngoài JSON; mọi trang và mọi phần tử phải đúng dạng trước identity | Không bỏ qua run ngoài danh sách; KeyError không thể thay schema hợp lệ trên code gốc |
| `total_count` từng trang | int không bool, ≥0, các trang bằng nhau; số id phân biệt bằng đúng count | Đây là thuộc tính trang, không phải identity. Chốt identity trước đếm không thay chốt count; lỗi nào cũng trả 12 |
| run `id` | int không bool; khóa map identity; max id sau lọc; xét mọi bản trùng của max | Được dùng làm khóa (không cần lặp trong tuple). Bool/float không đồng nhất được với id thật nhờ schema |
| run `name`, `check_suite.id`, `head_sha` | Tuple `(name, check_suite.id, head_sha)` của TẤT CẢ runs trước lọc, bất kể trang/tên bắt buộc/id mới hay cũ | Ba trường identity dùng để lọc hoặc đối chiếu head đều được chốt; 24 probe identity biến thể đều 12 với lý do đúng |
| run `status` | `== completed` trên mọi bản trùng của max id | Không thuộc identity vì là trạng thái biến đổi; không bị lọc theo status; bản không completed còn nguyên và làm đỏ |
| run `conclusion` | `== success` trên mọi bản trùng của max id | Không thuộc identity vì là trạng thái biến đổi; không chọn success trước max; failure/null/neutral của bản trùng mới đều đỏ |

Không có trường quyết định xanh nào khác: cảnh báo đọc name/suite/id để in, không sửa `do`/`xanh`; `state_dir` không dùng trong lệnh. Metadata/app không dùng và không đưa vào tuple. Không phát hiện đường H3 mới qua F01/F02 trong phạm vi này; **H3 giữ 4**, không tăng 5. Không yêu cầu trạng thái cũ xanh khi đã có id mới thành công (luật rerun hiện hành).

F02 giữ nguyên chuỗi khi int thất bại; chuỗi không bằng bất kỳ int nào qua schema. Với số dài ở evidence: runtime mặc định từ chối JSON và trả 12 có kiểm soát; với `PYTHONINTMAXSTRDIGITS=0`, JSON/int cùng đọc được số 4301 chữ số, cùng suite thực sự xanh, không bị fallback chặn oan. `except` không bao quanh đọc file/identity nên không nuốt lỗi evidence. Cả hai hướng đều đã đo ở `long-evidence-default` / `long-evidence-unlimited`.

Đối chiếu cuối lớp cũ: F01 và F02 **ĐÃ ĐÓNG / ĐÃ VÁ THẬT**, không có biểu hiện mới cùng cơ chế tìm được qua probe trên. Tỷ lệ chuyển tiếp U={H3, cli-decimal-conversion-unhandled}, F=U: **2/2=100%**; không coi tỷ lệ này là approval.

Tái dựng artifact bool riêng: `typed-check-suite-bool-preserved.json`; lệnh/rc/output ở `layer-c-bool-preserved.json`; rc=12

```text
KHÔNG ĐO ĐƯỢC: /tmp/wp788-r2.AITtnb/c-inputs/typed-check-suite-bool-preserved.json: trang 0 check_runs[1] `check_suite` không phải object có `id` số nguyên: {'id': True}
```

## Lớp D — Audit TOÀN BỘ bảng đột biến một lượt

Command: `bash .review/mut_all.sh "$PWD/.claude/dev" kg_ /tmp/wp788-r2.AITtnb/mutants > /tmp/wp788-r2.AITtnb/mut_all.out 2>&1`, exec session 76631, **exit_code=0**. Mỗi mutant một bản sao/một subprocess; runner dùng `python -B`, `PYTHONDONTWRITEBYTECODE=1`; không có `.pyc`/setup/import lỗi trong thư mục output. Rc shell chỉ là completion của script; verdict dựa trên từng thông điệp ca đích.

Đã parse và đọc từng thông điệp, đối chiếu khóa mutant và tập ca với catalog hiện tại; không thiếu/đúp ca. **39 mutant / 92 ô: 0 sống; 91 ô đổi đúng mã/nội dung, 1 ô traceback (không cấp tín dụng giết theo spec).** `mutation-audit.json` chứa phép đếm và ô không hợp lệ; 39 stderr files rỗng. 82 ô lượt trước đều còn và giữ phân loại giết đúng chốt; 10 ô mới (8 F01, 2 F02). Không dùng chữ AssertionError một mình làm bằng chứng: đã đọc cả rc/lý do bên trong.

| Mutant mới/đổi | Ca đích | Kết quả thực | Phân loại |
|---|---|---|---|
| `kg_n1_bo_kiem_dang` | `kg_n1_check_suite_abc` | AssertionError: kiem-gate: đòi rc=2, được rc=12; stderr="CẢNH BÁO: 'gate' có 1 run ở suite khác (1) — bỏ qua\n  ĐỎ  'gate': VẮNG — không check-run nào mang đúng tên này trong suite abc\ngate KHÔNG xanh trên abababababababababababababababababababab: 1/1 tên bắt buộc đỏ" | GIẾT ĐÚNG CHỐT |
| `kg_n1_bo_kiem_dang` | `kg_n1_check_suite_am` | AssertionError: kiem-gate: đòi rc=2, được rc=12; stderr="CẢNH BÁO: 'gate' có 1 run ở suite khác (1) — bỏ qua\n  ĐỎ  'gate': VẮNG — không check-run nào mang đúng tên này trong suite -1\ngate KHÔNG xanh trên abababababababababababababababababababab: 1/1 tên bắt buộc đỏ" | GIẾT ĐÚNG CHỐT |
| `kg_n1_bo_kiem_dang` | `kg_n1_check_suite_0` | AssertionError: kiem-gate: đòi rc=2, được rc=12; stderr="CẢNH BÁO: 'gate' có 1 run ở suite khác (1) — bỏ qua\n  ĐỎ  'gate': VẮNG — không check-run nào mang đúng tên này trong suite 0\ngate KHÔNG xanh trên abababababababababababababababababababab: 1/1 tên bắt buộc đỏ" | GIẾT ĐÚNG CHỐT |
| `kg_n1_bo_kiem_dang` | `kg_n1_check_suite_012` | AssertionError: kiem-gate: đòi rc=2, được rc=12; stderr="CẢNH BÁO: 'gate' có 1 run ở suite khác (1) — bỏ qua\n  ĐỎ  'gate': VẮNG — không check-run nào mang đúng tên này trong suite 12\ngate KHÔNG xanh trên abababababababababababababababababababab: 1/1 tên bắt buộc đỏ" | GIẾT ĐÚNG CHỐT |
| `kg_n1_bo_kiem_dang` | `kg_n1_check_suite_cong` | AssertionError: kiem-gate: đòi rc=2, được rc=12; stderr="CẢNH BÁO: 'gate' có 1 run ở suite khác (1) — bỏ qua\n  ĐỎ  'gate': VẮNG — không check-run nào mang đúng tên này trong suite 5\ngate KHÔNG xanh trên abababababababababababababababababababab: 1/1 tên bắt buộc đỏ" | GIẾT ĐÚNG CHỐT |
| `kg_n1_bo_kiem_dang` | `kg_n1_check_suite_cach` | AssertionError: kiem-gate: đòi rc=2, được rc=0; stderr='' | GIẾT ĐÚNG CHỐT |
| `kg_n1_bo_kiem_dang` | `kg_n1_check_suite_unicode` | AssertionError: kiem-gate: đòi rc=2, được rc=12; stderr="CẢNH BÁO: 'gate' có 1 run ở suite khác (1) — bỏ qua\n  ĐỎ  'gate': VẮNG — không check-run nào mang đúng tên này trong suite 11\ngate KHÔNG xanh trên abababababababababababababababababababab: 1/1 tên bắt buộc đỏ" | GIẾT ĐÚNG CHỐT |
| `kg_n2_chi_kiem_bat_buoc` | `kg_n2_run_khong_bat_buoc_thieu_suite` | AssertionError: kiem-gate: đòi rc=12, được rc=0; stderr='' | GIẾT ĐÚNG CHỐT |
| `kg_f01_bo_kiem_danh_tinh` | `kg_f01_cung_id_khac_suite` | AssertionError: kiem-gate: đòi rc=12, được rc=0; stderr="CẢNH BÁO: 'gate' có 1 run ở suite khác (1) — bỏ qua" | GIẾT ĐÚNG CHỐT |
| `kg_f01_bo_kiem_danh_tinh` | `kg_f01_cung_id_khac_ten` | AssertionError: kiem-gate: đòi rc=12, được rc=0; stderr='' | GIẾT ĐÚNG CHỐT |
| `kg_f01_bo_kiem_danh_tinh` | `kg_f01_cung_id_hai_ten_bat_buoc` | AssertionError: kiem-gate: đòi rc=12, được rc=0; stderr='' | GIẾT ĐÚNG CHỐT |
| `kg_f01_bo_kiem_danh_tinh` | `kg_f01_cung_id_khac_suite_hai_trang` | AssertionError: kiem-gate: đòi rc=12, được rc=0; stderr="CẢNH BÁO: 'gate' có 1 run ở suite khác (1) — bỏ qua" | GIẾT ĐÚNG CHỐT |
| `kg_f01_bo_suite_khoi_danh_tinh` | `kg_f01_cung_id_khac_suite` | AssertionError: kiem-gate: đòi rc=12, được rc=0; stderr="CẢNH BÁO: 'gate' có 1 run ở suite khác (1) — bỏ qua" | GIẾT ĐÚNG CHỐT |
| `kg_f01_bo_suite_khoi_danh_tinh` | `kg_f01_cung_id_khac_suite_hai_trang` | AssertionError: kiem-gate: đòi rc=12, được rc=0; stderr="CẢNH BÁO: 'gate' có 1 run ở suite khác (1) — bỏ qua" | GIẾT ĐÚNG CHỐT |
| `kg_f01_bo_ten_khoi_danh_tinh` | `kg_f01_cung_id_khac_ten` | AssertionError: kiem-gate: đòi rc=12, được rc=0; stderr='' | GIẾT ĐÚNG CHỐT |
| `kg_f01_bo_ten_khoi_danh_tinh` | `kg_f01_cung_id_hai_ten_bat_buoc` | AssertionError: kiem-gate: đòi rc=12, được rc=0; stderr='' | GIẾT ĐÚNG CHỐT |
| `kg_f02_bo_bat_tran_int` | `kg_f02_suite_vuot_tran_int` | AssertionError: kiem-gate --check-suite 4301 chữ số: đòi rc=12, được rc=1; stderr='Traceback (most recent call last):\n  File "/tmp/wp788-r2.AITtnb/mutants/kg_f02_bo_bat_tran_int/packet_loop.py", line 2588, in <module>\n    sys.exit(main())\n             ~~~~^^\n  File "/tmp/wp788-r2.AITtnb/mutants/kg_f02_bo_bat_tran_int/packet_loop.py", line 2584, in main\n    return a.fn(a, Path(a.state_dir))\n           ~~~~^^^^^^^^^^^^^^^^^^^^^^\n  File "/tmp/wp788-r2.AITtnb/mutants/kg_f02_bo_bat_tran_int/pa …  limit (4300 digits) for integer string conversion: value has 4301 digits; use sys.set_int_max_str_digits() to increase the limit' | TRACEBACK — không tính giết; F03 |
| `kg_f02_du_phong_khop_nham` | `kg_f02_suite_vuot_tran_int` | AssertionError: kiem-gate --check-suite 4301 chữ số: đòi rc=12, được rc=0; stderr='' | GIẾT ĐÚNG CHỐT |

`kg_n1_bo_kiem_dang`: abc đổi 2→12 có VẮNG, không còn suite None; dấu cách đổi 2→0. Bảy ô vẫn bắt đúng hợp đồng mã lỗi đối số, không chết vì int traceback. `kg_n2_chi_kiem_bat_buoc`: thay kèm cách truy cập identity để không KeyError; run không bắt buộc thiếu suite thực sự làm 12→0, nên ca đang đo schema toàn bộ, không được identity bắt hộ.

Catalog so với lượt 1 (chỉ import metadata, không chạy lại review cũ): **388→394 ca; kg 86→92; removed=[]; removed_mutants=[]**. Sáu ca thêm chính là 5 F01 + 1 F02. Không có ca không-kg đổi danh sách; diff mới không đổi nội dung các ca đó. Raw: `catalog-delta.json`.

**Thẩm định lời khai executor:** `kg_f02_bo_bat_tran_int` đúng là tái tạo chính ValueError 4301 chữ số của F02, không phải lỗi import/setup vô can. Nhưng spec đóng băng ghi **“traceback = tín dụng giả”**, và cột đỏ ghi **“traceback đếm là giết”**; assignment không cấp ngoại lệ sửa luật ấy. Companion `kg_f02_du_phong_khop_nham` đã đo độc lập là 12→0, stderr rỗng, nên có tín dụng hợp lệ cho lỗi khớp nhầm. Nó không đổi phân loại của ô traceback thứ nhất. F02 sản phẩm vẫn ĐÃ ĐÓNG; vấn đề còn lại là ghi tín dụng của bảng đột biến.

## Finding F03 — `mutation-credit-traceback-contract`

- **P2**; trục **Spec**; lớp `mutation-credit-traceback-contract` (không phải H3); tệp `.claude/dev/packet_loop_test.py:5651`–5655, đăng ký mutant `kg_f02_bo_bat_tran_int`. Đường chấm điểm có sẵn tại 5944–5959 coi mọi lỗi ca đích không phải skip là giết; đăng ký mới đưa traceback vào phép đếm ấy.
- **Bằng chứng chạy được:** command lớp D đã chạy trên exact head; riêng ô `kg_f02_bo_bat_tran_int / kg_f02_suite_vuot_tran_int` trả `AssertionError: … đòi rc=12, được rc=1; stderr='Traceback … ValueError: Exceeds the limit (4300 digits) … 4301 digits'`. Ô companion `kg_f02_du_phong_khop_nham` trả `đòi rc=12, được rc=0; stderr=''`. Raw đầy đủ trong `mut_all.out` và `mutation-audit.json`. Spec `nghiem_thu/dot-bien` cấm cấp tín dụng traceback; comment mới tự tạo ngoại lệ chưa được authority chốt.
- **Tác động/giới hạn:** không tái mở F02 sản phẩm, không có đường cấp XANH mới. Đây là một ô tín dụng sai hợp đồng làm bảng được báo “giết” rộng hơn evidence được phép tính. Companion hợp lệ không biến ô traceback thành hợp lệ. Gom toàn bộ ô sai chốt của lượt này vào finding này: đúng **1 ô**, không tách finding phụ.
- **HINT — vá ở đâu/thế nào:** rẻ nhất là bỏ mutant tái tạo crash khỏi `MUTANTS` dùng cho bảng tính giết và sửa comment tự miễn trừ; giữ ca nền `kg_f02_suite_vuot_tran_int` cùng mutant đổi màu `kg_f02_du_phong_khop_nham`. Phản chứng tái tạo crash có thể giữ ở evidence chẩn đoán ngoài bảng tính giết. Không cần sửa mã gate sản phẩm hoặc mở rộng runner dùng chung. Phương án giữ crash trong một bảng có loại riêng cần authority sửa hợp đồng/reporting rõ ràng; không tự nới spec bằng comment.
- **HINT — test khóa:** ca F02 nền vẫn xanh (12 + VẮNG, không traceback); companion bắt buộc đổi 12→0 khiến test đỏ. Bảng nhận tín dụng không còn ô traceback. Đã thử phương án test-only trong scratch: `hint-check.json`, baseline `{'kg_f02_suite_vuot_tran_int': None}`; companion rc wrapper=0, kết quả ca `AssertionError … đòi rc=12, được rc=0; stderr=''`, không Traceback. Không chạy lại full suite trên bản HINT và không khai đã làm vậy.
- **HINT — nguy cơ:** chỉ xóa ca regression hoặc chỉ đổi lời khai sẽ làm mất bảo vệ thật; cần giữ nguyên ca nền và companion. Đừng thêm allowlist traceback vào generic scorer, vì sẽ mở lại tín dụng do lỗi vô can. Patch test-only dưới đây giảm số dòng, không đòi vượt trần 300.

HINT thuần TEST — **chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm commit**. Bản sao scratch đã chạy kiểm targeted như trên; checkout được review không bị sửa. File `/tmp/wp788-r2.AITtnb/HINT-F03.patch`:

```diff
--- a/.claude/dev/packet_loop_test.py
+++ b/.claude/dev/packet_loop_test.py
@@ -5648,11 +5648,7 @@
                                        ["kg_f01_cung_id_khac_suite", "kg_f01_cung_id_khac_suite_hai_trang"]),
     "kg_f01_bo_ten_khoi_danh_tinh": ('dt = (r["name"], r["check_suite"]["id"], r["head_sha"])', 'dt = (r["check_suite"]["id"], r["head_sha"])',
                                      ["kg_f01_cung_id_khac_ten", "kg_f01_cung_id_hai_ten_bat_buoc"]),
-    # F02: bỏ đường bắt trần `int()` ⇒ traceback. Ở ĐÂY traceback chính là lỗi đang khoá, nên ca
-    # đích chết vì nó là đúng chốt (ca đòi rc=12 và vắng traceback).
-    "kg_f02_bo_bat_tran_int": (("    try:\n        suite = int(a.check_suite)\n    except ValueError:", "        suite = a.check_suite   #"),
-                               ("    if True:\n        suite = int(a.check_suite)\n    if False:", "        pass   #"),
-                               ["kg_f02_suite_vuot_tran_int"]),
+    # F02: ca nền khóa lỗi traceback; bảng mutation đo đổi màu của fallback.
     "kg_f02_du_phong_khop_nham": ("        suite = a.check_suite   #", "        suite = 1   #", ["kg_f02_suite_vuot_tran_int"]),
     "kg_n6_dong_xanh_khong_suite": ('(suite {suite}): ', ": ", ["kg_m2_object_mot_trang", "kg_n7_that_suite_ci"]),
 })
```

## Lớp E — Gate (đang chờ kết thúc)

Suite nền đã có bằng chứng dương:

```text
  BỎ QUA  luong_canonical_chay_that: chỉ đo lệnh pwsh trên Windows
nền: 393/393 đạt · BỎ QUA: 1
```

Chưa có `TỔNG: ĐẠT` và exit code cuối ở thời điểm ghi mục này: full gate **pending**, không dùng 393/393 thay completion. Windows thực **skipped**, không tính pass.

Kiểm delta nhẹ (raw ở `gates-delta.json`): `python -B -m ruff check --no-cache --select F <path>` với Ruff 0.15.15, cùng một runtime cho blob nền d347 và head; cả hai rc=1, cùng một F841 `n` ở dòng 1804 ⇒ **bare lint failed nền, DELTA=0 đạt tiêu chí spec**. Không khai Ruff sạch. `doctrine-scan --root .` rc=0, `10 tệp, 0 chỗ chép doctrine`; `adr-song --root .` rc=0, `53 ADR / 53 dòng`, giữ kết quả lượt 1. Ruff pin/probe contract **not_run** trong lượt này (không thay đổi).

Không chạy lại ma trận N1–N7 của lượt 1. Các ô hành vi đổi và ca regression mới được cập nhật ở cuối; 82 ô mutation cũ đã được audit đầy đủ theo yêu cầu lớp D.

Đã xác nhận trên chính output full suite (không chỉ suy từ mã scorer):

```text
  ok  kg_f02_bo_bat_tran_int → giết 1 ca đích · 3 đối chứng khác họ còn sống
  ok  kg_f02_du_phong_khop_nham → giết 1 ca đích · 3 đối chứng khác họ còn sống
```

Dòng thứ nhất đúng là đang được tính giết, dù lớp D đo được traceback. Đây là bằng chứng dương cho F03; dòng thứ hai xác nhận companion có tín dụng riêng. Phép đo bytecode trong scratch mutation: `.pyc=0`, `.pyo=0`; 39 tệp stderr có kích thước 0.

## Bảng lớp và phần chưa đo

| Slug lớp | Finding / nguồn | Trạng thái lượt 2 | Kiểm đóng lớp / giới hạn |
|---|---|---|---|
| `bang-chung-dau-vao-tin-qua-muc` (H3) | F01 lượt 1 e995730464da03223cf636e49ad32e220c6ec720; kế thừa H3=4 sau checkpoint | ĐÃ VÁ THẬT trong phạm vi được giao; không có H3 mới tìm được | Bốn probe cũ đỏ đúng lý do, đối chứng xanh, 24 biến thể identity, luật status/conclusion toàn bộ bản trùng; mutant F01 giết đúng chốt. Không nâng H3 lên 5 |
| `cli-decimal-conversion-unhandled` | F02 lượt 1 e995730464da03223cf636e49ad32e220c6ec720 | ĐÃ VÁ THẬT | 4301 chữ số trả 12 + VẮNG, không crash; limit 640/4300/0, fallback không khớp int, companion đổi màu |
| `mutation-credit-traceback-contract` | F03 mới lượt 2 4ffae005eb1c434d660cbfb713ad21ed92115a8a, P2 | CHƯA ĐÓNG | Một ô traceback được scorer ghi giết; HINT pure-test đã đo ngoài checkout. Cần executor tái dẫn xuất theo hợp đồng, không cần sửa spec để nhận crash là giết |

Đếm riêng: **2 lớp cũ được đóng; 1 lớp mới còn mở / 1 finding / 1 biểu hiện**. Không nhập F03 vào F02, không tự tạo finding H3 từ việc bảng test ghi tín dụng sai. Lượt này xét ngưỡng sensitive theo assignment: P0=P1=P2 phải 0 và mọi P3 có hướng xử lý.

`not_run/not_measured`: Windows thực, CI/head cuối `tu-do`, connector completed, merge authorization, refs/lease/state máy chủ, runtime model/effort executor và receipt delivery. Assignment cấm GitHub/mạng; không dùng fixture bb8c0c4 hay local suite thay evidence CI head cuối. Những mục này giữ giới hạn lượt 1, không ghi finding mới ngoài scope. Không push, commit, merge, land, deploy, LIVE hoặc đăng comment. Phần vận chuyển/receipt/state thuộc controller; artifact cục bộ không tự đổi assurance.

Đối chiếu drift merge bổ sung: `git rev-parse 49a47badfefb944a7bb4f037c0a34e78f77355b9:.claude/skills/soan-spec/SKILL.md d347d426334bbe1bbb1161184ab0acffee9be054:.claude/skills/soan-spec/SKILL.md` rc=0, cả hai blob cùng `b1975ef9e96d7a5cde040cd678bfbc68d8fb94ec`. Nội dung drift đúng blob d347, không chỉ trùng tên tệp.

## Kết quả terminal lớp E và kết luận

Exec session `41695` kết thúc **exit_code=0** — mã thật của lệnh Python redirect, không chỉ marker grep. `suite-completion.json` lưu completion quan sát được. Output thật:

```text
  BỎ QUA  luong_canonical_chay_that: chỉ đo lệnh pwsh trên Windows
nền: 393/393 đạt · BỎ QUA: 1
  ok  78 lớp lách đều có đột biến giết · 6 đột biến PHỐI HỢP · 0 ngoại lệ
  ca               : 394
  đột biến         : 166
  lớp lách         : 78
  ca bắt-oan       : 35
  ngoại lệ AC 18   : 0
TỔNG: ĐẠT
```

166/78 là số **runner in ra**, không thay audit đúng chốt lớp D; riêng kg chỉ có **38 mutant / 91 ô** nhận tín dụng đúng hợp đồng, một mutant / một ô traceback không được tính. Full suite xanh không đóng F03.

- **passed**: suite Linux rc=0 + 393/393 + TỔNG; 7 probe A; 99 probe C và probe bool lưu riêng; 38 mutant/91 ô kg hợp lệ; kích thước/write set/merge drift; Ruff delta=0; scanner doctrine/ADR giữ màu.
- **failed**: một ô mutation nhận tín dụng traceback (F03 P2); bare Ruff có F841 nền cả base/head (tiêu chí delta đạt). Không có phản chứng F01/F02 sản phẩm còn đỏ.
- **skipped**: một ca pwsh Windows thực, không tính passed.
- **not_run/not_measured**: CI/Windows/receipt/authority đã liệt kê; không suy từ suite local hay tên job.

Kiểm cuối `2026-10-18T00:34:35.313083+00:00`: HEAD/tree giữ nguyên; `git diff --exit-code` và `git diff --cached --exit-code` đều rc=0, output rỗng; tracked hashes delta=`[]` trên 3680 tệp không nhạy cảm. Untracked/ignored chỉ artifact được giao và `.codex/` đã thấy đầu run. Hai snapshot không chứng minh chưa từng ghi rồi hoàn nguyên giữa hai mốc. Sandbox thực workspace-write. Raw `end.json`. Lần đầu script đóng báo cáo lỗi SyntaxError trước thực thi, không ghi gì; đã sửa và chạy lại, rc=0 như evidence cuối.

Hiện vật ổn định (inventory đầy đủ ở `/tmp/wp788-r2.AITtnb/artifacts.json`):

| Artifact | Bytes | SHA-256 |
|---|---:|---|
| `.review/suite.out` | 20009 | `f4d64355b6ea55df65f10f7896e8ac12573a1488906359d79465618eb94ef85e` |
| `/tmp/wp788-r2.AITtnb/layer-a.json` | 13038 | `be5a38d2fc5a7713f54f38a53d565e80b5a245882f662d5677b98cc62dc442d3` |
| `/tmp/wp788-r2.AITtnb/layer-c.json` | 195239 | `ed6b7dc879aaf4aed102a10000cd604b3c0d94c73100398618ed8c75c3dcb99e` |
| `/tmp/wp788-r2.AITtnb/mut_all.out` | 17858 | `42c28c744a2e32b0c15afa23ebd42f9604bca5b5875356697f95d0c839d5eefb` |
| `/tmp/wp788-r2.AITtnb/mutation-audit.json` | 1850 | `799f80a3778159e1955b6da702940aa0f8d0051f24a6f08056f2476744a590e0` |
| `/tmp/wp788-r2.AITtnb/HINT-F03.patch` | 1336 | `a284b0d09b31a8f7228282887f941cab2765dd93117823770c275a43a1c76ceb` |

Nhận dạng contract cuối thay mô tả sơ bộ “tool-mediated” đầu artifact: **provider `openai_codex`, model_family `openai`, execution_surface `codex_cli`, transport `machine`**, nguồn run.json/header đúng run. Không tạo approval, receipt hoặc GitHub state. Theo ngưỡng sensitive của assignment, còn P2 ⇒ **changes_requested**; HINT có thể xử lý trong write set hiện hành. H3 giữ **4**, không có finding H3 mới kích hoạt dừng ở 5.

reviewed_sha: 4ffae005eb1c434d660cbfb713ad21ed92115a8a
reviewed_tree: f6aeed236145682acc26dbb310f0cada5f6f33d8
verdict: changes_requested
counts: P0=0, P1=0, P2=1, P3=0
provider: openai_codex
model_family: openai
model: gpt-6.1-sol (CLI header)
effort: xhigh (CLI header)
execution_surface: codex_cli
transport: machine
assurance: không có approval; chưa vận chuyển/validate receipt/state

Bảng chỉ các ô N1–N7 đã đổi so lượt 1 (N2/N4/N6 giữ kết luận trước, không chạy lại ma trận từ đầu):

| Ô | Lượt 1 | Lượt 2 / bằng chứng cập nhật |
|---|---|---|
| N1 | Chưa đạt đầy đủ vì F02, 4301 chữ số rc=1 + Traceback | **ĐÃ VÁ F02**: cùng probe rc=12 + VẮNG, không Traceback; limit 640/4300/0 không khớp nhầm. Mutant bỏ dạng cập nhật vẫn bắt đúng hợp đồng mã 2; riêng dấu cách đổi 2→0 |
| N3 | Luật sau lọc đúng nhưng F01 lọc mất identity mâu thuẫn còn XANH | **ĐÃ VÁ F01**: cùng id khác suite/tên, hai tên bắt buộc, xuyên trang đều 12 + mang hai danh tính; duplicate nhất quán vẫn xanh; ba mutant F01/8 ô chết đúng chốt |
| N5 (consistency bổ sung) | Đếm đủ id không đóng F01 | **ĐÃ VÁ consistency** trước lọc/đếm; một ID không còn chứng minh hai danh tính. Count/schema gốc giữ kết luận |
| N7 | Chưa có regression F01/F02; kg 86 ca; nền 387/387 + 1 skipped | **ĐÃ THÊM** 6 ca, kg 92; không mất ca cũ; nền 393/393 + 1 skipped, TỔNG: ĐẠT, rc=0. Gate mutation riêng còn **F03 P2** (1 ô traceback được ghi giết), chưa đủ approve |
