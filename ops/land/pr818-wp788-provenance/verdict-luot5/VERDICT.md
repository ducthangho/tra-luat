verdict: approve

# Cross-review lượt 5 — wp788 (#788)

- Vai trò: Reviewer độc lập; provider: openai_codex; model_family: openai; execution_surface: codex_cli; transport: machine.
- Không gọi mạng/GitHub; chỉ ghi artifact .review được người dùng yêu cầu; mã nguồn review read-only.
- Đang kiểm preflight và lớp A–E.

## Preflight

- Candidate `984032f375aa0c8fe6039dfd35f6842acd49c926`, tree `ca01ca9b18b840fbb56668aab28adb9885f97005`; exact HEAD khớp, detached. Origin `https://github.com/ducthangho/tra-luat`. Tracked/index sạch, untracked chỉ `.review/`, ignored `.codex/`.
- Packet wp788 r1/g1 theo assignment và lịch sử review; spec authoritative offline `.review/SPEC.md`, SHA-256 `82dc170446c3a4431739a3effbec8cb55adadc13d69f5c510f8782a2b45eb54e`, khớp. Hash bốn verdict trước đều khớp chỉ thị.
- Mốc spec `d8b15cb0730c85e7019aee627c3bfa645a6d3eaf`; nền diff được giao `d347d426334bbe1bbb1161184ab0acffee9be054`; candidate như trên. Không dời baseline.
- Authority review offline: prompt.snapshot run `b8b00f3d9d0a4a96911df056671375d9`, hash `cd7689e8e3d2a7c388f478d702d83950cb802a88755fb19a62422ed4821b4fdb`. Chủ kho cho tiếp tục đến hết P1/P2/P3, miễn trần 300 dòng thêm, chốt từ chối ký tự splitlines trong --bat-buoc. Không dùng prompt thành lease ghi/land; lease/state/budget live chưa đo vì cấm mạng/GitHub.
- Class `sensitive`, review_axes `[spec, standards_security]`. Effective write set sản phẩm đúng hai path `.claude/dev/packet_loop.py`, `.claude/dev/packet_loop_test.py`; cả hai read-only trong review. Chỉ ghi artifact được giao `.review/VERDICT.md`, `.review/suite.out`; scratch ngoài repo `/tmp/wp788-review5.DEwL1y7g`.
- Runtime Linux, Python 3.13.16, Ruff 0.15.15; core.abbrev=7. Sandbox thực workspace-write, không giả OS read-only. Header đúng run: Codex 0.163.0, model `gpt-6.1-sol`, effort `xhigh`, session `01a14ca3-86eb-7023-906e-1602c6522634`; header chỉ chứng minh CLI công bố. Executor họ Claude theo spec, runtime receipt executor chưa được cấp. GitHub submitter null, context reviewer độc lập.
- Không có tool environment_status được cung cấp; không chạy doctor/credential probe/mạng theo scope. Snapshot đầu lưu cả tracked/untracked/ignored ngoài .git/.review sau khi đọc tài liệu, không chứng minh toàn lịch sử run; `snapshot-start.json` băm 3680 tệp. Chỉ quan sát checkout reviewer, không kho executor nguồn.
- Gate nền bắt đầu ngay: `python -B .claude/dev/packet_loop_test.py > .review/suite.out 2>&1`, exec session 99742. Đang chạy, chưa khai pass.

## Lớp A — ĐỐI CHIẾU LƯỢT TRƯỚC

`PYTHONDONTWRITEBYTECODE=1 python -B -W ignore /tmp/wp788-review5.DEwL1y7g/layer_a.py`: 31/31 CLI probe đúng kỳ vọng. Lệnh đầu rc=1 do lỗi phép đo membership trên list tuple CASES; đã sửa phép kiểm sang dict(CASES), kiểm lại raw CLI và catalog, rc=0. Đây là lỗi rig, không là finding sản phẩm; không cấp tín dụng traceback ấy. Script đã sửa lưu ngoài kho, dữ liệu từng argv/input/rc/stdout/stderr ở `layer-a.json`.

| Finding | Đo độc lập trên candidate | Trạng thái |
|---|---|---|
| F04 `warning-name-repr-not-spec-literal` | 11 biến thể U+000A/000B/000C/000D/001C/001D/001E/0085/2028/2029/CRLF: ở --bat-buoc đều rc=2 + “xuống dòng”; ở name JSON với --bat-buoc sạch đều rc=0, stderr exact một dòng cảnh báo gate, không tách dòng. 6 đối chứng tab, chéo ngược+n, nháy đơn/đôi/cả hai+chéo ngược, Unicode in được đều rc=0, cảnh báo đúng mẫu nguyên văn | **ĐÃ VÁ THẬT** ở mọi biểu hiện lượt 4; kiểm hồi quy miền tên tiếp tại C |
| F01 `bang-chung-dau-vao-tin-qua-muc` | Cùng id khác suite, count đúng: rc=12 + “mang hai danh tính”, không traceback | Giữ **ĐÃ VÁ THẬT** |
| F02 `cli-decimal-conversion-unhandled` | Suite 4301 chữ số: rc=12 + VẮNG, không traceback | Giữ **ĐÃ VÁ THẬT** |
| F03 `mutation-credit-traceback-contract` | Crash mutant vắng; ca regression và companion đổi màu còn. Audit mọi ô ở D trước khi đóng toàn lớp | Đối chiếu catalog đạt, chờ D |
| F05 `warning-count-records-not-distinct-runs` | Cùng run ngoài suite lặp xuyên trang, total_count=2: rc=0, exact `1 run … (2)` | Giữ **ĐÃ VÁ THẬT** |

## Lớp B — diff mới và kích thước

`git diff 47591ebc51af917523e67191b2e96939506b78fe HEAD` rc=0: đúng một commit thêm kiểm `t.splitlines() != [t]`, bổ sung thông báo RC_ARG, 12 ca F04, một mutant mới và mở tập đích mutant tên rỗng. Không thay lọc tên/suite hoặc formatter N4. Chú thích mới đúng: mọi tên đã qua kiểm giữ `splitlines()==[t]`; cảnh báo N4 chỉ lấy tên từ ten_bb đã kiểm, tên JSON ngoài tập không được in trong N4.

`git diff --numstat d347d426334bbe1bbb1161184ab0acffee9be054 HEAD` rc=0:

```text
55      12      .claude/dev/packet_loop.py
261     18      .claude/dev/packet_loop_test.py
```

2 tệp, **316 dòng thêm / 30 dòng xoá**, đúng write set. Trần 300 đã được chủ kho miễn theo assignment; không ghi finding về kích thước. Raw `new-diff.patch`, `full-diff.patch` nằm trong scratch.

## Lớp C — rà toàn bộ diff và H3

Đã đọc toàn bộ diff d347→candidate (cả mã và tests), không giới hạn delta lượt 5: `_doc_check_runs`, `cmd_kiem_gate`, parser/help; helper đếm, schema/identity/producer/count, fixture thật, catalog mutant và codepage stdout. `git diff --check d347d426334bbe1bbb1161184ab0acffee9be054 HEAD` rc=0, output rỗng.

`PYTHONDONTWRITEBYTECODE=1 python -B /tmp/wp788-review5.DEwL1y7g/layer_c.py` rc=0, **69/69 CLI probes** + help rc=0 (`layer-c.json`):

- Tên rỗng/chỉ khoảng trắng: 5 ca đúng RC_ARG; 5 tên hợp lệ có khoảng trắng biên/tab/nháy/chéo ngược/Unicode vẫn khớp tuyệt đối, tên lặp chỉ xuất hiện một lần trên dòng XANH và một cảnh báo. Không strip/normalize tên dùng lọc.
- 11 separator ở ĐẦU/CUỐI tên, xen tên sạch và tên trùng: 22 ca đúng RC_ARG + xuống dòng, không traceback. Cùng với 22 probe giữa tên ở A phủ cả ba vị trí và đường JSON ngoài tập.
- 3 ca ĐỎ với newline ở status/conclusion/head dùng repr: stderr đúng hai dòng (một ĐỎ + tổng), không tách tên/lý do. 11 diagnostic identity chứa tên JSON ngắt dòng dùng tuple repr, stderr đúng một dòng; ca VẮNG với nháy/chéo ngược vẫn 12, không cảnh báo. Dòng XANH chỉ nội suy tên bắt buộc đã kiểm; không còn đường raw newline trong tên được in ở XANH/N4. JSON không bắt buộc có newline không vi phạm miền CLI, và không làm N4 in thêm. N4 không đặt hợp đồng một dòng cho mọi lỗi schema; các đường hiện đo cũng an toàn với chuỗi qua repr.
- H3: 3 trường identity × 2 thứ tự × 1/2 trang = 12 probe đều 12 + mang hai danh tính trước mọi lọc; 6 duplicate cùng identity khác trạng thái/kết luận đều đỏ; 4 đối chứng duplicate nhất quán, rerun hợp lệ, cảnh báo duplicate trạng thái khác, hai id cảnh báo thật đều đúng. Không tìm đường cấp xanh vượt evidence trong phạm vi `_doc_check_runs`/`cmd_kiem_gate`; **H3 giữ 4**, không lên 5.
- Help giữ đủ N6 (`--check-suite`, `actions/runs/`, `check_suite_id`, `filter=all`); chưa nhắc giới hạn newline ngay ở help --bat-buoc, nhưng thông báo RC_ARG đã nêu cụ thể ràng buộc mới. N6 không đòi help liệt kê miền tên; không có lời help khẳng định newline được nhận, không ghi P3 cho lựa chọn biên tập này.

`python -B /tmp/wp788-review5.DEwL1y7g/catalogs.py` rc=0: base **352 ca / 50 kg**, lượt 4 **394 / 92 kg**, candidate **406 / 104 kg**; tập ca mất so cả base/lượt 4 đều `[]`, ca thêm không-kg `[]`. Hai ca stdout vẫn có kiem-gate với suite/count mới. Mutant kg **40→41**, không mất mutant; chỉ kg_bo_kiem_ten_rong đổi anchor/tập đích và kg_f04_bo_kiem_xuong_dong mới. Fixture 32 run/14 context giữ app/suite/cancelled, không thay thế bằng chứng CI head cuối.

F04 đóng toàn lớp trong phạm vi đã đo, không sinh hồi quy miền tên; F01/F02/F05 giữ đóng. Không có finding P1/P2/P3 mới tại A–C. Chờ audit toàn bảng và terminal gate trước kết luận.

## Lớp D — audit TOÀN BỘ bảng đột biến trong một lượt

`bash .review/mut_all.sh "$PWD/.claude/dev" kg_ /tmp/wp788-review5.DEwL1y7g/mutants > /tmp/wp788-review5.DEwL1y7g/mut_all.out 2>&1` kết thúc **rc=0** (exec session 79530). `python -B /tmp/wp788-review5.DEwL1y7g/audit_mutations.py` rc=0, đối chiếu đủ catalog/tập ca, đọc từng kết quả và kiểm lỗi con, không tin rc cuối của shell wrapper.

**41 mutant / 113 ô**, toàn bộ bắt đúng chốt; **0 ô sống, 0 traceback, 0 setup/import error**, cả 41 tệp `.err` rỗng; không `.pyc/.pyo`. Đã kiểm lý do: thay đổi mã 12↔0, 2→12/0, 12→8, hoặc assertion đúng nội dung help/cảnh báo/suite; không cấp tín dụng chỉ vì có AssertionError. Raw `mut_all.out`, `mutation-audit.json` lưu mọi ô và message đầy đủ.

So lượt 4: **93 ô cũ giữ trạng thái bắt đúng**, **20 ô mới**. Chi tiết chỉ các ô mới dưới đây; ở mỗi hàng là HAI ô độc lập (mỗi mutant chạy một tiến trình riêng), lượt 4 chưa có ô đó:

| Ca | kg_bo_kiem_ten_rong | kg_f04_bo_kiem_xuong_dong |
|---|---|---|
| `kg_f04_xuong_dong_lf` | **Bắt đúng**: đòi rc=2, được rc=12 + VẮNG | **Bắt đúng**: đòi rc=2, được rc=12 + VẮNG |
| `kg_f04_xuong_dong_cr` | **Bắt đúng**: đòi rc=2, được rc=12 + VẮNG | **Bắt đúng**: đòi rc=2, được rc=12 + VẮNG |
| `kg_f04_xuong_dong_crlf` | **Bắt đúng**: đòi rc=2, được rc=12 + VẮNG | **Bắt đúng**: đòi rc=2, được rc=12 + VẮNG |
| `kg_f04_xuong_dong_vt` | **Bắt đúng**: đòi rc=2, được rc=12 + VẮNG | **Bắt đúng**: đòi rc=2, được rc=12 + VẮNG |
| `kg_f04_xuong_dong_ff` | **Bắt đúng**: đòi rc=2, được rc=12 + VẮNG | **Bắt đúng**: đòi rc=2, được rc=12 + VẮNG |
| `kg_f04_xuong_dong_fs` | **Bắt đúng**: đòi rc=2, được rc=12 + VẮNG | **Bắt đúng**: đòi rc=2, được rc=12 + VẮNG |
| `kg_f04_xuong_dong_nel` | **Bắt đúng**: đòi rc=2, được rc=12 + VẮNG | **Bắt đúng**: đòi rc=2, được rc=12 + VẮNG |
| `kg_f04_xuong_dong_ls` | **Bắt đúng**: đòi rc=2, được rc=12 + VẮNG | **Bắt đúng**: đòi rc=2, được rc=12 + VẮNG |
| `kg_f04_xuong_dong_ps` | **Bắt đúng**: đòi rc=2, được rc=12 + VẮNG | **Bắt đúng**: đòi rc=2, được rc=12 + VẮNG |
| `kg_f04_xuong_dong_cuoi` | **Bắt đúng**: đòi rc=2, được rc=12 + VẮNG | **Bắt đúng**: đòi rc=2, được rc=12 + VẮNG |

Ca cũ tên rỗng của kg_bo_kiem_ten_rong vẫn bắt đúng 2→12; việc đổi anchor theo guard mới không thay trạng thái ô ấy. Không ô sai chốt để gom thành finding mới. F03 **ĐÃ VÁ THẬT**: crash mutant vẫn vắng, ca nền F02 đúng 12+VẮNG, companion vẫn bị bắt bởi 12→0, stderr rỗng; không nhận traceback làm giết. N4 dedup và mẫu nháy giữ răng qua hai mutant có từ lượt 4.

## Lớp E — gate và parity nhẹ

Suite nền session 99742 vẫn đang chạy, chưa nhận pass trước terminal rc và marker tổng. `python -B /tmp/wp788-review5.DEwL1y7g/gates.py` rc=0, dựng hai clone ngoài repo trong MỘT lượt với cùng bootstrap, core.abbrev=7 và origin endpoint thật, chỉ clone từ đường dẫn local, không gọi remote. `gates-delta.json` lưu từng command/cwd/rc/output và identity.

| Command (cwd từng clone) | d347 baseline | Candidate | Đánh giá |
|---|---|---|---|
| `python -B -m ruff check --no-cache --select F .claude/dev/packet_loop.py` | rc=1, 1 F841 `n` dòng 1804 | rc=1, cùng 1 F841 | Bare lint failed nền, **DELTA=0**, đạt tiêu chí spec |
| `python -B .claude/dev/packet_loop.py doctrine-scan --root .` | rc=0, 10 tệp / 0 chỗ chép doctrine | rc=0, cùng output | passed parity |
| `python -B .claude/dev/packet_loop.py adr-song --root .` | rc=0, 53 ADR / 53 dòng, cùng ngoại lệ ADR-0016 | rc=0, cùng output | passed parity |

Ruff pin/probe workflow contract `not_run`, không suy từ bare lint. Phép parity local này không là admission/CI authority hay gate land.

## Bảng lớp và giới hạn

| Slug lớp | Finding / nguồn | Trạng thái trên candidate | Phép kiểm đóng lớp |
|---|---|---|---|
| `bang-chung-dau-vao-tin-qua-muc` | F01, lượt 1 `e995730464da03223cf636e49ad32e220c6ec720` | **ĐÃ VÁ THẬT** | A + C identity trước lọc/mọi trang, duplicate trạng thái, D mọi mutant F01; H3 giữ 4 |
| `cli-decimal-conversion-unhandled` | F02, lượt 1 cùng SHA | **ĐÃ VÁ THẬT** | A 4301 chữ số 12+VẮNG không traceback, D companion 12→0 |
| `mutation-credit-traceback-contract` | F03, lượt 2 `4ffae005eb1c434d660cbfb713ad21ed92115a8a` | **ĐÃ VÁ THẬT** | D 41 mutant/113 ô đúng chốt, crash mutant vắng, regression/companion còn |
| `warning-name-repr-not-spec-literal` | F04, lượt 3 `8264089a14f79867091da2629edbf45a22854c39`, tái mở lượt 4 `47591ebc51af917523e67191b2e96939506b78fe` | **ĐÃ VÁ THẬT** | A đủ 11 biến thể ở CLI/JSON + đối chứng, C biên/rỗng/whitespace/trùng/output, D 20 ô mới bắt đúng; chính sách miền tên do chủ kho chốt |
| `warning-count-records-not-distinct-runs` | F05, lượt 3 cùng SHA | **ĐÃ VÁ THẬT** | A lặp xuyên trang, C lặp trạng thái khác/hai id thật, D mutant đếm bản ghi vẫn bị bắt |

5 lớp lịch sử giữ nguyên slug; **0 lớp / 0 biểu hiện còn mở** sau A–D; không lớp mới, không tái mở. U cuối lượt 4={F04}, F xác minh đóng lượt 5={F04}, **1/1=100%**; không dùng tỷ lệ hay suite tổng thay phép đóng lớp. Không reset budget/lịch sử theo phiên này.

- `not_run/not_measured`: Windows execution/parity; CI, provenance và JSON thật (`tu-do`) của head cuối; connector completion; refs/state/lease/budget máy chủ; merge authorization; runtime receipt executor; delivery receipt/state transition. Prompt cấm mạng/GitHub, không được suy fixture bb8c0c4 hoặc suite local thành các bằng chứng ấy.
- Nhận dạng reviewer có header CLI đúng run và run.json; không chứng minh mọi request/model hoặc runtime của executor. Controller còn phải đối chiếu terminal launcher/child/receipt khi vận chuyển verdict; artifact cục bộ không tự thay state hoặc cấp quyền merge/land/deploy/LIVE.
- Snapshot chỉ phủ checkout reviewer tại hai mốc, kể cả untracked/ignored ngoài `.git/.review`; không chứng minh chưa từng ghi rồi hoàn nguyên ở giữa. Sandbox thực workspace-write. Không quan sát kho executor nguồn.

## Kết quả terminal lớp E và toàn vẹn cuối

Suite session **99742** kết thúc **exit_code=0** do công cụ tiến trình trả trực tiếp. `suite-completion.json` neo command/rc/hash/SHA/tree; không suy rc từ output. Marker thực:

```text
  BỎ QUA  luong_canonical_chay_that: chỉ đo lệnh pwsh trên Windows
nền: 405/405 đạt · BỎ QUA: 1
  BỎ QUA  đột biến luong_canonical_chay_that_dao_os_name: ca ['luong_canonical_chay_that'] không được tính là đã giết
  ca               : 406
  đột biến         : 168
  lớp lách         : 78
  ca bắt-oan       : 35
  ngoại lệ AC 18   : 0
TỔNG: ĐẠT
```

405/405 là số ca chạy trên Linux; catalog có 406 ca, một ca pwsh Windows skipped. Catalog mutant là 168, mutant phụ thuộc ca Windows skipped vẫn giữ skipped, không tính đã chạy/giết. Audit kg độc lập ở D là 41 mutant/113 ô.

- **passed:** suite Linux rc=0 + 405/405 + TỔNG: ĐẠT; A 31/31 CLI và kiểm catalog F03; C 69/69 CLI + help; D 41 mutant/113 ô đúng chốt; write set/diff check; Ruff delta=0; doctrine/ADR parity.
- **failed:** bare Ruff nền rc=1, một F841 ở cả baseline/candidate (delta=0 đúng tiêu chí spec). Không finding sản phẩm P0/P1/P2/P3 còn mở. Lỗi membership trong rig A đầu run đã sửa/kiểm lại, không cấp tín dụng traceback đó.
- **skipped:** một ca pwsh Windows và mutant phụ thuộc, không coi là pass Windows.
- **not_run/not_measured:** CI/head cuối tu-do/Windows/connector/lease/budget/authority/receipt và Ruff pin contract như mục giới hạn; không biến thiếu bằng chứng thành pass.

Snapshot cuối 2026-10-18T01:42:29.759278+00:00: **3680 tệp** ngoài .git/.review, kể cả untracked/ignored, so snapshot đầu: thêm/xoá/nội dung/mode đều không đổi; không path bị loại theo mẫu secrets ở cả hai mốc. HEAD/tree đầu–cuối khớp; git diff/index rc=0, output rỗng. Untracked chỉ .review được giao, ignored .codex giữ nguyên. Spec và bốn verdict đầu vào vẫn khớp hash ghim. Không tuyên bố hai mốc chứng minh toàn lịch sử chưa từng ghi/hoàn nguyên.

Artifact raw nằm tại `/tmp/wp788-review5.DEwL1y7g`; manifest `artifacts.json` băm verdict, suite và các dữ liệu độc lập sau khi ghi kết luận. Controller kiểm lại terminal launcher/child và hash khi vận chuyển; run hiện tại không gọi GitHub hoặc cập nhật state/assurance.

## Kết luận

Áp ngưỡng được giao: hết P0/P1/P2/P3. F01/F02/F03/F04/F05 đều **ĐÃ VÁ THẬT** trong phạm vi đã kiểm; không finding mới, H3 giữ 4. **approve** cho exact candidate dưới đây trong phạm vi review offline. Đây không là ủy quyền merge/land/deploy/LIVE; evidence CI/tu-do/identity receipt/authority còn thuộc các gate riêng, không bị thay bởi verdict hay local suite.

```yaml
packet_id: wp788
revision: 1
generation: 1
role: reviewer
provider: openai_codex
model_family: openai
model: gpt-6.1-sol # header CLI đúng run, không đo từng request
effort: xhigh # header CLI
execution_surface: codex_cli
transport: machine
session_id: 01a14ca3-86eb-7023-906e-1602c6522634
run_id: b8b00f3d9d0a4a96911df056671375d9
model_reviewer_identity: openai_codex/gpt-6.1-sol/01a14ca3-86eb-7023-906e-1602c6522634
github_submitter_identity: null
independent_from_executor_session: true
review_axes: [spec, standards_security]
reviewed_sha: 984032f375aa0c8fe6039dfd35f6842acd49c926
reviewed_tree: ca01ca9b18b840fbb56668aab28adb9885f97005
verdict: approve
counts: {P0: 0, P1: 0, P2: 0, P3: 0}
findings_open: []
findings_closed: [F01, F02, F03, F04, F05]
# Controller còn phải validate/vận chuyển receipt và nhận assurance theo protocol.
```

Bảng **chỉ các ô N1–N7 đã đổi so lượt 4**; N1/N2/N3/N5/N6 giữ kết luận trước:

| Ô | Lượt 4 | Lượt 5 trên exact reviewed_sha |
|---|---|---|
| N4 | F04 P3 tái mở: 11 biến thể ngắt dòng tách cảnh báo | **ĐÃ VÁ THẬT** theo chính sách owner: tên bắt buộc chứa mọi separator đều 2 + xuống dòng; name JSON ngoài tập không tách N4; đối chứng hợp lệ giữ nguyên; F05 vẫn đóng |
| N7 | 394 ca (92 kg), nền 393/393 + 1 skipped; 40 mutant kg/93 ô; chưa khóa newline | 406 ca (104 kg), nền **405/405 + 1 skipped**, **TỔNG: ĐẠT**, rc=0; **41 mutant kg/113 ô** bắt đúng, thêm 20 ô khóa RC_ARG newline, không mất ca cũ |
