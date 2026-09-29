verdict: changes_requested
reviewed_spec_sha256: ef9b3700514921d4cabe95947f86937fc36f4aecf2f4e2e39587cafe88a9bb20
model_tu_khai: OpenAI Codex qua API và công cụ shell trong sandbox; cấu hình phiên mô tả GPT-6. Không có chứng thực độc lập variant backend hay effort; không suy gpt-6-astra/xhigh từ tiêu đề, lời khai điều phối hoặc GitHub submitter. Transport công cụ là machine, không phải ChatGPT Web human-mediated.

Review **đặc tả r3**, chưa có implementation thu hồi để nghiệm thu. **10 finding mới/còn lại được cụ thể hoá: 9 P1 + 1 P2**; không cộng các ID lịch sử trùng nguyên nhân vào con số này. N1–N11: **6 ĐÓNG, 3 ĐÓNG-MỘT-PHẦN, 2 ĐÓNG SAI**. Với 14 finding lượt 1: **7 ĐÓNG, 7 ĐÓNG-MỘT-PHẦN**; finding packet-loop từng ĐÓNG SAI nay đã đóng đúng về hợp đồng target ID/ba trạng thái.

Base Git `b416830ef2a509d60203d55552ce17950afcf67c`, tree `266a2aba97d925dac3ab7473dda55adb0fe23b8e`, core.abbrev=7. Bản SPEC trong `cay-kho` khớp hash trên. Chỉ đọc kho; mọi copy/fixture/đột biến ở `scratch/`. Không commit/push kho, không mạng, không đọc đích origin ngoài cwd. Origin thật trong config không nằm trong cwd nên **không gọi ls-remote vào origin ấy**; bare nội bộ chỉ dùng thử hành vi, không là thẩm quyền độ tươi. Không tự dựng payload đường thoát cây, đồng tự Unicode hoặc chuỗi thoát; các ca ấy ghi not_run.

`HINT.patch` là unified diff **chỉ sửa chữ của SPEC.md**, đề xuất revision tiếp theo cho mọi P1/P2 bên dưới; không phải patch mã workflow/authority do reviewer viết hộ executor. Nhãn: **chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm commit**. Hint thay đổi thiết kế/bootstrap và prerequisite, không chứng nhận các dependency/ngoại lệ đã được cấp. Đã dry-run và áp trên bản sao; bằng chứng cuối ở phần cuối verdict.

Chỉ thị trực tiếp lượt này cho phép hoàn tất review/artifact trong sandbox. Nó không làm lời khai của SPEC §0 về quota PR trở thành đúng; R10 phân biệt hai việc này. Theo phạm vi tiền thi công được giao, dùng `changes_requested` để sửa hợp đồng, không tự mở Issue/lease hoặc chuyển thành executor. Nếu gặp các thiếu sót này trong thi công một packet đã ready thì §3.2 yêu cầu `blocked` và revision.

## Bảng finding lượt 1–2 → trạng thái

ĐỐI CHIẾU LƯỢT TRƯỚC. “ĐÓNG” ở đây là đóng finding cụ thể trong **hợp đồng r3**, có chạy lại phản chứng khi có thể; không có nghĩa code mới đã tồn tại. `P` = `scratch/probes-r3.json`; `E` = `scratch/extra-r3.json`; `F` = `scratch/followup-r3.json`; `L` = `scratch/loop-r3.json`; `D` = `scratch/measure-r3.json`. Các script/log/trace cùng tên nằm trong scratch. Mọi hạng lịch sử được giữ nguyên.

| id | hạng | trạng thái | bằng chứng |
|---|---|---|---|
| N1 canonical-remote-identity-unbound | P1 | **ĐÓNG-MỘT-PHẦN** | Q4: đổi origin trực tiếp sang B hoặc insteadOf sang B nay 12 (`new-q4-origin-redirect`, `r3-q4-insteadof`). Nhưng `remote.origin.vcs` giữ get-url canonical, discovery rc0 trả sổ B; đổi config giữa hai lời gọi cũng được. R1. |
| N2 snapshot-pinned-after-unverified-recapture | P1 | **ĐÓNG** | Q4.2–5 đã capture trước, lấy canonical OID từ advertisement đã so, không recapture. `q4-snapshot-move` giữ OID; `new-q4-recapture-after-compare` mutant đổi OID và bị assertion phân biệt. R2 là vector replacement-object khác, không phủ nhận việc đã sửa đúng race recapture. |
| N3 admission-workflow-does-not-cover-canonical-updates | P1 | **ĐÓNG-MỘT-PHẦN** | M9 riêng, không còn thừa kế ops/path/author/rc9 filter: ma trận F theo hợp đồng mới nhận cả PR docs/integration/bot/standalone. Nhưng workflow đầu tiên vắng ở A0, và M9 fetch PR head không bảo đảm exact cây/current base sẽ land. R3/R5. Không khai đã chạy GitHub Actions. |
| N4 canonical-checker-bootstrap-is-circular | P1 | **ĐÓNG SAI** | Predecessor có thể cung cấp command: base thật vẫn rc2; stub chỉ chứng minh code A0 đã canonical có command→0. Tuy nhiên A0 không cài M9, A1 muốn workflow mới chạy từ base trước khi nó tồn tại; cổng thay thế nằm trong mã PR. Rig: thêm record→1, thêm record+xóa test→0/1-of-1. Cờ False chỉ làm reader 12; không tạo trusted admission. R3/R4. |
| N5 effective-write-set-and-symlink-resolution-missing | P1 | **ĐÓNG SAI** | Alias nội bộ nay resolve cùng docs/a.md→11, sửa được phản chứng cũ. Nhưng nhánh mới “có effective thì dùng” nhận self-declared []: raw overlap11→0, cả phía ứng viên hoặc holder trong fixture. Native lease parser cũng nhận trường thêm này, rc0. Fallback raw thiếu companion vẫn0 thay vì11 theo §5. R6; nguồn cây/vòng còn R7. |
| N6 historical-cutoff-revives-feature-holders | P1 | **ĐÓNG-MỘT-PHẦN** | Đã nói đúng bốn gate và cổng delta trước A1; E chạy lại old={r4}, new={r1,r2,r3,r4}, r4=8 nên A1 phải chặn ở snapshot này. Nhưng A0 đã áp vị từ trước cổng; zero eligibility mắc cả g2 trước C; chờ gate cuối làm g2 hết hạn. Mốc “lúc A0 land” cần ghi cụ thể vào A1 sau readback. R4/R8. |
| N7 candidate-map-omits-entry-mode | P1 | **ĐÓNG** | M1/M4 map full tuple, full namespace T. Git commit đổi 100644→120000 cùng blob nay gate8; S/T tuples trong P. Thêm hợp lệ0. R9 là lỗi chọn mutant A8 mới, không phải mode còn lọt cổng tuple. |
| N8 record-lease-guard-has-no-candidate-id | P1 | **ĐÓNG** | Q5/M7 nhận target ID; L chạy state init thật, record-lease sống0/leased, revoked8/stale/event1 đúng X, không record_lease; unknown8 byte-match. ID từ state cũ mutant vẫn8/awaiting_lease, không đạt postcondition. Bốn route khác cũng có controls. |
| N9 acceptance-prepublish-and-second-parent-contradictions | P1 | **ĐÓNG** | Q3/A5 tách pure0/0 với CLI chưa publish12; E kiểm exact pair và namespace. A8 parent2 giữ sổ0, mất sổ8 bằng Git thật. Hai assert trái nhau của r2 đã được sửa; lỗi A8 mutant khác ở R9. |
| N10 authorization-json-and-url-contract-is-open | P2 | **ĐÓNG** | Q2 chỉ Issue comment, phân biệt number/global ID, đúng6 khóa, type equality, duplicate cấm; chạy lại float/duplicate đều8, control JSON đúng0. URL/endpoint contract đã đóng bằng chữ; không khai đã readback object GitHub. A9 nên viết rõ JSON envelope12/JSON command8 như Q2, hint đã đồng bộ. |
| N11 readback-after-admission-lifecycle-undefined | P2 | **ĐÓNG** | Q2.3/A9: chưa canonical phải đọc lại delta mỗi lần; sau canonical không đọc căn cứ cũ. Stateful API200→404: sau admission Y0, thêm0 API call; nếu chưa canonical lần kiểm mới12. Không còn phụ thuộc URL lịch sử mutable để cấp lại. |
| L1 authority-signature-evidence-false | P1 | **ĐÓNG** | Raw Git: b416830 có1 gpgsig PGP; 6635379 có1 gpgsig SSH/2 marker BEGIN-END. R3 sửa lời khai đếm2 và tách API login khỏi raw author. D.signatures. Không xác minh signer. |
| L1 default-ref-is-untrusted-cache | P1 | **ĐÓNG-MỘT-PHẦN** | Local symref giả không đổi nguồn; server main thắng master; thiếu/mismatch bị chặn. Endpoint/transport vẫn R1 và nội dung OID vẫn R2. |
| L1 standalone-revocation-has-no-admission-gate | P1 | **ĐÓNG-MỘT-PHẦN** | M4 standalone gọi API1,404→12; M9 mới có chủ ý phủ không phụ thuộc lease. Nhưng chưa đóng bootstrap/provenance/exact candidate R3/R5; không dùng counter bên trong hàm thay việc workflow phải được tạo. |
| L1 evidence-mention-is-not-an-authorization | P1 | **ĐÓNG** | Prose phủ định và ID X-extra đều8 dưới parser command; control0. Câu chữ Q2 đã yêu cầu intent/scope/type, không dùng substring. |
| L1 write-set-exclusion-is-incomplete | P1 | **ĐÓNG-MỘT-PHẦN** | Không thay thế/prefix/case-fold đều11; alias mới11. Chưa đủ closure/provenance và ngữ nghĩa giải cây R6/R7. Nhánh effective tự khai của bản sửa tạo lỗi mới đã đánh ĐÓNG SAI ở N5. |
| L1 snapshot-check-does-not-fence-writers | P1 | **ĐÓNG** | R3 thừa nhận pure trước publish0/0, sau publish11/11; check không acquire; Q11 dừng worker/cấp/readback/bắt đầu tuần tự, land fencing là nợ công khai. Không chứng minh workflow race hoặc cancellation production đã được thực hiện. |
| L1 reads-are-not-pinned-to-one-snapshot | P1 | **ĐÓNG** | Race đọc tên/recapture cũ đã sửa và chạy lại. Đọc OID đã so giữ kết quả, stale SHA từ đầu12. R2/R7 là các thiếu sót mới về diễn giải object và map/source cây, không phải tái nhận recapture r2. |
| L1 legacy-fallback-conflicts-with-ledger | P1 | **ĐÓNG-MỘT-PHẦN** | Legacy old-copy0; sổ đích Z thắng bia X→Y nên8; Y chết lịch sử8. Thuật toán precedence/áp ID đã đóng, cutover/activation R4/R8 chưa đóng. |
| L1 append-only-check-misses-candidate-and-merges | P1 | **ĐÓNG-MỘT-PHẦN** | Candidate sửa8, merge ours bỏ sổ8 dù log0 byte, parent2 giữ0, mode8. Còn M9 chọn H/base cũ thay candidate thực R5 và bootstrap R3. |
| L1 packet-loop-guard-is-partial-and-boolean | P1 | **ĐÓNG** | 5×4 route/status đã chạy qua parser/entrypoint thật với guard r3 trong bộ nhớ. Revoked stale/event1/idempotent; unknown byte-match; record-lease có target. Mutant helper-only vẫn cho ba route sau0→accepted. Không nhầm positive state với lỗi snapshot. |
| L1 acceptance-confuses-refs-blobs-and-mutations | P1 | **ĐÓNG-MỘT-PHẦN** | A1=3 cặp/4 ref, A2=1 cặp/3 ref; fixed clock, CLI/pure và parent2 đã sửa. A8 mutant cụ thể vẫn sống (R9); A11 bootstrap PR tự xoá catalog vẫn xanh (R3); smoke g2 hết hạn R8. |
| L1 revocation-schema-and-error-contract-incomplete | P2 | **ĐÓNG** | M1 giữ schema/type/ID/mode/error precedence và consumer mapping đã đóng r2. R3 thêm JSON chặt Q2. Không có cơ sở nói parser chưa viết đã pass toàn bộ schema matrix. |
| L1 size-estimate-and-slice-anchor-are-stale | P2 | **ĐÓNG** | Mốc409/368/328 và31 commit đo lại khớp. R3 sửa câu tuyệt đối mọi slice vượt300; tổng725–1055, A0 vượt, A1/B/C dưới ước. Còn lựa chọn bootstrap/ước lại do finding mới, không phải sai phép cộng cũ. |
| L1 ready-and-rollout-decisions-are-not-closed | P2 | **ĐÓNG-MỘT-PHẦN** | Q12 bỏ đòi code mới chạy trước lease A0, phái sinh không được miễn. Còn nguồn transport, closure, bootstrap, cutover, exact candidate R1/R3–R8; Q10 thiếu các điều kiện cụ thể ấy. |

## Findings mới

Các phản chứng dưới đây là **Git/process thật + mô hình vị từ r3 ghi rõ trong script**, không phải verdict chạy trên implementation tương lai. Nêu một cách thực hiện tuân thao tác được r3 viết nhưng trái bất biến là đủ chỉ ra hợp đồng còn thiếu; không suy mọi executor sẽ mắc đúng cách đó. Các R-ID là nhãn tra nhanh, stable ID là kebab-case ở heading.

### canonical-url-check-does-not-bind-transport · P1 · R1 · Q4.1–3, A2/A6, M7/Q12

**TÁI HIỆN:** P.`r3-q4-remote-vcs-helper`: origin có URL `https://github.com/ducthangho/tra-luat`; cấu hình repo chọn `remote.origin.vcs=rv3fixture`. Helper chỉ phục vụ bare B trong scratch. `git ls-remote --get-url origin` vẫn in URL canonical; discovery rc0 trả HEAD symref master cùng OID B. Cache master được đặt đúng OID B, nên đủ phép so r3; B có X trong sổ, bare A làm nguồn canonical đối chứng không có. Không gọi mạng. P.`r3-q4-config-race` cũng kiểm URL canonical trước rồi đổi origin giữa get-url/discovery: discovery nhận B mà hằng identity đã qua.

Đối chứng: insteadOf trực tiếp sang B làm get-url đổi và r3 chặn12. pushInsteadOf chỉ đổi push URL, read get-url giữ canonical; **không dựng được bypass reader từ riêng pushInsteadOf**. Bỏ scheme như r3 cũng chưa định nghĩa allowlist transport/xác thực; URL text không chứng minh TLS/SSH endpoint hoặc helper thực.

**Vì sao:** N1 sửa đối tượng được so nhưng vẫn tin runtime config chọn cách đọc. “Ghim trong mã” không ràng buộc hai lời gọi dùng cùng transport. Không cần phá GitHub protection thật: reader đã đọc một nguồn khác như canonical. Threat model của phản chứng là config/helper selection không tin cậy như chính đề bài Q4, không tuyên bố chống máy chạy bị kiểm soát hoàn toàn.

**GỢI Ý VÁ:** adapter nguồn có endpoint/transport đã xác minh, discovery không chịu config repo/candidate, không dùng tên origin sau get-url để tái chọn nguồn; cấu hình credential/proxy hợp lệ do deployment tin cậy cấp, có ca xanh. get-url là diagnostic, không là chứng thư. Profile không đo được→12, không TLS-insecure/CLI override. M7 chỉ cần Git adapter này, không thêm REST. Hint Q4/A2/A6/Q12; ca helper và config race phải bị chặn hoặc không còn đổi được nguồn.

### replace-refs-bypass-oid-pinning · P1 · R2 · Q4.5, M1/M4, A6

**TÁI HIỆN:** E.`r3-replace-ref-counterfeit-tree`: Git commit S0 không có sổ; S khác có X. Trong scratch thêm replacement S0→S. Cùng lệnh `ls-tree -r <S0> -- ops/thu-hoi` trước trả rỗng, sau trả record X. Đối số OID không đổi. `git --no-replace-objects ls-tree ...` lại rỗng. JSON giữ full OID, path/mode/blob và raw output.

**Vì sao:** Git porcelain/plumbing thông thường có thể diễn giải OID qua refs/replace. Q4 chỉ yêu cầu dùng OID đã ghim, không vô hiệu hoá lớp diễn giải này. Advertisement/cached SHA đúng không bảo đảm tree đọc được là tree của commit canonical thật; reader sau admission lại không readback căn cứ lịch sử (đúng N11), nên source boundary phải bảo đảm tree thật. Cùng vector có thể làm sai ancestry/append-only.

**GỢI Ý VÁ:** mọi đọc tree/blob và phép ancestry/diff sử dụng raw object/DAG với replacement vô hiệu hoá; cô lập hoặc từ chối graft/config làm đổi DAG. Scope phải gồm M4, không chỉ loader sổ. Ca replacement trước/sau snapshot giữ tree gốc hoặc12; mutant gỡ chốt phải đổi holder/record và bị bắt. Hint Q4.5/A6. Không giải bằng quét tên ref sau mỗi lần đọc.

### bootstrap-gate-trusts-pr-and-arrives-too-late · P1 · R3 · write_set A0/A1, M9, A11/A12, Q7/Q10

**TÁI HIỆN:** P.`r3-bootstrap-pr-deletes-test` chạy rig test registration tối thiểu cho đúng predicate A0: rỗng→rc0; thêm X→rc1; giữ X và bỏ riêng ca rỗng→rc0, output1/1. Đây là **mô hình executable của chốt tương lai**, không giả suite A0 đã có. YAML thật `ci.yml` có lane pull_request, checkout ứng viên và `run: bash ops/chay_lease_publish_test.sh`; bằng chứng đối lập nằm ngay trong `duyet-khac-danh-tinh.yml:16–31` về chốt PR tự sửa.

R3 A0 chỉ có hai file Python; M9 workflow mới nằm A1. Vì vậy canonical base sau A0 không có definition M9 để chạy cho PR thêm M9 đầu tiên. F.`new-m9-canonical-command-bootstrap` chạy lại phản chứng command: base thật rc2; stub có command được lấy từ OID A0 fixture→0, nhưng chỉ chứng minh **có executable**, không sinh workflow từ một base chưa có nó.

**Vì sao:** test PR là regression evidence, không là biên authority chống PR sửa chính test. Cờ False/nonempty→12 là fail-close của reader, không ngăn record bẩn land trước activation. Không được bỏ qua record ấy ở lần activation vì nó đã thuộc S và Q2 chỉ đọc delta mới; cũng không được coi reader outage12 là bootstrap thành công. Q10 đòi facts trước True trong khi A1 đồng thời mới tạo workflow/True, vẫn có vòng khởi động.

**GỢI Ý VÁ:** rẻ hơn và chặt hơn là bỏ ý tưởng tự bảo vệ bằng một ca CI PR. A0 đưa cả code và workflow tin cậy lên canonical, giữ inactive. Lần land A0 đầu cần audit exact S/H/tree rỗng + review hiện có và khoảng bootstrap được điều phối đóng; sau đó cấu hình/readback required check và chạy workflow canonical A0 trước A1. Cổng A0 kiểm S/T rỗng bằng mã A0, bất kể PR xóa test/wrapper/workflow. A1 chỉ activation sổ rỗng; C mới thêm record. Nếu không có biên bootstrap ngoài kho đạt được thì giữ proposed/inactive, không nới bằng skip. Hint write_set/M9/A11/A12/Q7/Q10.

### inactive-a0-already-changes-lease-decisions · P1 · R4 · Q3/Q6, M2/M3, slice A0/A1, A7/A11

**TÁI HIỆN:** P.`r3-a0-changes-before-activation`: fixture lịch sử X→Y hợp lệ, old check Y0. A0 được giao M3 precedence Q3(2) nhưng BIA_MO_LICH_SU chỉ ghim ở A1: áp vị từ mới khi danh sách chưa có→8. A1 có danh sách→0. Nếu executor tự tính một danh sách tạm ở A0 thì đó là một cách ghim thêm chưa được spec quy định. Với dữ liệu thật, E/F còn đo các delta gate/g2 mà Q6 chỉ đòi kiểm tại activation A1.

**Vì sao:** `SO_THU_HOI_KICH_HOAT=False` được viết cho sổ rỗng/nonempty, không nói M3/Q6 vẫn giữ luật cũ cho tới A1. Phân slice đã giao các thay đổi cổng production cho A0. Vậy A0 có thể làm check/holder đổi trước cổng delta và trước khi history/policy được cung cấp. “A0 hữu ích như phép đo” không tự biến M3 thành diagnostic-only. Đây là mâu thuẫn hành vi giữa slice, không phải đòi implementation mới phải tồn tại trước lease viết nó.

**GỢI Ý VÁ:** chốt rõ inactive giữ quyết định lease cũ trên đầu vào hợp lệ/sổ rỗng; tính luật mới ở hàm dự báo có nhãn, không cấp quyền. False/nonempty vẫn12. M4 validator ứng viên tách khỏi consumer runtime; activation mới bật toàn bộ semantics mới cùng mốc/closure. Ca A0 old/new phải so verdict sản phẩm lẫn dự báo, mutant gọi vị từ mới sớm→đỏ. Hint Q3/M3/A7/A11/Q7.

### admission-head-is-not-the-landed-candidate · P1 · R5 · M9, M1 append-only, Q1/Q10, A8/A11

**TÁI HIỆN:** P.`r3-m9-base-drift`: S0 chưa có X; H thêm X đích Y→M4(S0,H)=0. Base tiến tới B đã có X đích Z. Cây merge M hai cha B/H chọn nội dung H cho X: M4(B,M)=8 vì sửa event canonical. Receipt cũ S0/H vẫn0. Đây là commit Git thật, có full parents/OID/tree; **không phải đã merge được trên GitHub production**. Control cập nhật H2 chứa B giữ X đúng→0 và merge tree bằng H2.

M9 chỉ ghi fetch `refs/pull/<n>/head`, chưa so OID nhận với event `head.sha`; checkout “base như workflow kia” có thể là `base.ref` trôi trong khi đối số S là `base.sha`. Workflow base-update không nằm trong types; edited/retarget cũng vắng. workflow_dispatch không nêu PR/S/H input hay nguồn definition được tin. Nhìn thân lệnh khi đã được gọi không chứng minh check được tạo hoặc được gắn đúng H.

**Vì sao:** M1 đòi exact cây sẽ nhận nhưng M9 đưa PR head cho nó. Có thể chặn oan PR khi S không là ancestor H, hoặc dùng receipt trước drift nếu ngoài kho không thực sự buộc current candidate. Q10 nói “neo đúng S/T” là mục tiêu, chưa định nghĩa cách GitHub/check/land bảo đảm mục tiêu đó. Không được suy comment receipt là required check, hoặc workflow target/dispatch mặc nhiên chứng thực PR head.

**GỢI Ý VÁ:** chọn cụ thể S=current canonical đã xác minh, H=event/readback PR head và fetch OID phải bằng H; code checkout exact S. Receipt ghi S/H/tree T/checker OID, phân biệt merge commit M. Strict require-branches-up-to-date **có thể loại ca Git drift ở trên** khi được cưỡng chế tại merge, không bypass và tree merge bằng H. **Một mình setting đó chưa đủ** cho code S, fetched H, check provenance, race sau check, dispatch/retarget hoặc merge queue. Cần re-run khi S/H đổi, land/current base/tree equality hoặc lane merge_group cho exact candidate; chưa hỗ trợ queue thì chặn. Hint M9/Q10/A8/A11; facts ngoài kho vẫn phải đo.

### self-declared-effective-set-shrinks-exclusion · P1 · R6 · Q3.166–177, A5, Q10/Q12, protocol §3.2/§5

**TÁI HIỆN:** P.`r3-effective-set-shrink`: Y.raw={p}, W.raw={p}→11. Thêm `effective_write_set: []` cho Y theo nhánh ưu tiên r3→0; fixture chỉ W có trường rỗng cũng0. E.`r3-native-lease-allows-self-declared-effective`: native baseline check g2 original0, g2 thêm trường rỗng0. Native probe chỉ chứng minh parser hiện tại không xác thực nguồn field; phép giao r3 là mô hình độc lập, không gán nó cho code chưa viết.

P.`r3-missing-policy-closure`: W.raw={SKILL.md}, Y={references/GOTCHAS.md}: fallback raw0; closure §5 có companion→11. D xác nhận policy lẫn schema đúng vị trí protocol đều vắng, không chỉ path schema mà r3 nêu.

**Vì sao:** ngoặc “dispatcher điền” là lời khai, không có comparison/provenance enforce. Spec cho chính dữ liệu lease được quét quyết định bỏ bớt set. Đây là lỗi mới so với raw-only r2. Mặt khác §5 bắt effective exclusion toàn kho, §3.2 cấm agent tự khai phái sinh; gọi closure là debt không cho phép bật semantics cấp quyền trên raw fallback. Q12 yêu cầu policy SHA trước ready nhưng Q3 lại thiết kế fallback khi policy vắng; phải chọn một hợp đồng thống nhất.

**GỢI Ý VÁ:** tính lại closure từ policy canonical đã ghim, đối chiếu authority/spec_hash/revision/generation và effective field; raw set phải nằm trong closure. Sai khai→8, thiếu nguồn không tính được→12; không tin field có mặt. Đóng dependency #473 hoặc ngoại lệ riêng có authority trước quyền ghi; không lan miễn trừ b416830. Test thêm trường rỗng/thu hẹp/thiếu companion ở cả Y/W và missing-policy, với controls authoritative đúng. Hint Q3/A5/Q10/Q12; không tự thêm file policy ngoài write set.

### symlink-resolution-lacks-source-and-termination-contract · P2 · R7 · Q3.171–176, Q4.2/5, A5/A6

**TÁI HIỆN:** P.`new-q3-symlink-alias` đã đóng vector đơn giản: alias trong tree trỏ docs, hai path resolve cùng docs/a.md→11. F.`r3-symlink-source-tree`: **cùng lease blob/path** ở S/T, S có alias trỏ other, T có alias trỏ docs. Resolve theo canonical S→other/a.md, không giao W.docs/a.md, rc0; resolve theo occurrence T→docs/a.md, rc11. Cả hai OID đều là snapshot hợp lệ; r3 không nói dùng OID nào cho một cặp dedup qua nhiều ref.

P.`r3-symlink-cycle` tạo hai symlink tương đối A↔B hoàn toàn trong tree. Resolver an toàn bổ sung visited-set kết thúc12; r3 chỉ nói đọc đích/chuẩn hoá/so, chưa có bound/vòng hoặc verdict. Ca tuyệt đối/trỏ ngoài cây/NFC payload bị cấm **not_run**, chỉ mô tả bằng lời. Q4 capture duy nhất remote-tracking map trong khi đơn vị quét gồm local heads; chưa nói OID của local-only occurrence được ghim lúc nào.

**Vì sao:** executor phải chọn nguồn cây, thời điểm dedup, xử link ở parent/file mới/prefix và vòng; các lựa chọn cho verdict khác nhau hoặc không kết thúc. Thứ tự case-fold trước Git lookup cũng cần phân biệt comparison key với tên entry thật. Không dùng filesystem của container giải symlink của một OID khác.

**GỢI Ý VÁ:** giữ nguồn OID từng occurrence và map local/remote trước so; resolve theo đúng cây có liên quan, hợp conservative các đường logic/đích trước khử trùng. Định nghĩa relative target từ parent, absolute/outside→12, visited/bound→12, parent missing cho file mới, prefix có symlink, lookup raw name và canonical comparison. Thay đổi cây/policy làm closure đổi phải re-evaluate trước quyền ghi. Hint Q3/Q4/A5/A6; các lớp bị cấm do điều phối dựng.

### cutover-delta-and-fixed-g2-smoke-conflict · P1 · R8 · Q6.235–253, A1/A3, Q8/Q10/Q12

**TÁI HIỆN:** E/F đọc dữ liệu hiện có, clock14:33:15: gate old holder={r4}, new={r1,r2,r3,r4}, r4 check8. R3 đã bắt delta này. Nhưng **g2 cũng có eligibility delta**: native old check0; r3 Q3(2) chưa có sổ r2 và không có cặp r2→g2 ở mốc b416830 nên8. Q6 đòi bảng “người giữ/eligibility cũ vs mới” delta0 trước activation A1, trong khi C cần A1 để ghi event làm g2 hợp lệ: vòng ở dữ liệu mục tiêu, không chỉ ở gate.

Phương án r3 nêu chờ hết hạn có phép đo quyết định: gate cuối hết `2026-09-08T10:17:12Z`, g2 hết **09:52:00Z** cùng ngày. Chạy clock tại10:17:12 trên frozen data: g2 HẾT_HẠN; sau event C tập holder wp461 rỗng, không phải1 g2. R3 câu “trước bất kỳ mốc A0 khả dĩ nào” không có phép đo/schedule bảo đảm và không suy được từ expiry. Không khẳng định mọi A0 tương lai bất khả thi: một cây/migration plan mới có thể khác, nhưng r3 chưa quy định nó.

**Vì sao:** điều kiện cutover gộp thay đổi bảo thủ dự kiến và sai lệch cần cấm thành zero tuyệt đối, làm đích C thành prerequisite của A1. R3 vừa cho chờ vừa giữ hậu điều g2 cố định, nên theo nhánh chờ ấy implementation đúng không thể xanh smoke. Việc đã gắn nhãn số liệu theo thời điểm không cứu được assert dự kiến sai sau thời điểm ấy.

**GỢI Ý VÁ:** chốt một kế hoạch cutover có authority với delta theo ID/path/eligibility, phân biệt conservative block dự kiến trước C, removal có nguồn hợp lệ và delta không giải thích được; loại cuối chặn. Dừng lane bị ảnh hưởng, không tự bỏ holder để làm xanh. Đặt rõ pre/post-C, hạn đích và đường revise C/Q8 khi g2 hết hạn; không tự gia hạn/tái dùng ID. Q6 mốc có cách đo rẻ: readback **OID A0 cuối sau land**, A1 mới ghi hằng/mảng được dẫn xuất từ OID ấy, không nhúng own-final-SHA vào A0 hoặc quét HEAD A1. Ca hai cây X→Y ở mốc, Z→W ở sau: fixed checkW8, mutant mở danh sách0; P đã chạy và phân biệt được. Hint Q6/A1/A3/Q10/Q12.

### a8-mode-case-cannot-kill-stated-mutant · P1 · R9 · A8.369–373, M1/M4

**TÁI HIỆN:** E.`r3-a8-shielded-single-mutant` chạy cùng commit đổi mode giữ blob: gate r3 đầy đủ→8; mutant **chỉ validate phần thêm**, nhưng giữ nguyên tuple-map mà r3 bắt buộc→**8**. `stated_mode_case_kills_mutant=false`. So map chặn trước full-M1(T), nên ca không quan sát được việc bỏ validation toàn namespace.

**Vì sao:** A8 vẫn hứa mutant này sẽ lọt đổi mode, trong khi chính N7 vừa thêm một chốt độc lập chặn nó. Đây là P1 theo rubric “tiêu chí không thể đỏ với đột biến được viện ra”; **không phải khẳng định mọi A8 là hằng-xanh** hay mode còn fail-open. Khi S đã hợp lệ, tuple giữ nguyên cũng làm schema entry cũ bất biến; test full-validation cần xác định riêng đường gọi/tiền điều kiện thay vì gán công cho một chốt không chạy tới.

**GỢI Ý VÁ:** công khai single mutant này sống dưới ca mode; dùng mutant kết hợp map blob-only + chỉ validate phần thêm để tái hiện lỗ mode thật, hoặc tách unit trực tiếp của full-T validator với input lỗi/đối chứng. Không sửa assert thành mong0 ở bản tuple đúng. Giữ case mode8 và các cases Git merge/parent2. Hint A8/A11/A12.

### spec-review-label-does-not-waive-review-cap · P1 · R10 · §0.30–34, hinh_dang_ke_thua, protocol §8/§12

**TÁI HIỆN:** đối chiếu văn bản thật: protocol `docs/PROTOCOL_DA_PHIEN.md:806–816` nói tối đa hai Codex review **trên cùng PR**, checkpoint khi chạm trần, đổi prompt/session không reset. §8:579 cũng giữ trần. Không có ngoại lệ “review spec trên PR không tính như code”. SPEC §0 đưa chính phân biệt ấy và lời chat được chép vào spec/PR làm căn cứ tiếp tục lượt≥3; bundle không chứa raw readback owner object/budget quyết định.

**Vì sao:** đây là mâu thuẫn luật, không phải yêu cầu reviewer bỏ việc đang được user trực tiếp giao. Chỉ thị lượt này ưu tiên trong phiên này và đã được thực hiện; nó không tự chứng minh exception bền cho automation tương lai. Giữ counter đúng nhưng tiếp tục vô hạn theo khẩu hiệu vẫn không tuân stop condition; R1 còn chứng minh hình dạng identity thất bại lặp tiếp tới r3.

**GỢI Ý VÁ:** bỏ ngoại lệ suy từ nhãn spec; nêu phạm vi chỉ thị review hiện tại và giới hạn chưa readback. Giữ counts/finding IDs, đóng Review Rescue Checkpoint với revision/thiết kế lại, human audit hoặc pause; nếu thay budget phải có phạm vi/trần/authority bền rõ. Không tự reset khi tách A0/A1. Hint §0/hình dạng/Q7. Không yêu cầu thêm permission để hoàn tất artifact read-only lượt này.

## Phản chứng đã chạy lại + mới

Lệnh chính (đều từ cwd, không installer/mạng):

```text
PYTHONDONTWRITEBYTECODE=1 python3 scratch/measure_r3.py
PYTHONDONTWRITEBYTECODE=1 python3 scratch/probes_r3.py
PYTHONDONTWRITEBYTECODE=1 python3 scratch/loop_r3.py
PYTHONDONTWRITEBYTECODE=1 python3 scratch/extra_r3.py
PYTHONDONTWRITEBYTECODE=1 python3 scratch/followup_r3.py
```

Mọi lệnh cuối rc0. P có **42 mục**, trace207 invocation được ghi; E trace54, F trace33, D trace602. Đây là số **mục trace**, không nhận là toàn bộ syscall/Git invocation (hàm tạo blob còn gọi subprocess trực tiếp). L có **25 tổ hợp**: 5×4 status, 2 mutant ID cũ, 3 mutant helper-only;27 guard calls. Log đầy đủ ở `scratch/logs/`. Script r1/r2 gốc không có trong bundle; các ca được **tái dựng từ VERDICT.luot1/2.md**, không khai đã chạy lại nguyên file harness cũ. Một lỗi rig ban đầu dùng empty pathspec cho ls-tree đã sửa trước lượt thành công; không tính lỗi rig này thành finding SPEC.

**19 ca D3 cũ được tái dựng đủ ID**, kết quả r3 như sau:

| ca | kết quả mới | điều đã/không chứng minh |
|---|---|---|
| q1-symref-authority | rc0, canonical OID vẫn của A dù local HEAD trỏ feature | Đóng local-symref authority cũ; không là phép chứng minh transport. |
| q1-fallback-revived | rc0, chọn main có sổ, không chọn master cũ | Đóng fallback master. |
| q2-no-admission | standalone M4 model đọc API1,404→12 | Chứng minh thân validator; wiring/provenance riêng R3/R5. |
| q2-substring-not-command | prose phủ định→8 | Không còn coi nhắc ID là lệnh. |
| q2-unrelated-prefix | X-extra trong prose→8 | So command exact, không substring. |
| q3-no-replacement-scope | Y không khai thay thế, W giữ p→11 | Exclusion áp mọi lease. |
| q3-prefix-overlap | docs/ với docs/a.md→11 | Comparator prefix đúng control. |
| q3-casefold-overlap | DOCS/A.MD với docs/a.md→11 | Không cần tự dựng đồng tự Unicode. |
| q3-concurrent-replacements | pure trước publish0/0, sau có cả Y/Z11/11; CLI published predicate không có pair→12 | Mô hình predicate r3; không khai hai GitHub push đã race. E kiểm membership riêng bằng tree Git thật. |
| q4-snapshot-move | ref đổi sau so, OID r3 không đổi | M2/N2 sửa đúng. |
| q4-stale-sha-control | cache đúng tên/OID cũ→12 | Static mismatch vẫn fail-close. |
| q6-legacy-old-copy | history X→Y, còn blob X cũ: checkY0, holderY | Áp lịch sử toàn ID. |
| q6-fallback-overrides-reservation | sổ X dành Z, lịch sử X→Y: checkY8 | Sổ thắng, không OR fallback. |
| q6-republish-legacy-dead | history Y→Z: checkY8 | Chiều ngược không chỉ nhìn sổ. |
| a8-normal-modification | ứng viên sửa X→8 | Kiểm T, không quét mỗi canonical. |
| a8-merge-erases-registry | merge ours bỏ X, S ở parent2→8; legacy path log0 byte | Đóng điểm mù Git log; không dùng số dòng log làm số record. |
| q5-existence-boolean | xóa loose blob chỉ trong fixture: Git128, reader model12 | Unknown không bị coi là sổ vắng. L kiểm ánh xạ RC_STATE riêng. |
| a1-cardinality-mutant | X3 cặp trên4 ref; map ref-count2/1/1; correct holderY, known-only mutantX/Y | Blob thứ3 ngoài known-list thật sự phân biệt mutant. Nhãn output sản phẩm mới chưa có để chạy. |
| q1-control-a2 | cùng pair trên3 ref→1 cặp, MAP_REF đủ3 | Không trở lại assert3 dòng sai đơn vị. |

| phản chứng r2 hoặc mới | chạy lại dưới r3 / kết quả mới |
|---|---|
| N1 redirect origin | Wrong repository12; insteadOf12; helper get-url đúng/discovery B0; config race vẫn nhận B. |
| N2 recapture | OID r3 giữ nguyên; recapture mutant khác, bị ca phân biệt. |
| N3 old ops/path/author wiring | Hợp đồng M9 tách riêng đã bỏ các filter cũ; ma trận F là mô hình event, **không** receipt Actions. Còn base drift/retarget/dispatch/source chưa đóng. |
| N4 missing canonical command | Base thật `invalid choice`2; command tồn tại trên A0 fixture0; stub chỉ đo availability. Definition workflow vẫn chưa ở A0 r3. |
| N5 symlink và closure | Alias đơn giản11; nguồn S/T khác cho0/11; effective tự khai rỗng0; raw missing companion0 vs closure11. |
| N6 gate cutoff | Old1/new4, r4check8; activation phải chặn với delta0 hiện tại. Không mở cutoff để giả xanh. |
| N7 mode same blob | Map full tuple→8. Không checkout/materialize entry symlink có nội dung YAML. |
| N8 record-lease | Sống0/leased, revoked8/stale/event1 đúng candidate ID, no record_lease; unknown byte-match. |
| N9 prepublish/parent2 | CLI predicate không pair12; server ordinary/ops/default head đủ exactpair0; same-ID-old-blob/same-blob-wrong-path12. Parent2 giữ0/mất8. |
| N10 float/duplicate JSON | Cả hai8, correct block0. Không có JSON duplicate payload ngoài lớp thông thường được phép. |
| N11 API object sau admission | First200→0; after canonical thêm0 API call/Y0; chưa canonical recheck404→12. |
| git replace | Cùng OID đọc sổ giả sau replace; no-replace đọc tree gốc rỗng. |
| PR xoá ca bootstrap | Empty0; record-only1; record+remove-test0/1-of-1; detector chỉ dựa catalog PR cũng mất ca khi xoá cả registration. |
| M9 drift | Old S0/H0; actual B/M8; strict ancestor control H2/M2 cùng tree0. Không chứng minh GitHub production cho merge ca sai. |
| BIA_MO list tự mở rộng | Mốc chỉ X→Y; cây sau thêmZ→W: đúng checkW8, mutant quét cây sau0. Exact tuple-list phân biệt, không chỉ so “có mốc”. |
| A0 flag False | Hợp đồng M3 mới/history chưa ghim có thể đổi oldY0→8 trước activation. Safe inactive control cần giữ0 sản phẩm và tách dự báo8. |
| A8 single mutant bị chốt khác che | Full gate8 và only-new-validation8 trên cùng mode mutation; ca không giết mutant được chỉ tên. |
| M7 REST vs Git | M7 model guard không gọi REST; sau canonical REST lỗi thêm0call/Y0. Git unknown ở L chặn8/byte-match. Proxy thật container **chưa đo**, không quy REST403 thành Git failure. |

L chạy **entrypoint/parser/state thật của packet_loop**; guard r3 được bọc trong bộ nhớ trước route, không sửa source. Chỉ precondition doctor được stub thành hợp lệ để không lẫn bài toán môi trường; snapshot status là fixture bốn trạng thái, transport Git được thử độc lập ở P/E. Cả5 route có live/feature-only0; revoked8/stale/event1, lặp state không đổi/không tiêu thêm; unknown8/state byte-match. Ba route post/transition/review của nền vẫn0→accepted khi chỉ `_kiem_luoc_do_lease` bị ép chặn. Không nhận đây là đã nghiệm thu implementation M7/root CLI chưa viết, lỗi disk, mọi nguyên nhân clock/schema hay cancellation thật.

## Tiêu chí A1–A12

Audit hợp đồng và khả năng phân biệt mutant; **không** gắn nhãn A1–A12 đã chạy N/N. Mã mới chưa có. “Có thể đỏ” cần input tới đúng chốt và positive control khác họ còn xanh; mutant bị một chốt khác chặn không chứng minh ca đã đo chốt dự định.

| tiêu chí | đơn vị / phép đỏ thật | đột biến đúng ca, ca không thể đỏ/xanh và phần còn thiếu |
|---|---|---|
| **A1** | Holder-ID set,3 pair của X, map pair→refs, expiry/revocation label; fixed clock | Known-only mutant sống X, nên fixture có phép đỏ thật. Bỏ loader/in dòng cũng có assertion phân biệt. Smoke g2 cố định không xanh khi dùng nhánh chờ qua09:52Z (R8); cần tách lịch sử event với quyền cấp lại còn hạn. Output label CLI mới not_run. |
| **A2** |1 pair/3refs; source identity/default/holder, rc12 | Any-ref/local-symref/master fallback có ca đỏ. Wrong-url12 thật, nhưng ca bỏ identity hiện tại chỉ đo spelling URL; helper và config race vẫn qua. Thêm authenticated adapter/transport controls R1, không gọi pushInsteadOf là reader exploit khi chưa có. |
| **A3** | rc của5 nhánh, closed history/precedence | Old-copy0, reservation8, reverse legacy8 đã phân biệt. Ca mở danh sách cần **hai OID khác**; fixed-list vs candidate-recomputed cho8/0 đã chạy. Mốc A0 phải lấy được sau land rồi ghi trong A1; không dùng hằng tự tham chiếu final A0 SHA. Thêm eligibility delta wp461/gate và pre/post-C R8. |
| **A4** | rc8/ĐÃ_THU_HỒI từ sổ hoặc history, có/không thay thế; live0 | Hướng mutant bỏ riêng từng nguồn hợp lý. Đã chạy historical reverse8; ledger-dead logic cũng dùng trong guard. Cần implementation chạy full2×2 matrix; không lấy một hàm parser pass chứng nhận mọi consumer. |
| **A5** | rc11 + ID/path; exact/prefix/case/alias; CLI exactpublished pair | Những ca cũ có phép đỏ thật, prepublish12 đã thống nhất N9. E chứng minh server ordinary/ops/default heads đều đủ; tag/pull/local-only không đủ theo discovery Q4. R6 [] có thể thu hẹp thành0; R7 nguồn/tree/cycle chưa rõ. Unicode/absolute/outside payload not_run. Pure0/0 chỉ đo giới hạn snapshot, không acquire test. |
| **A6** | name/OID mismatch, diagnostic2SHA; pinned OID;3 lượt median ratio≤2 | Recapture/refname mutants đúng đích và phân biệt được. Chưa phủ replace refs hoặc local-head source map. Không có timing numerator implementation r3, nên ratio **not_run**, không lấy baseline3,3s làm pass. Adapter/proxy/closure bổ sung phải benchmark lại chi phí thật. |
| **A7** | mỗi schema constraint một lỗi + control, rc4/8/12 và RC_STATE mapping | Hợp đồng YAML/type/allowlist tiến bộ; lỗi mode mới parser12 khác mode cũ append8 nếu map chặn trước là hợp lý. Cờ False cần tách consumer runtime/M4/bootstrap/dự báo; r3 không nêu đầy đủ nên A0 có thể tự đổi behavior R4. Chưa chạy mọi constraint×consumer, không bịa N/N. raise→continue có thể cho0 hoặc11, r3 đã khai đúng. |
| **A8** | tuple-map cây ứng viên + rc, parent2 giữ0/mất8 | Git mutation/merge cases thật phân biệt đúng; N7/N9 đóng. **Single mutant chỉ validate additions không thể đỏ bằng ca mode đã nêu**, vì tuple-map vẫn8 (R9). Chỉ-quét-canonical/log-only có mục tiêu đúng. Cần actual-candidate drift/source receipt test R5; hai mapper/validator unit không thay workflow. |
| **A9** | Stateful API endpoint/globalID/issue/login/block/types/call-count/body-hash/receipt | Float/duplicate/prose negatives8 và positive0 đã đo model. New canonical event làm downstream thêm0calls/Y0. Readback trước canonical404→12. JSON hỏng12 phải là API envelope; command JSON hỏng8 theo Q2. Standalone counter≥1 chỉ giết bỏ call khi job có; không chứng minh event/job được tạo (R3/R5). Actual API/mapping/facts not_run. |
| **A10** |5×4 route/status, rc/state/history/attempt/post/repeat/root | L có25 tổ hợp kể mutants: candidate ID live/revoked đã sửa, helper-only bị phân biệt ở3route. Unknown byte-match. M7 không có REST dependency theo Q4/Q2.3; không chặn oan chỉ vì REST403. Root CLI sản phẩm, exact transport profile, disk failure và nguyên nhân unknown riêng chưa chạy vì implementation chưa có. |
| **A11** | base/candidate cùng môi trường, delta theo tên; actionlint/shellcheck, YAML wiring/Actions provenance | A0 “record-only đỏ” là ca có giá trị hồi quy, **không chứng minh PR không xoá chính ca đó**. First-workflow definition cũng chưa có ở A0. Trích thân YAML không đo trigger/check association/runtime S/H/tree. BASE lease120/121 do t33, loop278/278 thật; CANDIDATE chưa có nên không có delta0/N/N của r3. |
| **A12** | rc/byte/registered/executed/pass/fail/skip/not_run + exact code/tree | Model detector bắt no-suite và bỏ invocation khi catalog được giữ; xoá cả catalog+invocation thành1/1 vẫn qua tự kiểm. Phải neo catalog/detector độc lập cho authority/activation. Banner/rỗng không được gọi đo được; không gộp not_run lớp sandbox vào passed. Hợp đồng artifact không thay bootstrap trust. |

Không chứng minh cả một tiêu chí là hằng-xanh với **mọi** implementation. Kết luận “không thể đỏ” cụ thể là A8 với **single mutant và fixture mode được r3 viện ra**; “không thể xanh” cụ thể là smoke1g2 **sau nhánh chờ gate cuối trên frozen data hiện tại**. Phân biệt này tránh sửa code đúng chỉ để thỏa một assert sai.

### Nhất quán luật, slice và §0

| nguồn | đối chiếu r3 |
|---|---|
| Protocol §3.2 / ADR-0025 | Issue/spec_hash/revision/generation/phái sinh do dispatcher, không tự khai effective. Ready facts là nghĩa vụ, không được miễn vì #473 chưa có code. R6/Q12 cần đóng dependency/ngoại lệ thật; không tự tạo hash/authority. Review đặc tả tiền thi công chưa cấp lease. |
| §4 / ADR-0028 | Q5/Q11 đúng hướng stale/new generation/no tự cherry-pick/giữ last SHA-state-journal. Dừng worker và retention là hành động phải đọc lại, chưa đo offline. Land/heartbeat/push fencing vẫn là nợ, không được biến một snapshot rc0 thành lock. G2 hết hạn phải cấp generation mới qua thẩm quyền, không sửa timestamp để cứu smoke. |
| §5 | Effective closure toàn kho, symlink/parent/canonical path còn R6/R7. Schema chuẩn nằm **.github/coordination/schemas/**, r3/EVIDENCE nêu thêm path schemas/ ở root; đã đo cả hai, đều vắng. Predecessor integrated là điều kiện scope nối tiếp; code cho workflow phải **đã canonical**, không chỉ ở PR/integration. |
| §8 / AGENTS.md | Kho review giữ read-only; scratch ngoài cay-kho; hash/base/tree và model/transport khai đúng. Findings có Git/process/model evidence riêng. Hint chỉ chữ SPEC và cần executor tái dẫn xuất; không có reviewer patch authority code tự duyệt. Required skipped/wrong SHA/no positive evidence không pass. |
| §12 / ADR-0044 | Budget per PR, không per loại tài liệu; R10. Đổi architecture thành A0/A1 không reset history/counters. A0 chỉ được gọi slice độc lập nếu outcome/acceptance riêng và không kích hoạt phần authority còn thiếu; cờ False alone chưa đủ R3/R4. Cắt test hoặc chia PR chồng lấn không chữa coupling. |
| CLAUDE: “có MẶT ≠ có ĐO”, ba trạng thái | A8 mutant bị map che; A11 test PR tự xoá; YAML body extraction không có Actions receipt. R3 tốt ở errors M1/N8/N10/N11 nhưng nguồn identity/object/closure còn R1/R2/R6. Empty API hoặc HTTP403 không chứng minh Git unavailable. |
| CLAUDE: đo thứ đã đến | Q2 body UTF-8 hash và event lifecycle đã rõ; receipt phải thêm exact candidate/checker semantics R5. Không lấy câu trong SPEC/EVIDENCE làm chứng authority hoặc độ tươi. |

**Kích thước r3:** A0=480–680 dòng/2tệp, A1=80–140/3tệp, B=150–220/2tệp, C≈15/1tệp; tổng **725–1055**, **6 path duy nhất**. Chỉ A0 vượt300 theo ước; A1/B/C không vượt, nhưng đây chưa là diff runtime. Mốc lịch sử +409 SPEC/#250, +368 code/#275, +328 code/#248 đo đúng; không phải số chứng minh estimate mới đủ. Move trusted workflow vào A0 khiến A0 thành3tệp và tăng công adapter/closure/wiring/cases: hint ước lại **600–850 / 120–200 / 150–220 /15 = 885–1285**, chỉ là estimate đề xuất cần scope/ngoại lệ và numstat trước review. Không cộng dòng patch chữ SPEC vào diff code để giả đã đo kích thước implementation.

### Q7–Q12: câu còn thiếu và đáp án bắt buộc

| câu | điều còn phải chốt/đo | điều đã có đáp án bắt buộc |
|---|---|---|
| Q7 | Packaging cuối, exception A0 có phạm vi, trusted workflow đặt ở đâu, boundary lần land bootstrap đầu và Review Rescue Checkpoint | Từng slice có scope/acceptance/base đúng; predecessor đã được nhận, code/workflow cần chạy có trên canonical; không cắt test/PR overlap hoặc tự reset budget. A0 không được áp semantics mới trước readiness. |
| Q8 | Owner Issue comment cụ thể cho r2, exact target/hạn còn phù hợp lúc C; nếu g2 hết hạn phải revise intent/đích trước land | Chỉ Issue comment cùng repo/#461 theo Q2, đúng6 field/type/account; bot projection5569885143/PR474 không thay event có authority. Không phân biệt người với agent dùng cùng tài khoản/PAT từ Git signature. |
| Q9 | Nhận event cho lease hết hạn là lựa chọn sản phẩm; khuyến nghị nhận của r3 vẫn hợp lý | Không hồi sinh lease/tái dùng ID hoặc kéo dài expiry vì event được nhận. Hết hạn phải parse/đo, không suy từ “land rồi”. |
| Q10 | Exact trusted-check publisher/consumer và S/H/tree semantics, strict up-to-date/direct-push/bypass/queue/dispatch facts; freeze/bootstrap interval; cutover delta owner đã audit | Authority trước hiệu lực, candidate tree thật, code đã canonical, skipped/wrong SHA/no evidence không pass. Cờ False khi thiếu facts. Không coi required check được đặt tên là đã enforce provenance; không chỉ bảo vệ file sổ mà bỏ code authority. |
| Q11 | Ai tuần tự hoá; fact dừng worker, lastSHA/state/journal, deployment B và readback sau C; xử lý đích đã hết hạn | Check là snapshot; không bắt đầu mới trước dừng/readback hợp lệ; generation mới và retention theo luật. Răng máy tầng land chưa có không được khai là đã có. |
| Q12 | Trusted Git transport/proxy/profile, closure policy/provenance, source OID cho symlink, mốc A0 ghi vào A1, ready/runtime facts từng slice | Phái sinh dispatcher + spec_hash không miễn; missing policy không raw fallback; mã chưa viết không cần đã chạy trước lease viết nó, nhưng hợp đồng phải đóng trước ready và runtime facts phải có trước activation. |

Hai câu hỏi user gợi ý đã có thể trả lời dứt khoát từ r3: **“đã publish”** là exact pair trên **bất kỳ advertised refs/heads/** trong snapshot Q4, không riêng ops/** và không bao gồm mọi loại ref Git; E có controls tương ứng. **M7 REST403/gitOK**: Q4/M7 không cần REST căn cứ lịch sử nên REST403 riêng nó không phải lý do chặn. Get-url bị proxy rewrite sang identity khác hoặc Git discovery hỏng thì r3 cố ý chặn; khả năng container cụ thể chạy được adapter mới là deployment fact chưa đo, không bịa thành P1 “fail-close luôn chặn oan”.

## Bảng đo lại

D đo trên `cay-kho` không sửa repo, các OID/ref được ghim trong JSON. Clock lịch sử là **phân loại lại dữ liệu Git ở thời điểm chỉ định**, không giả đã quan sát môi trường production vào giờ ấy. CLI nền chạy trên `scratch/base` với origin bare `scratch/mirror-server.git` tự dựng từ object/ref snapshot; đây là measurement hành vi offline, **không** corroboration GitHub freshness.

| lời khai/đơn vị | đo lại | bằng chứng/giới hạn |
|---|---|---|
| SPEC r3 + untracked copy | cả2 sha256 `ef9b3700514921d4cabe95947f86937fc36f4aecf2f4e2e39587cafe88a9bb20` | sha256sum trước/sau; review đúng nội dung. |
| SPEC.r2.md | `9e775a154dd83741fd4e7af85aaeae1f5693ceabc5c5763cf6890ff4f2606c80` | Hash file được cấp. |
| VERDICT.luot2.md / HINT.luot2.patch | `bb29329551222c3ee75124c549d66516a8e3ee40e6152a1dbfe58fa43a01e9f2` / `02b562b36c546f3a9620849c8df3a088306c7e01e211cb21a467f069bcf60c9c` | Khớp lời khai bundle; không phải chứng thực raw run/model. |
| VERDICT.luot1.md | `b60a755f611bf814e0c9116e1cb5c9c4f9cb5ac3f1a6e96a951cd3dc7f17123e` | Đã đọc lịch sử finding/trace description. |
| HEAD/tree/abbrev | b416830… /266a2aba… full ở đầu;7 | rev-parse/config local, detached không làm mất branch master. |
| Ref | **303 =302 remote +1 local master**, trừ HEAD alias | for-each-ref refs/heads refs/remotes, map full OID trong D. |
| Pair/path/lease_id | **288 /273 /273** | ls-tree theo ref/OID, khử trùng(blob,path), parse YAML; không tính ref thành pair. |
| ID nhiều blob | **7**, số blob2/2/4/4/5/3/2 | ag-t0-r2, mutant, n5, plat-x5-exec-r4/review2/review3, wp461r2. D.multiblob có full ID. |
| CÒN_HẠN / chưa bia mộ ở ít nhất1 pair | **8/4 lúc13:41:00Z**, **7/3 lúc14:33:15Z**; measurement lúc15:32:58Z cũng7/3 | `_phan_loai_lease` baseline ở fixed clock; không suy chỉ3 còn hạn khi đã bia mộ. |
| #456 expiry | **2026-09-07T14:30:07Z** | Sau14:30:07 phân loại HẾT_HẠN, khớp đính chính; thời điểm API14:30:12 không đo. |
| Gate4 expiry | **2026-09-08**: r1 **03:37:33Z**, r2 **07:50:35Z**, r3 **09:44:51Z**, r4 **10:17:12Z** | E.r3-gate-migration-delta đọc đủ4 Git lease; cả4 còn hạn ở14:33Z. Không có earliest-A0 timestamp. |
| wp461 expiry | r1 **03:05:00Z**, r2 **05:27:42Z**, g2 **09:52:00Z**, đều08-09 | D/F; g2 hết trước gate cuối25m12s. |
| Bia mộ master/#468 | **7/11**; cả7 cặp master hai chiều và ID/tên file đúng | D.canonical_tombs/feature_tombs; 4 thêm trên feature là3gate+mutant. Không coi feature là authority. |
| Commit riêng #468 | **0 /31** so master | rev-list --left-right --count; không phải28. |
| r2 blob không tomb26f07b4 | full `26f07b4fe49964034c710864f350402fe5bf55c3`, **4 ref** | heads/master, origin/master, origin/ops/cap-lease-461, origin/claude/soan-spec-3-viec-treo-20260906. |
| r2 blob có tombfdfde3a | full `fdfde3a57ab9fd2c83454e9b9b2eff96f77ef229`, **1 ref** | origin/ops/lease-wp461-g2. R2 là2pair/1path, không5pair. |
| “ref thứ5 sau PR475” | **chưa đo**, mirror chỉ4 | r3 đã tách [API], không lấy absence trong snapshot bác nguồn tương lai. |
| mutant #456 sống/tomb blob | `8b2103c06687546379a17f6deafc97f1fe0173fd` **11 ref** / `1f9504281c3415f7194e124eb7b2702c34c8efd1` **1 ref** | D.special refs đầy đủ. Expiry không làm số ref tự đổi. |
| Policy/schema | policy `.github/coordination/change-impact.v1.json` **vắng**; schema đúng `.github/coordination/schemas/change-impact.v1.schema.json` **vắng**; path root `schemas/change-impact.v1.schema.json` cũng **vắng** | ls-tree canonical. Root schemas chỉ review_verdict.v1.schema.json. Phải sửa path viện dẫn, không chỉ đọc path root rồi suy source protocol. |
| Planned legacy | **3 ID**, plat-x4-exec1, plat-x5-exec1/r2, đều hết hạn21-08 | D.planned; không coi số3 là ref count. |
| Sổ hiện tại | **0 entry canonical** | ls-tree origin/master ops/thu-hoi. M5 là kế hoạch, chưa có record thật. |
| Symref local | **refs/remotes/origin/HEAD→origin/master** | Mirror này có; EVIDENCE nói clone điều phối không symbolic là nguồn khác. Không dùng nó xác nhận server default. |
| Server symref/main, heads freshness, agent/wp461 rỗng | **chưa đo trên nguồn canonical** | Origin gốc ngoài cwd không được gọi. Fake bare main/master controls không có giá trị authority/freshness. |
| Chữ ký6635379 | **1 gpgsig SSH**,2 marker | Raw cat-file; không2 chữ ký và không signer verification. |
| Chữ kýb416830 | **1 gpgsig PGP**; raw author ducthangho/committerGitHub | API web-flow/login khác raw identity. Không chạy xác minh keyring hay REST trong lượt này. |
| 5 actor run372–376 / author.login claude / HTTP403 | **chưa đo** | Chỉ có lời khai điều phối; không có raw API receipt trong bundle để xác thực. |
| `kiem()` gọi matcher | **0** | AST kiem/_lease_cham_duong; là baseline, không code r3. |
| 5 cửa packet_loop gọi schema helper | **1/1/0/0/0** | record-lease /begin-attempt /record-post /transition /record-review, AST; mutant L cũng cho ba route sau qua. |
| `--state-dir` default | **.claude/.packet_state** | Parser dòng1972; fixture state đặt trong scratch, không ghi default. |
| ci.yml lane PR | checkout fetch-depth0, wrapper AL_VER1.7.7, packet_loop test | Đọc YAML đúng file; không chạy wrapper tải mạng hoặc Actions. |
| duyet-khac-danh-tinh.yml | target(open/reopen/sync/ready)+review(submitted/dismissed), checkout base.ref, contents read/pull-requests read | Đọc YAML; mẫu ấy không chứng minh exactS/check association của M9 chưa viết. |
| Bốn đường g2 ai-dang-giu | **NGƯỜI_GIỮ2, rc11 cả4** | launcher **3.375s/2217B**; CHANGELOG **3.377s/941B**; provider plan **3.479s/941B**; bien_nhan_v2_test **3.551s/941B**. Một lượt mỗi path, không benchmark r3. |
| Check g2 baseline | **0 ĐĂNG ĐƯỢC** | NativeCLI on scratch/base, original0 và thêm EWS[] vẫn0; không là check exclusivity r3. |
| #250/#275/#248 numstat | **239+170=409/0**, **149+219=368/0**, **89+239=328/1** | git diff first-parent merge2854380/7883aad/647cfea, mỗi2file. #250 là SPEC. |
| R3 slice estimate | **725–1055**,6 unique paths; A0 vượt300 | Cộng 480–680 +80–140 +150–220 +15; chưa có diff code. |
| Lease suite nền | **120/121**, executed121, skip0, **rc1**, **9027B**,64.164s | `scratch/baseline_r3.py lease`, raw log; chỉ t33 thiếu actionlint. Không gọi delta0=N/N. |
| Wrapper121/121 | **chưa đo** | Không có actionlint được xác minh; không cài mạng hoặc thay bằng parser YAML. |
| Packet-loop suite nền | **278/278**, **81 mutants**, **rc0**, **8752B**,211.113s | Raw log có TỔNG ĐẠT,78 lớp lách/35 ca bắt-oan/0 ngoại lệ AC18. |
| Doc-claims strict | **rc0, ok:true**,106 files,0 flags,367 advisories;70861B | Chạy copy base, không chứng nhận SPEC semantic correctness. |
| Doctrine-scan kèm SPEC | **8 tệp,0 chỗ chép,rc0**,69B | Copy base+SPEC, mặc định7 thêm1; không suy r3 không mâu thuẫn protocol. |
| Run duration/model/effort của lượt1/2 | **chưa đo raw run** | Hash verdict/hint được cấp khớp; stderr bytes/thời lượng/model metadata vẫn lời khai ngoài artifact đọc được. |

## chua_do_duoc

1. **GitHub authority/freshness:** không mạng. Chưa readback comment Q8, bot comment5569885143, PR475 body/actor, default hiện tại, protection/ruleset/direct-push/bypass, check publisher association, Actions run thật hoặc trạng thái merge. Bare fixture không là chứng cứ độ tươi; code tạo commit không chứng minh production cho merge commit đó.
2. **Model/transport metadata lịch sử:** không có raw run.json/backend attestation trong cwd. Khai theo cấu hình hiện tại và hành vi tool, không nhận title/model name do điều phối ghi là tự chứng thực.
3. **Implementation mới:** M1–M9 r3 chưa tồn tại; model chỉ kiểm các vị từ đã chỉ rõ. Không có N/N A1–A12, actual delta baseline/candidate, exact new numstat hoặc timing ratio A6. Bản code stub A0 chỉ dùng chứng minh availability, không là bộ kiểm authority.
4. **Bootstrap/activation:** chưa có A0/A1 landed OID, registry active, canonical workflow mới, freeze interval có authority, cutoff receipt/list hoặc kế hoạch delta đã được owner chấp nhận. Hint chỉ đề xuất hợp đồng triển khai; không lấy code/matrix mô phỏng thay facts ấy.
5. **Phạm vi normalization:** absolute/outside/tree-escape, đồng tự/NFC tấn công, chuỗi thoát theo lệnh cấm **not_run**. Symlink nội bộ, hai-cây-cùng-blob và vòng nội bộ có ca. Chưa chạy Windows filesystem thật, toàn bộ descendant-prefix/new-file/disk failure cases của implementation tương lai; các trường hợp ấy phải được điều phối dựng theo Q3 đã đóng.
6. **Guard và fencing:** L dùng doctor precondition hợp lệ và snapshot status tiêm. Không đo transport profile/proxy container thật; REST403 không bị suy thành Git fail. Không đo kill process, heartbeat/push/handoff/land fencing, durable state disk failure hoặc cleanup/retention thật. Root/state paths fixture đều nằm trong cwd.
7. **Suites:** baseline lease còn t33 đỏ do thiếu actionlint; không tải công cụ bằng mạng, không dùng stub actionlint làm pass. Wrapper121/121 là lời khai, không kết quả lượt này. Full product selftest/release gate không chạy vì review đặc tả read-only, không có runtime diff; các suite liên quan và doc/doctrine đã đo, không gộp các ca chưa chạy vào passed.
8. **Nguồn luật/phạm vi:** đọc AGENTS, CONTEXT, protocol, CLAUDE, ADR0025/0028/0044 và provider plan trong cwd. Adapter cross-review Claude chỉ dùng đối chiếu workflow/role; không chạy bootstrap/install/đăng review của adapter, không gọi reviewer khác hay đọc auth ngoài cwd. User đã trực tiếp yêu cầu artifact lượt3, nên không dừng xin lại quyền vì một hướng dẫn dành cho executor/launcher.
9. **Review/hint:** mọi finding P1/P2 có hunk spec tương ứng; không có patch runtime authority hoặc commit. Executor còn phải chốt revision/scope/dependency/authority và tái dẫn xuất trên cây thật. Những phần R5/Q10 yêu cầu facts ngoài kho được để thành prerequisite có chủ ý, không khai đã gỡ cửa sổ authority bằng câu chữ.

Kiểm tra artefact bằng `scratch/validate_artifacts_r3.py`: đủ25 hàng lịch sử,10 finding mới đúng9P1/1P2,19 ID D3 tái dựng; coverage hint có đủ R1–R10. `patch --dry-run -p0` và áp thật trong bản sao đều rc0; byte-match với bản đề xuất. HINT sha256 **0a81bd8b2288cc5c235a7e5477785014c0c431005cbb842a8f89713c275662d8**; SPEC sau áp trên bản sao **17920b745345f5decd9dd6f8e8ec27edb75b25b8a0d6a8f304326814e3291152**. SPEC gốc giữ hash đã review; tracked diff cay-kho rc0, status chỉ còn đúng spec untracked ban đầu. Receipt có timestamp/hashes và kết quả máy ở `scratch/artifact-validation.json`.
