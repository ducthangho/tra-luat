verdict: changes_requested
reviewed_spec_sha256: 48ea894a81b776742ae7152a8ce039d1b46eee3acd0e63a67a77cce5b21effe0
reviewed_sha: b416830ef2a509d60203d55552ce17950afcf67c
reviewed_tree: 266a2aba97d925dac3ab7473dda55adb0fe23b8e
reviewed_adr0047_sha256: 4f0dd27be6fc9713c8ca56c2ff089fc8b167051431f04d8856fd56e61846baf4
model_tu_khai: GPT-6 / Codex theo chỉ dẫn phiên; provider OpenAI, execution_surface API/Codex có shell cục bộ, transport machine. Không có chứng thực độc lập build/variant/effort; không suy identity từ người đăng verdict.

# Cross-review r8 — lượt 7, lời gọi 8

**KHÔNG CÒN P1. `changes_requested` chỉ vì 2 P2: S8 ĐÓNG-MỘT-PHẦN và S10 mới. S1/S3/S5/S6/S7 ĐÓNG; S2/S4 giữ ĐÓNG; S9 ĐÓNG trong SPEC.** Không có P1 thuộc hình dạng nguồn tin cậy, cũng không có P1 ngoài hình dạng ấy. Không nâng hạng để kéo dài review, không tự mở một vòng P1 khác. Reroute PR #475 `5578460203` và bộ đếm lời gọi8 được nhận theo chỉ thị user; không tự readback API hoặc suy thành lease/kích hoạt/approval land.

S1 đã có hợp đồng đủ để executor không tự chọn nền tin cậy: producer độc lập caller/cây PR, approver có authority bền, manifest bao trùm executable/helper/runtime/trust/proxy, giữ bất biến invocation, serialization và **một** phép so neo. Giá trị runner/image, người được giao duyệt cụ thể, manifest/credential/CA/proxy production chưa có là **quyết định/facts chủ kho phải cấp**, không là finding. Câu r8 tự khai “đã đóng” được kiểm độc lập bên dưới; không dùng nó làm bằng chứng.

Bắt đầu theo user `2026-09-09T09:30:11Z`; VERDICT sơ bộ đã ghi đầu lượt rồi bổ sung. `cay-kho/` chỉ đọc, mọi task-data được đọc trong cwd, không mạng, không agent phụ, không sửa ref/commit/config của kho review. Scratch mới chỉ ở `scratch/luot7/`; không sửa script/fixture lượt6. Các kiểm tra nguồn bị cấm chỉ **MÔ TẢ BẰNG LỜI**, không dựng payload và không chạy từ harness cũ. Git env cô lập trong control chỉ phục vụ kho fixture bình thường, không đổi nguồn thẩm quyền production.

`HINT.patch` chỉ là unified diff `patch -p0` lên `SPEC.md`: **“chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm commit”**. Không có hunk gate/runtime/workflow. HINT làm rõ S8/S10 và ghi câu ADR cần đồng bộ trong cùng revision; do đầu ra chỉ được patch SPEC, **áp HINT không tự sửa ADR-0047**. Executor phải cập nhật ADR bằng phạm vi đã được cấp, ghi `hint_provenance`, review/đo lại phần mình thực hiện. Không promote ADR `Accepted` bằng review văn bản này.

Ký hiệu: **M**=`measurements.json` + `measure-r8-summary.json`; **C**=`controls.json`; **F**=`more-controls.json`; **G**=`admission-controls.json`; **P**=`partial-and-symlink.json`; **U**=`r8-controls.json`; **J**=`join-model.json`; **K**=`budget-controls.json`; **T**=`typed-memo.json`; **N**=`native-r8.json`, tất cả trong `scratch/luot7/`. M/C/F/G/P là replay harness hợp lệ đã đọc của lượt6; U/J/K/T/N dựng mới. Model/schema fixture không là implementation r8.

## Bảng finding lượt 1–6 → trạng thái

**ĐỐI CHIẾU LƯỢT TRƯỚC.** Hạng ở cột thứ hai là hạng lịch sử, không phải số finding còn mở. “ĐÓNG” là kết luận hợp đồng của bản đặc tả, không phải công nhận mã chưa viết đã đạt nghiệm thu.

| ID lượt6 | Hạng cũ | Trạng thái r8 | Bằng chứng độc lập / phần còn lại |
|---|---|---|---|
| S1 adapter-environment-boundary-is-not-specified | P1 | **ĐÓNG** | SPEC242–278 và ADR35–69 đủ producer/approval/manifest bất biến + actual execution/trust identities + digest so một lần. F.profile khớp hằng `0b756e06…`⇒0. Không chứng nhận profile production; khác biệt câu chữ ADR thuộc S10 P2, không phải execution closure bị bỏ sót lần7. |
| S2 raw-object-read-does-not-verify-content-identity | P1 | **ĐÓNG** | Q4.5 tiếp tục băm actual type/size/body, lấy cạnh từ bytes đã băm, không đọc lại tên ref. M đọc scan và parent closure; C/G/P/T kiểm routing/pinning/missing/type. Chưa chạy bytes lệch OID theo phân công. |
| S3 a6-single-mutant-is-shielded-by-cli-flag | P1 | **ĐÓNG** | A6:480–490 tách đúng ca/seam. C positive routing0→12; thiếu routing12→12 SỐNG; model trong-miền-khác-neo12→0; ngoài-miền12→12 SỐNG. Không còn nhận công kill ở ca bị che. |
| S4 q13-selected-mode-conflicts-with-a5-and-ready-fields | P1 | **ĐÓNG** | Q3/Q12/Q13 vẫn đúng union policy/ngoại lệ/không neo; F closure11/0/11/12, claims[]8; U có schema metadata để policy fixture thực sự biểu diễn được. |
| S5 m9-check-publisher-consumer-is-unspecified | P2 | **ĐÓNG** | M9:410–447 khép join suite/run/attempt job/check_run_url/artifact ID, quyền đọc, retention, journal và thứ tự consumer trước bootstrap. J19 ca, positive0/âm12; đây là đường API ĐỀ XUẤT, không canary thật. Thiếu facts⇒giữ đóng, không executor tự nới association. |
| S6 q13-exception-scope-and-retirement-are-not-bound | P2 | **ĐÓNG** | Q3:193–223 ghim repository/expiry/activation binding, first-policy hash, draft S, immutable marker, policy hiện tại qua binding mới. U descriptor/activation0/12/12; B→B2 mới0/cũ12; B→D12; drift trước/sau admission tách rõ. |
| S7 retirement-file-conflicts-with-ledger-schema | P1 | **ĐÓNG** | M1/M4:449–454 dispatcher đúng một path reserved, sáu khoá100644, metadata không phải lease/Q2. U revocation M1=0, metadata Q13=0; missing/broken/mode/near-name12; sửa/xoá marker cũ8. Không còn mâu thuẫn “có tệp cũng chết, thiếu cũng chết”. |
| S8 object-store-layout-and-resource-contract-is-open | P2 | **ĐÓNG-MỘT-PHẦN** | Bare/linked/pack/alternates/partial/shallow và typed memo có lời giải, control xanh/đỏ đúng. Tám trần có đơn vị/đề xuất, nhưng `max_tree_or_alias_edges` chưa định nghĩa phạm vi đếm; K cây rộng cho hai quyết định0/12. Xem finding. |
| S9 reroute-accounting-is-stale | P3 | **ĐÓNG** | §0/Q14/ngoai_pham_vi/hinh_dang_ke_thua đã ghi reroute tới hếtP1, khôngreset, lần6 hình dạng. Những đoạn “4 lần”, “tận cùng” còn lại được đánh dấu lịch sử bị bác. ADR mở đầu kể bối cảnh5 lượt, lớp2 bổ sung lượt6; không lấy đó làm số hiện tại sai. |

| ID lịch sử | Hạng | Trạng thái r8 | Căn cứ đọc/rerun lượt này |
|---|---|---|---|
| R1 canonical-url-check-does-not-bind-transport | P1 | ĐÓNG | S1 đã đóng hợp đồng; endpoint ghim, profile độc lập; G control nguồn nội bộ0. Hướng helper/rewrite chỉ mô tả. |
| R2 replace-refs-bypass-oid-pinning | P1 | ĐÓNG | Repo tạm không ref/no-replace/raw verified graph; không dựng replacement. |
| R3 bootstrap-gate-trusts-pr-and-arrives-too-late | P1 | ĐÓNG | A0 có M9 + audit ngoài cây PR + freeze + consumer trước bootstrap; không dùng test PR cấp quyền. |
| R4 inactive-a0-already-changes-lease-decisions | P1 | ĐÓNG | Q3/Q5 giữ verdict cũ/DU_BAO; U metadata-only inactive0, revocation inactive12. |
| R5 admission-head-is-not-the-landed-candidate | P1 | ĐÓNG | M9 strict S/H/T, current base/head, tree(M), queue chặn. J không thay canary thật. |
| R6 self-declared-effective-set-shrinks-exclusion | P1 | ĐÓNG | Q3 không tin EWS tự khai; F claims_empty8. |
| R7 symlink-resolution-lacks-source-and-termination-contract | P2 | ĐÓNG | P cùng lease blob ở hai OID, alias→docs/a.md và other/a.md, hợp cả hai; vòng/thoát chỉ đọc. S8 là đơn vị budget mới. |
| R8 cutover-delta-and-fixed-g2-smoke-conflict | P1 | ĐÓNG | Q6 phân loại delta; C=null, g3 riêng; clock mới toàn bộ hết hạn, không assert g2 cố định. |
| R9 a8-mode-case-cannot-kill-stated-mutant | P1 | ĐÓNG | G đúng8/only-new8 SỐNG/combined0 ĐỎ; full-T unit12. |
| R10 spec-review-label-does-not-waive-review-cap | P1 | ĐÓNG | Reroute user cấp, lời gọi8, khôngreset; không tự mở vòng sau. |
| N1 canonical-remote-identity-unbound | P1 | ĐÓNG | S1/R1; không còn authority từ tên origin. |
| N2 snapshot-pinned-after-unverified-recapture | P1 | ĐÓNG | G map capture trước, stale12, ref đổi sau vẫn dùng OID cũ. |
| N3 admission-workflow-does-not-cover-canonical-updates | P1 | ĐÓNG | M9 mọi PR vào default, không filter path/author/rc9, edited, no queue. |
| N4 canonical-checker-bootstrap-is-circular | P1 | ĐÓNG | A0 bootstrap riêng; canary PR child S tạo được trong U khi canonical đóng; command nền rc2 chỉ phản ánh chưa có implementation. |
| N5 effective-write-set-and-symlink-resolution-missing | P1 | ĐÓNG | Q3 closure/occurrence + Q13 đã chốt; F/P/U. |
| N6 historical-cutoff-revives-feature-holders | P1 | ĐÓNG | Mốc phải readback sau A0; Q6 cutover có điều kiện; không lấy master hiện tại làm mốc đã cấp. |
| N7 candidate-map-omits-entry-mode | P1 | ĐÓNG | G và U map(mode,type,blob) chặn mode cũ8. |
| N8 record-lease-guard-has-no-candidate-id | P1 | ĐÓNG | Q5/A10 ID ứng viên, năm cửa; AST nền1/1/0/0/0. Không khai đã chạy state-machine r8. |
| N9 acceptance-prepublish-and-second-parent-contradictions | P1 | ĐÓNG | Q3 tách pure/CLI; F S cha2 giữ0/mất8. |
| N10 authorization-json-and-url-contract-is-open | P2 | ĐÓNG | Q2 đủ URL/envelope/đúng6keys/types/duplicate/error order; không có raw API thật. |
| N11 readback-after-admission-lifecycle-undefined | P2 | ĐÓNG | Q2.3/M9 trước canonical kiểm lại, sau canonical không gỡ event khi artifact/comment mất. |
| L1 authority-signature-evidence-false | P1 | ĐÓNG | M mỗi commit1gpgsig; b416830PGP,6635379SSH; không suy signer/actor. |
| L1 default-ref-is-untrusted-cache | P1 | ĐÓNG | G main thắng master + S1 khép profile; không chứng nhận freshness server thật. |
| L1 standalone-revocation-has-no-admission-gate | P1 | ĐÓNG | M4/M9 luôn admission, không phụ thuộc lease hoặc rc9; S5 khép interface. |
| L1 evidence-mention-is-not-an-authorization | P1 | ĐÓNG | Q2 bắt exact authorization block, không prose/substring. |
| L1 write-set-exclusion-is-incomplete | P1 | ĐÓNG | Q3 mọi lease, closure/prefix/occurrence; F/P; lifecycle S6/S7 đã đóng. |
| L1 snapshot-check-does-not-fence-writers | P1 | ĐÓNG | Q11 tuần tự stop→g3→readback→start; fencing land còn nợ có tên. |
| L1 reads-are-not-pinned-to-one-snapshot | P1 | ĐÓNG | G pinned OID, M verified graph; một map/clock. |
| L1 legacy-fallback-conflicts-with-ledger | P1 | ĐÓNG | Q3 precedence/history/chiều ngược, Q6 cờ/delta. |
| L1 append-only-check-misses-candidate-and-merges | P1 | ĐÓNG | F/G merges+mode, U marker; whole namespace dispatcher. |
| L1 packet-loop-guard-is-partial-and-boolean | P1 | ĐÓNG | Q5/A10 năm cửa/3state/targetID/idempotence/bytes state, giữ hạng lịch sử đã đóng; S10 chỉ làm rõ biên rc ADR. |
| L1 acceptance-confuses-refs-blobs-and-mutations | P1 | ĐÓNG | F3cặp/4ref và1cặp/3ref; G A8; C A6 sửa đúng S3. |
| L1 revocation-schema-and-error-contract-incomplete | P2 | ĐÓNG | M1 r3 recovered đúng hash, đọc schema trực tiếp; U kiểm dispatcher metadata mới. |
| L1 size-estimate-and-slice-anchor-are-stale | P2 | ĐÓNG | M409/368/328; r8 gọi825–1195 là ước trước vá, bắt ước lại trướcready, không giả numstat mới. |
| L1 ready-and-rollout-decisions-are-not-closed | P2 | ĐÓNG-MỘT-PHẦN | Các lifecycle/joins cũ đã khép; còn S8/S10 và facts triển khai đã khai. Không cộng đúp alias này. |

## Findings mới

### S8 — object-store-layout-and-resource-contract-is-open · P2 · tiếp diễn

**Vị trí:** SPEC312–321, đặc biệt `max_tree_or_alias_edges=128` và câu “depth là số cạnh”; A6:491–492; Q12. **Độ tin cao về mơ hồ đơn vị**, không phải một bypass đã chạy.

R8 đã giải quyết phần lớn S8: API giải object directory thay ghép `.git`, read-only layout, loose+pack, adapter quản alternate, missing partial⇒12, chuẩn bị trước snapshot, shallow⇒12, memo expected type. Tám con số được gắn nhãn **ĐỀ XUẤT**, nên không có finding vì chưa benchmark chúng như số production.

Câu còn thiếu là **`max_tree_or_alias_edges` đếm trên toàn snapshot, một root, một occurrence hay từng đường lookup/resolve? Có tiếp tục cộng sau symlink restart không?** `max_parent_path_edges` ít nhất nói “path”; tên tree/alias không nói phạm vi, câu “depth là số cạnh” chưa nối nó vào một counter cụ thể. Hai executor có thể chọn hai miền đầu vào khác nhau mà cùng gọi là128edges.

K dựng Git thường với129 thư mục anh em, mỗi thư mục có một tệp: tổng258 tree edges, đường dài nhất2edges. Diễn giải tổng snapshot⇒12; diễn giải depth mỗi lookup⇒0. Đây là **counter oracle/model trên graph thật**, không nói code r8 đã chọn sai. Nó chứng minh P2 “executor phải tự quyết”, không chứng minh fail-open/P1. Hợp đồng hash/cạnh S2 vẫn đúng ở cả hai cách đếm.

**Vá ở đâu/cách vá:** Q4.5 chọn rõ phạm vi. HINT chọn128 là số bước tree-entry + dereference cộng dồn trên **một resolve tại một occurrence OID**, kể cả restart; width chịu unique_objects/total_bytes/deadline. Định nghĩa root0, alternate-store phân biệt ngoài primary, alternate-depth theo đường và xử cycle/đường trùng; budget được giữ bởi adapter/parent reader, không đòi cat-file xuất sẵn mọi counter.

**Ca khoá:** cây129 sibling phải có expected rõ; chuỗi alias tại bound; từng bound−1/bound/bound+1 với chốt khác hợp lệ; cùng store tới bằng hai đường không che đường sâu. K đã dựng alternate3/4/5: Git thực đọc được0/0/0, adapter profile model depth4⇒0/0/12 — có ca thật để bắt mutant bỏ depth, không bị native Git che ở đây. K cũng dùng child Python bình thường im lặng1s: parent với deadline0,1s dừng ở≈0,102s, reader12. Đó là chứng minh phương pháp timeout khả thi, **không phải benchmark60s trên Git production**.

**Hệ quả:** lựa chọn total-vs-path đổi miền chấp nhận; phải đóng vào profile/spec_hash trước ready, không nới bằng caller. Các ngân sách không đo hết từ cat-file, nhưng đều có thể đo từ **adapter + parent reader**; không có căn cứ nói `max_reader_wall_seconds` bất khả thi. `readline/read/wait` blocking vô hạn rồi mới kiểm giờ là implementation sai hợp đồng, chưa phải lỗi đã thấy trong mã r8 chưa tồn tại.

### S10 — adr-spec-interface-boundaries-are-not-aligned · P2 · mới

**Vị trí:** ADR-0047:19–22,48–65,76–82,94–96 đối chiếu SPEC:195–200,250–277,317–319,335–341,449–454,A10. **Độ tin cao về chỗ cần làm rõ; không báo là fail-open.**

Có thể hiện thực đúng fail-close bằng reader error12 rồi wrapper packet_loop trả8. SPEC Q5/A10 và M1 r3 đã cho interface cụ thể, nên tôi **không** gọi A10 bất khả thi và không nâng thành P1 “mâu thuẫn luật”. Nhưng ADR liệt kê cả guard packet_loop rồi viết mọi cổng ĐỎ `(rc=12)` mà không nói đây là mã reader; implementation theo một trong hai tầng sẽ ghi receipt/expected khác. AST nền tại `.claude/dev/packet_loop.py:60` xác nhận `RC_STATE=8`, không phải giả thuyết.

Các biên cần đồng bộ trong cùng nhóm:

| Câu ADR | Câu spec | Mạnh/yếu và cách đọc cần chốt |
|---|---|---|
|19–22: mọi cổng, gồm guard packet_loop, rc12 |Q5/A10/M1: lỗi guard→RC_STATE(8) |ADR gộp hai interface; phải ghi rc12 nội bộ reader/lease_publish, public packet_loop8, giữ diagnostic gốc. Cả hai đều fail-close nên không tự là P1. |
|82: “chạm trần ⇒12” |319: “Vượt bất kỳ trần…⇒12” |Nếu hiểu literal, ADR mạnh hơn ở đúng bound. Với path4edges và bound4 đã tớiS, oracle `>=`12 và `>`0 khác nhau. Ghi inclusive cho count/bytes/depth; timeout mô tả việc đã hoàn tất/chưa hoàn tất tại deadline, không dùng một câu chung mơ hồ. |
|94–96: bất kỳ field YAML/Issue “chỉ được so…lệch⇒8” |Q3: claim EWS lệch8; descriptor/binding nguồn không xác minh được12; write_set/time vẫn là input khai báo |ADR viết quá rộng về field và mã lỗi. Khoanh **claim phái sinh không được thu hẹp**; nguồn/activation lỗi theoQ13, rồi wrapper mapping. Không biến input khai báo thành phái sinh không có producer. |
|49: approver là chủ kho |250–251: chủ kho/người uỷ quyền bền |Spec nói rõ trường hợp delegation mà ADR chưa nói. §2 protocol cho uỷ quyền bền/có phạm vi; không suy executor được tự duyệt. Đồng bộ cụm vai trò, không cần tự chọn một cá nhân thật. |
|61: JSON UTF-8 chuẩn hoá/sort_keys |271: thêm separators/schema_version cụ thể |ADR ít chi tiết hơn, **phù hợp** vai trò bất biến/spec chi tiết. Không phải thêm phép so thứ hai; không finding riêng. |
|76: alternates “chỉ qua” env adapter |293–295: còn kiểm info/alternates và bắc cầu Git tự đọc |Đọc ADR là hạn chế nguồn cấu hình caller; spec làm rõ store metadata phải được kiểm. Không suy đặt env là tắt info/alternates. Đây là chi tiết đã khép trong spec, không mở lại S2. |

**Vá ở đâu/cách vá:** HINT thêm một mục đồng bộ ADR và assertion boundary ở A10/A6; ghi nguyên câu cần thay ở ADR. ADR giữ bất biến “unknown làm cổng đỏ”, source authority độc lập và claim không thu hẹp, còn interface/error code và counter ở spec. Không sửa `RC_STATE`, không áp blanket8 lên metadata/nguồn12, không đổi workflow thành pass khi missing.

**Ca khoá:** reader unknown12→cả5 entrypoint packet_loop8, state byte-match; mutant trả thẳng12 phải làm assertion A10 đỏ. Parent witness kết thúc đúng bound phải có cùng oracle hai tài liệu. Q13 descriptor mismatch12 khác EWS claim mismatch8; U đã kiểm nhánh descriptor/binding12, F EWS8. K ghi hai oracle boundary để chỉ rõ chỗ khác, không nhận model ấy là test sản phẩm.

**Hệ quả:** cần sửa đồng bộ cả tệp ADR Proposed khi điều phối chuẩn bị revision. Không cần thêm quyết định nền nào được tin để sửa những câu này. S10 là thiếu phân định interface/counter trong hai văn bản, **không phải lần7** của hình dạng nguồn tin cậy và không làm S1 mở lại ở P1. Không phát hiện xung đột mới với luật Accepted §3.2/§4/§5/§8/§12 hoặc ADR-0025/0028/0044.

## Phản chứng đã chạy lại + mới

Các lệnh chạy từ cwd với `PYTHONDONTWRITEBYTECODE=1`. `replay.py` đọc source cũ đã kiểm, compile trong module đặt HERE sang `scratch/luot7/`; không chỉnh sửa script cũ. F dùng lại **JSON trơ nguyên byte** của fixture approved cũ để so hằng trong mã; các path bên trong chỉ là chuỗi, không mở những path đó. C.profile khác F: C tự tạo fixture anchor để kiểm serialization; **F** mới là control khớp hằng độc lập, không trộn hai mức chứng cứ.

| Lệnh/harness | Đã đo | Giới hạn |
|---|---|---|
| `python3 scratch/luot7/replay.py measure controls more_controls admission_controls partial_and_symlink` | Tất cả completed/rc0; M counts/raw graph, C routing/layout/memo, F cardinality/profile/parent2, G map/mode, P partial+symlink | M/F sửa phạm vi numstat sang merge-base→PRhead như lượt6; kết quả tip-to-tip ban đầu giữ riêng, không làm claimPR. C metadata/M9 đời r6 chỉ là replay lịch sử, kết luận r8 dùngU/J. |
| `python3 scratch/luot7/r8_controls.py` | **22/22** admission assertions; unit revocationM1=0/metadataQ13=0; binding0/12/12; bare0 | Git commit/blob/mode thật; dispatcher và policy validator là model (policy schema fixture tối thiểu), không full parser/consumer r8. |
| `python3 scratch/luot7/join_model.py` | **19/19** assertions: positive paginated0; wrong suite/pages/job URL/attempt/artifact ID/missing/expired/duplicate/file/app/event/association12; hai giả thuyết SHA tách riêng | API ĐỀ XUẤT, không có raw GitHub canary. jobID404≠checkID101. Không nhận run_id trong receipt làm thẩm quyền; no UI URL parse. |
| `python3 scratch/luot7/budget_controls.py` | Alternate3/4/5 real Git đọc0/0/0, model giới hạn0/0/12; wide tree258edges/depth2; subprocess im lặng bị deadline dừng | Counter bound lớn còn là seam/model, không dựng đủ50.000objects/128MiB hoặc chạy60s production. |
| `python3 scratch/luot7/typed_memo_control.py` | Explicit memo `(expected_type,OID)`: blob0, cache-hitblob0, cùngOID yêu cầu tree12 | R6 raw reader cũng so actual type ở cache-hit; facade làm key tuple tường minh. Không bịa collision hay hai object hợp lệ khác type cùngOID. |
| `python3 scratch/luot7/native_r8.py` |4path holder0/rc0; g2 hết hạn8; command mới2; doc-claims0/ok:true; doctrine cóSPEC8tệp/0 | Clone mới của **base**, không phải implementation r8; không chạy toàn bộ suites có ca ngoài phân công. |

**Catalog A6 yêu cầu chạy lại:**

| Ca | Bản đúng | Mutant | Credit |
|---|---|---|---|
| Routed positive Git commit/tree/blob |0/0/0|Bỏ routing12/12/12|ĐỎ thật ở positive; C |
| Đầu vào đã thiếu routing |12|Bỏ routing12|SỐNG; C, Git rc0/missing |
| Profile trong miền nhưng khác neo |12|Bỏ phép so profile0|ĐỎ ở predicate model; C |
| Profile ngoài miền |12|Bỏ phép so profile12|SỐNG, domain validator che; C |
| F.profile đổi thứ tự key, khớp hằng |0|Không đột biến|Control serialize/compare; dữ liệu trơ |
| Bỏ env/cờ no-replace khi source không có replacement |0|0|SỐNG, không nhận công; hướng source replacement không chạy |
| Bytes mismatch sau cat-file/trước hash |not_run|not_run|Chỉ mô tả theo phân công, không dùng lỗi Git trước seam làm kill |

**Control S7/S6 mới trong U:** first policy+marker+revocation0; metadata missing/broken/wrongmode/missingkey/extrakey/boolversion/duplicate12; đúng hai tên gần reserved yêu cầu vẫnM1⇒12; sửa/xoá/đổi mode marker đã ởS⇒8; B(P1,R1)→B2(P2,R1) sau binding mới0, bindingcũ12; B→D12. Metadata-only khi inactive0; revocation thật inactive12. Các schema metadata có **đúng sáu** khoá và regular100644 trong ca positive.

**Bốn hướng r8 cần phân tích thêm:**

1. **`base_sha_before_add == S`: không phải so với mọi S về sau.** Q3:212 mở nhánh “S chưa có marker và policy vắng”; chỉ nhánh first admission so213. U: S0/H0 hợp lệ0; một commit canonical khác chen vào, PR cập nhật theoS1 nhưng giữ marker draftS0⇒12 **đúng vì stale**; sửa marker draft sangS1⇒0 (S1 chưa có marker nên không phạm append-only). Sau khi marker canonical, PR sau giữ nguyên marker⇒0 dù S mới khác `base_sha_before_add`. Nếu executor so lại trường đó với mọi S thì đó là bug trái nhánh transition, không là yêu cầu r8. Không có phản chứng từ drift làm marker đã nhận bị8/12 oan theo hợp đồng đã đọc.
2. **Descriptor ghim A1 kiểm được marker đến nhiều ngày sau.** Hằng ghim digest **descriptor**, không phải blob/hash marker tương lai. Khi first policy tới, lấy policyT, S hiện tại và descriptor đã biết để so; H/T containing marker nằm ngoài cây trong receipt. U tạo marker sau commitS và vẫn0. Không có yêu cầu fixed-point hash hoặc biết trước policySHA/markerblob ở A1. Policy tới giữa A0/A1 khi neo chưa đủ phải12 hoặc revision/bootstrap; không tự nhận từ câyPR. Q13 đã chọn lối không cần policy trướcA1.
3. **Bỏ dispatch không làm canary S≠H bất khả thi.** Sau A0 land trong khoảng canonical đóng, tạo/mở PR thường cóH là descendant củaS, revocation-set rỗng, event `pull_request_target`; tạo PR/ref không cập nhật canonical. U dựngS≠H đúng ancestry/tree và inactive0. M9 còn CLI chẩn đoán `kiem-thu-hoi-github` và rerun attempt của eventPR đã xác minh; chẩn đoán ngoài lane không tạo required pass. GitHub association thực vẫn chưa đo, nhưng không thiếu đường tạo candidate/event về mặt hợp đồng.
4. **Proxy precedence — chỉ mô tả, không probe.** Theo cơ chế Git/libcurl thông thường, `http.proxy` cấu hình tường minh được Git truyền thành proxy option, có ưu tiên so với env proxy; khi không có option tường minh, libcurl chọn env theo scheme, dạng lowercase `https_proxy` ưu tiên dạng uppercase khi cùng có. Không có source Git/libcurl/API tương ứng trong bundle để chứng nhận phiên bản implementation này; không mạng/không đọc tài liệu hệ thống ngoàicwd. Kết luận hợp đồng không phụ thuộc giả thuyết thứ tự ấy: r8:267–268 **không chọn env đè config**, mà yêu cầu mọi cấu hình có mặt quy về cùng giá trị ghim và từ chối xung đột trước thực thi. Env dựng rỗng, không mang NO_PROXY/ALL_PROXY ambient vào. Vì vậy chưa có căn cứ báo r8 “bắt ngược chiều ưu tiên”. Giá trị proxy/CA/image/token thật vẫn là fact chưa có, không lấy F.profile làm transport control production.

**CHỈ MÔ TẢ / not_run:** fake remote helper; remote.<x>.vcs; URL rewrite sang kho khác; replacement/graft; env/executable đổi nguồn; bytes cache lệchOID; helper/runtime/CA giả; đường thoát cây; đồng tự Unicode; chuỗi thoát. Không chạy harness nào dựng các hướng ấy. Không Internet/GitHub/credential reads hoặc probe transport thật. Ma trận nguồn âm của A2/A6 do điều phối cung cấp, không được đánh passed từ lời mô tả.

## Tiêu chí A1–A12

| Tiêu chí | Đơn vị / phép đỏ thật | Đánh giá r8 |
|---|---|---|
| A1 |Cặp(blob,path) cho dòng; leaseID cho holder; occurrence choMAP_REF; known-list mutant bỏ blob3 |F thực có3cặp/4ref, 1blob ngoài known; model3dòng→2 và holderY→X/Y. Có phép đỏ; smoke∅/{g2} theo clock, không bắt g2 sống. |
| A2 |1cặp/3ref; server default/name+OID/profile; bỏ authority source seam |F1/3; G main/master/map xanh. Nguồn âm/helper chỉ mô tả. S1 hợp đồng đủ; không cấp credit kill cho negative chưa chạy. |
| A3 |Năm mã r3=8/0/8/0/8; cặp lịch sử đúng mốc; product inactive vsDU_BAO |Đọc r3 recovered đúnghash. Hai cây mốc có phép đỏ mutant lấy cây sau; inactive áp sớm phải đổi verdict. Không chạy lại5case sản phẩm lượt này. |
| A4 |Chiều ngược ledger/history, có/không replacement; đối chứng sống0 |Hai nguồn có thể tắt riêng để đổi8→0; không thấy chốt phủ làm mất phép đỏ khi fixture tách nguồn. Chỉ review hợp đồng, chưa N/N mới. |
| A5 |Closure/exact/prefix/alias từngOID/claim; pure vsCLI publish exactpair |F policy11/ngoại lệrời0/giao11/noanchor12/[]8; P đa occurrence; U policy+marker biểu diễn hợp lệ0. S7 không còn làm nhánhpolicy bất khả thi. Các hướng vòng/thoát/Unicode không chạy. |
| A6 |Routing/profile/raw object/graph/pinning; mỗi seam+oracle; E2E3cặp xen kẽ |S3 đóng, catalog phân biệt đúng ĐỎ/SỐNG. C/G/P/T và K layout/deadline/alternate. **S8/P2 và S10/P2** cần làm rõ scope/biên; không có cơ sở bảo whole A6 đãpass hoặc ratioE2E≤2. |
| A7 |Từng constraint M1/reserved, mode/type, 0/4/8/12; qua consumer |U positive0, âm metadata12, near-name12, inactive revocation12. Full inherited M1×consumer chưa chạy. `raise→continue` phải so verdict cuối; không dùng sốcase thay bằng chứng. |
| A8 |Map(path,mode,type,blob), toànT, ancestry/parent2; S/H/T exact |F parent2 giữ0/mất8; G mode8/8/combined0, full-validator12; U metadata first0/mutate8/B2new0/D12/drift-rebind. Chọn mutant mode đúng. |
| A9 |Stateful API endpoint/ID/calls; readback mọi lần trước canonical, sau0 thêm |Q2/M9 và r3 rõ; không còn đảo hiệu lực khi căn cứ/artifact lịch sử mất. Không chạy ma trậnQ2/API thật lượt này. |
| A10 |5entrypoints×4 trạng thái; candidateID/idempotent event/bytesstate; RC_STATE8 |Q5 đủ oracle. AST nền thiếu3guard là phép đo hiện trạng, không nghiệm thu code chưa có. ADR cần ghi biên reader12→CLI8 (S10P2), không đổi interfaceA10 hoặc nhận source-error12 như CLI8. |
| A11 |Base/candidate cùng lệnh, têncase/delta/actualworkflow; canary rawS≠H |N doc/doctrine xanh; full121/121,278/278+81mutant không chạy. J/U chứng minh model/join/candidate có thể dựng, chưa chứng minh Actions/token/workflowSHA. Raw thiếu⇒False và giữ đóng là đúng, không điều kiện impossible-green. |
| A12 |Catalog expected neo ngoàiPR; registered/executed/pass/fail/skipped/not_run; credit tại seam |F catalog độc lập bắt mất invocation và mất cảregistration+invocation. R8 không nhận công lỗi trước seam. Chưa có product catalog/count để nhận toàn bộ mutants. |

### Nhất quán luật và kích thước slice

| Nguồn luật | Kết luận |
|---|---|
| §3.2 / ADR-0025 |Issue/spec_hash/revision/generation/phái sinh trướcready; thay dependency/profile/policy kéo revision. Không cấp lease từ reviewer hoặc descriptor chung. Q13 không miễn ready packet khác. |
| §4 / ADR-0028 |Q5/Q11 giữ stale/stop/generation/lastSHA/retention. Journal bền khác artifact có hạn; cleanup sau final hash readback. Không coi snapshot là fencing. |
| §5 |Policy→closure và pause/re-evaluate/binding mới; symlink theo occurrence. Ngoại lệQ13 đã được chủ kho chốt, không bắt chọn lại policy trướcA1. |
| §8 / CLAUDE.md |Review read-only/exactsha, hai trục spec+standards, so mutant với oracle độc lập. HINT provenance đã nêu; chỉspec, không reviewer sửa authoritycode. Suites không chạy không thành pass. |
| §12 |Lời gọi8 theo reroute đã giao, khôngreset/call mới. Không cònP1 nên không tự yêu cầu một vòng reviewP1 tiếp. Hình dạng nguồn vẫn6lần lịch sử, không cộngS10 thành7. |
| ADR-0047 Proposed |Ba lớp và governance S1 đủ, hash/cạnh S2 đủ; các interface/counter rộng hơn spec cần đồng bộS10. Không nhận Accepted/47cổng từ việc thêm văn bản. |
| ADR-0044 |A0 3path,+560–780 cũ; A1 3path,+90–160; B2path,+160–240; C1path,~15;6path duy nhất. A0 vượt300 đã khai phạm vi/lý do, Q7 cần chốt. MốcPR409/368/328 đo đúng; PR250 làspec, không lấy nó làm độ lớn code tương đương. |

**Ước A0 chưa đủ cơ sở coi còn đúng cho r8.** Schema metadata/transition + deployment manifest verifier + suite/attempt/artifact join làm scope tăng; không có implementation numstat để ước lại chính xác. R8:372 đã gọi825–1195 là **tổng trước vá lượt6** và buộc ước/đo lại trướcready, nên không báo lời khai sai hoặc giữ finding kích thước cũ mở chỉ vì chưa có số mới. Phép cộng560+90+160+15=825,780+160+240+15=1195 đúng. Consumer dependency là packet ngoàiwrite_set, không giấu vào6path hay tự mở A0 thành4path. A0/A1 cần predecessor đãcanonical ở nơiM9 đòi; integration-only không thay bootstrap trust. Native suite/gate số lớn trong EVIDENCE không là số đã chạy lại.

### Q7–Q14

| Câu | Phần bắt buộc/đã chốt | Còn thiếu đúng bước |
|---|---|---|
| Q7 |A0→A1→B→C, spec/Issue/lease/acceptance riêng; consumer trước bootstrap |Chủ kho chốt ngoại lệA0/biên audit; cập nhật ước dòng thật trướcready. Không hỏi lại thứ tự dependency đã được r8 quy định. |
| Q8 |C là lệnh r2 **không đích**, g3 riêng |Object Issue comment có đúng authorizationJSON của chủ kho chưa có; reviewer không tạo lệnh. |
| Q9 |Đặc tả khuyến nghị nhận revocation lease hết hạn, không tái dùngID |Quyết định chủ kho chưa có trong bundle. Hết hạn nay không làm C tự biến thành vô nghĩa hoặc đổi thành gia hạn. |
| Q10 |Thiếufacts⇒False; actualS/H/T/strict/queue/bypass/profile/consumer/canary/closure/delta/journal |Canary raw đúng token và profile deployment thật, ruleset/retention, audit/freeze/readback; không dùng controlmodel làmfacts. |
| Q11 |C→stop+lastSHA/state→g3check/land/readback1→start |Facts C/stop/g3; không có quyền reviewer thực hiện land/fencing. |
| Q12 |Hợp đồng trướcreadyA0, giá trị từng slice trướcready/kích hoạt; producer phái sinh có authority |S8 counter scope, S10 đồng bộADR; profile/budget/activationbinding thật ở bước tương ứng. Không bắt chạy implementation mới trước lease viết nó. |
| Q13 |**ĐÃ CHỐT(ii)** theo5575587924; ngoại lệ raw+symlink tới first policy, khôngEWS tự khai; marker firstpolicy giữ nguyên |Bodyhash/authority readback thật + activation context chưa đo. Hợp đồng transition r8 đủ; không hỏi lại chọn(i)/(ii), không tự grandfather policy trướcguard. |
| Q14 |**ĐÃ CHỐT** tới hếtP1, khôngreset, call8 |Không cònP1 ở lượt này. HaiP2 không tự gia hạn một cuộc reviewP1. Việc Issue/lease tiếp theo thuộc điều phối, không thuộc reviewoffline. |

## Bảng đo lại

Map hiện tại bằng **từng tên/OID** với `scratch/luot6/refs.json`. Đây là map frozen mirror, **không phải** advertisement mới của server. Mirror thiếu nhánh mới #482/#483 theo EVIDENCE; không fetch lại. Phân loại ở clock quá khứ dùng bytes hiện có, không phải đã quan sát server tại giờ ấy.

| Đại lượng | Đo lượt7 | Đối chiếu/giới hạn |
|---|---|---|
| SPEC / bản untracked trongcay-kho |48ea894a81b776742ae7152a8ce039d1b46eee3acd0e63a67a77cce5b21effe0 |Byte-match,594dòng; không review nhầmr6/r7 |
| VERDICT6 / HINT6 |9090aadd34f34ea6607bae2e55cd87daffd2f1f43a2df10b2190b4db4e8d7db8 /47fbf8cba3265a8f4ad285d03f1fe21136a0c7edff01bc5155959501b05fb84c |Khớp bàn giao |
| HEAD / tree / abbrev / shallow |b416830ef2a509d60203d55552ce17950afcf67c /266a2aba97d925dac3ab7473dda55adb0fe23b8e /7 /false |Detached; chỉ2tệp untracked được giao (SPEC vàADR) |
| origin/master |585c7d510e026b4ea5a2b395c69581f24c1d8fa0 |48commit saubase; không phải mốcA0 đãland |
| Ref theo công thức spec |310=309remote+1local;306tipphân biệt |Map đúng lượt6; không claim server hiện có309 |
| Cặp/path/leaseID/IDđablob |288/273/273/7 |Không đổi |
| Clock07-09 13:41 /14:33:15 /08-09 03:12:57 |Còn hạn/chưa tomb8/4;7/3;6/3 |Khớp lịch sử trongM |
| Clock08-09 03:37:33 /09:52 /10:17:12 |5/3;1/1;0/0 |Clockfixtures; không là receipt sauC |
| **Clock09-09 09:30:11 lượt này** |**0ID/0cặp còn hạn;0chưa tomb** |Không chép6/3 thành hiện tại |
| r2 blob26f07b4 /fdfde3a |9ref/1ref |KhớpL5r8 vàverdict6 |
| #456 blob8b2103c /1f95042 |14ref/5ref |KhớpL5r8 vàverdict6 |
| Tomb tạibase /H02b0b86 /master585c7d5 |7/11/11 |#468 vào master, không gọi base7 là master hiện tại |
| base…H02b0b86 |0trái/31phải |Khớp31commit riêng; không phải witnesslength |
| Gpgsig b416830 /6635379 |Mỗi commit1;PGP/SSH |Không xác minh keyring/actor/human signer |
| planned: lease |3ID, đều hết hạn |KhớpM/claim cũ |
| `kiem→_lease_cham_duong` / schema helper5cửa |0 /1,1,0,0,0 |AST nền, chưa guard mới |
| Policy/schema/sổ/workflowadmission tạibase/master |Đều vắng |R8 chỉspec, không có product implementation |
| Native4pathwp461 /checkg2 |Cả4holder0/rc0;g2rc8 |G2 bytes nguyên từ ref, stderr báo hết hạn; khác lượt6 do clock, không regression |
| Nativecommandmới |rc2 invalidchoice |Không có command trongbase |
| Doc-claims strict |rc0,ok:true,70.861stdoutB |Nativebase/core.abbrev7; không đồng nghĩa toàn bộ advisory biến mất |
| Doctrine vớiSPEC |rc0,8tệp,0chỗchép |Không thay canary hoặc chứng minh logicADR đồng bộ |
| PR250/275/248 merge-base→head |+409/−0;+368/−0;+328/−1 |Base/head/per-file trongM; không dùngtip-to-tip |
| Ước trướcvá A0/A1/B/C |560–780/90–160/160–240/~15;825–1195 |Ước lịch sử, cần cập nhật trướcready |
| Scanlease+absence |1204object=307commit+609tree+288blob;4.350.922bodyB;≈2,604s |306tips+base; chưa toàn bộ rootsymlink/schema/workflowdeployment |
| Parentclosure đầy đủ của map |2658commit;3555object cộngscan;8.883.868B;≈0,239s phầnclosure |Khớpverdict6 |
| AncestryS→H02b0b86 |9commit/8cạnh;visited9 |Parent-cuối-trước của reader; không lấy witness làm chi phí fullgraph |
| Componentbenchmark3cặp xen kẽ |Median khônghash0,063482s;cóhash0,065756s;ratio1,035820 |Mỗi lượt1204object,4.350.922bodyB/4.413.764outputB,1cat-file. **Không phải E2E≤2** |
| Bare/linked/pack/alternate |0/0/0/0 |Git thường; source giữ trongcwd |
| Partialmissing→materialize /shallow /typedmemo |12→0 /12 /blob0→tree12 |Không đồng nhất missingobject với absententry |
| Alternate-depth3/4/5 |NativeGit0/0/0;preflightmodel0/0/12 |Bound4 thực có thể dựng3ca; không bị chốt nativeche ca5 |
| Fullsuites /81mutant /1709selftest /adr-song47/47 /CIr8 |not_run hoặc chua_do_duoc |EVIDENCE kể được, mirrorbase không có cả nhánhPRr8 để tái lập |

**Trả lời riêng §1 “Đo lại L5”: không tìm thấy số nào chép sai từ VERDICT.luot6.md.** Toàn bộ310/306/288/273/273/7/6–3/9–1/14–5/7–11–11/1204/4.350.922/2658/9–8 đều có đúng trong verdict6 và JSON gốc, replay cho cùng số. `03:12Z` là clock phân loại/start đã khai, không timestamp GitHub mới. Nếu đọc6/3 thành hômnay thì sai cách dùng clock; r8 gắn rõ08-09. Tôi không dựng một finding theo tiền giả định của câu hỏi. Không có con số sai được dùng chống đỡ lời khai **thẩm quyền** ở đây.

## chua_do_duoc

1. Implementationr8 chưa có: fullM1×consumer, A1–A12/N/N, catalogmutantsảnphẩm, base/candidate named-delta, E2E≤2 và memory/deadline thật trên mọi deployment. Model nhỏ không thay những bằng chứng ấy.
2. Các hướng bị cấm chỉ mô tả; không có source-negative hay OID-mismatch probe thực trongscratch. Fullsuites có ca ngoài phân công không được chạy mù từ bản cũ.
3. RawGitHub check/suite/run/attemptjobs/artifactdownload/digest/pagination, workflow-definition association khiS≠H, token/scopes/upload/runtime, branch protection và receiptpublisher thật. **Đường API trong spec/J vẫn ĐỀ XUẤT chưa canary**, không khẳng định responsefields hiện hành tồn tại chỉ vì model có chúng.
4. Runtime/helper/trust-store/image/proxy/credential production và người được chủ kho giao duyệt cụ thể. Đây là **facts/quyết định còn thiếu, không phải S1 P1/P2**. Không đọc binary/CA/credentials/tài liệu ngoàicwd để bịa controlproduction.
5. Tám defaultbudget trên roots/thựcthi thật; K chỉ có counterseam + alternate thực + subprocess deadline thu nhỏ. Walltime không thể suy từ rc subprocess sau khi nó đã treo; parent phải đo/enforce. Native precedence Git/libcurl chỉ được phân tích bằng lời, chưa canary phiênbản thực.
6. Comment5575587924/5578460203 bodyhash/actor/approval không tựreadback; authority review và lựa chọnQ13 được user cấp để dùng ở lượt này. Không suy từ đó quyền ready/lease/activate/merge.
7. Factsrollout: từngIssue/lease, mốcA0 saucanonical, audit/freeze/firstreceipt/consumerlanded, ruleset/bypass/directpush/queue, retention/journal, Q8lệnh, stopworker/lastSHA/g3/readback. Reviewer không thực hiện các thao tác ấy.
8. Map303ref và1186objects/4.311.029B/2622commits của lượt5 không tái lập exact vìscratch/mapcũ mất. Có maplượt6 đầy đủ và replaykhớp, không lấy mapmới bác sốlịch sử. Freshness server hiện tại không đo (mirrorthiếunhánhmới theo điềuphối).
9. Ranh giới “chủ kho gõ” và “agent cầmPAT”, signer identity thật; rawGitgpgsig/author không chứng minh người thao tác. EVIDENCE CI/d612ced/bfb0f9a, selftest1709/1709, releaseverify, adr-song47/47 và thời lượng/byte launcher không tự dựng lại từ phần codebase đã giao.

### Kiểm tra hiện vật cuối

`HINT.patch`: **5 hunk, 9.922 byte**, sha256 `95b637728152b227f17fed0d33f715dc003fe5b1bafe011f935a575ce6c25fcc`. Đã dry-run với `patch --dry-run --batch --fuzz=0 -p0`, rồi áp thật **chỉ lên bản sao** tại `scratch/luot7/patch-check/SPEC.md`; cả hai rc0, `cmp` với `SPEC.hinted.md` rc0. Bản sau áp sha256 `33af1f9c5ca9ce40b41b7a8d220fe1729409d66e885765ea71689a1b48a27166`. HINT phủ cả S8/S10; nhiệm vụ đồng bộ ADR được ghi tường minh, không giả ADR đã được patch.

`final-checks.json`: SPEC/ADR/HEAD/tree/ref map/status kho review giữ nguyên; đủ các section bắt buộc; không NUL; doc-claims có `ok:true`. **25 hiện vật lượt6** trong manifest lưu trữ đều khớp hash, bao gồm script đã replay. Kho review vẫn chỉ có hai tệp untracked được giao ban đầu. Các kết quả và script mới được kê hash trong `scratch/luot7/ARTIFACTS.sha256`.

Hoàn tất 2026-09-09T09:52:57+00:00; 1366.5 giây từ mốc user, trong trần60 phút. Kết luận: **không còn P1; changes_requested chỉ P2 S8/S10**. Không yêu cầu quyết định runner/profile còn thiếu như một finding, không tự xin thêm vòng reviewP1.
