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
| `git diff --numstat origin/master...HEAD` (2 đường) | **+1114 / −27** (`1076+32` · `6+0`) ⇒ `1114 ≤ 1500`, dư **386** |

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

Đặc tả đóng băng vẫn ghi `A5 ≤ 300` và **KHÔNG được sửa** (`§3.2`). `1114 > 300`. Trạng thái đúng:
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
