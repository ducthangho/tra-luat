tran_kich_thuoc_sensitive: ADR-0053@8ab100793df9831505f495543a74044b91c2c9ab

# PR1184-MERGE-CONTRACT r1 — DỰ THẢO CHỜ DUYỆT, CHƯA CẤP LEASE

## Định danh và authority

- packet_id: PR1184-MERGE-CONTRACT; revision: 1; generation dự kiến: 1.
- packet_issue: CHUA_TAO; mission_issue: CHUA_CHOT. Không sửa kế hoạch Mission #1177 trong Packet này; việc gắn dependency hạ tầng vào Mission cần quyết định của chủ kho.
- nguon_cap_viec: chỉ thị người dùng trong chat ngày 04-11-2026: “Thực hiện theo quy trình tới khi đủ điều kiện merge”; sau đó duyệt mở Packet riêng và “chuẩn bị spec và lease để duyệt”. Chỉ thị sau cùng cấp quyền SOẠN, chưa phải quyền thi công hay grant.
- Nguồn tiền nhiệm: PR #1184, Packet #1178 r3 g3; báo cáo `/workspace/HANDOFF-PR1184.md`, log `kiem-merge` trong `/workspace/scratch/pr1184/`.
- Canonical base dự kiến: `1f0941e9bba1d1d517eda4174167b81963c06bd5`; đo lại master qua GitHub ngày 04-11-2026 trong phiên này, vẫn khớp. Trước grant phải đọc lại OID/full fence/ownership.
- review_class: sensitive; risk: sensitive, vì sửa merge/assurance contract.
- Executor dự kiến: phiên mới Codex Desktop, `openai_codex / codex_desktop / machine`, environment cloud. Không khai thành CLI. Phiên land hiện tại chỉ soạn hồ sơ, không thi công.
- Reviewer: human độc lập với Executor, `human / manual_audit / human`, assurance_target human_audited. Human audit nội dung và Approver cấp quyền land vẫn là hai quyết định riêng.

## Số đo và giới hạn

Đo trên base nêu trên ngày 04-11-2026: gói tương đương gần nhất `82adc57d1829bcac6aef6e8aae0b7f474054db94` (#1124) đổi 5 tệp, +207/-83 dòng; đây là số đo tiền nhiệm, KHÔNG phải dự báo diff Packet mới. Dự kiến Packet mới tối đa 5 tệp và 450 dòng thêm, theo ADR-0053 đã kích hoạt bằng dòng OID land ở đầu spec. Dừng trước review nếu vượt; không tự tăng trần. Diff thật chưa tồn tại nên numstat mới `not_measured`.

Không khai dòng nâng trần lời gọi Codex: dùng trần mặc định hiện hành, không suy được tăng trần từ số vòng. Trước mỗi lời gọi phải đối chiếu budget thật; dự kiến human audit chính và tối đa 2 lời gọi model bổ sung, không phải quota được tự cấp. Không reset lịch sử PR #1184 bằng Packet này.

Ownership chưa xác định: `lease_publish.py ai-dang-giu .claude/dev/packet_loop.py` rc12 vì clone thiếu nhánh máy chủ; không phải “write set rảnh”. Phải đồng bộ đủ namespace trong clone điều phối riêng, đo từng đường dẫn, đọc lease/tombstone rồi mới grant. Ref fence hiện tại gồm 1768 refs; so snapshot đầu phiên và snapshot mới nhất không có delta. Số này là số refs ở hai snapshot đã đo, không bảo đảm bất biến về sau.

## Write set sản phẩm — 5 đường dẫn chính xác

1. `.claude/dev/packet_loop.py`
2. `.claude/dev/packet_loop_test.py`
3. `docs/PROTOCOL_DA_PHIEN.md`
4. `docs/adr/0063-merge-spec-ref-va-human-audit.md` — số ADR dự kiến; phải kiểm tra còn trống trước freeze.
5. `ops/specs/PR1184-MERGE-CONTRACT-r1.md`

Đường dẫn thứ 5 là bổ sung so với proposal JSON ban đầu: bản spec của CHÍNH Packet hạ tầng này được phép hiện diện nguyên byte ở head để checker canonical cũ vẫn kiểm được K1 trong lúc triển khai. Không dựa vào checker chưa land để tự thông qua Packet mới. Spec/lease metadata ref vẫn được neo OID/hash riêng; lease và review receipts không chèn vào head đã approve. Spec không tự chứa hash của chính nó.

## Ngoài phạm vi

Không sửa năm tệp `ops/environment/`, H/tree/spec/lease g3 của Packet #1178, CI workflows, rulesets/branch protection, launcher, lease publisher, security path khác hoặc release manifest/golden/VERSION. Không deploy, không LIVE, không miễn K0–K7, không auto-merge, không tự ghi approval. Không đưa bản sửa scratch vào vai trò canonical checker. Không đổi budget cũ hoặc giả review offline trước push.

## Mục tiêu và contract đề xuất

1. Trong `packet_loop.py`, giữ đường K1 spec tại H hiện có; thêm đường đọc spec từ `spec_ref` bất biến trong lease, đúng protocol §3.2.1. Ref phải có tên `refs/heads/...@<OID40>`; object, path và SHA256 phải khớp nguồn được cấp, `spec_hash`, `spec_sha256_required` nếu có, Packet/revision của spec và lease. Không đọc spec từ working tree hoặc ref trôi để quyết định. Nhiều nguồn khai mà khác bytes/hash, field lỗi hoặc object thiếu thì fail-closed; không tự fallback sang nguồn khác khi nguồn authoritative lỗi. Vẫn áp đúng ADR-0062 cho 0/1/≥2 dòng `dieu_kien_merge`.
2. Trong `packet_loop.py`, giữ đường K4 model run/stdout cũ và thêm nguồn human audit riêng, không chuyển comment người thành run.json/model stdout. Nguồn là raw readback một owner comment trên đúng repo/PR, kèm receipt có schema đóng; so full H, tree(H), spec hash, Packet/revision/generation, verdict và identity. Không chỉ tin tài khoản vận chuyển receipt. Caller không đổi được danh tính chủ kho. Hai đường cùng được truyền nhưng xung đột thì chặn.
3. Trong `packet_loop_test.py`, thêm kiểm chứng hành vi dương/âm và đột biến làm rơi từng ràng buộc; giữ regression của K0–K7, legacy model path và exact-SHA CI.
4. Trong ADR mới và protocol, ghi contract nguồn, mốc có hiệu lực và giới hạn thời gian review. Duy trì sự khác nhau giữa human audit, approval, authorization và merge. Đăng ký ADR mới ở bảng §20; không sửa lịch sử Accepted hoặc nâng advisory thành human/cross assurance.
5. Giữ spec này nguyên byte trong write set để kiểm K1 legacy của chính Packet hạ tầng; sửa nội dung sau freeze phải revision/hash/authority mới.

### Receipt human audit đề xuất

Raw GitHub comment phải có `user.login` đúng owner canonical và `issue_url` đúng `/repos/ducthangho/tra-luat/issues/<PR>`, có ID/URL/time lấy từ API. Body chứa duy nhất một record YAML có schema cố định:

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
audit_source: https://github.com/ducthangho/tra-luat/pull/1184#issuecomment-6625327662
```

Đây là VÍ DỤ CHƯA ĐƯỢC CHỦ KHO ĐĂNG/XÁC NHẬN. Agent không được đăng nó như lời audit của chủ kho. `open_findings` phải ghi slug/severity rõ khi khác rỗng; P0–P2 chặn, P3 đi K5. Thiếu field/schema lạ/trùng key/OID rút gọn/actor sai/sai URL/H/tree/spec/generation đều chặn. Quyền maintain/auditor và source origin phải được kiểm theo protocol, không suy từ display name.

### Chuyển tiếp lịch sử — quy tắc ĐỀ XUẤT, cần chủ kho duyệt

H của PR #1184 đã push trước mốc ADR-0062; audit của owner diễn ra sau push. PR #1186 land ADR-0062 tại `1f0941e9bba1d1d517eda4174167b81963c06bd5`, GitHub merged_at `2026-11-04T08:36:24Z`. Receipt mới không thể làm review sau push thành review offline trước push. Đề xuất quy tắc chuyển tiếp sau, chỉ có hiệu lực nếu chủ kho duyệt và ADR mới đã land:

- Với candidate đã có readback GitHub run tạo trước mốc ADR-0062, đúng repo và full H, không đổi H/tree kể từ audit, K4 có thể dùng structured human audit hiện thời thay artifact model pre-push. Phải có comment chủ kho CHẤP THUẬN CHUYỂN TIẾP nêu Packet/revision/generation/H/tree/spec, URL run chứng minh H đã ở remote trước mốc, OID land ADR-0062 và lý do chấp nhận audit sau push. Comment này là điều kiện của nhánh human K4 cho ca chuyển tiếp; không giả receipt model.
- Bằng chứng thời gian và H phải lấy từ raw API run readback; OID mốc phải được xác minh trên first-parent master. Bằng chứng sai/thiếu hoặc H đổi thì không có đường chuyển tiếp; test âm/đột biến phải bắt từng điều kiện đó trong `packet_loop_test.py`.
- Đây là sửa điều kiện THỜI ĐIỂM M5/M12 cho candidate lịch sử được owner chấp thuận, không phải lời khai đã đạt trước push. M1/M3/M6/M9 và mọi gate K khác giữ nguyên; audit, CI, Windows, authority vẫn phải đủ exact H. Candidate push mới sau mốc tiếp tục yêu cầu review offline trước push theo M5/M12.
- Lịch sử số push, advisory calls/rounds và trần cũ được giữ nguyên. Chủ kho phải làm budget checkpoint trước khi gọi connector #1184; không dùng nhánh chuyển tiếp để reset hoặc xóa các lần vượt trần đã có.

Quy tắc này là PHẦN CẦN DUYỆT của spec, chưa là policy hiện hành. Nếu chủ kho không chấp thuận điều kiện thời gian chuyển tiếp, chỉ triển khai khả năng đọc metadata/human receipt sẽ chưa đủ đưa #1184 qua protocol; phải giữ blocked và chọn kế hoạch khác, không tự tạo exemption trong code.

## Nghiệm thu và phản chứng

| ID | Phép đo dương | Điều kiện phải đỏ / đột biến đích | Đường dẫn |
|---|---|---|---|
| A1 | Legacy spec tại H + hash lease đúng vẫn qua K1 | Đổi spec bytes/hash thì đỏ; bỏ hash check phải giết ca âm | packet_loop.py; packet_loop_test.py |
| A2 | Spec tại pinned metadata OID/path, cùng hash + Packet/revision lease, qua K1 | Ref trôi/OID hỏng/object thiếu/path khác/Packet khác/hash khác/khai hai nguồn khác nhau đều đỏ; bỏ mỗi binding phải bị bắt | hai tệp code/test |
| A3 | Trạng thái 0/1/≥2 dòng ADR-0060 giữ kết quả ADR-0062 | Một dòng sai hoặc ≥2 dòng không được về nhánh không khai; đột biến bỏ branch validation chết | hai tệp code/test |
| A4 | Human receipt thật đúng actor/repo/PR/H/tree/spec/generation/verdict được nhận riêng | Từng field bị tráo, missing, unknown schema, duplicate YAML key, agent repost hoặc free text không cấu trúc thì đỏ; bỏ từng neo phải bị bắt | hai tệp code/test |
| A4b | Candidate lịch sử có run trước mốc + owner transition exact H được xử lý theo ADR mới đã land | Run sau mốc/sai H/sai repo/mốc không first-parent/thiếu owner disposition phải đỏ; bỏ từng điều kiện phải bị bắt | hai tệp code/test; ADR mới |
| A5 | Legacy model run/stdout approve đúng H vẫn qua K4 | Sai H/rc/status/stdout hash/last verdict đỏ; không gọi fallback human khi model path hỏng mà chưa có audit độc lập hợp lệ | hai tệp code/test |
| A6 | Mọi finding giữ hạng/slug, P0–P2 chặn, P3 phải được đóng/owner xử lý đúng scope | Receipt có finding nhưng bị bỏ qua, hay nâng advisory thành human, thì ca âm đỏ | hai tệp code/test |
| A7 | K0/K2/K3/K5/K6/K7 không đổi; bộ fixture đầy đủ qua tất cả | Thiếu từng gate vẫn rc12; đột biến bỏ connector/CI/Windows vẫn bị bộ hiện có bắt | hai tệp code/test |
| A8 | ADR mới được đăng ký, contract nói rõ metadata/human/legacy/timing | Xóa từng mục neo hoặc đăng ký ADR làm doctrine/adr guard đỏ; giữ lịch sử cũ nguyên vẹn | ADR mới; protocol |
| A9 | Spec bytes ở head hạ tầng khớp frozen source/hash | Sửa spec sau freeze làm K1 legacy đỏ; không giải quyết bootstrap bằng tự chạy checker mới | spec; evidence |

A7 ở bảng này là mã nghiệm thu nội bộ, KHÔNG khai tiêu chí A7 đặc thù về consumer đột biến của protocol §10.2.3. Mỗi đột biến ở đây vẫn phải có receipt dương/âm đúng test/command/rc/property; import/setup chết không tính là bắt được.

Trước thi công: đo baseline cho phần đo được. Hiện K1 của #1184 đỏ vì spec tại H không có; K4 thiếu artifact; `doctrine-scan` trên canonical sạch 10 tệp/0 chỗ; test hành vi mới chưa tồn tại (`not_run`), không giả là ca đã đỏ. Khi có implementation, chạy full packet-loop tests, doctrine/adr checks, impact closure/admission và gate phù hợp scope. Vì diff chạm `.claude/dev/**`, Windows M3 và `full_mutant_audit` M9 đều required, cộng CI PR và CI master. Báo riêng rc, positive marker, passed/failed/skipped/not_run/not_measured.

## Hình dạng lỗi kế thừa

- `k1-spec-source-tree-vs-frozen-metadata`: 1 biểu hiện đã đo ở #1184 (log rc12), chưa có vòng sửa code trong Packet mới.
- `k4-human-audit-vs-model-process-artifact`: mismatch đã đo ở #1184; không có artifact model để hợp thức hóa human audit.
- `review-prepush-time-vs-migrated-candidate`: H đã push trước audit; không thể giải quyết bằng đổi schema receipt.
- Timeline #1184 có 5 comment advisory Codex và 2 comment human audit đã đọc; đây là số COMMENT quan sát được, không phải tổng model calls hoặc verdict rounds. Tổng budget dùng thực tế `not_measured`; phải giữ hồ sơ cũ khi checkpoint, không reset.

## Chưa đo được và stop condition

Issue/mapping Mission; actual executor session; durable grant actor/source; spec OID sau publish; clock grant/expiry; ownership đủ namespace; actual diff numstat; review/Windows/CI của Packet mới; transition decision M5/M12; budget checkpoint cho connector #1184 — đều chưa hoàn tất. Lease dự thảo phải giữ null cho các quyền chưa có, không đặt giờ quá khứ/tương lai giả.

Trước grant: chủ kho duyệt exact spec hash, chốt các mục trên; tạo Issue/spec metadata source bền, quét ownership, cấp lease bằng actor được protocol công nhận cho phiên mới. Không đổi metadata spec trong PR #1184. Sau thi công/review của Packet hạ tầng, chỉ land bằng authorization riêng exact H mới; sau landed mới chạy lại K0–K7 của #1184 trên canonical mới, thu Windows/CI/provenance/connector thật và authority base mới. Không merge #1184 chỉ vì Packet hạ tầng xong.
