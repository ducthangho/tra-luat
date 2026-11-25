VERDICT: changes_requested
reviewed_sha: d1c28891acec4f861a9f26e092d92b71bd08af9d
reviewed_tree: 0e44eaf4a22f66d5c04d243f691f252695e64889
spec_sha256: 280f6f8d0dc97f29a79ed8ef94d3070d8ae1fe0487b549054137bcdbc4acbb0c

**Còn 1 finding P2: F02-R3, cùng lớp `v1-not-fully-specified`.** Lỗi YAML của F02-R2 đã được sửa, nhưng chốt độ sâu JSON mới hạ đỏ đầu vào hợp lệ theo hợp đồng đóng băng. Không xác nhận P0/P1. Các cổng đã commit đều đạt; kết quả đó không phủ định phản chứng dưới đây.

## Hai trục và phạm vi

- **Spec: KHÔNG ĐẠT.** Trần 64 tầng tự thêm điều kiện XANH ở REST/mảnh và làm mất `measured` ở definition dù dữ liệu cần thiết vẫn đọc và kiểm được.
- **Standards/Security: ĐẠT trong phạm vi đã đo.** F01, F03, F04 không tái phát; sáu lớp ngoại lệ YAML được bắt quanh riêng parser. Không xác nhận lỗi an ninh mới. Độ phủ lỗi sập của hai ca P2/P3 có giới hạn, phân tích riêng bên dưới.

Reviewer độc lập, chỉ đọc `src/`; tất cả bản sao đột biến và fixture mới ở ngoài checkout. Metadata [review-runtime.json](review-runtime.json), nguồn `runs/c8a3bf7e/run.json`: provider `openai_codex`, execution_surface `codex_cli`, transport `machine`, run `c8a3bf7ece7f4bbabdabf434ba5d70d5`; sandbox thực tế `workspace-write`. Model/effort thực sự phục vụ từng request: **KHÔNG ĐO ĐƯỢC**, không lấy tên yêu cầu trong prompt làm phép đo. Agent `tl_auditor` chỉ đọc tài liệu và tiêu hoá output theo `src/CLAUDE.md:32`; không thực hiện một lượt cross-review riêng, không quyết finding.

HEAD/tree/cha/ông khớp H3/H2/H1 đã giao; base `5259239d763c9ffc1677f033bd9a9cf23ede9299`. Đã băm SPEC **trước khi đọc**, kiểm lease r9/g3 từ ref được giao. Hai đoạn nội dung từ Mục tiêu đến Kích thước và từ Quy trình đến Thay đổi trùng byte r7/r9, gồm hợp đồng, nghiệm thu và khối kiểm ([spec-r7-r9.json](spec-r7-r9.json)). Không gọi GitHub, commit, push, dispatch hoặc sửa nguồn. Verdict này không cấp quyền land hay lượt executor/reviewer mới.

## Đối chiếu lượt trước

Kiểm kê F02 độc lập được ghi **trước khi đọc HANDOFF.yaml** tại [inventory-before-handoff.md](inventory-before-handoff.md). Nó gồm context; bốn REST; YAML và matrix; lịch/khung; trường job; tên/id/digest artifact và đường dẫn; JSON mảnh/dấu; definition/base64/băm; schema; dựng, validate, mã hoá và ghi hai hình receipt. Sau đó mới đối chiếu P1–P4 và các đường executor khai đã an toàn.

| Finding / lớp lịch sử | Nhãn duy nhất trên H3 | Bằng chứng chạy được và phạm vi |
|---|---|---|
| F01 / `rest-error-sidecar-ignored` | **ĐÃ SỬA ĐÚNG LỚP** | Bốn điểm run/jobs/artifacts/definition vẫn qua reader kiểm dấu lỗi. Chạy lại probe trạng thái JSON/lỗi/cả hai/vắng; dấu lỗi rỗng/thư mục/mode000. Ba lõi đỏ, definition `not_measured` nhưng xanh. Bốn mutant bỏ kiểm ở từng caller và bốn mutant reviewer bỏ riêng từng endpoint đều bị đúng lớp/tên ca giết: [round2-mutants.json](round2-mutants.json), [round2-probes.json](round2-probes.json). |
| F02, F02-R2 / `v1-not-fully-specified` | **VÁ HỜ** | Biểu hiện YAML sâu cũ đã đóng: H3 64/512/900 đều rc1 + receipt đúng schema + X2; H1/H2 512/900 mất receipt. Gỡ riêng chín chốt H3: 9/9 đúng `TinHieuChotCa` và đúng tên. Tuy nhiên P3 hạ đỏ dữ liệu hợp đồng chấp nhận ở **run/jobs/artifacts/mảnh**, và làm mất measured ở definition. Đây là hồi quy cùng lớp, không được lấy việc hết traceback để tuyên bố đóng lớp. |
| F03 / `workflow-context-interpreted-as-shell` | **ĐÃ SỬA ĐÚNG LỚP** | H2..H3 không đổi workflow. 10 context vẫn qua env và quote. Mười mutant nội suy từng context, các mutant env/quote của lượt 2 đều bị giết. Bash thật trên bốn ref dữ liệu giữ đủ 10/10 argv; thân không chứa biểu thức Actions. [round2-probes.json](round2-probes.json). |
| F04 / `collector-derived-evidence-unasserted` | **ĐÃ SỬA ĐÚNG LỚP** | Các assertion băm/định danh của H2 được giữ. Sáu mutant F04 vẫn bị giết; ba mutant từng sống ở H1 nay bị test committed giết. Nhân chứng độc lập so blob, sha256 definition và công cụ tiếp tục phân biệt được cả ba băm sai; bản chuẩn đúng 3/3. [hash-evidence.json](hash-evidence.json), [reviewer-mutants.json](reviewer-mutants.json). |

Đối chiếu với handoff không tìm thêm điểm parser/decoder trực tiếp nào chưa liệt kê. **Phần bị bỏ sót là miền dữ liệu được chấp nhận tại các điểm đã liệt kê**: trường dư của REST và mảnh cũng bị bộ đọc chung áp trần. Danh sách caller đầy đủ không đủ chứng minh sửa đúng lớp khi chính sách reader thay đổi hợp đồng.

Tập lớp còn mở cuối lượt 2 chỉ có F02; lượt này chưa đóng được: **0/1**, không phải 3/4 lớp đã sửa trong toàn lịch sử. Giữ liên hệ B1-04 → F02 → F02-R2 → F02-R3; không đổi slug để xoá lần tái diễn. Phần chuyển sang B1b không được tính là đã vá. Đây là lượt nguồn cuối theo chỉ thị; không hạ severity vì hết lượt.

## Finding mới của lượt này

Đường dẫn/dòng tính từ gốc `src/` tại H3.

| ID | Mức | Lớp nguyên nhân | Tệp:dòng | Mô tả và bằng chứng chạy được | Hướng xử lý |
|---|---|---|---|---|---|
| **F02-R3** | **P2** | `v1-not-fully-specified` | `.claude/dev/ci_dang_ky_test.py:1614`, `:1623`, `:1626`; caller `:1687`, `:1763`, `:1780` | `_doc_json_du` loại **toàn tài liệu** nếu còn phần tử sau 64 lượt duyệt, kể cả phần không tham gia X1–X8/C1–C12. `python3 -B out/depth_contract.py`: 24 cặp H2/H3; trường ghi chú hữu hạn ở run/jobs/artifacts/mảnh tạo **10 đối chứng H2 xanh → H3 đỏ**. H2 có receipt đúng schema, consumer chuẩn cho tập vi phạm rỗng, băm ZIP/nội dung tự đo. Hai ca definition vẫn xanh nhưng `measured → not_measured` dù path/blob/content không đổi. | Bảo toàn miền đầu vào hợp đồng; xử lý recursion tại các phép tiêu dùng dữ liệu thực sự có thể đệ quy, kiểm kiểu trường cần dùng trước khi dựng thông báo, không biến độ sâu trường không dùng thành điều kiện XANH mới. Thêm ca dương cho từng điểm đang bị hạ đỏ, cùng ca âm/đột biến cho từng biên lỗi thực sự. Muốn áp trần dữ liệu toàn cục phải đổi hợp đồng qua revision có thẩm quyền. |

**Cách đo và ý nghĩa.** Fixture giữ hình REST phân trang, các job theo chính workflow H3, dấu hợp lệ, và tám mảnh với đủ trường của producer cũ (`phien_ban`, chế độ, chỉ số/tổng mảnh, head, rc, mốc, kết quả). Chốt `_loi_mot_bien_nhan` cũ chấp nhận tất cả mảnh ở mọi ca. Chỉ thêm trường ghi chú lồng hữu hạn; không có shell payload, đường dẫn thoát cây hoặc phép ép cạn tài nguyên. Bộ kiểm consumer được trích nguyên byte từ SPEC; input consumer, nội dung tệp và băm ZIP được tính độc lập với receipt, sau khi mô phỏng run đã kết thúc.

| Nơi thêm ghi chú | Số lớp ghi chú đã thử | H2 | H3 |
|---|---|---|---|
| run | 0, 60, 64, 70 | Xanh cả bốn; C1–C12 rỗng | 0/60 xanh; 64/70 đỏ X1 |
| một bản ghi jobs | 0, 60, 64, 70 | Xanh cả bốn; C1–C12 rỗng | 0 xanh; 60/64/70 đỏ X1 |
| một bản ghi artifacts | 0, 60, 64, 70 | Xanh cả bốn; C1–C12 rỗng | 0 xanh; 60/64/70 đỏ X1 |
| definition | 0, 60, 64, 70 | Xanh, measured cả bốn | Vẫn xanh; 64/70 thành not_measured |
| một mảnh | 0, 60, 64, 70 | Xanh cả bốn; C1–C12 rỗng; kiểm mảnh cũ không lỗi | 0/60 xanh; 64/70 đỏ X5 |
| một dấu | 0, 60, 64, 70 | Đỏ cả bốn | Đỏ cả bốn, đúng schema cấm trường dư |

Số lớp ghi chú không phải độ sâu toàn tài liệu; jobs/artifacts có thêm lớp bao phân trang. `additionalProperties: false` của schema đóng băng áp lên **receipt và dấu**, không phải lên REST hay nội dung mảnh của C12. Không có điều kiện độ sâu cho trường ghi chú này trong X1/X5/C12. Đây là ca hợp lệ theo hợp đồng offline, **không phải lời khai GitHub đang trả tài liệu sâu như vậy**.

Bằng chứng: [depth_contract.py](depth_contract.py), [depth-contract.json](depth-contract.json), [depth-contract.log](depth-contract.log). Tất cả 48 receipt H2/H3 trong phép đo hợp lệ theo schema; phân biệt lỗi kết luận với lỗi hình. Không cần sửa schema hoặc nới oracle để có phản chứng.

**Rà cùng lớp (§8.3):** reader này dùng chung cho bốn REST và hai họ tệp. Đã đo đủ sáu điểm; phát hiện bốn điểm hạ đỏ, một điểm mất measured, dấu sai hình vẫn đỏ đúng. Rủi ro khi bỏ trần đơn thuần là mở lại recursion ở validator hoặc dựng `repr`; vì vậy không đề nghị chỉ xoá chốt rồi dừng. Cần đo cả dữ liệu hợp lệ và dữ liệu sai hình tại từng consumer. Không đính patch sản phẩm cho đường gate nhạy cảm.

## Đo lại lời khai

Môi trường: Linux, Python **3.13.18**, PyYAML **6.0.3**, jsonschema **4.26.0**. Hai clone A/B được dựng trong một lệnh, cùng `core.abbrev=7`. Mã thoát ở [command-results.json](command-results.json) và [previous-command-results.json](previous-command-results.json).

| Lời khai / phép đo | Kết quả reviewer |
|---|---|
| Numstat base..H3 | **4 tệp +1598/−20**: Python +1316/−20, workflow +87, schema +34, fixture +161. Khớp. |
| H2..H3 | Chỉ Python **+39/−7**; ba tệp còn lại trùng byte. |
| Hai tệp hợp đồng | Đúng băm `844b5218b6f6844945f5c4c9440f09015d238fe09a60d64b3787c440787e4f46` và `ce8595739a1ab2f4a86c9c196255e5f91fb19a9f6d3865df6caa2d66f9970e6d`, trùng byte nguồn SPEC. |
| `python .claude/dev/ci_dang_ky_test.py` trong A/B | Base rc0, **1226/1226**, TỔNG ĐẠT, **8 s**. H3 rc0, **1646/1646**, TỔNG ĐẠT, **239 s**; delta tại máy này +231 s. Khớp lời khai H3 khoảng 240 s. Có phép đo độc lập chạy cùng thời gian. |
| Bảng đột biến wp1460 committed | **98/98 giết đúng lý do; 6/6 tự kiểm; nền 92/92**. Chạy riêng bảng cũng rc0; 104 hàng đúng phân hạng mong đợi. |
| Nghiệm thu 1, trích riêng từ SPEC | rc0, đúng **480/480**, **249/249 = 57 + 192**, `TONG: DAT`. Băm khối Python `d9c78e708e18a211b7d8c7309638ffd1c73200578cf3128f9f0fc4275430f24e`. |
| `bash ab.sh … base H3 …` | rc0, **32/32** trùng stdout/stderr/rc/cây chọn. |
| Fixture wp1166 committed của lượt 1 | rc0; **75/75 ca gốc**, **68/68** A/B CLI trùng byte. |
| actionlint + ShellCheck | Base/H3 rc0/0; **0/0 finding, delta0**. actionlint **1.7.7**, ShellCheck **0.9.0** có mặt. |
| Bare Ruff F | `python3 -m ruff check --select F .claude/dev/ci_dang_ky_test.py`: base/H3 rc0/0, `All checks passed!`, **delta0**; Ruff **0.15.15**. Suite riêng có `RUFF CI: 3/3 hợp đồng`. |
| Probe F02-R2 thích nghi H1/H2/H3 | rc0 của giàn; **9/9** đối chứng. Riêng H3 64/512/900 đều rc1 + receipt hợp lệ + X2. Không gọi rc0 của giàn là collector xanh. |
| Mutant reviewer lượt 1 chạy lại | **40 GIẾT + 1 tự kiểm KeyError bị từ chối tín dụng**, nền 41/41. Ba mutant băm từng sống không còn sống. |
| Mutant lượt 2 chạy lại | **45 GIẾT + 2 tự kiểm sai lớp/tên**, nền 47/47. Trong đó 28 chốt H2 và ba ca bổ sung lịch/schema đều còn răng. |
| Probe dữ liệu lượt 1–2 | Lượt 1: 40 hàng gồm 37 probe dữ liệu và ba phân tích shell cũ. Lượt 2: **78 hàng, 0 bất ngờ**; bổ sung **7** YAML/số lớn và **28** cấu trúc JSON sâu, đều có receipt hợp lệ. |
| Hợp đồng lớp / cấu trúc | **26** phép class-evidence đạt. YAML sau bỏ đúng phần thêm bằng base; bốn hàm legacy giữ nguyên nguồn. |

Log đầy đủ được giữ ở `out/ab-*.out`, `out/rerun-*.log` và các JSON liên kết. Ba hàng `shlex` của probe lượt 1 chưa giải env nên vẫn không giữ literal ref; đây là giới hạn giàn cũ, không phải F03 tái phát. Probe Bash thật của lượt 2 đo đúng đường env hiện hành.

## Đo răng chín chốt mới và đột biến riêng

[round3_mutants.py](round3_mutants.py) kiểm trực tiếp **`type(exc) is module.TinHieuChotCa` và `exc.args == (case,)`**, độc lập với hàm phân hạng sản phẩm. Mọi bản sao tên riêng, tắt bytecode. Mỏ neo/thay thế và tên ca đầy đủ nằm trong [round3-mutants.json](round3-mutants.json).

| Chốt mới, mỗi hàng gỡ riêng | Ca đích (hậu tố sau `wp1460-con-khong-vo-thu-am-`) | Kết quả |
|---|---|---|
| P1 catch RecursionError | `x2-workflow-yaml-bo-phan-tich-vo-RecursionError` | GIẾT đúng lớp/tên |
| P1 catch KeyError | `x2-workflow-yaml-bo-phan-tich-vo-KeyError` | GIẾT đúng lớp/tên |
| P1 catch IndexError | `x2-workflow-yaml-bo-phan-tich-vo-IndexError` | GIẾT đúng lớp/tên |
| P1 catch AttributeError | `x2-workflow-yaml-bo-phan-tich-vo-AttributeError` | GIẾT đúng lớp/tên |
| P1 catch TypeError | `x2-workflow-yaml-bo-phan-tich-vo-TypeError` | GIẾT đúng lớp/tên |
| P1 catch OverflowError | `x2-workflow-yaml-bo-phan-tich-vo-OverflowError` | GIẾT đúng lớp/tên |
| P2 kiểm UTF-8 tên job | `x2-ten-job-khong-ma-hoa-duoc-utf8` | GIẾT đúng lớp/tên; xem giới hạn dưới |
| P3 kiểm độ sâu | `x1-rest-jobs-json-long-qua-tran` | GIẾT đúng lớp/tên; xem giới hạn dưới |
| P4 bắt ValueError đường dẫn | `x4-ten-job-chua-nul-khong-thanh-duong-dan` | GIẾT đúng lớp/tên |

Bảng riêng reviewer chọn thêm trong lượt này, **không cộng chín hàng trên vào số mutant mới độc lập**:

| Mutant | Kết quả ca đích committed | Ý nghĩa |
|---|---|---|
| Chỉ áp trần JSON khi đọc tệp REST, bỏ cho bytes dấu/mảnh | **SỐNG** | Ca P3 chỉ đo jobs không bảo vệ caller dấu/mảnh. |
| Chỉ kiểm UTF-8 khoá job, bỏ phần giá trị matrix trong tên mở rộng | **SỐNG** | Ca P2 hiện tại chỉ có tên khoá job bất thường. |
| Đổi trần 64 thành 65 | **SỐNG** | Ca sâu 100 không ghim biên 64; không tự coi sai biệt này là lỗi sản phẩm riêng. |
| Hạ trần xuống 4 | GIẾT đúng lớp/tên | Ca lượt đầu xanh phát hiện reader loại dữ liệu thông thường. |
| Parser vẫn hạ đỏ nhưng dùng câu lỗi tổng quát | GIẾT đúng lớp/tên | Assertion ràng câu lý do, dù kết luận không đổi. |
| Băm tên artifact thay nội dung | GIẾT đúng lớp/tên | Bằng chứng băm có kiểm nguồn. |
| Definition fallback đánh mất workflow SHA đã biết | GIẾT đúng lớp/tên | Ca fallback bảo vệ định danh context. |
| Bỏ qua lỗi mã hoá UTF-8 | GIẾT đúng lớp/tên | Ca P2 phân biệt có/không có chốt. |
| Tự kiểm ném KeyError vô can | **GIẾT SAI LÝ DO** | Không cấp tín dụng giết. |
| Tự kiểm ném TinHieuChotCa mang tên khác | **GIẾT SAI LÝ DO** | Không cấp tín dụng giết. |

Tổng lượt 3: chín chốt mới **9/9 GIẾT**; mười mutant tự chọn **5 GIẾT, 3 SỐNG, 2 GIẾT SAI LÝ DO có chủ đích để tự kiểm**. Nền **19/19** đạt. SỐNG ở bảng này nghĩa là sống qua **ca đích được nêu trong JSON**, không khai đã sống qua toàn suite. Không tự biến mỗi lỗ độ phủ giả định thành finding sản phẩm khi chưa có phản chứng hành vi.

## Hồi quy H2..H3 và bảy lựa chọn đã chấp nhận

| Lựa chọn / phạm vi | Kết luận trên H3 |
|---|---|
| 1. Ref bắt buộc; 2. cron phải có tham số, dispatch nhận rỗng | Giữ nguyên; ca committed và probe lượt 1 vẫn đúng rc2/no receipt khi thiếu, dispatch rỗng xanh. |
| 3. X5 kiểm chỉ số mảnh | Giữ nguyên; mutant bỏ so chỉ số vẫn bị giết. **Tuy nhiên reader mới thêm hạn chế ngoài X5/C12**, chính là F02-R3. |
| 4. Definition measured khi path/blob đúng | Các phép path/blob cũ giữ nguyên; REST byte khác checkout vẫn measured. **Hồi quy mới:** dữ liệu phụ sâu làm mất measured trước khi tới kiểm path/blob. |
| 5. Xanh sai schema phải hạ đỏ | Giữ nguyên kết luận trên dữ liệu trường sai kiểu/sai dạng. Hai hình vẫn được kiểm. Trần mới loại thêm tài liệu không hề làm schema của receipt sai. |
| 6. CLI cũ bỏ qua các cờ mới theo phạm vi nghiệm thu hẹp | Không đổi. Không cờ mới: base/H3 rc0/0; kèm ba cờ mới đã biết: rc2/0. Không tuyên bố tương đương mọi argv. |
| 7. Chạy đầy đủ oracle ở tiến trình con | Giữ đầy đủ 480/249, không cắt phép kiểm. Thời gian tại chỗ không phải thời gian runner. |
| F01/F03/F04 và I1 | Không thấy hồi quy trong miền đo; workflow H2/H3 cùng byte, các chốt và phản chứng cũ tiếp tục đạt. |

Không thấy catch P1 che lỗi traversal do mã của collector: phép tiêm lỗi kiểm soát trong `jobs.items()` **ngoài parser** vẫn thoát bằng TypeError, không bị đổi thành X2 ([parser-boundary.json](parser-boundary.json)). Không suy điều này thành chứng minh mọi lỗi nội bộ của PyYAML đều được phân biệt với dữ liệu.

## BẢNG SĂN

| Hướng / giả thuyết | Phép đo | Kết quả |
|---|---|---|
| 1. Parser YAML còn thoát biên X2 | Probe lượt 2 thích nghi H3, 64/512/900; sáu ca committed và gỡ từng catch | Biểu hiện cũ đã đóng; 9/9 đối chứng YAML, sáu catch có răng. |
| 2. Trần JSON hạ đỏ trường không tham gia hợp đồng | 24 cặp H2/H3, ZIP/băm độc lập, oracle đóng băng | **F02-R3: 10 ca xanh→đỏ; 2 ca definition mất measured.** |
| 3. Dấu và mảnh bị coi nhầm cùng hình | Thêm ghi chú tương tự vào từng họ, kiểm schema và C12; kiểm mảnh legacy | Dấu phải đỏ vì trường dư; mảnh được phép và bị H3 từ chối sai. |
| 4. Ca P2/P3 chỉ khoá câu lỗi | Quan sát rc/receipt/schema khi chạy đúng ca committed, trước/sau gỡ từng chốt | Cả bốn lần đều rc1 + receipt hợp lệ; mutant chỉ đổi lý do. |
| 5. Catch YAML che lỗi mã ngoài parser | Tiêm TypeError ở traversal sau parser | Ngoại lệ vẫn thoát; không có catch toàn hàm. |
| 6. REST lỗi bị JSON tốt che | Bốn endpoint × trạng thái, sidecar rỗng/thư mục/mode000; mutant từng caller | F01 giữ đúng; mode000 dưới root không chứng minh PermissionError thật. |
| 7. Mốc hoặc số lớn gây traceback | Probe lịch biên, số 19/20/64/65/4301/5000 chữ số; 28 trường JSON sâu | Đầu vào sai cho receipt hợp lệ; không phát hiện thêm đường sập ở phạm vi này. |
| 8. Context env mất byte / bị hiểu thành shell | Bash thật bốn ref thường, dấu nháy, dollar, Unicode; 10 context | Giữ nguyên argv, F03 không tái phát. |
| 9. Hash bị đổi nguồn nhưng test vẫn xanh | Mutant H1 chạy lại, nhân chứng độc lập, mutant mới băm tên | Các băm sai bị phát hiện; F04 giữ đúng. |
| 10. Hồi quy selector/job cũ bị helper che | A/B 32 + 68, 75 ca gốc, AST hàm và YAML trừ phần thêm | Trùng byte và giữ I1 trong miền đã chốt. |

## Đầu vào thù địch — mô tả đường xử lý và ca phủ

Không soạn payload tấn công mới, không tạo fixture nhằm thoát cây. Các ca mới chỉ dùng dữ liệu ghi chú hữu hạn, đối chứng mã và quan sát ca đã có. Không chạy fuzz executor rồi nhận kết quả khai sẵn làm bằng chứng.

| Nhóm | Đường xử lý và độ phủ đã đo |
|---|---|
| YAML lồng sâu | `job_ky_vong_du` → `safe_load` → chuyển ngoại lệ parser thành ValueError → biên X2. Probe H3 64/512/900 và ca con RecursionError đã chạy; gỡ catch bị đúng ca giết. |
| YAML thẻ kiểu lạ | Sáu lớp trong bảng P1 được ca committed kích hoạt trên PyYAML 6.0.3; catch riêng từng lớp có đột biến. Không tạo thêm chuỗi thẻ mới. |
| YAML bí danh | `safe_load` trả đồ thị, còn kiểm kê chỉ đi jobs/strategy/matrix và kiểm kiểu phần tử, không tự mở rộng đệ quy. Các thử bí danh/cycle của executor **không được reviewer đo lại**; không nhận lời khai đó là kết quả độc lập. |
| JSON sâu tại run/jobs/artifacts/definition | `_doc_json_du` bắt lỗi decode/parse rồi áp trần chung; ba lõi đi X1, definition đi not_measured. Probe lượt 2 chạy lại đủ bốn điểm; phép dữ liệu hợp lệ mới phát hiện F02-R3. |
| JSON sâu trong dấu/mảnh | Chung reader bytes; dấu tiếp tục qua validator X4, mảnh qua object/head/manh X5. Probe sâu lượt 2 vẫn receipt hợp lệ; dữ liệu ghi chú mới phân biệt schema dấu với hợp đồng mảnh. Chưa tái tạo cửa sổ sập gần giới hạn parser mà executor khai. |
| Tên job không mã hoá được UTF-8 | Tên mở rộng đi qua encode ở `job_ky_vong_du` rồi X2; ca committed và mutant P2 đã chạy. Chưa dựng lại thư mục tên byte đặc biệt của probe executor. |
| Tên job/artifact có NUL hoặc không biểu diễn được thành đường dẫn | Tên REST ngoài kiểm kê/họ bị X2/X7; tên khớp đi tới `lay`, lỗi đường dẫn thuộc OSError/ValueError thành X4. Ca committed NUL có đột biến riêng; không tạo đường thoát cây. |
| Số rất lớn | Parse JSON/YAML, giới hạn chuỗi matrix và regex attempt bảo vệ các phép chuyển số trong collector. Các ca cũ/số biên đã chạy; không đo cạn bộ nhớ hoặc mọi cấu hình giới hạn chữ số Python. |

## Phán câu hỏi 1–4 của executor

**1. Sáu lớp ngoại lệ P1:** chấp nhận cách đặt biên hiện tại trong môi trường được ghim. `try` chỉ bọc lời gọi parser; mỗi lớp có ca thực và mutant riêng. Chỉ bắt RecursionError thì bỏ sót năm đường đã có ca; bắt Exception quanh collector sẽ che thêm lỗi lập trình và làm bằng chứng kém hơn. Bắt các lớp hiện tại quanh parser vẫn có thể che lỗi nội bộ cùng lớp của thư viện, nhưng kết quả là đỏ có receipt, không biến lỗi thành xanh. Workflow ghim PyYAML 6.0.3, đúng bản đã đo; không cần dự đoán mọi ngoại lệ của đời sau để chấp nhận bản ghim này. Nâng thư viện phải đo lại biên, không gọi danh sách sáu lớp là bảo đảm phổ quát.

**2. Trần JSON ≤64:** **không chấp nhận**, vì đã có phản chứng hợp đồng cụ thể, không chỉ tranh luận về văn xuôi. Trường dư ở REST/mảnh được oracle cho qua; dấu thì không. Nâng 64 lên một số khác chỉ dời biên sai. Phương án bắt RecursionError tại các consumer có thể giữ miền hợp đồng tốt hơn, nhưng phải bao gồm cả dựng thông báo/`repr` và validator hai hình/dấu, không chỉ thêm một catch rồi suy toàn phần. Cần giữ kiểm kiểu/định danh và ca dương ở những phần không được consumer sử dụng.

**3. P2/P4 mở rộng theo lớp:** đúng phạm vi sửa F02, không phải việc ngoài packet. Trên tên UTF-8 thông thường và các fixture hợp lệ đã chạy, không đổi kết luận. Surrogate không thể xuất nguyên văn thành UTF-8 như lệnh ghi hiện hành; NUL không thể là thành phần tên tệp thực. Từ chối chúng là xử lý dữ liệu không thể tạo đủ bằng chứng, không có phản chứng xanh hợp lệ bị hạ đỏ do riêng P2/P4 trong miền đã đo. Không lấy nhận định đó làm bằng chứng đã chạy probe thư mục đặc biệt của executor.

**4. P2/P3 là ca có ĐO hay có MẶT:** chúng **có thực thi và có đo nhánh/lý do**, không phải test `return` sớm bỏ qua công việc. Tuy nhiên chúng **chưa đo trực tiếp tính chất chống sập đã được viện dẫn**. [test-signal-evidence.json](test-signal-evidence.json) quan sát đúng ca: sau khi gỡ P2, vẫn rc1/receipt hợp lệ do thiếu artifact; sau khi gỡ P3, vẫn rc1/receipt hợp lệ do started_at sai hình. Tín hiệu TinHieuChotCa đúng lớp/tên là thật, nhưng nguyên nhân assertion là câu lý do đổi, trong khi hợp đồng nói `ly_do` không mang nghĩa máy. P2 có giá trị như ca đơn vị của biên mã hoá; không đủ một mình chứng minh mọi đường ghi không sập. P3 còn đang khoá một luật đầu vào sai hợp đồng; tỷ lệ giết đó không thể chứng minh vá đúng. Cần ca quan sát hành vi cần bảo vệ ở từng biên, kèm đối chứng dương, không bắt buộc mọi nền phải dùng đúng một con số độ sâu sát ngưỡng máy khác.

## Write set, P3 và phần chưa đo

[identity-checks.json](identity-checks.json): đúng bốn đường của lease; **1598 ≤1700**, còn 102 dòng theo trần; hai hiện vật hợp đồng đúng byte. Quét cả bốn tệp và toàn thông điệp ba commit H1/H2/H3: **0 dấu bỏ-qua-CI** trong các dạng chuẩn đã kiểm. `git diff --check base H3` rc0.

**Danh sách P3 còn mở:** không có P3 mới được xác nhận trong phạm vi review này. Không đổi F02-R3 thành P3 hoặc tự miễn finding. Các giới hạn đo dưới đây không được trình bày thành đã đạt.

**KHÔNG ĐO ĐƯỢC / not_run:**

- GitHub/REST/context/runner thật, PR Ubuntu CI, K7, canary A3, push/rerun/schedule thật và các nghiệm thu sau push/merge. Không tiêu quota M9, không cấp miễn Windows exact-H.
- Windows, macOS, Python 3.12 của workflow, PyYAML khác 6.0.3; không suy test Linux 3.13 thành phép đo những nền này.
- Cửa sổ JSON sâu khoảng 9993–9997 và thư mục tên byte đặc biệt mà executor khai; fuzz a5/b5/c5 và probe surrogate của executor không được tính là bằng chứng reviewer. Bí danh YAML chưa đo lại độc lập. Việc chưa đo này không làm yếu phản chứng dữ liệu thường đã chạy.
- OOM/MemoryError, hết đĩa, đầu ra không ghi được, mất byte chương trình; lỗi permission thật dưới người dùng không có quyền. Không dựng payload thực thi hoặc thoát thư mục.
- Không chạy registry `--chay`, selftest toàn runtime, hoặc lặp các cổng lân cận không bị diff H2..H3 tác động; không lấy log các lượt trước làm kết quả H3. Không đo chi phí runner hai nhân.
- Ref/lease/budget từ snapshot được giao, không xác minh remote live. Model/effort từng request và receipt kết thúc launcher đang bao phiên chưa đo được.

Hướng tái chạy: [REPRODUCE.md](REPRODUCE.md).


## Kiểm cuối và bàn giao

Đã đối chiếu **17.994/17.994 tệp worktree**, gồm hidden/ignored, ở hai mốc: **0 thêm, 0 xoá, 0 đổi byte**. Git status, working diff, index diff rỗng; HEAD/tree/cha cuối giữ nguyên. [read-only-check.json](read-only-check.json) ghi kết quả và giới hạn: snapshot nội dung đầu được lấy sau khi khởi động giàn chỉ chạy trên bản sao; đây là so hai mốc, không phải giám sát mọi syscall. Git sạch đã được kiểm ngay preflight.

Đã dọn `review-scratch/` do reviewer tạo; giữ `out/` với verdict, script, log, JSON, hướng dẫn và `SHA256SUMS`. Không sửa/dọn `src/`, `luot-1/`, `luot-2/` hay `executor-probes/`. Kết luận cuối: **changes_requested, F02-R3 P2 còn mở**.
