# HANDOFF — `TAT-DINH-VOID-HA-TANG` (#262), Executor **generation 3** (`claude`)

- **Kết quả: DỪNG theo `dieu_kien_dung`.** `N11` hỏng **lần thứ TƯ**, cùng một họ lỗi.
- **PR #279 KHÔNG merge.** Cổng xanh, nhưng chốt trung tâm của slice **không đo được thứ nó khai**.
- Không phải thất bại nội dung mới: hai bản vá gen 3 đều **đúng và đã đo**; cái sai nằm ở
  **CÁCH TIẾP CẬN của N11**, và §12 bảo lúc này phải xem lại cách làm chứ không vá tiếp.

---

## 0. Handoff MÁY ĐỌC ĐƯỢC — `docs/PROTOCOL_DA_PHIEN.md` §7

```yaml
schema_version: 1
packet_id: TAT-DINH-VOID-HA-TANG        # Issue #262
generation: 3
spec_hash: dc4bc6226dbdfe3b5a3dc86cb990cc2c85574456a30f3c65f6d7492bd015d827   # r4, KHONG doi
provider: claude
role: executor
base_sha: 7707832f0570a5b87fd9e4e26329ef4a072ce5b3
head_sha: 7d34c34d447e7e52550e317454e1605f3efc3d3d
tree: b9c2075b17d728a1ce7df1d712ac4a2bb60bf182
status: blocked
summary: >-
  Ap dung hai ban va da thiet ke o handoff gen 2, va ca hai deu DUNG va da do. Nhung
  chieu BE MAT cua N11 hong LAN THU TU o cung mot ho: chot do mot PHEP CHIEU cua be
  mat CLI chu khong do toan bo be mat. Lan nay lot bang DOI SO VI TRI.
changed_paths:
  - .claude/dev/packet_loop.py
  - .claude/dev/packet_loop_test.py
  - ops/KE_HOACH_THI_CONG_CLAUDE_CODEX.md
tests:
  - name: packet_loop_test.py
    status: passed        # 231/231; 60 dot bien; 0 ngoai le AC 18
  - name: gate (ubuntu-latest)
    status: passed        # tren 7d34c34 — NHUNG khong do mot dong nao cua write set
remaining_work:
  - 'N11 chieu BE MAT chua canh duoc viec BO M3/M4. Bon lan sua, bon lan bi lach.'
  - 'Cau hoi dung KHONG con la "va the nao" ma la "liet ke be mat parser co phai
     cach dung de chung minh M3/M4 da bien mat khong".'
next_role: human
failure:
  fingerprint: n11-do-phep-chieu-cua-be-mat-cli-lan-thu-tu
  category: content
successors: []            # phien thi cong KHONG tu mo packet ke nhiem
```

---

## 1. BỐN LẦN, MỘT HỌ — đây là kết quả chính của generation này

| # | lượt | chốt (b) của N11 **đo gì** | lách bằng | ai tìm ra |
|---|---|---|---|---|
| 1 | gen 2 vòng 1 | `void-attempt --help` | `help=argparse.SUPPRESS` | codex |
| 2 | gen 2 vòng 2 | **bốn chính tả** cờ trong parser | alias `--evidence-file` | codex |
| 3 | gen 3 vòng 1 | tập cờ trên parser **tự nạp** (`_n11`) | cờ dưới `if __name__ == "__main__"` | codex |
| 4 | gen 3 vòng 2 | `option_strings` của parser **THẬT** | **đối số VỊ TRÍ** (`option_strings == []`) | codex |

**Mỗi lần vá đều đi đúng hướng và đều thất bại theo cùng một cách.** Từ (1) tới (4), chốt tiến
gần cửa CLI thật hơn — nhưng lần nào cũng đo **một PHÉP CHIẾU** của bề mặt ấy: văn bản trợ giúp →
tên cờ → đối tượng parser → `option_strings`. Mỗi phép chiếu bỏ sót một phần bề mặt, và reviewer
chỉ cần tìm đúng phần bị bỏ sót.

Nguyên văn reviewer vòng 2: *"vẫn là một cửa CLI thật khác master chưa đi qua chốt, tức **lần thứ
tư mở rộng phạm vi quan sát**."*

### Phản chứng lần 4, đã chạy trên `git worktree` rời

```
tiem:  q.add_argument("evidence_file", nargs="?")      # DOI SO VI TRI, khong phai co

CLI THAT:  void-attempt --packet 55 --reason quota fake-evidence.json
           ->  rc=8   (loi state — argparse DA NHAN; rc=2 moi la tu choi)
SUITE   :  nen: 231/231 dat      TONG: DAT      <- XANH HOAN TOAN
```

Tệ hơn lần 3: lần ấy còn có dòng đỏ phụ; lần này suite **sạch tuyệt đối** trong khi cửa CLI thật
nhận một đường bằng chứng.

## 2. Hai bản vá của gen 3 — cả hai ĐÚNG, giữ lại

Đừng làm lại. Chúng không phải nguyên nhân dừng.

**(a) Chốt đo CHÍNH parser `main()` dùng** (thay parser song song). Đo được:

```
a5e068e (parser song song) + co duoi guard __main__  ->  231/231   0 ca chet, LOT
7d34c34 (parser that)      + cung don                ->  230/231   1 ca chet, BAT
```

**(b) Trả lại `mt_siet_nguong_tuoi_ve_am_mot` kèm số đã đo**: bán kính **37/231**, `N1` không nằm
trong đó. Bán kính 1 là **BẤT KHẢ** cho một ca chiều THA. Lỗi của gen 2 vòng 1 không phải con số
mà là **khai 1 trong khi chưa đo**; gen 2 vòng 2 lại **xoá nghĩa vụ** thay vì thoả nó.

Ngân sách: `+253` → **nén** về **250/250**, không nới (gen 1 đã nới hai lần).

## 3. Bản vá vòng 2 của reviewer — GHI LẠI, CỐ Ý KHÔNG ÁP

> thay phép tính `co` bằng **phép chiếu phát sentinel cho mọi positional action** (net 0 dòng),
> thêm mutant positional 5 dòng; bù 5 dòng bằng bỏ hai dòng chú thích 2641–2642 và nén khối
> 2649–2654 từ sáu xuống ba dòng. Ca mới phải giết N11, chạy lại mutant alias, giữ
> `void_attempt_allowlist` xanh.

Bản vá này **có thể đúng**. Không áp vì nó là **phép chiếu thứ năm**: nó vá đúng lỗ vừa lộ
(positional) và để nguyên câu hỏi *"còn phần bề mặt nào nữa chưa đo?"*. Vài đường **chưa ai chạy**:
`parse_known_args` · `nargs=REMAINDER` · alias của subparser · cờ thêm **sau** `parse_args` đầu ·
`prefix_chars` khác · `argparse.SUPPRESS` trên chính subparser.

## 4. Câu hỏi cho packet kế nhiệm — KHÔNG phải "vá thế nào"

**Liệt kê bề mặt parser có phải cách đúng để chứng minh M3/M4 đã biến mất không?**

Một hướng KHÁC KIỂU (chưa thẩm định, nêu để khỏi mất): **so cấu trúc với `master`**. PR #274 từng
làm đúng một lần và nó có răng — *"thân `cmd_void_attempt` sau khi bỏ, lọc dòng chú thích, khớp
từng dòng với master: 20/20 dòng mã, 0 khác, 0 thiếu"*. Mở rộng phép ấy sang **khối dựng subparser
`void-attempt`** thì chốt không còn liệt kê thứ parser PHƠI RA, mà đòi mã dựng nó **giống hệt**
bản master vốn chưa từng có M3/M4. Bề mặt bao nhiêu chiều cũng không quan trọng nữa.

Điểm yếu đã thấy trước: nó nhạy với **mọi** thay đổi vô hại (đổi `help=`, xuống dòng), nên có thể
đỏ giả. Đó là đánh đổi cần thẩm định, không phải kết luận.

## 5. `chua_do_duoc` — khai thẳng

- **`packet_loop_test.py` KHÔNG có cổng CI nào.** `grep -rn "packet_loop" .github/` ⇒ **0**. Mọi
  tick xanh trên #274/#279 **không đo một dòng nào** của write set. Nợ đã tách: **#277**.
- **`N10′` tới giờ chưa lần nào được đo thật** — Linux bỏ qua có in lý do, Windows không ai gọi.
- **Gen 3 KHÔNG có bản ghi máy.** Tôi không chạy `init`/`record-lease`/`begin-attempt`/
  `record-review`, nên `attempts_used` và `review_rounds_used` của gen 3 **chỉ tồn tại trong
  comment**. Hai gen trước đều có — và chính bản ghi ấy là thứ làm cổng `same_failure` bắn được ở
  gen 2. Đây là chỗ tôi làm mỏng hơn tiền lệ, và nó nghĩa là **lần dừng này do người đọc phán,
  không do máy bắn**.
- **Cổng `same_failure` đếm SLUG, không đếm Ý ĐỊNH** — nợ từ gen 2 §6, vẫn cố ý không vá: sửa cái
  cổng vừa dừng mình, trong chính packet nó dừng, là tự cấp lối thoát.
- **Bốn chỗ mỏng của r1** vẫn nguyên: ngưỡng tươi 3600s đo bằng `mtime` (số là CHỌN, không ĐO) ·
  `getattr` nuốt im lặng một lần đổi tên · hai chỗ còn lại thuộc M4 đã bỏ.

## 6. Trạng thái để lại

| | |
|---|---|
| PR #279 | **MỞ**, cổng xanh trên `7d34c34` — **KHÔNG merge** |
| packet #262 | gen 3 `blocked`; gen 1 và gen 2 cũng `blocked` |
| vòng review gen 3 | **2/2 đã dùng**, `nang_tran: []` |
| ngân sách | **250/250**, 3/3 tệp — hết dư |
| lease gen 3 | `tat-dinh-void-ha-tang-exec-3-claude-20260823` (#262 comment `5384868006`) — **không hồi sinh** |
| #276 | packet kế nhiệm cho xác thực nguồn gốc, chưa lease — **độc lập với chỗ dừng này** |
| cây làm việc | sạch |
