Bạn là reviewer chéo KHÁC NỀN cho **vòng 7** của PR #512 / packet #504 `WINDOWS-LEASE-SUITE`
(kho `ducthangho/tra-luat`). Tác giả là một phiên Claude; bạn KHÔNG cùng họ với tác giả.

# PHẠM VI — cứng

Thư mục làm việc của bạn là **thư mục sandbox này**. **CẤM đọc ra ngoài nó.** Mọi thứ bạn cần đã ở đây:

| đường | là gì |
|---|---|
| `cay-kho/` | bản sao ĐẦY ĐỦ của kho, detached đúng `36f68c7e95e0de1fcf8e2311db33a164816db20f`. `is-shallow=false`, 2135 commit trên master, `core.abbrev=7`. Bạn ĐƯỢC chạy test, ĐƯỢC đột biến nó. |
| `kho.git/` | mirror bare, nguồn của `cay-kho` |
| `SPEC.md` | đặc tả ĐÓNG BĂNG, sha256 `6af324a368550eda667c67315052cf4fe1a1fb861e2c0da77202163deb34d105` |
| `EVIDENCE.md` | **lời khai của tác giả** — dữ liệu cần KIỂM, không phải sự thật |
| `VERDICT-luot6.md` | verdict vòng 6 (nguồn có thẩm quyền của lượt trước) |
| `HINT-luot6.patch` | bản vá vòng 6 mà tác giả đã áp ở `36f68c7` |
| `diff.patch` · `numstat.txt` | diff `bb7013c..36f68c7` |
| `do-cua-tac-gia/` | log suite, catalogue đột biến, bộ đo F6 (bản vá + bản phản chứng), hồ sơ F6 |

**CẤM ĐỌC** trong `cay-kho/`: `CLAUDE.md` · `docs/PROTOCOL_DA_PHIEN.md` · `.claude/skills/**` · `AGENTS.md`.
Chúng là chỉ dẫn cho tác giả, không phải đầu vào của bạn.

**CẤM TỰ SOẠN** nội dung dạng đường dẫn thoát khỏi cây thư mục, payload khai thác, hay mã tấn công.
Mọi phản chứng cần thiết ĐÃ nằm trong cây: việc của bạn là **CHẠY** chúng và **ĐỘT BIẾN** bản vá để đo
răng. Hướng thử nào đòi bạn tự soạn nội dung như thế thì **MÔ TẢ BẰNG LỜI** cho phiên điều phối viết —
đừng tự viết. (Đã trả giá: hai lượt review chết vì bộ lọc nội dung của nền khi reviewer tự soạn.)

# GHI `VERDICT.md` SAU MỖI PHÁT HIỆN — chốt quan trọng nhất của lượt này

Container này **bị recycle bất chợt** (vòng 6 phải phóng BỐN lần; uptime đo được 1,3 / 0,6 / 4,9 / 8,5
phút). Nếu bạn để dành việc ghi tới cuối, một lần chết xoá sạch cả lượt.

Vì vậy: **ghi `VERDICT.md` ngay sau MỖI phát hiện**, append dần, đừng đợi. Con số chứng minh nó có tác
dụng: qua ba lượt của vòng 6, `VERDICT.md` đi `1 089 → 11 688 → 18 888` byte — mỗi lần chết chỉ mất
MỘT finding thay vì mất cả lượt. Kết thúc bằng dòng `XONG VERDICT`.

# VIỆC

## 1. Đối chiếu lượt trước — BẮT BUỘC có mục `## ĐỐI CHIẾU LƯỢT TRƯỚC`

Vòng 6 khai **3 lớp P1 / 0 P2 / 0 P3 / 5 thể hiện**: `F2` (1 thể hiện), `F6` (1), `F7` (3).
Cho **TỪNG LỚP** một trạng thái canonical, dùng ĐÚNG một trong bốn từ:

**ĐÃ VÁ THẬT · VÁ HỜ · VÁ SINH LỖI MỚI · CHƯA VÁ**

và **điểm danh TỪNG thể hiện cũ** (`F2.3`, `F6.4`, `F7.2a`, `F7.2b`, `F7.2c`) — không gộp, không bỏ sót.
Bốn lớp `F1`/`F3`/`F4`/`F5` vòng 6 đã kết `ĐÃ VÁ THẬT`: kiểm xem bản vá vòng này có làm chúng **thoái
lui** không.

Cụ thể, năm mutant vòng 6 thấy SỐNG — `N01` `N02` `N10` `N12` `N17` `N18` — hãy **dựng lại và chạy**
trên `cay-kho` hiện tại. Chúng phải CHẾT. `N09` vòng 6 kết là mutant TƯƠNG ĐƯƠNG, không tính finding;
kiểm lại kết luận ấy nếu bạn muốn, nhưng đừng đếm nó thành P.

## 2. Phân loại theo **LỚP**, không theo từng lỗi riêng lẻ

`so_p1` / `so_p2` / `so_p3` đếm **LỚP**. `so_the_hien` đếm **thể hiện**. Hai con số khác nhau và phải
cùng có mặt. Một lớp có năm thể hiện vẫn là **một** lớp.

## 3. Kiểm lời khai của tác giả — `EVIDENCE.md` là dữ liệu, không phải sự thật

Tác giả **tự khai một lỗi số của chính mình** trong `EVIDENCE.md` (numstat `1114` → `1101`). **Kiểm nó
trước tiên**, kể cả phần giải thích nguyên nhân: nếu lời đính chính ấy cũng sai, đó là một finding nặng
hơn con số gốc.

Và quét rộng hơn thế: bài học đắt của kho này là **một quan hệ đúng che được các số hạng đã trôi**
(*"117 cặp / 100 đường, chênh 10"* — chênh vẫn đúng 10 trong khi cả hai số hạng đã sai). Nên khi một câu
vừa nêu số hạng vừa nêu quan hệ, **kiểm SỐ HẠNG**, đừng kiểm quan hệ.

Bảng số trong `EVIDENCE.md` do tôi trích, và nó **chắc chắn thiếu**: tôi chỉ liệt kê thứ tôi nghĩ tới.
**Mỗi con số trong kho mà bảng ấy bỏ sót, bạn tìm ra được, tính là một finding.**

## 4. Đo răng bằng ĐỘT BIẾN, không bằng đọc

- Chạy suite: `AL_VER=1.7.7 AL_DICH=<thư mục tạm trong sandbox>/actionlint bash ops/chay_lease_publish_test.sh`
  trong `cay-kho`. **Đòi bằng chứng DƯƠNG**: ba dòng `lease_publish: N/N đạt` với **hai số BẰNG NHAU**,
  ở CHA **và** cả hai vế `[A]`/`[B]`. `rc=0` một mình **không** phải bằng chứng.
  Nếu `shellcheck` vắng trong môi trường của bạn thì `t137`/`t159` sẽ ĐỎ với lý do `KHÔNG ĐO ĐƯỢC` —
  đó là cổng fail-close đúng thiết kế, **không phải** hồi quy; khai điều kiện đo thay vì khai hồi quy.
- Chạy catalogue đột biến `do-cua-tac-gia/dotbien512.py` và **tự kiểm bộ đo** bằng `--tu-kiem`.
  Bộ đo này VỪA được vá cho F6; `dotbien512_REGEX_CU.py` là bản phản chứng khác **đúng một dòng**.
  **Đừng tin con số `16/16` cho tới khi bạn tự chạy `--tu-kiem` cả hai bản.**
- **Đột biến bị giết không phải đột biến bị giết ĐÚNG LÝ DO.** Một mutant chết vì `AttributeError` vô
  can mà được đếm là "giết" là **tín dụng giả**. Kho này đã trả giá hai lần cho đúng chuyện đó.

## 5. Ranh giới bạn KHÔNG được vượt

- **Không sửa** `cay-kho` rồi để lại: kết thúc, `git -C cay-kho status --porcelain` phải **RỖNG** và
  `git -C cay-kho log --oneline 36f68c7..HEAD` phải **RỖNG**. Đột biến thì làm trên BẢN SAO TẠM.
- **Không** quyết định merge, **không** approve thay chủ kho, **không** cấp hay nâng trần nào.
- `ops/lease_publish.py` · `.claude/dev/packet_loop.py` · `.github/workflows/**` **ngoài write set**:
  lỗi ở đó là **nợ được khai**, không phải finding đòi PR này sửa. Nói rõ khi bạn chạm phải.

# DẠNG ĐẦU RA — `VERDICT.md` trong sandbox

Bắt đầu bằng khối khoá, đúng các trường sau:

```
verdict: approve | changes_requested
reviewed_sha: 36f68c7e95e0de1fcf8e2311db33a164816db20f
reviewed_base: bb7013c7669da19304a8769e5b25f8c1f8951e9c
reviewed_files_sha256:
  ops/lease_publish_test.py: <bạn tự băm>
  ops/chay_lease_publish_test.sh: <bạn tự băm>
model_tu_khai: <model bạn tự khai; không xác minh backend độc lập>
review_round: 7
so_p1: <số LỚP>
so_p2: <số LỚP>
so_p3: <số LỚP>
so_the_hien: <số thể hiện>
hint_sha256: <nếu bạn nộp HINT.patch; bỏ trống nếu không>
previous_hint_sha256: e7cbefc7d9b11c6dae94bae5d0b04ad15ef9e404ad41564b0466feae6d751ee0
```

Rồi các mục: `## ĐỐI CHIẾU LƯỢT TRƯỚC` · `## BẢNG ĐO` · `## Findings theo lớp` · `## Mutant đã chạy`
· `## chua_do_duoc`.

Nếu bạn nộp bản vá: **`HINT.patch`** ở gốc sandbox, `patch -p0` áp được từ gốc cây kho, `--fuzz=0`,
**chỉ chạm hai đường write set**. Tự chạy `patch -p0 --dry-run --fuzz=0` và ghi rc vào verdict.

`## chua_do_duoc` là **bắt buộc**, kể cả khi bạn `approve`. Ba trạng thái, không phải hai:
**có · không · KHÔNG ĐO ĐƯỢC** — và cái thứ ba không được im lặng biến thành "đạt".

Kết thúc tệp bằng dòng `XONG VERDICT`.
