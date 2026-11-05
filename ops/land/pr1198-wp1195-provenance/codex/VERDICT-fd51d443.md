VERDICT: approve

Review độc lập packet #1195 `T191-PY314-INTERPOLATION` r1, hai trục Spec và Standards/Security. Không phát hiện lỗi cần sửa trên candidate trong phạm vi snapshot. P0=0, P1=0, P2=0, P3=0; không có finding mở. Hai mutant còn sống được khai riêng bên dưới, không ghi thành ĐỎ.

**Mốc và phạm vi**

- Repository: `ducthangho/tra-luat`; checkout riêng `/tmp/claude-0/rv`, detached HEAD.
- `reviewed_sha`: `ab39416fe919452c9dadda38dd99c5589f7967e8`.
- Tree đầu/cuối: `49a474d980fa22cc579b2f42d239f9433f63f260`.
- Baseline/merge-base với master cục bộ: `1813bfd4513704cf792a272a86b22e5e08893b9a`.
- Spec authoritative do assignment chỉ định: `SPEC_R1.md`, SHA-256 `e6ea2cf7c20279e6f1521b71b6562e811add01256d6c373d677acf9e3acf4ebe`; bản đọc tại checkout khớp. Tệp này có sẵn, untracked, không sửa.
- Diff toàn candidate: duy nhất `ops/lease_publish_test.py`, **19 dòng thêm / 3 dòng xoá**, đạt A3. `ops/lease_publish.py` và workflow không đổi.
- Authority chạy review và tạo hiện vật: `/tmp/claude-0/review/runs/fd51d443/prompt.snapshot`. Chỉ ghi `VERDICT.md` và `review_mutations_fd51d443/`, theo ngoại lệ vị trí scratch mà assignment chỉ định; không ghi tệp nguồn/index/ref/config.
- Provider `openai_codex`; execution surface `codex_cli`; transport `machine`; model family `openai`; run `fd51d4437de74102916d184a494b5034`. Nguồn surface/transport: `run.json` cùng run. Exact model/effort phục vụ lượt chạy và cặp identity Executor–Reviewer: `not_measured`; không tự cấp nhãn `cross_approved` hay quyền land. Không nhận context Executor hoặc dùng subagent.
- Review Class không được khai trong snapshot/spec: áp thước kiểm `sensitive` theo protocol. Generation, lease/ref và review history trên GitHub không nằm trong dữ liệu đã cấp, chưa xác minh live; verdict này là kết quả review cục bộ trên exact candidate, không xác nhận transition/gate/approval của GitHub.

**Kết quả chạy HEAD**

Cwd `/tmp/claude-0/rv`. Chạy nguyên lệnh sau cho từng executable, không bỏ qua ca:

```bash
python3 -B ops/lease_publish_test.py --chi-ca=t191_MOI_chot_cua_kiem_deu_duoc_t190_phu_o_nhanh_DA_DANG
/tmp/claude-0/v314/bin/python -B ops/lease_publish_test.py --chi-ca=t191_MOI_chot_cua_kiem_deu_duoc_t190_phu_o_nhanh_DA_DANG
```

| Python thực đo | rc | Kết quả | Chốt đều PHU | Dòng phân loại / sinh / ô | Ca âm | Thời gian ca |
|---|---:|---|---:|---|---:|---:|
| 3.13.18 (`python3`) | 0 | passed, `lease_publish: 1/1 đạt; đã chạy=1, bỏ qua=0` | 13 | 7034 / 6895 / 2386 | 11 | 78.538 s |
| 3.14.6 (`/tmp/claude-0/v314/bin/python`) | 0 | passed, `lease_publish: 1/1 đạt; đã chạy=1, bỏ qua=0` | 13 | 7100 / 6961 / 2402 | 11 | 81.700 s |

Cả hai cùng thấy đúng một miễn sẵn: `[('raise Chan', 1114, 8)]`. Thời gian là wall time khi có các phép đo đồng thời, không phải benchmark. Có SyntaxWarning escape và RuntimeWarning coroutine của các mẫu cũ; không che rc hoặc đổi kết quả thành pass.

Bằng chứng lệnh/rc/output: [head_results.json](review_mutations_fd51d443/head_results.json). Receipt này giữ output tổng kết và một chunk cảnh báo; không phải toàn bộ transcript stderr đầu–cuối.

**Soát các yêu cầu R1–R5 và chốt chung**

- R1, `ops/lease_publish_test.py:10967`: mẫu t-string đi qua `_phan_tich_duoc_t191`; Python 3.13 có 60 mẫu, Python 3.14 có 61. Đối chiếu các lớp `ast` của hai interpreter: lớp thêm đúng `Interpolation`, `TemplateStr`; `_fields` của các lớp chung không đổi. `_vu_tru_t191()` trên HEAD trả `([], [], [], [])` ở cả hai bản. Việc mất tên nội bộ `_ast_Ellipsis` không phải thiếu lớp AST cụ thể mới cần mẫu.
- R2, `ops/lease_publish_test.py:11303`: `[*?]*` đọc được `expr?*`, còn assert tập tên trường phải bằng `_fields` giữ nguyên. Trên 3.13 không có chữ ký lớp nào đổi kết quả giữa regex cũ/mới; 3.14 khác ở `Dict`, `arguments` và docstring lớp cơ sở `expr`.
- R3, `ops/lease_publish_test.py:11019`, `:11021`, `:11123`: cả `_thay_t191` và `_sinh_goc_t191` gọi helper sau thay con. Quét toàn bộ lớp AST thực tế: 3.13 không lớp nào có trường `str`; 3.14 chỉ `Interpolation`. Helper giữ nguyên AST của 1763 lượt nút không phải Interpolation ở 3.13 và 1775 lượt ở 3.14 trong kho mẫu/toán tử. Không thấy thay đổi hành vi lớp khác. Đọc trực tiếp implementation `_Unparser.visit_Interpolation` của Python đang chạy xác nhận `str=None` khiến nó in từ `value`.
- R4, `ops/lease_publish_test.py:11154`: thêm 10 tiền tố miễn, trải thành đúng **51 khoá**: `TemplateStr.values` 33, `Interpolation.format_spec` 11, gốc `Interpolation` 6, gốc `TemplateStr/or` 1. Các lý do đo được lần lượt là `ValueError`, `ValueError`, `{SyntaxError, dung-lai-khac-lop}`, `{ValueError, witness (False, False)}`; không thấy khoá `Interpolation.value` được miễn. Tập khoá bằng đúng có-dòng hợp miễn, hai tập rời nhau; tập ô không dòng và tập lý do khớp hoàn toàn. Vòng sinh vẫn thử mọi lần xuất hiện, không đổi cơ chế thu lỗi hay assert. Mutant nới tiền tố xuống toàn lớp bị chính chốt giao hai tập bắt.
- R5, `ops/lease_publish_test.py:11394`: block tự kiểm có điều kiện đúng phiên bản, tạo `Interpolation.value` và kiểm chốt trong văn bản dựng lại. Chạy cô lập chính block lấy từ AST của HEAD: HEAD passed; helper `_thay_t191` thiếu xoá `str` bị `TinHieuChotCa` đúng thông điệp `3.14: thay Interpolation.value bị unparse bỏ qua (còn str)`. Văn bản HEAD: `_a = t'{(_kiem_gia_t191(lease), 1)[1]}'`.
- Không hunk nào sửa các chốt liệt kê, đếm thô, so nội dung/nhãn, witness, vũ trụ khoá, miễn chết, giao có-dòng/miễn, lý do lỗi hoặc đối chứng t190. Không thấy nút/trường biểu thức/câu lệnh 3.14 nào khác bị bỏ sót trong vũ trụ mà ca khai đo. `str` và `conversion` là metadata, không phải ô biểu thức cần witness.

Đo A/B base–HEAD trên **3.13** bằng `probe_contract.py`: toàn bộ mẫu, bảng miễn, 6895 dòng sinh (cả nhãn, nguồn, bộ ba), 2386 khoá phủ, 2519 khoá vũ trụ và lý do lỗi đều bằng nhau. Hash nội dung dòng ở cả hai: `1d61e973ad94972cb01aebdf345e73659240e526ec21c7fb00bbee8a2f63ca0a`. Đây là bằng chứng giữ hành vi ma trận 3.13; không suy thành kết quả toàn suite.

Lệnh probe, đều rc=0:

```bash
python3 -B review_mutations_fd51d443/probe_contract.py 313
/tmp/claude-0/v314/bin/python -B review_mutations_fd51d443/probe_contract.py 314
/tmp/claude-0/v314/bin/python -B review_mutations_fd51d443/probe_survivors.py
```

Dữ liệu: [probe_313.json](review_mutations_fd51d443/probe_313.json), [probe_314.json](review_mutations_fd51d443/probe_314.json), [survivor_probe.json](review_mutations_fd51d443/survivor_probe.json). Các probe ghi kết quả vào scratch; `probe_contract.py 313` cần thư mục `baseline_1813` chưa tồn tại khi chạy mới.

**Bảng đột biến trên Python 3.14.6**

Mỗi mutant là một thư mục riêng chứa bản sao hai tệp `lease_publish.py` và `lease_publish_test.py`. Tệp sản phẩm giữ nguyên byte. Lệnh từng dòng:

```bash
/tmp/claude-0/v314/bin/python -B review_mutations_fd51d443/<tên>/lease_publish_test.py --chi-ca=t191_MOI_chot_cua_kiem_deu_duoc_t190_phu_o_nhanh_DA_DANG
```

| Tên thư mục mutant | Thay đổi | rc | ĐỎ/XANH | Bằng chứng dương/âm |
|---|---|---:|---|---|
| `R1_no_template_sample` | Bỏ mẫu t-string | 1 | ĐỎ, `0/1` | `mục miễn không khớp khoá vũ trụ nào (miễn chết)` |
| `R2_old_doc_regex` | Trả `[*?]?` | 1 | ĐỎ, `0/1` | `chữ ký docstring lệch _fields` |
| `R3_no_str_clearing` | Bỏ cả hai lần gọi helper | 1 | ĐỎ, `0/1` | Thiếu khoá CHỐT/CỜ `Interpolation.value` |
| `R3a_no_str_in_thay` | Chỉ bỏ gọi trong `_thay_t191` | 1 | ĐỎ, `0/1` | Thiếu khoá CHỐT/CỜ `Interpolation.value` |
| `R3b_no_str_in_goc` | Chỉ bỏ gọi trong `_sinh_goc_t191` | 0 | XANH, `1/1` | Witness gốc chuyển sang `format_spec`; xem đo cô lập dưới đây |
| `R4_no_template_exemptions` | Bỏ toàn bộ miễn mới | 1 | ĐỎ, `0/1` | Thiếu khoá `Interpolation.format_spec`, `TemplateStr.values` |
| `R5_no_smoke_check` | Bỏ block R5 | 0 | XANH, `1/1` | R5 dư với các chốt ma trận hiện có; R3a bị bắt trước khi tới R5 |
| `EXTRA_broad_interpolation_exemption` | Nới `(l, Interpolation, format_spec, don)` thành `(l, Interpolation)` | 1 | ĐỎ, `0/1` | `Interpolation.value` vừa có dòng vừa miễn |
| `EXTRA_wrong_version_315` | Đổi cả hai điều kiện mới thành `>= (3, 15)` | 1 | ĐỎ, `0/1` | Trên 3.14 thiếu các khoá được miễn mới |

Kết quả **7 ĐỎ / 2 XANH**; không mutant nào được tính là bị bắt do import/setup/permission. A2 gỡ trọn R1, R2, R3, R4 đều ĐỎ. Mỗi thư mục có `change.patch` với mỏ neo/thay thế chính xác, `result.json` chứa command/rc/hash, `stdout.log`, `stderr.log`. Bảng máy: [mutations_results.json](review_mutations_fd51d443/mutations_results.json); script dựng/chạy: [run_mutations.py](review_mutations_fd51d443/run_mutations.py), rc=0 cho runner hoàn tất, rc của mutant giữ riêng như bảng. Script dựng thư mục mới, không chạy lại đè lên hiện vật cũ.

R3b là giới hạn độ nhạy đã đo: HEAD chọn witness `t'{1 // (not bo_qua_han) and 1!r:>{2}}{3}{4}'`; mutant chọn `t'{1!r:>{1 // (not bo_qua_han) and 2}}{3}{4}'`. Cả hai vẫn chứng minh năm ngữ cảnh gốc `TemplateStr`, nên chốt phủ gốc không phân biệt hai đường. Probe thêm với kho cô lập chỉ có `t'{1}{2}{3}'`: HEAD phủ cả năm ngữ cảnh; mutant phủ **0**, witness sai `(True, True)`. Điều này xác nhận call-site trên HEAD đúng và cần cho đường value; không tuyên bố t191 hiện tại có mutant riêng giết được từng call-site. A2 chỉ yêu cầu gỡ trọn R3; không gán thêm yêu cầu đó vào đặc tả.

R5 bị che theo đúng ngoại lệ trong assignment: xoá assertion tự kiểm không thay hành vi bộ sinh; các chốt vũ trụ đã bắt R3a trước R5. Probe thực thi riêng block xác nhận assertion không phải hằng đúng. Không báo mutant R5 là ĐỎ.

**Trạng thái kiểm chứng và tính toàn vẹn**

- `passed`: hai lượt t191 trên HEAD; đối chiếu ma trận base–HEAD 3.13; kiểm vũ trụ/miễn 3.14; probe cô lập R3b/R5; `git diff --check 1813bfd4513704cf792a272a86b22e5e08893b9a ab39416fe919452c9dadda38dd99c5589f7967e8` rc=0.
- `failed` có chủ ý: bảy mutant rc=1 trong bảng. Hai mutant rc=0 được ghi đúng XANH, không tính pass yêu cầu mutant chết.
- `skipped`: 0 ca trong các lượt t191.
- `not_run`: toàn suite `ops/lease_publish_test.py` trên hai interpreter (A1 toàn suite), Ruff contract/bare lint, selftest ứng dụng và các release/land gate; assignment yêu cầu chạy riêng t191. Không dùng `1/1` để chứng nhận toàn suite `284/284` hoặc CI.
- `not_measured`: GitHub lease/generation/current remote HEAD/required CI/provenance, exact model/effort và assurance của cặp thực thi; nội dung ignored/private `.codex/`. Không công bố pass cho các phần này.
- Snapshot byte đầu/cuối của **11.472 tệp tracked** không có delta; HEAD/tree, tracked diff và index diff giữ nguyên; hash spec giữ nguyên; danh sách ignored giữ nguyên. Chỉ thêm hai đường được giao. Bằng chứng [snapshot_before.json](review_mutations_fd51d443/snapshot_before.json) và [snapshot_after.json](review_mutations_fd51d443/snapshot_after.json). Phép đo hai mốc chứng minh trạng thái quan sát được, không chứng minh toàn bộ lịch sử ghi/hoàn nguyên. Sandbox thực tế `workspace-write`, Git/source read-only là kỷ luật vai trò; không tự khai OS đã chặn ghi mọi tệp nguồn.
