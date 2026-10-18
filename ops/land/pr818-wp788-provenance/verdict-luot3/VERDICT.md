verdict: changes_requested

# Cross-review lượt 3 — wp788

reviewed_sha: 8264089a14f79867091da2629edbf45a22854c39

Đã hoàn tất lớp A–E; kết luận cuối ở cuối tệp.

## Preflight

- Exact head `8264089a14f79867091da2629edbf45a22854c39`, tree `bbbcb30ec09191e8f3390fdeea259abbdcef54ea`; detached checkout; origin `https://github.com/ducthangho/tra-luat`. Spec r1/g1 theo assignment và lịch sử nhánh.
- SHA-256 spec: `82dc170446c3a4431739a3effbec8cb55adadc13d69f5c510f8782a2b45eb54e`; hai verdict trước khớp băm giao. Immutable spec baseline `d8b15cb0730c85e7019aee627c3bfa645a6d3eaf`; nền so diff được assignment cấp `d347d426334bbe1bbb1161184ab0acffee9be054`; candidate là exact head trên. Spec nguồn review là `.review/SPEC.md` đã ghim hash, không tự nhận spec trong product tree là nguồn mới.
- Review Class `sensitive`; write set sản phẩm đúng hai tệp `.claude/dev/packet_loop.py` và `.claude/dev/packet_loop_test.py`. Assignment cho phép ghi verdict và suite output trong `.review/`; scratch `/tmp/wp788-review3-knzzguqq`, ngoài checkout.
- Authority review offline lượt 3/tiếp tục sau checkpoint H3=4 là `prompt.snapshot` của run `15a18a971a124d12b448af1971c7f112`. Không dùng prompt làm lease viết/land; không gọi GitHub/mạng. Lease/state/refs live và budget live không đo lại theo giới hạn assignment.
- Reviewer: `openai_codex / codex_cli / machine`, họ `openai`, phiên độc lập executor. Header đúng run: Codex `0.163.0`, model `gpt-6.1-sol`, effort `xhigh`, session `01a14c78-6e9f-7052-be70-ff68a7cc68d9`. Nguồn: `runs/15a18a97/run.json` và đầu `stderr.log`; header không chứng minh model mọi request. Executor họ `claude`, `claude-opus-5-5 / claude_code / machine/local` theo spec; runtime receipt executor không được cấp để đo lại.
- Runtime Linux, Python `3.13.16`, ripgrep `15.2.0`, `core.abbrev=7`; sandbox thực `workspace-write`, không khai OS read-only. Không chạy `doctor/chuan-bi` vì assignment cấm mạng và không giao xử lý credential; capability dùng trực tiếp qua Git/Python/bash. Tool environment_status không có trong bộ công cụ khả dụng.
- Snapshot đầu: HEAD/tree/index/diff và hash nội dung toàn cây (gồm untracked/ignored, trừ `.git` và `.review` được giao ghi) lưu ngoài kho. Giới hạn quan sát: chỉ checkout reviewer, không kho executor nguồn.
- Suite khởi chạy ngay sau đọc assignment: `python -B .claude/dev/packet_loop_test.py > .review/suite.out 2>&1`, session `73333`; chưa tính pass tới khi có rc thật và marker cuối.

## Lớp A — ĐỐI CHIẾU LƯỢT TRƯỚC

Lệnh targeted qua `packet_loop_test.chay_suite` trên code candidate, `python -B`, scratch ngoài kho; wrapper rc=0. Output:

```json
{
  "selected": [
    "kg_f01_cung_id_khac_suite",
    "kg_f02_suite_vuot_tran_int"
  ],
  "results": {
    "kg_f01_cung_id_khac_suite": null,
    "kg_f02_suite_vuot_tran_int": null
  },
  "removed_crash_mutant": true,
  "companion_present": true
}
```

- F01: **ĐÃ VÁ THẬT**, probe `kg_f01_cung_id_khac_suite` còn đỏ 12 đúng lý do `mang hai danh tính`; mỗi finding cũ được kiểm độc lập, không nhận tổng suite thay probe.
- F02: **ĐÃ VÁ THẬT**, probe `kg_f02_suite_vuot_tran_int` kiểm suite 4301 chữ số: rc=12 + `VẮNG`, không traceback.
- F03: mutant crash đã bị bỏ, ca nền và companion còn nguyên. Kết luận đóng toàn lớp sau audit toàn bộ bảng ở lớp D; chưa dùng việc xoá tên làm bằng chứng đủ. Raw `layer-a.json`.

## Lớp B — diff mới và phạm vi toàn packet

Đã đọc toàn bộ `git diff 4ffae005eb1c434d660cbfb713ad21ed92115a8a HEAD`, rc=0: chỉ xoá một mutant crash và sửa comment tương ứng; sản phẩm không đổi so lượt 2. Không xoá ca F02 hay companion.

`git diff --numstat d347d426334bbe1bbb1161184ab0acffee9be054 HEAD`, rc=0:

```text
52	10	.claude/dev/packet_loop.py
240	16	.claude/dev/packet_loop_test.py
```

2 tệp, 292 dòng thêm / 26 dòng xoá; trong trần ≤3 tệp / ≤300 dòng thêm. `git diff --check d347d426334bbe1bbb1161184ab0acffee9be054 HEAD`, rc=0, stdout/stderr rỗng. Hai path đúng write set; raw command/rc/hash/diff tại `layer-b.json`, `full-diff.patch`, `new-diff.patch` trong scratch.

## Lớp C — rà toàn bộ diff, comment/help, helper và H3

Đã đọc toàn bộ diff d347→candidate (không chỉ commit mới), cả `_doc_check_runs`, `cmd_kiem_gate`, parser/help, các closure `_KG_CA`, `case_kg_n4_canh_bao`, fixture và MUTANTS. Probe độc lập JSON/CLI: `layer-c-identity.json` có **21/21 đạt**, wrapper rc=0; `layer-c-warnings.json` có **8 subprocess** gồm F01/F02 thực và các biến thể cảnh báo. Không chạy lại ma trận lượt 1.

- F01 thực: `A-f01.json`, rc=12, stderr `id 1 mang hai danh tính ('gate', 1, 'abababababababababababababababababababab') và ('gate', 9, 'abababababababababababababababababababab') — bằng chứng mâu thuẫn`.
- F02 thực: `A-f02.json`, `--check-suite` = `"1" * 4301`, rc=12, `VẮNG`, không Traceback; stdout rỗng. Argv/output đầy đủ trong JSON, không rút ngắn dữ liệu gốc.
- H3: danh tính `(name, check_suite.id, head_sha)` được kiểm toàn bộ trước lọc; **12** probe đổi từng trường, đổi thứ tự, 1/2 trang đều 12 đúng lý do. **6** probe giữ identity nhưng sai status/conclusion ở mỗi thứ tự đều 12 đúng lý do; bản cũ failure + bản mới success, metadata không dùng và duplicate nhất quán vẫn 0 (**3** đối chứng). Đếm/schema được rà ở các trường lệnh thực đọc; không tìm thêm đường cấp xanh ngoài evidence. **H3 giữ 4**, không có H3 mới thứ 5.
- Help/epilog: `kiem-gate --help`, rc=0, có `--check-suite`, `GET actions/runs/<run_id>` → `check_suite_id`, `filter=all` và mã 0/2/12 đúng hành vi. Raw `help.json`.
- Helper: đã materialize/đọc **88 closure** `_KG_CA` vào `helper-audit.json` (4 ca kg còn lại là function riêng). Các ca thiếu count thực sự dùng `dem=False`; raw duplicate-key/non-JSON bypass helper nhưng có count; count sai có chủ ý được `setdefault` giữ nguyên. Schema trước đếm; ca thiếu conclusion cố định count=1 để mutant bỏ phần tử không bị N5 chặn hộ. Bool suite mặc định 1 để mutant thật sự đổi màu, không chỉ đổi lý do. Không tìm thêm ô bị helper đo nhầm chốt; audit mutant ở D là phép đối chứng bắt buộc.
- Comment về 30 runs gắn snapshot `bb8c0c4` trong spec; fixture mới ghi rõ đo 17-10 có 32, không gọi 30 là số hiện tại. Số 32/14 tên và các cancelled có thể kiểm trực tiếp fixture; nguồn API thật không xác thực lại do ngoài phạm vi. Các comment H3/fallback/count đối chiếu được với mã/probe; comment F03 không còn tự miễn trừ traceback.

Phát hiện hai biểu hiện P3 ở N4, ghi riêng theo hai nguyên nhân dưới đây. Chúng không đổi màu gate và không là H3.

### F04 — `warning-name-repr-not-spec-literal`

- **P3**, trục **Spec**, lớp `warning-name-repr-not-spec-literal`; `.claude/dev/packet_loop.py:2346`, `cmd_kiem_gate`. N4 bắt buộc đúng định dạng `CẢNH BÁO: '<tên>' ...`; `ten_cb!r` chọn dấu nháy theo Python repr và escape tên, không giữ tên/nháy đơn như hợp đồng.
- Phản chứng JSON/CLI `C-warning-3.json`: 2 run id=1 suite=1 và id=2 suite=9, cùng tên `reviewer's gate`, completed/success/đúng head; `--bat-buoc "reviewer's gate" --check-suite 1`. Rc=0, stdout xanh; stderr thực:

```text
CẢNH BÁO: "reviewer's gate" có 1 run ở suite khác (2) — bỏ qua
```

Spec đòi `CẢNH BÁO: 'reviewer's gate' có 1 run ở suite khác (2) — bỏ qua`. Đối chứng `gate` và tên có nháy kép giữ đúng định dạng. Tên/argv là dữ liệu chuỗi, không thực thi shell. Phép so exact trong `layer-c-warnings.json`: sai ở tên có nháy đơn và tên chứa dấu chéo ngược, đúng ở hai đối chứng; không tự giới hạn tên theo 14 context fixture.
- **HINT — ở đâu/thế nào:** sửa riêng formatter cảnh báo N4 tại `cmd_kiem_gate`, xuất tên theo đúng quy tắc literal của spec với nháy đơn cố định; giữ logic chọn run. Không đổi formatter chẩn đoán lỗi khác vốn không có contract này. Nếu cần escaping ký tự điều khiển để luôn một dòng, phải chốt quy tắc với owner/spec, không ngầm coi Python repr là mẫu được giao.
- **Test khóa:** thêm tên có nháy đơn vào ca N4, đòi exact stderr, rc không đổi; đối chứng tên bình thường/nháy kép. Đột biến đưa `!r` trở lại phải làm ca nháy đơn đỏ. Phản chứng hiện tại đã chạy và sai đúng chuỗi trên; chưa có test mới trên cây thật.
- **Nguy cơ:** nội suy nguyên văn tên có newline có thể phá một-dòng; không sửa bằng cách từ chối mọi dấu nháy hoặc đổi tên thật. Đây là P3 sai định dạng/định danh trong diagnostics, không phải bypass gate.

### F05 — `warning-count-records-not-distinct-runs`

- **P3**, trục **Spec/Standards**, lớp `warning-count-records-not-distinct-runs` (thuộc H1 claim-precision, **không** H3); `.claude/dev/packet_loop.py:2344`. `_doc_check_runs` chấp nhận bản ghi lặp nhất quán xuyên trang, coi cùng id là một check-run và N5 đếm id phân biệt; cảnh báo lại đếm từng bản ghi.
- Phản chứng `C-warning-duplicate.json`: trang 1 total_count=2 có gate id1 suite1 và gate id2 suite9; trang 2 total_count=2 lặp lại gate id2 suite9. Mọi trạng thái completed/success/đúng head. Rc=0, gate xanh, stderr thực:

```text
CẢNH BÁO: 'gate' có 2 run ở suite khác (2, 2) — bỏ qua
```

Chỉ có **một** run ngoài suite (id2), được lặp hai bản; N4 khai **hai** run. Đối chứng hai id khác nhau 2 và 3 in `2 run ... (2, 3)`, rc=0; duplicate của suite neo vẫn xanh. Raw argv/JSON/output lưu tại `layer-c-warnings.json`.
- **HINT — ở đâu/thế nào:** dựng danh sách ID ngoài suite từ tập id phân biệt trước sắp xếp/đếm ở khối cảnh báo N4. Chỉ khử trùng **bản chiếu cảnh báo**; giữ đủ mọi bản ghi cho luật mọi bản trùng của max-id đều xanh. Thay đổi rẻ nhất đóng lỗi thống kê, không cần sửa schema/logic N3/N5.
- **Test khóa:** hai trang trên phải in đúng `1 run ... (2)`; hai id thật 2/3 vẫn in `2 run ... (2, 3)`; thêm bản trùng cùng identity nhưng failure ở suite neo vẫn đỏ 12. Đột biến quay lại đếm list phải làm ca duplicate warning đỏ. Fixture/đối chứng hiện đã chạy trên candidate.
- **Nguy cơ:** khử trùng toàn `runs` sẽ mất bản failure cùng id, mở bypass mà N3 cố chặn; vì vậy không đẩy việc dedup vào `_doc_check_runs`. Không coi việc đổi count cảnh báo là lý do đổi màu gate.

## Lớp D — audit toàn bảng (setup)

Lời gọi đầu `bash .review/mut_all.sh "$PWD/.claude/dev" kg_ /tmp/wp788-review3-knzzguqq/mutants` trả shell rc=0 nhưng thư mục output con chưa tồn tại: redirect từng `.err` thất bại trước khi subprocess mutant chạy. **Không tính là audit/pass**, không cấp tín dụng cho output rỗng. Raw `mut_all-setup-error.out`. Đã tạo thư mục output ngoài kho; chạy lại toàn catalog trong một lượt dưới đây.

### Lớp D — kết quả toàn bảng và đóng F03

Lượt chạy thật: `bash .review/mut_all.sh "$PWD/.claude/dev" kg_ /tmp/wp788-review3-knzzguqq/mutants > /tmp/wp788-review3-knzzguqq/mut_all.out 2>&1`, session `23711`, **exit_code=0**. Đọc từng output và đối chiếu catalog/tập ca, không chỉ nhận rc wrapper hay nhãn AssertionError. **38 mutant / 91 ô: 91 ô bị bắt đúng luật, 0 sống, 0 traceback, 0 lỗi setup/import trong lượt thực thi.** 38 `.err` đều 0 byte; không `.pyc/.pyo`. Raw `mut_all.out`, `mutation-audit.json`.

Đối chiếu catalog exact Git blob lượt 2, không chạy suite cũ: 394→394 ca, kg giữ 92; không mất ca; 39→38 mutant kg; chỉ mất `kg_f02_bo_bat_tran_int`, mọi mutant còn lại giữ nguyên payload/tập ca.

Chỉ ô có trạng thái khác lượt 2:

| Mutant / ca | Lượt 2 | Lượt 3 |
|---|---|---|
| `kg_f02_bo_bat_tran_int` / `kg_f02_suite_vuot_tran_int` | Traceback bị runner nhận tín dụng, F03 P2 | **Đã loại khỏi catalog tính giết**, không còn ô nhận traceback. Ca nền vẫn đạt và companion bên dưới vẫn có răng |

Companion (xác nhận bắt buộc, trạng thái giữ nguyên): `kg_f02_du_phong_khop_nham / kg_f02_suite_vuot_tran_int` → `AssertionError: kiem-gate --check-suite 4301 chữ số: đòi rc=12, được rc=0; stderr=''`. Ca nền cùng tên trả 12 + VẮNG, không traceback (A). Do đó **F03 ĐÃ ĐÓNG / ĐÃ VÁ THẬT**; không còn finding ô sai chốt để gom. Đối chiếu U lượt 2 chỉ gồm F03: F={F03}, **1/1=100%**; tỷ lệ không thay điều kiện approval và hai P3 mới F04/F05 không vào tử số.

### Phản chứng chạy lại được cho lớp F04/F05

Script thuần JSON/CLI ngoài kho:

```bash
python -B /tmp/wp788-review3-knzzguqq/n4_regressions.py "$PWD" /tmp/wp788-review3-knzzguqq
```

**rc=1**, output thật:

```json
{"cases": 10, "passed": 5, "failed": ["quote-apostrophe", "quote-both", "repeat-same-page", "repeat-cross-page", "repeat-mutable-state"]}
```

Hai biểu hiện cùng root F04: nháy đơn và cả hai loại nháy; ba biểu hiện cùng root F05: trùng trong trang, xuyên trang, trùng có trạng thái khác ở suite ngoài. Năm đối chứng giữ đúng: tên thường, nháy kép, một id ngoài suite, hai id ngoài suite, bản trùng failure của suite neo. Phản chứng không có traceback/setup failure, từng command/rc/stdout/stderr và kỳ vọng được lưu ở `n4-regressions.json`. Đây là test cho diagnostics sản phẩm thật; không đưa vào bảng mutant hay tính tín dụng giết của D.

## Lớp E — gate và đối chiếu baseline

Suite chính vẫn đang chạy, chưa tính pass; chỉ chốt khi session `73333` kết thúc cùng `nền: N/N` và `TỔNG: ĐẠT`.

Các kiểm nhẹ, raw `gates-delta.json`: dựng hai clone ngoài checkout trong **một** script giống nhau từ OID d347 và candidate, origin endpoint thật, `core.abbrev=7`. Không chạy scanner do candidate để tự chứng nhận authority; đây là kiểm rc parity của hai phiên bản theo spec, không admission/CI evidence.

| Lệnh (Python `-B`, cwd/root từng clone) | Baseline d347 | Candidate | Đánh giá |
|---|---|---|---|
| `python -B -m ruff check --no-cache --select F .claude/dev/packet_loop.py` (Ruff 0.15.15) | rc=1, một F841 biến `n` dòng 1804 | rc=1, cùng một F841 | Bare lint **failed nền**, DELTA=0 **đạt tiêu chí spec**, không khai sạch Ruff |
| `python -B .claude/dev/packet_loop.py doctrine-scan --root .` | rc=0: 10 tệp, 0 chỗ chép doctrine | rc=0: cùng output | passed parity |
| `python -B .claude/dev/packet_loop.py adr-song --root .` | rc=0: 53 ADR / 53 dòng, khớp 1–1 | rc=0: cùng output | passed parity |

Ruff pin/probe workflow contract **not_run** (ngoài thay đổi); không dùng bare lint thay contract hoặc ngược lại. Không có CI/Windows mới trong vòng vá này.

Đối chiếu catalog nghiệm thu chung-2, chỉ đọc metadata blob baseline: `acceptance-catalog.json`:

```json
{
  "baseline_cases": 352,
  "candidate_cases": 394,
  "baseline_kg": 50,
  "candidate_kg": 92,
  "removed_baseline_cases": [],
  "added_non_kg": []
}
```

Không mất ca kg cũ, cũng không mất ca khác họ. Full suite đang là phép kiểm màu mọi ca trên candidate; không suy chỉ từ catalog rằng chúng xanh.

## Bảng lớp — lịch sử và trạng thái finding

| Slug lớp | Finding/nguồn | Trạng thái trên candidate | Kiểm đóng lớp/giới hạn |
|---|---|---|---|
| `bang-chung-dau-vao-tin-qua-muc` (H3) | F01 lượt 1 `e995730464da03223cf636e49ad32e220c6ec720` | **ĐÃ VÁ THẬT** | A + 12 probe identity, 6 state, 3 đối chứng; mutant identity D; không tìm H3 mới, H3 giữ 4 |
| `cli-decimal-conversion-unhandled` | F02 lượt 1 cùng SHA | **ĐÃ VÁ THẬT** | CLI 4301 chữ số rc=12 VẮNG, không traceback; companion 12→0 |
| `mutation-credit-traceback-contract` | F03 lượt 2 `4ffae005eb1c434d660cbfb713ad21ed92115a8a` | **ĐÃ VÁ THẬT** | Catalog chỉ bỏ crash mutant, ca F02 còn; D 38/91 không traceback/sai chốt |
| `warning-name-repr-not-spec-literal` | F04 mới lượt 3, candidate | **MỞ P3**, 2 biểu hiện trong script N4 | Fix formatter theo contract; test literal quote và đột biến đưa `!r` lại; executor packet chịu trách nhiệm xử lý |
| `warning-count-records-not-distinct-runs` | F05 mới lượt 3, candidate | **MỞ P3**, 3 biểu hiện trong script N4 | Count unique id riêng cảnh báo; test lặp trong/xuyên trang và status mutable; executor packet xử lý, giữ N3 đầy đủ bản trùng |

Đếm **5 lớp được theo dõi**: 3 lớp lịch sử đóng, 2 lớp mới mở / **2 finding mới / 5 biểu hiện đã đo**. Không nhập lớp formatter vào lớp count vì khác nguyên nhân/vá/test; không nâng lỗi diagnostics thành H3. P0=P1=P2=0, P3=2 tại thời điểm này. Chỉ thị chủ kho trong assignment chặt hơn ngưỡng mặc định: phải hết cả P3 mới approve.

`chua_do_duoc/not_run`: CI trên head cuối (`tu-do`), Windows thực, completion connector, live refs/state/lease, merge authorization, runtime receipt executor và delivery receipt/state transition; assignment cấm mạng/GitHub. Fixture bb8c0c4 và suite local không chứng minh CI head này. Không có quyền push/commit/merge/land/deploy/LIVE trong lượt reviewer này. Model/effort chỉ là khai báo CLI header của đúng run; không tự chứng minh từng request. Phần receipt/provenance/assurance bền do controller xử lý sau, artifact cục bộ không tự đổi GitHub state.

Hash prompt authority hiện đo: `81f4a937da281344104cac515ecb093e39632ad709065a699d42015bf73694fa`; input-artifacts.json giữ hash/size từng đầu vào.

## Kết quả terminal lớp E và kiểm toàn vẹn cuối

Session `73333` đã kết thúc **exit_code=0** (kết quả tiến trình thật của lệnh Python redirect). `suite-completion.json` giữ command, nguồn rc quan sát và hash output. Output thật:

```text
  BỎ QUA  luong_canonical_chay_that: chỉ đo lệnh pwsh trên Windows
nền: 393/393 đạt · BỎ QUA: 1
  BỎ QUA  đột biến luong_canonical_chay_that_dao_os_name: ca ['luong_canonical_chay_that'] không được tính là đã giết
  ok  kg_f02_du_phong_khop_nham → giết 1 ca đích · 3 đối chứng khác họ còn sống
  ok  78 lớp lách đều có đột biến giết · 5 đột biến PHỐI HỢP · 0 ngoại lệ
  ca               : 394
  đột biến         : 165
  lớp lách         : 78
  ca bắt-oan       : 35
  ngoại lệ AC 18   : 0
TỔNG: ĐẠT
```

394/165 là số catalog runner in; không đọc mutant Windows bị skipped thành đã chạy/đã giết. Riêng audit kg của D: 38 mutant/91 ô được đo độc lập và hợp lệ. Suite xanh không phủ nhận hai phản chứng diagnostics N4.

- **passed**: full suite Linux rc=0 + 393/393 + TỔNG; 2 probe targeted A, 21 probe identity/state C; 38 mutant/91 ô kg đúng lý do; diff/write set/kích thước; Ruff delta=0; doctrine/ADR parity. Các đối chứng N4 được phân loại riêng trong script, không gọi cả script là pass.
- **failed**: diagnostics N4, 2 lớp P3 (F04/F05), script 10 ca có 5 sai/5 đối chứng đúng, rc=1. Bare Ruff rc=1 nền cả hai cây, cùng một F841; không phát sinh delta. Lời gọi setup mutant đầu có lỗi redirect, không có phép đo; không tính pass.
- **skipped**: 1 ca Windows thực và mutant phụ thuộc ca ấy; không cấp tín dụng Windows. SyntaxWarning `\d` trong test cũ hiện cả baseline/candidate, không traceback; không là finding mới.
- **not_run/not_measured**: Ruff pin/probe workflow contract; Windows execution, CI/head cuối, receipt/provenance/connector/authority live như mục giới hạn. Không dùng local suite thay những bằng chứng đó.

Snapshot cuối `2026-10-18T00:56:06.345765+00:00`: **3680 tệp** thuộc phạm vi snapshot ngoài `.git/.review`, delta nội dung/thêm/xoá đều `[]`; HEAD/tree/index/diff đầu–cuối khớp. `git diff --exit-code` và `git diff --cached --exit-code` đều rc=0, output rỗng; untracked chỉ hiện vật `.review` được giao và ignored `.codex` đã có. Các input spec/verdict cũ/helper không bị thay; inventory input ở `input-artifacts.json`. Không quan sát repo executor nguồn; hai snapshot không chứng minh chưa từng ghi rồi hoàn nguyên giữa hai mốc. Sandbox thực `workspace-write`, không khai OS read-only.

Các artifact ổn định được băm tại `artifacts.json` trong scratch; một số mỏ neo chính:

| Artifact | Bytes | SHA-256 |
|---|---:|---|
| `/tmp/claude-0/-home-user-tra-luat/aec15584-50e8-55b9-b3a8-d6a2cfe55128/scratchpad/rv3/.review/suite.out` | 19914 | `5f96de3849cb50afd8bb873ab141259c4fdf4fe71d892587e9c736fb28ede7cf` |
| `/tmp/wp788-review3-knzzguqq/n4_regressions.py` | 2965 | `773699022725736020f8e8b1e5dea104a5e6768c274ff627532e21e5d92e1615` |
| `/tmp/wp788-review3-knzzguqq/n4-regressions.json` | 8766 | `3bc89fb5d02079941121a9500defede6131d1124e9de94c7091fbfedcd64aaa0` |
| `/tmp/wp788-review3-knzzguqq/mut_all.out` | 17046 | `2a522af57f512e69415b4ac0e600c5d3cffed542e05a8408d4e78b5d1a46e2e1` |
| `/tmp/wp788-review3-knzzguqq/mutation-audit.json` | 18472 | `2b788a76de017bab1e7daca04b49aef1f9321438bfae3fe688be50a64393f375` |

## Kết luận

Ngưỡng áp dụng là chỉ thị chủ kho trong assignment: hết cả P1/P2/P3. F01/F02 giữ đóng; F03 **ĐÃ VÁ THẬT**. Không có H3 mới (giữ 4). Còn F04 và F05, đều P3 về diagnostics N4, nên **changes_requested**; không phải approval hay merge/land authorization.

Dữ liệu nhận dạng dưới đây là metadata của review cục bộ, không là receipt/state event:

```yaml
packet_id: wp788
revision: 1
generation: 1
role: reviewer
provider: openai_codex
model_family: openai
model: gpt-6.1-sol # CLI header đúng run, không đo từng request
effort: xhigh # CLI header
execution_surface: codex_cli
transport: machine
session_id: 01a14c78-6e9f-7052-be70-ff68a7cc68d9
run_id: 15a18a971a124d12b448af1971c7f112
model_reviewer_identity: openai_codex/gpt-6.1-sol/01a14c78-6e9f-7052-be70-ff68a7cc68d9 # header CLI
github_submitter_identity: null
independent_from_executor_session: true
review_axes: [spec, standards_security]
reviewed_sha: 8264089a14f79867091da2629edbf45a22854c39
reviewed_tree: bbbcb30ec09191e8f3390fdeea259abbdcef54ea
verdict: changes_requested
counts: {P0: 0, P1: 0, P2: 0, P3: 2}
# Assurance approval chưa được cấp; controller còn phải vận chuyển/validate receipt/state.
findings_open: [F04, F05]
findings_closed: [F01, F02, F03]
```

Bảng **chỉ các ô N1–N7 đã đổi** so lượt 2; N1/N2/N3/N5/N6 giữ kết luận trước, không làm lại ma trận lượt 1:

| Ô | Lượt 2 | Lượt 3 trên exact candidate |
|---|---|---|
| N4 | Chưa có finding từ ca cảnh báo tên thường/một bản ghi | **Còn F04/F05 P3**: định dạng tên quote lệch mẫu spec; một run lặp bị đếm hai run. Script độc lập xác nhận 2+3 biểu hiện, 5 đối chứng đúng. Cần executor vá trong packet theo chỉ thị hết P3 |
| N7 / dot-bien | F03 P2, 39 mutant/92 ô gồm 1 ô traceback được runner nhận tín dụng; 394 ca | **F03 ĐÃ ĐÓNG**: giữ 394 ca (92 kg), không xoá ca; 38 mutant/91 ô kg hợp lệ; full suite 393/393 + 1 skipped, TỔNG: ĐẠT, rc=0. Các regression N4 mới chưa có trong catalog, HINT ở F04/F05; không dùng xanh của suite hiện có để đóng N4 |
