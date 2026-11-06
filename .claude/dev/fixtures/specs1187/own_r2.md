tran_kich_thuoc_sensitive: ADR-0053@8ab100793df9831505f495543a74044b91c2c9ab

# PR1184-MERGE-CONTRACT r2 — DỰ THẢO CHỜ CHỦ KHO DUYỆT, CHƯA GRANT

## Định danh, authority và phạm vi quyết định

- packet_id: PR1184-MERGE-CONTRACT; revision: 2; generation: 2.
- packet_issue: https://github.com/ducthangho/tra-luat/issues/1187; mission_issue: #1177 chỉ là dependency cần chủ kho điều phối.
- Canonical base: 1f0941e9bba1d1d517eda4174167b81963c06bd5. Tiếp nối frozen r1 H abc6bdab035b14bf24f55ea5d557233c927ad951, tree 94da193973b02d28e7f67d222e968dea66342f7f.
- r1 được chủ kho duyệt exact SHA256 056804c42c3ae5fe867257b12ce99fe8a4a9045e4716b2e675769f7bb052fe71. Giữ nguyên byte r1; r2 là quyết định authority mới, không hồi tố grant r1.
- review_class: sensitive; risk: sensitive. Executor: fresh Codex Desktop session, openai_codex / codex_desktop / machine, cloud Linux; không khai CLI hay model identity chưa xác minh.
- Reviewer bắt buộc: human độc lập Executor, human / manual_audit / human, assurance_target human_audited. Human audit, approval, authorization và land là các quyết định riêng.
- Trạng thái: chỉ là proposal scratch theo chỉ thị điều phối; chủ kho CHƯA duyệt r2, lease r2g2 CHƯA cấp. Không push product code hoặc yêu cầu merge dựa spec này.
- Sau khi owner duyệt exact hash: dispatcher publish frozen spec metadata, kiểm full namespace ownership/fence, cấp lease mới revision2/generation2/start_from abc6, giới hạn run mới và reviewed_sha_required cập nhật theo protocol. Không dùng lease r1 để triển khai acceptance r2 vào product.

## Lý do revision và số đo

Advisory Claude hoàn tất trên abc6 với changes_requested; không phải human assurance. Phản chứng thực thi trên abc6 tái hiện: later rerun bỏ qua owner transition; new human/external spec dùng khi ADR0063 chưa land; inline revision mâu thuẫn standalone vẫn được nhận. Duplicate-key fixture cũ không đầy đủ nên không bắt mất guard. Cần sửa cùng contract và kiểm consumer thay vì giảm test để vừa trần.

nang_tran:
  ai_nang: "Chủ kho ducthangho theo protocol §2 — ĐỀ NGHỊ, CHƯA ĐƯỢC DUYỆT"
  can_cu: "K1/spec identity/hash là input K4, cùng rollout ADR0063 và test consumer. Có thể tách thành nhiều Packet/ADR/lease nhưng tăng coordination và trạng thái trung gian; đề nghị review cùng một contract. Bỏ productcopy spec r1 đã supersede, giữ frozen metadata/history; net base diff năm tệp, effective write set sáu paths. Số đo exact numstat kèm proposal; cap dư có giới hạn cho sửa review, không bảo đảm gói lớn dễ review."
  tran_cu: "ADR0053: 6 tệp/450 dòng thêm; approved r1: 5 tệp/450 dòng thêm"
  tran_moi: "6 effective paths, tối đa 5 net tệp/1000 dòng thêm — đề nghị, chỉ áp dụng khi chủ kho duyệt exact spec và lease r2g2"

Trần 1000 là trần đề nghị, không tự cấp quyền. Diff thực tế phải <=1000 dòng thêm và đúng effective write set sáu paths dưới đây; receipt numstat/hash/patch đi kèm là căn cứ review. Không nén code hoặc bỏ negative/mutation để đạt số. Nếu vượt, dừng trước review và trình số đo mới.

## Write set sản phẩm — đúng sáu đường dẫn

1. .claude/dev/packet_loop.py
2. .claude/dev/packet_loop_test.py
3. docs/PROTOCOL_DA_PHIEN.md
4. docs/adr/0063-merge-spec-ref-va-human-audit.md
5. ops/specs/PR1184-MERGE-CONTRACT-r1.md — DELETE productcopy đã supersede; không sửa frozen metadata r1 hoặc byte lịch sử ở abc6. Owner phải duyệt xóa path này trong continuation.
6. ops/specs/PR1184-MERGE-CONTRACT-r2.md — nguyên byte spec r2 đã duyệt, để canonical checker cũ đọc spec tại H cho bootstrap.

Net base..candidate là năm tệp; effective write set sáu paths cho phép; actual continuation abc6→r2 chạm năm paths gồm xóa productcopy r1 và thêm r2, protocol không đổi so với abc6. Frozen r1 vẫn nguyên byte tại metadata36b040e40503a810be20dced6dcd5f73d57110c8 và parent abc6. Lease/spec metadata được publish riêng, ghim source OID/hash và không chèn receipts vào product H. Spec không tự chứa hash của chính nó. Không sửa CI workflows, launcher, lease publisher, five environment files của #1184, release/corpus/registry, rulesets hoặc lịch sử ADR Accepted. Không sửa spec/lease/H của wp1178 r3g3.

## K1 — nguồn spec

Legacy không có spec_ref giữ nguyên đọc bytes tại H và so spec_hash; không tự áp spec_sha256_required của đường mới. Khi lease khai spec_ref, bắt buộc refs/heads/...@OID40, đúng spec_path/--spec, object đọc được, SHA256 khớp spec_hash và spec_sha256_required nếu có. Tên ref là nhãn vị trí nguồn; authority là lease frozen OID/path/hash, không resolve ref trôi hay đòi nhánh vẫn tồn tại. Nguồn authoritative lỗi thì fail-closed, không fallback. Có blob tại H thì phải cùng bytes/hash.

Packet_id lease là nonempty str; revision là positive int chính xác, không nhận bool/string. Thu tất cả standalone packet_id/revision, inline Markdown packet_id/revision và H1 '# <packet> r<N> — ...'; mọi khai báo cùng có mặt phải thống nhất và khớp lease. Bỏ fenced examples/HTML comments khi đọc identity; Markdown không đóng thì chặn. Không lấy working tree làm authority. Giữ nguyên ADR0062 cho 0/1/≥2 khai dieu_kien_merge.

External K1 và mọi nhánh human K4 phải kiểm ADR0063 đã có hiệu lực: history không shallow, đọc được first-parent origin/master, commit giới thiệu path nằm trên chuỗi đó, path vắng ở parent đọc được, intro và current master đều đủ ADR0063_ANCHORS. Có file rỗng, thiếu anchor, đọc lỗi hoặc chỉ có file ở H đều chặn. K0 vẫn giữ ancestor base/head/origin/master. Dispatcher kiểm freshness bằng fetch/readback thật; checker không tự chứng minh network freshness.

## K4 — human audit tách khỏi model artifact

Giữ nguyên model run/stdout validation. Human dùng raw API GitHub owner comment riêng; không biến human thành run.json/stdout model. Canonical repo ducthangho/tra-luat, user.login ducthangho, user.type User, author_association OWNER, ID positive int chính xác, issue_url và html_url đúng repo/PR/ID, created_at/updated_at canonical UTC hợp lệ. Thiếu input trả lỗi rõ; không tự nhận free text, agent repost hoặc raw file giả là audit thật.

Body là duy nhất YAML đóng schema, không duplicate key/alias, với đúng keys:

```yaml
schema: human_exact_head_audit.v1
packet: wp1178
revision: 3
generation: 3
pr: 1184
reviewed_sha: a7b5aedc122575a66280ace3ff7f2567251af8e2
reviewed_tree: 11b2a8a93a5b1dbb0bf36e14f8d3e19116ae15cc
spec_sha256: 4fe4cc94da39fff575b3c0c60d3d2795af3afd948f08359a3e8a5b9d94ff67bf
verdict: approve
assurance: human_audited
review_axes: [spec, standards_security]
open_findings: []
audit_source: https://github.com/ducthangho/tra-luat/pull/1184#issuecomment-EXAMPLE_ONLY
```

Đây là ví dụ schema, KHÔNG receipt hợp lệ và KHÔNG lời audit đã đăng. Field packet/revision/generation/PR/full H/tree(H)/spec hash phải đúng type và exact bindings; audit_source là URL chính raw comment. revision/generation/PR positive int, không bool. Unknown/missing keys, short H, wrong actor/tree/spec/generation/verdict/axes đều chặn. open_findings là list {slug,severity}; slug kebab ASCII, P0–P2 chặn, P3 chuyển K5 human:<slug>; waiver phải qua đúng owner mechanism hiện có với exact tập slug. Truyền cả model và human thì cả hai đều phải hợp lệ; không có cả hai thì chặn. Audit không thay approval/authorization/merge.

## Thời điểm M5/M12 và chuyển tiếp owner

Human dùng --human-remote-run và toàn bộ --workflow-runs đã kiểm completeness theo K2. Chọn mọi run đúng repo/full H, kiểm positive id/origin URL/event nonempty/time hợp lệ, lấy created_at nhỏ nhất; selected raw run phải hiện diện đúng các fields id/head/repository/URL/event/time và đạt min time. Khi đồng thời nhiều run sớm nhất, nhận một raw run thuộc tập min. Later rerun không chuyển candidate lịch sử thành candidate mới.

Candidate mới sau mốc ADR0062 cần audit.updated_at trước run sớm nhất. Raw JSON chỉ chứng minh consistency của readback được cấp, không chứng minh transport provenance hay tuyệt đối lần push đầu; retention/no-CI có thể thiếu lịch sử. Operator phải xác minh GitHub nguồn và push timeline, không dùng rerun để hợp thức hóa audit sau push.

Mốc cố định: ADR0062 land 1f0941e9bba1d1d517eda4174167b81963c06bd5, GitHub merged_at 2026-11-04T08:36:24Z. Candidate có run sớm nhất trước mốc được dùng human audit sau push CHỈ khi có thêm owner raw comment đóng schema human_audit_transition.v1 với đúng keys: schema, packet, revision, generation, pr, reviewed_sha, reviewed_tree, spec_sha256, adr0062_oid, remote_run, disposition, reason, transition_source. Các bindings như audit; adr0062_oid bằng mốc, remote_run URL selected earliest run, disposition accept_post_push_audit, reason nonempty str, transition_source URL chính comment. Kiểm mốc trên first-parent master và thực sự đưa ADR0062 path vào cây, path vắng ở parent; mọi git rc lỗi chặn. Rollout ADR0063 vẫn bắt buộc.

Đây là ngoại lệ thời điểm cần owner disposition hiện thời, không tuyên bố review trước push. Existing #1184 owner free text không tự nâng thành schema. Hiện structured successor audit/transition chưa tồn tại; không tạo receipt thay owner. Không reset H/push/advisory history. K0/K2/K3/K5/K6/K7, M1/M3/M6/M9, Windows và CI exact H giữ nguyên. #1184 budget checkpoint owner vẫn cần.

## Nghiệm thu và phản chứng bắt buộc

- A1: legacy source/hash tại H qua; bytes/hash sai đỏ; legacy optional field giữ hành vi cũ.
- A2: pinned external source đúng qua sau rollout; ref/path/object/hash/packet/revision/type/conflicting declarations/source bytes sai đỏ. Chạy actual wp1178 r3 blob và actual frozen own specs có fenced sample receipt.
- A3: ADR0062 0/1/≥2 khai giữ kết quả; canonical bootstrap của chính Packet dùng checker base và spec r2 tại H, không tự dùng code mới.
- A4: structured human đúng bindings nhận riêng; single-field/missing/unknown/duplicate/alias/free-text/actor/time/type sai đỏ. Duplicate fixture phải đầy đủ mọi field khác; bỏ duplicate guard phải nhận sai và bị test phát hiện.
- A4b: positive historical transition với earliest complete K2 evidence và owner disposition; later rerun bypass, thiếu policy, empty/current/introduction policy, non-first-parent/shallow/git read errors, missing/wrong transition đều đỏ. Test CLI transition và mutant cụ thể.
- A5: model path cũ giữ regression; human/model conflict và neither-review đỏ. Missing human input rõ và fail-closed.
- A6: P3 qua CLI K5 chặn khi chưa waiver, exact owner waiver nhận; P0–P2 chặn. Bỏ forwarding phải bị CLI case bắt.
- A7: giữ toàn bộ K0/K2/K3/K5/K6/K7 và legacy fixtures, complete packet-loop suite, doctrine/ADR/doc-claims checks; không coi related subset là full suite.
- A8: doctrine ADR0063 có contract source/timing/rollout/authority/budget và protocol registration; không sửa lịch sử Accepted.
- A9: spec r1 frozen metadata/history giữ đúng, productcopy bị xóa theo write set mới; r2 exact owner-approved bytes/hash xuất hiện tại H, canonical legacy K1 qua.

Mỗi mutant có intended consumer, actual positive controls và phân loại kill đúng property; import/setup/crash/timeout không tính kill. Guard dư thừa không thể bỏ đơn lẻ để vượt contract phải được ghi rõ thay vì dựng mutation credit. Actual #1184 raw data phải vẫn blocked cho tới ADR0063 land và owner structured records; chỉ dùng synthetic fixtures để thử positive, không ghi chúng là GitHub receipts.

Trước heavy tests: canonical base admission, ownership/fence, diff/write-set/numstat. Chạy full packet-loop, targeted positive/negative và related mutations thật, doctrine/adr/doc checks. Windows M3, GitHub full_mutant_audit M9, PR CI và master CI required; khi chưa push vì thiếu offline human audit phải ghi not_run, không giả receipt. Tests >5 phút có progress.

## Review budget, handoff và stop

Giữ toàn bộ lịch sử r1: hai Codex transport attempts thất bại không review text, một Claude advisory completed changes_requested trên abc6. Theo ADR0052 chỉ tính khi đo output/token thực; không coi failed attempt là verdict và không reset ledger. Tối đa hai model calls có output của Packet giữ nguyên; trước rereview dispatcher checkpoint budget, không tự nâng. Independent human audit exact final H/tree/spec trước first code push vẫn mandatory theo sensitive/M5/M12; model advisory không thay thế.

Run r1 tối đa90 phút không được kéo bằng expiry; r2 cần lease/run clock mới sau owner grant. Không push, tự approve hoặc land. Handoff phải có final H/tree, exact spec/hash, diff/numstat/paths, source/test hashes, commands/rc/positive-negative counts/mutant receipts, limitations, bundle hashes. Giữ old-head interrupted/failed evidence riêng. Sau owner duyệt r2 mới đưa patch scratch vào product dưới lease mới, chạy đủ checks trên exact H, rồi human audit và authorization land riêng.

## Ghi nhận quyết định chủ kho cho r2

Chủ kho đã trả lời “Nâng trần 1000 đi” cho hồ sơ r2/g2, giữ phạm vi và acceptance nêu trên. Chỉ thị này duyệt trần1000 dòng thêm và continuation/lease r2g2; các nhãn dự thảo và điều kiện chờ duyệt trong phần đề xuất phía trên là lịch sử soạn, không phủ quyết chỉ thị mới. Đây không phải human code audit hoặc quyền land. Dispatcher ghi nhận bằng comment Issue1187 và lease riêng; clock grant là thời điểm cấp thực tế, không suy thời điểm từ câu trả lời chat.
