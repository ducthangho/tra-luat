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
5. `SKILL.md` — bắt buộc khi Packet liên quan pháp luật, corpus, Drive,
   NotebookLM, registry hoặc hành vi runtime của skill.

Đọc được kế hoạch không đồng nghĩa được giao việc. Không có Packet Spec hoặc
authority được protocol hiện hành thừa nhận thì dừng.

## 2. Preflight bắt buộc

Trước khi sửa:

- xác minh đúng repository, branch/worktree và exact base Git OID;
- xác minh Packet revision/spec hash/generation;
- xác minh effective write set;
- xác minh Review Class và capability cần thiết;
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
- khai đúng model/provider thực tế và mức assurance;
- không suy model reviewer identity từ tài khoản dùng để đăng verdict lên GitHub.

### Approver / Land Operator

- chỉ thao tác trên exact SHA đã được ủy quyền bền;
- approval, audit và thao tác land là các vai độc lập;
- merge không tự đồng nghĩa `landed` hoặc Mission `complete`.

## 4. Provider và assurance

Assurance được suy từ cặp Executor–Reviewer và protocol hiện hành, không gắn
cố định theo tên agent.

Antigravity có thể làm Executor hoặc Reviewer theo Packet. AG–AG là
same-provider review. Không khai AG thành Claude/Codex và không ghi
`cross_approved` nếu provider registry, runtime hoặc receipt hiện hành chưa
hỗ trợ bằng chứng đó.

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
- môi trường và phần chưa đo được.

Required check bị `skipped`, không được tạo, chạy trên SHA khác hoặc thiếu
positive evidence không được coi là pass. Không chạy hoặc không đo được không
phải là pass.

## 6. Dừng ngay khi

- thiếu hoặc stale Packet/lease/spec/generation;
- head SHA đổi sau review hoặc sau CI; review, gate và authorization cũ đều stale;
- cần ghi ngoài write set;
- cần secret, LIVE, merge, deploy hoặc authority chưa được cấp;
- reviewer phải sửa branch mới có thể tiếp tục;
- gate thiếu bằng chứng dương;
- cùng finding lặp đến stop condition;
- tài liệu tại đây mâu thuẫn protocol.

Khi mâu thuẫn, nguồn có thẩm quyền theo loại quyết định thắng file này:
`SKILL.md` cho legal/safety, protocol và Packet Spec cho orchestration,
GitHub facts/verified receipts cho authority, và Git commit/manifest cho
phiên bản cùng tính toàn vẹn.
