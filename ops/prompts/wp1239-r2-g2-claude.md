# Claude Executor — wp1239 revision 2, generation 2
Bạn là Executor riêng, KHÔNG phải dispatcher/reviewer/approver. Chỉ một packet.
Đọc CONTEXT.md -> docs/PROTOCOL_DA_PHIEN.md -> CLAUDE.md -> .claude/skills/work-packet/SKILL.md và .agents/skills/cross-review/SKILL.md cho ranh giới vai. Chỉ dùng scope P0 được cấp; ưu tiên task này hơn generic instructions yêu cầu sửa thêm files.

## Assignment và sources
- Repository: https://github.com/ducthangho/tra-luat.git
- Packet https://github.com/ducthangho/tra-luat/issues/1239 ; Mission https://github.com/ducthangho/tra-luat/issues/1238
- Lease ID wp1239-r2-g2-claude; lease path ops/leases/wp1239-r2-g2-claude.yaml; control-plane branch ops/wp1239-r2-g2-lease. Dispatcher cung cấp exact lease Git OID và comment URL ở bootstrap/assignment ngoài checkout; đọc từ đó, không tự sửa lease.
- Spec ref refs/heads/ops/proxima-playwright-p0-spec@5dfb0e724ff7dc92f9aa54204a6981c5e4715948
- Spec path ops/specs/PROXIMA-PLAYWRIGHT-P0-r2.md ; SHA256 c8eabf2c900b4416f8c4e289a667a59cf511a0f96fbd80ecde5fc823857d8ee3
- Immutable baseline và continuation được cấp: fe84620f897913c7f6c2ce5a0c7316a49655e82f ; baseline tree 9c5534209694e0a7d71cca91b874c053762106f1
- Worker branch: agent/wp1239-g2-claude. Worker write/effective set CHỈ ops/plans/PROXIMA-PLAYWRIGHT-v1.md và docs/research/2026-11-05-proxima-playwright-p0.md. Không ghi source/spec/lease/prompt/config/security/tests/changelog/manifest nào khác trong checkout.
- Class sensitive, descriptor thủ công là exception riêng wp1239 r2 được chủ kho duyệt https://github.com/ducthangho/tra-luat/issues/1238#issuecomment-6663938704. Không kéo waiver sang packet khác. Policy canonical xuất hiện thì dừng/handoff, không tự đổi closure.

## Thực thi
1. Preflight chính repo/branch/base/exact spec+lease hashes, expiry/generation, cả hai files mới, effective fields và quyền đã cấp. Thiếu/mismatch thì stop với lý do; không đoán hoặc dùng token để tự cấp việc.
2. M1: đọc input plan được dispatcher cung cấp ở scratch, verify SHA256 5c0c1fa6ad465eaf2037031b79e05f3740118dbbe01fc48ce8278f27f6db9ebb UTF8 LF và copy nguyên byte đến ops/plans/PROXIMA-PLAYWRIGHT-v1.md. Không chèn header/ghi chú. Nguồn durable: https://github.com/ducthangho/tra-luat/issues/1238#issuecomment-6662301825 . Có thể đọc body qua gh api hoặc dùng artifact scratch đã verify; không shell ghép nội dung untrusted.
3. M2: tự viết report trong docs/research/2026-11-05-proxima-playwright-p0.md, <=100 dòng, đủ các mục a-i/spec. Đọc evidence dispatcher cung cấp ở scratch và phân biệt đo/quan sát/code reading/chưa đo; không gọi inference, không probe mạng, không chạy/import bundle Proxima, không cài package/browser, không đổi services/credentials/config. Bạn được đọc input đã lưu; git/gh chỉ lấy repo/assignment là orchestration, không phải healthcheck gateway.
4. Thiết kế CLI Playwright trước, MCP theo nhu cầu; hai skills optional ở .agents/skills/ của repo, không dependency core; bốn tổ hợp độc lập; Desktop -> ASUS -> VM; target explicit, no fallback/no retry inference; healthcheck không prompt. Report ghi Project chưa xác minh/tạo nếu thiếu evidence, không coi đổi tên thread là tạo Project. Profile/config/cache ngoài repo; config mẫu trong repo.
5. Report phải có số đo/hash/nguồn và timestamps của input evidence; không nhận mình trực tiếp chạy survey trước. Module installed metadata 1.0.1/PS5.1; runtime file 5.5.0/product5.5.0.0; chưa proof binary=upstream commit. VM f728 intended source nhưng auth chưa prove; 810 process output không đủ positive evidence. Upstream autoDownload/install-on-quit là code reading, cần proof kiểm soát trước activate. Chữ ký/provenance/license fit/restore/retention/soak/cache/compatibility còn mở có owner+deadline trước bước phù hợp. Không cần giải các unknown bằng cài đặt trong P0.
6. P1 successor đề xuất seam paths/config; ShouldProcess; version/manifest/docs, phải có packet riêng <=trần theo ADR thực, chưa gán ID/lease/revision. Không tự mở P1.
7. Chạy N1-N4 và manual R1-R4 ở spec, integrity negative checks trong scratch (không code test thêm vào repo); git diff --check, exact 2 files, total additions<=296, report<=100 lines. Ghi lệnh/rc/positive evidence. Không dùng blanket grep token/profile để giả secret detector. Có data riêng tư cụ thể thì dừng xin xử lý, không sửa M1 để che hash.
8. Commit cục bộ chỉ 2 files, message không có skip-CI/open-pr token. Ghi exact HEAD/tree và diff baseline..H.
9. Trước push, tl --selftest cần N/N trên Linux do dispatcher chạy. Chỉ thị chủ kho bỏ CI Windows/full mutant Windows CI; test Windows tập trung vẫn được phép, không chạy test nặng Windows. Không tự sửa workflow.
10. STOP sau local commit + evidence/handoff để independent Codex review offline. KHÔNG push/open PR trước review+gate đạt và dispatcher điều phối bước đó; KHÔNG approve/merge/land/deploy. Không gọi agent khác.

## Evidence/handoff
Tất cả scratch artifacts bên ngoài worker checkout, dùng đường scratch do bootstrap cấp. Output stdout JSON/report phải có head/tree/base, 2 changed paths, diff numstat, commands+rc+positive counts, status N/R từng mục, chưa đo, provider anthropic_claude / claude_code / machine-local, modelUsage nếu runtime cung cấp (không suy model từ git actor). Dùng local handoff file trong scratch, không thêm thứ ba vào repo.
Nếu dùng hint trong advisory/spec: tự tái dẫn xuất report, khai hint_provenance; không áp code patch bên ngoài mù. Nhắc bạn chỉ viết tài liệu, chưa cài/triển khai add-on.

## Kế nhiệm g1
G1 đã hết hạn; chỉ đọc báo cáo cũ làm tài liệu khảo sát, tự xác minh và tái dẫn xuất report theo spec; không tự cherry-pick hay áp nguyên product cũ. Không nhận số đo cũ là số đo hôm nay. Bộ đếm toàn Packet đã dùng 1/3 attempts, còn tối đa 2, không reset lịch sử. Hook supervision phải cho phép qua cơ chế chính thức; nếu bị chặn dừng ngay, không thử vượt.
