```text
verdict: approve
reviewed_sha: a5305449893109a62fe04f9a7f4ae2d7fd27534e
dem: P0=0 P1=0 P2=0 P3=0
```

Approve đặc tả. Không phát hiện lỗi mới. Tree: `745b92a16d5a9bbfc8c80a269e759a9fa2a32388`. Reviewer: `openai_codex / codex_cli / machine`.

| Finding cũ | Kết luận đo lại |
|---|---|
| S822-01 | **ĐÃ ĐÓNG**: M3 tách ba dạng ca; bỏ khử trùng làm số lần xuất hiện đổi 1→2 dù rc vẫn 0. |
| S822-02 | **ĐÃ ĐÓNG**: M1/A5 cùng đòi bảo toàn rc/stdout/stderr; bỏ K06 đổi lý do và làm `kg_n5_thieu` đỏ. |
| S822-03 | **ĐÃ ĐÓNG**: prototype trong bản sao tệp test loại tín dụng cho crash F02, nhận mutant xanh giả; gỡ loại crash làm tự kiểm đỏ. |
| S822-04 | **ĐÃ ĐÓNG**: hai câu đã sửa đúng phạm vi A11: 106 ca gọi gate, giữ cả hai ca codepage. |

| Lời khai | Kết quả |
|---|---|
| Nền | 100/100 `_KG_CA`; 104/104 họ kg; 106/106 tập A11 |
| D1/K18 | Neo đúng 1 chỗ; đỏ 0/100, 0/104, 0/106 |
| D2/K35 | Neo đúng 1 chỗ; đỏ 0/100, 0/104, 0/106 |
| D3/K10 | Neo đúng 1 chỗ; đỏ 0/100, 0/104, 0/106 |
| D4/K11 | Neo đúng 1 chỗ; đỏ 0/100, 0/104, 0/106 |
| D5/K12 | Neo đúng 1 chỗ; đỏ 0/100, 0/104, 0/106 |
| D6/K13 | Neo đúng 1 chỗ; đỏ 0/100, 0/104, 0/106 |
| Sáu fixture A2 | Cả sáu: nền rc=12 đúng lý do → mutant rc=0, không traceback |
| A3 | Nền: thiếu `conclusion`; D6: `THỪA id`; cả hai rc=12 |
| K37: thiếu / null / sai kiểu | Lần lượt 12→0 / 0→0 / 12→12 |
| Kiểm kê / tổng CASES | 37 ID K; 406 ca, trong đó 106 thuộc A11 |
| Doctrine / ADR | **passed**, rc=0 |
| Bare Ruff | **failed** sẵn trên base/head; delta=0 |

Các probe hoàn tất với rc=0. Không ca skipped trong tập 106; toàn suite, CI và LIVE **not_run**. Authority GitHub/lease và eligibility trần 8/450 **chưa đo đủ** trong lượt offline.

Checkout giữ nguyên HEAD/tree, index và bytes của 3.764 tệp.

Đã lưu [verdict đầy đủ và bằng chứng](/tmp/wp822-review-r4-e25b2759/VERDICT.md), gồm command, rc, output và manifest hash.