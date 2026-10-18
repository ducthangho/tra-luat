# Đặc tả packet — DOT-BIEN-L-BIEN-CONG-KHAI (revision 8)

- `packet_id`: **wp677** (ID bền theo `docs/PROTOCOL_DA_PHIEN.md` §3.2: `wp<issue>`; r1–r6 ghi nhầm slug vào trường này)
- `packet_slug`: **DOT-BIEN-L-BIEN-CONG-KHAI**
- `packet_issue`: **#677**
- `mission_issue`: **KHONG_CO**. Đây là nợ số 3 mang sang từ #579, không thuộc lane kế hoạch nào.
- `revision`: **8** · soạn **17:10Z 29-09-2026** (r7 soạn 11:43Z) · nền đo `origin/master` **`89fc4fa`**; nhánh spec đã merge master `1c23933`
- `thay_the_cho`: revision 7 (`ops/specs/dot-bien-l-bien-cong-khai-r7.md`, sha256 `98138c5c…032da2`), do lượt codex 2
  trên PR #689 (`1290ebb`: 0 P1 / 2 P2 / 0 P3 / 1 P4) và Review Rescue Checkpoint của chủ kho (§0.7). r7 thay r6
  (`deb33408…40b1dd`). Chuỗi trước: r5 `fb261f64…53302`, r4 `d69178c6…d3f489`, r3 `e5be2293…148d7`, r2 `4510f060…47bb5`, r1 `81468e21…42a4da`. Xem §0.
- `depends_on`: **`[]`**. Lease của #676 trên `ops/lease_publish_test.py` đã nhả (đo §9).
- `executor`: claude · reviewer: codex `gpt-6-astra` (effort ≥ medium) · `environment`: cloud
- `risk`: **sensitive** · `review_class`: **sensitive**
- `assurance_target`: **human_audited**

> Mọi con số trong tệp này đều kèm mốc đo. Đo lại TRƯỚC mỗi bước công bố: cấp lease, đăng verdict, merge.
> Các quyết định neo vào BẤT BIẾN, còn con số chỉ để đối chiếu.

---

## 0. Thay đổi theo từng lượt cross-review

### 0.7 — r8, sau lượt codex 2 trên PR #689 (`1290ebb`) — REVIEW RESCUE CHECKPOINT có quyết định chủ kho

Verdict lượt 2: `pull/689#issuecomment-5894677255` (16:49Z; VERDICT.md sha256 trong comment). R1-F3/F4/F6/F8
ĐÃ ĐÓNG; R1-F1/F2/F5/F7 ĐÓNG MỘT PHẦN. Theo Q15 lượt 2 là lượt cuối ⇒ checkpoint.

Cùng lúc có HAI phiên điều phối lái #677 và nhận hai bộ chỉ thị lệch nhau (`issues/677#issuecomment-5894971548`):
Q16/Q17 của phiên `session_015WM7xm…` (16:50Z: trần 400, Sonnet) và Q18/Q19 của phiên `session_01RU4YGG…`
(~17:00Z). Chủ kho chốt ở Q20: **phiên `session_01RU4YGG…` lái**, bộ Q18/Q19 có hiệu lực, Q16/Q17 bị thay.

| Lớp lượt 2 | Mức | Xử lý ở r8 |
|---|---|---|
| **L1** — phản chứng vá theo ví dụ, 13 đường vào chưa khoá (L1-E1…E13) | P2 | **A11** mới (§7): mỗi đường vào một phản chứng riêng, đột biến N1–N13 phải ĐỎ đúng assertion. |
| **L2** — quyền vượt trần dòng A7 chưa ghi bền | P2 | **Q19** (§3): trần ≤ 600, ghi nguyên văn; A7(2) đổi theo. |
| **L3** — điểm nối sổ bỏ qua của #687 | P4 | Ghi nhận; bên land sau (#687) đăng ký các ca mới có đường `BoQuaNen`. |

Q18 mở trần 2 lượt codex cho PR #689 BẰNG quyết định chủ kho ghi bền ở đây — không lặp C-P1 của r7.
§1–§10 ngoài §3 (thêm Q16–Q20), A7(2) và A11 **không đổi**.

### 0.6 — r7, sau review của connector codex trên `04483e8` — và REVIEW RESCUE CHECKPOINT

Connector codex (`chatgpt-codex-connector[bot]`, review `5351933254`, 11:40Z 29-09) tự chạy khi PR chuyển sang
ready. Đó là lời gọi codex thứ **7** trên PR #684.

| finding | mức | r7 xử lý |
|---|---|---|
| **C-P1** — vượt trần 2 lượt codex/PR (protocol §8 dòng 669, §12 dòng 1079) mà không qua Review Rescue Checkpoint | P1 | **Đúng.** Lượt 3–6 của phiên điều phối đã vượt trần theo chỉ thị thường trực "lặp tới khi 0 P1/P2/P3", không đối chiếu với trần. Checkpoint nay được ghi (Q14, §3): **không gọi codex nữa trên PR #684**; bảo chứng đi bằng `human_audited` trên head mới. Các verdict lượt 1–6 giữ nguyên làm hồ sơ lịch sử. |
| **C-P2a** — `packet_id` phải là `wp677` (§3.2) | P2 | Đầu tệp: `packet_id: wp677`, thêm `packet_slug`. |
| **C-P2b** — A7 lọc theo đường dẫn nên không thấy tệp lạ | P2 | A7 viết lại: tập đường dẫn đổi (không lọc) phải **bằng đúng** `{ops/lease_publish_test.py}`, rồi mới áp trần 300 dòng. |
| **C-P2c** — A8 so với `origin/master` là mốc trôi | P2 | A8 viết lại: so với `start_from_sha` của lease đang hiệu lực (OID đầy đủ). Master trôi thật trong packet này (`89fc4fa` → `1c23933`). |
| **C-P2d** — lệnh trích ghi `do_bien_L.py` và `.pyc` vào checkout | P2 | Phụ lục A: trích và chạy trong thư mục tạm **ngoài** checkout, interpreter `-B`. |
| **C-P2e** — nhãn "(r2: …28701faf)" sai | P2 | Sửa thành r3–r7. |

§1–§10 ngoài A7/A8 và nhãn Phụ lục **không đổi**; M1–M6 không đổi.

### 0.5 — r6, sau lượt 5 (codex `gpt-6-astra`, effort `high`, trên `b91e029`)

| finding | mức | r6 xử lý |
|---|---|---|
| **R5-F1** — §11 bỏ sót R4-F1 dù R4-F1 chính là một lần `LOI-KHAI-RONG-HON-PHEP-DO` đã xác nhận | P3 | §11: bộ đếm 9 → **10**, ghi nguồn R4-F1 (lượt 4, `e601b22`). |

**Chỉ §0 và §11 đổi.** Mục tiêu, nghiệm thu, write set, giàn, số đo giữ nguyên — việc của executor không đổi.

### 0.4 — r5, sau lượt 4 (codex `gpt-6-astra`, effort `high`, trên `e601b22`)

| finding | mức | r5 xử lý |
|---|---|---|
| **R4-F1** — §10.1 vẫn khai "tổ hợp §2.3 cần một comment bot **trên PR**", trong khi 7/15 chứng nhân nằm trên **Issue** | P3 | §10.1 tách hai nhóm: nhóm PR (8 dòng) giữ `KHÔNG ĐO ĐƯỢC`; nhóm Issue (7 dòng) dẫn §2.4 — dấu bot trên Issue là thứ workflow **tự sinh**, đã mô phỏng; HTTP thật chưa đo. |

**Chỉ §0 và §10.1 đổi.** Không đổi mục tiêu, nghiệm thu, write set, giàn hay số đo — việc của executor không đổi.

### 0.3 — r4, sau lượt 3 (codex `gpt-6-astra`, effort `high`, trên `884ba8f`)

Lượt 3 xác nhận **đã vá thật** cả ba finding lượt 2 (R2-F1 chạy lại đủ ma trận ba trạng thái × ba đột biến guard;
R2-F2; R2-F3 với `PER_ROW_CHECK 95 ERRORS []`) và giữ được các phép vá của lượt 1.

| finding | mức | r4 xử lý |
|---|---|---|
| **R3-F1** — chưa quyết định phạm vi khi phản hồi `comments` **thay đổi giữa các GET** trong một lượt (snapshot đổi; lỗi một lần rồi phục hồi) | P2 | Tiền đề mới ở §2.6: phản hồi `gh` **ổn định trong một lượt**. Hai chứng nhân của reviewer ghi vào §2.6. **Q13** (§3): trục này **loại khỏi tập khoá**, kèm lý do. |

Lượt soạn r4 **không** đổi giàn Phụ lục A và **không** đổi các con số của §2.3: R3-F1 nằm ngoài miền snapshot tĩnh
mà giàn đo, và reviewer lượt 3 tái lập đúng 95 dòng trên chính giàn ấy.

### 0.2 — r3, sau lượt 2 (codex `gpt-6-astra`, effort `high`, trên `bd401e8`)

Lượt 2 xác nhận F1 và F2 của lượt 1 **đã vá thật**; F3 **vá hờ** (đóng hẹp); F4 **vá sinh lỗi mới** ở phần số.

| finding | mức | r3 xử lý |
|---|---|---|
| **R2-F1** — A9(c)/M6 vẫn đếm sự có mặt; guard chỉ xét `os.name` qua được cả A9(a), A9(b) và `t70` | P2 | A9 viết lại lần hai (§7). Helper có **điểm dò ngay sau guard** (M1). Một ca meta thử **ba trạng thái** qua điểm dò ấy — posix · nt + workflow thật · nt + workflow tạm matrix Ubuntu+Windows — không chạy I/O dưới `os.name` giả. Ba đột biến guard, mỗi cái đỏ đúng một trạng thái; lượt soạn đã dựng thử và đo (§7, A9). M6 hạ xuống **kiểm kê**, không còn là bằng chứng nhánh. |
| **R2-F2** — trục GET loại số hiệu lỗi mở thêm mất tín hiệu đỏ trên Issue còn hạn | P2 | Thêm trục bổ sung vào giàn (§2.2): 5 dòng. Ba dòng lệch mã thoát mới (§2.3). Q12 mở rộng: **không** thêm họ M3c, kèm lý do (§3). |
| **R2-F3** — số log `73/5` không tái lập; hai vế tự dựng hạn khác nhau | P3 | Giàn dựng YAML **một lần mỗi cặp**, và tự in dòng `LOG` (Phụ lục A). Số mới `80 / 15` sinh từ chính giàn, chạy hai lần trùng từng dòng (§2.3). `73/5` của r2 là tạo tác của việc dựng hạn hai lần. |

### 0.1 — r2, sau lượt 1 (codex `gpt-6-astra`, effort `high`, trên `c78a5d0`)

| finding | mức | r2 xử lý |
|---|---|---|
| **F1** — thiếu trục HẾT HẠN; nó mở thêm tổ hợp mất tín hiệu đỏ ngay trên **Issue** | P2 | Thêm trục hạn vào giàn (§2.2). Không gian 46 → **90** dòng; lệch mã thoát 4 → **12** (§2.3). Cơ chế ở §2.4. Thêm họ chứng nhân **M3b** (Issue + có dấu + hết hạn) vào M3/A2, áp dụng nguyên luật Q8/Q9 (§3, Q12). |
| **F2** — chưa khai điều kiện giữ cố định để A1/A2 phân biệt được `L` | P2 | Bảng tiền đề fixture §2.6. Liệt kê các trục **che mất** độ phân biệt (lỗi kép), kèm số reviewer đo. M1/M5 buộc fixture giữ bảng ấy. |
| **F3** — phản chứng A9 không kiểm được điều kiện bỏ qua | P2 | A9 viết lại (§7): ca mới phải CHẠY trên Linux; một ca meta dùng `_chay_main_meta(<ca>, "nt")` phải cho đúng dòng `BỎ QUA` kèm lý do `runs-on`; hai đột biến guard. Thêm **M6**: `t70` đếm cả helper mới. |
| **F4** — "log chỉ lệch dấu thời gian" sai với chính bốn dòng lệch mã thoát | P3 | §2.3 viết lại theo phép đo log từng dòng. Cột `=` định nghĩa là bằng trên bộ `(rc, goi, dang)`, không phải bằng byte log. |

Ngoài bốn finding, lượt soạn r2 tự tìm thêm một chỗ: `t70` ghim **đúng 7** ca có tên `_chay_buoc_dang` trong
`co_names`. Helper mới cũng chạy thân bước `đăng`; nếu `t70` không đếm nó, ca mới sẽ là ca đọc thân bước mà chốt
"matrix có Windows phải chạy lại" không canh. Đó là **M6**, vẫn trong write set.

---

## 1. `nguon_cap_viec`

Nợ mang sang của packet #579. Nguồn:

- Human audit [`pull/589#issuecomment-5857502345`](https://github.com/ducthangho/tra-luat/pull/589#issuecomment-5857502345).
- Biên nhận land [`issues/579#issuecomment-5858147839`](https://github.com/ducthangho/tra-luat/issues/579#issuecomment-5858147839), mục "Nợ mang sang":
  *"Vế 'biên công khai' của đột biến `L`: `KHÔNG ĐO ĐƯỢC`"*.
- Đặc tả cha `ops/specs/dang-lease-dau-truoc-kiem-sau-r30.md` (sha256 `c8a72a41…0dc2`), §7.8, §10 mục 8, §12.4.

**Đột biến `L`**: gỡ hai dòng chốt `lease_id` khỏi `_tien_kiem_mien_dang` trong `ops/lease_publish.py`:

```python
    if not isinstance(lease.get("lease_id"), (str, int)) or isinstance(lease.get("lease_id"), bool):
        raise Chan(RC_NOI_DUNG, "tiền kiểm: thiếu `lease_id` hoặc sai kiểu")
```

`t178` đã giết `L` ở **đơn vị phép dò** (`_do_dau_da_dang`): nền 0 lời gọi GitHub, `L` 1 lời gọi. Câu hỏi của
packet này: khác biệt ấy có nguy hiểm ở **biên công khai** không, tức ở thân bước `đăng` của
`.github/workflows/ops-publish-lease.yml` khi chạy với `ops/lease_publish.py` THẬT.

## 2. Phép đo của lượt soạn spec — và lời khai SAI mà nó đã sửa

### 2.1 — Giàn đo

Phụ lục A là giàn, chép nguyên văn (sha256 của tệp giàn lúc chép, r3: `28701faf…feb2`; r2 là `147b33c5…6853`; r1 là
`fb1950d4…e98b`). Giàn làm ba việc:

1. Trích thân bước `đăng` bằng `_buoc_workflow("đăng")` của chính `ops/lease_publish_test.py`.
2. Chép `ops/lease_publish.py` của cây vào một `$NEO` tạm, ở hai vế: **nền** (nguyên văn) và **`L`** (gỡ đúng hai dòng trên).
   Mỗi lượt dùng một thư mục tạm riêng, với `PYTHONDONTWRITEBYTECODE=1`.
3. Đặt `gh` giả trên **PATH**. `gh` giả **giữ trạng thái**: mỗi số hiệu có danh sách comment và cờ "là PR"; POST thêm comment vào đó.
   Mọi lời gọi được ghi lại dưới dạng `(method, endpoint)`.

**Lần đo đầu, giàn HỎNG, và đây là bẫy chính của packet.** `lease_publish.py` gọi `gh` qua `subprocess` (`GOI_GH`),
chứ không qua thân bước. Thay chuỗi `gh api` trong thân bước là KHÔNG đủ. Khi đó mọi lượt, kể cả ca đối chứng
hợp lệ, đều cho `rc=1` với 0 lời gọi, vì `[Errno 2] No such file or directory: 'gh'`. Bắt được nhờ **ca đối
chứng dương**. Mọi số dưới đây là của giàn đã sửa.

### 2.2 — Không gian đã đo: BỐN trục (luật Q11)

| trục | giá trị | số giá trị |
|---|---|---|
| `lease_id` trong YAML | `null` · `~` · `[wp579-thu]` · `true` · `yes` · `{x: 1}` · `1.5` · `1.50` · `2026-09-29` · `123` · `wp-ok-1` | 11 |
| số hiệu `packet_issue: 55` | Issue · Pull Request | 2 |
| trạng thái comment | trống · đã có comment `github-actions[bot]` bắt đầu bằng ``**Lease `str(giá trị)`**`` | 2 |
| hạn lease (MỚI ở r2, F1) | còn hạn (`mai_sau()`) · hết hạn (một giờ trước lúc chạy) | 2 |
| **bổ sung** (MỚI ở r3, R2-F2): GET `issues/55` (loại số hiệu) **lỗi** HTTP 500, `comments` vẫn đọc được | chỉ ở ô Issue + có dấu + còn hạn, với 5 dạng: `true` · `1.5` · `2026-09-29` · `null` · `wp-ok-1` | 5 dòng |
| dạng tài liệu (chỉ ở ô Issue, trống) | thiếu `lease_id` · tài liệu là danh sách | 2 |

Tổng: 11 × 2 × 2 × 2 + 2 + 5 = **95 dòng**, mỗi dòng chạy hai vế ⇒ **190 lượt chạy bước** (đo 10:22Z 29-09, `89fc4fa`;
chạy lại lần hai cùng giờ: phân loại **trùng từng dòng**). Hai dạng tài liệu chỉ chạy ở ô còn hạn, Issue, trống.
Hai vế của mỗi dòng nhận **cùng byte YAML** (r3, R2-F3).

r1 đo trên 46 dòng (ba trục đầu). 46 dòng ấy là tập con giữ nguyên trong 90 dòng và tái lập đúng số cũ
(`4 / 32 / 10`, đo lại bởi cả reviewer lượt 1 lẫn lượt soạn r2). Lưới 90 dòng của r2 giữ nguyên số `12 / 60 / 18`.

### 2.3 — Kết quả (đo 10:22Z 29-09-2026, `89fc4fa`)

| lớp kết quả | số dòng | nơi xảy ra |
|---|---|---|
| **lệch MÃ THOÁT** của bước | **15** | lưới: 4 dạng (`true` · `1.5` · `1.50` · `2026-09-29`) × 3 ô — **PR + có dấu + còn hạn** · **Issue + có dấu + hết hạn** · **PR + có dấu + hết hạn** (12); bổ sung: `true` · `1.5` · `2026-09-29` × **Issue + có dấu + GET loại số hiệu lỗi** (3) |
| chỉ lệch bộ (số lời gọi, POST) — mã thoát trùng | 61 | lưới: các ô còn lại của **9** dạng bị tiền kiểm chặn (`null` `~` danh sách `true` `yes` ánh xạ `1.5` `1.50` ngày), 9 × 8 − 12 = 60; bổ sung: `null` (1) |
| trùng trên bộ `(rc, goi, dang)` | 19 | lưới: `123` · `wp-ok-1` (8 ô mỗi dạng) · hai dạng tài liệu (18); bổ sung: `wp-ok-1` (1) |

`=` và "chỉ lệch bộ" so trên bộ `(rc, dãy lời gọi, comment đã POST)`, **không** so byte log (F4). Log do **chính
giàn** tổng kết ở dòng `LOG` (Phụ lục A; 10:22Z 29-09, hai lượt trùng): cả **80** dòng không lệch mã thoát có log
**bằng từng byte**; cả **15** dòng lệch mã thoát có log **khác nội dung** — nền in `CHAN [8]` (số hiệu là PR; lease
đã hết hạn; hoặc `KHÔNG ĐO ĐƯỢC loại số hiệu`), `L` in `CHAN [9] … bỏ qua`.

Con số `73 / 5` mà r2 ghi **không tái lập được** (reviewer lượt 2 đo `74 / 4` trên cùng giàn): giàn r2 dựng YAML
**riêng cho từng vế**, nên mốc hạn hai vế có thể lệch một giây. Nó là tạo tác của giàn, không phải khác biệt do `L`.

Chi tiết mười lăm dòng lệch mã thoát:

| `lease_id` × ô | nền | `L` |
|---|---|---|
| 4 dạng × PR + có dấu + còn hạn | `rc=1`, ĐỎ — `CHAN [8]` số hiệu là PR | `rc=0`, *"đã đăng trước đó — bỏ qua"*, XANH |
| 4 dạng × Issue + có dấu + **hết hạn** | `rc=1`, ĐỎ — `CHAN [8]` lease đã hết hạn | `rc=0`, bỏ qua, XANH |
| 4 dạng × PR + có dấu + **hết hạn** | `rc=1`, ĐỎ — `CHAN [8]` lease đã hết hạn | `rc=0`, bỏ qua, XANH |
| 3 dạng × Issue + có dấu + còn hạn + **GET loại số hiệu lỗi** | `rc=1`, ĐỎ — `CHAN [8]` KHÔNG ĐO ĐƯỢC loại số hiệu | `rc=0`, bỏ qua, XANH |

Dạng `yes` rơi vào "chỉ lệch số lời gọi" ở ô PR + có dấu. Lý do là **tạo tác của fixture**: giàn dựng dấu theo chữ `yes`,
trong khi YAML 1.1 đã ép giá trị thành `True`. Đo riêng với dấu ``**Lease `True`**`` (07:58Z 29-09) thì `yes` cũng
lệch mã thoát, y như `true`.

Không ô nào có POST ở vế này mà không có ở vế kia.

Chuỗi hợp lệ (`wp-ok-1`) + có dấu + hết hạn cho `rc=0` bỏ qua ở **cả hai** vế. Đó là hành vi có chủ đích của #579
(`t174`: lease đã đăng rồi mới hết hạn thì bỏ qua, không đỏ), không do `L`.

### 2.4 — Cơ chế

Với `L`, phép dò chạm mạng, thấy dấu, rồi ném `RC_DA_DANG`. Nhánh đã-có-dấu của `kiem_github` chạy
`kiem(bo_qua_han=True)`. Hàm này **nhận** `True`/`1.5`/date: nó làm `str()` trước khi so regex, nên `"True"`,
`"1.5"`, `"2026-09-29"` đều khớp `LEASE_ID`. Nhánh ấy **không chạy `_kiem_loai_so_hieu`**, đúng giới hạn mà docstring
`kiem_github` đã khai. Trên nền, chốt `lease_id` chặn phép dò, nên chuỗi cũ chạy trọn và `_kiem_loai_so_hieu` bắt được "số hiệu là PR".

Trục bổ sung (R2-F2) cùng cơ chế với ô PR, cùng chốt bị bỏ: `_kiem_loai_so_hieu` không tới được lời khai
"số hiệu là Issue" nên nền đỏ `KHÔNG ĐO ĐƯỢC`; nhánh đã-có-dấu của `L` không gọi chốt ấy.

Trục hạn (F1) cùng một cơ chế, khác chốt bị bỏ: nền chết ở chốt **hạn** của `kiem()` (`CHAN [8]` lease đã hết hạn);
`L` đi nhánh đã-có-dấu, và nhánh ấy gọi `kiem(bo_qua_han=True)`, tức cố ý bỏ đúng chốt hạn.

⇒ **Chốt `lease_id` của `_tien_kiem_mien_dang` có răng ở biên công khai**: nó giữ ĐỎ các tổ hợp mà `L` biến thành XANH.

**Ô Issue + hết hạn thực tế hơn ô PR** (§10.1). Chính giàn này đo (10:03Z 29-09, `89fc4fa`): ô `true`/`1.5`/ngày + Issue + trống +
còn hạn cho `rc=0` và **đúng 1 POST** ở cả hai vế, thân bắt đầu bằng ``**Lease `True`**`` / `` `1.5` `` /
`` `2026-09-29` ``. Tức dấu bot mang giá trị ép kiểu trên một Issue là thứ workflow **tự sinh ra được**; lease
ấy hết hạn sau đó là đủ để vào ô M3b. Còn ô PR cần một comment bot trên PR, điều §10.1 vẫn ghi `KHÔNG ĐO ĐƯỢC`.

### 2.5 — Lời khai SAI đã rút lại

Thân Issue #677 lúc tạo (06:19Z 29-09) khai *"vô hại, cho cả 13 dạng"*. Lời khai ấy được đo trên HAI trục
(`lease_id` × trạng thái comment) và **thiếu hẳn trục loại số hiệu**. Rút lại ở
[`issues/677#issuecomment-5886120520`](https://github.com/ducthangho/tra-luat/issues/677#issuecomment-5886120520).
Dấu hiệu đã báo trước mà lượt đầu đọc sót: chênh số lời gọi `L − nền` có giá trị **−1**, tức `L` bỏ qua một
lời gọi mà nền có. Đó là lời gọi `GET issues/55` của `_kiem_loai_so_hieu`.

### 2.6 — Tiền đề fixture: các điều kiện GIỮ CỐ ĐỊNH (MỚI ở r2, F2)

Kết luận §2.3 và độ phân biệt của A1/A2 chỉ đúng khi mọi chốt KHÁC trong chuỗi đều qua. Fixture của M2/M3/M4 phải
giữ nguyên các điều kiện sau (tất cả là mặc định của `lease_mau()` và của `gh` giả ở Phụ lục A):

| điều kiện | giá trị giữ cố định |
|---|---|
| `packet_issue` | số nguyên dương `55`, khớp số hiệu `gh` giả phục vụ |
| `granted_by` | người trong `NGUOI_CO_THAM_QUYEN` (`ducthangho`); `GITHUB_ACTOR` cũng vậy |
| `schema_version` / lớp review | như `lease_mau()` (schema 1, không có khối lớp review) |
| `reviewed_sha_required` | 40 ký tự hex thường |
| neo prompt | **vắng cả cặp** `prompt_path` / `prompt_sha256_required` |
| hạn | theo trục §2.2 (còn hạn, hoặc hết hạn một giờ ở M3b) |
| `gh api` | đọc được: GET `issues/55` trả `html_url` đúng loại; GET `comments` trả danh sách phân trang hợp lệ |
| **tính ổn định trong một lượt** (r4, R3-F1) | mọi GET `comments` trong **cùng một lượt chạy bước** thấy **cùng một snapshot** và **cùng trạng thái** thành công/lỗi; snapshot chỉ đổi do chính POST của bước, và bước không đọc lại sau POST |

**Các trục CHE MẤT độ phân biệt** — reviewer lượt 1 đo (09:51–10:02Z 29-09, trên `c78a5d0`), mỗi trục thêm vào
tổ hợp M3a (`true` + PR + có dấu):

| thêm trục | nền | `L` | hệ quả |
|---|---|---|---|
| `packet_issue` sai kiểu (`'55'` `True` `1.5` `[]` `None`) × `lease_id` `null`/`true` | `rc=1`, 0 GET | `rc=1`, 0 GET | 10 tổ hợp, không phân biệt được |
| tự cấp (`CHAN [4]`) · prompt thiếu (`CHAN [6]`) · schema v2 thiếu lớp (`CHAN [10]`) · SHA sai (`CHAN [8]`) | `rc=1`, 0 GET | `rc=1`, 1 GET | mã thoát không phân biệt; chỉ số lời gọi phân biệt |
| API `comments` trả lỗi | `rc=1` | `rc=1`, không bỏ qua | không phân biệt được |
| dấu bot ở **trang hai** của `--paginate` | như trang một | như trang một | **không** che (giữ kết luận gốc) |

Lượt 2 còn đo thêm (10:09–10:21Z 29-09 theo mốc tệp `VERDICT.md` của lượt, trên `bd401e8`), đều **không** đổi kỳ vọng M2/M3/M4: hạn sai cú pháp (che,
`CHAN [8]` cả hai vế); con trỏ trường treo và `thay_the_cho` sai kiểu (che); comment hỏng nằm **trước** dấu (che) —
nằm **sau** dấu thì `L` vẫn lật `1→0`, tức độ phân biệt phụ thuộc thứ tự nếu mở rộng miền; phân trang phẳng có dấu
(`L` lật `1→0`); scalar YAML khác (`.inf` `.nan` `false`) lật `1→0` ở M3a và M3b — cùng hai chốt đã khai; `role`
rỗng (không phải trường bắt buộc của schema 1) lật `1→0` ở PR. Bảng 11 giá trị `lease_id` **không** khai là mọi scalar.

**Phản hồi `comments` đổi giữa các GET — NGOÀI PHẠM VI KHOÁ (r4, R3-F1, Q13).** Reviewer lượt 3 đo (trên
`884ba8f`, theo mốc tệp `VERDICT.md` của lượt), Issue còn hạn, `true`/`1.5`/ngày:

| biểu hiện | nền | `L` |
|---|---|---|
| GET `comments` lần đầu trả snapshot **rỗng**, các lần sau trả **có dấu** | `rc=0`, **POST=1** | `rc=0`, POST=0 |
| `true`, GET `comments` **lỗi đúng một lần** rồi phục hồi, Issue **có dấu** | `rc=1`, POST=0 | `rc=0`, POST=0 |
| như trên, Issue **trống** | `rc=1`, POST=0 | `rc=0`, **POST=1** |

Chuỗi hợp lệ: hai vế tương đương. Đây là trục **lịch gọi**, không phải trục chốt: nền (tiền kiểm chặn phép dò) gọi
`comments` **một** lần, còn `L` gọi **hai** lần (phép dò + cửa cuối), nên một đồ giả đánh chỉ số theo LẦN GỌI cho chênh
lệch theo **cả hai chiều** — ở biểu hiện đầu, chính nền mới là bên đăng trùng. Ở hai biểu hiện sau, cái đỏ của nền là
`KHÔNG ĐO ĐƯỢC` do lỗi tạm thời (tính sẵn sàng), và `L` qua vì vô tình có thêm một lần đọc, không vì vượt một chốt thẩm
quyền. Phần "kiểu ép được đăng" thuộc #678 (Q2).

**GET loại số hiệu lỗi KHÔNG phải trục che** — nó là chứng nhân mới (R2-F2, §2.3). Khác hẳn lỗi API `comments`
(che): ở đây `comments` đọc được dấu, chỉ GET `issues/55` hỏng.

Đây là lỗi kép: chốt khác chặn trước, nên `L` không còn đường tới nhánh bỏ qua. Packet **không** đòi mọi tổ hợp lỗi
kép phải giết `L`. Nó chỉ đòi fixture M2/M3 giữ bảng tiền đề trên, và M5 khai các trục che vào docstring.

## 3. Quyết định của chủ kho (29-09-2026, hai vòng, chấp nhận nguyên văn mọi khuyến nghị)

| câu | quyết định |
|---|---|
| **Q1** | Ca biên khoá **cả bộ quan sát** cho tập (i) ở §6: `rc` bước, dãy `(method, endpoint)`, số POST. |
| **Q2** | Các dạng ép kiểu mà hiện đang **được đăng** (Issue thật, chưa có dấu) **không** khoá ở đây. Đó là việc của #678. |
| **Q3** | **Helper mới** (tạm tên `_chay_buoc_dang_that`). **Không** sửa `_chay_buoc_dang`. |
| **Q4** | Ba đột biến bắt buộc ĐỎ **đúng lý do**: `L`; `gh` giả vắng khỏi PATH; `gh` giả không ghi POST. |
| **Q5** | Trần ADR-0044 cho `sensitive`: **≤ 300 dòng thêm**, 1 tệp, không xin ngoại lệ. Vượt thì DỪNG và hỏi. |
| **Q6** | Bỏ qua trên Windows **chỉ** qua `_ly_do_bo_qua_workflow` (tức `os.name == "nt"` **và** job chỉ chạy Ubuntu). Không chạy CI Windows. |
| **Q7** | `human_audited`; spec nằm trên nhánh riêng, land qua PR bookkeeping, không tính vào write set. |
| **Q8** | Tổ hợp §2.3 xếp **NGUY HIỂM** (mất tín hiệu đỏ ở cổng). Nền đã đúng ⇒ **không vá `ops/lease_publish.py`**; chỉ khoá. |
| **Q9** | Tập khoá chia hai, (i) và (ii), xem §6. Tập (ii) thay phần "loại dạng ép kiểu" của Q2 cho riêng ô PR + có dấu. |
| **Q10** | Đóng băng spec ngay; **chờ** #676 land hoặc hết hạn rồi mới xin lease; không xin #676 nhả sớm. Sau #676: #677 rồi #678. |
| **Q11** | Mọi kết luận "vô hại" hoặc "nguy hiểm" phải kèm **danh sách TRỤC đã đo**. Reviewer được giao nhiệm vụ **tìm trục còn thiếu**. |
| **Q12** (r2) | **Không phải quyết định mới**: áp nguyên luật Q8/Q9 cho các ô F1 tìm ra. Ô Issue + có dấu + hết hạn là mất tín hiệu đỏ ⇒ nguy hiểm (Q8) ⇒ khoá bằng họ **M3b**, chỉ khoá `rc ≠ 0`, 0 POST, không "bỏ qua" (Q9). Ô PR + có dấu + hết hạn **không** thêm họ riêng: M3a và M3b đã phủ hai chốt bị `L` bỏ qua (loại số hiệu, hạn). **r3 (R2-F2):** ô Issue + có dấu + GET loại số hiệu lỗi **không** thêm họ M3c, vì nó bỏ **cùng chốt** `_kiem_loai_so_hieu` như M3a — M3a giết `L` đã chứng minh đường vòng qua chốt ấy; M3c chỉ đổi cách chốt ấy không đạt (PR thay vì không đo được). Chủ kho có thể bác Q12 ở lượt audit. |
| **Q14** (r7, chủ kho 29-09 "Đồng ý cả 2 khuyến nghị") | **Review Rescue Checkpoint cho PR #684**: trần 2 lượt codex đã vượt (7 lời gọi). Vá C-P2a..e thành r7, **không gọi codex nữa**; bảo chứng bằng human audit của chủ kho trên head mới. Human audit trên `04483e8` hết hiệu lực vì head đổi. |
| **Q16** (phiên `session_015WM7xm…`, 16:50Z, `issues/677#issuecomment-5894685680`) — **BỊ THAY bởi Q19** | "Q16 chốt 400": trần A7/S4 300 → 400. |
| **Q17** (cùng phiên, cùng comment) — **BỊ THAY bởi Q19** | "Q17 giữ sonnet, high hoặc xhigh effort". |
| **Q18** (phiên `session_01RU4YGGdYMx94uVcywPjo4F`, ~17:00Z) | Tại checkpoint sau lượt 2, chủ kho chọn nguyên văn **"Cho phép vượt trần Codex"** — phương án: "ghi bền ngoại lệ trần 2 lượt cho PR #689: Opus vá L1, rồi Codex lượt 3 (và tiếp) tới 0 P1/P2/P3. Ngoại lệ ghi vào spec r8 để không lặp lỗi C-P1 của r7." Thay Q15 cho PR #689. |
| **Q19** (cùng phiên) | Trần dòng thêm `ops/lease_publish_test.py` **≤ 600** — chủ kho chọn nguyên văn **"≤ 600 dòng thêm (Recommended)"**. Executor **Opus 5.5, effort high** (chỉ thị cùng phiên: "tiếp tục lặp vá (opus 5.5, high effort)"). Không CI tới khi đủ điều kiện merge. Phần "1 tệp" của Q5 giữ. |
| **Q20** (cùng phiên, ~17:08Z) | Hỏi "Phiên nào lái #677?", chủ kho chọn nguyên văn **"Phiên này lái (Recommended)"** — phiên `session_01RU4YGG…`; phiên `session_015WM7xm…` dừng; lease g5 thay g4. |
| **Q15** (r7, cùng lời chủ kho) | **PR #689 (mã) giữ trần 2 lượt codex.** Lượt 1 đã dùng (`11f73ac`, 0/5/3). Lượt 2 sau khi executor vá là lượt **cuối**; chưa approve ⇒ checkpoint, hỏi chủ kho, không gọi tiếp. |
| **Q13** (r4) | **Không phải quyết định mới** — áp tiêu chí của Q8 ("mất tín hiệu đỏ ở một **chốt**"). Trục phản hồi `comments` đổi giữa các GET (R3-F1) **loại khỏi tập khoá**: chênh lệch đến từ **số lần** gọi `comments` (1 so 2), đi theo cả hai chiều, và cái đỏ mà `L` làm mất ở đó là đỏ `KHÔNG ĐO ĐƯỢC` của một lỗi tạm thời chứ không phải đỏ của chốt thẩm quyền, hạn hay loại số hiệu. M2–M4 giữ tiền đề "ổn định trong một lượt" (§2.6). Khoá trục này sẽ là khoá **lịch gọi** của đồ giả, và nó sẽ đổi màu khi bất kỳ ai thêm/bớt một lần đọc vì lý do không liên quan. Chủ kho có thể bác Q13 ở lượt audit. |

## 4. `review_class`

`sensitive`. Đo 08:05Z 29-09: `_tinh_lop_tu_write_set(['ops/lease_publish_test.py'])` ⇒ `sensitive`. Kèm giới hạn đã
biết từ #603: hàm này hiện chỉ trả được `sensitive`.

## 5. `write_set`

- `ops/lease_publish_test.py`

**Một đường dẫn.** Không có `ops/lease_publish.py` (Q8: nền đúng, không vá). Không có `.github/workflows/**`.
Không có `CLAUDE.md`. Tệp spec này nằm trên nhánh spec và land qua PR bookkeeping (Q7).

## 6. `muc_tieu`

Mỗi mục chiếu vào `ops/lease_publish_test.py`.

- **M1** — Helper `_chay_buoc_dang_that`. Nó chạy thân bước `đăng` trích bằng `_buoc_workflow("đăng")`, với:
  - `$NEO/ops/lease_publish.py` **chép từ cây đang test** (không phải bản giả, không phải bản neo master);
  - `gh` giả **giữ trạng thái**, đặt trên **PATH**;
  - trả về `rc`, dãy `(method, endpoint)`, danh sách comment đã POST, và `out`.

  Cờ "số hiệu là PR" là một tham số. Helper nhận một **nguồn `lease_publish.py` tuỳ chọn**, để phép đột biến
  không phải ghi đè tệp thật. Helper bắt đầu bằng **đúng** guard của `_chay_buoc_dang`:
  `if _ly_do_bo_qua_workflow(WORKFLOW_DANG, "dang"): raise BoQuaNen(WORKFLOW_DANG, "dang")`.
  Ngay **sau** guard, **trước** mọi I/O, helper có một **điểm dò** (một tham số, tên tuỳ người thi hành): bật điểm
  dò thì helper trả về một giá trị chỉ "đã qua guard" mà không chạy gì thêm. Guard đọc `WORKFLOW_DANG` lúc gọi,
  nên ca meta thay được nó bằng một workflow tạm (A9). Điểm dò không được làm thay đổi hành vi khi tắt.
  Fixture giữ bảng tiền đề §2.6, kể cả **tính ổn định trong một lượt** (r4). `gh` giả phải **lưu** comment đã POST
  vào trạng thái (A4), và mọi GET trong một lượt đọc cùng trạng thái ấy — không đánh chỉ số theo lần gọi.
- **M2** — Ca biên **tập (i)**, khoá cả bộ quan sát:
  - `lease_id` ∈ {`null`, danh sách, ánh xạ} × {Issue, PR} × {trống, có dấu};
  - và hai dạng tài liệu: thiếu `lease_id`, tài liệu là danh sách.

  Kỳ vọng trên nền, đo 08:01Z 29-09: `rc=1`, **0 lời gọi `gh`**, 0 POST.
- **M3** — Ca biên **tập (ii)**, chỉ khoá `rc ≠ 0`, 0 POST, và **không có** dòng `đã đăng trước đó — bỏ qua`:
  - **M3a**: `lease_id` ∈ {`true`, `1.5`, `2026-09-29`} × **PR** × **có dấu** ``**Lease `str(giá trị)`**`` × còn hạn;
  - **M3b** (r2, Q12): `lease_id` ∈ {`true`, `1.5`, `2026-09-29`} × **Issue** × **có dấu** × **hết hạn**.

  Kỳ vọng trên nền, đo 10:03Z 29-09 trên `89fc4fa`: `rc=1`, 0 POST, không "bỏ qua" ở cả 6 ô.

  **Không** khoá dãy lời gọi ở tập này, để giữ đúng khi #678 đổi đường từ chối (Q9).
- **M4** — **Đối chứng dương**: `lease_id: wp-ok-1`, Issue, trống ⇒ `rc=0`, **đúng 1 POST**, thân bắt đầu bằng
  ``**Lease `wp-ok-1`**``. Nó là thứ làm giàn hỏng không thể xanh (§2.1).
- **M5** — Docstring của ca nêu:
  - (a) bảng trục đã đo, theo §2.2;
  - (b) vì sao tập (i) khoá dãy lời gọi: đó là **tín hiệu phân biệt** của `L`, không phải vì lượt GET thừa nguy hiểm;
  - (c) vì sao tập (ii) chỉ khoá mã thoát;
  - (d) trỏ #678 cho các dạng ép kiểu **được đăng**;
  - (e) bảng tiền đề §2.6 và các trục che mất độ phân biệt (lỗi kép).

  Mọi câu khai phải nêu phép đo đứng sau nó, hoặc nói thẳng `KHÔNG ĐO ĐƯỢC`.

- **M6** (r2; r3 hạ vai trò) — Mở rộng `t70` để đếm các ca đọc thân bước qua **cả hai** helper (`_chay_buoc_dang` và
  `_chay_buoc_dang_that`). Con số ghim tăng đúng bằng số ca mới gọi helper mới. `t70` nằm ngoài tập A8 (A8 chỉ
  khoá `_chay_buoc_dang` và `t51`–`t68`), nên sửa nó không trái A8. **M6 là KIỂM KÊ, không phải bằng chứng nhánh**:
  lượt 2 đo được guard sai (chỉ xét `os.name`) vẫn qua `t70` đã mở rộng (`count=8`). Bằng chứng nhánh là A9(b).

## 7. `nghiem_thu`

Mọi đột biến chạy trên **BẢN SAO TẠM** của cây (CLAUDE.md), bằng `python ops/lease_publish_test.py --chi-ca=<tên ca>`.
Ca đỏ được đọc từ dòng `ĐỎ  <tên>: <lý do>`.

| mã | tiêu chí | phép đo làm nó ĐỎ |
|---|---|---|
| **A1** | Tập (i) (M2) xanh trên nền | Đột biến **`L`** ⇒ ca M2 **ĐỎ**, lý do nêu dãy lời gọi (0 → 1 GET `comments`). Không được đỏ vì ngoại lệ vô can. |
| **A2** | Tập (ii) (M3a và M3b) xanh trên nền | Đột biến **`L`** ⇒ ca M3 **ĐỎ** qua **mã thoát** ở **cả hai họ** (nền `rc=1` → `L` `rc=0` + dòng "bỏ qua"). Người thi hành ghi dòng `ĐỎ` cho từng họ. Đây là tiêu chí chính của packet (Q8, Q12). Độ phân biệt này **neo vào revision sản phẩm tại `start_from_sha`** — xem §10.5. |
| **A3** | Đối chứng dương (M4) xanh | Đột biến **`gh` giả không nằm trên PATH** (chỉ thay chuỗi trong thân bước, như lỗi của §2.1) ⇒ ca M4 **ĐỎ**. |
| **A4** | Đối chứng dương đo POST thật | Đột biến **`gh` giả in id nhưng KHÔNG ghi comment vào trạng thái** ⇒ ca M4 **ĐỎ** ở chốt "đúng 1 POST". |
| **A5** | Mỗi đột biến A1–A4 đỏ **đúng lý do** | Với mỗi đột biến: ca đỏ phải là **đúng ca đích**, và lý do phải là **thông điệp chốt tường minh của ca**, không phải `AttributeError`/`KeyError`/`FileNotFoundError`… (hình dạng `GIET-NHUNG-KHONG-DUNG-LY-DO`). Người thi hành ghi nguyên dòng `ĐỎ` cho từng đột biến. |
| **A6** | Không hồi quy | Toàn suite `python ops/lease_publish_test.py` ⇒ dòng tổng kết `N/N` với **N = số `@ca` đếm tĩnh**, hai số bằng nhau. Nền 187 ca (đếm `^@ca`), đo 07:57Z trên `1741e0a`, 08:05Z và 10:06Z trên `89fc4fa`; đo lại lúc thi hành. |
| **A7** | Write set đúng một tệp + trần kích thước (viết lại ở r7, C-P2b) | **(1)** `git diff --name-only <start_from_sha>...HEAD` (KHÔNG lọc đường dẫn; `start_from_sha` lấy từ lease đang hiệu lực) ⇒ tập đường dẫn **bằng đúng** `{ops/lease_publish_test.py}`. Tệp merge từ master về không tính, vì so với `start_from_sha` mới — nếu nhánh đã merge master thì dùng `git diff --name-only <merge-base mới nhất với master>...HEAD` và ghi rõ merge-base ấy. **(2)** `git diff --numstat` trên cùng phạm vi ⇒ **≤ 600** dòng thêm (Q19, r8; r7 là 300). Phản chứng: thêm một tệp `.py` bất kỳ vào bản sao nhánh ⇒ (1) ĐỎ. |
| **A8** | Không đụng giàn cũ (viết lại ở r7, C-P2c) | `_chay_buoc_dang` và `t51`–`t68` **bằng byte** với bản trong `ops/lease_publish_test.py` tại **`start_from_sha` của lease đang hiệu lực** (OID đầy đủ, `git show <start_from_sha>:ops/lease_publish_test.py`), cắt theo `ast` rồi so byte — KHÔNG so với `origin/master` (mốc trôi). `--chi-ca=t5` và `--chi-ca=t6` xanh. Nếu nhánh phải merge master mà master đã đổi các khối ấy (ví dụ #687 land trước), đó là việc của **generation mới** với `start_from_sha` mới, không lặng lẽ chấp nhận. |
| **A9** | Bỏ qua nền đúng chỗ (viết lại ở r3, R2-F1) | **(a)** Trên Linux, `--chi-ca=<tiền tố ca mới>` cho dòng tổng kết `đã chạy=k, bỏ qua=0` và `k/k đạt` — ca THẬT SỰ chạy. **(b)** Một ca meta gọi helper **qua điểm dò** (M1) ở ba trạng thái, mỗi trạng thái đặt `os.name` và `WORKFLOW_DANG` bằng `mock.patch`: **S1** posix + workflow thật ⇒ qua guard; **S2** `nt` + workflow thật (job chỉ Ubuntu) ⇒ `BoQuaNen`, và `_ly_do_bo_qua_workflow` dẫn xuất được lý do `chỉ chạy Ubuntu`; **S3** `nt` + workflow **tạm** có `runs-on: ${{ matrix.os }}` với matrix `[ubuntu-latest, windows-latest]` ⇒ qua guard. Ba đột biến guard, mỗi cái phải làm ca meta ĐỎ ở đúng trạng thái của nó: *luôn ném* ⇒ S1 (và S3) · *gỡ guard* ⇒ S2 · *chỉ xét `os.name`* ⇒ S3. Lượt soạn đã dựng thử thiết kế này ngoài kho (khoảng 10:24Z 29-09, `89fc4fa`): guard đúng đạt cả S1/S2/S3; *luôn ném* đỏ S1+S3; *gỡ guard* đỏ S2; *chỉ xét nt* đỏ S3. Mô phỏng `os.name` **không** được khai là đã chạy Windows thật. |
| **A10** | Cổng phụ | `ruff check --select F ops/lease_publish_test.py`: **delta so master = 0**. `doctrine-scan`, `adr-song`, `git diff --check`: rc=0. |
| **A11** (r8, L1 lượt 2) | Mỗi đường vào L1-E1…E13 của verdict lượt 2 có một phản chứng riêng | Tập ô M2/M3 được xác minh trên **đầu vào thật** truyền cho giàn (kiểu raw/dấu của ánh xạ, `la_pr`, comment có dấu, `het_han`, kiểu ngày), không chỉ trên nhãn; `_lech_m4` khoá `startswith` ở vị trí đầu và mọi `rc ≠ 0`; `gh` giả: GET sau POST có rc=0, thân lưu nguyên vẹn, tác giả là bot; guard `nt` + matrix Ubuntu/Windows với điểm dò TẮT phải tới I/O. Đột biến N1–N13 (bảng L1 lượt 2) mỗi cái làm ĐỎ đúng ca đích bằng `TinHieuChotCa`/`chot()`; không tín dụng từ ngoại lệ vô can. |

## 8. `ngoai_pham_vi`

1. **Các dạng `lease_id` ép kiểu được ĐĂNG** (Issue, chưa có dấu: `true`/`yes`/`on` → `True`, `1.50` → `1.5`,
   `0x1F` → `31`, `017` → `15`, date) và **va chạm danh tính** giữa chúng. Đó là packet **#678** `LEASE-ID-EP-KIEU-YAML`.
   Khoá hành vi "được đăng" ở đây là chôn lỗi vào test (Q2).
2. **Giới hạn đã khai của nhánh đã-có-dấu**: nó bỏ `_kiem_loai_so_hieu`, nên **chuỗi hợp lệ** + PR + có dấu vẫn ra
   `rc=0` bỏ qua, ở CẢ nền lẫn `L` (đo 08:01Z 29-09). Đây là đánh đổi có chủ đích của #579, không do `L`. Packet này không đổi nó.
3. **Sửa `ops/lease_publish.py`**: nền đúng (Q8).
4. **Sửa `.github/workflows/**`**.
5. **Đo trên endpoint HTTP thật của GitHub**: xem §10.

## 9. Lease — điều kiện trước khi cấp

Đo 10:26Z 29-09-2026, sau khi so `ls-remote` 512 với `for-each-ref` 512, thiếu 0, master cục bộ khớp `origin/master`
`89fc4fa`: `ai-dang-giu ops/lease_publish_test.py` ⇒ **`NGƯỜI_GIỮ 1`** — `lease-publish-windows-do-r1-g1-claude`
(packet **#687** `LEASE-PUBLISH-WINDOWS-DO`, `granted_by: ducthangho`, cấp `2026-09-29T10:20:00Z`, hết hạn
`2026-09-30T10:20:00Z`, ref `origin/claude/lease-publish-windows-do`).

Lịch sử: lease của #676 giữ tệp tới khi bị thu hồi bằng rút hạn về 08:15Z; 09:11Z và 10:06Z đo `NGƯỜI_GIỮ 0`; lease
#687 cấp 10:20Z. Thứ tự "#677 trước #678" (Q7/Q10) **không** nói gì về #687 — xếp #677 so với #687 là việc của chủ kho.

**Bất biến (neo quyết định vào đây, không vào con số):** chỉ cấp lease cho #677 khi `ai-dang-giu ops/lease_publish_test.py`
cho `NGƯỜI_GIỮ 0`, đo trên đủ ref ngay trước lúc cấp. `start_from_sha` là `origin/master` **tại lúc cấp** — nếu #687
land trước thì `start_from_sha` sẽ chứa mã của #687, và A6/A7/A8 đo lại trên nền ấy. Lease neo revision **cuối cùng**
của spec này đã qua cross-review, không neo r1/r2.

## 10. `chua_do_duoc`

1. **Các tổ hợp §2.3 có xảy ra ngoài đời không** — hai nhóm, trả lời khác nhau (r5, R4-F1):
   - **Nhóm PR** (8 trong 15 dòng lệch mã thoát: PR + có dấu, còn hạn hoặc hết hạn). Cần một comment của
     `github-actions[bot]` **trên một PR**, bắt đầu đúng bằng ``**Lease `True`**`` (hoặc `1.5`, ngày…). Workflow đăng
     lease có đăng được lên PR với `issues: write` hay không là `KHÔNG ĐO ĐƯỢC` từ phiên này: không có REST tới
     `repos/…`, và thử bằng cách đăng thật là ghi ra ngoài.
   - **Nhóm Issue** (7 dòng: Issue + có dấu + hết hạn, 4; Issue + có dấu + GET loại số hiệu lỗi, 3). Dấu bot trên
     Issue là thứ workflow **tự sinh** — §2.4 đo trong giàn: `true`/`1.5`/ngày + Issue trống + còn hạn cho `rc=0` và
     đúng 1 POST ở cả hai vế. Đó là **mô phỏng** qua `gh` giả; trên GitHub thật (HTTP) chưa đo.
   Q8 xếp nguy hiểm **bất kể** cả hai câu này.
2. **Endpoint HTTP thật.** Mọi phép đo đi qua `gh` giả. Hình dạng phản hồi thật của `gh api --paginate --slurp`
   chỉ được mô phỏng, theo đúng dạng mà `_kiem_comment_da_co` chấp nhận.
3. **Windows.** Ca bỏ qua trên Windows (Q6), nên hành vi của giàn trên Windows `KHÔNG ĐO`: đây là **chọn không đo**.
4. **Sau #676.** #676 có thể đổi số ca và vị trí dòng trong tệp. A6/A7 phải đo lại lúc thi hành.
5. **A2 sau #678.** Reviewer lượt 1 đo: chèn chốt kiểu nghiêm hơn vào `kiem()` ở **cả hai** bản nguồn tạm thì M3 nền
   và M3 `L` đều xanh — tức khi #678 sửa kiểu, `L` có thể thành **tương đương về mã thoát** ở M3. Đó là đúng: khi
   `kiem()` tự từ chối dạng ép kiểu thì chốt `lease_id` của tiền kiểm không còn là hàng rào duy nhất. M3 vẫn đúng sau
   #678; A2 chỉ cam kết giết `L` trên **revision tại `start_from_sha`**, không cam kết mãi mãi.

## 11. `hinh_dang_ke_thua`

Chép từ `ops/specs/dang-lease-dau-truoc-kiem-sau-r30.md` §6 (packet cha #579), cộng phần phát sinh ở lượt soạn này:

| hình dạng | số lần | nguồn |
|---|---|---|
| `LOI-KHAI-RONG-HON-PHEP-DO` | 6 → 7 → 8 → 9 → 10 → **12** | **+1** ở r1: *"vô hại cho cả 13 dạng"* đo trên 2 trục, thiếu trục loại số hiệu (§2.5). Chủ kho (Q11) cho tiếp, kèm luật khai trục. **+1** ở r2 (F4): *"log hai vế chỉ lệch dấu thời gian"* — bộ phân loại không so log, và chính bốn dòng lệch mã thoát lệch cả log. F1 **không** tính: kết luận r1 đã khai đúng phạm vi trục, và reviewer tìm trục thiếu đúng như Q11 giao. **+1** ở r3 (R2-F3): r2 ghi `73 / 5` như một số ổn định trong khi giàn dựng đầu vào hai lần, nên số ấy không tái lập. R2-F2 **không** tính, cùng lý do như F1. **+1** ở r6 (R5-F1): R4-F1 — §10.1 của r1–r4 khai "tổ hợp §2.3 cần comment bot trên PR" trong khi 7/15 chứng nhân nằm trên Issue (lượt 4, `e601b22`). r5 vá câu ấy mà quên cộng vào đây; chính lượt 5 bắt được. R3-F1 **không** tính (trục mới, loại theo Q13, không phải lời khai sai). **+2** ở r7: C-P2b — A7 khai "không tệp nào khác trong diff mã" trong khi lệnh của nó lọc theo đường dẫn nên không đo được điều ấy; C-P2e — nhãn "(r2: …28701faf)" khai sai revision. |
| `THOI-DIEM-DO-GAN-SAI` | **1** | MỚI. Vòng 1 của lượt soạn gắn mốc *"đo 06:4xZ"* cho `NGƯỜI_GIỮ 0`, trong khi số ấy đo **trước** 06:05Z. Lease #676 cấp 06:05Z, nên quyết định Q7 được đưa ra trên một số đã chết. |
| `GIET-NHUNG-KHONG-DUNG-LY-DO` | 2 | Chép. Chống bằng A5. |
| `VA-DUNG-CHO-DUOC-CHI-ROI-BO-SOT-DUONG-THU-BA` | 2 | Chép. |
| `VUOT-TRAN-REVIEW-THEO-QUAN-TINH` | **1** | MỚI ở r7 (C-P1). Phiên điều phối gọi codex lượt 3–6 trên PR #684 theo chỉ thị "lặp tới khi 0 P1/P2/P3" mà không đối chiếu trần 2 lượt/PR của protocol §8/§12. Connector codex bắt được. Chữa bằng Q14/Q15 (checkpoint có quyết định chủ kho). |
| `NEO-VAO-REF-TROI` | **1** | MỚI ở r7 (C-P2c): A8 so với `origin/master`, một ref trôi — và nó đã trôi thật trong packet (`89fc4fa` → `1c23933`). |
| `PHEP-DO-GHI-VAO-CAY-DUOC-DO` | **1** | MỚI ở r7 (C-P2d): lệnh tái lập của Phụ lục A ghi `do_bien_L.py` và `.pyc` vào chính checkout mà reviewer phải giữ read-only. |
| `DEM-SU-CO-MAT-THAY-VI-KHA-NANG` | 1 → 2 → **3** | Chép 1. **+1** ở r2 (F3): A9 của r1 đo sự **vắng mặt** của dòng `BỎ QUA`, trong khi bộ chạy vốn đã đổi mọi lượt bỏ qua sai thành ĐỎ — tiêu chí không thể đỏ vì đúng lý do nó khai. (Giàn hỏng §2.1 vẫn không tính: bắt được trước khi thành lời khai.) **+1** ở r3 (R2-F1): r2 dùng M6 — một phép **đếm** ca trong tầm `t70` — làm bằng chứng cho nhánh "nt + matrix có Windows". Cùng lúc đó là một lần vá hẹp (`VA-DUNG-CHO-DUOC-CHI-ROI-BO-SOT-DUONG-THU-BA`), nhưng chỉ đếm một lần, vào hình dạng gốc. |
| `CHOT-DO-SAI-TOAN-TU` | 1 | Chép. |
| `DOT-BIEN-SONG-SOT-VI-NHANH-CHUA-AI-CHAM` | 1 | Chép. |
| `TIN-HIEU-DO-CHINH-MA-TEST-GIA-MAO` | 2 | Chép. |
| `VA-BANG-REGEX-RONG-HON-Y-DINH` | 1 | Chép. |

## 12. Việc của reviewer (Q11)

**r7: KHÔNG còn lượt codex nào trên PR #684 (Q14).** Mục này giữ lại cho human audit và làm hồ sơ; reviewer mã của
PR #689 áp nó cho code theo trần Q15.

Ngoài review thường lệ, reviewer phải **tìm trục còn thiếu** trong §2.2. Mỗi trục mới mà làm một kết luận của §2.3
hoặc của ca M2/M3 đổi thì là một finding.

Lượt 1 đã thử (xem §2.6): `packet_issue` sai kiểu × `lease_id` sai kiểu; trang hai của `--paginate`; hết hạn (thành
trục của r2); tự cấp; neo prompt; schema v2 thiếu lớp; SHA sai; API `comments` lỗi; `yes` với dấu sau parse; siết
kiểu theo hướng #678.

Lượt 2 đã thử (xem §2.6, §2.3): GET loại số hiệu lỗi (thành trục bổ sung của r3); comment hỏng trước/sau dấu; phân
trang phẳng/rỗng/lẫn kiểu; hạn sai cú pháp; con trỏ trường treo; `thay_the_cho` sai kiểu; scalar YAML khác; `role`
rỗng; guard nền với matrix hỗn hợp (thành A9 của r3); hai vế cùng/khác byte đầu vào (thành R2-F3).

Lượt 3 đã thử: snapshot `comments` đổi giữa các GET và lỗi một lần rồi phục hồi (thành R3-F1, loại theo Q13); bước
đăng nhiều tệp với tệp thứ hai hỏng SHA; POST lỗi trước/sau khi lưu; GET loại số hiệu thành công nhưng JSON thiếu/sai
cấu trúc; YAML khoá trùng và merge alias; cùng các đối chứng của lượt 1–2.
Lượt sau nên thử trục **khác** các trục ấy.

---

## Phụ lục A — giàn đo của lượt soạn (chép nguyên văn)

Chạy: `python do_bien_L.py <gốc kho> [kq.json]`. Bảng in ra stderr; cột cuối `KHAC-RC` / `KHAC-GOI` / `=`
(so trên bộ `(rc, goi, dang)`, không so log — xem §2.3). Cột thứ hai có tiền tố `HH-` cho ô hết hạn và
`LOI-ISSUE-` cho trục bổ sung. Dòng cuối `LOG …` tổng kết log hai vế.
Giàn **không** thuộc write set. Nó chỉ là bằng chứng tái lập của §2. Ca M1–M4 thay nó trong kho.

**Trích đúng khối — bẫy đã gặp:** tệp này có HAI khối `python`. Khối ở §1 là hai dòng chốt; giàn là khối
**CUỐI**. Lượt soạn r1 đã trích nhầm khối đầu và nhận `IndentationError`. Lệnh đúng (r3–r7: sha256 của khối trích ra
phải là `28701faf…feb2`, và chạy cho `KHAC-GOI 61 · KHAC-RC 15 · = 19` cùng dòng
`LOG KHONG-RC/byte-bang=80 RC/noi-dung-khac=15`). r7 (C-P2d): trích và chạy **trong thư mục tạm ngoài checkout**,
interpreter `-B`, nên checkout không nhận `do_bien_L.py` hay `__pycache__` nào; chạy từ gốc kho:

```
D="$(mktemp -d)"; python -B -c "import sys;s=open(sys.argv[1],encoding='utf-8').read();open(sys.argv[2],'w',encoding='utf-8').write(s.rsplit(chr(96)*3+'python\n',1)[1].rsplit(chr(96)*3+'\n',1)[0])" ops/specs/dot-bien-l-bien-cong-khai-r7.md "$D/do_bien_L.py" && python -B "$D/do_bien_L.py" "$PWD" "$D/kq.json"; echo "thu muc tam: $D"
```

```python
"""Đo đột biến L ở BIÊN workflow `ops-publish-lease.yml` bước `đăng`.

Chạy thân bước TRÍCH TỪ YAML với `ops/lease_publish.py` THẬT (nền và L, bản sao tạm),
và một `gh` giả GIỮ TRẠNG THÁI (issue, comments; POST thêm comment vào state).
Ghi: lời gọi gh theo (method, endpoint), rc bước, comment đã đăng, stdout/stderr.
"""
import json, os, re, subprocess, sys, tempfile
from pathlib import Path

if len(sys.argv) < 2:
    sys.exit("dùng: python do_bien_L.py <gốc kho> [tệp kết quả .json]")
KHO = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(KHO / "ops"))
import lease_publish_test as T  # noqa: E402
import yaml  # noqa: E402

THAN = T._buoc_workflow("đăng")["run"]
GOC_SRC = (KHO / "ops" / "lease_publish.py").read_text(encoding="utf-8")
DONG_L = ('    if not isinstance(lease.get("lease_id"), (str, int)) or isinstance(lease.get("lease_id"), bool):\n'
          '        raise Chan(RC_NOI_DUNG, "tiền kiểm: thiếu `lease_id` hoặc sai kiểu")\n')
assert GOC_SRC.count(DONG_L) == 1, "không định vị được chốt lease_id"
BIEN_THE = {"nen": GOC_SRC, "L": GOC_SRC.replace(DONG_L, "")}

GH_GIA = r'''
import json, os, pathlib, sys
a = sys.argv[1:]
assert a[0] == "api", a
a = a[1:]
st = pathlib.Path(os.environ["GH_STATE"]); d = json.loads(st.read_text())
log = pathlib.Path(os.environ["GH_LOG"])
ep = [x for x in a if x.startswith("repos/")][0]
method = "POST" if "--input" in a else "GET"
with log.open("a") as f: f.write(json.dumps([method, ep, a]) + "\n")
parts = ep.split("/")  # repos o r issues N [comments]
so = parts[4]
iss = d["issues"].get(so)
if iss is None:
    print('{"message":"Not Found"}'); print("gh: Not Found (HTTP 404)", file=sys.stderr); sys.exit(1)
if len(parts) == 5 and iss.get("issue_loi"):
    print("gh: Server Error (HTTP 500)", file=sys.stderr); sys.exit(1)
if len(parts) == 5:
    loai = "pull" if iss.get("pr") else "issues"
    print(json.dumps({"number": int(so), "html_url": f"https://github.com/o/r/{loai}/{so}"})); sys.exit(0)
if method == "GET":
    print(json.dumps([iss["comments"]])); sys.exit(0)
body = json.loads(pathlib.Path(a[a.index("--input") + 1]).read_text())["body"]
cid = 7000 + len(iss["comments"])
iss["comments"].append({"id": cid, "body": body, "user": {"login": "github-actions[bot]"}})
st.write_text(json.dumps(d)); print(cid)
'''


def yaml_lease(lid_raw, bo_lease_id=False, packet_issue=55, top_list=False, het_han=False):
    d = T.lease_mau(packet_issue=packet_issue)
    if het_han:
        from datetime import datetime, timedelta, timezone
        d["lease_expires_at_utc"] = (datetime.now(timezone.utc) - timedelta(hours=1)).strftime("%Y-%m-%dT%H:%M:%SZ")
    d.pop("lease_id")
    van = yaml.safe_dump(d, allow_unicode=True, sort_keys=False)
    if not bo_lease_id:
        van += f"lease_id: {lid_raw}\n"
    if top_list:
        van = "- " + van.replace("\n", "\n  ").rstrip() + "\n"
    return van


def chay(bien_the, van_yaml, comments_san, la_pr=False, issue_loi=False):
    with tempfile.TemporaryDirectory() as t:
        goc, neo = Path(t) / "goc", Path(t) / "neo"
        (goc / "ops" / "leases").mkdir(parents=True); (neo / "ops").mkdir(parents=True)
        (neo / "ops" / "lease_publish.py").write_text(BIEN_THE[bien_the], encoding="utf-8")
        (neo / "gh_gia.py").write_text(GH_GIA, encoding="utf-8")
        (goc / "ops" / "leases" / "x.yaml").write_text(van_yaml, encoding="utf-8")
        (goc / "ds.txt").write_text("ops/leases/x.yaml\n", encoding="utf-8")
        st, log = Path(t) / "st.json", Path(t) / "gh.log"
        st.write_text(json.dumps({"issues": {"55": {"comments": list(comments_san), "pr": la_pr, "issue_loi": issue_loi}}}))
        log.write_text("")
        py = sys.executable
        than = THAN.replace("python3 ", f"'{py}' ")
        assert "python3 " not in than and than.count("gh api ") == 1
        bin_ = Path(t) / "bin"; bin_.mkdir()
        (bin_ / "gh").write_text(f"#!/bin/sh\nexec '{py}' '{neo}/gh_gia.py' \"$@\"\n")
        (bin_ / "gh").chmod(0o755)
        mt = dict(os.environ, NEO=str(neo), REPO="o/r", GITHUB_REPOSITORY="o/r",
                  GITHUB_ACTOR="ducthangho", GH_TOKEN="gia", GH_STATE=str(st), GH_LOG=str(log),
                  PYTHONDONTWRITEBYTECODE="1", PATH=f"{bin_}:{os.environ['PATH']}")
        p = subprocess.run(["bash", "-c", than], cwd=goc, env=mt, capture_output=True, text=True)
        goi = [tuple(json.loads(x)[:2]) for x in log.read_text().splitlines()]
        sau = json.loads(st.read_text())["issues"]["55"]["comments"]
        moi = sau[len(comments_san):]
        return {"rc": p.returncode, "goi": goi, "dang": [c["body"].splitlines()[0] for c in moi],
                "out": (p.stdout + p.stderr)}


def bot(body):
    return {"id": 1, "body": body, "user": {"login": "github-actions[bot]"}}


FIX = [
    # nhãn, yaml lease_id, dấu mà str() của giá trị Python sẽ dựng
    ("null", "null", "None"),
    ("~ (null)", "~", "None"),
    ("list", "[wp579-thu]", "['wp579-thu']"),
    ("bool true", "true", "True"),
    ("bool yes? (YAML1.1 safe_load: str)", "yes", "yes"),
    ("mapping", "{x: 1}", "{'x': 1}"),
    ("float 1.5", "1.5", "1.5"),
    ("float 1.50", "1.50", "1.5"),
    ("date", "2026-09-29", "2026-09-29"),
    ("int (hợp lệ ở tiền kiểm)", "123", "123"),
    ("str hợp lệ (đối chứng)", "wp-ok-1", "wp-ok-1"),
]

if __name__ == "__main__":
    kq = []
    for nhan, raw, dau_str in FIX:
     for het_han in (False, True):
      for la_pr in (False, True):
        for tt, san in (("trong", []),
                        ("co-dau-bot", [bot(f"**Lease `{dau_str}`** — đăng tự động")])):
            dong = {"fixture": nhan, "yaml": raw,
                    "issue": ("HH-" if het_han else "") + ("PR-" if la_pr else "issue-") + tt}
            # r3 (R2-F3): dựng YAML MỘT lần cho mỗi cặp — hai vế nhận CÙNG byte đầu vào.
            van = yaml_lease(raw, het_han=het_han)
            for bt in ("nen", "L"):
                dong[bt] = chay(bt, van, san, la_pr)
            kq.append(dong)
    # r3 (R2-F2): trục bổ sung — GET issues/55 (loại số hiệu) LỖI; Issue, có dấu, còn hạn.
    for nhan, raw, dau_str in [x for x in FIX if x[1] in ("true", "1.5", "2026-09-29", "null", "wp-ok-1")]:
        dong = {"fixture": nhan, "yaml": raw, "issue": "LOI-ISSUE-issue-co-dau-bot"}
        van = yaml_lease(raw)
        for bt in ("nen", "L"):
            dong[bt] = chay(bt, van, [bot(f"**Lease `{dau_str}`** — đăng tự động")], False, issue_loi=True)
        kq.append(dong)
    for tt, san in (("issue-trong", []),):
        for nhan, van in (("thiếu lease_id", yaml_lease(None, bo_lease_id=True)),
                          ("tài liệu là danh sách", yaml_lease("wp-ok-1", top_list=True))):
            dong = {"fixture": nhan, "yaml": "-", "issue": tt}
            for bt in ("nen", "L"):
                dong[bt] = chay(bt, van, san)
            kq.append(dong)
    json.dump(kq, open(sys.argv[2] if len(sys.argv) > 2 else "/dev/stdout", "w"),
              ensure_ascii=False, indent=1)
    print(f"{'fixture':38} {'issue':17} | nền: rc goi dang | L: rc goi dang | KHÁC?", file=sys.stderr)
    for d in kq:
        n, l = d["nen"], d["L"]
        tom = lambda r: f"{r['rc']} {[g[0][0]+':'+g[1].split('/',3)[3] for g in r['goi']]} {len(r['dang'])}"
        khac = (n["rc"], n["goi"], n["dang"]) != (l["rc"], l["goi"], l["dang"])
        # `=` nghĩa là BẰNG NHAU trên bộ (rc, goi, dang) — KHÔNG so byte stdout/stderr (r2, F4).
        nhan = "KHAC-RC" if n["rc"] != l["rc"] else "KHAC-GOI" if khac else "="
        print(f"{d['fixture']:38} {d['issue']:20} | {tom(n)} | {tom(l)} | {nhan}",
              file=sys.stderr)
    # r3 (R2-F3): tổng kết log TỪ CHÍNH GIÀN — tách dòng lệch mã thoát khỏi dòng không lệch.
    import collections
    chuan = lambda x: re.sub(r"\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d(Z|\+00:00)", "<T>", x)
    dem = collections.Counter()
    for d in kq:
        n, l = d["nen"], d["L"]
        lop = "RC" if n["rc"] != l["rc"] else "KHONG-RC"
        dem[(lop, "byte-bang" if n["out"] == l["out"] else
             "chi-lech-moc-T" if chuan(n["out"]) == chuan(l["out"]) else "noi-dung-khac")] += 1
    print("LOG " + " ".join(f"{a}/{b}={v}" for (a, b), v in sorted(dem.items())), file=sys.stderr)
```
