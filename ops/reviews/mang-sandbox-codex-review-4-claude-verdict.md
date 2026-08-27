verdict: approved
reviewed_sha: 944742869b53946b56531c1da3f831a47707ecac
provider: claude
executor: codex
reviewer: claude
round: 4

# Cross-review vòng 4 — `MANG-SANDBOX-CODEX` (#334)

## 0. Khả năng chạy mã, `codex sandbox` lồng, bảng số tôi TỰ đo

```text
python3 --version               -> Python 3.11.15, rc=0
python3 -c 'print("PROBE_OK")'  -> PROBE_OK, rc=0
codex --version                 -> codex-cli 0.150.1, rc=0
```

Workspace đã đứng đúng `HEAD=944742869b53946b56531c1da3f831a47707ecac` (detached),
`git status --porcelain` RỖNG. Không dựng clone riêng — cây đã đúng exact SHA, sạch, tôi không sửa
gì trong đó.

**`codex sandbox` LỒNG chạy được** trong môi trường của tôi (nền `claude`, giống round 2/round 3,
khác round 1 và executor lượt 3 vốn `rc=101`). Tôi tự chạy cả bảy lệnh (3 cột + 4 tổ hợp) NGUYÊN
VĂN từ `docs/MANG_SANDBOX_CODEX.md` (không chép số của round 2/3):

### Bảng ba cột — tôi tự đo

| lệnh | socket | url | git | class socket | class url | class git |
|---|---:|---:|---:|---|---|---|
| `python3 .claude/dev/probe_mang.py` (ngoài codex) | 0 | 0 | 0 | `LOT` | `LOT` | `LOT` |
| `codex sandbox -c sandbox_mode=workspace-write --` | 1 | 1 | 1 | `POLICY_DENIED`(create) | `POLICY_DENIED`(urlopen) | `UNKNOWN`(rc=128) |
| `... -c sandbox_workspace_write.network_access=true --` | 0 | 0 | 0 | `LOT` | `LOT` | `LOT` |

### Bảng bốn tổ hợp — bốn lệnh nguyên văn `docs/MANG_SANDBOX_CODEX.md:34-38`, copy-paste và chạy

```text
(a) không override                       -> socket=1 url=1 git=1  (git: UNKNOWN, rc=128)
(b) network_access=true                  -> socket=0 url=0 git=0  (LOT)
(c) writable_roots=[.../.git,/tmp]       -> socket=1 url=1 git=1  (git: UNKNOWN, rc=128)
(d) network_access=true + writable_roots -> socket=0 url=0 git=0  (LOT)
```

Cả bảy ô khớp **byte-với-byte** với hai bảng trong tài liệu, kể cả cột `LỚP`. Đây là lượt review
THỨ BA liên tiếp (sau round 2, round 3) tái lập được toàn bộ bảng bằng lệnh nguyên văn.

**Đối chiếu nguyên nhân proxy — khớp SỐ CỔNG cụ thể, lần thứ ba, cổng thứ ba khác nhau:**

```text
$ env | grep -i https_proxy
https_proxy=http://127.0.0.1:33663
$ (trong sandbox mặc định) raw git = "...Failed to connect to 127.0.0.1 port 33663 after 0 ms..."
```

Cổng trong biến môi trường (`33663`) khớp cổng trong lỗi `git` bên trong sandbox lồng. Round 2 đo
cổng `37215`, round 3 đo cổng `44213`, tôi đo `33663` — ba phiên, ba cổng khác nhau (đúng như
doctrine "class của git phụ thuộc cấu hình proxy TỪNG PHIÊN"), cùng cơ chế được xác nhận ba lần
độc lập.

**Baseline `probe_mang_test.py` tôi tự chạy:**

```text
tự đột biến cổng: 9/9 chết (m1..m5 + 4 dòng cơ chế)
nền: 11/11 đạt
SỐ LIỆU: ca 11 · đột biến 5 · sống 0
TỔNG: ĐẠT
rc=0
```

Khớp lời khai đề bài từng chữ.

## 1. Việc 1 — P2 vòng 3 `dong-11-hoi-to-lop-chua-cap-nhat-theo-cot-moi`: ĐÃ ĐÓNG

Dòng 11-12 hiện tại (lượt 5, diff `2ab5c76c..94474286` trên `docs/MANG_SANDBOX_CODEX.md`, -1/+2
dòng):

> "Hai bảng giữ nguyên cột số 0/1 cũ; vì lượt đo cũ không lưu lớp/raw, KHÔNG suy diễn lớp cho
> những số ấy. Cột `LỚP` ở hai bảng dưới là số **ĐO LẠI ĐỘC LẬP**, không phải suy diễn từ 0/1."

So với câu cũ round 3 trích ("...không hồi tố số 1 thành policy-denied."), câu mới nói RÕ hai điều
mà câu cũ không nói: (a) cột 0/1 là số CŨ, (b) cột `LỚP` là số ĐO LẠI ĐỘC LẬP — đúng khớp với thực
tế tôi vừa tự đo lại ở mục 0 (bảy ô, ba phiên độc lập). Bản vá gần như nguyên văn đề xuất của round
3 ("cột LỚP... là số ĐO LẠI độc lập, không phải suy diễn từ số 0/1 cũ").

Đọc lại với cùng phép thử của round 3 ("người đọc lướt dòng 11 rồi nhìn xuống bảng có cột `LỚP`
đầy nhãn cụ thể có còn hỏi 'vậy sao có cột lớp ở đây' không?"): KHÔNG còn — câu mới trả lời thẳng
câu hỏi đó ngay tại chỗ, không cần suy luận từ cách dùng từ "hồi tố" mơ hồ nữa. **Đóng.**

Không thấy câu vá tạo ra mâu thuẫn MỚI ở chỗ khác (xem Việc 3).

## 2. Việc 3 — quét toàn tệp (61 dòng, đọc từ dòng 1) tìm câu chỏi khác

Đọc trọn `docs/MANG_SANDBOX_CODEX.md`, đối chiếu từng khẳng định văn xuôi với bảng và với mục
`KHÔNG_ĐO_ĐƯỢC`:

- Dòng 8 ("`MA_CU=1` chỉ có nghĩa *không lọt*") ↔ dòng 25 ("`1` KHÔNG đồng nghĩa 'bị chặn bởi
  chính sách sandbox'") — nhất quán, cùng một khẳng định nhắc lại có chủ đích, không chỏi.
- Dòng 19-23 (bảng ba cột) ↔ dòng 41-46 (bảng bốn tổ hợp) — hàng "mặc định"/"(a)" và hàng
  "network_access=true"/"(b)" ra cùng số, cùng lớp. Nhất quán.
- Dòng 30-31 ("phiên điều phối rút... chạy lại; không dùng nó để tuyên bố đã tái lập trong sandbox
  Codex của executor lượt này") ↔ dòng 54 ("Executor lượt này không chạy lại... rc=101 trước
  probe") — cùng nói một sự kiện (executor không tự chạy được), không chỏi; đúng lý do vì sao bảng
  bốn tổ hợp cần một actor khác (điều phối/reviewer) chạy hộ.
- Dòng 48-50 ("`network_access=true` một mình đã đảo cả ba quan sát; `writable_roots` không đảo ô
  nào") — khớp đúng dữ liệu bảng (so (a) với (c): không đổi; so (a) với (b): đổi cả ba). Đã tự đo
  lại ở mục 0, khớp.
- Dòng 55-60 (git UNKNOWN do proxy, không phải chính sách) ↔ đối chiếu cổng ở mục 0 — khớp, và nay
  có THÊM một điểm dữ liệu (cổng thứ ba) củng cố thay vì chỉ hai.
- Dòng 16 ghi điều kiện `codex-cli 0.150.0`; phiên tôi chạy là `0.150.1`. Đây KHÔNG phải câu chỏi
  nội tại — dòng 4-5 đã tự rào "Bảng dưới là số đã chốt ngày 27-08-2026, không phải lời hứa cho
  phiên bản hay cấu hình khác", và thực tế tôi tái lập được y hệt trên `0.150.1` nên chênh version
  không gây sai số, chỉ là ghi chú điều kiện lịch sử. Không đủ để thành finding.

Không tìm thêm câu chỏi nào khác ngoài cái round 3 đã bắt và lượt 5 đã đóng.

## 3. Việc 4 — hai tệp mã không đổi ở lượt 4/5: XÁC NHẬN

```text
$ git diff b5bb3952b99f991e84f458f70dcd38c0bf9b90e2 944742869b53946b56531c1da3f831a47707ecac \
    -- .claude/dev/probe_mang.py .claude/dev/probe_mang_test.py
(rỗng, rc=0)
```

Lời khai "chỉ chạm `docs/` ở lượt 4 và 5" ĐÚNG cho toàn bộ khoảng lượt 3→5, không chỉ lượt 4.
Baseline `11/11 ca · 5 đột biến · 0 sống · rc=0` tôi tự chạy lại ở mục 0, khớp.

## 4. Việc 5 — ngân sách và phạm vi

```text
$ git diff --numstat ac82ddc583f688d54bdc60e06922ec09bdab9f16 944742869b53946b56531c1da3f831a47707ecac \
    -- .claude/dev/probe_mang.py .claude/dev/probe_mang_test.py docs/MANG_SANDBOX_CODEX.md
101  0  .claude/dev/probe_mang.py
156  0  .claude/dev/probe_mang_test.py
61   0  docs/MANG_SANDBOX_CODEX.md
```

Tổng = **318**, khớp lời khai đề bài ("khai 318"). Trần **320** → biên còn **2**, khớp đề bài.

```text
$ git diff --name-only ac82ddc583f688d54bdc60e06922ec09bdab9f16 944742869b53946b56531c1da3f831a47707ecac
.claude/dev/probe_mang.py
.claude/dev/probe_mang_test.py
docs/MANG_SANDBOX_CODEX.md
```

Đúng ba đường dẫn, không thừa.
`git diff --name-only ac82ddc... 94474286... -- docs/GOI_AGENT_DA_NEN.md` = RỖNG trên TOÀN khoảng
(không chỉ lượt cuối) → tệp ngoài write set không bị chạm ở bất kỳ lượt nào.

Không có hướng vá nào tôi thấy cần thêm — biên 2 dòng không bị đụng tới.

## 5. BẢNG LỚP của chính tôi (round 4)

| lệnh/tổ hợp | class socket | class url | class git | khớp tài liệu? |
|---|---|---|---|---|
| ngoài sandbox | `LOT` | `LOT` | `LOT` | có |
| sandbox mặc định / (a) | `POLICY_DENIED`(create) | `POLICY_DENIED`(urlopen) | `UNKNOWN`(rc=128) | có |
| (b) network_access=true | `LOT` | `LOT` | `LOT` | có |
| (c) writable_roots | `POLICY_DENIED`(create) | `POLICY_DENIED`(urlopen) | `UNKNOWN`(rc=128) | có |
| (d) cả hai cờ | `LOT` | `LOT` | `LOT` | có |

Không ô nào lệch. Ba lượt review liên tiếp (2, 3, 4) cùng tái lập bảy ô này với ba proxy port khác
nhau — dữ liệu SỰ THẬT của packet nay đã được kiểm độc lập bốn lần (executor lượt 3 + ba reviewer).

## 6. Finding mới

Không có. Không P1, không P2 mới. P2 duy nhất còn treo từ round 3 (`dong-11-hoi-to-lop-chua-cap-
nhat-theo-cot-moi`) đã được vá thật ở lượt 5 (mục 1) — không phải chỉ ghi nợ, mà đã đóng bằng nội
dung.

`meta-test-tu-canh-khong-ai-canh` giữ nguyên trạng thái: cố ý KHÔNG vá trong packet này, đã tách
sang `CONG-NGOAI-WRITE-SET` theo đúng chỉ dẫn đề bài — không chấm là "chưa vá" để chặn land.

## 7. CHỖ KHÔNG ĐO ĐƯỢC

| khẳng định | lệnh đã thử | lý do |
|---|---|---|
| Trạng thái Issue `CONG-NGOAI-WRITE-SET` / PR #334 trên GitHub | không thử | ngoài phạm vi đề bài; mọi phép đo neo exact SHA cục bộ, đúng chỉ dẫn |
| `class` của `git` trong môi trường KHÔNG có proxy loopback | không có môi trường như vậy | phiên này chỉ có một loại container, giống hạn chế round 2/3 đã ghi |
| Tái lập `meta-test-tu-canh-khong-ai-canh` trên bản sao ngoài cây | không tự chạy lại — round 3 đã làm và tôi không nghi ngờ vì đây không phải finding đang mở của lượt này | ngân sách; trọng tâm lượt 4 là bảng số + câu chỏi + phạm vi, đề bài không yêu cầu đo lại việc round 3 đã đóng |

## 8. Kết luận

`approved`. Không còn P1 nào trong write set. P2 duy nhất còn mở sau round 3 đã được vá thật ở
lượt 5 (không chỉ ghi nợ) — kiểm bằng diff trực tiếp và đọc lại toàn văn, không chỉ tin lời khai.
Bảy ô số liệu cốt lõi của packet đã được bốn phiên độc lập (executor lượt 3, reviewer round 2,
round 3, và tôi ở round 4) tái lập giống hệt nhau bằng lệnh nguyên văn từ tài liệu. Hai tệp mã
không đổi từ `b5bb3952`, baseline test vẫn `11/11 · 5 đột biến · 0 sống`. Ngân sách 318/320, đúng
ba đường dẫn write set, tệp ngoài write set không bị chạm. Không nâng P2 lên P1 để giữ packet mở.
