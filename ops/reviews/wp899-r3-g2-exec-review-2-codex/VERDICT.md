verdict: changes_requested
reviewed_sha: 7f5a02c9c2ff346484e10c2f5b4e94fcb0468b8b
base_sha: dc657149941f9db3ab2afc6fb6462ba4827bf18f
Reviewed commit: 7f5a02c9c2ff346484e10c2f5b4e94fcb0468b8b
reviewed_tree: a6b391d5a467aa457f5770d3a99dc2dd208403d6
packet: wp899-r3-g2
review_round: 2
role: reviewer
provider: openai_codex
model_family: openai
model: gpt-6.1-sol (CLI-published)
effort: xhigh (CLI-published)
session_id: 01a16dbe-aca3-7472-bcfb-157cff53f305
model_reviewer_identity: openai_codex/gpt-6.1-sol/01a16dbe-aca3-7472-bcfb-157cff53f305 (CLI-published)
execution_surface: codex_cli
transport: machine
independent_from_executor_session: true
review_axes: [spec, standards_security]
github_submitter_identity: null
assurance: review_deferred

**Chưa đạt V2: một lớp mở — P0=1, P1=0, P2=0, P3=0 (đếm theo lớp, lấy hạng cao nhất). F02 `nhac-ten-script-thanh-thuc-thi` LẶP LỚP ở lượt 2 r3 ⇒ DỪNG HẲN theo V5.** F08 đã vá thật. Sáu phản chứng lượt 1 đều xanh, tám biến thể collision cũ đều `not_measured`; nhưng còn va chạm nguồn: nhóm Run của composite action được xác thực bằng `run:` ở job/bước khác vốn bị tắt. Shell của composite có thể không chạy script được in lại, mà công cụ vẫn ghi marker/Gate `passed`. Nhóm con sau `shell:` còn có thể đóng nhầm nhóm cha và che dòng màu muộn.

Đây là lời gọi **6/8 theo assignment**, không tự xác minh sổ chi remote. Không đổi slug để né lịch sử F02. V5 không cấp vòng vá tiếp; HINT chỉ phục vụ checkpoint của chủ kho. Verdict không cấp approval, quyền đẩy, merge, land, LIVE hay chuyển state.

**Preflight và authority.** Đã đọc toàn bộ prompt, đặc tả r3/r2, bốn verdict r2, verdict/script phản chứng r3 lượt 1, tài liệu entry point và skill cross-review. Spec authoritative của assignment `.review-input/wp899-r3.md`: **18.402 byte**, SHA-256 `dd1a997d1f3682e23bb4b5577264076b7d9a12aeff5d9823f491cdda05e4f36f`; r2 **23.189 byte**, SHA-256 `d858c7c65a38a7f0fadda1cabf839c98ce70a881372d847c8979165925971707`. Cả hai khớp. Revision3/generation2, sensitive. Giữ Q1–Q8 và quyết định nâng trần prompt dẫn từ issuecomment-6383572422: **≤8 tệp/≤1050 dòng thêm**, effective write set vẫn chỉ ba tệp.

Origin `https://github.com/ducthangho/tra-luat.git`; detached HEAD/tree đúng đầu verdict; parent `29d641cbd4a38504eb30d87f0fc7eaa82a185f24`. Base tồn tại, `git merge-base --is-ancestor <base> HEAD` **rc0**; kho không shallow; `core.abbrev=7` đã có, không sửa config. Baseline nghiệm thu giữ `dc657149941f9db3ab2afc6fb6462ba4827bf18f`; điểm xuất phát `9e5019ef2e3b8d59345fff2165569c3281cba3b5` không thay baseline. Tự so blob OID ba tệp ở điểm xuất phát với `19b114867fbcad4c3b580bcbe4367bc78a890773`: **3/3 khớp** (`startpoint.json`). Lease/state/ref freshness/authority remote **KHÔNG ĐO ĐƯỢC** trong assignment offline.

Numstat từ base **rc0**: `.claude/dev/ci_dang_ky_test.py` **1/0**, `ops/ci_provenance.py` **393/0**, `ops/ci_provenance_test.py` **656/0**: **3 tệp/1050 dòng thêm**, đúng write set, chạm trần. Mục MOI thêm đúng một dòng. `git diff --check <base> HEAD` **rc0**. Đã đọc toàn mã mới/diff đầy đủ/delta lượt1; bằng chứng `preflight.json`, `full.patch`, `delta.patch`.

**Môi trường/identity và cách tái hiện.** Linux x86_64, Python **3.13.17** (`/usr/bin/python`), PyYAML **6.0.3**, Git **2.43.0**, Ruff **0.15.15**, codex-cli **0.164.0**. `preflight.json` trích metadata đúng thread từ `/root/.codex/sessions/2026/10/24/rollout-2026-10-24T11-49-36-01a16dbe-aca3-7472-bcfb-157cff53f305.jsonl`: session ID khớp thread môi trường, originator=codex_exec, provider OpenAI; turn_context công bố model/effort trên. Đây là **model do CLI công bố**; model phục vụ từng request **KHÔNG ĐO ĐƯỢC**. Không băm rollout đang ghi để nhận receipt cuối A13. Executor Claude/cloud/model_family=claude là thông tin spec, chưa có runtime receipt Executor độc lập trong assignment.

Sandbox thực tế `workspace-write`; read-only đối với candidate được giữ bằng hành vi/snapshot, không tuyên bố OS khóa ghi toàn cây. Catalog không có `environment_status`. Không gọi subagent, mạng/GitHub/LIVE, push hay sửa sản phẩm. Doctor/chuan-bi, cài dependency, native Windows/pwsh và full runtime/release gates **not_run**. Lệnh A9 tự gọi signer fixture qua loopback và bị sandbox từ chối; không bypass signer/trust/quyền.

Từ gốc workspace: `python -B .review/run.py <nhãn> <command...>`. Wrapper đặt `PYTHONDONTWRITEBYTECODE=1`, TMPDIR/TMP/TEMP/cache trong `.review/`; mỗi receipt giữ command, **rc con thật**, thời gian, size/hash stdout/stderr. Rc0 của driver thu thập không thay rc phép thử trong JSON. Mọi script/fixture/mutant/output reviewer nằm trong `.review/`.

Lần chạy review_cases trước khi suite xong thiếu `suite.stdout.txt`, làm emitter lỗi setup. Giữ riêng `review-cases-before-suite.*`, `r4-comparison-before-suite.*`; **không dùng làm finding hoặc tín dụng giết**. Sau khi stdout suite thật ổn định, chạy lại nguyên script: sáu ca DAT, r2→r3 và tám collision đúng như dưới. Không dùng stdout executor thay kết quả suite tự chạy.

**ĐỐI CHIẾU F01–F08 / LƯỢT TRƯỚC.** Nguồn gần nhất `.review-input/r3-luot1/VERDICT.md`, SHA `29d641cbd4a38504eb30d87f0fc7eaa82a185f24`; giữ lịch sử r2, đặc biệt F02 mở bốn lượt r2 rồi còn mở ở r3 lượt1.

| lớp | phân loại trên candidate | phép đo độc lập / phạm vi |
|---|---|---|
| F01 `thieu-dinh-danh-van-passed` | **GIỮ ĐÃ VÁ THẬT trong phạm vi đo** | c22/các mutant F01 GIET đúng ca; chạy lại probe Run thiếu head/event/path, steps rỗng/sai phần tử, URL sai kiểu/newline: không nâng mốc thiếu thành passed, không ném ở các shape đã đo. Không lấy riêng kich_ban.trang_thai=passed làm chứng minh bước đã xác thực. |
| F02 `nhac-ten-script-thanh-thuc-thi` | **VÁ HỜ ở cấp đóng lớp; LẶP LỚP — P0** | Sáu ca reviewer lượt1 rc0; hai cơ chế r4 trên source r2 Gate passed→candidate not_measured; tám collision khác job/cùng job/thứ tự/env nay not_measured. c35/năm mutant cấu trúc có răng. Nhưng composite-origin collision còn passed sai; endgroup con sau shell còn làm khối cha thiếu/mất màu được xác thực. Chi tiết bảng lớp. |
| F03 `phan-trang-dem-thay-vi-chung-minh-du` | **GIỮ ĐÃ VÁ THẬT trong phạm vi đo** | c20/mutant và probe cả jobs/artifacts: total2→3 dù cuối đủ ID vẫn du=false; total ổn định du=true; empty/duplicate/underreported không được khai đủ. |
| F04 `rest-gia-khong-neo-run` | **GIỮ ĐÃ VÁ THẬT trong phạm vi đo** | RestGia trả404 cho run6/jobs run6/artifacts run6/logID lạ; attempt khác đọc state tương ứng; hai mutant URL run+1 GIET c20. |
| F05 `duong-loi-bo-dong-dem-bat-buoc` | **GIỮ ĐÃ VÁ THẬT trong phạm vi đo** | c01/c19 và mutant summary/projection/lưới cuối GIET. HTTP403 ở bốn endpoint, Run list/null/string, lỗi ghi và AttributeError tiêm tại thu giữ summary và rc/ngoại lệ thật. Không suy mọi lỗi đã được thử. |
| F06 `redirect-loi-thoat-ngoai-bo-boc` | **GIỮ ĐÃ VÁ THẬT trong phạm vi đo** | c24/hai mutant GIET: direct/sau302 URLError/OSError thành LoiRest; redirect thành công giữ bytes; blob request là URL trần. Mock offline, mạng thật KHÔNG ĐO ĐƯỢC. |
| F07 `a10-doi-sha-khi-checkout-skipped` | **GIỮ ĐÓNG BẰNG AUTHORITY** | Áp đính chính13+1; tự replay đủ14 full logs run39342960764/Git local:13Checkout passed, chuan-bi not_measured. Không dựng SHA cho job không checkout. |
| F08 `nguon-workflow-git-khong-duoc-kiem-thu` | **ĐÃ VÁ THẬT trong phạm vi đo** | c34 gọi git_blob thật trên tree tự dựng, HEAD chưa sinh: đúng bytes/newline, thiếu path/non-UTF8 trả None. Hai mutant cũ chạy lại **mọi35 ca**: mỗi con chỉ chết c34, rc3/DO:c34_git_blob_that do TinHieuChotCa;34 ca khác xanh. Ca reviewer git_workflow_source đọc commit thật b27fe85 so git bytes cũng xanh, hai mutant chết đúng ca reviewer. |

U cuối lượt1={F02,F08}; F sửa thật={F08}; tỷ lệ **1/2=50%**. Không có slug nguyên nhân mới trong tập kiểm; hai biểu hiện mới nối F02. Tỷ lệ không thay V5. Tree của c34 kiểm hợp đồng `<oid>:<path>` của reader; ca reviewer trên commit thật kiểm thêm đường commit. Fixture c34 tự đủ, không cần commit/ký/object lịch sử trên CI. Lỗi setup Git sẽ là HONG, không phải TinHieuChotCa; trên runtime này baseline và hai target mutant đã chạy thật.

**BẢNG LỚP CÒN MỞ.** Một lớp/hai nhóm biểu hiện, hạng cao nhất P0. Biểu hiện b chỉ khẳng định P1 về cấu trúc trên dữ liệu dựng.

| lớp | hạng | biểu hiện (tệp:dòng) | phép đo tái hiện | HINT patch | ước lượng dòng |
|---|---|---|---|---|---|
| **F02 `nhac-ten-script-thanh-thuc-thi` — LẶP LỚP ⇒ V5** | **P0** (a); **P1** (b) | **a.** `ops/ci_provenance.py:165`, `:167`, `:215`, `:245`, `:249`, `:257`, `:278`: guard mới chỉ thấy uses mức job; bước uses không có run bị bỏ khỏi inventory. Mọi nhóm Run được xét độc lập nên substep composite trùng run ở job bị tắt/sibling skipped được xác thực; shell/env thật của substep không nằm trong ứng viên ấy. **b.** `:219`, `:224`, `:226`: nhóm không phải Run sau shell bị bỏ qua; endgroup con đóng luôn cha, màu muộn chuyển sang phan, không làm hop_le=false. | **a.** `python -B .review/run.py composite-final python -B .review/composite_case.py`: **rc3/DO:F02_composite_origin_collision**, đúng TinHieuChotCa. Bash thật rc0, trace chỉ `python -B .review/emit.py .review/composite/runner-step.sh`, **không chạy target** ops/ci_provenance_test.py. Tool **rc0, marker target/Gate passed, buoc_xac_thuc=1**. Bỏ decoy khỏi YAML/giữ log ⇒ không marker/Gate not_measured; env-decoy ⇒ che_do_khong_xac_dinh. Matrix khác-job trước/sau/cùng-job skipped đều tái hiện; parent/candidate đỏ cùng chốt. **b.** `python -B .review/run.py boundary python -B .review/boundary_case.py`: **rc3/DO:F02_nested_incomplete_echo** đúng chốt; cha thiếu đóng/còn màu muộn vẫn **hop_le=true, buoc_xac_thuc=1, Gate passed**. Đối chứng không endgroup/nested trước shell ⇒ không xác thực. | **Ở đâu:** hợp đồng nguồn/ranh giới giữa ung_vien, tach_buoc và do_dau_duong, trước equality Q2. **Cách rẻ:** fail-closed khi không loại trừ được nhóm thuộc uses/composite chưa giải, hoặc nhóm lồng làm nguồn/đóng khối mơ hồ; không chỉ thêm một luật màu. Giữ YAML tại SHA làm nguồn script/equality/vế chặt nhất. Không cần hỗ trợ thực thi composite để từ chối đo nó. Đường đắt là gắn nhóm đúng bước/job/nguồn action, cần authority nếu đổi phạm vi/Q2. **Khóa:** composite_case/boundary_case, matrix ba vị trí decoy/không-decoy/env-decoy, sáu ca cũ/A14–A19/simple/CRLF. Mutant bỏ guard nguồn/đóng nhóm phải chết đúng ca; chỉ đổi guard shell top-level không giết composite case này. **Rủi ro:** chặn mọi uses mù sẽ mất coverage workflow có checkout/setup; phải khai not_measured, không whitelist tên action thay bằng chứng đã giải nguồn. Xử lý nested phải giữ nhóm output sau metadata đã đóng. | **Ước lượng chưa áp:** khoảng20–40 dòng ròng gồm ca/mutant cho fail-closed bảo thủ; ánh xạ nguồn đầy đủ chưa ước lượng được trong trần. Candidate **không còn dư dòng**; V5 đã chạm, không cấp quyền vá/nâng trần. |

**Căn cứ và giới hạn F02.** `composite/action.yml` khai custom shell `python -B .review/emit.py {0}`; runner script là `python ops/ci_provenance_test.py`, nhưng shell thật chỉ in stdout suite đã đo trước đó, không chạy script argument. Không lệnh workflow/action nào in giả `##[group]Run`; nhóm là dữ liệu harness mô phỏng runner vọng lệnh. Workflow/action/log giữ cố định khi thêm/bỏ/đảo decoy; chính va chạm nguồn làm trạng thái đổi. Shell thật ở action không được áp guard shell của ứng viên top-level. Đây là F02 (nguồn khác dùng chứng minh target đã chạy), mạnh hơn việc chỉ thiếu chế độ của một lời gọi đã chạy; không tách slug mới để né V5.

Đã chạy shell/parser thật, **MOI/regex thật và stdout suite thật**. REST/workflow tại SHA/checkout/Git callback của phản chứng là fixture; không giả workflow đó là workflow của b27fe85. Log Actions-shaped do reviewer dựng, **không** mới tải từ GitHub; runner thật render composite/custom shell/nested như fixture hay không **KHÔNG ĐO ĐƯỢC** offline. Không tuyên bố lỗi đã xảy ra trong hai run A10. Giữ giới hạn “không chống tác giả workflow”: không yêu cầu chống workflow cố ý in nhóm Run giả hoặc sửa test. Lỗi đo ở đây là shell ngoài grammar trong composite chưa giải lại được chứng nhận bằng grammar/shell của một run không chạy ở nơi khác. Scope composite chưa hỗ trợ phải giữ chưa đo khi nguồn mơ hồ. Biểu hiện b kiểm fail-closed cho log thiếu/mất màu cùng miền phản chứng lượt1, không khẳng định Actions đã sinh nó.

**Quét bản vá/log thật.** Chạy nguyên `.review-input/do_cau_truc.py`: **rc0**,37 tệp/325 nhóm Run/226 nhóm màu, **226** header khớp dòng màu đầu, **226** ngay sau màu là shell, **226** có đóng, **0** màu muộn theo phép đo, **226** hop_le. Tự kiểm **37/37 SHA256SUMS** (`log-hash-check.json`). Đo thêm trên full logs: **0** nested trong metadata trước dấu đóng đầu, **0** dòng màu rỗng, **0** tệp CRLF, **0** endgroup có hậu tố, **0** env trước shell. Corpus không có các hình dạng ấy nên226/226 không chứng minh parser đúng trên chúng.

`probes.py` chạy lại đủ **85 nhóm đo** lượt1; `new_probes.py` thêm nhóm con trước/sau shell, cha chưa đóng, màu muộn sau dấu đóng con, suffix, shell/env đảo, CRLF, blank/whitespace màu, header dài/truncated, composite collision và đối chứng. CRLF/simple đo được; env trước shell/blank không màu/header cắt đều chưa xác thực. Header dài vẫn định vị đúng, path ngoài MOI giữ chưa đo. Dòng màu rỗng ở đuôi có thể không khớp sau rstrip newline: ghi giới hạn coverage, không nâng thành pass. Không tìm slug mới ngoài F02 trong tập kiểm. Hướng cần payload nhạy cảm path/symlink/credential chỉ mô tả bằng lời, **KHÔNG ĐO ĐƯỢC**, không tự soạn/thử.

**ĐỐI CHIẾU A1–A19.** Passed phạm vi ca không thay việc M4/F02 chưa đạt; failed, skipped, not_run, not_measured giữ riêng.

| tiêu chí | kết quả | evidence / phạm vi |
|---|---|---|
| A1 | **passed** | c01/help rc0 đủ bốn cờ; mutant bỏ attempt GIET đúng c01; sai đối số giữ rc2/summary4. |
| A2 | **passed** | c02/mutant bỏ so attempt GIET: attempt2 so yêu cầu1 failed/rc12. |
| A3 | **passed phạm vi bảy ca** | c03–c09 và mutant duy nhất SHA/thiếu/Linux-only/REST head/quan hệ PR GIET đúng ca; fixture Windows không phải execution Windows. Ca reviewer reader Git trên commit thật xanh. |
| A4/M4 | **năm ca hẹp passed; M4 failed — F02** | c10–c15/runner0/not_run/skipped/marker lệch/khác bước/ngoàiMOI/import động đạt, mutant có răng; composite-origin vẫn cấp passed sai. |
| A5 | **passed** | c16/mutant path⇒passed GIET; Workflow definition luôn not_measured, REST path chỉ lời khai. |
| A6 | **passed phạm vi lỗi thử** | c17/mutant ghi thẳng GIET; lỗi giữa chừng giữ bản trước/không out. Không đo power loss/crash/writer cạnh tranh/native Windows. |
| A7/M7 | **passed phạm vi đo** | c18 summary1/rc0; c19 bốn endpointHTTP403/rc3/summary4; Run sai dạng/lỗi ghi/lưới cuối giữ summary; mutant tương ứng GIET. Không đọc rc0 thành đủ bốn mốc. |
| A8/M8/M11 | **suite/phân hạng passed; không đóng F02** | Suite **rc0: CA35/35, DOT BIEN74/74, TU KIEM DAT(2), TONG DAT**. Audit riêng76 mutant có baseline từng target. Tiêm mutant AttributeError qua except đổi kiểu vào DOT_BIEN trong bộ nhớ ⇒ **CA35/35, DOT BIEN0/1, TIN_DUNG_GIA, TONG DO, main rc1**; driver classifier rc0 chỉ thu kết quả. |
| A9 | **lệnh failed rc1; full acceptance KHÔNG ĐO ĐƯỢC vì môi trường** | `python -B .claude/dev/ci_dang_ky_test.py --chay`: ĐĂNG KÝ25/25, LAUNCHER WINDOWS4/4, RUFF CI3/3, rồi git commit fixture **rc128**, signer loopback `socket: operation not permitted`. Dừng trước chay_moi; không chứng nhận test đã chạy qua lệnh này. kiem() thật errors=[]/25/25; bỏ mục registry trong bộ nhớ ⇒ đúng lỗi test sống chưa đăng ký/25/24. Regex bằng tiền lệ, nhận suite thật, từ chối tổng lệch/0mutant/TONG DO (`readback2.json`). |
| A10 | **replay frozen passed; LIVE độc lập KHÔNG ĐO ĐƯỢC** | Replay37full logs, hash/size37/37 khớp provenance; workflow/parents/tree dùng Git thật; hai provenance **trùng byte** với bản đóng băng. Chi tiết dưới; không có HTTP receipt/mạng mới để tự xác thực nguồn GitHub. |
| A11 | **passed theo trần đã cấp** | doctrine-scan rc0:10tệp/0chép; adr-song rc0:53/53 khớp1–1, tha0016; Ruff `check --no-cache --select F` đúng hai tệp rc0/All checks passed;3tệp/1050dòng, diff-check rc0. Ruff pin/probe contract riêng loi_ruff_ci()=([],3), không dùng thay bare lint. |
| A12/V1–V5 | **KHÔNG ĐO ĐƯỢC remote/future; V2 failed, V5 chạm** | Không ls-remote/push/connector trong assignment. F02P0 lặp lượt2r3 ⇒ dừng hẳn; không có quyền đẩy/mở lượt vá tiếp. |
| A13 | **KHÔNG ĐO ĐƯỢC hoàn chỉnh** | Có model/effort/thread metadata đúng run; bên vận chuyển cần stdout thread.started, launcher run.json, rollout/hash ổn định sau khi tiến trình kết thúc, đối chiếu1–5. Không nhận rollout đang ghi là receipt cuối. |
| A14 | **passed ca chỉ định; F02 còn mở** | c25/mutant dựng script từ màu GIET; replay r4_env r2passed→r3not_measured. |
| A15 | **passed ca chỉ định; F02 còn mở** | c26/mutant tập con GIET; replay r4_mixed/tám collision cũ bị chặn; không thay phép đo nguồn composite bằng ca này. |
| A16 | **passed ca/mutant chỉ định; xác thực rộng còn F02** | c27 âm nonminimal/đối chứng toàn minimal; mutant bỏ whole-block/equality GIET. Cha đóng nhầm vẫn cho tập con khớp ứng viên khác. |
| A17 | **passed ba vế và đối chứng** | c28/c29/c30 và ba mutant đúng ca; c31/các chốt phụ cũ và guard job-uses mới có răng. Shell/env composite chưa giải không nằm trong các ứng viên này. |
| A18 | **passed phạm vi đo, F08 đóng** | c32 thiếu object/path/YAML/SHA qua fixture không ném; mutant REST head thay checkout/YAML hỏng GIET; c34/commit reviewer và hai mutant F08 có răng. |
| A19 | **passed ca chặt nhất** | c33/lấy ứng viên đầu GIET; env-decoy vẫn chặn. Decoy không env khác job/sibling bị tắt không xác định được nguồn composite — F02. |

**A10 — replay độc lập từ dữ liệu đóng băng.** `python -B .review/run.py readback2 python -B .review/readback2.py` **rc0**. Script dựng response Run từ field frozen của provenance, dùng jobs được giao và artifacts frozen; không giả thành raw HTTP mới. Logs đọc đủ37 tệp, hash/size từng log khớp log_day_du; git_blob thật đọc workflow tại SHA checkout, git_cuc_bo thật đọc metadata commit. Toàn provenance.yaml replay **bằng byte** với bản được giao:

| run / attempt | SHA-256 frozen = replay | kết quả đo |
|---|---|---|
|39342960764 / 1|`87b8be84f479d0b17b214a4d3b0983d2fd46b89089602f3e55f118bfaef206b4`|14jobs/labelsUbuntu;13Checkout passed tại `b27fe85c9e9593ddbb059808fe4347fe1bd267be`, chuan-bi chưa đo;14Gate not_measured;WD not_measured;summary16. Không marker MOI nào passed.|
|40074551995 / 1|`d2e5247ff36f512428b2e82a004f53cc8bfc59b7d584e7d3835aafbe7aa73c6a`|23jobs/labelsUbuntu;22Checkout passed tại base `dc657149941f9db3ab2afc6fb6462ba4827bf18f`, chuan-bi chưa đo;23Gate not_measured/0failed;WD not_measured;summary25. Tám gate-nhanh-manh có marker nhanh_don_duoc_test chưa đo/che_do_khong_xac_dinh; bước gom có đối số không sinh marker target.|

Khớp hash nội bộ không chứng minh nguồn HTTP hoặc chúng đã được thu trên exact HEAD này. A10LIVE vẫn cần evidence executor/điều phối readback; hai run frozen không thay CI required checks của candidate. Không nâng Workflow definition bằng YAML tại checkout.

**DANH SÁCH MUTANT VÀ HẠNG.** `mutants/results.json` giữ source/neo/thay, command, baseline rc, mutant rc/output/hash từng con. Mỗi target xanh trên bản sao gốc trước khi đột biến; chạy `python -B ops/ci_provenance_test.py --mot-ca <ca>` với `CI_PROVENANCE_MA=<bản sao>`. Chỉ rc3 + `DO:<đúng-ca>:` từ handler TinHieuChotCa tính GIET; rc4 là TIN_DUNG_GIA. Audit riêng **76 mutant phân biệt:74GIET,1TIN_DUNG_GIA,1SONG_SOT,0HONG**. Hai tự kiểm có hạng đúng chủ ý.

Hai mutant mang tên reviewer được chạy lại toàn35ca là **cùng hai phép thay** với F08 trong bảng, không cộng thêm thành mutant phân biệt; cả hai GIET đúng c34,34 ca khác xanh (`extra-mutants/results.json`, `classified.json`). Chúng còn GIET đúng ca reviewer git_workflow_source. Phản chứng F02 đỏ trên candidate không là mutant, không cộng vào số giết.

| mutant | ca đích | rc baseline → mutant | hạng |
|---|---|---|---|
| `A1_xoa_co_attempt` | `c01_cli_du_co` | 0 → 3 | **GIET** |
| `A2_bo_so_attempt` | `c02_attempt_lech` | 0 → 3 | **GIET** |
| `A3d_lay_sha_dau_tien` | `c06_checkout_hai_sha` | 0 → 3 | **GIET** |
| `A3c_thieu_la_do_duoc` | `c05_checkout_khong_sha` | 0 → 3 | **GIET** |
| `A3e_lay_head_sha_rest` | `c07_checkout_push_lech` | 0 → 3 | **GIET** |
| `A3b_chi_nhan_linux` | `c04_checkout_windows` | 0 → 3 | **GIET** |
| `A3g_pr_nhan_moi_sha` | `c09_checkout_pr_lech` | 0 → 3 | **GIET** |
| `A3_sha_khong_nguyen_dong` | `c05_checkout_khong_sha` | 0 → 3 | **GIET** |
| `A4d_regex_ca_log_job` | `c13_marker_buoc_khac` | 0 → 3 | **GIET** |
| `A4b_skipped_la_passed` | `c11_job_skipped` | 0 → 3 | **GIET** |
| `A4a_runner_0_la_passed` | `c10_runner_id_0` | 0 → 3 | **GIET** |
| `A4c_khong_khop_la_not_measured` | `c12_marker_khong_khop` | 0 → 3 | **GIET** |
| `A4_chep_cung_MOI` | `c15_moi_mot_nguon` | 0 → 3 | **GIET** |
| `A4_job_failure_bo_qua` | `c14_ngoai_moi` | 0 → 3 | **GIET** |
| `A5_passed_khi_co_path` | `c16_workflow_def_luon_not_measured` | 0 → 3 | **GIET** |
| `A6_ghi_thang_vao_out` | `c17_ghi_nguyen_tu` | 0 → 3 | **GIET** |
| `A7_bo_dong_dem` | `c18_dem_not_measured` | 0 → 3 | **GIET** |
| `A7_gop_rest_vao_12` | `c19_rest_loi` | 0 → 3 | **GIET** |
| `M1_chi_doc_trang_dau` | `c20_du_trang` | 0 → 3 | **GIET** |
| `F03_dung_khi_du_total` | `c20_du_trang` | 0 → 3 | **GIET** |
| `F03_tap_luon_du` | `c20_du_trang` | 0 → 3 | **GIET** |
| `F03_trung_id_van_them` | `c20_du_trang` | 0 → 3 | **GIET** |
| `F04_jobs_run_khac` | `c20_du_trang` | 0 → 3 | **GIET** |
| `F04_artifacts_run_khac` | `c20_du_trang` | 0 → 3 | **GIET** |
| `F01_run_thieu_van_passed` | `c22_thieu_dinh_danh_khong_passed` | 0 → 3 | **GIET** |
| `F01_gate_thieu_van_passed` | `c22_thieu_dinh_danh_khong_passed` | 0 → 3 | **GIET** |
| `F01_checkout_head_thieu` | `c22_thieu_dinh_danh_khong_passed` | 0 → 3 | **GIET** |
| `F02_search_thay_match` | `c23_chi_loi_goi_that` | 0 → 3 | **GIET** |
| `A14_kich_ban_tu_dong_mau` | `c25_f02_env_mang_mau` | 0 → 3 | **GIET** |
| `A15_khoi_la_tap_con` | `c26_f02_dong_khong_mau` | 0 → 3 | **GIET** |
| `A16_bo_luat_toan_khoi` | `c27_f02_yaml_khong_toi_gian` | 0 → 3 | **GIET** |
| `A16_bo_khop_nguyen_van` | `c25_f02_env_mang_mau` | 0 → 3 | **GIET** |
| `A17i_cho_env_buoc` | `c28_che_do_env_buoc` | 0 → 3 | **GIET** |
| `A17ii_bo_env_job` | `c29_che_do_env_job` | 0 → 3 | **GIET** |
| `A17iii_cho_doi_so` | `c30_che_do_doi_so` | 0 → 3 | **GIET** |
| `che_do_bo_tien_to_VAR` | `c31_che_do_duong_khac` | 0 → 3 | **GIET** |
| `che_do_bo_env_workflow` | `c31_che_do_duong_khac` | 0 → 3 | **GIET** |
| `che_do_bo_defaults_workflow` | `c31_che_do_duong_khac` | 0 → 3 | **GIET** |
| `che_do_bo_job_goi_lai` | `c31_che_do_duong_khac` | 0 → 3 | **GIET** |
| `che_do_bo_defaults_job` | `c31_che_do_duong_khac` | 0 → 3 | **GIET** |
| `che_do_moi_shell` | `c31_che_do_duong_khac` | 0 → 3 | **GIET** |
| `che_do_bo_GITHUB_ENV` | `c31_che_do_duong_khac` | 0 → 3 | **GIET** |
| `F08_git_bo_sha` | `c34_git_blob_that` | 0 → 3 | **GIET** |
| `F08_git_luon_vang` | `c34_git_blob_that` | 0 → 3 | **GIET** |
| `F02_bo_doi_dong` | `c35_f02_khoi_khong_tron_ven` | 0 → 3 | **GIET** |
| `F02_bo_doi_shell` | `c35_f02_khoi_khong_tron_ven` | 0 → 3 | **GIET** |
| `F02_cho_mau_sau` | `c35_f02_khoi_khong_tron_ven` | 0 → 3 | **GIET** |
| `F02_bo_het_tien_to` | `c35_f02_khoi_khong_tron_ven` | 0 → 3 | **GIET** |
| `F02_bo_doi_header` | `c35_f02_khoi_khong_tron_ven` | 0 → 3 | **GIET** |
| `A18_head_sha_thay_sha_checkout` | `c32_workflow_khong_doc_duoc` | 0 → 3 | **GIET** |
| `A18_yaml_hong_nem` | `c32_workflow_khong_doc_duoc` | 0 → 3 | **GIET** |
| `A19_lay_ung_vien_dau` | `c33_nhieu_ung_vien` | 0 → 3 | **GIET** |
| `F01_steps_chi_la_list` | `c22_thieu_dinh_danh_khong_passed` | 0 → 3 | **GIET** |
| `F05_chieu_khong_an_toan` | `c22_thieu_dinh_danh_khong_passed` | 0 → 3 | **GIET** |
| `F05_luoi_cuoi` | `c19_rest_loi` | 0 → 3 | **GIET** |
| `F02_khong_noi_dong` | `c23_chi_loi_goi_that` | 0 → 3 | **GIET** |
| `F02_cho_moi_co` | `c23_chi_loi_goi_that` | 0 → 3 | **GIET** |
| `F01_bool_la_int` | `c22_thieu_dinh_danh_khong_passed` | 0 → 3 | **GIET** |
| `F01_chuoi_rong` | `c22_thieu_dinh_danh_khong_passed` | 0 → 3 | **GIET** |
| `F01_conclusion_bat_ky` | `c22_thieu_dinh_danh_khong_passed` | 0 → 3 | **GIET** |
| `F01_labels_rong` | `c22_thieu_dinh_danh_khong_passed` | 0 → 3 | **GIET** |
| `F01_check_run_bat_ky` | `c22_thieu_dinh_danh_khong_passed` | 0 → 3 | **GIET** |
| `F01_head_sha_bat_ky` | `c22_thieu_dinh_danh_khong_passed` | 0 → 3 | **GIET** |
| `F01_head_sha_nhan_newline` | `c22_thieu_dinh_danh_khong_passed` | 0 → 3 | **GIET** |
| `F01_check_run_nhan_newline` | `c22_thieu_dinh_danh_khong_passed` | 0 → 3 | **GIET** |
| `F01_artifact_khong_kiem` | `c22_thieu_dinh_danh_khong_passed` | 0 → 3 | **GIET** |
| `F01_phong_bi_khong_kiem` | `c22_thieu_dinh_danh_khong_passed` | 0 → 3 | **GIET** |
| `F03_bo_kiem_total_doi` | `c20_du_trang` | 0 → 3 | **GIET** |
| `F05_than_run_sai_dang` | `c19_rest_loi` | 0 → 3 | **GIET** |
| `F05_loi_ghi_mat_dong_dem` | `c19_rest_loi` | 0 → 3 | **GIET** |
| `F05_sai_doi_so_mat_dong_dem` | `c01_cli_du_co` | 0 → 3 | **GIET** |
| `F05_rest_mat_dong_dem` | `c19_rest_loi` | 0 → 3 | **GIET** |
| `F06_redirect_lot_loi` | `c24_goi_that_loi_va_chuyen_huong` | 0 → 3 | **GIET** |
| `F06_redirect_mang_token` | `c24_goi_that_loi_va_chuyen_huong` | 0 → 3 | **GIET** |
| `vo_can_AttributeError_qua_except_doi_kieu` | `c03_checkout_linux` | 0 → 4 | **TIN_DUNG_GIA** |
| `chi_them_chu_thich` | `c20_du_trang` | 0 → 0 | **SONG_SOT** |
| `git_ignore_sha` (alias F08_git_bo_sha, chạy mọi ca) | `c34_git_blob_that` | 0 → 3;34 ca khác rc0 | **GIET** |
| `git_always_unavailable` (alias F08_git_luon_vang, chạy mọi ca) | `c34_git_blob_that` | 0 → 3;34 ca khác rc0 | **GIET** |

**Sổ lệnh chính và receipt.** Các lệnh dưới được gọi qua wrapper đã mô tả, với bytecode tắt/cache/tmp trong `.review/`. Tên receipt là `.review/<nhãn>.receipt.json`; stdout/stderr nguyên văn cùng tiền tố. Các probe rc0 vẫn phải đọc kết quả con trong JSON; phản chứng rc3 là lỗi assertion đặc tả chủ đích, không phải setup.

| nhãn | command con | rc thật / bằng chứng dương |
|---|---|---|
| suite | `python -B ops/ci_provenance_test.py` |0;CA35/35,DOT BIEN74/74,TU KIEM2,TONG DAT|
| mutants | `python -B .review/audit_mutants.py` |0;76 mục phân hạng,74GIET/1tín dụng giả/1sống chủ ý|
| extra-mutants | `python -B .review/extra_mutants.py` |0 driver; mỗi mutant34/35 xanh, c34rc3 đúng chốt; classified.json ghi GIET|
| review-cases | `python -B .review/run_review_cases.py` |0 driver; sáu ca gốc rc0,hai mutant Git rc3 đúng ca reviewer|
| r4-comparison | `python -B .review/r4_compare.py` |0;hai r4r2passed→r3not_measured,tám collision not_measured|
| probes | `python -B .review/probes.py` |0;85 nhóm đo,không exception thoát|
| structure | `python -B .review-input/do_cau_truc.py` |0;37tệp/226nhóm màu/226hop_le|
| new-probes-final | `python -B .review/new_probes.py` |0;matrix biên/composite và thống kê bổ sung ở new-probes.json|
| composite-final | `python -B .review/composite_case.py` |3;DO:F02_composite_origin_collision do TinHieuChotCa; shell0/tool0/marker passed sai|
| composite-parent-final | `python -B .review/composite_case.py`, `CI_PROVENANCE_MA=.review/parent-source.py` |3;cùng phản chứng trên29d641c; source/hash riêng ở composite-parent-case.json|
| boundary | `python -B .review/boundary_case.py` |3;DO:F02_nested_incomplete_echo do TinHieuChotCa|
| classifier-negative | `python -B .review/classifier_negative.py` |0 driver;main1,DOT BIEN0/1,TIN_DUNG_GIA,TONG DO|
| registry | `python -B .claude/dev/ci_dang_ky_test.py --chay` |1;ĐĂNG KÝ25/25,RUFF CI3/3 rồi fixture git128;A9 chưa đo trọn|
| readback2 | `python -B .review/readback2.py` |0;hai provenance trùng byte,37/37log khớp;probe registry/regex và stderr signer được lưu|
| doctrine | `python -B .claude/dev/packet_loop.py doctrine-scan --root .` |0;10tệp/0chép|
| adr | `python -B .claude/dev/packet_loop.py adr-song --root .` |0;53/53khớp1–1|
| lint | `python -B -m ruff check --no-cache --select F ops/ci_provenance.py ops/ci_provenance_test.py` |0;All checks passed;bare lint riêng pin/probe contract|

**Giới hạn bàn giao và stop condition.** A9 full command chưa qua vì môi trường signer; A10LIVE độc lập, A12/A13, lease/ref freshness, CI/required checks exact candidate, native Windows/pwsh, runner composite thật, mạng/redirect thật và receipt vận chuyển cuối **KHÔNG ĐO ĐƯỢC**. Full runtime/release gates **not_run**. Fixture skipped/not_run giữ nguyên trạng thái, không dùng làm pass. Kết luận nội dung **changes_requested**, F08 đóng nhưng F02 lặp lượt2r3; **DỪNG HẲN theo V5**, bàn giao chủ kho, không tự vá/mở vòng tiếp.

**Snapshot cuối.** snapshot-start.json/snapshot-end.json/snapshot-comparison.json so hash/size **5,686 tệp** ngoài `.git/` và `.review/`, gồm ignored/untracked, `.review-input/` và `.codex/`: **0 delta**. HEAD/tree giữ exact OID đầu verdict; Git status không ignored, diff, cached diff và untracked không ignored rỗng, rc0. Raw danh sách ignored thay đổi do hiện vật được tạo trong `.review/`; sau loại đúng prefix output này, các kết quả Git đầu/cuối bằng nhau. Ignored ngoài output vẫn là `.codex/` và `.review-input/`, không có delta nội dung. `.git/` không băm toàn metadata, kiểm qua HEAD/tree/index/diff/status. Hai snapshot chỉ chứng minh không có delta quan sát tại hai mốc, không chứng minh lịch sử chưa từng ghi rồi hoàn nguyên. Không có repository nguồn bên ngoài được cấp/quan sát.
