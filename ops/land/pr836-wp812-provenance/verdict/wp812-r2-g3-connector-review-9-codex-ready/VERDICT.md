Reviewed commit: f4ab8b6cec07d2ce0d68b9efab660c73ca364395
Verdict: changes_requested — P0=0 P1=0 P2=3 P3=0

Nguồn: connector `chatgpt-codex-connector[bot]`, review 5564252087 trên PR #836, kích hoạt tự động "Draft marked ready"
(ngoài trần 8 lời gọi — không do executor gọi). Bản chép; thẩm quyền là review trên GitHub.

| slug (executor gán lớp) | hạng | comment | biểu hiện |
|---|---|---|---|
| lease-holder-scope-incomplete | P2 | 4308158588 (pl:2482) | phân giải symlink theo `--root` của người gọi, không theo snapshot lease ⇒ chồng lấn qua symlink chỉ có trong ref lease lọt rc=0 |
| findings-not-receipt-bound | P2 | 4308158580 (pl:2695) | `finding_counts` đếm theo `--finding-id` người gọi khai (tập con của bảng) ⇒ bỏ lớp tái diễn để né same-failure |
| identity-compared-by-provider-family | P2 | 4308158585 (pl:2618) | surface/transport để trống ở init là wildcard, record-lease không điền từ lease ⇒ runtime khai surface khác lease vẫn rc=0 |
