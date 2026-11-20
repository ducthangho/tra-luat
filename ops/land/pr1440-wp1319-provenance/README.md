# Provenance land — PR #1440, merge `d8cf2ab57f9f25a93cefedcebfb315826b6b78fe`

Làn lưu trữ ADR-0060 (M8). Đây là các tệp mà biên bản M8 của #1319 (`../wp1319-m8/m8-1319.yaml`, khoá
`moc_10_2_2_nguon`) trỏ tới bằng băm, và trước đây chỉ nằm trong thư mục làm việc của phiên điều phối.
Tệp chép nguyên byte; không tạo hồ sơ `*-land-evidence.yaml` mới — biên bản M8 trên Issue là điểm cuối.

| tệp | vai trò | sha256 (đầu) |
|---|---|---|
| `ci-provenance-44669622916/provenance.yaml` | đầu ra `ops/ci_provenance.py thu --repo ducthangho/tra-luat --run 44669622916 --attempt 1 --wd-run 44672185539` (rc 0); mốc run / checkout / workflow_definition | d749903c0613a112 |
| `ci-provenance-44669622916/run.json`, `jobs.json`, `jobs/*.trich.txt` | dữ liệu thô bộ thu ghi kèm | |
| `danh_gia_gate.py` | bộ đánh giá mốc Gate output v3, giống byte `../pr1378-wp1319-provenance/danh_gia_gate.py` | 0ea9a5e9… |
| `danh-gia-gate-output-44669622916.txt` | `python3 -I danh_gia_gate.py 44669622916 <out>`: `MOC_GATE_OUTPUT passed`, 39/39 job | 452024d7e9bd5d58 |

Run 44669622916 là `ci.yml` push master trên `d8cf2ab`; run 44672185539 là `ops-do-workflow-definition.yml`.
