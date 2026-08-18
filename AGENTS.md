# tra-luat — Agent Entry Point

> File này chỉ là CON TRỎ. Không định nghĩa lại protocol, legal doctrine,
> review budget, schema hay release gate.

## 1. Đọc trước khi làm việc

Theo thứ tự:

1. `CONTEXT.md` — từ vựng chung.
2. `docs/PROTOCOL_DA_PHIEN.md` — vai trò, state, review, handoff và stop condition.
3. `CLAUDE.md` — quy tắc phát triển, test và deploy của repository.
4. Packet Issue/Spec hiện hành — objective, generation, base SHA, write set,
   acceptance, risk và authority.
5. `SKILL.md` — bắt buộc khi Packet liên quan pháp luật, corpus, Drive,
   NotebookLM, registry hoặc hành vi runtime của skill.

Đọc được kế hoạch không đồng nghĩa được giao việc. Không có Packet/authority
hợp lệ thì dừng.

## 2. Preflight bắt buộc

Trước khi sửa:

- xác minh repository, branch/worktree và exact base SHA;
- xác minh Packet revision/spec hash/generation;
- xác minh effective write set;
- xác minh Review Class và capability cần thiết;
- giữ worktree sạch ngoài thay đổi thuộc Packet.

Lệch một điều kiện trên thì không tự sửa cho khớp; báo người điều phối.

## 3. Ranh giới vai trò

### Executor

- chỉ ghi trong effective write set;
- không tự review, approve, merge, land, deploy hoặc gọi LIVE;
- không tự cấp lease hoặc mở rộng Packet;
- tạo handoff neo exact head/tree và bằng chứng test.

### Reviewer

- dùng session/context và checkout độc lập;
- repository được review là read-only;
- scratch hoặc bản sao phản chứng phải nằm ngoài repository;
- không sửa branch Executor;
- verdict phải neo exact `reviewed_sha`;
- khai đúng provider và mức assurance thực tế.

### Approver / Land Operator

- chỉ thao tác trên exact SHA đã được ủy quyền bền;
- approval, audit và thao tác land là các vai độc lập;
- merge không tự đồng nghĩa `landed` hoặc Mission `complete`.

## 4. Provider và assurance

Assurance được suy từ cặp Executor–Reviewer và protocol hiện hành, không gắn
cố định theo tên agent.

Antigravity có thể làm Executor hoặc Reviewer theo Packet. AG–AG là
same-provider review. Không khai AG thành Claude/Codex và không ghi
`cross_approved` nếu runtime/receipt hiện hành chưa hỗ trợ bằng chứng đó.

## 5. Gate và bằng chứng

Chạy đúng gate do Packet Spec, `CLAUDE.md` và phạm vi thay đổi yêu cầu.

Không tự sửa release manifest, golden, workflow, security path hoặc land-only
artifact ngoài write set.

Báo cáo phải ghi:

- exact SHA/tree;
- command;
- mã thoát thật;
- bằng chứng dương;
- passed/failed/skipped/not_run tách riêng;
- môi trường và phần chưa đo được.

Không chạy hoặc không đo được không phải là pass.

## 6. Dừng ngay khi

- thiếu hoặc stale Packet/lease/spec/generation;
- head SHA đổi sau review;
- cần ghi ngoài write set;
- cần secret, LIVE, merge, deploy hoặc authority chưa được cấp;
- reviewer phải sửa branch mới có thể tiếp tục;
- gate thiếu bằng chứng dương;
- cùng finding lặp đến stop condition;
- tài liệu tại đây mâu thuẫn protocol.

Khi mâu thuẫn, `docs/PROTOCOL_DA_PHIEN.md`, Packet Spec và các nguồn authority
theo loại quyết định thắng file này.
