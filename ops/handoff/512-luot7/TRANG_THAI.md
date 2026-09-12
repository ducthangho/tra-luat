# Trạng thái bàn giao — PR #512 / packet #504 WINDOWS-LEASE-SUITE, sau khi áp HINT vòng 6

Soạn 13:05Z 12-09-2026, phiên `claude` `session_01VcRXCE7mEDMMcFnJVo5Xeb`.
Thư mục này tồn tại vì hiện vật review sống trong scratchpad EPHEMERAL của container — verdict vòng 1–5
của packet này ĐÃ MẤT đúng theo đường đó. Thứ phiên sau cần phải nằm trong **git**.

## Neo

| | |
|---|---|
| PR | #512 · nhánh `claude/windows-lease-suite` |
| head ĐÃ ĐẨY | **`36f68c7e95e0de1fcf8e2311db33a164816db20f`** (13:02:35Z) |
| base | `origin/master` **`bb7013c7669da19304a8769e5b25f8c1f8951e9c`** — drift ĐÃ ĐÓNG bằng merge `1db6af2` |
| lease gen 1 | `windows-lease-suite-exec-1-claude-20260911`, HẾT `2026-09-12T14:05:00Z` |
| spec đóng băng | `ops/specs/WINDOWS-LEASE-SUITE.md` sha256 `6af324a368550eda667c67315052cf4fe1a1fb861e2c0da77202163deb34d105` |
| write set (exact, 2 đường) | `ops/lease_publish_test.py` · `ops/chay_lease_publish_test.sh` |
| vòng review đã dùng | **6/10** — vòng 7 là vòng kế tiếp |

## Hai commit của lượt này

- `1db6af2` merge `origin/master` (`bb7013c`). **Đo:** merge KHÔNG đổi một byte nào của write set —
  `8bcc2293…35ea` và `87c76029…b693` giữ nguyên, khớp `reviewed_files_sha256` của verdict vòng 6.
  5 commit master mới chạm `RELEASE_MANIFEST.json`, `scripts/tl_core/release.py`, `scripts/tl_selftest.py`
  ⇒ **không** kích `S5`.
- `36f68c7` áp NGUYÊN VĂN `HINT.rvwin512-6.patch` (`e7cbefc7…1ee0`), `patch -p0 --fuzz=0`, +32/−13,
  một tệp. Đóng **F2** và **F7**.

## Đã đo trên `36f68c7`

| phép đo | kết quả |
|---|---|
| `AL_VER=1.7.7 AL_DICH=/tmp/actionlint bash ops/chay_lease_publish_test.sh` | `155/155 đạt; đã chạy=155, bỏ qua=0` ở **`[A]` (dòng 1055) · `[B]` (1060) · CHA (1156)**; 0 dòng `  ĐỎ  `; rc=0 |
| `t125` · `t158` · `t160` (CHA) | `55.445s QUA` (1061) · `3.381s QUA` (1146) · `0.066s QUA` (1148) |
| catalogue 16 đột biến, bằng **bộ đo ĐÃ VÁ** | `16/16 giết thật, 0 tín dụng giả, 0 sống sót`, rc=0 |
| tự kiểm bộ đo, **hai chiều** | bản CŨ `2/4` rc=1 · bản MỚI `4/4` rc=0 |
| `doctrine-scan --root .` | rc=0, `7 tệp, 0 chỗ chép doctrine` |
| `adr-song --root .` | rc=0, `47 ADR / 47 dòng §20` |
| `git diff --numstat origin/master...HEAD` (2 đường) | **+1101 / −27** (`1095` + `6`) ⇒ `1101 ≤ 1500`, dư **399** |

> **ĐÍNH CHÍNH `N32-b` (vòng 8).** Bản đầu của hàng trên ghi `+1114/−27`, số hạng `1076+32`, dư `386`.
> **Cả ba sai.** Số hạng thật: Python **1095**, shell **6**, tổng **1101**, dư **399**. HINT `+32/−13`
> thay thế 13 dòng vốn đã là dòng THÊM của chính PR, nên cột "thêm" tăng **19**, không 32.
> `418` (trong lease gen 1) là dư của head CŨ `353eae1` = `1500 − 1082` — đúng ở chỗ của nó.
> Bài học: **hai quan hệ `1101 ≤ 1500` và `1101 > 300` vẫn ĐÚNG trong khi CẢ HAI số hạng đã SAI.**
> Nó sống sót qua vòng 7 vì vòng 7 chỉ điểm danh con số nằm trong thông điệp commit, không quét tệp này.


### ĐIỀU KIỆN ĐO — đọc trước khi so số

Lượt **đầu** trong container này cho **153/155**: `t137` và `t159` ĐỎ, cả hai với lý do
*"KHÔNG ĐO ĐƯỢC: thiếu `shellcheck` — actionlint IM LẶNG bỏ toàn bộ luật shell khi vắng nó"*.
Đó là cổng **fail-close đúng thiết kế**, KHÔNG phải hồi quy của HINT. Cài `shellcheck 0.9.0` rồi đo lại
⇒ `155/155`. Log của **cả hai** lượt có trong thư mục này (`suite-36f68c7-THIEU-shellcheck.log` là lượt
thiếu công cụ). Nền của con số `155/155`: `actionlint 1.7.7` + `shellcheck 0.9.0`, Linux, python 3.11.15.

Bài học kèm theo: một con số trong tài liệu không ghi ĐIỀU KIỆN ĐO thì sẽ trôi mà không ai biết.

## Bảy lớp — trạng thái sau lượt này

| lớp | trước (vòng 6) | sau `36f68c7` | căn cứ |
|---|---|---|---|
| F1 thu hồi cả cây | ĐÃ VÁ THẬT | giữ nguyên | — |
| F3 selector | ĐÃ VÁ THẬT | giữ nguyên | — |
| F4 ngân sách tổng | ĐÃ VÁ THẬT | giữ nguyên | — |
| F5 tắt đệm con | ĐÃ VÁ THẬT | giữ nguyên | — |
| **F2** bằng chứng sống | VÁ HỜ, P1 | **đã áp HINT** | t160 nay đòi đủ 4 cặp `(tệp, nhãn)` tee tại consumer |
| **F7** phản chứng nối dây | VÁ HỜ, P1 | **đã áp HINT** | nhãn A/B, mẫu số, cấm `run` VÀ `Popen`, đo cả hai chiều `cap`/`cap[::-1]` |
| **F6** bộ đo cấp tín dụng giả | VÁ HỜ, P1 | **ĐÃ VÁ phần đo được · CÒN NỢ phần chống giả mạo tín hiệu** | `F6-HO-SO.md` |

**Trạng thái F2/F7 ở trên là "ĐÃ ÁP HINT", KHÔNG phải "ĐÃ VÁ THẬT".** Phân biệt này quan trọng: HINT do
reviewer soạn và tự kiểm trên cây của họ; lượt này chỉ chứng minh nó **áp sạch và suite xanh**.
Ai tuyên "đã vá thật" thì phải là vòng 7, sau khi chạy lại `N01`–`N18`. Catalogue `N01`–`N18` là của
**reviewer**, KHÔNG có trong kho — lượt này chỉ chạy lại được catalogue 16 mutant của tác giả.

## F6 — nói cho đúng phạm vi

Đo lại ra **HAI** thể hiện chứ không phải một (vòng 6 khai một): regex đòi **ít nhất một ký tự** trước
`Error|Exception`, nên `Exception:` trần **và** `Error:` trần đều lọt và được cấp `GIET THAT`.
Một lỗ gốc, hai đường vào — vá theo LỖ, không theo danh sách thể hiện reviewer liệt kê.

Vá: tiền tố thành **tuỳ chọn**. Răng: 4 `CONTROL` biết trước đáp án, chạy `--tu-kiem`; phản chứng là bản
`dotbien512_REGEX_CU.py` khác **đúng một dòng** ⇒ `2/4`, rc=1.

**CÒN NỢ, không được đọc thành đã đóng:** bộ đo chạy NGOÀI tiến trình và chỉ đọc CHUỖI, nên một
`except Exception as e: raise AssertionError(f"…{type(e).__name__}")` trong tệp test vẫn giả được tín hiệu.
Đóng hẳn đòi `main()` phát dấu riêng cho một lớp tín hiệu (`TinHieuChotCa` đã có ở
`ops/lease_publish_test.py:4328` nhưng chỉ dùng cho khối A0/`t139`, và `main()` bắt `AssertionError` rồi
in `str(ex)` nên danh tính lớp CHẾT ngay tại đó) ⇒ **thay đổi write set** ⇒ đề xuất chủ kho, không tự làm.

## Nợ có tên, chưa chữa

- **`A3`/`A4` chưa đo trên `36f68c7`** — không lượt Windows nào chạy, theo chỉ thị chủ kho (không CI tay;
  full CI khi merge). **Đừng đọc Linux `155/155` thành `A3` đạt.**
- **`S8-bo-deadline` chập chờn** — gốc trong `ops/lease_publish.py` = NGOÀI write set ⇒ chạm là `S3`.
- **Rò `GITHUB_ACTOR` vs ca chập chờn** — `KHÔNG ĐO ĐƯỢC`, không phải "đã loại trừ".
- **`SO-CANON-CHUA-TON-TAI`** — `grep -rln "review_rounds_used" --include=*.py .` ⇒ **0 tệp**.
  Trần 10 vòng KHÔNG có cổng nào canh; đếm vòng là đếm TAY.
- **F6 residual** ở trên.
- **Verdict vòng 1–5 ĐÃ MẤT** cùng container cũ, chưa từng vào kho — mất mát thật của hồ sơ
  (nợ ADR-0034), phải khai trong PR hồ sơ, không im lặng cho qua.

## `A5` — đừng biến thành ô tích xanh

Đặc tả đóng băng vẫn ghi `A5 ≤ 300` và **KHÔNG được sửa** (`§3.2`). `1101 > 300` (đính chính `N32-b`;
bản đầu ghi `1114`). Trạng thái đúng:
**"KHÔNG ĐẠT ở ngưỡng 300, được chủ kho OVERRIDE lên 1500"**.

## Hạ tầng — đã đo trong container NÀY

- `codex` `--kiem-song` ⇒ **rc=0 (VẪN dùng được)**, dù ảnh chụp `CODEX_AUTH_JSON` đã **69,3h** và nhãn
  tổng hợp vẫn in `SAP_HET_HAN`. Đọc CHI TIẾT, đừng đọc nhãn.
- `claude` **CHƯA_XAC_THUC** trong container này (không có `~/.claude/.credentials.json`, không có biến)
  ⇒ lane reviewer Claude không dùng được; reviewer đi bằng `codex`.
- `gh` **vắng**, và cài cũng vô ích (đi đúng đường proxy chặn). GitHub đi bằng **MCP + git**.
- `shellcheck` **vắng sẵn** trong container ⇒ phải tự cài, xem §ĐIỀU KIỆN ĐO.
- **Thông báo "background command completed (exit code 0)" của harness là vỏ shell nền thoát, KHÔNG phải
  lượt chạy xong.** Đã gặp hai lần trong lượt này. Đo bằng `pgrep` + đếm `<<< ra` + chờ dòng `SUITE_RC=`.

---

# CẬP NHẬT 13:40Z — VÒNG 7 ĐÃ XONG

`VERDICT.rvwin512-7.md` sha256 **`f3604ab0be75919e5146bd5ccaf6dc738cc73b19d10e8714f6243ecc0d363d4e`**
(hiện vật trong thư mục này — vòng 1–5 đã mất, vòng 6–7 nay CÓ trong git).

`verdict: changes_requested` · `so_p1: 1` · `so_p2: 0` · `so_p3: 0` · `so_the_hien: 38`
`reviewed_sha: 36f68c7` · `reviewed_base: bb7013c` · không nộp HINT.

Lượt chạy: phóng 13:10:20Z, `XONG VERDICT` 13:25:15Z ⇒ **895 s = 14 phút 55 giây**, 24 280 byte,
**0** chữ ký mất mạng.

> **ĐÍNH CHÍNH `N37` (vòng 8).** Bản đầu ghi *"~8,5 phút"*. Hiệu hai mốc là **895 s ≈ 14,92 phút**.
> Nguồn của `8,5`: bộ theo dõi in `~510s`, nhưng `510s` đếm **từ lúc bộ theo dõi bắt đầu**, không
> từ lúc phóng. Tôi lấy số của một đồng hồ rồi gán cho khoảng của đồng hồ khác — đúng bệnh
> **ghép sai lượt** mà `CLAUDE.md` đã tố cáo. Hai mốc `13:10:20Z`/`13:25:15Z` là **tự khai**,
> chưa chứng thực độc lập; điều sai ở đây là chính **phép trừ nội tại**.
Container KHÔNG recycle lần này — khác hẳn vòng 6 (phóng bốn lần).

## Bảy lớp sau vòng 7

| lớp | trạng thái canonical | căn cứ reviewer |
|---|---|---|
| F1 · F3 · F4 · F5 | **ĐÃ VÁ THẬT**, không thoái lui | control mỗi ca `1/1`; mutant chết đúng chốt (phạm vi POSIX, **không** ngoại suy Windows) |
| **F2** | **ĐÃ VÁ THẬT** | `N10` SỐNG ở `353eae1`, CHẾT ở `36f68c7` với `consumer t125 phải nối đủ bốn tệp vào đúng tee: []` |
| **F7** | **ĐÃ VÁ THẬT** | `N01 N02 N12 N17 N18` — **5/5** SỐNG ở `353eae1`, **5/5** CHẾT đúng chốt ở `36f68c7`. (ĐÍNH CHÍNH `N38`: bản đầu ghi `6/6` cho F7; tập ấy có **năm** phần tử — `6` là tổng F2+F7, vì `N10` thuộc **F2**.) |
| **F6** | **VÁ HỜ, P1** | `F6.5` `StopIteration` vẫn được cấp `GIET THAT` · `F6.6` lời khai gói log không khớp · `F6.N01–N36` số bảng EVIDENCE bỏ sót |

**`so_the_hien: 38` KHÔNG phải 38 lỗi thực thi** — reviewer nói rõ: 36 trong số đó là các con số bảng
`EVIDENCE` bỏ sót, tính riêng **theo đúng lời mời của tác giả**, và phần lớn đo lại **khớp**. Lỗi số thật
chỉ có hai: `N31` và `N32` (xem dưới).

## Đã xử sau vòng 7

- **F6.5 — ĐÃ VÁ, bằng cách ĐẢO CHIỀU phép đo** (không thêm tên vào danh sách): đo **hình dạng mà
  `main()` in ra** thay vì đoán tên ngoại lệ, cộng chốt **fail-close** cho chính hợp đồng in ấy.
  Ba phép đo trong `F6-HO-SO.md` §CẬP NHẬT SAU VÒNG 7. Bản mới **7/7** rc=0; bản vá vòng 6 trên **cùng
  7 control** ⇒ **5/7** rc=1; đổi hợp đồng in ⇒ bộ đo **TỰ CHẶN** rc=1; catalogue đo lại **16/16**,
  không ca nào đổi phân hạng.
- **F6.6 — ĐÍNH CHÍNH lời khai**, không sửa mã: log `153/155` **có thật và ở trong kho**
  (`suite-36f68c7-THIEU-shellcheck.log`); lỗi ở khâu **đóng gói sandbox**, không phải hiện vật thiếu.
- **`N31` — lỗi thật trong thông điệp commit `36f68c7`**: tiêu đề ghi *"5 mutant sống"*, trong khi chính
  thân commit liệt kê **SÁU** (`N01 N02 N10 N12 N17 N18`). Con số `5` chép lại từ `TRANG_THAI` vòng 6 mà
  không đếm. Đính chính bằng hồ sơ; **không** sửa lịch sử.
- **`N32` — `dư 386` SAI**, đúng là **`dư 399`** (`1500 − 1101`). `386` chỉ đúng với con số `1114` mà
  chính tôi đã thừa nhận sai. `418` của lease gen 1 là dư của head CŨ `353eae1` (`1500 − 1082`) — **đúng ở
  chỗ của nó**, không kéo sang head mới.

## `KHÔNG ĐO ĐƯỢC` mà vòng 7 khai — đọc trước khi tin bất cứ ô xanh nào

- **Reviewer KHÔNG chạy được full wrapper**: installer `actionlint` `rc=4`, sandbox không ra mạng. Nên
  ba tổng kết `CHA/A/B` của **lượt reviewer độc lập** là `KHÔNG ĐO ĐƯỢC`. Reviewer **không** mượn log của
  tác giả, không mượn `rc=0` của script bọc, không mượn control `1/1` để thay. Đúng kỷ luật.
- **`doctrine-scan 7/0` và `adr-song 47/47` tại HEAD**: `KHÔNG ĐO ĐƯỢC` từ phía reviewer — hai lệnh ấy đòi
  đọc `CLAUDE.md`/`PROTOCOL`/`AGENTS`/`skills`, đều nằm trong danh sách CẤM ĐỌC của prompt. Reviewer từ
  chối nhận lời khai làm sự thật. **Đây là chi phí có thật của ràng buộc cấm đọc** — nên biết mà tính.
- **Windows / `A2` `A3` `A4` / ngưỡng 15 phút**: `KHÔNG ĐO ĐƯỢC`. Các mốc thời gian Windows trong docstring
  (`N07` `N11`–`N15` `N17` `N18` `N30`) **thiếu log nguồn trong kho** — đó là nợ hồ sơ có thật.
- **`A5`**: `KHÔNG ĐẠT` — `1101 > 300`. Override lên 1500 **không đổi nhãn nghiệm thu đóng băng**.
- **Phần chống giả mạo tín hiệu của catalogue**: `KHÔNG ĐO ĐƯỢC đầy đủ`; reviewer **không tự soạn mã giả
  mạo**, đúng ràng buộc đã giao. `F6.5` đo ngoại lệ không hậu tố, **không phải** phép giả mạo.

## Việc kế tiếp

- **Vòng 8** đã chạy ⇒ đã dùng **8/10** vòng. (ĐÍNH CHÍNH `N39`: bản đầu ghi *"sẽ là 7/10 sau khi phóng"* — `7/10` là trạng thái TRƯỚC lượt 8, sau khi phóng phải là **8/10**.)
- **Lease gen 2 ĐÃ SOẠN nhưng CHƯA ĐẨY**: nhánh `ops/cap-lease-504`, commit cục bộ, bia mộ **hai chiều**
  đã khớp, `lease_publish.py check` ⇒ **`ĐĂNG ĐƯỢC` rc=0**. Còn thiếu **đúng một thứ**: URL chỉ thị bền của
  chủ kho cho `granted_on_instruction` và `nang_tran.can_cu`. Cổng **không** xác thực trường ấy, nên để
  placeholder là mỏ neo BỊA — không đẩy.
  **Chú ý:** khối `nang_tran` của gen 1 tự bó phạm vi *"Chỉ lease …exec-1…, generation 1"*, nên gen 2
  **KHÔNG tự thừa hưởng** trần `S2=1500`; phải cấp LẠI. Đọc một override hết phạm vi thành còn hiệu lực
  chính là tự nâng trần.

---

# CẬP NHẬT — VÒNG 8 ĐÃ XONG, và F6 phải DỪNG VÁ

`VERDICT.rvwin512-8.md` sha256 **`62d71e818c2d753a00e2e682c8dd844c53fa9eef5f7dc77a0efe94dd5c3f0cb2`**.
`verdict: changes_requested` · `so_p1: 1` · `so_p2: 0` · `so_p3: 0` · `so_the_hien: 9` · không nộp HINT.
Lượt chạy: phóng 13:36:19Z → `XONG VERDICT` 13:49:51Z ⇒ **812 s = 13 ph 32 s**, 21 430 byte, **0** chữ ký
(ĐÍNH CHÍNH `N40` vòng 9: bản đầu ghi `813 s = 13 ph 33 s`; hiệu đúng là **812 s**.)
mất mạng. (Mốc đo từ `run.json`/`stat`, KHÔNG từ số của bộ theo dõi — xem `N37`.)

## PR: SẠCH. Lớp còn mở nằm NGOÀI nó.

| lớp | vòng 8 |
|---|---|
| F1 · F2 · F3 · F4 · F5 · F7 | **ĐÃ VÁ THẬT**, không thoái lui (phạm vi Linux; **không** ngoại suy Windows) |
| **F6** (ngoài write set) | **VÁ SINH LỖI MỚI** |

Lượt này reviewer **chạy được full wrapper độc lập** (nhờ gói `actionlint` offline đóng kèm — vòng 7
`rc=4` vì sandbox không ra mạng): **`155/155` ở CHA, `[A]` và `[B]`**, 0 đỏ, 0 bỏ qua. Đây là **ba tổng
kết dương của LƯỢT REVIEWER**, không phải log của tác giả. Và nhờ **ngoại lệ hẹp** cấp riêng cho lượt 8,
reviewer tự chạy được `doctrine-scan` (`rc=0`, `7/0`) và `adr-song` (`rc=0`, `47/47`) — hai cổng mà vòng 7
buộc phải trả `KHÔNG ĐO ĐƯỢC` chỉ vì lệnh của chúng đọc tệp trong danh sách cấm.

## F6 — BA LẦN VÁ, BA LẦN MỘT HÌNH DẠNG. Đây là chỗ phải dừng.

| lượt | bản vá | đường lọt lượt sau tìm ra |
|---|---|---|
| vòng 6 → 7 | cho tiền tố regex thành **tuỳ chọn** | `StopIteration` — không mang hậu tố `Error`/`Exception` |
| vòng 7 → 8 | đo **hình dạng `main()` in ra**, `^[A-Za-z_][A-Za-z0-9_]*…: ` | `F6.7` tên lớp **Unicode** (`Bùng`) · `F6.8` thông điệp **RỖNG** (`Exception: ` → `.strip()` → `Exception:` → trượt `: `) |
| — | — | **`F6.9` HỒI QUY**: chốt THẬT `t96: khớp đúng nghĩa…` bị xếp `TIN DUNG GIA`; bản vòng 6 nhận **đúng** |

`F6.9` là điều quyết định, và reviewer phát biểu đúng bản chất: **hai miền chuỗi *"thông điệp assertion"*
và *"tên lớp + thông điệp"* GIAO NHAU** — `t96: ` là tiền tố tên ca bình thường **đã có trong cây**, không
phải chuỗi do reviewer bịa. Nên *"nới regex thêm nữa không tự giải quyết được sự nhập nhằng ấy"*.

Cộng `F6.10`: chốt fail-close `_kiem_hop_dong_main` **có** răng khi còn nguyên, nhưng **tự kiểm không canh
việc nó bị gỡ** — bỏ lời gọi vẫn `7/7` và catalogue vẫn `16/16`. Tức tôi đã dựng một chốt rồi **không đo
chính chốt ấy**, đúng lỗi mà `CLAUDE.md` gọi là *"cửa không có mutant là cửa sẽ âm thầm hở lại"*.

**`CLAUDE.md` có đúng luật cho tình huống này:** *"Đếm HÌNH DẠNG lỗi, đừng chỉ đếm lỗi: cùng một hình
dạng lặp ba lần trở lên thì câu hỏi đúng là 'CÓ NÊN LÀM VIỆC NÀY KHÔNG', không phải 'vá thế nào'."*
Ba lượt, cùng một hình dạng: **suy LÝ DO một mutant chết bằng cách phân tích CHUỖI trên stdout.**
Kết luận: **kiến trúc sai, không phải bản vá sai.** Vá lần thứ tư sẽ mua thêm một thể hiện và một hồi quy.

### Đường đúng — và nó đòi THẨM QUYỀN, nên phiên này DỪNG

Cho `main()` phát một **dấu riêng, không giả được**, cho một LỚP TÍN HIỆU của ca đích, để bộ đo **không
phải phân biệt chuỗi** nữa. Kho **đã có** `TinHieuChotCa(AssertionError)` (`ops/lease_publish_test.py:4328`)
với đúng chú thích *"không `except` nào trong mã sản phẩm hay fixture dựng được nó"* — nhưng nó chỉ dùng
cho khối `A0`/`t139`, và **`main()` bắt `AssertionError` rồi in `str(ex)`** nên danh tính lớp **chết ngay
tại đó**.

Đó là **thay đổi write set** (`ops/lease_publish_test.py`) ⇒ cần lease còn hiệu lực **và** quyết định của
chủ kho, vì nó mở rộng phạm vi packet ở vòng 8/10. Lease gen 1 hết `2026-09-12T14:05:00Z`; gen 2 đã soạn
nhưng **chưa đẩy** (thiếu URL chỉ thị). **Phiên này KHÔNG tự làm.**

Ba lựa chọn để chủ kho chọn, xếp theo mức xâm phạm:
1. **Dời F6 sang packet RIÊNG.** `dotbien512.py` là bộ đo, không phải sản phẩm; F6 chưa từng chặn PR #512
   ở bất kỳ vòng nào. PR #512 có thể land với F6 khai thành nợ có tên.
2. **Cấp gen 2 + cho phép sửa `main()`** để phát dấu riêng ⇒ đóng F6 theo KIẾN TRÚC, nhưng thêm dòng vào
   write set ở vòng 8/10 và đòi một vòng review nữa.
3. **Chấp nhận bộ đo ở trạng thái vòng 6** (đóng `Exception`/`Error` trần, nhận đúng chiều chốt thật) và
   khai ba thể hiện còn lại là nợ. Bản vòng 8 của tôi **tệ hơn** bản vòng 6 ở chiều dương (`F6.9`), nên
   nếu chọn hướng này thì phải **lùi** về `dotbien512_VA_VONG6.py`, không giữ bản mới.

**Khuyến nghị: (1).** F6 là công cụ đo, nằm ngoài write set, và ba vòng liền nó là lớp P1 duy nhất giữ
một PR mà mọi lớp sản phẩm đã `ĐÃ VÁ THẬT` và CI xanh. Giữ nó trong packet này là để một khuyết tật của
**thước đo** chặn một **bản vá đã được thước đo ấy chứng minh là tốt**.

---

# CẬP NHẬT 14:5xZ — hai quyết định của chủ kho ĐÃ THI HÀNH

Chỉ thị: phiên chat 12-09-2026, nguyên văn `"1. theo khuyến nghị"` / `"2. đẩy đi"`; mỏ neo bền
**#504 comment `5646460376`** (comment ấy do phiên GHI HỘ và KHAI RÕ điều đó trong chính nó).

## (2) Lease generation 2 — ĐÃ ĐĂNG

`windows-lease-suite-exec-2-claude-20260912`, commit `876bdc9` nhánh `ops/cap-lease-504`.
Marker do `github-actions[bot]` đăng: **#504 comment `5646489814`**, mở đầu đúng vị từ
`**Lease <id>**`. `ai-dang-giu` trên **cả hai** đường ⇒ `NGƯỜI_GIỮ 1` = gen 2. Hạn `2026-09-13T14:22:00Z`.

**Đã sửa hai thứ trong bản nháp trước khi đẩy:**
- bản nháp ghi `leased_at_utc: 13:20:00Z` — **lùi ngày** so với lúc chỉ thị đến. Re-time về `14:22:00Z`.
- `granted_on_instruction` / `nang_tran.can_cu` là placeholder ⇒ neo vào comment thật. Cổng `check`
  **không** xác thực trường ấy, nên nó là kỷ luật của người ghi, không phải của cổng.

**Trần `S2=1500` phải CẤP LẠI cho gen 2**, không tự thừa hưởng: khối `nang_tran` của gen 1 tự bó
*"Chỉ lease …exec-1…, generation 1"*.

### Lượt workflow đăng lease ĐỎ — và vì sao đó KHÔNG phải lỗi của gen 2

Run `34699156658` `conclusion: failure`. Đọc log thay vì suy: workflow lặp qua **mọi** tệp lease đổi
trong push, và commit chạm **hai** tệp.

| tệp | kết quả |
|---|---|
| `…exec-2…yaml` (gen 2) | `hai lớp GitHub ĐÃ QUA` · `ĐĂNG ĐƯỢC` · `đã đăng comment 5646489814` |
| `…exec-1…yaml` (gen 1, chạm chỉ để mang bia mộ) | `CHAN [8]: lease đã hết hạn lúc 2026-09-12T14:05:00+00:00` |

Từ chối ấy **ĐÚNG** — *"đăng một lease chết thì người nhận tưởng có quyền mà không có"*. Nhưng nó làm cả
lượt `exit 1`. **Nợ mới, chưa chữa:** thêm bia mộ vào một lease **đã hết hạn** thì workflow đăng lease sẽ
thử đăng lại nó và ĐỎ. `.github/workflows/**` **ngoài write set** (`S3`) ⇒ khai nợ, không sửa.

## (1) F6 — ĐÃ DỜI sang packet riêng

- Nợ: `ops/NO_KY_THUAT.md` **§23** `BO-DO-DOT-BIEN-SUY-LY-DO-CHET-TU-CHUOI-STDOUT`.
- Issue packet: **#530** · spec đóng băng `ops/specs/CHAM-DOT-BIEN-MIEN-NHIEM-LEASE-SUITE.md`
  sha256 `5fcc14b5e33ecf130172bc1cafbb0ca229ddae8363069284eba5fcca49602781`. **Chưa có lease.**
- **Hoá ra là một PORT**: kiến trúc đã land ở **#513** (closed-completed), và `#513` loại
  `ops/lease_publish_test.py` khỏi phạm vi **vì một packet KHÁC đang giữ nó**. F6 là hệ quả đoán được.

  > **ĐÍNH CHÍNH `N42` (vòng 9).** Bản đầu ghi *"vì `#504` giữ nó"* — **dẫn sai chủ thể**. Tệp spec thật
  > (`ops/specs/CHAM-DOT-BIEN-MIEN-NHIEM-CA-VO-CAN.md:129`) ghi **`#503`** giữ, lease
  > `m9-fetch-auth-exec-1-claude-20260911`, và phân việc `t125` sang packet `T125-RA-JOB-RIENG`.
  >
  > **Và có một chỗ lệch đáng báo, không phải lỗi của tôi:** thân **Issue `#513`** ghi
  > `ops/lease_publish_test.py (#504 giữ)`, còn **tệp spec** ghi `#503`. Hai hiện vật của cùng một packet
  > **nói khác nhau**. Tôi chép theo Issue rồi **quy cho tệp spec** — đó là lỗi dẫn nguồn của tôi. Nhưng
  > việc hai hiện vật lệch nhau là chuyện của `#513`, nên khai ra đây để người giữ biết.
  >
  > Điều **không** đổi: exclusion có thật, và `ops/lease_publish_test.py` bị loại khỏi phạm vi `#513` vì
  > một lease của packet khác đang giữ nó. Suy luận *"F6 là hệ quả của một write-set exclusion"* đứng
  > vững; chỉ **chủ thể** của exclusion là `#503`, không phải `#504`.

### Bản bộ đo mặc định — chọn BẰNG PHÉP ĐO, và phép đo BÁC dự đoán của kế hoạch

Kế hoạch dự đoán sẽ **lùi về `v6`**. Đo trên **10 control** (bộ 7 ca cũ **thiếu** hai ca vòng 8 đã tìm
ra) ⇒ **giữ `v8`**:

| bản | đúng | lọt | hồi quy |
|---|---|---|---|
| `v0` | `4/10` | 6 | 0 |
| `v6` | `7/10` | 3 | 0 |
| **`v8` (mặc định)** | `7/10` | **2** | **1** |

Lý do quyết định: **cả BỐN** lớp ngoại lệ của chính kho — `BoQuaNen`, `Chan`, `HetNganSachDay`,
`TinHieuChotCa` — đều thiếu hậu tố `Error`/`Exception`.

> **ĐÍNH CHÍNH vòng 9 (`F6.11`, `F6.12`) — hai con số trên SAI, và đây là chỗ tôi sai nặng nhất lượt này.**
> Tôi khớp regex với chuỗi **tự ghép** thay vì **chạy lớp thật qua `main()`**. Chạy thật:
> `main()` có **BA** nhánh — `except BoQuaNen` in chuỗi **cố định** nên `BoQuaNen` **lọt cả hai bản**; và
> `TinHieuChotCa` là con của `AssertionError` nên cũng lọt cả hai — mà **đếm nó vào đây vốn đã sai**, vì nó
> **LÀ** lớp tín hiệu. Nên `v8` loại **2/4**, không phải `4/4`; trên **ba** lớp vô can thật thì `v6` lọt
> **3/3**, `v8` lọt **1/3**.
> Và **biên `8/454` không tồn tại**: mẫu số thật **493**, bộ lọc bỏ **39** lời gọi tiền tố ĐỘNG; trong đó
> **21** mang hình dạng va chạm `f"{x}: …"` trên **7 ca nữa** (`t23 t26 t27 t126 t127 t131 t133`) ⇒
> **≥29 lời gọi / ≥10 ca**, phần lớn **không quyết định được tĩnh**. **RÚT** lời khai "có biên": cả hai bản
> đều có miền khuyết tật **không có biên**, chỉ ngược chiều. Giữ `v8` là lựa chọn trên **một mẫu đã đo**,
> KHÔNG phải phép chứng minh tối ưu.

Bộ đo được giao ở trạng thái **TỰ BÁO ĐỎ** (`7/10`, `rc=1`) — **cố ý**: bộ control kèm cả ba ca nó xử
sai, nên mỗi lần tự kiểm là một lần khuyết tật tự khai.

### Một bài học về PHÉP ĐO của chính lượt này

Phép đo `8/454` và `4/4` ở trên có một lần bị chạy **trên cây SAI** — đang đứng ở nhánh hồ sơ (nền
`master`, `147` ca) thay vì `36f68c7` (`155` ca, có `t153`–`t160`). Lộ ra vì `t153`–`t160` **không tồn
tại** trong kết quả. Chữa bằng cách **ghim BLOB** (`git show 36f68c7:…`) thay vì tin nhánh đang checkout.
Và lần ghim ấy còn sửa một con số đã đẩy: lớp ngoại lệ là **4**, không phải 3 — bộ lọc base class đầu bỏ
mất `HetNganSachDay`.

## Việc còn lại

- **Vòng 9** — phạm vi là hai đường write set, nhưng **KHÔNG đóng khung lớp lỗi cho reviewer**: phát hiện
  ngoài write set **vẫn báo**, đánh dấu là **nợ**. Sẽ là **9/10**.
- Sau `approve` ⇒ merge, rồi **ĐỌC** lượt CI hậu merge (lần đo Windows **đầu tiên** của mã này).
  **Không** CI bằng tay ở bất kỳ giai đoạn nào.
