# FULL-GATE PR #468 — chạy MỘT lần, 2026-09-07

Chủ kho ràng buộc: *"đừng chạy gate dài hoặc CI cho đến khi ít nhất là không còn P1.
Chỉ chạy full-gate 1 lần ở cuối"*. Đây là lần chạy duy nhất ấy.

Neo: nền `b416830ef2a509d60203d55552ce17950afcf67c` (origin/master) ·
sau `f77f19895e00835d71644d82f1c54e9b519ccfe6`.

## CÁCH TRÍCH SỐ (khai theo P3 `evidence-thieu-phuong-phap-trich-va-gioi-han-bao-phu`)

Mọi số dưới đây lấy từ tệp trong chính thư mục này, không chép tay:

| số | trích bằng | loại nguồn |
|---|---|---|
| `rc` từng bộ | trường thứ 2 của `nen.rc` / `sau.rc` | **đo lại được** — chạy `fullgate.sh` |
| `out_byte` | `wc -c` trên stdout mỗi bộ, ghi sẵn trong `*.rc` | **đo lại được** |
| số giây | `date +%s` trước/sau mỗi bộ | **đo lại được**, nhiễu ±5 s |
| `51/51`, `TỔNG: ĐẠT` | `tail -5` stdout, lưu ở `*.tail.txt` | **đo lại được** |
| `31 đột biến, 0 cái ĐỎ=[]` | `grep -c 'đột biến'` và `grep -c 'ĐỎ=\[\]'` trên `*.lease.norm.out` | **đo lại được** |
| `50/50 dòng` sau chuẩn hoá | `diff` hai tệp `*.lease.norm.out` | **đo lại được** |

Bộ lọc và phần bỏ sót — nêu để không ai tưởng bảng này phủ hết:

- `*.lease.norm.out` đã **chuẩn hoá** tên thư mục tạm bằng `sed -E 's/lp_[a-z0-9_]+/LP/g'`.
  Bản thô KHÔNG được kèm; muốn đối chiếu byte gốc phải chạy lại.
- `cidk` và `ploop` chỉ giữ **5 dòng cuối**, không phải toàn bộ stdout. Dòng lỗi nằm giữa
  stdout (nếu có) sẽ KHÔNG thấy ở đây.
- `doctrine-scan` và `adr-song` chỉ có `rc` và kích thước (69 B / 113 B), không kèm nội dung.
- Bảng này chỉ phủ **6 bộ** đã chạy. Nó KHÔNG phủ CI trên GitHub Actions.

## KẾT QUẢ

| bộ | nền `rc` | sau `rc` | out | bằng chứng dương |
|---|---:|---:|---:|---|
| `cidk` | 0 | 0 | 2934 B | `51/51 đỏ đúng · TỔNG: ĐẠT` |
| `ploop` | 0 | 0 | 8752 B | `TỔNG: ĐẠT` |
| `lease` | **1** | **1** | 8971 B | 31 đột biến, **0** cái có `ĐỎ=[]` |
| `doctrine-scan` | 0 | 0 | 69 B | — |
| `adr-song` | 0 | 0 | 113 B | — |
| `doc-claims-check` | 0 | 0 | 70861 B | — |

**DELTA = 0.** Khác duy nhất là số giây và tên thư mục tạm ngẫu nhiên. Chuẩn hoá xong,
`nen.lease.norm.out` và `sau.lease.norm.out` giống hệt từng byte, **50/50 dòng**.

**Không bộ nào `out=0B`.** Đây là phép kiểm có chủ đích: một lần chạy full-gate trước đó đã
XANH GIẢ vì script bọc mỗi bộ trong `/usr/bin/time` vốn không tồn tại — cả sáu bộ `rc=127`,
chưa hề chạy, mà so sánh delta vẫn in *"khớp từng dòng"* do `rc` khớp ở cả hai vế. Thứ bắt
được nó là kích thước output, không phải mã thoát.

## `lease rc=1` — KHÔNG tính là xanh

`t33_workflow_dang_lease_phai_qua_actionlint` trả `KHÔNG ĐO ĐƯỢC: thiếu actionlint`.
Container không cài `actionlint` (`command -v actionlint` không thấy). Đây là **fail-close
đúng** cho công cụ vắng mặt, **giống hệt hai vế**, KHÔNG phải hồi quy do các commit của PR.

Hệ quả phải ghi thẳng: **ca `t33` chưa từng được đo trong lần gate này.** Nó không đỏ, cũng
không xanh — nó không chạy. Ai muốn đóng nó phải cài `actionlint` rồi chạy lại.

## Điều bản ghi này KHÔNG chứng minh

- Không chứng minh CI trên GitHub Actions xanh. Bộ công cụ GitHub của phiên chỉ có **44 tool**,
  không có nhóm workflow/actions, nên trạng thái check của PR **KHÔNG ĐO ĐƯỢC** từ đây.
  Chỉ đọc được `mergeable_state=unstable` và `get_status` rỗng (`total_count=0`) — đó là API
  status cũ, không phải check run của Actions.
- Không phải merge authorization.
