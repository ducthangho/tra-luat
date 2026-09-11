verdict: changes_requested
reviewed_spec_sha256: 465538364b1a3f9477782fba79869bbd1c9351140e3fa9df50451baae22f9c79
reviewed_adr0047_sha256: b9975929c52e12767417b46b47829c265230117fe65df6a9fd22540d4868fdab
reviewed_sha: b416830ef2a509d60203d55552ce17950afcf67c
reviewed_tree: 266a2aba97d925dac3ab7473dda55adb0fe23b8e
reviewed_sha_role: codebase offline để đo; định danh bản đặc tả/ADR được review là hai sha256 ở trên, không phải PR head r9
model_tu_khai: GPT-6 / Codex theo chỉ dẫn phiên; provider OpenAI; execution_surface API/Codex có shell cục bộ; transport machine. Không có chứng thực độc lập build/variant/effort; không suy identity từ người đăng verdict.

# Cross-review r9 — lượt 8, lời gọi 9

**KHÔNG CÒN P1. S8 và S10 ĐÓNG. `changes_requested` chỉ vì S11/P2 về việc đối chiếu hồ sơ Packet Issue A0 với hợp đồng đã có, không phải lỗi thuật toán r9.** Không có P1 thuộc hình dạng nguồn tin cậy, không có P1 ngoài hình dạng ấy. Các ĐÓNG của lượt 7 giữ nguyên. Không nâng hạng để kéo dài, không hạ hạng để kết thúc.

**S11 xử được trong hồ sơ packet A0 trước ready, không cần revision đặc tả r9:** xác minh raw Issue, thống nhất định danh/mission và biểu diễn dependency đã có trong r9. Executor ghi kết quả preflight và điều phối/dispatcher có thẩm quyền hoàn thiện projection; executor không tự cấp mission/lease hoặc tự khai trường phái sinh. Không đưa consumer `land-packets`, ADR hay đường thứ tư vào write set A0. Nếu chỉ giữ trạng thái `proposed` trong lúc hoàn thiện thì chưa có bằng chứng một gate đã bị đi qua sai.

Theo chỉ thị đóng băng, **SPEC.md và ADR-0047.md không sửa**. `HINT.patch` là diff tham khảo trên SPEC cho S11, để chuyển nội dung sang ghi chú thực thi/hồ sơ Issue A0; **không áp vào r9 đã neo hash**. Nhãn: **“chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm commit”**. Kiểm patch chỉ trên bản sao; nếu dùng nội dung hint phải khai `hint_provenance`. Không cần thay câu nào trong ADR-0047. Không promote ADR thành Accepted bằng review này.

Bắt đầu theo user `2026-09-09T10:56:22Z`; VERDICT sơ bộ được ghi ngay đầu lượt rồi bổ sung. Chỉ đọc task-data trong cwd; không mạng; không agent phụ; kho `cay-kho/` chỉ đọc. Scratch mới nằm dưới `scratch/luot8/`. Mọi hướng bị cấm chỉ mô tả bằng lời, không tạo payload hoặc chạy suite chứa chúng. Giá trị nền thực thi, người duyệt và profile production chưa có là **quyết định/facts của chủ kho, không phải finding**.

Ký hiệu bằng chứng: **M**=`scratch/luot8/replay-clean/measurements.json` + `scratch/luot8/measure-r9-summary.json`; **C/F/G/P**=`controls.json`/`more-controls.json`/`admission-controls.json`/`partial-and-symlink.json`; **U/J/T/N**=`r8-controls.json`/`join-model.json`/`typed-memo.json`/`native-r8.json`, đều trong `scratch/luot8/replay-clean/`. Tên r8 là tên harness kế thừa; lần N này đưa **SPEC r9** vào bản sao nền. **K**=`scratch/luot8/r9-controls.json`, harness mới `r9_controls.py`; **O**=`a10-oracles.json`, oracle độc lập `a10_oracle.py`/`run_oracles.py`. Model không thay implementation chưa có.

## Bảng finding lượt 1–7 → trạng thái

Hạng dưới đây là hạng lịch sử. “ĐÓNG” là kết luận về hợp đồng; không tuyên bố implementation tương lai đã nghiệm thu.

| ID | Hạng cũ | Trạng thái r9 | Bằng chứng / phạm vi |
|---|---|---|---|
| S1 adapter-environment-boundary-is-not-specified | P1 | **ĐÓNG** | Q4.1:257–297 giữ producer độc lập, approver có uỷ quyền bền, manifest thực thi/trust bất biến, một phép so profile. ADR51–73 khớp. F serialization khớp neo fixture; không giả profile production. |
| S2 raw-object-read-does-not-verify-content-identity | P1 | **ĐÓNG** | Q4.5:304–325 vẫn băm actual type/size/body, cạnh từ bytes đã băm, memo kiểm type. M scan/closure; C routing; P missing; T blob0→tree12. Bytes lệch OID chỉ mô tả. |
| S3 a6-single-mutant-is-shielded-by-cli-flag | P1 | **ĐÓNG** | A6:507–520 giữ đúng seam và credit. C: routed0→unrouted12 là kill; input vốn unrouted12→12 SỐNG; profile trong miền khác neo12→0, ngoài miền12→12 SỐNG. K/O không lấy lỗi hạ tầng làm kill. |
| S4 q13-selected-mode-conflicts-with-a5-and-ready-fields | P1 | **ĐÓNG** | Q3/Q12/Q13 vẫn union policy / ngoại lệ / không neo; A5 khớp. F:11/0/11/12, claim[]8; U policy+metadata hợp lệ0. |
| S5 m9-check-publisher-consumer-is-unspecified | P2 | **ĐÓNG** | M9:439–477 không đổi về kỹ thuật; J19 ca join suite/run/attempt/job/artifact, positive0/âm12. Consumer trước bootstrap đã được quy định. S11 là hồ sơ Issue mới, không thiếu lại giao diện M9. Raw canary vẫn chưa đo. |
| S6 q13-exception-scope-and-retirement-are-not-bound | P2 | **ĐÓNG** | Q3:208–238 không đổi: descriptor/context, draft marker ghim S ở first admission, marker bất biến, policy mới qua binding mới, xoá policy12. U22 ca có control và các transition. |
| S7 retirement-file-conflicts-with-ledger-schema | P1 | **ĐÓNG** | Q3/M1/M4 giữ đúng một reserved path/sáu khoá/100644; metadata khác revocation/Q2. U: hai schema0, metadata mới lỗi12, marker cũ sửa/xoá/mode8, metadata-only inactive0. |
| S8 object-store-layout-and-resource-contract-is-open | P2 | **ĐÓNG** | Q4.5:327–351 định nghĩa từng phạm vi, inclusive, alias restart, alternate DAG và deadline do parent giữ. K cây258 cạnh/129 path/1 occurrence:0; mutant cộng snapshot12; sáu counter có 0/0/12; silent child timeout12. Chi tiết bên dưới. |
| S9 reroute-accounting-is-stale | P3 | **ĐÓNG** | §0/Q14: lượt7a preflight không tính; lượt7=call8. Lệnh mới user cho call9, không reset. Câu “cuối vòng này” là kết luận trước lệnh mới, không cấm lệnh mới của chủ kho. |
| S10 adr-spec-interface-boundaries-are-not-aligned | P2 | **ĐÓNG** | Đối chiếu từng câu ADR bên dưới: reader12/public8, count inclusive, claim phái sinh và uỷ quyền bền khớp. O: 5 control rc0, 5 mutant rc1 đúng assertion A10; state byte-match. |

| ID lịch sử | Hạng | Trạng thái r9 | Căn cứ giữ đóng |
|---|---|---|---|
| R1 canonical-url-check-does-not-bind-transport | P1 | ĐÓNG | S1; endpoint ghim, không authority từ origin; G nguồn nội bộ hợp lệ0. |
| R2 replace-refs-bypass-oid-pinning | P1 | ĐÓNG | Repo tạm không ref + no-replace + raw verified graph; không dựng replacement. |
| R3 bootstrap-gate-trusts-pr-and-arrives-too-late | P1 | ĐÓNG | Bootstrap audit ngoài cây PR, freeze, consumer trước bootstrap, mã canonical kiểm mọi PR. |
| R4 inactive-a0-already-changes-lease-decisions | P1 | ĐÓNG | Q3/Q5 giữ luật cũ trên input hợp lệ, DU_BAO riêng; U metadata-only0/revocation12 khi inactive. |
| R5 admission-head-is-not-the-landed-candidate | P1 | ĐÓNG | M9 ghim S/H/T, current base/head, tree(M), không queue, không dùng ngoại lệ drift. |
| R6 self-declared-effective-set-shrinks-exclusion | P1 | ĐÓNG | Q3 không tin EWS tự khai; F claim[]8. |
| R7 symlink-resolution-lacks-source-and-termination-contract | P2 | ĐÓNG | P hợp hai đích theo từng occurrence; K alias restart cộng tiếp, không reset. |
| R8 cutover-delta-and-fixed-g2-smoke-conflict | P1 | ĐÓNG | Q6 phân loại delta; C không đích, g3 riêng; smoke tập thật, không ép g2 đã hết hạn sống. |
| R9 a8-mode-case-cannot-kill-stated-mutant | P1 | ĐÓNG | G mode:8/only-new8 SỐNG/combined0 ĐỎ; full-T validator12. |
| R10 spec-review-label-does-not-waive-review-cap | P1 | ĐÓNG | Call9 được user giao rõ, không tự đặt ngoại lệ từ nhãn spec/Issue, không reset. |
| N1 canonical-remote-identity-unbound | P1 | ĐÓNG | S1/R1. |
| N2 snapshot-pinned-after-unverified-recapture | P1 | ĐÓNG | G map chụp trước, stale12, ref di chuyển sau vẫn đọc pinned OID. |
| N3 admission-workflow-does-not-cover-canonical-updates | P1 | ĐÓNG | M9 mọi PR/default, không lọc path/author/rc9, có edited, dispatch bị loại. |
| N4 canonical-checker-bootstrap-is-circular | P1 | ĐÓNG | Bootstrap audit riêng; U dựng canary H≠S khi canonical đóng; N command mới rc2 là hiện trạng nền. |
| N5 effective-write-set-and-symlink-resolution-missing | P1 | ĐÓNG | Q3 closure/occurrence + Q13; F/P/U. |
| N6 historical-cutoff-revives-feature-holders | P1 | ĐÓNG | Q6 mốc readback sau A0, feature tomb không thêm lịch sử; cutover có audit. |
| N7 candidate-map-omits-entry-mode | P1 | ĐÓNG | G/U map(mode,type,blob), marker cũ mode8. |
| N8 record-lease-guard-has-no-candidate-id | P1 | ĐÓNG | Q5/A10 truyền candidate ID, không lấy lease:null; K/O kiểm boundary model. |
| N9 acceptance-prepublish-and-second-parent-contradictions | P1 | ĐÓNG | Pure/CLI tách rõ; F second-parent giữ0/mất8. |
| N10 authorization-json-and-url-contract-is-open | P2 | ĐÓNG | Q2 URL/envelope/đúng6keys/types/duplicate/error order; raw API không đo. |
| N11 readback-after-admission-lifecycle-undefined | P2 | ĐÓNG | Q2/M9 trước canonical readback lại, sau canonical không gỡ event khi nguồn lịch sử mất. |
| L1 authority-signature-evidence-false | P1 | ĐÓNG | M mỗi commit1gpgsig, PGP/SSH; không suy actor/human signer. |
| L1 default-ref-is-untrusted-cache | P1 | ĐÓNG | G main thắng master; S1; không coi mirror như server mới. |
| L1 standalone-revocation-has-no-admission-gate | P1 | ĐÓNG | M4/M9 không phụ thuộc lease mới/rc9; S5. |
| L1 evidence-mention-is-not-an-authorization | P1 | ĐÓNG | Q2 exact authorization block, không prose/substring. |
| L1 write-set-exclusion-is-incomplete | P1 | ĐÓNG | Q3 mọi lease/closure/prefix/occurrence; F/P/U. |
| L1 snapshot-check-does-not-fence-writers | P1 | ĐÓNG | Q11 tuần tự stop→g3→readback→start; fencing land có nợ riêng. |
| L1 reads-are-not-pinned-to-one-snapshot | P1 | ĐÓNG | G OID pin + M verified graph + một map/clock. |
| L1 legacy-fallback-conflicts-with-ledger | P1 | ĐÓNG | Q3 precedence/history/reverse, Q6 cờ/delta. |
| L1 append-only-check-misses-candidate-and-merges | P1 | ĐÓNG | F/G merges+mode, U dispatcher metadata. |
| L1 packet-loop-guard-is-partial-and-boolean | P1 | ĐÓNG | Q5/A10 đủ5 cửa/3state/ID/idempotence; r9 làm rõ public8. |
| L1 acceptance-confuses-refs-blobs-and-mutations | P1 | ĐÓNG | F3 cặp/4 ref,1 cặp/3 ref; G mode; C/K/O đúng seam. |
| L1 revocation-schema-and-error-contract-incomplete | P2 | ĐÓNG | M1 r3 kế thừa được đọc ở bản phục hồi đúng hash; U schema reserved; r9 tách hai biên rc. |
| L1 size-estimate-and-slice-anchor-are-stale | P2 | ĐÓNG | M409/368/328; 825–1195 được ghi là ước trước vá, buộc ước/đo lại trước ready. |
| L1 ready-and-rollout-decisions-are-not-closed | P2 | ĐÓNG về hợp đồng cũ | S8/S10 đã đóng; facts rollout chưa có được khai đúng. S11 hồ sơ Issue mới không cộng đúp alias này. |

### S8 — kiểm đúng delta §0.5

K dùng cây Git thường có **129 thư mục anh em, mỗi path dài2**, tổng **258 cạnh**. Bốn object phân biệt (1 commit, 2 tree, 1 blob) là hợp lệ vì các subtree giống nhau; khử trùng object không khử 129 đường. Trên **một occurrence OID**, resolve129 path độc lập dưới bound128 đều0. Mutant dùng tổng258 để quyết định trả12 bị expected0 bắt. Đây chính là miền đếm r9, không lẫn “129 occurrence”.

| Counter/ca | Đơn vị/fixture | Kết quả đo |
|---|---|---|
| Parent | graph commit thật3/4/5 cạnh, bound4; S ở cuối đường | **0/0/12**; mutant `>=` thay `>` từ chối ca4, ĐỎ |
| Tree | tree thật3/4/5 entry, bound4 | **0/0/12**; mutant exclusive từ chối ca4, ĐỎ |
| Unique object |2/3/4 blob phân biệt, bound3, raw reader cũ | **0/0/12**; chặn trước body thứ4 |
| Total bytes |17/18/19 bytes body blob, bound18 | **0/0/12**; không tính header/protocol bytes vào body budget |
| Alternate depth | graph store thật3/4/5 cạnh, bound4 | Native Git đọc được **0/0/0**; preflight **0/0/12**; mutant bỏ depth nhận ca5⇒0, ĐỎ |
| Alternate stores |7/8/9 store ngoài primary, depth1, bound8 | Native **0/0/0**; preflight **0/0/12** |
| DAG chung đích | cùng bottom tới trực tiếp và qua nhánh dài5, 5 store ngoài primary | longest-depth5⇒12; không để cache lần ngắn che lần sâu |
| Alias nội bộ | `alias` trỏ `d/x`, tổng4 bước gồm dereference+restart; bounds3/4/5 | **12/0/0**; mutant reset counter sau link trả0 ở bound3, ĐỎ |
| Clock tiêm | pending ở thời điểm3/4/5, deadline4; hoàn tất tại3 trướcdeadline4 | **0/12/12**; hoàn tất trướcdeadline0; count inclusive không làm deadline inclusive |
| Child im lặng | child thường ngủ1s; deadline fixture0,1s | reader12; child bị kill và đã reap; stdout0; khoảng0,102s |

Không chạy lại `budget_controls.py` cũ như oracle r9: file ấy cố ý lưu hai cách hiểu r8 và còn mô hình count cho wall time. Đã đọc nó để kế thừa thiết kế fixture, dựng K mới với deadline riêng. Không nhận `rc` của Git thay preflight count, không suy default60s đã benchmark từ control0,1s. Per-object-byte counter ở seam riêng, default50000/8MiB/128MiB/10000 và roots deployment đầy đủ còn phải nghiệm thu ở A0; user yêu cầu ít nhất hai counter, lần này đo sáu.

### S10 — đối chiếu từng câu ADR-0047 r9 với SPEC r9

Bảng đi hết nội dung ADR, nhóm các câu liền nhau khi chúng có cùng đối chiếu; trong ô nêu riêng từng mệnh đề. Không chỉ so bốn từ thay. “Khớp” nghĩa không tạo oracle khác; chi tiết spec bổ sung được ghi rõ.

| ADR dòng/câu | Đối chiếu spec | Kết luận mạnh/yếu |
|---|---|---|
|3–4: Proposed; duyệt soạn; chưa Accepted; đồng bộ r9 |ngoai_pham_vi420, S10:562–571 |Khớp; sửa tài liệu không là promote/runtime |
|6–11: cùng hình dạng qua5lượt, các lớp và5hash verdict |§0 + hinh_dang_ke_thua573–590; hash các VERDICT1–5 đo lại |Khớp lịch sử; không đọc5 thành tổng hiện tại6 |
|11–15: lần3 xem lại; reviewer4b/5 yêu cầu ADR; r4 hứa dừng; ADR định nghĩa nguồn được tin |§0:42–55, hinh_dang_ke_thua580–590; §12 protocol |Khớp như tường thuật lịch sử; câu “không phải bản vá lần6” không xoá phát hiện lần6 được ADR40–44 ghi riêng |
|19–22: liệt kê cổng; một snapshot/ba lớp; thiếu/không đo được⇒đỏ |Q4:255–357, M9 |Khớp; snapshot Git duy nhất không thay readback authorization Q2 |
|22–25: reader/lease_publish12; wrapper mapping; packet_loop8+nguyên nhân+không đổi state; interface ở Q5/A10 |Q5:364–371; A10:538–541; S10:555–559 |**Khớp hoàn toàn**. “Không đổi state” ở đây chỉ lỗi nguồn không đo được; không áp lên thu hồi đã xác minh |
|29–31: canonical hằng trong mã; endpoint tường minh; không discovery qua remote/config/symref cục bộ |Q4.1:257–259,281,294–297 |Khớp |
|32–33: default từ advertisement; workflow option bằng symref; lệch/vắng/mơ hồ12; không fallback |Q4.3–4:300–303 |Khớp |
|34: get-url/local HEAD/config chỉ chẩn đoán |Q4.1:281,295, Q4.3 |Khớp; không biến chẩn đoán thành authority |
|35–36: bare fixture tiêm API nội bộ; không cờ/env production đổi authority |Q4.1:296–297; đầu nghiệm_thu |Khớp; các negative source vẫn phân công điều phối |
|40–44: bản đầu băm chưa đủ; helper name/CA directory/runtime ngoài digest; lần6; nền thực thi |§0.4 S1, Q4.1:264–274, hinh_dang_ke_thua |Khớp lịch sử và lý do thay lớp2 |
|46–50: approved environment; manifest Git/helper/runtime/full trust/endpoint/proxy; không băm OS; bất biến invocation |Q4.1:264–274 |Khớp; spec nói cụ thể identity/đường/hash và từ chối mutable/không định danh |
|51–54: producer độc lập; approver chủ kho/uỷ quyền bền có phạm vi qua commit review; cấm self-register |Q4.1:265–271, S10:569–570 |**Khớp**, không còn ADR chỉ cho riêng chủ kho |
|55–59: env dựng rỗng, repo tạm, flags cố định, absolute executable; blacklist chỉ chẩn đoán |Q4.1:259–264,272–274,293–295 |Khớp. Spec liệt kê thêm PATH/HOME/template/ceiling; hữu hạn cấu hình là chi tiết, không nguồn quyền mới |
|60–64: allowlist key/type/domain; đúng helper/trust/proxy; proxy thống nhất; không wildcard; parse kiểu Git; unknown12/TLS |Q4.1:276–284,290–292 |Khớp. Các “đúng neo” nằm trong **một phép so profile** theo ADR68–69/spec292; không dựng thêm comparator để che mutant |
|65–67: digest canonical JSON/version/secret identity; temp paths là vai trò; isolation riêng; không hash random paths |Q4.1:286–289 |Khớp; spec thêm separators`,`/`:` là định dạng cụ thể, ADR không quy định định dạng khác |
|67–69: digest bằng neo; lệch/không tính12; một comparator; receipt không thêm comparator |Q4.1:290–292, A6:517–520 |Khớp; S3 không tái mở |
|70–71: manifest đổi⇒chặn tới khi duyệt; deployment tốt nhưng chưa đăng ký vẫn chặn; không ambient fallback |Q4.1:270–274,283–284 |Khớp; đó là miền chấp nhận chủ ý, không impossible-green |
|72–73: nền cụ thể/quy trình mỏ neo của chủ kho; trước readyA0 |ngoai_pham_vi420, Q12:633–641 |Khớp khi “quy trình” là việc bố trí producer/approver cụ thể; các bất biến independent+commit review đã chốt ở51–54, không được tự chọn lại |
|77–80: cache untrusted; isolated reader; object dir giải API cho bare/worktree; readonly; alternates do adapter |Q4.5:304–310 |Khớp. Cụm “chỉ qua env adapter” không nói setting env tự vô hiệu info/alternates; spec yêu cầu kiểm cả metadata bắc cầu ấy |
|80–82: loose+pack; partialmissing12; shallow12; cat-file missing có thể Gitrc0 |Q4.5:308–316 |Khớp; C/P/K đo được, không đồng nhất missing với absence |
|83–85: đọc/băm actual bytes trước dùng; mọi cạnh từ bytes đã băm; không walker/merge-base/ls-tree |Q4.5:318–325 |Khớp; measurement numstat dùng merge-base không phải product ancestry source |
|85–87: ancestry tự đi parent/visited; **vượt count/byte/depth hoặc hết deadline12**; counter/biên ởQ4.5 |Q4.5:333–351; A6:522–528 |**Khớp**, n=bound đã tớiS được nhận; deadline pending hết thì12 |
|87–88: memo(expected_type,OID), hit kiểm actual type |Q4.5:319–323 |Khớp. Counter unique theo(actual_type,OID) còn cache key theoexpected là hai mục đích, không mâu thuẫn |
|89–90: absence cần parent verified; hash/missing/type/rc lỗi12 |Q4.5:318–325 |Khớp |
|91–92: source replacement không áp do repo tạm khôngref; ba lớp/seam riêng |Q4.5:324–325, A6:515–516 |Khớp; không hứa gỡ riêng no-replace sẽ kill dưới isolation còn nguyên |
|96–97: ba trạng thái; unknown đỏ; không offline conclusion cache |Q3/Q4/Q5 |Khớp; memo object **trong** snapshot không là cache verdict qua snapshot |
|98–99: map trước discovery; tên+SHA40; không recapture; hàm trạng thái chung |Q4.2–6:298–356 |Khớp; local heads chỉ thêm holder, không bù remote-tracking |
|100–101: **claim phái sinh** không thu hẹp; so giá trị tính lại; mismatch8 |Q3:201–207, S10:566–568 |**Khớp trong phạm vi claim phái sinh**. Ví dụ `da_bi_thay_the` không làm tomb feature thành nguồn thu hồi; phải tính theo chế độ Q3/lịch sử Q6. Không có lệnh biến mọi field raw thành phái sinh |
|102: input hợp lệ write_set/timestamp vẫn là input |Q3:203–207, M1r3, S10:567–568 |**Khớp**, không đòi producer phái sinh cho input khai báo |
|102–104: descriptor/binding không xác minh⇒reader12 rồi mapping; descriptor bằng neo canonical |Q3:208–215, Q13, S10:566–569 |**Khớp** với U binding0/12/12; không blanket8 lên lỗi nguồn |
|108: chỉ cổng đọc; không trao quyền ghi/thay lease§4 |Q1/Q2/Q5/Q11, ngoai_pham_vi |Khớp; M9 ràng buộc tiếp nhận, không tạo authority người ký |
|109–111: không chứng nhận OS/chuỗiTLS; khai giới hạn receipt |Q4.1:270–289, chua_do_duoc11 |Khớp; không cho tự bỏ helper/runtime/full trust khỏi manifest |
|112–113: M9/Q13 nằm ởspec, không chốt trong ADR |M9, Q3/Q13 |Khớp phân công; S10 không mở lại hình dạng nguồn |
|114–115: chi tiết allowlist/digest/roots/budget ởspec/mã; bất biến không đổi khi chi tiết đổi |Q4.1/Q4.5, S10:570–571 |Khớp; **spec** vẫn bắt revision/review khi đổi budget, câuADR không miễn bước đó |
|119–121: 0cổng ởmaster585c7d5; code cũ không adapter/hash, vẫnany; adr-song chỉ registry |§1:144, ngoai_pham_vi420; source-audit.json đọc bytes đã xác minh ở base/master |Khớp là snapshot code đã ghi ngày, không claim ADR mới được runtime enforcement |
|123–126: Accepted chỉ sau A0land+A2/A6 đỏ đúng seam+profile receipt; đo lại§20, không promote bằng chữ |ngoai_pham_vi420, Q10, A2/A6 |Khớp; điều kiện tương lai, chưa tuyên bố đạt |

**Không còn câu ADR nào bắt một mã lỗi hoặc biên chấp nhận trái r9.** ADR lược bớt chi tiết serialization/store/counter; spec cung cấp chi tiết ấy mà giữ cùng oracle. Phần “Đồng bộ hợp đồng” là điều kiện kiểm đồng bộ đã được bản ADR này đáp ứng, không yêu cầu A0 tự sửa thêm ADR ngoài write set. Nó không mâu thuẫn A10 cũ: ngay M1 r3 đã ghi packet_loop ánh xạ mọi lỗi sang RC_STATE; r9 chỉ đóng rõ giá trị8 và diagnostic12. Thu hồi tiếp tục lưu stale/event trước khi trả8 theo Q5.

## Findings mới

### S11 — packet-a0-projection-is-not-reconciled-with-frozen-contract · P2

**Vị trí:** hồ sơ Issue #488 như user cung cấp; SPEC:396–413,421,475–477,Q7/Q12; protocol§3.2:128–166 và§5:288–291. **Nguồn bằng chứng:** user cho `packet_id: THU-HOI-LEASE-VA-CAP-LAI-A0`, `mission_issue: null`, `depends_on: []` và comment nêu `LAND-DOC-RECEIPT-THU-HOI`. EVIDENCE:120 chỉ chứng thực theo lời điều phối rằng Issue proposed/neo hash/chưa lease; **không có raw Issue hoặc body comment trong bundle**. Không giả đã đọc chúng.

Các trường trên chưa đủ để công nhận hồ sơ conform§3.2: schema dùng `wp<issue>` và mission number; alias dài cần được phân biệt với ID packet theo schema, `null` không tự chứng minh một ngoại lệ standalone. `depends_on: []` cũng **không có nghĩa dependency M9 biến mất**: dependency có tên đã ở trong chính hash r9 và comment đã nhắc nó. Nhưng chưa có bản chiếu có kiểu cho biết nó được resolve sang Packet/Issue nào và được kiểm ở giai đoạn nào.

**Không suy một cạnh execution từ một điều kiện land:** §5 dùng `depends_on` để chặn bắt đầu trước predecessor integrated; M9 đòi consumer **land trước cửa sổ bootstrap**. Hai điều kiện khác nhau. Chỉ từ `[]` không thể chứng minh A0 được land thiếu consumer, cũng không được tự ép consumer phải land trước khi viết mọi dòng A0. Hồ sơ phải nói rõ dependency thực thi nếu có và land obligation bắt buộc, với cùng mỏ neo/authority của packet. Prose có tên đủ để không coi nợ bị quên; chưa đủ để chứng nhận projection phục vụ ready/land.

**Vì sao P2, không P1:** đây là hồ sơ **proposed**, chưa lease/ready; r9 đã quy định dependency, thứ tự bootstrap và nguồn phái sinh, không có câu cho phép dùng `[]` để bỏ gate. Chưa có bằng chứng code/dispatcher đã fail-open hoặc spec thiếu bất biến. Vấn đề còn lại là điền/đối chiếu biểu diễn với luật đã có. Không dùng “mâu thuẫn luật” để nâng một hồ sơ chưa ready thành P1 thuật toán; cũng không tuyên bố những trường đó đã conform.

**Vá ở đâu/cách vá:** trong Issue A0/projection/handoff preflight, dispatcher đối chiếu raw body+comments với hash r9; dùng ID chuẩn theo§3.2 (với #488 là `wp488`, tên dài giữ làm nhãn/alias), gắn mission hợp lệ hoặc dẫn ngoại lệ standalone được duyệt rõ nếu tồn tại. Resolve dependency có tên; biểu diễn đúng giai đoạn và land obligation; không đổi dependency thực tế đã đóng băng. Chốt trường phái sinh theo Q12. Executor A0 làm việc này trong packet cùng điều phối, **không cần revision SPEC r9** vì hợp đồng đã đủ. HINT đưa ghi chú đối chiếu Q12 làm vật liệu cho hồ sơ packet, không yêu cầu áp lên spec đóng băng.

**Ca khoá:** đọc lại Issue/projection đã hoàn thiện; so từng định danh/hash và dependency có tên với hợp đồng, không chỉ đếm số phần tử. Consumer chưa có receipt landed thì bootstrap không bắt đầu; đủ receipt/canary theo M9 mới qua. Đây là ca preflight/readback cần làm ở A0; lượt này chỉ **đọc hợp đồng**, không tạo mock raw Issue rồi nhận là bằng chứng GitHub.

**Write set:** spec A0 đúng ba path `ops/lease_publish.py`, `ops/lease_publish_test.py`, `.github/workflows/ops-thu-hoi-admission.yml`. User chỉ cho biết Issue có3 path, EVIDENCE không liệt kê tên; **không đo được exact set của Issue**. `3==3` không chứng minh hai tập bằng nhau. Không có căn cứ báo write-set mismatch đã xảy ra, cũng không có căn cứ báo byte/path match đã kiểm.

**Hệ quả:** không mở thêm path A0, không cho sửa consumer/ADR trong A0, không cấp lease từ review này. Nếu raw Issue đã có mapping/ngoại lệ hợp lệ trong phần chưa giao thì S11 được đóng bằng readback đó; không sửa spec để hợp thức hoá một ngoại lệ chưa có. Các giá trị profile/người duyệt production còn thiếu không thuộc S11.

### Các hướng mới đã bác / không thành finding

- **A10 cũ vs mục đồng bộ:** không xung đột. Reader unknown12→CLI8/state nguyên; revoked→ghi stale/event rồi8. Chỉ có mutant mapping bị O làm đỏ, không lấy public12 như một cách fail-close tương đương8.
- **§0.5/Q14 và bộ đếm:** theo facts user/EVIDENCE, call1–6=lượt1,2,3,4a,4b,5; call7=lượt6; 7a preflight không bắt đầu model output nên không tăng; call8=lượt7; lượt này **call9** theo lệnh09-09 mới. `stdout0` riêng nó không đủ phân loại: 4a stdout0 vẫn có output/token nên tính. `accounting.json` chỉ kiểm phép đếm theo facts được giao, không giả có raw launcher7a.
- **“Lời gọi8 cuối vòng này”:** đúng kết luận sau r8 dưới lệnh08-09. User/EVIDENCE:121 có lệnh09-09 yêu cầu đọc r9 chưa review; quyền mới ấy điều khiển lượt này, không reset hay phải sửa bản đóng băng để cho phép review. Không tự mở call10.
- **§1 Đo lại L5 /§0.5 chép số:** không tìm thấy số chép sai từ VERDICT7. L5 ghi rõ mốc08-09 và vốn dẫn lượt6; VERDICT7 xác nhận nguyên310/306/288/273/273/7,6/3 ởclock03:12,9/1,14/5,7/11/11, 1204/4.350.922,2658, 9/8. VERDICT7 hiện tại0/0 tại09-09 không phủ định clock lịch sử6/3. §0.5 đúng129/258/2, bound128, depth3/4/5,2P2/0 P1. Thời lượng launcher1377,096s (EVIDENCE) khác wall tự ghi1366,5s trong VERDICT7 là hai phép đo, không gán lẫn.

## Phản chứng đã chạy lại + mới

1. **Preflight/đóng băng:** `scratch/luot8/preflight.py` đo hash, HEAD/tree, detached, status, map refs, abbrev7, shallowfalse và hash hiện vật cũ. Hai tệp untracked trong kho khớp SPEC/ADR ngoài kho. Không fetch mirror.
2. **Replay hợp lệ:** đã đọc source trước chạy. `replay.py` nạp qua loader, chỉ redirect nơi ghi sang `scratch/luot8/replay-clean/`, không sửa source/fixture lượt6/7. Chạy `measure controls more_controls admission_controls partial_and_symlink r8_controls join_model typed_memo_control`; log đủ8 completion, runner rc0. C/F/G/P/U/J/T cho các kết quả ở bảng lịch sử. Có một lần gọi lặp nhầm harness ban đầu gặp `destination already exists`, rc1; **không tính là test fail sản phẩm/kill mutant**. Đã chạy trọn lại trong thư mục sạch riêng; chỉ kết quả `replay-clean/` được dùng. Các JSON ban đầu ngoài thư mục sạch là nháp, không dùng làm nghiệm thu.
3. **K mới:** Git thường bằng working/bare tree/commit/alias nội bộ/alternate DAG; đọc object từ raw reader đã kiểm; counter traversal mới theo r9. Sáu biên0/0/12, exact-bound mutants, width mutant, alias-restart mutant, alternate-depth mutant và silent subprocess. Harness cuối dùng `r9-control-v3/`; sửa nhãn đơn vị thành129 path/1 occurrence và duyệt tree giữ con trỏ hiện tại, rồi chạy lại rc0. Không dùng số đường làm số occurrence.
4. **O mới:** model guard lấy `RC_STATE=8` bằng AST từ source thật;5 cửa×4trạng thái=20 control; target candidate ởrecord-lease; unknown/statebyte-match; revoked/stale/mộtevent/idempotent; alive/other-ref đi tiếp. Oracle độc lập chạy thành10process:5 control exit0,5 mutant trả thẳng12 exit1 với `TinHieuChotCa: A10_unknown_<đúng cửa>`. Có stdout/stderr từng ca. **Đây là phép đỏ thật của oracle trên model boundary, chưa phải test20case trên state do product `init` tạo**; B chưa có implementation. REST không nằm trong guard model; không giả đã gọi REST403 thật.
5. **N native:** loader chạy `native_r8.py` đã đọc, clone/fetch **chỉ từ cay-kho cục bộ** sang scratch, không origin mạng; đưa SPEC r9 vào bản sao. Bốn holder0/rc0; g2rc8 do hết hạn; command mớirc2 vì chưa có; doctrine8 tệp/0/rc0; docclaims strict rc0+ok:true. Không chạy fullsuite chứa ca ngoài phân công.
6. **Delta HINT7:** dry-run rồi áp5hunk lên bản sao r8 rc0/fuzz0; được sha256 `33af1f9c5ca9ce40b41b7a8d220fe1729409d66e885765ea71689a1b48a27166`. Phần từ `nguon_cap_viec` đến trước Q14 **byte-identical** với r9. Chênh còn lại là đầu đề/kế toán§0/§0.5 và Q14, không hunk kỹ thuật lạ. `delta-review.json` lưu lệnh/output. Không áp vào SPEC/cay-kho.

**CHỈ MÔ TẢ / not_run:** fake remote helper; `remote.<x>.vcs`; rewrite sang kho khác; replacement/graft; Git env/executable nhằm đổi nguồn; bytes cache lệchOID; helper/runtime/trust giả; đường thoát cây; đồng tự Unicode; chuỗi thoát. Hợp đồng yêu cầu tách seam: không dùng detector presence, không cấp credit hash cho ca Git đã chặn trước hash, không cấp credit bỏprofile ở input ngoài miền. Không tạo các payload ấy, không import/chạy script cũ chứa chúng. Env cô lập/routing trong control chỉ đọc đúng kho fixture bình thường; không giả nguồn có thẩm quyền production.

## Tiêu chí A1–A12

Đã đọc M1/A1–A12 kế thừa ở `scratch/luot6/SPEC.r3.recovered.md` (hash `ef9b3700…` đúng r3), rồi áp các thay thế r9. Không dùng câu r3 đã bị delta ghi đè làm finding mới.

| Tiêu chí | Đơn vị/oracle/đột biến đúng ca | Đánh giá r9 và phép đo lượt này |
|---|---|---|
| A1 |cặp(blob,path) cho dòng; leaseID cho holder; occurrence choMAP_REF |F thật3 cặp/4 ref; known-list bỏblob3 làm3→2dòng/holderX sống lại. Có phép đỏ. Smoke∅/{g2} theoclock, không impossible-green sau expiry. |
| A2 |1 cặp/3 ref; nguồn/default/name+OID/profile |F1/3, G main/master0 và stale12. Negative authority chỉ mô tả. Không tin cùngSHA/symref là cùngnguồn; bỏ authority comparator cần đúng source seam còn lại hợp lệ. |
| A3 |năm oracle8/0/8/0/8; hai cây mốc; inactive vsDU_BAO |Hợp đồng có ca bắt fallback/đíchsai/featuretomb/mốctrôi; phải giữ clock/leasekhác hợp lệ để không bị expiry/claim che. Không chạy native5case r9. |
| A4 |chiều ngược từng nguồn tách riêng, alive0 |Tắt nguồn ledger dưới fixture chỉledger, tắt history dưới fixture chỉhistory mới8→0. Nếu cả hai cùng giết lease thì mutant đơn có thể SỐNG; không nhận credit từ ca ấy. Không thấy tiêu chí đòi kill trái điều này. |
| A5 |exact/prefix/alias perOID/closure/claim; pure vsCLI publishedpair |F11/0/11/12/[]8; P cùngblob/2 OID hợp cả2 đích; U policy+marker0. Hai purecandidate0/0 không chứng nhận atomic lock; CLI unpublished12/published-conflict11/11. Hướng thoát/Unicode không chạy. |
| A6 |seamrouting/profile/hash/type/graph/pinning;7 counter count/byte/depth +1 deadline; E2E3 cặp |C/G/P/T/K giữ correct/red/survived riêng; S8ĐÓNG. Width0/globalmutant12; exactbound0/strictmutant12; alt5native0/preflight12/dropdepth0; silentchild12. Hash mismatch chưa chạy; E2E≤2 chưa đo. Không thấy ca bất khả đỏ/xanh theo hợp đồng. |
| A7 |M1 mỗi constraint/rc4,8,12; dispatcherreserved; consumerverdict |U validrevocation0/metadatavalid0; lỗi metadata12; nearname12; inactive revocation12. M1 thẩmquyền4 khác field8 khác source12; packetloopmapping8 không đổi readeroracle. Full matrix×consumer chưa chạy. `raise→continue` phải so verdict/output thật. |
| A8 |map(path,mode,type,blob), toànT, ancestor/parent2, strictS/H/T |F cha2giữ0/mất8; G mode8/only-new8SỐNG/combined0ĐỎ/fullvalidator12; U markertransitions. Có controlfirstpolicy0 nên S7 không còn làm mọi nhánh chết. |
| A9 |stateful API endpoint/ID/trace; ≥1 trướcadmission;0lời gọi thêm saucanonical |Q2/M9 phân biệt envelope12/authorizationJSON8/actor4. Độc lập lease/rc9; bỏwiring mấtcall/receipt vẫnĐỎ dù CLIrc0. API fixture/full matrix và rawGitHub chưa chạy. |
| A10 |5entrypoints×4 trạng thái; native init state; IDcandidate; eventidempotence; unknownbyte-match |K20 controlmodel; O5 mapping mutant đỏ thực ở targetassertion public8/reader12. Không là20nativecase trêninitstate; chưa có B. Mục đồng bộ không đổi oracle cũ, chỉ định rõ8. |
| A11 |base/candidate cùnglệnh, named delta; rawworkflow/check/token; canaryS≠H |N doc/doctrine xanh trênbasecopy+r9. U dựng đượcS≠H/revocationsetempty; J đủ modeljoin. Không claim full121/278/81 hoặc Actions thật. Thiếucanary⇒giữđóng là gate cóđiều kiện, không tiêu chí không thể xanh đã chứng minh. |
| A12 |catalog expected ngoàiPR; registered/executed/pass/fail/skipped/not_run; credit đúngseam |F bắt mấtinvocation và xoá cảregistration+invocation. O targetsignal riêng, không bọc lỗi vôcan thành assertionđích. Chưa có productcatalog/N/N. |

### Nhất quán luật, Q7–Q14 và kích thước slice

| Nguồn | Kết luận |
|---|---|
|§3.2 / ADR-0025 |Q12 vẫn đòi Issue/revision/generation/hash/phái sinh cóproducer; đổi hợp đồng material phải revision. S11 chỉ đối chiếu hồ sơproposed với dependency đã có; không cho caller dùngprose/alias tự cấp quyền. Không kết luận rawIssue đã conform khi chưa đọc. |
|§4 / ADR-0028 |Q5 stale/event/lastSHA; Q11 stop→g3; retention/journal không thay bằng artifact có hạn. Snapshotkhông là fencing. |
|§5 |Closuretừpolicy hoặc ngoại lệQ13đãchốt; policyđổi thìpause/re-evaluate/revision; occurrenceunion; consumer ngoàiwrite-set cópacketriêng. Phân biệt dependencytrướcchạy với điều kiệnland. |
|§8 / CLAUDE.md |Reviewread-only/exactsha, hai trục spec+standards; positiveevidence/mutantđúnglýdo; HINT chỉspecthamkhảo, không mãauthority. Native doc/doctrine không chứng minh runtime/canary. |
|§12 |Call9 hợp lệnh mới;7a khôngcount vìfacts preflight chưamodeloutput,4avẫncount. Khôngreset và không tự mở vòngP1 tiếp. |
|ADR-0047 Proposed |Ba lớp/ba luật không thiếu hợp đồng S1; S10đồngbộ; chưaAccepted, không gán47registeredADR thành47cổngnguồn. |
|ADR-0044 |A0 3 path/+560–780 **ước cũ**, A1 3 path/+90–160, B2 path/+160–240, C1 path/~15; tổng6 pathduynhất và825–1195 đúngphépcộng. A0 vượt300đãkhailýdo/phạmvichứkhônggiấubằng“≈30ca”. Chưa cóimplementationnumstat mới; Q7/Q12 buộc ướclại trướcready. |

A0 tăng việc vì manifest/schema metadata/joins; không thể chứng nhận 560–780 vẫn là ước đủ từ chưa có code. Đây đã được r9 khai là ước trước vá, nên không giữ lại finding số liệu cũ hay tự bịa một ước chính xác mới. Consumer `LAND-DOC-RECEIPT-THU-HOI` không tính vào6 path của bốn slice này. A0 bootstrap cần mã canonical đúng nơiM9đòi; A1/B/C không mọc trên PR chưa nhận predecessor. PR250+409 là **spec**, không lấy làm mẫu code có độ phức tạp tương đương.

Q7 vẫn cần chủ kho bố trí ngoại lệ A0/audit; Q8 cần lệnh khôngđích thực; Q9 vẫn là khuyến nghị nhậnrevocationleasehếthạn; Q10/Q11 cầnfactsrollout; Q12 hợp đồng đủ nhưng profile/activation/phái sinh phải điền đúng bước; Q13 đã chọn(ii), không hỏi lại policy hay ngoại lệ; Q14 áp lệnh mới call9. Các việc đó không được giả thành approval/lease/activation từ verdict này.

## Bảng đo lại

Mọi số ref là **mirror đóng băng**, không advertisement mới. M so map từng tên/OID với lượt7: bằng nhau. Các clock quá khứ dùng bytes trong mirror để phân loại, không phải đã quan sát server ở thời điểm đó.

| Đại lượng | Lượt8 đo | Đối chiếu/giới hạn |
|---|---|---|
|SPEC / copy trongcay-kho |465538364b1a3f9477782fba79869bbd1c9351140e3fa9df50451baae22f9c79;652dòng |Đúng r9 |
|ADR0047 / copy |b9975929c52e12767417b46b47829c265230117fe65df6a9fd22540d4868fdab;126dòng |Đúng bản sửaS10 |
|VERDICT7 / HINT7 |f28b7d0ce868d15905d4468ea248db43bfed79b7fe1899f278fe4afe9a4c461c /95b637728152b227f17fed0d33f715dc003fe5b1bafe011f935a575ce6c25fcc |Khớp bàn giao; HINT5hunk áp sạch trênr8copy |
|VERDICT1/2/3/4b/5/6 |b60a755f…/bb293295…/6b8dde21…/7d3017ec…/1596d562…/9090aadd… |Khớp§0/ADR; r3recoveredhash ef9b3700… |
|HEAD/tree |b416830ef2a509d60203d55552ce17950afcf67c /266a2aba97d925dac3ab7473dda55adb0fe23b8e |Detached; abbrev7; shallowfalse |
|origin/master |585c7d510e026b4ea5a2b395c69581f24c1d8fa0 |48commit sau base; không là mốcA0đãland |
|Ref theo công thức |310=309remote+1local;306tipphânbiệt |Từng tên/OID khớplượt7 |
|Cặp/path/leaseID/đa-blob |288/273/273/7 |Không đổi |
|Clock07-09 13:41 /14:33:15 /08-09 03:12:57 |cònhạn/chưatomb8/4;7/3;6/3 |Mốc lịch sử, không phải hômnay |
|Clock08-09 03:37:33 /09:52 /10:17:12 |5/3;1/1;0/0 |Fixtureclock |
|**Clock09-09 10:56:22** |**0ID/0cặp cònhạn;0chưatomb** |Không chép6/3 thành hiện trạng |
|r2blob26f07b4/fdfde3a |9ref/1ref |KhớpL5/VERDICT7 |
|#456blob8b2103c/1f95042 |14 ref/5ref |KhớpL5/VERDICT7 |
|Tombbase/H02b0b86/master585c7d5 |7/11/11 |Không dùngbase7 làm masterhiệntại |
|base…H02b0b86 |0trái/31phải |Không đồng nhất31commitriêng với witness |
|Gpgsigb416830/6635379 |mỗicommit1;PGP/SSH |Rawheaders; không đọc keyring/kiểm chữ ký ngoài cwd, không đo actorhuman |
|planned |3leaseID, đềuhếthạn |Dữ liệu cũ, không giữ quyền hiện tại |
|AST `kiem→_lease_cham_duong` /schemahelper5 cửa |0 /1,1,0,0,0 |Nền thiếu3guard; không phải nghiệm thu code mới |
|AST RC_STATE |8 |Dùng để neo oracleO |
|Policy/schema/sổ/admissionworkflow ởbase/master |vắng |Không tự coi production đã cór9 |
|Native4holder /checkg2 /commandmới |holder0+rc0 cả4;g2rc8;newcommandrc2 |g2stderr chỉhếthạn; mã mới chưatồn tại |
|Native doctrine r9 |8 tệp/0chỗchép;rc0;69stdoutB |Basecopy+SPEC r9 |
|Native docclaims strict |rc0,ok:true;70.861stdoutB |Không chứng minh đồng bộ logicADR bằngscanner |
|PR250/275/248 merge-base→head |+409/−0;+368/−0;+328/−1 |Per-file/base/head trongM |
|Ước A0/A1/B/C |560–780/90–160/160–240/~15;825–1195 |Ước lịch sử, chưa implementationnumstat |
|Scanlease+absence |1204object=307commit+609tree+288blob;4.350.922bodyB;≈2,477s |306tips+base; chưa đủ mọi rootdeployment |
|Parentclosuremap |2658commit;3555object cộngscan;8.883.868B;≈0,237s phầnclosure |Khớp6/7 |
|Witness S→H02b0b86 |9commit/8cạnh;visited9 |Một thứ tự traversal, không phảifullgraphcost |
|Componentbenchmark3 cặp xen kẽ |median không hash0,057779s;cóhash0,068190s;ratio1,180189 |1204object/4.350.922bodyB/4.413.764outputB,1 cat-file/lượt; **không phải E2E≤2** |
|Bare/linked/pack/alternate |0/0/0/0 |ControlGitthường |
|Partialmissing→materialize/shallow/typedmemo |12→0 /12 /blob0→tree12 |Localpreparation; không network; khôngmissing=absent |
|K width/6 counter/alias/deadline |BảngS8 |Fixturethu nhỏ, khôngdefaultbudgetproduction |
|U/J/O |22 ca admission model;19 ca join model;5 controlgreen+5 mapping mutantred |Không gọi là A1–A12productN/N |
|Issue#488write_set |**chua_do_duoc** |Biết3 path theo user, không có tên/rawbody để soexactset |
|Full suites/81mutant/1709selftest/adr-song47/47/CI5ff6cd5 |not_run hoặcchua_do_duoc |Không nhận lờiđiềuphối thành số tựđo |

`source-audit.json` đọc lại chính blob `ops/lease_publish.py` của base và `origin/master`: `_kiem_bia_mo` còn `any`, không có hằng profile hoặc lệnh admission mới.

**Không phát hiện con số sai được dùng chống đỡ lời khai thẩm quyền.** 47/47, APIactor, launcherbytes/duration và rawIssue là lời khai có nguồn/giới hạn, chưa phải quyềnchochạy/land. Số scan/comparison của review không được gán cho runtime chưa viết.

## chua_do_duoc

1. Raw body/projection/comments Issue#488: IDbinding/mission/ngoại lệstandalone nếu có, dependencyID/phase/landobligation, exact3 path, actualspec_hashreadback/updated_at. Chỉ có các trường user trích và EVIDENCE120; không tự dựng raw giả.
2. Raw launcher7a,run7 và lệnhcomment09-09: facts từuser/EVIDENCE; không tự chứng nhận modeltoken/output từstdout0, không xác minh thời lượng/byte/auth. Không đọc credentials/tài liệu ngoài cwd.
3. Implementationr9 chưa có: fullM1×consumer, native A10 với state từ init+5 cửa, A1–A12N/N/catalognative, full121/278/81, base/candidatenameddelta và E2E≤2. Modelguard/schema/join không thay implementation.
4. Các hướng cấm chỉ mô tả, kể cả bytesmismatch seam và source-negative. Không chạy fullsuite cũ có ca ngoài phân công; chưa có rawnegativefixtuređiềuphối.
5. Profile/runner/image/helper/runtime/trust/secret-source/proxy/CAproduction; approver cụ thể. **Không phải finding**. Manifestfixture chỉ kiểm serialization/compare, không chứng nhận trust thực.
6. Támdefaultbudget trên mọi rootsdeployment; per-object8MiB/bộ50000 object/full10000 parent edges và thời gian60s/memory/cancellation thật. K đo sáucounterthu nhỏ, alternateGit thật và childdeadline0,1s; không chứng nhận overhead/setup/fetch/deployment.
7. Actions raw check/suite/run/attemptjobs/artifact download/digest/pagination, actualworkflowdefinitionS≠H, tokenreadscopes/upload/canary của workflowmới. Đường API trongr9/J vẫnđềxuất; không mạng để xác minh fields/association thực.
8. Ruleset/requiredcheck/bypass/directpush/queue/strict/currentS/H/treeM; publisher/consumer landed, bootstrapaudit/freeze/firstreceipt/journal/retention/readback, activationbindingQ13 và mốcA0. Reviewer không thực hiện chúng.
9. Q8authorizationcomment r2khôngđích; Q9decision; workerstop/lastSHA/stalegeneration/g3lease/holderreadback. Không cấp lại hoặc thu hồi bằng verdict.
10. Map303 ref/1186object/4.311.029B/2622commit ởlượt5 khôngtái lập exact vìscratchcũmất. Không dùngmap310bácclock/mapcũ. Freshness server nay không đo vìmirror08-09khôngfetch.
11. Keyring/chữký/signer thật và ranh giới “chủ kho gõ” với “agent cầmPAT”; rawgpgsig khôngchứngminhhuman. GateCI/d612ced/bfb0f9a/5ff6cd5/20ad2db, selftest1709 vàreleaseverify/adr-song47/47 theoEVIDENCE khôngtái lập từbase đã giao.

### Kiểm tra hiện vật cuối

`HINT.patch`: **1 hunk, 2,197 byte**, sha256 `10e35e99a05880d731f34cf6163d254e018174379a92f87d71a4b81a49142433`. Dry-run `patch --batch --fuzz=0 -p0 --dry-run` và áp thật bằng `patch -p0` **chỉ trên bản sao** đều rc0; bản sau áp byte-match `scratch/luot8/SPEC.hinted.md`, sha256 `5b71fc3ad4f463e9e18515bf9042e59ae555be3f815cdedba6e4944f97f52848`. S11 là ghi chú cho hồ sơ A0; không áp hint vào r9 đóng băng, không sửa ADR.

`final-checks.json`: hash SPEC/ADR/bản r8/VERDICT7/HINT7 và hai bản untracked giữ nguyên; HEAD/tree/ref map/status/abbrev/shallow giữ nguyên; tracked/index diff rc0. **109 hiện vật cũ** ở lượt6/7 khớp hash preflight, không sửa script cũ. Đủ các section bắt buộc; JSON control/oracle/native đều có bằng chứng dương đúng phạm vi. Manifest `scratch/luot8/ARTIFACTS.sha256` kê script/output mới; dữ liệu nháp ban đầu không thay replay-clean.

Hoàn tất 2026-09-09T11:19:43.288836+00:00; 1401.3 giây từ mốc user, trong trần60phút. **0 P1; changes_requested chỉ S11/P2 ở hồ sơ packet A0. S8/S10 ĐÓNG. Không yêu cầu revision SPEC r9 vì P2 này; không tự mở lượt review P1 tiếp.**
