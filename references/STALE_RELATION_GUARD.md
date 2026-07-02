# Stale relation guard — sửa đổi đã có nhưng registry chưa nối quan hệ (v1.17.24)

## Vấn đề

Log Thi đua, khen thưởng cho thấy một lỗi vận hành nghiêm trọng: `vb_status`/`source-map` có thể báo "chưa có sửa đổi/VBHN" khi registry thiếu trường quan hệ, dù văn bản sửa đổi đã nằm trong corpus và đã có `nlm_source_id`.

Ví dụ:

- Luật gốc `06/2022/QH15` để trống `sua_doi`.
- Luật sửa đổi `06/2026/QH16` đã có trong thư mục chủ đề/NLM nhưng để trống `goc`.
- Vì thiếu liên kết hai chiều, công cụ theo quan hệ trả thiếu và người rà soát có thể dùng nhầm bản gốc đơn lẻ.

## Quy tắc bắt buộc

Khi phát hiện một văn bản đã bị sửa đổi, hết hiệu lực một phần, hoặc nghi có VBHN mới:

1. Dừng rà soát nội dung trên bản cũ.
2. Chạy ngay `tl exists`/`tl source-map` và `tl relation-check`, không đưa vào mục xử lý sau.
3. Nếu relation-check thấy văn bản sửa đổi đã có trong corpus/NLM nhưng thiếu `goc/sua_doi`, hỏi người dùng xác nhận ghi registry ngay.
4. Nếu chưa thấy VBHN trong corpus, không kết luận không có; chạy web search QT-5 theo trích yếu + "hợp nhất".
5. Chỉ tiếp tục rà soát sau khi đã chốt nguồn: VBHN chính thức nếu có; nếu chưa có VBHN thì dùng bản gốc + bản sửa đổi đã liên kết.

## Lệnh chuẩn

```bash
python scripts/tl.py exists "06/2022/QH15" --json
python scripts/tl.py source-map "06/2022/QH15" --json
python scripts/tl.py relation-check \
  --base "06/2022/QH15" \
  --subject "thi đua khen thưởng" \
  --amendment "06/2026/QH16" \
  --json
```

Nếu thiếu VBHN:

```bash
python scripts/tl.py vbhn-check \
  --subject "thi đua khen thưởng" \
  --goc "06/2022/QH15" \
  --json
```

Sau khi tìm được VBHN ngoài corpus, phải tải/nhập bản chính thức và verify:

```bash
python scripts/tl.py vbhn-verify \
  --text-file vbhn_tdkt.txt \
  --expect-title "thi đua khen thưởng" \
  --expect-goc "06/2022/QH15" \
  --official-required \
  --json
```

## Truy vấn web tối thiểu

`vbhn-check`/`relation-check` phải gợi ý các query đơn giản, gồm:

- `"luật thi đua khen thưởng" "hợp nhất"`
- `"thi đua khen thưởng" "văn bản hợp nhất"`
- `"thi đua khen thưởng" "VBHN"`
- `"luật thi đua khen thưởng" "Thư viện Pháp luật"`
- `site:thuvienphapluat.vn "luật thi đua khen thưởng" "hợp nhất"`

Thư viện Pháp luật/luatvietnam là nguồn secondary để phát hiện nhanh; khi chốt canonical vẫn ưu tiên Văn phòng Quốc hội, Công báo, vbpl.vn, .gov.vn hoặc bản người dùng nạp vào `_HOP_NAP`.

## Ghi registry sau khi người dùng xác nhận

Ví dụ ca Thi đua, khen thưởng:

- Dòng Luật `06/2022/QH15`: thêm `sua_doi = 06/2026/QH16`.
- Dòng Luật `06/2026/QH16`: thêm `goc = 06/2022/QH15`, chuẩn hóa `loai`, `hieuluc`, `note` hiệu lực.

Sau ghi:

```bash
python scripts/tl.py manifest --touched-drive
python scripts/tl.py relation-check --base "06/2022/QH15" --subject "thi đua khen thưởng" --json
```
