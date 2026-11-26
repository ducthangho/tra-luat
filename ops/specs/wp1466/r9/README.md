# wp1466 r9: hồ sơ dựng đặc tả

Đặc tả r9 được dựng MÁY từ r8 (`ops/specs/wp1466.md` blob `a9de826`, sha256 `98790505…0834`). Các bước:

1. `dung_r9.py.txt <r8> <buoc1>` bỏ backtick quanh 18 con trỏ `ca:` của khối `p2-moi` và thêm câu luật vào đoạn dẫn.
2. `proto_r9.py.txt <r8> <buoc1> <protocol tại 96e4472> <ra>` thay §1.1 của protocol tại H lượt 1 bằng khối `p2-moi` r9, rồi băm `K01`.
   Kiểm chứng: cùng script cho lại băm `607431f2…0531` của r8 trên protocol tại H.
3. `dung_r9_b2.py.txt <buoc1> <r9> <băm K01>` thay băm trong khối `khoa` và thêm các đoạn văn của r9 (đầu tệp, mục 0, mục 8.3, mục 19).

Phép đo trên H lượt 1 (`96e4472`) cộng protocol r9 cộng băm `K01` mới trong `INV_KHOA_PROTOCOL`:
- `doc-claims-check --strict` rc 0, xem `doc-claims-H-cong-r9.json`;
- `doctrine-scan` rc 0; `adr-song` rc 0;
- `khoa_doc_lap.py` của executor: N5 đạt 7/7.

Trên H lượt 1 chưa vá, cùng lệnh `doc-claims-check` cho rc 2, 395 cờ.
