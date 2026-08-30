# tra-luat — Agent Entry Point

> File này chỉ là CON TRỎ. Không định nghĩa lại protocol, legal doctrine,
> review budget, schema hay release gate.

## 1. Đọc trước khi làm việc

Theo thứ tự:

1. `CONTEXT.md` — từ vựng chung.
2. `docs/PROTOCOL_DA_PHIEN.md` — vai trò, state, review, handoff và stop condition.
3. `CLAUDE.md` — quy tắc phát triển, test và deploy của repository.
4. Packet Issue/Spec hiện hành hoặc chỉ thị điều phối bền của người có thẩm quyền —
   objective, revision, generation, base SHA, write set, acceptance, risk và authority.
5. `ops/KE_HOACH_THI_CONG_DA_PROVIDER.md` — chính sách provider chuyển tiếp.
6. Hợp đồng provider tương ứng:
   - `ops/KE_HOACH_THI_CONG_ANTIGRAVITY.md` cho lịch sử và phạm vi AG;
   - `ops/chatgpt_review/README.md` khi dùng ChatGPT Pro qua Web.
7. `SKILL.md` — bắt buộc khi Packet liên quan pháp luật, corpus, Drive,
   NotebookLM, registry hoặc hành vi runtime của skill.

Đọc được kế hoạch không đồng nghĩa được giao việc. Không có Packet Spec hoặc
authority được protocol hiện hành thừa nhận thì dừng.

## 2. Preflight bắt buộc

Trước khi sửa hoặc review:

- xác minh đúng repository, branch/worktree và exact base Git OID;
- xác minh Packet revision/spec hash/generation;
- xác minh effective write set;
- xác minh Review Class và capability cần thiết;
- xác minh provider và execution surface thực tế;
- giữ worktree sạch ngoài thay đổi thuộc Packet.

Lệch một điều kiện trên thì không tự sửa cho khớp; báo người điều phối.

## 3. Ranh giới vai trò

### Executor

- chỉ ghi trong effective write set;
- phiên Executor không chuyển vai sang Reviewer trong cùng session/run;
- không tự approve, merge, land, deploy hoặc gọi LIVE;
- không tự cấp lease hoặc mở rộng Packet;
- tạo handoff neo exact head/tree và bằng chứng test.

### Reviewer

- dùng session/context độc lập, không fork hoặc tái sử dụng context Executor;
- checkout/worktree đang được review phải được đối xử read-only;
- scratch hoặc bản sao phục vụ phản chứng phải nằm ngoài repository được review;
- không sửa branch Executor;
- verdict phải neo exact `reviewed_sha` bằng Git OID đầy đủ, khớp head hiện hành;
- khai đúng model, provider, execution surface và transport thực tế;
- không suy model reviewer identity từ tài khoản dùng để đăng verdict lên GitHub.

Phần BẰNG CHỨNG bắt buộc của MỖI finding — thiếu một phần thì đó là *hướng vá bằng lời*,
không phải finding, và người nhận phải tự dựng lại bản vá từ văn xuôi:

- **phép đo**: lệnh đã chạy kèm output thật; không đo được thì ghi `KHÔNG ĐO ĐƯỢC` và vì
  sao — suy luận không thay được số đo, và im lặng không được đọc thành đã đo;
- **phản chứng**: cách tái hiện lỗi trên bản chưa vá, và đột biến làm bản đã vá ĐỎ trở lại;
- **bản vá**: diff áp được — reviewer tự chạy `git apply --check` và ghi mã thoát vào
  verdict — hoặc patch plan đánh số theo từng tệp/dòng khi diff không dựng được, kèm lý do
  chọn đường sau.

Ba gạch trên KHÔNG phải hợp đồng đầy đủ của một finding: hợp đồng gợi ý vá nằm ở
`docs/PROTOCOL_DA_PHIEN.md` §7 và đòi nhiều phần hơn, còn quy tắc đính patch nằm ở §8. Tra
hai mục ấy, đừng suy lại từ đầu và đừng đọc ba gạch này thành danh sách đủ.

### Approver / Land Operator

- chỉ thao tác trên exact SHA đã được ủy quyền bền;
- approval, audit và thao tác land là các vai độc lập;
- merge không tự đồng nghĩa `landed` hoặc Mission `complete`.

## 4. Provider, transport và assurance

Assurance được suy từ cặp Executor–Reviewer, evidence và protocol hiện hành;
không gắn cố định theo tên agent hoặc tên công cụ.

### Google Antigravity

Antigravity có thể làm Executor hoặc Reviewer theo Packet. AG–AG là
same-provider review.

### ChatGPT Pro qua Web

Khi dùng ChatGPT Pro qua Web, phải khai:

```yaml
provider: openai_chatgpt
execution_surface: chatgpt_web
transport: human_mediated
```

ChatGPT Web có thể:

- review một review bundle đóng băng;
- đề xuất finding, test và remediation;
- sinh patch hoặc patch plan cho tác vụ nhỏ.

ChatGPT Web không được:

- trực tiếp ghi repository;
- chạy shell hoặc công cụ cục bộ;
- tự khai đã chạy test;
- commit, push, merge, land hoặc gọi LIVE;
- tự tạo `cross_approved`, `same_provider_approved` hoặc `human_audited`.

Review của ChatGPT Web được ghi là `advisory_review`. Local validator chỉ xác minh
schema, bundle hash và exact SHA; nó không chứng minh model/session identity.

Không khai AG hoặc ChatGPT Web thành Claude/Codex để đi qua state machine.

## 5. Gate và bằng chứng

Chạy đúng gate do Packet Spec, `CLAUDE.md` và phạm vi thay đổi yêu cầu.

Không tự sửa release manifest, golden, workflow, security path hoặc land-only
artifact ngoài write set.

Báo cáo phải ghi:

- exact head SHA và tree hash;
- command;
- mã thoát thật;
- bằng chứng dương;
- `passed`, `failed`, `skipped`, `not_run` tách riêng;
- provider, execution surface và transport;
- môi trường và phần chưa đo được.

Required check bị `skipped`, không được tạo, chạy trên SHA khác hoặc thiếu
positive evidence không được coi là pass. Không chạy hoặc không đo được không
phải là pass.

## 6. Dừng ngay khi

- thiếu hoặc stale Packet/lease/spec/generation;
- head SHA đổi sau review hoặc sau CI; review, gate và authorization cũ đều stale;
- provider hoặc transport khác Packet Spec;
- cần ghi ngoài write set;
- cần secret, LIVE, merge, deploy hoặc authority chưa được cấp;
- reviewer phải sửa branch mới có thể tiếp tục;
- ChatGPT review note không khớp bundle hoặc exact SHA;
- ChatGPT output khai đã chạy test nhưng không có bằng chứng độc lập;
- gate thiếu bằng chứng dương;
- cùng finding lặp đến stop condition;
- tài liệu tại đây mâu thuẫn protocol.

Khi mâu thuẫn, nguồn có thẩm quyền theo loại quyết định thắng file này:
`SKILL.md` cho legal/safety, protocol và Packet Spec cho orchestration,
GitHub facts/verified receipts cho authority, và Git commit/manifest cho
phiên bản cùng tính toàn vẹn.
