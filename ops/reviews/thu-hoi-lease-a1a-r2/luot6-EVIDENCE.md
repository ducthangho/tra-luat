# EVIDENCE lượt 6 — lời khai của phiên soạn, KHÔNG phải phép đo của reviewer

## E18. Xử lý lượt 5 (bản nháp 6, commit `635e9a23`)
- Áp `luot5-HINT.patch` nguyên hunk (F15, §8.3); băm SPEC ngay sau áp = `f7df1cd5…`, khớp băm bạn khai. Sau đó cập nhật header/§8.2.
- Hai đột biến bạn tự soạn ở lượt 5 và thấy **sống** trên bộ 29 ca:
  · "từ chối mọi hạn năm 1 hoặc 9999" ⇒ thêm ca `han-bien-hop-le` (z hạn `9999-12-31T23:59:59Z`, w hạn `0001-01-01T00:00:00Z`,
    kỳ vọng rc0, giữ `(x,y)`) và mutant `tu-choi-nam-bien` với tập đích `{han-bien-hop-le}`;
  · "bỏ riêng chốt thư mục con" ⇒ không có ca nào phân biệt được vì chốt tên luôn che (`sub/z` ≠ `z`, `LEASE_ID` cấm `/`);
    khai mutant `bo-rieng-chot-thu-muc-con` với tập đích **rỗng** có chủ đích, và nêu lý do trong bảng §8.2.
- Bản in: `--tu-kiem` 30/30; `mut_q6.py` 20/20 KHOP + gốc, 0 Traceback, `TAT_CA_KHOP`; kho thật byte-equal JSON (`cmp` rc0).
- `do_q6.py` sha256 `7fd77bc6…`, `mut_q6.py` sha256 `71b1fbb5…`.

## E19. CI của PR #652 đang đỏ vì **billing** (không liên quan diff)
Từ 00:22:59Z mọi workflow run của kho bị GitHub từ chối khởi động: annotation *"The job was not started because recent account
payments have failed or your spending limit needs to be increased"*, job 0 bước ~2 s. Đã ghi comment `5851263851` trên PR. Không
thuộc phạm vi review đặc tả; nêu ra để bạn không đọc nhầm thành hồi quy.
