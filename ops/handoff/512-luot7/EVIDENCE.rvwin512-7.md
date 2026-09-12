# EVIDENCE — lời khai của tác giả cho vòng review 7, PR #512 / packet #504

Mọi con số dưới đây là **lời khai**. Việc của bạn là **ĐO LẠI**, không phải nhận. Chỗ nào tôi khai
rộng hơn phép đo, đó là một finding.

## Neo

| | |
|---|---|
| `reviewed_sha` | `36f68c7e95e0de1fcf8e2311db33a164816db20f` |
| base | `bb7013c7669da19304a8769e5b25f8c1f8951e9c` (= `origin/master`, và = `merge-base`) |
| write set exact (2 đường) | `ops/lease_publish_test.py` · `ops/chay_lease_publish_test.sh` |
| spec đóng băng | `SPEC.md`, sha256 `6af324a368550eda667c67315052cf4fe1a1fb861e2c0da77202163deb34d105` |
| vòng review | **7**; đã dùng 6/10 |

Hai commit của lượt này:
- `1db6af2` — merge `origin/master` (đóng drift). Khai: **không đổi một byte** nào của write set.
- `36f68c7` — áp **NGUYÊN VĂN** `HINT-luot6.patch` (`e7cbefc7…1ee0`), `patch -p0 --fuzz=0`, một tệp.

## Đã đo — kèm ĐIỀU KIỆN ĐO

| phép đo | kết quả khai |
|---|---|
| suite đầy đủ | `155/155 đạt; đã chạy=155, bỏ qua=0` ở **`[A]` (log dòng 1055) · `[B]` (1060) · CHA (1156)**; **0** dòng `  ĐỎ  `; rc=0 |
| `t125` · `t158` · `t160` ở CHA | `55.445s QUA` · `3.381s QUA` · `0.066s QUA` |
| catalogue 16 đột biến của tác giả | `16/16 giết thật, 0 tín dụng giả, 0 sống sót`, rc=0 |
| tự kiểm bộ đo, hai chiều | bản CŨ `2/4` rc=**1** · bản MỚI `4/4` rc=**0** |
| `doctrine-scan --root .` | rc=0, `7 tệp, 0 chỗ chép doctrine` |
| `adr-song --root .` | rc=0, `47 ADR / 47 dòng §20` |
| `git diff --numstat bb7013c 36f68c7` (2 đường) | **+1101 / −27** (`1095+6`) |

**ĐIỀU KIỆN ĐO của con số `155/155`:** `actionlint 1.7.7` + **`shellcheck 0.9.0`**, Linux, python 3.11.15.
Lượt ĐẦU trong container này cho **`153/155`** vì **thiếu `shellcheck`**: `t137` và `t159` ĐỎ với lý do
*"KHÔNG ĐO ĐƯỢC: thiếu `shellcheck` — actionlint IM LẶNG bỏ toàn bộ luật shell khi vắng nó"*. Đó là cổng
fail-close đúng thiết kế, không phải hồi quy. Log của **cả hai** lượt nằm trong `do-cua-tac-gia/`.

## TỰ KHAI MỘT LỖI CỦA CHÍNH TÔI — hãy kiểm nó trước tiên

Thông điệp commit `36f68c7` ghi `numstat ... +1114/−27 (1076+32 và 6+0)`. **Con số `1114` SAI.**
Số đúng, đo lại trên kho **đầy đủ độ sâu**: **`+1101/−27`** (`1095+6`).

Nguyên nhân, nói cho đúng vì một nguyên nhân sai còn tệ hơn không ghi: tôi **CỘNG** `+32` của patch vào
`1076` thay vì **ĐO LẠI** sau khi commit. Patch `+32/−13` thay thế 13 dòng vốn đã là dòng THÊM của chính
PR này, nên delta thật ở cột "thêm" là `+19`, không phải `+32`. Ba mỏ neo nay nhất quán:
`353eae1` (trước HINT) so `b98531e` ⇒ `1076+6 = 1082` — **khớp đúng** con số vòng 6 đã ghi.

Đây **KHÔNG** phải do kho nông, dù kho nguồn ĐÚNG LÀ đã nông (`682/2135` commit trên master) và tôi đã
`--unshallow` trước khi dựng mirror cho bạn. `merge-base(origin/master, HEAD)` = `bb7013c` = chính
`origin/master`, nên `numstat` không bị độ sâu ảnh hưởng. Đừng ghép hai chuyện này làm một.

Không sửa lịch sử để giấu: commit `36f68c7` giữ nguyên, lời đính chính đi bằng hồ sơ.

## KHÔNG ĐO ĐƯỢC — đừng đọc thành ĐẠT, và đừng đọc thành ĐÃ LOẠI TRỪ

- **`A3`/`A4` (Windows ≤ 15 phút)**: không lượt Windows nào chạy trên head này, theo chỉ thị chủ kho
  (không CI tay; full CI khi merge). Linux `155/155` **không** chứng nhận thời gian Windows.
- **`N01`–`N18`**: đó là catalogue của **REVIEWER vòng 6**, KHÔNG có trong kho. Tôi chỉ chạy lại được
  catalogue 16 mutant của tác giả. Nên lời khai đúng về F2/F7 là **"ĐÃ ÁP HINT, suite xanh"**, KHÔNG
  phải "ĐÃ VÁ THẬT". Ai tuyên "vá thật" phải là lượt của bạn.
- **Nợ `S8-bo-deadline` chập chờn**: gốc trong `ops/lease_publish.py` = NGOÀI write set ⇒ chạm là `S3`.
- **Phân biệt rò `GITHUB_ACTOR` với ca chập chờn**: `KHÔNG ĐO ĐƯỢC`, không phải "đã loại trừ".
- **Trạng thái GitHub trực tiếp**: `KHÔNG ĐO ĐƯỢC` từ sandbox (không mạng).
- **`SO-CANON-CHUA-TON-TAI`**: `grep -rln "review_rounds_used" --include=*.py .` ⇒ **0 tệp**. Trần 10 vòng
  KHÔNG có cổng nào canh; đếm vòng là đếm TAY.

## `A5` — KHÔNG phải một ô tích xanh

`SPEC.md` vẫn ghi `A5 ≤ 300` và **không được sửa** (`§3.2`). `1101 > 300`. Trạng thái đúng:
**"KHÔNG ĐẠT ở ngưỡng 300, được chủ kho OVERRIDE lên 1500"**. Nếu tôi viết nó thành "A5 đạt" ở bất kỳ
đâu, đó là finding.

## F6 — phạm vi của lời khai

`dotbien512.py` nằm NGOÀI write set ⇒ vá bằng hồ sơ riêng (nhánh `ops/handoff-512-luot7`), KHÔNG vào PR.
Đo lại ra **HAI** thể hiện, vòng 6 khai một: regex cũ đòi ít nhất một ký tự trước `Error|Exception` nên
`Exception:` TRẦN **và** `Error:` TRẦN đều lọt.

Trạng thái tôi khai: **"ĐÃ VÁ THẬT phần đo được, CÒN NỢ phần chống giả mạo tín hiệu"** — bộ đo chạy ngoài
tiến trình và chỉ đọc CHUỖI, nên một `except` trong tệp test vẫn giả được tín hiệu. Chi tiết
`do-cua-tac-gia/F6-HO-SO.md`. Nếu bạn thấy tôi khai mạnh hơn thế ở đâu, đó là finding.

## Sandbox — trạng thái đã đo

- `cay-kho` detached tại `36f68c7`, `status --porcelain` **RỖNG**, `is-shallow-repository` = **false**,
  `origin/master` có **2135** commit, `core.abbrev` ghim **7**.
- So tập ref kho nguồn với mirror: lệch **đúng một** tên, và là **THỪA** ở mirror
  (`claude/packet-504-pr-512-qdli7h`, nhánh cục bộ của phiên tác giả bị `clone --bare` kéo sang).
  Thừa ở cục bộ là vô hại; **thiếu** mới là mù, và không thiếu tên nào.
- Phép so hai nguồn ref đã chạy **TRÊN KHO NGUỒN, TRƯỚC khi clone**: `356/356`, `comm` rỗng cả hai chiều.
  Chạy lại nó **trong sandbox là vô nghĩa**: `origin` ở đây là URL HTTPS thật mà sandbox không ra được
  mạng, nên `ls-remote` sẽ `rc=128` và **0 dòng** — nó không đếm gì cả, không phải "đếm mirror".
