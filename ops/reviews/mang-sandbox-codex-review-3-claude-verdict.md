verdict: changes_requested
reviewed_sha: 2ab5c76c36562738d2a059887e4846c954739a0a
provider: claude
executor: codex
reviewer: claude
round: 3

# Cross-review vòng 3 — `MANG-SANDBOX-CODEX` (#334)

## 0. Khả năng chạy mã, và bảng số tôi TỰ đo (không chép round 2)

```text
python3 --version               -> Python 3.11.15, rc=0
python3 -c 'print("PROBE_OK")'  -> PROBE_OK, rc=0
codex --version                 -> codex-cli 0.150.1, rc=0
```

Workspace hiện tại (`/tmp/.../scratchpad/c334r3`) đã đứng đúng
`HEAD=2ab5c76c36562738d2a059887e4846c954739a0a` (detached), `git status --porcelain` RỖNG. Không
cần dựng clone rời riêng — cây đã đúng exact SHA, sạch, và tôi không sửa gì trong đó.

**`codex sandbox` LỒNG chạy được trong môi trường của tôi** — giống round 2, khác round 1/lượt-3
executor (`rc=101`). Tôi tự chạy cả bảy lệnh (3 cột + 4 tổ hợp) NGUYÊN VĂN từ tài liệu, không chép
số của round 2:

### Bảng ba cột — tôi tự đo

| lệnh | socket | url | git | class socket | class url | class git |
|---|---:|---:|---:|---|---|---|
| `python3 .claude/dev/probe_mang.py` (ngoài codex) | 0 | 0 | 0 | LOT | LOT | LOT |
| `codex sandbox -c sandbox_mode=workspace-write --` | 1 | 1 | 1 | `POLICY_DENIED`(create) | `POLICY_DENIED`(urlopen) | **`UNKNOWN`**(rc=128) |
| `... -c sandbox_workspace_write.network_access=true --` | 0 | 0 | 0 | LOT | LOT | LOT |

### Bảng bốn tổ hợp — bốn lệnh nguyên văn `docs/MANG_SANDBOX_CODEX.md:33-37`, tôi copy-paste và chạy

```text
(a) không override                    -> socket=1 url=1 git=1  (git: UNKNOWN, rc=128)
(b) network_access=true               -> socket=0 url=0 git=0  (LOT)
(c) writable_roots=[.../.git,/tmp]    -> socket=1 url=1 git=1  (git: UNKNOWN, rc=128)
(d) network_access=true + writable_roots -> socket=0 url=0 git=0  (LOT)
```

Cả bảy ô khớp **byte-với-byte** với hai bảng trong tài liệu (kể cả cột `LỚP` mới thêm ở lượt 4).
Đây là lượt review THỨ HAI (sau round 2) tái lập được toàn bộ bảng bằng lệnh nguyên văn — không
phải lượt đầu tiên như đề bài giả định (đề bài soạn trước khi biết round 2 đã làm việc này); ghi
lại thẳng vì đề bài dựa trên tiền đề chưa đúng.

**Đối chiếu nguyên nhân proxy — không chỉ "nghe hợp lý", mà khớp SỐ CỔNG cụ thể:**

```text
$ env | grep -i https_proxy
https_proxy=http://127.0.0.1:44213
$ (trong sandbox mặc định) raw git = "...Failed to connect to 127.0.0.1 port 44213 after 0 ms..."
```

Cổng trong biến môi trường (`44213`) và cổng trong thông báo lỗi `git` bên trong sandbox lồng
KHỚP CHÍNH XÁC. Đây là bằng chứng mạnh hơn suy luận cơ chế chung chung: không chỉ "có proxy
loopback" mà đúng CHÍNH proxy đó là đích bị từ chối kết nối. Round 2 đã làm phép đối chiếu này với
cổng của họ (37215) và cũng khớp — hai lượt độc lập, hai cổng khác nhau (đúng như kỳ vọng vì mỗi
phiên có proxy riêng), cùng cơ chế được xác nhận hai lần.

## 1. Phán quyết P1 `bang-chinh-gom-unknown-vao-1-nhu-chan` — ĐÃ VÁ THẬT

Bản vá (lượt 4, diff `b5bb3952..2ab5c76c` trên `docs/MANG_SANDBOX_CODEX.md`, +9 dòng thêm cột
`LỚP` cho hai bảng, +1 câu cảnh báo "`1` KHÔNG đồng nghĩa...", và viết lại mục `KHÔNG_ĐO_ĐƯỢC` để
nêu rõ nguyên nhân git/proxy chưa tách được) khớp ĐÚNG với dữ liệu tôi tự đo ở mục 0 — không lệch
ô nào. Cột `LỚP` đúng là dữ liệu **đo lại độc lập** (không phải suy diễn), và tôi vừa xác nhận lần
thứ ba (sau round 2, và giờ là tôi) rằng bảy ô đó tái lập được nguyên văn.

Người vá là phiên điều phối (cùng nền `claude` với reviewer round 2 VÀ với tôi) — đúng cảnh báo
trong đề bài, `cross_approved` không đứng cho riêng phần này. Nhưng vì tôi tự chạy lại toàn bộ số,
không tin lời khai của phiên điều phối lẫn của round 2, phần dữ liệu SỰ THẬT (bảy ô class) đã được
kiểm độc lập bởi một nền/phiên thứ ba (tôi). Phần LỜI VĂN diễn giải quanh bảng — xem Việc 2 dưới —
vẫn còn một câu chưa cập nhật.

## 2. Câu chỏi còn sót — `docs/MANG_SANDBOX_CODEX.md:11`

**P2** `dong-11-hoi-to-lop-chua-cap-nhat-theo-cot-moi`

**Trích dẫn:** dòng 11 (không đổi trong lượt 4, tồn tại từ lượt 3):
> "Hai bảng cũ giữ nguyên số 0/1; vì lượt đo cũ không lưu lớp/raw, không hồi tố số 1 thành
> policy-denied."

**Vấn đề:** Lượt 4 (diff trên) đã sửa **đúng câu song sinh** của nhận định này ở mục
`KHÔNG_ĐO_ĐƯỢC` — xoá "Số cũ `1` không có lớp, stage, rc con hay raw; không thể phân loại hồi tố."
và thay bằng đoạn giải thích git/proxy chi tiết. Nhưng dòng 11, nằm ở phần MỞ ĐẦU tệp, mang cùng
nội dung ("không hồi tố số 1 thành policy-denied") và KHÔNG được cập nhật, trong khi chính hai
bảng ngay dưới nó (dòng 18-22, 40-45) giờ có cột `LỚP` gán nhãn `POLICY_DENIED`/`UNKNOWN` cho đúng
những ô "1" đó.

Đọc kỹ hai lần tôi thấy đây KHÔNG phải mâu thuẫn logic tuyệt đối: cột `LỚP` là dữ liệu ĐO LẠI độc
lập (round 2 + tôi đã xác nhận), không phải "hồi tố" theo nghĩa suy diễn từ raw cũ — nên câu ở
dòng 11, đọc sát nghĩa, vẫn đúng kỹ thuật. Nhưng nó ĐỌC NHƯ mâu thuẫn: một người đọc lướt dòng 11
("hai bảng cũ... không có lớp... không hồi tố") rồi nhìn ngay xuống bảng có cột `LỚP` đầy nhãn cụ
thể sẽ hợp lý mà hỏi "vậy sao có cột lớp ở đây". Đây đúng lớp lỗi mà `ma-chan-gom-moi-loi-khong-
phan-loai` (round 1) và `bang-chinh-gom-unknown-vao-1-nhu-chan` (round 2) đã lặp lại: sửa Ở MỘT
CHỖ, để lại câu song sinh Ở CHỖ KHÁC trong CÙNG một tệp — táp một tầng nhẹ hơn hai lần trước (ở
đây không sai dữ kiện, chỉ gây đọc-hiểu-lầm).

**Độ tin:** vừa (tôi xác nhận được sự KHÔNG NHẤT QUÁN về hình thức giữa dòng 11 và bảng, chưa
xác nhận được liệu có người đọc thật nào hiểu sai — đây là đánh giá biên tập, không phải phép đo
nhị phân).

**Đề xuất vá (≤3 dòng, còn biên ngân sách):** thêm một mệnh đề vào dòng 11, ví dụ đổi
`"...không hồi tố số 1 thành policy-denied."` thành
`"...không SUY DIỄN lớp cho số 1 lịch sử; cột LỚP ở hai bảng dưới là số ĐO LẠI độc lập (không
phải suy diễn từ số 0/1 cũ)."` — 1 dòng sửa, giữ đúng ý gốc, xoá cảm giác mâu thuẫn.

## 3. `meta-test-tu-canh-khong-ai-canh` — xác nhận vẫn CHƯA VÁ, và việc tách packet có cơ sở

- **Vẫn tái lập được, tự đo lại (không tin lời khai round 2):** trên bản sao ngoài cây (`mktemp
  -d`), bỏ lời gọi `t12_cong_dot_bien_tu_canh(None)` trong `main()` VÀ xoá dòng `# canh-nen-do`
  cùng lúc → `TỔNG: ĐẠT, rc=0`. Tái lập y hệt round 2 mô tả.
- **`.claude/dev/probe_mang.py` và `probe_mang_test.py` KHÔNG đổi so với `b5bb3952`** — xác nhận
  bằng `git diff b5bb3952b99f991e84f458f70dcd38c0bf9b90e2 2ab5c76c... -- <hai tệp>` = RỖNG cho cả
  hai. Lời khai "chỉ chạm `docs/`" ở lượt 4 ĐÚNG.
- **Baseline vẫn `11/11 ca · 5 đột biến · 0 sống · rc=0`** — tôi tự chạy `probe_mang_test.py`
  không đối số, output khớp mô tả trong đề bài từng chữ (kèm dòng `tự đột biến cổng: 9/9 chết`).
- **Việc tách sang packet `CONG-NGOAI-WRITE-SET` có cơ sở CẤU TRÚC hợp lý**: đường vá đúng nghĩa
  (một cổng bên ngoài ba tệp write-set, ví dụ trong `.claude/dev/packet_loop.py` hoặc CI, kiểm
  rằng `probe_mang_test.py` thật sự chạy và in đúng chuỗi kill) đòi sửa tệp NGOÀI write set của
  packet này → đúng `S3` theo protocol, không thể làm trong packet `MANG-SANDBOX-CODEX`. Không tự
  mâu thuẫn với luật "danh sách CẤM không bao giờ đủ" trong `CLAUDE.md` — ở đây không phải một
  danh sách cấm bị né, mà là một giới hạn cấu trúc thật (tệp không tự bảo vệ được khỏi người sửa
  chính nó).
- **KHÔNG ĐO ĐƯỢC:** liệu Issue GitHub cho `CONG-NGOAI-WRITE-SET` đã thực sự tồn tại chưa. Tôi thử
  `mcp__github__search_issues` — bị chặn vì phiên chưa được cấp quyền công cụ đó
  (`"you haven't granted it yet"`); không có `gh` CLI trong PATH của phiên này để thử đường khác;
  không tìm thấy chuỗi `CONG-NGOAI-WRITE-SET` ở bất kỳ đâu trong cây repo (`grep` toàn kho = 0
  kết quả) — nghĩa là quyết định tách packet này KHÔNG được ghi lại thành hiện vật nào trong chính
  kho tại exact SHA đang review. Theo đúng doctrine "SO LEASE KHONG NAM MOT CHO"/"hỏi chỗ kết luận
  được ghi" trong `CLAUDE.md`: đây là lời khai chưa neo được vào hiện vật, KHÔNG phải bằng chứng
  nó sai — chỉ là chưa xác minh được từ phạm vi tôi có quyền.
- **Theo đúng chỉ dẫn đề bài: KHÔNG chấm finding này là "chưa vá" để chặn land.** Ghi nhận nó là
  nợ đã có tên (`meta-test-tu-canh-khong-ai-canh`), đã tách khỏi packet này, và tài liệu
  `docs/MANG_SANDBOX_CODEX.md` (đọc toàn bộ, không chỉ vùng sửa) KHÔNG có câu nào tự nhận packet
  này đã "đóng" P1 đó — không có overclaim, chỉ là im lặng. Im lặng ở đây chấp nhận được vì P1 đó
  đã được chuyển packet công khai (trong đề bài của người giữ kho), không phải bị giấu.

## 4. Ngân sách và phạm vi

```text
$ git diff --numstat ac82ddc583f688d54bdc60e06922ec09bdab9f16 -- .claude/dev/probe_mang.py .claude/dev/probe_mang_test.py docs/MANG_SANDBOX_CODEX.md
101  0  .claude/dev/probe_mang.py
156  0  .claude/dev/probe_mang_test.py
60   0  docs/MANG_SANDBOX_CODEX.md
```

Tổng = **317**, khớp lời khai executor/đề bài. Trần **320** → biên còn **3**, khớp đề bài.

```text
$ git diff --name-only ac82ddc583f688d54bdc60e06922ec09bdab9f16
.claude/dev/probe_mang.py
.claude/dev/probe_mang_test.py
docs/MANG_SANDBOX_CODEX.md
```

Đúng ba đường dẫn, không thừa. `git diff --name-only ac82ddc... -- docs/GOI_AGENT_DA_NEN.md` =
RỖNG → tệp này ngoài write set, không bị chạm — khớp lời khai.

Finding ở mục 2 (dòng 11) đề xuất vá **1 dòng** — nằm gọn trong biên 3 còn lại, không cần nâng
trần.

## 5. BẢNG LỚP của chính tôi (đối chiếu lại với tài liệu)

| lệnh/tổ hợp | class socket | class url | class git | khớp tài liệu? |
|---|---|---|---|---|
| ngoài sandbox | LOT | LOT | LOT | có |
| sandbox mặc định / (a) | POLICY_DENIED(create) | POLICY_DENIED(urlopen) | UNKNOWN(rc=128) | có |
| (b) network_access=true | LOT | LOT | LOT | có |
| (c) writable_roots | POLICY_DENIED(create) | POLICY_DENIED(urlopen) | UNKNOWN(rc=128) | có |
| (d) cả hai cờ | LOT | LOT | LOT | có |

Không ô nào lệch. Không phát hiện `bang-chinh-gom-unknown-vao-1-nhu-chan` tái phát ở tầng dữ liệu
— chỉ tái phát nhẹ ở tầng LỜI VĂN (mục 2).

## 6. Finding mới (tóm tắt)

- `dong-11-hoi-to-lop-chua-cap-nhat-theo-cot-moi` — **P2** — xem mục 2. Không chặn land.

Không có finding P1 mới. Không nâng P2 lên P1.

## 7. CHỖ KHÔNG ĐO ĐƯỢC

| khẳng định | lệnh đã thử | lý do |
|---|---|---|
| Issue GitHub `CONG-NGOAI-WRITE-SET` có thật hay chưa | `mcp__github__search_issues` | quyền công cụ chưa được cấp trong phiên này; không có `gh` CLI |
| Trạng thái review/merge của PR #334 trên GitHub | không thử — ngoài phạm vi đề bài | đề bài không yêu cầu, mọi phép đo neo vào exact SHA cục bộ |
| `class` của `git` trong môi trường KHÔNG có proxy loopback (Codex chạy trên máy không qua hạ tầng phiên dạng này) | không có môi trường như vậy để thử | phiên này chỉ có một loại container, giống hạn chế round 2 đã ghi |
| Toàn bộ tổ hợp gộp mã phân loại ngoài 5 cặp round 2 đã tự đo | không đo lại — tin baseline `t11` (kiểm tập hợp, không kiểm từng cặp) đã đủ mạnh về cấu trúc | ngân sách lượt review; rủi ro thấp theo lý do round 2 đã nêu |

## 8. Kết luận

`changes_requested`, nhưng chỉ vì một **P2** duy nhất (`dong-11-hoi-to-lop-chua-cap-nhat-theo-cot-
moi`), có thể land ngay nếu nó được ghi thành nợ có tên thay vì vá — theo đúng luật dừng của đề
bài ("chỉ P1 mới chặn land"). Không có P1 nào còn mở trong PHẠM VI write set của packet này:
`bang-chinh-gom-unknown-vao-1-nhu-chan` đã vá thật (mục 1, xác nhận độc lập bằng bảy ô tự đo ở mục
0/5); `meta-test-tu-canh-khong-ai-canh` cố ý tách packet với cơ sở cấu trúc hợp lệ, không bị chấm
là "chưa vá" theo đúng chỉ dẫn đề bài. Nếu người giữ kho muốn `approved` thẳng, chỉ cần xác nhận đã
ghi nợ tên cho `dong-11-hoi-to-lop-chua-cap-nhat-theo-cot-moi` (hoặc vá 1 dòng như đề xuất mục 2)
— tôi để `changes_requested` vì bản thân tôi không có quyền quyết định "ghi nợ là đủ" thay người
giữ kho, không phải vì tôi coi đây là P1.
