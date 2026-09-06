# Đặc tả packet — LO-319-LINUX-BANG-CHUNG-XANH

- `packet_id`: **LO-319-LINUX-BANG-CHUNG-XANH**
- `packet_issue`: **(để trống — chủ kho cấp)**
- `revision`: 1
- `generation`: 1
- `executor`: claude · `environment`: cloud
- `review_class`: **sensitive** (sửa CHÍNH vị từ quyết định xanh/đỏ của một cổng CI; không rõ ⇒ lấy mức chặt nhất)
- `base_sha`: `1b3caa1` (`origin/master`, đo 17:47Z 06-09-2026; `core.abbrev=7`)

## `nguon_cap_viec`

Packet **khắc phục**. Không phải một dòng trong bảng packet của
`ops/KE_HOACH_THI_CONG_CLAUDE_CODEX.md`.

Nguồn: `ops/specs/MUTANT-KHONG-CHAY-TREN-WINDOWS.md` mục `ngoai_pham_vi` #1 và khối chú thích
`.claude/dev/ci_dang_ky_test.py:35-38` — cả hai khai thẳng rằng lỗ #319 phía **Linux** CÓ THẬT,
có sẵn từ trước packet #456, và bị để lại **có chủ đích** vì M4 của #456 đóng băng hành vi Linux.
Cross-review Codex lượt 1 của #456 bắt đúng chỗ này (finding P2) và bản vá đã phải lùi lại
(`426bfc0` — *"trả mẫu Linux về nguyên bản, dời chốt số dương sang đường Windows"*).

Packet này là chỗ M4 ấy được **gỡ đóng băng có thẩm quyền**, không phải chỗ nó bị lách.

## Bối cảnh đo được (mọi số kèm thời điểm)

### Lỗ là gì, đo bằng lời gọi thật

`bang_chung_xanh(text, mau)` (`.claude/dev/ci_dang_ky_test.py:205`) chỉ soi **hai nhóm bắt** của
regex — mà ở `MOI` hai nhóm ấy là cặp số **CA**. Cặp số **đột biến** nằm ngoài nhóm bắt
(`DOT BIEN \d+/\d+ bi giet`) nên **không bao giờ được nhìn tới**.

Đo 17:45Z 06-09-2026 trên `1b3caa1`, gọi thẳng `bang_chung_xanh`:

| đầu vào (nền Linux) | mẫu `MOI` hiện tại | đúng ra phải |
|---|---|---|
| `TONG: CA 39/39 dat · DOT BIEN 34/34 bi giet` | `True` | `True` |
| `TONG: CA 39/39 dat · DOT BIEN 0/0 bi giet` | **`True`** ← LỖ | `False` |
| `TONG: CA 0/39 dat · DOT BIEN 34/34 bi giet` | `False` | `False` |

`DOT BIEN 0/0 bi giet` là đúng hình dạng *"tập rỗng thoả `not song`"* mà bài học **#319** sinh ra
để chặn.

### Lỗ chạm MẤY mục, không phải một

Đo 17:44Z 06-09-2026 — đếm theo **số mục trong `MOI`** (8 mục) và theo **số cặp `n/m` được KIỂM
trong span khớp**:

| mục `MOI` | số nhóm bắt | cặp `n/m` có trong span | cặp được KIỂM hôm nay |
|---|---:|---:|---:|
| `chon_reviewer_test.py` | 2 | 1 (`25/25`) | 1 |
| `gh_readback_test.py` | 2 | 1 (`8/8`) | 1 |
| `mcp_gh_test.py` | 2 | 2 (`42/42`, `54/54`) | 1 |
| `mcp_github_doc_test.py` | 2 | 1 (`17/17`) | 1 |
| `probe_mang_test.py` | **0** | 3 (`9/9`, `1/1`, `11/11`) | **0** |
| `pretooluse_guard_test.py` | 2 | 2 (`39/39`, `34/34`) | 1 |
| `subagent_ghi_detect_test.py` | 2 | 2 (`33/33`, `22/22`) | 1 |
| `nhanh_don_duoc_test.py` | 2 | 1 (`8/8`) | 1 |
| **tổng** | | **13** | **7** |

Bảy dòng đầu tiên của cột "cặp có trong span" đo trên **bản in THẬT** của bảy bộ chạy trong
container này lúc 17:39–17:47Z; dòng `pretooluse_guard_test.py` đo trên **dòng canonical của CI**
(`0c5e889` khai `CA=39, DOT_BIEN=34`) chứ **không** trên bản in của container này — bộ ấy ở đây
`rc=1` với 3 ca đỏ sẵn (xem `chua_do_duoc` #2), nên mẫu không khớp và không đo được tại chỗ.

Nên câu đúng **không** phải *"một mục bị hở"* mà là: **hai** mục (`pretooluse_guard_test.py`,
`subagent_ghi_detect_test.py` — cùng một regex, hai dòng kề nhau trong `MOI`) mang cặp đột biến
không ai canh, và **6 trong 13** cặp bằng chứng của cả sổ đăng ký chưa từng được kiểm.

### Hai hướng vá, ĐO CẢ HAI rồi mới chọn

Đơn vị: **số phản chứng trong `phan_chung()` đổi màu** (nền `1b3caa1` = `51/51` đỏ đúng, đo
17:46Z trong CÂY THẬT — đo trong bản sao ngoài cây cho `47/51` vì `ROOT = parents[2]` giải sai,
đó là **tạo tác rig**, không phải hồi quy) và **số mẫu regex phải sửa**.

| hướng | mẫu phải sửa | phản chứng đổi màu | bịt được lỗ? |
|---|---:|---:|---|
| **A-a** — `bang_chung_xanh` soi các nhóm bắt THEO CẶP | 0 | **0** (`51/51`) | **KHÔNG** — mẫu vẫn không bắt cặp đột biến |
| **A-b** — `bang_chung_xanh` soi **mọi** cặp `n/m` trong span khớp | **0** | **1** (`50/51`) | **CÓ** |
| **B-tự nhiên** — thêm nhóm bắt cho cặp đột biến (4 nhóm) | 2 | — | **KHÔNG — HỒI QUY** (xem dưới) |
| **B-thật** — siết từng mẫu thành `[1-9]\d*/[1-9]\d*` | 2 | **3** | CÓ, nhưng chỉ cho 2 mẫu ấy |

**B-tự nhiên là một cái BẪY, đo được:** mệnh đề `len(m.groups()) != 2` trong `bang_chung_xanh`
trả `True` **vô điều kiện** cho mọi mẫu có số nhóm khác 2. Nên cách hiển nhiên nhất để "canh cặp
đột biến" — bắt nó thành nhóm 3/4 — làm hàm **ngừng kiểm cả cặp CA**:

```
mẫu 2 nhóm, "CA 0/39 · DOT BIEN 0/0"  -> False   (đúng)
mẫu 4 nhóm, "CA 0/39 · DOT BIEN 0/0"  -> True    (SAI — đo 17:45Z 06-09-2026)
```

Hôm nay chưa mẫu nào có 1/3/4 nhóm nên mệnh đề ấy **đang ngủ**; nó thức dậy đúng lúc ai đó vá
theo hướng hiển nhiên. Đây là lý do quyết định: **lỗ phải được bịt ở `bang_chung_xanh`**, vì
hướng B để lại một cái bẫy nạp sẵn ngay trên đường mà người vá tiếp theo sẽ đi.

**A-b không sinh đỏ giả, đo được:** **11 lần xuất hiện** của `n/m` nằm trong span khớp của bảy
bản in thật (**10 chuỗi phân biệt**: `25/25` · `8/8` ×2 · `42/42` · `54/54` · `17/17` · `9/9` ·
`1/1` · `11/11` · `33/33` · `22/22`) — **không cặp nào** vi phạm "dương và bằng nhau". Số cặp
được KIỂM đi từ **6 lên 11** trên bảy bộ ấy, và từ **7 lên 13** trên cả tám khi tính dòng
canonical của `pretooluse_guard_test.py`.
Đơn vị: **số LẦN XUẤT HIỆN** của mẫu `\d+/\d+` trong span, không phải số chuỗi phân biệt — hai
bộ cùng in `8/8` là hai lần xuất hiện, hai phép kiểm.

**A-b cũng không đụng đường Windows:** dòng `MOI_WINDOWS`
(`DOT BIEN [1-9]\d* muc KHONG DO TREN WINDOWS`) chỉ có **một** cặp `n/m` là cặp CA; đo 17:47Z —
dòng Windows hợp lệ ⇒ `True`, cùng dòng ấy với `CA 0/39` ⇒ `False`.

### Ca đang khoá chiều "vẫn còn lỗ"

`p456-linux-nhan-0-tren-0-Y-HET-base` trong `.claude/dev/ci_dang_ky_test.py:473`
(`_dem_nen(_RONG456, False) == 0`) **cố ý** khẳng định rằng Linux VẪN nhận `0/0`. Packet này làm
mệnh đề ấy sai, nên ca ấy phải **đảo chiều**, không phải bị xoá — xem `nghiem_thu` A5.

Hai ca anh em của nó **KHÔNG** đổi màu dưới hướng A-b (đo 17:46Z): `p456-mau-linux-KHONG-DOI-so-voi-base`
và `p456-linux-A-B-tung-dau-vao-khop-base` vẫn xanh vì `MOI[_P456]` không bị sửa một ký tự nào.
Đó là bằng chứng thứ hai cho A-b: nó giữ được **hai** trong ba ca mà hướng B phá cả ba.

### Lease đang giữ write set — PHẢI THU HỒI TRƯỚC KHI CẤP

Đo 17:46Z 06-09-2026, `python ops/lease_publish.py ai-dang-giu .claude/dev/ci_dang_ky_test.py`:

```
NGƯỜI_GIỮ 1: mutant-khong-chay-tren-windows-exec-1-claude-20260906
```

Lease ấy cấp `14:30:07Z 06-09`, hết hạn `14:30:07Z 07-09` — **còn ~20,7 giờ hiệu lực** trong khi
packet #456 **ĐÃ LAND** (PR #457 merge vào `1b3caa1`). Nó giữ cả `.claude/dev/ci_dang_ky_test.py`
lẫn `.claude/hooks/pretooluse_guard_test.py`. Đây đúng nợ `AG-T0-01B-thu-hoi-lease-chua-co-duong`
mà `CLAUDE.md` đã đo một lần trên packet `#355`.

Phép quét hai nguồn chạy trước đó (17:46Z): `git ls-remote --heads origin` = **295** ·
`git for-each-ref refs/remotes/origin` = **295** · `comm -23` **rỗng** ⇒ không mù ref, kết luận
lease trên là ĐO chứ không phải LỜI KHAI.

**Điều kiện tiên quyết của packet này:** lease mới phải khai `thay_the_cho:
mutant-khong-chay-tren-windows-exec-1-claude-20260906`, và tệp lease CŨ phải được đặt
`da_bi_thay_the` — chốt `_kiem_bia_mo` đòi **hai chiều**. Không làm là tự mở cửa sổ hai writer.

## `review_class` và ngưỡng kích thước

`sensitive` ⇒ `ADR-0044`: **≤ 3 tệp và ≤ 300 dòng thêm**. Write set là **1 tệp**. Không cần khai
vượt trần.

## `write_set`

| # | đường dẫn | vì sao |
|---|---|---|
| 1 | `.claude/dev/ci_dang_ky_test.py` | nơi `bang_chung_xanh` sống, và nơi phản chứng của chính nó sống |

Không ký tự đại diện. Không đường dẫn nào khác.

Đo 17:48Z 06-09-2026: `rg -n 'bang_chung_xanh' --glob '!*.md'` ngoài tệp này ⇒ **0 kết quả**. Hàm
không có caller nào khác trong kho, nên write set một tệp là ĐỦ chứ không phải là cắt gọt.

## `ngoai_pham_vi`

1. **Không sửa một ký tự nào trong `MOI` hay `MOI_WINDOWS`.** Hướng A-b không cần, và giữ nguyên
   chúng là thứ giữ được hai ca `p456-mau-linux-KHONG-DOI-so-voi-base` và
   `p456-linux-A-B-tung-dau-vao-khop-base` — hai chốt do cross-review lượt 1 của #456 sinh ra.
2. **Không đụng `.claude/hooks/pretooluse_guard_test.py` hay
   `.claude/hooks/subagent_ghi_detect_test.py`.** Bản in của chúng đã đúng (`34/34`, `22/22`);
   thứ hỏng là bên ĐỌC, không phải bên IN.
3. **Không cắt vòng lặp đột biến của bộ nào khỏi Windows** — đó là hai packet riêng
   (`MUTANT-WINDOWS-SUBAGENT-GHI-DETECT`, `MUTANT-WINDOWS-NHANH-DON-DUOC`). Gộp vào đây là 3 tệp
   và một write set giao nhau ba chiều; `ADR-0044` đo được giá của việc ấy (`PLAT-X4` 4 tệp ⇒
   3 vòng, 8 finding).
4. **Không đụng `.github/workflows/ci.yml`.** Packet này không đổi thời gian chạy của bất cứ thứ
   gì; nó chỉ làm một cổng đang mù nhìn thấy.

## `muc_tieu`

| # | mục tiêu | chiếu vào |
|---|---|---|
| M1 | `bang_chung_xanh` kiểm **mọi** cặp `n/m` nằm trong span khớp, không chỉ hai nhóm bắt. `DOT BIEN 0/0 bi giet` bị từ chối trên **mọi** nền. | `write_set` #1 |
| M2 | Mệnh đề thoát `len(m.groups()) != 2` bị **gỡ**: không tồn tại số nhóm nào làm hàm trả `True` vô điều kiện. | `write_set` #1 |
| M3 | Mẫu 0 nhóm (`probe_mang_test.py`) vẫn ĐẠT, và các cặp số ghi cứng trong nó nay **được kiểm** chứ không được tha. | `write_set` #1 |
| M4 | Đường Windows của #456 không đổi hành vi: dòng `KHONG DO TREN WINDOWS` vẫn ĐẠT trên Windows, vẫn ĐỎ trên Linux. | `write_set` #1 |
| M5 | Ca `p456-linux-nhan-0-tren-0-Y-HET-base` được **đảo chiều và đổi tên** cho khớp sự thật mới; hai ca anh em giữ nguyên. | `write_set` #1 |

## `nghiem_thu`

**A1 (M1) — lỗ #319 phía Linux đóng, đo bằng SỐ ĐỎ của `chay_moi`, không bằng mắt.**
Phép làm ĐỎ: gọi `chay_moi(moi={P: MOI[P]}, chay_mot=lambda _: (0, RONG), doc_nen_windows=lambda: False)`
với `RONG = "TONG: CA 39/39 dat · DOT BIEN 0/0 bi giet\nTONG: DAT\n"`. Trị phải là **1**
(hôm nay là **0**). Đi qua chính `chay_moi` chứ không gọi thẳng `bang_chung_xanh` — khuyết tật
"làm tròn" nằm ở NƠI TIÊU THỤ, bài học r6/#401 đã trả giá ba lần trong đúng tệp này.
Đơn vị: **số mục bị đếm là ĐỎ**, không phải chuỗi in ra.

**A2 (M2) — mệnh đề thoát theo số nhóm không còn.**
Phép làm ĐỎ: một mẫu **4 nhóm** trên `TONG: CA 0/39 dat · DOT BIEN 0/0 bi giet` phải cho
`False`. Hôm nay cho `True` (đo 17:45Z). Thêm ca cho **1 nhóm** và **3 nhóm** — số nhóm LẺ là
biên mà cả hai hướng vá đều dễ bỏ quên.
Đơn vị: **giá trị trả về của `bang_chung_xanh`** trên mẫu có số nhóm ∈ {0, 1, 2, 3, 4}, năm ca.

**A3 (M3) — mẫu 0 nhóm không còn được tha vô điều kiện.**
Phép làm ĐỎ: mẫu 0 nhóm khớp một bản in chứa `0/0` phải cho `False`. Hôm nay cho `True`.
Và chiều ngược lại: bản in thật của `probe_mang_test.py` (`9/9`, `1/1`, `11/11`) phải vẫn `True` —
hai chiều, không phải một.

**A4 (M4) — đường Windows của #456 nguyên vẹn.**
Phép làm ĐỎ: bốn phản chứng `p456-*` hiện có phải vẫn xanh, cụ thể `_dem_nen(_WIN456, False) == 1`
và `_dem_nen(_WIN456, True) == 0` và `_dem_nen(_LNX456, True) == 0`. Đột biến bắt buộc: xoá điều
kiện nền trong `mau_theo_nen` ⇒ `p456-dong-windows-tren-linux-la-DO` phải ĐỎ.

**A5 (M5) — ca cũ đảo chiều, KHÔNG bị xoá, và ĐỔI TÊN.**
Ca `p456-linux-nhan-0-tren-0-Y-HET-base` khẳng định `_dem_nen(_RONG456, False) == 0`. Sau packet
này mệnh đề đúng là `== 1`. Đổi khẳng định **và** đổi tên (đề nghị:
`lo319-linux-KHONG-CON-nhan-0-tren-0`), vì một cái tên nói *"y hệt base"* đứng cạnh một khẳng
định nói ngược lại là đúng lớp lỗi *"hai lời khai mâu thuẫn trong cùng một tệp"* mà cross-review
PR #250 lượt 3 đã bắt.
Phép làm ĐỎ: giữ nguyên tên cũ ⇒ finding quy trình; giữ nguyên khẳng định cũ ⇒ `phan_chung()`
cho `50/51` (đo 17:46Z, chính xác một ca).
Đơn vị: **số phản chứng đỏ đúng / tổng** — phải là `N/N` với `N ≥ 51`. Con số `51` là nền đo
17:46Z 06-09-2026 trong CÂY THẬT; **đo lại tại lúc thi công**, đừng chép.

**A6 — sổ đăng ký chạy thật vẫn xanh trên ubuntu.**
`python .claude/dev/ci_dang_ky_test.py --chay` trên `ubuntu-latest` phải `success`. Đây là phép
đo duy nhất bắt được "A-b sinh đỏ giả vì một cặp `n/m` vô can lọt vào span".
Phép làm ĐỎ: một bộ trong sổ in thêm một cặp `n/m` không phải bằng chứng (ví dụ một tỉ lệ
`3/5 hướng`) ⇒ bước này ĐỎ. **Đó là hành vi ĐÚNG** của packet này, và nó là cái giá đã biết của
hướng A-b — xem `chua_do_duoc` #1.

**A7 — không đụng hành vi nào khác.** `git diff --numstat` chỉ hiện đúng **1** đường dẫn.

**A8 — lease cũ đã thu hồi TRƯỚC khi bắt tay.**
`python ops/lease_publish.py ai-dang-giu .claude/dev/ci_dang_ky_test.py` phải in `NGƯỜI_GIỮ 1`
và tên lease ấy phải là lease của **packet này**, không phải
`mutant-khong-chay-tren-windows-exec-1-claude-20260906`.
Phép làm ĐỎ: chạy lệnh trước khi thu hồi ⇒ ra tên lease #456 ⇒ DỪNG, không được bắt tay.

## `hinh_dang_ke_thua`

Bộ đếm **hình dạng lỗi**, chép từ `ops/specs/MUTANT-KHONG-CHAY-TREN-WINDOWS.md` và từ hồ sơ
`CI-CAI-JSONSCHEMA` (r1→r2→r3), cộng thêm những gì packet này đo được:

| hình dạng | số lần đã gặp | ghi chú |
|---|---:|---|
| tập RỖNG thoả `not song` (`0/0` được nhận là bằng chứng) | **3** | #319 (gốc) · #456 đường Windows (đã bịt) · đường Linux (packet này). Lần thứ ba ⇒ `PROTOCOL §12` đòi xem lại CÁCH LÀM: câu trả lời là **bịt ở vị từ dùng chung**, không bịt ở từng mẫu. |
| nâng `timeout-minutes` để mua cổng xanh | **3** (`25`→`45`→`60`) | Packet này không đụng `ci.yml`. |
| khai một phép đo là `KHÔNG ĐO ĐƯỢC` rồi để nguyên | **1** (`CI-CAI-JSONSCHEMA-r3` A5) | Đã đo được ở #456. |
| cổng vắng mặt trông giống cổng xanh | nhiều | Ở đây: cổng CÓ MẶT, CÓ CHẠY, và vẫn không đo — biến thể đắt hơn. |
| lease không tự chết khi packet đã land | **2** (`#355`, `#456`) | Đo 17:46Z 06-09: lease #456 còn 20,7 giờ hiệu lực sau khi packet đã merge. Xem A8. |

## `chua_do_duoc`

1. **Rủi ro đỏ giả của hướng A-b chưa có cận trên.** Nó soi span khớp, mà hai mẫu dùng `(?s).*`
   có span **2745 b** (`chon_reviewer_test.py`) và **2179 b** (`mcp_gh_test.py`) — toàn văn bản
   tự do. Hôm nay 10/10 cặp trong bảy span đều là bằng chứng thật; **không có gì bảo đảm** một
   bản in tương lai không chứa một cặp `n/m` vô can. Đây là đánh đổi CÓ CHỦ Ý: hướng B không có
   rủi ro ấy nhưng để lại bẫy 4-nhóm ở A2. Ghi thành nợ có tên
   **`SPAN-RONG-CO-THE-NUOT-CAP-VO-CAN`**; cách thu hẹp khi cần là buộc mẫu neo cặp vào một
   nhãn (`DOT BIEN`, `CA`) thay vì soi cả span — chưa làm ở packet này vì chưa có ca thật nào
   đòi.
2. **Nền của `pretooluse_guard_test.py` KHÔNG xanh trong container soạn spec.** `rc=1`,
   **270 giây**, 3 ca đỏ sẵn (`t11_lo_336_co_that_VA_bi_chan` ·
   `t15_cong_kiem_bang_khop_nguon_that` · `t33_cong_hoi_RUNTIME_chu_khong_parse_van_ban`), nên
   nó in `TONG: DIEM DOT BIEN BI TU CHOI` và mẫu `MOI` **không khớp**. CI ubuntu xanh
   (`test registry` 14,33 phút trên `1b3caa1`, run `34048685345`) ⇒ lệch **rig**, không phải hồi
   quy. Hệ quả: phiên thi công **không** dùng container này làm nền so sánh cho ca nền; phải
   dựng hai vế trong MỘT lệnh (bài học "phép đo delta phải dựng cả hai trong một lệnh").
3. **Chưa đo trên Windows.** Container này là Linux. Mọi khẳng định về hành vi Windows đi qua CI.
   Packet này không đổi gì theo nền nên rủi ro thấp, nhưng "thấp" không phải "đã đo".
4. **Không đo được cặp `n/m` của `pretooluse_guard_test.py` trên bản in thật ở đây** (lý do ở
   mục 2). Cặp `39/39` · `34/34` lấy từ thông điệp commit `0c5e889`, tức là **lời khai của lượt
   trước**, không phải phép đo của lượt này. Phiên thi công phải đo lại từ log CI.
