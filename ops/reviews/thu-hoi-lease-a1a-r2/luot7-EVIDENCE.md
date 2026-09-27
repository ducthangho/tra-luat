# EVIDENCE lượt 7 — lời khai của phiên soạn, KHÔNG phải phép đo của reviewer

## E20. Xử lý lượt 6 (bản nháp 7, commit `7fc28680`)
- Áp `luot6-HINT.patch` nguyên hunk (F16); băm SPEC ngay sau áp = `f8c0d3fb…`, khớp băm bạn khai. Sau đó cập nhật header/§8.2.
- Đột biến bạn tự soạn ở lượt 6 và thấy **sống** ("bỏ qua im lặng các tệp hạn hợp lệ năm 1/9999", vì tệp biên nằm ngoài cặp):
  · tách ca thành `han-bien-tren-hop-le` (đầu mới y hạn `9999-12-31T23:59:59Z` ⇒ rc0, giữ `(x,y)`) và `han-bien-duoi-hop-le`
    (đầu mới y hạn `0001-01-01T00:00:00Z` ⇒ rc0, `()`); vòng tự kiểm nhận phần tử thứ 4 tuỳ chọn = số `lease_hop_le` mong đợi,
    hai ca biên đòi **2**;
  · thêm mutant `bo-qua-im-lang-tep-han-bien` với tập đích hai ca biên; mutant `tu-choi-nam-bien` đổi tập đích sang hai ca mới.
- Lần đo đầu ma trận LỆCH: "bỏ lọc hạn" giết thêm `han-bien-duoi-hop-le` (hạn năm 1 lẽ ra bị loại) — hành vi đúng ⇒ mở rộng tập khai.
- Bản in: `--tu-kiem` 31/31; `mut_q6.py` 21/21 KHOP + gốc, 0 Traceback; kho thật byte-equal JSON.
- `do_q6.py` sha256 `36d8f166…`, `mut_q6.py` sha256 `272dc1e8…`.

## E21. CI của PR #652 vẫn đỏ vì billing (không liên quan diff; comment `5851263851`).
