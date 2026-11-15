# wp1325 r1 — đo đồng thời để A9 không bỏ lọt đột biến bỏ khóa
tran_loi_goi_codex: ADR-0055@d2e3052d479d140b7e7b91df41ec4914fab7d544
tran_kich_thuoc_sensitive: ADR-0053@8ab100793df9831505f495543a74044b91c2c9ab

packet_id: wp1325
packet_issue: 1325
revision: 1
planned_generation: 1
mission_issue: 1172
executor: claude
reviewer: codex
assurance_target: cross_approved
environment: cloud
depends_on: []
risk: sensitive
review_class: sensitive
effective_review_class: sensitive
windows: required
status: revised_draft_not_frozen_not_leased
prospective_spec_path: ops/specs/wp1325-a9-concurrency-r1.md

## nguon_cap_viec

Packet mới https://github.com/ducthangho/tra-luat/issues/1325 theo yêu cầu trực tiếp “Đồng ý, làm đi, chẩn đoán và vá luôn”, rồi “Đồng ý, làm tiếp đi”. Parent/checkpoint: https://github.com/ducthangho/tra-luat/issues/1315#issuecomment-6886050928; Mission direction approval/installation https://github.com/ducthangho/tra-luat/issues/1172#issuecomment-6881279303 (r40). Đây là correction kiểm thử hữu ích riêng để hỗ trợ hướng Mission đã duyệt; không dùng entitlement r40 đã đóng, không ghi rằng r40 đã duyệt enabler mới hoặc ngân sách mới.

Snapshot chính sách dùng cho review1–2: first-parent master `116d7767a1ac5628663ef11d1287fce83f491892` , gồm ADR0067. Những cơ chế ADR0067 còn đợi đổi cổng (lease/audit/tự merge) vẫn theo cổng cũ, không suy đã có hiệu lực. Ràng buộc byte của bản này và readback Issue được giữ trong hồ sơ review; chưa có đóng băng/lease.

## ba_moc_git

Immutable acceptance baseline = continuation base = `072d45a0595f3d2ff9f0880143a237c9e0ea70c3` . Pre-lease draft candidate Y= `266bc316dc3195a71d780e5a363a22524b4036ee` ; tree `3e0002874fa602486b406fa6bf6d67962ca004ee` . Diff baseline..Y: đúng1tệp/14dòng thêm, đo2026-11-15T04:19Z. Source revision này không đổi Y; review1 technical code_verdict approve nhưng overall/spec changes_requested, không phải provenance acceptance hay freeze. Candidate WP1315 H `669af5f9f58dfd72324d1f5b6aaefd15745592b1`  và audit gốc riêng của nó giữ nguyên.

## write_set

- scripts/test_fragments/wp1099_nlm_nap_lai.py

Không wildcard. Worker chỉ được nhận write set này qua lease tương lai; ghi draft spec/prompt/lease/receipt trên nhánh metadata riêng không cho phép sửa code khác. Không lấy generated artifact hay manifest làm worker write set ngầm.

## ngoai_pham_vi

Runtime NLM/auth và mọi nguồn thật, protected target journal/seed/HMAC/witness, ADR/protocol/authority/merge/lease gate, workflow, golden, VERSION, canonical phát hành: không sửa vì correction chỉ ở test. Không source push/PR/CI/merge/G5 trong bước review hiện tại.

Generated scripts/tl_test_fragments_bundled.py và RELEASE_MANIFEST.json chưa được worker sửa. Bundle committed của Y vẫn chứa A9 cũ; candidate chưa đủ điều kiện phát hành/bundle acceptance. Việc tái sinh phải thuộc land-only scope/admission riêng; không dùng kết quả scratch thay bằng chứng ở exact integrated head.

## muc_tieu

1. scripts/test_fragments/wp1099_nlm_nap_lai.py: A9 đo số lần thực thi đồng thời thân _nap_lai_mot thật, để refusal của lần ghi marker thứ hai không che đột biến bỏ khóa; giữ chốt số lệnh nạp, I/O thật, child-process, synchronization/deadline và start/join/finally/stderr restore.
2. scripts/test_fragments/wp1099_nlm_nap_lai.py: đối chứng khóa thật vẫn đạt, kể cả khi cài hook chỉ từ chối lần ghi thứ hai; không sửa runtime hay kết luận nguyên nhân CI thiếu bằng chứng.

## nghiem_thu

A1 (mục tiêu1): chạy external synthetic verify-a9.py trên baseline và candidate. Bản cũ + bỏ khóa + từ chối lần ghi thứ hai phải sống (chứng minh lỗ test); bản mới cùng đầu vào phải ném TinHieuChotCa A9. Bản mới + bỏ khóa không refusal cũng phải ném A9. ĐỎ nếu mutant sống, sai case/loại exception, hoặc peak không được đo khi hai thân chồng nhau. Mutation đối với bản vá: bỏ phép kiểm dinh[0]==1 phải làm phản chứng refusal sống trở lại. Đây là behavioral check, không khớp chuỗi.

A2 (mục tiêu2): cùng verifier có hai healthy-control rows (có/không cài refusal hook) phải đạt. Với khóa thật, concurrent_marker_write_attempts=1; hook không thực sự từ chối lần ghi nào. Với mutant, attempts=2 và refusal áp vào lần thứ hai khi bật. Không gọi healthy row là đã thực hiện một refusal. ĐỎ nếu healthy case ném hoặc attempts sai, không dùng exception/bỏ qua làm pass.

A3 (mục tiêu1,2): full fragment thật trên Linux dev phải giữ A12/12, D3/3,30/30 mutants và skip0. Trên Windows3.12.10 và3.13.17, bundle được tái sinh TRONG SCRATCH từ source candidate qua canonical generator phải giữ A12/12,24 mutant áp dụng bị giết; ghi rõ FIFO mutant không áp dụng và docs D không có trong bundle. ĐỎ nếu có ca/mutant áp dụng không đạt, returncode khác0, timeout/mất proof hay skip trái phép. Kết quả này chỉ là scratch-generated bundle evidence; không phải bundle committed Y hoặc native-main toàn packet/CI.

A4 (mục tiêu1,2): exact candidate sau tái dẫn xuất dưới lease có tl selftest N/N (đo draft trước đây1777/1777 rc0), F lint delta0, git diff --check rc0 và changed_paths đúng write set. SHA256 blob TOÀN TỆP scripts/test_fragments/wp1099_nlm_nap_lai.py ở Y =24dd2e7c076da6542742a5c94e0ca69ee522d28aecaf18ea908b403c27ada730. SHA256 file diff candidate.patch =4fd7bf1818c004e741309a322429ba9be4eca6682566c5dd910981fd35c5e3f8. Đây là hai đối tượng khác nhau. ĐỎ nếu so sai đối tượng, hash/rc lệch, source thay sau review hoặc xuất hiện file ngoài scope. Không nhận code review1 cho head khác.

A5 (mục tiêu1,2): báo cáo giữ nguyên r40 Windows CI31/32 chưa xác minh đóng, native interrupted/candidate Windows not_run và M9 aggregate chưa hoàn tất. ĐỎ nếu dùng test cục bộ/correction A9 làm bằng chứng khẳng định root cause duy nhất, CI xanh, accepted/landed/canaryPASS hay audit đã chuyển từ H cũ.

I1 — integration acceptance riêng, CHƯA ĐO: sau một admission land-only hợp lệ mới tái sinh committed adapter/manifest qua canonical generator, nhận exact integrated head Z và review/gate tương ứng khi artifact/tree thay. Trên Z, test-fragments-check phải xác nhận committed adapter khớp generator; bundle_fragment_check và Windows bundle case phải chạy trên chính artifact/head đó, với bo_khoa_luong bị giết đúng case A9 trong bundle_fragment_check trên Z; không dùng lần giết mutant này làm bằng chứng rằng forced marker-write refusal đã xảy ra trong bundle. Kết quả scratch ở Y không đóng I1. Chưa đủ source/CI/connector/native/M9/policy/K0–K7 hay hậu-merge/bookkeeping thì chưa merge-ready/landed. Admission CI riêng phải phân loại chi, dự trù hữu hạn/whole-fit; không tự dispatch từ spec này. Người đo I1 là Land Operator trong phiên land-only đã được admit riêng. Thời điểm: sau tái sinh và xác định Z, trước promotion/merge; hậu-merge đo lại trên exact merged head M khi admission yêu cầu. Đọc ngược record identity Z/M và provenance theo protocol §10.2.2 (run/attempt, checkout SHA, gate output và workflow definition), JSON test-fragments-check, JSON bundle_fragment_check, Windows job/command/rc và hash artifact/bundle đã chạy; so hash với exact tree tương ứng. Thiếu, stale, skipped hoặc chỉ có rc0 mà không positive output thì I1 chưa đạt. Chưa có các record ấy ở bản nháp này. Readback bo_khoa_luong không đòi một row per-mutant mà gate không xuất: phải nối cases[wp1099_nlm_nap_lai].ok=true của bundle_fragment_check với freshness/hash của committed adapter và bảng mutant tại exact Z (bo_khoa_luong có đích A9, không nằm trong capability skip). Fragment thật chỉ trả true khi mọi mutant áp dụng bị giết đúng đích. Ghi đây là kết luận qua hợp đồng whole-fragment, không giả một trace per-mutant hay một refusal row; nếu không xác minh được chuỗi bằng chứng này thì I1 chưa đạt. Phạm vi I1 chọn readback bundle bo_khoa_luong nêu trên, không yêu cầu hay nhận một refusal row từ JSON không có trường đó. Forced-refusal coverage vẫn là external-only A1/A2 trên source exact head sau lease; thiếu một forced-refusal run riêng cho generated bundle là limitation, không được quảng bá thành đã đo. Không thêm một lượt verifier bundle hay CI vào budget bằng câu này.

## tiep_nhan_prelease_draft_va_lease

Code14dòng đã được viết trong private draft TRƯỚC spec/Issue/lease; lưu nguyên provenance ấy, không backdate. Review1 chỉ approve technical content. Y chưa phải output của worker có lease.

Trình tự tới đây: (1) Issue1325 đã tạo; (2) revised spec phải được review độc lập approve rồi đóng băng đúng blob/hash vào metadata ref và ghi sổ theo ADR0067; (3) ngay trước cấp lease, fetch đủ refs và canonical ai-dang-giu quét toàn kho, write set không có holder mới cấp. Phải đối chiếu cả scope của WP1315 và mọi overlap khác; không coi hai tên Packet khác nhau là đủ exclusion. Bằng chứng scan cũ holder0 chỉ tham khảo, phải đo lại tại action; unknown/fail chặn.

(4) Lease owner-authorized còn hiệu lực phải neo exact spec/ref/hash/generation/provider và khớp executor=claude, reviewer=codex, environment=cloud, depends_on=[], risk=sensitive của spec; đổi một trường hợp đồng phải có revision/generation hợp lệ. Lease phải ghi rõ Y chỉ là input/hint đã có trước lease, không là output đã admit và không cho adopt nguyên commit dưới tên provider khác. Cổng cấp lease theo standing delegation CHƯA đổi thì cần quyền owner hiện hành (E2 nếu thiếu); không ghi agent tự cấp lease theo ADR0067 quyết định5 trước hiệu lực. (5) Executor dưới lease mới xác minh pre-leaseY/baseline/tree/blob/diff/đối chứng, rồi bắt buộc tái dẫn xuất correction từ ý tưởng/diff của Y vào branch riêng bắt đầu từ baseline; không adopt nguyên Y dưới nhãn tác giả Claude và không git-am mù. Ghi before/after exact head/tree; nếu OID đổi do commit provenance, phải review/evidence lại trên head mới, không chuyển approvalY tự động. Chạy lại A1–A4 đúng head nhận dưới lease, giữ provenance chi phí trước lease và cả trial failures. Không chỉnh journal/counter để làm draft thành lịch sử được admit.

(6) Chỉ thực hiện source publication/CI/integration sau các admission tương ứng, không lấy freeze/spec review làm quyền ghi code, owner audit, merge hoặc target grant. Review tiếp theo được đề nghị là spec/closure review riêng; chưa có lease hoặc worker action từ nó.


## dinh_tuyen_va_provenance_tac_gia

Theo protocol §8/ADR0041, executor của Packet sensitive này là Claude (họ model claude), environment cloud; không dùng ngoại lệ Codex executor sensitive và không thêm Codex executor call. Sensitive closure sau thi công cần fresh Codex review cross_approved trên H_new do Claude thực sự tạo, hoặc actual human audit đúng luật khi được cấp; không dùng các Claude reviews của pre-leaseY làm Codex cross-review. Không tự miễn gate hay đổi class để hợp tuyến.

Tác giả kỹ thuật của private pre-lease Y: provider codex, model_family openai, execution_surface codex_service, transport machine, theo witness của operator trong chính phiên soạn patch qua công cụ. actual_serving_model, actual_effort và provider session/runID của tác giả KHONG_DO_DUOC; /root chỉ là task path, không là model/session attestation. Git author/committer Duc Thang là identity chở commit, không chứng minh model. Xem AUTHOR-PROVENANCE.json, gồm giới hạn của witness. Đây không phải lời khai Y đã có lease, đã được phép route Codex sensitive, hay nằm trong tỷ lệ30%; ratio/history không đo đủ vẫn UNKNOWN và không được reset.

Trước khi worker chạy, chủ kho cấp lease/entitlement hiện hành cho Claude và readiness phải xác minh đúng surface/provider. Claude executor dưới lease mới phải hiểu, tái dẫn xuất rồi tự áp correction tối thiểu từ hint pre-leaseY; ghi hint_provenance và giữ tác giả/historical costs của input. H_new là commit mới do workflow được admit sinh ra; không khai tác giả input Y thành Claude chỉ vì nó được tiếp nhận. Whole diff/acceptance ở H_new phải được re-verify, cùng nguồn spec/lease chính xác. Independent Codex reviewer mới sau đó phải đọc exact H_new và ghi verdict/receipt đầy đủ; không chuyển code/spec verdict của Y sang H_new. Những Claude reviews hiện có chỉ chứng minh nội dung draft/spec ở các hash đã đọc, không đóng assurance của H_new. Mọi source executor/reviewer call tương lai cần admission/budget riêng; không nằm trong allowance review-spec hiện tại.

Cloud executor điều phối A3 trên máy Windows của chủ kho đang Online trong list_devices qua Desktop Commander, theo ADR0057–0059; không vào máy ngoài list_devices hay nâng quyền/đổi power policy. Readiness trước clock phải probe hostname, identity thường, Python/runtime, actual leased executor surface/tool capability, thư mục source/scratch riêng, tải và khóa theo từng máy; một heavy test trên một host vật lý, có heartbeat/nhả khóa và sổ đo. Thiếu host/capability/ownership hoặc command/OS provenance là E2; không thay bằng kết quả giả lập hay máy khác chưa chứng minh tương đương.

## tran_va_fit

Trần review theo dòng khai ADR0055/ADR0053 và protocol hiện hành, không đặt ngân sách mềm hay hỏi theo số lượt tự tạo. Lượt review1 đã dùng:1freshClaudeCode workload20min cap, actual193giây xấp xỉ (run `6cf1864b8f914db68c405be1f770c3a6`); giữ receipt/rc/snapshot. Owner cấp một lượt review1 ấy và đã tiêu; sau đó cấp thêm đúng một lượt review2, đã tiêu và terminal blocked sau286.03giây. Hai workload đều giữ nguyên, không refund. Cần quyền E2 riêng trước bất kỳ lượt Claude mới nào ngoài allowance được duyệt. Không gọi lại bằng session/prompt khác.

Prospective adoption/verification stage tái dẫn xuất, nếu được cấp lease:90phút liên tục theo protocol run cap; dự trù10 setup/ownership +15 Claude executor tái dẫn xuất correction/handoff +10 behavioral controls +20 Windows scratch checks (hai runtime,10phút mỗi lượt) +25 selftest +10 reconciliation/stop=90. Fresh Codex review H_new và mọi integration/CI không nằm trong90phút worker này và chưa có allowance; phải có admission/whole-fit riêng trước khi gọi. Chỉ dự trù, chưa cấp clock/slot; readiness, tool/auth/host-lock/namespace/currentauthority và finite fit phải đạt trước activation. Không tự gia hạn/refund. Integration/CI/native-main/M9 chưa reserve ở đây, phải có admission riêng.

## luat_dung

Theo protocol §12, ADR0060 và bảng chuyển tiếp ADR0067; không thêm soft stop/question threshold. Dừng hành động phụ thuộc nếu scope/head/spec/generation/authority/ownership/host/fit/proof sai hoặc có protected target access. Khi cần hỏi phải mang E: E1 khi hướng đã xét lại vẫn bế tắc, E2 khi thiếu hard budget/owner-only gate/máy/quyền, E3 khi bằng chứng đảo chỉ đạo owner. E4/E5 theo mục pham_vi_e. Finding spec xử ở bản nháp mới, không sửa blob đang frozen hoặc lách slot reviewer. Nội dung bắt buộc khi hỏi: E1 kèm gốc rễ, các phương án đã thử và vì sao hỏng, một đề xuất; E2 kèm mức đã dùng, còn thiếu bao nhiêu và để làm gì; E3 kèm quyết định nào, bằng chứng mâu thuẫn và hậu quả nếu giữ quyết định ấy. Theo bảng ADR0067, không dùng mã E như câu hỏi trống.

## pham_vi_e

E1: khong — có hướng sửa và phản chứng. E2: khong cho việc chuẩn bị bản nháp hiện tại; co cho lời gọi reviewer tiếp theo cho tới khi được cấp, và co nếu owner-only lease gate/budget/máy còn thiếu tại action. E3: khong — giữ hợp đồng một lần nạp và khóa thật. E4: khong trong source write set/repo-local verification; actual external Claude payload cần đúng quyền đã duyệt từng lượt, không kèm target/logs/secrets hay LIVE. E5: khong — không sửa authority/merge/lease gates hoặc danh sách cho phép. Mục sổ thực tế chỉ dùng kiem_e đủE1–E5 giá trị khong/co theo trạng thái tại action; có co không tự quyết vượt quyền.

## hinh_dang_ke_thua

Lớp A9 missing-lock mutant false negative: một phản chứng private đã tái hiện trước/sau trên Linux và Windows; chưa có vòng sửa code sau review (code1 approve). Original r40 Windows failure vẫn unconfirmed. Review1 spec changes_requested gồm S1 thiếu Packet/schema, S2 adoption/lease gap, S3 hash object ambiguity, S4 scratch-vs-committed bundle, S5 E/OID detail. Revision này chỉ sửa tài liệu để đóng các finding đó; không coi tự đánh giá là reviewer closure.

Known history giữ nguyên: WP1315authors2/reviews4; private A9author1/reviewer3; related reviews tổng7 (đo sau review3 tại 2026-11-15T06:35:20.053916+00:00). Target offline workload1 giữ riêng. Original r40 run/push/CI/native/costs/expired or closed clocks giữ; older billing/history UNKNOWN, không0. Không cộng inferred calls thành measured calls; newgeneration/Packet không reset các con số đã tiêu.

## chua_do_duoc

Root cause duy nhất của original Windows CI31/32; spec review2/closure; frozen spec/metadata pins; lease/adoption; exact-head tests sau lease; committed adapter/manifest regeneration I1; CI/connector/native-main/M9/integration/merge/postmerge/bookkeeping; actual-human/delegated audit và target current state. Không mục nào được gọi pass. Độ bền regression: bảng mutant trong repo chủ yếu biến đổi runtime nlm_cli; chưa có chứng minh rằng nó tự chặn việc xoá kiểm tra dinh[0]==1 dưới forced marker-write refusal. Verifier external phải được lưu theo hash, chạy A1 sau tái dẫn xuất dưới lease và mang theo ở handoff; không khai có regression tương đương trong repo khi chưa đo. Serving reviewer model do reviewer tự khai claude-opus-5-5 là report trong output; operator không có independent attestation nên identity receipt giữ KHONG_DO_DUOC cho actual serving model/effort và giữ nguyên raw report.

## ghi_chu_review2_va_policy_snapshot

Review2 run `74df2282d63d43b592ac2d99ca8909e1` xác nhận S1–S5 ĐÃ VÁ THẬT, nhưng overall blocked vì chưa đọc hết CURRENT-PROTOCOL.md theo prompt. Log launcher cho thấy thời gian khoảng4phút46giây, không phải timeout20phút; giữ nguyên raw claim và limitations, không refund workload. S6–S9 mức low được sửa ở bản nháp này; closure độc lập chưa có. Policy snapshot116d776 nêu trên là mốc đã cung cấp cho reviewers; trước mọi action phải resolve lại current canonical. Master `6e1047e5144ea0b013cf3cfd663dc0d9a3ada0f9` bổ sung ADR0066 và một dòng routing, chưa đổi executable admission gate; không tự kích hoạt các phần chờ packet B.

Chuẩn bị tiếp sau review2 dùng thêm policy snapshot `6e1047e5144ea0b013cf3cfd663dc0d9a3ada0f9` và public Mission/Issue readbacks. Các snapshot này cung cấp dữ liệu cho reviewer, không biến phê duyệt hướng Mission thành quyền code/CI/target hoặc đổi gate chưa land.

## xu_ly_review3

Review3 run `1e68238181954feb9ca102ff4f39b611` đã hoàn tất đủ bounded mandatory coverage, overall changes_requested: S7 dẫn đến routing conflict S10; S9 còn residual evidence-source S11; S12 là info về32hex runID. Revision này chọn default Claude executor và fresh Codex review H_new, không xin ngoại lệ routing, không adoptY dưới nhãn khác; I1 chọn bundle bo_khoa_luong evidence và giữ forced refusal external-only rõ ràng; runIDs đã tách token. Đây là proposed closure, chưa tự coi reviewer đã đóng. Allowance gộp hiện có2lượt tối đa, đã dùng1ở review3; review4 là lượt cuối trong allowance này. Không reset các workload trước.
