verdict: changes_requested

Đã hoàn tất review lượt 4 theo lớp A–E; kết luận và bảng ô đổi nằm cuối tệp.

## Preflight — wp788 r1/g1, review lượt 4

- `reviewed_sha`: `47591ebc51af917523e67191b2e96939506b78fe`; tree `e61829cd9fd0c97e5e58a7bd040b4f7b2af26413`. Detached HEAD, origin `https://github.com/ducthangho/tra-luat`; tracked diff/index sạch. Các tệp `.review/` là input/output được giao, `.codex/` đã ignored.
- Spec authoritative của lượt này là `.review/SPEC.md`, SHA-256 `82dc170446c3a4431739a3effbec8cb55adadc13d69f5c510f8782a2b45eb54e`, khớp assignment. Ba verdict cũ đều khớp hash giao. Baseline spec `d8b15cb0730c85e7019aee627c3bfa645a6d3eaf`, nền diff được giao `d347d426334bbe1bbb1161184ab0acffee9be054`; không tự dời baseline. Lookup phụ `git show d8b15cb:ops/specs/wp788.md` không có path, không dùng pipeline sha256 rỗng làm xác minh spec; nguồn review là tệp có hash được chỉ định.
- Vai Reviewer độc lập, class `sensitive`, hai trục `spec` và `standards_security`. Effective write set sản phẩm: `.claude/dev/packet_loop.py`, `.claude/dev/packet_loop_test.py`; không sửa các tệp đó. Chỉ ghi verdict/suite output được giao trong `.review/`, scratch `/tmp/wp788-review4-jacqWNTc` ngoài kho.
- Authority offline: `prompt.snapshot` run `77982f5bffe44943877903b9a3aa0083`, SHA-256 `2915699c907f823c957628de1c718f5c9c0382e112a4dbf60348524e8aa0207e`; chỉ thị tiếp tục và hết P1/P2/P3 thắng trần cũ trong tài liệu. Không dùng prompt thành lease viết/land. Revision/generation theo spec/lịch sử assignment; lease/state/budget live không đo do cấm mạng/GitHub.
- Reviewer `openai_codex / openai / codex_cli / machine`; header đúng run: Codex `0.163.0`, model `gpt-6.1-sol`, effort `xhigh`, session `01a14c8b-27ea-7b73-81f2-3fde65999e21`. Header chỉ là nhận dạng CLI công bố, không chứng minh từng request. Executor họ Claude theo spec; chưa được cấp runtime receipt executor. Submitter GitHub: null.
- Runtime Linux, Python 3.13.16, Ruff 0.15.15, core.abbrev=7. Sandbox thực `workspace-write`, không khai OS read-only. Không có tool `environment_status`; không mạng, doctor hay credential probe. Python dùng `-B`/`PYTHONDONTWRITEBYTECODE=1`, cache/output ngoài checkout.
- Suite bắt đầu ngay: `python -B .claude/dev/packet_loop_test.py > .review/suite.out 2>&1`, session 10183, đang chạy; chưa tính pass. Snapshot Git đầu được đo trước suite, snapshot nội dung toàn cây bắt đầu sau khi đọc tài liệu; sẽ so cuối, không suy rằng hai mốc chứng minh toàn lịch sử không ghi. Phạm vi quan sát chỉ checkout reviewer.

Raw evidence: `preflight.json`, `inputs.json`, `snapshot-start.json`, `full-diff.patch`, `new-diff.patch` trong scratch.

## Lớp A — ĐỐI CHIẾU LƯỢT TRƯỚC

Đã tạo dữ liệu bằng `python -B -c 'import json; …'` và gọi CLI thật trong từng subprocess; wrapper rc=0. Mã đầy đủ để chạy lại ở `/tmp/wp788-review4-jacqWNTc/layer-a-generator.txt`; `layer-a.json` lưu argv (kể cả suite 4301 chữ số), JSON/path, rc, stdout/stderr và kỳ vọng.

| Finding | Phản chứng/đối chứng tự chạy | Kết quả hiện tại |
|---|---|---|
| F04 | Tên `reviewer's gate`, tên chứa chéo ngược, cả hai dấu nháy, tên ngoài ASCII | 4/4 rc=0; stderr exact mẫu nháy đơn, tên giữ nguyên. Các biểu hiện lượt 3 đã đóng; việc đóng toàn lớp còn đối chiếu tác dụng bỏ `!r` ở C |
| F05 | Bản lặp cùng trang, xuyên trang, lặp có trạng thái ngoài suite khác nhau | 3/3 rc=0, đúng `1 run … (2)`; hai id thật 2/3 đúng `2 run … (2, 3)`; bản failure trùng id trong suite neo vẫn rc=12 đúng `conclusion='failure'`. **ĐÃ ĐÓNG / ĐÃ VÁ THẬT** |
| F01 | Cùng id=1 khác suite (1/9), count đúng 1 | rc=12 + `mang hai danh tính`, không traceback. Giữ **ĐÃ VÁ THẬT** |
| F02 | Suite hợp lệ về dạng, 4301 chữ số | rc=12 + `VẮNG`, không traceback. Giữ **ĐÃ VÁ THẬT** |
| F03 | Crash mutant không còn trong catalog; ca nền và companion đổi màu còn | Xác nhận catalog đạt; đóng toàn audit sau D, không nhận xoá tên làm bằng chứng đầy đủ |

Tổng lớp A: 11 CLI probes + 1 kiểm catalog đều đạt kỳ vọng; không dùng suite tổng thay bằng chứng từng finding.

## Lớp B — diff mới, toàn packet, chú thích

`git diff 8264089a14f79867091da2629edbf45a22854c39 HEAD` rc=0: formatter N4 bỏ `!r`, projection cảnh báo lấy set id trước sort; thêm hai bước test N4 và hai mutant, rút gọn 5 khối chú thích. Đã đối chiếu từng chú thích với mã: N2 vẫn kiểm mọi phần tử; F01 kiểm identity trước lọc; total_count=1 có chủ ý để mutant bỏ phần tử đổi màu; crash mutant F03 đã bỏ. Không tìm câu rút gọn nào nói sai hành vi.

`git diff --numstat d347d426334bbe1bbb1161184ab0acffee9be054 HEAD` rc=0:

```text
51      10      .claude/dev/packet_loop.py
248     16      .claude/dev/packet_loop_test.py
```

**2 tệp / 299 dòng thêm / 26 dòng xoá**, trong trần ≤3 tệp/≤300 dòng thêm, đúng write set. `git diff --check` cùng hai OID rc=0, output rỗng. Raw hai diff và command/rc ở scratch.

## Lớp C — toàn bộ diff, H3 và tác dụng của formatter mới

Đã đọc toàn bộ diff d347→candidate: `_doc_check_runs`, `cmd_kiem_gate`, parser/help, helper `_kg_dem/_kg_ca`, tất cả ca/fixture/MUTANTS thay đổi và ma trận codepage. Không chỉ đọc delta lượt 4.

- 21 probe JSON/CLI identity/state: 12 biến thể đổi name/suite/head, hai thứ tự × một/hai trang đều rc=12 đúng `mang hai danh tính`; 6 bản trùng cùng identity nhưng status/conclusion không xanh đều rc=12; 3 đối chứng duplicate nhất quán/metadata không dùng/rerun cũ đỏ mới xanh đều rc=0. Wrapper rc=0, **21/21**; raw `layer-c-identity.json`. Không tìm H3 mới; **H3 giữ 4**, không chạm 5.
- Helper count chỉ điền khi thiếu, dùng bản sao và giữ count cố ý sai; ca thiếu count có `dem=False`; raw JSON tránh helper ở ca parser. Ca thiếu conclusion cố định count để mutant bỏ phần tử không bị N5 che. Suite bool mặc định 1 làm mutant đổi màu. Fixture giữ 32 id/14 context, app/suite/cancelled; comment 30 run nêu snapshot spec, không là count hiện tại.
- F04 các tên in được (nháy đơn/đôi/chéo ngược/Unicode) đúng mẫu, nhưng bỏ repr mở lại lỗi xuống dòng dưới đây. F05 dedup chỉ projection cảnh báo, không mất bản trùng failure ở luật xanh.

### F04 — `warning-name-repr-not-spec-literal` — VÁ SINH LỖI MỚI / CHƯA ĐÓNG

- **P3**; trục **Spec/Standards**; lớp giữ slug lịch sử `warning-name-repr-not-spec-literal`; `.claude/dev/packet_loop.py:2345`, `cmd_kiem_gate`; test liên quan `.claude/dev/packet_loop_test.py:5473`.
- N4 yêu cầu đúng một dòng mỗi tên. `--bat-buoc` chỉ cấm chuỗi trống; `name` JSON chỉ đòi string, nên tên chứa LF/CR vẫn là đầu vào được nhận. Formatter mới nội suy nguyên văn các ký tự xuống dòng vào stderr. Tên `gate` + LF + `next`, hai run success id1/suite1 và id2/suite9, count=2, trả rc=0 nhưng stderr có **2 LF / 2 dòng**, thay vì một dòng N4:

```text
CẢNH BÁO: 'gate
next' có 1 run ở suite khác (2) — bỏ qua
```

- Phản chứng chạy thật `layer-c-names.json`: LF, CR, CRLF, U+2028, U+2029 đều bị tách thành 2 dòng (`splitlines()`); LF/CRLF còn có 2 byte LF thực, không phụ thuộc cách hiểu Unicode. Tab/tên thường/chuỗi hai ký tự chéo ngược+n vẫn một dòng. Wrapper kiểm 8 ca rc=1 (**5 lỗi / 3 đối chứng**), CLI từng ca rc=0, không traceback. JSON và đối số chỉ là dữ liệu chuỗi, không thực thi shell.
- Đây là biểu hiện mới do fix cùng lớp formatter F04, **không tạo H3 hay finding riêng**, không đổi màu luật gate. Biểu hiện nháy đơn/chéo ngược cũ đã sửa thật, nhưng chưa đóng cả lớp N4. Bản `!r` trước giữ tên chứa LF trên một dòng; C sẽ đối chứng trực tiếp phiên bản trước trong scratch.
- **HINT — ở đâu/thế nào:** xử lý hiển thị tại formatter N4 và test `case_kg_n4_canh_bao`; giữ nguyên tên dùng lọc và danh sách id. Cần quy tắc hiển thị một dòng cho ký tự ngắt dòng, đồng thời giữ nháy đơn cố định và các ký tự in được nguyên văn. Spec hiện chỉ ghi mẫu literal, chưa định nghĩa escaping control characters: executor/owner phải chốt rõ chính sách đó, hoặc quyết định hạn chế miền tên ở CLI; reviewer không tự chọn chính sách thay authority. Không quay lại `!r` nguyên khối vì tái mở nháy/chéo ngược; không thay ký tự trước phép so tên.
- **Test khóa:** tên có LF/CR/CRLF và Unicode line separator; assert toàn stderr chỉ một dòng, đúng chuỗi theo chính sách đã chốt, rc không đổi so dữ liệu tên thường. Giữ các đối chứng nháy/chéo ngược/Unicode thường và hai id thật. Mutant nội suy raw tên trở lại phải làm ca LF đỏ vì số dòng/chuỗi, không traceback.
- **Nguy cơ:** escaping không phân biệt chéo ngược+n với LF làm tên chẩn đoán mơ hồ; escape toàn bộ bằng repr tái tạo lỗi lượt 3; sửa tên gốc hoặc dedup toàn bộ runs có thể phá so khớp/N3. Nếu owner chọn từ chối newline, cần khai đó là thay đổi miền CLI có quyết định, không lặng lẽ thêm giới hạn.

Tất cả biểu hiện formatter đã gom trong F04; không báo tách 5 finding. H1/H3 không tăng vì đây là lỗi trình bày. Tiếp tục audit D và gate E đầy đủ theo assignment.

### Đối chứng phiên bản và phản chứng F04 chạy lại được

`PYTHONDONTWRITEBYTECODE=1 python -B -W ignore /tmp/wp788-review4-jacqWNTc/audit.py`, rc=0: trong một lần gọi, copy đúng blob lượt 3 vào scratch rồi gọi hai phiên bản với cùng JSON/argv/runtime. `n4-before-after.json`: cả 5 tên LF/CR/CRLF/U+2028/U+2029 **lượt 3: 1 dòng → lượt 4: 2 dòng**, rc cả hai vẫn 0. Đối chứng tên thường/chuỗi chéo ngược+n: 1→1 dòng. Phép này xác nhận hồi quy do đổi formatter, không dùng baseline để chứng minh mẫu nháy lượt 3 đúng.

Reproducer tối thiểu (chạy từ root checkout, không ghi mã sản phẩm):

```python
import json, subprocess, sys, tempfile
from pathlib import Path
h, name = 'ab' * 20, 'gate' + chr(10) + 'next'
f = Path(tempfile.mkdtemp(prefix='wp788-n4-')) / 'runs.json'
f.write_text(json.dumps({'total_count': 2, 'check_runs': [
    {'id': i, 'name': name, 'head_sha': h, 'status': 'completed',
     'conclusion': 'success', 'check_suite': {'id': s}}
    for i, s in [(1, 1), (2, 9)]]}), encoding='utf-8')
p = subprocess.run([sys.executable, '-B', '.claude/dev/packet_loop.py',
    'kiem-gate', '--head', h, '--check-suite', '1', '--check-runs', str(f),
    '--bat-buoc', name], capture_output=True)
print(p.returncode, p.stderr.count(b'\n'), p.stderr.decode().splitlines())
assert p.returncode == 0
assert len(p.stderr.decode().splitlines()) == 1, 'N4 đòi đúng một dòng'
```

Kết quả đã đo: `0 2 [...]`, assertion một dòng đỏ (chi tiết JSON/CLI ở `layer-c-names.json`); đây là phản chứng diagnostics, không là mutant nhận tín dụng trong D.

## Lớp D — audit TOÀN BỘ bảng đột biến trong một lượt

Lệnh thực: `bash .review/mut_all.sh "$PWD/.claude/dev" kg_ /tmp/wp788-review4-jacqWNTc/mutants > /tmp/wp788-review4-jacqWNTc/mut_all.out 2>&1`; thư mục output đã tạo trước redirect; session 58375 kết thúc **rc=0**.

Đã đọc **từng ô**, đối chiếu payload/tập ca với catalog, kiểm không chỉ nhãn AssertionError mà cả thay đổi rc/lý do/chuỗi. **40 mutant / 93 ô, 93 bắt đúng chốt, 0 sống, 0 traceback, 0 lỗi setup/import**. 40 `.err` đều rỗng, không `.pyc/.pyo`. Raw đầy đủ `mut_all.out`, `mutation-audit.json`; `audit.py` rc=0 xác nhận coverage và inventory. Không ô sai chốt để gom thành finding mới.

38 mutant / 91 ô cũ giữ kết quả lượt 3; không đổi tập ca của mutant cũ. Chi tiết chỉ hai ô mới:

| Mutant / ca | Lượt 3 | Lượt 4 |
|---|---|---|
| `kg_n4_dem_ban_ghi` / `kg_n4_canh_bao` | Chưa có | **Bắt đúng**: `AssertionError: bản lặp là MỘT run: rc=0 ["CẢNH BÁO: 'gate' có 2 run ở suite khác (2, 2) — bỏ qua"]` |
| `kg_n4_ten_theo_repr` / `kg_n4_canh_bao` | Chưa có | **Bắt đúng**: `AssertionError: tên nguyên văn: rc=0 [...]`, actual dùng nháy kép quanh `reviewer's gate` thay vì nháy đơn cố định |

F03 **ĐÃ ĐÓNG / ĐÃ VÁ THẬT**: crash mutant vẫn vắng; companion `kg_f02_du_phong_khop_nham` vẫn bị bắt vì **12→0**, không traceback. Ca nền F02 đạt ở A. Audit không cấp tín dụng exception vô can. Catalog so exact blob lượt 3: **394→394 ca**, không mất ca; chỉ thêm hai mutant nêu trên. Bảng mutant hiện có không kiểm newline, nên kết quả D không đóng F04.

## Lớp E — gate và parity nhẹ

Suite session 10183 còn chạy khi ghi mục này; chưa nhận pass trước terminal rc/marker.

Các kiểm nhẹ dựng baseline/candidate bằng hai clone ngoài kho trong **một** `gates.py`, cùng bootstrap, origin endpoint thật, core.abbrev=7. Không gọi remote. Đây là đo parity theo spec, không là admission/CI authority.

| Command (cwd từng clone) | d347 baseline | Candidate | Đánh giá |
|---|---|---|---|
| `python -B -m ruff check --no-cache --select F .claude/dev/packet_loop.py` | rc=1, 1 F841 biến `n` dòng 1804 | rc=1, cùng 1 F841 | Bare lint **failed nền**; **DELTA=0**, đạt tiêu chí spec |
| `python -B .claude/dev/packet_loop.py doctrine-scan --root .` | rc=0, 10 tệp / 0 chỗ chép doctrine | rc=0, cùng output | passed parity |
| `python -B .claude/dev/packet_loop.py adr-song --root .` | rc=0, 53 ADR / 53 dòng | rc=0, cùng output | passed parity |

`gates.py` rc=0; command/rc/stdout/stderr/identity đầy đủ ở `gates-delta.json`. Ruff pin/probe workflow contract `not_run`, không suy từ bare lint.

`acceptance-catalog.json`: baseline 352 ca (50 kg), candidate 394 ca (92 kg), `removed=[]`, `added_non_kg=[]`. Không mất ca cũ hoặc thêm/sửa hành vi lệnh ngoài `kiem-gate`; màu ca trên candidate đợi full suite.

### Khép phạm vi lớp formatter và đối chiếu lớp cũ

Đã chạy thêm toàn lớp ngắt dòng mà `str.splitlines()` (cũng là hàm ca N4 sử dụng) nhận diện: quét codepoint Unicode rồi đo CLI với **10 separator** U+000A, U+000B, U+000C, U+000D, U+001C, U+001D, U+001E, U+0085, U+2028, U+2029 và chuỗi CRLF (**11 biến thể**). `python -B /tmp/wp788-review4-jacqWNTc/linebreak-class.py`, rc=0: **11/11** trước=1 dòng, sau=2 dòng; rc sản phẩm đều 0. `linebreak-class.json` giữ từng argv/output; toàn bộ gom trong F04, không thêm 11 finding.

`python -B /tmp/wp788-review4-jacqWNTc/repro-f04.py > /tmp/wp788-review4-jacqWNTc/repro-f04.out 2>&1` trả **rc=1** do assertion cuối, output `0 2 [...]` đúng đoạn tái hiện ở C. Traceback trong tệp này là assertion của script phản chứng ngoài bảng D; CLI sản phẩm không traceback và script này **không nhận tín dụng mutant**.

| Slug lớp | Finding / nguồn | Trạng thái candidate | Phép đo / hướng xử lý |
|---|---|---|---|
| `bang-chung-dau-vao-tin-qua-muc` | F01 lượt 1 `e995730464da03223cf636e49ad32e220c6ec720` | **ĐÃ VÁ THẬT** | A + 21 probe C; H3 giữ 4; D identity vẫn có răng |
| `cli-decimal-conversion-unhandled` | F02 lượt 1 cùng SHA | **ĐÃ VÁ THẬT** | A suite 4301 chữ số 12+VẮNG không traceback, D companion 12→0 |
| `mutation-credit-traceback-contract` | F03 lượt 2 `4ffae005eb1c434d660cbfb713ad21ed92115a8a` | **ĐÃ VÁ THẬT** | Toàn D 40/93 đúng chốt, crash mutant không trở lại |
| `warning-name-repr-not-spec-literal` | F04 lượt 3 `8264089a14f79867091da2629edbf45a22854c39` | **CHƯA ĐÓNG / VÁ SINH LỖI MỚI, P3** | Nháy/chéo ngược cũ đóng; 11 biến thể ngắt dòng cùng formatter sai một dòng; owner/executor xử lý chính sách hiển thị + test theo HINT C |
| `warning-count-records-not-distinct-runs` | F05 lượt 3 cùng SHA | **ĐÃ ĐÓNG / ĐÃ VÁ THẬT** | Lặp cùng/xuyên trang/status mutable đếm 1; hai id thật đếm 2; N3 giữ bản failure; mutant list bị bắt đúng |

5 lớp được theo dõi; **1 lớp/finding P3 mở**, không lớp mới. F04 tái mở ở cùng slug vì bản vá formatter sinh lỗi mới; không đổi khóa để reset lịch sử. Hai lớp mở U từ lượt 3 là F04/F05; F được xác minh đóng toàn lớp chỉ có F05: **1/2 = 50%**, không phải cả hai đã đóng và không dưới 50%. F04 có finding ở hai lượt (3/4); chưa thành lần thứ ba. Chỉ thị hết cả P3 tiếp tục chặn approve.

## Giới hạn và trạng thái chưa đo

- `not_run/not_measured`: CI trên head cuối, phép `tu-do` với JSON thật của head này, Windows execution, connector completion, refs/state/lease/budget live, merge authorization, runtime receipt executor và delivery receipt/state transition. Assignment cấm mạng/GitHub; fixture bb8c0c4 và suite local không chứng minh các mục ấy. Không dùng thiếu bằng chứng này thành pass.
- Ruff pin/probe workflow contract `not_run`; bare lint và delta có kết quả riêng ở E. Không thay đổi workflow, release artifact, golden, manifest hay đường security ngoài write set.
- Snapshot nội dung phủ cả untracked/ignored ngoài `.git/.review`, trừ 9 path có tên thuộc vùng hạn chế đọc theo CLAUDE.md. Phần đó `not_measured` về nội dung, không suy sạch byte; Git diff/index vẫn được đo. Chỉ quan sát checkout reviewer, không kho executor nguồn. Hai mốc không chứng minh chưa từng ghi rồi hoàn nguyên giữa mốc; sandbox thực là workspace-write.
- Raw input prompt/spec/verdict cũ có hash ghim; output cục bộ cần controller kiểm terminal run/rc và băm lại sau khi phiên kết thúc nếu vận chuyển. Không có GitHub submitter trong phiên này; artifact không tự đổi state, không tự tạo `cross_approved` hay quyền merge/land/deploy/LIVE.


## Kết quả terminal lớp E và toàn vẹn cuối

Session **10183** kết thúc với **exit_code=0** do công cụ tiến trình trả trực tiếp, không suy rc từ file output. `suite-completion.json` neo command/rc/SHA/tree/hash. Marker thực:

```text
  BỎ QUA  luong_canonical_chay_that: chỉ đo lệnh pwsh trên Windows
nền: 393/393 đạt · BỎ QUA: 1
  BỎ QUA  đột biến luong_canonical_chay_that_dao_os_name: ca ['luong_canonical_chay_that'] không được tính là đã giết
  ok  kg_n4_dem_ban_ghi → giết 1 ca đích · 3 đối chứng khác họ còn sống
  ok  kg_n4_ten_theo_repr → giết 1 ca đích · 3 đối chứng khác họ còn sống
  ok  78 lớp lách đều có đột biến giết · 6 đột biến PHỐI HỢP · 0 ngoại lệ
  ca               : 394
  đột biến         : 167
  lớp lách         : 78
  ca bắt-oan       : 35
  ngoại lệ AC 18   : 0
TỔNG: ĐẠT
```

394/167 là số catalog runner in; không gọi mutant Windows skipped là đã chạy/đã giết. Audit kg riêng D là 40 mutant/93 ô; không nhầm 167 toàn catalog với 40 kg được audit độc lập.

- **passed:** suite Linux rc=0, 393/393 và TỔNG: ĐẠT; A 11 CLI + kiểm catalog; C 21 probe identity/state; D 40/93 đúng chốt; diff/write set/kích thước 2/299; Ruff delta=0; doctrine/ADR parity. Hai phép A/B formatter xác nhận hồi quy đúng kỳ vọng đo, không gọi hành vi N4 hiện tại là pass.
- **failed:** F04 P3 về một dòng N4 (11 biến thể ngắt dòng cùng lớp); script tối thiểu rc=1 do assertion cuối, CLI không traceback; bare Ruff rc=1 có sẵn cả hai cây, delta=0.
- **skipped:** 1 ca Windows thực và mutant phụ thuộc; không cấp tín dụng execution Windows.
- **not_run/not_measured:** các mục live/CI/head cuối/receipt/authority, Windows và Ruff contract đã khai; không chuyển chúng thành pass.

Snapshot cuối 2026-10-18T01:15:19.412573+00:00: **3671 tệp** đã băm trong phạm vi ngoài `.git/.review`, gồm untracked/ignored, delta thêm/xoá/nội dung đều `[]`; 9 path hạn chế không đọc nội dung. Input prompt/spec/verdict cũ/helper không đổi hash. HEAD/tree đầu–cuối khớp, `git diff --exit-code` và `git diff --cached --exit-code` đều rc=0, output rỗng. Untracked chỉ `.review/` được giao; ignored `.codex/` giữ nguyên. `snapshot-end.json` và `final-snapshot.py` lưu phép đo.

Manifest artifact ổn định: `/tmp/wp788-review4-jacqWNTc/artifacts.json`. Một số mỏ neo:

| Artifact | Bytes | SHA-256 |
|---|---:|---|
| `/tmp/claude-0/-home-user-tra-luat/aec15584-50e8-55b9-b3a8-d6a2cfe55128/scratchpad/rv4/.review/suite.out` | 20096 | `ef4e6d02bcded4363b59033de19b3d74910884fc9f5bf2b59be965b192a84451` |
| `/tmp/wp788-review4-jacqWNTc/mutation-audit.json` | 28655 | `1a11a076f4351822d720f511e49fa6e43467db99197b631298bc381b2a8d62e5` |
| `/tmp/wp788-review4-jacqWNTc/linebreak-class.json` | 13675 | `63a4a9e3f617f3f1b36b98127974a28830290d6ac035b7067b312a6d2268c281` |
| `/tmp/wp788-review4-jacqWNTc/n4-before-after.json` | 8242 | `edfaa9db13908ea8973c323b025c5b8bbbd20b145b7e9778564689438ae647c9` |
| `/tmp/wp788-review4-jacqWNTc/snapshot-end.json` | 673348 | `312a908cec3fab8437bbf9f54e7ee4e581c855804f8f89afaca016da737b127b` |

## Kết luận

Áp chỉ thị chặt hơn của assignment: hết cả P1/P2/P3 mới approve. F01/F02/F03 giữ đóng, **F05 ĐÃ ĐÓNG**, **F04 CHƯA ĐÓNG — VÁ SINH LỖI MỚI**. Không có H3 mới, H3 giữ 4. Suite xanh không đóng phản chứng N4. Verdict **changes_requested**, không là approval/merge/land authorization.

```yaml
packet_id: wp788
revision: 1
generation: 1
role: reviewer
provider: openai_codex
model_family: openai
model: gpt-6.1-sol # header CLI của đúng run, không đo mọi request
effort: xhigh # header CLI
execution_surface: codex_cli
transport: machine
session_id: 01a14c8b-27ea-7b73-81f2-3fde65999e21
run_id: 77982f5bffe44943877903b9a3aa0083
model_reviewer_identity: openai_codex/gpt-6.1-sol/01a14c8b-27ea-7b73-81f2-3fde65999e21
github_submitter_identity: null
independent_from_executor_session: true
review_axes: [spec, standards_security]
reviewed_sha: 47591ebc51af917523e67191b2e96939506b78fe
reviewed_tree: e61829cd9fd0c97e5e58a7bd040b4f7b2af26413
verdict: changes_requested
counts: {P0: 0, P1: 0, P2: 0, P3: 1}
findings_open: [F04]
findings_closed: [F01, F02, F03, F05]
# Không cấp approval assurance; receipt/state do controller xử lý sau khi run kết thúc.
```

Bảng **chỉ các ô N1–N7 đã đổi so lượt 3**; N1/N2/N3/N5/N6 giữ kết luận trước:

| Ô | Lượt 3 | Lượt 4 trên exact reviewed_sha |
|---|---|---|
| N4 | F04 P3 nháy/chéo ngược lệch mẫu; F05 P3 đếm bản ghi lặp như hai run | Nháy/chéo ngược/Unicode in được đúng mẫu; **F05 đóng** với duplicate và 2 id thật. **F04 còn 1 P3**: bỏ `!r` làm 11 biến thể ngắt dòng phá một dòng; cùng slug, không nâng H3 |
| N7 / dot-bien | 394 ca (92 kg), 165 mutant; audit kg 38/91; chưa có regression F04/F05 | 394 ca (92 kg) giữ đủ; thêm 2 bước trong ca N4 + 2 mutant có răng, catalog 167/audit kg **40/93 đúng chốt**. Full Linux 393/393 + 1 skipped, TỔNG: ĐẠT, rc=0. Còn thiếu test cho miền ngắt dòng F04 theo chính sách được owner chốt |
