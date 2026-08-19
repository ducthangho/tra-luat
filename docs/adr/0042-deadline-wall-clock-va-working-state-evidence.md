# ADR-0042 — Deadline wall-clock và working-state evidence

- **Trạng thái:** Accepted (2026-08-17, thẩm định chung Claude–Codex; chủ kho phê duyệt D1)

Mọi lượt Executor và Reviewer dùng absolute wall-clock deadline fail-closed, profile khởi điểm 90 phút cho
cả hai vai trò. Không đổi timeout sang active-time và không tự sửa power policy. Sau 3–5 run thật, chủ Mission
xem lại profile từ số đo; dispatcher không tự nâng trần.

Launcher chờ theo lát bị chặn và so lại wall clock sau mỗi lát, vì wait timeout trên Windows mới không tính
low-power state. Sổ ghi `wall_elapsed_seconds`, `working_elapsed_seconds`, `working_clock` và
`timeout_clock=wall`. Trên Windows, working-state evidence dùng `QueryUnbiasedInterruptTime` sau khi probe symbol
an toàn; QPC/`time.monotonic()` có tính sleep nên không được gọi là awake clock. Nền chưa có clock đã
đo thì ghi `null/unavailable`, không sao chép kết luận Windows.

W0-M4 chỉ ghi evidence và giữ kill-tree/rc `124/125`; nó không tự động `void-attempt` theo ngưỡng mềm.
Tự động phân loại infrastructure void sau này cần Packet Spec và phản chứng riêng ở seam packet-loop.
Phản chứng W0-M4 tách hai bất biến: wall clock nhảy qua deadline phải timeout+kill tree; working clock
đứng yên trong sleep mô phỏng phải làm wall elapsed lớn hơn working elapsed.
