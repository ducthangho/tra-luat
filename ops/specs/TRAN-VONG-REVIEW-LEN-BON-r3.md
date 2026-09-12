# Đặc tả packet — TRAN-VONG-REVIEW-LEN-BON (revision 3)

- `packet_id`: **TRAN-VONG-REVIEW-LEN-BON**; ID bền `wp522`.
- `packet_issue`: **522**
- `mission_issue`: **499**
- `revision`: **3** · `generation`: 3 · soạn **12-09-2026**
- `thay_the_cho`: **revision 2** (`spec_sha256`
  `7d2c383279e6557937664e45718629fdc9625ee936acacbbab84ff69b209d6d0`, đã cấp packet + lease gen 1,
  đã chạy 2 lượt cross-review). r2 **giữ nguyên trên đĩa làm hồ sơ**; đây là hợp đồng thay thế, không
  phải bản sửa r2.
- `depends_on`: **`[]`**
- `executor`: claude · `environment`: cloud
- `risk`: **sensitive** · `review_class`: **sensitive**

## `nguon_cap_viec`

Kế thừa r2 (chỉ thị chủ kho 12-09-2026 *"trần nâng lên thành 10 vòng đi"*,
[#issuecomment-5644646795](https://github.com/ducthangho/tra-luat/issues/522#issuecomment-5644646795)),
cộng hai chỉ thị MỚI của chủ kho trong phiên 12-09-2026 — **nới write set lên 4 đường kèm ngoại lệ
`ADR-0044`** và **cấp thêm `ops/reviews/**`** — bản chiếu ở [#issuecomment-5645452551](https://github.com/ducthangho/tra-luat/issues/522#issuecomment-5645452551).

Khối `nang_tran` gen 2 (`same_failure_limit` 2→10, `attempts_limit` 3→10, `ai_nang: ducthangho`) ở
[#issuecomment-5644974229](https://github.com/ducthangho/tra-luat/issues/522#issuecomment-5644974229)
**giữ hiệu lực** và được chép vào lease gen 3.

## VÌ SAO PHẢI CÓ r3 — r2 không thi hành được, đo bằng số

`M1` của r2 đòi một tệp ADR mới. Tệp ấy là Markdown thứ **73** dưới `docs/`, và
`scripts/tl_selftest.py` **đấm cứng** con số 72:

```python
ok3 = int(j.get("file_count") or 0) == len(paths) and len(paths) + 72 == 252   # dòng 21276
ok4 = (len(tren_dia) == 72                                                     # dòng 21279
```

Phép đo DELTA, hai vế dựng trong **MỘT lệnh** với **cùng các bước** (hai clone rời, cùng
`core.abbrev 7`, chạy song song — đúng thuốc của doctrine chống *"rig tự đẻ hồi quy"*):

| vế | commit | `docs/**/*.md` | `tl.py --selftest` |
|---|---|---:|---|
| nền | `015ffcc` (`origin/master`) | **72** | **rc=0**, `1709/1709`, 0 ca FAIL |
| sau | `a3f5f21` (head PR #526) | **73** | **rc=1**, `1708/1709`, đúng 1 ca FAIL = `r291_docs_ngoai_goi` |

Trên CI, cùng một ca: `gate` run `34685943174` (`a3f5f21`) **failure** · run `34684537107`
(`7059cbb`) **failure**; `thu-hoi` **success** cả hai. Ca đỏ duy nhất: `[FAIL] r291_docs_ngoai_goi`.

⇒ **nền XANH, delta là của packet.** Không phải đỏ sẵn, không phải nhiễu rig.

Chữa `r291` đòi `scripts/tl_selftest.py` — **đường thứ ba**. Và tệp ấy **nằm trong**
`RELEASE_MANIFEST.json`, ghim theo NỘI DUNG (đo: manifest `sha256`
`b65bc7519e9781b88a01432a124092a6bb05d5fd07b1b3fd468ade6e3e9c1ce8`, `size` `2137906`, **khớp đĩa**)
⇒ sửa nó là phải tái sinh manifest — **đường thứ tư**.

`§3.2` và `§5` của protocol đều đòi: đổi write set ⇒ **revision mới, generation mới, cấp lại lease**.
Nên r2 không được "nới tại chỗ"; nó bị **thay**.

`§5` còn áp thẳng: *"`scripts/tl_selftest.py` là legacy harness dùng chung và mặc định không thuộc
packet thường… Packet cần sửa chính harness … vẫn phải chạy tuần tự"*. Đã quét lease **toàn kho**
(sau `fetch --unshallow` refspec rộng; so TẬP TÊN hai nguồn `comm -23` = **0** ⇒ không mù):
`scripts/tl_selftest.py` ⇒ `rc=0`, **NGƯỜI_GIỮ 0**; `RELEASE_MANIFEST.json` ⇒ `rc=0`,
**NGƯỜI_GIỮ 0**. Bộ quét đã được hỏi một **ca biết trước đáp án** (`docs/adr/0048-*.md` ⇒ `rc=11`,
**NGƯỜI_GIỮ 1** = lease gen 1) nên lời khai `0` ở trên có răng.

## `review_class` và ngưỡng — ngoại lệ `ADR-0044` CÓ KHAI

`sensitive` ⇒ `ADR-0044`: **≤ 3 tệp, ≤ 300 dòng thêm**. Packet này **4 tệp** (chưa kể hiện vật
review), nên đi kèm khối ngoại lệ:

```yaml
ngoai_le_adr_0044:
  ai_nang: ducthangho
  tran_cu: 3 tệp
  tran_moi: 4 tệp (KHÔNG đổi trần 300 dòng thêm)
  can_cu: >-
    Hai đường thêm là CHI PHÍ BẮT BUỘC của M1, không phải mở rộng phạm vi: tệp ADR mới
    làm ratchet r291 đỏ, và tệp chữa ratchet lại bị manifest ghim theo nội dung. Không có
    tổ hợp 3 tệp nào vừa thoả M1 vừa để gate xanh — đã đo, không phải suy.
  khong_nang: >-
    Trần 300 dòng thêm GIỮ NGUYÊN. Trần ATTEMPT và trục LỜI GỌI GIỮ NGUYÊN.
    Ngoại lệ này KHÔNG áp cho packet nào khác và hết hiệu lực khi #522 terminal.
```

`ops/reviews/**` là **hiện vật review bất biến**, không phải mã sản phẩm; `ci.yml` đã khai chúng
*"không phải mã sống để CI chạy"*. Nó **không** tính vào bốn tệp trên, và nói thẳng ra đây để phép
đếm của `A6` không mơ hồ.

## `write_set`

| # | đường dẫn | kiểu | vì sao |
|---|---|---|---|
| 1 | `docs/adr/0048-tran-vong-review-len-muoi.md` | exact | ADR mới, thay số của `ADR-0043` |
| 2 | `docs/PROTOCOL_DA_PHIEN.md` | exact | dòng §20 cho ADR mới + dòng `ADR-0043` đổi trạng thái |
| 3 | `scripts/tl_selftest.py` | exact | kê khai slot `r291` 72→73 — **chỉ** khối `r291`, không chạm ca khác |
| 4 | `RELEASE_MANIFEST.json` | exact | tái sinh vì (3) bị ghim theo nội dung |
| 5 | `ops/reviews/` | prefix | `VERDICT.md` + `*.receipt.yaml` của các lượt cross-review |

Không ký tự đại diện ngoài prefix (5). **KHÔNG** đụng `docs/adr/0043-*.md`, bốn đặc tả đã đóng băng
chép con số cũ, `ops/specs/TRAN-VONG-REVIEW-LEN-BON.md` (r1) hay `-r2.md`.

## `ngoai_pham_vi`

1. **KHÔNG sửa bốn đặc tả đã đóng băng** (`BO-CONG-DUYET-KHAC-DANH-TINH`, `CI-CAI-JSONSCHEMA-r2`,
   `CI-CAI-JSONSCHEMA-r3`, `TAT-DINH-VOID-HA-TANG-r2`).
2. **KHÔNG viết cổng `so-canon`** — nợ `SO-CANON-CHUA-TON-TAI`, packet riêng.
3. **KHÔNG đổi `codex_review_calls_used`** (trục LỜI GỌI) hay trần ATTEMPT.
4. **KHÔNG đổi định nghĩa vòng review canon** (`PROTOCOL:814`).
5. **KHÔNG sửa cơ chế của `r291`** — chỉ kê khai slot theo đúng nếp tệp ấy đã dùng nhiều lần. Đổi
   `r291` sang TÍNH số thay vì đấm cứng là việc đáng làm nhưng là **packet khác** (nợ #4 dưới).
6. **KHÔNG chạm ca nào khác trong `scripts/tl_selftest.py`.**

## `muc_tieu`

| # | mục tiêu | chiếu vào |
|---|---|---|
| M1 | ADR mới khai trần canon trục VÒNG là **MƯỜI**, trỏ `ADR-0043` là tiền nhiệm, giữ nguyên hai trục kia. | 1 |
| M2 | ADR mới khai **luật hiệu lực theo thời điểm đóng băng**: packet có `spec_hash` đóng băng TRƯỚC ngày ADR được chấp nhận giữ trần cũ; muốn trần mới thì tạo revision. | 1 |
| M3 | `§20` có **đúng một dòng** cho ADR mới; dòng `ADR-0043` đổi sang trạng thái *đã bị thay số*, **không xoá**. | 2 |
| M4 | Khối `nang_tran` vẫn bắt buộc khi vượt trần MỚI. | 1 |
| M5 | ADR mới ghi **số biện hộ** và ghi thẳng rằng phần đo được chỉ biện hộ *"cao hơn 4"*. | 1 |
| **M6** | `r291_docs_ngoai_goi` **ĐẠT** với 73 Markdown dưới `docs/`, bằng một khối `KÊ KHAI SLOT` theo đúng nếp tệp ấy — nêu đúng tệp được thêm và số cũ → số mới. | 3 |
| **M7** | `RELEASE_MANIFEST.json` khớp cây; `release-verify --strict` `ok=true` với `expected == checked`. | 4 |
| **M8** | Hiện vật cross-review (verdict có băm + biên nhận) **sống trong git**, không chỉ trong container. | 5 |

## `nghiem_thu`

**A1 (M1,M3) — `adr-song` xanh.** `packet_loop.py adr-song --root .` ⇒ `rc=0`, số ADR trên đĩa
**BẰNG** số dòng §20 (**48/48**; trước packet 47/47).
**Phép làm ĐỎ:** thêm ADR mà quên dòng §20 ⇒ ĐỎ.

**A2 (M1) — con số chỉ có MỘT chỗ ở.** Đây là tiêu chí quan trọng nhất về NỘI DUNG, và nó được phát
biểu lại cho **chật hơn r2** vì r2 đã trả giá năm lần:

> Kiểm bằng **LIỆT KÊ rồi NGƯỜI phân loại**, không bằng một phép đo tự động khai là phát hiện được
> bản sao. Liệt kê mọi chỗ trong `docs/` nhắc **khái niệm** trần vòng review (không đòi dòng ấy mang
> giá trị), rồi phân loại từng chỗ là **TRỎ** hay **CHÉP GIÁ TRỊ**. Đạt khi: chỉ
> `docs/adr/0048-*.md` mang giá trị MỚI; `PROTOCOL:807` và `ADR-0037` vẫn **TRỎ**; các chỗ mang giá
> trị CŨ đều thuộc hồ sơ đã đóng băng hoặc là trích tiêu đề `ADR-0043`.

**KHAI THẲNG GIỚI HẠN, vì r2 đã tốn 5 bản đo cho đúng chỗ này:** không có phép đo theo **mẫu văn
bản** nào quyết được *"đây có phải bản sao con số trần không"* — đã đo và đã bị reviewer giết bốn
lần (v1 regex từ vựng · v2 khái niệm OR giá trị · v3 ba vế/một dòng theo TỆP · v4 che định danh theo
DÒNG; mỗi lần lại có cách viết thứ N+1). Việc ấy thuộc cổng `so-canon`, và `ngoai_pham_vi` mục 2
**CẤM** packet này viết nó. Nên `A2` **cố ý** là một phép kiểm CÓ NGƯỜI, và bất kỳ script hỗ trợ nào
là **NHÁP**: không vào write set, không commit, không được khai là cổng.
**Phép làm ĐỎ:** chép số `10` vào `PROTOCOL:807` hoặc `ADR-0037` ⇒ người phân loại thấy ngay ở danh
sách liệt kê.

**A3 (M2) — luật hiệu lực PHÂN BIỆT ĐƯỢC hai trạng thái.** ADR phải nêu **MỐC** (ngày chấp nhận) và
**THỨ NEO** (`spec_hash` đóng băng trước hay sau mốc), và cho câu trả lời **không mơ hồ** cho từng
đặc tả trong bốn cái đã đóng băng.
**Phép làm ĐỎ:** bỏ mốc, hoặc viết *"áp dụng cho mọi packet"* ⇒ ĐỎ.

**A4 (M4) — vượt trần vẫn đòi `nang_tran`** khai `ai_nang`, `can_cu`, `tran_cu`, `tran_moi`.
**Phép làm ĐỎ:** bỏ câu ấy ⇒ trần 10 thành trần mềm ⇒ ĐỎ.

**A5 (M5) — số biện hộ có mặt VÀ có giới hạn.**
**Phép làm ĐỎ:** viết *"đo được rằng 10 là con số đúng"* ⇒ lời khai rộng hơn phép đo ⇒ ĐỎ.

**A6 (toàn packet) — ngưỡng kích thước.** `git diff --numstat origin/master..HEAD` ⇒ **đúng 4** đường
dẫn ngoài `ops/reviews/**`, `additions` ≤ **300**. Bốn đường phải khớp **từng tên** với `write_set`
1–4; đường thứ năm nào ngoài đó ⇒ ĐỎ. (Ngoại lệ `ADR-0044` đã khai ở mục ngưỡng.)

**A7 — `doctrine-scan` xanh.** `packet_loop.py doctrine-scan --root .` ⇒ `rc=0`.

**A8 (M6,M7) — HAI cổng mà r2 KHÔNG có, và chính chỗ thiếu ấy làm r2 sập.**
- `python3 scripts/tl.py --selftest` ⇒ **rc=0** và dòng tổng kết hai số **BẰNG NHAU** (`N/N`).
  Đòi hai số bằng nhau, **không** đọc `rc` một mình — `rc` là thứ đã bị tin sai nhiều lần trong kho.
- `python3 scripts/tl.py release-verify RELEASE_MANIFEST.json --strict --json` ⇒ `ok=true`,
  `expected_file_count == checked_file_count`, `failed` rỗng.

**VÌ SAO A8 tồn tại — lịch sử đo được, không phải lo xa:** khối chú thích của chính `r291` ghi **bốn**
lần trả giá cùng một hình dạng (phiên chạy `adr-song` + `doctrine-scan` + `doc-claims-check --strict`,
cả ba xanh, rồi đẩy; CI mới là nơi ca này đỏ). Bàn giao của phiên r2 liệt kê **đúng bốn cổng ấy** và
không chạy `tl selftest` ⇒ **lần thứ năm**. Và lane PR **không** bắt được lệch manifest:
`release-verify strict (lane LAND)` có `if: github.ref == 'refs/heads/master'`, còn lane WORKER sinh
manifest tạm từ chính cây nên **hấp thụ** thay đổi nội dung ⇒ bỏ `release-verify` tại chỗ là **PR
xanh, master ĐỎ**.
**Phép làm ĐỎ:** thêm một tệp `.md` dưới `docs/` mà không kê khai slot ⇒ `--selftest` ĐỎ; sửa một byte
trong `scripts/tl_selftest.py` mà không tái sinh manifest ⇒ `release-verify --strict` ĐỎ. **Cả hai đã
tái hiện được**, không phải giả định.

**A9 (M6) — kê khai slot ĐÚNG NẾP, không chỉ đúng số.** Khối `KÊ KHAI SLOT` mới phải nêu: tệp được
thêm (`docs/adr/0048-*.md`), số cũ → số mới (**72 → 73**, và `252 → 253`), rằng gói **KHÔNG** đổi
(`file_count` giữ **180**) nên trần Package 200 không nhúc nhích, và rằng đây là lần thứ **NĂM** cùng
một cách sập — để lần sau đọc được lý do mà khỏi lặp.
**Phép làm ĐỎ:** đổi hai con số mà không ghi khối kê khai ⇒ ĐỎ ở review (không có cổng máy nào canh
nếp này; nói thẳng thay vì khai có cổng).

**A10 (M8) — hiện vật review sống trong git.** `packet_loop.py bien-nhan --packet 522` ⇒ **≥ 1** biên
nhận reviewer phân biệt được, và `VERDICT.md` của mỗi lượt có mặt dưới `ops/reviews/` với `sha256`
khớp bản chiếu đã đăng trên PR.
**Nói thẳng phần KHÔNG cứu được:** hai `VERDICT.md` của lượt 1 và 2 **đã chết theo container** của
phiên r2; chỉ còn `sha256` trong bản chiếu (`db9be984…`, `6032ff98…`). Hai băm ấy **KHÔNG ĐO ĐƯỢC**
từ nay và **không** được khai là đã kiểm. `A10` chỉ áp cho các lượt từ **lượt 3** trở đi.

**Điều kiện dừng:** `sensitive` ⇒ đòi cross-review **`approve` tường minh**.

## `chua_do_duoc`

1. **`so-canon` vẫn KHÔNG tồn tại.** `grep -rln "review_rounds_used" --include=*.py .` ⇒ **0 tệp**
   (đo lại 12-09-2026). Trần `10` **không có cổng nào canh**, y như trần `2`. Packet này **không**
   chữa và **không** được khai là đã chữa. Nợ: **`SO-CANON-CHUA-TON-TAI`**.
2. **Số vòng ở bảng biện hộ đếm bằng TAY** từ hiện vật phiên, không từ bộ đếm trong kho (nợ #1).
3. **Không đo được trần 10 có đủ hay không** — nó chưa từng bị chạm. Câu duy nhất đo được là trần 4
   ĐÃ bị chạm.
4. **`r291` vẫn đấm con số cứng.** Kê khai slot là chữa TRIỆU CHỨNG. Mỗi tệp `docs/*.md` thêm vào kho
   sau này lại làm nó đỏ và lại đòi một lần kê khai — đó chính là hình dạng đã lặp **năm** lần. Nợ có
   tên: **`R291-DAM-SO-CUNG`**; cách chữa là cho ca ấy TÍNH số từ cây và chỉ ratchet phần thực sự là
   bất biến (gói), nhưng việc đó ngoài phạm vi packet này.
5. **Sổ `packet_loop` của generation 1 KHÔNG tra được.** `.claude/.packet_state/` nằm trong
   `.gitignore` (dòng 32) nên nó chết theo container của phiên r2. Mỏ neo bền còn lại là ba comment
   trên Issue #522 / PR #526. Đừng đọc chỗ rỗng ấy thành *"gen 1 chưa từng blocked"*.
