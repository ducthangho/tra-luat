# VBHN hygiene/source-map guards (v1.17.15)

## Vấn đề từ phiên rà soát 4 luật

Phiên 2026-06-21 phát hiện các lỗi lớp metadata/hygiene:

- Manifest lưu số hiệu VBHN không nhất quán: `19-VPQH`, `40-VPQH`, `14-VBHN-VPQH`.
- Năm ban hành nằm trong tên file kiểu `_2024_`, `_2026_` nhưng parser cũ vẫn có thể coi là thiếu năm.
- `hygiene plan` gom theo số hiệu trần, làm lẫn các VBHN mà VPQH tái sử dụng số ở năm/chủ đề khác nhau.
- Nguồn NLM rỗng metadata có thể được điểm cao chỉ vì có `nlm_source_id`.
- File `.docx/.pdf` gốc nằm cạnh GDoc bị lẫn vào số orphan/quarantine, gây báo động giả.

## Guard đã thêm

- `norm_sohieu()` canonicalize `NN-VPQH` thành `NN-VBHN-VPQH`.
- Parser năm dùng pattern không phụ thuộc word-boundary, đọc được `_2024_`/`_2026_`.
- `_reconcile_clusters()` dùng key an toàn:

```text
VBHN:<số hiệu chuẩn>:<năm/chủ đề/gốc>
```

thay vì chỉ theo số hiệu trần.

- `NLM_GHOST_SOURCE` bị hạ điểm trong `_entry_score()`.
- `sidecar_source_files` được tách khỏi `orphans` và không đưa vào quarantine candidate.
- `hygiene scan --json` có thêm:
  - `sidecar_source_files`
  - `ghost_nlm_sources`
  - `vbhn_reuse_collisions`

## Việc dữ liệu vẫn phải xác nhận

Các thao tác ghi như rename, backfill `issue_year`, move `QUARANTINE`, hoặc đồng bộ tên NLM vẫn phải chờ xác nhận người dùng. Skill chỉ tạo guard để plan không còn đề xuất nguy hiểm.

