# Bàn giao `wp530` sang Executor `codex` — generation 2

Viết `2026-09-13T02:4xZ` bởi phiên `claude` đã thi công gen 1 (vòng 1→3). **Tệp này là hồ sơ, không
phải thẩm quyền**: thẩm quyền nằm ở lease `cham-dot-bien-mien-nhiem-lease-suite-exec-2-codex-20260913`
(nhánh `ops/cap-lease-530`) và chỉ thị `issues/530#issuecomment-5650262276`.

## Neo — kiểm được không cần tin ai

| thứ | giá trị |
|---|---|
| PR | **#532** (draft), nhánh `claude/cham-dot-bien-mien-nhiem-lease-suite` |
| head bàn giao | **`a1f18bd8bb008900a7c85c5a582ee331e8161ae8`** |
| write set | **MỘT** đường: `ops/lease_publish_test.py` |
| mỏ neo | `base_sha` = `start_from_sha` = `reviewed_sha_required` = `dc02c9beed42bd2ea44a80a2e34e1bbe3acfc6c5` |
| đặc tả ĐÓNG BĂNG | `ops/specs/CHAM-DOT-BIEN-MIEN-NHIEM-LEASE-SUITE.md` rev 3, sha256 `47c3b1fe70da6976cf802436fa8883c2ba48ac8f706b3d9ec103deaeb5f37778` — nhánh `ops/handoff-512-luot7`, **CHƯA trên master**; băm là thứ định danh, tên nhánh là thứ trôi |
| lease | `…exec-2-codex-20260913`, hết `2026-09-14T02:33:00Z`; `ai-dang-giu ops/lease_publish_test.py` ⇒ `NGƯỜI_GIỮ 1` = chính nó |

**Tự xác minh, đừng nhận bảng này:**

```
git fetch origin ops/cap-lease-530 claude/cham-dot-bien-mien-nhiem-lease-suite ops/handoff-530
git show origin/ops/cap-lease-530:ops/leases/cham-dot-bien-mien-nhiem-lease-suite-exec-2-codex-20260913.yaml
python3 ops/lease_publish.py ai-dang-giu ops/lease_publish_test.py     # rc=11 + NGƯỜI_GIỮ 1
```

## Trạng thái đo được lúc bàn giao

| trục | giá trị | trần |
|---|---|---|
| `S2` dòng thêm | **`+1292 / −61`** | **1500** ⇒ dư **208** |
| `S6` vòng review | **3/10** — nhưng vòng 3 **mới chỉ VÁ**, CHƯA có cross-review cho head này | 10 |
| `S5` | `git log dc02c9b..origin/master -- ops/lease_publish_test.py` **RỖNG** | — |

Cổng tại chỗ trên `a1f18bd`, bằng chứng DƯƠNG (hai số BẰNG NHAU, không đọc `rc` một mình):

```
t161 16/16, không giết 0, KHÔNG ĐO ĐƯỢC 0      t164 19/19
t162 12/12                                     t165 2/2
t163 11/11                                     t166 2/2
wrapper: BA dòng `lease_publish: 161/161 đạt; đã chạy=161, bỏ qua=0` (CHA + [A] + [B])
         0 dòng `  ĐỎ  `   ·   WRAPPER_RC=0
doctrine-scan rc=0 (7 tệp, 0 chỗ chép)   ·   adr-song rc=0 (48/48)
```

**ĐIỀU KIỆN ĐO — một con số không ghi điều kiện thì sẽ trôi mà không ai biết:** `AL_VER=1.7.7` (wrapper
tự cài `actionlint`; thiếu biến này wrapper thoát **2** trước khi chạy gì) và `shellcheck 0.9.0` CÓ MẶT.
Thiếu `shellcheck` thì `t137`/`t159` fail-close `KHÔNG ĐO ĐƯỢC` — đó là **nền đo**, không phải hồi quy.

```
AL_VER=1.7.7 bash ops/chay_lease_publish_test.sh
```

## Ba vòng đã đi, và HÌNH DẠNG của chúng quan trọng hơn nội dung

| vòng | head | kết quả |
|---|---|---|
| 1 | `a1c7d7f` | `0 P1 · 4 P2 · 2 P3` — vá cả sáu lớp ở `d5e7e7d` |
| 2 | `3f1cda1` | `0 P1 · 4 P2 · 1 P3 · 6 NỢ` — **ba** `P2` LẶP LẠI lớp vòng 1, **một** lớp là lỗ MỚI do chính bản vá vòng 1 mở ra |
| 3 | `a1f18bd` | đã vá cả bốn `P2` + `P3`; **chưa cross-review** |

**Bài học phải mang sang, vì nó đã tái phát hai lần liền:** mỗi bản vá của gen 1 đều **ĐÚNG** ở chỗ nó
phủ, nhưng **HẸP** — vá đúng chỗ reviewer chỉ rồi bỏ sót đường tiếp theo không ai chỉ. Vòng 3 vì thế
đổi cách: liệt kê **HẾT đường vào** của mỗi lớp TRƯỚC, đóng cả loạt, và cho **mỗi đường một chốt
riêng** có đột biến riêng. Nếu ba chốt không phân biệt được bằng đầu vào thì chúng là bộ **TƯƠNG
ĐƯƠNG** và ta chỉ đang đo một cái.

## Vòng 3 đã vá gì, và phản chứng nào chứng minh nó có răng

Bốn lớp, mỗi lớp một phép đo chạy được (`ops/handoff/530/review-vong2/` giữ verdict + 11 hiện vật):

1. **`m5-van-cham-chet-bang-chuoi`** — thêm **cột thứ SÁU** (`nhãn THÔ`) vào `DOT_BIEN_TU_KIEM_512`,
   đọc bằng `_nhan_tho_512`, **không** qua `doc_kenh`, **không** fail-close.
   · *Phản chứng (đúng phép tiêm reviewer đã dùng):* tiêm `Exception` thay `TinHieuChotCa` tại chốt
   cuối `t162` ⇒ **TRƯỚC `7/7 rc=0`, NAY `6/11 rc=1`**.
   · *Đối biến:* cùng phép tiêm, **gỡ** cột nhãn thô ⇒ `9/11`. Tức cột ấy bắt **THÊM 3** mục mà không
   chốt nào khác bắt được. **Phép đo là CON SỐ, không phải `rc`** — hai mục kỳ vọng `kenh=GIET` đã
   được chốt có sẵn bắt, nên đòi "gỡ cột ⇒ `rc=0`" là đòi sai đại lượng.
2. **`m3-bo-sot-loi-chuan-bi`** — `_cay_mut_512` và `sinh_dau_phien` vào phạm vi bắt `OSError` của
   **từng attempt**; bắt HẸP, không bắt rộng. Ca `t165` tiêm lỗi xác định ở **hai seam RIÊNG**.
3. **`control-bo-sot-chot-va-trang-thai`** — **sáu** fixture mới trong `t164`, mỗi fixture vi phạm
   **ĐÚNG MỘT** điều kiện. Phân loại sửa theo kết quả gỡ từng chốt: phân biệt `3 → 9`, hấp thụ `4 → 2`.
   · *Phản chứng:* gỡ riêng **sáu** chốt ⇒ `t164` ĐỎ cả sáu lần, mỗi lần gọi đúng tên fixture.
4. **`vat-hoa-tuong-duong-qua-rong`** — sửa chú thích còn khai sai, và trả hết
   `NO_CHUA_CO_TU_KIEM_512` (`2 → 0`) bằng ca `t166` + hai mục cuối bảng.

Script phản chứng: `ops/handoff/530/review-vong3/phan_chung_vong3.py` — `TONG: 8/8 phép đo ĐẠT`.

**Một phát hiện của CHÍNH oracle mới, ghi lại vì nó là lý do oracle ấy tồn tại:** lượt đầu `t163` cho
`10/11` — mutant làm `_ten_day_du_512` trả generator khiến `t166` chết vì `TypeError` **VÔ CAN**
(`nhan=DO_KHAC`) trước khi chốt của nó kịp chạy. Đúng lớp *"đột biến bị giết KHÔNG phải vì lý do đang
thử"*. Chữa bằng vật hoá ở phần **dựng fixture** của `t166`.

## Việc còn lại

1. **Cross-review vòng `3/10`** trên head `a1f18bd` — reviewer nền **`claude`** (`fable-5.1`, `xhigh`),
   và phải là phiên **KHÁC** phiên đã soạn bản vá (xem `recorder_xung_dot_loi_ich` trong lease).
2. Lặp **vá → cross-review theo LỚP lỗi (không theo lỗi riêng lẻ) → đăng verdict** tới khi **`approve`
   tường minh** hoặc hết `P1`/`P2`.
3. Verdict + hiện vật đi nhánh `ops/handoff-530` (**không** tính vào `S1`/`S2`).

## Điều kiện DỪNG — hỏi chủ kho, đừng tự nới

`S1` cần đường dẫn thứ hai · `S2` **> 1500** dòng thêm · `S3` phải sửa `ops/lease_publish.py` ·
`S4` muốn skip/cách ly/vô hiệu một ca **hoặc nâng `timeout-minutes`** · `S5` `origin/master` chạm write
set sau `dc02c9b` · `S6` hết **10** vòng · `S7` thiếu `approve` tường minh (*"0 P1 + 0 P2"* **KHÔNG
đủ**) · `S8` phải chạm `.github/workflows/ci.yml` hoặc `.claude/dev/ci_dang_ky_test.py` (`#463` giữ,
exclusive).

Thêm: **KHÔNG** sửa đặc tả rev 3 · **KHÔNG** sửa `ops/reviews/**` cũ · **KHÔNG** đổi ngữ nghĩa các ca
hiện có · **KHÔNG** chữa bằng một regex khác (`ngoai_pham_vi` #5, #6) · **KHÔNG** tự cấp lease.

## KHÔNG chạy CI — chỉ thị chủ kho

Không `workflow_dispatch`, không gắn nhãn `windows`, không chạy lại job đỏ. **Windows và full CI đứng ở
`KHÔNG ĐO ĐƯỢC`**, và theo chỉ thị đó là **lỗi ĐÃ BIẾT**, không gác packet này.

Ngoại lệ đã dùng và sẽ còn phải dùng: cổng **`thu-hoi`** đỏ `rc=12` với lý do
`workflow_sha <master hiện tại> != S <mốc canonical>` là **TRÔI NỀN**, không phải lỗi nội dung — chữa
bằng **merge `origin/master` vào nhánh PR** rồi chạy lại cổng tại chỗ. Đã gặp ở head `9bd16e1` và đóng
bằng merge `a1f18bd`. Một phiên khác gặp **năm lần** cùng lớp trong một phiên trên PR #525.

## Nợ phải khai, không im lặng

- **Chống giả mạo tín hiệu bởi mã CÙNG interpreter**: kênh bảo vệ khỏi một tập lỗi khai tường minh,
  **không** khỏi mã sửa thẳng trạng thái khung. Kế thừa NGUYÊN VẸN giới hạn của `#513` — `_nhan_tho_512`
  đóng ca *im lặng nhận tín dụng vì ngoại lệ vô can*, **không** đóng ca *cố tình giả mạo*.
- **Hai chốt còn trong `CHOT_BI_HAP_THU_512`** là **CHƯA DỰNG ĐƯỢC** đầu vào phân biệt, **không phải
  KHÔNG TỒN TẠI**. Đây đúng chỗ gen 1 đã trượt một lần: suy từ phép đo trên **tập fixture hiện có** ra
  mệnh đề về **toàn giao diện**. Ai dựng được đầu vào thì chuyển chúng lên bảng kia.
- **Ma trận 19 nhánh ⇒ 6 làm `t164` đỏ** là **độ phủ trên 19 phép gỡ ĐÃ LƯU**, KHÔNG phải lời khai
  rằng 13 nhánh còn lại độc lập hay có lỗi.
- **`SO-CANON-CHUA-TON-TAI`**: `grep nang_tran|tran_moi|tran_cu|ai_nang|review_round` trên
  `ops/lease_publish.py` ⇒ **0** dòng; trên `.claude/dev/packet_loop.py` ⇒ **0** dòng. Không cổng nào
  đọc `nang_tran`, không cổng nào canh trần vòng ⇒ **đếm vòng là đếm TAY**.
- **`kiem-github` KHÔNG ĐO ĐƯỢC** trong container remote (cần `gh`; `gh` vắng, và cài cũng vô ích vì
  nó đi đúng đường proxy chặn).
- **`actions_list` bỏ qua cả `branch` lẫn `event`** trong container này (đã đo hai lần) — phải lấy
  danh sách rộng rồi tự lọc.
- **`get_status` là API commit-status KIỂU CŨ**, luôn trả `total_count: 0, state: pending` ở kho này.
  Hỏi `get_check_run` / `pull_request_read get_check_runs`, đừng hỏi `get_status`.
- **Heartbeat 30 phút** của lease chưa có cơ chế nào.
- **`AG-T0-01B`**: sau khi merge, lease `#530` phải NGHỈ bằng **bia mộ hai chiều**. **KHÔNG** dùng sổ
  `ops/thu-hoi/` — `SO_THU_HOI_KICH_HOAT = False`, cờ tắt mà sổ có bản ghi ⇒ cổng `rc=12`.
- **Mỏ neo blob của mẫu `493`** trong đặc tả rev 3 sai OID (`rev-parse 36f68c7:…` ⇒ `5acd5632…`);
  **tổng `493` đúng**. Việc của một revision, không phải của lượt này.

## Bẫy vận hành đã trả giá — đọc trước khi phóng lượt review

- **Lượt review nền CHẾT khi phiên điều phối nhàn rỗi.** Hai lượt chết ở `8,5` và `6` phút; lượt sống
  duy nhất là lượt duy nhất có phiên **BẬN liên tục** ở foreground. **`setsid` ĐÃ BỊ BÁC bằng phép đo**
  (`sid` tách hẳn mà vẫn chết). Đó là **TƯƠNG QUAN**, chưa phải nhân quả đã chứng minh — nhưng đủ để
  thành điều kiện vận hành: giữ phiên bận, mỗi lệnh chờ ≤ 600s, nối tiếp nhau.
- **`run.json` ghi `dang_chay` mà tiến trình đã chết là `KHÔNG ĐO ĐƯỢC`**, không phải "đang chạy".
  Kiểm **ba** tín hiệu: `trang_thai` + `os.kill(pid,0)` + mtime `stderr.log`.
- **ĐỪNG sửa tệp trong lúc suite đang chạy** — các ca sinh tiến trình con đọc tệp từ **ĐĨA**, nên phép
  đo hỏng **im lặng**. Đã sập hai lần.
- **Heredoc phải đóng ngoặc**: `<<'PY'` chứ không `<<PY`, kẻo dấu huyền thành thay thế lệnh và ăn mất
  chữ. Đã sập một lần trong chính packet này.
- **Đột biến phải chạy trên BẢN SAO TẠM**, không bao giờ ghi vào cây thật rồi khôi phục trong `finally`.
