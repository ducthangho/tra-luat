verdict: changes_requested
reviewed_spec_sha256: 9e775a154dd83741fd4e7af85aaeae1f5693ceabc5c5763cf6890ff4f2606c80
model_tu_khai: OpenAI Codex qua API và công cụ shell trong sandbox; cấu hình phiên mô tả GPT-6. Không có chứng thực độc lập tên model backend, effort hay toàn bộ transport; không suy chúng từ tài khoản GitHub.

Review đặc tả r2 trước thi công, không approve mã triển khai. Cần revision: **5 finding cũ ĐÓNG, 8 ĐÓNG-MỘT-PHẦN, 1 ĐÓNG SAI**. Các finding cũ còn lại giữ hạng cũ. §3.2 quy định blocked khi executor gặp spec thiếu trong thi công; lượt này đang sửa hợp đồng trước Issue/lease nên dùng changes_requested như lượt 1.

Git base `b416830ef2a509d60203d55552ce17950afcf67c`, tree `266a2aba97d925dac3ab7473dda55adb0fe23b8e`. Không sửa/commit/push `cay-kho`, không dùng mạng, không đọc origin gốc vì đích của nó ở ngoài cwd. Chỉ dùng Git bare tự dựng trong `scratch/`; mọi biến đổi tree, mode, code và state đều ở đó. Không tự soạn payload đường thoát cây, đồng tự Unicode hoặc chuỗi thoát. Alias symlink được thử chỉ trỏ một thư mục **bên trong** kho giả.

`HINT.patch` chỉ vá CHỮ của SPEC, gợi ý draft r3; không chứa patch mã cổng. Nhãn: **chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm commit**. Đã dry-run và áp thật bằng `patch -p0` trên bản sao SPEC; kết quả byte-match bản dự kiến. Chấp nhận hint vẫn cần revision/review và chốt scope/dependency, không tự tạo quyền thi công.

## Bảng finding lượt 1 → trạng thái

Mã ca dưới đây trỏ đến `scratch/adversarial-r2.json` (D3-r2), `scratch/loop-routes-r2.json` (D4-r2), `scratch/workflow-r2.json` (W), `scratch/extra-r2.json` (E). Các ID mới N1–N11 được khai đầy đủ ở phần tiếp theo.

| id | hạng cũ | trạng thái | bằng chứng đối chiếu §0 với thân r2 |
|---|---|---|---|
| authority-signature-evidence-false | P1 | **ĐÓNG** | Q2: một SSH signature ở 6635379, một PGP ở b416830; đo lại đúng. Raw author khác API login; không còn suy human/agent từ chữ ký. |
| default-ref-is-untrusted-cache | P1 | **ĐÓNG-MỘT-PHẦN** | Q4/A2 bỏ local symref/fallback: q1-symref-authority vẫn holder X; q1-fallback-revived đọc main, X chết. Nhưng chưa neo identity của máy chủ được hỏi; đổi origin sang bare khác vẫn qua Q4: N1. |
| standalone-revocation-has-no-admission-gate | P1 | **ĐÓNG-MỘT-PHẦN** | Q2/M4 chặn standalone giả: 1 API call, 404→12. M9 đã vào scope, nhưng thêm path không phủ mọi cập nhật canonical, còn bot-author skip và bootstrap sai: W, N3/N4. |
| evidence-mention-is-not-an-authorization | P1 | **ĐÓNG** | Q2/A9 chuyển sang khối lệnh và so trường. Hai ca phủ định/ID chỉ là tiền tố đều 8 thay vì 0; repo/Issue/account được nêu. JSON/URL và vòng đời đọc lại là thiếu mới ở N10/N11, không phủ nhận việc đã sửa hai vị từ substring cũ. |
| write-set-exclusion-is-incomplete | P1 | **ĐÓNG-MỘT-PHẦN** | Q3/A5 cả không-thay-thế, prefix, case-fold đều 11 khi W giữ. Nhưng phép liệt kê thiếu resolve symlink/parent và chưa lấy effective closure theo §5: E, N5. |
| snapshot-check-does-not-fence-writers | P1 | **ĐÓNG** | Q3/Q5/Q11 bỏ lời hứa acquire nguyên tử, yêu cầu dừng worker/cấp-readback-bắt đầu tuần tự, nêu land/fencing chưa có. Hai phép tính trước publish vẫn 0/0; sau publish Y/Z đều 11. Giới hạn được khai đúng; không có bằng chứng quy trình Q11 đã được thực hiện. Mâu thuẫn cách gọi ca A5 còn ở N9. |
| reads-are-not-pinned-to-one-snapshot | P1 | **ĐÓNG-MỘT-PHẦN** | Ghim chính map đã so thì q4-snapshot-move giữ OID/sổ đúng. Nhưng chữ “sau đối chiếu, chụp map” cho phép chụp lại map mới rồi ghim: N2, holder X sống lại. A6 có ý định bắt lỗi này nhưng hợp đồng thứ tự chưa thống nhất. |
| legacy-fallback-conflicts-with-ledger | P1 | **ĐÓNG-MỘT-PHẦN** | Q3/Q6 sửa precedence, chiều ngược, áp toàn ID: ba ca cũ lần lượt checkY 0/8/8. Mốc đóng đo được 7 cặp hợp lệ. Tuy nhiên cutoff loại cả ba cặp gate đang ở feature; r4 bị 8 và bốn gate ID được đếm giữ, trái bảng di trú “người giữ hợp lệ/không đụng”: N6. |
| append-only-check-misses-candidate-and-merges | P1 | **ĐÓNG-MỘT-PHẦN** | A8 kiểm ứng viên: sửa record→8; merge ours mất sổ dù log rỗng→8. Map path→blob bỏ mode/type, và M1 chỉ được gọi cho phần thêm trong mô phỏng M4: mode mutation→0 rồi reader M1→12, N7. Wiring toàn canonical còn phụ thuộc N3. |
| packet-loop-guard-is-partial-and-boolean | P1 | **ĐÓNG SAI** | Q5/M7 sửa đúng 4 cửa có lease: revoked→stale, một event, không tiêu thêm; unknown không đổi state. Nhưng đưa guard chỉ nhận state vào trước record-lease khi state.lease=null làm cả ca sống→8, ca revoked không ghi stale/event. ID ứng viên phải được truyền riêng: D4-r2, N8. Đây là hậu quả của hợp đồng chữ ký/gắn guard đang viết, không khẳng định executor không thể tự đoán cách sửa. |
| acceptance-confuses-refs-blobs-and-mutations | P1 | **ĐÓNG-MỘT-PHẦN** | A1: 3 cặp, known-list thiếu 1, mutant sống X; A2: 1 cặp/3 ref; fixed clock, nhãn hết hạn và evidence runner đã rõ hơn. A5 còn gọi CLI trước publish 0 trong khi Q3 bắt ứng viên đã publish; A8 gộp ca second-parent hợp lệ vào nhóm 8: N9. |
| revocation-schema-and-error-contract-incomplete | P2 | **ĐÓNG** | M1 đã nêu kiểu, mapping/khoá trùng, regular entry, ID/path, authority, clock, optional cap/known blobs, lỗi 4/8/12 và precedence; A7 yêu cầu mỗi ràng buộc/consumer. Đây là đóng hợp đồng YAML, không chứng nhận parser chưa viết. Hợp đồng JSON của Q2 còn thiếu mới: N10. |
| size-estimate-and-slice-anchor-are-stale | P2 | **ĐÓNG** | Đo đúng +409 SPEC/#250, +368 mã/#275, +328/#248, #468=31; 655–945 cộng đúng, A=510–730/B=130–200/C≈15, thừa nhận A vượt và cần ngoại lệ. Packaging A vẫn vướng N4; câu tuyệt đối “không có slice ≤300” sai ngay với B/C, cần bỏ, không phải sai phép cộng. |
| ready-and-rollout-decisions-are-not-closed | P2 | **ĐÓNG-MỘT-PHẦN** | Q10–Q12 đã xuất hiện, phái sinh không được miễn và protection chưa đo thì không M5. Nhưng Q12 đòi wiring mới đã đo trước lease trong khi mục chưa-đo-5 hẹn đo lúc thi công đầu và bộ kiểm canonical chưa có lệnh. N4; còn source/cache/closure/activation chưa đủ hợp đồng. |

## Findings mới

Các mục sau gồm lỗ mới của r2 và phần còn lại được tách cụ thể từ finding cũ; các hàng trên giữ ID/hạng lịch sử. Phản chứng là Git/entrypoint thật cộng **mô phỏng vị từ r2**, không phải kết quả chạy một implementation thu hồi đã tồn tại.

### canonical-remote-identity-unbound · P1 · N1 · Q1/Q4, M2, A2

**TÁI HIỆN:** D3-r2 `new-q4-origin-redirect`: giữ bare canonical A ở commit không có record X; trong bản sao đổi origin sang bare B có record, push/fetch đủ cùng tập tên. B khai master bằng symref, cache/OID khớp. Mô phỏng Q4 trả snapshot hợp lệ, holder từ `[X]` thành `[]`, trong khi HEAD của A không đổi. Toàn bộ bare nằm trong scratch; không thử GitHub/protection thật.

**Vì sao:** thay “tin local HEAD” bằng “tin máy chủ mà origin chỉ đến” chưa xác minh đó là repository canonical. Q2 yêu cầu URL cùng repo không ràng buộc endpoint Git của Q4. Record thậm chí có thể có lệnh owner hợp lệ nhưng chưa được nhận vào canonical thật; reader vẫn đọc cây khác nếu nguồn bị đổi. Đây là phần neo nguồn còn thiếu của finding default-ref lượt 1.

**GỢI Ý VÁ:** truyền identity/endpoint từ nguồn điều phối tin cậy, xác minh repo/host/transport thực sau cấu hình Git, ghim identity vào snapshot/receipt; khác/không đo được→12. Không lấy tên origin hoặc cùng refs làm chứng. Fixture nguồn test không thành cờ production bỏ chốt. Hint Q4/A2/Q12.

### snapshot-pinned-after-unverified-recapture · P1 · N2 · Q4, A6

**TÁI HIỆN:** `new-q4-recapture-after-compare`: so map đúng, đổi remote-tracking master về OID trước sổ, rồi làm đúng thứ tự chữ “sau đối chiếu, chụp map…một lần”. Mọi đọc sau đó dùng OID đã ghim, nhưng OID ấy chưa được so; holder `[X]`. Đối chứng `q4-snapshot-move` ghim map đã so giữ holder rỗng; mismatch có sẵn từ đầu→12.

**Vì sao:** ghim OID không sửa được việc lấy OID từ lần quan sát khác. A6 đòi kết quả không đổi, nên mô phỏng permissive này **sẽ đỏ A6**; finding là mâu thuẫn thứ tự trong thân spec cần giải trước khi executor viết mã, không nói A6 thiếu hoàn toàn ý định kiểm.

**GỢI Ý VÁ:** capture local map trước phép so; canonical OID từ advertisement máy chủ đã đối chiếu với chính map đó; không recapture sau so. Kiểm HEAD OID khớp nhánh mà symref khai. A6 thêm mutant recapture-then-pin. Hint Q4/A6.

### admission-workflow-does-not-cover-canonical-updates · P1 · N3 · M9, M4/A8/A9/A11, Q10

**TÁI HIỆN:** đọc workflow hiện có, giữ cấu trúc và thêm đúng path M9 chỉ định. `scratch/workflow_probe.py` phân tích YAML: ops/revoke + record→job có; cùng delta với Git author name là bot→job không chạy; integration/master→không trigger; chỉ đổi docs→không trigger. Rig cũng tạo commit Git thật chỉ thêm record X, đọc raw author.name=github-actions[bot], và điều kiện job trả false. Workflow chỉ có event push. Điều kiện job ở dòng 66 dựa raw Git author name, không phải API actor. Chưa đo kết luận status của GitHub cho từng event; phép đo chỉ chứng minh không có execution theo wiring này.

**Vì sao:** M1/A8 yêu cầu kiểm **trước mọi cập nhật canonical**, kể cả tree làm mất sổ, nhưng M9 chỉ mở thêm path trong workflow đăng lease cho nhánh ops. Check bắt buộc ngoài kho không tự khiến job bị lọc chạy được. Chưa có cổng cho luồng integration/land, provenance exact S/T hoặc trạng thái skipped/not-created. Phép thử chỉ trích thân bước khi đã được gọi không đo được sự vắng trigger/job.

**GỢI Ý VÁ:** admission độc lập với phần đăng lease, phủ cây sẽ nhận của mọi cập nhật canonical; không phụ thuộc ops/path lease/rc9/Git author name. Chốt event/target/S/T và required-check provenance; không đo được bypass, không tạo check hoặc skipped thì chưa activation. Giữ comment publishing là bước sau. Hint M9/Q10/A8/A9/A11.

### canonical-checker-bootstrap-is-circular · P1 · N4 · bước neo workflow, Q7/Q12, M9

**TÁI HIỆN:** W chạy **nguyên thân bước “neo bộ kiểm vào nhánh mặc định”** từ YAML thật trên bản sao có origin nội bộ. S=b416830; T có stub entrypoint mới chỉ để chứng minh code mới hiện diện ở candidate. Bước neo rc=0, worktree neo HEAD=S. Candidate command→0; gọi lệnh mới qua `NEO/ops/lease_publish.py`→**2, invalid choice**. Không chạy stub như một bộ kiểm có thẩm quyền. S/T, băm thân bước và stdout/stderr có trong workflow-r2.json/trace.

**Vì sao:** A gộp code mới và workflow gọi code đó, nhưng chính mỏ neo cố ý không chạy code T. Q12 lại đòi wiring đã đo trước lease A; mục chưa-đo-5 hẹn đo trong thi công đầu. Không thể giải bằng tự dùng code ứng viên hoặc tự skip cổng đầu tiên. Required check có thể khiến activation kẹt; nới nó tùy ý sẽ bỏ biên authority.

**GỢI Ý VÁ:** predecessor A0 đưa parser/admission code + test lên canonical, ledger chưa kích hoạt; A1 mới gắn workflow/activation dùng code A0 đã được tiếp nhận, rồi B/C theo dependency. Đóng cơ chế bootstrap ở spec trước lease, đo runtime wiring trước activation/C; không đòi implementation mới trước lease A0. Ước lại A0/A1 và giữ ngoại lệ dòng cho phần lớn, không xem việc tách là tự đủ. Hint Q7/Q10/Q12/A11 và phạm vi chưa đo.

### effective-write-set-and-symlink-resolution-missing · P1 · N5 · Q3/M3/A5, protocol §5

**TÁI HIỆN:** ba ca D3 cũ về không-thay-thế/prefix/case-fold nay đều 11. Ca mới E tạo Git tree có alias symlink **ở trong cây** trỏ docs, lease xin alias/a.md và lease giữ docs/a.md: so đường theo các bước Q3 liệt kê không giao→0; resolve thực ra cùng tệp→11. Ca closure theo ví dụ §5: W khai SKILL.md, effective closure gồm GOTCHAS; Y xin GOTCHAS: raw giao rỗng, effective giao một đường. File policy canonical được protocol chỉ tên hiện **không có** trong mirror.

**Vì sao:** “theo §5” là hướng đúng nhưng thuật toán liệt kê và đơn vị vẫn là write_set, thiếu bước 5 của §5 và closure được neo policy. Ngoài phạm vi cưỡng chế bốn trường phái sinh không miễn nghĩa vụ đo effective exclusion. Executor phải tự chọn dùng raw set, tin trường tự khai hay chặn thiếu policy — khác verdict thực tế.

**GỢI Ý VÁ:** dùng closure/effective set đã xác minh và policy SHA; thiếu nguồn hợp lệ→12. Resolve symlink/parent theo cây snapshot, không dùng filesystem khác OID ngầm. Thêm alias trong cây, companion do closure và missing-policy controls. Dependency policy/closure phải chốt trước activation; không tự thêm file policy ngoài write set. Hint Q3/A5/Q12.

### historical-cutoff-revives-feature-holders · P1 · N6 · Q6, bảng di trú, A3/A4

**TÁI HIỆN:** E đọc anchor b416830 thật, xác nhận 7 cặp hai chiều hợp lệ. Không có ba cặp gate trong tập này; chúng nằm trên #468. Tại giờ đo 14:33:15, cả bốn gate ID còn hạn. Áp luật r2: không ID nào chết theo lịch sử canonical; r4 khai thay thế r3 nhưng không có sổ/cặp lịch sử cho r3→r4, nên nhánh Q3(2) trả **8**. Ba ca legacy cũ vẫn đóng ở thuật toán: old-copy→holder Y/check0; reservation→8; Y đã chết theo lịch sử→8.

**Vì sao:** đóng nguồn lịch sử là quyết định an toàn hơn về authority, nhưng làm thay đổi tập holder/eligibility của dữ liệu hiện hữu. Bảng Q6 vẫn gọi r4 “người giữ hợp lệ/không đụng” và chỉ di trú r2; còn ba gate cũ bị đếm lại. Đây là thiếu hợp đồng rollout của thay đổi compatibility, không phải đề nghị tin bia mộ feature hoặc bịa thẩm quyền cho chúng. Finding legacy P1 cũ chưa đủ điều kiện đóng hoàn toàn.

**GỢI Ý VÁ:** khai đúng bốn gate holder/r4 bị chặn; đo delta toàn kho trước activation, có quyết định dừng/di trú riêng đủ Q2 hoặc giữ ledger chưa kích hoạt khi còn lane bị ảnh hưởng. Không mở rộng cutoff để làm xanh; không tự ghi thêm record ngoài M5 write set. Ghim danh sách/anchor trong code tin cậy và tách anchor fixture nội bộ, không để candidate tự khai. Hint Q6/Q7/A3/A4.

### candidate-map-omits-entry-mode · P1 · N7 · M1 append-only, M4, A8

**TÁI HIỆN:** `new-a8-mode-not-in-map`: S có regular record X. Ở index kho giả, đổi mode của cùng path từ 100644 thành 120000, giữ blob `41fdc527d183e7ab5120205d6e055919653c2abf`; không checkout hoặc truy cập symlink đó. Map path→blob bằng nhau, phần thêm rỗng: cổng M4 mô phỏng→**0, không API call**. M1 kiểm toàn entry T→**12, not regular record**. Đây là Git commit thật, mode/type/OID trước/sau nằm trong JSON.

**Vì sao:** M4/A8 so blob và kiểm M1 cho phần thêm không cưỡng chế regular entry của bản ghi cũ ở T. Cây đã được gate nhận lại bị reader từ chối; append-only không chỉ là hash nội dung. Không cần giả định reader đi theo symlink để có finding này.

**GỢI Ý VÁ:** so path→(mode,type,blob), kiểm toàn namespace T bằng M1, rồi chỉ readback online phần mới. Sửa mode/type entry cũ phải đỏ trước merge; đối chứng thêm hợp lệ phải xanh. Hint M1/M4/A8.

### record-lease-guard-has-no-candidate-id · P1 · N8 · Q5.1/M7/A10

**TÁI HIỆN:** D4-r2 tạo state bằng `init` thật: awaiting_lease, lease=null. Bọc route bằng đúng guard nhận root/state/snapshot như r2, gọi trước thay đổi. Bốn cửa sau có ID trong state nên sống→0, revoked→8/stale/một event, unknown→8/không đổi state. Riêng record-lease sống→**8**, revoked→8 nhưng vẫn awaiting_lease, **0 event**. Hướng sửa thử riêng truyền ID ứng viên trước persist cho kết quả sống0/leased, revoked8/stale/một event. Toàn bộ setup dùng entrypoint, guard r2 là mô phỏng trong bộ nhớ.

**Vì sao:** root tường minh không thay được target ID. Guard không thể suy ID của lease mới từ state trước record-lease. Nếu coi lease vắng là sống thì có đường bỏ kiểm ứng viên; nếu coi unknown thì khóa đối chứng xanh A10. Chữ “TRƯỚC mọi thay đổi” cần phân biệt dựng ứng viên trong bộ nhớ với persist state; hợp đồng hiện buộc executor tự thiết kế thêm.

**GỢI Ý VÁ:** thêm target_lease_id/candidate lease đã validate vào guard. record-lease truyền ID từ đối số; bốn cửa kia từ state. Revoked ở record-lease ghi stale/event đúng ID mà không ghi event record_lease; sống mới persist lease. Đồng thời đóng định dạng/source của “đệm đã xác minh”, root/receipt OID; hiện r2 chỉ nói snapshot mà chưa chỉ nơi/proof được cấp cho lệnh offline. Hint Q5/A10/Q12.

### acceptance-prepublish-and-second-parent-contradictions · P1 · N9 · Q3/A5, M1/A8

**TÁI HIỆN:** D3-r2 `q3-concurrent-replacements` đo riêng vị từ snapshot trước publish=0/0 và điều kiện ứng viên có trên server=false. Sau publish, holder Y/Z, check mỗi bên11. Vì vậy cần chốt A5 đang gọi CLI hay hàm tính thuần: Q3 viết ứng viên **phải** đã có trên ref máy chủ, còn A5 viết hai CLI check trước publish cùng0. Ca `new-a8-valid-second-parent` tạo merge thường có S ở cha thứ hai, giữ nguyên map sổ: M1 append-only→0; câu A8 hiện liệt “fast-forward có S ở cha thứ hai” cùng nhóm⇒8.

**Vì sao:** hai ca đều thiếu điều kiện phân biệt. Nếu điều kiện published là của CLI thì ca A5 không thể xanh đúng luật; nếu nó chỉ là điều kiện điều phối cho bắt đầu thì phải nói vậy. Nếu ca second-parent chỉ nhằm merge ours mất X thì A8 phải buộc mất X, không lấy vị trí parent làm lý do đỏ. Không được sửa code để thỏa một assert trái bất biến. Hạng P1 giữ từ finding acceptance cũ; với A8 riêng, đây là cách viết mơ hồ có diễn giải gây chặn oan.

**GỢI Ý VÁ:** tách phép tính thuần 0/0 khỏi CLI published-condition, định nghĩa rõ mã cho chưa publish và so exact blob/path; tách second-parent giữ X→0/mất X→8. Fixture A3/A4 phải có cơ chế anchor test tin cậy, không đòi git init tạo OID b416830. Hint Q3/A3/A4/A5/A8.

### authorization-json-and-url-contract-is-open · P2 · N10 · Q2.2, M4, A9

**TÁI HIỆN:** `new-q2-json-types-duplicates` dùng JSON chuẩn được json.loads nhận: một block có packet_issue kiểu float cùng giá trị, hoặc một khóa lease_id lặp với giá trị cuối X. So bằng nhau từng trường kiểu Python như Q2 yêu cầu trả **0** trong cả hai. M1 cấm duplicate cho YAML nhưng Q2 chưa áp hợp đồng đó cho JSON lệnh. Không dùng payload bị sandbox cấm.

**Vì sao:** thiếu định nghĩa root/required keys/extra keys/duplicate/type equality/null normalization cho khối mới. Ngoài ra URL Issue body chứa Issue **number**, API có global **id** khác; PR review comment gắn với PR number, không tự có quan hệ với packet Issue. Q2 cho ba loại object nhưng “parse (loại, ID số), ID/Issue khớp” chưa quy định mapping endpoint và quan hệ cần đọc. Không khẳng định JSON duplicate là trường hợp đã phá trên GitHub; đây là nhánh executor phải tự quyết.

**GỢI Ý VÁ:** schema JSON đóng, kiểm kiểu trước so và từ chối khóa trùng; thống nhất optional cap với YAML. Hoặc định nghĩa đủ từng loại endpoint/ID/Issue relation, hoặc thu hẹp revision này về Issue comment như Q8 đã khuyến nghị. Hint chọn cách thu hẹp, có ví dụ JSON cú pháp hợp lệ và ca âm riêng. Không dùng mẫu ký hiệu lựa chọn làm JSON để copy nguyên văn.

### readback-after-admission-lifecycle-undefined · P2 · N11 · Q2.3, M4, A9

**TÁI HIỆN:** `new-q2-recheck-after-admission`: readback đúng→receipt, record vào canonical; sau đó API 404. Reader vẫn loại X và checkY snapshot→0, nhưng yêu cầu M4 “kiem-github của lease mới kiểm LẠI” gọi Q2→**12**. Trace có 200 rồi404. A9 chỉ assert X không sống lại, không assert khả năng đi qua admission của Y sau đó.

**Vì sao:** X không hồi sinh là đã rõ; phần chưa rõ là khi nào cổng thôi phụ thuộc căn cứ mutable đã tiêu thụ. Nếu kiểm lại căn cứ bất biến trong ledger mà URL bị xóa, đường replacement có thể kẹt mà không được sửa record append-only. Nếu cố ý chọn giới hạn availability này thì phải khóa nó trong AC và có đường xử lý; không thể vừa gọi đây là receipt lịch sử bền vừa để executor tự chọn bỏ/giữ readback.

**GỢI Ý VÁ:** readback mọi delta mới ở mỗi lần M4 trước canonical; sau canonical tin event qua biên tiếp nhận đã xác minh, không đọc lại căn cứ lịch sử trong kiem-github của Y. Receipt phải neo S/T/path/blob và định danh object, không chỉ ID/body hash lẻ; receipt/comment không thay required check. Hoặc chọn chính sách phụ thuộc API khác với nghiệm thu/khả năng phục hồi rõ. Hint chọn phương án trước.

## Phản chứng đã chạy lại + mới

Lệnh D3-r2: `PYTHONDONTWRITEBYTECODE=1 python3 scratch/adversarial_r2.py` (rc0); log `scratch/logs/adversarial-r2.log`, **25 kết quả = 19 ca D3 cũ + 6 ca mới**, trace **732 lệnh** Git/clone/commit/đọc object. D4-r2: `python3 scratch/loop_routes_r2.py` (rc0), 18 kết quả = đối chứng cũ + 15 tổ hợp route/trạng thái + 2 hướng sửa ID. W và E chạy riêng, không gộp chúng thành 25 ca D3. Script lượt 1 không được cấp trong bundle này; các ca được **tái dựng từ mô tả/trace contract trong VERDICT.luot1.md**, không khai đã chạy nguyên file D3/D4 cũ.

| phản chứng D3 lượt 1 | kết quả theo luật r2 mô phỏng |
|---|---|
| q1-symref-authority | Local HEAD giả không đổi canonical; holder X còn. Đóng vector cũ. |
| q1-fallback-revived | Máy chủ main, master cũ còn: đọc main, holder rỗng. |
| q2-no-admission | M4 standalone gọi API1 lần, 404→12, chưa publish canonical. Chỉ chứng minh hàm admission; wiring thật còn N3/N4. |
| q2-substring-not-command | Phủ định đơn thuần→8. |
| q2-unrelated-prefix | Prose X-extra→8. |
| q3-no-replacement-scope | Y không thay thế, W giữ p→11. |
| q3-prefix-overlap | W docs/, Y docs/a.md→11. |
| q3-casefold-overlap | Hai cách hoa/thường→11. |
| q3-concurrent-replacements | Hai clone: vị từ trước publish0/0, published-condition=false; sau push hai ref holder Y/Z, check11/11. Không có phép thử workflow GitHub race. |
| q4-snapshot-move | Dùng đúng map đã so, local ref đổi sau đó không đổi OID/holder. |
| q4-stale-sha-control | Tên đúng/SHA cũ ngay khi so→12, diagnostic hai SHA. |
| q6-legacy-old-copy | Cặp lịch sử anchor fixture, còn blob X cũ: holder Y/checkY0. |
| q6-fallback-overrides-reservation | Sổ đích Z, lịch sử X→Y: checkY8, không fallback. |
| q6-republish-legacy-dead | Y chết do lịch sử Y→Z: holder Z/checkY8. |
| a8-normal-modification | Sửa record ứng viên→8; log cũ có5 dòng không rỗng, không dùng số dòng làm đơn vị nữa. |
| a8-merge-erases-registry | Merge ours bỏ X, S ở cha thứ hai: log0 byte nhưng map gate8. |
| q5-existence-boolean | Xóa chỉ blob record trong object store giả sau snapshot: Git rc128→reader12; phải map RC_STATE ở loop. Unknown state được đo độc lập ở D4. |
| a1-cardinality-mutant | X ba blob/known hai: holder trước X/Y, sau Y; 3 cặp, MAP_REF counts4/2/2; mutant known-only làm X sống. |
| q1-control-a2 | Chọn đúng3 ref chứa cùng blob/path:1 cặp, MAP_REF3. |

Các ca legacy synthetic dùng `legacy_anchor` tiêm **nội bộ trong mô phỏng**; đây không phải cờ production của r2. Phép E độc lập đọc đúng b416830 thật kiểm danh sách 7 cặp và wp461 sau M5 chỉ còn g2, tránh giả rằng một kho init mới có OID lịch sử cố định.

| tấn công mới/đối chứng | kết quả và phạm vi |
|---|---|
| Q4 recapture sau so | Holder X sống; mọi đọc sau ghim vẫn dùng OID, nhưng OID không được so. N2. |
| Q4 origin khác | Canonical A không đổi, Q4 của B qua và holder X biến mất. N1; không phải phá GitHub protection đã đo. |
| Q2 JSON kiểu/khoá lặp | Field equality không strict nhận cả2; thiếu hợp đồng N10. |
| Q2 object xóa sau admission | X vẫn chết; online replacement recheck12; N11. |
| A8 đổi mode cùng blob | Map gate0, full-M1(T)12. Không materialize symlink bất thường. N7. |
| A8 merge hợp lệ S ở parent2 | Map giữ nguyên, gate0; không được đòi8 chỉ vì parent2. N9. |
| M9 neo code | Thân bước thật rc0, NEO=S; command mới ở NEO rc2. N4. |
| M9 trigger/job | Path mới chưa phủ integration/master/docs-only; bot author làm job vắng. YAML/control-flow offline, không phải Actions run. N3. |
| Q6 anchor canonical thật | 7 cặp hợp lệ, cutoff không có gate; r4 thiếu r3 event/cặp, check8; M5 r2 mô phỏng loại toàn ID r2. N6. |
| Q3 symlink trong cây/closure | Alias và target cùng tệp nhưng so lexical không giao; raw set rỗng trong khi effective giao1. N5. |
| D4 cũ | Helper luôn chặn, record-post/transition/record-review nền vẫn0/0/0→accepted, tái hiện đúng bệnh gốc. |
| D4 guard r2 | Bốn route có lease: mỗi route sống0, revoked8/stale/event1, lặp không đổi, unknown8/state byte-match. record-lease thiếu target mắc N8; thử truyền target sửa được hai chiều. |

Các chỗ harness cần chỉnh trước lần chạy thành công (import launcher, comment ID đủ độ dài, đường thứ tư wp461, mkdir khi chạy lại) là lỗi rig đã sửa, không tính thành finding sản phẩm hoặc ca ĐỎ của r2. Không sửa rig để đổi kết quả phản chứng được báo ở trên.

## Tiêu chí A1–A12

Đây là audit thiết kế test, không cấp nhãn A1–A12 đã nghiệm thu: mã r2 chưa được viết. Bộ nền được chạy riêng; D3/D4 chỉ thử các vị từ được ghi rõ trong script. “Giết mutant” phải là ca test đỏ với đối chứng khác họ xanh, không chỉ mutant trả rc khác 0.

| A | đơn vị và phép đỏ | đột biến đúng ca? khả năng xanh/đỏ |
|---|---|---|
| A1 | Tập holder, 3 cặp X, map cặp→ref, nhãn expiry/revocation; đã tách smoke động | **Đúng hơn r1.** Fixture đo trước X/Y, sau Y; known-only cho X/Y nên đổi màu thật. Bỏ loader/dòng in có assertion phân biệt. Fixed clock giúp mutant không được cứu bởi hết hạn. Smoke chỉ1 g2 sau M5 là kế hoạch, đã mô phỏng trên dữ liệu thật nhưng chưa land/đo production. |
| A2 | 1 cặp/3 ref; nguồn canonical bằng server symref | Any-ref/local HEAD/fallback có negative khác control, dựng được. Đã chạy local fake/main. Thiếu wrong repository identity N1; chỉ default đúng chưa là nguồn đúng. |
| A3 | 5 mã0/8 và precedence | Ba phản chứng cũ đã đóng, OR fallback/any-ref/bỏ áp toàn ID sẽ sai ca đích. Fixture lịch sử cần anchor tiêm nội bộ hoặc import object lịch sử thật; không thể tạo tùy ý OID b416830 bằng git init. Cần ca closed-list không tự mở rộng từ candidate và delta dữ liệu gate N6. |
| A4 | Y chết bởi hai nguồn, có/không thay thế, live control | Guard độc lập theo nguồn là khả thi; đã đo nhánh Y chết theo lịch sử→8. Khi dùng hàm trạng thái chung, mô tả mutant phải chỉ rõ bỏ nhánh nguồn nào, không giả luôn còn hai hàm guard riêng. |
| A5 | rc11 + W/path; fixed clock; canonical exact/prefix | Ba ca cũ đã đỏ đúng chiều. Cần closure và symlink/parent N5, malformed-live set→12. Nếu Q3 là precondition của CLI thì check trước publish0 không thể xanh; phải tách hàm thuần/CLI hoặc ghi published là điều kiện điều phối, N9. Payload Unicode thuộc lớp cấm: **not_run**, điều phối dựng. |
| A6 | Tên/SHA, pinned OID, thiếu object; median ratio≤2 từ3 lượt xen kẽ | Static stale12, đọc OID đã so không trôi, missing blob12 đều đo được. Mutant chỉ tên/refname đúng đích; thêm recapture-then-pin N2. **Chưa có numerator mã r2**, không lấy timing baseline làm chứng ratio. Fixture phải nêu thời điểm đổi ref và dùng đúng snapshot clock. |
| A7 | Mỗi ràng buộc M1 một lỗi + control; các consumer | Đủ hướng parser/error precedence; no-bool, key duplicate, allowlist có ca đích. packet_loop nhận **RC_STATE**, không nhận nguyên rc4/12: so mã ánh xạ và diagnostic gốc. raise→continue phải so verdict thực, r2 đã sửa điểm này. M4/all-entry validation và JSON khối mới còn N7/N10; không suy mọi consumer đã chạy từ parser pass. |
| A8 | Map ứng viên + rc, không metadata log | Sửa ứng viên/merge ours đều8; draft trước admission có thể0. Mutant quét default/log-only bị giết. Map còn thiếu mode/type N7. Ca second-parent hợp lệ→0 và mất record→8 phải tách N9; vị trí parent không tự là vi phạm. Phải test exact tree trước canonical và drift S/T, không chỉ gọi hàm rời. |
| A9 | Fake API giữ trạng thái, endpoint/ID/counter, content/account/scope/HTTP | Phủ định/prefix→8, 404→12 đã đo; khối hợp lệ→receipt. ≥1 call giết bỏ thân cổng **khi đã được gọi** nhưng chưa giết event/job không được tạo: cần ma trận W, N3/N4. Thiếu JSON strict/object-type mapping và downstream behavior sau xóa object, N10/N11. rc9 không được bypass admission. |
| A10 | 5 route × live/revoked/unknown, state/history/attempt/post, repeat/root | Bốn route sau đạt theo mô phỏng; mutant helper-only vẫn tới accepted ở baseline. record-lease không có ID trong state nên live không xanh và revoked không đạt postcondition stale/event: N8. Cần ID ứng viên + receipt cache/root explicit; lỗi ghi state vẫn phải chặn và không phát hành side effect. |
| A11 | Base/candidate cùng invocation, tập ca/delta theo tên; actionlint + shellcheck; wiring thật | Hợp đồng evidence tốt hơn r1. Nền local120/121 và278/278 đã đo; candidate r2 **not_run**, nên chưa có delta. Wiring bootstrap/canonical mandatory cần sửa N3/N4. In tổng121/121 hoặc t32 trích thân không chứng minh job đã chạy trên đúng event/SHA. Không cài wrapper tải mạng trong review này. |
| A12 | Command/SHA/tree/rc/byte, registered/executed/pass/fail/skip/not_run | Có khả năng đỏ: runner không gọi suite, chỉ banner, bỏ ca phải bị detector độc lập bắt. r2 nêu các mutants hợp lý; chưa có detector mới để chạy. Output byte dương là điều kiện cần, không thay executed count hoặc nguồn receipt. Ca cấm do điều phối chạy; reviewer không được gộp not_run vào passed. |

## Nhất quán luật và kích thước

| nguồn đã đọc | kết luận |
|---|---|
| Protocol §3.2, ADR-0025 | Q12 đúng khi không kế thừa miễn trừ wp461 r2 g1. Policy SHA/effective closure/checks/land obligations phải cùng băm hợp đồng trước ready; băm raw SPEC đang review chưa thay băm Issue đầy đủ. Wiring mới không thể là prerequisite trước lease viết chính wiring ấy, N4. File policy được protocol chỉ tên chưa có ở base: thiếu dependency thật, không được tự bịa closure. |
| §4, ADR-0028 | Q5/Q11 nhận generation mới, stale/giữ last SHA/state/retention và dừng worker; cơ chế máy push/heartbeat/handoff/land vẫn là nợ công khai. Trình tự thủ công cần fact có thẩm quyền và phải thực hiện trước bắt đầu mới; reviewer offline chưa xác minh được việc dừng. Không tự cherry-pick, không dọn worktree trước process dừng, không coi merge tự giết lease. |
| §5 | So effective set toàn repo, resolve symlink/parent, policy closure: còn N5. Slice nối tiếp chỉ chạy trên integration đã nhận predecessor; riêng code cho NEO phải có thật ở canonical, không chỉ ở integration/PR đang mở. N4 chưa được Q7 giải. |
| §8, CLAUDE/AGENTS reviewer | Review read-only, exact hash/base/tree và trung thực model/transport; hint chỉ chữ spec, không viết authority code cho executor. Không dùng comment submitter làm reviewer identity. Cần bằng chứng executable, đã có script/log/rc nhưng không mở rộng chúng thành production approval. |
| §12 | R2 đổi lời hứa snapshot là sửa có giá trị; đổi cách phát biểu không đủ đóng admission hỏng. Findings cắt ngang authority không thể để sau mà kích hoạt sổ. Giữ 14 ID cũ và lịch sử khi tách A0/A1; ID mới ở đây không reset failure/budget. Đây là lượt spec review thứ2; counters/PR receipt chưa readback, nên không tự suy còn quota gọi lượt3; bên điều phối đối chiếu Review Rescue Checkpoint theo luật. |
| ADR-0044 | Sáu file vượt3; tổng 655–945 đúng cộng. A=510–730/3 file vẫn vượt300; B=130–200/2 file, C≈15/1 file không vượt. Câu “không có cách chia MỘT slice≤300” không đúng cho B/C. Chưa có diff để chứng nhận estimate, tỷ lệ chi phí hoặc ngoại lệ đã được cấp. N4/N5/N8 thêm công việc nên phải ước lại, không kéo scope ngầm. |
| CLAUDE: có MẶT ≠ có ĐO | M9 có path/call không đồng nghĩa trigger/job/canonical code có thật; N3/N4. Base suites có counter thật, nhưng không thay tests r2. |
| CLAUDE: ba trạng thái/đo thứ đã đến | M1/HTTP contract đã tiến bộ. Admission phải giữ mode/source/candidate identity; M7 thiếu target/cache proof; body hash rời S/T chưa đủ, N1/N7/N8/N11. |

Số học ước r2: 180–260 + 300–420 + 30–50 + 50–80 + 80–120 +15 = **655–945**. A = ba thành phần đầu **510–730**, B = hai thành phần kế **130–200**, C≈15. Mốc +409/+368/+328 là lịch sử đo được, không chứng minh ước mới đủ dòng hay đã được chấp thuận ngoại lệ. `HINT.patch` là sửa spec chứ không là diff runtime để đem so ngưỡng đó.

## Q7–Q12: phần cần chốt và phần luật đã quyết

| câu | quyết định còn phải chốt | điều không phải tùy chọn |
|---|---|---|
| Q7 | Packaging/ngoại lệ cụ thể; chọn bootstrap A0/A1 hoặc một dependency tin cậy tương đương, estimate riêng, Issue/lease/base mỗi slice | Numstat trước review; không cắt test/PR chồng lấn để lách trần; predecessor đã được nhận; NEO phải có code đã canonical. A hiện tại chưa là bootstrap khả thi. |
| Q8 | Object cụ thể chứa lệnh r2, ID/URL/body fields/đích cấp lại; chưa có object đạt được reviewer readback | Account allowlist, đúng repo/Issue và lệnh tương ứng. Bot projection không đủ. Không có phép thử Git nào xác minh tác nhân người so với agent dùng cùng account. |
| Q9 | Nhận event của lease đã hết hạn là lựa chọn sản phẩm; khuyến nghị nhận hợp lý để tránh race soạn/merge | Không đảo ngược event/tái dùng ID chỉ vì hết hạn; không suy hết hạn từ lịch dự kiến. #456 nay đã đo hết hạn, không cần giả định nữa. |
| Q10 | Cơ chế event/check/provenance và bằng chứng ruleset/bypass/direct-push, exact S/T; thời điểm activation | Authority trước hiệu lực, không skip, không lấy default đã merge làm bằng chứng gate từng chạy. Chưa đo thì không activation. “Chỉ chưa ghi M5” chưa mô tả đầy đủ trạng thái reader trong bootstrap. |
| Q11 | Fact dừng worker cũ, inventory last SHA/state/journal và ai tuần tự hóa; chọn dependency máy hay quy trình có giới hạn công khai | Generation/stale/retention theo luật; readback fresh trước bắt đầu; check không acquire. Không coi một dòng xác nhận tương lai là cancellation đã xảy ra. |
| Q12 | Hợp đồng root/target/cache receipt, source identity, closure/policy và readiness của từng slice; khắc phục vòng bootstrap | Dispatcher tính phái sinh và đưa vào spec hash, dependency/base đúng; thiếu giữ proposed. Runtime wiring mới là nghiệm thu A1/prerequisite activation, không là điều kiện cần code chưa viết trước lease A0. |

## Bảng đo lại

D1 = `scratch/measure.py`, nguồn tất cả phép Git là `cay-kho`, timestamp **2026-09-07T14:33:15.126184Z**. D2 = `scratch/cli_measure.py`, CLI chạy trong `cay-kho` với origin **override chỉ trong tiến trình** sang `scratch/mirror-server.git` dựng từ chính snapshot; không sửa config repository. Vì vậy D2 đo hành vi offline, **không đo độ tươi GitHub hoặc origin gốc**. Bản sao để chạy suite giữ nguyên code base; không áp hint/code r2 vào đó.

| lời khai/con số | đo lại | lệnh/nguồn và giới hạn |
|---|---|---|
| SHA SPEC r2 | `9e775a154dd83741fd4e7af85aaeae1f5693ceabc5c5763cf6890ff4f2606c80` | sha256sum SPEC.md và bản untracked trong cay-kho, khớp cả2 |
| r1/verdict/hint được cấp | SHA r1 `43844cb2ea2653f502320a6f35a6e3ae7fd182770f02b62d4d73b9aa8dbea6f9`; verdict `b60a755f611bf814e0c9116e1cb5c9c4f9cb5ac3f1a6e96a951cd3dc7f17123e`; hint `1aeb9621efd07c74db90fd761a6e699b27ddb54ce703623a2936d253b4cd8eb2` | sha256sum, đúng artifact lượt1 |
| base/tree, abbrev | b416830… / 266a2aba… (full ở đầu verdict), core.abbrev **7** | rev-parse HEAD/HEAD^{tree}, config --local core.abbrev |
| 303 ref, 302 remote | **303 = 302 remote + 1 local master** | for-each-ref refs/heads refs/remotes, trừ HEAD symbolic; detached không làm mất local branch |
| 288 cặp · 273 đường · 273 ID | **288 / 273 / 273** | ls-tree theo ref/OID, cat-file YAML, khử trùng blob/path |
| 7 ID nhiều blob | **7**, số blob2,2,4,4,5,3,2 | D1 multiblob |
| 8 ID còn hạn, 4 chưa bia mộ | **8/4 tại clock13:41Z**; **7/3 tại14:33:15Z** | Parse expiry so hai clock; #456 đã hết hạn. Số cũ là lịch sử, không tiếp tục dùng cho “hiện tại” |
| #456 14:27:45 còn hạn, hết14:30:07 | Trường expiry **2026-09-07T14:30:07Z**, tại14:33:15 đã hết | Không tái hiện observation API14:27:45; có thể phân loại offline ở clock đó bằng dữ liệu Git |
| 7 tệp bia mộ trên master | **7**, cả7 cặp đúng hai chiều/ID==tên; 1 cặp wp461-r1 còn hạn ở giờ đo | D1 master_tombs; nhóm2 ci-jsonschema,1 khong-do-duoc,3 lease-hoi-toan-kho,1 wp461 |
| 11 tệp trên #468 | **11**, thêm3 gate +1 mutant so master | ls-tree/cat-file ref origin/claude/soan-spec-3-viec-treo-20260906; cả11 cặp có backlink trong tree ấy, không đồng nghĩa authority canonical |
| #468 31 commit riêng | **0 31** | rev-list --left-right --count origin/master...origin/claude/soan-spec-3-viec-treo-20260906 |
| r2 có2 cặp | **2**, một path; blob `26f07b4fe49964034c710864f350402fe5bf55c3` và `fdfde3a57ab9fd2c83454e9b9b2eff96f77ef229` | D1 special_pairs |
| 26f07b4 trước PR475 4 ref | **4**: heads/master, origin/master, origin/ops/cap-lease-461, origin/claude/soan-spec-3-viec-treo-20260906 | ls-tree mọi ref |
| 26f07b4 sau PR475 5 ref | **CHƯA ĐO** trạng thái sau PR475; snapshot chỉ4 | Không có nguồn mới/ref thứ5 trong tập được cấp; không kết luận lời khai GitHub sai chỉ từ snapshot thiếu |
| fdfde3a có bia mộ trên1 ref | **1**, origin/ops/lease-wp461-g2 | D1; toàn bộ5 occurrences r2 là2 cặp, không phải5 dòng/cặp |
| 8b2103c mutant chưa bia mộ11 ref; 1f95042 có1 | **11/1** | D1 full blobs `8b2103c…`/`1f9504281c3415f7194e124eb7b2702c34c8efd1`; số ref không thay vì expiry trôi |
| gate r4/g2 mỗi1 ref | **1/1** | Quét ID trên các pair/ref; #468/ops lease-g2 |
| planned dạng cũ3 lease, đều hết hạn | **3 ID**, plat-x4-exec-1, plat-x5-exec-1, plat-x5-exec-1r2; đều hết hạn | D1 parsed fields/expiry; không phải3 ref |
| symref máy chủ master / local clone điều phối không symbolic | **CHƯA ĐO nguồn điều phối**. Mirror này **có** local symref HEAD→origin/master; khác lời khai về clone kia | git symbolic-ref refs/remotes/origin/HEAD; không gọi origin gốc ngoài cwd. Bare fixture master/main/wrong local HEAD đã chạy, không phải GitHub |
| ls-remote/cache tên0/0, branch agent/wp461 rỗng hai lần | **CHƯA ĐO** hai thời điểm/canonical nguồn; **0** remote-tracking agent/wp461 khớp trong mirror | for-each-ref theo mẫu; không có thẩm quyền freshness và không suy không có process/commit chưa push |
| 6635379 “một SSH signature”, marker2 | **1 gpgsig, 2 dòng chứa SSH SIGNATURE (BEGIN/END)** | cat-file -p; không phải2 chữ ký, chưa verify signer |
| b416830 một PGP signature | **1 gpgsig PGP**, raw author ducthangho, raw committer GitHub | cat-file -p; không phải API login/web-flow proof |
| `%G?=E` và HTTP403/249 byte | **E đo lại** ở b416830 với GNUPGHOME rỗng trong scratch; HTTP403/249 B **CHƯA ĐO** | git -c gpg.program=gpg show -s với format %H %G?; không truy khóa/mạng, không xác minh signer |
| actor 5 run372–376, author.login claude, bot comment5569885143 | **CHƯA ĐO** | API facts không nằm trong Git. R2 ghi phía điều phối đo; reviewer không xác thực lại account/body/ID/receipt |
| ai-dang-giu launcher2, rc11 | **2, rc11**, 3.543 / 3.676 / 3.687 s, median **3.676 s**, mỗi2217 B | D2 native CLI, origin nội bộ thay trong tiến trình; baseline, không benchmark r2 |
| 3 đường wp461 còn lại đều2 | **2, rc11** mỗi đường; CHANGELOG3.804 s, kế hoạch provider3.436 s, ops/bien_nhan_v2_test.py3.480 s; mỗi941 B | D2, đúng4 đường từ g2 YAML |
| check g2 đăng được | **rc0, 240 B** | python3 cay-kho/ops/lease_publish.py check scratch/g2.yaml --root cay-kho; không đo độc quyền/online admission mới |
| _kiem_bia_mo 595–617, any606–610 | **đúng** | AST/read code base |
| kiem gọi _lease_cham_duong0 lần | **0** | AST kiem787–890; chỉ là code base |
| record-lease/begin gọi helper; 3 cửa khác0 | **1/1/0/0/0** | AST theo5 route; D4 nền0/0/0→accepted dù helper bị chặn |
| --state-dir mặc định | **.claude/.packet_state** | parser dòng1972; các route hiện chưa có root/snapshot admission API của r2 |
| workflow neo mặc định + chỉ lease paths | **đúng**; command mới canonical chưa có, rc2 | YAML thật + W; chưa có actionlint mới hoặc GitHub run |
| registry master hiện0, M5 sẽ1 | **0 hiện tại**;1 là kế hoạch | ls-tree origin/master -- ops/thu-hoi; không tự ghi M5 |
| #250 +409 SPEC/2 file | **239+170=409**, xóa0 | diff --numstat 2854380^1 2854380 |
| #275 +368 mã/2 file | **149+219=368**, xóa0 | diff --numstat 7883aad^1 7883aad |
| #248 PLAT-X8 cuối +328/2 file | **89+239=328**, xóa1 | diff --numstat 647cfea^1 647cfea |
| PLAT-X8 mốc giữa265/313 | **265/313**, mỗi mốc xóa1 | diff 08bb4ecd..67a7fbe0 và08bb4ecd..86a55663; không dùng thay mốc land |
| estimate655–945, A510–730/B130–200/C15 | **phép cộng khớp**,6 file | Ước chưa có runtime diff, không phải kết quả đo implementation |
| lease_publish_test120/121, 9027 B | **120/121**, executed121, skip0, rc1, **9027 B**, chỉ t33 thiếu actionlint | TMPDIR dưới scratch, chạy bản sao nguyên code base; không chạy installer mạng |
| wrapper121/121,8726 B | **CHƯA ĐO lượt2** | Lời khai phía điều phối; chưa có actionlint/shellcheck setup được xác minh trong lượt này |
| packet_loop_test278/278 +81 mutants,8752 B | **278/278**, skip0, **81 mutants**, rc0, **8752 B**, TỔNG ĐẠT; file4733 dòng | Suite trên bản sao base; log cũng ghi78 lớp lách,35 ca bắt-oan,0 ngoại lệ |
| doc-claims-check strict0 | **rc0, ok:true,106 file, flags0, advisory367**,70861 B | Chạy bản sao base; mặc định không quét SPEC |
| doctrine-scan7/0; thêmSPEC | **7/0**, thêm SPEC **8/0**, rc0,69 B mỗi lượt | Chỉ kiểm doctrine scan, không chứng nhận consistency mọi AC |
| r1 run1842.764s,stdout233/stderr777646 B; model/effort metadata | **CHƯA ĐO** raw run.json | File raw không được cấp; không suy từ title SPEC hoặc verdict artifact |
| 19 D3 cũ, D4 và14 finding của r1 | **19 ID D3 tái dựng đủ;14 heading finding cũ=11P1+3P2** | Đọc artifact và assert tập ca trong script r2; không chạy file script r1 vốn không có trong cwd |
| hai hình dạng dữ liệu, ba lời khai hội tụ, một bất đồng cổng | Hai họ dữ liệu có trong Git; check0/holder11 tái hiện; quote “không cửa sổ” có trong r1 | Causal count/lịch sử API không được suy rộng; các commit3c4c587/ddb3200 là object Git đọc được, “3 lần” là phân loại tác giả |

## chua_do_duoc

1. GitHub hiện tại: server symref/default, tập heads/OID sau PR475, độ tươi cache, run372–376/actor/API author.login, comment5569885143, PR474/475 và Issue facts; origin gốc ngoài cwd không được gọi. Một bare dựng từ snapshot không là nguồn authority độc lập.
2. Object Q8 đạt schema/intent/account/body thật và receipt sau readback; thẩm quyền người thật trong cùng account/PAT không thể suy từ Git/API actor. Chữ ký mới chỉ đọc header, không verify signer hay tải khóa web-flow.
3. Ruleset/required check/provenance/bypass/direct-push, chính xác event/context/result SHA ở GitHub, full refs do actions/checkout nạp, workflow code được nền tảng thực thi. W chỉ chạy thân neo hiện có với bare nội bộ và mô phỏng trigger/job từ YAML; không phải một run Actions đã chứng nhận admission.
4. Mã r2, delta base/candidate r2, tất cả parser/consumer/M9 mutants mới, actionlint/shellcheck của workflow sửa và wrapper tải công cụ; A6 ratio≤2 chưa có numerator. Stub command của W chỉ là probe bootstrap, không phải implementation hay gate xanh.
5. Hợp đồng/hiện vật source identity, cache receipt của loop, canonical policy/closure cho chính packet và legacy leases. Base thiếu file policy được protocol chỉ tên; không thay bằng dữ liệu fixture hoặc tự thêm vào kho.
6. Dừng worker cũ, tăng generation/state projection/journal, last SHA đầy đủ, retention/cancellation, fencing push/heartbeat/handoff/land; readback cấp lại tuần tự Q11 chưa được thực hiện trong review read-only.
7. Các payload lớp user cấm (đường thoát cây, đồng tự Unicode, chuỗi thoát) và mọi phép thử cần chúng: **not_run**, giao điều phối bằng mô tả lớp lỗi. Không tự dựng để tăng coverage. Phép alias symlink đã chạy không thoát cây.
8. Kích thước implementation sau bổ sung bootstrap/closure/cache, ngoại lệ ADR-0044 được người có thẩm quyền cấp, raw run.json/model receipt/counters review của lượt1 và ngân sách hiện tại. Không suy “lượt2” thành quota còn lại hoặc tự mở review mới.

**Phạm vi patch:** mọi N1–N11 có hunk trong HINT.patch: Q4/A2/A6 (N1/N2), M9/Q7/Q10/Q12/A11 (N3/N4), Q3/A5 (N5), Q6/A3/A4/activation (N6), M1/M4/A8 (N7), Q5/A10 (N8), Q3/A5/A8 (N9), Q2/A9 (N10/N11). Patch còn bỏ câu sai tuyệt đối về slice≤300 và tách số5 ref sau PR475 khỏi số đo snapshot. Không áp patch vào SPEC gốc/cay-kho.


Kiểm artefact cuối: `patch --dry-run -p0` và áp thật trên bản sao đều rc0; byte-match với draft dự kiến. HINT.patch có17 hunk, sha256 `02b562b36c546f3a9620849c8df3a088306c7e01e211cb21a467f069bcf60c9c`; SPEC sau áp trên bản sao sha256 `582fc8e94b77b178c1e29cda219f474e6da1980570e0992e1d73ca106db20fa6`. SPEC gốc giữ nguyên băm đã review; git diff --quiet rc0, status chỉ có SPEC untracked ban đầu. Receipt chi tiết: `scratch/final-audit.json`.
