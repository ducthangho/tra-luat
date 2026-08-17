# Vòng 5 — hiệu chính clock semantics rồi đóng phiên

Tiếp tục cùng session read-only. Codex đồng ý D1 `90/90` và D2 allowlist 11 receipt v1. Tuy nhiên,
trước khi ghi biên bản, Codex đã kiểm nguồn chính thức và thấy cần hiệu chính một chi tiết:

1. Microsoft `WaitForSingleObject`: từ Windows 8, timeout **không** tính low-power state.
   <https://learn.microsoft.com/en-us/windows/win32/api/synchapi/nf-synchapi-waitforsingleobject>
2. Microsoft `Acquiring high-resolution time stamps`: `QueryPerformanceCounter` **có** tính standby/hibernate/
   connected standby.
   <https://learn.microsoft.com/en-us/windows/win32/sysinfo/acquiring-high-resolution-time-stamps>
3. Microsoft `Windows Time`: `QueryUnbiasedInterruptTime` chỉ tính thời gian system ở working state.
   <https://learn.microsoft.com/en-us/windows/win32/sysinfo/windows-time>
4. Đo ngay trong environment: `time.get_clock_info('monotonic').implementation ==
   'QueryPerformanceCounter()'`.

Vì vậy `time.monotonic()` trên Windows **không phải awake/active clock**. Nếu W0-M4 ghi `active_elapsed`
bằng monotonic thì con số có tên đúng nhưng đo sai hiện tượng.

## Hiệu chính Codex đề nghị

- D1 vẫn là absolute wall-clock fail-closed, deadline `90/90`, không đụng power policy.
- W0-M4 ghi:
  - `wall_elapsed_seconds` từ UTC wall clock;
  - `working_elapsed_seconds` và `working_clock`;
  - trên Windows, `working_clock=QueryUnbiasedInterruptTime`; không dùng QPC/`time.monotonic()` để
    tuyên bố thời gian thức;
  - nếu platform không có working-state clock đã kiểm chứng, ghi `null/unavailable`, không suy đoán.
- W0-M4 chỉ cung cấp bằng chứng. Không tự động `void-attempt` theo một ngưỡng `active_elapsed`
  mơ hồ trong packet này. Có thể dùng lệnh `void-attempt` hiện có sau khi bằng chứng cho thấy lỗi hạ
  tầng; nếu sau này muốn tự động hóa thì phải có Packet Spec + phản chứng riêng.
- Phản chứng W0-M4 phải tách hai bất biến:
  1. wall clock nhảy qua deadline trong khi process còn sống ⇒ timeout + kill tree;
  2. fake working clock không nhảy trong khoảng sleep mô phỏng ⇒ `wall_elapsed > working_elapsed`, không đánh
     đồng hai clock.

## Yêu cầu kết luận

1. Verdict `AGREE | AGREE_WITH_CHANGE | DISAGREE` cho hiệu chính này.
2. Nếu agree, trả lại **bản khuyến nghị chung cuối cùng** ngắn gọn: lane, bundle A–G, D1, D2,
   owner approvals.
3. Nêu rõ không còn dissent và kết thúc sau vòng 5.

Không sửa file.
