# Trạng thái bàn giao — PR #512 / packet #504 WINDOWS-LEASE-SUITE, sau vòng review 6

Soạn 11:20Z 12-09-2026 bởi phiên `claude` (Opus 5) `session_01Lnos1VZ4KSzHLG9u4UETiW`.
**Thư mục này tồn tại vì hiện vật review sống trong scratchpad EPHEMERAL của container.** Container bị
recycle nhiều lần trong ngày (đo được: uptime 1,3 / 0,6 / 4,9 / 8,5 phút ở bốn thời điểm), nên mọi thứ
phiên sau cần phải nằm trong **git**, không nằm trong `/tmp`.

## Neo

| | |
|---|---|
| PR | #512 · nhánh `claude/windows-lease-suite` |
| head ĐÃ ĐẨY | **`353eae10120da2a1788dcaf7a906fe46261bd71b`** |
| base | `origin/master` **`015ffcc09d76fbc9cdfbc3d2ee0735c3ead8d364`** |
| Packet Issue | #504 · Mission #499 |
| lease | `windows-lease-suite-exec-1-claude-20260911`, gen 1, nhánh `ops/cap-lease-504` |
| **lease HẾT HẠN** | **`2026-09-12T14:05:00Z`** — sau mốc này cần generation mới, bất kể trần nào |
| spec đóng băng | `ops/specs/WINDOWS-LEASE-SUITE.md` sha256 `6af324a368550eda667c67315052cf4fe1a1fb861e2c0da77202163deb34d105` |
| write set (exact, 2 đường) | `ops/lease_publish_test.py` · `ops/chay_lease_publish_test.sh` |

## Đã đo trên `353eae1` — con số, kèm điều kiện đo

| phép đo | kết quả |
|---|---|
| `AL_VER=1.7.7 AL_DICH=/tmp/actionlint bash ops/chay_lease_publish_test.sh` | `lease_publish: 155/155 đạt; đã chạy=155, bỏ qua=0` ở **phiên cha** VÀ cả hai vế `[A]`/`[B]` (log: `suite-353eae1-linux.log`, dòng 1055 · 1060 · 1156) |
| `t125` · `t160` | `72.143s QUA` (dòng 1061) · `0.038s QUA` (dòng 1148) |
| catalogue 16 đột biến | `16/16 giết thật, 0 tín dụng giả, 0 sống sót` — **NHƯNG xem F6 dưới đây** |
| `packet_loop.py doctrine-scan --root .` | rc=0, `7 tệp, 0 chỗ chép doctrine` |
| `packet_loop.py adr-song --root .` | rc=0, `47 ADR / 47 dòng §20` |
| `git diff --numstat origin/master...HEAD` (2 đường write set) | **+1082 / −27** |
| CI tự động trên `353eae1` | `gate (ubuntu-latest)` **success** (09:34:22Z→10:09:11Z) · `thu-hoi` **success** · `mo` skipped |

## Trần và điều kiện dừng — trạng thái HIỆN TẠI

| trục | trần | trạng thái |
|---|---|---|
| `S2` dòng thêm | **1500** (nâng từ 300) | `1082 ≤ 1500`, dư **418**. Khối `nang_tran` ở `ops/leases/windows-lease-suite-exec-1-claude-20260911.yaml`, commit **`2d0ee53`** nhánh `ops/cap-lease-504`; chỉ thị chủ kho ở #504 comment `5645151563`; `lease_publish.py check` rc=0 |
| `S6` vòng review | **10** (nâng từ 2) | đã dùng **6**, còn **4** |
| `S1` đường dẫn thứ ba | — | chưa chạm |
| `S3` ca treo trong `ops/lease_publish.py` | — | chưa chạm. **Nợ `S8-bo-deadline` nằm ĐÚNG ở đó** ⇒ không sửa, khai nợ |
| `S4` skip/cách ly/nâng `timeout-minutes` | — | **CẤM tuyệt đối**, không có ngoại lệ |

**`A5` của đặc tả đóng băng vẫn ghi `300` và KHÔNG được sửa (`§3.2`).** Trạng thái đúng của `A5` là
*"KHÔNG ĐẠT ở ngưỡng 300, được chủ kho OVERRIDE lên 1500"* — **không** phải "A5 đạt". Đừng viết nó thành
một ô tích xanh ở bất kỳ hồ sơ nào.

## Vòng 6 — kết quả

`VERDICT.rvwin512-6.md` sha256 **`ea5b5205e4af786de41ae1a15fa7f41ac39849c5e6dd01173ae00a0885f39246`**
(đo trên tệp, khớp dòng `XONG VERDICT` của lượt chạy).
`verdict: changes_requested` · `so_p1: 3` · `so_p2: 0` · `so_p3: 0` · `so_the_hien: 5`.

`HINT.rvwin512-6.patch` sha256 **`e7cbefc7d9b11c6dae94bae5d0b04ad15ef9e404ad41564b0466feae6d751ee0`**.
Đã tự kiểm: chỉ chạm `ops/lease_publish_test.py`; `patch -p0 --dry-run --fuzz=0` từ gốc cây kho ⇒ **rc=0**.
**CHƯA ÁP** — head `353eae1` là head TRƯỚC HINT.

### Bảy lớp

| lớp | trạng thái | nội dung |
|---|---|---|
| F1 thu hồi cả cây | **ĐÃ VÁ THẬT** | — |
| F3 selector | **ĐÃ VÁ THẬT** | — |
| F4 ngân sách tổng | **ĐÃ VÁ THẬT** | — |
| F5 tắt đệm con | **ĐÃ VÁ THẬT** | — |
| **F2 bằng chứng sống** | **VÁ HỜ, P1** | `N10` thay danh sách luồng tee ở `t125` bằng `[]` ⇒ `t158` xanh, full wrapper **CHA 155/155**, **không dòng `[A]`/`[B]` nào**. Lỗ ở CALLER; HEAD thật vẫn tee đúng |
| **F6 bộ đo cấp tín dụng giả** | **VÁ HỜ, P1** | `dotbien512.py:123` chỉ nhận một số tên ngoại lệ theo tiền tố ⇒ control ném `Exception('CONTROL unrelated to A/B')` **được tính GIẾT THẬT**, còn `RuntimeError` bị loại đúng. **Ngoài write set** ⇒ hồ sơ riêng, KHÔNG nhét vào HINT |
| **F7 phản chứng nối dây** | **VÁ HỜ, P1** | 5 mutant SỐNG: `N01`/`N02` đảo nhãn A/B mà `t160` vẫn qua (chỉ so chuỗi, không gắn nhãn) · `N17`/`N18` bỏ mẫu số ⇒ consumer nhận `A 1/2` và `B 1/3` là khớp · **`N12` hồi sinh tầng retry bằng `Popen`/PIPE** (không nhóm/tee/ngân sách) mà `t160` và full wrapper vẫn xanh. `N11` cùng đường nhưng dùng `run` thì CHẾT đúng chốt. `N09` là mutant TƯƠNG ĐƯƠNG, reviewer tự loại — không tính finding |

### F6 nói cho ĐÚNG, vì nó nhắm vào lời khai của chính phiên trước

Phiên trước khai *"16/16 GIẾT THẬT, 0 tín dụng giả"*. Reviewer **không bác** con số ấy — nguyên văn:
*"không suy 16 mutant tác giả là giả — 16 log thực đã có đúng chốt"*. Thứ bị bác là **công cụ chứng
nhận**: nó sẽ cấp tín dụng cho một ngoại lệ vô can nếu gặp. Nên câu đúng là **"16 mutant ấy chết đúng
lý do, nhưng bộ đo chứng nhận chúng không đủ răng"**. Đừng viết mạnh hơn (thành "16 mutant là giả") và
cũng đừng viết nhẹ hơn (thành "bộ đo ổn").

## Lịch sử bốn lần phóng vòng 6 — và bài học vận hành đã trả giá

| lượt | kiểu | sống | `VERDICT.md` đạt được |
|---|---|---|---|
| `cdeee323` | phóng nguội | 15,5 ph | 1 089 B (`in_progress`) |
| `dab09336` | phóng nguội | 4,9 ph | — |
| `0e9efceb` | `codex exec resume` | ~7 ph | **11 688 B** |
| `759cad8a` | `codex exec resume` | trọn, `ma_thoat=0` | **18 888 B**, chốt verdict + HINT |

Ba lần chết đều cùng chữ ký: `responses_websocket: Connection refused (os error 111)` →
`Reconnecting... 3/5`, và `ma_thoat: None` (tức **`launcher.py` cũng bị giết** ⇒ container chết, không
phải codex bỏ cuộc). Đĩa còn 14G, RAM còn 15G ⇒ **KHÔNG** phải áp lực tài nguyên. Nguyên nhân recycle:
**KHÔNG ĐO ĐƯỢC từ bên trong** — đừng chế ra một nguyên nhân.

**Hai thứ chữa được, và cả hai có tác dụng ĐO ĐƯỢC:**

1. **`codex exec resume <session-id>`** giữ nguyên ngữ cảnh (rollout file lên 2,19 MB) nên không phải
   đo lại từ đầu. Bẫy cú pháp đã trả giá một `rc=2`: **`resume` KHÔNG nhận `-s` và `-C`** — sandbox phải
   đi qua `-c sandbox_mode=workspace-write`, và cwd phải `cd` TRƯỚC khi `exec`.
2. **Chỉ thị "ghi `VERDICT.md` SAU MỖI PHÁT HIỆN, không phải ở cuối"** — đây là thứ biến một lần chết từ
   *mất cả lượt* thành *mất một finding*. Con số chứng minh: 1 089 → 11 688 → 18 888.

`run.json` khai `trang_thai: dang_chay` cho cả ba lượt đã chết. **Đó là lời khai dối đã biết của công
cụ.** Ba phép đo phân biệt được, và cần cả ba: `ps -p <pid>` · mtime của `VERDICT.md` ·
`grep -E 'Connection refused|Reconnecting'` trong `stderr.log`.

## Nợ có tên, chưa chữa

- **`S8-bo-deadline` chập chờn** — lượt CI đỏ trên `e6feddb` chết vì mutant ấy sống sót ở seam
  `KhoObject._con_thoi_gian`. Gốc trong `ops/lease_publish.py` = **NGOÀI write set, chạm vào là `S3`**.
  Sáu lần thử tái hiện tại chỗ đều không ra.
- **`A3`/`A4` chưa đo trên `353eae1`** — không lượt Windows nào chạy trên head này, theo chỉ thị chủ kho
  (không CI tay, full CI khi merge). **Đừng đọc suite xanh trên Linux thành `A3` đạt.**
- **Phân biệt rò `GITHUB_ACTOR` với ca chập chờn**: `KHÔNG ĐO ĐƯỢC`, không phải "đã loại trừ". Bản vá
  vòng 5 cố ý thay một lời khai nhân quả không đo được bằng `LỆCH_CHƯA_RÕ_NGUYÊN_NHÂN`.
- **`SO-CANON-CHUA-TON-TAI`** — `grep -rln "review_rounds_used" --include=*.py .` ⇒ **0 tệp**. Trần 10
  vòng **không có cổng nào canh**, y như trần 2. Đếm vòng hiện là đếm TAY.
- **F6 ở trên** — `dotbien512.py` cần vá, nhưng nó ngoài write set nên đi hồ sơ riêng.

## CẬP NHẬT 11:30Z — master ĐÃ TRÔI, và hai biến thể của `rc=12`

**`origin/master` giờ là `bb7013c` ("Merge pull request #472")**, không còn `015ffcc` như bảng Neo ở trên
ghi. Con số `015ffcc` trong bảng ấy vẫn ĐÚNG như một phép đo **tại thời điểm review vòng 6** — đó là base
mà reviewer đã đo — nhưng nó **không còn là master hiện tại**. Đo lại 11:30Z: **cả bốn** nhánh
`ops/handoff-512-luot6` · `claude/windows-lease-suite` · `ops/cap-lease-522-523` · `ops/cap-lease-504`
đều **CÓ DRIFT**. Đừng suy trạng thái drift từ tệp này — `git merge-base --is-ancestor origin/master <nhánh>`
là phép đo, tệp này chỉ là ảnh chụp.

**`rc=12` của cổng `thu-hoi` có HAI biến thể, hai thông điệp, cùng một cách chữa — đừng nhầm chúng là một:**

| thông điệp | nghĩa | đã gặp ở |
|---|---|---|
| `workflow_sha <X> != S <Y> — định nghĩa không neo canonical` | base của PR (`S`) cũ hơn master mà định nghĩa workflow được lấy từ master hiện tại | PR #525 (`83deec1a`), #512 (`7964097`, `8239554`) |
| `KHÔNG_XÁC_ĐỊNH: S <X> không phải tổ tiên của H <Y>` | master hiện tại không nằm trong head PR | PR #528 (`083a977`) |

Cách chữa cho cả hai: **merge `origin/master` vào nhánh** (merge commit, KHÔNG rebase, KHÔNG force — nhánh
có thể có phiên khác làm việc trên đó). Cả hai đều **không** phải lỗi nội dung PR.

## Ràng buộc phối hợp từ #472 (merged `bb7013c` lúc 11:22:31Z) — cho phiên làm #522

Chủ kho đã thông báo nền canonical trên #512. Phần **liên quan tới packet khác, không phải #504**, chép
lại đây vì nó sẽ mất nếu chỉ nằm trong một comment:

- `#472` land ba tệp: `scripts/tl_core/release.py`, `scripts/tl_selftest.py` (**hồi quy `r357`**),
  `RELEASE_MANIFEST.json`. **Không** thêm nội dung adapter `.agents`.
- `#522`/`#526` **có overlap ở selftest + manifest**. Khi tích hợp `#522`: **giữ `r357` của `#472`**, đối
  chiếu slot `r291`, và **tái sinh manifest TỪ CÂY TÍCH HỢP** — **không ghép hash manifest thủ công**.
- Thông báo ấy **không cấp lease hay quyền mới**, và **không** yêu cầu packet nhận tin chạy CI.

Nhắc kèm từ `CLAUDE.md` §Quy ước deploy mục 5, vì nó là cái bẫy đúng chỗ này: `RELEASE_MANIFEST.json` băm
**nội dung** từng tệp, nên sửa một tệp đã có trong manifest cũng làm sha lệch dù `file_count` không đổi —
và **lane PR KHÔNG bắt được** (lane WORKER sinh manifest tạm từ chính cây nên hấp thụ mọi thay đổi) ⇒ PR
xanh, master ĐỎ. Muốn biết trước khi merge thì chạy đúng lệnh của lane LAND:
`python scripts/tl.py release-verify RELEASE_MANIFEST.json --strict --json`, đòi `ok=true` và
`expected == checked`.

## Hiện vật trong thư mục này

| tệp | là gì |
|---|---|
| `VERDICT.rvwin512-6.md` | verdict vòng 6, **nguồn có thẩm quyền**, byte-exact, sha256 ở trên |
| `HINT.rvwin512-6.patch` | bản vá reviewer đề xuất, **chưa áp**, `patch -p0` từ gốc cây kho |
| `EVIDENCE.rvwin512-6.md` | lời khai tác giả đã giao cho reviewer vòng 6 |
| `PROMPT.rvwin512-6.md` · `PROMPT-TIEP-lan3.rvwin512-6.md` | prompt đã dùng (phóng nguội · resume lần 3) |
| `suite-353eae1-linux.log` | log suite đầy đủ của `353eae1`, 3 lượt (CHA/A/B) — mọi số thời gian trong `EVIDENCE` neo theo SỐ DÒNG của tệp này |
| `dotbien-16-linux.txt` | đầu ra catalogue 16 đột biến |
| `dotbien512.py` | **bộ đo có lỗi F6** — persist ở đây để phiên sau vá được |
| `VERDICT.luot-chet-1.partial.md` | bản dở của lượt chết đầu, giữ làm hồ sơ hạ tầng |

Verdict vòng 1–5 **không** ở đây: chúng chưa từng được đẩy vào kho (nợ hồ sơ ADR-0034, sẽ vào PR hồ sơ
sau khi #512 land). Chúng chỉ còn trong scratchpad của container cũ ⇒ coi như **đã mất**, và đó là một
mất mát thật cần khai trong PR hồ sơ, không phải im lặng.
