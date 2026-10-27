Verdict: approve
Reviewed commit: e05ea6a11eb689e1cebb11b417a56930cec8f11e
Spec sha256: adaf8d2469ac16c46314c3c9ac7667cce90825a053a7b98e12b803c6719040c3; Chung sha256: 4e3d1e1b3f6a0b60b96ad7b70f0ece97eca4bb3d6d10defeab1cd24ac6d1cbf0

Trạng thái: đã hoàn tất review độc lập, offline, lượt 1; không còn finding P0/P1/P2/P3 trong phạm vi packet.

Packet #977 / revision 1 / generation 1 / lượt 1. Vai trò reviewer độc lập, offline; chỉ ghi dưới `out/`.

Đã xác minh hai băm đặc tả khớp. Candidate tree: `c4343b2c2456d0668fa74380a049c037a75541b2`.
Base `09db70350414d767b793a71cb630e643f216a1b1` là parent trực tiếp của candidate; origin/master cục bộ trỏ base.
Clone thường, không shallow, worktree sạch. Diff đúng `docs/PROTOCOL_DA_PHIEN.md`, 19 dòng thêm / 2 dòng xóa, chỉ §4 và §12.

Reviewer: Codex, họ model `openai`, provider `openai_codex`, execution surface `codex_cli`, transport `machine`; run `c126d6eebc3c4e9e8515750e9da340b0`. Provider/surface/transport có trong `runs/c126d6ee/run.json`; tệp đó không ghi canonical model/effort nên không tự khai hai giá trị ấy. Executor theo lease là Claude, họ `claude`; review class `sensitive`, assurance target `cross_approved`. Hai trục review: Spec và Standards/Security. Không dùng context executor, không gọi mạng/GitHub, không thay đổi packet.

Lease bản chép khớp packet/revision/generation/spec hash và phân vai. Lease cho phép handoff trên nhánh lease riêng; diff code ứng viên thực tế chỉ có một tệp protocol như prompt yêu cầu. `origin/master` ở đây là ref trong snapshot offline, không phải lời khai đã đọc lại remote thật.

**Bảng lớp finding**

| slug | hạng P0–P3 | biểu hiện file:dòng | phép đo/tái hiện đã chạy | hướng vá |
|---|---|---|---|---|
| — (không có lớp finding mở) | — | — | Các phép nghiệm thu và probe liệt kê dưới đây đều đạt | Không yêu cầu vá |

Đếm theo nguyên nhân: **P0=0, P1=0, P2=0, P3=0; 0 biểu hiện lỗi**. Áp đúng ngưỡng của prompt: chỉ lỗi nghĩa thật, luật chưa được mã cưỡng chế, mâu thuẫn protocol, phản chứng cũ còn sống hoặc thiếu mục bắt buộc mới lên P2+. Không phát hiện những tình huống đó. Đây là lượt 1, không có finding lượt trước để đối chiếu. Các probe đầu vào âm bị từ chối đúng là bằng chứng đạt, không phải finding. Không dựng đột biến mã mới hay phát hiện đột biến độ phủ mới sống sót, nên không phát sinh nợ P3 theo luật riêng của lượt này.

**Đối chiếu từng mệnh đề**

Các đường dẫn/dòng sau đều thuộc `src/` tại reviewed commit. Viết tắt `P` = `docs/PROTOCOL_DA_PHIEN.md`, `L` = `.claude/dev/packet_loop.py`.

| Mệnh đề mới / vị trí protocol | Neo mã (file:dòng) | Kết luận |
|---|---|---|
| Chỉ packet áp ADR-0054 có `mo-lai` (P:248) | L:2959; chế độ được ghi ở L:2673–2675 | Khớp: cờ phải là `True`. |
| Mở `approved_pending` trên SHA đang chờ (P:248) | L:2959–2965 | Khớp: lấy `pending_sha`, đưa vào kiểm biên nhận. |
| Hai nguyên nhân `ci-do` và `connector` (P:249–252) | L:2938; L:2955; L:2985–2986; parser L:3275 trở đi | Khớp miền nguyên nhân và hai đích. |
| Mỗi lớp có tham chiếu không rỗng, đúng dạng, không lặp (P:249) | L:2966–2972 | Khớp; kiểm trùng trên toàn tập refs, không chỉ trong từng lớp. |
| `ci-do` neo cặp `[workflow, job]` (P:249–250) | L:2967–2968; L:2983 | Khớp; hai chuỗi không trắng, dùng chính các cặp ấy để kiểm CI. |
| `ci-do` đưa về `running` (P:250) | L:2985; L:2991–2992 | Khớp, trừ điều kiện dừng được nêu ngay trong đoạn ở P:261–262. |
| Đỏ thật chỉ `failure`, `timed_out`, `startup_failure` (P:250–251) | L:2938; L:2983; L:2863; L:2872; L:2880 | Khớp: run, job và check-run phải hoàn tất, có kết luận thuộc tập đỏ. |
| Attempt mới nhất của run mới nhất (P:251) | L:2857–2880 | Khớp: run ID lớn nhất trong đúng workflow/kho/head, dùng `run_attempt`, bác job có attempt mới hơn; job/check-run cũng được chọn/đối chiếu đúng suite và app `github-actions`. |
| `ci-do` đòi connector không còn P0–P2 trên head; nếu có dùng `connector` (P:251–252) | L:2974–2978; L:2808–2835 | Khớp. `mo-lai` không đòi connector đã hoàn tất; văn bản cũng không thêm điều kiện đó. |
| Mỗi lớp `connector` phải P0–P2 (P:252) | L:2393; L:2970–2972 | Khớp. |
| Refs phủ bằng đúng tập P0–P2 của connector trên head (P:252) | L:2974–2976; L:2808–2833 | Khớp: so cặp `(endpoint, id)`, ba endpoint, đúng kho/PR/head; không chỉ so số lượng. |
| `connector` đưa vào `cho_chu_kho` (P:252–253) | L:2985–2992 | Khớp, chịu điều kiện dừng như nêu ở cuối đoạn. |
| Cũng mở từ `running` khi quyền hiện hành là `ci-do`, cùng generation (P:253) | L:2955–2959 | Khớp. |
| Chưa có `begin_attempt` sau sự kiện `mo_lai` cuối (P:253–254) | L:2956–2958 | Khớp: duyệt đoạn history tính từ sự kiện cuối cùng. |
| Xét trên chính SHA đã mở lại (P:254) | L:2962; L:2965; L:2974; L:2736–2738 | Khớp: chọn `mo_lai_tu.sha` rồi neo biên nhận/readback vào SHA ấy. Không có phép so HEAD hiện tại/đầu nhánh remote ở cửa này; câu không khẳng định có phép so ấy. |
| Mỗi lần mở lại thay quyền `mo_lai_tu` gồm nguyên nhân/generation/SHA (P:254–255) | L:2985–2989; L:2943–2946 | Khớp: ghi mới cả object, không cộng thêm nhiều quyền song song. |
| Cộng một same-failure cho mỗi slug từ biên nhận (P:255) | L:2727–2728; L:2748–2750; L:2984–2988; L:672–673 | Khớp: slug duy nhất, CLI finding IDs khớp bảng lớp, bộ đếm được kiểm lại từ review và sự kiện `mo_lai`. |
| `cho_chu_kho` không có cạnh `transition` (P:256) | L:212–222; L:715–722; L:1248–1259 | Khớp; kiểm động cả các đích hợp lệ trong bảng lẫn `landed`. |
| Chỉ rời `cho_chu_kho` qua `chu-kho-duyet` (P:256) | L:3003–3005; L:3034–3037; bảng mọi cửa bên dưới | Khớp trên luồng state hợp lệ. Cửa này có thể về `blocked` khi chạm trần, đúng ngoại lệ P:261–262. |
| Checkpoint trong `ops/checkpoints/<tên>.yaml`, đọc `origin/master` sau fetch và so `ls-remote` (P:257) | L:3006–3015 | Khớp: kiểm vị trí/đuôi, fetch ref master, so OID remote với local, đọc blob bằng OID vừa xác minh. |
| Checkpoint đúng lược đồ (P:257) | L:2940; L:3016–3022 | Khớp: đúng tập bảy khóa, kiểu chính xác, phạm vi không rỗng và thuộc miền đóng. |
| Do người có thẩm quyền quyết (P:258) | L:156; L:3028; L:3010–3015 | Khớp mô hình chứng cứ của đặc tả: tên trong allowlist và hiện vật trên master đã fetch. Không suy thêm phép xác thực danh tính live ngoài mã. |
| Khớp packet, generation, spec_hash, head (P:258) | L:3024–3028 | Khớp cả bốn trường; head là SHA nguồn cho quyền vá, `pending_sha` cho quyền đẩy. |
| Phạm vi `cho_phep_va` đưa về running và tiêu thụ `mo_lai_tu` (P:258–259) | L:3003; L:3024; L:3029; L:3034 | Khớp: `state=running`, `mo_lai_tu=None`; không khẳng định lệnh checkout/sửa Git HEAD. |
| `cho_phep_day` là quyền riêng tại `approved_pending`, head=pending_sha, ghi `checkpoint_day`, giữ state (P:259–260) | L:3003–3005; L:3024; L:3033–3036 | Khớp trên đường thành công; điều kiện dừng ở P:261–262 vẫn áp dụng. Quyền và event được ghi, chưa chuyển sang `accepted`. |
| Chưa có cửa tiêu thụ quyền đẩy; dành cho #816 (P:260–261) | L:681; L:2938; L:2943–2946; L:3035; quét toàn bộ tệp và các tệp Python/shell/PowerShell trong kho (`checkpoint-consumers.txt`) | Khớp: hiện chỉ kiểm hình dạng và ghi/thay quyền; không có nhánh xóa/tiêu thụ `checkpoint_day`. #816 là phạm vi kế tiếp, không phải tuyên bố đã triển khai. |
| Mỗi cặp hiện vật/phạm vi dùng một lần (P:261) | L:3023; L:3030; L:3033 | Khớp: khóa là SHA-256 bytes hiện vật + phạm vi, không phải tên đường dẫn. Cùng hiện vật có hai phạm vi được dùng một lần cho mỗi phạm vi. |
| Ba cửa cùng qua hàm xét dừng (P:261–262) | L:2939; L:1034; L:2991; L:3036; L:3053–3060 | Khớp chính xác tập `CUA_DI_TIEP`: không bỏ sót/thêm cửa. `accept`/`record-lease`/`record-review` cũng gọi `_xet_dung`, nhưng không thuộc tập kiểm same-failure sẵn có theo nhánh này; câu không nói chỉ ba cửa mới gọi hàm. |
| Chạm trần same-failure: ghi sổ rồi blocked (P:262) | L:2988–2991; L:3033–3036; L:3053–3060 | Khớp: `mo-lai`/`chu-kho-duyet` giữ event đã dựng rồi thêm `blocked_same_failure`, lưu và rc=3. `begin-attempt` lưu event dừng trước khi tăng attempt. |
| Packet chưa áp ADR-0054 không có các state/cửa mới này (P:262–263) | L:678–682; L:982; L:1231–1234; L:2959; L:3004 | Khớp đối với `approved_pending`, `cho_chu_kho`, `mo-lai`, `chu-kho-duyet`; không thay đường cũ của `running`/`begin-attempt`. |
| Mission chưa complete khi còn `approved_pending`/`cho_chu_kho` (P:1158–1159) | L:212–214; L:2904–2933; L:2949–3039; P:1038–1042; P:1085–1086; P:1235–1239 | Khớp: đây là hai state chưa hoàn tất. Câu là nghĩa vụ Mission, không tuyên bố `packet_loop.py` đã có lệnh/cổng Mission-complete. Hai trạng thái mới bổ sung đồ thị tổng quát §4, không đổi điều kiện landed/complete tại §10.2/§13. |

Đoạn bổ sung nằm ngay sau đoạn `approved_pending`, là một đoạn văn xuôi, không bảng; giữ giới hạn 40 dòng. M1 và M2 có đủ. §12:1127–1128 và §20:1550 vẫn nói ADR-0054 chưa kích hoạt; packet này không kích hoạt ADR ấy. Câu land thất bại về `paused` hoặc sinh packet sửa lỗi là nội dung giữ nguyên từ base.

**Rà mọi cửa ghi state**

Quét `_save`, các phép gán `state`, `state=`, và dictionary `state` trong toàn bộ `packet_loop.py`; kết quả giữ ở `state-writers.txt`. Không chỉ dựa vào chú thích của `CHUYEN_HOP_LE`.

| Cửa / neo mã | Khi ở `cho_chu_kho` hoặc `approved_pending` |
|---|---|
| `init`, L:781–793 | Không ghi đè state có sẵn. |
| `record-lease`, L:955–968; `_record_lease_ref`, L:2674 | Đòi `awaiting_lease` trước khi gọi đường ref; không reset hai state này. |
| `begin-attempt`, L:992–996 | Chỉ nhận `leased`/`running`. |
| `void-attempt`, L:1055–1065, L:1097–1102 | Hai state đạt từ review/mo-lai đều đã đóng attempt. Hơn nữa, phép gán state duy nhất của void chỉ chạy khi state là `reviewing`. |
| `record-review`, L:1133–1136 | Đòi `reviewing` trước mọi kết quả/dừng của review. |
| `record-codex-call` / `_vao_rescue`, L:1292–1303, L:696–701 | Đòi `reviewing` trước khi có thể ghi rescue; không đưa hai state này về blocked từ cửa này. |
| `transition`, L:1248–1259 | Bảng hai state đều không có cạnh ra; đích review-only cũng bị chặn. |
| `record-rescue`, L:1325–1336 | Chỉ từ `blocked` vì `rescue_required`. |
| `nang-tran`, L:1311–1321; `record-post`, L:1344–1356 | Có thể ghi metadata/bộ đếm/sổ comment, nhưng giữ nguyên trường state. Probe dương xác nhận cả hai. |
| `accept`, L:2907–2933 | Chỉ nhận `approved_pending`, đo remote head/CI/connector/P3 rồi vào `accepted`; từ `cho_chu_kho` bị chặn. |
| `mo-lai`, L:2954–2992 | Nhận `approved_pending` hoặc `running` thỏa điều kiện; không nhận `cho_chu_kho`. |
| `chu-kho-duyet`, L:3002–3038 | Cửa duy nhất rời `cho_chu_kho`: về running sau checkpoint vá, hoặc blocked khi điều kiện dừng thắng. Tại pending: ghi quyền đẩy, có thể blocked theo cùng hàm dừng. |
| `_load`, L:646–689 | Chỉ đọc/kiểm schema; bất biến `mo-lai` cấm `cho_chu_kho` thiếu cờ ADR/quyền connector. Không tự lưu state. |

**Bằng chứng nghiệm thu và probe**

Môi trường đo: Linux, Python 3.13.17, Git 2.43.0. Biểu thức E2 nguyên văn: `approved_pending.*cho_chu_kho|cho_chu_kho.*approved_pending`.

Toàn bộ command/working directory/rc/stdout/stderr cho nghiệm thu nằm trong `acceptance.jsonl`, bản dễ đọc ở `acceptance.log`. Các lệnh đọc nguồn dùng `PYTHONDONTWRITEBYTECODE=1`, `GIT_OPTIONAL_LOCKS=0`; Git global/system cô lập về `/dev/null`. Bản sao là clone thường tại `out/review-copy/`, ghim exact candidate và `core.abbrev=7`. Fixture, state và TMPDIR đều dưới `out/`; Git fixture chỉ dùng remote file cục bộ, `GIT_ALLOW_PROTOCOL=file`.

| Lệnh / phép đo | rc | Bằng chứng dương / kết quả |
|---|---|---|
| `sha256sum tham-chieu/wp977.md src/ops/specs/may-adr-0054-chung.md` | 0 | Hai băm đầy đủ khớp dòng 3, kiểm lại cuối review vẫn khớp. |
| `git -C src rev-parse HEAD HEAD^{tree} refs/remotes/origin/master` | 0 | Head/tree/base đúng các OID đã ghi. |
| `git -C src symbolic-ref -q HEAD` | 1 (mong đợi) | Detached HEAD; `.git` là thư mục. |
| `git -C src rev-parse --is-shallow-repository` | 0 | `false`. |
| `git -C src merge-base --is-ancestor 09db70350414d767b793a71cb630e643f216a1b1 e05ea6a11eb689e1cebb11b417a56930cec8f11e` | 0 | Base là tổ tiên. `git merge-base` riêng trả đúng base. |
| `git -C src diff --numstat <base> <head>` | 0 | `19 2 docs/PROTOCOL_DA_PHIEN.md`; đúng một tệp, 19 ≤ 40. |
| `git -C src diff <base> <head>`; `git -C src diff --check <base> <head>` | 0 / 0 | Hai hunk §4 và §12; không lỗi whitespace; `candidate.diff`. |
| `rg -n 'cho_chu_kho' docs/PROTOCOL_DA_PHIEN.md` (cwd SRC) | 0 | Khớp dòng 253, 256, 1158; có §4. |
| `rg -n <E2> docs/PROTOCOL_DA_PHIEN.md` | 0 | Khớp đúng câu §12, dòng 1158. |
| `rg -n 'chu-kho-duyet' docs/PROTOCOL_DA_PHIEN.md` | 0 | Khớp dòng 256, 259, 261. |
| `git show 09db70350414d767b793a71cb630e643f216a1b1:docs/PROTOCOL_DA_PHIEN.md`, rồi đưa bytes vào từng `rg -n <ba biểu thức trên>` | 0 cho show; 1/1/1 cho rg (mong đợi) | Cả ba stdout rỗng trên base; bytes lưu `base-protocol.md`. Ghi riêng rc để không mất lỗi pipeline. |
| `python .claude/dev/packet_loop.py doctrine-scan --root .` | 0 trên SRC và 0 trên copy | `sạch — đã quét 10 tệp, 0 chỗ chép doctrine`. |
| `python .claude/dev/packet_loop.py adr-song --root .` | 0 trên SRC và 0 trên copy | `55 ADR trên đĩa, 55 dòng trong §20, khớp 1–1`; ngoại lệ trạng thái sẵn có `0016` được scanner khai rõ. |
| `PYTHONDONTWRITEBYTECODE=1 python out/run_selected.py` | 0 | **48/48 đạt**, không skip: 5 ca đọc protocol trực tiếp + 43 ca `r813_*` có fixture đọc protocol thật tại `packet_loop_test.py:7677`. Chi tiết `selected-tests.log`, `selected-results.json`. |
| `PYTHONDONTWRITEBYTECODE=1 python out/probe_state_exits.py` | 0 | **38/38 đạt**: ở mỗi state, status dương + 9 đích transition + 7 cửa khác bị chặn + 2 cửa metadata dương. 32 ca âm đều rc=8 và băm state trước/sau khớp; 6 ca dương rc=0. |
| `PYTHONDONTWRITEBYTECODE=1 python out/probe_semantics.py` | 0 | **6/6 bước đạt**; năm bước rc=0, replay cùng cặp rc=7 với lý do `['da_dung']` và state nguyên byte. |
| `PYTHONDONTWRITEBYTECODE=1 python out/audit.py finish` | 0 | 7.307 mục tệp trước/sau, **0 delta** nội dung; head/tree không đổi, status gồm untracked/ignored rỗng. `source-integrity.json`, `src-before.json`, `src-after.json`. |

Phép thử state dùng baseline được tạo qua CLI thật (`init`/lease/review có receipt hợp lệ), rồi `mo-lai connector` thật; các snapshot của baseline chỉ được sao chép sang thư mục riêng cho từng probe. Không giả kết quả `_load`, không thay mã sản phẩm. Lần chạy đầu của script probe do reviewer viết truyền thiếu cờ `record-lease`, nên dừng ở rc=2 trước chốt state: đó là lỗi fixture, không tính là bằng chứng chặn state và không xếp finding. Đã giữ log `state-exit-probes-initial.log`/JSON, bổ sung đủ bốn cờ từ lease và chạy lại đủ 38 ca; bản cuối mới là evidence trong bảng.

Probe SHA tạo HEAD cục bộ khác SHA đã mở lại, không gọi `begin-attempt`; `mo-lai connector` vẫn rc=0 và giữ đúng SHA nguồn trong quyền. Điều đó xác nhận cách hiểu P:254: neo bằng chứng vào SHA đã mở lại, không hứa kiểm HEAD hiện tại. Probe checkpoint dùng một hiện vật có cả hai phạm vi: dùng `cho_phep_day` lần đầu đạt, dùng lại cùng cặp bị chặn, sau connector dùng chính hiện vật đó cho `cho_phep_va` đạt. Lúc kết thúc, `mo_lai_tu=None` còn `checkpoint_day` vẫn tồn tại. Kết quả/băm/state cụ thể ở `semantic-results.json`.

Suite đầy đủ `python .claude/dev/packet_loop_test.py`: **not_run bởi reviewer**, theo ngoại lệ nêu rõ trong prompt (45–60 phút, executor đã chạy trên exact head theo hồ sơ giao việc). Không tự nhận đã tái xác minh N/N của full suite hay mutation matrix. 48/48 ở đây chỉ là tập chọn lọc; không thay thế evidence CI/land. Những hướng thử đòi tự dựng đường dẫn thoát cây không được tạo. Snapshot nội dung đầu/cuối chứng minh không có delta quan sát được, không phải bằng chứng về toàn bộ lịch sử thao tác.

Kết luận này chỉ neo commit `e05ea6a11eb689e1cebb11b417a56930cec8f11e`; không cấp quyền push, merge hay land, không kích hoạt ADR-0054. Việc xác nhận provenance/receipt vận chuyển và hoàn tất CI/land thuộc quy trình tiếp theo.

