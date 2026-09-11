verdict: changes_requested
reviewed_sha: d5a980e9a214992c38112e603de6724728857be2
reviewed_tree: 9534d4903a4e4156611a15f9d70922c9e9c820df
reviewed_base: c0a5cbe89a90588115262e1a2c3ac84cbd98be9e
reviewed_spec_sha256: 465538364b1a3f9477782fba79869bbd1c9351140e3fa9df50451baae22f9c79
reviewed_adr0047_sha256: b9975929c52e12767417b46b47829c265230117fe65df6a9fd22540d4868fdab
model_tu_khai: GPT-6 (Codex, theo cấu hình phiên; không có phép đo độc lập model ID/build chi tiết)
provider: openai
execution_surface: codex_agent_with_local_tools
transport: direct_local_tools
review_class: sensitive
lease: wp488-thu-hoi-lease-a0-exec-1-claude-20260909
review_round: 1
started_at_utc: 2026-09-09T16:31:22Z

**3 P1, 6 P2; chưa đủ điều kiện approve.** Đây là review MÃ ở chế độ CHƯA KÍCH HOẠT, không xét lại tính hợp lý của spec. Không có finding nào dựa vào việc profile production chưa được chủ kho duyệt hoặc chỉ vì chưa có canary mạng. Không phát hiện spec tự mâu thuẫn cần nâng thành finding. Các P2 dưới đây có phần mã/test executor sửa được trong ba đường của packet; duyệt manifest deployment và facts Actions thật vẫn cần nguồn độc lập.

`VERDICT.md` đã được tạo từ đầu lượt và bổ sung khi có phản chứng. Mọi bản sao, fixture, mutant và hint nằm trong `scratch/`; không sửa mã/ref/config của `cay-kho/`, không mạng. Các ca bytes lệch, replacement và config rewrite chỉ chạy từ t130/t129/t136 đã được cung cấp; không tự dựng helper/remote/config đổi nguồn thuộc lớp bị cấm. Ca tên entry chứa `/` dùng object được Git băm đúng OID, không traversal; tên tiếng Việt là tên bình thường, không đồng tự.

`HINT.patch` là **TEST thuần**, áp bằng `patch -p0` từ gốc `cay-kho/`. Theo protocol §8 của checkout sensitive, không sinh hunk production/workflow. Nhãn bắt buộc: **“chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm commit”**. Patch bổ sung các phản chứng đỏ, không phải bản sửa sản phẩm đã hoàn tất. 11 ca đích của hint đã chạy trên mã head ở bản sao, đều đỏ bằng `TinHieuChotCa`; dry-run áp patch đạt. Đặc biệt, executor phải thay các control Q13 giả trong t133 bằng policy/binding hợp lệ khi sửa F01; chỉ thêm test mới không đủ làm suite xanh.

## Findings

### F01 — P1 — M4 nhận metadata Q13 chưa được xác minh

- **Vị trí:** `ops/lease_publish.py:1550`, `:1555`; fixture củng cố hành vi sai ở `ops/lease_publish_test.py:4483`, `:4524`.
- **Hợp đồng:** SPEC Q3/Q13 dòng 226–240 và M1/M4 dòng 479–484: policy phải hợp lệ; metadata mới phải so descriptor, hash policy đầu tiên và `base_sha_before_add == S`, kể cả inactive. Không xác minh được ⇒ 12.
- **Phản chứng đã chạy:** `python3 scratch/review_harness.py`, ca `m4_bad_policy_metadata`: H thêm policy có bytes `not JSON` và metadata của fixture (hash `a…`/`b…`, base SHA không phải S). M4 **rc=0**, ghi `TAP_THU_HOI_RONG` và nhận marker. `m4_policy_no_marker` cũng nhận policy hỏng không marker với rc=0. Receipt lưu ở `scratch/m4_bad_policy_metadata.json` / `scratch/m4_policy_no_marker.json`. Hint t140 đỏ bằng `TinHieuChotCa`.
- **Nguyên nhân:** `kho.tim(...policy) is not None` chỉ chứng minh entry tồn tại, không đọc/băm/parse policy hay xác minh transition. `kiem_metadata_retired` chỉ kiểm định dạng từng trường. Không có phép so ba binding Q13. t133 đang coi `{}` + metadata băm hằng là positive control, nên suite xanh không chứng minh Q13.
- **Vá:** trong M4, sau append-only và trước nhận metadata, đi verifier Q13 trên bytes policy/schema đã băm; so các binding đúng transition. Thiếu nguồn/binding được duyệt phải 12. Kiểm cả trường hợp policy mới không marker. Giữ append-only trước validator để sửa/xoá marker cũ vẫn 8. Thay control t133 bằng fixture có verifier/binding hợp lệ, giữ ca âm t140.
- **Nguy cơ khi vá:** không so `first_policy_sha256` của marker cũ với mọi policy tương lai; không vô tình cấm B(P1,R1)→B2(P2 hợp lệ,R1). Không tự bịa descriptor production. P1 vì hiện tại admission nhận dữ liệu Q13 không hợp lệ ngay khi cờ False.

### F02 — P1 — Consumer bỏ sót namespace không rỗng

- **Vị trí:** `ops/lease_publish.py:1445`, `:1453`, `:1463`; ảnh hưởng `lenh_ai_dang_giu` và `check --du-bao`.
- **Phản chứng đã chạy:** fixture Git thông thường thêm `ops/thu-hoi/thu hồi.yaml` trên feature đã push về bare fixture. `_quet_so_thu_hoi_moi_ref` trả `[]`; `ai-dang-giu` có và không `--du-bao` đều **rc=0**, trong khi M4 trên cùng dạng tên trả 12. Tệp ASCII rác của t134 vẫn bị chặn 12. Một fixture khác có `ops/thu-hoi` là blob hoặc gitlink cũng cho `ai-dang-giu rc=0`. Xem `scratch/review-harness.log`, `scratch/extra-checks.log`; hint t141/t142 đỏ đúng assertion.
- **Nguyên nhân:** `ls-tree -r` không `-z` trả tên Unicode được Git quote; dispatcher nhận cả dấu quote nên không thấy tiền tố namespace. Entry chính `ops/thu-hoi` cũng rơi vào `None` và bị bỏ qua khi nó không phải tree.
- **Vá:** đọc tên Git dạng NUL-delimited/raw, xử lý đúng type của chính namespace và các parent cần đi qua. Hoặc dùng reader đã xác minh để liệt kê namespace; giữ tất cả entry không hiểu để trả 12. Không dùng unescape tuỳ tiện. Không đưa kiểm Git vào `check` mặc định.
- **Nguy cơ khi vá:** phải giữ stdout sản phẩm luật cũ, `DU_BAO:` riêng; tên Unicode hợp lệ ngoài sổ vẫn qua, sổ vắng thật vẫn qua. P1 là bỏ chốt fail-close “sổ không rỗng khi False ⇒ 12”, không phải đã áp hiệu lực thu hồi mới.

### F03 — P1 — Tree entry sai cấu trúc biến thành bằng chứng sổ vắng

- **Vị trí:** `ops/lease_publish.py:1373`, `:1379`, `:1418`, `:1428`.
- **Hợp đồng:** Q4.5/M4: chỉ được kết luận vắng từ chuỗi tree hợp lệ đã xác minh; entry không hiểu/source lỗi ⇒ 12.
- **Phản chứng đã chạy:** `python3 scratch/extra_checks.py`, ca `m4_slash_entry_name`. H là commit thật, parent S; tree `ops` chứa một entry tên literal `thu-hoi/x.yaml`. Objects được `hash-object --literally` băm trung thực, không bytes lệch OID, không đường thoát cây. M4 **rc=0**, map sổ T `{}` và sinh receipt (`scratch/m4_slash_tree_name.json`). Hint t143 đỏ bằng `TinHieuChotCa`.
- **Nguyên nhân:** `tree()` không kiểm tên entry có `/`, tên rỗng/nhập nhằng hay mode hợp lệ. `tim()` tìm component `thu-hoi`, không thấy tên literal có slash, rồi `namespace()` tin đó là absence. Việc hash đúng chỉ xác minh bytes, không xác minh cấu trúc Git tree.
- **Vá:** validate framing, mode và tên từng entry trước khi trả tree; tên chứa `/` phải 12, không normalize nó thành đường dẫn. Từ chối entry trùng/không hiểu; chuyển lỗi parse sang Chan(12).
- **Nguy cơ khi vá:** không loại tên tiếng Việt bình thường và mode Git hợp lệ; vẫn xử lý submodule/symlink đúng vị trí. Phản chứng là raw tree không hợp lệ, không khẳng định một working-tree checkout bình thường sẽ sinh tree này. Reader nhận cache không tin cậy nên không được cấp receipt xanh cho nó.

### F04 — P2 — Deadline chưa bao phủ memo và lúc hoàn tất đọc

- **Vị trí:** `ops/lease_publish.py:1295`, `:1301`, `:1325`, `:1351`.
- **Phản chứng đã chạy:** đọc blob hợp lệ vào memo, đổi clock tiêm từ 100 lên 102 với deadline 101; đọc lại vẫn **rc=0**. Ca riêng dùng cat-file thật, chỉ cho clock chạm 102 khi `poll`/`wait` báo hoàn tất: vẫn rc=0 và trả bytes. Xem `reader_expired_memo` trong `scratch/review-results.json`, `deadline_at_completion` trong `scratch/extra-results.json`; hint t144.
- **Vá:** kiểm deadline trước cache-hit và trước trả kết quả/receipt; ngân sách thời gian của read/join/wait dùng cùng thời gian còn lại, không dùng lại timeout đã tính trước spawn. Áp deadline cho preflight và traversal dùng memo nữa.
- **Nguy cơ khi vá:** giữ biên count/byte/depth inclusive; wall deadline có nghĩa khác biên count. Không tăng số object cho cache-hit. Xếp P2 vì phản chứng này vẫn chỉ trả bytes đã băm đúng, chưa chứng minh đổi thẩm quyền/thu hồi; đây là vi phạm giới hạn vận hành đã chốt.

### F05 — P2 — Nhánh object quá lớn không thu hồi subprocess; total budget kiểm sau cấp phát

- **Vị trí:** `ops/lease_publish.py:1314`, `:1317`, `:1325`, `:1339`.
- **Phản chứng đã chạy:** blob Git thật 1 MiB, `max_object_bytes=100`, deadline 0,3 s. Thread dừng ngay sau header, child bị nghẽn stdout; `p.wait()` ném **TimeoutExpired**, child **còn sống**. Harness đã kill/reap child sau khi ghi nhận. Với total budget 1 byte và blob 4 byte, reader vẫn gọi `read(5)` rồi mới 12. Ca trạng thái tiến trình riêng giữ nguyên bytes thật, đổi riêng trạng thái kết thúc thành rc=1: reader vẫn trả 0 vì không kiểm returncode. Xem `scratch/review-results.json` và `scratch/extra-results.json`; hint t145/t146.
- **Vá:** kiểm cả object/total budget từ header trước đọc body; khi từ chối header hoặc timeout phải kill/reap/đóng pipe trong finally, chuyển timeout/I/O/rc≠0 thành 12. Kiểm trạng thái child trước dùng kết quả. Không chờ child đang bị nghẽn khi đã quyết định không đọc body nữa.
- **Nguy cơ khi vá:** không cấp phát body để “drain cho xong” vượt budget; không làm t131 exact-bound đỏ; không bỏ kiểm hash/type vì đã kiểm framing. P2 vì ca lớn hiện thất bại đóng nhưng sai mã lỗi và rò tài nguyên; ca rc=1 vẫn dùng bytes đã được hash xác minh.

### F06 — P2 — Schema nhận float 1.0 và lỗi lịch thoát thành traceback

- **Vị trí:** `ops/lease_publish.py:1028`, `:1042`, `:1073`, `:1084`.
- **Phản chứng đã chạy:** `schema_version: 1.0` được cả parser revocation và metadata nhận **rc=0**; metadata float còn được M4 nhận. Ngày `2026-02-30T00:00:00Z` qua regex nhưng `fromisoformat` ném ValueError. CLI thực cho cả revocation/metadata **rc=1 + traceback**, thay vì 8/12. Xem `scratch/review-results.json`, `scratch/final-controls.json`; hint t147.
- **Vá:** kiểm `type(sv) is int` và `sv == 1`; parse datetime có xử lý ValueError và ánh xạ đúng 8 cho trường revocation, 12 cho metadata. Dùng một clock snapshot khi validate nhiều record. Giữ thứ tự cấu trúc/ID12 → thẩm quyền4 → nội dung8.
- **Nguy cơ khi vá:** không nhận bool qua quan hệ bool/int; không dùng parsing fallback để chấp nhận timestamp thiếu Z hoặc scalar YAML datetime. Float 1.0 không đổi ý nghĩa thẩm quyền ở inactive nên không nâng hạng riêng thành P1.

### F07 — P2 — M9 chưa đo actual workflow definition và receipt chưa đủ hợp đồng

- **Vị trí:** `.github/workflows/ops-thu-hoi-admission.yml:55`, `:72`, `:93`, `:102`; `ops/lease_publish.py:1570`; thiếu assertion tương ứng ở t137/t138.
- **Hợp đồng M9:** đo riêng `workflow_sha`/workflow_ref và checkout, cả hai neo S; receipt có actual definition commit + blob sha256, check_run_id, checker rc; upload action ghim commit được duyệt.
- **Đo đã chạy:** lấy nguyên Python bổ sung receipt trong workflow, chạy trên scratch checkout có tệp workflow tại S, đặt metadata workflow actual SHA khác S. Đoạn mã vẫn rc=0 và hash tệp checkout; không dùng actual SHA/ref. Đây là phép đo đoạn bổ sung receipt, **không giả nhận đã chạy Actions**. Đọc toàn thân workflow: không có phép so definition==S nào; chỉ so HEAD==base.sha. Receipt còn thiếu definition commit, `check_run_id`, `checker_rc`; `upload-artifact@v4` là tag, không commit pin. `scratch/extra-results.json: workflow_receipt_definition_drift`; hint t148.
- **Vá:** nhận actual workflow SHA/ref từ context nền tảng, xác minh path/repo/commit với S, lấy blob tại đúng definition commit và hash bytes ấy; drift/vắng bằng chứng ⇒12 trước receipt. Hoàn thiện các trường/joins theo schema consumer dependency; không bịa check_run_id từ job ID. Pin upload action bằng commit đã được duyệt, không tự chọn SHA chưa được readback.
- **Nguy cơ khi vá:** quan hệ run/head/workflow cho pull_request_target phải canary thật, không suy từ checkout. Job vẫn quyền đọc; không tự ghi platform conclusion success. Xếp P2 theo phạm vi inactive: chưa thấy chạy code ứng viên hay quyền ghi; không nâng thành P1 chỉ từ receipt sai trường. Mã đo/emit trường và test sửa được trong packet; actual API facts/commit được duyệt cần nguồn độc lập.

### F08 — P2 — Profile layer 2 chưa là manifest được duyệt, không có validator miền

- **Vị trí:** `ops/lease_publish.py:1124`, `:1130`, `:1161`, `:1176`; `ops/lease_publish_test.py:4666`.
- **Đọc hợp đồng:** ADR-0047 lớp 2/Q4.1 đòi identity image/runtime, HTTPS helper thật, runtime/library, toàn trust store/default store, nguồn secret/version và allowlist key/type/domain trước phép so digest.
- **Đo/đọc mã:** `hoso_adapter_do()` chỉ tạo Git path/hash/version + credential_helper rỗng, hai đường CA null, proxy và endpoint. Không có identity helper HTTPS, runtime/library, default trust store, producer/ownership bất biến. `bam_ho_so` băm đủ dict được truyền, nhưng dict thiếu những yếu tố quyết định hành vi ấy; cùng Git chính không chứng minh cùng nền TLS. `kham_pha_nguon` chỉ kiểm dict/git_path và digest, không finite schema/domain.
- **Phản chứng trong phân công:** đột biến bản sao chính ca profile âm t136: trường khác proxy được thay bằng khoá vô hại ngoài schema `truong_khong_ho_tro`, neo fixture bằng digest dict đó. Kết quả **rc=0**, assertion đợi12 đỏ bằng `TinHieuChotCa`. Không tự dựng helper/trust/source ác ý. `scratch/profile_probe.py`, `scratch/profile-probe.log`; hunk t136 trong hint.
- **Vá:** schema/validator hữu hạn cho manifest producer độc lập và config hiệu lực; thiếu identity bắt buộc phải12. So đúng một digest bao trùm manifest/config/source-secret identity, giữ domain validator riêng, không tạo chốt digest trùng che mutant. Không tự thêm neo production.
- **Nguy cơ khi vá:** profile hợp lệ trong fixture vẫn có positive control; biến thể trong miền khác approved phải chết tại đúng phép so, ngoài miền phải chết ở domain validator. P2 ở A0 vì `PROFILE_ADAPTER_DA_DUYET` vẫn rỗng, không có CLI/env đăng ký neo; chưa có đường production mở qua chốt này.

### F09 — P2 — Preflight source của KhoObject vẫn dùng Git/env caller

- **Vị trí:** `ops/lease_publish.py:1240`, `:1242`, qua `_git:282` → `GOI_GIT:73`.
- **CONTROL đã chạy:** không đặt biến Git đổi nguồn. Theo dõi subprocess trong lúc mở reader với kho Git bình thường: hai lệnh `['git','rev-parse',…]` đều có **env=None**, trước khi `_env_rong` được dùng cho cat-file. Hint t149 đỏ bằng `TinHieuChotCa`, log ghi chính argv/env thực.
- **Mô tả bằng lời, không dựng ca bị cấm:** ở hai lệnh này, `GIT_DIR`, `GIT_COMMON_DIR`, `GIT_OBJECT_DIRECTORY`, `GIT_ALTERNATE_OBJECT_DIRECTORIES`, `GIT_CONFIG_*`, HOME và PATH caller vẫn được kế thừa. Vì vậy việc chọn shallow/common object directory chưa ở cùng biên cô lập với reader. `_env_rong` tự nó sạch; việc sạch ở lời gọi sau không sửa nguồn đã chọn ở lời gọi trước.
- **Vá:** dùng Git executable tuyệt đối đã giải và env từ rỗng cho preflight nguồn; giải bare/working/linked worktree bằng API Git trong context source tường minh, không ghép `.git/objects`, không đưa repo tạm vào trước khi giải source. Không sửa rộng GOI_GIT của luật cũ nếu chưa đo tương tác.
- **Nguy cơ khi vá:** bare/linked worktree/pack/alternate đang qua phải tiếp tục qua; giữ `check` mặc định thuần. P2 vì reader sau đó vẫn hash từng OID; chưa chạy hay khẳng định khai thác đổi authority qua env. Hint chỉ dùng marker env vô hại để kiểm không kế thừa, không thay biến Git nhằm đổi nguồn.

## Mutant đã chạy

Lệnh: `TMPDIR="$PWD/scratch/tmp" PYTHONDONTWRITEBYTECODE=1 python3 scratch/mutant_runner.py`. Bảng được tạo từ kết quả chạy từng mutant; nguồn catalog lấy nguyên AST của t139 đã đóng băng. Mọi neo thay thế kiểm đúng một lần. Chi tiết message/exception/thời gian ở `scratch/mutant-results.json` và `scratch/mutants.log`.

| Mutant | Ca đích | Kết quả | Lớp ngoại lệ |
|---|---|---|---|
| S7-noi-allowlist-metadata | t128 | GIET | TinHieuChotCa |
| M1-noi-allowlist-thu-hoi-boi | t127 | GIET | TinHieuChotCa |
| M1-bo-chot-PROVIDERS-SONG | t127 | SONG | không ném |
| S2-bo-bam-lai | t130 | GIET | TinHieuChotCa |
| S2-bo-so-type | t129 | GIET | TinHieuChotCa |
| S8-bo-tran-parent | t131 | GIET | TinHieuChotCa |
| S8-bo-deadline | t131 | GIET | TinHieuChotCa |
| S8-bo-tran-tree-edges | t131 | GIET | TinHieuChotCa |
| shallow-bo-chot | t132 | GIET | TinHieuChotCa |
| M4-gan-luat-moi-som | t133 | GIET | TinHieuChotCa |
| M4-bo-append-only | t133 | GIET | TinHieuChotCa |
| M4-bo-policy-Q13 | t133 | GIET | TinHieuChotCa |
| M2-bo-chot-so-rong | t134 | GIET | TinHieuChotCa |
| M3-du-bao-doi-rc | t135 | GIET | TinHieuChotCa |
| A2-bo-so-profile | t136 | GIET | TinHieuChotCa |
| A2-fallback-symref | t136 | GIET | TinHieuChotCa |
| A6-bo-GIT_NO_REPLACE-SONG | t129 | SONG | không ném |
| S8-bo-unique | t131 | GIET — bổ sung | TinHieuChotCa |
| S8-bo-object-bytes | t131 | GIET — bổ sung | TinHieuChotCa |
| S8-bo-total-bytes | t131 | GIET — bổ sung | TinHieuChotCa |
| S8-bo-alternate-depth | t131 | GIET — bổ sung | TinHieuChotCa |
| S8-bo-alternate-count | t131 | GIET — bổ sung | TinHieuChotCa |
| A6-bo-routing | t129 | Không nhận công (ngoài catalog gốc) — bổ sung | Chan |
| A6-bo-flag-no-replace | t129 | SONG — bổ sung | không ném |
| A6-bo-memo-type | t129 | GIET — bổ sung | TinHieuChotCa |
| A6-bo-ca-hai-no-replace | t129 | SONG — bổ sung | không ném |

**Đối chiếu catalog gốc:** đúng **17 = 15 GIẾT + 2 SỐNG**, không ca nào bị đổi thành sống và không ngoại lệ vô can nào được tính trong 15. Mutant deadline chết ở assertion đòi “trước spawn”; lớp join-timeout còn chặn bằng12 nhưng không qua được assertion đó. Mutant bỏ memo-type bổ sung cũng chết ở assertion thông điệp “hai type”; chốt actual type còn chặn12 — không nhận đây là bằng chứng bỏ tất cả kiểm type.

Bỏ riêng env no-replace vẫn có cả flag và repo tạm che. Đã chạy thêm bỏ riêng flag và **bỏ cả env + flag**, cùng fixture refs/replace t129 đã cung cấp: vẫn SỐNG. Điều này xác nhận repo tạm không ref đủ che như catalog ghi; không có finding giả về no-replace.

**Ngoài catalog:** 9 mutant bổ sung = 6 đỏ bằng `TinHieuChotCa`, 2 sống, 1 chết `Chan` không nhận công. Mutant bỏ routing làm positive control t129 ném Chan(12, missing) trước `chot`; đây là đúng tác động của việc mất routing, nhưng theo quy tắc lớp ngoại lệ của t139 thì chưa đủ điều kiện nhận công. Catalog gốc không hề khai mutant này trong 15, nên không nói con số 15 của EVIDENCE là sai. Executor nên bọc positive bằng `_ma_chan` + chốt rc0 rồi bổ sung mutant routing vào catalog A6.

**Đột biến test/fixture riêng, không trộn mẫu số 17:** (a) t136 đổi profile-negative thành unknown-key có digest fixture khớp: đỏ `TinHieuChotCa` (F08); (b) xoá đăng ký t130 và t139 trên bản sao làm tập đăng ký giảm **134→132**; runner dùng `len(CA)` làm mẫu số. Chỉ đo registration, không chạy cả suite mutant hay khai gate thành công. Bằng chứng này cho thấy CI tự đếm không chứng minh catalog độc lập A12; danh sách case bên ngoài PR/consumer bootstrap phải được neo riêng. Lượt này đã đóng băng danh sách A0 tại `scratch/catalog-names.txt` và bảng mutant trên, ngoài cây PR; chưa chứng nhận bootstrap consumer thực sự cưỡng chế danh sách đó.

## Bảng đo lại

| Phép đo | Kết quả tại môi trường review | Bằng chứng / giới hạn |
|---|---|---|
| HEAD / base / origin/master | d5a980e9a214992c38112e603de6724728857be2 / c0a5cbe89a90588115262e1a2c3ac84cbd98be9e / c0a5cbe89a90588115262e1a2c3ac84cbd98be9e | worktree ban đầu sạch, detached; không thay ref |
| Hash SPEC / ADR / 3 tệp | Khớp cả 5 giá trị được giao | sha256sum đầu và cuối lượt |
| Numstat packet | workflow +107/−0; mã +712/−0; test +865/−0; **3 tệp, +1684/−0** | git diff base..HEAD; write set exact, không đường khác |
| Suite head | **132/134 đạt, đã chạy134, bỏ qua0, rc=1** | `scratch/suite-head.log`; t33/t137 đỏ do thiếu actionlint |
| Suite base | **120/121 đạt, đã chạy121, bỏ qua0, rc=1** | `scratch/suite-base.log`; t33 đỏ do thiếu actionlint |
| Delta suite theo tên | 13 ca A0 thêm: 12 qua, t137 thiếu tool | Không quy kết 134/134 của điều phối là số đo lại tại sandbox này |
| Control lẻ | t53 và t127–t139 trừ t137: **13/13 qua** | `scratch/final-controls.json`; t53/t135 giữ check mặc định không git |
| t139 gốc | **15 giết / 2 sống / 0 tín dụng giả**, mẫu số17 | Log từng tên/ngoại lệ đã lưu, không dựa chỉ dòng tổng |
| Mutant bổ sung | 6 assertion đỏ, 2 sống, 1 Chan không nhận công | 9 ngoài catalog, không cộng vào số 15 |
| Hint regression | **11/11 ca đích ĐỎ dự kiến bằng TinHieuChotCa trên mã head** | `scratch/hint-results.json`; đây là phản chứng, không gọi 11 test pass |
| Hint apply | `patch --dry-run -p0 -d scratch/control < HINT.patch`: **rc=0** | `scratch/hint-dry-run.log`; test-only, chưa áp trên cay-kho |
| shellcheck workflow mới | **rc=0** cho cả hai run block, shell Bash | `scratch/workflow-step-1.sh`, `scratch/workflow-step-2.sh`, `scratch/shellcheck.log`; không thay actionlint |
| actionlint | **không có trên PATH** | t33/t137 fail-close đúng thiết kế; không cài qua mạng |
| git diff --check | rc=0 | base..HEAD |

Lệnh suite đã chạy từ cwd review, trên bản sao đầy đủ (mọi tempfile nằm dưới scratch):

```sh
TMPDIR="$PWD/scratch/tmp" PYTHONDONTWRITEBYTECODE=1 python3 scratch/control/ops/lease_publish_test.py
TMPDIR="$PWD/scratch/tmp" PYTHONDONTWRITEBYTECODE=1 python3 scratch/base/ops/lease_publish_test.py
```

`base` là linked worktree của **bản sao** `scratch/control`, đúng c0a5cbe; không tạo worktree/ref trong `cay-kho`. Các phép đo bổ sung có thể chạy lại bằng `python3 scratch/review_harness.py`, `python3 scratch/extra_checks.py`, `python3 scratch/mutant_runner.py`, `python3 scratch/profile_probe.py`, `python3 scratch/run_hint.py` (các script tự đặt TMPDIR trong cwd).

**Các phần đúng đã kiểm và giới hạn của lời khai:**

- `SO_THU_HOI_KICH_HOAT` vẫn False; tập profile và BIA_MO_LICH_SU vẫn rỗng. Không chạm packet_loop, ops/thu-hoi, ops-publish-lease.yml hay ci.yml. Ngoại lệ kích thước ADR-0044 có phạm vi trong SPEC write_set; số +1684 lớn hơn ước560–780 không tự là vi phạm write set.
- `check` không `--du-bao` vẫn luật cũ, thuần trên control t53/t135. Bia mộ hai chiều làm sản phẩm0 trong khi forecast8, rc vẫn0. Không thấy luật thu hồi mới đổi holder/rc sớm ở ca đầu vào hợp lệ đã chạy. Các đường tăng rc được đọc: forecast thiếu Git/kho12, quét sổ không rỗng12, metadata không policy12 (Q13), lỗi nguồn Git12. F02 là bỏ sót kiểm nguồn. Không đề xuất đưa kiểm sổ vào `check` mặc định để “vá” test thuần.
- M4 dùng bytes đã băm để lấy tree/parents, tự đi ancestry, append-only đứng trước validator, xử lý S==H0, H tree12, namespace là blob/gitlink12, tệp/entry con không hợp lệ12, revocation inactive12. Merge S ở cha2: giữ metadata cho0, mất8; control giữ dùng fixture metadata cũ chưa đủ Q13 (F01), nên số0 này chỉ chứng minh traversal/map, không chứng minh Q13 hợp lệ.
- Reader positive: working copy, bare, linked worktree, pack, alternate đều đọc đúng commit/blob/witness; shallow12, sau unshallow0, object cần thiết thiếu12. Bảy trần count/byte/depth t131 có inclusive boundary và các mutant bỏ chốt đã đo; DAG có store trùng qua đường sâu5 vẫn12 dưới bound4. 129 thư mục anh em dài2 cạnh: 129 lookup qua dưới trần128, memo dùng chung bytes không cộng depth toàn snapshot. Deadline trước spawn/silent process qua t131 nhưng chưa đủ các đường F04/F05.
- YAML: duplicate key lồng nhau12; alias mapping thường parse được; alias recursive12; tag `!!python`12 không chạy code; merge-key YAML bị từ chối12. Không thấy constructor Python unsafe. F06 là hai khe type/date ngoài ma trận hiện có. Regex can_cu ghim HTTPS/repo/issues/comment và số issue; t127 kiểm repo/loại URL/issue sai. Không đo readback JSON/GitHub Q2 ở chế độ active; inactive không nhận revocation mới.
- `_env_rong` không kế thừa `os.environ`; nó dựng PATH/HOME/GIT_DIR/config-global-null/no-system/template-empty/no-replace/prompt/locale, discovery thêm HTTPS-only. GIT_CONFIG_COUNT/KEY/VALUE/PARAMETERS, SSH/ASKPASS/PROXY/HOME caller không lọt **qua hàm đó**. Phần rò ở preflight được chỉ ra riêng F09. Argparse từ chối `--endpoint`, `--profile`, `--da-duyet`, `--kho-canonical`, `--kich-hoat` (t133).
- Workflow chỉ có pull_request_target đúng5 types, branch master, không path/author/dispatch filter; checkout base.sha fetch-depth0, persist-credentials false; fetch H qua endpoint canonical vào ref tạm rồi so OID. Không thấy checkout/chạy/hook/action của H. Permissions workflow/job chỉ contents read + pull-requests read, không quyền ghi. Artifact đúng tên/attempt, đúng receipt.json, if-no-files-found error, retention90. Những điểm này không khắc phục F07.
- Các early-return t137 khi không có thư mục workflow chỉ qua nếu đồng thời không có .git; checkout đầy đủ trong lượt này có cả hai nên không đi nhánh bỏ kiểm ấy. Không có skip nào trong hai suite đo lại. Dòng “mọi ca A0 dùng chot” không bao trùm mọi positive call: ví dụ bỏ routing ném Chan trước chot. Vì vậy ghi ngoại lệ từng mutant là cần thiết.

## chua_do_duoc

1. **Actionlint / wrapper có installer:** không có actionlint trên PATH, không dùng mạng để cài. Không chứng nhận wrapper134/134 hay actionlint0 ở sandbox. shellcheck0 chỉ là phép đo bổ sung.
2. **GitHub/Actions thật:** không mạng; chưa có raw check→suite→run→attempt-job→artifact joins, workflow_sha/S canary, token read scopes, branch protection/required check, upload/download/readback hay receipt consumer dependency. Không dùng đoạn receipt Python chạy local thay canary. Không chứng nhận bootstrap/ready/kích hoạt/land.
3. **Deployment/profile được duyệt:** chưa có identity image/runtime/helper/trust/secret-source do producer độc lập cung cấp. Không tự phê duyệt profile; không kết luận local bare fixture chứng minh HTTPS production an toàn. Các hướng helper/config/env nguồn bị cấm chỉ mô tả bằng lời ngoài fixture t129/t130/t136 đã cung cấp.
4. **Budget production và E2E:** không có benchmark3cặp xen kẽ baseline/candidate trên cùng snapshot/clock của deployment được duyệt; không xác nhận tỷ lệ≤2 hay8trần đủ cho toàn roots production. T131/fixture DAG/wide/pack là control chức năng, không phải đo capacity/E2E.
5. **Catalog độc lập ngoài PR được consumer cưỡng chế:** registration134→132 khi bỏ t130/t139 đã đo; không chạy suite mutant toàn bộ, không có raw bootstrap consumer guard để chứng nhận A12. Catalog/hash trong verdict này là neo review độc lập với nhánh; chưa chứng minh quy trình land dùng nó.
6. **Các gate khác EVIDENCE:** chưa đo lại doctrine-scan/doc-claims-check/release-verify/ruff hay ls-remote316/for-each-ref316 tại kho điều phối. Không xác nhận các con số đó bằng số local358 của mirror. Các gate không chạy không được ghi pass; không coi lời khai điều phối là bằng chứng thẩm quyền đã đo.
7. **Model identity chi tiết / transport bên ngoài:** chỉ tự khai đúng mô hình Codex/GPT-6 và local tools của phiên; không suy model build từ tài khoản submitter hoặc giá trị model ghi trong lease, không chứng nhận phiên bản codex-cli từ EVIDENCE.
