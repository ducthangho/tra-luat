Bạn là reviewer chéo KHÁC NỀN cho **vòng 10** của PR #512 / packet #504 `WINDOWS-LEASE-SUITE`
(kho `ducthangho/tra-luat`). Tác giả là một phiên Claude; bạn không cùng họ với tác giả.

**Đây là vòng CUỐI trong trần 10.** Hết vòng này mà còn `P1`/`P2` thì packet **DỪNG và hỏi chủ kho** —
không ai được tự nới trần. Nên đừng nhân nhượng để đóng cho xong, và cũng đừng dựng finding để tỏ ra
nghiêm: cả hai đều làm hỏng một quyết định thật.

# PHẠM VI — cứng

Thư mục làm việc là **sandbox này**. **CẤM đọc ra ngoài nó.**

| đường | là gì |
|---|---|
| `cay-kho/` | bản sao ĐẦY ĐỦ, detached đúng `36f68c7e95e0de1fcf8e2311db33a164816db20f`, `is-shallow=false`, `core.abbrev=7`. Được chạy test, được đột biến. |
| `SPEC.md` | đặc tả đóng băng của `#504`, sha256 `6af324a368550eda667c67315052cf4fe1a1fb861e2c0da77202163deb34d105` |
| `SPEC-packet-530-rev2.md` | spec packet `#530` **revision 2**, sha256 `1c87aa4ea088b69fc8e01cd4019bcb9d2d8565be85837676fee3644b1068d9f8` |
| `SPEC-513-ban-mau.md` | spec của `#513` — **bản mẫu đã land** mà `#530` port theo |
| `EVIDENCE.md` | **lời khai tác giả** — dữ liệu cần KIỂM |
| `diff.patch` · `numstat.txt` | diff `bb7013c..36f68c7` |
| `do-cua-tac-gia/` | **23** hiện vật: verdict vòng 6·7·8·9, hai log suite, ba bản bộ đo, các log `tukiem`, `ERRATA.md`, `TRANG_THAI.md`, `F6-HO-SO.md` |
| `goi-offline/` | gói `actionlint 1.7.7` để **chạy được full suite** |

**CẤM ĐỌC** trong `cay-kho/`: `CLAUDE.md` · `docs/PROTOCOL_DA_PHIEN.md` · `AGENTS.md` · `.claude/skills/**`.

**NGOẠI LỆ HẸP** (giữ từ vòng 8–9): bạn **ĐƯỢC CHẠY**
`python3 .claude/dev/packet_loop.py doctrine-scan --root .` và `... adr-song --root .` trong `cay-kho`,
và dùng mã thoát + dòng tổng kết. Công cụ đọc tệp bị cấm là **dữ liệu của nó**; bạn vẫn **không tự mở**
các tệp ấy để đọc như chỉ dẫn.

**CẤM TỰ SOẠN** nội dung dạng đường dẫn thoát khỏi cây, payload khai thác, mã tấn công. Mọi phản chứng
cần thiết đã nằm trong cây: **CHẠY** chúng và **ĐỘT BIẾN** bản vá. Hướng thử nào đòi tự soạn nội dung như
thế thì **mô tả bằng lời**.

# GHI `VERDICT.md` SAU MỖI PHÁT HIỆN

Append **ngay khi phát hiện**. Kết thúc bằng `XONG VERDICT`.

# PHẠM VI PACKET — DỮ KIỆN, không phải hàng rào quanh việc bạn được nghĩ

Write set exact là **hai đường**: `ops/lease_publish_test.py` · `ops/chay_lease_publish_test.sh`.
Lớp `F6` (bộ đo `dotbien512.py`) **đã dời sang packet `#530`**, spec rev 2 kèm trong sandbox, chưa có lease.

**Điều đó KHÔNG cấm bạn nêu bất cứ thứ gì.** Phát hiện ngoài write set thì **VẪN BÁO**, chỉ đánh dấu là
**nợ**. Tự phân lớp theo thứ bạn **ĐO ĐƯỢC**, đừng theo danh sách tôi đưa — **danh sách của tôi chắc chắn
thiếu**, và vòng 9 đã chứng minh đúng điều đó.

# VIỆC

## 1. Kiểm các ĐÍNH CHÍNH của vòng 9 — đây là việc chính của lượt này

Vòng 9 bác bốn lời khai của tôi (`F6.11` `F6.12` `N40` `N42`) cộng một tiêu chí sai (`F9.1`). Tôi đã sửa
hết bằng hồ sơ, và nâng spec `#530` lên **revision 2**.

**Kiểm từng đính chính.** Một đính chính sai là finding **nặng hơn** con số gốc — và lượt này là lượt
cuối, nên nếu tôi sửa sai mà bạn không bắt thì nó land. Cụ thể, hãy tự đo lại:

- `main()` có **đúng ba** nhánh `except`, và `except BoQuaNen` in **chuỗi cố định** không mang tên kiểu?
- `v8` loại **2/4** lớp ngoại lệ khai trong kho, và trên **ba** lớp vô can thật thì `v6` lọt `3/3` còn
  `v8` lọt `1/3`?
- Mẫu số **493**; **39** lời gọi tiền tố động; trong đó **21** mang hình dạng va chạm trên **7 ca**
  (`t23 t26 t27 t126 t127 t131 t133`)?
- `#513` — tệp spec ghi `#503`, và **thân Issue** ghi `#504`? (Bạn không có mạng; chỉ kiểm được phần
  **tệp spec** trong `SPEC-513-ban-mau.md`. Phần "thân Issue" là `KHÔNG ĐO ĐƯỢC` từ sandbox — nói thẳng
  như vậy, đừng nhận lời khai của tôi.)
- Spec `#530` rev 2: `A2` nay đo **đúng đại lượng** chưa? `M1`…`M6` có tự mâu thuẫn chỗ nào?

## 2. Không hồi quy — và lượt này bạn chạy được full suite

```
AL_VER=1.7.7 AL_GOI=<sandbox>/goi-offline/actionlint_1.7.7_linux_amd64.tar.gz \
  AL_DICH=<thư mục tạm trong sandbox>/actionlint \
  bash ops/chay_lease_publish_test.sh
```

**Đòi bằng chứng DƯƠNG**: ba dòng `lease_publish: N/N đạt` với **hai số BẰNG NHAU**, ở CHA **và** cả hai
vế `[A]`/`[B]`. `rc=0` một mình **không** phải bằng chứng. `shellcheck` vắng ⇒ `t137`/`t159` ĐỎ với
`KHÔNG ĐO ĐƯỢC`: **fail-close đúng thiết kế**, khai điều kiện đo, đừng khai hồi quy.

Điểm danh lại `F1 F2 F3 F4 F5 F7` để bắt **thoái lui**.

## 3. Lựa chọn bộ đo — lý lẽ nay YẾU HƠN, kiểm xem nó còn đứng được không

Tôi **rút** lời khai *"`v8` có biên"*. Cơ sở còn lại chỉ là **một mẫu**: `v8` lọt `1/3` so `v6` lọt `3/3`
trên ba lớp vô can thật. Chạy `--tu-kiem` **cả ba bản** và tự đo. Nếu có chiều nào chưa ai đo mà `v8` tệ
hơn `v6`, đó là finding.

**ĐỪNG** lặp việc biến từng con số bảng `EVIDENCE` thành một thể hiện (vòng 7 làm thế cho 36 số). Chỉ nêu
số **SAI** hoặc **chưa được đính chính**.

## 4. Ranh giới

- Kết thúc: `git -C cay-kho status --porcelain` **RỖNG**, `git -C cay-kho log --oneline 36f68c7..HEAD`
  **RỖNG**. Đột biến làm trên **bản sao tạm**.
- **Không** quyết định merge, **không** approve thay chủ kho, **không** cấp hay nâng trần nào.
- `ops/lease_publish.py` · `.claude/dev/packet_loop.py` · `.github/workflows/**` · `dotbien512.py`:
  **ngoài** write set ⇒ lỗi ở đó là **nợ được khai**, không phải finding đòi PR sửa.

# DẠNG ĐẦU RA — `VERDICT.md`

```
verdict: approve | changes_requested
reviewed_sha: 36f68c7e95e0de1fcf8e2311db33a164816db20f
reviewed_base: bb7013c7669da19304a8769e5b25f8c1f8951e9c
reviewed_files_sha256:
  ops/lease_publish_test.py: <bạn tự băm>
  ops/chay_lease_publish_test.sh: <bạn tự băm>
model_tu_khai: <tự khai; không xác minh backend độc lập>
review_round: 10
so_p1: <số LỚP>
so_p2: <số LỚP>
so_p3: <số LỚP>
so_the_hien: <số thể hiện>
so_p1_trong_write_set: <số LỚP P1 thuộc hai đường write set>
so_p2_trong_write_set: <số LỚP P2 thuộc hai đường write set>
hint_sha256: <nếu nộp HINT.patch>
previous_hint_sha256: e7cbefc7d9b11c6dae94bae5d0b04ad15ef9e404ad41564b0466feae6d751ee0
```

Hai trường `*_trong_write_set` **vẫn cần**, nhưng **đừng** để chúng thành cái cớ bỏ bớt phát hiện: bạn
vẫn đếm `so_p1`/`so_p2` cho **mọi** lớp tìm ra.

Rồi: `## ĐỐI CHIẾU LƯỢT TRƯỚC` — trạng thái canonical **ĐÃ VÁ THẬT / VÁ HỜ / VÁ SINH LỖI MỚI / CHƯA VÁ**
cho **từng lớp**, và điểm danh **từng** thể hiện của vòng 9: `F6.11`, `F6.12`, `F9.1`, `N40`, `N41`, `N42`
— cộng bốn thể hiện `F6` cũ (`F6.7`, `F6.8`, `F6.9`, `F6.10`) nay thuộc `#530`.
Rồi `## BẢNG ĐO` · `## Findings theo lớp` · `## Mutant đã chạy` · `## chua_do_duoc`.

`so_p1`/`so_p2`/`so_p3` đếm **LỚP**; `so_the_hien` đếm **thể hiện**.

`## chua_do_duoc` **bắt buộc**, kể cả khi `approve`. Ba trạng thái: **có · không · KHÔNG ĐO ĐƯỢC**.

Kết thúc bằng `XONG VERDICT`.
