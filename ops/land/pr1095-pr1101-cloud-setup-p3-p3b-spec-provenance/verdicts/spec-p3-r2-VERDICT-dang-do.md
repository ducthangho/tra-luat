verdict: pending
reviewed_sha: 37d5965b30462ef2340a26dd19333873e14d84d5
reviewed_tree: 07d9e10b85a25b3c80c81bfd263a28911b0768a3

## DANH TÍNH

Đo đầu lượt ngày 2026-11-02 UTC, tại sandbox hiện hành theo chỉ thị người dùng (bản prompt nằm trong `runs/0426eed0/`).

```text
$ git -C cay-kho rev-parse HEAD 'HEAD^{tree}'
37d5965b30462ef2340a26dd19333873e14d84d5
07d9e10b85a25b3c80c81bfd263a28911b0768a3
$ git -C cay-kho status --porcelain=v1 --ignored
[rỗng; rc 0]
$ sha256sum cay-kho/ops/specs/cloud-setup-p3-writeback-r1.md cay-kho/ops/specs/cloud-setup-p3-writeback-r2.md
e4b0800a197ab22d57b2ee75e11673960c6f47d8e7ace38c20a8aeab99e364d6  cay-kho/ops/specs/cloud-setup-p3-writeback-r1.md
c12e0449511f248de743ab603983c53d0a1c6f83f949bc4c1fa78b03f12bd020  cay-kho/ops/specs/cloud-setup-p3-writeback-r2.md
```

Danh tính và băm r2 khớp. Chỉ chấm r2; r1 dùng đối chiếu errata. Mọi phép đo chỉ dùng nguồn đóng băng và đồ giả cục bộ; không gọi mạng, dịch vụ hay credential thật. Mã sau head/PR #1100 không nằm trong phạm vi.

## ĐO LẠI KHẲNG ĐỊNH

| Khẳng định | Lệnh đo | Kết quả | Khớp/lệch |
| --- | --- | --- | --- |

## FINDINGS

### F01 — P2 — Khẳng định webapp 2p không có action ghi đè nội dung trái mã nguồn

- **Vị trí:** `ops/specs/cloud-setup-p3-writeback-r2.md:35–37`.
- **Mô tả:** câu “không có action nào ghi đè nội dung một tệp có sẵn” sai: `manifest_export` có nhánh cập nhật nội dung tại chỗ bằng `Drive.Files.update({}, _REQ_MANIFEST_ID_, blob, …)` và nhánh `loc.id`; ngoài ra `saveManifest_` cũng cập nhật blob tại chỗ. `upload`/`createtext` tạo mới không đủ chứng minh lời khai bao quát mọi action. Phân biệt quan trọng cho thiết kế là chưa có action CAS dành riêng cho credential, không phải chưa có API cập nhật nội dung.
- **Phép đo tái hiện:** `sed -n '325,331p;1745,1749p;3455,3470p' cay-kho/references/Code.2.21.2p.gs`. Kết quả: dispatcher gọi `doManifestExport_`, hàm này gọi `Drive.Files.update` với blob trên fileId hiện hữu.
- **Đề xuất sửa:** sửa chính đoạn Vấn đề thành “chưa có action CAS cập nhật credential được giới hạn đúng một fileId”; dẫn nhánh cập nhật Drive đã có làm tiền lệ. Kiểm lại bằng truy vết dispatcher tới các lời gọi `Drive.Files.update` có media. Đây chỉ là sửa lời khai/ranh giới action, không mở rộng quyền của action mới; tránh vô tình coi `manifest_export` là đường ghi credential được phép.

### F02 — P2 — Phép nghiệm thu B7 gọi Node trực tiếp với đuôi `.gs` không chạy được

- **Vị trí:** `ops/specs/cloud-setup-p3-writeback-r2.md:157`.
- **Mô tả:** B7 yêu cầu `node --check` trên tệp `Code.2.21.2q.gs` trả 0 nhưng Node từ chối đuôi `.gs` trước bước kiểm JavaScript. Vì vậy tiêu chí nguyên văn đỏ vì loader, kể cả mã GAS hợp lệ; không thể dùng nó làm bằng chứng action đúng/sai.
- **Phép đo tái hiện:** `node --version` ⇒ `v22.23.4`; `node --check cay-kho/references/Code.2.21.2p.gs` ⇒ rc 1, `TypeError [ERR_UNKNOWN_FILE_EXTENSION]: Unknown file extension ".gs"`. Đây là bản 2p mà q phải chép nguyên trước khi thêm action.
- **Đề xuất sửa:** quy định rõ `node --check < references/Code.2.21.2q.gs` hoặc chép nguyên byte sang một tệp `.js` tạm ngoài checkout rồi kiểm tệp ấy. Khoá bằng đối chứng: 2p hợp lệ rc 0, một lỗi cú pháp trong bản sao rc khác 0; cả hai phải thực sự đến bộ phân tích JavaScript. Không thêm `.js` vào write set hoặc sửa bản `.gs` chỉ để chiều loader.

### F03 — P1 — Write set năm tệp không thể đồng thời thêm q vào manifest và giữ G1 xanh

- **Vị trí:** `ops/specs/cloud-setup-p3-writeback-r2.md:49–55`, `:177–181`.
- **Mô tả:** spec bắt buộc thêm `references/Code.2.21.2q.gs` vào gói, tái sinh manifest (J1: số tệp = base + 1), nhưng cấm sửa `scripts/tl_selftest.py`. Hai ca selftest thật `_c291_docs_ngoai_goi` và `_c357_agents_ngoai_goi` đóng cứng số entry manifest ở 197 (`tl_selftest.py:22772`, `:22831`). Manifest hiện có 197 entry; q làm thành 198, khiến cả hai ca đỏ mới, trái G1 “delta = 0”. Đây là lỗi closure L2, không phải executor có thể xử trong năm đường dẫn được cấp.
- **Phép đo tái hiện:** `rg -n 'len\(paths\) == 197|r291_docs_ngoai_goi|r357_agents_ngoai_goi' cay-kho/scripts/tl_selftest.py`; `RELEASE_MANIFEST.json:8` khai `file_count: 197`, danh sách có đúng 197 entry. Hai điều kiện `ok3` nêu trên trả False khi manifest hợp lệ có 198 entry. Trên base lịch sử `4952cff3`, manifest là 195 và ratchet tương ứng vẫn đóng cứng: lỗi tồn tại cả ở nền soạn, không chỉ do master trôi.
- **Đề xuất sửa:** revision mới bổ sung `scripts/tl_selftest.py` vào write set và authority/trần tương ứng, cập nhật có chủ đích cả hai ratchet kèm kê khai slot, rồi tái sinh manifest sau mọi thay đổi. Hoặc chủ kho cắt mục thêm q vào gói bằng thay đổi thiết kế có authority; không được chỉ bỏ G1 hoặc giả định manifest tự sửa ratchet. Phép kiểm đóng: chạy hai hàm nguyên nguồn trên manifest nền và manifest +q, rồi selftest delta phải 0 sau sửa. Bản sửa phải giữ răng ratchet: một entry phát sinh ngoài q vẫn làm đỏ, tránh biến ngưỡng thành số tự đo từ chính manifest.

## TỔNG

P0: 0; P1: 1; P2: 2; P3: 0. Review chưa hoàn tất.
