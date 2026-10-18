Reviewed commit: 783463b5d62efbc43c6a6116e32c43accbc485f7
Verdict: changes_requested — P0=0 P1=4 P2=6 P3=0

Review độc lập, offline, lượt 1 của Packet #812 / MAY-ADR-0054-a. Reviewer: Codex, họ OpenAI; surface `codex_cli`, transport `machine`. Không có telemetry cung cấp tên model runtime cụ thể. Không kế thừa context executor và không ghi vào `/home/user/rv812`. Mọi fixture, fetch/push thử nghiệm và thay đổi state chạy trên kho giả cục bộ dưới `/tmp`; không truy cập GitHub, không cần PR.

Base `4c7c29858220ae575bebc5e0a343842cd3db4546`; tree của head `d2990e895a2c962c75fe2090ba570870f3f668f3`. Clone không shallow; base là tổ tiên head; worktree nguồn sạch trước và sau review. Đã đọc lease `origin/ops/wp812-spec:ops/leases/wp812-r1-g2-claude.yaml`: executor Claude, reviewer Codex, generation 2, assurance `cross_approved`, class `sensitive`. Dòng executor trong đặc tả được lease g2 thay đúng chỉ thị đã nêu trong yêu cầu.

Hai băm đặc tả đo bằng `sha256sum` đều khớp:

- `ops/specs/wp812.md`: `6b8b6c79703bc21949adf006ffc4bb351374254f5a27a0d85ed908ece6511d26`.
- `ops/specs/may-adr-0054-chung.md`: `4e3d1e1b3f6a0b60b96ad7b70f0ece97eca4bb3d6d10defeab1cd24ac6d1cbf0`.

**Bảng lớp — đếm theo nguyên nhân, không theo số biểu hiện**

Các dòng dưới đây là dòng trên exact head. Tên ngắn `pl` = `.claude/dev/packet_loop.py`; `test` = `.claude/dev/packet_loop_test.py`. Các probe chính có thể chạy lại bằng `python3 REPRO.py --copy /tmp/rv812-review-copy`; kết quả đã chạy nằm trong `REPRO.jsonl`. Baseline của script này có verdict blob Git thật, băm đúng, và được kiểm riêng bằng cả `_thieu` lẫn `_neo_git` của validator đầy đủ trước khi đổi đầu vào.

| slug | hạng | các biểu hiện (file:dòng) | phép đo / tái hiện đã chạy | hướng vá |
|---|---|---|---|---|
| receipt-validation-incomplete | P1 | pl:2396, pl:2409, pl:2523, pl:2532, pl:2545; test:5936 | Baseline H thật vào `approved_pending`; chỉ đổi provider thành `openai_chatgpt`, hoặc transport thành `human`, vẫn rc=0. Verdict path/object không tồn tại cũng được nhận. Validator đầy đủ từ cùng head bác các dữ liệu này. | Dựng đủ phụ thuộc canon; nguồn validator hỏng phải từ chối; chạy schema **và** xác minh mỏ neo Git/băm. HINT có các chốt tương ứng. |
| connector-verdict-incomplete | P1 | pl:2560, pl:2563, pl:2568 | `PENDING` review trên head, không có kết luận sạch, vẫn `accepted`; review `CHANGES_REQUESTED` chứa P1 và issue comment chứa P1 cũng đều `accepted`. | Đòi trạng thái review hoàn tất; đọc finding trên đủ ba endpoint, neo head và miền hạng cho từng loại. HINT có sửa vị từ. |
| ci-attempt-provenance-missing | P1 | pl:2585, pl:2587, pl:2590, pl:2593 | Chỉ thêm `run_attempt=2`, `status=in_progress`, `conclusion=null` vào run mới nhất; giữ check xanh attempt trước: rc=0, `accepted`. Check-run có URL thuộc kho khác vẫn được nhận. | Neo jobs/check-runs vào đúng kho, run và attempt mới nhất; thiếu provenance thì từ chối. HINT gợi ý đọc endpoint jobs và đối chiếu check-run URL. |
| conflicting-evidence-overwrite | P1 | pl:2427, pl:2434, pl:2563, pl:2587 | Cùng comment ID có bản P1 rồi bản P3, `total_count=1`, kèm quyết định P3: rc=0, `accepted`; hai workflow record cùng ID nhưng khác path cũng qua. | Sau phép đếm ID phân biệt, kiểm mọi bản cùng ID có nội dung/danh tính nhất quán; từ chối mâu thuẫn trước lọc và lập map. HINT thêm chốt dùng chung. |
| identity-compared-by-provider-family | P2 | pl:2528, pl:2538, pl:2539, pl:2540 | Biên nhận Gemini hợp lệ qua `_thieu` đầy đủ; với ngữ cảnh executor `google_antigravity` / `gemini`, vị từ từ chối riêng `ho-executor` (rc=11). Ngoài ra không có phép so transport lease ↔ receipt. | Chuẩn hoá danh tính qua nguồn canon; so đủ identity, dùng **model_family được lease khai** thay vì họ mặc định của tên provider. HINT sửa phép so. |
| findings-not-receipt-bound | P2 | pl:1171, pl:1183, pl:1192, pl:1212, pl:2568, pl:2595 | ADR-0054 `record-review changes_requested --finding-id executor-invented-class` không có biên nhận vẫn rc=0 và ghi bộ đếm. Connector P3 được xử lý bằng ID số, không có bảng lớp H. | Mọi verdict đưa finding vào bộ đếm phải lấy slug từ H đúng tuple I10; connector cần ánh xạ `(endpoint,id)` → slug do reviewer ký. HINT minh hoạ hai cửa. |
| stop-validation-order | P2 | pl:1014, pl:1160, pl:1213, pl:1225, pl:2607 | Ở trần vòng, review có `--codex-call`/receipt không tồn tại trả rc=3 và **đổi state**, còn `attempt_open=true`, chưa ghi review. Ở trần attempt, doctor path không tồn tại cũng đổi state thành `blocked` trước kiểm input. | Tách pha xác thực khỏi pha ghi sổ/dừng; cửa khép lượt ghi đủ kết quả trước xét trần. Gom same-failure và rescue vào `_xet_dung`. HINT minh hoạ. |
| lease-checks-worktree | P2 | pl:2476, pl:2478, pl:2479, pl:2499 | Baseline lease được nhận; chỉ xoá bản đặc tả trong worktree, giữ nguyên mọi object/ref và băm: rc=7 (`lease_publish check rc=6`), dù đặc tả đúng vẫn có tại lease OID. | Validator canon phải kiểm snapshot nội dung lease/ref đã đo, không phụ thuộc checkout ứng viên. HINT dựng snapshot riêng. |
| new-input-schema-incomplete | P2 | pl:668, pl:2439, pl:2530, pl:2579 | `required_checks=false`, `0`, `{}`, `""` đều ghi `leased` thay vì từ chối; slug có newline được approve; state JSON với `ngu_canh_lease={}` qua `_load` rồi `accept` traceback `KeyError: 'branch'`, rc=1. | Phân biệt thiếu với giá trị sai nhưng falsy; kiểm đầy đủ context/pending schema trước dùng; `fullmatch` slug. HINT có các chốt nền, cần mở rộng ma trận kiểu. |
| required-mutation-coverage-missing | P2 | test:5884, test:5921, test:5987, test:5997, test:6016 | Cả 19 ca #812 vẫn 19/19 khi lần lượt gỡ H lease check, gỡ holder check, gỡ shallow guard, hoặc gỡ remote pending-head check. Các bất biến tương ứng chưa được test bảo vệ. | Thêm baseline H/Đ thật, ca đổi một yếu tố cho từng chốt, và mutant riêng khóa `r812_*`; ghi lý do đỏ. HINT sửa chốt sản phẩm; ma trận test phải bổ sung theo bảng dưới. |

**Giải thích ảnh hưởng và phạm vi quét cùng lớp**

`receipt-validation-incomplete`: `_canon` chỉ chép ba tệp, trong khi `bien_nhan_v2._provider_chinh_tac` còn cần `AGENTS.md` và protocol. Do thiếu nguồn, `PROVIDER_NGUON_HONG` luôn khác `None` trong môi trường canon này; `_thieu` bỏ các phép kiểm hợp đồng provider/surface/transport và các cấm assurance. Caller không kiểm trạng thái lỗi nguồn. Đồng thời chỉ gọi `_thieu`, bỏ `_neo_git`, nên đường dẫn/băm verdict chỉ cần đúng hình dạng. Đã quét cả phần schema, danh tính và mỏ neo: không chỉ một trường bị bỏ. Fixture dương gốc còn dùng `evidence_url=https://x/y`, verdict không tồn tại và băm lặp `a`; validator đầy đủ bác mỏ neo ấy. Vì vậy `r812_duong_moi_du_dieu_kien` chứng minh luồng chạy được với một YAML, chưa chứng minh có H hợp lệ. Đây vi phạm I1/I8 và M2, dù nguồn YAML được người gọi cung cấp hoàn toàn thiện chí.

`connector-verdict-incomplete`: mọi review của bot có `commit_id=head` đều được tính là xong, không xét `state`. Chỉ `review_comments` được đọc badge; `reviews` và `issue_comments` chỉ dùng làm dấu hoàn tất. Bởi vậy finding nằm ở hai endpoint kia bị mất trước kiểm P0–P2/P3. Cùng lớp còn khiến P3 ở hai endpoint ấy không cần quyết định. Không coi review pending, lời nhắc head hay comment có finding là kết luận sạch. Các probe có đầy đủ envelope kho/PR/head và số ID hợp lệ.

`ci-attempt-provenance-missing`: lấy `max(run.id)` chỉ chọn run; rerun giữ cùng run ID, có attempt mới. `kiem-gate` chọn check ID lớn nhất trong các check đang có, không chứng minh check ấy thuộc attempt mới nhất. Mã mới không đọc `run_attempt`, status/conclusion của run hay endpoint jobs. Nó cũng không kiểm repository trong từng check-run. Mô hình readback R không miễn phép kiểm nhất quán I7. Probe kho khác dùng URL API thông thường, không soạn đường dẫn thoát cây.

`conflicting-evidence-overwrite`: đếm tập ID bằng `total_count` là cần nhưng chưa đủ. `_trang_du` trả cả bản lặp mâu thuẫn; dict comprehension của badge giữ bản cuối, `max` trên workflow ID bằng nhau giữ một bản theo thứ tự input. Đã kiểm cả connector và workflow; bộ đọc check-run cũ có chốt riêng và không bị báo lại ở lớp này. Không so ID giữa các endpoint.

`identity-compared-by-provider-family`: `HO_MODEL_MAC_DINH` không có Google Antigravity; executor đó có họ được khai trong lease, không có một họ cố định theo provider. So `ho_exec == ho(provider)` chặn một ngữ cảnh hợp lệ. Đây là lỗi phép so khác với lỗi dựng môi trường validator ở lớp đầu: sau khi dựng đủ môi trường canon, phép so này vẫn sai. Probe đơn vị giữ các trường khác của predicate và validator đầy đủ xanh, chỉ chuyển executor sang tuple Antigravity/Gemini hợp lệ.

`findings-not-receipt-bound`: `_du_dieu_kien_approve` chỉ chạy khi tham số CLI là `approve`. Nhánh verdict âm dùng trực tiếp `finding-id` rồi tăng `finding_counts`; executor vẫn tự cấp slug. `accept` cũng dùng khóa connector bằng số comment ID, không cần H ký bảng lớp. I11 thuộc phần chung và chạm ngay các cửa #812 sửa; đây không phải yêu cầu triển khai vòng P3 của #814. Cần giữ quyết định nợ của executor tách khỏi việc reviewer đặt lớp.

`stop-validation-order`: `_xet_dung(record-review)` được gọi trước xác minh codex-call và receipt, có thể ghi rescue rồi mới thấy input hỏng. Ở cửa begin, nó chạy trước xác minh doctor. Ngoài lỗi I4, cửa đóng review bị trần vòng chặn trước khi ghi kết quả đang mở (I5). M4 cũng chưa thực hiện việc gom mọi stop: same-failure và post-review budget vẫn nằm ngoài helper. Hành vi legacy cần giữ riêng theo I9; các phản chứng này dùng `luat_adr0054=true`. Trường hợp invalid review đã đo: review count giữ 1, attempt đang mở vẫn true, nhưng state chuyển blocked.

`lease-checks-worktree`: `git show lease_oid:spec_path` đúng chỉ chạy sau H check. H check lại nhận `--root` là checkout hiện tại và validator đọc prompt/spec từ đĩa. Kho không cần checkout nhánh ops để dùng lease remote; bản đặc tả có băm trong Git mới là nội dung được M1 chọn. Probe chỉ xoá bản worktree trong kho tạm, không đổi lease hay nguồn validator.

`new-input-schema-incomplete`: `or []` xoá bằng chứng giá trị có mặt nhưng sai kiểu; regex dùng `$` có thể khớp trước newline cuối; `_load` chỉ đòi context là dict và receipt summary là dict. Những đường input mới này phải trả mã có kiểm soát và không ghi state. Đã đo cả nhận nhầm dữ liệu hỏng và traceback. Đường context rỗng giữ byte nhưng vi phạm yêu cầu từ chối có kiểm soát; các required-check input hỏng lại thực sự ghi state.

**Đối chiếu từng ca bắt buộc `nghiem_thu`**

Không thiếu tên ca cho 21 mục cụ thể của danh sách. Có mục đo nền sai hoặc chưa đủ bất biến; sự hiện diện của tên ca không thay được chứng minh H và mutation coverage.

| mục bắt buộc | ca `r812_*` tương ứng | kết quả / giới hạn |
|---|---|---|
| lease chỉ ref cục bộ | `lease_chi_o_ref_cuc_bo` | Đạt; mutant bỏ ls-remote bị giết. |
| đặc tả lệch băm, state nguyên byte | `dac_ta_lech_bam` | Đạt; hai mutant băm/ghi-state bị giết. |
| init chưa lease | `duong_cu_luon_false` | Có đo awaiting_lease. Chưa có mutant riêng gỡ chính chốt init dưới khóa r812; mutant hiện tại đổi cờ false. |
| Ctx.cap_lease đường cũ | `duong_cu_luon_false` | Đạt leased + false; mutant tương ứng bị giết. |
| true không quay lại đường cũ | `true_khong_quay_ve_duong_cu` | Đạt và kiểm byte; mutant awaiting bị giết. |
| thiếu kích hoạt → false | `khong_kich_hoat_la_false` | Đạt; chỉ bảo vệ điều kiện 0055, chưa bảo vệ shallow/ba phép đo land. |
| approve còn P1 | `approve_kem_lop_p1` | Có đo lớp/hạng; nền receipt H của fixture gốc chưa hợp lệ. |
| hạng PX | `hang_px` | Có đo miền hạng offline; chưa bao phủ các endpoint connector. |
| lệch surface | `bien_nhan_lech_surface` | Có đo phép so surface trực tiếp; không đo nguồn/hợp đồng canon còn sống. |
| check bắt buộc vắng | `check_bat_buoc_vang` | Đạt ở tập check cố định. |
| check cùng tên app khác | `check_cung_ten_app_khac` | Đạt; đối chứng job cũ đỏ + job app khác xanh bắt được bypass. |
| readback PR khác cùng head | `readback_pr_khac_cung_head` | Đạt đối với issue_url từng mục. |
| P3 offline thiếu quyết định | `p3_offline_thieu_quyet_dinh` | Đạt chốt quyết định offline. |
| packet không ADR-0054 đi đường cũ | `khong_kich_hoat_la_false`, `duong_cu_luon_false` | Đường cũ vẫn accepted; nền suite cũ xanh. |
| generation khác | `bien_nhan_lech_generation` | Đạt phép so generation hiện hành. |
| receipt changes_requested, CLI approve | `verdict_changes_requested` | Đạt. |
| receipt blocked, CLI approve | `verdict_blocked` | Đạt. |
| lớp rỗng + connector sạch → accepted | `duong_moi_du_dieu_kien` | Luồng xanh, nhưng receipt không qua `_neo_git`; connector fixture thiếu trạng thái run/attempt. Chưa chứng minh positive H/I7 đầy đủ. |
| lease chưa comment workflow | `lease_chua_comment_workflow` | Đạt; mutant tương ứng bị giết. |
| workflow khác, cùng app/job | `check_cung_ten_workflow_khac` | Đạt với check_suite khác; chưa đo attempt mới trong cùng run. |
| mở attempt ở trần, cửa khép vẫn chạy | `cua_khep_luot_van_chay` | Chỉ dựng đường legacy và trần attempt; không đo cửa khép ADR-0054 ở trần vòng. Mutant đã có chỉ siết trần attempt. |

Đã chạy lại riêng 19 ca và toàn bộ 20 mutant `r812_*`, lưu lý do assertion trong `MUTANTS.jsonl`: mọi mutant khai báo đều giết ca đích vì trạng thái/mã thoát/byte thay đổi đúng chốt, không có traceback setup/import vô can. Đối với ca dương, mutant siết tập lớp rỗng đỏ đúng `bang-lop`/`con-P0-P2`.

Đã thêm bốn đột biến kiểm toán ngoài bảng của candidate; tất cả sống qua **19/19** ca #812 (`SURVIVORS.jsonl`):

| đột biến kiểm toán | bất biến/chốt không được suite #812 bảo vệ |
|---|---|
| bỏ `p.returncode` của lease H check | I2(H) |
| bỏ điều kiện kết quả `ai-dang-giu` | I2(Đ) |
| thay shallow guard bằng True | M1 / ba phép đo land của ADR-0052 |
| bỏ so remote branch head với pending_sha | I1/Đ và M3 |

Ngoài bốn thiếu hụt đã chứng minh bằng mutant sống, chưa có ca/mutant #812 bảo vệ: đủ từng phép đo land và khai đúng một dòng; validator canon thiếu phụ thuộc; mỏ neo Git/băm receipt; identity Antigravity và transport; review âm phải có H/slug; attempt mới nhất; review pending; badge ở review/issue-comment; ID lặp mâu thuẫn; context sai kiểu; input hỏng ở trần. I10 mới có mutant generation, chưa có phản chứng riêng cho packet/SHA/spec_hash/role. I11 chưa có mutant. I6 chưa mở quyền phái sinh trong packet này nên không yêu cầu triển khai #813–#815.

**Kết quả lệnh và bằng chứng dương**

- `cp -a /home/user/rv812 /tmp/rv812-review-copy`, rồi `python3 /tmp/rv812-review-copy/.claude/dev/packet_loop_test.py`: rc=0; `nền: 424/424 đạt · BỎ QUA: 1`; `TỔNG: ĐẠT`. Tổng 425 ca, 188 mutant. **187 mutant đo được và giết; 1 mutant Windows không đo được**, không ghi thành đã giết. Ca bỏ qua: `luong_canonical_chay_that`; mutant bỏ qua: `luong_canonical_chay_that_dao_os_name`. Toàn văn `SUITE.log`.
- Trên bản sao, `python3 .claude/dev/packet_loop.py doctrine-scan --root .`: rc=0, 10 tệp, 0 chỗ chép doctrine.
- Trên bản sao, `python3 .claude/dev/packet_loop.py adr-song --root .`: rc=0, 53 ADR / 53 dòng, khớp 1–1; ngoại lệ trạng thái 0016 được khai sẵn.
- `git diff --check 4c7c298 HEAD`: rc=0.
- Đã đo `_che_do_0054` với Git thật: baseline true; thiếu khai, khai hai dòng, OID chứa ADR nhưng không đưa ADR vào, thiếu cụm kích hoạt, protocol còn chưa kích hoạt, clone shallow đều false (`EXTRA.jsonl`). Đây là phép đo reviewer, không lấp phần thiếu test/mutant trong candidate.
- Đã đổi validator **worktree ứng viên** thành script lỗi trong fixture: record-lease vẫn rc=0, chứng minh đường này dùng bản `origin/master`. Lease local-only và comment thiếu cũng bị từ chối như các ca của suite. Không tìm thấy bypass riêng ở các chốt đó; vấn đề lease được báo là context của H check và coverage.
- Các probe từ chối bình thường trong 19 ca #812 kiểm nguyên byte đều xanh. Phản chứng I4 mới ở các đường trần và lược đồ như bảng lớp; không suy rằng mọi reject đều làm hỏng state.

Đo kích thước bằng `git diff --numstat 4c7c298 HEAD`:

| tệp | thêm | xoá |
|---|---:|---:|
| `.claude/dev/packet_loop.py` | 276 | 18 |
| `.claude/dev/packet_loop_test.py` | 168 | 1 |
| `docs/PROTOCOL_DA_PHIEN.md` | 4 | 0 |
| Tổng | **448** | **19** |

Đúng 3 đường dẫn, 448 ≤ 450, đạt ADR-0053. M5 thêm `approved_pending` có điều kiện trong protocol đã có. Không báo finding kích thước hay doc M5.

**HINT và phần chưa xác minh**

`HINT.patch` là diff gợi ý áp trên exact head; đã chạy `git apply --check` trong bản sao cùng SHA và kiểm cú pháp Python bằng `compile`, cả hai đạt. Không áp patch vào KHO. HINT minh hoạ chốt cho các lớp phức tạp: canon/anchor, identity, ID mâu thuẫn, đủ endpoint connector, provenance attempt, slug H, thứ tự dừng và snapshot lease.

HINT **chưa phải bản sửa đủ nghiệm thu**: bổ sung hợp đồng readback jobs/biên nhận connector cần fixture, schema và mutant tương ứng; cần kiểm đủ mọi kiểu dữ liệu mới và dọn snapshot tạm. Chưa chạy suite sản phẩm trên HINT và không khai các finding đã đóng. HINT không tối ưu theo ngân sách 450 dòng; executor phải thiết kế/refactor trong trần hoặc xin chủ kho điều chỉnh scope, không nhập nguyên xi rồi coi là đạt. Đặc biệt phải sửa fixture dương để có H và provenance thật trước khi đánh giá bản vá.

Ngoài phạm vi, không tính hạng: `mo-lai`, `cho_chu_kho`, checkpoint mới (#813), vòng vá P3 (#814), generation kế tiếp (#815), ghi số lần đẩy và kích hoạt (#816). Các lỗi ở cửa hiện hữu #812 được phân hạng ở trên; không đưa việc chưa làm các packet sau vào số finding. Không merge/push/đăng verdict ra dịch vụ ngoài.
