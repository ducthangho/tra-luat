# ADR-0019 — Ba skill, hai adapter, một protocol

- **Trạng thái:** Accepted (2026-08-03, phiên grilling)

Điều phối đa phiên dùng ba skill theo ranh giới invocation: `work-packet` và `cross-review` là model-invoked để
executor/reviewer tự vào đúng quy trình; `land-packets` là user-invoked vì prepare/apply cần chủ ý của người
dùng. `land-packets` chỉ là client local của operation `land apply` trong control plane; comment GitHub và
workflow dispatch là client tương đương để Android không phụ thuộc một skill hay Windows host. Nguồn sự thật
duy nhất là `docs/PROTOCOL_DA_PHIEN.md`; adapter mỏng trong `.claude/skills/` và
`planned:.agents/skills/` chỉ nối từng sản phẩm tới protocol, còn `CLAUDE.md`/`AGENTS.md` giữ chỉ dẫn bắt buộc tối thiểu.
CI kiểm parity các adapter. Cách này chấp nhận một ít scaffolding theo sản phẩm để tránh chép đôi quy trình và
giữ quyền land khỏi tự động kích hoạt; mọi client đều phải cung cấp cùng mission/head SHA và qua cùng gate/audit.
