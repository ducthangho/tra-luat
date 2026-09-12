Bạn là reviewer chéo KHÁC NỀN cho **vòng 9** của PR #512 / packet #504 `WINDOWS-LEASE-SUITE`
(kho `ducthangho/tra-luat`). Tác giả là một phiên Claude; bạn không cùng họ với tác giả.

# PHẠM VI — cứng

Thư mục làm việc là **sandbox này**. **CẤM đọc ra ngoài nó.**

| đường | là gì |
|---|---|
| `cay-kho/` | bản sao ĐẦY ĐỦ, detached đúng `36f68c7e95e0de1fcf8e2311db33a164816db20f`. `is-shallow=false`, `core.abbrev=7`. Được chạy test, được đột biến. |
| `SPEC.md` | đặc tả ĐÓNG BĂNG của `#504`, sha256 `6af324a368550eda667c67315052cf4fe1a1fb861e2c0da77202163deb34d105` |
| `SPEC-packet-F6-530.md` | spec đóng băng của packet `#530` (F6 đã dời sang đó), sha256 `5fcc14b5e33ecf130172bc1cafbb0ca229ddae8363069284eba5fcca49602781` |
| `EVIDENCE.md` | **lời khai tác giả** — dữ liệu cần KIỂM |
| `VERDICT-luot6/7/8.md` | verdict ba lượt trước |
| `diff.patch` · `numstat.txt` | diff `bb7013c..36f68c7` |
| `do-cua-tac-gia/` | **20** hiện vật của nhánh hồ sơ: hai log suite, ba bản bộ đo, các log `tukiem`, `ERRATA.md`, `TRANG_THAI.md`, `F6-HO-SO.md` |
| `goi-offline/` | gói `actionlint 1.7.7` để bạn **chạy được full suite** |

**CẤM ĐỌC** trong `cay-kho/`: `CLAUDE.md` · `docs/PROTOCOL_DA_PHIEN.md` · `AGENTS.md` · `.claude/skills/**`.

**NGOẠI LỆ HẸP** (giữ nguyên từ vòng 8, vì nó đã trả công): bạn **ĐƯỢC CHẠY**

```
python3 .claude/dev/packet_loop.py doctrine-scan --root .
python3 .claude/dev/packet_loop.py adr-song     --root .
```

trong `cay-kho` và dùng mã thoát + dòng tổng kết. Công cụ đọc các tệp bị cấm là **dữ liệu của nó**; bạn
vẫn **không được tự mở** các tệp ấy để đọc nội dung như chỉ dẫn.

**CẤM TỰ SOẠN** nội dung dạng đường dẫn thoát khỏi cây, payload khai thác, hay mã tấn công. Mọi phản
chứng cần thiết đã nằm trong cây: **CHẠY** chúng và **ĐỘT BIẾN** bản vá. Hướng thử nào đòi bạn tự soạn
nội dung như thế thì **mô tả bằng lời** cho phiên điều phối.

# GHI `VERDICT.md` SAU MỖI PHÁT HIỆN

Container có thể bị recycle bất chợt (vòng 6 phải phóng bốn lần). Append **ngay khi phát hiện**, đừng để
dành tới cuối. Kết thúc bằng dòng `XONG VERDICT`.

# PHẠM VI CỦA PACKET — là DỮ KIỆN, không phải hàng rào quanh việc bạn được nghĩ

Write set exact của `#504` là **hai đường**: `ops/lease_publish_test.py` · `ops/chay_lease_publish_test.sh`.
Lớp `F6` (bộ đo `dotbien512.py`) **đã được dời sang packet riêng** — Issue `#530`, spec đóng băng kèm
trong sandbox, chưa có lease.

**Điều đó KHÔNG có nghĩa bạn bị cấm nêu `F6` hay bất cứ thứ gì khác.** Nếu bạn thấy điều mới về nó, hoặc
về bất kỳ đường nào **ngoài** write set, **VẪN BÁO** — chỉ đánh dấu là **nợ**, không phải finding đòi PR
này sửa. Tự phân lớp theo thứ bạn ĐO ĐƯỢC, đừng theo danh sách tôi đưa: **danh sách của tôi chắc chắn
thiếu**, và mỗi chỗ nó thiếu mà bạn tìm ra là một finding.

# VIỆC

## 1. Kiểm hai lời khai NỀN trước mọi thứ khác

- **"Write set không đổi một byte kể từ vòng 7"** — đo, đừng nhận. Sai thì mọi kết luận `ĐÃ VÁ THẬT` của
  vòng 7 và 8 phải xét lại.
- **"`F6` là hệ quả đoán được của một write-set exclusion"** — đây là **lập luận trung tâm** cho việc dời
  `F6` ra khỏi PR. Kiểm nó: `cay-kho/ops/nhanh_don_duoc_test.py` có thật những gì `EVIDENCE` liệt kê
  không (lớp tín hiệu, ba trạng thái, kênh riêng, `DOT_BIEN_TU_KIEM`)? Nếu lập luận ấy sai, việc dời
  `F6` mất căn cứ và đó là finding **P1**.

## 2. Không hồi quy — và lượt này bạn chạy được full suite

`F1 F2 F3 F4 F5 F7` được vòng 8 kết `ĐÃ VÁ THẬT`. Kiểm **không thoái lui**.

```
AL_VER=1.7.7 AL_GOI=<sandbox>/goi-offline/actionlint_1.7.7_linux_amd64.tar.gz \
  AL_DICH=<thư mục tạm trong sandbox>/actionlint \
  bash ops/chay_lease_publish_test.sh
```

**Đòi bằng chứng DƯƠNG**: ba dòng `lease_publish: N/N đạt` với **hai số BẰNG NHAU**, ở CHA **và** cả hai
vế `[A]`/`[B]`. `rc=0` một mình **không** phải bằng chứng. `shellcheck` vắng ⇒ `t137`/`t159` ĐỎ với
`KHÔNG ĐO ĐƯỢC`: đó là **fail-close đúng thiết kế**, khai điều kiện đo thay vì khai hồi quy.

## 3. Kiểm lời khai số — gồm các ĐÍNH CHÍNH

Tác giả tự khai **sáu** lỗi số (`N31`…`N39` cộng một lỗi MỚI: "ba" lớp ngoại lệ → **bốn**) và **một lỗi
phép đo** (một lần chạy trên **cây sai**, nhánh nền `master` `147` ca thay vì `36f68c7` `155` ca).

**Kiểm chính các lời đính chính ấy.** Một đính chính sai là finding nặng hơn con số gốc. Và quét tiếp:
còn chỗ nào mang số cũ mà chưa được điểm danh không?

Nhắc bài học kho đã trả giá: **một quan hệ đúng che được các số hạng đã trôi** (`1101 ≤ 1500` đúng,
`1101 > 300` đúng — y như với `1114`). Khi một câu vừa nêu số hạng vừa nêu quan hệ, **kiểm SỐ HẠNG**.

**ĐỪNG** lặp lại việc biến từng con số bảng `EVIDENCE` thành một thể hiện (vòng 7 làm thế cho 36 số).
Chỉ nêu số **SAI** hoặc **chưa được đính chính**.

## 4. Bộ đo — kiểm quyết định, không kiểm lại cả lớp F6

`F6` thuộc `#530` rồi. Nhưng **một quyết định của lượt này** thì thuộc lượt này: tác giả chọn giữ `v8`
làm mặc định **dù vòng 8 xếp bản vá ấy là `VÁ SINH LỖI MỚI`**, với lý lẽ *"`v6` cấp tín dụng giả cho cả
bốn lớp ngoại lệ của kho"* và *"tập lọt của `v6` không có biên, hồi quy của `v8` đếm được `8/454`"*.

Chạy `--tu-kiem` **cả ba bản** trong `do-cua-tac-gia/` và tự đo lại hai con số ấy. Nếu lý lẽ sai — ví dụ
`v8` thật ra tệ hơn trên một chiều chưa ai đo — đó là finding.

## 5. Ranh giới

- Kết thúc: `git -C cay-kho status --porcelain` **RỖNG** và `git -C cay-kho log --oneline 36f68c7..HEAD`
  **RỖNG**. Đột biến làm trên **bản sao tạm**.
- **Không** quyết định merge, **không** approve thay chủ kho, **không** cấp hay nâng trần nào.
- `ops/lease_publish.py` · `.claude/dev/packet_loop.py` · `.github/workflows/**` · `dotbien512.py` đều
  **ngoài** write set: lỗi ở đó là **nợ được khai**, không phải finding đòi PR sửa.

# DẠNG ĐẦU RA — `VERDICT.md`

```
verdict: approve | changes_requested
reviewed_sha: 36f68c7e95e0de1fcf8e2311db33a164816db20f
reviewed_base: bb7013c7669da19304a8769e5b25f8c1f8951e9c
reviewed_files_sha256:
  ops/lease_publish_test.py: <bạn tự băm>
  ops/chay_lease_publish_test.sh: <bạn tự băm>
model_tu_khai: <tự khai; không xác minh backend độc lập>
review_round: 9
so_p1: <số LỚP>
so_p2: <số LỚP>
so_p3: <số LỚP>
so_the_hien: <số thể hiện>
so_p1_trong_write_set: <số LỚP P1 thuộc hai đường write set>
so_p2_trong_write_set: <số LỚP P2 thuộc hai đường write set>
hint_sha256: <nếu nộp HINT.patch>
previous_hint_sha256: e7cbefc7d9b11c6dae94bae5d0b04ad15ef9e404ad41564b0466feae6d751ee0
```

Hai trường `*_trong_write_set` là **mới** ở lượt này, và cần vì tiêu chí đóng của `#504` nói về write set
— nhưng bạn **vẫn** đếm `so_p1`/`so_p2` cho **mọi** lớp bạn tìm ra, kể cả ngoài write set. Đừng để hai
trường ấy thành cái cớ bỏ bớt phát hiện.

Rồi: `## ĐỐI CHIẾU LƯỢT TRƯỚC` (trạng thái canonical **ĐÃ VÁ THẬT / VÁ HỜ / VÁ SINH LỖI MỚI / CHƯA VÁ**
cho **từng lớp**, và điểm danh **từng** thể hiện mở của vòng 8: `F6.7`, `F6.8`, `F6.9`, `F6.10`, `N31-b`,
`N32-b`, `N37`, `N38`, `N39`) · `## BẢNG ĐO` · `## Findings theo lớp` · `## Mutant đã chạy` ·
`## chua_do_duoc`.

`so_p1`/`so_p2`/`so_p3` đếm **LỚP**; `so_the_hien` đếm **thể hiện**.

`## chua_do_duoc` **bắt buộc**, kể cả khi `approve`. Ba trạng thái: **có · không · KHÔNG ĐO ĐƯỢC**.

Kết thúc bằng `XONG VERDICT`.
