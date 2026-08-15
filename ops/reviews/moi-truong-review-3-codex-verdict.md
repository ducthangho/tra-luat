# Verdict: changes_requested

- Reviewer: `codex`
- Lease: `moi-truong-review-3-codex-20260815`
- Reviewed head: `c89ca5929c2d5da6c182f7858e652c51df147cd5`
- Delta base: `026c4ea95ae5039ce32f794018a69f03a94bf41a`
- Master base: `d5b7bccd679480f2eb9e7f7d84c518bade7f7df1`
- Prompt SHA-256: `a41865735ad45e09f034585a6a741805957eadd17f494e06664fc42c5b9870ab`
- `la_viec_cua_packet: false`

## Findings

### `launcher-gates-still-fail-after-global-isolation`

- Severity: high
- Disposition: changes_requested

Chốt cô lập mới xử lý được rò sang các mutation chạy sau, nhưng cổng bắt buộc vẫn đỏ
tất định ở chính mutation bảo vệ đường xác thực fail-open:
`do_codex_tin_DONG_DAU_thay_vi_ma_thoat` sống, giết `0/1` ca đích. Hai lượt độc lập
đều kết thúc `DOT BIEN: 46/47 dat (1 khong do duoc tren nen nay)`, trái tuyên bố
`47/47` và trái yêu cầu không còn mục `SAI`. Vì mutation này đồng thời bỏ hai lớp
phòng thủ (mã thoát và lựa dòng trạng thái), việc nó sống làm mất bằng chứng cho hành
vi xác thực fail-closed; đây không phải sai số trình bày.

Suite chuẩn cũng chưa tạo được bằng chứng `89/89`: trên hai lượt, nó chỉ phát dòng bỏ
qua `t62` rồi không phát tổng kết. Ở phép đo chuyển hướng, cả các lệnh shell đặt sau
Python cũng không chạy, nên không thể chấp nhận rc/tổng kết như công bố. Điều này cho
thấy harness vẫn tác động tới tiến trình gọi hoặc kết thúc bất thường ngoài phần trạng
thái năm singleton; bản vá hiện tại chưa đóng finding HIGH lượt 2 ở mức gate chạy được
và đáng tin.

Bằng chứng chạy lại trên snapshot neo SHA bất biến, luôn dùng HOME tạm:

```bash
tmp=$(mktemp -d)
git archive c89ca5929c2d5da6c182f7858e652c51df147cd5 | tar -x -C "$tmp"
probe_home=$(mktemp -d)
(cd "$tmp" && HOME="$probe_home" python3 .claude/dev/launcher_test.py --dot-bien)
```

Chạy nguyên văn hai lần đều có:

```text
do_codex_tin_DONG_DAU_thay_vi_ma_thoat SAI  giet 0/1: (khong ca nao chet)
DOT BIEN: 46/47 dat  (1 khong do duoc tren nen nay)
```

Phép đo suite chuẩn neo cùng SHA:

```bash
tmp=$(mktemp -d)
git archive c89ca5929c2d5da6c182f7858e652c51df147cd5 | tar -x -C "$tmp"
probe_home=$(mktemp -d)
(cd "$tmp" && HOME="$probe_home" python3 .claude/dev/launcher_test.py; printf 'after=%s\n' "$?")
```

Đầu ra chỉ có dòng `BO QUA t62...`; không có tổng kết `89/89` và không có dòng
`after=...`.

## Đánh giá riêng chốt cô lập và `t89`

Quét toàn tệp không thấy ca sửa `sys.path`, `sys.modules`, cwd, `os.putenv`, signal,
hoặc atexit trong tiến trình runner. Các gán trực tiếp còn lại thuộc đúng năm mục được
chụp; `ctypes.windll` có `finally` cục bộ. Không thấy code mức module vá singleton.
`os.environ` được khôi phục trên chính đối tượng gốc bằng `clear/update`, phù hợp với
`os.environb` dùng chung backing mapping trên nền hỗ trợ; không thấy ca giữ tham chiếu
để thao tác sau context.

`t89` có răng. Trên bản sao tạm của đúng head, ba đột biến cơ học độc lập — thay bản
chụp nội dung bằng `{}`, vô hiệu nhánh hoàn nguyên nội dung, và bỏ cleanup trên đường
ngoại lệ — đều làm lời gọi riêng `t89_harness_phai_hoan_nguyen_trang_thai_toan_cuc`
trả rc 1. Vì runner mutation hiện chỉ sửa `launcher.py`, lập luận không đưa mutation
harness vào bảng hiện tại là đúng về giới hạn kỹ thuật; probe bản sao là cách cơ học
hợp lý để khóa nó. Tuy nhiên `t89` chỉ chứng minh context manager, không chứng minh
toàn bộ suite không phá tiến trình gọi, như kết quả suite chuẩn ở trên.

## Gates và evidence

- Bước 0 khớp: non-shallow, `core.abbrev=7`, HEAD/ref đúng SHA, remote đúng, delta đúng
  một tệp `.claude/dev/launcher_test.py`.
- Verdict lượt 2 đọc từ object gốc có SHA-256 đúng
  `0b28a66da5765f05384ddf724e5f88f95c5046f85745a0a07bae21f35ec4a390`.
- EOL: `scanned=330`, `checked=308`, `violations=[]`.
- Doc claims strict: `flags=[]` (359 advisory, không phải flag).
- Cây kho sạch sau các phép đo.

## Boundaries

- Không chạy Windows; một mutation không đo được trên POSIX.
- Không fetch/config trong vai reviewer; điều phối viên đã làm trước, reviewer xác minh
  lại các SHA/ref bất biến bằng đọc.
- Không thử REST/GitHub/`gh` theo đường giao việc đã xác định không dùng được.
- Không đọc, ghi, xoá hay thay auth thật; mọi lượt launcher dùng HOME tạm.
- Không in giá trị biến môi trường.
- Không sửa tệp kho, commit, push, merge, land hay deploy.

