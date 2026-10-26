verdict: changes_requested
reviewed_sha: 22da28c738e651361274c1264e681a52461dad1e
base_sha: ba222ffd1615f0d74b59985b9612f725211b62f5
Reviewed commit: 22da28c738e651361274c1264e681a52461dad1e
reviewed_tree: 22da0a84e0a0f908664ceec22fe917f3166c29be
packet: wp899-r4
review_round: 5
role: reviewer
provider: openai_codex
model_family: openai
model: gpt-6.1-sol (CLI-published)
effort: xhigh (CLI-published)
session_id: 01a171df-f8f0-7b11-84d1-0ab8f928ddf4
execution_surface: codex_cli
transport: machine
github_submitter_identity: null
independent_from_executor_session: true
review_axes: [spec, standards_security]
assurance: review_deferred

**Chưa đạt V2: P0=0, P1=1, P2=0, P3=1 theo lớp (D01 mới; các ghi chú P3 của F10 không tách lớp). F10 `fixture-dinh-danh-buoc-chi-giu-dang-khop` LẶP, chưa đóng cả lớp.** Các biểu hiện lượt 4 đã vá thật: 20/20 mutant của `new_frontier.py` bị giết đúng ca; chỉ cập nhật scaffolding số ca baseline47→48, danh sách M20 không đổi (`new-frontier-replay5.json`). Tuy nhiên, 25 mutant mới và `n_goi_strip_run` vẫn sống 48/48 ca trên đầu vào có kết quả do M4/M12 định nghĩa; mỗi mutant có phản chứng riêng HEAD rc0 → mutant rc3 bởi `TinHieuChotCa` đúng tên. 2 mutant sống khác là tương đương hoặc thuộc phần chưa được đặc tả, ghi P3 và quyết định đề xuất bên dưới. Không suy lỗi của mutant thành lỗi sản phẩm hiện hành.

**Một lời khai tương đương đã bị bác bỏ.** `n_goi_strip_run` thay `run.rstrip("\n")` bằng `run.strip()` trước `dong_logic` KHÔNG tương đương. Dòng gọi script kết thúc bằng dấu `\` rồi khoảng trắng giữ nguyên khối in lại và ghép `passed`. HEAD không sinh marker; trim làm dấu `\` thành ký tự cuối dòng, `dong_logic` loại nó như nối dòng và mutant sinh marker/Gate `passed`. `norm-full5.json`: 48/48 ca xanh trên mutant. `norm-head.json` rc0 và `norm-mutant.json` rc3, dòng `DO:n_goi_strip_run:`; `norm_counterexample5.py` là phép đo chạy được. 11 ví dụ đồng kết quả trong `norm-equivalence5.json` chỉ là đối chứng hữu hạn, không chứng minh tương đương; kết luận sơ bộ trong artifact ấy đã được ghi rõ là bị phản chứng bác bỏ.

**Authority, preflight và giới hạn.** User giao trực tiếp `.review-input/prompt.md`; đã đọc trọn spec r4 (23.860 byte, SHA-256 `be1e1feabe7c23b832168e36b0cce333043863af505e65c48d5a22d2101cef45`) và các mục r2/r3 được kế thừa. Hash r2/r3 khớp `preflight5.json`. Áp skill [cross-review](../.agents/skills/cross-review/SKILL.md), protocol §7/§8/§8.1–§8.3/§10.2 và luật Packet. Không gọi subagent, mạng/GitHub, push, merge, land hay LIVE.

Origin `https://github.com/ducthangho/tra-luat.git`; detached HEAD/tree đúng đầu verdict. Parent `75d0f6b5fe01611dda0b8768e50f5826657135e7`; baseline nghiệm thu bất biến là `ba222ffd1615f0d74b59985b9612f725211b62f5` (ancestor rc0), không dời sang parent. `full.patch` và `delta.patch` giữ raw diff. Numstat: registry +1, sản phẩm +444, test +1060 = **1505 dòng thêm**, đúng ba tệp write set. Delta lượt 5 chỉ thêm 114 dòng test; diff sản phẩm so parent rỗng. `git diff --check <base> HEAD` rc0; `core.abbrev=7` có sẵn, không đổi config. Registry chỉ thêm một mục MOI.

Giữ Q1–Q12 và giới hạn gốc tin: workflow/script/action tại SHA checkout, gồm action pin tag, có quyền quyết định output. Các phép đo mới chỉ dùng dữ liệu hợp đồng vô hại; không tự soạn nội dung tấn công nhạy cảm. Theo quyết định chủ kho trong assignment sau checkpoint issuecomment-6393643859, không áp lại V5/trần 1250 cũ làm finding. Đây là lời gọi 5/8 theo assignment, còn 3 lời gọi gồm connector. Generation/lease/state GitHub, remote fence, chi thực tế và việc đẩy nhánh lưu trữ **KHÔNG ĐO ĐƯỢC offline**. Không tự dùng verdict này để chuyển state hay cấp authority land.

Linux x86_64, Python 3.13.17, PyYAML 6.0.3, Git 2.43.0, Ruff 0.15.15, codex-cli 0.164.0. `runtime5.json` trích metadata đúng thread từ `/root/.codex/sessions/2026/10/25/rollout-2026-10-25T07-04-27-01a171df-f8f0-7b11-84d1-0ab8f928ddf4.jsonl`: model/effort là CLI công bố; model phục vụ từng request **KHÔNG ĐO ĐƯỢC**. Executor Claude/cloud theo assignment, không suy model từ submitter. Rollout/launcher receipt sau khi writer kết thúc chưa thể chứng nhận trong chính lượt đang chạy; A13 chưa hoàn tất. Sandbox workspace-write, `.git` read-only, network false, approval never; candidate được giữ read-only bằng hành vi và snapshot, không khai sandbox là read-only toàn bộ.

**BẢNG LỚP — F10 P1 còn mở; D01 P3 mới; 0 lớp P0–P2 mới.** Chốt sản phẩm hiện đúng trong các đối chứng; HINT ở đây là bổ sung test/đột biến. Giữ slug cũ, không reset lịch sử bằng biểu hiện mới.

| lớp | hạng | biểu hiện (tệp:dòng) | phép đo tái hiện | HINT patch | ước lượng dòng |
|---|---|---|---|---|---|
| F10 — LẶP: chuẩn hoá thay ngữ nghĩa nối dòng | P1 | `ops/ci_provenance_test.py:389`, `:685`; `n_goi_strip_run` còn ngoài DOT_BIEN do khai tương đương sai. Chốt `ops/ci_provenance.py:297`. | `norm_counterexample5.py`: HEAD0 → mutant3 đúng ca; mutant sống 48/48. | **Ở đâu:** c23/c27 hoặc c48 + DOT_BIEN, vì cần khóa lời gọi tối giản sau khi khối đã xác thực. **Cách:** giữ nguyên dấu cách sau dấu nối dòng cuối, đòi ghép passed và không marker; thêm đối chứng nối dòng thật. **Khoá:** n_goi_strip_run phải chết đúng ca. **Rủi ro:** strip fixture hoặc khối lệch YAML sẽ che chốt; không cần sửa sản phẩm đang đúng. | ~5–9 |
| F10 — LẶP: miền và lượng từ env | P1 | `ops/ci_provenance_test.py:639`, `:685`: bảng chủ yếu đổi env job, một khoá với giá trị 1; không khóa đủ env workflow, mọi khoá và giá trị rỗng. Chốt `ops/ci_provenance.py:153`, `:214`. | Nhóm env trong `frontier5/results.json`; từng survivor có HEAD0 → mutant3 trong `counterexamples5.json`. | **Ở đâu:** c46/c48 + DOT_BIEN. **Cách:** cùng ma trận absent/map/expression ở cả workflow và job; map chứa khoá chặn ở vị trí đầu/giữa/cuối, giá trị rỗng vẫn chặn theo tên khoá. **Khoá:** wf_env_dict_only/nonempty_only, job_env_only_first_key và env_prefix_value_only, cùng các survivor miền trong bảng dưới. **Rủi ro:** map rỗng/absent bị lẫn, hoặc khoá khác che nhánh đang đo; mỗi hàng chỉ đổi một trục. | ~12–20 |
| F10 — LẶP: định vị job/bước ở chặn chế độ và đọc run | P1 | `ops/ci_provenance_test.py:511`, `:568`, `:639`: job đích thường đứng đầu; các phép chế độ thường đặt ở bước đích cuối. Chốt `ops/ci_provenance.py:213`, `:293`. | mode_first_job, dd_first_job, mode_last_step, mode_first_run_step sống; phản chứng hai job/two run có ghép passed và marker đúng vị trí. | **Ở đâu:** c33/c46 hoặc một ma trận đa job/đa bước. **Cách:** hoán vị job đích, đặt chặn lần lượt trước/đích/sau; kiểm toàn bộ danh sách marker. **Khoá:** bốn mutant trên phải GIET; có đối chứng job/bước không bị chặn. **Rủi ro:** helper fallback job đầu, run trùng hoặc chỉ đòi Gate chung sẽ tiếp tục che vị trí; dùng dữ liệu phân biệt và state REST độc lập. | ~14–24 |
| F10 — LẶP: biên ghép và khối còn thiếu | P1 | `ops/ci_provenance_test.py:537`, `:555`, `:568`, `:653`, `:685`: còn biên number/ghép rỗng/duy nhất/thời gian/văn bản chưa khóa; xem từng survivor bên dưới. | Các ca cùng tên trong `cases5.py`, baseline0 → mutant3; toàn 48 ca hiện có xanh trên từng survivor. | **Ở đâu:** c36–c39/c47–c48 + DOT_BIEN. **Cách:** thêm bảng quan hệ: number nguyên dạng float, thứ tự số qua 9→10; mọi vị trí cửa sổ giờ; tên key đồng thời là alias job khác; 0 nhóm với các bước skipped; nhiều newline cuối run và các biến thể khối còn sống. **Khoá:** mỗi survivor định nghĩa được phải chết đúng ca, giữ positive control đi tới marker. **Rủi ro:** ghép hỏng ở một vế khác che chốt; không áp chuẩn mới ngoài spec chỉ để giết mutant. | ~20–35 |

| D01 `mien-env-null-chua-chot` — MỚI | P3 | `ops/ci_provenance.py:153`, `:214`; null bị gộp với env vắng | mode_probe.py: hai scope null ra passed; actionlint1.7.7 rc1 ở null, rc0 ở map có giá trị; LIVE chưa đo | Owner ducthangho chốt miền/ngoại lệ null; nếu áp nghĩa chặt, phân biệt key vắng/null và khóa bằng ca cả hai scope. Rủi ro nullable cũ/đầu vào runner không sinh; chi tiết dưới. | ~6–10, chưa áp |

D01 `mien-env-null-chua-chot` — **P3, owner đề xuất ducthangho**: phép đo `mode_probe.py` cho thấy `env: null` ở job hoặc workflow vẫn sinh marker/Gate passed, vì `_env_chan(None)` coi nó như trường vắng. Spec nói env không phải dict phải chặn nhưng không tách riêng YAML null với trường vắng. Actionlint 1.7.7 từ chối cả hai workflow null bằng syntax-check (rc1); đối chứng map có A=1 rc0. Actionlint cũng từ chối map rỗng mà spec M4 cho phép, nên **không dùng actionlint thay đặc tả hay tự hạ các mutant env đã được spec định nghĩa**. Runner LIVE với null KHÔNG ĐO ĐƯỢC. Chưa đủ căn cứ nhận null là một đường tạo bằng chứng sai trên workflow được runner chấp nhận; cũng không tuyên bố nhánh null đã đạt M4. **Quyết định đề xuất:** chốt rõ ngoại lệ null; ưu tiên phân biệt trường vắng với null và cho null fail-closed nếu miền bao gồm YAML lỗi. **HINT (chưa áp):** ở `_env_chan`/`chan_buoc` và c46, giữ phép đo cả hai scope, đối chứng absent/map/expression; mutant gộp null với absent phải chết nếu owner chọn cách hiểu chặt. Rủi ro là đổi quy ước nullable cũ hoặc kiểm cả workflow không thể tạo REST job; không tự suy runtime từ lint. Ước 6–10 dòng test/hint, còn clarification ngoài write set cần owner chốt, không sửa trong review này. Evidence: `mode-probes.json`, `env-null-actionlint.json`, `env-map-actionlint.json`, `env-valid-actionlint.json`.

Tổng HINT cho F10 khoảng **51–88 dòng**, chỉ là ước lượng, chưa áp vào cây thật. Executor có thể tham số hoá gọn hơn, phải tự tái dẫn xuất và đo. Một thay đổi chung cho fixture đa trục và kiểm kết quả downstream rẻ hơn vá từng mutant; property-based generator là phương án đắt hơn để mở rộng miền, chưa bắt buộc thêm dependency.

**ĐỐI CHIẾU F01–F11.** Nguồn gần nhất r4 lượt4 tại parent; lịch sử r4 lượt1–3 và r3 được giữ trong input. “Giữ đóng” chỉ thuộc tập đo đã nêu.

| lớp | kết quả | bằng chứng độc lập và giới hạn |
|---|---|---|
| F01 `thieu-dinh-danh-van-passed` | GIỮ ĐÓNG | c22, mutant định danh đúng ca và probes kiểu/thiếu trường cũ. Không dùng trạng thái kich_ban thay ghép/marker. |
| F02 `nhac-ten-script-thanh-thuc-thi` | GIỮ ĐÓNG các phản chứng sản phẩm được giao | Chạy lại probes, r2 compare, r3 reviewer cases, composite/boundary trên REST r4 hợp lệ; xem legacy-final-results.json. C25–c27/c35/c40/c41/c43 và mutant đích có răng. Không vượt giới hạn gốc tin bằng sửa workflow tại SHA. |
| F03 `phan-trang-dem-thay-vi-chung-minh-du` | GIỮ ĐÓNG | c20, thiếu/lặp/total đổi, jobs/artifacts; từng mutant đích GIET. |
| F04 `rest-gia-khong-neo-run` | GIỮ ĐÓNG | Probes run/attempt/log sai trả404, hai mutant jobs/artifacts run+1 GIET c20. |
| F05 `duong-loi-bo-dong-dem-bat-buoc` | GIỮ ĐÓNG phạm vi đo | c01/c19/c22, HTTP403, shape, lỗi ghi/lưới cuối; summary/rc thật được giữ. Không nói mọi lỗi đã thử. |
| F06 `redirect-loi-thoat-ngoai-bo-boc` | GIỮ ĐÓNG | c24 và mock redirect/network/token cùng mutant; không đo mạng thật. |
| F07 `a10-doi-sha-khi-checkout-skipped` | GIỮ ĐÓNG bằng authority | Replay 13+1 và22+1, không gán SHA cho chuan-bi từ REST. |
| F08 `nguon-workflow-git-khong-duoc-kiem-thu` | GIỮ ĐÓNG | c34 Git/tree thật, thiếu path/nonUTF8, hai mutant reader đúng ca; git_workflow_source cũ. Object lịch sử thiếu trong shallow clone không tự coi là đúng. |
| F09 `thoi-diem-khong-hop-le-van-ghep` | GIỮ ĐÓNG | c38/calendar/finish probes, lịch thật/fullmatch/offset/giờ thiếu và các mutant được tái neo đúng vị trí mới. |
| F10 `fixture-dinh-danh-buoc-chi-giu-dang-khop` | **ĐÃ VÁ THẬT các biểu hiện lượt4 / CHƯA ĐÓNG CẢ LỚP** | 20/20 mutant lượt4 GIET; c48 đo thật 119 hàng (c48-rows5.json). 26 mutant định nghĩa được còn sống, gồm lời khai tương đương sai. Giữ cùng slug/lịch sử. |
| F11 `chan-path-chua-co-phan-chung` | GIỮ ĐÓNG | c42 ENV/PATH trước/khác job/sau, bỏ riêng PATH GIET đúng ca. Miền/vị trí thiếu còn lại thuộc F10. |

U={F10}, F={}: **0/1 lớp đóng toàn bộ**, 0 lớp P0–P2 mới. Một bảng biến dạng 119 hàng không tự chứng minh mọi dạng/miền/vị trí đã được kiểm.

**A1–A27 — phân biệt kết quả đã đo với gate chưa chạy.**

| tiêu chí | trạng thái/phạm vi |
|---|---|
| A1 | passed: c01 help đủ cờ, sai đối số giữ rc2 và summary; mutant c01 GIET. |
| A2 | passed: c02 lệch attempt rc12, mutant đúng ca. |
| A3 | passed trong fixture: c03–c09 và mutant Linux/Windows/SHA/PR; không nhận đây là native Windows execution. |
| A4 | passed các vế đã quy định: c10–c15 cùng mutant runner/skipped/regex từng bước/MOI import. |
| A5 | passed: c16 luôn not_measured, path chỉ là lời khai. |
| A6 | passed: c17 lỗi ghi nguyên tử, mutant đúng ca. |
| A7 | passed: c18/c19 và receipt mutant đích trong mutants/results.json; rc0+NOT_MEASURED1 và REST403 rc3 được đo riêng. |
| A8 | suite passed 48/48,209/209,2 tự kiểm; **nghĩa vụ độ phủ M11 chưa đạt** vì F10. Không lấy tổng suite thay coverage. |
| A9 | phần đăng ký/negative/regex/pin-probe đã đo; **full --chay not_run** theo chỉ thị chưa chạy gate nặng. Fixture signer trong phan_chung bị sandbox từ chối, ghi not_measured; không gọi đó là pass. |
| A10 | offline replay passed byte-match cả hai run; LIVE mới/freshness log không đo. Chi tiết dưới. |
| A11 | passed Ruff hai tệp, doctrine10/0 và ADR53/53, diff/check/write set; số dòng1505 được báo theo authority nâng trần. |
| A12 | not_run/not_measured: chưa đẩy nhánh code, không có mạng đo remote fence; phải đo trước lần đẩy theo authority. |
| A13 | incomplete: metadata đúng thread đã đọc; rollout hash/launcher receipt chỉ chốt sau tiến trình kết thúc; không tự nhận approval. |
| A14 | passed c25 env mang màu không xác thực, không marker; mutant dựng kịch bản từ dòng màu GIET đúng ca. |
| A15 | passed c26 khối chỉ là tập con không được xác thực; mutant subset GIET đúng ca. |
| A16 | passed c27 luật toàn khối và đối chứng lời gọi tối giản; các mutant nguyên văn/allowlist GIET đúng ca. |
| A17 | passed các vế c28 env bước, c29 env job, c30 đối số sau script, c31 tiền tố/defaults/shell/workflow env. F10 còn lỗ miền bổ sung, D01 null chưa chốt riêng. |
| A18 | passed c32 workflow thiếu object/path/YAML/SHA checkout chưa đo không sinh marker, không ném ở tập đã thử; mutant head_sha fallback GIET đúng ca; c34 đo reader Git thật. |
| A19 | passed c33 hai chiều và mutant; vị trí job thứ hai còn thiếu răng thuộc F10. |
| A20 | passed c36 thiếu/thừa log/REST và mutant số đếm. |
| A21 | passed c37 và mutant tên; các miền ghép mới ghi F10. |
| A22 | passed c38/calendar và mutant; lượng từ “mọi bước” bổ sung còn F10. |
| A23 | passed c39 và mutant duy nhất/prefix/expression; biên exact key cùng alias job khác còn F10. |
| A24 | passed c40/c35 và mutant nested không tương đương; nested-after-only tương đương được chứng minh riêng. |
| A25 | passed c41 uses/composite/count, mutant đúng ca. |
| A26 | passed c42 ENV/PATH ba chiều, c47 và c48 skipped; các chốt vị trí đã liệt kê F10. |
| A27 | passed c43 khối khác bước, mutant đúng ca. |

**Kết quả chạy và chọn phép đo.** Từ gốc workspace: `python -B .review/run.py <nhãn> <command...>`. Wrapper đặt bytecode off, TMPDIR/TMP/TEMP/cache trong `.review/`, ghi command, rc thật, thời gian, stdout/stderr size/hash. Hai kiểm Ruff tách biệt: bare lint hai tệp rc0,0 finding; pin/probe contract [] lỗi/3 probe. Bare lint `scripts/tl.py` không chạy, không suy từ contract. Heavy/release/CI/LIVE không chạy theo authority hiện hành.

```
CA: 48/48 dat
DOT BIEN: 209/209 bi giet dung ly do
TU KIEM PHAN HANG: DAT (2 dot bien)
TONG: DAT
```

Audit từng mutant catalogue: 209 GIET đúng ca; hai tự kiểm lần lượt TIN_DUNG_GIA và SONG_SOT có chủ ý. `mutants/results.json` giữ neo/thay, ca đích, baseline, lệnh/rc/output/hash; không cấp tín dụng cho setup/import/permission. `frontier5/results.json` chạy cả 48 ca trên mỗi mutant mới; survivor nào chỉ khác miền chưa định nghĩa được phân P3. Bộ toán tử kế thừa chạy lại **130/130 đúng ca** tại exact HEAD bằng `operators5_target.py`, chọn ca đích đã giết ở lượt4, không tuyên bố quét lại mọi lỗi vô can của 48 ca trên mỗi toán tử. `remaining5.py` cũng chọn exact catalogue target khi neo/thay trùng; các mục không có target chạy đủ ca. Phạm vi lựa chọn được giữ trong JSON từng mục, không lấy rc0 driver làm kết quả con.

Các script cũ có neo hoặc scaffolding stale được giữ lỗi gốc, rồi sửa CHỈ bản sao scratch: thiếu object9e5019e dùng source r2 được giao và khai chưa xác thực OID; boundary raw thiếu REST steps dùng bản current; emitter/composite phải chờ stdout suite thật; registry đổi số đếm sang48/209. `prior-reruns.json`, `remaining5-results.json`, `legacy-final-results.json`, `legacy-reanchored.json` và inventory ghi lệnh/rc. Script dựng snapshot/chuẩn bị/render verdict lịch sử không được dùng để ghi đè verdict hiện hành; các phép đo trùng byte giữa lượt1–4 được nối đến producer đã chạy, không tự nhận thêm số mẫu độc lập.

**Replay A10 offline.** 37/37 full log khớp SHA256SUMS và hash/size trong provenance; workflow đọc bằng Git tại checkout SHA. Cả hai provenance giống **từng byte** với `.review-input/a10/` đo trên52e9573: **0 khác biệt** cần giải thích. `replay5-details.json` và `prior2/q1-summary.json` giữ stdout, hash, API mock call và đối chiếu độc lập.

| run / attempt | Run | Checkout / ghép bước | Gate và marker MOI | SHA-256 provenance |
|---|---|---|---|---|
|39342960764 /1|passed|13 passed ở b27fe85…, 1 chuan-bi not_measured; ghép13/14|14 Gate not_measured,0 failed;0 marker cho đường dẫn MOI; các đường ngoài MOI vẫn not_measured|`5ad9afeafb5312101ae326d738855e8adb1e46e7e4240944c2b21e12ed2bafe0`|
|40074551995 /1|passed|22 passed ở dc65714…,1 chuan-bi not_measured; ghép22/23|23 Gate not_measured,0 failed;8 gate-nhanh-manh có nhanh_don_duoc not_measured/che_do_khong_xac_dinh; gate-nhanh-gop không marker|`24ffa770ff268876c030f12f59fee1010956138ba2ca3fa4370710456ffd185b`|

Mọi labels đều ubuntu-latest; Workflow definition cả hai luôn not_measured. Replay không đo endpoint LIVE hiện tại, Windows/pwsh thật, PR synthetic merge thật, action đổi môi trường hay receipt vận chuyển cuối phiên.

**Danh sách mutant còn sống và phân hạng.** Với mỗi dòng dưới, toàn bộ48 ca hiện hành xanh; ngoài mutant tương đương được chứng minh riêng bằng AST và 6 vị trí, `counterexamples5.json` ghi baseline0 → mutant3/DO đúng tên bằng `cases5.py <tên>`. Chỉ mô tả hướng vá sản phẩm; các script được cung cấp là dữ liệu phản chứng/test, không phải patch trên nhánh Executor.

| mutant | hạng | kết quả/đề xuất |
|---|---|---|
|n_goi_strip_run|P1 / F10|48/48 xanh; phản chứng dấu nối dòng + khoảng trắng, norm_counterexample5.py; bổ sung ca vào suite và DOT_BIEN.|
|wf_env_dict_only|P1 / F10|Baseline0 → mutant3 đúng ca; xem neo/thay và output đầy đủ trong frontier5/results.json, counterexamples5.json.|
|wf_env_nonempty_only|P1 / F10|Baseline0 → mutant3 đúng ca; xem neo/thay và output đầy đủ trong frontier5/results.json, counterexamples5.json.|
|job_env_only_first_key|P1 / F10|Baseline0 → mutant3 đúng ca; xem neo/thay và output đầy đủ trong frontier5/results.json, counterexamples5.json.|
|mode_last_step|P1 / F10|Baseline0 → mutant3 đúng ca; xem neo/thay và output đầy đủ trong frontier5/results.json, counterexamples5.json.|
|mode_first_run_step|P1 / F10|Baseline0 → mutant3 đúng ca; xem neo/thay và output đầy đủ trong frontier5/results.json, counterexamples5.json.|
|mode_first_job|P1 / F10|Baseline0 → mutant3 đúng ca; xem neo/thay và output đầy đủ trong frontier5/results.json, counterexamples5.json.|
|dd_first_job|P1 / F10|Baseline0 → mutant3 đúng ca; xem neo/thay và output đầy đủ trong frontier5/results.json, counterexamples5.json.|
|job_match_exact_preference|P1 / F10|Baseline0 → mutant3 đúng ca; xem neo/thay và output đầy đủ trong frontier5/results.json, counterexamples5.json.|
|job_first_prefix_only|P1 / F10|Baseline0 → mutant3 đúng ca; xem neo/thay và output đầy đủ trong frontier5/results.json, counterexamples5.json.|
|time_name_last_key|P1 / F10|Baseline0 → mutant3 đúng ca; xem neo/thay và output đầy đủ trong frontier5/results.json, counterexamples5.json.|
|time_only_last_group|P1 / F10|Baseline0 → mutant3 đúng ca; xem neo/thay và output đầy đủ trong frontier5/results.json, counterexamples5.json.|
|name_skip_first_yaml|P1 / F10|Baseline0 → mutant3 đúng ca; xem neo/thay và output đầy đủ trong frontier5/results.json, counterexamples5.json.|
|rest_sort_lexical|P1 / F10|Baseline0 → mutant3 đúng ca; xem neo/thay và output đầy đủ trong frontier5/results.json, counterexamples5.json.|
|rest_number_integral_float|P1 / F10|Baseline0 → mutant3 đúng ca; xem neo/thay và output đầy đủ trong frontier5/results.json, counterexamples5.json.|
|ghep_zero_groups_reject|P1 / F10|Baseline0 → mutant3 đúng ca; xem neo/thay và output đầy đủ trong frontier5/results.json, counterexamples5.json.|
|env_false_accept|P1 / F10|Baseline0 → mutant3 đúng ca; xem neo/thay và output đầy đủ trong frontier5/results.json, counterexamples5.json.|
|env_int_accept|P1 / F10|Baseline0 → mutant3 đúng ca; xem neo/thay và output đầy đủ trong frontier5/results.json, counterexamples5.json.|
|env_empty_str_accept|P1 / F10|Baseline0 → mutant3 đúng ca; xem neo/thay và output đầy đủ trong frontier5/results.json, counterexamples5.json.|
|prior_run_only_strings|P3|Đặc tả không chốt cách diễn giải run không phải chuỗi ở bước TRƯỚC; runner không nhận workflow run là list. Đề xuất chủ kho ghi quyết định fail-closed cho dạng này ở revision/successor; không đổi sản phẩm chỉ để giết mutant hiện tại.|
|prior_path_suffix|P1 / F10|Baseline0 → mutant3 đúng ca; xem neo/thay và output đầy đủ trong frontier5/results.json, counterexamples5.json.|
|prior_env_word_boundary|P1 / F10|Baseline0 → mutant3 đúng ca; xem neo/thay và output đầy đủ trong frontier5/results.json, counterexamples5.json.|
|nested_only_after_shell|P3|TƯƠNG ĐƯƠNG, trùng ngữ nghĩa log_nested_after_only: AST bằng bản đã chứng minh; trước shell đã bị chốt cấu trúc chặn, sau shell hai điều kiện giống nhau. 6/6 vị trí đo bằng nhau; đề xuất không cố giết mutant tương đương. Xem nested5-equivalence.json và equivalence.json.|
|header_colored_exact|P1 / F10|Baseline0 → mutant3 đúng ca; xem neo/thay và output đầy đủ trong frontier5/results.json, counterexamples5.json.|
|run_blank_tail_only|P1 / F10|Baseline0 → mutant3 đúng ca; xem neo/thay và output đầy đủ trong frontier5/results.json, counterexamples5.json.|
|run_trailing_lf_exact|P1 / F10|Baseline0 → mutant3 đúng ca; xem neo/thay và output đầy đủ trong frontier5/results.json, counterexamples5.json.|
|name_uses_strip|P1 / F10|Baseline0 → mutant3 đúng ca; xem neo/thay và output đầy đủ trong frontier5/results.json, counterexamples5.json.|
|env_prefix_value_only|P1 / F10|Baseline0 → mutant3 đúng ca; xem neo/thay và output đầy đủ trong frontier5/results.json, counterexamples5.json.|

Các P3 trên: owner đề xuất `ducthangho`; giữ nợ/quyết định trước khi có revision chốt miền, không tự sửa tiêu chuẩn nghiệm thu. Không coi chúng là ca phải giết để làm đẹp tổng. F10 P1 vẫn chặn approval riêng.

**Toàn bộ inventory, gồm mutant bị giết và TÍN DỤNG GIẢ.** [MUTANTS.md](MUTANTS.md) là danh sách từng ID với phân hạng/ca đích/scope và nguồn JSON, thuộc gói verdict này. Các lần đo trùng neo/thay được giữ provenance, không cộng thành số mutant độc lập. Phân bố từng producer:

| producer | phân hạng thật |
|---|---|
|mutants|{'GIET': 209, 'TIN_DUNG_GIA': 1, 'SONG_SOT': 1}|
|frontier|{'GIET': 48, 'HONG_NEO': 1, 'SONG_SOT': 1}|
|frontier2|{'GIET': 11}|
|new-frontier|{'GIET': 20}|
|frontier5|{'SONG_SOT': 27, 'GIET': 18, 'GIET+NEM': 1}|
|operators5-target|{'GIET': 130}|
|prior2/extra-r4|{'SONG_SOT': 1, 'GIET': 12, 'HONG_NEO': 5, 'TIN_DUNG_GIA': 1}|

**TÍN DỤNG GIẢ / ngoại lệ ngoài ca đích.** Các lỗi dưới đây không được tính GIET; một mutant có ca đích chết đúng vẫn chỉ nhận tín dụng cho ca ấy. Phép toán tử chạy theo target không có phạm vi quan sát các lỗi ở ca khác của lượt4.

| producer / mutant | ca lỗi vô can |
|---|---|
|frontier5 / header_seconds_round|c38_ghep_lech_gio|
|prior2/extra-r4 / number_missing_tu_sinh|c22_thieu_dinh_danh_khong_passed|

**Read-only và bàn giao.** `snapshot-start.json`/`snapshot-end.json` và `snapshot-comparison5.json` so hash/bytes toàn bộ tracked/untracked/ignored ngoài `.review/`, HEAD/tree/diff/index; không có delta quan sát được, `git status --short` sạch. Chỉ chứng minh hai mốc, không chứng minh lịch sử chưa từng ghi rồi hoàn nguyên. Repo nguồn ngoài checkout không nằm trong phạm vi quan sát. `evidence-manifest5.json` băm các hiện vật sau khi mọi writer test kết thúc, không tự chứng nhận runtime/transport sau phiên. Không có quyền approve/merge/land/LIVE từ verdict này.
