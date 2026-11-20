# WP1319 r10 — Quyết định của chủ kho cho các hàng nghiệm thu còn dở

**Căn cứ:** đặc tả `ops/specs/wp1319-r10.md`, lease `ops/leases/wp1319-r10-g1-operator.yaml`. Không chạy gì trên host.

## 1. Trao đổi trong phiên điều phối (20/11)
- Chủ kho hỏi: *"Theo kế hoạch thì còn nhiệm vụ gì của Mission này không"*.
- Phiên điều phối trả lời:
  - Mission #1238 đã đóng. Còn packet #1319, với 6 WP con đã đóng.
  - Liệt kê ba việc:
    1. các hàng MATRIX còn dở cần chủ kho quyết;
    2. review độc lập cuối, xin cấp 1–2 lời gọi Codex;
    3. biên bản M8 và đóng #1319.
  - Kiến nghị cho mục 1: *"phần lớn hàng có thể miễn như U11, vì kiến trúc thực tế hẹp hơn kế hoạch ban đầu"*.
- Chủ kho trả lời: **"1,2,3 đồng ý các kiến nghị. Xử lý tiếp"**.

Tất cả là lời khai của phiên điều phối về trao đổi trong phiên, không có bản ghi trên GitHub.

## 2. Cách hiểu được ghi lại
- Mỗi hàng còn dở được **miễn** (`owner_waived`) hoặc **chấp nhận** (`owner_accepted`) theo hướng không đo thêm và không đổi hạ tầng.
- Dữ kiện đo **giữ nguyên** trong MATRIX.
- Không hàng nào được nâng lên `passed`.
- Nếu chủ kho muốn khác ở hàng nào, sửa bằng một revision mới; bản ghi này không tự mở rộng quyết định.

| Hàng | Dữ kiện giữ nguyên | Ghi |
|---|---|---|
| §11 #2 (đích từ xa / gateway thật) | partial; đường WinRM từ xa chưa mở (r9) | `owner_waived` |
| §11 #3 (WhatIf trên gateway thật) | passed scoped, backend giả | gateway thật: `owner_waived` |
| U1 (endpoint Proxima thật trên PS5.1) | passed scoped, backend giả | endpoint thật: `owner_waived` |
| §11 #5 F1 (dư lượng `ms-playwright\daemon`) | đo được ở P3 (18 tệp, 7 759 byte ở r6) | `owner_accepted`: giữ nguyên, không dọn |
| §11 #9 (phục hồi binary) | partial: chỉ đổi sang thư mục baseline đặt song song | vế binary: `owner_waived` |
| U4 (updater, các nhánh ngoài sai integrity) | chỉ đo nhánh sai integrity | phần còn lại: `owner_waived` |
| U7 (retention, soak, theo dõi) | partial: ngưỡng, owner, cửa sổ chưa ghi | `owner_waived`: không đặt |
| U8 (vế đăng nhập) | quan sát của chủ kho: phiên giữ được | `owner_accepted`; không có PASS/FAIL |
| Kiểm release hằng ngày | not_present trên 3 máy | `owner_accepted`: kiểm tay, không cài tác vụ lập lịch |
| Migration / nâng cấp / per-machine | not_evidenced | `owner_waived` |

## 3. Trạng thái sau r10
- Mọi hàng ở MATRIX mục I đã có kết quả đo hoặc quyết định của chủ kho:
  - quyết định r7: U5/U12, §11 #10;
  - quyết định r9: U11;
  - quyết định r10: các hàng ở bảng trên;
  - giữ nguyên từ trước: §11 #7 "updater trùng" (đã chấp nhận) và "NSIS gỡ của nhà cung cấp" (`failed`, finding sản phẩm NSIS-2).
- Việc còn lại của #1319:
  - review độc lập cuối trên hồ sơ đóng băng (chủ kho cấp tối đa 2 lời gọi Codex);
  - biên bản M8 rồi đóng Issue.
- Thu hồi lease đã merge mà còn hạn: `wp1319-r8-g1-operator` (PR #1435) và `wp1319-r9-g1-operator` (PR #1437).
