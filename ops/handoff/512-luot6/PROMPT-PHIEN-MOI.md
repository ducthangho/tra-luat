# Prompt cho phiên mới — tiếp tục PR #512 từ vòng review 7

Bạn tiếp nhận packet **#504 `WINDOWS-LEASE-SUITE`** / **PR #512** sau khi vòng review 6 đã xong.

## BƯỚC 0 — BẮT BUỘC, theo đúng thứ tự này, TRƯỚC mọi việc khác

```
sed -n '1,140p' .claude/dev/launcher.py
python3 .claude/dev/launcher.py doctor
python3 .claude/dev/launcher.py chuan-bi      # nếu doctor báo codex chưa dùng được
git fetch origin 'refs/heads/*:refs/remotes/origin/*' --prune
git show origin/ops/handoff-512-luot6:ops/handoff/512-luot6/TRANG_THAI.md
```

`TRANG_THAI.md` là **hồ sơ bàn giao đầy đủ**: neo, trần, điều kiện dừng, bảy lớp review, nợ có tên, và
bài học vận hành đã trả giá. Đọc hết nó trước khi làm gì. Prompt này chỉ là **con trỏ + việc cần làm**,
không chép lại số liệu — số liệu sống trong tệp có băm, không trong prompt.

**Hai việc đo ngay ở bước 0, vì kết luận sai ở đây làm hỏng mọi thứ sau:**

1. **Lease còn hiệu lực không?** Lease `windows-lease-suite-exec-1-claude-20260911` hết hạn
   **`2026-09-12T14:05:00Z`**. So với `date -u`. **Hết hạn ⇒ DỪNG, xin chủ kho cấp generation mới** —
   không tự làm tiếp. Đây là điều kiện dừng cứng, không phải lời khuyên.
2. **Hai nguồn ref có khớp không?** `git ls-remote --heads origin` so `git for-each-ref refs/remotes/origin`,
   **so bằng TẬP TÊN với `comm`, KHÔNG bằng `wc -l`**. Thiếu ref ở cục bộ ⇒ **MÙ**, fail-close, fetch lại.

## Việc — bốn bước

### 1. Áp `HINT.rvwin512-6.patch`

```
git fetch origin claude/windows-lease-suite
git checkout -B claude/windows-lease-suite origin/claude/windows-lease-suite   # head 353eae1
git show origin/ops/handoff-512-luot6:ops/handoff/512-luot6/HINT.rvwin512-6.patch > /tmp/h6.patch
sha256sum /tmp/h6.patch          # PHẢI = e7cbefc7d9b11c6dae94bae5d0b04ad15ef9e404ad41564b0466feae6d751ee0
patch -p0 --dry-run --fuzz=0 < /tmp/h6.patch      # rc PHẢI = 0
patch -p0 --fuzz=0 < /tmp/h6.patch
```

Áp **NGUYÊN VĂN**. HINT đóng ba lớp P1 còn mở: **F2** (`N10` bỏ tee ở `t125` mà suite vẫn xanh) và
**F7** (`N01 N02 N12 N17 N18` sống). Nó chỉ chạm `ops/lease_publish_test.py` — đã kiểm trước.

**F6 KHÔNG nằm trong HINT và đừng cố nhét vào**: lỗi ở `dotbien512.py` (bộ đo đột biến), **ngoài write
set** của lease. Xử bằng hồ sơ riêng, khai bằng lời trong bản chiếu verdict.

### 2. Cổng tại chỗ — đòi BẰNG CHỨNG DƯƠNG, đừng tin `rc=0`

```
git config core.abbrev 7
AL_VER=1.7.7 AL_DICH=/tmp/actionlint bash ops/chay_lease_publish_test.sh
python3 .claude/dev/packet_loop.py doctrine-scan --root .
python3 .claude/dev/packet_loop.py adr-song --root .
git diff --numstat origin/master...HEAD -- ops/lease_publish_test.py ops/chay_lease_publish_test.sh
```

Tiêu chí: dòng tổng kết `lease_publish: N/N đạt` với **hai số BẰNG NHAU**, ở **phiên cha VÀ cả hai vế
`[A]`/`[B]`** — ba dòng, không phải một. `numstat` phải **≤ 1500** dòng thêm (trần `S2` đã được chủ kho
nâng từ 300; xem `TRANG_THAI.md`).

Rồi chạy lại catalogue đột biến (`dotbien512.py` trong thư mục bàn giao) — **và biết trước rằng bộ đo ấy
có lỗi F6**: nó cấp `GIET THAT` cho ngoại lệ vô can. Sửa nó trước khi tin số nó in ra, hoặc kiểm tay
từng mutant. **Đừng khai "N/N giết thật" từ một bộ đo bạn biết là hở.**

### 3. Commit, push, đăng bản chiếu

Commit message nêu **lý do và phép đo**, không chỉ nêu việc. Push `claude/windows-lease-suite`. Đăng bản
chiếu verdict vòng 6 + kết quả áp HINT lên PR #512, và nói rõ **nguồn có thẩm quyền là tệp có băm**.

Chỉ nhận **lượt CI tự động** do push sinh ra. **KHÔNG** `workflow_dispatch`, **KHÔNG** lane `windows`,
**KHÔNG** chạy lại job đỏ — full CI chỉ khi merge.

### 4. Vòng review 7

Dựng sandbox mới, phóng cross-review `codex` (`gpt-6-astra`, `model_reasoning_effort=xhigh`) trên head
sau HINT. Đã dùng **6/10** vòng (trần 10 do chủ kho nâng).

Yêu cầu của bản prompt reviewer, giữ nguyên từ vòng 6:

- **Phân loại theo LỚP, không theo từng lỗi riêng lẻ.** `so_p1`/`so_p2`/`so_p3` đếm LỚP; `so_the_hien`
  đếm thể hiện. Có mục `## ĐỐI CHIẾU LƯỢT TRƯỚC` với trạng thái canonical
  **ĐÃ VÁ THẬT / VÁ HỜ / VÁ SINH LỖI MỚI / CHƯA VÁ** cho từng lớp, và điểm danh **từng** thể hiện cũ.
- **GHI `VERDICT.md` SAU MỖI PHÁT HIỆN, không phải ở cuối.** Đây là chốt quan trọng nhất của lượt, xem
  §hạ tầng dưới.
- **CẤM đọc** `cay-kho/CLAUDE.md`, `cay-kho/docs/PROTOCOL_DA_PHIEN.md`, `cay-kho/.claude/skills/**`,
  `cay-kho/AGENTS.md` (ngoại lệ nêu rõ từng prompt).
- **CẤM tự soạn nội dung dạng đường dẫn thoát hoặc mã khai thác** — mọi phản chứng đã nằm trong cây;
  hướng thử nào cần nội dung như thế thì **mô tả bằng lời** cho phiên điều phối viết. (Đã trả giá: hai
  lượt review chết vì bộ lọc nội dung của nền khi reviewer tự soạn.)

Lặp vá → review → đăng verdict **tới khi hết P1 và P2, hoặc `approve`**. Ở bước mà bạn **dự đoán còn một
vòng nữa là approve**, kiểm **head drift** với `origin/master`; có drift thì **merge master TRƯỚC** khi
mở vòng mới. Sau khi đã quyết merge thì dù head đổi cũng **chỉ cần CI hậu merge**, không bắt cross-review
lại — trừ khi phát hiện lỗi.

## Hạ tầng — đọc trước khi kết luận "công cụ hỏng"

Container của phiên trước **bị recycle liên tục** (uptime đo được ở bốn thời điểm: 1,3 / 0,6 / 4,9 / 8,5
phút). Vòng 6 phải phóng **bốn** lần. Ba lần chết cùng chữ ký
`responses_websocket: Connection refused (os error 111)` → `Reconnecting... 3/5`.

**Đừng đọc đó thành "codex không dùng được".** Lượt đầu chạy trọn 15 phút, đọc xong verdict trước và chạy
ba cây đột biến. Đường hỏng là **mạng của container**, không phải xác thực, không phải quota.

Ba phép đo phân biệt "chết" với "đang chạy" — cần **cả ba**, vì `run.json` khai `trang_thai: dang_chay`
cho mọi lượt đã chết:

```
ps -p <pid>                                        # (1) tiến trình còn không
stat -c '%y %s' <sandbox>/VERDICT.md               # (2) mtime có đứng không
grep -cE 'Connection refused|Reconnecting' <run>/stderr.log    # (3) chữ ký mất mạng
```

Hai thứ chữa được, tác dụng **đo được**:

1. **`codex exec resume <session-id>`** giữ nguyên ngữ cảnh — không phải đo lại từ đầu. Tìm session ở
   `~/.codex/sessions/<năm>/<tháng>/<ngày>/rollout-*.jsonl`.
   **Bẫy đã trả giá `rc=2`: `codex exec resume` KHÔNG nhận `-s` và `-C`.** Sandbox phải đi qua
   `-c sandbox_mode=workspace-write`, và cwd phải `cd` **TRƯỚC** khi `exec`.
2. **Chỉ thị ghi verdict sau mỗi phát hiện** — nó biến một lần chết từ *mất cả lượt* thành *mất một
   finding*. Con số: `VERDICT.md` đi 1 089 → 11 688 → 18 888 byte qua ba lượt.

## CẤM — không có ngoại lệ

- **KHÔNG sửa một dòng mã nào** trong `ops/lease_publish.py`, `.claude/dev/packet_loop.py`,
  `.github/workflows/**` khi chưa có lease cho đường đó. Ca treo `S8-bo-deadline` nằm **trong**
  `ops/lease_publish.py` ⇒ chạm vào là điều kiện dừng `S3` ⇒ **DỪNG**, khai nợ.
- **KHÔNG tự cấp lease.** `--granted-by` từ chối mọi tên provider; thẩm quyền là chủ kho `ducthangho`.
- **KHÔNG nâng `timeout-minutes` trong `ci.yml`**, **không** skip / cách ly / vô hiệu một ca test để lấy
  màu xanh. Đó là `S4`.
- **KHÔNG tự nâng bất kỳ trần nào.** Vượt `1500` dòng thêm, hoặc hết `10` vòng review, thì **DỪNG và hỏi
  chủ kho**.
- **KHÔNG sửa đặc tả đã đóng băng** (`ops/specs/WINDOWS-LEASE-SUITE.md`, `§3.2`). Hệ quả cụ thể: `A5`
  vẫn ghi `300`, nên trạng thái đúng là *"KHÔNG ĐẠT ở ngưỡng 300, được chủ kho OVERRIDE lên 1500"* —
  **không** phải "A5 đạt". Đừng biến nó thành một ô tích xanh.
- **KHÔNG sửa tệp verdict trong `ops/reviews/`** — byte-exact, và `.claude/.packet_state/` không sửa tay.
- **KHÔNG viết chuỗi bỏ-qua-CI nguyên văn trong commit message**, kể cả khi đang trích dẫn để giải thích.
  GitHub khớp trên toàn thông điệp; dấu nháy ngược không phải hàng rào. Viết tách chữ hoặc mô tả bằng lời.
- **KHÔNG đưa định danh model vào commit / PR body / code comment** ngoài dòng trailer bắt buộc.

## Nếp đo — ngắn, và đã trả giá cho từng dòng

- **`rc=0` là cổng có thể bị lừa.** Đòi bằng chứng DƯƠNG: `N/N` với **hai số bằng nhau**, `"ok": true`.
- **Cổng không nói dối — nó VẮNG MẶT**, và "vắng mặt vì sạch" trông y hệt "vắng mặt vì chưa chạy". Trước
  khi kết luận từ một chỗ RỖNG, hỏi *"nếu thứ tôi đang tìm CÓ THẬT thì nó sẽ được ghi ở ĐÂU?"* rồi đi
  hỏi đúng chỗ đó.
- **"Có MẶT" khác "có ĐO".** Một ca `return` sớm vì đường dẫn sai vẫn được đếm là ĐẠT.
- **Đột biến bị giết không phải đột biến bị giết ĐÚNG LÝ DO** — đúng đây là finding F6 đang mở.
- **`git for-each-ref` đọc bộ đệm cục bộ, không hỏi máy chủ.** Xem bước 0 mục 2.
- **Đo thứ ĐÃ ĐẾN, không phải thứ đã GỬI.** Nhưng biết rằng đường ĐỌC của GitHub cũng chuẩn hoá thực thể
  HTML (`'`→`&#39;` …) ⇒ chênh lệch thực thể trong `diff` bản-đã-đăng là **tạo tác của công cụ đọc**,
  đừng ghi thành phát hiện.
- **Gate đỏ ⇒ đo nền trước khi nghi bản vá của mình**: chạy lại trên `origin/master` sạch, so DELTA. Đỏ
  sẵn thì nói *"đỏ sẵn, delta = 0"*.
- Lời khai phải bằng phạm vi đo được. Ba trạng thái, không phải hai: **có · không · KHÔNG ĐO ĐƯỢC** — và
  cái thứ ba làm cổng ĐỎ.

## Việc còn nợ sau khi #512 land

PR hồ sơ ADR-0034 cho #512: verdict vòng 6 (có trong thư mục bàn giao) + biên nhận v2 + README +
CHANGELOG + manifest. **Khai thẳng rằng verdict vòng 1–5 ĐÃ MẤT** cùng container cũ — chúng chưa từng
được đẩy vào kho. Đó là mất mát thật của hồ sơ, không được im lặng cho qua.
